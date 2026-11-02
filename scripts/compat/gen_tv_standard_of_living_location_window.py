import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department"))
sys.path.insert(0, str(REPO_ROOT / "scripts_engineering_department/in_game/gui"))
from wonder_mechanics.render import render_header
import gen_location_window as tv_location_window

BASE_FILE = tv_location_window.GLORP_LOCATION_WINDOW_FILE
OUT_FILE = REPO_ROOT / "submods" / "tv_standard_of_living_compat" / "in_game" / "gui" / "location_window.gui"
SCRIPT_REL = "scripts/compat/gen_tv_standard_of_living_location_window.py"
DATA_REL = (
    ".eu5-base/reference_mods/3601047146/in_game/gui/location_window.gui + "
    ".eu5-base/reference_mods/3601047146/in_game/gui/vanilla/cmfg_location_window_vanilla_types.gui + "
    "scripts_engineering_department/in_game/gui/gen_location_window.py"
)


def generate() -> str:
    base_gui = tv_location_window.generate_host_gui()
    for marker in (
        "tv_location_wonders_button = {}",
        "tv_location_wonders_panel = {}",
        "sol_location_living_standard_button = {}",
    ):
        if base_gui.count(marker) != 1:
            raise RuntimeError(f"Expected one {marker!r} in SOL standalone location window")
    lines = render_header(SCRIPT_REL, DATA_REL)
    lines.append(base_gui)
    return "\n".join(line.rstrip() for line in "\n".join(lines).splitlines()).rstrip() + "\n"


def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(generate(), encoding="utf-8-sig", newline="\n")
    print(f"Wrote {OUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
