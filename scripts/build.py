"""Build Great Projects and its compatibility packages; deploy only with --deploy."""
import argparse
from datetime import date
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    'tv_engineering_department': 'src',
    'tv_meiou_and_taxes_compat': 'submods/tv_meiou_and_taxes_compat',
    'tv_standard_of_living_compat': 'submods/tv_standard_of_living_compat',
    'tv_prosper_or_perish_compat': 'submods/tv_prosper_or_perish_compat',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--deploy', type=Path, metavar='MOD_DIRECTORY')
    parser.add_argument('--date', type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    if not (ROOT / '.eu5-base/CLAUDE.md').is_file():
        raise SystemExit('Run scripts/bootstrap_base.py first.')
    for command in (
        ['update_mod_version.py', '--date', args.date.isoformat(), *(['--check'] if args.check else [])],
        ['generate.py', *(['--check'] if args.check else [])],
        ['validate.py'],
    ):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts' / command[0]), *command[1:]], cwd=ROOT)
        if result.returncode:
            return result.returncode
    if args.check:
        return 0
    for name, source in PACKAGES.items():
        package = ROOT / 'build' / name
        if package.resolve() != package or package.is_symlink():
            raise ValueError(f'Package path must stay inside this workspace: {package}')
        if package.exists():
            shutil.rmtree(package)
        shutil.copytree(ROOT / source, package, ignore=shutil.ignore_patterns('.gitkeep'))
        print(f'[OK] Packaged {package}')
    if args.deploy:
        mods = args.deploy.expanduser().resolve()
        if not mods.is_dir() or sys.platform != 'win32':
            raise ValueError('Deployment requires an existing Windows EU5 mod directory.')
        for name in PACKAGES:
            destination = mods / name
            if destination.resolve() != destination or destination.is_symlink():
                raise ValueError(f'Deployment target must not be a link: {destination}')
            result = subprocess.run(['robocopy', str(ROOT / 'build' / name), str(destination), '/MIR', '/XJ'])
            if result.returncode >= 8:
                return result.returncode
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
