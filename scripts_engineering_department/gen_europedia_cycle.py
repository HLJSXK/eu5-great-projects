"""Bake the overview's clockwise connectors; native GUI has no rotated lines.

Positions are shared with europedia_render so cards and arrows cannot drift.
"""
from math import cos, sin, radians
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CYCLE_SIZE = (1370, 960)
CYCLE_CENTER = (685, 480)
RADIUS = 382
STEP_SIZE = (264, 196)
TEXTURE = "gfx/interface/illustrations/tv_europedia_cycle.dds"


def point(angle: float, radius: float = RADIUS) -> tuple[float, float]:
    angle = radians(angle)
    return (CYCLE_CENTER[0] + radius * cos(angle),
            CYCLE_CENTER[1] + radius * sin(angle))


def step_positions(count: int = 7) -> list[tuple[int, int]]:
    if count < 3:
        raise ValueError("The overview circle requires at least three stages")
    return [(round(x - STEP_SIZE[0] / 2), round(y - STEP_SIZE[1] / 2))
            for x, y in (point(-90 + index * 360 / count) for index in range(count))]


def draw_connectors(count: int = 7):
    from PIL import Image, ImageDraw

    scale = 3
    image = Image.new("RGBA", tuple(value * scale for value in CYCLE_SIZE))
    draw = ImageDraw.Draw(image)
    boxes = [(x - 14, y - 14, x + STEP_SIZE[0] + 14, y + STEP_SIZE[1] + 14)
             for x, y in step_positions(count)]

    def scaled(points):
        return [(round(x * scale), round(y * scale)) for x, y in points]

    def clear(p):
        x, y = p
        return not any(left <= x <= right and top <= y <= bottom
                       for left, top, right, bottom in boxes)

    for index in range(count):
        start = -90 + index * 360 / count
        angles = [start + tick / 4 for tick in range(round(360 * 4 / count) + 1)
                  if clear(point(start + tick / 4))]
        end = angles[-1]
        arc = [point(angle) for angle in angles if angle <= end - 3]
        draw.line(scaled([(x, y + 2) for x, y in arc]), fill="#171c23", width=6 * scale)
        draw.line(scaled(arc), fill="#8c7045", width=4 * scale)
        draw.line(scaled(arc), fill="#d9bb7c", width=2 * scale)
        tip = point(end)
        base = point(end - 3.5)
        normal = (cos(radians(end)), sin(radians(end)))
        head = [tip, (base[0] + normal[0] * 7, base[1] + normal[1] * 7),
                (base[0] - normal[0] * 7, base[1] - normal[1] * 7)]
        draw.polygon(scaled(head), fill="#d9bb7c")

    # A quiet central medallion gives the stages a common visual centre.
    for radius, color in ((118, "#766344"), (112, "#443f34")):
        cx, cy = CYCLE_CENTER
        bounds = tuple(round(v * scale) for v in (cx-radius, cy-radius, cx+radius, cy+radius))
        draw.ellipse(bounds, outline=color, width=scale)
    return image.resize(CYCLE_SIZE, Image.Resampling.LANCZOS)


def main() -> None:
    image = draw_connectors()
    preview = REPO_ROOT / "assets/generated_icons/tv_europedia_cycle.png"
    preview.parent.mkdir(parents=True, exist_ok=True)
    image.save(preview)
    target = REPO_ROOT / "src/main_menu" / TEXTURE
    target.parent.mkdir(parents=True, exist_ok=True)
    # Uncompressed RGBA preserves the thin gold strokes and their antialiasing;
    # block compression introduces coloured speckles around these sparse lines.
    image.save(target, format="DDS")
    print(f"Wrote {preview.relative_to(REPO_ROOT)} and {target.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
