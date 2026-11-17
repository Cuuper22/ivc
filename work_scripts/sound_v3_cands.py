#!/usr/bin/env python3
"""List goods-object texts (tags, pots, tools, bangles, rods, copper and miniature tablets) that become fully
sounded under the third list and use at least one value that moved up or got its word in this pass.
Writes work_data/sound_v3/reading_candidates.csv."""
import re, collections
from sound_v3_common import *
from sound_v3_values import V3, TIER3, OLDTIER
OK = lambda s, allow: s in VAL or TIER3.get(s) in allow
UNLOCK = {s for s in TIER3 if TIER3[s] == 'building' and OLDTIER.get(s) != 'building'} | {'500'}
old = set(re.findall(r'Signs: `([0-9-]+)`', open(f'{ROOT}/READINGS.md').read()))
if __name__ == '__main__':
    out = []
    for allow, tag in [(('base', 'building'), 'built'), (('base', 'building', 'testing'), 'with testing')]:
        g = collections.defaultdict(list)
        for r in d[d.kind != 'seal'].itertuples():
            x = r.tok
            if not r.complete_txt or len(x) < 2 or '000' in x or 'ALT' in x: continue
            if not all(OK(a, allow) for a in x) or not (set(x) & UNLOCK): continue
            if '-'.join(x) in old: continue
            g[x].append(r)
        for x, rs in g.items():
            out.append(dict(level=tag, text='-'.join(x), n=len(rs), kinds='/'.join(sorted({r.kind for r in rs})), sites='/'.join(sorted({r.site for r in rs})),
                            ex=rs[0].cisi, area=rs[0]._5, mat=rs[0].material, words=' '.join(f'{a}:{V3[a][0] if a in V3 else VAL.get(a)}' for a in x)))
    df = pd.DataFrame(out).drop_duplicates('text').sort_values(['level', 'n'], ascending=[True, False])
    df.to_csv(f'{OUT3}/reading_candidates.csv', index=False)
    print(df.level.value_counts().to_dict())
    pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90)
    print(df.head(70).to_string(index=False))
