"""Native EU5 preview of Org_Logistics_Panel_Design.html, not live gameplay.

Only connectors are generated artwork. Panels, controls, fonts and icons use
the shared renderer's game/mod assets. Market and employment are explicit samples.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import engineering

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai_gui_assessment/images/org_logistics"
FIXTURE = ROOT / "ai_gui_assessment/fixtures/org_logistics.json"
PM = Path("in_game/common/production_methods/tv_engineering_department_production_methods.txt")
COLORS = {"ok": "2fb7d6", "mid": "e0b34a", "hi": "d9674f", "good": "7ec97e", "gold": "b39a65", "dim": "999ba8"}
FORMATS = {"ok": "color_concept", "mid": "color_yellow", "hi": "color_red", "good": "color_green", "gold": "color_yellow", "dim": "color_gray"}
CW, CG, CH, PITCH, CEND, MX, MW, TRUNK = 58, 8, 40, 48, 330, 350, 104, 482
GRAPH_HEIGHT = 544


def quote(value):
    return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"') + '"'


def text(x, y, w, value, size=13, color=None, align="left", h=22):
    if color:
        value = f'#{FORMATS[color]} {value}#!'
    return (f'text_single = {{ position = {{ {x} {y} }} size = {{ {w} {h} }} '
            f'autoresize = no fontsize = {size} fontsize_min = {size} '
            f'raw_text = {quote(value)} align = {align}|nobaseline }}')


def rgb(key):
    return " ".join(f"{int(COLORS[key][i:i+2], 16)/255:.4f}" for i in (0, 2, 4)) + " 1"


def widget(name, x, y, w, h, body, style="card", accent=None, tooltip=None):
    # Verified templates: vanilla main_menu/gui/shared/backgrounds.gui.
    bg = {
        "card": 'background = { using = bg_round_corners_dark_blue_texture } background = { using = bg_container_framed_texture }',
        "inset": 'background = { using = color_dark_blue_texture } using = bg_text_mask_container_dark_blue',
        "window": 'background = { using = bg_window_default_expandable_template } background = { using = bg_window_default_frame_template margin = { 0 0 } }',
        "none": "",
    }[style]
    if accent:
        bg += f' background = {{ using = bg_round_corners_frame_alt_texture modify_texture = {{ color = {{ {rgb(accent)} }} blend_mode = add }} }}'
    tip = f'tooltip = {quote(tooltip)} alwaystransparent = no' if tooltip else ''
    return f'widget = {{ name = {name} position = {{ {x} {y} }} size = {{ {w} {h} }} {bg} {tip} {body} }}'


def bar(name, x, y, w, value, maximum, label="", ticks=(), marker=None):
    body = (f'progressbar = {{ name = {name}_fill size = {{ {w} 14 }} '
            f'using = progress_bar_blue_alt value = {value:g} max = {maximum:g} }}')
    if marker is not None:
        body += f'widget = {{ position = {{ {min(w-2, round(w*marker)-1)} 0 }} size = {{ 2 14 }} background = {{ using = color_white_texture color = {{ {rgb("gold")} }} }} }}'
    body += text(0, -3, w, label, 10, align="center", h=18)
    for fraction, caption in ticks:
        body += text(max(0, min(w-34, round(w*fraction)-17)), 14, 34, caption, 10, "dim", "center", 18)
    return widget(name, x, y, w, 32, body, "none")


def button(name, y, label, disabled=False):
    return (f'button_regular_alt = {{ name = {name} position = {{ 10 {y} }} '
            f'size = {{ 500 32 }} enabled = {"no" if disabled else "yes"} '
            f'raw_text = {quote(label)} tooltip = "离线外观预览；尚未绑定游戏动作" }}')


def section(name, y, h, title, tag, body):
    header = widget(name + "_header", 0, 0, 520, 30,
                    text(10, 3, 210, title, 15) + text(205, 5, 303, tag, 11, "dim", "right"), "inset")
    return widget(name, 10, y, 520, h, header + body)


def status(demand, supply):
    ratio = supply / demand if demand else 1
    return "ok" if ratio >= 1 else "mid" if ratio >= .7 else "hi"


def load_model(state, fixture=FIXTURE):
    from eu5_gui_renderer.pdx import parse
    from eu5_gui_renderer.paths import GAME, MOD
    data = json.loads(Path(fixture).read_text(encoding="utf-8"))
    sample = data["states"][state]
    nodes = parse((MOD / PM).read_text(encoding="utf-8-sig"))
    recipes, maintenance = [], {}
    for node in nodes:
        values = {n.key: n.value for n in node.value}
        if node.key == "tv_wonder_labor_camp_maintenance":
            maintenance = {k: float(v) for k, v in values.items() if k != "category"}
        elif node.key.startswith("tv_wonder_material_dispatch_point_production"):
            recipes.append({"id": node.key, "output": float(values["output"]),
                            "produced": values["produced"], "inputs": {
                                k: float(v) for k, v in values.items()
                                if k not in ("category", "produced", "output")}})
    prices = {}
    for root in (GAME, MOD):
        for path in sorted((root / "in_game/common/goods").glob("*.txt")):
            for node in parse(path.read_text(encoding="utf-8-sig")):
                if isinstance(node.value, list):
                    for field in node.value:
                        if field.key == "default_market_price":
                            prices[node.key] = float(field.value)
    market = {key: dict(values) for key, values in data["market"].items()}
    if sample["balanced_market"]:
        for values in market.values():
            values["supply"] = max(values["demand"], values["supply"])
    level, employment = sample["level"], sample["employment"]
    cap = min(data["design_rules"]["max_level"], sample["organization"] // 5)
    base_progress = level * data["design_rules"]["progress_per_effective_level"]
    camp = base_progress * employment
    multiplier = .5 + sample["logistics"] / 100
    quantities = {good: amount * level for good, amount in maintenance.items()}
    demand = quantities["tv_wonder_materials"]
    supply = demand * sample["materials_supply"]
    market["tv_wonder_materials"] = {"demand": demand, "supply": supply}
    for recipe in recipes:
        # No fallback: every new ingredient needs an explicit market fixture.
        recipe["status"] = min((status(**market[g]) for g in recipe["inputs"]),
                               key={"hi": 0, "mid": 1, "ok": 2}.__getitem__)
    return {**sample, "state": state, "cap": cap, "market": market, "recipes": recipes,
            "maintenance": quantities, "base_prices": prices, "prices": data["prices"],
            "effective": level * employment, "base_progress": base_progress, "camp_progress": camp, "multiplier": multiplier,
            "progress": camp * multiplier * sample["materials_supply"], "gap": demand-supply,
            "maintenance_total": sum(q * data["prices"][g] for g, q in quantities.items())}


def organization(m, loc):
    body = widget("camp_icon", 10, 42, 46, 46,
                  'icon = { position = { 3 3 } size = { 40 40 } texture = "gfx/interface/icons/buildings/tv_wonder_labor_camp.dds" }', "inset", "gold")
    if m["state"] == "locked":
        body += text(68, 40, 420, "— / — 级劳工营", 24, "dim", h=34)
        body += bar("camp_scale", 68, 78, 430, 0, 20, "未勘测")
        body += widget("survey_notice", 10, 120, 500, 36,
                       text(10, 7, 480, "你必须先完成勘测，才能进行组织和物流。", 13, "mid"), accent="mid")
        body += button("build_camp", 168, "@construction! 建设工地 · 未勘测", True)
        return section("organization", 60, 212, "@organization! 组织", "读数 —", body)
    body += text(68, 39, 230, f'{m["level"]} / {m["cap"]} 级劳工营', 23, h=34)
    body += text(282, 46, 215, f'组织 ÷ 5 = {m["cap"]}（上限 20）', 11, "dim", "right")
    body += bar("camp_scale", 68, 78, 430, m["level"], 20, f'{m["level"]} / {m["cap"]}',
                [(i/20, str(i)) for i in (0, 5, 10, 15, 20)], m["cap"]/20)
    stats = [("劳工就业", f'{m["employment"]:.0%}', f'空缺 {1-m["employment"]:.0%}', "mid" if m["employment"] < 1 else "good"),
             ("有效等级", f'{m["effective"]:.2f}', f'{m["level"]} 级 × {m["employment"]:.0%}', None),
             ("月进度（营地）", f'+{m["camp_progress"]:,.0f}', "每有效级 1,000", "good")]
    for i, (label, value, note, color) in enumerate(stats):
        content = text(8, 2, 146, label, 11, "dim") + text(8, 23, 146, value, 20, color, h=26)
        content += text(8, 48, 146, note, 10, "dim")
        body += widget(f"stat_{i}", 10+i*169, 116, 162, 72, content, "inset")
    costs = text(8, 4, 100, "月维护", 12, "dim")
    costs += text(112, 1, 360, f'{m["maintenance_total"]:,.1f} 金 / 月', 21, "gold", h=30)
    for i, good in enumerate(("tools", "tv_wonder_materials")):
        price, base = m["prices"][good], m["base_prices"][good]
        delta = price/base-1
        color = "hi" if delta > .3 else "mid" if delta > .1 else "good" if delta < 0 else "dim"
        cell = text(6, 14, 38, f'@{good}!', 22, align="center", h=38)
        cell += text(48, 2, 192, f'{loc.get(good)} × {m["maintenance"][good]:g}/月', 11)
        cell += text(48, 22, 180, f'{price:.2f} 金', 21, color, h=28)
        cell += text(48, 49, 190, f'{"▼" if delta < 0 else "▲"} {abs(delta):.0%}    基准 {base:.2f}', 11, color)
        costs += widget(f"price_{good}", 5+i*247, 36, 243, 74, cell, "inset", color)
    body += widget("maintenance", 10, 196, 500, 116, costs, "inset")
    full = m["level"] >= m["cap"]
    body += button("build_camp", 320, "@construction! 建设工地" +
                   (" · 已达组织上限" if full else f'（{m["level"]} / {m["cap"]}）'), full)
    return section("organization", 60, 362, "@organization! 组织", f'读数 {m["organization"]} / 决定营地规模', body)


def connectors(m, output_root):
    """Bake geometry only; shared render_tree still draws every node and label."""
    from PIL import Image, ImageDraw
    scale = 3
    im = Image.new("RGBA", (500*scale, GRAPH_HEIGHT*scale))
    draw = ImageDraw.Draw(im)
    def line(points, color, width=2):
        draw.line([(round(x*scale), round(y*scale)) for x, y in points], fill="#"+COLORS[color], width=width*scale)
    top = len(m["recipes"])*PITCH+8
    for i, recipe in enumerate(m["recipes"]):
        y = 3+i*PITCH+CH/2
        xs = CEND-(len(recipe["inputs"])*CW+(len(recipe["inputs"])-1)*CG)
        line([(xs, y), (TRUNK, y)], recipe["status"])
    line([(TRUNK, 23), (TRUNK, top)], "ok" if m["gap"] == 0 else "mid", 3)
    line([(448, top+72), (448, top+92)], "ok" if m["gap"] == 0 else "mid", 4)
    line([(294, top+114), (336, top+114)], status(**m["market"]["tools"]), 2)
    if m["gap"]:
        for x in range(294, 336, 10):
            line([(x, top+22), (min(x+5, 336), top+22)], "dim")
    path = output_root / "gfx/interface/org_logistics" / f'{m["state"]}_connectors.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    return path.relative_to(output_root).as_posix()


def graph(m, loc, connector_texture):
    body = f'background = {{ texture = "{connector_texture}" }}'
    for j, recipe in enumerate(m["recipes"]):
        y = 3+j*PITCH
        xs = CEND-(len(recipe["inputs"])*CW+(len(recipe["inputs"])-1)*CG)
        for i, (good, amount) in enumerate(recipe["inputs"].items()):
            x = xs+i*(CW+CG)
            market = m["market"][good]
            color = status(**market)
            cell = text(2, 0, 54, f'@{good}!{loc.get(good)}', 9, h=19)
            cell += text(2, 19, 54, f'{market["demand"]:g}/{market["supply"]:g}', 11, color, h=19)
            body += widget(f"input_{j}_{good}", x, y, CW, CH, cell, "inset", color,
                           f'{loc.get(good)}：每工艺投入 {amount:g}；市场需求 {market["demand"]:g} / 供给 {market["supply"]:g}')
            if i+1 < len(recipe["inputs"]):
                body += text(x+CW, y+8, CG, "+", 10, align="center")
        label = text(4, 0, MW-8, loc.get(recipe["id"]), 12, align="center")
        word = {"ok": "畅通", "mid": "受限", "hi": "缺料"}[recipe["status"]]
        label += text(4, 20, MW-8, f'{word}  ·  产出 {recipe["output"]:g}', 10, recipe["status"], "center", 18)
        body += widget(f"method_{j}", MX, y, MW, CH, label, "inset", recipe["status"])
    top = len(m["recipes"])*PITCH+8
    market = m["market"]["tv_wonder_materials"]
    cell = text(8, 2, 148, "@tv_wonder_materials! 建材（本地市场）", 11)
    cell += text(8, 24, 148, f'{market["demand"]:g} / {market["supply"]:g}', 22, h=30)
    cell += text(8, 52, 148, f'缺 {m["gap"]:g}' if m["gap"] else "供需平衡", 10, "mid" if m["gap"] else "good", h=18)
    body += widget("materials_market", 336, top, 164, 72, cell, "inset", "mid" if m["gap"] else "ok")
    body += text(350, top+72, 145, f'{market["demand"]:g}/月', 10, "dim", "right", 18)
    cell = text(8, 0, 148, "@laborers! 劳工营", 12)
    cell += text(8, 23, 44, f'{m["level"]} 级', 19)
    cell += text(54, 20, 106, f'后勤 ×{m["multiplier"]:.0%}', 11)
    cell += text(54, 38, 106, f'建材 {m["materials_supply"]:.0%}', 11, "mid" if m["gap"] else "good")
    body += widget("graph_camp", 336, top+92, 164, 60, cell, "inset", "mid" if m["gap"] else "ok")
    if m["gap"]:
        cell = text(8, 0, 102, "@trade! 进口", 12) + text(8, 23, 102, f'待补 +{m["gap"]:g}/月', 11, "dim")
        body += widget("import_suggestion", 176, top, 118, 48, cell, "inset", "dim")
    tools_market = m["market"]["tools"]
    cell = text(8, 0, 102, "@tools! 工具", 12)
    cell += text(8, 23, 102, f'{tools_market["demand"]:g}/{tools_market["supply"]:g}', 13, status(**tools_market))
    body += widget("tools_market", 176, top+92, 118, 48, cell, "inset", status(**tools_market))
    body += text(294, top+88, 42, f'{m["maintenance"]["tools"]:g}/月', 9, "dim", "center")
    return widget("supply_graph", 10, 114, 500, GRAPH_HEIGHT, body, "none")


def logistics(m, loc, connector_texture):
    body = widget("logistics_icon", 10, 42, 46, 46,
                  text(3, 6, 40, "@tv_wonder_materials!", 25, align="center", h=38), "inset", "gold")
    body += text(68, 39, 240, f'{m["multiplier"]:.0%} 后勤乘数', 23, h=34)
    body += text(310, 46, 188, f'50% + 读数 {m["logistics"]}', 11, "dim", "right")
    body += bar("logistics_scale", 68, 78, 430, m["logistics"], 100, ticks=[(0, "50%"), (.5, "100%"), (1, "150%")], marker=.5)
    body += graph(m, loc, connector_texture)
    body += text(10, 664, 298, "数字 = 本地市场 需求 / 供给", 11, "dim")
    for i, (label, color) in enumerate((("充足", "ok"), ("紧张", "mid"), ("短缺", "hi"))):
        body += text(305+i*68, 664, 65, "━ " + label, 11, color)
    full = m["state"] == "full"
    body += button("build_workshop", 692, "@construction! 建设建材工坊" + (" · 已满配" if full else ""), full)
    return section("logistics", 430, 734, "@supply! 物流", f'读数 {m["logistics"]} / 决定速度与建材', body)


def summary(m):
    body = ""
    cells = [("营地", f'{m["camp_progress"]:,.0f}', f'有效 {m["effective"]:.2f} 级', None),
             ("后勤", f'{m["multiplier"]:.0%}', f'读数 {m["logistics"]}', None),
             ("建材供应", f'{m["materials_supply"]:.0%}', f'缺口 {1-m["materials_supply"]:.0%}', "mid" if m["gap"] else "good"),
             ("本月进度", f'{m["progress"]:,.0f}', "进度 / 月", "ok")]
    for i, (label, value, note, color) in enumerate(cells):
        cell = text(4, 2, 106, label, 11, "dim", "center") + text(4, 24, 106, value, 20, color, "center", 27)
        cell += text(4, 51, 106, note, 10, "dim", "center")
        body += widget(f"factor_{i}", 10+i*129, 40, 113, 76, cell, "inset", color if i == 2 else None)
        if i < 3:
            body += text(123+i*129, 65, 16, "=" if i == 2 else "×", 13, "dim", "center")
    if m["gap"]:
        recovered = m["camp_progress"] * m["multiplier"] - m["progress"]
        note = f'建材不足：吞吐降低 {1-m["materials_supply"]:.0%}。补齐供应后每月约 +{recovered:,.0f} 进度。'
    else:
        note = f'供应充足。{"组织与后勤已满配，" if m["state"] == "full" else ""}本月进度达到 {m["progress"]:,.0f}。'
    body += widget("diagnosis", 10, 124, 500, 38, text(9, 8, 482, note, 12, "mid" if m["gap"] else "good"), "inset", "mid" if m["gap"] else "good")
    return section("settlement", 1172, 172, "@construction! 每月进度结算", "营地 × 后勤 × 建材供应", body)


def render(state, resources, *, fixture=FIXTURE, output_root=OUT, scale=1):
    from eu5_gui_renderer.pdx import parse
    from eu5_gui_renderer.gui import Expander, build_target
    from eu5_gui_renderer.preview import render_tree, has_diagnostics
    m = load_model(state, fixture)
    height = 306 if state == "locked" else 1378
    title = text(52, 5, 410, "@organization! 组织和物流", 18, align="center", h=32)
    title += widget("help", 482, 8, 28, 26, text(0, 0, 28, "?", 16, "gold", "center"), "inset", "gold")
    body = widget("panel_title", 10, 10, 520, 42, title, "inset", "gold") + organization(m, resources.loc)
    if state != "locked":
        body += logistics(m, resources.loc, connectors(m, output_root)) + summary(m)
    body += text(10, height-26, 520, "离线设计预览 · 市场、就业为样例 · 配方与素材来自游戏 / Mod", 10, "dim", "center")
    source = widget("org_logistics_preview", 0, 0, 540, height, body, "window")
    gui = output_root / f"{state}.gui"
    gui.write_text(source, encoding="utf-8-sig")
    resources.db.roots[str(gui)] = parse(source, str(gui), dict(resources.db.consts))
    expander = Expander(resources.db)
    root = build_target(resources.db, expander, "org_logistics_preview", gui)
    details = {child.props["name"]: child for child in root.children
               if child.props.get("name") in ("organization", "logistics", "settlement")}
    report = render_tree(root, expander, resources, [], width=540, height=height, scale=scale,
                         output=output_root / f"{state}.png", detail_elements=details,
                         metadata={"sample_data": True, "state": state, "model": m,
                                   "design_reference": "docs/design/Org_Logistics_Panel_Design.html"})
    return report, has_diagnostics(report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", choices=("active", "locked", "full", "all"), default="all")
    parser.add_argument("--scale", type=float, default=1)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--output-root", type=Path, default=OUT)
    parser.add_argument("--game-root", type=Path)
    parser.add_argument("--renderer-root", type=Path)
    args = parser.parse_args()
    out = args.output_root.resolve()
    out.mkdir(parents=True, exist_ok=True)
    os.environ["RENDER_EXTRA_ROOTS"] = os.pathsep.join(filter(None, (str(out), os.environ.get("RENDER_EXTRA_ROOTS"))))
    engineering.configure(output_root=out, game_root=args.game_root, renderer_root=args.renderer_root)
    from eu5_gui_renderer.preview import load_resources
    resources = load_resources()
    reports, failed = [], False
    for state in ("active", "locked", "full") if args.state == "all" else (args.state,):
        report, diagnostic = render(state, resources, fixture=args.fixture, output_root=out, scale=args.scale)
        reports.append(report)
        failed |= diagnostic
        print(state, report["output"], "diagnostics", diagnostic)
    (out / "index.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    return int(args.strict and failed)


if __name__ == "__main__":
    raise SystemExit(main())
