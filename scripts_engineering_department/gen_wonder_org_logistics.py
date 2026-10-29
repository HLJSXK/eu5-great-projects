"""Own the organization/logistics GUI, display cache, localizations and connectors.

The cache is refreshed by the existing construction display lifecycle. It reads
the selected site's market and preserves the existing settlement algorithm.
Reference: triggers.log building_employed_amount/building_employment_size_amount,
goods_*_in_market; event_targets.log market_price; vanilla gold-fleet events.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from dds_image_lib import RgbaImage, write_dds

PM = ROOT / "src/in_game/common/production_methods/tv_engineering_department_production_methods.txt"
PREFIX = "tv_ol_"
PLAYER = "InternationalOrganizationsView.GetPlayer.MakeScope"
LOC = {}
# Vanilla market/status palette; state is a small marker, not a tinted card rim.
STATUS_TEXTURES = {0: "color_red_texture", 1: "color_yellow_texture",
                   2: "color_light_green_texture", 3: "color_light_green_texture"}
H = 1300


def inputs():
    blocks = dict(re.findall(r"(?ms)^(\w+)\s*=\s*\{(.*?)^}", PM.read_text(encoding="utf-8-sig")))
    def fields(body):
        return dict(re.findall(r"(?m)^\s*(\w+)\s*=\s*([^\s#]+)\s*$", body))
    maintenance = {k: float(v) for k, v in fields(blocks["tv_wonder_labor_camp_maintenance"]).items() if k != "category"}
    recipes = []
    for key, body in blocks.items():
        if key.startswith("tv_wonder_material_dispatch_point_production"):
            f = fields(body)
            recipes.append((key, {k: float(v) for k, v in f.items() if k not in ("category", "produced", "output")}, float(f["output"])))
            assert f["produced"] == "tv_wonder_materials"
    assert len(recipes) == 8, "Revisit the production list height for changed recipes"
    prices = {}
    for folder in (ROOT / ".eu5-base/reference_game_files/game/in_game/common/goods", ROOT / "src/in_game/common/goods"):
        for path in sorted(folder.glob("*.txt")):
            for key, body in re.findall(r"(?ms)^(\w+)\s*=\s*\{(.*?)^}", path.read_text(encoding="utf-8-sig")):
                match = re.search(r"default_market_price\s*=\s*([\d.]+)", body)
                if match:
                    prices[key] = float(match[1])
    return maintenance, recipes, prices


def variables():
    maintenance, recipes, _ = inputs()
    goods = sorted(maintenance)
    names = ["levels", "employed", "workers", "employment", "camp_progress", "input_efficiency", "maintenance", "recoverable", "materials_gap"]
    names += [f"{g}_{suffix}" for g in goods for suffix in ("demand", "supply", "price", "ratio", "status", "premium")]
    names += [f"{g}_quantity" for g in maintenance]
    return names


def effects():
    maintenance, recipes, prices = inputs()
    goods = sorted(maintenance)
    def assign(name, value):
        return f'set_variable = {{ name = {PREFIX}{name} value = {{ {value} }} }}'
    lines = ["tv_wonder_clear_org_logistics_display_effect = {"]
    lines += [f"remove_variable = {PREFIX}{name}" for name in ["ready", "workshop_type", *variables()]]
    lines += ["}", "", "tv_wonder_update_org_logistics_display_effect = {",
              "tv_wonder_clear_org_logistics_display_effect = yes", "if = {", "limit = {",
              "tv_wonder_construction_site_selected_trigger = yes",
              "var:tv_wonder_site ?= { exists = market }", "}",
              "save_scope_as = tv_ol_owner"]
    lines += [assign(name, "value = 0") for name in variables()]
    lines += [assign("levels", 'value = "var:tv_wonder_site.location_building_level(building_type:tv_wonder_labor_camp)"'),
              "var:tv_wonder_site ?= { every_buildings_in_location = {",
              "limit = { building_type = building_type:tv_wonder_labor_camp }",
              "scope:tv_ol_owner = {",
              "change_variable = { name = tv_ol_employed add = { value = prev.building_employed_amount } }",
              "change_variable = { name = tv_ol_workers add = { value = prev.building_employment_size_amount } }", "} } }",
              "if = { limit = { var:tv_ol_workers ?= { this > 0 } }",
              assign("employment", "value = var:tv_ol_employed divide = var:tv_ol_workers min = 0 max = 1"), "}",
              assign("camp_progress", "value = var:tv_wonder_worksite_scale_monthly_construction_progress subtract = var:tv_wonder_labor_shortage_construction_progress min = 0"),
              # Derive from the actual floored settlement, including tools and materials.
              "if = { limit = { var:tv_ol_camp_progress ?= { this > 0 } }",
              assign("input_efficiency", "value = var:tv_ol_camp_progress subtract = var:tv_wonder_material_input_shortage_construction_progress divide = var:tv_ol_camp_progress min = 0 max = 1"), "}",
              assign("recoverable", "value = var:tv_wonder_material_input_shortage_construction_progress multiply = var:tv_wonder_logistics_progress_percent divide = 100")]
    for good in goods:
        for suffix, link in (("demand", "goods_demand_in_market"), ("supply", "goods_supply_in_market"), ("price", "market_price")):
            lines.append(assign(f"{good}_{suffix}", f'value = "var:tv_wonder_site.market.{link}(goods:{good})"'))
        lines += [assign(f"{good}_ratio", "value = 1"),
                  f"if = {{ limit = {{ var:{PREFIX}{good}_demand ?= {{ this > 0 }} }}",
                  assign(f"{good}_ratio", f"value = var:{PREFIX}{good}_supply divide = var:{PREFIX}{good}_demand min = 0 max = 1"), "}",
                  f"if = {{ limit = {{ var:{PREFIX}{good}_ratio ?= {{ this >= 1 }} }}", assign(f"{good}_status", "value = 2"),
                  f"}} else_if = {{ limit = {{ var:{PREFIX}{good}_ratio ?= {{ this >= 0.7 }} }}", assign(f"{good}_status", "value = 1"), "}",
                  assign(f"{good}_premium", f"value = var:{PREFIX}{good}_price divide = {prices[good]:g} subtract = 1")]
    for good, quantity in maintenance.items():
        # Name this nominal maintenance: the engine may scale actual building expenses.
        lines += [assign(f"{good}_quantity", f"value = var:tv_ol_levels multiply = {quantity:g}"),
                  f"change_variable = {{ name = tv_ol_maintenance add = {{ value = var:{PREFIX}{good}_quantity multiply = var:{PREFIX}{good}_price }} }}"]
    lines += [assign("materials_gap", "value = var:tv_ol_tv_wonder_materials_demand subtract = var:tv_ol_tv_wonder_materials_supply min = 0")]
    # Actions can preview this lifecycle before writes commit. Calculate in locals,
    # then publish once; never read a newly assigned persistent display variable.
    source = "\n".join(lines)
    source = re.sub(r"set_variable = \{ name = tv_ol_", "set_local_variable = { name = tv_ol_", source)
    source = re.sub(r"change_variable = \{ name = tv_ol_", "change_local_variable = { name = tv_ol_", source)
    source = source.replace("var:tv_ol_", "local_var:tv_ol_")
    source = re.sub(r"(local_var:tv_ol_\w+) \?= \{ this ([><=]+) ([\d.]+) \}", r"\1 \2 \3", source)
    for name in variables():
        source += f'\nset_variable = {{ name = {PREFIX}{name} value = {{ value = local_var:{PREFIX}{name} }} }}'
    source += '\nset_variable = { name = tv_ol_workshop_type value = building_type:tv_wonder_material_dispatch_point }'
    source += '\nset_variable = { name = tv_ol_ready value = 1 }\n}\n'
    source += "\n".join(f"remove_local_variable = {PREFIX}{name}" for name in variables()) + "\n}"
    return pretty(source)


def v(name):
    return f"{PLAYER}.GetVariable('{PREFIX}{name}').GetValue"


def original(name):
    return f"{PLAYER}.GetVariable('tv_wonder_{name}').GetValue"


def value(name, fmt="0"):
    return f"[{v(name)}|{fmt}]"


def ov(name, fmt="0"):
    return f"[{original(name)}|{fmt}]"


def loc(key, zh, en):
    key = "TV_OL_" + key
    if key in LOC:
        assert LOC[key] == (zh, en)
    LOC[key] = zh, en
    return key


def txt(x, y, w, key, size=13, align="left", h=22):
    return f'text_single = {{ position = {{ {x} {y} }} size = {{ {w} {h} }} autoresize = no fontsize = {size} fontsize_min = 8 align = {align}|nobaseline text = "{key}" }}'


def raw(x, y, w, val, size=13, align="left", h=22):
    return txt(x, y, w, val, size, align, h).replace('text = "', 'raw_text = "')


def eq(name, n):
    return f"EqualTo_CFixedPoint({v(name)}, '(CFixedPoint){n}')"


def frame(style="inset"):
    # Match vanilla card_common and market goods rows (shared/cards.gui,
    # panels/market/market_goods.gui), without overriding their texture palette.
    return {
        "inset": 'using = bg_text_mask_container_dark_blue',
        "node": 'using = bg_scroll_card',
        "section": 'using = bg_paper_card using = bg_cabinet_card_frame',
        "header": 'using = bg_card_header_01_diplomacy using = bg_cabinet_inner_frame',
    }[style]


def status_marker(w, h, color, condition=None, vertical=False):
    visible = f'visible = "[{condition}]"' if condition else ""
    x, y, width, height = (2, 5, 3, h-10) if vertical else (4, h-2, w-8, 2)
    return f'widget = {{ {visible} position = {{ {x} {y} }} size = {{ {width} {height} }} alwaystransparent = yes background = {{ using = {STATUS_TEXTURES[color]} }} }}'


def box(name, x, y, w, h, body, *, status=None, accent=None, extra="", style="inset"):
    markers = ""
    if status:
        style = "node"
        markers = "".join(status_marker(w, h, n, eq(status, n)) for n in (0, 1, 2))
    elif accent in STATUS_TEXTURES:
        markers = status_marker(w, h, accent, vertical=True)
    return f'widget = {{ name = {name} position = {{ {x} {y} }} size = {{ {w} {h} }} {extra} {frame(style)} {body} {markers} }}'


def button(name, y, key, filter_key, enabled="yes"):
    return f'''button_regular = {{ name = {name} position = {{ 10 {y} }} size = {{ 480 32 }}
enabled = {enabled} text = "{key}"
action_tooltip = {{ click_type = left click_mode = single title = "{key}" on_action = "[OpenLateralViewWithFilter('production', '{filter_key}')]" }}
tooltipwidget = {{ BasicFunctionalTooltip = {{}} }} }}'''


def bar(name, x, y, w, current, maximum, caption):
    return f'''widget = {{ name = {name} position = {{ {x} {y} }} size = {{ {w} 18 }}
progressbar_framed = {{ size = {{ {w} 16 }} using = progressbar_bar_small min = 0 max = "[{maximum}]" value = "[{current}]" }}
{raw(0, -2, w, caption, 10, "center")} }}'''


def header(name, y, key, tag):
    return box(name, 0, y, 500, 30, txt(10, 3, 190, key, 15) + txt(200, 4, 290, tag, 13, "right"), style="header")


def org_logistics_help():
    """Original five organization + three logistics rows, as in the other steps."""
    sections = []
    for section, count in (("ORGANIZATION", 5), ("LOGISTICS", 3)):
        rows = []
        for index in range(1, count + 1):
            rows.append(f'''TooltipManualTableField = {{
blockoverride "row_size" {{ maximumsize = {{ -1 50 }} minimumsize = {{ -1 50 }} }}
text_multi = {{
    layoutpolicy_horizontal = expanding
    max_width = 380
    minimumsize = {{ 380 -1 }}
    autoresize = yes
    text = "TV_ENGINEERING_ORG_LOG_HELP_{section}_TEXT_{index}"
    align = nobaseline|left
}}
}}''')
        sections.append(f'''text_single = {{
layoutpolicy_horizontal = expanding
fontsize = 16
text = "TV_ENGINEERING_{section}_SECTION_TITLE"
align = center|nobaseline
}}
vbox = {{
set_parent_size_to_minimum = yes
layoutpolicy_horizontal = expanding
layoutpolicy_vertical = shrinking
margin = {{ 4 4 }}
background = {{ using = bg_container_framed_texture }}
{' '.join(rows)}
}}''')
    return f'''vbox = {{
set_parent_size_to_minimum = yes
layoutpolicy_horizontal = expanding
layoutpolicy_vertical = shrinking
spacing = 6
{' '.join(sections)}
}}'''


def step_header():
    # Reuse the same component as conception, debate, survey, construction and
    # ceremony. Only omit its body; all header visuals/geometry remain inherited.
    return f'''tv_engineering_department_card_common = {{
name = ol_title
size = {{ 500 50 }}
minimumsize = {{ 500 50 }}
maximumsize = {{ 500 50 }}
layoutpolicy_vertical = fixed
blockoverride "common_header_icon_texture" {{ texture = "gfx/interface/icons/location_icons/new/prosperity.dds" }}
blockoverride "common_header_text" {{ text = "TV_ENGINEERING_ORG_LOG_CARD_TITLE" }}
blockoverride "card_common_bottom_margin" {{ margin = {{ 0 0 }} }}
blockoverride "common_bottom_content" {{}}
blockoverride "header_help_tooltip" {{
    name = org_logistics_help
    tooltipwidget = {{
        ConceptTooltipType = {{
            blockoverride "title_icon" {{ icon = {{ using = tooltip_title_icon_size texture = "gfx/interface/icons/flat_icons/tabicons/europedia_flat_icon.dds" }} }}
            blockoverride "title_text" {{ text = "TV_ENGINEERING_ORG_LOG_CARD_TITLE" }}
            blockoverride "tooltip_content" {{
                {org_logistics_help()}
            }}
        }}
    }}
}}
}}'''


def production_methods():
    # Native building_view.gui list and production_method_simple composition.
    # Scope.GetBuildingType is a documented promote (data_types_script.txt).
    # This is a type-wide recipe overview: no arbitrary workshop is selected.
    return f'''widget = {{
name = production_methods
size = {{ 480 378 }}
datacontext = "[{PLAYER}.GetVariable('tv_ol_workshop_type').GetBuildingType]"
vbox = {{
    layoutpolicy_horizontal = expanding
    datamodel = "[BuildingType.GetPossibleProductionMethods]"
    item = {{
        vbox = {{
            layoutpolicy_horizontal = expanding
            spacing = 4
            widget = {{
                size = {{ 480 32 }}
                using = bg_paper_card
                using = bg_cabinet_card_frame
                text_single = {{
                    size = {{ 100% 100% }} autoresize = no align = center
                    text = "[BuildingType.GetProductionMethodsLabel]"
                }}
            }}
            vbox = {{
                layoutpolicy_horizontal = expanding
                spacing = 2
                datamodel = "[PossibleProductionMethods.GetMethods]"
                item = {{
                    widget = {{
                        name = method_row
                        size = {{ 480 40 }}
                        card_list_button = {{
                            name = production_method_recipe
                            size = {{ 100% 100% }}
                            tooltipwidget = {{ using = ProductionMethod_tooltip }}
                            hbox = {{
                                layoutpolicy_horizontal = expanding
                                using = production_method_simple
                                blockoverride "production_method_simple_bg" {{}}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
}}'''


def gui():
    maintenance, recipes, prices = inputs()
    body = step_header()
    # Fixed background leaves keep the authored layout and scroll extent intact.
    for name, y, h in (("organization", 50, 344), ("logistics", 404, 656), ("settlement", 1068, 232)):
        body += box(f"{name}_paper", 0, y, 500, h, "", style="section", extra="alwaystransparent = yes")
    body += header("ol_org_header", 50, "TV_ENGINEERING_ORGANIZATION_SECTION_TITLE", loc("ORG_READ", f'组织 {ov("organization_competence")}', f'Organization {ov("organization_competence")}'))
    body += box("camp_icon", 10, 90, 46, 46, 'icon = { position = { 3 3 } size = { 40 40 } texture = "gfx/interface/icons/buildings/tv_wonder_labor_camp.dds" }')
    body += txt(68, 88, 410, loc("CAMP_LEVEL", f'{value("levels")} / {ov("organization_site_level_cap")} 级劳工营', f'Labor camp  {value("levels")} / {ov("organization_site_level_cap")}'), 15, h=32)
    body += bar("camp_bar", 68, 125, 412, v("levels"), original("organization_site_level_cap_display"), f'{value("levels")} / {ov("organization_site_level_cap")}')
    stats = [("EMPLOYMENT", "劳工就业", "Employment", value("employment", "0%")), ("EFFECTIVE", "有效等级", "Effective levels", ov("effective_worksite_levels", "2")), ("CAMP_PROGRESS", "月进度（营地）", "Camp progress", value("camp_progress"))]
    for i, (key, zh, en, val) in enumerate(stats):
        tip = loc("STAT_HELP", f'劳工就业按实际雇用人数计算。施工有效等级为 {ov("effective_worksite_levels", "2")}，营地基础进度为 {value("camp_progress")}。', f'Employment uses actual workers. Construction effective levels are {ov("effective_worksite_levels", "2")}; camp progress is {value("camp_progress")}.')
        body += box(f"stat_{i}", 10+i*163, 158, 154, 68, txt(8, 2, 138, loc(key, zh, en), 13) + raw(8, 28, 138, val, 15, h=30), extra=f'alwaystransparent = no tooltip = "{tip}"')
    body += txt(10, 234, 480, loc("MAINTENANCE", f'名义月维护  #Y {value("maintenance", "1")}#! @gold!', f'Nominal maintenance  #Y {value("maintenance", "1")}#! @gold!'), 15, h=28)
    for i, (good, quantity) in enumerate(maintenance.items()):
        cell = raw(6, 14, 34, f'@{good}!', 22, "center", 38)
        cell += txt(44, 0, 185, loc(f"{good}_QUANTITY", f'${good}$ × {value(good+"_quantity", "1")}/月', f'${good}$ × {value(good+"_quantity", "1")}/mo'), 11)
        cell += raw(44, 23, 185, f'{value(good+"_price", "2")} @gold!', 15, h=28)
        cell += txt(44, 50, 185, loc(f"{good}_BASE", f'{value(good+"_premium", "=0%")}  基准 {prices[good]:.2f}', f'{value(good+"_premium", "=0%")}  Base {prices[good]:.2f}'), 10)
        premium = v(good+"_premium")
        # Price and supply states have different thresholds.
        accent = ''.join(status_marker(236, 78, color, condition, vertical=True) for condition, color in [
            (f"GreaterThan_CFixedPoint({premium}, '(CFixedPoint)0.3')", 0),
            (f"And(GreaterThan_CFixedPoint({premium}, '(CFixedPoint)0.1'), LessThanOrEqualTo_CFixedPoint({premium}, '(CFixedPoint)0.3'))", 1),
            (f"LessThan_CFixedPoint({premium}, '(CFixedPoint)0')", 3)])
        tip = loc(f"{good}_PRICE_HELP", f'${good}$\n市场需求 {value(good+"_demand", "2")} / 供给 {value(good+"_supply", "2")}\n市场价格 {value(good+"_price", "2")}，相对基准 {value(good+"_premium", "=0%")}。\n名义月耗量按营地等级计算；实际建筑支出见生产界面。', f'${good}$\nMarket demand {value(good+"_demand", "2")} / supply {value(good+"_supply", "2")}\nMarket price {value(good+"_price", "2")}; {value(good+"_premium", "=0%")} versus base.\nNominal inputs use camp levels. See Production for actual building expenses.')
        body += box(f"price_{good}", 10+i*244, 267, 236, 78, cell + accent, extra=f'alwaystransparent = no tooltip = "{tip}"')
    can_build = f'"[And(LessThan_CFixedPoint({v("levels")}, {original("organization_site_level_cap")}), Not({PLAYER}.GetVariable(\'tv_wonder_construction_complete\').IsSet))]"'
    body += button("build_camp", 354, "TV_ENGINEERING_BUILD_WORKSITE_BUTTON", "uses_tv_wonder_materials", can_build)
    body += header("ol_log_header", 404, "TV_ENGINEERING_LOGISTICS_SECTION_TITLE", loc("LOG_READ", f'后勤 {ov("logistics_competence")}', f'Logistics {ov("logistics_competence")}'))
    graph = 'background = { texture = "gfx/interface/tv_org_logistics_connectors.dds" }'
    graph += production_methods()
    top = 392
    cell = txt(8, 0, 140, loc("MATERIALS_MARKET", "@tv_wonder_materials! 建材市场", "@tv_wonder_materials! Materials market"), 11)
    cell += raw(8, 22, 140, f'{value("tv_wonder_materials_demand", "1")}/{value("tv_wonder_materials_supply", "1")}', 19, h=30)
    cell += txt(8, 51, 140, loc("GAP", f'缺口 {value("materials_gap", "1")}', f'Shortfall {value("materials_gap", "1")}'), 10, h=18)
    graph += box("materials_market", 324, top, 156, 72, cell, status="tv_wonder_materials_status")
    positive_gap = f"GreaterThan_CFixedPoint({v('materials_gap')}, '(CFixedPoint)0')"
    graph = f'background = {{ visible = "[{positive_gap}]" texture = "gfx/interface/tv_org_logistics_import.dds" }}' + graph
    graph += box("import_hint", 164, top, 116, 48, txt(8, 0, 100, loc("IMPORT", "@trade! 进口补缺", "@trade! Import shortfall"), 11) + raw(8, 23, 100, value("materials_gap", "1"), 14), extra=f'visible = "[{positive_gap}]"')
    graph += box("camp_flow", 324, top+92, 156, 60, txt(8, 0, 140, "tv_wonder_labor_camp", 12) + raw(8, 25, 140, f'{value("levels")}    ×{ov("logistics_progress_percent")}% ', 18))
    graph += box("tools_market", 164, top+92, 116, 48, txt(8, 0, 100, loc("TOOLS", "@tools! 工具", "@tools! Tools"), 11) + raw(8, 23, 100, f'{value("tools_demand")}/{value("tools_supply")}', 13), status="tools_status")
    body += f'widget = {{ name = ol_supply_graph position = {{ 10 444 }} size = {{ 480 544 }} {graph} }}'
    body += txt(10, 992, 480, loc("LEGEND", "需求 / 供给      绿 充足    黄 紧张    红 短缺", "Demand / supply    Green sufficient   Amber tight   Red shortage"), 11, "center")
    body += button("build_workshop", 1020, "TV_ENGINEERING_BUILD_MATERIAL_WORKSHOP_BUTTON", "tv_wonder_materials")
    body += header("ol_summary_header", 1068, loc("SETTLEMENT", "每月进度结算", "Monthly progress"), loc("CHAIN", "营地 × 后勤 × 物资效率", "Camp × logistics × input efficiency"))
    factors = [("CAMP_PROGRESS", value("camp_progress")), ("LOG_READ", ov("logistics_progress_percent")+"%"), ("INPUT", value("input_efficiency", "0%")), ("RESULT", ov("monthly_construction_progress"))]
    loc("INPUT", "物资效率", "Input efficiency")
    loc("RESULT", "本月进度", "Monthly progress")
    for i, (label, val) in enumerate(factors):
        if label == "LOG_READ":
            label = "LOG_FACTOR"
            loc(label, "后勤", "Logistics")
        tip = loc("SETTLEMENT_HELP", f'营地进度 {value("camp_progress")} × 物资效率 {value("input_efficiency", "2%")} × 后勤 {ov("logistics_progress_percent")}% = {ov("monthly_construction_progress", "2")}。\n物资效率包括工具与建材，并保留原有结算取整。', f'Camp progress {value("camp_progress")} × input efficiency {value("input_efficiency", "2%")} × logistics {ov("logistics_progress_percent")}% = {ov("monthly_construction_progress", "2")}.\nInput efficiency includes tools and materials, preserving settlement rounding.')
        body += box(f"factor_{i}", 10+i*124, 1110, 108, 74, txt(4, 4, 100, "TV_OL_"+label, 13, "center") + raw(4, 31, 100, val, 18, "center", 30), accent=1 if i==2 else None, extra=f'alwaystransparent = no tooltip = "{tip}"')
        if i < 3:
            body += raw(118+i*124, 1134, 16, "=" if i==2 else "×", 13, "center")
    notice = loc("SHORTAGE", f'物资不足。补齐工具与建材后每月可增加 {value("recoverable")} 进度。', f'Input shortage. Restoring tools and materials adds {value("recoverable")} progress/month.')
    good_notice = loc("SUPPLIED", "施工物资供应充足。", "Construction inputs are sufficiently supplied.")
    body += box("diagnosis", 10, 1194, 480, 42,
                f'text_multi = {{ size = {{ 462 38 }} position = {{ 9 2 }} max_width = 462 autoresize = no fontsize = 12 text = "[SelectLocalization(GreaterThan_CFixedPoint({v("recoverable")}, \'(CFixedPoint)0\'), \'{notice}\', \'{good_notice}\')]" }}', accent=1)
    body += txt(10, 1244, 480, loc("CAPACITY", f'有效工坊 {ov("effective_material_workshop_levels")} / 所需 {ov("material_workshop_need")} 级', f'Effective workshops {ov("effective_material_workshop_levels")} / required {ov("material_workshop_need")}'), 12, "center")
    body += bar("workshop_capacity", 10, 1273, 480, original("effective_material_workshop_levels"), original("material_workshop_need_display"), "")
    locked = box("locked_paper", 0, 0, 500, 198, "", style="section", extra="alwaystransparent = yes")
    locked += step_header()
    locked += txt(20, 62, 460, loc("LOCKED_LEVEL", "— / — 级劳工营", "— / — labor camp levels"), 15, h=34)
    locked += txt(20, 110, 460, "TV_ENGINEERING_ORG_LOG_LOCKED_TEXT", 13)
    locked += button("build_camp_locked", 152, "TV_ENGINEERING_BUILD_WORKSITE_BUTTON", "uses_tv_wonder_materials", "no")
    return pretty(f'types TVOrgLogistics {{ type tv_org_logistics_active = widget {{ size = {{ 500 {H} }} {body} }} type tv_org_logistics_locked = widget {{ size = {{ 500 198 }} {locked} }} }}')


def pretty(source):
    """Format generated PDX without touching braces/newlines inside strings."""
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|[{}]|[^\s{}"]+', source)
    lines, current, depth = [], [], 0
    for token in tokens:
        if token == "{":
            lines.append("\t"*depth + " ".join(current+[token])); current = []; depth += 1
        elif token == "}":
            if current: lines.append("\t"*depth + " ".join(current)); current = []
            depth -= 1; lines.append("\t"*depth + "}")
        else:
            # A scalar assignment is complete when the next property begins.
            if len(current) >= 3 and current[-2] == "=":
                lines.append("\t"*depth + " ".join(current)); current = []
            current.append(token)
    if current: lines.append("\t"*depth + " ".join(current))
    return "\n".join(lines)+"\n"


def connector_image(import_only=False):
    from PIL import Image, ImageDraw
    image = Image.new("RGBA", (960, 1088))
    draw = ImageDraw.Draw(image)
    def line(points, dashed=False):
        if dashed:
            x, y = points[0]; end = points[-1][0]
            for start in range(int(x), int(end), 10):
                line([(start,y),(min(start+5,end),y)])
        else:
            draw.line([(x*2,y*2) for x,y in points], fill="#b39a65", width=4)
    if import_only:
        line([(280,414),(324,414)], True)
        return image
    line([(440,464),(440,484)])
    line([(280,506),(324,506)])
    return image


def outputs():
    LOC.clear()
    result = {"src/in_game/gui/tv_wonder_org_logistics.gui": gui(),
              "src/in_game/common/scripted_effects/tv_wonder_org_logistics_display.txt": effects()}
    for folder in sorted((ROOT / "src/main_menu/localization").iterdir()):
        if not folder.is_dir(): continue
        language = folder.name
        index = 0 if language == "simp_chinese" else 1
        lines = [f"l_{language}:"]
        for key, pair in LOC.items():
            val = pair[index].replace('"', '\\"').replace("\n", "\\n")
            lines.append(f' {key}:0 "{val}"')
        result[f"src/main_menu/localization/{language}/tv_wonder_org_logistics_l_{language}.yml"] = "\n".join(lines)+"\n"
    header = '# @Generated by scripts_engineering_department/gen_wonder_org_logistics.py\n# Edit the generator and production-method inputs; do not hand-edit.\n'
    return {path: header + content for path, content in result.items()}


def main():
    for rel, content in outputs().items():
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8-sig", newline="\n")
        print("Wrote", rel)
    for name, import_only in (("connectors", False), ("import", True)):
        image = connector_image(import_only)
        write_dds(RgbaImage(image.width, image.height, image.tobytes()), ROOT / f"src/main_menu/gfx/interface/tv_org_logistics_{name}.dds", overwrite=True, mipmaps=True)


if __name__ == "__main__":
    main()
