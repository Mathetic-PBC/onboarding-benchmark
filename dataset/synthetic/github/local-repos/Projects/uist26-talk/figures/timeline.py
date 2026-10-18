"""Slide 6: P07 session as a state strip, revealed in 4 steps (one SVG per step)."""
import pandas as pd
import matplotlib
matplotlib.rcParams["svg.fonttype"] = "none"
import matplotlib.pyplot as plt
from palette import STATE_COLORS

STEPS = [(0, 300, "first 5 minutes"), (0, 492, "first error"), (0, 1010, "the stall"), (0, 1320, "recovery")]


def strip(df, upto, path, caption):
    fig, ax = plt.subplots(figsize=(10, 1.4))
    for _, r in df[df.t0 < upto].iterrows():
        ax.barh(0, min(r.t1, upto) - r.t0, left=r.t0, color=STATE_COLORS[r.state], height=0.8)
    ax.set_xlim(0, 1320); ax.set_yticks([])
    ax.set_xticks(range(0, 1321, 300), [f"{m} min" for m in range(0, 23, 5)])
    ax.set_title(caption, loc="left", fontsize=12)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(path, transparent=True); plt.close(fig)


if __name__ == "__main__":
    df = pd.read_csv("data/p07_states.csv")  # columns: t0, t1 (seconds), state
    for i, (_, upto, cap) in enumerate(STEPS, 1):
        strip(df, upto, f"slides/img/p07_step{i}.svg", cap)
    print("wrote", len(STEPS), "frames")
