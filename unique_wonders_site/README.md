# Wonders Atlas Site

Static atlas for Great Projects generic and unique wonders.

The site reads this repository's authored wonder data and writes its static bundle
under `unique_wonders_site/dist`. The map tiles and locations index are checked in
there, so a fresh clone can build with the current shared base.

If `.eu5-base/reference_mods_variants/eu5-towards-victory/national_destinies_site/dist`
contains reference tiles and a locations index, the build refreshes those assets.
The current base snapshot has no such directory: the build prints a warning and
uses the checked-in map assets. Do not delete `dist/tiles` or
`dist/data/locations_index.json` expecting the base to recreate them.

## Build

Run from the repository root:

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe unique_wonders_site/scripts/build/build_site.py
```

The build refreshes map assets only when that optional reference snapshot exists,
then generates `dist/data/unique_wonders.json` from local wonder data.
Unique wonders are displayed as map pins. Generic wonders have no map pins and
open from the left-side generic wonder list.

## Preview

```powershell
cd unique_wonders_site/dist
C:\Users\Hades\anaconda3\envs\eu5\python.exe -m http.server 8790
```

Then open `http://127.0.0.1:8790/`.
