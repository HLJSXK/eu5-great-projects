"""Render the actual shipped Europedia with only window/tab fixtures."""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.eu5-base/ai_gui_assessment/renderer'))


def walk(node):
    yield node
    for child in node.children:
        yield from walk(child)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language',default='simp_chinese',choices=['simp_chinese','english'])
    parser.add_argument('--tab',default='unique',choices=['overview','unique','generic'])
    parser.add_argument('--height',type=int,default=1300)
    args=parser.parse_args()
    from eu5_gui_renderer.config import configure_paths
    configure_paths(workspace=ROOT,mod_root=Path('src'),language=args.language,
                    output_root=ROOT/'ai_gui_assessment/images/europedia'/args.language)
    from eu5_gui_renderer.gui import Expander,build_target
    from eu5_gui_renderer.preview import load_resources,render_tree,has_diagnostics
    resources=load_resources()
    expander=Expander(resources.db)
    tree=build_target(resources.db,expander,'encyclopedia_lateralview',None)
    nodes=list(walk(tree))
    tab_name='tv_eu_overview_cycle' if args.tab=='overview' else 'tv_eu_catalogue_'+args.tab
    tab=next(n for n in nodes if n.get('name')==tab_name)
    entry_type='tv_eu_cycle_step' if args.tab=='overview' else 'tv_eu_catalogue_entry'
    entries=[n for n in walk(tab) if n.typename==entry_type]
    guides=[n for n in nodes if re.fullmatch(r'tv_eu_overview_guide_\d+', n.get('name') or '')] if args.tab=='overview' else []
    guide_tiles=[n for guide in guides for n in walk(guide) if n.typename=='tv_eu_anatomy_row']
    page={'__type__':'EncyclopediaPage','Self':'all','GetTitle':'All'}
    bindings={
        "GetVariableSystem.HasValue('tv_encyclopedia_active','yes')":True,
        "GetVariableSystem.Exists('tv_encyclopedia_filter')":True,
        'Encyclopedia.AccessPages':[], 'Encyclopedia.AccessCurrentPage':page,
        'Encyclopedia.GetCurrentPage':page,'Encyclopedia.GetAllPage':page,
        'PdxGuiWidget.GetIndexInParent':0,
    }
    for category in ('all','overview','mechanics','unique','generic'):
        bindings[f"GetVariableSystem.HasValue('tv_encyclopedia_filter','{category}')"]=category==args.tab
    for texture in ('top_header_bg','pattern_bevel_vertical_bis'):
        bindings[f"GetGraphicalCultureTexture('{texture}')"]=f'gfx/interface/graphical_cultures/east_asian_gfx/{texture}.dds'
    if args.tab=='overview':
        # Exact native name helpers, sampled from the selected game's/mod's
        # localization. These do not simulate gameplay or replace guide text.
        for helper, keys in (
            ('ShowEstateTypeName', ('nobles_estate','burghers_estate','clergy_estate')),
            ('ShowBuildingTypeName', ('tv_wonder_labor_camp','tv_wonder_material_dispatch_point')),
            ('ShowGoodsName', ('tools','tv_wonder_materials')),
            ('ShowPopTypeName', ('laborers',)),
        ):
            for key in keys:
                name=resources.loc.get(key)
                if name is None:
                    raise ValueError(f'Missing native-link localization: {key}')
                bindings[f"{helper}('{key}')"]=f'#game_link {name}#!'
    report=render_tree(tree,expander,resources,[(re.escape(k),v) for k,v in bindings.items()],
                       width=1920,height=args.height,output=Path(args.tab+'.png'),
                       detail_elements=({'cycle':tab, **{f'guide_{i+1}':node for i,node in enumerate(guides)}} if args.tab=='overview' else
                                        {f'entry_{i+1}':node for i,node in enumerate(entries[:3])}),
                       metadata={'source':'shipped GUI','tab':args.tab,'static_catalogue':args.tab!='overview'})
    if has_diagnostics(report):
        raise ValueError(json.dumps(report,ensure_ascii=False))
    if args.tab=='overview':
        assert len(entries)==7 and len(guides)==7
    # Layout every visible entry, including the ones below the viewport.
    for entry in entries:
        for node in walk(entry):
            if node.kind=='textbox' and node.w>0:
                assert node.x >= entry.x-.1 and node.x+node.w <= entry.x+entry.w+.1, (entry.x, entry.w, node.x, node.w, node.props)
                assert node.y >= entry.y-.1 and node.y+node.h <= entry.y+entry.h+.1, node.props
    print(f'{args.language}/{args.tab}: {len(entries)} entries; clean diagnostics and text bounds; {report["output"]}')


if __name__=='__main__':
    main()
