"""Guard the prototype's source-backed data and cross-panel consistency."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ai_gui_assessment"))
import org_logistics_mockups as preview


class OrgLogisticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        preview.engineering.configure()
        from eu5_gui_renderer.paths import GAME
        if not (GAME / "in_game/common/goods").is_dir():
            raise unittest.SkipTest("Installed game goods data required")

    def test_settlement_and_market_agree(self):
        m = preview.load_model("active")
        self.assertEqual(m["cap"], 12)
        self.assertAlmostEqual(m["effective"], 6.02)
        self.assertAlmostEqual(m["maintenance_total"], 1172.5)
        self.assertAlmostEqual(m["progress"], 4955.664)
        self.assertAlmostEqual(m["gap"], 22.4)
        market = m["market"]["tv_wonder_materials"]
        self.assertAlmostEqual(m["progress"] / (m["camp_progress"] * m["multiplier"]),
                               market["supply"] / market["demand"])

    def test_real_recipes_and_scarcest_input(self):
        recipes = preview.load_model("active")["recipes"]
        self.assertEqual(len(recipes), 8)
        self.assertEqual(recipes[0]["inputs"], {"clay": 4, "sand": 2, "lumber": .9, "fiber_crops": .3})
        self.assertEqual([r["status"] for r in recipes], ["hi", "hi", "mid", "ok", "mid", "hi", "mid", "hi"])
        self.assertTrue(all(r["produced"] == "tv_wonder_materials" for r in recipes))

    def test_supply_boundaries(self):
        self.assertEqual(preview.status(100, 100), "ok")
        self.assertEqual(preview.status(100, 70), "mid")
        self.assertEqual(preview.status(100, 69), "hi")
        self.assertEqual(preview.status(0, 0), "ok")

    def test_full_and_locked_samples(self):
        full = preview.load_model("full")
        self.assertEqual(full["progress"], 30000)
        self.assertEqual(full["gap"], 0)
        self.assertTrue(all(r["status"] == "ok" for r in full["recipes"]))
        locked = preview.load_model("locked")
        self.assertEqual(locked["progress"], 0)
        self.assertEqual(locked["maintenance_total"], 0)

    def test_missing_market_sample_is_not_invented(self):
        fixture = json.loads(preview.FIXTURE.read_text(encoding="utf-8"))
        del fixture["market"]["fiber_crops"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            with self.assertRaises(KeyError):
                preview.load_model("active", path)

    def test_full_buttons_disable_and_locked_card_hides_details(self):
        from eu5_gui_renderer.pdx import parse
        class Labels:
            def get(self, key):
                return key
        def named(nodes):
            found = {}
            for node in nodes:
                if isinstance(node.value, list):
                    props = {child.key: child.value for child in node.value}
                    if "name" in props:
                        found[props["name"]] = props
                    found.update(named(node.value))
            return found
        m = preview.load_model("full")
        nodes = named(parse(preview.organization(m, Labels()) + preview.logistics(m, Labels(), "sample.png")))
        self.assertEqual(nodes["build_camp"]["enabled"], "no")
        self.assertEqual(nodes["build_workshop"]["enabled"], "no")
        self.assertEqual(sum(k.startswith("method_") for k in nodes), 8)
        nodes = named(parse(preview.organization(preview.load_model("locked"), Labels())))
        self.assertEqual(nodes["build_camp"]["enabled"], "no")
        self.assertNotIn("maintenance", nodes)
        self.assertNotIn("stat_0", nodes)


if __name__ == "__main__":
    unittest.main()
