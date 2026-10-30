# Great Projects agent workflow

Read `.eu5-base/CLAUDE.md`, `.eu5-base/docs/knowledge/BRIEF.md`, and
`docs/knowledge/BRIEF.md`. If the base link is absent, run scripts/bootstrap_base.py.
Use the direct EU5 Python interpreter in managed sandboxes, never conda run.
Before non-trivial edits run scripts/ai_context.py --files <paths> or --changed;
read every required card and alert. Check data/generated_files.yaml for ownership.

`src/` is Great Projects; `scripts_engineering_department/` owns domain generators.
`scripts/` owns workspace tools and integration generators. `great_projects_editor_web/`
is the independent editor (port 8763). Compatibility submods and the atlas live here.
No command may read or write another mod checkout. Shared references and engine
knowledge come only from eu5-modding-base. TV runtime consumers keep existing IDs.

Generic actions must have AI-list actions membership, a root-owned PERFORM message
type, and all five HEADER/TITLE/SETUP/LOG/MAP keys with BOM and resolving aliases.
Every localization key must exist in all 11 languages in each mod root; language
key sets must match in both directions. English and Simplified Chinese are the
maintained source texts; other languages normally use machine translation or
English fallback. Missing translations never justify missing keys.
Run scripts/validate.py --changed --fix --ai-report and relevant tests before handoff.
Register every localization entry in data/localization_grades.json with its actual
grade: 原创 > AI生成 > 翻译 > 占位 > 缺失. Agents may use 原创 only for user-manual
content or an explicit user request to register it as original; record that evidence.
Read docs/knowledge/risk_cards/localization.md and use scripts/localization_grades.py
after regenerating changed text. --fix must never infer provenance.
Regenerate the knowledge brief with scripts/gen_brief.py after knowledge changes.
Read docs/archive/repository_split/Repository_Split.md for extraction evidence and audit guidance.
The archived gameplay/refactor investigations remain archived.
