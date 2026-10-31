import sys
from copy import deepcopy
from pathlib import Path
import re

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
WONDERS_FILE = REPO_ROOT / "data" / "wonders.yaml"
WONDER_DESIGN_NOTES_FILE = REPO_ROOT / "data" / "wonder_design_notes.yaml"
WONDER_FINAL_BUILDINGS_FILE = REPO_ROOT / "data" / "wonder_final_buildings.yaml"
WONDER_GENERIC_RITUALS_FILE = REPO_ROOT / "data" / "wonder_generic_rituals.yaml"
WONDER_BASE_MODIFIERS_FILE = REPO_ROOT / "data" / "wonder_base_modifiers.yaml"
WONDER_SITE_RULES_FILE = REPO_ROOT / "data" / "wonder_site_rules.yaml"
WONDER_MECHANICS_DATA_REL = (
    "data/wonder_final_buildings.yaml + data/wonder_generic_rituals.yaml + "
    "data/wonder_base_modifiers.yaml + data/wonder_site_rules.yaml"
)
UNIQUE_WONDERS_FILE = REPO_ROOT / "data" / "unique_wonders.yaml"
COST_REWARD_UNITS_FILE = REPO_ROOT / "data" / "cost_reward_units.yaml"
PULSE_REGISTRY_FILE = REPO_ROOT / "data" / "pulse_registry.yaml"
GENERIC_WONDER_IMAGE_PROMPTS_FILE = REPO_ROOT / "data" / "wonder_image_prompts.yaml"
MANUAL_TV_GAME_CONCEPTS_FILE = REPO_ROOT / "src" / "main_menu" / "common" / "game_concepts" / "tv_game_concepts.txt"
ALL_WONDER_MIN_ID = 1
ALL_WONDER_MAX_ID = 56
UNIQUE_WONDER_MIN_ID = 101
UNIQUE_WONDER_MAX_ID = 240
WONDER_MECHANICS_MIN_ID = ALL_WONDER_MIN_ID
WONDER_MECHANICS_MAX_ID = UNIQUE_WONDER_MAX_ID
PARTS = ["foundation", "body", "function", "decoration"]
FINAL_BUILDING_LEVEL_BY_TYPE_MAP = "tv_wonder_final_building_level_by_type"
FIXED_WONDER_STAGE_IMAGE_TASKS = [
    {"id": -1, "key": "stage_construction", "name": "tv_wonder_construction"},
    {"id": -2, "key": "stage_foundation", "name": "tv_wonder_foundation"},
    {"id": -3, "key": "stage_body", "name": "tv_wonder_body"},
    {"id": -4, "key": "stage_function", "name": "tv_wonder_function"},
    {"id": -5, "key": "stage_decoration", "name": "tv_wonder_decoration"},
    {"id": -6, "key": "stage_complete", "name": "tv_wonder_complete"},
]
GAME_CONCEPT_DECL_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\{$")
ROMAN_NUMERALS = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
}








SUPPORTED_SUITABILITY_KNOWLEDGE_ROW_TYPES = {"condition_bonus", "scaled_bonus"}
ENGINE_SCALED_FIXED_MODIFIER_MAX = 0.5
VALUE_MOVEMENT_MODIFIER_PREFIX = "monthly_towards_"
ENGINE_SCALED_FIXED_MODIFIERS = {
    "global_pop_assimilation_speed",
    "global_pop_conversion_speed",
    "local_manpower",
    "local_pop_assimilation_speed",
    "local_pop_conversion_speed",
    "local_sailors",
}
PREFERENCE_CONDITION_SCRIPT_TO_SUITABILITY_ID = {
    "topography = mountains": "topography_mountains",
    "topography = plateau": "topography_plateau",
    "topography = hills": "topography_hills",
    "vegetation = forest": "vegetation_forest",
    "vegetation = woods": "vegetation_woods",
    "OR = { vegetation = forest vegetation = woods }": "vegetation_forest_or_woods",
    "location_rank ?= location_rank:rural_settlement": "rank_rural",
    "location_rank ?= location_rank:city": "rank_city",
    "location_rank ?= location_rank:megalopolis": "rank_megalopolis",
    "any_neighbor_location = { tv_wonder_location_is_city_trigger = yes }": "neighbor_city",
    "any_neighbor_location = { tv_wonder_location_is_town_trigger = yes }": "neighbor_town",
    "has_building = building_type:monastery": "has_monastery",
    "has_building = building_type:cathedral": "has_cathedral",
    "dominant_religion = owner.religion": "dominant_religion_owner",
    "has_building = building_type:bridge_infrastructure": "has_bridge_infrastructure",
    "any_neighbor_location = { has_building = building_type:tv_wonder_bridge_opening }": "neighbor_bridge_opening",
    "OR = { has_river = yes is_adjacent_to_lake = yes is_port = yes }": "waterway_or_port",
    "is_port = yes": "is_port",
    "modifier:fort_level > 0": "fort_level",
    "OR = { location_rank ?= location_rank:city location_rank ?= location_rank:megalopolis }": "urban_rank",
    "is_capital = yes": "is_capital",
    "OR = { raw_material = goods:goods_gold raw_material = goods:silver raw_material = goods:copper }": "raw_coin_metal",
    "has_building = building_type:armory": "has_armory",
}
PREFERENCE_SCALE_SOURCE_PATH_TO_SUITABILITY_ID = {
    "development": "development",
    "total_building_levels": "total_building_levels",
    "modifier:harbor_suitability": "harbor_suitability",
    "modifier:free_building_levels": "free_building_levels",
    "average_location_literacy": "average_location_literacy",
}
PREFERENCE_SET_RE = re.compile(
    r"^set_variable = \{ name = tv_wonder_site_preference_bonus value = var:tv_wonder_survey_site\.([A-Za-z0-9_:]+) \}$"
)
PREFERENCE_CLAMP_RE = re.compile(
    r"^clamp_variable = \{ name = tv_wonder_site_preference_bonus min = ([^ ]+) max = ([^ ]+) \}$"
)
PREFERENCE_MULTIPLY_RE = re.compile(
    r"^change_variable = \{ name = tv_wonder_site_preference_bonus multiply = ([^ ]+) \}$"
)
PREFERENCE_RULE_RE = re.compile(
    r"^(if|else_if) = \{ limit = \{ var:tv_wonder_survey_site \?= \{ (.+?) \} \} tv_wonder_change_all_survey_competence_target_effect = \{ value = (.+?) \} \}$"
)
PREFERENCE_REMOVE_TEMP = "remove_variable = tv_wonder_site_preference_bonus"
PREFERENCE_APPLY_TEMP = (
    "tv_wonder_change_all_survey_competence_target_effect = { value = var:tv_wonder_site_preference_bonus }"
)
WONDER_SIZE_IDS = {
    "small": 1,
    "medium": 2,
    "large": 3,
}
ONE_SHOT_REWARD_EFFECTS = {
    "adm": {"effect": "add_adm", "scope": "ruler_scalar"},
    "all_estate_satisfaction": {"effect": "add_all_estate_satisfaction", "scope": "country_value_block"},
    "army_tradition": {"effect": "add_army_tradition", "scope": "country_scalar"},
    "artist_skill": {"effect": "add_artist_skill", "scope": "artist_scalar"},
    "burghers_satisfaction": {
        "effect": "add_estate_satisfaction",
        "scope": "estate_satisfaction",
        "estate": "estate_type:burghers_estate",
    },
    "celestial_authority": {"effect": "change_celestial_authority", "scope": "country_value_block"},
    "clergy_satisfaction": {
        "effect": "add_estate_satisfaction",
        "scope": "estate_satisfaction",
        "estate": "estate_type:clergy_estate",
    },
    "cultural_influence": {"effect": "add_cultural_influence", "scope": "culture_scalar"},
    "cultural_tradition": {"effect": "add_cultural_tradition", "scope": "culture_scalar"},
    "development": {"effect": "change_development", "scope": "location_scalar"},
    "dip": {"effect": "add_dip", "scope": "ruler_scalar"},
    "devotion": {"effect": "add_devotion", "scope": "country_scalar"},
    "diplomats": {"effect": "add_diplomats", "scope": "country_scalar"},
    "doom": {"effect": "add_doom", "scope": "country_scalar"},
    "gold": {"effect": "add_gold", "scope": "country_scalar"},
    "government_power": {"effect": "add_government_power", "scope": "country_scalar"},
    "harmony": {"effect": "add_harmony", "scope": "country_scalar"},
    "honor": {"effect": "add_honor", "scope": "country_scalar"},
    "horde_unity": {"effect": "add_horde_unity", "scope": "country_scalar"},
    "imperial_authority": {"effect": "change_imperial_authority", "scope": "country_value_block"},
    "inflation": {"effect": "add_inflation", "scope": "country_scalar"},
    "karma": {"effect": "add_karma", "scope": "country_scalar"},
    "laborers": {"effect": "add_pop", "scope": "location_laborers"},
    "legitimacy": {"effect": "add_legitimacy", "scope": "country_scalar"},
    "manpower": {"effect": "add_manpower", "scope": "country_scalar"},
    "mil": {"effect": "add_mil", "scope": "ruler_scalar"},
    "navy_tradition": {"effect": "add_navy_tradition", "scope": "country_scalar"},
    "nobles_satisfaction": {
        "effect": "add_estate_satisfaction",
        "scope": "estate_satisfaction",
        "estate": "estate_type:nobles_estate",
    },
    "prestige": {"effect": "add_prestige", "scope": "country_scalar"},
    "prosperity": {"effect": "change_prosperity", "scope": "location_scalar"},
    "purity": {"effect": "add_purity", "scope": "country_scalar"},
    "papal_authority": {"effect": "change_papal_authority", "scope": "country_value_block"},
    "peasants_satisfaction": {
        "effect": "add_estate_satisfaction",
        "scope": "estate_satisfaction",
        "estate": "estate_type:peasants_estate",
    },
    "religious_influence": {"effect": "add_religious_influence", "scope": "country_scalar"},
    "republican_tradition": {"effect": "add_republican_tradition", "scope": "country_scalar"},
    "research_progress": {"effect": "add_research_progress", "scope": "country_raw"},
    "righteousness": {"effect": "add_righteousness", "scope": "country_scalar"},
    "ruler_adm": {"effect": "add_adm", "scope": "ruler_scalar"},
    "ruler_dip": {"effect": "add_dip", "scope": "ruler_scalar"},
    "ruler_mil": {"effect": "add_mil", "scope": "ruler_scalar"},
    "sailors": {"effect": "add_sailors", "scope": "country_scalar"},
    "scaled_gold": {"effect": "change_gold_effect", "scope": "country_scale_block"},
    "self_control": {"effect": "add_self_control", "scope": "country_scalar"},
    "site_control": {"effect": "change_control", "scope": "location_scalar"},
    "site_development": {"effect": "change_development", "scope": "location_scalar"},
    "site_prosperity": {"effect": "change_prosperity", "scope": "location_scalar"},
    "site_raw_material_workers": {"effect": "change_max_raw_material_workers", "scope": "location_scalar"},
    "stability": {"effect": "add_stability", "scope": "country_scalar"},
    "tribal_cohesion": {"effect": "add_tribal_cohesion", "scope": "country_scalar"},
    "war_exhaustion": {"effect": "add_war_exhaustion", "scope": "country_scalar"},
    "yearly_gold": {"effect": "add_yearly_gold", "scope": "country_scalar"},
    "yearly_manpower": {"effect": "add_yearly_manpower", "scope": "country_scalar"},
    "yearly_sailors": {"effect": "add_yearly_sailors", "scope": "country_scalar"},
}
# The Unique Wonder Ceremony's per-stage cost is drawn from the standalone
# data/cost_reward_units.yaml catalog (country_reward/local_reward/character_reward/
# country_modifier/local_modifier), converting each catalog "reward" entry into a cost
# (negated, except country_reward.inflation which is inverted-polarity by design). A small
# number of catalog entries are excluded because they have no meaningful reading as a
# ceremony cost: the two boolean unlock switches (a flat unlock has no "5-year malus"
# reading), the monthly_towards_axis representative placeholder (not itself a real
# static-modifier field name), and local_reward.laborers (additive reward semantics do not
# translate safely into a negative site-labor cost). See docs/knowledge/risk_cards/wonders.md
# rule 20 for the full rationale.
COST_REWARD_CATALOGS = (
    "country_reward",
    "local_reward",
    "character_reward",
    "country_modifier",
    "local_modifier",
)
COST_REWARD_EXCLUDED_IDS = {
    ("country_modifier", "allow_open_sea_exploration"),
    ("country_modifier", "gender_equality"),
    ("country_modifier", "monthly_towards_axis"),
    ("local_reward", "laborers"),
}
_COST_REWARD_UNIT_ENTRIES_CACHE: dict[str, list[dict[str, object]]] | None = None
_COST_REWARD_UNITS_CACHE: dict[str, dict[str, float]] | None = None


def reset_cost_reward_unit_caches() -> None:
    """Forget the process-local cost/reward catalog after its source changes."""
    global _COST_REWARD_UNIT_ENTRIES_CACHE, _COST_REWARD_UNITS_CACHE
    _COST_REWARD_UNIT_ENTRIES_CACHE = None
    _COST_REWARD_UNITS_CACHE = None


def load_cost_reward_unit_entries() -> dict[str, list[dict[str, object]]]:
    """Load the complete data/cost_reward_units.yaml catalog, preserving every
    authored entry. Ceremony-cost helpers apply their own filtering on top."""
    global _COST_REWARD_UNIT_ENTRIES_CACHE
    if _COST_REWARD_UNIT_ENTRIES_CACHE is None:
        data = load_yaml(COST_REWARD_UNITS_FILE)
        catalogs: dict[str, list[dict[str, object]]] = {}
        for catalog in COST_REWARD_CATALOGS:
            raw_entries = data.get(catalog, [])
            if not isinstance(raw_entries, list):
                raise TypeError(f"{COST_REWARD_UNITS_FILE}.{catalog} must be a list")
            entries: list[dict[str, object]] = []
            for index, raw_entry in enumerate(raw_entries, start=1):
                if not isinstance(raw_entry, dict):
                    raise TypeError(f"{COST_REWARD_UNITS_FILE}.{catalog}[{index}] must be an object")
                entry_id = str(raw_entry.get("id", "")).strip()
                if not entry_id:
                    raise ValueError(f"{COST_REWARD_UNITS_FILE}.{catalog}[{index}] is missing id")
                entries.append(dict(raw_entry))
            catalogs[catalog] = entries
        _COST_REWARD_UNIT_ENTRIES_CACHE = catalogs
    return _COST_REWARD_UNIT_ENTRIES_CACHE


def load_cost_reward_units() -> dict[str, dict[str, float]]:
    """Load data/cost_reward_units.yaml, filtered to the ceremony-cost-usable
    {catalog: {id: base_value}} map. Cached after the first call."""
    global _COST_REWARD_UNITS_CACHE
    if _COST_REWARD_UNITS_CACHE is None:
        _COST_REWARD_UNITS_CACHE = build_cost_reward_unit_catalogs(
            {catalog: list(entries) for catalog, entries in load_cost_reward_unit_entries().items()}
        )
    return _COST_REWARD_UNITS_CACHE


def build_cost_reward_unit_catalogs(data: dict[str, object]) -> dict[str, dict[str, float]]:
    """Build the ceremony-cost lookup from an already validated candidate document."""
    catalogs: dict[str, dict[str, float]] = {}
    for catalog in COST_REWARD_CATALOGS:
        raw_entries = data.get(catalog, [])
        if not isinstance(raw_entries, list):
            raise TypeError(f"{COST_REWARD_UNITS_FILE}.{catalog} must be a list")
        usable: dict[str, float] = {}
        for entry in raw_entries:
            if not isinstance(entry, dict):
                raise TypeError(f"{COST_REWARD_UNITS_FILE}.{catalog} entries must be objects")
            entry_id = str(entry.get("id", "")).strip()
            if not entry_id or (catalog, entry_id) in COST_REWARD_EXCLUDED_IDS:
                continue
            value = entry.get("value")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            usable[entry_id] = value
        catalogs[catalog] = usable
    return catalogs


SITE_RULES_SECTION = "site_rules"


class WonderYamlDumper(yaml.SafeDumper):
    pass


_StrictWonderYamlBaseLoader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


class StrictWonderYamlLoader(_StrictWonderYamlBaseLoader):
    pass


def _represent_yaml_string(dumper: yaml.SafeDumper, value: str) -> yaml.ScalarNode:
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


WonderYamlDumper.add_representer(str, _represent_yaml_string)


def _construct_yaml_mapping_no_duplicates(
    loader: StrictWonderYamlLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict:
    mapping: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            source_name = getattr(loader, "source_name", "<yaml>")
            raise ValueError(f"Duplicate key {key!r} in {source_name}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


StrictWonderYamlLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_yaml_mapping_no_duplicates,
)


def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML source file: {path}")
    loader = StrictWonderYamlLoader(path.read_text(encoding="utf-8"))
    loader.source_name = str(path)
    try:
        data = loader.get_single_data()
    finally:
        loader.dispose()
    if not isinstance(data, dict):
        raise TypeError(f"{path} must contain a top-level mapping")
    return data


def dump_yaml_document(payload: object) -> str:
    return yaml.dump(
        payload,
        Dumper=WonderYamlDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,
    )


def _expect_keys(mapping: dict, *, required: set[str], optional: set[str], context: str) -> None:
    missing = sorted(required - set(mapping))
    if missing:
        raise ValueError(f"Missing keys in {context}: {', '.join(missing)}")
    unexpected = sorted(set(mapping) - required - optional)
    if unexpected:
        raise ValueError(f"Unexpected keys in {context}: {', '.join(unexpected)}")


def _require_mapping(value: object, context: str) -> dict:
    if not isinstance(value, dict):
        raise TypeError(f"{context} must be a mapping, got {type(value).__name__}")
    return value


def _require_list(value: object, context: str) -> list:
    if not isinstance(value, list):
        raise TypeError(f"{context} must be a list, got {type(value).__name__}")
    return value


def _require_string(value: object, context: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{context} must be a string, got {type(value).__name__}")
    if not allow_empty and not value.strip():
        raise ValueError(f"{context} cannot be empty")
    return value


def _validate_wonder_size(value: object, context: str) -> str:
    size = _require_string(value, context)
    if size not in WONDER_SIZE_IDS:
        supported = ", ".join(WONDER_SIZE_IDS)
        raise ValueError(f"{context} must be one of: {supported}")
    return size


def _require_optional_string(value: object, context: str) -> str | None:
    if value is None:
        return None
    return _require_string(value, context, allow_empty=True)


def _require_int(
    value: object,
    context: str,
    *,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{context} must be an int, got {type(value).__name__}")
    if minimum is not None and value < minimum:
        raise ValueError(f"{context} must be >= {minimum}, got {value}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{context} must be <= {maximum}, got {value}")
    return value


def validate_base_instant_effects(value: object, *, mechanic_keys: set[str]) -> dict:
    """Validate sparse prototype packages using the existing one-shot vocabulary."""
    import math

    context = "base_instant_effects"
    result = deepcopy(_require_mapping(value, context))
    unknown = set(result) - mechanic_keys
    if unknown:
        raise ValueError(f"{context}: unknown prototypes: {sorted(unknown)}")
    for key, entries in result.items():
        for index, entry in enumerate(_require_list(entries, f"{context}.{key}")):
            ctx = f"{context}.{key}[{index}]"
            _expect_keys(_require_mapping(entry, ctx), required={"type", "value"}, optional=set(), context=ctx)
            if not isinstance(entry["type"], str) or entry["type"] not in ONE_SHOT_REWARD_EFFECTS:
                raise ValueError(f"{ctx}: unknown instant effect type {entry['type']!r}")
            amount = _numeric_modifier_value(entry["value"])
            if amount is None or not math.isfinite(amount):
                raise ValueError(f"{ctx}.value must be a finite number")
            entry["value"] = amount
    return result


def wonder_base_instant_effects(wonder: dict, mechanics: dict, levels: int = 1) -> list[dict]:
    """Return a fresh, scaled package; never scale command names or scope fields."""
    if type(levels) is not int or not 0 <= levels <= 6:
        raise ValueError("Instant base effect levels must be an integer from 0 through 6")
    if levels == 0:
        return []
    multiplier = wonder.get("base_effect_multiplier", 1) * levels
    return [
        {"type": entry["type"], "value": float(entry["value"]) * multiplier}
        for entry in mechanics.get("base_instant_effects", {}).get(mechanic_key(wonder), [])
    ]


def _require_number_text(value: object, context: str) -> str:
    if isinstance(value, bool):
        raise TypeError(f"{context} must be a number or numeric string, got bool")
    if isinstance(value, (int, float)):
        return str(value)
    return _require_string(value, context)


def _numeric_modifier_value(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _check_engine_scaled_fixed_modifier_value(key: str, value: object, context: str) -> None:
    if key not in ENGINE_SCALED_FIXED_MODIFIERS:
        return
    numeric_value = _numeric_modifier_value(value)
    if numeric_value is None or numeric_value <= ENGINE_SCALED_FIXED_MODIFIER_MAX:
        return
    raise ValueError(
        f"{context}.{key} = {value!r} exceeds {ENGINE_SCALED_FIXED_MODIFIER_MAX}. "
        "EU5 multiplies this fixed-value modifier by 1000 in game; use the small fixed value, "
        "or use the matching *_modifier percent modifier when a percentage is intended."
    )


def _check_scaled_engine_fixed_modifiers(mapping: dict[str, object], multiplier: int | float, context: str) -> None:
    for key, value in mapping.items():
        if key not in ENGINE_SCALED_FIXED_MODIFIERS:
            continue
        numeric_value = _numeric_modifier_value(value)
        if numeric_value is None:
            continue
        scaled_value = numeric_value * float(multiplier)
        if scaled_value <= ENGINE_SCALED_FIXED_MODIFIER_MAX:
            continue
        raise ValueError(
            f"{context}.{key} = {value!r} scales to {scaled_value:g} with multiplier {multiplier:g}, "
            f"exceeding {ENGINE_SCALED_FIXED_MODIFIER_MAX}. EU5 multiplies this fixed-value modifier "
            "by 1000 in game; reduce the authored fixed value or use the matching *_modifier percent modifier."
        )


def _require_bool(value: object, context: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{context} must be a bool, got {type(value).__name__}")
    return value


def _validate_localized_text_map(value: object, context: str) -> dict[str, str]:
    mapping = _require_mapping(value, context)
    _expect_keys(mapping, required={"en", "zh"}, optional=set(), context=context)
    return {
        "en": _require_string(mapping["en"], f"{context}.en", allow_empty=True),
        "zh": _require_string(mapping["zh"], f"{context}.zh", allow_empty=True),
    }


def _validate_script_text(value: object, context: str, *, allow_empty: bool = True) -> str:
    text = _require_string(value, context, allow_empty=allow_empty)
    return text.strip("\n")


def _normalize_multiline_script(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").strip()


def normalize_inline_script(text: str) -> str:
    return " ".join(_normalize_multiline_script(text).split())


def split_top_level_statements(script: str, *, context: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    balance = 0
    for raw_line in _normalize_multiline_script(script).splitlines():
        stripped = raw_line.rstrip()
        if not stripped and not current:
            continue
        current.append(stripped)
        balance += stripped.count("{") - stripped.count("}")
        if balance == 0 and current:
            statements.append("\n".join(current).strip())
            current = []
    if current:
        raise ValueError(f"Unbalanced script block in {context}: {script}")
    return statements


def _parse_scaled_suitability_row(statements: list[str], index: int) -> tuple[dict[str, str], int] | None:
    if index + 3 >= len(statements):
        return None
    set_match = PREFERENCE_SET_RE.match(statements[index])
    clamp_match = PREFERENCE_CLAMP_RE.match(statements[index + 1])
    multiply_match = PREFERENCE_MULTIPLY_RE.match(statements[index + 2])
    if not (
        set_match
        and clamp_match
        and multiply_match
        and statements[index + 3] == PREFERENCE_APPLY_TEMP
    ):
        return None

    source = PREFERENCE_SCALE_SOURCE_PATH_TO_SUITABILITY_ID.get(set_match.group(1))
    if source is None:
        raise ValueError(f"Unknown suitability scale source path: {set_match.group(1)}")

    next_index = index + 4
    if next_index < len(statements) and statements[next_index] == PREFERENCE_REMOVE_TEMP:
        next_index += 1
    return (
        {
            "type": "scaled_bonus",
            "source": source,
            "min": clamp_match.group(1),
            "max": clamp_match.group(2),
            "multiplier": multiply_match.group(1),
        },
        next_index,
    )


def derive_suitability_knowledge_from_preference_script(script: str, *, context: str) -> list[dict[str, str]]:
    condition_rows: list[dict[str, str]] = []
    scaled_rows: list[dict[str, str]] = []
    statements = [
        normalize_inline_script(statement)
        for statement in split_top_level_statements(script, context=context)
    ]
    index = 0
    while index < len(statements):
        statement = statements[index]
        match = PREFERENCE_RULE_RE.match(statement)
        if match:
            _branch, condition_script, value = match.groups()
            condition = PREFERENCE_CONDITION_SCRIPT_TO_SUITABILITY_ID.get(normalize_inline_script(condition_script))
            if condition is None:
                raise ValueError(f"Unknown suitability condition in {context}: {condition_script}")
            condition_rows.append(
                {
                    "type": "condition_bonus",
                    "condition": condition,
                    "value": _require_number_text(value, f"{context}.condition_bonus.value"),
                }
            )
            index += 1
            continue

        scaled = _parse_scaled_suitability_row(statements, index)
        if scaled is not None:
            row, index = scaled
            scaled_rows.append(row)
            continue

        if statement == PREFERENCE_REMOVE_TEMP:
            index += 1
            continue

        raise ValueError(f"Cannot derive suitability knowledge from {context}: {statement}")

    return _validate_suitability_knowledge_rows(
        [*condition_rows, *scaled_rows],
        f"{context}.derived_suitability_knowledge",
    )


def _validate_string_list(value: object, context: str) -> list[str]:
    items = _require_list(value, context)
    normalized: list[str] = []
    for index, item in enumerate(items, start=1):
        normalized_item = _require_string(item, f"{context}[{index}]")
        if normalized_item in normalized:
            raise ValueError(f"Duplicate value {normalized_item!r} in {context}")
        normalized.append(normalized_item)
    return normalized


CEREMONY_STAGE_COUNT = 8


def _validate_parts_section(value: object, context: str) -> list[dict[str, str]]:
    parts = _require_list(value, context)
    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(parts, start=1):
        entry_context = f"{context}[{index}]"
        part = _require_mapping(item, entry_context)
        _expect_keys(part, required={"key"}, optional=set(), context=entry_context)
        key = _require_string(part["key"], f"{entry_context}.key")
        if key not in PARTS:
            raise ValueError(f"Unknown part key in {entry_context}: {key}")
        if key in seen:
            raise ValueError(f"Duplicate part key in {context}: {key}")
        seen.add(key)
        normalized.append({"key": key})
    missing = [key for key in PARTS if key not in seen]
    if missing:
        raise ValueError(f"Missing part entries in {context}: {', '.join(missing)}")
    return normalized


def _validate_sizes_section(value: object, context: str) -> dict[str, dict[str, int]]:
    sizes = _require_mapping(value, context)
    _expect_keys(sizes, required={"small", "medium", "large"}, optional=set(), context=context)
    normalized: dict[str, dict[str, int]] = {}
    for size_key in ("small", "medium", "large"):
        entry_context = f"{context}.{size_key}"
        entry = _require_mapping(sizes[size_key], entry_context)
        _expect_keys(entry, required={"progress"}, optional=set(), context=entry_context)
        normalized[size_key] = {
            "progress": _require_int(entry["progress"], f"{entry_context}.progress", minimum=1),
        }
    return normalized


def _validate_generic_wonder_record(raw: object) -> dict:
    context = "data/wonders.yaml wonder entry"
    wonder = _require_mapping(raw, context)
    _expect_keys(
        wonder,
        required={
            "id",
            "key",
            "concept",
            "size",
            "category",
            "pop_type",
            "final_building",
            "is_unique",
            "base_key",
            "mechanic_key",
            "base_effect_multiplier",
        },
        optional=set(),
        context=context,
    )

    key = _require_string(wonder["key"], f"{context}.key")
    if _require_bool(wonder["is_unique"], f"{context}.is_unique"):
        raise ValueError(f"{context}.is_unique must be false for generic wonders")
    if _require_string(wonder["base_key"], f"{context}.base_key") != key:
        raise ValueError(f"{context}.base_key must equal {key}")
    if _require_string(wonder["mechanic_key"], f"{context}.mechanic_key") != key:
        raise ValueError(f"{context}.mechanic_key must equal {key}")
    if _require_int(wonder["base_effect_multiplier"], f"{context}.base_effect_multiplier", minimum=1) != 1:
        raise ValueError(f"{context}.base_effect_multiplier must be 1 for generic wonders")

    return {
        **wonder,
        "id": _require_int(wonder["id"], f"{context}.id", minimum=ALL_WONDER_MIN_ID, maximum=ALL_WONDER_MAX_ID),
        "key": key,
        "concept": _require_string(wonder["concept"], f"{context}.concept"),
        "size": _validate_wonder_size(wonder["size"], f"{context}.size"),
        "category": _require_string(wonder["category"], f"{context}.category"),
        "pop_type": _require_string(wonder["pop_type"], f"{context}.pop_type"),
        "final_building": _require_string(wonder["final_building"], f"{context}.final_building"),
        "is_unique": False,
        "base_key": key,
        "mechanic_key": key,
        "base_effect_multiplier": 1,
    }


def _validate_suitability_knowledge_rows(value: object, context: str) -> list[dict[str, str]]:
    rows = _require_list(value, context)
    if not rows:
        raise ValueError(f"{context} must define at least one player-visible suitability row")

    normalized: list[dict[str, str]] = []
    for index, raw_row in enumerate(rows, start=1):
        row_context = f"{context}[{index}]"
        row = _require_mapping(raw_row, row_context)
        row_type = _require_string(row.get("type"), f"{row_context}.type")
        if row_type not in SUPPORTED_SUITABILITY_KNOWLEDGE_ROW_TYPES:
            supported = ", ".join(sorted(SUPPORTED_SUITABILITY_KNOWLEDGE_ROW_TYPES))
            raise ValueError(f"{row_context}.type must be one of: {supported}")

        if row_type == "condition_bonus":
            _expect_keys(row, required={"type", "condition", "value"}, optional=set(), context=row_context)
            normalized.append(
                {
                    "type": row_type,
                    "condition": _require_string(row["condition"], f"{row_context}.condition"),
                    "value": _require_number_text(row["value"], f"{row_context}.value"),
                }
            )
            continue

        _expect_keys(
            row,
            required={"type", "source", "min", "max", "multiplier"},
            optional=set(),
            context=row_context,
        )
        normalized.append(
            {
                "type": row_type,
                "source": _require_string(row["source"], f"{row_context}.source"),
                "min": _require_number_text(row["min"], f"{row_context}.min"),
                "max": _require_number_text(row["max"], f"{row_context}.max"),
                "multiplier": _require_number_text(row["multiplier"], f"{row_context}.multiplier"),
            }
        )
    return normalized


def _validate_site_rules(raw: object, *, mechanic_keys: set[str]) -> dict[str, dict]:
    context = f"{WONDER_SITE_RULES_FILE}.site_rules"
    site_rules = _require_mapping(raw, context)
    missing = sorted(mechanic_keys - set(site_rules))
    if missing:
        raise ValueError(f"Missing site_rules entries for: {', '.join(missing)}")
    extra = sorted(set(site_rules) - mechanic_keys)
    if extra:
        raise ValueError(f"Unknown site_rules entries for: {', '.join(extra)}")

    normalized: dict[str, dict] = {}
    for key in sorted(mechanic_keys):
        entry_context = f"{context}.{key}"
        entry = _require_mapping(site_rules[key], entry_context)
        _expect_keys(
            entry,
            required={"trigger_script", "preference_script"},
            optional=set(),
            context=entry_context,
        )
        preference_script = _validate_script_text(
            entry["preference_script"],
            f"{entry_context}.preference_script",
            allow_empty=False,
        )
        derive_suitability_knowledge_from_preference_script(
            preference_script,
            context=f"{entry_context}.preference_script",
        )
        normalized[key] = {
            "trigger_script": _validate_script_text(entry["trigger_script"], f"{entry_context}.trigger_script", allow_empty=False),
            "preference_script": preference_script,
        }
    return normalized


def _validate_modifier_mapping(value: object, context: str) -> dict[str, object]:
    mapping = _require_mapping(value, context)
    normalized: dict[str, object] = {}
    for raw_key, raw_value in mapping.items():
        key = _require_string(raw_key, f"{context} modifier key")
        if raw_value is None or isinstance(raw_value, (dict, list)):
            raise TypeError(
                f"{context}.{key} must be a scalar modifier value; nested maps are not valid shared local effects"
            )
        _check_engine_scaled_fixed_modifier_value(key, raw_value, context)
        normalized[key] = raw_value
    return normalized


def _validate_string_mapping(value: object, context: str) -> dict[str, str]:
    mapping = _require_mapping(value, context)
    return {
        _require_string(raw_key, f"{context} key"): _require_string(raw_value, f"{context}.{raw_key}")
        for raw_key, raw_value in mapping.items()
    }


def _validate_modifier_by_key_mapping(value: object, context: str) -> dict[str, dict[str, object]]:
    mapping = _require_mapping(value, context)
    normalized: dict[str, dict[str, object]] = {}
    for raw_key, raw_modifiers in mapping.items():
        key = _require_string(raw_key, f"{context} key")
        normalized[key] = _validate_modifier_mapping(raw_modifiers, f"{context}.{key}")
    return normalized


def _validate_generic_rituals(value: object, context: str) -> dict[str, dict]:
    axes = load_yaml(REPO_ROOT / "data/wonder_societal_axes.yaml")["societal_axes"]
    modifier_catalog = (REPO_ROOT / ".eu5-base/reference_official_defines/docs/modifiers.log").read_text(encoding="utf-8-sig")
    modifier_scopes = {name: set(categories.split(", ")) for name, categories in re.findall(r"Tag: (\w+), Categories: ([^\r\n]+)", modifier_catalog)}
    # Some unit-category modifiers also propagate from country modifiers (for
    # example vanilla a_moving_city.army_movement_speed). Preserve that evidence.
    vanilla_country = (REPO_ROOT / ".eu5-base/reference_game_files/game/main_menu/common/static_modifiers/country.txt").read_text(encoding="utf-8-sig")
    country_fields = set(re.findall(r"(?m)^\t(\w+)\s*=", vanilla_country))
    estates = {"nobles_estate", "clergy_estate", "burghers_estate", "peasants_estate", "dhimmi_estate", "tribes_estate", "cossacks_estate"}
    wonders = {w["key"]: w for w in load_wonders_source_data()["wonders"]}
    result = deepcopy(_require_mapping(value, context))
    if set(result) != set(wonders):
        raise ValueError(f"{context}: must cover every generic mechanism exactly once")
    for key, entry in result.items():
        ctx = f"{context}.{key}"
        _expect_keys(entry, required={"estate_preferences", "rituals"}, optional=set(), context=ctx)
        rows = _require_list(entry["rituals"], ctx)
        if len(rows) != 3 or sorted(r["style"] for r in rows) != [1, 2, 3]:
            raise ValueError(f"{ctx}: requires styles 1, 2, 3 exactly once")
        directions, used_axes, local_styles = set(), set(), []
        for row in rows:
            _expect_keys(row, required={"style", "societal_value", "reward"}, optional=set(), context=ctx)
            _require_int(row["style"], ctx, minimum=1, maximum=3)
            sv = _require_mapping(row["societal_value"], ctx)
            _expect_keys(sv, required={"axis", "direction"}, optional=set(), context=ctx)
            axis, direction = sv["axis"], sv["direction"]
            if axis not in axes or direction not in (axes[axis]["left"], axes[axis]["right"]):
                raise ValueError(f"{ctx}: invalid societal direction {sv}")
            directions.add(direction); used_axes.add(axis)
            reward = _require_mapping(row["reward"], ctx)
            if not reward or set(reward) - {"country_modifier", "location_modifier", "one_shot"} or not any(reward.values()):
                raise ValueError(f"{ctx}: at least one nonempty reward carrier is required")
            for carrier in ("country_modifier", "location_modifier"):
                if carrier in reward:
                    _validate_modifier_mapping(reward[carrier], ctx)
                    required_scope = "Country" if carrier == "country_modifier" else "Location"
                    invalid = [name for name in reward[carrier] if required_scope not in modifier_scopes.get(name, set()) and not (required_scope == "Country" and name in country_fields)]
                    if invalid:
                        raise ValueError(f"{ctx}.{carrier}: invalid {required_scope} modifiers: {invalid}")
                    if any(k.startswith("monthly_towards_") for k in reward[carrier]):
                        raise ValueError(f"{ctx}: societal movement is derived from societal_value")
            for item in _require_list(reward.get("one_shot", []), ctx):
                _expect_keys(item, required={"type", "value"}, optional=set(), context=ctx)
                if item["type"] not in ONE_SHOT_REWARD_EFFECTS:
                    raise ValueError(f"{ctx}: unknown one-shot reward {item['type']}")
                _require_number_text(item["value"], ctx)
            if reward.get("location_modifier"): local_styles.append(row["style"])
        if len(directions) != 3 or len(used_axes) < 2:
            raise ValueError(f"{ctx}: three distinct directions across at least two axes required")
        prefs = _require_mapping(entry["estate_preferences"], ctx)
        derived = location_reward_estate(wonders[key]) if len(local_styles) == 1 else None
        if set(prefs) != estates - ({derived} if derived else set()):
            raise ValueError(f"{ctx}: explicit estate preferences must cover exactly the non-derived estates")
        if any(type(v) is not int and v != "random" or type(v) is int and v not in (1, 2, 3) for v in prefs.values()):
            raise ValueError(f"{ctx}: estate preference must be 1/2/3/random")
        if len(local_styles) > 1 and prefs[location_reward_estate(wonders[key])] not in local_styles:
            raise ValueError(f"{ctx}: sponsoring estate must favor a location reward")
    return result


def _validate_building_attributes(value: object, context: str) -> dict[str, dict[str, object]]:
    mapping = _require_mapping(value, context)
    normalized: dict[str, dict[str, object]] = {}
    for raw_building, raw_attrs in mapping.items():
        building = _require_string(raw_building, f"{context} building key")
        attrs = _require_mapping(raw_attrs, f"{context}.{building}")
        normalized_attrs: dict[str, object] = {}
        for raw_key, raw_value in attrs.items():
            key = _require_string(raw_key, f"{context}.{building} attribute key")
            if raw_value is None or isinstance(raw_value, (dict, list)):
                raise TypeError(f"{context}.{building}.{key} must be a scalar attribute value")
            normalized_attrs[key] = raw_value
        normalized[building] = normalized_attrs
    return normalized


def _validate_buildings_section(raw: object, *, mechanic_keys: set[str]) -> dict[str, dict]:
    context = f"{WONDER_FINAL_BUILDINGS_FILE}.buildings"
    buildings = _require_mapping(raw, context)
    missing = sorted(mechanic_keys - set(buildings))
    if missing:
        raise ValueError(f"Missing buildings entries for: {', '.join(missing)}")
    extra = sorted(set(buildings) - mechanic_keys)
    if extra:
        raise ValueError(f"Unknown buildings entries for: {', '.join(extra)}")

    normalized: dict[str, dict] = {}
    for key in buildings:
        entry_context = f"{context}.{key}"
        entry = _require_mapping(buildings[key], entry_context)
        _expect_keys(
            entry,
            required={"final_local"},
            optional={"final_attributes", "include_local_cultural_baseline"},
            context=entry_context,
        )
        normalized_entry = {
            "final_local": _validate_modifier_mapping(entry["final_local"], f"{entry_context}.final_local"),
            "include_local_cultural_baseline": _require_bool(
                entry.get("include_local_cultural_baseline", True),
                f"{entry_context}.include_local_cultural_baseline",
            ),
        }
        if "final_attributes" in entry:
            normalized_entry["final_attributes"] = _validate_building_attributes(
                entry["final_attributes"],
                f"{entry_context}.final_attributes",
            )
        normalized[key] = normalized_entry
    return normalized


def load_wonders_source_data(path: Path = WONDERS_FILE) -> dict:
    raw = load_yaml(path)
    _expect_keys(raw, required={"wonders"}, optional={"parts", "sizes"}, context=str(path))
    wonders_raw = _require_list(raw["wonders"], f"{path}.wonders")
    wonders: list[dict] = []
    wonder_ids: set[int] = set()
    wonder_keys: set[str] = set()
    for index, item in enumerate(wonders_raw, start=1):
        wonder = _validate_generic_wonder_record(item)
        if wonder["id"] in wonder_ids:
            raise ValueError(f"Duplicate wonder id in {path}: {wonder['id']}")
        if wonder["key"] in wonder_keys:
            raise ValueError(f"Duplicate wonder key in {path}: {wonder['key']}")
        wonder_ids.add(wonder["id"])
        wonder_keys.add(wonder["key"])
        wonders.append(wonder)
    normalized = {
        **raw,
        "wonders": wonders,
    }
    if "parts" in raw:
        normalized["parts"] = _validate_parts_section(raw["parts"], f"{path}.parts")
    if "sizes" in raw:
        normalized["sizes"] = _validate_sizes_section(raw["sizes"], f"{path}.sizes")
    return normalized


def load_mechanics_source_data() -> dict:
    wonders_data = load_wonders_source_data()
    mechanic_keys = {wonder["mechanic_key"] for wonder in wonders_data["wonders"]}

    design_notes_raw = load_yaml(WONDER_DESIGN_NOTES_FILE)
    _expect_keys(design_notes_raw, required={"designs"}, optional=set(), context=str(WONDER_DESIGN_NOTES_FILE))
    designs = _require_mapping(design_notes_raw["designs"], f"{WONDER_DESIGN_NOTES_FILE}.designs")

    site_rules_raw = load_yaml(WONDER_SITE_RULES_FILE)
    _expect_keys(site_rules_raw, required={"site_rules"}, optional=set(), context=str(WONDER_SITE_RULES_FILE))
    site_rules = _validate_site_rules(site_rules_raw["site_rules"], mechanic_keys=mechanic_keys)

    buildings_raw = load_yaml(WONDER_FINAL_BUILDINGS_FILE)
    _expect_keys(buildings_raw, required={"buildings"}, optional=set(), context=str(WONDER_FINAL_BUILDINGS_FILE))
    buildings = _validate_buildings_section(buildings_raw["buildings"], mechanic_keys=mechanic_keys)

    generic_rituals_raw = load_yaml(WONDER_GENERIC_RITUALS_FILE)
    _expect_keys(generic_rituals_raw, required={"generic_rituals"}, optional=set(), context=str(WONDER_GENERIC_RITUALS_FILE))
    generic_rituals = _validate_generic_rituals(
        generic_rituals_raw["generic_rituals"],
        f"{WONDER_GENERIC_RITUALS_FILE}.generic_rituals",
    )

    base_modifiers_raw = load_yaml(WONDER_BASE_MODIFIERS_FILE)
    _expect_keys(base_modifiers_raw, required={"base_modifiers", "base_instant_effects"}, optional=set(), context=str(WONDER_BASE_MODIFIERS_FILE))
    base_modifiers = _validate_modifier_by_key_mapping(
        base_modifiers_raw["base_modifiers"],
        f"{WONDER_BASE_MODIFIERS_FILE}.base_modifiers",
    )
    base_instant_effects = validate_base_instant_effects(
        base_modifiers_raw["base_instant_effects"], mechanic_keys=mechanic_keys,
    )
    rules = load_yaml(REPO_ROOT / "data/wonder_ritual_rules.yaml")
    _expect_keys(rules, required={"ritual_rules"}, optional=set(), context="wonder_ritual_rules")
    rule = rules["ritual_rules"]
    _expect_keys(rule, required={"duration_months", "cost", "societal_value", "memory_years", "estate_satisfaction"}, optional=set(), context="ritual_rules")
    for key in ("duration_months", "memory_years"):
        _require_int(rule[key], f"ritual_rules.{key}", minimum=1)
    for group, keys in (("cost", {"catalog", "type", "value"}), ("societal_value", {"monthly"}), ("estate_satisfaction", {"support", "oppose"})):
        _expect_keys(_require_mapping(rule[group], f"ritual_rules.{group}"), required=keys, optional=set(), context=f"ritual_rules.{group}")
    import math
    for amount in (rule["societal_value"]["monthly"], rule["estate_satisfaction"]["support"], rule["estate_satisfaction"]["oppose"]):
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not math.isfinite(amount):
            raise ValueError("ritual_rules magnitudes must be finite numbers")
    if rule["cost"]["catalog"] != "country_reward" or rule["cost"]["type"] != "scaled_gold":
        raise ValueError("ritual_rules.cost must use country_reward.scaled_gold")
    if set(rule["cost"]["value"]) != {"small", "medium", "large"}:
        raise ValueError("ritual_rules.cost.value must cover all three sizes")
    for amount in rule["cost"]["value"].values():
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount < 0:
            raise ValueError("ritual_rules costs must be non-negative numbers")
    return {
        "designs": designs,
        "site_rules": site_rules,
        "buildings": buildings,
        "generic_rituals": generic_rituals,
        "base_modifiers": base_modifiers,
        "base_instant_effects": base_instant_effects,
        "ritual_rules": rule,
        "societal_axes": load_yaml(REPO_ROOT / "data/wonder_societal_axes.yaml")["societal_axes"],
    }


def load_unique_wonders_source_data(path: Path = UNIQUE_WONDERS_FILE) -> dict:
    raw = load_yaml(path)
    _expect_keys(raw, required={"unique_wonders"}, optional=set(), context=str(path))
    wonders_raw = _require_list(raw["unique_wonders"], f"{path}.unique_wonders")
    wonder_ids: set[int] = set()
    wonder_keys: set[str] = set()
    vanilla_carrier_keys: set[str] = set()
    wonders: list[dict] = []
    for index, item in enumerate(wonders_raw, start=1):
        context = f"{path}.unique_wonders[{index}]"
        wonder = _require_mapping(item, context)
        _expect_keys(
            wonder,
            required={
                "id",
                "key",
                "base_key",
                "concept",
                "location",
                "image",
                "prompt",
                "is_unique",
                "initial_level",
                "mechanic_key",
                "base_effect_multiplier",
                "final_building",
                "ritual_text",
            },
            optional={"native_canal", "vanilla_carriers", "vanilla_waivers", "identity_variants"},
            context=context,
        )

        wonder_id = _require_int(wonder["id"], f"{context}.id", minimum=UNIQUE_WONDER_MIN_ID, maximum=UNIQUE_WONDER_MAX_ID)
        if wonder_id in wonder_ids:
            raise ValueError(f"Duplicate unique wonder id in {path}: {wonder_id}")
        wonder_ids.add(wonder_id)

        key = _require_string(wonder["key"], f"{context}.key")
        if key in wonder_keys:
            raise ValueError(f"Duplicate unique wonder key in {path}: {key}")
        wonder_keys.add(key)

        if not _require_bool(wonder["is_unique"], f"{context}.is_unique"):
            raise ValueError(f"{context}.is_unique must be true for unique wonders")
        base_effect_multiplier = _require_int(
            wonder["base_effect_multiplier"],
            f"{context}.base_effect_multiplier",
            minimum=1,
        )
        if base_effect_multiplier != 2:
            raise ValueError(f"{context}.base_effect_multiplier must be 2 for unique wonders")
        initial_level = _require_int(
            wonder["initial_level"],
            f"{context}.initial_level",
            minimum=0,
            maximum=6,
        )
        if "native_canal" in wonder:
            _require_bool(wonder["native_canal"], f"{context}.native_canal")
        if "identity_variants" in wonder:
            validate_identity_variants(wonder["identity_variants"], f"{context}.identity_variants")

        own_carriers: set[str] = set()
        if "vanilla_carriers" in wonder:
            carriers = _require_list(wonder["vanilla_carriers"], f"{context}.vanilla_carriers")
            if not carriers:
                raise ValueError(f"{context}.vanilla_carriers must not be empty")
            for carrier in carriers:
                c = _require_mapping(carrier, f"{context}.vanilla_carriers[]")
                _expect_keys(c, required={"kind", "key", "mode"}, optional={"op", "present_at_level"}, context=context)
                carrier_key = _require_string(c["key"], f"{context}.vanilla_carriers.key")
                if carrier_key in vanilla_carrier_keys:
                    raise ValueError(f"Duplicate vanilla carrier key: {carrier_key}")
                vanilla_carrier_keys.add(carrier_key)
                own_carriers.add(carrier_key)
                if _require_string(c["kind"], f"{context}.vanilla_carriers.kind") not in {"art", "building", "effect", "modifier"}:
                    raise ValueError(f"{context}: invalid vanilla carrier kind {c['kind']!r}")
                if _require_string(c["mode"], f"{context}.vanilla_carriers.mode") not in {"replace", "augment"}:
                    raise ValueError(f"{context}: invalid vanilla carrier mode {c['mode']!r}")
                if c["mode"] == "replace" and "op" in c:
                    raise ValueError(f"{context}: replace carrier must not have op")
                if c["mode"] == "augment" and _require_string(c.get("op", ""), f"{context}.vanilla_carriers.op") not in {"raise", "lower", "damage", "restore"}:
                    raise ValueError(f"{context}: augment carrier requires a valid op")
                if "present_at_level" in c:
                    if c["kind"] not in {"art", "building"}:
                        raise ValueError(f"{context}: present_at_level is only valid for art/building")
                    _require_int(c["present_at_level"], f"{context}.present_at_level", minimum=1, maximum=6)
        if "vanilla_waivers" in wonder:
            for waiver in _require_list(wonder["vanilla_waivers"], f"{context}.vanilla_waivers"):
                w = _require_mapping(waiver, f"{context}.vanilla_waivers[]")
                _expect_keys(w, required={"site", "carrier", "reason"}, optional=set(), context=context)
                for field in ("site", "carrier", "reason"):
                    _require_string(w[field], f"{context}.vanilla_waivers.{field}")
                if w["carrier"] not in own_carriers:
                    raise ValueError(f"{context}: waiver carrier must be declared on this wonder")

        wonders.append(
            {
                **wonder,
                "id": wonder_id,
                "key": key,
                "base_key": _require_string(wonder["base_key"], f"{context}.base_key"),
                "concept": _require_string(wonder["concept"], f"{context}.concept"),
                "location": _require_string(wonder["location"], f"{context}.location"),
                "image": _require_string(wonder["image"], f"{context}.image"),
                "prompt": _require_string(wonder["prompt"], f"{context}.prompt"),
                "is_unique": True,
                "initial_level": initial_level,
                "mechanic_key": _require_string(wonder["mechanic_key"], f"{context}.mechanic_key"),
                "base_effect_multiplier": base_effect_multiplier,
                "final_building": _require_string(wonder["final_building"], f"{context}.final_building"),
                "ritual_text": _validate_ritual_text(wonder["ritual_text"], f"{context}.ritual_text"),
            }
        )
    return {
        "unique_wonders": wonders,
    }


def leading_comment_block(text: str) -> str:
    lines = text.splitlines()
    captured: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            captured.append(line.rstrip())
            continue
        break
    return "\n".join(captured).rstrip()


def save_yaml_document(path: Path, payload: object, *, preserve_leading_comments: bool = False) -> None:
    header = ""
    if preserve_leading_comments and path.exists():
        header = leading_comment_block(path.read_text(encoding="utf-8"))

    body = dump_yaml_document(payload).rstrip() + "\n"
    if header:
        path.write_text(f"{header}\n{body}", encoding="utf-8", newline="\n")
    else:
        path.write_text(body, encoding="utf-8", newline="\n")


def _load_wonder_image_prompt_section(path: Path, section: str) -> dict[str, str]:
    if not path.exists():
        return {}

    raw = load_yaml(path) or {}
    prompts = raw.get(section, {})
    if not isinstance(prompts, dict):
        raise ValueError(f"{section} must be a mapping")

    normalized: dict[str, str] = {}
    for key, prompt in prompts.items():
        normalized_key = str(key).strip()
        normalized_prompt = str(prompt).strip()
        if not normalized_key:
            raise ValueError("Wonder image prompt keys cannot be empty")
        if not normalized_prompt:
            raise ValueError(f"Wonder image prompt for {normalized_key} cannot be empty")
        normalized[normalized_key] = normalized_prompt
    return normalized


def load_generic_wonder_image_prompts(path: Path = GENERIC_WONDER_IMAGE_PROMPTS_FILE) -> dict[str, str]:
    return _load_wonder_image_prompt_section(path, "generic_wonder_image_prompts")


def load_fixed_wonder_stage_image_prompts(path: Path = GENERIC_WONDER_IMAGE_PROMPTS_FILE) -> dict[str, str]:
    prompts = _load_wonder_image_prompt_section(path, "fixed_wonder_stage_image_prompts")
    expected_keys = {task["key"] for task in FIXED_WONDER_STAGE_IMAGE_TASKS}

    missing_prompts = sorted(expected_keys - set(prompts))
    if missing_prompts:
        raise ValueError(
            "Missing fixed wonder stage image prompts for: "
            + ", ".join(missing_prompts)
        )

    extra_prompts = sorted(set(prompts) - expected_keys)
    if extra_prompts:
        raise ValueError(
            "Unknown fixed wonder stage image prompt keys: "
            + ", ".join(extra_prompts)
        )
    return prompts


def load_manual_game_concept_ids(path: Path = MANUAL_TV_GAME_CONCEPTS_FILE) -> set[str]:
    if not path.exists():
        return set()

    concept_ids: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        match = GAME_CONCEPT_DECL_RE.match(raw_line.strip())
        if match:
            concept_ids.add(match.group(1))
    return concept_ids


def mechanic_key(wonder: dict) -> str:
    return _require_string(wonder["mechanic_key"], f"{wonder['key']}.mechanic_key")


def wonder_ritual_composite_id(wonder_id: int, style: int) -> int:
    return int(wonder_id) * 100 + int(style)


def wonder_suitability_row_composite_id(mechanic_id: int, row: int) -> int:
    return int(mechanic_id) * 10 + int(row)


SUITABILITY_REVEAL_MAP = "tv_wonder_suitability_revealed"
SUITABILITY_ACTUAL_MAP = "tv_wonder_suitability_actual"
SUITABILITY_CURRENT_REVEALED_VARIABLE = "tv_wonder_suitability_current_revealed"


def suitability_current_revealed_variable() -> str:
    return SUITABILITY_CURRENT_REVEALED_VARIABLE


def suitability_current_actual_variable(row_index: int) -> str:
    return f"tv_wonder_suitability_current_actual_{int(row_index)}"


def ritual_style_ids(wonder: dict) -> list[int]:
    return [1, 2, 3]


def finalization_event_id(wonder: dict) -> int:
    return 5000 + int(wonder["id"])


def finalization_world_event_id(wonder: dict) -> int:
    return 6000 + int(wonder["id"])


def finalization_world_expansion_event_id(wonder: dict) -> int:
    return 6500 + int(wonder["id"])


def finalization_hidden_event_id() -> int:
    return 6999


def final_building_completion_sync_hidden_event_id() -> int:
    return 6998


def final_building_level_sync_hidden_event_id(wonder: dict) -> int:
    return 9400 + int(wonder["id"])


def ownership_gain_event_id(wonder: dict) -> int:
    return 8000 + int(wonder["id"])


def ownership_loss_event_id(wonder: dict) -> int:
    return 9000 + int(wonder["id"])


def finalization_visible_effect_name(wonder: dict) -> str:
    return f"tv_wonder_{wonder['key']}_finalization_visible_effect"


def final_building_level_changed_effect_name(wonder: dict) -> str:
    # Shared next-day resync after any final-building level change: native
    # demolition, external lowering, and external raising all land here.
    return f"tv_wonder_{wonder['key']}_handle_final_building_level_changed_effect"


# External level-change interface. The public wrappers in
# tv_wonder_level_change_effects.txt substitute the wonder key into these names,
# so the patterns below are the single source for both sides.
EXTERNAL_RAISE_GENERIC_LEVEL_PUBLIC_EFFECT = "tv_wonder_raise_generic_level_effect"
EXTERNAL_LOWER_GENERIC_LEVEL_PUBLIC_EFFECT = "tv_wonder_lower_generic_level_effect"
EXTERNAL_RAISE_UNIQUE_LEVEL_PUBLIC_EFFECT = "tv_wonder_raise_unique_level_effect"
EXTERNAL_LOWER_UNIQUE_LEVEL_PUBLIC_EFFECT = "tv_wonder_lower_unique_level_effect"
EXTERNAL_RAISE_GENERIC_LEVEL_EFFECT_PATTERN = "tv_wonder_{key}_raise_level_effect"
EXTERNAL_LOWER_GENERIC_LEVEL_EFFECT_PATTERN = "tv_wonder_{key}_lower_generic_level_effect"
EXTERNAL_RAISE_UNIQUE_LEVEL_EFFECT_PATTERN = "tv_wonder_{key}_raise_unique_level_effect"
EXTERNAL_LOWER_UNIQUE_LEVEL_EFFECT_PATTERN = "tv_wonder_{key}_lower_unique_level_effect"


def external_raise_generic_level_effect_name(wonder: dict) -> str:
    return f"tv_wonder_{wonder['key']}_raise_level_effect"


def external_lower_generic_level_effect_name(wonder: dict) -> str:
    return EXTERNAL_LOWER_GENERIC_LEVEL_EFFECT_PATTERN.format(key=wonder["key"])


def external_raise_unique_level_effect_name(wonder: dict) -> str:
    return EXTERNAL_RAISE_UNIQUE_LEVEL_EFFECT_PATTERN.format(key=wonder["key"])


def external_lower_unique_level_effect_name(wonder: dict) -> str:
    return EXTERNAL_LOWER_UNIQUE_LEVEL_EFFECT_PATTERN.format(key=wonder["key"])


def external_raise_existing_level_effect_name(wonder: dict) -> str:
    return f"tv_wonder_{wonder['key']}_raise_existing_final_building_level_effect"


def final_building_destruction_cmf_log_action_name() -> str:
    return "tv_engineering_department_cmf_log_destroyed"


def final_building_completion_cmf_log_action_name() -> str:
    return "tv_engineering_department_cmf_log_completed"


def final_building_cmf_log_arg2_name() -> str:
    return "tv_engineering_department_cmf_log_final_wonder_building"


def construct_final_building_effect_name(wonder: dict) -> str:
    return f"tv_wonder_{wonder['key']}_construct_final_building_effect"


def finalization_hidden_effect_name(wonder: dict) -> str:
    return f"tv_wonder_{wonder['key']}_finalization_hidden_effect"


def finalization_hidden_event_trigger_effect_name() -> str:
    return "tv_wonder_trigger_finalization_hidden_event_effect"


def finalization_hidden_event_execute_effect_name() -> str:
    return "tv_wonder_execute_finalization_hidden_event_effect"


def final_building_completion_sync_hidden_event_trigger_effect_name() -> str:
    return "tv_wonder_trigger_final_building_completion_sync_hidden_event_effect"


def final_building_completion_sync_hidden_event_execute_effect_name() -> str:
    return "tv_wonder_execute_final_building_completion_sync_hidden_event_effect"


def normalize_loc_map(value: object) -> dict[str, str]:
    return _validate_localized_text_map(value, "localized text")


def normalize_script_text(value: object) -> str:
    return _validate_script_text(value, "script text")


def normalize_string_list(value: object) -> list[str]:
    return _validate_string_list(value, "string list")


def indent_script_block(script: str | None, indent: int) -> list[str]:
    if not script:
        return []
    prefix = "\t" * indent
    lines: list[str] = []
    for raw_line in script.splitlines():
        if raw_line.strip():
            lines.append(f"{prefix}{raw_line.rstrip()}")
        else:
            lines.append("")
    return lines


def ritual_style(wonder: dict, mechanics: dict, style: int) -> dict:
    return next(row for row in ritual_styles(wonder, mechanics) if row["style"] == style)


def ritual_rules(mechanics: dict) -> dict:
    return mechanics["ritual_rules"]


def location_reward_estate(wonder: dict) -> str:
    return {"clergy": "clergy_estate", "nobles": "nobles_estate", "burghers": "burghers_estate", "laborers": "peasants_estate", "soldiers": "peasants_estate"}[wonder["pop_type"]]


def _validate_ritual_text(value: object, context: str) -> dict:
    text = _require_mapping(value, context)
    if set(text) != {1, 2, 3}: raise ValueError(f"{context}: all three styles required")
    for row in text.values():
        _expect_keys(row, required={"name_en", "name_zh", "desc_en", "desc_zh"}, optional=set(), context=context)
        for v in row.values(): _require_string(v, context)
    return text


def validate_identity_variants(value: object, context: str) -> None:
    variants = _require_list(value, context)
    if not variants:
        raise ValueError(f"{context} must not be empty")
    keys, states = set(), set()
    for variant in variants:
        v = _require_mapping(variant, context)
        _expect_keys(v, required={"key", "global_variable", "eligible_script", "restore_script",
                     "cost_scale", "reward_script", "name_en", "name_zh", "desc_en", "desc_zh",
                     "decision_en", "decision_zh", "decision_desc_en", "decision_desc_zh",
                     "image", "prompt", "ritual_text"}, optional={"vanilla_event"}, context=context)
        for field in set(v) - {"ritual_text", "cost_scale", "vanilla_event"}:
            _require_string(v[field], f"{context}.{field}")
        for field, seen in (("key", keys), ("global_variable", states)):
            if not re.fullmatch(r"[a-z][a-z0-9_]*", v[field]) or v[field] in seen:
                raise ValueError(f"{context}: invalid or duplicate {field}")
            seen.add(v[field])
        if not 0 < float(_require_number_text(v["cost_scale"], context)) < float('inf'):
            raise ValueError(f"{context}.cost_scale must be positive")
        for field in ("eligible_script", "restore_script", "reward_script"):
            _validate_script_text(v[field], f"{context}.{field}", allow_empty=False)
        _validate_ritual_text(v["ritual_text"], f"{context}.ritual_text")
        if "vanilla_event" in v:
            event = _require_mapping(v["vanilla_event"], context)
            _expect_keys(event, required={"path", "id", "option"}, optional=set(), context=context)
            for field in event:
                _require_string(event[field], f"{context}.vanilla_event.{field}")


def ritual_styles(wonder: dict, mechanics: dict) -> list[dict]:
    entry = mechanics["generic_rituals"][mechanic_key(wonder)]
    rules = ritual_rules(mechanics)
    local_styles = [r["style"] for r in entry["rituals"] if r["reward"].get("location_modifier")]
    prefs = deepcopy(entry["estate_preferences"])
    if len(local_styles) == 1: prefs[location_reward_estate(wonder)] = local_styles[0]
    result = []
    for row in sorted(entry["rituals"], key=lambda r: r["style"]):
        n, sv, reward = row["style"], row["societal_value"], row["reward"]
        sign = -1 if mechanics["societal_axes"][sv["axis"]]["left"] == sv["direction"] else 1
        country = deepcopy(reward.get("country_modifier", {}))
        country[f"monthly_towards_{sv['direction']}"] = rules["societal_value"]["monthly"]
        location = deepcopy(reward.get("location_modifier", {}))
        prefix = f"tv_wonder_{wonder['key']}_ritual_{n}"
        result.append({"style": n, "ritual_id": wonder["id"] * 100 + n,
            "modifier": prefix + "_modifier", "location_modifier": prefix + "_location_modifier" if location else None,
            "country_modifier": country, "location_modifier_values": location, "one_shot": deepcopy(reward.get("one_shot", [])),
            "societal_value": {**sv, "sign": sign, **rules["societal_value"]}, "estate_preferences": deepcopy(prefs),
            "name_key": f"game_concept_tv_wonder_display_{wonder['id']}_ritual_{n}",
            "desc_key": f"game_concept_tv_wonder_display_{wonder['id']}_ritual_{n}_desc",
            "final_desc_key": f"tv_engineering_department.500.d_{wonder['key']}_{n}"})
    return result


def load_wonder_data(
    min_id: int = ALL_WONDER_MIN_ID,
    max_id: int = ALL_WONDER_MAX_ID,
    *,
    require_designs: bool = True,
    require_buildings: bool = True,
    require_base_modifiers: bool = True,
) -> tuple[list[dict], dict]:
    wonders_data = load_wonders_source_data()
    mechanics = load_mechanics_source_data()
    wonders = [
        deepcopy(wonder)
        for wonder in wonders_data["wonders"]
        if min_id <= int(wonder["id"]) <= max_id
    ]
    for wonder in wonders:
        key = wonder["key"]
        if require_designs and key not in mechanics["designs"]:
            raise ValueError(f"Missing design data for {key}")
        if require_buildings and key not in mechanics["buildings"]:
            raise ValueError(f"Missing building data for {key}")
        if require_base_modifiers and key not in mechanics["base_modifiers"]:
            raise ValueError(f"Missing base modifier data for {key}")
    return wonders, mechanics


def _validate_generated_engine_scaled_fixed_modifiers(wonders: list[dict], mechanics: dict) -> None:
    for wonder in wonders:
        generated_level_6_multiplier = int(wonder.get("base_effect_multiplier", 1)) * 6
        mechanic = _require_string(wonder["mechanic_key"], f"{wonder['key']}.mechanic_key")

        base_modifiers = mechanics.get("base_modifiers", {}).get(mechanic, {})
        _check_scaled_engine_fixed_modifiers(
            base_modifiers,
            generated_level_6_multiplier,
            f"generated level-6 base modifiers for {wonder['key']} ({mechanic})",
        )

        final_local = mechanics.get("buildings", {}).get(mechanic, {}).get("final_local", {})
        _check_scaled_engine_fixed_modifiers(
            final_local,
            generated_level_6_multiplier,
            f"generated level-6 local display modifiers for {wonder['key']} ({mechanic})",
        )


def is_value_movement_modifier(modifier_key: str) -> bool:
    return modifier_key.startswith(VALUE_MOVEMENT_MODIFIER_PREFIX)


def _base_country_modifiers_for_rules(wonder: dict, mechanics: dict) -> dict[str, object]:
    mechanic = _require_string(wonder["mechanic_key"], f"{wonder['key']}.mechanic_key")
    return mechanics.get("base_modifiers", {}).get(mechanic, {})


def validate_wonder_size_base_country_modifier_rules(wonders: list[dict], mechanics: dict) -> None:
    for wonder in wonders:
        values = _base_country_modifiers_for_rules(wonder, mechanics)
        if any(is_value_movement_modifier(k) for k in values):
            raise ValueError(f"{wonder['key']}: base layer cannot contain societal movement")
        if wonder["size"] == "small" and values:
            raise ValueError(f"{wonder['key']}: small wonders cannot have national base effects")


def validate_unique_wonder_single_site_shape(wonder: dict) -> None:
    _require_string(wonder.get("location"), f"{wonder['key']}.location")
    _require_string(wonder.get("final_building"), f"{wonder['key']}.final_building")


def load_generic_wonder_mechanics_data() -> tuple[list[dict], dict]:
    wonders, mechanics = load_wonder_data(
        ALL_WONDER_MIN_ID,
        ALL_WONDER_MAX_ID,
        require_designs=False,
        require_buildings=True,
        require_base_modifiers=True,
    )
    generic_rituals = mechanics.get("generic_rituals", {})
    for wonder in wonders:
        if wonder["key"] not in generic_rituals:
            raise ValueError(f"Missing generic ritual data for {wonder['key']}")
    _validate_generated_engine_scaled_fixed_modifiers(wonders, mechanics)
    validate_wonder_size_base_country_modifier_rules(wonders, mechanics)
    return wonders, mechanics


def load_unique_wonders() -> list[dict]:
    wonders_data = load_wonders_source_data()
    mechanics = load_mechanics_source_data()
    unique_data = load_unique_wonders_source_data()
    base_by_key = {
        wonder["key"]: deepcopy(wonder)
        for wonder in wonders_data["wonders"]
    }
    unique_wonders: list[dict] = []
    for raw in unique_data["unique_wonders"]:
        base_key = raw["base_key"]
        if base_key not in base_by_key:
            raise ValueError(f"Unknown base wonder for unique wonder {raw['key']}: {base_key}")
        if base_key not in mechanics["buildings"]:
            raise ValueError(f"Missing building data for base wonder {base_key}")
        if base_key not in mechanics["base_modifiers"]:
            raise ValueError(f"Missing base modifier data for base wonder {base_key}")
        base = deepcopy(base_by_key[base_key])
        key = raw["key"]
        merged = {
            **base,
            **raw,
        }
        if merged["base_key"] != base_key:
            raise ValueError(f"Unique wonder {key} must keep base_key = {base_key}")
        if merged["mechanic_key"] != base_key:
            raise ValueError(f"Unique wonder {key} must keep mechanic_key = {base_key}")
        normalized = deepcopy(merged)
        validate_unique_wonder_single_site_shape(normalized)
        unique_wonders.append(normalized)
    return unique_wonders


def load_all_wonder_mechanics_data(*, include_unique: bool = True) -> tuple[list[dict], dict]:
    wonders, mechanics = load_generic_wonder_mechanics_data()
    if include_unique:
        wonders.extend(load_unique_wonders())
        _validate_generated_engine_scaled_fixed_modifiers(wonders, mechanics)
        validate_wonder_size_base_country_modifier_rules(wonders, mechanics)
    return wonders, mechanics


def load_generic_wonder_mechanics() -> tuple[list[dict], dict]:
    return load_generic_wonder_mechanics_data()


def load_all_wonder_mechanics(*, include_unique: bool = True) -> tuple[list[dict], dict]:
    return load_all_wonder_mechanics_data(include_unique=include_unique)


def legacy_site_trigger_lines(key: str, indent: int = 1) -> list[str]:
    raise RuntimeError("Legacy site trigger fallback has been removed; use data/wonder_site_rules.yaml")


def legacy_site_preference_lines(key: str, indent: int = 2) -> list[str]:
    raise RuntimeError("Legacy site preference fallback has been removed; use data/wonder_site_rules.yaml")


def site_rule_config(mechanics: dict, key: str) -> dict:
    site_rules = _require_mapping(mechanics.get(SITE_RULES_SECTION), f"{WONDER_SITE_RULES_FILE}.site_rules")
    if key not in site_rules:
        raise KeyError(f"Missing site_rules entry for {key}")
    entry = _require_mapping(site_rules[key], f"{WONDER_SITE_RULES_FILE}.site_rules.{key}")
    _expect_keys(
        entry,
        required={"trigger_script", "preference_script"},
        optional=set(),
        context=f"{WONDER_SITE_RULES_FILE}.site_rules.{key}",
    )
    return entry


def site_trigger_script_for_key(mechanics: dict, key: str) -> str:
    return _validate_script_text(
        site_rule_config(mechanics, key)["trigger_script"],
        f"{WONDER_SITE_RULES_FILE}.site_rules.{key}.trigger_script",
        allow_empty=False,
    )


def site_preference_script_for_key(mechanics: dict, key: str) -> str:
    return _validate_script_text(
        site_rule_config(mechanics, key)["preference_script"],
        f"{WONDER_SITE_RULES_FILE}.site_rules.{key}.preference_script",
        allow_empty=False,
    )


def suitability_knowledge_for_key(mechanics: dict, key: str) -> list[dict[str, str]]:
    return derive_suitability_knowledge_from_preference_script(
        site_preference_script_for_key(mechanics, key),
        context=f"{WONDER_SITE_RULES_FILE}.site_rules.{key}.preference_script",
    )


def suitability_knowledge_for_wonder(mechanics: dict, wonder: dict) -> list[dict[str, str]]:
    return suitability_knowledge_for_key(mechanics, mechanic_key(wonder))


def site_trigger_lines_for_wonder(mechanics: dict, wonder: dict, indent: int = 1) -> list[str]:
    return indent_script_block(site_trigger_script_for_key(mechanics, mechanic_key(wonder)), indent)


def site_preference_lines_for_wonder(mechanics: dict, wonder: dict, indent: int = 2) -> list[str]:
    return indent_script_block(site_preference_script_for_key(mechanics, mechanic_key(wonder)), indent)


def render_header(script_rel: str, data_rel: str = f"data/wonders.yaml + {WONDER_MECHANICS_DATA_REL} + data/unique_wonders.yaml") -> list[str]:
    return [
        f"# @Generated by {script_rel}",
        f"#   Data:    {data_rel}",
        f"#   Regen:   conda run --no-capture-output -n eu5 python {script_rel}",
        "# Do not edit directly - modify the data file and re-run the generator.",
        "",
    ]


def monthly_country_pulse_event_delay_days() -> int:
    registry = yaml.safe_load(PULSE_REGISTRY_FILE.read_text(encoding="utf-8")) or {}
    return int(registry.get("settings", {}).get("monthly_country_pulse_event_delay_days", 1))


def monthly_country_pulse_event(event_id: str) -> str:
    delay = monthly_country_pulse_event_delay_days()
    return f"trigger_event_non_silently = {{ id = {event_id} days = {delay} }}"


def upper_key(key: str) -> str:
    return key.upper()


def q(text: str) -> str:
    return (
        text.replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )


def all_final_buildings(wonders: list[dict]) -> list[str]:
    return [w["final_building"] for w in wonders]


def loc_line(key: str, value: str) -> str:
    return f' {key}:0 "{q(value)}"'


def level_static_modifier_loc(concept: str, level: int) -> str:
    numeral = ROMAN_NUMERALS.get(level)
    if numeral is None:
        raise ValueError(f"Unsupported wonder level for localization: {level}")
    return f"[{concept}|E] {numeral}"


def final_building(wonder: dict) -> str:
    return wonder["final_building"]


def wonder_image_name(wonder: dict) -> str:
    return str(wonder.get("image") or f"tv_wonder_{wonder['key']}")


def wonder_image_prompt(wonder: dict, generic_prompts: dict[str, str] | None = None) -> str:
    prompt = str(wonder.get("prompt") or "").strip()
    if prompt:
        return prompt

    prompts = generic_prompts or {}
    if wonder.get("is_unique"):
        raise ValueError(f"Unique wonder {wonder['key']} is missing an image prompt")

    prompt = str(prompts.get(wonder["key"]) or "").strip()
    if not prompt:
        raise ValueError(f"Generic wonder {wonder['key']} is missing an image prompt")
    return prompt


def load_wonder_image_tasks(*, include_unique: bool = True) -> list[dict]:
    wonders, _ = load_all_wonder_mechanics_data(include_unique=include_unique)
    stage_prompts = load_fixed_wonder_stage_image_prompts()
    generic_prompts = load_generic_wonder_image_prompts()
    generic_keys = {wonder["key"] for wonder in wonders if not wonder.get("is_unique")}

    missing_generic_prompts = sorted(key for key in generic_keys if key not in generic_prompts)
    if missing_generic_prompts:
        raise ValueError(
            "Missing generic wonder image prompts for: "
            + ", ".join(missing_generic_prompts)
        )

    extra_generic_prompts = sorted(key for key in generic_prompts if key not in generic_keys)
    if extra_generic_prompts:
        raise ValueError(
            "Unknown generic wonder image prompt keys: "
            + ", ".join(extra_generic_prompts)
        )

    tasks: list[dict] = [
        {
            "id": int(task["id"]),
            "key": str(task["key"]),
            "name": str(task["name"]),
            "prompt": stage_prompts[str(task["key"])],
            "is_unique": False,
            "is_stage": True,
        }
        for task in FIXED_WONDER_STAGE_IMAGE_TASKS
    ]
    for wonder in wonders:
        tasks.append(
            {
                "id": int(wonder["id"]),
                "key": wonder["key"],
                "name": wonder_image_name(wonder),
                "prompt": wonder_image_prompt(wonder, generic_prompts),
                "is_unique": bool(wonder.get("is_unique")),
                "is_stage": False,
            }
        )
        for variant in wonder.get("identity_variants", []):
            tasks.append({"id": int(wonder["id"]), "key": f"{wonder['key']}_{variant['key']}",
                          "name": variant["image"], "prompt": variant["prompt"],
                          "is_unique": True, "is_stage": False})
    return tasks


def wonder_maintenance_method(wonder: dict, stage: str) -> str:
    """Select upkeep by lifecycle stage and the wonder's own resolved size."""
    if stage not in {"module", "shell", "final"}:
        raise ValueError(f"Unknown wonder maintenance stage: {stage}")
    size = _validate_wonder_size(wonder["size"], "wonder maintenance size")
    return f"tv_wonder_{stage}_{size}_maintenance"


def scale_numeric_modifier_mapping(mapping: dict[str, object], multiplier: int | float) -> dict[str, object]:
    if multiplier == 1:
        return dict(mapping)
    scaled: dict[str, object] = {}
    for key, value in mapping.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            scaled[key] = value * multiplier
        else:
            scaled[key] = value
    return scaled


def merge_numeric_modifier_mappings(*maps: dict[str, object] | None) -> dict[str, object]:
    merged: dict[str, object] = {}
    for mapping in maps:
        if not mapping:
            continue
        for key, value in mapping.items():
            if (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and isinstance(merged.get(key), (int, float))
                and not isinstance(merged.get(key), bool)
            ):
                merged[key] = merged[key] + value
            else:
                merged[key] = value
    return merged


def wonder_base_country_modifiers(wonder: dict, mechanics: dict, level: int = 1) -> dict[str, object]:
    base = mechanics["base_modifiers"].get(mechanic_key(wonder), {})
    multiplier = wonder.get("base_effect_multiplier", 1) * level
    return scale_numeric_modifier_mapping(base, multiplier)


def authored_final_building_local_modifiers(wonder: dict, mechanics: dict) -> dict[str, object]:
    building_design = mechanics["buildings"][mechanic_key(wonder)]
    modifiers = building_design.get("final_local", {})
    return scale_numeric_modifier_mapping(modifiers, wonder.get("base_effect_multiplier", 1))


def wonder_static_display_modifier_name(wonder: dict, level: int) -> str:
    return f"tv_wonder_display_{wonder['id']}_level_{level}"


def wonder_static_local_display_modifier_name(wonder: dict, level: int) -> str:
    return f"tv_wonder_display_{wonder['id']}_local_level_{level}"


TV_WONDER_AUTO_LEVEL_BY_WONDER_ID_MAP = "tv_wonder_auto_level_by_wonder_id"


def wonder_auto_modifier_name(wonder: dict) -> str:
    return f"tv_wonder_auto_{wonder['key']}"


def wonder_auto_unscaled_modifier_name(wonder: dict) -> str:
    return f"{wonder_auto_modifier_name(wonder)}_unscaled"


def generic_ritual_for_wonder(mechanics: dict, wonder: dict) -> dict:
    return mechanics["generic_rituals"][mechanic_key(wonder)]
