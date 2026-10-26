# Wonder Ritual Risk Card

The 2026-10-23 rework is authoritative. Generic and unique wonders share three
ritual styles; unique wonders inherit mechanics and own only bilingual flavor text.

1. Canonical data is `wonder_generic_rituals.yaml` (`rituals`, reward carriers,
   societal directions, estate preferences), `wonder_ritual_rules.yaml`, and
   `unique_wonders.yaml.ritual_text`. Use `ritual_styles()` and `final_building()`.
   There are no ceremony stages, auxiliary buildings, bespoke hooks, or
   style-specific final buildings.
2. Each location/wonder instance owns its style and expiring memory maps. Only
   grant/revoke write the style map. Country benefits are deduplicated by wonder
   and style, and revoked only after the last corresponding instance disappears.
3. Confirming charges the size-based scaled gold price and settles existing estates
   (+0.10 / -0.05); plain inauguration gives every participating estate -0.05.
   Completion grants modifiers, one-shot rewards and a signed 20-point societal
   change. Expansion of a dedicated wonder repeats none of these ritual rewards.
4. Show the actual `tv_wonder_ritual_apply_choice_effect` with native effect rendering.
   State writes and scheduling are hidden. Do not substitute prose for effect
   previews. Estate satisfaction belongs in confirmation's native tooltip.
5. Never put owned-location scans in decision conditions, option triggers, or
   visible grant/settle chains. Rededication lookup and country sync run only from
   hidden event immediates or ownership/building lifecycle callbacks.
6. Ownership loss clears dedication before old-country cleanup. Last-level
   demolition clears it; surviving levels retain it. Initial and externally
   founded wonders are plain. Expiry checks the current memory token, so a queued
   timer from a previous dedication cannot revoke a renewed one.
7. Mode 3 is rededication. It requires stage 0 plus active conception; it grants
   ritual effects and 10 prestige, then starts conception from zero (reason 4).
   Cancellation/abandonment has no further penalties and refunds no confirmed costs.
8. Axis availability uses `has_societal_value = societal_value_type:<axis>`;
   the numeric slider read is `societal_value:<axis>`. Do not confuse the type
   scope with the numeric link. See vanilla `events/culture/culture_greek.txt`.
9. Ritual stage 4 neither decays domestic support nor triggers support collapse.
   CMM skipping still requires a style choice and explicit confirmation.

Run `scripts_engineering_department/test_wonder_mechanics_rules.py`,
`pytest tests/test_wonder_ritual_rework.py`, editor/AI regressions and
`scripts/validate.py --changed --fix --ai-report`. Offline checks do not prove
calendar, save/load, multiplayer, or native tooltip behavior; record those separately.
