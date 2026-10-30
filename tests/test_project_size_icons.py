"""Normal builds must not depend on the SVG author's Node/sharp installation."""
import os
import json
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image
import pytest

from scripts_engineering_department import gen_project_size_icons as icons

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    from scripts import generate
    import yaml
    registry = yaml.safe_load((ROOT / 'data/generated_files.yaml').read_text(encoding='utf-8'))
    selected = {'generated': [row for row in registry['generated']
                              if row['script'] == 'scripts_engineering_department/gen_project_size_icons.py']}
    # Exercise the same staging contract as build --check, including PNGs that
    # are both registered export outputs and inputs to the normal DDS build.
    generate.stage_registered_inputs(tmp_path, selected)
    for relative in ('scripts_engineering_department/gen_project_size_icons.py', 'scripts/dds_image_lib.py'):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    monkeypatch.setattr(icons, 'ROOT', tmp_path)
    monkeypatch.setattr(icons, 'SVG_DIR', tmp_path / 'assets/icons/project_size')
    monkeypatch.setattr(icons, 'PNG_DIR', tmp_path / 'assets/generated_icons')
    monkeypatch.setattr(icons, 'DDS_DIR', tmp_path / 'src/main_menu/gfx/interface/icons/location_icons')
    monkeypatch.setattr(icons, 'EXPORT_MANIFEST', icons.SVG_DIR / 'raster_exports.json')
    return tmp_path


def test_default_build_and_check_run_without_node_or_sharp(workspace):
    script = workspace / 'scripts_engineering_department/gen_project_size_icons.py'
    before = {path: path.read_bytes() for path in (workspace / 'assets').rglob('*') if path.is_file()}
    for args in ([], ['--check']):
        result = subprocess.run([sys.executable, str(script), *args], cwd=workspace,
                                env={**os.environ, 'PATH': '', 'NODE_PATH': ''},
                                capture_output=True, text=True, encoding='utf-8', timeout=30)
        assert result.returncode == 0, result.stdout + result.stderr
    assert all(path.read_bytes() == data for path, data in before.items())
    for size in icons.SIZES:
        actual = icons.DDS_DIR / f'tv_project_size_{size}.dds'
        assert actual.read_bytes() == (ROOT / actual.relative_to(workspace)).read_bytes()


@pytest.mark.parametrize('change', ['svg', 'pixels', 'dimensions', 'manifest'])
def test_stale_exports_fail_before_writing_dds(workspace, monkeypatch, capsys, change):
    monkeypatch.setattr(icons, 'render', lambda *a, **k: pytest.fail('Build invoked SVG rasterization'))
    png = icons.PNG_DIR / 'tv_project_size_small.png'
    if change == 'svg':
        svg = icons.SVG_DIR / 'project-small.svg'
        svg.write_text(svg.read_text(encoding='utf-8').replace('#557B4D', '#FFFFFF'), encoding='utf-8')
    elif change == 'manifest':
        icons.EXPORT_MANIFEST.unlink()
    else:
        with Image.open(png) as source:
            image = source.convert('RGBA')
        if change == 'dimensions':
            image = image.resize((64, 64))
        else:
            image.putpixel((0, 0), (99, 0, 0, 0))
        image.save(png)
    assert icons.main([]) == 1
    assert not icons.DDS_DIR.exists()
    assert '[ERROR] Project size icons:' in capsys.readouterr().err


def test_check_detects_changed_dds_and_ignores_png_compression(workspace, capsys):
    assert icons.main([]) == 0
    png = icons.PNG_DIR / 'tv_project_size_small.png'
    with Image.open(png) as source:
        pixels = source.copy()
    pixels.save(png, compress_level=0)
    assert icons.main(['--check']) == 0
    target = icons.DDS_DIR / 'tv_project_size_small.dds'
    data = target.read_bytes()
    target.write_bytes(data[:-1] + bytes([data[-1] ^ 1]))
    assert icons.main(['--check']) == 1
    assert 'tv_project_size_small.dds' in capsys.readouterr().out


def test_explicit_rasterize_refreshes_all_exports(workspace, monkeypatch):
    calls = []
    def render(size, **kwargs):
        calls.append(size)
        return Image.new('RGBA', (icons.EDGE, icons.EDGE), (40, 70, 90, 255))
    monkeypatch.setattr(icons, 'render', render)
    assert icons.main(['--rasterize']) == 0
    assert calls == list(icons.SIZES)
    assert json.loads(icons.EXPORT_MANIFEST.read_text(encoding='utf-8'))['_generated_by'] == icons.SCRIPT_REL
    assert icons.main(['--check']) == 0
