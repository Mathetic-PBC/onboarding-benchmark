"""Render a fictional paper from papers.py to PDF bytes. Shared by gen_zotero and gen_pdfs so copies are byte-identical."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from synthlib import pdf_bytes, dt
import dsl


def creators_short(authors):
    if len(authors) == 1: return authors[0][0]
    if len(authors) == 2: return f'{authors[0][0]} and {authors[1][0]}'
    return f'{authors[0][0]} et al.'


def venue_line(p):
    if p['type'] == 'inproceedings':
        return f"In {p['booktitle']} ({p.get('series', '')})" + (f", pp. {p['pages'].replace('--', '-')}" if p.get('pages') else '') + '.'
    if p['type'] == 'article' and p.get('eprint'):
        return f"arXiv:{p['eprint']} [{p['primaryclass']}], {dt(p['pub']).strftime('%-d %b %Y')}"
    if p['type'] == 'article':
        return f"{p['journal']} {p.get('volume', '')}({p.get('number', '')}), {p['year']}, pp. {p.get('pages', '').replace('--', '-')}."
    if p['type'] == 'techreport':
        return f"{p['institution']}, {p['number']}, {dt(p['pub']).strftime('%B %Y')}."
    return str(p['year'])


def paper_pdf(p):
    names = ', '.join(f'{first} {last}' for last, first in p['authors'])
    blocks = [('title', p['title']), ('p', names), ('p', venue_line(p)), ('h2', 'Abstract'), ('p', p['abstract'])]
    blocks += dsl.parse(p['body'])
    blocks.append(('h1', 'References'))
    for i, r in enumerate(p['refs'], 1): blocks.append(('p', f'[{i}] {r}'))
    return pdf_bytes(blocks, p['title'], '', p['pub'], p['pub'])
