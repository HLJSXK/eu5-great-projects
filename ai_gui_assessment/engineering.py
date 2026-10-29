"""Render Engineering Department tabs and rituals from the actual ED mod GUI.

The scenario supplies explicit, invented data; it does not execute game scripts.
Renderer imports are delayed so callers can select an installed renderer first.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field, replace
from functools import lru_cache
import json
from pathlib import Path
import re
import sys

WORKSPACE = Path(__file__).resolve().parents[1]
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))
GUI_PATH = "in_game/gui/panels/organization/tv_engineering_department.gui"
STATE_TABS = {
    "no-engineer": "overview", "conception": "overview", "proposal": "overview",
    "debate": "overview", "support-reserve": "overview",
    "survey": "resolutions", "survey-complete": "resolutions",
    "construction": "custom", "construction-complete": "custom",
    "ceremony-ready": "custom", "ritual-progress": "custom",
    "unique-ready": "custom", "unique-progress": "custom", "finalized": "custom",
    "reritual-ready": "custom", "reritual-progress": "custom",
    "hagia-church": "custom", "hagia-mosque": "custom",
}
STATE_NAMES = tuple(STATE_TABS)
TABS = ("overview", "resolutions", "custom")
# Explicit fixture vocabulary: newly introduced bindings remain diagnostic.
PLAYER_VARIABLES = """
tv_great_engineer_char tv_wonder_active_part tv_wonder_body_units
tv_wonder_burghers_demand
tv_wonder_ritual_choice tv_wonder_clergy_demand tv_wonder_cmm_skip_ceremony
tv_wonder_concept_in_progress tv_wonder_construction_complete
tv_wonder_construction_progress_pct tv_wonder_decoration_units
tv_wonder_effective_worksite_levels tv_wonder_finalized tv_wonder_foundation_units
tv_wonder_effective_material_workshop_levels tv_wonder_material_workshop_need
tv_wonder_material_workshop_need_display
tv_wonder_function_units  tv_wonder_level tv_wonder_locked
tv_wonder_locked_concept_display_id tv_wonder_locked_display_id
tv_wonder_locked_image_display_id tv_wonder_locked_is_unique
tv_wonder_locked_mechanic_id tv_wonder_locked_style_count tv_wonder_logistics_competence
tv_wonder_logistics_progress_percent tv_wonder_monthly_construction_progress
tv_wonder_remaining_years tv_wonder_remaining_months_mod
tv_wonder_nobles_demand tv_wonder_organization_competence
tv_wonder_organization_site_level_cap tv_wonder_organization_site_level_cap_display

tv_wonder_priority_found tv_wonder_priority_selected_candidate_id tv_wonder_project_mode
tv_wonder_proposal tv_wonder_proposal_mode tv_wonder_proposal_slot_1
tv_wonder_proposal_slot_2 tv_wonder_proposal_slot_3 tv_wonder_ritual_in_progress
tv_wonder_ritual_months_completed tv_wonder_ritual_progress_pct tv_wonder_scale_competence
tv_wonder_ritual_duration_months tv_wonder_ritual_completed tv_wonder_ritual_reward_claimed
tv_wonder_finalization_outcome tv_wonder_locked_size
tv_wonder_scale_tier
 tv_wonder_site tv_wonder_stage
tv_wonder_suitability_current_revealed tv_wonder_survey_complete tv_wonder_survey_site
""".split()
UNSUPPORTED = [
    "Sample data, not a save game; actions, script effects and monthly changes are not executed.",
    "3D character portraits and procedural country flags are not rendered.",
    "Hover states, animation and native scrolling are not reproduced.",
]


@dataclass(frozen=True)
class ScenarioState:
    """Separate country and organization stores, as the live GUI does."""

    name: str
    player_variables: dict[str, int | float | bool | None] = field(default_factory=dict)
    organization_variables: dict[str, int | float | bool | None] = field(default_factory=dict)
    engineer_name: str = "乔瓦尼·达·丰塔纳"
    tab: str = "overview"
    # Typed scope accessors and lists can be supplied by a JSON fixture.
    objects: dict[str, dict] = field(default_factory=dict)
    lists: dict[str, list] = field(default_factory=dict)
    action_availability: dict[str, bool] = field(default_factory=dict)
    global_variables: dict[str, int | float | bool | None] = field(default_factory=lambda: {'hagia_sophia_now_mosque': None})


@lru_cache(maxsize=1)
def wonder_data():
    from scripts_engineering_department.wonder_mechanics.io import load_all_wonder_mechanics
    return load_all_wonder_mechanics()


def scenario_state(name: str = "debate") -> ScenarioState:
    if name not in STATE_NAMES:
        raise ValueError(f"Unknown engineering state: {name}")
    player = dict.fromkeys(PLAYER_VARIABLES)
    for estate in ('nobles_estate', 'clergy_estate', 'burghers_estate', 'peasants_estate', 'dhimmi_estate', 'tribes_estate', 'cossacks_estate'):
        player[f'tv_wonder_estate_pref_{estate}'] = None
        player[f'tv_wonder_estate_pref_source_{estate}'] = None
    for index in range(1, 6):
        player[f"tv_wonder_suitability_current_actual_{index}"] = None
    player["tv_wonder_stage"] = 0
    organization = {"tv_wonder_concept_progress": 0, "tv_wonder_domestic_support": 0,
                    "tv_wonder_survey_progress": 0}
    if name != "no-engineer":
        player["tv_great_engineer_char"] = 1
    if name == "conception":
        player["tv_wonder_concept_in_progress"] = True
        organization["tv_wonder_concept_progress"] = 45
    if name == "proposal":
        player.update(tv_wonder_proposal=3, tv_wonder_proposal_slot_1=3,
                      tv_wonder_proposal_slot_2=7, tv_wonder_proposal_slot_3=10)
    if name in ("debate", "support-reserve"):
        player.update(tv_wonder_stage=1, tv_wonder_locked=3, tv_wonder_locked_display_id=3,
                      tv_wonder_locked_image_display_id=3, tv_wonder_nobles_demand=1,
                      tv_wonder_burghers_demand=2, tv_wonder_clergy_demand=3)
        organization["tv_wonder_domestic_support"] = 135 if name == "support-reserve" else 68
    tab = STATE_TABS[name]
    objects = {}
    if tab != "overview":
        player.update(tv_wonder_stage=2, tv_wonder_locked=3, tv_wonder_locked_display_id=3,
                      tv_wonder_locked_image_display_id=3, tv_wonder_locked_concept_display_id=3,
                      tv_wonder_locked_is_unique=0, tv_wonder_locked_style_count=3,
                      tv_wonder_locked_mechanic_id=1, tv_wonder_scale_competence=70,
                      tv_wonder_organization_competence=65, tv_wonder_logistics_competence=55,
                      tv_wonder_scale_tier=3, tv_wonder_organization_site_level_cap=3,
                      tv_wonder_organization_site_level_cap_display=3,
                      tv_wonder_effective_material_workshop_levels=0,
                      tv_wonder_material_workshop_need=0, tv_wonder_material_workshop_need_display=1,
                      tv_wonder_logistics_progress_percent=55, tv_wonder_survey_site=1,
                      tv_wonder_suitability_current_revealed=1)
        for index in range(1, 6):
            player[f"tv_wonder_suitability_current_actual_{index}"] = (0, 1, 2, 1, 0)[index - 1]
        organization["tv_wonder_survey_progress"] = 100 if name != "survey" else 45
        objects["tv_wonder_survey_site.GetLocation"] = location_context("rijeka", "里耶卡")
    if name == "survey-complete":
        player["tv_wonder_survey_complete"] = 1
    if tab == "custom":
        player.update(tv_wonder_site=1, tv_wonder_survey_complete=1, tv_wonder_stage=3,
                      tv_wonder_level=0, tv_wonder_project_mode=1,
                      tv_wonder_foundation_units=3, tv_wonder_body_units=1,
                      tv_wonder_function_units=0, tv_wonder_decoration_units=0,
                      tv_wonder_active_part=2, tv_wonder_construction_progress_pct=42,
                      tv_wonder_effective_worksite_levels=3, tv_wonder_monthly_construction_progress=12,
                      tv_wonder_effective_material_workshop_levels=24,
                      tv_wonder_material_workshop_need=30, tv_wonder_material_workshop_need_display=30,
                      tv_wonder_remaining_years=0, tv_wonder_remaining_months_mod=5)
        objects["tv_wonder_site.GetLocation"] = location_context("rijeka", "里耶卡")
    if tab == "custom" and name != "construction":
        player.update(tv_wonder_construction_complete=1, tv_wonder_stage=4,
                      tv_wonder_level=1, tv_wonder_active_part=None,
                      tv_wonder_construction_progress_pct=100, tv_wonder_body_units=3,
                      tv_wonder_function_units=3, tv_wonder_decoration_units=3)
    if tab == "custom" and name != "construction":
        from scripts_engineering_department.wonder_mechanics.rituals import location_reward_estate, ritual_styles
        wonders, mechanics = wonder_data()
        wonder_id = 102 if name.startswith("hagia-") else 101 if name.startswith("unique-") else 3
        wonder = next(w for w in wonders if w["id"] == wonder_id)
        player.update(tv_wonder_locked=wonder_id, tv_wonder_locked_display_id=wonder_id,
                      tv_wonder_locked_image_display_id=wonder_id, tv_wonder_locked_concept_display_id=wonder_id,
                      tv_wonder_locked_is_unique=int(wonder["is_unique"]),
                      tv_wonder_locked_mechanic_id=next(w["id"] for w in wonders if w["key"] == wonder["mechanic_key"]),
                      tv_wonder_locked_size=("small", "medium", "large").index(wonder["size"]) + 1,
                      tv_wonder_ritual_choice=1, tv_wonder_ritual_duration_months=mechanics["ritual_rules"]["duration_months"],
                      tv_wonder_ritual_completed=None, tv_wonder_ritual_months_completed=0, tv_wonder_ritual_progress_pct=0)
        if wonder["is_unique"]:
            objects["tv_wonder_site.GetLocation"] = location_context(wonder["location"], "君士坦丁堡" if name.startswith("hagia-") else "亚历山大")
            objects["tv_wonder_survey_site.GetLocation"] = dict(objects["tv_wonder_site.GetLocation"])
        styles = ritual_styles(wonder, mechanics)
        for row in styles:
            n, sv = row["style"], row["societal_value"]
            player[f"tv_wonder_ritual_display_axis_{n}"] = list(mechanics["societal_axes"]).index(sv["axis"]) + 1
            player[f"tv_wonder_ritual_display_dir_{n}"] = sv["sign"]
            player[f"tv_wonder_ritual_position_{n}"] = -0.12
            player[f"tv_wonder_ritual_alignment_{n}"] = -0.12 * sv["sign"]
        for estate, n in styles[0]["estate_preferences"].items():
            if estate in ("nobles_estate", "clergy_estate", "burghers_estate", "peasants_estate"):
                player[f"tv_wonder_estate_pref_{estate}"] = 3 if n == "random" else n
                local_owner = estate == location_reward_estate(wonder) and any(
                    row["location_modifier"] and row["style"] == n for row in styles)
                player[f"tv_wonder_estate_pref_source_{estate}"] = 1 if local_owner else 3 if n == "random" else 2
        preferences = [player[f'tv_wonder_estate_pref_{estate}'] for estate in styles[0]['estate_preferences']
                       if player.get(f'tv_wonder_estate_pref_{estate}') is not None]
        for row in styles:
            n = row['style']
            player[f'tv_wonder_ritual_reward_kind_{n}'] = (int(bool(row['country_modifier']))
                + 2 * int(bool(row['location_modifier'])) + 4 * int(bool(row['one_shot'])))
            player[f'tv_wonder_ritual_support_{n}'] = preferences.count(n)
            player[f'tv_wonder_ritual_oppose_{n}'] = len(preferences) - preferences.count(n)
        if name.startswith(("reritual-", "hagia-")): player["tv_wonder_project_mode"] = 3
    if name in ("ritual-progress", "unique-progress", "reritual-progress", "finalized"):
        player.update(tv_wonder_ritual_in_progress=1, tv_wonder_ritual_months_completed=10,
                      tv_wonder_ritual_progress_pct=1000 / player["tv_wonder_ritual_duration_months"])
    if name == "finalized":
        player.update(tv_wonder_finalized=1, tv_wonder_ritual_in_progress=None, tv_wonder_ritual_completed=1,
                      tv_wonder_finalization_outcome=player["tv_wonder_ritual_choice"], tv_wonder_ritual_reward_claimed=1,
                      tv_wonder_ritual_months_completed=player["tv_wonder_ritual_duration_months"], tv_wonder_ritual_progress_pct=100)
    return ScenarioState(name, player, organization, tab=tab, objects=objects,
                         global_variables={'hagia_sophia_now_mosque': True if name == 'hagia-mosque' else None})


def location_context(key: str, name: str) -> dict:
    return {"__type__": "Location", "Self": key, "GetName": name, "GetNameWithNoTooltip": name}


def _exact(expression: str) -> str:
    return re.escape(expression)


@lru_cache(maxsize=1)
def modifier_metadata():
    return json.loads((WORKSPACE / "data/index/modifier_localization.json").read_text(encoding="utf-8"))["modifiers"]


def ritual_effect_sample(state: ScenarioState, loc) -> str:
    """Data-derived stand-in for native completion text; never executes effects."""
    from eu5_gui_renderer.fixtures import modifier_sample_lines
    from eu5_gui_renderer.paths import LANGUAGE
    from scripts_engineering_department.wonder_mechanics.rituals import ritual_style
    english = LANGUAGE == "english"
    player = state.player_variables
    if player.get("tv_wonder_ritual_reward_claimed") is not None:
        return "(Sample) Ritual rewards already granted." if english else "【示例】仪式奖励已发放。"
    choice = player.get("tv_wonder_finalization_outcome")
    if choice not in (1, 2, 3):
        choice = player.get("tv_wonder_ritual_choice") if player.get("tv_wonder_stage") == 4 else None
    if choice not in (1, 2, 3):
        return ""
    wonders, mechanics = wonder_data()
    wonder = next(w for w in wonders if w["id"] == player["tv_wonder_locked"])
    row = ritual_style(wonder, mechanics, choice)
    lines = ["(Sample from current data; not engine output)" if english else "【示例·当前数据，非引擎执行结果】"]
    for field, caption in (("country_modifier", "Country" if english else "国家奖励"),
                           ("location_modifier_values", "Location" if english else "地点奖励")):
        if not row[field]:
            continue
        lines.append(caption + (":" if english else "："))
        lines.extend(modifier_sample_lines(row[field], modifier_metadata(), loc))
    for reward in row["one_shot"]:
        lines.append(f"{loc.get(reward['type']) or reward['type']}: {reward['value']:+g}")
    sv = row["societal_value"]
    direction = loc.get(f"{sv['direction']}_focus") or sv["direction"]
    lines.append(f"Societal change towards {direction}: {sv['shock']:+g}" if english
                 else f"价值观向{direction}移动：{sv['shock']:+g}")
    if player.get("tv_wonder_project_mode") == 3:
        lines.append(f"{loc.get('prestige')}: {mechanics['ritual_rules']['reritual_prestige']:+g}")
    return "\n".join(lines)


def mocks(state: ScenarioState, loc=None) -> list:
    """Mock known accessors only; unrecognised bindings stay diagnostic."""
    from eu5_gui_renderer.fixtures import object_mocks, requirements_list, string_pair_list, variable_mocks
    def country_context():
        return {"__type__": "Country", "GetName": "匈牙利", "GetNameWithNoTooltip": "匈牙利"}

    character = {"__type__": "Character", "GetName": state.engineer_name, "GetAge": 42, "IsFemale": False, "IsAlive": True,
                 "GetNameToFit('(int32)40','(bool)yes')": state.engineer_name}
    result = []
    for key, value in state.global_variables.items():
        result.append((_exact(f"GetGlobalVariable('{key}').IsSet"), value is not None))
    for context in state.objects.values():
        if context.get('__type__') == 'Location' and context.get('Self') and context.get('GetName'):
            result.append((_exact(f"ShowLocationName('{context['Self']}')"), context['GetName']))
    player_variables = dict(state.player_variables)
    choice = player_variables.get('tv_wonder_ritual_choice')
    for field in ('display_axis', 'display_dir', 'position'):
        player_variables[f'tv_wonder_ritual_{field}_selected'] = player_variables.get(f'tv_wonder_ritual_{field}_{choice}')
    for store, prefix in [
        (player_variables, "InternationalOrganizationsView.GetPlayer.MakeScope"),
        (player_variables, "Country.MakeScope"),
        (state.organization_variables, "InternationalOrganizationsView.GetInternationalOrganization.MakeScope"),
    ]:
        result.extend(variable_mocks(prefix, store))
    result.extend([
        (_exact("InternationalOrganizationsView.GetPlayer.MakeScope.GetVariable('tv_great_engineer_char').GetCharacter"), character),
        (r"InternationalOrganizationsView\.GetPlayer(?:\.Self)?|Player(?:\.Self)?", country_context()),
        (r"InternationalOrganizationsView\.GetInternationalOrganization(?:\.Self)?", {
            "__type__": "InternationalOrganization", "GetNameWithNoTooltip": "工程部",
            "GetIcon": "gfx/interface/icons/location_icons/new/prosperity.dds",
            "MakeScope.GetVariable('iberian_union_active').IsSet": False,
        }),
        (r"InternationalOrganizationsView\.GetInternationalOrganization\.GetLeaderCountry", country_context()),
        (r"InternationalOrganizationsView\.GetPlayer\.MakeScope(?:\.Self)?|PlayerScope(?:\.Self)?", {"__type__": "Scope"}),
        (r"InternationalOrganizationsView\.Vars\.(?:HasValue|NotExistOrHasValue)\('organizations','([^']+)'\)",
         lambda match: match[1] == state.tab),
        (r"InternationalOrganizationsView\.Vars\.Exists\('[^']+'\)", False),
        (r"PdxGuiWidget\.IsUberButtonEnabled", True),
        (r"InternationalOrganizationsView\.HasOverview", True),
        (r"InternationalOrganizationsView\.(?:HasActions|HasCandidates|HasLaws|HasSpecialMembers)", False),
        (r"InternationalOrganizationsView\.(?:GetActions|GetSpecialMemberItems)", []),
        (r"InternationalOrganizationsView\.GetInternationalOrganization\.GetType\.GetNameKey", "tv_engineering_department"),
        (r"InternationalOrganizationsView\.GetInternationalOrganization\.(?:GetName|GetNameWithNoTooltip)", "工程部"),
        (r"InternationalOrganizationsView\.GetInternationalOrganization\.(?:UsesLeader|IsLeaderCountryInPlace)", True),
        (r"InternationalOrganizationsView\.GetInternationalOrganization\.(?:HasReligion|HasMonthlyEffect|HasLeaderChangeMethod|HasLeadershipElectionResolution)", False),
        (r"InternationalOrganizationsView\.GetInternationalOrganization\.HasParliament", False),
        (r"InternationalOrganizationsView\.GetInternationalOrganization\.GetReligion\.(?:HasCanonization|HasCardinals|HasHolySites|HasReligiousFactions)", False),
        (r"InternationalOrganizationsView\.GetInternationalOrganization\.GetType\.(?:HasDeclareWarOnTargetCasusBelli|ShowStrengthComparisonWithTarget)", False),
        (r"InternationalOrganizationsView\.GetInternationalOrganization\.GetType\.GetVariables", []),
        (r"IsPlayerValid", True),
        (r"IsIOFaved\(InternationalOrganization.Self\)", False),
        (r"PdxGuiWidget\.GetIndexInParent", 0),
        (r"Character\.GetPortraitBg", None),
        (r"GetGraphicalCultureTexture\('([^']+)'\)", lambda match: f"gfx/interface/graphical_cultures/european_gfx/{match[1]}.dds"),
        (r"Country\.GetGovernment", {"__type__": "Government", "HasRuler": True,
            "HasActiveRegent": False, "GetRuler": {"__type__": "Character"}, "GetActiveRegent": None}),
        (r"Country\.GetGovernment\.HasRulerOrRegent", True),
        (r"InternationalOrganizationsView\.GetIllustration", "gfx/interface/illustrations/government/throne_rooms/throne_room_north_german.dds"),
        # Procedural heraldry is intentionally absent from this sample.
        (r"GetCountryCoatOfArms\(Country.Self\)", {"__type__": "CoatOfArmsWrapper",
            "GetTexture('(int32)72','(int32)48')": None}),
        (r"InternationalOrganizationsView\.ShouldShowRulingHistory", False),
        (r"IsLateralViewOpened\('(?:foreign_country|government)'\)", False),
        (r"InternationalOrganization\.GetPayments", []),
        (r"InternationalOrganizationsView\.GetSpecialMembersSortSearch", {"__type__": "FilteredSortedList", "GetSortKeys": [], "ToggleAllEnabled": False}),
        (r"FilteredSortedList\.GetSearchBar", {"__type__": "SearchBar"}),
        (r"SearchBar\.(?:GetAutocompleteEntries|GetCustomEnabledFilters|GetEnabledFilters)", []),
        (r"SearchBar\.(?:HasSearchFilterCategories|HasVisibleEnabledSearchFilters)", False),
        (r"SearchBar\.(?:IsTextFilterEmpty|Manager.IsLeftPanel)", True),
        (r"ShouldShowRulingHistoryForInternationalOrganization\(InternationalOrganizationsView.GetInternationalOrganization.Self\)", False),
    ])
    for accessor, context in state.objects.items():
        variable, getter = accessor.split('.', 1)
        prefix = f"InternationalOrganizationsView.GetPlayer.MakeScope.GetVariable('{variable}').{getter}"
        result.extend(object_mocks(prefix, context))
    for name in ("tv_wonder_priority_unfinished_list", "tv_wonder_priority_expansion_list"):
        result.append((_exact(f"InternationalOrganizationsView.GetPlayer.MakeScope.GetList('{name}')"), state.lists.get(name, [])))
    # Only these native requirement-table helpers are simulated. The line data
    # remains local to its own datamodel item, as in the installed GUI types.
    result.append((r"GetRequirementLineAux\([^)]*\)", {"__type__": "RequirementLineAux",
                   "GetAuxParentArrowSize('(float)3','(float)0','(float)10')": ("vec", 3, 10)}))
    # Mechanic 1's five condition-type ids from tv_wonder_index_effects.txt.
    # This fixture does not execute the game's global-variable-map initializer.
    if state.player_variables["tv_wonder_locked_mechanic_id"] == 1:
        for index in range(1, 6):
            for table, value in (("condition_type", index), ("weight", (15, 7.5, 0, 10, 5)[index - 1])):
                expression = (f"GetVariableFromGlobalVariableMap('tv_wonder_suitability_{table}',"
                              "MakeScopeFlag(Concatenate('tv_wonder_suitability_',Concatenate("
                              "ToString_int32(FixedPointToInt(InternationalOrganizationsView.GetPlayer.MakeScope."
                              f"GetVariable('tv_wonder_locked_mechanic_id').GetValue)),'_{index}')))).GetValue")
                result.append((_exact(expression), value))
    for variable, value in state.organization_variables.items():
        context = {"__type__": "MonthlySavedVariable", "Self": variable}
        result.append((_exact(f"InternationalOrganizationsView.GetInternationalOrganization.GetVariableSpec('{variable}')"), context))
        result.append((_exact(f"InternationalOrganizationsView.GetInternationalOrganization.GetVariableText('{variable}')"), f"{value}/100"))
    if loc is not None:
        for estate in ("nobles", "burghers", "clergy"):
            demand = state.player_variables[f"tv_wonder_{estate}_demand"]
            if demand is not None:
                expression = f"ShowScriptedEffectForScope('tv_wonder_accept_{estate}_demand_effect',InternationalOrganizationsView.GetPlayer.MakeScope.Self)"
                result.append((_exact(expression), loc.get(f"TV_ENGINEERING_SOLUTION_{estate.upper()}_{demand}") or ""))
        # Explicit display samples read from the id 3 level 1 source modifiers.
        # The game computes its own effect tooltips; this scenario does not.
        for variable in ("tv_wonder_locked_display_id", "tv_wonder_proposal"):
            for suffix, rows in [("_level_1", []), ("_local_level_1", [])]:
                expression = f"ShowModifierEffect(Concatenate('tv_wonder_display_',Concatenate(ToString_int32(FixedPointToInt(InternationalOrganizationsView.GetPlayer.MakeScope.GetVariable('{variable}').GetValue)),'{suffix}')))"
                result.append((_exact(expression), string_pair_list(rows)))
        from eu5_gui_renderer.paths import LANGUAGE
        english = LANGUAGE == "english"
        samples = {
            "ShowTriggerConditions('tv_wonder_site_rule_player_visible_locked_wonder_trigger',PlayerScope.Self)":
                [("(Sample) Site meets geographic requirements" if english else "【示例】地点满足地理条件", True)],
        }
        result.extend((_exact(expression), requirements_list(rows)) for expression, rows in samples.items())
    result.append((_exact("ShowScriptedEffectForScope('tv_wonder_ritual_apply_choice_effect',InternationalOrganizationsView.GetPlayer.MakeScope.Self)"),
                   ritual_effect_sample(state, loc) if loc is not None else ""))
    # The game renders pay_price itself, including its live country modifiers.
    # Offline previews do not execute prices or invent a treasury-dependent amount.
    from eu5_gui_renderer.paths import LANGUAGE
    result.append((_exact("ShowScriptedEffectForScope('tv_wonder_ritual_pay_effect',InternationalOrganizationsView.GetPlayer.MakeScope.Self)"),
                   '(Sample) Native ritual gold cost' if LANGUAGE == 'english' else '【示例】原生仪式金币费用'))
    result.append((_exact("GetVariableSystem.Exists('tv_wonder_ritual_details_open')"), False))
    result.append((_exact("GetVariableSystem.Exists('tv_wonder_construction_details_open')"), False))
    return result


def build(db, expander, width: int = 570, height: int = 1800, state: ScenarioState | None = None):
    """Select the ED instance and supply ED-specific action availability."""
    from eu5_gui_renderer.fixtures import set_action_availability
    from eu5_gui_renderer.gui import build_target
    from eu5_gui_renderer.paths import MOD
    gui_file = MOD / GUI_PATH
    if str(gui_file) not in db.roots:
        raise ValueError(f"Engineering Department GUI missing (use --mod-root): {gui_file}")
    element = build_target(db, expander, "organization_panel", gui_file)
    if state is not None:
        availability = {"tv_wonder_end_debate":
                        state.organization_variables["tv_wonder_domestic_support"] >= 100,
                        **state.action_availability}
        ritual_open = state.player_variables.get("tv_wonder_stage") == 4 and not state.player_variables.get("tv_wonder_ritual_in_progress") and not state.player_variables.get("tv_wonder_ritual_completed")
        for n in (1, 2, 3): availability.setdefault(f"tv_wonder_ritual_preview_{n}", ritual_open)
        availability.setdefault('tv_wonder_ritual_preview_plain', ritual_open and state.player_variables.get('tv_wonder_project_mode') != 3)
        availability.setdefault('tv_wonder_ritual_confirm', ritual_open and state.player_variables.get('tv_wonder_ritual_choice') in (1, 2, 3))
        availability.setdefault("tv_wonder_finish_construction", state.player_variables.get("tv_wonder_stage") == 3)
        set_action_availability(element, availability)
    return element


def configure(*, workspace: Path = WORKSPACE, renderer_root: Path | None = None,
              game_root: Path | None = None, output_root: Path | None = None,
              language: str = "simp_chinese", mod_root: Path | None = None) -> Path:
    workspace = workspace.resolve()
    renderer_root = (renderer_root or workspace / ".eu5-base/ai_gui_assessment/renderer").resolve()
    if not (renderer_root / "eu5_gui_renderer").is_dir():
        raise ValueError(f"Renderer package missing: {renderer_root}")
    sys.path.insert(0, str(renderer_root))
    from eu5_gui_renderer.config import configure_paths
    configure_paths(workspace=workspace, mod_root=mod_root or Path("src"),
                    game_root=game_root, language=language,
                    output_root=output_root or Path("ai_gui_assessment/images/engineering"))
    return renderer_root


def render(state: ScenarioState, *, width: int = 570, height: int = 1800,
           scale: float = 1, output: Path | None = None, resources=None,
           extra_mocks: list | None = None) -> dict:
    """Render after configure(); return the machine-readable diagnostics."""
    from eu5_gui_renderer.gui import Expander
    from eu5_gui_renderer.paths import MOD, OUTPUT
    from eu5_gui_renderer.preview import load_resources, render_tree
    resources = resources or load_resources()
    expander = Expander(resources.db)
    element = build(resources.db, expander, width, height, state)
    def walk(node):
        yield node
        for child in node.children:
            yield from walk(child)
    card = next((node for node in walk(element)
                 if node.typename == "tv_engineering_department_card_common"
                 and any(child.props.get("text") == "TV_WONDER_RITUAL_HEADER" for child in walk(node))), None)
    return render_tree(element, expander, resources, (extra_mocks or []) + mocks(state, resources.loc),
        width=width, height=height, scale=scale,
        output=output or OUTPUT / f"engineering_{state.name}.png",
        detail_elements={"ritual": card} if card is not None else None,
        metadata={
            "scenario": f"engineering-{state.tab}", "state": asdict(state), "sample_data": True,
            "gui": str(MOD / GUI_PATH), "unsupported": list(UNSUPPORTED),
            "sample_effect_text": ["ShowModifierEffect id 3 level 1 tables", "Three estate demand effect descriptions",
                                   "Site requirements are sample tables; ritual rewards come from current ritual_styles data, not script execution."],
            "sample_action_availability": "End debate requires support >= 100; explicit action_availability overrides apply; remaining actions are shown enabled without evaluating game triggers.",
        })


def load_fixture(state: ScenarioState, path: Path) -> ScenarioState:
    """Overlay fixture fields while preserving independent scope stores."""
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    mapping_fields = ("player_variables", "organization_variables", "global_variables", "objects", "lists", "action_availability")
    if not isinstance(payload, dict) or set(payload) - {*mapping_fields, "tab", "engineer_name"}:
        raise ValueError("Fixture must contain only tab, engineer_name, player_variables, organization_variables, global_variables, objects, lists, action_availability")
    changes = {}
    for key, value in payload.items():
        if key in mapping_fields:
            if not isinstance(value, dict):
                raise ValueError(f"Fixture {key} must be an object")
            for name, item in value.items():
                if key.endswith("_variables") and item is not None and not isinstance(item, (int, float, bool)):
                    raise ValueError(f"Fixture {key}.{name} must be numeric, boolean or null")
                if key == "action_availability" and not isinstance(item, bool):
                    raise ValueError(f"Fixture action_availability.{name} must be boolean")
                if key == "objects" and ("." not in name or not isinstance(item, dict) or "__type__" not in item):
                    raise ValueError(f"Fixture objects.{name} needs variable.accessor and a typed context")
                if key == "lists" and not isinstance(item, list):
                    raise ValueError(f"Fixture lists.{name} must be a list")
            changes[key] = {**getattr(state, key), **value}
        elif key == "tab" and value not in TABS:
            raise ValueError(f"Fixture tab must be one of {TABS}")
        elif key == "engineer_name" and not isinstance(value, str):
            raise ValueError("Fixture engineer_name must be a string")
        else:
            changes[key] = value
    return replace(state, **changes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--state", choices=STATE_NAMES, default="debate")
    selection.add_argument("--all", action="store_true", help="render every lifecycle preset with shared assets")
    parser.add_argument("--list-states", action="store_true")
    parser.add_argument("--tab", choices=TABS, help="override the preset's selected tab")
    parser.add_argument("--fixture", type=Path, help="JSON scope variables, objects, lists and action availability")
    parser.add_argument("--mocks", type=Path, help="JSON [expression regex, value] pairs; take precedence over samples")
    parser.add_argument("--strict", action="store_true", help="exit nonzero on unresolved bindings or assets")
    parser.add_argument("--workspace", type=Path, default=WORKSPACE)
    parser.add_argument("--renderer-root", type=Path)
    parser.add_argument("--mod-root", type=Path, help="deployable ED mod root, relative to workspace or absolute")
    parser.add_argument("--game-root", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--language", default="simp_chinese")
    parser.add_argument("--width", type=int, default=570)
    parser.add_argument("--height", type=int, default=1800)
    parser.add_argument("--scale", type=float, default=1)
    args = parser.parse_args(argv)
    if args.list_states:
        for name, tab in STATE_TABS.items():
            print(f"{name:24} {tab}")
        return 0
    if args.all and (args.output or args.fixture or args.tab):
        parser.error("--all cannot be combined with --output, --fixture or --tab")
    if args.width <= 0 or args.height <= 0 or args.scale <= 0:
        parser.error("width, height and scale must be positive")
    try:
        configure(workspace=args.workspace, renderer_root=args.renderer_root, mod_root=args.mod_root,
                  game_root=args.game_root, output_root=args.output_root, language=args.language)
        from eu5_gui_renderer.fixtures import load_mocks
        from eu5_gui_renderer.preview import has_diagnostics, load_resources, write_report
        states = [scenario_state(name) for name in (STATE_NAMES if args.all else (args.state,))]
        if args.fixture:
            states = [load_fixture(states[0], args.workspace / args.fixture)]
        if args.tab:
            states = [replace(states[0], tab=args.tab)]
        extra_mocks = load_mocks(args.workspace / args.mocks) if args.mocks else []
        resources = load_resources()
        reports = []
        for state in states:
            report = render(state, width=args.width, height=args.height, scale=args.scale,
                            output=args.output, resources=resources, extra_mocks=extra_mocks)
            reports.append(report)
            print(f"Rendered {report['output']} ({state.tab}); "
                  f"unknown={len(report['unknown_expressions'])}, "
                  f"contexts={len(report['unresolved_contexts'])}, "
                  f"textures={len(report['missing_textures'])}, "
                  f"textcontexts={len(report['unsupported_textcontexts'])}, "
                  f"localizations={len(report['missing_localizations'])}", flush=True)
        if args.all:
            from eu5_gui_renderer.paths import OUTPUT
            write_report(OUTPUT / "engineering_index.json", reports)
        return int(args.strict and any(has_diagnostics(report) for report in reports))
    except (ValueError, OSError, re.error) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
