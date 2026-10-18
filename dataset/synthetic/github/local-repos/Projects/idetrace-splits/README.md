# idetrace-splits

Split and baseline scripts for the IDETrace dataset (NeurIPS 2026 Datasets & Benchmarks submission).

```
python make_splits.py v1         # submission split (random windows; leaks students)
python make_splits.py v2 [seed]  # grouped by student (use this)
python train.py --model gbm --split v1
```

Data (`data/windows.parquet`) and generated splits are not committed.

## v1 vs v2 (macro-F1)

| model | v1 (window split, submitted) | v2 (grouped by student) |
|---|---|---|
| majority | 0.21 | 0.21 |
| GBM | 0.81 | 0.74 (±0.01 over 5 seeds) |
| BiLSTM | 0.79 | 0.72 |

The NeurIPS rebuttal (2026-07-29) reports both. v1 is kept only to reproduce the submitted numbers.
