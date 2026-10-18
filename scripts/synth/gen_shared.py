"""Shared synthetic assets (PERSON.md §6, 'same paper in several places'): the fictional Ostrowski et al. 2025 paper, as the
arXiv v1 and the camera-ready v2 (near-duplicates), plus its BibTeX. Generators copy these into zotero, pdfs, gmail, google-docs,
overleaf and slack."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import pdf_bytes, epoch, SHARED
import os

os.makedirs(SHARED, exist_ok=True)
TITLE = 'Productive Struggle or Silent Stalling? Telemetry Signals of Help-Seeking in LLM-Assisted CS1'
AUTHORS = 'Hannah Ostrowski, Mateo Lindqvist, Aisha Bello, and Ravi Chandrasekar'


def body(version):
    camera = version == 2
    b = [('title', TITLE),
         ('p', AUTHORS + (' — Proceedings of the 2025 ACM Conference on Learning at Scale (L@S \'25)' if camera else ' — arXiv:2507.01842v1 [cs.HC], 3 Jul 2025')),
         ('h2', 'Abstract'),
         ('p', 'Novice programmers who use large language model (LLM) assistants alternate between productive struggle and unproductive '
               'stalling, yet instructors rarely see which is which. We instrumented an introductory programming course (N=212) with '
               'editor and assistant telemetry and asked teaching assistants to label 1,904 thirty-second windows as productive struggle, '
               'stalling, help-seeking, or off-task. A gradient-boosted classifier over keystroke, run, and prompt features reached '
               + ('0.71' if camera else '0.69') + ' macro-F1 against TA labels. Stalling was best predicted by repeated near-identical '
               'prompts and long idle gaps after an error, while productive struggle co-occurred with frequent small edits and test runs. '
               'We discuss what instructors can and cannot infer from telemetry, and release our labeling guide.'),
         ('h1', '1 Introduction'),
         ('p', 'LLM assistants are now a default part of many CS1 courses. Their availability changes when and how students ask for '
               'help: a student who once raised a hand after twenty minutes can now ask an assistant after twenty seconds. Prior work on '
               'productive failure and desirable difficulties suggests some struggle is valuable, but distinguishing valuable struggle '
               'from stalling has relied on think-alouds and observation, which do not scale.'),
         ('p', 'We ask: RQ1, which telemetry signals distinguish productive struggle from stalling? RQ2, how reliably can trained '
               'TAs label these states from replayed sessions? RQ3, how well does a simple classifier reproduce TA labels?'),
         ('h1', '2 Related Work'),
         ('p', 'Help-seeking in programming has been studied through office-hours logs, forum posts, and intelligent tutoring '
               'systems. Keystroke-level data has been used to predict struggle and dropout. Recent work examines how students prompt '
               'code assistants and how instructors perceive these tools. We extend this line by labeling behavioral states in '
               'sessions that interleave editor activity and assistant prompts.'),
         ('h1', '3 Method'),
         ('p', 'Participants were students in two sections of an introductory Python course at a large public university. A browser '
               'IDE recorded edits, runs, test results and assistant prompts. Each session was cut into thirty-second windows; four TAs '
               'labeled windows after a two-hour calibration using our labeling guide (Appendix A).'),
         ('table', [['State', 'Windows', 'Share'], ['Productive struggle', '612', '32%'], ['Stalling', '441', '23%'],
                    ['Help-seeking', '538', '28%'], ['Off-task', '313', '16%']]),
         ('p', 'Inter-rater agreement on a 10% overlap sample was Cohen\'s kappa = ' + ('0.64' if camera else '0.62') + '.'),
         ('h1', '4 Results'),
         ('p', 'Repeated near-identical prompts (edit distance under 15% between consecutive prompts) were the strongest single '
               'predictor of stalling. Long idle gaps following a failed run were the second. Productive struggle windows showed '
               'more small edits per minute and more test runs.'),
         ('p', 'The classifier reached ' + ('0.71' if camera else '0.69') + ' macro-F1 with session-level cross-validation. '
               'Performance dropped to 0.58 when windows from the same student appeared in both train and test folds were removed '
               'from the comparison baseline, which we report to make leakage visible.'),
         ('pagebreak', None),
         ('h1', '5 Discussion'),
         ('p', 'Telemetry can flag likely stalling but cannot tell an instructor why a student stalled. We recommend surfacing '
               'flags as prompts for a human check-in rather than automatic interventions. Hint timing matters: hints offered during '
               'productive struggle were rated as less helpful by students in a follow-up survey.'),
         ('h1', '6 Limitations'),
         ('p', 'One institution, one course, one assistant. TA labels are themselves an imperfect proxy for students\' experience.'),
         ('h1', 'References'),
         ('p', '[1] Kapur, M. Productive failure. Cognition and Instruction, 2008.'),
         ('p', '[2] Bjork, R. A. Memory and metamemory considerations in the training of human beings, 1994.'),
         ('p', '[3] Price, T. W. et al. Factors influencing students\' help-seeking behavior while programming with human and computer tutors. ICER 2017.'),
         ]
    if camera:
        b.insert(-4, ('h1', 'Acknowledgments'))
        b.insert(-4, ('p', 'We thank the TAs who labeled sessions and the students who consented to share their data.'))
    return b


v1 = pdf_bytes(body(1), TITLE, '', '2025-07-03 09:12', '2025-07-03 09:12')
v2 = pdf_bytes(body(2), TITLE, '', '2025-06-20 16:40', '2025-08-11 10:05')
for name, data, when in [('Ostrowski2025_arXiv_v1.pdf', v1, '2025-07-03 09:12'), ('Ostrowski2025_LAS_camera_ready.pdf', v2, '2025-08-11 10:05')]:
    p = os.path.join(SHARED, name)
    open(p, 'wb').write(data); os.utime(p, (epoch(when), epoch(when)))

bib = """@inproceedings{ostrowski2025productive,
  title     = {Productive Struggle or Silent Stalling? Telemetry Signals of Help-Seeking in {LLM}-Assisted {CS1}},
  author    = {Ostrowski, Hannah and Lindqvist, Mateo and Bello, Aisha and Chandrasekar, Ravi},
  booktitle = {Proceedings of the Twelfth ACM Conference on Learning @ Scale},
  series    = {L@S '25},
  year      = {2025},
  pages     = {112--123},
  doi       = {10.1145/3698205.3729841},
  note      = {Fictional paper (synthetic benchmark data)}
}
"""
open(os.path.join(SHARED, 'ostrowski2025productive.bib'), 'w').write(bib)
print(os.listdir(SHARED))
