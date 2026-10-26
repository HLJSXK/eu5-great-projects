"""Shared rule semantics and applicability stay in the shared registries."""
import inspect
from pathlib import Path
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = (ROOT / ".eu5-base").resolve()
sys.path.insert(0, str(ROOT))
from scripts import validate
from knowledge_loader import load_anti_patterns, validate_migration_coverage

RULE_IDS = {"eu4_province_modifier_scope", "yaml_localization_non_ascii_quotes"}


@pytest.mark.parametrize("root", [BASE, ROOT], ids=["base", "workspace"])
def test_shared_rules_load_without_local_overrides(root):
    assert validate_migration_coverage(root)["base_entries"] > 0
    authority = {r["id"]: r for r in yaml.safe_load((BASE / "docs/knowledge/anti_patterns.yaml").read_text(encoding="utf-8-sig"))}
    view = {r["id"]: r for r in yaml.safe_load((BASE / "docs/knowledge/anti_patterns_shared.yaml").read_text(encoding="utf-8-sig"))}
    loaded = {r["id"]: r for r in load_anti_patterns(root)}
    for key in RULE_IDS:
        assert loaded[key] == authority[key] == view[key]


def test_province_rule_records_native_scope_and_requires_typed_analysis():
    rule = next(r for r in load_anti_patterns(ROOT) if r["id"] == "eu4_province_modifier_scope")
    assert rule["detectability"] == "needs_parser" and not rule["pattern"]
    assert "province scope" in rule["correction"]
    assert "location scope" in rule["correction"] and "country scope" in rule["correction"]
    assert "effects.log:367" in rule["source"]
    assert not validate.compile_anti_patterns([rule])


def test_localization_path_metadata_filters_script_comments(monkeypatch):
    monkeypatch.setattr(validate, "issues", [])
    rule = next(r for r in load_anti_patterns(ROOT) if r["id"] == "yaml_localization_non_ascii_quotes")
    compiled = validate.compile_anti_patterns([rule])
    assert compiled[0]["only_in"] == ("/localization/",)
    validate.check_anti_patterns(ROOT / "src/in_game/events/check.txt", "event.1 = { # d’Opera\n}", compiled)
    assert not validate.issues
    validate.check_anti_patterns(ROOT / "src/main_menu/localization/english/check.yml", " key: “text”", compiled)
    assert len(validate.issues) == 2


def test_validator_has_no_rule_id_exceptions_or_scope_name_guesses():
    source = inspect.getsource(validate.check_anti_patterns)
    assert all(key not in source for key in RULE_IDS)
    assert not hasattr(validate, "_modifier_scope_at")
