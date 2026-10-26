# Wonders / Engineering Department Risk Card

Load this top-level card before editing files whose names contain `wonder` or
`engineering_department`. Use the narrower routed cards when the touched object
or file type matches them.

## Current Architecture

- The Engineering Department / Wonder Construction subsystem is a standalone mod
  root at `src/`, with domain generators in `scripts_engineering_department/`.
  It depends on CMF 2.x and Construction Manager, not on the Towards Victory mod.
  The location panel imports Glorp UI 1.4 beta; its CM upgrade callbacks,
  auto-expand icon and town-rights map mode come from the declared CM dependency.
  Its Glorp CM activity detector is generated with the panel and registered separately.
- The main Towards Victory mod depends on Engineering Department because
  Prosperity Victory calls `tv_engineering_department_create_effect`.
- Wonder data remains in repo-root `data/`; generated source is emitted under
  `src/`.
- `character_title.txt` remains a generated full vanilla copy per deployable root.
  EU5 1.4.3 message types use additive `main_menu/gui/messagetypes/<root>.txt` files
  containing only that root's actions; never copy vanilla types or ED types into the main root.

## Always-Apply Rules

1. Keep local and national effects separate.
   Final/helper building `modifier` and `raw_modifier` entries are local. National
   or global wonder effects must be applied through country modifiers or
   generated country-auto paths, not through noncapital building modifiers.

2. Treat generated outputs as read-only.
   Check `data/generated_files.yaml` first. If a wonder source file is generated,
   edit the listed data file or generator and rerun the generator.

3. Keep the standalone root standalone.
   Engineering Department files must not rely on keys, trigger localization, message
   types, or helper definitions that exist only in the Towards Victory root unless the
   dependency is explicit and guaranteed.

4. Keep CMF integration centralized.
   Missing-Great-Engineer alerts, Wonder Control CMM registration, callbacks, GUI
   bridges, and action-log calls belong to the Engineering Department root. Do not
   move them back into the main mod.

5. Avoid read-path repair fallbacks.
   This project is unreleased. Fix lifecycle initialization and generator state
   directly; do not add old-schema rebuilds, `*_if_needed` routers, or compatibility
   probes to GUI, tooltip, selection, monthly read, or cache refresh paths.

6. Keep AI operations in the ED country driver.
   `tv_engineering_department_ai_*` callbacks use fixed rules and the same project
   effects/state as human countries. Do not enable native generic-action AI or
   copy selector flows into pulses. `monthly_balance` is last month's realized
   surplus; never replace it with gross income. Player CMM tuning does not apply
   to AI. The AI toggle stops scripted operations only. Paid confirmations must
   pay their action prices explicitly; construction uses the regular queue.

7. Preserve temporarily foreign priority sites.
   Ownership loss aborts an active project and applies the existing failure cost
   immediately; its event only notifies. Register surviving work before clearing
   project state. Temporarily foreign priority candidates stay in persistent maps
   but are omitted from selectable lists, then revalidated when owned again.

8. Change completed wonder levels only through the external interface.
   Features outside the Engineering Department project flow (vanilla wonder
   events, plunder, debug tools) must call `tv_wonder_raise/lower_generic_level_effect`
   or `tv_wonder_raise/lower_unique_level_effect`
   (`gen_tv_wonder_level_change_effects.py`). Do not write final-building levels
   directly: the interface owns the active-project redirect, suitability cap,
   no-reward rule, and the next-day `..._handle_final_building_level_changed_effect`
   resync. Contract: `docs/design/Wonder_Level_Change_Interface.md`.

## Routed Detail Cards

- `docs/knowledge/risk_cards/object_on_built.md`: any `on_built` hook.
- `docs/knowledge/risk_cards/wonder_buildings.md`: building types, prices,
  modifier types, auto modifiers, construction completion, labor/input reads.
- `docs/knowledge/risk_cards/wonder_gui.md`: location window, Engineering
  Department panel, Europedia cards, tooltip/layout/icon routing.
- `docs/knowledge/risk_cards/wonder_ceremony.md`: unified rituals, instance lifecycle,
  estate settlement, native effect previews and rededication.
- `docs/knowledge/risk_cards/wonder_unique_rituals.md`: unique flavor text and
  inheritance from the unified generic ritual mechanisms.

## Validation

Run the generated-file owner first, then:

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts\validate.py --changed --fix --ai-report
```

When changing scale-based wonder trigger/effect/building generators, also run:

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts_engineering_department\test_wonder_mechanics_rules.py
```
