"""Contracts for the remaining items in Error_Log_Fix_Plan_2026-10-23."""
from pathlib import Path
import re

import pytest

from test_wonder_priority_proposals import child, source_blocks, walk

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('missing', ['HEADER', 'TITLE', None])
def test_message_localization_validator_requires_header_and_title(tmp_path, monkeypatch, missing):
    from scripts import validate
    root = tmp_path/'src'
    actions = root/'in_game/common/generic_actions'
    actions.mkdir(parents=True)
    (actions/'probe.txt').write_text('tv_probe = {}\n')
    for language in validate.LOCALIZATION_LANGUAGES:
        folder = root/'main_menu/localization'/language
        folder.mkdir(parents=True)
        text = f'l_{language}:\n' + ''.join(
            f' PERFORM_tv_probe_ACTION_{suffix}:0 "Probe"\n'
            for suffix in ('HEADER', 'TITLE', 'SETUP', 'LOG', 'MAP') if suffix != missing)
        (folder/'probe.yml').write_text(text, encoding='utf-8-sig')
    monkeypatch.setattr(validate, 'REPO_ROOT', tmp_path)
    monkeypatch.setattr(validate, 'MOD_ROOTS', (root,))
    monkeypatch.setattr(validate, 'issues', [])
    validate.check_generic_action_message_localization()
    if missing:
        assert len(validate.issues) == len(validate.LOCALIZATION_LANGUAGES)
        assert all(f'PERFORM_tv_probe_ACTION_{missing}' in issue for issue in validate.issues)
    else:
        assert not validate.issues


def test_all_ritual_messages_have_five_localized_fields_in_every_language():
    from scripts_engineering_department.wonder_ritual_codegen import message_localization
    from scripts_engineering_department.wonder_localization_lib import load_yaml, WONDER_LOCALIZATION_FILE
    from great_projects_editor_web.services.wonder_generation import wonder_generation_plan
    localization = load_yaml(WONDER_LOCALIZATION_FILE)['wonder_localization']
    root = ROOT/'src/main_menu/localization'
    actions = ('tv_wonder_ritual_preview_1', 'tv_wonder_ritual_preview_2', 'tv_wonder_ritual_preview_3',
               'tv_wonder_ritual_confirm', 'tv_wonder_ritual_choose_plain', 'tv_wonder_ritual_cancel_reritual')
    folders = [folder for folder in root.iterdir() if folder.is_dir()]
    assert len(folders) == 11
    for folder in folders:
        path = folder/f'tv_wonder_ritual_messages_l_{folder.name}.yml'
        assert path.read_bytes().startswith(b'\xef\xbb\xbf')
        assert path.read_text(encoding='utf-8-sig') == message_localization(folder.name, localization)
        values = dict(re.findall(r'^\s*([^\s:#]+):\d*\s+"(.*)"', path.read_text(encoding='utf-8-sig'), re.M))
        labels = localization['simp_chinese' if folder.name == 'simp_chinese' else 'english']
        for action in actions:
            for suffix in ('HEADER', 'TITLE', 'SETUP', 'LOG', 'MAP'):
                assert values[f'PERFORM_{action}_ACTION_{suffix}'] == labels[action]
    plan = wonder_generation_plan({}, input_groups={'localization'}, repo_root=ROOT)
    assert all((folder/f'tv_wonder_ritual_messages_l_{folder.name}.yml') in plan.outputs for folder in folders)


def test_additive_message_files_are_fresh_disjoint_and_root_owned():
    from scripts import gen_messagetypes as generator
    all_outputs = generator.outputs()
    for path, expected in all_outputs.items():
        assert path.read_bytes().startswith(b'\xef\xbb\xbf')
        assert path.read_text(encoding='utf-8-sig') == expected
        if path.suffix == '.yml':
            text = '\n'.join(p.read_text(encoding='utf-8-sig') for p in path.parent.glob('*.yml'))
            keys = set(re.findall(r'^\s*([^\s:#]+):\d*\s+"', text, re.M))
            references = re.findall(r':0 "\$([^$]+)\$"', expected)
            assert references and set(references) <= keys
    outputs = {path: expected for path, expected in all_outputs.items() if path.suffix == '.txt'}
    assert len(outputs) == 1
    vanilla = ROOT/'.eu5-base/reference_game_files/game/main_menu/gui/messagetypes/00_messagetypes.txt'
    declaration = re.compile(r'(?m)^([A-Z][A-Za-z0-9_]*)\s*=\s*\{')
    seen = set(declaration.findall(vanilla.read_text(encoding='utf-8-sig')))
    for path, expected in outputs.items():
        assert path.read_bytes().startswith(b'\xef\xbb\xbf')
        assert path.read_text(encoding='utf-8-sig') == expected
        names = declaration.findall(expected)
        assert len(names) == len(set(names))
        assert not seen.intersection(names)
        seen.update(names)
        mod = path.relative_to(ROOT).parts[0]
        actions = generator.action_ids_under(ROOT/mod/'in_game/common/generic_actions', ROOT/mod/'in_game/common/country_interactions')
        assert all(generator.message_action_id(name) in actions for name in names)
        generic = generator.action_ids_under(ROOT/mod/'in_game/common/generic_actions')
        assert {f'PERFORM_{name}_ACTION' for name in generic} <= set(names)
    for mod in ('src',):
        assert not (ROOT/mod/'main_menu/gui/messagetypes.txt').exists()


@pytest.mark.parametrize('damage', ['none', 'missing', 'duplicate', 'vanilla_duplicate', 'legacy'])
def test_message_validator_detects_missing_duplicate_and_obsolete_files(tmp_path, monkeypatch, damage):
    from scripts import validate
    roots = tuple(tmp_path/name for name in ('src', 'src_fixture'))
    vanilla = tmp_path/'.eu5-base/reference_game_files/game/main_menu/gui/messagetypes/00_messagetypes.txt'
    vanilla.parent.mkdir(parents=True)
    vanilla.write_text('NATIVE_CATEGORY = {}\n')
    files = []
    for index, root in enumerate(roots):
        actions = root/'in_game/common/generic_actions'
        actions.mkdir(parents=True)
        (actions/'actions.txt').write_text(f'tv_action_{index} = {{}}\n')
        messages = root/f'main_menu/gui/messagetypes/root_{index}.txt'
        messages.parent.mkdir(parents=True)
        messages.write_text(f'PERFORM_tv_action_{index}_ACTION = {{}}\n')
        files.append(messages)
    if damage == 'missing': files[0].write_text('')
    elif damage == 'duplicate': files[1].write_text(files[1].read_text()+files[0].read_text())
    elif damage == 'vanilla_duplicate': files[0].write_text(files[0].read_text()+'NATIVE_CATEGORY = {}\n')
    elif damage == 'legacy': (roots[0]/'main_menu/gui/messagetypes.txt').write_text('')
    monkeypatch.setattr(validate, 'REPO_ROOT', tmp_path)
    monkeypatch.setattr(validate, 'MOD_ROOTS', roots)
    monkeypatch.setattr(validate, 'issues', [])
    validate.check_message_types()
    if damage == 'none': assert not validate.issues
    else:
        expected = {'missing': 'missing', 'duplicate': 'duplicate', 'vanilla_duplicate': 'duplicate', 'legacy': 'obsolete'}[damage]
        assert any(expected in issue for issue in validate.issues), validate.issues


def test_unique_proposal_keeps_50_support_with_current_cached_trigger():
    effects = source_blocks('common/scripted_effects/tv_engineering_department_effects.txt')
    matches = [n for body in effects.values() for n in walk(body)
               if n.key == 'if' and any(c.key == 'limit' and
               any(x.key == 'var:tv_wonder_locked_is_unique' and x.op == '?=' and x.value == '1' for x in c.children)
               for c in n.children)]
    assert matches
    assert any(any(n.key == 'tv_change_wonder_domestic_support_effect' and child(n.children, 'value').value == '50'
                   for n in walk(branch.children)) for branch in matches)
    assert 'tv_wonder_unique_locked_trigger' not in (ROOT/'src/in_game/common/scripted_effects/tv_engineering_department_effects.txt').read_text(encoding='utf-8-sig')


def test_all_hidden_ritual_events_have_empty_title_and_description():
    events = source_blocks('events/tv_wonder_ritual_lifecycle_events.txt')
    hidden = [body for body in events.values() if any(n.key == 'hidden' and n.value == 'yes' for n in body)]
    assert len(hidden) == 197
    assert all(child(body, 'title').value == child(body, 'desc').value == 'empty_text' for body in hidden)


def test_takeover_call_arguments_match_each_generated_trigger_signature():
    from scripts_engineering_department.vanilla_takeover.parse import parse, walk as nodes
    triggers = (ROOT/'src/in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt').read_text(encoding='utf-8-sig')
    signatures = {n.key: set(re.findall(r'\$([a-z_]+)\$', triggers[n.start:n.end]))
                  for n in parse(triggers) if '_present_' in n.key}
    checked = 0
    for relative in ('events/0000_tv_vw_vanilla_event_overrides.txt', 'common/decisions/tv_vw_vanilla_decision_overrides.txt'):
        text = (ROOT/'src/in_game'/relative).read_text(encoding='utf-8-sig')
        for top in parse(text):
            for node, _ in nodes(top):
                if node.key in signatures:
                    assert {c.key for c in node.children} == signatures[node.key], node.key
                    checked += 1
    assert checked > 30


def test_gui_only_ritual_variables_are_suppressed_in_standalone_ed():
    ed = (ROOT/'src/in_game/common/on_action/tv_engineering_department_cmf_suppressions.txt').read_text(encoding='utf-8-sig')
    assert not (ROOT/'src/in_game/common/on_action/tv_cmf_suppressions.txt').exists()
    gui = '\n'.join(path.read_text(encoding='utf-8-sig') for path in (ROOT/'src/in_game/gui').rglob('*.gui'))
    for family in ('display_axis', 'display_dir', 'position'):
        for index in (1, 2, 3):
            name = f'tv_wonder_ritual_{family}_{index}'
            assert name in gui
            assert f'cmf_suppress = {{ v = {name} }}' in ed
    phase = (ROOT/'src/in_game/common/scripted_effects/tv_wonder_ritual_phase_effects.txt').read_text(encoding='utf-8-sig')
    for family in ('has_country_modifier', 'has_location_modifier', 'has_one_shot'):
        assert f'tv_wonder_ritual_{family}_' not in phase
        assert f'tv_wonder_ritual_{family}_' not in ed
    bridges = (ROOT/'src/in_game/common/on_action/tv_engineering_department_pulse_bridges.txt').read_text(encoding='utf-8-sig')
    assert 'tv_engineering_department_cmf_warning_suppressions_monthly_pulse' in bridges
