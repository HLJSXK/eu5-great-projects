"""Build DXT5 badges from verified, checked-in 128px PNG exports.

Normal builds and --check need only Python/Pillow. After editing the SVG art,
run --rasterize to refresh the PNGs and their source/pixel hashes. Only that
explicit export step requires Node.js and sharp (--sharp-module can name an
absolute package path). Stale SVGs or changed PNG pixels fail before any write.
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
SCRIPT_REL = 'scripts_engineering_department/gen_project_size_icons.py'
EXPORT_MANIFEST = SVG_DIR / 'raster_exports.json'
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


def export_record(size: str, image: Image.Image) -> dict[str, str]:
    # Normalize text newlines so a Windows checkout does not invalidate pixels.
    source = (SVG_DIR / f'project-{size}.svg').read_text(encoding='utf-8')
    return {'svg_sha256': hashlib.sha256(source.encode('utf-8')).hexdigest(),
            'rgba_sha256': hashlib.sha256(image.tobytes()).hexdigest()}


def rasterize(*, node: str, sharp_module: str) -> dict[str, Image.Image]:
    # Finish every raster before replacing any approved export. Record provenance
    # last, so an interrupted export cannot silently pass the next normal build.
    images = {size: render(size, node=node, sharp_module=sharp_module) for size in SIZES}
    records = {'_generated_by': SCRIPT_REL,
               **{size: export_record(size, image) for size, image in images.items()}}
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    for size, image in images.items():
        image.save(PNG_DIR / f'tv_project_size_{size}.png')
    EXPORT_MANIFEST.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8', newline='\n')
    return images


def load_exports() -> dict[str, Image.Image]:
    records = json.loads(EXPORT_MANIFEST.read_text(encoding='utf-8'))
    if not isinstance(records, dict) or records.get('_generated_by') != SCRIPT_REL:
        raise ValueError('Invalid raster export manifest; refresh it with --rasterize.')
    images = {}
    for size in SIZES:
        path = PNG_DIR / f'tv_project_size_{size}.png'
        with Image.open(path) as source:
            if source.format != 'PNG' or source.size != (EDGE, EDGE) or source.n_frames != 1:
                raise ValueError(f'Invalid {size} PNG export; expected a static {EDGE}px PNG.')
            image = source.convert('RGBA')
        if records.get(size) != export_record(size, image):
            raise ValueError(f'Stale {size} SVG/PNG export; run this script with --rasterize '
                             '(requires Node.js and sharp, optionally --sharp-module PATH).')
        images[size] = image
    return images


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', default='node')
    parser.add_argument('--sharp-module', default='sharp')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='Verify SVG/PNG hashes and all DDS mip levels without Node.js.')
    mode.add_argument('--rasterize', action='store_true', help='Explicitly re-export edited SVG art using Node.js and sharp.')
    args = parser.parse_args(argv)
    try:
        images = rasterize(node=args.node, sharp_module=args.sharp_module) if args.rasterize else load_exports()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f'[ERROR] Project size icons: {exc}', file=sys.stderr)
        return 1
    stale = []
    for size, image in images.items():
        target = DDS_DIR / f'tv_project_size_{size}.dds'
        data = encode(image)
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
