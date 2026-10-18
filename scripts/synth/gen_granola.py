"""Synthetic Granola: David's own Granola notes (Aug-Oct 2026, San Francisco / PT), one JSON document per meeting in the shape
Granola's API / MCP returns a document (title, calendar event, people, AI-enhanced notes_markdown + notes_plain, transcript).

Content (hand-written notes + transcripts) lives in _scripts/synth/content/granola/m*.txt; this script only wraps it into the
native shape and computes deterministic transcript timestamps from word counts."""
import os, re, sys, glob, random, datetime
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

CONTENT = os.path.join(os.path.dirname(__file__), 'content', 'granola')
ACCOUNT = 'Granola (david@mathetic.com, Mathetic workspace)'
MODELED = 'Granola document JSON (API/MCP document shape); vocabulary from authentic/granola/shared-notes share pages'
ME_NAME, ME_EMAIL = 'David Barron', 'david@mathetic.com'
WORKSPACE = uid('granola-workspace-mathetic')
USER_ID = uid('granola-user-david')


def parse(path):
    out = []
    for block in open(path, encoding='utf-8').read().split('##### MEETING')[1:]:
        head, rest = block.split('=== notes', 1)
        notes, transcript = rest.split('=== transcript', 1)
        h = {}
        for line in head.strip().splitlines():
            k, _, v = line.partition(':')
            h[k.strip()] = v.strip()
        turns = []
        for line in transcript.strip().splitlines():
            line = line.strip()
            if not line: continue
            if line.startswith('~~'):  # silence (nobody talking, e.g. while an import runs): ~~ <seconds>
                turns.append(('~~', line[2:].strip()))
                continue
            spk, _, txt = line.partition(': ')
            turns.append((spk.strip(), txt.strip()))
        h['notes_md'] = notes.strip() + '\n'
        h['turns'] = turns
        out.append(h)
    return out


def attendees(s):
    res = []
    for a in [x.strip() for x in s.split(';') if x.strip()]:
        m = re.match(r'(.+?)\s*<(.+)>', a)
        res.append((m.group(1), m.group(2)) if m else (a, None))
    return res


def plain(md):
    lines = []
    for l in md.splitlines():
        l = re.sub(r'^#+\s*', '', l)
        l = l.replace('**', '')
        l = re.sub(r'^(\s*)- \[ \] ', r'\1', l)
        l = re.sub(r'^(\s*)- ', r'\1', l)
        lines.append(l)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip() + '\n'


def zt(d):
    return dt(d).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S.') + f'{dt(d).astimezone(UTC).microsecond // 1000:03d}Z'


def build_transcript(m, start, doc_id, people):
    rnd = random.Random('granola-ts-' + m['slug'])
    t = start + datetime.timedelta(seconds=rnd.uniform(4, 35))
    in_person = m.get('mode') == 'in-person'
    out = []
    prev_text = ''
    for i, (spk, txt) in enumerate(m['turns']):
        if spk == '~~':
            t += datetime.timedelta(seconds=float(txt) * rnd.uniform(0.95, 1.05))
            continue
        override = re.match(r'\{\+(\d+)\}\s*', txt)
        if override:
            txt = txt[override.end():]
        words = len(txt.split())
        dur = float(override.group(1)) if override else max(0.9, words / 2.45) * rnd.uniform(0.92, 1.15)
        if prev_text.endswith('—'):
            t -= datetime.timedelta(seconds=rnd.uniform(0.2, 0.7))  # interruption: next speaker cuts in
        is_me = spk == 'Me'
        speaker = 'Me' if is_me else people.get(spk, spk)
        end = t + datetime.timedelta(seconds=dur)
        out.append({
            'id': uid(f'{doc_id}-utt-{i}'),
            'document_id': doc_id,
            'start_timestamp': zt(t),
            'end_timestamp': zt(end),
            'text': txt,
            'source': 'microphone' if (is_me or in_person) else 'system',
            'speaker': speaker,
            'is_final': True,
        })
        prev_text = txt
        t = end + datetime.timedelta(seconds=rnd.uniform(0.15, 2.2))
    return out, end


def main():
    g = Gen('granola')
    meetings = []
    for f in sorted(glob.glob(os.path.join(CONTENT, 'm*.txt'))):
        meetings += parse(f)
    meetings.sort(key=lambda m: dt(m['start']))
    seen = set()
    for m in meetings:
        start = dt(m['start'])
        doc_id = uid('granola-doc-' + m['slug'])
        att = attendees(m.get('attendees', ''))
        people = {}
        for name, _ in att:
            display = re.sub(r'\s*\(.*\)$', '', name)
            people[display.split(' ')[0]] = display
        transcript, t_end = build_transcript(m, start, doc_id, people)
        rnd = random.Random('granola-doc-' + m['slug'])
        has_cal = m.get('calendar') == 'yes'
        created = start - datetime.timedelta(seconds=rnd.randint(40, 170)) if has_cal else dt(transcript[0]['start_timestamp']) - datetime.timedelta(seconds=6)
        updated = t_end + datetime.timedelta(seconds=rnd.randint(70, 330))
        assert updated <= REF, m['slug']
        sched_end = start + datetime.timedelta(minutes=int(m.get('scheduled_min') or 0))
        tzname = 'America/Los_Angeles' if tz_for(start) == PT else 'America/New_York'
        organizer = m.get('organizer') or ME_EMAIL
        cal = None
        if has_cal:
            cal_att = [{'email': ME_EMAIL, 'displayName': ME_NAME, 'responseStatus': 'accepted', 'self': True,
                        **({'organizer': True} if organizer == ME_EMAIL else {})}]
            for name, email in att:
                if email:
                    cal_att.append({'email': email, 'displayName': name, 'responseStatus': 'accepted',
                                    **({'organizer': True} if organizer == email else {})})
            cal = {
                'id': hexid('gcal-' + m['slug'], 26),
                'summary': m['title'],
                'start': {'dateTime': start.isoformat(), 'timeZone': tzname},
                'end': {'dateTime': sched_end.isoformat(), 'timeZone': tzname},
                'attendees': cal_att,
                'organizer': {'email': organizer},
                'creator': {'email': organizer},
                'htmlLink': 'https://www.google.com/calendar/event?eid=' + hexid('eid-' + m['slug'], 40),
                'status': 'confirmed',
            }
            if m.get('mode') == 'virtual':
                code = hexid('meet-' + m['slug'], 10)
                letters = ''.join('abcdefghijklmnopqrstuvwxyz'[int(c, 16) + (i % 10)] for i, c in enumerate(code))
                cal['hangoutLink'] = f'https://meet.google.com/{letters[:3]}-{letters[3:7]}-{letters[7:10]}'
            else:
                cal['location'] = 'Surplus house, SF' if 'berkeley' not in m['slug'] else 'UC Berkeley'
        doc = {
            'id': doc_id,
            'workspace_id': WORKSPACE,
            'user_id': USER_ID,
            'type': 'meeting',
            'title': m['title'],
            'created_at': zt(created),
            'updated_at': zt(updated),
            'deleted_at': None,
            'creation_source': 'macOS',
            'valid_meeting': True,
            'transcribe': True,
            'public': False,
            'sharing_link_visibility': 'workspace' if 'hudson@mathetic.com' in m.get('attendees', '') else 'private',
            'google_calendar_event': cal,
            'people': {
                'creator': {'name': ME_NAME, 'email': ME_EMAIL},
                'attendees': [{'name': re.sub(r'\s*\(.*\)$', '', n), **({'email': e} if e else {})} for n, e in att],
            },
            'notes_markdown': m['notes_md'],
            'notes_plain': plain(m['notes_md']),
            'transcript': transcript,
        }
        day = start.strftime('%Y-%m-%d')
        fname = f"{day} {m['title']}".replace('/', '_').replace(':', ' -')
        rel = f'david.barron (Granola)/{fname}.json'
        assert rel not in seen, rel
        seen.add(rel)
        g.json(rel, doc, created, updated, account=ACCOUNT, project_ids=[p.strip() for p in m['projects'].split(';')],
               modeled_on=MODELED, notes=m.get('label_notes', ''))
    g.dir_times('david.barron (Granola)', dt('2026-08-11 09:58'), max(dt(r['date']) for r in g.rows.values()))
    g.finish()


if __name__ == '__main__':
    main()
