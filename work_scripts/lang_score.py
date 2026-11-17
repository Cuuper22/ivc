# Head-to-head score of candidate languages: grammar fit against measured slot facts, and picture-and-job puns.
# 1 = works, 0.5 = works by meaning only or a near sound, 0 = fails or no word found. Sources per row in language_candidates.md.
import collections
LANGS = ['Dravidian', 'Munda', 'Indo-Aryan', 'Elamite', 'Sumerian', 'Burushaski', 'lost']
GRAMMAR = [  # (measured fact, scores)
 ('possessor + ending, then possessed ([name] jar man)', dict(Dravidian=1, Munda=1, **{'Indo-Aryan': 1}, Elamite=0, Sumerian=0, Burushaski=1, lost=0.5)),
 ('class/title after the name',                           dict(Dravidian=1, Munda=1, **{'Indo-Aryan': 0.5}, Elamite=1, Sumerian=1, Burushaski=1, lost=0.5)),
 ('number before the counted thing',                      dict(Dravidian=1, Munda=1, **{'Indo-Aryan': 1}, Elamite=0.5, Sumerian=0, Burushaski=1, lost=0.5)),
 ('two count systems: containers/measures vs living+grown (women with fish and trees)',
                                                          dict(Dravidian=0, Munda=0, **{'Indo-Aryan': 0}, Elamite=0, Sumerian=0, Burushaski=0.5, lost=0.5)),
 ('names built modifier-first, head-last (crest self tag)', dict(Dravidian=1, Munda=1, **{'Indo-Aryan': 1}, Elamite=0, Sumerian=0, Burushaski=1, lost=0.5)),
]
PUNS = [  # (sign, picture -> job, scores)
 ('740 jar', 'kuṭam waterpot ~ kuṭi house/lineage; *aṭka pot ~ oblique -aṭṭ-', dict(Dravidian=1)),
 ('090 man after jar', 'āḷ man/servant ~ āḷ to rule, manage a household', dict(Dravidian=1, Sumerian=0.5, **{'Indo-Aryan': 0.5})),
 ('220 fish opening names', 'mīn fish ~ mīṉ star', dict(Dravidian=1, **{'Indo-Aryan': 0.5})),
 ('016+220 six-fish unit', 'aṟu-mīn six-star = Pleiades', dict(Dravidian=1)),
 ('017 seven opening names', 'er̤u seven ~ er̤u rise, ascend (heavenly body)', dict(Dravidian=1, **{'Indo-Aryan': 0.5})),
 ('400 comb after jar, smallest seals', 'cīrppu comb ~ ciṟu/cīṟ small, junior', dict(Dravidian=1, **{'Indo-Aryan': 0.5})),
 ('520 spear class', 'vēl spear ~ vēḷ chief, petty ruler', dict(Dravidian=1)),
 ('142 person with staff', 'kōl staff ~ kō/kōṉ king', dict(Dravidian=1, Sumerian=0.5, **{'Indo-Aryan': 0.5})),
 ('154/158 load-carrier class', 'kā carrying pole ~ kā guard, keep; kāval store', dict(Dravidian=1, **{'Indo-Aryan': 0.5})),
 ('390 tree ending names', 'maram tree ~ maṟam valour, warrior', dict(Dravidian=0.5)),
 ('100 three-headed person ending names', 'mū three ~ mutu old, elder', dict(Dravidian=0.5)),
 ('002 two / 091 twin men', 'iru two; iraṭṭai pair, twins', dict(Dravidian=0.5)),
]
OUTSIDE = [  # outside words: which candidate they sound like
 ('Meluhha', dict(Dravidian=1, Munda=0.5, **{'Indo-Aryan': 0.5})),
 ('Akkadian ellu sesame oil', dict(Dravidian=1)),
 ('Rigveda ka-/ki- prefix words (kīnāśa ploughman)', dict(Munda=1)),
 ('Rigveda kulāya nest, khala threshing floor, daṇḍa stick (Zvelebil)', dict(Dravidian=1)),
 ('Witzel: Dravidian loans only from middle Rigveda', dict(Munda=1)),
]
def tot(rows, i):
    t = collections.Counter()
    for r in rows:
        for l in LANGS: t[l] += r[i].get(l, 0)
    return t
g, p, o = tot(GRAMMAR, 1), tot(PUNS, 2), tot(OUTSIDE, 1)
print(f"{'language':12s} grammar/{len(GRAMMAR)}  puns/{len(PUNS)}  outside/{len(OUTSIDE)}  total")
for l in LANGS: print(f"{l:12s} {g[l]:8.1f} {p[l]:8.1f} {o[l]:10.1f} {g[l]+p[l]+o[l]:7.1f}")
sole = collections.Counter(max(r[2], key=r[2].get) for r in PUNS if r[2] and list(r[2].values()).count(max(r[2].values())) == 1 and max(r[2].values()) == 1)
print('puns that work in one language only (full score):', dict(sole))
