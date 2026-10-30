"""Freshness uses PNG pixels, independent of the encoder's compression choices."""
from PIL import Image
import pytest
from scripts.generate import outputs_match


def test_png_compression_does_not_change_freshness(tmp_path):
    current, generated = tmp_path / 'old.png', tmp_path / 'new.png'
    pixels = Image.new('RGBA', (16, 16), (25, 50, 75, 0))
    pixels.save(current, compress_level=0)
    pixels.save(generated, compress_level=9)
    assert current.read_bytes() != generated.read_bytes()
    assert outputs_match(current, generated)


@pytest.mark.parametrize('change', ['rgb', 'alpha', 'transparent_rgb', 'size'])
def test_png_pixel_or_dimension_change_is_stale(tmp_path, change):
    current, generated = tmp_path / 'old.png', tmp_path / 'new.png'
    pixels = Image.new('RGBA', (16, 16), (25, 50, 75, 0 if change == 'transparent_rgb' else 255))
    pixels.save(current)
    if change == 'size':
        pixels = pixels.resize((17, 16))
    else:
        rgba = list(pixels.getpixel((0, 0)))
        rgba[3 if change == 'alpha' else 0] -= 1
        pixels.putpixel((0, 0), tuple(rgba))
    pixels.save(generated)
    assert not outputs_match(current, generated)


def test_missing_and_invalid_pngs_are_stale(tmp_path):
    current, generated = tmp_path / 'old.png', tmp_path / 'new.png'
    Image.new('RGB', (1, 1)).save(current)
    assert not outputs_match(current, generated)
    generated.write_bytes(b'broken PNG')
    assert not outputs_match(current, generated)


def test_text_still_compares_exact_bytes(tmp_path):
    current, generated = tmp_path / 'old.txt', tmp_path / 'new.txt'
    current.write_bytes(b'\xef\xbb\xbftext\n')
    generated.write_bytes(current.read_bytes())
    assert outputs_match(current, generated)
    generated.write_bytes(b'\xef\xbb\xbftext\r\n')
    assert not outputs_match(current, generated)


def test_freshness_stages_only_declared_external_inputs(tmp_path, monkeypatch):
    from scripts import generate
    root, stage = tmp_path / 'workspace', tmp_path / 'stage'
    monkeypatch.setattr(generate, 'ROOT', root)
    paths = ('assets/icons/project.svg', 'assets/icons/raster_exports.json', 'assets/exports/project.png')
    for relative in (*paths, 'assets/unrelated/huge.png', 'data/already-copied.yaml'):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(relative.encode())
    registry = {'generated': [{'data': ' + '.join((*paths, 'data/already-copied.yaml', '.eu5-base/reference.txt'))}]}
    generate.stage_registered_inputs(stage, registry)
    assert {path.relative_to(stage).as_posix() for path in stage.rglob('*') if path.is_file()} == set(paths)
    for relative in paths:
        assert (stage / relative).read_bytes() == (root / relative).read_bytes()


def test_freshness_rejects_missing_declared_art_source(tmp_path, monkeypatch):
    from scripts import generate
    monkeypatch.setattr(generate, 'ROOT', tmp_path / 'workspace')
    with pytest.raises(FileNotFoundError):
        generate.stage_registered_inputs(tmp_path / 'stage', {'generated': [{'data': 'assets/missing.svg'}]})


def test_build_registered_localization_producer_runs_offline(tmp_path, monkeypatch):
    """Exercise generate.py's real registry dispatch with the translator's CLI."""
    from pathlib import Path
    from types import SimpleNamespace
    from scripts import generate
    from great_projects_editor_web.services import generation, wonder_generation
    from scripts_engineering_department.main_menu.localization import (
        translate_engineering_department_localization_google as translate,
    )

    source = tmp_path / 'english' / 'example_l_english.yml'
    source.parent.mkdir()
    source.write_text('l_english:\n new_key:0 "English fallback"\n', encoding='utf-8-sig')
    french = tmp_path / 'french' / 'example_l_french.yml'
    french.parent.mkdir()
    preserved = 'l_french:\n existing:0 "Texte traduit"\n'
    french.write_text(preserved, encoding='utf-8-sig')
    monkeypatch.setattr(translate, 'SOURCE_DIR', source.parent)
    monkeypatch.setattr(translate, 'OUTPUT_ROOT', tmp_path)
    monkeypatch.setattr(translate, 'load_cache', lambda path: pytest.fail('Online translation started'))
    monkeypatch.setattr(wonder_generation, 'wonder_generation_plan', lambda *a, **kw: SimpleNamespace(steps=[]))
    monkeypatch.setattr(generation, 'run_generation', lambda *a, **kw: None)
    dispatched = []

    def run(command, **kwargs):
        if Path(command[1]).name == Path(translate.SCRIPT_REL).name:
            dispatched.append(command)
            monkeypatch.setattr(translate.sys, 'argv', command[1:])
            assert translate.main() == 0
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(generate.subprocess, 'run', run)
    assert generate.generate() == 0
    assert len(dispatched) == 1
    assert len(dispatched[0]) == 2  # The build passes no translation flags.
    assert french.read_text(encoding='utf-8-sig').startswith(preserved)
    for language in translate.LANGUAGE_TO_GOOGLE:
        output = tmp_path / language / f'example_l_{language}.yml'
        assert ' new_key:0 "English fallback"\n' in output.read_text(encoding='utf-8-sig')
