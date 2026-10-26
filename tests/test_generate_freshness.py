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
