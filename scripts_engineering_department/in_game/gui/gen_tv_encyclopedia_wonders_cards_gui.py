"""Generate the Great Projects Europedia card list as a standalone fragment.

Merged into src/in_game/gui/encyclopedia_lateralview.gui (a hand-authored full override of the
vanilla Europedia panel -- EU5 has no native, data-driven way to register a new Encyclopedia
sidebar page, see docs/knowledge/risk_cards/europedia.md) by
scripts_engineering_department/in_game/gui/merge_tv_encyclopedia_wonders_cards_gui.py, which
inserts or replaces a `# BEGIN/END GENERATED TV_ENCYCLOPEDIA_CARDS` marker pair right after the
`# TV_ENCYCLOPEDIA_CARDS_ANCHOR` comment in that shell file.

The cards themselves are built by scripts_engineering_department/europedia_render.py from
europedia_content.py (15 mechanic cards) and the shared wonder data package (Triumphal Axis
and Topkapi Palace teaching examples, plus the complete compact static catalogue). Their text is generated separately, from the same two
sources, into the English and Simplified Chinese Europedia localization files, so a card can
never reference a key that does not exist.

Card style: src/in_game/gui/shared/tv_europedia_style.gui.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from europedia_render import render_all  # noqa: E402,F401
from wonder_mechanics.io import load_all_wonder_mechanics_data  # noqa: E402
from wonder_mechanics.render import render_header  # noqa: E402

OUT_FILE = REPO_ROOT / "data" / "generated_fragments" / "tv_encyclopedia_wonders_cards.gui"
SCRIPT_REL = "scripts_engineering_department/in_game/gui/gen_tv_encyclopedia_wonders_cards_gui.py"
DATA_REL = (
    "scripts_engineering_department/europedia_content.py + scripts_engineering_department/europedia_render.py + scripts_engineering_department/europedia_catalogue.py + data/wonders.yaml + "
    "data/wonder_final_buildings.yaml + data/wonder_generic_rituals.yaml + "
    "data/wonder_base_modifiers.yaml + data/wonder_site_rules.yaml + data/unique_wonders.yaml"
)
MARKER = "TV_ENCYCLOPEDIA_CARDS"


def generate() -> str:
    wonders, mechanics = load_all_wonder_mechanics_data()
    rendered = render_all(wonders, mechanics)

    lines = render_header(SCRIPT_REL, DATA_REL)
    lines.append(f"# BEGIN GENERATED {MARKER}")
    lines.extend(rendered["gui"])
    lines.append(f"# END GENERATED {MARKER}")
    return "\n".join(line.rstrip() for line in lines).rstrip() + "\n"


def main() -> None:
    OUT_FILE.write_text(generate(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
