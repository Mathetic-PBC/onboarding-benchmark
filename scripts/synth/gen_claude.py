"""Synthetic claude.ai chats + projects (chat_conversations API shape) for dbarron410@vt.edu.

Content: _scripts/synth/content/claude/*.txt (hand-written chats, CHATFMT) and content/claude/docs/ (project knowledge docs).
Layout:  synthetic/claude/conversations/<uuid>.json
         synthetic/claude/projects/<uuid>/{project.json, docs.json, files.json, conversations.json}
"""
import os, sys, re, glob, random, datetime, hashlib
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

TOOL = 'claude'
SEED = 'claude-v1'
ACCOUNT = 'dbarron410@vt.edu'
DOCS = os.path.join(CONTENT, TOOL, 'docs')
ORG = uid('claude-org|dbarron410@vt.edu')
ME_UUID = uid('claude-user|david-barron')
MO_CONV = 'authentic/claude conversation JSON (claude.ai chat_conversations API shape)'
MO_PROJ = 'authentic/claude/projects/<uuid>/ project dir shape (project.json, docs.json, files.json, conversations.json)'
ROOT_PARENT = '00000000-0000-4000-8000-000000000000'


def z(d):
    """ISO-8601 UTC with microseconds and Z, like the claude.ai API."""
    return dt(d).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def zplus(d):
    return dt(d).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')


def model_for(d, slug):
    d = dt(d).astimezone(UTC).strftime('%Y-%m')
    h = int(hashlib.sha256(slug.encode()).hexdigest(), 16)
    if d < '2025-12': return 'claude-sonnet-4-5-20250929'
    if d < '2026-02': return 'claude-opus-4-5-20251101'
    if d < '2026-05': return ['claude-opus-4-6', 'claude-sonnet-4-6'][h % 2]
    if d < '2026-06': return 'claude-opus-4-7'
    if d < '2026-08': return 'claude-opus-4-8'
    if d < '2026-09': return 'claude-opus-5'
    return ['claude-opus-5', 'claude-fable-5-1'][h % 2]


def settings_for(d):
    s = {'enabled_web_search': True, 'tool_search_mode': 'auto', 'preview_feature_uses_artifacts': True}
    if dt(d) >= dt('2026-06-01'):
        s.update({'paprika_mode': 'auto', 'thinking_mode': 'auto', 'chat_memory_mode': 'enabled', 'enabled_artifacts_attachments': False})
    return s


PROJECTS_DEF = {
    'engelbart': dict(name='Engelbart onboarding', pid='project_engelbart', created='2026-08-26 15:12',
                      description='Onboarding flow, connect screen and import rules for Engelbart (Mathetic). Pilot feedback goes here too.',
                      instructions='engelbart_instructions.txt',
                      docs=[('Connect screen v3 spec.md', 'connect_screen_v3_spec.md', '2026-09-16 22:31'),
                            ('Import dedupe rules draft.md', 'import_dedupe_rules_draft.md', '2026-09-03 23:52')],
                      files=[('Engelbart onboarding flow v2.pdf', 'document', 6, 418_220, '2026-08-26 15:20'),
                             ('connect-screen-v3.png', 'image', None, 284_913, '2026-09-16 22:35'),
                             ('Pilot 1 notes - Priya 2026-10-09.pdf', 'document', 3, 96_402, '2026-10-09 19:38')]),
    'ise': dict(name='ISE 6664 report', pid='project_ise6664_affective_computing', created='2026-01-20 21:05',
                description='ISE 6664 Affective Design & Computing final project (Spring 2026): frustration signals in AI-tutoring transcripts.',
                instructions='ise_instructions.txt',
                docs=[('ISE 6664 project brief.md', 'ise_project_brief.md', '2026-01-21 10:14'),
                      ('Codebook v2.md', 'ise_codebook_v2.md', '2026-03-06 22:40')],
                files=[('ISE6664_proposal_Barron_Torres_Lee.pdf', 'document', 2, 188_604, '2026-02-06 16:02'),
                       ('frustration_coding_pilot.xlsx', 'document', None, 41_377, '2026-03-04 23:40')]),
}
for k, p in PROJECTS_DEF.items():
    p['uuid'] = uid(f'claude-project|{k}')


def conv_json(c, first, last):
    slug, meta = c['slug'], c['meta']
    cid = uid(f'claude-conv|{slug}')
    created = first - datetime.timedelta(seconds=1, microseconds=random.Random(slug).randint(0, 900000))
    updated = last + datetime.timedelta(seconds=1, microseconds=random.Random(slug + 'u').randint(0, 900000))
    model = meta.get('model') or model_for(first, slug)
    msgs, parent = [], ROOT_PARENT
    for i, m in enumerate(c['msgs']):
        mid = uid(f'claude-msg|{slug}|{i}')
        at = m['at']
        if m['role'] == 'assistant':
            start = c['msgs'][i - 1]['at'] + datetime.timedelta(seconds=min(2.0, (at - c['msgs'][i - 1]['at']).total_seconds() / 2))
        else:
            start = at
        cm = {'uuid': mid, 'text': '', 'content': [{'start_timestamp': z(start), 'stop_timestamp': z(at), 'type': 'text', 'text': m['text'], 'citations': []}],
              'sender': 'human' if m['role'] == 'user' else 'assistant', 'index': i, 'created_at': z(at), 'updated_at': z(at), 'truncated': False}
        if m['role'] == 'assistant': cm['stop_reason'] = 'stop_sequence'
        cm.update({'attachments': [], 'files': [], 'sync_sources': [], 'parent_message_uuid': parent})
        msgs.append(cm); parent = mid
    j = {'uuid': cid, 'name': meta['title'], 'summary': '', 'model': model, 'created_at': z(created), 'updated_at': z(updated),
         'settings': settings_for(first), 'is_starred': meta.get('starred') == 'true', 'is_archived': False, 'is_temporary': False,
         'workspace_upgraded': False, 'is_multiplayer': False, 'platform': 'CLAUDE_AI', 'is_wiggle_enabled': True,
         'effective_thinking_mode': 'auto' if dt(first) >= dt('2026-06-01') else 'off', 'chat_messages': msgs,
         'current_leaf_message_uuid': parent}
    if meta.get('project'):
        p = PROJECTS_DEF[meta['project']]
        j['project_uuid'] = p['uuid']
        j['project'] = {'uuid': p['uuid'], 'name': p['name']}
    return j, created, updated


def main():
    g = Gen(TOOL)
    convs = []
    for f in sorted(glob.glob(os.path.join(CONTENT, TOOL, '*.txt'))):
        convs += parse_chats(f)
    slugs = [c['slug'] for c in convs]
    assert len(slugs) == len(set(slugs)), 'duplicate slugs'
    by_project = {k: [] for k in PROJECTS_DEF}
    for c in convs:
        first, last = timeline(c, SEED)
        j, created, updated = conv_json(c, first, last)
        rel = f'conversations/{j["uuid"]}.json'
        notes = c['meta'].get('notes', '')
        pk = c['meta'].get('project')
        if pk:
            by_project[pk].append((j, created, updated))
            notes = notes or f"HARD CASE: chats inside projects — chat inside the Claude project '{PROJECTS_DEF[pk]['name']}'"
        projects = list(c['projects'])
        g.json(rel, j, created, updated, account=ACCOUNT, project_ids=projects, modeled_on=MO_CONV, notes=notes)
    # projects
    for k, p in PROJECTS_DEF.items():
        chats = by_project[k]
        pc = dt(p['created'])
        docs = []
        for name, src, when in p['docs']:
            text = open(os.path.join(DOCS, src), encoding='utf-8').read()
            docs.append({'uuid': uid(f'claude-doc|{k}|{name}'), 'file_name': name, 'content': text, 'created_at': zplus(when),
                         'project_uuid': p['uuid'], 'estimated_token_count': len(text) // 4, 'content_length': len(text), 'cleaned_content': None})
        files = []
        for name, kind, pages, size, when in p['files']:
            fu = uid(f'claude-file|{k}|{name}')
            f = {'success': True, 'path': None, 'sanitized_name': None, 'file_kind': kind, 'file_uuid': fu, 'file_name': name,
                 'created_at': zplus(when), 'user_uuid': None, 'size_bytes': size,
                 'thumbnail_asset': {'url': f'/api/{ORG}/files/{fu}/thumbnail', 'file_variant': 'thumbnail', 'primary_color': 'ffffff',
                                     'image_width': 309 if kind == 'document' else 400, 'image_height': 400 if kind == 'document' else 250},
                 'preview_asset': None, 'uuid': fu}
            if kind == 'document':
                f['document_asset'] = {'url': f'/api/{ORG}/files/{fu}/document', 'file_variant': 'original', 'page_count': pages, 'token_count': None}
            else:
                f['preview_asset'] = {'url': f'/api/{ORG}/files/{fu}/preview', 'file_variant': 'preview', 'primary_color': 'f4f4f2', 'image_width': 1440, 'image_height': 900}
            files.append(f)
        times = [pc] + [dt(w) for *_, w in p['docs']] + [dt(f[-1]) for f in p['files']] + [u for _, _, u in chats]
        pu = max(times)
        assert min(dt(w) for *_, w in p['docs'] + p['files']) >= pc and all(cr >= pc for _, cr, _ in chats)
        instructions = open(os.path.join(DOCS, p['instructions']), encoding='utf-8').read().strip()
        pj = {'uuid': p['uuid'], 'name': p['name'], 'description': p['description'], 'is_private': True,
              'creator': {'uuid': ME_UUID, 'full_name': 'David Barron'}, 'is_starred': k == 'engelbart', 'is_starter_project': False,
              'is_harmony_project': False, 'type': None, 'subtype': None, 'settings': {}, 'archiver': None, 'archived_at': None,
              'created_at': zplus(pc), 'updated_at': zplus(pu), 'permissions': ['chat_project:chat:create', 'chat_project:chat:view'],
              'docs_count': len(docs), 'files_count': len(files), 'moved_to': None, 'prompt_template': instructions,
              'organization_role': 'none', 'pending_access_request_count': None, 'cowork_bound_device': None, 'memory_general_enabled': True}
        clist = []
        for j, cr, up in sorted(chats, key=lambda x: x[2], reverse=True):
            s = {kk: vv for kk, vv in j.items() if kk not in ('chat_messages', 'project')}
            s['created_at'] = zplus(cr); s['updated_at'] = zplus(up); s['project'] = j['project']
            clist.append(s)
        key = f'projects/{p["uuid"]}'
        note = (f"HARD CASE: chats inside projects — Claude project '{p['name']}' (instructions, {len(docs)} knowledge docs, "
                f"{len(files)} files, {len(chats)} chats; the chats are separate items under conversations/)")
        meta = dict(account=ACCOUNT, project_ids=[p['pid']], modeled_on=MO_PROJ, label_key=key, notes=note)
        g.json(f'{key}/project.json', pj, pc, pu, **meta)
        g.json(f'{key}/docs.json', docs, pc, max(dt(w) for *_, w in p['docs']), **meta)
        g.json(f'{key}/files.json', files, pc, max(dt(f[-1]) for f in p['files']), **meta)
        g.json(f'{key}/conversations.json', clist, pc, pu, **meta)
        g.dir_times(key, pc, pu)
    g.finish()
    # summary
    from collections import Counter
    cnt = Counter(pid for lab in g.labels.values() for pid in lab['project_ids'])
    print('items:', len(g.labels), dict(sorted(cnt.items())))
    allt = [m['at'] for c in convs for m in c['msgs']]
    print('range:', min(allt).isoformat(), '->', max(allt).isoformat(), '| msgs per conv:', sorted(len(c['msgs']) for c in convs))


if __name__ == '__main__':
    main()
