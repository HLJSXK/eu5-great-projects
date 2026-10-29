"""Preview actual normalized candidate sources, without writing project data."""
from copy import copy, deepcopy
import hashlib
import json
import shutil

import pytest
import yaml

from great_projects_editor_web.services.platform import snapshot_files
from great_projects_editor_web.services.wonder import fields, localization, sources, values
from great_projects_editor_web.services.wonder_resource import WonderResourceService


@pytest.fixture(scope="module")
def loaded():
    return WonderResourceService()


@pytest.fixture
def service(loaded, tmp_path, monkeypatch):
    service = copy(loaded)
    for name in ('WONDER_LOCALIZATION_FILE', 'WONDER_FINAL_BUILDINGS_FILE', 'WONDER_GENERIC_RITUALS_FILE',
                 'WONDER_BASE_MODIFIERS_FILE', 'WONDER_SITE_RULES_FILE', 'WONDERS_FILE',
                 'UNIQUE_WONDERS_FILE'):
        old = getattr(sources, name)
        path = tmp_path / 'data' / old.name
        path.parent.mkdir(exist_ok=True)
        shutil.copyfile(old, path)
        monkeypatch.setattr(sources, name, path)
    monkeypatch.setattr(sources, 'REPO_ROOT', tmp_path)
    service._base = snapshot_files(sources.wonder_source_paths(), repo_root=tmp_path)
    return service


def preview(service, drafts):
    base = {item.path: item.sha256 for item in service._base}
    disk = {path: path.read_bytes() for path in sources.wonder_source_paths()}
    original = deepcopy((service.wonders_data, service.mechanics_data, service.unique_wonders_data,
                         service.localization_data))
    result = service.preview_resource_edits(drafts, base, regenerate=False)
    assert disk == {path: path.read_bytes() for path in disk}
    assert original == (service.wonders_data, service.mechanics_data, service.unique_wonders_data,
                        service.localization_data)
    assert result['generation_plan']['steps'] == []
    return result


def test_localization_diff_has_wonder_language_and_normalized_written_value(service):
    wonder = service.wonders[0]
    key = localization.wonder_name_key(wonder)
    report = preview(service, {wonder['id']: {'values': {
        'english': {key: '  Changed\r\nname  '}, 'simp_chinese': {key: '新名称'},
    }}})
    rows = report['diff']
    assert len(rows) == 2
    for row in rows:
        assert row['wonder_id'] == wonder['id']
        assert row['wonder_key'] == wonder['key']
        assert row['field'] == key
        assert row['scope'] == 'localization'
        assert row['before'] == service.localization_data[row['language']][key]
    assert {r['language']: r['after'] for r in rows} == {'english': 'Changed name', 'simp_chinese': '新名称'}


def test_multiple_wonder_edits_keep_distinct_identity(service):
    wonders = service.wonders[:2]
    report = preview(service, {w['id']: {'values': {'english': {localization.wonder_name_key(w): 'Changed ' + w['key']}}} for w in wonders})
    assert {r['wonder_id'] for r in report['diff']} == {w['id'] for w in wonders}


def test_structure_diff_uses_source_mapping_without_editor_options(service):
    wonder = next(w for w in service.wonders if not w['is_unique'])
    spec = next(s for s in fields.build_mechanics_specs_for_wonder(
        wonder, mechanics=service.mechanics, mechanics_data=service.mechanics_data,
        unique_wonders_data=service.unique_wonders_data,
        generic_options=service._generic_wonder_options() if wonder.get("is_unique") else [],
        option_catalogs=service._option_catalogs,
    ) if s.target_kind == 'base_modifiers')
    editor_value = json.loads(spec.original_value)
    editor_value['rows'][0]['value'] = '0.12345'
    report = preview(service, {wonder['id']: {'mechanics': {spec.key: json.dumps(editor_value)}}})
    row = next(r for r in report['diff'] if r['field'] == 'base_modifiers')
    assert row['value_kind'] == 'structure'
    assert row['before'] == service.mechanics_data['base_modifiers'][spec.target_key]
    assert row['after'] == values.mapping_from_modifier_rows(json.dumps(editor_value), context=spec.key)
    assert 'options' not in json.dumps(row)


def test_instant_base_effect_preview_commit_and_clear(service, monkeypatch):
    from scripts_engineering_department.wonder_mechanics import _core
    original_load = _core.load_yaml
    monkeypatch.setattr(_core, 'load_yaml', lambda path: original_load(
        sources.WONDER_BASE_MODIFIERS_FILE if path.name == 'wonder_base_modifiers.yaml' else path
    ))
    wonder = next(w for w in service.wonders if not w['is_unique'])
    key = f"mechanics.base_instant_effects.{wonder['key']}"
    draft = {wonder['id']: {'mechanics': {key: json.dumps({'rows': [{'type': 'gold', 'value': '2.5'}]})}}}
    report = preview(service, draft)
    row = next(row for row in report['diff'] if row['field'] == 'base_instant_effects')
    assert row['after'] == [{'type': 'gold', 'value': 2.5}]
    assert not row['before_present']
    base = {item.path: item.sha256 for item in service._base}
    service.commit_resource(draft, base, regenerate=False)
    saved = yaml.safe_load(sources.WONDER_BASE_MODIFIERS_FILE.read_bytes())
    assert saved['base_instant_effects'][wonder['key']] == row['after']
    assert saved['base_modifiers'] == service.mechanics_data['base_modifiers']
    base = {item.path: item.sha256 for item in service._base}
    service.commit_resource({wonder['id']: {'mechanics': {key: '{"rows":[]}'}}}, base, regenerate=False)
    assert wonder['key'] not in yaml.safe_load(sources.WONDER_BASE_MODIFIERS_FILE.read_bytes())['base_instant_effects']


def test_unique_instant_base_effects_are_scaled_readonly(service):
    service.mechanics_data = deepcopy(service.mechanics_data)
    wonder = next(w for w in service.wonders if w['is_unique'])
    service.mechanics_data['base_instant_effects'] = {wonder['mechanic_key']: [{'type': 'gold', 'value': 2.5}]}
    field = next(f for s in service.get_wonder_payload(wonder['id'])['mechanics']['sections']
                 for f in s['fields'] if f['target_kind'] == 'base_instant_effects')
    assert field['editable'] is False
    assert float(json.loads(field['original_value'])['rows'][0]['value']) == 5
    report = preview(service, {wonder['id']: {'mechanics': {field['key']: '{"rows":[]}'}}})
    assert report['diff'] == []


def test_prototype_selection_reports_both_written_source_fields(service):
    wonder = next(w for w in service.wonders if w['is_unique'])
    prototype = next(w for w in service.wonders if not w['is_unique'] and w['key'] != wonder['base_key'])
    spec = next(s for s in fields.build_mechanics_specs_for_wonder(
        wonder, mechanics=service.mechanics, mechanics_data=service.mechanics_data,
        unique_wonders_data=service.unique_wonders_data,
        generic_options=service._generic_wonder_options() if wonder.get("is_unique") else [],
        option_catalogs=service._option_catalogs,
    ) if s.target_kind == 'unique_prototype')
    report = preview(service, {wonder['id']: {'mechanics': {spec.key: prototype['key']}}})
    assert {r['field']: r['after'] for r in report['diff']} == {'base_key': prototype['key'], 'mechanic_key': prototype['key']}




def test_normalized_noop_has_no_field_or_file_diff(service):
    wonder = service.wonders[0]
    key = localization.wonder_name_key(wonder)
    report = preview(service, {wonder['id']: {'values': {'english': {key: '  ' + service.localization_data['english'][key] + '  '}}}})
    assert report['diff'] == report['file_diff'] == []


def test_preview_matches_commit_file_bytes_and_values(service):
    wonder = service.wonders[0]
    key = localization.wonder_name_key(wonder)
    drafts = {wonder['id']: {'values': {'english': {key: '  Committed\nname  '}}}}
    report = preview(service, drafts)
    base = {item.path: item.sha256 for item in service._base}
    # This check isolates source serialization/transaction from detail generation.
    service.reload_from_disk = lambda: setattr(service, '_base', snapshot_files(sources.wonder_source_paths(), repo_root=sources.REPO_ROOT))
    service.get_wonder_payload = lambda _id: None
    service.commit_resource(drafts, base, regenerate=False)
    for row in report['file_diff']:
        path = sources.REPO_ROOT / row['path']
        assert row['kind'] == 'file'
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['after']
    saved = yaml.safe_load(sources.WONDER_LOCALIZATION_FILE.read_bytes())
    assert saved['wonder_localization']['english'][key] == report['diff'][0]['after'] == 'Committed name'


@pytest.fixture
def cost_editor(service, monkeypatch):
    """A cost/reward service sharing the isolated Wonder sources, wired as in the server."""
    from scripts_engineering_department.wonder_mechanics import _core
    import scripts_engineering_department.wonder_localization_lib as localization_lib
    from great_projects_editor_web.services import cost_reward
    from great_projects_editor_web.services.generation import GenerationPlan

    root = sources.REPO_ROOT
    original_root = cost_reward.REPO_ROOT
    for name, filename in [('DATA_FILE', 'cost_reward_units.yaml'), ('TASK_POOL_FILE', 'task_pool.yaml')]:
        path = root / 'data' / filename
        shutil.copyfile(original_root / 'data' / filename, path)
        monkeypatch.setattr(cost_reward, name, path)
    monkeypatch.setattr(cost_reward, 'REPO_ROOT', root)
    monkeypatch.setattr(cost_reward, 'wonder_generation_plan', lambda *args, **kwargs: GenerationPlan(root, ()))
    original_load = _core.load_yaml

    def read_isolated(path):
        candidate = root / 'data' / path.name
        return original_load(candidate if candidate.exists() else path)

    monkeypatch.setattr(_core, 'load_yaml', read_isolated)
    monkeypatch.setattr(localization_lib, 'WONDER_LOCALIZATION_FILE', sources.WONDER_LOCALIZATION_FILE)
    _core.reset_cost_reward_unit_caches()
    try:
        editor = cost_reward.CostRewardEditorService()
        editor.set_reload_callback(service.reload_from_disk)
        yield editor
    finally:
        _core.reset_cost_reward_unit_caches()


def doubled_catalog_value(service, resource):
    group = next(g for g in resource['draft']['groups'] if g['key'] == 'country_reward')
    token = next(t for t in group['tokens'] if isinstance(t['value'], (int, float)) and not isinstance(t['value'], bool))
    return {group['key']: {token['id']: {'value': token['value'] * 2}}}


def test_cost_reward_commit_then_wonder_refresh_and_commit_preserves_both_edits(service, cost_editor):
    from great_projects_editor_web.services.platform import ConflictError

    old_base = {item.path: item.sha256 for item in service._base}
    wonder = next(w for w in service.wonders if w['is_unique'])
    key = localization.wonder_name_key(wonder)
    drafts = {wonder['id']: {'values': {'english': {key: 'Preserved Wonder draft'}}}}
    initial = cost_editor.load_resource()
    base = {item['path']: item['sha256'] for item in initial['change_set']['base']}
    result = cost_editor.save_tokens(doubled_catalog_value(service, initial), base)
    assert set(result['written_paths']) == {'data/cost_reward_units.yaml'}
    after_cost = sources.UNIQUE_WONDERS_FILE.read_bytes()
    service.preview_resource_edits(drafts, old_base, regenerate=False)
    refreshed = service.load_resource()
    new_base = {item['path']: item['sha256'] for item in refreshed['change_set']['base']}
    assert new_base.get('data/unique_wonders.yaml') == old_base.get('data/unique_wonders.yaml')
    report = service.preview_resource_edits(drafts, new_base, regenerate=False)
    assert [item['field'] for item in report['diff']] == [key]
    committed = service.commit_resource(drafts, new_base, regenerate=False)
    assert committed['operation']['status'] == 'succeeded'
    assert service.localization_data['english'][key] == 'Preserved Wonder draft'
    assert sources.UNIQUE_WONDERS_FILE.read_bytes() == after_cost


def test_wonder_commit_then_cost_reward_refresh_and_category_save(service, cost_editor):
    from great_projects_editor_web.services.platform import ConflictError

    initial = cost_editor.load_resource()
    old_base = {item['path']: item['sha256'] for item in initial['change_set']['base']}
    edits = doubled_catalog_value(service, initial)
    wonder = next(w for w in service.wonders if w['is_unique'])
    key = f"mechanics.unique_initial_level.{wonder['key']}"
    field = next(f for section in service.get_wonder_payload(wonder['id'])['mechanics']['sections']
                 for f in section['fields'] if f['key'] == key)
    level = '2' if str(field['original_value']).strip() == '3' else '3'
    wonder_base = {item.path: item.sha256 for item in service._base}
    committed = service.commit_resource({wonder['id']: {'mechanics': {key: level}}}, wonder_base, regenerate=False)
    assert committed['written_paths'] == ['data/unique_wonders.yaml']
    after_wonder = yaml.safe_load(sources.UNIQUE_WONDERS_FILE.read_bytes())
    cost_editor.preview_edits(edits, old_base)
    refreshed = cost_editor.load_resource()
    new_base = {item['path']: item['sha256'] for item in refreshed['change_set']['base']}
    assert new_base.get('data/unique_wonders.yaml') == old_base.get('data/unique_wonders.yaml')
    result = cost_editor.save_tokens(edits, new_base)
    assert result['operation']['status'] == 'succeeded'
    saved = yaml.safe_load(sources.UNIQUE_WONDERS_FILE.read_bytes())
    entry = lambda data: next(w for w in data['unique_wonders'] if w['key'] == wonder['key'])
    assert entry(saved).get('initial_level') == entry(after_wonder).get('initial_level')
