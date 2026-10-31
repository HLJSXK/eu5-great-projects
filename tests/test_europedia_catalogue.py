"""Static catalogue contract: current data, no load-time effect evaluation."""
import re
import json
from pathlib import Path

import pytest

from scripts_engineering_department.europedia_render import Catalogue
from scripts_engineering_department.europedia_content import CARDS
from scripts_engineering_department.wonder_mechanics.io import load_all_wonder_mechanics_data
from scripts_engineering_department.vanilla_takeover.parse import parse

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('card', CARDS, ids=lambda card: card['id'])
def test_each_teaching_card_is_a_complete_gui_block(card):
    from great_projects_editor_web.services.artifacts import _validate_script
    from scripts_engineering_department.europedia_render import render_content_card

    lines, _ = render_content_card(card)
    text = '\n'.join(lines)
    _validate_script(text.encode('utf-8-sig'), Path('card.gui'))
    nodes = parse(text)
    assert len(nodes) == 1
    assert nodes[0].key == 'vbox'


def test_getting_started_teaches_with_native_anatomy_rows():
    """Getting Started draws the panel's controls natively, one numbered row per sentence.

    The tab used to show baked screenshots of the panel. Those are gone: a bitmap cannot follow
    a translation, and it cannot point at the control it is explaining. Each step now carries a
    numbered anatomy block instead, so this test pins that structure and the rules that make it
    safe -- every mock label is a shipped panel key, and nothing in the tab fires an action.
    """
    from scripts_engineering_department.europedia_content import CARDS
    from scripts_engineering_department.europedia_render import ANATOMY_PANEL_TITLES

    # The shapes europedia_render.render_mock knows how to draw.
    mock_kinds = {
        'status', 'portrait', 'button', 'buttons', 'pills', 'bar', 'demands', 'triplet',
        'stats', 'stats_goods', 'equation', 'parts', 'stat', 'styles',
    }

    card = CARDS[0]
    guides = [section for section in card['sections'] if section['kind'] == 'guide']
    assert len(guides) == 7
    for section in guides:
        assert section['anatomy'] in ANATOMY_PANEL_TITLES
        assert section['body']
        rows = section['rows']
        assert rows, section['title']
        # A step is a teaching device only if most of it is a control, not prose.
        asserted = [row for row in rows if row.get('mock') is not None]
        assert len(asserted) >= len(rows) - 1, section['title']
        for row in rows:
            assert row['title'] and row['text']
            mock = row.get('mock')
            if mock is not None:
                assert isinstance(mock, tuple) and mock[0] in mock_kinds, (section['title'], mock)

    def language_keys(language: str) -> set[str]:
        """Every key the language ships, wherever the file lives: panel keys are not Europedia keys."""
        folder = ROOT / 'src/main_menu/localization' / language
        return {
            match.group(1)
            for path in folder.rglob('*.yml')
            for line in path.read_text(encoding='utf-8-sig').splitlines()
            if (match := re.match(r'^\s*([\w.\-]+):\d*\s+"', line))
        }

    shipped = {language: language_keys(language) for language in ('english', 'german')}

    for relative in (
        'data/generated_fragments/tv_encyclopedia_wonders_cards.gui',
        'src/in_game/gui/encyclopedia_lateralview.gui',
        'submods/tv_prosper_or_perish_compat/in_game/gui/encyclopedia_lateralview.gui',
    ):
        gui = (ROOT / relative).read_text(encoding='utf-8-sig')
        overview = gui.split('name = "tv_eu_overview_guide_1"', 1)[1].split('TV_EU_DEPARTMENT_TITLE', 1)[0]
        # One anatomy block per step, each with its numbered rows.
        assert overview.count('tv_eu_anatomy = {') == 7
        assert overview.count('tv_eu_anatomy_row = {') == sum(len(s['rows']) for s in guides)
        for number in range(1, 8):
            assert f'name = "tv_eu_overview_guide_{number}"' in gui
        # The seven project steps follow a clockwise ring; detailed lessons stay below it.
        assert 'name = "tv_eu_overview_cycle"' in gui
        assert gui.count('tv_eu_cycle_step = {') == 7
        assert 'tv_eu_overview_index' not in gui
        assert 'tv_eu_index_step = {' not in gui
        assert 'gfx/interface/illustrations/tv_europedia_cycle.dds' in gui
        assert (ROOT/'src/main_menu/gfx/interface/illustrations/tv_europedia_cycle.dds').is_file()
        assert 'europedia_ui/' not in gui
        # The tab explains the panel; it never calls into it or evaluates game state.
        assert 'scripted_action_tooltip' not in overview
        assert 'InternationalOrganizationsView' not in overview
        assert 'ShowScriptedEffectForScope' not in overview
        assert 'ShowTriggerConditionsForScope' not in overview
        assert 'tv_eu_choice = {' not in overview
        assert 'TV_EU_GUIDE_UI_LANGUAGE' not in overview
        # Every mock label is a panel key that already ships in all 11 languages, so a mock can
        # never introduce English-only prose into the middle of a translated page.
        for mock_key in set(re.findall(r'text = "(TV_[A-Z0-9_]+)"', overview)):
            for language, keys in shipped.items():
                assert mock_key in keys, f'{language} is missing panel key {mock_key}'


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
