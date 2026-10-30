# Europedia Risk Card

Read before changing Europedia layout, catalogue generation or display localization.

## Approved scope — 2026-10-30

The user approved the compact static catalogue after reviewing offline designs.
Keep the five tabs in order: All, Getting Started, Complete Mechanics, Unique Projects,
Generic Projects. All remains empty; the default is Complete Mechanics. Getting Started
contains the Great Projects overview/cycle. Complete Mechanics retains the other 14
teaching cards and the Triumphal Axis / Topkapi Palace worked examples. The two examples
now reuse the static compact entry. Unique and Generic contain one entry per concrete
wonder in the current data (139 unique, 56 generic at approval).

This explicitly supersedes the earlier restriction to 17 total cards. Do not restore the
old long, repetitive catalogue or its live effect/trigger tables.

## Static rendering contract

- `europedia_catalogue.py` bakes names, metadata, modifier names, all six level totals,
  ritual names/effects, original-art paths/dimensions and location captions offline.
- No `ShowModifierEffect`, `ShowScriptedEffectForScope`, `ShowTriggerConditionsForScope`,
  dynamic `textcontext`, gameplay datamodel or state-dependent localization in these
  entries, including the two teaching examples. Source aliases are resolved at generation;
  unresolved aliases or bracketed expressions fail generation. GUI tab visibility remains
  a local `GetVariableSystem` toggle.
- The user reports load-time hangs from live rendering calls. Hardcoding removes those
  calls; static checks do not establish native load performance or prove the old root cause.
- Do not display construction conditions. Unique entries alone have a location icon and
  fixed caption under the image. `SelectLocation(GetLocationByKey('<fixed id>').Self)` runs
  only on click. Generic entries do not create a location row. Offline preview cannot
  establish native click/hit-test behavior.
  The user's 2026-10-30 19:58:28 log rejects the former bare
  `SelectLocation(GetLocationByKey(...))` argument during GUI loading.
  `GetLocationByKey` is only a Global promote (official API line 733), whereas
  `Location.Self` is a value Function (line 93782). Vanilla's
  `SelectLocation(Siege.GetLocation)` works with a separate Function overload of
  that getter; it does not establish bare-promote argument support. Preserve the
  static caption and click-only lookup, and end the argument chain with `.Self`.
  `tests/test_europedia_catalogue.py` checks the API distinction and every generated
  consumer; native callback acceptance still requires a fresh game load.
- Identity variants use the authored default identity's static text and art. Do not read
  `hagia_sophia_now_mosque` while loading this reference catalogue.
- The accepted shape is 1450 wide and normally 300 high: full original art within 240×160,
  full-width I–VI effect table to its right, three ritual panels below the table. Longer
  English labels/titles and larger effect packages increase the entry height. Preserve
  every effect; never silently crop rows or make boolean/raw modifiers stack per level.
- `level_rows()` matches the shipped display-modifier rules, including per-level building
  serialization precision and unscaled raw modifiers. This catalogue is a static reference;
  conditional current-country availability is not evaluated.
- EN/ZH are authored/generated source texts; complete all 11 language key sets with BOM.
  Regenerate the English fallback files after catalogue changes. Numeric effect snapshots
  must be regenerated when gameplay data changes, including through the web editor plan.

## GUI ownership and engine contracts

EU5 has no verified data-driven registration API for an arbitrary Europedia page.
`encyclopedia_lateralview.gui` is a full-file override. The custom view uses
`tv_encyclopedia_active`; vanilla navigation clears it. Filters use
`tv_encyclopedia_filter`; only Complete Mechanics accepts an unset filter.
`Or` / `And` take exactly two arguments; use the numbered variants for wider predicates.

Preserve expanding layout on the custom root, scrollbox and content root, with
`set_parent_dimension_to_minimum = height` on the content list. Filter buttons expand
horizontally. Catalogue groups use sized entry widgets so scroll height includes every row.
`tv_eu_catalogue_entry` and teaching styles live in `shared/tv_europedia_style.gui`.
Title format remains `#yellow_titles`. Text widths are bounded; literal texture paths
are generated rather than constructed with runtime `Concatenate`.

Update `europedia_content.py` / `europedia_render.py` / `europedia_catalogue.py`, then run
GUI fragment, EN/ZH localization and GUI merge generators. The generated-files registry
owns these outputs. Rebuild the Prosper or Perish compatibility override with
`scripts/compat/gen_tv_prosper_or_perish_encyclopedia_lateralview.py`; it retains the
shared `tveu_compat_encyclopedia_active` toggle and both mods' navigation.

## Validation

Run `tests/test_europedia_catalogue.py`, the encyclopedia checks in
`tests/test_wonder_ritual_rework.py`, generation-plan regressions, and
`scripts/validate.py --changed --fix --ai-report`. Run
`ai_gui_assessment/europedia.py --tab unique` and `--tab generic` for EN/ZH previews of
the actual shipped panel. These fixtures bind only window chrome and tab state, not
catalogue content. Check native fresh-game loading, scrolling and location navigation
separately; offline success does not prove them.

## Historical evidence

On 2026-10-28 the user reported new-game initialization hangs with the old 210-card
catalogue. Removing 402 dynamic tables and hiding all cards did not establish a fix;
a single complete example loaded. The user also rejected its repeated prose and long
scrolling. The earlier 15 teaching cards plus two examples was a deliberate interim
scope. The current all-wonder design was explicitly approved after compact static
prototypes; hiding widgets alone is still not evidence of deferred construction.
