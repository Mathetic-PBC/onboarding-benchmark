# Analysis plan

Type: Analysis
Status: Draft
Owner: David Barron
Created: February 22, 2026 10:15 PM
Last edited time: March 1, 2026 11:30 PM

## Primary

`log(time_to_fix) ~ condition + lab + (1 | student) + (1 | error_pattern)`

- unit = failed run (only the first failed run of each error episode)
- condition contrast: stall-triggered vs immediate (H2 vs H1); delay-90 vs stall-triggered (H3)

## Secondary

- Transfer: time-to-fix on the next failed run with the same error pattern, same model.
- Hint acceptance: logistic mixed model, `accepted ~ condition + (1 | student)`.
- Frustration: ordinal (1–5) per student per lab, `clmm`.

## Exclusions

- Episodes where a TA helped before any hint (from the tally sheet).
- Students with < 2 failed runs in a lab.
- Sessions with > 20% missing telemetry (reconnect drops).

## Things not to get wrong

- Any train/test style split (if we try predicting stalls) must be grouped by student.
- Pre-register on OSF before the first lab, even if it's a pilot.

## Expected tables

| Table | Content |
| --- | --- |
| 1 | descriptives by condition (n episodes, median time-to-fix, acceptance) |
| 2 | mixed model estimates, primary |
| 3 | transfer + frustration |
