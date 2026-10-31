"""Generate Engineering Department wonder finalization effects."""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.rituals import ritual_styles
from wonder_mechanics.naming import (
    final_building_completion_sync_hidden_event_execute_effect_name,
    final_building_completion_sync_hidden_event_id,
    final_building_completion_sync_hidden_event_trigger_effect_name,
    FINAL_BUILDING_LEVEL_BY_TYPE_MAP,
    construct_final_building_effect_name,
    finalization_event_id,
    finalization_hidden_event_execute_effect_name,
    finalization_hidden_event_id,
    finalization_hidden_event_trigger_effect_name,
    finalization_hidden_effect_name,
    finalization_visible_effect_name,
    finalization_world_event_id,
    finalization_world_expansion_event_id,
)
from wonder_mechanics.render import monthly_country_pulse_event, render_header
from wonder_ritual_codegen import max_level_cache, plain_cache

OUT_FILE = REPO_ROOT / "src" / "in_game" / "common" / "scripted_effects" / "tv_wonder_finalization_effects.txt"
SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_finalization_effects.py"
DATA_REL = (
    "data/wonders.yaml + data/wonder_final_buildings.yaml + data/wonder_generic_rituals.yaml + "
    "data/wonder_base_modifiers.yaml + data/wonder_site_rules.yaml + data/unique_wonders.yaml + "
    "data/pulse_registry.yaml"
)
T = "\t"
FINAL_BUILDING_COMPLETION_SYNC_QUEUED_VAR = "tv_wonder_final_building_completion_sync_queued"

def building_type_ref(building: str) -> str:
    return building if building.startswith("building_type:") else f"building_type:{building}"


def loc_level(building: str, op: str, level: int) -> str:
    return f"location_building_level = {{ building_type = {building_type_ref(building)} value {op} {level} }}"


def change_level_lines(building: str, value: int, indent: int) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}change_building_level_in_location = {{",
        f"{prefix}{T}building = {building_type_ref(building)}",
        f"{prefix}{T}value = {value}",
        f"{prefix}{T}owner = prev",
        f"{prefix}}}",
    ]


def append_store_final_building_level(lines: list[str], building: str, level: str, indent: int) -> None:
    prefix = T * indent
    building_type = building_type_ref(building)
    lines.append(f"{prefix}remove_from_variable_map = {{ name = {FINAL_BUILDING_LEVEL_BY_TYPE_MAP} key = {building_type} }}")
    lines.append(
        f"{prefix}add_to_variable_map = {{ name = {FINAL_BUILDING_LEVEL_BY_TYPE_MAP} "
        f"key = {building_type} value = {level} }}"
    )
    lines.append(f"{prefix}tv_wonder_mechanics_refresh_location_display_state_effect = yes")


def append_hidden_event_trigger_effect(lines: list[str]) -> None:
    lines.append(f"{finalization_hidden_event_trigger_effect_name()} = {{")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_finalization_preview_ready")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_locked")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_finalization_outcome")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}trigger_event_silently = tv_engineering_department.{finalization_hidden_event_id()}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_hidden_event_execute_effect(lines: list[str], wonders: list[dict]) -> None:
    lines.append(f"{finalization_hidden_event_execute_effect_name()} = {{")
    for wonder in wonders:
        lines.append(f"\tif = {{ limit = {{ has_variable = tv_wonder_finalization_preview_ready var:tv_wonder_locked ?= {wonder['id']} }} {finalization_hidden_effect_name(wonder)} = yes }}")
    lines.extend(["}", ""])


def append_final_building_completion_sync_hidden_event_effects(lines: list[str], wonders: list[dict]) -> None:
    lines.append(f"{final_building_completion_sync_hidden_event_trigger_effect_name()} = {{")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ NOT = {{ has_variable = {FINAL_BUILDING_COMPLETION_SYNC_QUEUED_VAR} }} }}")
    lines.append(
        f"{T}{T}set_variable = {{ name = {FINAL_BUILDING_COMPLETION_SYNC_QUEUED_VAR} value = 1 }}"
    )
    lines.append(
        f"{T}{T}trigger_event_silently = {{ id = tv_engineering_department.{final_building_completion_sync_hidden_event_id()} days = 1 }}"
    )
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append(f"{final_building_completion_sync_hidden_event_execute_effect_name()} = {{")
    lines.append(f"{T}remove_variable = {FINAL_BUILDING_COMPLETION_SYNC_QUEUED_VAR}")
    lines.append(f"{T}tv_wonder_mechanics_sync_location_final_building_level_map_from_buildings_effect = yes")
    # Start the same native construction as the vanilla canal decision, after the
    # engine has committed the completed building level. Native construction owns
    # the remaining work and eventual opening; expansions must not restart it.
    for wonder in wonders:
        if not wonder.get("native_canal"):
            continue
        lines.extend([
            f"{T}if = {{",
            f"{T}{T}limit = {{",
            f"{T}{T}{T}this = location:{wonder['location']}",
            f"{T}{T}{T}exists = owner",
            f"{T}{T}{T}{loc_level(wonder['final_building'], '>=', 1)}",
            f"{T}{T}{T}is_canal_open = no",
            f"{T}{T}{T}NOT = {{ has_canal_construction = yes }}",
            f"{T}{T}}}",
            f"{T}{T}start_canal_construction = {{ }}",
            f"{T}}}",
        ])
    lines.append(f"{T}tv_wonder_mechanics_refresh_location_display_state_effect = yes")
    lines.append("}")
    lines.append("")


def destroy_intermediate_effect_name(wonder: dict) -> str:
    return f"tv_wonder_{wonder['key']}_destroy_finalization_intermediate_buildings_effect"


def broadcast_effect_name(wonder: dict) -> str:
    return f"tv_wonder_{wonder['key']}_broadcast_finalization_completion_event_effect"


def append_static_final_building_construction(lines: list[str], building: str, indent: int) -> None:
    prefix = T * indent
    lines.append(f"{prefix}if = {{")
    lines.append(f"{prefix}{T}limit = {{")
    lines.append(f"{prefix}{T}{T}NOT = {{ has_building = {building_type_ref(building)} }}")
    lines.append(f"{prefix}{T}{T}prev = {{ var:tv_wonder_level ?= {{ this >= 1 }} }}")
    lines.append(f"{prefix}{T}}}")
    lines.append(
        f"{prefix}{T}construct_building = {{ building_type = {building_type_ref(building)} "
        f"cost_multiplier = 0 cost_multiplier_reason = \"game_concept_event\" instant = yes }}"
    )
    for level in range(6, 1, -1):
        head = "if" if level == 6 else "else_if"
        lines.append(f"{prefix}{T}{head} = {{")
        lines.append(f"{prefix}{T}{T}limit = {{ prev = {{ var:tv_wonder_level ?= {{ this >= {level} }} }} }}")
        lines.append(
            f"{prefix}{T}{T}change_building_level_in_location = {{ "
            f"building = {building_type_ref(building)} value = {level - 1} owner = prev }}"
        )
        lines.append(f"{prefix}{T}}}")
    lines.append(f"{prefix}}}")
    for current_level in range(5, 0, -1):
        lines.append(f"{prefix}else_if = {{")
        lines.append(f"{prefix}{T}limit = {{ {loc_level(building, '>=', current_level)} }}")
        first_target = True
        for target_level in range(6, current_level, -1):
            delta = target_level - current_level
            head = "if" if first_target else "else_if"
            first_target = False
            lines.append(f"{prefix}{T}{head} = {{")
            lines.append(f"{prefix}{T}{T}limit = {{ prev = {{ var:tv_wonder_level ?= {{ this >= {target_level} }} }} }}")
            lines.append(
                f"{prefix}{T}{T}change_building_level_in_location = {{ "
                f"building = {building_type_ref(building)} value = {delta} owner = prev }}"
            )
            lines.append(f"{prefix}{T}}}")
        lines.append(f"{prefix}}}")
    append_store_final_building_level(lines, building, "prev.var:tv_wonder_level", indent)


def append_trigger_event_dispatch_effect(lines: list[str], wonders: list[dict]) -> None:
    lines.append("tv_wonder_mechanics_trigger_finalization_event_effect = {")
    first = True
    for wonder in wonders:
        head = "if" if first else "else_if"
        first = False
        lines.append(f"{T}{head} = {{")
        lines.append(f"{T}{T}limit = {{ var:tv_wonder_locked ?= {wonder['id']} }}")
        lines.append(f"{T}{T}{monthly_country_pulse_event(f'tv_engineering_department.{finalization_event_id(wonder)}')}")
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_construct_final_building_effect(lines: list[str], wonder: dict) -> None:
    building = wonder["final_building"]
    lines.append(f"{construct_final_building_effect_name(wonder)} = {{")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_finalization_preview_ready")
    lines.append(f"{T}{T}{T}var:tv_wonder_locked ?= {wonder['id']}")
    lines.append(f"{T}{T}{T}tv_wonder_construction_site_selected_trigger = yes")
    lines.append(f"{T}{T}{T}var:tv_wonder_level ?= {{ this >= 1 }}")
    lines.append(f"{T}{T}{T}var:tv_wonder_level ?= {{ this <= 6 }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}save_scope_as = tv_wonder_finalization_owner")
    lines.append(f"{T}{T}var:tv_wonder_site ?= {{")
    append_static_final_building_construction(lines, building, 3)
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_destroy_intermediate_buildings_effect(lines: list[str], wonder: dict) -> None:
    # Part module buildings represent unmerged surplus units by finalization time.
    # Only the merged helper is consumed by the final building.
    buildings = [f"tv_wonder_{wonder['key']}"]
    lines.append(f"{destroy_intermediate_effect_name(wonder)} = {{")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ tv_wonder_construction_site_selected_trigger = yes }}")
    lines.append(f"{T}{T}save_scope_as = tv_wonder_module_owner")
    lines.append(f"{T}{T}var:tv_wonder_site ?= {{")
    for building in buildings:
        lines.append(f"{T}{T}{T}if = {{")
        lines.append(f"{T}{T}{T}{T}limit = {{ has_building = {building_type_ref(building)} }}")
        lines.extend(change_level_lines(building, -6, 4))
        lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_broadcast_effect(lines: list[str], wonder: dict) -> None:
    lines.append(f"{broadcast_effect_name(wonder)} = {{")
    lines.append(f"{T}save_scope_as = tv_wonder_builder_country")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ tv_wonder_construction_site_selected_trigger = yes }}")
    lines.append(f"{T}{T}var:tv_wonder_site ?= {{ save_scope_as = tv_wonder_completed_site }}")
    lines.append(f"{T}}}")
    lines.append(f"{T}every_country = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}exists = capital")
    lines.append(f"{T}{T}{T}exists = scope:tv_wonder_builder_country")
    lines.append(f"{T}{T}{T}exists = scope:tv_wonder_completed_site")
    lines.append(f"{T}{T}{T}NOT = {{ this = scope:tv_wonder_builder_country }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}if = {{ limit = {{ scope:tv_wonder_builder_country = {{ var:tv_wonder_project_mode ?= 2 }} }}")
    lines.append(f"{T}{T}{T}trigger_event_non_silently = {{ id = tv_engineering_department.{finalization_world_expansion_event_id(wonder)} }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}else = {{")
    lines.append(f"{T}{T}{T}trigger_event_non_silently = {{ id = tv_engineering_department.{finalization_world_event_id(wonder)} }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_base_instant_effects(lines: list[str], wonder: dict, mechanics: dict) -> None:
    """Use persistent project levels and literal payouts in native option previews.

    Mode 1 is new construction; mode 2 pays only the expansion delta. No hooks
    are installed in load, ownership, external level changes or rededication.
    """
    from wonder_mechanics.modifiers import wonder_base_instant_effects
    from in_game.common.scripted_effects.gen_tv_engineering_department_wonder_mechanics_effects import reward_effect_lines

    if not wonder_base_instant_effects(wonder, mechanics):
        return
    for base_level in range(6):
        mode = 1 if base_level == 0 else 2
        lines.append(f"{T}{T}if = {{")
        conditions = f"var:tv_wonder_project_mode ?= {mode}"
        if base_level:
            conditions += f" var:tv_wonder_project_base_level ?= {base_level}"
        lines.append(f"{T}{T}{T}limit = {{ {conditions} tv_wonder_construction_site_selected_trigger = yes }}")
        for level in range(base_level + 1, 7):
            head = "if" if level == base_level + 1 else "else_if"
            lines.append(f"{T}{T}{T}{head} = {{")
            lines.append(f"{T}{T}{T}{T}limit = {{ var:tv_wonder_level ?= {level} }}")
            rewards = wonder_base_instant_effects(wonder, mechanics, level - base_level)
            # The shared ritual renderer rounds floats to three decimals. Base
            # effects preserve the engine's five-decimal precision as literals.
            rewards = [{**entry, "value": f"{entry['value']:.5f}".rstrip("0").rstrip(".")} for entry in rewards]
            lines.extend(reward_effect_lines(rewards, 4))
            lines.append(f"{T}{T}{T}}}")
        lines.append(f"{T}{T}}}")


def append_visible_effect(lines: list[str], wonder: dict, mechanics: dict) -> None:
    lines.append(f"{finalization_visible_effect_name(wonder)} = {{")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ has_variable = tv_wonder_finalization_preview_ready var:tv_wonder_locked ?= {wonder['id']} }}")
    lines.append(f"{T}{T}tv_wonder_apply_finalization_visible_rewards_effect = yes")
    append_base_instant_effects(lines, wonder, mechanics)
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_hidden_effect(lines: list[str], wonder: dict, mechanics: dict) -> None:
    lines.extend([f"{finalization_hidden_effect_name(wonder)} = {{",
        f"\tif = {{ limit = {{ has_variable = tv_wonder_finalization_preview_ready var:tv_wonder_locked ?= {wonder['id']} }}",
        "\ttv_wonder_complete_finalization_cleanup_effect = yes"])
    # This runs in the hidden finalization event, after the visible grant.
    # Retain other instances' country benefits while removing this site's old style.
    lines.extend([
        "\tif = { limit = { var:tv_wonder_project_mode ?= 2 }",
        "\t\tif = { limit = { var:tv_wonder_finalization_outcome ?= 0 }",
        "\t\t\tsave_scope_as = tv_wonder_ritual_sync_country",
        f"\t\t\tvar:tv_wonder_site ?= {{ tv_wonder_{wonder['key']}_ritual_revoke_effect = yes }}",
        "\t\t}",
        "\t\telse = {",
    ])
    for ritual in ritual_styles(wonder, mechanics):
        if ritual['location_modifier']:
            lines.append(
                f"\t\t\tif = {{ limit = {{ NOT = {{ var:tv_wonder_finalization_outcome ?= {ritual['style']} }} }} "
                f"var:tv_wonder_site ?= {{ remove_location_modifier = {ritual['location_modifier']} }} }}"
            )
    lines.extend([
        f"\t\t\ttv_wonder_{wonder['key']}_ritual_sync_country_effect = yes",
        "\t\t}",
        "\t}",
        f"\t{destroy_intermediate_effect_name(wonder)} = yes",
        f"\tif = {{ limit = {{ OR = {{ var:tv_wonder_project_mode ?= 1 var:tv_wonder_project_mode ?= 2 }} }} {broadcast_effect_name(wonder)} = yes }}",
        "\ttv_wonder_register_current_project_priority_candidate_from_variables_effect = yes",
        "\tvar:tv_wonder_site ?= { tv_wonder_mechanics_refresh_location_display_state_effect = yes }",
        # Finalization only creates/raises this known instance. Supplement both
        # maxima without rebuilding the country's complete owned-location table.
        max_level_cache(wonder, 'tv_wonder_auto_level_by_wonder_id', 'var:tv_wonder_level'),
        "\tif = { limit = { var:tv_wonder_finalization_outcome ?= 0 }",
        plain_cache(wonder, 'var:tv_wonder_level'), "\t}",
        "\ttv_wonder_clear_project_state_core_effect = yes", "\ttv_wonder_start_concept_effect = { reason = 3 }", "\t}", "}", ""])


def generate() -> str:
    wonders, mechanics = load_all_wonder_mechanics()
    lines = render_header(SCRIPT_REL, DATA_REL)
    append_hidden_event_trigger_effect(lines)
    append_hidden_event_execute_effect(lines, wonders)
    append_final_building_completion_sync_hidden_event_effects(lines, wonders)
    append_trigger_event_dispatch_effect(lines, wonders)
    for wonder in wonders:
        append_construct_final_building_effect(lines, wonder)
        append_destroy_intermediate_buildings_effect(lines, wonder)
        append_broadcast_effect(lines, wonder)
        append_visible_effect(lines, wonder, mechanics)
        append_hidden_effect(lines, wonder, mechanics)
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUT_FILE.write_text("\ufeff" + generate(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
