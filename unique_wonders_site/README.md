# Wonders Atlas Site

Static atlas for Great Projects generic and unique wonders.

The site reads this repository's authored wonder data and writes its static bundle
under `unique_wonders_site/dist`. The map tiles and locations index are checked in
there, so a fresh clone builds from the checked-in assets without another mod checkout.
Do not delete `dist/tiles` or `dist/data/locations_index.json` expecting the build to
recreate them.

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
