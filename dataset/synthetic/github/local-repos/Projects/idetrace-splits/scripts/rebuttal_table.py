import json, glob

res = {}
for f in glob.glob("results/*.json"):
    for r in json.load(open(f)):
        if r["split"] in ("v1", "v2"):
            res[(r["model"], r["split"])] = r["macro_f1"]
names = {"majority": "Majority class", "gbm": "Gradient boosting", "bilstm": "BiLSTM"}
lines = [r"\begin{tabular}{lccc}", r"\toprule",
         r"Model & Submitted (window split) & \textbf{Corrected (student split)} & $\Delta$ \\", r"\midrule"]
for m in ("majority", "gbm", "bilstm"):
    a, b = res[(m, "v1")], res[(m, "v2")]
    lines.append(f"{names[m]} & {a:.2f} & {b:.2f} & {b - a:+.2f} \\\\")
lines += [r"\bottomrule", r"\end{tabular}"]
open("rebuttal/table_splits.tex", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
