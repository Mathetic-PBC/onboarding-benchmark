"""Weekly training hours by sport from a Strava bulk export (activities.csv)."""
import sys
import pandas as pd
import matplotlib.pyplot as plt

SPORT = {"Run": "run", "Ride": "ride", "VirtualRide": "ride", "Workout": "elliptical", "Elliptical": "elliptical"}


def load(path="data/strava/activities.csv"):
    df = pd.read_csv(path)
    # the export repeats some headers; pandas suffixes the second copy with .1 (seconds / metres)
    df["date"] = pd.to_datetime(df["Activity Date"], format="%b %d, %Y, %I:%M:%S %p")
    df["sport"] = df["Activity Type"].map(SPORT).fillna("other")
    df["hours"] = df["Moving Time"] / 3600
    return df


def weekly(df, year=2026):
    d = df[df.date.dt.year == year]
    wk = d.groupby([pd.Grouper(key="date", freq="W-MON", label="left", closed="left"), "sport"]).hours.sum().unstack(fill_value=0)
    wk["total"] = wk.sum(axis=1)
    return wk.round(2)


if __name__ == "__main__":
    wk = weekly(load(*sys.argv[1:2]))
    print(wk.tail(12).to_string())
    ax = wk.drop(columns="total").plot.bar(stacked=True, figsize=(11, 4), width=0.85)
    ax.plot(range(len(wk)), wk["total"].rolling(4, min_periods=1).mean(), color="black", lw=1.2, label="4-wk avg")
    ax.axhspan(8, 11, color="green", alpha=0.08, label="8-11 h target")
    ax.set_xticklabels([d.strftime("%b %d") for d in wk.index], rotation=90, fontsize=7)
    ax.set_ylabel("hours"); ax.legend(fontsize=8)
    plt.tight_layout(); plt.savefig("weekly_hours.png", dpi=150)
    print("wrote weekly_hours.png")
