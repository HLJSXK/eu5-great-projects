# Wonder Support Reprieve (Engineering Department)

Status: implemented 2026-10-24 (awaiting in-game test)

## Rule

During one construction round (one locked project, from lock to completion or abort),
the first time post-debate Domestic Support reaches 0 does not settle the failure.
Instead the country receives event `tv_engineering_department.21`, a warning with
three options:

| Option | Cost | Result |
|---|---|---|
| a. Bribe the estates | 12 × `monthly_income_trade_and_tax` gold (min 100), split evenly among every estate the country has | +50 Domestic Support |
| b. Ruler's public statement | 50 political influence + 25 prestige | +50 Domestic Support |
| c. Give up | none | `tv_wonder_forced_abort_effect` (the normal failure) |

Options a/b are disabled when the country cannot pay. Option c is always available.
The second exhaustion in the same round goes straight to the existing failure event
`tv_engineering_department.20`.

The upgrade-project branch (level >= 1 and `tv_wonder_can_finish_construction_trigger`)
is unchanged: exhaustion there still finishes construction at the reached level,
because that is not a failure.

## State

| Variable (country) | Set | Cleared |
|---|---|---|
| `tv_wonder_support_reprieve_used` | support-resolution pulse, when `.21` is queued | `tv_wonder_clear_project_state_core_effect` (round reset) |
| `tv_wonder_support_reprieve_pending` | same time as `_used` | any `.21` option; round reset |

`_pending` blocks the monthly support-resolution pulse while the warning is open, so an
unanswered warning cannot be followed by a second-exhaustion failure next month.

## Files

- `src/in_game/common/on_action/tv_engineering_department_on_action.txt`:
  `tv_engineering_department_support_resolution_monthly_pulse` adds the `else_if` reprieve
  branch and the `_pending` guard.
- `src/in_game/events/tv_engineering_department_events.txt`: event `.21`.
- `src/in_game/common/scripted_effects/tv_engineering_department_effects.txt`:
  `tv_wonder_support_reprieve_bribe_effect`, `tv_wonder_support_reprieve_statement_effect`,
  round-reset cleanup.
- `src/in_game/common/scripted_triggers/tv_engineering_department_triggers.txt`:
  `tv_wonder_support_reprieve_project_active_trigger` (stale-event guard),
  `_can_bribe_trigger`, `_can_make_statement_trigger`.
- `src/in_game/common/script_values/tv_engineering_department_support_reprieve_values.txt`:
  all cost numbers (tune here).
- Localization: `.21.t/.d/.a/.b/.c` in English and Simplified Chinese; the Domestic
  Support game concept description mentions the reprieve. Other languages fall back
  until translated.

## Tuning notes

- Estate types handled: nobles, clergy, burghers, peasants, dhimmi, tribes, cossacks
  (all vanilla estates in `common/estates/00_default.txt`). A modded estate type would
  need adding to both the count script value and the bribe effect.
- AI weights: bribe 10, statement 5, give up 1 (only among affordable options).
