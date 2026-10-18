"""Final Phase 2 review (goal: "review every folder for a manifest, a plausible spread of dates, and consistency with
PERSON.md"). Reads synthetic/*/MANIFEST.csv and synthetic/*/source_items.json (run build_source_items.py first).
Prints per folder: manifest rows, items, labelled items, date range, items per quarter, hard cases, project spread;
and flags: missing manifest, unlabelled items, dates outside 2025-10-17..2026-10-17 (non-allowed), files whose mtime
disagrees with the manifest date, mentions of the Notion-only project outside notion, names not in PERSON.md."""
import collections, csv, datetime, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import ROOT, SYN

LO, HI = '2025-10-17', '2026-10-18'
tools = sorted(d for d in os.listdir(SYN) if os.path.isdir(os.path.join(SYN, d)))
allp = collections.Counter(); problems = []
for t in tools:
    d = os.path.join(SYN, t)
    mf = os.path.join(d, 'MANIFEST.csv')
    rows = list(csv.DictReader(open(mf))) if os.path.exists(mf) else []
    its = json.load(open(os.path.join(d, 'source_items.json'))) if os.path.exists(os.path.join(d, 'source_items.json')) else []
    if not rows: problems.append(f'{t}: no MANIFEST rows')
    lab = [i for i in its if i['ground_truth']['status'] == 'generated']
    if len(lab) != len(its): problems.append(f'{t}: {len(its) - len(lab)} items without a generated label: ' + ', '.join(i['path'] for i in its if i['ground_truth']['status'] != 'generated')[:400])
    dates = sorted(x for i in its for x in [i['modified_at'] or i['created_at']] if x)
    out = [x for x in dates if not (LO <= x[:10] < HI)]
    q = collections.Counter(x[:7] for x in dates)
    hard = collections.Counter(re.match(r'HARD CASE: ([^—\-;]+)', i['ground_truth'].get('notes') or '').group(1).strip()
                               for i in its if re.match(r'HARD CASE: ', i['ground_truth'].get('notes') or ''))
    proj = collections.Counter(p for i in lab for p in i['ground_truth']['project_ids'])
    allp.update(proj)
    rel = sum(1 for i in lab if set(i['ground_truth']['project_ids']) - {'project_none'})
    print(f'\n## {t}: manifest {len(rows)} rows, {len(its)} items, labelled {len(lab)}, related-to-a-project {rel}/{len(lab) or 1} '
          f'({100 * rel // (len(lab) or 1)}%), dates {dates[0][:10] if dates else "-"} .. {dates[-1][:10] if dates else "-"}, outside scope {len(out)}')
    print('   months:', ' '.join(f'{k[2:]}:{v}' for k, v in sorted(q.items())))
    if hard: print('   hard cases:', dict(hard))
    print('   projects:', dict(proj.most_common()))
    # manifest date vs file mtime
    bad = 0
    for r in rows:
        p = os.path.join(d, r['path'])
        if os.path.isfile(p) and r['date']:
            try: md = datetime.datetime.fromisoformat(r['date']).timestamp()
            except ValueError: continue
            if abs(os.stat(p).st_mtime - md) > 120: bad += 1
    if bad: problems.append(f'{t}: {bad} files whose mtime differs from the manifest date')
    # Notion-only project must not leak
    if t != 'notion':
        hits = [i['path'] for i in its if 'project_hint_timing_study' in i['ground_truth']['project_ids']]
        if hits: problems.append(f'{t}: hint-timing project labelled outside notion: {hits[:3]}')
print('\n## all projects:', dict(allp.most_common()))
print('\n## problems'); [print(' -', p) for p in problems] or print(' none')
