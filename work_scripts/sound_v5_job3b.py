#!/usr/bin/env python3
"""Job 3, redesigned tests (a null means the test was wrong: one redesign each).  Predictions written before running.
G1b the 45 jar uses followed by neither a closer nor the end: at least half are followed by a title/person word
    (guard 525-527, deputy 842, warrior 565, carrier 161, chief 255, staff-bearer 095, servant 617, goldsmith 104, lady 140).
G2b 060 then a number (34 uses): under uḷ "in" (eight_signs.md) a date "in the month, n": the opener before it is the
    month 920 more often than when a noun follows 060.
G3b dative: drop the never-with-the-jar condition: a sign that stands last right after a name word on goods objects,
    with a goods share at least twice the jar's (5+ texts).
G4b plural, goods only: on goods objects, leaving out fish signs (numbers in names are spelled words, star_names.md),
    no sign follows counted nouns 3x as often as uncounted ones (min 5).
G6b order, with the share/quarter words counted as measures (kāṇi is a land measure, DEDR 1444) and fish names left out:
    things take the number before (70%+), measures and shares take it after (70%+).
G7b owner before owned with spelled numbers allowed as owners: maka not text-first in 97%+, jar not first in 99%+.
G8b inside names (seal texts closing with the jar), crest/marker signs stand before the plain fish 220 in 70%+.
G9b verbs: given/sale/received/price stand last or right before a closing person sign (comb, carrier, man) in 60%+ of uses
    on goods faces (the act, then who did it: "sale, junior hand")."""
from sound_v5_job3 import *
rows.clear()
TITLE = {'525', '526', '527', '842', '565', '161', '255', '095', '617', '104', '140'}
oth = collections.Counter()
for x in R:
    for i, a in enumerate(x):
        if a == '740' and i + 1 < len(x) and x[i + 1] not in CLS: oth[x[i + 1]] += 1
t = sum(v for k, v in oth.items() if k in TITLE); n = sum(oth.values())
rep('G1b', 'half of the other signs after the jar are title/person words', f'{t} of {n} ({t / n:.0%}); commonest: {oth.most_common(8)}', 'jar + title = "of X\'s house, the [title]": a second title in the man\'s place', t / n >= 0.5)
op_num = collections.Counter(); op_noun = collections.Counter()
for x in A:
    for i, a in enumerate(x):
        if a == '060' and 0 < i and i + 1 < len(x):
            (op_num if x[i + 1] in NUMS else op_noun)[x[i - 1]] += 1
a1, n1 = op_num['920'], sum(op_num.values()); a2, n2 = op_noun['920'], sum(op_noun.values())
p = fisher_exact([[a1, n1 - a1], [a2, n2 - a2]], alternative='greater')[1]
rep('G2b', 'month opener before 060 more often when a number follows', f'month before 060 when a number follows {a1}/{n1} ({a1 / max(1, n1):.0%}) against {a2}/{n2} ({a2 / max(1, n2):.0%}) when a noun follows, P {p:.2g}; openers before 060+number {op_num.most_common(4)}',
    '060 + number after the month is a date: "in the month, n" (uḷ "in"), and 060 + noun after gate/district is an address', a1 / max(1, n1) > a2 / max(1, n2) and p <= 0.1)
cand = []
for s, c in fin.most_common():
    if c < 5 or s == '740' or s in NUMS: continue
    g, ng = goods_share({s})
    if g >= 2 * jar_g: cand.append((s, V5.get(s, ('?',))[0], c, round(g, 2)))
rep('G3b', 'a name-closing sign on goods objects at 2x the jar share', f'jar goods share {jar_g:.0%}; candidates (sign, sound, texts ending name+sign, goods share): {cand[:8]}', 'the closing sign of issue tablets after a name: "for/by X" read as the agent or recipient ending', bool(cand))
ca = collections.Counter(); ua = collections.Counter()
for x, k in A.items():
    if k == 'seal': continue
    for i in range(1, len(x) - 1):
        a = x[i]
        if a in NUMS or a in FISH: continue
        (ca if x[i - 1] in NUMS and VAL[x[i - 1]] >= 2 else ua)[x[i + 1]] += 1
tc, tu = sum(ca.values()), sum(ua.values())
pl = [(s, c, ua[s]) for s, c in ca.items() if c >= 5 and s not in NUMS and c / tc >= 3 * ua[s] / tu]
rep('G4b', 'no plural suffix on counted goods nouns', f'after counted goods nouns {tc}, uncounted {tu}; 3x+ signs: {pl}', 'empty list = the number alone makes the plural, as Dravidian does with non-human nouns', not pl)
MS = MEASW | {'861', '817', '820', '850', '877', '868'}
nb = na = mb = ma = 0
for x in R:
    for i in range(len(x) - 1):
        a, b = x[i], x[i + 1]
        if a in NUMS and b not in NUMS and b not in ('740', '700') and b not in FISH:
            if b in MS: mb += 1
            else: nb += 1
        if b in NUMS and a not in NUMS and a != '740' and a not in FISH:
            if a in MS: ma += 1
            else: na += 1
rep('G6b', 'things: number before 70%+; measures/shares: number after 70%+', f'things: before {nb}, after {na} ({nb / max(1, nb + na):.0%} before); measures and shares: before {mb}, after {ma} ({ma / max(1, mb + ma):.0%} after)',
    'count + thing, but measure/share + count: "kāṇi iru" two shares, "kalam mū" three kalam, the order Old Tamil uses for measures', nb / max(1, nb + na) >= 0.7 and ma / max(1, mb + ma) >= 0.7)
rep('G7b', 'maka not first 97%+, jar not first 99%+', f'maka not first {m_all - m_first} of {m_all} ({1 - m_first / m_all:.1%}); jar not first {j_all - j_first} of {j_all} ({1 - j_first / j_all:.1%})', 'possessor before possessed', 1 - m_first / m_all >= 0.97 and 1 - j_first / j_all >= 0.99)
MK = {'231', '233', '235', '240', '415', '798', '226'}
pre = post = 0
for x, k in A.items():
    if k != 'seal' or '740' not in x: continue
    j = max(i for i, a in enumerate(x) if a == '740'); nm = x[:j]
    for i in range(len(nm) - 1):
        if nm[i] in MK and nm[i + 1] == '220': pre += 1
        if nm[i] == '220' and nm[i + 1] in MK: post += 1
rep('G8b', 'markers before the plain fish in names 70%+', f'marker then plain fish {pre}; plain fish then marker {post} ({pre / max(1, pre + post):.0%} before)', 'modifier before head inside names: "Branch-Star", "Descendant-Star"', pre / max(1, pre + post) >= 0.7)
k = n = 0; per = collections.Counter()
for x, kd in A.items():
    if kd == 'seal': continue
    for i, a in enumerate(x):
        if a in VERB:
            n += 1; nx = x[i + 1] if i + 1 < len(x) else '$'
            if nx == '$' or nx in {'400', '090'} | PORTER: k += 1; per[a] += 1
rep('G9b', 'verbs last or right before a closing person sign 60%+', f'{k} of {n} ({k / max(1, n):.0%}); by sign {dict(per)}', 'verb + agent: "sold, junior hand"; the act stands at the end of the goods phrase', k / max(1, n) >= 0.6)
pd.DataFrame(rows).to_csv(f'{OUT5}/job3b_grammar.csv', index=False)
