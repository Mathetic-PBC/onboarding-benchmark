"""Shared helpers: copy items into benchmark-data preserving timestamps, and keep per-folder MANIFEST.csv files."""
import csv, os, shutil, subprocess, datetime

ROOT = os.path.expanduser('~/Desktop/benchmark/benchmark-data')
FIELDS = ['path', 'tool', 'account_or_library', 'date', 'origin', 'source', 'modeled_on', 'notes']


def iso(ts):
    return datetime.datetime.fromtimestamp(ts).astimezone().isoformat(timespec='seconds')


def mtime(p):
    return iso(os.stat(p).st_mtime)


class Manifest:
    """Rows keyed by path; rewrites the CSV on save so reruns don't duplicate rows."""

    def __init__(self, side, folder):
        self.dir = os.path.join(ROOT, side, folder)
        os.makedirs(self.dir, exist_ok=True)
        self.file = os.path.join(self.dir, 'MANIFEST.csv')
        self.rows = {}
        if os.path.exists(self.file):
            with open(self.file, newline='') as f:
                for r in csv.DictReader(f):
                    self.rows[r['path']] = r

    def add(self, path, tool, account, date, origin='authentic', source='', modeled_on='', notes=''):
        rel = os.path.relpath(path, self.dir) if os.path.isabs(path) else path
        self.rows[rel] = dict(path=rel, tool=tool, account_or_library=account, date=date, origin=origin,
                              source=source, modeled_on=modeled_on, notes=notes)

    def save(self):
        with open(self.file, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            for k in sorted(self.rows):
                w.writerow(self.rows[k])
        return len(self.rows)


def copy(src, dest):
    """Copy a file or directory preserving timestamps/metadata (ditto). Never touches src."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    subprocess.run(['ditto', src, dest], check=True)
    return dest


def set_mtime(path, ts):
    os.utime(path, (ts, ts))
