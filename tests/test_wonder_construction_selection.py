"""Exercise automatic part selection against deployed Jomini lifecycle effects.

Only country counters and deterministic branches are evaluated here. IO ticks,
building completion, competence changes and display updates remain engine seams.
"""

from dataclasses import replace
from itertools import product
import operator

import pytest

from test_wonder_priority_proposals import child, source_blocks, walk


EFFECTS = source_blocks("common/scripted_effects/tv_engineering_department_effects.txt")
TRIGGERS = source_blocks("common/scripted_triggers/tv_engineering_department_triggers.txt")
PARTS = ("foundation", "body", "function", "decoration")
COUNTERS = tuple(f"tv_wonder_{part}_units" for part in PARTS)
ACTIVE = "tv_wonder_active_part"
LEVEL = "tv_wonder_level"
SELECT = "tv_wonder_auto_advance_active_part_effect"
MONTHLY = "tv_wonder_monthly_construction_effect"
COMPARE = {"=": operator.eq, "?=": operator.eq, "<": operator.lt,
           "<=": operator.le, ">": operator.gt, ">=": operator.ge}


def bind_parameters(nodes, parameters):
    return tuple(replace(node, value=bind_parameters(node.value, parameters)
                         if isinstance(node.value, tuple) else parameters.get(node.value, node.value))
                 for node in nodes)


class Construction:
    ENGINE_SEAMS = {
        "tv_wonder_update_construction_tiers_from_competence_effect",
        "tv_wonder_set_required_progress_effect",
        "tv_wonder_update_logistics_metrics_effect",
        "tv_wonder_check_construction_unit_completion_effect",
        "tv_wonder_set_io_construction_progress_effect",
        "tv_wonder_update_construction_progress_display_effect",
        "trigger_event_non_silently",
    }

    def __init__(self, units, cap=6, unlocked=True):
        self.state = dict(zip(COUNTERS, units))
        self.state["tv_wonder_scale_tier"] = cap
        self.unlocked = unlocked
        self.calls = []
        self.run("tv_wonder_update_wonder_level_effect")

    def number(self, value):
        if value.startswith("var:"):
            return self.state[value[4:]]  # Missing counters must fail, as in game.
        return int(value)

    def condition(self, nodes):
        def check(node):
            if node.key in {"AND", "limit"}:
                return self.condition(node.children)
            if node.key == "OR":
                return any(check(item) for item in node.children)
            if node.key == "NOT":
                return not self.condition(node.children)
            if node.key == "has_variable":
                return node.value in self.state
            if node.key == "tv_wonder_organization_logistics_unlocked_trigger":
                return self.unlocked == (node.value == "yes")
            if node.key in TRIGGERS:
                return self.condition(TRIGGERS[node.key]) == (node.value == "yes")
            if node.op == "?=" and node.key[4:] not in self.state:
                return False
            if node.children:
                comparison = child(node.children, "this")
                return COMPARE[comparison.op](self.number(node.key), self.number(comparison.value))
            return COMPARE[node.op](self.number(node.key), self.number(node.value))
        return all(check(node) for node in nodes)

    def run(self, effect):
        nodes = EFFECTS[effect] if isinstance(effect, str) else effect
        matched = False
        for node in nodes:
            if node.key in {"if", "else_if", "else"}:
                if node.key == "if":
                    matched = False
                if not matched and (node.key == "else" or self.condition(child(node.children, "limit").children)):
                    matched = True
                    self.run(tuple(item for item in node.children if item.key != "limit"))
            elif node.key == "set_variable":
                self.state[child(node.children, "name").value] = self.number(child(node.children, "value").value)
            elif node.key == "remove_variable":
                self.state.pop(node.value, None)
            elif node.key == "clamp_variable":
                name = child(node.children, "name").value
                self.state[name] = max(self.number(child(node.children, "min").value),
                                       min(self.state[name], self.number(child(node.children, "max").value)))
            elif node.key in self.ENGINE_SEAMS:
                self.calls.append(node.key)
            elif node.key in EFFECTS:
                parameters = {f"${item.key}$": item.value for item in node.children}
                self.run(bind_parameters(EFFECTS[node.key], parameters) if parameters else node.key)
            else:
                raise AssertionError(f"Unsupported construction effect: {node}")

    def complete_part(self):
        part = self.state[ACTIVE]
        self.state[COUNTERS[part - 1]] += 1
        self.state["tv_wonder_last_completed_part"] = part
        self.run("tv_wonder_after_unit_completed_effect")
        self.run("tv_wonder_after_unit_completed_event_effect")


@pytest.mark.parametrize("base", range(6))
@pytest.mark.parametrize("remaining", [bits for bits in product((0, 1), repeat=4) if 0 < sum(bits) < 4])
def test_resuming_one_to_three_remaining_modules_fills_the_missing_part(base, remaining):
    units = tuple(base + extra for extra in remaining)
    for cap in range(base + 1, 7):
        project = Construction(units, cap)
        project.run(MONTHLY)
        assert project.state[ACTIVE] == remaining.index(0) + 1
        assert tuple(project.state[name] for name in COUNTERS) == units
        assert project.state[LEVEL] == base


@pytest.mark.parametrize("cap", range(1, 7))
def test_all_counter_combinations_choose_the_lowest_unfinished_level(cap):
    for units in product(range(7), repeat=4):
        project = Construction(units, cap)
        project.run(SELECT)
        expected = units.index(min(units)) + 1 if min(units) < cap else None
        assert project.state.get(ACTIVE) == expected, (units, cap)


@pytest.mark.parametrize("budget", [1, 2, 3])
def test_repeated_short_projects_reach_level_six(budget):
    units = (0, 0, 0, 0)
    completed = []
    for _ in range(24 // budget):
        # New country runtime, with only completed buildings carried over.
        project = Construction(units)
        assert "tv_wonder_last_completed_part" not in project.state
        project.run(MONTHLY)
        for _ in range(budget):
            completed.append(project.state[ACTIVE])
            project.complete_part()
        units = tuple(project.state[name] for name in COUNTERS)
    assert units == (6, 6, 6, 6)
    assert project.state[LEVEL] == 6
    assert ACTIVE not in project.state
    assert completed == [1, 2, 3, 4] * 6


def test_unbalanced_modules_are_filled_before_any_further_upgrade():
    project = Construction((4, 3, 2, 0))
    project.run(MONTHLY)
    for expected in (4, 4, 3, 4, 2, 3, 4):
        assert project.state[ACTIVE] == expected
        project.complete_part()
    assert tuple(project.state[name] for name in COUNTERS) == (4, 4, 4, 4)
    assert project.state[ACTIVE] == 1


@pytest.mark.parametrize("active", range(1, 5))
def test_monthly_construction_preserves_the_players_active_part(active):
    project = Construction((2, 2, 2, 0))
    project.state[ACTIVE] = active
    project.run(MONTHLY)
    assert project.state[ACTIVE] == active
    assert "tv_wonder_check_construction_unit_completion_effect" in project.calls


def test_locked_construction_does_not_select_a_part():
    project = Construction((1, 1, 1, 0), unlocked=False)
    project.run(MONTHLY)
    assert ACTIVE not in project.state


def test_selection_preview_is_safe_before_project_counters_are_initialized():
    project = Construction((0, 0, 0, 0))
    project.state.clear()
    project.run(SELECT)
    assert ACTIVE not in project.state
    project.run(bind_parameters(EFFECTS["tv_wonder_select_lowest_incomplete_part_effect"], {"$completed_level$": "0"}))
    assert ACTIVE not in project.state


def test_restoration_and_completion_refresh_level_before_automatic_selection():
    entry = child(EFFECTS["tv_wonder_select_construction_site_effect"], "if").children
    keys = [node.key for node in walk(entry)]
    assert keys.index("tv_wonder_sync_units_from_buildings_effect") < keys.index("tv_wonder_update_wonder_level_effect") < keys.index(MONTHLY)
    assert child(EFFECTS["tv_wonder_after_unit_completed_effect"], "tv_wonder_update_wonder_level_effect")
    assert child(EFFECTS["tv_wonder_after_unit_completed_event_effect"], SELECT)
