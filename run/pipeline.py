"""The import pipeline for one run: wave 1 (profiles + merge), wave 2 (shallow sort), new categories from
wave 2's proposals, a re-sort of the items they could hold, and the deep pass. No scoring.

  BENCH_RUN=run_002 python3 -I run/pipeline.py wave1|wave2|new_categories|resort|deep|write

Every model call is a headless `claude -p` with the stage's skill (or the profile prompt) as the
system prompt, its input on stdin, and nothing from outside runs/<run>/sandbox/. Each input is
screened by leakguard before it is sent and saved under inputs/.
"""
import collections, datetime, hashlib, json, os, re, subprocess, sys, tempfile, threading, time

sys.path.insert(0, os.path.dirname(__file__))
import extract, leakguard
from config import DATA, DATASET_ID, RUN, RUN_ID, SKILLS

SANDBOX = os.path.join(RUN, 'sandbox')
CALL_CWD = tempfile.mkdtemp(prefix='bench-call-')   # empty, so a call picks up no project files
MODEL = 'claude-sonnet-5-5'
SLOTS = 4
RETRIES = 2
CHAT_SOURCES = {'chatgpt', 'claude', 'gemini', 'grok', 'perplexity', 'cursor', 'claude-code', 'codex'}
BATCH_CHAT, BATCH_OTHER = 25, 50
# a category proposed in wave 2 is added only when this many items, or items from this many sources, back it
SUPPORT_ITEMS, SUPPORT_SOURCES = 3, 2
# per step: row id tag, inputs/outputs folder, analyses stage, rows file
STEPS = {'wave2': ('w2', 'wave2', 'wave2_shallow', 'wave2_rows.jsonl'),
         'resort': ('w2r', 'resort', 'wave2_resort', 'resort_rows.jsonl')}

BASE_FLAGS = ['--model', MODEL, '--setting-sources', '', '--strict-mcp-config', '--disable-slash-commands',
              '--no-session-persistence']
ENV = {**os.environ, 'CLAUDE_CODE_DISABLE_AUTO_MEMORY': '1'}

_lock = threading.Lock()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def path(*p):
    full = os.path.join(RUN, *p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    return full


def skill(name):
    return open(os.path.join(SKILLS, name, 'SKILL.md')).read()


def alias(item_id):
    return 'it_' + hashlib.sha256((RUN_ID + ':' + item_id).encode()).hexdigest()[:8]


def log_event(**kw):
    with _lock:
        with open(path('work', 'events.jsonl'), 'a') as fh:
            fh.write(json.dumps({'at': now(), **kw}) + '\n')


# ---------- model calls ----------

def parse_json(text):
    t = text.strip()
    t = re.sub(r'^```(?:json)?\s*|\s*```$', '', t)
    try:
        return json.loads(t)
    except Exception:
        a, b = t.find('{'), t.rfind('}')
        if a >= 0 and b > a:
            return json.loads(t[a:b + 1])
        raise


def usage_of(out):
    u = out.get('usage') or {}
    inp = (u.get('input_tokens') or 0) + (u.get('cache_creation_input_tokens') or 0) + (u.get('cache_read_input_tokens') or 0)
    return {'input_tokens': inp, 'output_tokens': u.get('output_tokens') or 0,
            'cost_usd': round(out.get('total_cost_usd') or 0.0, 6),
            'cache_read_input_tokens': u.get('cache_read_input_tokens') or 0,
            'cache_creation_input_tokens': u.get('cache_creation_input_tokens') or 0}


def call(stage, call_id, system, stdin, want_json=True, tools='', cwd=CALL_CWD, extra=(), timeout=1200):
    """One headless call with up to RETRIES retries. Returns a dict; never raises."""
    snap = path('inputs', stage, f'{call_id}.json' if want_json else f'{call_id}.txt')
    with open(snap, 'w') as fh:
        fh.write(stdin)
    leaks = {k: v for k, v in leakguard.hits(system + '\n' + stdin).items() if v}
    if leaks:
        log_event(stage=stage, call=call_id, event='leak_guard_blocked', patterns=sorted(leaks))
        return {'ok': False, 'error': 'leak guard blocked the input: ' + ', '.join(sorted(leaks)), 'snapshot': snap,
                'attempts': 0, 'usage': {'input_tokens': 0, 'output_tokens': 0, 'cost_usd': 0.0}}
    cmd = ['claude', '-p', *BASE_FLAGS, '--system-prompt', system, '--tools', tools, *extra]
    if '--output-format' not in extra:
        cmd += ['--output-format', 'json']
    usage_total = {'input_tokens': 0, 'output_tokens': 0, 'cost_usd': 0.0, 'cache_read_input_tokens': 0,
                   'cache_creation_input_tokens': 0}
    errors, started = [], now()
    for attempt in range(1 + RETRIES):
        t0 = time.time()
        try:
            p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, cwd=cwd, env=ENV, timeout=timeout)
            raw = p.stdout
            if '--output-format' in extra and 'stream-json' in extra:
                lines = [json.loads(l) for l in raw.splitlines() if l.strip().startswith('{')]
                out = next((l for l in reversed(lines) if l.get('type') == 'result'), {})
                out['_stream'] = lines
            else:
                out = json.loads(raw) if raw.strip() else {}
            u = usage_of(out)
            for k in usage_total:
                usage_total[k] += u.get(k, 0)
            if p.returncode != 0 or out.get('is_error') or not out.get('result'):
                raise RuntimeError(f"exit {p.returncode}: {(out.get('result') or p.stderr or raw)[:300]}")
            text = out['result']
            data = parse_json(text) if want_json else None
            with open(path('outputs', stage, f'{call_id}.json'), 'w') as fh:
                json.dump({k: v for k, v in out.items() if k != '_stream'}, fh, indent=1)
            log_event(stage=stage, call=call_id, event='ok', attempt=attempt, secs=round(time.time() - t0, 1), **u)
            return {'ok': True, 'data': data, 'text': text, 'usage': usage_total, 'attempts': attempt + 1,
                    'snapshot': snap, 'started_at': started, 'completed_at': now(), 'stream': out.get('_stream'),
                    'retry_errors': errors}
        except Exception as e:
            errors.append(f'{type(e).__name__}: {str(e)[:300]}')
            log_event(stage=stage, call=call_id, event='error', attempt=attempt, error=errors[-1])
    return {'ok': False, 'error': ' | '.join(errors), 'usage': usage_total, 'attempts': 1 + RETRIES, 'snapshot': snap,
            'started_at': started, 'completed_at': now()}


# ---------- shared data ----------

def sample_items():
    ids = set(json.load(open(os.path.join(RUN, 'sample.json')))['item_ids'])
    return [r for r in json.load(open(os.path.join(SANDBOX, 'items.json'))) if r['id'] in ids]


def catset(cid):
    return next(r for r in json.load(open(path('work', 'catsets.json'))) if r['id'] == cid)


def current_catset():
    """The list the deep pass works from: catset_v3 when wave 2's proposals added categories, else catset_v2."""
    sets = {r['id']: r for r in json.load(open(path('work', 'catsets.json')))}
    return sets.get('catset_v3') or sets['catset_v2']


def cats_for_prompt(cs):
    return [{'id': c['id'], 'name': c['name'], 'description': c['description']} for c in cs['categories']]


def other_id(cs):
    for c in cs['categories']:
        if c['id'] in ('cat_other', 'other') or c['name'].strip().lower() == 'other':
            return c['id']
    return None


def load_rows(name):
    f = path('work', name)
    if not os.path.exists(f):
        return {}
    rows = {}
    for ln in open(f):
        r = json.loads(ln)
        rows[r['item_id']] = r
    return rows


def save_row(name, row):
    with _lock:
        with open(path('work', name), 'a') as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + '\n')


def norm(s):
    return re.sub(r'\s+', ' ', s or '').strip()


def check_evidence(assignments, units_by_index, valid_ids, notes, folder=False):
    """Keep assignments with known category ids and evidence quotes found verbatim in their unit."""
    kept = []
    for a in assignments or []:
        pid = a.get('project_id')
        if pid not in valid_ids:
            notes.append(f'dropped assignment to unknown category {pid!r}')
            continue
        ev_kept = []
        for ev in a.get('evidence') or []:
            q, idx = ev.get('quote') or '', ev.get('index')
            cands = units_by_index.get(idx, [])
            if folder and ev.get('file'):
                cands = [u for u in cands if u.get('file') == ev.get('file')] or cands
            if q and any(q in u['text'] for u in cands):
                ev_kept.append(ev)
            elif q and any(norm(q) in norm(u['text']) for u in cands):
                ev_kept.append({**ev, 'match': 'whitespace_normalized'})
            else:
                notes.append(f'dropped quote not found verbatim in {ev.get("unit")} {idx}: {q[:60]!r}')
        kept.append({'project_id': pid, 'confidence': a.get('confidence'), 'evidence': ev_kept})
    return kept


# ---------- slot scheduler ----------

def run_slots(queues, work, label):
    """queues: {source: [job, ...]}. Each slot takes a source and works through it, then the next
    waiting source; once none are waiting, free slots take jobs from the source with most left."""
    waiting = sorted(queues, key=lambda s: -len(queues[s]))
    qs = {s: list(q) for s, q in queues.items()}
    lock = threading.Lock()

    def next_job(state):
        with lock:
            own = state.get('src')
            if own and qs[own]:
                return qs[own].pop(0)
            if waiting:
                state['src'] = waiting.pop(0)
                return qs[state['src']].pop(0) if qs[state['src']] else None
            busiest = max(qs, key=lambda s: len(qs[s]), default=None)
            if busiest and qs[busiest]:
                return qs[busiest].pop(0)
            return None

    def slot(n):
        state = {}
        while True:
            job = next_job(state)
            if job is None:
                with lock:
                    if not waiting and not any(qs.values()):
                        return
                continue
            try:
                work(job, n)
            except Exception as e:
                log_event(stage=label, event='slot_exception', slot=n, error=f'{type(e).__name__}: {e}')

    ts = [threading.Thread(target=slot, args=(n,)) for n in range(1, SLOTS + 1)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()


# ---------- wave 1 ----------

PROFILE_PROMPT = """You are given material an AI assistant saved about one person: memories, custom instructions and account profile.
Answer the question "What has this person worked on?" from this material only. Do not guess beyond it.
Write a Markdown profile: one section per project or area of work, each with a one-line description and any dates the material gives. End with a short list of anything that looks personal rather than work."""

LOCAL_PROMPT = """You have read-only tools over three folders of one person's coding activity, in your working directory:
- claude-code/: Claude Code session folders (projects/<folder named after the directory the session ran in>/<session>.jsonl), prompt history and related files
- codex/: Codex sessions (sessions/YYYY/MM/DD/rollout-*.jsonl) and prompt history
- github/: repositories; each has a GIT_LOG.txt with its commit history (date, author: subject)
Answer the question "What has this person worked on?" using only these folders. Read session folder names, session titles and first prompts, and the git logs. Sample broadly; do not try to read everything.
Finish with a Markdown profile of projects: for each, a one-line description, the folders, sessions or repos it shows up in, and first and last dates seen."""


def wave1():
    t0 = time.time()
    os.makedirs(path('profiles', 'x'), exist_ok=True)
    with open(path('prompts', 'profile-v1.md'), 'w') as fh:
        fh.write(PROFILE_PROMPT)
    with open(path('prompts', 'profile-local-v1.md'), 'w') as fh:
        fh.write(LOCAL_PROMPT)
    calls = {}
    mem = os.path.join(SANDBOX, 'files', 'assistant-memory')

    def materials(sub):
        parts = []
        for dp, _, fns in os.walk(os.path.join(mem, sub)):
            for fn in sorted(fns):
                p = os.path.join(dp, fn)
                parts.append(f'=== file: {os.path.relpath(p, mem)} ===\n{open(p, errors="replace").read()}')
        return 'Question: What has this person worked on?\n\nMaterial:\n\n' + '\n\n'.join(parts)

    def one(name):
        if name == 'local':
            lv = os.path.join(SANDBOX, 'local_view')
            deny = {'permissions': {'deny': [f'Read(/{p}/**)' for p in (
                DATA, os.path.expanduser('~/Desktop/onboarding-benchmark'), os.path.expanduser('~/.claude'),
                os.path.join(RUN, 'private'), os.path.join(RUN, 'work'), os.path.join(SANDBOX, 'files'))]}}
            r = call('wave1', 'profile_local', LOCAL_PROMPT, 'What has this person worked on?', want_json=False,
                     tools='Read,Glob,Grep', cwd=lv,
                     extra=('--settings', json.dumps(deny), '--output-format', 'stream-json', '--verbose'))
            r['audit'] = audit_tools(r.get('stream') or [], lv)
        else:
            r = call('wave1', f'profile_{name}', PROFILE_PROMPT, materials(name), want_json=False)
        if r['ok']:
            with open(path('profiles', f'{name}.md'), 'w') as fh:
                fh.write(r['text'].strip() + '\n')
        calls[name] = r

    ts = [threading.Thread(target=one, args=(n,)) for n in ('chatgpt', 'claude', 'local')]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    t_prof = time.time() - t0

    profiles = {n: open(path('profiles', f'{n}.md')).read() for n in ('chatgpt', 'claude', 'local')
                if os.path.exists(path('profiles', f'{n}.md'))}
    merge_input = json.dumps({'profile_projects': profiles}, ensure_ascii=False, indent=1)
    r = call('wave1', 'merge', skill('wave1-categories-v1'), merge_input)
    calls['merge'] = r
    created = now()
    out = []
    if r['ok']:
        cats = r['data'].get('categories') or []
        v1 = {'id': 'catset_v1', 'run_id': RUN_ID, 'dataset_id': DATASET_ID, 'categories': cats, 'created_at': created,
              'model': MODEL, 'prompt_version': 'wave1-categories-v1',
              'inputs': {'profiles': ['profiles/chatgpt.md', 'profiles/claude.md', 'profiles/local.md'],
                         'user_categories': None, 'project': None},
              'input_snapshot_path': os.path.relpath(r['snapshot'], RUN), 'usage': r['usage']}
        v2 = {'id': 'catset_v2', 'run_id': RUN_ID, 'dataset_id': DATASET_ID, 'categories': cats, 'created_at': now(),
              'model': MODEL, 'prompt_version': 'wave1-categories-v1', 'derived_from': 'catset_v1',
              'confirmation': 'simulated: draft accepted unchanged'}
        out = [v1, v2]
    json.dump(out, open(path('work', 'catsets.json'), 'w'), indent=1, ensure_ascii=False)
    summary = {'secs_profiles': round(t_prof, 1), 'secs_total': round(time.time() - t0, 1),
               'calls': {k: {'ok': v['ok'], 'attempts': v['attempts'], 'usage': v['usage'], 'error': v.get('error'),
                             **({'audit': v['audit']} if 'audit' in v else {})} for k, v in calls.items()}}
    json.dump(summary, open(path('work', 'wave1_summary.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1))
    if out:
        print('categories:', [(c['id'], c.get('flag')) for c in out[0]['categories']])


def audit_tools(stream, root):
    """Every path the local agent's tools touched must be inside root."""
    root = os.path.realpath(root)
    calls, outside = 0, []
    for ev in stream:
        if ev.get('type') != 'assistant':
            continue
        for c in (ev.get('message') or {}).get('content') or []:
            if c.get('type') != 'tool_use':
                continue
            calls += 1
            inp = c.get('input') or {}
            for k in ('file_path', 'path'):
                if inp.get(k):
                    p = inp[k] if os.path.isabs(inp[k]) else os.path.join(root, inp[k])
                    if not os.path.realpath(p).startswith(root):
                        outside.append(f"{c.get('name')}:{k}")
            pat = inp.get('pattern') or ''
            if pat.startswith('/') and not os.path.realpath(pat.split('*')[0] or '/').startswith(root):
                outside.append(f"{c.get('name')}:pattern")
    return {'tool_calls': calls, 'outside_root': len(outside), 'outside_kinds': sorted(set(outside))}


# ---------- wave 2 ----------

def wave2():
    t0 = time.time()
    cs = catset('catset_v2')
    cats = cats_for_prompt(cs)
    valid = {c['id'] for c in cats}
    system = skill('wave2-shallow-sort-v1')
    items = sample_items()
    done = load_rows('wave2_rows.jsonl')
    todo = [r for r in items if r['id'] not in done or done[r['id']]['status'] != 'completed']
    queues = batch_queues(todo, 'w2')

    def work(job, slot):
        bid, rs = job
        run_batch(bid, rs, slot, system, cats, valid, retry_missing=True)

    run_slots(queues, work, 'wave2')
    rows = load_rows('wave2_rows.jsonl')
    st = collections.Counter(rows[r['id']]['status'] for r in items if r['id'] in rows)
    print(json.dumps({'secs': round(time.time() - t0, 1), 'items': len(items), 'rows': dict(st),
                      'missing_rows': sum(1 for r in items if r['id'] not in rows)}, indent=1))


def batch_queues(rs, prefix):
    """One queue per source, cut into even batches near the source's target size."""
    by_src = collections.defaultdict(list)
    for r in sorted(rs, key=lambda r: r['id']):
        by_src[r['source']].append(r)
    queues = {}
    for src, group in by_src.items():
        size = BATCH_CHAT if src in CHAT_SOURCES else BATCH_OTHER
        n = -(-len(group) // size)
        per = -(-len(group) // n)
        queues[src] = [(f'{prefix}_{src}_{k + 1:02d}', group[k * per:(k + 1) * per]) for k in range(n)]
    return queues


def run_batch(bid, rs, slot, system, cats, valid, retry_missing, step='wave2', catset_id='catset_v2', parents=None):
    tag, folder, stage, rows_file = STEPS[step]
    recs, infos = {}, {}
    for r in rs:
        rec, info = extract.snippet(r)
        recs[r['id']] = {'id': alias(r['id']), **rec}
        infos[r['id']] = info
    payload = json.dumps({'categories': cats, 'items': [recs[r['id']] for r in rs]}, ensure_ascii=False, indent=1)
    res = call(folder, bid, system, payload)
    by_alias = {}
    if res['ok']:
        for x in (res['data'].get('results') or []) if isinstance(res['data'], dict) else []:
            if isinstance(x, dict) and x.get('item_id'):
                by_alias[x['item_id']] = x
    sizes = {r['id']: len(json.dumps(recs[r['id']], ensure_ascii=False)) for r in rs}
    total = sum(sizes.values()) or 1
    missing = []
    for r in rs:
        share = sizes[r['id']] / total
        usage = {k: (round(v * share, 6) if k == 'cost_usd' else round(v * share)) for k, v in res['usage'].items()}
        x = by_alias.get(alias(r['id']))
        if res['ok'] and x is None and retry_missing:
            missing.append(r)
            continue
        notes = []
        units = collections.defaultdict(list)
        for u in recs[r['id']]['snippet']['units']:
            units[u['index']].append(u)
        if res['ok'] and x is not None:
            assignments = check_evidence(x.get('project_assignments'), units, valid, notes)
            result = {'project_assignments': assignments, 'proposed_projects': x.get('proposed_projects') or [],
                      'summary': x.get('summary'), 'needs_deeper_read': bool(x.get('needs_deeper_read'))}
            status, error = 'completed', ('; '.join(notes) or None)
        else:
            result, status = None, 'failed'
            error = res.get('error') or 'item missing from batch output (after a retry as its own batch)'
        if res.get('retry_errors'):
            error = '; '.join(filter(None, [error, 'retried: ' + ' | '.join(res['retry_errors'])]))
        row = {'id': f'{RUN_ID}_{tag}_{r["id"]}', 'item_id': r['id'], 'run_id': RUN_ID, 'dataset_id': DATASET_ID,
               'parent_analysis_id': parents[r['id']]['id'] if parents else None, 'category_set_id': catset_id,
               'content_hash': r.get('content_hash'), 'stage': stage, 'status': status, 'error': error,
               'started_at': res.get('started_at'), 'completed_at': res.get('completed_at'), 'model': MODEL,
               'prompt_version': 'wave2-shallow-sort-v1',
               'config': {'tools': 'none', 'batch_target': BATCH_CHAT if r['source'] in CHAT_SOURCES else BATCH_OTHER,
                          'attempts': res['attempts'], 'alias': alias(r['id'])},
               'batch': {'id': bid, 'size': len(rs), 'slot': slot},
               'sample': {**infos[r['id']], 'input_snapshot_path': os.path.relpath(res['snapshot'], RUN)},
               'result': result, 'usage': usage}
        save_row(rows_file, row)
    if missing:
        log_event(stage=folder, call=bid, event='items_missing', n=len(missing))
        run_batch(bid + '_r', missing, slot, system, cats, valid, False, step, catset_id, parents)


# ---------- new categories from wave 2 ----------

def proposals_from(rows, items):
    """Wave 2's proposed categories, grouped by name, with the items, sources and titles behind each."""
    groups = {}
    for iid, row in sorted(rows.items()):
        res = row.get('result')
        if row['status'] != 'completed' or not res:
            continue
        for p in res.get('proposed_projects') or []:
            name = norm(p.get('name') or p.get('label'))
            if not name:
                continue
            key = re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
            g = groups.setdefault(key, {'key': key, 'name': name, 'descriptions': [], 'item_ids': [],
                                        'sources': set(), 'titles': []})
            d = norm(p.get('description'))
            if d and d not in g['descriptions'] and len(g['descriptions']) < 3:
                g['descriptions'].append(d)
            if iid not in g['item_ids']:
                g['item_ids'].append(iid)
                g['sources'].add(items[iid]['source'])
                if items[iid].get('title') and len(g['titles']) < 5:
                    g['titles'].append(items[iid]['title'])
    return groups


def new_categories():
    """Check wave 2's proposals against catset_v2 and write catset_v3 with the ones that are new and backed
    by enough items. The person's confirmation is simulated: every supported new category is accepted."""
    t0 = time.time()
    v2 = catset('catset_v2')
    items = {r['id']: r for r in sample_items()}
    groups = proposals_from(load_rows('wave2_rows.jsonl'), items)
    cats = cats_for_prompt(v2)
    valid = {c['id'] for c in cats}
    review = {'proposals': len(groups), 'added': [], 'unsupported': [], 'existing': [], 'dropped': [], 'unanswered': []}
    added, usage = [], None
    if groups:
        payload = json.dumps({'categories': cats, 'proposals': [
            {'key': g['key'], 'name': g['name'], 'descriptions': g['descriptions'], 'items': len(g['item_ids']),
             'sources': sorted(g['sources']), 'titles': g['titles']} for g in groups.values()]},
            ensure_ascii=False, indent=1)
        r = call('new_categories', 'review', skill('wave2-new-categories-v1'), payload)
        usage = r['usage']
        if not r['ok'] or not isinstance(r['data'], dict):
            sys.exit('new-categories call failed: ' + (r.get('error') or 'answer was not a JSON object'))
        x, seen = r['data'], set()
        for c in x.get('add') or []:
            keys = [k for k in c.get('merged_from') or [] if k in groups and k not in seen]
            seen.update(keys)
            ids = {i for k in keys for i in groups[k]['item_ids']}
            srcs = sorted({s for k in keys for s in groups[k]['sources']})
            entry = {'id': c.get('id'), 'name': c.get('name'), 'merged_from': keys, 'items': len(ids), 'sources': srcs}
            if not keys or not c.get('id') or c['id'] in valid:
                review['dropped'].append({**entry, 'why': 'answer had no known proposals or reused an id'})
            elif len(ids) >= SUPPORT_ITEMS or len(srcs) >= SUPPORT_SOURCES:
                added.append({'id': c['id'], 'name': c.get('name'), 'description': c.get('description'),
                              'source': 'wave2', 'flag': None,
                              'evidence': [t for k in keys for t in groups[k]['titles']][:5]})
                valid.add(c['id'])
                review['added'].append(entry)
            else:
                review['unsupported'].append(entry)
        for e in x.get('existing') or []:
            if e.get('key') in groups and e['key'] not in seen:
                seen.add(e['key'])
                review['existing'].append(e)
        for d in x.get('dropped') or []:
            if d.get('key') in groups and d['key'] not in seen:
                seen.add(d['key'])
                review['dropped'].append(d)
        review['unanswered'] = sorted(set(groups) - seen)
    sets = [s for s in json.load(open(path('work', 'catsets.json'))) if s['id'] != 'catset_v3']
    if added:
        oid = other_id(v2)
        sets.append({'id': 'catset_v3', 'run_id': RUN_ID, 'dataset_id': DATASET_ID,
                     'categories': [c for c in v2['categories'] if c['id'] != oid] + added
                                   + [c for c in v2['categories'] if c['id'] == oid],
                     'created_at': now(), 'model': MODEL, 'prompt_version': 'wave2-new-categories-v1',
                     'derived_from': 'catset_v2', 'added': [c['id'] for c in added],
                     'support_rule': f'{SUPPORT_ITEMS}+ items or {SUPPORT_SOURCES}+ sources',
                     'confirmation': 'simulated: new categories accepted unchanged', 'usage': usage})
    json.dump(sets, open(path('work', 'catsets.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(review, open(path('work', 'new_categories.json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({'secs': round(time.time() - t0, 1), 'proposals': len(groups),
                      **{k: len(v) for k, v in review.items() if k != 'proposals'}}, indent=1))


def resort():
    """Sort again, against catset_v3, the items wave 2 filed under "other" or that proposed a category."""
    t0 = time.time()
    cs = current_catset()
    if cs['id'] != 'catset_v3':
        print('no new categories, so nothing to re-sort')
        return
    oid = other_id(cs)
    w2 = load_rows('wave2_rows.jsonl')
    items = {r['id']: r for r in sample_items()}
    picks = []
    for iid, row in sorted(w2.items()):
        res = row.get('result')
        if row['status'] != 'completed' or not res:
            continue
        if oid in {a['project_id'] for a in res['project_assignments']} or res.get('proposed_projects'):
            picks.append(iid)
    done = load_rows('resort_rows.jsonl')
    todo = [items[i] for i in picks if i not in done or done[i]['status'] != 'completed']
    cats = cats_for_prompt(cs)
    valid = {c['id'] for c in cats}
    system = skill('wave2-shallow-sort-v1')

    def work(job, slot):
        bid, rs = job
        run_batch(bid, rs, slot, system, cats, valid, True, 'resort', cs['id'], w2)

    run_slots(batch_queues(todo, 'w2r'), work, 'resort')
    rows = load_rows('resort_rows.jsonl')
    print(json.dumps({'secs': round(time.time() - t0, 1), 'items': len(picks),
                      'rows': dict(collections.Counter(rows[i]['status'] for i in picks if i in rows))}, indent=1))


# ---------- deep ----------

def deep():
    t0 = time.time()
    cs = current_catset()
    cats = cats_for_prompt(cs)
    valid = {c['id'] for c in cats}
    oid = other_id(cs)
    picked = [c['id'] for c in cats if c['id'] != oid]
    system = skill('deep-pass-v1')
    items = {r['id']: r for r in sample_items()}
    w2 = load_rows('wave2_rows.jsonl')
    w2.update({i: r for i, r in load_rows('resort_rows.jsonl').items() if r['status'] == 'completed'})
    done = load_rows('deep_rows.jsonl')
    qual = []
    for iid, row in sorted(w2.items()):
        res = row.get('result')
        if row['status'] != 'completed' or not res:
            continue
        if res['needs_deeper_read'] or any(a['project_id'] in picked for a in res['project_assignments']):
            qual.append(iid)
    json.dump({'picked': picked, 'other': oid, 'qualifying': qual}, open(path('work', 'deep_selection.json'), 'w'), indent=1)
    todo = [i for i in qual if i not in done or done[i]['status'] != 'completed']
    queues = collections.defaultdict(list)
    for iid in todo:
        queues[items[iid]['source']].append(iid)

    def work(iid, slot):
        r, parent = items[iid], w2[iid]
        rec, info = extract.deep_read(r)
        a = alias(iid)
        shallow = {'item_id': a, **{k: parent['result'][k] for k in ('project_assignments', 'proposed_projects',
                                                                       'summary', 'needs_deeper_read')}}
        payload = json.dumps({'categories': cats, 'selected': picked, 'shallow': shallow,
                              'item': {'id': a, 'title': r.get('title'), 'source': r['source'],
                                       'date': (r.get('modified_at') or r.get('created_at') or '')[:10] or None,
                                       **rec}}, ensure_ascii=False, indent=1)
        res = call('deep', iid, system, payload)
        notes, result, status = [], None, 'failed'
        units = collections.defaultdict(list)
        for u in rec['units']:
            units[u['index']].append(u)
        if res['ok'] and isinstance(res['data'], dict):
            x = res['data']
            if x.get('item_id') not in (a, None):
                notes.append(f'item_id in answer was {x.get("item_id")!r}')
            dec = (x.get('decision') or '').strip().lower()
            if dec not in ('import', 'skip', 'pending'):
                notes.append(f'invalid decision {x.get("decision")!r}')
                dec = None
            assignments = check_evidence(x.get('project_assignments'), units, valid, notes,
                                         folder=any(u.get('file') for u in rec['units']))
            result = {'project_assignments': assignments, 'proposed_projects': x.get('proposed_projects') or [],
                      'summary': x.get('summary'), 'changed_from_shallow': x.get('changed_from_shallow'),
                      'change_reason': x.get('change_reason'), 'needs_deeper_read': False,
                      'decision': dec, 'library_action': None}
            status = 'completed' if dec else 'failed'
        error = '; '.join(filter(None, [res.get('error'), '; '.join(notes) or None,
                                        ('retried: ' + ' | '.join(res['retry_errors'])) if res.get('retry_errors') else None])) or None
        row = {'id': f'{RUN_ID}_deep_{iid}', 'item_id': iid, 'run_id': RUN_ID, 'dataset_id': DATASET_ID,
               'parent_analysis_id': parent['id'], 'category_set_id': cs['id'], 'content_hash': r.get('content_hash'),
               'stage': 'deep', 'status': status, 'error': error,
               'started_at': res.get('started_at'), 'completed_at': res.get('completed_at'), 'model': MODEL,
               'prompt_version': 'deep-pass-v1',
               'config': {'tools': 'none', 'items_per_call': 1, 'slot': slot, 'attempts': res['attempts'],
                          'selected_categories': picked, 'alias': a},
               'sample': {**info, 'input_snapshot_path': os.path.relpath(res['snapshot'], RUN)},
               'result': result, 'usage': res['usage']}
        save_row('deep_rows.jsonl', row)

    run_slots(dict(queues), work, 'deep')
    rows = load_rows('deep_rows.jsonl')
    assign_library_actions(rows, items)
    st = collections.Counter(rows[i]['status'] for i in qual if i in rows)
    dec = collections.Counter((rows[i]['result'] or {}).get('decision') for i in qual if i in rows)
    print(json.dumps({'secs': round(time.time() - t0, 1), 'qualifying': len(qual), 'rows': dict(st),
                      'decisions': dict(dec), 'missing_rows': sum(1 for i in qual if i not in rows)}, indent=1))


def assign_library_actions(rows, items):
    """Simulated library: the first import of a piece of content would create an entry; later
    imports of the same content (same hash, or a derived copy of an imported item) would reuse it."""
    created_hash, created_path = set(), set()
    for iid in sorted(rows):
        res = rows[iid].get('result')
        if not res or res.get('decision') != 'import':
            continue
        it = items[iid]
        src = (it.get('metadata') or {}).get('derived_from')
        if it.get('content_hash') in created_hash or (src and src in created_path):
            res['library_action'] = 'would_reuse'
        else:
            res['library_action'] = 'would_create'
            created_hash.add(it.get('content_hash')); created_path.add(it['path'])
    with open(path('work', 'deep_rows.jsonl'), 'w') as fh:
        for iid in sorted(rows):
            fh.write(json.dumps(rows[iid], ensure_ascii=False) + '\n')


# ---------- write tables ----------

def write():
    gc_path, an_path = os.path.join(DATA, 'generated_categories.json'), os.path.join(DATA, 'analyses.json')
    gc, an = json.load(open(gc_path)), json.load(open(an_path))
    if any(r.get('run_id') == RUN_ID for r in gc + an):
        sys.exit(f'{RUN_ID} rows already present; not appending twice')
    cats = json.load(open(path('work', 'catsets.json')))
    w2, rs, dp = load_rows('wave2_rows.jsonl'), load_rows('resort_rows.jsonl'), load_rows('deep_rows.jsonl')
    ids = json.load(open(os.path.join(RUN, 'sample.json')))['item_ids']
    rows = [w2[i] for i in ids if i in w2] + [rs[i] for i in ids if i in rs] + [dp[i] for i in ids if i in dp]
    json.dump(gc + cats, open(gc_path, 'w'), indent=1, ensure_ascii=False)
    json.dump(an + rows, open(an_path, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({'generated_categories_appended': len(cats), 'analyses_appended': len(rows),
                      'wave2_rows': sum(1 for r in rows if r['stage'] == 'wave2_shallow'),
                      'resort_rows': sum(1 for r in rows if r['stage'] == 'wave2_resort'),
                      'deep_rows': sum(1 for r in rows if r['stage'] == 'deep')}))


if __name__ == '__main__':
    {'wave1': wave1, 'wave2': wave2, 'new_categories': new_categories, 'resort': resort, 'deep': deep,
     'write': write}[sys.argv[1]]()
