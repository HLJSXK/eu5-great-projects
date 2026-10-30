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


def body_text(lines: list[str], text_key: str) -> None:
    lines.append(f"{T}{T}{T}tv_eu_text = {{ text = {_q(text_key)} }}")


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
        section_heading(lines, section.get("icon", ICON_SECTION), heading_key)
        kind = section["kind"]

        if kind == "text":
            body_key = key(cid, f"s{index}", "body")
            loc[body_key] = section["body"]
            body_text(lines, body_key)

        elif kind == "cycle":
            # Reserve the complete circle in the card's content-driven vbox.
            # Native widgets and baked connectors share the same geometry.
            positions = step_positions(len(section["steps"]))
            lines.append(f'{T*3}widget = {{')
            lines.append(f'{T*4}name = "tv_eu_{cid}_cycle"')
            lines.append(f'{T*4}size = {{ {CYCLE_SIZE[0]} {CYCLE_SIZE[1]} }}')
            lines.append(f'{T*4}margin = {{ 40 0 }}')
            lines.append(f'{T*4}icon = {{ size = {{ {CYCLE_SIZE[0]} {CYCLE_SIZE[1]} }} texture = {_q(TEXTURE)} alwaystransparent = yes }}')
            lines.append(f'{T*4}text_single = {{')
            lines.append(f'{T*5}position = {{ {CYCLE_CENTER[0] - 120} {CYCLE_CENTER[1] - 20} }}')
            lines.append(f'{T*5}size = {{ 240 40 }}')
            lines.append(f'{T*5}autoresize = no')
            lines.append(f'{T*5}align = center')
            lines.append(f'{T*5}using = Font_Type_Headers')
            lines.append(f'{T*5}fontsize = 26')
            lines.append(f'{T*5}default_format = "#yellow_titles"')
            lines.append(f'{T*5}text = {_q(title_key)}')
            lines.append(f'{T*4}}}')
            for step_index, (step, (x, y)) in enumerate(zip(section["steps"], positions), start=1):
                step_title = key(cid, f"s{index}", f"p{step_index}", "title")
                step_text = key(cid, f"s{index}", f"p{step_index}", "text")
                loc[step_title] = step["title"]
                loc[step_text] = step["text"]
                lines.append(f'{T*4}tv_eu_cycle_step = {{')
                lines.append(f'{T*5}name = "tv_eu_{cid}_cycle_step_{step_index}"')
                lines.append(f'{T*5}position = {{ {x} {y} }}')
                lines.append(f'{T*5}size = {{ {STEP_SIZE[0]} {STEP_SIZE[1]} }}')
                lines.append(f'{T*5}blockoverride "step_icon" {{ texture = {_q(step["icon"])} }}')
                lines.append(f'{T*5}blockoverride "step_link" {{ raw_text = {_q(step.get("link") or "")} }}')
                lines.append(f'{T*5}blockoverride "step_title" {{ text = {_q(step_title)} }}')
                lines.append(f'{T*5}blockoverride "step_text" {{ text = {_q(step_text)} }}')
                lines.append(f'{T*4}}}')
            lines.append(f'{T*3}}}')

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
    out[key("tab", "title")] = ("Great Projects", "大工程")
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
