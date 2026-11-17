# Number + fish units (Dravidian aru-mīn 'six-star' = Pleiades, er̤u-mīn 'seven-star' = Great Bear; mīn fish = mīṉ star, DEDR 4885/4876).
# Counts in reading order (stored order reversed): which numbers sit right before a fish sign, and where the unit sits.
import csv,re,collections
R=list(csv.DictReader(open('research/data/open_prototype/lipi/metadata_filtered.csv',encoding='utf-8')))
NUM={'001':'S1','002':'S2','003':'S3','004':'S4','005':'S5','006':'S6','007':'S7','012':'T2','013':'T3','014':'T4','015':'T5','016':'T6','017':'T7','018':'T8','031':'F1','032':'F2','033':'F3','034':'F4','035':'F5','036':'F6'}
VAL={k:int(v[1:]) for k,v in NUM.items()}
FISH={'220':'plain fish','235':'fish+caret hat','240':'fish+whiskers','233':'fish+line','231':'fish+stroke','226':'fish+4 strokes round','236':'fish 236'}
c=collections.Counter(); whole=collections.Counter(); pos=collections.Counter(); ex=collections.defaultdict(list)
for x in R:
    t=re.findall(r'\d{3}',x['text'])[::-1]
    for i in range(len(t)-1):
        if t[i] in NUM and t[i+1] in FISH:
            k=(NUM[t[i]],FISH[t[i+1]]); c[k]+=1
            p='alone' if len(t)==2 else ('start' if i==0 else ('end' if i+1==len(t)-1 else 'middle'))
            pos[(VAL[t[i]],p)]+=1
            if len(ex[VAL[t[i]]])<4: ex[VAL[t[i]]].append(f"{x['cisi']} {'-'.join(t)}")
by=collections.Counter()
for (n,f),v in c.items(): by[int(n[1:])]+=v
print('number right before a fish sign, by value:',sorted(by.items()))
print('by stroke style and fish:'); [print('  ',k,v) for k,v in c.most_common(20)]
print('position of number+fish unit in text:',sorted(pos.items()))
for n in (3,6,7): print(n,'examples:',ex[n])
