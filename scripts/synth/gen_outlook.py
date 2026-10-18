"""Synthetic Outlook (VT Microsoft 365, dbarron410@vt.edu): one item per conversation
(dbarron410@vt.edu/threads/<44-hex conversation id from Thread-Index>/<yyyymmdd-hhmmss>_<16 hex>.eml).
Hand-written content: _scripts/synth/content/outlook/vt.py. Rendering helpers come from gen_gmail.py."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *
from gen_gmail import load_threads, render_threads, report

if __name__ == '__main__':
    g = Gen('outlook')
    MOD = 'authentic/outlook dbarron410@vt.edu/threads/<conversation>/<yyyymmdd-hhmmss>_<id>.eml layout (Thread-Index, X-MS-Exchange headers)'
    s = render_threads(g, 'dbarron410@vt.edu', load_threads('outlook', 'vt'), 'outlook', None, MOD)
    report('dbarron410@vt.edu', s)
    g.finish()
