import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, copy, mtime
H = os.path.expanduser('~')
m = Manifest('authentic', 'pdfs')
lst = sys.argv[1]
SKIP = ('./.claude/projects/', './.claude-vault/', './Library/Group Containers/UBF8T346G9.Office/', './Library/Application Support/Engelbart/', './.engelbart/', './Desktop/benchmark/', './.Trash/', './Library/Caches/')
n = 0
for line in open(lst):
    rel = line.rstrip('\n')
    if rel.startswith(SKIP) or '/node_modules/' in rel: continue
    src = os.path.join(H, rel[2:])
    if not os.path.isfile(src): continue
    loc = rel[2:].replace('Library/Mobile Documents/com~apple~CloudDocs', 'iCloud Drive')
    dest = os.path.join(m.dir, loc)
    copy(src, dest)
    top = loc.split('/')[0]
    notes = []
    if '/fixtures/' in loc or '/build/' in loc or '/public/' in loc: notes.append('inside a code repo (fixture/build asset)')
    if 'memex-engelbart-bundle' in loc: notes.append('inside an Engelbart/memex export bundle on Desktop (copies)')
    if '/repos/' in loc: notes.append('inside a cloned repo')
    m.add(loc, 'PDFs on this Mac', top if top != 'iCloud Drive' else 'iCloud Drive', mtime(src), source='~/' + rel[2:], notes='; '.join(notes))
    n += 1
print(n, m.save())
