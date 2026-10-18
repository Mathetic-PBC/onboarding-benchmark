---
tags: [idetrace, neurips, bug]
created: 2026-07-24
updated: 2026-07-30
---
# IDETrace: the leakage bug

## what happened
- 07-24, while answering reviewer 2's "why is your baseline so strong" I re-ran the split script and printed student ids per
  fold. **same student ids in train and test.** windows were split randomly, so a student's 30-second windows from the same
  session landed on both sides
- the model was partly learning the student (typing rhythm, variable names), not the state

## fix
- split grouped by student id (`GroupKFold`, 5 folds, groups=student_id), stratification checked by hand afterward
- re-ran everything: baselines, the main model, the ablations. took two nights on the lab box
- macro-F1 **0.81 → 0.74**. per-class: stalled-after-error took the biggest hit, off-task barely moved
- the gap between the two numbers is itself evidence that student identity leaks through telemetry. that's actually a finding
  for the privacy paragraph

## rebuttal wording (posted 07-29)
- report both numbers, say plainly that the original split leaked, thank the reviewer for the question that made us look
- updated table goes in the revision; dataset card gets a "recommended splits" section with the grouped split as the only
  official one
- Yan's edit: lead with the corrected number, not the old one

## lessons
- [[Ostrowski2025 - Productive Struggle]] already reported a no-leak number. we read that paper and still did it
- add a test: assert no group overlap across folds. it's three lines
- full notebook with plots is in OneNote (IDETrace notebook), this is the summary
