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


if __name__ == "__main__":
    unittest.main()
