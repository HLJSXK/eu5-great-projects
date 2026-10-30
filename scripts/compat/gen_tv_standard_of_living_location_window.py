import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department" / "in_game" / "gui"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_location_window as tv_location_window
from location_window_1_4 import migrate_panel
from wonder_mechanics.render import render_header

BASE_FILE = REPO_ROOT / ".eu5-base" / "reference_mods_variants" / "eu5-towards-victory" / "3698931463" / "in_game" / "gui" / "location_window.gui"
OUT_FILE = REPO_ROOT / "submods" / "tv_standard_of_living_compat" / "in_game" / "gui" / "location_window.gui"
SCRIPT_REL = "scripts/compat/gen_tv_standard_of_living_location_window.py"
DATA_REL = (
    ".eu5-base/reference_game_files/game/in_game/gui/location_window.gui + "
    ".eu5-base/reference_mods_variants/eu5-towards-victory/3698931463/in_game/gui/location_window.gui + data/compat/sol_location_window_1_4.patch"
)
OVERLAY_MARKER = "\n\t\t\t\tvbox = {\n\t\t\t\t\texpand = {}\n"


def inject_tv_overlay(base_gui: str) -> str:
    if base_gui.count(OVERLAY_MARKER) != 1:
        raise RuntimeError("Could not find location scene overlay insertion point in Standard of Living location_window.gui")
    replacement = "\n" + tv_location_window.render_scene_overlay() + OVERLAY_MARKER
    return tv_location_window.inject_wonder_panel(base_gui.replace(OVERLAY_MARKER, replacement, 1))


def generate() -> str:
    base_gui = migrate_panel("sol_location_window_1_4.patch", BASE_FILE)
    # Replace the published snapshot's inline SOL button with SOL's public type.
    marker = 'name = "stat_sol_living_standard"'
    if base_gui.count(marker) != 1:
        raise RuntimeError("Expected one inline SOL living-standard button")
    start = base_gui.rfind('navigational_button_alt = {', 0, base_gui.index(marker))
    if start == -1:
        raise RuntimeError("Could not find inline SOL button container")
    button = tv_location_window.extract_top_level_block(base_gui[start:], 'navigational_button_alt = {')
    if 'using = StandardofLiving_tooltip' not in button:
        raise RuntimeError("Inline SOL button has an unexpected tooltip")
    base_gui = base_gui[:start] + 'sol_location_living_standard_button = {}' + base_gui[start + len(button):]
    lines = render_header(SCRIPT_REL, DATA_REL)
    lines.append(inject_tv_overlay(base_gui))
    return "\n".join(line.rstrip() for line in "\n".join(lines).splitlines()).rstrip() + "\n"


def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(generate(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
