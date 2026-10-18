#!/usr/bin/env python3
"""Rebuild README.md from the documentation page, so the README is usable on GitHub.

GitHub can't run the page's tabs, so each tab becomes a collapsible section. The JSON samples come from the
page's <script type="application/json"> blocks, and the Sources tab from its SOURCES list (read with Node,
since it's JavaScript). Edit the HTML, then run:  python3 docs/build_readme.py
"""
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'docs' / 'onboarding-benchmark-and-dataset-documentation.html'
OUT = ROOT / 'README.md'
VOID = {'br', 'hr', 'img', 'meta', 'link', 'input'}


class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs or {}), parent, []


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = Node('root')

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(html):
    t = Tree()
    t.feed(html)
    return t.root


def find(node, pred):
    if isinstance(node, str):
        return None
    if pred(node):
        return node
    for c in node.children:
        hit = find(c, pred)
        if hit:
            return hit
    return None


def text_of(node):
    return node if isinstance(node, str) else ''.join(text_of(c) for c in node.children)


def inline(node, cell=False):
    if isinstance(node, str):
        s = re.sub(r'\s+', ' ', node).replace('<', '&lt;').replace('>', '&gt;')
        return s.replace('|', '\\|') if cell else s
    if node.tag == 'code':
        s = re.sub(r'\s+', ' ', text_of(node))
        if cell:
            s = s.replace('|', '\\|')
        tick = '``' if '`' in s else '`'
        return f'{tick}{s}{tick}'
    if node.tag in ('b', 'strong'):
        return '**' + ''.join(inline(c, cell) for c in node.children).strip() + '**'
    if 'sources-hover' in node.attrs.get('class', ''):
        return node.attrs.get('title', '')
    return ''.join(inline(c, cell) for c in node.children)


def inline_html(html):
    return inline(parse(html)).strip()


def table(node):
    rows = [r for r in iter_tags(node, 'tr')]
    cells = [[inline(c, cell=True).strip() for c in r.children if not isinstance(c, str) and c.tag in ('th', 'td')] for r in rows]
    if not cells:
        return ''
    out = ['| ' + ' | '.join(cells[0]) + ' |', '|' + '---|' * len(cells[0])]
    out += ['| ' + ' | '.join(r) + ' |' for r in cells[1:]]
    return '\n'.join(out) + '\n'


def iter_tags(node, tag):
    for c in node.children:
        if isinstance(c, str):
            continue
        if c.tag == tag:
            yield c
        else:
            yield from iter_tags(c, tag)


def json_block(label, obj):
    return f'**{label}**\n\n```json\n{json.dumps(obj, indent=2, ensure_ascii=False)}\n```\n'


def blocks(node, ctx, depth=3):
    out = []
    for c in node.children:
        if isinstance(c, str):
            if c.strip():
                out.append(inline(c).strip() + '\n')
            continue
        tag, a = c.tag, c.attrs
        if tag in ('dialog', 'button', 'nav'):
            continue
        if a.get('id') in ('srclist', 'srcdetail'):
            continue
        if tag == 'h2':
            out.append('#' * depth + ' ' + inline(c).strip() + '\n')
        elif tag == 'h3':
            out.append('#' * (depth + 1) + ' ' + inline(c).strip() + '\n')
        elif tag == 'p':
            out.append(inline(c).strip() + '\n')
        elif tag == 'pre':
            out.append('```\n' + text_of(c).strip('\n') + '\n```\n')
        elif tag == 'table':
            out.append(table(c))
            samples = [r for r in iter_tags(c, 'tr') if r.attrs.get('data-json-id')]
            for r in samples:
                name = text_of(r.children[[i for i, x in enumerate(r.children) if not isinstance(x, str)][0]]).strip()
                out.append(details(f'Sample: {name}', json_block(name, ctx['json'][r.attrs['data-json-id']])))
        elif tag == 'ul':
            out.append(''.join('- ' + inline(li).strip() + '\n' for li in iter_tags(c, 'li')))
        elif tag == 'details':
            summary = find(c, lambda n: n.tag == 'summary')
            body = Node('div')
            body.children = [x for x in c.children if x is not summary]
            out.append(details(text_of(summary).strip() if summary else 'Details', blocks(body, ctx, depth)))
        elif tag == 'div' and a.get('data-json'):
            out.append(json_block(a.get('data-label', ''), ctx['json'][a['data-json']]))
        else:
            out.append(blocks(c, ctx, depth))
    return '\n'.join(x for x in out if x)


def details(summary, body, open_=False):
    return f'<details{" open" if open_ else ""}>\n<summary>{summary}</summary>\n\n{body.strip()}\n\n</details>\n'


def read_sources(html):
    # The Sources tab is drawn by the page's script from SOURCES and buildRow(); run that part with Node.
    script = max(re.findall(r'<script>([\s\S]*?)</script>', html), key=len)
    start, end = script.index('const SOURCES'), script.index('function el(')
    code = script[start:end] + '\n;globalThis.__out = SOURCES.map((s, i) => ({ ...s, row: buildRow(s, i) }));'
    runner = "const vm=require('vm');const c={};vm.runInNewContext(require('fs').readFileSync(0,'utf8'),c);process.stdout.write(JSON.stringify(c.__out));"
    return json.loads(subprocess.run(['node', '-e', runner], input=code, capture_output=True, text=True, check=True).stdout)


def sources_md(sources):
    out, group = [], None
    for s in sources:
        if s['group'] != group:
            group = s['group']
            out.append(f'#### {group}\n')
        checked = ('from the Onboarding 3 code reading' if s.get('checked') == 'code'
                   else "not checked; the file type above is a best guess at the platform's export, so check it against what the /goal run produced")
        notes = [f"- **Analysis unit:** `{s['unit']}` (what `sample.unit` counts)",
                 f"- **Engelbart today:** {inline_html(s['route'])} ({checked})"]
        if s.get('hard'):
            notes.append('- **Hard cases to plant:**\n' + '\n'.join('  - ' + inline_html(h) for h in s['hard']))
        if s['s'].get('prov') == 'synthetic':
            notes.append('\n`modeled_on` is an addition from the `/goal` manifest rule, not part of the original schema.')
        body = (f"`{s['id']}/`\n\n- **Stored as:** {inline_html(s['stored'])}\n- **One source item =** {inline_html(s['item'])}\n\n"
                + json_block('source_items row', s['row']) + '\n' + details('Notes', '\n'.join(notes)))
        out.append(details(s['label'], body))
    return '\n'.join(out)


def main():
    html = PAGE.read_text()
    ctx = {'json': {i: json.loads(b) for i, b in re.findall(r'<script type="application/json" id="([^"]+)">([\s\S]*?)</script>', html)}}
    root = parse(re.sub(r'<(script|style)[\s\S]*?</\1>', '', html))
    title = text_of(find(root, lambda n: n.tag == 'h1')).strip()
    header = find(root, lambda n: n.tag == 'header')
    lede = inline(find(header, lambda n: n.tag == 'p')).strip()
    tabs = [(a.attrs['data-tab'], text_of(a).strip()) for a in iter_tags(find(root, lambda n: n.attrs.get('id') == 'tabs'), 'a')]
    parts = [f'<!-- Built from {PAGE.relative_to(ROOT)} by docs/build_readme.py. Edit the page, then rerun the script. -->\n',
             f'# {title}\n', lede + '\n',
             f'The page itself, with its tabs: [{PAGE.name}]({PAGE.relative_to(ROOT).as_posix()}) (open it in a browser after cloning). '
             'Each tab is a section below; click one to open it.\n']
    for i, (tab, label) in enumerate(tabs):
        panel = find(root, lambda n, t=tab: n.tag == 'section' and n.attrs.get('id') == t)
        body = sources_md(read_sources(html)) if tab == 'sources' else blocks(panel, ctx)
        parts.append(details(f'<b>{label}</b>', body, open_=(i == 0)))
    OUT.write_text('\n'.join(parts))
    print(f'wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    main()
