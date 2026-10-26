"""Wonder edit application and queries."""
from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import quote

from scripts_engineering_department.wonder_localization_lib import normalize_editor_text

from . import sources
from .field_types import serialize_mechanics_specs, serialize_specs
from .fields import build_mechanics_specs_for_wonder, build_specs_for_wonder
from .localization import LANGUAGES, localization_value, wonder_name_key
from .options import reference_option_catalogs
from .site_rules import render_preference_script_from_state, render_trigger_script_from_state
from .sources import get_unique_wonder_source
from .values import mapping_from_modifier_rows, normalize_editor_wonder_size, normalize_multiline_editor_text, parse_unique_initial_level, parse_yaml_editor_value, reward_list_from_rows, wonder_size_label


RITUAL_DESIGN_FIELD_LABELS = {
    "title": "标题",
    "historical_flavor": "历史氛围",
    "mode": "模式",
    "duration": "持续时间",
    "listeners": "监听器",
    "confirmation_logic": "确认逻辑",
    "start_logic": "启动逻辑",
    "progress_logic": "推进逻辑",
    "completion_logic": "完成逻辑",
    "failure_or_timeout_logic": "失败或超时逻辑",
    "implementation_mapping": "实现映射",
    "confirmation_trigger_script": "确认触发脚本",
    "start_effect_script": "启动效果脚本",
    "snapshot_effect_script": "快照效果脚本",
    "progress_effect_script": "推进效果脚本",
    "completion_trigger_script": "完成触发脚本",
    "completion_effect_script": "完成效果脚本",
    "intended_rewards": "预期奖励",
    "permanent_country_modifier": "永久国家修正",
    "local_building_reward": "本地建筑奖励",
    "one_time_reward": "一次性奖励",
    "notes": "备注",
}


class WonderModel:
    """Apply Wonder edits and query summaries, details and ritual designs."""

    def option_catalog_payload(self) -> dict[str, Any]:
        with self._lock:
            return {"version": self._option_catalog_version, "catalogs": self._option_catalogs}

    def list_wonders(self, filter_text: str = "") -> list[dict[str, Any]]:
        normalized_filter = filter_text.strip().lower()
        wonders: list[dict[str, Any]] = []
        for wonder in self.wonders:
            haystack = " ".join(
                [
                    str(wonder["id"]),
                    wonder["key"],
                    wonder["concept"],
                    wonder.get("base_key", ""),
                    wonder.get("size", ""),
                    wonder_size_label(wonder.get("size", "")),
                    self._wonder_name(wonder, "english"),
                    self._wonder_name(wonder, "simp_chinese"),
                ]
            ).lower()
            if normalized_filter and normalized_filter not in haystack:
                continue
            wonders.append(self._wonder_summary(wonder))
        return wonders

    def get_wonder_payload(self, wonder_id: int | None) -> dict[str, Any] | None:
        with self._lock:
            if wonder_id is None:
                return None
            wonder = self._get_wonder(wonder_id)
            specs = build_specs_for_wonder(
                wonder, mechanics=self.mechanics, event_suffixes=self.event_suffixes,
                localization_data=self.localization_data,
            )
            mechanics_specs = build_mechanics_specs_for_wonder(
                wonder, mechanics=self.mechanics, mechanics_data=self.mechanics_data,
                unique_wonders_data=self.unique_wonders_data,
                generic_options=self._generic_wonder_options() if wonder.get("is_unique") else [],
                option_catalogs=self._option_catalogs,
            )
            payload = {
                "summary": self._wonder_summary(wonder),
                "meta": self._wonder_meta(wonder),
                "languages": serialize_specs(specs),
                "mechanics": serialize_mechanics_specs(mechanics_specs),
                "status": f"Loaded {wonder['key']}",
                "catalog_version": self._option_catalog_version,
            }
            reference_option_catalogs(payload["mechanics"], self._option_catalogs)
            return payload

    def _apply_wonder_edits(
        self,
        wonder_id: int,
        values_by_language: dict[str, dict[str, str]] | None,
        mechanics_values: dict[str, Any] | None = None,
    ) -> dict[str, bool]:
        wonder = self._get_wonder(wonder_id)
        specs = build_specs_for_wonder(
            wonder, mechanics=self.mechanics, event_suffixes=self.event_suffixes,
            localization_data=self.localization_data,
        )
        mechanics_specs = build_mechanics_specs_for_wonder(
            wonder, mechanics=self.mechanics, mechanics_data=self.mechanics_data,
            unique_wonders_data=self.unique_wonders_data,
            generic_options=self._generic_wonder_options() if wonder.get("is_unique") else [],
            option_catalogs=self._option_catalogs,
        )
        localization_updates: dict[str, dict[str, str]] = {language: {} for language in LANGUAGES}
        incoming_values = values_by_language or {}
        incoming_mechanics = mechanics_values or {}

        for language, language_specs in specs.items():
            language_values = incoming_values.get(language, {})
            for spec in language_specs:
                value = normalize_editor_text(str(language_values.get(spec.key, spec.original_value)))
                if value == spec.original_value:
                    continue
                localization_updates[language][spec.key] = value

        wonders_file_changed = False
        mechanics_file_changed = False
        unique_file_changed = False
        for spec in mechanics_specs:
            raw_value = incoming_mechanics.get(spec.key, spec.original_value)
            if spec.field_type in {
                "modifier_table",
                "reward_editor",
                "site_trigger_template",
                "site_preference_template",
            }:
                value = str(raw_value)
            else:
                value = normalize_multiline_editor_text(str(raw_value))
            if value == spec.original_value:
                continue
            if not spec.editable:
                continue

            if spec.target_kind == "site_rule":
                if spec.field_type == "site_trigger_template":
                    rendered_script = render_trigger_script_from_state(value, context=spec.key)
                elif spec.field_type == "site_preference_template":
                    rendered_script = render_preference_script_from_state(value, context=spec.key)
                else:
                    rendered_script = value
                if not rendered_script:
                    raise ValueError(f"{spec.key} cannot be empty")
                self.mechanics_data["site_rules"][spec.target_key][spec.target_parent_key] = rendered_script
                mechanics_file_changed = True
                continue

            if spec.target_kind == "generic_size":
                size = normalize_editor_wonder_size(value, context=spec.key)
                entry = self._get_generic_wonder_source(spec.target_key)
                entry["size"] = size
                wonders_file_changed = True
                continue

            if spec.target_kind == "unique_prototype":
                if not value:
                    raise ValueError(f"{spec.key} cannot be empty")
                self._get_generic_wonder_by_key(value)
                entry = get_unique_wonder_source(self.unique_wonders_data, spec.target_key)
                entry["base_key"] = value
                entry["mechanic_key"] = value
                unique_file_changed = True
                continue

            if spec.target_kind == "building_local":
                if spec.field_type == "modifier_table":
                    parsed = mapping_from_modifier_rows(value, context=spec.key)
                else:
                    parsed = parse_yaml_editor_value(value, expected_type=dict)
                self.mechanics_data.setdefault("buildings", {}).setdefault(spec.target_key, {})[
                    spec.target_parent_key
                ] = parsed
                mechanics_file_changed = True
                continue

            if spec.target_kind == "base_modifiers":
                if spec.field_type == "modifier_table":
                    parsed = mapping_from_modifier_rows(value, context=spec.key)
                else:
                    parsed = parse_yaml_editor_value(value, expected_type=dict)
                self.mechanics_data.setdefault("base_modifiers", {})[spec.target_key] = parsed
                mechanics_file_changed = True
                continue

            if spec.target_kind in {"ritual_reward", "ritual_direction", "ritual_estate"}:
                entry = self.mechanics_data["generic_rituals"][spec.target_key]
                if spec.target_kind == "ritual_estate":
                    entry["estate_preferences"][spec.target_parent_key] = "random" if value == "random" else int(value)
                else:
                    n = int(spec.target_parent_key.split(".")[0])
                    row = next(r for r in entry["rituals"] if r["style"] == n)
                    if spec.target_kind == "ritual_direction":
                        axis = next((key for key,data in self.mechanics["societal_axes"].items() if value in (data["left"],data["right"])), None)
                        if axis is None: raise ValueError(f"Unknown societal direction: {value}")
                        row["societal_value"] = {"axis": axis, "direction": value}
                    else:
                        carrier = spec.target_parent_key.split(".")[1]
                        parsed = reward_list_from_rows(value, context=spec.key) if carrier == "one_shot" else mapping_from_modifier_rows(value, context=spec.key)
                        if parsed: row["reward"][carrier] = parsed
                        else: row["reward"].pop(carrier, None)
                mechanics_file_changed = True
                continue

            if spec.target_kind == "unique_location":
                if not value:
                    raise ValueError(f"{spec.key} cannot be empty")
                entry = get_unique_wonder_source(self.unique_wonders_data, spec.target_key)
                entry["location"] = value
                unique_file_changed = True
                continue

            if spec.target_kind == "unique_initial_level":
                parsed = parse_unique_initial_level(value, context=spec.key)
                entry = get_unique_wonder_source(self.unique_wonders_data, spec.target_key)
                entry["initial_level"] = parsed
                unique_file_changed = True
                continue

            if spec.target_kind == "unique_ritual_text":
                n, field = spec.target_parent_key.split(".")
                if not value: raise ValueError(f"{spec.key} cannot be empty")
                get_unique_wonder_source(self.unique_wonders_data, spec.target_key)["ritual_text"][int(n)][field] = value
                unique_file_changed = True
                continue

            raise ValueError(f"Unsupported mechanics target kind: {spec.target_kind}")

        from scripts_engineering_department.wonder_mechanics import _core as data_core
        if mechanics_file_changed:
            data_core._validate_generic_rituals(self.mechanics_data["generic_rituals"], "generic_rituals")
        if unique_file_changed:
            for entry in self.unique_wonders_data["unique_wonders"]:
                data_core._validate_ritual_text(entry["ritual_text"], f"{entry['key']}.ritual_text")
        localization_file_changed = any(localization_updates[language] for language in LANGUAGES)
        if localization_file_changed:
            for language, updates in localization_updates.items():
                if not updates:
                    continue
                self.localization_data[language].update(updates)

        return {
            "localization": localization_file_changed,
            "mechanics": mechanics_file_changed,
            "wonders": wonders_file_changed,
            "unique": unique_file_changed,
        }


    def _get_wonder(self, wonder_id: int) -> dict[str, Any]:
        for wonder in self.wonders:
            if int(wonder["id"]) == int(wonder_id):
                return wonder
        raise KeyError(f"Unknown wonder id: {wonder_id}")

    def _unique_initial_level(self, wonder: dict[str, Any]) -> int:
        if not wonder.get("is_unique"):
            return 0
        unique_key = str(wonder["key"])
        entry = get_unique_wonder_source(self.unique_wonders_data, unique_key)
        return parse_unique_initial_level(
            entry.get("initial_level"),
            context=f"unique_wonders[{unique_key}].initial_level",
        )

    def _get_generic_wonder_source(self, wonder_key: str) -> dict[str, Any]:
        for wonder in self.wonders_data.get("wonders", []):
            if wonder.get("key") == wonder_key:
                return wonder
        raise KeyError(f"Unknown generic wonder key: {wonder_key}")

    def _get_generic_wonder_by_key(self, wonder_key: str) -> dict[str, Any]:
        for wonder in self.wonders:
            if not wonder.get("is_unique") and wonder.get("key") == wonder_key:
                return wonder
        raise KeyError(f"Unknown generic wonder key: {wonder_key}")

    def _wonder_name(self, wonder: dict[str, Any], language: str) -> str:
        return localization_value(self.localization_data, language, wonder_name_key(wonder))

    def _wonder_image_info(self, wonder: dict[str, Any]) -> dict[str, Any]:
        raw_stem = str(wonder.get("image") or f"tv_wonder_{wonder['key']}").strip()
        filename = raw_stem if raw_stem.lower().endswith(".png") else f"{raw_stem}.png"
        if not filename or Path(filename).name != filename:
            return {
                "stem": raw_stem,
                "filename": filename,
                "path": "",
                "url": None,
                "exists": False,
            }

        image_path = sources.GENERATED_WONDER_IMAGES_DIR / filename
        exists = image_path.is_file()
        return {
            "stem": Path(filename).stem,
            "filename": filename,
            "path": f"assets/generated_wonders/{filename}",
            "url": f"{sources.WONDER_IMAGE_URL_PREFIX}/{quote(filename)}" if exists else None,
            "exists": exists,
        }

    def _wonder_summary(self, wonder: dict[str, Any]) -> dict[str, Any]:
        kind_label = "Unique" if wonder.get("is_unique") else "Generic"
        name_en = self._wonder_name(wonder, "english")
        name_zh = self._wonder_name(wonder, "simp_chinese")
        size = str(wonder.get("size", ""))
        return {
            "id": int(wonder["id"]),
            "key": wonder["key"],
            "concept": wonder["concept"],
            "is_unique": bool(wonder.get("is_unique")),
            "initial_level": self._unique_initial_level(wonder),
            "kind_label": kind_label,
            "size": size,
            "size_label": wonder_size_label(size),
            "name_en": name_en,
            "name_zh": name_zh,
            "display_name": f"{name_zh} / {name_en}",
            "image": self._wonder_image_info(wonder),
        }

    def _wonder_meta(self, wonder: dict[str, Any]) -> dict[str, Any]:
        meta = {
            "id": int(wonder["id"]),
            "key": wonder["key"],
            "concept": wonder["concept"],
            "name_en": self._wonder_name(wonder, "english"),
            "name_zh": self._wonder_name(wonder, "simp_chinese"),
            "is_unique": bool(wonder.get("is_unique")),
            "initial_level": self._unique_initial_level(wonder),
            "size": str(wonder.get("size", "")),
            "size_label": wonder_size_label(wonder.get("size", "")),
            "image": self._wonder_image_info(wonder),
        }
        if wonder.get("is_unique"):
            meta["base_key"] = wonder.get("base_key")
            meta["mechanic_key"] = wonder.get("mechanic_key")
            meta["base_effect_multiplier"] = wonder.get("base_effect_multiplier", 1)
            meta["location"] = wonder.get("location")
        return meta

    def _generic_wonder_options(self) -> list[dict[str, str]]:
        options: list[dict[str, str]] = []
        for wonder in self.wonders:
            if wonder.get("is_unique"):
                continue
            options.append(
                {
                    "value": wonder["key"],
                    "label": self._wonder_summary(wonder)["display_name"],
                }
            )
        return options
