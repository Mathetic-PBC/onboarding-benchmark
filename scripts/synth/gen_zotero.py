"""Synthetic Zotero: David's own "My Library", exported the native ways (PERSON.md §1, §3, §6).

  synthetic/zotero/My Library/My Library.bib                    Better BibTeX export of the whole library
  synthetic/zotero/My Library/collections/<Collection>.ris      RIS export of one collection (at the time it was exported)
  synthetic/zotero/My Library/storage/<KEY>/<Author - Year - Title>.pdf   attachments (fictional papers + the Ostrowski paper)
  synthetic/zotero/My Library/notes/<KEY> - <title>.html        child notes (David's reading notes)

Content (papers, notes) is hand-written in content/zotero/. Deterministic; rerun freely.
"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'content', 'zotero'))
from synthlib import *
import dsl
from papers import PAPERS, REAL, WEB
from notes import NOTES
from render import creators_short, paper_pdf

g = Gen('zotero')
LIB = 'My Library'
ACCT = 'My Library'
ZALPHA = '23456789ABCDEFGHIJKLMNPQRSTUVWXYZ'
HOME_STORAGE = '/Users/divadbaroon/Zotero/storage'


def zkey(seed):
    h = int(hexid(('zotero', seed), 24), 16)
    out = ''
    for _ in range(8):
        out += ZALPHA[h % len(ZALPHA)]; h //= len(ZALPHA)
    return out


def zfile_name(p):
    t = re.sub(r'[:?"/\\*<>|]', '', p['title']).replace('  ', ' ')
    return f'{creators_short(p["authors"])} - {p["year"]} - {t}.pdf'


# ---------------------------------------------------------------- the Ostrowski paper (shared, fictional)
OSTRO = dict(key='ostrowski2025productive', type='inproceedings',
             title='Productive Struggle or Silent Stalling? Telemetry Signals of Help-Seeking in LLM-Assisted CS1',
             authors=[('Ostrowski', 'Hannah'), ('Lindqvist', 'Mateo'), ('Bello', 'Aisha'), ('Chandrasekar', 'Ravi')], year=2025,
             booktitle='Proceedings of the Twelfth ACM Conference on Learning @ Scale', series="L@S '25", pages='112--123',
             doi='10.1145/3698205.3729841', added='2026-03-24 01:40', collections=['TutorTrace UIST26'], projects=['project_tutortrace'],
             keywords=['help-seeking', 'telemetry', 'LLM assistants', 'CS1'],
             abstract='Novice programmers who use large language model (LLM) assistants alternate between productive struggle and unproductive '
                      'stalling, yet instructors rarely see which is which. We instrumented an introductory programming course (N=212) with '
                      'editor and assistant telemetry and asked teaching assistants to label 1,904 thirty-second windows as productive '
                      'struggle, stalling, help-seeking, or off-task.')
OSTRO_BIB_RAW = open(os.path.join(SHARED, 'ostrowski2025productive.bib')).read()

ALL = PAPERS + [OSTRO] + REAL + WEB
for e in ALL:
    e['zkey'] = zkey(e['key'])
    e['added_dt'] = dt(e['added'])

# attachments: (entry, attachment key, filename, source file or bytes, attached time, label notes)
ATTACH = []
for p in PAPERS:
    ATTACH.append((p, zkey(p['key'] + '/pdf'), zfile_name(p), paper_pdf(p), p['added'], None))
o_name = zfile_name(OSTRO)
ATTACH.append((OSTRO, zkey('ostrowski/camera'), o_name, os.path.join(SHARED, 'Ostrowski2025_LAS_camera_ready.pdf'), OSTRO['added'],
               'HARD CASE: same paper in several places — Ostrowski et al. 2025 camera-ready (L@S) attached in Zotero; byte-identical to '
               'pdfs/Desktop/papers/Ostrowski2025_LAS.pdf and the copies in gmail/google-docs/slack; overleaf refs.bib cites it'))
ATTACH.append((OSTRO, zkey('ostrowski/arxiv'), o_name, os.path.join(SHARED, 'Ostrowski2025_arXiv_v1.pdf'), '2026-06-13 23:52',
               'HARD CASE: same paper in several places — arXiv v1 of Ostrowski 2025, attached later as the "Preprint PDF" of the same Zotero '
               'item (same filename as the camera-ready attachment, different storage key); near-duplicate of the camera-ready '
               '(F1 0.69 vs 0.71, kappa 0.62 vs 0.64); byte-identical to pdfs/Downloads/2507.01842v1.pdf'))
FILES_OF = {}
for ent, k, name, src, when, _ in ATTACH:
    FILES_OF.setdefault(ent['key'], []).append((k, name))

# ---------------------------------------------------------------- notes
NOTE_OF = {}
for n in NOTES:
    n['zkey'] = zkey('note/' + n['parent'] + n['title'])
    NOTE_OF.setdefault(n['parent'], []).append(n)


def note_html_inner(n, parent):
    cite = f'{creators_short(parent["authors"])}, {parent["year"]}' if parent.get('authors') else parent['title']
    parts, ul = [], []
    first_p = True
    for line in n['body'].strip().split('\n'):
        s = line.strip()
        if not s: continue
        if s.startswith('- '):
            ul.append('<li>' + html.escape(s[2:]) + '</li>'); continue
        if ul: parts.append('<ul>\n' + '\n'.join(ul) + '\n</ul>'); ul = []
        if s.startswith('# '): parts.append('<h1>' + html.escape(s[2:]) + '</h1>'); continue
        if first_p:
            parts.append(f'<p><span class="citation" data-citation="%7B%22citationItems%22%3A%5B%7B%22uris%22%3A%5B%22http%3A%2F%2Fzotero.org%2Fusers%2Flocal%2FmyLibrary%2Fitems%2F{parent["zkey"]}%22%5D%7D%5D%7D">'
                         f'(<span class="citation-item">{html.escape(cite)}</span>)</span> {html.escape(s)}</p>')
            first_p = False
        else:
            parts.append('<p>' + html.escape(s) + '</p>')
    if ul: parts.append('<ul>\n' + '\n'.join(ul) + '\n</ul>')
    return '<div data-schema-version="9">' + '\n'.join(parts) + '\n</div>'


BY_KEY = {e['key']: e for e in ALL}
for n in NOTES:
    parent = BY_KEY[n['parent']]
    inner = note_html_inner(n, parent)
    n['inner'] = inner
    doc = ('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>' + html.escape(n['title']) + '</title>\n</head>\n<body>\n'
           + inner + '\n</body>\n</html>\n')
    mod = later(n['date'], minutes=6, seed=n['zkey'], jitter_min=40)
    safe = re.sub(r'[/:]', '-', n['title'])
    is_o = n['parent'] == 'ostrowski2025productive'
    g.text(f'{LIB}/notes/{n["zkey"]} - {safe}.html', doc, n['date'], mod, account=ACCT, project_ids=n['projects'],
           modeled_on='', source=f'zotero://select/library/items/{n["zkey"]}',
           notes=(f'child note of {parent["key"]} ({parent["zkey"]})' + ('; HARD CASE: same paper in several places — reading note on the '
                  'Ostrowski 2025 paper; mentions the arXiv v1 vs camera-ready copies in Downloads and Desktop/papers' if is_o else '')))

# ---------------------------------------------------------------- attachments
for ent, k, name, src, when, lab in ATTACH:
    rel = f'{LIB}/storage/{k}/{name}'
    meta = dict(account=ACCT, project_ids=ent['projects'], source=f'~/Zotero/storage/{k}/{name}',
                modeled_on='authentic/zotero engelbart-zotero-mirror files/<KEY>/<Author Year Title>.pdf (attachment storage layout)',
                notes=lab or f'attachment of {ent["key"]} ({ent["zkey"]}); fictional paper, fictional authors')
    if isinstance(src, (bytes, bytearray)):
        g.bytes(rel, src, when, when, **meta)
    else:
        g.copy_from(rel, src, when, when, **meta)
    g.dir_times(f'{LIB}/storage/{k}', when, when)

# ---------------------------------------------------------------- BibTeX (Better BibTeX style)


def bib_authors(a):
    return ' and '.join(f'{{{last}}}, {first}' if ' ' in last else f'{last}, {first}' for last, first in a)


def bib_escape(s):
    return s.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#')


def bib_title(t):
    # protect acronyms / capitalized words the way Better BibTeX does
    return re.sub(r'\b([A-Z][A-Za-z0-9@\-]*[A-Z0-9][A-Za-z0-9\-]*)\b', r'{\1}', bib_escape(t))


def bib_entry(e):
    if e['key'] == OSTRO['key']:
        raw = OSTRO_BIB_RAW.rstrip().rstrip('}').rstrip()
        extra = [f"  abstract  = {{{e['abstract']}}}", f"  keywords  = {{{', '.join(e['keywords'])}}}",
                 f"  file      = {{{';'.join(f'{n}:{HOME_STORAGE}/{k}/{n}:application/pdf' for k, n in FILES_OF[e['key']])}}}",
                 f"  timestamp = {{{iso(e['added'], z=True)}}}"]
        return raw + ',\n' + ',\n'.join(extra) + '\n}\n'
    t = {'online': 'misc'}.get(e['type'], e['type'])
    f = [('title', bib_title(e['title']))]
    if e.get('authors'): f.append(('author', bib_authors(e['authors'])))
    for k in ('booktitle', 'journal', 'series', 'volume', 'number', 'pages', 'edition', 'publisher', 'institution', 'address', 'eprint',
              'archiveprefix', 'primaryclass', 'doi'):
        if e.get(k): f.append((k, bib_escape(e[k])))
    if e['type'] != 'online': f.append(('year', str(e['year'])))
    if e.get('url'):
        f.append(('url', e['url'])); f.append(('urldate', dt(e['added']).strftime('%Y-%m-%d')))
    if e.get('abstract'): f.append(('abstract', bib_escape(e['abstract'])))
    if e.get('keywords'): f.append(('keywords', ', '.join(e['keywords'])))
    f.append(('langid', 'english'))
    if e['key'] in FILES_OF:
        f.append(('file', ';'.join(f'{n}:{HOME_STORAGE}/{k}/{n}:application/pdf' for k, n in FILES_OF[e['key']])))
    f.append(('timestamp', iso(e['added'], z=True)))
    body = ',\n'.join(f'  {k} = {{{v}}}' for k, v in f)
    return f'@{t}{{{e["key"]},\n{body}\n}}\n'


BIB_AT = '2026-10-14 23:05'
bib = ''.join(bib_entry(e) + '\n' for e in sorted(ALL, key=lambda x: x['key']) if e['added_dt'] <= dt(BIB_AT))
all_projects = sorted({pid for e in ALL for pid in e['projects'] if pid != 'project_none'})
g.text(f'{LIB}/{LIB}.bib', bib, BIB_AT, BIB_AT, account=ACCT, project_ids=all_projects,
       source='~/Desktop/My Library.bib', modeled_on='authentic/zotero engelbart-zotero-mirror/library.bib (BibTeX export shape)',
       notes=f'HARD CASE: same paper in several places — Better BibTeX export of the whole library ({bib.count("@")} entries) incl. '
             'ostrowski2025productive (also in the TutorTrace collection RIS, overleaf refs.bib, and as PDFs in pdfs/); exported 10-14 to '
             'test the Engelbart import; mixes project readings with a few unrelated items (running physiology, geopolitics)')

# ---------------------------------------------------------------- RIS collection exports
RIS_TYPE = {'article': 'JOUR', 'inproceedings': 'CPAPER', 'book': 'BOOK', 'techreport': 'RPRT', 'online': 'ELEC'}


def ris_entry(e, upto):
    L = [('TY', RIS_TYPE[e['type']]), ('TI', e['title'])]
    for last, first in e.get('authors', []): L.append(('AU', f'{last}, {first}'))
    if e.get('eprint'): L.append(('T2', 'arXiv preprint')); L.append(('M3', f'arXiv:{e["eprint"]}'))
    elif e.get('journal'): L.append(('T2', e['journal']))
    if e.get('booktitle'): L.append(('T2', e['booktitle']))
    if e.get('series'): L.append(('T3', e['series']))
    if e.get('volume'): L.append(('VL', e['volume']))
    if e.get('number') and e['type'] != 'techreport': L.append(('IS', e['number']))
    if e.get('number') and e['type'] == 'techreport': L.append(('M1', e['number']))
    if e.get('pages'):
        sp, *ep = e['pages'].split('--'); L.append(('SP', sp))
        if ep: L.append(('EP', ep[0]))
    if e['type'] != 'online': L.append(('PY', str(e['year'])))
    L.append(('DA', dt(e['added']).strftime('%Y/%m/%d/')))
    if e.get('publisher') or e.get('institution'): L.append(('PB', e.get('publisher') or e.get('institution')))
    if e.get('address'): L.append(('CY', e['address']))
    if e.get('edition'): L.append(('ET', e['edition']))
    if e.get('doi'): L.append(('DO', e['doi']))
    if e.get('url'): L.append(('UR', e['url'])); L.append(('Y2', dt(e['added']).strftime('%Y/%m/%d/%H:%M:%S')))
    if e.get('abstract'): L.append(('AB', e['abstract']))
    L.append(('LA', 'en'))
    for kw in e.get('keywords', []): L.append(('KW', kw))
    for k, n in FILES_OF.get(e['key'], []): L.append(('L1', f'storage/{k}/{n}'))
    for n in NOTE_OF.get(e['key'], []):
        if dt(n['date']) <= dt(upto): L.append(('N1', n['inner'].replace('\n', '')))
    L.append(('ER', ''))
    return '\r\n'.join(f'{a}  - {b}' for a, b in L) + '\r\n\r\n'


COLLECTIONS = [
    ('TutorTrace UIST26', '2026-06-16 00:40', None),
    ('IDETrace', '2026-07-28 01:10', None),
    ('ISE 6664 readings', '2026-04-28 22:15', None),
    ('Augmenting cognition', '2026-09-30 21:30', None),
    ('Engelbart competitors', '2026-10-13 22:40', None),
    ('PlotPact (old)', '2026-01-29 23:05', 'old PlotPact collection (items added Nov 2024), re-exported while revisiting constraint-based creativity'),
]
for name, when, extra in COLLECTIONS:
    ents = [e for e in ALL if name in e['collections'] and e['added_dt'] <= dt(when)]
    ents.sort(key=lambda e: e['added_dt'])
    # an attachment added after the export (the Ostrowski preprint PDF) must not be listed
    text = ''
    for e in ents:
        saved = FILES_OF.get(e['key'])
        if saved:
            FILES_OF[e['key']] = [(k, n) for (ent, k, n, src, w, _) in ATTACH if ent['key'] == e['key'] and dt(w) <= dt(when)]
        text += ris_entry(e, when)
        if saved: FILES_OF[e['key']] = saved
    pids = sorted({pid for e in ents for pid in e['projects']})
    hard = name == 'TutorTrace UIST26'
    g.text(f'{LIB}/collections/{name}.ris', text, when, when, account=ACCT, project_ids=pids, source=f'~/Downloads/{name}.ris',
           modeled_on='',
           notes=(('HARD CASE: same paper in several places — ' if hard else '') +
                  f'RIS export of the "{name}" collection ({len(ents)} items as of {when[:10]})' +
                  (' incl. the Ostrowski 2025 entry with its camera-ready PDF link and reading note' if hard else '') +
                  (('; ' + extra) if extra else '')))

for d in ('storage', 'notes', 'collections'):
    g.dir_times(f'{LIB}/{d}', '2026-01-14 21:20', BIB_AT)
g.dir_times(LIB, '2024-11-06 22:14', BIB_AT)
g.finish()
