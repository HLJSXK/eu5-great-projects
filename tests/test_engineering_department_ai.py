"""Policy scenarios evaluated against deployed Jomini, plus lifecycle regressions.

The tiny evaluator covers only deterministic country policy syntax. It does not
simulate the game engine, construction pricing, employment, or IO monthly ticks.
"""
from itertools import product
import math
from pathlib import Path
import re

import pytest
import yaml

from test_wonder_priority_proposals import child, contains, parse, source_blocks, walk


ROOT = Path(__file__).resolve().parents[1]
AI = source_blocks("common/scripted_effects/tv_engineering_department_ai_effects.txt")
TRIGGERS = source_blocks("common/scripted_triggers/tv_engineering_department_ai_triggers.txt")


class Policy:
    def __init__(self, **state):
        self.state = {"tv_wonder_current_site_is_shell_trigger": False, **state}
        self.locals = {}
        self.calls = []

    def number(self, value):
        if isinstance(value, tuple):
            total = 0
            for node in value:
                if node.key == "value": total = self.number(node.value)
                elif node.key == "add": total += self.number(node.value)
                elif node.key == "divide": total /= self.number(node.value)
                elif node.key == "max": total = min(total, self.number(node.value))
                elif node.key == "floor": total = math.floor(total)
                else: raise AssertionError(f"Unsupported numeric clause: {node}")
            return total
        if value.startswith("local_var:"): return self.locals[value[10:]]
        if value.startswith("var:"): return self.state.get(value[4:], 0)
        if value.startswith('"global_variable_map('):
            key = value.split("|var:")[1].split(")")[0]
            return self.state["sizes"][self.state[key]]
        if value in self.state: return self.state[value]
        return float(value)

    def condition(self, nodes):
        def check(n):
            if n.key in {"AND", "limit"}: return self.condition(n.children)
            if n.key == "OR": return any(check(c) for c in n.children)
            if n.key == "NOT": return not self.condition(n.children)
            if n.key == "has_variable": return n.value in self.state
            if n.key == "has_global_variable": return n.value in self.state.get("globals", set())
            if n.key == "has_global_variable_map": return bool(self.state.get("sizes"))
            if n.key == "is_key_in_global_variable_map":
                return self.number(child(n.children, "target").value) in self.state["sizes"]
            if n.key == "can_pay_price": return self.state[n.key]
            if n.key in self.state and isinstance(self.state[n.key], bool):
                return self.state[n.key] == (n.value == "yes")
            if n.key in TRIGGERS: return self.condition(TRIGGERS[n.key]) == (n.value == "yes")
            if n.op == "?=" and n.key.startswith("var:") and n.key[4:] not in self.state: return False
            left = self.number(n.key)
            if n.children and n.op == "?=":
                test = child(n.children, "this")
                right, op = self.number(test.value), test.op
            else:
                right, op = self.number(n.value), n.op
            return {"=": left == right, "?=": left == right, ">=": left >= right,
                    "<=": left <= right, ">": left > right, "<": left < right}[op]
        return all(check(n) for n in nodes)

    def run(self, nodes):
        matched = False
        for n in nodes:
            if n.key in {"if", "else_if", "else"}:
                if n.key == "if": matched = False
                take = not matched and (n.key == "else" or self.condition(child(n.children, "limit").children))
                if take:
                    matched = True
                    self.run(tuple(c for c in n.children if c.key != "limit"))
            elif n.key == "set_local_variable":
                self.locals[child(n.children, "name").value] = self.number(child(n.children, "value").value)
            elif n.key == "remove_local_variable": self.locals.pop(n.value)
            elif n.key == "change_local_variable":
                name = child(n.children, "name").value
                for c in n.children:
                    if c.key == "add": self.locals[name] += self.number(c.value)
                    if c.key == "subtract": self.locals[name] -= self.number(c.value)
            elif n.key == "while":
                iterations = 0
                while self.condition(child(n.children, "limit").children):
                    self.run(tuple(c for c in n.children if c.key != "limit"))
                    iterations += 1
                    assert iterations <= 15, "Camp loop must terminate without engine completion callbacks"
            elif n.key == "cmf_log_with_args": pass
            elif n.key == "pay_price": self.calls.append((n.key, n.value))
            elif n.key.startswith("tv_"): self.calls.append(n.key)
            else: raise AssertionError(f"Unsupported policy effect: {n}")


@pytest.mark.parametrize("balance", [299, 300, 599, 600, 899, 900, 1200])
def test_proposal_order_for_every_slot_combination(balance):
    for sizes in product(range(4), repeat=3):
        state = dict(monthly_balance=balance, gold=1000, prestige=20, sizes={i:i for i in (1,2,3)})
        state.update({f"tv_wonder_proposal_slot_{i}": size for i,size in enumerate(sizes,1) if size})
        policy = Policy(**state)
        policy.run(AI["tv_wonder_ai_select_proposal_effect"])
        preferred = 3 if balance >= 900 else 2 if balance >= 600 else 1
        expected = []
        if balance >= 300:
            for size in range(preferred,0,-1):
                if size in sizes:
                    expected = [f"tv_wonder_select_proposal_slot_{sizes.index(size)+1}_effect"]
                    break
            else: expected = ["tv_wonder_bribe_proposal_effect"]
        assert policy.calls == expected, (balance, sizes)
        assert not policy.locals, "Proposal evaluation must clean all scratch values"


@pytest.mark.parametrize("gold,prestige,expected", [(999,10,"refute"),(999,9,None),(1000,0,"bribe")])
def test_unmatched_proposal_rejection_budget(gold, prestige, expected):
    p = Policy(monthly_balance=300, gold=gold, prestige=prestige, sizes={1:2}, tv_wonder_proposal_slot_1=1)
    p.run(AI["tv_wonder_ai_select_proposal_effect"])
    assert p.calls == ([f"tv_wonder_{expected}_proposal_effect"] if expected else [])


@pytest.mark.parametrize("estate", ["nobles","burghers","clergy"])
def test_demand_whitelist_requires_real_availability(estate):
    key = f"tv_wonder_ai_can_accept_{estate}_demand_trigger"
    for demand in range(1,13):
        for available in (False,True):
            p = Policy(**{f"tv_wonder_{estate}_demand":demand,
                          f"tv_wonder_{estate}_current_demand_available_trigger":available})
            assert p.condition(TRIGGERS[key]) == (available and demand in {5,6,7,8,10,11,12})


def test_selected_proposal_waits_below_surplus_threshold_then_accepts_only_once():
    # Covers new, resumed, and expanded proposals: there is one shared gate.
    for mode in (None,1,2):
        state = dict(tv_wonder_stage=0, tv_wonder_proposal=101, tv_wonder_has_open_proposal_trigger=True,
                     tv_wonder_has_great_engineer_trigger=True, tv_wonder_in_debate_trigger=False,
                     tv_wonder_ritual_can_preview_trigger=False,
                     tv_wonder_ceremony_ready_for_free_confirmation_trigger=False,
                     tv_wonder_ceremony_ready_for_scaled_gold_confirmation_trigger=False,
                     tv_wonder_ceremony_ready_for_prestige_confirmation_trigger=False,
                     tv_wonder_hagia_active_trigger=False)
        if mode: state["tv_wonder_proposal_mode"] = mode
        for balance in (299,300):
            p = Policy(**state,monthly_balance=balance)
            p.run(AI["tv_engineering_department_ai_monthly_effect"])
            assert p.calls == (["tv_wonder_accept_proposal_effect"] if balance >= 300 else [])


def test_reappointment_preempts_every_other_monthly_operation():
    p = Policy(tv_wonder_stage=3, tv_wonder_has_great_engineer_trigger=False)
    p.run(AI["tv_engineering_department_ai_monthly_effect"])
    assert p.calls == ["tv_wonder_ai_appoint_engineer_effect"]


@pytest.mark.parametrize("base,level,expected", [(0,1,False),(0,2,True),(2,3,False),(2,4,True),(4,6,True)])
def test_early_finish_is_relative_to_project_base(base,level,expected):
    driver=AI["tv_engineering_department_ai_monthly_effect"]
    branch=next(n.children for n in driver if n.key=="else_if" and any(c.key=="tv_wonder_finish_construction_effect" for c in n.children))
    p=Policy(tv_wonder_stage=3,tv_wonder_project_base_level=base,tv_wonder_level=level,tv_wonder_construction_site_selected_trigger=True)
    assert p.condition(child(branch,"limit").children)==expected


@pytest.mark.parametrize("gold,existing,queued,target,expected", [
    (1000,0,0,5,1),(4999,0,0,5,4),(15000,2,2,5,1),(50000,0,0,15,15),
    (50000,3,2,5,0),(50000,7,1,4,0),(999,0,0,5,0),
])
def test_camp_loop_respects_snapshot_budget_and_queued_levels(gold,existing,queued,target,expected):
    body=AI["tv_wonder_ai_build_labor_camps_effect"]
    loop=child(body,"while")
    p=Policy(tv_wonder_ai_labor_camp_target=target,can_pay_price=True)
    p.locals.update(tv_wonder_ai_camp_budget=min(gold//1000,15),tv_wonder_ai_camp_count=existing+queued)
    # Construction is deliberately asynchronous; only country scratch counters
    # advance during the loop. No engine level update is simulated.
    loop_body=tuple(n for n in loop.children if n.key!="limit")
    iterations=0
    while p.condition(child(loop.children,"limit").children):
        p.run(tuple(n for n in loop_body if n.key!="var:tv_wonder_site"))
        iterations+=1
        assert iterations<=15
    assert iterations==expected
    construction=child(child(loop.children,"var:tv_wonder_site").children,"construct_building").children
    assert child(construction,"instant").value=="no"
    assert not contains(construction,"cost_multiplier")
    assert not contains(construction,"demand_multiplier")


def test_unified_ritual_confirmation_uses_the_shared_paid_effect():
    driver=AI["tv_engineering_department_ai_monthly_effect"]
    assert contains(driver, "tv_wonder_ai_ritual_effect", "yes")
    effects=source_blocks("common/scripted_effects/tv_wonder_ritual_phase_effects.txt")
    assert contains(effects["tv_wonder_ritual_confirm_effect"], "tv_wonder_ritual_pay_effect", "yes")
    assert len([n for n in walk(effects["tv_wonder_ritual_pay_effect"]) if n.key == "pay_price"]) == 3


def test_toggle_and_player_gates_apply_to_both_callbacks_without_stopping_passive_flow():
    pulses=source_blocks("common/on_action/tv_engineering_department_ai_on_action.txt")
    for name,body in pulses.items():
        assert contains(child(body,"trigger").children,"tv_engineering_department_ai_active_trigger","yes")
    for ai,enabled,member in product((False,True),repeat=3):
        p=Policy(is_ai=ai,globals={"tv_engineering_department_ai_enabled"} if enabled else set(),
                 **({"tv_engineering_department_member":1} if member else {}))
        assert p.condition(TRIGGERS["tv_engineering_department_ai_active_trigger"])==(ai and enabled and member)
    passive=(ROOT/"src/in_game/common/on_action/tv_engineering_department_on_action.txt").read_text(encoding="utf-8-sig")
    assert "tv_engineering_department_ai_enabled" not in passive


def test_loss_lifecycle_keeps_foreign_candidates_and_applies_failure_before_notification():
    callbacks=source_blocks("common/on_action/tv_wonder_ownership_on_action.txt")
    loss=callbacks["tv_wonder_construction_site_lost_on_owner_changed"]
    effect=child(child(loss,"effect").children,"scope:loser").children
    assert [n.key for n in effect]==["tv_wonder_forced_abort_effect","trigger_event_non_silently"]
    events=source_blocks("events/tv_engineering_department_events.txt")
    assert [n.key for n in child(events["tv_engineering_department.22"],"option").children]==["name"]
    effects=source_blocks("common/scripted_effects/tv_engineering_department_effects.txt")
    assert contains(effects["tv_wonder_destroy_labor_camp_effect"],"has_variable","tv_wonder_site")
    assert not contains(effects["tv_wonder_destroy_labor_camp_effect"],"tv_wonder_construction_site_selected_trigger")
    cleanup=effects["tv_wonder_clear_project_state_core_effect"]
    assert next(i for i,n in enumerate(cleanup) if n.key=="var:tv_wonder_site") < next(i for i,n in enumerate(cleanup) if n.key=="remove_variable" and n.value=="tv_wonder_site")
    refresh=source_blocks("common/scripted_effects/tv_wonder_module_effects.txt")["tv_wonder_select_saved_priority_proposal_effect"]
    guarded_removal=next(n.children for n in walk(refresh) if n.key=="else_if" and any(c.key=="tv_wonder_remove_current_priority_candidate_effect" for c in n.children))
    assert contains(child(guarded_removal,"limit").children,"owner","scope:tv_wonder_priority_owner")
    registry=yaml.safe_load((ROOT/"data/pulse_registry.yaml").read_text(encoding="utf-8"))
    hooks=registry["bridges"]["on_location_changed_owner"]
    assert hooks.index("tv_wonder_ownership_location_changed_owner") < hooks.index("tv_wonder_construction_site_lost_on_owner_changed")
    ownership=source_blocks("common/scripted_effects/tv_wonder_ownership_effects.txt")["tv_wonder_ownership_handle_location_owner_changed_effect"]
    loser=next(n.children for n in walk(ownership) if n.key=="scope:loser" and contains(n.children,"tv_wonder_ownership_trigger_loss_event_effect"))
    assert not contains(loser,"tv_wonder_unregister_current_site_priority_candidate_effect")
    winner=next(n.children for n in walk(ownership) if n.key=="scope:winner")
    assert contains(winner,"tv_wonder_find_current_site_priority_candidate_effect","yes")
    assert contains(child(child(winner,"if").children,"limit").children,"has_variable","tv_wonder_priority_existing_site_candidate")


def test_every_two_option_event_has_the_intended_ai_policy():
    events=source_blocks("events/tv_engineering_department_events.txt")
    for event in (320,321,322):
        options=[n.children for n in events[f"tv_engineering_department.{event}"] if n.key=="option"]
        assert [child(child(o,"ai_chance").children,"factor").value for o in options]==["0","100"]
    construction=source_blocks("events/tv_wonder_construction_events.txt")
    from scripts_engineering_department.wonder_construction_event_lib import build_events,load_data
    covered=0
    for event in build_events(load_data()):
        if event["kind"] not in {"trade_noneng_for_eng","choose_eng_or_noneng_loss"}: continue
        options=[n.children for n in construction[f"tv_engineering_department.{event['id']}"] if n.key=="option"]
        expected=["0","100"] if event["kind"]=="trade_noneng_for_eng" else ["100","0"]
        assert [child(child(o,"ai_chance").children,"factor").value for o in options]==expected
        covered+=1
    assert covered==130


def test_ai_never_fabricates_an_actor_or_invokes_selector_eligibility():
    for file in ("common/scripted_effects/tv_engineering_department_ai_effects.txt",
                 "common/scripted_triggers/tv_engineering_department_ai_triggers.txt"):
        text=(ROOT/"src/in_game"/file).read_text(encoding="utf-8-sig")
        assert "scope:actor" not in text
        assert "can_build_building" not in text
    dispatch=source_blocks("common/scripted_triggers/tv_engineering_department_wonder_mechanics_triggers.txt")["tv_wonder_location_can_host_locked_wonder_trigger"]
    assert not contains(dispatch,"exists","scope:actor")
    assert contains(dispatch,"owner")
