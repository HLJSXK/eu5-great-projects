# Great Projects

Independent Europa Universalis V mod workspace, extracted from Towards Victory.
The game mod id remains `hades.towards_victory.great_project`.

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

See [CLAUDE.md](CLAUDE.md) and [extraction handoff](docs/technical/Repository_Split.md).
