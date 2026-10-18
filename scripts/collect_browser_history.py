import os, sys, csv, sqlite3, shutil, json
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, copy, mtime
H = os.path.expanduser('~')
m = Manifest('authentic', 'browser-history')
CH = f'{H}/Library/Application Support/Google/Chrome'
info = json.load(open(f'{CH}/Local State'))['profile']['info_cache']
profiles = [(f'{CH}/{p}', f'chrome/{p}', 'Google Chrome', f'profile "{p}" ({info[p].get("name")}; {info[p].get("user_name") or "not signed in"})') for p in ['Default', 'Profile 1', 'Profile 2']]
profiles.append((f'{H}/Library/Application Support/Codex/Default', 'codex-app-browser/Default', 'Codex app built-in browser', 'Codex app Default profile'))
EPOCH = 11644473600
for src, rel, tool, acct in profiles:
    for name in ['History', 'Bookmarks', 'Top Sites']:
        s = f'{src}/{name}'
        if not os.path.exists(s): continue
        d = f'{m.dir}/{rel}/{name}'
        copy(s, d)
        m.add(f'{rel}/{name}', tool, acct, mtime(s), source='~/' + os.path.relpath(s, H), notes='native Chrome ' + ('SQLite history DB' if name == 'History' else name))
    # readable export of every visit (derived from the History copy)
    hp = f'{m.dir}/{rel}/History'
    if os.path.exists(hp):
        tmp = hp + '.tmpcopy'; shutil.copy(hp, tmp)
        con = sqlite3.connect(tmp)
        rows = con.execute(f"select datetime(v.visit_time/1000000-{EPOCH},'unixepoch','localtime'), u.url, u.title, v.transition & 255 from visits v join urls u on u.id=v.url order by v.visit_time").fetchall()
        con.close(); os.remove(tmp)
        out = f'{m.dir}/{rel}/visits.csv'
        with open(out, 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['visit_time_local', 'url', 'title', 'transition_core']); w.writerows(rows)
        m.add(f'{rel}/visits.csv', tool, acct, rows[-1][0] if rows else '', source='derived from History copy',
              notes=f'derived readable export: {len(rows)} visits, {rows[0][0] if rows else ""} → {rows[-1][0] if rows else ""}')
        print(rel, len(rows), rows[0][0] if rows else '', rows[-1][0] if rows else '')
    bp = f'{m.dir}/{rel}/Bookmarks'
    if os.path.exists(bp):
        def walk(n, path):
            if n.get('type') == 'url': yield [path, n.get('name'), n.get('url'), n.get('date_added')]
            for c in n.get('children', []): yield from walk(c, path + '/' + n.get('name', ''))
        b = json.load(open(bp)); rows = [r for k, root in b['roots'].items() if isinstance(root, dict) for r in walk(root, '')]
        print(rel, 'bookmarks', len(rows))
print(m.save())
