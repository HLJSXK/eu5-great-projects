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
    assert queues == 6
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
    base_gui = source.GLORP_LOCATION_WINDOW_FILE.read_text(encoding='utf-8-sig')
    with pytest.raises(RuntimeError, match='found 2'):
        source.inject_sol_button(base_gui + base_gui)


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


def test_mnt_host_uses_current_reference_and_preserves_its_new_location_ui():
    import gen_tv_meiou_and_taxes_location_window as mnt

    assert mnt.BASE_FILE == ROOT / '.eu5-base/reference_mods/3735059838/in_game/gui/location_window.gui'
    generated = mnt.generate()
    assert mnt.OUT_FILE.read_text(encoding='utf-8-sig') == generated
    for marker in (
        'name = "mnt_owner_flag_centers"',
        'mnt_center_slot_trade = { size = { 36 36 } }',
        'mnt_center_slot_production = { size = { 36 36 } }',
        'mnt_center_slot_culture = { size = { 36 36 } }',
        'mnt_center_slot_education = { size = { 36 36 } }',
        'tv_location_wonders_button = {}',
        'tv_location_wonders_panel = {}',
        'sol_location_living_standard_button = {}',
    ):
        assert marker in generated


@pytest.mark.parametrize('mod', ['src', 'submods/tv_standard_of_living_compat'])
def test_glorp_hosts_preserve_current_upstream_except_public_widget_insertions(mod):
    generated = (ROOT / mod / 'in_game/gui/location_window.gui').read_text(encoding='utf-8-sig')
    upstream = source.GLORP_LOCATION_WINDOW_FILE.read_text(encoding='utf-8-sig')
    upstream += '\n' + source.GLORP_LOCATION_TYPES_FILE.read_text(encoding='utf-8-sig').replace(
        'types LocationWindowTypes', 'types GPGlorpLocationWindowBaseTypes', 1)
    assert '.eu5-base/reference_mods/3601047146/in_game/gui/location_window.gui' in generated
    additions = {
        'tv_location_wonders_button = {}', 'tv_location_wonders_panel = {}',
        'sol_location_living_standard_button = {}',
        'using = tv_location_wonders_close_on_queue',
        'name = "tv_location_city_appearance"',
    }
    def original_lines(text):
        return [line.strip() for line in text.splitlines()
                if line.strip() and not line.lstrip().startswith('#') and line.strip() not in additions]
    assert original_lines(generated) == original_lines(upstream)
    # Preserve Glorp's CM integration and map-mode hovers without a Glorp runtime dependency.
    assert 'cm_is_auto_expand_on_icon = {}' in generated
    assert generated.count("GetScriptedGui('cm_check_for_auto_expand_when_upgrading_building')") == 3
    assert "PdxGuiWidget.PushMapModeOverride('control')" in generated


def test_glorp_host_includes_split_types_without_duplicate_definitions():
    nodes = list(walk(parse(source.generate_host_gui())))
    definitions = [node.key for node in nodes if node.key.startswith(('type:', 'template:'))]
    assert len(definitions) == len(set(definitions))
    for key in ('type:location_building_levels_piechart', 'type:garrison_sortie_button',
                'template:location_background', 'template:location_card_core'):
        assert key in definitions
