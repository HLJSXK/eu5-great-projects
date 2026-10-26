"""Generate the startup-only carrier reconciliation callback."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts_engineering_department"))
from vanilla_takeover.render import block, output

if __name__ == "__main__":
    contents = block("tv_wonder_vw_startup_reconcile_on_game_start", block("effect", block("hidden_effect", "tv_vw_startup_reconcile_effect = yes")))
    output(Path(__file__).relative_to(ROOT).as_posix(), "src/in_game/common/on_action/tv_vw_vanilla_takeover_on_action.txt", contents)
