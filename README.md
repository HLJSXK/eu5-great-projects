# Great Projects

Independent Europa Universalis V mod workspace, extracted from Towards Victory.
The game mod id remains `hades.towards_victory.great_project`.

The tooling requires Python 3.11 or newer.

Place this repository beside `eu5-modding-base`, then use the direct EU5 Python:

```powershell
python scripts/bootstrap_base.py
python -m pip install -r requirements.txt
python scripts/build.py --check
python -m great_projects_editor_web --check
python -m pytest -q
```

Set `EU5_MODDING_BASE` before bootstrap for another base location. The ignored
`.eu5-base` junction/symlink is the sole development dependency; TV is not needed.
Run `python -m great_projects_editor_web --no-browser` for the editor at port 8763.
`build.bat` packages locally; explicit `--deploy <game-mod-directory>` deploys
`tv_engineering_department` and the three named compatibility submods.
For local image processing install `requirements-image.txt` as well. Browser/Node tests
require Node 22+ and Chrome; the test script accepts EU5_PYTHON and CHROME_PATH.
Runtime dependencies remain Community Mod Framework 2.x and Construction Manager.

## Directory layout

| Path | Purpose |
| --- | --- |
| `src/` | Deployable Great Projects mod |
| `submods/` | Three GUI compatibility packages |
| `data/` | Source catalogs, generated-file registry and indexes |
| `data/tool_config/` | Shared image-tool and error-log configuration |
| `scripts/` | Workspace commands, integration generators and image tools |
| `scripts_engineering_department/` | Wonder and Engineering Department generators |
| `great_projects_editor_web/` | Independent editor, port 8763 |
| `unique_wonders_site/` | Atlas source and checked-in site output |
| `ai_gui_assessment/` | Offline GUI previews, fixtures and mockups |
| `assets/` | Original images, processed assets and historical image archives |
| `docs/` | Design, technical, knowledge and marketing documentation |
| `docs/archive/` | Pre-split editor documentation and repository extraction evidence |
| `tests/` | Python and Node regression tests |

Run `python scripts/error_log_filter.py` for the shared log filter, configured by
`data/tool_config/error_log_filter.json`. Image tools use
`data/tool_config/dds_icons.json`; paths inside that image configuration remain
relative to the repository root. Private `*.local.json` image settings remain at
the root and are ignored by Git.

`build/`, `tmp/`, Python caches and test caches are disposable local outputs.
Keep `.eu5-base`, `.editor_state/`, private settings, source images and historical
asset archives. The checked-in `unique_wonders_site/dist/` is part of the atlas.

See [CLAUDE.md](CLAUDE.md) and the [archive index](docs/archive/README.md) for the
extraction handoff and final audit.
