"""Offline mockups for the ED ritual rework (docs/design/Wonder_Ritual_Rework_Implementation_Plan.md).

The real Engineering Department panel is expanded in its ceremony state; every child of
the ceremony card's bottom vbox is replaced by one design fragment from
mockups/ritual_rework/. Sample data (great_port at Rijeka, invented societal-value
directions and estate preferences) and draft localization are mock-only; no game script runs.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engineering  # noqa: E402

MOCKUP_DIR = Path(__file__).resolve().parent / "mockups" / "ritual_rework"
PLAYER = "InternationalOrganizationsView.GetPlayer.MakeScope"

# name: (fragment, height)
SCHEMES = {
    "a_select": ("scheme_a_triptych.gui", 1800),
    "a_progress": ("scheme_a_triptych_progress.gui", 1800),
    "b_select": ("scheme_b_ledger.gui", 1900),
    "b_progress": ("scheme_b_ledger_progress.gui", 1900),
    "c_select": ("scheme_c_compass.gui", 1900),
    "c_progress": ("scheme_c_compass_progress.gui", 1900),
}


def walk(element):
    yield element
    for child in element.children:
        yield from walk(child)


def splice(root, db, expander, fragment: Path):
    from eu5_gui_renderer.pdx import parse
    target = next(
        element for element in walk(root) if element.kind == "vbox"
        and any(child.props.get("text") == "TV_ENGINEERING_CEREMONY_CHOOSE_STYLE_PROMPT" for child in element.children))
    nodes = parse(fragment.read_text(encoding="utf-8-sig"), str(fragment), dict(db.consts))
    target.children[:] = [expander.build(n.key, n.value, {}, str(fragment), n.line) for n in nodes if n.is_block()]


def effect_mocks(loc) -> list:
    """Stand-in engine output for the effect previews.

    The fragments render effects only through ShowScriptedEffectForScope on the real
    completion effects (tv_wonder_ritual_apply_choice_effect for the selected style,
    tv_wonder_ritual_apply_style_<n>_effect per style). The renderer cannot run script,
    so each call returns the matching RR_SAMPLE_ENGINE_FX_<n> sample text. Sample
    state: style 1 is the current choice.
    """
    import re
    def call(effect: str) -> str:
        return re.escape(f"ShowScriptedEffectForScope('{effect}',{PLAYER}.Self)")
    result = [(call("tv_wonder_ritual_apply_choice_effect"), loc.get("RR_SAMPLE_ENGINE_FX_1"))]
    result.extend((call(f"tv_wonder_ritual_apply_style_{n}_effect"), loc.get(f"RR_SAMPLE_ENGINE_FX_{n}"))
                  for n in (1, 2, 3))
    assert all(text for _, text in result), "RR_SAMPLE_ENGINE_FX_* missing from draft localization"
    return result


def render(name: str, width: int = 570, scale: float = 1) -> dict:
    from eu5_gui_renderer.data import Loc
    from eu5_gui_renderer.gui import Expander
    from eu5_gui_renderer.paths import OUTPUT
    from eu5_gui_renderer.preview import load_resources, render_tree
    fragment_name, height = SCHEMES[name]
    state = engineering.scenario_state("ceremony-ready")
    resources = load_resources()
    expander = Expander(resources.db)
    root = engineering.build(resources.db, expander, width, height, state)
    splice(root, resources.db, expander, MOCKUP_DIR / fragment_name)
    for line in (MOCKUP_DIR / "draft_loc_simp_chinese.yml").read_text(encoding="utf-8-sig").splitlines():
        match = Loc.LINE_RE.match(line)
        if match:
            resources.loc.d[match.group(1)] = match.group(2).replace('\\"', '"').replace("\\n", "\n")
    return render_tree(root, expander, resources, effect_mocks(resources.loc) + engineering.mocks(state, resources.loc),
        width=width, height=height, scale=scale, output=OUTPUT / "ritual_rework" / f"ritual_{name}.png",
        metadata={"scheme": name, "fragment": fragment_name, "sample_data": True,
                  "sample_effect_text": "ShowScriptedEffectForScope output is RR_SAMPLE_ENGINE_FX_* stand-in text, not script execution."})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schemes", nargs="*", help=f"subset of {list(SCHEMES)}; default all")
    parser.add_argument("--scale", type=float, default=1)
    parser.add_argument("--renderer-root", default=None)
    parser.add_argument("--game-root", default=None)
    parser.add_argument("--output-root", default=None)
    args = parser.parse_args(argv)
    unknown = set(args.schemes) - set(SCHEMES)
    if unknown:
        parser.error(f"unknown scheme(s): {sorted(unknown)}")
    configure_args = {key: Path(value) for key, value in {
        "renderer_root": args.renderer_root, "game_root": args.game_root,
        "output_root": args.output_root}.items() if value}
    engineering.configure(**configure_args)
    for name in args.schemes or list(SCHEMES):
        report = render(name, scale=args.scale)
        print(f"{name}: {report['output']} unknown={len(report['unknown_expressions'])} "
              f"unresolved={len(report['unresolved_contexts'])} missing={len(report['missing_textures'])} "
              f"loc={len(report.get('missing_localizations', []))}")
        for key in ("unknown_expressions", "missing_textures", "missing_localizations"):
            for item in report.get(key, [])[:20]:
                print("   ?", key, str(item)[:160])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
