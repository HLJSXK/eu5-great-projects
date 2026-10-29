"""Regressions for ED startup error groups observed on 2026-10-23.

Execute the relevant generated conditions with missing maps, and validate the
expanded building references and display-definition closure. This is a small
script subset, not a simulation of the game's events or modifier application.
"""
from dataclasses import replace
from pathlib import Path
import re

import pytest

from scripts_engineering_department.wonder_mechanics.io import load_all_wonder_mechanics
from test_wonder_priority_proposals import child, parse, source_blocks, walk


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'src/in_game'


def test_engineering_ai_actions_are_inside_the_actions_list_and_resolve():
    lists = source_blocks('common/generic_action_ai_lists/tv_engineering_department_list.txt')
    group = lists['tv_engineering_department_list']
    assert {node.key for node in group} == {'potential', 'actions'}, 'Action ids must be inside actions = { ... }'
    entries = child(group, 'actions').children
    assert all(not node.op and not node.children for node in entries)
    names = [node.key for node in entries]
    assert len(names) == len(set(names)), 'Duplicate action in the AI list'
    rituals = {'tv_wonder_ritual_preview_1', 'tv_wonder_ritual_preview_2', 'tv_wonder_ritual_preview_3',
               'tv_wonder_ritual_confirm', 'tv_wonder_ritual_choose_plain', 'tv_wonder_ritual_cancel_reritual'}
    assert rituals <= set(names)
    definitions = {node.key for path in (GAME/'common/generic_actions').glob('*.txt')
                   for node in parse(path.read_text(encoding='utf-8-sig')) if node.children}
    assert set(names) <= definitions, 'AI list refers to an undefined action'


def expand(nodes, parameters):
    def substitute(text):
        return re.sub(r'\$([a-z_]+)\$', lambda m: str(parameters[m[1]]), text)
    return tuple(replace(n, key=substitute(n.key), value=(expand(n.children, parameters)
                 if isinstance(n.value, tuple) else substitute(n.value))) for n in nodes)


def evaluate(nodes, *, maps, definitions=None, human=True, unlimited=False):
    """Evaluate conditions eagerly; only explicit trigger branches guard reads."""
    results, matched = [], False
    for n in nodes:
        if n.key in ('trigger_if', 'trigger_else_if'):
            if n.key == 'trigger_if': matched = False
            if not matched and evaluate(child(n.children, 'limit').children, maps=maps,
                                        definitions=definitions, human=human, unlimited=unlimited):
                matched = True
                results.append(evaluate(tuple(c for c in n.children if c.key != 'limit'), maps=maps,
                                        definitions=definitions, human=human, unlimited=unlimited))
            continue
        if n.key == 'trigger_else':
            if not matched:
                results.append(evaluate(n.children, maps=maps, definitions=definitions,
                                        human=human, unlimited=unlimited))
            continue
        if n.key == 'NOT':
            result = not evaluate(n.children, maps=maps, definitions=definitions,
                                  human=human, unlimited=unlimited)
        elif n.key == 'has_variable_map': result = n.value in maps
        elif n.key == 'is_key_in_variable_map':
            # Deliberately fail on a missing map, as the engine diagnostic does.
            result = int(child(n.children, 'target').value) in maps[child(n.children, 'name').value]
        elif n.key.startswith('variable_map('):
            name, key = n.key[len('variable_map('):-1].split('|')
            if n.children:
                comparison = child(n.children, 'this')
                assert comparison.op == '>='
                result = maps[name][int(key)] >= int(comparison.value)
            else:
                result = maps[name][int(key)] == int(n.value)
        elif n.key == 'owner':
            result = evaluate(n.children, maps=maps, definitions=definitions, human=human, unlimited=unlimited)
        elif n.key == 'is_ai': result = (not human) == (n.value == 'yes')
        elif n.key == 'has_global_variable':
            assert n.value == 'tv_engineering_department_unlimited_scale'
            result = unlimited
        elif n.key in ('always', 'has_building'): result = n.value == 'yes' or n.key == 'has_building'
        elif definitions and n.key in definitions:
            parameters = {c.key: c.value for c in n.children}
            result = evaluate(expand(definitions[n.key], parameters), maps=maps, definitions=definitions,
                              human=human, unlimited=unlimited)
        else: raise AssertionError(f'Unsupported condition: {n}')
        results.append(result)
    return all(results)


@pytest.fixture(scope='module')
def wonders():
    return load_all_wonder_mechanics()[0]


def test_level_helpers_do_not_add_a_second_type_prefix():
    effects = source_blocks('common/scripted_effects/tv_wonder_level_change_effects.txt')
    helpers = {'tv_wonder_raise_final_building_level_effect', 'tv_wonder_lower_final_building_level_effect',
               'tv_wonder_found_final_building_level_effect'}
    checked = 0
    for body in effects.values():
        for call in walk(body):
            if call.key not in helpers: continue
            parameters = {n.key: n.value for n in call.children}
            assert parameters['building'].startswith('building_type:tv_wonder_')
            for node in walk(expand(effects[call.key], parameters)):
                if node.key == 'location_building_level':
                    assert child(node.children, 'building_type').value == parameters['building']
                    checked += 1
    assert checked > 1000


def test_scale_limits_handle_missing_other_and_recorded_survey_keys(wonders):
    definitions = source_blocks('common/scripted_triggers/tv_wonder_level_change_triggers.txt')
    shared = source_blocks('common/scripted_triggers/tv_engineering_department_triggers.txt')[
        'tv_wonder_location_scale_allows_level_trigger']
    name = 'tv_wonder_survey_scale_tier'
    for w in wonders:
        wid = w['id']
        for requested in range(1, 8):
            condition = expand(shared, {'wonder_id': wid, 'level': requested})
            for maps in ({}, {name: {}}, {name: {999: 1}}):
                assert evaluate(condition, maps=maps, definitions=definitions)
            for tier in range(1, 7):
                maps = {name: {wid: tier}}
                assert evaluate(condition, maps=maps, definitions=definitions) == (requested <= tier)
                assert evaluate(condition, maps=maps, definitions=definitions, unlimited=True)
                assert evaluate(condition, maps=maps, definitions=definitions, human=False, unlimited=True) == (requested <= tier)
    # Quoted map expressions must have literal/runtime keys, never template arguments.
    for path in (GAME/'common').rglob('*.txt'):
        assert not re.search(r'"(?:global_|local_)?variable_map\([^"\n]*\$', path.read_text(encoding='utf-8-sig')), path


def test_location_display_reset_initializes_empty_slots_and_clears_previous_ritual():
    effects = source_blocks('common/scripted_effects/tv_wonder_location_display_effects.txt')
    reset = effects['tv_wonder_mechanics_clear_location_display_state_effect']
    fields = {
        f'tv_wonder_{group}_slot_{slot}_{suffix}'
        for group, count in (('display', 3), ('tooltip', 5))
        for slot in range(1, count + 1)
        for suffix in ('level', 'ritual_style', 'ritual_completed')
    } | {'tv_wonder_tooltip_overflow_count'}

    def apply_scalars(nodes, state):
        for node in nodes:
            if node.key == 'remove_variable':
                state.pop(node.value, None)
            elif node.key == 'set_variable':
                state[child(node.children, 'name').value] = int(child(node.children, 'value').value)
            else:
                raise AssertionError(f'Unexpected reset/push operation: {node.key}')

    state = {}
    for style in (1, 2, 3, 0, -1):
        apply_scalars(reset, state)
        assert {key: state[key] for key in fields} == dict.fromkeys(fields, 0)
        assert not any(key.endswith('_id') and '_slot_' in key for key in state)
        # Populate the first slot using the shipped push body, then clear it on
        # the next iteration: re-dedication, plain completion and shell reuse.
        for group in ('display', 'tooltip'):
            branch = effects[f'tv_wonder_mechanics_push_location_{group}_slot_effect'][0]
            body = expand(tuple(n for n in branch.children if n.key != 'limit'), {
                'wonder_id': 3, 'wonder_level': 6,
                'wonder_ritual_style': style, 'wonder_ritual_completed': int(style > 0),
            })
            apply_scalars(body, state)
            assert state[f'tv_wonder_{group}_slot_1_ritual_style'] == style
        state['tv_wonder_tooltip_overflow_count'] = 4
    apply_scalars(reset, state)
    assert all(state[key] == 0 for key in fields)

    refresh = 'tv_wonder_mechanics_refresh_location_display_state_effect'
    world = 'tv_wonder_mechanics_refresh_world_location_display_state_effect'
    assert effects[refresh][0].key == 'tv_wonder_mechanics_clear_location_display_state_effect'
    assert child(effects[world], 'every_location_in_the_world').children[0].key == refresh
    hooks = source_blocks('common/on_action/tv_engineering_department_on_action.txt')
    bridges = source_blocks('common/on_action/tv_engineering_department_pulse_bridges.txt')
    for phase in ('start', 'load'):
        callback = f'tv_wonder_initialize_location_display_state_on_game_{phase}'
        assert callback in {n.key for n in walk(bridges[f'on_game_{phase}'])}
        assert world in {n.key for n in walk(hooks[callback])}


def test_all_local_display_references_resolve_to_level_scaled_definitions(wonders):
    hidden_cultural_modifiers = {'local_cultural_tradition', 'local_cultural_influence'}
    effects = source_blocks('common/scripted_effects/tv_wonder_location_display_effects.txt')
    refs = {child(n.children, 'modifier').value for n in walk(
        effects['tv_wonder_mechanics_reference_display_modifiers_effect']) if n.key == 'add_location_modifier'}
    modifiers = source_blocks('common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt')
    assert len(refs) == 195 * 6
    assert refs <= modifiers.keys()
    buildings = source_blocks('common/building_types/tv_engineering_department_wonder_mechanics_buildings.txt')
    for w in wonders:
        building = buildings[w['final_building']]
        # Cultural bonuses still belong to the building, but are hidden in previews.
        base = {n.key: float(n.value) for n in child(building, 'modifier').children
                if n.key.startswith('local_') and n.key not in hidden_cultural_modifiers}
        raw = next((n.children for n in building if n.key == 'raw_modifier'), ())
        for level in range(1, 7):
            body = modifiers[f"tv_wonder_display_{w['id']}_local_level_{level}"]
            assert child(child(body, 'game_data').children, 'category').value == 'location'
            assert hidden_cultural_modifiers.isdisjoint(n.key for n in body)
            for key, value in base.items():
                assert float(child(body, key).value) == pytest.approx(value * level, abs=0.0005)
            for node in raw:
                assert float(child(body, node.key).value) == float(node.value)


@pytest.mark.parametrize('style', [None, 1, 2, 3])
def test_ritual_membership_and_expiry_safely_handle_absent_maps(style):
    state = source_blocks('common/scripted_effects/tv_wonder_ritual_state_effects.txt')
    membership = child(state['tv_wonder_ritual_revoke_location_effect'][0].children, 'limit').children
    expiry = source_blocks('events/tv_wonder_ritual_lifecycle_events.txt')['tv_engineering_department.3001']
    expires = child(child(child(expiry, 'immediate').children, 'if').children, 'limit').children
    maps = {} if style is None else {'tv_wonder_ritual_style_by_id': {1: style}}
    assert evaluate(membership, maps=maps) == (style is not None)
    assert evaluate(expires, maps=maps) == (style is not None)
    sync = state['tv_wonder_sacred_mountain_ritual_sync_country_effect']
    for expected, branch in enumerate((n for n in sync if n.key == 'if'), 1):
        conditions = child(child(branch.children, 'limit').children, 'any_owned_location').children
        assert evaluate(conditions, maps=maps) == (style == expected)
    maps['tv_wonder_ritual_memory_by_id'] = {1: 1}
    assert not evaluate(expires, maps=maps)
    maps['tv_wonder_ritual_memory_by_id'] = {2: 1}
    assert evaluate(expires, maps=maps) == (style is not None)


def test_map_queries_are_guarded_in_all_ritual_and_cache_paths():
    protected = {'tv_wonder_ritual_style_by_id', 'tv_wonder_ritual_memory_by_id',
                 'tv_wonder_plain_level_by_wonder_id', 'tv_wonder_auto_level_by_wonder_id'}
    checked = 0

    def inspect(nodes, guarded=frozenset()):
        nonlocal checked
        for n in nodes:
            if n.key == 'is_key_in_variable_map':
                name = child(n.children, 'name').value
                if name in protected:
                    assert name in guarded, f'Lookup can run before map creation: {name}'
                    checked += 1
            if n.key in ('trigger_if', 'trigger_else_if'):
                limit = child(n.children, 'limit').children
                inspect(limit, guarded)
                available = {c.value for c in limit if c.key == 'has_variable_map'}
                inspect(tuple(c for c in n.children if c.key != 'limit'), guarded | available)
            else: inspect(n.children, guarded)

    for directory in ('common/scripted_effects', 'common/scripted_triggers', 'events'):
        for path in (GAME/directory).glob('*.txt'):
            if any(name in path.read_text(encoding='utf-8-sig') for name in protected):
                inspect(parse(path.read_text(encoding='utf-8-sig')))
    assert checked > 1000


def test_building_edits_regenerate_the_local_display_definitions():
    from great_projects_editor_web.services.wonder_generation import wonder_generation_plan
    plan = wonder_generation_plan({}, input_groups=['mechanics.buildings'], repo_root=ROOT)
    assert any(path.name == 'tv_engineering_department_wonder_mechanics_modifiers.txt' for path in plan.outputs)
    assert any(path.name == 'tv_wonder_level_change_triggers.txt' for path in plan.outputs)


def test_fixed_outputs_match_their_generators():
    from scripts_engineering_department.in_game.common.scripted_effects import (
        gen_tv_wonder_level_change_effects as levels,
        gen_tv_wonder_ritual_state_effects as rituals,
        gen_tv_wonder_finalization_effects as finalization,
        gen_tv_engineering_department_wonder_mechanics_effects as display,
    )
    from scripts_engineering_department.in_game.common.static_modifiers import (
        gen_tv_engineering_department_wonder_mechanics_modifiers as modifiers,
    )
    expected = {
        levels.OUT_FILE: levels.generate(),
        levels.TRIGGERS_FILE: levels.generate_triggers(),
        modifiers.OUT_FILE: modifiers.generate(),
        finalization.OUT_FILE: finalization.generate(),
        GAME/'common/scripted_effects/tv_wonder_location_display_effects.txt': display.generate_location_display_effects(),
    }
    expected.update({ROOT/'src'/name: content for name, content in rituals.outputs().items()})
    for path, content in expected.items():
        assert path.read_bytes().startswith(b'\xef\xbb\xbf'), path
        assert path.read_text(encoding='utf-8-sig') == content, path


def test_all_hidden_ritual_events_have_localized_titles():
    events = source_blocks('events/tv_wonder_ritual_lifecycle_events.txt')
    titles = [child(body, 'title').value for body in events.values()
              if any(n.key == 'hidden' and n.value == 'yes' for n in body)]
    assert len(titles) == 197
    assert set(titles) == {'empty_text'}
    root = ROOT/'.eu5-base/reference_game_files/game/main_menu/localization'
    for language in ('english', 'simp_chinese'):
        assert any(re.search(r'^\s*empty_text:\d*\s+"', p.read_text(encoding='utf-8-sig'), re.M)
                   for p in (root/language).glob('*.yml'))
