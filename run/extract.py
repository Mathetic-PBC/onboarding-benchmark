"""Turn a sandbox item into numbered units, then into a wave 2 snippet or a deep-pass read.

Everything here reads only runs/<run>/sandbox/.
"""
import email, email.policy, html, html.parser, io, json, os, re, sqlite3, subprocess, zipfile
from email.utils import getaddresses

from config import RUN
FILES = os.path.join(RUN, 'sandbox', 'files')

DEEP_BUDGET = 60_000      # characters of unit text per item in the deep pass
DEEP_UNIT_CAP = 4_000     # characters per unit in the deep pass


# ---------- text helpers ----------

class _Strip(html.parser.HTMLParser):
    BLOCK = {'p', 'div', 'br', 'li', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'blockquote', 'section', 'article', 'dt', 'dd'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'head', 'title'):
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'head', 'title'):
            self.skip = max(0, self.skip - 1)
        elif tag in self.BLOCK:
            self.out.append('\n')

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


def next_text(page):
    """Text nodes from a Next.js page's flight payload (Granola shared notes)."""
    out = []
    for c in re.findall(r'self\.__next_f\.push\(\[1,(".*?")\]\)</script>', page, re.S):
        try:
            s = json.loads(c)
        except Exception:
            continue
        for m in re.findall(r'"text":"((?:[^"\\]|\\.)*)"', s):
            try:
                m = json.loads('"' + m + '"')
            except Exception:
                pass
            if m.strip():
                out.append(m.strip())
    return out


def html_text(s):
    p = _Strip()
    try:
        p.feed(s)
    except Exception:
        return re.sub(r'<[^>]+>', ' ', s)
    return ''.join(p.out)


def lines_of(text):
    out = []
    for ln in text.replace('\r', '').split('\n'):
        ln = re.sub(r'[ \t ]+', ' ', ln).strip()
        if ln:
            out.append(ln)
    return out


def read_text(path, limit=5_000_000):
    with open(path, 'rb') as fh:
        b = fh.read(limit)
    return b.decode('utf-8', 'replace')


def clip(s, n):
    s = s.strip()
    return s if len(s) <= n else s[:n].rstrip() + ' …'


def flatten_json(o, prefix='', out=None, limit=4000):
    if out is None:
        out = []
    if len(out) >= limit:
        return out
    if isinstance(o, dict):
        for k, v in o.items():
            flatten_json(v, f'{prefix}{k}.' if prefix or True else '', out, limit)
    elif isinstance(o, list):
        for v in o:
            flatten_json(v, prefix, out, limit)
    elif isinstance(o, str):
        s = o.strip()
        if s and not re.fullmatch(r'[0-9a-f\-]{16,}|[rc]{1,2}_[0-9a-f]+|https?://\S+\.(png|jpg|svg)', s):
            out.append(f'{prefix.rstrip(".")}: {s}' if prefix else s)
    elif o is not None and not isinstance(o, bool):
        pass
    return out


def git(gitdir, *args):
    try:
        r = subprocess.run(['git', f'--git-dir={gitdir}', '--no-pager', *args], capture_output=True, text=True, timeout=30)
        return r.stdout if r.returncode == 0 else ''
    except Exception:
        return ''


# ---------- per-format readers: each returns (kind, header, units) ----------
# A unit is {'unit': label, 'index': n, 'text': str, 'role': 'person'|'other'|None, 'file': name|None}

def U(label, i, text, role=None, file=None):
    return {'unit': label, 'index': i, 'text': text, 'role': role, 'file': file}


def chat_units(msgs):
    """msgs: [(role, text)] with role 'person' or 'other'."""
    return [U('message', i, t, r) for i, (r, t) in enumerate(m for m in msgs if m[1].strip())]


def read_chatgpt(o):
    m = o.get('mapping') or {}
    node, chain = o.get('current_node'), []
    while node and node in m:
        chain.append(m[node]); node = m[node].get('parent')
    if not chain:
        chain = list(m.values())
    else:
        chain.reverse()
    msgs = []
    for n in chain:
        msg = n.get('message') or {}
        role = (msg.get('author') or {}).get('role')
        if role not in ('user', 'assistant') or (msg.get('metadata') or {}).get('is_visually_hidden_from_conversation'):
            continue
        parts = (msg.get('content') or {}).get('parts') or []
        txt = '\n'.join(p if isinstance(p, str) else '[attachment]' for p in parts if isinstance(p, str) or isinstance(p, dict))
        txt = txt.replace('[attachment]', '').strip() or ('[attachment]' if parts else '')
        if txt:
            msgs.append(('person' if role == 'user' else 'other', txt))
    return chat_units(msgs)


def read_claude_chat(o):
    msgs = []
    for cm in o.get('chat_messages') or []:
        txt = '\n'.join(c.get('text', '') for c in (cm.get('content') or []) if c.get('type') == 'text') or cm.get('text', '')
        for a in cm.get('attachments') or []:
            if a.get('file_name'):
                txt += f"\n[attached: {a['file_name']}]"
        msgs.append(('person' if cm.get('sender') == 'human' else 'other', txt))
    return chat_units(msgs)


def read_gemini(o):
    msgs = []
    try:
        turns = o['read'][0][0]
        for t in reversed(turns):  # newest first in the export
            q = t[2][0][0] if t[2] and t[2][0] else ''
            a = ''
            try:
                a = t[3][0][0][1][0]
            except Exception:
                pass
            if isinstance(q, str):
                msgs.append(('person', q))
            if isinstance(a, str):
                msgs.append(('other', a))
    except Exception:
        msgs = [('other', s) for s in flatten_json(o.get('read'))[:200]]
    return chat_units(msgs)


def read_grok(o):
    return chat_units([('person' if r.get('sender') in ('human', 'user') else 'other', r.get('message') or '')
                       for r in o.get('responses') or []])


def read_perplexity(o):
    msgs = []
    for e in o.get('entries') or []:
        msgs.append(('person', e.get('query_str') or ''))
        msgs.append(('other', e.get('answer') or ''))
    return chat_units(msgs)


def read_cursor(path, sid):
    db = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    row = db.execute('select value from cursorDiskKV where key=?', (f'composerData:{sid}',)).fetchone()
    order = []
    if row:
        try:
            cd = json.loads(row[0])
            order = [h.get('bubbleId') for h in cd.get('fullConversationHeadersOnly') or []]
        except Exception:
            pass
    bubbles = {}
    for k, v in db.execute('select key, value from cursorDiskKV where key like ?', (f'bubbleId:{sid}:%',)):
        try:
            b = json.loads(v)
        except Exception:
            continue
        bubbles[k.split(':')[-1]] = b
    if not order:
        order = sorted(bubbles, key=lambda b: bubbles[b].get('createdAt') or '')
    msgs = [('person' if bubbles[b].get('type') == 1 else 'other', bubbles[b].get('text') or '') for b in order if b in bubbles]
    return chat_units(msgs)


def cc_text(content):
    if isinstance(content, str):
        return content
    out = []
    for c in content or []:
        if isinstance(c, dict) and c.get('type') == 'text':
            out.append(c.get('text', ''))
    return '\n'.join(out)


def read_claude_code(paths):
    """Main session file first; subagent files follow as their own units with the file named."""
    units, i = [], 0
    for fi, p in enumerate(paths):
        fname = os.path.relpath(p, FILES) if fi else None
        for ln in open(p, errors='replace'):
            try:
                l = json.loads(ln)
            except Exception:
                continue
            t, msg = l.get('type'), l.get('message') or {}
            if t == 'user' and not l.get('isMeta'):
                c = msg.get('content')
                if isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
                    continue
                txt = cc_text(c)
                if txt.strip() and not txt.startswith(('<local-command-stdout>', '<command-message>', 'Caveat:')):
                    units.append(U('message', i, txt, 'person' if not fi else 'other', fname)); i += 1
            elif t == 'assistant':
                txt = cc_text(msg.get('content'))
                if txt.strip():
                    units.append(U('message', i, txt, 'other', fname)); i += 1
            elif t == 'summary' and l.get('summary'):
                units.append(U('message', i, '[summary] ' + l['summary'], 'other', fname)); i += 1
    return units


CODEX_INJECTED = ('# AGENTS.md instructions', '<environment_context>', '<user_instructions>', '<INSTRUCTIONS>',
                  '<permissions', '<turn_aborted>', '<user_shell_command>')


def read_codex(path):
    units, i, meta, fallback = [], 0, {}, []
    for ln in open(path, errors='replace'):
        try:
            l = json.loads(ln)
        except Exception:
            continue
        p = l.get('payload') if isinstance(l.get('payload'), dict) else {}
        if l.get('type') == 'session_meta':
            meta = {'cwd': p.get('cwd')}
        elif l.get('type') == 'event_msg' and p.get('type') == 'user_message':
            units.append(U('message', i, p.get('message') or '', 'person')); i += 1
        elif l.get('type') == 'event_msg' and p.get('type') == 'agent_message':
            units.append(U('message', i, p.get('message') or '', 'other')); i += 1
        elif l.get('type') == 'response_item' and p.get('type') == 'message' and p.get('role') in ('user', 'assistant'):
            txt = '\n'.join(c.get('text', '') for c in p.get('content') or [] if isinstance(c, dict))
            if p['role'] == 'user' and txt.lstrip().startswith(CODEX_INJECTED):
                continue
            fallback.append(U('message', 0, txt, 'person' if p['role'] == 'user' else 'other'))
    if not any(u['role'] == 'person' for u in units):
        units = [{**u, 'index': j} for j, u in enumerate(x for x in fallback if x['text'].strip())]
    return [u for u in units if u['text'].strip()], meta


def eml_body(msg):
    body = None
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain' and not part.get_filename():
                body = part.get_content(); break
        if body is None:
            for part in msg.walk():
                if part.get_content_type() == 'text/html' and not part.get_filename():
                    body = html_text(part.get_content()); break
    else:
        try:
            body = msg.get_content()
        except Exception:
            body = msg.get_payload()
        if msg.get_content_type() == 'text/html':
            body = html_text(body)
    return body or ''


def strip_quoted(text):
    out = []
    for ln in text.replace('\r', '').split('\n'):
        if ln.lstrip().startswith('>'):
            continue
        if re.match(r'^On .{6,120}wrote:\s*$', ln.strip()) or ln.strip().startswith('-----Original Message'):
            break
        out.append(ln)
    return '\n'.join(out)


def read_eml_thread(paths):
    msgs, header = [], {}
    for p in sorted(paths):
        try:
            with open(p, 'rb') as fh:
                m = email.message_from_binary_file(fh, policy=email.policy.default)
        except Exception:
            continue
        try:
            body = eml_body(m)
        except Exception:
            body = ''
        frm = str(m.get('From', '')); to = str(m.get('To', '')); cc = str(m.get('Cc', ''))
        date = str(m.get('Date', ''))
        if not header:
            header = {'subject': str(m.get('Subject', '')), 'label': str(m.get('X-Gmail-Labels', '') or '') or None}
        people = [a for _, a in getaddresses([frm, to, cc]) if a]
        header.setdefault('people', [])
        for a in people:
            if a not in header['people']:
                header['people'].append(a)
        header.setdefault('dates', []).append(date)
        msgs.append((frm, date, body))
    units = [U('message', i, f'From: {f}\nDate: {d}\n\n{strip_quoted(b).strip()}', None) for i, (f, d, b) in enumerate(msgs)]
    return units, header


def docx_text(path):
    try:
        r = subprocess.run(['textutil', '-convert', 'txt', '-stdout', path], capture_output=True, timeout=60)
        return r.stdout.decode('utf-8', 'replace')
    except Exception:
        return ''


def pptx_slides(path):
    out = []
    with zipfile.ZipFile(path) as z:
        names = sorted((n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)),
                       key=lambda n: int(re.findall(r'\d+', n)[-1]))
        for n in names:
            xml = z.read(n).decode('utf-8', 'replace')
            out.append(' '.join(html.unescape(t) for t in re.findall(r'<a:t>([^<]*)</a:t>', xml)))
    return out


def xlsx_lines(path):
    out = []
    with zipfile.ZipFile(path) as z:
        if 'xl/workbook.xml' in z.namelist():
            wb = z.read('xl/workbook.xml').decode('utf-8', 'replace')
            out.append('Sheets: ' + ', '.join(html.unescape(s) for s in re.findall(r'<sheet [^>]*name="([^"]*)"', wb)))
        if 'xl/sharedStrings.xml' in z.namelist():
            ss = z.read('xl/sharedStrings.xml').decode('utf-8', 'replace')
            strs = [html.unescape(re.sub(r'<[^>]+>', '', s)) for s in re.findall(r'<si>(.*?)</si>', ss, re.S)]
            out += [s for s in strs if s.strip()]
    return out


def pdf_pages(path, max_pages=None):
    try:
        import pypdf
        r = pypdf.PdfReader(path)
        n = len(r.pages)
        pages = []
        for i, pg in enumerate(r.pages):
            if max_pages is not None and i >= max_pages:
                break
            try:
                pages.append(pg.extract_text() or '')
            except Exception:
                pages.append('')
        return pages, n
    except Exception as e:
        return [], 0


def zip_units(path, deep):
    units = []
    try:
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if not n.endswith('/')]
            units.append(U('line', 0, 'Archive contents: ' + ', '.join(names[:80]) + (' …' if len(names) > 80 else '')))
            tex = [n for n in names if n.endswith('.tex')]
            main = None
            for n in tex:
                if b'\\documentclass' in z.read(n)[:20000]:
                    main = n; break
            for n in ([main] if main else []) + ([] if not deep else [t for t in tex if t != main][:6]):
                for ln in lines_of(z.read(n).decode('utf-8', 'replace')):
                    units.append(U('line', len(units), ln, None, n))
            if not tex:
                for n in names:
                    if n.lower().endswith(('readme.md', 'readme.txt', 'readme')):
                        for ln in lines_of(z.read(n).decode('utf-8', 'replace')):
                            units.append(U('line', len(units), ln, None, n))
                        break
    except Exception as e:
        units.append(U('line', len(units), f'[archive could not be read: {type(e).__name__}]'))
    return units


def sqlite_units(path):
    units = []
    try:
        db = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
        tables = [t for (t,) in db.execute("select name from sqlite_master where type='table'")]
        if 'urls' in tables:      # Chrome History
            for title, url, n in db.execute('select title, url, visit_count from urls order by visit_count desc limit 300'):
                units.append(U('line', len(units), f'{title or ""} — {url} ({n} visits)'))
        elif 'moz_places' in tables:
            for title, url, n in db.execute('select title, url, visit_count from moz_places order by visit_count desc limit 300'):
                units.append(U('line', len(units), f'{title or ""} — {url} ({n} visits)'))
        else:
            units.append(U('line', 0, 'Tables: ' + ', '.join(tables)))
            for t in tables[:12]:
                try:
                    rows = db.execute(f'select * from "{t}" limit 20').fetchall()
                except Exception:
                    continue
                for r in rows:
                    s = ' | '.join(str(x)[:300] for x in r if isinstance(x, (str, int, float)))
                    if s.strip():
                        units.append(U('line', len(units), f'{t}: {s}'))
    except Exception as e:
        units.append(U('line', 0, f'[database could not be read: {type(e).__name__}]'))
    return units


def lines_units(text, label='line', file=None):
    return [U(label, i, ln, None, file) for i, ln in enumerate(lines_of(text))]


def para_units(text):
    paras = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n|\n', text)]
    return [U('paragraph', i, p) for i, p in enumerate(x for x in paras if x)]


def vtt_text(path):
    out = []
    for ln in read_text(path).split('\n'):
        ln = ln.strip()
        if not ln or ln == 'WEBVTT' or '-->' in ln or ln.isdigit():
            continue
        out.append(ln)
    return '\n'.join(out)


MEDIA = ('.png', '.jpg', '.jpeg', '.gif', '.heic', '.webp', '.svg', '.m4a', '.mp3', '.wav', '.mp4', '.mov', '.webm', '.pkpass', '.ico')


def read_repo(item):
    root = os.path.join(FILES, item['path'])
    gitdir = root if os.path.isfile(os.path.join(root, 'HEAD')) else os.path.join(root, '.git')
    name = os.path.basename(item['path'].rstrip('/'))
    desc = ''
    dfile = os.path.join(gitdir, 'description')
    if os.path.isfile(dfile):
        d = read_text(dfile).strip()
        if not d.startswith('Unnamed repository'):
            desc = d
    readme, rname = '', None
    for cand in ('README.md', 'README', 'readme.md', 'README.txt', 'README.rst'):
        if os.path.isfile(os.path.join(root, cand)):
            readme, rname = read_text(os.path.join(root, cand)), cand; break
    if not readme and os.path.isdir(gitdir):
        for cand in ('README.md', 'README', 'readme.md'):
            t = git(gitdir, 'show', f'HEAD:{cand}')
            if t:
                readme, rname = t, cand; break
    log = git(gitdir, 'log', '--all', '--date=short', '--format=%ad %s', '-n', '200') if os.path.isdir(gitdir) else ''
    tree = git(gitdir, 'ls-tree', '-r', '--name-only', 'HEAD') if os.path.isdir(gitdir) else ''
    if not tree:
        tree = '\n'.join(os.path.relpath(os.path.join(dp, f), root) for dp, dns, fns in os.walk(root)
                         if '/.git' not in dp + '/' and '/node_modules' not in dp for f in fns)
    return name, desc, readme, rname, log, tree


# ---------- the item reader ----------

def read_item(item):
    """Returns dict(kind, header, units, meta_read)."""
    src, ctype = item['source'], item['content_type']
    path = os.path.join(FILES, item['path'])
    files = [os.path.join(FILES, f) for f in item.get('files') or []]
    ext = os.path.splitext(item['path'])[1].lower()
    meta = item.get('metadata') or {}
    folder = os.path.dirname(item['path'])
    hdr = {'title': item.get('title'), 'date': item.get('modified_at') or item.get('created_at'), 'source': src,
           'folder': folder}
    meta_read = ['title', 'created_at', 'modified_at', 'source', 'path']

    def done(kind, units, **extra):
        hdr.update({k: v for k, v in extra.items() if v})
        return {'kind': kind, 'header': hdr, 'units': units, 'meta_read': meta_read}

    try:
        if src == 'cursor' and ctype == 'conversation':
            return done('chat', read_cursor(path, item['source_id']))
        if ctype == 'conversation' and src in ('chatgpt', 'claude', 'gemini', 'grok', 'perplexity') or \
                (src in ('gemini', 'grok', 'perplexity') and ext == '.json'):
            o = json.load(open(path))
            fn = {'chatgpt': read_chatgpt, 'claude': read_claude_chat, 'gemini': read_gemini,
                  'grok': read_grok, 'perplexity': read_perplexity}[src]
            extra = {}
            if src == 'perplexity' and (o.get('collection') or {}).get('title'):
                extra['project'] = o['collection']['title']
            if src == 'claude' and meta.get('project'):
                extra['project'] = meta.get('project')
            return done('chat', fn(o), **extra)
        if src == 'claude' and ctype == 'project':
            units = []
            for f in files:
                try:
                    o = json.load(open(f))
                except Exception:
                    continue
                for ln in flatten_json(o):
                    units.append(U('line', len(units), ln, None, os.path.relpath(f, FILES)))
            return done('folder', units)
        if src in ('claude-code',) and ctype == 'conversation':
            main = [path] + [f for f in files if f != path and f.endswith('.jsonl')]
            meta_read.append('cwd')
            return done('session', read_claude_code(main), folder_cwd=meta.get('cwd') or meta.get('project_dir'))
        if src == 'codex' and ctype == 'conversation':
            units, m = read_codex(path)
            meta_read.append('cwd')
            return done('session', units, folder_cwd=m.get('cwd') or meta.get('cwd'))
        if ctype == 'email_thread':
            emls = [f for f in files if f.endswith('.eml')] or [path]
            units, h = read_eml_thread(emls)
            return done('email', units, subject=h.get('subject'), people=h.get('people'), label=h.get('label'))
        if ctype == 'repository':
            name, desc, readme, rname, log, tree = read_repo(item)
            units = [U('line', i, ln, None, rname) for i, ln in enumerate(lines_of(readme))]
            extra_units = [U('line', 0, ln, None, 'git log') for ln in lines_of(log)] + \
                          [U('line', 0, ln, None, 'file tree') for ln in lines_of(tree)[:400]]
            if not units:  # no README: the commit history is the repo's opening text
                units = [U('line', i, ln, None, 'git log') for i, ln in enumerate(lines_of(log)[:60])]
                extra_units = extra_units[len(units):]
            r = done('repo', units, name=name, description=desc)
            r['deep_extra'] = extra_units
            return r
        if ext == '.pdf':
            pages, n = pdf_pages(path)
            return done('pdf', [U('page', i, t) for i, t in enumerate(pages)], page_count=n)
        if ext in ('.docx', '.doc', '.rtf', '.odt'):
            return done('document', para_units(docx_text(path)), type=ctype)
        if ext == '.pptx':
            return done('document', [U('slide', i, t) for i, t in enumerate(pptx_slides(path)) if True], type=ctype)
        if ext == '.xlsx':
            return done('document', [U('line', i, t) for i, t in enumerate(xlsx_lines(path))], type=ctype)
        if ext in ('.html', '.htm'):
            t = read_text(path)
            if src == 'granola' and 'self.__next_f.push' in t:
                return done('note', [U('line', i, x) for i, x in enumerate(next_text(t))])
            kind = 'note' if ctype == 'note' or src in ('apple-notes', 'onenote', 'zotero', 'granola') else 'document'
            return done(kind, lines_units(html_text(t)) if kind == 'note' else para_units(html_text(t)), type=ctype)
        if ext == '.enex':
            t = read_text(path)
            body = ' '.join(re.findall(r'<content>(.*?)</content>', t, re.S))
            body = html.unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', body))
            tags = re.findall(r'<tag>(.*?)</tag>', t)
            return done('note', lines_units(html_text(body)), tags=tags)
        if src == 'granola' and ext == '.json':
            o = json.load(open(path))
            people = [a.get('email') for a in ((o.get('google_calendar_event') or {}).get('attendees') or []) if a.get('email')]
            body = o.get('notes_markdown') or o.get('notes_plain') or ''
            units = lines_units(body)
            tr = o.get('transcript')
            if isinstance(tr, list):
                for seg in tr:
                    if isinstance(seg, dict) and seg.get('text'):
                        units.append(U('line', len(units), f"[{seg.get('source', 'transcript')}] {seg['text']}"))
            return done('note', units, people=people)
        if src == 'linear' and ext == '.json':
            o = json.load(open(path))
            iss = o.get('issue') or o.get('document') or o
            txt = '\n'.join(x for x in [iss.get('title') or '', iss.get('description') or iss.get('content') or ''] if x)
            units = lines_units(txt)
            for c in o.get('comments') or []:
                units.append(U('line', len(units), 'Comment: ' + (c.get('body') or '')))
            if not units:
                units = lines_units('\n'.join(flatten_json(o)))
            proj = ((iss.get('project') or {}).get('name') if isinstance(iss.get('project'), dict) else None)
            return done('note', units, project=proj)
        if ext == '.vtt' or (src == 'zoom'):
            vtts = [f for f in files if f.endswith(('.vtt', '.txt'))] or ([path] if ext == '.vtt' else [])
            units = []
            for f in vtts:
                units += [U('line', len(units) + i, ln, None, os.path.relpath(f, FILES)) for i, ln in enumerate(lines_of(vtt_text(f)))]
            if not units:
                units = [U('line', 0, 'Files: ' + ', '.join(os.path.basename(f) for f in files))]
            return done('other', units)
        if ext == '.zip':
            return done('other', zip_units(path, False), type=ctype)
        if ctype in ('database',) or ext in ('.sqlite', '.vscdb', '.db') or os.path.basename(path) == 'History':
            return done('other', sqlite_units(path), type=ctype)
        if ext in MEDIA or ctype in ('image', 'audio', 'video'):
            return done('other', [], type=ctype)
        if ext in ('.json',):
            o = json.load(open(path))
            return done('other', lines_units('\n'.join(flatten_json(o))), type=ctype)
        if ext == '.jsonl':
            out = []
            for ln in open(path, errors='replace'):
                try:
                    out += flatten_json(json.loads(ln))
                except Exception:
                    pass
                if len(out) > 4000:
                    break
            return done('other', lines_units('\n'.join(out)), type=ctype)
        if ext == '.ipynb':
            o = json.load(open(path))
            t = '\n'.join(''.join(c.get('source') or []) for c in o.get('cells') or [])
            return done('other', lines_units(t), type=ctype)
        # text-like fallback: notes, code, csv, md, txt, bib, …
        t = read_text(path)
        if '\x00' in t[:2000]:
            return done('other', [], type=ctype)
        kind = 'note' if ctype == 'note' else 'other'
        return done(kind, lines_units(t), type=ctype)
    except Exception as e:
        return done('other', [U('line', 0, f'[could not be read: {type(e).__name__}]')], type=ctype)


# ---------- wave 2 snippet ----------

def _pick(units, idxs, cap):
    return [{'unit': u['unit'], 'index': u['index'], **({'file': u['file']} if u.get('file') else {}),
             'text': clip(u['text'], cap)} for u in (units[i] for i in idxs)]


def _even(n, k):
    if n <= k:
        return list(range(n))
    return sorted({round(j * (n - 1) / (k - 1)) for j in range(k)})


def first_words(units, n_words=300, cap=600):
    out, words = [], 0
    for i, u in enumerate(units):
        if words >= n_words:
            break
        out.append(i); words += len(u['text'].split())
    return out


def snippet(item):
    """Wave 2 record for one item. Returns (record_without_id, sample_info)."""
    r = read_item(item)
    kind, h, units = r['kind'], r['header'], r['units']
    rec = {'title': h.get('title'), 'date': (h.get('date') or '')[:10] or None, 'source': h['source']}
    hint = {}
    if kind in ('chat', 'session'):
        person = [i for i, u in enumerate(units) if u['role'] == 'person']
        if kind == 'session':
            hint['folder'] = h.get('folder_cwd')
        if h.get('project'):
            hint['project'] = h['project']
        idx = []
        if person:
            idx = [person[0], person[-1]]
            digest = [i for i in person[1:-1]]
            idx += [digest[j] for j in _even(len(digest), 10)] if digest else []
        elif units:
            idx = [0]
        idx = sorted(set(idx))
        shown = []
        for i in idx:
            cap = 700 if i in (person[:1] + person[-1:]) else 200
            shown += _pick(units, [i], cap)
        unit_label = 'message'
    elif kind == 'email':
        hint.update({k: h[k] for k in ('label',) if h.get(k)})
        rec['subject'] = h.get('subject'); rec['people'] = (h.get('people') or [])[:8]
        idx = _even(len(units), 3)
        shown = []
        for i in idx:
            t = units[i]['text']
            head, _, body = t.partition('\n\n')
            shown.append({'unit': 'message', 'index': units[i]['index'], 'text': clip(head + '\n\n' + '\n'.join(lines_of(body)[:8]), 700)})
        unit_label = 'message'
    elif kind == 'repo':
        rec['title'] = h.get('name') or rec['title']
        if h.get('description'):
            rec['description'] = h['description']
        shown = _pick(units, first_words(units, 250), 300)
        unit_label = 'line'
    elif kind == 'pdf':
        hint['folder'] = h['folder']
        shown = [{'unit': 'page', 'index': 0, 'text': clip(units[0]['text'], 2000)}] if units else []
        unit_label = 'page'
    elif kind == 'document':
        hint['folder'] = h['folder']; rec['type'] = h.get('type')
        shown = _pick(units, first_words(units, 300), 600)
        unit_label = units[0]['unit'] if units else 'paragraph'
    elif kind == 'note':
        hint['folder'] = h['folder']
        if h.get('project'):
            hint['project'] = h['project']
        total = sum(len(u['text']) for u in units)
        idx = list(range(len(units))) if total <= 1500 else first_words(units, 250)
        shown = _pick(units, idx, 400)
        unit_label = 'line'
    else:  # other / folder
        hint['folder'] = h['folder']
        if h.get('type'):
            rec['type'] = h['type']
        shown = _pick(units, first_words(units, 200), 300)
        unit_label = units[0]['unit'] if units else 'line'
    rec['hint'] = {k: v for k, v in hint.items() if v}
    rec['snippet'] = {'units': shown, 'total_units': len(units)}
    idxs = [u['index'] for u in shown]
    info = {'metadata_fields_read': r['meta_read'], 'unit': unit_label, 'index_base': 0,
            'range_end': (max(idxs) if idxs else 0), 'ranges': _ranges(idxs),
            'units_read': len(shown), 'total_units': len(units),
            'coverage_fraction': round(len(shown) / len(units), 4) if units else 0.0}
    return rec, info


def _ranges(idxs):
    out = []
    for i in sorted(idxs):
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return out


# ---------- deep read ----------

def deep_read(item):
    """Full sample up to DEEP_BUDGET characters. Folder items keep the file named on every unit."""
    r = read_item(item)
    kind, h, units = r['kind'], r['header'], r['units']
    all_units = units + r.get('deep_extra', [])
    if kind in ('other',) and item.get('path', '').endswith('.zip'):
        all_units = zip_units(os.path.join(FILES, item['path']), True)
    # number deep_extra units after the main ones
    numbered, i = [], 0
    for u in all_units:
        numbered.append({**u, 'index': i if u in r.get('deep_extra', []) or kind == 'repo' else u['index']}); i += 1
    shown, used, truncated = [], 0, False
    for u in numbered:
        t = u['text']
        if len(t) > DEEP_UNIT_CAP:
            t = t[:DEEP_UNIT_CAP] + ' …[unit truncated]'; truncated = True
        if used + len(t) > DEEP_BUDGET:
            truncated = True
            break
        shown.append({'unit': u['unit'], 'index': u['index'], **({'file': u['file']} if u.get('file') else {}),
                      **({'role': u['role']} if u.get('role') else {}), 'text': t})
        used += len(t)
    meta = {k: v for k, v in h.items() if v}
    rec = {'metadata': meta, 'units': shown, 'total_units': len(numbered), 'truncated': truncated}
    idxs = [u['index'] for u in shown]
    info = {'metadata_fields_read': r['meta_read'], 'unit': shown[0]['unit'] if shown else 'line', 'index_base': 0,
            'range_end': max(idxs) if idxs else 0, 'ranges': _ranges(idxs), 'units_read': len(shown),
            'total_units': len(numbered), 'coverage_fraction': round(len(shown) / len(numbered), 4) if numbered else 0.0,
            'budget_chars': DEEP_BUDGET, 'unit_cap_chars': DEEP_UNIT_CAP, 'truncated': truncated}
    return rec, info
