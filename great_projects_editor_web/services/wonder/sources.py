"""Wonder source paths, input groups and ritual source loading."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from scripts_engineering_department.wonder_localization_lib import (
    REPO_ROOT,
    WONDER_LOCALIZATION_FILE,
)
from scripts_engineering_department.wonder_mechanics.io import (
    UNIQUE_WONDERS_FILE,
    WONDERS_FILE,
    WONDER_BASE_MODIFIERS_FILE,
    WONDER_FINAL_BUILDINGS_FILE,
    WONDER_GENERIC_RITUALS_FILE,
    WONDER_MECHANICS_DATA_REL,
    WONDER_SITE_RULES_FILE,
)

from ..platform import repo_relative_path
from ..wonder_generation import WONDER_SOURCE_GROUPS


WONDER_LOCALIZATION_DATA_REL = "data/wonder_localization.yaml"
GENERATED_LOC_DATA_REL = f"data/wonders.yaml + {WONDER_MECHANICS_DATA_REL} + data/unique_wonders.yaml + data/wonder_localization.yaml"


def wonder_source_paths() -> tuple[Path, ...]:
    """Return source paths from the current module constants.

    Tests and local editor instances can redirect the repository data files;
    deriving this tuple at use time keeps the resource contract aligned with
    those redirected paths.
    """
    return (
        WONDER_LOCALIZATION_FILE,
        WONDER_FINAL_BUILDINGS_FILE,
        WONDER_GENERIC_RITUALS_FILE,
        WONDER_BASE_MODIFIERS_FILE,
        WONDER_SITE_RULES_FILE,
        WONDERS_FILE,
        UNIQUE_WONDERS_FILE,
    )


def wonder_source_rels() -> tuple[str, ...]:
    return tuple(
        repo_relative_path(path, REPO_ROOT)
        for path in wonder_source_paths()
    )


def wonder_input_groups(files: dict[Path, bytes]) -> set[str]:
    return {
        WONDER_SOURCE_GROUPS[repo_relative_path(path, REPO_ROOT)]
        for path in files
        if repo_relative_path(path, REPO_ROOT) in WONDER_SOURCE_GROUPS
    }


WONDER_EDITOR_CATALOG_FILE = REPO_ROOT / "data" / "wonder_editor_catalog.yaml"
MODIFIER_LOCALIZATION_INDEX_FILE = REPO_ROOT / "data" / "index" / "modifier_localization.json"
GENERATED_WONDER_IMAGES_DIR = REPO_ROOT / "assets" / "generated_wonders"
WONDER_IMAGE_URL_PREFIX = "/wonder-images"
GENERATED_LOC_FILES = {
    "english": REPO_ROOT / "src" / "main_menu" / "localization" / "english" / "tv_engineering_department_wonder_mechanics_l_english.yml",
    "simp_chinese": REPO_ROOT / "src" / "main_menu" / "localization" / "simp_chinese" / "tv_engineering_department_wonder_mechanics_l_simp_chinese.yml",
}
MANUAL_CONCEPT_FILES = {
    "english": REPO_ROOT / "src" / "main_menu" / "localization" / "english" / "tv_engineering_department_game_concepts_l_english.yml",
    "simp_chinese": REPO_ROOT / "src" / "main_menu" / "localization" / "simp_chinese" / "tv_engineering_department_game_concepts_l_simp_chinese.yml",
}
MANUAL_ENGINEERING_FILES = {
    "english": REPO_ROOT / "src" / "main_menu" / "localization" / "english" / "tv_engineering_department_l_english.yml",
    "simp_chinese": REPO_ROOT / "src" / "main_menu" / "localization" / "simp_chinese" / "tv_engineering_department_l_simp_chinese.yml",
}
CONCEPT_FILE = REPO_ROOT / "src" / "main_menu" / "common" / "game_concepts" / "tv_engineering_department_wonder_mechanics_concepts.txt"
CONCEPT_SCRIPT_REL = "scripts_engineering_department/main_menu/common/game_concepts/gen_tv_engineering_department_wonder_mechanics_concepts.py"
REFERENCE_LOC_DIR_BY_EDITOR_LANGUAGE = {
    "english": REPO_ROOT / ".eu5-base" / "reference_game_files" / "game" / "main_menu" / "localization" / "english",
    "simp_chinese": REPO_ROOT / ".eu5-base" / "reference_game_files" / "game" / "main_menu" / "localization" / "simp_chinese",
}


def load_yaml_text(text: str) -> Any:
    """Safe-load YAML through libyaml; the ritual design source alone is about 6 MB."""
    return yaml.load(text, Loader=yaml.CSafeLoader)


def get_unique_wonder_source(data: dict[str, Any], key: str) -> dict[str, Any]:
    return next(row for row in data["unique_wonders"] if row["key"] == key)
