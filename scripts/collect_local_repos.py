import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, mtime
H = os.path.expanduser('~')
m = Manifest('authentic', 'github')
EXC = ['node_modules', '.venv', 'venv', '__pycache__', '.next', 'dist', 'out', 'release', '.turbo']
def git(r, *a):
    return subprocess.run(['git', '-C', r, *a], capture_output=True, text=True).stdout.strip()
for line in open(sys.argv[1]):
    rel = line.strip()[2:]
    src = os.path.join(H, rel)
    dest = os.path.join(m.dir, 'local-repos', rel)
    os.makedirs(dest, exist_ok=True)
    cmd = ['rsync', '-a'] + sum([['--exclude', e] for e in EXC], []) + [src + '/', dest + '/']
    subprocess.run(cmd, check=True)
    remote = git(src, 'remote', 'get-url', 'origin')
    last = git(src, 'log', '-1', '--format=%cI')
    first = git(src, 'log', '--reverse', '--format=%cI')[:25]
    branch = git(src, 'rev-parse', '--abbrev-ref', 'HEAD')
    ncommits = git(src, 'rev-list', '--all', '--count')
    dirty = len(git(src, 'status', '--porcelain').splitlines())
    notes = f'local working copy + .git (excluded: {",".join(EXC)}); branch={branch}; commits(all refs)={ncommits}; first commit={first}; uncommitted changes={dirty}'
    if not remote: notes += '; no remote (local-only repo)'
    if '-' in os.path.basename(rel) and remote and any(k in rel for k in ['berkeley-research-', 'claude-plugins-']): notes += '; HARD CASE: worktree-style duplicate checkout of the same remote'
    m.add(os.path.join('local-repos', rel), 'Local git repo', remote or 'local only', last or mtime(src), source='~/' + rel, notes=notes)
    print(rel, remote, last, flush=True)
print(m.save())
