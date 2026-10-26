"""Generate complete vanilla decision replacements with ED takeover edits."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts_engineering_department"))
from vanilla_takeover.render import output
from vanilla_takeover.rewrite import copies

if __name__ == "__main__":
    output(Path(__file__).relative_to(ROOT).as_posix(), "src/in_game/common/decisions/tv_vw_vanilla_decision_overrides.txt", copies().decisions)
