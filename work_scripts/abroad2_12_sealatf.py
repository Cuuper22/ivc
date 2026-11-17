"""Item 1 continued: read the seal blocks in the ATF of every candidate. Prediction: the legends are Ur III cuneiform (owner, 'dumu', 'ARAD2 of ...'); non-cuneiform (uninscribed, pictorial) seals are noted in CDLI as '$ seal impression ... ' or '@seal' with a '$' comment."""
import json, re, csv
OUT='/home/claude/ivc/work_data/abroad2'
A={a['id']:a for a in json.load(open(f'{OUT}/cdli_meluhha_guabba_full.json'))}
rows=list(csv.DictReader(open(f'{OUT}/sealed_candidates_all.csv')))
res=[]
for r in rows:
    a=A[int(r['id'][1:])]; atf=a['inscription']['atf']
    lines=atf.split('\n')
    blocks=[]
    for i,l in enumerate(lines):
        if re.match(r'\s*@seal',l):
            blocks.append(' ; '.join(x.strip() for x in lines[i:i+6] if not x.startswith('@obverse')))
        elif re.search(r'\$.*(seal|impression|uninscribed|illegible)',l,re.I):
            blocks.append(l.strip())
    if blocks:
        res.append((r,blocks))
print(len(res),'candidates with seal blocks')
txt=[x for x in res if x[0]['mel']=='True' or x[0]['wool']=='True']
print(len(txt),'of them Meluhha or textile-word texts')
with open(f'{OUT}/sealed_blocks.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','des','period','date','mel','wool','blocks','first'])
    for r,b in res: w.writerow([r['id'],r['des'],r['period'],r['date'],r['mel'],r['wool'],' || '.join(b)[:400],r['first']])
for r,b in txt[:60]:
    print(r['id'],r['des'][:22],r['period'][:8],'MEL' if r['mel']=='True' else '   ','TEX' if r['wool']=='True' else '   ','|',' || '.join(b)[:220])
