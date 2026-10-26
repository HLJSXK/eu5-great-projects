"""Rebuild the registered wonder pipeline and optionally refresh the static atlas."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from great_projects_editor_web.services.generation import run_generation
from great_projects_editor_web.services.wonder_generation import wonder_generation_plan
from audit_wonder_rituals import audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atlas', action='store_true', help='Also rebuild the atlas data using its existing map index.')
    args = parser.parse_args()
    plan = wonder_generation_plan({'mechanics': True}, repo_root=ROOT)
    run_generation(plan, log=lambda message: print(message, end='', flush=True))
    audit()
    if args.atlas:
        subprocess.run([
            sys.executable, str(ROOT / 'unique_wonders_site/scripts/build/build_wonders.py'),
            '--locations-index', str(ROOT / 'unique_wonders_site/dist/data/locations_index.json'),
        ], cwd=ROOT, check=True)
    print(f'[OK] Rebuilt {len(plan.steps)} registered generators and validated their artifacts.')


if __name__ == '__main__':
    main()
