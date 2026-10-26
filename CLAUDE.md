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
Run scripts/validate.py --changed --fix --ai-report and relevant tests before handoff.
Regenerate the knowledge brief with scripts/gen_brief.py after knowledge changes.
Read docs/technical/Repository_Split.md for extraction evidence and audit guidance.
The archived gameplay/refactor investigations remain archived.
