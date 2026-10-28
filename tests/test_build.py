"""Build modes must not accidentally deploy checks or failed builds."""
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import build


def test_default_directory_preserves_pre_split_deployment_target():
    # From Towards Victory's build.bat before extraction (756f4dcb^).
    assert build.default_mod_directory() == Path(
        r'C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis V\game\mod'
    )


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    root = tmp_path / 'workspace'
    (root / '.eu5-base').mkdir(parents=True)
    (root / '.eu5-base/CLAUDE.md').write_text('base', encoding='utf-8')
    for source in build.PACKAGES.values():
        (root / source).mkdir(parents=True)
        (root / source / 'content.txt').write_text(source, encoding='utf-8')
    mods = tmp_path / 'game mods'
    mods.mkdir()
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        # Robocopy code 1 means files were successfully copied.
        return SimpleNamespace(returncode=1 if command[0] == 'robocopy' else 0)

    monkeypatch.setattr(build, 'ROOT', root)
    monkeypatch.setattr(build.sys, 'platform', 'win32')
    monkeypatch.setattr(build.sys, 'argv', ['build.py'])
    monkeypatch.setattr(build, 'default_mod_directory', lambda: mods)
    monkeypatch.setattr(build.subprocess, 'run', run)
    return root, mods, calls


def test_default_build_packages_and_deploys_all_four_mods(workspace):
    root, mods, calls = workspace

    assert build.main() == 0

    for name, source in build.PACKAGES.items():
        assert (root / 'build' / name / 'content.txt').read_text(encoding='utf-8') == source
    mirrors = [command for command in calls if command[0] == 'robocopy']
    assert len(mirrors) == 4
    assert {Path(command[2]) for command in mirrors} == {mods / name for name in build.PACKAGES}
    assert all(command[3:] == ['/MIR', '/XJ'] for command in mirrors)


@pytest.mark.parametrize('mode', ['--check', '--package-only'])
def test_local_modes_do_not_resolve_or_deploy_to_game(workspace, monkeypatch, mode):
    root, mods, calls = workspace
    monkeypatch.setattr(build.sys, 'argv', ['build.py', mode])
    monkeypatch.setattr(build.sys, 'platform', 'linux')
    monkeypatch.setattr(build, 'default_mod_directory', lambda: pytest.fail('Resolved game directory'))

    assert build.main() == 0

    assert not any(command[0] == 'robocopy' for command in calls)
    assert (root / 'build').exists() == (mode == '--package-only')
    assert ('--check' in calls[0]) == (mode == '--check')
    assert ('--check' in calls[1]) == (mode == '--check')


def test_explicit_deploy_overrides_default_directory(workspace, monkeypatch, tmp_path):
    root, mods, calls = workspace
    other = tmp_path / 'custom mods'
    other.mkdir()
    monkeypatch.setattr(build.sys, 'argv', ['build.py', '--deploy', str(other)])
    monkeypatch.setattr(build, 'default_mod_directory', lambda: pytest.fail('Resolved default directory'))

    assert build.main() == 0

    assert {Path(command[2]).parent for command in calls if command[0] == 'robocopy'} == {other}


@pytest.mark.parametrize('failed_step', ['update_mod_version.py', 'generate.py', 'validate.py'])
def test_failed_build_never_packages_or_deploys(workspace, monkeypatch, failed_step):
    root, mods, calls = workspace

    def run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=2 if Path(command[1]).name == failed_step else 0)

    monkeypatch.setattr(build.subprocess, 'run', run)

    assert build.main() == 2
    assert not (root / 'build').exists()
    assert not any(command[0] == 'robocopy' for command in calls)


def test_missing_mod_directory_fails_before_build(workspace):
    root, mods, calls = workspace
    mods.rmdir()

    with pytest.raises(ValueError, match='EU5 mod directory does not exist'):
        build.main()

    assert not calls
    assert not (root / 'build').exists()


def test_robocopy_failure_is_propagated(workspace, monkeypatch):
    root, mods, calls = workspace

    def run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=8 if command[0] == 'robocopy' else 0)

    monkeypatch.setattr(build.subprocess, 'run', run)

    assert build.main() == 8
    assert len([command for command in calls if command[0] == 'robocopy']) == 1
