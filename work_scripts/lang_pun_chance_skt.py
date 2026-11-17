# Rival test: the same slot-specific look-alike search in Sanskrit (Monier-Williams XML on disk, SLP1 keys).
# For each picture, every Sanskrit word for it is tried (gives Sanskrit the advantage); a hit = some OTHER headword
# sharing the first L letters (vowel length, retroflex/dental, sibilants merged) whose gloss has the slot meaning.
import re, sys, collections, html
L = int(sys.argv[1]) if len(sys.argv) > 1 else 3
MW = 'evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml'
gl = collections.defaultdict(str)
for line in open(MW, encoding='utf-8'):
    m = re.search(r'<key1>([^<]+)</key1>.*?<body>(.*?)</body>', line)
    if m and len(gl[m.group(1)]) < 3000: gl[m.group(1)] += ' ' + re.sub(r'<[^>]+>', ' ', html.unescape(m.group(2)))
def key(w): return w.translate(str.maketrans('AIUFXTDNRzSMHqQ', 'aiurltdnnssmhdd'))[:L]
by = collections.defaultdict(list)
for w in gl: by[key(w)].append(w)
PIC = {'jar':  (['kumBa', 'kalaSa', 'Gawa', 'sTAlI', 'kuRqa', 'BARqa'], r"\b(house|household|family|lineage|race)\b"),
       'man':  (['puruza', 'nara', 'manuzya', 'dAsa'], r"\b(rule|rules|ruler|manage|master)\b"),
       'fish': (['matsya', 'mIna', 'Jaza'], r"\bstars?\b"),
       'seven':(['saptan', 'sapta'], r"\b(rise|ascend)\b"),
       'comb': (['kaNkata', 'prasADanI'], r"\b(small|young|younger|junior)\b"),
       'spear':(['SUla', 'Sakti', 'fzwi', 'kunta', 'prAsa'], r"\b(chief|king|ruler|lord)\b"),
       'staff':(['daRqa', 'yazwi', 'laguqa'], r"\b(king|chief|lord|emperor)\b"),
       'carrier':(['BAra', 'vivaDa', 'vIvaDa', 'kAca'], r"\b(guard|protect|protection|keep)\b"),
       'tree': (['vfkza', 'taru', 'druma'], r"\b(warrior|valour|bravery)\b")}
words = list(gl)
got = 0; ps = []
for pic, (ws, rx) in PIC.items():
    R = re.compile(rx)
    has = {w: bool(R.search(gl[w])) for w in words}
    nk = collections.Counter(key(w) for w in words if has[w])
    base = sum((nk[key(w)] - has[w]) > 0 for w in words) / len(words)
    hit = [w for w in ws if w in gl and (nk[key(w)] - has[w]) > 0]
    got += bool(hit); ps.append(base)
    print(f"  {pic:8s} chance {base:.3f}  hit via {hit[:3] if hit else '-'}")
dist = [1.0]
for p in ps:
    nd = [0.0] * (len(dist) + 1)
    for i, v in enumerate(dist): nd[i] += v * (1 - p); nd[i + 1] += v * p
    dist = nd
print(f"Sanskrit, prefix {L}: {got} of {len(PIC)} slot-right look-alikes; expected by chance for ONE word per picture {sum(ps):.2f}; P(>= {got}) single-word = {sum(dist[got:]):.3f}")
