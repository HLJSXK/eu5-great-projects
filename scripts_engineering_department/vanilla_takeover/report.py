"""CLI coverage report for declared vanilla wonder carriers."""

from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts_engineering_department"))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from vanilla_takeover.scan import scan_reference
from vanilla_takeover.rewrite import copies
from vanilla_takeover.render import startup_reconcile


def main():
    scan = scan_reference()
    copies()
    startup_reconcile()
    for path, targets in scan.setup_includes.items():
        if path.endswith(("/07_cities_and_buildings.txt", "/11_art.txt")):
            print(f"Setup include: {path} → {', '.join(targets)}")
    print("Setup sites below count physical declarations; include expansion and bookmark overrides are not evaluated.")
    for c in scan.carriers.values():
        print(f"{c.wonder['key']} → {c.kind}:{c.key} (present_at_level={c.level})")
        for s in (s for s in scan.sites if s.carrier is c):
            print(f"  {s.source.path}:{s.line} {s.site_id} [{s.form}] {s.path} → {s.status}")
    counts = Counter(s.status for s in scan.sites)
    print(f"{len(scan.carriers)} carriers, {len(scan.sites)} sites: " + ", ".join(f"{key}={n}" for key,n in sorted(counts.items())))
    if counts["未处理"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
