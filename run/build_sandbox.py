"""Step 1: build runs/<run>/sandbox/ from benchmark-data/ without the answer key.

Prints counts only. Never prints a hidden field or a ground-truth project id.

  sandbox/files/<path without authentic/ or synthetic/>   hardlinked item files
  sandbox/items.json                                      source items, stripped
  sandbox/local_view/{claude-code,codex,github}           hardlinked, for the wave 1 local agent
  private/path_map.json, private/excluded.json            for this harness only, never sent to a model
"""
import hashlib, json, os, re, shutil, sys, zipfile

sys.path.insert(0, os.path.dirname(__file__))
from config import DATA, RUN, RUN_ID
SANDBOX = os.path.join(RUN, 'sandbox')
FILES = os.path.join(SANDBOX, 'files')
PRIVATE = os.path.join(RUN, 'private')

HIDDEN_NAMES = {'ground_truth_projects.json', 'ground_truth_labels.json', 'PERSON.md',
                'MANIFEST.csv', 'PROGRESS.md', 'FAILURES.md', 'source_items.json'}
DROP_TOP = ('ground_truth', 'modeled_on', 'provenance', 'ingested_at')
DROP_META = ('collection_notes',)


def leak_patterns():
    # The ids are read here and only used as byte patterns; they are never printed.
    ids = [r['id'] for r in json.load(open(os.path.join(DATA, 'ground_truth_projects.json')))]
    named = {'ground_truth': [b'ground_truth'], 'HARD CASE': [b'HARD CASE'], 'PERSON.md': [b'PERSON.md']}
    named['project_ids'] = [i.encode() for i in ids]
    return named


def hidden(rel):
    parts = rel.split('/')
    return parts[0] == '_scripts' or parts[-1] in HIDDEN_NAMES or '_scripts' in parts


def item_files(item):
    """Every file an item owns, as paths relative to DATA."""
    roots = [item['path']] + list((item.get('metadata') or {}).get('parts') or [])
    out = []
    for r in roots:
        r = r.rstrip('/')
        full = os.path.join(DATA, r)
        if os.path.isdir(full):
            for dp, dns, fns in os.walk(full):
                for fn in fns:
                    out.append(os.path.relpath(os.path.join(dp, fn), DATA))
        elif os.path.exists(full):
            out.append(r)
    seen, uniq = set(), []
    for f in out:
        if f not in seen and not hidden(f):
            seen.add(f); uniq.append(f)
    return uniq


def scan_bytes(data, pats):
    return {k for k, ps in pats.items() if any(p in data for p in ps)}


def scan_file(full, pats):
    hits = set()
    try:
        with open(full, 'rb') as fh:
            data = fh.read()
    except OSError:
        return hits
    hits |= scan_bytes(data, pats)
    if data[:4] == b'PK\x03\x04':
        try:
            with zipfile.ZipFile(full) as z:
                for zi in z.infolist():
                    if zi.file_size <= 50_000_000 and not zi.is_dir():
                        hits |= scan_bytes(z.read(zi), pats)
        except Exception:
            pass
    return hits


def neutral(rel):
    # Drop the provenance folder and the "_synthetic" suffix some generated files carry.
    rest = rel.split('/', 1)[1]
    return re.sub(r'_synthetic(?=\.|$)', '', rest)


def restore_git_dirs(root):
    """Hardlinking copies files only; git won't open a repo without refs/."""
    n = 0
    for dp, dns, fns in os.walk(root):
        if 'HEAD' in fns and 'objects' in dns and ('config' in fns):
            for sub in ('refs/heads', 'refs/tags'):
                os.makedirs(os.path.join(dp, sub), exist_ok=True)
            n += 1
    return n


def main():
    pats = leak_patterns()
    items = json.load(open(os.path.join(DATA, 'source_items.json')))
    for d in (SANDBOX, PRIVATE):
        if os.path.exists(d):
            shutil.rmtree(d)
    os.makedirs(FILES); os.makedirs(PRIVATE)

    files_of, excluded = {}, {}
    for it in items:
        fs = item_files(it)
        hits = set()
        for f in fs:
            hits |= scan_file(os.path.join(DATA, f), pats)
        if hits:
            excluded[it['id']] = sorted(hits)
        else:
            files_of[it['id']] = fs

    # Destination paths. When two items' files land on the same path, the order that decides
    # who gets a suffix is a hash of the item id, not provenance.
    order = sorted(files_of, key=lambda i: hashlib.sha256((RUN_ID + ':' + i).encode()).hexdigest())
    taken, path_map = {}, {}
    for iid in order:
        for f in files_of[iid]:
            if f in path_map:
                continue
            dest = neutral(f)
            if dest in taken and taken[dest] != f:
                base, ext = os.path.splitext(dest)
                n = 2
                while f'{base} ({n}){ext}' in taken:
                    n += 1
                dest = f'{base} ({n}){ext}'
            taken[dest] = f
            path_map[f] = dest

    linked = 0
    for src, dest in path_map.items():
        d = os.path.join(FILES, dest)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        try:
            os.link(os.path.join(DATA, src), d)
        except OSError:
            shutil.copy2(os.path.join(DATA, src), d)
        linked += 1

    def remap(p):
        if not isinstance(p, str):
            return p
        q = p.rstrip('/')
        if q in path_map:
            return path_map[q]
        if q.startswith(('authentic/', 'synthetic/')):
            return neutral(q) + ('/' if p.endswith('/') else '')
        return p

    out = []
    for it in items:
        if it['id'] not in files_of:
            continue
        row = {k: v for k, v in it.items() if k not in DROP_TOP}
        meta = {k: v for k, v in (it.get('metadata') or {}).items() if k not in DROP_META}
        if 'parts' in meta:
            meta['parts'] = [remap(p) for p in meta['parts']]
        if 'derived_from' in meta:
            meta['derived_from'] = remap(meta['derived_from'])
        row['metadata'] = meta
        row['path'] = remap(it['path'])
        row['files'] = sorted({path_map[f] for f in files_of[it['id']]})
        out.append(row)
    out.sort(key=lambda r: r['id'])
    json.dump(out, open(os.path.join(SANDBOX, 'items.json'), 'w'), indent=1, ensure_ascii=False)

    restore_git_dirs(FILES)

    # Read-only view for the wave 1 local agent.
    lv = os.path.join(SANDBOX, 'local_view')
    for sub in ('claude-code', 'codex', 'github'):
        src = os.path.join(FILES, sub)
        if os.path.isdir(src):
            for dp, dns, fns in os.walk(src):
                for fn in fns:
                    s = os.path.join(dp, fn)
                    t = os.path.join(lv, os.path.relpath(s, FILES))
                    os.makedirs(os.path.dirname(t), exist_ok=True)
                    os.link(s, t)

    restore_git_dirs(lv)
    json.dump(path_map, open(os.path.join(PRIVATE, 'path_map.json'), 'w'), indent=0)
    json.dump(excluded, open(os.path.join(PRIVATE, 'excluded.json'), 'w'), indent=0)

    by_pat = {}
    for hits in excluded.values():
        for h in hits:
            by_pat[h] = by_pat.get(h, 0) + 1
    src_of = {it['id']: it['source'] for it in items}
    by_src = {}
    for iid in excluded:
        by_src[src_of[iid]] = by_src.get(src_of[iid], 0) + 1
    print(json.dumps({'items_in': len(items), 'items_in_sandbox': len(out), 'excluded_items': len(excluded),
                      'excluded_by_pattern': by_pat, 'excluded_by_source': by_src,
                      'files_linked': linked, 'renamed_or_suffixed': sum(1 for s, d in path_map.items() if d != s.split('/', 1)[1])},
                     indent=1))


if __name__ == '__main__':
    main()
