# Wonder GUI Risk Card

Load this card for Engineering Department GUI panels, `location_window.gui`,
Europedia wonder cards, generated GUI fragments, and wonder localization used by
GUI widgets.

## Required Checks

1. Remember that `.gui` files are full-file overrides.
   EU5 does not merge GUI files by widget. Any mod that also ships
   `in_game/gui/location_window.gui` can conflict with the wonder overlay. Known
   compat submods splice the overlay into third-party files; do not hand-copy
   partial GUI fragments into the main override.

2. Use tooltip scopes exactly as passed.
   If `ShowScriptedEffectForScope` passes `LocationView.GetLocation.MakeScope.Self`,
   the scripted effect root is already the location. Use `owner ?= { ... }` to
   enter the country. Reserve `location.owner` for callbacks that expose a
   separate `location` event target.

3. Bound paragraph text and its containers.
   A fixed-width `text_multi` with `max_width` and `autoresize` is not enough if
   its parent `hbox`/`vbox` collapses to content. Give explicit-width containers
   the needed layout policy too.

4. Keep dynamic routing numeric and generated.
   Do not use `GetFlagName` as a raw script key for loc, texture, modifier, or
   effect-name concatenation. Store numeric ids and generate branches or use a
   typed datamodel object with a real key accessor.

5. Engineering Department ritual choices render the real completion effect with
   `ShowScriptedEffectForScope`. Location-gallery ritual cards show their own
   country/local modifiers expanded with `ShowModifierEffect` in native
   `TooltipStringPairList` rows inside hover tooltips, including inactive styles.
   Do not replace the effect rows with `ShowModifier` name links (user correction,
   2026-10-29). Estate reactions remain part of the separate confirmation flow.

6. Prefer GUI display variables refreshed from lifecycle points.
   Do not call expensive rebuilds from hover, tooltip, or render-only paths.

7. Keep location ritual modifier details in hover tooltips, not on the cards.
   The visible rows contain the ritual name and active-state indication only.
   Historical pitfall when using compact summaries elsewhere:
   `ShowOnlyIconModifierEffect` still emits hard line breaks between modifiers;
   `text_single` does not remove them (user in-game screenshot, 2026-10-29).
   To display such output horizontally, preserve a newline between lists and use
   `StringToRowList(...).GetRows` with `HorizontalModifiersList`, following
   vanilla `ambitions_lateralview.gui`. Override the item text to `multiline = no`.
   Do not restore the compact location summaries; that layout was superseded.

8. Keep `fittype` off the location-gallery medallion `icon` widgets.
   The user's 2026-10-29 runtime log reports `Property 'fittype' not handled`
   on all 30 `tv_location_wonder_medallion_<slot>_<level>` instances, identifying
   the engine widget as `ubericon`. These square textures use an explicit
   48-by-48 size; the artwork's separate `background` keeps its own fit setting.
   Fix `gen_location_window.py` and regenerate the main, M&T and SoL panels.
   Offline rendering alone did not detect this unsupported runtime property.

9. Keep the gallery a direct child of the location `lateralview`, with a vertical
   offset aligning its top with the city appearance (163 native GUI units).
   Nesting it under the scene widget broke every gallery hover in the user's
   2026-10-29 game test, even with `allow_outside` on the scene and gallery.
   Offline tooltip selection bypasses mouse hit testing and did not catch this.
   Preserve the working root attachment; test hierarchy as well as alignment.

10. Level and ritual hovers use the native `ContextualTooltipType` header slots
    (`title_icon`, `title_text`, `concept_link`) and exactly two framed sections:
    effects stacked one per row in one `TooltipListBase`, then history in the
    native delayed `TooltipFlavorTextBlock`. Keep native sizing, fonts and
    backgrounds. Do not restore side-by-side country/local effect columns or
    replace the header/flavor widgets with custom text (user request, 2026-10-29).
    Artwork hovers use the same native header and history section, with a native
    `TooltipRequirementsList` for construction conditions as the first section.
    Preserve its location-scoped trigger preview and native row sizing/fonts.

11. Let `TooltipStringPairList` handle empty rows/footer through its native data
    model predicates; hide `stringpair_datamodel_is_empty` for absent local rewards.
    Do not gate these tables with `IsUTF8StringNotEmpty(Localize(...))` or
    `IsUTF8StringNotEmpty(ShowModifierEffect(...))`: both CString-producing paths
    continuously logged `FetchData failed` during the user's 2026-10-29 hover test.
    Do not mock the entire visibility predicate to a boolean in the preview;
    sample only its underlying data so unsupported expressions remain diagnostic.

## Validation

Before confirmation, the ritual ledger has exactly three sibling sections in
order: ritual options (including their supporting estates and selected ritual's
flavor below the plain choice), requirements (duration and native cost preview), and expected effects (native
completion-effect preview, including native societal-value effects). The confirmation action
is a separate footer below all three sections. Do not restore a fourth values
heading or put the confirmation button inside the requirements section. Retain
the shared plain-inauguration alternative for construction and rededication,
and the in-progress details toggle. Start the ledger directly with the options
section; there is no introductory banner or dedicated rededication cancel button.
The flavor paragraph uses native `default_format = "#flavor"` and the default
text size, without a custom font-size override or inline format wrapper.
Do not add a custom societal-value axis, progress bar, side labels or direction
arrows below the native effect preview; value movement is rendered by the effect itself.

The ritual ledger uses 42-unit choice cards showing only the icon and ritual
name. Plain shares the same card builder, font, padding, background and selection
highlight; it has no subtitle or separate checkmark. Each ritual style card has
its own horizontal `flowcontainer` with `wrap_count = 7`
for 36-unit supporting-estate widgets (32-unit estate icon plus a green check
badge), filtered by that style's cached preference. Keep the art transparent to
mouse input so the whole widget remains one hover target. Its native
`ContextualTooltipType` uses the typed Estate name in the support headline and
one `TooltipTextBlock` below for the cached preference source (local rewards,
established preference, or this ritual's random preference). Keep absent/non-supporting
estates hidden and the row height content-driven. Do not restore the bottom estate cards
or the choice-card detail/count lines (user layout revision, 2026-10-29).
Do not restore `dynamicgridbox` with `spacing`: the user's 2026-10-29 21:30:39
runtime log rejected that property at panel line 4174, and the cards overlapped
the terms and confirmation button. Fix `wonder_ritual_gui.py`, regenerate the
mechanics fragment, then run its merge script. Preview regressions cover empty,
sparse and seven-supporter rows, grouping before selection, and native-only effect output;
offline previews do not establish native acceptance after reload.

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts\validate.py --changed --fix --ai-report
```

For location-window generator changes, run the relevant generator and rely on
`validate.py` freshness checks for generated overrides.
