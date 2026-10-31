"""Public location widgets work without GP's full location-window override."""
from pathlib import Path
import sys

import pytest
import yaml

from scripts_engineering_department.in_game.gui import gen_location_window as source

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.eu5-base/ai_gui_assessment/renderer'))
sys.path.insert(0, str(ROOT / 'scripts/compat'))
from eu5_gui_renderer.gui import Expander, GuiDB
from eu5_gui_renderer.pdx import parse


def walk(nodes):
    for node in nodes:
        yield node
        if node.is_block():
            yield from walk(node.value)


@pytest.fixture(scope='module')
def widget_db():
    game = ROOT / '.eu5-base/reference_game_files/game'
    files = [path for stage in ('loading_screen', 'main_menu', 'in_game')
             for path in (game / stage / 'gui').rglob('*.gui')
             if path.name != 'location_window.gui']
    return GuiDB(files + [source.WIDGETS_FILE])


def test_exported_widgets_expand_without_gp_or_glorp_location_window(widget_db):
    host = parse('''widget = {
        widget = { tv_location_wonders_button = {} }
        tv_location_wonders_panel = {}
    }''')[0]
    expander = Expander(widget_db)
    root = expander.build(host.key, host.value, {})
    button = root.children[0].children[0]
    panel = root.children[1]
    assert button.props['name'] == 'tv_location_wonders_button'
    assert button.props['size'] == ['108', '30']
    assert panel.props['name'] == 'tv_location_wonders_panel'
    assert panel.props['position'] == ['0', '163']
    assert panel.props['parentanchor'] == 'top|right'
    assert panel.props['widgetanchor'] == 'top|left'
    assert panel.props['allow_outside'] == 'yes'
    assert panel.children
    assert not expander.log


@pytest.mark.parametrize('mod', ['src', 'submods/tv_meiou_and_taxes_compat', 'submods/tv_standard_of_living_compat'])
def test_all_window_hosts_reference_one_copy_of_each_widget_and_close_before_queue(mod, widget_db):
    path = ROOT / mod / 'in_game/gui/location_window.gui'
    nodes = parse(path.read_text(encoding='utf-8-sig'), str(path))
    entries = list(walk(nodes))
    for typename in ('tv_location_wonders_button', 'tv_location_wonders_panel',
                     'sol_location_living_standard_button'):
        instances = [node for node in entries if node.key == typename]
        assert len(instances) == 1
        assert instances[0].value == []
        assert not any(node.key == 'type:' + typename for node in entries)
    root = next(node for node in nodes if node.key == 'lateralview')
    assert any(node.key == 'tv_location_wonders_panel' for node in root.value)
    # Resolve the public template in each original action block; preserve the
    # original OpenConstructionQueue call and its widget/queue parameters.
    expander = Expander(widget_db)
    queues = 0
    for node in entries:
        if not node.is_block():
            continue
        if not any(child.key == 'on_action' and 'LocationView.OpenConstructionQueue(' in str(child.value)
                   for child in node.value):
            continue
        actions = [child.value for child in expander.splice_usings(node.value) if child.key == 'on_action']
        assert actions[0] == "[LocationView.Vars.Clear('tv_location_wonders_open')]"
        assert actions[1].startswith('[LocationView.OpenConstructionQueue(')
        assert len(actions) == 2
        queues += 1
    expected_queues = (6 if mod in {'src', 'submods/tv_meiou_and_taxes_compat'} else 0)
    assert queues == expected_queues
    assert not expander.log


def test_widget_output_has_one_owner_and_preserves_all_gallery_actions():
    gui = source.WIDGETS_FILE.read_text(encoding='utf-8-sig')
    assert gui == source.generate_widgets()
    assert source.WIDGETS_FILE.read_bytes().startswith(b'\xef\xbb\xbf')
    assert b'\r\n' not in source.WIDGETS_FILE.read_bytes()
    assert 'lateralview = {' not in gui
    assert 'sol_location_living_standard_button' not in gui
    for slot in range(1, 6):
        assert f'action_name = "tv_wonder_location_reritual_{slot}"' in gui
        assert 'parameter_value = "[LocationView.GetLocation]"' in gui
    rows = yaml.safe_load((ROOT / 'data/generated_files.yaml').read_text(encoding='utf-8'))['generated']
    owners = [row['script'] for row in rows if row['output'] == source.WIDGETS_FILE.relative_to(ROOT).as_posix()]
    assert owners == [source.SCRIPT_REL]


def test_sol_insertion_rejects_ambiguous_or_missing_host_slots():
    with pytest.raises(RuntimeError, match='Expected one SOL button insertion point'):
        source.inject_sol_button('widget = {}')
    vanilla = source.VANILLA_LOCATION_WINDOW_FILE.read_text(encoding='utf-8-sig')
    with pytest.raises(RuntimeError, match='found 2'):
        source.inject_sol_button(vanilla + vanilla)


@pytest.mark.parametrize('mod', ['src', 'submods/tv_meiou_and_taxes_compat',
                                'submods/tv_standard_of_living_compat'])
def test_levy_pie_bindings_match_current_vanilla(mod):
    game_gui = (ROOT / '.eu5-base/reference_game_files/game/in_game/gui/location_window.gui').read_text(encoding='utf-8-sig')
    gui = (ROOT / mod / 'in_game/gui/location_window.gui').read_text(encoding='utf-8-sig')
    for branch in ('Army', 'Navy'):
        old = f'Get{branch}LevyPercentage'
        current = f'{old}ForCountry(LocationView.GetPlayer)'
        assert f'{old})' not in gui
        for expression in (f'FixedPointToFloat(LocationView.GetLocation.GetProvince.{current})',
                           f"Subtract_float('(float)1.0', FixedPointToFloat(LocationView.GetLocation.GetProvince.{current}))"):
            assert f'value = "[{expression}]"' in game_gui
            assert gui.count(f'value = "[{expression}]"') == 1


def test_sol_host_regenerates_from_workspace_and_base_only():
    import gen_tv_standard_of_living_location_window as sol

    assert sol.BASE_FILE.is_relative_to(ROOT / '.eu5-base')
    assert sol.OUT_FILE.read_text(encoding='utf-8-sig') == sol.generate()
    assert source.OUT_FILE.read_text(encoding='utf-8-sig') == source.generate()


def test_location_window_is_injected_from_vanilla_base():
    generated = source.OUT_FILE.read_text(encoding='utf-8-sig')
    vanilla = source.VANILLA_LOCATION_WINDOW_FILE.read_text(encoding='utf-8-sig')
    assert source.DATA_REL.endswith('.eu5-base/reference_game_files/game/in_game/gui/location_window.gui')
    assert 'glorp_shared_types' not in generated
    assert generated.count('header_action_button_left_uber') == vanilla.count('header_action_button_left_uber')
    assert generated.count('tv_location_wonders_button = {}') == 1
    assert generated.count('tv_location_wonders_panel = {}') == 1
    assert 'types LocationWindowTypes' in vanilla
    assert generated.count('types LocationWindowTypes') == 1
