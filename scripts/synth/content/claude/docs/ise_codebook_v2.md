# Codebook v2 — Frustration signals (2026-03-06)

Unit: student turn. Multiple codes allowed. Coders read the whole session.

Blocked goal
- REPEAT — same or near-same request resent after an answer, adding NO new information (no new error, code, or constraint). New traceback = not REPEAT. (changed in v2)
- TERSE-DROP — sharp drop in turn length after longer turns, with no new information.
- GIVE-UP — quits, or asks for the answer outright ("just give me the code").
- DEFLECT — changes topic away from an unresolved error.

Negative valence
- NEG-EVAL — negative judgment of the tutor or task.
- SELF-NEG — negative statement about own ability.
- INTENSITY — caps, repeated punctuation, expletives (not inside code).

Session rule: frustrated = >=1 blocked-goal code and >=1 valence code within any 5 consecutive student turns.
Also report: blocked-goal-only sessions, valence-only sessions.

Agreement (pilot, 60 sessions, David & Maya): kappa = 0.62. Three raters on 30 sessions: Fleiss kappa = 0.58.
Borderline examples: see sessions 017 and 044 in the shared sheet.
