"""Place Granola meeting notes into authentic/granola/.

Granola's local store (~/Library/Application Support/Granola: granola.db, cache-v6.json.enc) is encrypted and the web app
is not signed in, so the notes collected are the public share pages linked from Slack and Linear (notes.granola.ai/d/<id>
and /t/<id>, which redirects to /d/<id>). Fetched read-only 2026-10-17 into _incoming/granola/share_pages/.
One file per distinct note (several links can point at the same note); mtime = the note's updated time embedded in the page.
"""
import datetime, html, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, set_mtime

INC = os.path.join(ROOT, '_incoming/granola/share_pages')
DST = os.path.join(ROOT, 'authentic/granola/shared-notes')
# link -> note id (from following the /t/ redirects)
REDIRECT = {'a445fd84-d9e9-411a-ad53-6635c9b8ce91': 'a7925251-70d6-4eb0-82c8-6c3ae2b938d4', 'ac3d1e9b-e1b9-4f56-9e2d-63ff2d32968b': 'e661d853-f0e6-4e7e-acee-00154772a17b',
            'b461e330-6796-464c-aa1e-aa60e49a7fc5': '7f0a46d2-9a73-4d55-abfa-3cecb613602d', 'dfbd1434-2b3c-4151-bc36-a856e52f8558': '496bb741-77fd-4ccb-ba6f-63f0a7fea61f',
            'e0df747c-a54d-491f-826a-96d4bbd4bce4': '6c06341d-afcb-46c2-9dd5-96480e5d7e1c', '3b94c852-c920-47f4-8cf0-9c7006d77c15': '810e02ca-6c31-4a51-a86e-c292cc2f6d54',
            '50ceea54-0a54-4963-9f61-f1fd2dda2d86': 'd41293cd-44d6-4677-a240-3595a4210cb0', '727414ce-66cd-4059-b591-341d4188e323': '7841d26b-56dc-48ad-a1a8-451259a7da86',
            '87caa162-8222-4ab7-a05d-54621cf42eda': '2445845a-7b11-4b4a-bced-86348c79a5b1'}
MON = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
REF = datetime.date(2026, 10, 17)


def where_linked(link_id):
    out = []
    for base in ('authentic/slack', 'authentic/linear'):
        for dp, _, fs in os.walk(os.path.join(ROOT, base)):
            for f in fs:
                if f.endswith(('.txt', '.json')) and f not in ('source_items.json',):
                    p = os.path.join(dp, f)
                    if link_id in open(p, errors='replace').read(): out.append(os.path.relpath(p, os.path.join(ROOT, 'authentic')))
    return sorted(set(out))


notes = {}
for f in sorted(os.listdir(INC)):
    kind, lid = f[:-5].split('_', 1)
    nid = lid if kind == 'd' else REDIRECT[lid]
    notes.setdefault(nid, []).append((kind, lid, f))

m = Manifest('authentic', 'granola')
os.makedirs(DST, exist_ok=True)
for nid, caps in sorted(notes.items()):
    caps.sort(key=lambda c: c[0])  # prefer the /d/ capture
    kind, lid, f = caps[0]
    raw = open(os.path.join(INC, f), encoding='utf-8', errors='replace').read()
    title = html.unescape(re.search(r'<title>([^<]*)</title>', raw).group(1)).strip()
    text = html.unescape(re.sub(r'<[^>]+>', '\n', re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', '', raw)))
    stamps = sorted(re.findall(r'20\d\d-\d\d-\d\dT[\d:.]+Z', raw))  # note created / updated, embedded in the page
    created, updated = (stamps[0], stamps[-1]) if stamps else (None, None)
    date = datetime.datetime.fromisoformat(updated.replace('Z', '+00:00')) if updated else None
    safe = re.sub(r'[/\\:]', '_', title)[:120]
    out = os.path.join(DST, f'{safe} [{nid[:8]}].html')
    shutil.copyfile(os.path.join(INC, f), out)
    if date: set_mtime(out, date.timestamp())
    links = [f'https://notes.granola.ai/{k}/{l}' for k, l, _ in caps]
    linked = sorted({p for _, l, _ in caps for p in where_linked(l)})
    m.add(os.path.relpath(out, os.path.join(ROOT, 'authentic/granola')), 'granola', 'Granola (Mathetic workspace, shared by Hudson Mitchell-Pullman)',
          updated or '', source=f'https://notes.granola.ai/d/{nid}',
          notes=f'public share page HTML (AI meeting notes; transcript not public); title={title!r}; links={links}; linked from {linked}'
                + (f'; created {created}' if created else '; no timestamps on page'))
    print(nid[:8], date, title[:60], len(caps))
print(m.save())
