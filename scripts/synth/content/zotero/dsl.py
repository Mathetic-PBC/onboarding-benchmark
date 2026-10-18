"""Tiny markup used by the zotero / overleaf / pdfs generators' hand-written content.

  # Heading 1        ## Heading 2        ### Heading 3
  - bullet           1. numbered item
  | a | b | c        table row (first row of a run = header)
  > quote            ``` ... ```  code block
  ===                page break
  blank line         paragraph break (consecutive text lines are joined)
"""
import re


def parse(text):
    blocks, para, table, code = [], [], [], None
    cont = False  # previous line was a list item (continuation lines are appended to it)

    def flush():
        nonlocal para, table
        if para: blocks.append(('p', ' '.join(para))); para = []
        if table: blocks.append(('table', table)); table = []

    for raw in text.strip('\n').split('\n'):
        line = raw.rstrip()
        if code is not None:
            if line.strip() == '```': blocks.append(('code', '\n'.join(code))); code = None
            else: code.append(raw)
            continue
        s = line.strip()
        if s == '```': flush(); code = []; continue
        if not s: flush(); cont = False; continue
        if cont and not re.match(r'^(#{1,3} |- |\d+\. |> |\||===|```)', s):
            k, v = blocks[-1]; blocks[-1] = (k, v + ' ' + s); continue
        cont = False
        if s == '===': flush(); blocks.append(('pagebreak', None)); continue
        m = re.match(r'^(#{1,3}) (.*)$', s)
        if m: flush(); blocks.append(('h' + str(len(m.group(1))), m.group(2))); continue
        if s.startswith('|'):
            if para: blocks.append(('p', ' '.join(para))); para = []
            table.append([c.strip() for c in s.strip('|').split('|')]); continue
        if table: blocks.append(('table', table)); table = []
        if s.startswith('- '): flush(); blocks.append(('bullet', s[2:])); cont = True; continue
        m = re.match(r'^(\d+)\. (.*)$', s)
        if m: flush(); blocks.append(('number', s)); cont = True; continue
        if s.startswith('> '): flush(); blocks.append(('quote', s[2:])); continue
        para.append(s)
    flush()
    return blocks


_TEX = [('\\', r'\textbackslash{}'), ('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}'),
        ('~', r'\textasciitilde{}'), ('^', r'\textasciicircum{}'), ('—', '---'), ('–', '--'), ('“', '``'), ('”', "''"), ('’', "'"),
        ('‘', '`'), ('…', r'\ldots{}'), ('->', r'$\rightarrow$'), ('<=', r'$\leq$'), ('>=', r'$\geq$'), ('<', r'$<$'), ('>', r'$>$')]


def tex(s):
    """Escape plain text for LaTeX. [[raw]] passes LaTeX through untouched (used for \\cite{...})."""
    parts = re.split(r'(\[\[.*?\]\])', s)
    out = []
    for part in parts:
        if part.startswith('[[') and part.endswith(']]'):
            out.append(part[2:-2]); continue
        t = part
        # placeholder for backslash so later replacements don't double-escape it
        t = t.replace('\\', '\x00')
        for a, b in _TEX[1:]:
            t = t.replace(a, b)
        t = t.replace('\x00', r'\textbackslash{}')
        t = re.sub(r'"([^"]*)"', r"``\1''", t)
        out.append(t)
    return ''.join(out)


def plain(s):
    """Strip [[raw]] LaTeX markers for PDF/plain renderings (\\cite{x} -> [x])."""
    def rep(m):
        inner = m.group(1)
        c = re.match(r'\\cite[pt]?\{([^}]*)\}', inner)
        if c: return '[' + c.group(1).replace(',', ', ') + ']'
        return re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', inner)
    return re.sub(r'\[\[(.*?)\]\]', rep, s)


def plain_blocks(blocks):
    out = []
    for k, v in blocks:
        if k == 'table': out.append((k, [[plain(c) for c in r] for r in v]))
        elif isinstance(v, str): out.append((k, plain(v)))
        else: out.append((k, v))
    return out


def to_latex(blocks, h1='section', h2='subsection', h3='subsubsection', caption_prefix=None):
    out, in_list = [], None
    tcount = 0

    def close():
        nonlocal in_list
        if in_list: out.append('\\end{%s}' % in_list); in_list = None

    for k, v in blocks:
        if k in ('bullet', 'number'):
            env = 'itemize' if k == 'bullet' else 'enumerate'
            if in_list != env: close(); out.append('\\begin{%s}' % env); in_list = env
            txt = re.sub(r'^\d+\. ', '', v) if k == 'number' else v
            out.append('  \\item ' + tex(txt)); continue
        close()
        if k in ('h1', 'h2', 'h3'):
            cmd = {'h1': h1, 'h2': h2, 'h3': h3}[k]
            title = re.sub(r'^\d+(\.\d+)*\.? ', '', v)
            out.append('\n\\%s{%s}' % (cmd, tex(title)))
        elif k == 'p': out.append('\n' + tex(v))
        elif k == 'quote': out.append('\\begin{quote}\n' + tex(v) + '\n\\end{quote}')
        elif k == 'code': out.append('\\begin{verbatim}\n' + v + '\n\\end{verbatim}')
        elif k == 'pagebreak': out.append('\\clearpage')
        elif k == 'table':
            tcount += 1
            n = max(len(r) for r in v)
            cols = 'l' + 'r' * (n - 1) if all(re.match(r'^[\d.,%+\-– ]+$|^—$', c or '0') for r in v[1:] for c in r[1:]) else 'l' * n
            lens = [max(len(r[j]) if j < len(r) else 0 for r in v) for j in range(n)]
            if sum(lens) > 75:  # wide table: wrap long text columns
                tot = sum(lens)
                cols = ''.join(('p{%.1fcm}' % max(1.6, 13.0 * L / tot)) if L > 18 else 'l' for L in lens)
            rows = [' & '.join(tex(c) for c in r) + ' \\\\' for r in v]
            cap = (caption_prefix[tcount - 1] if caption_prefix and tcount - 1 < len(caption_prefix) else None)
            out.append('\\begin{table}[h]\n\\centering\n\\small\n' + (('\\caption{%s}\n' % tex(cap)) if cap else '') +
                       '\\begin{tabular}{%s}\n\\toprule\n%s\n\\midrule\n%s\n\\bottomrule\n\\end{tabular}\n\\end{table}' %
                       (cols, rows[0], '\n'.join(rows[1:])))
    close()
    return '\n'.join(out) + '\n'
