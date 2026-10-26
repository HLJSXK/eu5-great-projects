import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.io import (
    load_all_wonder_mechanics,
    load_wonders_source_data,
)
from wonder_mechanics.naming import PARTS, WONDER_SIZE_IDS
from wonder_mechanics.render import render_header
from wonder_mechanics.rituals import ritual_style_ids
from wonder_mechanics.schema import suitability_knowledge_for_wonder
from wonder_mechanics.suitability_conditions import (
    SUITABILITY_KNOWLEDGE_ROW_SLOTS,
    format_weight_literal,
    suitability_row_condition_id,
    suitability_row_key,
    suitability_row_weight,
)

OUT_FILE = REPO_ROOT / "src" / "in_game" / "common" / "scripted_effects" / "tv_wonder_index_effects.txt"
SCRIPT_REL = "scripts_engineering_department/in_game/common/scripted_effects/gen_tv_wonder_index_effects.py"
T = "\t"

WONDER_CACHE_VARS = [
    "tv_wonder_locked_is_unique",
    "tv_wonder_locked_base_id",
    "tv_wonder_locked_mechanic_id",
    "tv_wonder_locked_size",
    "tv_wonder_locked_style_count",
    "tv_wonder_locked_display_id",
    "tv_wonder_locked_concept_display_id",
    "tv_wonder_locked_image_display_id",
]


WONDER_MAP_NAMES = [
    "tv_wonder_id_to_is_unique",
    "tv_wonder_id_to_base_id",
    "tv_wonder_id_to_mechanic_id",
    "tv_wonder_id_to_size",
    "tv_wonder_id_to_style_count",
    "tv_wonder_id_to_display_id",
    "tv_wonder_id_to_concept_display_id",
    "tv_wonder_id_to_image_display_id",
    "tv_wonder_id_to_required_progress",
]


SUITABILITY_ROW_MAP_NAMES = [
    "tv_wonder_mechanic_id_to_suitability_row_count",
]

# Global, generation-time-static per-(mechanic_id, row) lookup tables backing the
# dynamic engineering department suitability panel widget. Keyed by
# flag:tv_wonder_suitability_<mechanic_id>_<row_index> (named, not a bare number, so an
# unused-flag warning in error.log is recognizable as this system's own state rather
# than looking like a stray concatenation bug) so the GUI can rebuild the same key at
# runtime via MakeScopeFlag(Concatenate(...)) - see
# gen_tv_engineering_department_wonder_mechanics_gui.py.
SUITABILITY_CONDITION_TYPE_MAP = "tv_wonder_suitability_condition_type"
SUITABILITY_WEIGHT_MAP = "tv_wonder_suitability_weight"

INTERMEDIATE_BUILDING_WONDER_ID_MAP = "tv_wonder_intermediate_building_type_to_wonder_id"
FINAL_BUILDING_WONDER_ID_MAP = "tv_wonder_final_building_type_to_wonder_id"
UNIQUE_WONDER_LOCATION_MAP = "tv_wonder_unique_id_to_location"
UNIQUE_WONDER_FINAL_BUILDING_TYPE_MAP = "tv_wonder_unique_id_to_final_building_type"

WONDER_CACHE_MAPS = [
    ("tv_wonder_id_to_is_unique", "tv_wonder_locked_is_unique"),
    ("tv_wonder_id_to_base_id", "tv_wonder_locked_base_id"),
    ("tv_wonder_id_to_mechanic_id", "tv_wonder_locked_mechanic_id"),
    ("tv_wonder_id_to_size", "tv_wonder_locked_size"),
    ("tv_wonder_id_to_style_count", "tv_wonder_locked_style_count"),
    ("tv_wonder_id_to_display_id", "tv_wonder_locked_display_id"),
    ("tv_wonder_id_to_concept_display_id", "tv_wonder_locked_concept_display_id"),
    ("tv_wonder_id_to_image_display_id", "tv_wonder_locked_image_display_id"),
]



def module_building_type_map_name(part: str) -> str:
    return f"tv_wonder_id_to_{part}_module_building_type"





def map_replace_line(map_name: str, key: str, value: object, indent: int = 1) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}remove_from_global_variable_map = {{ name = {map_name} key = {key} }}",
        f"{prefix}add_to_global_variable_map = {{ name = {map_name} key = {key} value = {value} }}",
    ]


def map_init_lines(map_name: str, indent: int = 1, value: object = 0) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}remove_from_global_variable_map = {{ name = {map_name} key = 0 }}",
        f"{prefix}add_to_global_variable_map = {{ name = {map_name} key = 0 value = {value} }}",
    ]


def append_clear_cache_effect(lines: list[str], name: str, variables: list[str]) -> None:
    lines.append(f"{name} = {{")
    for variable in variables:
        lines.append(f"{T}remove_variable = {variable}")
    lines.append("}")
    lines.append("")


def append_cache_effect(
    lines: list[str],
    *,
    name: str,
    local_key: str,
    clear_effect: str,
    key_setup_lines: list[str],
    cache_maps: list[tuple[str, str]],
) -> None:
    required_map = cache_maps[0][0]
    lines.append(f"{name} = {{")
    lines.append(f"{T}{clear_effect} = yes")
    for line in key_setup_lines:
        lines.append(f"{T}{line}")
    lines.append(f"{T}if = {{")
    lines.append(f"{T}{T}limit = {{")
    lines.append(f"{T}{T}{T}has_local_variable = {local_key}")
    lines.append(f"{T}{T}{T}has_global_variable_map = {required_map}")
    lines.append(f"{T}{T}{T}is_key_in_global_variable_map = {{ name = {required_map} target = local_var:{local_key} }}")
    lines.append(f"{T}{T}}}")
    for map_name, variable in cache_maps:
        lines.append(f"{T}{T}set_variable = {{ name = {variable} value = \"global_variable_map({map_name}|local_var:{local_key})\" }}")
    lines.append(f"{T}}}")
    lines.append(f"{T}remove_local_variable = {local_key}")
    lines.append("}")
    lines.append("")


def append_refresh_country_cache(lines: list[str]) -> None:
    lines.extend(["tv_wonder_index_refresh_country_cache_effect = {", "\tif = { limit = { tv_wonder_has_locked_wonder_trigger = yes } tv_wonder_index_cache_locked_wonder_attributes_effect = { wonder_id = var:tv_wonder_locked } }", "\telse = { tv_wonder_index_clear_locked_wonder_cache_effect = yes }", "\ttv_wonder_mechanics_refresh_current_suitability_display_cache_effect = yes", "}", ""])


def append_rebuild_global_maps(lines: list[str], wonders: list[dict], mechanics: dict, source_data: dict) -> None:
    by_key = {wonder["key"]: wonder for wonder in wonders}
    size_progress = {size: int(record["progress"]) for size, record in source_data["sizes"].items()}
    all_map_names = [*WONDER_MAP_NAMES, *SUITABILITY_ROW_MAP_NAMES]
    first_wonder = wonders[0]
    building_map_defaults = [
        ("tv_wonder_id_to_helper_building_type", f"building_type:tv_wonder_{first_wonder['key']}"),
        *[
            (module_building_type_map_name(part), f"building_type:tv_wonder_{first_wonder['key']}_{part}")
            for part in PARTS
        ],
        ("tv_wonder_id_to_final_building_type", f"building_type:{first_wonder['final_building']}"),
    ]

    lines.append("tv_wonder_index_rebuild_global_maps_effect = {")
    lines.append(f"{T}# ID contract: existing wonder ids are canonical. Runtime map keys use numeric ids directly.")
    lines.append(f"{T}# Ritual branch id = wonder_id * 100 + style.")
    lines.append(f"{T}# Tooltip-safe module/final building maps key each fixed part/style directly by wonder_id.")
    lines.append(f"{T}# Event option tooltips can render dynamic local_var building types, but not same-chain computed map keys.")
    lines.append(f"{T}# Suitability row id = mechanic_id * 10 + row, because unique wonders share mechanic rows.")
    lines.append(f"{T}# Location display maps use building_type/location scopes directly and avoid numeric sentinel scope keys.")
    for map_name in all_map_names:
        lines.extend(map_init_lines(map_name))
    for map_name, default_value in building_map_defaults:
        lines.extend(map_init_lines(map_name, value=default_value))

    for wonder in wonders:
        wonder_id = int(wonder["id"])
        key = str(wonder_id)
        base_id = int(by_key[wonder["base_key"]]["id"])
        mechanic_id = int(by_key[wonder["mechanic_key"]]["id"])
        size = wonder["size"]
        if size not in WONDER_SIZE_IDS:
            raise ValueError(f"Unsupported wonder size for {wonder['key']}: {size}")
        lines.extend(map_replace_line("tv_wonder_id_to_is_unique", key, 1 if wonder.get("is_unique") else 0))
        lines.extend(map_replace_line("tv_wonder_id_to_base_id", key, base_id))
        lines.extend(map_replace_line("tv_wonder_id_to_mechanic_id", key, mechanic_id))
        lines.extend(map_replace_line("tv_wonder_id_to_size", key, WONDER_SIZE_IDS[size]))
        lines.extend(map_replace_line("tv_wonder_id_to_style_count", key, len(ritual_style_ids(wonder))))
        lines.extend(map_replace_line("tv_wonder_id_to_display_id", key, wonder_id))
        lines.extend(map_replace_line("tv_wonder_id_to_concept_display_id", key, wonder_id))
        lines.extend(map_replace_line("tv_wonder_id_to_image_display_id", key, wonder_id))
        lines.extend(map_replace_line("tv_wonder_id_to_required_progress", key, size_progress[wonder["size"]]))
        helper_building = f"building_type:tv_wonder_{wonder['key']}"
        lines.extend(map_replace_line("tv_wonder_id_to_helper_building_type", key, helper_building))
        lines.extend(map_replace_line(INTERMEDIATE_BUILDING_WONDER_ID_MAP, helper_building, wonder_id))

        for part in PARTS:
            module_building = f"building_type:tv_wonder_{wonder['key']}_{part}"
            lines.extend(map_replace_line(module_building_type_map_name(part), key, module_building))
            lines.extend(map_replace_line(INTERMEDIATE_BUILDING_WONDER_ID_MAP, module_building, wonder_id))

        final_ref = f"building_type:{wonder['final_building']}"
        lines.extend(map_replace_line("tv_wonder_id_to_final_building_type", key, final_ref))
        lines.extend(map_replace_line(FINAL_BUILDING_WONDER_ID_MAP, final_ref, wonder_id))

        if wonder.get("is_unique"):
            location_key = wonder.get("location")
            if location_key:
                final_building = f"building_type:{wonder['final_building']}"
                lines.extend(map_replace_line(UNIQUE_WONDER_LOCATION_MAP, key, f"location:{location_key}"))
                lines.extend(
                    map_replace_line(
                        UNIQUE_WONDER_FINAL_BUILDING_TYPE_MAP,
                        key,
                        final_building,
                    )
                )

    for wonder in wonders:
        if wonder.get("is_unique"):
            continue
        mechanic_id = int(wonder["id"])
        rows = suitability_knowledge_for_wonder(mechanics, wonder)
        lines.extend(map_replace_line("tv_wonder_mechanic_id_to_suitability_row_count", str(mechanic_id), len(rows)))
        for row_index in range(1, SUITABILITY_KNOWLEDGE_ROW_SLOTS + 1):
            if row_index > 9:
                raise ValueError(f"Suitability row key only reserves row 1..9: {wonder['key']} row {row_index}")
            row_key = f"flag:{suitability_row_key(mechanic_id, row_index)}"
            if row_index <= len(rows):
                row = rows[row_index - 1]
                condition_id = suitability_row_condition_id(row)
                weight = format_weight_literal(suitability_row_weight(row))
            else:
                condition_id = 0
                weight = "0"
            lines.extend(map_replace_line(SUITABILITY_CONDITION_TYPE_MAP, row_key, condition_id))
            lines.extend(map_replace_line(SUITABILITY_WEIGHT_MAP, row_key, weight))

    lines.append("}")
    lines.append("")


def generate() -> str:
    source_data = load_wonders_source_data()
    wonders, mechanics = load_all_wonder_mechanics()
    wonders = sorted(wonders, key=lambda item: int(item["id"]))

    lines = render_header(SCRIPT_REL)
    append_rebuild_global_maps(lines, wonders, mechanics, source_data)
    append_clear_cache_effect(lines, "tv_wonder_index_clear_locked_wonder_cache_effect", WONDER_CACHE_VARS)
    append_cache_effect(
        lines,
        name="tv_wonder_index_cache_locked_wonder_attributes_effect",
        local_key="tv_wonder_index_key",
        clear_effect="tv_wonder_index_clear_locked_wonder_cache_effect",
        key_setup_lines=[
            "remove_local_variable = tv_wonder_index_key",
            "set_local_variable = { name = tv_wonder_index_key value = $wonder_id$ }",
        ],
        cache_maps=WONDER_CACHE_MAPS,
    )
    append_refresh_country_cache(lines)
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUT_FILE.write_text("\ufeff" + generate(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
