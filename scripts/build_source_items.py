"""Build <side>/<source>/source_items.json for every source folder (format agreed with the user 2026-10-17), plus the
aggregate benchmark-data/source_items.json. Item ids are stable across reruns via _scripts/item_ids.json.

One item = what an importer should bring in as a unit (a chat, a coding session with its subagent/tool-result files as
parts, a note, a PDF, a repo, an email, a meeting). Collection artifacts (_collection/, MANIFEST.csv, source_items.json)
are not items. ground_truth.status is exactly one of: unlabeled (default for authentic items), generated (synthetic items:
project_ids set by the generator in synthetic/ground_truth_labels.json, {source: {item key: {project_ids, notes}}}),
reviewed (checked by David; set by hand, never by this script). library_item_id is null until Engelbart imports the item;
synthetic rows also carry modeled_on from their manifest. Collection notes go in metadata.collection_notes. Files are plain JSON arrays.

usage: python3 build_source_items.py [side/source ...]   (default: every folder)
"""
import csv, datetime, glob, hashlib, json, os, re, subprocess, sys

ROOT = os.path.expanduser('~/Desktop/benchmark/benchmark-data')
DATASET = 'benchmark_001'
IDS = os.path.join(ROOT, '_scripts', 'item_ids.json')
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
SKIP_NAMES = {'MANIFEST.csv', 'source_items.json', '.DS_Store'}

# ---------- helpers ----------

def utc(ts):
    """epoch seconds / ms / ISO string -> ISO-8601 UTC 'Z' string."""
    if ts in (None, ''):
        return None
    if isinstance(ts, (int, float)):
        if ts > 1e11: ts = ts / 1000
        return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    s = str(ts).strip()
    try:
        d = datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.astimezone()  # naive = this Mac's local time
    return d.astimezone(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def sha_file(p, h=None):
    h = h or hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h


def content_hash(files, base):
    files = sorted(files)
    if len(files) == 1:
        return 'sha256:' + sha_file(files[0]).hexdigest()
    h = hashlib.sha256()
    for p in files:
        h.update(os.path.relpath(p, base).encode() + b'\0' + sha_file(p).hexdigest().encode() + b'\n')
    return 'sha256:' + h.hexdigest()


def fstat_dates(p, original=None):
    s = os.stat(original if original and os.path.exists(original) else p)
    created = getattr(s, 'st_birthtime', None) or s.st_mtime
    return utc(created), utc(os.stat(p).st_mtime)


def language_of(p, limit=20000):
    try:
        with open(p, 'rb') as f: raw = f.read(limit)
        t = raw.decode('utf-8')
    except Exception:
        return None
    letters = [c for c in t if c.isalpha()]
    if len(letters) < 20: return None
    return 'en' if sum(c.isascii() for c in letters) / len(letters) > 0.97 else None


EXT_TYPE = {
    'md': 'note', 'markdown': 'note', 'txt': 'note', 'rtf': 'note', 'canvas': 'note', 'base': 'note',
    'docx': 'document', 'doc': 'document', 'pages': 'document', 'odt': 'document', 'html': 'web_page', 'htm': 'web_page',
    'pdf': 'pdf', 'pptx': 'slides', 'key': 'slides', 'xlsx': 'spreadsheet', 'numbers': 'spreadsheet', 'csv': 'data',
    'json': 'data', 'jsonl': 'data', 'tsv': 'data', 'rda': 'data', 'sqlite': 'database', 'zip': 'archive', 'eml': 'email',
    'png': 'image', 'jpg': 'image', 'jpeg': 'image', 'heic': 'image', 'svg': 'image', 'gif': 'image', 'eps': 'image', 'ai': 'image',
    'wav': 'audio', 'mp3': 'audio', 'm4a': 'audio', 'flp': 'audio', 'mp4': 'video', 'mov': 'video', 'tex': 'latex', 'bib': 'bibtex', 'ris': 'bibtex',
    'enex': 'note', 'vtt': 'transcript', 'srt': 'transcript',
}
CODE_EXT = {'py', 'js', 'ts', 'tsx', 'jsx', 'cjs', 'mjs', 'r', 'sh', 'swift', 'css', 'scss', 'sql', 'toml', 'yaml', 'yml', 'sty'}


def ext_of(p):
    b = os.path.basename(p)
    return b.rsplit('.', 1)[-1].lower() if '.' in b else ''


def type_of(p):
    e = ext_of(p)
    return EXT_TYPE.get(e) or ('code' if e in CODE_EXT else 'file')


def read_manifest(d):
    f = os.path.join(d, 'MANIFEST.csv')
    if not os.path.exists(f): return {}
    with open(f, newline='') as fh:
        return {r['path']: r for r in csv.DictReader(fh)}


def iter_jsonl(p):
    with open(p, errors='replace') as f:
        for line in f:
            try: yield json.loads(line)
            except Exception: continue


def text_of(content):
    if isinstance(content, str): return content
    if isinstance(content, list):
        return ' '.join(c.get('text', '') for c in content if isinstance(c, dict) and c.get('type') in ('text', 'input_text', 'output_text'))
    return ''


def short(s, n=90):
    s = re.sub(r'\s+', ' ', s or '').strip()
    return s if len(s) <= n else s[:n - 1] + '…'

# ---------- itemizers: each yields dicts with keys
# key, source_id, title, content_type, created_at, modified_at, main (abs path), files (abs), source_url, metadata, notes

def files_under(d):
    out = []
    for p in glob.glob(os.path.join(d, '**', '*'), recursive=True) + glob.glob(os.path.join(d, '**', '.*'), recursive=True):
        if os.path.isfile(p) and os.path.basename(p) not in SKIP_NAMES:
            out.append(p)
    return sorted(set(out))


def generic_files(d, man, tool):
    """One item per file (skipping _collection/)."""
    for p in files_under(d):
        rel = os.path.relpath(p, d)
        if '_collection' in rel.split('/'): continue
        r = man.get(rel, {})
        orig = os.path.expanduser(r['source']) if r.get('source', '').startswith('~/') else None
        c, m = fstat_dates(p, orig)
        yield dict(key=rel, source_id=r.get('source') or rel, title=os.path.basename(p), content_type=type_of(p), created_at=c, modified_at=m,
                   main=p, files=[p], source_url=r['source'] if r.get('source', '').startswith('http') else None,
                   metadata={'account': r.get('account_or_library') or None, 'original_path': r.get('source') or None}, notes=r.get('notes', ''))


def claude_code(d, man):
    for p in sorted(glob.glob(f'{d}/projects/*/*.jsonl')):
        sid = os.path.basename(p)[:-6]
        sub = p[:-6]
        parts = files_under(sub) if os.path.isdir(sub) else []
        first = last = None; title = None; first_prompt = None; n = 0; cwd = None; branch = None; entry = None; version = None
        for o in iter_jsonl(p):
            t = o.get('timestamp')
            if t: first = first or t; last = t
            typ = o.get('type')
            if typ in ('summary',) and o.get('summary'): title = title or o['summary']
            if typ in ('custom-title', 'ai-title') and (o.get('customTitle') or o.get('aiTitle') or o.get('title')): title = o.get('customTitle') or o.get('aiTitle') or o.get('title')
            if typ in ('user', 'assistant') and not o.get('isMeta'):
                n += 1
                cwd = cwd or o.get('cwd'); branch = branch or o.get('gitBranch'); entry = entry or o.get('entrypoint'); version = version or o.get('version')
                if typ == 'user' and first_prompt is None:
                    tx = text_of((o.get('message') or {}).get('content'))
                    if tx and not tx.startswith('<'): first_prompt = tx
        r = man.get(os.path.relpath(p, d), {})
        yield dict(key=os.path.relpath(p, d), source_id=sid, title=short(title or first_prompt or sid), content_type='conversation',
                   created_at=utc(first), modified_at=utc(last) or fstat_dates(p)[1], main=p, files=[p] + parts, source_url=None,
                   metadata={'message_count': n, 'account': 'Claude Code CLI (~/.claude/projects)', 'project_dir': os.path.basename(os.path.dirname(p)),
                             'cwd': cwd, 'git_branch': branch, 'entrypoint': entry, 'cli_version': version,
                             'parts': [os.path.relpath(x, ROOT) for x in parts], 'subagent_count': sum(1 for x in parts if '/subagents/' in x and x.endswith('.jsonl')),
                             'original_path': r.get('source')}, notes='')
    for p in [f'{d}/claude-home/history.jsonl'] + sorted(glob.glob(f'{d}/claude-home/plans/*')):
        if not os.path.exists(p): continue
        c, m = fstat_dates(p)
        hist = p.endswith('history.jsonl')
        yield dict(key=os.path.relpath(p, d), source_id=os.path.relpath(p, d), title='Claude Code prompt history' if hist else os.path.basename(p),
                   content_type='prompt_history' if hist else 'note', created_at=c, modified_at=m, main=p, files=[p], source_url=None,
                   metadata={'account': '~/.claude', 'message_count': sum(1 for _ in open(p)) if hist else None}, notes='')
    for p in sorted(glob.glob(f'{d}/claude-desktop-code-sessions/**/*.json', recursive=True)):
        c, m = fstat_dates(p)
        try: j = json.load(open(p))
        except Exception: j = {}
        yield dict(key=os.path.relpath(p, d), source_id=j.get('sessionId', os.path.basename(p)), title=j.get('title') or os.path.basename(p),
                   content_type='session_metadata', created_at=utc(j.get('createdAt')) or c, modified_at=utc(j.get('lastActivityAt')) or m, main=p, files=[p],
                   source_url=None, metadata={'account': 'Claude desktop app', 'cli_session_id': j.get('cliSessionId'), 'cwd': j.get('cwd')}, notes='desktop Code-tab metadata; transcript is under projects/')
    # claude-vault derived indexes: one item per chat-session dir / dated session dir; loose files one item each
    for vault in sorted(glob.glob(f'{d}/derived/*')) + sorted(glob.glob(f'{d}/derived/vault-backups/*')):
        if vault.endswith('vault-backups'): continue
        cs = f'{vault}/chat-sessions'
        units = [x for x in glob.glob(f'{cs}/*') if os.path.isdir(x)] + [x for x in glob.glob(f'{vault}/sessions/*/*') if os.path.isdir(x)]
        loose = [x for x in files_under(vault) if not any(x.startswith(u + '/') for u in units)]
        for u in sorted(units):
            fs = files_under(u)
            if not fs: continue
            mf = os.path.join(u, 'manifest.json'); pr = os.path.join(u, 'prompts.json')
            meta = {}
            try: meta = json.load(open(mf))
            except Exception: pass
            title = None
            try: title = (json.load(open(pr)).get('prompts') or [{}])[0].get('text')
            except Exception: pass
            c, m = fstat_dates(fs[0])
            yield dict(key=os.path.relpath(u, d), source_id=meta.get('session_id', os.path.basename(u)), title=short(title or os.path.basename(u)),
                       content_type='derived_session_index', created_at=utc(meta.get('created_at')) or c, modified_at=utc(meta.get('updated_at')) or m,
                       main=fs[0], files=fs, source_url=None,
                       metadata={'account': 'claude-vault (person-built tool)', 'derived_from': meta.get('transcript_path'), 'parts': [os.path.relpath(x, ROOT) for x in fs], 'tags': ['derived', 'duplicate-of-claude-code-session']},
                       notes="HARD CASE: derived index of a Claude Code session built by the person's claude-vault tool; not an original chat")
        for p in loose:
            c, m = fstat_dates(p)
            yield dict(key=os.path.relpath(p, d), source_id=os.path.relpath(p, d), title=os.path.basename(p), content_type=type_of(p), created_at=c, modified_at=m,
                       main=p, files=[p], source_url=None, metadata={'account': 'claude-vault (person-built tool)', 'tags': ['derived']}, notes='claude-vault state file')


def codex(d, man):
    names = {}
    idx = f'{d}/codex-home/session_index.jsonl'
    if os.path.exists(idx):
        for o in iter_jsonl(idx): names[o['id']] = o.get('thread_name')
    for p in sorted(glob.glob(f'{d}/sessions/**/*.jsonl', recursive=True)):
        tid = os.path.basename(p)[-42:-6]
        first = last = None; n = 0; first_prompt = None; cwd = None; origin = None
        for o in iter_jsonl(p):
            t = o.get('timestamp'); first = first or t; last = t or last
            pl = o.get('payload') or {}
            if o.get('type') == 'session_meta': cwd = pl.get('cwd'); origin = pl.get('originator') or pl.get('source')
            if o.get('type') == 'response_item' and pl.get('type') == 'message' and pl.get('role') in ('user', 'assistant'):
                n += 1
                if pl.get('role') == 'user' and first_prompt is None:
                    tx = text_of(pl.get('content'))
                    if tx and not tx.lstrip().startswith('<'): first_prompt = tx
        yield dict(key=os.path.relpath(p, d), source_id=tid, title=short(names.get(tid) or first_prompt or tid), content_type='conversation',
                   created_at=utc(first), modified_at=utc(last), main=p, files=[p], source_url=None,
                   metadata={'message_count': n, 'account': '~/.codex (local)', 'cwd': cwd, 'originator': origin}, notes='')
    for p in files_under(f'{d}/codex-home'):
        if p.endswith('session_index.jsonl'): pass
        c, m = fstat_dates(p)
        rel = os.path.relpath(p, d)
        yield dict(key=rel, source_id=rel, title=os.path.basename(p), content_type='prompt_history' if p.endswith('history.jsonl') else ('database' if '.sqlite' in p else type_of(p)),
                   created_at=c, modified_at=m, main=p, files=[p], source_url=None, metadata={'account': '~/.codex'}, notes=man.get(rel, {}).get('notes', ''))


def claude_web(d, man):
    idx = {}
    f = f'{d}/_collection/chat_conversations.json'
    if os.path.exists(f):
        idx = {c['uuid']: c for c in json.load(open(f))}
    for p in sorted(glob.glob(f'{d}/conversations/*.json')):
        j = json.load(open(p)); uid = j.get('uuid') or os.path.basename(p)[:-5]
        c = idx.get(uid, {})
        proj = j.get('project') or c.get('project') or {}
        r = man.get(os.path.relpath(p, d), {})
        yield dict(key=os.path.relpath(p, d), source_id=uid, title=j.get('name') or c.get('name') or '(untitled)', content_type='conversation',
                   created_at=utc(j.get('created_at')), modified_at=utc(j.get('updated_at')), main=p, files=[p], source_url=f'https://claude.ai/chat/{uid}',
                   metadata={'message_count': len(j.get('chat_messages') or []), 'account': "claude.ai — dbarron410@vt.edu's Organization", 'model': j.get('model'),
                             'project': proj.get('name') if isinstance(proj, dict) else None, 'parent_id': ('claude-project:' + proj['uuid']) if isinstance(proj, dict) and proj.get('uuid') else None,
                             'is_starred': j.get('is_starred'), 'collection': 'stopgap (signed-in web API)'}, notes=r.get('notes', ''))
    for pd in sorted(glob.glob(f'{d}/projects/*')):
        fs = files_under(pd)
        if not fs: continue
        pj = {}
        try: pj = json.load(open(f'{pd}/project.json'))
        except Exception: pass
        main = f'{pd}/project.json' if os.path.exists(f'{pd}/project.json') else fs[0]
        yield dict(key=os.path.relpath(pd, d), source_id=os.path.basename(pd), title=pj.get('name') or os.path.basename(pd), content_type='project',
                   created_at=utc(pj.get('created_at')), modified_at=utc(pj.get('updated_at')), main=main, files=fs, source_url=f'https://claude.ai/project/{os.path.basename(pd)}',
                   metadata={'account': "claude.ai — dbarron410@vt.edu's Organization", 'is_starter_project': pj.get('is_starter_project'), 'parts': [os.path.relpath(x, ROOT) for x in fs]},
                   notes='project: instructions, knowledge docs, file list, conversation list')


def chatgpt(d, man):
    for p in sorted(glob.glob(f'{d}/**/conversations/*.json', recursive=True)):
        j = json.load(open(p))
        msgs = [n for n in (j.get('mapping') or {}).values() if (n.get('message') or {}).get('author', {}).get('role') in ('user', 'assistant')
                and ((n['message'].get('content') or {}).get('parts') or (n['message'].get('content') or {}).get('text'))]
        cid = j.get('conversation_id') or j.get('id') or os.path.basename(p)[:-5]
        r = man.get(os.path.relpath(p, d), {})
        yield dict(key=os.path.relpath(p, d), source_id=cid, title=j.get('title') or '(untitled)', content_type='conversation',
                   created_at=utc(j.get('create_time')), modified_at=utc(j.get('update_time')), main=p, files=[p], source_url=f'https://chatgpt.com/c/{cid}',
                   metadata={'message_count': len(msgs), 'account': man.get(os.path.relpath(p, d), {}).get('account_or_library') or 'chatgpt.com',
                             'model': j.get('default_model_slug'), 'parent_id': ('chatgpt-project:' + j['gizmo_id']) if j.get('gizmo_id') else None,
                             'is_archived': j.get('is_archived'), 'collection': 'stopgap (signed-in web API)'}, notes=r.get('notes', ''))


def gmail(d, man):
    """One item per thread (threads/<thread-id>/), its messages (.eml, one per message) as parts."""
    from email.parser import BytesHeaderParser
    from email.header import decode_header, make_header
    from email.utils import parsedate_to_datetime
    hp = BytesHeaderParser()
    for td in sorted(glob.glob(f'{d}/*/threads/*')):
        fs = sorted(glob.glob(f'{td}/*.eml'))
        if not fs: continue
        msgs = []
        for p in fs:
            with open(p, 'rb') as fh: h = hp.parse(fh)
            try: dt = parsedate_to_datetime(h['Date']) if h['Date'] else None
            except Exception: dt = None
            if dt is not None and dt.tzinfo is None: dt = dt.replace(tzinfo=datetime.timezone.utc)
            try: subj = str(make_header(decode_header(h['Subject'] or '')))
            except Exception: subj = h['Subject'] or ''
            msgs.append((dt or datetime.datetime.fromtimestamp(os.stat(p).st_mtime, datetime.timezone.utc), p, subj))
        msgs.sort(key=lambda x: x[0])
        acct = os.path.basename(os.path.dirname(os.path.dirname(td)))
        tid = os.path.basename(td)
        notes = '; '.join(sorted({man.get(os.path.relpath(p, d), {}).get('notes', '').split('; ')[0] for _, p, _ in msgs} - {''}))[:500]
        yield dict(key=os.path.relpath(td, d), source_id=tid, title=short(next((s for _, _, s in msgs if s), '(no subject)')), content_type='email_thread',
                   created_at=utc(msgs[0][0].isoformat()), modified_at=utc(msgs[-1][0].isoformat()), main=msgs[0][1], files=[p for _, p, _ in msgs],
                   source_url=None, metadata={'message_count': len(msgs), 'account': acct, 'format_detail': 'one raw .eml per message',
                                              'parts': [os.path.relpath(p, ROOT) for _, p, _ in msgs]}, notes=notes)


def zoom(d, man):
    for md in sorted(glob.glob(f'{d}/*/*')):
        if not os.path.isdir(md): continue
        fs = files_under(md)
        c, m = fstat_dates(fs[0])
        yield dict(key=os.path.relpath(md, d), source_id=os.path.basename(md), title=os.path.basename(md), content_type='meeting_recording',
                   created_at=min(fstat_dates(x)[0] for x in fs), modified_at=max(fstat_dates(x)[1] for x in fs), main=fs[0], files=fs, source_url=None,
                   metadata={'account': man.get(os.path.relpath(fs[0], d), {}).get('account_or_library'), 'parts': [os.path.relpath(x, ROOT) for x in fs]},
                   notes=man.get(os.path.relpath(fs[0], d), {}).get('notes', ''))


def github(d, man):
    for rel, r in sorted(man.items()):
        p = os.path.join(d, rel)
        if not os.path.isdir(p): continue
        head = subprocess.run(['git', '-C', p, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        fs = [x for x in files_under(p) if '/.git/' not in x]
        first = subprocess.run(['git', '-C', p, 'log', '--reverse', '--format=%cI'], capture_output=True, text=True).stdout.split('\n')[0]
        yield dict(key=rel, source_id=r.get('account_or_library') if r.get('account_or_library', '').startswith('http') else r.get('source'), title=os.path.basename(rel),
                   content_type='repository', created_at=utc(first) or fstat_dates(p)[0], modified_at=utc(r.get('date')), main=p, files=fs, source_url=r.get('account_or_library') if r.get('account_or_library', '').startswith('http') else None,
                   metadata={'account': r.get('account_or_library'), 'original_path': r.get('source'), 'head': head, 'file_count': len(fs)}, notes=r.get('notes', ''))
    # anything else (e.g. github.com exports) as files
    for it in generic_files(d, man, 'GitHub'):
        if not it['key'].startswith('local-repos/'): yield it


def apple_notes(d, man):
    for p in sorted(glob.glob(f'{d}/**/*.html', recursive=True)):
        with open(p, errors='replace') as f: first = f.readline()
        meta = {}
        mm = re.match(r'<!-- apple-notes-export (.*) -->', first)
        if mm: meta = json.loads(mm.group(1))
        yield dict(key=os.path.relpath(p, d), source_id=meta.get('id'), title=meta.get('title') or os.path.basename(p)[:-5], content_type='note',
                   created_at=utc(meta.get('created')), modified_at=utc(meta.get('modified')), main=p, files=[p], source_url=None,
                   metadata={'account': f"Apple Notes — {meta.get('account')} / {meta.get('folder')}", 'format_detail': 'note body HTML via AppleScript'}, notes='')


def obsidian(d, man):
    for it in generic_files(d, man, 'Obsidian'):
        if '/.obsidian/' in '/' + it['key']:
            it['content_type'] = 'config'; it['metadata']['tags'] = ['vault-config']
        yield it


ITEMIZERS = {'claude-code': claude_code, 'codex': codex, 'claude': claude_web, 'chatgpt': chatgpt, 'zoom': zoom, 'github': github,
             'apple-notes': apple_notes, 'obsidian': obsidian, 'gmail': gmail}
LABELS = os.path.join(ROOT, 'synthetic', 'ground_truth_labels.json')  # written by the synthetic generator; hidden from the agent

# ---------- build ----------

def load_ids():
    return json.load(open(IDS)) if os.path.exists(IDS) else {'next': 1, 'items': {}}


def build(side, source, ids, labels):
    d = os.path.join(ROOT, side, source)
    man = read_manifest(d)
    fn = ITEMIZERS.get(source)
    its = list(fn(d, man)) if fn else list(generic_files(d, man, source))
    prev = {}
    pf = os.path.join(d, 'source_items.json')
    if os.path.exists(pf):
        j = json.load(open(pf))
        prev = {r['id']: r for r in (j['source_items'] if isinstance(j, dict) else j)}
    out = []
    for it in its:
        k = f'{side}|{source}|{it["key"]}'
        if k not in ids['items']:
            ids['items'][k] = {'id': f'item_{ids["next"]:06d}', 'ingested_at': NOW}; ids['next'] += 1
        reg = ids['items'][k]
        meta = {'format': ext_of(it['main']) or ('directory' if os.path.isdir(it['main']) else None), 'language': language_of(it['main']) if os.path.isfile(it['main']) else None,
                'message_count': None, 'tags': []}
        meta.update({k2: v for k2, v in it['metadata'].items() if v not in (None, '', [])} if it['metadata'] else {})
        if 'message_count' in it['metadata']: meta['message_count'] = it['metadata']['message_count']
        if it.get('notes'): meta['collection_notes'] = it['notes']
        gt = {'status': 'unlabeled', 'project_ids': [], 'notes': None}
        if side == 'synthetic':
            lab = labels.get(source, {}).get(it['key'])
            if lab: gt = {'status': 'generated', 'project_ids': lab.get('project_ids', []), 'notes': lab.get('notes')}
        old = prev.get(reg['id'], {})
        if (old.get('ground_truth') or {}).get('status') == 'reviewed': gt = old['ground_truth']  # never overwrite David's review
        row_extra = {}
        if side == 'synthetic':
            row_extra['modeled_on'] = (man.get(it['key']) or man.get(os.path.relpath(it['main'], d)) or {}).get('modeled_on') or None
        out.append({
            'id': reg['id'], 'dataset_id': DATASET, 'provenance': side, 'source': source, 'source_id': it['source_id'], 'title': it['title'],
            'content_type': it['content_type'], 'created_at': it['created_at'], 'modified_at': it['modified_at'], 'ingested_at': reg['ingested_at'],
            'path': os.path.relpath(it['main'], ROOT), 'source_url': it['source_url'],
            'content_hash': content_hash([x for x in it['files'] if os.path.isfile(x)], it['main'] if os.path.isdir(it['main']) else os.path.dirname(it['main'])),
            'library_item_id': old.get('library_item_id'),
            **row_extra,
            'metadata': meta,
            'ground_truth': gt,
        })
    out.sort(key=lambda x: x['id'])
    with open(os.path.join(d, 'source_items.json'), 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    return out


def main():
    targets = sys.argv[1:] or [f'{s}/{x}' for s in ('authentic', 'synthetic') for x in sorted(os.listdir(os.path.join(ROOT, s))) if os.path.isdir(os.path.join(ROOT, s, x))]
    ids = load_ids()
    labels = json.load(open(LABELS)) if os.path.exists(LABELS) else {}
    for t in targets:
        side, source = t.split('/')
        out = build(side, source, ids, labels)
        json.dump(ids, open(IDS, 'w'))
        print(f'{t}: {len(out)} items', flush=True)
    # aggregate
    allitems = []
    for f in sorted(glob.glob(os.path.join(ROOT, '*', '*', 'source_items.json'))):
        j = json.load(open(f))
        allitems += j['source_items'] if isinstance(j, dict) else j
    allitems.sort(key=lambda x: x['id'])
    with open(os.path.join(ROOT, 'source_items.json'), 'w') as f:
        json.dump(allitems, f, ensure_ascii=False)
    print('aggregate', len(allitems))


if __name__ == '__main__':
    main()
