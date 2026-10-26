# Wonders Atlas Site

Static atlas for Great Projects generic and unique wonders.

The site reads the mod's authored wonder data and the map assets from
`.eu5-base/reference_mods_variants/eu5-towards-victory/national_destinies_site`, then writes a deployable static bundle
under `unique_wonders_site/dist`.

## Build

Run from the repository root:

```powershell
C:\Users\Hades\anaconda3\envs\eu5\python.exe unique_wonders_site/scripts/build/build_site.py
```

The first build copies the reference map tile pyramid into `dist/tiles`, then
generates `dist/data/locations_index.json` and `dist/data/unique_wonders.json`.
Unique wonders are displayed as map pins. Generic wonders have no map pins and
open from the left-side generic wonder list.

## Preview

```powershell
cd unique_wonders_site/dist
C:\Users\Hades\anaconda3\envs\eu5\python.exe -m http.server 8790
```

Then open `http://127.0.0.1:8790/`.
