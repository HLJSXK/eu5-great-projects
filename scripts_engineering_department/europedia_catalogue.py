"""Bake compact Europedia entries; no game-state queries during display.

All names, effect descriptions, values, image geometry and location captions are
resolved at generation time. Only fixed-location click navigation is dynamic.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import struct
import unicodedata

from wonder_localization_lib import load_wonder_localization_data
from wonder_mechanics.modifiers import (
    authored_final_building_local_modifiers, wonder_base_country_modifiers,
    wonder_base_instant_effects, scale_numeric_modifier_mapping,
    merge_numeric_modifier_mappings,
)
from wonder_mechanics.rituals import ritual_styles, ritual_rules
from in_game.common.building_types.gen_tv_engineering_department_wonder_mechanics_buildings import (
    split_modifiers, merge_modifiers, fmt_value,
)

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ('english', 'simp_chinese')
LINE = re.compile(r'^\s*([\w.\-]+):\d*\s+"((?:[^"\\]|\\.)*)"')

# Explicit effect units, matching the one-shot effect vocabulary (not cost units).
REWARDS = {
    'all_estate_satisfaction': ('All estate satisfaction', '所有阶层满意度', True, True),
    'army_tradition': ('Army tradition', '陆军传统', False, True),
    'navy_tradition': ('Navy tradition', '海军传统', False, True),
    'diplomats': ('Diplomats', '外交官', False, True),
    'gold': ('Gold', '金币', False, True),
    'scaled_gold': ('Gold (scaled to economy)', '金币（按经济规模缩放）', False, True),
    'government_power': ('Government power', '政府权力值', False, True),
    'inflation': ('Inflation', '通货膨胀', True, False),
    'manpower': ('Manpower', '人力', False, True),
    'sailors': ('Sailors', '水手', False, True),
    'prestige': ('Prestige', '威望', False, True),
    'research_progress': ('Research progress', '研究进度', False, True),
    'ruler_adm': ('Ruler administrative ability', '统治者行政能力', False, True),
    'ruler_dip': ('Ruler diplomatic ability', '统治者外交能力', False, True),
    'ruler_mil': ('Ruler military ability', '统治者军事能力', False, True),
    'site_prosperity': ('Site prosperity', '所在地繁荣度', True, True),
    'stability': ('Stability', '稳定度', False, True),
}


def colored_number(value, percent=False, polarity='good') -> str:
    if isinstance(value, bool):
        raise TypeError('Boolean modifiers need a localized Yes/No value')
    number = float(value) * (100 if percent else 1)
    # Preserve small nonzero modifiers rather than rounding them to zero.
    rendered = f'{number:+.5f}'.rstrip('0').rstrip('.') + ('%' if percent else '')
    if polarity == 'neutral' or number == 0:
        return rendered
    positive = (number > 0) == (polarity == 'good')
    return f'#{"G" if positive else "R"} {rendered}#!'


def wrapped(value: str, width: int, font: int) -> tuple[str, int]:
    """Conservative offline wrapping shared by both source languages."""
    limit = width / font
    lines, current, used = [], '', 0.0
    for token in re.findall(r'[A-Za-z0-9_+%./-]+\s*|[^\x00-\x7f]|.', value):
        weight = sum(1 if unicodedata.east_asian_width(c) in ('W', 'F') else .62 for c in token)
        if current and used + weight > limit:
            lines.append(current.rstrip())
            current, used = '', 0.0
        current += token
        used += weight
    lines.append(current.rstrip())
    return '\n'.join(lines), len(lines)


class Catalogue:
    def __init__(self):
        self.loc: dict[str, tuple[str, str]] = {}
        self.sources = {}
        authored = load_wonder_localization_data()
        for language in LANGUAGES:
            values = {}
            base = ROOT/'.eu5-base/reference_game_files/game'
            for stage in ('main_menu',):
                for path in sorted((base/stage/'localization'/language).rglob('*.yml')):
                    for line in path.read_text(encoding='utf-8-sig').splitlines():
                        match = LINE.match(line)
                        if match:
                            values[match[1]] = match[2].replace('\\n', '\n').replace('\\"', '"')
            values.update(authored[language])
            self.sources[language] = values
        self.modifiers = json.loads((ROOT/'data/index/modifier_localization.json').read_text(encoding='utf-8'))['modifiers']

    def plain(self, language: str, value: str, seen=()) -> str:
        def substitute(match):
            alias = match[1]
            if alias in seen:
                raise ValueError(f'Circular static localization {seen + (alias,)}')
            return self.plain(language, self.sources[language][alias], seen + (alias,))
        value = re.sub(r'\$([\w.]+)\$', substitute, value)
        if '[' in value or '$' in value:
            raise ValueError(f'Live localization in static catalogue: {language}: {value}')
        return value

    def source(self, key: str) -> tuple[str, str]:
        return tuple(self.plain(lang, self.sources[lang][key]) for lang in LANGUAGES)

    def register(self, key: str, pair: tuple[str, str]) -> str:
        for value in pair:
            if '[' in value or '$' in value:
                raise ValueError(f'Dynamic catalogue text {key}: {value}')
        if key in self.loc and self.loc[key] != pair:
            raise ValueError(f'Conflicting catalogue text {key}')
        self.loc[key] = pair
        return key

    def text(self, lines, key, pair, x, y, width, height=24, font=15, gold=False, align='left', wrap=False):
        if wrap:
            pair = tuple(wrapped(v, width, font)[0] for v in pair)
        self.register(key, pair)
        kind = 'text_multi' if wrap else 'text_single'
        sizing = f'min_width = {width} max_width = {width} autoresize = yes' if wrap else f'size = {{ {width} {height} }} autoresize = no'
        style = 'using = Font_Type_Headers default_format = "#yellow_titles"' if gold else ''
        lines.append(f'{kind} = {{ position = {{ {x} {y} }} {sizing} fontsize = {font} align = {align}|nobaseline {style} text = "{key}" }}')

    def modifier_name(self, modifier):
        metadata = self.modifiers[modifier]
        return tuple(self.plain(lang, metadata[short]['name']) for lang, short in zip(LANGUAGES, ('en', 'zh')))

    def modifier_value(self, modifier, value):
        if isinstance(value, bool):
            return ('#G Yes#!', '#G 是#!') if value else ('#R No#!', '#R 否#!')
        metadata = self.modifiers[modifier]
        value = colored_number(value, metadata['value_kind'] == 'percent', metadata['color'])
        return (value, value)

    def reward(self, reward):
        en, zh, percent, good = REWARDS[reward['type']]
        value = colored_number(reward['value'], percent, 'good' if good else 'bad')
        return (en, zh), (value, value)

    def level_rows(self, wonder, mechanics):
        """Match the game's display modifiers, including raw/boolean semantics."""
        design = mechanics['buildings'][wonder['mechanic_key']]
        local, raw = split_modifiers(merge_modifiers(
            authored_final_building_local_modifiers(wonder, mechanics),
            include_local_cultural_baseline=design['include_local_cultural_baseline']))
        local = {k: float(fmt_value(v)) if isinstance(v, (int, float)) and not isinstance(v, bool) else v for k,v in local.items()}
        levels = []
        for level in range(1,7):
            site = merge_numeric_modifier_mappings(scale_numeric_modifier_mapping(local,level),raw)
            site = {k:v for k,v in site.items() if k not in {'local_cultural_tradition','local_cultural_influence'}}
            levels.append((wonder_base_country_modifiers(wonder,mechanics,level),site))
        rows = []
        for scope in (0,1):
            for modifier in levels[0][scope]:
                rows.append((('Nation','全国') if scope==0 else ('Local','当地'), self.modifier_name(modifier),
                             [self.modifier_value(modifier,level[scope][modifier]) for level in levels]))
        # Sparse instant base packages are separate from permanent modifiers.
        for index, reward in enumerate(wonder_base_instant_effects(wonder, mechanics)):
            values = [self.reward(wonder_base_instant_effects(wonder, mechanics, level)[index])[1] for level in range(1,7)]
            rows.append((('Once','一次'),self.reward(reward)[0],values))
        return rows

    def entry(self, wonder, mechanics, instance='catalogue'):
        wid = wonder['id']
        prefix = f'TV_EU_CATALOGUE_{wid}'
        identity = '_identity_default' if wonder.get('identity_variants') else ''
        rows = self.level_rows(wonder,mechanics)
        row_heights = [max(26, max(wrapped(v,268,14)[1] for v in row[1])*20) for row in rows]
        ritual_y = max(178, 40+27+sum(row_heights)+16)
        rituals = ritual_styles(wonder,mechanics)
        names = [self.source(r['name_key']+identity) for r in rituals]
        title_height = max(max(wrapped(v,318,16)[1] for v in pair)*23 for pair in names)
        effects = []
        for ritual in rituals:
            effect_rows = []
            for scope, values in ((('Nation','全国'),ritual['country_modifier']), (('Local','当地'),ritual['location_modifier_values'])):
                effect_rows += [(scope,self.modifier_name(k),self.modifier_value(k,v)) for k,v in values.items()]
            effect_rows += [(('Once','一次'),*self.reward(r)) for r in ritual['one_shot']]
            effects.append(effect_rows)
        heights = [[max(22,max(wrapped(v,244,14)[1] for v in row[1])*20) for row in group] for group in effects]
        ritual_height = max(110, 8+title_height+12+max(map(sum,heights))+10)
        height = max(300,ritual_y+ritual_height+12)
        lines = [f'tv_eu_catalogue_entry = {{ name = "tv_eu_{instance}_{wid}" size = {{ 1450 {height} }}']
        self.text(lines,prefix+'_NAME',self.source('game_concept_'+wonder['concept']+identity),46,2,880,28,19,True)
        size = {'small':('Small','小型'),'medium':('Medium','中型'),'large':('Large','大型')}[wonder['size']]
        category, pop = self.source(wonder['category']), self.source(wonder['pop_type'])
        self.text(lines,prefix+'_META',tuple(f'{size[i]} · {category[i]} · {pop[i]}' for i in range(2)),970,4,464,24,14,align='right')
        texture = f'gfx/interface/icons/towards_victory/wonders/{wonder.get("image", "tv_wonder_"+wonder["key"])}.dds'
        # Dimensions are in the fixed DDS header; generation need not decode
        # hundreds of original paintings or require an installed game.
        with (ROOT/'src/main_menu'/texture).open('rb') as art:
            header=art.read(20)
        if len(header)!=20 or header[:4]!=b'DDS ':
            raise ValueError(f'Invalid artwork DDS: {texture}')
        h,w=struct.unpack_from('<II',header,12)
        if not w or not h:
            raise ValueError(f'Empty artwork DDS: {texture}')
        scale=min(240/w,160/h)
        aw,ah=round(w*scale),round(h*scale)
        lines.append(f'widget = {{ position = {{ {16+(240-aw)//2} {42+(160-ah)//2} }} size = {{ {aw} {ah} }} background = {{ texture = "{texture}" }} }}')
        if wonder['is_unique']:
            location = self.source(wonder['location'])
            lines.append(f'button = {{ name = "location_reference_{wid}" position = {{ 16 224 }} size = {{ 240 48 }}')
            # GetLocationByKey is a Global promote, not a value-returning
            # function. End the chain with Location.Self for the callback arg.
            lines.append(f'onclick = "[SelectLocation(GetLocationByKey(\'{wonder["location"]}\').Self)]"')
            tip=self.register(prefix+'_LOCATION',location)
            lines.append(f'tooltip = "{tip}"')
            lines.append(icon('gfx/interface/icons/map_subdivisons/location.dds',8,8,32))
            self.text(lines,prefix+'_LOCATION_LINK',tuple('#L '+v+'#!' for v in location),48,8,184,32,16)
            # Clicks belong to the button rather than its text child.
            lines[-1]=lines[-1].replace('text_single = {','text_single = { alwaystransparent = yes',1)
            lines.append('}')
        self.text(lines,'TV_EU_CATALOGUE_LEVELS',('Total effects by level','各等级总效果'),290,40,310,24,14,True)
        for index, roman in enumerate(('I','II','III','IV','V','VI')):
            self.text(lines,f'TV_EU_CATALOGUE_LEVEL_{index+1}',(roman,roman),612+137*index,40,137,24,15,True,'center')
        y=67
        for ri,((scope,label,values),row_height) in enumerate(zip(rows,row_heights),1):
            lines.append(rule(282,y,1152))
            self.text(lines,prefix+f'_B{ri}_SCOPE',scope,290,y+2,44,24,11,True)
            self.text(lines,prefix+f'_B{ri}_LABEL',label,340,y+2,268,font=14,wrap=True)
            for ci,value in enumerate(values,1):
                self.text(lines,prefix+f'_B{ri}_L{ci}',value,612+137*(ci-1),y+2,137,24,15,align='center')
            y+=row_height
        if not rows:
            self.text(lines,'TV_EU_CATALOGUE_NO_BASE',('No base modifiers','无基础修正'),290,70,600,24,14)
        for i,(ritual,name,group,rheights) in enumerate(zip(rituals,names,effects,heights),1):
            lines.append(f'widget = {{ name = "ritual_{wid}_{i}" position = {{ {282+(i-1)*390} {ritual_y} }} size = {{ 372 {ritual_height} }} using = bg_paper_card')
            axis=ritual['societal_value']; side='left' if axis['sign']<0 else 'right'
            lines.append(icon(f'gfx/interface/icons/societal_values/{axis["axis"]}_{side}.dds',10,8,26))
            self.text(lines,prefix+f'_R{i}_NAME',name,44,8,318,font=16,gold=True,wrap=True)
            lines.append(rule(10,8+title_height+6,352))
            y=8+title_height+12
            for j,((scope,label,value),rh) in enumerate(zip(group,rheights),1):
                self.text(lines,prefix+f'_R{i}_{j}_SCOPE',scope,10,y,34,22,10,True)
                self.text(lines,prefix+f'_R{i}_{j}_LABEL',label,48,y,244,font=14,wrap=True)
                self.text(lines,prefix+f'_R{i}_{j}_VALUE',value,292,y,70,22,14,align='right')
                y+=rh
            lines.append('}')
        lines.append('}')
        return lines

    def tab(self, category, wonders, mechanics):
        lines=[f'vbox = {{ name = "tv_eu_catalogue_{category}" visible = "[GetVariableSystem.HasValue(\'tv_encyclopedia_filter\', \'{category}\')]"',
               'layoutpolicy_horizontal = expanding spacing = 12 margin = { 0 10 }']
        label=('Unique Projects','独特工程') if category=='unique' else ('Generic Projects','通用工程')
        lines.append('widget = { size = { 1450 30 }')
        self.text(lines,'TV_EU_CATALOGUE_COUNT_'+category.upper(),tuple(f'{v} · {len(wonders)}' for v in label),0,0,400,24,14)
        years=ritual_rules(mechanics)['memory_years']
        self.text(lines,'TV_EU_CATALOGUE_NOTE',
                  (f'Level totals · Ritual modifiers last {years} years; one-time rewards are marked Once',f'各列为等级总效果 · 仪式持续效果 {years} 年，一次性奖励另列'),400,0,1050,24,14,align='right')
        lines.append('}')
        for wonder in wonders:
            lines.extend(self.entry(wonder,mechanics))
        lines.append('}')
        return lines


def icon(texture,x,y,size):
    return f'icon = {{ position = {{ {x} {y} }} size = {{ {size} {size} }} texture = "{texture}" alwaystransparent = yes }}'


def rule(x,y,width):
    return f'icon = {{ position = {{ {x} {y} }} size = {{ {width} 1 }} using = color_gold_texture alpha = 0.2 }}'
