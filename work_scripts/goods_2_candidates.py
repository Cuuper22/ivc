"""Goods job step 2: pick candidate goods/unit signs by the brief's tests and write goods_out/candidates.csv plus picture sheets.
Tests (a sign enters if any holds): on goods tags, pots, tools/bangles/rods, at the port or bead towns, in the granary area, on copper tablets,
takes counts, stands alone as a whole text, follows a count and precedes a carrier."""
from goods_common import *
from PIL import Image, ImageDraw
W=pd.read_csv(f'{OUT}/sign_world.csv',dtype={'sign':str})
sh=pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv',dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
cw=pd.read_csv(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv',dtype=str); cw=cw[cw.rank_for_lipi_sign=='1'].set_index('lipi').mahadevan.to_dict()
def hit(r):
    why=[]
    if r.tag_n>=4 and r.tag_p<1e-3: why.append('tag')
    if r.pot_n>=4 and r.pot_p<1e-2: why.append('pot')
    if r.tool_n>=3 and r.tool_p<2e-3: why.append('tool/bangle/rod')
    if r.lothal_n>=4 and r.lothal_p<1e-3: why.append('Lothal')
    if r.chanhu_n>=4 and r.chanhu_p<1e-2: why.append('Chanhu-daro')
    if r.dhola_n>=4 and r.dhola_p<1e-2: why.append('Dholavira')
    if r.gran_n>=5 and r.gran_p<1e-4: why.append('granary')
    if r.copper_n>=8 and r.copper_p<1e-8: why.append('copper tablet')
    if r.ivory_n>=3 and r.ivory_p<1e-3: why.append('ivory/bone rod')
    if r.cnt_before+r.cnt_after>=12 and (r.cnt_before+r.cnt_after)/r.faces>=0.12: why.append('counted')
    if r.alone>=6 and r.alone/r.faces>=0.12: why.append('whole text')
    if r.cnt_s_carr>=3: why.append('count-X-carrier')
    return '; '.join(why)
W['why']=W.apply(hit,axis=1)
C=W[W.why!=''].copy()
C['mahadevan']=C.sign.map(cw); C['shape']=C.sign.map(sh)
C.to_csv(f'{OUT}/candidates.csv',index=False)
print(len(C),'candidate goods signs of',len(W))
# picture sheets, 24 per sheet
T=150; per=20
cs=C.sort_values('faces',ascending=False).reset_index(drop=True)
for k in range((len(cs)+per-1)//per):
    sub=cs.iloc[k*per:(k+1)*per]
    im=Image.new('RGB',(5*T,4*(T+34)),'white'); dr=ImageDraw.Draw(im)
    for j,(_,r) in enumerate(sub.iterrows()):
        x,y=(j%5)*T,(j//5)*(T+34)
        try:
            g=Image.open(f'{ROOT}/work_data/mahadevan_glyphs/{r.mahadevan}.png').convert('RGBA').resize((T-14,T-14))
            bg=Image.new('RGBA',g.size,'white'); bg.alpha_composite(g); im.paste(bg.convert('RGB'),(x+7,y+3))
        except Exception: pass
        dr.text((x+4,y+T-8),f"L{r.sign} M{r.mahadevan} n{r.faces}",fill='black')
        dr.text((x+4,y+T+4),r.why[:30],fill='darkblue'); dr.text((x+4,y+T+16),str(r['shape'])[:30],fill='darkred')
        dr.rectangle([x,y,x+T-1,y+T+33],outline='grey')
    im.save(f'{OUT}/cand_sheet_{k+1}.png')
print('sheets',(len(cs)+per-1)//per)
pd.set_option('display.width',250); pd.set_option('display.max_rows',300); pd.set_option('display.max_colwidth',60)
print(cs[['sign','mahadevan','faces','why','shape']].to_string())
