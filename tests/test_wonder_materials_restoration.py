"""Historical parity and integration contract for the restored material chain."""

from scripts_engineering_department.test_wonder_mechanics_rules import (
    validate_worksite_maintenance_input_contract,
)


def test_wonder_materials_match_pre_removal_history_and_remain_integrated():
    validate_worksite_maintenance_input_contract()
