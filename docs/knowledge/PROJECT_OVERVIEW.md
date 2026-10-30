# Great Projects

## Mod Identity

- **Mod Name:** Great Projects
- **Mod ID:** `hades.towards_victory.great_project`
- **Version:** Build date (`YYMMDD`)
- **Target:** EU5 1.4 beta (`1.4.*`)
- **Status:** In Development
- **Languages:** Complete keys in all 11 game languages; English + Simplified Chinese are the maintained source texts.

## Development Policy

This repository owns Engineering Department, wonder construction, the atlas,
GUI compatibility submods and their data, generators, editor and tests.
Its sole development dependency is `eu5-modding-base`, connected via `.eu5-base`.
CMF 2.x and Construction Manager remain runtime dependencies. TV consumes GP;
GP never imports TV's checkout. Keep existing `tv_` runtime identifiers.

Location windows reference SOL's optional `sol_location_living_standard_button`.
GP exports its wonder button, root-level gallery panel and queue-close template
through `in_game/gui/tv_location_wonder_widgets.gui`; the main window and both
location compatibility submods use those shared definitions. Other window owners
can use the same interface without copying GP's layout or tooltip implementation.
See `docs/guides/Location_GUI_Integration.md` for insertion sites and load order.

Unreleased internal tooling uses one current architecture, without compatibility
wrappers or read-path repair. Generated outputs belong to data/generated_files.yaml.
Generic actions require an AI actions list, message type and all five notification
localization fields (HEADER, TITLE, SETUP, LOG, MAP) in all 11 languages.

Within each mod root, every localization key present in any language must also
exist in every other language. Compare the union of all keys, recursively across
files; a key found only in Chinese or French is just as binding as an English key.
The required languages are `english`, `simp_chinese`, `french`, `german`, `spanish`,
`russian`, `polish`, `japanese`, `korean`, `braz_por`, and `turkish`, defined in
`scripts/localization_policy.py`. Except for English and Simplified Chinese,
localization normally uses machine translation or the English text directly.
Translation quality and key completeness are separate: missing keys fail validation.
Every entry also has a content-bound provenance grade in `data/localization_grades.json`:
原创 > AI生成 > 翻译 > 占位 > 缺失. Agents must register the actual source after edits
or regeneration. 原创 is reserved for user-manual content or an explicit user request,
with recorded evidence. The initial inventory is AI生成 for EN/ZH and 翻译 for all
other languages. See `docs/knowledge/risk_cards/localization.md` and
`scripts/localization_grades.py`; unregistered/stale grades fail `LOC_GRADE` validation.

Europedia keeps 15 teaching cards and two worked examples, plus the user-approved
compact catalogue in Unique Projects and Generic Projects (2026-10-30). Catalogue
entries and the two worked examples bake their text, six-level values and rituals
offline: no live effect/trigger previews or construction conditions. Unique entries
have a fixed location reference below their artwork. See
`docs/knowledge/risk_cards/europedia.md` for the static contract and historical
load-risk evidence. The overview/cycle remains in Getting Started.

## Archived Work

The October 22 archived vanilla-takeover, AI-observer and editor-refactor work
remains historical evidence. Extraction does not reopen gameplay investigation
or certify untested runtime scenarios. See docs/archive/repository_split/Repository_Split.md.
