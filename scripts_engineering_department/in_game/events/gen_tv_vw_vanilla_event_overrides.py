"""Generate early-loading complete vanilla event copies with ED takeover edits."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts_engineering_department"))
from vanilla_takeover.render import output
from vanilla_takeover.rewrite import copies

if __name__ == "__main__":
    output(Path(__file__).relative_to(ROOT).as_posix(), "src/in_game/events/0000_tv_vw_vanilla_event_overrides.txt", copies().events)
