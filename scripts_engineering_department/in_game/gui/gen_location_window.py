import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.render import render_header
from wonder_mechanics.naming import WONDER_SIZE_IDS
from wonder_identity import image_expression

GLORP_LOCATION_WINDOW_FILE = REPO_ROOT / ".eu5-base" / "reference_mods" / "3601047146" / "in_game" / "gui" / "location_window.gui"
GLORP_SHARED_TYPES_FILE = REPO_ROOT / ".eu5-base" / "reference_mods" / "3601047146" / "in_game" / "gui" / "glorpUI_shared_types.gui"
GLORP_VANILLA_TYPES_FILE = (
    REPO_ROOT
    / ".eu5-base" / "reference_mods" / "3601047146"
    / "in_game"
    / "gui"
    / "vanilla"
    / "cmfg_location_window_vanilla_types.gui"
)
OUT_FILE = REPO_ROOT / "src" / "in_game" / "gui" / "location_window.gui"
WIDGETS_FILE = REPO_ROOT / "src/in_game/gui/tv_location_wonder_widgets.gui"
CM_GUI_SOURCE = REPO_ROOT / ".eu5-base/reference_mods/3601047146/in_game/common/scripted_guis/glorpui_construction_manager_scripted_gui.txt"
CM_GUI_OUTPUT = REPO_ROOT / "src/in_game/common/scripted_guis/glorpui_construction_manager_scripted_gui.txt"
SITE_CONDITIONS_GUI_OUTPUT = REPO_ROOT / "src/in_game/common/scripted_guis/tv_wonder_location_site_conditions.txt"
SCRIPT_REL = "scripts_engineering_department/in_game/gui/gen_location_window.py"
DATA_REL = (
    "data/unique_wonders.yaml + "
    ".eu5-base/reference_mods/3601047146/in_game/gui/location_window.gui + "
    ".eu5-base/reference_mods/3601047146/in_game/gui/glorpUI_shared_types.gui + "
    ".eu5-base/reference_mods/3601047146/in_game/gui/vanilla/cmfg_location_window_vanilla_types.gui"
)
T = "\t"
UI_SCALE = 0.75


def scale_gui_layout(gui: str) -> str:
    """Emit smaller pixel bounds/fonts for our widgets, leaving bindings intact.

    Quoted strings and comments are consumed unchanged before matching layout
    properties. This must never scale wonder ids, levels, colors or expressions.
    Percentage dimensions and the -1 auto-size sentinel retain their meaning.
    """
    pattern = re.compile(
        r'"(?:\\.|[^"\\])*"|\#[^\n]*|'
        r'\b(?P<property>size|minimumsize|maximumsize|position|margin(?:_left|_right|_top|_bottom)?|'
        r'spacing|max_width|min_width|fontsize(?:_min)?)'
        r'(?P<equals>\s*=\s*)'
        r'(?P<value>\{\s*-?\d+(?:\.\d+)?%?(?:\s+-?\d+(?:\.\d+)?%?)*\s*\}|-?\d+(?:\.\d+)?)'
    )

    def replace(match: re.Match) -> str:
        prop = match['property']
        if prop is None:
            return match[0]

        def number(token: re.Match) -> str:
            value = token[0]
            if value.endswith('%') or (value == '-1' and prop in ('size', 'minimumsize', 'maximumsize')):
                return value
            scaled = float(value) * UI_SCALE
            if prop.startswith('fontsize'):
                scaled = max(1, int(scaled))
            return f'{scaled:g}'

        value = re.sub(r'-?\d+(?:\.\d+)?%?', number, match['value'])
        return prop + match['equals'] + value

    return pattern.sub(replace, gui)

OVERFLOW_VAR = "LocationView.GetLocation.MakeScope.GetVariable('tv_wonder_tooltip_overflow_count')"
LOCATION_SCOPE = "LocationView.GetLocation.MakeScope.Self"
DISPLAY_CONCEPT_PREFIX = "tv_wonder_display_"
IMAGE_CONCEPT_PREFIX = "tv_wonder_display_image_"
FULL_IMAGE_CONCEPT_PREFIX = "tv_wonder_display_full_image_"
TOOLTIP_SLOT_MAX = 5
# A separate button beside the vanilla queue keeps foreign wonders inspectable.
MENU_OPEN_VAR = "tv_location_wonders_open"
# Native header (40), content top margin (5), province row (45), location row (73).
# This is in native panel units, not the gallery's UI_SCALE.
MENU_TOP = 40 + 5 + 45 + 73
MENU_MAX_HEIGHT = 820
CARD_SPACING = 4
RITUAL_HEADER_HEIGHT = 48
RITUAL_GROUP_WIDTH = 224
MENU_WIDTH = 300 + CARD_SPACING + RITUAL_GROUP_WIDTH
PANEL_TEXT_HEIGHT = 24
PANEL_TEXT_FONT_SIZE = 18
PANEL_TEXT_MARGIN_X = 5
PANEL_TEXT_MARGIN_Y = 3
TOOLTIP_IMAGE_WIDTH = 300
TOOLTIP_IMAGE_HEIGHT = 200
TOOLTIP_IMAGE_OVERLAY_HEIGHT = 32
SIZE_BADGE_SIZE = 26
TOOLTIP_IMAGE_NAME_WIDTH = 205 - SIZE_BADGE_SIZE - 4
# 48 displayed pixels at UI_SCALE, matching the medallion asset design range.
LEVEL_MEDALLION_SIZE = 64


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


def fixed_point_to_int_string(var_expr: str) -> str:
    return f"ToString_int32(FixedPointToInt({var_expr}.GetValue))"


def slot_id_string(slot_type: str, slot: int) -> str:
    return fixed_point_to_int_string(slot_id_var(slot_type, slot))


def slot_level_string(slot_type: str, slot: int) -> str:
    return fixed_point_to_int_string(slot_level_var(slot_type, slot))


def slot_display_concept_expr(slot_type: str, slot: int) -> str:
    return f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', {slot_id_string(slot_type, slot)})"


def var_enabled_expr(var_expr: str) -> str:
    return f"Not(EqualTo_CFixedPoint({var_expr}.GetValue, '(CFixedPoint)0.0'))"


def slot_has_id_expr(slot_type: str, slot: int) -> str:
    return f"{slot_id_var(slot_type, slot)}.IsSet"


def slot_building_type_expr(slot_type: str, slot: int) -> str:
    # The existing index stores building_type scopes, so promote the map value
    # directly. No per-wonder localization adapter or raw-key recovery is needed.
    return (
        "GetVariableFromGlobalVariableMap('tv_wonder_id_to_final_building_type', "
        f"MakeScopeValue({slot_id_var(slot_type, slot)}.GetValue)).GetBuildingType"
    )


def slot_name_expr(slot_type: str, slot: int) -> str:
    return f"{slot_building_type_expr(slot_type, slot)}.GetName"


def slot_size_value_expr(slot: int) -> str:
    return (
        "GetVariableFromGlobalVariableMap('tv_wonder_id_to_size', "
        f"MakeScopeValue({slot_id_var('tooltip', slot)}.GetValue)).GetValue"
    )


def slot_size_visible_expr(slot: int, size: str) -> str:
    return f"EqualTo_CFixedPoint({slot_size_value_expr(slot)}, '(CFixedPoint){WONDER_SIZE_IDS[size]}.0')"


def render_size_icons(slot: int, *, title: bool = False) -> str:
    bounds = 'using = tooltip_title_icon_size' if title else f'size = {{ {SIZE_BADGE_SIZE} {SIZE_BADGE_SIZE} }}'
    return '\n'.join(f'''icon = {{
        name = "tv_location_wonder_size_{'title' if title else 'icon'}_{slot}_{size}"
        {bounds} alwaystransparent = yes
        visible = "[{slot_size_visible_expr(slot, size)}]"
        texture = "gfx/interface/icons/location_icons/tv_project_size_{size}.dds"
    }}''' for size in WONDER_SIZE_IDS)


def render_size_badge(slot: int) -> str:
    # Keep the existing concept link inside the single sentence. A second
    # header subtitle would repeat the size and add an unwanted text line.
    descriptions = '\n'.join(f'''TooltipTextBlock = {{
        name = "tv_location_wonder_size_description_{slot}_{size}"
        visible = "[{slot_size_visible_expr(slot, size)}]"
        blockoverride "text" {{ text = "TV_LOCATION_WONDER_SIZE_{size.upper()}" }}
    }}''' for size in WONDER_SIZE_IDS)
    return f'''widget = {{
        name = "tv_location_wonder_size_{slot}"
        size = {{ {SIZE_BADGE_SIZE} {SIZE_BADGE_SIZE} }}
        alwaystransparent = no
        {render_size_icons(slot)}
        tooltipwidget = {{
            ContextualTooltipType = {{
                blockoverride "title_icon" {{ {render_size_icons(slot, title=True)} }}
                blockoverride "title_text" {{ text = "TV_LOCATION_WONDER_SIZE" }}
                blockoverride "concept_link" {{ visible = no }}
                blockoverride "tooltip_content" {{ {descriptions} }}
            }}
        }}
    }}'''


def slot_image_expr(slot_type: str, slot: int) -> str:
    return image_expression(None, f"{slot_id_var(slot_type, slot)}.GetValue", f"Concatenate('{IMAGE_CONCEPT_PREFIX}', {slot_id_string(slot_type, slot)})", cropped=True)


def slot_full_image_expr(slot_type: str, slot: int) -> str:
    return image_expression(None, f"{slot_id_var(slot_type, slot)}.GetValue", f"Concatenate('{FULL_IMAGE_CONCEPT_PREFIX}', {slot_id_string(slot_type, slot)})")


def slot_modifier_level_string(slot_type: str, slot: int) -> str:
    # No level-0 modifier exists. Keep even an eagerly evaluated hidden table's
    # reference valid; the unbuilt/shell tooltip displays only the no-effect text.
    return f"ToString_int32(FixedPointToInt(Max_CFixedPoint({slot_level_var(slot_type, slot)}.GetValue, '(CFixedPoint)1.0')))"


def slot_modifier_key_expr(slot_type: str, slot: int) -> str:
    level_expr = slot_modifier_level_string(slot_type, slot)
    return (
        f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', "
        f"Concatenate({slot_id_string(slot_type, slot)}, Concatenate('_level_', {level_expr})))"
    )


def slot_local_modifier_key_expr(slot_type: str, slot: int) -> str:
    level_expr = slot_modifier_level_string(slot_type, slot)
    return (
        f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', "
        f"Concatenate({slot_id_string(slot_type, slot)}, Concatenate('_local_level_', {level_expr})))"
    )


def slot_base_site_rules_trigger_key_expr(slot_type: str, slot: int) -> str:
    return (
        f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', "
        f"Concatenate({slot_id_string(slot_type, slot)}, '_base_site_rules_trigger'))"
    )


def slot_site_rules_met_expr(slot: int) -> str:
    # Use the established ScriptedGui predicate API with an explicit location
    # root. The bridge only calls the requirements trigger; it never writes state.
    key = f"Concatenate('{DISPLAY_CONCEPT_PREFIX}', Concatenate({slot_id_string('tooltip', slot)}, '_site_conditions'))"
    return f"GetScriptedGui({key}).IsShown(GuiScope.SetRoot(LocationView.GetLocation.MakeScope).End)"


def render_tooltip_image_overlay(indent: str, *, slot: int) -> list[str]:
    level_var = slot_level_var("tooltip", slot)
    return [
        f"{indent}widget = {{",
        f"{indent}{T}alwaystransparent = yes",
        f"{indent}{T}size = {{ 100% {TOOLTIP_IMAGE_OVERLAY_HEIGHT} }}",
        f"{indent}{T}parentanchor = top",
        f"{indent}{T}widgetanchor = top",
        f"{indent}{T}using = bg_text_mask_container_dark_blue",
        f"{indent}{T}hbox = {{",
        f"{indent}{T}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}{T}layoutpolicy_vertical = fixed",
        f"{indent}{T}{T}margin = {{ {PANEL_TEXT_MARGIN_X} {PANEL_TEXT_MARGIN_Y} }}",
        f"{indent}{T}{T}spacing = 4",
        render_size_badge(slot),
        f"{indent}{T}{T}text_single = {{",
        f'{indent}{T}{T}{T}name = "tv_location_wonder_name_{slot}"',
        f"{indent}{T}{T}{T}alwaystransparent = no",
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
        f"{indent}{T}{T}{T}alwaystransparent = yes",
        f'{indent}{T}{T}{T}text = "TV_LOCATION_WONDER_LEVEL_SHORT"',
        f"{indent}{T}{T}{T}align = right|nobaseline",
        f"{indent}{T}{T}{T}fontsize = {PANEL_TEXT_FONT_SIZE}",
        f"{indent}{T}{T}}}",
        f"{indent}{T}{T}text_single = {{",
        f"{indent}{T}{T}{T}alwaystransparent = yes",
        f'{indent}{T}{T}{T}text = "[{level_var}.GetValue|0]"',
        f"{indent}{T}{T}{T}align = right|nobaseline",
        f"{indent}{T}{T}{T}fontsize = {PANEL_TEXT_FONT_SIZE}",
        f"{indent}{T}{T}}}",
        f"{indent}{T}}}",
        f"{indent}}}",
    ]


def render_overflow_line(indent: str) -> list[str]:
    visible = var_enabled_expr(OVERFLOW_VAR)
    return [
        f"{indent}hbox = {{",
        f'{indent}{T}visible = "[{visible}]"',
        f"{indent}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}layoutpolicy_vertical = fixed",
        f"{indent}{T}size = {{ {MENU_WIDTH} 20 }}",
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


def slot_localization_expr(slot: int, suffix: str = "") -> str:
    return f"Localize(Concatenate('game_concept_', Concatenate({slot_display_concept_expr('tooltip', slot)}, '{suffix}')))"


def slot_ritual_modifiers_expr(slot: int, style: int, scope: str) -> str:
    return f"Localize(Concatenate('TV_WONDER_RITUAL_{scope}_MODIFIERS_{style}_', {slot_id_string('tooltip', slot)}))"


def render_art_tooltip(slot: int) -> str:
    building_type = slot_building_type_expr('tooltip', slot)
    trigger_key = slot_base_site_rules_trigger_key_expr('tooltip', slot)
    conditions = f'''TooltipRequirementsList = {{
        name = "tv_wonder_conditions_section"
        blockoverride "block_title" {{ text = "TV_LOCATION_WONDER_CONDITIONS" }}
        blockoverride "requirementslist_datamodel_is_empty" {{ visible = no }}
        textcontext = "[ShowTriggerConditionsForScope({trigger_key},{LOCATION_SCOPE})]"
    }}'''
    icons = '''icon = { using = tooltip_title_icon_size texture = "[GetConceptTexture('tv_wonder_construction')]" }'''
    return native_wonder_tooltip(f'[{building_type}.GetNameWithNoTooltip]', '[tv_wonder_construction|e]',
        icons, conditions, f'[{building_type}.GetFlavorText]')


def slot_current_effects_expr(slot: int) -> str:
    return (
        f"And(GreaterThan_CFixedPoint({slot_level_var('tooltip', slot)}.GetValue, '(CFixedPoint)0.0'), "
        f"Not(EqualTo_CFixedPoint({slot_ritual_style_var('tooltip', slot)}.GetValue, '(CFixedPoint)-1.0')))"
    )


def native_effect_rows(name: str, effects: str, *, title_key: str | None = None) -> str:
    # One shared native section frame; its country/local rows stack vertically.
    # Let the native table's GetRows/GetFooter visibility handle empty output.
    # IsUTF8StringNotEmpty fails on these CString producers in the game.
    title = 'visible = no' if title_key is None else f'''visible = "[Or(DataModelHasItems(StringPairList.GetRows), DataModelHasItems(StringPairList.GetFooter))]"
            text = "{title_key}"'''
    return f'''TooltipStringPairList = {{
        name = "{name}"
        margin = {{ 0 0 }}
        blockoverride "bg_listbase" {{}}
        blockoverride "block_title" {{ {title} }}
        blockoverride "stringpair_datamodel_is_empty" {{ visible = no }}
        textcontext = "[{effects}]"
    }}'''


def native_wonder_tooltip(title: str, subtitle: str, icons: str, section: str, history: str) -> str:
    # Same composition as ProductionMethod_tooltip / timed_modifier_tooltip.
    # Inherit native header, row typography and delayed flavor treatment.
    return f'''tooltipwidget = {{
        ContextualTooltipType = {{
            blockoverride "title_icon" {{ {icons} }}
            blockoverride "title_text" {{ text = "{title}" }}
            blockoverride "concept_link" {{ text = "{subtitle}" }}
            blockoverride "tooltip_content" {{
                {section}
                TooltipFlavorTextBlock = {{
                    name = "tv_wonder_history_section"
                    blockoverride "text" {{ text = "{history}" }}
                }}
            }}
        }}
    }}'''


def render_level_tooltip(slot: int) -> str:
    active = slot_current_effects_expr(slot)
    rows = '\n'.join(native_effect_rows(f'tv_location_wonder_level_modifiers_{slot}_{scope}',
        f"ShowModifierEffect({getter('tooltip', slot)})",
        title_key=f'TV_LOCATION_WONDER_RITUAL_{scope.upper()}_GAINS')
        for scope, getter in (('country', slot_modifier_key_expr), ('local', slot_local_modifier_key_expr)))
    effects = f'''vbox = {{ visible = "[{active}]" layoutpolicy_horizontal = expanding ignoreinvisible = yes
        {rows}
    }}
    TooltipTextBlock = {{ visible = "[Not({active})]"
        blockoverride "bg_listbase" {{}}
        blockoverride "text" {{ text = "TV_LOCATION_WONDER_NO_EFFECT" }}
    }}'''
    icons = '\n'.join(f'''icon = {{ using = tooltip_title_icon_size
        visible = "[EqualTo_CFixedPoint({slot_level_var('tooltip', slot)}.GetValue, '(CFixedPoint){level}.0')]"
        texture = "gfx/interface/icons/location_icons/tv_wonder_level_{level}.dds"
    }}''' for level in range(7))
    building = slot_building_type_expr('tooltip', slot)
    subtitle = f"[Localize('TV_LOCATION_WONDER_LEVEL_SHORT')] [{slot_level_var('tooltip', slot)}.GetValue|0]"
    section = f'TooltipListBase = {{ name = "tv_wonder_effects_section" {effects} }}'
    return native_wonder_tooltip(f'[{building}.GetNameWithNoTooltip]', subtitle, icons,
                                 section, f'[{building}.GetFlavorText]')


def slot_ritual_active_expr(slot: int, style: int) -> str:
    # Lifecycle reset keeps the numeric style defined for every slot. Positive
    # styles are projected only from implemented rituals; 0/-1 never highlight.
    return f"EqualTo_CFixedPoint({slot_ritual_style_var('tooltip', slot)}.GetValue, '(CFixedPoint){style}.0')"


def slot_ritual_completion_expr(slot: int, style: int) -> str:
    return f"Localize(Concatenate('TV_WONDER_RITUAL_COMPLETION_{style}_', {slot_id_string('tooltip', slot)}))"


def render_ritual_tooltip(slot: int, style: int) -> str:
    active = slot_ritual_active_expr(slot, style)
    effects = '\n'.join(native_effect_rows(f'tv_location_wonder_ritual_modifiers_{slot}_{style}_{scope.lower()}',
        slot_ritual_modifiers_expr(slot, style, scope),
        title_key=f'TV_LOCATION_WONDER_RITUAL_{scope}_GAINS') for scope in ('COUNTRY', 'LOCAL'))
    # Scripted-effect descriptions are native effect/condition lines, not
    # modifier name/value pairs. Match action_tooltip_inner_content in vanilla
    # cooltip_types.gui, including its empty-list gate and native row styling.
    effects += f'''\nTooltipConditionList = {{
        name = "tv_location_wonder_ritual_completion_{slot}_{style}"
        datacontext = "[StringToConditionListOnlyPassedAndNeutral({slot_ritual_completion_expr(slot, style)})]"
        visible = "[ConditionList.HasItems]"
        margin = {{ 0 0 }}
        blockoverride "bg_listbase" {{}}
        blockoverride "block_title" {{
            text = "TV_LOCATION_WONDER_RITUAL_COMPLETION"
        }}
    }}'''
    icons = '''icon = { using = tooltip_title_icon_size texture = "[GetConceptTexture('tv_wonder_ceremony')]" }'''
    subtitle = (f"[{slot_building_type_expr('tooltip', slot)}.GetNameWithNoTooltip] · "
                f"[SelectLocalization({active}, 'TV_LOCATION_WONDER_RITUAL_ACTIVE', 'TV_LOCATION_WONDER_RITUAL_HEADER')]")
    section = f'TooltipListBase = {{ name = "tv_wonder_effects_section" {effects} }}'
    return native_wonder_tooltip(f"[{slot_localization_expr(slot, f'_ritual_{style}')}]", subtitle,
        icons, section, f"[{slot_localization_expr(slot, f'_ritual_{style}_desc')}]")


def render_menu_slot(indent: str, *, slot: int) -> list[str]:
    lines = [f'''hbox = {{
        name = "tv_location_wonder_entry_{slot}"
        visible = "[{slot_has_id_expr('tooltip', slot)}]"
        layoutpolicy_horizontal = fixed
        layoutpolicy_vertical = fixed
        size = {{ {MENU_WIDTH} {TOOLTIP_IMAGE_HEIGHT} }}
        spacing = {CARD_SPACING}
        widget = {{
            name = "tv_location_wonder_art_{slot}"
            size = {{ {TOOLTIP_IMAGE_WIDTH} {TOOLTIP_IMAGE_HEIGHT} }}
            alwaystransparent = no
            background = {{ texture = "[{slot_full_image_expr('tooltip', slot)}]" fittype = fill }}
            {render_art_tooltip(slot)}''']
    # The building name keeps its native link; decorative parts pass hover to the art.
    overlay = "\n".join(render_tooltip_image_overlay("", slot=slot))
    lines += [overlay, f'''widget = {{
            name = "tv_location_wonder_site_conditions_{slot}"
            parentanchor = bottom|left widgetanchor = bottom|left position = {{ -2 2 }}
            size = {{ {LEVEL_MEDALLION_SIZE} {LEVEL_MEDALLION_SIZE} }} alwaystransparent = no
            {render_art_tooltip(slot)}
            widget = {{
                parentanchor = center widgetanchor = center size = {{ 35.2 35.2 }}
                alwaystransparent = yes using = bg_circle_piechart
                icon = {{
                    name = "tv_location_wonder_site_conditions_yes_{slot}"
                    parentanchor = center widgetanchor = center size = {{ 25.6 25.6 }}
                    alwaystransparent = yes
                    visible = "[{slot_site_rules_met_expr(slot)}]"
                    texture = "gfx/interface/icons/text_icons/trigger_yes.dds"
                }}
                icon = {{
                    name = "tv_location_wonder_site_conditions_no_{slot}"
                    parentanchor = center widgetanchor = center size = {{ 25.6 25.6 }}
                    alwaystransparent = yes
                    visible = "[Not({slot_site_rules_met_expr(slot)})]"
                    texture = "gfx/interface/icons/text_icons/trigger_no.dds"
                }}
            }}
        }}
        widget = {{
            name = "tv_location_wonder_level_{slot}"
            visible = "[{slot_has_id_expr('tooltip', slot)}]"
            parentanchor = bottom|right widgetanchor = bottom|right position = {{ 2 2 }}
            size = {{ {LEVEL_MEDALLION_SIZE} {LEVEL_MEDALLION_SIZE} }} alwaystransparent = no
            {render_level_tooltip(slot)}''']
    # Static texture handles are required by the engine. This remains one hover
    # target; exactly one of the seven transparent medallion sprites is visible.
    # icon/ubericon uses its explicit square size; it does not support fittype.
    for level in range(7):
        lines.append(f'''icon = {{
            name = "tv_location_wonder_medallion_{slot}_{level}"
            visible = "[EqualTo_CFixedPoint({slot_level_var('tooltip', slot)}.GetValue, '(CFixedPoint){level}.0')]"
            size = {{ {LEVEL_MEDALLION_SIZE} {LEVEL_MEDALLION_SIZE} }} alwaystransparent = yes
            texture = "gfx/interface/icons/location_icons/tv_wonder_level_{level}.dds"
        }}''')
    lines.append('}')
    ritual_height = (TOOLTIP_IMAGE_HEIGHT - RITUAL_HEADER_HEIGHT - 3 * CARD_SPACING) / 3
    lines += ['}', f'''vbox = {{
        name = "tv_location_wonder_ritual_group_{slot}"
        size = {{ {RITUAL_GROUP_WIDTH} {TOOLTIP_IMAGE_HEIGHT} }}
        layoutpolicy_horizontal = fixed layoutpolicy_vertical = fixed spacing = {CARD_SPACING}
        widget = {{
            name = "tv_location_wonder_ritual_header_{slot}"
            size = {{ {RITUAL_GROUP_WIDTH} {RITUAL_HEADER_HEIGHT} }} alwaystransparent = no
            using = bg_card_header_01_production
            using = bg_cabinet_card_frame
            text_single = {{ size = {{ {RITUAL_GROUP_WIDTH} {RITUAL_HEADER_HEIGHT} }}
                autoresize = no align = center|nobaseline using = Font_Type_Headers fontsize = 20
                text = "TV_LOCATION_WONDER_RITUAL_HEADER" alwaystransparent = yes }}
            button_regular = {{
                name = "tv_location_wonder_reritual_{slot}"
                parentanchor = right|vcenter widgetanchor = right|vcenter position = {{ -6 0 }}
                size = {{ 32 32 }}
                visible = "[LocationView.GetLocation.GetOwner.IsPlayer]"
                enabled = "[PdxGuiWidget.IsUberButtonEnabled]"
                scripted_action_tooltip = {{
                    click_type = left click_mode = single
                    action_name = "tv_wonder_location_reritual_{slot}"
                    actor = "[LocationView.GetPlayer]"
                    parameter = {{ parameter_name = "target" parameter_value = "[LocationView.GetLocation]" }}
                }}
                button_tooltip_override = {{ title = "tv_wonder_location_reritual_{slot}" description = "tv_wonder_location_reritual_{slot}_desc" }}
                tooltipwidget = {{ using = action_tooltip_pop_out }}
                icon = {{ parentanchor = center size = {{ 24 24 }}
                    texture = "gfx/interface/icons/location_icons/tv_wonder_arrow_restart.dds" alwaystransparent = yes }}
            }}
        }}
        ''']
    for style in (1, 2, 3):
        active = slot_ritual_active_expr(slot, style)
        lines.append(f'''widget = {{
            name = "tv_location_wonder_ritual_{slot}_{style}"
            size = {{ {RITUAL_GROUP_WIDTH} {ritual_height} }} alwaystransparent = no
            using = bg_cabinet_card_frame
            background = {{ using = color_black_texture alpha = 0.6 }}
            widget = {{ visible = "[{active}]" size = {{ {RITUAL_GROUP_WIDTH} {ritual_height} }}
                alwaystransparent = yes background = {{ using = color_yellow_texture alpha = 0.28 }} }}
            widget = {{ visible = "[{active}]" size = {{ 3 {ritual_height} }}
                alwaystransparent = yes background = {{ using = color_yellow_texture }} }}
            text_single = {{ position = {{ 8 0 }} size = {{ {RITUAL_GROUP_WIDTH - 38} {ritual_height} }}
                autoresize = no align = left|nobaseline fontsize = 18
                raw_text = "[{slot_localization_expr(slot, f'_ritual_{style}')}]" alwaystransparent = yes }}
            text_single = {{ visible = "[{active}]" position = {{ {RITUAL_GROUP_WIDTH - 30} {(ritual_height - 24) / 2} }} size = {{ 26 24 }}
                raw_text = "@trigger_yes!" alwaystransparent = yes align = center|nobaseline }}
            {render_ritual_tooltip(slot, style)}
        }}''')
    lines.extend(['}', '}'])
    return [indent + line for line in "\n".join(lines).splitlines()]


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
    ]
    for slot in range(1, TOOLTIP_SLOT_MAX + 1):
        lines.extend(render_menu_slot(T * 3, slot=slot))
    lines.extend(render_overflow_line(T * 3))
    lines.extend([f"{T}{T}}}", f"{T}}}", "}", ""])
    return scale_gui_layout("\n".join(lines))


def render_wonder_button_type() -> str:
    indent = T
    opened = f"LocationView.Vars.Exists('{MENU_OPEN_VAR}')"
    label = f"SelectLocalization({opened}, 'TV_LOCATION_WONDER_CLOSE_DETAILS', 'TV_LOCATION_WONDER_OPEN_DETAILS')"
    return scale_gui_layout("\n".join([
        f"{indent}type tv_location_wonders_button = header_button_left {{",
        f'{indent}{T}name = "tv_location_wonders_button"',
        f'{indent}{T}datacontext = "[LocationView.GetLocation]"',
        f'{indent}{T}visible = "[{slot_has_id_expr("tooltip", 1)}]"',
        f"{indent}{T}size = {{ 144 40 }}",
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
        f'{indent}{T}{T}on_action = "[LocationView.Vars.Toggle(\'{MENU_OPEN_VAR}\')]"',
        f"{indent}{T}}}",
        f"{indent}{T}tooltipwidget = {{ BasicFunctionalTooltip = {{}} }}",
        f"{indent}{T}hbox = {{",
        f"{indent}{T}{T}layoutpolicy_horizontal = expanding",
        f"{indent}{T}{T}margin = {{ 8 0 }}",
        f"{indent}{T}{T}spacing = 4",
        f'{indent}{T}{T}text_single = {{ layoutpolicy_horizontal = expanding autoresize = no align = center|nobaseline fontsize = 18 text = "[{label}]" }}',
        f'{indent}{T}{T}icon = {{ visible = "[Not({opened})]" size = {{ 24 24 }} texture = "gfx/interface/icons/location_icons/tv_wonder_arrow_right.dds" }}',
        f'{indent}{T}{T}icon = {{ visible = "[{opened}]" size = {{ 24 24 }} texture = "gfx/interface/icons/location_icons/tv_wonder_arrow_left.dds" }}',
        f"{indent}{T}}}",
        f"{indent}}}",
    ]))


def render_wonder_panel_type() -> str:
    return "\n".join([
        f"{T}type tv_location_wonders_panel = tv_location_wonders_menu {{",
        f'{T}{T}name = "tv_location_wonders_panel"',
        f"{T}{T}parentanchor = top|right",
        f"{T}{T}widgetanchor = top|left",
        f"{T}{T}position = {{ 0 {MENU_TOP} }}",
        f"{T}{T}allow_outside = yes",
        f'{T}{T}visible = "[And(LocationView.Vars.Exists(\'{MENU_OPEN_VAR}\'), {slot_has_id_expr("tooltip", 1)})]"',
        f"{T}}}",
    ])


def generate_widgets() -> str:
    lines = render_header(SCRIPT_REL, "data/unique_wonders.yaml")
    lines.extend([
        "# Public location-window integration: see docs/guides/Location_GUI_Integration.md.",
        "# Templates belong at file scope, outside the types groups.",
        "template tv_location_wonders_close_on_queue {",
        f'{T}on_action = "[LocationView.Vars.Clear(\'{MENU_OPEN_VAR}\')]"',
        "}",
        render_wonder_menu_types(),
        "types tv_location_wonder_widgets {",
        render_wonder_button_type(),
        render_wonder_panel_type(),
        "}",
    ])
    return "\n".join(line.rstrip() for line in "\n".join(lines).splitlines()).rstrip() + "\n"


def render_scene_overlay() -> str:
    return f"{T * 4}tv_location_wonders_button = {{}}"


def inject_sol_button(gui: str) -> str:
    # SOL owns this optional type, its assets and tooltip. Do not copy its body
    # or make the generator depend on another project's checkout.
    anchor = re.compile(
        r'(?m)^\s*expand = \{\}\s*\n\s*subheader_unified_icon = \{\s*\n'
        r'\s*visible = "\[HasPopBreakdownIntelOn\(Location\.Self\)\]"'
    )
    matches = list(anchor.finditer(gui))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one SOL button insertion point, found {len(matches)}")
    offset = matches[0].start()
    return gui[:offset] + f'\n{T * 7}sol_location_living_standard_button = {{}}\n' + gui[offset:]


def inject_wonder_panel(gui: str) -> str:
    # Keep the gallery directly under the lateralview: nesting it outside the
    # scene's bounds broke all gallery hovers in game despite allow_outside.
    # Name the scene for alignment checks without changing its input hierarchy.
    scene_marker = '\n\t\t\t# SCENE\n\t\t\twidget = {'
    if gui.count(scene_marker) != 1:
        raise RuntimeError("Could not find city appearance for wonder panel")
    gui = gui.replace(scene_marker, scene_marker + f'\n{T * 4}name = "tv_location_city_appearance"', 1)
    marker = '\n\twidgetid = "location_window"'
    if gui.count(marker) != 1:
        raise RuntimeError("Could not find location window root for wonder panel")
    panel = f"\n{T}tv_location_wonders_panel = {{}}\n"
    gui = gui.replace(marker, marker + panel, 1)
    # Opening either side panel closes the other, matching the wonder button.
    gui, count = re.subn(
        r'(?m)^(\s*)on_action = "(\[LocationView\.OpenConstructionQueue\([^\n]+)"',
        lambda match: (
            f'{match[1]}using = tv_location_wonders_close_on_queue\n'
            f'{match[1]}on_action = "{match[2]}"'
        ), gui,
    )
    if count == 0 and "LocationView.OpenConstructionQueue(" in gui:
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
    lines.append(glorp_vanilla_types)
    lines.append(inject_overlay(inject_sol_button(glorp_location_window)))
    return "\n".join(line.rstrip() for line in "\n".join(lines).splitlines()).rstrip() + "\n"


def generate_site_condition_guis() -> str:
    from wonder_mechanics.io import load_all_wonder_mechanics

    wonders, _ = load_all_wonder_mechanics()
    lines = render_header(SCRIPT_REL)
    lines.append("# Read-only predicates, evaluated by the visible location gallery.")
    for wonder in wonders:
        lines.extend([
            f"tv_wonder_display_{wonder['id']}_site_conditions = {{",
            "\tscope = location",
            f"\tis_shown = {{ tv_wonder_display_{wonder['id']}_base_site_rules_trigger = yes }}",
            "\teffect = { }",
            "}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(generate(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")
    WIDGETS_FILE.write_text(generate_widgets(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {WIDGETS_FILE.relative_to(REPO_ROOT)}")
    CM_GUI_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cm_header = render_header(SCRIPT_REL, CM_GUI_SOURCE.relative_to(REPO_ROOT).as_posix())
    CM_GUI_OUTPUT.write_text("\n".join(cm_header) + "\n" + CM_GUI_SOURCE.read_text(encoding="utf-8-sig"), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {CM_GUI_OUTPUT.relative_to(REPO_ROOT)}")
    SITE_CONDITIONS_GUI_OUTPUT.write_text(generate_site_condition_guis(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {SITE_CONDITIONS_GUI_OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
