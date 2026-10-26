"""Generate vanilla wonder ownership and existence predicates."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts_engineering_department"))
from vanilla_takeover.render import output, triggers

if __name__ == "__main__":
    output(Path(__file__).relative_to(ROOT).as_posix(), "src/in_game/common/scripted_triggers/tv_vw_vanilla_takeover_triggers.txt", triggers())
