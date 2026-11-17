#!/usr/bin/env python3
"""Split step 4: plain description of the three-profile groups on copy events (one row per object, batches once)."""
from split_common import *
for s in ['001', '850']:
    R = pd.read_csv(f'{SPL}/contexts_{s}.csv')
    print(f'== {s}: {len(R)} copy-event rows')
    for g in sorted(R.group3.unique()):
        G = R[R.group3 == g]
        print(f' group3 {g}: n {len(G)}; start {(G.pos==0).mean():.2f} end {(G.pos_from_end==0).mean():.2f}; len median {G.length.median():.0f}; kinds {G.kind.value_counts().head(3).to_dict()}; sites {G.site.value_counts().head(3).to_dict()}; left {G.left.value_counts().head(4).to_dict()}; right {G.right.value_counts().head(4).to_dict()}')
R = pd.read_csv(f'{SPL}/contexts_824.csv'); print('824 by group x site x kind'); print(R.groupby(['group', 'site', 'kind']).size())
