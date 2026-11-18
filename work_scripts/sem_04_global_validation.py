#!/usr/bin/env python3
"""sem_04_global_validation.py -- System-level decoy & held-out validation of physical semantic anchors.

Runs three global validation tests against 2,000 matched decoy/shuffle controls:
  1. Zero-Leakage Out-of-Sample Context Prediction on Held-Out Mahadevan `new texts` (990 events):
     - Anchor selection is done STRICTLY on Lipi (top Lipi domain per sign with Lipi P_shuf <= 0.05
       among domains present in Mahadevan `new texts`; zero `new texts` numbers used for selection!).
     - Evaluates mean log-odds / enrichment on unseen Mahadevan `new texts` vs 2,000 frequency-band-matched
       decoy anchor tables (permuting Lipi-selected domain targets among signs in the same Lipi frequency band).
     - Also evaluates phrase-level Lipi->New out-of-sample context prediction vs 2,000 frequency-matched decoys.
  2. Inscription-Internal Domain Coherence on Held-Out Mahadevan `new texts`:
     - Learns pairwise domain/CATS lift strictly on Lipi events (excluding same-sign pairs).
     - Scores unseen `new text` multi-sign inscriptions under real Lipi-derived `CATS` masks vs 2,000
       frequency-band & v2-class matched decoy shuffles.
  3. Ideographic vs. Rebus/Phonetic Boundary Across Syntactic Slots (Visual Shape vs. Physical Context):
     - Maps each sign's purely visual drawing (`sign_shapes.csv`) to visual categories (plant, vessel/tool,
       person, animal, number/stroke, place/grid/hill) with zero knowledge of archaeological findspots.
     - Measures exact alignment between visual glyph category and purely contextual archaeological `CATS` mask
       separately in:
         (a) Functional/Commodity/Ending slots (`COUNTED`, `SOLO`, `GOODS_OR_SOLO`, `ENDING`, `FRONT`), vs
         (b) Personal/House `NAME` slots (`NAME`, `NAME_CREST`, `PRE_CLOSER`),
       against 2,000 shuffles! Directly tests where Indus glyphs act as transparent ideograms/logograms
       versus phonetic/rebus or clan-emblem name elements.
"""
import os
import re
import sys
import json
import collections
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from sense_common import CATS
from sem_02_anchors import DOMAINS

OUT = os.path.join(ROOT, 'work_data', 'sem')
rng = np.random.default_rng(20261120)
N_SHUF = 2000


def log(*args):
    print('[sem_04]', *args, flush=True)


ev_lipi = json.load(open(os.path.join(OUT, 'events_lipi.json')))
ev_new = json.load(open(os.path.join(OUT, 'events_new.json')))
for r in ev_lipi:
    r['_st'] = set(r['subtypes'])
    r['_zn'] = set(r['zones'])
for r in ev_new:
    r['_st'] = set(r['subtypes'])
    r['_zn'] = set(r['zones'])

sweep = pd.read_csv(os.path.join(OUT, 'sweep_all_hits.csv'), dtype=str).fillna('')
for c in ['lipi_p_shuf', 'lipi_z_shuf', 'lipi_exp_shuf', 'lipi_k_in', 'lipi_k_tot']:
    sweep[c] = pd.to_numeric(sweep[c], errors='coerce')
sweep['strat_lift'] = sweep['lipi_k_in'] / sweep['lipi_exp_shuf'].clip(lower=0.01)

dom_specs = {d[0]: d for d in DOMAINS if d[7]}  # domains that exist in Mahadevan `new texts`

# Precompute Mahadevan `new texts` domain indicator vectors (pool mask & target mask over 990 events)
new_dom_masks = {}
for dom_id, (_, _, _, pool_fn, target_fn, _, _, _) in dom_specs.items():
    pmask = np.array([bool(pool_fn(r)) for r in ev_new], dtype=bool)
    tmask = np.array([bool(pool_fn(r) and target_fn(r)) for r in ev_new], dtype=bool)
    if tmask.sum() >= 2 and (pmask.sum() - tmask.sum()) >= 2:
        new_dom_masks[dom_id] = (pmask, tmask)


# ---------------- TEST 1: Zero-Leakage Lipi -> Held-Out `New Texts` Context Prediction ----------------
log('=== Global Test 1: Zero-Leakage Lipi -> Held-Out New Texts Context Prediction ===')

# Select strictly on LIPI ONLY (zero look at `new texts`!):
# For each sign (or phrase), pick its single strongest Lipi domain (lowest lipi_p_shuf, tie-break highest lipi_z_shuf)
# among testable domains with Lipi P_shuf <= 0.02 and strat_lift >= 1.5!
lipi_sign_tot = collections.Counter(s for r in ev_lipi for s in r['signs'])
new_sign_vecs = {}
for s in {x for r in ev_new for x in r['signs']}:
    new_sign_vecs[s] = np.array([s in r['signs'] for r in ev_new], dtype=bool)

new_p2_vecs = {}
for p in {x for r in ev_new for x in r['phrases2']}:
    new_p2_vecs[p] = np.array([p in r['phrases2'] for r in ev_new], dtype=bool)


def run_oos_prediction(ftype_filter, vec_lookup, min_new_occ=2, p_cut=0.02, label='SIGN'):
    sub = sweep[(sweep.ftype.isin(ftype_filter)) &
                (sweep.domain.isin(new_dom_masks.keys())) &
                (sweep.lipi_p_shuf <= p_cut) &
                (sweep.strat_lift >= 1.5)].copy()
    # Strictly sort by LIPI stats only!
    sub = sub.sort_values(['lipi_p_shuf', 'lipi_z_shuf'], ascending=[True, False])
    chosen = []
    seen_u = set()
    for _, r in sub.iterrows():
        u = r['unit']
        if u in seen_u:
            continue
        seen_u.add(u)
        if u in vec_lookup and vec_lookup[u].sum() >= min_new_occ:
            chosen.append((u, r['domain'], int(r['lipi_k_tot'])))
    if len(chosen) < 5:
        return None

    # Frequency bands (3 tertiles on Lipi frequency) for fair decoy shuffling
    freqs = np.array([c[2] for c in chosen])
    q1, q2 = np.quantile(freqs, [1 / 3, 2 / 3])
    bands = np.array([0 if f <= q1 else (1 if f <= q2 else 2) for f in freqs])

    # Precompute log-lift matrix M[i, j]: score if unit i is evaluated on chosen[j]'s domain in `new texts`!
    n_u = len(chosen)
    L_mat = np.zeros((n_u, n_u), dtype=float)
    hit_mat = np.zeros((n_u, n_u), dtype=float)
    exp_mat = np.zeros((n_u, n_u), dtype=float)
    for i, (u_i, _, _) in enumerate(chosen):
        uv = vec_lookup[u_i]
        for j, (_, dom_j, _) in enumerate(chosen):
            pmask, tmask = new_dom_masks[dom_j]
            k_pool = int((uv & pmask).sum())
            k_in = int((uv & tmask).sum())
            n_pool = int(pmask.sum())
            n_in = int(tmask.sum())
            exp_ij = k_pool * (n_in / max(n_pool, 1))
            # Smoothed log2 lift on held-out `new texts`
            L_mat[i, j] = np.log2((k_in + 0.5) / (exp_ij + 0.5))
            hit_mat[i, j] = k_in
            exp_mat[i, j] = exp_ij

    real_loglift = float(np.diag(L_mat).mean())
    real_hits = float(np.diag(hit_mat).sum())
    real_exp = float(np.diag(exp_mat).sum())

    decoy_loglifts = []
    decoy_hits = []
    band_groups = [np.where(bands == b)[0] for b in (0, 1, 2)]
    idx_all = np.arange(n_u)
    for _ in range(N_SHUF):
        perm = idx_all.copy()
        for bg in band_groups:
            if len(bg) > 1:
                perm[bg] = rng.permutation(bg)
        decoy_loglifts.append(float(L_mat[idx_all, perm].mean()))
        decoy_hits.append(float(hit_mat[idx_all, perm].sum()))

    dl = np.array(decoy_loglifts)
    dh = np.array(decoy_hits)
    z_ll = (real_loglift - dl.mean()) / max(dl.std(), 1e-6)
    p_ll = (1.0 + (dl >= real_loglift).sum()) / (N_SHUF + 1.0)
    z_ht = (real_hits - dh.mean()) / max(dh.std(), 1e-6)
    p_ht = (1.0 + (dh >= real_hits).sum()) / (N_SHUF + 1.0)

    log(f'  [{label}] {n_u} Lipi-anchored units tested blind on held-out Mahadevan `new texts`:')
    log(f'    Total target-domain hits: real = {real_hits:.0f} (expected from marginals {real_exp:.1f}) '
        f'vs frequency-matched decoys = {dh.mean():.1f} +- {dh.std():.1f} (z = +{z_ht:.2f}, P = {p_ht:.5f})')
    log(f'    Mean log2-lift per unit : real = +{real_loglift:.4f} '
        f'vs frequency-matched decoys = {dl.mean():+.4f} +- {dl.std():.4f} (z = +{z_ll:.2f}, P = {p_ll:.5f})')
    return dict(
        test=f'OOS_NewTexts_{label}', n_units=n_u,
        real_hits=real_hits, decoy_hits_mean=round(float(dh.mean()), 2), decoy_hits_sd=round(float(dh.std()), 2),
        z_hits=round(float(z_ht), 3), p_hits=round(float(p_ht), 5),
        real_loglift=round(real_loglift, 4), decoy_loglift_mean=round(float(dl.mean()), 4),
        z_loglift=round(float(z_ll), 3), p_loglift=round(float(p_ll), 5),
    )


t1_signs = run_oos_prediction(['SIGN'], new_sign_vecs, min_new_occ=2, p_cut=0.02, label='SIGNS')
t1_phrases = run_oos_prediction(['PHRASE2', 'PHRASE3'], new_p2_vecs, min_new_occ=1, p_cut=0.02, label='PHRASES')


# ---------------- TEST 2: Inscription-Internal Domain Coherence on Held-Out `New Texts` ----------------
log('=== Global Test 2: Inscription-Internal Physical-Domain Coherence on Held-Out New Texts ===')
sa = pd.read_csv(os.path.join(OUT, 'sign_anchors.csv'), dtype=str).fillna('')
sa_primary = sa.drop_duplicates('sign').copy()
anchored_signs = sorted(sa_primary.sign.tolist())
s2idx = {s: i for i, s in enumerate(anchored_signs)}
K_S = len(anchored_signs)

# Build (K_S, 13) boolean matrix of Lipi-derived CATS masks & source_domain family per sign
B_cats = np.zeros((K_S, len(CATS)), dtype=float)
dom_fam = []
v2_cls = []
freqs_s = []
for i, s in enumerate(anchored_signs):
    row = sa_primary[sa_primary.sign == s].iloc[0]
    mask = int(row['cat_mask'])
    for b in range(len(CATS)):
        if (mask >> b) & 1:
            B_cats[i, b] = 1.0
    dom_fam.append(row['source_domain'])
    v2_cls.append(row['v2_class'])
    freqs_s.append(lipi_sign_tot[s])

freqs_s = np.array(freqs_s)
q1, q2 = np.quantile(freqs_s, [1 / 3, 2 / 3])
fbands = np.array([0 if f <= q1 else (1 if f <= q2 else 2) for f in freqs_s])

# Learn 13x13 CATS co-occurrence lift strictly on LIPI events!
n_mat = np.zeros((13, 13), dtype=float)
marg = np.zeros(13, dtype=float)
tot_pairs = 0.0
for r in ev_lipi:
    us = [s2idx[s] for s in r['signs'] if s in s2idx]
    if len(us) < 2:
        continue
    for a in us:
        for b in us:
            if a == b:
                continue
            n_mat += np.outer(B_cats[a], B_cats[b])
            marg += B_cats[a]
            tot_pairs += 1.0
p_marg = marg / max(tot_pairs, 1.0)
exp_pairs = tot_pairs * np.outer(p_marg, p_marg)
lift_13 = np.log((n_mat + 1.0) / (exp_pairs + 1.0))

# Pairwise sign-to-sign compatibility score under assignment perm:
# S_pair[u, v] = mean CATS-lift + 0.5 * same_source_domain_bonus
dom_eq = np.array([[1.0 if dom_fam[i] == dom_fam[j] else 0.0 for j in range(K_S)] for i in range(K_S)])
norm_B = B_cats / np.maximum(B_cats.sum(axis=1, keepdims=True), 1.0)
cat_lift_pair = norm_B @ lift_13 @ norm_B.T

# Extract all unordered pairs of distinct anchored signs co-occurring on held-out `new texts`!
new_pair_counts = collections.Counter()
n_new_scored = 0
for r in ev_new:
    us = sorted({s2idx[s] for s in r['signs'] if s in s2idx})
    if len(us) < 2:
        continue
    n_new_scored += 1
    w = 1.0 / (len(us) * (len(us) - 1) / 2.0)
    for idx1 in range(len(us)):
        for idx2 in range(idx1 + 1, len(us)):
            new_pair_counts[(us[idx1], us[idx2])] += w

u_arr = np.array([k[0] for k in new_pair_counts.keys()], dtype=int)
v_arr = np.array([k[1] for k in new_pair_counts.keys()], dtype=int)
w_arr = np.array(list(new_pair_counts.values()), dtype=float)
w_arr /= w_arr.sum()

real_same_dom = float((dom_eq[u_arr, v_arr] * w_arr).sum())
real_cat_lift = float((cat_lift_pair[u_arr, v_arr] * w_arr).sum())

# Shuffle within (v2_class, freq_band) cells (and fallback freq_band if singleton)
cells = collections.defaultdict(list)
for i in range(K_S):
    cells[(v2_cls[i], fbands[i])].append(i)
# Merge singleton cells into same freq_band so every sign moves in shuffles!
merged_cells = collections.defaultdict(list)
for (vc, fb), idxs in cells.items():
    if len(idxs) >= 2:
        merged_cells[(vc, fb)].extend(idxs)
    else:
        merged_cells[('MISC', fb)].extend(idxs)
cell_arrays = [np.array(v, dtype=int) for v in merged_cells.values() if len(v) >= 2]

shuf_same_dom = []
shuf_cat_lift = []
base_idx = np.arange(K_S)
for _ in range(N_SHUF):
    perm = base_idx.copy()
    for ca in cell_arrays:
        perm[ca] = rng.permutation(ca)
    shuf_same_dom.append(float((dom_eq[perm[u_arr], perm[v_arr]] * w_arr).sum()))
    shuf_cat_lift.append(float((cat_lift_pair[perm[u_arr], perm[v_arr]] * w_arr).sum()))

sd_arr = np.array(shuf_same_dom)
cl_arr = np.array(shuf_cat_lift)
z_sd = (real_same_dom - sd_arr.mean()) / max(sd_arr.std(), 1e-6)
p_sd = (1.0 + (sd_arr >= real_same_dom).sum()) / (N_SHUF + 1.0)
z_cl = (real_cat_lift - cl_arr.mean()) / max(cl_arr.std(), 1e-6)
p_cl = (1.0 + (cl_arr >= real_cat_lift).sum()) / (N_SHUF + 1.0)

log(f'  Scored {n_new_scored} held-out `new text` inscriptions containing >=2 Lipi-anchored signs:')
log(f'    Same-physical-domain co-occurrence: real = {real_same_dom:.4f} '
    f'vs class+freq matched decoys = {sd_arr.mean():.4f} +- {sd_arr.std():.4f} (z = +{z_sd:.2f}, P = {p_sd:.5f})')
log(f'    Lipi-learned CATS coherence lift  : real = {real_cat_lift:+.4f} '
    f'vs class+freq matched decoys = {cl_arr.mean():+.4f} +- {cl_arr.std():.4f} (z = +{z_cl:.2f}, P = {p_cl:.5f})')


# ---------------- TEST 3: Ideographic vs. Rebus Boundary Across Syntactic Slots ----------------
log('=== Global Test 3: Visual Glyph Iconography vs. Contextual Physical Domain by Slot ===')


def visual_cats_of_shape(desc):
    """Purely visual glyph classification from Wells shape_description (zero context used)."""
    s = desc.lower()
    if not s:
        return set()
    vc = set()
    if any(w in s for w in ('tree', 'leaf', 'leaves', 'plant', 'wheat', 'flower', 'branch')):
        vc.add('plant')
    if any(w in s for w in ('person', 'man', 'arms', 'breasts', 'heads', 'knees')):
        vc.add('person')
    if any(w in s for w in ('fish', 'bird', 'spider', 'animal', 'paw')):
        vc.add('animal')
    if any(w in s for w in ('jar', 'bow', 'arrow', 'table', 'wheel', 'pitchfork', 'pincer', 'box', 'square', 'U with', 'simple u')):
        vc.add('tool')
        vc.add('measure')
    if any(w in s for w in ('grid', 'mountain', 'stripes', 'triangle with horizontal')):
        vc.add('place')
    if re.search(r'\b(one|two|three|four|five|six|seven)\b.*stroke', s):
        vc.add('number')
    return vc


vis_rows = []
for _, r in sa.iterrows():
    vc = visual_cats_of_shape(r['shape_desc'])
    if not vc:
        continue
    ctx_c = set(r['cats'].split('|')) - {''}
    hit = int(bool(vc & ctx_c))
    is_name_slot = (r['slot'] in ('NAME', 'NAME_CREST', 'PRE_CLOSER')) or (
        r['slot'] == 'ANY' and r['v2_class'] in ('CREST', 'PERSONAL', 'NAME_BACK')
    )
    vis_rows.append(dict(sign=r['sign'], slot=r['slot'], v2=r['v2_class'],
                         is_name=is_name_slot, vis=vc, ctx=ctx_c, hit=hit))

vdf = pd.DataFrame(vis_rows)
func_df = vdf[~vdf.is_name].reset_index(drop=True)
name_df = vdf[vdf.is_name].reset_index(drop=True)


def eval_vis_match(sub_vdf, label):
    n = len(sub_vdf)
    real_m = float(sub_vdf.hit.mean())
    vis_list = list(sub_vdf.vis)
    ctx_list = list(sub_vdf.ctx)
    sims = []
    for _ in range(N_SHUF):
        perm = rng.permutation(n)
        sims.append(np.mean([1.0 if (vis_list[i] & ctx_list[perm[i]]) else 0.0 for i in range(n)]))
    sims = np.array(sims)
    z = (real_m - sims.mean()) / max(sims.std(), 1e-6)
    p = (1.0 + (sims >= real_m).sum()) / (N_SHUF + 1.0)
    log(f'  [{label}] n={n} pictured anchors: visual-to-context match = {real_m*100:.1f}% ({int(sub_vdf.hit.sum())}/{n}) '
        f'vs shuffled = {sims.mean()*100:.1f}% +- {sims.std()*100:.1f}% (z = {z:+.2f}, P = {p:.5f})')
    return dict(group=label, n=n, hits=int(sub_vdf.hit.sum()), real_rate=round(real_m, 4),
                shuf_mean=round(float(sims.mean()), 4), z=round(float(z), 3), p=round(float(p), 5))


v_all = eval_vis_match(vdf, 'ALL_SLOTS')
v_func = eval_vis_match(func_df, 'NON_NAME_SLOTS (COUNTED/SOLO/FRONT/ENDING/MEASURE/THING)')
v_name = eval_vis_match(name_df, 'NAME_SLOTS (NAME/CREST/PRE_CLOSER/PERSONAL)')

summary_json = dict(
    oos_signs=t1_signs,
    oos_phrases=t1_phrases,
    coherence_new_texts=dict(
        n_inscriptions=n_new_scored,
        real_same_dom=round(real_same_dom, 4), decoy_same_dom=round(float(sd_arr.mean()), 4),
        z_same_dom=round(float(z_sd), 3), p_same_dom=round(float(p_sd), 5),
        real_cat_lift=round(real_cat_lift, 4), decoy_cat_lift=round(float(cl_arr.mean()), 4),
        z_cat_lift=round(float(z_cl), 3), p_cat_lift=round(float(p_cl), 5),
    ),
    ideographic_boundary=dict(all=v_all, functional_slots=v_func, name_slots=v_name),
)
with open(os.path.join(OUT, 'global_validation.json'), 'w') as fh:
    json.dump(summary_json, fh, indent=2)
log('Saved work_data/sem/global_validation.json.')
