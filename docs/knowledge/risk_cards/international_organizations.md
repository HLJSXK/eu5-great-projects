# International Organizations Risk Card

Load this card before editing files under `common/international_organizations/` or effects
that create, find, or mutate Engineering Department IOs.

The `tv_` runtime namespace is retained. TV-only Trade League state and law-seeding
policies belong to the TV workspace and do not configure Engineering Department.
Cross-repository examples below are historical evidence, not local tool dependencies.

## Required Checks

1. Preserve Engineering Department IO leader invariants.
   Do not call `international_organization_chooses_new_leader` for Engineering Department IOs. Keep
   `leader_change_trigger_type = none`, and read appointed characters through
   `leader_country.var:tv_xxx_leader_char.attribute`.

2. Treat Engineering Department IOs as non-unique unless explicitly documented otherwise.
   Do not use `international_organization:type_key` links for non-unique Engineering Department IOs. Iterate
   memberships and filter by `international_organization_type = international_organization_type:<id>`.

3. Make nullable leader_country access optional.
   Use `leader_country ?= ...` in filters or tooltip-visible contexts. Vanilla IOs and newly
   created IOs can have null leader countries during evaluation. IO law browsing can also
   walk `on_activate` / `on_deactivate` effect chains, so mirrored leader-country writes there
   must use `leader_country ?= { ... }`.

4. Do not use IO `monthly_effect`.
   Engineering Department international_organization types must not define `monthly_effect` blocks. They have
   severe performance costs even when hidden. Use IO variable `monthly_change` only for
   visible breakdowns meant to appear in tooltips. When a visible IO typed variable's progress
   UI or monthly tooltip depends on automatic monthly gain, keep the real contribution in that
   variable's `monthly_change`. Move maintenance/completion side effects to registered country
   monthly pulses or explicit lifecycle hooks; repair `monthly_change` scope/conditions or
   cached country inputs rather than moving visible variable arithmetic elsewhere.

5. Match scope to monthly_change.
   IO variable `monthly_change` evaluates from IO/variable context. Do not call country-scoped
   scripted triggers that depend on `root`, `prev`, or caller-specific saved scopes unless the
   full scope chain is verified in the IO variable context. Prefer writing the condition directly
   under `leader_country ?= { ... }`, or create an IO-scoped helper trigger.

6. Match scope to IO law block type.
   In IO policy `allow`, `on_activate`, and `on_deactivate`, the current root is already the IO.
   Do not wrap IO variable or policy checks in `scope:recipient` there. Reserve `scope:recipient`
   for documented country-root AI math blocks such as `wants_this_policy_bias` and
   `wants_propose_policy`.

7. Guard IO law AI math recipient reads.
   `wants_this_policy_bias`, `wants_propose_policy`, `wants_keep_policy`, `reasons_to_join`,
   and `diplomatic_capacity_cost` may be pre-evaluated without a recipient event target.
   Before direct `scope:recipient` reads, add `exists = scope:recipient` in the same limit
   block, or use optional `scope:recipient ?= { ... }` when a trigger-only check is enough.

8. Use the evaluating country in generic action AI-list IO filters.
   `generic_action_ai_lists` potential root is the country. Inside
   `any_international_organizations_member_of`, `this` is the IO, so leader checks should use
   `exists = leader_country` plus `leader_country = root`, not `leader_country = this`.

9. Use `scope:actor` in country interaction potential blocks.
   In `common/country_interactions`, `potential` exposes the acting country as `scope:actor`.
   Wrap IO membership checks in `scope:actor = { ... }`; direct country-scoped IO iterators
   under `potential` can evaluate from an invalid root.

10. Guard country interaction pre-selection reads.
   Country interaction `accept` scoring and sometimes `effect` preview paths can be evaluated
   from panel buttons before a `select_trigger` has populated `scope:recipient`. Put direct
   `scope:recipient` reads behind `exists = scope:recipient`, and initialize actor-owned
   variables at the lifecycle point that creates the IO before reading them in `accept`.

11. Keep heavy generated maintenance behind cheap country-pulse gates.
    Register a named country monthly pulse through `data/pulse_registry.yaml`, save the country
    scope, iterate that country's `every_international_organizations_member_of` filtered to the
    relevant Engineering Department IO plus `leader_country ?= <saved country>`, and only then call the IO-scoped
    refresh effect.

12. Match IO membership iterators to trigger/effect context.
    `any_international_organizations_member_of` is trigger syntax. In effect bodies,
    use `every_international_organizations_member_of = { limit = { ... } ... }`
    when you need to enter matching IO scopes and run effects.

13. Define custom special-status parliament modifier type pairs.
    Every custom IO special status key that can be implemented by an IO needs
    `<status>_can_participate_in_parliament` and `<status>_agenda_impact` in
    `main_menu/common/modifier_type_definitions`, both with
    `game_data = { category = internationalorganization }`. Missing definitions can
    trigger startup DB assertions even when the status is not explicitly using parliament.

14. Give parliament law votes a real meeting location.
    `call_parliament_for_law_change` ends by calling `set_parliament_location` on a saved
    `parliament_location`. For non-HRE IOs it can use `parliament_seat`, a proposer-owned
    IO-owned location, or a random IO-owned location. If a Engineering Department IO has no IO-owned locations,
    set its `parliament_seat` variable to a valid location such as the leader capital before
    policy votes can be proposed.

15. Sync custom parliament special statuses from stable lifecycle points.
    For custom IO statuses that drive parliament voting or visible special-status power, do
    not rely only on `auto_bestowal_trigger` or same-tick `on_joined` state. Follow the HRE
    free-city pattern: the action or lifecycle effect that creates, invites, promotes, demotes,
    or removes a country should directly call `international_organization_add_special_status`
    or `international_organization_remove_special_status` from the IO scope. Do not add
    recurring monthly refreshes for special-status repair, and do not add extra parliament-seat
    or full-member repair unless a separate law-vote/location bug proves it is needed.

16. Keep IO-scoped helpers out of unstable creation-block roots.
    A `create_international_organization = { ... }` body can be walked during generic-action
    pre-evaluation before the new IO is a stable root. Do not call helpers there if they start
    with IO-only triggers such as `international_organization_type`. Prefer the IO type's
    `on_creation` / `on_joined` hooks, or switch to a verified saved IO scope after creation.

17. Define member opinion biases for every Engineering Department IO type.
    Each IO type should have a matching `io_opinion_<io_type>` entry under
    `in_game/common/biases/` and the same key localized in both supported languages.
    Missing the bias logs a startup warning that the organization needs an opinion of
    other members.

18. Filter IO policy member modifiers to their intended recipients.
    Vanilla `policy_vote` adds `scope:vote.modifier_utility(scope:actor)` to each
    voting country's AI support as `POLICY_MODIFIER_UTILITY`. If a visible IO law
    policy effect is meant for the leader country only and must stack with other
    law modifiers, keep it as `country_modifier` but make the display filter
    recipient-safe:
    `potential_trigger = { OR = { NOT = { exists = scope:recipient } is_leader_of_international_organization = scope:recipient } }`.
    The no-recipient branch is for ordinary law browsing; the leader check still
    applies when a vote/application recipient exists. Use `leader_modifier` only
    when replacing previous leader modifiers is intended. Otherwise subject or
    non-target members can strongly favor a policy because they evaluate the
    unfiltered modifier package as their own direct benefit.

19. Keep idle parliament issues positively desirable.
    When a custom IO uses vanilla `call_organization_parliament` for normal, non-law
    sessions, make sure at least one issue for the participating special status has
    valid `potential` / `allow` / `selectable_for` and positive
    `wants_this_parliament_issue_bias` in ordinary founding or neutral-member states.
    Otherwise the issue picker can show that no special status has issues to bring.

20. Use native IO membership tenure checks.
    For mechanics gated by how long a country has belonged to an IO, use the country-scoped
    `years_in_international_organization = { international_organization = <io scope> value >= N }`
    trigger. In an IO-root `every_international_organization_member` iterator, `root` is the
    IO; in an IO effect iterator that enters a member country, `prev` can point back to the
    iterated IO. Do not add monthly countdown variables or date stamps just to mirror this
    built-in tenure value.

21. Do not re-read a variable_map as the confirmation gate for a long-open event.
    A `trigger_event_non_silently` confirmation event can stay open for arbitrary game
    time before the player answers. Validate the scope captured at queue time/`immediate`
    directly (e.g. ownership) instead of re-reading a `variable_map`/`global_variable_map`
    entry for the event's key and identity-matching it against that captured scope;
    ownership-change or lifecycle handling can legitimately reselect the map's candidate
    while the popup is open. Also make any trailing unconditional cleanup effect
    conditional on the confirmation having actually committed, so a failed confirm does
    not silently discard the pending request. If the same option also ran an `instant`
    construction in its visible effect just before this confirm runs, do NOT re-check
    `has_building_with_at_least_one_level` here either -- instant construction does not
    reliably update that read within the same effect chain (see the Critical EU5 Gotchas
    in the repo-root CLAUDE.md); trust that the visible construct_building already ran and
    only re-validate ownership/other non-building state.
    See `tv_govhouse_confirm_local_administration_event_scope_effect` in
    `eu5-towards-victory:src/in_game/common/scripted_effects/tv_govhouse_effects.txt` and
    `docs/knowledge/anti_patterns.yaml` rule `variable_map_reread_as_confirmation_gate`.

22. Create IOs from a start-of-game event's `immediate`, not a visible option.
    An onboarding/game-start event whose option calls a "create or join this founder IO"
    scripted effect must have that call in the event's `immediate` block, not the option's
    effect chain. The nested `add_country_to_international_organization` / `set_leader_country`
    inside `create_international_organization = { ... }` render their own tooltip text
    (`THIRD_ADD_TO_INTERNATIONAL_ORGANIZATION_EFFECT`, `SET_LEADER_EFFECT`), and option-effect
    tooltip preview evaluates them before the IO is actually created, causing
    `Promote 'INTERNATIONAL_ORGANIZATION' returned nullptr`. See
    `docs/knowledge/anti_patterns.yaml` rule `io_creation_in_visible_option_effect_breaks_tooltip_preview`
    and `docs/knowledge/risk_cards/events.md` rule 11.

23. Give each signed `monthly_change` contribution its own named operation.
    Do not wrap positive and negative cases in one `add = { desc = KEY ... }` and flip the
    negative case with an inner conditional `multiply = -1`. The IO variable tooltip can expose
    that anonymous sign operation as a phantom negative row with `missing tooltip`, including
    when the branch does not actually affect the monthly total. Put mutually exclusive conditions
    outside the arithmetic node: emit `add = { desc = KEY <positive magnitude> }` for the positive
    case and `subtract = { desc = KEY <positive magnitude> }` for the negative case. Conditions
    that produce zero should enter neither operation. This matches the signed contribution pattern
    in vanilla `catholic_church.txt`.

## Validation

Run `validate.py --changed --fix --ai-report`; it fails any Engineering Department IO `monthly_effect` block. Then
inspect shared IO tooltips in game. Tooltip rendering is part of the execution surface for IO
variables. For any visible IO typed variable changed during a task, verify that the monthly
breakdown still appears in the IO variable tooltip.
