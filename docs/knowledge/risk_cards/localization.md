# Localization Risk Card

Load this card before writing or editing any player-facing localization text under
`src/main_menu/localization/` (all 11 languages), or before adding loc
strings inline while generating events, GUI, effects, or other content that produces new
localization keys.

## Required Checks

### 条目等级登记（强制）

所有本地化条目按强到弱分为：**原创 > AI生成 > 翻译 > 占位 > 缺失**。
等级表示文本来源和完成状态，不是按语言自动判定的质量分。

- **原创**：用户手动创作/修改的内容，或用户明确要求登记为原创的内容。
  **Agent 操作本地化文本时必须如实登记；除上述两种情况外，不得使用“原创”。**
  用户要求“写一段文案”、认可 AI 文案、运行生成器或在编辑器点击保存，都不等于明确要求登记为原创。
  登记时必须提供 `user_manual` 或 `user_requested` 依据，并用 `note` 如实说明具体来源/要求；不得虚构依据。
- **AI生成**：agent/AI 新写或实质改写的文本，包括生成器输出的新文案。
- **翻译**：从另一语言翻译而来，包括 AI/机器翻译；不能因使用 AI 翻译就升级为“AI生成”。
- **占位**：临时文案、直接复制英文的回退文本、尚未完成的替代文本。
- **缺失**：文本尚未提供。登记缺失不能豁免所有语言键集合一致的要求。

按用户 2026-10-30 的明确要求，初始化时现有中英文条目全部登记为 **AI生成**，
其他语言全部登记为 **翻译**。这只是当前库存的初始认定，不是后续新增/修改的默认规则。
现有空字符串同样保留用户指定的初始等级；空字符串可能有意用于界面排版，不能仅凭为空重新分类。

`data/localization_grades.json` 是独立、人工维护的逐条等级账本，按文件路径与 key 标识，
每条记录绑定文本 SHA-256。不要将等级塞入游戏 YAML 的版本数字。移动、删除、重命名、
生成器重建或源 YAML 改动后，必须在完成输出再登记；相同文本保留原等级，文本变动必须重新判断来源。
先按 `data/generated_files.yaml` 修改 owner/input 并重新生成，不要直接修改生成物或把账本作为可覆盖的生成输出。

使用直接 EU5 Python 解释器运行（`<file>` 为输出本地化文件，`<key>` 为实际条目）：

```text
scripts/localization_grades.py register --files <file> --keys <key> --grade AI生成
scripts/localization_grades.py register --files <file> --keys <key> --grade 翻译
scripts/localization_grades.py register --files <file> --keys <key> --grade 占位
scripts/localization_grades.py register --files <file> --keys <key> --grade 原创 --original-basis user_requested --note "用户明确要求及其范围" --replace
scripts/localization_grades.py prune
scripts/localization_grades.py check
scripts/localization_grades.py summary
```

默认只登记新增或文本变化的条目，保持未改动条目的等级；`--replace` 才会重新评级未变的文本。
批量不带 `--keys` 时，务必确认所有待登记条目确属同一来源。
`prune` 仅移除已删除键/文件的旧登记。初始化命令仅允许账本不存在时运行，不能重置已有等级。
通用本地化编辑器显示等级，并把通过其文本编辑接口保存的改动保守登记为 AI生成；
若实际为翻译、占位或符合原创条件，用登记工具明确更正。Agent 通过 UI/API 操作同样受本卡约束。

`LOC_GRADE` 是硬错误：未登记、非法等级、文本指纹过期、删除后残留登记和原创缺少依据均失败。
`validate.py --changed --fix --ai-report` 即使没有代码改动也检查；`--fix` 不得猜测作者或提升等级。

0. **All languages must contain identical key sets within each mod root.**
   `scripts/localization_policy.py` lists the 11 required languages. Any key that
   exists in any language must exist in every other language, including keys only
   present in a non-English source. Compare recursively across files; translations
   may organize keys in different filenames. A missing directory or file must not
   hide missing keys, and a file's `l_<language>:` header must match its directory.
   English and Simplified Chinese are the maintained source texts. The other nine
   languages normally use machine translation or English text directly; an English
   fallback is valid, an absent key is not. Preserve BOM and all interpolation tokens.
   The check runs even with `--changed`, unrelated changes, or no existing changed
   files. `--fix` does not silently invent translations or waive missing keys.

1. **Use the canonical six-way text-formatting mapping — do not invent or repurpose tags.**
   TV has a fixed semantic mapping from meaning to EU5's `#tag content#!` color/style tags,
   documented in full in `CLAUDE.md` section "Localization Text Formatting Convention":

   | Semantic need | Tag |
   |---|---|
   | Positive effect (gain/bonus) | `#G` |
   | Negative effect (loss/malus) | `#R` |
   | Neutral highlighted value/keyword (cost, threshold, non-judged number) | `#Y` |
   | Important content (pure emphasis, no valence) | `#high` |
   | Beginner tip / guidance text | `#weak` |
   | Pure flavor text (wonder descriptions, etc.) | `#F` |

   Do not use `#G`/`#R` for neutral numbers (a cost or requirement is not "positive" or
   "negative"). Do not use `#W`, `#X`, `#P`/`#N`, `#L`, or `#V` for any of the six needs above
   — those tags are reserved for their narrower vanilla roles (difficulty labels, danger
   warnings, enabled/disabled labels, secondary de-emphasis, alternate highlight). Trigger/requirement
   text inside `custom_tooltip`/`trigger` blocks must NOT be manually tagged with this table —
   the engine already colors it via `#trigger_pass`/`#trigger_fail`, and manual tags conflict
   with that automatic coloring. If a genuinely new semantic need doesn't fit these six rows
   (e.g. an irreversible-action risk warning distinct from a stat-based negative effect), ask
   before assigning it a tag rather than silently reusing an existing row for a different
   meaning.

2. **Always separate a color/style tag from its content with a space.**
   `#Y Text#!`, `#G {group}#!`, `#R 30#!` are correct; `#YText#!`, `#G{group}#!`, `#R30#!` are
   not — the parser reads the tag name as everything up to the first non-alphanumeric
   character, so adjacent content gets absorbed into the tag name and dropped or mangled. This
   applies equally to hand-written localization and to codegen that substitutes a generated
   name/value into colored text. See `docs/knowledge/anti_patterns.yaml` rules
   `loc_color_tag_adjacent_text` / `loc_color_tag_adjacent_variable`.

3. **File encoding and quoting.** Localization YAML must be UTF-8 **with BOM**, and only
   straight ASCII double-quotes (`"`) are valid — smart/curly quotes silently break parsing.
   Keep each key/value on one physical line; use `\n` inside the quoted string for an
   intentional line break, not a real newline (a real newline makes the next physical line
   parse as a new key).

4. **Full tag catalog reference.** For the complete list of available `#tag` values (including
   ones not part of TV's six-way mapping, like `#T` tooltip headers, `#col`/`#col_t`/`#col_m`
   tabular tags, and `#TOOLTIP:$TAG$...#!` breakdowns), see
   `docs/technical/EU5_Modding_Knowledge_Base.md` section 6.3 "Text Format Tag Catalog" before
   inventing a bespoke display solution.

5. **A YAML loc key alone is not enough for scripted-effect tooltips.** Any
   `custom_description = { text = KEY ... }` inside `common/scripted_effects` needs a matching
   `KEY = { ... }` registration entry under `in_game/common/effect_localization/` — the YAML
   string is only the display text, not the registry entry the engine validates at load.
   Missing the registration produces `No effect loc KEY` /
   `PostValidate of effect 'custom_description' returned false`. Register all four perspectives
   (`none`/`global`/`first`/`third`) as a safe default, and give positive/negative variants of
   the same event/effect **distinct** loc ids (`..._neg`, `..._past_neg`, etc.) — reusing one id
   for both produces `Negative and positive version share loc for effect loc <key>`. For
   third-person perspectives (`third`/`third_past`), keep the string self-contained (no
   `[COUNTRY.GetName]`-style promotes) since generic-action/event hover tooltips can
   pre-evaluate `custom_description` before a real `COUNTRY` promote target exists. See
   `docs/technical/EU5_Modding_Knowledge_Base.md` §6.1 "Scripted Effect `custom_description`
   Localization" and the risk cards for `philosophy_debate`/`wonders`, which hit this
   repeatedly.

6. **Trigger tooltips need a `trigger_localization` entry, not just a YAML key.** A
   `custom_description`/`custom_tooltip` referencing a trigger's loc key needs a matching entry
   in `src/in_game/common/trigger_localization/`; declare all four perspectives
   (`none`/`global`/`first`/`third`) as the safe default even if only `global` is currently used.

7. **`.tt`-suffixed `custom_tooltip` keys are a naming convention only — not auto-wired.** A key
   like `my_event.1.a.tt` must still be referenced explicitly via `custom_tooltip = my_event.1.a.tt`
   inside the option/effect block; the engine does not pick up `.tt`-suffixed keys automatically
   just because they exist in the YAML.

8. **`customizable_localization` files are non-additive database entries, not merge blocks.**
   Each top-level block name (e.g. `character_title_prefix`) in
   `in_game/common/customizable_localization/` is a single database key. Adding a second file
   with the same block name does not merge with the first — the engine logs
   `Duplicated key <block_name> will not be created` and silently drops the duplicate. To extend
   existing customizable localization (e.g. add title text), edit/copy the full original block
   rather than adding a second file. **General syntax/usage** (the `type`/`random_valid`/`text`/
   `trigger`/`fallback` block shape, and calling it from loc text with `Custom('block_name')`
   chained off a scope, e.g. `ROOT.GetCountry.Custom('ruler_residence')`) is documented in
   `docs/technical/EU5_Modding_Knowledge_Base.md` §6.3 "Customizable Localization Syntax and
   Usage" — read it before writing a new customizable-localization block or a `Custom(...)` call,
   since this system (conditional key selection via triggers, not a plain loc key) is unlike
   other Paradox games and easy to misuse as a normal loc lookup.

9. **Every generated modifier/database id needs its matching `_NAME_<id>` (and, for static
   modifiers, `_DESC_<id>`) loc key in every supported language** — this applies to
   `static_modifier` (`STATIC_MODIFIER_NAME_<id>`), `auto_modifiers`
   (`AUTO_MODIFIER_NAME_<id>`), and action price modifier types
   (`MODIFIER_TYPE_NAME_<id>_cost_modifier` / `MODIFIER_TYPE_DESC_<id>_cost_modifier`). Missing
   entries are silent in-game (blank/id-string display) rather than a load error, so a generator
   emitting a new id must emit its loc key in the same change.

10. **Do not chain `MakeScope` after an already-scripted-scope object in event localization.**
    `ROOT.MakeScope.GetVariable(...)` / `THIS.MakeScope.GetVariable(...)` treats an
    already-scoped object as if it were a GUI-layer binding and logs
    `Could not find promote for 'MakeScope'` / `Failed converting statement`. Read
    `ROOT.GetVariable(...)` / `THIS.GetVariable(...)` directly; reserve `.MakeScope` chains
    (`Country.MakeScope.GetVariable(...)`, `Location.MakeScope.GetVariable(...)`,
    `Player.MakeScope.GetVariable(...)`) for GUI-layer bindings that are not already a script
    scope.

## Validation

Run `validate.py --changed --fix --ai-report` after any localization change. Language
key parity is a hard failure (`LOC_COVERAGE`) and mismatched headers fail with
`LOC_LANGUAGE`; neither is a baseline warning. The validator also lints the
adjacent-tag rule, BOM encoding, and `effect_localization`/`trigger_localization` coverage for
`custom_description` keys (including the positive/negative distinct-id rule from check 5). There
is no automated lint for tag *semantic* misuse (e.g. using `#G` on a neutral cost value) or for
the `customizable_localization` non-additive-block rule in check 8; apply those by reading intent
and by grepping for an existing block name before adding a new customizable-localization file.
