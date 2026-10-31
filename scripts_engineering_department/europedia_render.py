"""Render the Great Projects Europedia: card GUI lines and their localization.

Three thin generators consume this module, so a card's layout and its text can never drift
apart:

    in_game/gui/gen_tv_encyclopedia_wonders_cards_gui.py          -> data/generated_fragments/
    main_menu/localization/english/gen_tv_europedia_l_english.py  -> src/.../english/
    main_menu/localization/simp_chinese/gen_tv_europedia_l_simp_chinese.py

Card shapes come from in_game/gui/shared/tv_europedia_style.gui; prose and layout intent come
from europedia_content.py; wonder cards are built from the wonder data package so their
effects, dedications and estates are always the shipped ones.

Catalogue effects are baked from current data by europedia_catalogue.py. The user
approved static content to avoid live effect/trigger evaluation during loading.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "scripts_engineering_department") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from europedia_content import CARDS  # noqa: E402
from europedia_catalogue import Catalogue  # noqa: E402
from gen_europedia_cycle import CYCLE_SIZE, CYCLE_CENTER, STEP_SIZE, TEXTURE, step_positions  # noqa: E402


T = "\t"
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}

FILTER_IDS = ("all", "overview", "mechanics", "unique", "generic")
PREFIX = "TV_EU"

# Worked examples remain in Mechanics. Dedicated tabs hold the approved compact,
# static catalogue (2026-10-30); see the Europedia risk card.
WONDER_CARD_KEYS = ("triumphal_axis", "unique_topkapi_palace")

# Section icons for generated cards. Every path below is one vanilla GUI already uses.
ICON_SECTION = "gfx/interface/icons/flat_icons/tabicons/europedia_flat_icon.dds"
ICON_SIZE = "gfx/interface/icons/flat_icons/mass_upgrade.dds"
ICON_EFFECT = "gfx/interface/icons/flat_icons/tabicons/advances.dds"
ICON_SITE = "gfx/interface/icons/flat_icons/tabicons/mapmodes.dds"
ICON_RITUAL = "gfx/interface/icons/flat_icons/hre_parliament.dds"
ICON_ESTATE = "gfx/interface/icons/flat_icons/estates/estates.dds"
ICON_CATEGORY = "gfx/interface/icons/flat_icons/cultural_tradition.dds"


def key(*parts: str) -> str:
    return PREFIX + "_" + "_".join(part.upper() for part in parts)


def _q(text: str) -> str:
    return f'"{text}"'


def visible_by_filter(category: str) -> str:
    """Show only this tab's cards; the first visit defaults to complete mechanics.

    All is an empty reserved tab for now, not an aggregate of the other tabs.
    """
    selected = f"GetVariableSystem.HasValue('tv_encyclopedia_filter', '{category}')"
    if category == "mechanics":
        return f"[Or(Not(GetVariableSystem.Exists('tv_encyclopedia_filter')), {selected})]"
    return f"[{selected}]"


# --------------------------------------------------------------------------- card shell ----


def card_open(lines: list[str], category: str) -> None:
    """Open a card. The shell (paper sheet, width, margins) is the tv_eu_card type; a card only
    supplies its header tab and its body."""
    lines.append(f"{T}vbox = {{")
    lines.append(f"{T}{T}visible = {_q(visible_by_filter(category))}")
    lines.append(f"{T}{T}tv_eu_card = {{")


def card_header(lines: list[str], texture: str, title_key: str) -> None:
    """The vanilla card header tab: an icon and a gold title on the blue tab strip."""
    lines.append(f'{T}{T}{T}blockoverride "card_header" {{')
    lines.append(f"{T}{T}{T}{T}icon = {{")
    lines.append(f"{T}{T}{T}{T}{T}layoutpolicy_horizontal = expanding")
    lines.append(f"{T}{T}{T}{T}{T}using = button_main_tab_texture")
    lines.append(f"{T}{T}{T}{T}{T}frame = 4")
    lines.append("")
    lines.append(f"{T}{T}{T}{T}{T}modify_texture = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}using = color_intense_bg_blue_texture")
    lines.append(f"{T}{T}{T}{T}{T}{T}blend_mode = multiply")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append("")
    lines.append(f"{T}{T}{T}{T}{T}modify_texture = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}using = overlay_leather_texture")
    lines.append(f"{T}{T}{T}{T}{T}{T}blend_mode = overlay")
    lines.append(f"{T}{T}{T}{T}{T}{T}alpha = 0.2")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append("")
    lines.append(f"{T}{T}{T}{T}{T}hbox = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}margin = {{ 40 0 }}")
    lines.append(f"{T}{T}{T}{T}{T}{T}margin_top = 8")
    lines.append("")
    lines.append(f"{T}{T}{T}{T}{T}{T}icon = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}size = {{ 45 45 }}")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}texture = {_q(texture)}")
    lines.append(f"{T}{T}{T}{T}{T}{T}}}")
    lines.append("")
    lines.append(f"{T}{T}{T}{T}{T}{T}text_single = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}using = layoutpolicy_expanding")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}using = Font_Type_Headers")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}fontsize = 22")
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}autoresize = yes")
    lines.append(f'{T}{T}{T}{T}{T}{T}{T}default_format = "#yellow_titles"')
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}text = {_q(title_key)}")
    lines.append(f"{T}{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f'{T}{T}{T}}}')
    # everything after the header is the body
    lines.append(f'{T}{T}{T}blockoverride "card_body" {{')
    lines.append(f"{T}{T}{T}{T}vbox = {{")
    lines.append(f"{T}{T}{T}{T}{T}layoutpolicy_horizontal = expanding")
    lines.append(f"{T}{T}{T}{T}{T}spacing = 10")


def card_close(lines: list[str]) -> None:
    lines.append(f"{T}{T}{T}{T}}}")  # card body vbox
    lines.append(f"{T}{T}{T}}}")     # blockoverride card_body
    lines.append(f"{T}{T}}}")        # tv_eu_card
    lines.append(f"{T}}}")           # per-card wrapper


def section_heading(lines: list[str], texture: str, title_key: str) -> None:
    lines.append(f"{T}{T}{T}tv_eu_section = {{")
    lines.append(f'{T}{T}{T}{T}blockoverride "section_icon" {{ texture = {_q(texture)} }}')
    lines.append(f'{T}{T}{T}{T}blockoverride "section_title" {{ text = {_q(title_key)} }}')
    lines.append(f"{T}{T}{T}}}")


def body_text(lines: list[str], text_key: str, width: int | None = None) -> None:
    bounds = f"min_width = {width} max_width = {width} " if width is not None else ""
    lines.append(f"{T}{T}{T}tv_eu_text = {{ {bounds}text = {_q(text_key)} }}")


def _medallion(lines: list[str], spec: tuple) -> None:
    kind, value = spec
    if kind == "text":
        lines.append(f"{T}{T}{T}{T}{T}{T}text_single = {{")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}size = {{ 64 64 }}")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}align = center")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}using = Font_Type_Headers")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}fontsize = 26")
        lines.append(f'{T}{T}{T}{T}{T}{T}{T}default_format = "#yellow_titles"')
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}autoresize = yes")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}raw_text = {_q(str(value))}")
        lines.append(f"{T}{T}{T}{T}{T}{T}}}")
    elif kind == "icon":
        lines.append(f"{T}{T}{T}{T}{T}{T}icon = {{ size = {{ 64 64 }} texture = {_q(str(value))} }}")
    elif kind == "bar":
        # A painted bar: the base plate plus a stretched gold fill, the shape the debate card
        # uses to show where a support value sits on its 0-200 scale.
        width = max(1, int(round(60 * float(value))))
        lines.append(f"{T}{T}{T}{T}{T}{T}background = {{ using = color_bg_brown_texture }}")
        lines.append(f"{T}{T}{T}{T}{T}{T}icon = {{")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}size = {{ {width} 64 }}")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}position = {{ 2 2 }}")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}using = color_gold_texture")
        lines.append(f"{T}{T}{T}{T}{T}{T}}}")
    elif kind == "roman":
        _medallion(lines, ("text", ROMAN[int(value)]))
    else:  # pragma: no cover - content mistake, fail loudly at generation time
        raise ValueError(f"Unknown medallion spec {spec!r}")


def _entry_icons(lines: list[str], icons: list) -> None:
    lines.append(f"{T}{T}{T}{T}{T}hbox = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}spacing = 8")
    for icon in icons:
        if isinstance(icon, tuple) and icon[0] == "icon":
            lines.append(f"{T}{T}{T}{T}{T}{T}icon = {{")
            lines.append(f"{T}{T}{T}{T}{T}{T}{T}size = {{ 64 64 }}")
            lines.append(f"{T}{T}{T}{T}{T}{T}{T}texture = {_q(icon[1])}")
            lines.append(f"{T}{T}{T}{T}{T}{T}}}")
        else:  # pragma: no cover
            raise ValueError(f"Unknown entry icon {icon!r}")
    lines.append(f"{T}{T}{T}{T}{T}}}")


def _panel_item(lines: list[str], item: dict) -> None:
    """One icon in a comparison panel; alpha dims an icon for the thing being ignored."""
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}tv_eu_item = {{")
    icon_block = f'{T}{T}{T}{T}{T}{T}{T}{T}blockoverride "item_icon" {{ texture = {_q(item["icon"])}'
    alpha = item.get("alpha")
    if alpha is not None:
        icon_block += f" alpha = {alpha}"
    lines.append(icon_block + " }")
    lines.append(f'{T}{T}{T}{T}{T}{T}{T}{T}blockoverride "item_link" {{ raw_text = {_q(item.get("link") or "")} }}')
    lines.append(f"{T}{T}{T}{T}{T}{T}{T}}}")


# --------------------------------------------------------------- content (mechanic) cards ----


# ----------------------------------------------------------- anatomy (teaching) cards ----

# Every anatomy control is built from the same two primitives: a strip that looks like the
# panel's own widget, and the panel's own localization key for its label. No control below is
# clickable, so the tab cannot fire a gameplay action while merely explaining one.
MOCK_ICON_ESTATE = "gfx/interface/icons/flat_icons/estates/estates.dds"
LOC_KEY = re.compile(r"^[A-Z][A-Z0-9]*_[A-Z0-9_]+$")


def _is_loc_key(value: str) -> bool:
    """A tile value is either a sample figure or a reference to a shipped panel label."""
    return bool(LOC_KEY.match(value))

# Each step's mock carries the header of the card it explains, so the player matches the two
# by title rather than by guessing. These are shipped keys, identical in all 11 languages.
ANATOMY_PANEL_TITLES = {
    "appointment": "TV_ENGINEERING_GREAT_ENGINEER_CARD_TITLE",
    "conception": "TV_ENGINEERING_CONCEPT_CARD_TITLE",
    "debate": "TV_ENGINEERING_STATUS_CARD_TITLE",
    "survey": "TV_ENGINEERING_SURVEY_CARD_TITLE",
    "organization_logistics": "TV_ENGINEERING_ORG_LOG_CARD_TITLE",
    "construction": "TV_ENGINEERING_CONSTRUCTION_CARD_TITLE",
    "ceremony": "TV_ENGINEERING_CEREMONY_CARD_TITLE",
}


def _mock_button(lines: list[str], label_key: str, colour: str | None, indent: str,
                 width: int, height: int = 32) -> None:
    """One button-shaped strip carrying the panel's real label. Never clickable."""
    style = {
        "green": "tv_eu_mock_button_green",
        "yellow": "tv_eu_mock_button_yellow",
        "red": "tv_eu_mock_button_red",
    }.get(colour or "", "tv_eu_mock_button")
    lines.append(f"{indent}widget = {{")
    lines.append(f"{indent}{T}size = {{ {width} {height} }}")
    lines.append(f"{indent}{T}{style} = {{")
    lines.append(f'{indent}{T}{T}blockoverride "mock_text" {{ text = {_q(label_key)} }}')
    lines.append(f"{indent}{T}}}")
    lines.append(f"{indent}}}")


def _mock_buttons(lines: list[str], buttons: list, indent: str) -> None:
    """A stack of button-shaped strips, each the width of a list row in the panel."""
    for label_key, colour in buttons:
        _mock_button(lines, label_key, colour, indent, 400)


def _mock_bar(lines: list[str], mock: tuple, indent: str) -> None:
    """A labelled bar frozen at its example value; the number is the step's sample, not live."""
    _, label_key, value, text, *rest = mock
    captions = rest[0] if rest else None
    lines.append(f"{indent}tv_eu_mock_bar = {{")
    lines.append(f'{indent}{T}blockoverride "mock_label" {{ text = {_q(label_key)} }}')
    if text:
        lines.append(f'{indent}{T}blockoverride "mock_bar_text" {{ raw_text = {_q(text)} }}')
    lines.append(f'{indent}{T}blockoverride "mock_bar_value" {{ value = {value} }}')
    lines.append(f"{indent}}}")
    if captions:
        lines.append(f"{indent}hbox = {{")
        lines.append(f"{indent}{T}layoutpolicy_horizontal = expanding")
        for caption_key in captions:
            lines.append(f"{indent}{T}text_single = {{")
            lines.append(f"{indent}{T}{T}layoutpolicy_horizontal = expanding")
            lines.append(f"{indent}{T}{T}autoresize = yes")
            lines.append(f"{indent}{T}{T}fontsize = 12")
            lines.append(f'{indent}{T}{T}default_format = "#weak"')
            lines.append(f"{indent}{T}{T}text = {_q(caption_key)}")
            lines.append(f"{indent}{T}}}")
        lines.append(f"{indent}}}")


def _mock_stats(lines: list[str], cells: list[tuple[str, str]], indent: str) -> None:
    """A row of stat tiles. A cell whose value is an ALL_CAPS key is a panel label, not a number."""
    lines.append(f"{indent}tv_eu_mock_stats = {{")
    lines.append(f'{indent}{T}blockoverride "mock_stats" {{')
    lines.append(f"{indent}{T}{T}hbox = {{")
    lines.append(f"{indent}{T}{T}{T}spacing = 6")
    for label_key, value in cells:
        lines.append(f"{indent}{T}{T}{T}tv_eu_mock_stat = {{")
        lines.append(f'{indent}{T}{T}{T}{T}blockoverride "mock_stat_label" {{ text = {_q(label_key)} }}')
        if _is_loc_key(value):
            lines.append(f'{indent}{T}{T}{T}{T}blockoverride "mock_stat_value" {{ text = {_q(value)} }}')
        else:
            lines.append(f'{indent}{T}{T}{T}{T}blockoverride "mock_stat_value" {{ raw_text = {_q(value)} }}')
        lines.append(f"{indent}{T}{T}{T}}}")
    lines.append(f"{indent}{T}{T}}}")
    lines.append(f"{indent}{T}}}")
    lines.append(f"{indent}}}")


def _mock_pills(lines: list[str], labels: list[str], active: str | None, indent: str) -> None:
    """Size pills: the panel's three size labels, one of them picked."""
    lines.append(f"{indent}hbox = {{")
    lines.append(f"{indent}{T}spacing = 8")
    for label_key in labels:
        _mock_button(lines, label_key, "yellow" if label_key == active else None, f"{indent}{T}", 180)
    lines.append(f"{indent}}}")


def _mock_status(lines: list[str], label_key: str, indent: str) -> None:
    """The header status strip: the one line that says why nothing can start."""
    lines.append(f"{indent}widget = {{")
    lines.append(f"{indent}{T}minimumsize = {{ 360 32 }}")
    lines.append(f"{indent}{T}maximumsize = {{ 560 32 }}")
    lines.append(f"{indent}{T}layoutpolicy_horizontal = expanding")
    lines.append(f"{indent}{T}using = bg_text_mask_container_dark_blue")
    lines.append(f"{indent}{T}text_single = {{")
    lines.append(f"{indent}{T}{T}size = {{ 100% 100% }}")
    lines.append(f"{indent}{T}{T}align = center|nobaseline")
    lines.append(f"{indent}{T}{T}autoresize = no")
    lines.append(f'{indent}{T}{T}default_format = "#high"')
    lines.append(f"{indent}{T}{T}text = {_q(label_key)}")
    lines.append(f"{indent}{T}}}")
    lines.append(f"{indent}}}")


def _mock_portrait(lines: list[str], label_key: str, indent: str) -> None:
    """The empty chief portrait: a framed slot with a + and the appointment prompt."""
    lines.append(f"{indent}widget = {{")
    lines.append(f"{indent}{T}size = {{ 250 150 }}")
    lines.append(f"{indent}{T}using = bg_text_mask_container_dark_blue")
    lines.append(f"{indent}{T}vbox = {{")
    lines.append(f"{indent}{T}{T}size = {{ 250 150 }}")
    lines.append(f"{indent}{T}{T}spacing = 2")
    lines.append(f"{indent}{T}{T}expand = {{}}")
    lines.append(f"{indent}{T}{T}text_single = {{")
    lines.append(f"{indent}{T}{T}{T}size = {{ 250 44 }}")
    lines.append(f"{indent}{T}{T}{T}raw_text = \"+\"")
    lines.append(f"{indent}{T}{T}{T}fontsize = 34")
    lines.append(f"{indent}{T}{T}{T}align = center|nobaseline")
    lines.append(f'{indent}{T}{T}{T}default_format = "#yellow_titles"')
    lines.append(f"{indent}{T}{T}}}")
    lines.append(f"{indent}{T}{T}text_single = {{")
    lines.append(f"{indent}{T}{T}{T}size = {{ 250 20 }}")
    lines.append(f"{indent}{T}{T}{T}fontsize = 14")
    lines.append(f"{indent}{T}{T}{T}align = center|nobaseline")
    lines.append(f'{indent}{T}{T}{T}default_format = "#high"')
    lines.append(f"{indent}{T}{T}{T}text = {_q(label_key)}")
    lines.append(f"{indent}{T}{T}}}")
    lines.append(f"{indent}{T}{T}expand = {{}}")
    lines.append(f"{indent}{T}}}")
    lines.append(f"{indent}}}")


def _mock_demands(lines: list[str], indent: str) -> None:
    """One demand row per estate: the estate icon, the panel's own demand line, three answers.

    The demand text is the shipped slot-1 wording for each estate, so the player reads the same
    sentence here as in the panel. Which of the shipped variants a live city would roll is not
    known offline, so the first one stands as the example.
    """
    for estate, demand_key in (
        ("nobles_estate", "TV_ENGINEERING_DEMAND_NOBLES_1"),
        ("burghers_estate", "TV_ENGINEERING_DEMAND_BURGHERS_1"),
        ("clergy_estate", "TV_ENGINEERING_DEMAND_CLERGY_1"),
    ):
        lines.append(f"{indent}widget = {{")
        lines.append(f"{indent}{T}minimumsize = {{ 560 44 }}")
        lines.append(f"{indent}{T}maximumsize = {{ 560 44 }}")
        lines.append(f"{indent}{T}using = bg_text_mask_container_dark_blue")
        lines.append(f"{indent}{T}hbox = {{")
        lines.append(f"{indent}{T}{T}layoutpolicy_horizontal = expanding")
        lines.append(f"{indent}{T}{T}margin = {{ 6 4 }}")
        lines.append(f"{indent}{T}{T}spacing = 6")
        lines.append(f"{indent}{T}{T}text_single = {{")
        lines.append(f"{indent}{T}{T}{T}size = {{ 26 22 }}")
        lines.append(f"{indent}{T}{T}{T}align = center|nobaseline")
        lines.append(f"{indent}{T}{T}{T}fontsize = 15")
        lines.append(f"{indent}{T}{T}{T}raw_text = {_q(f'[ShowEstateTypeName({estate!r})]')}")
        lines.append(f"{indent}{T}{T}}}")
        lines.append(f"{indent}{T}{T}text_multi = {{")
        lines.append(f"{indent}{T}{T}{T}min_width = 380")
        lines.append(f"{indent}{T}{T}{T}max_width = 380")
        lines.append(f"{indent}{T}{T}{T}autoresize = yes")
        lines.append(f"{indent}{T}{T}{T}fontsize = 12")
        lines.append(f"{indent}{T}{T}{T}text = {_q(demand_key)}")
        lines.append(f"{indent}{T}{T}}}")
        for colour, texture in (("green", "trigger_yes"), ("red", "trigger_no"), ("yellow", "gold")):
            style = f"tv_eu_mock_button_{colour}"
            lines.append(f"{indent}{T}{T}widget = {{")
            lines.append(f"{indent}{T}{T}{T}size = {{ 28 24 }}")
            lines.append(f"{indent}{T}{T}{T}{style} = {{")
            lines.append(f'{indent}{T}{T}{T}{T}blockoverride "mock_text" {{ raw_text = "@{texture}!" }}')
            lines.append(f"{indent}{T}{T}{T}}}")
            lines.append(f"{indent}{T}{T}}}")
        lines.append(f"{indent}{T}}}")
        lines.append(f"{indent}}}")


def _mock_triplet(lines: list[str], indent: str) -> None:
    """The survey's three readings, as three compact competence bars."""
    for label_key, value, caption in (
        ("TV_ENGINEERING_SCALE_COMPETENCE_LABEL", 70, "TV_ENGINEERING_SURVEY_SCALE_EFFECT_LABEL"),
        ("TV_ENGINEERING_ORGANIZATION_COMPETENCE_LABEL", 65, "TV_ENGINEERING_SURVEY_ORGANIZATION_EFFECT_LABEL"),
        ("TV_ENGINEERING_LOGISTICS_COMPETENCE_LABEL", 55, "TV_ENGINEERING_SURVEY_LOGISTICS_EFFECT_LABEL"),
    ):
        _mock_bar(lines, ("bar", label_key, value, f"{value}%"), indent)
        lines.append(f"{indent}text_single = {{")
        lines.append(f"{indent}{T}size = {{ 560 16 }}")
        lines.append(f"{indent}{T}autoresize = yes")
        lines.append(f"{indent}{T}fontsize = 12")
        lines.append(f'{indent}{T}default_format = "#weak"')
        lines.append(f"{indent}{T}text = {_q(caption)}")
        lines.append(f"{indent}}}")


def _mock_stats_goods(lines: list[str], indent: str) -> None:
    """The input goods table: a header row, then two goods with price and demand over supply."""
    def header(cell_key: str, width: int, align: str) -> None:
        lines.append(f"{indent}text_single = {{")
        lines.append(f"{indent}{T}size = {{ {width} 16 }}")
        lines.append(f"{indent}{T}align = {align}|nobaseline")
        lines.append(f"{indent}{T}autoresize = yes")
        lines.append(f"{indent}{T}fontsize = 11")
        lines.append(f'{indent}{T}default_format = "#weak"')
        lines.append(f"{indent}{T}text = {_q(cell_key)}")
        lines.append(f"{indent}}}")

    lines.append(f"{indent}hbox = {{")
    lines.append(f"{indent}{T}layoutpolicy_horizontal = expanding")
    lines.append(f"{indent}{T}spacing = 8")
    lines.append(f"{indent}{T}size = {{ -1 16 }}")
    header("TV_OL_INPUT_GOODS", 196, "left")
    header("TV_OL_LOCAL_PRICE", 120, "right")
    header("TV_OL_DEMAND_SUPPLY", 176, "right")
    lines.append(f"{indent}}}")
    for goods, price, demand_supply in (
        ("tools", "1.35 @gold!", "#R 150.0 / 120.0#!"),
        ("tv_wonder_materials", "6.20 @gold!", "#R 140.0 / 117.6#!"),
    ):
        lines.append(f"{indent}hbox = {{")
        lines.append(f"{indent}{T}layoutpolicy_horizontal = expanding")
        lines.append(f"{indent}{T}spacing = 8")
        lines.append(f"{indent}{T}size = {{ -1 26 }}")
        lines.append(f"{indent}{T}icon = {{ size = {{ 26 26 }} texture = \"{MOCK_ICON_ESTATE}\" }}")
        lines.append(f"{indent}{T}text_single = {{")
        lines.append(f"{indent}{T}{T}layoutpolicy_horizontal = expanding")
        lines.append(f"{indent}{T}{T}autoresize = yes")
        lines.append(f"{indent}{T}{T}raw_text = {_q(f'[ShowGoodsName({goods!r})]')}")
        lines.append(f"{indent}{T}}}")
        lines.append(f"{indent}{T}text_single = {{")
        lines.append(f"{indent}{T}{T}size = {{ 110 26 }}")
        lines.append(f"{indent}{T}{T}align = right|nobaseline")
        lines.append(f"{indent}{T}{T}autoresize = yes")
        lines.append(f"{indent}{T}{T}raw_text = {_q(price)}")
        lines.append(f"{indent}{T}}}")
        lines.append(f"{indent}{T}text_single = {{")
        lines.append(f"{indent}{T}{T}size = {{ 150 26 }}")
        lines.append(f"{indent}{T}{T}align = right|nobaseline")
        lines.append(f"{indent}{T}{T}autoresize = yes")
        lines.append(f"{indent}{T}{T}raw_text = {_q(demand_supply)}")
        lines.append(f"{indent}{T}}}")
        lines.append(f"{indent}}}")


def _mock_equation(lines: list[str], indent: str) -> None:
    """The monthly settlement sum, in the panel's own words, with sample figures."""
    lines.append(f"{indent}widget = {{")
    lines.append(f"{indent}{T}minimumsize = {{ 560 30 }}")
    lines.append(f"{indent}{T}maximumsize = {{ 560 30 }}")
    lines.append(f"{indent}{T}using = bg_text_mask_container_dark_blue")
    lines.append(f"{indent}{T}text_single = {{")
    lines.append(f"{indent}{T}{T}size = {{ 100% 100% }}")
    lines.append(f"{indent}{T}{T}align = center|nobaseline")
    lines.append(f"{indent}{T}{T}autoresize = no")
    lines.append(f"{indent}{T}{T}text = \"TV_OL_CHAIN\"")
    lines.append(f"{indent}{T}}}")
    lines.append(f"{indent}}}")
    _mock_stats(lines, [("TV_OL_BASE_PROGRESS", "6020 /mo"),
                        ("TV_OL_INPUT", "82%"),
                        ("TV_OL_LOG_FACTOR", "98%"),
                        ("TV_OL_RESULT", "4837 /mo")], indent)


def _mock_parts(lines: list[str], indent: str) -> None:
    """The four construction parts, each a row of unit pips: finished, active, waiting."""
    rows = (
        ("TV_ENGINEERING_CONSTRUCTION_PART_FOUNDATION", (3, 3, 3, 3, 3, 3)),
        ("TV_ENGINEERING_CONSTRUCTION_PART_BODY", (2, 2, 2, 2, 1, 0)),
        ("TV_ENGINEERING_CONSTRUCTION_PART_FUNCTION", (1, 1, 0, 0, 0, 0)),
        ("TV_ENGINEERING_CONSTRUCTION_PART_DECORATION", (1, 0, 0, 0, 0, 0)),
    )
    for label_key, units in rows:
        lines.append(f"{indent}hbox = {{")
        lines.append(f"{indent}{T}layoutpolicy_horizontal = expanding")
        lines.append(f"{indent}{T}spacing = 6")
        lines.append(f"{indent}{T}size = {{ -1 28 }}")
        lines.append(f"{indent}{T}text_single = {{")
        lines.append(f"{indent}{T}{T}size = {{ 96 28 }}")
        lines.append(f"{indent}{T}{T}autoresize = yes")
        lines.append(f"{indent}{T}{T}text = {_q(label_key)}")
        lines.append(f"{indent}{T}}}")
        lines.append(f"{indent}{T}tv_eu_mock_pips = {{")
        lines.append(f'{indent}{T}{T}blockoverride "mock_pips" {{')
        lines.append(f"{indent}{T}{T}{T}hbox = {{")
        lines.append(f"{indent}{T}{T}{T}{T}spacing = 4")
        for number, state in enumerate(units, start=1):
            texture = "button_regular_texture_alt_green" if state == 3 else (
                "button_regular_texture_alt_yellow" if state == 2 else (
                    "button_regular_texture_alt_red" if state == 1 else "button_regular_texture"))
            lines.append(f"{indent}{T}{T}{T}{T}widget = {{")
            lines.append(f"{indent}{T}{T}{T}{T}{T}size = {{ 30 26 }}")
            lines.append(f"{indent}{T}{T}{T}{T}{T}using = {texture}")
            lines.append(f"{indent}{T}{T}{T}{T}{T}text_single = {{")
            lines.append(f"{indent}{T}{T}{T}{T}{T}{T}size = {{ 100% 100% }}")
            lines.append(f"{indent}{T}{T}{T}{T}{T}{T}align = center|nobaseline")
            lines.append(f"{indent}{T}{T}{T}{T}{T}{T}autoresize = no")
            lines.append(f"{indent}{T}{T}{T}{T}{T}{T}fontsize = 12")
            lines.append(f"{indent}{T}{T}{T}{T}{T}{T}raw_text = \"{number}\"")
            lines.append(f"{indent}{T}{T}{T}{T}{T}}}")
            lines.append(f"{indent}{T}{T}{T}{T}}}")
        lines.append(f"{indent}{T}{T}{T}}}")
        lines.append(f"{indent}{T}{T}}}")
        lines.append(f"{indent}{T}}}")
        lines.append(f"{indent}}}")


def _mock_styles(lines: list[str], labels: list[str], indent: str) -> None:
    """The ceremony style picker: one wide row per style, the first one previewed."""
    for position, label_key in enumerate(labels):
        _mock_button(lines, label_key, "yellow" if position == 0 else None, indent, 438, 36)


def render_mock(lines: list[str], mock, indent: str) -> None:
    """Draw one control imitation. The tuple's first element names the shape."""
    if mock is None:
        return
    kind = mock[0]
    if kind == "button":
        _mock_buttons(lines, [(mock[1], mock[2])], indent)
    elif kind == "buttons":
        _mock_buttons(lines, mock[1], indent)
    elif kind == "bar":
        _mock_bar(lines, mock, indent)
    elif kind == "status":
        _mock_status(lines, mock[1], indent)
    elif kind == "portrait":
        _mock_portrait(lines, mock[1], indent)
    elif kind == "pills":
        _mock_pills(lines, mock[1], mock[2], indent)
    elif kind == "demands":
        _mock_demands(lines, indent)
    elif kind == "triplet":
        _mock_triplet(lines, indent)
    elif kind == "stats":
        _mock_stats(lines, [("TV_OL_BASE_PROGRESS", "7000 /mo"),
                            ("TV_OL_EMPLOYMENT", "12040 / 14000"),
                            ("TV_OL_CAMP_PROGRESS", "6020 /mo"),
                            ("TV_OL_MAINTENANCE", "1172.50 @gold!")], indent)
    elif kind == "stats_goods":
        _mock_stats_goods(lines, indent)
    elif kind == "equation":
        _mock_equation(lines, indent)
    elif kind == "parts":
        _mock_parts(lines, indent)
    elif kind == "stat":
        _mock_stats(lines, [(mock[1], mock[2]), (mock[3], mock[4])], indent)
    elif kind == "styles":
        _mock_styles(lines, mock[1], indent)
    else:  # pragma: no cover - content mistake, fail loudly instead of drawing nothing
        raise ValueError(f"Unknown anatomy mock {kind!r}")


def render_anatomy_section(lines: list[str], loc: dict[str, tuple[str, str]],
                           cid: str, index: int, section: dict, heading_key: str) -> None:
    """One teaching step: the heading, a full-width paragraph, then numbered anatomy rows.

    The paragraph sits above the panel rather than beside it, so both the text and the controls
    get the whole 1370 body width. Each row is a number, a real control imitation, and the one
    sentence that explains it, in the order a player meets them on screen.
    """
    prefix = key(cid, f"s{index}")
    body_key = prefix + "_BODY"
    loc[body_key] = section["body"]
    # The mock's header repeats the shipped card title, the same words the player sees there.
    panel_title_key = ANATOMY_PANEL_TITLES[section["anatomy"]]

    lines.append(f'vbox = {{ name = "tv_eu_{cid}_guide_{index - 1}"')
    lines.append('minimumsize = { 1450 -1 } maximumsize = { 1450 -1 } layoutpolicy_horizontal = expanding spacing = 10')
    section_heading(lines, section["icon"], heading_key)
    body_text(lines, body_key, width=1370)

    lines.append("tv_eu_anatomy = {")
    lines.append(f'{T}blockoverride "anatomy_header_icon" {{ texture = {_q(section["icon"])} }}')
    lines.append(f'{T}blockoverride "anatomy_title" {{ text = {_q(panel_title_key)} }}')
    lines.append(f'{T}blockoverride "anatomy_rows" {{')
    lines.append(f"{T}{T}vbox = {{")
    lines.append(f"{T}{T}{T}layoutpolicy_horizontal = expanding")
    lines.append(f"{T}{T}{T}spacing = 10")
    for row_number, row in enumerate(section["rows"], start=1):
        row_prefix = f"{prefix}_R{row_number}"
        title_key = row_prefix + "_TITLE"
        text_key = row_prefix + "_TEXT"
        loc[title_key] = row["title"]
        loc[text_key] = row["text"]
        lines.append(f"{T}{T}{T}tv_eu_anatomy_row = {{")
        if row_number == len(section["rows"]):
            # The row type carries a bottom margin for the gap between rows; on the last row it
            # would sit outside the panel and clip the note against the paper edge.
            lines.append(f"{T}{T}{T}{T}margin_bottom = 0")
        lines.append(f'{T}{T}{T}{T}blockoverride "row_number" {{ raw_text = "{row_number}" }}')
        lines.append(f'{T}{T}{T}{T}blockoverride "row_control" {{')
        lines.append(f"{T}{T}{T}{T}{T}vbox = {{")
        lines.append(f"{T}{T}{T}{T}{T}{T}layoutpolicy_horizontal = expanding")
        lines.append(f"{T}{T}{T}{T}{T}{T}spacing = 4")
        render_mock(lines, row.get("mock"), f"{T}{T}{T}{T}{T}{T}")
        lines.append(f"{T}{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}{T}}}")
        lines.append(f'{T}{T}{T}{T}blockoverride "row_note" {{')
        lines.append(f"{T}{T}{T}{T}{T}vbox = {{")
        lines.append(f"{T}{T}{T}{T}{T}{T}spacing = 3")
        lines.append(f"{T}{T}{T}{T}{T}{T}text_single = {{")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}layoutpolicy_horizontal = expanding")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}autoresize = yes")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}using = Font_Type_Headers")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}fontsize = 16")
        lines.append(f'{T}{T}{T}{T}{T}{T}{T}default_format = "#yellow_titles"')
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}text = {_q(title_key)}")
        lines.append(f"{T}{T}{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}{T}{T}{T}text_multi = {{")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}min_width = 700")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}max_width = 700")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}autoresize = yes")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}text = {_q(text_key)}")
        lines.append(f"{T}{T}{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}}}")
    lines.append(f"{T}{T}}}")
    lines.append(f"{T}}}")
    lines.append("}")
    lines.append("}")


def render_guide_section(lines: list[str], loc: dict[str, tuple[str, str]],
                         cid: str, index: int, section: dict, heading_key: str) -> None:
    """Getting Started steps are anatomy blocks; the shared dispatcher lives in the card."""
    render_anatomy_section(lines, loc, cid, index, section, heading_key)


def render_content_card(card: dict) -> tuple[list[str], dict[str, tuple[str, str]]]:
    """One hand-authored card. Returns its GUI lines and its localization entries."""
    lines: list[str] = []
    loc: dict[str, tuple[str, str]] = {}
    cid = card["id"]

    title_key = key(cid, "title")
    lead_key = key(cid, "lead")
    loc[title_key] = card["title"]
    loc[lead_key] = card["lead"]

    card_open(lines, card["filter"])
    card_header(lines, card["icon"], title_key)
    lines.append("")
    lines.append(f"{T}{T}{T}tv_eu_lead = {{ text = {_q(lead_key)} }}")

    for index, section in enumerate(card.get("sections", []), start=1):
        heading_key = key(cid, f"s{index}", "title")
        loc[heading_key] = section["title"]
        lines.append("")
        kind = section["kind"]
        if kind == "guide":
            render_guide_section(lines, loc, cid, index, section, heading_key)
            continue
        section_heading(lines, section.get("icon", ICON_SECTION), heading_key)

        if kind == "text":
            body_key = key(cid, f"s{index}", "body")
            loc[body_key] = section["body"]
            body_text(lines, body_key)

        elif kind == "cycle":
            # The stage cards and baked connectors share fixed geometry so the circular route
            # remains aligned at every language and resolution.
            positions = step_positions(len(section["steps"]))
            # `widget` resolves to an uberwidget in the game and rejects `margin`; keep the
            # spacing on a normal layout container and let the fixed-size child stay unchanged.
            lines.append(f'{T*3}hbox = {{')
            lines.append(f'{T*4}margin = {{ 40 0 }}')
            lines.append(f'{T*4}widget = {{')
            lines.append(f'{T*4}name = "tv_eu_{cid}_cycle"')
            lines.append(f'{T*4}size = {{ {CYCLE_SIZE[0]} {CYCLE_SIZE[1]} }}')
            lines.append(f'{T*4}icon = {{ size = {{ {CYCLE_SIZE[0]} {CYCLE_SIZE[1]} }} texture = {_q(TEXTURE)} alwaystransparent = yes }}')
            lines.append(f'{T*4}text_single = {{')
            lines.append(f'{T*5}position = {{ {CYCLE_CENTER[0] - 120} {CYCLE_CENTER[1] - 20} }}')
            lines.append(f'{T*5}size = {{ 240 40 }}')
            lines.append(f'{T*5}autoresize = no align = center')
            lines.append(f'{T*5}using = Font_Type_Headers fontsize = 26')
            lines.append(f'{T*5}default_format = "#yellow_titles" text = {_q(title_key)}')
            lines.append(f'{T*4}}}')
            for step_index, step in enumerate(section["steps"], start=1):
                step_title = key(cid, f"s{index}", f"p{step_index}", "title")
                step_text = key(cid, f"s{index}", f"p{step_index}", "text")
                loc[step_title] = step["title"]
                loc[step_text] = step["text"]
                x, y = positions[step_index - 1]
                lines.append(f'{T*4}tv_eu_cycle_step = {{')
                lines.append(f'{T*5}name = "tv_eu_{cid}_cycle_step_{step_index}"')
                lines.append(f'{T*5}position = {{ {x} {y} }}')
                lines.append(f'{T*5}size = {{ {STEP_SIZE[0]} {STEP_SIZE[1]} }}')
                lines.append(f'{T*5}blockoverride "step_icon" {{ texture = {_q(step["icon"])} }}')
                lines.append(f'{T*5}blockoverride "step_link" {{ raw_text = {_q(step.get("link") or "")} }}')
                lines.append(f'{T*5}blockoverride "step_title" {{ text = {_q(step_title)} }}')
                lines.append(f'{T*5}blockoverride "step_text" {{ text = {_q(step_text)} }}')
                lines.append(f'{T*4}}}')
            lines.append(f'{T*4}}}')
            lines.append(f'{T*3}}}')
            body_key = key(cid, f"s{index}", "note")
            if section.get("note"):
                loc[body_key] = section["note"]
                body_text(lines, body_key, width=1370)

        elif kind == "flow":
            # Match tv_eu_card's 1450 width, the row's 40px side margins,
            # 30px arrows and two 8px gaps per arrow. Narrow longer linear
            # flows because the style's default 305px step only fits four.
            step_count = len(section["steps"])
            step_width = min(305, (1450 - 2 * 40 - (step_count - 1) * (30 + 2 * 8)) // step_count)
            text_width = step_width - 2 * 14
            lines.append(f"{T}{T}{T}hbox = {{")
            lines.append(f"{T}{T}{T}{T}margin = {{ 40 0 }}")
            lines.append(f"{T}{T}{T}{T}spacing = 8")
            for step_index, step in enumerate(section["steps"], start=1):
                step_title = key(cid, f"s{index}", f"p{step_index}", "title")
                step_text = key(cid, f"s{index}", f"p{step_index}", "text")
                loc[step_title] = step["title"]
                loc[step_text] = step["text"]
                lines.append("")
                lines.append(f"{T}{T}{T}{T}tv_eu_step = {{")
                lines.append(f"{T}{T}{T}{T}{T}minimumsize = {{ {step_width} 236 }}")
                lines.append(f"{T}{T}{T}{T}{T}maximumsize = {{ {step_width} -1 }}")
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "step_icon" {{ texture = {_q(step["icon"])} }}')
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "step_link" {{ tv_eu_link = {{ min_width = {text_width} max_width = {text_width} raw_text = {_q(step.get("link") or "")} }} }}')
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "step_title" {{ text = {_q(step_title)} }}')
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "step_text" {{ min_width = {text_width} max_width = {text_width} text = {_q(step_text)} }}')
                lines.append(f"{T}{T}{T}{T}}}")
                if step_index < len(section["steps"]):
                    lines.append(f"{T}{T}{T}{T}tv_eu_arrow = {{}}")
            lines.append(f"{T}{T}{T}}}")
            if section.get("body"):
                body_key = key(cid, f"s{index}", "body")
                loc[body_key] = section["body"]
                body_text(lines, body_key)

        elif kind == "scale":
            lines.append(f"{T}{T}{T}hbox = {{")
            lines.append(f"{T}{T}{T}{T}margin = {{ 40 0 }}")
            lines.append(f"{T}{T}{T}{T}spacing = 10")
            for step_index, step in enumerate(section["steps"], start=1):
                label_key = key(cid, f"s{index}", f"k{step_index}")
                loc[label_key] = step["label"]
                lines.append("")
                lines.append(f"{T}{T}{T}{T}tv_eu_scale_step = {{")
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "medallion" {{')
                _medallion(lines, step["medallion"])
                lines.append(f"{T}{T}{T}{T}{T}}}")
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "scale_label" {{ text = {_q(label_key)} }}')
                lines.append(f"{T}{T}{T}{T}}}")
            lines.append(f"{T}{T}{T}}}")
            if section.get("body"):
                body_key = key(cid, f"s{index}", "body")
                loc[body_key] = section["body"]
                body_text(lines, body_key)

        elif kind == "panels":
            sign_key = key(cid, f"s{index}", "sign")
            # Three styles necessarily disagree, so "or" is the honest default separator.
            loc[sign_key] = section.get("sign", ("or", "或"))
            lines.append(f"{T}{T}{T}hbox = {{")
            lines.append(f"{T}{T}{T}{T}margin = {{ 40 0 }}")
            lines.append(f"{T}{T}{T}{T}spacing = 8")
            for panel_index, panel in enumerate(section["panels"], start=1):
                panel_title = key(cid, f"s{index}", f"a{panel_index}", "title")
                panel_text = key(cid, f"s{index}", f"a{panel_index}", "text")
                loc[panel_title] = panel["title"]
                loc[panel_text] = panel["text"]
                lines.append("")
                lines.append(f"{T}{T}{T}{T}tv_eu_panel = {{")
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "panel_icons" {{')
                lines.append(f"{T}{T}{T}{T}{T}{T}hbox = {{")
                lines.append(f"{T}{T}{T}{T}{T}{T}{T}spacing = 10")
                items = panel.get("items", [])
                for item_index, item in enumerate(items):
                    _panel_item(lines, item)
                    if panel.get("arrows") and item_index < len(items) - 1:
                        lines.append(f"{T}{T}{T}{T}{T}{T}{T}tv_eu_item_arrow = {{}}")
                lines.append(f"{T}{T}{T}{T}{T}{T}}}")
                lines.append(f"{T}{T}{T}{T}{T}}}")
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "panel_title" {{ text = {_q(panel_title)} }}')
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "panel_text" {{ text = {_q(panel_text)} }}')
                lines.append(f"{T}{T}{T}{T}}}")
                if panel_index < len(section["panels"]):
                    lines.append(f"{T}{T}{T}{T}tv_eu_sign = {{")
                    lines.append(f'{T}{T}{T}{T}{T}blockoverride "sign_text" {{ text = {_q(sign_key)} }}')
                    lines.append(f"{T}{T}{T}{T}}}")
            lines.append(f"{T}{T}{T}}}")

        elif kind == "entries":
            if section.get("body"):
                body_key = key(cid, f"s{index}", "body")
                loc[body_key] = section["body"]
                body_text(lines, body_key)
            lines.append(f"{T}{T}{T}vbox = {{")
            lines.append(f"{T}{T}{T}{T}margin = {{ 40 0 }}")
            lines.append(f"{T}{T}{T}{T}spacing = 8")
            for entry_index, entry in enumerate(section["entries"], start=1):
                entry_title = key(cid, f"s{index}", f"e{entry_index}", "title")
                entry_text = key(cid, f"s{index}", f"e{entry_index}", "text")
                loc[entry_title] = entry["title"]
                loc[entry_text] = entry["text"]
                lines.append("")
                lines.append(f"{T}{T}{T}{T}tv_eu_entry = {{")
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "entry_icons" {{')
                _entry_icons(lines, entry["icons"])
                lines.append(f"{T}{T}{T}{T}{T}}}")
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "entry_title" {{ text = {_q(entry_title)} }}')
                lines.append(f'{T}{T}{T}{T}{T}blockoverride "entry_text" {{ text = {_q(entry_text)} }}')
                lines.append(f"{T}{T}{T}{T}}}")
            lines.append(f"{T}{T}{T}}}")

        else:  # pragma: no cover
            raise ValueError(f"Unknown section kind {kind!r} in card {cid}")

    card_close(lines)
    return lines, loc


# ----------------------------------------------------------------------- wonder cards ----


# ------------------------------------------------------------------------- shared text ----


def shared_localization() -> dict[str, tuple[str, str]]:
    """Text every generated card and the filter row share."""
    filters = {
        "all": ("All", "全部"),
        "overview": ("Getting Started", "入门"),
        "mechanics": ("Complete Mechanics", "完整机制"),
        "unique": ("Unique Projects", "独特工程"),
        "generic": ("Generic Projects", "通用工程"),
    }
    out: dict[str, tuple[str, str]] = {}
    for name, value in filters.items():
        out[key("filter", name)] = value
        out[key("filter", name, "tooltip")] = (
            f"Open the {value[0].lower()} tab.",
            f"打开{value[1]}页签。",
        )
    out[key("tab", "title")] = ("Great Projects", "伟大工程")
    return out


def select_wonder_cards(wonders: list[dict]) -> list[dict]:
    """Resolve the two approved examples, in editorial order, from live data."""
    selected = []
    for key in WONDER_CARD_KEYS:
        matches = [wonder for wonder in wonders if wonder["key"] == key]
        if len(matches) != 1:
            raise ValueError(f"Europedia requires exactly one wonder with key {key}")
        selected.append(matches[0])
    return selected


def render_all(wonders: list[dict], mechanics: dict) -> dict:
    """Build teaching cards and all approved static catalogue entries."""
    gui: list[str] = [
        "vbox = {",
        f"{T}using = layoutpolicy_expanding",
        f"{T}set_parent_dimension_to_minimum = height",
        f"{T}spacing = 4",
        "",
    ]
    loc_en: dict[str, str] = {}
    loc_zh: dict[str, str] = {}

    def merge(pairs: dict[str, tuple[str, str]]) -> None:
        for localization_key, (english, chinese) in pairs.items():
            if localization_key in loc_en:
                raise KeyError(f"Duplicate Europedia localization key {localization_key}")
            loc_en[localization_key] = english
            loc_zh[localization_key] = chinese

    for card in CARDS:
        lines, card_loc = render_content_card(card)
        gui.extend(lines)
        gui.append("")
        merge(card_loc)

    catalogue = Catalogue()
    for wonder in select_wonder_cards(wonders):
        gui.append(f'vbox = {{ visible = {_q(visible_by_filter("mechanics"))} margin = {{ 0 10 }}')
        gui.extend(catalogue.entry(wonder, mechanics, instance='example'))
        gui.append('}')
    for category, unique in (('unique', True), ('generic', False)):
        gui.extend(catalogue.tab(category, [w for w in wonders if bool(w['is_unique']) == unique], mechanics))
    merge(catalogue.loc)

    gui.append("}")
    merge(shared_localization())
    return {"gui": gui, "loc_en": loc_en, "loc_zh": loc_zh}
