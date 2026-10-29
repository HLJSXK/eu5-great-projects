import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.modifiers import (
    authored_final_building_local_modifiers,
    merge_numeric_modifier_mappings,
    scale_numeric_modifier_mapping,
    wonder_base_country_modifiers,
)
from wonder_mechanics.naming import wonder_static_display_modifier_name, wonder_static_local_display_modifier_name
from wonder_mechanics.render import render_header
from wonder_mechanics.rituals import ritual_styles
from in_game.common.building_types.gen_tv_engineering_department_wonder_mechanics_buildings import (
    fmt_value as building_modifier_value,
    merge_modifiers,
    split_modifiers,
)

OUT_FILE = REPO_ROOT / "src" / "in_game" / "common" / "static_modifiers" / "tv_engineering_department_wonder_mechanics_modifiers.txt"
SCRIPT_REL = "scripts_engineering_department/in_game/common/static_modifiers/gen_tv_engineering_department_wonder_mechanics_modifiers.py"
T = "\t"


def fmt_value(value: object) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:.5f}".rstrip("0").rstrip(".")
    return str(value)


def modifier_block(name: str, modifiers: dict, *, category: str | None = None) -> list[str]:
    lines = [f"{name} = {{"]
    if category:
        lines.append(f"{T}game_data = {{ category = {category} }}")
    for key, value in modifiers.items():
        lines.append(f"{T}{key} = {fmt_value(value)}")
    lines.append("}")
    lines.append("")
    return lines


def generate() -> str:
    wonders, mechanics = load_all_wonder_mechanics()
    lines = render_header(SCRIPT_REL)
    for wonder in wonders:
        building_design = mechanics["buildings"][wonder["mechanic_key"]]
        local, raw_local = split_modifiers(merge_modifiers(
            authored_final_building_local_modifiers(wonder, mechanics),
            include_local_cultural_baseline=building_design["include_local_cultural_baseline"],
        ))
        # Match the serialized per-level building values before applying levels;
        # otherwise rounding a small source value can make the preview disagree.
        local = {key: float(building_modifier_value(value))
                 if isinstance(value, (int, float)) and not isinstance(value, bool) else value
                 for key, value in local.items()}
        for level in range(1, 7):
            modifiers = wonder_base_country_modifiers(wonder, mechanics, level)
            lines.extend(modifier_block(wonder_static_display_modifier_name(wonder, level), modifiers))
            local_modifiers = merge_numeric_modifier_mappings(scale_numeric_modifier_mapping(local, level), raw_local)
            # Omit the cultural baseline from display previews only.
            local_modifiers = {key: value for key, value in local_modifiers.items()
                               if key not in {"local_cultural_tradition", "local_cultural_influence"}}
            lines.extend(modifier_block(wonder_static_local_display_modifier_name(wonder, level), local_modifiers, category="location"))
        for row in ritual_styles(wonder, mechanics):
            for name, values, category in ((row["modifier"], row["country_modifier"], "country"), (row["location_modifier"], row["location_modifier_values"], "location")):
                if name:
                    lines.extend([f"{name} = {{", f"\tgame_data = {{ category = {category} }}", *[f"\t{k} = {fmt_value(v)}" for k,v in values.items()], "}", ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUT_FILE.write_text(generate(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
