"""Synthetic Notion data for David Barron (PERSON.md): a Notion "Export -> Markdown & CSV", unzipped.

Layout: synthetic/notion/David's Notion/...  Pages are `Title <32-hex>.md`; a page with subpages has a sibling folder
`Title <32-hex>/`; databases export as `DB <id>.csv` (the view) and `DB <id>_all.csv` (all properties) plus a folder of
row pages. Personal workspace pages sit at the top; the shared teamspace lives under `Mathetic HQ <id>/`.
Every file is its own item (generic itemizer), so every .md and .csv gets a label.
"""
import os, re, sys, csv, io, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('notion')
WS = "David's Notion"
PERS = "David's Notion"
TEAM = "David's Notion / Mathetic HQ (teamspace)"
NEAR_DUP = 'HARD CASE: near-duplicate — Notion exports both the view CSV and the _all CSV of the same database'
ONE_TOOL = 'HARD CASE: project in only one tool — the hint-timing pilot exists only in this Notion database'
VAGUE = 'HARD CASE: vague title — '


def nd(s):
    return dt(s).strftime('%B %-d, %Y %-I:%M %p')


def ndate(s):
    return dt(s).strftime('%B %-d, %Y')


def clean(t):
    return ''.join(c for c in t if c not in '/\\:?*"<>|').strip()


class N:
    """A page or database in the export tree."""
    def __init__(self, title, seed, parent=None):
        self.title, self.parent = title, parent
        self.id = hexid('notion:' + seed)

    @property
    def name(self):
        return f'{clean(self.title)} {self.id}'

    @property
    def where(self):  # directory that holds this node's .md/.csv
        return self.parent.folder if self.parent else WS

    @property
    def folder(self):  # directory that holds this node's children
        return f'{self.where}/{self.name}'


def link(parent, child, ext='.md', label=None):
    """Relative markdown link from parent's .md to child, as Notion writes it."""
    rel = f'{parent.name}/{child.name}{ext}'
    return f'[{label or child.title}]({urllib.parse.quote(rel)})'


def page(node, created, edited, body, projects, account=PERS, props=(), notes=None, auto_created=True):
    lines = [f'# {node.title}', '']
    bl = body.strip('\n').split('\n')
    lead = []
    while bl and re.match(r'^(Tags|Status): ', bl[0]):
        k, v = bl.pop(0).split(': ', 1); lead.append((k, v))
    body = '\n'.join(bl)
    pl = ([('Created', nd(created))] if auto_created else []) + [(k, v) for k, v in props if v] + lead
    if pl:
        lines += [f'{k}: {v}' for k, v in pl] + ['']
    content = '\n'.join(lines) + '\n' + body.strip('\n') + '\n'
    g.text(f'{node.where}/{node.name}.md', content, created, edited, account=account, project_ids=projects, notes=notes or '')


def database(db, cols_all, cols_view, rows, created, projects, account=PERS, view_filter=None, notes_view=None, notes_all=None):
    """rows: dicts title, seed, props{col: value}, created, edited, body, projects, notes.
    Created / Last edited time columns are filled from the row's dates."""
    out = []
    for r in rows:
        n = N(r['title'], r['seed'], db)
        vals = dict(r['props'])
        vals['Created'] = nd(r['created'])
        vals['Last edited time'] = nd(r['edited'])
        vals['Name'] = r['title']
        props = [(c, vals.get(c, '')) for c in cols_all if c != 'Name']
        page(n, r['created'], r['edited'], r['body'], r['projects'], account=account, props=props, notes=r.get('notes'),
             auto_created=False)
        out.append(vals)
    last = max(dt(r['edited']) for r in rows)

    def csvtext(cols, rs):
        b = io.StringIO()
        w = csv.writer(b, lineterminator='\n')
        w.writerow(cols)
        for v in rs: w.writerow([v.get(c, '') for c in cols])
        return '﻿' + b.getvalue()
    view_rows = [v for v in out if not view_filter or view_filter(v)]
    g.text(f'{db.where}/{db.name}.csv', csvtext(cols_view, view_rows), created, last, account=account, project_ids=projects,
           notes=notes_view or 'database view export (visible columns only)')
    g.text(f'{db.where}/{db.name}_all.csv', csvtext(cols_all, out), created, last, account=account, project_ids=projects,
           notes=notes_all or NEAR_DUP)


# =====================================================================================================================
# Personal workspace
# =====================================================================================================================

gs = N('Getting Started', 'getting-started')
page(gs, '2026-01-26 22:41', '2026-01-26 22:58', """
👋 Welcome to Notion! This page is here to show you around.

## The basics

- [x] Click anywhere on the page and start typing
- [x] Type `/` to add headings, to-dos, tables, toggles, images and more
- [x] Select some text to bold it, link it, or turn it into a comment
- [ ] Drag the `⋮⋮` handle next to any block to move it somewhere else
- [ ] Add a page from the sidebar with `+ New page`
- [ ] Browse `Templates` for ready-made pages (meeting notes, reading lists, trackers)
- Toggle blocks hide extra detail until you click them
    - Like this one. Put long explanations inside toggles to keep pages short.

## Tips

<aside>
💡 Press `Cmd + P` to search every page in your workspace.

</aside>

- Share a page from the `Share` menu in the top right.
- Every page can hold subpages, so you can nest as deep as you want.
- Turn on dark mode with `Cmd + Shift + L`.

---

ok trying this for real this time. plan: reading list + company wiki + weekly planner in here, see if it sticks past february
""", ['project_none'], notes='default onboarding page, lightly edited')

hab = N('Habit tracker', 'habit-tracker')
page(hab, '2026-01-26 23:05', '2026-02-14 23:52', """
Tags: personal

Four habits, two weeks, then decide if this is worth the overhead.

| Day | Asleep by 1am | Read 20 min (not papers) | No phone first hour | 1 chess puzzle set |
| --- | --- | --- | --- | --- |
| Mon Jan 26 | No | Yes | No | Yes |
| Tue Jan 27 | Yes | Yes | Yes | Yes |
| Wed Jan 28 | No | No | No | No |
| Thu Jan 29 | No | Yes | Yes | Yes |
| Fri Jan 30 | Yes | Yes | No | Yes |
| Sat Jan 31 | No | No | No | Yes |
| Sun Feb 1 | Yes | Yes | Yes | No |
| Mon Feb 2 | No | No | No | Yes |
| Tue Feb 3 | Yes | Yes | No | Yes |
| Wed Feb 4 | Yes | No | Yes | No |
| Thu Feb 5 | No | Yes | No | Yes |
| Fri Feb 6 | No | No | No | No |
| Sat Feb 7 | Yes | Yes | Yes | Yes |
| Sun Feb 8 | No | No | No | No |

Score: sleep 6/14, reading 8/14, phone 5/14, chess 10/14.

Verdict (Feb 14): the chess one sticks because it's fun. the phone one never will. sleep failed on every night I worked on the Papert Lab doc, which is the actual problem. stopping the tracker, keeping the puzzles.
""", ['project_none'])

# ---- Weekly planner -------------------------------------------------------------------------------------------------
wp = N('Weekly planner', 'weekly-planner')
w1 = N('Week of Jan 26', 'week-jan-26', wp)
w2 = N('Week of Feb 2', 'week-feb-2', wp)
page(wp, '2026-01-26 23:30', '2026-02-08 22:15', f"""
Tags: planning

Sunday night routine: dump everything, pick 3, put them on the calendar, ignore the rest.

{link(wp, w1)}

{link(wp, w2)}

<aside>
📌 Rule: if it isn't one of the 3, it waits until Friday.

</aside>
""", ['project_ise6664_affective_computing', 'project_dynamite', 'project_mathetic_company', 'project_tutortrace'],
     notes='index page for two weekly plans that mix several projects')

page(w1, '2026-01-26 23:36', '2026-01-31 21:10', """
Tags: planning

## Top 3

1. ISE 6664 reading response #2 (Picard ch. 2 + the emotion-in-learning review) — due Thu 11:59
2. Dynamite: rerun HDBSCAN with `min_cluster_size=15` on all 3,100 posts and start checking the LLM cluster labels
3. Write up the notebook idea properly so Hudson can react to it (started Wed night, it's called "Papert Lab notebook" for now)

## Schedule

| Day | Morning | Afternoon | Evening |
| --- | --- | --- | --- |
| Mon | Z2 run 60' | Dynamite embeddings rerun | ISE reading |
| Tue | lab meeting 10:00 | ISE 6664 lecture 2:00 | bike 75' |
| Wed | Z2 run 50' | Dynamite labels | notebook idea doc |
| Thu | elliptical 45' | ISE 6664 lecture 2:00, response due | — |
| Fri | 1:1 with Yan 11:00 | TutorTrace kappa script | off |
| Sat | long run 1:35 | — | chess / reading |
| Sun | bike 90' | plan next week | — |

## Everything else (Friday or never)

- [x] renew VT parking permit for spring
- [x] cancel Cursor Pro (trial is over, not worth it)
- [ ] reply to Xiaohang about the labeling guide v3 diff
- [ ] book dentist
- [x] move reading list into Notion

## How it went (Sat)

Dynamite rerun took 40 min on the lab box instead of 8 because I forgot the embeddings cache. 41 clusters again, good, stable. Got through 23 of 41 labels; 4 of the LLM labels are wrong in an obvious way (it named two clusters after the same week's assignment). ISE response submitted Thu at 11:40. The Papert Lab doc ate Wed night and Thu night. Training was 9 h, fine.
""", ['project_ise6664_affective_computing', 'project_dynamite', 'project_mathetic_company', 'project_engelbart',
      'project_tutortrace', 'project_endurance_training'], notes='weekly plan spanning several projects')

page(w2, '2026-02-01 22:15', '2026-02-07 23:48', """
Tags: planning

## Top 3

1. Share the Notion with Hudson (Mon) and agree who owns what
2. ISE 6664: team is me + Maya Torres + Jordan Lee. Pick the project topic by Thu. Current favourite: frustration signals in AI-tutoring transcripts
3. Dynamite: finish the remaining 18 cluster labels and write the method paragraph

## Schedule

| Day | Main thing | Training |
| --- | --- | --- |
| Mon | Hudson call 2:00, Notion setup | Z2 run 55' |
| Tue | ISE lecture, team meeting after | bike 75' |
| Wed | Dynamite labels | Z2 run 60' |
| Thu | ISE topic due | elliptical 40' |
| Fri | Yan 1:1 — bring the TutorTrace kappa numbers (0.71 across 3 raters) | off |
| Sat | write | long run 1:40 |
| Sun | plan | bike 90' |

## Other

- [x] email Dr. Brooks our topic + team names
- [x] fix the kappa script (was counting the calibration windows twice)
- [ ] UIST: outline the related work section, it's 7 weeks out
- [ ] read Papert ch. 1 for reading group
- [ ] grocery run

## Review

All 41 Dynamite labels checked: 6 relabelled, 2 merged. ISE topic approved by Brooks on Thu with a note to scope the transcripts to one tutoring system. UIST outline did not happen, moving it to next week's top 3.
""", ['project_ise6664_affective_computing', 'project_dynamite', 'project_mathetic_company', 'project_tutortrace',
      'project_endurance_training'], notes='weekly plan spanning several projects')

# ---- Training dashboard ---------------------------------------------------------------------------------------------
tr = N('Training dashboard', 'training-dashboard')
z2 = N('Zone 2 HR drift log', 'z2-drift', tr)
page(tr, '2026-01-27 07:02', '2026-04-19 18:30', f"""
Tags: running, base

<aside>
🏃 Base phase (Block 2, Jan–Apr 2026). Target 9–11 h/week aerobic. Max 2 sessions/week above Z2, and only strides or short hills. Long run builds to 2:00 by mid-March.

</aside>

## Zones (from the Dec 2025 lab-style test on the treadmill)

| Zone | HR | Feel |
| --- | --- | --- |
| Z1 | < 132 | recovery, walk breaks fine |
| Z2 | 132–152 | nose-breathing, could talk in full sentences |
| Z3 | 153–165 | "grey zone", avoid |
| Z4 | 166–178 | threshold, not in this block |
| Z5 | > 178 | strides only |

## Weekly log

| Week of | Run h | Bike h | Elliptical h | Total h | Long run | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Jan 26 | 5.5 | 2.0 | 1.5 | 9.0 | 1:35 | snow Tue/Wed → elliptical |
| Feb 2 | 6.0 | 2.5 | 1.0 | 9.5 | 1:40 | |
| Feb 9 | 6.0 | 3.0 | 0.5 | 9.5 | 1:45 | |
| Feb 16 | 4.0 | 2.0 | 1.0 | 7.0 | 1:20 | down week |
| Feb 23 | 6.5 | 3.0 | 1.0 | 10.5 | 1:50 | |
| Mar 2 | 6.5 | 3.5 | 0.5 | 10.5 | 1:50 | strides x2 |
| Mar 9 | 7.0 | 3.0 | 1.0 | 11.0 | 2:00 | first 2h run since November |
| Mar 16 | 4.5 | 2.0 | 1.0 | 7.5 | 1:25 | down week |
| Mar 23 | 4.0 | 1.5 | 1.5 | 7.0 | 1:15 | UIST crunch, slept 5h most nights |
| Mar 30 | 3.0 | 1.0 | 1.0 | 5.0 | — | deadline week, survival mode |
| Apr 6 | 6.0 | 3.0 | 0.5 | 9.5 | 1:45 | back to normal |
| Apr 13 | 6.5 | 3.0 | 0.5 | 10.0 | 1:50 | |

## Rules I keep breaking

- Easy days drift into Z3 on the hill back from the Huckleberry trail. Walk the hill if HR > 152.
- Don't stack the long run the day after a bike > 90'.
- Down week every 4th week even if I feel good.

## Next

- [ ] Block 3 (May–Jul): same volume, add 1 steady session at top of Z2
- [ ] Pick a fall half. Owen wants a Bay Area one in October if I'm out there by then
- [x] new shoes at 450 miles (done Mar 2)

{link(tr, z2)}
""", ['project_endurance_training'])

page(z2, '2026-02-03 08:10', '2026-03-29 10:05', """
Tags: running

Aerobic decoupling on steady Z2 runs: compare avg HR first half vs second half at roughly the same pace. Under 5% = aerobic base is fine at that pace.

| Date | Duration | Avg pace | HR 1st half | HR 2nd half | Drift | Conditions |
| --- | --- | --- | --- | --- | --- | --- |
| Feb 3 | 60' | 8:45/mi | 141 | 149 | 5.7% | 28°F, windy |
| Feb 10 | 60' | 8:40/mi | 140 | 147 | 5.0% | |
| Feb 17 | 50' | 8:50/mi | 138 | 143 | 3.6% | down week |
| Feb 24 | 70' | 8:38/mi | 141 | 148 | 5.0% | last 10' uphill |
| Mar 3 | 70' | 8:32/mi | 140 | 145 | 3.6% | new shoes |
| Mar 10 | 75' | 8:30/mi | 139 | 144 | 3.6% | |
| Mar 17 | 60' | 8:29/mi | 138 | 142 | 2.9% | |
| Mar 28 | 50' | 8:55/mi | 146 | 154 | 5.5% | 5h sleep, ignore |

Takeaway: 8:30/mi is now properly aerobic. The bad ones line up with bad sleep, not with mileage. Next check: can 8:15 hold under 5%?
""", ['project_endurance_training'])

# ---- Juno graveyard -------------------------------------------------------------------------------------------------
juno = N('Juno graveyard', 'juno-graveyard')
page(juno, '2026-02-07 00:20', '2026-02-07 01:05', """
Tags: archive, juno

Everything I built for Juno (2023–2025) and why each piece died. Writing it down so I stop reopening the repos at 1am.

<aside>
🪦 Juno = customizable AI voice agents ("conversational entities") you could give a persona, a voice and a memory. CLI first, then a lab web app, then a browser extension.

</aside>

## The graves

- **juno CLI** (spring 2023 → fall 2023)
    - What it was: `juno new --persona tutor --voice warm` spun up a voice agent in the terminal; push-to-talk with the space bar.
    - Cause of death: latency. 2.5–4 s round trip (STT → LLM → TTS) made every conversation feel like a bad phone line. Streaming TTS helped but never got under 1.5 s.
    - Salvage: the persona YAML format was actually nice.
- **Juno lab web app** (2024)
    - What it was: a web page where PRIME Lab people could build agents and share a link with study participants.
    - Cause of death: nobody wanted a generic agent builder; every study needed something custom, and I became the custom-builder.
    - Salvage: the transcript viewer with per-turn timing.
- **browser extension** (early 2025)
    - What it was: talk to any webpage; agent reads the DOM and answers questions about it.
    - Cause of death: Chrome Web Store review rejected it twice for broad host permissions; by the time I narrowed them every big lab shipped the same thing.
    - Salvage: nothing really. maybe the "explain this paragraph" shortcut.
- **memory layer** (never shipped)
    - Agents were supposed to remember past chats with a user. Ended up as a JSON file per user that grew forever.
    - Cause of death: I never figured out what was worth remembering. This is the part I keep thinking about.

## What I learned

1. Voice is a delivery format, not the product. People came for the persona and left because of latency.
2. Building a platform before having one user with one real job to do = graveyard.
3. The memory question (what should a tool remember about how you think) is still the interesting one. → maybe the notebook idea is the real version of it.

## Don't

- [ ] don't revive the CLI
- [ ] don't port the extension to MV3 "just to see"
""", ['project_juno'], notes='retrospective on the older Juno project; mentions the notebook idea only in passing')

# ---- TACode handoff -------------------------------------------------------------------------------------------------
tac = N('TACode — handoff (archived)', 'tacode-handoff')
page(tac, '2026-01-30 15:40', '2026-01-30 16:25', """
Tags: archived, PRIME Lab
Status: Archived

Moved here from the handoff email thread in November 2025 so it lives somewhere searchable. I'm no longer on TACode; Rezky owns the backend and Yue owns the frontend as of 2025-11-14.

## Repos

| Repo | What | Owner now | State at handoff |
| --- | --- | --- | --- |
| `tacode` | React frontend: TA queue view, student code viewer, suggested-feedback panel | Yue | builds, 3 open PRs |
| `tacode_backend` | FastAPI + Postgres; queue, sessions, LLM feedback drafts | Rezky | deployed on the lab VM, nightly backup cron |

## How to run it locally

1. `docker compose up db` (Postgres 15)
2. `cd tacode_backend && uv sync && uv run alembic upgrade head && uv run uvicorn app.main:app --reload`
3. `cd tacode && pnpm i && pnpm dev` (expects the API on :8000)
4. Keys: the LLM key and the Canvas token are in the lab password vault under "TACode", **not** in `.env.example`.

## Known issues (as of handoff)

- Feedback drafts sometimes quote the wrong file when a student has two files with the same name in different folders (keyed by basename, should be full path).
- Queue position jumps when a TA reassigns a ticket; the websocket sends the old index. Repro in issue #41.
- Canvas roster sync fails silently if a section has zero students; add a log line.
- Alembic migration 0012 is not reversible. Don't downgrade past it.

## Decisions we made and why

- TAs approve every LLM draft before a student sees it. Non-negotiable after the pilot where one draft gave away the solution.
- No student code leaves the lab VM except the snippet sent to the model; we strip names and emails first.

## Open questions I left for Rezky and Yue

- Whether to keep the "suggested next hint" button or drop it (TAs said it was noisy).
- Whether to migrate off the lab VM before spring.

---

Archived 2026-01-30. Not touching this again unless someone asks.
""", ['project_tacode'])

# ---- vague pages ----------------------------------------------------------------------------------------------------
notes_pg = N('Notes', 'notes-page')
page(notes_pg, '2026-02-05 21:30', '2026-02-05 21:58', """
call w hudson, pricing + who it's for

- who is the first user. grad students in our lab-like situations: lots of chats, papers, notes all over the place
- hudson: labs won't pay for a notebook, individuals might. or the advisor pays for the lab
- me: $12/mo individual? lab seat? too early, he's right
- the thing people will pay for = "I don't have to re-find where I read that"
- interviews: need 10 by end of feb. have 3 scheduled. ask Minsun + Xiaohang if they'd do 20 min
- hudson does the landing page copy, I do the prototype
- don't build sync yet. local first.
- name still bad. "Papert Lab notebook" is a placeholder

todo
- [ ] interview guide v1 (in HQ)
- [ ] list 15 people to ask
- [ ] find the Licklider "85% clerical" bit for the pitch, it's the whole argument
""", ['project_mathetic_company', 'project_engelbart'],
     notes=VAGUE + 'page called "Notes" holds a pricing/first-user call with Hudson (company)')

unt1 = N('Untitled', 'untitled-1')
page(unt1, '2026-02-08 19:02', '2026-02-08 19:09', """
chicken thighs 3 lb
greek yogurt x2 (big tubs)
rice 5 lb
frozen broccoli x3
oats
eggs 18
bananas
cottage cheese
salsa

sunday prep: 2 trays thighs + broccoli, rice cooker x2, portion into 8
""", ['project_none'], notes=VAGUE + '"Untitled" page that is a grocery / meal-prep list (personal clutter)', auto_created=False)

unt2 = N('Untitled', 'untitled-2')
page(unt2, '2026-01-31 00:44', '2026-01-31 01:10', """
licklider thoughts before thursday

- symbiosis is not automation. he's explicit that the machine does the routinizable work and the human sets goals + judges. the interesting middle is the "real time" coupling
- his self-observation: most of his "thinking" time went to getting into a position to think (finding, plotting, converting). redo that on myself for a week? log every time I'm searching for something I already read
- 1960 assumption: the bottleneck is the computer's speed. 2026: the bottleneck is that my stuff is in 9 apps
- question for group: is an LLM chat closer to his "symbiosis" or to the clerical assistant he wanted to get rid of?
- question 2: he wanted shared, reliable memory between human and machine. where's that today? (it's nowhere, that's the point of the notebook thing)

bring: printed copy, the Bush comparison table from last week
""", ['project_augmenting_cognition_reading_group'],
     notes=VAGUE + 'second "Untitled" page (different id) holding reading-group prep on Licklider', auto_created=False)

# ---- personal clutter pages -----------------------------------------------------------------------------------------
tax = N('Taxes 2025', 'taxes-2025')
page(tax, '2026-03-14 11:20', '2026-04-11 16:45', """
Tags: admin

## Documents

- [x] W-2 from Virginia Tech (GRA) — in the HokieSpa tax forms tab
- [x] 1098-T — mostly irrelevant, tuition is covered by the waiver
- [x] 1099-INT from the high-yield savings account
- [x] last year's return PDF for the carryover numbers
- [ ] ~~1099-NEC~~ no freelance this year

## Federal

- Filing single, standard deduction.
- The summer stipend from the lab was on the W-2 already, nothing separate.
- Retirement savers credit? no — student.

## Virginia

- Full-year resident 2025. Same software handles the state return.
- Check the VA 529 deduction question: n/a.

## Notes for next year

- 2026 is going to be weird: part-year VA (until August), part-year California after the move. Keep the move date (Aug 8) and the first SF pay stub.
- If Mathetic pays me anything in 2026 that's a different form. Ask Hudson's accountant friend.

## Status

- Mar 14: gathered everything
- Apr 4: federal + VA drafted, both small refunds
- Apr 11: submitted both. waiting on acceptance emails.
""", ['project_none'])

geo = N('Geopolitics reading notes', 'geopolitics-notes')
page(geo, '2026-02-21 22:10', '2026-03-15 23:40', """
Tags: reading, strategy

Running notes. My own summaries, not quotes.

## Themes I keep coming back to

- **Power transition vs. peaking power.** Two stories about US–China: the rising power gets impatient (classic transition story), or the challenger peaks and acts while its window is still open. The second one is scarier and I find it more convincing after the demographic chapters.
- **Geography as the slow variable.** Rivers, coastlines and chokepoints don't change; everything else is noise on top. The Malacca Strait comes up in every book.
- **Alliances as infrastructure.** Treaties matter less than whether militaries have actually trained together; interoperability is the real asset.
- **Grand strategy = matching ends to means.** Every failure in Gaddis is someone with infinite aims and finite means.

## Questions

- How much of the "window closing" argument is just reading demographic charts backwards?
- Is semiconductor supply chain policy strategy or industrial policy wearing a costume?
- Why do the July 1914 accounts all make it sound inevitable in hindsight but contingent day by day?

## Log

- Feb 21: started Freedman, skipped ahead to the chapters on the Cold War
- Feb 28: finished the Clark book on 1914, the chapter on the Balkan crisis is the best thing I've read this year
- Mar 8: Brands & Beckley — read half, too repetitive
- Mar 15: notes above cleaned up; going quiet until UIST is in
""", ['project_none'])

rec = N('Recipes to try', 'recipes-to-try')
page(rec, '2026-02-01 18:30', '2026-03-01 19:12', """
Tags: food

Target: ~160 g protein/day without hating life. Everything here should batch to 6–8 portions.

| Recipe | Protein / portion | Time | Tried? | Verdict |
| --- | --- | --- | --- | --- |
| Sheet-pan chicken thighs + broccoli + rice | 42 g | 50 min | Yes | default, boring, works |
| Turkey chili (2 lb turkey, 3 cans beans) | 38 g | 1 h | Yes | great frozen |
| Greek yogurt overnight oats | 30 g | 5 min | Yes | breakfast every day now |
| Beef + lentil bolognese | 35 g | 1 h 15 | Feb 22 | too heavy for weekdays |
| Egg + cottage cheese bake | 28 g | 40 min | No | |
| Salmon rice bowls | 34 g | 30 min | No | expensive |
| Chicken tikka (yogurt marinade) | 40 g | 1 h + marinade | Mar 1 | make double next time |

## Notes

- Rice cooker twice on Sundays covers the week.
- Freeze 3 of the 8 chili portions immediately or I eat them by Wednesday.
- Spice drawer is low on cumin + smoked paprika.
""", ['project_none'])

subs = N('Subscriptions audit', 'subscriptions-audit')
page(subs, '2026-01-31 13:05', '2026-01-31 13:40', """
Tags: money

| Service | $/mo | Use it? | Decision |
| --- | --- | --- | --- |
| ChatGPT Plus | 20 | daily | keep |
| Claude Pro | 20 | daily | keep (maybe Max later) |
| Cursor Pro | 20 | trial over Jan 20, back to Claude Code | **cancel** ✅ |
| Spotify | 11.99 | daily | keep |
| iCloud 200 GB | 2.99 | yes | keep |
| Strava | 11.99 | weekly | keep, the training log export is useful |
| Chess.com Diamond | 9.99 | puzzles only | **cancel**, lichess puzzles are free |
| NYT | 4 (promo) | rarely | cancel before promo ends Mar 3 |
| Notion | 0 | new | free plan is enough for now |
| Overleaf | 0 | VT has the pro license | — |

Savings: ~$34/mo.

- [x] cancel Cursor
- [x] cancel Chess.com
- [ ] set a reminder for NYT (Mar 1)
""", ['project_none'])

car = N('Car — registration + insurance', 'car-reg')
page(car, '2026-02-24 09:40', '2026-03-03 12:15', """
Tags: admin

## Registration (Virginia)

- Renewal due **Mar 31**. DMV online renewal, 2 years.
- Emissions inspection not needed in Montgomery County.
- [x] renewed Mar 3, sticker comes in the mail

## Insurance

- Current policy renews Apr 15. Got two other quotes:
    - quote A: 6-month, same coverage, ~8% cheaper but higher deductible
    - quote B: about the same as current
- Decision: stay, ask about the good-student discount (they said grad students count with a transcript).

## If I move to SF this summer

- California wants the car registered within 20 days of becoming a resident; needs a smog check.
- Honestly might sell the car instead. Parking near the house is a nightmare from what Hudson says.
- [ ] decide by July
""", ['project_none'])

chess = N('Chess study plan', 'chess-plan')
page(chess, '2026-02-15 22:30', '2026-02-19 23:05', """
Tags: chess

Rapid (lichess) 1480 → goal 1600 by summer. 30 min/day max, it's a break, not a project.

## Repertoire

- **White:** London. Stop playing the early h4 nonsense. Learn the plan vs the Kings Indian setup (c3, h3, Be2, O-O, then e4).
- **Black vs 1.e4:** Caro-Kann. Advance variation is where I lose; learn the ...c5 break and when to play ...Qb6.
- **Black vs 1.d4:** Queens Gambit Declined. Fine already.

## Weekly

| Day | What |
| --- | --- |
| Mon/Wed/Fri | 20 puzzles (lichess, rated) |
| Tue/Thu | 1 annotated game from my own losses |
| Sat | 3 rapid games 15+10, no blitz |
| Sun | endgame drill: rook endings (Lucena, Philidor) |

## Patterns from my last 30 losses

- 11 lost from time trouble in winning positions → 15+10 only
- 7 hung a piece in the first 15 moves → blunder check before every move, out loud if needed
- 5 lost rook endings that were draws → that's the Sunday drill

## Progress

- Feb 19: 1503. two clean Caro-Kann wins.
""", ['project_none'])

bike = N('Bike — rear derailleur skipping', 'bike-derailleur')
page(bike, '2026-03-08 14:15', '2026-03-11 18:40', """
Tags: bike

## Symptom

- Skips on cogs 3–5 under load (climbing), fine on the big cogs.
- Started after the bike fell over at the rack on Mar 6.

## Tried

- [x] barrel adjuster: quarter turns out (looser) → worse; two quarter turns in → better on 3 and 4, still skips on 5
- [x] cleaned + lubed chain
- [x] checked chain wear: 0.5% on the gauge, fine
- [ ] hanger alignment — no tool, and the derailleur looks a bit tilted from behind

## Result

Took it to the shop downtown Mar 10. Hanger was bent. They straightened it and re-indexed; $35. Picked up Mar 11, no skipping on a 40' test ride.

Note to self: buy a spare hanger (model-specific) before the next bike trip. Rode the trainer in the meantime.
""", ['project_none'])

park = N('VT parking ticket appeal', 'parking-appeal')
page(park, '2026-02-04 10:05', '2026-02-12 16:20', """
Tags: admin

- Citation #26-118804, Feb 3, 9:52 am, Perry Street lot
- Reason on ticket: "no valid permit displayed"
- Reality: spring permit was bought Jan 29, the hang tag hadn't arrived; the plate was registered to the permit online

## Appeal text (submitted Feb 4)

> I purchased a spring 2026 graduate permit on January 29; the hang tag had not been mailed yet, but my plate was linked to the permit in the parking portal at the time of the citation. Screenshot of the purchase confirmation attached. I'd ask that the citation be voided.

## Status

- Feb 4: submitted with screenshot
- Feb 12: **approved**, citation voided 🎉
- Hang tag arrived Feb 9
""", ['project_none'])

dub = N('Dublin trip — Niamh wedding', 'dublin-trip')
page(dub, '2026-03-18 21:40', '2026-04-05 22:10', """
Tags: travel, family

Cousin Niamh's wedding in Dublin, Saturday **July 11, 2026**. Logistics only here.

## RSVP

- [x] RSVP'd yes for 1 (Mar 18, via their website)
- [x] dietary: none
- [ ] gift — they have a registry, pick something by June

## Flights (Roanoke or DC?)

| Option | Route | Out | Back | Notes |
| --- | --- | --- | --- | --- |
| A | IAD → DUB direct | Wed Jul 8 eve | Tue Jul 14 | best times, priciest |
| B | ROA → CLT → DUB | Wed Jul 8 | Mon Jul 13 | one stop, cheaper |
| C | IAD → DUB | Thu Jul 9 | Sun Jul 12 | too tight with jet lag |

Leaning A. Drive to IAD, park at the economy lot.

## Stay

- Family is putting people up near the venue; I'm in a B&B 10 min walk away, booked Apr 5 (free cancellation until Jun 30).

## Conflicts to check

- NeurIPS rebuttal window is late July, should be clear by then
- UIST rebuttal is mid June, fine
- Passport expires 2028, fine
""", ['project_none'], notes='family logistics only (personal clutter)')

pod = N('Podcast + listening queue', 'podcast-queue')
page(pod, '2026-04-02 23:15', '2026-04-02 23:31', """
Tags: personal

- [ ] the episode on the history of the Strait of Hormuz everyone keeps linking
- [ ] the long interview with the chess coach on how adults should study (Owen sent it)
- [ ] running physiology episode on polarized vs pyramidal training
- [x] the one on semiconductor export controls
- [ ] whatever the next Dwarkesh episode is

for long runs: 1:30+ only, otherwise music
""", ['project_none'])

gifts = N('Gift ideas', 'gift-ideas')
page(gifts, '2026-03-01 12:30', '2026-03-22 20:05', """
Tags: personal

| For | Occasion | Idea | Budget | Done |
| --- | --- | --- | --- | --- |
| Mom | birthday (May) | framed print from the Dragon's Tooth hike photo | 60 | |
| Dad | Father's Day | good bike lights | 50 | |
| Owen | race day thing | nice running socks + a gel sampler | 30 | |
| Niamh + partner | wedding (Jul 11) | something from the registry | 100 | |
| Hudson | when we incorporate | lol a Papert book, Mindstorms first edition if findable | 40 | |
""", ['project_none'])

movies = N('Movies + shows', 'movies-shows')
page(movies, '2026-02-22 21:05', '2026-04-04 23:50', """
Tags: personal

## Watch

- [ ] the new season of that Danish political drama
- [ ] the 1914 documentary series (after finishing the Clark book)
- [ ] Hudson's recommendation, the one about the Xerox PARC people
- [x] the chess one with the Soviet coach (good)

## Watched

| Title-ish | When | Rating /10 |
| --- | --- | --- |
| the Bell Labs documentary | Feb 22 | 8 |
| Oppenheimer rewatch | Mar 7 | 7 |
| the marathon doc about the 2-hour attempt | Apr 4 | 9 |
""", ['project_none'])

lap = N('New Mac setup', 'mac-setup')
page(lap, '2026-08-04 21:15', '2026-08-06 23:40', """
Tags: setup

New MacBook arrived Aug 4. Doing it clean, no Migration Assistant.

## Install

```
brew install git gh uv pnpm node ripgrep fd jq tmux
brew install --cask ghostty raycast obsidian zotero spotify 1password
```

- [x] Xcode command line tools
- [x] dotfiles from github (zshrc, gitconfig, ghostty config)
- [x] ssh key for GitHub (new key, revoke the old laptop's)
- [x] Claude Code + the plugins folder
- [x] Zotero: sign in, let it sync, check the Better BibTeX export path
- [x] Obsidian vaults
- [ ] Overleaf: nothing to install, just check the git bridge token
- [ ] FL Studio: license transfer (deactivate old laptop first!)

## Don't bother

- Notion desktop. haven't opened it since April.
- Cursor.

## Old laptop

- [ ] wipe after Aug 8 (keep until I'm in SF in case something's missing)
""", ['project_none'], notes='straggler page from Aug 2026 (new Mac); mentions Notion abandoned in April')

# ---- Apartment search -----------------------------------------------------------------------------------------------
apt = N('SF apartment search', 'sf-apartment')
apt_v = N('Viewings log', 'sf-viewings', apt)
apt_q = N('Questions to ask', 'sf-questions', apt)
page(apt, '2026-07-14 22:05', '2026-08-12 21:30', f"""
Tags: move, SF

Moving Aug 8. Surplus has a room in the house for the program; this page is about whether to take it or find a sublet nearby.

## Constraints

- Budget: up to **$2,400/mo** for a room or studio sublet, utilities included ideally
- Commute to the Surplus house: ≤ 25 min bike or Muni
- Month-to-month or ≤ 6 months (no idea where we'll be in 2027)
- Somewhere to keep a bike inside
- Close to a park or the Panhandle for Z2 runs

## Neighborhoods

| Area | Pros | Cons |
| --- | --- | --- |
| Mission | near house, food, sunny | loud, bike theft stories |
| Inner Sunset | Golden Gate Park runs, calmer | fog, longer commute |
| Hayes Valley / NoPa | Panhandle, central | priciest |
| Lower Haight | central, cheaper than Hayes | small rooms |

## Sources

- Surplus Slack housing channel (best leads so far)
- Craigslist sublets (lots of scams: never pay a deposit before a video tour)
- friend-of-friend sublets via Hudson

{link(apt, apt_v)}

{link(apt, apt_q)}

## Decision (Aug 2)

Taking the room at the Surplus house for Aug–Oct. Cheaper than every sublet I saw, zero commute, and Sam (other housemate) says the bike room is fine. Revisit in mid-October for a November place.
""", ['project_none'])

page(apt_v, '2026-07-24 20:10', '2026-08-12 21:30', """
Tags: move

| Date | Area | Type | $/mo | Tour | Notes | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Jul 24 | Inner Sunset | room in 3BR | 1,850 | video | nice people, fog, 30 min to house | maybe |
| Jul 25 | Mission | studio sublet | 2,600 | video | over budget, no bike storage | no |
| Jul 27 | Lower Haight | room in 4BR | 1,950 | video | tiny room, great location | maybe |
| Jul 28 | Hayes Valley | room | 2,350 | video | lease through Dec only, landlord wants 3 months up front | no |
| Jul 29 | Mission | room | 1,700 | — | asked for deposit before tour → scam | no |
| Aug 10 | Inner Sunset | (same as Jul 24) | 1,850 | in person | still available for Nov, liked it | keep in mind |

Notes

- The Jul 24 room: housemates are a nurse and a grad student; quiet house; laundry in unit.
- The Lower Haight room fits a bed and nothing else.
- Aug 10: walked the Inner Sunset place after the first week here; 28 min door to door by bike. Told them I'd know by Oct 15.
""", ['project_none'])

page(apt_q, '2026-07-15 09:30', '2026-07-24 19:55', """
Tags: move

Ask every time:

- [ ] Is the rent all-in? Which utilities extra (PG&E, internet)?
- [ ] Deposit amount, and when is it due (never before a tour)
- [ ] Month-to-month allowed after the initial term?
- [ ] Where do bikes go?
- [ ] Is the current tenant subletting with the landlord's OK? (get it in writing)
- [ ] Who else lives there, what are their hours?
- [ ] Laundry: in unit / building / laundromat
- [ ] Heat? (apparently a real question in SF)
- [ ] Earliest move-in, can it be Aug 8–10?
- [ ] Furnished? Desk?
""", ['project_none'])

# ---- Reading list database ------------------------------------------------------------------------------------------
RG = 'project_augmenting_cognition_reading_group'
rl = N('Reading list', 'reading-list')
RL_COLS = ['Name', 'Authors', 'Year', 'Type', 'Status', 'Tags', 'Discussed', 'Rating', 'Created', 'Last edited time']
rl_rows = [
    dict(title='As We May Think', seed='rl-bush', created='2026-01-29 22:10', edited='2026-02-06 00:35',
         props={'Authors': 'Vannevar Bush', 'Year': '1945', 'Type': 'Essay', 'Status': 'Discussed', 'Tags': 'reading group, memex',
                'Discussed': 'January 29, 2026', 'Rating': '⭐⭐⭐⭐⭐'}, projects=[RG], body="""
## My summary

Bush, writing at the end of the war, worries that the record of science has outgrown our ways of consulting it. He imagines the memex: a desk that stores a person's books, notes and photos on microfilm and lets them build "trails" — named, saved chains of linked items — which they can annotate, revisit and hand to someone else.

## What I took from it

- The unit isn't the document, it's the **trail**: the path through documents that produced an idea.
- Association beats indexing. He thinks alphabetical/hierarchical filing is the core problem.
- Trails are shareable artifacts. A researcher could pass a colleague the trail, not just the conclusion.

## Discussion notes (Jan 29)

- Group argued about whether browser history is a degenerate trail (yes but nobody names or curates it).
- Hudson: the memex is a single-user tool; collaboration is bolted on.
- Me: the missing piece is provenance — which source did a thought actually come from. That's the thing I keep wanting for my own work.

## Follow-ups

- [ ] compare the memex trail to Engelbart's links in the 1962 report next week
""", notes='reading-group summary (own words)'),
    dict(title='Man-Computer Symbiosis', seed='rl-licklider', created='2026-01-29 22:14', edited='2026-02-06 00:41',
         props={'Authors': 'J. C. R. Licklider', 'Year': '1960', 'Type': 'Paper', 'Status': 'Discussed', 'Tags': 'reading group',
                'Discussed': 'February 5, 2026', 'Rating': '⭐⭐⭐⭐'}, projects=[RG], body="""
## My summary

Licklider proposes a partnership where humans set goals, form hypotheses and judge results while computers do the routine work in between, fast enough to be part of the thinking rather than a batch job afterward. He lists what's missing to get there: time-sharing, memory, natural-ish languages, displays and input.

## Notes

- His informal time study of himself is the most useful part: most of his "thinking" hours went to preparing to think.
- He treats symbiosis as an interim stage before machines might do more on their own. Reads differently in 2026.
- The requirements list (speed, memory organization, language, I/O) is basically a roadmap of the next 30 years.

## Discussion (Feb 5)

- Is an LLM chat symbiosis or the clerk he wanted to offload? We split 3–3.
- Agreed that "shared memory between person and machine" is still the unsolved one.
""", notes='reading-group summary (own words)'),
    dict(title='Augmenting Human Intellect: A Conceptual Framework', seed='rl-engelbart', created='2026-01-30 09:20', edited='2026-02-13 23:58',
         props={'Authors': 'Douglas C. Engelbart', 'Year': '1962', 'Type': 'Report', 'Status': 'Discussed', 'Tags': 'reading group, H-LAM/T',
                'Discussed': 'February 12, 2026', 'Rating': '⭐⭐⭐⭐⭐'}, projects=[RG], body="""
## My summary

Engelbart frames intelligence as a system: a human plus language, artifacts, methodology and training (H-LAM/T). Improving any part changes what the whole system can think. He argues for "bootstrapping": build tools that make the toolbuilders more effective, then use those to build the next tools.

## Notes

- The long hypothetical with the architect working at a display is a surprisingly concrete UI spec for 1962.
- Augmentation ≠ automation. The point is raising the ceiling on hard problems, not doing easy ones faster.
- The system view means a tool that ignores the person's existing methods won't stick. Relevant to anything that wants to slot into someone's research habits.

## Discussion (Feb 12)

- Long one. We spent 40 minutes on bootstrapping and whether a small team can actually do it.
- Hudson pointed out he's naming the problem we're working on, and maybe the product.

## Quotes to find later

- the "co-evolution" of tools and methods passage, for the pitch deck (keep it short)
""", notes='reading-group summary (own words)'),
    dict(title='Mindstorms: Children, Computers, and Powerful Ideas', seed='rl-papert', created='2026-02-03 21:45', edited='2026-02-20 22:30',
         props={'Authors': 'Seymour Papert', 'Year': '1980', 'Type': 'Book', 'Status': 'Discussed', 'Tags': 'reading group, mathetics',
                'Discussed': 'February 19, 2026', 'Rating': '⭐⭐⭐⭐'}, projects=[RG], body="""
## My summary

Papert argues children learn best by building things they care about with a computer as a medium (Logo, the turtle), and that learning should be studied as its own craft. He uses "mathetics" for the study of learning, as opposed to didactics, the study of teaching.

## Notes

- "Debugging" as a positive learning stance: mistakes are information, not failure.
- Objects-to-think-with: the turtle lets a kid use their own body knowledge to reason about geometry.
- Mathetics is a good word. Hudson and I both lit up at it. (company name?)

## Discussion (Feb 19)

- Is "constructionism" just project-based learning with better branding? Group said no, it's about the medium.
- Me: AI tutors that hand out answers are the opposite of debugging-as-learning.
""", notes='reading-group summary (own words)'),
    dict(title='Personal Dynamic Media', seed='rl-kay', created='2026-02-20 22:40', edited='2026-03-05 21:15',
         props={'Authors': 'Alan Kay, Adele Goldberg', 'Year': '1977', 'Type': 'Paper', 'Status': 'Discussed', 'Tags': 'reading group, dynabook',
                'Discussed': 'March 5, 2026', 'Rating': '⭐⭐⭐'}, projects=[RG], body="""
## My summary

Kay and Goldberg describe the Dynabook vision and the interim Smalltalk systems at PARC: a personal computer as a medium that people of all ages can shape, with examples of kids and adults building their own tools (animation, music, drawing).

## Notes

- Strong on "the user should be able to make their own tools", weak on how a non-programmer actually gets there.
- The examples are all creative media. Nothing about research or managing what you've read.

## Discussion (Mar 5)

- Short session, three of us. Last one before UIST; group pauses until mid-April.
""", notes='reading-group summary (own words)'),
    dict(title='Productive Struggle or Silent Stalling? Telemetry Signals of Help-Seeking in LLM-Assisted CS1', seed='rl-ostrowski',
         created='2026-03-26 01:20', edited='2026-03-27 00:05',
         props={'Authors': 'Hannah Ostrowski, Mateo Lindqvist, Aisha Bello, Ravi Chandrasekar', 'Year': '2025', 'Type': 'Paper',
                'Status': 'Read', 'Tags': 'related work, TutorTrace', 'Rating': '⭐⭐⭐⭐'}, projects=['project_tutortrace', RG], body="""
## Why it's here

Closest prior work to TutorTrace. Need it in related work before the UIST deadline (Mar 31).

## Summary

L@S '25 paper. Instrumented a CS1 course (N=212) with editor + assistant telemetry; four TAs labeled 1,904 thirty-second windows as productive struggle / stalling / help-seeking / off-task. A gradient-boosted classifier hits 0.71 macro-F1 (0.69 in the arXiv v1). Repeated near-identical prompts and long idle gaps after a failed run predict stalling.

## How we differ

- They label 4 states; we have the finer state set incl. "stalled-after-error" from labeling guide v3.
- Their kappa is 0.64 on a 10% overlap; ours is 0.71 across 3 raters. Say this carefully, different label sets.
- They report a leakage-style number (windows from the same student in train and test) — cite it in our evaluation section as precedent for grouped splits.

## To do

- [x] add bib entry to the Overleaf (`ostrowski2025productive`)
- [ ] make sure we cite the camera-ready, not the arXiv v1 — numbers differ
""", notes='the fictional Ostrowski 2025 paper as a reading-list row (also appears in zotero/pdfs/gmail/etc.)'),
    dict(title='Strategy: A History', seed='rl-freedman', created='2026-02-21 22:05', edited='2026-03-01 23:10',
         props={'Authors': 'Lawrence Freedman', 'Year': '2013', 'Type': 'Book', 'Status': 'Reading', 'Tags': 'strategy, personal'},
         projects=['project_none'], body="""
Personal reading, not group.

- Huge. Reading the military and Cold War parts, skimming business strategy.
- Useful idea: strategy as a story you tell about how you get from here to there, which keeps getting rewritten as things happen.
- Stalled at ~40% (Mar 1). Maybe finish in summer.
"""),
    dict(title='The Sleepwalkers', seed='rl-clark', created='2026-02-07 21:30', edited='2026-02-28 22:45',
         props={'Authors': 'Christopher Clark', 'Year': '2012', 'Type': 'Book', 'Status': 'Done', 'Tags': 'history, personal', 'Rating': '⭐⭐⭐⭐⭐'},
         projects=['project_none'], body="""
How Europe went to war in 1914.

- Best part: refuses to find one guilty party; shows each capital acting on partial information and worst-case readings of the others.
- The Balkan chapters are dense but worth it.
- Finished Feb 28. Recommend to Owen.
"""),
    dict(title='Danger Zone', seed='rl-brands', created='2026-03-08 20:00', edited='2026-09-20 22:15',
         props={'Authors': 'Hal Brands, Michael Beckley', 'Year': '2022', 'Type': 'Book', 'Status': 'Abandoned', 'Tags': 'US-China, personal', 'Rating': '⭐⭐'},
         projects=['project_none'], body="""
- The peaking-power argument: a rising challenger may act before its window closes.
- Half the book makes the argument, the second half repeats it. Stopped at ch. 5 (Mar 8).
- Sep 20: saw a long thread arguing the demographic data was cherry-picked; marking abandoned for good.
""", notes='straggler edit Sep 2026'),
    dict(title='On Grand Strategy', seed='rl-gaddis', created='2026-06-07 21:40', edited='2026-07-19 23:05',
         props={'Authors': 'John Lewis Gaddis', 'Year': '2018', 'Type': 'Book', 'Status': 'Done', 'Tags': 'strategy, personal', 'Rating': '⭐⭐⭐⭐'},
         projects=['project_none'], body="""
Added after the UIST reviews came in; needed something not about telemetry.

- Hedgehog vs fox applied to leaders: those who know one big thing and those who know many small things. The best do both, aims fixed and means flexible.
- Long sections on Augustus and Elizabeth I that are better than they have any right to be.
- Done Jul 19, on the plane-day reading list for Dublin.
""", notes='straggler (Jun–Jul 2026)'),
    dict(title='Chess Structures: A Grandmaster Guide', seed='rl-rios', created='2026-02-15 22:40', edited='2026-04-02 22:00',
         props={'Authors': 'Mauricio Flores Rios', 'Year': '2014', 'Type': 'Book', 'Status': 'Reading', 'Tags': 'chess, personal'},
         projects=['project_none'], body="""
- Doing one structure a week: Caro-Kann structure first, then the Carlsbad.
- Each chapter: read the summary, play through 2 model games, then find the same structure in my own games.
- Apr 2: paused, UIST ate March.
"""),
    dict(title='The Rise and Fall of the Great Powers', seed='rl-kennedy', created='2026-03-15 23:30', edited='2026-08-30 21:20',
         props={'Authors': 'Paul Kennedy', 'Year': '1987', 'Type': 'Book', 'Status': 'To read', 'Tags': 'history, personal'},
         projects=['project_none'], body="""
- Recommended in two of the strategy books. Economic base → military power over 500 years.
- Aug 30: Sam has a copy at the house. Borrowing it after UIST.
""", notes='straggler edit Aug 2026'),
]
database(rl, RL_COLS, ['Name', 'Authors', 'Status', 'Tags'], rl_rows, '2026-01-29 22:05', [RG, 'project_tutortrace'],
         notes_view='reading list database (view export); mixes reading-group papers with personal books')

# ---- Hint timing pilot database (ONLY place this project exists) --------------------------------------------------
HT = ['project_hint_timing_study']
ht = N('Hint timing pilot', 'hint-timing-pilot')
HT_COLS = ['Name', 'Type', 'Status', 'Owner', 'Due', 'Created', 'Last edited time']
ht_rows = [
    dict(title='Kickoff — when should the hint appear?', seed='ht-kickoff', created='2026-02-11 21:30', edited='2026-02-12 10:05',
         props={'Type': 'Plan', 'Status': 'Done', 'Owner': 'David Barron'}, projects=HT, notes=ONE_TOOL + ' (kickoff, 2026-02-11)', body="""
<aside>
❓ Question: in a CS1 lab, does it matter **when** an AI hint is offered — immediately on error, after a fixed delay, or only once the student looks stuck?

</aside>

## Why

- In our classroom telemetry, a lot of "stalled-after-error" windows are students who had an assistant open and didn't use it, and a lot of fast fixes are students who asked the assistant within seconds and pasted.
- Hints that arrive too early may short-circuit productive struggle; hints that arrive too late lose students for 10 minutes.
- Nobody has run the simple version: same hints, different timing, real lab.

## Hypotheses

- **H1** Immediate hints minimize time-to-fix for the current error but lower performance on the next similar error.
- **H2** Hints offered only after a detected stall give the best transfer (next-error time-to-fix) with acceptable frustration.
- **H3** A fixed 90 s delay is worse than stall-triggered on both, because it ignores whether the student is making progress.

## Conditions (draft)

| Condition | Rule |
| --- | --- |
| Immediate | hint button glows as soon as a run fails |
| Delay-90 | hint available 90 s after a failed run |
| Stall-triggered | hint offered when no successful run and idle > 45 s after a failed run |

## Measures

- time-to-fix after each failed run
- hint acceptance rate
- next-error time-to-fix on a similar error (transfer)
- self-reported frustration 1–5 at the end of lab
- one post-lab quiz item per lab

## Next

- [x] write up study design (separate page)
- [x] ask Yan if this can be a small side study this spring (yes, "if it stays small")
- [ ] find out which CS 1114 lab weeks are usable
"""),
    dict(title='Study design', seed='ht-design', created='2026-02-12 23:10', edited='2026-02-17 22:40',
         props={'Type': 'Plan', 'Status': 'Done', 'Owner': 'David Barron'}, projects=HT, notes=ONE_TOOL + ' (study design)', body="""
## Design

- Within-subjects crossover over **two lab weeks** so each student sees two of the three conditions; condition order counterbalanced by lab bench (benches 1–6 / 7–12 / 13–18).
- Hints are identical across conditions: a fixed bank of **24 TA-authored hints** for labs 5 and 6 (loops + lists), 12 per lab, each mapped to an error pattern.
- Hint = conceptual nudge, never code. Max 2 hints per error.

## Participants

- Two lab sections of CS 1114, ~30 students each → ~60 students, expect ~50 with usable data.
- Students opt in at the start of lab; non-consenting students get the same tool with hints always available (data not stored).

## Stall detector

- Stall = no successful run **and** no edit larger than 3 characters for 45 s, after a failed run.
- Pilot the threshold on last fall's telemetry first: what fraction of failed runs would trigger it? Target 30–40%.

## Power (rough)

- With ~50 students × ~6 failed runs each, we can detect a medium effect on time-to-fix. Transfer measure will be noisy; treat as exploratory.

## Risks

- Lab TAs helping students in person swamps any hint-timing effect → ask TAs to log when they help (tally sheet).
- Students share hints across benches → seat them by condition group.

## Decisions

- [x] crossover, not between-subjects (Feb 17)
- [x] 45 s idle threshold for now, re-check against old telemetry
- [ ] decide whether the post-lab quiz counts for participation credit
"""),
    dict(title='CS1 lab logistics', seed='ht-logistics', created='2026-02-14 15:20', edited='2026-02-27 16:45',
         props={'Type': 'Logistics', 'Status': 'Blocked', 'Owner': 'David Barron', 'Due': 'March 9, 2026'}, projects=HT,
         notes=ONE_TOOL + ' (lab logistics)', body="""
## Which labs

- Labs 5 and 6 are the loops/lists labs → scheduled for the weeks of **Mar 16** and **Mar 23**.
- Sections: Tue 2:30–4:20 and Wed 9:05–10:55, McBryde 1st floor lab.
- Lead GTA for 1114 is fine with it as long as the lab handout doesn't change.

## Setup

- [ ] browser IDE plugin build with the three hint modes behind a URL param
- [ ] bench → condition map printed for TAs
- [ ] 6 loaner laptops in case the lab machines block the extension
- [x] TA tally sheet for in-person help (draft below)
- [ ] 10-min consent slot at start of lab — needs approved consent form first

## TA tally sheet (draft)

| Bench | Time | Helped with | Before or after a hint? |
| --- | --- | --- | --- |
| | | | |

## Problem (Feb 27)

The Mar 23 week is the UIST crunch week and Mar 16 is the week before. I can't run two lab sessions + debug a plugin live in those weeks. Next usable labs would be in April (labs 8–9, recursion), which changes the hint bank entirely.
"""),
    dict(title='Consent form draft', seed='ht-consent', created='2026-02-18 20:40', edited='2026-02-24 21:15',
         props={'Type': 'IRB', 'Status': 'In review', 'Owner': 'David Barron'}, projects=HT, notes=ONE_TOOL + ' (consent draft)', body="""
<aside>
⚠️ Need to check: amendment to the existing classroom-telemetry protocol vs a new exempt submission. Amendment turnaround has been ~3 weeks.

</aside>

## Draft text

**Study title:** Timing of automated hints in introductory programming labs

**What you'll do:** Work on this week's lab as usual. The coding tool may offer you hints at different times. At the end of lab you'll answer two short questions (about 2 minutes).

**What we collect:** Your code edits, runs and test results during the lab, when hints are shown and whether you open them, and your two answers. We do not collect your name; your lab session is linked to a random ID.

**Risks:** Minimal. Some hint timings may feel early or late. Your grade does not depend on taking part or on how you use the hints.

**Your choice:** You can say no now, or stop at any time, with no effect on your grade. If you say no, you'll use the same tool and your data won't be saved.

**Questions:** contact the study team (email TBD) or the university IRB office.

## Open questions

- [ ] Does the quiz item count as "research data" if it's also part of the normal lab? (ask IRB)
- [ ] Data retention: 3 years, de-identified, same as the main protocol?
- [x] Remove "AI" from the title — Yan's suggestion, avoids priming
"""),
    dict(title='Analysis plan', seed='ht-analysis', created='2026-02-22 22:15', edited='2026-03-01 23:30',
         props={'Type': 'Analysis', 'Status': 'Draft', 'Owner': 'David Barron'}, projects=HT, notes=ONE_TOOL + ' (analysis plan)', body="""
## Primary

`log(time_to_fix) ~ condition + lab + (1 | student) + (1 | error_pattern)`

- unit = failed run (only the first failed run of each error episode)
- condition contrast: stall-triggered vs immediate (H2 vs H1); delay-90 vs stall-triggered (H3)

## Secondary

- Transfer: time-to-fix on the next failed run with the same error pattern, same model.
- Hint acceptance: logistic mixed model, `accepted ~ condition + (1 | student)`.
- Frustration: ordinal (1–5) per student per lab, `clmm`.

## Exclusions

- Episodes where a TA helped before any hint (from the tally sheet).
- Students with < 2 failed runs in a lab.
- Sessions with > 20% missing telemetry (reconnect drops).

## Things not to get wrong

- Any train/test style split (if we try predicting stalls) must be grouped by student.
- Pre-register on OSF before the first lab, even if it's a pilot.

## Expected tables

| Table | Content |
| --- | --- |
| 1 | descriptives by condition (n episodes, median time-to-fix, acceptance) |
| 2 | mixed model estimates, primary |
| 3 | transfer + frustration |
"""),
    dict(title='Parking this', seed='ht-parking', created='2026-03-05 23:05', edited='2026-03-05 23:30',
         props={'Type': 'Decision', 'Status': 'Parked', 'Owner': 'David Barron'}, projects=HT,
         notes=ONE_TOOL + ' (decision to park the pilot, ~2026-03-05; never revived)', body="""
Parking the hint-timing pilot. Writing down why so future me doesn't have to reconstruct it.

## Why

1. **Timing.** The only labs that fit the hint bank (labs 5–6) land in the two weeks before the UIST deadline (Mar 31). Not doing both.
2. **IRB.** The amendment wouldn't come back before mid/late March anyway.
3. **Scope creep.** Every design conversation added a condition or a measure. It was supposed to be small.
4. Yan agreed: "revisit in the fall if you still care".

## What exists (all in this database)

- kickoff + hypotheses
- study design (crossover, 24-hint bank, 45 s stall rule)
- lab logistics + TA tally sheet
- consent draft (not submitted)
- analysis plan (mixed models, exclusions)

## If I pick it back up

- [ ] re-pick labs for fall (loops labs are usually week 6–7)
- [ ] validate the 45 s threshold on old telemetry first — cheapest step, do it before anything else
- [ ] submit the IRB amendment 6 weeks ahead, not 3
- [ ] cut to 2 conditions (immediate vs stall-triggered)
"""),
]
database(ht, HT_COLS, ['Name', 'Status', 'Type'], ht_rows, '2026-02-11 21:25', HT,
         notes_view=ONE_TOOL + ' (database view CSV)',
         notes_all=NEAR_DUP + '; also HARD CASE: project in only one tool (hint-timing pilot)')

# =====================================================================================================================
# Teamspace "Mathetic HQ" (shared with Hudson 2026-02-02)
# =====================================================================================================================
MC, EB = 'project_mathetic_company', 'project_engelbart'
hq = N('Mathetic HQ', 'mathetic-hq')
pl = N('Papert Lab notebook', 'papert-lab-notebook', hq)
pl_name = N('Name brainstorm', 'name-brainstorm', pl)
pl_int = N('Researcher interview guide', 'interview-guide', pl)
vals = N('Values', 'values', hq)
hire = N('Hiring wishlist', 'hiring', hq)
princ = N('Product principles', 'principles', hq)
comp = N('Competitor teardown', 'competitors', hq)
inc = N('Incorporation checklist (PBC)', 'incorporation', hq)
crm = N('Investor CRM', 'investor-crm', hq)
mtg = N('Meeting notes', 'meeting-notes', hq)

page(hq, '2026-02-02 10:20', '2026-03-21 00:15', f"""
Tags: home

Shared with Hudson Feb 2, 2026. Company wiki for the thing we're calling Papert Lab until we have a better name.

<aside>
🏠 Start here. If it's a decision, it goes in Meeting notes. If it's a doc, it's a page here. Tasks live in our heads until we get Linear (soon).

</aside>

## Pages

- {link(hq, pl)} — the original idea doc (Jan 28)
- {link(hq, vals)}
- {link(hq, princ)}
- {link(hq, comp)}
- {link(hq, hire)}
- {link(hq, inc)}

## Databases

- {link(hq, mtg, '.csv')}
- {link(hq, crm, '.csv')}

## Who does what (agreed Feb 2)

| | David | Hudson |
| --- | --- | --- |
| Prototype | ✅ | |
| Interviews | ✅ | ✅ |
| Landing page + copy | | ✅ |
| Fundraising | ✅ | ✅ |
| Legal / incorporation | | ✅ |

## Status (Mar 21)

Paused until after Mar 31 (UIST). See meeting notes.
""", [MC, EB], account=TEAM)

page(pl, '2026-01-28 23:10', '2026-02-09 01:12', f"""
Tags: idea, product

<aside>
💡 A research notebook that remembers where your thoughts came from.

</aside>

## The problem (mine, for now)

I have ~2 years of research spread over: ChatGPT and Claude chats, Zotero, PDFs in Downloads, Overleaf, Slack, Apple Notes, Google Docs, a lab Drive, and GitHub. When I write a related-work paragraph I spend more time re-finding *where I read something* than writing. This week (UIST related work) I lost an hour looking for a chat where I'd already worked out how our labels differ from prior work.

Licklider's self-study, again: most of the time goes to getting ready to think.

## The idea

- Import everything a researcher already has (chats, papers, notes, repos) **once**.
- Every note / claim in the notebook keeps a **trail** back to the sources and conversations it came from (Bush's trails, but automatic).
- You write in the notebook; it shows the provenance of each paragraph on hover.
- It's a notebook first, not a search engine. Search is a side effect.

## Why the name

Papert: learning by building, "mathetics". The notebook is where you build your thinking. Placeholder.

## Who for

- PhD students and postdocs with too many tools
- later: small labs (shared trails)

## First prototype (2 weeks?)

- [ ] importer for ChatGPT + Claude exports and a Zotero library
- [ ] dedupe the same paper across Zotero and Downloads (this will be harder than it sounds)
- [ ] a canvas/notebook view with a "came from" panel
- [ ] try it on my own UIST related-work section

## Open questions

- Local-first or cloud? (Local-first; researchers won't upload unpublished work to a startup.)
- Is "provenance" something people want, or something I want?
- How does this not become another app in the pile?

## Pages

- {link(pl, pl_int)}
- {link(pl, pl_name)}
""", [EB, MC], account=TEAM, notes='first "Papert Lab notebook" page (2026-01-28), pre-Engelbart product idea')

page(pl_int, '2026-02-04 22:00', '2026-02-15 23:20', """
Tags: research, interviews

20 minutes, Zoom or in person. Goal: understand how they move from reading → thinking → writing, and where things get lost. **Don't pitch.**

## Warm-up (3 min)

- What are you working on right now? What's the next deadline?

## Their stack (5 min)

- Walk me through where your stuff lives: papers, notes, AI chats, drafts, code.
- Which of those do you search most? Which do you never open again?

## The last time it hurt (7 min)

- Tell me about the last time you couldn't find something you knew you'd read or written. What was it? How long did it take? Did you find it?
- When you write related work, where do the sentences come from?
- Do you ever need to know *where* an idea came from (a paper, a chat, an advisor meeting)? When?

## AI chats (3 min)

- How many chats a week? Do you go back to old ones? How?

## Close (2 min)

- If you could press one button to fix one of these, what would it do?
- Who else should I talk to?

## Log

| # | Who (role) | Date | Biggest pain |
| --- | --- | --- | --- |
| 1 | PRIME Lab PhD student | Feb 6 | can't find old ChatGPT chats |
| 2 | VT ISE PhD student | Feb 9 | Zotero vs Downloads duplicates, never sure which PDF has her highlights |
| 3 | CS postdoc (friend of Hudson) | Feb 10 | writing: sentences with no memory of the source |
| 4 | HCI master's student | Feb 12 | "I don't take notes, I just ask the chatbot again" |
| 5 | education PhD student | Feb 13 | advisor meeting notes scattered across 3 apps |
""", [EB, MC], account=TEAM)

page(pl_name, '2026-02-10 00:30', '2026-03-06 23:40', """
Tags: brand

## Candidates

| Name | Why | Problem |
| --- | --- | --- |
| Papert Lab | Papert, learning by building | sounds like a research lab, not a product |
| Mathetic | Papert's word for the study of learning | hard to spell? people say "mathematic" |
| Memex | Bush | taken a hundred times |
| Trails | the core feature | too generic, outdoor brand vibes |
| Provenance | literal | sounds like a supply-chain startup |
| Engelbart | the 1962 framework, augmenting intellect | maybe for the product, not the company |

## Hudson's take (Feb 12)

Company = **Mathetic**, product named separately. Likes that it's a real word with a story.

## Mine

Agree. Product name: still undecided, Engelbart is the frontrunner after the reading group discussion. Don't decide until the prototype exists.

## Mar 6

Decided in the sync: company is **Mathetic** (PBC if we incorporate). Product name later.
""", [MC, EB], account=TEAM)

page(vals, '2026-02-03 22:45', '2026-02-10 21:30', """
Tags: culture

Written together on the Feb 3 call, cleaned up by David.

1. **Respect the researcher's work.** Their notes and unpublished ideas are theirs. Local-first by default; nothing leaves the machine without them knowing exactly what and why.
2. **Show your sources.** If the product makes a claim, it shows where it came from. Same rule for us in docs and decks.
3. **Augment, don't automate.** We help people think; we don't think for them. If a feature makes the user's understanding worse, it's a bad feature even if it saves time.
4. **Build for one real person first.** A feature ships when one named researcher uses it for real work.
5. **Say the boring truth.** In updates to each other and to investors: numbers first, no spin.
6. **Small team, high trust.** Disagree in the doc, decide in the sync, then commit.

## Not values (things we said and cut)

- "Move fast" — everyone says it, and it contradicts #1.
- "Open source everything" — maybe later, not a value.
""", [MC], account=TEAM)

page(hire, '2026-02-18 21:00', '2026-02-28 22:30', """
Tags: hiring

Nobody until we have money and a prototype people use. This is the list for when we do.

## First hire: founding engineer

- Desktop app experience (Electron or Tauri), local databases (SQLite), sync
- Has shipped something people use daily
- Comfortable with LLM-backed features but skeptical of them
- Bonus: has been a grad student / knows the research workflow
- Equity heavy, salary light; SF or remote with SF trips

## Second: design

- Someone who can do interaction design for dense information (think: Figma people who love spreadsheets)
- Contract first

## Later

- research-community person (pilots, onboarding, talks)

## Where to look

- VT CS alumni who went to dev-tools companies
- people who maintain popular Obsidian / Zotero plugins
- the incubator network if we get into one

## Comp notes

- Read up on founding engineer equity ranges (0.5–1.5% seems typical for first hire pre-seed)
""", [MC], account=TEAM)

page(princ, '2026-02-25 23:20', '2026-03-04 00:40', """
Tags: product

Rules for deciding what the notebook does and doesn't do.

## 1. Import is the onboarding

The first 10 minutes are: connect your stuff, watch it come in. If import misses things or shows duplicates, the user decides the product is broken. **Import quality > every other feature.**

- show counts per source as it imports ("312 Claude chats, 41 PDFs")
- dedupe the same paper across sources, but show that it was in 3 places
- never silently drop items; list what failed

## 2. Every paragraph has a trail

Provenance is visible on hover and clickable. A paragraph with no trail is marked as "yours" (that's fine, it's a feature).

## 3. Local-first

Data on disk, readable formats. Cloud is for sync and only when asked.

## 4. Notebook, not inbox

We don't show a feed of imported stuff. You start from a blank page and pull things in.

## 5. Slow AI, not chatty AI

Model calls happen when the user asks or in the background for indexing. No assistant popping up mid-sentence.

## 6. Respect existing tools

Don't make people leave Zotero or Obsidian. Read from them, link back to them.

## Anti-goals

- not a reference manager
- not a chat UI with a sidebar
- not team wiki software (we know, we're writing this in one)
""", [EB, MC], account=TEAM)

page(comp, '2026-03-02 22:10', '2026-03-09 23:55', """
Tags: market

Quick teardown. Focus: what each does for "where did this idea come from".

| Tool | What it is | Imports | Provenance | Why people leave |
| --- | --- | --- | --- | --- |
| Notion (+AI) | docs/wiki | manual, some importers | none at paragraph level | becomes a graveyard (see: this teamspace in a month?) |
| Obsidian | local markdown notes | plugins | backlinks only, manual | setup cost, plugin roulette |
| Roam / Logseq | outliner, block refs | weak | block refs, manual | performance, niche |
| Zotero | reference manager | papers only | citation-level | not for thinking, just storage |
| NotebookLM | Q&A over uploaded sources | upload docs | cites sources in answers | per-notebook silos, not your whole history |
| Elicit / lit-search tools | find + summarize papers | search | per claim citations | discovery, not your own notes |
| ChatGPT / Claude projects | chats with files | upload | none across chats | history is unsearchable at scale |

## Takeaways

- Nobody imports *everything* a researcher already has, including AI chats.
- Provenance exists only as citations to papers, not to your own conversations and notes.
- The closest thing is NotebookLM, but it's a per-project Q&A tool, not a notebook you write in.

## Risks

- Big labs add "memory" to chat products and it's good enough.
- Notion/Obsidian add AI import. (They'd still lack the trail.)
""", [EB], account=TEAM)

page(inc, '2026-03-12 20:15', '2026-03-19 22:40', """
Tags: legal
Status: Draft — not doing this before April

Hudson owns this. Notes from reading + one call with a founder friend of his.

## Entity

- Delaware **public benefit corporation** (PBC). Benefit statement draft: "to help researchers think more clearly by preserving the provenance of their ideas".
- Use a standard formation service vs a lawyer: formation service + a lawyer review for the founder docs.

## Steps

- [ ] file certificate of incorporation (PBC language + benefit statement)
- [ ] bylaws, initial board consent
- [ ] founder stock purchase agreements, 4-year vesting, 1-year cliff
- [ ] **83(b) elections within 30 days** of stock issuance (mail certified, keep the receipt!)
- [ ] EIN
- [ ] bank account
- [ ] IP assignment from both founders (incl. anything built before incorporation)
- [ ] register as foreign corp in the state where we operate (VA now, CA if we move)

## Ongoing

- Delaware annual report + franchise tax due **March 1** every year. Use the assumed par value method or the bill will look insane.
- PBC: biennial benefit report to stockholders.

## VT question

- Check VT IP policy: is anything I build on my own time while a GRA university property? Ask before incorporating. (Grad school office, not Yan.)
""", [MC], account=TEAM)

crm_rows = [
    dict(title='Thiel Fellowship', seed='crm-thiel', created='2026-02-19 22:30', edited='2026-03-10 23:15',
         props={'Type': 'Fellowship', 'Stage': 'Applied', 'Contact': 'online application', 'Check size': '$200k (grant)',
                'Next step': 'wait; interviews are rolling', 'Last contact': 'March 10, 2026', 'Owner': 'David Barron'},
         projects=[MC], body="""
## Notes

- Application is per person; only David is eligible-ish (age). Hudson helps with the essay.
- Essay angle: the 1962 framework, bootstrapping, and why the AI chat era makes provenance urgent.
- Submitted Mar 10 at 11:40 pm. 3 short answers + a 1-min video recorded at 1am, oh well.

## Questions they asked (short answer)

- something important you believe few people agree with → "the bottleneck in research is re-finding, not finding"
- what you'll build in 2 years
"""),
    dict(title='Surplus (incubator)', seed='crm-surplus', created='2026-02-20 10:15', edited='2026-03-13 18:30',
         props={'Type': 'Incubator', 'Stage': 'Interview', 'Contact': 'Lena Hoffmann', 'Check size': 'housing + stipend, no equity?',
                'Next step': 'second call after UIST', 'Last contact': 'March 13, 2026', 'Owner': 'Hudson Mitchell-Pullman'},
         projects=[MC], body="""
## What it is

SF incubator house: founders live and work together for a summer/fall cohort. Program lead: Lena Hoffmann.

## Notes from first call (Mar 13, Hudson + David)

- Lena asked: who's the user, what have you shipped, why now. We had no users yet; she said that's normal for the cohort.
- Cohort starts in **August**. Would mean moving to SF. (David: leave of absence? talk to Yan before saying yes.)
- Terms: housing + small stipend; she was vague on equity, follow up.
- Next: second call after Mar 31 with a prototype demo.
"""),
    dict(title='Northfield Angels', seed='crm-northfield', created='2026-02-26 21:40', edited='2026-03-14 11:05',
         props={'Type': 'Angel group', 'Stage': 'Researching', 'Contact': 'Marcus Oyelaran', 'Check size': '$25–100k',
                'Next step': 'ask Lena for intro once in Surplus', 'Owner': 'David Barron'},
         projects=[MC], body="""
- Angel group; Marcus Oyelaran invests in edtech and research tools, ex-founder.
- Has backed two companies from the Surplus house before, per Lena.
- Don't cold email. Warm intro after we have pilot users.
- Likely questions: retention, who pays (individuals vs labs), why not a feature of the big chat apps.
"""),
    dict(title='VT alumni angel network', seed='crm-vt-angels', created='2026-03-02 09:50', edited='2026-03-02 10:20',
         props={'Type': 'Angel group', 'Stage': 'Not now', 'Contact': 'general inbox', 'Check size': '$10–50k',
                'Next step': 'revisit after incorporation', 'Owner': 'Hudson Mitchell-Pullman'},
         projects=[MC], body="""
- They want an incorporated company and some traction. We have neither.
- Pitch night is twice a year; next one is in the fall.
- Revisit after incorporation.
"""),
]
CRM_COLS = ['Name', 'Type', 'Stage', 'Contact', 'Check size', 'Next step', 'Last contact', 'Owner', 'Created', 'Last edited time']
database(crm, CRM_COLS, ['Name', 'Stage', 'Contact', 'Next step'], crm_rows, '2026-02-19 22:20', [MC], account=TEAM,
         view_filter=lambda v: v['Stage'] != 'Not now',
         notes_view='investor CRM view export ("Active" view: hides Not-now rows and some columns)',
         notes_all=NEAR_DUP + ' (here the view also filters out one row)')

H = 'David Barron, Hudson Mitchell-Pullman'
mtg_rows = [
    dict(title='Kickoff — is this a company', seed='mtg-kickoff', created='2026-02-02 11:00', edited='2026-02-02 11:35',
         props={'Date': 'January 30, 2026', 'Type': 'Sync', 'Attendees': H}, projects=[MC, EB], body="""
Backfilled from my phone notes; we talked Jan 30 before this workspace existed.

## Discussed

- Read the Papert Lab notebook doc. Hudson: "this is the first idea you've had that you'd use yourself every day."
- Is this a company or a research project? Could be a CHI paper. Decided: try it as a company for 3 months, research angle stays open.
- Time: David still has UIST (Mar 31), ISE 6664, and GRA work. Max ~10 h/week until April.

## Decisions

- Hudson: landing page + interviews outreach. David: prototype + interview guide.
- Weekly sync, Mondays.

## Actions

- [x] David: share Notion workspace (Feb 2)
- [x] Hudson: list 15 researchers to interview
"""),
    dict(title='Notion setup + who does what', seed='mtg-setup', created='2026-02-02 14:05', edited='2026-02-02 15:10',
         props={'Date': 'February 2, 2026', 'Type': 'Sync', 'Attendees': H}, projects=[MC], body="""
## Discussed

- Workspace tour: HQ home, the notebook doc, this database.
- Ownership table (now on the HQ page).
- Values: draft tomorrow night together.

## Decisions

- Decisions get written here, with the date, or they didn't happen.
- No Linear yet; to-dos inside pages.

## Actions

- [x] both: values call Tue 10pm
- [x] David: interview guide v1 by Wed
"""),
    dict(title='Interview debrief (5 researchers)', seed='mtg-debrief', created='2026-02-16 21:00', edited='2026-02-16 22:20',
         props={'Date': 'February 16, 2026', 'Type': 'Sync', 'Attendees': H}, projects=[MC, EB], body="""
## What we heard (5 interviews, Feb 6–13)

- 4/5 lose things in AI chat history. Nobody has a system for it.
- 3/5 have the same paper in multiple places and don't know which copy has their highlights.
- 2/5 care about *where* an idea came from; the other 3 care about finding it at all. → provenance is the hook for some, retrieval is the hook for all.
- Nobody wants another app to write in. They want their existing stuff to become useful.

## Implications

- Lead with import + retrieval, provenance as the differentiator.
- Duplicates matter more than we thought.

## Actions

- [ ] David: prototype the importer on my own data first (ChatGPT, Claude, Zotero)
- [ ] Hudson: 5 more interviews, outside CS
"""),
    dict(title='Thiel app + naming', seed='mtg-thiel', created='2026-03-06 22:00', edited='2026-03-06 23:40',
         props={'Date': 'March 6, 2026', 'Type': 'Decision', 'Attendees': H}, projects=[MC], body="""
## Decisions

- Company name: **Mathetic**. Product name later (Engelbart is the favourite).
- David submits the Thiel application by Mar 10; Hudson reviews the essay Sunday.
- Apply to Surplus; Hudson takes the first call.

## Discussed

- Incorporation: not before April. Checklist page is up.
- Prototype: importer reads ChatGPT + Claude exports, Zotero half done. Dedupe is a mess (same paper, 3 filenames).

## Actions

- [x] David: Thiel app (submitted Mar 10)
- [x] Hudson: Surplus application + first call
"""),
    dict(title='Pause until UIST is in', seed='mtg-pause', created='2026-03-20 23:10', edited='2026-03-20 23:35',
         props={'Date': 'March 20, 2026', 'Type': 'Decision', 'Attendees': H}, projects=[MC], body="""
Short one.

- David is underwater with the UIST paper until Mar 31. No company work until Apr 6.
- Hudson keeps interviews going and preps the Surplus second call.
- Surplus first call went well (Mar 13). They want a demo next time.

## Decision

Pause syncs for two weeks. Next sync Apr 8.
"""),
    dict(title='Do we keep Notion', seed='mtg-notion', created='2026-04-08 21:30', edited='2026-04-09 00:20',
         props={'Date': 'April 8, 2026', 'Type': 'Decision', 'Attendees': H}, projects=[MC, EB], body="""
## Discussed

- Nobody opened the wiki during the pause. Meeting notes are the only thing we used.
- We write in Slack all day anyway; the docs here are stale already.
- Ironically this is the exact problem the product is supposed to solve.

## Decision

- Stop using Notion for the company. Move:
    - decisions → Slack channel + a pinned canvas
    - tasks → Linear (Hudson sets it up this week)
    - long docs → markdown in an Obsidian vault in the repo
- Leave this teamspace as an archive. Don't delete.

## Actions

- [ ] Hudson: Linear workspace
- [ ] David: export the notebook doc + principles to markdown
- [ ] both: Surplus second call, Apr 15
"""),
]
MTG_COLS = ['Name', 'Date', 'Type', 'Attendees', 'Created', 'Last edited time']
database(mtg, MTG_COLS, ['Name', 'Date', 'Type'], mtg_rows, '2026-02-02 10:55', [MC, EB], account=TEAM,
         notes_view='meeting notes database view export (David + Hudson syncs, Jan 30 – Apr 8 2026)')

g.finish()
