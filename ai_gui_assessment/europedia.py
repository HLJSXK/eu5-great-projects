"""Render the actual shipped Europedia catalogue with only window/tab fixtures."""
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
    parser.add_argument('--tab',default='unique',choices=['unique','generic'])
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
    tab=next(n for n in nodes if n.get('name')=='tv_eu_catalogue_'+args.tab)
    entries=[n for n in walk(tab) if n.typename=='tv_eu_catalogue_entry']
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
    report=render_tree(tree,expander,resources,[(re.escape(k),v) for k,v in bindings.items()],
                       width=1920,height=1300,output=Path(args.tab+'.png'),
                       detail_elements={f'entry_{i+1}':node for i,node in enumerate(entries[:3])},
                       metadata={'source':'shipped GUI','tab':args.tab,'static_catalogue':True})
    if has_diagnostics(report):
        raise ValueError(json.dumps(report,ensure_ascii=False))
    # Layout every visible entry, including the ones below the viewport.
    for entry in entries:
        for node in walk(entry):
            if node.kind=='textbox' and node.w>0:
                assert node.x >= entry.x-.1 and node.x+node.w <= entry.x+entry.w+.1, node.props
                assert node.y >= entry.y-.1 and node.y+node.h <= entry.y+entry.h+.1, node.props
    print(f'{args.language}/{args.tab}: {len(entries)} entries; clean diagnostics and text bounds; {report["output"]}')


if __name__=='__main__':
    main()
