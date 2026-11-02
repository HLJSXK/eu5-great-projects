"""Exercise actual page branches with the selected game GUI and sample states."""
from pathlib import Path
from dataclasses import replace
import json
import sys
import tempfile
import unittest

WORKSPACE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WORKSPACE))
from ai_gui_assessment import engineering


class EngineeringPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engineering.configure()
        from eu5_gui_renderer.paths import GAME
        if not (GAME / "loading_screen/fonts").is_dir():
            raise unittest.SkipTest("Installed game assets required for page layout checks")
        from eu5_gui_renderer.preview import load_resources
        resources = load_resources()
        cls.db, cls.loc, cls.formats, cls.icons = resources.db, resources.loc, resources.formats, resources.icons

    def page(self, name, *, state=None, height=2400):
        from eu5_gui_renderer.data import Evaluator
        from eu5_gui_renderer.engine import Engine
        from eu5_gui_renderer.gui import Expander
        state = state or engineering.scenario_state(name)
        log = []
        ex = Expander(self.db, log)
        element = engineering.build(self.db, ex, state=state)
        ev = Evaluator(engineering.mocks(state, self.loc), self.loc, log)
        engine = Engine(ex, ev, self.loc, self.formats, self.icons, 1)
        engine.place(element, 0, 0, 570, height)
        return element, engine, ev, log

    def visible_nodes(self, element, engine):
        pushed = engine.push(element)
        try:
            if engine.visible(element):
                yield element
                for child in engine.vis_children(element):
                    yield from self.visible_nodes(child, engine)
        finally:
            engine.pop(pushed)

    def test_first_page_states_use_actual_gui_branches(self):
        for name, tab in engineering.STATE_TABS.items():
            if tab != "overview":
                continue
            with self.subTest(state=name):
                root, engine, _, log = self.page(name)
                nodes = list(self.visible_nodes(root, engine))
                keys = {node.props.get("text") for node in nodes}
                self.assertIn("TV_ENGINEERING_CONCEPT_CARD_TITLE", keys)
                self.assertEqual("TV_ENGINEERING_CONCEPT_ACTIONS_TITLE" in keys,
                                 name in ("debate", "support-reserve"))
                self.assertEqual("TV_ENGINEERING_CONCEPT_IN_PROGRESS_TEXT" in keys,
                                 name == "conception")
                self.assertFalse(engine.unsupported_textcontexts)
                self.assertFalse(any("StringPairList" in entry for entry in log), log)
                names = [node for node in nodes if "Character.GetNameToFit" in str(node.props.get("raw_text", ""))]
                self.assertEqual(bool(names), name != "no-engineer")
                self.assertTrue(all(node.w > 0 for node in names))
                self.assertEqual(engine.ev.item_stack, [])
                self.assertFalse(log, log)

    def test_end_debate_threshold_and_complete_page_bounds(self):
        for name, enabled, bar_value in (("debate", False, 68), ("support-reserve", True, 35)):
            with self.subTest(state=name):
                root, engine, ev, _ = self.page(name, height=1800)
                nodes = list(self.visible_nodes(root, engine))
                buttons = [node for node in nodes if node.props.get("scripted_action_tooltip", {}).get("action_name") == "tv_wonder_end_debate"]
                self.assertEqual(len(buttons), 1)
                button = buttons[0]
                pushed = engine.push(button)
                self.assertEqual(ev.truthy(button.props["enabled"]), enabled)
                engine.pop(pushed)
                self.assertGreater(button.w, 400)
                self.assertLess(button.y + button.h, 1670)
                values = [engine.resolve(node.props.get("value")) for node in nodes if node.kind == "progressbar"]
                self.assertIn(bar_value, values)

    def test_country_and_organization_variables_remain_distinct(self):
        from eu5_gui_renderer.data import Evaluator, Unknown
        state = engineering.scenario_state("conception")
        ev = Evaluator(engineering.mocks(state, self.loc), self.loc, [])
        self.assertEqual(ev.eval_str("[InternationalOrganizationsView.GetInternationalOrganization.MakeScope.GetVariable('tv_wonder_concept_progress').GetValue]"), 45)
        self.assertIsInstance(ev.eval_str("[InternationalOrganizationsView.GetPlayer.MakeScope.GetVariable('tv_wonder_concept_progress').GetValue]"), Unknown)

    def test_all_presets_resolve_actual_visible_gui(self):
        for name in engineering.STATE_NAMES:
            with self.subTest(state=name):
                root, engine, ev, log = self.page(name)
                missing = engine.missing_localizations | ev.missing_localizations
                self.assertFalse(log, log)
                self.assertFalse(engine.unresolved_contexts)
                self.assertFalse(engine.unsupported_textcontexts)
                self.assertFalse(missing, missing)
                self.assertEqual(engine.ev.item_stack, [])

    def test_all_card_variants_keep_width_and_expand_encyclopedia_help(self):
        for name in engineering.STATE_NAMES:
            with self.subTest(state=name):
                root, engine, ev, log = self.page(name)
                cards = [node for node in self.visible_nodes(root, engine)
                         if node.typename == 'tv_engineering_department_card_common']
                self.assertTrue(cards)
                self.assertTrue(all(card.w == 500 for card in cards),
                                [(card.x, card.w) for card in cards])
                if engineering.STATE_TABS[name] == 'custom':
                    self.assertEqual(len({(card.x, card.w) for card in cards}), 1)
                for card in cards:
                    nodes = list(self.visible_nodes(card, engine))
                    title = next(node.props['text'] for node in nodes
                                 if str(node.props.get('text', '')).endswith(('CARD_TITLE', 'ACTIONS_TITLE')))
                    owners = [node for node in nodes
                              if node.props.get('action_tooltip', {}).get('on_action') == "[OpenLateralView('encyclopedia')]"]
                    self.assertEqual(len(owners), 1)
                    owner = owners[0]
                    self.assertIsNotNone(owner.tooltipwidget)
                    popup = engine.ex.build_lazy(owner.tooltipwidget)
                    pushed = engine.push(owner)
                    # These buttons open the encyclopedia, without concept-link metadata.
                    ev.item_stack.append({'__type__': 'PdxGuiWidget', 'HasTooltipMetaGameConcept': False})
                    ev.item_stack.append({'__type__': 'ExtraTooltipInfo', 'GetTintColor': [1, 1, 1, 1],
                                          'TooltipIsReady': True, 'HasUIAction': False, 'GetUIAction': None})
                    try:
                        width, height = engine.measure(popup, 570)['hint']
                        engine.place(popup, 0, 0, width, height)
                        labels = [node for node in self.visible_nodes(popup, engine)
                                  if 'text' in node.props or 'raw_text' in node.props]
                        keys = {node.props.get('text') for node in labels}
                        self.assertIn(title, keys)
                        self.assertNotIn('Card title header', keys)
                        help_text = [node for node in labels
                                     if '_HELP_' in str(node.props.get('text', ''))]
                        self.assertTrue(help_text, title)
                        self.assertTrue(all(node.w > 0 and node.h > 0 and engine.text_of(node)
                                            for node in help_text))
                    finally:
                        ev.item_stack.pop()
                        ev.item_stack.pop()
                        engine.pop(pushed)
                self.assertFalse(log, log)
                self.assertFalse(engine.missing_text)
                self.assertFalse(engine.unresolved_contexts)

    def test_survey_and_construction_tabs_preserve_panel_branches(self):
        for name, expected, absent in (
            ("survey", "TV_ENGINEERING_SURVEY_CARD_TITLE", "TV_ENGINEERING_CONCEPT_CARD_TITLE"),
            ("construction", "TV_ENGINEERING_CEREMONY_LOCKED_TEXT", "TV_ENGINEERING_CEREMONY_CHOOSE_STYLE_PROMPT"),
            ("construction-complete", "TV_WONDER_RITUAL_SECTION_OPTIONS", "TV_ENGINEERING_CEREMONY_LOCKED_TEXT"),
        ):
            with self.subTest(state=name):
                root, engine, _, _ = self.page(name)
                nodes = list(self.visible_nodes(root, engine))
                keys = {node.props.get("text") for node in nodes}
                self.assertIn(expected, keys)
                self.assertNotIn(absent, keys)
                values = [engine.resolve(node.props.get("value")) for node in nodes if node.kind == "progressbar"]
                if name == 'construction-complete':
                    self.assertNotIn(100, values)  # Construction is over; only the summary remains.
                    summary = [node.props.get("name") for node in nodes
                               if node.props.get("name") == 'tv_wonder_construction_summary']
                    self.assertEqual(['tv_wonder_construction_summary'], summary)
                    self.assertNotIn('TV_ENGINEERING_CONSTRUCTION_FOLD', keys)
                    self.assertFalse([node for node in nodes
                                      if 'construction_details' in str(node.props.get('onclick', ''))])
                else:
                    self.assertIn(45 if name == "survey" else 42, values)

    def test_ritual_preview_progress_and_action_availability(self):
        state = replace(engineering.scenario_state("ceremony-ready"), action_availability={"tv_wonder_ritual_confirm": False})
        root, engine, ev, log = self.page(state.name, state=state)
        nodes = list(self.visible_nodes(root, engine))
        self.assertTrue(any("tv_wonder_ritual_apply_choice_effect" in str(n.props.get("raw_text", "")) for n in nodes))
        action = next(n for n in nodes if n.props.get("scripted_action_tooltip", {}).get("action_name") == "tv_wonder_ritual_confirm")
        pushed = engine.push(action)
        try: self.assertFalse(ev.truthy(action.props["enabled"]))
        finally: engine.pop(pushed)
        self.assertFalse(log, log)
        root, engine, _, log = self.page("ritual-progress")
        nodes = list(self.visible_nodes(root, engine))
        self.assertIn("TV_WONDER_RITUAL_PROGRESS", {n.props.get("text") for n in nodes})
        self.assertFalse(any(n.props.get("scripted_action_tooltip", {}).get("action_name") == "tv_wonder_ritual_confirm" for n in nodes))
        self.assertFalse(log, log)

    def test_unique_and_reritual_states_share_the_unified_card(self):
        for name in ("unique-ready", "unique-progress", "reritual-ready", "reritual-progress"):
            root, engine, _, log = self.page(name)
            nodes = list(self.visible_nodes(root, engine))
            actions = {n.props.get("scripted_action_tooltip", {}).get("action_name") for n in nodes}
            if name.endswith('-ready'):
                self.assertIn("tv_wonder_ritual_preview_1", actions)
                self.assertIn("tv_wonder_ritual_preview_plain", actions)
            else:
                self.assertFalse(any(action and action.startswith('tv_wonder_ritual_preview_') for action in actions))
                choices = [n for n in nodes if str(n.props.get('name', '')).startswith('tv_wonder_ritual_choice_')]
                self.assertEqual(len(choices), 1)
            self.assertNotIn("tv_wonder_ritual_cancel_reritual", actions)
            self.assertFalse(log, log)

    def test_ritual_sections_keep_requirements_before_effects_and_actions_below(self):
        for state_name, overrides in (
            ('ceremony-ready', {}), ('unique-ready', {}), ('reritual-ready', {}),
            ('ceremony-ready', {'tv_wonder_ritual_choice': None}),
            ('ceremony-ready', {'tv_wonder_ritual_choice': 0}),
            ('reritual-ready', {'tv_wonder_ritual_choice': 0}),
            ('ceremony-ready', {'tv_wonder_cmm_skip_ceremony': 1}),
        ):
            with self.subTest(state=state_name, overrides=overrides):
                state = engineering.scenario_state(state_name)
                state = replace(state, player_variables={**state.player_variables, **overrides})
                root, engine, _, log = self.page(state_name, state=state)
                nodes = list(self.visible_nodes(root, engine))
                ledger = next(n for n in nodes if n.props.get('name') == 'tv_wonder_ritual_ledger')
                self.assertEqual(ledger.children[0].props.get('name'), 'tv_wonder_ritual_section_options')
                sections = [n for n in ledger.children if str(n.props.get('name', '')).startswith('tv_wonder_ritual_section_')]
                self.assertEqual([n.props['name'] for n in sections], [
                    'tv_wonder_ritual_section_options', 'tv_wonder_ritual_section_requirements',
                    'tv_wonder_ritual_section_effects'])
                options, requirements, effects = sections
                options_nodes = list(self.visible_nodes(options, engine))
                choices = [n for n in options_nodes if str(n.props.get('name', '')).startswith('tv_wonder_ritual_choice_')]
                self.assertEqual(len(choices), 4)
                self.assertEqual({(n.x, n.w, n.h) for n in choices}, {(choices[0].x, 438, 42)})
                plain = next(n for n in choices if n.props['name'] == 'tv_wonder_ritual_choice_plain')
                labels = [n for n in self.visible_nodes(plain, engine)
                          if n.kind == 'textbox' and (n.props.get('text') or n.props.get('raw_text'))]
                self.assertEqual([n.props.get('text') for n in labels], ['TV_WONDER_RITUAL_PLAIN_STATE'])
                flavor = [n for n in options_nodes if 'TV_WONDER_RITUAL_DESC_' in str(n.props.get('raw_text', ''))]
                if state.player_variables.get('tv_wonder_ritual_choice') in (1, 2, 3):
                    self.assertEqual(len(flavor), 1)
                    self.assertLessEqual(plain.y + plain.h, flavor[0].y)
                    self.assertLessEqual(flavor[0].y + flavor[0].h, requirements.y)
                else:
                    self.assertFalse(flavor)
                for section, following in zip(sections, sections[1:]):
                    self.assertGreater(section.h, 24)
                    self.assertLessEqual(section.y + section.h, following.y)
                requirement_nodes = list(self.visible_nodes(requirements, engine))
                effect_nodes = list(self.visible_nodes(effects, engine))
                self.assertFalse(any('TV_WONDER_RITUAL_DESC_' in str(n.props.get('raw_text', '')) for n in effect_nodes))
                self.assertFalse(any(n.kind in ('progressbar', 'icon') for n in effect_nodes))
                self.assertFalse(any('apply_choice_effect' in str(n.props.get('raw_text', '')) for n in requirement_nodes))
                self.assertFalse(any('pay_effect' in str(n.props.get('raw_text', '')) for n in effect_nodes))
                self.assertNotIn('TV_WONDER_RITUAL_SECTION_VALUES', {n.props.get('text') for n in nodes})
                footer = next(n for n in ledger.children if n.props.get('name') == 'tv_wonder_ritual_actions')
                self.assertLessEqual(effects.y + effects.h, footer.y)
                buttons = [n for n in self.visible_nodes(footer, engine) if n.props.get('scripted_action_tooltip')]
                self.assertEqual(len(buttons), 1)
                self.assertFalse(log, log)

    def test_plain_choice_has_one_confirmation_and_no_ritual_effects(self):
        state = engineering.scenario_state('ceremony-ready')
        state = replace(state, player_variables={**state.player_variables, 'tv_wonder_ritual_choice': 0})
        root, engine, _, log = self.page(state.name, state=state)
        nodes = list(self.visible_nodes(root, engine))
        actions = {n.props.get('scripted_action_tooltip', {}).get('action_name') for n in nodes}
        self.assertIn('tv_wonder_ritual_preview_plain', actions)
        self.assertIn('tv_wonder_ritual_choose_plain', actions)
        self.assertNotIn('tv_wonder_ritual_confirm', actions)
        self.assertFalse(any('ShowScriptedEffectForScope' in str(n.props.get('raw_text', '')) for n in nodes))
        self.assertNotIn('TV_WONDER_RITUAL_PLAIN_CONSEQUENCE', {n.props.get('text') for n in nodes})
        self.assertFalse(log, log)

        reritual = engineering.scenario_state('reritual-ready')
        reritual = replace(reritual, player_variables={**reritual.player_variables, 'tv_wonder_ritual_choice': 0})
        root, engine, _, log = self.page(reritual.name, state=reritual)
        nodes = list(self.visible_nodes(root, engine))
        self.assertFalse(any('ShowScriptedEffectForScope' in str(n.props.get('raw_text', '')) for n in nodes))
        keys = {n.props.get('text') for n in nodes}
        self.assertTrue({'TV_WONDER_RITUAL_PLAIN_TERMS', 'TV_WONDER_RITUAL_PLAIN_DETAIL'} <= keys)
        for action in ('tv_wonder_ritual_preview_plain', 'tv_wonder_ritual_choose_plain'):
            widget = next(n for n in nodes if n.props.get('scripted_action_tooltip', {}).get('action_name') == action)
            pushed = engine.push(widget)
            try: self.assertTrue(engine.ev.truthy(widget.props['enabled']))
            finally: engine.pop(pushed)
        self.assertFalse(log, log)
        inherited = engineering.scenario_state('finalized')
        inherited = replace(inherited, player_variables={**inherited.player_variables,
            'tv_wonder_ritual_choice': None, 'tv_wonder_finalization_outcome': 9})
        root, engine, _, log = self.page(inherited.name, state=inherited)
        keys = {n.props.get('text') for n in self.visible_nodes(root, engine)}
        # Dedicated expansions reuse the existing ritual and hide this card.
        self.assertNotIn('TV_WONDER_RITUAL_COMPLETE_PENDING', keys)
        self.assertNotIn('TV_WONDER_RITUAL_PLAIN_COMPLETE', keys)
        self.assertFalse(log, log)

    def test_no_selection_disables_confirmation_and_shows_supporters(self):
        state = engineering.scenario_state('ceremony-ready')
        player = {**state.player_variables, 'tv_wonder_ritual_choice': None}
        root, engine, ev, log = self.page(state.name, state=replace(state, player_variables=player))
        action = next(n for n in self.visible_nodes(root, engine)
                      if n.props.get('scripted_action_tooltip', {}).get('action_name') == 'tv_wonder_ritual_confirm')
        pushed = engine.push(action)
        try: self.assertFalse(ev.truthy(action.props['enabled']))
        finally: engine.pop(pushed)
        self.assertFalse(log, log)
        supporters = [n for n in self.visible_nodes(root, engine) if n.typename == 'tv_wonder_ritual_supporter']
        expected = {key.removeprefix('tv_wonder_estate_pref_') for key, value in player.items()
                    if key.startswith('tv_wonder_estate_pref_') and not key.startswith('tv_wonder_estate_pref_source_')
                    and value in (1, 2, 3)}
        self.assertEqual({n.props['name'] for n in supporters}, expected)

    def test_supporters_follow_each_choice_without_gaps_or_overlaps(self):
        estates = ('nobles_estate', 'clergy_estate', 'burghers_estate', 'peasants_estate',
                   'dhimmi_estate', 'tribes_estate', 'cossacks_estate')
        state = engineering.scenario_state('ceremony-ready')
        for active in ((), (0,), (0, 2, 5), tuple(range(7))):
            with self.subTest(active=active):
                player = dict(state.player_variables)
                for i, estate in enumerate(estates):
                    player[f'tv_wonder_estate_pref_{estate}'] = 1 if i in active else None
                    player[f'tv_wonder_estate_pref_source_{estate}'] = 2 if i in active else None
                root, engine, _, log = self.page(state.name, state=replace(state, player_variables=player))
                nodes = list(self.visible_nodes(root, engine))
                flow = next(n for n in nodes if n.props.get('name') == 'tv_wonder_ritual_supporters_1')
                # dynamicgridbox accepted by the offline renderer previously
                # failed in game: its spacing property is not supported.
                self.assertEqual(flow.kind, 'flowcontainer')
                icons = [n for n in nodes if n.typename == 'tv_wonder_ritual_supporter']
                self.assertEqual([n.props['name'] for n in icons], [estates[i] for i in active])
                self.assertEqual(len({n.y for n in icons}), int(bool(active)))
                choice = next(n for n in nodes if n.props.get('name') == 'tv_wonder_ritual_choice_1')
                next_choice = next(n for n in nodes if n.props.get('name') == 'tv_wonder_ritual_choice_2')
                self.assertEqual(choice.h, 42)
                labels = [n for n in self.visible_nodes(choice, engine) if n.kind == 'textbox' and n.props.get('raw_text')]
                self.assertEqual(len(labels), 1)
                for i, icon in enumerate(icons):
                    self.assertGreaterEqual(icon.y, choice.y + choice.h)
                    self.assertLessEqual(icon.y + icon.h, next_choice.y)
                    self.assertGreaterEqual(icon.x, flow.x)
                    self.assertLessEqual(icon.x + icon.w, flow.x + flow.w)
                    if i:
                        self.assertEqual(icon.x - icons[i - 1].x, 46)
                    self.assertIsNotNone(icon.tooltipwidget)
                    self.assertIn(f"GetEstateFromKey('{icon.props['name']}')", icon.props['datacontext'])
                    badge = next(n for n in self.visible_nodes(icon, engine) if n.props.get('name') == 'support_badge')
                    self.assertEqual(badge.props['alwaystransparent'], 'yes')
                    self.assertGreaterEqual(badge.x, icon.x)
                    self.assertGreaterEqual(badge.y, icon.y)
                    self.assertLessEqual(badge.x + badge.w, icon.x + icon.w)
                    self.assertLessEqual(badge.y + badge.h, icon.y + icon.h)
                self.assertFalse(any(n.typename == 'tv_wonder_ritual_estate_card' for n in nodes))
                arrows = [n for n in nodes if n.props.get('raw_text') in ('#Y ←#!', '#Y →#!')]
                self.assertFalse(arrows)
                self.assertFalse(log, log)

    def test_supporter_tooltips_resolve_each_estate_and_its_cached_reason(self):
        estates = ('nobles_estate', 'clergy_estate', 'burghers_estate', 'peasants_estate',
                   'dhimmi_estate', 'tribes_estate', 'cossacks_estate')
        reasons = {1: 'LOCATION', 2: 'HISTORICAL', 3: 'RANDOM'}
        state = engineering.scenario_state('ceremony-ready')
        for offset in range(3):
            player = {**state.player_variables, 'tv_wonder_ritual_choice': 3}
            for i, estate in enumerate(estates):
                player[f'tv_wonder_estate_pref_{estate}'] = i % 3 + 1
                player[f'tv_wonder_estate_pref_source_{estate}'] = (i + offset) % 3 + 1
            root, engine, ev, log = self.page(state.name, state=replace(state, player_variables=player))
            owners = [n for n in self.visible_nodes(root, engine) if n.typename == 'tv_wonder_ritual_supporter']
            self.assertEqual(len(owners), 7)
            for owner in owners:
                estate = owner.props['name']
                with self.subTest(estate=estate, reason_offset=offset):
                    popup = engine.ex.build_lazy(owner.tooltipwidget)
                    pushed = engine.push(owner)
                    ev.item_stack.append({'__type__': 'ExtraTooltipInfo', 'GetTintColor': [1, 1, 1, 1],
                                          'TooltipIsReady': True, 'HasUIAction': False, 'GetUIAction': None})
                    try:
                        width, height = engine.measure(popup, 570)['hint']
                        engine.place(popup, 0, 0, width, height)
                        nodes = list(self.visible_nodes(popup, engine))
                        self.assertEqual(sum(n.typename == 'ContextualTooltipHeader' for n in nodes), 1)
                        self.assertEqual(sum(n.typename == 'TooltipTextBlock' for n in nodes), 1)
                        labels = [n for n in nodes if n.props.get('text') in {
                            'TV_WONDER_RITUAL_ESTATE_SUPPORTS_STYLE',
                            *(f'TV_WONDER_RITUAL_SUPPORT_REASON_{label}' for label in reasons.values())}]
                        self.assertEqual(len(labels), 2)
                        title, reason = labels
                        self.assertIn(self.loc.get(estate), engine.text_of(title))
                        self.assertIn('当前#G 支持#!该仪式风格', engine.text_of(title))
                        source = player[f'tv_wonder_estate_pref_source_{estate}']
                        self.assertEqual(engine.text_of(reason), self.loc.get(f'TV_WONDER_RITUAL_SUPPORT_REASON_{reasons[source]}'))
                        self.assertGreaterEqual(reason.y, title.y + title.h)
                        self.assertLessEqual(reason.x + reason.w, popup.x + popup.w)
                    finally:
                        ev.item_stack.pop()
                        engine.pop(pushed)
            self.assertFalse(log, log)
            self.assertFalse(engine.missing_text)
            self.assertFalse(engine.unresolved_contexts)

    def test_ritual_effect_samples_follow_selected_style_and_completion(self):
        state = engineering.scenario_state("ceremony-ready")
        first = engineering.ritual_effect_sample(state, self.loc)
        self.assertIn("海上贸易效率: +20%", first)
        self.assertIn("重商主义", first)
        self.assertNotIn("价值观向", first)
        self.assertNotIn("Societal change towards", first)
        second = engineering.ritual_effect_sample(replace(state, player_variables={
            **state.player_variables, "tv_wonder_ritual_choice": 2}), self.loc)
        self.assertIn("移民吸引力: +1", second)
        self.assertIn("每月海权主义倾向: +0.1", second)
        self.assertNotIn("海上贸易效率", second)
        third = engineering.ritual_effect_sample(replace(state, player_variables={
            **state.player_variables, "tv_wonder_ritual_choice": 3}), self.loc)
        self.assertIn("杜卡特: +10000", third)
        self.assertIn("自由贸易", third)
        reritual = engineering.ritual_effect_sample(engineering.scenario_state("reritual-ready"), self.loc)
        self.assertEqual(reritual, first)
        completed = engineering.ritual_effect_sample(engineering.scenario_state("finalized"), self.loc)
        self.assertIn("已发放", completed)
        self.assertNotIn("+20%", completed)

    def test_ritual_fixtures_render_supporters_under_their_preferred_style(self):
        for style in (2, 3):
            state = engineering.load_fixture(engineering.scenario_state("ceremony-ready"),
                WORKSPACE / f"ai_gui_assessment/fixtures/ceremony_style_{style}.json")
            root, engine, _, log = self.page(state.name, state=state)
            nodes = list(self.visible_nodes(root, engine))
            for n in (1, 2, 3):
                row = next(node for node in nodes if node.props.get('name') == f'tv_wonder_ritual_supporters_{n}')
                icons = [node for node in self.visible_nodes(row, engine) if node.typename == 'tv_wonder_ritual_supporter']
                self.assertEqual({node.props['name'] for node in icons}, {
                    key.removeprefix('tv_wonder_estate_pref_') for key, value in state.player_variables.items()
                    if key.startswith('tv_wonder_estate_pref_') and not key.startswith('tv_wonder_estate_pref_source_') and value == n})
            confirm = next(n for n in nodes if n.props.get("scripted_action_tooltip", {}).get("action_name") == "tv_wonder_ritual_confirm")
            pushed = engine.push(confirm)
            try: self.assertEqual(engine.ev.truthy(confirm.props["enabled"]), style == 2)
            finally: engine.pop(pushed)
            self.assertFalse(log, log)

    def test_ritual_detail_is_exported_by_the_shared_pipeline(self):
        from eu5_gui_renderer.preview import RenderResources, has_diagnostics
        resources = RenderResources(self.db, self.loc, self.formats, self.icons)
        with tempfile.TemporaryDirectory() as folder:
            for name in ("ceremony-ready", "construction"):
                with self.subTest(state=name):
                    output = Path(folder) / f"{name}.png"
                    report = engineering.render(engineering.scenario_state(name), output=output, resources=resources)
                    self.assertFalse(has_diagnostics(report))
                    self.assertEqual("ritual" in report["details"], name == "ceremony-ready")
                    if name == "ceremony-ready":
                        self.assertEqual(Path(report["details"]["ritual"]), output.with_name(f"{name}_ritual.png"))
                        self.assertTrue(Path(report["details"]["ritual"]).is_file())
                    self.assertEqual(json.loads(output.with_name(f"{name}_report.json").read_text(encoding="utf-8")), report)

    def test_priority_mockup_replaces_native_list_and_keeps_actual_preview(self):
        from ai_gui_assessment import priority_proposal_mockups as mockup
        from eu5_gui_renderer.gui import Expander
        state, _ = mockup.scenario()
        expander = Expander(self.db)
        root = engineering.build(self.db, expander, state=state)
        previews = {id(node) for node in mockup.walk(root)
                    if node.props.get("text") == "TV_ENGINEERING_WONDER_PREVIEW_EFFECT_TITLE"}
        self.assertTrue(previews)
        mockup.splice(root, self.db, expander, mockup.MOCKUP_DIR / mockup.SCHEMES["a"][0], True)
        nodes = list(mockup.walk(root))
        self.assertTrue(previews.issubset({id(node) for node in nodes}))
        self.assertEqual(sum(node.props.get("text") == "TV_ENGINEERING_PRIORITY_UNFINISHED_HEADER" for node in nodes), 1)
        self.assertFalse(any(node.props.get("text") == "TV_ENGINEERING_PROPOSAL_NEEDS_ENGINEER_TEXT" for node in nodes))


class ScenarioFixtureTests(unittest.TestCase):
    def test_ritual_presets_match_source_identity_duration_and_estates(self):
        from scripts_engineering_department.wonder_mechanics.rituals import ritual_styles
        wonders, mechanics = engineering.wonder_data()
        for name in ("ceremony-ready", "ritual-progress", "unique-ready", "unique-progress", "reritual-ready"):
            with self.subTest(state=name):
                state = engineering.scenario_state(name)
                player = state.player_variables
                wonder = next(w for w in wonders if w["id"] == player["tv_wonder_locked"])
                self.assertEqual(player["tv_wonder_locked_is_unique"], int(wonder["is_unique"]))
                self.assertEqual(player["tv_wonder_locked_size"], ("small", "medium", "large").index(wonder["size"]) + 1)
                self.assertEqual(player["tv_wonder_ritual_duration_months"], mechanics["ritual_rules"]["duration_months"])
                self.assertEqual(player["tv_wonder_estate_pref_source_burghers_estate"], 1)
                self.assertIsNone(player["tv_wonder_estate_pref_dhimmi_estate"])
                if wonder["is_unique"]:
                    self.assertEqual(state.objects["tv_wonder_site.GetLocation"]["Self"], wonder["location"])
                    self.assertEqual(player["tv_wonder_locked_mechanic_id"], 5)
                if name.endswith("progress"):
                    self.assertAlmostEqual(player["tv_wonder_ritual_progress_pct"],
                        player["tv_wonder_ritual_months_completed"] / player["tv_wonder_ritual_duration_months"] * 100)
                self.assertEqual(player["tv_wonder_estate_pref_burghers_estate"],
                    ritual_styles(wonder, mechanics)[0]["estate_preferences"]["burghers_estate"])

    def fixture(self, payload):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "fixture.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return engineering.load_fixture(engineering.scenario_state("ceremony-ready"), path)

    def test_overrides_preserve_scope_separation_and_preset(self):
        state = self.fixture({"tab": "resolutions", "player_variables": {"tv_wonder_ritual_choice": None},
                              "organization_variables": {"tv_wonder_domestic_support": 100},
                              "action_availability": {"tv_wonder_ritual_confirm": False}})
        self.assertEqual(state.tab, "resolutions")
        self.assertIsNone(state.player_variables["tv_wonder_ritual_choice"])
        self.assertEqual(state.organization_variables["tv_wonder_domestic_support"], 100)
        self.assertNotIn("tv_wonder_domestic_support", state.player_variables)
        self.assertEqual(engineering.scenario_state("ceremony-ready").player_variables["tv_wonder_ritual_choice"], 1)

    def test_invalid_fixtures_fail_before_rendering(self):
        for payload in ([1], {"unknown": 1}, {"tab": "invalid"}, {"objects": {"site": {}}},
                        {"action_availability": {"action": 1}}, {"player_variables": {"id": "3"}},
                        {"lists": {"x": {}}}, {"engineer_name": 12}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                self.fixture(payload)



if __name__ == "__main__":
    unittest.main()
