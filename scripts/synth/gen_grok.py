"""Synthetic Grok conversations (grok.com conversation export shape, one JSON per conversation) for the X account
@dbarron_runs (signed up with david.barron.runs@gmail.com, Feb 2026). No real Grok data exists; the shape follows the
documented grok.com export: {"conversation": {...}, "responses": [...]}.

Content: _scripts/synth/content/grok/*.txt (CHATFMT). Inside an @assistant block, trailing lines
  [src] title | url | preview     -> webSearchResults
  [x] <anything>                  -> xPostIds (a snowflake id derived from the message time)
are stripped from the message text.
Layout: synthetic/grok/@dbarron_runs/conversations/<conversationId>.json
"""
import os, sys, re, glob, random, datetime
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

# ---------------------------------------------------------------- CHATFMT (shared text format for hand-written chats)
# A content file holds many conversations:
#   ### CONV <slug>
#   title: <title>                      start: 2026-03-27 23:10 | auto | auto 2026-03-01 2026-04-15   (local time, see synthlib.dt)
#   projects: project_x, project_y      notes: <hidden label note>    <any other key>: <value>
#   ---
#   @user                     (first message at `start`)
#   text ...
#   @assistant                (reply a few seconds later)
#   text ...
#   @user +3h | +2d | +45m    (gap since previous message) | @user 2026-03-28 09:10 (absolute) | key=value modifiers
# Message bodies are verbatim (markdown, code, pasted logs). Without a modifier a user turn follows the previous message
# after a reading/typing pause; an assistant turn follows after a few seconds.
CONTENT = os.path.join(os.path.dirname(__file__), 'content')


def parse_chats(path):
    convs, cur, msg, head = [], None, None, False
    for raw in open(path, encoding='utf-8').read().split('\n'):
        if raw.startswith('### CONV '):
            cur = {'slug': raw[9:].strip(), 'meta': {}, 'msgs': []}; convs.append(cur); msg = None; head = True; continue
        if cur is None: continue
        if head:
            if raw.strip() == '---': head = False
            elif ':' in raw:
                k, v = raw.split(':', 1); cur['meta'][k.strip()] = v.strip()
            continue
        m = re.match(r'^@(user|assistant)(?![\w])(.*)$', raw)
        if m:
            msg = {'role': m.group(1), 'mods': m.group(2).strip(), 'lines': []}; cur['msgs'].append(msg); continue
        if msg is not None: msg['lines'].append(raw)
    for c in convs:
        for m in c['msgs']:
            m['text'] = '\n'.join(m.pop('lines')).strip('\n')
        c['projects'] = [p.strip() for p in c['meta'].get('projects', 'project_none').split(',') if p.strip()]
    return convs


def _delta(tok):
    n, u = int(tok[1:-1]), tok[-1]
    return datetime.timedelta(**{{'m': 'minutes', 'h': 'hours', 'd': 'days', 's': 'seconds'}[u]: n})


assert _delta('+2h') == datetime.timedelta(hours=2)


def timeline(c, seed):
    """Give every message an aware datetime ('at') and key=value modifiers ('kv'). Returns (first, last)."""
    rnd = random.Random(f'{seed}|{c["slug"]}')
    s = c['meta'].get('start', 'auto')
    if s.startswith('auto'):
        parts = s.split()[1:]
        lo = parts[0] if len(parts) > 0 else None
        hi = (parts[1] + ' 23:59') if len(parts) > 1 else None
        t = bursty_dates(1, f'{seed}|{c["slug"]}', start=lo, end=hi)[0]
    else:
        t = dt(s)
    prev = None
    for i, m in enumerate(c['msgs']):
        toks = m['mods'].split()
        m['kv'] = dict(x.split('=', 1) for x in toks if '=' in x)
        toks = [x for x in toks if '=' not in x]
        if i == 0:
            pass
        elif toks and re.match(r'^\d{4}-\d\d-\d\d$', toks[0]):
            t = dt(' '.join(toks[:2]))
        elif toks and re.match(r'^\+\d+[smhd]$', toks[0]):
            t = t + _delta(toks[0]) + datetime.timedelta(seconds=rnd.randint(0, 50))
        elif m['role'] == 'user':
            t = t + datetime.timedelta(seconds=rnd.randint(35, 160) + min(600, len(prev['text']) // 30 + len(m['text']) // 6))
        else:
            t = t + datetime.timedelta(seconds=rnd.randint(4, 18) + min(90, len(m['text']) // 140), milliseconds=rnd.randint(0, 999))
        m['at'] = t
        prev = m
    first, last = c['msgs'][0]['at'], c['msgs'][-1]['at']
    assert last <= REF, (c['slug'], last)
    assert all(a['at'] <= b['at'] for a, b in zip(c['msgs'], c['msgs'][1:])), c['slug']
    return first, last
# ---------------------------------------------------------------- end CHATFMT

ACCOUNT = 'david.barron.runs@gmail.com (Grok via X @dbarron_runs)'
MODELED = 'grok.com conversation export (documented shape; no real Grok data)'
SEED = 'grok'
TWEPOCH = 1288834974657


def zts(d):
    return dt(d).astimezone(UTC).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def snowflake(d, salt):
    rnd = random.Random(salt)
    ms = int(dt(d).timestamp() * 1000) - rnd.randint(20, 600) * 60000  # post is older than the answer
    return str(((ms - TWEPOCH) << 22) | rnd.randrange(1 << 22))


def model_for(d):
    return 'grok-3' if dt(d) < dt('2026-07-01 00:00') else 'grok-4'


def main():
    g = Gen('grok')
    convs = []
    for f in sorted(glob.glob(os.path.join(CONTENT, 'grok', '*.txt'))):
        convs += parse_chats(f)
    slugs = [c['slug'] for c in convs]
    assert len(slugs) == len(set(slugs)), 'duplicate slugs'
    for c in convs:
        first, last = timeline(c, SEED)
        assert first >= dt('2026-02-03 00:00'), (c['slug'], first)
        cid = uid(f'grok-conv|{c["slug"]}')
        responses, parent = [], None
        for i, m in enumerate(c['msgs']):
            rid = uid(f'grok-resp|{c["slug"]}|{i}')
            lines, srcs, xs = [], [], []
            for ln in m['text'].split('\n'):
                if m['role'] == 'assistant' and ln.startswith('[src] '):
                    t, u, p = [x.strip() for x in ln[6:].split('|', 2)]
                    srcs.append({'title': t, 'url': u, 'preview': p})
                elif m['role'] == 'assistant' and ln.startswith('[x] '):
                    xs.append(snowflake(m['at'], f'{c["slug"]}|{i}|{len(xs)}'))
                else:
                    lines.append(ln)
            r = {'responseId': rid, 'message': '\n'.join(lines).strip(), 'sender': 'human' if m['role'] == 'user' else 'assistant',
                 'createTime': zts(m['at']), 'parentResponseId': parent}
            if m['role'] == 'assistant':
                r['model'] = m['kv'].get('model') or c['meta'].get('model') or model_for(m['at'])
                if srcs: r['webSearchResults'] = srcs
                if xs: r['xPostIds'] = xs
            responses.append(r)
            parent = rid
        obj = {'conversation': {'conversationId': cid, 'title': c['meta']['title'], 'createTime': zts(first), 'modifyTime': zts(last),
                                'starred': c['meta'].get('starred', 'false') == 'true', 'temporary': False},
               'responses': responses}
        g.json(f'@dbarron_runs/conversations/{cid}.json', obj, first, last, account=ACCOUNT, project_ids=c['projects'],
               modeled_on=MODELED, notes=c['meta'].get('notes', ''))
    g.finish()


if __name__ == '__main__':
    main()
