"""Tiny data DSL for the hand-written mail content (gmail + outlook). Content modules build THREADS = [T(...), ...].

T(subject, projects, msgs, labels=('Inbox',), notes=None, quote=True, modeled_on='')
M(date, frm, to, body, cc=None, html=None, att=(), subject=None, quote=None, unread=False, reply_to=None)
   date: 'YYYY-MM-DD HH:MM' local to David (ET until 2026-08-08, PT after). The Date header is written in the sender's tz
   (person tz, or David's tz for David / automated senders without tz).
   html: True -> HTML alternative generated from the plain body; or an HTML string.
   quote: None -> thread default (quote previous message under "On ... wrote:"); False -> no quote.
   reply_to: index of the message this one answers (default: the previous one).
A(kind, name, ...) attachment specs:
   A('pdf'|'docx', name, blocks, title)   blocks as synthlib: [('h1','..'),('p','..'),('bullet','..'),('table',[[..],..])]
   A('xlsx', name, {sheet: rows}, title)
   A('ics', name, dict(summary=, start='YYYY-MM-DD HH:MM', end=, location=, description=, organizer=PERSON, attendees=[PERSON]))
   A('png', name, dict(title=, labels=[..], values=[..], ylabel=))  -> a small bar chart image
   A('file', name, abs_path, mime)        A('csv'|'txt', name, text)
"""

def P(name, email, tz=None):
    return dict(name=name, email=email, tz=tz)

ET, PT, UK, IE = 'America/New_York', 'America/Los_Angeles', 'Europe/London', 'Europe/Dublin'

# David
ME_VT = P('David Barron', 'dbarron410@vt.edu')
ME_G = P('David Barron', 'davidbarron410@gmail.com')
ME_R = P('David Barron', 'david.barron.runs@gmail.com')

# people (addresses are invented)
HUDSON = P('Hudson Mitchell-Pullman', 'hudson@mathetic-pbc.com', PT)
YAN = P('Yan Chen', 'ychen.prime@vt.edu', ET)
GRACE = P('Grace Kim', 'gracek.csgrad@vt.edu', ET)
BROOKS = P('Alan Brooks', 'abrooks.ise@vt.edu', ET)
MINSUN = P('Minsun', 'msun.prime@vt.edu', ET)
XIAOHANG = P('Xiaohang', 'xhang.prime@vt.edu', ET)
REZKY = P('Rezky', 'rezky.prime@vt.edu', ET)
YUE = P('Yue', 'yue.prime@vt.edu', ET)
WENSKOVITCH = P('John Wenskovitch', 'jwensk.cs@vt.edu', ET)
PRIYA = P('Priya Raman', 'priya.raman@berkeley.edu', PT)
MARCUS = P('Marcus Oyelaran', 'marcus@northfieldangels.com', PT)
LENA = P('Lena Hoffmann', 'lena@surplus-sf.org', PT)
TOMAS = P('Tomás Reyes', 'tomas.reyes.hci@gmail.com', ET)
OWEN = P('Owen Patel', 'owen.patel.runs@gmail.com', ET)
SAM = P('Sam Whitaker', 'sam.whitaker.sf@gmail.com', PT)
NIAMH = P('Niamh Barron', 'niamh.barron.dub@gmail.com', IE)
KEVIN = P('Kevin Liu', 'kevin.liu@stackforge.dev', PT)
ELENA = P('Elena Park', 'elena.park@berkeley.edu', PT)
BEN = P('Ben Adeyemi', 'b.adeyemi@berkeley.edu', PT)
DANIEL = P('Daniel Osei', 'dosei@andrew.cmu.edu', ET)
MAYA = P('Maya Torres', 'mayat.ise@vt.edu', ET)
JORDAN = P('Jordan Lee', 'jordanlee.ise@vt.edu', ET)


def M(date, frm, to, body, cc=None, html=None, att=(), subject=None, quote=None, unread=False, reply_to=None, headers=None):
    return dict(date=date, frm=frm, to=to if isinstance(to, list) else [to], body=body.strip('\n') + '\n', cc=cc, html=html,
                att=list(att), subject=subject, quote=quote, unread=unread, reply_to=reply_to, headers=headers or {})


def T(subject, projects, msgs, labels=('Inbox',), notes=None, quote=True, modeled_on=''):
    return dict(subject=subject, projects=list(projects), msgs=msgs, labels=list(labels), notes=notes, quote=quote, modeled_on=modeled_on)


def A(kind, name, *args):
    return (kind, name) + tuple(args)
