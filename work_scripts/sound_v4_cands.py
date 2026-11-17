#!/usr/bin/env python3
"""Texts that became readable start to finish in the fourth pass (readable under the fourth list, not under the third),
ranked by copies; marks which read under the strict list too.  Also the share of new texts (second catalogue,
no Lipi partner) that read whole before and after.  Writes work_data/sound_v4/reading_candidates.csv."""
from sound_v4_common import *
from sound_v4_values import V4, TIER4, STRICT4
sub = d[d.complete_txt]
rows = collections.defaultdict(list)
for r in sub.itertuples():
    x = r.tok
    if readable(x, TIER4) and not readable(x, TIER3): rows['-'.join(x)].append(r)
out = []
for t, rs in rows.items():
    out.append(dict(text=t, copies=len(rs), strict=readable(tuple(t.split('-')), STRICT4), kinds=dict(collections.Counter(r.kind for r in rs)),
                    sites=dict(collections.Counter(r.site for r in rs)), new=[a for a in t.split('-') if TIER3.get(a) != 'building' and a not in VAL and TIER3.get(a) != 'base'],
                    ids=[r.cisi for r in rs][:3]))
df = pd.DataFrame(out).sort_values(['copies', 'strict'], ascending=False); df.to_csv(f'{OUT4}/reading_candidates.csv', index=False)
print(len(df), 'newly readable distinct texts;', df.strict.sum(), 'under the strict list')
print(df.head(70).to_string(max_colwidth=50))
m = M[~M.partnered & M.complete_b]
for nm, T in [('third', TIER3), ('fourth strict', STRICT4), ('fourth wide', TIER4)]:
    h = m.tok.apply(lambda x: readable(x, T))
    print(f'new texts read whole under the {nm} list: {h.sum()} of {len(m)} complete new texts; seals {h[m.kind == "seal"].sum()} of {(m.kind == "seal").sum()}, goods {h[m.kind != "seal"].sum()} of {(m.kind != "seal").sum()}')
