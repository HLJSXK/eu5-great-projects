"""Draw the paired gold navigation arrows for the location detail button.

The polygon is the editable source; supersampling keeps the 24px GUI icons crisp.
"""
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageOps

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / 'scripts'))
from dds_image_lib import RgbaImage, write_dds


def draw_right_arrow() -> Image.Image:
    scale = 4
    points = [(8, 26), (34, 26), (34, 13), (56, 32),
              (34, 51), (34, 38), (8, 38)]
    image = Image.new('RGBA', (64 * scale, 64 * scale))
    draw = ImageDraw.Draw(image)
    shape = [(x * scale, y * scale) for x, y in points]
    draw.polygon([(x, y + 2 * scale) for x, y in shape], fill='#281d12')
    draw.polygon(shape, fill='#dec58c')
    draw.line(shape + [shape[0]], fill='#785c32', width=2 * scale, joint='curve')
    draw.line([(10 * scale, 28 * scale), (36 * scale, 28 * scale),
               (36 * scale, 18 * scale), (51 * scale, 31 * scale)],
              fill='#fff0c5', width=2 * scale, joint='curve')
    return image.resize((64, 64), Image.Resampling.LANCZOS)


def main() -> None:
    right = draw_right_arrow()
    for direction, image in (('right', right), ('left', ImageOps.mirror(right))):
        name = f'tv_wonder_arrow_{direction}'
        preview = REPO_ROOT / 'assets/generated_icons' / f'{name}.png'
        preview.parent.mkdir(parents=True, exist_ok=True)
        image.save(preview)
        target = REPO_ROOT / 'src/main_menu/gfx/interface/icons/location_icons' / f'{name}.dds'
        write_dds(RgbaImage(image.width, image.height, image.tobytes()), target,
                  overwrite=True, mipmaps=True)
        print(f'Wrote {preview.relative_to(REPO_ROOT)} and {target.relative_to(REPO_ROOT)}')


if __name__ == '__main__':
    main()
