"""IDETrace NeurIPS 2026 D&B rebuttal (Overleaf project, Jul 2026). PERSON.md §7: leakage bug found 2026-07-24 (same student's
windows in train and test), fixed with a split grouped by student id; macro-F1 0.81 -> 0.74; rebuttal posted 2026-07-29 reports
both numbers. Body in content/zotero/dsl.py markup; [[...]] is raw LaTeX. Also rendered to PDF by gen_pdfs."""

TITLE = 'IDETrace -- Author Response (NeurIPS 2026 Datasets & Benchmarks)'

BODY = '''
## General response to all reviewers
We thank the four reviewers. Before answering individual points we need to report a correction that affects the main results
table. While preparing the per-class analysis requested by Reviewer xT4q, we found that our evaluation split assigned thirty-second
windows to folds at random. Because each student contributes many windows, the same student appeared in both training and test folds.
This is a known form of leakage for educational sequence data [[\\citep{ferreira2023groupaware,kaufman2012leakage}]].

We re-ran every experiment with folds grouped by student id (5-fold GroupKFold; no student appears in more than one fold), and we also
hold out one full lab section as an additional test set. Corrected numbers are below. We report both because the original numbers are in
the submitted PDF, and we think reviewers should see the size of the change.

| Model (macro-F1) | Submitted (random split) | Corrected (grouped) | Held-out section |
| Majority class | 0.12 | 0.12 | 0.12 |
| Counts + logistic regression | 0.69 | 0.66 | 0.65 |
| Counts + gradient boosting | 0.77 | 0.71 | 0.70 |
| GRU over event sequence | 0.79 | 0.72 | 0.71 |
| IDETrace baseline (transformer) | 0.81 | 0.74 | 0.73 |

The ranking of models is unchanged; all models lose 3-7 points, and the transformer baseline drops from 0.81 to 0.74. A probe that
predicts the student id from the same features reaches 49% top-1 accuracy over 160 students (chance 0.6%), which explains why random
splits inflated results. The released splits (v1.1) are grouped by student, and the datasheet now states the split unit explicitly
[[\\citep{gebru2021datasheets}]].

## Reviewer xT4q (score 5)
Q1. Does macro-F1 hide minority classes? Yes, partly. Help-seeking is our smallest class (7.1% of windows). Per-class F1 on the
corrected split:

| Class | Share of windows | F1 (corrected) |
| Productive editing | 38.2% | 0.83 |
| Run-and-inspect | 24.5% | 0.79 |
| Stalled | 17.9% | 0.68 |
| Assistant help-seeking | 7.1% | 0.61 |
| Off-task / idle | 12.3% | 0.77 |

We will add this table and expected calibration error for the stalled class, which is the class a downstream intervention would
use [[\\citep{olsen2025macro}]]. The model is trained with class weights, so we will report calibration after temperature scaling
fit on held-out students.

Q2. Are the 160 students representative? They come from two terms of one university's CS1 (Fall 2025 and Spring 2026). We state
this as a limitation and do not claim population representativeness.

## Reviewer 9bPm (score 6)
Q1. Licensing and consent. Data were collected under an IRB-approved protocol with per-stream consent. Prompt text is released only for
students who opted in to its release (131 of 160); for the others we release derived features. The license prohibits re-identification
and linking with other data.

Q2. Logging gaps. One lab section lost events during a reconnect outage. Affected windows are flagged in the release (column
gap_flag) rather than silently dropped.

## Reviewer Lw2s (score 4)
Q1. Novelty relative to existing edit benchmarks. Existing benchmarks of novice edits do not include assistant interactions. IDETrace
pairs editor events with assistant prompts and responses at the same timestamp resolution, which is what makes help-seeking
prediction possible.

Q2. Leakage. We agree this was a serious problem, and we thank the reviewer for asking about the split in the original review. The
corrected protocol is described above and in the revised Section 5.

## Reviewer 2kDf (score 6)
Q1. Baseline tuning budget. All baselines received the same budget (40 trials of random search over documented ranges, selected on
grouped validation folds). Configurations are in the supplementary material.

## Summary of changes
- Corrected results with student-grouped splits; original numbers kept in a footnote for transparency.
- Per-class F1 and calibration for the stalled class.
- Datasheet updated: split unit, logging gaps, consent per stream.
- Released splits v1.1 grouped by student.
'''

REFS_BIB = r"""@article{ferreira2023groupaware,
  title   = {Group-Aware Splits for Educational Sequence Data: How Student Overlap Inflates Reported Accuracy},
  author  = {Ferreira, Ana and Kowalczyk, Piotr},
  journal = {Journal of Educational Data Mining},
  volume  = {15},
  number  = {2},
  pages   = {44--67},
  year    = {2023}
}

@article{kaufman2012leakage,
  title   = {Leakage in Data Mining: Formulation, Detection, and Avoidance},
  author  = {Kaufman, Shachar and Rosset, Saharon and Perlich, Claudia and Stitelman, Ori},
  journal = {ACM Transactions on Knowledge Discovery from Data},
  volume  = {6},
  number  = {4},
  pages   = {15:1--15:21},
  year    = {2012}
}

@article{gebru2021datasheets,
  title   = {Datasheets for Datasets},
  author  = {Gebru, Timnit and Morgenstern, Jamie and Vecchione, Briana and Vaughan, Jennifer Wortman and Wallach, Hanna and Daum{\'e} III, Hal and Crawford, Kate},
  journal = {Communications of the ACM},
  volume  = {64},
  number  = {12},
  pages   = {86--92},
  year    = {2021}
}

@inproceedings{olsen2025macro,
  title     = {Macro-F1 Is Not Enough: Calibration of Behavior Classifiers on Imbalanced Learning Logs},
  author    = {Olsen, Erik and Mahmoud, Layla},
  booktitle = {Artificial Intelligence in Education: 26th International Conference, AIED 2025},
  pages     = {318--331},
  year      = {2025}
}
"""

SPLIT_NOTES = r"""% scratch file: commands + numbers for the rebuttal table (not compiled)
% 2026-07-24  found it: make_splits.py used KFold over windows -> same student in train/test
% 2026-07-25  rerun with GroupKFold(n_splits=5) on student_id, seed 13
%   transformer 0.81 -> 0.74, GRU 0.79 -> 0.72, GB 0.77 -> 0.71, LR 0.69 -> 0.66
% 2026-07-26  held-out lab section (section 2, fall) as extra test: 0.73
% 2026-07-26  student-id probe (GB on same features, 160 students): top-1 0.49
% 2026-07-27  per-class table from corrected run (see table in rebuttal.tex)
% TODO after rebuttal: temperature scaling on grouped val folds; ECE for stalled
"""
