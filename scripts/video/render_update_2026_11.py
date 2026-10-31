#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""伟大工程 · 1.4 更新视频 —— 纯截图版渲染器。

内容依据 docs/video/2026-11_update/导演设计.md 的分镜表与口播稿。
输出两条轨：内容轨（1920x1080 / 30fps / 无音轨）与字幕轨（SRT）。

用法：
    python3 render_update_2026_11.py --probe    # 每镜头抽静帧供检查
    python3 render_update_2026_11.py --render   # 出片
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

# ---------------------------------------------------------------- 基本参数
W, H, FPS = 1920, 1080, 30

REPO = Path(__file__).resolve().parents[2]
VIDEO_DIR = REPO / "docs" / "video" / "2026-11_update"
BUILD = VIDEO_DIR / "build"
OUT = VIDEO_DIR / "out"

FONT_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SC = 2  # .ttc 内的简体中文字面

RED = (200, 40, 40)
BLUE = (30, 90, 180)
INK = (32, 32, 34)
GREY = (128, 128, 132)
PAGE = (255, 255, 255)
BAR = (237, 237, 239)

_font_cache: dict[tuple, ImageFont.FreeTypeFont] = {}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_B if bold else FONT_R, size, index=SC)
    return _font_cache[key]


def asset(rel: str) -> Path:
    p = REPO / rel
    if not p.exists():
        raise FileNotFoundError(rel)
    return p


def load(rel: str) -> Image.Image:
    return Image.open(asset(rel)).convert("RGB")


# ---------------------------------------------------------------- 图像工具
def cover(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    nw, nh = max(w, int(im.width * s + 0.5)), max(h, int(im.height * s + 0.5))
    r = im.resize((nw, nh), Image.LANCZOS)
    x, y = (nw - w) // 2, (nh - h) // 2
    return r.crop((x, y, x + w, y + h))


def contain(im: Image.Image, w: int, h: int) -> Image.Image:
    s = min(w / im.width, h / im.height)
    return im.resize((max(1, int(im.width * s + 0.5)), max(1, int(im.height * s + 0.5))), Image.LANCZOS)


def blur_fill(im: Image.Image, w: int, h: int, dark: float = 0.45) -> tuple[Image.Image, Image.Image]:
    """模糊铺底 + 等比完整前景。"""
    bg = cover(im, w, h).filter(ImageFilter.GaussianBlur(42))
    bg = Image.eval(bg, lambda v: int(v * dark))
    return bg, contain(im, w, h)


def label_band(im: Image.Image, height: int = 96, alpha: int = 150) -> Image.Image:
    out = im.convert("RGBA")
    out.alpha_composite(Image.new("RGBA", (im.width, height), (0, 0, 0, alpha)), (0, im.height - height))
    return out.convert("RGB")


class Push:
    """单帧缓推：预放大一次，逐帧裁窗后回缩。"""

    def __init__(self, im: Image.Image, zmax: float, ox: float = 0.5, oy: float = 0.5):
        self.big = cover(im, W, H).resize((int(W * zmax), int(H * zmax)), Image.LANCZOS)
        self.zmax, self.ox, self.oy = zmax, ox, oy

    def frame(self, z: float) -> Image.Image:
        z = max(1.0001, min(z, self.zmax))
        cw, ch = int(W * self.zmax / z), int(H * self.zmax / z)
        bx = int((self.big.width - cw) * self.ox)
        by = int((self.big.height - ch) * self.oy)
        return self.big.crop((bx, by, bx + cw, by + ch)).resize((W, H), Image.LANCZOS)


def crop_zoom(im: Image.Image, box, sharpen: float = 1.0) -> Image.Image:
    out = cover(im.crop(box), W, H)
    if sharpen > 1.0:
        out = out.filter(ImageFilter.UnsharpMask(radius=2, percent=int(60 * (sharpen - 1)), threshold=2))
    return out


def dashed_rect(d: ImageDraw.ImageDraw, box, color=RED, width=4, dash=16, gap=10):
    x0, y0, x1, y1 = box
    for x in range(x0, x1, dash + gap):
        d.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=width)
        d.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=width)
    for y in range(y0, y1, dash + gap):
        d.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=width)
        d.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=width)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def caption(im: Image.Image, text: str) -> Image.Image:
    out = im.convert("RGBA")
    d = ImageDraw.Draw(out)
    d.rectangle((0, 964, W, H), fill=(12, 12, 14, 205))
    d.text((96, 1022), text, font=font(42), fill=(240, 240, 242), anchor="lm")
    return out.convert("RGB")


# ---------------------------------------------------------------- 口播与时长
SCENE_DUR = [
    ("T00", 4), ("S01", 11), ("S02", 7), ("S03", 9), ("S04", 11), ("S05", 9),
    ("S06", 13), ("S07", 6), ("S08", 15), ("S09", 8), ("S10", 11), ("S11", 7),
    ("S12", 9), ("S13", 12), ("S14", 14), ("S15", 9), ("S16", 9),
]
TOTAL = sum(d for _, d in SCENE_DUR)
START: dict[str, float] = {}
_t = 0.0
for _s, _d in SCENE_DUR:
    START[_s] = _t
    _t += _d

SCRIPT = {
    "S01": ["各位观众朋友们，大家好。", "伟大工程又更了一版，",
            "这一版里，大半是评论区点名要的。", "这期不放录屏，全部用截图说话。"],
    "S02": ["一共三件事：", "地点界面重做，", "原画全部重绘，", "机制按反馈改了一批。"],
    "S03": ["先说界面。", "以前鼠标往奇观上一放，弹出来的框里，",
            "每座奇观的条件、国家修正、本地修正，全给你铺开。"],
    "S04": ["现在改成一个按钮：点一下，右边挂出一块面板，",
            "每座奇观占一行，原画、名字、等级，一目了然。", "再点一下，整块收回去。"],
    "S05": ["一行就是一座。", "想看它有什么效果，把鼠标放到旁边的仪式名上，",
            "只展开这一份，不会再铺满整个屏幕。"],
    "S06": ["面板关着的时候，这一整块根本不绘制；",
            "开着了，也只是每座一行，而不是每座的完整效果表。", "奇观多、窗口开得久的地方，体感最明显。"],
    "S07": ["第二件事，原画。", "旧的那一批是凭空生成的，好看，但经不起细看。"],
    "S08": ["新的一批，每一张都从一张真实素材开始：", "一张近代照片，一幅雕版，或者一幅历史绘画。",
            "构图、机位、建筑形制都照着来，只换画风。", "所以它看着像画，画的却是一座真房子。"],
    "S09": ["压色、勾线、加纸纹——换的是画法，不是建筑。", "这一批一共一百九十多张，一张一张过的。"],
    "S10": ["第三件事，机制。先加内容：", "这一版新增了五座伟大工程，",
            "有新拆出来的通用原型，也有绑定真实历史地点的独特奇观。"],
    "S11": ["施工期间的移民吸引力，从正二收到正一。", "施工该吸人，但以前吸得有点过。"],
    "S12": ["扩建以前是随机给你一个方向，", "现在三种风格加朴素落成，四个自己挑，", "扩建完还能重新选。"],
    "S13": ["仪式阶段那串一步一停的抉择，删了。",
            "以前每个阶段都要选一次：掏钱硬上，还是先放一放。", "现在整段仪式一次确认，二十四个月走完。"],
    "S14": ["倾向改由仪式决定：选哪个风格，就往那个方向长期推，每月零点一。",
            "轴还没出现的时候，它就只是不带价值观的一个风格，", "不想选也可以跳过，之后再说。"],
    "S15": ["已经落成的也能换，走一遍重新仪式化就行。", "不过仪式会淡忘，一百年过去，它就只是座漂亮房子了。"],
    "S16": ["模组已经在创意工坊更新，奇观图鉴网站也同步了。", "有问题欢迎留言，或者加群找我。谢谢大家。"],
}


def _clean_len(s: str) -> int:
    return sum(1 for c in s if c.isalnum())


MIN_CUE = 1.2   # 字幕可读下限（秒，不含换行间隙）
GAP = 0.25      # 每条字幕末尾留白，避免贴脸切换


def _fit_slots(weights, total, min_slot, gap):
    """按权重分配时长，并保证每格不低于 min_slot；总量严格守恒。"""
    n = len(weights)
    if min_slot * n > total:            # 极端情况：平均分配
        return [total / n] * n
    fixed = [False] * n
    for _ in range(n):
        free = [i for i in range(n) if not fixed[i]]
        free_total = total - min_slot * sum(fixed)
        wsum = sum(weights[i] for i in free)
        slots = [0.0] * n
        for i in range(n):
            slots[i] = min_slot if fixed[i] else free_total * weights[i] / wsum
        newly = [i for i in free if slots[i] < min_slot]
        if not newly:
            return slots
        for i in newly:
            fixed[i] = True
    return slots


def build_subs():
    subs = []
    for scene, dur in SCENE_DUR:
        lines = SCRIPT.get(scene)
        if not lines:
            continue
        weights = [_clean_len(ln) / 4.6 + GAP for ln in lines]
        # 槽内含间隙，故下限要抬到 MIN_CUE + GAP，才能保证显示时长不低于 MIN_CUE
        slots = _fit_slots(weights, dur, MIN_CUE + GAP, GAP)
        t = START[scene]
        for i, (ln, slot) in enumerate(zip(lines, slots)):
            end = t + slot - GAP
            subs.append({"scene": scene, "start": t, "end": end, "text": ln})
            t += slot
    return subs


def ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(subs, path: Path):
    out = [f"{i}\n{ts(s['start'])} --> {ts(s['end'])}\n{s['text']}\n" for i, s in enumerate(subs, 1)]
    path.write_text("\n".join(out), encoding="utf-8")


# ---------------------------------------------------------------- 白底页
def page(bar_text: str | None = None) -> Image.Image:
    im = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 130), fill=BAR)
    d.rectangle((0, 130, W, 136), fill=RED)
    icon = Image.open(asset("assets/cover/ED.png")).convert("RGBA").resize((92, 92), Image.LANCZOS)
    im.paste(icon, (W - 72 - 92, 19), icon)
    if bar_text:
        d.text((72, 65), bar_text, font=font(60, True), fill=INK, anchor="lm")
    return im


# ---------------------------------------------------------------- 镜头表
SHOTS: list[dict] = []


def shot(sid: str, dur: float, scene: str | None, fn):
    SHOTS.append({"id": sid, "dur": dur, "scene": scene, "fn": fn, "frames": int(round(dur * FPS))})


# --- T00 片头 -------------------------------------------------------------
def t00(t, dur):
    base = t00.push.frame(1.00 + 0.04 * (t / dur)).convert("RGBA")
    base.alpha_composite(Image.new("RGBA", (W, H), (8, 12, 18, 150)))
    d = ImageDraw.Draw(base)
    d.text((W // 2, 448), "伟大工程", font=font(132, True), fill=(255, 255, 255), anchor="mm",
           stroke_width=3, stroke_fill=(0, 0, 0))
    d.line([(W // 2 - 132, 534), (W // 2 + 132, 534)], fill=RED, width=5)
    d.text((W // 2, 604), "1.4 更新", font=font(76, True), fill=(255, 236, 232), anchor="mm",
           stroke_width=2, stroke_fill=(0, 0, 0))
    return base.convert("RGB")


# --- 白底页 ---------------------------------------------------------------
def p01(t, dur):
    im = page()
    d = ImageDraw.Draw(im)
    d.text((140, 358), "评论区点名要的", font=font(96, True), fill=INK, anchor="la")
    d.text((140, 486), "这次都做了。", font=font(96, True), fill=RED, anchor="la")
    d.line([(146, 626), (466, 626)], fill=RED, width=5)
    d.text((140, 678), "本期全部为截图", font=font(48), fill=GREY, anchor="la")
    return im


def p02(t, dur):
    im = page("本次更新")
    d = ImageDraw.Draw(im)
    rows = [("01", "界面", "点开才挂出，一座一行"),
            ("02", "原画", "一百九十多张，全部重绘"),
            ("03", "机制", "扩建自选、仪式重做")]
    y = 268
    for num, name, desc in rows:
        d.text((150, y), num, font=font(64, True), fill=RED, anchor="la")
        d.text((300, y - 6), name, font=font(76, True), fill=INK, anchor="la")
        d.text((570, y + 18), desc, font=font(46), fill=GREY, anchor="la")
        y += 214
    return im


def p03(t, dur):
    im = page("界面 · 开销")
    d = ImageDraw.Draw(im)
    d.text((W // 2, 516), "关着不绘制", font=font(96, True), fill=INK, anchor="mm")
    d.text((W // 2, 648), "一座只画一行", font=font(96, True), fill=RED, anchor="mm")
    return im


def p04(t, dur):
    im = page("伟大工程 · 1.4 更新")
    art = cover(load("assets/generated_wonders/tv_wonder_unique_suzhou_classical_gardens.png"), 660, 800)
    im.paste(art, (1188, 196))
    d = ImageDraw.Draw(im)
    d.rectangle((1188, 196, 1847, 995), outline=(214, 214, 216), width=2)
    rows = [
        ("创意工坊", "steamcommunity.com/sharedfiles/filedetails/?id=3766375743"),
        ("奇观图鉴", "hljsxk.github.io/eu5-towards-victory"),
        ("QQ 群", "1070041687　·　qm.qq.com/q/Yc2QwEsCgC"),
    ]
    y = 292
    for name, val in rows:
        d.text((150, y), name, font=font(46, True), fill=RED, anchor="la")
        d.text((150, y + 62), val, font=font(32), fill=INK, anchor="la")
        y += 198
    return im


# --- S03 界面·旧 ----------------------------------------------------------
SZ = dict(w=1476.0, h=1080.0, x=222.0)   # location_zh.jpg (1305x955) 在画布中的落位
S03_BOXES = [(845, 645, 1200, 745)]      # 国家修正 / 本地修正 两列


def _loc_canvas() -> Image.Image:
    bg, fg = blur_fill(load("docs/marketing/assets/location_zh.jpg"), W, H, dark=0.30)
    bg.paste(fg, (int(SZ["x"]), 0))
    return bg


def _loc_map(box):
    sx, sy = SZ["w"] / 1305.0, SZ["h"] / 955.0
    x0, y0, x1, y1 = box
    return (int(SZ["x"] + x0 * sx), int(y0 * sy), int(SZ["x"] + x1 * sx), int(y1 * sy))


def s03(t, dur):
    base = s03.base.convert("RGBA")
    out = base.copy()
    out.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 158)))
    for b in S03_BOXES:
        cb = _loc_map(b)
        cb = (cb[0] - 12, cb[1] - 12, cb[2] + 12, cb[3] + 12)
        out.paste(base.crop(cb), cb[:2])
    d = ImageDraw.Draw(out)
    for b in S03_BOXES:
        cb = _loc_map(b)
        dashed_rect(d, (cb[0] - 12, cb[1] - 12, cb[2] + 12, cb[3] + 12), width=4)
    return out.convert("RGB")


# --- S04 界面·新 ----------------------------------------------------------
def _c01():
    out = load("assets/1030-movie/C01.png").convert("RGBA")
    out.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 80)))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle((424, 279, 571, 334), radius=8, outline=RED, width=5)
    return out.convert("RGB")


def _c02():
    return load("assets/1030-movie/C02.png")


def s04a(t, dur):
    return Push(_c01(), 1.02).frame(1.0 + 0.015 * (t / dur))


def s04b(t, dur):
    return Push(_c02(), 1.05).frame(1.0 + 0.035 * (t / dur))


def s04c(t, dur):
    return Push(_c01(), 1.02).frame(1.02 - 0.015 * (t / dur))


# --- S05 一行里有什么 -----------------------------------------------------
S05_ROW = (503, 588, 930, 828)     # C02：原画 + 名称 + 等级 + 右侧仪式名
S05_TT = (957, 660, 1393, 906)     # C03：悬停效果提示


def s05a(t, dur):
    return crop_zoom(_c02(), S05_ROW, sharpen=1.5)


def s05b(t, dur):
    return crop_zoom(load("assets/1030-movie/C03.png"), S05_TT, sharpen=1.5)


# --- S06 开销 -------------------------------------------------------------
def _c04_marked():
    out = load("assets/1030-movie/C04.png").convert("RGBA")
    out.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 60)))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle((497, 288, 936, 772), radius=6, outline=RED, width=5)
    return out.convert("RGB")


def s06a(t, dur):
    return p03(t, dur)


def s06b(t, dur):
    return Push(_c04_marked(), 1.03).frame(1.0 + 0.02 * (t / dur))


def s06c(t, dur):
    base = s06c.base.convert("RGBA")
    p = ease(min(1.0, t / (dur * 0.86)))
    reg = _loc_map((520, 300, 1290, 800))
    gray = ImageOps.grayscale(base.crop(reg).convert("RGB")).convert("RGBA")
    cut = int(reg[3] * p)
    if cut > 0:
        base.paste(gray.crop((0, 0, reg[2] - reg[0], cut)), (reg[0], reg[1]))
    return base.convert("RGB")


# --- S07 原画·旧 ----------------------------------------------------------
S07_OLD = "assets/historical/review/original_ai/tv_wonder_unique_leaning_tower_of_pisa.png"
S07_RING = (1236, 150, 1516, 950)   # 塔身拱廊：这版多出好几层


def s07(t, dur):
    im = s07.push.frame(1.00 + 0.05 * (t / dur)).convert("RGBA")
    a = ease((t - 2.6) / 0.8) if t > 2.6 else 0.0
    if a > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse(S07_RING, outline=(255, 60, 60, int(255 * a)), width=7)
        im.alpha_composite(lay)
    return im.convert("RGB")


# --- S08 原画·源素材 ------------------------------------------------------
S08_A = "assets/historical/比萨斜塔.jpg"
S08_C = "assets/historical/processed/比萨斜塔_ai_cartoon.png"
S08_ZOOM = (255, 270, 605, 1020)


def _s08_frame(src, cap, t, dur):
    bg, fg = blur_fill(src, W, H, dark=0.34)
    bg.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
    return Push(bg, 1.03).frame(1.0 + 0.025 * (t / dur))


def s08a(t, dur):
    return _s08_frame(s08.a, "真实照片 · 游客与脚手架都留着", t, dur)


def s08b(t, dur):
    return _s08_frame(s08.b, "局部：先看真实建筑形制", t, dur)


def s08c(t, dur):
    return _s08_frame(s08.c, "同机位重绘 · 只换画风", t, dur)


# --- S09 对照表 -----------------------------------------------------------
S09_TBL = "assets/historical/review/comparison_01.jpg"
S09_ROW = (0, 0, 1600, 300)


def s09a(t, dur):
    return Push(s09.a, 1.03).frame(1.0 + 0.02 * (t / dur))


def s09b(t, dur):
    """四栏对照表的一行：等比贴在深色画布上，保留表头列名。"""
    strip = s09.a.crop(S09_ROW)
    scale = 1720 / strip.width
    strip = strip.resize((1720, int(strip.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (26, 27, 30))
    canvas.paste(strip, ((W - strip.width) // 2, (H - strip.height) // 2 - 30))
    d = ImageDraw.Draw(canvas)
    d.rectangle(((W - strip.width) // 2, (H - strip.height) // 2 - 30,
                 (W + strip.width) // 2, (H + strip.height) // 2 - 30), outline=(90, 92, 96), width=2)
    return canvas


# --- S10 五座新工程 -------------------------------------------------------
S10_ITEMS = [
    ("assets/generated_wonders/tv_wonder_grand_garden_complex.png", "园林群", "small", "通用原型"),
    ("assets/generated_wonders/tv_wonder_unique_amber_room.png", "琥珀宫", "large", "独特奇观"),
    ("assets/generated_wonders/tv_wonder_unique_parthenon.png", "帕特农神庙", "medium", "独特奇观"),
    ("assets/generated_wonders/tv_wonder_unique_bangkok_grand_palace.png", "曼谷大皇宫", "large", "独特奇观"),
    ("assets/generated_wonders/tv_wonder_unique_wat_arun.png", "郑王庙", "small", "独特奇观"),
]


def _s10_card(item) -> Image.Image:
    rel, name, size, kind = item
    out = cover(load(rel), W, H).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    for i in range(300):
        dd.line([(0, H - 300 + i), (W, H - 300 + i)], fill=(0, 0, 0, int(185 * (i / 300) ** 1.4)))
    out.alpha_composite(ov)
    d = ImageDraw.Draw(out)
    badge = Image.open(asset(f"assets/generated_icons/tv_project_size_{size}.png")).convert("RGBA")
    badge = badge.resize((104, 104), Image.LANCZOS)
    out.paste(badge, (W - 120 - 104, 72), badge)
    d.text((120, H - 152), name, font=font(96, True), fill=(255, 255, 255), anchor="ls",
           stroke_width=5, stroke_fill=(0, 0, 0))
    d.text((120, H - 92), kind, font=font(40), fill=(228, 228, 230), anchor="ls",
           stroke_width=3, stroke_fill=(0, 0, 0))
    return out.convert("RGB")


def s10(t, dur):
    n = len(S10_ITEMS)
    per = dur / n
    idx = min(n - 1, int(t / per))
    lt = (t - idx * per) / per
    out = Push(s10.cards[idx], 1.04).frame(1.0 + 0.035 * lt)
    fade = ease(min(1.0, lt * 6))
    if fade < 1.0 and idx > 0:
        prev = Push(s10.cards[idx - 1], 1.04).frame(1.035)
        out = Image.blend(prev, out, fade)
    return out


# --- S11 施工期吸引力 -----------------------------------------------------
S11_TT = (455, 600, 985, 900)


def s11(t, dur):
    return crop_zoom(load("assets/1030-movie/C05.png"), S11_TT, sharpen=1.5)


# --- 画中画白底页 ---------------------------------------------------------
def pip_page(crop_img: Image.Image, lines, *, card_w=820, title=None, strike=False):
    im = page(title)
    cw = card_w
    ch = int(crop_img.height * cw / crop_img.width)
    card = crop_img.resize((cw, ch), Image.LANCZOS)
    if strike:
        card = ImageOps.grayscale(card).convert("RGB")
    x, y = 110, (H - ch) // 2
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((x + 8, y + 10, x + cw + 8, y + ch + 10), fill=(0, 0, 0, 46))
    im = im.convert("RGBA")
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
    im.paste(card, (x, y))
    d = ImageDraw.Draw(im)
    d.rectangle((x, y, x + cw, y + ch), outline=(206, 206, 210), width=2)
    if strike:
        d.line([(x + 26, y + 26), (x + cw - 26, y + ch - 26)], fill=(210, 40, 40, 235), width=14)
        d.line([(x + cw - 26, y + 26), (x + 26, y + ch - 26)], fill=(210, 40, 40, 235), width=14)
    tx, yy = x + cw + 84, 244
    for kind, txt in lines:
        f = font(50, True) if kind in ("h", "r", "b") else (font(38) if kind == "g" else font(44))
        col = {"h": INK, "r": RED, "b": BLUE, "g": GREY}.get(kind, INK)
        d.text((tx, yy), txt, font=f, fill=col, anchor="la")
        yy += 78 if kind == "g" else 98
    return im.convert("RGB")


# ceremony-ready.png 986..      ：四行风格 + 风味文本（示例行之上）
S12_CROP = (28, 495, 542, 942)
S14_CROP_B = (26, 1062, 550, 1170)   # 价值观一节（示例行之下）
S15_A_CROP = (20, 452, 556, 684)     # finalized：黄金拍卖 + 仪式已完成 · 永久生效
S15_B_CROP = (28, 490, 542, 822)     # reritual-ready：顶部横幅 + 取消 + 风格行
S13_CROP = (28, 660, 542, 1215)      # 旧版八阶段仪式


def s12(t, dur):
    return pip_page(s12.img, [
        ("h", "扩建方向：四个自己挑"),
        ("g", "以前：随机给一个方向"),
        ("b", "现在：三风格 + 朴素落成"),
        ("", "扩建完还能重新选"),
    ], title="机制 · 扩建")


def s13(t, dur):
    return pip_page(s13.img, [
        ("h", "一步一停的抉择"),
        ("r", "旧版 · 已删除"),
        ("g", "以前每阶段选一次：掏钱硬上 / 先放一放"),
        ("b", "现在：一次确认，24 个月走完"),
    ], title="机制 · 仪式", strike=True, card_w=760)


def s14a(t, dur):
    return pip_page(s14a.img, [
        ("h", "选哪个风格，就往那个方向长期推"),
        ("b", "每月 +0.1"),
        ("", "轴未出现时：只是不带价值观的风格"),
        ("g", "不想选也可以跳过，之后再说"),
    ], title="机制 · 倾向")


def s14b(t, dur):
    return pip_page(s14b.img, [
        ("h", "轴出现之前"),
        ("", "它只是一套画风，不带价值观"),
        ("b", "倾向由仪式慢慢累积"),
        ("g", "可以跳过，之后再说"),
    ], title="机制 · 倾向")


def s15a(t, dur):
    return pip_page(s15a.img, [
        ("h", "已落成的也能换"),
        ("b", "走一遍重新仪式化"),
        ("", "仅授予仪式加成与 10 威望"),
        ("g", "不用推倒重来"),
    ], title="机制 · 重仪式化")


def s15b(t, dur):
    return pip_page(s15b.img, [
        ("h", "不过仪式会淡忘"),
        ("r", "100 年后"),
        ("", "它就只是座漂亮房子了"),
        ("g", "记得回来再做一次"),
    ], title="机制 · 重仪式化")


# ---------------------------------------------------------------- 预计算
class _NS:
    """镜头素材的挂载点。"""


s08 = _NS()
s09 = _NS()


def prepare():
    BUILD.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    t00.push = Push(load("assets/generated_wonders/tv_wonder_unique_suzhou_classical_gardens.png"), 1.06)
    s03.base = _loc_canvas()
    s06c.base = _loc_canvas()

    s07.push = Push(load(S07_OLD), 1.06)

    s08.a = load(S08_A)
    s08.b = s08.a.crop(S08_ZOOM)
    s08.c = load(S08_C)

    s09.a = load(S09_TBL)

    s10.cards = [_s10_card(it) for it in S10_ITEMS]

    s12.img = load("ai_gui_assessment/images/engineering/simp_chinese/ceremony-ready.png").crop(S12_CROP)
    s13.img = load("ai_gui_assessment/images/engineering/engineering_ceremony-stages.png").crop(S13_CROP)
    s14a.img = s12.img
    s14b.img = load("ai_gui_assessment/images/engineering/simp_chinese/ceremony-ready.png").crop(S14_CROP_B)
    s15a.img = load("ai_gui_assessment/images/engineering/simp_chinese/finalized.png").crop(S15_A_CROP)
    s15b.img = load("ai_gui_assessment/images/engineering/simp_chinese/reritual-ready.png").crop(S15_B_CROP)


def build_shotlist():
    SHOTS.clear()
    shot("T00", 4, None, t00)
    shot("S01", 11, "S01", p01)
    shot("S02", 7, "S02", p02)
    shot("S03", 9, "S03", s03)
    shot("S04a", 3.0, "S04", s04a)
    shot("S04b", 6.5, "S04", s04b)
    shot("S04c", 1.5, "S04", s04c)
    shot("S05a", 4.5, "S05", s05a)
    shot("S05b", 4.5, "S05", s05b)
    shot("S06a", 5.5, "S06", s06a)
    shot("S06b", 3.5, "S06", s06b)
    shot("S06c", 4.0, "S06", s06c)
    shot("S07", 6, "S07", s07)
    shot("S08a", 5, "S08", s08a)
    shot("S08b", 5, "S08", s08b)
    shot("S08c", 5, "S08", s08c)
    shot("S09a", 3, "S09", s09a)
    shot("S09b", 5, "S09", s09b)
    shot("S10", 11, "S10", s10)
    shot("S11", 7, "S11", s11)
    shot("S12", 9, "S12", s12)
    shot("S13", 12, "S13", s13)
    shot("S14a", 7, "S14", s14a)
    shot("S14b", 7, "S14", s14b)
    shot("S15a", 4, "S15", s15a)
    shot("S15b", 5, "S15", s15b)
    shot("S16", 9, "S16", p04)
    total = sum(s["dur"] for s in SHOTS)
    assert abs(total - TOTAL) < 1e-6, f"镜头总时长 {total} 与分镜表 {TOTAL} 不符"


# ---------------------------------------------------------------- 渲染
def encode_segment(sh, path: Path):
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-g", "60", str(path)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(sh["frames"]):
        im = sh["fn"](i / FPS, sh["dur"])
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        proc.stdin.write(im.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"编码失败：{sh['id']}")


def cmd_probe():
    prepare()
    build_shotlist()
    dst = BUILD / "probe"
    dst.mkdir(parents=True, exist_ok=True)
    tiles = []
    for sh in SHOTS:
        im = sh["fn"](sh["dur"] * 0.5, sh["dur"]).convert("RGB")
        im.save(dst / f"{sh['id']}.png")
        tiles.append((sh["id"], im))
    cols, tw, th = 4, 480, 270
    rows = math.ceil(len(tiles) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * (th + 26)), (24, 24, 26))
    d = ImageDraw.Draw(sheet)
    for i, (sid, im) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * (th + 26)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x + 6, y + th + 4), sid, font=font(16), fill=(230, 230, 230))
    sheet.save(BUILD / "contact_sheet.png")
    print(f"probe: {len(SHOTS)} shots -> {dst}")
    print(f"contact sheet -> {BUILD / 'contact_sheet.png'}")


def _probe_ok(path: Path, want_dur: float) -> bool:
    """片段必须能被 ffprobe 读出，且时长接近预期，才算完成。"""
    if not path.exists() or path.stat().st_size < 10000:
        return False
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", str(path)],
                             capture_output=True, text=True, timeout=20)
        if out.returncode != 0:
            return False
        return abs(float(out.stdout.strip()) - want_dur) < 0.5
    except Exception:
        return False


def cmd_render(resume_override: bool = False, only: str | None = None):
    prepare()
    build_shotlist()
    seg_dir = BUILD / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    lo, hi = 1, len(SHOTS)
    if only:
        a_, b_ = only.split("-")
        lo, hi = int(a_), int(b_)
    for i, sh in enumerate(SHOTS, 1):
        if not (lo <= i <= hi):
            continue
        p = seg_dir / f"{i:03d}_{sh['id']}.mp4"
        # 断点续渲：可读且时长正确的片段直接跳过
        if not resume_override and _probe_ok(p, sh["dur"]):
            print(f"[{i}/{len(SHOTS)}] {sh['id']} 已存在，跳过", flush=True)
            continue
        encode_segment(sh, p)
        print(f"[{i}/{len(SHOTS)}] {sh['id']} {sh['dur']}s", flush=True)

    segs = sorted(seg_dir.glob("*.mp4"))
    expected = [f"{i:03d}_{sh['id']}.mp4" for i, sh in enumerate(SHOTS, 1)]
    missing = [n for n, sh in zip(expected, SHOTS) if not _probe_ok(seg_dir / n, sh["dur"])]
    if missing:
        print(f"还有 {len(missing)} 段未完成，暂不拼接：{missing[:6]}…")
        return

    lst = seg_dir / "list.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in segs), encoding="utf-8")

    content = OUT / "great_projects_1.4_content.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", "-an", "-movflags", "+faststart", str(content)], check=True)

    subs = build_subs()
    srt = OUT / "great_projects_1.4_subtitle.srt"
    write_srt(subs, srt)

    muxed = OUT / "great_projects_1.4_with_subs.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-i", str(content), "-i", str(srt),
                    "-c:v", "copy", "-c:s", "mov_text",
                    "-metadata:s:s:0", "language=chi", "-movflags", "+faststart", str(muxed)], check=True)

    (BUILD / "script.json").write_text(json.dumps(
        {k: {"start": START[k], "dur": dict(SCENE_DUR)[k], "lines": v} for k, v in SCRIPT.items()},
        ensure_ascii=False, indent=2), encoding="utf-8")
    (BUILD / "shots.json").write_text(json.dumps(
        [{"id": s["id"], "scene": s["scene"], "dur": s["dur"],
          "zoom": "1.00→1.04", "focus": None, "crop": None} for s in SHOTS],
        ensure_ascii=False, indent=2), encoding="utf-8")
    (BUILD / "edl.json").write_text(json.dumps(
        [{"id": s["id"], "start": round(sum(x["dur"] for x in SHOTS[:i]), 3), "dur": s["dur"]}
         for i, s in enumerate(SHOTS)], ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"content -> {content}")
    print(f"subtitle -> {srt}（{len(subs)} 条）")
    print(f"muxed   -> {muxed}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--fresh", action="store_true", help="忽略已存在的片段，全部重渲")
    ap.add_argument("--only", default=None, help="只渲指定片段，如 011-020")
    a = ap.parse_args()
    if a.probe:
        cmd_probe()
    elif a.render:
        cmd_render(resume_override=a.fresh, only=a.only)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
