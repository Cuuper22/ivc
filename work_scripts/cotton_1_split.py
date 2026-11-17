"""PART 1. Split reading A (Chest-guard: 590 'chest' + 390 'keeper', a name or title) from reading B (Chest of cotton: 390 = cotton, a house named for its trade).
Run: python3 cotton_1_split.py   (log -> cotton_out/split_log.txt, tables -> cotton_out/split_*.csv)

PREDICTIONS, WRITTEN BEFORE THE RUN
Reading A (a keeper's name or title -> a WHO):
  A1 the pair sits in the name slot: the jar 'of the house' follows it at the rate it follows names (about 70% or more), on seals.
  A2 a keeper is not counted in lots: 390 should NOT be a counted noun elsewhere (A has no use for 3-8 of them); counts before the pair are opener strokes (two strokes), not tall lots.
  A3 'box + X' for other X gives other keepers/titles (carriers, comb), not goods.
Reading B (a trade house named for its goods -> a WHO that carries a WHAT word inside it):
  B1 slot: still the name slot (a house named for cotton) on seals, but goods-like on tags (count in front, no jar).
  B2 390 is a counted noun on its own (lots of 3+), and the box before it takes the lot count (tall strokes, 3 or more), not an opener stroke.
  B3 'box + X': X are goods words (counted nouns) -> 590-405 (yarn?), 590-407 (cloth?) exist; box+sesame(838), box+grain(413) are asked.
  B4 object types: more tags/pots/tablets than names would have.
WHERE THEY DIFFER (the splitters): B2 (390 elsewhere counted in lots; tall lot-count before the box), B3 (X are counted nouns), A3 (X are keeper signs).
If A1 and B1-B3 all come true: a house named after its trade. Say so with the numbers.
"""
from cotton_common import *
f = open(f'{OUTC}/split_log.txt', 'w')
d = faces()
NUMS = {k: v for k, v in CNT.items() if v[0] != 'A'}
TALLS = {k for k, v in NUMS.items() if v[0] == 'F'}
def val(t): return NUMS[t][1]
T = d.toks.tolist()
N = len(d)
log(f, f'faces {N}, objects {d.obj.nunique()}')
# ---------------- the pair faces
pi = [i for i, t in enumerate(T) if has_pair(t, '590', '390')]
log(f, f'\n== S0 the pair: {len(pi)} faces on {d.iloc[pi].obj.nunique()} objects')
# ---------------- S1 slot: what follows the pair
def after(t, j, k=1): return t[j + k] if j + k < len(t) else None
def before(t, j, k=1): return t[j - k] if j - k >= 0 else None
rows = []
for i in pi:
    t = T[i]; j = has_pair(t, '590', '390')[0]
    rows.append(dict(i=i, obj=d.obj.iloc[i], cls=d.cls.iloc[i], site=d.site.iloc[i], jar=after(t, j + 1) == JAR if j + 1 < len(t) else False,
                     end=(j + 2 == len(t)), nxt=after(t, j + 1), prv=before(t, j), text='-'.join(t)))
R = pd.DataFrame(rows)
log(f, 'S1 what follows the pair (by object class):')
log(f, R.groupby('cls').apply(lambda g: pd.Series(dict(faces=len(g), jar_next=int(g.jar.sum()), pair_is_last=int(g.end.sum())))).to_string())
# jar rate base: P(jar directly after a given sign position) for seals, tags etc. as base: faces with jar after the LAST-but-one position? use: share of faces whose text ends in jar
def ends_jar(t): return len(t) > 0 and t[-1] == JAR
base = d.groupby('cls').apply(lambda g: pd.Series(dict(n=len(g), ends_in_jar=np.mean([ends_jar(t) for t in g.toks])))).round(3)
log(f, 'base: share of faces ending in the jar, by object class:\n' + base.to_string())
# jar-after rate for every bigram (a,b) with n>=10 -> where does 590-390 sit
bg = collections.defaultdict(lambda: [0, 0, 0, 0, 0])  # n, jar_after, count_before, seal, tag/pot
for k, t in enumerate(T):
    c = d.cls.iloc[k]
    for j in range(len(t) - 1):
        a, b = t[j], t[j + 1]
        e = bg[(a, b)]
        e[0] += 1
        if j + 2 < len(t) and t[j + 2] == JAR: e[1] += 1
        if j > 0 and t[j - 1] in NUMS: e[2] += 1
        if c == 'seal': e[3] += 1
        if c in ('tag', 'pot'): e[4] += 1
B = pd.DataFrame([(a, b, *v) for (a, b), v in bg.items()], columns=['a', 'b', 'n', 'jar_after', 'count_before', 'on_seal', 'on_tag_pot'])
B = B[(B.n >= 10) & (B.a != '000') & (B.b != '000') & (B.a != JAR) & (B.b != JAR)].copy()
B['jar_rate'] = B.jar_after / B.n; B['count_rate'] = B.count_before / B.n; B['seal_rate'] = B.on_seal / B.n; B['tagpot_rate'] = B.on_tag_pot / B.n
B.to_csv(f'{OUTC}/split_bigrams.csv', index=False)
me = B[(B.a == '590') & (B.b == '390')].iloc[0]
log(f, f'\nS1b among the {len(B)} bigrams with n>=10 (no lost sign, no jar): 590-390 has n {int(me.n)}, jar right after {me.jar_rate:.2f}, count right before {me.count_rate:.2f}, on seals {me.seal_rate:.2f}, on tags/pots {me.tagpot_rate:.3f}')
for col in ['jar_rate', 'count_rate', 'seal_rate', 'tagpot_rate']:
    log(f, f'   {col}: percentile of 590-390 among bigrams = {100*(B[col] < me[col]).mean():.0f}  (median of bigrams {B[col].median():.2f})')
# name-class reference: bigrams whose first sign is a fish crest; goods-class reference: bigrams with count_rate>=0.4 (counted-thing pairs)
FISHC = {'220', '233', '235', '240', '231', '226', '236'}
names_ref = B[B.a.isin(FISHC)]
goods_ref = B[B.count_rate >= 0.4]
log(f, f'   fish-crest-first bigrams ({len(names_ref)}): median jar_rate {names_ref.jar_rate.median():.2f}, count_rate {names_ref.count_rate.median():.2f}, tagpot {names_ref.tagpot_rate.median():.3f}')
log(f, f'   counted-pair bigrams (count_rate>=0.4, {len(goods_ref)}): median jar_rate {goods_ref.jar_rate.median():.2f}, count_rate {goods_ref.count_rate.median():.2f}, tagpot {goods_ref.tagpot_rate.median():.3f}')
# ---------------- S2 counts in front of the pair
log(f, '\n== S2 counts in front of the pair')
cb = Counter = collections.Counter()
for i in pi:
    t = T[i]; j = has_pair(t, '590', '390')[0]
    p = before(t, j)
    cb[p if p in NUMS else 'none'] += 1
log(f, 'what stands right before 590 (count sign or none): ' + str(dict(cb.most_common())))
tall_pair = sum(v for k, v in cb.items() if k in TALLS); two_pair = cb.get('002', 0)
nonpair590 = []; 
for k, t in enumerate(T):
    for j, x in enumerate(t):
        if x == '590' and not (j + 1 < len(t) and t[j + 1] == '390'):
            nonpair590.append((k, j))
cnt_np = collections.Counter((before(T[k], j) if before(T[k], j) in NUMS else 'none') for k, j in nonpair590)
log(f, f'box 590 NOT followed by 390 ({len(nonpair590)} places): ' + str(dict(cnt_np.most_common(8))))
r, p = fe(tall_pair, len(pi) - tall_pair, sum(v for k, v in cnt_np.items() if k in TALLS), len(nonpair590) - sum(v for k, v in cnt_np.items() if k in TALLS))
log(f, f'tall-stroke count right before the box: with 390 {tall_pair}/{len(pi)}, without {sum(v for k,v in cnt_np.items() if k in TALLS)}/{len(nonpair590)}: ratio {r:.2f}, one-sided P {p:.3f}')
# value of count before pair (3 or more?)
vals = [val(k) for k in cb if k in NUMS for _ in range(cb[k])]
log(f, f'count values before the pair (n {len(vals)}): {sorted(collections.Counter(vals).items())}; share >=3: {np.mean([v>=3 for v in vals]):.2f}')
vals2 = [val(before(T[k], j)) for k, j in nonpair590 if before(T[k], j) in NUMS]
log(f, f'count values before box-without-390 (n {len(vals2)}): {sorted(collections.Counter(vals2).items())}; share >=3: {np.mean([v>=3 for v in vals2]):.2f}')
# ---------------- S3 390 elsewhere: counted noun?
log(f, '\n== S3 sign 390 on its own (not right after 590)')
e390 = [(k, j) for k, t in enumerate(T) for j, x in enumerate(t) if x == '390']
alone = [(k, j) for k, j in e390 if not (j > 0 and T[k][j - 1] == '590')]
cnt_alone = [(k, j) for k, j in alone if j > 0 and T[k][j - 1] in NUMS]
log(f, f'390 places {len(e390)}; after the box {len(e390)-len(alone)}; elsewhere {len(alone)}; of those with a count right before {len(cnt_alone)} ({len(cnt_alone)/len(alone):.2f})')
v3 = [val(T[k][j - 1]) for k, j in cnt_alone]
log(f, f'   count values before 390 elsewhere: {sorted(collections.Counter(v3).items())}; share >=3: {np.mean([v>=3 for v in v3]):.2f}')
log(f, f'   390 elsewhere: jar right after {np.mean([(j+1<len(T[k]) and T[k][j+1]==JAR) for k,j in alone]):.2f}; on seals {np.mean([d.cls.iloc[k]=="seal" for k,j in alone]):.2f}; text is 390 only {sum(len(T[k])==1 for k,j in alone)}')
# base: P(count right before sign) for the 40 commonest signs, ranking of 390
sc = collections.defaultdict(lambda: [0, 0])
for t in T:
    for j, x in enumerate(t):
        if x in NUMS or x in ('000', 'ALT'): continue
        sc[x][0] += 1
        if j > 0 and t[j - 1] in NUMS: sc[x][1] += 1
S = pd.DataFrame([(k, *v) for k, v in sc.items()], columns=['sign', 'n', 'counted']); S = S[S.n >= 30]; S['rate'] = S.counted / S.n
S = S.sort_values('rate', ascending=False); S.to_csv(f'{OUTC}/split_counted_rate.csv', index=False)
rk = list(S.sign).index('390') + 1
log(f, f'   counted rate (count right before, all places) for 390 = {S.set_index("sign").loc["390","rate"]:.2f}; rank {rk} of {len(S)} signs with n>=30; median of all {S.rate.median():.2f}')
for s in ['405', '407', '590', '838', '413', '806', '220']:
    if s in set(S.sign): log(f, f'      sign {s}: n {int(S.set_index("sign").loc[s,"n"])}, count right before {S.set_index("sign").loc[s,"rate"]:.2f}')
# ---------------- S4 box + X
log(f, '\n== S4 what follows the box 590 (all faces)')
fx = collections.Counter(T[k][j + 1] for k, j in [(k, j) for k, t in enumerate(T) for j, x in enumerate(t) if x == '590' and j + 1 < len(t)])
tot590 = sum(fx.values())
tab = []
Sd = S.set_index('sign')
for x, n in fx.most_common(14):
    jar = np.mean([ (j + 2 < len(T[k]) and T[k][j + 2] == JAR) for k, t in enumerate(T) for j in range(len(t) - 1) if t[j] == '590' and t[j + 1] == x])
    rate = Sd.loc[x, 'rate'] if x in Sd.index else np.nan
    tab.append((x, n, round(jar, 2), round(rate, 2) if rate == rate else None))
log(f, 'sign after box, n, jar right after the pair, counted-rate of that sign (count right before it, anywhere):')
for r_ in tab: log(f, '   ' + str(r_))
pd.DataFrame(tab, columns=['X', 'n', 'jar_after_pair', 'X_counted_rate']).to_csv(f'{OUTC}/split_box_X.csv', index=False)
# same-face co-occurrence of box with sesame, grain, crop, carriers
for x in ['838', '413', '806', '405', '407', '392', '390']:
    both = sum(1 for t in T if '590' in t and x in t)
    adj = sum(1 for t in T for j in range(len(t) - 1) if t[j] == '590' and t[j + 1] == x)
    adj_rev = sum(1 for t in T for j in range(len(t) - 1) if t[j] == x and t[j + 1] == '590')
    n_x = sum(1 for t in T if x in t)
    n_b = sum(1 for t in T if '590' in t)
    exp = n_x * n_b / N
    log(f, f'   box with {x} on the same face {both} (chance {exp:.1f}); box then {x} adjacent {adj}; {x} then box {adj_rev}')
fam = {'390', '405', '407', '406', '392'}
log(f, f'tree family right after the box: {sum(n for x, n in fx.items() if x in fam)} of {tot590} box places ({sum(n for x,n in fx.items() if x in fam)/tot590:.2f}); base share of tree family among all sign places {sum(sum(1 for x in t if x in fam) for t in T)/sum(len(t) for t in T):.3f}')
# keeper signs after the box (A3): carriers 151-158, spear 520, man 090, comb 400
KEEP = {'151', '153', '154', '155', '156', '157', '158', '520', '090', '400'}
log(f, f'keeper/title signs (carriers, spear, man, comb) right after the box: {sum(n for x,n in fx.items() if x in KEEP)} of {tot590}')
# ---------------- S5 who/what: long-text phrase kinds
log(f, '\n== S5 who-part / what-part (long texts)')
lp = pd.read_csv(f'{ROOT}/work_data/long_texts/long_phrases_all.csv', dtype=str, keep_default_na=False)
hit = lp[lp.signs.str.contains(r'(^|-)590-(390|405|407)(-|$)')]
log(f, f'long-text phrases containing box+tree-family: {len(hit)} of {len(lp)}; kinds: {dict(hit.kind.value_counts())}')
log(f, f'all phrase kinds: {dict(lp.kind.value_counts())}')
for _, r_ in hit.iterrows(): log(f, f'   {r_.cisi} line {r_.line} [{r_.kind}] {r_.signs}')
# ---------------- S6 who in front of the pair
log(f, '\n== S6 is there a separate name in front?')
def front_signs(t, j): return [x for x in t[:j] if x not in NUMS and x not in ('000',)]
fr = []
for i in pi:
    t = T[i]; j = has_pair(t, '590', '390')[0]
    fr.append(len(front_signs(t, j)))
fr = np.array(fr)
log(f, f'non-count signs in front of the pair: 0 on {np.sum(fr==0)} faces (the pair IS the whole name), 1 on {np.sum(fr==1)}, 2+ on {np.sum(fr>=2)} (n {len(fr)})')
# same for other recurring trade-like pairs ending a name: compare to 590-405, 590-407
for x in ['405', '407']:
    idx = [(k, has_pair(T[k], '590', x)[0]) for k, t in enumerate(T) if has_pair(t, '590', x)]
    z = [len(front_signs(T[k], j)) for k, j in idx]
    jr = np.mean([(j + 2 < len(T[k]) and T[k][j + 2] == JAR) for k, j in idx])
    sl = np.mean([d.cls.iloc[k] == 'seal' for k, j in idx])
    cp = np.mean([(j > 0 and T[k][j - 1] in NUMS) for k, j in idx])
    tl = np.mean([(d.cls.iloc[k] in ('tag', 'pot')) for k, j in idx])
    tb = np.mean([(d.cls.iloc[k] in ('tabB', 'tabI')) for k, j in idx])
    mat = collections.Counter(d.mat.iloc[k] for k, j in idx)
    log(f, f'box+{x}: n {len(idx)}; jar right after {jr:.2f}; on seals {sl:.2f}; on tablets {tb:.2f}; tag/pot {tl:.2f}; count right before box {cp:.2f}; nothing in front {np.mean(np.array(z)==0):.2f}; materials {dict(mat)}')
R.to_csv(f'{OUTC}/split_pair_faces.csv', index=False)
f.close()
