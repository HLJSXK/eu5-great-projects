"""Conversions between Wonder source values and structured editor values."""
from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

import yaml

from scripts_engineering_department.wonder_mechanics.io import dump_yaml_document


WONDER_SIZE_LABELS = {
    "small": "Small",
    "medium": "Medium",
    "large": "Large",
}
WONDER_SIZE_OPTIONS = [
    {"value": size, "label": label}
    for size, label in WONDER_SIZE_LABELS.items()
]
ESTATE_POWER_BY_POP_TYPE = {
    "clergy": "local_clergy_estate_power",
    "nobles": "local_nobles_estate_power",
    "burghers": "local_burghers_estate_power",
    "laborers": "local_peasants_estate_power",
    "soldiers": "local_crown_estate_power",
}
GENERIC_STYLE_2_DERIVED_TITLE = "Auto-applied estate power"
GENERIC_STYLE_2_DERIVED_HELP_TEXT = (
    "The auxiliary building generator always adds this +0.5 local estate power effect "
    "for the wonder's pop_type on top of the editable local modifiers."
)


def serialize_yaml_editor_value(value: object) -> str:
    return dump_yaml_document(value).rstrip()


def normalize_multiline_editor_text(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").strip()


def parse_yaml_editor_value(raw_value: str, *, expected_type: type) -> object:
    text = raw_value.strip()
    if not text:
        raise ValueError(f"Expected {expected_type.__name__} YAML value, got empty input")
    try:
        value = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML value: {exc}") from exc
    if not isinstance(value, expected_type):
        raise ValueError(f"Expected {expected_type.__name__}, got {type(value).__name__}")
    return value


def normalize_text_file(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def serialize_structured_editor_value(payload: object) -> str:
    return json.dumps(without_editor_options(payload), ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def without_editor_options(value: object) -> object:
    """Reserve options and *_options for UI lists, never edited source data."""
    if isinstance(value, dict):
        return {
            key: without_editor_options(item)
            for key, item in value.items()
            if key != "options" and not key.endswith("_options")
        }
    if isinstance(value, list):
        return [without_editor_options(item) for item in value]
    return value


def parse_structured_editor_value(raw_value: object, *, context: str) -> object:
    if isinstance(raw_value, str):
        text = raw_value.strip()
        if not text:
            raise ValueError(f"{context} cannot be empty")
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{context} is not valid editor JSON: {exc}") from exc
    return deepcopy(raw_value)


def stringify_editor_scalar(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value)


def parse_editor_scalar(raw_value: object) -> object:
    if isinstance(raw_value, (int, float)) and not isinstance(raw_value, bool):
        return raw_value
    text = str(raw_value).strip()
    if not text:
        raise ValueError("Scalar value cannot be empty")
    if text.lower() == "yes":
        return True
    if text.lower() == "no":
        return False
    try:
        if any(marker in text for marker in (".", "e", "E")):
            number = float(text)
            if number.is_integer() and "." not in text and "e" not in text.lower():
                return int(number)
            return number
        return int(text)
    except ValueError:
        return text


def parse_unique_initial_level(raw_value: object, *, context: str) -> int:
    parsed = parse_editor_scalar(raw_value)
    if not isinstance(parsed, int) or isinstance(parsed, bool):
        raise ValueError(f"{context} must be an integer from 0 to 6")
    if parsed < 0 or parsed > 6:
        raise ValueError(f"{context} must be an integer from 0 to 6")
    return parsed


def wonder_size_label(size: object) -> str:
    return WONDER_SIZE_LABELS.get(str(size), str(size))


def normalize_editor_wonder_size(raw_value: object, *, context: str) -> str:
    size = str(raw_value).strip()
    if size not in WONDER_SIZE_LABELS:
        supported = ", ".join(WONDER_SIZE_LABELS)
        raise ValueError(f"{context} must be one of: {supported}")
    return size


def modifier_rows_from_mapping(mapping: dict[str, object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for modifier, value in mapping.items():
        rows.append(
            {
                "modifier": str(modifier),
                "value": stringify_editor_scalar(value),
            }
        )
    return rows


def scale_numeric_mapping(mapping: dict[str, object], multiplier: int | float) -> dict[str, object]:
    if multiplier == 1:
        return dict(mapping)
    scaled: dict[str, object] = {}
    for modifier, value in mapping.items():
        if isinstance(value, (int, float)):
            scaled[modifier] = value * multiplier
        else:
            scaled[modifier] = value
    return scaled


def mapping_from_modifier_rows(raw_value: object, *, context: str) -> dict[str, object]:
    payload = parse_structured_editor_value(raw_value, context=context)
    if not isinstance(payload, dict):
        raise ValueError(f"{context} must be an object")
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError(f"{context}.rows must be a list")
    mapping: dict[str, object] = {}
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"{context}.rows[{index}] must be an object")
        modifier = str(row.get("modifier", "")).strip()
        value = str(row.get("value", "")).strip()
        if not modifier and not value:
            continue
        if not modifier:
            raise ValueError(f"{context}.rows[{index}] is missing modifier")
        if not value:
            raise ValueError(f"{context}.rows[{index}] is missing value")
        if modifier in mapping:
            raise ValueError(f"Duplicate modifier {modifier!r} in {context}")
        mapping[modifier] = parse_editor_scalar(value)
    return mapping


def reward_rows_from_list(reward: list[object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in reward:
        if not isinstance(item, dict):
            continue
        rows.append(
            {
                "type": str(item.get("type", "")).strip(),
                "value": stringify_editor_scalar(item.get("value", "")),
            }
        )
    return rows


def reward_list_from_rows(raw_value: object, *, context: str) -> list[dict[str, object]]:
    payload = parse_structured_editor_value(raw_value, context=context)
    if not isinstance(payload, dict):
        raise ValueError(f"{context} must be an object")
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError(f"{context}.rows must be a list")
    reward: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"{context}.rows[{index}] must be an object")
        reward_type = str(row.get("type", "")).strip()
        value = str(row.get("value", "")).strip()
        if not reward_type and not value:
            continue
        if not reward_type:
            raise ValueError(f"{context}.rows[{index}] is missing reward type")
        if not value:
            raise ValueError(f"{context}.rows[{index}] is missing reward value")
        reward.append(
            {
                "type": reward_type,
                "value": parse_editor_scalar(value),
            }
        )
    return reward


def string_rows_from_list(items: list[str]) -> list[dict[str, str]]:
    return [{"value": item} for item in items]


def list_from_string_rows(raw_value: object, *, context: str) -> list[str]:
    payload = parse_structured_editor_value(raw_value, context=context)
    if not isinstance(payload, dict):
        raise ValueError(f"{context} must be an object")
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError(f"{context}.rows must be a list")
    values: list[str] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"{context}.rows[{index}] must be an object")
        value = str(row.get("value", "")).strip()
        if not value:
            continue
        if value in values:
            raise ValueError(f"Duplicate value {value!r} in {context}")
        values.append(value)
    return values


def build_modifier_editor_state(
    mapping: dict[str, object],
    *,
    modifier_scope: str,
    options: list[dict[str, Any]],
    derived_mapping: dict[str, object] | None = None,
    derived_title: str = "",
    derived_help_text: str = "",
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "modifier_scope": modifier_scope,
        "rows": modifier_rows_from_mapping(mapping),
        "options": list(options),
    }
    if derived_mapping:
        payload["derived_rows"] = modifier_rows_from_mapping(derived_mapping)
        payload["derived_title"] = derived_title or "Auto-applied modifiers"
        if derived_help_text:
            payload["derived_help_text"] = derived_help_text
    return payload


def build_reward_editor_state(*, rows: list[dict[str, str]], options: list[dict[str, Any]]) -> dict[str, Any]:
    return {"rows": rows, "options": list(options)}


def _optional_editor_text(value: object) -> str | None:
    text = normalize_multiline_editor_text(str(value))
    return text or None
