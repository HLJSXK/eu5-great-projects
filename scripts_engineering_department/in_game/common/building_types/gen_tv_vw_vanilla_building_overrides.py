"""Seal declared vanilla building carriers when their ED site has the same owner."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts_engineering_department"))
from vanilla_takeover.render import buildings, output

if __name__ == "__main__":
    output(Path(__file__).relative_to(ROOT).as_posix(), "src/in_game/common/building_types/tv_vw_vanilla_building_overrides.txt", buildings())
