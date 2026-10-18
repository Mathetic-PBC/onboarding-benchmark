# Kickoff — when should the hint appear?

Type: Plan
Status: Done
Owner: David Barron
Created: February 11, 2026 9:30 PM
Last edited time: February 12, 2026 10:05 AM

<aside>
❓ Question: in a CS1 lab, does it matter **when** an AI hint is offered — immediately on error, after a fixed delay, or only once the student looks stuck?

</aside>

## Why

- In our classroom telemetry, a lot of "stalled-after-error" windows are students who had an assistant open and didn't use it, and a lot of fast fixes are students who asked the assistant within seconds and pasted.
- Hints that arrive too early may short-circuit productive struggle; hints that arrive too late lose students for 10 minutes.
- Nobody has run the simple version: same hints, different timing, real lab.

## Hypotheses

- **H1** Immediate hints minimize time-to-fix for the current error but lower performance on the next similar error.
- **H2** Hints offered only after a detected stall give the best transfer (next-error time-to-fix) with acceptable frustration.
- **H3** A fixed 90 s delay is worse than stall-triggered on both, because it ignores whether the student is making progress.

## Conditions (draft)

| Condition | Rule |
| --- | --- |
| Immediate | hint button glows as soon as a run fails |
| Delay-90 | hint available 90 s after a failed run |
| Stall-triggered | hint offered when no successful run and idle > 45 s after a failed run |

## Measures

- time-to-fix after each failed run
- hint acceptance rate
- next-error time-to-fix on a similar error (transfer)
- self-reported frustration 1–5 at the end of lab
- one post-lab quiz item per lab

## Next

- [x] write up study design (separate page)
- [x] ask Yan if this can be a small side study this spring (yes, "if it stays small")
- [ ] find out which CS 1114 lab weeks are usable
