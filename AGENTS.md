# Repository instructions for coding agents

Read `CLAUDE.md` as the main workflow entry, then the shared and workspace briefs.
Before non-trivial edits, run the direct EU5 interpreter with
`scripts/ai_context.py --files <target paths>`; use `--changed` to cover current edits.
Read every required card and every `required` alert in the default output.

When adding, renaming, moving, or generating a generic action, complete all three
registrations in the action's own mod root:

1. Put its id inside an AI list's `actions = { ... }` block.
2. Register `PERFORM_<action_id>_ACTION` in `main_menu/gui/messagetypes/<mod>.txt`.
3. Provide all five localized keys: `HEADER`, `TITLE`, `SETUP`, `LOG`, and `MAP`.
   Keep UTF-8 BOM and ensure every `$alias$` resolves. Three fields are incomplete.

This also applies when editing Python generators, source YAML, GUI action callers,
AI lists, or message/localization generators. Use the owner in
`data/generated_files.yaml`; update inputs, regenerate outputs, and run
`scripts/validate.py --changed --fix --ai-report` before handoff. A passing check
must cover the new action and all five fields; suppressing these diagnostics is
not a fix. See `docs/knowledge/risk_cards/generic_actions.md` for the worked example.
