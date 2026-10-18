"""Build _incoming/gdrive_gmail/meta.json (davidbarron410@gmail.com Drive selection) from the Drive web list views scraped
2026-10-17 (the Drive connector only covers dbarron410@vt.edu).

Views: listing/*.json (first pass: id+title), listing_dates.json (type:* / after: / shared-with-me with the 'Date modified'
or 'Shared by' column), window_listing.json (month windows after:X before:Y, PDF year windows, and the shared folder
'Investment Docs 🤬 Rise48 Equity'). Drive search returns a capped, varying window (~40-60 rows) for broad queries, so the
union of narrow windows is used. Dates are day-level ('Oct 5', 'Dec 7, 2025', '10:32 AM') as shown by Drive; owner is only
known for 'Shared with me' rows (the sharer) and for the Rise48 folder (shared by bentleycapital@gmail.com).
Selection = modified in the last year, or any PDF, or any Google-native file, or anything in Shared with me.
"""
import datetime, glob, json, os, re, sys

ROOT = os.path.expanduser('~/Desktop/benchmark/benchmark-data/_incoming/gdrive_gmail')
REF = datetime.date(2026, 10, 17)
CUT = datetime.date(2025, 10, 17)
FOLDER = 'folder:1aBPW2OKefbBtz6eR5bBZj0Spzg-cFJCW'
MON = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
EXT_MIME = {'pdf': 'application/pdf', 'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'mp4': 'video/mp4', 'mov': 'video/quicktime', 'wav': 'audio/wav',
            'mp3': 'audio/mpeg', 'zip': 'application/zip', 'rar': 'application/vnd.rar', 'flp': 'application/octet-stream', 'csv': 'text/csv'}
NATIVE = {'d': 'application/vnd.google-apps.document', 's': 'application/vnd.google-apps.spreadsheet', 'p': 'application/vnd.google-apps.presentation'}


def parse_date(parts):
    for x in parts:
        x = x.strip()
        m = re.match(r'^(\w{3}) (\d{1,2})(?:, (\d{4}))?$', x)
        if m and m.group(1) in MON:
            y = int(m.group(3)) if m.group(3) else REF.year
            d = datetime.date(y, MON[m.group(1)], int(m.group(2)))
            if not m.group(3) and d > REF: d = d.replace(year=y - 1)
            return d
        if re.match(r'^\d{1,2}:\d\d\s?[AP]M$', x):
            return REF
    return None


views = {}
for f in glob.glob(f'{ROOT}/listing/*.json'):
    views[os.path.basename(f)[:-5] + ' (pass 1)'] = [[r[0], [r[1]]] for r in json.load(open(f))['rows']]
for f in ('listing_dates.json', 'window_listing.json'):
    for k, v in json.load(open(f'{ROOT}/{f}')).items():
        views[k + ('' if f == 'window_listing.json' else ' (pass 2)')] = v['rows']
plan = json.load(open(f'{ROOT}/plan.json'))
natives = dict(plan['nat'])
for k, t in (('type:document (pass 2)', 'd'), ('type:presentation (pass 2)', 'p'), ('type:spreadsheet (pass 2)', 's')):
    for i, _ in views[k]: natives.setdefault(i, t)

ids = {}
for k, rows in views.items():
    for i, parts in rows:
        e = ids.setdefault(i, {'views': set(), 'title': None, 'date': None, 'sharer': None})
        e['views'].add(k)
        e['title'] = e['title'] or parts[0]
        if k.startswith('shared-with-me'):
            if len(parts) >= 3: e['sharer'] = parts[-2] if parts[-1].startswith('More actions') else parts[-1]
        else:
            d = parse_date(parts[1:])
            if d and not e['date']: e['date'] = d

meta = {}
for i, e in sorted(ids.items()):
    t = e['title'].strip()
    ext = t.rsplit('.', 1)[1].lower() if re.search(r'\.[A-Za-z0-9]{2,4}$', t) else ''
    if len(i) > 40 and natives.get(i) in NATIVE: mime = NATIVE[natives[i]]
    elif ext: mime = EXT_MIME.get(ext, 'application/octet-stream')
    else: mime = 'unknown (no extension; probably a folder)'
    shared = any(v.startswith('shared-with-me') for v in e['views'])
    why = []
    if e['date'] and e['date'] >= CUT: why.append('modified in last year')
    if mime == 'application/pdf': why.append('pdf, any age')
    if 'google-apps' in mime: why.append('google-native, any age')
    if shared: why.append('shared with me')
    if not why: continue
    owner = e['sharer'] if shared else ('bentleycapital@gmail.com' if FOLDER in e['views'] else 'davidbarron410@gmail.com')
    meta[i] = {'title': t, 'mime': mime, 'modified': (e['date'].isoformat() + 'T12:00:00Z') if e['date'] else None,
               'owner': owner, 'why': ', '.join(why), 'views': sorted(e['views']),
               'note': ('date is day-level from the Drive web list (time set to 12:00Z)' if e['date'] else 'no modified date shown (Shared with me view only)')
                       + ('; owner = sharer shown in Shared with me' if shared else '; owner not shown in Drive web list, assumed account owner' if owner == 'davidbarron410@gmail.com' else '; in shared folder Investment Docs 🤬 Rise48 Equity (third-party financial documents)')}
json.dump(meta, open(f'{ROOT}/meta.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print(len(ids), 'seen;', len(meta), 'selected;', Counter(m['mime'].split('/')[-1][:30] for m in meta.values()).most_common(12))
print('no date', sum(1 for m in meta.values() if not m['modified']))
