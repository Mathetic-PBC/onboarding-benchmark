"""Mathetic one-pager (Aug 2026) and the UIST 2026 TutorTrace talk (beamer with speaker notes, Sep-Oct 2026). Written by David
(synthetic). PERSON.md §7: Surplus kickoff 2026-08-11, first Marcus Oyelaran call 2026-08-20; UIST talk 2026-10-07, 15 min + 5 Q&A,
session "Learning & Tutoring", chair Tomas Reyes."""

ONEPAGER_V1 = r"""\documentclass[10pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=0.7in]{geometry}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{hyperref}
\definecolor{ink}{HTML}{1F2A44}
\definecolor{accent}{HTML}{C2410C}
\setlist{nosep,leftmargin=1.2em}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}

\begin{document}
{\color{ink}\fontsize{22}{26}\selectfont\textbf{Engelbart}}\hfill{\color{accent}\textbf{Mathetic PBC}}\\[2pt]
{\large A research notebook that remembers where your thoughts came from.}

\vspace{6pt}\hrule\vspace{6pt}

\textbf{\color{ink}The problem.} Researchers think across a dozen tools: papers in a reference manager, drafts in Overleaf and Docs,
ideas in chats with AI assistants, decisions in Slack and meetings. Notes record ideas but not their sources. Two weeks later, about a
third of a researcher's notes can no longer be traced to where they came from, and AI chats, a fast-growing source of ideas, are the
hardest to recover. When it is time to write the related work, revisit an abandoned project, or explain a decision to an advisor, the
trail is gone.

\textbf{\color{ink}What Engelbart does.}
\begin{itemize}
  \item \textbf{Imports a researcher's existing tools in one step} -- chats, files, papers, repos, notes, email and drive -- and
        groups them by project.
  \item \textbf{Keeps provenance}: every thought on the canvas links back to the chat, paper or conversation it came from.
  \item \textbf{Deduplicates without losing history}: the same paper from Zotero and Downloads becomes one entry; drafts stay as versions.
  \item \textbf{Answers ``where did this come from?''} for any claim in a draft.
\end{itemize}

\textbf{\color{ink}Why now.} AI assistants have multiplied the volume of research thinking that happens in chat. None of it is
connected to the rest of a researcher's work. Export formats are finally rich enough to import it.

\textbf{\color{ink}Who it is for.} PhD students and postdocs first (fast feedback, strong word of mouth), then research labs, then
R\&D teams in industry.

\textbf{\color{ink}Traction.} Working canvas prototype; import from 10+ sources; pilot onboarding sessions with researchers at
UC Berkeley and CMU scheduled for October 2026.

\textbf{\color{ink}Team.} \textbf{David Barron} (CEO) -- HCI PhD student at Virginia Tech (on leave), first-author work on learning
analytics datasets at UIST and NeurIPS D\&B. \textbf{Hudson Mitchell-Pullman} (co-founder) -- product, design and go-to-market.
Based at the Surplus incubator, San Francisco.

\textbf{\color{ink}Public benefit.} Mathetic is a Delaware public benefit corporation. Our purpose: to help people learn and think
more clearly by keeping the record of how their ideas formed in their own hands.

\textbf{\color{ink}The ask.} Raising a pre-seed round on a SAFE to fund 12 months of product work and pilots.

\vfill
{\small David Barron \& Hudson Mitchell-Pullman \quad\textbullet\quad Surplus, San Francisco \quad\textbullet\quad August 2026}
\end{document}
"""

# later edits (before the 08-20 investor call): retention line, 'who pays' answer
ONEPAGER_EDITS = [
    (r"""\textbf{\color{ink}Who it is for.} PhD students and postdocs first (fast feedback, strong word of mouth), then research labs, then
R\&D teams in industry.""",
     r"""\textbf{\color{ink}Who it is for, and who pays.} PhD students and postdocs first (fast feedback, strong word of mouth), then
research labs, then R\&D teams in industry. Individuals pay a monthly subscription; labs pay per seat with shared projects. Retention
target for pilots: weekly use in 6 of the first 8 weeks."""),
]

ONEPAGER_README = """Mathetic one-pager
- onepager.tex -> 1 page, compile with pdfLaTeX
- keep it to ONE page. if it spills, cut the "why now" para first
- numbers: "about a third" = Halvorsen & Quist 2025 (31% of notes untraceable after 2 weeks). don't put the citation on the page
- v for Marcus call 08-20; Lena (Surplus) asked for a copy too
"""

TALK = r"""\documentclass[aspectratio=169]{beamer}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{booktabs}
\usetheme{default}
\usecolortheme{dove}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[frame number]
% speaker notes: compile with \setbeameroption{show notes on second screen=right} for the presenter view
%\setbeameroption{show notes on second screen=right}

\title{TutorTrace: Classifying Learner States in AI-Assisted Programming}
\subtitle{UIST 2026 -- Session ``Learning \& Tutoring''}
\author{David Barron}
\institute{PRIME Lab, Virginia Tech \\ joint work with Minsun, Xiaohang, Rezky, Yue and Yan Chen}
\date{October 7, 2026}

\begin{document}

\begin{frame}
  \titlepage
\end{frame}
\note{Thanks Tom\'as. Hi everyone, I'm David. This is work from the PRIME Lab at Virginia Tech with Minsun, Xiaohang, Rezky, Yue and
my advisor Yan Chen. (15 min, aim for 13:30 so there is slack.)}

\begin{frame}{A student, 14 minutes into a lab}
  \begin{itemize}
    \item Runs the code. \texttt{IndexError}.
    \item Asks the assistant. Pastes the fix. Runs. \texttt{IndexError}.
    \item Asks again, same words, plus ``still''.
    \item Stops typing for four minutes.
  \end{itemize}
  \vspace{1em}
  \textbf{Is this student learning, or stuck?}
\end{frame}
\note{Open with the replay. Play the 20-second clip from the deployment (consented student, section A). Pause on the idle gap.
The point: from the final code you cannot tell this happened.}

\begin{frame}{Instructors can't see the process}
  \begin{itemize}
    \item Autograders see submissions, not sessions
    \item Assistants see prompts, not what happens in the editor
    \item TAs see the 5 students who raise their hands
  \end{itemize}
\end{frame}
\note{Three partial views. Nobody sees the whole session. That's the gap TutorTrace fills.}

\begin{frame}{TutorTrace}
  \begin{itemize}
    \item \textbf{Dataset}: replayable sessions combining editor events, runs and assistant prompts
    \item \textbf{Taxonomy}: six learner states, labeled in 30-second windows
    \item \textbf{Classifier}: predicts states from telemetry
  \end{itemize}
\end{frame}
\note{Three contributions. I'll spend most time on the taxonomy because that's what people ask about.}

\begin{frame}{Data: a live CS2 deployment}
  \begin{itemize}
    \item CS 3114, Fall 2025: 87 students, 2 lab sections, 3 TAs
    \item Instrumented editor + assistant panel, per-stream consent
    \item 2,340 thirty-second windows labeled by 3 raters
    \item One section lost events to a reconnect bug -- windows excluded, list released
  \end{itemize}
\end{frame}
\note{Be upfront about the dropped events, a reviewer asked. Hotfix went in during the lab. ~12 percent of section B events, before 4:10 pm.}

\begin{frame}{Six states}
  \begin{columns}
    \column{0.5\textwidth}
    \begin{itemize}
      \item Productive progress
      \item Exploratory tinkering
      \item \textbf{Stalled after error}
    \end{itemize}
    \column{0.5\textwidth}
    \begin{itemize}
      \item Assistant help-seeking
      \item Verifying (run \& inspect)
      \item Disengaged
    \end{itemize}
  \end{columns}
  \vspace{1em}
  Stalled-after-error was added in labeling guide v3.
\end{frame}
\note{Explain why stalled-after-error is separate from tinkering: no successful run in 3 min and reverted edits. This is the
boundary raters disagreed on most before v3.}

\begin{frame}{Reliability}
  \centering
  \begin{tabular}{lr}
    \toprule
    & Fleiss' $\kappa$ \\
    \midrule
    Overall (3 raters, 2,340 windows) & 0.71 \\
    Assistant help-seeking & 0.84 \\
    Tinkering vs.\ stalled-after-error & 0.58 \\
    \bottomrule
  \end{tabular}
\end{frame}
\note{Per-state numbers were a rebuttal promise, now in the appendix. Say: help-seeking is easy because it's an observable event;
tinkering vs stalled is a judgment.}

\begin{frame}{What predicts stalling}
  \begin{itemize}
    \item Repeated near-identical prompts to the assistant
    \item Long idle gap after a failed run
    \item Reverting the assistant's change
  \end{itemize}
  \vspace{0.5em}
  Consistent with Ostrowski et al., L@S 2025.
\end{frame}
\note{Mention Ostrowski et al. found the repeated-prompt signal too, with a different scheme. Nice convergence, don't oversell.}

\begin{frame}{Classifier}
  \begin{itemize}
    \item Gradient boosting over keystroke, run and prompt features
    \item Splits grouped by student
    \item Macro-F1 0.78 in-course
  \end{itemize}
\end{frame}
\note{Emphasize grouped splits -- after what happened with IDETrace I'm careful about this. (Don't actually say that.)}

\begin{frame}{Does it transfer? Cross-course analysis}
  \begin{itemize}
    \item Second course: intro Python, Spring 2026
    \item Train on CS 3114, test on the second course
    \item Macro-F1 0.64 raw, 0.69 with per-course normalization
    \item Stalled-after-error transfers worst: it depends on the error channel
  \end{itemize}
\end{frame}
\note{This analysis was promised in the rebuttal and is in the camera-ready, Section 6.4. Good place to slow down.}

\begin{frame}{Design implications}
  \begin{itemize}
    \item Flags as prompts for a human check-in, not automatic interventions
    \item Replay as a second stage for flagged sessions
    \item Consent per data stream; prompts are the most sensitive
  \end{itemize}
\end{frame}
\note{Tie back to the student from slide 2: the right response was a TA walking over, not another code block.}

\begin{frame}{Limitations}
  \begin{itemize}
    \item Two courses, one institution
    \item Labels are judgments, even at $\kappa = 0.71$
    \item States depend on the assistant students used
  \end{itemize}
\end{frame}
\note{Keep this short but don't skip it.}

\begin{frame}{Thank you}
  \centering
  \Large Dataset, labeling guide and replay viewer: \\[0.5em]
  \normalsize (link on the paper page) \\[1.5em]
  David Barron \quad dbarron410@vt.edu
\end{frame}
\note{Questions. Likely: (1) privacy -- per-stream consent, prompts only for opt-in; (2) why 30 s windows -- reliability peaks there;
(3) would this work with a different assistant -- honestly unknown.}

\end{document}
"""

# edits over the talk's life: first full draft 09-22, AV check with Tomas 10-02, final 10-06
TALK_DRAFT_EDITS = [  # applied in reverse to get the 09-22 draft from the final
    ('Macro-F1 0.64 raw, 0.69 with per-course normalization', 'Macro-F1 ?? raw, ?? normalized (numbers from Minsun)'),
    ("""\\note{Thanks Tom\\'as. Hi everyone,""", """\\note{Thank the chair. Hi everyone,"""),
]

TALK_README = """UIST26 talk -- TutorTrace
- 15 min + 5 Q&A, session "Learning & Tutoring", Wed Oct 7
- chair: Tomas Reyes. AV check on Zoom Oct 2 -- HDMI + USB-C both fine, 16:9, presenter view works with notes on second screen
- export: compile, then File > Download PDF; for the presenter view uncomment \\setbeameroption line
- timing run 10-05: 14:10. cut 10 s from the data slide
"""
