"""Gloss 30 real texts sign by sign using the commodity lexicon. Writes work_data/counted/gloss30.md (draft lines)."""
import sys; sys.path.insert(0,'/home/claude/ivc/work_scripts')
from counted_common import *
LEX={'000':'<lost>','861':'OPENER-diamond','817':'OPENER-diamond','820':'OPENER-wheel','740':'jar','741':'jar-dot','400':'comb','090':'man','091':'two-men','097':'man-bracketed',
'806':'crop','154':'carried','158':'carried','155':'carried','156':'porter-load','151':'porter','700':'cup-measure','220':'fish','235':'fish-hat','240':'fish-whisker','233':'fish-line','231':'fish-dot','226':'fish-caged','236':'fish-hat-caged',
'520':'spear','390':'tree-A','405':'tree-B','407':'tree-C','585':'box-585','590':'bar-box','845':'hatched-leaves','923':'paren-outline','705':'U-staff','706':'U-staff2','140':'woman','142':'staff-man','130':'fork-man','125':'archer','100':'three-head-man','176':'sitting-man',
'415':'pitchfork','061':'lambda','900':'paren','840':'two-leaves','803':'leaf-803','798':'leaf-pincer','760':'branch-U','060':'060','048':'seven-in-parens','055':'four-rows','575':'trapezoid-box','550':'pincer','384':'heart','904':'nested-paren','920':'paren-leaf','692':'692'}
CN={'S':'{}','F':'{}f','T':'{}t'}
def cname(tok):
    s,v=CNT[tok]
    return 'A-comb' if s=='A' else {'S':str(v),'F':f'{v}(tall)','T':f'{v}(stacked)'}[s]
res=pd.read_csv(f'{ROOT}/work_data/counted/instances_resolved.csv',dtype=str,keep_default_na=False)
own={(r.id,int(r.pos),r.frame) for r in res.itertuples()}
def gloss(r,toks):
    out=[];i=0
    while i<len(toks):
        t=toks[i]
        if t in CNT and i>=1 and toks[i-1] in('705','706') and t=='033':
            out[-1]=f"[{LEX[toks[i-1]]} x 3(tall)]"; i+=1; continue
        if t in CNT:
            # count owned by right neighbour?
            if (r['id'],i+1,'B') in own and i+1<len(toks):
                out.append(f"[{cname(t)} x {LEX.get(toks[i+1],'<'+toks[i+1]+'>')}]"); i+=2; continue
            out.append(f"#{cname(t)}"); i+=1; continue
        # left-owned count after it
        if i+1<len(toks) and toks[i+1] in CNT and (r['id'],i,'A') in own:
            out.append(f"[{LEX.get(t,'<'+t+'>')} x {cname(toks[i+1])}]"); i+=2; continue
        out.append(LEX.get(t,'<'+t+'>')); i+=1
    return ' '.join(out)
if __name__=='__main__':
    rows=load(); pick=sys.argv[1:]
    for r,t,b in rows:
        if r['id'] in pick: print(r['id'],r['cisi'],r['site'],r['type'],r['material'],'|',' '.join(t),'|',gloss(r,t))
