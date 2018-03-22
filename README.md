# overwatch-stats
Python wrapper around ovrstat API

WIP: currently has many hardcoded values, currently prints stats for allHeroes and top 5 most played heroes per player

Sample usage:

```
$ python3 main.py

STATS FOR sinatraa-11809
key missing: average.allDamageDoneAvgPer10Min
key missing: average.allDamageDoneAvgPer10Min
key missing: average.allDamageDoneAvgPer10Min
key missing: average.allDamageDoneAvgPer10Min
+----------------------------+-----------+
|   allDamageDoneAvgPer10Min |  name     |
+============================+===========+
|                      17    | allHeroes |
+----------------------------+-----------+
|                      10.82 | sombra    |
+----------------------------+-----------+
|                            | moira     |
+----------------------------+-----------+
|                            | orisa     |
+----------------------------+-----------+
|                            | mercy     |
+----------------------------+-----------+
|                            | symmetra  |
+----------------------------+-----------+


STATS FOR Fleta-31226
key missing: average.allDamageDoneAvgPer10Min
+----------------------------+-----------+
|   allDamageDoneAvgPer10Min |  name     |
+============================+===========+
|                      15    | allHeroes |
+----------------------------+-----------+
|                      17.19 | moira     |
+----------------------------+-----------+
|                      13.39 | doomfist  |
+----------------------------+-----------+
|                       9.01 | orisa     |
+----------------------------+-----------+
|                      10.04 | sombra    |
+----------------------------+-----------+
|                            | symmetra  |
+----------------------------+-----------+

```

