"""Export approved SVG badges to transparent 128px PNG and DXT5 DDS.

Requires Node.js and sharp (on its module search path, or --sharp-module with
an absolute package path). SVGs remain the art source; --check verifies both
shipped formats against a fresh render, including every DDS mip level.
"""
from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path
import subprocess
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from dds_image_lib import RgbaImage, build_dds_header, build_mipmap_chain, encode_dxt5

SVG_DIR = ROOT / 'assets/icons/project_size'
PNG_DIR = ROOT / 'assets/generated_icons'
DDS_DIR = ROOT / 'src/main_menu/gfx/interface/icons/location_icons'
SIZES = ('small', 'medium', 'large')
EDGE = 128
RASTERIZE = r"""
const [source, moduleName, edge] = process.argv.slice(1);
const sharp = require(moduleName);
sharp(source, { density: 288 }).resize(Number(edge), Number(edge))
  .ensureAlpha().raw().toBuffer().then(bytes => process.stdout.write(bytes))
  .catch(error => { console.error(error); process.exitCode = 1; });
"""


def render(size: str, *, node: str, sharp_module: str) -> Image.Image:
    result = subprocess.run(
        [node, '-e', RASTERIZE, str(SVG_DIR / f'project-{size}.svg'), sharp_module, str(EDGE)],
        capture_output=True, timeout=60, check=False,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace'))
    if len(result.stdout) != EDGE * EDGE * 4:
        raise ValueError(f'Unexpected raster length for {size}: {len(result.stdout)}')
    return Image.frombytes('RGBA', (EDGE, EDGE), result.stdout)


def encode(image: Image.Image) -> bytes:
    rgba = RgbaImage(image.width, image.height, image.tobytes())
    blocks = [encode_dxt5(level) for level in build_mipmap_chain(rgba, 1)]
    return build_dds_header(image.width, image.height, len(blocks[0]), 'DXT5', len(blocks)) + b''.join(blocks)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', default='node')
    parser.add_argument('--sharp-module', default='sharp')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    stale = []
    for size in SIZES:
        image = render(size, node=args.node, sharp_module=args.sharp_module)
        png = BytesIO()
        image.save(png, format='PNG')
        name = f'tv_project_size_{size}'
        for target, data in ((PNG_DIR / f'{name}.png', png.getvalue()),
                             (DDS_DIR / f'{name}.dds', encode(image))):
            if args.check:
                if not target.exists() or target.read_bytes() != data:
                    stale.append(target.relative_to(ROOT).as_posix())
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                print(f'Wrote {target.relative_to(ROOT)}')
    if args.check:
        for target in stale:
            print(f'Stale: {target}')
        print(f'{len(stale)} stale size-icon assets')
    return int(bool(stale))


if __name__ == '__main__':
    raise SystemExit(main())
