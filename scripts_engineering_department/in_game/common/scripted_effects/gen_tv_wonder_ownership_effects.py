"""Generate Engineering Department wonder ownership-transfer effects."""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.naming import (
    FINAL_BUILDING_LEVEL_BY_TYPE_MAP,
    ownership_gain_event_id,
    ownership_loss_event_id,
)
from wonder_mechanics.render import render_header

OUT_FILE = REPO_ROOT / "src" / "in_game" / "common" / "scripted_effects" / "tv_wonder_ownership_effects.txt"
SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ownership_effects.py"
T = "\t"

FINAL_BUILDING_WONDER_ID_MAP = "tv_wonder_final_building_type_to_wonder_id"
LOCATION_SURVEY_SCALE_TIER_MAP = "tv_wonder_survey_scale_tier"
PRIORITY_CANDIDATE_WONDER_ID_VAR = "tv_wonder_priority_candidate_wonder_id"
PRIORITY_CANDIDATE_CURRENT_MODE_VAR = "tv_wonder_priority_candidate_current_mode"
OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL = "tv_wonder_ownership_final_building_type"
OWNERSHIP_FINAL_BUILDING_LEVEL_VAR = "tv_wonder_ownership_final_building_level"
OWNERSHIP_SCALE_TIER_VAR = "tv_wonder_ownership_scale_tier"
OWNERSHIP_EVENT_WONDER_ID_VAR = "tv_wonder_ownership_event_wonder_id"
OWNERSHIP_LOSS_RETAINS_SAME_WONDER_VAR = "tv_wonder_ownership_loss_retains_same_wonder"
OWNERSHIP_TARGET_WONDER_ID_LOCAL = "tv_wonder_ownership_target_wonder_id"
OWNERSHIP_SCANNED_WONDER_ID_LOCAL = "tv_wonder_ownership_scanned_wonder_id"


def append_location_owner_changed_handler(lines: list[str]) -> None:
    lines.append("# Root: changed location. scope:winner is the new owner; scope:loser is the old owner.")
    lines.append("# Scans final-building maps so all non-event ownership work remains data-driven.")
    lines.append("tv_wonder_ownership_handle_location_owner_changed_effect = {")
    lines.append("\tclear_saved_scope = tv_wonder_ritual_sync_country")
    lines.append("\tscope:loser ?= { save_scope_as = tv_wonder_ritual_sync_country }")
    lines.append("\ttv_wonder_ritual_revoke_location_effect = yes")
    lines.append(f"{T}save_scope_as = tv_wonder_priority_site")
    lines.append(f"{T}save_scope_as = tv_wonder_ownership_site")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ NOT = {{ has_variable = tv_wonder_ownership_revision }} }}")
    lines.append(f"{T}{T}set_variable = {{ name = tv_wonder_ownership_revision value = 0 }}")
    lines.append(f"{T}}}")
    lines.append(f"{T}change_variable = {{ name = tv_wonder_ownership_revision add = 1 }}")
    lines.append(f"{T}save_scope_value_as = {{ name = tv_wonder_ownership_revision value = var:tv_wonder_ownership_revision }}")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ has_global_variable_map = {FINAL_BUILDING_WONDER_ID_MAP} }}")
    lines.append(f"{T}{T}every_key_in_global_variable_map = {{")
    lines.append(f"{T}{T}{T}variable = {FINAL_BUILDING_WONDER_ID_MAP}")
    lines.append(f"{T}{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}{T}scope:tv_wonder_ownership_site = {{")
    lines.append(f"{T}{T}{T}{T}{T}has_variable_map = {FINAL_BUILDING_LEVEL_BY_TYPE_MAP}")
    lines.append(
        f"{T}{T}{T}{T}{T}is_key_in_variable_map = {{ "
        f"name = {FINAL_BUILDING_LEVEL_BY_TYPE_MAP} target = prev }}"
    )
    lines.append(f"{T}{T}{T}{T}{T}location_building_level = {{ building_type = prev value >= 1 }}")
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}}}")
    # Capture the real style, not the first of a generic wonder's three building types.
    # The type scope also survives level-one demolition for the result notification.
    lines.append(f"{T}{T}{T}save_scope_as = tv_wonder_ownership_building_type")
    lines.append(f"{T}{T}{T}scope:tv_wonder_ownership_site = {{")
    lines.append(
        f"{T}{T}{T}{T}set_local_variable = {{ "
        f"name = {OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL} value = prev }}"
    )
    lines.append(
        f"{T}{T}{T}{T}set_variable = {{ name = {OWNERSHIP_FINAL_BUILDING_LEVEL_VAR} "
        f"value = \"variable_map({FINAL_BUILDING_LEVEL_BY_TYPE_MAP}|local_var:{OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL})\" }}"
    )
    lines.append(f"{T}{T}{T}{T}remove_local_variable = {OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}scope:loser ?= {{")
    lines.append(
        f"{T}{T}{T}{T}set_local_variable = {{ "
        f"name = {OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL} value = prev }}"
    )
    lines.append(
        f"{T}{T}{T}{T}set_variable = {{ name = {PRIORITY_CANDIDATE_WONDER_ID_VAR} "
        f"value = \"global_variable_map({FINAL_BUILDING_WONDER_ID_MAP}|local_var:{OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL})\" }}"
    )
    # Lost sites stay in the old country registry until owned and revalidated.

    lines.append(
        f"{T}{T}{T}{T}set_variable = {{ "
        f"name = {OWNERSHIP_EVENT_WONDER_ID_VAR} value = var:{PRIORITY_CANDIDATE_WONDER_ID_VAR} }}"
    )
    lines.append(f"{T}{T}{T}{T}tv_wonder_ownership_cleanup_loss_effect = yes")
    lines.append(f"{T}{T}{T}{T}if = {{")
    lines.append(f"{T}{T}{T}{T}{T}limit = {{ NOT = {{ exists = scope:winner }} }}")
    lines.append(f"{T}{T}{T}{T}{T}save_scope_value_as = {{ name = tv_wonder_ownership_choice value = 2 }}")
    lines.append(f"{T}{T}{T}{T}{T}tv_wonder_ownership_trigger_loss_event_effect = yes")
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}remove_variable = {OWNERSHIP_EVENT_WONDER_ID_VAR}")
    lines.append(f"{T}{T}{T}{T}remove_variable = {PRIORITY_CANDIDATE_WONDER_ID_VAR}")
    lines.append(f"{T}{T}{T}{T}remove_local_variable = {OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}scope:winner ?= {{")
    lines.append(
        f"{T}{T}{T}{T}set_local_variable = {{ "
        f"name = {OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL} value = prev }}"
    )
    lines.append(
        f"{T}{T}{T}{T}set_variable = {{ name = {PRIORITY_CANDIDATE_WONDER_ID_VAR} "
        f"value = \"global_variable_map({FINAL_BUILDING_WONDER_ID_MAP}|local_var:{OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL})\" }}"
    )
    lines.append(f"{T}{T}{T}{T}tv_wonder_find_current_site_priority_candidate_effect = yes")
    lines.append(f"{T}{T}{T}{T}if = {{")
    lines.append(f"{T}{T}{T}{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}NOT = {{ has_variable = tv_wonder_priority_existing_site_candidate }}")
    # Unfinished work belongs to the losing country's resume record. The loss
    # callback runs after this handler and preserves that record for recovery.
    lines.append(f"{T}{T}{T}{T}{T}{T}NOT = {{ scope:loser ?= {{ var:tv_wonder_site ?= scope:tv_wonder_ownership_site NOT = {{ has_variable = tv_wonder_finalized }} }} }}")
    lines.append(f"{T}{T}{T}{T}{T}{T}scope:tv_wonder_ownership_site = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}has_variable_map = {LOCATION_SURVEY_SCALE_TIER_MAP}")
    lines.append(
        f"{T}{T}{T}{T}{T}{T}{T}is_key_in_variable_map = {{ "
        f"name = {LOCATION_SURVEY_SCALE_TIER_MAP} target = prev.var:{PRIORITY_CANDIDATE_WONDER_ID_VAR} }}"
    )
    lines.append(f"{T}{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}{T}scope:tv_wonder_ownership_site = {{")
    lines.append(
        f"{T}{T}{T}{T}{T}{T}set_variable = {{ name = {OWNERSHIP_SCALE_TIER_VAR} "
        f"value = \"variable_map({LOCATION_SURVEY_SCALE_TIER_MAP}|prev.var:{PRIORITY_CANDIDATE_WONDER_ID_VAR})\" }}"
    )
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}{T}if = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}scope:tv_wonder_ownership_site = {{")
    lines.append(
        f"{T}{T}{T}{T}{T}{T}{T}{T}var:{OWNERSHIP_SCALE_TIER_VAR} > "
        f"var:{OWNERSHIP_FINAL_BUILDING_LEVEL_VAR}"
    )
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}{T}{T}}}")
    lines.append(
        f"{T}{T}{T}{T}{T}{T}set_variable = {{ "
        f"name = {PRIORITY_CANDIDATE_CURRENT_MODE_VAR} value = 2 }}"
    )
    lines.append(f"{T}{T}{T}{T}{T}{T}tv_wonder_register_current_priority_candidate_effect = yes")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}{T}scope:tv_wonder_ownership_site = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}remove_variable = {OWNERSHIP_SCALE_TIER_VAR}")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(
        f"{T}{T}{T}{T}set_variable = {{ "
        f"name = {OWNERSHIP_EVENT_WONDER_ID_VAR} value = var:{PRIORITY_CANDIDATE_WONDER_ID_VAR} }}"
    )
    lines.append(f"{T}{T}{T}{T}tv_wonder_ownership_trigger_gain_event_effect = yes")
    lines.append(f"{T}{T}{T}{T}remove_variable = {OWNERSHIP_EVENT_WONDER_ID_VAR}")
    lines.append(f"{T}{T}{T}{T}remove_variable = {PRIORITY_CANDIDATE_WONDER_ID_VAR}")
    lines.append(f"{T}{T}{T}{T}remove_variable = {PRIORITY_CANDIDATE_CURRENT_MODE_VAR}")
    lines.append(f"{T}{T}{T}{T}remove_variable = tv_wonder_priority_existing_site_candidate")
    lines.append(f"{T}{T}{T}{T}remove_local_variable = {OWNERSHIP_FINAL_BUILDING_TYPE_LOCAL}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}scope:tv_wonder_ownership_site = {{")
    lines.append(f"{T}{T}{T}{T}remove_variable = {OWNERSHIP_FINAL_BUILDING_LEVEL_VAR}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_loss_cleanup_effect(lines: list[str], all_wonders: list[dict], mechanics: dict) -> None:
    lines.extend(["tv_wonder_ownership_cleanup_loss_effect = {", "\ttv_wonder_mechanics_refresh_country_auto_level_map_effect = yes", "}", ""])


def append_event_dispatch_effects(lines: list[str], all_wonders: list[dict]) -> None:
    lines.append("# Intentional per-wonder dispatch: events need static ids and static images.")
    lines.append("tv_wonder_ownership_trigger_gain_event_effect = {")
    for index, wonder in enumerate(all_wonders):
        head = "if" if index == 0 else "else_if"
        lines.append(f"{T}{head} = {{")
        lines.append(f"{T}{T}limit = {{ var:{OWNERSHIP_EVENT_WONDER_ID_VAR} ?= {int(wonder['id'])} }}")
        lines.append(
            f"{T}{T}trigger_event_non_silently = {{ id = tv_engineering_department.{ownership_gain_event_id(wonder)} }}"
        )
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append("# Intentional per-wonder dispatch: events need static ids and static images.")
    lines.append("tv_wonder_ownership_trigger_loss_event_effect = {")
    for index, wonder in enumerate(all_wonders):
        head = "if" if index == 0 else "else_if"
        lines.append(f"{T}{head} = {{")
        lines.append(f"{T}{T}limit = {{ var:{OWNERSHIP_EVENT_WONDER_ID_VAR} ?= {int(wonder['id'])} }}")
        lines.append(
            f"{T}{T}trigger_event_non_silently = {{ id = tv_engineering_department.{ownership_loss_event_id(wonder)} }}"
        )
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def generate() -> str:
    all_wonders, mechanics = load_all_wonder_mechanics()
    lines = render_header(SCRIPT_REL)
    lines.append("# Wonder ownership-transfer lifecycle.")
    lines.append("# Keep event dispatch static; keep final-building detection and cache updates map-driven.")
    lines.append("")
    append_location_owner_changed_handler(lines)
    append_loss_cleanup_effect(lines, all_wonders, mechanics)
    append_event_dispatch_effects(lines, all_wonders)
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUT_FILE.write_text("\ufeff" + generate(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
