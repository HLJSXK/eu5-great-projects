"""Ledger ritual card. Read lifecycle caches; render executable effects natively."""
from wonder_ritual_codegen import ESTATES

PLAYER = 'InternationalOrganizationsView.GetPlayer.MakeScope'


def variable(name):
    return f"{PLAYER}.GetVariable('{name}')"


def equals(name, value):
    return f"EqualTo_CFixedPoint({variable(name)}.GetValue, '(CFixedPoint){value}.0')"


def selected(prefix):
    return variable(prefix + 'selected')


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


def section(key):
    return f'''widget = {{ size = {{ 438 24 }} background = {{ using = color_black_texture alpha = 0.3 }}
text_single = {{ position = {{ 8 0 }} size = {{ 422 24 }} autoresize = no fontsize = 14 text = "{key}" align = nobaseline|left }} }}'''


def ritual_types():
    # Independent slots prevent caller overrides from affecting sibling instances.
    return '''types TVWonderRitualTypes {
type tv_wonder_ritual_estate_card = widget {
size = { 216 68 }
background = { using = color_black_texture alpha = 0.22 }
block "reaction_tint" {}
icon = { position = { 8 8 } size = { 32 32 } block "estate_icon" {} }
text_single = { position = { 48 5 } size = { 158 24 } autoresize = no fontsize = 15 align = nobaseline|left block "estate_name" {} }
block "estate_reaction" {}
block "estate_reason" {}
}
}'''


def style_row(n, mechanics, pending, running):
    choice = equals('tv_wonder_ritual_choice', n)
    out = [f'''widget = {{ visible = "[Or({pending}, {choice})]" size = {{ 438 76 }}
{button(f'tv_wonder_ritual_preview_{n}', '', pending, width=438, height=76)}
widget = {{ visible = "[{choice}]" size = {{ 438 76 }} alwaystransparent = yes background = {{ using = color_yellow_texture alpha = 0.12 }} }}
widget = {{ visible = "[{choice}]" size = {{ 3 76 }} alwaystransparent = yes background = {{ using = color_yellow_texture }} }}''']
    for axis_id, data in enumerate(mechanics['societal_axes'].values(), 1):
        for sign, side in ((-1, 'left'), (1, 'right')):
            show = f"And({equals(f'tv_wonder_ritual_display_axis_{n}', axis_id)}, {equals(f'tv_wonder_ritual_display_dir_{n}', sign)})"
            out.append(f'icon = {{ visible = "[{show}]" position = {{ 12 16 }} size = {{ 36 36 }} texture = "{data[side + "_icon"]}" alwaystransparent = yes }}')
    axis = f"ToString_int32(FixedPointToInt({variable(f'tv_wonder_ritual_display_axis_{n}')}.GetValue))"
    direction = f"ToString_int32(FixedPointToInt({variable(f'tv_wonder_ritual_display_dir_{n}')}.GetValue))"
    side_key = f"Localize(Concatenate(Concatenate('TV_WONDER_RITUAL_SIDE_', {axis}), Concatenate('_', {direction})))"
    out += [f'''text_single = {{ position = {{ 58 5 }} size = {{ 340 24 }} autoresize = no fontsize = 17 raw_text = "{route(f'TV_WONDER_RITUAL_NAME_{n}_')}" align = nobaseline|left alwaystransparent = yes }}
text_single = {{ position = {{ 58 30 }} size = {{ 362 20 }} autoresize = no fontsize = 13 raw_text = "[{side_key}] · [Localize(Concatenate('TV_WONDER_RITUAL_REWARD_KIND_', ToString_int32(FixedPointToInt({variable(f'tv_wonder_ritual_reward_kind_{n}')}.GetValue))))]" align = nobaseline|left alwaystransparent = yes }}
text_single = {{ visible = "[{pending}]" position = {{ 58 52 }} size = {{ 350 20 }} autoresize = no fontsize = 13 text = "TV_WONDER_RITUAL_COUNTS_{n}" align = nobaseline|left alwaystransparent = yes }}
text_single = {{ visible = "[{choice}]" position = {{ 408 5 }} size = {{ 24 24 }} raw_text = "@trigger_yes!" alwaystransparent = yes }}
text_single = {{ visible = "[{running}]" position = {{ 58 52 }} size = {{ 350 20 }} autoresize = no fontsize = 13 text = "TV_WONDER_RITUAL_LOCKED" align = nobaseline|left alwaystransparent = yes }}
}}''']
    return '\n'.join(out)


def value_axis(mechanics):
    axis, direction, position = (selected('tv_wonder_ritual_' + key + '_') for key in ('display_axis', 'display_dir', 'position'))
    out = []
    for axis_id, data in enumerate(mechanics['societal_axes'].values(), 1):
        out.append(f'''widget = {{ visible = "[EqualTo_CFixedPoint({axis}.GetValue, '(CFixedPoint){axis_id}.0')]" size = {{ 438 40 }}''')
        for side, x, label_x in (('left', 0, 40), ('right', 402, 222)):
            out.append(f'''icon = {{ position = {{ {x} 2 }} size = {{ 36 36 }} texture = "{data[side + '_icon']}" }}
text_single = {{ position = {{ {label_x} 2 }} size = {{ 176 36 }} autoresize = no text = "{data[side]}_focus" fontsize = 14 align = nobaseline|{'left' if side == 'left' else 'right'} }}''')
        out.append('}')
    out += [f'''widget = {{ size = {{ 438 24 }}
progressbar = {{ position = {{ 0 8 }} size = {{ 216 8 }} min = 0 max = 1 invertprogress = yes
progresstexture = "gfx/interface/progressbars/progress_bar_blue_alt_left.dds"
noprogresstexture = "gfx/interface/progressbars/slider_default_bg.dds"
value = "[Abs_float(Min_float(FixedPointToFloat({position}.GetValue), '(float)0'))]" }}
progressbar = {{ position = {{ 222 8 }} size = {{ 216 8 }} min = 0 max = 1
progresstexture = "gfx/interface/progressbars/progress_bar_blue_alt.dds"
noprogresstexture = "gfx/interface/progressbars/slider_default_bg.dds"
value = "[Max_float(FixedPointToFloat({position}.GetValue), '(float)0')]" }}
widget = {{ position = {{ 218 4 }} size = {{ 2 16 }} background = {{ using = color_white_texture alpha = 0.7 }} }}
text_single = {{ visible = "[EqualTo_CFixedPoint({direction}.GetValue, '(CFixedPoint)-1.0')]" size = {{ 216 24 }} raw_text = "#Y ←#!" align = nobaseline|right }}
text_single = {{ visible = "[EqualTo_CFixedPoint({direction}.GetValue, '(CFixedPoint)1.0')]" position = {{ 222 0 }} size = {{ 216 24 }} raw_text = "#Y →#!" align = nobaseline|left }}
}}''']
    return '\n'.join(out)


def estate_cards():
    out = ['dynamicgridbox = { layoutpolicy_horizontal = expanding size = { 438 -1 } maximumsize = { 438 -1 } flipdirection = yes datamodel_wrap = 2 spacing = 6 ignoreinvisible = yes']
    for estate in ESTATES:
        pref = variable(f'tv_wonder_estate_pref_{estate}')
        support = f"EqualTo_CFixedPoint({pref}.GetValue, {variable('tv_wonder_ritual_choice')}.GetValue)"
        out += [f'''tv_wonder_ritual_estate_card = {{ visible = "[{pref}.IsSet]"
blockoverride "estate_icon" {{ texture = "gfx/interface/icons/estates/{estate}.dds" }}
blockoverride "estate_name" {{ text = "{estate}" }}
blockoverride "reaction_tint" {{
widget = {{ visible = "[{support}]" size = {{ 3 68 }} background = {{ using = color_market_green_texture }} }}
widget = {{ visible = "[Not({support})]" size = {{ 3 68 }} background = {{ using = color_mid_red_texture }} }}
}}
blockoverride "estate_reaction" {{
text_single = {{ visible = "[{support}]" position = {{ 48 28 }} size = {{ 158 20 }} autoresize = no fontsize = 13 text = "TV_WONDER_RITUAL_SUPPORT" align = nobaseline|left }}
text_single = {{ visible = "[Not({support})]" position = {{ 48 28 }} size = {{ 158 20 }} autoresize = no fontsize = 13 text = "TV_WONDER_RITUAL_OPPOSE" align = nobaseline|left }}
}}
blockoverride "estate_reason" {{''']
        for source, label in ((1, 'LOCATION'), (2, 'HISTORICAL'), (3, 'RANDOM')):
            out.append(f'text_single = {{ visible = "[{equals(f"tv_wonder_estate_pref_source_{estate}", source)}]" position = {{ 8 48 }} size = {{ 200 18 }} autoresize = no fontsize = 12 text = "TV_WONDER_RITUAL_REASON_{label}" align = nobaseline|left }}')
        out.append('} }')
    return '\n'.join(out + ['}'])


def ritual_card(mechanics):
    running = f"{variable('tv_wonder_ritual_in_progress')}.IsSet"
    complete = f"Or({variable('tv_wonder_ritual_completed')}.IsSet, {variable('tv_wonder_finalized')}.IsSet)"
    pending = f"Not(Or({running}, {complete}))"
    reritual = equals('tv_wonder_project_mode', 3)
    plain = f"And({variable('tv_wonder_ritual_choice')}.IsSet, {equals('tv_wonder_ritual_choice', 0)})"
    chosen = f"And({variable('tv_wonder_ritual_choice')}.IsSet, Not({plain}))"
    details_open = "GetVariableSystem.Exists('tv_wonder_ritual_details_open')"
    out = ['vbox = { name = "tv_wonder_ritual_ledger" layoutpolicy_horizontal = expanding layoutpolicy_vertical = shrinking set_parent_size_to_minimum = yes ignoreinvisible = yes spacing = 6 margin = { 12 10 }']
    out.append(text('TV_WONDER_RITUAL_HEADER', f'And({pending}, Not({reritual}))', size=14))
    out.append(f'''hbox = {{ visible = "[And(Not({complete}), {reritual})]" layoutpolicy_horizontal = expanding spacing = 6
{text('TV_WONDER_RERITUAL_BANNER', width=282, size=14)}
{button('tv_wonder_ritual_cancel_reritual', 'TV_WONDER_RITUAL_CANCEL_SHORT', pending, width=150)} }}''')
    for n in (1, 2, 3):
        out.append(style_row(n, mechanics, pending, running))
    out.append(f'''widget = {{ visible = "[And({pending}, Not({reritual}))]" size = {{ 438 58 }}
{button('tv_wonder_ritual_preview_plain', '', width=438, height=58)}
widget = {{ size = {{ 438 58 }} alwaystransparent = yes background = {{ using = color_black_texture alpha = 0.3 }} }}
widget = {{ visible = "[{plain}]" size = {{ 438 58 }} alwaystransparent = yes background = {{ using = color_yellow_texture alpha = 0.12 }} }}
widget = {{ visible = "[{plain}]" size = {{ 3 58 }} alwaystransparent = yes background = {{ using = color_yellow_texture }} }}
text_single = {{ position = {{ 12 4 }} size = {{ 390 24 }} text = "TV_WONDER_RITUAL_PLAIN_STATE" alwaystransparent = yes align = nobaseline|left }}
text_single = {{ position = {{ 12 30 }} size = {{ 410 20 }} fontsize = 13 text = "TV_WONDER_RITUAL_PLAIN_CONSEQUENCE" alwaystransparent = yes align = nobaseline|left }}
text_single = {{ visible = "[{plain}]" position = {{ 408 4 }} size = {{ 24 24 }} raw_text = "@trigger_yes!" alwaystransparent = yes }} }}''')
    out += [f'vbox = {{ visible = "[{running}]" layoutpolicy_horizontal = expanding spacing = 4',
            text('TV_WONDER_RITUAL_PROGRESS'),
            f'''progressbar = {{ size = {{ 438 14 }} min = 0 max = 100
progresstexture = "gfx/interface/progressbars/progress_bar_goldish.dds" noprogresstexture = "gfx/interface/progressbars/slider_default_bg.dds"
value = "[{variable('tv_wonder_ritual_progress_pct')}.GetValue]" }}''',
            text('TV_WONDER_RITUAL_ESTATES_SETTLED', size=13),
            '''button_regular = { size = { 438 28 } text = "TV_WONDER_RITUAL_TOGGLE_DETAILS" tooltip = "TV_WONDER_RITUAL_TOGGLE_DETAILS"
onclick = "[GetVariableSystem.Toggle('tv_wonder_ritual_details_open')]" }''', '}']
    out.append(f'vbox = {{ visible = "[And({chosen}, And(Not({complete}), Or({pending}, {details_open})))]" layoutpolicy_horizontal = expanding layoutpolicy_vertical = shrinking ignoreinvisible = yes spacing = 6')
    out += [text('#F ' + route('TV_WONDER_RITUAL_DESC_', dynamic_style=True) + '#!', raw=True, size=14),
            section('TV_WONDER_RITUAL_SECTION_EFFECTS'),
            text("[ShowScriptedEffectForScope('tv_wonder_ritual_apply_choice_effect',InternationalOrganizationsView.GetPlayer.MakeScope.Self)]", raw=True, size=14),
            section('TV_WONDER_RITUAL_SECTION_VALUES'), value_axis(mechanics),
            section('TV_WONDER_RITUAL_ESTATES_PENDING'), estate_cards(), '}']
    out.append(text('TV_WONDER_RITUAL_PLAIN_DETAIL', f'And({pending}, {plain})', size=14))
    out.append(f'vbox = {{ visible = "[{pending}]" layoutpolicy_horizontal = expanding ignoreinvisible = yes spacing = 6')
    out += [section('TV_WONDER_RITUAL_SECTION_TERMS'), text('TV_WONDER_RITUAL_TERMS', f"And(Not({plain}), Not({variable('tv_wonder_cmm_skip_ceremony')}.IsSet))", size=14),
            text("[ShowScriptedEffectForScope('tv_wonder_ritual_pay_effect',InternationalOrganizationsView.GetPlayer.MakeScope.Self)]", f"And(Not({plain}), Not({variable('tv_wonder_cmm_skip_ceremony')}.IsSet))", raw=True, size=14),
            text('TV_WONDER_RITUAL_SKIP_TERMS', f"And(Not({plain}), {variable('tv_wonder_cmm_skip_ceremony')}.IsSet)", size=14),
            text('TV_WONDER_RITUAL_PLAIN_TERMS', plain, size=14),
            button('tv_wonder_ritual_confirm', 'TV_WONDER_RITUAL_CONFIRM', f'Not({plain})', height=38),
            button('tv_wonder_ritual_choose_plain', 'TV_WONDER_RITUAL_PLAIN', plain, height=38), '}']
    inherited = equals('tv_wonder_finalization_outcome', 9)
    out += [text('TV_WONDER_RITUAL_COMPLETE_PENDING', f'And({complete}, Or({chosen}, {inherited}))', size=17),
            text('TV_WONDER_RITUAL_PLAIN_COMPLETE', f'And({complete}, Not(Or({chosen}, {inherited})))', size=17), '}']
    return '\n'.join(out)
