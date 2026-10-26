"""Regenerate registered GP outputs; --check compares an isolated build byte for byte."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def generate() -> int:
    from great_projects_editor_web.services.generation import run_generation
    from great_projects_editor_web.services.wonder_generation import wonder_generation_plan
    plan = wonder_generation_plan({'mechanics': True, 'cost_reward': True}, repo_root=ROOT)
    run_generation(plan, log=lambda s: print(s, end='', flush=True))
    completed = {step.spec.script for step in plan.steps}
    registry = yaml.safe_load((ROOT / 'data/generated_files.yaml').read_text(encoding='utf-8'))
    scripts = list(dict.fromkeys(row['script'] for row in registry['generated']))
    for script in scripts:
        if script in completed or script == 'scripts/gen_index.py':
            continue
        subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/gen_index.py')], cwd=ROOT, check=True)
    print(f'[OK] Generated {len(scripts)} registered producers.')
    return 0


def check() -> int:
    registry = yaml.safe_load((ROOT / 'data/generated_files.yaml').read_text(encoding='utf-8'))
    outputs = {row['output'] for row in registry['generated']}
    # GUI mergers declare their final output in the domain plan.
    from great_projects_editor_web.services.wonder_generation import wonder_generation_plan
    outputs.update(p.relative_to(ROOT).as_posix() for p in wonder_generation_plan({'mechanics': True, 'cost_reward': True}, repo_root=ROOT).outputs)
    base = (ROOT / '.eu5-base').resolve()
    (ROOT / 'tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='freshness-', dir=ROOT / 'tmp') as directory:
        stage = Path(directory)
        for name in ('scripts', 'scripts_engineering_department', 'data', 'src', 'submods', 'great_projects_editor_web'):
            shutil.copytree(ROOT / name, stage / name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        env = {**os.environ, 'EU5_MODDING_BASE': str(base), 'PYTHONDONTWRITEBYTECODE': '1'}
        subprocess.run([sys.executable, str(stage / 'scripts/bootstrap_base.py')], cwd=stage, env=env, check=True)
        result = subprocess.run([sys.executable, str(stage / 'scripts/generate.py')], cwd=stage, env=env)
        if result.returncode:
            return result.returncode
        stale = [p for p in sorted(outputs) if not (ROOT / p).is_file() or not (stage / p).is_file() or (ROOT / p).read_bytes() != (stage / p).read_bytes()]
        for path in stale:
            print(f'[STALE] {path}')
        print(f'[{"FAIL" if stale else "OK"}] Compared {len(outputs)} registered/merged outputs.')
        return int(bool(stale))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    raise SystemExit(check() if parser.parse_args().check else generate())
