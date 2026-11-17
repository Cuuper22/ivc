#!/usr/bin/env python3
"""Job 3 of the fifth pass: the grammar.  Every claim's prediction is written here before the number was computed.
Test bed: distinct texts that read whole under the fifth wide list (first catalogue complete faces + complete new
texts), and for the scans all distinct texts of both catalogues.  Writes work_data/sound_v5/job3_grammar.csv.

PREDICTIONS (written first)
G1  jar = possessive "of the house": in read texts the sign after the jar is a person/class sign (man 090, comb 400,
    spear 520, carriers) or the end of the text in at least 95% of jar uses, and the sign before it is never a number.
G2  060 = joiner -iṉ "of": the sign before 060 is an opener (920, 550, 692, 820) in at least 70% of uses, and the
    sign after it is never a number and never the end of the text.
G3  dative "for": at least one sign that closes a name on goods objects stands where the jar stands (after a name
    word) but never on a face with the jar, and sits on goods objects at twice the jar's goods share or more.
G4  no plural suffix on counted nouns (Dravidian non-human nouns with a numeral take none): no sign follows counted
    nouns three or more times as often as it follows the same nouns uncounted (minimum 5 uses after counted nouns).
G5  "and": a sign that repeats inside one text, each time right after a noun ("X-um Y-um"), more than signs of its
    frequency repeat.  Prediction: at least one such sign with 3+ texts.
G6  number before noun for things and persons (at least 70% of number-noun contacts have the number first), and
    number AFTER the measure words (705, 706, 711, 320, 575, 540, 171) in at least 70% (noun-measure-count, the Old
    Tamil account order "nel kalam mūṉṟu").
G7  owner before owned: maka "child of" 760 never opens a text and stands after its owner word in at least 90%;
    the jar never opens a text.
G8  modifier before head: where a marker sign stands next to the plain fish 220 (star names), the marker comes first
    in at least 80% (Branch-Star, not Star-Branch).
G9  verbs at the end of account lines: given 890, sale 892, received 440, price 824 are the last sign on goods faces
    at least twice as often as signs on goods faces overall.
G10 head-last overall: on read texts with 3+ signs the last sign is a closing class or verb word (jar, man, comb,
    spear, carrier, guard, given, sale, received) in at least 60%."""
from sound_v5_common import *
from sound_v5_values import V5, TIER5
NUMS = set(VAL)
MEASW = {'705', '706', '711', '320', '575', '540', '171'}
OPEN = {'920', '550', '692', '820'}
CLS = {'090', '400', '520'} | PORTER
VERB = {'890', '892', '440', '824'}
CLOSERS = {'740', '090', '400', '520', '527', '525', '526', '890', '892', '440'} | PORTER


def read_texts():
    out = {}
    for r in d[d.complete_txt].itertuples():
        if readable(r.tok, TIER5): out.setdefault(r.tok, r.kind)
    m = M[~M.partnered & M.complete_b]
    for x, k in zip(m.tok, m.kind):
        if readable(x, TIER5): out.setdefault(x, k)
    return out


def all_texts():
    out = {}
    for x, k, st in kfaces('LM'):
        if '000' not in x and 'ALT' not in x: out.setdefault(tuple(x), k)
    return out


R = read_texts(); A = all_texts(); rows = []
def rep(g, pred, num, meaning, ok):
    rows.append(dict(claim=g, prediction=pred, number=num, outcome='yes' if ok else 'no', meaning=meaning))
    print(f'{g}: {"yes" if ok else "no"} | {num}\n   {meaning}', flush=True)

print(f'test bed: {len(R)} distinct read texts; scans over {len(A)} distinct texts', flush=True)
# G1
after = collections.Counter(); before_num = 0; n = 0
for x in R:
    for i, a in enumerate(x):
        if a == '740':
            n += 1; nx = x[i + 1] if i + 1 < len(x) else '$'; after[nx if nx in CLS or nx == '$' else 'other'] += 1
            before_num += i > 0 and x[i - 1] in NUMS
sh = (n - after['other']) / n
rep('G1', 'after the jar: class sign or end in 95%+; never a number before it', f'jar uses {n}: next is end {after["$"]}, man {after["090"]}, comb {after["400"]}, other {after["other"]} ({sh:.1%} class or end); a number right before the jar {before_num}',
    'the jar closes a name and only a person word may follow: "of X\'s house" then "the man / the junior". A possessive ending, not a noun.', sh >= 0.95)
# G2
pv = collections.Counter(); nx = collections.Counter(); n = 0
for x in A:
    for i, a in enumerate(x):
        if a == '060':
            n += 1; pv['open' if i > 0 and x[i - 1] in OPEN else 'start' if i == 0 else 'other'] += 1
            b = x[i + 1] if i + 1 < len(x) else '$'; nx['num' if b in NUMS else 'end' if b == '$' else 'noun'] += 1
rep('G2', 'opener before 060 in 70%+; after it never a number, never the end', f'060 uses {n} (all distinct texts): opener before {pv["open"]} ({pv["open"] / n:.0%}), text start {pv["start"]}, other {pv["other"]}; after it a noun {nx["noun"]}, a number {nx["num"]}, the end {nx["end"]}',
    '060 links the opener to the noun after it, like Old Tamil -iṉ: "[month/gate/assembly]-of [ward ...]".', pv['open'] / n >= 0.7 and nx['num'] == 0 and nx['end'] == 0)
# G3 dative scan: signs standing right after a name-slot word (a crest or a house word that takes the jar) as last sign
NAMEW = {a for a in V5 if TIER5.get(a) in ('building', 'base')} - NUMS - CLOSERS - {'700'}
def goods_share(S):
    k = [kd != 'seal' for x, kd in A.items() if S & set(x)]; return np.mean(k) if k else np.nan, len(k)
jar_g, _ = goods_share({'740'})
cand = []
fin = collections.Counter(); withjar = collections.Counter()
for x, kd in A.items():
    if len(x) >= 2 and x[-2] in NAMEW: fin[x[-1]] += 1
    for a in set(x):
        if '740' in x and a != '740': withjar[a] += 1
for s, c in fin.most_common():
    if c < 4 or s in ('740',) or s in NUMS: continue
    g, ng = goods_share({s})
    if withjar[s] == 0 and g >= 2 * jar_g: cand.append((s, c, ng, round(g, 2)))
rep('G3', 'a name-closing sign never with the jar, on goods objects at 2x the jar\'s share', f'jar on goods objects {jar_g:.0%} of its texts; candidates (sign, texts ending name+sign, texts with sign, goods share): {cand[:8]}',
    'a sign in the jar\'s place on goods objects and never with it is the issue ending "for X" (Old Tamil dative -ku): ' + (', '.join(f'{c[0]} {V5.get(c[0], ("?",))[0]}' for c in cand[:5]) or 'none found'), bool(cand))
# G4 plural
cnt_after = collections.Counter(); unc_after = collections.Counter(); nounc = collections.Counter(); nounu = collections.Counter()
for x in A:
    for i in range(1, len(x) - 1):
        a = x[i]
        if a in NUMS: continue
        if x[i - 1] in NUMS and VAL[x[i - 1]] >= 2: cnt_after[x[i + 1]] += 1; nounc[a] += 1
        else: unc_after[x[i + 1]] += 1; nounu[a] += 1
tc = sum(cnt_after.values()); tu = sum(unc_after.values())
plur = [(s, c, unc_after[s], round((c / tc) / max(unc_after[s] / tu, 1e-9), 1)) for s, c in cnt_after.items() if c >= 5 and s not in NUMS and (c / tc) >= 3 * (unc_after[s] / tu)]
rep('G4', 'no sign follows counted nouns 3x as often as uncounted ones (min 5)', f'signs after counted nouns: {tc}, after uncounted: {tu}; signs 3x+ after counted nouns: {sorted(plur, key=lambda r: -r[1])[:8]}',
    'if empty: no plural suffix, the number alone marks plurality, as in Dravidian non-human nouns; any sign listed is a plural or a unit word to look at', not plur)
# G5 "and"
rep_txt = collections.Counter(); use = collections.Counter()
for x in A:
    for a in set(x): use[a] += 1
    for a in set(x):
        idx = [i for i, b in enumerate(x) if b == a]
        if len(idx) >= 2 and all(i > 0 and x[i - 1] not in NUMS and x[i - 1] != a for i in idx) and a not in NUMS: rep_txt[a] += 1
peers = {a: rep_txt[a] / use[a] for a in use if use[a] >= 10}
med = np.median(list(peers.values()))
andc = [(a, rep_txt[a], use[a], V5.get(a, ('?',))[0]) for a in sorted(rep_txt, key=lambda a: -rep_txt[a]) if rep_txt[a] >= 3 and use[a] >= 10 and peers[a] > 3 * max(med, 0.005)]
rep('G5', 'a sign repeated in one text after two different nouns, 3+ texts', f'repeat-after-noun texts (sign, texts, uses, sound): {andc[:8]}; median repeat share {med:.3f}',
    'a sign that comes back after each listed noun is the coordinator "-um ... -um" (and)', bool(andc))
# G6 number order
nb = na = mb = ma = 0
for x in R:
    for i in range(len(x) - 1):
        a, b = x[i], x[i + 1]
        if a in NUMS and b not in NUMS and b not in ('740', '700'):
            if b in MEASW: mb += 1
            else: nb += 1
        if b in NUMS and a not in NUMS:
            if a in MEASW: ma += 1
            elif a not in ('740',): na += 1
rep('G6', 'number before noun 70%+; number after measure words 70%+', f'nouns: number before {nb}, after {na} ({nb / max(1, nb + na):.0%} before); measure words: number before {mb}, after {ma} ({ma / max(1, mb + ma):.0%} after)',
    'two orders: count + thing ("three chests", "two shares"), and thing + measure + count ("grain kalam three"), the Old Tamil account order', nb / max(1, nb + na) >= 0.7 and ma / max(1, mb + ma) >= 0.7)
# G7 owner before owned
m_first = sum(1 for x in A if x and x[0] == '760'); m_all = sum(1 for x in A if '760' in x)
j_first = sum(1 for x in A if x and x[0] == '740'); j_all = sum(1 for x in A if '740' in x)
m_after_name = sum(1 for x in A for i, a in enumerate(x) if a == '760' and i > 0 and x[i - 1] not in NUMS); m_n = sum(1 for x in A for a in x if a == '760')
rep('G7', 'maka never first, after its owner 90%+; jar never first', f'760 first in {m_first} of {m_all} texts; after a non-number word {m_after_name} of {m_n} uses; jar first in {j_first} of {j_all}',
    'possessor first, possessed after: "[owner] maka" = "[owner]\'s child", "[name] kuṭi" = "[name]\'s house"', m_first == 0 and m_after_name / m_n >= 0.9 and j_first == 0)
# G8 modifier before head
mods = {'415', '798', '255', '141', '061', '235', '231', '240', '233', '226'}
pre = post = 0
for x in A:
    for i in range(len(x) - 1):
        if x[i + 1] == '220' and x[i] not in NUMS and x[i] not in ('220',): pre += 1
        if x[i] == '220' and x[i + 1] not in NUMS and x[i + 1] not in CLOSERS and x[i + 1] not in ('220', '700'): post += 1
rep('G8', 'marker before the plain fish 80%+', f'a word right before the plain fish 220: {pre}; a non-closing word right after it: {post} ({pre / max(1, pre + post):.0%} before)',
    'modifier before head: "Branch-Star", "Descendant Star"; the fish (star) is the head noun of the name', pre / max(1, pre + post) >= 0.8)
# G9 verbs last
fin_all = sum(1 for x, k in A.items() if k != 'seal' for i, a in enumerate(x) if i == len(x) - 1 and len(x) >= 2)
pl_all = sum(len(x) for x, k in A.items() if k != 'seal' and len(x) >= 2)
vv = []
for v in sorted(VERB):
    k = sum(1 for x, kd in A.items() if kd != 'seal' and len(x) >= 2 for i, a in enumerate(x) if a == v and i == len(x) - 1)
    n = sum(1 for x, kd in A.items() if kd != 'seal' and len(x) >= 2 for a in x if a == v)
    vv.append((v, V5[v][0], k, n))
k = sum(r[2] for r in vv); n = sum(r[3] for r in vv); base = fin_all / pl_all
p = binomtest(k, n, base, alternative='greater').pvalue if n else 1
rep('G9', 'verb words last on goods faces at 2x the base', f'verb words last {k} of {n} uses ({k / max(1, n):.0%}) against {base:.0%} for all goods-face sign places (P {p:.2g}); per sign {vv}',
    'the account line ends in the act: "[goods] [amount] given / sold / received", verb-final like Dravidian', n > 0 and k / n >= 2 * base)
# G10 head-last overall
fin3 = [x[-1] in CLOSERS for x in R if len(x) >= 3]
rep('G10', 'last sign is a closer or verb in 60%+ of read texts with 3+ signs', f'{sum(fin3)} of {len(fin3)} ({np.mean(fin3):.0%})', 'texts end in the head: possessive, title or verb', np.mean(fin3) >= 0.6)
pd.DataFrame(rows).to_csv(f'{OUT5}/job3_grammar.csv', index=False)
