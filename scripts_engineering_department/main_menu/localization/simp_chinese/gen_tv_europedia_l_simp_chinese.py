"""Generate the Simplified Chinese localization for the Great Projects Europedia tab.

Same source as the English generator: europedia_content.py carries both languages side by side,
so the two files always cover the same keys.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))

from europedia_render import render_all, select_wonder_cards  # noqa: E402
from wonder_identity import image_expression  # noqa: E402
from wonder_image_crop_lib import cropped_wonder_image_name  # noqa: E402
from wonder_mechanics.io import load_all_wonder_mechanics_data  # noqa: E402
from wonder_mechanics.render import loc_line, render_header  # noqa: E402

OUT_FILE = (
    REPO_ROOT / "src" / "main_menu" / "localization" / "simp_chinese" / "tv_europedia_l_simp_chinese.yml"
)
SCRIPT_REL = (
    "scripts_engineering_department/main_menu/localization/simp_chinese/"
    "gen_tv_europedia_l_simp_chinese.py"
)
DATA_REL = "scripts_engineering_department/europedia_content.py + scripts_engineering_department/europedia_render.py"


def wonder_icon_texture(wonder: dict) -> str:
    if wonder.get("identity_variants"):
        return '[' + image_expression([wonder], None, f"'tv_wonder_display_image_{wonder['id']}'", cropped=True) + ']'
    image = wonder.get("image", f"tv_wonder_{wonder['key']}")
    return f"gfx/interface/icons/towards_victory/wonders/{cropped_wonder_image_name(image)}.dds"


def generate() -> str:
    wonders, mechanics = load_all_wonder_mechanics_data()
    textures = {int(wonder["id"]): wonder_icon_texture(wonder) for wonder in select_wonder_cards(wonders)}
    values = render_all(wonders, mechanics, textures)["loc_zh"]
    lines = ["l_simp_chinese:"]
    for line in render_header(SCRIPT_REL, DATA_REL):
        lines.append(f" {line}".rstrip())
    for key in sorted(values):
        lines.append(loc_line(key, values[key]))
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUT_FILE.write_text(generate(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
