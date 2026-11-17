"""Scan the CDLI texts that mention Meluhha for textile / fibre / tree-product words. Prediction: if the Meluhha trade included cloth or cotton, a cloth word (tug2, gada, siki, ...) appears in the same text more often than in matched random Ur III texts. (Control not run here; this is the listing.)"""
import json, re, collections, csv
OUT='/home/claude/ivc/work_data/abroad2'
rows=[json.loads(l) for l in open(f'{OUT}/cdli_meluhha_atf.jsonl')]
print(len(rows))
per=collections.Counter(); 
for r in rows:
    p=r['period']; per[str(p)[:80]]+=1
print(per.most_common(12))
TEX=re.compile(r'tug2|gada|siki|uš-bar|usz-bar|ku[sš]|gu2|ha-za-nu|ga-ra|ĝeš?|gesz|ugula usz|nig2-lam|ku3-babbar|za3-gin3|na4|uruda|guškin|gusz-kin|sag-?tug|gu-la|bar-dul5|ib2-lah5|tug2-(?:\S+)',re.I)
ML=re.compile(r'me-?l?u?h?-?luh|me-luh|me-lu-uh|me-lu-ha|me-luh-ha',re.I)
out=[]
for r in rows:
    lines=(r['atf'] or '').split('\n')
    ml=[i for i,l in enumerate(lines) if re.search(r'me-l[uú]h?-?(?:uh-)?h[ai]|me-luh',l)]
    for i in ml:
        ctx=lines[max(0,i-3):i+4]
        out.append(dict(id=r['id'],des=r['designation'],period=str(r['period'])[:60],prov=str(r['provenience'])[:60],line=lines[i].strip()[:120],ctx=' // '.join(c.strip() for c in ctx)[:400]))
print(len(out))
with open(f'{OUT}/cdli_meluhha_lines.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
cl=re.compile(r'tug2|gada|siki|usz-bar|uš-bar',re.I)
for o in out:
    if cl.search(o['ctx']): print(o['id'],o['des'],o['period'],'|',o['ctx'][:300])
