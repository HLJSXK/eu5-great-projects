"""Ledger ritual card. Read lifecycle caches; render executable effects natively."""
from wonder_ritual_codegen import ESTATES

PLAYER = 'InternationalOrganizationsView.GetPlayer.MakeScope'


def variable(name):
    return f"{PLAYER}.GetVariable('{name}')"


def equals(name, value):
    return f"EqualTo_CFixedPoint({variable(name)}.GetValue, '(CFixedPoint){value}.0')"


def text(key, visible=None, raw=False, width=438, size=15):
    show = f'visible = "[{visible}]"' if visible else ''
    return f'''text_multi = {{ {show} layoutpolicy_horizontal = expanding minimumsize = {{ {width} -1 }}
max_width = {width} autoresize = yes fontsize = {size} {'raw_text' if raw else 'text'} = "{key}" align = nobaseline|left }}'''


def button(action, key, visible=None, raw=False, width=438, height=34):
    show = f'visible = "[{visible}]"' if visible else ''
    return f'''button_regular = {{ {show} size = {{ {width} {height} }} enabled = "[PdxGuiWidget.IsUberButtonEnabled]"
{'raw_text' if raw else 'text'} = "{key}"
scripted_action_tooltip = {{ click_type = left click_mode = single action_name = "{action}" actor = "[InternationalOrganizationsView.GetPlayer]" }}
button_tooltip_override = {{ title = "{action}" description = "{action}_desc" }}
tooltipwidget = {{ using = action_tooltip_pop_out }}
}}'''


def route(prefix, dynamic_style=False):
    wid = f"ToString_int32(FixedPointToInt({variable('tv_wonder_locked')}.GetValue))"
    key = f"Concatenate('{prefix}', {wid})"
    if dynamic_style:
        choice = f"ToString_int32(FixedPointToInt({variable('tv_wonder_ritual_choice')}.GetValue))"
        key = f"Concatenate(Concatenate('{prefix}', {choice}), Concatenate('_', {wid}))"
    return f"[Localize({key})]"


def section(name, key, content, visible=None):
    show = f' visible = "[{visible}]"' if visible else ''
    return f'''vbox = {{ name = "tv_wonder_ritual_section_{name}"{show}
layoutpolicy_horizontal = expanding layoutpolicy_vertical = shrinking ignoreinvisible = yes spacing = 6
widget = {{ size = {{ 438 24 }} background = {{ using = color_black_texture alpha = 0.3 }}
text_single = {{ position = {{ 8 0 }} size = {{ 422 24 }} autoresize = no fontsize = 14 text = "{key}" align = nobaseline|left }} }}
{chr(10).join(content)}
}}'''


def ritual_types():
    return '''types TVWonderRitualTypes {
type tv_wonder_ritual_supporter = widget {
size = { 36 36 }
alwaystransparent = no
icon = { size = { 32 32 } alwaystransparent = yes block "estate_icon" {} }
icon = {
name = "support_badge"
position = { 20 20 } size = { 16 16 }
texture = "gfx/interface/icons/text_icons/trigger_yes.dds"
alwaystransparent = yes
}
}
}'''


def choice_card(key, title, choice, pending, icons, *, raw=False, visible=None):
    show = f' visible = "[{visible}]"' if visible else ''
    return f'''widget = {{ name = "tv_wonder_ritual_choice_{key}"{show} size = {{ 438 42 }}
{button(f'tv_wonder_ritual_preview_{key}', '', pending, width=438, height=42)}
widget = {{ visible = "[{choice}]" size = {{ 438 42 }} alwaystransparent = yes background = {{ using = color_yellow_texture alpha = 0.12 }} }}
widget = {{ visible = "[{choice}]" size = {{ 3 42 }} alwaystransparent = yes background = {{ using = color_yellow_texture }} }}
{chr(10).join(icons)}
text_single = {{ position = {{ 52 9 }} size = {{ 374 24 }} autoresize = no fontsize = 17 {'raw_text' if raw else 'text'} = "{title}" align = nobaseline|left alwaystransparent = yes }}
}}'''


def style_row(n, mechanics, pending):
    choice = equals('tv_wonder_ritual_choice', n)
    icons = []
    for axis_id, data in enumerate(mechanics['societal_axes'].values(), 1):
        for sign, side in ((-1, 'left'), (1, 'right')):
            show = f"And({equals(f'tv_wonder_ritual_display_axis_{n}', axis_id)}, {equals(f'tv_wonder_ritual_display_dir_{n}', sign)})"
            icons.append(f'icon = {{ visible = "[{show}]" position = {{ 10 5 }} size = {{ 32 32 }} texture = "{data[side + "_icon"]}" alwaystransparent = yes }}')
    return '\n'.join([
        f'''vbox = {{ name = "tv_wonder_ritual_style_{n}" visible = "[Or({pending}, {choice})]"
layoutpolicy_horizontal = expanding layoutpolicy_vertical = shrinking ignoreinvisible = yes spacing = 4''',
        choice_card(n, route(f'TV_WONDER_RITUAL_NAME_{n}_'), choice, pending, icons, raw=True),
        supporting_estates(n), '}'])


def supporter_tooltip(estate):
    reasons = []
    for source, label in ((1, 'LOCATION'), (2, 'HISTORICAL'), (3, 'RANDOM')):
        reasons.append(f'''TooltipTextBlock = {{
visible = "[{equals(f'tv_wonder_estate_pref_source_{estate}', source)}]"
blockoverride "text" {{ text = "TV_WONDER_RITUAL_SUPPORT_REASON_{label}" }}
}}''')
    return f'''tooltipwidget = {{ ContextualTooltipType = {{
blockoverride "title_icon_texture" {{ texture = "gfx/interface/icons/estates/{estate}.dds" }}
blockoverride "title_text" {{ text = "TV_WONDER_RITUAL_ESTATE_SUPPORTS_STYLE" }}
blockoverride "concept_link" {{ visible = no }}
blockoverride "tooltip_content" {{
{chr(10).join(reasons)}
}}
}} }}'''


def supporting_estates(style):
    # At most seven icons fit in one row; hidden estates leave no gaps.
    # Native flowcontainer supports spacing, unlike dynamicgridbox.
    out = [f'''flowcontainer = {{ name = "tv_wonder_ritual_supporters_{style}"
layoutpolicy_horizontal = expanding layoutpolicy_vertical = shrinking size = {{ 438 -1 }} maximumsize = {{ 438 -1 }}
direction = horizontal wrap_count = 7 spacing = 10 margin = {{ 10 0 }} ignoreinvisible = yes''']
    for estate in ESTATES:
        pref = variable(f'tv_wonder_estate_pref_{estate}')
        support = f"And({pref}.IsSet, {equals(f'tv_wonder_estate_pref_{estate}', style)})"
        out.append(f'''tv_wonder_ritual_supporter = {{ name = "{estate}" visible = "[{support}]"
datacontext = "[InternationalOrganizationsView.GetPlayer.GetGovernment.GetEstateFromKey('{estate}')]"
blockoverride "estate_icon" {{ texture = "gfx/interface/icons/estates/{estate}.dds" }}
{supporter_tooltip(estate)}
}}''')
    return '\n'.join(out + ['}'])


def ritual_card(mechanics):
    running = f"{variable('tv_wonder_ritual_in_progress')}.IsSet"
    complete = f"Or({variable('tv_wonder_ritual_completed')}.IsSet, {variable('tv_wonder_finalized')}.IsSet)"
    pending = f"Not(Or({running}, {complete}))"
    plain = f"And({variable('tv_wonder_ritual_choice')}.IsSet, {equals('tv_wonder_ritual_choice', 0)})"
    chosen = f"And({variable('tv_wonder_ritual_choice')}.IsSet, Not({plain}))"
    details_open = "GetVariableSystem.Exists('tv_wonder_ritual_details_open')"
    show_details = f'And({chosen}, And(Not({complete}), Or({pending}, {details_open})))'
    out = ['vbox = { name = "tv_wonder_ritual_ledger" layoutpolicy_horizontal = expanding layoutpolicy_vertical = shrinking set_parent_size_to_minimum = yes ignoreinvisible = yes spacing = 6 margin = { 12 10 }']
    choices = [style_row(n, mechanics, pending) for n in (1, 2, 3)]
    choices.append(choice_card('plain', 'TV_WONDER_RITUAL_PLAIN_STATE', plain, pending, [
        'icon = { position = { 10 5 } size = { 32 32 } texture = "gfx/interface/icons/flat_icons/building_default.dds" alwaystransparent = yes }'
    ], visible=pending))
    # Native panel flavor formatting; retain the default text font size.
    choices.append(f'''text_multi = {{ visible = "[{show_details}]"
layoutpolicy_horizontal = expanding minimumsize = {{ 438 -1 }} max_width = 438
autoresize = yes align = nobaseline|left default_format = "#flavor"
raw_text = "{route('TV_WONDER_RITUAL_DESC_', dynamic_style=True)}" }}''')
    out.append(section('options', 'TV_WONDER_RITUAL_SECTION_OPTIONS', choices))
    out += [f'vbox = {{ visible = "[{running}]" layoutpolicy_horizontal = expanding spacing = 4',
            text('TV_WONDER_RITUAL_PROGRESS'),
            f'''progressbar = {{ size = {{ 438 14 }} min = 0 max = 100
progresstexture = "gfx/interface/progressbars/progress_bar_goldish.dds" noprogresstexture = "gfx/interface/progressbars/slider_default_bg.dds"
value = "[{variable('tv_wonder_ritual_progress_pct')}.GetValue]" }}''',
            text('TV_WONDER_RITUAL_ESTATES_SETTLED', size=13),
            '''button_regular = { size = { 438 28 } text = "TV_WONDER_RITUAL_TOGGLE_DETAILS" tooltip = "TV_WONDER_RITUAL_TOGGLE_DETAILS"
onclick = "[GetVariableSystem.Toggle('tv_wonder_ritual_details_open')]" }''', '}']
    requirements = [text('TV_WONDER_RITUAL_TERMS', f"And(Not({plain}), Not({variable('tv_wonder_cmm_skip_ceremony')}.IsSet))", size=14),
            text("[ShowScriptedEffectForScope('tv_wonder_ritual_pay_effect',InternationalOrganizationsView.GetPlayer.MakeScope.Self)]", f"And(Not({plain}), Not({variable('tv_wonder_cmm_skip_ceremony')}.IsSet))", raw=True, size=14),
            text('TV_WONDER_RITUAL_SKIP_TERMS', f"And(Not({plain}), {variable('tv_wonder_cmm_skip_ceremony')}.IsSet)", size=14),
            text('TV_WONDER_RITUAL_PLAIN_TERMS', plain, size=14)]
    out.append(section('requirements', 'TV_WONDER_RITUAL_SECTION_TERMS', requirements, pending))
    effects = [f'vbox = {{ visible = "[{show_details}]" layoutpolicy_horizontal = expanding layoutpolicy_vertical = shrinking ignoreinvisible = yes spacing = 6',
            text("[ShowScriptedEffectForScope('tv_wonder_ritual_apply_choice_effect',InternationalOrganizationsView.GetPlayer.MakeScope.Self)]", raw=True, size=14),
            '}',
            text('TV_WONDER_RITUAL_PLAIN_DETAIL', f'And({pending}, {plain})', size=14),
            text('TV_WONDER_RITUAL_SELECT_FOR_EFFECTS', f'And({pending}, Not({variable("tv_wonder_ritual_choice")}.IsSet))', size=14)]
    out.append(section('effects', 'TV_WONDER_RITUAL_SECTION_EFFECTS', effects, f'Or({pending}, {show_details})'))
    out.append(f'vbox = {{ name = "tv_wonder_ritual_actions" visible = "[{pending}]" layoutpolicy_horizontal = expanding layoutpolicy_vertical = shrinking ignoreinvisible = yes spacing = 6')
    out += [button('tv_wonder_ritual_confirm', 'TV_WONDER_RITUAL_CONFIRM', f'Not({plain})', height=38),
            button('tv_wonder_ritual_choose_plain', 'TV_WONDER_RITUAL_PLAIN', plain, height=38), '}']
    inherited = equals('tv_wonder_finalization_outcome', 9)
    out += [text('TV_WONDER_RITUAL_COMPLETE_PENDING', f'And({complete}, Or({chosen}, {inherited}))', size=17),
            text('TV_WONDER_RITUAL_PLAIN_COMPLETE', f'And({complete}, Not(Or({chosen}, {inherited})))', size=17), '}']
    return '\n'.join(out)
