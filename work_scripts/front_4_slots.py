#!/usr/bin/env python3
"""FRONT job 4: the slot signs.  Number series or fixed marker?  2026-11-17.

Questions: after one front word, does the slot run through 1, 2, 3 strokes (001 002 003 ...)?  Do 741 / 742 / 745 behave
as first, second, third of something (the same front and the same name with a different slot sign)?  Or is the slot a
marker that does not move with anything?

Predictions, written before the numbers:
 P1  NOT a number series: after the diamond fronts (861, 817) the sign after the front is 002 in 90%+ of cases and the
     other stroke counts (001, 003, 004 ...) together under 5%. After the wheel 820 the stroke count DOES vary (001 and
     002 both common): 820 is the one front that takes a count, and its 001 / 002 split goes with nothing else
     (ending, city, kind, time) beyond dealing.
 P2  741 / 742 / 745 after 920-060 are spelling variants: they split by nothing (city, kind, ending, crest, time),
     and the same name never appears under two of them (no 'series').
 P3  368 after 817 (817-368 instead of 817-002) is a different slot that goes with tablets (Harappa heading 817-368-690).
Unit = copy events; dealt control = the slot label dealt among texts of the same front word and site.
"""
from front_common import *

say = make_logger('log_4_slots.txt')
rng = np.random.default_rng(4)
D = load(); F, *_ = front_set(D, say); D = add_parse(D, F)
E = copy_events(D[D.first_ok & (D.front != '') & (D.tok.map(len) >= 2)]).copy()
E = E[E.tok.map(lambda t: t[1] != '000' and t[1] != 'ALT')]
E['after'] = E.tok.map(lambda t: t[1])
E['after2'] = E.tok.map(lambda t: t[2] if len(t) > 2 else '(end)')

# ---------- stroke counts right after each front word
STROKES = {'001': 1, '002': 2, '003': 3, '004': 4, '005': 5, '016': 6, '017': 7, '013': 3, '014': 4, '015': 5,
           '031': 1, '032': 2, '033': 3, '034': 4, '035': 5, '036': 6}
rows = []
for f, g in E.groupby('front'):
    c = g.after.value_counts()
    strokes = {s: int(c.get(s, 0)) for s in STROKES if c.get(s, 0)}
    rows.append(dict(front=f, events=len(g), after_002=int(c.get('002', 0)), after_060=int(c.get('060', 0)),
                     other_stroke_counts='; '.join(f'{k}:{v}' for k, v in strokes.items() if k != '002'),
                     share_002_of_strokes=round(c.get('002', 0) / max(1, sum(strokes.values())), 3),
                     top_after='; '.join(f'{k} {v}' for k, v in c.head(8).items())))
ST = pd.DataFrame(rows).sort_values('events', ascending=False); ST.to_csv(f'{OUTF}/f4_strokes_after_front.csv', index=False)
say('\nSIGN RIGHT AFTER EACH FRONT WORD (copy events):'); say(ST.to_string(index=False))

# what follows 820-001, 820-002, 820-060 ... and their texts
for f in ('820', '692', '817', '861'):
    g = E[E.front == f]
    say(f'\n{f}: texts by sign after it (first 12 each)')
    for a, gg in g.groupby('after'):
        if len(gg) >= 2 or a in STROKES:
            say(f'  {f}-{a} ({len(gg)}): ' + ', '.join(gg.signs.head(12)))


def chi(a, b):
    t = pd.crosstab(a, b).values.astype(float)
    if t.shape[0] < 2 or t.shape[1] < 2: return 0.0
    e = t.sum(1, keepdims=True) * t.sum(0, keepdims=True) / t.sum()
    return float(((t - e) ** 2 / np.where(e > 0, e, 1)).sum())


def deal_test(sub, lab, attrs, tag):
    out = []
    for nm, vals, grp in attrs:
        ok = vals != ''
        s = sub[ok]; v = vals[ok]; g = grp[ok]
        if s[lab].nunique() < 2 or len(set(v)) < 2: continue
        o = chi(s[lab].values, v)
        null = [chi(deal_within(s[lab].values, g, rng), v) for _ in range(3000)]
        out.append(dict(test=tag, attribute=nm, n=len(s), chi2=round(o, 1), dealt_mean=round(np.mean(null), 1),
                        P=round(pval_hi(null, o), 4)))
        say(f'  [{tag}] {nm}: chi2 {o:.1f} against {np.mean(null):.1f}, P {pval_hi(null, o):.4f}, n {len(s)}')
    return out


def ecls(r):
    if r.is_count: return 'count'
    if '090' in r.ending: return 'man'
    if '400' in r.ending: return 'comb'
    if r.endstr.startswith('520'): return 'spear'
    if r.endstr == '740': return 'jar'
    return 'other'


E['ecls'] = [ecls(r) for r in E.itertuples()]
E['ccls'] = E.crest.map(lambda c: 'fish' if c in {'220', '231', '233', '240', '226', '222', '243', '235'} else ('-' if not c else 'other'))
res = []
# 820: 001 vs 002 vs 060
W = E[(E.front == '820') & E.after.isin(['001', '002', '060'])].copy()
say(f'\n820 slot split: {W.after.value_counts().to_dict()}')
attrs = lambda W: [('ending', W.ecls.values, W.site.values), ('object kind', W.kind.values, W.site.values),
                   ('city', W.site.where(W.site.isin(['Harappa', 'Mohenjo-daro']), 'other').values, W.kind.values),
                   ('time bin', W.bin.values, W.site.values), ('crest', W.ccls.where(W.ccls != '-', '').values, W.site.values),
                   ('length', W.L.clip(upper=7).astype(str).values, W.site.values)]
res += deal_test(W, 'after', attrs(W), '820: 001/002/060')
# 920-060-x: 741 / 742 / 745 / other
W = E[(E.front == '920') & (E.after == '060')].copy()
W['third'] = W.tok.map(lambda t: t[2] if len(t) > 2 else '(end)')
W['third'] = W.third.where(W.third.isin(['741', '742', '745']), 'other')
say(f'\n920-060 + third sign: {W.third.value_counts().to_dict()}')
res += deal_test(W, 'third', attrs(W), '920-060: 741/742/745/other')
# 817: 002 vs 368
W = E[(E.front == '817') & E.after.isin(['002', '368'])].copy()
say(f'\n817 slot split: {W.after.value_counts().to_dict()}; 817-368 texts: ' + ', '.join(W[W.after == '368'].signs))
res += deal_test(W, 'after', attrs(W), '817: 002/368')
pd.DataFrame(res).to_csv(f'{OUTF}/f4_slot_tests.csv', index=False)
for f in ('817', '861'):
    W = E[(E.front == f) & E.after.isin(['002', '368'])]
    say(f'{f}: slot x kind ' + str(pd.crosstab(W.after, W.kind).to_dict()))

# 741 742 745 everywhere: what precedes, what follows
for s in ('741', '742', '745'):
    prev = collections.Counter(); nxt = collections.Counter(); kinds = collections.Counter()
    for t, k in zip(D.tok, D.kind):
        for i, x in enumerate(t):
            if x == s:
                prev[t[i - 1] if i else '(start)'] += 1; nxt[t[i + 1] if i + 1 < len(t) else '(end)'] += 1; kinds[k] += 1
    say(f'\n{s}: before {prev.most_common(8)}; after {nxt.most_common(8)}; kinds {dict(kinds)}')

# ---------- same front and same name with different slot signs
rows = []
X = copy_events(D[D.complete & (D.front != '') & (D.name.map(len) > 0)])
X = X.assign(slotkey=X.slotstr.where(X.slotstr != '', '(none)'))
for (f, n), g in X.groupby(['front', 'namestr']):
    if g.slotkey.nunique() >= 2:
        for r in g.itertuples():
            rows.append(dict(front=f, name=n, slot=r.slotkey, text=r.signs, kind=r.kind, site=r.site, building=r.building,
                             bin=r.bin, animal=r.animal, cisi=r.cisi))
# the same name under 741, 742, 745 regardless of front
for n, g in X[X.slotstr.str.contains('741|742|745')].groupby('namestr'):
    pass
C = pd.DataFrame(rows); C.to_csv(f'{OUTF}/f4_same_front_name_diff_slot.csv', index=False)
say(f'\nSAME FRONT + SAME NAME, DIFFERENT SLOT: {C.groupby(["front", "name"]).ngroups if len(C) else 0} cases')
if len(C): say(C.to_string(index=False))
# control: how many (front,name) groups with 2+ texts exist, and how many would differ in slot if slots were dealt within front+site
G = X.groupby(['front', 'namestr']).filter(lambda g: len(g) >= 2)
def ndiff(sl):
    return int(pd.DataFrame({'k': G.front + '|' + G.namestr, 's': sl}).groupby('k').s.nunique().gt(1).sum())
ob = ndiff(G.slotkey.values)
null = [ndiff(deal_within(G.slotkey.values, (G.front + '|' + G.site).values, rng)) for _ in range(2000)]
say(f'(front, name) groups with 2+ copy events: {G.groupby(["front", "namestr"]).ngroups}; with a slot difference {ob} '
    f'against {np.mean(null):.2f} with slots dealt within front word and site (P low {pval_lo(null, ob):.4f}, P high {pval_hi(null, ob):.4f})')
# same name, slot 741 vs 742 vs 745 anywhere
Y = copy_events(D[D.complete])
names_by_slot = collections.defaultdict(set)
for t in Y.tok:
    for i, x in enumerate(t):
        if x in ('741', '742', '745') and i + 1 < len(t):
            rest = t[i + 1:]
            j = len(rest)
            while j > 0 and (rest[j - 1] in CLOSERS or rest[j - 1] in TITLES): j -= 1
            if j: names_by_slot['-'.join(rest[:j])].add(x)
multi = {n: s for n, s in names_by_slot.items() if len(s) >= 2}
say(f'\nnames standing after 741/742/745 (anywhere): {len(names_by_slot)}; under two or more of them: {len(multi)} {multi}')
