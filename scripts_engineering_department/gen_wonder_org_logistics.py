"""Own the organization/logistics GUI, display cache and localizations.

The cache is refreshed by the existing construction display lifecycle. It reads
the selected site's market and preserves the existing settlement algorithm.
Reference: triggers.log building_employed_amount/building_employment_size_amount,
goods_*_in_market; event_targets.log market_price; vanilla gold-fleet events.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

PM = ROOT / "src/in_game/common/production_methods/tv_engineering_department_production_methods.txt"
PREFIX = "tv_ol_"
PLAYER = "InternationalOrganizationsView.GetPlayer.MakeScope"
WORKSITE = f"{PLAYER}.GetVariable('tv_ol_worksite')"
LOC = {}
# Vanilla market/status palette; state is a small marker, not a tinted card rim.
STATUS_TEXTURES = {0: "color_red_texture", 1: "color_yellow_texture",
                   2: "color_light_green_texture", 3: "color_light_green_texture"}
ORGANIZATION_HEIGHT = 316
LOGISTICS_Y = ORGANIZATION_HEIGHT + 10
FLOW_CARD_HEIGHT = 64
FLOW_HEIGHT = FLOW_CARD_HEIGHT + 44
LOGISTICS_HEIGHT = 432 + FLOW_HEIGHT + 8
SETTLEMENT_Y = LOGISTICS_Y + LOGISTICS_HEIGHT + 8
H = SETTLEMENT_Y + 232


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
    names = ["levels", "employed", "workers", "employment", "camp_progress", "input_efficiency", "recoverable", "materials_gap"]
    names += [f"{g}_{suffix}" for g in goods for suffix in ("demand", "supply", "price", "ratio", "status", "premium")]
    return names


def effects():
    maintenance, recipes, prices = inputs()
    goods = sorted(maintenance)
    def assign(name, value):
        return f'set_variable = {{ name = {PREFIX}{name} value = {{ {value} }} }}'
    lines = ["tv_wonder_clear_org_logistics_display_effect = {"]
    lines += [f"remove_variable = {PREFIX}{name}" for name in ["ready", "workshop_type", "worksite", *variables()]]
    lines += ["tv_wonder_clear_worksite_maintenance_display_effect = yes"]
    lines += ["}", "", "tv_wonder_update_org_logistics_display_effect = {",
              "tv_wonder_clear_org_logistics_display_effect = yes", "if = {", "limit = {",
              "tv_wonder_construction_site_selected_trigger = yes",
              "var:tv_wonder_site ?= { exists = market }", "}",
              "save_scope_as = tv_ol_owner"]
    lines += [assign(name, "value = 0") for name in variables()]
    lines += [assign("levels", 'value = "var:tv_wonder_site.location_building_level(building_type:tv_wonder_labor_camp)"'),
              "var:tv_wonder_site ?= { every_buildings_in_location = {",
              "limit = { building_type = building_type:tv_wonder_labor_camp }",
              "set_local_variable = { name = tv_ol_worksite value = this }",
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
    lines += [assign("materials_gap", "value = var:tv_ol_tv_wonder_materials_demand subtract = var:tv_ol_tv_wonder_materials_supply min = 0")]
    # Actions can preview this lifecycle before writes commit. Calculate in locals,
    # then publish once; never read a newly assigned persistent display variable.
    source = "\n".join(lines)
    source = re.sub(r"set_variable = \{ name = tv_ol_", "set_local_variable = { name = tv_ol_", source)
    source = re.sub(r"change_variable = \{ name = tv_ol_", "change_local_variable = { name = tv_ol_", source)
    source = source.replace("var:tv_ol_", "local_var:tv_ol_")
    source = re.sub(r"(local_var:tv_ol_\w+) \?= \{ this ([><=]+) ([\d.]+) \}", r"\1 \2 \3", source)
    source += '\ntv_wonder_update_worksite_maintenance_display_effect = yes'
    for name in variables():
        source += f'\nset_variable = {{ name = {PREFIX}{name} value = {{ value = local_var:{PREFIX}{name} }} }}'
    # Keep a typed building reference so the GUI uses the engine's upkeep and
    # breakdown, including the active mod's country modifiers and expense setting.
    source += '\nif = { limit = { has_local_variable = tv_ol_worksite } set_variable = { name = tv_ol_worksite value = local_var:tv_ol_worksite } }'
    source += '\nset_variable = { name = tv_ol_workshop_type value = building_type:tv_wonder_material_dispatch_point }'
    source += '\nset_variable = { name = tv_ol_ready value = 1 }\n}\n'
    source += "\n".join(f"remove_local_variable = {PREFIX}{name}" for name in [*variables(), "worksite"]) + "\n}"
    # Compatibility mods replace only these display hooks, never the project
    # settlement or the country's real maintenance ledger.
    source += '\ntv_wonder_clear_worksite_maintenance_display_effect = {}\ntv_wonder_update_worksite_maintenance_display_effect = {}\n'
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


def txt(x, y, w, key, size=13, align="left", h=22, *, extra=""):
    return f'text_single = {{ {extra} position = {{ {x} {y} }} size = {{ {w} {h} }} autoresize = no fontsize = {size} fontsize_min = 8 align = {align}|nobaseline text = "{key}" }}'


def raw(x, y, w, val, size=13, align="left", h=22, *, extra=""):
    return txt(x, y, w, val, size, align, h, extra=extra).replace('text = "', 'raw_text = "')


def eq(name, n):
    return f"EqualTo_CFixedPoint({v(name)}, '(CFixedPoint){n}')"


def frame(style="inset"):
    # Match vanilla card_common and market goods rows (shared/cards.gui,
    # panels/market/market_goods.gui), without overriding their texture palette.
    return {
        "flow_card": 'using = bg_market_card using = bg_market_card_frame',
        "cost_card": 'using = bg_market_card using = bg_loans_card_frame',
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


def button(name, y, key, filter_key, enabled="yes", *, market=None, x=10):
    action = (f"ShowProductionViewWithMarketAndFilter({market}, '{filter_key}', '(bool)yes')"
              if market is not None else f"OpenLateralViewWithFilter('production', '{filter_key}')")
    return f'''button_regular = {{ name = {name} position = {{ {x} {y} }} size = {{ 480 32 }}
enabled = {enabled} text = "{key}"
action_tooltip = {{ click_type = left click_mode = single title = "{key}" on_action = "[{action}]" }}
tooltipwidget = {{ BasicFunctionalTooltip = {{}} }} }}'''


def bar(name, x, y, w, current, maximum, caption, *, height=16, fontsize=10):
    return f'''widget = {{ name = {name} position = {{ {x} {y} }} size = {{ {w} {height+2} }}
progressbar_framed = {{ size = {{ {w} {height} }} using = progressbar_bar_small min = 0 max = "[{maximum}]" value = "[{current}]" }}
{raw(0, -2, w, caption, fontsize, "center", height+4)} }}'''


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


def step_card(bottom_content=""):
    # Keep the full shared card for locked stages, including its body styling.
    # Active organization uses only the header above its custom summary.
    sizing = "maximumsize = { 500 -1 }" if bottom_content else '''size = { 500 50 }
minimumsize = { 500 50 }
maximumsize = { 500 50 }
layoutpolicy_vertical = fixed
blockoverride "card_common_bottom_margin" { margin = { 0 0 } }'''
    return f'''tv_engineering_department_card_common = {{
name = ol_title
{sizing}
blockoverride "common_header_icon_texture" {{ texture = "gfx/interface/icons/location_icons/new/prosperity.dds" }}
blockoverride "common_header_text" {{ text = "TV_ENGINEERING_ORG_LOG_CARD_TITLE" }}
blockoverride "common_bottom_content" {{ {bottom_content} }}
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


def organization():
    """Compact worksite summary; values come from the real site's display cache."""
    maintenance, _, _ = inputs()
    body = step_card()
    body += box("organization_paper", 0, 50, 500, ORGANIZATION_HEIGHT-50, "", style="section", extra="alwaystransparent = yes")
    body += 'icon = { name = camp_icon position = { 14 66 } size = { 40 40 } texture = "gfx/interface/icons/buildings/tv_wonder_labor_camp.dds" }'
    body += raw(66, 59, 130, "[ShowBuildingTypeName('tv_wonder_labor_camp')]", 15,
                extra="name = worksite_building_reference alwaystransparent = no")
    organization_read = loc("ORG_READ",
        f'[tv_wonder_organization_competence|E] {ov("organization_competence")} @button_simple! 最大等级 {ov("organization_site_level_cap")}',
        f'[tv_wonder_organization_competence|E] {ov("organization_competence")} @button_simple! Max level {ov("organization_site_level_cap")}')
    body += txt(196, 60, 286, organization_read, 12, "right",
                extra="name = organization_concept_reference alwaystransparent = no")
    body += bar("camp_bar", 66, 87, 416, v("levels"), original("organization_site_level_cap_display"),
                f'{value("levels")} / {ov("organization_site_level_cap")}', height=20, fontsize=12)
    progress_tip = loc("STAT_HELP",
        f'工地等级 {value("levels")}\n劳工雇佣率 {value("employment", "0%")}\n有效等级 {ov("effective_worksite_levels", "2")}',
        f'Worksite levels {value("levels")}\nEmployment {value("employment", "0%")}\nEffective levels {ov("effective_worksite_levels", "2")}')
    def metric(name, x, width, label, value_key, value_name, *, icon, tooltip=None, style="flow_card", worksite=False):
        extra = f'name = {value_name}'
        if tooltip:
            extra += f' alwaystransparent = no tooltip = "{tooltip}"'
        content = raw(8, 6, width-16, f"@{icon}! [Localize('{label}')]", 12)
        if worksite:
            content = 'tv_worksite_maintenance_content = {}'
        else:
            content += txt(10, 30, width-20, value_key, 16, h=26, extra=extra)
        return box(name, x, 0, width, 64, content, style=style)
    calculation = metric("base_progress_card", 0, 90,
        loc("BASE_PROGRESS", "基础进度", "Base progress"),
        loc("BASE_PROGRESS_VALUE", f'{ov("worksite_scale_monthly_construction_progress")} /月',
            f'{ov("worksite_scale_monthly_construction_progress")} /mo'), "base_progress_value", icon="building_levels")
    calculation += raw(90, 20, 18, "×", 18, "center", 24, extra="name = employment_multiply")
    # Script population amounts use thousands; the displayed fraction is people.
    employed = f"[Multiply_CFixedPoint({v('employed')}, '(CFixedPoint)1000')|0]"
    workers = f"[Multiply_CFixedPoint({v('workers')}, '(CFixedPoint)1000')|0]"
    calculation += metric("employment_card", 108, 118,
        loc("EMPLOYMENT", "雇佣", "Employment"),
        loc("EMPLOYMENT_VALUE", f'{employed} / {workers}', f'{employed} / {workers}'),
        "employment_value", icon="laborers", tooltip=progress_tip)
    calculation += raw(226, 20, 18, "=", 18, "center", 24, extra="name = employment_equals")
    calculation += metric("camp_progress_card", 244, 90,
        loc("CAMP_PROGRESS", "工地进度", "Progress"),
        loc("CAMP_PROGRESS_VALUE", f'{value("camp_progress")} /月', f'{value("camp_progress")} /mo'),
        "camp_progress_value", icon="construction", tooltip=progress_tip)
    calculation += metric("maintenance_card", 348, 132,
        loc("MAINTENANCE", "总维护费", "Total maintenance"),
        loc("MAINTENANCE_VALUE", f'[{WORKSITE}.GetBuilding.GetUpkeep|2] @gold! /月', f'[{WORKSITE}.GetBuilding.GetUpkeep|2] @gold! /mo'),
        "maintenance_value", icon="gold", style="cost_card", worksite=True)
    body += f'widget = {{ name = worksite_calculation position = {{ 10 121 }} size = {{ 480 64 }} {calculation} }}'
    body += txt(18, 189, 170, loc("INPUT_GOODS", "投入品", "Inputs"), 11, h=20)
    body += txt(212, 189, 122, loc("LOCAL_PRICE", "当地单价", "Local price"), 11, "right", 20)
    body += txt(350, 189, 132, loc("DEMAND_SUPPLY", "需求 / 供给", "Demand / supply"), 11, "right", 20)
    for i, good in enumerate(maintenance):
        cell = raw(5, 0, 34, f'@{good}!', 19, "center", 32)
        cell += raw(44, 4, 158, f"[ShowGoodsName('{good}')]", 14,
                    extra=f"name = goods_reference_{good} alwaystransparent = no")
        cell += raw(200, 4, 122, f'{value(good+"_price", "2")} @gold!', 15, "right",
                    extra=f"name = price_{good}")
        demand_supply = f'{value(good+"_demand", "1")} / {value(good+"_supply", "1")}'
        short = loc(f"{good}_DEMAND_SUPPLY_SHORT", f'#R {demand_supply}#!', f'#R {demand_supply}#!')
        supplied = loc(f"{good}_DEMAND_SUPPLY_OK", f'#G {demand_supply}#!', f'#G {demand_supply}#!')
        condition = f"GreaterThan_CFixedPoint({v(good+'_demand')}, {v(good+'_supply')})"
        cell += txt(338, 4, 132, f"[SelectLocalization({condition}, '{short}', '{supplied}')]", 13, "right",
                    extra=f"name = demand_supply_{good}")
        body += box(f"resource_{good}", 12, 211+i*34, 476, 32, cell)
    can_build = f'"[And(LessThan_CFixedPoint({v("levels")}, {original("organization_site_level_cap")}), Not({PLAYER}.GetVariable(\'tv_wonder_construction_complete\').IsSet))]"'
    site_market = f"{PLAYER}.GetVariable('tv_wonder_site').GetLocation.GetMarket.Self"
    body += button("build_camp", 282, "TV_ENGINEERING_BUILD_WORKSITE_BUTTON", "uses_tv_wonder_materials", can_build,
                   market=site_market)
    return f'widget = {{ name = ol_organization_summary size = {{ 500 {ORGANIZATION_HEIGHT} }} {body} }}'


def maintenance_gui():
    """Small whole-file GUI override surface for maintenance compatibility."""
    content = raw(8, 6, 116, "@gold! [Localize('TV_OL_MAINTENANCE')]", 12)
    content += f'widget = {{ name = maintenance_building position = {{ 10 30 }} size = {{ 112 26 }} visible = "[{WORKSITE}.IsSet]" datacontext = "[{WORKSITE}.GetBuilding]"'
    content += txt(0, 0, 112, "TV_OL_MAINTENANCE_VALUE", 16, h=26,
                   extra='name = maintenance_value alwaystransparent = no tooltipwidget = { using = Building_upkeep_tooltip }') + '}'
    empty = loc("MAINTENANCE_EMPTY_VALUE", '0.00 @gold! /月', '0.00 @gold! /mo')
    content += txt(10, 30, 112, empty, 16, h=26,
                   extra=f'name = maintenance_empty_value visible = "[Not({WORKSITE}.IsSet)]"')
    return pretty(f'types TVWorksiteMaintenance {{ type tv_worksite_maintenance_content = widget {{ size = {{ 132 64 }} {content} }} }}')


def gui():
    body = organization()
    # Keep following sections adjacent to the compact summary.
    for name, y, h in (("logistics", LOGISTICS_Y, LOGISTICS_HEIGHT), ("settlement", SETTLEMENT_Y, 232)):
        body += box(f"{name}_paper", 0, y, 500, h, "", style="section", extra="alwaystransparent = yes")
    body += header("ol_log_header", LOGISTICS_Y, "TV_ENGINEERING_LOGISTICS_SECTION_TITLE", loc("LOG_READ", f'后勤 {ov("logistics_competence")}', f'Logistics {ov("logistics_competence")}'))
    body += f'widget = {{ name = ol_supply_graph position = {{ 10 {LOGISTICS_Y+40} }} size = {{ 480 384 }} {production_methods()} }}'
    # Materials + tools -> worksite. Keep all three inputs/results on one baseline.
    # Use the native market cards' independent frames, with room inside each edge.
    flow = ""
    def balance(good):
        values = f'{value(good+"_demand", "1")} / {value(good+"_supply", "1")}'
        return ''.join(raw(12, 30, 116, f'#{color} {values}#!', 16, h=26,
                           extra=f'visible = "[{eq(good+"_status", status)}]"')
                       for status, color in ((0, "R"), (1, "Y"), (2, "G")))
    cell = raw(12, 6, 116, "@tv_wonder_materials! [ShowGoodsName('tv_wonder_materials')]", 12,
               extra="alwaystransparent = no")
    cell += balance("tv_wonder_materials")
    import_tip = loc("IMPORT_HELP", f'进口补缺 {value("materials_gap", "1")}', f'Import shortfall {value("materials_gap", "1")}')
    flow += box("materials_market", 0, 0, 140, FLOW_CARD_HEIGHT, cell, style="flow_card",
               extra=f'alwaystransparent = no tooltip = "{import_tip}"')
    flow += raw(140, (FLOW_CARD_HEIGHT-30)//2, 26, "+", 22, "center", 30, extra="name = supply_plus")
    cell = raw(12, 6, 116, "@tools! [ShowGoodsName('tools')]", 12, extra="alwaystransparent = no")
    cell += balance("tools")
    flow += box("tools_market", 166, 0, 140, FLOW_CARD_HEIGHT, cell, style="flow_card")
    flow += raw(306, (FLOW_CARD_HEIGHT-30)//2, 34, "@button_simple!", 20, "center", 30, extra="name = supply_arrow")
    cell = 'icon = { name = camp_flow_icon position = { 12 6 } size = { 20 20 } texture = "gfx/interface/icons/buildings/tv_wonder_labor_camp.dds" alwaystransparent = yes }'
    cell += raw(36, 6, 92, f"[ShowBuildingTypeName('tv_wonder_labor_camp')] ×{value('levels')}", 12,
                extra="name = camp_flow_name alwaystransparent = no")
    cell += txt(12, 30, 116, loc("CAMP_SUPPLY", f'供应 {value("input_efficiency", "0%")}', f'Supply {value("input_efficiency", "0%")}'), 16, h=26,
                extra="name = camp_supply_value")
    flow += box("camp_flow", 340, 0, 140, FLOW_CARD_HEIGHT, cell, style="flow_card")
    flow += button("build_workshop", FLOW_CARD_HEIGHT+12, "TV_ENGINEERING_BUILD_MATERIAL_WORKSHOP_BUTTON", "tv_wonder_materials", x=0)
    body += f'widget = {{ name = ol_logistics_flow position = {{ 10 {LOGISTICS_Y+432} }} size = {{ 480 {FLOW_HEIGHT} }} {flow} }}'
    body += header("ol_summary_header", SETTLEMENT_Y, loc("SETTLEMENT", "每月进度结算", "Monthly progress"), loc("CHAIN", "营地 × 后勤 × 物资效率", "Camp × logistics × input efficiency"))
    factors = [("CAMP_PROGRESS", value("camp_progress")), ("LOG_READ", ov("logistics_progress_percent")+"%"), ("INPUT", value("input_efficiency", "0%")), ("RESULT", ov("monthly_construction_progress"))]
    loc("INPUT", "物资效率", "Input efficiency")
    loc("RESULT", "本月进度", "Monthly progress")
    for i, (label, val) in enumerate(factors):
        if label == "LOG_READ":
            label = "LOG_FACTOR"
            loc(label, "后勤", "Logistics")
        tip = loc("SETTLEMENT_HELP", f'营地进度 {value("camp_progress")} × 物资效率 {value("input_efficiency", "2%")} × 后勤 {ov("logistics_progress_percent")}% = {ov("monthly_construction_progress", "2")}。\n物资效率包括工具与建材，并保留原有结算取整。', f'Camp progress {value("camp_progress")} × input efficiency {value("input_efficiency", "2%")} × logistics {ov("logistics_progress_percent")}% = {ov("monthly_construction_progress", "2")}.\nInput efficiency includes tools and materials, preserving settlement rounding.')
        body += box(f"factor_{i}", 10+i*124, SETTLEMENT_Y+42, 108, 74, txt(4, 4, 100, "TV_OL_"+label, 13, "center") + raw(4, 31, 100, val, 18, "center", 30), accent=1 if i==2 else None, extra=f'alwaystransparent = no tooltip = "{tip}"')
        if i < 3:
            body += raw(118+i*124, SETTLEMENT_Y+66, 16, "=" if i==2 else "×", 13, "center")
    notice = loc("SHORTAGE", f'物资不足。补齐工具与建材后每月可增加 {value("recoverable")} 进度。', f'Input shortage. Restoring tools and materials adds {value("recoverable")} progress/month.')
    good_notice = loc("SUPPLIED", "施工物资供应充足。", "Construction inputs are sufficiently supplied.")
    body += box("diagnosis", 10, SETTLEMENT_Y+126, 480, 42,
                f'text_multi = {{ size = {{ 462 38 }} position = {{ 9 2 }} max_width = 462 autoresize = no fontsize = 12 text = "[SelectLocalization(GreaterThan_CFixedPoint({v("recoverable")}, \'(CFixedPoint)0\'), \'{notice}\', \'{good_notice}\')]" }}', accent=1)
    body += txt(10, SETTLEMENT_Y+176, 480, loc("CAPACITY", f'有效工坊 {ov("effective_material_workshop_levels")} / 所需 {ov("material_workshop_need")} 级', f'Effective workshops {ov("effective_material_workshop_levels")} / required {ov("material_workshop_need")}'), 12, "center")
    body += bar("workshop_capacity", 10, SETTLEMENT_Y+205, 480, original("effective_material_workshop_levels"), original("material_workshop_need_display"), "")
    locked = step_card('''widget = {
size = { 470 74 }
text_multi = {
    margin = { 4 6 }
    max_width = 462
    autoresize = yes
    text = "TV_ENGINEERING_ORG_LOG_LOCKED_TEXT"
    align = nobaseline|left
}
}''')
    return pretty(f'types TVOrgLogistics {{ type tv_org_logistics_active = widget {{ size = {{ 500 {H} }} {body} }} type tv_org_logistics_locked = vbox {{ size = {{ 500 -1 }} {locked} }} }}')


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


def outputs():
    LOC.clear()
    result = {"src/in_game/gui/tv_wonder_org_logistics.gui": gui(),
              "src/in_game/gui/tv_wonder_worksite_maintenance.gui": maintenance_gui(),
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


if __name__ == "__main__":
    main()
