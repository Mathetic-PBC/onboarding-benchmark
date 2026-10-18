"""Synthetic Gmail: three accounts, one item per thread, real layout: <account>/threads/thread-f_<decimal thread id>/<16-hex msg id>.eml
(threads holding only David's own sent messages: thread-a_r-<decimal>).
Hand-written content lives in _scripts/synth/content/gmail/{runs,personal,vt}.py (THREADS lists built with _dsl.py).
The helpers here (attachments, quoting, header building, writing) are shared with gen_outlook.py."""
import os, sys, io, re, base64, datetime, hashlib, importlib.util, html as _html
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
SCOPE_LO = dt('2025-10-17 00:00')


def load_threads(sub, name):
    sys.path.insert(0, os.path.join(CONTENT, 'gmail'))  # _dsl
    spec = importlib.util.spec_from_file_location(f'mail_{sub}_{name}', os.path.join(CONTENT, sub, name + '.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.THREADS

# ---------------- attachments ----------------

MIME = {'pdf': 'application/pdf', 'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'ics': 'text/calendar',
        'png': 'image/png', 'csv': 'text/csv', 'txt': 'text/plain'}


def png_chart(spec):
    from PIL import Image, ImageDraw, ImageFont
    W, H = 640, 360
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    try: font = ImageFont.load_default(size=14)
    except TypeError: font = ImageFont.load_default()
    d.text((20, 12), spec.get('title', ''), fill='black', font=font)
    labels, vals = spec['labels'], spec['values']
    top = max(vals) * 1.15 or 1
    x0, y0, x1, y1 = 60, 50, W - 20, H - 50
    d.line((x0, y0, x0, y1), fill='#444'); d.line((x0, y1, x1, y1), fill='#444')
    if spec.get('ylabel'): d.text((8, y0 - 18), spec['ylabel'], fill='#444', font=font)
    n = len(vals); bw = (x1 - x0) / n
    for i, (lab, v) in enumerate(zip(labels, vals)):
        h = (y1 - y0) * v / top
        bx = x0 + i * bw + bw * 0.15
        d.rectangle((bx, y1 - h, bx + bw * 0.7, y1), fill=spec.get('color', '#fc5200'))
        d.text((bx, y1 - h - 16), f'{v:g}', fill='black', font=font)
        d.text((bx, y1 + 6), str(lab), fill='#333', font=font)
    b = io.BytesIO(); im.save(b, 'PNG'); return b.getvalue()


def ics_bytes(ev, stamp):
    def f(s): return dt(s).astimezone(UTC).strftime('%Y%m%dT%H%M%SZ')
    org = ev.get('organizer')
    lines = ['BEGIN:VCALENDAR', 'PRODID:-//Microsoft Corporation//Outlook 16.0 MIMEDIR//EN' if ev.get('outlook') else '-//Google Inc//Google Calendar 70.9054//EN',
             'VERSION:2.0', 'METHOD:REQUEST', 'BEGIN:VEVENT',
             f'UID:{ev.get("uid") or hexid((ev["summary"], ev["start"]), 32)}', f'DTSTAMP:{f(stamp)}',
             f'DTSTART:{f(ev["start"])}', f'DTEND:{f(ev["end"])}', f'SUMMARY:{ev["summary"]}']
    if ev.get('location'): lines.append(f'LOCATION:{ev["location"]}')
    if ev.get('description'): lines.append('DESCRIPTION:' + ev['description'].replace('\n', '\\n'))
    if ev.get('rrule'): lines.append('RRULE:' + ev['rrule'])
    if org: lines.append(f'ORGANIZER;CN={org["name"]}:mailto:{org["email"]}')
    for a in ev.get('attendees', []):
        lines.append(f'ATTENDEE;CN={a["name"]};ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE:mailto:{a["email"]}')
    lines += ['STATUS:CONFIRMED', 'SEQUENCE:0', 'END:VEVENT', 'END:VCALENDAR']
    return ('\r\n'.join(lines) + '\r\n').encode()


def att_bytes(spec, when):
    kind, name = spec[0], spec[1]
    if kind == 'pdf': return name, pdf_bytes(spec[2], spec[3] if len(spec) > 3 else name, 'David Barron' if len(spec) <= 4 else spec[4], when, when), MIME['pdf']
    if kind == 'docx': return name, docx_bytes(spec[2], spec[3] if len(spec) > 3 else name, spec[4] if len(spec) > 4 else 'David Barron', when, when), MIME['docx']
    if kind == 'xlsx': return name, xlsx_bytes(spec[2], spec[3] if len(spec) > 3 else name, spec[4] if len(spec) > 4 else 'David Barron', when, when), MIME['xlsx']
    if kind == 'ics': return name, ics_bytes(spec[2], when), 'text/calendar'
    if kind == 'png': return name, png_chart(spec[2]), MIME['png']
    if kind in ('csv', 'txt'): return name, spec[2].encode(), MIME[kind]
    if kind == 'file':
        assert '/authentic/' not in os.path.abspath(spec[2])
        return name, open(spec[2], 'rb').read(), spec[3] if len(spec) > 3 else 'application/octet-stream'
    raise ValueError(kind)

# ---------------- html ----------------

def auto_html(body, title, accent='#1a73e8'):
    out = []
    for block in re.split(r'\n\s*\n', body.strip()):
        lines = block.split('\n')
        if all(' | ' in l for l in lines):
            rows = [l.split(' | ') for l in lines]
            out.append('<table style="border-collapse:collapse;width:100%;font-size:14px">' + ''.join(
                '<tr>' + ''.join(f'<td style="border-bottom:1px solid #e5e5e5;padding:6px 4px">{_html.escape(c.strip())}</td>' for c in r) + '</tr>'
                for r in rows) + '</table>')
        elif all(l.startswith(('- ', '* ')) for l in lines):
            out.append('<ul>' + ''.join(f'<li>{_html.escape(l[2:])}</li>' for l in lines) + '</ul>')
        else:
            out.append('<p>' + '<br>'.join(_html.escape(l) for l in lines) + '</p>')
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><title>' + _html.escape(title) + '</title></head>'
            '<body style="margin:0;background:#f4f4f4;font-family:Helvetica,Arial,sans-serif;color:#222">'
            '<div style="max-width:600px;margin:0 auto;background:#fff;padding:24px">'
            f'<div style="border-top:4px solid {accent};padding-top:12px;font-size:20px;font-weight:bold">' + _html.escape(title) + '</div>'
            + ''.join(out) + '</div></body></html>')

# ---------------- thread rendering ----------------

def sender_tz(person, d, flavor):
    if flavor == 'outlook': return UTC
    if person.get('tz'): return ZoneInfo(person['tz'])
    return tz_for(d)


def gmail_quote(prev, prev_date, prev_from, tz):
    when = prev_date.astimezone(tz)
    hdr = f"On {when.strftime('%a, %b')} {when.day}, {when.year} at {when.strftime('%I:%M %p').lstrip('0')} {prev_from['name']} <{prev_from['email']}> wrote:"
    return '\n\n' + hdr + '\n' + '\n'.join(('>' if l.startswith('>') else '> ') + l if l else '>' for l in prev.rstrip('\n').split('\n')) + '\n'


def outlook_quote(prev, prev_date, prev_msg, subject):
    when = prev_date.astimezone(ET if prev_date < MOVE else PT)
    to = '; '.join(p['name'] for p in prev_msg['to'])
    return ('\n\n________________________________\n'
            f"From: {prev_msg['frm']['name']} <{prev_msg['frm']['email']}>\n"
            f"Sent: {when.strftime('%A, %B')} {when.day}, {when.year} {when.strftime('%I:%M %p').lstrip('0')}\n"
            f'To: {to}\nSubject: {subject}\n\n' + prev.rstrip('\n') + '\n')


def gmail_msg_hex(d, seed):
    ms = int(d.timestamp() * 1000)
    return f'{(ms << 20) | (int(hexid(seed, 5), 16) & 0xFFFFF):016x}'


def gmail_message_id(seed, sender):
    dom = sender['email'].split('@')[1]
    h = hashlib.sha256(str(seed).encode()).digest()
    if dom in ('gmail.com', 'vt.edu') or dom.endswith('.vt.edu') or dom == 'berkeley.edu':
        tok = base64.b64encode(h + hashlib.sha256(h).digest()[:10]).decode().replace('/', '_').replace('=', '')[:52]
        return f'<CA{tok}@mail.gmail.com>'
    return f'<{h.hex()[:24]}.{h.hex()[24:32]}@{dom}>'


def filetime(d):
    return int((d.timestamp() + 11644473600) * 10_000_000)


def thread_index(first, d, guid, n_children):
    head = bytes([1]) + filetime(first).to_bytes(8, 'big')[:5] + guid
    out = head
    for i in range(n_children):
        delta = max(0, filetime(d) - filetime(first)) >> 18
        out += ((((delta * (i + 1)) // max(1, n_children)) & 0x7FFFFFFF) << 9 | (int(hexid((guid, i), 3), 16) & 0x1FF)).to_bytes(5, 'big')
    return base64.b64encode(out).decode(), head.hex()


OUTLOOK_HOSTS = ['BN8PR03MB4721', 'SJ0PR03MB6255', 'MN2PR03MB5034', 'CH3PR03MB7458', 'BL1PR03MB6019', 'DM6PR03MB4410']


def outlook_message_id(seed, sender):
    dom = sender['email'].split('@')[1]
    h = hexid(seed, 40).upper()
    if dom.endswith('vt.edu'):
        host = OUTLOOK_HOSTS[int(h[:2], 16) % len(OUTLOOK_HOSTS)]
        return f'<{host}{h[:20]}@{host}.namprd03.prod.outlook.com>'
    return gmail_message_id(seed, sender)


def is_me(person, acct):
    return person['email'].lower() == acct.lower()


def render_threads(g, acct, threads, flavor='gmail', min_date=None, modeled_on=''):
    """Write every thread; returns stats dict."""
    stats = dict(threads=0, messages=0, attachments=0, projects={}, hard=[], first=None, last=None)
    lo = dt(min_date) if min_date else SCOPE_LO
    seen_ids = set()
    for ti, t in enumerate(threads):
        msgs = t['msgs']
        dates = [dt(m['date']) for m in msgs]
        for a, b in zip(dates, dates[1:]):
            assert b > a, f'{acct} thread {t["subject"]!r}: dates not ascending ({a} -> {b})'
        assert dates[0] >= lo and dates[-1] <= REF, f'{acct} thread {t["subject"]!r}: date outside scope {dates[0]}..{dates[-1]}'
        seed0 = (acct, t['subject'], msgs[0]['date'])
        if flavor == 'gmail':
            tid = gmail_msg_hex(dates[0], seed0)
        else:
            guid = bytes.fromhex(hexid(seed0, 32))
            tid = thread_index(dates[0], dates[0], guid, 0)[1]
        assert tid not in seen_ids, tid; seen_ids.add(tid)
        if flavor == 'gmail':  # real Gmail layout: thread-f_<decimal thread id>; sent-only threads thread-a_r-<decimal>
            if all(is_me(m['frm'], acct) for m in msgs):
                n = int(hexid(('a_r', seed0), 16), 16) % 9_000_000_000_000_000_000 + 1_000_000_000_000_000_000
                tdir = f"thread-a_r-{n}" if int(hexid(('sign', seed0), 2), 16) % 4 else f"thread-a_r{n}"
            else:
                tdir = f'thread-f_{int(tid, 16)}'
        else:
            tdir = tid
        key = f'{acct}/threads/{tdir}'
        notes = t.get('notes')
        has_att = any(m['att'] for m in msgs)
        if not notes and has_att: notes = 'HARD CASE: email with attachments — ' + ', '.join(a[1] for m in msgs for a in m['att'])
        mids, bodies = [], []
        for mi, (m, d) in enumerate(zip(msgs, dates)):
            frm = m['frm']
            tz = sender_tz(frm, d, flavor)
            subj = m['subject'] or (t['subject'] if mi == 0 else ('RE: ' if flavor == 'outlook' else 'Re: ') + re.sub(r'^(re|RE|Re|fwd|Fwd|FW):\s*', '', t['subject']))
            body = m['body']
            ri = m['reply_to'] if m['reply_to'] is not None else mi - 1
            q = m['quote'] if m['quote'] is not None else t['quote']
            if mi > 0 and q:
                if flavor == 'gmail' and subj.startswith('Fwd:'):
                    pf, pd = msgs[ri]['frm'], dates[ri].astimezone(tz_for(d))
                    body = body.rstrip('\n') + ('\n\n---------- Forwarded message ---------\n'
                        f"From: {pf['name']} <{pf['email']}>\nDate: {pd.strftime('%a, %b')} {pd.day}, {pd.year} at {pd.strftime('%I:%M %p').lstrip('0')}\n"
                        f"Subject: {msgs[ri]['subject'] or t['subject']}\nTo: {', '.join(x['name'] + ' <' + x['email'] + '>' for x in msgs[ri]['to'])}\n\n"
                        + bodies[ri].rstrip('\n') + '\n')
                elif flavor == 'gmail':
                    body = body.rstrip('\n') + gmail_quote(bodies[ri], dates[ri], msgs[ri]['frm'], tz_for(d) if is_me(frm, acct) else tz)
                else:
                    body = body.rstrip('\n') + outlook_quote(bodies[ri], dates[ri], msgs[ri], msgs[ri]['subject'] or t['subject'])
            bodies.append(body)
            seed = (acct, tid, mi, m['date'])
            mid = gmail_message_id(seed, frm) if flavor == 'gmail' else outlook_message_id(seed, frm)
            headers = {}
            if flavor == 'gmail':
                mhex = tid if mi == 0 else gmail_msg_hex(d, seed)
                if is_me(frm, acct): labs = ['Sent']
                else:
                    labs = [l for l in t['labels']]
                    labs.append('Unread' if m['unread'] else 'Opened')
                headers['X-GM-THRID'] = str(int(tid, 16))
                headers['X-Gmail-Labels'] = ','.join(labs)
            else:
                mhex = hexid(mid, 16)
                ti_b64, _ = thread_index(dates[0], d, guid, mi)
                headers['Thread-Topic'] = re.sub(r'^(re|RE|Re|fwd|Fwd|FW):\s*', '', t['subject'])
                headers['Thread-Index'] = ti_b64
                headers['Content-Language'] = 'en-US'
                headers['X-MS-Has-Attach'] = 'yes' if m['att'] else ''
                headers['X-MS-TNEF-Correlator'] = ''
                internal = frm['email'].endswith('vt.edu')
                headers['X-MS-Exchange-Organization-SCL'] = '-1' if internal else '1'
                headers['X-MS-Exchange-Organization-AuthAs'] = 'Internal' if internal else 'Anonymous'
                headers['X-MS-Exchange-Organization-AuthSource'] = OUTLOOK_HOSTS[int(hexid(mid, 2), 16) % len(OUTLOOK_HOSTS)] + '.namprd03.prod.outlook.com'
                headers['X-MS-Exchange-Organization-Network-Message-Id'] = uid(('netmsg', mid))
                headers['X-MS-Exchange-Organization-RecordReviewCfmType'] = '0'
                headers['X-MS-Exchange-CrossTenant-OriginalArrivalTime'] = d.astimezone(UTC).strftime('%d %b %Y %H:%M:%S.') + f'{int(hexid(mid, 3), 16) % 1000:03d} (UTC)'
            headers.update(m['headers'])
            html = auto_html(m['body'], subj, accent=m.get('accent', '#1a73e8')) if m['html'] is True else m['html']
            atts = [att_bytes(a, d) for a in m['att']]
            stats['attachments'] += len(atts)
            fname = f"{mhex}.eml" if flavor == 'gmail' else f"{d.astimezone(UTC):%Y%m%d-%H%M%S}_{mhex}.eml"
            to = [addr((p['name'], p['email'])) for p in m['to']]
            cc = [addr((p['name'], p['email'])) for p in m['cc']] if m['cc'] else None
            g.eml(f'{key}/{fname}', frm=(frm['name'], frm['email']), to=to, cc=cc, subject=subj, date=d.astimezone(tz), body=body,
                  html=html, attachments=atts, message_id=mid,
                  in_reply_to=mids[ri] if mi > 0 else None, references=' '.join(mids[:ri + 1]) if mi > 0 else None,
                  headers=headers, account=acct, project_ids=t['projects'], label_key=key, label_notes=notes,
                  modeled_on=t.get('modeled_on') or modeled_on, notes=notes or '')
            mids.append(mid)
        g.dir_times(key, dates[0], dates[-1])
        stats['threads'] += 1; stats['messages'] += len(msgs)
        for p in t['projects']: stats['projects'][p] = stats['projects'].get(p, 0) + 1
        if notes and notes.startswith('HARD CASE'): stats['hard'].append((key, notes.split(' — ')[0]))
        stats['first'] = min(stats['first'] or dates[0], dates[0]); stats['last'] = max(stats['last'] or dates[-1], dates[-1])
    return stats


def report(acct, s):
    print(f"  {acct}: {s['threads']} threads, {s['messages']} messages, {s['attachments']} attachments, "
          f"{s['first']:%Y-%m-%d} .. {s['last']:%Y-%m-%d}")
    print('    projects:', dict(sorted(s['projects'].items(), key=lambda x: -x[1])))
    hk = {}
    for k, h in s['hard']: hk[h] = hk.get(h, 0) + 1
    print('    hard cases:', hk)


if __name__ == '__main__':
    g = Gen('gmail')
    MOD = 'authentic/gmail <account>/threads/<thread>/ layout (one raw .eml per message), Gmail Takeout-style X-Gmail-Labels headers'
    for acct, name, lo in [('david.barron.runs@gmail.com', 'runs', '2025-12-03 00:00'),
                           ('davidbarron410@gmail.com', 'personal', None),
                           ('dbarron410@vt.edu', 'vt', None)]:
        path = os.path.join(CONTENT, 'gmail', name + '.py')
        if not os.path.exists(path): print('  (missing content)', path); continue
        threads = load_threads('gmail', name)
        if name == 'runs':  # the whole account is the 'second email account' hard case; clutter threads are 'personal clutter'
            for t in threads:
                if t.get('notes'): continue
                kind = 'personal clutter' if t['projects'] == ['project_none'] else 'second email account'
                t['notes'] = f"HARD CASE: {kind} — david.barron.runs@gmail.com: {t['subject']}"
                atts = [a[1] for m in t['msgs'] for a in m['att']]
                if atts: t['notes'] += '; email with attachments: ' + ', '.join(atts)
        s = render_threads(g, acct, threads, 'gmail', lo, MOD)
        report(acct, s)
    g.finish()
