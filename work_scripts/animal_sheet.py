# Make contact sheets of seal photos for a list of animal labels (to read what each catalogue label looks like).
import pandas as pd, os, re, sys, random
from PIL import Image, ImageDraw
R='/home/claude/ivc/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'
M=pd.read_csv('/home/claude/ivc/research/data/open_prototype/lipi/metadata_filtered.csv',dtype=str,keep_default_na=False)
fs=os.listdir(R); pre={}
for f in fs: pre.setdefault(f.split('_')[0],[]).append(f)
def pick(c):
    L=sorted(pre.get(c,[]))
    for f in L:
        if re.match(r'^[^_]+_[aA]\.',f) or re.match(r'^[^_]+_[aA]_',f): return f
    return L[0] if L else None
def sheet(labels,out,per=6,seed=3,W=170):
    random.seed(seed); rows=[]
    s=M[M.type.str.startswith('SEAL')]
    for lab in labels:
        sub=s[(s.symbol==lab)&(s.cisi!='-')&s.cisi.isin(pre)]
        ids=list(sub.index); random.shuffle(ids); rows.append((lab,[ (sub.loc[i,'cisi'],pick(sub.loc[i,'cisi'])) for i in ids[:per]],len(sub)))
    H=W+18
    im=Image.new('RGB',(per*W+90,H*len(rows)),'white'); d=ImageDraw.Draw(im)
    for r,(lab,items,n) in enumerate(rows):
        d.text((2,r*H+W//2),f'{lab}\nn={n}',fill='black')
        for c,(ci,f) in enumerate(items):
            try:
                x=Image.open(f'{R}/{f}').convert('RGB'); x.thumbnail((W-4,W-4)); im.paste(x,(90+c*W,r*H))
                d.text((90+c*W,r*H+W),ci,fill='red')
            except Exception as e: pass
    im.save(out)
if __name__=='__main__':
    sheet(sys.argv[2].split(','),sys.argv[1])
