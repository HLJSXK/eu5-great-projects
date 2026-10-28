"""Actual location window, menu selection and empty/overflow regressions."""
from pathlib import Path
import sys
import tempfile
import unittest

WORKSPACE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WORKSPACE))
from ai_gui_assessment import engineering, location


class LocationPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engineering.configure()
        from eu5_gui_renderer.paths import GAME
        if not (GAME / 'loading_screen/fonts').is_dir():
            raise unittest.SkipTest('Installed game assets required for location previews')
        from eu5_gui_renderer.preview import load_resources
        cls.resources = load_resources()

    def test_actual_panel_and_menu_states_are_complete_and_diagnostic_free(self):
        from eu5_gui_renderer.preview import has_diagnostics
        from PIL import Image
        with tempfile.TemporaryDirectory() as folder:
            for state, wonders in location.STATES.items():
                with self.subTest(state=state):
                    report = location.render(state, self.resources, output=Path(folder) / f'{state}.png')
                    self.assertFalse(has_diagnostics(report), report)
                    self.assertEqual(report['gui'], str(WORKSPACE / 'src' / location.GUI_PATH))
                    self.assertTrue(Path(report['details']['panel']).is_file())
                    self.assertIsNone(report['tooltip'])
                    if not wonders:
                        self.assertFalse(report['menu_open'])
                        self.assertNotIn('menu', report['details'])
                        continue
                    self.assertTrue(report['menu_open'])
                    with Image.open(report['details']['menu']) as image:
                        self.assertGreaterEqual(image.width, 462)
                        self.assertLess(image.width, 540)
                        self.assertLessEqual(image.height, 672)
                        self.assertGreater(len(image.getcolors(image.width * image.height)), 500)

    def test_selecting_later_project_and_closed_menu(self):
        from eu5_gui_renderer.preview import has_diagnostics
        with tempfile.TemporaryDirectory() as folder:
            selected = location.render('multiple', self.resources, selected_slot=3,
                                       output=Path(folder) / 'selected.png')
            self.assertFalse(has_diagnostics(selected), selected)
            tree = Path(selected['tree']).read_text(encoding='utf-8')
            # Only the selected detail should be laid out; changing the selection
            # must not leave every project's large image/effect block expanded.
            self.assertEqual(sum('300x200@' in line for line in tree.splitlines()), 1)
            closed = location.render('multiple', self.resources, menu=False,
                                     output=Path(folder) / 'closed.png')
            self.assertFalse(has_diagnostics(closed), closed)
            self.assertNotIn('menu', closed['details'])

    def test_unknown_binding_is_not_filled_by_fixture(self):
        from eu5_gui_renderer.data import Evaluator, Unknown
        evaluator = Evaluator(location.scenario_mocks('multiple', self.resources), self.resources.loc, [])
        self.assertIsInstance(evaluator.eval_str("[Location.MakeScope.GetVariable('new_unconfigured_variable').GetValue]"), Unknown)

    def test_compact_slots_tooltip_slots_and_overflow_are_independent(self):
        values = location.wonder_variables(location.STATES['overflow'])
        self.assertEqual(values['tv_wonder_tooltip_overflow_count'], 1)
        self.assertEqual(values['tv_wonder_display_slot_3_id'], 1)
        self.assertEqual(values['tv_wonder_tooltip_slot_5_id'], 4)
        empty = location.wonder_variables([])
        self.assertIsNone(empty['tv_wonder_display_slot_1_id'])
        self.assertIsNone(empty['tv_wonder_tooltip_slot_1_id'])
        unbuilt = location.wonder_variables(location.STATES['unbuilt'])
        self.assertEqual(unbuilt['tv_wonder_tooltip_slot_1_level'], 0)


if __name__ == '__main__':
    unittest.main()
