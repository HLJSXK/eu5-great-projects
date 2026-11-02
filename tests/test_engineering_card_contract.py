"""Keep the six ED cards' frame/help contracts across every source variant.

These checks use the shipped GUI and need no installed game assets. Layout and
lazy tooltip expansion are also exercised by the engineering preview tests.
"""
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.eu5-base/ai_gui_assessment/renderer'))
from eu5_gui_renderer.pdx import parse


def walk(nodes):
    for node in nodes:
        yield node
        if node.is_block():
            yield from walk(node.value)


CARDS = [
    pytest.param(node, id=f'{path.name}:{node.line}')
    for path in (
        ROOT / 'src/in_game/gui/panels/organization/tv_engineering_department.gui',
        ROOT / 'src/in_game/gui/tv_wonder_org_logistics.gui',
    )
    for node in walk(parse(path.read_text(encoding='utf-8-sig'), str(path)))
    if node.key == 'tv_engineering_department_card_common'
]


@pytest.mark.parametrize('card', CARDS)
def test_named_card_retains_shared_width_budget(card):
    props = {node.key: node.value for node in card.value}
    assert 'maximumsize' in props, 'A replacement card must retain the 500-unit frame cap'
    assert props['maximumsize'][0].key == '500'


@pytest.mark.parametrize('card', CARDS)
def test_named_card_retains_encyclopedia_help(card):
    props = {node.key: node.value for node in card.value}
    title = next(node.value for node in props['blockoverride:common_header_text'] if node.key == 'text')
    assert 'blockoverride:header_help_tooltip' in props, f'{title} inherits empty placeholder help'
    help_nodes = list(walk(props['blockoverride:header_help_tooltip']))
    assert any(node.key == 'ConceptTooltipType' for node in help_nodes)
    help_title = next(node for node in help_nodes if node.key == 'blockoverride:title_text')
    assert any(node.key == 'text' and node.value == title for node in help_title.value)
    body = next(node for node in help_nodes if node.key == 'blockoverride:tooltip_content')
    assert any(node.key == 'text' and str(node.value).startswith('TV_ENGINEERING_')
               for node in walk(body.value)), f'{title} has no explanatory text'
    assert not any(node.value == 'Card title header' for node in help_nodes)
