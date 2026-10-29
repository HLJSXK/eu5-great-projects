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
   country/local modifiers expanded with `ShowModifierEffect` in separate
   `TooltipStringPairList` tables inside hover tooltips, including inactive styles.
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

## Validation

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe scripts\validate.py --changed --fix --ai-report
```

For location-window generator changes, run the relevant generator and rely on
`validate.py` freshness checks for generated overrides.
