#!/usr/bin/env python3
"""Validate scale-based Engineering Department wonder data rules."""

from collections import Counter
import importlib.util
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "scripts_engineering_department") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))
TRIGGER_GENERATOR = (
    REPO_ROOT
    / "scripts_engineering_department" / "in_game"
    / "common"
    / "scripted_triggers"
    / "gen_tv_engineering_department_wonder_mechanics_triggers.py"
)
SITE_REQUIREMENT_AUDITOR = (
    REPO_ROOT / "scripts_engineering_department" / "audit_unique_wonder_site_requirements.py"
)
EFFECT_GENERATOR = (
    REPO_ROOT
    / "scripts_engineering_department" / "in_game"
    / "common"
    / "scripted_effects"
    / "gen_tv_engineering_department_wonder_mechanics_effects.py"
)
WONDER_MECHANICS_ENGLISH_LOC_GENERATOR = (
    REPO_ROOT
    / "scripts_engineering_department" / "main_menu"
    / "localization"
    / "english"
    / "gen_tv_engineering_department_wonder_mechanics_l_english.py"
)
WONDER_MECHANICS_CHINESE_LOC_GENERATOR = (
    REPO_ROOT
    / "scripts_engineering_department" / "main_menu"
    / "localization"
    / "simp_chinese"
    / "gen_tv_engineering_department_wonder_mechanics_l_simp_chinese.py"
)
ENGINEERING_DEPARTMENT_EFFECTS = (
    REPO_ROOT
    / "src" / "in_game"
    / "common"
    / "scripted_effects"
    / "tv_engineering_department_effects.txt"
)
ENGINEERING_DEPARTMENT_PRODUCTION_METHODS = (
    REPO_ROOT / "src" / "in_game" / "common"
    / "production_methods" / "tv_engineering_department_production_methods.txt"
)
ENGINEERING_DEPARTMENT_ROOT = REPO_ROOT / "src"

from wonder_mechanics.io import load_all_wonder_mechanics
from wonder_mechanics.modifiers import validate_wonder_size_base_country_modifier_rules
from wonder_localization_lib import load_wonder_localization_data
from great_projects_editor_web.services.wonder.localization import render_expected_localization_output


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_worksite_maintenance_input_contract() -> None:
    """Keep the restored production chain identical to the pre-removal revision."""
    import hashlib

    manifest = json.loads((REPO_ROOT / "tests/fixtures/wonder_materials_history.json").read_text(encoding="utf-8"))
    for entry in manifest["blocks"]:
        text = (REPO_ROOT / entry["path"]).read_text(encoding="utf-8-sig")
        match = re.search(r"(?ms)^" + re.escape(entry["key"]) + r" = \{.*?^}", text)
        require(match is not None, f"Missing restored definition: {entry['key']}")
        require(
            hashlib.sha256(match[0].encode()).hexdigest() == entry["sha256"],
            f"Restored definition differs from {manifest['source_commit']}: {entry['key']}",
        )
    for entry in manifest["assets"]:
        path = REPO_ROOT / entry["path"]
        require(path.is_file(), f"Missing restored asset: {entry['path']}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"],
                f"Restored asset differs from history: {entry['path']}")

    buildings = (ENGINEERING_DEPARTMENT_ROOT / "in_game/common/building_types/tv_engineering_department_buildings.txt").read_text(encoding="utf-8-sig")
    worksite = extract_trigger_block(buildings, "tv_wonder_labor_camp")
    methods = re.findall(r"^\s*(tv_wonder_labor_camp_[a-z0-9_]+)\s*$",
                         extract_trigger_block(worksite, "possible_production_methods"), re.MULTILINE)
    require(methods == ["tv_wonder_labor_camp_maintenance"],
            "Government worksites must have one maintenance method; alternatives belong to the profitable workshop.")
    effects = ENGINEERING_DEPARTMENT_EFFECTS.read_text(encoding="utf-8-sig")
    for effect in ("tv_wonder_clear_current_survey_effect", "tv_wonder_clear_project_state_core_effect"):
        body = extract_trigger_block(effects, effect)
        for variable in ("tv_wonder_effective_material_workshop_levels", "tv_wonder_material_workshop_need",
                         "tv_wonder_material_workshop_need_display", "tv_wonder_material_input_shortage_construction_progress"):
            require(f"remove_variable = {variable}" in body, f"{effect} must clear {variable}")
    gui = (ENGINEERING_DEPARTMENT_ROOT / "in_game/gui/panels/organization/tv_engineering_department.gui").read_text(encoding="utf-8-sig")
    for filter_key in ("uses_tv_wonder_materials", "tv_wonder_materials"):
        require(f"OpenLateralViewWithFilter('production', '{filter_key}')" in gui,
                f"Missing production entry point: {filter_key}")
    for language in ("english", "simp_chinese"):
        loc = (ENGINEERING_DEPARTMENT_ROOT / f"main_menu/localization/{language}/tv_engineering_department_l_{language}.yml").read_text(encoding="utf-8-sig")
        for key in ("tv_wonder_materials", "tv_wonder_material_dispatch_point", "tv_wonder_material_dispatch_point_price",
                    "tv_wonder_material_dispatch_point_production", "tv_wonder_material_dispatch_point_production_no_marble",
                    "TV_ENGINEERING_MATERIAL_WORKSHOP_PROGRESS_TT", "TV_WONDER_MATERIAL_INPUT_SHORTAGE_CONSTRUCTION_PROGRESS"):
            require(re.search(rf"^ {key}:", loc, re.MULTILINE), f"Missing {language} localization: {key}")


def load_trigger_generator():
    spec = importlib.util.spec_from_file_location("wonder_mechanics_trigger_generator", TRIGGER_GENERATOR)
    require(spec is not None and spec.loader is not None, "Could not load wonder mechanics trigger generator.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_site_requirement_auditor():
    spec = importlib.util.spec_from_file_location("wonder_site_requirement_auditor", SITE_REQUIREMENT_AUDITOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load site-requirement auditor: {SITE_REQUIREMENT_AUDITOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_effect_generator():
    spec = importlib.util.spec_from_file_location("wonder_mechanics_effect_generator", EFFECT_GENERATOR)
    require(spec is not None and spec.loader is not None, "Could not load wonder mechanics effect generator.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_ceremony_loc_generator(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"Could not load {name}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_trigger_block(script: str, name: str) -> str:
    marker = f"{name} = {{"
    start = script.find(marker)
    require(start >= 0, f"Missing generated trigger {name}.")
    depth = 0
    for index in range(start, len(script)):
        char = script[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return script[start : index + 1]
    raise AssertionError(f"Generated trigger {name} is not closed.")


def extract_assignment_block_containing(script: str, assignment: str, marker: str) -> str:
    marker_index = script.find(marker)
    require(marker_index >= 0, f"Missing marker {marker} in {assignment} block.")
    start = script.rfind(f"{assignment} = {{", 0, marker_index)
    require(start >= 0, f"Missing containing {assignment} block for {marker}.")
    depth = 0
    for index in range(start, len(script)):
        char = script[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return script[start : index + 1]
    raise AssertionError(f"Containing {assignment} block for {marker} is not closed.")


def validate_generated_trigger_scope_layers(wonders: list[dict]) -> None:
    trigger_script = load_trigger_generator().generate()
    require(
        "tv_wonder_can_start_project_" not in trigger_script,
        "Generator must not emit country-level start-project target pre-scans for survey selectors.",
    )
    for wonder in wonders:
        key = wonder["key"]
        country_gate = f"tv_wonder_country_has_{key}_project_or_final_trigger"
        location_host = extract_trigger_block(trigger_script, f"tv_wonder_location_can_host_{key}_trigger")
        require(
            country_gate not in location_host,
            f"Location host trigger for {key} must not contain country-level uniqueness gates.",
        )
        require(
            "scope:actor" not in location_host,
            f"Location host trigger for {key} must not depend on actor scope.",
        )

        can_build = extract_trigger_block(trigger_script, f"tv_wonder_can_build_{key}_trigger")
        if wonder["size"] == "small":
            require(country_gate not in can_build, f"Small can-build trigger for {key} should not be unique-gated.")
        else:
            require(country_gate in can_build, f"{key} can-build trigger must enforce country uniqueness.")

        if int(wonder.get("initial_level") or 0) > 0:
            expandable = extract_trigger_block(
                trigger_script,
                f"tv_wonder_location_has_{key}_expandable_final_building_trigger",
            )
            require(
                f"is_key_in_variable_map = {{ name = tv_wonder_surveyed target = {int(wonder['id'])} }}"
                in expandable,
                f"{key} initial final building must remain expandable before its first survey.",
            )


def validate_survey_map_trigger_guards(wonders: list[dict]) -> None:
    generator = load_trigger_generator()
    script = generator.generate()

    def guarded_map_read(block: str, map_name: str, target: object, absent_result: str) -> str:
        key_check = f"is_key_in_variable_map = {{ name = {map_name} target = {target} }}"
        branch = extract_assignment_block_containing(block, "trigger_if", key_check)
        limit = extract_trigger_block(branch, "limit")
        require(
            f"has_variable_map = {map_name}" in limit and key_check not in limit,
            f"{map_name} membership must only be evaluated after its map exists.",
        )
        require(key_check in branch, f"{map_name} key check escaped its conditional branch.")
        after_branch = block[block.index(branch) + len(branch) :].lstrip()
        require(
            after_branch.startswith(f"trigger_else = {{ always = {absent_result} }}"),
            f"Missing {map_name} must explicitly return {absent_result}.",
        )
        return branch

    for wonder in wonders:
        wonder_id = int(wonder["id"])
        expandable = extract_trigger_block(
            script, f"tv_wonder_location_has_{wonder['key']}_expandable_final_building_trigger"
        )
        stored_tier = guarded_map_read(expandable, "tv_wonder_survey_scale_tier", wonder_id, "no")
        # A map for another wonder must not bypass the current wonder's key check.
        require(
            extract_trigger_block(stored_tier, "is_key_in_variable_map")
            == f"is_key_in_variable_map = {{ name = tv_wonder_survey_scale_tier target = {wonder_id} }}",
            f"{wonder['key']} must require its own stored tier key.",
        )
        for level in range(1, 6):
            require(
                f'"variable_map(tv_wonder_survey_scale_tier|{wonder_id})" ?= {{ this >= {level + 1} }}'
                in stored_tier,
                f"{wonder['key']} level {level} must require a tier permitting the next level.",
            )
        for building in generator.final_buildings(wonder):
            require(
                f"NOT = {{ {generator.loc_level(building, '>=', 6)} }}" in expandable,
                f"{building} must retain its level-six cap.",
            )
        require(
            "has_global_variable = tv_engineering_department_unlimited_scale" in expandable,
            f"{wonder['key']} must retain the unlimited-scale option.",
        )
        if int(wonder.get("initial_level") or 0) > 0:
            unsurveyed = guarded_map_read(expandable, "tv_wonder_surveyed", wonder_id, "yes")
            require(
                f"NOT = {{ is_key_in_variable_map = {{ name = tv_wonder_surveyed target = {wonder_id} }} }}"
                in unsurveyed,
                f"{wonder['key']} must remain unsurveyed when another wonder's map lacks its key.",
            )

    cached = extract_trigger_block(script, "tv_wonder_selected_survey_already_cached_trigger")
    location = extract_trigger_block(cached, "scope:tv_wonder_selected_survey_site")
    guarded_map_read(location, "tv_wonder_surveyed", "prev.var:tv_wonder_locked", "no")


def validate_existing_unique_initialization_seeds_survey_maps(wonders: list[dict]) -> None:
    location_display_script = load_effect_generator().generate_location_display_effects()
    init_block = extract_trigger_block(
        location_display_script,
        "tv_wonder_initialize_existing_unique_wonders_effect",
    )
    seed_block = extract_trigger_block(
        location_display_script,
        "tv_wonder_seed_existing_unique_wonders_effect",
    )
    existing_unique_ids = [
        int(wonder["id"])
        for wonder in wonders
        if wonder.get("is_unique") and int(wonder.get("initial_level") or 0) > 0
    ]
    require(existing_unique_ids, "Expected at least one game-start unique wonder.")
    initialization_guard = "NOT = { has_global_variable = tv_wonder_existing_unique_wonders_initialized }"
    initialization_marker = "set_global_variable = tv_wonder_existing_unique_wonders_initialized"
    require(
        init_block.count(initialization_guard) == 1,
        "Existing unique wonder initialization must have exactly one save-level guard.",
    )
    require(
        init_block.count(initialization_marker) == 1,
        "Existing unique wonder initialization must set its save-level marker exactly once.",
    )
    require(
        init_block.index(initialization_guard)
        < init_block.index("tv_wonder_seed_existing_unique_wonders_effect = yes"),
        "Existing unique wonder initialization guard must wrap the seed effect call.",
    )
    require(
        init_block.index(initialization_marker)
        > init_block.index("tv_wonder_seed_existing_unique_wonders_effect = yes"),
        "Existing unique wonder initialization marker must be set after the seed effect completes.",
    )
    expected_survey_seed = {
        "tv_wonder_surveyed": 1,
        "tv_wonder_survey_scale_competence": 100,
        "tv_wonder_survey_logistics_competence": 85,
        "tv_wonder_survey_organization_competence": 85,
        "tv_wonder_survey_scale_tier": 6,
    }
    for wonder_id in existing_unique_ids:
        for map_name, value in expected_survey_seed.items():
            require(
                f"add_to_variable_map = {{ name = {map_name} key = {wonder_id} value = {value} }}" in seed_block,
                f"Game-start unique wonder {wonder_id} must seed {map_name} with {value}.",
            )


def validate_editor_localization_rendering_matches_generators() -> None:
    localization_data = load_wonder_localization_data()
    for language, name, path in (
        ("english", "wonder_mechanics_english_loc_generator", WONDER_MECHANICS_ENGLISH_LOC_GENERATOR),
        ("simp_chinese", "wonder_mechanics_chinese_loc_generator", WONDER_MECHANICS_CHINESE_LOC_GENERATOR),
    ):
        actual = load_ceremony_loc_generator(name, path).generate()
        expected = render_expected_localization_output(language, localization_data)
        require(actual == expected, f"Editor localization rendering must match {name}.")


def validate_site_requirement_audit_uses_authoritative_ports() -> dict[str, dict]:
    auditor = load_site_requirement_auditor()
    ports = auditor.load_ports()
    require(
        ports.get("jiangyin") == "yantze_estuary",
        "The site-requirement audit must load Jiangyin's authoritative ports.csv entry.",
    )
    require(
        ports.get("malacca") == "inner_strait_malacca",
        "The site-requirement audit must load Malacca's authoritative ports.csv entry.",
    )

    summary = auditor.audit()
    rows = {row["key"]: row for row in summary["results"]}
    require(
        rows["unique_longjiang_shipyard"]["status"] == "PASS",
        "Longjiang Shipyard at Jiangyin must pass is_port using ports.csv, even with zero harbor suitability.",
    )
    require(
        rows["unique_malacca_port"]["status"] == "PASS",
        "Malacca Port must pass is_port using ports.csv, even with zero harbor suitability.",
    )
    return rows


def validate_asia_wonder_expansion_coverage(
    wonders: list[dict],
    site_audit_rows: dict[str, dict],
) -> None:
    generic_wonders = [wonder for wonder in wonders if not wonder.get("is_unique")]
    unique_wonders = [wonder for wonder in wonders if wonder.get("is_unique")]
    require(
        len(generic_wonders) == 56,
        f"Asia expansion must leave exactly 56 generic wonder prototypes, got {len(generic_wonders)}.",
    )
    require(
        len(unique_wonders) == 139,
        "must have exactly 139 unique wonders (including the Grand Palace and Wat Arun)",
    )

    expected_generic_ids = {
        55: "grand_garden_complex",
        56: "state_examination_complex",
    }
    actual_generic_ids = {
        wonder["id"]: wonder["key"]
        for wonder in generic_wonders
        if wonder["id"] in expected_generic_ids
    }
    require(
        actual_generic_ids == expected_generic_ids,
        f"Asia expansion generic wonder IDs drifted: expected {expected_generic_ids}, got {actual_generic_ids}.",
    )

    expected_unique_ids = {
        224: "unique_suzhou_classical_gardens",
        225: "unique_fin_garden",
        226: "unique_jiangnan_examination_hall",
        227: "unique_thang_long_temple_of_literature",
        228: "unique_maragheh_observatory",
        229: "unique_xian_bell_and_drum_towers",
        230: "unique_behistun_inscription",
        231: "unique_beijing_imperial_granaries",
        232: "unique_bursa_imperial_mint",
        233: "unique_enderun_palace_school",
        234: "unique_ayutthaya_foreign_quarters",
        235: "unique_yunnan_weisuo_colonies",
        236: "unique_zhoushan_beacon_network",
    }
    actual_unique_ids = {
        wonder["id"]: wonder["key"]
        for wonder in unique_wonders
        if wonder["id"] in expected_unique_ids
    }
    require(
        actual_unique_ids == expected_unique_ids,
        f"Asia expansion unique wonder IDs drifted: expected {expected_unique_ids}, got {actual_unique_ids}.",
    )

    formerly_unadopted_base_keys = {
        "giant_observatory",
        "royal_granary_system",
        "frontier_colonization_belt",
        "coastal_beacon_network",
        "war_college_system",
        "great_clock_bell_system",
        "world_embassy_quarter",
        "law_code_stele_project",
        "royal_mint_system",
    }
    unique_adoption_counts = Counter(wonder["base_key"] for wonder in unique_wonders)
    still_unadopted = sorted(
        base_key
        for base_key in formerly_unadopted_base_keys
        if unique_adoption_counts[base_key] < 1
    )
    require(
        not still_unadopted,
        "Asia expansion must give every formerly zero-adoption prototype at least one unique wonder: "
        + ", ".join(still_unadopted),
    )

    missing_audit_rows = sorted(set(expected_unique_ids.values()) - set(site_audit_rows))
    require(
        not missing_audit_rows,
        "Asia expansion wonders are missing from the site-requirement audit: "
        + ", ".join(missing_audit_rows),
    )
    non_passing_sites = {
        key: site_audit_rows[key]["status"]
        for key in expected_unique_ids.values()
        if site_audit_rows[key]["status"] != "PASS"
    }
    require(
        not non_passing_sites,
        f"All 13 Asia expansion unique wonders must pass the site-requirement audit: {non_passing_sites}.",
    )


def main() -> None:
    from audit_wonder_rituals import audit
    wonders, mechanics = load_all_wonder_mechanics()
    validate_worksite_maintenance_input_contract()
    validate_wonder_size_base_country_modifier_rules(wonders, mechanics)
    validate_generated_trigger_scope_layers(wonders)
    validate_survey_map_trigger_guards(wonders)
    validate_existing_unique_initialization_seeds_survey_maps(wonders)
    validate_editor_localization_rendering_matches_generators()
    rows = validate_site_requirement_audit_uses_authoritative_ports()
    validate_asia_wonder_expansion_coverage(wonders, rows)
    audit()
    print("[OK] Construction, survey, initialization, localization and ritual contracts validated.")


if __name__ == "__main__":
    main()
