"""Render the shipped location window and its click-open wonder menu.

All scenario values are fictional. Modifier tables read the selected mod's
generated definitions; native trigger/effect evaluation is not emulated.
"""
from __future__ import annotations

import argparse
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
            values = dict(id=None, level=None, ritual_style=None, ritual_completed=None)
            if index <= len(wonders):
                ident, level = wonders[index - 1]
                values.update(id=ident, level=level, ritual_style=0, ritual_completed=0)
            result.update({f'tv_wonder_{group}_slot_{index}_{key}': value for key, value in values.items()})
    return result


def scenario_mocks(state, resources, selected_slot=1):
    from eu5_gui_renderer.fixtures import object_mocks, variable_mocks, requirements_list, string_pair_list, modifier_sample_lines
    from eu5_gui_renderer.paths import MOD, LANGUAGE
    from eu5_gui_renderer.pdx import parse
    from scripts_engineering_department.in_game.gui import gen_location_window as source
    payload = json.loads((WORKSPACE / 'ai_gui_assessment/fixtures/location.json').read_text(encoding='utf-8'))
    result = [(re.escape(key.replace('LocationView.GetLocation.', 'Location.')), value)
              for key, value in payload['bindings'].items()]
    for expression, context in payload['objects'].items():
        result.extend(object_mocks(expression, context))
        if expression == 'LocationView.GetLocation':
            result.extend(object_mocks('Location', context))
    result.extend(variable_mocks('Location.MakeScope', wonder_variables(STATES[state])))
    for slot in range(1, source.TOOLTIP_SLOT_MAX + 1):
        result.append((re.escape(source.menu_slot_selected_expr(slot).replace(' ', '')), slot == selected_slot))
    # The native context-menu host provides this object, just as it does for
    # production_method_chooser_menu. This is popup context, not wonder data.
    result.append((re.escape('ExtraTooltipInfo.GetTintColor'), [1, 1, 1, 1]))
    result.append((re.escape('ExtraTooltipInfo.TooltipIsReady'), True))
    result.append((re.escape("GetGlobalVariable('hagia_sophia_now_mosque').IsSet"), False))
    metadata = json.loads((WORKSPACE / 'data/index/modifier_localization.json').read_text(encoding='utf-8'))['modifiers']
    modifiers = {}
    for path in [p for stage in ('main_menu', 'in_game')
                 for p in (MOD / stage / 'common/static_modifiers').glob('*.txt')]:
        for node in parse(path.read_text(encoding='utf-8-sig'), str(path)):
            if node.is_block() and node.key.startswith('tv_wonder_display_'):
                modifiers[node.key] = {n.key: (n.value == 'yes' if n.value in ('yes', 'no') else float(n.value))
                                       for n in node.value if n.key in metadata}
    for index, (ident, level) in enumerate(STATES[state][:5], 1):
        for local, getter in ((False, source.slot_modifier_key_expr), (True, source.slot_local_modifier_key_expr)):
            key = f'tv_wonder_display_{ident}_{"local_" if local else ""}level_{level}'
            if level > 0 and key not in modifiers:
                raise ValueError(f'Missing current display modifier: {key}')
            rows = [tuple(line.rsplit(': ', 1)) for line in modifier_sample_lines(modifiers.get(key, {}), metadata, resources.loc)]
            expression = f'ShowModifierEffect({getter("tooltip", index)})'.replace(' ', '')
            result.append((re.escape(expression.replace('LocationView.GetLocation.', 'Location.')), string_pair_list(rows)))
        expression = f"ShowTriggerConditionsForScope({source.slot_base_site_rules_trigger_key_expr('tooltip', index)},{source.LOCATION_SCOPE})".replace(' ', '')
        result.append((re.escape(expression.replace('LocationView.GetLocation.', 'Location.')), requirements_list([
            ('(Sample) Site requirements satisfied' if LANGUAGE == 'english' else '【示例】满足建造地点条件', True)])))
    result.append((r'GetRequirementLineAux\([^)]*\)', {'__type__': 'RequirementLineAux',
                  "GetAuxParentArrowSize('(float)3','(float)0','(float)10')": ('vec', 3, 10)}))
    return result


def wonder_menu_spec(resources):
    """Read the actual button attachment; do not render a detached mock menu."""
    from eu5_gui_renderer.paths import MOD

    def visit(nodes):
        for node in nodes:
            if not node.is_block():
                continue
            if any(c.key == 'name' and c.value == 'tv_location_wonders_button' for c in node.value):
                return next(c for c in node.value if c.key == 'contextmenu_widget').value[0]
            found = visit(node.value)
            if found is not None:
                return found

    spec = visit(resources.db.roots[str(MOD / GUI_PATH)])
    if spec is None:
        raise ValueError('Missing shipped wonder button/contextmenu_widget')
    return spec


def build(resources, expander, panel_width, height, menu=False):
    from eu5_gui_renderer.gui import Element, build_target
    from eu5_gui_renderer.paths import MOD
    panel = build_target(resources.db, expander, 'location_window', MOD / GUI_PATH)
    panel.props.update(size=[str(panel_width), str(height)], position=['0', '0'],
                       parentanchor='top|left', widgetanchor='top|left')
    root = Element('widget', 'location_preview', children=[panel])
    popup = None
    if menu:
        spec = wonder_menu_spec(resources)
        popup = expander.build(spec.key, spec.value, {}, spec.src, spec.line)
        # Native positioning/input is not executed by the offline renderer.
        popup.props.update(position=[str(panel_width + 25), '24'], parentanchor='top|left',
                           widgetanchor='top|left')
        root.children.append(popup)
    return root, panel, popup


def render(state, resources, *, width=1420, height=1080, scale=1, menu=True, selected_slot=1,
           extra_mocks=None, output=None):
    from eu5_gui_renderer.gui import Expander
    from eu5_gui_renderer.paths import OUTPUT, MOD
    from eu5_gui_renderer.preview import render_tree
    expander = Expander(resources.db)
    if STATES[state] and not 1 <= selected_slot <= min(5, len(STATES[state])):
        raise ValueError('selected_slot must refer to a displayed wonder')
    root, panel, popup = build(resources, expander, 560, height, menu=menu and bool(STATES[state]))
    details = {'panel': panel}
    if popup is not None:
        details['menu'] = popup
    return render_tree(root, expander, resources, (extra_mocks or []) + scenario_mocks(state, resources, selected_slot),
        width=width, height=height, scale=scale, output=output or OUTPUT / f'location_{state}.png',
        detail_elements=details, metadata={'scenario': 'location', 'state': state, 'sample_data': True,
            'menu_open': popup is not None, 'selected_slot': selected_slot,
            'gui': str(MOD / GUI_PATH), 'wonders': STATES[state],
            'sample_tables': 'Modifier values from current selected mod static definitions; site checks are explicit sample results.',
            'unsupported': ['No save, script execution, native popup placement, clicks, scrolling, 3D map, portraits or procedural flags.',
                            'Queues and secondary lists are empty sample data; infrastructure tab is selected.']})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--state', choices=STATES, default='multiple')
    selection.add_argument('--all', action='store_true')
    parser.add_argument('--closed', action='store_true')
    parser.add_argument('--selected-slot', type=int, default=1)
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('--workspace', type=Path, default=WORKSPACE)
    parser.add_argument('--renderer-root', type=Path)
    parser.add_argument('--mod-root', type=Path, default=Path('src'))
    parser.add_argument('--game-root', type=Path)
    parser.add_argument('--output-root', type=Path, default=Path('ai_gui_assessment/images/location'))
    parser.add_argument('--mocks', type=Path)
    parser.add_argument('--language', default='simp_chinese')
    parser.add_argument('--width', type=int, default=1420)
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
                            menu=not args.closed, selected_slot=args.selected_slot, extra_mocks=extra)
            reports.append(report)
            print(f"Rendered {report['output']}; unknown={len(report['unknown_expressions'])}, contexts={len(report['unresolved_contexts'])}, missing_textures={len(report['missing_textures'])}", flush=True)
        write_report(OUTPUT / 'location_index.json', reports)
        return int(args.strict and any(has_diagnostics(r) for r in reports))
    except (ValueError, OSError, re.error) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    raise SystemExit(main())
