#!/usr/bin/env python3
"""Draw the six wonder level medallions.

One circular copper-gold medallion carries a centred Roman numeral. The borders
escalate one element at a time, so a glance at the fixed slot in the lower right
of a wonder card tells the level without reading the numeral:

    I    a single bronze ring, dark field
    II   + inner hairline (a ring inside the ring)
    III  + bead band outside the ring
    IV   + separate outer ring, with a gap
    V    + four studs on the outer ring
    VI   + twelve rays, and the palest gold of the ramp

Each level keeps every element of the level below it; only the frame grows. The
numeral stays the brightest element and keeps a constant size, so the grade is
read from the border and the value from the digit.

Outputs one 128x128 DXT5 DDS per level plus a PNG preview and a contact sheet.
Re-run after changing the geometry; the DDS files are shipped.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from dds_image_lib import (  # noqa: E402
    RgbaImage,
    build_dds_header,
    build_mipmap_chain,
    encode_dxt5,
    write_dds,
)

SCRIPT_REL = "scripts_engineering_department/gen_wonder_level_medallions.py"
PNG_DIR = REPO_ROOT / "assets" / "generated_icons"
DDS_DIR = REPO_ROOT / "src" / "main_menu" / "gfx" / "interface" / "icons" / "location_icons"
SHEET = PNG_DIR / "tv_wonder_level_medallions.png"
NAME = "tv_wonder_level_{level}"

FINAL = 128          # delivered texture edge, in pixels
SS = 8               # supersample factor while drawing
CANVAS = FINAL * SS
CX = CY = CANVAS / 2

# Palatino-family serif: the emperor-inscription register the numeral wants.
# Search order covers Windows, then the URW/TeX clones present on Linux builds.
FONT_CANDIDATES = (
    "C:/Windows/Fonts/pala.ttf",
    "C:/Windows/Fonts/palab.ttf",
    "/usr/share/fonts/opentype/urw-base35/P052-Bold.otf",
    "/usr/share/texmf/fonts/opentype/public/lm/lmroman12-bold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/System/Library/Fonts/Palatino.ttc",
)

NUMERALS = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}

GOLD = {
    "shadow": (30, 21, 12),
    "dark": (78, 55, 23),
    "deep": (116, 83, 36),
    "mid": (158, 122, 60),
    "brass": (194, 158, 95),
    "bright": (228, 202, 145),
    "pale": (255, 246, 212),
}

# Cumulative: level N draws everything level N-1 draws, then one more element.
LADDER = {
    1: dict(rim=5.0, inner=False, beads=0, studs=False, spikes=0, outer=False, wash=0.60),
    2: dict(rim=5.4, inner=True, beads=0, studs=False, spikes=0, outer=False, wash=0.66),
    3: dict(rim=5.8, inner=True, beads=26, studs=False, spikes=0, outer=False, wash=0.72),
    4: dict(rim=6.0, inner=True, beads=26, studs=False, spikes=0, outer=True, wash=0.78),
    5: dict(rim=6.2, inner=True, beads=26, studs=True, spikes=0, outer=True, wash=0.85),
    6: dict(rim=6.4, inner=True, beads=26, studs=True, spikes=12, outer=True, wash=0.95),
}

R_RIM = 41.0
R_INNER = 32.4
R_BEAD = 46.4
R_OUTER = 50.6
NUMERAL_CAP = 34.0
NUMERAL_MAX_WIDTH = 45.0
TRACKING = 0.085     # extra gap between glyphs, as a fraction of the em size


def s(value: float) -> float:
    """Logical medallion units → supersampled pixels."""
    return value * SS


def resolve_font() -> str:
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise SystemExit(
        "No serif face found for the level medallions. Tried:\n  "
        + "\n  ".join(FONT_CANDIDATES)
        + "\nAdd an available path to FONT_CANDIDATES."
    )


def lerp_stops(stops: list[tuple[float, tuple[int, int, int]]], t: float) -> tuple[int, int, int]:
    t = min(1.0, max(0.0, t))
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t <= t1 or i == len(stops) - 2:
            span = t1 - t0
            f = 0.0 if span == 0 else min(1.0, max(0.0, (t - t0) / span))
            return tuple(int(round(c0[k] + (c1[k] - c0[k]) * f)) for k in range(3))
    return stops[-1][1]


def rim_colour(level: int, t: float) -> tuple[int, int, int]:
    """Bronze at level 1 → palest gold at level 6.

    ``t`` walks the ring vertically: 0 is the lit top edge, 1 the shaded bottom.
    """
    ramp = (
        (0.0, ((0.0, GOLD["mid"]), (0.55, GOLD["deep"]), (1.0, GOLD["dark"]))),
        (0.5, ((0.0, GOLD["brass"]), (0.55, GOLD["mid"]), (1.0, GOLD["deep"]))),
        (1.0, ((0.0, GOLD["pale"]), (0.5, GOLD["bright"]), (1.0, GOLD["brass"]))),
    )
    u = (level - 1) / 5
    for i in range(len(ramp) - 1):
        if ramp[i][0] <= u <= ramp[i + 1][0]:
            f = (u - ramp[i][0]) / (ramp[i + 1][0] - ramp[i][0])
            low = lerp_stops(list(ramp[i][1]), t)
            high = lerp_stops(list(ramp[i + 1][1]), t)
            return tuple(int(round(low[k] + (high[k] - low[k]) * f)) for k in range(3))
    return GOLD["bright"]


def ring(canvas: Image.Image, radius: float, width: float, colour, alpha: int = 255) -> None:
    w = max(1.0, s(width))
    ImageDraw.Draw(canvas).ellipse(
        [CX - s(radius) - w / 2, CY - s(radius) - w / 2, CX + s(radius) + w / 2, CY + s(radius) + w / 2],
        outline=tuple(colour) + (alpha,), width=int(round(w)))


def metal_ring(canvas: Image.Image, radius: float, width: float, level: int, alpha: int = 255) -> None:
    """A ring carrying its own lit top edge and shaded bottom, so it reads as metal."""
    ring(canvas, radius, width, rim_colour(level, 0.45), alpha)
    offset = width * 0.26
    ring(canvas, radius + offset, max(0.9, width * 0.32), rim_colour(level, 0.0), alpha)
    ring(canvas, radius - offset, max(0.9, width * 0.32), rim_colour(level, 1.0), alpha)
    ring(canvas, radius + width * 0.55, 0.9, GOLD["shadow"], int(alpha * 0.9))
    ring(canvas, radius - width * 0.55, 0.9, GOLD["shadow"], int(alpha * 0.9))


def radial_disc(size: int, stops, radius: float) -> Image.Image:
    img = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(img)
    steps = 150
    for i in range(steps, -1, -1):
        t = i / steps
        r = s(radius) * t
        draw.ellipse([CX - r, CY - r, CX + r, CY + r], fill=lerp_stops(list(stops), t))
    return img


def soft_disc(size: int, radius: float, strength: float, power: float = 3.4) -> Image.Image:
    """Coverage mask: opaque core falling off smoothly at the edge."""
    img = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(img)
    steps = 46
    for i in range(steps, 0, -1):
        t = i / steps
        r = s(radius) * t
        alpha = int(255 * strength * min(1.0, (1 - t ** power) ** 0.55))
        draw.ellipse([CX - r, CY - r, CX + r, CY + r], fill=alpha)
    return img


def dot(canvas: Image.Image, x: float, y: float, radius: float, level: int, highlight: float = 0.20) -> None:
    high = rim_colour(level, 0.0)
    low = rim_colour(level, 0.85)
    draw = ImageDraw.Draw(canvas)
    r = s(radius)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=low + (255,))
    draw.ellipse([x - r * 0.70, y - r * 0.70 - s(radius * highlight),
                  x + r * 0.60, y + r * 0.60 - s(radius * highlight)], fill=high + (255,))


def bead_band(canvas: Image.Image, radius: float, count: int, dot_radius: float, level: int) -> None:
    for i in range(count):
        angle = -math.pi / 2 + 2 * math.pi * (i + 0.5) / count
        dot(canvas, CX + s(radius) * math.cos(angle), CY + s(radius) * math.sin(angle),
            dot_radius, level, 0.18)


def stud_band(canvas: Image.Image, radius: float, dot_radius: float, level: int) -> None:
    for k in range(4):
        angle = -math.pi / 2 + k * math.pi / 2
        dot(canvas, CX + s(radius) * math.cos(angle), CY + s(radius) * math.sin(angle),
            dot_radius, level, 0.24)


def spike_band(canvas: Image.Image, r_in: float, r_out: float, count: int, level: int,
               offset_deg: float = 0.0) -> None:
    high = rim_colour(level, 0.0)
    draw = ImageDraw.Draw(canvas)
    half = math.pi / count * 0.34
    for i in range(count):
        angle = math.radians(offset_deg) + 2 * math.pi * i / count
        p1 = (CX + s(r_in) * math.cos(angle - half), CY + s(r_in) * math.sin(angle - half))
        p2 = (CX + s(r_in) * math.cos(angle + half), CY + s(r_in) * math.sin(angle + half))
        p3 = (CX + s(r_out) * math.cos(angle), CY + s(r_out) * math.sin(angle))
        draw.polygon([p1, p2, p3], fill=high + (255,))


def numeral_mask(font_path: str, numeral: str, cap_height: float, max_width: float) -> Image.Image:
    """Rasterise the numeral glyph by glyph with tracking.

    Palatino sets I and V hard against each other; untracked, ``IV`` collapses
    into one blob and ``III`` loses its gaps once the medallion is drawn at the
    in-game 40px.
    """
    probe = ImageFont.truetype(font_path, 400)
    bb = probe.getbbox("I")
    cap = bb[3] - bb[1]
    size = 400 * s(cap_height) / cap
    track = size * TRACKING

    def layout(px: float):
        font = ImageFont.truetype(font_path, int(px))
        glyphs = [(ch, font.getbbox(ch)) for ch in numeral]
        width = sum(gb[2] - gb[0] for _, gb in glyphs) + track * (len(glyphs) - 1) * px / 400
        return font, glyphs, width

    font, glyphs, total = layout(size)
    if total > s(max_width):
        size *= s(max_width) / total
        track = size * TRACKING
        font, glyphs, total = layout(size)

    heights = [gb[3] - gb[1] for _, gb in glyphs]
    pad = int(s(1.6))
    mask = Image.new("L", (int(total) + 2 * pad, max(heights) + 2 * pad), 0)
    draw = ImageDraw.Draw(mask)
    x = float(pad)
    for ch, gb in glyphs:
        # Share one baseline: align every glyph's ink box to the tallest.
        draw.text((x - gb[0], pad + (max(heights) - (gb[3] - gb[1])) - gb[1]), ch, font=font, fill=255)
        x += (gb[2] - gb[0]) + track
    return mask


def draw_numeral(canvas: Image.Image, font_path: str, numeral: str) -> None:
    """Pale-gold numeral with an engraved drop shadow and a soft top light.

    The body colour does not change with level: the numeral is the value, the
    frame is the grade. Only the frame may get brighter.
    """
    mask = numeral_mask(font_path, numeral, NUMERAL_CAP, NUMERAL_MAX_WIDTH)
    w, h = mask.size
    x, y = int(CX - w / 2), int(CY - h / 2)

    canvas.paste(Image.new("RGBA", (w, h), GOLD["shadow"] + (255,)),
                 (x + int(s(0.9)), y + int(s(1.0))),
                 mask.filter(ImageFilter.GaussianBlur(s(0.85))))

    column = Image.new("RGB", (1, h))
    cd = ImageDraw.Draw(column)
    stops = [(0.0, GOLD["pale"]), (0.42, GOLD["bright"]), (0.82, GOLD["brass"]), (1.0, GOLD["mid"])]
    for yy in range(h):
        cd.point((0, yy), fill=lerp_stops(stops, yy / max(1, h - 1)))
    canvas.paste(column.resize((w, h)), (x, y), mask)

    canvas.paste(Image.new("RGBA", (w, h), GOLD["pale"] + (255,)),
                 (x - int(s(0.5)), y - int(s(0.6))),
                 mask.filter(ImageFilter.GaussianBlur(s(0.5))).point(lambda v: int(v * 0.30)))


def draw_medallion(level: int, font_path: str) -> Image.Image:
    spec = LADDER[level]
    canvas = Image.new("RGBA", (CANVAS, CANVAS))

    # Faint halo keeps the ornament band legible over bright artwork.
    canvas.paste(Image.new("RGBA", (CANVAS, CANVAS), (18, 13, 8, 255)), (0, 0),
                 soft_disc(CANVAS, R_OUTER + 4.0, 0.42, power=2.2))
    canvas.paste(Image.new("RGBA", (CANVAS, CANVAS), (20, 14, 9, 255)), (0, 0),
                 soft_disc(CANVAS, R_RIM + 2.5, 0.94))
    canvas.paste(radial_disc(CANVAS, ((0.0, (70, 51, 28)), (0.55, (45, 33, 19)),
                                     (1.0, (25, 18, 11))), R_RIM - 2.0), (0, 0),
                 soft_disc(CANVAS, R_RIM - 2.0, spec["wash"]))

    if spec["spikes"]:
        # Offset so the rays fall between the cardinal studs, not under them.
        spike_band(canvas, R_OUTER - 2.0, R_OUTER + 7.4, spec["spikes"], level, offset_deg=-75)
    if spec["outer"]:
        metal_ring(canvas, R_OUTER, 1.6, level, alpha=252)
    if spec["beads"]:
        bead_band(canvas, R_BEAD, spec["beads"], 1.20, level)
    if spec["studs"]:
        stud_band(canvas, R_OUTER, 3.5, level)

    if spec["inner"]:
        ring(canvas, R_INNER + 1.0, 1.4, GOLD["shadow"], 175)
        ring(canvas, R_INNER, 0.85, rim_colour(level, 0.10), 210)

    draw_numeral(canvas, font_path, NUMERALS[level])
    metal_ring(canvas, R_RIM, spec["rim"], level)

    return canvas.resize((FINAL, FINAL), Image.LANCZOS)


def contact_sheet(images: list[Image.Image]) -> Image.Image:
    """One review image: 128px art, 44px and 33px in-game sizes, both backdrops."""
    sheet = Image.new("RGBA", (6 * 150 + 30, 300), (36, 29, 19, 255))
    for i, im in enumerate(images):
        x = i * 150 + 20
        sheet.alpha_composite(im, (x, 16))
        sheet.alpha_composite(im.resize((44, 44), Image.LANCZOS), (x + 42, 160))
        sheet.alpha_composite(im.resize((33, 33), Image.LANCZOS), (x + 48, 216))
    return sheet


def encoded_dds(image: Image.Image) -> bytes:
    """The exact bytes write_dds() would produce for this image.

    DXT5 is lossy, so a decoded comparison can never match a fresh render; the
    regression check has to compare encoded output.
    """
    rgba = RgbaImage(image.width, image.height, image.tobytes())
    levels = build_mipmap_chain(rgba, 1)
    blocks = [encode_dxt5(level) for level in levels]
    return (build_dds_header(image.width, image.height, len(blocks[0]), "DXT5", len(blocks))
            + b"".join(blocks))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="compare shipped DDS with a fresh render instead of writing")
    args = parser.parse_args(argv)

    font_path = resolve_font()
    images = [draw_medallion(level, font_path) for level in range(1, 7)]

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    DDS_DIR.mkdir(parents=True, exist_ok=True)

    stale: list[str] = []
    for level, image in enumerate(images, 1):
        name = NAME.format(level=level)
        preview = PNG_DIR / f"{name}.png"
        target = DDS_DIR / f"{name}.dds"
        if args.check:
            if not target.exists():
                stale.append(f"{target.relative_to(REPO_ROOT)} missing")
                continue
            if target.read_bytes() != encoded_dds(image):
                stale.append(f"{target.relative_to(REPO_ROOT)} differs from a fresh render")
            continue
        image.save(preview)
        write_dds(RgbaImage(image.width, image.height, image.tobytes()), target,
                  overwrite=True, mipmaps=True)
        print(f"Wrote {preview.relative_to(REPO_ROOT)} and {target.relative_to(REPO_ROOT)}")

    if args.check:
        for problem in stale:
            print(problem)
        print(f"{len(stale)} stale asset(s)")
        return 1 if stale else 0

    sheet = contact_sheet(images)
    sheet.save(SHEET)
    print(f"Wrote {SHEET.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
