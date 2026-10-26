# AI tool workflow

Read CLAUDE.md, .eu5-base/CLAUDE.md and both knowledge briefs. Run the direct EU5
Python interpreter with scripts/ai_context.py --files <paths> (or --changed)
before edits. Read every required card and alert. Routes are owned by
`docs/knowledge/context_routes.yaml` and merged with shared-base routes.

Only this repository's registered source roots and generator outputs are owned
here. Follow data/generated_files.yaml, edit inputs and regenerate. Generic actions
require AI actions-list membership, an additive message type, and all five
HEADER/TITLE/SETUP/LOG/MAP localizations with BOM and resolving aliases.

Run scripts/validate.py --changed --fix --ai-report before handoff. Regenerate
scripts/gen_brief.py after knowledge changes. Shared engine rules belong in
.eu5-base; implementation rules belong here. Repository extraction evidence and
known validation limits are in docs/technical. Archived investigations stay archived.
