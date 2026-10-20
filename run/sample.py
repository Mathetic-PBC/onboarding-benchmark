"""Fixed pilot sample, seed 17: up to 60 items per source (Gmail 300), split evenly between
authentic and synthetic, with any shortfall on one side filled from the other."""
import json, os, random, collections, sys

sys.path.insert(0, os.path.dirname(__file__))
from config import DATA, RUN
CAP = {'gmail': 300}

sandbox = {r['id']: r for r in json.load(open(os.path.join(RUN, 'sandbox/items.json')))}
prov = {r['id']: r['provenance'] for r in json.load(open(os.path.join(DATA, 'source_items.json'))) if r['id'] in sandbox}

rng = random.Random(17)
pools = collections.defaultdict(lambda: {'authentic': [], 'synthetic': []})
for iid in sorted(sandbox):
    pools[sandbox[iid]['source']][prov[iid]].append(iid)

chosen, report = [], {}
for src in sorted(pools):
    cap = CAP.get(src, 60)
    a, s = pools[src]['authentic'][:], pools[src]['synthetic'][:]
    rng.shuffle(a); rng.shuffle(s)
    half = cap // 2
    na = min(len(a), max(half, cap - len(s)))
    ns = min(len(s), cap - na)
    pick = sorted(a[:na] + s[:ns])
    chosen += pick
    report[src] = {'total': len(pick), 'authentic': na, 'synthetic': ns}

json.dump({'seed': 17, 'rule': 'per source: cap 60 (gmail 300), even authentic/synthetic split with spillover',
           'item_ids': sorted(chosen), 'per_source': {k: v['total'] for k, v in report.items()}},
          open(os.path.join(RUN, 'sample.json'), 'w'), indent=1)
json.dump(report, open(os.path.join(RUN, 'private/sample_provenance.json'), 'w'), indent=1)
print(len(chosen))
for k, v in report.items():
    print(f"{k:18} {v['total']:4}  (a {v['authentic']}, s {v['synthetic']})")
