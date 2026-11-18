# Read real seal texts aloud with the first Dravidian sound values (guesses built in language_candidates.md).
# Reading order = stored order reversed. Picks complete seal texts whose signs all have a value (openers allowed),
# prints cisi id, signs, sound string and gloss. Run from /home/antigravity/Cuuper22/ivc.
import csv,re,collections
R=list(csv.DictReader(open('research/data/open_prototype/lipi/metadata_filtered.csv',encoding='utf-8')))
V={ # sign: (sound, gloss)
 '740':('-kuṭi','house of / of'), '090':('āḷ','man, manager'), '400':('ciṟ','junior'), '520':('vēḷ','chief'),
 '142':('kō','king, great man'), '154':('kā','keeper'),'156':('kā','keeper'),'158':('kā','keeper'),'151':('kā','keeper'),
 '220':('mīn','star'), '390':('maṟam','warrior'), '100':('mū(tu)','elder'),
 '235':('mīn₂₃₅','star-crest A'),'240':('mīn₂₄₀','star-crest B'),'233':('mīn₂₃₃','star-crest C'),'231':('mīn₂₃₁','star-crest D'),
 '001':('oru','one'),'002':('iru','two'),'003':('mū','three'),'004':('nāl','four'),'005':('ai','five'),'016':('aṟu','six'),'017':('er̤u','seven'),
 '012':('iru','two'),'013':('mū','three'),'014':('nāl','four'),'031':('oru','one'),'032':('iru','two'),'033':('mū','three'),'034':('nāl','four'),
 '861':('[opener]',''),'817':('[opener]',''),'820':('[opener]',''),
}
OPEN={'861','817','820'}
seen=set(); out=[]
for x in R:
    if not x['type'].startswith('SEAL') or x['complete']!='Y': continue
    t=re.findall(r'\d{3}',x['text'])[::-1]
    if len(t)<2 or any(s not in V for s in t): continue
    if sum(s not in OPEN and not re.match(r'0[0-3]\d',s) for s in t)<2: continue
    key='-'.join(t)
    if key in seen: continue
    seen.add(key)
    snd=' '.join(V[s][0] for s in t).replace(' -','-')
    gl=' | '.join(f"{s}={V[s][1]}" for s in t if V[s][1])
    out.append((x['site'],x['cisi'],key,snd,gl))
print(len(out),'distinct complete seal texts read wholly with the value list')
bysite=collections.defaultdict(list)
for o in out: bysite[o[0]].append(o)
for s,L in sorted(bysite.items(),key=lambda z:-len(z[1])):
    for o in L: print(f"{o[1]:8s} {o[0]:12s} {o[2]:24s} {o[3]:34s} {o[4]}")
