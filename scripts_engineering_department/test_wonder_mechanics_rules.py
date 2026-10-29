#!/usr/bin/env python3
"""Validate scale-based Engineering Department wonder data rules."""

from collections import Counter
from decimal import Decimal
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
    """Preserve restored integration; workshop recipes follow the regional rework."""
    import hashlib

    manifest = json.loads((REPO_ROOT / "tests/fixtures/wonder_materials_history.json").read_text(encoding="utf-8"))
    for entry in manifest["blocks"]:
        text = (REPO_ROOT / entry["path"]).read_text(encoding="utf-8-sig")
        match = re.search(r"(?ms)^" + re.escape(entry["key"]) + r" = \{.*?^}", text)
        require(match is not None, f"Missing restored definition: {entry['key']}")
        # The original fixture remains historical evidence, not a new balance snapshot.
        # These two recipes are now covered by the economic contract below.
        if entry["key"] in {
            "tv_wonder_material_dispatch_point_production",
            "tv_wonder_material_dispatch_point_production_no_marble",
        }:
            continue
        historical_block = match[0]
        if entry["key"] == "tv_wonder_material_dispatch_point":
            # Only its method list changed: still enforce all other historical properties.
            current_methods = extract_trigger_block(historical_block, "possible_production_methods")
            historical_block = historical_block.replace(current_methods,
                "possible_production_methods = {\n"
                "\t\ttv_wonder_material_dispatch_point_production\n"
                "\t\ttv_wonder_material_dispatch_point_production_no_marble\n\t}")
        if entry["key"] == "tv_wonder_update_logistics_metrics_effect":
            # Fixed output changed 2 -> 1, so the demand display now needs 20 workshops.
            # Preserve the historical check for the rest of this logistics effect.
            historical_block = re.sub(
                r"(name = tv_wonder_material_workshop_need\s+value = \{\s+"
                r"value = var:tv_wonder_effective_worksite_levels\s+multiply = )20\b",
                r"\g<1>10", historical_block, count=1,
            )
        require(
            hashlib.sha256(historical_block.encode()).hexdigest() == entry["sha256"],
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
    validate_material_workshop_production_contract()


def load_material_workshop_economy():
    """Read deployed recipes and actual goods prices, without a duplicated price table."""
    goods_prices = {}
    for folder in (
        REPO_ROOT / ".eu5-base/reference_game_files/game/in_game/common/goods",
        ENGINEERING_DEPARTMENT_ROOT / "in_game/common/goods",
    ):
        for path in sorted(folder.glob("*.txt")):
            for key, body in re.findall(r"(?ms)^(\w+)\s*=\s*\{(.*?)^}", path.read_text(encoding="utf-8-sig")):
                price = re.search(r"\bdefault_market_price\s*=\s*([\d.]+)", body)
                if price:
                    goods_prices[key] = Decimal(price[1])
    buildings = (ENGINEERING_DEPARTMENT_ROOT / "in_game/common/building_types/tv_engineering_department_buildings.txt").read_text(encoding="utf-8-sig")
    workshop = extract_trigger_block(buildings, "tv_wonder_material_dispatch_point")
    method_list = extract_trigger_block(workshop, "possible_production_methods")
    method_ids = re.findall(r"^\s*(tv_\w+)\s*$", method_list, re.MULTILINE)
    script = ENGINEERING_DEPARTMENT_PRODUCTION_METHODS.read_text(encoding="utf-8-sig")
    recipes = {}
    for method in method_ids:
        body = extract_trigger_block(script, method)
        fields = re.findall(r"^\s+(\w+)\s*=\s*(\S+)\s*$", body, re.MULTILINE)
        require(len(dict(fields)) == len(fields), f"Duplicate recipe field: {method}")
        recipes[method] = dict(fields)
    return goods_prices, method_ids, recipes


def validate_material_workshop_production_contract() -> None:
    prices, method_ids, recipes = load_material_workshop_economy()
    require(5 <= len(method_ids) <= 10 and len(set(method_ids)) == len(method_ids),
            "Workshop must expose 5-10 distinct regional methods.")
    script = ENGINEERING_DEPARTMENT_PRODUCTION_METHODS.read_text(encoding="utf-8-sig")
    declared = re.findall(r"(?m)^(tv_wonder_material_dispatch_point_production\w*) =", script)
    require(set(declared) == set(method_ids) and len(declared) == len(method_ids),
            "Every workshop method must be defined once and selectable.")
    profits = []
    inputs_by_method = []
    for method, fields in recipes.items():
        require(fields.get("produced") == "tv_wonder_materials", f"Wrong output good: {method}")
        require(Decimal(fields.get("output", "0")) == 1, f"Output must be exactly 1.00: {method}")
        require(fields.get("category") == "building_maintenance", f"Wrong category: {method}")
        inputs = {key: Decimal(value) for key, value in fields.items()
                  if key not in {"produced", "output", "category"}}
        require(bool(inputs) and all(key in prices and value > 0 for key, value in inputs.items()),
                f"Inputs must be positive amounts of defined goods: {method}")
        require("tv_wonder_materials" not in inputs, f"Recipe must not consume its own output: {method}")
        cost = sum(prices[key] * value for key, value in inputs.items())
        profit = prices["tv_wonder_materials"] - cost
        require(0 <= profit / cost < Decimal("0.30"), f"Base profit outside engine limits: {method}")
        profits.append(profit)
        inputs_by_method.append(inputs)
    require(all(a < b for a, b in zip(profits, profits[1:])),
            "Base profits must strictly increase with processing sophistication.")
    require(profits[0] <= Decimal("0.05"), "The simplest method must barely break even.")
    require(sum("tools" not in recipe for recipe in inputs_by_method) >= 3,
            "Tool-poor regions need multiple independent production routes.")
    require(any("marble" in recipe for recipe in inputs_by_method)
            and any("marble" not in recipe for recipe in inputs_by_method[-2:]),
            "Both marble-rich and marble-poor regions need advanced routes.")
    worksite = extract_trigger_block(script, "tv_wonder_labor_camp_maintenance")
    materials_demand = re.search(r"tv_wonder_materials\s*=\s*([\d.]+)", worksite)
    effects = ENGINEERING_DEPARTMENT_EFFECTS.read_text(encoding="utf-8-sig")
    workshop_need = re.search(
        r"name = tv_wonder_material_workshop_need\s+value = \{\s+"
        r"value = var:tv_wonder_effective_worksite_levels\s+multiply = ([\d.]+)", effects,
    )
    require(materials_demand is not None and workshop_need is not None,
            "Worksite demand and workshop capacity display must remain connected.")
    require(all(Decimal(workshop_need[1]) * Decimal(fields["output"]) == Decimal(materials_demand[1])
                for fields in recipes.values()), "Workshop capacity display must reflect the new fixed output.")
    for language in ("english", "simp_chinese"):
        path = ENGINEERING_DEPARTMENT_ROOT / f"main_menu/localization/{language}/tv_engineering_department_l_{language}.yml"
        require(path.read_bytes().startswith(b"\xef\xbb\xbf"), f"Missing localization BOM: {language}")
        loc = path.read_text(encoding="utf-8-sig")
        names = []
        for method in method_ids:
            values = re.findall(rf'^ {method}:(?:0)? "([^"\n]+)"$', loc, re.MULTILINE)
            require(len(values) == 1, f"Missing/duplicate localized method name: {language}/{method}")
            names.extend(values)
        require(len(set(names)) == len(names), f"Method names must be distinct: {language}")


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


def validate_world_market_effect_contract(mechanics: dict) -> None:
    """Keep market attraction out of repeatable project levels and preserve exact replacements."""
    port = mechanics["buildings"]["great_port"]["final_local"]
    canal = mechanics["buildings"]["canal_hub_city"]["final_local"]
    market_design = mechanics["buildings"]["world_market"]
    market_country = mechanics["base_modifiers"]["world_market"]
    require(port.get("harbor_suitability") == 0.2 and "local_trade_center_power" not in port,
            "Great Port must use harbor_suitability = 0.2 without repeatable market attraction.")
    require(canal.get("local_build_new_buildings_efficiency") == 0.1
            and "local_trade_center_power" not in canal,
            "Canal Hub City must replace repeatable market attraction with building efficiency.")
    require(market_design["final_local"] == {}
            and market_design["include_local_cultural_baseline"] is False,
            "World Market must have no authored or shared local baseline effect.")
    require(market_country.get("selling_efficiency") == 0.0125
            and "global_trade_center_power" not in market_country,
            "World Market must use selling_efficiency = 0.0125, not global market attraction.")

    buildings = (REPO_ROOT / "src/in_game/common/building_types/tv_engineering_department_wonder_mechanics_buildings.txt").read_text(encoding="utf-8-sig")
    market_block = extract_trigger_block(buildings, "tv_wonder_luxury_goods_market")
    market_modifier = extract_trigger_block(market_block, "modifier")
    for key in ("local_cultural_tradition", "local_cultural_influence", "local_trade_center_power", "local_migration_attraction"):
        require(not re.search(rf"(?m)^\s*{re.escape(key)}\s*=", market_modifier),
                f"World Market actual building must not retain local modifier: {key}")
    require(re.search(r"(?m)^\s*selling_efficiency\s*=\s*0\.0125\s*$", market_modifier),
            "World Market actual building must preserve the exact 0.0125 selling-efficiency value.")

    zimbabwe = extract_trigger_block(buildings, "tv_wonder_unique_great_zimbabwe_inaugurated")
    zimbabwe_modifier = extract_trigger_block(zimbabwe, "modifier")
    require(not re.search(r"(?m)^\s*local_cultural_tradition\s*=|^\s*local_cultural_influence\s*=", zimbabwe_modifier),
            "Unique Great Zimbabwe must inherit World Market's no-location-effect rule.")
    require(re.search(r"(?m)^\s*selling_efficiency\s*=\s*0\.025\s*$", zimbabwe_modifier),
            "Unique Great Zimbabwe must inherit World Market selling efficiency at the unique x2 multiplier.")

    modifiers = (REPO_ROOT / "src/in_game/common/static_modifiers/tv_engineering_department_wonder_mechanics_modifiers.txt").read_text(encoding="utf-8-sig")
    require("selling_efficiency = 0.0125" in extract_trigger_block(modifiers, "tv_wonder_display_34_level_1"),
            "Generated level-1 static modifier must retain four-decimal precision.")
    auto = (REPO_ROOT / "src/in_game/common/auto_modifiers/tv_engineering_department_wonder_mechanics_auto_modifiers.txt").read_text(encoding="utf-8-sig")
    require("selling_efficiency = 0.0125" in extract_trigger_block(auto, "tv_wonder_auto_world_market"),
            "Generated auto modifier must retain four-decimal precision.")


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
    validate_world_market_effect_contract(mechanics)
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
