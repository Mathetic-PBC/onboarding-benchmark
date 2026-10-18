"""Place ChatGPT conversations read from the signed-in chatgpt.com account (STOPGAP, 2026-10-17) into authentic/chatgpt/.

_incoming/chatgpt/index/conversations.json   conversation list (2,360 rows, /backend-api/conversations paging)
_incoming/chatgpt/conversations/<id>.json    full conversation (/backend-api/conversation/<id>: mapping tree, all nodes)
Output: authentic/chatgpt/dbarron410@vt.edu/conversations/<id>.json (mtime = update_time) and _collection/conversations_index.json.
Conversations listed but not downloaded (all older than the 1-year scope; David chose to stop there) are written to _collection/not_collected.json.
"""
import datetime, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, set_mtime

ACCT = 'dbarron410@vt.edu'
INC = os.path.join(ROOT, '_incoming/chatgpt')
DST = os.path.join(ROOT, 'authentic/chatgpt', ACCT)


def ts(v):
    if isinstance(v, (int, float)): return float(v)
    return datetime.datetime.fromisoformat(v.replace('Z', '+00:00')).timestamp() if v else None


def iso(v):
    t = ts(v)
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).isoformat(timespec='seconds') if t else ''


idx = json.load(open(os.path.join(INC, 'index/conversations.json')))
m = Manifest('authentic', 'chatgpt')
os.makedirs(os.path.join(DST, 'conversations'), exist_ok=True)
os.makedirs(os.path.join(DST, '_collection'), exist_ok=True)
shutil.copyfile(os.path.join(INC, 'index/conversations.json'), os.path.join(DST, '_collection/conversations_index.json'))
m.add(f'{ACCT}/_collection/conversations_index.json', 'chatgpt', ACCT, '', notes=f'STOPGAP: conversation list from chatgpt.com, {len(idx)} conversations')
missing, n = [], 0
for c in idx:
    src = os.path.join(INC, 'conversations', c['id'] + '.json')
    if not os.path.exists(src):
        missing.append({k: c.get(k) for k in ('id', 'title', 'create_time', 'update_time', 'gizmo_id', 'is_archived')}); continue
    j = json.load(open(src))
    out = os.path.join(DST, 'conversations', c['id'] + '.json')
    shutil.copyfile(src, out)
    t = ts(j.get('update_time') or c.get('update_time'))
    if t: set_mtime(out, t)
    msgs = sum(1 for nd in (j.get('mapping') or {}).values() if ((nd.get('message') or {}).get('author') or {}).get('role') in ('user', 'assistant'))
    notes = [f'STOPGAP (signed-in web API, replace with official export)', f'title={j.get("title")!r}', f'created {iso(j.get("create_time"))}', f'{msgs} user/assistant nodes']
    if j.get('gizmo_id'): notes.append(f'custom GPT {j["gizmo_id"]}')
    if j.get('is_archived'): notes.append('archived')
    m.add(f'{ACCT}/conversations/{c["id"]}.json', 'chatgpt', ACCT, iso(j.get('update_time') or c.get('update_time')),
          source=f'https://chatgpt.com/c/{c["id"]}', notes='; '.join(notes))
    n += 1
json.dump(missing, open(os.path.join(DST, '_collection/not_collected.json'), 'w'), indent=1, ensure_ascii=False)
m.add(f'{ACCT}/_collection/not_collected.json', 'chatgpt', ACCT, '', notes=f'{len(missing)} listed conversations not downloaded: all last updated before 2025-10-17 (David chose to stop after the last year because of the rate limit)')
print('placed', n, 'missing', len(missing), 'rows', m.save())
