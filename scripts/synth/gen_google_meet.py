"""Synthetic Google Meet docs (PERSON.md §1: weekly advisor 1:1s and lab meetings recorded with transcripts + "Notes by Gemini").
Meet saves each transcript and each Gemini notes file as a Google Doc in My Drive > Meet Recordings; stored here as exported .docx.
One item per doc. Content (hand-written) lives in content/google-meet/*.txt:

  header lines `key: value` (title, start, attendees, projects, docs = both|transcript|gemini, length, notes)
  === transcript   -> `Speaker: text` turns, `[pause N]` = N seconds of silence (screen share, doorbell, ...)
  === gemini       -> `summary: ...`, `detail: Topic: text`, `next: [ ] ...`
"""
import os, sys, glob, random, datetime
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('google-meet')
CONTENT = os.path.join(os.path.dirname(__file__), 'content', 'google-meet')
ACCOUNT = 'dbarron410@vt.edu (Google Meet / My Drive > Meet Recordings)'
BASE = 'dbarron410@vt.edu/Meet Recordings'


def parse(path):
    meta, sections, cur = {}, {}, None
    for line in open(path, encoding='utf-8').read().split('\n'):
        if line.startswith('=== '):
            cur = line[4:].strip(); sections[cur] = []; continue
        if cur is None:
            if ':' in line:
                k, v = line.split(':', 1); meta[k.strip()] = v.strip()
        elif line.strip():
            sections[cur].append(line.rstrip())
    return meta, sections


def hms(sec):
    sec = int(round(sec))
    return f'{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}'


def timed_turns(lines, seed):
    """[(seconds, speaker, text)] with times derived from word counts (~2.5 words/s) plus small gaps."""
    rnd = random.Random(seed)
    t = rnd.uniform(2, 9); out = []
    for ln in lines:
        if ln.startswith('[pause'):
            t += int(ln.strip('[]').split()[1]); continue
        spk, txt = ln.split(':', 1)
        txt = txt.strip()
        out.append((t, spk.strip(), txt))
        t += len(txt.split()) / rnd.uniform(2.0, 2.5) + rnd.uniform(0.5, 3.5)
    return out, t + rnd.uniform(3, 12)


def safe(name):  # Drive export replaces characters that aren't allowed in file names
    return name.replace('/', '_')


def offset(d):
    return int(d.utcoffset().total_seconds() // 3600)


total = 0
for path in sorted(glob.glob(os.path.join(CONTENT, '*.txt'))):
    meta, sec = parse(path)
    start = dt(meta['start'])
    stamp = f"{start:%Y-%m-%d %H:%M} GMT{offset(start)}"
    title = meta['title']
    projects = [p.strip() for p in meta['projects'].split(',')]
    attendees = [a.strip() for a in meta['attendees'].split(',')]
    seed = os.path.basename(path)
    rnd = random.Random(seed + 'files')
    if 'transcript' in sec:
        turns, length = timed_turns(sec['transcript'], seed)
    else:
        h, m, s_ = map(int, meta['length'].split(':')); length = h * 3600 + m * 60 + s_
    end = start + datetime.timedelta(seconds=length)
    docs = meta['docs']
    pair_note = f'pair: {title} ({stamp}) transcript + Gemini notes; each doc is its own item' if docs == 'both' else None
    note = meta.get('notes') or pair_note or ''
    long_date = f'{start:%b} {start.day}, {start.year}'

    if docs in ('both', 'transcript'):
        doc_title = f'{title} ({stamp}) - Transcript'
        blocks = [('title', doc_title), ('p', 'Attendees'), ('p', ', '.join(attendees)), ('h2', 'Transcript')]
        blocks += [('p', f'{hms(t)} {spk}: {txt}') for t, spk, txt in turns]
        blocks.append(('p', f'Meeting ended after {hms(length)} 👋'))
        c = end + datetime.timedelta(minutes=rnd.uniform(2, 5))
        mo = c + datetime.timedelta(seconds=rnd.uniform(0, 50))
        g.docx(f'{BASE}/{safe(doc_title)}.docx', blocks, c, mo, title=doc_title, author='Google Meet',
               account=ACCOUNT, project_ids=projects, modeled_on='',
               notes=note or ('transcript only; Gemini notes were not turned on' if docs == 'transcript' else ''))
        total += 1

    if docs in ('both', 'gemini'):
        doc_title = f'{title} ({stamp}) - Notes by Gemini'
        gem = {'summary': [], 'detail': [], 'next': []}
        for ln in sec['gemini']:
            k, v = ln.split(':', 1); gem[k.strip()].append(v.strip())
        blocks = [('title', '📝 Notes'), ('p', long_date), ('h1', title), ('p', 'Invited ' + ' '.join(attendees)),
                  ('p', 'Attachments ' + title)]
        if docs == 'both':
            blocks.append(('p', 'Meeting records Transcript'))
        blocks += [('h2', 'Summary')] + [('p', x) for x in gem['summary']]
        blocks += [('h2', 'Details')] + [('bullet', x) for x in gem['detail']]
        blocks += [('h2', 'Suggested next steps')] + [('bullet', x) for x in gem['next']]
        blocks.append(('p', "You should review Gemini's notes to make sure they're accurate. Get tips and learn how Gemini takes notes"))
        c = end + datetime.timedelta(minutes=rnd.uniform(8, 15))
        mo = c + datetime.timedelta(seconds=rnd.uniform(0, 90))
        g.docx(f'{BASE}/{safe(doc_title)}.docx', blocks, c, mo, title=doc_title, author='Google Meet',
               account=ACCOUNT, project_ids=projects, modeled_on='', notes=note)
        total += 1

g.dir_times(BASE, '2025-10-21 14:30', '2026-07-27 11:40')
g.dir_times('dbarron410@vt.edu', '2025-10-21 14:30', '2026-07-27 11:40')
print('docs written:', total)
g.finish()
