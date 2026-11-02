#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""伟大工程 · 1.4 更新视频 —— 暖纸编辑风 · 逐帧动画渲染器（v3）。

内容依据 docs/video/2026-11_update/ 的分镜与口播稿。
输出三条轨：纯内容（1920x1080 / 30fps / 无音轨）、字幕（SRT）、合成。

v3 相对 v2 的改动：
  * 视觉：去掉灰色页眉条，改成暖纸底 + 细金线 + 衬线标题的编辑版式；
    页脚有细进度条与页码，全片像一本会翻页的册子。
  * 动画：v2 每镜头只组合一帧复用；v3 逐帧重绘，用「淡入上浮 / 描线 /
    扫高亮 / 数字滚动 / 曲线生长」这类示意性动作说明内容，不动图片素材本身
    （图片只做淡入与极小的位移，不做滤镜、不做裁块放大）。
  * 转场：镜头之间 8 帧交叉溶解，页眉不动、内容变化，切换不生硬。
  * 时长微调：T00/S01/S04/S06/S07/S10/S11/S13/S14 各调 ±1s 给动画留落点，
    总长仍为 123s，字幕时间轴由同一张表派生。

用法：
    python3 render_update_2026_11.py --probe        # 每镜头抽三帧静帧供检查
    python3 render_update_2026_11.py --render       # 出片
    python3 render_update_2026_11.py --render --fresh
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------- 基本参数
W, H, FPS = 1920, 1080, 30

REPO = Path(__file__).resolve().parents[2]
VIDEO_DIR = REPO / "docs" / "video" / "2026-11_update"
BUILD = VIDEO_DIR / "build"
OUT = VIDEO_DIR / "out"

_FONT_DIR = "/usr/share/fonts/opentype/noto"
FONT_R = f"{_FONT_DIR}/NotoSansCJK-Regular.ttc"
FONT_B = f"{_FONT_DIR}/NotoSansCJK-Bold.ttc"
SERIF_R = f"{_FONT_DIR}/NotoSerifCJK-Regular.ttc"
SERIF_B = f"{_FONT_DIR}/NotoSerifCJK-Bold.ttc"
SC = 2  # .ttc 内的简体中文字面

# ---- 暖纸编辑风配色 ----
PAPER = (246, 242, 233)
CARD = (252, 250, 245)
INK = (26, 24, 22)
MUTED = (124, 116, 104)
FAINT = (168, 160, 148)
RED = (176, 40, 32)
GOLD = (166, 130, 62)
HAIR = (221, 212, 196)
BLUE = (44, 84, 140)
DARK = (32, 30, 28)

# ---- 统一版式常量：所有页面共用，改这里就等于改全片 ----
HEADER_H = 152          # 页眉高度（细线落在这里）
TOPBAR_BOTTOM = HEADER_H + 46
MARGIN = 96             # 左右页边距
CONTENT_W = W - 2 * MARGIN            # 1728
CONTENT_BOTTOM = H - 132
AVAIL_H = CONTENT_BOTTOM - TOPBAR_BOTTOM   # 750

NOTE_W = 486            # 右侧说明栏宽度
NOTE_GAP = 76
IMG_W = CONTENT_W - NOTE_W - NOTE_GAP  # 1166

XFADE = 8               # 转场交叉溶解帧数

_font_cache: dict[tuple, ImageFont.FreeTypeFont] = {}


def _ttf(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=SC)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    key = ("s", size, bold)
    if key not in _font_cache:
        _font_cache[key] = _ttf(FONT_B if bold else FONT_R, size)
    return _font_cache[key]


def serif(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    key = ("f", size, bold)
    if key not in _font_cache:
        _font_cache[key] = _ttf(SERIF_B if bold else SERIF_R, size)
    return _font_cache[key]


def asset(rel: str) -> Path:
    p = REPO / rel
    if not p.exists():
        raise FileNotFoundError(rel)
    return p


def load(rel: str) -> Image.Image:
    return Image.open(asset(rel)).convert("RGB")


# ---------------------------------------------------------------- 基础工具
def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else hi if x > hi else x


def ease(t: float) -> float:
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease_out(t: float) -> float:
    t = clamp(t)
    return 1 - (1 - t) ** 3


def prog(t: float, start: float, dur: float) -> float:
    """t 在 [start, start+dur] 上的线性进度。"""
    if dur <= 0:
        return 1.0 if t >= start else 0.0
    return clamp((t - start) / dur)


def lerp(c1, c2, a: float):
    a = clamp(a)
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * a)) for i in range(3))


def contain(im: Image.Image, w: int, h: int, up: float = 1.0) -> Image.Image:
    """等比缩放到 (w,h) 之内；up 为允许的最大放大倍数（默认只缩不放）。"""
    s = min(w / im.width, h / im.height, up)
    return im.resize((max(1, int(im.width * s + 0.5)), max(1, int(im.height * s + 0.5))),
                     Image.LANCZOS)


_SHADOW_CACHE: dict[tuple, Image.Image] = {}


def soft_shadow(w: int, h: int, blur: int = 18, alpha: int = 46) -> Image.Image:
    """同一尺寸的投影只算一次（高斯模糊很贵）。"""
    key = (w, h, blur, alpha)
    if key not in _SHADOW_CACHE:
        pad = blur * 2
        sh = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle((pad, pad + 6, pad + w, pad + h + 6),
                                     fill=(0, 0, 0, alpha))
        _SHADOW_CACHE[key] = sh.filter(ImageFilter.GaussianBlur(blur))
    return _SHADOW_CACHE[key]


def card(img: Image.Image, *, border=True, shadow=True) -> Image.Image:
    """把一张图包成“压在纸上的照片”：投影 + 发丝边，返回带透明留白的 RGBA 块。

    块必须是透明的：相邻的块、后画的文字都可能落在留白里，填纸色会盖掉它们。
    这里只缓存投影；图像内容每帧都不同，缓存整块会把动画冻在第一帧。
    """
    pad = CARD_PAD
    out = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    if shadow:
        sh = soft_shadow(img.width, img.height)
        out.alpha_composite(sh, (pad - sh.width // 2 + img.width // 2,
                                 pad - sh.height // 2 + img.height // 2))
    out.paste(img.convert("RGB"), (pad, pad))
    if border:
        ImageDraw.Draw(out).rectangle((pad, pad, pad + img.width - 1, pad + img.height - 1),
                                      outline=HAIR + (255,), width=1)
    return out


CARD_PAD = 40


def paste_card(im: Image.Image, blk: Image.Image, x: int, y: int, alpha: float = 1.0):
    """落位一张 card() 产生的块；x,y 是图片本身的目标坐标。"""
    pos = (x - CARD_PAD, y - CARD_PAD)
    tile = blk if alpha >= 0.999 else _fade_rgba(blk, alpha)
    im.paste(tile, pos, tile)


def _fade_rgba(im: Image.Image, alpha: float) -> Image.Image:
    out = im.convert("RGBA").copy()
    out.putalpha(out.getchannel("A").point(lambda v: int(v * clamp(alpha))))
    return out


def tracked(d, xy, s, size, fill, *, track=3, bold=False, use_serif=False,
            anchor="la", alpha=1.0, bg=PAPER) -> int:
    """带字距的文本（小标签用）。返回总宽度。"""
    f = serif(size, bold) if use_serif else font(size, bold)
    if not s:
        return 0
    widths = [d.textlength(ch, font=f) for ch in s]
    total = sum(widths) + track * (len(s) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    col = lerp(bg, fill, alpha)
    for ch, w in zip(s, widths):
        if ch != " ":
            d.text((x, y), ch, font=f, fill=col, anchor="l" + anchor[1])
        x += w + track
    return int(total)


def wrap(d, txt: str, f, width: int) -> list[str]:
    """按像素宽度折行（中文没有空格，逐字累加；避免单字孤行）。"""
    lines, cur = [], ""
    for ch in txt:
        if d.textlength(cur + ch, font=f) > width and cur:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    # 修孤字：末行只有一个字时，从上一行挪一个字下来
    if len(lines) >= 2 and len(lines[-1]) == 1 and len(lines[-2]) > 2:
        lines[-1] = lines[-2][-1] + lines[-1]
        lines[-2] = lines[-2][:-1]
    return lines


def line_at(d, p0, p1, f, fill, width=3):
    f = clamp(f)
    if f <= 0:
        return
    d.line([p0, (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)],
           fill=fill, width=width)


def arrow(im, p0, p1, f, fill, width=4, head=20):
    """画一支逐渐长出来的箭头（不透明度随进度）。"""
    f = ease_out(f)
    if f <= 0.01:
        return
    x0, y0 = p0
    x1, y1 = (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
    d = ImageDraw.Draw(im)
    d.line([(x0, y0), (x1, y1)], fill=fill, width=width)
    ang = math.atan2(y1 - y0, x1 - x0)
    for s in (+1, -1):
        a = ang + math.pi + s * 0.44
        d.line([(x1, y1), (x1 + head * math.cos(a), y1 + head * math.sin(a))],
               fill=fill, width=width)


def brackets(im, box, color=RED, width=4, arm=28, alpha=1.0, grow=1.0):
    """四角括号式选取框，比整圈红框轻。"""
    x0, y0, x1, y1 = box
    arm = max(6, int(arm * clamp(grow)))
    tile = Image.new("RGBA", (x1 - x0 + width * 2 + 2, y1 - y0 + width * 2 + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    ox = oy = width + 1
    col = color + (255,)
    L = [(x0, y0, x0 + arm, y0), (x0, y0, x0, y0 + arm),
         (x1, y0, x1 - arm, y0), (x1, y0, x1, y0 + arm),
         (x0, y1, x0 + arm, y1), (x0, y1, x0, y1 - arm),
         (x1, y1, x1 - arm, y1), (x1, y1, x1, y1 - arm)]
    for ax, ay, bx, by in L:
        d.line([(ax - x0 + ox, ay - y0 + oy), (bx - x0 + ox, by - y0 + oy)],
               fill=col, width=width)
    if alpha < 0.999:
        tile.putalpha(tile.getchannel("A").point(lambda v: int(v * clamp(alpha))))
    im.paste(tile, (x0 - ox, y0 - oy), tile)


def badge(im, xy, n, r=20, fill=RED, alpha=1.0, scale=1.0, bg=PAPER, ring=4):
    """圆形编号徽标，带 pop 缩放。外圈留一圈纸色，压在截图上也不糊成一团。"""
    s = clamp(scale, 0.01, 2.0)
    r2 = int(r * s)
    pad = 6 + ring
    tile = Image.new("RGBA", (r2 * 2 + pad * 2, r2 * 2 + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    c = (r2 + pad, r2 + pad)
    if ring:
        d.ellipse((c[0] - r2 - ring, c[1] - r2 - ring, c[0] + r2 + ring, c[1] + r2 + ring),
                  fill=bg + (255,))
    d.ellipse((c[0] - r2, c[1] - r2, c[0] + r2, c[1] + r2), fill=fill + (255,))
    d.text((c[0], c[1] + 1), str(n), font=serif(int(r2 * 1.25), True),
           fill=(252, 248, 240, 255), anchor="mm")
    if alpha < 0.999:
        tile.putalpha(tile.getchannel("A").point(lambda v: int(v * clamp(alpha))))
    im.paste(tile, (int(xy[0]) - c[0], int(xy[1]) - c[1]), tile)


def pop(t: float, start: float, dur: float = 0.45) -> float:
    """0→1 的弹性 pop：略微过冲。"""
    p = prog(t, start, dur)
    if p <= 0:
        return 0.0
    s = 1.70158
    return 1 + (s + 1) * (p - 1) ** 3 + s * (p - 1) ** 2


def sweep(im, box, f, color=(255, 248, 236), strength=0.30):
    """在方块内扫过一条高光带（悬停示意）。"""
    x0, y0, x1, y1 = [int(v) for v in box]
    if f <= 0 or x1 <= x0 or y1 <= y0:
        return
    w = x1 - x0
    bw = max(24, int(w * 0.45))
    cx = x0 + int((w + bw) * ease_out(f)) - bw
    a0, a1 = max(x0, cx), min(x1, cx + bw)
    if a1 <= a0:
        return
    region = im.crop((a0, y0, a1, y1))
    im.paste(Image.blend(region, Image.new("RGB", region.size, color), strength), (a0, y0))


def _map(box, rect, src_w, src_h):
    """把原图坐标上的框换算到图片实际落位。

    src_w/src_h 必须是**原图**尺寸（图片文件本身的宽高），不是 contain() 之后的结果。
    传缩放后的尺寸会让框按错误比例放大并飘出图片——S05 的圈就是这么跑到天空上的。
    """
    sx, sy = rect[2] / src_w, rect[3] / src_h
    return (rect[0] + int(box[0] * sx), rect[1] + int(box[1] * sy),
            rect[0] + int(box[2] * sx), rect[1] + int(box[3] * sy))


# ---------------------------------------------------------------- 纸张与页眉
_PAPER: Image.Image | None = None


def paper() -> Image.Image:
    """暖纸底：极轻的暗角 + 一点纸纹噪声，整片复用同一张。"""
    global _PAPER
    if _PAPER is None:
        rng = np.random.default_rng(20261101)
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        cx, cy = W * 0.5, H * 0.42
        r = np.sqrt(((x - cx) / W) ** 2 + ((y - cy) / H) ** 2)
        vig = 1.0 - 0.055 * np.clip(r * 1.55, 0, 1) ** 2
        noise = rng.normal(0.0, 1.9, (H, W)).astype(np.float32)
        base = np.array(PAPER, dtype=np.float32)[None, None, :]
        arr = base * vig[..., None] + noise[..., None]
        _PAPER = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    return _PAPER.copy()


_ICON: Image.Image | None = None


def icon() -> Image.Image:
    """右上角圆形图标（一次生成，全片复用）。"""
    global _ICON
    if _ICON is None:
        src = Image.open(asset("assets/cover/ED.png")).convert("RGBA")
        s = 78
        src = src.resize((s, s), Image.LANCZOS)
        mask = Image.new("L", (s * 4, s * 4), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
        mask = mask.resize((s, s), Image.LANCZOS)
        out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        out.paste(src, (0, 0), mask)
        ring = ImageDraw.Draw(out)
        ring.ellipse((0, 0, s - 1, s - 1), outline=(214, 200, 176, 255), width=2)
        _ICON = out
    return _ICON


def header(im: Image.Image, tag: str, title: str) -> Image.Image:
    """全片唯一的页眉：红色小竖标 + 字距小标签 + 衬线标题 + 右上圆图标 + 细线。"""
    d = ImageDraw.Draw(im)
    d.rectangle((MARGIN, 52, MARGIN + 5, 104), fill=RED)
    tracked(d, (MARGIN + 26, 54), tag, 20, GOLD, track=4)
    d.text((MARGIN + 24, 108), title, font=serif(50, True), fill=INK, anchor="lm")
    ic = icon()
    im.paste(ic, (W - MARGIN - ic.width, 46), ic)
    d.line([(MARGIN, HEADER_H), (W - MARGIN, HEADER_H)], fill=HAIR, width=1)
    d.line([(MARGIN, HEADER_H), (MARGIN + 148, HEADER_H)], fill=RED, width=3)
    return im


def page(tag: str, title: str) -> Image.Image:
    return header(paper(), tag, title)


def footer(im: Image.Image, idx: int, total: int, g: float) -> Image.Image:
    """页脚：细进度条 + 页码 + 作品小字。"""
    d = ImageDraw.Draw(im)
    y = H - 32
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=(231, 223, 209), width=1)
    n = int((W - 2 * MARGIN) * clamp(g))
    if n > 0:
        d.line([(MARGIN, y), (MARGIN + n, y)], fill=RED, width=2)
    tracked(d, (MARGIN, H - 76), "伟大工程 · Towards Victory", 17, FAINT, track=2)
    s = f"{idx:02d} / {total:02d}"
    wpx = sum(d.textlength(c, font=font(17, False)) for c in s) + 2 * (len(s) - 1)
    tracked(d, (W - MARGIN - wpx, H - 76), s, 17, FAINT, track=2)
    return im


# ---------------------------------------------------------------- 说明栏
def _notes_plan(d, notes, panel_w: int, size: int, head: int):
    """预算每条的高度，返回 [(kind, txt, font, lines, indent, block_h)]。"""
    plan, n = [], 0
    for kind, txt in notes:
        if kind == "h":
            f, indent = serif(head, True), 0
            lh = int(head * 1.5)
        else:
            n += 1
            f = font(size, True) if kind in ("r", "b") else font(size)
            indent = 58
            lh = int(size * 1.46)
        lines = wrap(d, txt, f, panel_w - indent)
        gap = 30 if kind == "h" else 20
        plan.append((kind, txt, f, lines, indent, lh * len(lines) + gap, lh, n))
    return plan


def side_notes(im, notes, *, x=None, top=None, w=None, size=34, head=42,
               center_on=None, t=0.0, t0=1.0, step=0.42, fade=0.5) -> Image.Image:
    """右侧说明栏。每条按 t0 + i*step 依次淡入上浮。"""
    panel_w = w or NOTE_W
    px = x if x is not None else (W - MARGIN - panel_w)
    d = ImageDraw.Draw(im)
    plan = _notes_plan(d, notes, panel_w, size, head)
    total_h = sum(p[5] for p in plan)
    if center_on is not None:
        y = center_on[1] + (center_on[3] - total_h) // 2
    else:
        y = top if top is not None else TOPBAR_BOTTOM + 90
    for i, (kind, txt, f, lines, indent, bh, lh, num) in enumerate(plan):
        a = ease(prog(t, t0 + i * step, fade))
        if a <= 0:
            y += bh
            continue
        dy = int(14 * (1 - a))
        col = {"h": INK, "r": RED, "b": BLUE, "g": MUTED}.get(kind, INK)
        if kind == "h":
            d.text((px, y + dy), lines[0], font=f, fill=lerp(PAPER, INK, a), anchor="la")
            for k, ln in enumerate(lines[1:], 1):
                d.text((px, y + dy + k * lh), ln, font=f, fill=lerp(PAPER, INK, a), anchor="la")
            # 标题下的短线
            line_at(d, (px, y + dy + lh * len(lines) + 2),
                    (px + 54, y + dy + lh * len(lines) + 2), ease(prog(t, t0 + i * step, 0.5)),
                    lerp(PAPER, GOLD, a), width=2)
        else:
            r = 19
            badge(im, (px + r, y + dy + lh // 2), num, r=r,
                  fill={"r": RED, "b": BLUE, "g": MUTED}.get(kind, INK),
                  alpha=a, scale=0.7 + 0.3 * a)
            for k, ln in enumerate(lines):
                d.text((px + indent, y + dy + k * lh), ln, font=f,
                       fill=lerp(PAPER, col, a), anchor="la")
        y += bh
    return im


def caption(im, text, xy=None, *, size=28, color=MUTED, alpha=1.0, anchor="mm"):
    d = ImageDraw.Draw(im)
    if xy is None:
        xy = (W // 2, H - 96)
    d.text(xy, text, font=font(size), fill=lerp(PAPER, color, alpha), anchor=anchor)
    return im


def big_line(im, x, y, w, f, color=RED, thick=4):
    d = ImageDraw.Draw(im)
    line_at(d, (x, y), (x + w, y), f, color, width=thick)
    return im


# ---------------------------------------------------------------- 音轨与时间轴
# v4：音轨由 assets/1030-movie/音频 1_2.wav 做后处理后得到（见 build_audio_chain()），
# 长 126.175s。下面所有时间点都来自该音轨的**词级时间戳**，不是估算。
AUDIO_SRC = "assets/1030-movie/音频 1_2.wav"
AUDIO_WAV = OUT / "great_projects_1.4_audio.wav"
AUDIO_DUR = 126.175

# 降噪链：高通去低频轰鸣 → afftdn 自适应降噪 → anlmdn 抹残余宽带嘶声
# → 320Hz 减一点箱音、3kHz 提一点清晰度 → de-esser 压齿音
# → 轻压缩收动态 → EBU R128 归一到 -16 LUFS → 限幅。
def build_audio_chain() -> str:
    return ",".join([
        "highpass=f=85:poles=2",
        "afftdn=nf=-55:nr=30:tn=1",
        "anlmdn=s=7:p=0.002:r=0.002:m=15",
        "equalizer=f=320:t=q:w=1.0:g=-1.5",
        "equalizer=f=3000:t=q:w=1.2:g=1.0",
        "deesser=i=0.35",
        "acompressor=threshold=-20dB:ratio=2.5:attack=12:release=180:makeup=1.5",
        f"loudnorm=I=-16:TP=-1.5:LRA=11:linear=true",
        "alimiter=limit=0.94",
    ])


# ---- 镜头边界：全部落在语音段落的静音处（帧号，30fps） ----
# 顺序与画面内容不变，只调切换点，让每一页盖住它对应的那段口播。
SCENE_FRAMES = [
    ("T00", 195),   # 0.00   片头 · 大家好 / 更到 1.4 了
    ("S01", 315),   # 6.50   评论区点名要的 + 三件事
    ("S02", 276),   # 17.00  界面：旧版铺满
    ("S04", 393),   # 26.20  界面：新版按钮 / 面板 / 悬停
    ("S05", 195),   # 39.30  原画：凭空生成、不够精细
    ("S06", 277),   # 45.80  原画：真实素材 → 油画卡通
    ("S07", 263),   # 55.03  五座新工程
    ("S08", 180),   # 63.80  机制：移民吸引力 2 → 1
    ("S09", 283),   # 69.80  扩建自选 / 朴素落成 / 重选
    ("S10", 228),   # 79.23  八步抉择删掉
    ("S11", 286),   # 86.83  倾向由仪式决定
    ("S12", 225),   # 96.37  落成后能换 / 淡忘
    ("S13", 452),   # 103.87 AI 自己会建奇观
    ("S14", 217),   # 118.93 结尾
]
SCENE_DUR = [(s, round(n / FPS, 4)) for s, n in SCENE_FRAMES]
TOTAL = sum(n for _, n in SCENE_FRAMES) / FPS   # 精确值，避免取整后断言不过
START: dict[str, float] = {}
_t = 0.0
for _s, _n in SCENE_FRAMES:
    START[_s] = _t
    _t += _n / FPS

# ---- 字幕：时间取自词级时间戳，文本按语义校正后人工定稿 ----
# (start, end, text)。end 已留 0.15s 左右余量，避免字幕贴脸切换。
SUBTITLES = [
    (1.12, 2.70, "各位观众朋友们，大家好。"),
    (3.14, 6.45, "我们伟大工程模组，也是更到 1.4 了。"),
    (6.80, 7.95, "这次更新，"),
    (8.04, 11.10, "主要就是把评论区点名要的做了一下。"),
    (11.90, 15.45, "主要就是界面、原画和机制三个方面。"),
    (17.00, 18.05, "先说界面吧。"),
    (18.54, 21.30, "以前呢，这个是展开的。"),
    (21.48, 24.95, "每个奇观的条件、修正什么的，都是铺满的。"),
    (25.02, 26.18, "这个其实不是很好看。"),
    (26.22, 28.32, "现在是改成一个按钮。"),
    (28.36, 29.75, "你点一下，"),
    (30.98, 33.18, "就可以切换右边是否显示具体的面板。"),
    (33.24, 36.70, "那你要看效果，就停在等级和仪式名上，"),
    (36.78, 38.85, "就只展开对应奇观的版本。"),
    (39.32, 41.18, "第二件是原画。"),
    (41.24, 43.42, "就那一批是凭空生成的，"),
    (43.46, 45.74, "这 AI 画得不够精细。"),
    (45.78, 46.95, "现在这一批，"),
    (47.06, 49.20, "每一张都是从一张真实素材开始的。"),
    (49.32, 52.45, "然后把它的风格"),
    (52.92, 54.32, "改成油画卡通的风格。"),
    (55.04, 57.20, "这一版新增了五座伟大工程。"),
    (57.30, 58.98, "有的是通用的，"),
    (59.12, 62.66, "剩下四个是独特的。"),
    (63.78, 65.26, "第三件是机制方面。"),
    (65.38, 68.02, "那移民吸引力也是从二改成一了。"),
    (68.08, 69.62, "以前那个有点太夸张。"),
    (69.78, 73.66, "那扩建现在也是仪式可以自己挑了，"),
    (74.24, 75.80, "所以还加了一个朴素落成，"),
    (75.84, 77.40, "可以不用等时间，直接完成。"),
    (77.54, 78.54, "扩建完了也可以重选。"),
    (79.22, 82.10, "那仪式以前那个八步的"),
    (82.14, 83.44, "抉择也删掉了，"),
    (83.46, 85.05, "因为这个没有什么意思。"),
    (85.18, 86.20, "很多人也抱怨。"),
    (86.82, 89.94, "最后就是倾向，改成由仪式决定了。"),
    (90.00, 93.08, "选每个风格，国家的价值观就往那边倾向。"),
    (93.16, 95.70, "不想选也可以选朴素，也可以省时间。"),
    (96.34, 99.16, "最后呢，已经落成的仪式也可以随时更换。"),
    (99.82, 102.14, "但是呢，如果你一个既有的仪式，"),
    (102.18, 103.40, "一百年是会被淡忘的。"),
    (103.84, 104.75, "最后就是 AI。"),
    (104.86, 107.62, "这一版给 AI 补上了自己建奇观的逻辑。"),
    (107.66, 109.92, "一局五百多年，"),
    (110.44, 114.14, "AI 世界里的奇观从 66 座变成了 257 座。"),
    (114.62, 116.45, "那么进攻 AI、夺取奇观，"),
    (116.48, 118.90, "也真正成为了一种策略。"),
    (118.92, 121.52, "模组已经在创意工坊更新了。"),
    (121.54, 125.70, "大家有什么问题，欢迎留言，也欢迎加群来告诉我。"),
]

# 分镜头：一个场景一个镜头，时长与 SCENE_FRAMES 一致。
SHOT_PLAN = [(s, n / FPS, s) for s, n in SCENE_FRAMES]

_CUT_FRAME: list[int] = []
_f = 0
for _s, _n in SCENE_FRAMES:
    _CUT_FRAME.append(_f)
    _f += _n


def _snap(a: float, b: float) -> tuple[float, float]:
    """把字幕首尾收进同一页画面。

    镜头之间是 8 帧交叉溶解，旧页在切换点之前就已经淡掉了；所以：
      * 结尾只溢进切换点后 <=0.30s（溶解期）→ 拉回切换点；
      * 开头比切换点早 <=0.35s（还没轮到它说话）→ 推到切换点。
    超过这个范围说明字幕横跨了两页，属于切分问题，不该硬修。
    判断一律换算成帧号，避免 79.233 与 79.23333 这类浮点误差。
    """
    edges = [n for n in _CUT_FRAME]
    fa, fb = round(a * FPS), round(b * FPS)
    for e in edges:
        if 0 < fb - e <= round(0.30 * FPS):
            fb = e
        if 0 < e - fa <= round(0.35 * FPS):
            fa = e
    return fa / FPS, fb / FPS


def build_subs():
    subs = []
    for a, b, t in SUBTITLES:
        a, b = _snap(a, b)
        subs.append({"start": round(a, 3), "end": round(b, 3), "text": t})
    return subs


def _check_subs():
    """字幕不许重叠、不许超出镜头时间轴、每条都要读得完。"""
    prev_end = -1.0
    for a, b, t in SUBTITLES:
        assert b > a, f"时长倒挂：{t}"
        assert a >= prev_end - 1e-6, f"与前一条重叠：{t}"
        assert b <= AUDIO_DUR + 1e-6, f"超出音轨：{t}"
        assert b - a >= 0.65, f"太短，读不完：{t}"
        prev_end = b
    assert abs(SUBTITLES[-1][1] - AUDIO_DUR) < 1.5, "末条字幕与音轨结尾差太多"


def ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(subs, path: Path):
    out = [f"{i}\n{ts(s['start'])} --> {ts(s['end'])}\n{s['text']}\n"
           for i, s in enumerate(subs, 1)]
    path.write_text("\n".join(out), encoding="utf-8")


# ---------------------------------------------------------------- 镜头表
SHOTS: list[dict] = []
_BASE: dict[str, Image.Image] = {}


def base(sid: str, build) -> Image.Image:
    """每个镜头的静态底板只构建一次（纸、页眉、图片、不动文字）。"""
    if sid not in _BASE:
        _BASE[sid] = build()
    return _BASE[sid]


def shot(sid: str, dur: float, scene: str | None, fn):
    SHOTS.append({"id": sid, "dur": dur, "scene": scene, "fn": fn,
                  "frames": int(round(dur * FPS))})


def _g(sid: str, t: float) -> float:
    """全局进度 0..1，用于页脚进度条。"""
    return clamp((START[sid] + t) / TOTAL)


# --- T00 片头 -------------------------------------------------------------
def t00(t, dur):
    im = page("序 · PROLOGUE", "伟大工程 · 1.4 更新")
    im = footer(im, 1, len(SHOTS), _g("T00", t))

    art = load("assets/generated_wonders/tv_wonder_unique_suzhou_classical_gardens.png")
    art = contain(art, 1080, 700)
    # 图上压一层暗色衬底，让标题跳出来；衬底与图一起淡入
    scrim = Image.new("RGB", art.size, (14, 16, 20))
    art = Image.blend(art, scrim, 0.52)
    blk = card(art)
    ax = (W - art.width) // 2
    ay = TOPBAR_BOTTOM + (AVAIL_H - art.height) // 2 - 6
    a = ease(prog(t, 0.15, 1.1))
    paste_card(im, blk, ax, ay, alpha=a)
    if a < 0.999:
        return im

    d = ImageDraw.Draw(im)
    cx, cy = ax + art.width // 2, ay + art.height // 2
    # 标题：字距拉开，逐字升起
    ta = ease(prog(t, 0.9, 0.9))
    if ta > 0:
        d.text((cx + 8, cy - 96 + int(18 * (1 - ta))), "伟大工程", font=serif(126, True),
               fill=(252, 248, 240), anchor="mm")
    rw = ease_out(prog(t, 0.6, 0.8))
    if rw > 0:
        half = int(150 * rw)
        d.line([(cx - half, cy + 4), (cx + half, cy + 4)], fill=RED, width=5)
    sa = ease(prog(t, 1.5, 0.8))
    if sa > 0:
        d.text((cx, cy + 74 + int(14 * (1 - sa))), "1.4 更新", font=serif(62, True),
               fill=(255, 226, 218), anchor="mm")
    ca = ease(prog(t, 2.3, 0.8))
    if ca > 0:
        d.text((cx, cy + 172), "界面 · 原画 · 机制", font=font(34),
               fill=lerp((16, 16, 16), (208, 190, 176), ca), anchor="mm")
    return im


# --- S01 开场 + 三件事 ----------------------------------------------------
S01_ROWS = [("01", "界面", "点开才挂出，一座一行", RED),
            ("02", "原画", "一百九十多张，全部重绘", GOLD),
            ("03", "机制", "扩建自选、仪式重做、AI 主动建", BLUE)]


def _s01_base() -> Image.Image:
    im = page("总览 · OVERVIEW", "伟大工程 · 1.4 更新")
    d = ImageDraw.Draw(im)
    # 左右分栏的竖向细线
    d.line([(W // 2 - 44, TOPBAR_BOTTOM + 70), (W // 2 - 44, CONTENT_BOTTOM - 40)],
           fill=HAIR, width=1)
    return im


def s01(t, dur):
    im = base("S01", _s01_base).copy()
    im = footer(im, 2, len(SHOTS), _g("S01", t))
    d = ImageDraw.Draw(im)

    x = MARGIN + 8
    y = TOPBAR_BOTTOM + 170
    a1 = ease(prog(t, 0.2, 0.7))
    if a1 > 0:
        d.text((x, y + int(16 * (1 - a1))), "评论区点名要的", font=serif(84, True),
               fill=lerp(PAPER, INK, a1), anchor="la")
    a2 = ease(prog(t, 0.75, 0.7))
    if a2 > 0:
        d.text((x, y + 132 + int(16 * (1 - a2))), "这次都做了。", font=serif(84, True),
               fill=lerp(PAPER, RED, a2), anchor="la")
    line_at(d, (x + 6, y + 268), (x + 306, y + 268), ease_out(prog(t, 1.4, 0.7)), RED, width=5)
    a3 = ease(prog(t, 1.8, 0.6))
    if a3 > 0:
        d.text((x, y + 312), "本期全部为实机截图", font=font(32),
               fill=lerp(PAPER, MUTED, a3), anchor="la")

    xr = W // 2 + 8
    y0 = TOPBAR_BOTTOM + 118
    for i, (num, name, desc, col) in enumerate(S01_ROWS):
        st = 2.2 + i * 0.55
        a = ease(prog(t, st, 0.55))
        if a <= 0:
            continue
        yy = y0 + i * 176 + int(18 * (1 - a))
        line_at(d, (xr, yy), (xr + 700, yy), ease_out(prog(t, st - 0.1, 0.6)),
                lerp(PAPER, HAIR, a), width=1)
        d.text((xr, yy + 34), num, font=serif(30, True), fill=lerp(PAPER, FAINT, a), anchor="la")
        d.text((xr + 84, yy + 24), name, font=serif(58, True), fill=lerp(PAPER, INK, a), anchor="la")
        d.text((xr + 250, yy + 46), desc, font=font(30), fill=lerp(PAPER, MUTED, a), anchor="la")
        d.rectangle((xr, yy + 96, xr + 60 + int(120 * a), yy + 99), fill=lerp(PAPER, col, a * 0.9))
    line_at(d, (xr, y0 + 3 * 176), (xr + 700, y0 + 3 * 176), ease_out(prog(t, 3.9, 0.7)),
            HAIR, width=1)
    return im


# --- S02 界面：旧版 -------------------------------------------------------
LOC = "docs/marketing/assets/location_zh.jpg"
LOC_BOX = (845, 645, 1200, 745)   # 国家修正 / 本地修正 两列（原图坐标）


def _s02_base():
    im = page("界面 · UI", "旧版：悬停就铺开")
    src = load(LOC)
    src = contain(src, IMG_W, AVAIL_H)
    rect = (MARGIN, TOPBAR_BOTTOM + (AVAIL_H - src.height) // 2, src.width, src.height)
    paste_card(im, card(src), rect[0], rect[1])
    return im, rect, src.size


def s02(t, dur):
    blk, rect, _ = base("S02", _s02_base)
    im = blk.copy()
    im = footer(im, 3, len(SHOTS), _g("S02", t))
    box = _map(LOC_BOX, rect, 1305, 955)
    g = ease_out(prog(t, 0.7, 0.8))
    brackets(im, box, RED, width=4, arm=30, alpha=g, grow=0.35 + 0.65 * g)
    s = pop(t, 1.4)
    if s > 0:
        badge(im, (box[0] - 30, box[1] - 22), 1, r=21, alpha=clamp(s), scale=s)
    side_notes(im, [
        ("h", "悬停就铺开"),
        ("r", "一屏摊满"),
        ("g", "每座的条件、国家修正、本地修正全给你铺开"),
        ("g", "奇观一多，既看不清，也没法横向比较"),
    ], center_on=rect, t=t, t0=1.8, step=0.75)
    return im


# --- S04 界面：新版 -------------------------------------------------------
C01 = "assets/1030-movie/C01.png"
C02 = "assets/1030-movie/C02.png"
C03 = "assets/1030-movie/C03.png"
C04 = "assets/1030-movie/C04.png"
C05 = "assets/1030-movie/C05.png"

PNL = (568, 288, 987, 772)      # 面板整体（原图坐标 1920x1080）
ROW = (568, 292, 987, 450)      # 托普卡帕宫那一行


def _s04_base():
    im = page("界面 · UI", "新版：一座一行")
    src = load(C02)
    src = contain(src, IMG_W, AVAIL_H)
    rect = (MARGIN, TOPBAR_BOTTOM + (AVAIL_H - src.height) // 2, src.width, src.height)
    paste_card(im, card(src), rect[0], rect[1])
    return im, rect


def s04(t, dur):
    blk, rect = base("S04", _s04_base)
    im = blk.copy()
    im = footer(im, 4, len(SHOTS), _g("S04", t))
    pnl = _map(PNL, rect, 1920, 1080)
    row = _map(ROW, rect, 1920, 1080)

    g = ease_out(prog(t, 0.6, 0.8))
    brackets(im, pnl, RED, width=4, arm=30, alpha=g, grow=0.35 + 0.65 * g)
    s = pop(t, 1.3)
    if s > 0:
        badge(im, (pnl[0] - 34, pnl[1] + 40), 1, r=21, alpha=clamp(s), scale=s)

    # 悬停：这一行亮一下，然后收束
    sweep(im, row, prog(t, 4.6, 1.2), strength=0.22)
    g2 = ease_out(prog(t, 5.4, 0.7))
    brackets(im, row, BLUE, width=4, arm=24, alpha=g2, grow=0.5 + 0.5 * g2)
    s2 = pop(t, 5.9)
    if s2 > 0:
        badge(im, (row[0] - 34, row[3] - 34), 2, r=21, fill=BLUE,
              alpha=clamp(s2), scale=s2)

    side_notes(im, [
        ("h", "点一下，挂出这块面板"),
        ("r", "一座一行"),
        ("g", "原画、名字、等级都在这一行里"),
        ("b", "悬停仪式名，只展开这一份"),
    ], center_on=rect, t=t, t0=1.7, step=1.35)
    return im


# --- S05 原画：旧版 -------------------------------------------------------
PISA_OLD = "assets/historical/review/original_ai/tv_wonder_unique_leaning_tower_of_pisa.png"


def _s05_base():
    im = page("原画 · ART", "旧版：凭空生成的")
    art = load(PISA_OLD)
    src_size = art.size                 # 原图尺寸：给 _map 换算用
    art = contain(art, IMG_W, AVAIL_H)
    rect = (MARGIN, TOPBAR_BOTTOM + (AVAIL_H - art.height) // 2, art.width, art.height)
    paste_card(im, card(art), rect[0], rect[1])
    return im, rect, src_size


def s05(t, dur):
    blk, rect, size = base("S05", _s05_base)
    im = blk.copy()
    im = footer(im, 5, len(SHOTS), _g("S05", t))
    d = ImageDraw.Draw(im)
    ring = _map((1082, 196, 1352, 664), rect, size[0], size[1])
    f = ease_out(prog(t, 0.8, 1.4))
    if f > 0:
        d.arc([ring[0], ring[1], ring[2], ring[3]], start=-90, end=-90 + int(360 * f),
              fill=RED, width=5)
    s = pop(t, 2.1)
    if s > 0:
        badge(im, (ring[0] - 4, ring[1] + 96), 1, r=21, alpha=clamp(s), scale=s)
    side_notes(im, [
        ("h", "好看，但经不起细看"),
        ("r", "拱廊层数对不上"),
        ("g", "这类错误，只有真素材才能杜绝"),
    ], center_on=rect, t=t, t0=1.2, step=1.0)
    return im


# --- S06 原画：素材 → 成品 ------------------------------------------------
PISA_PHOTO = "assets/historical/比萨斜塔.jpg"
PISA_NEW = "assets/historical/processed/比萨斜塔_ai_cartoon.png"


def _s06_base():
    im = page("原画 · ART", "从一张真素材开始")
    slots = [(MARGIN, 430), (MARGIN + 430 + 84, 430), (MARGIN + 430 * 2 + 84 * 2 + 40, 660)]
    return im, slots


def s06(t, dur):
    blk, slots = base("S06", _s06_base)
    im = blk.copy()
    im = footer(im, 6, len(SHOTS), _g("S06", t))
    d = ImageDraw.Draw(im)
    items = [(PISA_PHOTO, "① 真实照片", "起点", INK),
             (PISA_NEW, "② 同机位重绘", "只换画风，不换建筑", RED),
             (PISA_OLD, "③ 旧版", "凭空生成", MUTED)]
    heights = [566, 566, 420]
    placed = []
    for i, ((rel, label, note, col), (sx, sw), hh) in enumerate(zip(items, slots, heights)):
        art = load(rel)
        art = contain(art, sw, hh)
        x = sx + (sw - art.width) // 2
        y = TOPBAR_BOTTOM + 34 + (566 - art.height) // 2
        a = ease(prog(t, 0.1 + i * 0.55, 0.75))
        if a > 0:
            paste_card(im, card(art), x, y + int(26 * (1 - a)), alpha=a)
        placed.append((x, y, art.width, art.height))

    # 箭头的两个落点：卡 1 右侧 → 卡 2 左侧
    if placed[1][2] > 0:
        p0 = (placed[0][0] + placed[0][2] + 10, placed[0][1] + placed[0][3] // 2)
        p1 = (placed[1][0] - 14, p0[1])
        arrow(im, p0, p1, prog(t, 1.5, 0.8), GOLD, width=4, head=16)

    # 卡 3 上的红叉
    x, y, aw, ah = placed[2]
    f = ease_out(prog(t, 2.4, 0.55))
    if f > 0:
        cx, cy = x + aw // 2, y + ah // 2
        rr = int(min(aw, ah) * 0.16)
        d = ImageDraw.Draw(im)
        line_at(d, (cx - rr, cy - rr), (cx + rr, cy + rr), f, RED, width=7)
        line_at(d, (cx + rr, cy - rr), (cx - rr, cy + rr), f, RED, width=7)

    # 标签
    for i, ((rel, label, note, col), (sx, sw)) in enumerate(zip(items, slots)):
        a = ease(prog(t, 0.5 + i * 0.55, 0.6))
        if a <= 0:
            continue
        x, y, aw, ah = placed[i]
        cx = x + aw // 2
        by = TOPBAR_BOTTOM + 34 + 566 + 50
        d.text((cx, by), label, font=font(34, True),
               fill=lerp(PAPER, col, a), anchor="mm")
        d.text((cx, by + 44), note, font=font(26),
               fill=lerp(PAPER, MUTED, a), anchor="mm")
    return im


# --- S07 五座新工程 -------------------------------------------------------
NEW_WONDERS = [
    ("assets/generated_wonders/tv_wonder_grand_garden_complex.png", "园林群", "通用原型"),
    ("assets/generated_wonders/tv_wonder_unique_amber_room.png", "琥珀宫", "独特奇观"),
    ("assets/generated_wonders/tv_wonder_unique_parthenon.png", "帕特农神庙", "独特奇观"),
    ("assets/generated_wonders/tv_wonder_unique_bangkok_grand_palace.png", "曼谷大皇宫", "独特奇观"),
    ("assets/generated_wonders/tv_wonder_unique_wat_arun.png", "郑王庙", "独特奇观"),
]
GAP7, CELLW7, CELLH7 = 52, 512, 268


def _s07_base():
    return page("机制 · MECHANICS", "新增五座伟大工程")


def s07(t, dur):
    im = base("S07", _s07_base).copy()
    im = footer(im, 7, len(SHOTS), _g("S07", t))
    d = ImageDraw.Draw(im)
    rows = [NEW_WONDERS[:3], NEW_WONDERS[3:]]
    y = TOPBAR_BOTTOM + 12
    k = 0
    for row in rows:
        total_w = CELLW7 * len(row) + GAP7 * (len(row) - 1)
        x0 = (W - total_w) // 2
        for i, (rel, name, kind) in enumerate(row):
            art = load(rel)
            art = contain(art, CELLW7, CELLH7)
            x = x0 + i * (CELLW7 + GAP7) + (CELLW7 - art.width) // 2
            yy = y + (CELLH7 - art.height) // 2
            a = ease(prog(t, 0.15 + k * 0.28, 0.7))
            if a > 0:
                paste_card(im, card(art), x, yy + int(22 * (1 - a)), alpha=a)
                cx = x + art.width // 2
                d.text((cx, y + CELLH7 + 38), name, font=serif(34, True),
                       fill=lerp(PAPER, INK, a), anchor="mm")
                col = RED if kind == "通用原型" else FAINT
                tracked(d, (cx, y + CELLH7 + 66), kind, 17, col, track=2, anchor="ma", alpha=a)
            k += 1
        y += CELLH7 + 108
    a = ease(prog(t, 2.4, 0.7))
    if a > 0:
        d.text((W // 2, H - 96), "通用原型可复用；独特奇观绑定真实历史地点",
               font=font(27), fill=lerp(PAPER, MUTED, a), anchor="mm")
    return im


# --- S08 施工期移民吸引力 -------------------------------------------------
def _s08_base():
    im = page("机制 · MECHANICS", "施工期吸引力")
    src = contain(load(C05), IMG_W, AVAIL_H)
    rect = (MARGIN, TOPBAR_BOTTOM + (AVAIL_H - src.height) // 2, src.width, src.height)
    paste_card(im, card(src), rect[0], rect[1])
    return im, rect


def s08(t, dur):
    blk, rect = base("S08", _s08_base)
    im = blk.copy()
    im = footer(im, 8, len(SHOTS), _g("S08", t))
    box = _map((455, 600, 985, 900), rect, 1920, 1080)
    g = ease_out(prog(t, 0.5, 0.7))
    brackets(im, box, RED, width=4, arm=26, alpha=g, grow=0.4 + 0.6 * g)
    s = pop(t, 1.1)
    if s > 0:
        badge(im, (box[0] - 28, box[1] - 20), 1, r=21, alpha=clamp(s), scale=s)

    # 右栏：+2 划掉 → +1
    d = ImageDraw.Draw(im)
    px = W - MARGIN - NOTE_W
    y = TOPBAR_BOTTOM + 96
    tracked(d, (px, y), "施工期移民吸引力", 17, GOLD, track=3)
    d.text((px, y + 40), "地点修正", font=serif(40, True), fill=INK, anchor="la")

    a2 = ease(prog(t, 1.2, 0.5))
    if a2 > 0:
        d.text((px, y + 118), "+2", font=serif(104, True), fill=lerp(PAPER, (196, 190, 180), a2),
               anchor="la")
        strike = ease_out(prog(t, 1.9, 0.55))
        if strike > 0:
            line_at(d, (px - 6, y + 168), (px + 138, y + 168), strike, RED, width=5)
    a1 = ease(prog(t, 2.6, 0.6))
    if a1 > 0:
        d.text((px + 210, y + 118), "+1", font=serif(104, True), fill=lerp(PAPER, RED, a1),
               anchor="la")
        d.text((px + 214, y + 236), "现在", font=font(24), fill=lerp(PAPER, MUTED, a1), anchor="la")
    side_notes(im, [
        ("h", "施工该吸人"),
        ("g", "以前吸得有点过：+2 → +1"),
        ("b", "落成后另有一份落成加成"),
    ], x=px, top=y + 320, t=t, t0=2.9, step=0.85)
    return im


# --- S09 扩建自选 ---------------------------------------------------------
CER = "ai_gui_assessment/images/engineering/simp_chinese/ceremony-ready.png"
CER_BOX = (28, 495, 542, 942)        # 四行风格 + 风味文本
CER_ROWS = [(574, 650), (656, 732), (742, 818), (822, 878)]


def _crop(rel: str, box) -> Image.Image:
    return load(rel).crop(box)


def _s09_base():
    im = page("机制 · MECHANICS", "扩建自己挑")
    card_img = contain(_crop(CER, CER_BOX), IMG_W - 60, AVAIL_H - 40, up=1.55)
    rect = (MARGIN + 30, TOPBAR_BOTTOM + (AVAIL_H - card_img.height) // 2, card_img.width,
            card_img.height)
    paste_card(im, card(card_img), rect[0], rect[1])
    return im, rect


def s09(t, dur):
    blk, rect = base("S09", _s09_base)
    im = blk.copy()
    im = footer(im, 9, len(SHOTS), _g("S09", t))
    d = ImageDraw.Draw(im)
    sy = rect[3] / (CER_BOX[3] - CER_BOX[1])
    x0, x1 = rect[0] + 10, rect[0] + rect[2] - 10
    lit = -1
    for i, (y0, y1) in enumerate(CER_ROWS):
        st = 0.9 + i * 1.15
        yy0 = rect[1] + int((y0 - CER_BOX[1]) * sy)
        yy1 = rect[1] + int((y1 - CER_BOX[1]) * sy)
        p = prog(t, st, 0.55)
        if p <= 0:
            continue
        a = ease_out(p)
        # 选中条从左侧拉出
        line_at(d, (x0, yy1), (x0 + (x1 - x0) * 0.16, yy1), a, RED, width=3)
        brackets(im, (x0, yy0, x1, yy1), RED if i < 3 else GOLD, width=3, arm=22,
                 alpha=a * 0.9, grow=0.6 + 0.4 * a)
        badge(im, (x0 - 16, (yy0 + yy1) // 2), i + 1, r=18, alpha=a, scale=0.75 + 0.25 * a)
        lit = i
    side_notes(im, [
        ("h", "四个自己挑"),
        ("r", "三种风格"),
        ("b", "朴素落成"),
        ("g", "扩建完还能重新选"),
    ], center_on=rect, t=t, t0=1.1, step=1.15)
    return im


# --- S10 仪式一次确认 -----------------------------------------------------
RITUAL = "ai_gui_assessment/images/engineering/engineering_ceremony-stages.png"
RITUAL_BOX = (28, 660, 542, 1215)


def _s10_base():
    im = page("机制 · MECHANICS", "仪式一次确认")
    card_img = contain(_crop(RITUAL, RITUAL_BOX), IMG_W - 120, AVAIL_H - 30, up=1.5)
    rect = (MARGIN + 40, TOPBAR_BOTTOM + (AVAIL_H - card_img.height) // 2, card_img.width,
            card_img.height)
    paste_card(im, card(card_img), rect[0], rect[1])
    return im, rect


def s10(t, dur):
    blk, rect = base("S10", _s10_base)
    im = blk.copy()
    im = footer(im, 10, len(SHOTS), _g("S10", t))
    d = ImageDraw.Draw(im)
    px = W - MARGIN - NOTE_W
    y = TOPBAR_BOTTOM + 62
    tracked(d, (px, y), "以前", 17, GOLD, track=3)
    chips = ["① 掏钱硬上？", "② 还是先放一放？", "③ 再选一次？"]
    for i, s in enumerate(chips):
        st = 0.7 + i * 0.55
        a = ease(prog(t, st, 0.45))
        if a <= 0:
            continue
        yy = y + 36 + i * 66
        d.rounded_rectangle((px, yy, px + NOTE_W - 60, yy + 48), radius=6,
                            outline=lerp(PAPER, HAIR, a), width=2,
                            fill=lerp(PAPER, CARD, a))
        d.text((px + 18, yy + 24), s, font=font(27), fill=lerp(PAPER, MUTED, a), anchor="lm")
        st2 = ease_out(prog(t, 1.9 + i * 0.35, 0.5))
        if st2 > 0:
            tw = d.textlength(s, font=font(27)) + 4
            line_at(d, (px + 14, yy + 24), (px + 18 + tw, yy + 24), st2, RED, width=3)

    a = ease(prog(t, 3.4, 0.6))
    if a > 0:
        yy = y + 36 + 3 * 66 + 18
        d.rounded_rectangle((px, yy, px + NOTE_W, yy + 62), radius=8, fill=lerp(PAPER, RED, a))
        d.text((px + 22, yy + 31), "一次确认 · 二十四个月", font=font(30, True),
               fill=lerp(RED, (255, 250, 244), a), anchor="lm")
    side_notes(im, [
        ("g", "以前每个阶段都要选一次"),
        ("b", "现在整段仪式，一次确认"),
    ], x=px, top=y + 36 + 3 * 66 + 110, t=t, t0=4.1, step=0.8)
    return im


# --- S11 倾向 -------------------------------------------------------------
def _s11_base():
    im = page("机制 · MECHANICS", "倾向由仪式决定")
    y0, y1 = 938, 1200
    card_img = contain(_crop(CER, (28, y0, 542, y1)), IMG_W - 150, 486, up=1.9)
    rect = (MARGIN + 40, TOPBAR_BOTTOM + 44, card_img.width, card_img.height)
    paste_card(im, card(card_img), rect[0], rect[1])
    return im, rect, (y0, y1)


def s11(t, dur):
    blk, rect, (y0, y1) = base("S11", _s11_base)
    im = blk.copy()
    im = footer(im, 11, len(SHOTS), _g("S11", t))
    d = ImageDraw.Draw(im)
    sy = rect[3] / (y1 - y0)
    hl = (rect[0] + 6, rect[1] + int((1008 - y0) * sy),
          rect[0] + rect[2] - 6, rect[1] + int((1056 - y0) * sy))
    g = ease_out(prog(t, 0.8, 0.7))
    brackets(im, hl, RED, width=3, arm=20, alpha=g, grow=0.5 + 0.5 * g)
    s = pop(t, 1.4)
    if s > 0:
        badge(im, (hl[0] + 14, (hl[1] + hl[3]) // 2), 1, r=17, alpha=clamp(s), scale=s)

    # 下方的倾向轴：指针随时间右移。轴长跟卡片同宽，别缩成一小段
    ax0, ax1 = rect[0] + 66, rect[0] + rect[2] - 66
    ay = rect[1] + rect[3] + 116
    fa = ease(prog(t, 2.2, 0.6))
    if fa > 0:
        d.line([(ax0, ay), (ax0 + (ax1 - ax0) * fa, ay)], fill=lerp(PAPER, HAIR, fa), width=3)
        for k in range(5):
            xx = ax0 + (ax1 - ax0) * k / 4
            if xx <= ax0 + (ax1 - ax0) * fa:
                d.line([(xx, ay - 7), (xx, ay + 7)], fill=lerp(PAPER, HAIR, fa), width=2)
        d.text((ax0, ay + 26), "传统", font=font(22), fill=lerp(PAPER, FAINT, fa), anchor="la")
        d.text((ax1, ay + 26), "革新", font=font(22), fill=lerp(PAPER, FAINT, fa), anchor="ra")
    fp = ease(prog(t, 2.9, 3.2))
    if fp > 0:
        mx = ax0 + (ax1 - ax0) * (0.18 + 0.34 * fp)
        d.ellipse((mx - 9, ay - 9, mx + 9, ay + 9), fill=RED)
        tracked(d, (mx + 18, ay - 34), "+0.1 / 月", 22, RED, track=1)
    side_notes(im, [
        ("h", "选哪个风格，就往那个方向推"),
        ("g", "落成时一次性推一把，之后每月继续推"),
        ("g", "轴还没出现时：只是不带价值观的风格"),
        ("g", "不想选也可以跳过，之后再说"),
    ], x=W - MARGIN - NOTE_W + 40, top=TOPBAR_BOTTOM + 90, w=440, size=32,
        t=t, t0=1.0, step=1.1)
    return im


# --- S12 重仪式化 / 淡忘 --------------------------------------------------
FIN = "ai_gui_assessment/images/engineering/simp_chinese/finalized.png"
RER = "ai_gui_assessment/images/engineering/simp_chinese/reritual-ready.png"


def _s12_base():
    return page("机制 · MECHANICS", "落成之后也能换")


def s12(t, dur):
    im = base("S12", _s12_base).copy()
    im = footer(im, 12, len(SHOTS), _g("S12", t))
    d = ImageDraw.Draw(im)
    a = contain(_crop(FIN, (20, 452, 556, 684)), 700, 330, up=1.5)
    b = contain(_crop(RER, (28, 490, 542, 822)), 560, 330, up=1.5)
    gap = 150
    total = a.width + gap + b.width
    x0 = (W - total) // 2
    y0 = TOPBAR_BOTTOM + 60
    for i, imgs in enumerate([a, b]):
        a_ = ease(prog(t, 0.15 + i * 0.7, 0.7))
        if a_ <= 0:
            continue
        x = x0 if i == 0 else x0 + a.width + gap
        y = y0 + int(24 * (1 - a_))
        paste_card(im, card(imgs), x, y, alpha=a_)

    arrow(im, (x0 + a.width + 14, y0 + 165), (x0 + a.width + gap - 18, y0 + 165),
          prog(t, 1.6, 0.8), GOLD, width=4, head=18)
    for i, label in enumerate(["已落成 · 永久生效", "重新仪式化 · 再走一遍"]):
        al = ease(prog(t, 2.1 + i * 0.5, 0.6))
        if al <= 0:
            continue
        cx = x0 + (a.width // 2 if i == 0 else a.width + gap + b.width // 2)
        d.text((cx, y0 + 380), label, font=serif(33, True), fill=lerp(PAPER, INK, al),
               anchor="mm")

    al = ease(prog(t, 3.4, 0.7))
    if al > 0:
        wln = ease_out(prog(t, 3.4, 0.9))
        cy = y0 + 452
        line_at(d, (x0 + 30, cy), (x0 + total - 30, cy), wln, lerp(PAPER, RED, al * 0.75), width=2)
        d.text((W // 2, cy + 44), "一百年不做，仪式就淡忘了 —— 只剩座漂亮房子",
               font=font(34, True), fill=lerp(PAPER, RED, al), anchor="mm")
    return im


# --- S13 AI 自己会建奇观 --------------------------------------------------
def _ai_series():
    import csv
    rows = []
    with open(REPO / "docs/technical/observer_8fb6/snapshots.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append({
                "year": float(str(r["date"]).split(".")[0]),
                "final": int(float(r["final_count"] or 0)),
                "generic": int(float(r["generic_final_count"] or 0)),
            })
    return rows


def _s13_base():
    im = page("机制 · MECHANICS", "AI 自己会建奇观")
    return im


CW, CH = 1166, 700
_PL, _PR, _PT, _PB = 108, CW - 62, 196, 556
_YMAX = 280


def _chart_static(rows) -> Image.Image:
    """图表的静态部分（表头、网格、坐标、图例）：整段只画一次。"""
    cv = Image.new("RGB", (CW, CH), CARD)
    d = ImageDraw.Draw(cv)
    d.rectangle((0, 0, CW, 92), fill=DARK)
    d.text((36, 46), "AI 建成的伟大工程", font=serif(34, True), fill=(250, 246, 238), anchor="lm")
    tracked(d, (CW - 40, 38), "1338–1840 · 52 个年度快照", 19, (176, 170, 160), track=1,
            anchor="ra", bg=DARK)
    pl, pr, pt, pb = _PL, _PR, _PT, _PB
    ymax = _YMAX
    yrs = [r["year"] for r in rows]
    x0, x1 = min(yrs), max(yrs)
    for v in range(0, ymax + 1, 70):
        y = pb - (pb - pt) * v / ymax
        d.line([(pl, y), (pr, y)], fill=(233, 229, 221), width=1)
        d.text((pl - 16, y), str(v), font=font(20), fill=(146, 140, 130), anchor="rm")
    d.line([(pl, pb), (pr, pb)], fill=(206, 200, 190), width=2)
    for yr in range(1350, 1801, 50):
        x = pl + (pr - pl) * (yr - x0) / (x1 - x0)
        d.line([(x, pb), (x, pb + 7)], fill=(206, 200, 190), width=2)
        d.text((x, pb + 22), str(yr), font=font(19), fill=(146, 140, 130), anchor="mm")
    lg = CH - 34
    d.line([(pl, lg), (pl + 42, lg)], fill=BLUE, width=5)
    d.text((pl + 56, lg), "AI 建成总数", font=font(21), fill=(96, 90, 82), anchor="lm")
    d.line([(pl + 232, lg), (pl + 274, lg)], fill=RED, width=5)
    d.text((pl + 288, lg), "其中通用奇观", font=font(21), fill=(96, 90, 82), anchor="lm")
    return cv


def _chart(rows, t, t_draw=0.0):
    """在静态底图上叠动态部分：两条生长曲线、前端点、滚动数字、年份读数。"""
    cv = base("S13CHART", lambda: _chart_static(rows)).copy()
    d = ImageDraw.Draw(cv)
    pl, pr, pt, pb = _PL, _PR, _PT, _PB
    x0 = min(r["year"] for r in rows)
    x1 = max(r["year"] for r in rows)

    def xy(r, key):
        return (pl + (pr - pl) * (r["year"] - x0) / (x1 - x0),
                pb - (pb - pt) * r[key] / _YMAX)

    def head(f):
        k = clamp(f) * (len(rows) - 1)
        i = int(k)
        frac = k - i
        pts = [xy(r, key) for r in rows[:i + 1]]
        if i + 1 < len(rows) and frac > 0:
            a, b = rows[i], rows[i + 1]
            pa, pb_ = xy(a, key), xy(b, key)
            pts.append((pa[0] + (pb_[0] - pa[0]) * frac, pa[1] + (pb_[1] - pa[1]) * frac))
        return i, frac, pts

    fa = ease(prog(t, t_draw + 0.2, 8.0))
    key = "final"
    if fa > 0:
        i, frac, pts = head(fa)
        if len(pts) >= 2:
            d.polygon([(pl, pb)] + pts + [(pts[-1][0], pb)], fill=(232, 238, 248))
            d.line(pts, fill=BLUE, width=5, joint="curve")
        hy = pts[-1]
        d.ellipse((hy[0] - 8, hy[1] - 8, hy[0] + 8, hy[1] + 8), fill=BLUE,
                  outline=(255, 255, 255), width=2)

    fg = ease(prog(t, t_draw + 1.0, 7.2))
    key = "generic"
    if fg > 0:
        i, frac, pts = head(fg)
        if len(pts) >= 2:
            d.line(pts, fill=RED, width=5, joint="curve")
        hy = pts[-1]
        d.ellipse((hy[0] - 7, hy[1] - 7, hy[0] + 7, hy[1] + 7), fill=RED,
                  outline=(255, 255, 255), width=2)

    def val_at(k, f):
        j = clamp(f) * (len(rows) - 1)
        i = int(j)
        frac = j - i
        a = rows[i][k]
        b = rows[min(i + 1, len(rows) - 1)][k]
        return int(round(a + (b - a) * frac))

    d.text((pl + 4, 100), str(val_at("final", fa)), font=serif(60, True), fill=BLUE, anchor="la")
    d.text((pl + 4, 170), "AI 建成总数", font=font(20), fill=(150, 144, 134), anchor="la")
    d.text((pl + 250, 118), str(val_at("generic", fg)), font=serif(44, True), fill=RED, anchor="la")
    d.text((pl + 250, 170), "其中通用奇观", font=font(20), fill=(150, 144, 134), anchor="la")

    if fa > 0.02:
        hx = pl + (pr - pl) * clamp(fa)
        d.line([(hx, pt - 10), (hx, pb)], fill=(222, 216, 206), width=1)
        d.text((pl + 470, 132), f"{int(round(x0 + (x1 - x0) * clamp(fa)))} 年",
               font=serif(26, True), fill=DARK, anchor="la")
    if fa > 0.985:
        fp = xy(rows[-1], "final")
        d.text((fp[0] - 16, fp[1] - 22), f"{rows[-1]['final']} 座", font=serif(28, True),
               fill=BLUE, anchor="rs")
    return cv


def _s13_layout():
    return _chart(AI.rows, 0.0)


def s13(t, dur):
    im = base("S13", _s13_base).copy()
    im = footer(im, 13, len(SHOTS), _g("S13", t))
    ch = _chart(AI.rows, t, t_draw=0.6)
    x, y = MARGIN - 40 + CARD_PAD, TOPBAR_BOTTOM + (AVAIL_H - ch.height) // 2
    a = ease(prog(t, 0.1, 0.8))
    paste_card(im, card(ch), x, y, alpha=a)
    side_notes(im, [
        ("h", "进攻 AI 有了新理由"),
        ("g", "一局五百多年，AI 世界的奇观"),
        ("b", "66 座 → 257 座"),
        ("r", "新建成的大半是通用奇观"),
        ("g", "夺奇观，从此是一种策略"),
    ], center_on=(x, y, ch.width, ch.height), t=t, t0=1.2, step=2.4)
    return im


# --- S14 结尾 -------------------------------------------------------------
def _s14_base():
    return page("尾声 · OUTRO", "伟大工程 · 1.4 更新")


def s14(t, dur):
    im = base("S14", _s14_base).copy()
    im = footer(im, 14, len(SHOTS), _g("S14", t))
    d = ImageDraw.Draw(im)
    rows = [("创意工坊", "steamcommunity.com/sharedfiles/filedetails/?id=3766375743"),
            ("奇观图鉴", "hljsxk.github.io/eu5-towards-victory"),
            ("QQ 群", "1070041687　·　qm.qq.com/q/Yc2QwEsCgC")]
    y = TOPBAR_BOTTOM + 96
    for i, (name, val) in enumerate(rows):
        st = 0.2 + i * 0.5
        a = ease(prog(t, st, 0.6))
        if a <= 0:
            continue
        dx = int(24 * (1 - a))
        line_at(d, (MARGIN + 8, y), (MARGIN + 640, y), ease_out(prog(t, st - 0.1, 0.6)),
                lerp(PAPER, HAIR, a), width=1)
        d.text((MARGIN + 8 + dx, y + 26), name, font=serif(42, True), fill=lerp(PAPER, RED, a),
               anchor="la")
        d.text((MARGIN + 8 + dx, y + 96), val, font=font(29), fill=lerp(PAPER, INK, a),
               anchor="la")
        y += 176

    a = ease(prog(t, 2.0, 0.8))
    if a > 0:
        d.text((MARGIN + 8, y + 26), "有问题欢迎留言，或者加群找我。谢谢大家。",
               font=font(32), fill=lerp(PAPER, MUTED, a), anchor="la")

    art = load("assets/generated_wonders/tv_wonder_unique_suzhou_classical_gardens.png")
    art = contain(art, 560, 620)
    px = W - MARGIN - art.width - CARD_PAD + CARD_PAD
    py = TOPBAR_BOTTOM + (AVAIL_H - art.height) // 2
    aa = ease(prog(t, 0.5, 0.9))
    if aa > 0:
        paste_card(im, card(art), W - MARGIN - art.width, py, alpha=aa)
    return im


# ---------------------------------------------------------------- 预计算
class _NS:
    """镜头素材的挂载点。"""


AI = _NS()          # 注意：不要用 sXX 这类名字，会和同名镜头函数撞车


def prepare():
    BUILD.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    AI.rows = _ai_series()


def build_shotlist():
    SHOTS.clear()
    fns = {"T00": t00, "S01": s01, "S02": s02, "S04": s04, "S05": s05,
           "S06": s06, "S07": s07, "S08": s08, "S09": s09, "S10": s10, "S11": s11,
           "S12": s12, "S13": s13, "S14": s14}
    for sid, dur, scene in SHOT_PLAN:
        shot(sid, dur, scene, fns[sid])
    total = sum(s["dur"] for s in SHOTS)
    assert abs(total - TOTAL) < 1e-6, f"镜头总时长 {total} 与分镜表 {TOTAL} 不符"


# ---------------------------------------------------------------- 渲染
def _ffmpeg_writer(path: Path):
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-g", "60", str(path)]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def encode_segment(sh, path: Path, prev=None):
    proc = _ffmpeg_writer(path)
    n = sh["frames"]
    for i in range(n):
        t = i / FPS
        im = sh["fn"](t, sh["dur"])
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        im = im.convert("RGB")
        if prev is not None and i < XFADE:
            im = Image.blend(prev, im, (i + 1) / XFADE)
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"编码失败：{sh['id']}")


def _last_frame(sh) -> Image.Image:
    im = sh["fn"](max(0.0, sh["dur"] - 1.0 / FPS), sh["dur"])
    return im.convert("RGB")


def cmd_probe(only: str | None = None):
    prepare()
    build_shotlist()
    dst = BUILD / "probe3"
    dst.mkdir(parents=True, exist_ok=True)
    fr = [0.18, 0.52, 0.88]
    tiles = []
    for sh in SHOTS:
        for k, f in enumerate(fr):
            im = sh["fn"](sh["dur"] * f, sh["dur"]).convert("RGB")
            p = dst / f"{sh['id']}_{k}.png"
            im.save(p)
            if k == 1:
                tiles.append((sh["id"], im))
    cols, tw, th = 3, 620, 349
    rows_n = math.ceil(len(tiles) / cols)
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + 26)), (24, 24, 26))
    d = ImageDraw.Draw(sheet)
    for i, (sid, im) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * (th + 26)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x + 8, y + th + 3), sid, font=font(18), fill=(230, 230, 230))
    sheet.save(BUILD / "contact_sheet3.png")
    print(f"probe: {len(SHOTS)} shots x {len(fr)} frames -> {dst}")
    print(f"contact sheet -> {BUILD / 'contact_sheet3.png'}")


def _probe_ok(path: Path, want_dur: float) -> bool:
    if not path.exists() or path.stat().st_size < 10000:
        return False
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", str(path)],
                             capture_output=True, text=True, timeout=20)
        if out.returncode != 0:
            return False
        # 容差必须小于最小的镜头间差异，否则旧时长的片段会被误判为合格
        return abs(float(out.stdout.strip()) - want_dur) < 0.05
    except Exception:
        return False


def build_audio(force: bool = False):
    """从原始口播做降噪/均衡/响度，产出 48k 立体声 wav。"""
    if AUDIO_WAV.exists() and not force:
        print(f"audio 已存在，跳过：{AUDIO_WAV.name}", flush=True)
        return
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(REPO / AUDIO_SRC),
                    "-af", build_audio_chain(), "-ar", "48000", "-ac", "2",
                    "-c:a", "pcm_s16le", str(AUDIO_WAV)], check=True)
    print(f"audio -> {AUDIO_WAV}", flush=True)


def cmd_render(resume_override: bool = False, only: str | None = None,
               jobs: int = 1):
    from concurrent.futures import ProcessPoolExecutor

    prepare()
    build_shotlist()
    _check_subs()
    assert abs(TOTAL - AUDIO_DUR) < 0.05, (
        f"画面总长 {TOTAL}s 与音轨 {AUDIO_DUR}s 差得太多，检查 SCENE_FRAMES")
    build_audio(force=resume_override)
    seg_dir = BUILD / "segments_v3"
    seg_dir.mkdir(parents=True, exist_ok=True)

    lo, hi = 1, len(SHOTS)
    if only:
        a_, b_ = only.split("-")
        lo, hi = int(a_), int(b_)

    todo = []
    for i, sh in enumerate(SHOTS, 1):
        if not (lo <= i <= hi):
            continue
        p = seg_dir / f"{i - 1:03d}_{sh['id']}.mp4"
        if not resume_override and _probe_ok(p, sh["dur"]):
            print(f"[{i + 1}/{len(SHOTS)}] {sh['id']} 已存在，跳过", flush=True)
            continue
        todo.append((i - 1, p))

    if jobs > 1 and len(todo) > 1:
        # 并行时每个进程自己做转场用的上一镜末帧
        with ProcessPoolExecutor(max_workers=jobs) as ex:
            futs = []
            for i, p in todo:
                prev = _last_frame(SHOTS[i - 1]) if i > 0 else None
                sh = SHOTS[i]
                futs.append((i, ex.submit(_render_one, i, str(p), prev)))
            for i, f in futs:
                f.result()
                print(f"[{i + 1}/{len(SHOTS)}] {SHOTS[i]['id']} 完成", flush=True)
    else:
        for i, p in todo:
            prev = _last_frame(SHOTS[i - 1]) if i > 0 else None
            encode_segment(SHOTS[i], p, prev)
            print(f"[{i + 1}/{len(SHOTS)}] {SHOTS[i]['id']} {SHOTS[i]['dur']}s", flush=True)

    segs = [seg_dir / f"{i:03d}_{sh['id']}.mp4" for i, sh in enumerate(SHOTS)]
    missing = [p.name for p, sh in zip(segs, SHOTS) if not _probe_ok(p, sh["dur"])]
    if missing:
        print(f"还有 {len(missing)} 段未完成，暂不拼接：{missing[:6]}…")
        return

    lst = seg_dir / "list.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in segs), encoding="utf-8")

    content = OUT / "great_projects_1.4_content.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", "-an", "-movflags", "+faststart",
                    str(content)], check=True)

    subs = build_subs()
    srt = OUT / "great_projects_1.4_subtitle.srt"
    write_srt(subs, srt)

    muxed = OUT / "great_projects_1.4_with_subs.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-i", str(content), "-i", str(AUDIO_WAV), "-i", str(srt),
                    "-map", "0:v:0", "-map", "1:a:0", "-map", "2:s:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-c:s", "mov_text",
                    "-metadata:s:s:0", "language=chi",
                    "-metadata:s:a:0", "language=chi",
                    "-movflags", "+faststart",
                    str(muxed)], check=True)

    # 字幕轨在多数播放器里默认不打开，另出一份烧进画面的预览版
    burned = OUT / "great_projects_1.4_burned.mp4"
    style = ("FontName=Noto Sans CJK SC,FontSize=22,PrimaryColour=&H00F8F4EC,"
             "OutlineColour=&H00201410,BorderStyle=1,Outline=2.6,Shadow=0.6,"
             "MarginV=26,Alignment=2")
    esc = str(srt).replace("\\", "/").replace(":", "\\:")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-i", str(muxed),
                    "-vf", f"subtitles='{esc}':force_style='{style}'",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                    "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", str(burned)], check=True)

    (BUILD / "script.json").write_text(json.dumps(
        [{"start": a, "end": b, "text": t} for a, b, t in SUBTITLES],
        ensure_ascii=False, indent=2), encoding="utf-8")
    (BUILD / "edl.json").write_text(json.dumps(
        [{"id": s["id"], "scene": s["scene"], "start": round(START[s["id"]], 3), "dur": s["dur"]}
         for s in SHOTS], ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"content -> {content}")
    print(f"subtitle -> {srt}（{len(subs)} 条）")
    print(f"muxed   -> {muxed}")
    print(f"burned  -> {burned}")


def _render_one(i: int, path: str, prev):
    encode_segment(SHOTS[i], Path(path), prev)
    return i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--fresh", action="store_true", help="忽略已存在的片段，全部重渲")
    ap.add_argument("--only", default=None, help="只渲指定片段，如 011-015")
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args()
    if a.probe:
        cmd_probe()
    elif a.render:
        cmd_render(resume_override=a.fresh, only=a.only, jobs=a.jobs)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
