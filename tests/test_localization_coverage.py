"""All-language parity must fail in both CLI modes, including deletion-only runs."""
import json
import shutil
import sys

import pytest

from scripts import validate
from scripts.localization_policy import LOCALIZATION_LANGUAGES


def write_loc(root, language, keys, relative="test.yml", header=None):
    path = root / "main_menu/localization" / language / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"l_{header or language}:\n" + "".join(f' {key}:0 "English fallback"\n' for key in keys)
    path.write_text(text, encoding="utf-8-sig")
    return path


@pytest.fixture
def mod(tmp_path, monkeypatch):
    root = tmp_path / "src"
    monkeypatch.setattr(validate, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(validate, "MOD_ROOTS", (root,))
    monkeypatch.setattr(validate, "issues", [])
    monkeypatch.setattr(validate, "warnings", [])
    for language in LOCALIZATION_LANGUAGES:
        write_loc(root, language, ["shared"])
    return root


def coverage():
    validate.check_loc_coverage()
    return [validate._parse_issue_structured(issue) for issue in validate.issues]


def test_complete_english_fallback_is_valid(mod):
    assert len(LOCALIZATION_LANGUAGES) == 11
    assert coverage() == []


@pytest.mark.parametrize("language", LOCALIZATION_LANGUAGES)
def test_missing_key_in_any_language_fails(mod, language):
    write_loc(mod, language, [])
    errors = coverage()
    assert len(errors) == 1
    assert errors[0]["rule"] == "loc_coverage"
    assert f"'shared' is missing from {language} in " in errors[0]["message"]
    assert errors[0]["line"] == 2
    assert errors[0]["file"].endswith("test.yml")


@pytest.mark.parametrize("language", ["simp_chinese", "french", "japanese"])
def test_non_english_only_key_is_checked_in_reverse(mod, language):
    write_loc(mod, language, ["foreign.only-key"], "events/extra.yml")
    errors = coverage()
    assert len(errors) == 1
    assert "foreign.only-key" in errors[0]["message"]
    assert "english" in errors[0]["message"]
    assert f"/{language}/events/extra.yml" in errors[0]["file"].replace("\\", "/")


@pytest.mark.parametrize("mode", ["directory", "file", "empty_directory"])
def test_deleting_locale_cannot_hide_missing_keys(mod, mode):
    folder = mod / "main_menu/localization/korean"
    if mode == "directory":
        shutil.rmtree(folder)
    else:
        (folder / "test.yml").unlink()
    if mode == "file":
        write_loc(mod, "korean", [], "unrelated.yml")
    assert "'shared' is missing from korean in " in coverage()[0]["message"]


def test_language_sets_can_use_different_filenames_and_nested_folders(mod):
    for language in LOCALIZATION_LANGUAGES:
        write_loc(mod, language, ["event.1001.t", "key-with-hyphen"], f"events/{language}.yml")
    assert coverage() == []


def test_keys_without_indentation_are_not_skipped(mod):
    path = write_loc(mod, "english", [], "unindented.yml")
    path.write_text('l_english:\nno_indent:0 "text"\n # commented:0 "ignore"\n', encoding="utf-8-sig")
    errors = coverage()
    assert len(errors) == 1
    assert "no_indent" in errors[0]["message"]


def test_wrong_language_header_does_not_satisfy_coverage(mod):
    write_loc(mod, "french", ["shared"], header="english")
    errors = coverage()
    assert {error["rule"] for error in errors} == {"loc_language", "loc_coverage"}
    assert "l_french:" in errors[0]["message"]


def test_extra_language_is_also_compared(mod):
    write_loc(mod, "test_language", ["shared", "extra_only"])
    errors = coverage()
    assert len(errors) == 1
    assert "extra_only" in errors[0]["message"]


def test_other_mod_root_cannot_fill_a_missing_translation(mod, monkeypatch):
    other = mod.parent / "other_mod"
    for language in LOCALIZATION_LANGUAGES:
        write_loc(other, language, ["shared"])
    write_loc(mod, "french", [])
    monkeypatch.setattr(validate, "MOD_ROOTS", (mod, other))
    errors = coverage()
    assert len(errors) == 1
    assert errors[0]["message"].replace("\\", "/").endswith("src/main_menu/localization")


@pytest.mark.parametrize("ai_report", [False, True])
@pytest.mark.parametrize("changed", [False, True])
def test_cli_fails_for_parity_even_with_no_existing_changed_files(mod, monkeypatch, capsys, ai_report, changed):
    (mod / "main_menu/localization/spanish/test.yml").unlink()
    monkeypatch.setattr(validate, "load_anti_patterns", lambda _: [])
    monkeypatch.setattr(validate, "load_valid_enums", lambda _: {})
    monkeypatch.setattr(validate, "load_modifier_whitelist", lambda: set())
    monkeypatch.setattr(validate, "load_hardcoded_on_actions", lambda: set())
    monkeypatch.setattr(validate, "load_warning_baseline", lambda: [])
    monkeypatch.setattr(validate, "get_changed_files", lambda: [])
    monkeypatch.setattr(validate, "collect_files", lambda _: [])
    argv = ["validate.py", "--fix"]
    if changed:
        argv.append("--changed")
    if ai_report:
        argv.append("--ai-report")
    monkeypatch.setattr(sys, "argv", argv)
    with pytest.raises(SystemExit) as result:
        validate.main()
    assert result.value.code == 1
    output = capsys.readouterr().out
    if ai_report:
        report = json.loads(output)
        assert report["pass"] is False
        assert report["errors"][0]["rule"] == "loc_coverage"
    else:
        assert "[FAIL]" in output
    assert not (mod / "main_menu/localization/spanish/test.yml").exists()


def test_unrelated_changed_file_still_runs_parity(mod, monkeypatch):
    write_loc(mod, "german", [])
    for name in dir(validate):
        if name.startswith("check_") and name != "check_loc_coverage":
            monkeypatch.setattr(validate, name, lambda *args, **kwargs: None)
    validate.run_global_checks([mod.parent / "scripts/unrelated.py"], True, [])
    assert len(validate.issues) == 1
    assert "missing from german" in validate.issues[0]


def test_modifier_key_catalog_includes_all_languages(mod):
    assert set(validate._loc_keys_by_language()) == set(LOCALIZATION_LANGUAGES)
    assert all("shared" in keys for keys in validate._loc_keys_by_language().values())
