"""Build Wonder field specifications from explicit source data and catalogs."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from scripts_engineering_department.wonder_mechanics.modifiers import authored_final_building_local_modifiers
from scripts_engineering_department.wonder_mechanics.naming import final_building, mechanic_key
from scripts_engineering_department.wonder_mechanics.schema import (
    site_preference_script_for_key,
    site_trigger_script_for_key,
)

from . import sources
from .field_types import FieldSpec, MechanicsFieldSpec
from .localization import LANGUAGES, branch_button_key, concept_key_for_wonder, localization_value, wonder_name_key
from .site_rules import parse_preference_builder_state, parse_trigger_builder_state
from .sources import get_unique_wonder_source
from .values import WONDER_SIZE_OPTIONS, build_modifier_editor_state, build_reward_editor_state, parse_unique_initial_level, reward_rows_from_list, scale_numeric_mapping, serialize_structured_editor_value, stringify_editor_scalar


def build_mechanics_specs_for_wonder(
    wonder: dict[str, Any],
    *,
    mechanics: dict[str, Any],
    mechanics_data: dict[str, Any],
    unique_wonders_data: dict[str, Any],
    generic_options: list[dict[str, str]],
    option_catalogs: dict[str, list[dict[str, Any]]],
) -> list[MechanicsFieldSpec]:
    specs: list[MechanicsFieldSpec] = []
    prototype_key = mechanic_key(wonder)
    shared_source_kind = "shared"
    inherits_from_prototype = bool(wonder.get("is_unique"))
    base_effect_multiplier = wonder.get("base_effect_multiplier", 1)
    site_help_text = (
        "Inherited from the prototype. Use the prototype selector to change this rule set; edit the prototype wonder to modify the script."
        if inherits_from_prototype
        else "Choose a site-condition template, then adjust the allowed condition atoms instead of editing the raw trigger script directly."
    )
    preference_help_text = (
        "Inherited from the prototype. Use the prototype selector to change this rule set; edit the prototype wonder to modify the script."
        if inherits_from_prototype
        else "Choose a preference template, then edit condition bonus rows and scaled bonus rows; player-visible suitability rows are derived from these rules."
    )
    base_modifier_help_text = (
        (
            f"Inherited from the prototype. Displayed values already apply this unique wonder's x{base_effect_multiplier} "
            "base-effect multiplier; edit the prototype wonder to modify the underlying modifier list."
        )
        if inherits_from_prototype
        else "Structured editor for data/wonder_base_modifiers.yaml base_modifiers entries."
    )
    base_modifier_mapping = mechanics_data.get("base_modifiers", {}).get(prototype_key, {})
    displayed_base_modifier_mapping = (
        scale_numeric_mapping(base_modifier_mapping, base_effect_multiplier)
        if inherits_from_prototype
        else base_modifier_mapping
    )
    building_design = mechanics_data.get("buildings", {}).get(prototype_key, {})
    final_local_mapping = building_design.get("final_local", {})
    displayed_final_building_local_mapping = (
        authored_final_building_local_modifiers(wonder, mechanics)
        if inherits_from_prototype
        else {}
    )

    if not inherits_from_prototype:
        _add_mechanics_spec(
            specs,
            group="Core Data",
            label="Wonder size",
            key=f"mechanics.generic_size.{wonder['key']}",
            source_kind="generic",
            file_path=sources.WONDERS_FILE,
            original_value=str(wonder["size"]),
            field_type="select",
            target_kind="generic_size",
            target_key=wonder["key"],
            height=1,
            options=WONDER_SIZE_OPTIONS,
            help_text="Small, medium, or large. Unique wonders inherit this value from their prototype wonder.",
            target_path=f"wonders[{wonder['key']}].size",
        )

    _add_mechanics_spec(
        specs,
        group="Site Rules",
        label="Build condition template",
        key=f"mechanics.site_trigger.{wonder['key']}",
        source_kind=shared_source_kind,
        file_path=sources.WONDER_SITE_RULES_FILE,
        original_value=serialize_structured_editor_value(
            parse_trigger_builder_state(site_trigger_script_for_key(mechanics_data, prototype_key))
        ),
        field_type="site_trigger_template",
        target_kind="site_rule",
        target_key=prototype_key,
        target_parent_key="trigger_script",
        height=10,
        help_text=site_help_text,
        target_path=f"site_rules.{prototype_key}.trigger_script",
        structured_value=parse_trigger_builder_state(site_trigger_script_for_key(mechanics_data, prototype_key)),
        editable=not inherits_from_prototype,
        prototype_key=prototype_key if inherits_from_prototype else "",
    )
    _add_mechanics_spec(
        specs,
        group="Site Rules",
        label="Survey preference template",
        key=f"mechanics.site_preference.{wonder['key']}",
        source_kind=shared_source_kind,
        file_path=sources.WONDER_SITE_RULES_FILE,
        original_value=serialize_structured_editor_value(
            parse_preference_builder_state(site_preference_script_for_key(mechanics_data, prototype_key))
        ),
        field_type="site_preference_template",
        target_kind="site_rule",
        target_key=prototype_key,
        target_parent_key="preference_script",
        height=14,
        help_text=preference_help_text,
        target_path=f"site_rules.{prototype_key}.preference_script",
        structured_value=parse_preference_builder_state(site_preference_script_for_key(mechanics_data, prototype_key)),
        editable=not inherits_from_prototype,
        prototype_key=prototype_key if inherits_from_prototype else "",
    )
    if inherits_from_prototype:
        inherited_local_state = build_modifier_editor_state(
            displayed_final_building_local_mapping,
            modifier_scope="local",
            options=option_catalogs["local_modifier"],
        )
        _add_mechanics_spec(
            specs,
            group="Final Building Local Effects",
            label="Inherited doubled local effects",
            key=f"mechanics.building_local.inherited.{wonder['key']}",
            source_kind=shared_source_kind,
            file_path=sources.WONDER_FINAL_BUILDINGS_FILE,
            original_value=serialize_structured_editor_value(inherited_local_state),
            field_type="modifier_table",
            target_kind="building_local",
            target_key=prototype_key,
            target_parent_key="final_local",
            height=10,
            help_text=(
                f"Inherited from prototype. Displayed values already apply this unique wonder's x{base_effect_multiplier} "
                "multiplier to the prototype's authored final_local package; edit the prototype wonder to modify the source."
            ),
            target_path=f"buildings.{prototype_key}.final_local",
            structured_value=inherited_local_state,
            editable=False,
            prototype_key=prototype_key,
        )
    else:
        final_local_state = build_modifier_editor_state(
            final_local_mapping,
            modifier_scope="local",
            options=option_catalogs["local_modifier"],
        )
        _add_mechanics_spec(
            specs,
            group="Final Building Local Effects",
            label="Shared final local effects",
            key=f"mechanics.building_local.{wonder['key']}.final_local",
            source_kind=shared_source_kind,
            file_path=sources.WONDER_FINAL_BUILDINGS_FILE,
            original_value=serialize_structured_editor_value(final_local_state),
            field_type="modifier_table",
            target_kind="building_local",
            target_key=prototype_key,
            target_parent_key="final_local",
            height=10,
            help_text="Shared local effects applied identically to all three final-building branches.",
            target_path=f"buildings.{prototype_key}.final_local",
            structured_value=final_local_state,
        )
    _add_mechanics_spec(
        specs,
        group="Base Modifiers",
        label="Per-level base modifiers",
        key=f"mechanics.base_modifiers.{wonder['key']}",
        source_kind=shared_source_kind,
        file_path=sources.WONDER_BASE_MODIFIERS_FILE,
        original_value=serialize_structured_editor_value(
            build_modifier_editor_state(
                displayed_base_modifier_mapping,
                modifier_scope="country",
                options=option_catalogs["country_modifier"],
            )
        ),
        field_type="modifier_table",
        target_kind="base_modifiers",
        target_key=prototype_key,
        height=10,
        help_text=base_modifier_help_text,
        target_path=f"base_modifiers.{prototype_key}",
        structured_value=build_modifier_editor_state(
            displayed_base_modifier_mapping,
            modifier_scope="country",
            options=option_catalogs["country_modifier"],
        ),
        editable=not inherits_from_prototype,
        prototype_key=prototype_key if inherits_from_prototype else "",
    )

    if wonder.get("is_unique"):
        unique_key = wonder["key"]
        unique_entry = get_unique_wonder_source(unique_wonders_data, unique_key)
        _add_mechanics_spec(
            specs,
            group="Unique Wonder",
            label="Prototype wonder",
            key=f"mechanics.unique_prototype.{unique_key}",
            source_kind="unique",
            file_path=sources.UNIQUE_WONDERS_FILE,
            original_value=str(unique_entry["base_key"]),
            field_type="select",
            target_kind="unique_prototype",
            target_key=unique_key,
            height=1,
            options=generic_options,
            help_text="Choose which generic wonder this unique wonder inherits its site rules and base modifiers from.",
            target_path=f"unique_wonders[{unique_key}].base_key",
        )
        _add_mechanics_spec(
            specs,
            group="Unique Wonder",
            label="Fixed location",
            key=f"mechanics.unique_location.{unique_key}",
            source_kind="unique",
            file_path=sources.UNIQUE_WONDERS_FILE,
            original_value=str(unique_entry["location"]),
            field_type="text",
            target_kind="unique_location",
            target_key=unique_key,
            height=2,
            help_text="Edits data/unique_wonders.yaml location.",
            target_path=f"unique_wonders[{unique_key}].location",
        )
        _add_mechanics_spec(
            specs,
            group="Unique Wonder",
            label="Initial level",
            key=f"mechanics.unique_initial_level.{unique_key}",
            source_kind="unique",
            file_path=sources.UNIQUE_WONDERS_FILE,
            original_value=stringify_editor_scalar(
                parse_unique_initial_level(
                    unique_entry.get("initial_level"),
                    context=f"unique_wonders[{unique_key}].initial_level",
                )
            ),
            field_type="number",
            target_kind="unique_initial_level",
            target_key=unique_key,
            height=1,
            help_text="Sets the fixed-site unique wonder level at game-start initialization. Use 0 when absent at start.",
            target_path=f"unique_wonders[{unique_key}].initial_level",
        )
        for n in (1, 2, 3):
            for field, value in unique_entry["ritual_text"][n].items():
                _add_mechanics_spec(specs, group="Ritual Text", label=f"Style {n}: {field}",
                    key=f"mechanics.ritual_text.{unique_key}.{n}.{field}", source_kind="unique",
                    file_path=sources.UNIQUE_WONDERS_FILE, original_value=value, field_type="text",
                    target_kind="unique_ritual_text", target_key=unique_key, target_parent_key=f"{n}.{field}", height=3,
                    target_path=f"unique_wonders[{unique_key}].ritual_text.{n}.{field}")

    from scripts_engineering_department.wonder_mechanics._core import location_reward_estate
    entry = mechanics_data["generic_rituals"][prototype_key]
    for row in entry["rituals"]:
        n = row["style"]
        for carrier, scope, catalog in (("country_modifier", "country", "country_modifier"), ("location_modifier", "local", "local_modifier")):
            state = build_modifier_editor_state(row["reward"].get(carrier, {}), modifier_scope=scope, options=option_catalogs[catalog])
            _add_mechanics_spec(specs, group=f"Ritual {n}", label=carrier.replace("_", " "),
                key=f"mechanics.ritual.{wonder['key']}.{n}.{carrier}", source_kind="shared", file_path=sources.WONDER_GENERIC_RITUALS_FILE,
                original_value=serialize_structured_editor_value(state), field_type="modifier_table", target_kind="ritual_reward",
                target_key=prototype_key, target_parent_key=f"{n}.{carrier}", structured_value=state,
                editable=not inherits_from_prototype, prototype_key=prototype_key if inherits_from_prototype else "",
                target_path=f"generic_rituals.{prototype_key}.rituals[{n}].reward")
        state = build_reward_editor_state(rows=reward_rows_from_list(row["reward"].get("one_shot", [])), options=option_catalogs["reward_type"])
        _add_mechanics_spec(specs, group=f"Ritual {n}", label="One-shot rewards", key=f"mechanics.ritual.{wonder['key']}.{n}.one_shot",
            source_kind="shared", file_path=sources.WONDER_GENERIC_RITUALS_FILE, original_value=serialize_structured_editor_value(state),
            field_type="reward_editor", target_kind="ritual_reward", target_key=prototype_key, target_parent_key=f"{n}.one_shot", structured_value=state,
            editable=not inherits_from_prototype, prototype_key=prototype_key if inherits_from_prototype else "",
            target_path=f"generic_rituals.{prototype_key}.rituals[{n}].reward")
        direction_options = [{"value": end, "label": f"{axis}: {end}"} for axis, data in mechanics["societal_axes"].items() for end in (data["left"], data["right"])]
        _add_mechanics_spec(specs, group=f"Ritual {n}", label="Societal direction", key=f"mechanics.ritual.{wonder['key']}.{n}.direction",
            source_kind="shared", file_path=sources.WONDER_GENERIC_RITUALS_FILE, original_value=row["societal_value"]["direction"],
            field_type="select", target_kind="ritual_direction", target_key=prototype_key, target_parent_key=str(n), options=direction_options,
            editable=not inherits_from_prototype, prototype_key=prototype_key if inherits_from_prototype else "",
            target_path=f"generic_rituals.{prototype_key}.rituals[{n}].societal_value")
    for estate, preference in entry["estate_preferences"].items():
        _add_mechanics_spec(specs, group="Estate Preferences", label=estate, key=f"mechanics.ritual.{wonder['key']}.estate.{estate}",
            source_kind="shared", file_path=sources.WONDER_GENERIC_RITUALS_FILE, original_value=str(preference), field_type="select",
            target_kind="ritual_estate", target_key=prototype_key, target_parent_key=estate,
            options=[{"value": str(n), "label": str(n)} for n in (1, 2, 3, "random")], editable=not inherits_from_prototype,
            prototype_key=prototype_key if inherits_from_prototype else "", target_path=f"generic_rituals.{prototype_key}.estate_preferences.{estate}")
    _add_mechanics_spec(specs, group="Ritual Rules", label="Shared timing, cost and satisfaction", key="mechanics.ritual.rules",
        source_kind="shared", file_path=sources.REPO_ROOT / "data/wonder_ritual_rules.yaml", original_value=str(mechanics["ritual_rules"]),
        field_type="text", target_kind="ritual_rules", target_key="", editable=False, target_path="ritual_rules")
    return specs


def _add_mechanics_spec(
    specs: list[MechanicsFieldSpec],
    *,
    group: str,
    label: str,
    key: str,
    source_kind: str,
    file_path: Path,
    original_value: str,
    field_type: str,
    target_kind: str,
    target_key: str,
    target_parent_key: str = "",
    height: int = 3,
    options: list[dict[str, Any]] | None = None,
    help_text: str = "",
    target_path: str = "",
    structured_value: Any | None = None,
    editable: bool = True,
    prototype_key: str = "",
) -> None:
    specs.append(
        MechanicsFieldSpec(
            key=key,
            label=label,
            group=group,
            source_kind=source_kind,
            file_path=file_path,
            original_value=original_value,
            field_type=field_type,
            target_kind=target_kind,
            target_key=target_key,
            target_parent_key=target_parent_key,
            height=height,
            options=list(options or []),
            help_text=help_text,
            source_path=str(file_path.relative_to(sources.REPO_ROOT)),
            target_path=target_path,
            structured_value=structured_value,
            editable=editable,
            prototype_key=prototype_key,
        )
    )


def build_specs_for_wonder(wonder: dict[str, Any], *, mechanics: dict[str, Any], event_suffixes: dict[int, str], localization_data: dict[str, dict[str, str]]) -> dict[str, list[FieldSpec]]:
    specs = {language: [] for language in LANGUAGES}
    code = wonder["key"].upper()
    for language in LANGUAGES:
        keys = [("Concept", "Description", f"{concept_key_for_wonder(wonder)}_desc"), ("Wonder", "Wonder name", wonder_name_key(wonder)),
            ("Wonder", "Description", f"{wonder_name_key(wonder)}_desc"), ("Final Building", "Name", wonder["final_building"]),
            ("Final Building", "Description", wonder["final_building"] + "_desc")]
        keys += [("Proposal", label, f"{prefix}_{code}_TEXT") for label,prefix in (("Proposal", "TV_ENGINEERING_PROPOSAL"), ("Resume", "TV_ENGINEERING_PROPOSAL_RESUME"), ("Expansion", "TV_ENGINEERING_PROPOSAL_EXPAND"), ("Locked", "TV_ENGINEERING_LOCKED"))]
        if not wonder["is_unique"]:
            keys += [(f"Ritual {n}", label, f"TV_WONDER_RITUAL_{suffix}_{n}_{wonder['id']}") for n in (1,2,3) for label,suffix in (("Name","NAME"),("Description","DESC"))]
        for group,label,key in keys:
            _add_localization_field(localization_data, specs, language, group, label, key, height=3)
    return specs


def _branch_name(localization_data: dict[str, dict[str, str]], wonder: dict[str, Any], style: int, language: str) -> str:
    building = final_building(wonder)
    return localization_value(localization_data, language, branch_button_key(building))


def _add_localization_field(
    localization_data: dict[str, dict[str, str]],
    specs: dict[str, list[FieldSpec]],
    language: str,
    group: str,
    label: str,
    key: str | None,
    *,
    height: int = 3,
) -> None:
    if key is None:
        raise KeyError(f"Missing generated localization key for {label}")
    specs[language].append(
        FieldSpec(
            key=key,
            label=label,
            group=group,
            language=language,
            file_path=sources.WONDER_LOCALIZATION_FILE,
            original_value=localization_value(localization_data, language, key),
            height=height,
        )
    )
