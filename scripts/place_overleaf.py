"""Place Overleaf projects into authentic/overleaf/.

Read 2026-10-18 from overleaf.com, signed in by David in Chrome (read-only):
_incoming/overleaf/projects.json   project list (the project dashboard's ol-prefetchedProjectsBlob)
_incoming/overleaf/zips/<id>.zip   each project's source zip (/project/<id>/download/zip, Overleaf's own "Download > Source")
Output: authentic/overleaf/<account>/<project name>.zip (mtime = lastUpdated) and <account>/_collection/projects.json.
One zip per project, kept as Overleaf serves it.
"""
import datetime, json, os, re, shutil, sys, zipfile
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, set_mtime

INC = os.path.join(ROOT, '_incoming/overleaf')
ACCT = 'dbarron410@vt.edu'
DST = os.path.join(ROOT, 'authentic/overleaf', ACCT)

blob = json.load(open(os.path.join(INC, 'projects.json')))
m = Manifest('authentic', 'overleaf')
m.rows = {}
os.makedirs(os.path.join(DST, '_collection'), exist_ok=True)
shutil.copyfile(os.path.join(INC, 'projects.json'), os.path.join(DST, '_collection/projects.json'))
m.add(f'{ACCT}/_collection/projects.json', 'overleaf', ACCT, '', notes=f'Overleaf project list ({len(blob["projects"])} projects: name, owner, access level, archived/trashed, lastUpdated)')
used, missing = set(), []
for p in blob['projects']:
    src = os.path.join(INC, 'zips', p['id'] + '.zip')
    if not os.path.exists(src) or not zipfile.is_zipfile(src):
        missing.append(p); continue
    name = re.sub(r'[/\\:\x00-\x1f]', '_', p['name']).strip()[:150]
    if name.lower() in used: name = f'{name} ({p["id"][:8]})'
    used.add(name.lower())
    dst = os.path.join(DST, name + '.zip')
    shutil.copyfile(src, dst)
    set_mtime(dst, datetime.datetime.fromisoformat(p['lastUpdated'].replace('Z', '+00:00')).timestamp())
    with zipfile.ZipFile(src) as z:
        files = [i.filename for i in z.infolist() if not i.is_dir()]
    owner = (p.get('owner') or {}).get('email')
    by = (p.get('lastUpdatedBy') or {}).get('email')
    notes = [f'project id {p["id"]}', f'owner {owner}', f'access {p["accessLevel"]} ({p["source"]})', f'{len(files)} files',
             f'main .tex candidates: {[f for f in files if f.endswith(".tex")][:5]}']
    if by: notes.append(f'last updated by {by}')
    if p.get('archived'): notes.append('archived')
    if p.get('trashed'): notes.append('trashed')
    m.add(f'{ACCT}/{name}.zip', 'overleaf', ACCT, p['lastUpdated'], source=f'https://www.overleaf.com/project/{p["id"]}', notes='; '.join(notes))
    print(p['lastUpdated'][:10], len(files), name[:70])
json.dump(missing, open(os.path.join(DST, '_collection/not_collected.json'), 'w'), indent=1)
m.add(f'{ACCT}/_collection/not_collected.json', 'overleaf', ACCT, '', notes=f'{len(missing)} listed projects without a zip')
print('placed', len(blob['projects']) - len(missing), 'missing', len(missing), 'rows', m.save())
