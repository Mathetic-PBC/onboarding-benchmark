"""Synthetic "PDFs on this Mac": PDFs under home-relative paths (Desktop/, Downloads/, iCloud Drive/), like authentic/pdfs.
File times = when David saved/downloaded the file; PDF internal CreationDate/ModDate = when the document was made.
Content in content/pdfs/docs.py (plus the shared Ostrowski paper, the fictional Zotero papers, and the Overleaf texts)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
for sub in ('zotero', 'overleaf', 'pdfs'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'content', sub))
from synthlib import *
import dsl
from render import paper_pdf
from papers import PAPERS
import docs as D
import idetrace_rebuttal as IR
import ise_report as ISE
import onepager_talk as OT

g = Gen('pdfs')
MODEL = 'authentic/pdfs home-relative PDF layout (Desktop/, Downloads/, iCloud Drive/)'
PAPER = {p['key']: p for p in PAPERS}


def acct(path):
    return path.split('/')[0]


def put(rel, data, created, modified, projects, notes, modeled_on=MODEL):
    g.bytes(rel, data, created, modified, account=acct(rel), project_ids=projects, source='~/' + rel, modeled_on=modeled_on, notes=notes)

# ---------------------------------------------------------------- the Ostrowski paper (shared, fictional)
g.copy_from('Downloads/2507.01842v1.pdf', os.path.join(SHARED, 'Ostrowski2025_arXiv_v1.pdf'), '2026-03-23 23:48', '2026-03-23 23:48',
            account='Downloads', project_ids=['project_tutortrace'], source='~/Downloads/2507.01842v1.pdf', modeled_on=MODEL,
            notes='HARD CASE: same paper in several places — arXiv v1 of Ostrowski et al. 2025 (fictional); near-duplicate of the camera-ready '
                  'in Desktop/papers (F1 0.69 vs 0.71, kappa 0.62 vs 0.64); also attached in zotero as the preprint PDF')
g.copy_from('Desktop/papers/Ostrowski2025_LAS.pdf', os.path.join(SHARED, 'Ostrowski2025_LAS_camera_ready.pdf'), '2026-03-24 01:38',
            '2026-03-24 01:38', account='Desktop', project_ids=['project_tutortrace'], source='~/Desktop/papers/Ostrowski2025_LAS.pdf',
            modeled_on=MODEL,
            notes='HARD CASE: same paper in several places — camera-ready of Ostrowski et al. 2025 (fictional); byte-identical to the Zotero '
                  'attachment; near-duplicate of ~/Downloads/2507.01842v1.pdf')

# ---------------------------------------------------------------- TutorTrace camera-ready + exact duplicate download
cr_blocks = [('title', D.TUTORTRACE_CR_TITLE)] + dsl.parse(D.TUTORTRACE_CR)
cr = pdf_bytes(cr_blocks, D.TUTORTRACE_CR_TITLE, '', '2026-08-10 14:02', '2026-08-14 21:30')
put('Downloads/TutorTrace_UIST26_camera_ready.pdf', cr, '2026-08-14 21:41', '2026-08-14 21:41', ['project_tutortrace'],
    'HARD CASE: near-duplicate — TutorTrace UIST camera-ready PDF downloaded from Overleaf on the camera-ready deadline; an exact '
    'duplicate "(1)" was downloaded again for talk prep')
put('Downloads/TutorTrace_UIST26_camera_ready (1).pdf', cr, '2026-09-22 22:10', '2026-09-22 22:10', ['project_tutortrace'],
    'HARD CASE: near-duplicate — exact duplicate download (byte-identical) of TutorTrace_UIST26_camera_ready.pdf, re-downloaded 09-22 '
    'when starting the talk slides')

# ---------------------------------------------------------------- renderers for the other kinds


def slides_blocks():
    out = []
    frames = re.findall(r'\\begin\{frame\}(\{[^}]*\})?(.*?)\\end\{frame\}', OT.TALK, re.S)
    for i, (ft, body) in enumerate(frames):
        if i: out.append(('pagebreak', None))
        if not ft:
            out += [('title', 'TutorTrace: Classifying Learner States in AI-Assisted Programming'),
                    ('p', 'UIST 2026 -- Session "Learning & Tutoring"'), ('p', 'David Barron -- PRIME Lab, Virginia Tech'),
                    ('p', 'joint work with Minsun, Xiaohang, Rezky, Yue and Yan Chen'), ('p', 'October 7, 2026')]
            continue
        out.append(('h1', ft.strip('{}')))
        rows = re.findall(r'^[ \t]*([^\n&]*?)[ \t]*&[ \t]*([^\n]+?)[ \t]*\\\\', body, re.M)
        if rows:
            out.append(('table', [[clean(a), clean(b)] for a, b in rows]))
        for line in body.split('\n'):
            s = line.strip()
            if s.startswith('\\item'):
                out.append(('bullet', clean(s[5:])))
            elif s and not s.startswith('\\') and '&' not in s:
                out.append(('p', clean(s)))
            elif s.startswith('\\textbf') or s.startswith('\\Large') or s.startswith('\\normalsize') or s.startswith('David'):
                t = clean(s)
                if t: out.append(('p', t))
    return out


def clean(s):
    s = s.replace('``', '"').replace("''", '"').replace('\\\\', ' ').replace('\\&', '&').replace('\\quad', ' ').replace('--', '–').replace("\\'a", 'á')
    s = re.sub(r'\$\\kappa\s*=\s*', 'kappa = ', s)
    s = re.sub(r'\$\\kappa\$', 'kappa', s)
    s = re.sub(r'\\(textbf|texttt|emph)\{([^}]*)\}', r'\2', s)
    s = re.sub(r'\\(Large|normalsize|centering|vspace\{[^}]*\})', '', s)
    s = re.sub(r'\[[0-9.]+em\]', '', s)
    s = s.replace('\\ ', ' ').replace('$', '').replace('\\', '')
    return re.sub(r'\s+', ' ', s).strip()


def bib_refs(bib):
    refs = []
    for m in re.finditer(r'@\w+\{(\w+),(.*?)\n\}', bib, re.S):
        f = dict(re.findall(r'(\w+)\s*=\s*\{(.*?)\},?\s*$', m.group(2), re.M))
        authors = f.get('author', '').replace('{\\\'e}', 'é').replace("{\\'i}", 'í').split(' and ')
        a = ', '.join(x.split(',')[0] for x in authors[:3]) + (' et al.' if len(authors) > 3 else '')
        venue = f.get('journal') or f.get('booktitle') or f.get('publisher', '')
        t = re.sub(r'[{}]', '', f.get('title', '')).replace('``', '"').replace("''", '"')
        refs.append((a, f"{a} ({f.get('year', '')}). {t}. {venue}" + (f", {f['volume']}({f.get('number', '')})" if f.get('volume') else '')
                     + (f", {f['pages'].replace('--', '-')}" if f.get('pages') else '') + '.'))
    return [r for _, r in sorted(refs)]


def cite_map(bib):
    m = {}
    for e in re.finditer(r'@\w+\{(\w+),(.*?)\n\}', bib, re.S):
        f = dict(re.findall(r'(\w+)\s*=\s*\{(.*?)\},?\s*$', e.group(2), re.M))
        au = [x.split(',')[0].strip() for x in f.get('author', '').split(' and ')]
        a = au[0] if len(au) == 1 else (f'{au[0]} and {au[1]}' if len(au) == 2 else f'{au[0]} et al.')
        m[e.group(1)] = f"{a}, {f.get('year', '')}"
    return m


def cites(text, bib):
    m = cite_map(bib)
    return re.sub(r'\[\[\\citep\{([^}]*)\}\]\]', lambda x: '(' + '; '.join(m[k.strip()] for k in x.group(1).split(',')) + ')', text)


def ise_blocks(draft=False):
    title = ISE.TITLE if not draft else 'Frustration Signals in AI-Tutoring Transcripts (DRAFT)'
    b = [('title', title), ('p', ', '.join(ISE.AUTHORS)), ('p', ISE.COURSE.replace('--', '–')), ('p', ISE.INSTRUCTOR),
         ('p', 'May 2, 2026' if not draft else 'Draft of April 28, 2026 -- not for submission'), ('h2', 'Abstract')]
    abstract = ISE.ABSTRACT
    if draft:
        abstract = abstract.replace('raised it to 0.79', 'raised it to 0.77').replace(' We close with design implications for assistants '
                   'that notice frustration and respond with acknowledgement, reframing and a change of strategy rather than another code block.',
                   ' [TODO: implications sentence once Section 7 is written.]')
    b.append(('p', abstract))
    b.append(('pagebreak', None))
    for slug, head, body in ISE.SECTIONS:
        if draft and slug == 'discussion':
            b += [('h1', '7 Design Implications'), ('p', '[Jordan drafting -- due Thursday before the presentation.]')]
            continue
        if draft and slug == 'conclusion':
            b += [('h1', '9 Conclusion'), ('p', '[TODO]')]
            continue
        if draft and slug == 'contributions':
            continue
        if draft:
            body = body.replace(*ISE.DRAFT_RESULTS_TABLE_OLD).replace('raised it to 0.79', 'raised it to 0.77')
        b.append(('h1', head))
        b += dsl.plain_blocks(dsl.parse(cites(body, ISE.BIB)))
    b.append(('pagebreak', None))
    b.append(('h1', 'References'))
    b += [('p', r) for r in bib_refs(ISE.BIB)]
    return b


def ide_blocks():
    b = [('title', IR.TITLE.replace('--', '–'))] + dsl.plain_blocks(dsl.parse(cites(IR.BODY, IR.REFS_BIB)))
    b.append(('h2', 'References'))
    b += [('p', r) for r in bib_refs(IR.REFS_BIB)]
    return b

# ---------------------------------------------------------------- the hand-written documents
for d in D.DOCS:
    created, modified = d['file']
    pc, pm = d.get('pdf', (created, modified))
    kind = d.get('kind')
    if kind == 'zotero_paper':
        p = PAPER[d['paper_key']]
        data = paper_pdf(p)
    elif kind == 'slides':
        data = pdf_bytes(slides_blocks(), d['title'], '', '2026-10-06 23:14', '2026-10-06 23:14')
    elif kind == 'idetrace_rebuttal':
        data = pdf_bytes(ide_blocks(), d['title'], '', pc, pm)
    elif kind == 'ise_final':
        data = pdf_bytes(ise_blocks(), ISE.TITLE, '', '2026-05-02 01:14', '2026-05-02 01:14')
    elif kind == 'ise_draft':
        data = pdf_bytes(ise_blocks(draft=True), 'Frustration Signals in AI-Tutoring Transcripts (DRAFT)', '', '2026-04-29 01:18', '2026-04-29 01:18')
    else:
        data = pdf_bytes([('title', d['title'])] + dsl.parse(d['body']), d['title'], d.get('author', ''), pc, pm)
    put(d['path'], data, created, modified, d['projects'], d['notes'])

# folder times
for folder, c, m in [('Downloads', '2025-11-15 01:12', '2026-10-14 01:33'), ('Desktop/papers', '2026-03-24 01:38', '2026-09-02 23:29'),
                     ('Desktop/ISE6664', '2026-04-29 01:22', '2026-05-02 01:21'), ('Desktop/IDETrace', '2026-07-25 14:12', '2026-07-25 14:12'),
                     ('Desktop/vizpi', '2025-11-11 23:34', '2025-11-12 13:05'), ('Desktop/engelbart', '2026-10-14 01:33', '2026-10-14 01:33'),
                     ('Desktop/UIST talk', '2026-10-06 23:20', '2026-10-06 23:20'), ('iCloud Drive', '2025-10-29 15:41', '2026-08-05 00:12')]:
    g.dir_times(folder, c, m)
g.finish()
