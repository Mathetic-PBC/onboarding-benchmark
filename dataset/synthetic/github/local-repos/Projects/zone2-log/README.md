# zone2-log

Personal training log for the multi-year aerobic base plan (mostly Zone 2 running, cycling and elliptical).

- `data/log.csv`: one row per session (date, sport, minutes, avg HR, notes)
- `log_session.py`: append a session, e.g. `python log_session.py run 62 137 "easy loop"`
- `hr_zones.py`: zones from max HR 196
- `data/plan_block*.csv`: block plans (weekly hour targets)
- `weekly_hours.py`: weekly hours by sport from a Strava bulk export (`data/strava/activities.csv`, not committed), with the 8–11 h band and a 4-week rolling mean
- `decoupling.py`: aerobic decoupling (Pa:HR drift, first vs second half) for runs ≥ 75 min from per-second streams (`data/streams/`, not committed). Under 5% = base is fine
- `race/`: race notes
