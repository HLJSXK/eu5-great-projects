"""Compatibility extraction must preserve complete upstream GUI blocks."""
from pathlib import Path

import pytest

from scripts.compat import gen_tv_prosper_or_perish_encyclopedia_lateralview as merge
from scripts_engineering_department.vanilla_takeover.parse import parse


@pytest.fixture
def upstream():
    return (Path(__file__).resolve().parents[1] /
            '.eu5-base/reference_mods/3613232232/in_game/gui/encyclopedia_lateralview.gui'
            ).read_text(encoding='utf-8-sig')


@pytest.mark.parametrize('padding', [0, 1200])
def test_extracts_complete_blocks_despite_upstream_line_changes(upstream, padding):
    # New sections, comments and quoted braces must not truncate the final card.
    upstream = ('# added upstream header\n' * padding + upstream).replace(
        'text = "game_concept_pp_starvation_desc"',
        'text = "game_concept_pp_starvation_desc"\n'
        'raw_text = "a quoted } and {" # a commented }\n' + '\n' * padding)
    lines = upstream.splitlines()
    button = '\n'.join(merge.pp_tab_button_block(lines))
    content = '\n'.join(merge.pp_mod_content_block(lines))
    for block, kind in ((button, 'hbox'), (content, 'vbox')):
        nodes = parse(block)
        assert len(nodes) == 1 and nodes[0].key == kind
    assert 'pp_select_page' in button
    assert merge.SHARED_SET_PP in button
    assert 'game_concept_pp_starvation_desc' in content
    assert 'TooltipListScrollArea' not in content
    assert merge.SHARED_HASVALUE_PP in content


def test_generated_panel_has_one_root_and_both_tabs(upstream, monkeypatch):
    from great_projects_editor_web.services.artifacts import _validate_script

    monkeypatch.setattr(merge, 'pp_lines', lambda: upstream.splitlines())
    text = merge.generate()
    _validate_script(text.encode('utf-8-sig'), Path('panel.gui'))
    nodes = parse(text)
    assert len(nodes) == 1 and nodes[0].key == 'lateralview_full'
    assert merge.SHARED_HASVALUE_PP in text
    assert merge.SHARED_HASVALUE_TV in text
    assert 'game_concept_pp_starvation_desc' in text


def test_missing_or_duplicate_pp_content_fails(upstream):
    with pytest.raises(RuntimeError, match='found 0'):
        merge.pp_mod_content_block(['vbox = {}'])
    with pytest.raises(RuntimeError, match='found 2'):
        merge.pp_mod_content_block((upstream + '\n' + upstream).splitlines())
