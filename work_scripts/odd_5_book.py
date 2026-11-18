#!/usr/bin/env python3
"""Write CORPUS.md (repo root) from work_data/corpus_english2.csv (second reading): key and counts, every WHOLE inscription grouped by site and
object kind (identical texts once, with copies and ids), then the 100 most common PART inscriptions.
Run after corpus_build2.py."""
import pandas as pd, collections
ROOT = '/home/antigravity/Cuuper22/ivc'
c = pd.read_csv(f'{ROOT}/work_data/corpus_english2.csv', dtype=str).fillna('')
G = ['whole', 'part', 'damaged', 'none']
tot = c.grade.value_counts()
site_tab = pd.crosstab(c.site, c.grade).reindex(columns=G, fill_value=0)
site_tab['all faces'] = site_tab.sum(axis=1)
site_tab = site_tab.sort_values('all faces', ascending=False)
L = []
L.append('# The Indus corpus in English\n')
L.append('## Key (read this first)\n')
L.append('- **A seal** is a small stone or clay stamp with a few signs cut in mirror image; **a tablet, tag, pot, rod** and the rest are other objects that carry signs. Each side of an object with signs is one **face**, and this book reads one face at a time (5,679 faces in the Lipi catalogue).')
L.append('- **The template** is the shape most seals follow: [opener] [name] [ending]. The name is a crest (a house sign), a personal part and a tag, in that order; the jar sign ends a name with "house of"; a count comes before the thing it counts; a load tag is "n loads of produce, carried". A program (the template parser) gives every sign one of these slots, and the English is written from the slots by fixed rules (listed at the top of `work_scripts/corpus_build2.py`: slot words, count attachment by stroke style, spelled numbers inside names, one record per multi-face object), so the same signs always give the same English.')
L.append('- **The sounds** are guesses at early Dravidian words, one per sign (`work_data/values_master2.csv`). Where a sign has no value, the English shows its number in square brackets, like [345].')
L.append('- **Grades.** *whole*: every sign has a value we are building on (strict or wide) and nothing is lost. *part*: some signs read, the rest show as [number]. *damaged*: the face has a lost, unclear or broken sign. *none*: no sign has a value.')
L.append('- **Strict and wide**: strict values were promoted on a fact nobody had seen while choosing the word, wide ones also on seen facts. A "whole" line here may use either.')
L.append('- The English is a reading under working guesses, not a translation.\n')
L.append('### Counts\n')
L.append('| grade | faces | share |\n|---|---|---|')
for g in G: L.append(f'| {g} | {int(tot.get(g, 0))} | {tot.get(g, 0) / len(c):.1%} |')
L.append(f'| all | {len(c)} | |\n')
L.append('Per site (faces):\n')
L.append('| site | whole | part | damaged | none | all |\n|---|---|---|---|---|---|')
for s, r in site_tab.iterrows(): L.append(f'| {s} | {r.whole} | {r.part} | {r.damaged} | {r.none} | {r["all faces"]} |')
L.append('')
w = c[c.grade == 'whole']
L.append(f'## Part 1. Every whole inscription ({len(w)} faces, {w.signs.nunique()} different sign strings)\n')
for site in site_tab.index:
    ws = w[w.site == site]
    if not len(ws): continue
    L.append(f'### {site}\n')
    for kind, wk in ws.groupby('object_kind'):
        L.append(f'**{kind}** ({len(wk)} faces)\n')
        grp = collections.OrderedDict()
        for r in wk.itertuples(): grp.setdefault(r.signs, []).append(r)
        for signs, rs in sorted(grp.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            ids = ', '.join(r.face_id for r in rs)
            cp = f'{len(rs)} copies: ' if len(rs) > 1 else ''
            L.append(f'- `{signs}` *{rs[0].sounds}* : {rs[0].english}  ({cp}{ids})')
        L.append('')
p = c[c.grade == 'part']
top = p.groupby('signs').agg(n=('face_id', 'size'), sounds=('sounds', 'first'), english=('english', 'first'), ids=('face_id', lambda s: ', '.join(list(s)[:8]) + (' ...' if len(s) > 8 else ''))).reset_index()
top = top.sort_values(['n', 'signs'], ascending=[False, True]).head(100)
L.append('## Part 2. The 100 most common part-read inscriptions\n')
L.append('| copies | signs | sounds | English | first ids |\n|---|---|---|---|---|')
for r in top.itertuples(): L.append(f'| {r.n} | `{r.signs}` | {r.sounds} | {r.english} | {r.ids} |')
R = pd.read_csv(f'{ROOT}/work_data/odd/object_records.csv', dtype=str).fillna('')
L.append('\n## Part 3. Multi-face objects read as one record (%d objects with 2 or more faces; %d with every face whole)\n' % (len(R), int((R.grade == 'whole').sum())))
L.append('Each object: who (house or person) + what (goods words) + amount. Faces are separated by " / " in the sign column.\n')
for r in R[R.grade == 'whole'].itertuples(): L.append(f'- object {r.object_id} ({r.object_kind}, {r.site}) `{r.signs}` : {r.record}')
open(f'{ROOT}/CORPUS.md', 'w').write('\n'.join(L) + '\n')
print('CORPUS.md written:', len(L), 'lines;', len(w), 'whole faces;', len(top), 'part rows')
