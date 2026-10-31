"""Regenerate GP outputs; --check compares text bytes and decoded PNG pixels."""
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
STAGED_DIRECTORIES = ('scripts', 'scripts_engineering_department', 'data', 'src', 'submods', 'great_projects_editor_web')
EXTERNAL_REFERENCE_ROOTS = ('prosper-or-perish-upstream', 'eu5-modding-project')


def stage_registered_inputs(stage: Path, registry: dict) -> None:
    """Copy declared art inputs outside the normal source roots, not all assets."""
    inputs = {part.strip() for row in registry['generated']
              for part in row.get('data', '').split('+') if part.strip()}
    for value in sorted(inputs):
        relative = Path(value)
        if relative.is_absolute():
            raise ValueError(f'Registered input must be workspace-relative: {value}')
        if '..' in relative.parts:
            resolved = (ROOT / relative).resolve()
            allowed = tuple((ROOT.parent / name).resolve() for name in EXTERNAL_REFERENCE_ROOTS)
            if not any(resolved == root or root in resolved.parents for root in allowed):
                raise ValueError(f'Registered external input is not an approved reference checkout: {value}')
            source, target = ROOT / relative, stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target, dirs_exist_ok=True)
            else:
                shutil.copy2(source, target)
            continue
        if relative.parts[0] in (*STAGED_DIRECTORIES, '.eu5-base'):
            continue
        source, target = ROOT / relative, stage / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=True)
        else:
            shutil.copy2(source, target)


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


def outputs_match(current: Path, generated: Path) -> bool:
    """Ignore PNG compression differences, while detecting every changed pixel."""
    if not current.is_file() or not generated.is_file():
        return False
    if current.suffix.lower() != '.png':
        return current.read_bytes() == generated.read_bytes()
    from PIL import Image
    try:
        with Image.open(current) as left, Image.open(generated) as right:
            # Registered PNGs are static thumbnails. Compare all channels, including
            # RGB beneath transparent pixels; ImageChops.getbbox can miss those.
            return (left.format == right.format == 'PNG'
                    and left.n_frames == right.n_frames == 1
                    and left.size == right.size
                    and left.convert('RGBA').tobytes() == right.convert('RGBA').tobytes())
    except (OSError, ValueError):
        return False


def check() -> int:
    registry = yaml.safe_load((ROOT / 'data/generated_files.yaml').read_text(encoding='utf-8'))
    outputs = {row['output'] for row in registry['generated']}
    # GUI mergers declare their final output in the domain plan.
    from great_projects_editor_web.services.wonder_generation import wonder_generation_plan
    outputs.update(p.relative_to(ROOT).as_posix() for p in wonder_generation_plan({'mechanics': True, 'cost_reward': True}, repo_root=ROOT).outputs)
    base = (ROOT / '.eu5-base').resolve()
    (ROOT / 'tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='freshness-', dir=ROOT / 'tmp') as directory:
        sandbox = Path(directory)
        stage = sandbox / 'workspace'
        stage.mkdir()
        for name in STAGED_DIRECTORIES:
            shutil.copytree(ROOT / name, stage / name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        stage_registered_inputs(stage, registry)
        env = {**os.environ, 'EU5_MODDING_BASE': str(base), 'PYTHONDONTWRITEBYTECODE': '1'}
        subprocess.run([sys.executable, str(stage / 'scripts/bootstrap_base.py')], cwd=stage, env=env, check=True)
        result = subprocess.run([sys.executable, str(stage / 'scripts/generate.py')], cwd=stage, env=env)
        if result.returncode:
            return result.returncode
        stale = [p for p in sorted(outputs) if not outputs_match(ROOT / p, stage / p)]
        for path in stale:
            print(f'[STALE] {path}')
        print(f'[{"FAIL" if stale else "OK"}] Compared {len(outputs)} registered/merged outputs.')
        return int(bool(stale))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    raise SystemExit(check() if parser.parse_args().check else generate())
