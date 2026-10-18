"""TutorTrace UIST 2026 rebuttal (Overleaf project) and its 'Copy of' near-duplicate. All text written by David (synthetic).
PERSON.md §7: reviews 2026-06-11 asked about label reliability (kappa 0.71, 3 raters), generalization beyond one course and the
privacy of telemetry; the rebuttal (due 2026-06-18) promised a cross-course analysis and a limitations section."""

REBUTTAL_TEX = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{natbib}
\usepackage{hyperref}

% UIST 2026 rebuttal, paper #2214 -- plain text box on PCS, limit 5,000 characters.
% Draft here, paste into PCS. Keep \cite out of the pasted version.
\newcommand{\todo}[1]{\textcolor{red}{[TODO: #1]}}
\newcommand{\rev}[1]{\textbf{#1}}

\title{TutorTrace -- Rebuttal (UIST 2026, \#2214)}
\date{Draft: June 2026}

\begin{document}
\maketitle

We thank the reviewers for careful reviews. All reviewers found the dataset and the taxonomy useful; the main concerns were
(1) the reliability of the labels, (2) generalization beyond a single course, and (3) the privacy of fine-grained telemetry.
We address each and list concrete changes for the camera-ready.

\section*{1. Label reliability (\rev{1AC}, \rev{R2}, \rev{R3})}
Three raters labeled all 2,340 thirty-second windows independently after two calibration rounds using our labeling guide (v3).
Agreement across the three raters was Fleiss' $\kappa = 0.71$ overall. R2 asked for per-state agreement: it ranges from 0.84
(assistant help-seeking, which is an observable event) to 0.58 (exploratory tinkering vs.\ stalled-after-error, the hardest
boundary). This matches the pattern reported by \citet{nakamura2025labeling}, who also found most disagreement at the
tinkering/stuck boundary. Guide v3 added an explicit rule for that boundary (no successful run in the previous three minutes and
reverted edits $\rightarrow$ stalled-after-error); agreement on that pair rose from 0.49 (v2) to 0.58 (v3).
\textbf{Change:} we will add the per-state $\kappa$ table, the decision rules, and the disagreement matrix to the appendix.

For comparison, \citet{ostrowski2025productive} report $\kappa = 0.64$ with four TAs on a 10\% overlap sample; our scheme
separates stalled-after-error from general stalling, so the numbers are not directly comparable and we will say so.

\section*{2. Generalization beyond one course (\rev{R1}, \rev{R3})}
R1 and R3 are right that all labeled sessions come from one course (CS 3114, Fall 2025). We have consented telemetry from a second
course (an introductory Python course, Spring 2026) collected with the same instrumentation. \textbf{Change:} the camera-ready will
include a cross-course analysis: we will label a sample from the second course with the same guide and raters, train on CS 3114 and
test on the second course, reporting both raw and per-course normalized features, following the protocol of
\citet{duarte2025beyond}. We will report the result whatever it is; we expect the stalled-after-error state to transfer least
because it depends on the error channel. We will also soften claims in the abstract and introduction from ``novice programmers'' to
``students in the studied course'' where the evidence is single-course.

\section*{3. Privacy of telemetry (\rev{R2})}
Consent separated three streams (editor events, run results, assistant prompts); 9 of 87 students declined prompt logging.
The released dataset contains derived features and labels for all consenting students, and raw prompt text only for students who
opted in to its release. Identifiers are replaced with per-release random ids, and string literals are stripped from code
snapshots. Survey evidence suggests prompts are the stream students are least comfortable sharing \citep{brennan2026what}; we will
cite this and describe our per-stream consent design in the paper. \textbf{Change:} a new ``Data and consent'' subsection and a
datasheet in the supplementary material.

\section*{4. Other points}
\begin{itemize}
  \item \rev{R1}: \emph{``How were the 12\% dropped events handled?''} A websocket reconnect bug dropped telemetry for one lab
        section until a hotfix during the session. Windows overlapping the gap were excluded before labeling (they are listed in
        the release); we will state this in the paper.
  \item \rev{R3}: \emph{``Relation to productive failure.''} We will expand the discussion of productive struggle
        \citep{kapur2008productive} and explain why stalled-after-error is not the same as productive failure.
  \item \rev{1AC}: \emph{``Limitations are thin.''} \textbf{Change:} a dedicated Limitations section (single institution, label
        subjectivity, telemetry gaps, and the dependence of states on the assistant used).
\end{itemize}

\section*{Summary of changes}
(1) per-state agreement and decision rules; (2) cross-course analysis; (3) data and consent subsection plus datasheet;
(4) dedicated limitations section; (5) softened generality claims.

\bibliographystyle{plainnat}
\bibliography{refs}
\end{document}
"""

MATRIX_TEX = r"""% Response matrix: every reviewer point -> response -> paper change -> owner.
% Included from rebuttal.tex? No -- compile on its own (Menu > Main document) to print for the lab meeting.
\documentclass[10pt,landscape]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=0.6in]{geometry}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}

\begin{document}
\section*{TutorTrace UIST26 -- reviewer response matrix (reviews received 2026-06-11)}

\begin{longtable}{@{}p{0.6cm}p{1.0cm}p{6.2cm}p{6.2cm}p{3.2cm}p{1.6cm}p{1.6cm}@{}}
\toprule
ID & Rev. & Concern & Response & Paper change & Owner & Status \\
\midrule
\endhead
C1 & 1AC, R2, R3 & Label reliability: is $\kappa=0.71$ good enough; per-state? & Report per-state $\kappa$ (0.58--0.84), decision rules from guide v3 & Appendix B table + rules & Xiaohang & promised \\
C2 & R1, R3 & One course only (CS 3114) & Cross-course analysis on spring Python course, raw + normalized & New Sec.\ 6.4 & Minsun, David & promised \\
C3 & R2 & Telemetry privacy, prompt text release & Per-stream consent; prompts only for opt-in; derived labels for all & New Sec.\ 3.3 + datasheet & David & promised \\
C4 & R1 & 12\% dropped events in one section & Windows overlapping the gap excluded, list released & Sec.\ 3.2 sentence & David & ready \\
C5 & R3 & Relation to productive failure & Expand discussion, cite Kapur 2008, Ostrowski 2025 & Sec.\ 7 paragraph & David & ready \\
C6 & 1AC & Limitations thin & Dedicated Limitations section & New Sec.\ 8 & Yan, David & promised \\
C7 & R2 & Classifier baseline unclear & Add majority + counts-only baselines to Table 4 & Table 4 & Rezky & ready \\
C8 & R3 & Figure 5 unreadable in grayscale & Redraw with patterns & Fig.\ 5 & Yue & ready \\
C9 & R1 & Overclaiming ``novice programmers'' & Soften to studied course & Abstract, Sec.\ 1 & David & ready \\
\bottomrule
\end{longtable}

\paragraph{Character budget.} PCS box: 5,000 chars. Current draft (rebuttal.tex body, no cites): $\approx$4,850.
\end{document}
"""

# refs.bib: the Ostrowski entry is taken verbatim from shared/ostrowski2025productive.bib by the generator.
REFS_BIB_REST = r"""
@inproceedings{nakamura2025labeling,
  title     = {Labeling Learner States in Programming Sessions: A Reliability Study of Thirty-Second Windows},
  author    = {Nakamura, Ren and Feld, Sarah},
  booktitle = {Proceedings of the 2025 ACM Conference on International Computing Education Research - Volume 1},
  series    = {ICER '25},
  pages     = {233--245},
  year      = {2025}
}

@inproceedings{duarte2025beyond,
  title     = {Beyond One Course: Do Behavioral-State Classifiers Transfer Across Programming Courses?},
  author    = {Duarte, Paulo and Sim, Hye-jin},
  booktitle = {Proceedings of the 18th International Conference on Educational Data Mining},
  series    = {EDM '25},
  pages     = {141--152},
  year      = {2025}
}

@article{brennan2026what,
  title         = {What Will Students Share? Consent and Comfort with Fine-Grained Telemetry in Educational IDEs},
  author        = {Brennan, Colm and Zhou, Wei and Adler, Ruth},
  journal       = {arXiv preprint arXiv:2602.11873},
  year          = {2026}
}

@article{kapur2008productive,
  title   = {Productive Failure},
  author  = {Kapur, Manu},
  journal = {Cognition and Instruction},
  volume  = {26},
  number  = {3},
  pages   = {379--424},
  year    = {2008}
}

@article{cohen1960coefficient,
  title   = {A Coefficient of Agreement for Nominal Scales},
  author  = {Cohen, Jacob},
  journal = {Educational and Psychological Measurement},
  volume  = {20},
  number  = {1},
  pages   = {37--46},
  year    = {1960}
}
"""

# 'Copy of' project (2026-06-20): made two days after submitting, to start the camera-ready plan from the rebuttal.
# A few edits: status column updated after the lab meeting, a camera-ready TODO block, one sentence reworded.
COPY_EDITS_REBUTTAL = [
    (r"""\date{Draft: June 2026}""", r"""\date{Submitted 2026-06-18 -- copy for camera-ready planning (2026-06-20)}"""),
    (r"""We address each and list concrete changes for the camera-ready.""",
     r"""We address each and list concrete changes for the camera-ready.

% --- camera-ready plan (added 06-20, after lab meeting) ---
% \todo{C2: Minsun labels 600 windows from the spring course by 07-10; same 3 raters? check Xiaohang availability}
% \todo{C3: datasheet draft -- reuse IDETrace datasheet sections}
% \todo{C6: Limitations: Yan wants the telemetry-gap paragraph first}"""),
    (r"""We will report the result whatever it is; we expect the stalled-after-error state to transfer least
because it depends on the error channel.""",
     r"""We will report the result whatever it is. We expect stalled-after-error to transfer least, since its signature depends on
the course's error messages."""),
]
COPY_EDITS_MATRIX = [
    ('Minsun, David & promised', 'Minsun, David & in progress'),
    ('New Sec.\\ 3.3 + datasheet & David & promised', 'New Sec.\\ 3.3 + datasheet & David & in progress'),
    ('Appendix B table + rules & Xiaohang & promised', 'Appendix B table + rules & Xiaohang & done'),
    (r"""\paragraph{Character budget.} PCS box: 5,000 chars. Current draft (rebuttal.tex body, no cites): $\approx$4,850.""",
     r"""\paragraph{Submitted.} Rebuttal submitted 2026-06-18 (4,962 chars). This copy tracks camera-ready work; status column updated 2026-06-20."""),
]
