"""Production cache lifecycle and generated-source contracts."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts_engineering_department import gen_wonder_org_logistics as gen


class OrgLogisticsSourceTests(unittest.TestCase):
    def test_generated_text_is_fresh_and_bom_encoded(self):
        for rel, content in gen.outputs().items():
            with self.subTest(path=rel):
                raw = (ROOT/rel).read_bytes()
                self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
                self.assertEqual(raw.decode("utf-8-sig"), content)

    def test_cache_is_country_owned_and_published_after_local_calculation(self):
        source = gen.effects()
        self.assertIn("save_scope_as = tv_ol_owner", source)
        self.assertIn("scope:tv_ol_owner = {", source)
        self.assertIn("prev.building_employed_amount", source)
        self.assertIn("prev.building_employment_size_amount", source)
        self.assertNotIn("value = var:tv_ol_", source)
        self.assertIn("local_var:tv_ol_workers > 0", source)
        self.assertIn("local_var:tv_ol_camp_progress > 0", source)
        for name in gen.variables():
            self.assertIn(f"remove_variable = tv_ol_{name}", source)
            self.assertIn(f"remove_local_variable = tv_ol_{name}", source)
        published = source.index("set_variable = {")
        self.assertGreater(published, source.rindex("set_local_variable = {"))

    def test_refresh_and_cleanup_follow_existing_lifecycle(self):
        source = (ROOT/"src/in_game/common/scripted_effects/tv_engineering_department_effects.txt").read_text(encoding="utf-8-sig")
        self.assertRegex(source, r"tv_wonder_update_logistics_metrics_effect = yes\s+tv_wonder_update_org_logistics_display_effect = yes")
        for effect in ("tv_wonder_clear_current_survey_effect", "tv_wonder_clear_project_state_core_effect"):
            self.assertRegex(source, effect+r" = \{\s+tv_wonder_clear_org_logistics_display_effect = yes")
        gui = gen.gui()
        self.assertNotIn("Execute", gui)
        self.assertNotIn("ScriptedGui", gui)
        self.assertIn("tv_wonder_organization_site_level_cap_display", gui)
        self.assertIn("tv_wonder_monthly_construction_progress", gui)

    def test_native_method_list_has_typed_building_source_and_cleanup(self):
        source = gen.effects()
        self.assertIn("value = building_type:tv_wonder_material_dispatch_point", source)
        self.assertIn("remove_variable = tv_ol_workshop_type", source)
        self.assertNotIn("tv_ol_method_0_status", source)
        gui = gen.gui()
        self.assertIn(".GetVariable('tv_ol_workshop_type').GetBuildingType", gui)
        self.assertIn("BuildingType.GetPossibleProductionMethods", gui)
        self.assertIn("PossibleProductionMethods.GetMethods", gui)
        self.assertIn("using = production_method_simple", gui)
        self.assertNotIn("ChangeBuildingProductionMethod", gui)


if __name__ == "__main__":
    unittest.main()
