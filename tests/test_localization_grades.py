"""Provenance must follow content, including generated text and deletions."""
import json
import sys

import pytest

from scripts import localization_grades as grades, validate, ai_context
from scripts.localization_policy import LOCALIZATION_GRADES, LOCALIZATION_GRADE_RANK


def write_loc(root, language="english", text="Hello", key="demo", mod="src"):
    path = root / mod / "main_menu/localization" / language / f"demo_l_{language}.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'l_{language}:\n {key}:0 "{text}"\n', encoding="utf-8-sig")
    return path


def save(root, data):
    path = root / grades.REGISTRY
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(grades.registry_bytes(data))


@pytest.fixture
def inventory(tmp_path, monkeypatch):
    monkeypatch.setattr(grades, "REPO_ROOT", tmp_path)
    for language in ("english", "simp_chinese", "french"):
        write_loc(tmp_path, language)
    write_loc(tmp_path, "english", mod="submods/compat")
    assert grades.main(["initialize"]) == 0
    return tmp_path


def test_initialization_order_and_each_entry(inventory):
    assert LOCALIZATION_GRADES == ("原创", "AI生成", "翻译", "占位", "缺失")
    assert list(LOCALIZATION_GRADE_RANK.values()) == [5, 4, 3, 2, 1]
    data = grades.load_registry(inventory)
    assert len(data["files"]) == 4
    for path, rows in data["files"].items():
        assert rows["demo"]["grade"] == ("翻译" if "/french/" in path else "AI生成")
    assert grades.check_registry(inventory) == []
    before = (inventory / grades.REGISTRY).read_bytes()
    with pytest.raises(SystemExit):
        grades.main(["initialize"])
    assert (inventory / grades.REGISTRY).read_bytes() == before


@pytest.mark.parametrize("grade", LOCALIZATION_GRADES)
def test_explicit_grade_roundtrip(grade):
    value = None if grade == "缺失" else 'Text $alias$ #Y 10#! \\n [ROOT.GetName]'
    evidence = {"original_basis": "user_requested", "note": "User explicitly requested original"} if grade == "原创" else {}
    record = grades.make_record(value, grade, **evidence)
    data = {"version": 1, "files": {"src/test.yml": {"demo": record}}}
    assert json.loads(grades.registry_bytes(data)) == data
    assert grades.entry_status(data, "src/test.yml", "demo", value)["grade"] == grade


@pytest.mark.parametrize("kwargs", [{}, {"original_basis": "agent", "note": "AI wrote it"},
                                   {"original_basis": "user_manual", "note": " "}])
def test_original_requires_evidence(kwargs):
    with pytest.raises(ValueError, match="原创 requires"):
        grades.make_record("text", "原创", **kwargs)


def test_manual_invalid_original_is_caught(inventory):
    data = grades.load_registry(inventory)
    next(iter(data["files"].values()))["demo"]["grade"] = "原创"
    save(inventory, data)
    assert "原创 lacks user provenance" in grades.check_registry(inventory)[0]


def test_changes_new_keys_deletions_and_prune(inventory):
    path = write_loc(inventory, text="Changed")
    assert any("stale" in error for error in grades.check_registry(inventory))
    assert grades.main(["register", "--files", str(path), "--grade", "占位"]) == 0
    assert grades.check_registry(inventory) == []
    write_loc(inventory, text="New", key="new")
    errors = grades.check_registry(inventory)
    assert any("unregistered" in error for error in errors)
    assert any("deleted text" in error for error in errors)
    grades.main(["register", "--files", str(path), "--grade", "AI生成"])
    grades.main(["prune"])
    assert grades.check_registry(inventory) == []


def test_unchanged_original_survives_bulk_but_changed_text_does_not():
    data = {"version": 1, "files": {}}
    grades.register_entries(data, "file", {"a": "Original"}, "原创",
                            original_basis="user_manual", note="User wrote this text")
    grades.register_entries(data, "file", {"a": "Original", "b": "New"}, "AI生成")
    assert data["files"]["file"]["a"]["grade"] == "原创"
    grades.register_entries(data, "file", {"a": "Rewritten"}, "AI生成")
    assert data["files"]["file"]["a"] == grades.make_record("Rewritten", "AI生成")


def test_translation_and_placeholder_are_explicit_not_language_defaults(inventory):
    path = write_loc(inventory, "english", "Translated to English")
    grades.main(["register", "--files", str(path), "--grade", "翻译"])
    data = grades.load_registry(inventory)
    relative = path.relative_to(inventory).as_posix()
    assert data["files"][relative]["demo"]["grade"] == "翻译"
    grades.main(["register", "--files", str(path), "--grade", "占位", "--replace"])
    assert grades.load_registry(inventory)["files"][relative]["demo"]["grade"] == "占位"


def test_missing_does_not_hide_text_or_waive_coverage():
    with pytest.raises(ValueError):
        grades.make_record("Exists", "缺失")
    with pytest.raises(ValueError):
        grades.make_record(None, "AI生成")
    assert grades.entry_status({"files": {}}, "file", "absent", None)["grade"] == "缺失"


def test_generated_rewrite_is_detected_without_modifying_game_bytes(inventory):
    before = {path: path.read_bytes() for path in grades.discover_files(inventory)}
    assert grades.check_registry(inventory) == []
    grades.main(["summary"])
    assert all(path.read_bytes() == content for path, content in before.items())
    path = write_loc(inventory, text="Generator changed $alias$")
    assert any(path.name in error and "stale" in error for error in grades.check_registry(inventory))


@pytest.mark.parametrize("no_changes", [True, False])
def test_validator_always_checks_grades_without_autofix(inventory, monkeypatch, capsys, no_changes):
    write_loc(inventory, text="Unregistered change")
    before = (inventory / grades.REGISTRY).read_bytes()
    monkeypatch.setattr(validate, "REPO_ROOT", inventory)
    monkeypatch.setattr(validate, "issues", [])
    monkeypatch.setattr(validate, "warnings", [])
    for name in dir(validate):
        if name.startswith("check_") and name not in ("check_loc_grades", "check_registry"):
            monkeypatch.setattr(validate, name, lambda *args, **kwargs: [])
    if no_changes:
        for name in ("load_anti_patterns", "load_valid_enums", "load_modifier_whitelist",
                     "load_hardcoded_on_actions", "load_warning_baseline"):
            monkeypatch.setattr(validate, name, lambda *args: [])
        monkeypatch.setattr(validate, "get_changed_files", lambda: [])
        monkeypatch.setattr(sys, "argv", ["validate.py", "--changed", "--fix", "--ai-report"])
        capsys.readouterr()
        with pytest.raises(SystemExit) as result:
            validate.main()
        assert result.value.code == 1
        assert json.loads(capsys.readouterr().out)["pass"] is False
    else:
        validate.run_global_checks([inventory / "scripts/unrelated.py"], True, [])
    assert any("LOC_GRADE" in error and "stale" in error for error in validate.issues)
    assert (inventory / grades.REGISTRY).read_bytes() == before


@pytest.mark.parametrize("path", ["scripts/localization_grades.py", "data/localization_grades.json",
                                 "data/wonder_localization.yaml", "great_projects_editor_web/services/localization_editor.py",
                                 "src/main_menu/localization/english/new_l_english.yml"])
def test_grading_work_routes_to_risk_card(path):
    context = ai_context.build_context([path], ai_context.load_routes())
    assert "docs/knowledge/risk_cards/localization.md" in {card["path"] for card in context["cards"]}
    alert = next(row for row in context["alerts"] if row["id"] == "localization_grade_registration")
    assert alert["severity"] == "required"
    assert "用户明确要求" in alert["message"]
