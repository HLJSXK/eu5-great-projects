"""Static catalogue contract: current data, no load-time effect evaluation."""
import re
from pathlib import Path

import pytest

from scripts_engineering_department.europedia_render import Catalogue
from scripts_engineering_department.wonder_mechanics.io import load_all_wonder_mechanics_data
from scripts_engineering_department.vanilla_takeover.parse import parse

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def source():
    return Catalogue(), *load_all_wonder_mechanics_data()


def test_every_level_matches_shipped_modifier_definitions(source):
    catalogue,wonders,mechanics=source
    path=ROOT/'src/in_game/common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt'
    definitions={node.key:node for node in parse(path.read_text(encoding='utf-8-sig'))}
    for wonder in wonders:
        for level in range(1,7):
            expected=[]
            for scope,infix in (('Nation',''),('Local','local_')):
                node=definitions[f'tv_wonder_display_{wonder["id"]}_{infix}level_{level}']
                for item in node.children:
                    if item.key=='game_data':
                        continue
                    value={'yes':True,'no':False}.get(item.value)
                    if value is None:
                        value=float(item.value)
                    expected.append((scope,catalogue.modifier_name(item.key),catalogue.modifier_value(item.key,value)))
            rows=catalogue.level_rows(wonder,mechanics)
            actual=[(scope[0],label,values[level-1]) for scope,label,values in rows if scope[0]!='Once']
            assert actual==expected, (wonder['key'],level)


def test_catalogue_only_queries_a_location_on_click(source):
    catalogue,wonders,mechanics=source
    for wonder in wonders:
        gui='\n'.join(catalogue.entry(wonder,mechanics))
        clicks=re.findall(r'onclick = "([^"\n]+)"',gui)
        expected=[f"[SelectLocation(GetLocationByKey('{wonder['location']}').Self)]"] if wonder['is_unique'] else []
        assert clicks==expected
        rest=re.sub(r'onclick = "[^"\n]+"','',gui)
        assert '[' not in rest and 'textcontext' not in rest and 'datacontext' not in rest
        assert 'conditions_' not in gui
    assert all('[' not in value and '$' not in value for pair in catalogue.loc.values() for value in pair)


def test_fixed_location_callbacks_use_a_value_accessor_in_all_generated_consumers(source):
    # The native loader rejects a promote alone as SelectLocation's argument.
    # Unlike Siege.GetLocation, GetLocationByKey has no Function overload.
    api = (ROOT / '.eu5-base/reference_official_defines/docs/data_types_uncategorized.txt').read_text(encoding='utf-8-sig')
    assert 'GetLocationByKey( Arg0 )\nDefinition type: Global promote\nReturn type: Location' in api
    assert 'GetLocationByKey( Arg0 )\nDefinition type: Global function' not in api
    assert 'Location.Self\nDefinition type: Function' in api
    locations = {wonder['location'] for wonder in source[1] if wonder['is_unique']}
    for relative in (
        'data/generated_fragments/tv_encyclopedia_wonders_cards.gui',
        'src/in_game/gui/encyclopedia_lateralview.gui',
        'submods/tv_prosper_or_perish_compat/in_game/gui/encyclopedia_lateralview.gui',
    ):
        gui = (ROOT / relative).read_text(encoding='utf-8-sig')
        assert not re.search(r'SelectLocation\(GetLocationByKey\([^)]*\)\)', gui), relative
        callbacks = re.findall(r"SelectLocation\(GetLocationByKey\('([^']+)'\)\.Self\)", gui)
        assert set(callbacks) == locations, relative
        assert len(callbacks) == gui.count('SelectLocation('), relative


def test_boolean_unlock_and_raw_local_modifier_do_not_stack(source):
    catalogue,wonders,mechanics=source
    wonder=next(w for w in wonders if w['key']=='mobile_fortress')
    rows=catalogue.level_rows(wonder,mechanics)
    label=catalogue.modifier_name('can_recruit_regiment_in_this_location')
    values=next(values for _,name,values in rows if name==label)
    assert values==[('#G Yes#!','#G 是#!')]*6


def test_live_localization_is_rejected(source):
    catalogue=source[0]
    with pytest.raises(ValueError,match='Live localization'):
        catalogue.plain('english',"[ShowModifierEffect('a')]")
    with pytest.raises(ValueError,match='Dynamic catalogue'):
        catalogue.register('TEST',('static',"[Player.GetName]"))


def test_generated_source_language_keys_match():
    def read(language):
        data=(ROOT/f'src/main_menu/localization/{language}/tv_europedia_l_{language}.yml').read_bytes()
        assert data.startswith(b'\xef\xbb\xbf')
        return set(re.findall(r'^ (TV_EU_CATALOGUE_\w+):',data.decode('utf-8-sig'),re.M))
    assert read('english')==read('simp_chinese')
    assert len(read('english'))>1000
