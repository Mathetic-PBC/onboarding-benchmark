"""Turn one onboarding done in Engelbart's own UI into a benchmark run.

  BENCH_RUN=run_002 python3 -I run/from_engelbart.py [--data-root ~/.engelbart] [--session <id>]
                                                    [--app-repo ~/Desktop/engelbart-canvas] [--write]

Run it right after onboarding, on a data root that started empty, with Engelbart closed. It reads what Engelbart already
keeps in the data root:
  .connect/<session>/session.json   the onboarding session: the model chosen, the sources picked, each job and its counts
  .connect/trace/<day>.jsonl        every agent turn (prompt, input, steps, answer) and each step of dispatching
  .connect/imported-log.jsonl       each key brought in, with the session and job that brought it and its library rows
  .connect/imported.json            the same keys, for the whole data root (used only when the log isn't there)
  .connect/discovery.json           the recent-projects and tools discovery agents' answers
  .connect/scenario.json            what run/engelbart_scenario.cjs ran (absent for a run done by hand in the UI)
It copies them to runs/<run>/engelbart/ (real content, never committed) and writes runs/<run>/work/engelbart.json: the
run's `runs` row, a `generated_categories` row for the projects discovery named, and `analyses` rows: one per imported
item (decision import), and one per item an agent listed but didn't bring in (decision skip, with the tool's reason when it
gave one), matched to its source_items row where the key names it. Without --write it only prints counts. --write appends
the rows to benchmark-data's tables and adds the runs row to this repo's dataset/tables/runs.json.

The trace's token counts, cost, prompt hashes, tool calls and the import log come from Engelbart's onboarding-bench-recording
branch (2026-10-19). On an older build they're missing and those fields stay empty.
"""
import argparse, collections, datetime, glob, hashlib, json, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(__file__))
from config import DATA, DATASET_ID, RUN, RUN_ID

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = re.compile(r'[A-Za-z0-9][A-Za-z0-9_\-.]{7,}|\b[A-Z][A-Z0-9]+-\d+\b')   # long ids, and issue ids (MATH-92)
COMMON = 5          # a token found in more source items than this names none of them


def load(p, default=None):
    try:
        return json.load(open(p))
    except (OSError, ValueError):
        return default


def minutes(a, b):
    if not a or not b:
        return None
    t = lambda s: datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
    return round((t(b) - t(a)).total_seconds() / 60, 1)


# ---------- reading the data root ----------

def pick_session(root, sid):
    sessions = [s for s in (load(p) for p in glob.glob(os.path.join(root, '.connect', '*', 'session.json'))) if s]
    if not sessions:
        sys.exit(f'no onboarding session in {root}/.connect')
    if sid:
        return next((s for s in sessions if s['id'] == sid), None) or sys.exit(f'no session {sid}'), len(sessions)
    return max(sessions, key=lambda s: s.get('created') or ''), len(sessions)


def trace_of(root, session):
    """The session's trace entries (last version of each), plus discovery's, which run before a session exists."""
    entries = {}
    for f in sorted(glob.glob(os.path.join(root, '.connect', 'trace', '*.jsonl'))):
        for line in open(f):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            entries[e['id']] = e
    jobs = {j['id'] for j in session.get('jobs') or []}
    ends = [j.get('ended') for j in session.get('jobs') or [] if j.get('ended')]
    last = max(ends) if ends else None
    keep = []
    for e in entries.values():
        mine = e.get('sessionId') == session['id'] or e.get('jobId') in jobs
        before = e.get('sessionId') is None and (last is None or e['at'] <= last)
        if mine or before:
            keep.append(e)
    return sorted(keep, key=lambda e: e['at'])


def imported_of(root, session):
    """→ [{key, at, jobId, rows}] brought in by this session; from imported.json (whole data root) on an older build."""
    log = os.path.join(root, '.connect', 'imported-log.jsonl')
    if os.path.exists(log):
        out = []
        for line in open(log):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get('sessionId') == session['id']:
                # a row with no key of its own (a PDF, a folder, a link) is named by what it was added from
                out.append({**e, 'key': e.get('key') or e.get('what')})
        # a keyed item's own rows are logged twice (the key, and each row): one entry an item, the key's
        seen_rows, kept = set(), []
        for e in sorted(out, key=lambda e: bool(e.get('what'))):   # keyed entries first
            rows = set(e.get('rows') or [])
            if e.get('what') and rows and rows <= seen_rows:
                continue
            seen_rows |= rows
            kept.append(e)
        return kept, 'imported-log'
    return [{'key': k, 'at': None, 'jobId': None, 'rows': []} for k in load(os.path.join(root, '.connect', 'imported.json'), [])], 'imported.json'


# ---------- what the agents listed and left out (the trace's tool calls) ----------

ID_FIELDS = ('id', 'key', 'path', 'file', 'url', 'link', 'thread', 'source')
LIST_FIELDS = ('ids', 'keys', 'files', 'paths', 'threads', 'urls')


def detail_of(e):
    d = e.get('detail')
    if isinstance(d, str):
        try:
            return json.loads(d)
        except ValueError:
            return None   # cut in the middle: too long a listing
    return d


def entries_in(value, depth=0):
    """Every object in a tool result that names a thing (has an id, a path, a link...)."""
    if depth > 6:
        return
    if isinstance(value, dict):
        if any(isinstance(value.get(f), str) for f in ID_FIELDS):
            yield value
        for k, v in value.items():
            if k in LIST_FIELDS and isinstance(v, list):   # a listing of bare paths or ids
                yield from ({'path' if k in ('files', 'paths') else 'id': x} for x in v if isinstance(x, str))
            elif isinstance(v, (dict, list)):
                yield from entries_in(v, depth + 1)
    elif isinstance(value, list):
        for v in value:
            yield from entries_in(v, depth + 1)


def asked_in(args):
    """The ids an import tool was asked to bring in."""
    out = []
    for f in LIST_FIELDS:
        for v in (args or {}).get(f) or []:
            out.append(v.get('id') if isinstance(v, dict) else v)
    return [v for v in out if isinstance(v, str)]


def tool_calls(trace):
    """→ seen {handle: (entry, tool, jobId)}, asked {handle: (tool, jobId)}, why {handle: reason}, calls Counter,
    added [(handle, tool, jobId, at)]: what an import call says it brought in (all it was asked for but what it skipped,
    when its count says so), for a run whose import log has no keyless rows (a build before 2026-10-19 evening)."""
    seen, asked, why, calls, added = {}, {}, {}, collections.Counter(), []
    for e in trace:
        if e['type'] != 'event' or e.get('kind') != 'tool':
            continue
        name, d = e.get('text'), detail_of(e) or {}
        calls[name] += 1
        if name.startswith(('import_', 'add_')):
            args, result = d.get('args') or {}, d.get('result') or {}
            mine = asked_in(args) or ([args['input']] if isinstance(args.get('input'), str) else [])
            for h in mine:
                asked[h] = (name, e.get('jobId'))
            gone = set()
            for sk in result.get('skipped') or []:
                h = next((sk.get(f) for f in ('id', 'key', 'file') if isinstance(sk.get(f), str)), None)
                if h:
                    why[h] = sk.get('why')
                    gone.add(h)
            n = result.get('added')
            kept = [h for h in mine if h not in gone and h not in (result.get('left') or [])]
            if n is True or (isinstance(n, int) and not isinstance(n, bool) and n == len(kept) and n):
                added += [(h, name, e.get('jobId'), e.get('at')) for h in kept]
            continue
        for x in entries_in(d.get('result')):
            h = next(x[f] for f in ID_FIELDS if isinstance(x.get(f), str))
            seen.setdefault(h, (x, name, e.get('jobId')))
    return seen, asked, why, calls, added


# ---------- matching imported keys to source_items ----------

def handles(r):
    """Strings that name a source item: its ids, link, original path, file name, and its long tokens."""
    meta = r.get('metadata') or {}
    out = {r.get('source_id'), r.get('source_url'), meta.get('original_path')}
    for p in (r.get('path') or '', meta.get('original_path') or ''):
        base = os.path.basename(p.rstrip('/'))
        out.add(base)
        out.add(os.path.splitext(base)[0])
    toks = set()
    for s in list(out):
        if s:
            toks.update(TOKEN.findall(s))
    return {s for s in out if s}, toks


def build_index(items):
    exact, by_tok, df = {}, collections.defaultdict(set), collections.Counter()
    derived = {r['id'] for r in items if '/derived/' in (r.get('path') or '')}
    for r in items:
        hs, toks = handles(r)
        for h in hs:
            exact.setdefault(os.path.expanduser(h), set()).add(r['id'])
        for t in toks:
            by_tok[t].add(r['id'])
    for t, ids in by_tok.items():
        df[t] = len(ids)
    return exact, by_tok, df, derived


def match(key, exact, by_tok, df, derived=frozenset()):
    """→ (item_id or None, how). Exact handles first (a path, a link, an id); then the item sharing the most rare tokens."""
    rest = key.split(':', 1)[1] if re.match(r'^(chat|note|file|page|paper|item):', key) else key
    for cand in (rest, rest.split(':', 1)[-1], os.path.basename(rest.rstrip('/'))):
        ids = exact.get(os.path.expanduser(cand)) or set()
        if len(ids) > 1:
            ids = (ids - derived) or ids   # a Claude Code session and its derived index: the session
        if len(ids) == 1:
            return next(iter(ids)), 'exact'
    score = collections.Counter()
    for t in set(TOKEN.findall(key)):
        if 0 < df[t] <= COMMON:
            for i in by_tok[t]:
                score[i] += 1
    if not score:
        return None, 'none'
    if len(score) > 1:
        for i in derived & set(score):
            del score[i]
    (best, n), *others = score.most_common(2) + [(None, 0)]
    if others and others[0][1] == n:
        return None, 'ambiguous'
    return best, 'tokens'


# ---------- rows ----------

def app_version(repo):
    git = lambda *a: subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True).stdout.strip()
    return {'repo': os.path.basename(repo), 'branch': git('rev-parse', '--abbrev-ref', 'HEAD') or None,
            'commit': git('rev-parse', '--short', 'HEAD') or None, 'dirty': bool(git('status', '--porcelain'))}


def hash_of(e):
    return e.get('systemHash') or hashlib.sha256((e.get('system') or '').encode()).hexdigest()[:12]


def performance(session, trace):
    turns = [e for e in trace if e['type'] == 'turn']
    blank = lambda: {'turns': 0, 'failed': 0, 'minutes': 0.0, 'input_tokens': 0, 'cache_read_tokens': 0,
                     'output_tokens': 0, 'cost_usd': 0.0, 'turns_without_usage': 0}
    by_kind = collections.defaultdict(blank)
    total = blank()
    for e in turns:
        u = e.get('usage')
        for k in (by_kind[e['kind']], total):
            k['turns'] += 1
            k['failed'] += e['status'] == 'failed'
            k['minutes'] = round(k['minutes'] + (minutes(e['at'], e.get('ended')) or 0), 1)
            if not u:
                k['turns_without_usage'] += 1
                continue
            k['input_tokens'] += u.get('input') or 0
            k['cache_read_tokens'] += u.get('cacheRead') or 0
            k['output_tokens'] += u.get('output') or 0
            k['cost_usd'] = round(k['cost_usd'] + (u.get('costUsd') or 0), 4)
    with_usage = total['turns'] - total['turns_without_usage']
    starts = [e['at'] for e in turns] + [session.get('created')]
    ends = [e.get('ended') for e in turns if e.get('ended')] + [j.get('ended') for j in session.get('jobs') or [] if j.get('ended')]
    return {'minutes': minutes(min(filter(None, starts)), max(ends)) if ends else None,
            'turns': len(turns), 'failed_turns': total['failed'],
            'by_kind': dict(by_kind),
            # None when no turn reported usage (a build before 2026-10-19); Codex reports tokens, no cost
            'input_tokens': total['input_tokens'] if with_usage else None,
            'cache_read_tokens': total['cache_read_tokens'] if with_usage else None,
            'output_tokens': total['output_tokens'] if with_usage else None,
            'cost_usd': total['cost_usd'] if with_usage else None,
            'turns_without_usage': total['turns_without_usage']}


def prompts_of(trace):
    """Each kind of agent's system prompt hashes, so two runs tell whether a prompt changed."""
    out = collections.defaultdict(set)
    for e in trace:
        if e['type'] == 'turn':
            out[e['kind']].add(hash_of(e))
    return {k: sorted(v) for k, v in sorted(out.items())}


def match_entry(h, x, exact, by_tok, df, derived):
    """A listed thing → (item_id, how): its id first, then its path or link, then its title."""
    for cand in [h] + [x.get(f) for f in ('path', 'url', 'link', 'title', 'name', 'subject') if isinstance(x.get(f), str)]:
        iid, m = match(cand, exact, by_tok, df, derived)
        if iid:
            return iid, m
    return None, 'none'


def rows_for(session, trace, discovery, imported, items, app, root, scenario=None):
    exact, by_tok, df, derived = build_index(items)
    choice = session.get('choice') or {}
    model = choice.get('modelName') or choice.get('model')
    jobs_by_id = {j['id']: j for j in session.get('jobs') or []}
    row = lambda n, iid, at, job_id, config, result: {
        'id': f'{RUN_ID}_eb_{n:05d}', 'item_id': iid, 'run_id': RUN_ID, 'dataset_id': DATASET_ID,
        'parent_analysis_id': None, 'category_set_id': None, 'content_hash': None,
        'stage': 'engelbart_import', 'status': 'completed', 'error': None,
        'started_at': at, 'completed_at': at, 'model': model,
        'prompt_version': f"engelbart@{app['commit']}",
        'config': {**config, 'job': job_id, 'job_kind': (jobs_by_id.get(job_id) or {}).get('kind')},
        'sample': None, 'result': result, 'usage': None}
    analyses, how = [], collections.Counter()
    got = set()
    for e in imported:
        key = e['key']
        iid, m = match(key, exact, by_tok, df, derived)
        how[m] += 1
        got.add(iid)
        analyses.append(row(len(analyses) + 1, iid, e.get('at'), e.get('jobId'), {'engelbart_key': key, 'match': m},
                            {'decision': 'import', 'project_assignments': [], 'library_key': key,
                             'library_rows': e.get('rows') or []}))
    # What an import call brought in that the import log doesn't name (a PDF, a folder or a link, on an older build).
    seen, asked, why, calls, tool_added = tool_calls(trace)
    keys = [e['key'] for e in imported]
    from_calls = 0
    for h, tool, job_id, at in tool_added:
        iid, m = match(h, exact, by_tok, df, derived)
        if (iid and iid in got) or (not iid and any(k.endswith(h) for k in keys)):
            continue
        got.add(iid)
        from_calls += 1
        how[m] += 1
        analyses.append(row(len(analyses) + 1, iid, at, job_id, {'engelbart_handle': h, 'from': tool, 'match': m},
                            {'decision': 'import', 'project_assignments': [], 'library_key': None}))
    # What an agent listed and didn't bring in: a skip, with the tool's reason when it was asked to and refused.
    skipped = collections.Counter()
    for h, (x, tool, job_id) in seen.items():
        iid, m = match_entry(h, x, exact, by_tok, df, derived)
        if iid is None or iid in got:
            continue
        got.add(iid)
        reason = why.get(h) or ('asked for, not brought in' if h in asked else 'listed, not chosen')
        skipped[reason if h in asked else 'listed, not chosen'] += 1
        analyses.append(row(len(analyses) + 1, iid, None, job_id, {'engelbart_handle': h, 'listed_by': tool, 'match': m},
                            {'decision': 'skip', 'reason': reason, 'project_assignments': []}))
    proj = (discovery or {}).get('projects') or {}
    cats = []
    if proj.get('projects'):
        cats.append({'id': f'{RUN_ID}_discovery', 'run_id': RUN_ID, 'dataset_id': DATASET_ID,
                     'categories': [{'id': p.get('id'), 'name': p.get('title'), 'description': p.get('description'),
                                     'source': 'engelbart-discovery', 'flag': None} for p in proj['projects']],
                     'created_at': proj.get('ended') or proj.get('started'), 'model': model,
                     'prompt_version': f"engelbart@{app['commit']}", 'inputs': {'from': proj.get('from')}})
    jobs = session.get('jobs') or []
    sources = {k: sorted(v.get('apps') or []) or (['on'] if v.get('on') else [])
               for k, v in ((session.get('choices') or {}).get('sources') or {}).items() if (v or {}).get('on')}
    # a manual run's choices hold no `direct` (the librarian takes them over): its mode comes from the scenario's input
    direct = (session.get('choices') or {}).get('direct') or ((scenario or {}).get('input') or {}).get('direct') or {}
    run = {'id': RUN_ID, 'dataset_id': DATASET_ID,
           'date': (session.get('created') or '')[:10],
           'config': {'runner': 'engelbart-script' if scenario else 'engelbart-ui',
                      'scenario': ((scenario or {}).get('scenario') or {}).get('name'),
                      'mode': direct.get('mode'),  # manual: the person picked the sources; auto: agents found the tools
                      'engelbart': app,
                      'provider': choice.get('provider'), 'model': model, 'effort': choice.get('effort'),
                      'agent': choice.get('name'), 'permissions': session.get('permissions'),
                      'sources_picked': sources, 'custom_instructions': bool((session.get('choices') or {}).get('custom')),
                      'data_root': root,
                      'prompts': prompts_of(trace)},
           'results': {'categories': sum(len(c['categories']) for c in cats),
                       'jobs': dict(collections.Counter(f"{j['kind']}:{j['status']}" for j in jobs)),
                       'notes': (session.get('counts') or {}).get('notes'),
                       'items': (session.get('counts') or {}).get('items'),
                       'imported': len(imported) + from_calls, 'imported_from_tool_calls': from_calls,
                       'matched_to_source_items': len(imported) + from_calls - how['none'] - how['ambiguous'],
                       'match': dict(how),
                       'listed': len(seen), 'skipped_matched': dict(skipped), 'tool_calls': dict(calls)},
           'performance': performance(session, trace),
           'scored': False}
    return run, cats, analyses


# ---------- scoring: what the current onboarding does, without the waves ----------
# Engelbart's onboarding has no wave 1, 2 or deep pass: it names up to 5 recent projects and brings in what pertains to
# them, sorting nothing into categories. So it is scored on what it does: which of the person's projects it named
# (against ground_truth_projects, judged by one headless call), how much of each source it reached, and how its
# import/skip decisions agree with run_001's deep pass, the reference for what is worth bringing in.

NOT_SCORED = {'No project', 'Hint-timing pilot (synthetic only)'}
MATCH_PROMPT = """You match the projects an onboarding agent named for a person against the person's own list of their
projects. For each named project, give the id of the one project on the list it is (the same work, even if named
differently or more narrowly), or null if it is none of them. Two named projects may be the same listed project.
Return JSON only: {"matches": [{"named": "<named title>", "project_id": "<id or null>", "why": "<at most 15 words>"}]}"""


def match_projects(named, truth):
    """→ ([{named, project_id, why}], cost) from one headless call, or None when it fails."""
    if not named:
        return [], 0
    stdin = json.dumps({'named': named, 'list': [{'id': p['id'], 'name': p['name'], 'description': p['description']}
                                                   for p in truth]}, ensure_ascii=False)
    cmd = ['claude', '-p', '--model', 'claude-sonnet-5-5', '--setting-sources', '', '--strict-mcp-config',
           '--disable-slash-commands', '--no-session-persistence', '--tools', '', '--output-format', 'json',
           '--system-prompt', MATCH_PROMPT]
    try:
        p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=600,
                           env={**os.environ, 'CLAUDE_CODE_DISABLE_AUTO_MEMORY': '1'}, cwd=tempfile.mkdtemp(prefix='bench-score-'))
        out = json.loads(p.stdout)
        text = re.sub(r'^```(?:json)?\s*|\s*```$', '', out['result'].strip())
        return json.loads(text)['matches'], round(out.get('total_cost_usd') or 0, 4)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as e:
        print(f'note: the project match call failed ({e}); results.score.projects left empty')
        return None


def score(cats, analyses, items, truth, reference, call_model=True):
    by_id = {r['id']: r for r in items}
    real = [p for p in truth if p['name'] not in NOT_SCORED]
    named = [c['name'] for c in (cats[0]['categories'] if cats else [])]
    got = match_projects(named, real) if call_model else None
    matches, cost = got if got is not None else (None, None)
    projects = None
    if matches is not None:
        hit = {m['project_id'] for m in matches if m.get('project_id')}
        projects = {'named': len(named), 'named_real': sum(1 for m in matches if m.get('project_id')),
                    'found': len(hit), 'of': len(real), 'recall': round(len(hit) / len(real), 3) if real else None,
                    'precision': round(sum(1 for m in matches if m.get('project_id')) / len(named), 3) if named else None,
                    'missed': sorted(p['name'] for p in real if p['id'] not in hit),
                    'matches': matches, 'judge': 'claude-sonnet-5-5', 'judge_cost_usd': cost,
                    'note': 'discovery names at most 5 projects, so recall is capped at 5 of the list'}
    # how far it reached into each source
    per = collections.defaultdict(lambda: {'items': 0, 'imported': 0, 'skipped': 0})
    for r in items:
        per[r.get('source')]['items'] += 1
    for a in analyses:
        src = (by_id.get(a['item_id']) or {}).get('source')
        if src:
            per[src]['imported' if a['result']['decision'] == 'import' else 'skipped'] += 1
    # against run_001's deep pass: the items it read in full and decided on
    deep = {a['item_id']: a['result'].get('decision') for a in reference
            if a.get('stage') == 'deep' and a.get('result') and a['result'].get('decision') in ('import', 'skip')}
    mine = {a['item_id']: a['result']['decision'] for a in analyses if a['item_id']}
    both = [i for i in deep if i in mine]
    agree = sum(deep[i] == mine[i] for i in both)
    deep_import = {i for i, d in deep.items() if d == 'import'}
    return {'projects': projects,
            'by_source': {k: v for k, v in sorted(per.items(), key=lambda kv: -kv[1]['items'])},
            'sources_reached': sorted(k for k, v in per.items() if v['imported']),
            'vs_run_001_deep_pass': {
                'deep_pass_items': len(deep), 'deep_pass_imports': len(deep_import),
                'decided_by_both': len(both), 'agree': agree,
                'agreement': round(agree / len(both), 3) if both else None,
                'deep_imports_onboarding_also_imported': sum(mine.get(i) == 'import' for i in deep_import),
                'deep_imports_onboarding_skipped': sum(mine.get(i) == 'skip' for i in deep_import),
                'deep_imports_onboarding_never_saw': sum(i not in mine for i in deep_import),
                'onboarding_imports_deep_skipped': sum(deep.get(i) == 'skip' and d == 'import' for i, d in mine.items())}}


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-root', default=os.path.expanduser('~/.engelbart'))
    ap.add_argument('--session')
    ap.add_argument('--app-repo', default=os.path.expanduser('~/Desktop/engelbart-canvas'))
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--no-judge', action='store_true', help='skip the headless call that matches named projects')
    a = ap.parse_args()
    root = os.path.expanduser(a.data_root)
    session, n_sessions = pick_session(root, a.session)
    trace = trace_of(root, session)
    imported, imported_from = imported_of(root, session)
    discovery = load(os.path.join(root, '.connect', 'discovery.json'))
    scenario = load(os.path.join(root, '.connect', 'scenario.json'))
    items = load(os.path.join(DATA, 'source_items.json'), [])
    run, cats, analyses = rows_for(session, trace, discovery, imported, items, app_version(a.app_repo), root, scenario)
    truth = load(os.path.join(DATA, 'ground_truth_projects.json'), [])
    reference = [r for r in load(os.path.join(DATA, 'analyses.json'), []) if r.get('run_id') == 'run_001']
    run['results']['score'] = score(cats, analyses, items, truth, reference, call_model=not a.no_judge)
    run['scored'] = run['results']['score']['projects'] is not None
    summary = {'session': session['id'], 'sessions_in_data_root': n_sessions, 'trace_entries': len(trace),
               'runner': run['config']['runner'], 'scenario': run['config']['scenario'], 'mode': run['config']['mode'],
               'categories': run['results']['categories'], 'imported': run['results']['imported'],
               'imported_from': imported_from, 'imported_from_tool_calls': run['results']['imported_from_tool_calls'],
               'match': run['results']['match'], 'listed': run['results']['listed'],
               'skipped_matched': run['results']['skipped_matched'], 'jobs': run['results']['jobs'],
               'prompts': run['config']['prompts'], 'performance': run['performance'], 'score': run['results']['score']}
    print(json.dumps(summary, indent=1))
    days = sorted({e['at'][:10] for e in trace})
    if days and (datetime.date.today() - datetime.date.fromisoformat(days[0])).days >= 12:
        print('note: Engelbart keeps 14 days of trace; this run is close to that, so --write it now')
    if n_sessions > 1 and imported_from == 'imported.json':
        print('note: this data root holds more than one onboarding session; imported.json covers all of them, so start '
              'each benchmark run from an empty data root')
    if not a.write:
        return
    raw = os.path.join(RUN, 'engelbart')
    os.makedirs(raw, exist_ok=True)
    shutil.copy(os.path.join(root, '.connect', session['id'], 'session.json'), raw)
    for name in ('imported.json', 'imported-log.jsonl', 'discovery.json', 'onboarding.json', 'scenario.json'):
        if os.path.exists(os.path.join(root, '.connect', name)):
            shutil.copy(os.path.join(root, '.connect', name), raw)
    with open(os.path.join(raw, 'trace.jsonl'), 'w') as fh:
        for e in trace:
            fh.write(json.dumps(e, ensure_ascii=False) + '\n')
    os.makedirs(os.path.join(RUN, 'work'), exist_ok=True)
    json.dump({'run': run, 'generated_categories': cats, 'analyses': analyses},
              open(os.path.join(RUN, 'work', 'engelbart.json'), 'w'), indent=1, ensure_ascii=False)
    gc_path, an_path = os.path.join(DATA, 'generated_categories.json'), os.path.join(DATA, 'analyses.json')
    gc, an = load(gc_path, []), load(an_path, [])
    if any(r.get('run_id') == RUN_ID for r in gc + an):
        sys.exit(f'{RUN_ID} rows already present; not appending twice')
    json.dump(gc + cats, open(gc_path, 'w'), indent=1, ensure_ascii=False)
    json.dump(an + analyses, open(an_path, 'w'), indent=1, ensure_ascii=False)
    runs_path = os.path.join(REPO, 'dataset', 'tables', 'runs.json')
    runs = [r for r in load(runs_path, []) if r['id'] != RUN_ID] + [{**run, 'config': {**run['config'], 'data_root': None}}]
    with open(runs_path, 'w') as fh:
        json.dump(runs, fh, indent=1)
        fh.write('\n')
    print(f'wrote {len(cats)} generated_categories, {len(analyses)} analyses rows and the runs row for {RUN_ID}')


if __name__ == '__main__':
    main()
