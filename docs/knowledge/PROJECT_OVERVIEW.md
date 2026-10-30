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

Europedia has a permanent scope of 15 mechanic cards plus Triumphal Axis and
Topkapi Palace as two worked examples. The full 195-wonder card catalogue was
removed for both initialization risk and poor information design: repeated
explanations and long scrolling obscure the mechanics. Do not restore it as a
performance fix or automatically add cards for new wonders. See
`docs/knowledge/risk_cards/europedia.md` for the decision and test evidence.

## Archived Work

The October 22 archived vanilla-takeover, AI-observer and editor-refactor work
remains historical evidence. Extraction does not reopen gameplay investigation
or certify untested runtime scenarios. See docs/archive/repository_split/Repository_Split.md.
