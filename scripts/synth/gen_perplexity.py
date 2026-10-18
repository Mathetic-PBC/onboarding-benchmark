"""Synthetic Perplexity threads (one JSON per thread) for the Perplexity account opened with david.barron.runs@gmail.com.

Content: _scripts/synth/content/perplexity/*.txt (hand-written threads in CHATFMT; each @user = query_str, each @assistant =
answer markdown with [n] citations followed by `[src] name | url | snippet` lines that become `sources`).
Layout:  synthetic/perplexity/david.barron.runs@gmail.com/threads/<slug>-<id>.json
Pro trial Feb–Apr 2026 (Pro models, Pro Search/COPILOT by default); free tier before and after (turbo, CONCISE by default).
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

ACCOUNT = 'david.barron.runs@gmail.com'
TRIAL = (dt('2026-02-01 00:00'), dt('2026-04-30 23:59'))
PRO_MODELS = ['pplx_pro', 'pplx_pro', 'claude-sonnet', 'gpt-5', 'sonar']
B62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def b62id(seed, n=22):
    h = int(hexid(seed, 40), 16); out = ''
    for _ in range(n):
        h, r = divmod(h, 62); out += B62[r]
    return out


def slugify(q, maxlen=48):
    words = re.sub(r'[^a-z0-9 ]+', ' ', q.lower()).split()
    s = ''
    for w in words:
        if len(s) + len(w) + 1 > maxlen: break
        s = (s + '-' + w) if s else w
    return s or 'thread'


def split_sources(text):
    body, srcs = [], []
    for line in text.split('\n'):
        if line.startswith('[src] '):
            name, url, snip = [x.strip() for x in line[6:].split('|', 2)]
            srcs.append({'name': name, 'url': url, 'snippet': snip})
        else:
            body.append(line)
    return '\n'.join(body).strip(), srcs


def main():
    g = Gen('perplexity')
    convs = []
    for f in sorted(glob.glob(os.path.join(CONTENT, 'perplexity', '*.txt'))):
        convs += parse_chats(f)
    slugs = [c['slug'] for c in convs]
    assert len(slugs) == len(set(slugs)), 'duplicate slugs'
    for c in convs:
        first, last = timeline(c, 'perplexity')
        meta = c['meta']
        rnd = random.Random('pplx|' + c['slug'])
        trial = TRIAL[0] <= first <= TRIAL[1]
        msgs = c['msgs']
        assert [m['role'] for m in msgs] == ['user', 'assistant'] * (len(msgs) // 2), c['slug']
        entries = []
        for q, a in zip(msgs[0::2], msgs[1::2]):
            answer, sources = split_sources(a['text'])
            assert sources, (c['slug'], 'no sources')
            for n in set(int(x) for x in re.findall(r'\[(\d+)\]', answer)):
                assert 1 <= n <= len(sources), (c['slug'], n)
            mode = q['kv'].get('mode') or meta.get('mode') or ('COPILOT' if trial else 'CONCISE')
            model = q['kv'].get('model') or meta.get('model') or (rnd.choice(PRO_MODELS) if trial else 'turbo')
            entries.append({'uuid': uid(f'pplx-entry|{c["slug"]}|{len(entries)}'), 'query_str': q['text'], 'answer': answer,
                            'sources': sources, 'mode': mode, 'model': model, 'created_at': iso(q['at'], z=True),
                            'updated_at': iso(a['at'], z=True)})
        tid = b62id('pplx|' + c['slug'])
        slug = f'{slugify(msgs[0]["text"])}-{tid}'
        updated = last + datetime.timedelta(seconds=rnd.randint(1, 20))
        assert updated <= REF
        space = meta.get('space')
        obj = {'uuid': uid('pplx-thread|' + c['slug']), 'slug': slug, 'title': meta['title'],
               'thread_url': f'https://www.perplexity.ai/search/{slug}',
               'created_at': iso(first, z=True), 'updated_at': iso(updated, z=True),
               'collection': ({'uuid': uid('pplx-space|' + space), 'title': space} if space else None),
               'access': 'private', 'entries': entries}
        notes = meta.get('notes', '')
        g.json(f'{ACCOUNT}/threads/{slug}.json', obj, first, updated, account=f'{ACCOUNT} (Perplexity)',
               project_ids=c['projects'], modeled_on='', notes=notes,
               source=f'https://www.perplexity.ai/search/{slug}')
    g.finish()


if __name__ == '__main__':
    main()
