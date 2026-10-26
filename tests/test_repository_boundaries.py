"""Great Projects must build with its own files and the shared base only."""
import json
from pathlib import Path
import re
import yaml
from scripts import ai_context, gen_index, validate
from great_projects_editor_web.services import validation

ROOT = Path(__file__).resolve().parents[1]


def test_single_owned_root_and_complete_registry_inputs():
    assert validate.MOD_ROOT_NAMES == validation.MOD_ROOT_NAMES == ('src',)
    assert gen_index.MOD_ROOTS == [ROOT / 'src']
    assert ai_context.load_routes()['mod_roots'] == ['src']
    for row in yaml.safe_load((ROOT / 'data/generated_files.yaml').read_text(encoding='utf-8'))['generated']:
        assert (ROOT / row['script']).is_file(), row
        assert (ROOT / row['output']).is_file(), row
        for source in str(row.get('data', '')).split(' + '):
            source = source.split(' (', 1)[0].strip()
            if source:
                assert list(ROOT.glob(source)), (row, source)


def test_no_development_import_from_tv_or_victory_sources():
    for folder in ('scripts', 'scripts_engineering_department', 'great_projects_editor_web', 'unique_wonders_site/scripts'):
        for path in (ROOT / folder).rglob('*.py'):
            text = path.read_text(encoding='utf-8-sig')
            assert not re.search(r'(?m)^\s*(?:from|import) towards_victory_editor_web\b', text), path
    for name in ('data/victory_paths.yaml', 'data/io_establishment.yaml', 'great_projects_editor_web/services/victory_tree.py'):
        assert not (ROOT / name).exists()
    metadata = json.loads((ROOT / 'src/.metadata/metadata.json').read_text(encoding='utf-8'))
    assert metadata['id'] == 'hades.towards_victory.great_project'
    assert {row['id'] for row in metadata['relationships']} == {'community_mod_framework', 'romaimperator.construction_manager'}
    assert '/.eu5-base' in (ROOT / '.gitignore').read_text(encoding='utf-8')


def test_ownership_notification_has_distinct_id_and_support_event_remains():
    text = (ROOT / 'src/in_game/events/tv_engineering_department_events.txt').read_text(encoding='utf-8-sig')
    assert len(re.findall(r'(?m)^tv_engineering_department\.21\s*=', text)) == 1
    assert len(re.findall(r'(?m)^tv_engineering_department\.22\s*=', text)) == 1
    for language in ('english', 'simp_chinese'):
        path = ROOT / f'src/main_menu/localization/{language}/tv_engineering_department_ai_l_{language}.yml'
        assert path.read_bytes().startswith(b'\xef\xbb\xbf')
        assert 'tv_engineering_department.22.t:' in path.read_text(encoding='utf-8-sig')
    hook = (ROOT / 'src/in_game/common/on_action/tv_wonder_ownership_on_action.txt').read_text(encoding='utf-8-sig')
    assert 'id = tv_engineering_department.22' in hook
    assert 'id = tv_engineering_department.21' not in hook


def test_all_actual_generic_actions_keep_complete_registration():
    validate.issues.clear()
    validate.check_message_types()
    validate.check_generic_action_message_localization()
    assert not validate.issues
    # AI action membership is checked independently of message localization.
    actions = set()
    for path in (ROOT / 'src/in_game/common/generic_actions').glob('*.txt'):
        actions.update(re.findall(r'(?m)^([a-z]\w*)\s*=\s*\{', path.read_text(encoding='utf-8-sig')))
    registered = set()
    for path in (ROOT / 'src/in_game/common/generic_action_ai_lists').glob('*.txt'):
        for body in re.findall(r'\bactions\s*=\s*\{([^{}]*)\}', path.read_text(encoding='utf-8-sig')):
            registered.update(re.findall(r'\b[a-z]\w*\b', re.sub(r'#.*', '', body)))
    assert actions and actions <= registered, sorted(actions - registered)


def test_changed_validation_keeps_game_errors_but_excludes_negative_fixtures(tmp_path, monkeypatch):
    from types import SimpleNamespace
    bad = 'construct_building = { building_type = market cost_multiplier = 0 }\n'
    paths = ('src/in_game/common/scripted_effects/bad.txt', 'tests/fixtures/probe/bad.txt')
    for relative in paths:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(bad, encoding='utf-8-sig')
    monkeypatch.setattr(validate, 'REPO_ROOT', tmp_path)
    monkeypatch.setattr(validate.subprocess, 'run', lambda *args, **kwargs: SimpleNamespace(stdout='\n'.join(paths)))
    assert validate.get_changed_files() == [tmp_path / paths[0]]
    monkeypatch.setattr(validate, 'issues', [])
    validate.check_construct_building_cost_multiplier_reason(tmp_path / paths[0], bad)
    assert validate.issues


def test_owned_trigger_localization_does_not_use_tv_key():
    text = (ROOT / 'src/in_game/common/trigger_localization/tv_engineering_department_triggers.txt').read_text(encoding='utf-8-sig')
    assert 'TV_ENGINEERING_DEPARTMENT_HAS_VARIABLE_NOT_SET_TT = {' in text
    assert 'TV_HAS_VARIABLE_NOT_SET_TT = {' not in text
