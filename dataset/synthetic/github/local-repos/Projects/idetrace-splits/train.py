"""Train a baseline on a split and write results/<model>_<split>.json."""
import argparse, json, os
import numpy as np
import pandas as pd
import yaml
from sklearn.metrics import f1_score

from models import make_model, FEATURES


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=["majority", "gbm", "bilstm"])
    ap.add_argument("--split", default="v1")
    ap.add_argument("--config", default="configs/baselines.yaml")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))[a.model] or {}
    feats = pd.read_parquet("data/windows.parquet").set_index("window_id")
    load = lambda k: feats.loc[pd.read_csv(f"splits/{a.split}/{k}.csv").window_id]
    tr, te = load("train"), load("test")
    m = make_model(a.model, **cfg).fit(tr[FEATURES], tr.label)
    f1 = f1_score(te.label, m.predict(te[FEATURES]), average="macro")
    os.makedirs("results", exist_ok=True)
    path = f"results/{a.model}_{a.split}.json"
    json.dump([{"model": a.model, "split": a.split, "macro_f1": round(float(f1), 2)}], open(path, "w"))
    print(f"{a.model:<9} split={a.split}  macro-F1={f1:.2f}")


if __name__ == "__main__":
    main()
