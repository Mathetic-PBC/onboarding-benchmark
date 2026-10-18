"""Aerobic decoupling (Pa:HR drift) for long runs: (EF first half - EF second half) / EF first half."""
import json
from pathlib import Path
import pandas as pd
from weekly_hours import load


def decoupling(stream, warmup_s=600):
    t, hr, v = stream["time"], stream["heartrate"], stream["velocity_smooth"]
    pts = [(ti, h, vi) for ti, h, vi in zip(t, hr, v) if ti >= warmup_s and h and vi > 1.5]  # drop warm-up and stops
    if len(pts) < 1200:
        return None
    mid = len(pts) // 2
    ef = lambda seg: sum(p[2] for p in seg) / sum(p[1] for p in seg)  # speed per beat
    a, b = ef(pts[:mid]), ef(pts[mid:])
    return round(100 * (a - b) / a, 1)


if __name__ == "__main__":
    acts = load()
    runs = acts[(acts.sport == "run") & (acts["Moving Time"] >= 75 * 60)]
    rows = []
    for _, r in runs.iterrows():
        f = Path(f"data/streams/{r['Activity ID']}.json")
        if f.exists():
            d = decoupling(json.load(open(f)))
            if d is not None:
                rows.append({"date": r.date.date(), "name": r["Activity Name"], "min": round(r["Moving Time"] / 60), "decoupling_%": d})
    out = pd.DataFrame(rows).sort_values("date")
    out["ok"] = out["decoupling_%"] < 5
    print(out.to_string(index=False))
