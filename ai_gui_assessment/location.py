"""Render the shipped location window and its click-open wonder menu.

All scenario values are fictional. Modifier tables read the selected mod's
generated definitions; native trigger/effect evaluation is not emulated.
"""
from __future__ import annotations

import argparse
from copy import copy
from dataclasses import replace
import json
from pathlib import Path
import re
import sys

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))
GUI_PATH = 'in_game/gui/location_window.gui'
STATES = {
    'single': [(102, 1)],
    'multiple': [(102, 1), (3, 2), (1, 1)],
    'empty': [],
    'overflow': [(102, 1), (3, 2), (1, 1), (2, 1), (4, 1), (5, 1)],
    'unbuilt': [(102, 0)],
    'shell': [(3, 3, -1)],
    'dedicated': [(102, 6, 1), (3, 3, 2), (1, 2, 3)],
    'four_modifiers': [(27, 3, 2), (40, 3, 2), (53, 3, 2)],
    'jerusalem': [(140, 1), (103, 1)],
    'marseille': [(195, 1)],
}


def configure(args):
    renderer = (args.renderer_root or args.workspace / '.eu5-base/ai_gui_assessment/renderer').resolve()
    sys.path.insert(0, str(renderer))
    from eu5_gui_renderer.config import configure_paths
    configure_paths(workspace=args.workspace, mod_root=args.mod_root, game_root=args.game_root,
                    output_root=args.output_root, language=args.language)


def wonder_variables(wonders):
    result = {'tv_wonder_tooltip_overflow_count': max(0, len(wonders) - 5)}
    for group, limit in (('display', 3), ('tooltip', 5)):
        for index in range(1, limit + 1):
            values = dict(id=None, level=0, ritual_style=0, ritual_completed=0)
            if index <= len(wonders):
                ident, level, *style = wonders[index - 1]
                ritual = style[0] if style else 0
                values.update(id=ident, level=level, ritual_style=ritual, ritual_completed=int(ritual > 0))
            result.update({f'tv_wonder_{group}_slot_{index}_{key}': value for key, value in values.items()})
    return result


def scenario_mocks(state, resources, menu=True, *, localized_tables=None):
    from eu5_gui_renderer.fixtures import object_mocks, variable_mocks, requirements_list, string_pair_list, modifier_sample_lines
    from eu5_gui_renderer.paths import MOD, LANGUAGE
    from eu5_gui_renderer.pdx import parse
    from scripts_engineering_department.in_game.gui import gen_location_window as source
    from scripts_engineering_department.wonder_mechanics.io import load_all_wonder_mechanics
    from scripts_engineering_department.wonder_mechanics.rituals import ritual_styles
    payload = json.loads((WORKSPACE / 'ai_gui_assessment/fixtures/location.json').read_text(encoding='utf-8'))
    result = [(re.escape(key.replace('LocationView.GetLocation.', 'Location.')), value)
              for key, value in payload['bindings'].items()]
    for expression, context in payload['objects'].items():
        result.extend(object_mocks(expression, context))
        if expression == 'LocationView.GetLocation':
            result.extend(object_mocks('Location', context))
    result.extend(variable_mocks('Location.MakeScope', wonder_variables(STATES[state])))
    result.append((re.escape(f"LocationView.Vars.Exists('{source.MENU_OPEN_VAR}')"), menu))
    result.append((re.escape("GetGlobalVariable('hagia_sophia_now_mosque').IsSet"), False))
    # Show the native delayed flavor section in this settled-hover sample.
    result.append((re.escape('ExtraTooltipInfo.IsDelayedInfoShowing'), True))
    # Native building links use the current final-building name. The offline
    # renderer samples that text only; it does not emulate native link interaction.
    all_wonders, mechanics = load_all_wonder_mechanics()
    wonders = {w['id']: w for w in all_wonders}
    for slot, (ident, *_) in enumerate(STATES[state][:5], 1):
        key = wonders[ident]['final_building']
        expression = source.slot_building_type_expr('tooltip', slot).replace('LocationView.GetLocation.', 'Location.').replace(' ', '')
        result.extend(object_mocks(expression, {'__type__': 'BuildingType',
            'GetName': resources.loc.get(key), 'GetNameWithNoTooltip': resources.loc.get(key),
            'GetFlavorText': resources.loc.get(key + '_desc')}))
    metadata = json.loads((WORKSPACE / 'data/index/modifier_localization.json').read_text(encoding='utf-8'))['modifiers']
    modifiers = {}
    for path in [p for stage in ('main_menu', 'in_game')
                 for p in (MOD / stage / 'common/static_modifiers').glob('*.txt')]:
        for node in parse(path.read_text(encoding='utf-8-sig'), str(path)):
            if node.is_block() and node.key.startswith('tv_wonder_'):
                modifiers[node.key] = {n.key: (n.value == 'yes' if n.value in ('yes', 'no') else float(n.value))
                                       for n in node.value if n.key in metadata}
    # Sample expanded native tables from the actual reward definitions.
    for ident in {entry[0] for entry in STATES[state][:5]}:
        for row in ritual_styles(wonders[ident], mechanics):
            completion_key = f"TV_WONDER_RITUAL_COMPLETION_{row['style']}_{ident}"
            expected = (f"[ShowScriptedEffectForScope('tv_wonder_display_{ident}_ritual_{row['style']}_completion_effect', LocationView.GetLocation.MakeScope.Self)]"
                        if row['one_shot'] else '')
            if resources.loc.get(completion_key) != expected:
                raise ValueError(f'Ritual completion route does not match reward: {completion_key}')
            if localized_tables is not None:
                # Explicit samples of the current rewards, not engine execution.
                sample = '(Sample)' if LANGUAGE == 'english' else '【示例】'
                localized_tables[completion_key] = string_pair_list([
                    (f"{sample} {resources.loc.get(reward['type']) or reward['type']}", f"{reward['value']:+g}")
                    for reward in row['one_shot']
                ])
            for scope, modifier in (('COUNTRY', row['modifier']), ('LOCAL', row['location_modifier'])):
                rows = []
                if modifier:
                    if modifier not in modifiers:
                        raise ValueError(f'Missing ritual modifier: {modifier}')
                    rows = [tuple(line.rsplit(': ', 1)) for line in modifier_sample_lines(modifiers[modifier], metadata, resources.loc)]
                key = f"TV_WONDER_RITUAL_{scope}_MODIFIERS_{row['style']}_{ident}"
                expected = f"[ShowModifierEffect('{modifier}')]" if modifier else ''
                if resources.loc.get(key) != expected:
                    raise ValueError(f'Ritual table route does not match reward: {key}')
                if localized_tables is not None:
                    localized_tables[key] = string_pair_list(rows)
    for index, (ident, current_level, *_) in enumerate(STATES[state][:5], 1):
        for local, getter in ((False, source.slot_modifier_key_expr), (True, source.slot_local_modifier_key_expr)):
            key = f'tv_wonder_display_{ident}_{"local_" if local else ""}level_{max(current_level, 1)}'
            if key not in modifiers:
                raise ValueError(f'Missing display modifier: {key}')
            rows = [tuple(line.rsplit(': ', 1)) for line in modifier_sample_lines(modifiers[key], metadata, resources.loc)]
            expression = f'ShowModifierEffect({getter("tooltip", index)})'.replace(' ', '')
            result.append((re.escape(expression.replace('LocationView.GetLocation.', 'Location.')), string_pair_list(rows)))
        expression = f"ShowTriggerConditionsForScope({source.slot_base_site_rules_trigger_key_expr('tooltip', index)},{source.LOCATION_SCOPE})".replace(' ', '')
        result.append((re.escape(expression.replace('LocationView.GetLocation.', 'Location.')), requirements_list([
            ('(Sample) Site requirements satisfied' if LANGUAGE == 'english' else '【示例】满足建造地点条件', True)])))
    result.append((r'GetRequirementLineAux\([^)]*\)', {'__type__': 'RequirementLineAux',
                  "GetAuxParentArrowSize('(float)3','(float)0','(float)10')": ('vec', 3, 10)}))
    return result


def build(resources, expander, panel_width, height, menu=False):
    from eu5_gui_renderer.gui import Element, build_target
    from eu5_gui_renderer.paths import MOD
    panel = build_target(resources.db, expander, 'location_window', MOD / GUI_PATH)
    panel.props.update(size=[str(panel_width), str(height)], position=['0', '0'],
                       parentanchor='top|left', widgetanchor='top|left')
    root = Element('widget', 'location_preview', children=[panel])
    # Use the shipped child and its anchors. Artificially positioning a detached
    # copy here used to conceal overlap in the actual context-menu attachment.
    def visit(node):
        yield node
        for child in node.children:
            yield from visit(child)
    popup = next((child for child in visit(panel) if child.props.get('name') == 'tv_location_wonders_panel'), None)
    if popup is None:
        raise ValueError('Missing shipped wonder panel in location window')
    return root, panel, popup if menu else None


def render(state, resources, *, width=1600, height=1080, scale=1, menu=True,
           extra_mocks=None, output=None, hover=None):
    from eu5_gui_renderer.gui import Expander
    from eu5_gui_renderer.paths import OUTPUT, MOD
    from eu5_gui_renderer.preview import render_tree
    expander = Expander(resources.db)
    root, panel, popup = build(resources, expander, 560, height, menu=menu and bool(STATES[state]))
    details = {'panel': panel}
    if popup is not None:
        details['menu'] = popup
    # The renderer cannot parse localized native table markup. Supply the exact
    # verified localization routes as table fixtures in this render's own copy.
    tables = {}
    mocks = scenario_mocks(state, resources, menu, localized_tables=tables)
    sample_loc = copy(resources.loc)
    sample_loc.d = {**resources.loc.d, **tables}
    return render_tree(root, expander, replace(resources, loc=sample_loc), (extra_mocks or []) + mocks,
        width=width, height=height, scale=scale, output=output or OUTPUT / f'location_{state}.png',
        detail_elements=details, tooltip_selector=hover, metadata={'scenario': 'location', 'state': state, 'sample_data': True,
            'menu_open': popup is not None,
            'gui': str(MOD / GUI_PATH), 'wonders': STATES[state],
            'sample_tables': 'Expanded modifier values and one-shot reward samples from current mod definitions. Site checks are explicit sample results.',
            'unsupported': ['No save, script execution, clicks, scrolling, 3D map, portraits or procedural flags.',
                            'Queues and secondary lists are empty sample data; infrastructure tab is selected.']})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--state', choices=STATES, default='multiple')
    selection.add_argument('--all', action='store_true')
    parser.add_argument('--closed', action='store_true')
    parser.add_argument('--hover', help='Name of the shipped artwork, level badge or ritual strip')
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('--workspace', type=Path, default=WORKSPACE)
    parser.add_argument('--renderer-root', type=Path)
    parser.add_argument('--mod-root', type=Path, default=Path('src'))
    parser.add_argument('--game-root', type=Path)
    parser.add_argument('--output-root', type=Path, default=Path('ai_gui_assessment/images/location'))
    parser.add_argument('--mocks', type=Path)
    parser.add_argument('--language', default='simp_chinese')
    parser.add_argument('--width', type=int, default=1600)
    parser.add_argument('--height', type=int, default=1080)
    parser.add_argument('--scale', type=float, default=1)
    args = parser.parse_args(argv)
    try:
        configure(args)
        from eu5_gui_renderer.preview import load_resources, write_report, has_diagnostics
        from eu5_gui_renderer.fixtures import load_mocks
        from eu5_gui_renderer.paths import OUTPUT
        resources = load_resources()
        extra = load_mocks(args.workspace / args.mocks) if args.mocks else []
        reports = []
        for state in STATES if args.all else [args.state]:
            report = render(state, resources, width=args.width, height=args.height, scale=args.scale,
                            menu=not args.closed, hover=args.hover, extra_mocks=extra)
            reports.append(report)
            print(f"Rendered {report['output']}; unknown={len(report['unknown_expressions'])}, contexts={len(report['unresolved_contexts'])}, missing_textures={len(report['missing_textures'])}", flush=True)
        write_report(OUTPUT / 'location_index.json', reports)
        return int(args.strict and any(has_diagnostics(r) for r in reports))
    except (ValueError, OSError, re.error) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    raise SystemExit(main())
