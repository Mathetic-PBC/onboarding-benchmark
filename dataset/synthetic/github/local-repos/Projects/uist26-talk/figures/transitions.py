import pandas as pd
import matplotlib.pyplot as plt
from palette import STATE_COLORS

STATE_ORDER = list(STATE_COLORS)  # paper order; includes stalled-after-error


def draw(df, path):
    """Slide 8: state -> next-state flow, bar per source state."""
    nxt = df.assign(next=df.state.shift(-1)).dropna()
    counts = nxt.groupby(["state", "next"]).size().unstack(fill_value=0)
    order = [s for s in STATE_ORDER if s in counts.index]
    share = counts.loc[order].div(counts.loc[order].sum(axis=1), axis=0)
    ax = share.plot.barh(stacked=True, color=[STATE_COLORS.get(c, "#999999") for c in share.columns], figsize=(9, 4), width=0.8)
    ax.set_xlabel("share of next window"); ax.legend(bbox_to_anchor=(1, 1), fontsize=9, frameon=False)
    plt.tight_layout(); plt.savefig(path, transparent=True); plt.close()


if __name__ == "__main__":
    draw(pd.read_csv("data/p07_states.csv"), "slides/img/transitions.svg")
