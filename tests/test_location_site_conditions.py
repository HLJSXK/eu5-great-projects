"""Native site-condition bridge coverage and the runtime text-fetch regression."""
from pathlib import Path

import yaml

from scripts_engineering_department.in_game.gui import gen_location_window as source
from scripts_engineering_department.wonder_mechanics.io import load_all_wonder_mechanics
from test_wonder_priority_proposals import child, parse

ROOT = Path(__file__).resolve().parents[1]


def test_every_site_predicate_is_read_only_and_calls_the_existing_location_trigger():
    wonders, _ = load_all_wonder_mechanics()
    actual = source.SITE_CONDITIONS_GUI_OUTPUT.read_text(encoding='utf-8-sig')
    assert actual == source.generate_site_condition_guis()
    assert source.SITE_CONDITIONS_GUI_OUTPUT.read_bytes().startswith(b'\xef\xbb\xbf')
    bridges = {node.key: node for node in parse(actual)}
    triggers = {node.key for node in parse((ROOT / 'src/in_game/common/scripted_triggers/'
                                           'tv_engineering_department_wonder_mechanics_triggers.txt')
                                          .read_text(encoding='utf-8-sig'))}
    assert set(bridges) == {f"tv_wonder_display_{w['id']}_site_conditions" for w in wonders}
    for wonder in wonders:
        body = bridges[f"tv_wonder_display_{wonder['id']}_site_conditions"].children
        assert {node.key for node in body} == {'scope', 'is_shown', 'effect'}
        assert child(body, 'scope').value == 'location'
        assert not child(body, 'effect').children
        checks = child(body, 'is_shown').children
        assert len(checks) == 1
        assert checks[0].key == f"tv_wonder_display_{wonder['id']}_base_site_rules_trigger"
        assert checks[0].key in triggers
        assert checks[0].value == 'yes'


def test_site_predicate_output_belongs_to_the_gallery_generator():
    rows = yaml.safe_load((ROOT / 'data/generated_files.yaml').read_text(encoding='utf-8'))['generated']
    entries = [row for row in rows if row['output'] == source.SITE_CONDITIONS_GUI_OUTPUT.relative_to(ROOT).as_posix()]
    assert len(entries) == 1
    assert entries[0]['script'] == source.SCRIPT_REL


def test_all_gallery_slots_use_native_predicates_and_static_icon_textures():
    gui = source.WIDGETS_FILE.read_text(encoding='utf-8-sig')
    assert 'EvaluateTrigger(' not in gui
    for slot in range(1, 6):
        predicate = source.slot_site_rules_met_expr(slot)
        assert f'visible = "[{predicate}]"' in gui
        assert f'visible = "[Not({predicate})]"' in gui
        assert '.IsShown(GuiScope.SetRoot(LocationView.GetLocation.MakeScope).End)' in predicate
        for state in ('yes', 'no'):
            assert f'name = "tv_location_wonder_site_conditions_{state}_{slot}"' in gui
            assert f'texture = "gfx/interface/icons/text_icons/trigger_{state}.dds"' in gui
        assert f'name = "tv_location_wonder_site_conditions_icon_{slot}"' not in gui
