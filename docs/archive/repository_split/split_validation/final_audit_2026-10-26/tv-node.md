```text
TAP version 13
# Subtest: 409 resource_busy includes server diagnostics in the shared guidance
ok 1 - 409 resource_busy includes server diagnostics in the shared guidance
  ---
  duration_ms: 101.2612
  type: 'test'
  ...
# Subtest: 409 resource_changed includes server diagnostics in the shared guidance
ok 2 - 409 resource_changed includes server diagnostics in the shared guidance
  ---
  duration_ms: 0.9776
  type: 'test'
  ...
# Subtest: 500 retains generation on the error
ok 3 - 500 retains generation on the error
  ---
  duration_ms: 1.2029
  type: 'test'
  ...
# Subtest: 500 retains log_text on the error
ok 4 - 500 retains log_text on the error
  ---
  duration_ms: 0.8775
  type: 'test'
  ...
# Subtest: non-JSON error bodies are consumed once and retain the original text
ok 5 - non-JSON error bodies are consumed once and retain the original text
  ---
  duration_ms: 2.3012
  type: 'test'
  ...
# Subtest: a successful response returns JSON and forwards request options unchanged
ok 6 - a successful response returns JSON and forwards request options unchanged
  ---
  duration_ms: 2.2197
  type: 'test'
  ...
# Subtest: an unrecognized 409 keeps its diagnostic instead of reporting a stale resource
ok 7 - an unrecognized 409 keeps its diagnostic instead of reporting a stale resource
  ---
  duration_ms: 1.462
  type: 'test'
  ...
# Subtest: structured validation details remain inspectable and produce a readable message
ok 8 - structured validation details remain inspectable and produce a readable message
  ---
  duration_ms: 2.6721
  type: 'test'
  ...
# Subtest: empty detail falls back to the raw response and custom messages keep diagnostics
ok 9 - empty detail falls back to the raw response and custom messages keep diagnostics
  ---
  duration_ms: 3.2751
  type: 'test'
  ...
# Subtest: filters cost/reward rows by id and bilingual loc text
ok 10 - filters cost/reward rows by id and bilingual loc text
  ---
  duration_ms: 6.3156
  type: 'test'
  ...
# Subtest: dirty row collection ignores empty field maps and supports only-dirty filtering
ok 11 - dirty row collection ignores empty field maps and supports only-dirty filtering
  ---
  duration_ms: 0.8373
  type: 'test'
  ...
# Subtest: filter and only-dirty conditions compose without changing token order
ok 12 - filter and only-dirty conditions compose without changing token order
  ---
  duration_ms: 1.4013
  type: 'test'
  ...
# Subtest: value notes stay within the comments-backed category meanings
ok 13 - value notes stay within the comments-backed category meanings
  ---
  duration_ms: 0.4504
  type: 'test'
  ...
# Subtest: catalogue renders one section per root/domain in catalogue order, with counts and rows
ok 14 - catalogue renders one section per root/domain in catalogue order, with counts and rows
  ---
  duration_ms: 96.1184
  type: 'test'
  ...
# Subtest: run stays disabled until a script is selected; group toggle and order follow the click order
ok 15 - run stays disabled until a script is selected; group toggle and order follow the click order
  ---
  duration_ms: 2.4917
  type: 'test'
  ...
# Subtest: a run sends the selected scripts in order and renders steps and artifacts through the shared renderer
ok 16 - a run sends the selected scripts in order and renders steps and artifacts through the shared renderer
  ---
  duration_ms: 4.0365
  type: 'test'
  ...
# Subtest: dry_run reports skipped steps, no artifacts and says nothing was executed or written
ok 17 - dry_run reports skipped steps, no artifacts and says nothing was executed or written
  ---
  duration_ms: 0.9067
  type: 'test'
  ...
# Subtest: a timed-out step renders through the shared report instead of a raw identifier
ok 18 - a timed-out step renders through the shared report instead of a raw identifier
  ---
  duration_ms: 0.8771
  type: 'test'
  ...
# Subtest: a failed run reports the server detail as an error and releases the panel
ok 19 - a failed run reports the server detail as an error and releases the panel
  ---
  duration_ms: 0.6886
  type: 'test'
  ...
# Subtest: rows and actions are locked while a run is in flight
ok 20 - rows and actions are locked while a run is in flight
  ---
  duration_ms: 0.8022
  type: 'test'
  ...
# Subtest: the page entry loads the catalogue once, only when the generators tab is activated
ok 21 - the page entry loads the catalogue once, only when the generators tab is activated
  ---
  duration_ms: 57.8655
  type: 'test'
  ...
# Subtest: importing the shell activates the first tab and dispatches tool-activated once
ok 22 - importing the shell activates the first tab and dispatches tool-activated once
  ---
  duration_ms: 22.4959
  type: 'test'
  ...
# Subtest: the dirty registry adds and removes entries and only notifies on a real change
ok 23 - the dirty registry adds and removes entries and only notifies on a real change
  ---
  duration_ms: 3.4351
  type: 'test'
  ...
# Subtest: a dirty tool paints its tab dot and an active job shows the running marker
ok 24 - a dirty tool paints its tab dot and an active job shows the running marker
  ---
  duration_ms: 1.9687
  type: 'test'
  ...
# Subtest: beforeunload is only blocked while some tool is dirty
ok 25 - beforeunload is only blocked while some tool is dirty
  ---
  duration_ms: 1.7992
  type: 'test'
  ...
# Subtest: ResourceState reports only real dirty transitions through onDirtyChange
ok 26 - ResourceState reports only real dirty transitions through onDirtyChange
  ---
  duration_ms: 1.1699
  type: 'test'
  ...
# Subtest: operation groups split running, failed and finished without repeating a row
ok 27 - operation groups split running, failed and finished without repeating a row
  ---
  duration_ms: 42.9249
  type: 'test'
  ...
# Subtest: a multi-resource operation marks every tab that owns one of its resources
ok 28 - a multi-resource operation marks every tab that owns one of its resources
  ---
  duration_ms: 0.5615
  type: 'test'
  ...
# Subtest: the operations list renders loaded, empty and failed states and escapes payloads
ok 29 - the operations list renders loaded, empty and failed states and escapes payloads
  ---
  duration_ms: 2.4014
  type: 'test'
  ...
# Subtest: a poll refresh keeps an expanded row open and the next first click still expands
ok 30 - a poll refresh keeps an expanded row open and the next first click still expands
  ---
  duration_ms: 11.7516
  type: 'test'
  ...
# Subtest: the page entry loads only when the localization tab is activated, and only once
ok 31 - the page entry loads only when the localization tab is activated, and only once
  ---
  duration_ms: 74.8502
  type: 'test'
  ...
# Subtest: files are indexed into one group per logical file, with generated pairs read-only
ok 32 - files are indexed into one group per logical file, with generated pairs read-only
  ---
  duration_ms: 1.03
  type: 'test'
  ...
# Subtest: read-only comes from either file of the pair, so the other language cannot bypass it
ok 33 - read-only comes from either file of the pair, so the other language cannot bypass it
  ---
  duration_ms: 0.4766
  type: 'test'
  ...
# Subtest: missing translations are counted in both directions and the summary matches the pairs
ok 34 - missing translations are counted in both directions and the summary matches the pairs
  ---
  duration_ms: 0.6192
  type: 'test'
  ...
# Subtest: filters split by missing and edited, and search matches key or either language
ok 35 - filters split by missing and edited, and search matches key or either language
  ---
  duration_ms: 1.0192
  type: 'test'
  ...
# Subtest: a new key must carry both languages, and only real changes reach the request
ok 36 - a new key must carry both languages, and only real changes reach the request
  ---
  duration_ms: 0.9474
  type: 'test'
  ...
# Subtest: the panel loads the resource, renders both columns and reports the missing counts
ok 37 - the panel loads the resource, renders both columns and reports the missing counts
  ---
  duration_ms: 3.4844
  type: 'test'
  ...
# Subtest: \#G content\#! renders as a colored span, and \#Gfoo\#! degrades instead of absorbing its content
ok 38 - \#G content\#! renders as a colored span, and \#Gfoo\#! degrades instead of absorbing its content
  ---
  duration_ms: 5.2135
  type: 'test'
  ...
# Subtest: $X$ renders as a variable placeholder and is never expanded
ok 39 - $X$ renders as a variable placeholder and is never expanded
  ---
  duration_ms: 0.5623
  type: 'test'
  ...
# Subtest: [trust|e] renders as a localization function call and its argument is kept
ok 40 - [trust|e] renders as a localization function call and its argument is kept
  ---
  duration_ms: 0.4086
  type: 'test'
  ...
# Subtest: \\n becomes a line break and a physical newline does too
ok 41 - \\n becomes a line break and a physical newline does too
  ---
  duration_ms: 0.2633
  type: 'test'
  ...
# Subtest: unclosed markup degrades: the marker is reported and nothing crashes
ok 42 - unclosed markup degrades: the marker is reported and nothing crashes
  ---
  duration_ms: 0.4954
  type: 'test'
  ...
# Subtest: unsupported markup is labeled, not faked: @icon! and unknown tags
ok 43 - unsupported markup is labeled, not faked: @icon! and unknown tags
  ---
  duration_ms: 0.2365
  type: 'test'
  ...
# Subtest: nested tags keep their order and every text run is escaped
ok 44 - nested tags keep their order and every text run is escaped
  ---
  duration_ms: 0.6341
  type: 'test'
  ...
# Subtest: plain text drops supported markup and keeps line breaks
ok 45 - plain text drops supported markup and keeps line breaks
  ---
  duration_ms: 0.2555
  type: 'test'
  ...
# Subtest: an interrupted publication warns about formal outputs and retained backups
ok 46 - an interrupted publication warns about formal outputs and retained backups
  ---
  duration_ms: 72.5331
  type: 'test'
  ...
# Subtest: a job interrupted before it started does not warn about partial publication
ok 47 - a job interrupted before it started does not warn about partial publication
  ---
  duration_ms: 1.0931
  type: 'test'
  ...
# Subtest: discarded intermediate files are separate from formal output conflicts
ok 48 - discarded intermediate files are separate from formal output conflicts
  ---
  duration_ms: 1.158
  type: 'test'
  ...
# Subtest: a late poll after cancellation cannot append duplicate lines
ok 49 - a late poll after cancellation cannot append duplicate lines
  ---
  duration_ms: 36.7986
  type: 'test'
  ...
# Subtest: a late response from an earlier job cannot change the current job
ok 50 - a late response from an earlier job cannot change the current job
  ---
  duration_ms: 1.8489
  type: 'test'
  ...
# Subtest: transient polling failure retains the cursor and logs, then resumes
ok 51 - transient polling failure retains the cursor and logs, then resumes
  ---
  duration_ms: 1.9733
  type: 'test'
  ...
# Subtest: a nontransient polling failure allows stopping without losing the job or accepting late responses
ok 52 - a nontransient polling failure allows stopping without losing the job or accepting late responses
  ---
  duration_ms: 2.0644
  type: 'test'
  ...
# Subtest: 404 stops tracking and unlocks the form while preserving diagnostics
ok 53 - 404 stops tracking and unlocks the form while preserving diagnostics
  ---
  duration_ms: 1.5285
  type: 'test'
  ...
# Subtest: 410 stops tracking and unlocks the form while preserving diagnostics
ok 54 - 410 stops tracking and unlocks the form while preserving diagnostics
  ---
  duration_ms: 1.6407
  type: 'test'
  ...
# Subtest: cancellation failure remains visible across polling and allows another cancel
ok 55 - cancellation failure remains visible across polling and allows another cancel
  ---
  duration_ms: 1.9127
  type: 'test'
  ...
# Subtest: a cancellation failure is cleared once the job reaches a terminal state
ok 56 - a cancellation failure is cleared once the job reaches a terminal state
  ---
  duration_ms: 1.0513
  type: 'test'
  ...
# Subtest: same-cursor terminal cancellation discards a late running response
ok 57 - same-cursor terminal cancellation discards a late running response
  ---
  duration_ms: 1.5065
  type: 'test'
  ...
# Subtest: a job detached by Stop tracking stays cancellable and resumes tracking from the cancel snapshot
ok 58 - a job detached by Stop tracking stays cancellable and resumes tracking from the cancel snapshot
  ---
  duration_ms: 5.0859
  type: 'test'
  ...
# Subtest: accepted cancellation reports a rendering failure without claiming the request failed
ok 59 - accepted cancellation reports a rendering failure without claiming the request failed
  ---
  duration_ms: 1.3415
  type: 'test'
  ...
# Subtest: media bootstrap failure reaches the copyable log
ok 60 - media bootstrap failure reaches the copyable log
  ---
  duration_ms: 41.8885
  type: 'test'
  ...
# Subtest: media submit failure reaches the copyable log
ok 61 - media submit failure reaches the copyable log
  ---
  duration_ms: 5.6534
  type: 'test'
  ...
# Subtest: requests freeze editing and duplicates, and failure retains draft and base
ok 62 - requests freeze editing and duplicates, and failure retains draft and base
  ---
  duration_ms: 11.3638
  type: 'test'
  ...
# Subtest: replacing a resource ignores both stale success and stale failure
ok 63 - replacing a resource ignores both stale success and stale failure
  ---
  duration_ms: 0.9976
  type: 'test'
  ...
# Subtest: applying a replacement keeps the request busy and reports render failures
ok 64 - applying a replacement keeps the request busy and reports render failures
  ---
  duration_ms: 0.6226
  type: 'test'
  ...
# Subtest: a render failure during polling is reported and keeps an active job polling
ok 65 - a render failure during polling is reported and keeps an active job polling
  ---
  duration_ms: 2.4082
  type: 'test'
  ...
# Subtest: shared logs, tabs and HTML escaping keep data as text and restore newly rendered controls
ok 66 - shared logs, tabs and HTML escaping keep data as text and restore newly rendered controls
  ---
  duration_ms: 3.8636
  type: 'test'
  ...
# Subtest: generation diagnostics include the operation, attempted artifacts and separate recovery result
ok 67 - generation diagnostics include the operation, attempted artifacts and separate recovery result
  ---
  duration_ms: 0.7642
  type: 'test'
  ...
# Subtest: preview renders structured values and derived file hashes without interpreting HTML
ok 68 - preview renders structured values and derived file hashes without interpreting HTML
  ---
  duration_ms: 3.2267
  type: 'test'
  ...
# Subtest: Wonder text and structure preview preserves newlines and differentiates deletion from null
ok 69 - Wonder text and structure preview preserves newlines and differentiates deletion from null
  ---
  duration_ms: 0.8581
  type: 'test'
  ...
# Subtest: save previews before commit, blocks duplicates, and commits the exact confirmed request
ok 70 - save previews before commit, blocks duplicates, and commits the exact confirmed request
  ---
  duration_ms: 45.9859
  type: 'test'
  ...
# Subtest: return from preview keeps the draft and never commits
ok 71 - return from preview keeps the draft and never commits
  ---
  duration_ms: 2.7429
  type: 'test'
  ...
# Subtest: escape from preview keeps the draft and never commits
ok 72 - escape from preview keeps the draft and never commits
  ---
  duration_ms: 3.0117
  type: 'test'
  ...
# Subtest: preview failure shows diagnostics and keeps the draft and base
ok 73 - preview failure shows diagnostics and keeps the draft and base
  ---
  duration_ms: 1.5496
  type: 'test'
  ...
# Subtest: commit failure shows diagnostics and keeps the draft and base
ok 74 - commit failure shows diagnostics and keeps the draft and base
  ---
  duration_ms: 3.8213
  type: 'test'
  ...
# Subtest: reload requires approval for a dirty draft and discards it only on success
ok 75 - reload requires approval for a dirty draft and discards it only on success
  ---
  duration_ms: 1.6986
  type: 'test'
  ...
# Subtest: both job panels show identical file reports, validation errors and retained-backup diagnostics
ok 76 - both job panels show identical file reports, validation errors and retained-backup diagnostics
  ---
  duration_ms: 1.7855
  type: 'test'
  ...
# Subtest: initial load failure does not claim a draft was preserved
ok 77 - initial load failure does not claim a draft was preserved
  ---
  duration_ms: 0.9105
  type: 'test'
  ...
# Subtest: committed source paths are announced even when the saved page cannot render
ok 78 - committed source paths are announced even when the saved page cannot render
  ---
  duration_ms: 7.9127
  type: 'test'
  ...
# Subtest: intersecting writes from another editor refresh once after the active request
ok 79 - intersecting writes from another editor refresh once after the active request
  ---
  duration_ms: 3.7363
  type: 'test'
  ...
# Subtest: job panel errors put the diagnostic before the operation report
ok 80 - job panel errors put the diagnostic before the operation report
  ---
  duration_ms: 0.8323
  type: 'test'
  ...
# Subtest: pass, warnings and errors responses render their summary, state and grouped item counts
ok 81 - pass, warnings and errors responses render their summary, state and grouped item counts
  ---
  duration_ms: 42.8505
  type: 'test'
  ...
# Subtest: 400/504/500 responses show an incomplete validation, not a pass or a rule failure
ok 82 - 400/504/500 responses show an incomplete validation, not a pass or a rule failure
  ---
  duration_ms: 2.528
  type: 'test'
  ...
# Subtest: a save during a running validation queues exactly one follow-up run
ok 83 - a save during a running validation queues exactly one follow-up run
  ---
  duration_ms: 1.5279
  type: 'test'
  ...
# Subtest: the page instance validates on resource-saved and editor_panel emits it only after a successful commit
ok 84 - the page instance validates on resource-saved and editor_panel emits it only after a successful commit
  ---
  duration_ms: 12.495
  type: 'test'
  ...
# Subtest: fields group shared, path, milestones, task catalogue and national tasks separately
ok 85 - fields group shared, path, milestones, task catalogue and national tasks separately
  ---
  duration_ms: 8.3886
  type: 'test'
  ...
# Subtest: draft changes notify the victory-paths dirty indicator and reverting clears it
ok 86 - draft changes notify the victory-paths dirty indicator and reverting clears it
  ---
  duration_ms: 2.9536
  type: 'test'
  ...
# Subtest: request uses only document and the two source hashes without generated slot fields
ok 87 - request uses only document and the two source hashes without generated slot fields
  ---
  duration_ms: 2.7092
  type: 'test'
  ...
# Subtest: invalid numeric and JSON input remains a dirty draft and blocks validate and commit
ok 88 - invalid numeric and JSON input remains a dirty draft and blocks validate and commit
  ---
  duration_ms: 1.8828
  type: 'test'
  ...
# Subtest: booleans, multiline scripts and null values keep their types in the candidate
ok 89 - booleans, multiline scripts and null values keep their types in the candidate
  ---
  duration_ms: 1.2053
  type: 'test'
  ...
# Subtest: cancelled preview preserves base and sparse draft with no commit
ok 90 - cancelled preview preserves base and sparse draft with no commit
  ---
  duration_ms: 2.2593
  type: 'test'
  ...
# Subtest: save freezes identical validate, preview and commit bodies and clears drafts only after commit
ok 91 - save freezes identical validate, preview and commit bodies and clears drafts only after commit
  ---
  duration_ms: 2.369
  type: 'test'
  ...
# Subtest: missing reward reference from GET blocks save until read-only validation resolves it
ok 92 - missing reward reference from GET blocks save until read-only validation resolves it
  ---
  duration_ms: 1.2298
  type: 'test'
  ...
# Subtest: missing rewards discovered during validation never open preview or commit
ok 93 - missing rewards discovered during validation never open preview or commit
  ---
  duration_ms: 1.342
  type: 'test'
  ...
# Subtest: not-ready previews cannot be confirmed or committed
ok 94 - not-ready previews cannot be confirmed or committed
  ---
  duration_ms: 1.2973
  type: 'test'
  ...
# Subtest: 409 refreshes base and preserves user draft without retrying commit
ok 95 - 409 refreshes base and preserves user draft without retrying commit
  ---
  duration_ms: 1.5683
  type: 'test'
  ...
# Subtest: resource_busy does not rebase or auto-retry a commit
ok 96 - resource_busy does not rebase or auto-retry a commit
  ---
  duration_ms: 0.9639
  type: 'test'
  ...
# Subtest: generation failure retains operation diagnostics, base and unsaved draft
ok 97 - generation failure retains operation diagnostics, base and unsaved draft
  ---
  duration_ms: 0.864
  type: 'test'
  ...
# Subtest: refresh failure leaves loaded document, base and draft unchanged
ok 98 - refresh failure leaves loaded document, base and draft unchanged
  ---
  duration_ms: 0.5949
  type: 'test'
  ...
# Subtest: identity-based refresh survives reordered paths and tasks without changing task source identity
ok 99 - identity-based refresh survives reordered paths and tasks without changing task source identity
  ---
  duration_ms: 1.3725
  type: 'test'
  ...
# Subtest: deleted targets retain orphan drafts and block submit rather than silently applying elsewhere
ok 100 - deleted targets retain orphan drafts and block submit rather than silently applying elsewhere
  ---
  duration_ms: 1.1637
  type: 'test'
  ...
# Subtest: cost/reward refresh is deferred through confirmation and never expands the two-source base
ok 101 - cost/reward refresh is deferred through confirmation and never expands the two-source base
  ---
  duration_ms: 1.2831
  type: 'test'
  ...
# Subtest: generation plan is entirely registry-derived and includes read-only output and artifact reports
ok 102 - generation plan is entirely registry-derived and includes read-only output and artifact reports
  ---
  duration_ms: 0.4767
  type: 'test'
  ...
# Subtest: panel renders typed grouped fields, three read-only slots, dirty drafts and path switching
ok 103 - panel renders typed grouped fields, three read-only slots, dirty drafts and path switching
  ---
  duration_ms: 6.6936
  type: 'test'
  ...
# Subtest: panel renders unresolved reward warning and prevents save with read-only reference and output controls
ok 104 - panel renders unresolved reward warning and prevents save with read-only reference and output controls
  ---
  duration_ms: 1.6688
  type: 'test'
  ...
# Subtest: six-tool rail registers a dirty dot and external modal without generator execution
ok 105 - six-tool rail registers a dirty dot and external modal without generator execution
  ---
  duration_ms: 1.6228
  type: 'test'
  ...
1..105
# tests 105
# suites 0
# pass 105
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 399.5789
```
