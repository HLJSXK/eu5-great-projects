# Europedia Risk Card

Load this card before editing `encyclopedia_lateralview.gui`, adding new browsable Europedia
content, or wiring any `game_concept` into a curated (as opposed to search/link-only) display.

## Approved content scope — 2026-10-28

百科固定保留 **15 张机制说明卡、1 张凯旋轴线、1 张托普卡帕宫，共 17 张卡片**。
这是用户确认的长期内容设计；其余 193 张奇观百科卡片已经删除，不能通过默认遍历全部
奇观数据、隐藏控件或保留测试开关重新带回。`europedia_render.py` 的
`WONDER_CARD_KEYS` 仅列出 `triumphal_axis` 和 `unique_topkapi_palace`，
`select_wonder_cards()` 从当前玩法数据解析这两个示例。新增玩法奇观不会自动新增百科卡片。
主模组、生成片段和 Prosper or Perish 兼容覆盖必须采用同一范围。
本决定只删除百科卡片，不删除其他奇观的玩法、图像、概念或游戏内提示。

2026-10-29 页签调整：依次为 **全部、入门、完整机制、独特工程、通用工程**。
2026-10-30 调整：首张“大工程”总览卡（含环形全流程）归入“入门”，其余 16 张归入
“完整机制”。“全部”“独特工程”“通用工程”暂时留空，“全部”暂不聚合内容。
首次打开默认选中“完整机制”；保留原有 filter id，`overview` 对应“入门”。

**缩减不仅因为加载期卡死；原本的全量展开设计本身也不好。** 将相同的机制解释、等级效果、
选址说明和三种仪式结构重复铺在 195 张大卡片中，造成大量重复文字、冗长滚动和信息噪声，
让机制教学与逐个奇观的数据展示混在一起，难以阅读和定位。百科应集中讲清通用机制，
用一个通用奇观和一个独特奇观作完整示例。即使以后解决了性能问题，也不应恢复这种全量目录。

加载期证据与设计决定分开记录：原全量版本包含 210 张卡片；用户报告新游戏初始化卡死，
移除 402 个新增动态表格后仍卡死，改为筛选变量未设置时隐藏所有卡片后也仍卡死。
仅生成一张完整的凯旋轴线卡片、保留其动态表格和仪式预览时，用户确认可以加载。
这些结果没有证明具体引擎死锁、某个函数或纯控件数量就是唯一根因；隐藏控件不能作为已验证的
延迟创建方案。17 张卡片的最终范围来自上述设计取舍，不依赖将猜测写成确定根因。

## Required Checks

1. There is no native, data-driven way to add an Encyclopedia sidebar page/category.
   `Encyclopedia.AccessPages` / `EncyclopediaPage` is a read-only, engine-populated collection
   (`GetTitle`, `Self`, `AccessSelf` only — no `AddPage`/`RegisterPage`). A `game_concept` block's
   `family` field is a loose thematic tag with no page/category effect in vanilla's own
   `encyclopedia_lateralview.gui`. Do not search for a registry folder or a `page =` field — none
   exists. See anti-pattern `europedia_page_has_no_native_registration`.

2. A dedicated browsable tab requires a full override of `in_game/gui/encyclopedia_lateralview.gui`
   using the `GetVariableSystem`-toggle pattern (the only working precedent found, confirmed
   against released community mod `3613232232`): one button sets a toggle variable
   (`GetVariableSystem.Set('<var>', 'yes')`), vanilla content and the custom content become two
   sibling `vbox`es with mutually exclusive `visible = "[GetVariableSystem.HasValue(...)]"` /
   `"[Not(GetVariableSystem.HasValue(...))]"` guards, and every vanilla sidebar button additionally
   gets `onclick = "[GetVariableSystem.Clear('<var>')]"` so clicking back into a real page exits the
   custom view. `src/in_game/gui/encyclopedia_lateralview.gui` implements this with
   `tv_encyclopedia_active` (tab toggle) and `tv_encyclopedia_filter` (all/overview/mechanics/
   unique/generic filter buttons within the tab).

3. Preserve vanilla's `default_format = "#yellow_titles"` exactly on card titles.
   The reference mod's own copy of this line dropped the leading `#` (`"yellow_titles"`) — a
   drift, not an intentional variant. Copy the vanilla card template verbatim for this field.

4. The tab's own text lives in a generated Europedia localization pair, not in the concept
   files. `src/main_menu/localization/{english,simp_chinese}/tv_europedia_l_*.yml` are generated
   by `scripts_engineering_department/main_menu/localization/*/gen_tv_europedia_l_*.py` from the
   same two sources the cards are (`europedia_content.py` for the hand-written mechanic cards and
   `europedia_render.py` for the text every wonder card shares), so a card can never reference a
   key that does not exist. Cards read plain localization with `text = "<KEY>"`, and prose links
   with `raw_text = "<[link]>"` — never `[id|e]` for the card title itself.

   Wonder cards take their title and lead from the existing `game_concept_<concept>` /
   `game_concept_<concept>_desc` pair; everything else on those cards is generated from the wonder
   data (effects, dedications, estates, size, category). Do not hand-write per-wonder prose into
   the concept files: those keys are the wonder's in-game tooltip too, and the previous
   `game_concept_<id>_europedia_desc` mechanism was removed with the 2026-10-28 rewrite.

5. Card layout lives in `src/in_game/gui/shared/tv_europedia_style.gui`, a new-types file (it
   overrides no vanilla file, so it cannot conflict with another mod's GUI). A card is a header
   tab, a `tv_eu_lead` paragraph, then sections; each section is a `tv_eu_section` heading
   followed by `tv_eu_text`, a `tv_eu_step` flow, a `tv_eu_scale_step` ladder, a `tv_eu_panel`
   comparison, a `tv_eu_entry` list or a `tv_eu_choice` trio. Build cards through
   `scripts_engineering_department/europedia_render.py` rather than emitting them by hand, and put
   hand-written prose in `europedia_content.py`, which carries English and Simplified Chinese side
   by side. Keep card text bounded: `tv_eu_text` is a `text_multi` with matching
   `max_width`/`min_width` (1450, matching vanilla) and `autoresize = yes`, because an
   unconstrained elastic column blows out a card's width.

6. Do not build per-entry texture paths with a runtime `Concatenate` inside `texture =`.
   The two example images are known at generation time. Bake their literal DDS paths into the
   generated `.gui` text through the generator's `wonder_icon_texture()` helper. A runtime
   `Concatenate(...)` path expression can render blank (see `docs/knowledge/risk_cards/gui.md`
   rule 19). Do not restore the removed full-database card loop for image routing.

7. Preserve the scrollbox sizing contract on custom content. The custom tab's visible root and
   its `scrollbox` must use `layoutpolicy_expanding`; the static card-list root inside
   `scrollbox_content` must also use it and set `set_parent_dimension_to_minimum = height`.
   Each filter `button_regular` needs `layoutpolicy_horizontal = expanding`. Otherwise the
   scrollbox receives no stable content height and the cards/buttons can collapse into the panel's
   upper-left corner. This follows the same expanding-content shape used by vanilla
   `ui_library.gui`.

   Two more engine limits bite this panel specifically:

   - `Or` and `And` take **exactly two** arguments. `Or(a, b, c)` logs
     `Function 'Or' expected 2 arguments, got 3` and the whole widget expression is dropped
     (2026-10-28, the filter guards). The numbered forms exist for wider tests and take exactly
     their number: `Or3`/`And3`, `Or4`/`And4`, `Or5`/`And5` (counted in vanilla's own GUI: Or3 75,
     Or4 6, Or5 7, And3 223, And4 30, And5 11). Either nest two-argument `Or` or use `Or3`; `Not`
     takes one argument.
     `tests/test_wonder_ritual_rework.py::test_encyclopedia_gui_expressions_match_engine_arity`
     checks the whole panel for this.
   - The filter variable does not exist until a filter button is pressed. The mechanics button
     and its cards accept the unset case (`Not(GetVariableSystem.Exists('tv_encyclopedia_filter'))`)
     so the first visit selects Complete Mechanics. Other tabs match only their own value.

8. **`encyclopedia_lateralview.gui` full-file-override conflicts with other Workshop mods.**
   EU5's Jomini GUI loader replaces a `.gui` file wholesale per relative path — it does not
   merge — so any other mod that also ships its own `in_game/gui/encyclopedia_lateralview.gui`
   will silently drop either its own or our custom tab, whichever mod loads last, with no error
   logged (the same failure mode documented for `location_window.gui` in
   `docs/knowledge/risk_cards/wonders.md`). Prosper or Perish (Workshop `3613232232` — the same
   mod cited as the tab-toggle precedent in rule 2 above) also fully overrides this file with its
   own `pp_encyclopedia_active`/`pp_filter` tab. `submods/tv_prosper_or_perish_compat/` resolves
   this via `scripts/compat/gen_tv_prosper_or_perish_encyclopedia_lateralview.py`, which merges
   both tabs onto a single shared toggle variable (`tveu_compat_encyclopedia_active`) using
   distinct string values (`'tv'` / `'pp'`) instead of two independent per-mod booleans. This
   avoids needing to chain multiple `GetVariableSystem` effect calls in one vanilla nav button's
   `onclick` (no verified precedent for that exists anywhere in `reference_game_files`) — since
   both tabs share one variable, the vanilla "all pages" button and each per-page nav button only
   ever need a single `Clear('tveu_compat_encyclopedia_active')`, and the mutual-exclusion check
   for "is any custom tab active" uses the single-arg `GetVariableSystem.Exists(...)` accessor
   (verified at `.eu5-base/reference_game_files/game/main_menu/gui/...`: `GetVariableSystem.Exists('gamerules_page')`)
   instead of `Or`-ing two `HasValue(...)` checks. The compat submod depends on
   `hades.towards_victory.great_project` (which owns `encyclopedia_lateralview.gui`); Prosper or
   Perish has no declared internal mod id (`"id": ""` in its own metadata) so it cannot be
   declared as a formal dependency relationship — the submod's description names it instead.
   After changing either TV's or Prosper or Perish's tab content, re-run
   `scripts/compat/gen_tv_prosper_or_perish_encyclopedia_lateralview.py`; it asserts exact
   occurrence counts of the known toggle-variable patterns and the exact 6-line closing tail of
   TV's file, and raises rather than silently mis-merging if either upstream file's structure has
   drifted.

## Validation

Run `validate.py --changed --fix --ai-report` (it checks that the generated localization exists
and is fresh), then manually open the Europedia panel in-game, click the custom tab and each of
the five filter buttons, scroll the full card list, and hover a few cards — text-width, blank-icon
and empty `ShowModifierEffect` rows only surface on render/hover, not statically.

`tests/test_wonder_ritual_rework.py::test_encyclopedia_keeps_only_approved_cards` checks all
15 mechanic cards, exactly the two approved examples and six native ritual previews in the
generator and both deployed source roots. Missing or duplicate example keys fail generation.
`test_encyclopedia_renders_three_native_previews_in_the_body` also checks that each example's
three completion previews use the real scripted effects in body text, never a `text_single` or
`icon`. Verify a fresh new-game load and both example cards in game; static checks do not prove
native initialization or rendering behavior.

## Relevant Anti-Patterns

- `europedia_page_has_no_native_registration` [advisory]: no data-driven Encyclopedia page
  registration point exists; a custom tab requires the full-panel `GetVariableSystem`-toggle
  override described above.
