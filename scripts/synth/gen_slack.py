"""Synthetic Slack (Phase 2): two invented workspaces in the same layout as authentic/slack/Mathetic.

  synthetic/slack/<workspace>/<name>__<channel id>/messages.json   top-level messages, oldest first (connector parse shape:
                                                                    ts, user, user_name, datetime, text; thread/reaction/file
                                                                    lines appended to text like the real parse)
  synthetic/slack/<workspace>/<name>__<channel id>/history.txt     raw connector pages, newest first
  synthetic/slack/<workspace>/<name>__<channel id>/threads/<ts>.txt one file per thread
  synthetic/slack/<workspace>/files/<file id>__<name>               shared files
  synthetic/slack/<workspace>/users/<user id>.txt                   user profiles
  synthetic/slack/<workspace>/conversations.md                      conversation list

Workspaces: "PRIME Lab (VT)" (Oct 2025 – Aug 2026, fading after the leave) and "Surplus Residents" (Aug – Oct 2026).
Messages are hand-written in _scripts/synth/content/slack/<ws>/<conversation>.txt:
  @YYYY-MM-DD                      set the current day (local time where David was: ET until 2026-08-08, then PT)
  HH:MM handle | text              top-level message   (text "<join>" = "has joined the channel")
  > [YYYY-MM-DD ]HH:MM handle | t  thread reply to the last top-level message
  <two spaces>text                 continuation line of the last message/reply ("\\" alone = empty line)
  ~r name:n name:n                 reactions on the last top-level message
  ~f key                           file shared with the last top-level message (FILES below)
  ~p project ...                   projects of that message's thread file (default: the conversation's)
  ~n note                          label note for that thread file
  <@handle>                        mention -> <@UID|Real Name>
Every file is its own item for the itemizer, so both files of a conversation get the same projects; each thread file gets
the projects of its own thread.
"""
import os, sys, re, random, hashlib, datetime
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

CONTENT = os.path.join(os.path.dirname(__file__), 'content', 'slack')
g = Gen('slack')
ALPH = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
MOD_MSG = 'authentic/slack/Mathetic/<channel>/messages.json shape (connector parse)'
MOD_HIST = 'authentic/slack/Mathetic/<channel>/history.txt shape (raw connector pages)'
MOD_THREAD = 'authentic/slack/Mathetic/<channel>/threads/<ts>.txt shape'


def sid(prefix, seed, n=6):
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16); s = ''
    for _ in range(n): s += ALPH[h % len(ALPH)]; h //= len(ALPH)
    return prefix + s


def human_size(n):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if n < 1024 or unit == 'GB':
            return f'{n} B' if unit == 'B' else f'{n:.1f} {unit}'
        n /= 1024


def D(t):
    return datetime.datetime.fromtimestamp(float(t), UTC)


def show(ts):
    return datetime.datetime.fromtimestamp(float(ts), PT).strftime('%Y-%m-%d %H:%M:%S %Z')

# ---------------- workspaces ----------------

WS = {
    'prime': dict(
        folder='PRIME Lab (VT)', team='PRIME Lab (VT)',
        account='PRIME Lab (VT) Slack workspace (David Barron, dbarron410@vt.edu)',
        users={  # handle: (real name, user_name as rendered, username, title, tz, email)
            'david': ('David Barron', 'David Barron <dbarron410@vt.edu>', 'dbarron', 'PhD student', 'America/Los_Angeles', 'dbarron410@vt.edu'),
            'yan': ('Yan Chen', 'Yan Chen', 'yanchen', 'Assistant Professor, CS', 'America/New_York', ''),
            'minsun': ('Minsun', 'Minsun', 'minsun', 'PhD student', 'America/New_York', ''),
            'xiaohang': ('Xiaohang', 'Xiaohang', 'xiaohang', 'PhD student', 'America/New_York', ''),
            'rezky': ('Rezky', 'Rezky', 'rezky', 'PhD student', 'America/New_York', ''),
            'yue': ('Yue', 'Yue', 'yue', 'PhD student', 'America/New_York', ''),
        },
        # (file stem, kind, display name, projects of the conversation, dm user, note)
        convs=[
            ('general', 'channel', 'general', ['project_vizpi', 'project_tutortrace', 'project_idetrace', 'project_mathetic_company', 'project_vt_phd_admin'], None,
             'lab-wide channel: deployment, deadlines, lab logistics, the leave announcement'),
            ('vizpi', 'channel', 'vizpi', ['project_vizpi'], None, 'VizPI CS 3114 deployments, reconnect bug, Cursor trial, handoff'),
            ('labeling', 'channel', 'labeling', ['project_vizpi', 'project_tutortrace'], None, 'Nov 2025 labeling sprint (guide v3, kappa)'),
            ('uist26', 'channel', 'uist26', ['project_tutortrace'], None, 'TutorTrace UIST 2026: crunch, rebuttal, camera-ready'),
            ('idetrace', 'channel', 'idetrace', ['project_idetrace'], None, 'IDETrace NeurIPS D&B: submission, leakage bug, rebuttal'),
            ('random', 'channel', 'random', ['project_none'], None, 'off-topic lab chatter (cake, chess, snow, a 5k, a beat)'),
            ('paper-reading', 'channel', 'paper-reading', ['project_vizpi', 'project_tutortrace', 'project_idetrace', 'project_augmenting_cognition_reading_group'], None,
             'HARD CASE: same paper in several places — #paper-reading holds the Ostrowski et al. 2025 PDF share (file in files/) and its discussion'),
            ('dm_yan', 'dm', 'Yan Chen', ['project_tutortrace', 'project_idetrace', 'project_vizpi', 'project_vt_phd_admin', 'project_cs3604_gta'], 'yan',
             'advisor DMs: scheduling, UIST pitch, rebuttal, leave of absence, travel funding, talk'),
            ('dm_minsun', 'dm', 'Minsun', ['project_vizpi', 'project_tutortrace'], 'minsun', ''),
            ('dm_xiaohang', 'dm', 'Xiaohang', ['project_idetrace'], 'xiaohang', 'IDETrace student-id join and grouped splits'),
            ('dm_rezky', 'dm', 'Rezky', ['project_vizpi', 'project_tutortrace'], 'rezky', ''),
            ('dm_yue', 'dm', 'Yue', ['project_tutortrace', 'project_idetrace'], 'yue', ''),
        ]),
    'surplus': dict(
        folder='Surplus Residents', team='Surplus Residents',
        account='Surplus Residents Slack workspace (David Barron, david@mathetic.com)',
        users={
            'david': ('David Barron', 'David Barron <david@mathetic.com>', 'david', 'Co-founder, Mathetic', 'America/Los_Angeles', 'david@mathetic.com'),
            'hudson': ('Hudson Mitchell-Pullman', 'Hudson Mitchell-Pullman', 'hudson', 'Co-founder, Mathetic', 'America/Los_Angeles', ''),
            'lena': ('Lena Hoffmann', 'Lena Hoffmann', 'lena', 'Program Lead, Surplus', 'America/Los_Angeles', ''),
            'sam': ('Sam Whitaker', 'Sam Whitaker', 'sam', '', 'America/Los_Angeles', ''),
        },
        convs=[
            ('announcements', 'channel', 'announcements', ['project_mathetic_company'], None, 'incubator program announcements (Lena)'),
            ('demo-day', 'channel', 'demo-day', ['project_mathetic_company', 'project_engelbart'], None, 'pitch practice and feedback for demo day'),
            ('housing', 'channel', 'housing', ['project_none'], None, 'house logistics: groceries, chores, bike shop, dishwasher'),
            ('dm_lena', 'dm', 'Lena Hoffmann', ['project_mathetic_company'], 'lena', 'program lead DMs: desk, residency agreement, check-in, intro to Daniel Osei'),
        ]),
}
for key, ws in WS.items():
    ws['uid'] = {h: sid('U0SYN', f'{key}/user/{h}') for h in ws['users']}

# ---------------- shared files (written first so sizes are real) ----------------

GUIDE_V3 = [
    ('title', 'VizPI Labeling Guide v3'),
    ('p', 'PRIME Lab, Virginia Tech. Version 3, 2025-11-17 (v2: 2025-11-10). For labeling 30-second windows of VizPI replays '
          'from CS 3114 deployment #2 (2025-11-12).'),
    ('h2', 'What a window is'),
    ('p', 'Each window is 30 seconds of one student\'s session. Windows start at a run event when one falls within 5 seconds of the '
          'nominal boundary, otherwise on the 30-second grid. Watch the replay at 1x for the window plus 30 seconds of context before it.'),
    ('h2', 'States (pick exactly one)'),
    ('table', [['State', 'Definition', 'Typical evidence'],
               ['productive', 'Making progress toward the spec', 'edits that change test results, new passing tests'],
               ['stuck', 'Active but unproductive', 'edits/runs that do not change the error message'],
               ['stalled-after-error (new in v3)', 'Error or failed test in the last 60 s AND no edit or run for >= 45 s of the window AND no help request', 'scrolling, idle cursor, re-reading the error'],
               ['help_seeking', 'Asking the TA queue or the assistant', 'help button, assistant prompt, raised-hand flag'],
               ['off_task', 'Not working on the assignment', 'other tabs, no IDE focus for > 20 s']]),
    ('h2', 'Decision rules'),
    ('bullet', 'If a help request happens anywhere in the window, label help_seeking, even if the student was stalled before it.'),
    ('bullet', 'stalled-after-error needs all three conditions. If the student edits once in the last 10 s, it is stuck, not stalled.'),
    ('bullet', 'Windows flagged partial_telemetry (section B, 3:30-4:10 pm) are labeled normally; add the comment #partial if a gap is visible.'),
    ('bullet', 'Unsure between two states: pick the earlier one in the table and add #unsure.'),
    ('h2', 'Calibration (2025-11-14)'),
    ('p', 'Before batch A the three raters labeled 40 windows together (8 per state, both sections), discussed every disagreement and '
          'wrote down the edge cases above. Batches of 780 windows follow, with 15% pairwise overlap for agreement.'),
    ('h2', 'Changes from v2'),
    ('bullet', 'Added stalled-after-error. v2 put these windows under stuck or, sometimes, off_task.'),
    ('bullet', 'Clarified the window start rule (align to run events).'),
    ('bullet', 'Keyboard shortcuts: 1 productive, 2 stuck, 3 help_seeking, 4 stalled-after-error, 5 off_task (labeler v0.3.1).'),
]

DEP2_LOSS = """bucket_start_et,section,students,events_received,events_expected_est,events_lost_est,lost_pct,notes
15:30,A,43,21612,21930,318,1.5,normal jitter
15:40,A,43,21890,21930,40,0.2,
15:50,A,43,21951,21930,0,0.0,
16:00,A,43,21874,21930,56,0.3,
16:10,A,43,21960,21930,0,0.0,
16:20,A,43,21702,21930,228,1.0,
16:30,A,43,21405,21930,525,2.4,students finishing early
16:40,A,43,10522,10965,443,4.0,5-minute bucket
15:30,B,44,18180,22000,3820,17.4,reconnect bug (idle sockets dropped after ~60s)
15:40,B,44,16760,22000,5240,23.8,reconnect bug
15:50,B,44,16390,22000,5610,25.5,reconnect bug; flagged on dashboard 15:47
16:00,B,44,17258,22000,4742,21.6,hotfix a91d0f3 deployed 16:10
16:10,B,44,21930,22000,70,0.3,after hotfix
16:20,B,44,21985,22000,15,0.1,
16:30,B,44,21810,22000,190,0.9,
16:40,B,44,10875,11000,125,1.1,5-minute bucket
TOTAL,B,44,145188,165000,19812,12.0,includes post-fix jitter; bug-attributable loss 19412 (11.8%)
"""

F1_COMPARE = """model,split_v1_random_window,split_v2_grouped_student,delta
majority,0.17,0.17,0.00
logistic_regression,0.66,0.64,-0.02
lightgbm_gbdt,0.81,0.74,-0.07
transformer_events,0.79,0.70,-0.09
gbdt_per_state:productive,0.86,0.80,-0.06
gbdt_per_state:stuck,0.77,0.69,-0.08
gbdt_per_state:stalled_after_error,0.84,0.75,-0.09
gbdt_per_state:help_seeking,0.83,0.78,-0.05
gbdt_per_state:off_task,0.75,0.68,-0.07
"""

HANDBOOK = [
    ('title', 'Surplus Resident Handbook: Cohort 7'),
    ('p', 'August 11 - November 19, 2026. Questions: Lena Hoffmann, program lead (#announcements or DM).'),
    ('h2', 'Program at a glance'),
    ('table', [['When', 'What'], ['Aug 11', 'Kickoff, house tour, intros'], ['Tuesdays 7pm', 'Resident dinner + speaker'],
               ['Thursdays 2-5pm', 'Office hours with Lena (sign-up sheet)'], ['Sept 14-18', 'Mid-program check-ins (30 min)'],
               ['Sept 29', 'Investor speed-dating'], ['Wednesdays 4pm from Oct 7', 'Pitch practice'], ['Nov 17', 'Dress rehearsal'],
               ['Nov 19', 'Demo day']]),
    ('pagebreak', None),
    ('h2', 'The house'),
    ('bullet', 'Quiet hours 10pm-7am. Dishwasher and laundry before 10pm.'),
    ('bullet', 'Shared pantry shelf: anything unlabeled is fair game.'),
    ('bullet', 'Bikes in the garage; the door code is posted on the fridge, never in Slack.'),
    ('bullet', 'Chore wheel rotates monthly and lives on the fridge.'),
    ('pagebreak', None),
    ('h2', 'Coworking side'),
    ('p', 'Badges at the front desk. Desks are assigned per team at kickoff. Whiteboards are wiped every Sunday night, so photograph '
          'anything you need.'),
    ('pagebreak', None),
    ('h2', 'Phone booth and meeting room'),
    ('p', 'The phone booth is bookable through the house calendar (link pinned in #announcements), 45 minutes maximum per booking. '
          'The meeting room seats 6 and is first come, first served outside office hours.'),
    ('h2', 'Agreements'),
    ('p', 'Each company signs the residency agreement once, by one officer, in the legal name on its certificate of incorporation. '
          'The August addendum removes the shared-IP clause; every team must sign it by Aug 31.'),
]

FILES = {}  # key -> dict(ws, id, name, mime, rel, size)


def add_file(ws_key, key, name, mime, when, writer, projects, notes, modeled_on=''):
    ws = WS[ws_key]
    fid = sid('F0SYN', f'{ws_key}/file/{key}')
    rel = f"{ws['folder']}/files/{fid}__{name}"
    path = writer(rel, when)
    FILES[key] = dict(ws=ws_key, id=fid, name=name, mime=mime, rel=rel, size=os.path.getsize(path), when=when, projects=projects)
    return path


def file_meta(ws_key, projects, notes, modeled_on=''):
    return dict(account=WS[ws_key]['account'], project_ids=projects, notes=notes, modeled_on=modeled_on)

# share times (must match the content files)
add_file('prime', 'ostrowski', 'Ostrowski2025_arXiv_v1.pdf', 'application/pdf', '2025-11-19 21:05:31',
         lambda rel, w: g.copy_from(rel, os.path.join(SHARED, 'Ostrowski2025_arXiv_v1.pdf'), w, w,
                                    **file_meta('prime', ['project_tutortrace', 'project_vizpi'],
                                                "HARD CASE: same paper in several places — Ostrowski et al. 2025 arXiv v1 PDF shared by Minsun in #paper-reading "
                                                "(same bytes as the copies in zotero/pdfs/gmail; camera-ready v2 elsewhere is a near-duplicate)",
                                                'authentic/slack/Mathetic/files/<id>__<name>.pdf (Slack file share)')),
         ['project_tutortrace', 'project_vizpi'], '')
add_file('prime', 'guide_v3', 'VizPI_labeling_guide_v3.pdf', 'application/pdf', '2025-11-17 11:15:22',
         lambda rel, w: g.pdf(rel, GUIDE_V3, '2025-11-17 10:58', w, title='VizPI Labeling Guide v3', author='David Barron',
                              **file_meta('prime', ['project_vizpi'], "Slack file 'VizPI_labeling_guide_v3' shared in #labeling (adds stalled-after-error)",
                                          'authentic/slack/Mathetic/files/<id>__<name>.pdf (Slack file share)')),
         ['project_vizpi'], '')
add_file('prime', 'dep2_loss', 'dep2_section_event_loss.csv', 'text/csv', '2025-11-13 10:40:09',
         lambda rel, w: g.text(rel, DEP2_LOSS, '2025-11-13 10:31', w,
                               **file_meta('prime', ['project_vizpi'], "Slack file 'dep2_section_event_loss.csv': per-bucket telemetry loss, deployment #2")),
         ['project_vizpi'], '')
add_file('prime', 'f1_compare', 'idetrace_f1_random_vs_grouped.csv', 'text/csv', '2026-07-25 18:30:44',
         lambda rel, w: g.text(rel, F1_COMPARE, '2026-07-25 18:12', w,
                               **file_meta('prime', ['project_idetrace'], "Slack file: IDETrace baselines, random-window vs student-grouped split (leakage fix)")),
         ['project_idetrace'], '')
add_file('surplus', 'handbook', 'Surplus_Resident_Handbook_Cohort7.pdf', 'application/pdf', '2026-08-11 12:40:18',
         lambda rel, w: g.pdf(rel, HANDBOOK, '2026-08-07 15:00', w, title='Surplus Resident Handbook: Cohort 7', author='Lena Hoffmann',
                              **file_meta('surplus', ['project_mathetic_company'], "Slack file: Surplus resident handbook pinned in #announcements",
                                          'authentic/slack/Mathetic/files/<id>__<name>.pdf (Slack file share)')),
         ['project_mathetic_company'], '')

# ---------------- parsing ----------------
MSG = re.compile(r'^(\d{1,2}):(\d\d) (\w+) \| ?(.*)$')
REP = re.compile(r'^> (?:(\d{4}-\d\d-\d\d) )?(\d{1,2}):(\d\d) (\w+) \| ?(.*)$')


def parse(path):
    msgs = []; day = None; last = None
    for raw in open(path, encoding='utf-8').read().split('\n'):
        line = raw.rstrip('\n')
        if not line.strip() or line.startswith('# '): continue
        if line.startswith('@'): day = line[1:].strip(); continue
        if line.startswith('  '):
            t = line[2:]
            last['text'] += '\n' + ('' if t == '\\' else t); continue
        if line.startswith('~'):
            cmd, _, arg = line[1:].partition(' ')
            top = msgs[-1]
            if cmd == 'r': top['reactions'] = [(a.split(':')[0], int(a.split(':')[1]) if ':' in a else 1) for a in arg.split()]
            elif cmd == 'f': top['files'].append(arg.strip())
            elif cmd == 'p': top['projects'] = arg.split()
            elif cmd == 'n': top['note'] = arg.strip()
            else: raise ValueError(line)
            continue
        m = REP.match(line)
        if m:
            d, hh, mm, who, text = m.groups()
            last = dict(day=d or day, hh=int(hh), mm=int(mm), who=who, text=text)
            msgs[-1]['replies'].append(last); continue
        m = MSG.match(line)
        if m:
            hh, mm, who, text = m.groups()
            last = dict(day=day, hh=int(hh), mm=int(mm), who=who, text=text, replies=[], reactions=[], files=[], projects=None, note=None)
            msgs.append(last); continue
        raise ValueError(f'{path}: cannot parse {line!r}')
    return msgs

# ---------------- render ----------------
total_msgs = 0
for ws_key, ws in WS.items():
    users, uids = ws['users'], ws['uid']
    conv_index = []
    first_seen, last_seen = {}, {}

    def fix(text):
        return re.sub(r'<@(\w+)>', lambda m: f'<@{uids[m.group(1)]}|{users[m.group(1)][0]}>', text)

    for stem, kind, name, projects, dm_user, conv_note in ws['convs']:
        cid = sid('D0SYN' if kind == 'dm' else 'C0SYN', f'{ws_key}/conv/{stem}')
        folder = f"{ws['folder']}/{'DM_with_' + name.replace(' ', '_') if kind == 'dm' else name}__{cid}"
        conv_index.append((kind, name, cid, dm_user))
        msgs = parse(os.path.join(CONTENT, ws_key, stem + '.txt'))
        rnd = random.Random(f'{ws_key}/{stem}')
        prev = 0.0

        def make_ts(day, hh, mm, floor):
            sec = rnd.randrange(60)
            t = epoch(f'{day} {hh:02d}:{mm:02d}:{sec:02d}')
            if t <= floor: t = floor + rnd.randint(2, 9)
            return t, f'{int(t)}.{rnd.randrange(1000000):06d}'

        for m in msgs:
            m['t'], m['ts'] = make_ts(m['day'], m['hh'], m['mm'], prev); prev = m['t']
            rprev = m['t']
            for r in m['replies']:
                r['t'], r['ts'] = make_ts(r['day'], r['hh'], r['mm'], rprev); rprev = r['t']
            for k in m['files']:
                f = FILES[k]
                assert abs(epoch(f['when']) - m['t']) < 120, (k, f['when'], show(m['ts']))
                g.times(os.path.join(g.dir, f['rel']), D(m['t']), D(m['t']))  # file uploaded with the message
                g.rows[f['rel']]['date'] = iso(D(m['t']))
        for m in msgs:
            if m['text'] == '<join>':
                u = m['who']; m['text'] = f'<@{uids[u]}|{users[u][0]}> has joined the channel'
            m['text'] = fix(m['text'])
            for r in m['replies']: r['text'] = fix(r['text'])
            for u in [m['who']] + [r['who'] for r in m['replies']]:
                first_seen.setdefault(u, m['t'])

        def full_text(m):
            parts = [m['text']]
            if m['replies']:
                parts.append(f"Thread: {len(m['replies'])} replies (latest: {show(m['replies'][-1]['ts'])})")
            if m['reactions']:
                parts.append('Reactions: ' + ', '.join(f'{n} ({c})' for n, c in m['reactions']))
            if m['files']:
                parts.append('Files: ' + ', '.join(f"{FILES[k]['name']} (ID: {FILES[k]['id']}, {FILES[k]['mime']}, {human_size(FILES[k]['size'])})" for k in m['files']))
            return '\n'.join(parts)

        def uname(u): return users[u][1]

        out = [dict(ts=m['ts'], user=uids[m['who']], user_name=uname(m['who']), datetime=show(m['ts']), text=full_text(m)) for m in msgs]
        first_t = msgs[0]['t']
        last_t = max([m['t'] for m in msgs] + [r['t'] for m in msgs for r in m['replies']])
        n = len(msgs); total_msgs += n + sum(len(m['replies']) for m in msgs)
        label = f'#{name}' if kind == 'channel' else f'DM with {name}'
        header = f'Channel: #{name} ({cid})' if kind == 'channel' else f'Channel: DM ({cid})'
        blocks = [f"=== Message from {uname(m['who'])} ({uids[m['who']]}) at {show(m['ts'])} === \nMessage TS: {m['ts']}\n{full_text(m)}"
                  for m in reversed(msgs)]
        hard = conv_note.startswith('HARD CASE')
        note_tail = f' — {conv_note}' if conv_note and not hard else ''
        pre = (lambda t: f'{conv_note}; {t}') if hard else (lambda t: t)
        g.json(f'{folder}/messages.json', out, D(first_t), D(last_t), indent=2, account=ws['account'], project_ids=projects,
               modeled_on=MOD_MSG, notes=pre(f'{label}: {n} messages parsed from history.txt, oldest first{note_tail}'))
        g.text(f'{folder}/history.txt', header + '\n\n' + '\n\n'.join(blocks), D(first_t), D(last_t), account=ws['account'], project_ids=projects,
               modeled_on=MOD_HIST, notes=pre(f'{label}: {n} messages, raw connector pages (newest first){note_tail}'))
        for m in msgs:
            if not m['replies']: continue
            body = (f"=== THREAD PARENT MESSAGE ===\nFrom: {uname(m['who'])} ({uids[m['who']]})\nTime: {show(m['ts'])}\nMessage TS: {m['ts']}\n{m['text']}\n\n"
                    f"=== THREAD REPLIES ({len(m['replies'])} total) ===\n")
            for i, r in enumerate(m['replies'], 1):
                body += (f"\n--- Reply {i} of {len(m['replies'])} ---\nFrom: {uname(r['who'])} ({uids[r['who']]})\nTime: {show(r['ts'])}\n"
                         f"Message TS: {r['ts']}\n{r['text']}\n")
            tp = m['projects'] or projects
            tnote = f'{label}: thread under message {m["ts"]}'
            if m['note']: tnote = f"{m['note']}; {tnote}" if m['note'].startswith('HARD CASE') else f"{tnote}; {m['note']}"
            g.text(f"{folder}/threads/{m['ts']}.txt", body, D(m['t']), D(m['replies'][-1]['t']), account=ws['account'], project_ids=tp,
                   modeled_on=MOD_THREAD, notes=tnote, label_notes=m['note'] if m['note'] else None)
        for u in uids:
            if any(x['who'] == u for x in msgs) or any(r['who'] == u for x in msgs for r in x['replies']):
                last_seen[u] = max(last_seen.get(u, 0), last_t)

    # conversations.md (same layout as the real connector list)
    lines = [f'## My Channels (showing {len(conv_index)} of {len(conv_index)} total)', '']
    for kind, name, cid, dm_user in conv_index:
        if kind == 'channel':
            lines += [f'### #{name}', f'- **ID:** {cid}', '- **Type:** Public Channel', '- **Archived:** No', '']
        else:
            lines += [f'### DM with {name}', f'- **ID:** {cid}', '- **Type:** Direct Message', f'- **User ID:** {uids[dm_user]}', '- **Archived:** No', '']
    t_end = max(last_seen.values())
    g.text(f"{ws['folder']}/conversations.md", '\n'.join(lines), D(min(first_seen.values())), D(t_end), account=ws['account'], project_ids=['project_none'],
           modeled_on='authentic/slack/Mathetic/conversations.md shape', notes=f'conversation list from the connector ({len(conv_index)} conversations); index only')
    for h, (real, shown, username, title, tz, email) in users.items():
        body = (f'User ID: {uids[h]}\nUsername: {username}\nDisplay Name: \nReal Name: {real}\nPronouns: \nTitle: {title}\nEmail: {email}\n'
                f'Organization Name: {ws["team"]}\nPhone: \nStatus:  \nTimezone: {tz}\nAdmin: {"Yes" if h in ("yan", "lena") else "No"}\n'
                f'Owner: {"Yes" if h in ("yan", "lena") else "No"}\nBot: No\nRestricted: No')
        g.text(f"{ws['folder']}/users/{uids[h]}.txt", body, D(first_seen.get(h, t_end)), D(last_seen.get(h, t_end)), account=ws['account'],
               project_ids=['project_none'], modeled_on='authentic/slack/Mathetic/users/<id>.txt shape', notes=f'user profile: {real} (directory metadata)')

print('slack messages incl. replies:', total_msgs)
g.finish()
