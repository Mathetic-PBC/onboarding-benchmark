"""OneNote (synthetic): per-page HTML as Microsoft Graph returns it (GET /me/onenote/pages/{id}/content).
Layout: synthetic/onenote/dbarron410@vt.edu/<Notebook>/<Section>/<Page title>.html. One item per page file."""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('onenote')
ACCT = 'dbarron410@vt.edu (Microsoft 365 OneNote)'
BASE = 'dbarron410@vt.edu'
ISE, IDE, QN = 'ISE 6664 Affective Computing', 'IDETrace', 'Quick Notes'
P_ISE, P_IDE, P_GTA = 'project_ise6664_affective_computing', 'project_idetrace', 'project_cs3604_gta'

PS = 'margin-top:0pt;margin-bottom:0pt'


def inline(s):
    s = html.escape(s, quote=False)
    parts = s.split('**')
    return ''.join(f'<span style="font-weight:bold">{x}</span>' if i % 2 else x for i, x in enumerate(parts))


def lis(items, tag):
    out = [f'<{tag}>']
    for it in items:
        if isinstance(it, tuple):
            out.append(f'<li>{inline(it[0])}{lis(it[1], tag)}</li>')
        else:
            out.append(f'<li>{inline(it)}</li>')
    out.append(f'</{tag}>')
    return ''.join(out)


def render(title, created, blocks):
    body = []
    for b in blocks:
        k, v = b[0], b[1]
        if k == 'h1': body.append(f'<h1 style="font-size:16pt;color:#1e4e79;{PS}">{inline(v)}</h1>')
        elif k == 'h2': body.append(f'<h2 style="font-size:13pt;color:#2e75b5;{PS}">{inline(v)}</h2>')
        elif k == 'p': body.append(f'<p style="{PS}">{inline(v)}</p>')
        elif k == 'br': body.append(f'<p style="{PS}">&nbsp;</p>')
        elif k == 'ul': body.append(lis(v, 'ul'))
        elif k == 'ol': body.append(lis(v, 'ol'))
        elif k == 'todo':
            for text, done in v:
                tag = 'to-do:completed' if done else 'to-do'
                body.append(f'<p data-tag="{tag}" style="{PS}">{inline(text)}</p>')
        elif k == 'table':
            rows = []
            for i, r in enumerate(v):
                cell = lambda c: ('<span style="font-weight:bold">%s</span>' % html.escape(str(c), quote=False)) if i == 0 else html.escape(str(c), quote=False)
                cells = ''.join('<td style="border:1px solid">%s</td>' % cell(c) for c in r)
                rows.append(f'<tr>{cells}</tr>')
            body.append('<table border="1" style="border:1px solid;border-collapse:collapse">' + ''.join(rows) + '</table>')
        else: raise ValueError(k)
    c = dt(created).strftime('%Y-%m-%dT%H:%M:%S') + '.0000000'
    inner = '\n\t\t\t'.join(body)
    return (f'<html lang="en-US">\n\t<head>\n\t\t<title>{html.escape(title, quote=False)}</title>\n'
            f'\t\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
            f'\t\t<meta name="created" content="{c}" />\n\t</head>\n'
            f'\t<body data-absolute-enabled="true" style="font-family:Calibri;font-size:11pt">\n'
            f'\t\t<div data-id="_default" style="position:absolute;left:48px;top:120px;width:624px">\n\t\t\t{inner}\n\t\t</div>\n'
            f'\t</body>\n</html>\n')


def safe(t):
    return t.replace('/', '-').replace(':', '-')


def page(nb, sec, title, created, modified, projects, blocks, notes=''):
    rel = f'{BASE}/{nb}/{sec}/{safe(title)}.html'
    assert dt(created) <= dt(modified) <= REF, title
    g.text(rel, render(title, created, blocks), created, modified, account=ACCT, project_ids=projects, notes=notes, modeled_on='',
           source=f'Microsoft Graph GET /me/onenote/pages/1-{hexid(rel, 32)}!{hexid(rel + "x", 6)}/content')


# =====================================================================================================
# ISE 6664 Affective Computing (Spring 2026, Dr. Alan Brooks)
# =====================================================================================================
L = 'Lectures'
page(ISE, L, 'Week 1 - Intro + logistics', '2026-01-13 14:04', '2026-01-13 15:22', [P_ISE], [
    ('h1', 'ISE 6664 wk1 — Tue Jan 13 2026'),
    ('p', 'Dr. Alan Brooks. Whittemore 3xx, TR 2:00–3:15. OH Wed 10–11 + by appt. ~22 people, mix of ISE / CS / psych.'),
    ('h2', 'grading'),
    ('table', [['component', 'weight', 'notes'], ['reading responses', '20%', '8 of 10, ~1 page, due Mon 11:59pm'],
               ['participation / discussion lead', '10%', 'lead one discussion, sign-up sheet on Canvas'],
               ['midterm', '20%', 'take-home, week 8'], ['team project', '50%', 'proposal 10 / report 25 / presentation 15']]),
    ('h2', 'what is affective computing'),
    ('ul', ['computing that relates to, arises from, or deliberately influences emotion (Picard 1997 framing)',
            'three strands he keeps coming back to: **recognize** affect, **express** affect (agents), **respond** to affect (adaptive systems)',
            'he is skeptical of "emotion AI" marketing — wants us to always ask what the ground truth is',
            'example he used: car that detects drowsiness vs. a hiring tool that "reads" candidate enthusiasm — same tech, totally different validity + ethics']),
    ('h2', 'project'),
    ('ul', ['teams of 3, pick by wk 4', 'can reuse own research data if IRB allows — ask him first',
            'final presentations last week (Apr 30), report ~12–15 pages ACM format']),
    ('p', 'thought: frustration during AI-assisted programming is basically our whole lab topic. could do something with tutor transcripts instead of IDE telemetry so it is not double-dipping on VizPI/TutorTrace.'),
])

page(ISE, L, 'Week 2 - Theories of emotion', '2026-01-20 14:02', '2026-01-21 09:40', [P_ISE], [
    ('h1', 'wk2 — theories (Jan 20)'),
    ('h2', 'basic / discrete emotions'),
    ('ul', ['Ekman: small set of universal categories w/ distinct expressions', 'critique: cross-cultural recognition studies used forced choice → inflated agreement']),
    ('h2', 'dimensional'),
    ('ul', ['Russell circumplex: valence × arousal', 'PAD adds dominance', 'nice for continuous annotation (FEELtrace-style sliders)',
            'frustration ≈ negative valence, moderate–high arousal; boredom ≈ negative valence, low arousal — these get confused by text classifiers']),
    ('h2', 'appraisal theories'),
    ('ul', ['emotion = outcome of evaluating an event vs your goals (relevance, congruence, coping potential, agency)',
            'frustration = goal blocked + you still think you could have done it → this maps really cleanly onto a student stuck on a bug',
            'OCC model used a lot in agents bc it is implementable as rules']),
    ('h2', 'constructed emotion (Barrett)'),
    ('ul', ['categories are constructed from interoception + concepts, no fingerprints', 'implication for us: labels are always an interpretation, treat as annotator judgement not ground truth']),
    ('p', 'Brooks: "pick the theory that matches your measurement, and say so in the paper." write that down for the project report.'),
])

page(ISE, L, 'Week 3 - Measuring affect', '2026-01-27 14:06', '2026-01-27 15:31', [P_ISE], [
    ('h1', 'wk3 — measurement (Jan 27)'),
    ('table', [['method', 'pros', 'cons'], ['self-report (SAM, PANAS)', 'cheap, direct', 'retrospective bias, interrupts task'],
               ['experience sampling', 'in situ', 'annoying, low compliance after week 1'],
               ['physiology (EDA, HRV)', 'continuous', 'arousal only, motion artifacts, needs baseline'],
               ['observation (BROMP)', 'field-ready, trained coders', 'coder drift, 20s windows'],
               ['behavioral logs', 'free, scalable', 'needs validation against one of the above']]),
    ('ul', ['BROMP: trained observers code students round-robin in 20s windows → kind of what our 30s TA labeling windows are doing post-hoc',
            'Brooks wants each project to have at least one validation source that is not the same signal it is predicting',
            'EDA lab in wk6 — wristbands from the Kinesiology lab']),
    ('p', 'reading response 2 due Mon: pick one measurement paper and critique its ground truth.'),
])

page(ISE, L, 'Week 4 - Faces and the FACS debate', '2026-02-03 14:01', '2026-02-03 15:18', [P_ISE], [
    ('h1', 'wk4 — faces (Feb 3)'),
    ('ul', ['FACS = action units, anatomically grounded, coders need ~100h training',
            'automated AU detection works ok for posed, much worse for spontaneous + webcam lighting',
            '2019 review (Barrett et al.): facial movements do not reliably map to emotion categories across contexts — a scowl is not always anger',
            'class discussion got heated about proctoring software that flags "suspicious" expressions']),
    ('p', 'for our project: we are NOT doing video. text only. good, avoids the whole debate + IRB headache.'),
    ('todo', [('ask Maya if she still has access to the tutor transcript set from her RA job', True),
              ('email Jordan re: team name for sign-up sheet', True)]),
])

page(ISE, L, 'Week 5 - Affect in learning', '2026-02-10 14:03', '2026-02-11 08:55', [P_ISE, 'project_vizpi'], [
    ('h1', 'wk5 — affect + learning (Feb 10)'),
    ('ul', ['learning-centered states differ from basic emotions: confusion, frustration, boredom, engaged concentration, delight, surprise',
            'confusion is not bad by itself — productive if it gets resolved',
            ('D\'Mello & Graesser affect dynamics model', ['impasse → confusion', 'confusion unresolved → frustration', 'frustration persists → boredom / disengagement',
                                                            'resolution at any point → back to engaged concentration']),
            'implication: timing of help matters — intervene in the confusion→frustration transition, not before']),
    ('p', '**this is basically the stalled-after-error state from the VizPI labeling guide v3.** a student who errors, re-runs the same thing, then goes idle = confusion turning into frustration. worth a sentence in the related work for TutorTrace too.'),
    ('p', 'Brooks mentioned Baker et al. "better to be frustrated than bored" — boredom is the one that predicts worse outcomes.'),
])

page(ISE, L, 'Week 6 - EDA wristband lab', '2026-02-17 14:00', '2026-02-17 15:40', [P_ISE], [
    ('h1', 'wk6 lab — EDA (Feb 17)'),
    ('p', 'paired with Jordan. Empatica-style wristbands, 4 Hz EDA. protocol: 2 min baseline, 3 min Stroop, 2 min rest, 3 min mental arithmetic w/ time pressure.'),
    ('table', [['segment', 'mean SCL (µS) me', 'mean SCL (µS) Jordan'], ['baseline', '2.1', '3.4'], ['Stroop', '2.9', '3.9'],
               ['rest', '2.4', '3.6'], ['arithmetic', '3.6', '4.8']]),
    ('ul', ['huge individual differences in absolute level → always normalize per person', 'my peaks lag the stressor by ~2–3 s',
            'moving my hand to the keyboard caused spikes. motion artifacts are real.',
            'arousal went up for both tasks but only arithmetic felt bad — EDA can\'t tell valence. Brooks\' point exactly.']),
])

page(ISE, L, 'Week 7 - Text-based affect detection', '2026-02-24 14:05', '2026-02-24 15:27', [P_ISE], [
    ('h1', 'wk7 — text (Feb 24)'),
    ('ul', ['lexicon approaches (LIWC categories: negemo, anger, anx) — interpretable, terrible at negation + sarcasm',
            'fine-tuned transformers better but inherit annotator bias',
            'short chat turns are hard: "ok" can be resignation or agreement',
            'context window matters — label the turn given the previous 2–3 turns, not alone']),
    ('h2', 'notes for our project'),
    ('ul', ['frustration markers in tutor chats probably behavioural not lexical: repeated question, shrinking message length, "just tell me", all caps, giving up',
            'need to code at the **turn** level with conversation context',
            'baseline = LIWC negemo; compare against our codebook-based features']),
])

page(ISE, L, 'Week 9 - Affect-aware design + ethics', '2026-03-17 14:02', '2026-03-17 15:15', [P_ISE], [
    ('h1', 'wk9 — design + ethics (Mar 17, post spring break)'),
    ('ul', ['who benefits from detection? student, instructor, platform?', 'consent for continuous affect inference ≠ consent for chat logging',
            'EU AI Act bans emotion recognition in workplaces + education (with exceptions) — Brooks spent 20 min on this',
            'design pattern: surface to the person themselves first ("you seem stuck, want a hint?") instead of reporting up to an instructor',
            'false positives cost: telling a focused student they look frustrated is annoying + breaks flow']),
    ('p', 'our report needs an ethics section: we only analyze existing de-identified transcripts, no deployment, and say explicitly what a real system should not do.'),
])

page(ISE, L, 'Week 11 - Guest lecture (missed)', '2026-03-31 13:48', '2026-04-02 21:10', [P_ISE], [
    ('h1', 'wk11 — guest lecture on affective tutoring systems'),
    ('p', 'skipped — UIST deadline is tonight 23:59 AoE. told Brooks Monday.'),
    ('p', 'from Maya\'s notes (pasted Apr 2):'),
    ('ul', ['guest built an affect-sensitive math tutor, used a mix of interaction logs + self-report pop-ups every 5 min',
            'empathetic messages alone did not improve learning; changing the task difficulty did',
            'students hated being asked how they feel too often (pop-up fatigue after ~3 per session)']),
    ('todo', [('watch the recording on Canvas', False)]),
])

page(ISE, L, 'Week 12 - Evaluation and validity', '2026-04-07 14:04', '2026-04-07 15:20', [P_ISE], [
    ('h1', 'wk12 — evaluation (Apr 7)'),
    ('ul', ['report agreement with chance correction (kappa / Krippendorff alpha), not % agreement',
            'base rates! a detector of a rare state with 90% accuracy can be useless',
            'leave-one-person-out / group CV when the same person contributes multiple samples — otherwise you learn the person not the state',
            'ecological validity: lab-induced frustration ≠ real frustration']),
    ('p', 'note to self: our transcript split should be grouped by student too. same issue as any telemetry dataset.'),
])

R = 'Readings'
page(ISE, R, 'Reading responses - schedule', '2026-01-15 21:30', '2026-03-02 23:41', [P_ISE], [
    ('h1', 'reading responses — need 8 of 10'),
    ('table', [['#', 'due', 'topic', 'status'], ['1', 'Jan 19', 'Picard ch. 1', 'done'], ['2', 'Feb 2', 'measurement critique', 'done'],
               ['3', 'Feb 9', 'D\'Mello & Graesser dynamics', 'done'], ['4', 'Feb 16', 'Calvo & D\'Mello review', 'done'],
               ['5', 'Feb 23', 'text affect detection', 'done'], ['6', 'Mar 2', 'physiology', 'done'], ['7', 'Mar 23', 'ethics', 'skip (UIST)'],
               ['8', 'Mar 30', 'affective tutors', 'skip (UIST)'], ['9', 'Apr 6', 'evaluation', 'todo'], ['10', 'Apr 13', 'open', 'todo']]),
    ('p', 'skipping 7 + 8 uses up both drops. do NOT miss 9 or 10.'),
])

page(ISE, R, 'Calvo and D\'Mello 2010 review', '2026-01-31 22:15', '2026-02-01 00:20', [P_ISE], [
    ('h1', 'Calvo & D\'Mello (2010) — affect detection review'),
    ('p', 'my summary: survey of detection across modalities (face, voice, body, physiology, text, multimodal). main argument is that the field had grown by modality silos and needed theory to drive which signals matter.'),
    ('ul', ['multimodal fusion helps less than expected in naturalistic data — gains mostly in posed datasets',
            'most systems trained on acted emotions; spontaneous data much harder',
            'calls for context-aware detection (task, person, history)']),
    ('h2', 'response angle'),
    ('p', '16 years later the silo problem looks the same for LLM tutoring: people classify single messages without the session context. that is the critique I wrote.'),
])

page(ISE, R, 'D\'Mello and Graesser 2012 - dynamics', '2026-02-08 20:50', '2026-02-08 23:05', [P_ISE], [
    ('h1', 'D\'Mello & Graesser (2012) — dynamics of affective states during complex learning'),
    ('ul', ['transition likelihoods between states measured with retrospective judgements from video of sessions',
            'confusion → engagement when resolved, confusion → frustration when not',
            'frustration → boredom path is weaker than the model predicts but present',
            'methodological point: they used a transition metric that corrects for base rates (L statistic)']),
    ('p', 'for project: we could compute transitions between coded turns too (neutral → confused → frustrated → disengaged) instead of just counting frustration turns. Jordan liked this.'),
])

PJ = 'Project'
page(ISE, PJ, 'Kickoff with Maya and Jordan', '2026-02-05 16:10', '2026-02-05 17:30', [P_ISE], [
    ('h1', 'project kickoff — Thu Feb 5, Newman library 2nd floor'),
    ('p', 'team: me, Maya Torres (ISE, HF track), Jordan Lee (CS MS).'),
    ('h2', 'ideas we threw out'),
    ('ol', ['EDA during code review — needs devices + IRB, too slow', 'sentiment of course forum posts over semester — done to death',
            '**frustration signals in AI-tutoring transcripts** ← picked', 'voice prosody in TA office hours — no data']),
    ('h2', 'data'),
    ('ul', ['Maya\'s old RA lab has ~600 de-identified transcripts from an LLM homework tutor (intro stats), already IRB-cleared for secondary analysis',
            'need Brooks OK + data use note from her former PI', 'turn-level, timestamps included → can get response latency']),
    ('h2', 'roles (tentative)'),
    ('ul', ['Maya: data access, codebook lead', 'Jordan: feature extraction + classifier baseline', 'me: related work, analysis plan, transitions analysis, writing glue']),
    ('todo', [('Maya: email former PI re data use', True), ('David: 1-paragraph pitch to Brooks by Mon', True), ('Jordan: set up shared repo + Overleaf', True)]),
])

page(ISE, PJ, 'Proposal outline', '2026-02-16 19:20', '2026-02-18 22:47', [P_ISE], [
    ('h1', 'proposal — due Feb 20'),
    ('p', 'title: **Frustration signals in AI-tutoring transcripts**'),
    ('h2', 'RQs'),
    ('ol', ['which observable conversational behaviours mark student frustration in LLM-tutor chats?',
            'how reliably can human coders label frustration at the turn level?',
            'do tutor response types (direct answer, hint, question, encouragement) differ in what follows a frustrated turn?']),
    ('h2', 'method'),
    ('ul', ['sample 200 of the ~600 transcripts, stratified by length', 'codebook: 5 states (neutral, confused, frustrated, disengaged, satisfied) + behavioural markers',
            '3 coders (us), 50 transcripts overlap for kappa', 'baseline: LIWC negemo per turn; ours: marker features + previous-turn context',
            'transition analysis à la D\'Mello & Graesser']),
    ('h2', 'risks'),
    ('ul', ['frustration might be rare (<10% turns) → class imbalance', 'stats homework ≠ programming, generalization caveat', 'only 3 coders, all on the team (bias)']),
])

page(ISE, PJ, 'Meeting 2026-03-05 - codebook v1', '2026-03-05 17:05', '2026-03-05 18:40', [P_ISE], [
    ('h1', 'meeting Mar 5 — codebook v1 agreement'),
    ('p', 'coded 50 overlap transcripts (1,212 student turns) independently.'),
    ('table', [['pair', 'kappa (5 states)', 'kappa (frustrated vs not)'], ['David–Maya', '0.55', '0.61'], ['David–Jordan', '0.52', '0.57'], ['Maya–Jordan', '0.60', '0.64'],
               ['Fleiss (all 3)', '0.56', '0.61']]),
    ('h2', 'disagreements'),
    ('ul', ['"ok" / "k" after a long tutor explanation — Maya codes disengaged, I code neutral', 'sarcastic "great thanks" — Jordan coded satisfied (lol)',
            'confused vs frustrated boundary: decided frustrated requires a **repeat** or explicit negative statement']),
    ('h2', 'codebook v2 changes'),
    ('ul', ['add marker: re-asks same question within 3 turns', 'add marker: message length drops by >50% vs own running mean',
            'sarcasm rule: code by following turn', 'decision tree in the codebook instead of definitions only']),
    ('todo', [('Maya: write v2 doc', True), ('everyone recode 30 new overlap transcripts by Mar 19', True)]),
])

page(ISE, PJ, 'Meeting 2026-04-02 - results check-in', '2026-04-02 16:00', '2026-04-02 17:25', [P_ISE], [
    ('h1', 'meeting Apr 2 — back from UIST hole'),
    ('p', 'apologized for being MIA last week. Jordan + Maya finished coding the remaining transcripts.'),
    ('ul', ['v2 agreement on the new 30: Fleiss kappa 0.69 (frustrated vs not 0.73)', '200 transcripts, 4,870 student turns; frustrated = 9.8% of turns, 41% of transcripts have ≥1',
            'strongest markers: re-ask within 3 turns, "just give me the answer"-type requests, length drop',
            'LIWC negemo baseline AUC 0.61; marker + context logistic regression AUC 0.78 (transcript-grouped 5-fold CV)']),
    ('h2', 'tutor responses after a frustrated turn'),
    ('table', [['tutor response', 'n', 'next turn still frustrated / disengaged'], ['direct answer', '142', '31%'], ['hint', '171', '44%'],
               ['Socratic question', '98', '58%'], ['encouragement only', '66', '61%']]),
    ('p', 'interesting tension: Socratic questions are pedagogically "good" but most often followed by more frustration. need to be careful — not causal, students who get questions may already be further gone.'),
    ('todo', [('David: transition matrix + L statistic', True), ('Jordan: confusion matrix + feature importances', True), ('Maya: ethics section draft', True)]),
])

page(ISE, PJ, 'Meeting 2026-04-16 - report split', '2026-04-16 16:30', '2026-04-24 23:58', [P_ISE], [
    ('h1', 'report plan — target 14 pages, due May 5'),
    ('table', [['section', 'owner', 'pages', 'status'], ['1 intro', 'David', '1.5', 'drafted'], ['2 related work', 'David', '2', 'drafted'],
               ['3 data + codebook', 'Maya', '2.5', 'drafted'], ['4 method (features, CV)', 'Jordan', '2', 'drafted'],
               ['5 results', 'Jordan + David', '3', 'figures done'], ['6 discussion + design implications', 'David', '1.5', 'in progress'],
               ['7 ethics + limitations', 'Maya', '1', 'drafted'], ['refs + appendix codebook', 'all', '0.5 + appx', '—']]),
    ('ul', ['transition result: confused → frustrated jumps when tutor gives a hint that restates the problem (L = 0.18)',
            'Brooks feedback on proposal: be explicit about which emotion theory → we use appraisal (goal blocked) + say labels are coder judgements',
            'final presentation Apr 30, 12 min + 3 Q&A']),
])

FP = 'Final presentation'
page(ISE, FP, 'Final presentation prep (Apr 30)', '2026-04-27 21:15', '2026-04-29 01:12', [P_ISE], [
    ('h1', 'final presentation — Thu Apr 30, slot 3 of 6'),
    ('h2', 'slide plan (12 min)'),
    ('table', [['#', 'slide', 'who', 'time'], ['1', 'title + hook (a real-looking frustrated exchange, paraphrased)', 'David', '0:45'],
               ['2', 'why frustration, why transcripts', 'David', '1:15'], ['3', 'data + codebook decision tree', 'Maya', '2:00'],
               ['4', 'agreement v1 → v2', 'Maya', '1:00'], ['5', 'markers + classifier (AUC 0.61 vs 0.78)', 'Jordan', '2:00'],
               ['6', 'tutor response table', 'Jordan', '1:30'], ['7', 'transition diagram', 'David', '1:30'], ['8', 'design implications + ethics', 'Maya', '1:30'],
               ['9', 'limitations / questions', 'David', '0:30']]),
    ('h2', 'likely questions'),
    ('ul', ['why not use the students\' own self-report? → none in this data, say it is the biggest limitation',
            'stats homework vs programming? → markers are behavioural, likely transfer, not tested',
            'is the Socratic finding causal? → no, selection; propose a randomized follow-up',
            'what about LLM-based labeling? → tried GPT-style zero-shot on 100 turns as a side check, kappa vs majority 0.48, not in the main results']),
    ('todo', [('rehearse full run Wed 7pm Torgersen 1030', True), ('cut slide 2 to 1 min if over', True), ('bring HDMI-C adapter', True)]),
])

page(ISE, FP, 'Dry run feedback', '2026-04-29 20:40', '2026-04-29 22:05', [P_ISE], [
    ('h1', 'dry run Apr 29 — ran 14:10, need to cut 2 min'),
    ('ul', ['Maya slide 3 too dense — split the decision tree into a build animation', 'my transition slide: say the takeaway first, then the diagram',
            'Jordan: drop the feature-importance bar chart, keep the AUC comparison', 'everyone: stop saying "basically"',
            'second run: 12:20. fine.']),
    ('p', 'after presentation (Apr 30): Brooks asked about base rates and whether 9.8% frustrated turns is "real" or a codebook artifact. good question, add a paragraph to the report.'),
])

# =====================================================================================================
# IDETrace leakage investigation (Jul–Aug 2026)
# =====================================================================================================
LB, RB = 'Leakage bug', 'Rebuttal'
page(IDE, LB, '2026-07-24 symptoms', '2026-07-24 10:12', '2026-07-24 13:40', [P_IDE], [
    ('h1', 'Fri Jul 24 — something is off with the splits'),
    ('p', 'was re-running the per-feature ablation R2 asked for. dropping ALL keystroke features only costs 0.02 macro-F1?? that should hurt way more.'),
    ('h2', 'symptoms'),
    ('ul', ['per-student accuracy on test is weirdly uniform (0.79–0.84) — real behaviour is never that even',
            'nearest-neighbour check: for 61% of test windows, the closest train window (cosine on features) is from the **same student**, often adjacent in time',
            'student s_0412 has 211 windows in train and 54 in test',
            'a model trained on student id one-hot alone gets 0.46 macro-F1. majority class is 0.19. it is learning who, not what.']),
    ('p', 'hypothesis: split is at the window level, not the student level. windows from the same session are near-duplicates (30s overlapping by 10s). leakage.'),
    ('todo', [('read make_splits.py properly', True), ('tell Yan before the weekend', True), ('don\'t panic-post in Slack yet', True)]),
])

page(IDE, LB, 'Checking the split script', '2026-07-24 14:05', '2026-07-24 23:31', [P_IDE], [
    ('h1', 'make_splits.py audit (Jul 24, afternoon)'),
    ('p', 'confirmed. line ~88: train_test_split(windows, stratify=labels, test_size=0.2, random_state=13). no groups anywhere.'),
    ('table', [['check', 'result'], ['students total', '318'], ['students with windows in both train + test', '318 (100%)'],
               ['windows total', '61,480'], ['test windows whose session also in train', '96.4%'],
               ['windows overlapping in time with a train window', '38.7% (10s overlap from sliding stride)']]),
    ('ul', ['the stride overlap makes it even worse: some test windows share 1/3 of their events with a train window',
            'the README for the dataset says "student-disjoint splits". it was never true. this is on me, I wrote the script in April under deadline',
            'baseline numbers in the submitted paper all use this split']),
    ('p', 'called Yan 6pm. her take: fix it now, rerun everything, report both numbers honestly in the rebuttal. reviewers will respect it more than if they find it later.'),
])

page(IDE, LB, 'Grouped split fix', '2026-07-25 11:20', '2026-07-25 19:02', [P_IDE], [
    ('h1', 'fix — split grouped by student id (Sat Jul 25)'),
    ('ul', ['replaced with StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=13), groups=student_id; fold 0 = test, rest train/val',
            'also stride now non-overlapping inside test (no shared events across windows in eval)',
            'added assert: set(train.student_id) & set(test.student_id) == set()',
            'split files now written to splits/v2/ with a SPLITS.md + hashes so the release has exact ids']),
    ('h2', 'label distribution after regroup (test fold)'),
    ('table', [['label', 'v1 test %', 'v2 test %'], ['productive', '34.1', '33.2'], ['stalled', '21.7', '23.0'], ['help-seeking', '26.9', '25.8'],
               ['off-task', '17.3', '18.0']]),
    ('p', 'distribution close enough. 64 students in test, 254 in train/val.'),
])

page(IDE, LB, 'Rerun results', '2026-07-26 09:30', '2026-07-26 22:48', [P_IDE], [
    ('h1', 'rerun with v2 splits (Sun Jul 26) — 5 seeds each'),
    ('table', [['model', 'macro-F1 v1 (leaky)', 'macro-F1 v2 (grouped)', 'Δ'], ['majority', '0.19', '0.19', '0.00'], ['logistic regression', '0.69', '0.65', '−0.04'],
               ['XGBoost', '0.77', '0.71', '−0.06'], ['GRU over events', '0.79', '0.72', '−0.07'], ['transformer (ours)', '0.81', '0.74', '−0.07']]),
    ('ul', ['std over seeds for transformer v2: ±0.012', 'ranking of models unchanged → the paper\'s claims about which model family wins still hold',
            'biggest per-class drop: stalled (0.76 → 0.64). makes sense, stalled windows from one student look alike',
            'keystroke ablation now costs 0.09 → the R2 ablation finally behaves sensibly']),
    ('p', 'headline: **0.81 → 0.74**. still well above baselines. annoying but survivable.'),
])

page(IDE, LB, 'Sanity checks after fix', '2026-07-27 13:15', '2026-07-27 23:50', [P_IDE], [
    ('h1', 'more checks (Mon Jul 27)'),
    ('todo', [('student-id-only model on v2: 0.19 = majority. leakage gone', True),
              ('near-duplicate windows ACROSS students (starter code, TA demo paste)? 2.1% of test have a >0.95 cosine twin in train from another student — keep, it is real (same starter code)', True),
              ('course-level held-out split (train on course A, test on B) as extra robustness: 0.69', True),
              ('check the other two downstream tasks (next-action, time-to-help) for the same bug', True),
              ('time-to-help task: also leaky, MAE 41s → 53s', True)]),
    ('p', 'course-level number (0.69) goes in the appendix, not headline. Yan agrees.'),
])

page(IDE, RB, 'Rebuttal wording', '2026-07-28 15:40', '2026-07-29 02:14', [P_IDE], [
    ('h1', 'rebuttal paragraph drafts (Jul 28)'),
    ('h2', 'draft 1 (too apologetic)'),
    ('p', 'We sincerely apologize for an error in our data splitting procedure which may have inflated our results...'),
    ('h2', 'draft 3 (going with this, ~120 words)'),
    ('p', 'While running the ablation requested by R2 we found that our original train/test split was made at the window level, so windows from the same student appeared in both sets. We have re-split the data grouped by student id (no student appears in more than one split) and re-ran all experiments with five seeds. Our best model\'s macro-F1 changes from 0.81 to 0.74; all baselines drop by similar margins and the ranking of models is unchanged. We report both numbers in the revision, release the exact split ids, and add a course-held-out evaluation (0.69). We thank R2: the ablation is what exposed the problem.'),
    ('ul', ['Yan edits: drop "unfortunately", put the new number in the first sentence where possible', 'keep both numbers in a table in the revised paper, not just the text']),
])

page(IDE, RB, 'Rebuttal posted - what we promised', '2026-07-29 17:05', '2026-07-29 18:20', [P_IDE], [
    ('h1', 'rebuttal posted Wed Jul 29, 4:52pm ET'),
    ('h2', 'commitments (do not forget these if accepted)'),
    ('ol', ['replace all main-table numbers with v2 grouped-split results', 'add a "split audit" subsection + table showing v1 vs v2',
            'release splits/v2 ids + hashes with the dataset', 'course-held-out result in appendix',
            'fix README claim about student-disjoint splits', 'datasheet: add a known-issues/errata entry for anyone who downloaded the preview']),
    ('p', 'decision expected late Sept. nothing to do until then except the datasheet/README.'),
])

page(IDE, RB, 'Leftovers after rebuttal', '2026-08-12 21:30', '2026-08-26 22:05', [P_IDE], [
    ('h1', 'loose ends (from SF)'),
    ('todo', [('push splits/v2 + SPLITS.md to the dataset repo', True), ('README: replace "student-disjoint" claim with how splits are made', True),
              ('datasheet errata entry dated 2026-07-29', True), ('re-export figures with v2 numbers (fig 3, fig 5)', False),
              ('ask Xiaohang whether TutorTrace eval used the same helper — it did not, it uses session-level CV already', True)]),
    ('p', 'reminder: GRA ends Aug 15, so any remaining IDETrace work is on my own time now.'),
])

# =====================================================================================================
# Quick Notes
# =====================================================================================================
OH, MI = 'CS 3604 Office Hours', 'Misc'
page(QN, OH, 'OH 10-22', '2025-10-22 15:02', '2025-10-22 16:58', [P_GTA], [
    ('h1', 'CS 3604 office hours — Wed Oct 22, 3–5pm, McB 106'),
    ('table', [['time', 'who (initials)', 'topic', 'resolved?'], ['3:05', 'K.M.', 'P3 — Flask route returns 405 on form submit (missing methods=["POST"])', 'yes'],
               ['3:20', 'A.T.', 'P3 — how much of the user-story template to fill', 'yes'], ['3:40', 'R.S. + J.P.', 'team conflict, one member not committing → sent to instructor', 'referred'],
               ['4:10', 'D.N.', 'P2 regrade question — rubric item 3, points were correct', 'no change'], ['4:35', 'L.H.', 'SQLAlchemy session not committing', 'yes']]),
    ('p', '5 visits. P3 405 error came up twice this week — post a Canvas announcement about methods=["POST"].'),
])

page(QN, OH, 'OH - P3 questions', '2025-11-05 15:00', '2025-11-05 17:10', [P_GTA], [
    ('h1', 'OH Wed Nov 5 — P3 due Fri'),
    ('ul', ['busiest one so far, ~11 students, line out the door at 4', 'most common: CSRF token missing in forms (WTForms) → 4 people',
            'test coverage requirement (70%) — people do not know how to run coverage with pytest; showed pytest --cov',
            'two teams asked for extension → no, policy is the 3 late days']),
    ('todo', [('ask instructor about adding a second OH slot P3 week', True), ('write up the coverage command as FAQ on Canvas', True)]),
])

page(QN, OH, 'OH 12-03 final project', '2025-12-03 15:01', '2025-12-03 17:22', [P_GTA], [
    ('h1', 'OH Dec 3 — final project crunch'),
    ('ul', ['deploy issues on the department VM: port 5000 blocked, use 8080 + the nginx config from the handout',
            'demo video length: max 5 min, several teams at 9+ — told them to cut',
            'one team\'s Postgres migrations broken after renaming a column, walked through alembic downgrade/upgrade',
            'reminder: grades due Dec 15 — final project grading has to start Dec 10 latest']),
    ('p', '64 students → 16 teams. block 2h per evening Dec 10–13 for grading.'),
])

page(QN, OH, 'regrade - P4 late days', '2025-12-11 22:40', '2025-12-12 10:15', [P_GTA], [
    ('h1', 'P4 regrade dispute — notes for instructor'),
    ('ul', ['student submitted P4 at 12:07am, 7 min after deadline, Canvas marked late → 1 late day used, but student had 0 left (used 3 on P2/P3)',
            'their argument: Canvas was slow, upload started 11:58pm', 'syllabus: late days counted by Canvas timestamp, no grace period stated',
            'submission history shows first attempt at 12:04am (failed, file too large), not 11:58']),
    ('p', 'my recommendation: apply policy as written (−10%), but suggest a 15-min grace period in the syllabus next term. forwarded to instructor Dec 12; their call.'),
])

page(QN, MI, 'to do this week', '2025-11-10 08:45', '2025-11-14 23:20', [P_GTA, 'project_vizpi', 'project_none'], [
    ('h1', 'week of Nov 10'),
    ('todo', [('VizPI deployment #2 data dump → s3 + check section B gaps (reconnect bug 3:30–4:10)', True),
              ('labeling sprint kickoff w/ Minsun + Xiaohang Fri', True), ('grade P3 (16 teams) by Sun', False),
              ('CS 3604 OH Wed', True), ('bike shop — derailleur skipping on 4th gear', False), ('renew car registration (DMV online)', True),
              ('respond to TACode handoff email', True)]),
], notes='mixed to-do list spanning VizPI, CS 3604 and personal errands')

page(QN, MI, 'Untitled page', '2026-07-21 11:02', '2026-07-21 11:40', ['project_vt_phd_admin'], [
    ('p', 'call w Grace Kim 11am'),
    ('ul', ['leave of absence form: needs advisor signature (Yan) + dept head, then Graduate School', 'effective Fall 2026, up to 2 semesters, can extend once',
            'GRA appointment ends Aug 15 — last paycheck end of Aug', 'health insurance: student plan ends with enrollment, look at COBRA-like option or SF employer',
            'have to notify ISSS? no — not international, ignore', 'returning: submit return form 30 days before semester',
            'she\'ll send DocuSign by end of next week → target signing Jul 31']),
    ('p', 'ask: does leave pause the qualifying exam clock? — she thinks yes, will confirm by email'),
], notes='HARD CASE: vague title — "Untitled page" holds leave-of-absence call notes with Grace Kim (project_vt_phd_admin)')

page(QN, MI, 'Page 1', '2026-02-24 22:10', '2026-03-03 09:15', ['project_none'], [
    ('p', 'parking ticket appeal'),
    ('ul', ['ticket #A-2219xx, Jan 29, lot near Perry St garage, "no valid permit"', 'I had the permit, it was on the dash face down after the wind',
            'appeal window 10 days — submitted online Feb 6 with photo of permit', 'result Mar 2: reduced to warning']),
    ('p', 'car insurance renews Apr 1 — compare quotes before 03-20'),
], notes='HARD CASE: vague title — "Page 1" is a personal parking-ticket / car note')

d = bursty_dates(1, 'onenote-taxes', '2026-03-01', '2026-04-10')[0]
page(QN, MI, 'taxes 2025 - docs', d, later(d, days=9, hours=3), ['project_none'], [
    ('h1', '2025 taxes'),
    ('todo', [('W-2 from VT (GRA)', True), ('1098-T tuition statement — check box 5 scholarships vs box 1', True), ('1099-INT from savings', True),
              ('state return VA', True), ('figure out if the stipend portion is taxable — it is', True), ('file by Apr 15', True)]),
    ('p', 'used free file. refund small. keep pdfs in Drive/Taxes/2025.'),
])

d = bursty_dates(1, 'onenote-geo', '2026-01-12', '2026-02-15')[0]
page(QN, MI, 'podcast notes - chips + Taiwan', d, later(d, minutes=50), ['project_none'], [
    ('h1', 'notes from a grand strategy podcast episode on chips'),
    ('ul', ['export controls on advanced lithography as a chokepoint strategy — works only as long as allies align',
            'argument that the controls buy time but also accelerate domestic substitution in China',
            'Taiwan "silicon shield" idea — some think it cuts both ways',
            'want to read: something on the history of the 1980s US–Japan semiconductor agreement for comparison']),
])

d = bursty_dates(1, 'onenote-bike', '2026-05-09', '2026-06-14')[0]
page(QN, MI, 'bike derailleur', d, later(d, days=3), ['project_none'], [
    ('h1', 'rear derailleur still skipping'),
    ('ul', ['skips under load in 4th–5th, fine on the stand', 'tried: barrel adjuster ¼ turn counterclockwise — better but not fixed',
            'probably bent hanger from when it fell at the rack', 'shop quote: hanger alignment $15, new hanger $28 + labour', 'chain at 0.5% wear, ok for now']),
    ('todo', [('drop off Tue', True), ('ask about cassette wear too', False)]),
])

page(QN, MI, 'before leaving Blacksburg', '2026-07-30 22:15', '2026-08-06 23:40', ['project_none'], [
    ('h1', 'move out list (leaving Aug 7)'),
    ('todo', [('lease end walkthrough Aug 6 10am', True), ('cancel internet (Aug 6)', True), ('forward mail → SF address', True),
              ('sell desk + monitor arm on marketplace', True), ('return VT key for the lab + McB office', True), ('donate kitchen stuff', True),
              ('ship 3 boxes of books (UPS ground ~$90)', True), ('car: drive or sell?? — selling to carmax, offer Aug 3', True)]),
])

page(QN, MI, 'travel funding form - fields', '2026-09-22 20:10', '2026-09-24 11:30', ['project_vt_phd_admin', 'project_tutortrace'], [
    ('h1', 'VT GSA / dept travel funding — UIST 2026'),
    ('table', [['field', 'what I put'], ['event', 'UIST 2026 (paper presentation, TutorTrace)'], ['presentation date', 'Oct 7, 2026'],
               ['registration', '$650 (student, early)'], ['lodging', '3 nights shared'], ['airfare', 'n/a — already in SF? check if it is local'],
               ['advisor approval', 'Yan — emailed Sep 22'], ['enrollment status', 'on leave — Grace says still eligible since paper is VT work']]),
    ('todo', [('get Yan\'s approval email', True), ('attach acceptance letter + program page', True), ('submit by Sep 24', True)]),
    ('p', 'submitted Sep 24 11:20am PT.'),
])

n = g.finish()
