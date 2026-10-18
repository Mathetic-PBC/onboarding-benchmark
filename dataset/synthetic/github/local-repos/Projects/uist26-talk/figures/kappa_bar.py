"""Slide 7: kappa per state (one-vs-rest Fleiss), same numbers as the paper."""
import matplotlib
matplotlib.rcParams["svg.fonttype"] = "none"
import matplotlib.pyplot as plt
from palette import STATE_COLORS

KAPPA = {"productive": 0.74, "exploring": 0.66, "help-seeking": 0.79, "stalled": 0.61, "stalled-after-error": 0.58, "off-task": 0.84}


def draw(path="../slides/img/kappa_by_state.svg"):
    fig, ax = plt.subplots(figsize=(9, 3.6))
    states = [s for s in STATE_COLORS if s in KAPPA]
    ax.bar(states, [KAPPA[s] for s in states], color=[STATE_COLORS[s] for s in states])
    ax.axhline(0.71, ls="--", lw=1, color="k"); ax.text(len(states) - 0.5, 0.72, "overall 0.71", ha="right", fontsize=11)
    ax.set_ylim(0, 1); ax.set_ylabel("κ")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(path, transparent=True); plt.close(fig)


if __name__ == "__main__":
    draw()
