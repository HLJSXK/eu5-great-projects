"""Ownership choices against generated scripts; engine building queues remain external."""

import pytest

from test_wonder_priority_proposals import child, contains, load_generator, parse, source_blocks, walk
from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.naming import all_final_buildings, ownership_gain_event_id, ownership_loss_event_id


WONDERS, _ = load_all_wonder_mechanics()
EVENTS = source_blocks("events/tv_wonder_ownership_events.txt")
EFFECTS = source_blocks("common/scripted_effects/tv_wonder_ownership_effects.txt")


def test_generated_ownership_outputs_are_current():
    for name, path, deployed in (
        ("ownership_events", "in_game/events/gen_tv_wonder_ownership_events.py", EVENTS),
        ("ownership_effects", "in_game/common/scripted_effects/gen_tv_wonder_ownership_effects.py", EFFECTS),
    ):
        generated = load_generator(name, path).generate()
        assert {node.key: node.children for node in parse(generated)} == deployed


def test_transfer_rejects_unfinished_buildings_and_stale_cached_levels():
    hook = source_blocks("common/on_action/tv_wonder_ownership_on_action.txt")["tv_wonder_ownership_location_changed_owner"]
    buildings = child(child(hook, "trigger").children, "any_buildings_in_location").children
    assert child(buildings, "building_level").op == ">="
    assert child(buildings, "building_level").value == "1"
    registry = child(buildings, "is_key_in_global_variable_map").children
    assert child(registry, "name").value == "tv_wonder_final_building_type_to_wonder_id"
    assert child(registry, "target").value == "building_type"
    handler = EFFECTS["tv_wonder_ownership_handle_location_owner_changed_effect"]
    scan = next(n for n in walk(handler) if n.key == "every_key_in_global_variable_map")
    assert contains(child(scan.children, "limit").children, "location_building_level")
    assert contains(scan.children, "save_scope_as", "tv_wonder_ownership_building_type")
    assert contains(handler, "tv_wonder_ownership_cleanup_loss_effect", "yes")
    assert contains(handler, "save_scope_value_as")


@pytest.mark.parametrize("wonder", WONDERS, ids=lambda w: w["key"])
def test_each_wonder_has_its_own_rewards_level_interface_and_result_notices(wonder):
    event = EVENTS[f"tv_engineering_department.{ownership_gain_event_id(wonder)}"]
    preserve, plunder = [n.children for n in event if n.key == "option"]
    assert [child(child(o, "ai_chance").children, "factor").value for o in (preserve, plunder)] == ["80", "20"]
    assert contains(preserve, "add_prestige", "5")
    assert not contains(preserve, "add_gold")
    assert contains(plunder, "add_gold", str({"small": 2000, "medium": 4000, "large": 6000}[wonder["size"]]))
    effect = "tv_wonder_lower_unique_level_effect" if wonder.get("is_unique") else "tv_wonder_lower_generic_level_effect"
    lowering = [n for n in walk(plunder) if n.key == effect]
    assert len(lowering) == 1
    assert child(lowering[0].children, "wonder").value == wonder["key"]
    assert not contains(event, "change_building_level_in_location")
    expected_buildings = {f"building_type:{b}" for b in all_final_buildings([wonder])}
    for option, result in ((preserve, "0"), (plunder, "1")):
        success = child(option, "if").children
        guard = child(success, "limit").children
        assert contains(guard, "owner", "root")
        assert contains(guard, "var:tv_wonder_ownership_revision", "scope:tv_wonder_ownership_revision")
        assert {child(n.children, "building_type").value for n in walk(guard) if n.key == "location_building_level"} == expected_buildings
        notification = child(success, "hidden_effect").children
        assert child(child(notification, "save_scope_value_as").children, "value").value == result
        target = child(notification, "scope:loser")
        assert target.op == "?="
        assert contains(target.children, "id", f"tv_engineering_department.{ownership_loss_event_id(wonder)}")
    notice = EVENTS[f"tv_engineering_department.{ownership_loss_event_id(wonder)}"]
    # Result notices must never withdraw benefits again: the old owner may have retaken the site.
    assert not contains(notice, "remove_country_modifier")
    assert not contains(notice, "remove_from_variable_map")
    assert contains(notice, "desc", "tv_wonder_ownership.900.d_preserved")
    assert contains(notice, "desc", "tv_wonder_ownership.900.d_plundered")


def choice_branch(wonder, *, choice, owner="new", level=1, revision=1, former_owner=True):
    """Evaluate only ownership guards and option effects, without simulating engine queues."""
    event = EVENTS[f"tv_engineering_department.{ownership_gain_event_id(wonder)}"]
    option = [n.children for n in event if n.key == "option"][choice]
    levels = {f"building_type:{all_final_buildings([wonder])[-1]}": level}
    calls = []

    def condition(nodes):
        for n in nodes:
            if n.key == "scope:tv_wonder_ownership_site":
                passed = condition(n.children)
            elif n.key == "owner":
                passed = owner == "new"
            elif n.key == "var:tv_wonder_ownership_revision":
                passed = revision == 1
            elif n.key == "OR":
                passed = any(condition((c,)) for c in n.children)
            elif n.key == "location_building_level":
                fields = n.children
                passed = levels.get(child(fields, "building_type").value, 0) >= int(child(fields, "value").value)
            else:
                raise AssertionError(f"Unhandled ownership condition: {n}")
            if not passed:
                return False
        return True

    def run(nodes):
        matched = False
        for n in nodes:
            if n.key == "if":
                matched = condition(child(n.children, "limit").children)
                if matched:
                    run(tuple(c for c in n.children if c.key != "limit"))
            elif n.key == "else":
                if not matched:
                    run(n.children)
            elif n.key in {"hidden_effect", "scope:tv_wonder_ownership_site"}:
                run(n.children)
            elif n.key == "scope:loser":
                if former_owner:
                    run(n.children)
            elif n.key == "save_scope_value_as":
                calls.append(("result", child(n.children, "value").value))
            elif n.key in {"add_gold", "add_prestige", "trigger_event_non_silently"} or n.key.startswith("tv_wonder_lower_"):
                calls.append((n.key, n.value))
            elif n.key not in {"name", "ai_chance"}:
                raise AssertionError(f"Unhandled ownership effect: {n}")

    run(option)
    return calls


@pytest.mark.parametrize("choice", (0, 1))
@pytest.mark.parametrize("level,owner,revision,valid", (
    (1, "new", 1, True), (6, "new", 1, True),
    (0, "new", 1, False), (3, "other", 1, False),
    (3, "new", 3, False),  # Lost and retaken: an older event cannot pay out again.
))
def test_open_event_revalidates_before_rewards_and_always_notifies(choice, level, owner, revision, valid):
    calls = choice_branch(WONDERS[0], choice=choice, level=level, owner=owner, revision=revision)
    rewards = [key for key, _ in calls if key in {"add_gold", "add_prestige"}]
    lowerings = [key for key, _ in calls if key.startswith("tv_wonder_lower_")]
    assert len(rewards) == int(valid)
    assert len(lowerings) == int(valid and choice == 1)
    assert ("result", str(choice) if valid else "2") in calls
    assert len([key for key, _ in calls if key == "trigger_event_non_silently"]) == 1


def test_an_ownerless_origin_does_not_require_a_notification_target():
    calls = choice_branch(WONDERS[0], choice=1, former_owner=False)
    assert any(key == "add_gold" for key, _ in calls)
    assert not any(key == "trigger_event_non_silently" for key, _ in calls)
