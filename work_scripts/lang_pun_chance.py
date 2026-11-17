# How cheap is a Dravidian pun? For every Tamil headword in DEDR, look for ANOTHER entry whose Tamil headword shares
# the first 3 letters and whose gloss holds a "job" meaning (king, chief, rule, house, family, star, small, young,
# guard, elder, old, warrior, rise, servant). Compare the rate for the 9 picture words we used against all headwords.
import re, random, unicodedata, collections
random.seed(3)
JOB = re.compile(r"\b(king|chief|lord|rule|rules|ruler|house|household|family|lineage|star|small|young|younger|guard|protect|elder|aged|old|warrior|valour|rise|servant|master)\b")
heads = {}
for line in open('/tmp/dedr/dedr_text.txt'):
    m = re.match(r"^(\d+[a-z]?) Ta\. ([^\s,;(]+)\s+([^.]*)", unicodedata.normalize('NFC', line))
    if m and len(m.group(2)) >= 2 and m.group(3): heads.setdefault(m.group(1), (m.group(2), m.group(3)))
heads['399'] = ('āḷ', 'man, servant'); heads['4711'] = ('maram', 'tree')
items = list(heads.items())
by3 = collections.defaultdict(list)
import sys
L = int(sys.argv[1]) if len(sys.argv) > 1 else 3
def key(w):  # first L letters with vowel length and r/ṟ, l/ḷ, n/ṉ/ṇ merged (near-homophones)
    w = unicodedata.normalize('NFD', w); w = ''.join(c for c in w if not unicodedata.combining(c))
    return w[:L]
for k, (w, g) in items: by3[key(w)].append((k, w, g))
def has_pun(k, w):
    return any(JOB.search(g) for k2, w2, g in by3[key(w)] if k2 != k)
rate = sum(has_pun(k, w) for k, (w, g) in items) / len(items)
OURS = {'1651': 'kuṭam', '399': 'āḷ', '4885': 'mīṉ', '910': 'ēr̤u', '1610': 'cīppu', '5536': 'vēl', '2237': 'kōl', '1417': 'kā', '4711': 'maram'}
hits = {w: has_pun(k, w) for k, w in OURS.items()}
print(f"Tamil headwords: {len(items)}; share with a 3-letter look-alike carrying a job meaning: {rate:.3f}")
print("our picture words:", hits, f"-> {sum(hits.values())}/{len(hits)}")
from math import comb
n, x = len(hits), sum(hits.values())
p = sum(comb(n, i) * rate**i * (1-rate)**(n-i) for i in range(x, n+1))
print(f"P(at least {x} of {n} by chance at that rate) = {p:.4f}")

# Slot-specific version: the look-alike must carry the meaning the SLOT needs, not any job meaning.
SPEC = {'1651': r"\b(house|household|family|lineage|clan)\b", '399': r"\b(rule|rules|ruler|manage|master)\b",
        '4885': r"\bstars?\b", '910': r"\b(rise|ascend)\b", '1610': r"\b(small|young|younger|junior)\b",
        '5536': r"\b(chief|king|ruler|lord)\b", '2237': r"\b(king|chief|lord|emperor)\b",
        '1417': r"\b(guard|protect|protection|keep)\b", '4711': r"\b(warrior|valour|bravery)\b"}
print("\nslot-specific: share of all Tamil headwords that have a look-alike with the meaning this slot needs")
exp = 0; got = 0
for k, rx in SPEC.items():
    R2 = re.compile(rx); w = heads[k][0]
    base = sum(any(R2.search(g) for k2, w2, g in by3[key(ww)] if k2 != kk) for kk, (ww, gg) in items) / len(items)
    hit = any(R2.search(g) for k2, w2, g in by3[key(w)] if k2 != k)
    exp += base; got += hit
    print(f"  {w:8s} needs /{rx}/  chance {base:.3f}  ours {'yes' if hit else 'no'}")
print(f"  expected look-alike hits by chance {exp:.2f} of {len(SPEC)}; ours {got}")
# exact chance of at least this many hits (Poisson-binomial over the per-slot chances)
ps = []
for k, rx in SPEC.items():
    R2 = re.compile(rx)
    ps.append(sum(any(R2.search(g) for k2, w2, g in by3[key(ww)] if k2 != kk) for kk, (ww, gg) in items) / len(items))
dist = [1.0]
for p_ in ps:
    nd = [0.0] * (len(dist) + 1)
    for i, v in enumerate(dist): nd[i] += v * (1 - p_); nd[i + 1] += v * p_
    dist = nd
print(f"  P(at least {got} slot-right look-alikes by chance) = {sum(dist[got:]):.2e}")
