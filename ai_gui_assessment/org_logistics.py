"""Render the installed mod's organization/logistics widgets in their real panel.

The fixture is explicit invented market/employment data, not a script emulator.
Render a tall scroll area to export the entire card using shared detail cropping.
"""
import argparse
from copy import copy
from dataclasses import replace
import json
import math
import re
from pathlib import Path

import engineering
import org_logistics_mockups as prototype
from scripts_engineering_department import gen_wonder_org_logistics as gen

OUT = engineering.WORKSPACE / "ai_gui_assessment/images/org_logistics_mod"


def meiou_resources(resources):
    """Overlay the actual compatch's small GUI file and localization."""
    from eu5_gui_renderer.gui import GuiDB, collect_files
    from eu5_gui_renderer.paths import LANGUAGE
    from scripts.compat import gen_tv_meiou_and_taxes_worksite_maintenance as mt
    relative = "in_game/gui/tv_wonder_worksite_maintenance.gui"
    native = engineering.WORKSPACE / "src" / relative
    compat = engineering.WORKSPACE / mt.MOD / relative
    files = [compat if path.resolve() == native.resolve() else path for path in collect_files()]
    loc = copy(resources.loc)
    loc.d = dict(resources.loc.d)
    path = engineering.WORKSPACE / mt.MOD / f"main_menu/localization/{LANGUAGE}/tv_wonder_mt_worksite_maintenance_l_{LANGUAGE}.yml"
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = loc.LINE_RE.match(line)
        if match:
            loc.d[match[1]] = match[2]
    return replace(resources, db=GuiDB(files), loc=loc)


def meiou_sample(state, loc=None):
    """Explicit display outputs; this does not execute or emulate EPBM pricing."""
    from scripts.compat import gen_tv_meiou_and_taxes_worksite_maintenance as mt
    if loc is None:
        from eu5_gui_renderer.data import Loc
        loc = Loc()
    values = {mt.PREFIX + name: 0 for name in mt.estates()}
    values.update(tv_ol_mt_ready=1, tv_ol_mt_total=100, tv_ol_mt_crown=20,
                  tv_ol_mt_nobles=30, tv_ol_mt_clergy=50)
    mocks = [(re.escape(f"InternationalOrganizationsView.GetPlayer.GetGovernment.GetEstateFromKey('{name}_estate').ExistsForCountry"),
              name in ("nobles", "clergy")) for name in mt.estates()]
    mocks += [(re.escape(f"ShowEstateTypeName('{name}_estate')"), loc.get(f"{name}_estate"))
              for name in ("crown", *mt.estates())]
    return replace(state, player_variables={**state.player_variables, **values}), mocks


def help_mocks(loc):
    """Only the known encyclopedia action and static name helpers for this hover."""
    action = {"__type__": "UIAction", "HasAnyClickModifierAvailable": False}
    for click in ("LeftClick", "LeftClickAndConfirm", "RightClick", "RightClickAndConfirm"):
        action[f"Is{click}Visible"] = click == "LeftClick"
        action[f"Is{click}Enabled"] = click == "LeftClick"
        action[f"Get{click}Name"] = loc.get("OPEN_EUROPEDIA") if click == "LeftClick" else ""
        action[f"Get{click}Tooltip"] = ""
        action[f"Get{click}Cost"] = ""
    for side in ("Left", "Right"):
        for modifier in ("shift", "ctrl", "alt"):
            action[f"Is{side}ClickModifierEnabled('{modifier}')"] = False
    mocks = [(re.escape("ExtraTooltipInfo.GetUIAction"), action),
             (re.escape("PdxGuiWidget.HasTooltipMetaGameConcept"), False),
             (re.escape("PdxGuiWidget.GetTooltipMetaGameConcept"), ""),
             ("IsActionConfirmAndHoldMode", False), ("IsActionDialogMode", True),
             (re.escape("StringToConditionListOnlyFail('').GetOutput"), ""),
             (re.escape("StringToConditionListOnlyFailAndWarningCollapseRequirement('')"), {"__type__": "ConditionList", "GetLines": []})]
    for kind, keys in (("BuildingType", ("tv_wonder_labor_camp", "tv_wonder_material_dispatch_point")), ("Goods", ("tv_wonder_materials",))):
        mocks.extend((re.escape(f"Show{kind}Name('{key}')"), loc.get(key)) for key in keys)
    return mocks


def production_type_context(recipes, loc):
    """Explicit native data-model samples, derived from the current recipes."""
    def good(key):
        return {"__type__": "Goods", "Self": key, "GetName": loc.get(key),
                "GetNameWithNoTooltip": loc.get(key),
                f"GetGoodsIcon('{key}')": f"gfx/interface/icons/trade_goods/icon_goods_{key}.dds"}
    methods = []
    for recipe in recipes:
        key = recipe["id"]
        methods.append({"__type__": "ProductionMethod", "Self": key,
                        "GetNameWithNoTooltip": loc.get(key), "HasFlavorText": False,
                        "IsProducing": True, "GetOutput": recipe["output"],
                        "GetProduced": good(recipe["produced"]),
                        f"GetProductionMethodIcon('{key}')": "gfx/interface/icons/production_methods/_default.dds",
                        "GetGoodsDemand.GetEntries": [
                            {"__type__": "GoodsDemandEntry", "GetValue": quantity, "GetGoods": good(g)}
                            for g, quantity in recipe["inputs"].items()]})
    return {"__type__": "BuildingType", "Self": "tv_wonder_material_dispatch_point",
            "GetProductionMethodsLabel": loc.get("POSSIBLE_PRODUCTION_METHODS_LABEL"),
            "GetPossibleProductionMethods": [{"__type__": "PossibleProductionMethods", "GetMethods": methods}]}


def scenario(name, loc=None):
    state = engineering.scenario_state("survey" if name == "locked" else "construction")
    if name == "locked":
        return state
    m = prototype.load_model(name)
    values = {gen.PREFIX+key: 0 for key in gen.variables()}
    values.update(tv_ol_ready=1, tv_ol_workshop_type=1, tv_ol_worksite=1, tv_ol_levels=m["level"], tv_ol_employment=m["employment"],
                  tv_ol_employed=m["level"]*2*m["employment"], tv_ol_workers=m["level"]*2,
                  tv_ol_camp_progress=math.floor(m["camp_progress"]))
    for good, market in m["market"].items():
        if good not in m["maintenance"]:
            continue
        ratio = min(1, market["supply"]/market["demand"]) if market["demand"] else 1
        prefix = gen.PREFIX+good+"_"
        values.update({prefix+"demand": market["demand"], prefix+"supply": market["supply"],
                       prefix+"ratio": ratio, prefix+"status": 2 if ratio >= 1 else 1 if ratio >= .7 else 0,
                       prefix+"price": m["prices"].get(good, m["base_prices"][good])})
        values[prefix+"premium"] = values[prefix+"price"]/m["base_prices"][good]-1
    # Current game effect averages tools and materials only when a camp lacks goods.
    efficiency = (values["tv_ol_tools_ratio"]+values["tv_ol_tv_wonder_materials_ratio"])/2
    adjusted = math.floor(values["tv_ol_camp_progress"]*efficiency)
    values["tv_ol_input_efficiency"] = adjusted/values["tv_ol_camp_progress"] if values["tv_ol_camp_progress"] else 0
    values["tv_ol_recoverable"] = (values["tv_ol_camp_progress"]-adjusted)*m["multiplier"]
    values["tv_ol_materials_gap"] = m["gap"]
    values.update(tv_wonder_organization_competence=m["organization"], tv_wonder_organization_site_level_cap=m["cap"],
                  tv_wonder_organization_site_level_cap_display=max(1,m["cap"]),
                  tv_wonder_worksite_scale_monthly_construction_progress=m["base_progress"],
                  tv_wonder_logistics_competence=m["logistics"], tv_wonder_logistics_progress_percent=m["multiplier"]*100,
                  tv_wonder_effective_worksite_levels=m["effective"], tv_wonder_monthly_construction_progress=adjusted*m["multiplier"],
                  tv_wonder_effective_material_workshop_levels=math.floor(m["market"]["tv_wonder_materials"]["supply"]),
                  tv_wonder_material_workshop_need=math.floor(m["effective"]*20),
                  tv_wonder_material_workshop_need_display=max(1,math.floor(m["effective"]*20)))
    if loc is None:
        from eu5_gui_renderer.data import Loc
        loc = Loc()
    return replace(state, name="org-logistics-"+name, tab="resolutions", player_variables={**state.player_variables, **values},
                   objects={**state.objects, "tv_ol_workshop_type.GetBuildingType": production_type_context(m["recipes"], loc),
                            # Explicit sample of the native API, not an upkeep formula emulator.
                            "tv_ol_worksite.GetBuilding": {"__type__": "Building", "GetUpkeep": 37.25,
                                                         "GetUpkeepInfo": ""}})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", choices=("all", "active", "locked", "full"), default="all")
    parser.add_argument("--language", default="simp_chinese")
    parser.add_argument("--fixture", type=Path, help="Overlay explicit sample values on the selected scenario")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--meiou-and-taxes", action="store_true", help="Overlay the M&T maintenance widget with explicit sample shares")
    hover = parser.add_mutually_exclusive_group()
    hover.add_argument("--hover-method", type=int, choices=range(1, 9), help="Preview one native production-method tooltip")
    hover.add_argument("--hover-help", action="store_true", help="Preview the complete encyclopedia tooltip and native action footer")
    hover.add_argument("--hover-maintenance", action="store_true", help="Preview the maintenance cost breakdown")
    args = parser.parse_args()
    out = OUT / args.language
    engineering.configure(output_root=out, language=args.language)
    from eu5_gui_renderer.preview import load_resources, has_diagnostics
    resources = load_resources()
    if args.meiou_and_taxes:
        resources = meiou_resources(resources)
    reports, failed = [], False
    for name in ("active", "locked", "full") if args.state == "all" else (args.state,):
        selector = None
        suffix = ""
        extra_mocks = []
        if args.hover_help:
            selector = "org_logistics_help"
            suffix = "_help"
            extra_mocks = help_mocks(resources.loc)
        elif args.hover_method and name != "locked":
            seen = []
            def selector(node):
                if node.get("name") != "production_method_recipe":
                    return False
                seen.append(node)
                return len(seen) == args.hover_method
            suffix = f"_method_{args.hover_method}"
        elif args.hover_maintenance and name != "locked":
            selector = "maintenance_value"
            suffix = "_maintenance"
        state = scenario(name, resources.loc)
        if args.meiou_and_taxes:
            state, mt_mocks = meiou_sample(state, resources.loc)
            extra_mocks += mt_mocks
            suffix += "_mt"
        if args.fixture:
            state = engineering.load_fixture(state, args.fixture)
            suffix += "_" + args.fixture.stem
        report = engineering.render(state, resources=resources, height=3200,
                                    output=out/f"{name}{suffix}.png", hover=selector, extra_mocks=extra_mocks)
        failed |= has_diagnostics(report)
        reports.append(report)
        print(name, report["details"], "diagnostics", has_diagnostics(report))
    (out/"index.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    return int(args.strict and failed)


if __name__ == "__main__":
    raise SystemExit(main())
