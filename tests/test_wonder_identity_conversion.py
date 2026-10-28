"""Identity conversion preserves the engineering instance and native event contract."""
from copy import deepcopy
from pathlib import Path
import re

import pytest

from scripts_engineering_department.wonder_mechanics import _core as core
from scripts_engineering_department.wonder_localization_lib import (
    load_wonder_localization_data, collapse_wonder_localization_data, load_yaml,
    WONDER_LOCALIZATION_FILE,
    engineering_department_wonder_mechanics_localization_map,
)
from scripts_engineering_department.vanilla_takeover.parse import parse, walk, Source, REFERENCE
from scripts_engineering_department.in_game.common.scripted_effects.gen_tv_wonder_identity_effects import outputs

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'src'
PREFIX = 'tv_wonder_unique_hagia_sophia_mosque'


@pytest.fixture(scope='module')
def wonder():
    return next(w for w in core.load_all_wonder_mechanics()[0] if w['id'] == 102)


@pytest.mark.parametrize('damage', ['missing_style', 'missing_translation', 'unknown_field', 'duplicate', 'bad_state', 'negative_cost', 'empty_trigger'])
def test_identity_schema_rejects_incomplete_data(wonder, damage):
    variants = deepcopy(wonder['identity_variants'])
    v = variants[0]
    if damage == 'missing_style': v['ritual_text'].pop(3)
    elif damage == 'missing_translation': v['ritual_text'][1].pop('desc_zh')
    elif damage == 'unknown_field': v['building'] = 'second_building'
    elif damage == 'duplicate': variants.append(deepcopy(v))
    elif damage == 'bad_state': v['global_variable'] = 'scope:invalid'
    elif damage == 'negative_cost': v['cost_scale'] = -1
    else: v['eligible_script'] = ''
    with pytest.raises((ValueError, TypeError)):
        core.validate_identity_variants(variants, 'test.identity_variants')


def nodes_in(text):
    return [node for root in parse(text) for node, _ in walk(root)]


def test_conversion_never_writes_building_levels_and_resynchronizes_next_day(wonder):
    generated = outputs()
    keys = {n.key for text in generated.values() for n in nodes_in(text)}
    assert not keys & {'construct_building', 'destroy_building_forcefully', 'change_building_level_in_location'}
    assert wonder['final_building'] == 'tv_wonder_unique_hagia_sophia_inaugurated'
    assert sum(w['location'] == 'constantinople' for w in core.load_unique_wonders()) == 3
    effect = generated['in_game/common/scripted_effects/tv_wonder_identity_effects.txt']
    assert 'tv_wonder_unique_hagia_sophia_ritual_revoke_effect = yes' in effect
    delayed = next(n for n in nodes_in(effect) if n.key == 'trigger_event_silently')
    assert delayed.scalar('id') == 'tv_engineering_department.9502'
    assert delayed.scalar('days') == '1'


def test_decision_checks_ownership_religion_completed_building_and_active_project_twice():
    text = outputs()['in_game/common/decisions/tv_wonder_identity_decisions.txt']
    decision = parse(text)[0]
    allow = decision.child('allow')
    option = decision.child('option')
    guard = option.child('effect').child('if').child('limit')
    signature = lambda node: (node.key, node.op, node.value, tuple(signature(c) for c in node.children))
    assert signature(allow)[3] == signature(guard)[3]
    assert 'var:tv_wonder_stage ?= { this >= 3 }' in text
    for required in ('owns', 'location:constantinople', 'religion.group', 'NOT', 'gold'):
        assert allow.child(required) is not None
    cost = [n for n in nodes_in(text) if n.key == 'change_gold_effect']
    assert len(cost) == 1 and cost[0].scalar('scale') == '-1.2'
    assert len([n for n in nodes_in(text) if n.key == 'add_prestige']) == 1
    assert decision.child('ai_will_do').scalar('value') == '0'


def test_vanilla_event_keeps_its_cost_rewards_and_both_original_options(wonder):
    spec = wonder['identity_variants'][0]['vanilla_event']
    original = next(n for n in Source.read(REFERENCE / spec['path']).definitions if n.key == spec['id'])
    patched = next(n for n in parse(outputs()['in_game/events/0000_tv_wonder_identity_events.txt']) if n.key == spec['id'])
    old_options = [n for n in original.children if n.key == 'option']
    new_options = [n for n in patched.children if n.key == 'option']
    signature = lambda node: (node.key, node.op, node.value, tuple(signature(c) for c in node.children))
    assert len(new_options) == len(old_options) == 2
    guarded = new_options[0].child('if')
    original_effects = [n for n in old_options[0].children if n.key != 'name']
    new_effects = [n for n in guarded.children if n.key not in ('limit', 'hidden_effect')]
    assert [signature(n) for n in new_effects] == [signature(n) for n in original_effects]
    assert guarded.child('hidden_effect').child(PREFIX + '_changed_effect')
    assert new_options[0].child('trigger')
    assert any(n.key == 'has_global_variable' and n.value == 'hagia_sophia_now_mosque'
               for n, _ in walk(guarded.child('limit')))
    assert signature(old_options[1]) == signature(new_options[1])


def test_restoration_does_not_depend_on_the_already_removed_native_flag():
    text = outputs()['in_game/common/on_action/tv_wonder_identity_on_action.txt']
    callbacks = parse(text)
    religion = next(n for n in callbacks if n.key == PREFIX + '_religion_changed')
    assert 'has_global_variable' not in {n.key for n, _ in walk(religion)}
    assert 'has_variable' in {n.key for n, _ in walk(religion)}
    assert 'tv_wonder_unique_hagia_sophia_ritual_revoke_effect' in {n.key for n, _ in walk(religion)}
    ownership = next(n for n in callbacks if n.key == PREFIX + '_owner_changed')
    assert 'remove_variable' in {n.key for n, _ in walk(ownership)}
    bridges = (MOD / 'in_game/common/on_action/tv_engineering_department_pulse_bridges.txt').read_text(encoding='utf-8-sig')
    assert PREFIX + '_religion_changed' in bridges
    assert PREFIX + '_owner_changed' in bridges


def test_localization_switches_without_context_and_editor_round_trip_preserves_authored_text():
    expanded = load_wonder_localization_data()
    authored = load_yaml(WONDER_LOCALIZATION_FILE)['wonder_localization']
    collapsed = collapse_wonder_localization_data(expanded)
    for language, values in expanded.items():
        for key in ('game_concept_tv_wonder_display_102', 'game_concept_tv_wonder_unique_hagia_sophia_desc',
                    'TV_WONDER_RITUAL_NAME_1_102', 'TV_WONDER_RITUAL_DESC_3_102'):
            text = values[key]
            assert "GetGlobalVariable('hagia_sophia_now_mosque').IsSet" in text
            for target in re.findall(r"'(\w+_identity_\w+)'", text):
                assert values[target] and target != key
        assert values['tv_wonder_unique_hagia_sophia_inaugurated'] == authored[language]['tv_wonder_unique_hagia_sophia_inaugurated']
        for key in ('tv_wonder_unique_hagia_sophia', 'tv_wonder_unique_hagia_sophia_desc', 'game_concept_tv_wonder_unique_hagia_sophia_desc'):
            assert collapsed[language][key] == authored[language][key]
        assert not any('_identity_' in key for key in collapsed[language])
        rendered = engineering_department_wonder_mechanics_localization_map(language, values)
        key = 'tv_engineering_department.500.d_unique_hagia_sophia_1'
        assert '#weak ' in rendered[key]
        assert '#weak ' not in rendered[key + '_identity_mosque']
        assert '#weak ' not in rendered[key + '_identity_default']


def test_identity_images_use_registered_texture_handles_and_real_assets():
    concepts = (MOD / 'main_menu/common/game_concepts/tv_engineering_department_wonder_mechanics_concepts.txt').read_text(encoding='utf-8-sig')
    for kind in ('image', 'full_image'):
        assert f'tv_wonder_identity_{kind}_102_mosque = ' in concepts
    for filename in ('location_window.gui', 'panels/organization/tv_engineering_department.gui'):
        text = (MOD / 'in_game/gui' / filename).read_text(encoding='utf-8-sig')
        assert "GetConceptTexture(Select_CString(" in text
        assert "GetGlobalVariable('hagia_sophia_now_mosque').IsSet" in text
    # Europedia's two approved examples exclude Hagia Sophia; live gameplay
    # panels must still retain its dynamic identity and registered image handles.
    encyclopedia = (MOD / 'in_game/gui/encyclopedia_lateralview.gui').read_text(encoding='utf-8-sig')
    assert 'game_concept_tv_wonder_unique_hagia_sophia' not in encyclopedia
    image_tasks = core.load_wonder_image_tasks()
    assert len([t for t in image_tasks if t['key'] == 'unique_hagia_sophia_mosque']) == 1
    for suffix in ('', '_cropped'):
        path = MOD / 'main_menu/gfx/interface/icons/towards_victory/wonders' / f'tv_wonder_unique_hagia_sophia_mosque{suffix}.dds'
        assert path.read_bytes()[:4] == b'DDS '
