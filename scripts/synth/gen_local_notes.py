"""Synthetic local notes on David's Mac (PERSON.md): home-relative layout (Desktop/, Documents/, Downloads/, iCloud Drive/,
Projects/) holding .md/.txt/.docx/.html notes. Deterministic; rebuilds synthetic/local-notes/."""
import io, os, re, sys, zipfile
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('local-notes')
MOD = 'authentic/local-notes home-relative note file'


def fix_office(data, modified):
    mod = dt(modified).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    zin = zipfile.ZipFile(io.BytesIO(data)); out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            b = zin.read(it.filename)
            if it.filename == 'docProps/core.xml':
                x = b.decode()
                x = re.sub(r'(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)', lambda m_: m_.group(1) + mod + m_.group(2), x)
                x = re.sub(r'<dc:description>generated[^<]*</dc:description>', '<dc:description/>', x)
                b = x.encode()
            zi = zipfile.ZipInfo(it.filename, date_time=dt(modified).timetuple()[:6])  # no save-time leak, deterministic
            zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = it.external_attr
            zout.writestr(zi, b)
    return out.getvalue()


def note(rel, body, c, m, pids, notes=''):
    g.text(rel, body.lstrip('\n'), c, m, account=rel.split('/')[0] if '/' in rel else 'Home', project_ids=pids, modeled_on=MOD, notes=notes)


def docx_note(rel, blocks, c, m, pids, notes='', title=None):
    g.bytes(rel, fix_office(docx_bytes(blocks, title or os.path.splitext(os.path.basename(rel))[0], 'David Barron', c, m), m), c, m,
            account=rel.split('/')[0], project_ids=pids, modeled_on=MOD + ' (.docx)', notes=notes)


# ---------------------------------------------------------------------------------------------------------------
note('Desktop/todo.txt', """
TODO  (updated 10/16)

[ ] import v2: claude pagination past 1000 convos  <- blocks pilot 3
[ ] dedupe by DOI, fallback title+author+year
[ ] rename "Other" on connect screen -> "More tools"
[ ] send Marcus pilot numbers by 10/24 (weekly actives, trails opened)
[ ] reimburse: UIST receipts to Grace (hotel, per diem)  -- travel request went in 9/24
[ ] Delaware PBC annual report: reminder set for 2027-03-01, nothing to do now
[x] UIST talk 10/7
[x] Priya onboarding 10/9
[x] Daniel onboarding 10/13
[x] half 10/15 (1:24:51!!)
[ ] CA car registration (20 days after move?? already late, check)
[ ] cancel news newsletter
[ ] recovery week: no workouts till 10/22, easy 30-40 min only
""", '2026-09-28 22:10', '2026-10-16 23:05', ['project_engelbart', 'project_mathetic_company', 'project_vt_phd_admin', 'project_endurance_training', 'project_none'])

NOTES_MD = """# notes

## pilot 1 — Priya (10/9)
- expected ~1400 claude chats, we got 1262. gap ~140. she noticed before I did
- same paper twice: Ostrowski 2025, one from Zotero one from ~/Downloads. she laughed but it's bad
- trail view = the moment. "oh that's where that came from"
- she wants to drag a chat excerpt straight onto the canvas
- asked if anything leaves her laptop. answer: no, unless she turns on sync

## pilot 2 — Daniel (10/13)
- postdoc @ CMU, lives in Notion + Granola. neither is a connector yet
- put Notion under "Other" then couldn't find it again
- liked counts-before-import ("so I know what I'm getting")
- wants per-project privacy: some projects never imported

## so
1. pagination fix (claude export)
2. DOI dedupe
3. kill "Other"
"""
note('Desktop/notes.md', NOTES_MD, '2026-10-09 18:05', '2026-10-13 19:40', ['project_engelbart'],
     notes='HARD CASE: near-duplicate — original of Desktop/notes copy.md')
NOTES_COPY = NOTES_MD.replace("- she wants to drag a chat excerpt straight onto the canvas\n", "") \
    .replace("3. kill \"Other\"\n", "3. kill \"Other\"\n4. Notion connector before Granola? ask Hudson\n") \
    .replace("gap ~140. she noticed before I did", "gap ~140 (root cause: pagination stops at 1000)")
note('Desktop/notes copy.md', NOTES_COPY, '2026-10-14 09:20', '2026-10-14 11:02', ['project_engelbart'],
     notes='HARD CASE: near-duplicate — Finder copy of Desktop/notes.md with three lines changed')

note('Desktop/meeting scratch 9-10.txt', """
berkeley chat w/ Priya Raman  9/10 10:30  (Doe library cafe)

- 3rd yr, education + HCI, studies how TAs use dashboards
- tools: claude (lots), zotero ("graveyard"), downloads folder is the real library, google docs per project
- lost idea story: an argument for study 2 that lived in a july chat. found it 3 weeks later by scrolling
- copies chat text into docs, never keeps where it came from
- would she pilot? yes. wants to try on her TA-dashboard project
- follow up: send gift card, pilot invite early oct
- quote: "my zotero is a graveyard, my downloads folder is the real library"
""", '2026-09-10 10:31', '2026-09-10 11:24', ['project_berkeley_research_chats'])

note('Desktop/engelbart/import-dedupe brain dump.md', """
# import dedupe — brain dump (10/14, after Marcus call)

ok so the pilots broke import in two ways and they're the same problem: we don't know what we *should* have.

**missing**: we never compare expected vs got. claude export says 1,400 convos, we paginate to 1,000 and stop.
nobody notices unless the user counts. fix = every connector reports `expected` (from the source's own count / listing)
and we show the gap on the import summary. "1,262 of 1,400 Claude chats — 138 missing, retry?"

**dupes**: the same thing arrives from two tools. cases I've seen:
- paper PDF in Zotero storage + ~/Downloads + Drive (+ attached in gmail). key = DOI. no DOI -> title/first author/year
- a chat exported twice (two export zips, Aug and Oct). key = vendor convo id
- google doc + its downloaded .docx. key = ??? content hash after text extraction? title + modified?
- zip that contains files we also have unzipped. hash members

**not dupes** (do NOT merge):
- "Copy of X" vs "X" — versions, group them
- "deck" vs "deck v2"
- notes.md vs "notes copy.md" (lol I have this on my own desktop)

**wrong items**: stuff that isn't research at all getting dumped into projects (receipts, meal plans). project
assignment should be allowed to say "none". ask: is a training log "a project"? for me yes.

order: expected counts -> DOI dedupe -> version grouping -> "none" bucket. ship to Priya again before pilot 3.
""", '2026-10-14 21:30', '2026-10-15 00:48', ['project_engelbart'])

note('Desktop/uist26/talk Q&A prep.md', """
# UIST talk — Q&A prep

likely questions + short answers (keep each < 30 s)

**Q: kappa 0.71 isn't that high?**
For five behavioral states from replays it's in line with prior affect/behavior labeling. Most disagreement is between the two
stalled states, and merging them gives 0.80. Confusion matrix is in the paper.

**Q: does it generalize?**
Second course offering in the camera-ready: macro-F1 0.78 -> 0.74. One university, so no strong claim.

**Q: isn't this surveillance?**
States not prompt text; replays are an explicit logged action; opt-out with no penalty; we discuss it in limitations. Default
output is "go check in", not a grade.

**Q: why not just use an LLM to label?**
We tried zero-shot as a baseline; worse on stalled-after-error because it depends on timing, not text.

**Q: what do instructors do with it?**
In the study they walked to stalled-after-error students first. They ignored off-task. That surprised us.

**Q: relation to Ostrowski et al. L@S 2025?**
Similar stalling signals (repeated prompts, idle after error). They label offline; we focus on a live instructor view.

if blank: "great question — can I find you after the session?"
""", '2026-10-03 21:15', '2026-10-06 23:20', ['project_tutortrace'])

note('Documents/training/training thoughts.md', """
# training thoughts

**2025-11-02** — year 1 of the base plan done-ish. 8 h/week average, Z2 ceiling 148. resting HR 46 -> 43.

**2026-01-11** — block 1. the hard part isn't the running, it's not turning easy days into medium days. strap > wrist.

**2026-03-29** — UIST week. 4 h total. that's fine. consistency over months, not weeks.

**2026-06-09** — block 3: bike commute counts. Z2 HR drift on 60 min runs is ~3% now vs 5% in Jan.

**2026-08-12** — SF hills. Z2 pace on hills is a joke; go by HR and accept 5:30s on the climbs.

**2026-09-15** — 3x3 km @ HM pace felt controlled. half goal 1:25.

**2026-10-16** — 1:24:51. negative split. the base works. next year: keep 9-11 h, add one threshold session, maybe a marathon in spring?
""", '2025-11-02 20:40', '2026-10-16 21:10', ['project_endurance_training'])

note('Documents/packing list - UIST Detroit.txt', """
packing — UIST Detroit (fly SFO->DTW Sun 10/4, back Thu 10/8)

- laptop + charger + USB-C to HDMI dongle (Tomás says HDMI + USB-C in room, bring anyway)
- clicker (backup)
- talk PDF on USB stick + Drive zip
- badge confirmation email
- 2 shirts for talk day, 1 jacket
- running shoes + shorts (treadmill or riverwalk)
- HR strap
- receipts envelope for reimbursement
- poster tube? no, not presenting a poster
""", '2026-09-30 22:05', '2026-10-03 21:40', ['project_tutortrace'])

note('Desktop/Untitled.txt', """
14 / 41 / 190
0.71 -> 0.80 merged
ask Rezky re replay perf numbers
""", '2026-09-27 00:14', '2026-09-27 00:19', ['project_tutortrace'],
     notes='HARD CASE: vague title — "Untitled.txt" with bare numbers from the UIST talk prep')

note('Documents/recipes/turkey chili.md', """
# turkey chili (6 portions)

- 2 lb ground turkey, 1 onion, 1 red pepper, 4 garlic
- 2 cans kidney beans, 1 can black beans, 1 can crushed tomatoes, 1 can diced
- 2 tbsp chili powder, 1 tbsp cumin, 1 tsp smoked paprika, pinch cinnamon, salt
- brown turkey, then onion/pepper 6 min, garlic + spices 1 min, everything else, simmer 40 min
- freezes fine. ~520 kcal per portion with rice
""", '2026-01-18 17:10', '2026-01-18 17:40', ['project_none'])

note('Documents/recipes/peanut noodles.md', """
# peanut noodles (4)

sauce: 4 tbsp peanut butter, 3 tbsp soy, 1 tbsp rice vinegar, 1 tbsp honey, 1 tsp chili crisp, hot water to thin
- 300 g noodles, frozen edamame, shredded carrots, cucumber
- tofu or leftover chicken
- better cold the next day
""", '2026-02-08 19:00', '2026-04-12 18:20', ['project_none'])

note('Documents/recipes/overnight oats.txt', """
overnight oats (x4 jars)
80 g oats, 150 ml milk, 100 g greek yogurt, 1 tbsp chia, 1 tbsp honey, cinnamon
add banana or frozen berries in the morning
""", '2025-11-09 21:30', '2025-11-09 21:35', ['project_none'])

note('iCloud Drive/SF move planning.md', """
# moving to SF — planning

**2026-06-23**

Talked to Yan yesterday about the leave. It went better than I expected. The plan is: finish the UIST camera-ready and the
NeurIPS rebuttal, then go on leave from Fall and move to SF for the Surplus incubator. Everything below is logistics so I
stop carrying it in my head.

Big dates I know: incubator kickoff Aug 11. Camera-ready Aug 14 (do it before moving if at all possible). GRA ends Aug 15.

**2026-06-30**

Gave notice on the apartment, last day Aug 6. Things I own that are worth shipping: books (maybe 2 boxes after a purge),
running gear, the audio interface and monitors, the good chair if it fits a box (it won't). The desk and the bike trainer go
on the VT marketplace. Keeping the bike, shipping it with a bike box from the shop.

Questions:
- live in the incubator house or find a sublet? House is cheap and next to the work. Sublet gives a life outside work.
- car: drive it across or sell it? Driving is 5 days. Selling means buying something in SF, which nobody does.

**2026-07-08**

Started the apartment comparison sheet. SF rents are what everyone says. Inner Sunset rooms ~$1,650, Mission ~$1,900,
studios $2,300+. The incubator house room is $1,200 through December and 2 minutes from where we'd work. The only thing
against it is living at work. Sam Whitaker (other founder in the house) says it's fine as long as you leave for runs.

**2026-07-15**

Decided to drive the car out and keep it until December, then decide. Insurance will jump with an SF zip code; get quotes
after the move. Booked a one-way rental? No, driving my own car. Route: I-81 -> I-40 -> I-15 -> I-80, about 2,600 miles.
Actually that's a lot of days alone in a car right before the busiest month. Flying out on Aug 7 instead and shipping the
car with a carrier ($1,150 quoted). Final answer.

**2026-07-30**

Taking the incubator house room. Sent no-thanks to the two sublets. Leave form gets signed tomorrow.

Moving week plan:
- Aug 3-5: pack, ship boxes, car pickup Aug 5
- Aug 4: new Mac arrives — set it up clean from a Brewfile, don't migrate the old mess
- Aug 6: hand in keys, stay with Owen
- Aug 7: fly ROA -> CLT -> SFO (arrive Aug 8 after a missed connection, probably)
- Aug 8-10: unpack, find a running loop, groceries
- Aug 11: Surplus kickoff with Lena

**2026-08-09**

Here. The missed connection happened, landed the 8th around noon. Room is small but bright. Found a running loop along the
Embarcadero and a longer one to Golden Gate Park. Fog is real; it was 58°F in August. Car arrives "within 7-10 days".

**2026-08-16**

Week one done. Camera-ready went in on the 14th from the kitchen table. Car arrived on the 15th. Still need: CA car
registration, update address with the bank and VT, renters insurance (house covers? ask Lena).

**2026-09-06**

Settled. Routine: run 6:30, work 8-7 with Hudson, Friday demos at 4. The thing I miss is the quiet of Blacksburg trails.
The thing I don't miss is the drive to campus.
""", '2026-06-23 22:40', '2026-09-06 21:15', ['project_none'])

note('Desktop/ise6664 presentation notes.txt', """
ISE 6664 final pres 4/30 — my part (models slide, ~2 min)

- three approaches, same 600 annotated turns, 5-fold
- lexicon 0.48: misses sarcasm ("great, another error")
- fine-tuned 0.63: best, but needs labels
- zero-shot LLM 0.59: over-predicts mild frustration on terse messages
- takeaway: text alone gets you to ~0.6; timing features would help (TutorTrace-ish)
- hand off to Jordan for the survival curve
""", '2026-04-28 23:10', '2026-04-30 08:55', ['project_ise6664_affective_computing'])

note('Downloads/Claude-Leakage check in split script-20260724-2311.md', """
# Leakage check in split script

**Exported:** 2026-07-24 23:11

---

**User:**
ok so be concise. macro-F1 on IDETrace is 0.81 and that feels too good for the stalled class. here's make_splits.py, does anything
leak?

```python
train, test = train_test_split(windows, test_size=0.2, random_state=7, stratify=windows.label)
```

**Assistant:**
Yes. You split at the window level, so windows from the same student (often consecutive 30 s windows from one session) land in both
train and test. The model can memorize per-student patterns. Use a grouped split:

```python
from sklearn.model_selection import GroupShuffleSplit
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=7)
train_idx, test_idx = next(gss.split(windows, windows.label, groups=windows.student_id))
```

Then check `set(train.student_id) & set(test.student_id)` is empty. Expect the score to drop.

**User:**
38 students overlapped in fold 1. reran grouped: 0.74. ugh. ok that's the real number. rebuttal reports both

**Assistant:**
Reporting both, with the grouped split as the default going forward, is the right call.
""", '2026-07-24 23:11', '2026-07-24 23:11', ['project_idetrace'])

note('Projects/claude-plugins/hc-notes.md', """
# hc plugin notes

hc = "human compact": a compaction hook that asks me (or a rule file) what must survive before Claude Code compacts.

- 0.5.0 (8/17): naive summary. lost the file list twice. bad
- 0.11.0 (8/21): keep a pinned TODO block + failing test names verbatim. task success 2/2
- 0.13.0 (8/25): "focus hint" — one line I write about what I'm doing. helps a lot
- 0.13.1 (8/27): dropped an env var detail (E2B key name). add "keep env var names" to rules
- next: measure tokens after compaction vs success over 10 runs, not 6
- compact-focus as a separate tiny plugin? Hudson thinks yes
""", '2026-08-17 23:05', '2026-08-28 22:50', ['project_claude_code_plugins'])

note('Projects/engelbart-onboarding/connect-screen.html', """<!doctype html>
<html><head><meta charset="utf-8"><title>connect screen v3 notes</title>
<style>body{font:15px/1.5 -apple-system,sans-serif;max-width:720px;margin:40px auto}h2{margin-top:28px}code{background:#f3f3f3;padding:1px 4px}</style>
</head><body>
<h1>Connect screen v3 (2026-10-15)</h1>
<p>Replaces v2 after pilot B. Groups by <em>where thinking happens</em>, not by vendor.</p>
<h2>Groups</h2>
<ul>
<li><b>Conversations</b> — Claude, ChatGPT, Gemini, Granola (new), Slack</li>
<li><b>Writing</b> — Google Docs, Notion (new), Obsidian, Apple Notes, local notes</li>
<li><b>Papers</b> — Zotero, PDFs in Downloads/Desktop, Overleaf</li>
<li><b>Code</b> — GitHub, local repos, Claude Code / Codex sessions</li>
<li><b>Mail &amp; calendar</b> — Gmail, Outlook</li>
<li><b>More tools</b> (was "Other") — anything with an export file</li>
</ul>
<h2>Before import</h2>
<p>Show expected counts per source: <code>Claude 1,400 · Zotero 312 · Downloads PDFs 188</code>. After import show
<code>imported / expected</code> and a retry button on gaps.</p>
<h2>Duplicates</h2>
<p>"We found 23 papers in more than one place. Keep one copy each?" with a per-item preview.</p>
</body></html>
""", '2026-10-15 10:20', '2026-10-15 13:05', ['project_engelbart'])

note('Desktop/PapertLab/papert lab notebook idea.md', """
# papert lab — notebook idea (1/28/26, 1 am)

can't sleep, writing it down.

- I have ~900 claude chats from the last year and I can't find the one where I worked out the stalled-after-error split
- the paper cites the labeling guide, the guide came from a chat, the chat came from a lab meeting. nobody keeps that chain
- a notebook that imports chats + papers + docs and keeps the chain
- name: Papert Lab? (Papert -> constructionism -> learning by making things)
- first version = import claude export, cluster by project, timeline per project
- show Hudson this week
""", '2026-01-28 01:05', '2026-01-28 01:40', ['project_engelbart', 'project_mathetic_company'])

note('Documents/VT/leave questions for Grace.txt', """
questions for Grace Kim (call Tue 7/28 2pm)

1. does leave pause the time-to-degree clock / quals deadline?  -> yes, extended by leave length
2. can I keep vt.edu email + drive?  -> yes during approved leave
3. travel funding for UIST in Oct while on leave?  -> yes if the work was done while enrolled; submit by late Sep
4. health insurance options after GRA ends 8/15  -> student plan continuation form, deadline 8/31
5. what does Yan need to sign?  -> advisor section of the leave form (done 7/30)
6. return process for Spring/Fall 2027  -> re-enrollment form 6 weeks before term
""", '2026-07-27 21:20', '2026-07-28 14:35', ['project_vt_phd_admin'])

note('Documents/VT/cs3604 grading notes.txt', """
CS 3604 grading notes F25

P3 (REST API): autograder misses tests outside /test — check /spec manually. 4 teams used /spec.
P3 common deductions: no README run instructions (-2), hard-coded keys in config (-2), 500s on bad input (-3)
P4 (React): accessibility criterion: check alt text + labels with axe; don't fail for color contrast on default theme
late policy: 2 free late days per assignment? NO — 1 free, then -5/day. syllabus section 6.
regrade window: 7 days after grades posted
finals: grades due Mon 12/15 noon. final demos 12/9-12/11, 16 teams
""", '2025-10-21 13:30', '2025-12-10 22:45', ['project_cs3604_gta'])

note('Desktop/vizpi deploy 2 notes.txt', """
vizpi deploy #2  11/12  CS 3114

3:30 sec A + B start. 87 students. TAs: 3
3:45 sec B event rate drops to ~6/min. A fine.
3:52 reproduced locally: reconnect re-subscribes before token refresh resolves -> server drops events silently
4:05 patch: await refresh, buffer up to 500 events until ack
4:10 hotfix deployed, asked B to reload. rate back to ~55/min by 4:12
5:20 export raw -> vizpi-deploy2/raw/
loss estimate ~12% of sec B events (keystrokes in autosave vs telemetry)
TODO: heartbeat w/ buffered count; incident doc; tell Minsun/Xiaohang which windows are unlabelable
""", '2025-11-12 15:31', '2025-11-12 21:15', ['project_vizpi'])

note('Desktop/dynamite todo.md', """
# dynamite todo (jan)

- [x] embed 3,100 posts (384-d)
- [x] umap -> 10d
- [x] hdbscan min_cluster_size=15 -> 41 clusters, 23% noise
- [x] LLM labels for clusters, check every one by hand (6 too generic, 2 wrong)
- [ ] seed stability (5 seeds)
- [ ] cluster map figure for instructors
- [ ] stop using cursor for this file, it keeps rewriting the loader
""", '2026-01-20 22:40', '2026-02-03 23:15', ['project_dynamite'])

note('Documents/reading/as we may think - notes.md', """
# Bush, "As We May Think" (1945) — notes for reading group 2/12

- the memex: desk with microfilm, "associative trails" between documents, trails can be shared
- the key move is the *trail*, not the storage. he imagines a lawyer handing a colleague a trail
- what he got wrong: he thought the bottleneck was storage and retrieval speed
- what he got right: the bottleneck is the record of *why* things are connected
- connection to Engelbart (1962): Bush gives the artifact, Engelbart gives the system around it
- discussion q: are AI chat logs today's trails? nobody shares them, and nobody can find them
""", '2026-02-11 21:30', '2026-02-12 18:40', ['project_augmenting_cognition_reading_group'])

note('Documents/beats/beat ideas.txt', """
beat ideas

- dusk loop: Am9 -> Fmaj7 -> C -> G/B. 84 bpm. pad sidechained to kick, -6 dB duck, fast release
- v2: swap the clap for a rim, add vinyl noise bus at -28
- v3 (9/12): new kick (tape drums pack), cut 2nd drop, ends at 1:48. export stems + a quick wav bounce
- "deadline" 140 bpm 808 thing from 4/1 — never finished, maybe never
- try: resample the rhodes through the guitar amp sim
""", '2026-03-14 00:20', '2026-09-12 01:35', ['project_music_production'])

note('Documents/chess/chess notes.txt', """
chess notes (rapid 10+0)

rating: 1612 (oct 25) -> 1688 (mar 26) -> 1650 (sep 26, stopped playing in aug)
- london: stop h4 before castling. ...c5 + ...Qb6 hits b2 every time
- caro advance: ...Bf5, ...e6, ...c5. don't take on d4 early
- endgames: rook behind passed pawn. I keep forgetting this in time trouble
- puzzle rush best: 31
""", '2025-10-27 22:15', '2026-09-20 23:00', ['project_none'])

note('Documents/geopolitics notes.md', """
# geopolitics notes

**on chokepoints** — the more I read, the more the story of the decade looks like a fight over a few chokepoints:
advanced chips, a handful of straits, rare-earth processing. Everything else is commentary.

**grand strategy for middle powers** — the interesting countries are the ones that can't pick a side and don't want to.
Hedging is a strategy, not indecision.

**reading rule** — one chapter a night instead of the phone. Thucydides Book 1 re-read: the "truest cause" passage hits
differently after a year of tariff news.

**question I keep coming back to** — do export controls buy time or just change where the work happens?
""", '2025-12-02 23:30', '2026-07-19 22:50', ['project_none'])

note('Desktop/new mac setup.md', """
# new mac (8/4/26)

- clean install, no migration assistant
- `brew bundle --file ~/Brewfile`
- ssh key ed25519, add to GitHub personal + Mathetic-PBC org
- git config user.name/email (vt.edu for lab repos? no — personal everywhere, per-repo override for lab)
- node via brew, python via uv
- FL Studio: deactivated old license first, re-activated here
- browsers: Firefox personal, Brave for testing the landing page, Chrome for work accounts
- trackpad: natural scrolling off, tap to click on
- copy over: Desktop, Documents, Projects, Music/Projects. NOT Downloads (it's a landfill)
""", '2026-08-04 10:05', '2026-08-04 17:30', ['project_none'])

docx_note('Downloads/sublet listing notes.docx', [
    ('title', 'Sublet listings — notes'),
    ('p', 'July 2026. Looking for Aug-Dec, under $2,000, < 30 min to SoMa.'),
    ('table', [['Listing', 'Rent', 'Pros', 'Cons'], ['Inner Sunset room', '$1,650', 'quiet, near park', 'fog, 35 min commute'],
               ['Mission room', '$1,900', 'in-unit laundry, close', 'loud street'], ['Outer Richmond room', '$1,450', 'cheap', '45 min, 4 roommates']]),
    ('p', 'Red flags seen: one listing wanted a deposit before a video tour. Skipped.'),
    ('p', '7/30: going with the incubator house instead.'),
], '2026-07-10 21:40', '2026-07-30 21:30', ['project_none'])

note('iCloud Drive/Dublin wedding logistics.txt', """
Niamh's wedding — logistics

- RSVP: sent 5/12, +0
- dates: ceremony Saturday, arrive Thursday to get over jet lag
- flights: now from SFO since the move. SFO-DUB direct exists, ~10.5 h
- guesthouse near the venue booked 6/3, 3 nights
- gift: registry (kitchen)
- bring: suit, the good shoes, adapter (type G)
""", '2026-05-12 20:50', '2026-08-26 21:10', ['project_none'])

note('Desktop/investor call 2 notes.md', """
# Marcus Oyelaran — call 2 (10/14, 11:00 PT)

- opened with pilots. told him straight: import missed ~140 chats + showed dupes for pilot 1. he liked the honesty
- he cares about: weekly actives among pilots, trails opened per week per user, does anyone come back without a nudge
- "who pays" again: individual first, lab plan when 2+ people share a project. he's ok with that for pre-seed
- **interested in $50k into the pre-seed SAFE if pilots convert** (convert = still active after 4 weeks + willing to pay)
- wants numbers by 10/24
- intro offer: a lab director at a university he knows, after we fix import

next: update cap table SAFE tab (Marcus = verbal, contingent), metrics doc for 10/24
""", '2026-10-14 11:52', '2026-10-14 13:20', ['project_mathetic_company'])

note('Desktop/pilot daniel notes.md', """
pilot B — Daniel Osei (CMU postdoc)  10/13 1pm PT

- 45 min, zoom, he drove
- sources he wanted: claude, zotero, notion (!), granola (!), github
- connect screen: put Notion under "Other". 2 min later couldn't find it. "where did Notion go"
- import counts before import = good. "so I know what I'm getting"
- trail view: liked it but wants to hide some projects from import entirely
- bug: canvas didn't re-render after import finished until he scrolled
- will he keep using it? "if Notion shows up, yes"
""", '2026-10-13 13:02', '2026-10-13 14:15', ['project_engelbart'])

note('Documents/taxes 2025.txt', """
taxes 2025

- W-2 VT: in Drive
- 1098-T: tuition fully covered by waiver, box 5 scholarships > box 1 -> check fellowship part taxable (it's GRA wages, so no)
- VA state: same software
- filed 4/4, fed refund 4/22, VA 5/1
""", '2026-03-08 20:15', '2026-05-01 19:30', ['project_none'])

note('Documents/portfolio redesign ideas.md', """
# portfolio redesign

- one page. name, one line, three links
- papers first (TutorTrace UIST '26, IDETrace in review, VizPI)
- Engelbart with a 20 s loop video, not a screenshot
- old projects at the bottom: Juno, PlotPact
- steal: big serif name + small sans body; no carousel
- deploy: same static host as before; custom domain stays
""", '2026-07-12 21:05', '2026-07-21 22:40', ['project_portfolio'])

docx_note('Documents/ISE6664 reflection.docx', [
    ('title', 'ISE 6664 — personal reflection'),
    ('p', 'Submitted with the final report, 2026-05-08.'),
    ('p', 'I came into the course thinking affect detection was a modeling problem. The annotation work changed my mind: Maya\'s codebook '
          'took four rounds because "frustration" meant different things depending on whether the student was close to a solution. That '
          'distinction maps directly onto the stalled-after-error state in my own research.'),
    ('p', 'On ethics: detecting frustration from text is easy to overclaim. I would not deploy our classifier to change what students see '
          'without them knowing. At most it should nudge a human TA, the same conclusion we reached in TutorTrace.'),
    ('p', 'What I would do differently: add timing features and ask students to self-report frustration on a few prompts so the labels are not '
          'only from annotators.'),
], '2026-05-07 22:30', '2026-05-08 10:10', ['project_ise6664_affective_computing'])

note('Downloads/bike derailleur.txt', """
derailleur fix (5/10)
- symptom: skips 3rd-5th cog under load, since the 5/9 crash
- hanger bent, visible from behind
- barrel adjuster 1/2 turn ccw -> better not fixed
- shop: new hanger $28 + $35 labor, ready 5/12
""", '2026-05-10 18:40', '2026-05-12 18:20', ['project_none'])

note('iCloud Drive/half marathon race plan.txt', """
HM race plan 10/15
goal 1:25 = 4:02/km
0-5k 4:05 (don't chase Owen)
5-15k 4:01-4:02, gels at 7 + 14
15-21k whatever's left, hill @17 costs ~10s
shoes: racer, 96 km
result: 1:24:51 (Owen 1:22:10) 2nd half faster by ~20s
""", '2026-10-11 20:15', '2026-10-15 14:40', ['project_endurance_training'])

note('Documents/VT/tacode handoff email draft.txt', """
to: Minsun   subj: TACode handoff (draft 11/18)

hey — writing up TACode before I forget the details. full doc in Drive (VT > TACode > handoff). short version:
- main branch deployable, claim-timer branch half done
- known bug: two TAs can claim the same ticket within ~1s, needs a transactional claim
- canvas roster import breaks with cross-listed sections
- secrets in the lab password manager, not the repo
honestly I'd fold the queue into the VizPI TA dashboard instead of reviving it. happy to walk through it next week
""", '2025-11-18 17:05', '2025-11-18 17:30', ['project_tacode'])

g.finish()
