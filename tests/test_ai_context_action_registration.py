"""Action registration reminders must reach default agent context before edits."""
from contextlib import redirect_stdout
import io
import json
import sys

import pytest

from scripts import ai_context


ACTION_PATHS = ['src/in_game/common/generic_actions/new_action.txt', 'scripts/in_game/common/generic_actions/gen_new_action.py', 'scripts/gen_messagetypes.py', 'scripts_engineering_department/wonder_ritual_codegen.py', 'data/wonder_generic_rituals.yaml', 'src/main_menu/localization/english/tv_wonder_ritual_messages_l_english.yml']

@pytest.mark.parametrize('path', ACTION_PATHS)
def test_registration_check_is_present_in_default_and_json_context(path, monkeypatch):
    # A reminder cannot depend on its position in the truncated anti-pattern list.
    monkeypatch.setattr(ai_context, 'relevant_rules', lambda *args, **kwargs: [])
    context = ai_context.build_context([path], ai_context.load_routes())
    alerts = [row for row in context['alerts'] if row['id'] == 'generic_action_registration']
    assert len(alerts) == 1, path
    message = alerts[0]['message']
    for token in ('actions = {', 'PERFORM_', 'messagetypes/', 'HEADER', 'TITLE', 'SETUP', 'LOG', 'MAP', 'validate.py'):
        assert token in message, (path, token)
    output = io.StringIO()
    with redirect_stdout(output):
        ai_context.print_markdown(context, full=False)
    assert message in output.getvalue()
    assert '## Risk Card:' not in output.getvalue()
    assert 'generic_action_registration' in json.dumps(context)


def test_unrelated_work_does_not_get_an_action_registration_reminder():
    for path in ('README.md', 'docs/knowledge/risk_cards/generic_actions.md', 'tests/test_ai_context_action_registration.py'):
        context = ai_context.build_context([path], ai_context.load_routes())
        assert not any(row['id'] == 'generic_action_registration' for row in context['alerts']), path


def test_one_registration_reminder_for_several_action_sources():
    context = ai_context.build_context(ACTION_PATHS, ai_context.load_routes())
    assert len([row for row in context['alerts'] if row['id'] == 'generic_action_registration']) == 1


@pytest.mark.parametrize('option', ['--changed', '--files'])
def test_cli_entry_points_emit_the_required_check(option, monkeypatch, capsys):
    path = 'src/in_game/common/generic_actions/new_action.txt'
    monkeypatch.setattr(ai_context, 'changed_files', lambda: [path])
    monkeypatch.setattr(sys, 'argv', ['ai_context.py', option, *([path] if option == '--files' else []), '--json'])
    ai_context.main()
    result = json.loads(capsys.readouterr().out)
    assert any(row['id'] == 'generic_action_registration' for row in result['alerts'])


def test_startup_instructions_expose_the_complete_message_contract():
    root = ai_context.REPO_ROOT
    for path in (root/'AGENTS.md', root/'CLAUDE.md'):
        text = path.read_text(encoding='utf-8')
        for token in ('HEADER', 'TITLE', 'SETUP', 'LOG', 'MAP', 'ai_context.py'):
            assert token in text, (path, token)
