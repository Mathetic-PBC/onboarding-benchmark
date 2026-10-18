"""Heart-rate zones from max HR (196, field test Oct 2025)."""
MAX_HR = 196
BOUNDS = [(1, 0.0, 0.60), (2, 0.60, 0.70), (3, 0.70, 0.80), (4, 0.80, 0.90), (5, 0.90, 1.01)]


def zone(hr):
    f = hr / MAX_HR
    return next(z for z, lo, hi in BOUNDS if lo <= f < hi)


if __name__ == "__main__":
    for z, lo, hi in BOUNDS:
        print(f"Z{z}: {round(lo * MAX_HR)}-{round(min(hi, 1) * MAX_HR)} bpm")
