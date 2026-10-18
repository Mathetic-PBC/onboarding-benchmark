"""Synthetic Obsidian vault 'research-vault' (PERSON.md: reading group notes on Bush/Licklider/Engelbart, Ostrowski 2025
literature note, Engelbart import-dedupe thoughts, IDETrace leakage, bursty daily notes). One item per file."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('obsidian')
V = 'research-vault'
ACCT = 'vault "research-vault" (~/Documents/research-vault)'
MOD = 'authentic/obsidian vault layout (.obsidian config + markdown notes with YAML frontmatter)'

RG = 'project_augmenting_cognition_reading_group'
ENG = 'project_engelbart'


def note(rel, body, created, modified=None, projects=('project_none',), notes=''):
    g.text(f'{V}/{rel}', body.lstrip('\n'), created, modified, account=ACCT, project_ids=list(projects), modeled_on=MOD, notes=notes)


# ---------------- vault config ----------------
CFG_C, CFG_M = '2026-01-14 21:40', '2026-08-05 22:13'
g.text(f'{V}/.obsidian/app.json', json.dumps({
    "alwaysUpdateLinks": True, "newFileLocation": "folder", "newFileFolderPath": "Inbox", "attachmentFolderPath": "Attachments",
    "showLineNumber": False, "readableLineLength": True, "promptDelete": False, "useMarkdownLinks": False,
    "newLinkFormat": "shortest", "vimMode": False}, indent=2), CFG_C, CFG_M, account=ACCT, project_ids=['project_none'],
    modeled_on='authentic/obsidian .obsidian/app.json shape', notes='vault config')
g.text(f'{V}/.obsidian/appearance.json', json.dumps({
    "accentColor": "#7c6cf0", "theme": "obsidian", "baseFontSize": 15, "interfaceFontFamily": "", "textFontFamily": "iA Writer Quattro S",
    "monospaceFontFamily": "JetBrains Mono", "showViewHeader": True}, indent=2), CFG_C, '2026-02-02 00:31', account=ACCT,
    project_ids=['project_none'], modeled_on='authentic/obsidian .obsidian/appearance.json shape', notes='vault config')
g.text(f'{V}/.obsidian/core-plugins.json', json.dumps({
    "file-explorer": True, "global-search": True, "switcher": True, "graph": True, "backlink": True, "canvas": False,
    "outgoing-link": True, "tag-pane": True, "properties": True, "page-preview": True, "daily-notes": True, "templates": True,
    "note-composer": False, "command-palette": True, "slash-command": False, "editor-status": True, "bookmarks": True,
    "markdown-importer": False, "zk-prefixer": False, "random-note": False, "outline": True, "word-count": True, "slides": False,
    "audio-recorder": False, "workspaces": False, "file-recovery": True, "publish": False, "sync": False, "bases": False,
    "webviewer": False}, indent=2), CFG_C, CFG_M, account=ACCT, project_ids=['project_none'],
    modeled_on='authentic/obsidian .obsidian/core-plugins.json shape', notes='vault config')

# ---------------- templates + home ----------------
note('Templates/Daily.md', '''
---
tags: [daily]
created: {{date:YYYY-MM-DD}}
---
# {{date:dddd, MMMM D}}

## doing
-

## thinking about
-

## links
-
''', '2026-01-14 21:52', '2026-01-14 21:58', notes='template note (no project content)')

note('Templates/Literature.md', '''
---
tags: [lit]
author:
year:
venue:
read:
status: to-read
---
# {{title}}

**one-line claim:**

## what they argue

## what I actually think

## connections
-

## quotes (keep short, cite page)
-
''', '2026-01-14 22:05', '2026-01-27 23:40', notes='template note (no project content)')

note('Home.md', '''
---
tags: [moc]
created: 2026-01-14
---
# research-vault

Started this because the lab notes repo is great for meeting minutes but terrible for "what did I think about this paper
three weeks ago". Rule: one note per paper in `Literature/`, one note per day in `Daily/`, anything half-formed goes to `Inbox/`.

## reading group (augmenting cognition)
Thursday 5pm, PRIME Lab room / Zoom when people are away. Rotation in [[Reading group - schedule]].
- [[Bush1945 - As We May Think]]
- [[Licklider1960 - Man-Computer Symbiosis]]
- [[Engelbart1962 - Augmenting Human Intellect]]
- [[Nelson1965 - A File Structure for the Complex]]
- [[Kay1977 - Personal Dynamic Media]]
- [[Papert1980 - Mindstorms]]

## research
- TutorTrace / UIST: [[Ostrowski2025 - Productive Struggle]], [[Kapur2008 - Productive Failure]], [[TutorTrace - talk Q&A prep]]
- IDETrace / NeurIPS D&B: [[IDETrace - leakage]]

## engelbart (the product, not the person)
- [[Engelbart - where did this thought come from]]
- [[Engelbart - import dedupe]]

## inbox
- [[Untitled]]
''', '2026-01-14 22:10', '2026-09-22 23:20', projects=[RG, ENG, 'project_tutortrace', 'project_idetrace'],
     notes='vault index / map-of-content linking reading-group, research and Engelbart notes')

# ---------------- literature ----------------
note('Literature/Bush1945 - As We May Think.md', '''
---
tags: [lit, reading-group, memex]
author: Vannevar Bush
year: 1945
venue: The Atlantic Monthly (July 1945)
read: 2026-01-15
status: read
---
# Bush 1945, As We May Think

**one-line claim:** the bottleneck of science is no longer producing records but finding and following them, so build a
machine that stores a person's records and lets them tie items together the way the mind associates.

## what he argues
- written right after the war, addressed to scientists who had been building weapons: what should they build now?
- the scientific record has outgrown our ability to consult it; indexing by alphabet/hierarchy is the wrong model because the
  mind works by association
- proposes the **memex**: a desk with microfilm storage, a scanner for adding your own notes and photos, and two viewing
  screens side by side
- the key primitive is the **trail**: you join two items, then keep joining, and the trail can be named, replayed, and
  copied to a friend
- imagines a new profession of "trail blazers" who make useful trails through the record for others

## what I actually think
- the hardware is pure 1945 (microfilm, dry photography, a head-mounted camera) but the trail is still not solved. browser
  history is a trail nobody can read; a Zotero collection is a pile, not a path
- he cares about the trail being **shareable** with the reasoning intact. that is the part every PKM tool drops. you can
  share a doc but not "how I got here"
- the trail is *authored after the fact* in his telling (you tie items while consulting). he doesn't assume it records itself.
  for us that's a real design question: automatic provenance vs. curated trails

## connections
- [[Engelbart1962 - Augmenting Human Intellect]] cites Bush directly; Engelbart says this essay set him off
- [[Engelbart - where did this thought come from]] is basically "make the trail a first-class object"
- group discussion (01-15): Rezky pushed back that most of what Bush wanted is just a search engine. I disagree: search
  gives you the item, not the path between two items

## quotes (short)
- "the trail" is the unit, not the document (my paraphrase, his framing ~p.6)
''', '2026-01-13 23:20', '2026-01-16 00:41', projects=[RG], notes='own summary; no long quotes')

note('Literature/Licklider1960 - Man-Computer Symbiosis.md', '''
---
tags: [lit, reading-group]
author: J. C. R. Licklider
year: 1960
venue: IRE Transactions on Human Factors in Electronics, HFE-1
read: 2026-01-22
status: read
---
# Licklider 1960, Man-Computer Symbiosis

**one-line claim:** the near-term goal is not machines that think on their own but tight, real-time partnership where humans
set goals and evaluate, and the machine does the routinizable work that clears the way to insight.

## what he argues
- distinguishes "mechanically extended man" (tools) and full AI from **symbiosis**: two dissimilar partners, each doing what
  it is good at, in close coupling
- the famous self-study: he logged his own working time and found most of it went to *getting into a position to think*
  (finding, plotting, converting), not thinking. roughly 85% by his estimate
- prerequisites he lists: time-sharing, memory hardware, memory organization (retrieve by content, not by address),
  natural-ish language between human and machine, displays and pen input, speech recognition
- humans: set goals, formulate hypotheses, handle the unanticipated. machines: transform data, remember, compute

## what I actually think
- the 85% stat is the whole pitch deck for a research notebook. I should actually redo the measurement on myself for one
  week (see [[Untitled]] in inbox, that was me starting to do it)
- "retrieve by content not address" in 1960 is wild. the import problem in Engelbart is the same issue one level up: the
  user remembers *what it was about*, not which app it was in
- he is weirdly optimistic about timelines (thinks the symbiotic period could last 10–15 years before machines dominate).
  group had fun with that given LLMs

## connections
- [[Engelbart1962 - Augmenting Human Intellect]] is the operational version of this
- [[Bush1945 - As We May Think]] is the storage side; Licklider adds the interaction loop
- Yue brought up that the TA-in-the-loop framing in our lab work is basically symbiosis at classroom scale
''', '2026-01-21 22:15', '2026-01-23 01:02', projects=[RG], notes='own summary; no long quotes')

note('Literature/Engelbart1962 - Augmenting Human Intellect.md', '''
---
tags: [lit, reading-group, engelbart]
author: Douglas C. Engelbart
year: 1962
venue: SRI Summary Report AFOSR-3223 ("Augmenting Human Intellect: A Conceptual Framework")
read: 2026-01-29
status: read (sections I–III fully, IV skimmed)
---
# Engelbart 1962, Augmenting Human Intellect: A Conceptual Framework

**one-line claim:** human capability comes from a whole system (the person plus language, artifacts, methodology and training),
so you can augment intellect by co-evolving the tools *and* the ways of working, not just by building faster machines.

## what he argues
- **H-LAM/T**: Human using Language, Artifacts, Methodology, in which he is Trained. the augmentation means are the LAM/T part
- capability is hierarchical: big processes ("write a report") decompose into smaller ones down to motor skills; improving a
  low-level process can ripple up and change what high-level work is even possible
- the pencil-tied-to-a-brick thought experiment: make writing slower and clumsier and you change how people think, not only
  how fast they write. so the reverse should hold
- the long "Joe" walkthrough (section IV): a fictional user shows off structured text, linking, views that rearrange the same
  statements, and symbol-structuring that changes the user's concept-structuring
- **bootstrapping**: the people who build augmentation tools should use them on their own work first, so improvements compound

## what I actually think
- H-LAM/T is the best frame I've found for why "just add an LLM" products feel shallow: they change the A and ignore the M and T
- the hierarchical-process point matters for import: if the low-level process "find where I read that" gets 10x cheaper, the
  high-level process "write related work" changes shape. that's the product thesis in one line
- bootstrapping = dogfooding but stricter. we should be doing all Mathetic research *inside* Engelbart. we're not yet
- section IV is long and dated but the "same statements, different views" idea is exactly what the canvas does with topics

## connections
- named the product after him for a reason; see [[Engelbart - where did this thought come from]]
- builds directly on [[Bush1945 - As We May Think]] and is in conversation with [[Licklider1960 - Man-Computer Symbiosis]]
- [[Kay1977 - Personal Dynamic Media]] picks up the "medium for thought" thread a generation later
''', '2026-01-27 23:05', '2026-02-01 00:20', projects=[RG, ENG], notes='own summary; no long quotes; ties reading group to the product name')

note('Literature/Nelson1965 - A File Structure for the Complex.md', '''
---
tags: [lit, reading-group, hypertext]
author: Theodor H. Nelson
year: 1965
venue: ACM '65 National Conference ("A File Structure for the Complex, the Changing and the Indeterminate")
read: 2026-02-12
status: read
---
# Nelson 1965, A File Structure for the Complex, the Changing and the Indeterminate

**one-line claim:** writers and researchers need a file system that keeps every version and every link between pieces, because
their material is complex, keeps changing, and its final structure is unknown while they work.

## what he argues
- introduces the **ELF** (evolutionary list file): entries, lists of entries, and links between them, all versioned
- coins "hypertext" (and "hyperfilm") here, as text that branches and can't be printed conveniently
- the user is a writer rearranging notes, keeping drafts, and comparing alternatives; the system should never throw away a prior
  arrangement
- argues the file structure itself, not clever retrieval, is the thing to get right

## what I actually think
- "the changing and the indeterminate" is a good description of a PhD student's material. half my notes are about a paper that
  doesn't exist yet
- his insistence on keeping versions is relevant for dedupe: two near-identical drafts are *not* duplicates to a writer, they're
  history. we should merge display, not delete ([[Engelbart - import dedupe]])
- less vision about collaboration than Bush or Engelbart; very single-author

## connections
- [[Bush1945 - As We May Think]] (Nelson credits the memex)
''', '2026-02-11 22:40', '2026-02-13 00:15', projects=[RG, ENG], notes='own summary; ties versioning to Engelbart import dedupe')

note('Literature/Kay1977 - Personal Dynamic Media.md', '''
---
tags: [lit, reading-group]
author: Alan Kay, Adele Goldberg
year: 1977
venue: IEEE Computer 10(3)
read: 2026-02-26
status: read
---
# Kay & Goldberg 1977, Personal Dynamic Media

**one-line claim:** a personal computer should be a medium people (including children) can shape for their own purposes, the
Dynabook, and Smalltalk experiments at PARC show non-programmers can build real tools in it.

## what they argue
- the computer as a *metamedium*: it can simulate other media and also media that can't exist physically
- describes the interim Dynabook (Alto + Smalltalk) and what kids and adults built with it: animation, music, drawing tools,
  a hospital simulation
- the user should be able to reach in and change the tool, not just use it

## what I actually think
- "metamedium" is a better word than "app" for what a research notebook should be
- the kids section is the part the group liked most. connects to Papert (the Papert Lab name came from this thread)
- skeptical note: most users don't want to reach in and change the tool. they want defaults that already fit

## connections
- [[Papert1980 - Mindstorms]]
- [[Engelbart1962 - Augmenting Human Intellect]]
''', '2026-02-25 23:10', '2026-02-27 00:05', projects=[RG])

note('Literature/Papert1980 - Mindstorms.md', '''
---
tags: [lit, reading-group, learning]
author: Seymour Papert
year: 1980
venue: Basic Books ("Mindstorms: Children, Computers, and Powerful Ideas")
read: 2026-01-08 (reread for group 2026-03-05)
status: read
---
# Papert 1980, Mindstorms

**one-line claim:** children learn deeply when they build things with computers (the Logo turtle) that let them think about
their own thinking; the computer should be an object to think with, not a drill machine.

## what he argues
- "objects to think with": the turtle connects body knowledge (walking a circle) to formal math
- the word **mathetic** (about learning, as opposed to didactic, about teaching). the whole company name is from this chapter
- debugging as a mindset: errors are information, not failure. learners who debug learn more than those who get it right
- critique of computer-aided instruction where the computer programs the child

## what I actually think
- the debugging-as-learning point is half of TutorTrace in one sentence: stalled-after-error vs productive struggle is exactly
  whether the error became information
- also the reason I'm suspicious of hints that arrive too early. a hint during productive struggle steals the debugging
- for the company: Papert Lab was the working name, Mathetic stuck. keep the "learning, not teaching" stance in product copy

## connections
- [[Kapur2008 - Productive Failure]]
- [[Ostrowski2025 - Productive Struggle]]
- [[Kay1977 - Personal Dynamic Media]]
''', '2026-01-08 22:30', '2026-03-06 00:48', projects=[RG, 'project_mathetic_company', 'project_tutortrace'],
     notes='reading-group note that also explains the Mathetic/Papert Lab name and links to TutorTrace')

note('Literature/Kapur2008 - Productive Failure.md', '''
---
tags: [lit, tutortrace, related-work]
author: Manu Kapur
year: 2008
venue: Cognition and Instruction 26(3)
read: 2026-03-24
status: read (for UIST related work)
---
# Kapur 2008, Productive Failure

**one-line claim:** students who struggle and fail on complex, ill-structured problems before instruction can end up with
better transfer than students who get well-structured support from the start.

## what matters for us
- the design: ill-structured vs well-structured problem groups, then a common test. ill-structured groups did worse in the
  moment and better on the later well-structured and ill-structured tests
- the struggle has to be with something *generative*: students have to produce and compare solutions, not just be stuck
- this is the citation reviewers expect when we say "productive struggle". also the counterweight: not all struggle is
  productive, which is literally our label set

## how I'm using it
- intro para 2 of the TutorTrace paper: struggle can be good, so a tool that flags all struggle as a problem is wrong
- labeling guide v3 "stalled-after-error" maps to the *unproductive* side (no generation, repeated near-identical attempts)

## connections
- [[Ostrowski2025 - Productive Struggle]] (they cite this too, ref 1)
- [[Papert1980 - Mindstorms]] debugging-as-learning
''', '2026-03-24 23:55', '2026-03-25 01:10', projects=['project_tutortrace'])

note('Literature/Ostrowski2025 - Productive Struggle.md', '''
---
tags: [lit, tutortrace, reading-group, telemetry]
author: Hannah Ostrowski, Mateo Lindqvist, Aisha Bello, Ravi Chandrasekar
year: 2025
venue: L@S '25 (arXiv 2507.01842 first)
citekey: ostrowski2025productive
read: 2026-02-09
status: read twice (arXiv v1 in Feb, camera-ready in Mar)
---
# Ostrowski et al. 2025, Productive Struggle or Silent Stalling? Telemetry Signals of Help-Seeking in LLM-Assisted CS1

**one-line claim:** editor + assistant telemetry can separate productive struggle from stalling in CS1 reasonably well, with
repeated near-identical prompts and idle gaps after errors as the strongest stalling signals.

## setup
- intro Python course, N=212, two sections, browser IDE logging edits/runs/tests/assistant prompts
- 30-second windows (same as ours!), 4 TAs, labels: productive struggle / stalling / help-seeking / off-task
- 1,904 labeled windows. kappa on 10% overlap: 0.62 in arXiv v1, **0.64 in camera-ready**
- gradient-boosted classifier: macro-F1 0.69 (v1) → **0.71** (camera-ready)

## findings I care about
- stalling ← prompts that are nearly the same as the previous one (edit distance under ~15%), and long idle after a failed run
- productive struggle ← many small edits, frequent test runs
- they report a lower number when same-student windows can't leak across folds. good practice
- (07-25 addendum) we did NOT do this in IDETrace and it bit us, see [[IDETrace - leakage]]
- discussion: hints offered *during* productive struggle were rated less helpful in their follow-up survey

## where we differ (for the UIST related-work paragraph)
- our label set adds "stalled-after-error" as its own state (labeling guide v3), they fold it into stalling
- we have 2,340 windows from the VizPI CS 3114 deployment, 3 raters, kappa 0.71
- they have one course and one assistant; so do we, honestly. reviewers will hit both of us on generalization

## careful
- I have this paper in like four places (Zotero, Downloads, the papers folder, the Overleaf .bib). the v1 and the camera-ready
  have different numbers. **cite the camera-ready (0.71 / 0.64)**, not the arXiv numbers
- for the reading group: good example of a "trail" problem. two versions of the same paper, and which one I read determines
  which number ends up in my draft

## connections
- [[Kapur2008 - Productive Failure]]
- [[Papert1980 - Mindstorms]]
- [[TutorTrace - talk Q&A prep]]
- [[Engelbart - import dedupe]] (the same-paper-in-several-places case)
''', '2026-02-09 23:30', '2026-07-25 01:05', projects=['project_tutortrace', RG],
     notes='literature note on the fictional Ostrowski et al. 2025 paper (same-paper-in-several-places story); v1 vs camera-ready numbers')

# ---------------- projects ----------------
note('Projects/Reading group - schedule.md', '''
---
tags: [reading-group, admin]
created: 2026-01-14
---
# Reading group: schedule

Thursdays 5:00–6:15pm ET. ~25 pages max per week or people stop reading. Presenter brings 3 questions, not a summary.

| date | reading | presenter | notes |
|---|---|---|---|
| 01-15 | Bush 1945 | David | [[Bush1945 - As We May Think]] |
| 01-22 | Licklider 1960 | Yue | [[Licklider1960 - Man-Computer Symbiosis]] |
| 01-29 | Engelbart 1962 §I–III | David | [[Engelbart1962 - Augmenting Human Intellect]] |
| 02-05 | Engelbart 1962 §IV (Joe) | Rezky | skimmed, everyone hated the length |
| 02-12 | Nelson 1965 | Xiaohang | [[Nelson1965 - A File Structure for the Complex]] |
| 02-19 | — | — | cancelled, nobody around |
| 02-26 | Kay & Goldberg 1977 | Minsun | [[Kay1977 - Personal Dynamic Media]] |
| 03-05 | Papert 1980 ch. 1 + 5 | David | [[Papert1980 - Mindstorms]] |
| 03-12 | Ostrowski et al. 2025 | David | modern one, telemetry. [[Ostrowski2025 - Productive Struggle]] |
| 03-19 → 04-09 | paused | | UIST crunch + after |
| 04-16 | Engelbart & English 1968 (the demo, watch first 30 min) | Yue | |

## after April
- group went every-other-week in May, then stopped when I left for SF. Hudson wants to restart it remotely as a Mathetic
  thing: same readings, plus whoever from the Berkeley chats wants to join
- candidates for the restart: Hutchins *Cognition in the Wild* ch. 9, Victor *Magic Ink*, Matuschak & Nielsen on mnemonic media
''', '2026-01-14 22:20', '2026-09-02 23:44', projects=[RG])

note('Projects/Engelbart - where did this thought come from.md', '''
---
tags: [engelbart, product, provenance]
created: 2026-08-13
---
# Engelbart: "where did this thought come from"

The one-sentence product: a research notebook that remembers where your thoughts came from.

## what a "trail" is for us
A trail is the chain from a note back to its sources: the chat where I first said it, the paper that made me think it, the
meeting where Yan pushed back. Bush's trail ([[Bush1945 - As We May Think]]) was hand-made; ours has to be mostly automatic,
because nobody curates.

## minimum viable trail
1. every imported item keeps: source tool, original id/path, created time, and the account it came from
2. every note can point at items ("came from") with a span if we have it
3. the canvas shows the trail as a thin line from the note to its sources, collapsed by default
4. two items that are the same thing (same paper from Zotero and Downloads) show up as **one** node with two origins, not two
   nodes. see [[Engelbart - import dedupe]]

## open questions
- time: is the trail "where the idea came from" or "where I first wrote it down"? those differ a lot for me (ideas show up in
  a run, get written in Apple Notes, get argued in Claude)
- privacy: trails into personal stuff (a meal-prep chat that happens to contain a research idea) need to be visible to me
  but not exported with a shared topic
- how much should the trail survive editing? if I rewrite a note completely, is the trail still true?

## H-LAM/T framing for the deck
- Artifacts = the canvas + import. Methodology = topics/goals. Training = the onboarding. we only built A so far
- ([[Engelbart1962 - Augmenting Human Intellect]])
''', '2026-08-13 22:50', '2026-09-14 00:30', projects=[ENG, RG])

note('Projects/Engelbart - import dedupe.md', '''
---
tags: [engelbart, import, dedupe]
created: 2026-09-08
updated: 2026-10-15
---
# Engelbart: import dedupe

## the problem (from pilots)
- Priya's onboarding (10-09): same paper showed up twice, once from Zotero and once from ~/Downloads. she thought we were
  broken. also her Claude import missed ~140 chats
- Daniel's onboarding (10-13): no Notion/Granola importer at all, so nothing to dedupe there, but he asked why "Other" had
  both a PDF and the same PDF inside a zip
- my own test account: the Ostrowski paper appears as arXiv v1 PDF, camera-ready PDF, a .bib entry, a Slack file share, a Gmail
  attachment ([[Ostrowski2025 - Productive Struggle]])

## kinds of "duplicate"
| kind | example | what to do |
|---|---|---|
| byte-identical | same PDF in Downloads and ~/Desktop/papers | merge into one node, list both locations |
| same work, different version | arXiv v1 vs camera-ready | one *work* node, two *version* children, newest preferred for citing |
| same content, different container | PDF vs PDF inside a zip, email attachment | merge, keep the container as an origin |
| exported twice | Notion `.csv` and `_all.csv`, Evernote single note + notebook export | merge silently, but count both for "did we import everything" |
| near-duplicate drafts | doc v2, "copy of" | **don't merge**. Nelson was right, drafts are history ([[Nelson1965 - A File Structure for the Complex]]). group under one title |

## matching ladder (cheap → expensive)
1. sha256 of bytes
2. DOI / arXiv id from PDF metadata or first page text
3. normalized title + first author + year (lowercase, strip punctuation and LaTeX braces)
4. MinHash over text shingles, threshold ~0.9, for things without identifiers
5. only then ask the LLM, and only for borderline pairs, with both snippets shown

## things that bit us
- titles with `{LLM}` braces from BibTeX didn't match PDF titles until we stripped braces
- the zip case: we were hashing the zip, not its members
- Apple Notes exports truncate long titles with an ellipsis, so title matching against the same note elsewhere fails. use body
- recall is the thing pilots notice first. a missed item is worse than a duplicate. don't let dedupe eat real items

## todo
- [ ] write the version-children UI on the canvas (Hudson has a sketch)
- [x] log every merge decision with the reason so we can audit it
- [ ] benchmark: build a fake person with stuff spread across ~30 tools and measure omissions / wrong items / duplicates
''', '2026-09-08 23:15', '2026-10-15 23:58', projects=[ENG])

note('Projects/IDETrace - leakage.md', '''
---
tags: [idetrace, neurips, bug]
created: 2026-07-24
updated: 2026-07-30
---
# IDETrace: the leakage bug

## what happened
- 07-24, while answering reviewer 2's "why is your baseline so strong" I re-ran the split script and printed student ids per
  fold. **same student ids in train and test.** windows were split randomly, so a student's 30-second windows from the same
  session landed on both sides
- the model was partly learning the student (typing rhythm, variable names), not the state

## fix
- split grouped by student id (`GroupKFold`, 5 folds, groups=student_id), stratification checked by hand afterward
- re-ran everything: baselines, the main model, the ablations. took two nights on the lab box
- macro-F1 **0.81 → 0.74**. per-class: stalled-after-error took the biggest hit, off-task barely moved
- the gap between the two numbers is itself evidence that student identity leaks through telemetry. that's actually a finding
  for the privacy paragraph

## rebuttal wording (posted 07-29)
- report both numbers, say plainly that the original split leaked, thank the reviewer for the question that made us look
- updated table goes in the revision; dataset card gets a "recommended splits" section with the grouped split as the only
  official one
- Yan's edit: lead with the corrected number, not the old one

## lessons
- [[Ostrowski2025 - Productive Struggle]] already reported a no-leak number. we read that paper and still did it
- add a test: assert no group overlap across folds. it's three lines
- full notebook with plots is in OneNote (IDETrace notebook), this is the summary
''', '2026-07-24 23:40', '2026-07-30 01:15', projects=['project_idetrace'])

note('Projects/TutorTrace - talk Q&A prep.md', '''
---
tags: [tutortrace, uist, talk]
created: 2026-09-22
updated: 2026-10-06
---
# TutorTrace: talk Q&A prep

UIST 2026, session "Learning & Tutoring", chair Tomás Reyes. 15 min + 5 Q&A. Tuesday 10-07.

## likely questions and short answers
1. **"kappa 0.71 with 3 raters, is that good enough?"** substantial agreement; the disagreements cluster at the
   struggle/stall boundary, which is exactly the hard part. show the confusion slide (backup 3)
2. **"does this generalize beyond one course?"** rebuttal promised the cross-course analysis; it's in the camera-ready
   section 7. say what changed and what didn't (help-seeking transfers, off-task doesn't)
3. **"privacy of telemetry?"** students consented; we don't keep keystroke content beyond the session; the IDETrace leakage
   finding shows identity leaks through timing, so we treat it as identifying data
4. **"how is this different from Ostrowski et al.?"** stalled-after-error as its own state, replay-based labeling, and the TA
   view. cite camera-ready numbers only ([[Ostrowski2025 - Productive Struggle]])
5. **"would you intervene automatically?"** no. flags go to a TA, who decides. Papert-ish answer: the error is information

## timing
- intro + problem 3:00, system 4:00, labeling study 3:30, results 3:00, implications 1:30
- practiced 10-04 with Hudson on Zoom: 16:40. cut the second demo video
''', '2026-09-22 23:05', '2026-10-06 22:40', projects=['project_tutortrace'])

# ---------------- inbox ----------------
note('Inbox/Untitled.md', '''
licklider redo for one week:
- mon: 3h "thinking", 5h finding stuff / setting up
- tue: forgot to log

where did the 5h go. zotero search, scrolling slack for the link yan sent, re-finding the claude chat about hdbscan params

trail = path not pile
''', '2026-02-02 23:51', '2026-02-04 00:10', projects=[RG],
     notes='HARD CASE: vague title — "Untitled" inbox note; content is a reading-group follow-up (redoing Licklider\'s time study)')

note('Inbox/caro-kann lines.md', '''
---
tags: [chess]
---
- 1.e4 c6 2.d4 d5 3.e5 Bf5 (advance). stop playing 4.Nf3 on autopilot vs me, people go 4.h4 and I panic
- vs 3.Nc3 dxe4 4.Nxe4 Bf5 5.Ng3 Bg6 6.h4 h6 7.Nf3 Nd7: learn this to move 10, it's 40% of my games
- two knights (2.Nc3 d5 3.Nf3): Bg4 line, fine
- lichess study: "caro main lines" (mine), do 10 min a day of the drill instead of 3+0 blitz
''', '2026-04-12 22:30', '2026-04-14 23:05', notes='personal clutter: chess (PERSON.md §5)')

# ---------------- daily notes ----------------
D = []
D.append(('2026-01-14', '22:00', '23:30', [RG], '''
# Wednesday, January 14

## doing
- made this vault. obsidian over notion for reading notes because it's files and I can grep it
- reading group starts tomorrow, I'm presenting Bush. 3 questions:
  1. is a trail authored or recorded?
  2. what's the modern trail blazer (a good survey paper? a blog?)
  3. why did nobody build the sharing part
- ISE 6664 first lecture was today; Brooks wants a project proposal by 02-04

## thinking about
- [[Bush1945 - As We May Think]]
'''))
D.append(('2026-01-27', '23:10', '23:59', [RG, 'project_mathetic_company', 'project_dynamite'], '''
# Tuesday, January 27

- read Engelbart 62 §I–III for thursday. H-LAM/T is the frame I've been missing
- talked to Hudson for 2h. idea: a notebook for researchers that is built on the H-LAM/T idea, working name **Papert Lab
  notebook** (we keep saying Papert). he wants to write it up in notion tomorrow, fine, I'll keep reading notes here
- Dynamite clustering still running, 41 clusters, labels look ok

## links
- [[Engelbart1962 - Augmenting Human Intellect]]
- [[Papert1980 - Mindstorms]]
'''))
D.append(('2026-02-09', '22:45', '23:59', ['project_tutortrace', RG], '''
# Monday, February 9

- read Ostrowski et al. (arXiv v1). very close to TutorTrace. same 30s windows. we need to position against it in related work
  before reviewers do it for us → [[Ostrowski2025 - Productive Struggle]]
- their stalling signal (near-identical prompts) is something we never computed. check on our VizPI data this week
- reading group: Nelson thursday, Xiaohang presenting
'''))
D.append(('2026-03-25', '00:30', '01:40', ['project_tutortrace'], '''
# Wednesday, March 25

- 6 days to UIST. related work section rewritten around Kapur + Ostrowski. [[Kapur2008 - Productive Failure]]
- camera-ready version of Ostrowski has different numbers than arXiv (0.71 vs 0.69 F1, kappa 0.64 vs 0.62). **use camera-ready**.
  fixed the .bib note
- our kappa 0.71 (3 raters). Yan wants the confusion matrix in the main paper not appendix
- skipped run, 5h sleep, do not do this again next week (will do this again next week)
'''))
D.append(('2026-03-31', '19:20', '23:58', ['project_tutortrace'], '''
# Tuesday, March 31

- deadline 23:59 AoE so really tomorrow morning ET, but Yan wants it in tonight
- final pass: abstract 148 words, figure 3 colors fixed for grayscale, supplementary video 2:58
- submitted 22:41. confirmation email came, paper id in the PCS tab
- sleep
'''))
D.append(('2026-04-28', '21:00', '22:15', ['project_ise6664_affective_computing'], '''
# Tuesday, April 28

- ISE 6664 final presentation thursday. our deck is 14 slides, too many for 12 minutes. Maya cutting the methods slides,
  Jordan does results, I do motivation + the frustration-lexicon part
- reading group: paused since the UIST crunch, restart in May maybe
- 10k easy, legs ok
'''))
D.append(('2026-05-05', '23:30', '23:59', ['project_idetrace'], '''
# Tuesday, May 5

- NeurIPS D&B tomorrow. IDETrace datasheet done, croissant metadata validated on the 3rd try
- splits: random 70/15/15 over windows. (future me: this is the bug. see [[IDETrace - leakage]])
- hosting on the lab HF org, license CC BY-NC 4.0
'''))
D.append(('2026-06-16', '22:10', '23:55', ['project_tutortrace', 'project_vt_phd_admin'], '''
# Tuesday, June 16

- UIST reviews: label reliability (kappa 0.71 ok but they want per-class), generalization beyond one course, telemetry privacy
- rebuttal plan: promise cross-course analysis (we have the Fall CS 3114 + one summer section), add limitations section,
  per-class kappa table. due thursday 06-18
- leave-of-absence talk with Yan is monday 06-22. write down what I actually want before the call, not during
'''))
D.append(('2026-07-24', '22:30', '23:59', ['project_idetrace'], '''
# Friday, July 24

- found it. train/test share students. everything in IDETrace is optimistic. → [[IDETrace - leakage]]
- told Yan on slack, she said fix first, panic later
- rebuttal due wednesday
'''))
D.append(('2026-08-12', '22:40', '23:35', [ENG, 'project_mathetic_company'], '''
# Wednesday, August 12

- day 4 in SF. Surplus kickoff with Lena was yesterday, demo day is far but they want weekly updates
- camera-ready for UIST due friday, almost done
- started [[Engelbart - where did this thought come from]]. the trail idea from Bush is the product, not a feature
- house wifi is unreliable on the 3rd floor, work from the kitchen
'''))
D.append(('2026-09-08', '23:00', '23:59', [ENG, 'project_berkeley_research_chats'], '''
# Tuesday, September 8

- berkeley chats start tomorrow (Elena Park), Priya thursday, Ben next week on zoom. questions doc is in drive
- import is the thing that has to work for these people. started [[Engelbart - import dedupe]]
- ask everyone: where does a thought live first for you? and how many tools hold your papers?
'''))
D.append(('2026-10-06', '21:30', '23:10', ['project_tutortrace'], '''
# Tuesday, October 6

- talk tomorrow 10:40. ran it twice: 15:20, 15:05. [[TutorTrace - talk Q&A prep]]
- clicker batteries, HDMI-C dongle, backup deck on USB and in email to myself
- Tomás said speakers meet at the session room 15 min before
'''))
D.append(('2026-10-14', '22:15', '23:50', [ENG, 'project_mathetic_company'], '''
# Wednesday, October 14

- Marcus call 2 this morning. he'll consider $50k into the pre-seed SAFE if the pilots convert. so: pilots have to convert
- Daniel (pilot B, yesterday) wanted Notion + Granola import and didn't understand the "Other" bucket on the connect screen
- combined with Priya's missed chats and duplicate PDFs: import is the product right now. updated
  [[Engelbart - import dedupe]] with the matching ladder
- half marathon tomorrow. carb load = rice. go to bed
'''))
D.append(('2026-10-16', '20:10', '20:40', [ENG, 'project_endurance_training'], '''
# Friday, October 16

- 1:24:51 yesterday. Owen 1:22:10. calves destroyed. went out too fast miles 3–5
- idea from the run: benchmark for import = invent a person, spread their stuff over ~30 tools, measure omissions / wrong
  items / dupes. Hudson likes it. start this weekend
'''))

for day, t0, t1, projs, body in D:
    fm = f'---\ntags: [daily]\ncreated: {day}\n---\n'
    note(f'Daily/{day}.md', fm + body.lstrip('\n'), f'{day} {t0}', f'{day} {t1}', projects=projs,
         notes='daily note (date-named title)')

g.finish()
