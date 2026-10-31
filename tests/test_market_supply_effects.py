"""Economic/scope contracts evaluated from generated Jomini.

This evaluator covers the effect's arithmetic and dispatch, not engine market
simulation, demand stacking, expiry, or tooltip rendering.
"""
from pathlib import Path
import re
import sys

import pytest
import yaml

from test_wonder_priority_proposals import child, parse


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts_engineering_department"))
import gen_market_supply_effects as generator


class Sale:
    def __init__(self):
        self.country = {"gold": 100, "shipment_size": 12.5, "shipment_months": 6}
        self.market = {"prices": {g: 4.2 for g in generator.goods_ids()}, "demands": []}
        self.scopes = {"target_market": self.market, "target_goods": "goods:medicaments"}
        self.descriptions = []
        self.source = (ROOT / generator.EFFECT_PATH).read_text(encoding="utf-8-sig")
        self.script_values = {node.key: node.value for node in parse(
            (ROOT / generator.VALUES_PATH).read_text(encoding="utf-8-sig"))}

    def value(self, token, current):
        if isinstance(token, tuple):
            total = 0
            for node in token:
                if node.key == "value":
                    total = self.value(node.value, current)
                elif node.key == "multiply":
                    total *= self.value(node.value, current)
                else:
                    raise AssertionError(f"Unsupported arithmetic: {node}")
            return total
        if token.startswith('"'):
            match = re.fullmatch(r'"(scope:\w+)\.price_in_market\((scope:\w+)\)"', token)
            assert match, token
            good = self.value(match[1], current).removeprefix("goods:")
            return self.value(match[2], current)["prices"][good]
        if token.startswith("scope:"):
            return self.scopes.get(token.removeprefix("scope:"))
        if token.startswith("goods:"):
            return token
        if token == "capital.market":
            # Deliberately unusable: this test's caller has no capital.
            raise AssertionError("The effect must use the supplied target market")
        if token in current:
            return current[token]
        if token in self.script_values:
            return self.value(self.script_values[token], current)
        return float(token)

    def condition(self, nodes, current):
        for node in nodes:
            if node.key == "exists":
                passed = self.value(node.value, current) is not None
            elif node.op == ">":
                passed = self.value(node.key, current) > self.value(node.value, current)
            else:
                assert node.op == "=", node
                passed = self.value(node.key, current) == self.value(node.value, current)
            if not passed:
                return False
        return True

    def run(self, nodes, current):
        taken = False
        for node in nodes:
            if node.key in {"if", "else_if"}:
                if node.key == "if":
                    taken = False
                if not taken and self.condition(child(node.children, "limit").children, current):
                    taken = True
                    self.run(tuple(n for n in node.children if n.key != "limit"), current)
            elif node.key == "save_scope_value_as":
                self.scopes[child(node.children, "name").value] = self.value(child(node.children, "value").value, current)
            elif node.key == "save_scope_as":
                self.scopes[node.value] = current
            elif node.key == "custom_description":
                # This slot parses a value target, unlike add_gold's arithmetic.
                assert isinstance(child(node.children, "value").value, str)
                self.descriptions.append(self.value(child(node.children, "value").value, current))
                metadata = {"text", "subject", "object", "value"}
                self.run(tuple(n for n in node.children if n.key not in metadata), current)
            elif node.key == "add_gold":
                assert current is self.country, "Gold must go to the calling country"
                current["gold"] += self.value(node.value, current)
            elif node.key == "add_temporary_demand":
                assert current is self.market, "Demand must go to the target market"
                assert isinstance(child(node.children, "months").value, str)
                current["demands"].append({n.key: (n.value if n.key == "type" else self.value(n.value, current)) for n in node.children})
            elif node.key == "tv_sell_goods_with_temporary_supply_apply_effect":
                demand = child(node.children, "demand").value
                helper = child(parse(self.source.replace("$demand$", demand)), node.key)
                self.run(helper.children, current)
            elif node.key.startswith(("scope:", "goods:")):
                self.run(node.children, self.value(node.key, current))
            else:
                raise AssertionError(f"Unexpected effect (including inventory mutation): {node}")

    def call(self, amount="shipment_size", time="shipment_months"):
        source = self.source
        for key, value in {"market": "scope:target_market", "goods": "scope:target_goods", "amount": amount, "time": time}.items():
            source = source.replace(f"${key}$", value)
        self.run(child(parse(source), "tv_sell_goods_with_temporary_supply_effect").children, self.country)


@pytest.mark.parametrize("good", generator.goods_ids())
def test_each_good_pays_once_and_offsets_only_its_own_demand(good):
    sale = Sale()
    sale.scopes["target_goods"] = f"goods:{good}"
    sale.call()
    assert sale.country["gold"] == pytest.approx(415)
    assert sale.descriptions == [pytest.approx(315)]
    assert sale.market["demands"] == [{"type": f"demand:tv_market_supply_{good}", "scale": 12.5, "months": 6}]
    demand = child(parse((ROOT / generator.DEMAND_PATH).read_text(encoding="utf-8-sig")), f"tv_market_supply_{good}")
    assert [(n.key, n.value) for n in demand.children if n.key not in {"hidden", "category"}] == [(good, "-1")]


def test_price_is_read_on_each_call_and_inputs_are_captured_before_gold_changes():
    sale = Sale()
    sale.call(amount="gold", time="gold")
    assert sale.country["gold"] == pytest.approx(42100)
    assert sale.market["demands"][0]["scale"] == 100
    assert sale.market["demands"][0]["months"] == 100
    sale.market["prices"]["medicaments"] = 2
    sale.call(amount="3", time="2")
    assert sale.country["gold"] == pytest.approx(42112)
    assert sale.descriptions == [pytest.approx(42000), pytest.approx(12)]
    assert sale.market["demands"][1]["scale"] == 3
    assert sale.market["demands"][1]["months"] == 2


@pytest.mark.parametrize("months,payout", [(10, 1000), (20, 2000), (30, 3000)])
def test_plunder_pays_full_term_upfront_without_scaling_monthly_supply(months, payout):
    sale = Sale()
    sale.scopes["target_goods"] = "goods:tv_wonder_materials"
    sale.market["prices"]["tv_wonder_materials"] = 5
    sale.call(amount="20", time=str(months))
    assert sale.country["gold"] == 100 + payout
    assert sale.descriptions == [payout]
    assert sale.market["demands"] == [{
        "type": "demand:tv_market_supply_tv_wonder_materials", "scale": 20, "months": months,
    }]


@pytest.mark.parametrize("amount,time", [("0", "6"), ("-1", "6"), ("15", "0"), ("15", "-1")])
def test_nonpositive_inputs_do_not_pay_or_add_demand(amount, time):
    sale = Sale()
    sale.call(amount, time)
    assert sale.country["gold"] == 100
    assert sale.market["demands"] == []


@pytest.mark.parametrize("key,value", [("target_market", None), ("target_goods", None), ("target_goods", "goods:unregistered_test_good")])
def test_missing_target_or_unsupported_good_does_not_pay(key, value):
    sale = Sale()
    sale.scopes[key] = value
    sale.call()
    assert sale.country["gold"] == 100
    assert sale.market["demands"] == []


def test_generated_files_owned_fresh_encoded_and_localized():
    manifest = yaml.safe_load((ROOT / "data/generated_files.yaml").read_text(encoding="utf-8-sig"))["generated"]
    for relative, expected in generator.outputs().items():
        assert (ROOT / relative).read_bytes() == b"\xef\xbb\xbf" + expected.encode("utf-8")
        assert [item["script"] for item in manifest if item["output"] == relative] == [generator.GENERATOR]
        if relative.endswith(".yml"):
            keys = re.findall(r"(?m)^ (tv_market_supply_\w+):", expected)
            assert sorted(keys) == [f"tv_market_supply_{good}" for good in generator.goods_ids()]
    assert "tv_wonder_materials" in generator.goods_ids()


@pytest.mark.parametrize("language", ["english", "simp_chinese"])
def test_sale_wording_matches_vanilla_in_all_perspectives(language):
    native_path = ROOT / f".eu5-base/reference_game_files/game/main_menu/localization/{language}/effects_l_{language}.yml"
    native = dict(re.findall(r'^\s*(\w+):(?:\d+)?\s*"(.*)"\s*$', native_path.read_text(encoding="utf-8-sig"), re.MULTILINE))
    deployed_path = ROOT / f"src/main_menu/localization/{language}/tv_market_supply_l_{language}.yml"
    deployed = dict(re.findall(r'^\s*(\w+):0\s*"(.*)"\s*$', deployed_path.read_text(encoding="utf-8-sig"), re.MULTILINE))
    # Normalize bindings back to native placeholders, then compare the entire
    # sentence including tense, perspective, icons, spacing and amount format.
    bindings = {
        "$VALUE|2$": "$GOLD$",
        "[Multiply_CFixedPoint(SCOPE.GetValue('tv_market_supply_amount'), SCOPE.GetValue('tv_market_supply_months'))|+=2]": "$AMOUNT|+=2$",
        "[SCOPE.sGoods('tv_market_supply_goods').GetName]": "$GOODS$",
        "[SCOPE.sCountry('tv_market_supply_country').GetName]": "[COUNTRY.GetName]",
        "[SCOPE.sMarket('tv_market_supply_market').GetName]": "[TARGET_MARKET.GetName]",
        "[SCOPE.sMarket('tv_market_supply_market').GetShortName]": "[TARGET_MARKET.GetShortName]",
    }
    registry = child(parse((ROOT / generator.EFFECT_LOC_PATH).read_text(encoding="utf-8-sig")), generator.DESCRIPTION)
    for perspective, native_key in generator.SALE_LOCALIZATIONS.items():
        text = deployed[child(registry.children, perspective).value]
        assert "$VALUE|2$" in text
        for binding, placeholder in bindings.items():
            text = text.replace(binding, placeholder)
        assert text == native[native_key]


def test_one_custom_description_wraps_the_actual_effects():
    source = parse((ROOT / generator.EFFECT_PATH).read_text(encoding="utf-8-sig"))
    helper = child(source, "tv_sell_goods_with_temporary_supply_apply_effect")
    assert [node.key for node in helper.children] == ["save_scope_as", "custom_description"]
    description = child(helper.children, "custom_description")
    assert child(description.children, "text").value == generator.DESCRIPTION
    assert child(description.children, "subject").value == "this"
    assert child(description.children, "object").value == "scope:tv_market_supply_market"
    # No native-sale preview that could use a different price or add stockpile goods.
    assert child(description.children, "value").value == generator.PAYOUT_VALUE
    assert child(child(description.children, "add_gold").children, "value").value == generator.PAYOUT_VALUE
    assert "sell_goods_to_market" not in {node.key for node in description.children}
