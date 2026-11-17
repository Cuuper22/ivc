#!/usr/bin/env python3
"""Sign list steps 5-7: the inventory after merging, its growth, and the true sign table. Rules fixed before any number:

GROUPS: the rule-v2 merge groups (merge_groups.csv) plus rare signs (< 5 uses) attached to a partner through a form-only
  link (merge_rare_formonly.csv: same shape code or description overlap >= 0.6 AND a shared Mahadevan number); a rare sign
  joins its partner's group (or the partner itself). Every other catalogue sign is its own true sign.
  The catalogue = every Lipi number used in the first catalogue plus every number in the shape list.
COUNTS: uses over first-catalogue copy events (identical moulded batches once).
INVENTORY: signs in use, used once, used <= 5 times; how many signs cover 50 / 80 / 95% of uses; share of uses covered by
  the top 50 and top 100 signs; Chao1 estimate of the full list (observed + f1^2 / (2 f2); f1 = signs used once, f2 =
  twice). The same figures for the raw catalogue (no merging) and the second catalogue's own numbering.
GROWTH (step 6): copy events in random order, 300 orders; distinct true signs after each 1% of events; new signs found in the
  last 10% of events (mean over orders); Heaps exponent = slope of log(distinct signs) on log(tokens) over the second half.
  Per frame-v2 class (a true sign takes the class of its most-used member; unclassed signs count as PERSONAL, as frame v2
  does): the same curve on that class's tokens.
  CLOSED class: mean new signs in the last 10% of events < 1.0 AND Chao1 <= 1.1 x observed. Otherwise OPEN.
  SECOND SCHEME (added after the first run, because frame v2 names its small classes as fixed sign sets and files every
  other sign under PERSONAL, so 'closed' is partly built in): the machine's 10-state classes learned from sign order alone
  (work_data/frame/classes.csv, hmm10_implied_job), which give every sign, rare ones included, a class.
Outputs: work_data/signlist/true_signs.csv, inventory.csv, growth.csv, growth_by_class.csv, log_inventory.txt
"""
from signlist_common import *

say = logger('inventory')
L = load_lipi(); U = uses(L); SH = shapes(); CL = v2classes()
G = pd.read_csv(f'{OUT}/merge_groups.csv', dtype=str)
R = pd.read_csv(f'{OUT}/merge_rare_formonly.csv', dtype=str)
MP = pd.read_csv(f'{OUT}/merge_pairs.csv', dtype={'a': str, 'b': str})
catalogue = sorted(set(U) | set(SH))
group = {s: s for s in catalogue}; evidence = {s: '' for s in catalogue}
for r in G.itertuples():
    for m in r.members.split('|'):
        group[m] = r.group
    for a, b, c, sf in zip(MP.a, MP.b, MP.combo, MP.swap_frames):
        if a in r.members.split('|'):
            for x in (a, b): evidence[x] += f'{a}-{b}[{c}; swap frames {sf}] '
# rare links: strongest partner = the most used
for rare, g in R.groupby('rare'):
    p = max(g.partner, key=lambda s: U.get(s, 0))
    group[rare] = group[p]
    evidence[rare] += f'form-only: same drawing as {p} and one Mahadevan number ({g[g.partner == p].mahadevan.iloc[0]}) '
# resolve chains
for s in catalogue:
    seen = set()
    while group[s] != s and group[group[s]] != group[s] and group[s] not in seen:
        seen.add(group[s]); group[s] = group[group[s]]
members = collections.defaultdict(list)
for s in catalogue: members[group[s]].append(s)
tc = collections.Counter()
for s in catalogue: tc[group[s]] += U.get(s, 0)
tclass = {}
for g, ms in members.items():
    top = max(ms, key=lambda s: U.get(s, 0)); tclass[g] = CL.get(top, 'PERSONAL') or 'PERSONAL'

SPL = pd.read_csv(f'{OUT}/splits_clean.csv', dtype={'sign': str}) if os.path.exists(f'{OUT}/splits_clean.csv') else pd.DataFrame(columns=['sign', 'behaves_as_two'])
split = dict(zip(SPL.sign, SPL.behaves_as_two))
MF = pd.read_csv(f'{OUT}/mark_families.csv', dtype=str)
markof = {c: f'{b} + {t}' for c, b, t in zip(MF.compound, MF.base, MF.mark_type)}
X = crosswalk(); X = X.sort_values('share', ascending=False)
mah = X.groupby('lipi').apply(lambda t: '|'.join(f'{m}({s:.2f})' for m, s in zip(t.mahadevan, t.share)))
rows = []
for s in catalogue:
    rows.append(dict(sign=s, true_sign=group[s], group_members='|'.join(sorted(members[group[s]])), uses=U.get(s, 0),
                     true_sign_uses=tc[group[s]], v2_class=CL.get(s, ''), true_sign_class=tclass[group[s]],
                     merge_evidence=evidence[s].strip(), compound_of=markof.get(s, ''), behaves_as_two=split.get(s, ''),
                     shape_code=SH.get(s, ('', ''))[0], shape=SH.get(s, ('', ''))[1], mahadevan=mah.get(s, '')))
T = pd.DataFrame(rows); T.to_csv(f'{ROOT}/work_data/signlist/true_signs.csv', index=False)

def inv(counts, label):
    c = np.array(sorted([v for v in counts.values() if v > 0], reverse=True)); tot = c.sum(); cum = np.cumsum(c) / tot
    f1 = int((c == 1).sum()); f2 = int((c == 2).sum())
    d = dict(list=label, signs_in_use=len(c), uses=int(tot), used_once=f1, used_le5=int((c <= 5).sum()),
             cover50=int(np.searchsorted(cum, 0.5) + 1), cover80=int(np.searchsorted(cum, 0.8) + 1), cover95=int(np.searchsorted(cum, 0.95) + 1),
             top50_share=round(float(cum[49]), 3), top100_share=round(float(cum[99]), 3), chao1=round(len(c) + f1 * f1 / (2 * max(f2, 1)), 1))
    say(f'{label}: ' + ', '.join(f'{k} {v}' for k, v in d.items() if k != 'list')); return d
Mm = load_mahadevan('mah'); Um = uses(Mm)
I = [inv({s: U[s] for s in U}, 'first catalogue, raw numbers'), inv(dict(tc), 'first catalogue, true signs (after merging)'),
     inv(dict(Um), 'second catalogue, its own numbers')]
pd.DataFrame(I).to_csv(f'{OUT}/inventory.csv', index=False)
say(f'catalogue numbers: {len(catalogue)} ({sum(1 for s in catalogue if U.get(s, 0))} in use); true signs: {len(members)} '
    f'({sum(1 for g in members if tc[g])} in use)')

# ---------------- growth ----------------
CM = pd.read_csv(f'{ROOT}/work_data/frame/classes.csv', dtype=str).fillna('')
HM = dict(zip(CM.sign, CM.hmm10_implied_job))
tclass_h = {}
for g, ms in members.items():
    top = max(ms, key=lambda s: U.get(s, 0)); tclass_h[g] = HM.get(top, '') or 'none'
ev_tok = [[group[s] for f in e['faces'] for s in f if is_sign(s)] for e in L]
n = len(ev_tok)
CK = np.unique(np.linspace(1, n, 101).astype(int)); i90 = int(np.searchsorted(CK, int(0.9 * n)))
def heaps(cv, tk):
    h = len(CK) // 2; x = np.log(np.maximum(tk.mean(0)[h:], 1)); y = np.log(np.maximum(cv.mean(0)[h:], 1))
    if np.ptp(x) == 0: return float('nan')
    return float(np.polyfit(x, y, 1)[0])
GC = []
for scheme, TCL in (('frame v2', tclass), ('machine hmm10', tclass_h)):
    rng = np.random.default_rng(2026)
    classes = sorted(set(TCL.values()))
    curve = np.zeros((300, len(CK))); ctok = np.zeros((300, len(CK)))
    ccurve = {c: np.zeros((300, len(CK))) for c in classes}; ctoks = {c: np.zeros((300, len(CK))) for c in classes}
    for r in range(300):
        bar(r, 300, f'growth orders, {scheme}', every=100)
        order = rng.permutation(n); seen = set(); seenc = collections.defaultdict(set); t = 0; tcn = collections.Counter(); j = 0
        for i, ei in enumerate(order, 1):
            for g in ev_tok[ei]:
                seen.add(g); seenc[TCL[g]].add(g); t += 1; tcn[TCL[g]] += 1
            if j < len(CK) and i == CK[j]:
                curve[r, j] = len(seen); ctok[r, j] = t
                for c in classes: ccurve[c][r, j] = len(seenc[c]); ctoks[c][r, j] = tcn[c]
                j += 1
    if scheme == 'frame v2':
        pd.DataFrame(dict(events=CK, tokens=ctok.mean(0).round(1), distinct_mean=curve.mean(0).round(2), distinct_p5=np.percentile(curve, 5, 0),
                          distinct_p95=np.percentile(curve, 95, 0))).to_csv(f'{OUT}/growth.csv', index=False)
        say(f'all signs: {curve.mean(0)[-1]:.0f} at the end; new in the last 10% of texts {curve.mean(0)[-1] - curve.mean(0)[i90]:.2f}; '
            f'at 50% of texts {curve.mean(0)[50]:.1f}; at 25% {curve.mean(0)[25]:.1f}; Heaps exponent {heaps(curve, ctok):.3f}')
    say(f'classes, scheme {scheme}:')
    for c in classes:
        cv = ccurve[c]; obs = cv.mean(0)[-1]; last = obs - cv.mean(0)[i90]
        cnts = collections.Counter({g: tc[g] for g in members if TCL[g] == c and tc[g]})
        f1 = sum(1 for v in cnts.values() if v == 1); f2 = sum(1 for v in cnts.values() if v == 2)
        chao = obs + f1 * f1 / (2 * max(f2, 1))
        closed = last < 1.0 and chao <= 1.1 * obs
        toks = sum(cnts.values())
        top = ' '.join(g for g, _ in cnts.most_common(6))
        GC.append(dict(scheme=scheme, cls=c, signs=int(round(obs)), tokens=toks, used_once=f1, new_in_last_10pct=round(last, 2),
                       half_way=round(cv.mean(0)[50], 1), chao1=round(chao, 1), heaps=round(heaps(cv, ctoks[c]), 3),
                       verdict='closed' if closed else 'open', commonest=top))
        say(f'   {c}: {obs:.0f} signs, {toks} uses, used once {f1}, new in last 10% {last:.2f}, half-way {cv.mean(0)[50]:.1f}, Chao1 {chao:.1f}, '
            f'Heaps {heaps(cv, ctoks[c]):.3f} -> {"CLOSED" if closed else "open"}  [{top}]')
pd.DataFrame(GC).to_csv(f'{OUT}/growth_by_class.csv', index=False)

# ---------------- slots: how often a rare sign fills each place (added after the class runs, rule fixed here) ----------
# A place in a text is named by its known neighbour: the slot right after a front word (OPEN / SLOT sign), after a number,
# right before a closer (740 520 151 154 155 158), right after a closer, text start, text end; neighbours must be signs with
# 50+ uses (their job is known). For each place: share of the signs standing there that are RARE true signs (5 or fewer
# uses) and that are used ONCE. Chance line = the same shares over all sign uses. Unbroken faces only for start / end.
NUMS = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}
def place_tags(f, br, i):
    tags = []
    if i == 0 and not br: tags.append('text start')
    if i == len(f) - 1 and not br: tags.append('text end')
    if i > 0 and is_sign(f[i - 1]) and U.get(f[i - 1], 0) >= 50:
        c = CL.get(f[i - 1], '')
        if c in ('OPEN', 'SLOT'): tags.append('after a front word or its slot')
        if c in NUMS: tags.append('after a number')
        if c == 'CLOSER': tags.append('after a closer')
        if c == 'CREST': tags.append('after a crest')
    if i < len(f) - 1 and is_sign(f[i + 1]) and U.get(f[i + 1], 0) >= 50:
        c = CL.get(f[i + 1], '')
        if c == 'CLOSER': tags.append('before a closer')
        if c in NUMS: tags.append('before a number')
        if c == 'THING': tags.append('before a counted thing')
    return tags
slot = collections.defaultdict(lambda: [0, 0, 0])
for e in L:
    for f, br in zip(e['faces'], e['broken']):
        for i, s in enumerate(f):
            if not is_sign(s): continue
            g = group[s]; rare = tc[g] <= 5; once = tc[g] == 1
            for t in place_tags(f, br, i) + ['all uses']:
                slot[t][0] += 1; slot[t][1] += rare; slot[t][2] += once
SL = pd.DataFrame([dict(place=t, uses=v[0], rare_share=round(v[1] / v[0], 4), once_share=round(v[2] / v[0], 4)) for t, v in slot.items()]).sort_values('rare_share')
SL.to_csv(f'{OUT}/slot_openness.csv', index=False)
say('places in the text: share of rare (<=5 uses) and once-used signs standing there')
for r in SL.itertuples(): say(f'   {r.place}: {r.uses} uses, rare {r.rare_share:.2%}, used once {r.once_share:.2%}')

# event token lists in true signs, for the size-matched yardsticks (signlist_6_yardsticks.py)
with open(f'{OUT}/indus_true_tokens.txt', 'w') as fh:
    for t in ev_tok:
        if t: fh.write(' '.join(t) + '\n')
