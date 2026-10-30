"""Render the Great Projects Europedia: card GUI lines and their localization.

Three thin generators consume this module, so a card's layout and its text can never drift
apart:

    in_game/gui/gen_tv_encyclopedia_wonders_cards_gui.py          -> data/generated_fragments/
    main_menu/localization/english/gen_tv_europedia_l_english.py  -> src/.../english/
    main_menu/localization/simp_chinese/gen_tv_europedia_l_simp_chinese.py

Card shapes come from in_game/gui/shared/tv_europedia_style.gui; prose and layout intent come
from europedia_content.py; wonder cards are built from the wonder data package so their
effects, dedications and estates are always the shipped ones.

Two rules this module exists to keep:

1. Ritual completion effects are shown with ShowScriptedEffectForScope, never as prose. The
   engine renders what the effect actually does; a hand-written summary would go stale.
2. Every number a card shows is read from the shipped data, never typed into it by hand.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "scripts_engineering_department") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from europedia_content import CARDS  # noqa: E402
from gen_europedia_cycle import CYCLE_SIZE, CYCLE_CENTER, STEP_SIZE, TEXTURE, step_positions  # noqa: E402
from wonder_mechanics.modifiers import (  # noqa: E402
    authored_final_building_local_modifiers,
    wonder_base_country_modifiers,
)
from wonder_mechanics.rituals import location_reward_estate, ritual_styles  # noqa: E402

T = "\t"
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}

FILTER_IDS = ("all", "overview", "mechanics", "unique", "generic")
PREFIX = "TV_EU"

# Permanent editorial scope: 15 mechanic cards and these two worked examples.
# Do not turn the complete wonder database into a static catalogue again.
# See docs/knowledge/risk_cards/europedia.md for the design and runtime evidence.
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


def wonder_loc_keys(concept: str) -> dict[str, str]:
    return {"name": f"game_concept_{concept}", "lead": f"game_concept_{concept}_desc"}


def _effect_row(lines: list[str], label_key: str, modifier: str) -> None:
    lines.append(f"{T}{T}{T}{T}vbox = {{")
    lines.append(f"{T}{T}{T}{T}{T}layoutpolicy_horizontal = expanding")
    lines.append(f"{T}{T}{T}{T}{T}spacing = 2")
    lines.append(f"{T}{T}{T}{T}{T}text_single = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}fontsize = 15")
    lines.append(f'{T}{T}{T}{T}{T}{T}default_format = "#high"')
    lines.append(f"{T}{T}{T}{T}{T}{T}autoresize = yes")
    lines.append(f"{T}{T}{T}{T}{T}{T}text = {_q(label_key)}")
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}{T}TooltipStringPairList = {{")
    lines.append(f"{T}{T}{T}{T}{T}{T}layoutpolicy_horizontal = expanding")
    lines.append(f"{T}{T}{T}{T}{T}{T}textcontext = \"[ShowModifierEffect('{modifier}')]\"")
    # Preserve the nested title slot and hide it in this non-tooltip panel.
    lines.append(f'{T}{T}{T}{T}{T}{T}blockoverride "bg_listbase" {{}}')
    lines.append(f'{T}{T}{T}{T}{T}{T}blockoverride "block_title" {{ block "block_title" {{ visible = no }} }}')
    lines.append(f"{T}{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}}}")


def _site_requirements(lines: list[str], wonder: dict) -> None:
    """The real siting rule, rendered by the engine against the player's capital.

    The trigger name is baked per card: the rule is a scripted trigger that already exists for
    this wonder, so asking the engine to print it keeps the card correct when the rule changes.
    """
    trigger = f"tv_wonder_display_{int(wonder['id'])}_base_site_rules_trigger"
    lines.append(f"{T}{T}{T}tv_eu_text = {{ text = {_q(key('wonder', 'site_example'))} }}")
    lines.append(f"{T}{T}{T}TooltipRequirementsList = {{")
    lines.append(f"{T}{T}{T}{T}layoutpolicy_horizontal = expanding")
    lines.append(f"{T}{T}{T}{T}textcontext = \"[ShowTriggerConditionsForScope('{trigger}', Player.GetCapital.MakeScope.Self)]\"")
    lines.append(f'{T}{T}{T}{T}blockoverride "field_text_format" {{ fontsize = 14 }}')
    lines.append(f'{T}{T}{T}{T}blockoverride "bg_listbase" {{}}')
    lines.append(f'{T}{T}{T}{T}blockoverride "block_title" {{')
    lines.append(f'{T}{T}{T}{T}{T}block "block_title" {{ visible = no }}')
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}}}")


def append_card(
    lines: list[str],
    *,
    category: str,
    texture: str,
    title_key: str,
    body_key: str,
    wonder: dict | None = None,
    mechanics: dict | None = None,
) -> None:
    """Emit one wonder card.

    Kept signature-compatible with the previous generator so the ritual regression test can
    call it directly; what changed is the card itself, not the way a wonder is handed in.
    """
    card_open(lines, category)
    card_header(lines, texture, title_key)
    lines.append("")
    lines.append(f"{T}{T}{T}tv_eu_lead = {{ text = {_q(body_key)} }}")

    if wonder is None or mechanics is None:  # a title and a paragraph, nothing else
        card_close(lines)
        return

    wid = int(wonder["id"])
    unique = bool(wonder.get("is_unique"))

    # --- at a glance -------------------------------------------------------------------
    lines.append("")
    section_heading(lines, ICON_SIZE, key("wonder", "glance"))
    lines.append(f"{T}{T}{T}hbox = {{")
    lines.append(f"{T}{T}{T}{T}margin = {{ 40 0 }}")
    lines.append(f"{T}{T}{T}{T}spacing = 10")
    lines.append(f"{T}{T}{T}{T}tv_eu_item = {{")
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_icon" {{ texture = {_q(ICON_SIZE)} }}')
    size_link = "[tv_wonder_{}|e]".format(wonder["size"])
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_link" {{ raw_text = {_q(size_link)} }}')
    lines.append(f"{T}{T}{T}{T}}}")
    pop_type = wonder.get("pop_type", "laborers")
    lines.append(f"{T}{T}{T}{T}tv_eu_item = {{")
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_icon" {{ texture = "gfx/interface/icons/pops/{pop_type}.dds" }}')
    pop_link = "[ShowPopTypeName('{}')]".format(pop_type)
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_link" {{ raw_text = {_q(pop_link)} }}')
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}tv_eu_item = {{")
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_icon" {{ texture = {_q(ICON_CATEGORY)} }}')
    category_link = "[ShowBuildingCategoryName('{}')]".format(wonder["category"])
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_link" {{ raw_text = {_q(category_link)} }}')
    lines.append(f"{T}{T}{T}{T}}}")
    if unique and wonder.get("location"):
        lines.append(f"{T}{T}{T}{T}tv_eu_item = {{")
        lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_icon" {{ texture = {_q(ICON_SITE)} }}')
        location_link = "[ShowLocationName('{}')]".format(wonder["location"])
        lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_link" {{ raw_text = {_q(location_link)} }}')
        lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}}}")
    body_text(lines, key("wonder", "glance_text"))

    # --- what the levels give ----------------------------------------------------------
    # Some wonders carry only country effects, some only local ones, and a few neither. A row
    # is emitted only when the modifier behind it has something to show: an empty
    # ShowModifierEffect would draw an empty list rather than stay hidden.
    has_country = bool(wonder_base_country_modifiers(wonder, mechanics, 1))
    has_local = bool(authored_final_building_local_modifiers(wonder, mechanics))
    if has_country or has_local:
        lines.append("")
        section_heading(lines, ICON_EFFECT, key("wonder", "effects"))
        body_text(lines, key("wonder", "effects_note"))
        lines.append(f"{T}{T}{T}hbox = {{")
        lines.append(f"{T}{T}{T}{T}margin = {{ 40 0 }}")
        lines.append(f"{T}{T}{T}{T}spacing = 30")
        if has_country:
            _effect_row(lines, key("wonder", "effects_country_1"), f"tv_wonder_display_{wid}_level_1")
            _effect_row(lines, key("wonder", "effects_country_6"), f"tv_wonder_display_{wid}_level_6")
        if has_local:
            _effect_row(lines, key("wonder", "effects_local_6"), f"tv_wonder_display_{wid}_local_level_6")
        lines.append(f"{T}{T}{T}}}")

    # --- where it can stand ------------------------------------------------------------
    lines.append("")
    section_heading(lines, ICON_SITE, key("wonder", "site"))
    body_text(lines, key("wonder", "site_unique" if unique else "site_generic"))
    if not unique:
        _site_requirements(lines, wonder)

    # --- the three dedications ---------------------------------------------------------
    rows = ritual_styles(wonder, mechanics)
    lines.append("")
    section_heading(lines, ICON_RITUAL, key("wonder", "rituals"))
    body_text(lines, key("wonder", "rituals_note"))
    lines.append(f"{T}{T}{T}hbox = {{")
    lines.append(f"{T}{T}{T}{T}margin = {{ 40 0 }}")
    lines.append(f"{T}{T}{T}{T}spacing = 10")
    for row in rows:
        axis = row["societal_value"]
        side = "left" if axis["sign"] < 0 else "right"
        catalogue = f"tv_wonder_display_{wid}_ritual_{row['style']}_catalogue_effect"
        lines.append("")
        lines.append(f"{T}{T}{T}{T}tv_eu_choice = {{")
        lines.append(f'{T}{T}{T}{T}{T}blockoverride "choice_icon" {{')
        lines.append(f'{T}{T}{T}{T}{T}{T}texture = "gfx/interface/icons/societal_values/{axis["axis"]}_{side}.dds"')
        lines.append(f"{T}{T}{T}{T}{T}}}")
        lines.append(f'{T}{T}{T}{T}{T}blockoverride "choice_title" {{ text = {_q(row["name_key"])} }}')
        lines.append(f'{T}{T}{T}{T}{T}blockoverride "choice_text" {{ text = {_q(row["desc_key"])} }}')
        lines.append(f'{T}{T}{T}{T}{T}blockoverride "choice_extra" {{')
        lines.append(f"{T}{T}{T}{T}{T}{T}vbox = {{")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}spacing = 4")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}text_multi = {{")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}{T}max_width = 408")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}{T}min_width = 408")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}{T}autoresize = yes")
        preview = f"[ShowScriptedEffectForScope('{catalogue}', Player.MakeScope.Self)]"
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}{T}raw_text = {_q(preview)}")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}text_multi = {{")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}{T}max_width = 408")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}{T}min_width = 408")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}{T}autoresize = yes")
        direction_link = "[ShowSocietyDirectionName('{}')]".format(axis["direction"])
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}{T}raw_text = {_q(direction_link)}")
        lines.append(f"{T}{T}{T}{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}{T}{T}}}")
        lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}}}")
    body_text(lines, f"TV_WONDER_RITUAL_ESTATE_PREFS_{wid}")

    # --- who gains ---------------------------------------------------------------------
    lines.append("")
    section_heading(lines, ICON_ESTATE, key("wonder", "standing"))
    body_text(lines, key("wonder", "standing_unique" if unique else "standing_generic"))
    reward_estate = location_reward_estate(wonder).removesuffix("_estate")
    lines.append(f"{T}{T}{T}hbox = {{")
    lines.append(f"{T}{T}{T}{T}margin = {{ 40 0 }}")
    lines.append(f"{T}{T}{T}{T}spacing = 10")
    lines.append(f"{T}{T}{T}{T}tv_eu_item = {{")
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_icon" {{ texture = "gfx/interface/icons/estates/{reward_estate}_estate.dds" }}')
    estate_link = "[ShowEstateTypeName('{}')]".format(reward_estate + "_estate")
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_link" {{ raw_text = {_q(estate_link)} }}')
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}{T}tv_eu_item = {{")
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_icon" {{ texture = {_q(ICON_EFFECT)} }}')
    lines.append(f'{T}{T}{T}{T}{T}blockoverride "item_link" {{ raw_text = {_q(key("wonder", "standing_reward"))} }}')
    lines.append(f"{T}{T}{T}{T}}}")
    lines.append(f"{T}{T}{T}}}")

    card_close(lines)


def append_wonder_card(lines: list[str], wonder: dict, mechanics: dict, texture: str) -> None:
    keys = wonder_loc_keys(wonder["concept"])
    append_card(
        lines,
        category="mechanics",
        texture=texture,
        title_key=keys["name"],
        body_key=keys["lead"],
        wonder=wonder,
        mechanics=mechanics,
    )


# ------------------------------------------------------------------------- shared text ----


def shared_localization() -> dict[str, tuple[str, str]]:
    """Text every generated card and the filter row share."""
    wonder = {
        "glance": ("At a Glance", "一览"),
        "glance_text": (
            "Size fixes the ritual price and how high the monument can be raised; the estate sets "
            "who works it and who gains most from its dedication.",
            "规模决定仪式价格与可建高度；阶层决定由谁施工，以及落成后谁获益最多。",
        ),
        "effects": ("What Every Level Gives", "每一等级提供什么"),
        "effects_note": (
            "The wonder's own effects, exactly as the game applies them, at the first level and at "
            "the last. Each level adds the same again, so a level VI wonder carries this six times.",
            "这是奇观本身的效果，与游戏实际生效的一致，分别显示一级与满级。每升一级即再叠加一份，"
            "因此六级奇观相当于承此六倍。",
        ),
        "effects_country_1": ("At level I, country-wide", "一级 · 全国"),
        "effects_country_6": ("At level VI, country-wide", "六级 · 全国"),
        "effects_local_6": ("At level VI, at the site", "六级 · 工地"),
        "site": ("Where It Can Stand", "可以建在哪里"),
        "site_generic": (
            "A generic wonder belongs to no place: you choose the site, and the ground decides what "
            "it is worth. The requirements below are the wonder's own siting rule, checked against "
            "your capital as an example; the department lists every location that passes.",
            "通用奇观不专属于任何地方：由你选择工地，而地基决定它的价值。下列要求即这座奇观本身的选址"
            "规则，以你的首都为例进行判定；部门面板会列出所有符合条件的地点。",
        ),
        "site_unique": (
            "A unique wonder belongs to one place in the world, and only the country holding that "
            "place can build it. Its site is fixed, so no siting rule applies; the row above names "
            "the location.",
            "独特奇观属于世上唯一某地，只有控制该地者才能建造。其选址固定，因此没有选址规则；上一行"
            "已指明地点。",
        ),
        "site_example": ("#T Read against your capital:#!", "#T 以你的首都判定：#!"),
        "rituals": ("Three Dedications", "三种落成"),
        "rituals_note": (
            "Every wonder is dedicated in one of three styles, or merely opened plain. Each style "
            "below shows the effect the game will actually apply, and the societal value it pulls "
            "towards. Estate satisfaction is settled when the ritual is confirmed.",
            "每座奇观或以三种风格之一落成，或朴素启用。下列每一种都显示游戏实际会生效的效果，以及它所"
            "牵引的社会价值观。阶层好感在确认仪式时结算。",
        ),
        "standing": ("Who Gains", "谁得益"),
        "standing_unique": (
            "One place, one owner, once. Whoever holds the site builds it, and its dedication is "
            "remembered for a century unless the site changes hands.",
            "一地、一主、一座。持有该地者建造它，其落成将被记住一百年，除非该地易主。",
        ),
        "standing_generic": (
            "Freely sited, so it can be raised wherever the ground reads best. Small wonders may be "
            "raised more than once, which makes them a renewable source of the same reward.",
            "可自由选址，因此可以建在读数最佳之处。小型奇观可重复建造，是同一套奖励的可再生来源。",
        ),
        "standing_reward": ("the ritual reward", "仪式奖励"),
    }
    filters = {
        "all": ("All", "全部"),
        "overview": ("Getting Started", "入门"),
        "mechanics": ("Complete Mechanics", "完整机制"),
        "unique": ("Unique Projects", "独特工程"),
        "generic": ("Generic Projects", "通用工程"),
    }
    out: dict[str, tuple[str, str]] = {}
    for name, value in wonder.items():
        out[key("wonder", name)] = value
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


def render_all(wonders: list[dict], mechanics: dict, textures: dict[int, str]) -> dict:
    """Build the 15 mechanic cards, two examples and their localization."""
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

    for wonder in select_wonder_cards(wonders):
        append_wonder_card(gui, wonder, mechanics, textures[int(wonder["id"])])
        gui.append("")

    gui.append("}")
    merge(shared_localization())
    return {"gui": gui, "loc_en": loc_en, "loc_zh": loc_zh}
