import sys,os
from PIL import Image,ImageDraw
D='/home/antigravity/Cuuper22/ivc/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/'
O='/tmp/carrier_sheets/';os.makedirs(O,exist_ok=True)
objs=sys.argv[1:]
files=[]
for o in objs:
    fs=sorted(f for f in os.listdir(D) if f.startswith(o+'_'))
    files+=fs
def sheet(fl,name):
    ims=[Image.open(D+f).convert('RGB') for f in fl]
    ims=[i.resize((int(i.width*min(2.5,520/max(i.size))),int(i.height*min(2.5,520/max(i.size))))) if max(i.size)<520 else i for i in ims]
    W=sum(i.width for i in ims[:3])+40;rows=[ims[k:k+3] for k in range(0,len(ims),3)]
    H=sum(max(i.height for i in r)+20 for r in rows)
    S=Image.new('RGB',(max(sum(i.width+10 for i in r) for r in rows),H),'white');d=ImageDraw.Draw(S);y=0;k=0
    for r in rows:
        x=0
        for i in r:
            S.paste(i,(x,y+16));d.text((x+2,y+2),fl[k],fill='red');x+=i.width+10;k+=1
        y+=max(i.height for i in r)+20
    S.save(O+name)
for n in range(0,len(files),6):
    sheet(files[n:n+6],f'{sys.argv[1]}_{n//6}.png')
print(files)
