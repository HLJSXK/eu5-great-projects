import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from wonder_mechanics.io import load_all_wonder_mechanics_data
from wonder_identity import image_expression
from wonder_mechanics.render import render_header
from wonder_mechanics.schema import (
    suitability_current_actual_variable,
    suitability_current_revealed_variable,
)

OUT_FILE = REPO_ROOT / "data" / "generated_fragments" / "tv_engineering_department_wonder_mechanics.gui"
SCRIPT_REL = "scripts_engineering_department/in_game/gui/panels/organization/gen_tv_engineering_department_wonder_mechanics_gui.py"
T = "\t"
PLAYER = "InternationalOrganizationsView.GetPlayer.MakeScope"
PLAYER_SCOPE = f"{PLAYER}.Self"
SUITABILITY_KNOWLEDGE_ROW_SLOTS = 5
SUITABILITY_KNOWLEDGE_COLUMNS_WIDTH = 444
SUITABILITY_KNOWLEDGE_COLUMN_WIDTH = 218
SUITABILITY_KNOWLEDGE_COLUMN_SPACING = 8
SUITABILITY_ROW_LABEL_MAX_WIDTH = 168
SUITABILITY_ROW_HIDDEN_MAX_WIDTH = 214
SUITABILITY_LOCATION_CONDITION_ROW_HEIGHT = 22
PREVIEW_TOP_CARD_HEIGHT = 32
PREVIEW_PANEL_WIDTH = 470
PREVIEW_IMAGE_HEIGHT = 333
PREVIEW_CONTENT_WIDTH = 454
PREVIEW_MODIFIER_COLUMNS_WIDTH = 454
PREVIEW_MODIFIER_COLUMN_WIDTH = 223
PREVIEW_MODIFIER_COLUMN_SPACING = 8
# TooltipTableColumn's field_text (main_menu_cooltip_types.gui) has no built-in width cap;
# long English modifier effect text overflows past the fixed-width StringPairList column
# unless field_text_format bounds it explicitly. The label (left) and value (right) columns
# share this one column_width budget as two side-by-side TooltipTableColumn/TooltipTableField
# instances, each with its own margin={10,0} + spacing=5 (2 gaps) chrome = ~30px per column,
# ~60px for both, leaving the value column's own short text (e.g. "+15.0%") its remaining
# share. 140 confirmed in-game by the user as the widest the label can go without the row
# overflowing again.
PREVIEW_MODIFIER_TEXT_MAX_WIDTH = 140
RITUAL_PROGRESS_MONTHS_VAR = "tv_wonder_ritual_months_completed"
RITUAL_PROGRESS_PCT_VAR = "tv_wonder_ritual_progress_pct"
RITUAL_PROGRESS_MAX_MONTHS = 12
LOCKED_NAME_CARD_HEIGHT = 50
LOCKED_NAME_CARD_TEXT_Y_OFFSET = -4
PROPOSAL_SIZE_ROW_HEIGHT = 24
PROPOSAL_SIZE_ROW_SPACING = 4
PROPOSAL_PREVIEW_HEIGHT = PROPOSAL_SIZE_ROW_HEIGHT + PROPOSAL_SIZE_ROW_SPACING + PREVIEW_IMAGE_HEIGHT
LOCKED_PREVIEW_HEIGHT = (
    LOCKED_NAME_CARD_HEIGHT
    + PROPOSAL_SIZE_ROW_SPACING
    + PROPOSAL_SIZE_ROW_HEIGHT
    + PROPOSAL_SIZE_ROW_SPACING
    + PREVIEW_IMAGE_HEIGHT
)
PROPOSAL_SIZE_INACTIVE_ALPHA = 0.18
PROPOSAL_SIZE_ACTIVE_ALPHA = 1.0
PROPOSAL_SIZE_INDICATORS = [
    ("small", "TV_ENGINEERING_WONDER_SIZE_SMALL_LABEL", "color_market_green_texture", "color_market_green_texture"),
    ("medium", "TV_ENGINEERING_WONDER_SIZE_MEDIUM_LABEL", "color_yellow_texture", "color_yellow_texture"),
    ("large", "TV_ENGINEERING_WONDER_SIZE_LARGE_LABEL", "color_mid_red_texture", "color_red_texture"),
]


def var_is_set(var: str) -> str:
    return f"{player_var(var)}.IsSet"


def reveal_progress_visible(var: str, row_index: int) -> str:
    return (
        f"And({PLAYER}.GetVariable('{var}').IsSet, "
        f"GreaterThanOrEqualTo_CFixedPoint({PLAYER}.GetVariable('{var}').GetValue, '(CFixedPoint){row_index}.0'))"
    )


def fold_bool(op: str, terms: list[str]) -> str:
    if not terms:
        return "False" if op == "Or" else "True"
    if len(terms) == 1:
        return terms[0]
    expr = f"{op}({terms[0]}, {terms[1]})"
    for term in terms[2:]:
        expr = f"{op}({expr}, {term})"
    return expr


def fixed_point_to_int_string(var_expr: str) -> str:
    return f"ToString_int32(FixedPointToInt({var_expr}.GetValue))"


def player_var(var_name: str) -> str:
    return f"{PLAYER}.GetVariable('{var_name}')"


def concept_in_progress() -> str:
    return f"{player_var('tv_wonder_concept_in_progress')}.IsSet"


def dynamic_localized_text_key(prefix: str, var_name: str) -> str:
    return f"Localize(Concatenate('{prefix}', {fixed_point_to_int_string(player_var(var_name))}))"


def dynamic_localized_text_key_from_accessor(prefix: str, accessor: str) -> str:
    return f"Localize(Concatenate('{prefix}', {fixed_point_to_int_string(accessor)}))"


def dynamic_image_texture(var_name: str) -> str:
    return image_expression(None, f"{player_var(var_name)}.GetValue", f"Concatenate('tv_wonder_display_full_image_', {fixed_point_to_int_string(player_var(var_name))})")


def dynamic_display_modifier_key(var_name: str, suffix: str) -> str:
    id_string = fixed_point_to_int_string(player_var(var_name))
    return f"Concatenate('tv_wonder_display_', Concatenate({id_string}, '{suffix}'))"


def dynamic_locked_wonder_concept_link() -> str:
    display_var = player_var("tv_wonder_locked_display_id")
    id_string = fixed_point_to_int_string(display_var)
    return (
        f"[SelectGameConcept({display_var}.IsSet, "
        f"Concatenate('tv_wonder_display_', {id_string}), 'tv_wonder_construction')]"
    )


def proposal_slot_var(slot: int) -> str:
    return f"{PLAYER}.GetVariable('tv_wonder_proposal_slot_{slot}')"


def action_button_fields(
    text: str,
    title: str,
    description: str,
    action_name: str,
) -> str:
    return (
        f'text = "{text}" '
        f'enabled = "[PdxGuiWidget.IsUberButtonEnabled]" '
        f'scripted_action_tooltip = {{ click_type = left click_mode = single '
        f'action_name = "{action_name}" actor = "[InternationalOrganizationsView.GetPlayer]" }} '
        f'button_tooltip_override = {{ title = "{title}" description = "{description}" }} '
        f'tooltipwidget = {{ using = action_tooltip_pop_out }}'
    )


def green_action_button(
    visible: str,
    size: str,
    text: str,
    title: str,
    description: str,
    action_name: str,
) -> str:
    return (
        f'{T}button_regular = {{ visible = "[{visible}]" size = {{ {size} }} '
        f'using = button_regular_texture_alt_green '
        f'using = button_common_textobj_template fontsize = 13 '
        f'{action_button_fields(text, title, description, action_name)} }}'
    )


def proposal_button(slot: int) -> str:
    slot_var = proposal_slot_var(slot)
    slot_id_string = fixed_point_to_int_string(slot_var)
    text = f"[SelectGameConcept({slot_var}.IsSet, Concatenate('tv_wonder_display_', {slot_id_string}), 'tv_wonder_construction')]"
    selected_visible = fold_bool(
        "And",
        [
            f"{slot_var}.IsSet",
            f"{player_var('tv_wonder_proposal')}.IsSet",
            f"Not({concept_in_progress()})",
            (
                f"EqualTo_CFixedPoint({player_var('tv_wonder_proposal')}.GetValue, "
                f"{slot_var}.GetValue)"
            ),
        ],
    )
    title = f"tv_wonder_select_proposal_slot_{slot}"
    description = f"tv_wonder_select_proposal_slot_{slot}_desc"
    action_name = f"tv_wonder_select_proposal_slot_{slot}"
    return "\n".join(
        [
            f"widget = {{",
            f'{T}visible = "[And({slot_var}.IsSet, Not({concept_in_progress()}))]"',
            f"{T}size = {{ 152 30 }}",
            f"{T}button_regular_diamond = {{ size = {{ 152 30 }} {action_button_fields(text, title, description, action_name)} }}",
            green_action_button(selected_visible, "152 30", text, title, description, action_name),
            f"}}",
        ]
    )


def dynamic_proposal_text(prefix: str, max_width: int = 352) -> str:
    return (
        f'{T}text_multi = {{ visible = "[And({player_var("tv_wonder_proposal")}.IsSet, Not({concept_in_progress()}))]" '
        f'max_width = {max_width} autoresize = yes text = "[{dynamic_localized_text_key(prefix, "tv_wonder_proposal")}]" '
        f'align = nobaseline|left }}'
    )


def priority_candidates_visible() -> str:
    return fold_bool(
        "And",
        [
            var_is_set("tv_wonder_priority_found"),
            f"Not({var_is_set('tv_wonder_locked')})",
            f"Not({concept_in_progress()})",
        ],
    )


def priority_candidate_row(*, expansion: bool) -> str:
    # Registry keys and action target_1 are numeric script values. Scope.Self has
    # an unregistered return type; MakeScopeValue explicitly supplies a Scope.
    candidate_key = "MakeScopeValue(Scope.GetValue)"
    selection_scope = f"GuiScope.SetRoot({PLAYER}).AddScope('target_1', {candidate_key}).End"
    selection_gui = "GetScriptedGui('tv_wonder_select_priority_candidate')"

    def candidate_value(map_name: str) -> str:
        return f"{PLAYER}.GetVariableFromVariableMap('tv_wonder_priority_{map_name}', {candidate_key})"

    location = f"{candidate_value('candidate_site_by_id')}.GetLocation"
    display_id = candidate_value("candidate_wonder_by_id")
    id_string = fixed_point_to_int_string(display_id)
    candidate_image = image_expression(None, f"{display_id}.GetValue", f"Concatenate('tv_wonder_display_full_image_', {id_string})")
    selected = (
        f"And({var_is_set('tv_wonder_priority_selected_candidate_id')}, "
        f"EqualTo_CFixedPoint(Scope.GetValue, {player_var('tv_wonder_priority_selected_candidate_id')}.GetValue))"
    )
    lines = [
        "widget = {",
        f"{T}size = {{ 470 52 }}",
        f"{T}using = bg_text_mask_container_dark_blue",
        f'{T}widget = {{ visible = "[{selected}]" size = {{ 100% 100% }} background = {{ using = color_market_green_texture alpha = 0.35 }} }}',
        f'{T}widget = {{ visible = "[{selected}]" size = {{ 4 100% }} background = {{ using = color_market_green_texture alpha = 1.0 }} }}',
        f'{T}widget = {{ position = {{ 10 6 }} size = {{ 64 40 }} background = {{ texture = "[{candidate_image}]" fittype = centercrop }} }}',
        f'{T}text_single = {{ position = {{ 84 6 }} size = {{ 180 22 }} autoresize = no text = "[SelectGameConcept({display_id}.IsSet, Concatenate(\'tv_wonder_display_\', {id_string}), \'tv_wonder_construction\')]" fontsize = 15 align = nobaseline|left }}',
        f'{T}text_single = {{ position = {{ 84 28 }} size = {{ 180 18 }} autoresize = no raw_text = "#weak [{location}.GetName]#!" fontsize = 12 align = nobaseline|left }}',
    ]
    if expansion:
        lines.extend([
            f'{T}text_single = {{ parentanchor = right position = {{ -10 6 }} size = {{ 172 22 }} autoresize = no text = "TV_ENGINEERING_PRIORITY_LEVEL" fontsize = 14 align = nobaseline|right }}',
            f"{T}progressbar = {{",
            f"{T}{T}parentanchor = right position = {{ -10 32 }} size = {{ 172 10 }}",
            f"{T}{T}using = progress_bar_green_alt",
            f'{T}{T}max = "[{candidate_value("display_cap")}.GetValue]"',
            f'{T}{T}value = "[{candidate_value("display_level")}.GetValue]"',
            f"{T}}}",
        ])
    else:
        lines.append(f"{T}widget = {{ parentanchor = right|vcenter position = {{ -10 0 }} size = {{ 172 20 }}")
        for module in range(1, 5):
            lines.extend([
                f"{T}{T}widget = {{ position = {{ {(module - 1) * 44} 0 }} size = {{ 40 20 }}",
                f"{T}{T}{T}background = {{ using = color_black_texture alpha = 0.5 }}",
                f'{T}{T}{T}widget = {{ visible = "[EqualTo_CFixedPoint({candidate_value(f"display_module_{module}")}.GetValue, \'(CFixedPoint)1.0\')]" size = {{ 100% 100% }} background = {{ using = color_yellow_texture alpha = 0.85 }} }}',
                f'{T}{T}{T}text_single = {{ size = {{ 100% 100% }} autoresize = no text = "TV_ENGINEERING_PRIORITY_MODULE_{module}" fontsize = 12 align = center|nobaseline }}',
                f"{T}{T}}}",
            ])
        lines.append(f"{T}}}")
    lines.extend([
        f"{T}button = {{",
        f"{T}{T}size = {{ 100% 100% }}",
        # The base button type supplies no texture. Keep the click layer
        # transparent with an explicit vanilla asset rather than an empty binding.
        f'{T}{T}texture = "gfx/portraits/portrait_transparent.dds"',
        f'{T}{T}enabled = "[{selection_gui}.IsValid({selection_scope})]"',
        f'{T}{T}onclick = "[{selection_gui}.Execute({selection_scope})]"',
        f"{T}{T}tooltipwidget = {{",
        f"{T}{T}{T}ContextualTooltipType = {{",
        f'{T}{T}{T}{T}blockoverride "title_text" {{ text = "tv_wonder_select_priority_candidate" }}',
        f'{T}{T}{T}{T}blockoverride "tooltip_content" {{ TooltipTextBlock = {{ blockoverride "text" {{ text = "tv_wonder_select_priority_candidate_desc" }} }} }}',
        f'{T}{T}{T}{T}blockoverride "tooltip_ui_action_block" {{}}',
        f"{T}{T}{T}}}",
        f"{T}{T}}}",
        f"{T}}}",
        "}",
    ])
    return "\n".join(lines)


def priority_candidates_list() -> str:
    lines = [
        "vbox = {",
        f'{T}visible = "[{priority_candidates_visible()}]"',
        f"{T}layoutpolicy_horizontal = expanding",
        f"{T}ignoreinvisible = yes",
        f"{T}spacing = 6",
        f"{T}hbox = {{",
        f"{T}{T}layoutpolicy_horizontal = expanding layoutpolicy_vertical = fixed size = {{ 470 116 }} spacing = 10 margin = {{ 8 8 }}",
        f"{T}{T}using = bg_paper_card_situations",
        f"{T}{T}widget = {{ size = {{ 76 92 }}",
        f"{T}{T}{T}portrait_standard_head_button = {{ using = character_portrait_bg parentanchor = center widgetanchor = center size = {{ 58 72 }}",
        f'{T}{T}{T}{T}visible = "[{var_is_set("tv_great_engineer_char")}]"',
        f'{T}{T}{T}{T}datacontext = "[{player_var("tv_great_engineer_char")}.GetCharacter]"',
        f'{T}{T}{T}{T}icon = {{ texture = "gfx/interface/component_decoration/character_frames/character_frame_1.dds" texture_density = 2 size = {{ 100% 100% }} }}',
        f"{T}{T}{T}}}",
        f"{T}{T}}}",
        f"{T}{T}widget = {{ size = {{ 368 92 }} using = bg_text_mask_container_dark_blue",
        f'{T}{T}{T}text_multi = {{ position = {{ 8 8 }} max_width = 352 autoresize = yes text = "TV_ENGINEERING_PRIORITY_LIST_TEXT" fontsize = 14 align = nobaseline|left }}',
        f"{T}{T}}}",
        f"{T}}}",
    ]
    for section, color in [("unfinished", "color_yellow_texture"), ("expansion", "color_market_green_texture")]:
        model = f"{PLAYER}.GetList('tv_wonder_priority_{section}_list')"
        lines.extend([
            f"{T}widget = {{ size = {{ 470 28 }} using = bg_text_mask_container_dark_blue",
            f"{T}{T}widget = {{ size = {{ 4 20 }} position = {{ 6 4 }} background = {{ using = {color} alpha = 1.0 }} }}",
            f'{T}{T}text_single = {{ position = {{ 18 0 }} size = {{ 300 28 }} autoresize = no text = "TV_ENGINEERING_PRIORITY_{section.upper()}_HEADER" fontsize = 15 align = nobaseline|left }}',
            f'{T}{T}text_single = {{ parentanchor = right position = {{ -10 0 }} size = {{ 60 28 }} autoresize = no raw_text = "[GetDataModelSize({model})]" fontsize = 15 align = nobaseline|right }}',
            f"{T}}}",
            f"{T}vbox = {{ layoutpolicy_horizontal = expanding spacing = 3",
            f'{T}{T}datamodel = "[{model}]"',
            f"{T}{T}item = {{",
            *indent_lines(priority_candidate_row(expansion=section == "expansion"), 3),
            f"{T}{T}}}",
            f"{T}}}",
        ])
    lines.append("}")
    return "\n".join(lines)


def dynamic_locked_text(
    prefix: str = "TV_ENGINEERING_WONDER_LOCKED_TEXT_", max_width: int = 352
) -> str:
    return (
        f'{T}text_multi = {{ visible = "[And({player_var("tv_wonder_locked_display_id")}.IsSet, Not({concept_in_progress()}))]" '
        f'max_width = {max_width} autoresize = yes text = "[{dynamic_localized_text_key(prefix, "tv_wonder_locked_display_id")}]" '
        f'align = nobaseline|left }}'
    )


def trigger_conditions_list(trigger_name: str, indent: int, width: int | None = None) -> list[str]:
    prefix = T * indent
    lines = [
        f"{prefix}TooltipRequirementsList = {{",
        f"{prefix}{T}layoutpolicy_horizontal = {'fixed' if width is not None else 'expanding'}",
        f'{prefix}{T}textcontext = "[ShowTriggerConditions(\'{trigger_name}\', PlayerScope.Self)]"',
    ]
    if width is not None:
        lines.extend(
            [
                f"{prefix}{T}maximumsize = {{ {width} -1 }}",
                f'{prefix}{T}blockoverride "tooltip_minimumsize" {{ minimumsize = {{ {width} -1 }} }}',
            ]
        )
    lines.extend(
        [
            f'{prefix}{T}blockoverride "field_text_format" {{',
            f"{prefix}{T}{T}fontsize = 13",
            f"{prefix}{T}}}",
            f'{prefix}{T}blockoverride "row_size" {{',
            f"{prefix}{T}{T}maximumsize = {{ -1 {SUITABILITY_LOCATION_CONDITION_ROW_HEIGHT} }}",
            f"{prefix}{T}{T}minimumsize = {{ -1 {SUITABILITY_LOCATION_CONDITION_ROW_HEIGHT} }}",
            f"{prefix}{T}}}",
            f'{prefix}{T}blockoverride "block_title" {{',
            f'{prefix}{T}{T}block "block_title" {{',
            f"{prefix}{T}{T}{T}visible = no",
            f"{prefix}{T}{T}}}",
            f"{prefix}{T}}}",
            f'{prefix}{T}blockoverride "requirementslist_datamodel_is_empty" {{',
            f"{prefix}{T}{T}visible = no",
            f"{prefix}{T}}}",
            f"{prefix}}}",
        ]
    )
    return lines


def suitability_location_conditions_type() -> str:
    lines = [
        "type tv_engineering_suitability_location_conditions_column = vbox {",
        f"{T}layoutpolicy_horizontal = fixed",
        f"{T}layoutpolicy_vertical = expanding",
        f"{T}minimumsize = {{ {SUITABILITY_KNOWLEDGE_COLUMN_WIDTH} -1 }}",
        f"{T}maximumsize = {{ {SUITABILITY_KNOWLEDGE_COLUMN_WIDTH} -1 }}",
        f"{T}ignoreinvisible = yes",
        f"{T}spacing = 3",
        f'{T}text_single = {{ text = "TV_ENGINEERING_SUITABILITY_LOCATION_CONDITIONS_TITLE" max_width = {SUITABILITY_KNOWLEDGE_COLUMN_WIDTH} fontsize = 13 align = nobaseline|left }}',
    ]
    lines.extend(
        trigger_conditions_list(
            "tv_wonder_site_rule_player_visible_locked_wonder_trigger",
            1,
            width=SUITABILITY_KNOWLEDGE_COLUMN_WIDTH,
        )
    )
    lines.append(f"{T}expand = {{}}")
    lines.append("}")
    return "\n".join(lines)


def suitability_composite_key_expr(row_index: int) -> str:
    mechanic_id_str = fixed_point_to_int_string(player_var("tv_wonder_locked_mechanic_id"))
    return f"MakeScopeFlag(Concatenate('tv_wonder_suitability_', Concatenate({mechanic_id_str}, '_{row_index}')))"


def suitability_condition_id_accessor(row_index: int) -> str:
    return (
        "GetVariableFromGlobalVariableMap('tv_wonder_suitability_condition_type', "
        f"{suitability_composite_key_expr(row_index)})"
    )


def suitability_weight_accessor(row_index: int) -> str:
    return (
        "GetVariableFromGlobalVariableMap('tv_wonder_suitability_weight', "
        f"{suitability_composite_key_expr(row_index)})"
    )


def suitability_row_used_visible(row_index: int) -> str:
    return f"Not(EqualTo_CFixedPoint({suitability_condition_id_accessor(row_index)}.GetValue, '(CFixedPoint)0'))"


def suitability_row_actual_complete_visible(actual_var: str) -> str:
    return (
        f"And({PLAYER}.GetVariable('tv_wonder_survey_complete').IsSet, "
        f"{PLAYER}.GetVariable('{actual_var}').IsSet)"
    )


def suitability_dynamic_row(row_index: int, reveal_var: str, indent: int) -> list[str]:
    prefix = T * indent
    revealed = reveal_progress_visible(reveal_var, row_index)
    actual_var = suitability_current_actual_variable(row_index)
    completed = suitability_row_actual_complete_visible(actual_var)
    label_expr = dynamic_localized_text_key_from_accessor(
        "TV_ENGINEERING_SUITABILITY_CONDITION_ID_", suitability_condition_id_accessor(row_index)
    )
    weight_text = f"#P [{suitability_weight_accessor(row_index)}.GetValue|+=]#!"
    actual_text = f"#P [{PLAYER}.GetVariable('{actual_var}').GetValue|+=]#!/{weight_text}"
    unknown_text = f"#T ?#!/{weight_text}"
    return [
        f"{prefix}vbox = {{",
        f'{prefix}{T}visible = "[{suitability_row_used_visible(row_index)}]"',
        f"{prefix}{T}layoutpolicy_horizontal = expanding",
        f"{prefix}{T}ignoreinvisible = yes",
        f"{prefix}{T}hbox = {{",
        f'{prefix}{T}{T}visible = "[{revealed}]"',
        f"{prefix}{T}{T}layoutpolicy_horizontal = expanding",
        f"{prefix}{T}{T}spacing = 4",
        f'{prefix}{T}{T}text_single = {{ text = "[{label_expr}]" max_width = {SUITABILITY_ROW_LABEL_MAX_WIDTH} fontsize = 13 align = nobaseline|left }}',
        f"{prefix}{T}{T}expand = {{}}",
        f'{prefix}{T}{T}text_single = {{ visible = "[{completed}]" raw_text = "{actual_text}" fontsize = 13 align = nobaseline|right }}',
        f'{prefix}{T}{T}text_single = {{ visible = "[Not({completed})]" raw_text = "{unknown_text}" fontsize = 13 align = nobaseline|right }}',
        f"{prefix}{T}}}",
        f"{prefix}{T}text_single = {{",
        f'{prefix}{T}{T}visible = "[Not({revealed})]"',
        f'{prefix}{T}{T}text = "TV_ENGINEERING_SUITABILITY_ROW_HIDDEN"',
        f"{prefix}{T}{T}max_width = {SUITABILITY_ROW_HIDDEN_MAX_WIDTH}",
        f"{prefix}{T}{T}fontsize = 13",
        f"{prefix}{T}{T}align = nobaseline|left",
        f"{prefix}{T}}}",
        f"{prefix}}}",
    ]


def suitability_knowledge_display() -> str:
    reveal_var = suitability_current_revealed_variable()
    visible = f"{player_var('tv_wonder_locked_mechanic_id')}.IsSet"
    min_height = 82 + SUITABILITY_KNOWLEDGE_ROW_SLOTS * 20
    lines: list[str] = [
        f"{T}widget = {{",
        f'{T}{T}visible = "[{visible}]"',
        f"{T}{T}layoutpolicy_vertical = shrinking",
        f"{T}{T}minimumsize = {{ 462 {min_height} }}",
        f"{T}{T}using = bg_text_mask_container_dark_blue",
        "",
        f"{T}{T}vbox = {{",
        f"{T}{T}{T}set_parent_size_to_minimum = yes",
        f"{T}{T}{T}layoutpolicy_horizontal = expanding",
        f"{T}{T}{T}layoutpolicy_vertical = shrinking",
        f"{T}{T}{T}margin = {{ 6 5 }}",
        f"{T}{T}{T}ignoreinvisible = yes",
        f"{T}{T}{T}spacing = 3",
        f'{T}{T}{T}text_single = {{ text = "TV_ENGINEERING_SUITABILITY_KNOWLEDGE_TITLE" fontsize = 18 align = nobaseline|left }}',
        f"{T}{T}{T}hbox = {{",
        f"{T}{T}{T}{T}layoutpolicy_horizontal = fixed",
        f"{T}{T}{T}{T}size = {{ {SUITABILITY_KNOWLEDGE_COLUMNS_WIDTH} -1 }}",
        f"{T}{T}{T}{T}spacing = {SUITABILITY_KNOWLEDGE_COLUMN_SPACING}",
        f"{T}{T}{T}{T}ignoreinvisible = yes",
        f"{T}{T}{T}{T}tv_engineering_suitability_location_conditions_column = {{ }}",
        f"{T}{T}{T}{T}vbox = {{",
        f"{T}{T}{T}{T}{T}layoutpolicy_horizontal = fixed",
        f"{T}{T}{T}{T}{T}layoutpolicy_vertical = expanding",
        f"{T}{T}{T}{T}{T}minimumsize = {{ {SUITABILITY_KNOWLEDGE_COLUMN_WIDTH} -1 }}",
        f"{T}{T}{T}{T}{T}maximumsize = {{ {SUITABILITY_KNOWLEDGE_COLUMN_WIDTH} -1 }}",
        f"{T}{T}{T}{T}{T}ignoreinvisible = yes",
        f"{T}{T}{T}{T}{T}spacing = 3",
        f'{T}{T}{T}{T}{T}text_single = {{ text = "TV_ENGINEERING_SUITABILITY_CONDITIONS_TITLE" max_width = {SUITABILITY_KNOWLEDGE_COLUMN_WIDTH} fontsize = 13 align = nobaseline|left }}',
    ]
    for row_index in range(1, SUITABILITY_KNOWLEDGE_ROW_SLOTS + 1):
        lines.extend(suitability_dynamic_row(row_index, reveal_var, 5))
    lines.extend(
        [
            f"{T}{T}{T}{T}{T}expand = {{}}",
            f"{T}{T}{T}{T}}}",
            f"{T}{T}{T}}}",
            f"{T}{T}}}",
            f"{T}}}",
        ]
    )
    return "\n".join(lines)


def preview_location_card(id_var_name: str) -> list[str]:
    visible_expr = f"{player_var(id_var_name)}.IsSet"
    text_expr = dynamic_localized_text_key("TV_ENGINEERING_WONDER_PREVIEW_LOCATION_TEXT_", id_var_name)
    return [
        f"{T}widget = {{",
        f'{T}{T}visible = "[{visible_expr}]"',
        f"{T}{T}size = {{ 100% {PREVIEW_TOP_CARD_HEIGHT} }}",
        f"{T}{T}parentanchor = top",
        f"{T}{T}widgetanchor = top",
        f"{T}{T}using = bg_text_mask_container_dark_blue",
        f"{T}{T}hbox = {{",
        f"{T}{T}{T}layoutpolicy_horizontal = expanding",
        f"{T}{T}{T}layoutpolicy_vertical = fixed",
        f"{T}{T}{T}margin = {{ 8 5 }}",
        f"{T}{T}{T}text_single = {{",
        f'{T}{T}{T}{T}text = "[{text_expr}]"',
        f"{T}{T}{T}{T}max_width = {PREVIEW_CONTENT_WIDTH}",
        f"{T}{T}{T}{T}fontsize = 13",
        f"{T}{T}{T}{T}align = nobaseline|left",
        f"{T}{T}{T}}}",
        f"{T}{T}{T}expand = {{}}",
        f"{T}{T}}}",
        f"{T}}}",
    ]


def preview_modifier_column(indent: int, *, title_key: str, modifier_key: str) -> list[str]:
    prefix = T * indent
    empty_key = "TV_WONDER_NO_BASE_COUNTRY_EFFECT" if "COUNTRY" in title_key else "TV_WONDER_NO_BASE_LOCATION_EFFECT"
    return [
        f"{prefix}vbox = {{",
        f"{prefix}{T}layoutpolicy_horizontal = fixed",
        f"{prefix}{T}layoutpolicy_vertical = shrinking",
        f"{prefix}{T}minimumsize = {{ {PREVIEW_MODIFIER_COLUMN_WIDTH} -1 }}",
        f"{prefix}{T}maximumsize = {{ {PREVIEW_MODIFIER_COLUMN_WIDTH} -1 }}",
        f"{prefix}{T}spacing = 2",
        f"{prefix}{T}text_single = {{",
        f'{prefix}{T}{T}text = "{title_key}"',
        f"{prefix}{T}{T}max_width = {PREVIEW_MODIFIER_COLUMN_WIDTH}",
        f"{prefix}{T}{T}align = left|nobaseline",
        f"{prefix}{T}{T}fontsize = 13",
        f"{prefix}{T}}}",
        f"{prefix}{T}TooltipStringPairList = {{",
        f"{prefix}{T}{T}layoutpolicy_horizontal = fixed",
        f"{prefix}{T}{T}maximumsize = {{ {PREVIEW_MODIFIER_COLUMN_WIDTH} -1 }}",
        f'{prefix}{T}{T}blockoverride "tooltip_minimumsize" {{ minimumsize = {{ {PREVIEW_MODIFIER_COLUMN_WIDTH} -1 }} }}',
        f'{prefix}{T}{T}blockoverride "field_text_format" {{',
        f"{prefix}{T}{T}{T}fontsize = 13",
        f"{prefix}{T}{T}{T}autoresize = yes",
        f"{prefix}{T}{T}{T}max_width = {PREVIEW_MODIFIER_TEXT_MAX_WIDTH}",
        f"{prefix}{T}{T}{T}elide = right",
        f"{prefix}{T}{T}}}",
        f'{prefix}{T}{T}blockoverride "row_size" {{',
        f"{prefix}{T}{T}{T}maximumsize = {{ -1 22 }}",
        f"{prefix}{T}{T}{T}minimumsize = {{ -1 22 }}",
        f"{prefix}{T}{T}}}",
        f'{prefix}{T}{T}textcontext = "[ShowModifierEffect({modifier_key})]"',
        f'{prefix}{T}{T}text_multi = {{ visible = "[Not(DataModelHasItems(StringPairList.GetRows))]" max_width = {PREVIEW_MODIFIER_COLUMN_WIDTH} autoresize = yes text = "{empty_key}" fontsize = 13 }}',
        f"{prefix}{T}}}",
        f"{prefix}}}",
    ]


def preview_effect_card(id_var_name: str) -> list[str]:
    visible_expr = f"{player_var(id_var_name)}.IsSet"
    country_modifier_key = dynamic_display_modifier_key(id_var_name, "_level_1")
    local_modifier_key = dynamic_display_modifier_key(id_var_name, "_local_level_1")
    lines = [
        f"{T}widget = {{",
        f'{T}{T}visible = "[{visible_expr}]"',
        f"{T}{T}size = {{ 100% -1 }}",
        f"{T}{T}parentanchor = bottom",
        f"{T}{T}widgetanchor = bottom",
        f"{T}{T}using = bg_text_mask_container_dark_blue",
        f"{T}{T}vbox = {{",
        f"{T}{T}{T}set_parent_size_to_minimum = yes",
        f"{T}{T}{T}layoutpolicy_horizontal = expanding",
        f"{T}{T}{T}layoutpolicy_vertical = shrinking",
        f"{T}{T}{T}margin = {{ 8 7 }}",
        f"{T}{T}{T}spacing = 4",
        f"{T}{T}{T}ignoreinvisible = yes",
        f'{T}{T}{T}text_single = {{ text = "TV_ENGINEERING_WONDER_PREVIEW_EFFECT_TITLE" max_width = {PREVIEW_CONTENT_WIDTH} fontsize = 14 align = nobaseline|left }}',
        f"{T}{T}{T}hbox = {{",
        f"{T}{T}{T}{T}layoutpolicy_horizontal = fixed",
        f"{T}{T}{T}{T}layoutpolicy_vertical = shrinking",
        f"{T}{T}{T}{T}size = {{ {PREVIEW_MODIFIER_COLUMNS_WIDTH} -1 }}",
        f"{T}{T}{T}{T}spacing = {PREVIEW_MODIFIER_COLUMN_SPACING}",
        f"{T}{T}{T}{T}ignoreinvisible = yes",
    ]
    lines.extend(
        preview_modifier_column(
            4,
            title_key="TV_LOCATION_WONDER_COUNTRY_MODIFIERS_TITLE",
            modifier_key=country_modifier_key,
        )
    )
    lines.extend(
        preview_modifier_column(
            4,
            title_key="TV_LOCATION_WONDER_LOCAL_MODIFIERS_TITLE",
            modifier_key=local_modifier_key,
        )
    )
    lines.extend(
        [
            f"{T}{T}{T}}}",
            f"{T}{T}}}",
            f"{T}}}",
        ]
    )
    return lines


def indent_lines(text: str, level: int) -> list[str]:
    prefix = T * level
    return [f"{prefix}{line}" if line else line for line in text.splitlines()]


def wonder_size_visible(wonders: list[dict], size_key: str, value_var_name: str) -> str:
    value_var = player_var(value_var_name)
    size_terms = [
        f"EqualTo_CFixedPoint({value_var}.GetValue, '(CFixedPoint){int(wonder['id'])}.0')"
        for wonder in wonders
        if wonder["size"] == size_key
    ]
    return fold_bool("And", [f"{value_var}.IsSet", fold_bool("Or", size_terms)])


def proposal_size_segment(
    indent: int,
    *,
    label_key: str,
    inactive_texture: str,
    active_texture: str,
    active_visible: str,
) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}widget = {{",
        f"{prefix}{T}layoutpolicy_horizontal = expanding",
        f"{prefix}{T}layoutpolicy_vertical = fixed",
        f"{prefix}{T}size = {{ -1 {PROPOSAL_SIZE_ROW_HEIGHT} }}",
        f"{prefix}{T}alwaystransparent = yes",
        f"{prefix}{T}background = {{",
        f"{prefix}{T}{T}using = {inactive_texture}",
        f"{prefix}{T}{T}alpha = {PROPOSAL_SIZE_INACTIVE_ALPHA}",
        f"{prefix}{T}}}",
        f"{prefix}{T}widget = {{",
        f'{prefix}{T}{T}visible = "[{active_visible}]"',
        f"{prefix}{T}{T}size = {{ 100% 100% }}",
        f"{prefix}{T}{T}alwaystransparent = yes",
        f"{prefix}{T}{T}background = {{",
        f"{prefix}{T}{T}{T}using = {active_texture}",
        f"{prefix}{T}{T}{T}alpha = {PROPOSAL_SIZE_ACTIVE_ALPHA}",
        f"{prefix}{T}{T}}}",
        f"{prefix}{T}{T}text_single = {{",
        f'{prefix}{T}{T}{T}text = "{label_key}"',
        f"{prefix}{T}{T}{T}size = {{ 100% 100% }}",
        f"{prefix}{T}{T}{T}parentanchor = center",
        f"{prefix}{T}{T}{T}align = center|nobaseline",
        f"{prefix}{T}{T}{T}fontsize = 13",
        f"{prefix}{T}{T}}}",
        f"{prefix}{T}}}",
        f"{prefix}}}",
    ]


def proposal_size_row(
    wonders: list[dict],
    indent: int,
    value_var_name: str,
    visible: str | None = None,
) -> list[str]:
    prefix = T * indent
    lines = [
        f"{prefix}hbox = {{",
    ]
    if visible:
        lines.append(f'{prefix}{T}visible = "[{visible}]"')
    lines.extend(
        [
            f"{prefix}{T}layoutpolicy_horizontal = expanding",
            f"{prefix}{T}layoutpolicy_vertical = fixed",
            f"{prefix}{T}size = {{ {PREVIEW_PANEL_WIDTH} {PROPOSAL_SIZE_ROW_HEIGHT} }}",
            f"{prefix}{T}spacing = 0",
        ]
    )
    for size_key, label_key, inactive_texture, active_texture in PROPOSAL_SIZE_INDICATORS:
        lines.extend(
            proposal_size_segment(
                indent + 1,
                label_key=label_key,
                inactive_texture=inactive_texture,
                active_texture=active_texture,
                active_visible=wonder_size_visible(wonders, size_key, value_var_name),
            )
        )
    lines.append(f"{prefix}}}")
    return lines


def locked_wonder_name_card(indent: int, visible: str) -> list[str]:
    prefix = T * indent
    return [
        f"{prefix}widget = {{",
        f'{prefix}{T}visible = "[{visible}]"',
        f"{prefix}{T}layoutpolicy_horizontal = fixed",
        f"{prefix}{T}layoutpolicy_vertical = fixed",
        f"{prefix}{T}size = {{ {PREVIEW_PANEL_WIDTH} {LOCKED_NAME_CARD_HEIGHT} }}",
        f"{prefix}{T}using = bg_country_banner",
        f"{prefix}{T}text_single = {{",
        f'{prefix}{T}{T}text = "{dynamic_locked_wonder_concept_link()}"',
        f"{prefix}{T}{T}size = {{ 100% 100% }}",
        f"{prefix}{T}{T}parentanchor = center",
        f"{prefix}{T}{T}position = {{ 0 {LOCKED_NAME_CARD_TEXT_Y_OFFSET} }}",
        f"{prefix}{T}{T}max_width = {PREVIEW_CONTENT_WIDTH}",
        f"{prefix}{T}{T}fontsize = 15",
        f"{prefix}{T}{T}align = center|nobaseline",
        f"{prefix}{T}}}",
        f"{prefix}}}",
    ]


def preview_widget(image_var_name: str, id_var_name: str, visible: str | None = None) -> str:
    var_expr = player_var(image_var_name)
    visible_expr = visible or f"{var_expr}.IsSet"
    lines = [
        "widget = {",
        f'{T}visible = "[{visible_expr}]"',
        f"{T}layoutpolicy_horizontal = fixed",
        f"{T}layoutpolicy_vertical = fixed",
        f"{T}size = {{ {PREVIEW_PANEL_WIDTH} {PREVIEW_IMAGE_HEIGHT} }}",
        f"{T}background = {{",
        f'{T}{T}texture = "[{dynamic_image_texture(image_var_name)}]"',
        f"{T}{T}fittype = centercrop",
        f"{T}}}",
    ]
    lines.extend(preview_location_card(id_var_name))
    lines.extend(preview_effect_card(id_var_name))
    lines.append("}")
    return "\n".join(lines)


def locked_preview_widget(wonders: list[dict], visible: str) -> str:
    lines = [
        "widget = {",
        f'{T}visible = "[{visible}]"',
        f"{T}layoutpolicy_horizontal = fixed",
        f"{T}layoutpolicy_vertical = fixed",
        f"{T}size = {{ {PREVIEW_PANEL_WIDTH} {LOCKED_PREVIEW_HEIGHT} }}",
        f"{T}vbox = {{",
        f"{T}{T}set_parent_size_to_minimum = yes",
        f"{T}{T}layoutpolicy_horizontal = expanding",
        f"{T}{T}layoutpolicy_vertical = shrinking",
        f"{T}{T}spacing = {PROPOSAL_SIZE_ROW_SPACING}",
        f"{T}{T}ignoreinvisible = yes",
    ]
    lines.extend(locked_wonder_name_card(2, visible))
    lines.extend(proposal_size_row(wonders, 2, "tv_wonder_locked_display_id", visible))
    lines.extend(indent_lines(preview_widget("tv_wonder_locked_image_display_id", "tv_wonder_locked_display_id", visible), 2))
    lines.extend(
        [
            f"{T}}}",
            "}",
        ]
    )
    return "\n".join(lines)


def proposal_preview_widget(wonders: list[dict], visible: str) -> str:
    proposal_image_visible = f"{player_var('tv_wonder_proposal')}.IsSet"
    lines = [
        "widget = {",
        f'{T}visible = "[{visible}]"',
        f"{T}layoutpolicy_horizontal = fixed",
        f"{T}layoutpolicy_vertical = fixed",
        f"{T}size = {{ {PREVIEW_PANEL_WIDTH} {PROPOSAL_PREVIEW_HEIGHT} }}",
        f"{T}vbox = {{",
        f"{T}{T}set_parent_size_to_minimum = yes",
        f"{T}{T}layoutpolicy_horizontal = expanding",
        f"{T}{T}layoutpolicy_vertical = shrinking",
        f"{T}{T}spacing = {PROPOSAL_SIZE_ROW_SPACING}",
        f"{T}{T}ignoreinvisible = yes",
    ]
    lines.extend(proposal_size_row(wonders, 2, "tv_wonder_proposal", proposal_image_visible))
    lines.extend(indent_lines(preview_widget("tv_wonder_proposal", "tv_wonder_proposal"), 2))
    lines.extend(
        [
            f"{T}}}",
            "}",
        ]
    )
    return "\n".join(lines)


def generate() -> str:
    wonders, _mechanics = load_all_wonder_mechanics_data()
    max_wonder_id = max(wonder["id"] for wonder in wonders)

    lines = render_header(SCRIPT_REL)
    lines.append("### BEGIN TV_WONDER_MECHANICS_PREVIEW_WIDGETS")
    locked_preview_visible = (
        f"And({player_var('tv_wonder_locked_image_display_id')}.IsSet, "
        f"Not({concept_in_progress()}))"
    )
    lines.append(locked_preview_widget(wonders, locked_preview_visible))
    proposal_preview_visible = (
        f"And3(Not({player_var('tv_wonder_locked')}.IsSet), "
        f"{player_var('tv_wonder_proposal')}.IsSet, "
        f"Not({concept_in_progress()}))"
    )
    lines.append(proposal_preview_widget(wonders, proposal_preview_visible))
    lines.append("### END TV_WONDER_MECHANICS_PREVIEW_WIDGETS")
    lines.append("")
    lines.append("### BEGIN TV_WONDER_MECHANICS_PROPOSAL_TEXTS")
    lines.append(dynamic_proposal_text("TV_ENGINEERING_WONDER_PROPOSAL_TEXT_"))
    lines.append("### END TV_WONDER_MECHANICS_PROPOSAL_TEXTS")
    lines.append("")
    lines.append("### BEGIN TV_WONDER_MECHANICS_PROPOSAL_RESUME_TEXTS")
    lines.append(dynamic_proposal_text("TV_ENGINEERING_WONDER_PROPOSAL_RESUME_TEXT_"))
    lines.append("### END TV_WONDER_MECHANICS_PROPOSAL_RESUME_TEXTS")
    lines.append("")
    lines.append("### BEGIN TV_WONDER_MECHANICS_PROPOSAL_EXPAND_TEXTS")
    lines.append(dynamic_proposal_text("TV_ENGINEERING_WONDER_PROPOSAL_EXPAND_TEXT_"))
    lines.append("### END TV_WONDER_MECHANICS_PROPOSAL_EXPAND_TEXTS")
    lines.append("")
    lines.append("### BEGIN TV_WONDER_MECHANICS_LOCKED_TEXTS")
    lines.append(dynamic_locked_text())
    lines.append("### END TV_WONDER_MECHANICS_LOCKED_TEXTS")
    lines.append("")
    lines.append("### BEGIN TV_WONDER_MECHANICS_SUITABILITY_LOCATION_CONDITIONS_TYPE")
    lines.append(suitability_location_conditions_type())
    lines.append("### END TV_WONDER_MECHANICS_SUITABILITY_LOCATION_CONDITIONS_TYPE")
    lines.append("")
    lines.append("### BEGIN TV_WONDER_MECHANICS_SUITABILITY_KNOWLEDGE")
    lines.append(suitability_knowledge_display())
    lines.append("### END TV_WONDER_MECHANICS_SUITABILITY_KNOWLEDGE")
    lines.append("")
    lines.append("### BEGIN TV_WONDER_MECHANICS_PROPOSAL_BUTTONS")
    for slot in range(1, 4):
        lines.append(proposal_button(slot))
    lines.append("### END TV_WONDER_MECHANICS_PROPOSAL_BUTTONS")
    lines.append("")
    lines.append("### BEGIN TV_WONDER_MECHANICS_PRIORITY_CANDIDATES")
    lines.append(priority_candidates_list())
    lines.append("### END TV_WONDER_MECHANICS_PRIORITY_CANDIDATES")
    lines.append("")
    from wonder_ritual_gui import ritual_card, ritual_types
    lines.extend(["### BEGIN TV_WONDER_RITUAL_TYPES", ritual_types(), "### END TV_WONDER_RITUAL_TYPES"])
    lines.extend(["### BEGIN TV_WONDER_RITUAL_CARD", ritual_card(_mechanics), "### END TV_WONDER_RITUAL_CARD"])
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(generate(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
