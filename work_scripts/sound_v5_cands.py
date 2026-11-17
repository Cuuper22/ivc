#!/usr/bin/env python3
"""Texts that read start to finish for the first time in the fifth pass (fifth wide list, not fourth wide list),
ranked by copies; marks which read under the fifth strict list.  New texts that newly read are listed too.
Writes work_data/sound_v5/reading_candidates.csv."""
from sound_v5_common import *
from sound_v4_values import TIER4
from sound_v5_values import V5, TIER5, STRICT5
rows = collections.defaultdict(list)
for r in d[d.complete_txt].itertuples():
    if readable(r.tok, TIER5) and not readable(r.tok, TIER4): rows['-'.join(r.tok)].append(r)
out = [dict(text=t, copies=len(rs), strict=readable(tuple(t.split('-')), STRICT5), kinds=dict(collections.Counter(r.kind for r in rs)),
            sites=dict(collections.Counter(r.site for r in rs)), ids=[r.cisi for r in rs][:3], cat='L') for t, rs in rows.items()]
m = M[~M.partnered & M.complete_b]
for r in m.itertuples():
    if readable(r.tok, TIER5) and not readable(r.tok, TIER4):
        out.append(dict(text='-'.join(r.tok), copies=1, strict=readable(r.tok, STRICT5), kinds={r.kind: 1}, sites={r.site_l: 1}, ids=[f'M77 {r.textnum}'], cat='Mu'))
df = pd.DataFrame(out).sort_values(['copies', 'strict'], ascending=False); df.to_csv(f'{OUT5}/reading_candidates.csv', index=False)
print(len(df), 'newly readable texts;', df.strict.sum(), 'strict')
for r in df.head(60).itertuples(): print(r.text, r.copies, r.strict, r.kinds, r.sites, r.ids, ' | ', ' '.join(V5[a][0] if a in V5 else VAL.get(a, '?') if a in VAL else '?' for a in r.text.split('-')))
