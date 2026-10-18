"""Place Outlook (Microsoft 365, dbarron410@vt.edu) mail read from outlook.cloud.microsoft into authentic/outlook/.

Read 2026-10-18 in the signed-in browser, read-only: each message was selected in the list and saved with Outlook's own
File > Download > Download as EML; the page script caught the file in memory instead of a browser download.
_incoming/outlook_web/msgs/<hash>.eml   one raw message (hash = sha256(Message-ID)[:16]; a message seen in several folders is kept once)
_incoming/outlook_web/index_run<n>.json {byMid: {hash: {folders, mid, date, list_date, label, filename, size, child, note}}, skippedUnread, fail, log}
Output: authentic/outlook/dbarron410@vt.edu/threads/<conversation>/<yyyymmdd-hhmmss>_<hash>.eml (mtime = Date header),
grouped by conversation (first 22 bytes of the Thread-Index header, like Outlook's conversation id), and
dbarron410@vt.edu/_collection/{mail_index.json, not_collected.json}.
"""
import base64, email.utils, hashlib, json, os, re, shutil, sys
from email.parser import BytesHeaderParser
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, set_mtime

ACCT = 'dbarron410@vt.edu'
INC = os.path.join(ROOT, '_incoming/outlook_web')
DST = os.path.join(ROOT, 'authentic/outlook', ACCT)
hp = BytesHeaderParser()

import glob
idx = {'byMid': {}, 'skippedUnread': [], 'fail': [], 'log': [], 'seenAgain': {}}
for f in sorted(glob.glob(os.path.join(INC, 'index_run*.json'))):  # one index per browser run; later runs only add messages
    j = json.load(open(f))
    for k, v in j['byMid'].items(): idx['byMid'].setdefault(k, v)
    for k in ('skippedUnread', 'fail', 'log'): idx[k] += j.get(k, [])
    for k, fs in j.get('seenAgain', {}).items(): idx['seenAgain'].setdefault(k, []).extend(fs)
for k, fs in idx['seenAgain'].items():  # same message reached again from another folder / conversation
    if k in idx['byMid']: idx['byMid'][k]['folders'] = sorted(set(idx['byMid'][k]['folders']) | set(fs))
m = Manifest('authentic', 'outlook')
m.rows = {k: v for k, v in m.rows.items() if not k.startswith(ACCT + '/')}
if os.path.isdir(os.path.join(DST, 'threads')): shutil.rmtree(os.path.join(DST, 'threads'))  # our own copies; rebuilt each run
os.makedirs(os.path.join(DST, '_collection'), exist_ok=True)
n, convs, missing = 0, set(), []
for hk, e in sorted(idx['byMid'].items()):
    src = os.path.join(INC, 'msgs', hk + '.eml')
    if not os.path.exists(src):
        missing.append({'hash': hk, **e, 'reason': 'listed but no file received'}); continue
    with open(src, 'rb') as f: h = hp.parse(f)
    ti = (h['Thread-Index'] or '').strip()
    try: conv = base64.b64decode(ti + '=' * (-len(ti) % 4))[:22].hex() if ti else None
    except Exception: conv = None
    conv = conv or 'single-' + hk
    try: dt = email.utils.parsedate_to_datetime(h['Date'])
    except Exception: dt = None
    name = (dt.strftime('%Y%m%d-%H%M%S') if dt else 'nodate') + f'_{hk}.eml'
    out = os.path.join(DST, 'threads', conv, name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copyfile(src, out)
    if dt: set_mtime(out, dt.timestamp())
    convs.add(conv); n += 1
    notes = [f'Outlook web "Download as EML"', f'folders {",".join(e["folders"])}', f'subject={(h["Subject"] or "")[:120]!r}']
    if e.get('note'): notes.append(e['note'])
    m.add(os.path.relpath(out, os.path.join(ROOT, 'authentic/outlook')), 'Outlook on the web (Microsoft 365)', ACCT,
          dt.isoformat() if dt else '', source=f'Message-ID {e.get("mid")}', notes='; '.join(notes))
json.dump(idx, open(os.path.join(DST, '_collection/mail_index.json'), 'w'), indent=1, ensure_ascii=False)
nc = {'not_downloaded': missing, 'skipped_unread': idx.get('skippedUnread', []), 'failed': idx.get('fail', [])}
json.dump(nc, open(os.path.join(DST, '_collection/not_collected.json'), 'w'), indent=1, ensure_ascii=False)
m.add(f'{ACCT}/_collection/mail_index.json', 'Outlook on the web (Microsoft 365)', ACCT, '', notes='per-message index: folders, list date, list label, Message-ID; plus the per-folder run log')
m.add(f'{ACCT}/_collection/not_collected.json', 'Outlook on the web (Microsoft 365)', ACCT, '',
      notes=f'{len(missing)} not downloaded, {len(nc["skipped_unread"])} unread skipped (opening would mark them read), {len(nc["failed"])} failures')
print('placed', n, 'messages in', len(convs), 'conversations; missing', len(missing), 'unread skipped', len(nc['skipped_unread']),
      'failed', len(nc['failed']), 'rows', m.save())
