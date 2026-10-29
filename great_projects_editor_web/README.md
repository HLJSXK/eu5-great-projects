# Great Projects editor

Run `python -m great_projects_editor_web --check` for offline checks, or
`python -m great_projects_editor_web --no-browser` to serve the local editor.
Install `great_projects_editor_web/requirements.txt` with the direct EU5 interpreter.

All resource writes, generation, media jobs and operation logs are local to this
repository. Existing preview/commit, transaction, cancellation and rollback
contracts remain in force. The generated-file registry is authoritative.

Tools: wonder mechanics/localization, image cropper, media generation, cost/reward,
localization and registered generators. Default port: 8763.

The Base Effects group edits persistent per-level country modifiers and a separate
instant-effect list. Both are stored in `data/wonder_base_modifiers.yaml`:
`base_modifiers` retains its mapping; `base_instant_effects` is a sparse mapping
from generic prototype keys to lists of `{type, value}` entries. Types use the
existing ritual one-shot vocabulary; values must be finite numbers. Unique
wonders inherit both packages with their base-effect multiplier and are read-only.
All shipped instant-effect lists are currently empty.

Instant effects pay on project finalization: new construction pays its completed
level, expansion pays `level - project_base_level`. Plain inauguration also pays;
rededication, initial buildings, ownership/load refreshes and direct external
level changes do not. The existing finalization claim guard prevents a second
claim. Generated native option effects serve as both preview and payout; the
atlas displays the same scaled package per newly completed level. Removing a
list row changes future payouts only; it cannot undo a previous instant effect.

Run `node tests/wonder_base_effects_browser.cjs` for offline visual acceptance.
It uses headless local Chrome, leaves source data unchanged, and saves editor
screenshots plus bilingual atlas effect-section fixtures at 1440/900px to
`tmp/base-effects-preview/`. Atlas fixtures use the production renderer/CSS
without the unrelated CDN map; fixture rewards are never added to authored data.

Use scripts/run_editor_tests.py for the local test selection. The pre-extraction
manual is preserved in docs/archive/pre_split_editor/Editor_Web_Pre_Split_Reference.md; it is
historical evidence, not the current list of tools or repository paths.
