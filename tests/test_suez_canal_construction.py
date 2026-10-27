"""Suez hands off to native construction only after real wonder completion.

These inspect the generated lifecycle boundary, not Canal Manager internals.
Construction progress, save/load and fleet pathfinding still need game testing.
"""

from pathlib import Path

from scripts_engineering_department.wonder_mechanics.io import load_all_wonder_mechanics
from scripts_engineering_department.wonder_mechanics.naming import (
    final_building_completion_sync_hidden_event_execute_effect_name,
    final_building_completion_sync_hidden_event_id,
    final_building_completion_sync_hidden_event_trigger_effect_name,
    final_building_level_changed_effect_name,
)
from test_wonder_priority_proposals import child, contains, parse, source_blocks, walk


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "src/in_game"
FINALIZATION = "common/scripted_effects/tv_wonder_finalization_effects.txt"


def suez_wonder():
    wonders, _ = load_all_wonder_mechanics()
    canals = [wonder for wonder in wonders if wonder.get("native_canal")]
    assert [(wonder["key"], wonder["location"]) for wonder in canals] == [
        ("unique_suez_ancient_canal", "suez"),
    ]
    return canals[0]


def test_native_start_is_reached_from_the_deferred_real_completion_hook():
    wonder = suez_wonder()
    trigger_name = final_building_completion_sync_hidden_event_trigger_effect_name()
    execute_name = final_building_completion_sync_hidden_event_execute_effect_name()
    event_id = f"tv_engineering_department.{final_building_completion_sync_hidden_event_id()}"

    buildings = source_blocks("common/building_types/tv_engineering_department_wonder_mechanics_buildings.txt")
    completion = child(buildings[wonder["final_building"]], "on_construction_ended")
    location = child(child(completion.children, "hidden_effect").children, "location")
    assert contains(location.children, trigger_name, "yes")

    effects = source_blocks(FINALIZATION)
    scheduled = next(node for node in walk(effects[trigger_name]) if node.key == "trigger_event_silently")
    assert child(scheduled.children, "id").value == event_id
    assert child(scheduled.children, "days").value == "1"
    event = source_blocks("events/tv_wonder_finalization_events.txt")[event_id]
    assert child(event, "type").value == "location_event"
    assert child(event, "hidden").value == "yes"
    assert contains(child(event, "immediate").children, execute_name, "yes")


def test_start_requires_completed_suez_and_skips_open_or_in_progress_canals():
    wonder = suez_wonder()
    callback = source_blocks(FINALIZATION)[final_building_completion_sync_hidden_event_execute_effect_name()]
    branch = next(node for node in callback if node.key == "if" and contains(node.children, "start_canal_construction"))
    guard = child(branch.children, "limit").children
    assert child(guard, "this").value == "location:suez"
    assert child(guard, "exists").value == "owner"
    level = child(guard, "location_building_level").children
    assert child(level, "building_type").value == f"building_type:{wonder['final_building']}"
    assert (child(level, "value").op, child(level, "value").value) == (">=", "1")
    assert child(guard, "is_canal_open").value == "no"
    assert child(child(guard, "NOT").children, "has_canal_construction").value == "yes"
    assert not contains(guard, "has_building")

    vanilla = ROOT / ".eu5-base/reference_game_files/game/in_game/common/decisions/canal_construction.txt"
    decision = child(parse(vanilla.read_text(encoding="utf-8-sig")), "build_suez_canal")
    native_start = next(node for node in walk(decision.children) if node.key == "start_canal_construction")
    assert child(branch.children, "start_canal_construction") == native_start
    assert not {"add_gold", "pay_price", "has_advance", "current_age_or_later", "owns_or_non_sovereign_subject_owns"} & {
        node.key for node in walk(callback)
    }


def test_no_preview_or_demolition_path_controls_native_canal_state():
    # Catch extra call sites, including a future reintroduction of the old close
    # effect or a start in a visible option/ritual/ownership refresh.
    starts = []
    for path in GAME.rglob("*.txt"):
        text = path.read_text(encoding="utf-8-sig")
        if "start_canal_construction" not in text and "set_canal_open" not in text:
            continue
        blocks = parse(text)
        assert not contains(blocks, "set_canal_open"), path
        starts.extend((path.relative_to(GAME).as_posix(), block.key)
                      for block in blocks for node in walk(block.children)
                      if node.key == "start_canal_construction")
    assert starts == [(FINALIZATION, final_building_completion_sync_hidden_event_execute_effect_name())]

    wonder = suez_wonder()
    demolition = source_blocks("common/scripted_effects/tv_wonder_location_display_effects.txt")[
        final_building_level_changed_effect_name(wonder)
    ]
    assert contains(demolition, f"tv_wonder_{wonder['key']}_ritual_revoke_effect", "yes")
    assert contains(demolition, "tv_wonder_mechanics_refresh_location_display_state_effect", "yes")


def test_bilingual_player_descriptions_explain_the_extra_construction_phase():
    from scripts_engineering_department.wonder_localization_lib import load_wonder_localization_data

    localization = load_wonder_localization_data()
    for language, phrase in (("english", "only after canal construction finishes"),
                             ("simp_chinese", "须等开凿完成后")):
        for key in ("game_concept_tv_wonder_unique_suez_ancient_canal_desc",
                    "tv_wonder_unique_suez_ancient_canal_inaugurated_desc",
                    "tv_engineering_department.500.d_unique_suez_ancient_canal_plain"):
            assert phrase in localization[language][key]
