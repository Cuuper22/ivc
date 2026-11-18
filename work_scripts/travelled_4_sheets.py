"""Job: the travelled name. Step 4: contact sheets of the photos of 590-390 objects (one primary photo per object, labelled). Output: travelled_out/sheet_N.jpg"""
import pandas as pd, os, re
from PIL import Image, ImageDraw, ImageOps
R='/home/antigravity/Cuuper22/ivc/'
S=R+'evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/'
d=pd.read_csv(R+'work_scripts/travelled_out/t590_390.csv',dtype=str)
files=sorted(os.listdir(S))
items=[]
for r in d.drop_duplicates('object').itertuples():
    if r.cisi=='-': continue
    m=[f for f in files if re.match(re.escape(r.cisi)+r'_[aA](\.|_)',f) or re.match(re.escape(r.cisi)+r'_[aA]_1',f)]
    if not m: m=[f for f in files if re.match(re.escape(r.cisi)+r'_',f)]
    if m: items.append((r.cisi,r.site,r.type,r.reading_order_text,m[0]))
print(len(items),'photos')
W,H=420,330
per=6
for k in range(0,len(items),per):
    chunk=items[k:k+per]
    sheet=Image.new('RGB',(W*3,H*2),'white')
    for i,(c,s,t,txt,f) in enumerate(chunk):
        im=Image.open(S+f).convert('RGB'); im.thumbnail((W-10,H-50)); 
        x,y=(i%3)*W,(i//3)*H
        sheet.paste(im,(x+5,y+45))
        dr=ImageDraw.Draw(sheet); dr.text((x+5,y+4),f'{c} {s} {t}',fill='black'); dr.text((x+5,y+22),txt,fill='darkred')
    sheet.save(R+f'work_scripts/travelled_out/sheet_{k//per+1}.jpg',quality=85)
    print('sheet',k//per+1,[c for c,*_ in chunk])
