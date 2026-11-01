"""Generate per-wonder ownership choices and former-owner notifications."""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.naming import (
    EXTERNAL_LOWER_GENERIC_LEVEL_PUBLIC_EFFECT,
    EXTERNAL_LOWER_UNIQUE_LEVEL_PUBLIC_EFFECT,
    all_final_buildings,
    ownership_gain_event_id,
    ownership_loss_event_id,
    wonder_image_name,
)
from wonder_mechanics.render import render_header
from wonder_image_crop_lib import cropped_wonder_image_name

OUT_FILE = REPO_ROOT / "src" / "in_game" / "events" / "tv_wonder_ownership_events.txt"
SCRIPT_REL = "scripts_engineering_department/in_game/events/gen_tv_wonder_ownership_events.py"
T = "\t"
WONDER_IMAGE_DIR = "gfx/interface/icons/towards_victory/wonders"
PLUNDER_SUPPLY_SCALE = {"small": 1, "medium": 2, "large": 3}


def wonder_event_image(wonder: dict) -> str:
    return f"{WONDER_IMAGE_DIR}/{cropped_wonder_image_name(wonder_image_name(wonder))}.dds"


def append_choice_guard(lines: list[str], wonder: dict) -> None:
    """An open event must not reward a country after the site or wonder is lost."""
    lines.append(f"{T}{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}{T}scope:tv_wonder_ownership_site ?= {{")
    lines.append(f"{T}{T}{T}{T}{T}owner ?= root")
    lines.append(f"{T}{T}{T}{T}{T}var:tv_wonder_ownership_revision = scope:tv_wonder_ownership_revision")
    lines.append(f"{T}{T}{T}{T}{T}OR = {{")
    for building in all_final_buildings([wonder]):
        lines.append(f"{T}{T}{T}{T}{T}{T}location_building_level = {{ building_type = building_type:{building} value >= 1 }}")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}}}")


def append_loss_notification(lines: list[str], wonder: dict, result: int, indent: int) -> None:
    pad = T * indent
    lines.append(f"{pad}hidden_effect = {{")
    lines.append(f"{pad}{T}save_scope_value_as = {{ name = tv_wonder_ownership_choice value = {result} }}")
    lines.append(f"{pad}{T}scope:loser ?= {{")
    lines.append(f"{pad}{T}{T}trigger_event_non_silently = {{ id = tv_engineering_department.{ownership_loss_event_id(wonder)} }}")
    lines.append(f"{pad}{T}}}")
    lines.append(f"{pad}}}")


def append_ownership_gain_event(lines: list[str], wonder: dict) -> None:
    lines.append(f"tv_engineering_department.{ownership_gain_event_id(wonder)} = {{")
    lines.append(f"{T}type = country_event")
    lines.append(f"{T}title = tv_wonder_ownership.800.t")
    lines.append(f"{T}desc = tv_wonder_ownership.800.d")
    lines.append(f'{T}image = "{wonder_event_image(wonder)}"')
    lines.append(f"{T}outcome = positive")
    lines.append("")
    for suffix, weight, result in (("a", 80, 0), ("b", 20, 1)):
        lines.append(f"{T}option = {{")
        lines.append(f"{T}{T}name = tv_wonder_ownership.800.{suffix}")
        lines.append(f"{T}{T}ai_chance = {{ factor = {weight} }}")
        lines.append(f"{T}{T}if = {{")
        append_choice_guard(lines, wonder)
        if result == 0:
            lines.append(f"{T}{T}{T}add_prestige = 5")
        else:
            lines.append(f"{T}{T}{T}tv_sell_goods_with_temporary_supply_effect = {{")
            lines.append(f"{T}{T}{T}{T}market = scope:tv_wonder_ownership_site.market")
            lines.append(f"{T}{T}{T}{T}goods = goods:tv_wonder_materials")
            lines.append(f"{T}{T}{T}{T}amount = 20")
            lines.append(f"{T}{T}{T}{T}scale = {PLUNDER_SUPPLY_SCALE[wonder['size']]}")
            lines.append(f"{T}{T}{T}}}")
            effect = (EXTERNAL_LOWER_UNIQUE_LEVEL_PUBLIC_EFFECT if wonder.get("is_unique")
                      else EXTERNAL_LOWER_GENERIC_LEVEL_PUBLIC_EFFECT)
            lines.append(f"{T}{T}{T}scope:tv_wonder_ownership_site = {{")
            lines.append(f"{T}{T}{T}{T}{effect} = {{ wonder = {wonder['key']} }}")
            lines.append(f"{T}{T}{T}}}")
        append_loss_notification(lines, wonder, result, 3)
        lines.append(f"{T}{T}}}")
        lines.append(f"{T}{T}else = {{")
        append_loss_notification(lines, wonder, 2, 3)
        lines.append(f"{T}{T}}}")
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_ownership_loss_event(lines: list[str], wonder: dict) -> None:
    lines.append(f"tv_engineering_department.{ownership_loss_event_id(wonder)} = {{")
    lines.append(f"{T}type = country_event")
    lines.append(f"{T}title = tv_wonder_ownership.900.t")
    lines.append(f"{T}desc = {{")
    lines.append(f"{T}{T}first_valid = {{")
    for result, suffix in ((0, "preserved"), (1, "plundered"), (2, "stale")):
        lines.append(f"{T}{T}{T}triggered_desc = {{")
        lines.append(f"{T}{T}{T}{T}trigger = {{ scope:tv_wonder_ownership_choice ?= {result} }}")
        lines.append(f"{T}{T}{T}{T}desc = tv_wonder_ownership.900.d_{suffix}")
        lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}triggered_desc = {{ desc = tv_wonder_ownership.900.d }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append(f'{T}image = "{wonder_event_image(wonder)}"')
    lines.append(f"{T}outcome = negative")
    lines.append("")
    lines.append(f"{T}option = {{")
    lines.append(f"{T}{T}name = tv_wonder_ownership.900.a")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def generate() -> str:
    all_wonders, _mechanics = load_all_wonder_mechanics()
    lines = render_header(SCRIPT_REL)
    lines.append("namespace = tv_engineering_department")
    lines.append("")
    lines.append("# Event IDs intentionally remain 8000 + wonder id and 9000 + wonder id.")
    lines.append("# Only event dispatch is per-wonder; ownership state handling is in tv_wonder_ownership_effects.txt.")
    lines.append("")
    for wonder in all_wonders:
        append_ownership_gain_event(lines, wonder)
    for wonder in all_wonders:
        append_ownership_loss_event(lines, wonder)
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUT_FILE.write_text("\ufeff" + generate(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
