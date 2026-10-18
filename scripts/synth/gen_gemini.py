"""Synthetic Gemini conversations, stored in the raw batchexecute shape of the authentic collection
(list_entry from the chat list + the hNvQHb conversation read, turns newest-first).

Content: _scripts/synth/content/gemini/{gmail,vt}.txt (hand-written chats in the CHATFMT format).
Layout:  synthetic/gemini/<account>/conversations/c_<16hex>.json  (one file per conversation)
Accounts: dbarron410@vt.edu (u/0, VT Workspace) and davidbarron410@gmail.com (u/1).
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


SEED = 'gemini-v1'
ACCTS = {  # account -> (list_entry kind, prompt-meta flags, account hash used in turns; invented)
    'davidbarron410@gmail.com': dict(kind=2, pflag=(2, 0), ph_tail=(0, None, None, False), h=hexid('gemini-acct-u1', 16)),
    'dbarron410@vt.edu': dict(kind=4, pflag=(4, 1), ph_tail=(None, None, None, None), h=hexid('gemini-acct-u0', 16)),
}
MODELED = 'authentic/gemini/<account>/conversations raw batchexecute JSON (list_entry + hNvQHb read)'


def model_for(d):
    if d < dt('2025-11-19 00:00'): return '2.5 Flash', None
    if d < dt('2026-06-01 00:00'): return '3 Pro', None
    return '3.1 Pro', 'gemini-3.1-pro-preview'


def ts(d):
    e = dt(d).timestamp()
    return [int(e), int(round((e - int(e)) * 1e9 / 1000)) * 1000]


def candidate(rc, answer):
    return [rc, [answer], None, None, None, None, None, None, [2], 'en', None, None,
            [None, None, None, None, None, None, None, []], None, None, None, None, None, None, None, None, [False],
            None, None, None, None, None, None, [], None, None]


def turn(cid, r, rc, prev, user_text, answer, when, acct):
    a = ACCTS[acct]
    label, mid = model_for(when)
    prompt = [[user_text], a['pflag'][0], None, a['pflag'][1], a['h'], *a['ph_tail'], None, []]
    resp = [[candidate(rc, answer)], None, None, rc, None, None, None, None, 'US', True, None, None, None, None,
            a['h'], None, None, a['h'], None, None, None, label, None, None, 3]
    if mid:
        resp += [1, None, None, None, None, None, mid]
    return [[cid, r], [cid, prev[0], prev[1]] if prev else None, prompt, resp, ts(when)]


def main():
    g = Gen('gemini')
    n_turns = 0
    for f in sorted(glob.glob(os.path.join(CONTENT, 'gemini', '*.txt'))):
        for c in parse_chats(f):
            acct = c['meta']['account']
            first, last = timeline(c, SEED)
            msgs = c['msgs']
            assert len(msgs) % 2 == 0 and all(m['role'] == ('user' if i % 2 == 0 else 'assistant') for i, m in enumerate(msgs)), c['slug']
            cid = 'c_' + hexid(('gemini', c['slug']), 16)
            turns, prev = [], None
            for i in range(0, len(msgs), 2):
                u, a = msgs[i], msgs[i + 1]
                r = 'r_' + hexid((cid, i, 'r'), 16); rc = 'rc_' + hexid((cid, i, 'rc'), 16)
                turns.append(turn(cid, r, rc, prev, u['text'], a['text'], a['at'], acct))
                prev = (r, rc)
            turns.reverse()  # newest first, as returned by the read call
            title = c['meta']['title']
            last_rc = turns[0][3][3]
            list_entry = [cid, title, None, None, None, ts(last), None, None, None, ACCTS[acct]['kind']] + [None] * 11 + [last_rc]
            obj = {'id': cid, 'title': title, 'list_entry': list_entry, 'read': [[turns, None, None, 0]]}
            note = (f"title='{title}'; first turn {iso(first)}; ~{len(turns)} response ids; raw batchexecute JSON (list_entry + hNvQHb read)")
            if c['meta'].get('notes'): note += '; ' + c['meta']['notes']
            g.json(f'{acct}/conversations/{cid}.json', obj, first, last, indent=None, account=acct, project_ids=c['projects'],
                   modeled_on=MODELED, notes=note, label_notes=c['meta'].get('notes') or None)
            n_turns += len(turns)
    print('turns:', n_turns)
    g.finish()


if __name__ == '__main__':
    main()
