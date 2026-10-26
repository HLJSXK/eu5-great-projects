"""Offline mockup listing every priority (unfinished / expansion) candidate.

The adopted layout (scheme A) is a GUI fragment under mockups/priority_proposal/.
The real Engineering Department panel is expanded first; the fragment then
replaces the proposal card, slot buttons and action row in the overview bottom
vbox, keeping the real proposal preview below it. The
scenario uses invented candidates and draft localization; no game script runs.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engineering  # noqa: E402

MOCKUP_DIR = Path(__file__).resolve().parent / "mockups" / "priority_proposal"
PLAYER = "InternationalOrganizationsView.GetPlayer.MakeScope"

# id, location key, location name, mode, built modules, level, cap
CANDIDATES = [
    (3, "rijeka", "里耶卡", 1, (1, 2), 0, 0),
    (15, "zagreb", "萨格勒布", 1, (1,), 0, 0),
    (18, "buda", "布达", 2, (), 2, 4),
    (10, "pecs", "佩奇", 2, (), 1, 3),
    (7, "kremnica", "克雷姆尼察", 2, (), 3, 5),
]
SELECTED = "rijeka"

SCHEMES = {
    # name: (fragment, keep the real proposal preview below, height)
    "baseline": (None, True, 1180),
    "a": ("scheme_a_grouped_list.gui", True, 1420),
}


def candidate_item(wonder_id, key, name, mode, modules, level, cap) -> dict:
    var = "GetLocation.MakeScope.GetVariable('{}')"
    item = {"__type__": "Scope", "GetLocation": key, "GetLocation.Self": key,
            "GetLocation.GetName": name, "GetLocation.GetNameWithNoTooltip": name}
    values = {"tv_wonder_priority_display_id": wonder_id, "tv_wonder_priority_display_mode": mode,
              "tv_wonder_priority_display_level": level if mode == 2 else None,
              "tv_wonder_priority_display_cap": cap if mode == 2 else None}
    for index in range(1, 5):
        values[f"tv_wonder_priority_display_module_{index}"] = 1 if index in modules else None
    for variable, value in values.items():
        item[var.format(variable) + ".IsSet"] = value is not None
        item[var.format(variable) + ".GetValue"] = 0 if value is None else value
    return item


def scenario():
    state = engineering.scenario_state("proposal")
    selected = next(c for c in CANDIDATES if c[1] == SELECTED)
    state.player_variables.update(
        tv_wonder_proposal=selected[0], tv_wonder_proposal_mode=selected[3],
        tv_wonder_proposal_site=1, tv_wonder_priority_found=1,
        tv_wonder_proposal_slot_1=None, tv_wonder_proposal_slot_2=None, tv_wonder_proposal_slot_3=None)
    return state, selected


def extra_mocks(selected) -> list:
    items = [candidate_item(*c) for c in CANDIDATES]
    lists = {
        "tv_wonder_priority_unfinished_list": [i for i, c in zip(items, CANDIDATES) if c[3] == 1],
        "tv_wonder_priority_expansion_list": [i for i, c in zip(items, CANDIDATES) if c[3] == 2],
    }
    result = [(re.escape(f"{PLAYER}.GetList('{name}')"), value) for name, value in lists.items()]
    site = f"{PLAYER}.GetVariable('tv_wonder_proposal_site').GetLocation"
    result += [
        (re.escape(site + ".Self"), selected[1]),
        (re.escape(site + ".GetName"), selected[2]),
    ]
    return result


def walk(element):
    yield element
    for child in element.children:
        yield from walk(child)


def splice(root, db, expander, fragment: Path | None, keep_preview: bool):
    from eu5_gui_renderer.pdx import parse
    if fragment is None:
        return
    def contains_text(element, key):
        return any(child.props.get("text") == key for child in walk(element))

    # Locate ED content by its labels rather than a previous visible expression
    # or child offset; the live panel also contains its own priority list now.
    target, start, end = next(
        (element, start, end)
        for element in walk(root) if element.kind == "vbox"
        for start, child in enumerate(element.children)
        if child.kind == "hbox" and contains_text(child, "TV_ENGINEERING_PROPOSAL_NEEDS_ENGINEER_TEXT")
        for end in range(start + 1, len(element.children))
        if contains_text(element.children[end], "TV_ENGINEERING_WONDER_PREVIEW_EFFECT_TITLE"))
    preview = target.children[end]
    del target.children[start:end + 1]
    nodes = parse(fragment.read_text(encoding="utf-8-sig"), str(fragment), dict(db.consts))
    built = [expander.build(n.key, n.value, {}, str(fragment), n.line) for n in nodes if n.is_block()]
    if keep_preview:
        built.append(preview)
    target.children[start:start] = built


def render(name: str, width: int = 570, scale: float = 1) -> dict:
    from eu5_gui_renderer.data import Loc
    from eu5_gui_renderer.gui import Expander
    from eu5_gui_renderer.paths import OUTPUT
    from eu5_gui_renderer.preview import load_resources, render_tree
    fragment_name, keep_preview, height = SCHEMES[name]
    state, selected = scenario()
    resources = load_resources()
    expander = Expander(resources.db)
    root = engineering.build(resources.db, expander, width, height, state)
    splice(root, resources.db, expander, MOCKUP_DIR / fragment_name if fragment_name else None, keep_preview)
    for line in (MOCKUP_DIR / "draft_loc_simp_chinese.yml").read_text(encoding="utf-8-sig").splitlines():
        match = Loc.LINE_RE.match(line)
        if match:
            resources.loc.d[match.group(1)] = match.group(2)
    return render_tree(root, expander, resources, extra_mocks(selected) + engineering.mocks(state, resources.loc),
        width=width, height=height, scale=scale, output=OUTPUT / "priority_proposal" / f"priority_{name}.png",
        metadata={"scheme": name, "fragment": fragment_name, "sample_data": True,
                  "candidates": CANDIDATES, "selected": SELECTED})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schemes", nargs="*", help=f"subset of {list(SCHEMES)}; default all")
    parser.add_argument("--scale", type=float, default=1)
    args = parser.parse_args(argv)
    unknown = set(args.schemes) - set(SCHEMES)
    if unknown:
        parser.error(f"unknown scheme(s): {sorted(unknown)}")
    engineering.configure()
    for name in args.schemes or list(SCHEMES):
        report = render(name, scale=args.scale)
        print(f"{name}: {report['output']} unknown={len(report['unknown_expressions'])} "
              f"unresolved={len(report['unresolved_contexts'])} missing={len(report['missing_textures'])}")
        for expression in report["unknown_expressions"]:
            print("   ?", expression[:160])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
