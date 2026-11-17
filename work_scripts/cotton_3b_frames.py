"""PART 3 rescue (new idea): the three tree signs never share an object (0 against 5.7 / 6.2 / 2.6 expected). Prediction if they are three words in ONE slot (a paradigm: chest of cotton / thread / cloth):
they share frames (same left neighbour and same right neighbour in different distinct texts) more than signs of equal frequency do.
Chance: 2000 draws of three random signs matched in distinct-text count (within 25%)."""
from cotton_common import *
import random
f = open(f'{OUTC}/fibre_frames.txt', 'w')
d = faces(); d['txt'] = d.toks.apply('-'.join); dist = d.drop_duplicates('txt')
T = dist.toks.tolist()
fr = collections.defaultdict(set); cnt = collections.Counter()
for t in T:
    for j, x in enumerate(t):
        cnt[x] += 1
        l = t[j-1] if j > 0 else '^'; r = t[j+1] if j + 1 < len(t) else '$'
        fr[x].add((l, r))
        fr[x]; 
def shared(a, b): return len(fr[a] & fr[b])
for a, b in [('390', '405'), ('390', '407'), ('405', '407')]:
    s = shared(a, b)
    random.seed(1)
    pool_a = [x for x in cnt if x not in ('000', 'ALT') and abs(cnt[x] - cnt[a]) <= .25 * cnt[a] and x != a]
    pool_b = [x for x in cnt if x not in ('000', 'ALT') and abs(cnt[x] - cnt[b]) <= .25 * cnt[b] and x != b]
    sims = [shared(random.choice(pool_a), random.choice(pool_b)) for _ in range(2000)]
    p = np.mean([x >= s for x in sims])
    log(f, f'{a} ({cnt[a]} places) & {b} ({cnt[b]}): shared frames {s}; random equal-frequency pairs mean {np.mean(sims):.2f}, P(>= observed) {p:.3f}')
# frames shared with the box slot: left = 590 handled separately (all three follow the box)
log(f, 'shared frames listing 390/405: ' + str(sorted(fr['390'] & fr['405'])[:12]))
log(f, 'shared frames listing 390/407: ' + str(sorted(fr['390'] & fr['407'])[:12]))
log(f, 'shared frames listing 405/407: ' + str(sorted(fr['405'] & fr['407'])[:12]))
f.close()
