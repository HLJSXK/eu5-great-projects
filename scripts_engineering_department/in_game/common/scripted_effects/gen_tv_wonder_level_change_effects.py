"""Generate the external wonder level-change interface.

Four public scripted effects let non-Engineering-Department features change a
completed wonder's level by exactly one step:

    tv_wonder_raise_generic_level_effect = { wonder = <generic key> style = <1-3> }   # location scope
    tv_wonder_lower_generic_level_effect = { wonder = <generic key> }                 # location scope
    tv_wonder_raise_unique_level_effect = { wonder = <unique key> }                   # any scope
    tv_wonder_lower_unique_level_effect = { wonder = <unique key> }                   # any scope

The wrappers substitute the key into a static per-wonder effect name. Per-wonder
dispatchers are thin: they check which final building stands at the site and call
one of three shared helpers that own the level-change logic, the cap/scale guard,
and the next-day resync dispatch. The contract (boundaries, lifecycle, rewards)
is documented in docs/design/Wonder_Level_Change_Interface.md.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.naming import (
    EXTERNAL_LOWER_GENERIC_LEVEL_EFFECT_PATTERN,
    EXTERNAL_LOWER_GENERIC_LEVEL_PUBLIC_EFFECT,
    EXTERNAL_LOWER_UNIQUE_LEVEL_EFFECT_PATTERN,
    EXTERNAL_LOWER_UNIQUE_LEVEL_PUBLIC_EFFECT,
    EXTERNAL_RAISE_GENERIC_LEVEL_EFFECT_PATTERN,
    EXTERNAL_RAISE_GENERIC_LEVEL_PUBLIC_EFFECT,
    EXTERNAL_RAISE_UNIQUE_LEVEL_EFFECT_PATTERN,
    EXTERNAL_RAISE_UNIQUE_LEVEL_PUBLIC_EFFECT,
    external_lower_generic_level_effect_name,
    external_lower_unique_level_effect_name,
    external_raise_existing_level_effect_name,
    external_raise_generic_level_effect_name,
    external_raise_unique_level_effect_name,
    final_building_completion_sync_hidden_event_trigger_effect_name,
    final_building_level_sync_hidden_event_id,
)
from wonder_mechanics.render import render_header
from wonder_mechanics.rituals import ritual_style_ids

OUT_FILE = (
    REPO_ROOT / "src" / "in_game" / "common" / "scripted_effects"
    / "tv_wonder_level_change_effects.txt"
)
SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_level_change_effects.py"
TRIGGERS_FILE = (
    REPO_ROOT / "src" / "in_game" / "common" / "scripted_triggers"
    / "tv_wonder_level_change_triggers.txt"
)
DATA_REL = "data/wonders.yaml + data/unique_wonders.yaml"
T = "\t"
MAX_LEVEL = 6

PROJECT_REQUEST_EFFECT = "tv_wonder_request_external_project_level_raise_effect"
PROJECT_QUEUE_EFFECT = "tv_wonder_queue_external_project_level_raise_effect"
PROJECT_PENDING_VAR = "tv_wonder_external_project_level_raise_pending"
PROJECT_EVENT_ID = 207
ACTIVE_PROJECT_TRIGGER = "tv_wonder_location_has_active_project_for_trigger"
SCALE_ALLOWS_TRIGGER = "tv_wonder_location_scale_allows_level_trigger"
PROJECT_BELOW_CAP_TRIGGER = "tv_wonder_project_level_below_scale_tier_trigger"

# Shared helpers — the single place that owns level-change logic.
RAISE_HELPER = "tv_wonder_raise_final_building_level_effect"
LOWER_HELPER = "tv_wonder_lower_final_building_level_effect"
FOUND_HELPER = "tv_wonder_found_final_building_level_effect"

FOUNDED_TEXT = "tv_wonder_level_founded_text"
DESTROYED_TEXT = "tv_wonder_level_destroyed_text"
PROJECT_RAISED_TEXT = "tv_wonder_level_raised_project_text"
RAISE_CAPPED_TT = "TV_WONDER_LEVEL_RAISE_CAPPED_TT"
RAISE_PROJECT_CAPPED_TT = "TV_WONDER_LEVEL_RAISE_PROJECT_CAPPED_TT"
RAISE_UNOWNED_TT = "TV_WONDER_LEVEL_RAISE_UNOWNED_TT"
LOWER_ABSENT_TT = "TV_WONDER_LEVEL_LOWER_ABSENT_TT"


def effect_localization_keys() -> list[str]:
    """Every custom_description text this generator emits (registered by hand in effect_localization)."""
    return [FOUNDED_TEXT, DESTROYED_TEXT, PROJECT_RAISED_TEXT]


def custom_tooltip_keys() -> list[str]:
    return [RAISE_CAPPED_TT, RAISE_PROJECT_CAPPED_TT, RAISE_UNOWNED_TT, LOWER_ABSENT_TT]


def building_ref(building: str) -> str:
    return f"building_type:{building}"


def level_at_least(building: str, level: int) -> str:
    """The building argument is a typed reference, including helper parameters."""
    return f"location_building_level = {{ building_type = {building} value >= {level} }}"


def wonder_buildings(wonder: dict) -> list[str]:
    return [wonder["final_building"] for style in ritual_style_ids(wonder)]


def sync_event_id(wonder: dict) -> int:
    return final_building_level_sync_hidden_event_id(wonder)


# ===== Shared helpers =====


def append_raise_helper(lines: list[str]) -> None:
    """Raise an existing final building by one level, respecting the cap and scale tier."""
    lines.append(f"# Location scope. $building$ = building_type:X, $wonder_id$ = N, $sync_event_id$ = 94XX.")
    lines.append(f"# Auto-generated 'Gains 1 [BUILDING_TYPE.GetName]' tooltip conveys the change;")
    lines.append(f"# the cap-failure branch shows a custom_tooltip instead.")
    lines.append(f"{RAISE_HELPER} = {{")
    for current in range(MAX_LEVEL, 0, -1):
        target = current + 1
        if current == MAX_LEVEL:
            lines.append(f"{T}if = {{")
            lines.append(f"{T}{T}limit = {{ {level_at_least('$building$', current)} }}")
            lines.append(f"{T}{T}custom_tooltip = {{ text = {RAISE_CAPPED_TT} }}")
            lines.append(f"{T}}}")
        else:
            lines.append(f"{T}else_if = {{")
            lines.append(f"{T}{T}limit = {{ {level_at_least('$building$', current)} }}")
            lines.append(f"{T}{T}if = {{")
            lines.append(
                f"{T}{T}{T}limit = {{ {SCALE_ALLOWS_TRIGGER} = {{ wonder_id = $wonder_id$ level = {target} }} }}"
            )
            lines.append(
                f"{T}{T}{T}change_building_level_in_location = {{ building = $building$ value = 1 owner = owner }}"
            )
            lines.append(
                f"{T}{T}{T}hidden_effect = {{ trigger_event_silently = {{ id = tv_engineering_department.$sync_event_id$ days = 1 }} }}"
            )
            lines.append(f"{T}{T}}}")
            lines.append(f"{T}{T}else = {{ custom_tooltip = {{ text = {RAISE_CAPPED_TT} }} }}")
            lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_lower_helper(lines: list[str]) -> None:
    """Lower a final building by one level. Level 1 → 0 destroys the wonder."""
    lines.append(f"# Location scope. $building$ = building_type:X, $sync_event_id$ = 94XX.")
    lines.append(f"# Levels 2-6 use the auto-generated 'Loses 1 [BUILDING_TYPE.GetName]' tooltip;")
    lines.append(f"# level 1 → 0 uses a custom_description so the player sees 'destroyed'.")
    lines.append(f"{LOWER_HELPER} = {{")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{ {level_at_least('$building$', 2)} }}")
    lines.append(f"{T}{T}change_building_level_in_location = {{ building = $building$ value = -1 }}")
    lines.append(
        f"{T}{T}hidden_effect = {{ trigger_event_silently = {{ id = tv_engineering_department.$sync_event_id$ days = 1 }} }}"
    )
    lines.append(f"{T}}}")
    lines.append(f"{T}else_if = {{")
    lines.append(f"{T}{T}limit = {{ {level_at_least('$building$', 1)} }}")
    lines.append(f"{T}{T}custom_description = {{")
    lines.append(f"{T}{T}{T}text = {DESTROYED_TEXT}")
    lines.append(f"{T}{T}{T}value = $building$")
    lines.append(f"{T}{T}{T}change_building_level_in_location = {{ building = $building$ value = -1 }}")
    lines.append(
        f"{T}{T}{T}hidden_effect = {{ trigger_event_silently = {{ id = tv_engineering_department.$sync_event_id$ days = 1 }} }}"
    )
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_found_helper(lines: list[str]) -> None:
    """Found a wonder at level 1 on a site that has no final building."""
    lines.append(f"# Location scope. $building$ = building_type:X, $sync_event_id$ = 94XX.")
    lines.append(f"{FOUND_HELPER} = {{")
    lines.append(f"{T}custom_description = {{")
    lines.append(f"{T}{T}text = {FOUNDED_TEXT}")
    lines.append(f"{T}{T}value = $building$")
    lines.append(
        f"{T}{T}construct_building = {{ building_type = $building$ "
        'cost_multiplier = 0 cost_multiplier_reason = "game_concept_event" instant = yes }'
    )
    lines.append(f"{T}{T}hidden_effect = {{")
    lines.append(f"{T}{T}{T}{final_building_completion_sync_hidden_event_trigger_effect_name()} = yes")
    lines.append(
        f"{T}{T}{T}trigger_event_silently = {{ id = tv_engineering_department.$sync_event_id$ days = 1 }}"
    )
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


# ===== Per-wonder dispatchers =====


def append_raise_existing_effect(lines: list[str], wonder: dict) -> None:
    """Check which final building stands here and call the shared raise helper."""
    buildings = wonder_buildings(wonder)
    wid = int(wonder["id"])
    sid = sync_event_id(wonder)
    lines.append(f"{external_raise_existing_level_effect_name(wonder)} = {{")
    for index, building in enumerate(buildings):
        head = "if" if index == 0 else "else_if"
        lines.append(f"{T}{head} = {{")
        lines.append(f"{T}{T}limit = {{ {level_at_least(building_ref(building), 1)} }}")
        lines.append(f"{T}{T}{RAISE_HELPER} = {{ building = {building_ref(building)} wonder_id = {wid} sync_event_id = {sid} }}")
        lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


def append_generic_effects(lines: list[str], wonder: dict) -> None:
    append_raise_existing_effect(lines, wonder)
    styles = [1]
    buildings = wonder_buildings(wonder)
    wid = int(wonder["id"])
    sid = sync_event_id(wonder)
    any_level = "OR = { " + " ".join(level_at_least(building_ref(b), 1) for b in buildings) + " }"
    for style in styles:
        found_building = wonder["final_building"]
        lines.append(f"# Location scope. Founds style {style} when no {wonder['key']} stands here.")
        lines.append(f"{external_raise_generic_level_effect_name(wonder)} = {{")
        lines.append(f"{T}if = {{")
        lines.append(f"{T}{T}limit = {{ NOT = {{ has_owner = yes }} }}")
        lines.append(f"{T}{T}custom_tooltip = {{ text = {RAISE_UNOWNED_TT} }}")
        lines.append(f"{T}}}")
        lines.append(f"{T}else_if = {{")
        lines.append(f"{T}{T}limit = {{ {ACTIVE_PROJECT_TRIGGER} = {{ wonder_id = {wid} }} }}")
        lines.append(f"{T}{T}{PROJECT_REQUEST_EFFECT} = yes")
        lines.append(f"{T}}}")
        lines.append(f"{T}else_if = {{")
        lines.append(f"{T}{T}limit = {{ {any_level} }}")
        lines.append(f"{T}{T}{external_raise_existing_level_effect_name(wonder)} = yes")
        lines.append(f"{T}}}")
        lines.append(f"{T}else = {{")
        lines.append(f"{T}{T}{FOUND_HELPER} = {{ building = {building_ref(found_building)} sync_event_id = {sid} }}")
        lines.append(f"{T}}}")
        lines.append("}")
        lines.append("")
    lines.append(f"{external_lower_generic_level_effect_name(wonder)} = {{")
    for index, building in enumerate(buildings):
        head = "if" if index == 0 else "else_if"
        lines.append(f"{T}{head} = {{")
        lines.append(f"{T}{T}limit = {{ {level_at_least(building_ref(building), 1)} }}")
        lines.append(f"{T}{T}{LOWER_HELPER} = {{ building = {building_ref(building)} sync_event_id = {sid} }}")
        lines.append(f"{T}}}")
    lines.append(f"{T}else = {{ custom_tooltip = {{ text = {LOWER_ABSENT_TT} }} }}")
    lines.append("}")
    lines.append("")


def append_unique_effects(lines: list[str], wonder: dict) -> None:
    styles = [1]
    if len(styles) != 1:
        raise ValueError(f"{wonder['key']}: unique wonders must have exactly one final building style")
    append_raise_existing_effect(lines, wonder)
    location = wonder["location"]
    wid = int(wonder["id"])
    sid = sync_event_id(wonder)
    building = wonder["final_building"]
    lines.append(f"# Any scope. Always acts on the fixed site location:{location}.")
    lines.append(f"{external_raise_unique_level_effect_name(wonder)} = {{")
    lines.append(f"{T}location:{location} = {{")
    lines.append(f"{T}{T}if = {{")
    lines.append(f"{T}{T}{T}limit = {{ NOT = {{ has_owner = yes }} }}")
    lines.append(f"{T}{T}{T}custom_tooltip = {{ text = {RAISE_UNOWNED_TT} }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}else_if = {{")
    lines.append(f"{T}{T}{T}limit = {{ {ACTIVE_PROJECT_TRIGGER} = {{ wonder_id = {wid} }} }}")
    lines.append(f"{T}{T}{T}{PROJECT_REQUEST_EFFECT} = yes")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}else_if = {{")
    lines.append(f"{T}{T}{T}limit = {{ {level_at_least(building_ref(building), 1)} }}")
    lines.append(f"{T}{T}{T}{external_raise_existing_level_effect_name(wonder)} = yes")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}else = {{")
    lines.append(f"{T}{T}{T}{FOUND_HELPER} = {{ building = {building_ref(building)} sync_event_id = {sid} }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")
    lines.append(f"{external_lower_unique_level_effect_name(wonder)} = {{")
    lines.append(f"{T}location:{location} = {{")
    lines.append(f"{T}{T}if = {{")
    lines.append(f"{T}{T}{T}limit = {{ {level_at_least(building_ref(building), 1)} }}")
    lines.append(f"{T}{T}{T}{LOWER_HELPER} = {{ building = {building_ref(building)} sync_event_id = {sid} }}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}{T}else = {{ custom_tooltip = {{ text = {LOWER_ABSENT_TT} }} }}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("")


# ===== Public interface =====


def append_public_interface(lines: list[str]) -> None:
    lines.extend([
        "# ===== Public interface =====",
        "# The only supported way for other features to change a completed wonder's level.",
        "# One call = one level. Same-day repeated calls read the pre-change building level",
        "# (level changes are queued engine tasks), so callers wanting several steps must",
        "# space them across days. See docs/design/Wonder_Level_Change_Interface.md.",
        "",
    ])
    wrappers = [
        (EXTERNAL_RAISE_GENERIC_LEVEL_PUBLIC_EFFECT, EXTERNAL_RAISE_GENERIC_LEVEL_EFFECT_PATTERN,
         {"key": "$wonder$"},
         ["# Location scope. wonder = generic key from data/wonders.yaml, style = ceremony style 1-3.",
          "# style only matters when founding from level 0; an existing wonder keeps its style."]),
        (EXTERNAL_LOWER_GENERIC_LEVEL_PUBLIC_EFFECT, EXTERNAL_LOWER_GENERIC_LEVEL_EFFECT_PATTERN,
         {"key": "$wonder$"},
         ["# Location scope. wonder = generic key. Level 1 -> 0 destroys the wonder."]),
        (EXTERNAL_RAISE_UNIQUE_LEVEL_PUBLIC_EFFECT, EXTERNAL_RAISE_UNIQUE_LEVEL_EFFECT_PATTERN,
         {"key": "$wonder$"},
         ["# Any scope. wonder = unique key from data/unique_wonders.yaml; acts on its fixed location."]),
        (EXTERNAL_LOWER_UNIQUE_LEVEL_PUBLIC_EFFECT, EXTERNAL_LOWER_UNIQUE_LEVEL_EFFECT_PATTERN,
         {"key": "$wonder$"},
         ["# Any scope. wonder = unique key. Level 1 -> 0 destroys the wonder."]),
    ]
    for name, pattern, params, comment_lines in wrappers:
        target = pattern.format(**params)
        lines.extend(comment_lines)
        lines.append(f"{name} = {{")
        lines.append(f"{T}{target} = yes")
        lines.append("}")
        lines.append("")


# ===== Active project redirect =====


def append_project_request_effects(lines: list[str]) -> None:
    lines.extend([
        "# ===== Active Engineering Department project at the same site =====",
        "# Location scope. The owner is building/expanding this same wonder here, so the",
        "# raise advances the project by one level instead of touching the final building.",
        "# Hover only renders persistent project state; the mutation runs in the immediate",
        f"# of tv_engineering_department.{PROJECT_EVENT_ID}, which also explains the change.",
        f"{PROJECT_REQUEST_EFFECT} = {{",
        f"{T}if = {{",
        f"{T}{T}limit = {{ owner ?= {{ {PROJECT_BELOW_CAP_TRIGGER} = yes }} }}",
    ])
    for current in range(0, MAX_LEVEL):
        head = "if" if current == 0 else "else_if"
        lines.extend([
            f"{T}{T}{head} = {{",
            f"{T}{T}{T}limit = {{ owner ?= {{ var:tv_wonder_level ?= {current} }} }}",
            f"{T}{T}{T}custom_description = {{",
            f"{T}{T}{T}{T}text = {PROJECT_RAISED_TEXT}",
            f"{T}{T}{T}{T}value = {current + 1}",
            f"{T}{T}{T}{T}hidden_effect = {{",
            f"{T}{T}{T}{T}{T}owner = {{ {PROJECT_QUEUE_EFFECT} = yes }}",
            f"{T}{T}{T}{T}}}",
            f"{T}{T}{T}}}",
            f"{T}{T}}}",
        ])
    lines.extend([
        f"{T}}}",
        f"{T}else = {{ custom_tooltip = {{ text = {RAISE_PROJECT_CAPPED_TT} }} }}",
        "}",
        "",
        "# Country scope. Collapses same-day duplicate requests into one queued raise.",
        f"{PROJECT_QUEUE_EFFECT} = {{",
        f"{T}if = {{",
        f"{T}{T}limit = {{ NOT = {{ has_variable = {PROJECT_PENDING_VAR} }} }}",
        f"{T}{T}set_variable = {{ name = {PROJECT_PENDING_VAR} value = 1 }}",
        f"{T}{T}trigger_event_non_silently = {{ id = tv_engineering_department.{PROJECT_EVENT_ID} }}",
        f"{T}}}",
        "}",
        "",
    ])


def generate() -> str:
    wonders, _mechanics = load_all_wonder_mechanics()
    lines = render_header(SCRIPT_REL, DATA_REL)
    append_public_interface(lines)
    lines.append("# ===== Shared helpers (internal; called by the per-wonder dispatchers) =====")
    lines.append("")
    append_raise_helper(lines)
    append_lower_helper(lines)
    append_found_helper(lines)
    append_project_request_effects(lines)
    lines.append("# ===== Per-wonder dispatchers (internal; call the public interface) =====")
    lines.append("")
    for wonder in wonders:
        if wonder.get("is_unique"):
            append_unique_effects(lines, wonder)
        else:
            append_generic_effects(lines, wonder)
    return "\n".join(lines).rstrip() + "\n"


def generate_triggers() -> str:
    # Quoted map links cannot contain scripted-trigger parameters. Dispatch by
    # the id in the trigger name, keeping each lookup key a generated literal.
    wonders, _mechanics = load_all_wonder_mechanics()
    lines = render_header(SCRIPT_REL, DATA_REL)
    for wonder in wonders:
        wid = wonder["id"]
        lines.extend([
            f"tv_wonder_location_survey_scale_allows_level_{wid}_trigger = {{",
            f'{T}"variable_map(tv_wonder_survey_scale_tier|{wid})" ?= {{ this >= $level$ }}',
            "}", "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUT_FILE.write_text("\ufeff" + generate(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")
    TRIGGERS_FILE.write_text(generate_triggers(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {TRIGGERS_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
