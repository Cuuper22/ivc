#!/usr/bin/env python3
"""FRAME v3 — Step 2: Sign-class refinement (Lipi 5-fold CV) and explicit word-free Clause Grammar.

Strictly learns all sign-to-class moves on Lipi (`d` / `train_texts()`) ONLY. Unseen Mahadevan `new texts`
are NEVER accessed here.

Exports:
  - `work_data/fv3/classes_v3.csv`: every Lipi sign, uses, intact face count, v2_base, v3_class, positional stats.
  - `work_data/fv3/cv_class_moves.csv`: sequential 5-fold Lipi CV log-likelihood gains for all accepted moves.
  - Reusable parsers:
      * `parse_v3_initial(cl, kind)` — initial broad recursive/boustrophedon clause grammar (v3a).
      * `parse_v3(cl, kind)` — final tightened boundary-anchored clause segmenter (v3).
      * `tag_sign_roles(cl, clauses)` — per-sign structural role within its clause.
"""
import os, sys, re, collections
import numpy as np, pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DYN = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.insert(0, SCRIPT_DIR)
from frame2_common import *

OUT_FV3 = os.path.join(ROOT_DYN, 'work_data', 'fv3')
os.makedirs(OUT_FV3, exist_ok=True)

V3_CLASSES = list(V2_CLASSES)  # Same 14 explicit word-free jobs; zero singleton classes!


def build_v3_classes(verbose=True):
    """Learn role-consistent sign-to-class moves strictly on Lipi 5-fold CV (`seed=2026`)."""
    c2 = pd.read_csv(os.path.join(OUT2, 'classes_v2.csv'), dtype=str).fillna('')
    V2B = dict(zip(c2.sign, c2.v2_base))

    T = train_texts()
    vocab, idx = vocab_of(T)
    C_all = counts(T, idx)

    intact_faces = [(x, kind_of(k), k) for x, f, k in zip(d.tok, d.flg, d.kind)
                    if x and not (set(x) & UNK) and not (f & {'broken', 'lost', 'alt'})]
    face_occ = collections.Counter(s for x, _, _ in intact_faces for s in x)

    # Prepare 5-fold Lipi CV splits (seed 2026) and Half-A / Half-B split (seed 2026)
    rng_cv = np.random.default_rng(2026)
    folds = rng_cv.integers(0, 5, size=len(T))
    rng_ab = np.random.default_rng(2026)
    half = rng_ab.random(len(T)) < 0.5

    def make_split(tr, va):
        Ctr = counts(tr, idx)
        def flat_t(txts):
            a, b, st, en = [], [], [], []
            for x, clean, k in txts:
                ids = [idx[s] for s in x if s in idx]
                if len(ids) != len(x): continue
                for p, q in zip(ids, ids[1:]): a.append(p); b.append(q)
                if clean: st.append(ids[0]); en.append(ids[-1])
            return np.array(a, int), np.array(b, int), np.array(st, int), np.array(en, int)
        aA, bA, sA, eA = flat_t(tr); aB, bB, sB, eB = flat_t(va)
        ntokB = sum(len(x) for x, c, k in va if all(s in idx for s in x))
        return dict(uniA=Ctr['uni'], aA=aA, bA=bA, sA=sA, eA=eA, aB=aB, bB=bB, sB=sB, eB=eB, ntokB=ntokB)

    FOLD_DATA = [make_split([t for t, fl in zip(T, folds) if fl != f],
                            [t for t, fl in zip(T, folds) if fl == f]) for f in range(5)]
    AB_DATA = [make_split([t for t, h in zip(T, half) if h],
                          [t for t, h in zip(T, half) if not h])]

    def eval_splits(z, K, splits):
        tot_ll = 0.0; tot_n = 0
        for fd in splits:
            uniA = fd['uniA']
            nk = np.bincount(z, minlength=K); cu = np.bincount(z, uniA, K)
            em = (uniA + 0.5) / (cu[z] + 0.5 * nk[z])
            cb = np.bincount(z[fd['aA']] * K + z[fd['bA']], minlength=K * K).reshape(K, K).astype(float)
            ce = np.bincount(z[fd['eA']], minlength=K).astype(float)
            rows_m = np.concatenate([cb, ce[:, None]], 1) + 0.1; rows_m /= rows_m.sum(1, keepdims=True)
            cs = np.bincount(z[fd['sA']], minlength=K) + 0.1; cs /= cs.sum()
            lem = np.log2(em)
            ll = (np.log2(cs[z[fd['sB']]]) + lem[fd['sB']]).sum() + \
                 (np.log2(rows_m[z[fd['aB']], z[fd['bB']]]) + lem[fd['bB']]).sum() + \
                 (np.log2(rows_m[z[fd['eB']], K])).sum()
            tot_ll += ll; tot_n += fd['ntokB']
        return -tot_ll / tot_n

    # Event-deduplicated Lipi intact texts (len >= 2) for positional profiles
    seen_ev = set(); ev_texts = []
    for idx_r, (x, f, k) in enumerate(zip(d.tok, d.flg, d.kind)):
        if not x or len(x) < 2 or set(x) & UNK or f & {'broken', 'lost', 'alt'}: continue
        ek = (d.site.iloc[idx_r], str(d['area-section'].iloc[idx_r]), k, x)
        if ek in seen_ev: continue
        seen_ev.add(ek); ev_texts.append(x)

    occ = collections.Counter()
    p_init = collections.Counter(); p_fin = collections.Counter()
    p_af_open = collections.Counter(); p_af_num = collections.Counter(); p_bf_num = collections.Counter()
    p_bf_end = collections.Counter(); p_af_end = collections.Counter(); p_af_meas = collections.Counter()
    p_bf_slot = collections.Counter(); p_bf_thing = collections.Counter()

    for x in ev_texts:
        cl = [V2B.get(s, 'PERSONAL') for s in x]
        for i, s in enumerate(x):
            occ[s] += 1
            if i == 0: p_init[s] += 1
            if i == len(x) - 1: p_fin[s] += 1
            if i > 0 and cl[i-1] == 'OPEN': p_af_open[s] += 1
            if i + 1 < len(x) and cl[i+1] == 'SLOT': p_bf_slot[s] += 1
            if i > 0 and cl[i-1] in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME'): p_af_num[s] += 1
            if i + 1 < len(x) and cl[i+1] in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME'): p_bf_num[s] += 1
            if i + 1 < len(x) and cl[i+1] in ('CLOSER', 'TITLE'): p_bf_end[s] += 1
            if i > 0 and cl[i-1] in ('CLOSER', 'TITLE'): p_af_end[s] += 1
            if i > 0 and (cl[i-1] == 'MEASURE' or x[i-1] == '706'): p_af_meas[s] += 1
            if i + 1 < len(x) and cl[i+1] == 'THING': p_bf_thing[s] += 1

    def strict_role_ok(s, orig_name, tgt_name):
        n = occ[s]
        if n < 3: return False
        if orig_name != 'PERSONAL':
            if orig_name == 'PLACE' and tgt_name in ('OPEN', 'THING'): pass
            elif orig_name == 'CREST' and s in ('226', '222', '243') and tgt_name in ('CLOSER', 'TITLE', 'THING', 'NAME_BACK'): pass
            else: return False
        fi = p_fin[s]/n; ini = p_init[s]/n
        af_o = p_af_open[s]/n; bf_sl = p_bf_slot[s]/n
        af_n = p_af_num[s]/n; bf_n = p_bf_num[s]/n
        bf_e = p_bf_end[s]/n; af_e = p_af_end[s]/n; af_m = p_af_meas[s]/n
        bf_th = p_bf_thing[s]/n
        if tgt_name == 'CLOSER':
            return (fi >= 0.55 and ini <= 0.25) or (fi >= 0.40 and fi + bf_e >= 0.65 and ini <= 0.20)
        if tgt_name == 'TITLE':
            # Clause-final title/ending or medial tablet closer before count clause (711) or measure-final (167, 868, 200)
            return (fi >= 0.55 and ini <= 0.25) or (af_e >= 0.35 and fi >= 0.45) or (af_m >= 0.50 and fi >= 0.85) or (bf_n >= 0.85 and ini == 0.0 and s == '711')
        if tgt_name == 'THING':
            return (af_n >= 0.35 and bf_n <= 0.15) or (fi >= 0.55 and ini <= 0.22 and af_n >= 0.05)
        if tgt_name == 'MEASURE':
            return bf_n >= 0.45 or bf_th >= 0.45
        if tgt_name == 'AFTER_M':
            return af_m >= 0.35
        if tgt_name == 'OPEN':
            return fi <= 0.15 and (ini >= 0.65 or (ini >= 0.50 and bf_sl >= 0.40))
        if tgt_name == 'SLOT':
            return af_o >= 0.25 and fi <= 0.20
        if tgt_name == 'NAME_BACK':
            return bf_e >= 0.60 and fi <= 0.18
        if tgt_name == 'CREST':
            return ini >= 0.45 and fi <= 0.10
        return False

    labs = list(V3_CLASSES); K = len(labs)
    z0 = np.array([labs.index(V2B.get(s, 'PERSONAL')) for s in vocab])
    z = z0.copy()
    base_cv = eval_splits(z0, K, FOLD_DATA)
    base_ab = eval_splits(z0, K, AB_DATA)
    cur = base_cv

    TARGET_FUNC = ['CLOSER', 'TITLE', 'THING', 'MEASURE', 'AFTER_M', 'OPEN', 'SLOT', 'NAME_BACK', 'CREST']
    tgt_ids = [labs.index(c) for c in TARGET_FUNC]

    move_hist = []
    while True:
        best = (0.0, None)
        for i, s in enumerate(vocab):
            u = C_all['uni'][i]
            if u < 4 and not (u >= 2 and face_occ[s] >= 3): continue
            orig_name = V2B.get(s, 'PERSONAL')
            for c in tgt_ids:
                if c == z[i]: continue
                if not strict_role_ok(s, orig_name, labs[c]): continue
                z2 = z.copy(); z2[i] = c
                g = cur - eval_splits(z2, K, FOLD_DATA)
                if g > best[0]:
                    best = (g, (i, c))
        if best[1] is None or best[0] < 0.0001:
            break
        i, c = best[1]
        s = vocab[i]
        frm, to = labs[z[i]], labs[c]
        z[i] = c
        cur -= best[0]
        ab_now = eval_splits(z, K, AB_DATA)
        n = occ[s]
        move_hist.append(dict(
            step=len(move_hist) + 1, sign=s, distinct_uses=int(C_all['uni'][i]), intact_faces=face_occ[s],
            from_class=frm, to_class=to, cv5_gain_bits=round(best[0], 6), cv5_bits=round(cur, 5), halfB_bits=round(ab_now, 5),
            p_init=round(p_init[s]/n, 3) if n else 0.0, p_fin=round(p_fin[s]/n, 3) if n else 0.0,
            p_after_num=round(p_af_num[s]/n, 3) if n else 0.0, p_before_num=round(p_bf_num[s]/n, 3) if n else 0.0,
            p_before_end=round(p_bf_end[s]/n, 3) if n else 0.0, p_after_meas=round(p_af_meas[s]/n, 3) if n else 0.0
        ))

    v3_map = {s: labs[z[i]] for i, s in enumerate(vocab)}
    # Include any rare Lipi signs that only occurred on damaged faces (defaulting to V2B)
    for s, vc in V2B.items():
        v3_map.setdefault(s, vc)

    cls_rows = []
    for s in sorted(v3_map):
        u = int(C_all['uni'][idx[s]]) if s in idx else 0
        n = occ[s]
        cls_rows.append(dict(
            sign=s, distinct_uses=u, intact_faces=face_occ[s],
            v2_base=V2B.get(s, 'PERSONAL'), v3_class=v3_map[s],
            moved=(V2B.get(s, 'PERSONAL') != v3_map[s]),
            p_init=round(p_init[s]/n, 3) if n else 0.0,
            p_fin=round(p_fin[s]/n, 3) if n else 0.0,
            p_after_num=round(p_af_num[s]/n, 3) if n else 0.0,
            p_before_num=round(p_bf_num[s]/n, 3) if n else 0.0,
            p_before_end=round(p_bf_end[s]/n, 3) if n else 0.0,
        ))
    pd.DataFrame(cls_rows).to_csv(os.path.join(OUT_FV3, 'classes_v3.csv'), index=False)
    pd.DataFrame(move_hist).to_csv(os.path.join(OUT_FV3, 'cv_class_moves.csv'), index=False)
    if verbose:
        log(f'FRAME v3 classes built on Lipi: {len(move_hist)} CV-validated moves across {K} explicit classes')
        log(f'  5-fold Lipi CV: {base_cv:.5f} -> {cur:.5f} bits/sign (delta {cur - base_cv:+.5f})')
        log(f'  Lipi Half-B   : {base_ab:.5f} -> {eval_splits(z, K, AB_DATA):.5f} bits/sign')
    return v3_map, V2B, move_hist


# ==============================================================================
# GRAMMAR DEFINITIONS: INITIAL BROAD (v3a) AND TIGHTENED FINAL (v3)
# ==============================================================================
NUM = '(?:NUM_SHORT|NUM_TALL|NUM_NAME)'
NS = '(?:CREST|PERSONAL|NUM_NAME|NUM_SHORT|NUM_TALL|PLACE|NAME_BACK|MEASURE|AFTER_M|THING)'
FRONT = '(?:(?:OPEN )+(?:SLOT ){0,2}|(?:SLOT ){1,2})'
END = '(?:(?:CLOSER ){1,2}(?:TITLE ){0,2}|TITLE CLOSER (?:TITLE )?|(?:TITLE ){1,2})'

# --- Final Tightened Atomic Clauses (FRAME v3) ---
V3_ATOMIC = [
    ('name_clause', re.compile(rf'^(?:{FRONT})?(?:TITLE )?(?:{NS} )+{END}$')),
    ('open_closed_clause', re.compile(rf'^(?:OPEN )+(?:SLOT ){{0,2}}{END}$')),
    ('count_clause', re.compile(rf'^(?:{FRONT})?(?:(?:{NUM} )+(?:THING|CREST|OPEN|MEASURE) )+$')),
    ('goods_clause', re.compile(rf'^(?:(?:{FRONT})?(?:(?:{NS} )*(?:{NUM}|MEASURE|AFTER_M|PLACE|CREST) (?:PERSONAL )?)|(?:{FRONT})?(?:{NS} ){{1,2}})(?:THING )+$')),
    ('measure_clause', re.compile(rf'^(?:{FRONT})?(?:(?:{NS} ){{1,3}})?MEASURE (?:(?:AFTER_M|{NUM}) )*(?:(?:AFTER_M|{NUM}) |{END})$')),
    ('after_measure_clause', re.compile(rf'^(?:{FRONT})?(?:{NS} ){{1,3}}AFTER_M (?:{END})?$')),
    ('vessel_tally', re.compile(rf'^(?:THING )+(?:{NUM} )+$')),
    ('header_clause', re.compile(rf'^(?:(?:OPEN )+(?:SLOT ){{1,2}}(?:{NS} )+|(?:(?:PLACE|CREST|PERSONAL|{NUM}) ){{1,2}}(?:OPEN )?(?:SLOT ){{1,2}})$')),
    ('paired_emblem', re.compile(r'^(?:(?:PLACE ){2,3}|(?:CREST ){2,3})$')),
]

SECOND_STRICT = {'name_clause', 'open_closed_clause', 'count_clause', 'goods_clause', 'measure_clause', 'paired_emblem'}
FIRST_STRICT = {'name_clause', 'open_closed_clause', 'count_clause', 'goods_clause', 'measure_clause', 'header_clause', 'paired_emblem'}

RX_SLOT_PRE = re.compile(rf'^(?:{FRONT})?(?:{NS} )+(?:SLOT ){{1,2}}$')
RX_PRE_OPEN = re.compile(rf'^(?:{NS} ){{1,4}}$')
RX_NUM_PLACE_TAG = re.compile(rf'^(?:(?:{NUM}|PLACE|THING) ){{1,2}}$')
RX_RECIP_TAIL = re.compile(rf'^(?:{NS} ){{1,2}}$')
RX_FRONT_ALONE = re.compile(r'^(?:OPEN )+(?:SLOT ){0,2}$')
RX_TITLE_ALONE = re.compile(r'^(?:CLOSER|TITLE) (?:TITLE )?$')
RX_FUNC_SOLO = re.compile(rf'^(?:{NUM}|THING|MEASURE|SLOT|CREST|PLACE) $')


def match_v3_atomic(cl_slice):
    s = ' '.join(cl_slice) + ' '
    for nm, rx in V3_ATOMIC:
        if rx.match(s):
            return nm
    return ''


def _match_1_or_2_strict(cl_slice):
    m1 = match_v3_atomic(cl_slice)
    if m1 in SECOND_STRICT:
        return m1, [(0, len(cl_slice), m1)]
    n = len(cl_slice)
    for sp in range(1, n):
        c1 = match_v3_atomic(cl_slice[:sp])
        if c1 not in FIRST_STRICT: continue
        c2 = match_v3_atomic(cl_slice[sp:])
        if c2 in SECOND_STRICT:
            return f'compound:{c1}+{c2}', [(0, sp, c1), (sp, n, c2)]
    return '', []


def parse_v3(cl, kind):
    """Final tightened FRAME v3 parser & clause segmenter.
    Returns (pattern_name, [(start, end, clause_type), ...]). Empty ('', []) if unparsed.
    """
    n = len(cl)
    if n == 0:
        return '', []
    s_full = ' '.join(cl) + ' '

    # 1. Single atomic clause
    m1 = match_v3_atomic(cl)
    if m1:
        return m1, [(0, n, m1)]
    if RX_TITLE_ALONE.match(s_full):
        return 'title_alone', [(0, n, 'title_alone')]
    if RX_FRONT_ALONE.match(s_full):
        return 'front_alone', [(0, n, 'front_alone')]

    # 2. Multi-clause inscriptions (length >= 3)
    if n >= 3:
        # 2a. Juxtaposed 2-clause (or 3-clause) strict compounds & tight post-clause tails
        for split in range(1, n):
            c1 = match_v3_atomic(cl[:split])
            if c1 not in FIRST_STRICT: continue
            c2, seg2 = _match_1_or_2_strict(cl[split:])
            if c2:
                lbl = f'compound:{c1}+{c2}' if not c2.startswith('compound:') else f'triple:{c1}+{c2[9:]}'
                return lbl, [(0, split, c1)] + [(a + split, b + split, t) for a, b, t in seg2]
            if c1 in ('name_clause', 'open_closed_clause') and RX_NUM_PLACE_TAG.match(' '.join(cl[split:]) + ' '):
                return f'{c1}+num_place_tag', [(0, split, c1), (split, n, 'num_place_tag')]
            if c1 in ('count_clause', 'measure_clause') and RX_RECIP_TAIL.match(' '.join(cl[split:]) + ' '):
                return f'{c1}+recipient_tail', [(0, split, c1), (split, n, 'recipient_tail')]
            if c1 == 'name_clause' and split >= 4 and n - split == 1 and kind in ('ctab', 'mtab', 'tag'):
                return 'name_clause+docket', [(0, split, c1), (split, n, 'docket_sign')]

        # 2b. Postpositional slot-linked compound: [Phrase + SLOT{1,2}]{1,2} + [Strict Clause(s)]
        for split in range(2, n):
            if cl[split - 1] == 'SLOT' and RX_SLOT_PRE.match(' '.join(cl[:split]) + ' '):
                c2, seg2 = _match_1_or_2_strict(cl[split:])
                if c2:
                    return f'slot_linked+{c2}', [(0, split, 'slot_clause')] + [(a + split, b + split, t) for a, b, t in seg2]
                for sp2 in range(split + 2, n):
                    if cl[sp2 - 1] == 'SLOT' and RX_SLOT_PRE.match(' '.join(cl[split:sp2]) + ' '):
                        c3, seg3 = _match_1_or_2_strict(cl[sp2:])
                        if c3:
                            return f'slot_linked2+{c3}', [(0, split, 'slot_clause'), (split, sp2, 'slot_clause')] + [(a + sp2, b + sp2, t) for a, b, t in seg3]
                if kind in ('tag', 'ctab', 'mtab') and 2 <= n - split <= 3 and cl[split] == 'THING':
                    return 'slot_linked+tally_docket', [(0, split, 'slot_clause'), (split, n, 'tally_docket')]

        # 2c. Short prefix + explicit OPEN-headed strict clause(s)
        for split in range(1, min(5, n - 1)):
            if cl[split] == 'OPEN' and RX_PRE_OPEN.match(' '.join(cl[:split]) + ' '):
                c2, seg2 = _match_1_or_2_strict(cl[split:])
                if c2:
                    return f'prefix+{c2}', [(0, split, 'prefix_phrase')] + [(a + split, b + split, t) for a, b, t in seg2]

        # 2d. Mirror-incised miniature tablet / pot / bangle with OPEN at right edge (len 3-4, non-seal)
        if kind in ('mtab', 'pot', 'other') and n in (3, 4) and cl[-1] == 'OPEN' and cl[0] != 'OPEN':
            return 'mirror_tablet_open', [(0, n, 'mirror_tablet_open')]

    # 3. Length-1 shorthand & emblem marks
    if n == 1:
        if kind == 'ctab': return 'one_picture', [(0, 1, 'one_picture')]
        if RX_FUNC_SOLO.match(s_full): return 'single_mark', [(0, 1, 'single_mark')]
        if kind in ('pot', 'other'): return 'pot_tool_mark', [(0, 1, 'pot_tool_mark')]

    return '', []


# --- Initial Broad Design (v3a, prior to Step-3 decoy tightening) ---
V3A_BROAD_CLAUSES = V3_ATOMIC[:-2] + [
    ('measure_broad', re.compile(rf'^(?:{FRONT})?(?:(?:{NS} ){{1,3}})?MEASURE (?:(?:AFTER_M|{NUM}|PERSONAL) ){{1,2}}(?:{END})?$')),
    ('header_broad', re.compile(rf'^(?:OPEN (?:SLOT ){{1,2}}(?:{NS} )+|OPEN (?:{NS} ){{1,2}}|(?:(?:PLACE|CREST|PERSONAL|{NUM}) ){{1,2}}(?:OPEN )?(?:SLOT ){{1,2}})$')),
    ('paired_broad', re.compile(rf'^(?:(?:PLACE ){{2,3}}|(?:CREST ){{2,3}}|(?:{NUM} ){{2,3}})$')),
]
RX_CAP_BROAD = re.compile(rf'^(?:(?:{NUM} )+PERSONAL |PERSONAL (?:{NUM} )+|(?:{NUM} )PERSONAL (?:{NUM} ))$')


def parse_v3_initial(cl, kind):
    """Initial broad multi-clause parser (v3a) before decoy-selectivity tightening."""
    nm, segs = parse_v3(cl, kind)
    if nm:
        return nm, segs
    n = len(cl); s_full = ' '.join(cl) + ' '
    for bnm, rx in V3A_BROAD_CLAUSES[-3:]:
        if rx.match(s_full): return bnm, [(0, n, bnm)]
    if n >= 2:
        cl_rev = cl[::-1]
        if cl_rev[0] == 'OPEN' or cl_rev[-1] in ('CLOSER', 'TITLE'):
            mr = match_v3_atomic(cl_rev)
            if mr: return f'boustrophedon:{mr}', [(0, n, f'rev_{mr}')]
    if n in (2, 3) and kind in ('pot', 'mtab', 'other') and RX_CAP_BROAD.match(s_full):
        return 'capacity_potter_mark', [(0, n, 'capacity_potter_mark')]
    if n in (2, 3) and kind in ('pot', 'other') and all(c == 'PERSONAL' for c in cl):
        return 'pot_tool_shorthand', [(0, n, 'pot_tool_shorthand')]
    return '', []


def tag_sign_roles(cl, segs):
    """Assign each token a concrete within-clause grammatical role."""
    if not segs:
        return ['unparsed:' + c.lower() for c in cl]
    roles = [''] * len(cl)
    for idx_c, (a, b, ctype) in enumerate(segs, start=1):
        sub = cl[a:b]
        for j, c in enumerate(sub):
            pos = a + j
            if c == 'OPEN':
                r = 'clause_opener' if j == 0 or sub[j-1] == 'OPEN' else 'counted_house'
            elif c == 'SLOT':
                r = 'clause_linker' if j == len(sub) - 1 else 'header_slot'
            elif c == 'CLOSER':
                r = 'clause_closer'
            elif c == 'TITLE':
                r = 'front_title' if j == 0 and len(sub) > 1 else 'clause_title'
            elif c == 'THING':
                r = 'vessel_head' if ctype == 'vessel_tally' and j == 0 else ('counted_commodity' if j == len(sub) - 1 or sub[min(j+1, len(sub)-1)] == 'THING' else 'stem_thing')
            elif c == 'MEASURE':
                r = 'measure_unit'
            elif c == 'AFTER_M':
                r = 'measure_completer'
            elif c in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME'):
                r = 'name_numeral' if c == 'NUM_NAME' and ctype == 'name_clause' else 'quantifier'
            elif c == 'CREST':
                r = 'name_crest'
            elif c == 'NAME_BACK':
                r = 'pre_closer_stem'
            elif c == 'PLACE':
                r = 'place_or_time'
            else:
                r = 'name_stem'
            roles[pos] = f'c{idx_c}:{r}'
    return roles


if __name__ == '__main__':
    build_v3_classes(verbose=True)
