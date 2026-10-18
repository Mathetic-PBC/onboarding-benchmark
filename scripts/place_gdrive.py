"""Place Google Drive files collected 2026-10-17 into authentic/google-docs/<account>/{my-drive,shared-with-me}/.

Sources (all under _incoming/):
  dbarron410@vt.edu         metadata: gdrive_vt/selection.json (Drive connector listing, {id: {file, why}})
                            natives:  gdrive/dbarron410@vt.edu/<id>.<docx|xlsx|pptx|png> (docs.google.com export)
                            binaries: gdrive_vt/bin/<id>.bin (connector) or gdrive_bin/dbarron410@vt.edu/<id>.bin (/uc retry)
                            forms:    gdrive_forms/dbarron410@vt.edu/<id>.viewform.html
  davidbarron410@gmail.com  metadata: gdrive_gmail/meta.json ({id: {title, mime, modified, owner, why}}, Drive web DOM)
                            natives:  gdrive/davidbarron410@gmail.com/<id>.<ext>; binaries: gdrive_bin/davidbarron410@gmail.com/<id>.bin
File names are the Drive title plus the export extension; a title used twice in one folder gets ' (<id[:8]>)' appended.
mtime = Drive modifiedTime. Items with no content (folders, sites, scripts, shortcuts, failed downloads) are listed in
<account>/_collection/not_collected.json (with the reason; per-file download errors come from _incoming/gdrive_bin/*fail*.json)
and logged in FAILURES.md. Each run rebuilds the account's manifest rows and removes copies it no longer produces.
"""
import datetime, glob, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, set_mtime

INC = os.path.join(ROOT, '_incoming')
OUT = os.path.join(ROOT, 'authentic/google-docs')
NATIVE = {'document': 'docx', 'spreadsheet': 'xlsx', 'presentation': 'pptx', 'drawing': 'png'}
MIME_EXT = {'application/pdf': 'pdf'}


def ts_of(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp() if s else None


def safe(t):
    t = re.sub(r'[/\\:\x00-\x1f]', '_', t or 'Untitled').strip().strip('.') or 'Untitled'
    return t[:150]


def place(acct, items):
    """items: {id: dict(title, mime, modified, created, owner, why, url, size)}"""
    m = Manifest('authentic', 'google-docs')
    m.rows = {k: v for k, v in m.rows.items() if not k.startswith(acct + '/')}  # rebuilt from scratch for this account
    base = os.path.join(OUT, acct)
    fails = {}
    for ff in glob.glob(os.path.join(INC, 'gdrive_bin', '*fail*.json')):
        fails.update(json.load(open(ff)))
    placed = set()
    os.makedirs(os.path.join(base, '_collection'), exist_ok=True)
    used, missing, n = {}, [], 0
    for fid in sorted(items):
        it = items[fid]
        kind = it['mime'].replace('application/vnd.google-apps.', '') if 'google-apps' in it['mime'] else None
        src = None
        if kind in NATIVE:
            src = os.path.join(INC, 'gdrive', acct, f'{fid}.{NATIVE[kind]}'); ext = NATIVE[kind]
        elif kind == 'form':
            src = os.path.join(INC, 'gdrive_forms', acct, f'{fid}.viewform.html'); ext = 'form.html'
        elif kind is None:
            for c in (os.path.join(INC, 'gdrive_vt/bin', f'{fid}.bin'), os.path.join(INC, 'gdrive_bin', acct, f'{fid}.bin')):
                if os.path.exists(c): src = c
            t = it['title']
            ext = t.rsplit('.', 1)[1] if '.' in t[-6:] else MIME_EXT.get(it['mime'], '')
        if not src or not os.path.exists(src) or os.path.getsize(src) == 0:
            if kind in ('folder', 'site', 'script', 'shortcut'): reason = f'no content (Drive {kind})'
            elif it['mime'].startswith('unknown'): reason = 'no file extension and no download: probably a folder (Drive web list does not show the type)'
            else: reason = 'download failed: ' + fails.get(fid, 'no file received')
            missing.append({'id': fid, 'title': it['title'], 'mime': it['mime'], 'kind': kind or 'binary', 'reason': reason, 'meta': it})
            continue
        sub = 'my-drive' if it.get('owner') in (acct, None, '') else 'shared-with-me'
        title = safe(it['title'])
        if kind is None and ext and title.lower().endswith('.' + ext.lower()):
            title = title[: -len(ext) - 1]
        name = f'{title}.{ext}' if ext else title
        key = (sub, name.lower())
        if key in used:
            name = f'{title} ({fid[:8]}).{ext}' if ext else f'{title} ({fid[:8]})'
        used[key] = fid
        dst = os.path.join(base, sub, name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        placed.add(dst)
        t = ts_of(it.get('modified'))
        if t: set_mtime(dst, t)
        n += 1
        notes = [f'drive id {fid}', f'mime {it["mime"]}', f'owner {it.get("owner") or "?"}', f'selected: {it.get("why")}']
        if it.get('created'): notes.append(f'created {it["created"]}')
        if kind in NATIVE: notes.append(f'exported from Google {kind} as .{NATIVE[kind]} (docs.google.com export)')
        if kind == 'form': notes.append('Google Form: public viewform page HTML (questions; FB_PUBLIC_LOAD_DATA_), responses not included')
        if it.get('note'): notes.append(it['note'])
        m.add(os.path.relpath(dst, os.path.join(ROOT, 'authentic/google-docs')), 'google-docs', acct, it.get('modified') or '',
              source=it.get('url') or f'https://drive.google.com/file/d/{fid}', notes='; '.join(notes))
    stale = [os.path.join(dp, f) for sub in ('my-drive', 'shared-with-me') for dp, _, fs in os.walk(os.path.join(base, sub)) for f in fs
             if os.path.join(dp, f) not in placed]
    for f in stale: os.remove(f)  # our own copies from an earlier run whose name changed
    if stale: print('removed', len(stale), 'stale copies')
    json.dump(missing, open(os.path.join(base, '_collection/not_collected.json'), 'w'), indent=1, ensure_ascii=False)
    m.add(f'{acct}/_collection/drive_selection.json', 'google-docs', acct, '', notes='Drive metadata for every selected file + selection reason')
    m.add(f'{acct}/_collection/not_collected.json', 'google-docs', acct, '', notes=f'{len(missing)} selected Drive items with no collectable content')
    print(acct, 'placed', n, 'missing', len(missing), 'rows', m.save())
    return missing


def vt():
    sel = json.load(open(os.path.join(INC, 'gdrive_vt/selection.json')))
    items = {}
    for fid, v in sel.items():
        f = v['file']
        items[fid] = dict(title=f.get('title'), mime=f.get('mimeType'), modified=f.get('modifiedTime'), created=f.get('createdTime'),
                          owner=f.get('owner'), why=v['why'], url=f.get('viewUrl'), size=f.get('fileSize'))
    base = os.path.join(OUT, 'dbarron410@vt.edu/_collection')
    os.makedirs(base, exist_ok=True)
    shutil.copyfile(os.path.join(INC, 'gdrive_vt/selection.json'), os.path.join(base, 'drive_selection.json'))
    return place('dbarron410@vt.edu', items)


def gmail():
    f = os.path.join(INC, 'gdrive_gmail/meta.json')
    if not os.path.exists(f):
        print('gmail account: no meta.json yet'); return []
    items = json.load(open(f))
    base = os.path.join(OUT, 'davidbarron410@gmail.com/_collection')
    os.makedirs(base, exist_ok=True)
    shutil.copyfile(f, os.path.join(base, 'drive_selection.json'))
    return place('davidbarron410@gmail.com', items)


if __name__ == '__main__':
    which = sys.argv[1:] or ['vt', 'gmail']
    for w in which:
        globals()[w]()
