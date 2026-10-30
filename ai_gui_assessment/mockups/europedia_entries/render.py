"""Review-only Europedia entry design. Writes only beside this script.

Uses the real GUI renderer/styles/art and current gameplay data. Textual condition
samples below are reviewed translations of the two selected trigger scripts;
this does not run triggers, modifier effects, actions or a saved game.

Design contract: all entry text, values and texture paths are baked offline.
The eventual production entries must also remain static: no live effect/trigger
description APIs or current-country/location evaluation at load/display time.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.eu5-base/ai_gui_assessment/renderer'))
sys.path.insert(0, str(ROOT / 'scripts_engineering_department'))
from eu5_gui_renderer.config import configure_paths
configure_paths(workspace=ROOT, mod_root=Path('src'), output_root=OUT, language='simp_chinese')
from eu5_gui_renderer.gui import Expander, build_target
from eu5_gui_renderer.preview import load_resources, render_tree, has_diagnostics
from wonder_mechanics.io import load_all_wonder_mechanics_data
from wonder_mechanics.modifiers import wonder_base_country_modifiers, authored_final_building_local_modifiers
from wonder_mechanics.rituals import ritual_styles, ritual_rules
from wonder_mechanics._core import site_trigger_script_for_key
from europedia_render import card_header

draft_loc = {}
serial = 0


def key(text):
    global serial
    serial += 1
    k = f'GP_ENTRY_DRAFT_{serial}'
    draft_loc[k] = text
    return k


def text(value, x, y, width, height=28, *, font=16, gold=False, align='left', multi=False):
    kind = 'text_multi' if multi else 'text_single'
    sizing = f'min_width = {width} max_width = {width} autoresize = yes' if multi else f'size = {{ {width} {height} }} autoresize = no'
    style = 'using = Font_Type_Headers default_format = "#yellow_titles"' if gold else ''
    return f'{kind} = {{ position = {{ {x} {y} }} {sizing} fontsize = {font} align = {align}|nobaseline {style} text = "{key(value)}" }}'


def icon(texture, x, y, width=32, height=None):
    return f'icon = {{ position = {{ {x} {y} }} size = {{ {width} {height or width} }} texture = "{texture}" alwaystransparent = yes }}'


def rule(x, y, width, alpha=.5):
    return f'icon = {{ position = {{ {x} {y} }} size = {{ {width} 1 }} using = color_gold_texture alpha = {alpha} }}'


def section(title, y, texture):
    return '\n'.join([icon(texture, 0, y, 32), text(title, 44, y, 220, 32, font=19, gold=True), rule(262, y+16, 1108, .55)])


def value_string(modifier, value, metadata):
    percent = metadata[modifier]['value_kind'] == 'percent'
    result = f'{value*100:+g}%' if percent else f'{value:+g}'
    # Monthly societal movement has a direction, not an intrinsic good/bad sign.
    if modifier.startswith('monthly_towards_'):
        return result
    return '#G ' + result + '#!'


def make_draft(wonder, wonders, mechanics, loc, metadata):
    unique = wonder['is_unique']
    stem = wonder.get('image', 'tv_wonder_' + wonder['key'])
    art = f'gfx/interface/icons/towards_victory/wonders/{stem}.dds'
    name = loc.get('game_concept_' + wonder['concept'])
    size_names = {'small': '小型', 'medium': '中型', 'large': '大型'}
    group = '独特工程' if unique else '通用工程'
    lines = ['widget = { name = "entry_design" size = { 1530 1190 }',
             'background = { using = color_intense_bg_blue_texture }']
    for i, label in enumerate(('全部', '入门', '完整机制', '独特工程', '通用工程')):
        lines.append(f'button_regular = {{ position = {{ {20+i*300} 12 }} size = {{ 292 32 }} text = "{key(label)}" down = {"yes" if label == group else "no"} }}')
    count = sum(w['is_unique'] == unique for w in wonders)
    lines.append(text(f'{group}  ·  {count} 项', 40, 56, 600, font=15))
    lines.append('tv_eu_card = { position = { 40 92 }')
    header = []
    card_header(header, 'gfx/interface/icons/flat_icons/tabicons/europedia_flat_icon.dds', key(name))
    # The shared builder also opens its standard body vbox; this prototype
    # supplies its own body, so retain only the complete header override.
    lines.extend(header[:next(i for i, line in enumerate(header) if 'blockoverride "card_body"' in line)])
    lines.append('blockoverride "card_body" { widget = { name = "entry_body" size = { 1370 940 } margin = { 40 0 }')

    # Full 3:2 original art, not the square/cropped icon used by the existing cards.
    art_height = 360 if not unique else 359
    lines.append(f'widget = {{ name = "original_art" position = {{ 0 16 }} size = {{ 540 {art_height} }} background = {{ texture = "{art}" }} }}')
    lines.append(text(f'{size_names[wonder["size"]]}工程  ·  {loc.get(wonder["category"])}  ·  {loc.get(wonder["pop_type"])}', 576, 18, 794, 28, font=15))
    lines.append(icon('gfx/interface/icons/flat_icons/tabicons/mapmodes.dds', 576, 68, 30))
    lines.append(text('建造条件', 618, 68, 400, 32, font=19, gold=True))
    lines.append(rule(576, 108, 794))
    script = site_trigger_script_for_key(mechanics, wonder['mechanic_key'])
    if unique:
        assert script.strip() == 'is_capital = yes', script
        conditions = [f'固定地点  {loc.get(wonder["location"])}', '持有该地点', '该地点为本国首都']
        note = '独特工程 · 固定地点'
    else:
        assert 'location_rank:city' in script and 'location_rank:megalopolis' in script, script
        conditions = ['选择一处自有地点', f'地点等级为{loc.get("city")}或{loc.get("megalopolis")}']
        note = '通用工程 · 自由选址'
    for i, condition in enumerate(conditions):
        lines.append(text('•  '+condition, 582, 126+i*36, 770, 30, font=17))
    lines.append(text(note, 576, 262, 794, 28, font=15, gold=True))
    lines.append(text('由工程部提出工程，经辩论、勘测后开始施工。', 576, 300, 760, multi=True))

    # Exact level totals: the local base is per level, matching the shipped display modifiers.
    lines.append(section('各等级效果', 398, 'gfx/interface/icons/flat_icons/tabicons/advances.dds'))
    lines.append(text('各列为该等级的总效果', 1050, 438, 320, 24, font=14, align='right'))
    table_y = 468
    lines.append(f'widget = {{ name = "levels" position = {{ 0 {table_y} }} size = {{ 1370 150 }} using = bg_paper_card')
    label_width, col = 434, 156
    lines.append(text('效果', 18, 7, 400, 30, gold=True))
    for i, roman in enumerate(('I', 'II', 'III', 'IV', 'V', 'VI')):
        lines.append(text(roman+' 级', label_width+i*col, 7, col, 30, gold=True, align='center'))
    rows = []
    for scope, values in (('全国', wonder_base_country_modifiers(wonder, mechanics)), ('所在地', authored_final_building_local_modifiers(wonder, mechanics))):
        for modifier, base in values.items():
            rows.append({'scope': scope, 'modifier': modifier, 'values': [base*level for level in range(1,7)]})
    assert len(rows) == 2, 'These two review samples use two effect rows.'
    for ri, row in enumerate(rows):
        y = 44+ri*50
        lines.append(rule(14, y-2, 1342, .18))
        lines.append(text(row['scope'], 18, y+5, 82, 34, font=14, gold=True))
        lines.append(text(loc.get('MODIFIER_TYPE_NAME_'+row['modifier']), 108, y+5, 310, 34, font=16))
        for i, value in enumerate(row['values']):
            lines.append(text(value_string(row['modifier'], value, metadata), label_width+i*col, y+5, col, 34, font=17, align='center'))
    lines.append('}')

    lines.append(section('三种仪式', 642, 'gfx/interface/icons/flat_icons/hre_parliament.dds'))
    lines.append(text('选择一种仪式奉献工程', 1000, 684, 370, 24, font=14, align='right'))
    rituals = ritual_styles(wonder, mechanics)
    for ri, ritual in enumerate(rituals):
        x = ri*462
        lines.append(f'widget = {{ name = "ritual_{ri+1}" position = {{ {x} 716 }} size = {{ 446 212 }} using = bg_paper_card')
        axis = ritual['societal_value']
        side = 'left' if axis['sign'] < 0 else 'right'
        lines.append(icon(f'gfx/interface/icons/societal_values/{axis["axis"]}_{side}.dds', 16, 14, 42))
        lines.append(text(loc.get(ritual['name_key']), 72, 20, 358, 32, font=18, gold=True))
        lines.append(rule(16, 68, 414, .35))
        y = 78
        for caption, values in ((f'国家 · {ritual_rules(mechanics)["memory_years"]} 年', ritual['country_modifier']),
                                (f'所在地 · {ritual_rules(mechanics)["memory_years"]} 年', ritual['location_modifier_values'])):
            if not values:
                continue
            lines.append(text(caption, 18, y, 410, 22, font=13, gold=True))
            y += 23
            for modifier, value in values.items():
                lines.append(text(loc.get('MODIFIER_TYPE_NAME_'+modifier), 18, y, 318, 26, font=15))
                lines.append(text(value_string(modifier,value,metadata), 338, y, 90, 26, font=16, align='right'))
                y += 27
        if ritual['one_shot']:
            lines.append(text('落成时', 18, y, 410, 22, font=13, gold=True))
            y += 23
            for reward in ritual['one_shot']:
                label = {'ruler_mil': '统治者军事能力', 'ruler_dip': '统治者外交能力'}[reward['type']]
                lines.append(text(label, 18, y, 318, 26, font=15))
                lines.append(text(f'#G {reward["value"]:+g}#!', 338, y, 90, 26, font=16, align='right'))
                y += 27
        assert y <= 208
        lines.append('}')
    lines.append('} } }')
    lines.append(text('设计样稿 · 当前数据示例', 40, 1148, 1450, 24, font=14, align='right'))
    lines.append('}')
    return '\n'.join(lines), {'wonder': wonder['key'], 'site_rule': script, 'level_effects': rows, 'rituals': rituals}


def walk(node):
    yield node
    for child in node.children:
        yield from walk(child)


def main():
    wonders, mechanics = load_all_wonder_mechanics_data()
    resources = load_resources()
    metadata = json.loads((ROOT/'data/index/modifier_localization.json').read_text(encoding='utf-8'))['modifiers']
    for target, output in (('unique_topkapi_palace','unique'), ('triumphal_axis','generic')):
        wonder = next(w for w in wonders if w['key']==target)
        gui, snapshot = make_draft(wonder,wonders,mechanics,resources.loc,metadata)
        path = OUT/f'{output}.gui'
        path.write_text(gui,encoding='utf-8-sig')
        (OUT/f'{output}_data.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
        scene_resources = load_resources(extra_files=[path])
        scene_resources.loc.d.update(draft_loc)
        expander = Expander(scene_resources.db)
        tree = build_target(scene_resources.db,expander,'entry_design',path)
        details = {n.get('name'):n for n in walk(tree) if n.get('name') in ('levels','ritual_1','ritual_2','ritual_3')}
        assert set(details) == {'levels','ritual_1','ritual_2','ritual_3'}
        report = render_tree(tree,expander,scene_resources,[],width=1530,height=1190,output=Path(f'{output}.png'),
                            detail_elements=details,metadata={'prototype_only':True,'data_driven_sample':True,'wonder':target})
        if has_diagnostics(report):
            raise RuntimeError(json.dumps(report,ensure_ascii=False))
        for node in walk(tree):
            if node.kind == 'textbox' and node.w>0:
                assert 0 <= node.x and node.x+node.w <= 1530.1, (node.props,node.x,node.w)
                assert 0 <= node.y and node.y+node.h <= 1190.1, (node.props,node.y,node.h)
        print(f'{output}: clean render, {report["output"]}')
    loc_lines=['l_simp_chinese:']
    for k,v in draft_loc.items():
        loc_lines.append(f' {k}:0 '+json.dumps(v,ensure_ascii=False))
    (OUT/'draft_l_simp_chinese.yml').write_text('\n'.join(loc_lines)+'\n',encoding='utf-8-sig')


if __name__=='__main__':
    main()
