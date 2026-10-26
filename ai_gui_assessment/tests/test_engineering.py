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

    def test_survey_and_construction_tabs_preserve_panel_branches(self):
        for name, expected, absent in (
            ("survey", "TV_ENGINEERING_SURVEY_CARD_TITLE", "TV_ENGINEERING_CONCEPT_CARD_TITLE"),
            ("construction", "TV_ENGINEERING_CEREMONY_LOCKED_TEXT", "TV_ENGINEERING_CEREMONY_CHOOSE_STYLE_PROMPT"),
            ("construction-complete", "TV_WONDER_RITUAL_HEADER", "TV_ENGINEERING_CEREMONY_LOCKED_TEXT"),
        ):
            with self.subTest(state=name):
                root, engine, _, _ = self.page(name)
                nodes = list(self.visible_nodes(root, engine))
                keys = {node.props.get("text") for node in nodes}
                self.assertIn(expected, keys)
                self.assertNotIn(absent, keys)
                values = [engine.resolve(node.props.get("value")) for node in nodes if node.kind == "progressbar"]
                if name == 'construction-complete':
                    self.assertNotIn(100, values)  # Construction is folded during ritual selection.
                    self.assertIn('TV_ENGINEERING_CONSTRUCTION_FOLD', keys)
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
            else:
                self.assertFalse(any(action and action.startswith('tv_wonder_ritual_preview_') for action in actions))
                self.assertIn('TV_WONDER_RITUAL_LOCKED', {n.props.get('text') for n in nodes})
            if name == "reritual-ready":
                self.assertIn("tv_wonder_ritual_cancel_reritual", actions)
                self.assertNotIn("tv_wonder_ritual_choose_plain", actions)
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
        self.assertIn('TV_WONDER_RITUAL_PLAIN_CONSEQUENCE', {n.props.get('text') for n in nodes})
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

    def test_no_selection_disables_confirmation_and_seven_estates_wrap(self):
        state = engineering.scenario_state('ceremony-ready')
        player = {**state.player_variables, 'tv_wonder_ritual_choice': None}
        root, engine, ev, log = self.page(state.name, state=replace(state, player_variables=player))
        action = next(n for n in self.visible_nodes(root, engine)
                      if n.props.get('scripted_action_tooltip', {}).get('action_name') == 'tv_wonder_ritual_confirm')
        pushed = engine.push(action)
        try: self.assertFalse(ev.truthy(action.props['enabled']))
        finally: engine.pop(pushed)
        self.assertFalse(log, log)
        for estate in ('dhimmi_estate', 'tribes_estate', 'cossacks_estate'):
            player[f'tv_wonder_estate_pref_{estate}'] = 1
            player[f'tv_wonder_estate_pref_source_{estate}'] = 2
        player['tv_wonder_ritual_choice'] = 1
        root, engine, _, log = self.page(state.name, state=replace(state, player_variables=player))
        cards = [n for n in self.visible_nodes(root, engine) if n.typename == 'tv_wonder_ritual_estate_card']
        self.assertEqual(len(cards), 7)
        self.assertEqual(len({n.y for n in cards}), 4)
        self.assertTrue(all(0 <= n.x and n.x + n.w <= 570 for n in cards))
        self.assertFalse(log, log)

    def test_ritual_effect_samples_follow_selected_style_and_completion(self):
        state = engineering.scenario_state("ceremony-ready")
        first = engineering.ritual_effect_sample(state, self.loc)
        self.assertIn("海上贸易效率: +20%", first)
        self.assertIn("重商主义", first)
        second = engineering.ritual_effect_sample(replace(state, player_variables={
            **state.player_variables, "tv_wonder_ritual_choice": 2}), self.loc)
        self.assertIn("移民吸引力: +1", second)
        self.assertIn("+50%", second)
        self.assertNotIn("海上贸易效率", second)
        third = engineering.ritual_effect_sample(replace(state, player_variables={
            **state.player_variables, "tv_wonder_ritual_choice": 3}), self.loc)
        self.assertIn("杜卡特: +10000", third)
        self.assertIn("自由贸易", third)
        reritual = engineering.ritual_effect_sample(engineering.scenario_state("reritual-ready"), self.loc)
        self.assertIn("威望: +10", reritual)
        completed = engineering.ritual_effect_sample(engineering.scenario_state("finalized"), self.loc)
        self.assertIn("已发放", completed)
        self.assertNotIn("+20%", completed)

    def test_ritual_fixtures_render_current_choice_and_estate_reason(self):
        for style in (2, 3):
            state = engineering.load_fixture(engineering.scenario_state("ceremony-ready"),
                WORKSPACE / f"ai_gui_assessment/fixtures/ceremony_style_{style}.json")
            root, engine, _, log = self.page(state.name, state=state)
            nodes = list(self.visible_nodes(root, engine))
            self.assertIn("TV_WONDER_RITUAL_REASON_LOCATION", {n.props.get("text") for n in nodes})
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
