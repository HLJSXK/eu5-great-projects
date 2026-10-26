"""Stitch the panel header and the ceremony card of a ritual_rework mockup render into one image."""
import re
import sys
from pathlib import Path

from PIL import Image

HEADER_BOTTOM = 338


def stitch(png: Path, out: Path) -> None:
    tree = png.with_name(png.stem + "_tree.txt").read_text(encoding="utf-8")
    title = [int(m.group(1)) for m in re.finditer(r"@\d+,(\d+) txt=TV_ENGINEERING_CEREMONY_CARD_TITLE", tree) if int(m.group(1)) > 0]
    bottoms = [int(m.group(2)) + int(m.group(1)) for m in re.finditer(r" \d+x(\d+)@\d+,(\d+) .*txt=RR_", tree)]
    top = min(title) - 22
    bottom = max(bottoms) + 58
    image = Image.open(png)
    head = image.crop((0, 0, image.width, HEADER_BOTTOM))
    body = image.crop((0, top, image.width, bottom))
    result = Image.new("RGB", (image.width, head.height + body.height))
    result.paste(head, (0, 0))
    result.paste(body, (0, head.height))
    result.save(out)
    print(out, result.size)


if __name__ == "__main__":
    for arg in sys.argv[2:]:
        source = Path(arg)
        stitch(source, Path(sys.argv[1]) / source.name)
