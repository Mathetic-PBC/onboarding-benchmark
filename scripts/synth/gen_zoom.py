"""Synthetic Zoom local recordings (PERSON.md §1: occasional external calls). One item per meeting folder
local-recordings/<YYYY-MM-DD HH.MM.SS Topic>/ holding recording.conf, meeting_saved_chat.txt and a WEBVTT transcript.
No audio/video media is generated (recording.conf names m4a/mp4 files that are absent).

Hand-written meeting content lives in content/zoom/*.txt:
  header lines (topic/start/host/projects/notes/speakers/rate), '=== cues' with 'KEY: text' lines,
  '=== chat' with '@<cue index>+<seconds> FROM>TO: text' lines (FROM/TO = speaker key or full name; TO 'Everyone' or a person = DM).
Cue timings are derived deterministically from word counts."""
import os, re, sys, glob, random, datetime
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

CONTENT = os.path.join(os.path.dirname(__file__), 'content', 'zoom')
MODELED = "authentic/zoom/local-recordings/<meeting folder> layout + recording.conf"
ACCT_HOST = 'local recordings (~/Documents/Zoom), host David Barron'
ACCT_PART = 'local recordings (~/Documents/Zoom), participant David Barron (recording permission granted)'


def parse(path):
    head, cues, chat, sec = {}, [], [], 'head'
    for line in open(path, encoding='utf-8').read().split('\n'):
        if line.startswith('=== '):
            sec = line[4:].strip(); continue
        if not line.strip(): continue
        if sec == 'head':
            k, v = line.split(':', 1); head[k.strip()] = v.strip()
        elif sec == 'cues':
            k, v = line.split(':', 1); cues.append((k.strip(), v.strip()))
        else:
            m = re.match(r'@(\d+)\+(\d+) (.+?)>(.+?): (.*)$', line)
            chat.append((int(m.group(1)), int(m.group(2)), m.group(3).strip(), m.group(4).strip(), m.group(5)))
    head['speakers'] = dict(x.strip().split('=', 1) for x in head['speakers'].split(';'))
    return head, cues, chat


def split_cue(text, maxw=26):
    """Zoom VTT cues are short: break a long turn at sentence ends into chunks of <= ~maxw words."""
    sents = re.split(r'(?<=[.?!])\s+', text)
    out, cur = [], []
    for s in sents:
        if cur and len(' '.join(cur + [s]).split()) > maxw:
            out.append(' '.join(cur)); cur = []
        cur.append(s)
    if cur: out.append(' '.join(cur))
    return out


def ts(sec):
    h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'


def build(g, path):
    head, cues, chat = parse(path)
    spk = head['speakers']
    name = lambda k: spk.get(k, k)
    rnd = random.Random(os.path.basename(path))
    rate = float(head.get('rate', 2.8))
    start = dt(head['start'])
    t = 1.5 + rnd.random() * 2.5
    timed, cue_start = [], {}
    for i, (k, text) in enumerate(cues):
        if i > 0 and cues[i - 1][0] != k and rnd.random() < 0.12: t += rnd.uniform(2.5, 9.0)  # pauses, screen-share fiddling
        cue_start[i] = t
        for chunk in split_cue(text):
            dur = max(1.1, len(chunk.split()) / rate + rnd.uniform(0.1, 0.6))
            timed.append((t, t + dur, name(k), chunk))
            t += dur + rnd.uniform(0.05, 0.5)
        t += rnd.uniform(0.2, 1.3)
    length = t + rnd.uniform(3, 8)
    end = start + datetime.timedelta(seconds=length)

    vtt = ['WEBVTT', '']
    for n, (a, b, who, txt) in enumerate(timed, 1):
        vtt += [str(n), f'{ts(a)} --> {ts(b)}', f'{who}: {txt}', '']
    chat_lines = []
    for idx, delay, frm, to, txt in sorted(chat, key=lambda c: cue_start[c[0]] + c[1]):
        when = start + datetime.timedelta(seconds=cue_start[idx] + delay)
        assert when < end, (path, idx)
        target = 'Everyone' if to == 'Everyone' else f'{name(to)}(Direct Message)'
        chat_lines.append(f'{when.strftime("%H:%M:%S")} From {name(frm)} to {target}:\n\t{txt}\n')

    folder = f'local-recordings/{start.strftime("%Y-%m-%d %H.%M.%S")} {head["topic"]}'
    magic = str(100000000 + int(hexid(folder), 16) % 900000000)
    conf = '{"magic_number":"%s","items":[{"process":100,"audio":"audio1%s.m4a","prefix":"","video":"video1%s.mp4"}]}' % (magic, magic, magic)
    vtt_name = 'GMT' + start.astimezone(UTC).strftime('%Y%m%d-%H%M%S') + '_Recording.transcript.vtt'
    meta = dict(account=ACCT_HOST if head['host'] == 'yes' else ACCT_PART, project_ids=head['projects'].split(','),
                modeled_on=MODELED, notes=head['notes'], label_key=folder)
    g.text(f'{folder}/meeting_saved_chat.txt', ''.join(chat_lines), end + datetime.timedelta(seconds=4), end + datetime.timedelta(seconds=64), **meta)
    g.text(f'{folder}/recording.conf', conf, end + datetime.timedelta(seconds=22), end + datetime.timedelta(seconds=82), **meta)
    g.text(f'{folder}/{vtt_name}', '\n'.join(vtt), end + datetime.timedelta(seconds=95), end + datetime.timedelta(seconds=155), **meta)
    g.dir_times(folder, start, end + datetime.timedelta(seconds=155))
    print(f'  {folder}: {len(cues)} turns -> {len(timed)} cues, {len(chat_lines)} chat msgs, {length/60:.1f} min')


def main():
    g = Gen('zoom')
    for p in sorted(glob.glob(os.path.join(CONTENT, '*.txt'))):
        build(g, p)
    g.dir_times('local-recordings', '2025-11-19 16:00', '2026-10-02 11:00')
    g.finish()


if __name__ == '__main__':
    main()
