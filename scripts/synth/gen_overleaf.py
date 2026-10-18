"""Synthetic Overleaf: six of David's projects as Overleaf "Download Source" zips under synthetic/overleaf/dbarron410@vt.edu/
(layout of authentic/overleaf). Per-file dates inside each zip = when that file was last edited. Content in content/overleaf/."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'content', 'zotero'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'content', 'overleaf'))
from synthlib import *
import dsl
import tutortrace_rebuttal as TT
import idetrace_rebuttal as IR
import ise_report as ISE
import onepager_talk as OT

g = Gen('overleaf')
ACCT = 'dbarron410@vt.edu'
MODEL = 'authentic/overleaf/dbarron410@vt.edu/<Project name>.zip (Overleaf "Download Source" zip)'


def apply(text, edits, reverse=False):
    for a, b in edits:
        if reverse: a, b = b, a
        assert a in text, a[:70]
        text = text.replace(a, b)
    return text


def project(name, files, created, modified, projects, notes='', main=None):
    pid = hexid(('overleaf', name), 24)
    rel = f'{ACCT}/{name}.zip'
    mains = main or [n for n, *_ in files if n.endswith('.tex')][:1]
    meta = (f'project id {pid}; owner {ACCT}; access owner (owner); {len(files)} files; main .tex: {mains}; last updated by {ACCT}')
    g.zip(rel, files, created, modified, account=ACCT, project_ids=projects, source=f'https://www.overleaf.com/project/{pid}',
          modeled_on=MODEL, notes=(notes + '; ' if notes else '') + meta)

# ---------------------------------------------------------------- 1+2. TutorTrace rebuttal and its copy
ostro_bib = open(os.path.join(SHARED, 'ostrowski2025productive.bib')).read()
tt_bib = ostro_bib + TT.REFS_BIB_REST
project('TutorTrace UIST26 rebuttal', [
    ('refs.bib', tt_bib, '2026-06-13 23:58'),
    ('response_matrix.tex', TT.MATRIX_TEX, '2026-06-15 02:10'),
    ('rebuttal.tex', TT.REBUTTAL_TEX, '2026-06-18 21:40'),
], '2026-06-12 00:34', '2026-06-18 21:52', ['project_tutortrace'],
    notes='HARD CASE: same paper in several places — refs.bib carries the ostrowski2025productive entry (also in zotero, pdfs, gmail, '
          'google-docs, slack); rebuttal submitted 2026-06-18')

copy_reb = apply(TT.REBUTTAL_TEX, TT.COPY_EDITS_REBUTTAL)
copy_mat = apply(TT.MATRIX_TEX, TT.COPY_EDITS_MATRIX)
project('Copy of TutorTrace UIST26 rebuttal', [
    ('refs.bib', tt_bib, '2026-06-20 11:05'),
    ('response_matrix.tex', copy_mat, '2026-06-20 15:31'),
    ('rebuttal.tex', copy_reb, '2026-06-20 16:02'),
], '2026-06-20 11:05', '2026-06-20 16:09', ['project_tutortrace'],
    notes='HARD CASE: near-duplicate — Overleaf "Copy of" the rebuttal project made two days after submission; same three files, a '
          'few edits (camera-ready TODO block, one reworded sentence, status column updated); refs.bib identical incl. ostrowski2025productive')

# ---------------------------------------------------------------- 3. IDETrace NeurIPS rebuttal
ide_body = dsl.to_latex(dsl.parse(IR.BODY), h1='section*', h2='section*', h3='subsection*')
ide_tex = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\usepackage[numbers]{natbib}
\usepackage{hyperref}

% NeurIPS 2026 D&B author response. OpenReview takes markdown, so this is the drafting copy;
% tables get pasted as markdown. Posted 2026-07-29.

\title{""" + dsl.tex(IR.TITLE) + r"""}
\date{}

\begin{document}
\maketitle
""" + ide_body + r"""
\bibliographystyle{plainnat}
\bibliography{refs}
\end{document}
"""
project('IDETrace NeurIPS rebuttal', [
    ('refs.bib', IR.REFS_BIB, '2026-07-25 02:03'),
    ('split_numbers.tex', IR.SPLIT_NOTES, '2026-07-27 23:51'),
    ('rebuttal.tex', ide_tex, '2026-07-29 18:20'),
], '2026-07-25 01:31', '2026-07-29 18:26', ['project_idetrace'],
    notes='author response reporting the leakage fix (macro-F1 0.81 -> 0.74, grouped by student id)')

# ---------------------------------------------------------------- 4. ISE 6664 Final Report
CAPTIONS = {
    'method': ['Dataset summary.'],
    'codebook': ['Final codebook: frustration and confusion markers, with examples paraphrased from the data.'],
    'results': ['Probability that the next student turn is coded frustrated, by preceding event.',
                'Turn-level frustration detection (5-fold cross-validation grouped by student).'],
}
SECTION_DATES = {'introduction': '2026-04-26 23:40', 'background': '2026-04-27 01:15', 'related': '2026-04-27 22:30',
                 'method': '2026-04-28 00:55', 'codebook': '2026-04-28 23:20', 'results': '2026-05-01 22:47',
                 'discussion': '2026-05-02 00:31', 'limitations': '2026-05-02 00:44', 'conclusion': '2026-05-02 01:02',
                 'contributions': '2026-05-02 01:10'}
ise_files = []
for slug, head, body in ISE.SECTIONS:
    if slug == 'contributions':
        tex = '\\section*{Team Contributions}\n' + dsl.to_latex(dsl.parse(body))
    else:
        tex = dsl.to_latex([('h1', head)] + dsl.parse(body), caption_prefix=CAPTIONS.get(slug))
        tex = tex.lstrip('\n')
        eol = tex.index('\n')
        tex = tex[:eol] + '\\label{sec:' + slug + '}' + tex[eol:]
    ise_files.append((f'sections/{slug}.tex', f'% {head}\n' + tex, SECTION_DATES[slug]))

ise_main = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=1in]{geometry}
\usepackage{setspace}
\usepackage{booktabs}
\usepackage[round]{natbib}
\usepackage{hyperref}
\doublespacing

\title{""" + dsl.tex(ISE.TITLE) + r"""}
\author{""" + r' \and '.join(ISE.AUTHORS) + r"""}
\date{\small """ + dsl.tex(ISE.COURSE) + r"""\\ \small """ + dsl.tex(ISE.INSTRUCTOR) + r"""\\[0.5em] May 2, 2026}

\begin{document}
\maketitle
\thispagestyle{empty}

\begin{abstract}
""" + dsl.tex(ISE.ABSTRACT) + r"""
\end{abstract}
\clearpage

""" + '\n'.join(f'\\input{{sections/{slug}}}' for slug, *_ in ISE.SECTIONS) + r"""

\clearpage
\bibliographystyle{plainnat}
\bibliography{refs}
\end{document}
"""
ise_files = [('refs.bib', ISE.BIB, '2026-04-28 00:20'), ('main.tex', ise_main, '2026-05-02 01:14')] + ise_files
ise_files.sort(key=lambda x: x[2])
project('ISE 6664 Final Report', ise_files, '2026-04-21 21:12', '2026-05-02 01:14', ['project_ise6664_affective_computing'],
        notes='team report with Maya Torres and Jordan Lee (Dr. Alan Brooks); ~14 pages double-spaced', main=['main.tex'])

# ---------------------------------------------------------------- 5. Mathetic one-pager
onepager = apply(OT.ONEPAGER_V1, OT.ONEPAGER_EDITS)
project('Mathetic one-pager', [
    ('README.txt', OT.ONEPAGER_README, '2026-08-13 22:15'),
    ('onepager.tex', onepager, '2026-08-18 22:41'),
], '2026-08-13 21:50', '2026-08-18 22:41', ['project_mathetic_company', 'project_engelbart'],
    notes='one-page company/product summary for the Surplus program and the first Marcus Oyelaran call (2026-08-20)', main=['onepager.tex'])

# ---------------------------------------------------------------- 6. UIST talk (beamer)
project('UIST26 talk script (beamer)', [
    ('README.txt', OT.TALK_README, '2026-10-05 23:30'),
    ('talk.tex', OT.TALK, '2026-10-06 23:12'),
], '2026-09-22 22:05', '2026-10-06 23:12', ['project_tutortrace'],
    notes='beamer slides with \\note{} speaker script for the 2026-10-07 UIST talk (session "Learning & Tutoring", chair Tomás Reyes)',
    main=['talk.tex'])

g.dir_times(ACCT, '2026-04-21 21:12', '2026-10-06 23:12')
g.finish()
