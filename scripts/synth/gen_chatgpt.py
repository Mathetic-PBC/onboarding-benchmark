"""Synthetic ChatGPT conversations (backend-api conversation JSON, `mapping` tree) for dbarron410@vt.edu.

Content: _scripts/synth/content/chatgpt/*.txt (hand-written chats in the CHATFMT text format below).
Layout:  synthetic/chatgpt/dbarron410@vt.edu/conversations/<conversation_id>.json
         synthetic/chatgpt/dbarron410@vt.edu/projects/<g-p-id>.json   (ChatGPT Project "TutorTrace UIST")
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
        t = dt(s) + datetime.timedelta(seconds=rnd.randint(0, 59))
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

ACCOUNT = 'dbarron410@vt.edu'
MODELED = 'authentic/chatgpt conversation JSON (backend-api shape)'
SEED = 'chatgpt-v1'
GIZMO_ID = 'g-p-' + hexid('chatgpt project TutorTrace UIST', 32)
PROJECT_CREATED = '2026-03-24 22:40'


def model_for(d):
    """default_model_slug by period (follows the slug timeline seen in the authentic account)."""
    m = d.astimezone(ET).strftime('%Y-%m')
    if m <= '2025-10': return 'gpt-4o'
    if m <= '2025-12': return 'gpt-5-1'
    if m <= '2026-01': return 'gpt-5-2'
    if m <= '2026-05': return 'gpt-5-3'
    if m <= '2026-06': return 'gpt-5-5'
    return 'gpt-5-6-thinking'


def conv_id(first, slug):
    h = hexid(('chatgpt-conv', slug), 32)
    return f'{int(first.timestamp()):08x}-{h[:4]}-83{h[4:6]}-{h[6:10]}-{h[10:22]}'


def build(c):
    first, last = timeline(c, SEED)
    meta = c['meta']
    model = meta.get('model') or model_for(first)
    thinking = 'thinking' in model
    cid = conv_id(first, c['slug'])
    rnd = random.Random(f'{SEED}|ids|{c["slug"]}')
    mapping = {'client-created-root': {'id': 'client-created-root', 'message': None, 'parent': None, 'children': []}}
    parent = 'client-created-root'
    turn = None; req = None
    for i, m in enumerate(c['msgs']):
        at = m['at'].timestamp()
        if m['role'] == 'user':
            turn = uid((c['slug'], 'turn', i)); req = 'wfr_' + hexid((c['slug'], 'req', i), 26)
            mid = uid((c['slug'], 'msg', i))
            msg = {'id': mid, 'author': {'role': 'user', 'name': None, 'metadata': {}}, 'create_time': at, 'update_time': None,
                   'content': {'content_type': 'text', 'parts': [m['text']]}, 'status': 'finished_successfully', 'end_turn': None,
                   'weight': 1.0, 'metadata': {'selected_sources': [], 'serialization_metadata': {'custom_symbol_offsets': [], 'render_format': 'markdown'},
                                               'request_id': req, 'message_source': None, 'turn_exchange_id': turn, 'can_save': False},
                   'recipient': 'all', 'channel': None}
            if meta.get('gizmo'): msg['metadata']['gizmo_id'] = GIZMO_ID
            nodes = [msg]
        else:
            nodes = []
            prev_at = c['msgs'][i - 1]['at'].timestamp()
            base = {'request_id': req, 'message_type': 'next', 'turn_exchange_id': turn, 'model_slug': model, 'default_model_slug': model,
                    'resolved_model_slug': model, 'model_switcher_deny': []}
            if thinking:
                secs = max(2, int((at - prev_at) * 0.6))
                rid = uid((c['slug'], 'recap', i))
                nodes.append({'id': rid, 'author': {'role': 'assistant', 'name': None, 'metadata': {}}, 'create_time': prev_at + secs + 0.3,
                              'update_time': None, 'content': {'content_type': 'reasoning_recap', 'content': f'Thought for {secs}s'},
                              'status': 'finished_successfully', 'end_turn': False, 'weight': 1.0,
                              'metadata': {**base, 'reasoning_status': 'reasoning_ended', 'finished_duration_sec': secs,
                                           'reasoning_start_time': prev_at + 0.4, 'reasoning_end_time': prev_at + secs + 0.2,
                                           'cot_version': 'v5', 'thinking_effort': 'standard', 'can_save': False},
                              'recipient': 'all', 'channel': None})
            mid = uid((c['slug'], 'msg', i))
            nodes.append({'id': mid, 'author': {'role': 'assistant', 'name': None, 'metadata': {}}, 'create_time': at,
                          'update_time': at + rnd.uniform(0.5, 6.0) if thinking else None,
                          'content': {'content_type': 'text', 'parts': [m['text']]}, 'status': 'finished_successfully', 'end_turn': True,
                          'weight': 1.0, 'metadata': {**base, 'finish_details': {'type': 'stop', 'stop_tokens': [200002]}, 'is_complete': True,
                                                      'citations': [], 'content_references': [], 'search_result_groups': [], 'can_save': True},
                          'recipient': 'all', 'channel': 'final' if thinking else None})
        for n in nodes:
            n_id = n['id']
            if n['author']['role'] == 'assistant': n['metadata']['parent_id'] = parent
            mapping[n_id] = {'id': n_id, 'message': n, 'parent': parent, 'children': []}
            mapping[parent]['children'].append(n_id)
            parent = n_id
    create = first.timestamp() + 0.12
    update = min(last.timestamp() + rnd.uniform(0.3, 2.5), REF.timestamp())
    gz = bool(meta.get('gizmo'))
    obj = {'title': meta['title'], 'create_time': create, 'update_time': update, 'mapping': mapping, 'moderation_results': [],
           'current_node': parent, 'plugin_ids': None, 'conversation_id': cid,
           'conversation_template_id': GIZMO_ID if gz else None, 'gizmo_id': GIZMO_ID if gz else None, 'gizmo_type': 'snorlax' if gz else None,
           'is_archived': meta.get('archived') == 'true', 'is_starred': None, 'safe_urls': [], 'blocked_urls': [], 'default_model_slug': model,
           'atlas_mode_enabled': None, 'conversation_origin': None, 'is_read_only': None, 'voice': None, 'async_status': None,
           'disabled_tool_ids': [], 'is_temporary_chat': False, 'is_do_not_remember': False, 'memory_scope': 'project_enabled' if gz else 'global_enabled',
           'context_scopes': None, 'sugar_item_id': None, 'sugar_item_visible': False, 'pinned_time': None, 'is_study_mode': False,
           'owner': None, 'sectioned_conversation': None, 'context_truncation_continuation': None, 'id': cid}
    return cid, obj, first, last


def main():
    g = Gen('chatgpt')
    convs = []
    for f in sorted(glob.glob(os.path.join(CONTENT, 'chatgpt', '*.txt'))):
        convs += parse_chats(f)
    slugs = [c['slug'] for c in convs]
    assert len(slugs) == len(set(slugs)), 'duplicate slugs'
    proj_convs = []
    for c in convs:
        cid, obj, first, last = build(c)
        n = sum(1 for v in obj['mapping'].values() if v['message'] and v['message']['content']['content_type'] == 'text')
        note = c['meta'].get('notes', '')
        g.json(f'{ACCOUNT}/conversations/{cid}.json', obj, created=first, modified=datetime.datetime.fromtimestamp(obj['update_time'], UTC),
               account=ACCOUNT, project_ids=c['projects'], modeled_on=MODELED, source=f'https://chatgpt.com/c/{cid}',
               notes=note or f"title={obj['title']!r}; {n} user/assistant messages")
        if obj['gizmo_id']:
            proj_convs.append((first, cid, obj['title'], obj['update_time']))
    # ChatGPT Project definition (backend-api/gizmos/<g-p-id> shape)
    proj_convs.sort()
    files = [('tutortrace_uist26_submission.pdf', 'application/pdf', 2_871_402, '2026-03-24 22:44'),
             ('labeling_guide_v3.pdf', 'application/pdf', 412_880, '2026-03-24 22:45'),
             ('uist26_reviews_paper1187.txt', 'text/plain', 18_244, '2026-06-14 22:01'),
             ('rebuttal_v4.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 31_920, '2026-06-17 23:30'),
             ('tutortrace_camera_ready_v2.pdf', 'application/pdf', 3_104_557, '2026-08-12 22:26'),
             ('uist_talk_script_v2.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 24_310, '2026-10-04 21:12')]
    last_upd = max(u for *_, u in proj_convs)
    proj = {
        'gizmo': {
            'id': GIZMO_ID, 'organization_id': None, 'short_url': GIZMO_ID + '-tutortrace-uist', 'author': {'display_name': 'David Barron', 'is_verified': False},
            'voice': None, 'workspace_id': None, 'model': None, 'instructions':
                'This project is for the TutorTrace paper (UIST 2026; PRIME Lab, Virginia Tech; advisor Yan Chen). '
                'Co-labelers: Minsun and Xiaohang. Use the uploaded submission, labeling guide, reviews and rebuttal as ground truth. '
                'Never invent numbers: if a number is not in the files or in my message, ask. Keep paper prose concise and non-hedgy; '
                'UIST style (ACM sigconf). Key facts: 87 students in a CS2 course (CS 3114), 2,340 thirty-second windows, five states '
                'incl. stalled-after-error, Light\'s kappa 0.71 (3 raters, computed before adjudication), TA study n=6. '
                'Talk: 2026-10-07, 15 min + 5 Q&A, session "Learning & Tutoring", chair Tomás Reyes.',
            'settings': {}, 'display': {'name': 'TutorTrace UIST', 'description': '', 'prompt_starters': [], 'profile_picture_url': None,
                                        'emoji': None, 'theme': None},
            'share_recipient': 'private', 'created_at': iso(PROJECT_CREATED, z=True), 'updated_at': iso(datetime.datetime.fromtimestamp(last_upd, UTC), z=True),
            'num_interactions': len(proj_convs), 'categories': [], 'version': None, 'live_version': None, 'training_disabled': None,
            'sharing_targets': [], 'appeal_info': None, 'vanity_metrics': {}, 'workspace_approved': None, 'gizmo_type': 'snorlax',
            'context_stuffing_budget': None, 'is_project': True},
        'files': [{'id': 'file-' + hexid(('cgpt-file', n), 22), 'type': t, 'name': n, 'size': s, 'created_at': iso(d, z=True),
                   'file_size_tokens': None, 'is_owner': True} for n, t, s, d in files],
        'conversations': [{'id': cid, 'title': t, 'create_time': iso(f, z=True)} for f, cid, t, _ in proj_convs],
        'memory_scope': 'project_enabled',
    }
    g.json(f'{ACCOUNT}/projects/{GIZMO_ID}.json', proj, created=PROJECT_CREATED, modified=datetime.datetime.fromtimestamp(last_upd, UTC),
           account=ACCOUNT, project_ids=['project_tutortrace'], modeled_on='ChatGPT Project (backend-api/gizmos/<g-p-id> response, gizmo_type snorlax)',
           notes='HARD CASE: chats inside projects — ChatGPT Project "TutorTrace UIST" definition: instructions, uploaded files, '
                 f'{len(proj_convs)} conversations (their JSON carries gizmo_id {GIZMO_ID})')
    g.finish()


if __name__ == '__main__':
    main()
