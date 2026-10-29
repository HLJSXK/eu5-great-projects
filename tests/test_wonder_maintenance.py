"""Check the shipped upkeep recipes and every generic/unique wonder carrier."""

from pathlib import Path
import re

import pytest

from scripts_engineering_department.wonder_mechanics.io import load_all_wonder_mechanics
from scripts_engineering_department.wonder_mechanics.naming import PARTS, final_building


ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "src/in_game/common"
WONDERS, _ = load_all_wonder_mechanics()


def blocks(path):
    return dict(re.findall(r"(?ms)^(\w+) = \{(.*?)^\}", path.read_text(encoding="utf-8-sig")))


METHODS = blocks(COMMON / "production_methods/tv_engineering_department_production_methods.txt")
BUILDINGS = {
    **blocks(COMMON / "building_types/tv_wonder_module_buildings.txt"),
    **blocks(COMMON / "building_types/tv_engineering_department_wonder_mechanics_buildings.txt"),
}


@pytest.mark.parametrize("wonder", WONDERS, ids=lambda wonder: wonder["key"])
def test_each_wonder_carrier_consumes_size_based_maintenance(wonder):
    # Unique wonder reward multipliers must not multiply their maintenance.
    x = {"small": 1, "medium": 2, "large": 3}[wonder["size"]]
    carriers = [
        *[(f"tv_wonder_{wonder['key']}_{part}", {"tv_wonder_materials": x}) for part in PARTS],
        (f"tv_wonder_{wonder['key']}", {"tv_wonder_materials": 2 * x}),
        (final_building(wonder), {"tv_wonder_materials": 2 * x, "tools": 2 * x}),
    ]
    for building, expected in carriers:
        method_block = re.search(r"possible_production_methods = \{([^}]+)\}", BUILDINGS[building])
        assert method_block, building
        methods = method_block[1].split()
        assert len(methods) == 1, building
        fields = dict(re.findall(r"(?m)^\s*(\w+) = (\S+)\s*$", METHODS[methods[0]]))
        assert fields.pop("category") == "building_maintenance", building
        assert {key: float(value) for key, value in fields.items()} == expected, building


@pytest.mark.parametrize("language", ("english", "simp_chinese"))
def test_size_based_maintenance_names_are_localized(language):
    path = ROOT / f"src/main_menu/localization/{language}/tv_engineering_department_l_{language}.yml"
    assert path.read_bytes().startswith(b"\xef\xbb\xbf")
    text = path.read_text(encoding="utf-8-sig")
    for stage in ("module", "shell", "final"):
        for size in ("small", "medium", "large"):
            key = f"tv_wonder_{stage}_{size}_maintenance"
            assert key in METHODS
            assert re.search(rf'^ {key}:\d* "[^"\n]+"$', text, re.MULTILINE), key
