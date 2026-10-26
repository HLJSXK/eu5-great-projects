"""Build side-by-side comparison sheets from the stitched renders in renders/."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
RENDERS = HERE / "renders"
LABELS = {"a": "A · 三联卡", "b": "B · 卷宗", "c": "C · 罗盘"}
STATES = {"select": "选择阶段", "progress": "仪式进行中"}


def main(font_path: str) -> None:
    font = ImageFont.truetype(font_path, 30)
    for state, title in STATES.items():
        crops = []
        for scheme in LABELS:
            image = Image.open(RENDERS / f"ritual_{scheme}_{state}.png")
            crops.append(image.crop((0, 330, image.width, image.height)))
        sheet = Image.new("RGB", (570 * 3 + 40, max(c.height for c in crops) + 56), (20, 24, 32))
        draw = ImageDraw.Draw(sheet)
        for index, (scheme, crop) in enumerate(zip(LABELS, crops)):
            x = index * 590
            sheet.paste(crop, (x, 56))
            draw.text((x + 14, 10), f"{LABELS[scheme]}（{title}）", fill=(240, 215, 140), font=font)
        sheet.save(RENDERS / f"compare_{state}.png")
        print(RENDERS / f"compare_{state}.png", sheet.size)


if __name__ == "__main__":
    main(sys.argv[1])
