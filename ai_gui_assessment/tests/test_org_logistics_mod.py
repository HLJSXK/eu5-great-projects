"""Check the actual mod instance, including scroll bounds and native actions."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"ai_gui_assessment"))
import engineering
import org_logistics


class OrgLogisticsModTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engineering.configure()
        from eu5_gui_renderer.paths import GAME
        if not (GAME/"loading_screen/fonts").is_dir():
            raise unittest.SkipTest("Installed game resources required")
        from eu5_gui_renderer.preview import load_resources
        cls.resources = load_resources()

    def page(self, state):
        from eu5_gui_renderer.data import Evaluator
        from eu5_gui_renderer.engine import Engine
        from eu5_gui_renderer.gui import Expander
        r = self.resources
        ex = Expander(r.db)
        root = engineering.build(r.db, ex, state=state)
        ev = Evaluator(engineering.mocks(state, r.loc), r.loc, ex.log)
        engine = Engine(ex, ev, r.loc, r.formats, r.icons, 1)
        engine.place(root, 0, 0, 570, 3200)
        def walk(node):
            pushed = engine.push(node)
            try:
                if engine.visible(node):
                    yield node
                    for child in engine.vis_children(node):
                        yield from walk(child)
            finally:
                engine.pop(pushed)
        nodes = list(walk(root))
        self.assertFalse(ex.log, ex.log)
        return nodes, engine

    def test_three_states_use_real_widgets_and_preserve_full_graph(self):
        for state in ("active", "full", "locked"):
            with self.subTest(state=state):
                nodes, engine = self.page(org_logistics.scenario(state, self.resources.loc))
                panels = [n for n in nodes if n.typename.startswith("tv_org_logistics_")]
                self.assertEqual(len(panels), 1)
                self.assertEqual(panels[0].typename, "tv_org_logistics_locked" if state=="locked" else "tv_org_logistics_active")
                self.assertEqual(sum(n.props.get("name", "").startswith("method_") for n in nodes), 0 if state=="locked" else 8)
                goods = [n for n in nodes if n.typename in ("production_method_good", "production_method_good_small")]
                if state != "locked":
                    expected_inputs = sum(len(recipe[1]) for recipe in org_logistics.gen.inputs()[1])
                    self.assertEqual(len(goods), expected_inputs + 8)
                    rows = [n for n in nodes if n.props.get("name") == "method_row"]
                    self.assertTrue(all(row.w == 480 and row.h == 40 for row in rows))
                    self.assertTrue(all(left.y+left.h <= right.y for left,right in zip(rows,rows[1:])))
                self.assertLessEqual(panels[0].x+panels[0].w, 570)
                self.assertLessEqual(panels[0].y+panels[0].h, 3200)
                buttons = [n for n in nodes if n.props.get("name", "").startswith("build_camp")]
                if state == "locked":
                    self.assertFalse(buttons)
                    text = [n.props.get("text") for n in nodes
                            if panels[0].y <= n.y < panels[0].y + panels[0].h
                            and n.kind == "textbox"]
                    self.assertEqual(text, ["TV_ENGINEERING_ORG_LOG_CARD_TITLE",
                                            "TV_ENGINEERING_ORG_LOG_LOCKED_TEXT"])
                    self.assertEqual(panels[0].h, 144)
                    continue
                self.assertEqual(len(buttons), 1)
                enabled = engine.resolve(buttons[0].props["enabled"])
                self.assertEqual(enabled not in (False, "no"), state=="active")
                self.assertIn("uses_tv_wonder_materials", str(buttons[0].props["action_tooltip"]))

    def test_unlimited_cap_is_not_clamped_to_the_design_sample(self):
        state = org_logistics.scenario("full")
        state = replace(state, player_variables={**state.player_variables, "tv_wonder_organization_site_level_cap":100, "tv_wonder_organization_site_level_cap_display":100})
        nodes, engine = self.page(state)
        camp = next(n for n in nodes if n.props.get("name")=="build_camp")
        self.assertTrue(engine.resolve(camp.props["enabled"]))
        bar = next(n for n in nodes if n.kind=="progressbar" and "organization_site_level_cap_display" in str(n.props.get("max")))
        self.assertEqual(engine.resolve(bar.props["max"]), 100)

    def test_compact_summary_keeps_goods_and_build_button_inside_its_bounds(self):
        nodes, engine = self.page(org_logistics.scenario("active", self.resources.loc))
        named = {n.props.get("name"): n for n in nodes if n.props.get("name")}
        summary = named["ol_organization_summary"]
        self.assertLessEqual(summary.h, 320)
        self.assertNotIn("stat_0", named)
        self.assertNotIn("ol_org_header", named)
        rows = [named["resource_tools"], named["resource_tv_wonder_materials"]]
        self.assertLessEqual(rows[0].y+rows[0].h, rows[1].y)
        self.assertLessEqual(rows[1].y+rows[1].h, named["build_camp"].y)
        self.assertLessEqual(named["build_camp"].y+named["build_camp"].h, summary.y+summary.h)
        self.assertLessEqual(summary.y+summary.h, named["ol_log_header"].y)
        for row in rows:
            self.assertGreaterEqual(row.x, summary.x)
            self.assertLessEqual(row.x+row.w, summary.x+summary.w)
        action = str(named["build_camp"].props["action_tooltip"])
        self.assertIn("ShowProductionViewWithMarketAndFilter", action)
        self.assertIn("GetVariable('tv_wonder_site').GetLocation.GetMarket.Self", action)

    def test_summary_reads_real_cache_values_and_shows_demand_before_supply(self):
        base = org_logistics.scenario("active", self.resources.loc)
        for supplied, color in ((120, "#R"), (160, "#G")):
            with self.subTest(supply=supplied):
                state = replace(base, player_variables={**base.player_variables,
                    "tv_ol_camp_progress": 1234, "tv_ol_maintenance": 987.65,
                    "tv_ol_tools_price": 6.35, "tv_ol_tools_demand": 150,
                    "tv_ol_tools_supply": supplied, "tv_ol_levels": 7,
                    "tv_ol_input_efficiency": 0.42, "tv_wonder_logistics_progress_percent": 135})
                nodes, engine = self.page(state)
                named = {n.props.get("name"): n for n in nodes if n.props.get("name")}
                self.assertIn("1234", engine.text_of(named["camp_progress_value"]).replace(",", ""))
                self.assertIn("987.65", engine.text_of(named["maintenance_value"]))
                self.assertIn("6.35", engine.text_of(named["price_tools"]))
                self.assertIn("×7", engine.text_of(named["camp_flow_name"]))
                self.assertIn("42%", engine.text_of(named["camp_supply_value"]))
                self.assertNotIn("135", engine.text_of(named["camp_supply_value"]))
                rendered = engine.text_of(named["demand_supply_tools"])
                self.assertIn(f"150.0 / {supplied}.0", rendered)
                self.assertIn(color, rendered)
                for name, reference in (
                    ("worksite_building_reference", "ShowBuildingTypeName('tv_wonder_labor_camp')"),
                    ("goods_reference_tools", "ShowGoodsName('tools')"),
                    ("goods_reference_tv_wonder_materials", "ShowGoodsName('tv_wonder_materials')"),
                ):
                    self.assertIn(reference, named[name].props["raw_text"])
                    self.assertTrue(engine.text_of(named[name]))
                self.assertFalse(engine.missing_text)
                self.assertFalse(engine.missing_localizations)

    def test_employment_equation_displays_people_and_keeps_four_cards_separate(self):
        base = org_logistics.scenario("active", self.resources.loc)
        state = engineering.load_fixture(base, ROOT/"ai_gui_assessment/fixtures/worksite_employment.json")
        nodes, engine = self.page(state)
        named = {n.props.get("name"): n for n in nodes if n.props.get("name")}
        self.assertIn("2000", engine.text_of(named["base_progress_value"]).replace(",", ""))
        self.assertIn("1282 / 4000", engine.text_of(named["employment_value"]).replace(",", ""))
        self.assertIn("641", engine.text_of(named["camp_progress_value"]))
        self.assertIn("369.74", engine.text_of(named["maintenance_value"]))
        row = named["worksite_calculation"]
        cards = [named[key] for key in ("base_progress_card", "employment_card", "camp_progress_card", "maintenance_card")]
        for card in cards:
            self.assertEqual(card.y, row.y)
            self.assertEqual(card.h, 64)
            self.assertGreaterEqual(card.x, row.x)
            self.assertLessEqual(card.x+card.w, row.x+row.w)
        self.assertTrue(all(left.x+left.w < right.x for left, right in zip(cards, cards[1:])))
        self.assertLessEqual(row.y+row.h, named["resource_tools"].y)
        self.assertFalse(engine.missing_text)
        self.assertFalse(engine.missing_localizations)


if __name__ == "__main__":
    unittest.main()
