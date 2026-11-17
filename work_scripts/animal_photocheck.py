"""Draw 30 seals for the photo check of the catalogue animal column (stratified by label, fixed seed) and make 3 sheets of 10.
The labels are hidden on the sheets (only a number), so the look is made before the label is seen; the key is printed after."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
import pandas as pd, os, re, random
from PIL import Image, ImageDraw
from animal_sheet import R,pick,pre
b=pd.read_csv('/home/claude/ivc/work_data/animal/animal_base.csv',dtype=str,keep_default_na=False)
b=b[(b.cisi!='-')&b.cisi.isin(pre)]
plan=[('UNICORN',5),('SHORTHORN',3),('ZEBU',3),('ELEPHANT',3),('RHINO',2),('TIGER',2),('BUFFALO',2),('GOAT',2),('COMPOSITE',2),('NONE',3),('BULL_OTHER',2),('UNKNOWN',1)]
random.seed(20261117); pick30=[]
for a,n in plan:
    ids=list(b[b.animal==a].index); random.shuffle(ids)
    for i in ids[:n]: pick30.append(i)
random.shuffle(pick30); S=b.loc[pick30]
S=S.reset_index(drop=True); S['no']=range(1,len(S)+1)
S[['no','id','cisi','site','symbol','animal','stand','reading_order_text']].to_csv('/home/claude/ivc/work_data/animal/photocheck_key.csv',index=False)
W=330
for sh in range(3):
    im=Image.new('RGB',(5*W,2*(W+16)),'white'); d=ImageDraw.Draw(im)
    for k in range(10):
        r=S.iloc[sh*10+k]; f=pick(r.cisi)
        x=Image.open(f'{R}/{f}').convert('RGB'); x.thumbnail((W-6,W-6))
        im.paste(x,((k%5)*W,(k//5)*(W+16))); d.text(((k%5)*W+2,(k//5)*(W+16)+W),f'#{r.no}  {r.cisi}',fill='red')
    im.save(f'/home/claude/ivc/work_scripts/animal_out/photocheck_{sh+1}.png')
