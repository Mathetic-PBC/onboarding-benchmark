"""Synthetic Linear (Phase 2): a synthetic "Pilots" team (key PIL) in the Mathetic workspace, same layout and JSON shapes as
authentic/linear/Mathetic (Linear MCP: get_issue + issue detail + list_comments; get_project + milestones + status updates;
get_document; workspace lists).

  synthetic/linear/Mathetic/issues/PIL-<n>.json      {issue, detail, comments}  (comments inline, newest first, like the real export)
  synthetic/linear/Mathetic/projects/P-PIL-1.json    {project, milestones, status_updates, comments}
  synthetic/linear/Mathetic/documents/<uuid>.json    document with markdown content
  synthetic/linear/Mathetic/workspace/*.json         workspace, teams, users, labels, statuses, cycles, custom_views

Sep–Oct 2026: pilot-program setup, Priya Raman's session (2026-10-09), Daniel Osei's session (2026-10-13). Identifiers PIL-*
never collide with the real MATH-* issues. Every file is one item (generic itemizer).
"""
import os, sys, re, hashlib, datetime
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('linear')
W = 'Mathetic'
ACCT = 'Mathetic workspace (linear.app/mathetic)'
MOD = 'authentic/linear/Mathetic/{} shape (Linear MCP export)'
ENG, CO, BRC = 'project_engelbart', 'project_mathetic_company', 'project_berkeley_research_chats'


def J(s):
    """local time string 'YYYY-MM-DD HH:MM[:SS]' -> aware UTC datetime; minute-precision strings get deterministic seconds + ms"""
    h = int(hashlib.sha256(str(s).encode()).hexdigest()[:8], 16)
    d = dt(s).astimezone(UTC)
    if len(str(s).strip()) <= 16: d += datetime.timedelta(seconds=h % 60)
    return d + datetime.timedelta(microseconds=1000 * ((h >> 8) % 1000))


def L(s):
    """local time string -> Linear ISO UTC with milliseconds"""
    d = J(s)
    return d.strftime('%Y-%m-%dT%H:%M:%S.') + f'{d.microsecond // 1000:03d}Z'


def slug(t, n=70):
    s = re.sub(r'[^a-z0-9 \-]', '', t.lower()).strip()
    s = re.sub(r'[\s\-]+', '-', s)
    if len(s) > n: s = s[:n].rsplit('-', 1)[0]
    return s


USERS = {
    'David Barron': dict(id=uid('linear/user/david'), name='David Barron', email='david@mathetic.com', displayName='david', isAdmin=True,
                         isGuest=False, isActive=True, createdAt=L('2026-09-14 20:02'), updatedAt=L('2026-09-14 20:05'),
                         status='Offline (last seen 2026-10-17T05:41:12.000Z)'),
    'Hudson': dict(id=uid('linear/user/hudson'), name='Hudson', email='hudson@mathetic.com', displayName='hudson', isAdmin=True,
                   isGuest=False, isActive=True, createdAt=L('2026-09-14 20:10'), updatedAt=L('2026-09-14 20:12'),
                   status='Offline (last seen 2026-10-16T23:58:40.000Z)'),
}
TEAM = dict(id=uid('linear/team/PIL'), key='PIL', parentId=None, displayName='Pilots', icon='Users', name='Pilots', visibility='public',
            createdAt=L('2026-09-14 20:04'), updatedAt=L('2026-10-13 18:30'))
STATUSES = {n: dict(id=uid(f'linear/status/{n}'), type=t, name=n) for n, t in
            [('Backlog', 'backlog'), ('Todo', 'unstarted'), ('In Progress', 'started'), ('In Review', 'started'), ('Done', 'completed'),
             ('Canceled', 'canceled'), ('Duplicate', 'duplicate')]}
LABELS = [('Bug', '#EB5757', 'Something is broken.'), ('Feature', '#BB87FC', 'New capability.'),
          ('Improvement', '#4EA7FC', 'Make something that works work better.'),
          ('Pilot feedback', '#F2994A', 'Came out of a pilot session. Link the session in the description.'),
          ('Import', '#26B5CE', 'Connect / import / dedupe pipeline.'), ('Onboarding', '#4CB782', 'First-run, connect screen, tour.'),
          ('Ops', '#95A2B3', 'Logistics: builds, scheduling, paperwork, gift cards.')]
PRIO = {0: 'No priority', 1: 'Urgent', 2: 'High', 3: 'Medium', 4: 'Low'}
PROJECT_ID = uid('linear/project/pilot-program')
PROJECT_NAME = 'Pilot program'
MILESTONES = {
    'kit': dict(id=uid('linear/ms/kit'), name='Pilot kit ready', description='Signed build, interview script, consent one-pager, feedback form. By 10/2.',
                progress=100.0, sortOrder=10, targetDate='2026-10-02'),
    'onboard': dict(id=uid('linear/ms/onboard'), name='First two pilots onboarded', description='Priya (10/9) and Daniel (10/13) through a full import + debrief.',
                    progress=100.0, sortOrder=20, targetDate='2026-10-13'),
    'fixes': dict(id=uid('linear/ms/fixes'), name='Import fixes from pilot feedback shipped',
                  description='Everything labeled Pilot feedback + Bug from the first two sessions, before the 2-week check-ins.',
                  progress=58.33, sortOrder=30, targetDate='2026-10-24'),
    'convert': dict(id=uid('linear/ms/convert'), name='3 converted pilots',
                    description='Converted = weekly active in 3 of 4 weeks after onboarding + yes to paying (definition in PIL-36). Before demo day 11/19.',
                    progress=0.0, sortOrder=40, targetDate='2026-11-13'),
}
DOCS = {}  # key -> (uuid, title)
for key, title in [('script', 'Pilot interview script'), ('dedupe', 'Import dedupe rules v0'), ('synth', 'Pilot feedback synthesis')]:
    DOCS[key] = (uid(f'linear/doc/{key}'), title)

D, H = 'David Barron', 'Hudson'
PR = 'https://github.com/Mathetic-PBC/engelbart/pull/{}'

# ---------------- issues (hand-written) ----------------
# states: [(status, local time), ...] first = created state. comments: [(author, time, body)] (oldest first here; written newest first)
ISSUES = []


def I(n, title, desc, states, prio, labels, assignee, creator, ms=None, proj=True, parent=None, due=None, comments=(), related=(), dup=None,
      attach=(), docs=(), pids=(ENG,), note=''):
    ISSUES.append(dict(n=n, title=title, desc=desc, states=states, prio=prio, labels=list(labels), assignee=assignee, creator=creator, ms=ms,
                       proj=proj, parent=parent, due=due, comments=list(comments), related=list(related), dup=dup, attach=list(attach),
                       docs=list(docs), pids=list(pids), note=note))


I(1, 'Write the pilot interview script',
  "45-minute session over Zoom with screen share. Shape:\n\n1. 5 min context (what Engelbart is, what we will and won't look at)\n"
  "2. 15 min connect + import, live, pilot drives\n3. 15 min: pick one idea from the last month and follow its trail\n4. 10 min debrief\n\n"
  "Questions must not lead: \"what did you expect to happen\", never \"was that confusing\". Script lives in the doc *Pilot interview script*.",
  [('Todo', '2026-09-14 21:10'), ('In Progress', '2026-09-21 10:30'), ('Done', '2026-09-22 16:45')], 2, ['Onboarding'], D, D, ms='kit', docs=['script'],
  comments=[(H, '2026-09-22 11:20', 'Read it. Add a question about which tools they *didn\'t* connect and why. That tells us more than what they did connect.'),
            (D, '2026-09-22 16:40', 'Added as Q9 ("Is there anywhere your research lives that you didn\'t connect? Why not?"). Marking done.')])
I(2, 'Shortlist pilot users from the Berkeley research chats',
  "Candidates: the three Berkeley research chats (Elena 9/9, Priya 9/10, Ben 9/16) + Lena's intros.\n\nCriteria:\n- more than a year of AI chats (Claude or ChatGPT)\n"
  "- uses Zotero or another reference manager\n- willing to screen share for 45 min and send the import log afterwards",
  [('Todo', '2026-09-14 21:25'), ('In Progress', '2026-09-15 09:00'), ('Done', '2026-09-18 17:10')], 2, [], H, H, ms='kit', pids=(ENG, BRC),
  comments=[(H, '2026-09-18 17:05', "Priya: yes, Fri 10/9.\nElena: wants to wait until after her quals (November).\nBen: no, his chats are on a lab account he can't export.\n"
                                     "Lena's intro, Daniel Osei (postdoc, CMU): yes, Tue 10/13.")])
I(3, 'Consent + data-handling one-pager for pilots',
  "Plain language, one page:\n- what Engelbart reads on your machine (only the sources you tick)\n- what leaves the laptop (nothing, except opt-in crash reports)\n"
  "- how to delete everything (one button + the folder path)\n- who to contact\n\nSend it with the calendar invite, not at the start of the call.",
  [('Todo', '2026-09-15 10:00'), ('In Progress', '2026-09-23 14:00'), ('Done', '2026-09-25 12:30')], 2, ['Ops'], D, D, ms='kit', pids=(ENG, CO),
  comments=[(H, '2026-09-24 19:15', 'Can we say "nothing leaves your laptop" in bold at the top? That\'s the first question everyone asked in the research chats.'),
            (D, '2026-09-25 12:25', 'Done. Also added the exact folder: `~/Library/Application Support/Engelbart/`.')])
I(4, 'Signed + notarized macOS build for pilots',
  "Developer ID cert on the Mathetic PBC Apple account, notarize with `notarytool` in CI, staple the ticket. Pilots should not have to right-click → Open.",
  [('Todo', '2026-09-16 11:00'), ('In Progress', '2026-09-28 20:00'), ('Done', '2026-09-30 01:40')], 2, ['Ops'], D, D, ms='kit',
  comments=[(D, '2026-09-29 23:10', 'Notarization fails: "The signature of the binary is invalid" for the bundled `rg` (ripgrep) inside `Contents/Resources/bin`. '
                                    'Nested binaries need `--options runtime` and their own signature before the app is signed.'),
            (D, '2026-09-30 01:35', 'Fixed. `codesign --deep` was the problem; now signing inner binaries explicitly, then the app. `Engelbart-0.9.3.dmg` notarized + stapled, '
                                    'opens with a double click on a fresh account.')],
  attach=[('PR #198: Sign nested binaries before the app bundle; notarize in CI', PR.format(198))])
I(5, 'Dry-run the full onboarding on a fresh macOS user account',
  "New macOS user, no dev tools, Claude export + a small Zotero library + a messy Downloads folder. Time it end to end and write down every moment we'd have to explain something.",
  [('Todo', '2026-09-16 11:05'), ('In Progress', '2026-10-01 15:00'), ('Done', '2026-10-03 13:20')], 3, ['Onboarding'], H, D, ms='kit',
  comments=[(H, '2026-10-03 13:15', '22 minutes end to end. The big one: the Full Disk Access prompt only shows up *after* the connect screen, so the first Downloads scan '
                                    'silently finds 0 files. Filed PIL-10. Smaller: the import progress screen says "Working…" with no numbers (PIL-12).')],
  related=[10, 12])
I(6, 'Import log: per-source found / imported / skipped / duplicate counts',
  "Local-only log at `~/Library/Application Support/Engelbart/import-log.jsonl`, one line per source per run:\n\n"
  "```\n{\"source\":\"claude\",\"found\":612,\"imported\":612,\"skipped\":[],\"duplicates\":0,\"started\":\"…\",\"finished\":\"…\"}\n```\n\n"
  "Pilots can send it to us if they want. Without it we can't tell \"missed\" from \"skipped\" from \"deduped\".",
  [('Todo', '2026-09-18 10:00'), ('In Progress', '2026-09-25 13:00'), ('In Review', '2026-09-26 22:40'), ('Done', '2026-09-27 11:15')], 2, ['Import', 'Feature'], D, D,
  ms='kit', attach=[('PR #191: import-log.jsonl with per-source counts', PR.format(191))])
I(7, 'Pilot feedback form',
  "8 questions, sent right after the session and again one week later. Same questions both times so we can see what changed. Include \"what would make you stop using it\".",
  [('Todo', '2026-09-20 12:00'), ('In Progress', '2026-09-23 10:00'), ('Done', '2026-09-24 18:00')], 3, ['Onboarding'], H, H, ms='kit')
I(8, 'Schedule pilot sessions',
  "- Priya Raman: Fri 10/9, 10:00 PT, Zoom\n- Daniel Osei: Tue 10/13, 9:00 PT / 12:00 ET, Zoom\n\nInvite 2 days before with the dmg link, the consent one-pager (PIL-3) and "
  "\"please have your Claude export downloaded\".",
  [('Todo', '2026-09-18 17:20'), ('Done', '2026-09-26 10:05')], 3, ['Ops'], H, H, ms='onboard')
I(9, 'Pilot thank-you gift cards ($100)',
  "One per pilot after the debrief. Paid from the Mathetic PBC card, keep the receipts in the Drive finance folder.",
  [('Todo', '2026-09-20 12:10'), ('In Progress', '2026-10-09 13:00'), ('Done', '2026-10-14 15:00')], 4, ['Ops'], H, H, pids=(CO,),
  comments=[(H, '2026-10-10 09:40', 'Priya\'s sent (she asked for the bookstore one). Daniel\'s after Tuesday, tracked in PIL-34.')])
I(10, 'Ask for Full Disk Access before the connect screen, not after',
  "Found in the PIL-5 dry run. Today: connect screen → user ticks Downloads → scan runs → 0 files → *then* macOS shows the Full Disk Access prompt. "
  "Move the permission step before the connect screen, explain it in one sentence, and re-scan automatically once it's granted.",
  [('Todo', '2026-10-03 13:30'), ('In Progress', '2026-10-05 10:00'), ('Done', '2026-10-06 17:45')], 2, ['Bug', 'Onboarding'], D, H, ms='onboard',
  attach=[('PR #203: Permissions step before Connect; auto-rescan on grant', PR.format(203))], related=[5])
I(11, 'Claude import: handle both export layouts',
  "Older Claude exports have one `conversations.json`; newer ones also ship `projects.json` and `users.json`. Make the parser accept both and fail loudly on anything else "
  "instead of importing 0 conversations.",
  [('Todo', '2026-10-01 11:00'), ('In Progress', '2026-10-04 14:00'), ('Done', '2026-10-05 19:30')], 2, ['Import', 'Feature'], D, D, ms='onboard',
  attach=[('PR #200: Claude export: accept both layouts, error on unknown', PR.format(200))])
I(12, 'Import progress: show counts per source while importing',
  "Replace \"Working…\" with a row per source: found / imported / duplicates so far. Pull the numbers from the same counters as the import log (PIL-6).",
  [('Todo', '2026-10-03 13:35'), ('In Progress', '2026-10-06 09:30'), ('Done', '2026-10-07 22:10')], 3, ['Onboarding', 'Improvement'], D, H, ms='onboard')
I(13, 'Recording consent line in the session invite',
  "Add: \"We'd like to record the screen share for our notes only. Say no and we won't, no problem.\" Ask again at the start of the call.",
  [('Todo', '2026-10-05 16:00'), ('Done', '2026-10-06 10:20')], 4, ['Ops'], H, H, ms='onboard')
I(14, 'Claude import missed ~140 of Priya\'s conversations',
  "From Priya's session (10/9). Her Claude export has 612 conversations; Engelbart showed 471 after import. The import log says `found: 471`, so we never saw the other 141 "
  "(not skipped, not deduped).\n\nRepro with our own exports before touching code.",
  [('Todo', '2026-10-09 11:20'), ('In Progress', '2026-10-09 14:00'), ('In Review', '2026-10-11 21:30'), ('Done', '2026-10-12 18:05')], 1,
  ['Bug', 'Import', 'Pilot feedback'], D, D, ms='fixes', due='2026-10-12',
  comments=[(D, '2026-10-09 16:40', "Repro with my own export: 38 missing. Every missing one is either\n(a) inside a Claude Project, or\n(b) untitled (`\"name\": \"\"`).\n\n"
                                    "(a) the parser only walks top-level conversations and drops anything with a `project_uuid` it can't resolve, because we never read `projects.json`.\n"
                                    "(b) the dedupe key was `(name, created_at[:10])`, so all untitled chats from the same day collapsed into the first one."),
            (D, '2026-10-10 01:15', "Priya's numbers: 97 project conversations + 44 untitled = 141. Fix: read `projects.json` and attach project conversations; dedupe key is now "
                                    "the conversation `uuid` only (rule 3 in *Import dedupe rules v0*)."),
            (H, '2026-10-10 09:00', 'Is the untitled collapse also hitting ChatGPT? Their export has untitled ones too.'),
            (D, '2026-10-10 09:30', 'No, the ChatGPT path already keys on `conversation_id`. Only Claude. Added a test with 3 untitled chats on the same day.'),
            (D, '2026-10-12 18:00', 'Re-ran Priya\'s export (she sent the zip again): 612/612. Merged.')],
  attach=[('PR #212: Claude import: read projects.json, key conversations by uuid', PR.format(212))], docs=['dedupe'], related=[23],
  note="Priya's 10-09 pilot bug (PERSON.md §7: import missed ~140 Claude chats)")
I(15, 'Same paper imported twice (Zotero storage + ~/Downloads)',
  "From Priya's session (10/9). Her library showed *Productive Struggle or Silent Stalling?* (Ostrowski et al.) twice: once from "
  "`~/Zotero/storage/8KQ2M4ZD/Ostrowski et al. - 2025 - Productive Struggle or Silent Stalling.pdf` and once from `~/Downloads/2507.01842v1.pdf`. "
  "Same bytes. She found ~30 more like it while scrolling.\n\nNobody wants two cards for one file.",
  [('Todo', '2026-10-09 11:25'), ('In Progress', '2026-10-10 10:00'), ('In Review', '2026-10-12 23:00'), ('Done', '2026-10-13 20:30')], 2,
  ['Bug', 'Import', 'Pilot feedback'], D, D, ms='fixes',
  comments=[(D, '2026-10-10 10:20', "Byte-identical → same sha256, rule 1 in the dedupe doc. But some pairs are *not* identical: arXiv v1 in Downloads vs the camera-ready in Zotero. "
                                    "Those should become one paper with two versions, not a merge (PIL-37)."),
            (D, '2026-10-13 20:25', "Shipped content-hash dedupe + DOI match. Priya's PDFs: Zotero 760 + Downloads 454 = 1,214 files → 987 unique, 227 merged. "
                                    "Each merged card lists every location it was found in.")],
  attach=[('PR #214: Dedupe PDFs by sha256 and DOI; keep all locations', PR.format(214))], docs=['dedupe'], related=[37],
  note="Priya's 10-09 pilot bug (duplicate PDFs, Zotero vs Downloads); mentions the Ostrowski paper by title")
I(16, 'Write import dedupe rules v0',
  "One page, concrete rules, in evaluation order. Each rule says what key, what happens on a match, and what we do NOT merge. Doc: *Import dedupe rules v0*.",
  [('Todo', '2026-10-10 00:30'), ('In Progress', '2026-10-10 11:00'), ('Done', '2026-10-11 16:00')], 2, ['Import'], D, D, ms='fixes', docs=['dedupe'],
  comments=[(H, '2026-10-11 12:10', 'Rule 6 (title similarity never merges on its own) is the right call. Suggest-only.')])
I(17, 'Make the provenance trail step 1 of the tour',
  "Priya's best moment (10/9): she clicked a note and saw the three chats and the PDF it came from, and said \"oh, that's the thing I actually want\". "
  "Today the trail is step 5 of 6 in the tour and she only found it because I asked her to. Move it to step 1.",
  [('Todo', '2026-10-09 15:30'), ('In Progress', '2026-10-15 10:00')], 3, ['Improvement', 'Onboarding', 'Pilot feedback'], D, H, ms='fixes')
I(18, 'After import, list skipped items with a reason',
  "\"Skipped 23\" with no list makes people assume the worst. Show the list: file, source, reason (unsupported type, permission denied, partial download, over size limit).",
  [('Todo', '2026-10-10 10:40')], 3, ['Improvement', 'Import', 'Pilot feedback'], D, D, ms='fixes')
I(19, 'Zotero: take title/authors/DOI from the parent item, not the attachment filename',
  "Zotero attachments are named whatever the PDF was called on download (`2507.01842v1.pdf`). The parent item in `zotero.sqlite` has the real title, authors and DOI. "
  "Use the parent's metadata for the card and keep the attachment path as a location.",
  [('Todo', '2026-10-10 11:30'), ('In Progress', '2026-10-14 10:00'), ('In Review', '2026-10-16 19:20')], 2, ['Import', 'Improvement'], D, D, ms='fixes',
  comments=[(D, '2026-10-16 19:15', 'Reading `zotero.sqlite` read-only via a copy (Zotero locks it while open). Parent lookup through `itemAttachments.parentItemID`. In review.')],
  attach=[('PR #219: Zotero: parent item metadata for attachments', PR.format(219))])
I(20, 'Downloads scan picks up partial downloads (.crdownload, .download, .part)',
  "Priya had 4 `.crdownload` files in Downloads that showed up as broken PDFs.",
  [('Todo', '2026-10-09 15:40'), ('In Progress', '2026-10-10 14:00'), ('Done', '2026-10-10 16:30')], 4, ['Bug', 'Import'], D, D, ms='fixes',
  comments=[(D, '2026-10-10 16:25', 'Ignored by extension now, and any file modified in the last 60 s is retried on the next scan instead of imported.')])
I(21, 'Import stalls on very large PDFs',
  "Priya has a 312 MB scanned textbook in Downloads. Hashing it on the import thread blocks the queue for ~40 s and the progress screen looks frozen. "
  "Hash in a worker, stream the file, and show \"hashing large file\" in the row.",
  [('Backlog', '2026-10-10 11:50')], 3, ['Bug', 'Import'], None, D)
I(22, 'Follow up with Priya: fixes + re-import',
  "Email her what we fixed (PIL-14, PIL-15, PIL-20), ask for the export zip again, and book a 15-min check-in for week 2.",
  [('Todo', '2026-10-12 18:10'), ('Done', '2026-10-13 09:30')], 3, ['Ops', 'Pilot feedback'], H, H, ms='fixes',
  comments=[(H, '2026-10-13 09:25', 'Sent. Week-2 check-in booked for Fri 10/23.')])
I(23, "Re-run Priya's import end to end after PIL-14 / PIL-15",
  "Same machine state she had on 10/9 as far as we can reproduce it: her Claude zip, ChatGPT zip, Zotero data dir copy, a listing of Downloads.",
  [('Todo', '2026-10-12 18:15'), ('In Progress', '2026-10-13 21:00'), ('Done', '2026-10-14 00:40')], 2, ['Import'], D, D, ms='fixes',
  comments=[(D, '2026-10-14 00:35', "Claude 612/612 · ChatGPT 288/288 · Zotero 760 + Downloads 454 PDFs → 987 unique (227 merged by hash/DOI) · 0 partial downloads. "
                                    "Import took 6m40s. The 312 MB book still stalls the queue (PIL-21).")], related=[14, 15])
I(24, 'Notion import (Markdown & CSV export zip)',
  "From Daniel's session (10/13). His lab notebook is in Notion: ~400 pages, 6 databases. Notion's \"Markdown & CSV\" export zip:\n\n"
  "- pages are `.md` files named `Title <32-hex id>.md`\n- databases are a `.csv` plus a folder with one `.md` per row\n- nested pages live in a folder named like the parent page\n\n"
  "Strip the id for display titles; keep it as the stable source id (rule 7 in the dedupe doc), so re-importing a new export updates instead of duplicating.",
  [('Todo', '2026-10-13 12:40'), ('In Progress', '2026-10-15 13:00')], 2, ['Feature', 'Import', 'Pilot feedback'], D, D, ms='fixes',
  comments=[(H, '2026-10-15 11:30', 'Daniel sent a sample export (12 pages, 1 database). Links between pages are relative paths with `%20` for spaces.'),
            (D, '2026-10-16 22:50', 'Pages + nested pages work on the sample. Databases next: each CSV row becomes a note whose properties go in the header.')])
I(25, 'Granola import',
  "From Daniel's session (10/13): he records every meeting in Granola and wants those notes next to his papers. There's no official export. Options:\n\n"
  "1. paste \"Copy as Markdown\" per note\n2. Granola shared links\n3. the local cache file\n\nFigure out what's stable before building anything.",
  [('Todo', '2026-10-13 12:45')], 3, ['Feature', 'Import', 'Pilot feedback'], D, D, ms='fixes',
  comments=[(D, '2026-10-14 10:10', 'The local cache is undocumented and changed between the last two versions. Not building on it. Start with shared links + markdown paste.')])
I(26, "Connect screen: replace 'Other' with named sources",
  "Daniel (10/13) looked for Notion and Granola, didn't see them, clicked **Other** expecting a list, and got a generic folder picker. His words: \"so Other means… a folder?\"\n\n"
  "Split Other into: *Folder on this Mac*, *Notion (export zip)*, *Granola (links)*, *Obsidian vault*. Anything we don't support yet: say \"coming soon\" and let them "
  "ask for it, instead of a folder picker.",
  [('Todo', '2026-10-13 12:50'), ('In Progress', '2026-10-14 15:00')], 2, ['Improvement', 'Onboarding', 'Pilot feedback'], D, D, ms='fixes',
  comments=[(H, '2026-10-13 19:20', 'Priya also hovered over Other for a while on 10/9, I didn\'t flag it then. Two for two.'),
            (D, '2026-10-14 15:05', 'Mock in Figma, going with a list of named tiles + one "Request a source" tile at the end.')],
  note="Daniel Osei's 10-13 pilot ask (confusing 'Other' category)")
I(27, 'Connect screen: say what each source will read before connecting',
  "One line under each tile: \"Reads: conversations.json from your Claude export\", \"Reads: PDFs and their Zotero metadata\". Both pilots asked \"what is it going to look at\".",
  [('Todo', '2026-10-13 13:00')], 3, ['Improvement', 'Onboarding', 'Pilot feedback'], None, D, ms='fixes')
I(28, 'Obsidian: follow symlinked folders in the vault',
  "Daniel's vault has `papers/` symlinked from Dropbox; we skip symlinks, so 0 of his ~180 paper notes came in. Follow symlinks inside the vault root, guard against loops.",
  [('Backlog', '2026-10-13 13:10')], 4, ['Bug', 'Import'], None, D)
I(29, 'Claude chats imported twice (export zip + desktop app cache)',
  "While setting up Daniel's machine (10/13): he connected both his Claude export and the Claude desktop app folder, and every conversation present in both showed up twice. "
  "Same conversation uuid on both sides.",
  [('Todo', '2026-10-13 14:30'), ('In Progress', '2026-10-13 16:00'), ('Done', '2026-10-14 13:10')], 2, ['Bug', 'Import'], D, D, ms='fixes',
  comments=[(D, '2026-10-14 13:05', 'Rule 3 now applies across sources, not just within one export: same Claude conversation uuid = one conversation, keep the copy with the '
                                    'newest `updated_at`, record both origins.')],
  attach=[('PR #216: Dedupe Claude conversations by uuid across sources', PR.format(216))], docs=['dedupe'])
I(30, 'ChatGPT shared links create duplicate conversations',
  "A conversation opened from a shared link gets its own id in the export. Match on (title, hash of first user message, create_time within 1 s) and link it to the original "
  "instead of importing a second copy.",
  [('Todo', '2026-10-14 10:30')], 4, ['Bug', 'Import'], None, D)
I(31, 'Google Drive shortcuts import as empty files',
  "Daniel's university Drive has many shortcuts (`application/vnd.google-apps.shortcut`). We import them as 0-byte files. Resolve the shortcut target, or skip with reason "
  "\"shortcut to a file you don't own\".",
  [('Backlog', '2026-10-13 15:00')], 3, ['Bug', 'Import', 'Pilot feedback'], None, H)
I(32, 'Pilot feedback synthesis (Priya + Daniel)',
  "One doc, both sessions: what worked, what broke, what they asked for, and the order we fix things in. Doc: *Pilot feedback synthesis*.",
  [('Todo', '2026-10-14 09:00'), ('In Progress', '2026-10-14 11:00')], 2, ['Pilot feedback'], D, D, ms='fixes', docs=['synth'])
I(33, 'Recruit pilot 3',
  "Options: Elena Park (after her quals, November), or one of Lena's intros. Prefer someone who is *not* a heavy AI-chat user, so we see the other end of the range.",
  [('Todo', '2026-10-14 09:10')], 2, ['Ops'], H, H, ms='convert', pids=(ENG, BRC))
I(34, "Send Daniel's gift card",
  "Same as Priya's ($100).", [('Todo', '2026-10-13 12:30'), ('Done', '2026-10-14 15:00')], 4, ['Ops'], H, H, parent=9, pids=(CO,))
I(35, 'Pilot metrics snapshot for Marcus every 2 weeks',
  "After the 10/14 call: Marcus (Northfield Angels) is interested in a $50k check into the pre-seed SAFE if the pilots convert. Send a short snapshot every two weeks: pilots "
  "onboarded, weekly active, import completeness (found vs imported from the import log), and the converted definition (PIL-36). First one Wed 10/28.",
  [('Todo', '2026-10-14 17:30')], 2, ['Ops'], H, H, proj=False, due='2026-10-28', pids=(CO,),
  note='company follow-up from the second Marcus Oyelaran call (2026-10-14)')
I(36, "Define 'converted pilot'",
  "We keep saying \"if pilots convert\" (Marcus, Lena's pitch feedback). Write it down.",
  [('Todo', '2026-10-14 17:35'), ('In Progress', '2026-10-14 21:00'), ('Done', '2026-10-15 10:15')], 2, [], D, H, ms='convert', pids=(ENG, CO),
  comments=[(D, '2026-10-14 22:40', "Proposal: converted = weekly active in 3 of the 4 weeks after onboarding (opened a note AND followed at least one provenance link that week) "
                                    "AND answers yes to \"would you pay $15/month for this\" at the week-4 check-in."),
            (H, '2026-10-15 09:50', 'Agree. Put "followed a provenance link" in the definition, otherwise opening the app counts as active. Going on the demo day slide too.'),
            (D, '2026-10-15 10:10', 'Done, added to the project description.')])
I(37, 'Link versions of the same paper instead of merging (arXiv v1 vs camera-ready)',
  "Same DOI or same arXiv id but different bytes → one paper card with versions (v1, camera-ready), newest first. Never merge on title similarity alone (dedupe rule 6). "
  "Priya had 41 such pairs between Downloads (preprints) and Zotero (published versions).",
  [('Backlog', '2026-10-10 10:25')], 3, ['Feature', 'Import'], None, D, related=[15])
I(38, 'First-run: explain the provenance trail in one sentence',
  "Candidate copy: \"Every note remembers where it came from. Click the trail to see the chats, papers and notes behind it.\"",
  [('Todo', '2026-10-15 10:30')], 4, ['Onboarding'], H, H, ms='fixes')
I(39, 'Evernote ENEX import',
  "Was on the list from the research chats.",
  [('Backlog', '2026-09-15 10:30'), ('Canceled', '2026-10-15 10:40')], 4, ['Feature', 'Import'], None, D,
  comments=[(D, '2026-10-15 10:40', 'Neither pilot uses Evernote and nobody in the chats asked twice. Canceling until someone asks.')])
I(40, 'Same PDF twice from ~/Desktop/papers and ~/Downloads',
  "Daniel (10/13): every paper he'd dragged from Downloads into `~/Desktop/papers` showed up twice.",
  [('Todo', '2026-10-13 13:20'), ('Duplicate', '2026-10-13 18:00')], 3, ['Bug', 'Import', 'Pilot feedback'], None, H, dup=15,
  comments=[(D, '2026-10-13 17:58', 'Same root cause as PIL-15 (no hash dedupe yet). Marking duplicate; the fix in #214 covers it.')])

# ---------------- write issues ----------------
by_n = {x['n']: x for x in ISSUES}
assert sorted(by_n) == list(range(1, 41))
STARTED = {'started'}


def label_obj(name): return name


for x in ISSUES:
    n = x['n']; ident = f'PIL-{n}'
    st = x['states']; final, final_t = st[-1]
    created = st[0][1]
    times = [t for _, t in st] + [c[1] for c in x['comments']]
    updated = max(times, key=J)
    started = next((t for s, t in st if STATUSES[s]['type'] in STARTED), None)
    completed = final_t if final == 'Done' else None
    canceled = final_t if final in ('Canceled', 'Duplicate') else None
    hist = []
    for i, (s, t) in enumerate(st):
        hist.append(dict(state=dict(id=STATUSES[s]['id'], name=s, type=STATUSES[s]['type']), startedAt=L(t),
                         endedAt=L(st[i + 1][1]) if i + 1 < len(st) else None))
    issue = dict(
        id=ident, uuid=uid(f'linear/issue/{ident}'), title=x['title'], description=x['desc'],
        projectMilestone=dict(id=MILESTONES[x['ms']]['id'], name=MILESTONES[x['ms']]['name']) if x['ms'] else None,
        priority=dict(value=x['prio'], name=PRIO[x['prio']]), estimate=None,
        url=f'https://linear.app/mathetic/issue/{ident}/{slug(x["title"])}',
        gitBranchName=f'david/{ident.lower()}-{slug(x["title"], 55)}',
        createdAt=L(created), updatedAt=L(updated), archivedAt=None, completedAt=L(completed) if completed else None,
        startedAt=L(started) if started else None, canceledAt=L(canceled) if canceled else None, dueDate=x['due'],
        status=final, statusType=STATUSES[final]['type'], labels=x['labels'], createdBy=x['creator'], assignee=x['assignee'],
        project=PROJECT_NAME if x['proj'] else None, projectId=PROJECT_ID if x['proj'] else None,
        parentId=f"PIL-{x['parent']}" if x['parent'] else None, team='Pilots', cycleId=None)
    rel = dict(blocks=[], blockedBy=[], relatedTo=[dict(id=f'PIL-{r}', title=by_n[r]['title']) for r in x['related']],
               duplicateOf=dict(id=f"PIL-{x['dup']}", title=by_n[x['dup']]['title']) if x['dup'] else None)
    detail = dict(id=ident,
                  attachments=[dict(id=uid(f'linear/att/{ident}/{u}'), title=t, subtitle=None, url=u) for t, u in x['attach']],
                  documents=[dict(id=DOCS[k][0], title=DOCS[k][1]) for k in x['docs']],
                  stateHistory=hist, relations=rel, releases=[])
    comments = []
    for i, (who, t, body) in enumerate(x['comments']):
        comments.append(dict(id=uid(f'linear/comment/{ident}/{i}'), body=body, attachments=[], createdAt=L(t), updatedAt=L(t), parentId=None,
                             resolvedAt=None, quotedText=None, author=dict(id=USERS[who]['id'], name=who), onBehalfOf=None))
    comments.reverse()  # newest first, like list_comments
    note = f"'{x['title']}'; status={final}; project={PROJECT_NAME if x['proj'] else None}; {len(comments)} comments"
    if x['note']: note += f'; {x["note"]}'
    g.json(f'{W}/issues/{ident}.json', dict(issue=issue, detail=detail, comments=comments), J(created), J(updated), indent=2,
           account=ACCT, project_ids=x['pids'], modeled_on=MOD.format('issues/<id>.json'), notes=note)

# ---------------- documents ----------------
DOC_BODY = {}
DOC_BODY['script'] = ("""Pilot sessions are 45 minutes over Zoom with screen share. One of us runs the script, the other takes notes and does not talk. Send the consent one-pager (PIL-3) and the dmg two days before. Ask about recording at the start even if they said yes by email.

## Before the call

* Pilot has: the signed dmg installed, their Claude and/or ChatGPT export **downloaded** (exports take up to a day to arrive), Zotero closed.
* We have: the import log path ready (`~/Library/Application Support/Engelbart/import-log.jsonl`), a timer, this doc open.

## 1. Context (5 min)

> "Engelbart is a research notebook that remembers where your thoughts came from. Today you'll connect a few of your sources, import them, and then we'll look at one idea together. Nothing leaves your laptop. We're testing the product, not you; if something is confusing, that's on us."

## 2. Connect + import (15 min, pilot drives)

* Don't help unless they're stuck for more than 60 seconds. Note where they hesitate.
* Q1. Before you click anything: what do you expect this screen to do?
* Q2. (after connecting) What do you think it is going to read?
* Q3. (during import) What would you do while this runs?

## 3. Follow one idea (15 min)

* Q4. Think of something you were working on in the last month. Can you find it here?
* Q5. Where do you think this note came from? (then show the trail if they don't find it)
* Q6. Is anything here that shouldn't be? Anything missing that should be?
* Q7. Did you see the same thing twice anywhere?

## 4. Debrief (10 min)

* Q8. What would make you open this next week?
* Q9. Is there anywhere your research lives that you didn't connect? Why not?
* Q10. What would make you stop using it?
* Ask for the import log file. Explain the week-1 and week-4 check-ins and the gift card.

## Don'ts

* Don't say "was that confusing". Say "what did you expect to happen".
* Don't demo features they didn't reach on their own until section 3.
* Don't fix bugs live. Write them down with the time.
""", '2026-09-21 10:40', '2026-09-22 16:35', D, D)
DOC_BODY['dedupe'] = ("""Rules for deciding when two imported things are the same thing. Written after Priya's session (10/9: PIL-14, PIL-15). Evaluate in this order; the first rule that matches wins. **Merging** means one card that lists every location and origin. **Linking** means separate items shown as versions or related. When in doubt we link, never merge: a wrong merge loses data, a missed merge is only clutter.

## Rule 1: same content hash → merge

* Key: sha256 of the file bytes (PDFs, images, docx, any file).
* Primary location: the earliest one we saw; the others are listed under "Also found in".
* Example: Priya's `~/Zotero/storage/8KQ2M4ZD/…Productive Struggle or Silent Stalling.pdf` and `~/Downloads/2507.01842v1.pdf` are byte-identical → one card.

## Rule 2: same DOI → same paper

* Key: DOI, lowercased, `https://doi.org/` and `doi:` prefixes stripped, trailing punctuation stripped.
* Same DOI + same hash → already merged by rule 1.
* Same DOI + different bytes → **link as versions** of one paper (PIL-37), newest first.
* DOI sources: Zotero parent item, PDF metadata, first page text (regex), BibTeX.

## Rule 3: same Claude conversation uuid → merge, across every source

* Key: the conversation `uuid`. Applies across exports, re-exports and the Claude desktop app cache (PIL-29).
* Keep the copy with the newest `updated_at`; record every origin.
* **Never** key on `name`. Untitled conversations all have `name: ""` (this caused PIL-14).

## Rule 4: same ChatGPT conversation_id → merge

* Shared-link copies have their own id: handled by PIL-30, link not merge.

## Rule 5: same arXiv id → same paper

* Key: arXiv id without the version suffix (`2507.01842`).
* Different version suffix (v1, v2) → link as versions.

## Rule 6: title similarity alone never merges

* Same or near-same title with no shared hash/DOI/arXiv id → show under "Possible duplicates" for the user to confirm. Reason: workshop and journal versions with the same title can have different content, and notes called "Notes" or "Untitled" are not duplicates of each other.

## Rule 7: stable source ids from note tools

* Notion: the 32-hex page id at the end of each exported filename. A new export of the same page updates the note.
* Obsidian: vault-relative path + file creation time.
* Granola: note id from the shared link.
* Gmail: `Message-ID` header. Same Message-ID in two mailboxes → one email.

## Rule 8: Zotero attachment and its parent item are one card

* The parent item gives title, authors, DOI (PIL-19). The attachment gives the bytes and the path.

## Rule 9: things we ignore entirely

* Partial downloads: `.crdownload`, `.download`, `.part`, and any file modified in the last 60 seconds (retry next scan).
* 0-byte files and Drive shortcuts we can't resolve (PIL-31): skipped with a reason, listed after import (PIL-18).

## Not covered yet

* The same text pasted into two different notes (would need near-duplicate text detection).
* A chat that quotes a paper vs. the paper itself: related, not duplicates. That's the provenance trail's job, not dedupe's.
""", '2026-10-10 11:05', '2026-10-15 09:20', D, D)
DOC_BODY['synth'] = ("""Two sessions so far: **Priya Raman** (Berkeley, education + HCI PhD student; Fri 10/9) and **Daniel Osei** (CMU postdoc; Tue 10/13). Both ran the full script (*Pilot interview script*). Import logs received from both.

## What worked

* The provenance trail. Priya: clicking a note and seeing the three chats and the PDF behind it was "the thing I actually want". Daniel asked if he could send a trail to his advisor.
* Import speed was fine for both once it started (Priya ~7 min, Daniel ~4 min).
* Nobody worried about privacy after reading the one-pager.

## What broke

| Problem | Who | Issue | Status |
| -- | -- | -- | -- |
| ~140 Claude chats missing (Projects + untitled) | Priya | PIL-14 | fixed, 612/612 |
| Same PDF twice (Zotero vs Downloads) | Priya, Daniel | PIL-15 / PIL-40 | fixed: 1,214 → 987 |
| Claude chats twice (export + desktop cache) | Daniel | PIL-29 | fixed |
| Partial downloads shown as broken PDFs | Priya | PIL-20 | fixed |
| 312 MB PDF stalls the queue | Priya | PIL-21 | backlog |
| Symlinked Obsidian folder skipped | Daniel | PIL-28 | backlog |
| Drive shortcuts as empty files | Daniel | PIL-31 | backlog |

## What they asked for

* Daniel: **Notion** import (his lab notebook, ~400 pages) and **Granola** import (all his meetings). PIL-24, PIL-25.
* Both: say what each source will read before connecting (PIL-27).
* Priya: version links for preprint vs published PDFs (PIL-37).

## The connect screen's "Other"

Both of them hovered over **Other** and neither knew what it meant. Daniel clicked it expecting a list and got a folder picker. This is the clearest onboarding problem we have. PIL-26 replaces it with named sources.

## Order of work (until the week-2 check-ins, 10/23 and 10/27)

1. PIL-26 connect screen without "Other"
2. PIL-24 Notion import (Daniel's main source)
3. PIL-17 trail as step 1 of the tour
4. PIL-19 Zotero parent metadata
5. PIL-18 skipped list

## Open questions

* Is a "Request a source" tile enough for Granola until we know what's stable?
* Do we count Daniel as active if he only uses Notion-imported notes? (Yes, by the PIL-36 definition, as long as he follows trails.)
* Pilot 3: someone who doesn't live in AI chats (PIL-33).
""", '2026-10-14 11:10', '2026-10-16 21:05', D, H)

for key, (body, c, m, creator, updater) in DOC_BODY.items():
    did, title = DOCS[key]
    doc = dict(id=did, title=title, content=body, url=f'https://linear.app/mathetic/document/{slug(title)}-{hexid("linear/docslug/" + key, 12)}',
               createdAt=L(c), updatedAt=L(m), archivedAt=None, creator=dict(id=USERS[creator]['id'], name=creator),
               updatedBy=dict(id=USERS[updater]['id'], name=updater), project=dict(id=PROJECT_ID, name=PROJECT_NAME), initiative=None, team=None, issue=None)
    g.json(f'{W}/documents/{did}.json', doc, J(c), J(m), indent=2, account=ACCT, project_ids=[ENG],
           modeled_on=MOD.format('documents/<uuid>.json'), notes=f"'{title}'; project={PROJECT_NAME}" + ('; concrete dedupe rules (content hash, DOI, Claude conversation uuid, arXiv id, ...)' if key == 'dedupe' else ''))

# ---------------- project ----------------
P_URL = f'https://linear.app/mathetic/project/pilot-program-{hexid("linear/projslug", 12)}'
done_in = lambda k: [x for x in ISSUES if x['ms'] == k]
for k, ms in MILESTONES.items():
    xs = done_in(k)
    if xs: ms['progress'] = round(100 * sum(1 for x in xs if x['states'][-1][0] in ('Done', 'Canceled', 'Duplicate')) / len(xs), 2)
updates = [
    dict(body="## Pilot 1 done (Priya, 10/9)\n\n* Import missed 141 of her 612 Claude conversations: everything inside Claude Projects plus untitled chats collapsing on the dedupe key. "
              "Root-caused, fix in review (PIL-14).\n* Same PDFs twice from Zotero and Downloads (PIL-15). *Import dedupe rules v0* written; hash + DOI dedupe in progress.\n"
              "* Best moment: the provenance trail. Moving it to step 1 of the tour (PIL-17).\n\nNext: Daniel on Tuesday 10/13.",
         health='onTrack', t='2026-10-10 18:20', who=D,
         diff="**Status**: In Progress\n**Target date** set to Nov 13th\n\n*Progress since Oct 3*: 31% → 46%"),
    dict(body="Both pilots onboarded.\n\n* Priya re-import: Claude 612/612, 987 unique PDFs from 1,214 files (PIL-23).\n"
              "* Daniel: blocked on Notion and Granola import (PIL-24, PIL-25) and confused by the connect screen's \"Other\" (PIL-26, Priya hit it too).\n"
              "* \"Converted pilot\" is defined (PIL-36) and goes on the demo day slide.\n\n"
              "**Risk:** pilot 3 isn't recruited (PIL-33), so *3 converted pilots* by 11/13 is at risk even if both current pilots convert.",
         health='atRisk', t='2026-10-16 17:40', who=H,
         diff="**Status**: In Progress\n\n*Progress since Oct 10*: 46% → 63%"),
]
status_updates = []
for i, u in enumerate(updates):
    sid_ = uid(f'linear/projupdate/{i}')
    status_updates.append(dict(id=sid_, body=u['body'], health=u['health'], url=f'{P_URL}/activity#project-update-{sid_[:8]}', createdAt=L(u['t'] + ':00'),
                               updatedAt=L(u['t'] + ':02'), editedAt=None, archivedAt=None, diffMarkdown=u['diff'], isDiffHidden=False,
                               user=dict(id=USERS[u['who']]['id'], name=u['who']), type='project', project=dict(id=PROJECT_ID, name=PROJECT_NAME)))
status_updates.reverse()
project = dict(
    id='P-PIL-1', uuid=PROJECT_ID, icon='Users', color='#4cb782', name=PROJECT_NAME,
    summary='Onboard 3 researchers onto Engelbart, fix what breaks, and get them weekly active.',
    description="Pilot users run Engelbart on their own machines with their real chats, papers and notes. We watch the first import live, then check in at weeks 1, 2 and 4.\n\n"
                "**Converted pilot** (PIL-36): weekly active in 3 of the 4 weeks after onboarding (opened a note *and* followed at least one provenance link that week) "
                "and says yes to \"would you pay $15/month\" at the week-4 check-in.\n\nPilots: Priya Raman (UC Berkeley, 10/9), Daniel Osei (CMU, 10/13), pilot 3 TBD.",
    url=P_URL, trashed=False, resourceCount=3, createdAt=L('2026-09-14 20:20'), updatedAt=L('2026-10-16 17:40:02'), startedAt=L('2026-09-15 09:00'),
    completedAt=None, canceledAt=None, startDate='2026-09-15', startDateResolution=None, targetDate='2026-11-13', targetDateResolution=None,
    priority=dict(value=1, name='Urgent'), labels=[], initiatives=[], lead=dict(id=USERS[D]['id'], name=D),
    leadTeam=dict(id=TEAM['id'], name='Pilots', key='PIL'), status=dict(id=uid('linear/projstatus/started'), name='In Progress', type='started'),
    teams=[dict(id=TEAM['id'], name='Pilots', key='PIL')])
pcomments = [dict(id=uid('linear/projcomment/0'), body='Demo day is 11/19, so the "3 converted pilots" milestone has to land the week before. No slack in this.',
                  attachments=[], createdAt=L('2026-10-05 21:30'), updatedAt=L('2026-10-05 21:30'), parentId=None, resolvedAt=None, quotedText=None,
                  author=dict(id=USERS[H]['id'], name=H), onBehalfOf=None)]
g.json(f'{W}/projects/P-PIL-1.json', dict(project=project, milestones=dict(milestones=list(MILESTONES.values())),
                                          status_updates=dict(statusUpdates=status_updates, hasNextPage=False), comments=pcomments),
       J('2026-09-14 20:20'), J('2026-10-16 17:40:02'), indent=2, account=ACCT, project_ids=[ENG, CO],
       modeled_on=MOD.format('projects/P-MATH-<n>.json'), notes=f"project '{PROJECT_NAME}' (team Pilots): 4 milestones, 2 status updates")

# ---------------- workspace ----------------
WS_META = dict(account=ACCT, modeled_on=MOD.format('workspace/<name>.json'))
g.json(f'{W}/workspace/workspace.json', dict(id=uid('linear/workspace'), name='Mathetic', url='https://linear.app/mathetic'),
       '2026-09-14 20:02', '2026-09-14 20:02', indent=2, project_ids=[CO], notes='workspace metadata (synthetic export)', **WS_META)
g.json(f'{W}/workspace/teams.json', dict(teams=[TEAM], hasNextPage=False), '2026-09-14 20:04', '2026-10-13 18:30', indent=2, project_ids=[ENG],
       notes='team list: synthetic Pilots team (PIL)', **WS_META)
g.json(f'{W}/workspace/users.json', dict(users=list(USERS.values()), hasNextPage=False), '2026-09-14 20:12', '2026-10-17 05:41', indent=2,
       project_ids=[CO], notes='workspace members', **WS_META)
g.json(f'{W}/workspace/labels.json', dict(labels=[dict(id=uid(f'linear/label/{n}'), name=n, color=c, description=d, archivedAt=None) for n, c, d in LABELS],
                                         hasNextPage=False), '2026-09-14 20:30', '2026-09-20 11:00', indent=2, project_ids=[ENG],
       notes='issue labels for the Pilots team', **WS_META)
g.json(f'{W}/workspace/statuses.json', list(STATUSES.values()), '2026-09-14 20:04', '2026-09-14 20:04', indent=2, project_ids=[ENG],
       notes='workflow states for the Pilots team', **WS_META)
cycles = [dict(id=uid('linear/cycle/1'), number=1, name='Pilot week 1', startsAt=L('2026-10-05 00:00'), endsAt=L('2026-10-12 00:00'),
               completedAt=L('2026-10-12 00:00'), progress=0.82, team=dict(id=TEAM['id'], key='PIL')),
          dict(id=uid('linear/cycle/2'), number=2, name='Pilot week 2', startsAt=L('2026-10-12 00:00'), endsAt=L('2026-10-19 00:00'),
               completedAt=None, progress=0.47, team=dict(id=TEAM['id'], key='PIL'))]
g.json(f'{W}/workspace/cycles.json', cycles, '2026-10-04 22:00', '2026-10-17 01:00', indent=2, project_ids=[ENG], notes='Pilots team cycles', **WS_META)
g.json(f'{W}/workspace/custom_views.json', dict(customViews=[dict(id=uid('linear/view/pilot-bugs'), name='Pilot bugs',
                                                                   description='Pilot feedback + Bug, not done', shared=True,
                                                                   filterData={'labels': {'name': {'in': ['Pilot feedback', 'Bug']}},
                                                                               'state': {'type': {'nin': ['completed', 'canceled', 'duplicate']}}},
                                                                   createdAt=L('2026-10-10 12:00'), owner=dict(id=USERS[D]['id'], name=D))],
                                                hasNextPage=False), '2026-10-10 12:00', '2026-10-10 12:00', indent=2, project_ids=[ENG],
       notes='saved view: open pilot bugs', **WS_META)
g.finish()
