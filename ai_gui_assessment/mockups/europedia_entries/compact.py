"""Compact review-only entries; three complete entries per 1080px preview.

All strings, numbers and artwork paths are baked offline. No production files
are edited. Fixed-location navigation runs only on click; display has no live
game-data bindings.
"""
from pathlib import Path
import json
import re

import render as draft
from PIL import Image
from eu5_gui_renderer.gui import Expander, build_target
from eu5_gui_renderer.preview import load_resources, render_tree, has_diagnostics
from wonder_mechanics.io import load_all_wonder_mechanics_data
from wonder_mechanics.modifiers import wonder_base_country_modifiers, authored_final_building_local_modifiers
from wonder_mechanics.rituals import ritual_styles, ritual_rules

OUT = Path(__file__).resolve().parent
text, icon, rule, key = draft.text, draft.icon, draft.rule, draft.key
SAMPLES = {
    'unique': ['unique_topkapi_palace', 'unique_pharos_lighthouse', 'unique_hagia_sophia'],
    'generic': ['triumphal_axis', 'great_lighthouse', 'palace_of_nations'],
}


def entry(wonder, mechanics, loc, metadata, index):
    y = 82 + index * 312
    wid = wonder['id']
    # Identity variants use explicit authored default strings in this catalogue,
    # never the gameplay localization that evaluates a global variable.
    identity_suffix = '_identity_default' if wonder.get('identity_variants') else ''
    stem = wonder.get('image', 'tv_wonder_' + wonder['key'])
    art = f'gfx/interface/icons/towards_victory/wonders/{stem}.dds'
    width, height = Image.open(draft.ROOT/'src/main_menu'/art).size
    scale = min(240 / width, 160 / height)
    art_width, art_height = round(width * scale), round(height * scale)
    art_x, art_y = 16 + (240-art_width)//2, 42 + (160-art_height)//2
    lines = [f'widget = {{ name = "entry_{wid}" position = {{ 40 {y} }} size = {{ 1450 300 }} using = bg_paper_card',
             'blockoverride "card_color" { using = color_intense_bg_blue_texture blend_mode = multiply }',
             'widget = { size = { 1450 32 } background = { using = button_main_tab_texture frame = 4 modify_texture = { using = color_intense_bg_blue_texture blend_mode = multiply } } }',
             icon('gfx/interface/icons/flat_icons/tabicons/europedia_flat_icon.dds', 12, 4, 24),
             text(loc.get('game_concept_'+wonder['concept']+identity_suffix), 46, 2, 880, 28, font=19, gold=True),
             text(f'{ {"small":"小型","medium":"中型","large":"大型"}[wonder["size"]]} · {loc.get(wonder["category"])} · {loc.get(wonder["pop_type"])}', 970, 4, 464, 24, font=14, align='right'),
             f'widget = {{ name = "art_{wid}" position = {{ {art_x} {art_y} }} size = {{ {art_width} {art_height} }} background = {{ texture = "{art}" }} }}']
    location_reference = None
    if wonder['is_unique']:
        location_id = wonder['location']
        location_name = loc.get(location_id)
        assert location_name and '[' not in location_name
        location_reference = {'id': location_id, 'name': location_name}
        lines.append(f'button = {{ name = "location_reference_{wid}" position = {{ 16 224 }} size = {{ 240 48 }}')
        # Fixed display text; the typed location lookup runs only on click.
        # Source: context_menu.gui PanToLocation/SelectLocation callers and
        # religious_doctrine.gui's GetLocationByKey fixed-id references.
        lines.append(f'onclick = "[SelectLocation(GetLocationByKey(\'{location_id}\'))]"')
        lines.append(f'tooltip = "{key(location_name)}"')
        lines.append(icon('gfx/interface/icons/map_subdivisons/location.dds',8,8,32))
        lines.append(text('#L '+location_name+'#!',48,8,184,32,font=16).replace('text_single = {', 'text_single = { alwaystransparent = yes',1))
        lines.append('}')

    rows = []
    for scope, values in (('全国',wonder_base_country_modifiers(wonder,mechanics)),('当地',authored_final_building_local_modifiers(wonder,mechanics))):
        for modifier, base in values.items():
            rows.append({'scope':scope,'modifier':modifier,'values':[base*i for i in range(1,7)]})
    assert 1 <= len(rows) <= 3
    lines.append(f'widget = {{ name = "levels_{wid}" position = {{ 282 40 }} size = {{ 1152 106 }}')
    lines.append(text('各等级总效果',8,0,310,24,font=14,gold=True))
    label_width, col = 330, 137
    for ci, roman in enumerate(('I','II','III','IV','V','VI')):
        lines.append(text(roman,label_width+ci*col,0,col,24,font=15,gold=True,align='center'))
    for ri, row in enumerate(rows):
        ry = 27+ri*26
        lines.append(rule(0,ry,1152,.16))
        lines.append(text(row['scope'],8,ry+2,44,24,font=13,gold=True))
        lines.append(text(loc.get('MODIFIER_TYPE_NAME_'+row['modifier']),58,ry+2,268,24,font=15))
        for ci, value in enumerate(row['values']):
            lines.append(text(draft.value_string(row['modifier'],value,metadata),label_width+ci*col,ry+2,col,24,font=15,align='center'))
    lines.append('}')

    rituals = ritual_styles(wonder,mechanics)
    for ri, ritual in enumerate(rituals):
        lines.append(f'widget = {{ name = "ritual_{wid}_{ri+1}" position = {{ {282+ri*390} 178 }} size = {{ 372 110 }} using = bg_paper_card')
        axis = ritual['societal_value']
        side = 'left' if axis['sign'] < 0 else 'right'
        lines.append(icon(f'gfx/interface/icons/societal_values/{axis["axis"]}_{side}.dds',10,8,26))
        lines.append(text(loc.get(ritual['name_key']+identity_suffix),44,8,318,26,font=16,gold=True))
        lines.append(rule(10,36,352,.3))
        effect_y = 40
        for scope, values in (('全国',ritual['country_modifier']),('当地',ritual['location_modifier_values'])):
            for modifier,value in values.items():
                lines.append(text(scope,10,effect_y,34,22,font=12,gold=True))
                lines.append(text(loc.get('MODIFIER_TYPE_NAME_'+modifier),48,effect_y,244,22,font=14))
                lines.append(text(draft.value_string(modifier,value,metadata),292,effect_y,70,22,font=14,align='right'))
                effect_y += 22
        for reward in ritual['one_shot']:
            label = {'ruler_mil':'统治者军事能力','ruler_dip':'统治者外交能力','prestige':'威望','all_estate_satisfaction':'所有阶层满意度'}[reward['type']]
            value = f'{reward["value"]*100:+g}%' if reward['type']=='all_estate_satisfaction' else f'{reward["value"]:+g}'
            lines.append(text('一次',10,effect_y,34,22,font=12,gold=True))
            lines.append(text(label,48,effect_y,244,22,font=14))
            lines.append(text('#G '+value+'#!',292,effect_y,70,22,font=14,align='right'))
            effect_y += 22
        assert effect_y <= 106
        lines.append('}')
    lines.append('}')
    return lines, {'id':wid,'wonder':wonder['key'],'location_reference':location_reference,'level_effects':rows,'rituals':rituals}


def main():
    wonders,mechanics=load_all_wonder_mechanics_data()
    resources=load_resources()
    metadata=json.loads((draft.ROOT/'data/index/modifier_localization.json').read_text(encoding='utf-8'))['modifiers']
    for category, samples in SAMPLES.items():
        group='独特工程' if category=='unique' else '通用工程'
        lines=['widget = { name = "compact_design" size = { 1530 1080 } background = { using = color_intense_bg_blue_texture }']
        for i,label in enumerate(('全部','入门','完整机制','独特工程','通用工程')):
            lines.append(f'button_regular = {{ position = {{ {20+i*300} 12 }} size = {{ 292 32 }} text = "{key(label)}" down = {"yes" if label==group else "no"} }}')
        count=sum(w['is_unique']==(category=='unique') for w in wonders)
        lines.append(text(f'{group} · {count} 项',40,52,600,24,font=14))
        lines.append(text(f'各列为等级总效果 · 仪式持续效果 {ritual_rules(mechanics)["memory_years"]} 年，一次性奖励另列',690,52,800,24,font=14,align='right'))
        snapshots=[]
        for i,target in enumerate(samples):
            wonder=next(w for w in wonders if w['key']==target)
            block,snapshot=entry(wonder,mechanics,resources.loc,metadata,i)
            lines.extend(block)
            snapshots.append(snapshot)
        lines.append(text('紧凑设计样稿 · 当前数据示例',40,1040,1450,24,font=14,align='right'))
        lines.append('}')
        gui='\n'.join(lines)
        # Only fixed-id, click-only navigation is allowed; content stays baked.
        static_gui=re.sub(r'onclick = "\[SelectLocation\(GetLocationByKey\(\'[a-z_]+\'\)\)\]"', '', gui)
        assert not any(token in static_gui for token in ('[','textcontext','datacontext'))
        assert all(isinstance(v,str) and '[' not in v for v in draft.draft_loc.values())
        assert all('建造条件' not in v for v in draft.draft_loc.values())
        path=OUT/f'compact_{category}.gui'
        path.write_text(gui,encoding='utf-8-sig')
        (OUT/f'compact_{category}_data.json').write_text(json.dumps(snapshots,ensure_ascii=False,indent=2),encoding='utf-8')
        scene=load_resources(extra_files=[path])
        scene.loc.d.update(draft.draft_loc)
        expander=Expander(scene.db)
        tree=build_target(scene.db,expander,'compact_design',path)
        entries={n.get('name'):n for n in draft.walk(tree) if n.get('name','').startswith('entry_')}
        assert len(entries)==3
        location_rows=[n for n in draft.walk(tree) if n.get('name','').startswith('location_reference_')]
        assert len(location_rows)==(3 if category=='unique' else 0)
        report=render_tree(tree,expander,scene,[],width=1530,height=1080,output=Path(f'compact_{category}.png'),
                           detail_elements=entries,metadata={'prototype_only':True,'static_content':True,'sample_count':3})
        assert not has_diagnostics(report), report
        for container in entries.values():
            for node in draft.walk(container):
                if node.kind=='textbox':
                    assert node.x >= container.x and node.x+node.w <= container.x+container.w+.1, node.props
                    assert node.y >= container.y and node.y+node.h <= container.y+container.h+.1, node.props
        print(f'{category}: three 300px entries; clean static render; {report["output"]}')
    (OUT/'compact_l_simp_chinese.yml').write_text('l_simp_chinese:\n'+'\n'.join(f' {k}:0 '+json.dumps(v,ensure_ascii=False) for k,v in draft.draft_loc.items())+'\n',encoding='utf-8-sig')


if __name__=='__main__':
    main()
