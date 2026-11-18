#!/usr/bin/env python3
"""Do marked fish get written out as [mark sign] + plain fish 220? For each single sign, among the frames where it is
swapped for two signs (spell2.csv), the share whose second sign is the plain fish 220."""
import pandas as pd, collections
from scipy.stats import fisher_exact
sp = pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/sound/spell2.csv', dtype=str)
sp['frames'] = sp.frames.astype(int); sp['second'] = sp.two.str.split('-').str[1]
g = sp.groupby('one').apply(lambda t: pd.Series(dict(frames=t.frames.sum(), fish_end=t[t.second == '220'].frames.sum())))
fish = ['233', '235', '240', '231', '226', '236']
F = g.loc[[f for f in fish if f in g.index]]; O = g.drop([f for f in fish if f in g.index]); O = O[~O.index.isin(['220'])]
print(F); print('marked fish: %d of %d swaps end in 220; other single signs: %d of %d' % (F.fish_end.sum(), F.frames.sum(), O.fish_end.sum(), O.frames.sum()))
print('P (one-sided Fisher):', fisher_exact([[F.fish_end.sum(), F.frames.sum() - F.fish_end.sum()], [O.fish_end.sum(), O.frames.sum() - O.fish_end.sum()]], alternative='greater')[1])
print(sp[(sp.one.isin(fish)) & (sp.second == '220')][['one', 'two', 'frames', 'examples']].to_string())
