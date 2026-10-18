"""Normalize sample file names: <kind>_<descriptor>_<nn>[_<key>][_<bpm>].wav (dry run unless --apply)."""
import argparse, csv, re
from pathlib import Path

KINDS = ["kick", "snare", "clap", "hat", "perc", "bass", "keys", "pluck", "pad", "lead", "vox", "fx", "loop"]
ALIAS = {"rhodes": "keys", "piano": "keys", "ep": "keys", "hihat": "hat", "hh": "hat", "808": "bass", "vocal": "vox", "sfx": "fx", "shaker": "perc", "rim": "perc"}
KEY = re.compile(r"(?<![a-z])([a-g](?:#|b)?(?:m|min|maj)?)(?![a-z])", re.I)
BPM = re.compile(r"(?<!\d)(\d{2,3})\s*(?:bpm)?(?!\d)", re.I)
VENDOR = re.compile(r"^(kshmr|cymatics|splice|unison)\s*(vol\s*\d+)?\s*[-_ ]*", re.I)


def parse(stem):
    s = VENDOR.sub("", stem.lower())
    s = re.sub(r"[()\[\]]", " ", s)
    toks = [t for t in re.split(r"[\s_\-]+", s) if t]
    kind = next((ALIAS.get(t, t) for t in toks if ALIAS.get(t, t) in KINDS), "fx")
    bpm = next((int(m.group(1)) for t in toks if (m := BPM.fullmatch(t)) and 60 <= int(m.group(1)) <= 200), None)
    key = next((t.lower().replace("min", "m") for t in toks if KEY.fullmatch(t) and t.lower() not in ("a", "b")), None)
    num = next((int(t) for t in toks if t.isdigit() and int(t) != bpm and len(t) <= 2), 1)
    desc = [t for t in toks if t not in KINDS and t not in ALIAS and not t.isdigit() and t not in ("loop", "bpm") and t != key]
    return kind, "-".join(desc[:2]) or "x", num, key, bpm


def new_name(path, detect=False):
    kind, desc, num, key, bpm = parse(path.stem)
    if detect and bpm is None:
        from .bpm import estimate
        bpm = estimate(path)
    parts = [kind, desc, f"{num:02d}"] + ([key] if key else []) + ([str(bpm)] if bpm else [])
    return "_".join(parts) + ".wav"


def undo(log):
    """Rename files back using the old,new pairs in the log (newest first)."""
    pairs = list(csv.reader(open(log)))
    for old, new in reversed(pairs):
        if Path(new).exists() and not Path(old).exists():
            Path(new).rename(old)
    print(f"restored {len(pairs)} files")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--detect-bpm", action="store_true", help="estimate BPM for loops without one in the name")
    ap.add_argument("--log", default="rename_log.csv")
    ap.add_argument("--undo", action="store_true", help="restore names from --log")
    a = ap.parse_args()
    if a.undo:
        return undo(a.log)
    rows = []
    for p in sorted(a.root.rglob("*")):
        if p.suffix.lower() != ".wav":
            continue
        q = p.with_name(new_name(p, detect=a.detect_bpm))
        if q.name == p.name:
            continue
        taken = {r[1] for r in rows}
        n = 2
        while q.exists() or str(q) in taken:  # two samples normalizing to one name used to overwrite each other
            kind, desc, *rest = q.stem.split("_")
            q = q.with_name("_".join([kind, desc, f"{n:02d}"] + rest[1:]) + q.suffix); n += 1
        rows.append((str(p), str(q)))
        print(f"{p.name}  ->  {q.name}")
        if a.apply:
            p.rename(q)
    with open(a.log, "a", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"{len(rows)} files {'renamed' if a.apply else 'would be renamed (dry run)'}")


if __name__ == "__main__":
    main()
