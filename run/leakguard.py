"""Answer-key leak patterns, used for the sandbox check and on every model input.

Reports counts only; never prints a matched project id.
  python3 -I leakguard.py <dir-or-file> ...
"""
import json, os, sys

DATA = os.path.expanduser('~/Desktop/benchmark/benchmark-data')  # no BENCH_RUN needed to scan


def patterns():
    ids = [r['id'] for r in json.load(open(os.path.join(DATA, 'ground_truth_projects.json')))]
    return {'ground_truth': [b'ground_truth'], 'HARD CASE': [b'HARD CASE'], 'PERSON.md': [b'PERSON.md'],
            'project_ids': [i.encode() for i in ids],
            # hidden source-item fields
            'modeled_on': [b'"modeled_on"'], 'collection_notes': [b'"collection_notes"']}


_P = None


def hits(data):
    """Number of matches per pattern group in a bytes/str payload."""
    global _P
    if _P is None:
        _P = patterns()
    if isinstance(data, str):
        data = data.encode('utf-8', 'replace')
    return {k: sum(data.count(p) for p in ps) for k, ps in _P.items()}


def scan(paths):
    total = {k: 0 for k in patterns()}
    files_hit = {k: 0 for k in total}
    n = 0
    for root in paths:
        walk = [(os.path.dirname(root), [], [os.path.basename(root)])] if os.path.isfile(root) else os.walk(root)
        for dp, _, fns in walk:
            for fn in fns:
                p = os.path.join(dp, fn)
                if os.path.islink(p):
                    continue
                n += 1
                if fn == 'PERSON.md':
                    files_hit['PERSON.md'] += 1
                with open(p, 'rb') as fh:
                    h = hits(fh.read())
                for k, v in h.items():
                    total[k] += v
                    files_hit[k] += bool(v)
    return n, total, files_hit


if __name__ == '__main__':
    n, total, files_hit = scan(sys.argv[1:])
    print(json.dumps({'files_scanned': n, 'match_counts': total, 'files_with_match': files_hit}, indent=1))
