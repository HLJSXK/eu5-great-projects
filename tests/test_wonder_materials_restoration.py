"""Historical integration and regional economics of the material chain."""

from decimal import Decimal

import pytest

from scripts_engineering_department.test_wonder_mechanics_rules import (
    load_material_workshop_economy,
    validate_worksite_maintenance_input_contract,
)


def test_wonder_materials_match_pre_removal_history_and_remain_integrated():
    validate_worksite_maintenance_input_contract()


@pytest.mark.parametrize(("multipliers", "expected_suffix"), [
    ({"clay": "0.5", "sand": "0.5", "fiber_crops": "0.5"}, "_rammed_earth"),
    ({"lumber": "0.5", "clay": "0.5", "fiber_crops": "0.5"}, "_timber_frame"),
    ({"clay": "0.5", "sand": "0.5", "lumber": "0.5"}, "_wood_kiln"),
    ({"clay": "0.5", "sand": "0.5", "coal": "0.5"}, "_coal_kiln"),
    ({"stone": "0.5"}, "_no_marble"),
    ({"marble": "0.5"}, ""),
    ({"masonry": "0.5", "paper": "0.5", "iron": "0.5", "steel": "2"}, "_patterned_components"),
    ({}, "_steel_cutting"),
    ({"tools": "4"}, "_coal_kiln"),
])
def test_regional_prices_change_the_most_profitable_method(multipliers, expected_suffix):
    prices, _, recipes = load_material_workshop_economy()
    for good, factor in multipliers.items():
        prices[good] *= Decimal(factor)
    costs = {
        method: sum(prices[good] * Decimal(amount) for good, amount in fields.items()
                    if good not in {"produced", "output", "category"})
        for method, fields in recipes.items()
    }
    assert min(costs, key=costs.get) == "tv_wonder_material_dispatch_point_production" + expected_suffix
