#!/usr/bin/env python3
"""861 second try. First word 'Holding' (land holder) went against: land words on the face 8/120 against 6.1% (odd_3c_rescue.py).
PREDICTION for the new word 'tribute / due' (kāṇikkai, DEDR 1444 kāṇi 'present to a superior, due'): away from the front 861 stands beside
transaction words (440 received, 892 sale, 890 given, 176/175 tax) far above the base rate, and it is text-final more than chance."""
from odd_common import *
F = faces(); TR = {'440','892','890','176','175'}
for cat in ('L','Mu','ALL'):
    FL = [f for f in F if cat=='ALL' or f['cat']==cat]
    use = [(f,i) for f in FL for i,a in enumerate(f['x']) if a=='861' and i>0]
    k = sum(((f['x'][i-1] in TR) or (i+1<len(f['x']) and f['x'][i+1] in TR)) for f,i in use)
    base = np.mean([ (f['x'][i-1] in TR) or (i+1<len(f['x']) and f['x'][i+1] in TR) for f in FL for i in range(1,len(f['x']))])
    kf = sum(i==len(f['x'])-1 for f,i in use); bf = np.mean([1/len(f['x']) for f in FL if len(f['x'])>1])
    print(cat, f'861 beside a transaction word {k}/{len(use)} = {k/len(use):.0%} against {base:.1%}, P {pbin(k,len(use),base):.2g}; text-final {kf}/{len(use)} against {bf:.1%}, P {pbin(kf,len(use),bf):.2g}')
