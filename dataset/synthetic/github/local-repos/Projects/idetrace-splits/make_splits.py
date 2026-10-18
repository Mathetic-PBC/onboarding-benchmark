"""Train/val/test splits of IDETrace 30-second windows.

v1 = random windows (used for the 2026-05-06 submission; leaks students across splits, kept for reproducibility).
v2 = grouped by student (2026-07-25): every window of a student is in exactly one split.
"""
import os, sys
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedGroupKFold


def window_split(win):
    tr, te = train_test_split(win, test_size=0.2, stratify=win.label, random_state=7)
    tr, va = train_test_split(tr, test_size=0.111, stratify=tr.label, random_state=7)
    return tr, va, te


def grouped_split(win, seed=7):
    """10 folds over students: 1 fold test, 1 fold val, 8 folds train (80/10/10 by students), stratified on the label mix."""
    folds = list(StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=seed).split(win, win.label, groups=win.student_id))
    te = win.iloc[folds[0][1]]
    va = win.iloc[folds[1][1]]
    tr = win.drop(te.index).drop(va.index)
    return tr, va, te


def main(version="v2", seed=7):
    seed = int(seed)
    win = pd.read_parquet("data/windows.parquet")[["window_id", "student_id", "label"]]
    # one student was logged under two spellings ("S118" and "s118 ") and was split across train/test
    win["student_id"] = win.student_id.str.strip().str.upper()
    tr, va, te = window_split(win) if version == "v1" else grouped_split(win, seed)
    out = f"splits/{version}" + ("" if seed == 7 else f"_seed{seed}")
    os.makedirs(out, exist_ok=True)
    for k, d in (("train", tr), ("val", va), ("test", te)):
        d.to_csv(f"{out}/{k}.csv", index=False)
    print(f"{version}: train {len(tr):,} windows / {tr.student_id.nunique()} students; val {len(va):,} / {va.student_id.nunique()}; "
          f"test {len(te):,} / {te.student_id.nunique()}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
