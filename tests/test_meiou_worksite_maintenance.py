"""Execute the adapter with an explicit upstream pricing result, not a price emulator."""
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

from scripts.compat import gen_tv_meiou_and_taxes_worksite_maintenance as gen
from scripts_engineering_department import gen_wonder_org_logistics as base
from test_wonder_priority_proposals import child, parse, walk

ROOT = Path(__file__).resolve().parents[1]


class Adapter:
    """Small generated-effect executor; upstream pricing is the tested boundary."""
    def __init__(self, *, worksite=True, opened=True, level=2, government=False):
        self.locals = {"tv_ol_worksite": "building"} if worksite else {}
        self.variables = {}
        self.scopes = {}
        self.powers = {"crown": Decimal(".2"), "nobles": Decimal(".3"), "clergy": Decimal(".5")}
        self.opened, self.level, self.government = opened, level, government
        self.priced = 0
        self.definitions = {n.key.removeprefix("REPLACE:"): n.children for n in parse(gen.effects())}

    def value(self, source, context, estate):
        if isinstance(source, tuple):
            value = self.value(child(source, "value").value, context, estate)
            for node in source:
                if node.key == "multiply":
                    value *= self.value(node.value, context, estate)
            return value
        source = source.strip('"').replace("$estate$", estate)
        if source.startswith("local_var:"):
            return self.locals[source.removeprefix("local_var:")]
        if source in ("epbm_cost_share", "epbm_inflation_factor"):
            assert context == "country", "EPBM's country values must use country scope"
            return {"epbm_cost_share": Decimal(".5"), "epbm_inflation_factor": Decimal("1.25")}[source]
        if source.startswith("estate_power("):
            assert context == "country"
            return self.powers[source.split(":", 1)[1].removesuffix("_estate)")]
        return Decimal(source)

    def condition(self, nodes, estate):
        for node in nodes:
            key = node.key.replace("$estate$", estate)
            if key == "has_local_variable": result = node.value in self.locals
            elif key == "is_opened": result = self.opened
            elif key == "building_level": result = self.level > int(node.value)
            elif key == "building_category": result = self.government
            elif key == "country_has_estate": result = estate in self.powers
            elif key.startswith("local_var:"): result = self.locals[key.removeprefix("local_var:")] == Decimal(node.value)
            else: raise AssertionError(f"Unsupported adapter condition {node}")
            if not result: return False
        return True

    def run(self, nodes, context="country", estate=""):
        for node in nodes:
            key = node.key.replace("$estate$", estate)
            if key == "if":
                if self.condition(child(node.children, "limit").children, estate):
                    self.run(tuple(n for n in node.children if n.key != "limit"), context, estate)
            elif key in ("set_local_variable", "set_variable", "change_local_variable"):
                name = child(node.children, "name").value.replace("$estate$", estate)
                store = self.variables if key == "set_variable" else self.locals
                if key == "set_variable":
                    assert context == "country"
                    assert name.startswith("tv_ol_mt_"), "Display may not write EPBM's ledger"
                if key == "change_local_variable":
                    store[name] *= self.value(child(node.children, "multiply").value, context, estate)
                else:
                    store[name] = self.value(child(node.children, "value").value, context, estate)
            elif key in ("remove_variable", "remove_local_variable"):
                (self.variables if key == "remove_variable" else self.locals).pop(node.value, None)
            elif key == "save_temporary_scope_as": self.scopes[node.value] = context
            elif key == "epbm_price_building":
                assert context == "building"
                assert self.scopes == {"epbm_bldg": "building", "epbm_bt": "building_type", "epbm_mkt": "market"}
                self.priced += 1
                self.locals["epbm_bldg_cost"] = Decimal("160")
            elif key == "epbm_for_each_estate":
                helper = child(node.children, "effect").value
                for member in gen.estates(): self.run(self.definitions[helper], context, member)
            elif key in ("local_var:tv_ol_worksite", "building_type", "location", "market", "scope:tv_ol_owner"):
                target = {"local_var:tv_ol_worksite": "building", "scope:tv_ol_owner": "country"}.get(key, key)
                self.run(node.children, target, estate)
            else: raise AssertionError(f"Unexpected adapter effect {node}")


@pytest.mark.parametrize("government", [False, True])
def test_generated_adapter_prices_in_building_scope_and_splits_in_country_scope(government):
    adapter = Adapter(government=government)
    adapter.run(adapter.definitions["tv_wonder_update_worksite_maintenance_display_effect"])
    assert adapter.priced == 1
    assert adapter.variables["tv_ol_mt_total"] == 100  # Stub pricing 160, share .5, inflation 1.25.
    assert adapter.variables["tv_ol_mt_crown"] == (100 if government else 20)
    assert adapter.variables["tv_ol_mt_nobles"] == (0 if government else 30)
    assert adapter.variables["tv_ol_mt_clergy"] == (0 if government else 50)
    assert sum(adapter.variables[f"tv_ol_mt_{name}"] for name in ("crown", *gen.estates())) == 100
    assert adapter.locals == {"tv_ol_worksite": "building"}
    adapter.run(adapter.definitions["tv_wonder_clear_worksite_maintenance_display_effect"])
    assert adapter.variables == {}


@pytest.mark.parametrize("options", [{"worksite": False}, {"opened": False}, {"level": 0}])
def test_missing_closed_and_zero_level_worksites_do_not_call_pricing(options):
    adapter = Adapter(**options)
    adapter.run(adapter.definitions["tv_wonder_update_worksite_maintenance_display_effect"])
    assert adapter.priced == 0
    assert adapter.variables["tv_ol_mt_total"] == adapter.variables["tv_ol_mt_crown"] == 0


def test_adapter_reuses_pricing_and_estate_list_without_national_settlement_calls():
    source = gen.effects()
    for forbidden in ("epbm_calculate_maintenance", "epbm_split_by_estate_power", "epbm_collect_maintenance",
                      "epbm_charge_estates", "add_gold", "add_gold_to_estate"):
        assert not any(n.key == forbidden for n in walk(parse(source)))
    assert 'epbm_price_building = yes' in source
    assert 'epbm_for_each_estate = {' in source
    lifecycle = base.effects()
    assert lifecycle.index('tv_wonder_update_worksite_maintenance_display_effect = yes') < lifecycle.index('name = tv_ol_ready')
    assert 'tv_wonder_clear_worksite_maintenance_display_effect = yes' in lifecycle


def test_generated_compat_outputs_are_owned_fresh_and_complete_in_all_languages():
    manifest = yaml.safe_load((ROOT / "data/generated_files.yaml").read_text(encoding="utf-8-sig"))
    registered = {item["output"] for item in manifest["generated"] if item["script"] == gen.SCRIPT}
    outputs = gen.outputs()
    assert registered == set(outputs)
    for relative, content in outputs.items():
        raw = (ROOT / relative).read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf")
        assert raw.decode("utf-8-sig") == content
    languages = [content for path, content in outputs.items() if path.endswith('.yml')]
    assert len(languages) == 11
    assert len({frozenset(line.split(':', 1)[0].strip() for line in content.splitlines() if line.startswith(' TV_')) for content in languages}) == 1
