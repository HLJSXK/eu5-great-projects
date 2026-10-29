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
        self.source = (ROOT / generator.EFFECT_PATH).read_text(encoding="utf-8-sig")

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
            elif node.key == "add_gold":
                assert current is self.country, "Gold must go to the calling country"
                current["gold"] += self.value(node.value, current)
            elif node.key == "add_temporary_demand":
                assert current is self.market, "Demand must go to the target market"
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
    assert sale.country["gold"] == pytest.approx(152.5)
    assert sale.market["demands"] == [{"type": f"demand:tv_market_supply_{good}", "scale": 12.5, "months": 6}]
    demand = child(parse((ROOT / generator.DEMAND_PATH).read_text(encoding="utf-8-sig")), f"tv_market_supply_{good}")
    assert [(n.key, n.value) for n in demand.children if n.key not in {"hidden", "category"}] == [(good, "-1")]


def test_price_is_read_on_each_call_and_inputs_are_captured_before_gold_changes():
    sale = Sale()
    sale.call(amount="gold", time="gold")
    assert sale.country["gold"] == pytest.approx(520)
    assert sale.market["demands"][0]["scale"] == 100
    assert sale.market["demands"][0]["months"] == 100
    sale.market["prices"]["medicaments"] = 2
    sale.call(amount="3", time="2")
    assert sale.country["gold"] == pytest.approx(526)
    assert sale.market["demands"][1]["scale"] == 3
    assert sale.market["demands"][1]["months"] == 2


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
