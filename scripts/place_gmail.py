"""Place Gmail raw messages (downloaded 2026-10-17 from mail.google.com 'Show original' view=att&disp=comp via the local
receiver) into authentic/gmail/<account>/threads/<thread>/<msg>.eml, mtime = Date header. The 499 files from the first,
crashed run (numeric thread dirs) are superseded by the second run and are not placed."""
import email.parser, email.utils, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, iso, set_mtime

ACCT = 'davidbarron410@gmail.com'
SRC = os.path.join(ROOT, '_incoming/gmail', ACCT)
DST = os.path.join(ROOT, 'authentic/gmail', ACCT)
idx = json.load(open(os.path.join(SRC, '_index/threads_v2.json')))
labels = {k.replace(':', '_'): v['q'] for k, v in idx.items()}
hp = email.parser.BytesHeaderParser()
m = Manifest('authentic', 'gmail')
os.makedirs(os.path.join(DST, '_collection'), exist_ok=True)
for f in os.listdir(os.path.join(SRC, '_index')):
    shutil.copy2(os.path.join(SRC, '_index', f), os.path.join(DST, '_collection', f))
    m.add(f'{ACCT}/_collection/{f}', 'gmail', ACCT, '', notes='collection index (thread/message ids and the Gmail views each was listed in)')


def clean(s):
    return ' '.join(str(s or '').split())[:150]


n = 0
for d in sorted(os.listdir(os.path.join(SRC, 'messages'))):
    if d.isdigit():
        continue
    latest = 0
    for f in sorted(os.listdir(os.path.join(SRC, 'messages', d))):
        src = os.path.join(SRC, 'messages', d, f)
        out = os.path.join(DST, 'threads', d, f)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(src, out)
        with open(src, 'rb') as fh:
            h = hp.parse(fh)
        try:
            ts = email.utils.parsedate_to_datetime(h['Date']).timestamp()
        except Exception:
            ts = os.stat(src).st_mtime
        set_mtime(out, ts); latest = max(latest, ts)
        q = labels.get(d, [])
        m.add(f'{ACCT}/threads/{d}/{f}', 'gmail', ACCT, iso(ts),
              notes=f'from={clean(h["From"])}; subject={clean(h["Subject"])}; listed in {",".join(q)}; attachments inline (MIME)')
        n += 1
    set_mtime(os.path.join(DST, 'threads', d), latest)
print(n, m.save())
