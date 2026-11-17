#!/usr/bin/env python3
"""FRONT job 9: the slot sign as the END of a front field.  2026-11-17.

Seen while running front_7/8 (written down here before the numbers below): long 'frontless' seal texts often carry a
slot sign (060 741 742 745 368 365) at position 2 to 4: 500-741-..., 390-741-..., 634-368-..., 317-920-002-...,
416-861-002-...  Idea: the slot sign closes a FRONT FIELD, and the field can hold a classic front word, a front word
with a sign before it, or some other sign or pair.  A text = [front field] [slot] [name] [ending].

Definitions: a SLOT BOUNDARY text = a complete text with a slot sign (060 741 742 745 368 365; 002 only when the sign
before it is a front word) at position 1, 2 or 3 (0-based), with at least one sign after it.  Field = signs before it.
Field types: 'classic' (one front word), 'pre + front word' (signs, then a front word, then the slot), 'other' (no
front word in the field).

Predictions:
 P1  'other' fields are real: names after an 'other' field look like names after a classic front (same length within
     0.5 sign; shorter than frontless names) and unlike frontless names.
 P2  'other' fields repeat: the field strings recur in 3+ distinct texts more often than signs of the same frequency
     placed before a slot by chance (fields dealt among texts keeping the slot).
 P3  'other' fields are seal things too (seal share like classic fields), and their slot sign mix differs from the
     classic one: 741 dominates (500-741, 390-741).
"""
from front_common import *

say = make_logger('log_9_field.txt')
rng = np.random.default_rng(9)
D = load(); F, *_ = front_set(D, say); D = add_parse(D, F)
A = copy_events(D[D.complete]).copy()
SB = {'060', '741', '742', '745', '368', '365'}


def field(t):
    for i in range(1, min(4, len(t) - 1)):
        x = t[i]
        if x in SB or (x == '002' and t[i - 1] in F):
            f = t[:i]
            if len(f) == 1 and f[0] in F: typ = 'classic'
            elif f[-1] in F: typ = 'pre + front word'
            elif any(s in F for s in f): typ = 'front word inside field'
            else: typ = 'other'
            j = i + 1
            while j < len(t) and t[j] in SB and j - i < 2: j += 1   # 920-060-741: second slot belongs to the boundary
            return typ, '-'.join(f), '-'.join(t[i:j]), t[j:]
    return None


R = []
for r in A.itertuples():
    p = field(r.tok)
    if p is None:
        if r.front:   # a classic front with no slot (820-001-..., 091-056) stays classic, no boundary
            R.append(dict(idx=r.Index, typ='front word, no slot', fieldstr=r.front, slot='', rest=r.body)); continue
        R.append(dict(idx=r.Index, typ='none', fieldstr='', slot='', rest=r.tok)); continue
    R.append(dict(idx=r.Index, typ=p[0], fieldstr=p[1], slot=p[2], rest=p[3]))
R = pd.DataFrame(R).set_index('idx')
A = A.join(R)
def rest_parts(rest):
    j = len(rest)
    while j > 0 and (rest[j - 1] in CLOSERS or rest[j - 1] in TITLES): j -= 1
    return rest[:j], rest[j:]
A['rname'] = A.rest.map(lambda r: rest_parts(tuple(r))[0])
A['rend'] = A.rest.map(lambda r: rest_parts(tuple(r))[1])
A['rnl'] = A.rname.map(len)
A['rclose'] = A.rend.map(lambda e: any(s in CLOSERS for s in e))
A['rcrest'] = A.rname.map(lambda n: bool(n) and V2.get(n[0]) == 'CREST')
say('field type by object kind (complete copy events):')
say(pd.crosstab(A.typ, A.kind).to_string())
rows = []
for typ in ['classic', 'pre + front word', 'front word inside field', 'other', 'front word, no slot', 'none']:
    for k in ('seal', 'all'):
        g = A[(A.typ == typ) & ((A.kind == 'seal') if k == 'seal' else True)]
        gn = g[(g.rnl > 0) & g.rclose]
        rows.append(dict(field=typ, objects=k, texts=len(g), name_closer=len(gn),
                         name_len_mean=round(gn.rnl.mean(), 2) if len(gn) else '',
                         crest_first=round(gn.rcrest.mean(), 3) if len(gn) else '',
                         text_len_mean=round(g.L.mean(), 2) if len(g) else '',
                         seal_share=round((g.kind == 'seal').mean(), 3) if len(g) else '',
                         MD_share=round((g.site == 'Mohenjo-daro').mean(), 3) if len(g) else ''))
T = pd.DataFrame(rows); T.to_csv(f'{OUTF}/f9_fields.csv', index=False)
say('\nNAMES AFTER EACH KIND OF FIELD:'); say(T.to_string(index=False))

# name length test: 'other' vs none, seals, labels dealt within site
G = A[(A.kind == 'seal') & A.typ.isin(['other', 'none', 'classic']) & (A.rnl > 0) & A.rclose]
for a, b in (('other', 'none'), ('other', 'classic'), ('classic', 'none')):
    H = G[G.typ.isin([a, b])]
    lab = (H.typ == a).values; v = H.rnl.values.astype(float)
    o = v[lab].mean() - v[~lab].mean()
    null = [v[l].mean() - v[~l].mean() for l in (deal_within(lab, H.site.values, rng).astype(bool) for _ in range(3000))]
    say(f'name length, {a} minus {b} (seals): {o:+.2f}, dealt {np.mean(null):+.2f}, P low {pval_lo(null, o):.4f}, P high {pval_hi(null, o):.4f} (n {lab.sum()} / {(~lab).sum()})')

# the fields
O = A[A.typ.isin(['other', 'pre + front word', 'front word inside field'])]
fc = O.groupby(['typ', 'fieldstr', 'slot']).size().sort_values(ascending=False)
say('\nnon-classic fields with 2+ texts:'); say(fc[fc >= 2].to_string())
fc.reset_index().rename(columns={0: 'texts'}).to_csv(f'{OUTF}/f9_field_strings.csv', index=False)
say(f'\nslot after field, by field type: ' + str(pd.crosstab(A[A.typ != 'none'].typ, A[A.typ != 'none'].slot.str[:3]).to_dict('index')))
# P2 repeat test for 'other' fields: how many field strings recur in 3+ texts, against fields dealt among the same texts
OT = A[A.typ == 'other']
def nrep(f): c = collections.Counter(f); return sum(1 for v in c.values() if v >= 3), sum(v for v in c.values() if v >= 3)
ob = nrep(OT.fieldstr)
# control: for each 'other' text, a random sign string of the same field length taken from position 0 of random complete
# texts of the same kind whose sign at that position is NOT followed by a slot (what fields look like without the boundary)
pool = collections.defaultdict(list)
for r in A[A.typ == 'none'].itertuples():
    for L in (1, 2, 3):
        if len(r.tok) > L: pool[(r.kind, L)].append('-'.join(r.tok[:L]))
null = []
for _ in range(1000):
    fs = [pool[(k, len(f.split('-')))][rng.integers(len(pool[(k, len(f.split('-')))]))] for k, f in zip(OT.kind, OT.fieldstr)]
    null.append(nrep(fs))
null = np.array(null)
say(f"\n'other' fields: {len(OT)} texts; field strings in 3+ texts: {ob[0]} strings covering {ob[1]} texts; "
    f"text-openings of the same length from texts without a boundary: {null[:, 0].mean():.2f} strings / {null[:, 1].mean():.1f} texts "
    f"(P high {pval_hi(null[:, 1], ob[1]):.4f})")

# ---------- rival: room on the stone (a field uses up space, so the name is shorter)
say('\nRIVAL, room on the stone: name length (seals, name + closer) by face-area half within site group and format')
G = A[(A.kind == 'seal') & A.typ.isin(['classic', 'other', 'pre + front word', 'none']) & (A.rnl > 0) & A.rclose & A.area_mm2.notna()].copy()
G['fielded'] = G.typ != 'none'
G['big'] = G.groupby(['siteg', 'fmt']).area_mm2.transform(lambda s: s >= s.median())
rows = []
for big in (False, True):
    H = G[G.big == big]
    lab = H.fielded.values; v = H.rnl.values.astype(float)
    o = v[lab].mean() - v[~lab].mean()
    null = [v[l].mean() - v[~l].mean() for l in (deal_within(lab, H.site.values, rng).astype(bool) for _ in range(3000))]
    say(f'  {"big" if big else "small"} stones: fielded {v[lab].mean():.2f} (n {lab.sum()}), unfielded {v[~lab].mean():.2f} (n {(~lab).sum()}); '
        f'difference {o:+.2f}, dealt {np.mean(null):+.2f}, P low {pval_lo(null, o):.4f}; total text length fielded {H[H.fielded].L.mean():.2f}, unfielded {H[~H.fielded].L.mean():.2f}')
    rows.append(dict(stones='big' if big else 'small', fielded_name=round(v[lab].mean(), 2), unfielded_name=round(v[~lab].mean(), 2),
                     diff=round(o, 2), P_low=pval_lo(null, o), fielded_text=round(H[H.fielded].L.mean(), 2),
                     unfielded_text=round(H[~H.fielded].L.mean(), 2)))
pd.DataFrame(rows).to_csv(f'{OUTF}/f9_room_rival.csv', index=False)
# longest texts: do fielded texts ever reach the longest names?
say('name length distribution, seals: ' + str(pd.crosstab(G.rnl.clip(upper=7), G.fielded).to_dict()))

# ---------- what do long unfielded names hold that fielded names lack?
say('\nPositions in seal names (name + closer): class of each sign, fielded names against unfielded names of 4+ signs')
U = G[(~G.fielded) & (G.rnl >= 4)]; Fd = G[G.fielded]
def cls_by_pos(H, pos):
    return collections.Counter(V2.get(n[pos] if pos >= 0 else n[pos], 'PERSONAL') for n in H.rname if len(n) > abs(pos) - (pos < 0))
for lab, H in (('fielded', Fd), ('unfielded 4+', U)):
    for pos in (0, 1, -1):
        c = cls_by_pos(H, pos); n = sum(c.values())
        say(f'  {lab}, position {pos}: ' + ', '.join(f'{k} {v/n:.2f}' for k, v in c.most_common(6)))
# first signs of long unfielded names: are they the signs that fill 'other' fields?
other_field_signs = collections.Counter(s for f in A[A.typ == 'other'].fieldstr for s in f.split('-'))
lf = collections.Counter(n[0] for n in U.rname); sf = collections.Counter(n[0] for n in G[(~G.fielded) & (G.rnl <= 2)].rname)
def share_in(c): return sum(v for k, v in c.items() if k in other_field_signs) / max(1, sum(c.values()))
say(f"first sign of a long unfielded name is a sign seen in 'other' fields: {share_in(lf):.3f} (n {sum(lf.values())}); "
    f"short unfielded names (1-2 signs): {share_in(sf):.3f}; signs in 'other' fields: {len(other_field_signs)} kinds")

# ---------- DECOY: the same cut made at signs of the same frequency that are not slot signs (20 decoy slot sets)
say('\nDECOY slot sets: each real slot sign swapped for a sign of about the same frequency (within 35%), not a front word, '
    'slot, closer, title or number; the same field rule applied; seals, fields with no front word')
freq = collections.Counter(s for t in A.tok for s in t)
bad = F | SLOT | {'745'} | CLOSERS | TITLES | NUMS | {'000', 'ALT'}
cands = [s for s in freq if s not in bad and not s.startswith('X')]
whole = set(A[(A.front == '') & (A.name.map(len) > 0) & A.has_closer].signs)
def other_stats(sb):
    rows = []
    for r in A[A.kind == 'seal'].itertuples():
        t = r.tok
        if t and t[0] in F: continue
        for i in range(1, min(4, len(t) - 1)):
            if t[i] in sb:
                rest = t[i + 1:]; nm, en = rest_parts(rest)
                rows.append((len(nm), bool(nm) and V2.get(nm[0]) == 'CREST', any(s in CLOSERS for s in en),
                             '-'.join(rest) in whole and len(nm) > 0))
                break
    if not rows: return dict(n=0)
    a = np.array(rows, dtype=float)
    keep = a[:, 2] == 1
    return dict(n=len(a), name_closer=int(keep.sum()), name_len=a[keep, 0].mean() if keep.any() else np.nan,
                crest_first=a[keep, 1].mean() if keep.any() else np.nan, rest_is_whole_text=a[:, 3].mean())
real = other_stats(SB)
dec = []
for k in range(20):
    sb = set()
    for s in SB:
        pool = [c for c in cands if abs(freq[c] - freq[s]) <= 0.35 * freq[s] and c not in sb]
        if pool: sb.add(pool[rng.integers(len(pool))])
    dec.append(other_stats(sb))
Dd = pd.DataFrame(dec)
say(f"  real slots: {real}")
say(f"  decoys (mean of 20): texts {Dd.n.mean():.1f}, name+closer {Dd.name_closer.mean():.1f}, name length {Dd.name_len.mean():.2f} "
    f"(range {Dd.name_len.min():.2f}-{Dd.name_len.max():.2f}), crest first {Dd.crest_first.mean():.3f} (max {Dd.crest_first.max():.3f}), "
    f"rest is a whole attested frontless text {Dd.rest_is_whole_text.mean():.3f} (max {Dd.rest_is_whole_text.max():.3f})")
pd.concat([pd.DataFrame([dict(set='real', **real)]), Dd.assign(set='decoy')]).to_csv(f'{OUTF}/f9_decoy.csv', index=False)
