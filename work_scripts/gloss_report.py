#!/usr/bin/env python3
"""Coverage + world tests + 40 glosses for gloss.py.  Writes jobs/out/gloss_report.md.  Runs in seconds."""
import sys, collections, math, re
sys.path.insert(0, '/home/claude/ivc/work_scripts')
import numpy as np, pandas as pd
from scipy import stats
from gloss import *

rng = np.random.default_rng(7)
d = load(); lex = lexicon_from(d)
d['roles'] = [gloss_text(x, lex, f) for x, f in zip(d.tok, d.flg)]
d['parsed'] = [is_parsed(r) for r in d.roles]
TEMPLATE = {'opener', 'opener-strokes', 'count', 'amount', 'class', 'class-tail', 'house', 'title-phrase', 'cap', 'cap-selector'}


def tight(r):
    return ('unknown' not in r and r.count('who') <= 2 and sum(q in TEMPLATE or q in ('house-marker',) for q in r) >= 0.5 * len(r))


d['tight'] = [tight(r) for r in d.roles]
L = []
P = L.append
C = d[d.complete_txt].drop_duplicates(['tok', 'group']).copy()          # distinct complete texts per object type
Cu = d[d.complete_txt].drop_duplicates(['tok'])                          # distinct complete texts overall
P('# Gloss report: sign-by-sign parse of the Indus corpus\n')
P('Reading order = stored order reversed. A text is complete when it has no broken edge, no lost sign (000) and no ambiguous sign.')
P('Roles: opener, opener-strokes, count, amount, who, house, house-marker, class, class-tail, title-phrase, cap, cap-selector, plus roles learned from the data (head, second-slot, counted-thing, fixed-ending, phrase, mark). "Fully parsed" = every sign gets a role. "Tight" = fully parsed with at most 2 who-signs and at least half the signs in template roles.\n')
P('## 1. Coverage\n')
tot_rows = len(d)
P(f'Rows {tot_rows}; distinct complete texts {len(Cu)} ({len(C)} counting each object type separately). Fully parsed: {int(Cu.parsed.sum())} of {len(Cu)} ({Cu.parsed.mean()*100:.1f}%). Tight: {int(Cu.tight.sum())} ({Cu.tight.mean()*100:.1f}%). All rows incl. broken/lost texts: {int(d.parsed.sum())} of {tot_rows} parse ({d.parsed.mean()*100:.1f}%).\n')
P('### By object type (distinct complete texts)\n')
P('| type | texts | fully parsed | % | tight | % |\n|---|---|---|---|---|---|')
for g, s in C.groupby('group'):
    P(f'| {g} | {len(s)} | {int(s.parsed.sum())} | {s.parsed.mean()*100:.1f} | {int(s.tight.sum())} | {s.tight.mean()*100:.1f} |')
P('\n### By raw type code\n')
P('| type | texts | fully parsed | % | tight % |\n|---|---|---|---|---|')
for g, s in C.groupby('type'):
    if len(s) >= 15: P(f'| {g} | {len(s)} | {int(s.parsed.sum())} | {s.parsed.mean()*100:.1f} | {s.tight.mean()*100:.1f} |')
P('\n### By site (distinct complete texts)\n')
P('| site | texts | fully parsed | % | tight % |\n|---|---|---|---|---|')
for g, s in C.drop_duplicates(['tok', 'site']).groupby('site'):
    if len(s) >= 10: P(f'| {g} | {len(s)} | {int(s.parsed.sum())} | {s.parsed.mean()*100:.1f} | {s.tight.mean()*100:.1f} |')
# blockers
U = Cu[~Cu.parsed]
bl = collections.Counter(s for x, r in zip(U.tok, U.roles) for s, q in zip(x, r) if q == 'unknown')
P(f'\n### Signs that block a full parse ({len(U)} unparsed distinct complete texts)\n')
P('Block = the sign has no role in an unparsed text (texts of 3+ signs with no anchor sign). Count = unparsed texts it sits in. Shape from sign_shapes.csv.\n')
sh = pd.read_csv(SHAPES, dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
P('| sign | texts blocked | shape |\n|---|---|---|')
for s, k in bl.most_common(15): P(f'| {s} | {k} | {sh.get(s, "?")[:70]} |')
P(f'\nLength of unparsed texts: ' + ', '.join(f'{k} signs: {v}' for k, v in sorted(collections.Counter(len(x) for x in U.tok).items())) + '.')
# token-level role shares
rc = collections.Counter(q for r in Cu.roles for q in r)
tt = sum(rc.values())
P('\n### Share of all sign tokens by role (distinct complete texts)\n')
P(', '.join(f'{k} {v/tt*100:.1f}%' for k, v in rc.most_common()) + '.')

# held-out
P('\n### Held-out check: lexicon learned without the test site\n')
P('| test set | lexicon from | texts | fully parsed % | tight % |\n|---|---|---|---|---|')
def ev(testsite, label):
    te = d[d.complete_txt & (d.site == testsite)].drop_duplicates('tok')
    trn = d[d.complete_txt & (d.site != testsite)].drop_duplicates('tok')
    for nm, lx in (('other sites', Lexicon(list(trn.tok))), ('nothing (template only)', Lexicon([]))):
        rr = [gloss_text(x, lx) for x in te.tok]
        P(f'| {testsite} | {nm} | {len(te)} | {np.mean([is_parsed(r) for r in rr])*100:.1f} | {np.mean([tight(r) for r in rr])*100:.1f} |')
for s in ('Mohenjo-daro', 'Harappa', 'Dholavira', 'Lothal'): ev(s, s)

# top-100 signs
P('\n## 2. Role of the 100 most common signs\n')
P('Role = most common role of the sign over all rows (all texts, reading order); share = fraction of its occurrences in that role. Shape from the catalogue.\n')
sc = collections.Counter(s for x in d.tok for s in x if s not in ('000', 'ALT'))
role_of = collections.defaultdict(collections.Counter)
for x, r in zip(d.tok, d.roles):
    for s, q in zip(x, r): role_of[s][q] += 1
P('| rank | sign | n | main role | share | second role | shape |\n|---|---|---|---|---|---|---|')
for i, (s, n) in enumerate(sc.most_common(100), 1):
    m = role_of[s].most_common(2)
    sec = f'{m[1][0]} {m[1][1]/n*100:.0f}%' if len(m) > 1 else ''
    P(f'| {i} | {s} | {n} | {m[0][0]} | {m[0][1]/n*100:.0f}% | {sec} | {sh.get(s, "?")[:55]} |')

# ---------- world tests
P('\n## 3. What the parse says about the world\n')
# role tokens per row
def slot_signs(x, r, role): return [s for s, q in zip(x, r) if q == role]
d['house_sign'] = [(slot_signs(x, r, 'house') or [None])[0] for x, r in zip(d.tok, d.roles)]
d['class_sign'] = [(slot_signs(x, r, 'class') or [None])[-1] for x, r in zip(d.tok, d.roles)]
bad = lambda v: v in ('', '--', '-')
mo = d[(d.site == 'Mohenjo-daro') & d.complete_txt & d.house_sign.notna() & (d.group == 'seal')].copy()
P('### 3a. Does the house sign repeat inside excavation houses at Mohenjo-daro?\n')
P(f'Mohenjo-daro seals with a complete text and a house sign: {len(mo)}.\n')
P('| excavation unit | seals with unit | distinct units | same-unit pairs | pairs sharing the house sign | by shuffling (mean) | ratio | p |\n|---|---|---|---|---|---|---|---|')
def pair_test(df, unitcols, label, extra_sign='house_sign', nperm=3000):
    df = df[[not any(bad(r[c]) for c in unitcols) for _, r in df.iterrows()]].copy()
    df['unit'] = df[unitcols].agg('|'.join, axis=1)
    df = df.drop_duplicates(['unit', 'reading'] if 'reading' in df else ['unit', 'tok'])
    sg = df[extra_sign].values; un = df.unit.values
    def stat(u):
        t = pd.DataFrame({'u': u, 's': sg})
        ng = t.groupby(['u', 's']).size()
        return int((ng * (ng - 1) // 2).sum())
    nu = pd.Series(un).value_counts()
    pairs = int((nu * (nu - 1) // 2).sum())
    obs = stat(un)
    null = np.array([stat(rng.permutation(un)) for _ in range(nperm)])
    p = (np.sum(null >= obs) + 1) / (nperm + 1)
    P(f'| {label} | {len(df)} | {len(nu)} | {pairs} | {obs} | {null.mean():.1f} | {obs/max(null.mean(),1e-9):.2f} | {p:.4f} |')
    return df
pair_test(mo, ['area-section', 'block-house'], 'area-section + block-house')
pair_test(mo, ['area-section', 'block-house', 'room-grid'], 'area-section + block-house + room-grid')
pair_test(mo, ['block-house'], 'block-house alone')
mo2 = mo.copy()
mo2['whoset'] = [tuple(sorted(set(slot_signs(x, r, 'who')))) for x, r in zip(mo2.tok, mo2.roles)]
mo2['who1'] = [(slot_signs(x, r, 'who') or [None])[-1] for x, r in zip(mo2.tok, mo2.roles)]
P('\nControl: the same test on the last who-sign instead of the house sign, then on the class sign.\n')
P('| excavation unit | seals | units | same-unit pairs | pairs sharing | shuffle mean | ratio | p |\n|---|---|---|---|---|---|---|---|')
mw = mo2[mo2.who1.notna()]
pair_test(mw, ['area-section', 'block-house'], 'who-sign, area-section + block-house', 'who1')
pair_test(mo2, ['area-section', 'block-house'], 'class sign, area-section + block-house', 'class_sign')
P('\nRescue tests for the house slot (the first attempt above is null).\n')
P('| variant | seals | units | same-unit pairs | pairs sharing | shuffle mean | ratio | p |\n|---|---|---|---|---|---|---|---|')
def adj(x, r):
    for i in range(len(x) - 1, 0, -1):
        if r[i] in ('class', 'class-tail'): return x[i - 1]
    return None
mo2['adjsign'] = [adj(x, r) for x, r in zip(mo2.tok, mo2.roles)]
pair_test(mo2[mo2.adjsign.notna()], ['area-section', 'block-house'], 'sign directly before the class (markers not skipped)', 'adjsign')
mj = mo2[[r.class_sign == '740' for _, r in mo2.iterrows()]]
pair_test(mj, ['area-section', 'block-house'], 'jar-closed seals only, house sign', 'house_sign')
rare = {k for k, v in sc.items() if v <= 100}
mo2['rare_mid'] = [tuple(sorted({s_ for s_, q in zip(x, r) if q in ('who', 'house', 'house-marker') and s_ in rare})) for x, r in zip(mo2.tok, mo2.roles)]
mo2['rm'] = [t_ if t_ else None for t_ in mo2.rare_mid]
def share_test(df, cols, label, nperm=3000):
    df = df[[not any(bad(r[c]) for c in cols) for _, r in df.iterrows()]].copy()
    df['unit'] = df[cols].agg('|'.join, axis=1)
    df = df.drop_duplicates(['unit', 'tok'])
    sets = [set(v) for v in df.rm.fillna('').map(lambda t_: t_ if t_ else ())]
    un = df.unit.values
    def stat(u):
        g = collections.defaultdict(list)
        for i_, k_ in enumerate(u): g[k_].append(i_)
        c_ = 0
        for ids in g.values():
            for a_ in range(len(ids)):
                for b_ in range(a_ + 1, len(ids)):
                    if sets[ids[a_]] & sets[ids[b_]]: c_ += 1
        return c_
    nu = pd.Series(un).value_counts(); pairs = int((nu * (nu - 1) // 2).sum())
    obs = stat(un); null = np.array([stat(rng.permutation(un)) for _ in range(nperm)])
    P(f'| {label} | {len(df)} | {len(nu)} | {pairs} | {obs} | {null.mean():.1f} | {obs/max(null.mean(),1e-9):.2f} | {(np.sum(null>=obs)+1)/(nperm+1):.4f} |')
share_test(mo2, ['area-section', 'block-house'], 'any shared rare sign (<=100 uses) in who+house+marker slots')
share_test(mo2, ['area-section', 'block-house', 'room-grid'], 'any shared rare sign in who+house+marker, down to room')
# top repeated houses inside units
dfu = mo[[not any(bad(r[c]) for c in ['area-section', 'block-house']) for _, r in mo.iterrows()]].copy()
dfu['unit'] = dfu['area-section'] + ' / ' + dfu['block-house']
rep = dfu.groupby(['unit', 'house_sign']).agg(n=('cisi', 'size'), objs=('cisi', lambda v: ', '.join(list(v)[:5]))).reset_index()
rep = rep[rep.n >= 2].sort_values('n', ascending=False)
P(f'\nHouse sign appears 2+ times in one unit: {len(rep)} unit/sign cells. Largest:\n')
P('| unit | house sign | seals | examples |\n|---|---|---|---|')
for _, r in rep.head(12).iterrows(): P(f'| {r.unit} | {r.house_sign} | {r.n} | {r.objs} |')

# ---- class vs size / animal / material
P('\n### 3b. Does the class go with seal size, animal and material?\n')
sd = d[(d.group == 'seal') & d.class_sign.notna() & d.complete_txt].drop_duplicates(['cisi', 'tok']).copy()
sd['h'] = pd.to_numeric(sd['horizontal(mm)'], errors='coerce'); sd['v'] = pd.to_numeric(sd['vertical(mm)'], errors='coerce')
sd['area'] = sd.h * sd.v
sd['animal'] = sd.symbol.str.split(':').str[0].replace({'': 'none', '-': 'none'})
cls_names = {'740': 'jar 740', '520': 'spear 520', '090': 'person 090', '400': 'comb 400', '151': 'carrier 151', '154': 'carrier 154', '156': 'carrier 156', '158': 'carrier 158'}
top = sd.class_sign.value_counts()
P(f'Seals with a class sign: {len(sd)}; distinct class signs {sd.class_sign.nunique()}; top 8 cover {top.head(8).sum()/len(sd)*100:.1f}%.\n')
P('| class | seals | median area mm2 | median wide mm | median high mm | share with no animal | top animal |\n|---|---|---|---|---|---|---|')
for c, n in top.head(10).items():
    s = sd[sd.class_sign == c]; a = s.area[s.area > 0]
    P(f'| {cls_names.get(c, c)} | {n} | {a.median():.0f} | {s.h[s.h>0].median():.1f} | {s.v[s.v>0].median():.1f} | {(s.animal=="none").mean()*100:.0f}% | {s.animal.value_counts().index[0]} ({s.animal.value_counts().iloc[0]}) |')
big = sd[sd.class_sign.isin(top.head(6).index)]
ar = big[big.area > 0]
kw = stats.kruskal(*[g.area.values for _, g in ar.groupby('class_sign') if len(g) > 5])
P(f'\nSeal area by class (top 6 classes, {len(ar)} seals): Kruskal-Wallis H = {kw.statistic:.1f}, p = {kw.pvalue:.2g}. Direction: classes differ in size; order above.')
def cramer(a, b, nperm=2000):
    ct = pd.crosstab(a, b); chi = stats.chi2_contingency(ct, correction=False)[0]
    v = math.sqrt(chi / (ct.values.sum() * (min(ct.shape) - 1)))
    nl = []
    for _ in range(nperm):
        c2 = stats.chi2_contingency(pd.crosstab(a.values, rng.permutation(b.values)), correction=False)[0]; nl.append(c2)
    return v, (np.sum(np.array(nl) >= chi) + 1) / (nperm + 1)
for col, lab in (('animal', 'animal'), ('material', 'material'), ('site', 'site')):
    s = big[big[col].isin(big[col].value_counts().head(8).index)]
    s = s[~s[col].isin(['', '-'])] if col != 'animal' else s
    v, p = cramer(s.class_sign, s[col])
    P(f'Class x {lab} ({len(s)} seals): Cramer V = {v:.3f}, permutation p = {p:.4f}.')
# closer share by animal / material
P('\nClass share by animal (top 6 animals; each row sums to 100% over the top 6 classes):\n')
ct = pd.crosstab(big.animal, big.class_sign); ct = ct.loc[ct.sum(1).sort_values(ascending=False).head(7).index]
P('| animal | n | ' + ' | '.join(cls_names.get(c, c) for c in ct.columns) + ' |\n|---|---|' + '---|' * len(ct.columns))
for a, r in ct.iterrows(): P(f'| {a} | {r.sum()} | ' + ' | '.join(f'{v/r.sum()*100:.0f}%' for v in r) + ' |')
P('\nClass share by material:\n')
ct = pd.crosstab(big.material.replace({'': 'unknown', '-': 'unknown'}), big.class_sign); ct = ct.loc[ct.sum(1).sort_values(ascending=False).head(5).index]
P('| material | n | ' + ' | '.join(cls_names.get(c, c) for c in ct.columns) + ' |\n|---|---|' + '---|' * len(ct.columns))
for a, r in ct.iterrows(): P(f'| {a} | {r.sum()} | ' + ' | '.join(f'{v/r.sum()*100:.0f}%' for v in r) + ' |')

# ---- name-likeness
P('\n### 3c. Do who-slots look like names and class like a closed set?\n')
S = Cu[Cu.group == 'seal']
def slot_stats(role, last_only=False):
    v = []
    for x, r in zip(S.tok, S.roles):
        ss = slot_signs(x, r, role)
        if ss: v += ss
    c = collections.Counter(v); n = len(v)
    hap = sum(1 for k, q in c.items() if q == 1)
    ent = -sum(q / n * math.log2(q / n) for q in c.values())
    return n, len(c), hap, sum(q for _, q in c.most_common(8)) / n, ent
P('Seal texts only, distinct complete texts. Tokens = slot fillings; types = distinct signs; singletons = signs seen once in the slot; top-8 = share of tokens held by the 8 commonest signs; entropy in bits.\n')
P('| slot | tokens | types | types/tokens | singleton types | top-8 share | entropy (bits) |\n|---|---|---|---|---|---|---|')
for role in ('who', 'house', 'class', 'count', 'opener'):
    n, k, h, t8, e = slot_stats(role)
    P(f'| {role} | {n} | {k} | {k/n:.3f} | {h} | {t8*100:.0f}% | {e:.2f} |')
# who-sign order effects: first who vs last who
wf = collections.Counter(); wl = collections.Counter()
for x, r in zip(S.tok, S.roles):
    w = slot_signs(x, r, 'who')
    if w: wf[w[0]] += 1; wl[w[-1]] += 1
P(f'\nFirst who-sign: {len(wf)} distinct over {sum(wf.values())} seals, top-8 {sum(q for _, q in wf.most_common(8))/sum(wf.values())*100:.0f}%. Last who-sign (next to the house): {len(wl)} distinct, top-8 {sum(q for _, q in wl.most_common(8))/sum(wl.values())*100:.0f}%.')

# ---------- 40 texts
P('\n## 4. The 40 most completely glossed texts\n')
P('Chosen from distinct complete texts of 3+ signs, fully parsed, at most 1 who-sign, scored by number of distinct template roles used; each role string used once; title-phrase texts are favoured.\n')
def count_val(s): return int(s[-1])
cls_words = {'740': 'jar class', '520': 'spear class', '090': 'person class', '400': 'comb class', '151': 'carrier class', '154': 'carrier class', '156': 'carrier class', '158': 'carrier class'}
def short(s):
    t = sh.get(s, 'unlisted sign')
    return t if len(t) <= 48 else t[:46] + '..'
def plain(x, r):
    out = []
    skip = set()
    for i_ in range(len(x) - 2):
        if r[i_] == 'title-phrase' and r[i_ + 1] == 'title-phrase' and x[i_] in A_VARIANTS: skip |= {i_, i_ + 1, i_ + 2}
    tdone = set()
    for i_, (s, q) in enumerate(zip(x, r)):
        if i_ in skip:
            if x[i_] in A_VARIANTS: out.append(f'carrier title, grade {s}')
            continue
        if q == 'opener': out.append('opening mark')
        elif q == 'opener-strokes': out.append('two')
        elif q == 'count': out.append(f'count {count_val(s)}')
        elif q == 'amount': out.append('amount' if s == '700' else f'{count_val(s)}')
        elif q == 'who': out.append(f'person {s}')
        elif q == 'house': out.append(f'house {s}')
        elif q == 'house-marker': out.append(f'house marker {s}')
        elif q in ('class', 'class-tail'): out.append(cls_words.get(s, f'class {s}'))
        elif q == 'cap': out.append('cap ' + s)
        elif q == 'cap-selector': out.append('cap selector ' + s)
        elif q == 'title-phrase': out.append(f'grade {s}' if s in A_VARIANTS else ('carrier' if s in ('154', '158') else 'leaf-on-tree'))
        else: out.append(f'{q} {s}')
    # merge title phrase
    return ' / '.join(out)
cand = Cu[Cu.parsed & (Cu.tok.map(len) >= 3) & (Cu.cisi != '')].copy()
cand['nw'] = [r.count('who') for r in cand.roles]
cand = cand[cand.nw <= 1]
cand['score'] = [len(set(r) & TEMPLATE) * 10 + sum(q in TEMPLATE for q in r) - 3 * r.count('who') - 5 * sum(q in ('phrase', 'head', 'second-slot', 'counted-thing', 'fixed-ending', 'mark') for q in r) for r in cand.roles]
cand['score'] += [30 * ('title-phrase' in r) for r in cand.roles]
cand = cand.sort_values('score', ascending=False)
seen = collections.Counter(); picked = []
for _, row in cand.iterrows():
    key = ' '.join(row.roles)
    if seen[key] >= 1: continue
    seen[key] += 1; picked.append(row)
    if len(picked) == 40: break
for row in picked:
    parts = [f'[{short(s)}, sign {s}] ({q})' for s, q in zip(row.tok, row.roles)]
    P(f'**{row.cisi}** ({row.site}, {row.type}) reading order `{"-".join(row.tok)}`  ')
    P(' '.join(parts) + f'  \n= "{plain(row.tok, row.roles)}"\n')

open('/home/claude/ivc/jobs/out/gloss_report.md', 'w').write('\n'.join(L))
print('\n'.join(L[:60]))
