"""Do Sumerian words for cloth/thread/wool/spindle line up with Dravidian words for the same things better than chance?
Prediction written first: if Sumerian cloth words took any Dravidian words (or the reverse), matching word-skeletons (first consonant class + second consonant class) will be above the shuffle null. I expect a weak or null result: the only strong-looking pair is tug / tuṇi.
Method: pick words by gloss keyword only (no hand picking). Sumerian: sumerian_wiktionary.tsv + sumerian_halloran.tsv headwords whose gloss has a textile keyword. Dravidian: DEDR entries whose first Tamil gloss has a textile keyword (headword = first Tamil form). Skeleton: C1 class + C2 class (None if no 2nd consonant). Match = C1 equal and (C2 equal or one has none). Null: same number of random words from each full lexicon, 20000 draws."""
import re, random, unicodedata, collections
random.seed(1)
L='/home/claude/ivc/work_data/lexicons'
KW=re.compile(r'\b(cloth|garment|thread|yarn|wool|flax|linen|spindle|weav|warp|spin|textile|cotton|rope|string)',re.I)
def nrm(s):
    s=unicodedata.normalize('NFD',s.lower())
    s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    s=s.replace('ĝ','g').replace('š','s').replace('ṭ','t').replace('ḍ','d').replace('ṇ','n').replace('ḷ','l').replace('ṟ','r').replace('ḻ','l').replace('ṅ','n').replace('ñ','n').replace('ś','s').replace('ṣ','s')
    return re.sub(r'[^a-z]','',s)
CL={'k':'K','g':'K','c':'K','q':'K','t':'T','d':'T','p':'P','b':'P','v':'P','f':'P','s':'S','z':'S','j':'S','h':'H','n':'N','m':'M','l':'L','r':'R','y':'Y','w':'P'}
def skel(w):
    w=nrm(w)
    cons=[CL[c] for c in w if c in CL]
    return (cons[0] if cons else None, cons[1] if len(cons)>1 else None)
def match(a,b):
    if a[0] is None or b[0] is None or a[0]!=b[0]: return False
    return a[1] is None or b[1] is None or a[1]==b[1]
# Sumerian
sum_all={}
for f in ['sumerian_wiktionary.tsv','sumerian_halloran.tsv']:
    for l in open(f'{L}/tsv/{f}'):
        p=l.rstrip('\n').split('\t')
        if len(p)<2: continue
        h=nrm(p[0]); 
        if 2<=len(h)<=6: sum_all.setdefault(h,[]).append(p[1])
sum_tex={h:g for h,g in sum_all.items() if any(KW.search(x[:90]) for x in g)}
# Dravidian
dr_all={}; dr_tex={}
for l in open(f'{L}/dedr/dedr_entries.tsv'):
    n,t=l.rstrip('\n').split('\t',1)
    m=re.match(r'Ta\. ([^\s,;()]+)(.*)',t)
    if not m: continue
    h=nrm(m.group(1))
    if len(h)<2: continue
    gl=t[:160]
    dr_all[h]=(n,gl)
    if KW.search(gl[len(m.group(1)):]): dr_tex[h]=(n,gl)
print('Sumerian textile words',len(sum_tex),'of',len(sum_all),'; Dravidian textile words',len(dr_tex),'of',len(dr_all))
pairs=[(s,d) for s in sum_tex for d in dr_tex if match(skel(s),skel(d))]
# count by Sumerian word having any Dravidian partner
S_hit=len({s for s,d in pairs}); D_hit=len({d for s,d in pairs})
print('observed pairs',len(pairs),'; Sumerian words with a partner',S_hit,'; Dravidian words with a partner',D_hit)
sa=list(sum_all); da=list(dr_all)
ns,nd=len(sum_tex),len(dr_tex)
sk_s={s:skel(s) for s in sa}; sk_d={d:skel(d) for d in da}
ge=0; vals=[]
N=20000
for _ in range(N):
    S=random.sample(sa,ns); D=random.sample(da,nd)
    c=sum(1 for s in S for d in D if match(sk_s[s],sk_d[d]))
    vals.append(c); ge+= c>=len(pairs)
print('null mean pairs',round(sum(vals)/N,1),'; draws >= observed',ge,'of',N)
# show the tightest ones: exact C1 C2 equal and both have 2 consonants, short words
print('Pairs with full two-consonant agreement, first 40:')
c=0
for s,d in sorted(pairs):
    a,b=skel(s),skel(d)
    if a==b and a[1] is not None:
        c+=1
        if c<=40: print(' ',s,sum_tex[s][0][:40],'|',d,dr_tex[d][0],dr_tex[d][1][:60])
print('n full-skeleton pairs',c)
