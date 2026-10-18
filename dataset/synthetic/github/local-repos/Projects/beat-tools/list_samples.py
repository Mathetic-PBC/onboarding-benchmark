"""Count samples per pack and rough kind (from the file name)."""
import collections, sys
from pathlib import Path

KINDS = ["kick", "snare", "clap", "hat", "perc", "808", "bass", "pad", "pluck", "lead", "vox", "fx", "loop"]

root = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "Music" / "Samples")
for pack in sorted(p for p in root.iterdir() if p.is_dir()):
    c = collections.Counter()
    for f in pack.rglob("*"):
        if f.suffix.lower() == ".wav":
            name = f.stem.lower()
            c[next((k for k in KINDS if k in name), "other")] += 1
    print(f"{pack.name:<28} {sum(c.values()):>5}  " + " ".join(f"{k}:{n}" for k, n in c.most_common(5)))
