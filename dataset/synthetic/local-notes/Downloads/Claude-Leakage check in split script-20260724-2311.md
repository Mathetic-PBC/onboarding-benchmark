# Leakage check in split script

**Exported:** 2026-07-24 23:11

---

**User:**
ok so be concise. macro-F1 on IDETrace is 0.81 and that feels too good for the stalled class. here's make_splits.py, does anything
leak?

```python
train, test = train_test_split(windows, test_size=0.2, random_state=7, stratify=windows.label)
```

**Assistant:**
Yes. You split at the window level, so windows from the same student (often consecutive 30 s windows from one session) land in both
train and test. The model can memorize per-student patterns. Use a grouped split:

```python
from sklearn.model_selection import GroupShuffleSplit
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=7)
train_idx, test_idx = next(gss.split(windows, windows.label, groups=windows.student_id))
```

Then check `set(train.student_id) & set(test.student_id)` is empty. Expect the score to drop.

**User:**
38 students overlapped in fold 1. reran grouped: 0.74. ugh. ok that's the real number. rebuttal reports both

**Assistant:**
Reporting both, with the grouped split as the default going forward, is the right call.
