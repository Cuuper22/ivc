# usage: carrier_crop.py out.png scale file:fx0,fy0,fx1,fy1 ...  (fractions of image)
import sys
from PIL import Image,ImageDraw
D='/home/claude/ivc/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/'
out,s=sys.argv[1],float(sys.argv[2]);cr=[]
for a in sys.argv[3:]:
    f,b=a.split(':');x0,y0,x1,y1=map(float,b.split(','))
    i=Image.open(D+f+'.jpg').convert('RGB');w,h=i.size
    c=i.crop((int(x0*w),int(y0*h),int(x1*w),int(y1*h)));c=c.resize((int(c.width*s),int(c.height*s)),Image.LANCZOS)
    cr.append((f,c))
W=sum(c.width+10 for _,c in cr[:3]);rows=[cr[k:k+3] for k in range(0,len(cr),3)]
H=sum(max(c.height for _,c in r)+18 for r in rows)
S=Image.new('RGB',(max(sum(c.width+10 for _,c in r) for r in rows),H),'white');d=ImageDraw.Draw(S);y=0
for r in rows:
    x=0
    for f,c in r:
        S.paste(c,(x,y+16));d.text((x+2,y+2),f,fill='red');x+=c.width+10
    y+=max(c.height for _,c in r)+18
S.save(out)
