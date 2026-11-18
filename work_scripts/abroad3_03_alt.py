"""Alternative reading of the tall strokes after 705 in the photograph: 033 (three full-height strokes) or 032 (two full-height) instead of 002.
Prediction first: home texts show 705 033 004 390 or 033 004 390 at least as often as 705 002 004 390 (0 times)."""
import sys
sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from cotton_common import *
d=faces(); d=d[d.id!='3884.1']
def find(seq):
    s=' '.join(seq); return [(r.id,r.site,r.symbol,' '.join(r.toks)) for _,r in d.iterrows() if s in ' '.join(r.toks)]
for seq in (['705','033','004','390'],['033','004','390'],['705','032','004','390'],['032','004','390'],['705','002','004'],['705','033','004'],['705','033','002'],['033','004'],['032','004'],['705','004','390'],['705','390']):
    f=find(seq); print(' '.join(seq),len(f),f[:6])
