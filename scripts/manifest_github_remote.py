"""Manifest rows for github.com mirror clones (+ .meta JSON) made by collect_github_remote.sh."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, iso, mtime

m = Manifest('authentic', 'github')
def meta_date(p):
    return json.load(open(os.path.join(p, 'repo.json'))).get('pushed_at') or ''

base = os.path.join(ROOT, 'authentic/github/github.com')
for owner in sorted(os.listdir(base)):
    od = os.path.join(base, owner)
    if not os.path.isdir(od): continue
    for e in sorted(os.listdir(od)):
        p = os.path.join(od, e)
        rel = os.path.relpath(p, os.path.join(ROOT, 'authentic/github'))
        if e.endswith('.git'):
            name = f'{owner}/{e[:-4]}'
            meta = json.load(open(os.path.join(od, e[:-4] + '.meta', 'repo.json')))
            last = subprocess.run(['git', '--git-dir', p, 'log', '--all', '-1', '--format=%cI'], capture_output=True, text=True).stdout.strip()
            n = subprocess.run(['git', '--git-dir', p, 'rev-list', '--all', '--count'], capture_output=True, text=True).stdout.strip()
            m.add(rel, 'github', 'divadbaroon', last or meta.get('pushed_at') or '', notes=f'git clone --mirror of github.com/{name}; private={meta.get("private")} fork={meta.get("fork")}; {n} commits; created {meta.get("created_at")}' + ('; empty repository' if n == '0' else ''))
        elif e.endswith('.meta'):
            for f in sorted(os.listdir(p)):
                fp = os.path.join(p, f)
                try: j = json.load(open(fp))
                except Exception: j = []
                recs = j if isinstance(j, list) else [j]
                k = len(recs)
                date = max((r.get('updated_at') or r.get('created_at') or '' for r in recs if isinstance(r, dict)), default='') or meta_date(p)
                m.add(os.path.join(rel, f), 'github', 'divadbaroon', date, notes=f'gh api read of {owner}/{e[:-5]} ({k} records)')
for f in sorted(os.listdir(os.path.join(ROOT, 'authentic/github/account'))):
    fp = os.path.join(ROOT, 'authentic/github/account', f)
    m.add(os.path.join('account', f), 'github', 'divadbaroon', mtime(fp), notes='gh api read of account (starred repos listed only, not cloned)')
m.save()
print('ok')
