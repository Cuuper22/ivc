#!/usr/bin/env python3
"""Sign list step 4: COMPOUND SIGNS = base sign + added mark. Rules fixed before any number:

FAMILIES from the shape list (work_data/sign_shapes.csv):
  prefix rule: sign C is base B + mark when C's description starts with B's whole description (trailing ',' '.' and spaces
    dropped), is longer, and has a different shape code. The rest of C's description is the mark.
  noun rule: bases written as plain nouns: fish 220 ("Fish with no other decoration") for every "Fish with ..."; U 700
    ("Simple U with no other decoration") for every "U with ..."; person 090 ("Person with two arms and two legs") for every
    "Person with ..."; leaf 790 ("Simple leaf or diamond") for every "Leaf ..." / "Leaf with ...".
  For a compound with several bases (prefix chain), the nearest one (longest description) is the base.
MARK TYPES (keywords in the mark text): cage = 'caged'; brackets = 'bracket' or 'parenthes'; hat = 'hat' or 'capped';
  strokes-inside = 'stroke' with 'inside' / 'in mouth' / 'in the body' / 'inserted' / 'through body' / 'between'; hatching =
  'hatch'; whiskers = 'whisker'; held object = the rest of a "Person with X" / "U with X" (two signs joined); other.
TEST (as measured once for the marked fish): ONE-FOR-TWO frames, both catalogues in Lipi numbering, copy events, faces with
  no lost sign and no broken edge: text 1 = P + [x] + S, text 2 = P + [y z] + S, P + S holding at least one sign; frame =
  (P, S), counted once. For a compound C with base B: share of C's one-for-two frames whose pair [y z] holds B. Pooled
  over all compounds against the same share for every other single sign x and that compound's base (rate of "a base
  written out" for non-compounds).
CONTROL (marks dealt at random): every compound gets a base drawn at random from the other bases of the family list
  (5,000 deals); score = frames whose pair holds the dealt base. P = share of deals >= real.
PER MARK TYPE: the same score by mark type, and its own deal. A mark is a REAL UNIT when its compounds are written out as
  [something + base] more than dealt bases give (P < 0.05) or when the standalone mark sign (strokes 001-004 for strokes
  inside, 904 / 923 for brackets, four short strokes 004 for cage) shows up as y with z = B.
Output: work_data/signlist/mark_families.csv, mark_test.csv, one_for_two.csv, log_marks.txt
"""
from signlist_common import *
from scipy.stats import fisher_exact

say = logger('marks')
SH = shapes()
def clean(t): return t.strip().rstrip('.,; ').strip()
desc = {s: clean(t) for s, (c, t) in SH.items()}
code = {s: c for s, (c, t) in SH.items()}
NOUN = {'220': ('fish with ',), '700': ('u with ',), '090': ('person with ',), '790': ('leaf with ', 'leaf, ', 'leaf ')}
fam = {}
for c in desc:
    best = None
    for b in desc:
        if b == c or code[b] == code[c]: continue
        if desc[c].lower().startswith(desc[b].lower()) and len(desc[c]) > len(desc[b]) + 2:
            if best is None or len(desc[b]) > len(desc[best]): best = b
    if best is None:
        for b, pre in NOUN.items():
            if c != b and code[c] != code[b] and any(desc[c].lower().startswith(p) for p in pre) and 'no other decoration' not in desc[c].lower():
                best = b; break
    if best: fam[c] = (best, desc[c][len(desc[best]):].strip(' ,.') if desc[c].lower().startswith(desc[best].lower()) else desc[c])
def mtype(m, base):
    t = m.lower()
    if 'caged' in t: return 'cage'
    if 'bracket' in t or 'parenthes' in t: return 'brackets'
    if 'hat' in t.split() or 'hat' in t or 'capped' in t: return 'hat'
    if ('stroke' in t or 'line' in t) and any(k in t for k in ('inside', 'in mouth', 'in the body', 'inserted', 'through body', 'between', 'in body')): return 'strokes inside'
    if 'hatch' in t: return 'hatching'
    if 'whisker' in t: return 'whiskers'
    if base in ('090', '700', '790'): return 'joined object'
    return 'other'
F = pd.DataFrame([dict(compound=c, base=b, mark=m, mark_type=mtype(m, b), compound_shape=desc[c][:90]) for c, (b, m) in fam.items()])
L = load_lipi(); Mx = load_mahadevan('lipi'); U = uses(L)
F['uses'] = F.compound.map(lambda s: U.get(s, 0)); F['base_uses'] = F.base.map(lambda s: U.get(s, 0))
F = F.sort_values(['base', 'compound']); F.to_csv(f'{OUT}/mark_families.csv', index=False)
say(f'families: {F.base.nunique()} bases, {len(F)} compounds; mark types: {F.mark_type.value_counts().to_dict()}')
for b, g in F.groupby('base'):
    if g.uses.sum() >= 5: say(f'   base {b} ({U.get(b, 0)} uses; {desc.get(b, "")[:40]}): ' + ', '.join(f'{c}[{t}; {u}]' for c, t, u in zip(g.compound, g.mark_type, g.uses)))

# ---------------- one-for-two frames ----------------
faces = set()
for evs in (L, Mx):
    for e in evs:
        for f, br in zip(e['faces'], e['broken']):
            if not br and len(f) >= 2 and all(is_sign(s) for s in f): faces.add(f)
by_frame = collections.defaultdict(set)       # (P, S) -> singles x
for f in faces:
    for i in range(len(f)):
        by_frame[(f[:i], f[i + 1:])].add(f[i])
o42 = collections.defaultdict(set)            # x -> set of (frame, y, z)
for f in faces:
    for i in range(len(f) - 1):
        key = (f[:i], f[i + 2:])
        if not key[0] and not key[1]: continue
        for x in by_frame.get(key, ()):
            o42[x].add((key, f[i], f[i + 1]))
rows = [dict(one=x, y=y, z=z, frame='-'.join(k[0]) + '-[ ]-' + '-'.join(k[1])) for x, v in o42.items() for (k, y, z) in v]
OF = pd.DataFrame(rows); OF.to_csv(f'{OUT}/one_for_two.csv', index=False)
say(f'one-for-two frames: {len(OF)} over {OF.one.nunique()} single signs')
cnt = {x: len(v) for x, v in o42.items()}
def holds(x, b): return sum(1 for (k, y, z) in o42.get(x, ()) if b in (y, z))
def holds_mark(x, b, ms): return sum(1 for (k, y, z) in o42.get(x, ()) if (z == b and y in ms) or (y == b and z in ms))

comp = [c for c in F.compound if cnt.get(c, 0)]
real = sum(holds(c, fam[c][0]) for c in comp); tot = sum(cnt[c] for c in comp)
# other single signs, against the same bases
bases = sorted(set(F.base))
oth = [x for x in cnt if x not in fam and x not in bases]
oth_hold = sum(holds(x, b) for x in oth for b in bases if True) ; oth_tot = sum(cnt[x] for x in oth) * len(bases)
say(f'ALL COMPOUNDS: {real} of {tot} one-for-two frames hold their own base; non-compound signs hold a given base in '
    f'{oth_hold} of {oth_tot} (frame x base) cases ({oth_hold / max(1, oth_tot):.3%}); Fisher P '
    f'{fisher_exact([[real, tot - real], [oth_hold, oth_tot - oth_hold]], alternative="greater")[1]:.2e}')
rng = np.random.default_rng(5)
def dealt(compounds):
    out = []
    for _ in range(5000):
        s = 0
        for c in compounds:
            b = rng.choice([x for x in bases if x != fam[c][0]]); s += holds(c, b)
        out.append(s)
    return np.array(out)
D = dealt(comp)
say(f'   control, bases dealt at random: mean {D.mean():.2f}, max {D.max()}; real {real}; P {pvalue_hi(D, real):.4f}')
MARKSIGN = {'strokes inside': {'001', '002', '003', '004'}, 'brackets': {'904', '923'}, 'cage': {'004'}, 'hat': {'480'}}
T = []
for t, g in F.groupby('mark_type'):
    cs = [c for c in g.compound if cnt.get(c, 0)]
    if not cs: continue
    r = sum(holds(c, fam[c][0]) for c in cs); n = sum(cnt[c] for c in cs)
    Dt = dealt(cs)
    ms = MARKSIGN.get(t, set())
    rm = sum(holds_mark(c, fam[c][0], ms) for c in cs) if ms else None
    ex = '; '.join(f'{c}~{y}-{z}' for c in cs for (k, y, z) in list(o42[c]) if fam[c][0] in (y, z))[:300]
    T.append(dict(mark_type=t, compounds=len(cs), frames=n, frames_holding_base=r, dealt_mean=round(Dt.mean(), 2), dealt_max=int(Dt.max()),
                  P=pvalue_hi(Dt, r), mark_sign_plus_base=rm, examples=ex))
    say(f'   mark {t}: {len(cs)} compounds, {r} of {n} frames hold the base (dealt {Dt.mean():.2f}, P {pvalue_hi(Dt, r):.4f})'
        + (f'; standalone mark sign next to base: {rm}' if ms else ''))
# per family (base) with 5+ frames
for b, g in F.groupby('base'):
    cs = [c for c in g.compound if cnt.get(c, 0)]
    n = sum(cnt.get(c, 0) for c in cs)
    if n < 5: continue
    r = sum(holds(c, b) for c in cs); Dt = dealt(cs)
    T.append(dict(mark_type=f'family of base {b}', compounds=len(cs), frames=n, frames_holding_base=r, dealt_mean=round(Dt.mean(), 2),
                  dealt_max=int(Dt.max()), P=pvalue_hi(Dt, r), mark_sign_plus_base=None,
                  examples='; '.join(f'{c}~{y}-{z}' for c in cs for (k, y, z) in list(o42[c]) if b in (y, z))[:300]))
    say(f'   family {b}: {r} of {n} frames hold the base (dealt {Dt.mean():.2f}, P {pvalue_hi(Dt, r):.4f})')
pd.DataFrame(T).to_csv(f'{OUT}/mark_test.csv', index=False)
# direct check: standalone stroke signs written right before the jar 740 against jar-with-strokes compounds
bg = collections.Counter(); uni = collections.Counter(); N = 0
for e in L:
    for f in e['faces']:
        for a, b in zip(f, f[1:]):
            if is_sign(a) and is_sign(b): bg[(a, b)] += 1; N += 1
for c in sorted(set(F[F.base == '740'].compound)):
    say(f'   jar compound {c} ({U.get(c, 0)} uses, mark "{fam[c][1][:40]}")')
for m in ['001', '002', '003', '004']:
    say(f'   bigram {m}-740: {bg[(m, "740")]}; {m}-700 (U): {bg[(m, "700")]}; {m}-220 (fish): {bg[(m, "220")]}')
