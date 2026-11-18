"""Composite beasts and goats and the marked-fish houses: second test, a different way. Count marked fish (231,233,235,240) ANYWHERE in the text on composite+goat seals (67) against the rate on all other animal seals at the same sites.
PREDICTION written before numbers: composite+goat seals carry marked fish at less than half the rate of the rest (<9%)."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from animal_common import *
from scipy.stats import binomtest, fisher_exact
FISH={'231','233','235','240'}
d=b[(b.g!='')&(b.g!='NONE')].copy(); d['fish']=d.reading_order_text.map(lambda t:any(x in FISH for x in t.split('-')))
cg=d[d.g.isin(['COMP','GOAT'])]; rest=d[~d.g.isin(['COMP','GOAT'])&d.site.isin(cg.site.unique())]
rate=rest.fish.mean(); print('composite+goat seals',len(cg),'with marked fish',cg.fish.sum(),'| rest at same sites',len(rest),f'rate {rate:.3f}')
print('binomial P(<= observed):',binomtest(int(cg.fish.sum()),len(cg),rate,alternative='less').pvalue)
# does it hold with a fish-free baseline of the same text length? fish is on longer texts, so compare texts of 3+ signs only
c3=cg[cg.reading_order_text.str.count('-')>=2]; r3=rest[rest.reading_order_text.str.count('-')>=2]
print('texts of 3+ signs: composite+goat',len(c3),'with fish',c3.fish.sum(),f'| rest {len(r3)} rate {r3.fish.mean():.3f}','P',binomtest(int(c3.fish.sum()),len(c3),r3.fish.mean(),alternative='less').pvalue)
print(cg[['cisi','site','symbol','reading_order_text']].assign(fish=cg.fish).head(70).to_string(index=False)[:0])
