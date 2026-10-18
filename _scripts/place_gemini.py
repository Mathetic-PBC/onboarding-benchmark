"""Place Gemini web chats (read via gemini.google.com batchexecute MaZiqc list + hNvQHb read, 2026-10-17) into authentic/gemini/<account>/."""
import json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, iso, set_mtime

INC = os.path.join(ROOT, '_incoming/gemini')
m = Manifest('authentic', 'gemini')
for acct in sorted(os.listdir(INC)):
    src = os.path.join(INC, acct)
    dst = os.path.join(ROOT, 'authentic/gemini', acct)
    idx = json.load(open(os.path.join(src, '_index/chats.json')))
    os.makedirs(os.path.join(dst, 'conversations'), exist_ok=True)
    os.makedirs(os.path.join(dst, '_collection'), exist_ok=True)
    shutil.copy2(os.path.join(src, '_index/chats.json'), os.path.join(dst, '_collection/chats_index.json'))
    m.add(f'{acct}/_collection/chats_index.json', 'gemini', acct, '', notes=f'chat list as returned by Gemini (MaZiqc), {len(idx)} chats')
    for c in idx:
        f = os.path.join(src, 'conversations', c['id'] + '.json')
        out = os.path.join(dst, 'conversations', c['id'] + '.json')
        if not os.path.exists(f):
            print('MISSING', acct, c['id']); continue
        shutil.copyfile(f, out)
        raw = open(f).read()
        secs = [int(s) for s in re.findall(r'\[(1[67]\d{8}),\s*\d+\]', raw)]
        ts = c['ts'][0]
        set_mtime(out, ts)
        first = iso(min(secs)) if secs else ''
        turns = raw.count('"r_')
        m.add(f'{acct}/conversations/{c["id"]}.json', 'gemini', acct, iso(ts),
              notes=f'title={c["title"]!r}; first turn {first}; ~{turns} response ids; raw batchexecute JSON (list_entry + hNvQHb read)')
print(m.save())
