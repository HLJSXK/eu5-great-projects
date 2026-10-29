"""Contracts and lifecycle boundaries for the 2026-10 ritual rewrite."""
from copy import deepcopy
from pathlib import Path
import re

import pytest

from scripts_engineering_department.wonder_mechanics import _core as core
from scripts_engineering_department.wonder_mechanics.rituals import ritual_styles
from test_wonder_priority_proposals import child, contains, source_blocks, walk

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def data():
    return core.load_all_wonder_mechanics()


def test_all_wonders_inherit_all_three_reward_carriers(data):
    wonders, mechanics = data
    bases = {w['key']: w for w in wonders if not w['is_unique']}
    assert len(wonders) == 195
    for wonder in wonders:
        rows = ritual_styles(wonder, mechanics)
        assert [r['style'] for r in rows] == [1, 2, 3]
        assert not {'ritual', 'ceremony', 'final_buildings'} & wonder.keys()
        if wonder['is_unique']:
            inherited = ritual_styles(bases[wonder['mechanic_key']], mechanics)
            for a, b in zip(rows, inherited):
                assert a['modifier'] != b['modifier']
                for key in ('country_modifier', 'location_modifier_values', 'one_shot', 'societal_value', 'estate_preferences'):
                    assert a[key] == b[key]


def test_location_ritual_tooltip_expands_every_granted_modifier_natively(data):
    from scripts_engineering_department.wonder_localization_lib import (
        load_wonder_localization_data, collapse_wonder_localization_data,
    )
    wonders, mechanics = data
    localized = load_wonder_localization_data()
    collapsed = collapse_wonder_localization_data(localized)
    effects = source_blocks('common/scripted_effects/tv_wonder_ritual_state_effects.txt')
    modifiers = source_blocks('common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt')
    for wonder in wonders:
        for row in ritual_styles(wonder, mechanics):
            style = row['style']
            grant = effects[f"tv_wonder_{wonder['key']}_ritual_{style}_grant_effect"]
            granted = {child(node.children, 'modifier').value for node in walk(grant)
                       if node.key in ('add_country_modifier', 'add_location_modifier')}
            assert granted <= modifiers.keys()
            for language in ('english', 'simp_chinese'):
                calls = []
                for scope, modifier in (('COUNTRY', row['modifier']), ('LOCAL', row['location_modifier'])):
                    key = f"TV_WONDER_RITUAL_{scope}_MODIFIERS_{style}_{wonder['id']}"
                    value = localized[language][key]
                    assert value == (f"[ShowModifierEffect('{modifier}')]" if modifier else '')
                    calls.extend(re.findall(r"\[ShowModifierEffect\('([^']+)'\)\]", value))
                    assert key not in collapsed[language]
                assert set(calls) == granted and len(calls) == len(granted)


@pytest.mark.parametrize('damage', ['axis', 'duplicate_direction', 'missing_estate', 'wrong_scope', 'empty_reward', 'old_shape'])
def test_schema_rejects_invalid_authored_rituals(data, damage):
    _, mechanics = data
    entries = deepcopy(mechanics['generic_rituals'])
    entry = entries['sacred_mountain']
    if damage == 'axis': entry['rituals'][0]['societal_value']['axis'] = 'not_an_axis'
    elif damage == 'duplicate_direction': entry['rituals'][1]['societal_value'] = deepcopy(entry['rituals'][0]['societal_value'])
    elif damage == 'missing_estate': entry['estate_preferences'].pop('dhimmi_estate')
    elif damage == 'wrong_scope': entry['rituals'][0]['reward']['country_modifier'] = {'local_max_literacy': 10}
    elif damage == 'empty_reward': entry['rituals'][0]['reward'] = {}
    else: entry['style_1'] = {}
    with pytest.raises(ValueError): core._validate_generic_rituals(entries, 'test')


def test_mixed_rewards_are_supported_without_changing_style_identity(data):
    _, mechanics = data
    entries = deepcopy(mechanics['generic_rituals'])
    entries['sacred_mountain']['rituals'][0]['reward']['one_shot'] = [{'type': 'prestige', 'value': 5}]
    core._validate_generic_rituals(entries, 'test')
    entries['sacred_mountain']['rituals'][0]['reward']['location_modifier'] = {'local_max_control': 0.1}
    entries['sacred_mountain']['estate_preferences']['clergy_estate'] = 2
    core._validate_generic_rituals(entries, 'test')
    mechanics = {**mechanics, 'generic_rituals': entries}
    wonder = next(w for w in data[0] if w['key'] == 'sacred_mountain')
    assert [r['style'] for r in ritual_styles(wonder, mechanics) if r['location_modifier']] == [1, 2]
    assert ritual_styles(wonder, mechanics)[0]['estate_preferences']['clergy_estate'] == 2


def test_estate_sponsor_and_data_corrections(data):
    wonders, mechanics = data
    for w in wonders:
        rows = ritual_styles(w, mechanics)
        assert rows[0]['estate_preferences'][core.location_reward_estate(w)] == 2
    assert mechanics['generic_rituals']['great_assembly_hall']['rituals'][1]['reward']['location_modifier']['local_max_literacy'] == 10
    assert mechanics['generic_rituals']['great_sculpture_group']['rituals'][1]['reward']['location_modifier']['local_monthly_prosperity'] == 0.004
    assert mechanics['generic_rituals']['giant_dam_project']['rituals'][2]['reward']['one_shot'][0]['value'] == 0.5


def test_each_construction_round_requires_a_fresh_ritual_choice():
    phase = source_blocks('common/scripted_effects/tv_wonder_ritual_phase_effects.txt')
    enter = phase['tv_wonder_ritual_enter_phase_effect']
    # Neither project mode nor a site's old dedication may bypass this entry.
    assert all(n.key in ('remove_variable', 'set_variable',
                         'tv_wonder_ritual_roll_estates_effect',
                         'tv_wonder_ritual_refresh_display_effect') for n in enter)
    cleared = {n.value for n in enter if n.key == 'remove_variable'}
    assert {'tv_wonder_ritual_choice', 'tv_wonder_finalization_outcome',
            'tv_wonder_ritual_reward_claimed', 'tv_wonder_ritual_in_progress',
            'tv_wonder_ritual_completed'} <= cleared
    assert contains(enter, 'tv_wonder_ritual_roll_estates_effect')
    assert contains(enter, 'tv_wonder_ritual_refresh_display_effect')
    triggers = source_blocks('common/scripted_triggers/tv_wonder_ritual_triggers.txt')
    ready = triggers['tv_wonder_ritual_outcome_ready_trigger']
    assert not contains(ready, 'var:tv_wonder_finalization_outcome', '9')
    assert contains(ready, 'has_variable', 'tv_wonder_ritual_completed')
    # All three real grants/settlements remain available on every round.
    choice = phase['tv_wonder_ritual_apply_choice_effect']
    for style in (1, 2, 3):
        assert contains(choice, f'tv_wonder_ritual_apply_style_{style}_effect')


def test_expansion_cleans_old_dedication_only_at_hidden_finalization(data):
    from scripts_engineering_department.wonder_mechanics.naming import finalization_hidden_effect_name
    effects = source_blocks('common/scripted_effects/tv_wonder_finalization_effects.txt')
    for wonder in data[0]:
        finish = effects[finalization_hidden_effect_name(wonder)]
        expansion = next(n for n in walk(finish) if n.key == 'if' and
                         contains(child(n.children, 'limit').children, 'var:tv_wonder_project_mode', '2'))
        plain, styled = [n for n in expansion.children if n.key != 'limit']
        assert contains(child(plain.children, 'limit').children, 'var:tv_wonder_finalization_outcome', '0')
        assert contains(plain.children, 'save_scope_as', 'tv_wonder_ritual_sync_country')
        assert contains(child(plain.children, 'var:tv_wonder_site').children,
                        f"tv_wonder_{wonder['key']}_ritual_revoke_effect")
        assert styled.key == 'else'
        assert styled.children[-1].key == f"tv_wonder_{wonder['key']}_ritual_sync_country_effect"
        # The selected local modifier survives, every other local style is removed.
        for ritual in ritual_styles(wonder, data[1]):
            if not ritual['location_modifier']:
                continue
            removal = next(n for n in styled.children if n.key == 'if' and
                           contains(n.children, 'remove_location_modifier', ritual['location_modifier']))
            condition = child(child(removal.children, 'limit').children, 'NOT')
            assert contains(condition.children, 'var:tv_wonder_finalization_outcome', str(ritual['style']))
        assert not contains(styled.children, f"tv_wonder_{wonder['key']}_ritual_revoke_effect")


def test_confirmation_pays_and_settles_estates_before_timer_but_completion_does_not():
    effects = source_blocks('common/scripted_effects/tv_wonder_ritual_phase_effects.txt')
    confirm = effects['tv_wonder_ritual_confirm_effect']
    keys = [n.key for n in walk(confirm)]
    assert keys.index('tv_wonder_ritual_pay_effect') < keys.index('tv_wonder_ritual_settle_estates_effect')
    assert keys.index('tv_wonder_ritual_settle_estates_effect') < keys.index('set_variable')
    assert not any(n.key == 'add_estate_satisfaction' for n in walk(effects['tv_wonder_ritual_apply_choice_effect']))
    plain = effects['tv_wonder_ritual_settle_estates_plain_effect']
    assert len([n for n in walk(plain) if n.key == 'add_estate_satisfaction']) == 7
    assert all(child(n.children, 'value').value == '-0.05' for n in walk(plain) if n.key == 'add_estate_satisfaction')
    availability = [n.value for n in walk(effects['tv_wonder_ritual_refresh_display_effect']) if n.key == 'has_societal_value']
    assert availability and all(value.startswith('societal_value_type:') for value in availability)


def test_plain_preview_only_selects_and_has_all_five_message_fields():
    from scripts_engineering_department.wonder_localization_lib import load_localization_map
    actions = source_blocks('common/generic_actions/tv_wonder_ritual_actions.txt')
    action = actions['tv_wonder_ritual_preview_plain']
    preview = next(n for n in walk(action) if n.key == 'tv_wonder_ritual_preview_effect')
    assert child(preview.children, 'style').value == '0'
    effects = source_blocks('common/scripted_effects/tv_wonder_ritual_phase_effects.txt')
    keys = {n.key for n in walk(effects['tv_wonder_ritual_preview_effect'])}
    assert not {'pay_price', 'add_estate_satisfaction', 'tv_wonder_finalize_effect'} & keys
    registration = 'PERFORM_tv_wonder_ritual_preview_plain_ACTION'
    mod = ROOT / 'src'
    assert 'tv_wonder_ritual_preview_plain' in (mod / 'in_game/common/generic_action_ai_lists/tv_engineering_department_list.txt').read_text(encoding='utf-8-sig')
    assert registration in (mod / 'main_menu/gui/messagetypes/tv_engineering_department_messagetypes.txt').read_text(encoding='utf-8-sig')
    files = list((mod / 'main_menu/localization').glob('*/tv_wonder_ritual_messages_l_*.yml'))
    assert len(files) == 11
    for path in files:
        assert path.read_bytes().startswith(b'\xef\xbb\xbf')
        loc = load_localization_map(path)
        assert all(loc[f'{registration}_{suffix}'] for suffix in ('HEADER', 'TITLE', 'SETUP', 'LOG', 'MAP'))


def test_memory_token_guards_stale_expiry_and_sync_keeps_other_instances():
    effects = source_blocks('common/scripted_effects/tv_wonder_ritual_state_effects.txt')
    grant = effects['tv_wonder_sacred_mountain_ritual_2_grant_effect']
    memory = [n for n in walk(grant) if n.key == 'add_to_variable_map' and child(n.children, 'name').value == 'tv_wonder_ritual_memory_by_id']
    assert child(memory[0].children, 'days').value == '36500'
    assert child(child(grant, 'hidden_effect').children, 'trigger_event_silently').children
    events = source_blocks('events/tv_wonder_ritual_lifecycle_events.txt')
    expiry = events['tv_engineering_department.3001']
    assert contains(expiry, 'is_key_in_variable_map')
    text = (ROOT/'src/in_game/events/tv_wonder_ritual_lifecycle_events.txt').read_text(encoding='utf-8-sig')
    assert 'has_variable_map = tv_wonder_ritual_memory_by_id' in text
    sync = effects['tv_wonder_sacred_mountain_ritual_sync_country_effect']
    assert len([n for n in walk(sync) if n.key == 'any_owned_location']) == 3
    revoke = effects['tv_wonder_sacred_mountain_ritual_revoke_effect']
    assert contains(revoke, 'remove_location_modifier')
    assert contains(revoke, 'scope:tv_wonder_ritual_sync_country')


def test_preview_paths_do_not_scan_locations_and_only_lifecycle_writes_style_map():
    root = ROOT/'src/in_game'
    writers = []
    for path in (root/'common/scripted_effects').glob('*.txt'):
        for name, body in source_blocks('common/scripted_effects/' + path.name).items():
            for node in walk(body):
                if node.key in ('add_to_variable_map','remove_from_variable_map') and child(node.children,'name').value == 'tv_wonder_ritual_style_by_id':
                    writers.append(name)
    assert writers and all(name.endswith(('_grant_effect','_revoke_effect')) for name in writers)
    phase = source_blocks('common/scripted_effects/tv_wonder_ritual_phase_effects.txt')
    for n in (1,2,3):
        assert not any(node.key.endswith('owned_location') for node in walk(phase[f'tv_wonder_ritual_apply_style_{n}_effect']))


def test_reritual_only_uses_buff_preview_and_returns_to_new_conception():
    effects = source_blocks('common/scripted_effects/tv_wonder_ritual_phase_effects.txt')
    finish = effects['tv_wonder_reritual_finish_effect']
    assert contains(finish, 'tv_wonder_clear_project_state_core_effect')
    assert contains(finish, 'tv_wonder_start_concept_effect')
    assert not contains(finish, 'tv_wonder_register_current_project_priority_candidate_from_variables_effect')
    completion = effects['tv_wonder_ritual_apply_choice_effect']
    assert contains(completion, 'add_prestige', '10')
    assert not contains(completion, 'tv_wonder_apply_finalization_visible_rewards_effect')
    assert not contains(completion, 'construct_building')
    actions = source_blocks('common/generic_actions/tv_engineering_department_actions.txt')
    allow = child(child(actions['tv_wonder_abandon'], 'allow').children, 'scope:actor').children
    assert not contains(allow, 'has_variable', 'tv_wonder_ritual_in_progress')
    project = source_blocks('common/scripted_effects/tv_engineering_department_effects.txt')
    reritual_branch = child(project['tv_wonder_abandon_effect'], 'if').children
    assert contains(reritual_branch, 'tv_wonder_ritual_cancel_reritual_effect')
    assert not contains(reritual_branch, 'tv_wonder_retire_great_engineer_effect')
    assert not contains(reritual_branch, 'add_prestige')
    lifecycle = source_blocks('common/scripted_effects/tv_wonder_location_display_effects.txt')
    demolished = lifecycle['tv_wonder_sacred_mountain_handle_final_building_level_changed_effect']
    assert contains(demolished, 'tv_wonder_ritual_cancel_reritual_effect')


def test_unique_ritual_text_preview_preserves_every_other_source_and_cached_state():
    import yaml
    from great_projects_editor_web.services.wonder_resource import WonderResourceService
    from great_projects_editor_web.services.wonder import sources
    service = WonderResourceService()
    original = deepcopy(service.unique_wonders_data)
    wonder = next(w for w in service.wonders if w['is_unique'])
    field = f"mechanics.ritual_text.{wonder['key']}.2.desc_zh"
    changed, files, ids = service._candidate_for_drafts({wonder['id']: {'mechanics': {field: '新的奉献仪式说明。'}}})
    assert changed['unique'] and ids == [wonder['id']]
    assert set(files) == {sources.UNIQUE_WONDERS_FILE}
    candidate = yaml.safe_load(files[sources.UNIQUE_WONDERS_FILE])
    entry = next(w for w in candidate['unique_wonders'] if w['key'] == wonder['key'])
    assert entry['ritual_text'][2]['desc_zh'] == '新的奉献仪式说明。'
    entry['ritual_text'][2]['desc_zh'] = wonder['ritual_text'][2]['desc_zh']
    assert candidate == original
    assert service.unique_wonders_data == original


def test_atlas_exposes_localized_directions_and_preferences_for_each_style(data):
    from unique_wonders_site.scripts.build.build_wonders import append_ritual_plan_sections
    from scripts_engineering_department.wonder_localization_lib import load_wonder_localization_data
    wonders, mechanics = data
    wonder = next(w for w in wonders if w['key'] == 'unique_pharos_lighthouse')
    effects = []
    for n in (1, 2, 3):
        append_ritual_plan_sections(effects, wonder=wonder, mechanics=mechanics,
            loc_data=load_wonder_localization_data(), modifier_index={}, style=n)
    country = [row for row in effects if row['scope'] == 'country']
    assert len(country) == 3
    for row in country:
        assert row['meta']['direction']['en'] and row['meta']['direction']['zh']
        assert abs(row['meta']['shock']) == 20
        assert len(row['meta']['estate_preferences']) == 7
        assert all(pref['estate']['zh'] and pref['preference']['zh'] for pref in row['meta']['estate_preferences'])


def test_encyclopedia_renders_three_native_previews_in_the_body(data):
    from scripts_engineering_department.in_game.gui.gen_tv_encyclopedia_wonders_cards_gui import append_card
    from scripts_engineering_department.vanilla_takeover.parse import parse, walk as gui_walk
    wonder, mechanics = data[0][0], data[1]
    lines = []
    append_card(lines, category='generic', texture='test.dds', title_key='test', body_key='test_desc', wonder=wonder, mechanics=mechanics)
    previews = []
    for root in parse('\n'.join(lines)):
        for node, ancestors in gui_walk(root):
            raw = node.child('raw_text')
            if node.key == 'text_multi' and raw and '_catalogue_effect' in raw.value:
                previews.append(node)
                assert not any(parent.key in ('text_single', 'icon') for parent in ancestors)
    assert len(previews) == 3


def test_encyclopedia_keeps_only_approved_cards(data):
    from scripts_engineering_department.europedia_content import CARDS
    from scripts_engineering_department.europedia_render import render_all, select_wonder_cards

    wonders, mechanics = data
    examples = select_wonder_cards(list(reversed(wonders)) + [{'key': 'future_wonder'}])
    assert [w['key'] for w in examples] == ['triumphal_axis', 'unique_topkapi_palace']
    assert [w['is_unique'] for w in examples] == [False, True]
    assert len(CARDS) == 15
    textures = {int(w['id']): 'test.dds' for w in examples}
    rendered = render_all(wonders, mechanics, textures)
    surfaces = ['\n'.join(rendered['gui'])]
    for relative in (
        'src/in_game/gui/encyclopedia_lateralview.gui',
        'submods/tv_prosper_or_perish_compat/in_game/gui/encyclopedia_lateralview.gui',
    ):
        text = (ROOT / relative).read_text(encoding='utf-8-sig')
        surfaces.append(text.split('# BEGIN GENERATED TV_ENCYCLOPEDIA_CARDS', 1)[1]
                       .split('# END GENERATED TV_ENCYCLOPEDIA_CARDS', 1)[0])
    for text in surfaces:
        assert len(re.findall(r'\btv_eu_card\s*=\s*\{', text)) == 17
        for card in CARDS:
            assert f'text = "TV_EU_{card["id"].upper()}_TITLE"' in text
        actual = {w['key'] for w in wonders if f'text = "game_concept_{w["concept"]}"' in text}
        assert actual == {'triumphal_axis', 'unique_topkapi_palace'}
        previews = re.findall(r"ShowScriptedEffectForScope\('(tv_wonder_display_\d+_ritual_\d+_catalogue_effect)'", text)
        assert len(previews) == 6
        assert set(previews) == {
            f'tv_wonder_display_{w["id"]}_ritual_{style}_catalogue_effect'
            for w in examples for style in (1, 2, 3)
        }


@pytest.mark.parametrize('damage', ['missing', 'duplicate'])
def test_encyclopedia_rejects_ambiguous_example_data(data, damage):
    from scripts_engineering_department.europedia_render import select_wonder_cards

    wonders = list(data[0])
    topkapi = next(w for w in wonders if w['key'] == 'unique_topkapi_palace')
    if damage == 'missing':
        wonders.remove(topkapi)
    else:
        wonders.append(topkapi)
    with pytest.raises(ValueError, match='unique_topkapi_palace'):
        select_wonder_cards(wonders)


def test_encyclopedia_gui_expressions_match_engine_arity():
    """Or/And take exactly two arguments; a third is a load error, not a silent miss.

    The engine rejects `Or(a, b, c)` with "Function 'Or' expected 2 arguments, got 3" and then
    drops the whole widget expression, so a three-way visibility test has to nest.
    """
    text = (ROOT / 'src/in_game/gui/encyclopedia_lateralview.gui').read_text(encoding='utf-8-sig')
    # Or/And take exactly two arguments; the numbered forms take exactly their number. Vanilla
    # itself uses Or3/Or4/Or5 and And3/And4/And5, so both spellings are legal and both are checked.
    expected = {'Or': 1, 'Or3': 2, 'Or4': 3, 'Or5': 4,
                'And': 1, 'And3': 2, 'And4': 3, 'And5': 4, 'Not': 0}
    wrong = []
    for name, arity in expected.items():
        for match in re.finditer(rf'\b{name}\(', text):
            index, depth, commas = match.end(), 1, 0
            while index < len(text) and depth:
                char = text[index]
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                elif char == ',' and depth == 1:
                    commas += 1
                index += 1
            if commas != arity:
                line = text.count('\n', 0, match.start()) + 1
                wrong.append(f'{name} with {commas} argument(s) at line {line}')
    assert not wrong, wrong


def _run_plain_cache(nodes, *, level, old_level):
    """Execute the generated cache subset; engine calendar/queues are outside this test."""
    maps = {'tv_wonder_plain_level_by_wonder_id': {999: 6}}
    if old_level is not None:
        maps['tv_wonder_plain_level_by_wonder_id'][1] = old_level
    variables, local = {'tv_wonder_level': level}, {}

    def value(raw):
        raw = raw.strip('"')
        if raw.startswith('local_var:'): return local[raw.split(':', 1)[1]]
        if raw.startswith('var:'): return variables[raw.split(':', 1)[1]]
        if raw.startswith('variable_map('):
            name, key = raw[len('variable_map('):-1].split('|')
            return maps[name][int(key)]
        return int(raw)

    def condition(items):
        matched = False
        for n in items:
            if n.key in ('trigger_if', 'trigger_else_if'):
                if n.key == 'trigger_if': matched = False
                if not matched and condition(child(n.children, 'limit').children):
                    matched = True
                    if not condition(tuple(c for c in n.children if c.key != 'limit')): return False
                continue
            elif n.key == 'trigger_else':
                if not matched and not condition(n.children): return False
                continue
            elif n.key == 'has_variable_map': passed = n.value in maps
            elif n.key == 'always': passed = n.value == 'yes'
            elif n.key == 'NOT': passed = not condition(n.children)
            elif n.key == 'is_key_in_variable_map':
                passed = value(child(n.children, 'target').value) in maps[child(n.children, 'name').value]
            elif n.key == 'has_building': passed = level > 0
            elif n.key == 'location_building_level': passed = level >= value(child(n.children, 'value').value)
            elif n.key.startswith('local_var:') and n.op == '<': passed = value(n.key) < value(n.value)
            else: raise AssertionError(f'Unhandled cache condition: {n}')
            if not passed: return False
        return True

    def run(items):
        matched = False
        for n in items:
            if n.key in ('if', 'else_if'):
                if n.key == 'if': matched = False
                if not matched and condition(child(n.children, 'limit').children):
                    matched = True
                    run(tuple(c for c in n.children if c.key != 'limit'))
            elif n.key == 'else':
                if not matched: run(n.children)
            elif n.key == 'owner': run(n.children)
            elif n.key in ('set_variable', 'set_local_variable'):
                target = local if n.key == 'set_local_variable' else variables
                target[child(n.children, 'name').value] = value(child(n.children, 'value').value)
            elif n.key == 'remove_local_variable': local.pop(n.value)
            elif n.key in ('add_to_variable_map', 'remove_from_variable_map'):
                target = maps[child(n.children, 'name').value]
                key = value(child(n.children, 'key').value)
                if n.key == 'remove_from_variable_map': target.pop(key, None)
                else: target.setdefault(key, value(child(n.children, 'value').value))
            else: raise AssertionError(f'Unhandled cache effect: {n}')
    run(nodes)
    assert not local
    assert maps['tv_wonder_plain_level_by_wonder_id'][999] == 6
    return maps['tv_wonder_plain_level_by_wonder_id'].get(1), variables.get('tv_wonder_has_plain_wonder')


def test_plain_lifecycle_supplements_maxima_without_country_rebuild(data):
    from scripts_engineering_department.wonder_mechanics.naming import finalization_hidden_effect_name
    final = source_blocks('common/scripted_effects/tv_wonder_finalization_effects.txt')
    events = source_blocks('events/tv_wonder_ritual_lifecycle_events.txt')
    for w in data[0]:
        finish = final[finalization_hidden_effect_name(w)]
        expiry = events[f"tv_engineering_department.{3000+w['id']}"]
        for body in (finish, expiry):
            assert not contains(body, 'tv_wonder_mechanics_refresh_country_auto_level_map_effect')
            assert not any(n.key.endswith('owned_location') for n in walk(body))
        # Every completion also supplements the national base-effect maximum.
        writes = [n for n in walk(finish) if n.key == 'add_to_variable_map']
        assert {child(n.children, 'name').value for n in writes} == {
            'tv_wonder_auto_level_by_wonder_id', 'tv_wonder_plain_level_by_wonder_id'}
        assert all(child(n.children, 'value').value == 'var:tv_wonder_level' for n in writes)

    finish = final[finalization_hidden_effect_name(data[0][0])]
    plain = next(n for n in walk(finish) if n.key == 'if' and
                 contains(child(n.children, 'limit').children, 'var:tv_wonder_finalization_outcome', '0') and
                 contains(n.children, 'name', 'tv_wonder_plain_level_by_wonder_id'))
    supplement = tuple(n for n in plain.children if n.key != 'limit')
    expiry = events['tv_engineering_department.3001']
    expired_instance = next(n for n in walk(expiry) if n.key == 'if' and
                            contains(child(n.children, 'limit').children, 'has_building'))
    for level in range(1, 7):
        for old in (None, *range(1, 7)):
            expected = (max(level, old or 0), 1)
            assert _run_plain_cache(supplement, level=level, old_level=old) == expected
            assert _run_plain_cache((expired_instance,), level=level, old_level=old) == expected
    assert _run_plain_cache((expired_instance,), level=0, old_level=None) == (None, None)
    phase = source_blocks('common/scripted_effects/tv_wonder_ritual_phase_effects.txt')
    assert not contains(phase['tv_wonder_reritual_finish_effect'], 'tv_wonder_mechanics_refresh_country_auto_level_map_effect')


def test_retired_eight_stage_localization_is_absent_from_sources_and_all_outputs():
    from scripts_engineering_department.wonder_localization_lib import load_yaml, load_localization_map
    retired = re.compile(r'TV_ENGINEERING_(?:CEREMONY|ACTIVE_RITUAL)_')
    raw = load_yaml(ROOT/'data/wonder_localization.yaml')['wonder_localization']
    assert all(not retired.match(key) for rows in raw.values() for key in rows)
    files = list((ROOT/'src/main_menu/localization').glob('*/tv_engineering_department_wonder_mechanics_l_*.yml'))
    assert len(files) == 11
    for path in files:
        assert not any(retired.match(key) for key in load_localization_map(path))
        # General UI labels with the same prefix remain owned by the manual file.
        language = path.parent.name
        manual = load_localization_map(path.with_name(f'tv_engineering_department_l_{language}.yml'))
        assert 'TV_ENGINEERING_CEREMONY_CARD_TITLE' in manual


def test_single_reritual_event_contains_every_candidate_and_a_final_exit(data):
    event = source_blocks('events/tv_wonder_ritual_lifecycle_events.txt')['tv_engineering_department.2001']
    options = [n.children for n in event if n.key == 'option']
    assert len(options) == 196
    assert [child(option, 'name').value for option in options[:-1]] == [
        f"tv_wonder_reritual_option_{w['id']}" for w in data[0]]
    assert child(options[-1], 'name').value == 'TV_WONDER_RERITUAL_LATER'
    for option, wonder in zip(options, data[0]):
        trigger = child(option, 'trigger').children
        assert contains(trigger, 'name', 'tv_wonder_plain_level_by_wonder_id')
        assert contains(trigger, 'target', str(wonder['id']))
        assert not any(n.key.endswith('owned_location') for n in walk(option))


def test_translation_pruning_preserves_surviving_bytes_and_is_idempotent(tmp_path, monkeypatch):
    from scripts_engineering_department.main_menu.localization import translate_engineering_department_localization_google as translate
    source = tmp_path/'tv_test_l_english.yml'
    source.write_text('l_english:\n live:0 "Current"\n', encoding='utf-8-sig')
    target = tmp_path/'french'/'tv_test_l_french.yml'
    target.parent.mkdir()
    kept = 'l_french:\r\n # header\r\n live:0 "Texte traduit"\r\n'
    target.write_bytes((kept+' retired:0 "Ancien"\r\n').encode('utf-8-sig'))
    monkeypatch.setattr(translate, 'OUTPUT_ROOT', tmp_path)
    assert translate.prune_obsolete_keys('french', [source]) == 1
    assert target.read_bytes() == kept.encode('utf-8-sig')
    assert translate.prune_obsolete_keys('french', [source]) == 0
