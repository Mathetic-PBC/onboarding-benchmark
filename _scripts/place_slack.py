"""Place Slack (workspace Mathetic) from verbatim Slack MCP results (read-only; collected 2026-10-17 by a subagent).
The connector returns rendered text, not Slack's export JSON, so each conversation keeps the raw pages (history.txt,
threads/*.txt) plus a parsed messages.json in Slack-export-like shape."""
import json, os, re, shutil, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, iso, set_mtime

OUT = os.path.join(ROOT, 'authentic/slack/Mathetic')
ACCT = 'Mathetic Slack workspace (David Barron, david@papertlab.org)'
m = Manifest('authentic', 'slack')
SAVED = re.compile(r'saved to:? (/\S+?\.(?:json|txt|pdf|png|jpg|jpeg|gif|mp4|bin|webp|docx|pptx|xlsx|csv|zip|mov))\b')


def resolve(text):
    """Return (kind, payload): ('text', str) or ('blob', path)."""
    s = SAVED.search(text[:1500])
    if s and ('Output too large' in text[:300] or 'exceeds maximum' in text[:300]):
        p = s.group(1)
        raw = open(p).read()
        if p.endswith('.json'):
            try:
                raw = ''.join(x.get('text', '') for x in json.loads(raw))
            except Exception:
                pass
        return 'text', raw
    return 'text', text


def body(text):
    try:
        j = json.loads(text)
        return j.get('messages') or j.get('result') or text, j
    except Exception:
        return text, {}


MSG = re.compile(r'=== Message from (.*?) \((\w+)\) at (.*?) === \nMessage TS: ([\d.]+)\n(.*?)(?=\n\n=== Message from |\Z)', re.S)


def write(rel, data, ts=None, notes='', binary=False):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if binary:
        shutil.copyfile(data, p)
    else:
        open(p, 'w').write(data if isinstance(data, str) else json.dumps(data, indent=2, ensure_ascii=False))
    if ts: set_mtime(p, ts)
    m.add('Mathetic/' + rel, 'slack', ACCT, iso(ts) if ts else '', notes=notes)


calls = [json.loads(l) for l in open(os.path.join(ROOT, '_incoming/slack_calls.jsonl'))]
lst = next(c for c in calls if c['tool'].endswith('list_user_channels'))
names = dict((i, n) for n, i in re.findall(r'### (.+?)\n- \*\*ID:\*\* (\w+)', body(lst['result'])[0]))
write('conversations.md', body(lst['result'])[0], None, f'conversation list from the connector ({len(names)} conversations)')

pages, threads = {}, {}
for c in calls:
    t = c['tool'].split('__')[-1]
    if t == 'slack_read_channel' and not c['is_error']:
        pages.setdefault(c['input']['channel_id'], []).append(body(resolve(c['result'])[1])[0])
    if t == 'slack_read_thread' and not c['is_error']:
        threads.setdefault(c['input']['channel_id'], {}).setdefault(c['input']['message_ts'], []).append(body(resolve(c['result'])[1])[0])
for cid, name in names.items():
    safe = re.sub(r'[^\w.-]+', '_', name.strip('#')) + '__' + cid
    raw = '\n\n'.join(pages.get(cid, []))
    msgs = [dict(ts=ts, user=uid, user_name=who, datetime=when, text=txt.strip()) for who, uid, when, ts, txt in MSG.findall(raw)]
    msgs = sorted({x['ts']: x for x in msgs}.values(), key=lambda x: float(x['ts']))
    last = float(msgs[-1]['ts']) if msgs else None
    write(f'{safe}/history.txt', raw, last, f'{name}: {len(msgs)} messages, raw connector pages (newest first)')
    write(f'{safe}/messages.json', msgs, last, f'{name}: {len(msgs)} messages parsed from history.txt, oldest first')
    for ts, parts in threads.get(cid, {}).items():
        write(f'{safe}/threads/{ts}.txt', '\n\n'.join(parts), float(ts), f'{name}: thread under message {ts}')

for c in calls:
    t = c['tool'].split('__')[-1]
    if t == 'slack_read_user_profile':
        write(f'users/{c["input"]["user_id"]}.txt', body(c['result'])[0], None, 'user profile via connector')
    if t != 'slack_read_file':
        continue
    fid, r = c['input']['file_id'], c['result']
    if c['is_error'] or r.startswith('execution_failed'):
        continue
    if 'exceeds maximum' in r[:300]:
        r = resolve(r)[1]
    title = (re.search(r'Title: (.*)', r) or [None, fid])[1].strip()
    created = re.search(r'Created: (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)', r)
    ts = datetime.datetime.strptime(created.group(1), '%Y-%m-%d %H:%M:%S').timestamp() if created else None
    blob = re.search(r'(?:saved to|source:) (/\S+?mcp-claude_ai_Slack-blob-\S+?\.\w+)', r)
    safe = re.sub(r'[^\w.-]+', '_', title)[:80]
    if blob and os.path.exists(blob.group(1)):
        ext = os.path.splitext(blob.group(1))[1]
        name = safe if safe.lower().endswith(ext) else safe + ext
        write(f'files/{fid}__{name}', blob.group(1), ts, f'Slack file {title!r} (binary as returned by connector)', binary=True)
    else:
        write(f'files/{fid}__{safe}.txt', r, ts, f'Slack file {title!r}: text as rendered by the connector (original binary not returned)')
print(m.save())
