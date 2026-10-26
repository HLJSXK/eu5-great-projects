import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.naming import UNIQUE_WONDER_MIN_ID
from wonder_mechanics.naming import ALL_WONDER_MIN_ID, FINAL_BUILDING_LEVEL_BY_TYPE_MAP, final_building_level_changed_effect_name, mechanic_key, wonder_static_display_modifier_name, wonder_static_local_display_modifier_name, wonder_suitability_row_composite_id
from wonder_mechanics.render import (
    indent_script_block,
    monthly_country_pulse_event,
    render_header,
    variable_map_key_trigger,
)
from wonder_mechanics.rituals import ONE_SHOT_REWARD_EFFECTS, ritual_style_ids, ritual_style
from wonder_mechanics.schema import (
    site_preference_lines_for_wonder,
    SUITABILITY_ACTUAL_MAP,
    SUITABILITY_REVEAL_MAP,
    suitability_current_actual_variable,
    suitability_current_revealed_variable,
    suitability_knowledge_for_wonder,
)

OUT_FILE = REPO_ROOT / "src" / "in_game" / "common" / "scripted_effects" / "tv_engineering_department_wonder_mechanics_effects.txt"
SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_engineering_department_wonder_mechanics_effects.py"
PROPOSAL_SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_proposal_effects.py"
SURVEY_SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_survey_effects.py"
RITUAL_SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_ritual_effects.py"
LOCATION_DISPLAY_SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_location_display_effects.py"
DATA_REL = (
    "data/wonders.yaml + data/wonder_final_buildings.yaml + data/wonder_generic_rituals.yaml + "
    "data/wonder_base_modifiers.yaml + data/wonder_site_rules.yaml + data/unique_wonders.yaml"
)
PULSE_DATA_REL = f"{DATA_REL} + data/pulse_registry.yaml"
T = "\t"
DISPLAY_SLOT_MAX = 3
TOOLTIP_SLOT_MAX = 5
FEASIBLE_GENERIC_DECK_MAP = "tv_wonder_feasible_generic_deck"
FEASIBLE_UNIQUE_DECK_MAP = "tv_wonder_feasible_unique_deck"
LOCATION_SURVEYED_MAP = "tv_wonder_surveyed"
LOCATION_SURVEY_SCALE_MAP = "tv_wonder_survey_scale_competence"
LOCATION_SURVEY_LOGISTICS_MAP = "tv_wonder_survey_logistics_competence"
LOCATION_SURVEY_ORGANIZATION_MAP = "tv_wonder_survey_organization_competence"
LOCATION_SURVEY_SCALE_TIER_MAP = "tv_wonder_survey_scale_tier"
LOCATION_SURVEY_ACTUAL_MAP = "tv_wonder_survey_suitability_actual"
SUITABILITY_ROW_COUNT_MAP = "tv_wonder_mechanic_id_to_suitability_row_count"
SURVEY_WONDER_KEY_VAR = "tv_wonder_survey_wonder_key"
SURVEY_MECHANIC_KEY_VAR = "tv_wonder_survey_mechanic_key"
SURVEY_ROW_KEY_VAR = "tv_wonder_survey_row_key"
SURVEY_LOCATION_COPY_TEMP_VAR = "tv_wonder_survey_location_cache_temp"
SUITABILITY_ACTUAL_TEMP_VAR = "tv_wonder_suitability_row_temp"
SUITABILITY_MECHANIC_KEY_LOCAL = "tv_wonder_suitability_mechanic_key"
SUITABILITY_ROW_KEY_LOCAL = "tv_wonder_suitability_row_key"
SUITABILITY_ROW_COUNT_LOCAL = "tv_wonder_suitability_row_count"
SUITABILITY_REVEAL_VALUE_LOCAL = "tv_wonder_suitability_reveal_value"
FINAL_BUILDING_WONDER_ID_MAP = "tv_wonder_final_building_type_to_wonder_id"
UNIQUE_WONDER_LOCATION_MAP = "tv_wonder_unique_id_to_location"
UNIQUE_WONDER_FINAL_BUILDING_TYPE_MAP = "tv_wonder_unique_id_to_final_building_type"
AUTO_CACHE_COUNTRY_SCOPE = "tv_wonder_auto_cache_country"
AUTO_CACHE_LOCATION_SCOPE = "tv_wonder_auto_cache_location"
AUTO_CACHE_BUILDING_TYPE_LOCAL = "tv_wonder_auto_cache_final_building_type"
AUTO_CACHE_WONDER_ID_LOCAL = "tv_wonder_auto_cache_wonder_id"
AUTO_CACHE_LEVEL_LOCAL = "tv_wonder_auto_cache_level"
AUTO_CACHE_EXISTING_LEVEL_LOCAL = "tv_wonder_auto_cache_existing_level"
EXISTING_UNIQUE_WONDERS_INITIALIZED_GLOBAL = "tv_wonder_existing_unique_wonders_initialized"
EXISTING_UNIQUE_WONDERS_SEED_EFFECT = "tv_wonder_seed_existing_unique_wonders_effect"
PRIORITY_CANDIDATE_WONDER_ID_VAR = "tv_wonder_priority_candidate_wonder_id"
PRIORITY_CANDIDATE_CURRENT_MODE_VAR = "tv_wonder_priority_candidate_current_mode"
OWNERSHIP_EVENT_WONDER_ID_VAR = "tv_wonder_ownership_event_wonder_id"
OWNERSHIP_LOSS_RETAINS_SAME_WONDER_VAR = "tv_wonder_ownership_loss_retains_same_wonder"
LOCATION_DISPLAY_SCOPE = "tv_wonder_location_display_location"
LOCATION_DISPLAY_WONDER_ID_LOCAL = "tv_wonder_location_display_wonder_id"
LOCATION_DISPLAY_BUILDING_TYPE_LOCAL = "tv_wonder_location_display_building_type"
LOCATION_DISPLAY_ID_VAR = "tv_wonder_location_display_id"
LOCATION_DISPLAY_LEVEL_VAR = "tv_wonder_location_display_level"
LOCATION_DISPLAY_RITUAL_STYLE_VAR = "tv_wonder_location_display_ritual_style"
LOCATION_DISPLAY_RITUAL_COMPLETED_VAR = "tv_wonder_location_display_ritual_completed"
WONDER_MAP_UNIQUE_LEVEL_VAR = "tv_wonder_map_unique_level"
WONDER_MAP_GENERIC_LEVEL_VAR = "tv_wonder_map_generic_level"
WONDER_MAP_HAS_POTENTIAL_UNIQUE_VAR = "tv_wonder_map_has_potential_unique"
RITUAL_SHARED_RUNTIME_VARS = [
    "tv_wonder_ritual_auxiliary_building_finished",
    "tv_wonder_ritual_months_completed",
    "tv_wonder_ritual_progress_pct",
]
SUITABILITY_CONDITION_SCRIPTS = {
    "topography_mountains": "topography = mountains",
    "topography_plateau": "topography = plateau",
    "topography_hills": "topography = hills",
    "vegetation_forest": "vegetation = forest",
    "vegetation_woods": "vegetation = woods",
    "vegetation_forest_or_woods": "OR = {\n\tvegetation = forest\n\tvegetation = woods\n}",
    "rank_rural": "location_rank ?= location_rank:rural_settlement",
    "rank_city": "location_rank ?= location_rank:city",
    "rank_megalopolis": "location_rank ?= location_rank:megalopolis",
    "neighbor_city": "any_neighbor_location = { tv_wonder_location_is_city_trigger = yes }",
    "neighbor_town": (
        "NOT = { any_neighbor_location = { tv_wonder_location_is_city_trigger = yes } }\n"
        "any_neighbor_location = { tv_wonder_location_is_town_trigger = yes }"
    ),
    "has_monastery": "has_building = building_type:monastery",
    "has_cathedral": "has_building = building_type:cathedral",
    "dominant_religion_owner": "dominant_religion = owner.religion",
    "has_bridge_infrastructure": "has_building = building_type:bridge_infrastructure",
    "neighbor_bridge_opening": "any_neighbor_location = { has_building = building_type:tv_wonder_bridge_opening }",
    "waterway_or_port": "OR = {\n\thas_river = yes\n\tis_adjacent_to_lake = yes\n\tis_port = yes\n}",
    "is_port": "is_port = yes",
    "fort_level": "modifier:fort_level > 0",
    "urban_rank": "OR = {\n\tlocation_rank ?= location_rank:city\n\tlocation_rank ?= location_rank:megalopolis\n}",
    "is_capital": "is_capital = yes",
    "raw_coin_metal": "OR = {\n\traw_material = goods:goods_gold\n\traw_material = goods:silver\n\traw_material = goods:copper\n}",
    "has_armory": "has_building = building_type:armory",
}
SUITABILITY_SOURCE_EXPRESSIONS = {
    "development": "development",
    "total_building_levels": "total_building_levels",
    "harbor_suitability": "modifier:harbor_suitability",
    "free_building_levels": "modifier:free_building_levels",
    "average_location_literacy": "average_location_literacy",
}


def add_site_preference(wonder: dict, mechanics: dict, indent: int = 2) -> list[str]:
    prefix = T * indent
    lines = site_preference_lines_for_wonder(mechanics, wonder, indent)
    if wonder.get("is_unique"):
        lines.append(f"{prefix}tv_wonder_change_scale_competence_target_effect = {{ value = 100 }}")
        lines.append(f"{prefix}tv_wonder_change_logistics_competence_target_effect = {{ value = 20 }}")
        lines.append(f"{prefix}tv_wonder_change_organization_competence_target_effect = {{ value = 20 }}")
    return lines


def fmt_value(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return str(value)


def all_wonders_by_key(wonders: list[dict]) -> dict[str, dict]:
    return {str(wonder["key"]): wonder for wonder in wonders}


def mechanic_id_for_wonder(wonder: dict, by_key: dict[str, dict]) -> int:
    return int(by_key[mechanic_key(wonder)]["id"])


def suitability_row_key_for_wonder(wonder: dict, row_index: int, by_key: dict[str, dict]) -> int:
    return wonder_suitability_row_composite_id(mechanic_id_for_wonder(wonder, by_key), row_index)


def map_key_exists_condition(map_name: str, key: object, indent: int) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}has_variable_map = {map_name}",
        f"{prefix}is_key_in_variable_map = {{ name = {map_name} target = {key} }}",
    ]


def map_replace_lines(map_name: str, key: object, value: str, indent: int) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}remove_from_variable_map = {{ name = {map_name} key = {key} }}",
        f"{prefix}add_to_variable_map = {{ name = {map_name} key = {key} value = {value} }}",
    ]


def loc_level(building_ref: str, op: str, level: int) -> str:
    return f"location_building_level = {{ building_type = {building_ref} value {op} {level} }}"


def append_register_existing_unique_priority_candidate(
    lines: list[str],
    wonder_id: int,
    indent: int,
) -> None:
    prefix = T * indent
    lines.append(f"{prefix}if = {{")
    lines.append(f"{prefix}{T}limit = {{ has_owner = yes }}")
    lines.append(f"{prefix}{T}save_scope_as = tv_wonder_priority_site")
    lines.append(f"{prefix}{T}owner ?= {{")
    lines.append(f"{prefix}{T}{T}save_scope_as = tv_wonder_priority_owner")
    lines.append(
        f"{prefix}{T}{T}set_variable = {{ name = {PRIORITY_CANDIDATE_WONDER_ID_VAR} value = {wonder_id} }}"
    )
    lines.append(
        f"{prefix}{T}{T}set_variable = {{ name = {PRIORITY_CANDIDATE_CURRENT_MODE_VAR} value = 2 }}"
    )
    lines.append(f"{prefix}{T}}}")
    lines.append(f"{prefix}{T}if = {{")
    lines.append(f"{prefix}{T}{T}limit = {{ exists = scope:tv_wonder_priority_owner }}")
    lines.append(f"{prefix}{T}{T}scope:tv_wonder_priority_owner = {{")
    lines.append(f"{prefix}{T}{T}{T}tv_wonder_unregister_current_site_priority_candidate_effect = yes")
    lines.append(f"{prefix}{T}{T}{T}tv_wonder_register_current_priority_candidate_effect = yes")
    lines.append(f"{prefix}{T}{T}{T}remove_variable = {PRIORITY_CANDIDATE_WONDER_ID_VAR}")
    lines.append(f"{prefix}{T}{T}{T}remove_variable = {PRIORITY_CANDIDATE_CURRENT_MODE_VAR}")
    lines.append(f"{prefix}{T}{T}}}")
    lines.append(f"{prefix}{T}}}")
    lines.append(f"{prefix}}}")


def set_survey_row_key_var_lines(row_index: int, indent: int) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}set_variable = {{ name = {SURVEY_ROW_KEY_VAR} value = var:{SURVEY_MECHANIC_KEY_VAR} }}",
        f"{prefix}change_variable = {{ name = {SURVEY_ROW_KEY_VAR} multiply = 10 }}",
        f"{prefix}change_variable = {{ name = {SURVEY_ROW_KEY_VAR} add = {row_index} }}",
    ]


def clear_current_suitability_actual_cache_lines(max_rows: int, indent: int) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}remove_variable = {suitability_current_actual_variable(row_index)}"
        for row_index in range(1, max_rows + 1)
    ]


def clear_current_suitability_display_cache_lines(max_rows: int, indent: int) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}remove_variable = {suitability_current_revealed_variable()}",
        *clear_current_suitability_actual_cache_lines(max_rows, indent),
    ]


def artist_skill_reward_effect_lines(effect: str, value: str, indent: int) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}random_artist = {{ limit = {{ is_alive = yes }} save_scope_as = tv_wonder_ritual_reward_artist }}",
        f"{prefix}if = {{",
        f"{prefix}{T}limit = {{ exists = scope:tv_wonder_ritual_reward_artist }}",
        f"{prefix}{T}scope:tv_wonder_ritual_reward_artist = {{ {effect} = {value} }}",
        f"{prefix}}}",
    ]


def location_laborer_reward_effect_lines(value: str, indent: int) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}if = {{",
        f"{prefix}{T}limit = {{ has_owner = yes }}",
        f"{prefix}{T}add_pop = {{",
        f"{prefix}{T}{T}culture = owner.culture",
        f"{prefix}{T}{T}religion = owner.religion",
        f"{prefix}{T}{T}type = pop_type:laborers",
        f"{prefix}{T}{T}size = {value}",
        f"{prefix}{T}}}",
        f"{prefix}}}",
    ]


def country_reward_effect_lines(reward: list[dict], indent: int = 1) -> list[str]:
    prefix = T * indent
    lines: list[str] = []
    for entry in reward:
        effect_type = entry["type"]
        if effect_type in ONE_SHOT_REWARD_EFFECTS:
            spec = ONE_SHOT_REWARD_EFFECTS[effect_type]
            effect = spec["effect"]
            scope = spec["scope"]
            value = fmt_value(entry["value"])
            if scope in {"country_scalar", "country_raw"}:
                lines.append(f"{prefix}{effect} = {value}")
            elif scope == "country_value_block":
                lines.append(f"{prefix}{effect} = {{ value = {value} }}")
            elif scope == "country_scale_block":
                lines.append(f"{prefix}{effect} = {{ scale = {value} }}")
            elif scope == "ruler_scalar":
                lines.append(f"{prefix}ruler ?= {{ {effect} = {value} }}")
            elif scope == "culture_scalar":
                lines.append(f"{prefix}culture = {{ {effect} = {value} }}")
            elif scope == "estate_satisfaction":
                estate = str(spec["estate"])
                lines.append(f"{prefix}if = {{")
                lines.append(f"{prefix}{T}limit = {{ country_has_estate = {estate} }}")
                lines.append(f"{prefix}{T}{effect} = {{ type = {estate} value = {value} }}")
                lines.append(f"{prefix}}}")
            elif scope == "artist_scalar":
                lines.extend(artist_skill_reward_effect_lines(effect, value, indent))
            elif scope == "location_scalar":
                raise ValueError(f"Location ritual reward effect type must be handled outside country scope: {effect_type}")
            elif scope == "location_laborers":
                raise ValueError(f"Location ritual reward effect type must be handled outside country scope: {effect_type}")
            else:
                raise ValueError(f"Unsupported ritual reward scope for {effect_type}: {scope}")
        elif effect_type == "estate_satisfaction":
            estate = entry["estate"]
            lines.append(f"{prefix}if = {{")
            lines.append(f"{prefix}{T}limit = {{ country_has_estate = estate_type:{estate} }}")
            lines.append(f"{prefix}{T}add_estate_satisfaction = {{ type = estate_type:{estate} value = {fmt_value(entry['value'])} }}")
            lines.append(f"{prefix}}}")
        else:
            raise ValueError(f"Unsupported ritual reward effect type: {effect_type}")
    return lines


def reward_effect_lines(reward: list[dict], indent: int = 1) -> list[str]:
    prefix = T * indent
    lines: list[str] = []
    for entry in reward:
        reward_type = entry["type"]
        spec = ONE_SHOT_REWARD_EFFECTS.get(reward_type, {})
        if spec.get("scope") == "location_scalar":
            lines.append(f"{prefix}var:tv_wonder_site ?= {{ {spec['effect']} = {fmt_value(entry['value'])} }}")
        elif spec.get("scope") == "location_laborers":
            lines.append(f"{prefix}var:tv_wonder_site ?= {{")
            lines.extend(location_laborer_reward_effect_lines(fmt_value(entry["value"]), indent + 1))
            lines.append(f"{prefix}}}")
        else:
            lines.extend(country_reward_effect_lines([entry], indent))
    return lines


def location_tooltip_reward_effect_lines(reward: list[dict], indent: int = 1) -> list[str]:
    prefix = T * indent
    lines: list[str] = []
    for entry in reward:
        reward_type = entry["type"]
        spec = ONE_SHOT_REWARD_EFFECTS.get(reward_type, {})
        if spec.get("scope") == "location_scalar":
            lines.append(f"{prefix}{spec['effect']} = {fmt_value(entry['value'])}")
        elif spec.get("scope") == "location_laborers":
            lines.extend(location_laborer_reward_effect_lines(fmt_value(entry["value"]), indent))
        else:
            lines.append(f"{prefix}owner ?= {{")
            lines.extend(country_reward_effect_lines([entry], indent + 1))
            lines.append(f"{prefix}}}")
    return lines


def ritual_entries(wonders: list[dict], mechanics: dict) -> list[tuple[dict, int, dict]]:
    entries: list[tuple[dict, int, dict]] = []
    for wonder in wonders:
        for style in ritual_style_ids(wonder):
            entries.append((wonder, style, ritual_style(wonder, mechanics, style)))
    return entries


def append_display_modifier_reference_effect(lines: list[str], wonders: list[dict]) -> None:
    lines.append("tv_wonder_mechanics_reference_display_modifiers_effect = {")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ always = no }}")
    lines.append(f"{T}{T}# Static references for dynamic ShowModifierEffect display keys.")
    for wonder in wonders:
        for level in range(1, 7):
            lines.append(
                f"{T}{T}add_country_modifier = {{ "
                f"modifier = {wonder_static_display_modifier_name(wonder, level)} "
                "years = -1 mode = add_and_extend }"
            )
    lines.append(f"{T}{T}capital = {{")
    for wonder in wonders:
        for level in range(1, 7):
            lines.append(
                f"{T}{T}{T}add_location_modifier = {{ "
                f"modifier = {wonder_static_local_display_modifier_name(wonder, level)} "
                "years = -1 mode = add_and_extend }"
            )
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def slot_id_var(slot: int) -> str:
    return f"tv_wonder_display_slot_{slot}_id"


def slot_level_var(slot: int) -> str:
    return f"tv_wonder_display_slot_{slot}_level"


def slot_ritual_style_var(slot: int) -> str:
    return f"tv_wonder_display_slot_{slot}_ritual_style"


def slot_ritual_completed_var(slot: int) -> str:
    return f"tv_wonder_display_slot_{slot}_ritual_completed"


def tooltip_slot_id_var(slot: int) -> str:
    return f"tv_wonder_tooltip_slot_{slot}_id"


def tooltip_slot_level_var(slot: int) -> str:
    return f"tv_wonder_tooltip_slot_{slot}_level"


def tooltip_slot_ritual_style_var(slot: int) -> str:
    return f"tv_wonder_tooltip_slot_{slot}_ritual_style"


def tooltip_slot_ritual_completed_var(slot: int) -> str:
    return f"tv_wonder_tooltip_slot_{slot}_ritual_completed"


def append_location_display_slot_push(lines: list[str], *, indent: int, compact: bool) -> None:
    prefix = T * indent
    if compact:
        lines.append(
            f"{prefix}tv_wonder_mechanics_push_location_display_slot_effect = {{ "
            f"wonder_id = var:{LOCATION_DISPLAY_ID_VAR} "
            f"wonder_level = var:{LOCATION_DISPLAY_LEVEL_VAR} "
            f"wonder_ritual_style = var:{LOCATION_DISPLAY_RITUAL_STYLE_VAR} "
            f"wonder_ritual_completed = var:{LOCATION_DISPLAY_RITUAL_COMPLETED_VAR} }}"
        )
    lines.append(
        f"{prefix}tv_wonder_mechanics_push_location_tooltip_slot_effect = {{ "
        f"wonder_id = var:{LOCATION_DISPLAY_ID_VAR} "
        f"wonder_level = var:{LOCATION_DISPLAY_LEVEL_VAR} "
        f"wonder_ritual_style = var:{LOCATION_DISPLAY_RITUAL_STYLE_VAR} "
        f"wonder_ritual_completed = var:{LOCATION_DISPLAY_RITUAL_COMPLETED_VAR} }}"
    )


def append_location_display_push_effects(lines: list[str]) -> None:
    lines.append("tv_wonder_mechanics_push_location_display_slot_effect = {")
    for slot in range(1, DISPLAY_SLOT_MAX + 1):
        head = "if" if slot == 1 else "else_if"
        lines.append(f"{T}{head} = {{")
        lines.append(f"{T}{T}limit = {{ NOT = {{ has_variable = {slot_id_var(slot)} }} }}")
        lines.append(f"{T}{T}set_variable = {{ name = {slot_id_var(slot)} value = $wonder_id$ }}")
        lines.append(f"{T}{T}set_variable = {{ name = {slot_level_var(slot)} value = $wonder_level$ }}")
        lines.append(f"{T}{T}set_variable = {{ name = {slot_ritual_style_var(slot)} value = $wonder_ritual_style$ }}")
        lines.append(
            f"{T}{T}set_variable = {{ name = {slot_ritual_completed_var(slot)} value = $wonder_ritual_completed$ }}"
        )
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_push_location_tooltip_slot_effect = {")
    for slot in range(1, TOOLTIP_SLOT_MAX + 1):
        head = "if" if slot == 1 else "else_if"
        lines.append(f"{T}{head} = {{")
        lines.append(f"{T}{T}limit = {{ NOT = {{ has_variable = {tooltip_slot_id_var(slot)} }} }}")
        lines.append(f"{T}{T}set_variable = {{ name = {tooltip_slot_id_var(slot)} value = $wonder_id$ }}")
        lines.append(f"{T}{T}set_variable = {{ name = {tooltip_slot_level_var(slot)} value = $wonder_level$ }}")
        lines.append(f"{T}{T}set_variable = {{ name = {tooltip_slot_ritual_style_var(slot)} value = $wonder_ritual_style$ }}")
        lines.append(
            f"{T}{T}set_variable = {{ name = {tooltip_slot_ritual_completed_var(slot)} value = $wonder_ritual_completed$ }}"
        )
        lines.append(f"{T}}}")
    lines.append(f"{T}else = {{")
    lines.append(f"{T}{T}if = {{")
    lines.append(f"{T}{T}{T}limit = {{ has_variable = tv_wonder_tooltip_overflow_count }}")
    lines.append(f"{T}{T}{T}change_variable = {{ name = tv_wonder_tooltip_overflow_count add = 1 }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}else = {{")
    lines.append(f"{T}{T}{T}set_variable = {{ name = tv_wonder_tooltip_overflow_count value = 1 }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_location_display_clear_effect(lines: list[str]) -> None:
    lines.append("tv_wonder_mechanics_clear_location_display_state_effect = {")
    lines.append(f"{T}remove_variable = {LOCATION_DISPLAY_ID_VAR}")
    lines.append(f"{T}remove_variable = {LOCATION_DISPLAY_LEVEL_VAR}")
    lines.append(f"{T}remove_variable = {LOCATION_DISPLAY_RITUAL_STYLE_VAR}")
    lines.append(f"{T}remove_variable = {LOCATION_DISPLAY_RITUAL_COMPLETED_VAR}")
    lines.append(f"{T}remove_variable = {WONDER_MAP_UNIQUE_LEVEL_VAR}")
    lines.append(f"{T}remove_variable = {WONDER_MAP_GENERIC_LEVEL_VAR}")
    lines.append(f"{T}remove_variable = {WONDER_MAP_HAS_POTENTIAL_UNIQUE_VAR}")
    lines.append(f"{T}set_variable = {{ name = tv_wonder_tooltip_overflow_count value = 0 }}")
    for slot in range(1, DISPLAY_SLOT_MAX + 1):
        lines.append(f"{T}remove_variable = {slot_id_var(slot)}")
        lines.append(f"{T}remove_variable = {slot_level_var(slot)}")
        lines.append(f"{T}remove_variable = {slot_ritual_style_var(slot)}")
        lines.append(f"{T}remove_variable = {slot_ritual_completed_var(slot)}")
    for slot in range(1, TOOLTIP_SLOT_MAX + 1):
        lines.append(f"{T}remove_variable = {tooltip_slot_id_var(slot)}")
        lines.append(f"{T}remove_variable = {tooltip_slot_level_var(slot)}")
        lines.append(f"{T}remove_variable = {tooltip_slot_ritual_style_var(slot)}")
        lines.append(f"{T}remove_variable = {tooltip_slot_ritual_completed_var(slot)}")
    lines.append("}")
    lines.append("")


def append_location_display_unique_location_projection(lines: list[str], *, compact: bool) -> None:
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}has_global_variable_map = {UNIQUE_WONDER_LOCATION_MAP}")
    lines.append(f"{T}{T}{T}has_global_variable_map = {UNIQUE_WONDER_FINAL_BUILDING_TYPE_MAP}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}every_key_in_global_variable_map = {{")
    lines.append(f"{T}{T}{T}variable = {UNIQUE_WONDER_LOCATION_MAP}")
    lines.append(f"{T}{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}{T}is_key_in_global_variable_map = {{ name = {UNIQUE_WONDER_FINAL_BUILDING_TYPE_MAP} target = this }}")
    lines.append(
        f"{T}{T}{T}{T}\"global_variable_map({UNIQUE_WONDER_LOCATION_MAP}|this)\" = {{ "
        f"this = scope:{LOCATION_DISPLAY_SCOPE} }}"
    )
    lines.append(
        f"{T}{T}{T}{T}\"global_variable_map({UNIQUE_WONDER_FINAL_BUILDING_TYPE_MAP}|this)\" = {{"
    )
    lines.append(f"{T}{T}{T}{T}{T}scope:{LOCATION_DISPLAY_SCOPE} = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}NOT = {{ has_building = prev }}")
    lines.append(f"{T}{T}{T}{T}{T}{T}OR = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}NOT = {{ has_variable_map = {FINAL_BUILDING_LEVEL_BY_TYPE_MAP} }}")
    lines.append(
        f"{T}{T}{T}{T}{T}{T}{T}NOT = {{ "
        f"is_key_in_variable_map = {{ name = {FINAL_BUILDING_LEVEL_BY_TYPE_MAP} target = prev }} }}"
    )
    lines.append(f"{T}{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}scope:{LOCATION_DISPLAY_SCOPE} = {{")
    lines.append(f"{T}{T}{T}{T}set_variable = {{ name = {WONDER_MAP_HAS_POTENTIAL_UNIQUE_VAR} value = 1 }}")
    lines.append(f"{T}{T}{T}{T}set_local_variable = {{ name = {LOCATION_DISPLAY_WONDER_ID_LOCAL} value = prev }}")
    lines.append(f"{T}{T}{T}{T}set_local_variable = {{")
    lines.append(f"{T}{T}{T}{T}{T}name = {LOCATION_DISPLAY_BUILDING_TYPE_LOCAL}")
    lines.append(
        f"{T}{T}{T}{T}{T}value = "
        f"\"global_variable_map({UNIQUE_WONDER_FINAL_BUILDING_TYPE_MAP}|local_var:{LOCATION_DISPLAY_WONDER_ID_LOCAL})\""
    )
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(
        f"{T}{T}{T}{T}set_variable = {{ name = {LOCATION_DISPLAY_ID_VAR} "
        f"value = local_var:{LOCATION_DISPLAY_WONDER_ID_LOCAL} }}"
    )
    lines.append(f"{T}{T}{T}{T}set_variable = {{ name = {LOCATION_DISPLAY_LEVEL_VAR} value = 0 }}")
    lines.append(f"{T}{T}{T}{T}set_variable = {{ name = {LOCATION_DISPLAY_RITUAL_STYLE_VAR} value = 0 }}")
    lines.append(f"{T}{T}{T}{T}set_variable = {{ name = {LOCATION_DISPLAY_RITUAL_COMPLETED_VAR} value = 0 }}")
    lines.append(f'{T}{T}{T}{T}set_local_variable = {{ name = tv_wonder_potential_helper value = "global_variable_map(tv_wonder_id_to_helper_building_type|local_var:{LOCATION_DISPLAY_WONDER_ID_LOCAL})" }}')
    lines.append(f'{T}{T}{T}{T}if = {{ limit = {{ NOT = {{ has_building = local_var:tv_wonder_potential_helper }} }}')
    append_location_display_slot_push(lines, indent=4, compact=compact)
    lines.extend(['}', 'remove_local_variable = tv_wonder_potential_helper'])
    lines.append(f"{T}{T}{T}{T}remove_local_variable = {LOCATION_DISPLAY_BUILDING_TYPE_LOCAL}")
    lines.append(f"{T}{T}{T}{T}remove_local_variable = {LOCATION_DISPLAY_WONDER_ID_LOCAL}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")


def append_wonder_map_level_update(lines: list[str], *, indent: int, source_level_var: str, target_level_var: str) -> None:
    prefix = T * indent
    for level in range(6, 0, -1):
        head = "if" if level == 6 else "else_if"
        lines.extend([
            f"{prefix}{head} = {{",
            f"{prefix}\tlimit = {{ var:{source_level_var} ?= {{ this >= {level} }} NOT = {{ var:{target_level_var} ?= {{ this >= {level} }} }} }}",
            f"{prefix}\tset_variable = {{ name = {target_level_var} value = {level} }}",
            f"{prefix}}}",
        ])


def append_location_display_final_building_projection(lines: list[str], *, compact: bool) -> None:
    lines.extend(["\tif = { limit = { has_variable_map = tv_wonder_final_building_level_by_type }",
        "\t\tevery_key_in_variable_map = { variable = tv_wonder_final_building_level_by_type",
        "\t\t\tset_local_variable = { name = tv_wonder_display_building_key value = this }",
        f"\t\t\tscope:{LOCATION_DISPLAY_SCOPE} = {{",
        'set_variable = { name = tv_wonder_location_display_id value = "global_variable_map(tv_wonder_final_building_type_to_wonder_id|local_var:tv_wonder_display_building_key)" }',
        'set_variable = { name = tv_wonder_location_display_level value = "variable_map(tv_wonder_final_building_level_by_type|local_var:tv_wonder_display_building_key)" }',
        'set_local_variable = { name = tv_wonder_display_id_key value = var:tv_wonder_location_display_id }',
        'set_variable = { name = tv_wonder_location_display_ritual_style value = 0 }',
        'set_variable = { name = tv_wonder_location_display_ritual_completed value = 0 }',
        'if = { limit = { ' + variable_map_key_trigger('tv_wonder_ritual_style_by_id', 'local_var:tv_wonder_display_id_key') + ' }',
        'set_variable = { name = tv_wonder_location_display_ritual_style value = "variable_map(tv_wonder_ritual_style_by_id|local_var:tv_wonder_display_id_key)" }',
        'set_variable = { name = tv_wonder_location_display_ritual_completed value = 1 }', '}',
        'remove_local_variable = tv_wonder_display_id_key'])
    lines.append(f'if = {{ limit = {{ var:{LOCATION_DISPLAY_ID_VAR} ?= {{ this >= {UNIQUE_WONDER_MIN_ID} }} }}')
    append_wonder_map_level_update(lines, indent=4, source_level_var=LOCATION_DISPLAY_LEVEL_VAR, target_level_var=WONDER_MAP_UNIQUE_LEVEL_VAR)
    lines.append('}')
    lines.append('else = {')
    append_wonder_map_level_update(lines, indent=4, source_level_var=LOCATION_DISPLAY_LEVEL_VAR, target_level_var=WONDER_MAP_GENERIC_LEVEL_VAR)
    lines.append('}')
    append_location_display_slot_push(lines, indent=4, compact=compact)
    lines.extend(['}', 'remove_local_variable = tv_wonder_display_building_key', '}', '}'])


def append_location_display_effects(lines: list[str]) -> None:
    append_location_display_push_effects(lines)
    append_location_display_clear_effect(lines)

    lines.append("tv_wonder_mechanics_refresh_location_display_state_effect = {")
    lines.append(f"{T}tv_wonder_mechanics_clear_location_display_state_effect = yes")
    lines.append(f"{T}save_scope_as = {LOCATION_DISPLAY_SCOPE}")
    append_location_display_unique_location_projection(lines, compact=True)
    append_location_display_final_building_projection(lines, compact=True)
    append_location_display_shell_projection(lines)
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_refresh_world_location_display_state_effect = {")
    lines.append(f"{T}every_location_in_the_world = {{")
    lines.append(f"{T}{T}tv_wonder_mechanics_refresh_location_display_state_effect = yes")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_location_display_shell_projection(lines: list[str]) -> None:
    lines.extend(['if = { limit = { has_global_variable_map = tv_wonder_id_to_helper_building_type }',
        'every_key_in_global_variable_map = { variable = tv_wonder_id_to_helper_building_type',
        'set_local_variable = { name = tv_wonder_shell_id value = this }',
        'if = { limit = { local_var:tv_wonder_shell_id > 0 }',
        f'scope:{LOCATION_DISPLAY_SCOPE} = {{',
        'set_local_variable = { name = tv_wonder_shell_building value = "global_variable_map(tv_wonder_id_to_helper_building_type|local_var:tv_wonder_shell_id)" }',
        'set_local_variable = { name = tv_wonder_shell_final value = "global_variable_map(tv_wonder_id_to_final_building_type|local_var:tv_wonder_shell_id)" }',
        'if = { limit = { has_building = local_var:tv_wonder_shell_building NOT = { has_building = local_var:tv_wonder_shell_final } }',
        'set_variable = { name = tv_wonder_location_display_id value = local_var:tv_wonder_shell_id }',
        'set_variable = { name = tv_wonder_location_display_ritual_style value = -1 }',
        'set_variable = { name = tv_wonder_location_display_ritual_completed value = 0 }'])
    for level in range(6, 0, -1):
        head = 'if' if level == 6 else 'else_if'
        lines.append(f'{head} = {{ limit = {{ location_building_level = {{ building_type = local_var:tv_wonder_shell_building value >= {level} }} }} set_variable = {{ name = tv_wonder_location_display_level value = {level} }} }}')
    append_location_display_slot_push(lines, indent=0, compact=True)
    lines.extend(['}', 'remove_local_variable = tv_wonder_shell_building', 'remove_local_variable = tv_wonder_shell_final', '}', '}', 'remove_local_variable = tv_wonder_shell_id', '}', '}'])


def append_final_building_level_map_sync_effects(lines: list[str]) -> None:
    lines.append("tv_wonder_mechanics_sync_location_final_building_level_map_from_buildings_effect = {")
    lines.append(f"{T}clear_variable_map = {FINAL_BUILDING_LEVEL_BY_TYPE_MAP}")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ has_global_variable_map = {FINAL_BUILDING_WONDER_ID_MAP} }}")
    lines.append(f"{T}{T}every_key_in_global_variable_map = {{")
    lines.append(f"{T}{T}{T}variable = {FINAL_BUILDING_WONDER_ID_MAP}")
    lines.append(f"{T}{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}{T}prev = {{ has_building = prev }}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}prev = {{")
    for index, level in enumerate(range(6, 0, -1)):
        head = "if" if index == 0 else "else_if"
        lines.append(f"{T}{T}{T}{T}{head} = {{")
        lines.append(f"{T}{T}{T}{T}{T}limit = {{ {loc_level('prev', '>=', level)} }}")
        lines.extend(map_replace_lines(FINAL_BUILDING_LEVEL_BY_TYPE_MAP, "prev", str(level), 5))
        lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_sync_world_final_building_level_maps_from_buildings_effect = {")
    lines.append(f"{T}every_location_in_the_world = {{")
    lines.append(f"{T}{T}tv_wonder_mechanics_sync_location_final_building_level_map_from_buildings_effect = yes")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_final_building_level_changed_effects(lines: list[str], all_wonders: list[dict], mechanics: dict) -> None:
    for wonder in all_wonders:
        key, wid = wonder["key"], wonder["id"]
        lines.extend([f"{final_building_level_changed_effect_name(wonder)} = {{",
            "\ttv_wonder_mechanics_sync_location_final_building_level_map_from_buildings_effect = yes",
            "\tclear_saved_scope = tv_wonder_ritual_sync_country",
            "\towner ?= { save_scope_as = tv_wonder_ritual_sync_country }",
            f"\tif = {{ limit = {{ NOT = {{ has_building = building_type:{wonder['final_building']} }} }} tv_wonder_{key}_ritual_revoke_effect = yes }}",
            "\tsave_scope_as = tv_wonder_priority_site", "\towner ?= {",
            f"\t\tset_variable = {{ name = tv_wonder_priority_candidate_wonder_id value = {wid} }}",
            "\t\ttv_wonder_unregister_current_site_priority_candidate_effect = yes",
            f"\t\tif = {{ limit = {{ scope:tv_wonder_priority_site = {{ tv_wonder_location_is_valid_priority_final_project_for_{key}_trigger = yes }} }} set_variable = {{ name = tv_wonder_priority_candidate_current_mode value = 2 }} tv_wonder_register_current_priority_candidate_effect = yes }}",
            "\t\tremove_variable = tv_wonder_priority_candidate_wonder_id", "\t\tremove_variable = tv_wonder_priority_candidate_current_mode",
            "\t\ttv_wonder_mechanics_refresh_country_auto_level_map_effect = yes",
            f"\t\tif = {{ limit = {{ var:tv_wonder_project_mode ?= 3 var:tv_wonder_locked ?= {wid} var:tv_wonder_site ?= scope:tv_wonder_priority_site scope:tv_wonder_priority_site = {{ NOT = {{ has_building = building_type:{wonder['final_building']} }} }} }} tv_wonder_ritual_cancel_reritual_effect = yes }}",
            "\t}"])
        if wonder.get("native_canal"):
            lines.append(f"\tif = {{ limit = {{ NOT = {{ has_building = building_type:{wonder['final_building']} }} }} set_canal_open = no }}")
        lines.extend(["\ttv_wonder_mechanics_refresh_location_display_state_effect = yes", "}", ""])


def append_country_auto_level_map_effect(lines: list[str]) -> None:
    lines.extend(['tv_wonder_mechanics_refresh_country_auto_level_map_effect = {',
        'clear_variable_map = tv_wonder_auto_level_by_wonder_id', 'clear_variable_map = tv_wonder_plain_level_by_wonder_id',
        'remove_variable = tv_wonder_has_plain_wonder', 'save_scope_as = tv_wonder_auto_cache_country',
        'every_owned_location = { limit = { has_variable_map = tv_wonder_final_building_level_by_type }',
        'save_scope_as = tv_wonder_auto_cache_location',
        'every_key_in_variable_map = { variable = tv_wonder_final_building_level_by_type',
        'set_local_variable = { name = tv_wonder_auto_cache_building value = this }',
        'scope:tv_wonder_auto_cache_location = {',
        'set_local_variable = { name = tv_wonder_auto_cache_wonder_id value = "global_variable_map(tv_wonder_final_building_type_to_wonder_id|local_var:tv_wonder_auto_cache_building)" }',
        'set_local_variable = { name = tv_wonder_auto_cache_level value = "variable_map(tv_wonder_final_building_level_by_type|local_var:tv_wonder_auto_cache_building)" }',
        'scope:tv_wonder_auto_cache_country = {'])
    for map_name in ('tv_wonder_auto_level_by_wonder_id', 'tv_wonder_plain_level_by_wonder_id'):
        if 'plain' in map_name:
            lines.append('if = { limit = { scope:tv_wonder_auto_cache_location = { NOT = { ' + variable_map_key_trigger('tv_wonder_ritual_style_by_id', 'local_var:tv_wonder_auto_cache_wonder_id') + ' } } } set_variable = { name = tv_wonder_has_plain_wonder value = 1 }')
        lines.extend([f'if = {{ limit = {{ NOT = {{ {variable_map_key_trigger(map_name, "local_var:tv_wonder_auto_cache_wonder_id")} }} }}',
            *map_replace_lines(map_name, 'local_var:tv_wonder_auto_cache_wonder_id', 'local_var:tv_wonder_auto_cache_level', 0), '}',
            'else = {', f'set_local_variable = {{ name = tv_wonder_auto_cache_old value = "variable_map({map_name}|local_var:tv_wonder_auto_cache_wonder_id)" }}',
            'if = { limit = { local_var:tv_wonder_auto_cache_old < local_var:tv_wonder_auto_cache_level }',
            *map_replace_lines(map_name, 'local_var:tv_wonder_auto_cache_wonder_id', 'local_var:tv_wonder_auto_cache_level', 0), '}',
            'remove_local_variable = tv_wonder_auto_cache_old', '}'])
        if 'plain' in map_name: lines.append('}')
    lines.extend(['}', 'remove_local_variable = tv_wonder_auto_cache_wonder_id', 'remove_local_variable = tv_wonder_auto_cache_level', '}',
        'remove_local_variable = tv_wonder_auto_cache_building', '}', '}', '}', ''])


def append_existing_unique_wonders_initialization_effect(lines: list[str], unique_wonders: list[dict]) -> None:
    existing_wonders = [wonder for wonder in unique_wonders if int(wonder["initial_level"]) > 0]
    lines.append("tv_wonder_initialize_existing_unique_wonders_effect = {")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(
        f"{T}{T}{T}NOT = {{ has_global_variable = {EXISTING_UNIQUE_WONDERS_INITIALIZED_GLOBAL} }}"
    )
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}{EXISTING_UNIQUE_WONDERS_SEED_EFFECT} = yes")
    lines.append(f"{T}{T}set_global_variable = {EXISTING_UNIQUE_WONDERS_INITIALIZED_GLOBAL}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append(f"{EXISTING_UNIQUE_WONDERS_SEED_EFFECT} = {{")
    for wonder in existing_wonders:
        initial_level = int(wonder["initial_level"])
        if initial_level > 1:
            raise ValueError(
                f"{wonder['key']} initial_level > 1 needs next-tick construction upgrade handling"
            )
        final_building = wonder["final_building"]
        if not final_building:
            raise ValueError(f"{wonder['key']} must define final_buildings[1] for game-start initialization")
        building_ref = f"building_type:{final_building}"
        lines.append(f"{T}location:{wonder['location']} = {{")
        lines.append(f"{T}{T}if = {{")
        lines.append(f"{T}{T}{T}limit = {{ NOT = {{ has_building = {building_ref} }} }}")
        lines.append(
            f"{T}{T}{T}construct_building = {{ building_type = {building_ref} "
            'cost_multiplier = 0 cost_multiplier_reason = "game_concept_event" instant = yes }'
        )
        lines.append(f"{T}{T}}}")

        lines.append(f"{T}{T}if = {{")
        lines.append(f"{T}{T}{T}limit = {{")
        lines.append(f"{T}{T}{T}{T}OR = {{")
        lines.append(f"{T}{T}{T}{T}{T}NOT = {{ has_variable_map = {FINAL_BUILDING_LEVEL_BY_TYPE_MAP} }}")
        lines.append(
            f"{T}{T}{T}{T}{T}NOT = {{ is_key_in_variable_map = {{ "
            f"name = {FINAL_BUILDING_LEVEL_BY_TYPE_MAP} target = {building_ref} }} }}"
        )
        lines.append(f"{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}}}")
        lines.extend(map_replace_lines(FINAL_BUILDING_LEVEL_BY_TYPE_MAP, building_ref, str(initial_level), 3))
        lines.append(f"{T}{T}}}")

        if initial_level < 6:
            lines.append(f"{T}{T}if = {{")
            lines.append(f"{T}{T}{T}limit = {{")
            lines.append(f"{T}{T}{T}{T}OR = {{")
            lines.append(f"{T}{T}{T}{T}{T}NOT = {{ has_variable_map = {LOCATION_SURVEYED_MAP} }}")
            lines.append(
                f"{T}{T}{T}{T}{T}NOT = {{ is_key_in_variable_map = {{ "
                f"name = {LOCATION_SURVEYED_MAP} target = {wonder['id']} }} }}"
            )
            lines.append(f"{T}{T}{T}{T}}}")
            lines.append(f"{T}{T}{T}}}")
            append_register_existing_unique_priority_candidate(lines, int(wonder["id"]), 3)
            lines.extend(map_replace_lines(LOCATION_SURVEYED_MAP, wonder["id"], "1", 3))
            lines.extend(map_replace_lines(LOCATION_SURVEY_SCALE_MAP, wonder["id"], "100", 3))
            lines.extend(map_replace_lines(LOCATION_SURVEY_LOGISTICS_MAP, wonder["id"], "85", 3))
            lines.extend(map_replace_lines(LOCATION_SURVEY_ORGANIZATION_MAP, wonder["id"], "85", 3))
            lines.extend(map_replace_lines(LOCATION_SURVEY_SCALE_TIER_MAP, wonder["id"], "6", 3))
            lines.append(f"{T}{T}}}")
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_current_suitability_display_cache_effects(
    lines: list[str],
    wonders: list[dict],
    mechanics: dict,
) -> None:
    max_rows = max(len(suitability_knowledge_for_wonder(mechanics, wonder)) for wonder in wonders)
    lines.append("tv_wonder_mechanics_clear_current_suitability_display_cache_effect = {")
    lines.extend(clear_current_suitability_display_cache_lines(max_rows, 1))
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_clear_current_suitability_actual_cache_effect = {")
    lines.extend(clear_current_suitability_actual_cache_lines(max_rows, 1))
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_refresh_current_suitability_display_cache_effect = {")
    lines.append(f"{T}tv_wonder_mechanics_clear_current_suitability_display_cache_effect = yes")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ has_variable = tv_wonder_locked_mechanic_id }}")
    lines.append(f"{T}{T}set_variable = {{ name = {suitability_current_revealed_variable()} value = 0 }}")
    lines.append(f"{T}{T}set_local_variable = {{ name = {SUITABILITY_MECHANIC_KEY_LOCAL} value = var:tv_wonder_locked_mechanic_id }}")
    lines.append(f"{T}{T}if = {{")
    lines.append(f"{T}{T}{T}limit = {{")
    lines.extend(map_key_exists_condition(SUITABILITY_REVEAL_MAP, f"local_var:{SUITABILITY_MECHANIC_KEY_LOCAL}", 4))
    lines.append(f"{T}{T}{T}}}")
    lines.append(
        f"{T}{T}{T}set_variable = {{ name = {suitability_current_revealed_variable()} "
        f"value = \"variable_map({SUITABILITY_REVEAL_MAP}|local_var:{SUITABILITY_MECHANIC_KEY_LOCAL})\" }}"
    )
    lines.append(f"{T}{T}}}")
    for row_index in range(1, max_rows + 1):
        current_actual = suitability_current_actual_variable(row_index)
        lines.append(f"{T}{T}set_local_variable = {{ name = {SUITABILITY_ROW_KEY_LOCAL} value = var:tv_wonder_locked_mechanic_id }}")
        lines.append(f"{T}{T}change_local_variable = {{ name = {SUITABILITY_ROW_KEY_LOCAL} multiply = 10 }}")
        lines.append(f"{T}{T}change_local_variable = {{ name = {SUITABILITY_ROW_KEY_LOCAL} add = {row_index} }}")
        lines.append(f"{T}{T}if = {{")
        lines.append(f"{T}{T}{T}limit = {{")
        lines.extend(map_key_exists_condition(SUITABILITY_ACTUAL_MAP, f"local_var:{SUITABILITY_ROW_KEY_LOCAL}", 4))
        lines.append(f"{T}{T}{T}}}")
        lines.append(
            f"{T}{T}{T}set_variable = {{ name = {current_actual} "
            f"value = \"variable_map({SUITABILITY_ACTUAL_MAP}|local_var:{SUITABILITY_ROW_KEY_LOCAL})\" }}"
        )
        lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}remove_local_variable = {SUITABILITY_ROW_KEY_LOCAL}")
    lines.append(f"{T}{T}remove_local_variable = {SUITABILITY_MECHANIC_KEY_LOCAL}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_suitability_reveal_effect(lines: list[str]) -> None:
    lines.append("tv_wonder_mechanics_reveal_suitability_knowledge_effect = {")
    lines.append(f"{T}tv_wonder_index_refresh_country_cache_effect = yes")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_locked_mechanic_id")
    lines.append(f"{T}{T}{T}has_global_variable_map = {SUITABILITY_ROW_COUNT_MAP}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}set_local_variable = {{ name = {SUITABILITY_MECHANIC_KEY_LOCAL} value = var:tv_wonder_locked_mechanic_id }}")
    lines.append(f"{T}{T}if = {{")
    lines.append(f"{T}{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}{T}is_key_in_global_variable_map = {{ name = {SUITABILITY_ROW_COUNT_MAP} target = local_var:{SUITABILITY_MECHANIC_KEY_LOCAL} }}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(
        f"{T}{T}{T}set_local_variable = {{ name = {SUITABILITY_ROW_COUNT_LOCAL} "
        f"value = \"global_variable_map({SUITABILITY_ROW_COUNT_MAP}|local_var:{SUITABILITY_MECHANIC_KEY_LOCAL})\" }}"
    )
    lines.append(f"{T}{T}{T}if = {{")
    lines.append(f"{T}{T}{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}{T}{T}OR = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}NOT = {{ has_variable_map = {SUITABILITY_REVEAL_MAP} }}")
    lines.append(f"{T}{T}{T}{T}{T}{T}AND = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}has_variable_map = {SUITABILITY_REVEAL_MAP}")
    lines.append(
        f"{T}{T}{T}{T}{T}{T}{T}NOT = {{ is_key_in_variable_map = {{ "
        f"name = {SUITABILITY_REVEAL_MAP} target = local_var:{SUITABILITY_MECHANIC_KEY_LOCAL} }} }}"
    )
    lines.append(f"{T}{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}}}")
    lines.extend(map_replace_lines(SUITABILITY_REVEAL_MAP, f"local_var:{SUITABILITY_MECHANIC_KEY_LOCAL}", "0", 4))
    lines.append(f"{T}{T}{T}}}")
    lines.append(
        f"{T}{T}{T}set_local_variable = {{ name = {SUITABILITY_REVEAL_VALUE_LOCAL} "
        f"value = \"variable_map({SUITABILITY_REVEAL_MAP}|local_var:{SUITABILITY_MECHANIC_KEY_LOCAL})\" }}"
    )
    lines.append(f"{T}{T}{T}if = {{")
    lines.append(f"{T}{T}{T}{T}limit = {{ local_var:{SUITABILITY_REVEAL_VALUE_LOCAL} < local_var:{SUITABILITY_ROW_COUNT_LOCAL} }}")
    lines.append(f"{T}{T}{T}{T}change_local_variable = {{ name = {SUITABILITY_REVEAL_VALUE_LOCAL} add = 1 }}")
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}if = {{")
    lines.append(f"{T}{T}{T}{T}limit = {{ local_var:{SUITABILITY_REVEAL_VALUE_LOCAL} > local_var:{SUITABILITY_ROW_COUNT_LOCAL} }}")
    lines.append(f"{T}{T}{T}{T}set_local_variable = {{ name = {SUITABILITY_REVEAL_VALUE_LOCAL} value = local_var:{SUITABILITY_ROW_COUNT_LOCAL} }}")
    lines.append(f"{T}{T}{T}}}")
    lines.extend(
        map_replace_lines(
            SUITABILITY_REVEAL_MAP,
            f"local_var:{SUITABILITY_MECHANIC_KEY_LOCAL}",
            f"local_var:{SUITABILITY_REVEAL_VALUE_LOCAL}",
            3,
        )
    )
    lines.append(f"{T}{T}{T}tv_wonder_mechanics_refresh_current_suitability_display_cache_effect = yes")
    lines.append(f"{T}{T}{T}remove_local_variable = {SUITABILITY_REVEAL_VALUE_LOCAL}")
    lines.append(f"{T}{T}{T}remove_local_variable = {SUITABILITY_ROW_COUNT_LOCAL}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}remove_local_variable = {SUITABILITY_MECHANIC_KEY_LOCAL}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_suitability_condition_limit(lines: list[str], condition: str, indent: int) -> None:
    if condition not in SUITABILITY_CONDITION_SCRIPTS:
        raise ValueError(f"Missing suitability actual condition script for {condition}")
    prefix = T * indent
    lines.append(f"{prefix}var:tv_wonder_survey_site ?= {{")
    lines.extend(indent_script_block(SUITABILITY_CONDITION_SCRIPTS[condition], indent + 1))
    lines.append(f"{prefix}}}")


def append_suitability_actual_row(
    lines: list[str],
    wonder: dict,
    row: dict[str, str],
    row_index: int,
    by_key: dict[str, dict],
    indent: int,
) -> None:
    prefix = T * indent
    row_key = suitability_row_key_for_wonder(wonder, row_index, by_key)
    lines.extend(map_replace_lines(SUITABILITY_ACTUAL_MAP, row_key, "0", indent))
    if row["type"] == "condition_bonus":
        lines.append(f"{prefix}if = {{")
        lines.append(f"{prefix}{T}limit = {{")
        append_suitability_condition_limit(lines, row["condition"], indent + 2)
        lines.append(f"{prefix}{T}}}")
        lines.extend(map_replace_lines(SUITABILITY_ACTUAL_MAP, row_key, fmt_value(row["value"]), indent + 1))
        lines.append(f"{prefix}}}")
        return

    source = row["source"]
    if source not in SUITABILITY_SOURCE_EXPRESSIONS:
        raise ValueError(f"Missing suitability actual source expression for {source}")
    source_expression = SUITABILITY_SOURCE_EXPRESSIONS[source]
    lines.append(f"{prefix}if = {{")
    lines.append(f"{prefix}{T}limit = {{ tv_wonder_survey_site_selected_trigger = yes }}")
    lines.append(f"{prefix}{T}set_variable = {{ name = {SUITABILITY_ACTUAL_TEMP_VAR} value = var:tv_wonder_survey_site.{source_expression} }}")
    lines.append(
        f"{prefix}{T}clamp_variable = {{ name = {SUITABILITY_ACTUAL_TEMP_VAR} "
        f"min = {fmt_value(row['min'])} max = {fmt_value(row['max'])} }}"
    )
    lines.append(f"{prefix}{T}change_variable = {{ name = {SUITABILITY_ACTUAL_TEMP_VAR} multiply = {fmt_value(row['multiplier'])} }}")
    lines.extend(map_replace_lines(SUITABILITY_ACTUAL_MAP, row_key, f"var:{SUITABILITY_ACTUAL_TEMP_VAR}", indent + 1))
    lines.append(f"{prefix}{T}remove_variable = {SUITABILITY_ACTUAL_TEMP_VAR}")
    lines.append(f"{prefix}}}")


def append_suitability_actual_effects(
    lines: list[str],
    wonders: list[dict],
    mechanics: dict,
    by_key: dict[str, dict],
) -> None:
    lines.append("tv_wonder_mechanics_clear_suitability_actuals_effect = {")
    lines.append(f"{T}clear_variable_map = {SUITABILITY_ACTUAL_MAP}")
    lines.append(f"{T}tv_wonder_mechanics_clear_current_suitability_actual_cache_effect = yes")
    lines.append("}")
    lines.append("")

    for wonder in wonders:
        rows = suitability_knowledge_for_wonder(mechanics, wonder)
        lines.append(f"tv_wonder_calculate_{wonder['key']}_suitability_actuals_effect = {{")
        for row_index, row in enumerate(rows, start=1):
            append_suitability_actual_row(lines, wonder, row, row_index, by_key, 1)
        lines.append(f"{T}tv_wonder_mechanics_refresh_current_suitability_display_cache_effect = yes")
        lines.append("}")
        lines.append("")

    lines.append("tv_wonder_mechanics_calculate_suitability_actuals_effect = {")
    for idx, wonder in enumerate(wonders):
        head = "if" if idx == 0 else "else_if"
        lines.append(f"{T}{head} = {{")
        lines.append(f"{T}{T}limit = {{ var:tv_wonder_locked ?= {wonder['id']} }}")
        lines.append(f"{T}{T}tv_wonder_calculate_{wonder['key']}_suitability_actuals_effect = yes")
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_survey_cache_transfer_effects(lines: list[str], max_rows: int) -> None:
    completed_survey_maps = [
        LOCATION_SURVEYED_MAP,
        LOCATION_SURVEY_SCALE_MAP,
        LOCATION_SURVEY_LOGISTICS_MAP,
        LOCATION_SURVEY_ORGANIZATION_MAP,
        LOCATION_SURVEY_SCALE_TIER_MAP,
    ]
    competence_maps = [
        (LOCATION_SURVEY_SCALE_MAP, "tv_wonder_scale_competence"),
        (LOCATION_SURVEY_LOGISTICS_MAP, "tv_wonder_logistics_competence"),
        (LOCATION_SURVEY_ORGANIZATION_MAP, "tv_wonder_organization_competence"),
        (LOCATION_SURVEY_SCALE_TIER_MAP, "tv_wonder_scale_tier"),
    ]

    lines.append("tv_wonder_mechanics_copy_completed_survey_from_location_effect = {")
    lines.append(f"{T}tv_wonder_index_refresh_country_cache_effect = yes")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_locked")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_locked_mechanic_id")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}set_variable = {{ name = {SURVEY_WONDER_KEY_VAR} value = var:tv_wonder_locked }}")
    lines.append(f"{T}{T}set_variable = {{ name = {SURVEY_MECHANIC_KEY_VAR} value = var:tv_wonder_locked_mechanic_id }}")
    lines.append(f"{T}}}")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}has_variable = {SURVEY_WONDER_KEY_VAR}")
    lines.append(f"{T}{T}{T}has_variable = {SURVEY_MECHANIC_KEY_VAR}")
    lines.append(f"{T}{T}{T}exists = scope:tv_wonder_selected_survey_site")
    lines.append(f"{T}{T}{T}scope:tv_wonder_selected_survey_site = {{")
    lines.extend(map_key_exists_condition(LOCATION_SURVEYED_MAP, "prev.var:" + SURVEY_WONDER_KEY_VAR, 4))
    lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}scope:tv_wonder_selected_survey_site = {{")
    for map_name, target_var in competence_maps:
        lines.append(f"{T}{T}{T}if = {{")
        lines.append(f"{T}{T}{T}{T}limit = {{")
        lines.extend(map_key_exists_condition(map_name, "prev.var:" + SURVEY_WONDER_KEY_VAR, 5))
        lines.append(f"{T}{T}{T}{T}}}")
        lines.append(
            f"{T}{T}{T}{T}set_variable = {{ name = {SURVEY_LOCATION_COPY_TEMP_VAR} "
            f"value = \"variable_map({map_name}|prev.var:{SURVEY_WONDER_KEY_VAR})\" }}"
        )
        lines.append(
            f"{T}{T}{T}{T}prev = {{ set_variable = {{ name = {target_var} "
            f"value = scope:tv_wonder_selected_survey_site.var:{SURVEY_LOCATION_COPY_TEMP_VAR} }} }}"
        )
        lines.append(f"{T}{T}{T}{T}remove_variable = {SURVEY_LOCATION_COPY_TEMP_VAR}")
        lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}set_variable = {{ name = tv_wonder_survey_complete value = 1 }}")
    lines.append(f"{T}{T}remove_variable = tv_wonder_survey_active")
    lines.append(f"{T}{T}tv_wonder_set_io_survey_progress_effect = {{ value = 100 }}")
    lines.append(f"{T}{T}tv_wonder_update_construction_tiers_from_competence_effect = yes")
    lines.append(f"{T}{T}tv_wonder_mechanics_calculate_suitability_actuals_effect = yes")
    for row_index in range(1, max_rows + 1):
        lines.extend(set_survey_row_key_var_lines(row_index, 2))
        lines.append(f"{T}{T}scope:tv_wonder_selected_survey_site = {{")
        lines.append(f"{T}{T}{T}if = {{")
        lines.append(f"{T}{T}{T}{T}limit = {{")
        lines.extend(map_key_exists_condition(LOCATION_SURVEY_ACTUAL_MAP, "prev.var:" + SURVEY_ROW_KEY_VAR, 5))
        lines.append(f"{T}{T}{T}{T}}}")
        lines.append(
            f"{T}{T}{T}{T}set_variable = {{ name = {SURVEY_LOCATION_COPY_TEMP_VAR} "
            f"value = \"variable_map({LOCATION_SURVEY_ACTUAL_MAP}|prev.var:{SURVEY_ROW_KEY_VAR})\" }}"
        )
        lines.append(f"{T}{T}{T}{T}prev = {{")
        lines.extend(
            map_replace_lines(
                SUITABILITY_ACTUAL_MAP,
                "var:" + SURVEY_ROW_KEY_VAR,
                f"scope:tv_wonder_selected_survey_site.var:{SURVEY_LOCATION_COPY_TEMP_VAR}",
                5,
            )
        )
        lines.append(f"{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}{T}remove_variable = {SURVEY_LOCATION_COPY_TEMP_VAR}")
        lines.append(f"{T}{T}{T}}}")
        lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}tv_wonder_mechanics_refresh_current_suitability_display_cache_effect = yes")
    lines.append(f"{T}}}")
    lines.append(f"{T}remove_variable = {SURVEY_ROW_KEY_VAR}")
    lines.append(f"{T}remove_variable = {SURVEY_MECHANIC_KEY_VAR}")
    lines.append(f"{T}remove_variable = {SURVEY_WONDER_KEY_VAR}")
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_clear_completed_survey_from_location_effect = {")
    lines.append(f"{T}tv_wonder_index_refresh_country_cache_effect = yes")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}exists = scope:tv_wonder_selected_survey_site")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_locked")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_locked_mechanic_id")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}set_variable = {{ name = {SURVEY_WONDER_KEY_VAR} value = var:tv_wonder_locked }}")
    lines.append(f"{T}{T}set_variable = {{ name = {SURVEY_MECHANIC_KEY_VAR} value = var:tv_wonder_locked_mechanic_id }}")
    lines.append(f"{T}{T}scope:tv_wonder_selected_survey_site = {{")
    for map_name in completed_survey_maps:
        lines.append(f"{T}{T}{T}remove_from_variable_map = {{ name = {map_name} key = prev.var:{SURVEY_WONDER_KEY_VAR} }}")
    lines.append(f"{T}{T}}}")
    for row_index in range(1, max_rows + 1):
        lines.extend(set_survey_row_key_var_lines(row_index, 2))
        lines.append(f"{T}{T}scope:tv_wonder_selected_survey_site = {{")
        lines.append(f"{T}{T}{T}remove_from_variable_map = {{ name = {LOCATION_SURVEY_ACTUAL_MAP} key = prev.var:{SURVEY_ROW_KEY_VAR} }}")
        lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}remove_variable = {SURVEY_ROW_KEY_VAR}")
    lines.append(f"{T}{T}remove_variable = {SURVEY_MECHANIC_KEY_VAR}")
    lines.append(f"{T}{T}remove_variable = {SURVEY_WONDER_KEY_VAR}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_store_survey_on_location_effect = {")
    lines.append(f"{T}tv_wonder_index_refresh_country_cache_effect = yes")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}tv_wonder_survey_site_selected_trigger = yes")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_locked")
    lines.append(f"{T}{T}{T}has_variable = tv_wonder_locked_mechanic_id")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}tv_wonder_mechanics_calculate_suitability_actuals_effect = yes")
    lines.append(f"{T}{T}set_variable = {{ name = {SURVEY_WONDER_KEY_VAR} value = var:tv_wonder_locked }}")
    lines.append(f"{T}{T}set_variable = {{ name = {SURVEY_MECHANIC_KEY_VAR} value = var:tv_wonder_locked_mechanic_id }}")
    lines.append(f"{T}{T}var:tv_wonder_survey_site ?= {{")
    lines.extend(map_replace_lines(LOCATION_SURVEYED_MAP, "prev.var:" + SURVEY_WONDER_KEY_VAR, "1", 3))
    lines.extend(map_replace_lines(LOCATION_SURVEY_SCALE_MAP, "prev.var:" + SURVEY_WONDER_KEY_VAR, "prev.var:tv_wonder_scale_competence", 3))
    lines.extend(map_replace_lines(LOCATION_SURVEY_LOGISTICS_MAP, "prev.var:" + SURVEY_WONDER_KEY_VAR, "prev.var:tv_wonder_logistics_competence", 3))
    lines.extend(map_replace_lines(LOCATION_SURVEY_ORGANIZATION_MAP, "prev.var:" + SURVEY_WONDER_KEY_VAR, "prev.var:tv_wonder_organization_competence", 3))
    lines.extend(map_replace_lines(LOCATION_SURVEY_SCALE_TIER_MAP, "prev.var:" + SURVEY_WONDER_KEY_VAR, "prev.var:tv_wonder_scale_tier", 3))
    lines.append(f"{T}{T}}}")
    for row_index in range(1, max_rows + 1):
        lines.extend(set_survey_row_key_var_lines(row_index, 2))
        lines.append(f"{T}{T}if = {{")
        lines.append(f"{T}{T}{T}limit = {{")
        lines.extend(map_key_exists_condition(SUITABILITY_ACTUAL_MAP, "var:" + SURVEY_ROW_KEY_VAR, 4))
        lines.append(f"{T}{T}{T}}}")
        lines.append(
            f"{T}{T}{T}set_variable = {{ name = {SURVEY_LOCATION_COPY_TEMP_VAR} "
            f"value = \"variable_map({SUITABILITY_ACTUAL_MAP}|var:{SURVEY_ROW_KEY_VAR})\" }}"
        )
        lines.append(f"{T}{T}{T}var:tv_wonder_survey_site ?= {{")
        lines.extend(
            map_replace_lines(
                LOCATION_SURVEY_ACTUAL_MAP,
                "prev.var:" + SURVEY_ROW_KEY_VAR,
                f"prev.var:{SURVEY_LOCATION_COPY_TEMP_VAR}",
                4,
            )
        )
        lines.append(f"{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}remove_variable = {SURVEY_LOCATION_COPY_TEMP_VAR}")
        lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}remove_variable = {SURVEY_ROW_KEY_VAR}")
    lines.append(f"{T}{T}remove_variable = {SURVEY_MECHANIC_KEY_VAR}")
    lines.append(f"{T}{T}remove_variable = {SURVEY_WONDER_KEY_VAR}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_roll_random_feasible_proposal_effect(lines: list[str], name: str, deck_map: str) -> None:
    lines.append(f"{name} = {{")
    lines.append(f"{T}remove_variable = tv_wonder_proposal")
    lines.append(f"{T}save_scope_as = tv_wonder_proposal_owner")
    lines.append(f"{T}random_key_in_variable_map = {{")
    lines.append(f"{T}{T}variable = {deck_map}")
    lines.append(f"{T}{T}scope:tv_wonder_proposal_owner = {{")
    lines.append(f"{T}{T}{T}set_variable = {{ name = tv_wonder_proposal value = prev }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def finish_lines(lines: list[str]) -> str:
    return "\n".join(lines).rstrip() + "\n"


def append_proposal_effects(lines: list[str], all_wonders: list[dict]) -> None:
    lines.append("tv_wonder_mechanics_clear_feasible_deck_effect = {")
    lines.append(f"{T}clear_variable_map = {FEASIBLE_GENERIC_DECK_MAP}")
    lines.append(f"{T}clear_variable_map = {FEASIBLE_UNIQUE_DECK_MAP}")
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_rebuild_feasible_deck_effect = {")
    for wonder in all_wonders:
        deck_map = FEASIBLE_UNIQUE_DECK_MAP if wonder.get("is_unique") else FEASIBLE_GENERIC_DECK_MAP
        lines.append(f"{T}if = {{")
        lines.append(f"{T}{T}limit = {{ tv_wonder_can_build_{wonder['key']}_trigger = yes }}")
        lines.append(f"{T}{T}add_to_variable_map = {{ name = {deck_map} key = {wonder['id']} value = 1 }}")
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    append_roll_random_feasible_proposal_effect(
        lines,
        "tv_wonder_generic_roll_random_feasible_proposal_effect",
        FEASIBLE_GENERIC_DECK_MAP,
    )
    append_roll_random_feasible_proposal_effect(
        lines,
        "tv_wonder_unique_roll_random_feasible_proposal_effect",
        FEASIBLE_UNIQUE_DECK_MAP,
    )

    lines.append("tv_wonder_roll_next_slot_from_priority_deck_effect = {")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ tv_wonder_unique_has_any_feasible_proposal_trigger = yes }}")
    lines.append(f"{T}{T}tv_wonder_unique_roll_random_feasible_proposal_effect = yes")
    lines.append(f"{T}}}")
    lines.append(f"{T}else_if = {{")
    lines.append(f"{T}{T}limit = {{ tv_wonder_generic_has_any_feasible_proposal_trigger = yes }}")
    lines.append(f"{T}{T}tv_wonder_generic_roll_random_feasible_proposal_effect = yes")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_remove_current_proposal_from_deck_effect = {")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ var:tv_wonder_proposal ?= {{ this >= {ALL_WONDER_MIN_ID} }} }}")
    lines.append(f"{T}{T}set_local_variable = {{ name = tv_wonder_current_proposal_id value = var:tv_wonder_proposal }}")
    lines.append(f"{T}{T}remove_from_variable_map = {{ name = {FEASIBLE_GENERIC_DECK_MAP} key = local_var:tv_wonder_current_proposal_id }}")
    lines.append(f"{T}{T}remove_from_variable_map = {{ name = {FEASIBLE_UNIQUE_DECK_MAP} key = local_var:tv_wonder_current_proposal_id }}")
    lines.append(f"{T}{T}remove_local_variable = tv_wonder_current_proposal_id")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_accept_proposal_tooltip_effect = {")
    lines.append(f"{T}custom_tooltip = {{ text = tv_wonder_accept_proposal_desc }}")
    lines.append("}")
    lines.append("")


def generate_proposal_effects(script_rel: str = PROPOSAL_SCRIPT_REL) -> str:
    all_wonders, _mechanics = load_all_wonder_mechanics()
    lines = render_header(script_rel)
    append_proposal_effects(lines, all_wonders)
    return finish_lines(lines)


def append_survey_effects(
    lines: list[str],
    all_wonders: list[dict],
    mechanics: dict,
    by_key: dict[str, dict],
) -> None:
    append_current_suitability_display_cache_effects(lines, all_wonders, mechanics)
    append_suitability_actual_effects(lines, all_wonders, mechanics, by_key)
    max_rows = max(len(suitability_knowledge_for_wonder(mechanics, wonder)) for wonder in all_wonders)
    append_survey_cache_transfer_effects(lines, max_rows)

    lines.append("tv_wonder_mechanics_apply_survey_site_preference_effect = {")
    for idx, wonder in enumerate(all_wonders):
        head = "if" if idx == 0 else "else_if"
        lines.append(f"{T}{head} = {{")
        lines.append(f"{T}{T}limit = {{")
        lines.append(f"{T}{T}{T}var:tv_wonder_locked ?= {wonder['id']}")
        lines.append(f"{T}{T}{T}tv_wonder_survey_site_selected_trigger = yes")
        lines.append(f"{T}{T}}}")
        lines.extend(add_site_preference(wonder, mechanics, 2))
        lines.append(f"{T}{T}tv_wonder_calculate_{wonder['key']}_suitability_actuals_effect = yes")
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_start_survey_effect = {")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}exists = scope:target")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}tv_wonder_clear_current_survey_effect = yes")
    lines.append(f"{T}{T}tv_wonder_mechanics_clear_suitability_actuals_effect = yes")
    lines.append(f"{T}{T}scope:target = {{ save_scope_as = tv_wonder_selected_survey_site }}")
    lines.append(f"{T}{T}set_variable = {{ name = tv_wonder_survey_site value = scope:target }}")
    lines.append(f"{T}{T}set_variable = {{ name = tv_wonder_stage value = 2 }}")
    lines.append(f"{T}{T}if = {{")
    lines.append(f"{T}{T}{T}limit = {{ tv_wonder_selected_survey_already_cached_trigger = yes }}")
    lines.append(f"{T}{T}{T}tv_wonder_copy_completed_survey_from_location_effect = yes")
    lines.append(f"{T}{T}{T}remove_variable = tv_wonder_cmm_skip_survey")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}else_if = {{")
    lines.append(f"{T}{T}{T}limit = {{ has_variable = tv_wonder_cmm_skip_survey }}")
    lines.append(f"{T}{T}{T}set_variable = {{ name = tv_wonder_survey_active value = 1 }}")
    lines.append(f"{T}{T}{T}set_variable = {{ name = tv_wonder_scale_competence value = 100 }}")
    lines.append(f"{T}{T}{T}set_variable = {{ name = tv_wonder_logistics_competence value = 85 }}")
    lines.append(f"{T}{T}{T}set_variable = {{ name = tv_wonder_organization_competence value = 85 }}")
    lines.append(f"{T}{T}{T}tv_wonder_mechanics_complete_survey_effect = yes")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}else = {{")
    lines.append(f"{T}{T}{T}set_variable = {{ name = tv_wonder_survey_active value = 1 }}")
    lines.append(f"{T}{T}{T}tv_wonder_prepare_survey_competence_targets_effect = yes")
    lines.append(f"{T}{T}{T}tv_wonder_set_io_survey_progress_effect = {{ value = 0 }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    lines.append("tv_wonder_mechanics_complete_survey_effect = {")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ tv_wonder_survey_active_trigger = yes }}")
    lines.append(f"{T}{T}clamp_variable = {{ name = tv_wonder_scale_competence min = 0 max = 100 }}")
    lines.append(f"{T}{T}clamp_variable = {{ name = tv_wonder_logistics_competence min = 0 max = 100 }}")
    lines.append(f"{T}{T}clamp_variable = {{ name = tv_wonder_organization_competence min = 0 max = 100 }}")
    lines.append(f"{T}{T}tv_wonder_update_construction_tiers_from_competence_effect = yes")
    lines.append(f"{T}{T}tv_wonder_store_survey_on_location_effect = yes")
    lines.append(f"{T}{T}tv_wonder_mechanics_reveal_suitability_knowledge_effect = yes")
    lines.append(f"{T}{T}set_variable = {{ name = tv_wonder_survey_complete value = 1 }}")
    lines.append(f"{T}{T}remove_variable = tv_wonder_cmm_skip_survey")
    lines.append(f"{T}{T}remove_variable = tv_wonder_survey_active")
    lines.append(f"{T}{T}remove_variable = tv_wonder_survey_speed")
    lines.append(f"{T}{T}remove_variable = tv_wonder_scale_competence_target")
    lines.append(f"{T}{T}remove_variable = tv_wonder_logistics_competence_target")
    lines.append(f"{T}{T}remove_variable = tv_wonder_organization_competence_target")
    lines.append(f"{T}{T}remove_variable = tv_wonder_scale_competence_monthly_gain")
    lines.append(f"{T}{T}remove_variable = tv_wonder_logistics_competence_monthly_gain")
    lines.append(f"{T}{T}remove_variable = tv_wonder_organization_competence_monthly_gain")
    lines.append(f"{T}{T}tv_wonder_set_io_survey_progress_effect = {{ value = 100 }}")
    lines.append(f"{T}{T}if = {{")
    lines.append(f"{T}{T}{T}limit = {{ tv_wonder_survey_site_selected_trigger = yes }}")
    lines.append(f"{T}{T}{T}var:tv_wonder_survey_site ?= {{ save_scope_as = tv_wonder_event_location }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}set_variable = {{ name = tv_wonder_survey_competence_average value = var:tv_wonder_scale_competence }}")
    lines.append(f"{T}{T}change_variable = {{ name = tv_wonder_survey_competence_average add = var:tv_wonder_logistics_competence }}")
    lines.append(f"{T}{T}change_variable = {{ name = tv_wonder_survey_competence_average add = var:tv_wonder_organization_competence }}")
    lines.append(f"{T}{T}change_variable = {{ name = tv_wonder_survey_competence_average divide = 3 }}")
    lines.append(f"{T}{T}{monthly_country_pulse_event('tv_engineering_department.300')}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")

    append_suitability_reveal_effect(lines)


def generate_survey_effects(script_rel: str = SURVEY_SCRIPT_REL) -> str:
    all_wonders, mechanics = load_all_wonder_mechanics()
    by_key = all_wonders_by_key(all_wonders)
    lines = render_header(script_rel, PULSE_DATA_REL)
    append_survey_effects(lines, all_wonders, mechanics, by_key)
    return finish_lines(lines)


def append_location_display_group(
    lines: list[str],
    all_wonders: list[dict],
    unique_wonders: list[dict],
    mechanics: dict,
) -> None:
    append_display_modifier_reference_effect(lines, all_wonders)
    append_final_building_level_map_sync_effects(lines)
    append_final_building_level_changed_effects(lines, all_wonders, mechanics)
    append_existing_unique_wonders_initialization_effect(lines, unique_wonders)
    append_country_auto_level_map_effect(lines)
    append_location_display_effects(lines)


def generate_location_display_effects(script_rel: str = LOCATION_DISPLAY_SCRIPT_REL) -> str:
    all_wonders, mechanics = load_all_wonder_mechanics()
    unique_wonders = [wonder for wonder in all_wonders if wonder.get("is_unique")]
    lines = render_header(script_rel)
    append_location_display_group(lines, all_wonders, unique_wonders, mechanics)
    return finish_lines(lines)


def append_project_state_cleanup_effect(lines: list[str], all_wonders: list[dict], mechanics: dict, ritual_entry_list: list) -> None:
    lines.extend(["tv_wonder_mechanics_clear_project_state_effect = {", "\tclear_variable_map = tv_wonder_feasible_generic_deck", "\tclear_variable_map = tv_wonder_feasible_unique_deck", "\ttv_wonder_ritual_clear_project_effect = yes", "}", ""])


def generate() -> str:
    all_wonders, mechanics = load_all_wonder_mechanics()
    lines = render_header(SCRIPT_REL)
    append_project_state_cleanup_effect(
        lines,
        all_wonders,
        mechanics,
        ritual_entries(all_wonders, mechanics),
    )
    return finish_lines(lines)


def main() -> None:
    OUT_FILE.write_text("\ufeff" + generate(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
