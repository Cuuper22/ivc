#!/usr/bin/env python3
"""Pick 60 glossed texts across the grammar and write GLOSSES.md."""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import pandas as pd, numpy as np
from gloss2 import *
d = load2(); lex = learn(d); own = lex['owner']
d['r'] = [parse_face(x, lex, own) for x in d.tok]
d['gloss'] = [sentence(x, r) for x, r in zip(d.tok, d.r)]
d['obj'] = [object_id(i) for i in d['id']]
d['text_s'] = ['-'.join(x) for x in d.tok]
d['tight'] = [is_tight(x, r, lex) for x, r in zip(d.tok, d.r)]
def where(r):
    bits = [r.site]
    for k in ('area-section', 'block-house', 'room-grid'):
        v = r[k]
        if v not in ('--', '-', ''): bits.append(v)
    dep = r['depth']
    if dep not in ('- -', '-', ''): bits.append('depth ' + dep)
    return ', '.join(bits)
rng = np.random.default_rng(11)
def pick(mask, k, seen):
    c = d[mask & d.complete_txt & d.tight & ~d.text_s.isin(seen)].drop_duplicates('text_s')
    c = c[c.cisi != '-']
    c = c.iloc[rng.permutation(len(c))][:k]
    seen.update(c.text_s); return c
seen = set(); groups = []
isseal = d.type.str.startswith('SEAL')
jar = d.r.map(lambda r: bool(r['jars']))
rel = d.r.map(lambda r: r['relation'] or '')
nlen = d.r.map(lambda r: len(r['name']))
groups.append(("Seals of owners: opener? + name + jar", pick(isseal & jar & (rel == '') & (nlen >= 2), 16, seen)))
groups.append(("Seals of servants: name + jar + man", pick(isseal & jar & rel.str.startswith('090'), 12, seen)))
groups.append(("Other things one can be to a master: jar + comb / table-X / barred rectangle / stroke", pick(d.type.str.startswith('SEAL') & jar & rel.isin(['400', '679', '621', '001']), 8, seen)))
nojar = ~jar
groups.append(("Seals with no jar: name + spear / carrier / man / comb", pick(isseal & nojar & d.r.map(lambda r: r['ending_kind'] == 'ending'), 7, seen)))
loadm = d.r.map(lambda r: 'load-count' in r['roles'])
groups.append(("Load tags and counted things", pick(loadm, 5, seen)))
body = []; n = 0
for title, c in groups:
    body.append(f'\n## {title}\n')
    for _, r in c.iterrows():
        n += 1
        body.append(f"{n}. `{r.text_s}`  {r.gloss}  \n   {r.cisi}, {r.type}; {where(r)}.")
# tablet records
body.append('\n## Tablets read as records (one line per face)\n')
recs = []
wanted = ['H-2229', 'H-2238', 'H-2218', 'H-1100', 'H-1102', 'H-1354', 'M-486', 'H-2119', 'H-921', 'H-2246', 'H-2213', 'M-494']
for cs in wanted:
    g = d[d.cisi == cs]
    if len(g) < 2: continue
    recs.append(g)
for g in recs:
    n += 1
    first = g.iloc[0]
    lines = ' | '.join(g.gloss.str.rstrip('.'))
    sign_lines = ' | '.join(g.text_s)
    body.append(f"{n}. `{sign_lines}`  {lines}.  \n   {first.cisi}, {first.type}, {len(g)} faces; {where(first)}.")
print(n)
hdr = """# Glosses

Sixty inscriptions read with the possessive model (`work_scripts/gloss2.py`, sample picked by `work_scripts/gloss2_sample.py`, all texts in `work_data/gloss2_all.csv`).

How to read a line. The sign numbers in backticks are in reading order (left to right as printed here). A name is written in square brackets as crest, self, tag: a crest is the first sign of a family name (a fish-hat sign, a crop sign), a tag is a closing name sign (branching-U, three-headed person). `Of [...]` is a name followed by the jar sign 740, the possessive ending: the seal's owner. `[...]'s man` is the same with the man sign 090 after the jar. `(opening: ...)` is the opener at the head of the text (diamond or wheel plus two strokes, or the 060 cap). A sign written as `(NNN)` has no name yet and is described by its shape. Counts come before the counted thing: "Three porters" is `003 156`. Names are not translated: the crest and tag labels describe the sign pictures, not their meaning.
"""
open('/home/antigravity/Cuuper22/ivc/GLOSSES.md', 'w').write(hdr + '\n'.join(body) + '\n')
