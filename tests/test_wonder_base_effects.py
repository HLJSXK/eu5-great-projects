"""Instant base packages: validation, inheritance and generated payout branches."""
from copy import deepcopy

import pytest

from scripts_engineering_department.wonder_mechanics import _core as core
from test_wonder_priority_proposals import parse, child, walk
from scripts_engineering_department.in_game.common.scripted_effects.gen_tv_wonder_finalization_effects import append_visible_effect, generate


@pytest.fixture(scope="module")
def data():
    return core.load_all_wonder_mechanics()


def test_shipped_data_has_no_instant_rewards_or_runtime_change(data):
    wonders, mechanics = data
    assert mechanics["base_instant_effects"] == {}
    assert all(core.wonder_base_instant_effects(w, mechanics) == [] for w in wonders)
    path = core.REPO_ROOT / "src/in_game/common/scripted_effects/tv_wonder_finalization_effects.txt"
    assert generate() == path.read_text(encoding="utf-8-sig")


@pytest.mark.parametrize("value", [True, None, "add_gold = 100", "nan", float("inf"), {}, []])
def test_invalid_amounts_rejected(value):
    with pytest.raises(ValueError):
        core.validate_base_instant_effects({"sample": [{"type": "gold", "value": value}]}, mechanic_keys={"sample"})


@pytest.mark.parametrize("package", [
    {"unknown": []}, {"sample": {}}, {"sample": [{"type": "unknown", "value": 1}]},
    {"sample": [{"type": "gold"}]}, {"sample": [{"type": "gold", "value": 1, "scope": "root"}]},
])
def test_invalid_packages_rejected(package):
    with pytest.raises((ValueError, TypeError)):
        core.validate_base_instant_effects(package, mechanic_keys={"sample"})


def test_scaled_inheritance_does_not_mutate_sources(data):
    wonders, mechanics = data
    unique = next(w for w in wonders if w["is_unique"])
    generic = next(w for w in wonders if w["key"] == unique["mechanic_key"])
    mechanics = {**mechanics, "base_instant_effects": {generic["key"]: [{"type": "gold", "value": 2.5}]}}
    before = deepcopy(mechanics)
    assert core.wonder_base_instant_effects(unique, mechanics, 3) == [{"type": "gold", "value": 15}]
    assert core.wonder_base_instant_effects(generic, mechanics, 3) == [{"type": "gold", "value": 7.5}]
    assert core.wonder_base_instant_effects(unique, mechanics, 0) == []
    assert mechanics == before


@pytest.mark.parametrize("unique", [False, True])
def test_native_payout_branches_pay_new_levels_only(data, unique):
    wonders, mechanics = data
    wonder = next(w for w in wonders if w["is_unique"] == unique)
    mechanics = {**mechanics, "base_instant_effects": {wonder["mechanic_key"]: [
        {"type": "gold", "value": 3}, {"type": "development", "value": 0.00001},
    ]}}
    lines = []
    append_visible_effect(lines, wonder, mechanics)
    body = child(parse("\n".join(lines))[0].children, "if").children
    branches = [n for n in body if n.key == "if"]
    assert len(branches) == 6
    multiplier = wonder["base_effect_multiplier"]
    for base, branch in enumerate(branches):
        limit = child(branch.children, "limit").children
        assert child(limit, "var:tv_wonder_project_mode").value == str(1 if base == 0 else 2)
        if base:
            assert child(limit, "var:tv_wonder_project_base_level").value == str(base)
        payouts = [n for n in branch.children if n.key in ("if", "else_if")]
        assert len(payouts) == 6 - base
        for level, payout in enumerate(payouts, base + 1):
            assert child(child(payout.children, "limit").children, "var:tv_wonder_level").value == str(level)
            assert float(child(payout.children, "add_gold").value) == 3 * (level - base) * multiplier
            location = child(payout.children, "var:tv_wonder_site")
            assert float(child(location.children, "change_development").value) == pytest.approx(0.00001 * (level - base) * multiplier)
    assert not any(n.key in ("set_variable", "set_local_variable", "every_owned_location") for n in walk(body))


def test_atlas_uses_same_scaled_package(data):
    from unique_wonders_site.scripts.build import build_wonders as atlas
    wonders, mechanics = data
    generic = next(w for w in wonders if not w["is_unique"])
    mechanics = {**mechanics, "base_instant_effects": {generic["key"]: [{"type": "gold", "value": 4}]}}
    loc = {"english": {}, "simp_chinese": {}}
    record = atlas.build_record(generic, base_wonders={generic["key"]: generic}, mechanics=mechanics,
        loc_data=loc, locations_index={}, reference_loc={}, modifier_index={}, trigger_index={})
    instant = next(section for section in record["effects"] if section["id"] == "base_instant_effects")
    assert instant["rows"][0]["value"] == 4
