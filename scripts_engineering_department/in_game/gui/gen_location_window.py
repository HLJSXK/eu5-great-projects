import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.render import render_header
from wonder_identity import image_expression

GLORP_LOCATION_WINDOW_FILE = REPO_ROOT / ".eu5-base" / "reference_mods_variants" / "eu5-towards-victory" / "3812518640" / "in_game" / "gui" / "location_window.gui"
GLORP_SHARED_TYPES_FILE = REPO_ROOT / ".eu5-base" / "reference_mods_variants" / "eu5-towards-victory" / "3812518640" / "in_game" / "gui" / "glorpUI_shared_types.gui"
GLORP_VANILLA_TYPES_FILE = (
    REPO_ROOT
    / ".eu5-base" / "reference_mods_variants" / "eu5-towards-victory"
    / "3812518640"
    / "in_game"
    / "gui"
    / "vanilla"
    / "cmfg_location_window_vanilla_types.gui"
)
OUT_FILE = REPO_ROOT / "src" / "in_game" / "gui" / "location_window.gui"
CM_GUI_SOURCE = REPO_ROOT / ".eu5-base/reference_mods_variants/eu5-towards-victory/3812518640/in_game/common/scripted_guis/glorpui_construction_manager_scripted_gui.txt"
CM_GUI_OUTPUT = REPO_ROOT / "src/in_game/common/scripted_guis/glorpui_construction_manager_scripted_gui.txt"
SCRIPT_REL = "scripts_engineering_department/in_game/gui/gen_location_window.py"
DATA_REL = (
    "data/unique_wonders.yaml + "
    ".eu5-base/reference_mods_variants/eu5-towards-victory/3812518640/in_game/gui/location_window.gui + "
    ".eu5-base/reference_mods_variants/eu5-towards-victory/3812518640/in_game/gui/glorpUI_shared_types.gui + "
    ".eu5-base/reference_mods_variants/eu5-towards-victory/3812518640/in_game/gui/vanilla/cmfg_location_window_vanilla_types.gui"
)
T = "\t"

OVERFLOW_VAR = "LocationView.GetLocation.MakeScope.GetVariable('tv_wonder_tooltip_overflow_count')"
LOCATION_SCOPE = "LocationView.GetLocation.MakeScope.Self"
DISPLAY_CONCEPT_PREFIX = "tv_wonder_display_"
IMAGE_CONCEPT_PREFIX = "tv_wonder_display_image_"
FULL_IMAGE_CONCEPT_PREFIX = "tv_wonder_display_full_image_"
TOOLTIP_SLOT_MAX = 5
# A separate button beside the vanilla queue keeps foreign wonders inspectable.
MENU_SELECTION_VAR = "tv_location_wonder_detail"
MENU_OPEN_VAR = "tv_location_wonders_open"
MENU_MAX_HEIGHT = 650
PANEL_TEXT_HEIGHT = 14
PANEL_TEXT_FONT_SIZE = 14
PANEL_TEXT_MARGIN_X = 5
PANEL_TEXT_MARGIN_Y = 3
TOOLTIP_EFFECT_COLUMN_WIDTH = 462
TOOLTIP_IMAGE_WIDTH = 300
TOOLTIP_IMAGE_HEIGHT = 200
TOOLTIP_IMAGE_OVERLAY_HEIGHT = 24
TOOLTIP_IMAGE_NAME_WIDTH = 205
TOOLTIP_EFFECT_MARGIN_X = 8
TOOLTIP_MODIFIER_COLUMN_SPACING = 8
# Match Engineering Department suitability columns: 444 = 218 + 8 + 218.
TOOLTIP_MODIFIER_COLUMNS_WIDTH = TOOLTIP_EFFECT_COLUMN_WIDTH - TOOLTIP_EFFECT_MARGIN_X * 2 - 2
TOOLTIP_MODIFIER_COLUMN_WIDTH = (TOOLTIP_MODIFIER_COLUMNS_WIDTH - TOOLTIP_MODIFIER_COLUMN_SPACING) // 2


def extract_top_level_block(text: str, start_marker: str) -> str:
    start = text.find(start_marker)
    if start == -1:
        raise RuntimeError(f"Could not find {start_marker!r} in Glorp UI shared types")
    depth = 0
    for index, char in enumerate(text[start:], start=start):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1].rstrip()
    raise RuntimeError(f"Could not find matching closing brace for {start_marker!r}")


def render_glorp_shared_types() -> str:
    glorp_shared_types = GLORP_SHARED_TYPES_FILE.read_text(encoding="utf-8-sig")
    # Import only the shared Glorp type that location_window.gui actually uses.
    shared = extract_top_level_block(glorp_shared_types, "types glorp_shared_types {")
    # Glorp's old snapshot carries this removed 1.3 input property on the
    # shared zoom button; do not copy it into an active EU5 1.4 target.
    return shared.replace("\n        use_global_input_instance = yes", "")


def location_var(name: str) -> str:
    return f"LocationView.GetLocation.MakeScope.GetVariable('{name}')"


def compact_slot_var(slot: int, suffix: str) -> str:
    return location_var(f"tv_wonder_display_slot_{slot}_{suffix}")


def tooltip_slot_var(slot: int, suffix: str) -> str:
    return location_var(f"tv_wonder_tooltip_slot_{slot}_{suffix}")


def slot_id_var(slot_type: str, slot: int) -> str:
    return compact_slot_var(slot, "id") if slot_type == "compact" else tooltip_slot_var(slot, "id")


def slot_level_var(slot_type: str, slot: int) -> str:
    return compact_slot_var(slot, "level") if slot_type == "compact" else tooltip_slot_var(slot, "level")


def slot_ritual_style_var(slot_type: str, slot: int) -> str:
    return compact_slot_var(slot, "ritual_style") if slot_type == "compact" else tooltip_slot_var(slot, "ritual_style")


def slot_ritual_completed_var(slot_type: str, slot: int) -> str:
    return compact_slot_var(slot, "ritual_completed") if slot_type == "compact" else tooltip_slot_var(slot, "ritual_completed")


def fixed_point_to_int_string(var_expr: str) -> str:
    return f"ToString_int32(FixedPointToInt({var_expr}.GetValue))"


def slot_id_string(slot_type: str, slot: int) -> str:
    return fixed_point_to_int_string(slot_id_var(slot_type, slot))


def slot_level_string(slot_type: str, slot: int) -> str:
    return fixed_point_to_int_string(slot_level_var(slot_type, slot))


def slot_ritual_style_string(slot_type: str, slot: int) -> str:
    return fixed_point_to_int_string(slot_ritual_style_var(slot_type, slot))


def slot_display_concept_expr(slot_type: str, slot: int) -> str:
    return f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', {slot_id_string(slot_type, slot)})"


def var_enabled_expr(var_expr: str) -> str:
    return f"And({var_expr}.IsSet, Not(EqualTo_CFixedPoint({var_expr}.GetValue, '(CFixedPoint)0.0')))"


def slot_has_id_expr(slot_type: str, slot: int) -> str:
    return f"{slot_id_var(slot_type, slot)}.IsSet"


def slot_has_payload_expr(slot_type: str, slot: int) -> str:
    return (
        f"And({slot_id_var(slot_type, slot)}.IsSet, "
        f"And({slot_level_var(slot_type, slot)}.IsSet, "
        f"And({slot_ritual_style_var(slot_type, slot)}.IsSet, {slot_ritual_completed_var(slot_type, slot)}.IsSet)))"
    )


def slot_level_is_expr(slot_type: str, slot: int, level: int) -> str:
    level_var = slot_level_var(slot_type, slot)
    return f"And({level_var}.IsSet, EqualTo_CFixedPoint({level_var}.GetValue, '(CFixedPoint){level}.0'))"


def slot_has_base_effect_payload_expr(slot_type: str, slot: int) -> str:
    return (
        f"And3({slot_has_payload_expr(slot_type, slot)}, "
        f"Not({slot_level_is_expr(slot_type, slot, 0)}), "
        f"Not(EqualTo_CFixedPoint({slot_ritual_style_var(slot_type, slot)}.GetValue, '(CFixedPoint)-1.0')))"
    )


def slot_no_effect_payload_expr(slot_type: str, slot: int) -> str:
    return (
        f"And({slot_has_payload_expr(slot_type, slot)}, "
        f"{slot_level_is_expr(slot_type, slot, 0)})"
    )


def slot_has_ritual_effect_payload_expr(slot_type: str, slot: int) -> str:
    return (
        f"And({slot_has_base_effect_payload_expr(slot_type, slot)}, "
        f"{var_enabled_expr(slot_ritual_completed_var(slot_type, slot))})"
    )


def slot_ritual_no_effect_payload_expr(slot_type: str, slot: int) -> str:
    return (
        f"And({slot_has_base_effect_payload_expr(slot_type, slot)}, "
        f"Not({var_enabled_expr(slot_ritual_completed_var(slot_type, slot))}))"
    )


def slot_name_expr(slot_type: str, slot: int) -> str:
    return f"SelectGameConcept({slot_has_id_expr(slot_type, slot)}, {slot_display_concept_expr(slot_type, slot)}, 'tv_wonder_construction')"


def slot_image_expr(slot_type: str, slot: int) -> str:
    return image_expression(None, f"{slot_id_var(slot_type, slot)}.GetValue", f"Concatenate('{IMAGE_CONCEPT_PREFIX}', {slot_id_string(slot_type, slot)})", cropped=True)


def slot_full_image_expr(slot_type: str, slot: int) -> str:
    return image_expression(None, f"{slot_id_var(slot_type, slot)}.GetValue", f"Concatenate('{FULL_IMAGE_CONCEPT_PREFIX}', {slot_id_string(slot_type, slot)})")


def slot_modifier_key_expr(slot_type: str, slot: int) -> str:
    return (
        f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', "
        f"Concatenate({slot_id_string(slot_type, slot)}, Concatenate('_level_', {slot_level_string(slot_type, slot)})))"
    )


def slot_local_modifier_key_expr(slot_type: str, slot: int) -> str:
    return (
        f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', "
        f"Concatenate({slot_id_string(slot_type, slot)}, Concatenate('_local_level_', {slot_level_string(slot_type, slot)})))"
    )


def slot_ritual_effect_key_expr(slot_type: str, slot: int) -> str:
    return (
        f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', "
        f"Concatenate({slot_id_string(slot_type, slot)}, "
        f"Concatenate('_ritual_', Concatenate({slot_ritual_style_string(slot_type, slot)}, "
        "'_location_tooltip_effect'))))"
    )


def slot_base_site_rules_trigger_key_expr(slot_type: str, slot: int) -> str:
    return (
        f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', "
        f"Concatenate({slot_id_string(slot_type, slot)}, '_base_site_rules_trigger'))"
    )


def render_level_line(indent: str, *, slot_type: str, slot: int) -> list[str]:
    level_var = slot_level_var(slot_type, slot)
    return [
        f"{indent}hbox = {{",
        f"{indent}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}layoutpolicy_vertical = fixed",
        f"{indent}{T}size = {{ -1 18 }}",
        f"{indent}{T}spacing = 4",
        f"{indent}{T}text_single = {{",
        f'{indent}{T}{T}text = "TV_LOCATION_WONDER_LEVEL_SHORT"',
        f"{indent}{T}{T}align = left|nobaseline",
        f"{indent}{T}{T}fontsize = 13",
        f"{indent}{T}}}",
        f"{indent}{T}text_single = {{",
        f'{indent}{T}{T}visible = "[{level_var}.IsSet]"',
        f'{indent}{T}{T}text = "[{level_var}.GetValue|0]"',
        f"{indent}{T}{T}align = left|nobaseline",
        f"{indent}{T}{T}fontsize = 13",
        f"{indent}{T}}}",
        f'{indent}{T}text_single = {{ visible = "[EqualTo_CFixedPoint({slot_ritual_style_var(slot_type, slot)}.GetValue, \'(CFixedPoint)0.0\')]" text = "TV_WONDER_RITUAL_PLAIN_STATE" fontsize = 13 }}',
        f'{indent}{T}text_single = {{ visible = "[EqualTo_CFixedPoint({slot_ritual_style_var(slot_type, slot)}.GetValue, \'(CFixedPoint)-1.0\')]" text = "TV_WONDER_RITUAL_SHELL_STATE" fontsize = 13 }}',
        f'{indent}{T}text_single = {{ visible = "[{var_enabled_expr(slot_ritual_completed_var(slot_type, slot))}]" text = "[Localize(Concatenate(Concatenate(\'game_concept_tv_wonder_display_\', {slot_id_string(slot_type, slot)}), Concatenate(\'_ritual_\', {slot_ritual_style_string(slot_type, slot)})))]" fontsize = 13 }}',
        f"{indent}{T}expand = {{}}",
        f"{indent}}}",
    ]


def render_tooltip_image_overlay(indent: str, *, slot: int) -> list[str]:
    level_var = slot_level_var("tooltip", slot)
    return [
        f"{indent}widget = {{",
        f"{indent}{T}size = {{ 100% {TOOLTIP_IMAGE_OVERLAY_HEIGHT} }}",
        f"{indent}{T}parentanchor = top",
        f"{indent}{T}widgetanchor = top",
        f"{indent}{T}using = bg_text_mask_container_dark_blue",
        f"{indent}{T}hbox = {{",
        f"{indent}{T}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}{T}layoutpolicy_vertical = fixed",
        f"{indent}{T}{T}margin = {{ {PANEL_TEXT_MARGIN_X} {PANEL_TEXT_MARGIN_Y} }}",
        f"{indent}{T}{T}spacing = 4",
        f"{indent}{T}{T}text_single = {{",
        f'{indent}{T}{T}{T}text = "[{slot_name_expr("tooltip", slot)}]"',
        f"{indent}{T}{T}{T}layoutpolicy_horizontal = fixed",
        f"{indent}{T}{T}{T}size = {{ {TOOLTIP_IMAGE_NAME_WIDTH} {PANEL_TEXT_HEIGHT} }}",
        f"{indent}{T}{T}{T}max_width = {TOOLTIP_IMAGE_NAME_WIDTH}",
        f"{indent}{T}{T}{T}align = left|nobaseline",
        f"{indent}{T}{T}{T}autoresize = no",
        f"{indent}{T}{T}{T}fontsize = {PANEL_TEXT_FONT_SIZE}",
        f"{indent}{T}{T}}}",
        f"{indent}{T}{T}expand = {{}}",
        f"{indent}{T}{T}text_single = {{",
        f'{indent}{T}{T}{T}text = "TV_LOCATION_WONDER_LEVEL_SHORT"',
        f"{indent}{T}{T}{T}align = right|nobaseline",
        f"{indent}{T}{T}{T}fontsize = {PANEL_TEXT_FONT_SIZE}",
        f"{indent}{T}{T}}}",
        f"{indent}{T}{T}text_single = {{",
        f'{indent}{T}{T}{T}visible = "[{level_var}.IsSet]"',
        f'{indent}{T}{T}{T}text = "[{level_var}.GetValue|0]"',
        f"{indent}{T}{T}{T}align = right|nobaseline",
        f"{indent}{T}{T}{T}fontsize = {PANEL_TEXT_FONT_SIZE}",
        f"{indent}{T}{T}}}",
        f"{indent}{T}}}",
        f"{indent}}}",
    ]


def render_tooltip_full_image(indent: str, *, slot: int) -> list[str]:
    visible = slot_has_id_expr("tooltip", slot)
    lines = [
        f"{indent}widget = {{",
        f'{indent}{T}visible = "[{visible}]"',
        f"{indent}{T}layoutpolicy_horizontal = fixed",
        f"{indent}{T}layoutpolicy_vertical = fixed",
        f"{indent}{T}size = {{ {TOOLTIP_IMAGE_WIDTH} {TOOLTIP_IMAGE_HEIGHT} }}",
        f"{indent}{T}using = bg_cabinet_card_frame",
        f"{indent}{T}background = {{",
        f'{indent}{T}{T}texture = "[{slot_full_image_expr("tooltip", slot)}]"',
        f"{indent}{T}{T}fittype = fill",
        f"{indent}{T}}}",
    ]
    lines.extend(render_tooltip_image_overlay(indent + T, slot=slot))
    lines.append(f"{indent}}}")
    return lines


def render_modifier_column(
    indent: str,
    *,
    title_key: str,
    modifier_key: str,
    column_width: int,
    font_size: int,
    row_height: int,
    vertical_policy: str,
) -> list[str]:
    return [
        f"{indent}vbox = {{",
        f"{indent}{T}layoutpolicy_horizontal = fixed",
        f"{indent}{T}layoutpolicy_vertical = {vertical_policy}",
        f"{indent}{T}minimumsize = {{ {column_width} -1 }}",
        f"{indent}{T}maximumsize = {{ {column_width} -1 }}",
        f"{indent}{T}spacing = 2",
        f"{indent}{T}text_single = {{",
        f'{indent}{T}{T}text = "{title_key}"',
        f"{indent}{T}{T}max_width = {column_width}",
        f"{indent}{T}{T}align = left|nobaseline",
        f"{indent}{T}{T}fontsize = {font_size}",
        f"{indent}{T}}}",
        f"{indent}{T}TooltipStringPairList = {{",
        f"{indent}{T}{T}layoutpolicy_horizontal = fixed",
        f"{indent}{T}{T}maximumsize = {{ {column_width} -1 }}",
        f'{indent}{T}{T}blockoverride "tooltip_minimumsize" {{ minimumsize = {{ {column_width} -1 }} }}',
        f'{indent}{T}{T}blockoverride "field_text_format" {{',
        f"{indent}{T}{T}{T}fontsize = {font_size}",
        f"{indent}{T}{T}{T}autoresize = yes",
        # Label (left) and value (right) columns share this one column_width budget as two
        # side-by-side TooltipTableColumn/TooltipTableField instances (~30px margin+spacing
        # chrome each, ~60px combined), leaving the value column's own short text its remaining
        # share. 140 confirmed in-game by the user as the widest the label can go without the
        # row overflowing again.
        f"{indent}{T}{T}{T}max_width = 140",
        f"{indent}{T}{T}{T}elide = right",
        f"{indent}{T}{T}}}",
        f'{indent}{T}{T}blockoverride "row_size" {{',
        f"{indent}{T}{T}{T}maximumsize = {{ -1 {row_height} }}",
        f"{indent}{T}{T}{T}minimumsize = {{ -1 {row_height} }}",
        f"{indent}{T}{T}}}",
        f'{indent}{T}{T}textcontext = "[ShowModifierEffect({modifier_key})]"',
        f"{indent}{T}}}",
        f"{indent}{T}expand = {{}}",
        f"{indent}}}",
    ]


def render_tooltip_modifier_column(indent: str, *, title_key: str, modifier_key: str) -> list[str]:
    return render_modifier_column(
        indent,
        title_key=title_key,
        modifier_key=modifier_key,
        column_width=TOOLTIP_MODIFIER_COLUMN_WIDTH,
        font_size=13,
        row_height=22,
        vertical_policy="expanding",
    )


def render_tooltip_construction_conditions_block(indent: str, *, slot: int) -> list[str]:
    visible = slot_has_id_expr("tooltip", slot)
    trigger_key = slot_base_site_rules_trigger_key_expr("tooltip", slot)
    return [
        f"{indent}vbox = {{",
        f'{indent}{T}visible = "[{visible}]"',
        f"{indent}{T}layoutpolicy_horizontal = fixed",
        f"{indent}{T}layoutpolicy_vertical = shrinking",
        f"{indent}{T}minimumsize = {{ {TOOLTIP_MODIFIER_COLUMNS_WIDTH} -1 }}",
        f"{indent}{T}maximumsize = {{ {TOOLTIP_MODIFIER_COLUMNS_WIDTH} -1 }}",
        f"{indent}{T}margin_bottom = 6",
        f"{indent}{T}spacing = 2",
        f"{indent}{T}TooltipRequirementsList = {{",
        f"{indent}{T}{T}layoutpolicy_horizontal = expanding",
        f'{indent}{T}{T}textcontext = "[ShowTriggerConditionsForScope({trigger_key},{LOCATION_SCOPE})]"',
        f'{indent}{T}{T}blockoverride "field_text_format" {{',
        f"{indent}{T}{T}{T}fontsize = 13",
        f"{indent}{T}{T}}}",
        f'{indent}{T}{T}blockoverride "row_size" {{',
        f"{indent}{T}{T}{T}maximumsize = {{ -1 22 }}",
        f"{indent}{T}{T}{T}minimumsize = {{ -1 22 }}",
        f"{indent}{T}{T}}}",
        f'{indent}{T}{T}blockoverride "block_title" {{',
        f'{indent}{T}{T}{T}block "block_title" {{',
        f"{indent}{T}{T}{T}{T}visible = no",
        f"{indent}{T}{T}{T}}}",
        f"{indent}{T}{T}}}",
        f'{indent}{T}{T}blockoverride "requirementslist_datamodel_is_empty" {{',
        f"{indent}{T}{T}{T}visible = no",
        f"{indent}{T}{T}}}",
        f"{indent}{T}}}",
        f"{indent}}}",
    ]


def render_tooltip_effect_block(indent: str, *, slot: int) -> list[str]:
    base_effect_visible = slot_has_base_effect_payload_expr("tooltip", slot)
    ritual_effect_visible = slot_has_ritual_effect_payload_expr("tooltip", slot)
    ritual_no_effect_visible = slot_ritual_no_effect_payload_expr("tooltip", slot)
    no_effect_visible = slot_no_effect_payload_expr("tooltip", slot)
    country_modifier_key = slot_modifier_key_expr("tooltip", slot)
    local_modifier_key = slot_local_modifier_key_expr("tooltip", slot)
    ritual_effect_key = slot_ritual_effect_key_expr("tooltip", slot)
    lines = [
        f"{indent}widget = {{",
        f"{indent}{T}layoutpolicy_horizontal = fixed",
        f"{indent}{T}layoutpolicy_vertical = shrinking",
        f"{indent}{T}size = {{ {TOOLTIP_EFFECT_COLUMN_WIDTH} -1 }}",
        f"{indent}{T}vbox = {{",
        f"{indent}{T}{T}set_parent_size_to_minimum = yes",
        f"{indent}{T}{T}margin_left = 8",
        f"{indent}{T}{T}margin_right = 8",
        f"{indent}{T}{T}margin_bottom = 6",
        f"{indent}{T}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}{T}layoutpolicy_vertical = shrinking",
        f"{indent}{T}{T}spacing = 0",
        f"{indent}{T}{T}ignoreinvisible = yes",
    ]
    lines.extend(render_tooltip_construction_conditions_block(indent + T * 2, slot=slot))
    lines.extend(
        [
            f"{indent}{T}{T}text_multi = {{",
            f'{indent}{T}{T}{T}visible = "[{no_effect_visible}]"',
            f'{indent}{T}{T}{T}text = "TV_LOCATION_WONDER_NO_EFFECT"',
            f"{indent}{T}{T}{T}layoutpolicy_horizontal = expanding",
            f"{indent}{T}{T}{T}autoresize = yes",
            f"{indent}{T}{T}{T}max_width = {TOOLTIP_MODIFIER_COLUMNS_WIDTH}",
            f"{indent}{T}{T}{T}minimumsize = {{ {TOOLTIP_MODIFIER_COLUMNS_WIDTH} -1 }}",
            f"{indent}{T}{T}}}",
            f"{indent}{T}{T}hbox = {{",
            f'{indent}{T}{T}{T}visible = "[{base_effect_visible}]"',
            f"{indent}{T}{T}{T}layoutpolicy_horizontal = fixed",
            f"{indent}{T}{T}{T}layoutpolicy_vertical = shrinking",
            f"{indent}{T}{T}{T}size = {{ {TOOLTIP_MODIFIER_COLUMNS_WIDTH} -1 }}",
            f"{indent}{T}{T}{T}spacing = {TOOLTIP_MODIFIER_COLUMN_SPACING}",
            f"{indent}{T}{T}{T}ignoreinvisible = yes",
        ]
    )
    lines.extend(
        render_tooltip_modifier_column(
            indent + T * 3,
            title_key="TV_LOCATION_WONDER_COUNTRY_MODIFIERS_TITLE",
            modifier_key=country_modifier_key,
        )
    )
    lines.extend(
        render_tooltip_modifier_column(
            indent + T * 3,
            title_key="TV_LOCATION_WONDER_LOCAL_MODIFIERS_TITLE",
            modifier_key=local_modifier_key,
        )
    )
    lines.extend(
        [
            f"{indent}{T}{T}}}",
            f"{indent}{T}{T}hbox = {{",
            f'{indent}{T}{T}{T}visible = "[{base_effect_visible}]"',
            f"{indent}{T}{T}{T}layoutpolicy_horizontal = expanding",
            f"{indent}{T}{T}{T}layoutpolicy_vertical = shrinking",
            f"{indent}{T}{T}{T}margin_top = 6",
            f"{indent}{T}{T}{T}text_single = {{",
            f'{indent}{T}{T}{T}{T}text = "TV_LOCATION_WONDER_RITUAL_TITLE_PREFIX"',
            f"{indent}{T}{T}{T}{T}align = left|nobaseline",
            f"{indent}{T}{T}{T}{T}fontsize = 13",
            f"{indent}{T}{T}{T}}}",
            f"{indent}{T}{T}}}",
            f"{indent}{T}{T}TooltipRequirementsList = {{",
            f'{indent}{T}{T}{T}visible = "[{ritual_effect_visible}]"',
            f"{indent}{T}{T}{T}layoutpolicy_horizontal = expanding",
            f'{indent}{T}{T}{T}textcontext = "[ShowScriptedEffectForScope({ritual_effect_key},{LOCATION_SCOPE})]"',
            f'{indent}{T}{T}{T}blockoverride "field_text_format" {{',
            f"{indent}{T}{T}{T}{T}fontsize = 13",
            f"{indent}{T}{T}{T}}}",
            f'{indent}{T}{T}{T}blockoverride "row_size" {{',
            f"{indent}{T}{T}{T}{T}maximumsize = {{ -1 22 }}",
            f"{indent}{T}{T}{T}{T}minimumsize = {{ -1 22 }}",
            f"{indent}{T}{T}{T}}}",
            f'{indent}{T}{T}{T}blockoverride "block_title" {{',
            f'{indent}{T}{T}{T}{T}block "block_title" {{',
            f"{indent}{T}{T}{T}{T}{T}visible = no",
            f"{indent}{T}{T}{T}{T}}}",
            f"{indent}{T}{T}{T}}}",
            f'{indent}{T}{T}{T}blockoverride "requirementslist_datamodel_is_empty" {{',
            f"{indent}{T}{T}{T}{T}visible = no",
            f"{indent}{T}{T}{T}}}",
            f"{indent}{T}{T}}}",
            f"{indent}{T}{T}text_single = {{",
            f'{indent}{T}{T}{T}visible = "[{ritual_no_effect_visible}]"',
            f'{indent}{T}{T}{T}text = "TV_LOCATION_WONDER_NO_EFFECT"',
            f"{indent}{T}{T}{T}layoutpolicy_horizontal = expanding",
            f"{indent}{T}{T}{T}size = {{ -1 22 }}",
            f"{indent}{T}{T}{T}align = left|nobaseline",
            f"{indent}{T}{T}{T}fontsize = 13",
            f"{indent}{T}{T}}}",
            f"{indent}{T}}}",
            f"{indent}}}",
        ]
    )
    return lines


def render_overflow_line(indent: str) -> list[str]:
    visible = var_enabled_expr(OVERFLOW_VAR)
    return [
        f"{indent}hbox = {{",
        f'{indent}{T}visible = "[{visible}]"',
        f"{indent}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}layoutpolicy_vertical = fixed",
        f"{indent}{T}size = {{ {TOOLTIP_EFFECT_COLUMN_WIDTH} 20 }}",
        f"{indent}{T}margin_left = 8",
        f"{indent}{T}spacing = 4",
        f"{indent}{T}text_single = {{",
        f'{indent}{T}{T}text = "TV_LOCATION_WONDER_OVERFLOW_PREFIX"',
        f"{indent}{T}{T}align = left|nobaseline",
        f"{indent}{T}{T}fontsize = 13",
        f"{indent}{T}}}",
        f"{indent}{T}text_single = {{",
        f'{indent}{T}{T}text = "[{OVERFLOW_VAR}.GetValue|0]"',
        f"{indent}{T}{T}align = left|nobaseline",
        f"{indent}{T}{T}fontsize = 13",
        f"{indent}{T}}}",
        f"{indent}{T}text_single = {{",
        f'{indent}{T}{T}text = "TV_LOCATION_WONDER_OVERFLOW_SUFFIX"',
        f"{indent}{T}{T}align = left|nobaseline",
        f"{indent}{T}{T}fontsize = 13",
        f"{indent}{T}}}",
        f"{indent}}}",
    ]


def menu_slot_selected_expr(slot: int) -> str:
    predicate = "NotExistOrHasValue" if slot == 1 else "HasValue"
    return f"LocationView.Vars.{predicate}('{MENU_SELECTION_VAR}', '{slot}')"


def render_menu_slot(indent: str, *, slot: int) -> list[str]:
    selected = menu_slot_selected_expr(slot)
    lines = [
        f"{indent}vbox = {{",
        f'{indent}{T}name = "tv_location_wonder_entry_{slot}"',
        f'{indent}{T}visible = "[{slot_has_id_expr("tooltip", slot)}]"',
        f"{indent}{T}minimumsize = {{ {TOOLTIP_EFFECT_COLUMN_WIDTH} -1 }}",
        f"{indent}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}spacing = 6",
        f"{indent}{T}card_list_button = {{",
        f"{indent}{T}{T}size = {{ {TOOLTIP_EFFECT_COLUMN_WIDTH} 44 }}",
        f'{indent}{T}{T}down = "[{selected}]"',
        f"{indent}{T}{T}action_tooltip = {{",
        f'{indent}{T}{T}{T}title = "[{slot_name_expr("tooltip", slot)}]"',
        f'{indent}{T}{T}{T}on_action = "[LocationView.Vars.Set(\'{MENU_SELECTION_VAR}\', \'{slot}\')]"',
        f"{indent}{T}{T}}}",
        f"{indent}{T}{T}tooltipwidget = {{ BasicFunctionalTooltip = {{}} }}",
        f"{indent}{T}{T}hbox = {{",
        f"{indent}{T}{T}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}{T}{T}margin = {{ 8 5 }}",
        f"{indent}{T}{T}{T}spacing = 8",
        f"{indent}{T}{T}{T}icon = {{",
        f"{indent}{T}{T}{T}{T}size = {{ 48 32 }}",
        f'{indent}{T}{T}{T}{T}texture = "[{slot_image_expr("tooltip", slot)}]"',
        f"{indent}{T}{T}{T}{T}fittype = centercrop",
        f"{indent}{T}{T}{T}}}",
        f"{indent}{T}{T}{T}text_single = {{",
        f"{indent}{T}{T}{T}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}{T}{T}{T}autoresize = no",
        f"{indent}{T}{T}{T}{T}fontsize = 15",
        f"{indent}{T}{T}{T}{T}align = left|nobaseline",
        f'{indent}{T}{T}{T}{T}text = "[{slot_name_expr("tooltip", slot)}]"',
        f"{indent}{T}{T}{T}}}",
        f'{indent}{T}{T}{T}text_single = {{ text = "TV_LOCATION_WONDER_LEVEL_SHORT" fontsize = 13 }}',
        f'{indent}{T}{T}{T}text_single = {{ raw_text = "[{slot_level_var("tooltip", slot)}.GetValue|0]" fontsize = 13 }}',
        f"{indent}{T}{T}}}",
        f"{indent}{T}}}",
        f"{indent}{T}vbox = {{",
        f'{indent}{T}{T}name = "tv_location_wonder_detail_{slot}"',
        f'{indent}{T}{T}visible = "[{selected}]"',
        f"{indent}{T}{T}minimumsize = {{ {TOOLTIP_EFFECT_COLUMN_WIDTH} -1 }}",
        f"{indent}{T}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}{T}spacing = 6",
        f"{indent}{T}{T}using = bg_paper_card",
        f"{indent}{T}{T}using = bg_cabinet_card_frame",
    ]
    lines.extend(render_tooltip_full_image(indent + T * 2, slot=slot))
    lines.extend(render_level_line(indent + T * 2, slot_type="tooltip", slot=slot))
    lines.extend(render_tooltip_effect_block(indent + T * 2, slot=slot))
    lines.extend([f"{indent}{T}}}", f"{indent}}}"])
    return lines


def render_wonder_menu_types() -> str:
    # ContextMenuBase's scroll layout, with panel audio instead of its
    # ExtraTooltipInfo-dependent sound widget. This is an ordinary child panel.
    frame = """\ttype tv_location_wonders_frame = container {
\t\tusing = bg_context_menu
\t\tusing = snd_UI_panel
\t\talwaystransparent = no
\t\tfilter_mouse = all
\t\tscrollarea = {
\t\t\tscrollbarpolicy_horizontal = always_off
\t\t\tautoresizeviewport = yes
\t\t\tautoresizescrollarea = yes
\t\t\tblock "contextmenu_scroll_maximumsize" {}
\t\t\tviewportwidget = { widget = { scissor = yes } }
\t\t\tscrollbar_vertical = { using = Scrollbar_Vertical }
\t\t\tscrollwidget = {
\t\t\t\twidget = {
\t\t\t\t\tvbox = {
\t\t\t\t\t\tset_parent_size_to_minimum = yes
\t\t\t\t\t\tmargin = { 11 11 }
\t\t\t\t\t\tignoreinvisible = yes
\t\t\t\t\t\tspacing = 6
\t\t\t\t\t\tblock "contextmenu_content" {}
\t\t\t\t\t}
\t\t\t\t}
\t\t\t}
\t\t}
\t\twidget = {
\t\t\tusing = bg_tooltip_frame
\t\t\t# Both frame backgrounds bind tint even when their lock layer is hidden.
\t\t\tblockoverride "tooltip_bg_color" { tintcolor = { 1 1 1 1 } }
\t\t}
\t}"""
    lines = [
        "types tv_location_wonder_menu_types {",
        frame,
        f"{T}type tv_location_wonders_menu = tv_location_wonders_frame {{",
        f'{T}{T}datacontext = "[LocationView.GetLocation]"',
        f'{T}{T}blockoverride "tooltip_text_color" {{ fonttintcolor = {{ 1 1 1 1 }} }}',
        f'{T}{T}blockoverride "contextmenu_scroll_maximumsize" {{ maximumsize = {{ -1 {MENU_MAX_HEIGHT} }} }}',
        f'{T}{T}blockoverride "contextmenu_content" {{',
        f"{T}{T}{T}hbox = {{",
        f"{T}{T}{T}{T}minimumsize = {{ {TOOLTIP_EFFECT_COLUMN_WIDTH} 42 }}",
        f"{T}{T}{T}{T}layoutpolicy_horizontal = expanding",
        f"{T}{T}{T}{T}using = bg_card_header_01_production",
        f"{T}{T}{T}{T}using = bg_cabinet_card_frame",
        f"{T}{T}{T}{T}margin = {{ 8 6 }}",
        f"{T}{T}{T}{T}spacing = 8",
        f'{T}{T}{T}{T}icon = {{ size = {{ 24 24 }} texture = "gfx/interface/icons/location_icons/new/prosperity.dds" }}',
        f'{T}{T}{T}{T}text_single = {{ layoutpolicy_horizontal = expanding using = Font_Type_Headers text = "TV_LOCATION_WONDER_TOOLTIP_TITLE" }}',
        f"{T}{T}{T}{T}widget = {{",
        f"{T}{T}{T}{T}{T}size = {{ 25 25 }}",
        f"{T}{T}{T}{T}{T}button_close_alt = {{",
        f'{T}{T}{T}{T}{T}{T}blockoverride "close_on_action" {{ on_action = "[LocationView.Vars.Clear(\'{MENU_OPEN_VAR}\')]" }}',
        f"{T}{T}{T}{T}{T}}}",
        f"{T}{T}{T}{T}}}",
        f"{T}{T}{T}}}",
    ]
    for slot in range(1, TOOLTIP_SLOT_MAX + 1):
        lines.extend(render_menu_slot(T * 3, slot=slot))
    lines.extend(render_overflow_line(T * 3))
    lines.extend([f"{T}{T}}}", f"{T}}}", "}", ""])
    return "\n".join(lines)


def render_scene_overlay() -> str:
    indent = T * 4
    opened = f"LocationView.Vars.Exists('{MENU_OPEN_VAR}')"
    label = f"SelectLocalization({opened}, 'TV_LOCATION_WONDER_CLOSE_DETAILS', 'TV_LOCATION_WONDER_OPEN_DETAILS')"
    return "\n".join([
        f"{indent}header_button_left = {{",
        f'{indent}{T}name = "tv_location_wonders_button"',
        f'{indent}{T}datacontext = "[LocationView.GetLocation]"',
        f'{indent}{T}visible = "[{slot_has_id_expr("tooltip", 1)}]"',
        f"{indent}{T}size = {{ 170 34 }}",
        f"{indent}{T}parentanchor = top|right",
        f"{indent}{T}widgetanchor = top|right",
        f"{indent}{T}position = {{ -8 8 }}",
        f'{indent}{T}down = "[{opened}]"',
        f'{indent}{T}blockoverride "header_button_full_content" {{}}',
        f"{indent}{T}action_tooltip = {{",
        f"{indent}{T}{T}click_type = left",
        f"{indent}{T}{T}click_mode = single",
        f'{indent}{T}{T}title = "[{label}]"',
        f'{indent}{T}{T}on_action = "[LocationView.CloseBuildingQueueMenu]"',
        f'{indent}{T}{T}on_action = "[LocationView.Vars.Clear(\'{MENU_SELECTION_VAR}\')]"',
        f'{indent}{T}{T}on_action = "[LocationView.Vars.Toggle(\'{MENU_OPEN_VAR}\')]"',
        f"{indent}{T}}}",
        f"{indent}{T}tooltipwidget = {{ BasicFunctionalTooltip = {{}} }}",
        f"{indent}{T}hbox = {{",
        f"{indent}{T}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}{T}margin = {{ 10 0 }}",
        f"{indent}{T}{T}spacing = 6",
        f'{indent}{T}{T}text_single = {{ layoutpolicy_horizontal = expanding autoresize = no align = center|nobaseline fontsize = 15 text = "[{label}]" }}',
        f'{indent}{T}{T}icon = {{ visible = "[Not({opened})]" size = {{ 24 24 }} texture = "gfx/interface/icons/location_icons/tv_wonder_arrow_right.dds" }}',
        f'{indent}{T}{T}icon = {{ visible = "[{opened}]" size = {{ 24 24 }} texture = "gfx/interface/icons/location_icons/tv_wonder_arrow_left.dds" }}',
        f"{indent}{T}}}",
        f"{indent}}}",
    ])


def inject_wonder_panel(gui: str) -> str:
    # Anchor to the whole lateral view, not the inset scene or its button.
    marker = '\n\twidgetid = "location_window"'
    if gui.count(marker) != 1:
        raise RuntimeError("Could not find location window root for wonder panel")
    panel = "\n".join([
        "", f"{T}tv_location_wonders_menu = {{",
        f'{T}{T}name = "tv_location_wonders_panel"',
        f"{T}{T}parentanchor = top|right",
        f"{T}{T}widgetanchor = top|left",
        f"{T}{T}position = {{ 0 0 }}",
        f"{T}{T}allow_outside = yes",
        f'{T}{T}visible = "[And(LocationView.Vars.Exists(\'{MENU_OPEN_VAR}\'), {slot_has_id_expr("tooltip", 1)})]"',
        f"{T}}}", "",
    ])
    gui = gui.replace(marker, marker + panel, 1)
    # Opening either side panel closes the other, matching the wonder button.
    gui, count = re.subn(
        r'(?m)^(\s*)on_action = "(\[LocationView\.OpenConstructionQueue\([^\n]+)"',
        lambda match: (
            f'{match[1]}on_action = "[LocationView.Vars.Clear(\'{MENU_OPEN_VAR}\')]"\n'
            f'{match[1]}on_action = "{match[2]}"'
        ), gui,
    )
    if count == 0:
        raise RuntimeError("Could not find native construction queue actions")
    return gui


def inject_overlay(vanilla: str) -> str:
    marker = "\n\t\t\t\tvbox = {\n\t\t\t\t\texpand = {}\n"
    replacement = "\n" + render_scene_overlay() + marker
    if vanilla.count(marker) != 1:
        raise RuntimeError("Could not find location scene overlay insertion point in Glorp UI location_window.gui")
    return inject_wonder_panel(vanilla.replace(marker, replacement, 1))


def generate() -> str:
    glorp_vanilla_types = GLORP_VANILLA_TYPES_FILE.read_text(encoding="utf-8-sig")
    glorp_location_window = GLORP_LOCATION_WINDOW_FILE.read_text(encoding="utf-8-sig")
    lines = render_header(SCRIPT_REL, DATA_REL)
    lines.append(render_glorp_shared_types())
    lines.append(render_wonder_menu_types())
    lines.append(glorp_vanilla_types)
    lines.append(inject_overlay(glorp_location_window))
    return "\n".join(line.rstrip() for line in "\n".join(lines).splitlines()).rstrip() + "\n"


def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(generate(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")
    CM_GUI_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cm_header = render_header(SCRIPT_REL, CM_GUI_SOURCE.relative_to(REPO_ROOT).as_posix())
    CM_GUI_OUTPUT.write_text("\n".join(cm_header) + "\n" + CM_GUI_SOURCE.read_text(encoding="utf-8-sig"), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {CM_GUI_OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
