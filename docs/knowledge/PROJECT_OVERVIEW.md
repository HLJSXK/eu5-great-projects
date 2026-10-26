# Great Projects

## Mod Identity

- **Mod Name:** Great Projects
- **Mod ID:** `hades.towards_victory.great_project`
- **Version:** Build date (`YYMMDD`)
- **Target:** EU5 1.4 beta (`1.4.*`)
- **Status:** In Development
- **Language:** English + Simplified Chinese

## Development Policy

This repository owns Engineering Department, wonder construction, the atlas,
GUI compatibility submods and their data, generators, editor and tests.
Its sole development dependency is `eu5-modding-base`, connected via `.eu5-base`.
CMF 2.x and Construction Manager remain runtime dependencies. TV consumes GP;
GP never imports TV's checkout. Keep existing `tv_` runtime identifiers.

Unreleased internal tooling uses one current architecture, without compatibility
wrappers or read-path repair. Generated outputs belong to data/generated_files.yaml.
Generic actions require an AI actions list, message type and all five notification
localization fields (HEADER, TITLE, SETUP, LOG, MAP) in both languages.

## Archived Work

The October 22 archived vanilla-takeover, AI-observer and editor-refactor work
remains historical evidence. Extraction does not reopen gameplay investigation
or certify untested runtime scenarios. See docs/technical/Repository_Split.md.
