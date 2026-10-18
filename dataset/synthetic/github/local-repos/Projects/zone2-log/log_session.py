"""Append a session to data/log.csv: python log_session.py <sport> <minutes> <avg_hr> [notes] [--date YYYY-MM-DD]"""
import csv, sys
from datetime import date

SPORTS = {"run", "ride", "elliptical", "race"}


def main(argv):
    d = date.today().isoformat()
    if "--date" in argv:
        i = argv.index("--date"); d = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
    sport, minutes, hr, *notes = argv
    assert sport in SPORTS, f"sport must be one of {sorted(SPORTS)}"
    with open("data/log.csv", "a", newline="") as f:
        csv.writer(f).writerow([d, sport, int(minutes), int(hr), " ".join(notes)])
    print(f"logged {d} {sport} {minutes} min @ {hr}")


if __name__ == "__main__":
    main(sys.argv[1:])
