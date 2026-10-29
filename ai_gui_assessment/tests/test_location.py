"""Shipped gallery geometry, hover routes and empty/overflow regressions."""
from pathlib import Path
import sys
import tempfile
import re
import unittest
from unittest.mock import patch

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
                        self.assertGreaterEqual(image.width, 396)
                        self.assertLess(image.width, 430)
                        self.assertLessEqual(image.height, 633)
                        self.assertGreater(len(image.getcolors(image.width * image.height)), 500)

    def test_all_artwork_visible_and_closed_menu(self):
        from eu5_gui_renderer.preview import has_diagnostics
        with tempfile.TemporaryDirectory() as folder:
            selected = location.render('multiple', self.resources,
                                       output=Path(folder) / 'selected.png')
            self.assertFalse(has_diagnostics(selected), selected)
            tree = Path(selected['tree']).read_text(encoding='utf-8')
            self.assertEqual(sum('225x150@' in line for line in tree.splitlines()), 3)
            # One square medallion hover target per artwork.
            from eu5_gui_renderer.gui import Expander
            _, _, popup = location.build(self.resources, Expander(self.resources.db), 560, 1080, menu=True)
            def visit(node):
                yield node
                for child in node.children:
                    yield from visit(child)
            badges = [node for node in visit(popup)
                      if str(node.props.get('name', '')).startswith('tv_location_wonder_level_')]
            self.assertEqual(len(badges), 5)
            self.assertEqual({node.props['parentanchor'] for node in badges}, {'bottom|right'})
            closed = location.render('multiple', self.resources, menu=False,
                                     output=Path(folder) / 'closed.png')
            self.assertFalse(has_diagnostics(closed), closed)
            self.assertNotIn('menu', closed['details'])

    def test_art_and_current_level_hover_render_separately(self):
        from eu5_gui_renderer.preview import has_diagnostics
        with tempfile.TemporaryDirectory() as folder:
            for owner in ['tv_location_wonder_art_1', 'tv_location_wonder_level_1']:
                with self.subTest(owner=owner):
                    report = location.render('single', self.resources, hover=owner,
                                             output=Path(folder) / f'{owner}.png')
                    self.assertFalse(has_diagnostics(report), report)
                    self.assertLessEqual(report['tooltip']['bounds'][2], 450)
                    tree = Path(report['tooltip']['tree']).read_text(encoding='utf-8')
                    if '_level_' in owner:
                        self.assertNotIn('ShowScriptedEffectForScope', tree)
                        self.assertNotIn('ShowTriggerConditionsForScope', tree)

    def test_current_badge_effects_follow_all_levels_and_unbuilt_states(self):
        from eu5_gui_renderer.data import Evaluator
        from eu5_gui_renderer.preview import has_diagnostics
        from scripts_engineering_department.in_game.gui import gen_location_window as source
        cases = [(3, level, 0) for level in range(7)] + [(3, 3, -1), (102, 6, 2)]
        with tempfile.TemporaryDirectory() as folder:
            for ident, level, style in cases:
                with self.subTest(wonder=ident, level=level, style=style), patch.dict(location.STATES, {'current': [(ident, level, style)]}):
                    evaluator = Evaluator(location.scenario_mocks('current', self.resources), self.resources.loc, [])
                    for local, getter in ((False, source.slot_modifier_key_expr), (True, source.slot_local_modifier_key_expr)):
                        expression = getter('tooltip', 1).replace('LocationView.GetLocation.', 'Location.')
                        self.assertEqual(evaluator.eval_str('[' + expression + ']'),
                                         f'tv_wonder_display_{ident}_{"local_" if local else ""}level_{max(level, 1)}')
                    active = source.slot_current_effects_expr(1).replace('LocationView.GetLocation.', 'Location.')
                    self.assertEqual(evaluator.eval_str('[' + active + ']'), level > 0 and style != -1)
                    from eu5_gui_renderer.gui import Expander
                    _, _, menu = location.build(self.resources, Expander(self.resources.db), 560, 1080, menu=True)
                    def visit(node):
                        yield node
                        for child in node.children:
                            yield from visit(child)
                    badge = next(node for node in visit(menu) if node.props.get('name') == 'tv_location_wonder_level_1')
                    self.assertEqual(evaluator.eval_str(badge.props['visible'].replace('LocationView.GetLocation.', 'Location.')), level > 0)
                    sprites = [node for node in badge.children if node.kind == 'icon' and
                               evaluator.eval_str(node.props['visible'].replace('LocationView.GetLocation.', 'Location.'))]
                    self.assertEqual(len(sprites), int(level > 0))
                    if level:
                        self.assertEqual(sprites[0].props['texture'], f'gfx/interface/icons/location_icons/tv_wonder_level_{level}.dds')
                    report = location.render('current', self.resources, hover='tv_location_wonder_level_1' if level else None,
                                             output=Path(folder) / f'{ident}_{level}_{style}.png')
                    self.assertFalse(has_diagnostics(report), report)
                    if level:
                        self.assertLessEqual(report['tooltip']['bounds'][2], 450)
                    else:
                        self.assertIsNone(report['tooltip'])

    def test_ritual_highlight_requires_implemented_style_and_plain_has_none(self):
        from eu5_gui_renderer.data import Evaluator
        from scripts_engineering_department.in_game.gui import gen_location_window as source
        for state in ('empty', 'multiple', 'dedicated', 'unbuilt', 'shell'):
            evaluator = Evaluator(location.scenario_mocks(state, self.resources), self.resources.loc, [])
            for slot in range(1, 6):
                for style in (1, 2, 3):
                    expression = '[' + source.slot_ritual_active_expr(slot, style).replace('LocationView.GetLocation.', 'Location.') + ']'
                    self.assertEqual(evaluator.eval_str(expression), state == 'dedicated' and slot == style)

    def test_unknown_binding_is_not_filled_by_fixture(self):
        from eu5_gui_renderer.data import Evaluator, Unknown
        from scripts_engineering_department.in_game.gui import gen_location_window as source
        evaluator = Evaluator(location.scenario_mocks('multiple', self.resources), self.resources.loc, [])
        self.assertIsInstance(evaluator.eval_str("[Location.MakeScope.GetVariable('new_unconfigured_variable').GetValue]"), Unknown)
        self.assertIsInstance(evaluator.eval_str('[ExtraTooltipInfo.GetTintColor]'), Unknown)
        # These failed in game; fixture booleans previously concealed the failure.
        for producer in (source.slot_ritual_modifiers_expr(1, 1, 'COUNTRY'),
                         f"ShowModifierEffect({source.slot_modifier_key_expr('tooltip', 1)})"):
            self.assertIsInstance(evaluator.eval_str(f'[IsUTF8StringNotEmpty({producer})]'), Unknown)

    def test_ritual_modifiers_are_only_in_hover_and_all_styles_are_inspectable(self):
        from eu5_gui_renderer.gui import Expander
        from eu5_gui_renderer.preview import has_diagnostics
        expander = Expander(self.resources.db)
        _, _, menu = location.build(self.resources, expander, 560, 1080, menu=True)

        def visit(node):
            yield node
            for child in node.children:
                yield from visit(child)

        self.assertFalse(any(str(node.props.get('name', '')).startswith('tv_location_wonder_ritual_modifiers_')
                             for node in visit(menu)))
        cards = [node for node in visit(menu) if re.fullmatch(
            r'tv_location_wonder_ritual_\d+_[123]', str(node.props.get('name', '')))]
        self.assertEqual(len(cards), 15)
        for card in cards:
            popup = expander.build_lazy(card.tooltipwidget)
            tables = [node for node in visit(popup) if str(node.props.get('name', '')).startswith('tv_location_wonder_ritual_modifiers_')]
            self.assertEqual(len(tables), 2)
            self.assertTrue(all(node.typename == 'TooltipStringPairList' for node in tables))
            self.assertTrue(all('ritual_style' not in node.props.get('visible', '') for node in tables))
        with tempfile.TemporaryDirectory() as folder:
            for state in ('jerusalem', 'dedicated'):
                for style in (1, 2, 3):
                    with self.subTest(state=state, style=style):
                        report = location.render(state, self.resources,
                            hover=f'tv_location_wonder_ritual_1_{style}',
                            output=Path(folder) / f'{state}_{style}.png')
                        self.assertFalse(has_diagnostics(report), report)
                        self.assertLessEqual(report['tooltip']['bounds'][2], 450)
                        tree = Path(report['tooltip']['tree']).read_text(encoding='utf-8')
                        # Hidden nodes remain in the dump; no empty placeholder
                        # may reserve a visible row in the effects section.
                        self.assertNotRegex(tree, r'TooltipListEmptyContent<[^>]+> \d+x[1-9]\d*@')

    def test_gallery_tooltips_use_native_header_and_two_sections(self):
        from eu5_gui_renderer.gui import Expander
        expander = Expander(self.resources.db)
        _, panel, _ = location.build(self.resources, expander, 560, 1080, menu=True)

        def visit(node):
            yield node
            for child in node.children:
                yield from visit(child)

        owners = [node for node in visit(panel) if re.fullmatch(
            r'tv_location_wonder_(?:(?:art|level)_\d+|ritual_\d+_[123])', str(node.props.get('name', '')))]
        self.assertEqual(len(owners), 25)
        for owner in owners:
            popup = expander.build_lazy(owner.tooltipwidget)
            nodes = list(visit(popup))
            self.assertEqual(sum(node.typename == 'ContextualTooltipHeader' for node in nodes), 1)
            sections = [node for node in nodes if node.props.get('name') in
                        ('tv_wonder_effects_section', 'tv_wonder_conditions_section', 'tv_wonder_history_section')]
            if '_art_' in owner.props['name']:
                self.assertEqual([node.typename for node in sections], ['TooltipRequirementsList', 'TooltipFlavorTextBlock'])
                self.assertIn('ShowTriggerConditionsForScope(', sections[0].props['textcontext'])
                self.assertIn('LocationView.GetLocation.MakeScope.Self', sections[0].props['textcontext'])
                continue
            self.assertEqual([node.typename for node in sections], ['TooltipListBase', 'TooltipFlavorTextBlock'])
            # Both reward scopes occupy the same full-width vertical section.
            row_parents = [parent for parent in visit(sections[0]) for node in parent.children
                           if node.typename == 'TooltipStringPairList']
            self.assertEqual(len(row_parents), 2)
            self.assertTrue(all(parent.kind == 'vbox' for parent in row_parents))

    def test_panel_has_no_tooltip_context_bindings_even_in_hidden_layers(self):
        from eu5_gui_renderer.gui import Expander
        expander = Expander(self.resources.db)
        _, _, panel = location.build(self.resources, expander, 560, 1080, menu=True)
        dependencies = []

        def check_values(value, path):
            if isinstance(value, str) and 'ExtraTooltipInfo.' in value:
                dependencies.append(f'{path}: {value}')
            elif isinstance(value, dict):
                for key, child in value.items():
                    if key != '__buttontext__':
                        check_values(child, f'{path}.{key}')
            elif isinstance(value, (list, tuple)):
                for index, child in enumerate(value):
                    check_values(child, f'{path}[{index}]')

        def visit(element, path):
            for field in ('props', 'backgrounds', 'modifies', 'glows', 'states'):
                check_values(getattr(element, field), f'{path}.{field}')
            for index, child in enumerate(element.children):
                visit(child, f'{path}/{child.typename}[{index}]')
            for spec in (element.item, element.props.get('__buttontext__')):
                if spec is not None:
                    visit(expander.build_lazy(spec), f'{path}/item')
            # Real tooltipwidget attachments receive ExtraTooltipInfo from the
            # engine. Only the persistent panel tree must be independent of it.

        visit(panel, panel.typename)
        self.assertEqual(dependencies, [])

    def test_panel_tracks_location_right_edge_at_different_widths(self):
        from eu5_gui_renderer.gui import Expander
        from eu5_gui_renderer.preview import render_tree, has_diagnostics
        with tempfile.TemporaryDirectory() as folder:
            for width in (560, 700):
                with self.subTest(width=width):
                    expander = Expander(self.resources.db)
                    root, panel, menu = location.build(self.resources, expander, width, 1080, menu=True)
                    # A visually correct scene child lost every gallery hover
                    # in game. Offline tooltip rendering bypasses hit testing.
                    self.assertIn(menu, panel.children)
                    report = render_tree(root, expander, self.resources,
                        location.scenario_mocks('multiple', self.resources), width=1420, height=1080,
                        output=Path(folder) / f'width_{width}.png')
                    self.assertFalse(has_diagnostics(report), report)
                    self.assertGreater(menu.w, 0)
                    self.assertAlmostEqual(menu.x, panel.x + panel.w)
                    def visit(node):
                        yield node
                        for child in node.children:
                            yield from visit(child)
                    scene = next(node for node in visit(panel)
                                 if node.props.get('name') == 'tv_location_city_appearance')
                    self.assertAlmostEqual(menu.y, scene.y)
                    self.assertGreater(menu.y, panel.y)

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
