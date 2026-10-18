"""Synthetic Apple Notes (iCloud account; folders Notes, Training, Personal). Same shape as the real AppleScript export:
first line `<!-- apple-notes-export {json meta} -->`, then the note body as Notes.app HTML (<div> per line, <ul><li>, <h1>).
One item per .html file."""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('apple-notes')
STORE = 'SYNTH-' + hexid('apple-notes-store', 8).upper() + '-' + hexid('apple-notes-store-2', 4).upper()
MOD = 'authentic/apple-notes/iCloud/<folder>/<title>.html (AppleScript body HTML + apple-notes-export meta comment)'
N = [0]


def fname(title):
    t = title.replace('/', '-').replace(':', '-')
    return t if len(t) <= 64 else t[:63].rstrip() + '…'


def body_html(lines):
    """lines: list of str (plain line, '' = blank), ('h1'|'h2', text), ('ul', [items]), ('check', [(done, text)]), ('b', text)."""
    out = []
    for ln in lines:
        if isinstance(ln, str):
            out.append(f'<div>{html.escape(ln)}<br></div>' if ln else '<div><br></div>')
        elif ln[0] in ('h1', 'h2'):
            out.append(f'<div><{ln[0]}>{html.escape(ln[1])}</{ln[0]}></div>')
        elif ln[0] == 'b':
            out.append(f'<div><b>{html.escape(ln[1])}</b></div>')
        elif ln[0] == 'ul':
            out.append('<ul>\n' + '\n'.join(f'<li>{html.escape(x)}</li>' for x in ln[1]) + '\n</ul>')
        elif ln[0] == 'ol':
            out.append('<ol>\n' + '\n'.join(f'<li>{html.escape(x)}</li>' for x in ln[1]) + '\n</ol>')
        elif ln[0] == 'check':
            out.append('<ul class="checklist">\n' + '\n'.join(
                f'<li class="{"checked" if d else "unchecked"}">{html.escape(x)}</li>' for d, x in ln[1]) + '\n</ul>')
    return '\n'.join(out) + '\n'


def anote(folder, title, created, modified, lines, projects, notes=''):
    N[0] += 1
    c, m = dt(created), dt(modified)
    meta = {"id": f"x-coredata://{STORE}/ICNote/p{100 + N[0]}", "account": "iCloud", "folder": folder, "title": title,
            "created": c.astimezone(PT).strftime('%Y-%m-%dT%H:%M:%S'), "modified": m.astimezone(PT).strftime('%Y-%m-%dT%H:%M:%S'), "password_protected": "false"}
    first = '<!-- apple-notes-export ' + json.dumps(meta, ensure_ascii=False) + ' -->\n'
    rel = f'iCloud/{folder}/{fname(title)}.html'
    g.text(rel, first + body_html(lines), c, m, account=f'iCloud / {folder}', project_ids=projects, modeled_on=MOD, notes=notes,
           source=f'Notes.app via AppleScript ({meta["id"]})')


# ================= Notes =================
anote('Notes', 'ClarityX', '2025-10-21 01:14', '2025-10-23 22:40', [
    ('h1', 'ClarityX'),
    '',
    'X is the unknown. we give clarity on the unknown.',
    '',
    'the one-liner is the whole thing so far. what it could be:',
    ('ul', ['you paste in something you don\'t understand (a contract clause, a stats method, a lab protocol) and it tells you what you\'d need to know to understand it, in order',
            'not an explainer, a map of the unknowns. "you\'re missing 3 things: what a random effect is, why they log-transformed, what n means here"',
            'X = the variable. every question has one']),
    '',
    'why not: chatgpt already kind of does this if you ask well. the value would only be in the "order of unknowns" part',
    '',
    '10/23 — shelving. not a company. maybe a feature of something else',
], ['project_clarityx'], notes='ClarityX one-liner idea note (Oct 2025), shelved two days later')

anote('Notes', 'New Note', '2026-03-26 00:52', '2026-03-26 01:03', [
    'kappa table — per pair not just overall??',
    'r1/r2 .74  r1/r3 .69  r2/r3 .70 → 0.71 avg',
    '',
    'ask yan if appendix ok',
    'fig 3 grayscale',
    'abstract under 150',
], ['project_tutortrace'], notes='HARD CASE: vague title — "New Note" holding TutorTrace UIST-crunch kappa numbers (3 raters, 0.71)')

anote('Notes', 'asdf', '2026-05-12 13:20', '2026-05-12 13:21', [
    'oat milk',
    'the thing for the bike chain',
    'return amazon box by thurs',
], ['project_none'], notes='HARD CASE: vague title — "asdf" errand fragment; personal clutter')

anote('Notes', 'VizPI deploy 2 — lab checklist', '2025-11-11 22:05', '2025-11-12 17:48', [
    ('h1', 'VizPI deploy 2 — CS 3114 — Wed 11/12 3:30'),
    '',
    ('check', [(True, 'confirm room + projector w/ John'),
               (True, 'backend on the lab box, pm2 restart, check /health'),
               (True, 'seed 87 student accounts from the roster csv'),
               (True, 'TA logins x3 (sections A and B)'),
               (True, 'consent slide first 2 min'),
               (False, 'second laptop as hot spare'),
               (True, 'export telemetry right after, before anyone touches the db')]),
    '',
    ('b', 'during'),
    '3:52 section B dashboard frozen, students still typing',
    'websocket not reconnecting after the wifi blip — events dropping',
    '4:10 hotfix pushed (reconnect w/ backoff + resend buffer). B looks alive again',
    'guess ~12% of B events lost between 3:50 and 4:10. note it in the data README',
    '',
    ('b', 'after'),
    ('ul', ['dump done 5:30, 2 files, checksum in slack',
            'labeling sprint fri 11/14 → 11/21 w/ Minsun + Xiaohang',
            'add "stalled-after-error" to the guide? lots of that today']),
], ['project_vizpi'], notes='deployment-day checklist for VizPI deployment #2 (2025-11-12)')

anote('Notes', 'leave of absence — ask Grace', '2026-07-20 23:30', '2026-07-31 15:10', [
    ('h1', 'leave of absence — ask Grace'),
    '',
    ('ol', ['which form — the graduate school one or the dept one first?',
            'does Yan sign before or after the dept head',
            'what happens to GRA funding — ends 8/15?',
            'health insurance through the fall? (just ask what the policy is)',
            'does the clock on quals pause',
            'how do I come back — just re-enroll or a new form',
            'can I keep my vt email + library access']),
    '',
    '7/31 — signed. effective fall 2026. GRA ends 8/15. email + library stay. return = re-enrollment form by the deadline the semester before',
], ['project_vt_phd_admin'], notes='questions for Grace Kim before the leave-of-absence form (signed 2026-07-31)')

anote('Notes', 'Lena — kickoff questions', '2026-08-10 21:40', '2026-08-11 16:25', [
    'surplus kickoff tmrw 10am',
    '',
    ('ul', ['what does "weekly update" mean, written or a call',
            'demo day date + format',
            'who else is in the house and what are they building',
            'is there a shared calendar for office hours w/ mentors',
            'can Hudson stay over when he visits',
            'mail address for the PBC stuff — use the house?']),
    '',
    'answers: written, friday by 6pm. demo day TBD (winter). office hours in notion lol. mail: yes use the house address for now',
], ['project_mathetic_company'], notes='prep for Surplus kickoff with Lena Hoffmann (2026-08-11)')

anote('Notes', 'Berkeley chats — what to ask', '2026-09-07 22:10', '2026-09-08 23:40', [
    ('h1', 'Berkeley chats — what to ask'),
    '',
    'not a sales call. 30 min. listen',
    '',
    ('ol', ['walk me through the last time you had an idea for your research. where did you write it down first?',
            'how many places do your papers live? (zotero, downloads, slack, email…)',
            'when you go back to an old idea, how do you find where it came from?',
            'show me your notes app right now (if ok)',
            'what did you try and stop using? why?',
            'would you let a tool read your chats with claude/chatgpt?']),
    '',
    'Elena 9/9 (learning sciences), Priya 9/10, Ben 9/16 on zoom',
    'record only if they say yes. granola otherwise',
], ['project_berkeley_research_chats'], notes='interview guide notes for the Berkeley research chats (Sep 2026)')

anote('Notes', 'UIST talk — opening lines', '2026-09-27 23:12', '2026-10-05 22:58', [
    ('h1', 'opening lines'),
    '',
    'v1: "Picture a CS1 lab at 4pm. Thirty students, two TAs, and an AI assistant that never gets tired." — too slow',
    '',
    'v2: "When a student stops typing for ninety seconds, are they thinking or are they stuck?" — better. ask it, pause, then the replay clip',
    '',
    'v3 (Yan): start with the replay clip, no words for 10s, then v2. ← doing this',
    '',
    ('b', 'then'),
    ('ul', ['one sentence on why TAs can\'t tell: they see the student, not the history',
            'TutorTrace = replay + 4 labels + a TA view',
            'don\'t say "novel". don\'t apologize for one course, it\'s in limitations',
            'end of intro: "we labeled 2,340 windows with three raters, kappa 0.71"']),
    '',
    'closing: "the pause is information. the question is who gets to see it." — keep',
], ['project_tutortrace'], notes='UIST 2026 talk opening drafts (talk 2026-10-07)')

anote('Notes', 'Priya onboarding — what she said', '2026-10-09 14:05', '2026-10-09 15:20', [
    'pilot 1 · Priya · 10/9 11am',
    '',
    ('ul', ['"where are my claude chats" — import got some but she has way more. she estimates 140+ missing',
            'Ostrowski paper twice (zotero + downloads). "is it broken?"',
            'liked the trail: clicked a note → saw the chat it came from → "oh that\'s the thing"',
            'connect screen ok for her, she just clicked everything',
            'wants to tag by chapter of her dissertation not by project']),
    '',
    'fix first: claude pagination (we stop at some page?), dedupe by hash + DOI',
    'follow up mon w/ a fresh import',
], ['project_engelbart'], notes='quick notes during Engelbart pilot onboarding with Priya Raman (2026-10-09)')

anote('Notes', 'connect screen "Other"', '2026-10-13 18:30', '2026-10-13 19:02', [
    'Daniel (pilot B) today:',
    '"what goes in Other?" — he dragged a zip of his Notion export there and nothing happened',
    'he expected Notion + Granola as real tiles',
    '',
    ('b', 'ideas'),
    ('ul', ['kill "Other". replace w/ "drop files" + a list of every importer incl. coming-soon ones',
            'detect notion zips and route them',
            'show a count after import per source so people can tell if something is missing']),
], ['project_engelbart'], notes='connect-screen feedback from pilot B (Daniel Osei, 2026-10-13)')

anote('Notes', 'beat idea 92 bpm', '2026-01-18 01:40', '2026-01-18 01:52', [
    '92 bpm, F minor',
    'chop the rhodes sample at bar 3, pitch down 2 st',
    'kick on 1 and the "and" of 2, no snare on 4 — clap + rim instead',
    'hats swung 58%',
    '808 slides on the last bar of every 8',
    'name: "half step"',
], ['project_music_production'], notes='beat idea (FL Studio)')

anote('Notes', 'books', '2025-11-30 22:10', '2026-06-02 21:45', [
    ('h1', 'books'),
    '',
    ('b', 'reading'),
    ('ul', ['The Sleepwalkers — Clark (halfway, very good on how alliances lock in)']),
    ('b', 'next'),
    ('ul', ['Destined for War — Allison',
            'The Strategy of Conflict — Schelling',
            'Chip War — Miller (Owen recommended)',
            'The Grand Chessboard — Brzezinski']),
    ('b', 'done'),
    ('ul', ['The Guns of August', 'Thinking in Systems']),
], ['project_none'], notes='personal clutter: geopolitics / grand strategy reading list (PERSON.md §5)')

anote('Notes', 'parking appeal', '2026-02-24 16:02', '2026-02-24 16:30', [
    'ticket from the Perry St lot 2/20',
    'had a valid permit, it was on the dash but flipped face down',
    'appeal online within 10 business days',
    'photo of permit + receipt from the parking portal',
    'submitted 2/24 4:28pm',
], ['project_none'], notes='personal clutter: VT parking ticket appeal (PERSON.md §5)')

# ================= Personal =================
anote('Personal', 'groceries', '2026-02-01 11:20', '2026-02-01 12:05', [
    ('check', [(True, 'chicken thighs 3 lb'), (True, 'greek yogurt x2'), (True, 'eggs 18'), (True, 'jasmine rice'),
               (False, 'frozen broccoli'), (True, 'bananas'), (True, 'oats'), (False, 'salsa'), (True, 'cottage cheese')]),
], ['project_none'], notes='HARD CASE: personal clutter — grocery list (Blacksburg)')

anote('Personal', 'Grocery list', '2026-08-13 18:40', '2026-08-13 19:25', [
    'trader joe\'s on masonic',
    ('check', [(True, 'ground turkey'), (True, 'skyr'), (True, 'rice'), (True, 'bagged salad'), (True, 'frozen berries'),
               (False, 'whey (order online, TJ doesn\'t have it)'), (True, 'eggs'), (True, 'sourdough'),
               (True, 'coffee'), (False, 'paper towels for the house')]),
    '',
    'house fridge shelf = 2nd from top',
], ['project_none'], notes='HARD CASE: personal clutter — grocery list (SF)')

anote('Personal', 'SF apartment viewings', '2026-07-26 20:10', '2026-08-02 23:30', [
    ('h1', 'SF apartment viewings'),
    '',
    'budget: room ≤ $1,900 or studio ≤ $2,600. close to Surplus or the N line',
    '',
    ('b', '7/27 — Inner Sunset room (video tour)'),
    ('ul', ['$1,750, 3 roommates, all grad students', 'small window, fog lol', 'lease starts 9/1 — too late']),
    ('b', '7/28 — Mission studio (video tour)'),
    ('ul', ['$2,550, tiny, no laundry', 'landlord wants 2x deposit + proof of income, I have neither right now']),
    ('b', '7/30 — sublet in Hayes Valley'),
    ('ul', ['$1,850 aug–oct, furnished', 'she\'s back in nov so it\'s only 3 months', 'maybe as a bridge?']),
    '',
    '8/2 — decided: just stay at the Surplus house first, look again in Nov once there\'s money',
], ['project_none'], notes='personal clutter: SF apartment search (Jul–Aug 2026, PERSON.md §5)')

anote('Personal', 'packing — Dublin', '2026-06-30 22:15', '2026-07-08 07:40', [
    'Niamh\'s wedding — RSVP\'d yes, fly out 7/9',
    '',
    ('check', [(True, 'passport (expires 2029, ok)'), (True, 'suit + 2 shirts'), (True, 'dress shoes'),
               (True, 'running stuff (2 sets)'), (True, 'adapter type G'), (True, 'laptop + charger'),
               (False, 'gift — buy at the airport?'), (True, 'card for the couple')]),
    '',
    'cousin\'s address is in the email from her, not here',
], ['project_none'], notes='personal clutter: packing list for a cousin\'s wedding trip (logistics only)')

anote('Personal', 'moving out — blacksburg', '2026-07-21 21:00', '2026-08-07 09:15', [
    ('h1', 'moving out'),
    '',
    ('check', [(True, 'tell landlord (30 days)'), (True, 'sell desk + chair (fb marketplace)'), (True, 'donate winter stuff I won\'t need'),
               (True, 'ship bike (bikeflights) — derailleur still bent, fix in SF'), (True, 'cancel internet'),
               (True, 'forward mail (USPS)'), (True, 'car: register in CA within 20 days of moving?? check'),
               (True, 'return lab keys to Yan'), (False, 'final walkthrough photos')]),
    '',
    'flight 8/8 6:05am ROA → CLT → SFO',
], ['project_none'], notes='personal clutter: moving checklist (move 2026-08-08)')

anote('Personal', 'new mac setup', '2026-08-04 19:30', '2026-08-05 23:10', [
    'm4 pro, 48gb',
    '',
    ('ol', ['migrate nothing. fresh', 'homebrew → git, gh, node, pnpm, uv, ffmpeg, ripgrep',
            'iterm + zsh config from dotfiles repo', 'claude code, then log in',
            'obsidian + open both vaults', 'FL Studio (license re-activate, 1 of 2)', 'zotero + sync',
            'turn off "natural" scrolling', 'key repeat fastest']),
    '',
    'old mac: wipe after a week if nothing missing',
], ['project_none'], notes='personal clutter: laptop setup notes (new Mac 2026-08-04)')

anote('Personal', 'house stuff', '2026-08-09 10:05', '2026-08-20 08:40', [
    'surplus house',
    '',
    ('ul', ['wifi: network "surplus-main" (pw on the card by the router — don\'t write it here)',
            'guest network for visitors is the other one',
            'trash: green/blue/black bins out sun night',
            'Sam is in room 2, works nights, quiet after 11',
            'gym: the one on 16th has a 10% founder discount via Lena',
            'laundry downstairs, quarters app']),
], ['project_none'], notes='personal clutter: house/Wi-Fi info at the SF house (no passwords stored)')

anote('Personal', 'derailleur', '2026-05-09 12:30', '2026-08-16 17:10', [
    'rear derailleur hanger bent after the bike fell over at the rack',
    'shifting skips in 3 lowest gears',
    '',
    'shop said: new hanger ~$30, alignment $20',
    'or do it myself, need hanger alignment tool',
    '',
    '8/16 — done at the shop on valencia. $48 total. shifts clean',
], ['project_none'], notes='personal clutter: broken bike derailleur (PERSON.md §5)')

anote('Personal', 'taxes 2025', '2026-03-08 20:00', '2026-04-11 21:30', [
    'docs to collect:',
    ('check', [(True, 'W-2 from VT (GRA)'), (True, '1098-T'), (True, '1099-INT'), (True, 'last year\'s return for reference'),
               (True, 'state return — VA')]),
    '',
    'file after UIST. not before.',
    '4/11 — filed both. done.',
], ['project_none'], notes='personal clutter: 2025 taxes checklist (no amounts or ids)')

anote('Personal', 'chess openings to study', '2026-01-04 21:10', '2026-04-15 22:40', [
    ('h1', 'chess openings to study'),
    '',
    'white: london is fine but boring. try the italian w/ c3-d4 for a month',
    'black vs e4: caro-kann (main lines to move 10)',
    'black vs d4: QGD, stop playing the dutch in rapid',
    '',
    ('b', 'mistakes I keep making'),
    ('ul', ['castling into a pawn storm in opposite-side positions',
            'trading my good bishop', 'flagging in won positions in 3+0 → play 10+0']),
    '',
    'rating 1720 rapid (jan) → 1785 (apr)',
], ['project_none'], notes='personal clutter: online chess (PERSON.md §5)')

# ================= Training =================
anote('Training', 'zone 2 HR', '2025-10-29 07:30', '2025-11-19 06:55', [
    ('h1', 'zone 2'),
    '',
    'LT1 from the drift test 10/26: ~148. zone 2 = 135–148',
    'easy pace at 145 avg: 8:25–8:45/mi (was 9:10 in july)',
    '',
    ('b', 'rules'),
    ('ul', ['if HR drifts > 5% in the second half, it wasn\'t zone 2', 'nose breathing ok',
            'bike counts: 1h bike ≈ 45 min run for the weekly total', 'elliptical on rest-ish days']),
    '',
    '11/19 — 9.1h last week. aerobic decoupling 3.2% on the long run',
], ['project_endurance_training'], notes='training note: zone 2 heart-rate rules')

anote('Training', 'mile repeats', '2026-04-19 09:10', '2026-04-19 10:20', [
    '4 x 1 mile @ threshold, 2 min jog',
    '5:58 / 5:55 / 5:57 / 5:51',
    'felt controlled until the last 400 of #4',
    'HR 172 → 178 by the end',
    '',
    'compared to the miler days this is slow but the recovery between is way better',
], ['project_endurance_training'], notes='workout log')

anote('Training', 'Block 4 — week 3', '2026-08-24 06:40', '2026-08-30 20:15', [
    ('h1', 'Block 4 · wk 3 (8/24–8/30)'),
    '',
    ('ul', ['mon: 50 min easy + strides', 'tue: 2 x 20 min @ HMP-ish (6:30) on the Embarcadero',
            'wed: 70 min bike Z2', 'thu: 45 easy', 'fri: off / elliptical 30', 'sat: long 14 mi, last 3 @ 6:40',
            'sun: 60 easy hills (Twin Peaks, too steep, walk next time)']),
    '',
    'total: 10.4 h. legs heavy thurs. sleep bad all week (new house)',
    'goal for the half 10/15: sub 1:25',
], ['project_endurance_training'], notes='training week in Block 4 (Aug–Oct 2026)')

anote('Training', 'half — splits', '2026-10-15 11:30', '2026-10-15 19:05', [
    ('h1', 'half marathon 10/15'),
    '',
    'chip 1:24:51 (goal sub 1:25 ✓ barely)',
    'Owen 1:22:10',
    '',
    ('b', 'splits'),
    ('ul', ['1: 6:22', '2: 6:20', '3: 6:15', '4: 6:14', '5: 6:16 (too fast 3–5)', '6: 6:24', '7: 6:28', '8: 6:30',
            '9: 6:33', '10: 6:35 (hill)', '11: 6:31', '12: 6:29', '13: 6:24', 'last .1: 0:37']),
    '',
    'gels at 5 and 10. calves gone by 11',
    'next: even pacing. 6:28 flat would have been 1:24:40-ish with way less pain',
], ['project_endurance_training'], notes='race splits for the 2026-10-15 half marathon (1:24:51)')

g.finish()
