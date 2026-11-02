"""Adapt the selected worksite's display to M&T's EPBM maintenance model.

epbm_price_building is called in building scope with EPBM's three saved inputs.
Its only financial output used here is local_var:epbm_bldg_cost; the upstream
market/PM cache remains upstream-owned. Never call the national calculate,
snapshot, split or charge effects: they mutate the real payment ledger.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.localization_policy import LOCALIZATION_LANGUAGES
from scripts_engineering_department.gen_wonder_org_logistics import PLAYER, pretty, raw, txt

MOD = "submods/tv_meiou_and_taxes_compat"
REFERENCE = ROOT / ".eu5-base/reference_mods/3735059838/in_game/common"
SCRIPT = "scripts/compat/gen_tv_meiou_and_taxes_worksite_maintenance.py"
PREFIX = "tv_ol_mt_"


def estates():
    source = (REFERENCE / "scripted_effects/epbm_effects.txt").read_text(encoding="utf-8-sig")
    result = re.findall(r"\$effect\$\s*=\s*\{\s*estate\s*=\s*(\w+)\s*\}", source)
    if not result or len(result) != len(set(result)):
        raise ValueError("Review EPBM's estate iterator before regenerating maintenance")
    return tuple(result)


def effects():
    shares = estates()
    names = ("total", "crown", *shares)
    lines = ["REPLACE:tv_wonder_clear_worksite_maintenance_display_effect = {"]
    lines += [f"remove_variable = {PREFIX}{name}" for name in (*names, "ready")]
    lines += ["}", "REPLACE:tv_wonder_update_worksite_maintenance_display_effect = {"]
    lines += [f"set_local_variable = {{ name = {PREFIX}{name} value = 0 }}" for name in ("total", "crown", "crown_only")]
    lines += ['if = { limit = { has_local_variable = tv_ol_worksite }',
              'local_var:tv_ol_worksite ?= {',
              'if = { limit = { is_opened = yes building_level > 0 }',
              'save_temporary_scope_as = epbm_bldg',
              'building_type = { save_temporary_scope_as = epbm_bt }',
              'location = { market = { save_temporary_scope_as = epbm_mkt } }',
              'epbm_price_building = yes',
              'if = { limit = { building_category = government_category }',
              f'set_local_variable = {{ name = {PREFIX}crown_only value = 1 }}', '}',
              'scope:tv_ol_owner = {',
              f'set_local_variable = {{ name = {PREFIX}total value = {{ value = local_var:epbm_bldg_cost multiply = epbm_cost_share multiply = epbm_inflation_factor }} }}',
              '}', '}', '}', '}',
              f'set_local_variable = {{ name = {PREFIX}crown value = local_var:{PREFIX}total }}',
              f'if = {{ limit = {{ local_var:{PREFIX}crown_only = 0 }}',
              f'change_local_variable = {{ name = {PREFIX}crown multiply = "estate_power(estate_type:crown_estate)" }}', '}',
              'epbm_for_each_estate = { effect = tv_wonder_mt_worksite_estate_share_display_effect }']
    lines += [f'set_variable = {{ name = {PREFIX}{name} value = local_var:{PREFIX}{name} }}' for name in names]
    lines += [f'set_variable = {{ name = {PREFIX}ready value = 1 }}']
    lines += [f'remove_local_variable = {PREFIX}{name}' for name in (*names, "crown_only")]
    # EPBM's pricing helper leaves scratch locals in the caller's effect context.
    lines += [f'remove_local_variable = {name}' for name in (
        "epbm_bldg_cost", "epbm_per_level", "epbm_price", "epbm_qty", "epbm_loc_access", "epbm_bldg_eff")]
    lines += ['}', 'tv_wonder_mt_worksite_estate_share_display_effect = {',
              f'set_local_variable = {{ name = {PREFIX}$estate$ value = 0 }}',
              'if = { limit = { country_has_estate = estate_type:$estate$_estate',
              f'local_var:{PREFIX}crown_only = 0', '}',
              f'set_local_variable = {{ name = {PREFIX}$estate$ value = {{ value = local_var:{PREFIX}total multiply = "estate_power(estate_type:$estate$_estate)" }} }}',
              '}', '}']
    return '# Country display hooks; the caller has calculated local_var:tv_ol_worksite.\n' + pretty('\n'.join(lines))


def gui():
    ready = f"{PLAYER}.GetVariable('{PREFIX}ready').IsSet"
    content = raw(8, 6, 116, "@gold! [Localize('TV_MT_OL_MAINTENANCE')]", 12)
    content += txt(10, 30, 112, "TV_MT_OL_MAINTENANCE_VALUE", 16, h=26,
                   extra=f'name = maintenance_value visible = "[{ready}]" alwaystransparent = no tooltipwidget = {{ using = tv_mt_worksite_maintenance_tooltip }}')
    content += txt(10, 30, 112, "TV_MT_OL_MAINTENANCE_EMPTY_VALUE", 16, h=26,
                   extra=f'name = maintenance_empty_value visible = "[Not({ready})]"')

    def row(name, label, *, estate=None):
        visible = '' if estate is None else f'visible = "[InternationalOrganizationsView.GetPlayer.GetGovernment.GetEstateFromKey(\'{estate}_estate\').ExistsForCountry]"'
        return f'''TooltipManualTableField = {{ name = maintenance_share_{name} {visible}
            blockoverride "field_content" {{
                text_single = {{ layoutpolicy_horizontal = expanding text = "{label}" }}
                expand = {{}}
                text_single = {{ min_width = 80 align = right raw_text = "[{PLAYER}.GetVariable('{PREFIX}{name}').GetValue|2] @gold!" }}
            }}
        }}'''

    rows = row("total", "TV_MT_OL_MAINTENANCE_TOTAL")
    rows += row("crown", "[ShowEstateTypeName('crown_estate')]")
    rows += ''.join(row(estate, f"[ShowEstateTypeName('{estate}_estate')]", estate=estate) for estate in estates())
    template = f'''template tv_mt_worksite_maintenance_tooltip {{
        ContextualTooltipType = {{
            blockoverride "title_text" {{ text = "TV_MT_OL_MAINTENANCE_TITLE" }}
            blockoverride "title_icon" {{ icon = {{ using = tooltip_title_icon_size texture = "[GetConceptTexture('building_maintenance')]" }} }}
            blockoverride "concept_link" {{ text = "[building_maintenance|e]" }}
            blockoverride "tooltip_content" {{
                TooltipTextBlock = {{ blockoverride "text" {{ text = "TV_MT_OL_MAINTENANCE_HELP" }} }}
                TooltipListBase = {{ {rows} }}
            }}
        }}
    }}'''
    return pretty(template + f'\ntypes TVWorksiteMaintenance {{ type tv_worksite_maintenance_content = widget {{ size = {{ 132 64 }} {content} }} }}')


def outputs():
    header = f"# @Generated by {SCRIPT}\n# Edit the generator; do not hand-edit.\n"
    result = {
        f"{MOD}/in_game/common/scripted_effects/tv_wonder_mt_worksite_maintenance.txt": effects(),
        f"{MOD}/in_game/gui/tv_wonder_worksite_maintenance.gui": gui(),
    }
    values = {
        "TV_MT_OL_MAINTENANCE": ("国库维护费", "Treasury upkeep"),
        "TV_MT_OL_MAINTENANCE_TITLE": ("工地维护费", "Worksite maintenance"),
        "TV_MT_OL_MAINTENANCE_HELP": ("按当前情况估算的每月开支。", "Estimated monthly expenses under current conditions."),
        "TV_MT_OL_MAINTENANCE_TOTAL": ("总计", "Total"),
        "TV_MT_OL_MAINTENANCE_VALUE": (
            f"[{PLAYER}.GetVariable('{PREFIX}crown').GetValue|2] @gold! /月",
            f"[{PLAYER}.GetVariable('{PREFIX}crown').GetValue|2] @gold! /mo"),
        "TV_MT_OL_MAINTENANCE_EMPTY_VALUE": ("0.00 @gold! /月", "0.00 @gold! /mo"),
    }
    for language in LOCALIZATION_LANGUAGES:
        index = 0 if language == "simp_chinese" else 1
        lines = [f"l_{language}:"]
        lines += [f' {key}:0 "{pair[index]}"' for key, pair in values.items()]
        result[f"{MOD}/main_menu/localization/{language}/tv_wonder_mt_worksite_maintenance_l_{language}.yml"] = '\n'.join(lines) + '\n'
    return {path: header + content for path, content in result.items()}


def main():
    for relative, content in outputs().items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8-sig", newline="\n")
        print(f"Wrote {relative}")


if __name__ == "__main__":
    main()
