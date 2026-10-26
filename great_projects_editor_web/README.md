# Great Projects editor

Run `python -m great_projects_editor_web --check` for offline checks, or
`python -m great_projects_editor_web --no-browser` to serve the local editor.
Install `great_projects_editor_web/requirements.txt` with the direct EU5 interpreter.

All resource writes, generation, media jobs and operation logs are local to this
repository. Existing preview/commit, transaction, cancellation and rollback
contracts remain in force. The generated-file registry is authoritative.

Tools: wonder mechanics/localization, image cropper, media generation, cost/reward,
localization and registered generators. Default port: 8763.

Use scripts/run_editor_tests.py for the local test selection. The pre-extraction
manual is preserved in docs/archive/pre_split_editor/Editor_Web_Pre_Split_Reference.md; it is
historical evidence, not the current list of tools or repository paths.
