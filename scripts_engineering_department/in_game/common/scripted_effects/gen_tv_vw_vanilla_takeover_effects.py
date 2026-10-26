"""Generate vanilla wonder level-change wrappers."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts_engineering_department"))
from vanilla_takeover.render import operations, output, startup_reconcile

if __name__ == "__main__":
    output(Path(__file__).relative_to(ROOT).as_posix(), "src/in_game/common/scripted_effects/tv_vw_vanilla_takeover_effects.txt", operations() + "\n\n" + startup_reconcile())
