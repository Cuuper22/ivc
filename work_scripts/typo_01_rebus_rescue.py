#!/usr/bin/env python3
"""typo_01_rebus_rescue.py -- Execute all 4 Unrun Rebus Rescues from jobs/out/language_machine2.md
plus the Multi-Sign Graphic Compound & Swap Phonetic Test and Dense Embedding Redesign.

Rescues executed:
  (1a) High-Signal Core Slot Restriction:
       Evaluate nested closed grammatical/accounting sign sets (T1_CloserTitle [24 signs],
       T2_CoreV2_5 [CLOSER,TITLE,MEASURE,OPEN,SLOT: 33 signs], T3_CoreGram_53 [closed core: 53 signs],
       T4_AllClosed_74 [all non-PERSONAL signs: 74 signs]) vs Full_235 (diluted by 161 PERSONAL signs).
  (1b) Cognate-Root / Etymon Clustering + Base-Rate-Adjusted Controls + Derivational-Cluster C3:
       Score cognate-filtered & homonym-resolved lexicons across all 7 families (Proto-Dravidian >=2-branch
       DEDR cognates + Cf.-merged roots, Pre-IA Proto-Munda + North/South Munda cognates, Turner OIA + PII
       cognates, Elamite roots, Sumerian roots, Akkadian Semitic root clusters, pooled Burushaski) against:
         - C1_adj: class shuffle (base-rate adjusted)
         - C2_adj: outside drawable noun decoys (base-rate adjusted)
         - C3_clust: derivational-cluster-preserving sound shuffle (base-rate adjusted) + C3_entry
         - C4_adj: wrong class for same picture (base-rate adjusted)
       Plus Redesign 1b-R: Dense Multilingual Embedding Rebus Alignment (/tmp/dict_emb/emb_m2v.npy)
       eliminating rigid English/German keyword lists!
  (1c) Multi-Sign Graphic Compound & Swap Phonetic Test:
       - 99-of-830 fish-mark decompositions ([modifier] + [plain fish 220]) & all 149 compound decompositions
         (one_for_two.csv) + held-out Mahadevan new-texts (1,183 lines) verification:
         (i) Double-Rebus Modifier+Base Bridge score vs 2,000 random (modifier, base) pairs & C3 shuffles
         (ii) Attested Dictionary Compound Headword match rate vs 2,000 shuffled (modifier, base) pairs
       - Rescued Swap Pairs (swap_pairs.csv): All 108 pairs on homonym-fixed cognate lexicons vs
         filtered Non-Personal / Allographic Swap Pairs (removing '[opener]-NameA/NameB-[740]' name slots).

Outputs (work_data/typo/):
  - rebus_rescue_grid.csv
  - rebus_rescue_summary.csv
  - rebus_embedding_redesign.csv
  - compound_swap_results.csv
  - rebus_rescued_candidates.csv (real vs matched same-class decoy pairings)
"""
import os, sys, re, csv, json, time, collections, itertools, unicodedata
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "work_scripts"))

TMP_LEX = "/tmp/typo_lex"
OUT_DIR = os.path.join(ROOT, "work_data", "typo")
os.makedirs(OUT_DIR, exist_ok=True)

t0 = time.time()
def log(*a):
    print(f"[typo_01 {time.time()-t0:6.1f}s]", *a, flush=True)

# Always ensure updated lexicons exist
import typo_00_lexicons
if not os.path.exists(os.path.join(TMP_LEX, "pdrav_2branch.tsv")) or os.environ.get("TYPO_REBUILD_LEX") == "1":
    log("Building cognate & homonym-resolved lexicons via typo_00_lexicons...")
    typo_00_lexicons.main()

from lang_m2_common import (
    CLASSES, CLS, MOVES, DE, OUTSIDE, DISTS, BREADTHS, KEYS,
    pic_terms_en, kw_terms, blind_nouns, outside_list, plain
)

GERMAN_LEX = {"elamite_hinzkoch", "elamite_roots"}

COGNATE_FAMILIES = collections.OrderedDict([
    ("Dravidian", ["pdrav_2branch"]),
    ("Munda", ["pmunda_cognates"]),
    ("Indo-Aryan", ["oia_cognates"]),
    ("Elamite", ["elamite_roots"]),
    ("Sumerian", ["sumerian_roots"]),
    ("Akkadian", ["akkadian_roots"]),
    ("Burushaski", ["burushaski_all"]),
])

DAUGHTER_POOLS = collections.OrderedDict([
    ("Dravidian_daughters", ["dedr_tamil", "dedr_malayalam", "dedr_kannada", "dedr_telugu"]),
    ("Dravidian_cfmerged", ["pdrav_2branch_cfmerged"]),
    ("Munda_daughters", ["santali_campbell", "santali_bodding5", "santali_wiktionary", "mundari_bhadra", "kharia_druart"]),
    ("Indo-Aryan_turner", ["oia_turner", "proto_indoiranian"]),
    ("Sumerian_daughters", ["sumerian_halloran", "sumerian_wiktionary"]),
])


def sense_words(gl, max_per_sense):
    """Extract words up to max_per_sense from EACH ';'-separated sense in gloss."""
    out = []
    for seg in str(gl).split(';'):
        ws = re.findall(r'[a-z]+', plain(seg))[:max_per_sense]
        out.append(ws)
    return out


class CognateLex:
    """Cognate-aware lexicon with eid (etymon) and cid (derivational cluster)."""
    def __init__(self, name, nouns, outside):
        self.name = name
        self.de = name in GERMAN_LEX
        path = os.path.join(TMP_LEX, f"{name}.tsv")
        rows = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8") if "\t" in l]
        self.eid = [r[0] for r in rows]
        self.cid = [r[1] for r in rows]
        self.hw = [r[2] for r in rows]
        self.nf = [r[3] for r in rows]
        self.sk = [r[4] for r in rows]
        self.gl = [r[5] for r in rows]
        self.n = len(rows)
        self.nentries = len(set(self.eid))
        self.nclusters = len(set(self.cid))
        self.eid_arr = np.array(self.eid)
        self.cid_arr = np.array(self.cid)
        eid_map = {e: idx for idx, e in enumerate(dict.fromkeys(self.eid))}
        self.eid_int = np.array([eid_map[e] for e in self.eid], dtype=np.int32)
        self._near_cache = {d: {} for d in DISTS}

        inv3 = collections.defaultdict(set)
        inv5 = collections.defaultdict(set)
        for i, g in enumerate(self.gl):
            for ws in sense_words(g, 5):
                for k, w in enumerate(ws):
                    forms = {w} | ({w[:-1]} if w.endswith('s') else set()) | ({w[:-2]} if w.endswith('es') else set())
                    for f_ in forms:
                        inv5[f_].add(i)
                        if k < 3:
                            inv3[f_].add(i)

        terms = {}
        for nn in nouns:
            terms[nn] = set(DE.get(nn, '').split()) if self.de else pic_terms_en(nn)
        for e, d in outside:
            terms[f"OUT:{e}"] = {d if self.de else e}

        self.pic_flag = {k: set().union(*[inv3.get(t, set()) for t in ts]) if ts else set() for k, ts in terms.items()}
        self.is_pic = {k: sorted(v) for k, v in self.pic_flag.items()}

        self.kwkeys = [(c, b) for c in CLS for b in BREADTHS]
        self.kwmat = np.zeros((self.n, len(self.kwkeys)), dtype=bool)
        for col, (c, b) in enumerate(self.kwkeys):
            for t in kw_terms(c, b, self.de):
                for i in inv5.get(t, ()):
                    self.kwmat[i, col] = True

        # Dictionary-wide base rate per (class, breadth)
        self.baserate = self.kwmat.mean(axis=0) if self.n > 0 else np.zeros(len(self.kwkeys))

        self.by_nf = collections.defaultdict(list)
        self.by_sk = collections.defaultdict(list)
        self.by_del = collections.defaultdict(list)
        for i in range(self.n):
            self.by_nf[self.nf[i]].append(i)
            self.by_sk[self.sk[i]].append(i)
            for key in self.dels(self.sk[i]):
                self.by_del[key].append(i)

    @staticmethod
    def dels(s):
        if len(s) < 2:
            return {('=', s)}
        return {('=', s)} | {('-', s[:k] + s[k + 1:]) for k in range(len(s))} | {('+', s)}

    def near_form(self, nf, dist):
        cache = self._near_cache[dist]
        arr = cache.get(nf)
        if arr is not None:
            return arr
        if dist == 'strict':
            res = self.by_nf.get(nf, [])
        else:
            sk = re.sub(r'[aeiou]', '', nf)
            if dist == 'medium' or len(sk) < 2:
                res = self.by_sk.get(sk, [])
            else:
                out = set()
                mine = {('-', sk[:k] + sk[k + 1:]) for k in range(len(sk))}
                for key in mine:
                    out.update(self.by_del.get(key, []))
                    out.update(i for i in self.by_sk.get(key[1], []))
                for i in self.by_del.get(('-', sk), []):
                    out.add(i)
                out.update(self.by_sk.get(sk, []))
                res = [i for i in out if len(self.sk[i]) >= 2 or self.sk[i] == sk]
        arr = np.asarray(res, dtype=np.int32)
        cache[nf] = arr
        return arr


def compute_matrices(L, nouns, perm=None, evidence=None, ev_cls=None):
    """Returns {(dist, breadth): (H[noun, cls], T[noun])} where sound-alikes come from DIFFERENT eid."""
    CI = {c: i for i, c in enumerate(CLS)}
    out = {k: (np.zeros((len(nouns), len(CLS)), np.float32), np.zeros(len(nouns), np.float32)) for k in KEYS}
    inv = None
    if perm is not None:
        inv = np.empty_like(perm)
        inv[perm] = np.arange(len(perm), dtype=np.int32)
    qmask = np.zeros(L.n, dtype=bool)
    for a, noun in enumerate(nouns):
        pws = L.is_pic.get(noun, [])
        if not pws:
            continue
        pf_arr = np.asarray(pws, dtype=np.int32)
        for d in DISTS:
            qmask.fill(False)
            for pw in pws:
                f = L.nf[pw] if perm is None else L.nf[perm[pw]]
                c = L.near_form(f, d)
                if len(c) == 0:
                    continue
                if perm is not None:
                    c = inv[c]
                valid = c[L.eid_int[c] != L.eid_int[pw]]
                if len(valid) == 0:
                    continue
                qmask[valid] = True
                if evidence is not None and d in ('strict', 'medium'):
                    pf_set = L.pic_flag[noun]
                    for q in valid:
                        q_i = int(q)
                        if q_i in pf_set:
                            continue
                        for col in np.nonzero(L.kwmat[q_i])[0]:
                            cc, b = L.kwkeys[col]
                            if ev_cls is None or cc in ev_cls.get(noun, ()):
                                evidence.append({
                                    'dict': L.name, 'dist': d, 'breadth': b, 'noun': noun, 'cls': cc,
                                    'picture_word': L.hw[pw], 'picture_eid': L.eid[pw], 'picture_cid': L.cid[pw],
                                    'picture_gloss': L.gl[pw][:80],
                                    'soundalike': L.hw[q_i], 'soundalike_eid': L.eid[q_i], 'soundalike_cid': L.cid[q_i],
                                    'soundalike_gloss': L.gl[q_i][:100],
                                    'same_deriv_cluster': int(L.cid[pw] == L.cid[q_i]),
                                })
            qmask[pf_arr] = False
            cnt_q = int(qmask.sum())
            if cnt_q == 0:
                continue
            km = L.kwmat[qmask].sum(axis=0)
            for col, (cc, b) in enumerate(L.kwkeys):
                out[(d, b)][0][a, CI[cc]] = km[col]
            for b in BREADTHS:
                out[(d, b)][1][a] = cnt_q
    return out


def make_perm_generator(id_list, n_total, rng):
    """Build stratified block-permutation generator (shuffles whole clusters/entries of equal row count)."""
    groups = collections.OrderedDict()
    for i, gid in enumerate(id_list):
        groups.setdefault(gid, []).append(i)
    strata = collections.defaultdict(list)
    for gid, rows_ in groups.items():
        strata[len(rows_)].append(rows_)
    # Merge singleton/rare large strata (>5 rows) into nearest bucket by cutting/grouping if needed,
    # or permute exact-size strata (covers >98% of entries cleanly)
    exact_strata = {k: np.array(v, dtype=np.int32) for k, v in strata.items() if len(v) >= 2}
    def gen():
        perm = np.arange(n_total, dtype=np.int32)
        for k_, src in exact_strata.items():
            dst = src[rng.permutation(len(src))]
            perm[src.ravel()] = dst.ravel()
        return perm
    return gen


# ==============================================================================
# BUILD SIGN & UNIT TIERS FOR RESCUE 1(a)
# ==============================================================================
def build_unit_tiers():
    sgs = list(csv.DictReader(open(os.path.join(ROOT, "work_data", "lang_m2", "signs.csv"), encoding="utf-8")))
    cv2 = {r['sign']: r['v2_base'] for r in csv.DictReader(open(os.path.join(ROOT, "work_data", "frame", "classes_v2.csv"), encoding="utf-8"))}

    # Keep blind 3of3 + 2of3 pictured signs (and also track 3of3-only subset for CoreGram)
    valid_b = [r for r in sgs if r['level'] in ('3of3', '2of3') and r['cls'] and r['nouns']]
    for r in valid_b:
        r['v2'] = cv2.get(r['sign'], 'PERSONAL')

    tiers_signs = collections.OrderedDict([
        # Rescue #3 in language_machine2.md line 17: closing & title signs only
        ("T1_CloserTitle_24", [r for r in valid_b if r['cls'] in ('H10_0', 'H10_8')]),
        # Prompt 1(a) strict Frame v2 closed grammatical/accounting core
        ("T2_CoreV2_33", [r for r in valid_b if r['v2'] in ('CLOSER', 'TITLE', 'MEASURE', 'OPEN', 'SLOT')]),
        # Prompt 1(a) ~45-60 closed grammatical/accounting core (HMM core H10_0,8,1,5 + Frame v2 OPEN/MEASURE/AFTER_M)
        ("T3_CoreGram_53", [r for r in valid_b if (r['cls'] in ('H10_0', 'H10_8', 'H10_1', 'H10_5') or r['v2'] in ('CLOSER', 'TITLE', 'MEASURE', 'OPEN', 'SLOT', 'AFTER_M'))]),
        # All non-PERSONAL closed-class signs in Frame v2 (eliminating the 161 PERSONAL name signs!)
        ("T4_AllClosed_74", [r for r in valid_b if r['v2'] != 'PERSONAL']),
        # Also 3of3-only version of CoreGram for strict picture check
        ("T3_CoreGram_3of3", [r for r in valid_b if r['level'] == '3of3' and (r['cls'] in ('H10_0', 'H10_8', 'H10_1', 'H10_5') or r['v2'] in ('CLOSER', 'TITLE', 'MEASURE', 'OPEN', 'SLOT', 'AFTER_M'))]),
        # Original lang_m2 diluted set (235 signs, 161 PERSONAL)
        ("T5_FullDiluted_235", valid_b),
    ])

    tiers_units = collections.OrderedDict()
    for tname, s_list in tiers_signs.items():
        us = collections.OrderedDict()
        for r in s_list:
            key = ('|'.join(sorted(r['nouns'].split(';'))), r['cls'])
            us.setdefault(key, []).append(r['sign'])
        u_list = [{'nouns': ns, 'cls': c, 'cls_name': CLASSES[c][0], 'signs': '/'.join(ss)} for (ns, c), ss in us.items()]
        tiers_units[tname] = (len(s_list), u_list)
        log(f"Tier {tname:20s}: {len(s_list):3d} signs -> {len(u_list):3d} units | classes: {dict(collections.Counter(u['cls'] for u in u_list))}")
    return tiers_units


# ==============================================================================
# RUN RESCUES 1(a) & 1(b): CORE SLOT RESTRICTION + COGNATE ROOTS + BASE-RATE CONTROLS
# ==============================================================================
def run_rebus_rescues(tiers_units):
    rng = np.random.default_rng(20261118)
    NOUNS = blind_nouns()
    NI = {n: i for i, n in enumerate(NOUNS)}
    OUTS = outside_list()
    OUTN = [f"OUT:{e}" for e, _ in OUTS]
    CI = {c: i for i, c in enumerate(CLS)}
    N1, N2, N4 = 2000, 2000, 2000
    N3 = int(os.environ.get("TYPO_N3", 500))

    # Collect all dictionaries needed across Cognate Families + Daughter Pools
    all_dicts = sorted({d for pool in list(COGNATE_FAMILIES.values()) + list(DAUGHTER_POOLS.values()) for d in pool})

    ev_cls = collections.defaultdict(set)
    for _, (_, ulist) in tiers_units.items():
        for u in ulist:
            for n in u['nouns'].split('|'):
                ev_cls[n].add(u['cls'])

    lex_objs = {}
    real_m, out_m, c3_clust_m, c3_entry_m, br_map = {}, {}, {}, {}, {}
    evidence = []

    for dname in all_dicts:
        L = CognateLex(dname, NOUNS, OUTS)
        lex_objs[dname] = L
        real_m[dname] = compute_matrices(L, NOUNS, evidence=evidence, ev_cls=ev_cls)
        out_m[dname] = compute_matrices(L, OUTN)
        br_map[dname] = {
            b: np.array([L.kwmat[:, L.kwkeys.index((c, b))].sum() for c in CLS], dtype=np.float64)
            for b in BREADTHS
        }
        br_map[dname]['_n'] = max(1, L.n)

        gen_clust = make_perm_generator(L.cid, L.n, rng)
        gen_entry = make_perm_generator(L.eid, L.n, rng)
        runs_c, runs_e = [], []
        same_ce = (L.nclusters == L.nentries)
        for t in range(N3):
            runs_c.append(compute_matrices(L, NOUNS, perm=gen_clust()))
            if not same_ce:
                runs_e.append(compute_matrices(L, NOUNS, perm=gen_entry()))
        c3_clust_m[dname] = runs_c
        c3_entry_m[dname] = runs_c if same_ce else runs_e
        cov = sum(1 for n in NOUNS if L.is_pic.get(n))
        log(f"Scored {dname:24s}: {L.n:5d} rows, {L.nentries:5d} etyma, {L.nclusters:5d} clusters, pic_cov={cov}/{len(NOUNS)}")

    # Pre-draw outside-noun mappings (shared across tiers & families)
    maps2 = [rng.choice(len(OUTN), size=len(NOUNS), replace=False) for _ in range(N2)]

    grid_rows = []
    sum_rows = []
    unit_hit_rows = []

    eval_groups = list(COGNATE_FAMILIES.items()) + list(DAUGHTER_POOLS.items())

    for tname, (n_signs, units) in tiers_units.items():
        nU = len(units)
        ar = np.arange(nU)
        A = np.zeros((nU, len(NOUNS)), dtype=np.float32)
        for i, u in enumerate(units):
            for n in u['nouns'].split('|'):
                A[i, NI[n]] = 1.0
        cls = np.array([CI[u['cls']] for u in units], dtype=np.int32)

        # Shared class shuffles C1 and wrong-class-same-picture C4 within this tier
        P1 = np.array([rng.permutation(cls) for _ in range(N1)], dtype=np.int32)
        groups = collections.defaultdict(list)
        for i, u in enumerate(units):
            groups[u['nouns']].append(i)
        # Weight C4 draws across all 10 classes (or tier classes if >=3 available) so single-noun units always get a true wrong class
        cfreq_all = np.bincount(cls, minlength=len(CLS)).astype(float) + 0.25
        P4 = np.tile(cls, (N4, 1))
        for t in range(N4):
            for g in groups.values():
                avail = np.array([c for c in range(len(CLS)) if c not in set(cls[g])], dtype=np.int32)
                w_ = cfreq_all[avail]
                w_ = w_ / w_.sum()
                P4[t, g] = rng.choice(avail, size=len(g), replace=len(avail) < len(g), p=w_)

        def eval_stats(H, T, C, br_vec):
            """Returns (hits, raw_share, adj_share) for class vector/matrix C."""
            UH = A @ H
            UT = A @ T
            UB = (A @ (H > 0)) > 0
            C2d = np.atleast_2d(C)
            hits = UB[ar[None, :], C2d].sum(axis=1)
            ok = UT > 0
            with np.errstate(invalid='ignore', divide='ignore'):
                raw_u = np.where(ok[None, :], UH[ar[None, :], C2d] / UT[None, :], 0.0)
                adj_u = np.where(ok[None, :], raw_u - br_vec[C2d], 0.0)
            return hits, raw_u.sum(axis=1), adj_u.sum(axis=1)

        for g_label, dnames in eval_groups:
            is_primary_cog = g_label in COGNATE_FAMILIES
            z_c3_list, z_c1_list, z_c2_list, z_c4_list = [], [], [], []
            cov_nouns = set().union(*[{n for n in NOUNS if lex_objs[dn].is_pic.get(n)} for dn in dnames])
            n_cov_units = sum(1 for u in units if any(x in cov_nouns for x in u['nouns'].split('|')))

            for k in KEYS:
                d_str, b_str = k
                H = sum(real_m[dn][k][0] for dn in dnames)
                T = sum(real_m[dn][k][1] for dn in dnames)
                br_vec = sum(br_map[dn][b_str] for dn in dnames) / sum(br_map[dn]['_n'] for dn in dnames)

                r_hits, r_raw, r_adj = eval_stats(H, T, cls, br_vec)
                c1_hits, c1_raw, c1_adj = eval_stats(H, T, P1, br_vec)
                c4_hits, c4_raw, c4_adj = eval_stats(H, T, P4, br_vec)

                H_out = sum(out_m[dn][k][0] for dn in dnames)
                T_out = sum(out_m[dn][k][1] for dn in dnames)
                c2_res = [eval_stats(H_out[m], T_out[m], cls, br_vec) for m in maps2]
                c2_hits = np.array([x[0][0] for x in c2_res])
                c2_adj = np.array([x[2][0] for x in c2_res])

                c3c_res = [eval_stats(sum(c3_clust_m[dn][t][k][0] for dn in dnames),
                                      sum(c3_clust_m[dn][t][k][1] for dn in dnames), cls, br_vec) for t in range(N3)]
                c3c_hits = np.array([x[0][0] for x in c3c_res])
                c3c_adj = np.array([x[2][0] for x in c3c_res])

                c3e_res = [eval_stats(sum(c3_entry_m[dn][t][k][0] for dn in dnames),
                                      sum(c3_entry_m[dn][t][k][1] for dn in dnames), cls, br_vec) for t in range(N3)]
                c3e_adj = np.array([x[2][0] for x in c3e_res])

                def p_And_z(obs, null_arr):
                    null_arr = np.asarray(null_arr, dtype=np.float64)
                    p = (1.0 + np.sum(null_arr >= obs - 1e-9)) / (1.0 + len(null_arr))
                    sd = null_arr.std()
                    z_obs = 0.0 if sd < 1e-12 else (obs - null_arr.mean()) / sd
                    z_null = np.zeros_like(null_arr) if sd < 1e-12 else (null_arr - null_arr.mean()) / sd
                    return round(float(null_arr.mean()), 4), round(float(p), 4), round(float(z_obs), 3), z_null

                c1_m, c1_p, c1_z, c1_zn = p_And_z(r_adj[0], c1_adj)
                c2_m, c2_p, c2_z, c2_zn = p_And_z(r_adj[0], c2_adj)
                c3_m, c3_p, c3_z, c3_zn = p_And_z(r_adj[0], c3c_adj)
                c3e_m, c3e_p, c3e_z, _  = p_And_z(r_adj[0], c3e_adj)
                c4_m, c4_p, c4_z, c4_zn = p_And_z(r_adj[0], c4_adj)

                _, h_c1_p, _, _ = p_And_z(r_hits[0], c1_hits)
                _, h_c2_p, _, _ = p_And_z(r_hits[0], c2_hits)
                h_c3_m, h_c3_p, h_c3_z, _ = p_And_z(r_hits[0], c3c_hits)
                _, h_c4_p, _, _ = p_And_z(r_hits[0], c4_hits)

                z_c3_list.append((c3_z, c3_zn))
                z_c1_list.append((c1_z, c1_zn))
                z_c2_list.append((c2_z, c2_zn))
                z_c4_list.append((c4_z, c4_zn))

                adj_all4 = (c1_p < 0.05 and c2_p < 0.05 and c3_p < 0.05 and c4_p < 0.05)
                hits_all4 = (h_c1_p < 0.05 and h_c2_p < 0.05 and h_c3_p < 0.05 and h_c4_p < 0.05)

                grid_rows.append({
                    'tier': tname, 'signs': n_signs, 'units': nU, 'covered_units': n_cov_units,
                    'family_or_pool': g_label, 'is_cognate_lex': int(is_primary_cog),
                    'dist': d_str, 'breadth': b_str,
                    'hits': int(r_hits[0]), 'hits_c3_mean': round(h_c3_m, 2), 'hits_c3_P': h_c3_p, 'hits_all4': int(hits_all4),
                    'raw_share': round(float(r_raw[0]), 4),
                    'adj_share': round(float(r_adj[0]), 4),
                    'c1_adj_mean': c1_m, 'c1_P': c1_p, 'c1_z': c1_z,
                    'c2_adj_mean': c2_m, 'c2_P': c2_p, 'c2_z': c2_z,
                    'c3_clust_mean': c3_m, 'c3_clust_P': c3_p, 'c3_clust_z': c3_z,
                    'c3_entry_mean': c3e_m, 'c3_entry_P': c3e_p, 'c3_entry_z': c3e_z,
                    'c4_adj_mean': c4_m, 'c4_P': c4_p, 'c4_z': c4_z,
                    'adj_all4': int(adj_all4),
                })

                # Save per-unit hits on T3_CoreGram_53 and T2_CoreV2_33 for candidate extraction
                if is_primary_cog and tname in ("T2_CoreV2_33", "T3_CoreGram_53"):
                    UB = (A @ (H > 0)) > 0
                    uhit = UB[ar, cls]
                    c3_uhit_rate = np.mean([
                        ((A @ (sum(c3_clust_m[dn][t][k][0] for dn in dnames) > 0)) > 0)[ar, cls]
                        for t in range(N3)
                    ], axis=0)
                    for i, u in enumerate(units):
                        unit_hit_rows.append({
                            'tier': tname, 'family': g_label, 'dist': d_str, 'breadth': b_str,
                            'nouns': u['nouns'], 'cls': u['cls'], 'cls_name': u['cls_name'],
                            'signs': u['signs'], 'real_hit': int(uhit[i]),
                            'c3_clust_hit_rate': round(float(c3_uhit_rate[i]), 4)
                        })

            def comb_z(zlist):
                rm = float(np.mean([x[0] for x in zlist]))
                nm = np.mean([x[1] for x in zlist], axis=0)
                p = (1.0 + np.sum(nm >= rm - 1e-12)) / (1.0 + len(nm))
                return round(rm, 3), round(float(p), 4)

            Z3, Z3_P = comb_z(z_c3_list)
            Z1, Z1_P = comb_z(z_c1_list)
            Z2, Z2_P = comb_z(z_c2_list)
            Z4, Z4_P = comb_z(z_c4_list)
            sub_cells = grid_rows[-len(KEYS):]
            beat4 = sum(r['adj_all4'] + r['hits_all4'] for r in sub_cells)
            sum_rows.append({
                'tier': tname, 'signs': n_signs, 'units': nU, 'covered_units': n_cov_units,
                'family_or_pool': g_label, 'is_cognate_lex': int(is_primary_cog),
                'cells': 12, 'beat_all4': beat4,
                'Z1_adj': Z1, 'Z1_P': Z1_P,
                'Z2_adj': Z2, 'Z2_P': Z2_P,
                'Z3_clust': Z3, 'Z3_clust_P': Z3_P,
                'Z4_adj': Z4, 'Z4_P': Z4_P,
            })
            if is_primary_cog:
                log(f"SUMMARY {tname:20s} | {g_label:11s}: beat_all4={beat4}/12 | "
                    f"Z1={Z1:+.2f}(P={Z1_P:.3f}) Z2={Z2:+.2f}(P={Z2_P:.3f}) Z3_clust={Z3:+.2f}(P={Z3_P:.3f}) Z4={Z4:+.2f}(P={Z4_P:.3f})")

    pd.DataFrame(grid_rows).to_csv(os.path.join(OUT_DIR, "rebus_rescue_grid.csv"), index=False)
    pd.DataFrame(sum_rows).to_csv(os.path.join(OUT_DIR, "rebus_rescue_summary.csv"), index=False)
    return lex_objs, evidence, unit_hit_rows, sum_rows, grid_rows


# ==============================================================================
# REDESIGN 1(b)-R: DENSE MULTILINGUAL EMBEDDING REBUS ALIGNMENT (/tmp/dict_emb/)
# ==============================================================================
def run_embedding_redesign(tiers_units):
    """Honestly different redesign when exact English/German keyword matching is sparse:
    Use precomputed multilingual Model2Vec embeddings (/tmp/dict_emb/emb_m2v.npy) to score
    continuous semantic cosine similarity between sound-alike glosses and class prototypes,
    base-rate centered per dictionary, on T2_CoreV2_33 and T3_CoreGram_53!"""
    emb_path = "/tmp/dict_emb/emb_m2v.npy"
    ph_path = "/tmp/dict_emb/phrases.json"
    if not (os.path.exists(emb_path) and os.path.exists(ph_path)):
        log("Skipping embedding redesign: /tmp/dict_emb not found")
        return []

    log("Running Redesign 1b-R: Dense Multilingual Embedding Rebus Alignment (/tmp/dict_emb/emb_m2v.npy)...")
    emb = np.load(emb_path).astype(np.float32)  # (N_phrases, 256), L2-normalized & mean-centered
    ph_data = json.load(open(ph_path, encoding="utf-8"))
    phrase_to_id = {p: i for i, p in enumerate(ph_data["phrases"])}

    # Build word-level fallback index from single-word phrases in phrases.json so EVERY gloss gets embedded cleanly
    word_vec = {}
    for p, idx in phrase_to_id.items():
        if ' ' not in p and p.isalpha():
            word_vec[p] = emb[idx]

    def embed_text(text):
        t_clean = str(text).lower().strip()
        if t_clean in phrase_to_id:
            return emb[phrase_to_id[t_clean]]
        ws = [w for w in re.findall(r"[a-zäöüß]+", t_clean)[:10] if w in word_vec]
        if not ws:
            return None
        v = np.mean([word_vec[w] for w in ws], axis=0)
        nrm = np.linalg.norm(v)
        return v / nrm if nrm > 1e-8 else None

    # Class prototype vectors (English wide keywords -> mean normalized vector)
    CI = {c: i for i, c in enumerate(CLS)}
    proto = np.zeros((len(CLS), emb.shape[1]), dtype=np.float32)
    for c in CLS:
        kws = list(kw_terms(c, 'wide', de=False))
        vs = [word_vec[w] for w in kws if w in word_vec]
        v = np.mean(vs, axis=0)
        proto[CI[c]] = v / (np.linalg.norm(v) + 1e-8)

    NOUNS = blind_nouns()
    NI = {n: i for i, n in enumerate(NOUNS)}
    OUTS = outside_list()
    rng = np.random.default_rng(20261199)

    redesign_rows = []
    for fam, dnames in COGNATE_FAMILIES.items():
        dname = dnames[0]
        L = CognateLex(dname, NOUNS, OUTS)
        # Embed every row's gloss in L
        row_vecs = np.zeros((L.n, emb.shape[1]), dtype=np.float32)
        valid_mask = np.zeros(L.n, dtype=bool)
        for i, g in enumerate(L.gl):
            # Take primary sense before ';'
            v = embed_text(g.split(';')[0])
            if v is not None:
                row_vecs[i] = v
                valid_mask[i] = True
        # Score matrix S_row[i, cls] = cosine(row_i, proto[cls]), centered by dictionary mean per class!
        S_row = row_vecs @ proto.T  # (L.n, 10)
        cls_mean = S_row[valid_mask].mean(axis=0) if valid_mask.any() else np.zeros(len(CLS))
        S_centered = np.where(valid_mask[:, None], S_row - cls_mean[None, :], 0.0)

        def mean_cos_mat(nouns_list, perm=None):
            inv = None
            if perm is not None:
                inv = np.empty_like(perm)
                inv[perm] = np.arange(len(perm))
            M_strict = np.zeros((len(nouns_list), len(CLS)), dtype=np.float32)
            M_med = np.zeros((len(nouns_list), len(CLS)), dtype=np.float32)
            has_s = np.zeros(len(nouns_list), dtype=bool)
            has_m = np.zeros(len(nouns_list), dtype=bool)
            qmask_e = np.zeros(L.n, dtype=bool)
            for a, nn in enumerate(nouns_list):
                pws = L.is_pic.get(nn, [])
                if not pws:
                    continue
                pf_arr = np.asarray(pws, dtype=np.int32)
                for dist_tag, M_dst, h_dst in (('strict', M_strict, has_s), ('medium', M_med, has_m)):
                    qmask_e.fill(False)
                    for pw in pws:
                        f = L.nf[pw] if perm is None else L.nf[perm[pw]]
                        c = L.near_form(f, dist_tag)
                        if len(c) == 0:
                            continue
                        if perm is not None:
                            c = inv[c]
                        qmask_e[c[L.eid_int[c] != L.eid_int[pw]]] = True
                    qmask_e[pf_arr] = False
                    qmask_e &= valid_mask
                    if qmask_e.any():
                        M_dst[a] = S_centered[qmask_e].mean(axis=0)
                        h_dst[a] = True
            return {'strict': (M_strict, has_s), 'medium': (M_med, has_m)}

        real_em = mean_cos_mat(NOUNS)
        gen_c = make_perm_generator(L.cid, L.n, rng)
        c3_em = [mean_cos_mat(NOUNS, perm=gen_c()) for _ in range(300)]

        for tname in ("T2_CoreV2_33", "T3_CoreGram_53"):
            _, units = tiers_units[tname]
            nU = len(units)
            ar = np.arange(nU)
            A = np.zeros((nU, len(NOUNS)), dtype=np.float32)
            for i, u in enumerate(units):
                for x in u['nouns'].split('|'):
                    A[i, NI[x]] = 1.0
            A_norm = A / np.maximum(1.0, A.sum(axis=1, keepdims=True))
            cls = np.array([CI[u['cls']] for u in units], dtype=np.int32)
            P1 = np.array([rng.permutation(cls) for _ in range(2000)], dtype=np.int32)

            for d_tag in ('strict', 'medium'):
                M_d, _ = real_em[d_tag]
                UM = A_norm @ M_d
                obs = float(UM[ar, cls].sum())
                n1 = UM[ar[None, :], P1].sum(axis=1)
                n3 = np.array([(A_norm @ c3_em[t][d_tag][0])[ar, cls].sum() for t in range(300)])
                p1 = (1.0 + np.sum(n1 >= obs - 1e-9)) / (1.0 + len(n1))
                p3 = (1.0 + np.sum(n3 >= obs - 1e-9)) / (1.0 + len(n3))
                z1 = 0.0 if n1.std() < 1e-9 else (obs - n1.mean()) / n1.std()
                z3 = 0.0 if n3.std() < 1e-9 else (obs - n3.mean()) / n3.std()
                redesign_rows.append({
                    'tier': tname, 'family': fam, 'dictionary': dname, 'dist': d_tag,
                    'excess_cosine_sum': round(obs, 4),
                    'c1_mean': round(float(n1.mean()), 4), 'c1_z': round(float(z1), 3), 'c1_P': round(float(p1), 4),
                    'c3_clust_mean': round(float(n3.mean()), 4), 'c3_clust_z': round(float(z3), 3), 'c3_clust_P': round(float(p3), 4),
                })
                log(f"  [Emb-Redesign] {tname} | {fam:10s} | {d_tag:6s}: excess_cos={obs:+.3f} | "
                    f"C1 z={z1:+.2f}(P={p1:.3f}) | C3_clust z={z3:+.2f}(P={p3:.3f})")

    pd.DataFrame(redesign_rows).to_csv(os.path.join(OUT_DIR, "rebus_embedding_redesign.csv"), index=False)
    return redesign_rows


# ==============================================================================
# STEP 1(c): MULTI-SIGN GRAPHIC COMPOUND & SWAP PHONETIC TEST + HELD-OUT NEW TEXTS
# ==============================================================================
NUMERAL_WORDS_EN = {
    1: {'one', 'single', 'first'},
    2: {'two', 'pair', 'double', 'both'},
    3: {'three', 'triple'},
    4: {'four'},
    5: {'five'},
    6: {'six'},
    7: {'seven'},
}
NUMERAL_WORDS_DE = {
    1: {'eins', 'ein', 'erste'}, 2: {'zwei', 'beide', 'paar'}, 3: {'drei'},
    4: {'vier'}, 5: {'fuenf', 'funf'}, 6: {'sechs'}, 7: {'sieben'},
}
# Attested native numeral stems where dictionaries omit bare cardinal glosses in etymological/cuneiform tables
NATIVE_NUM_STEMS = {
    "Dravidian": {1: ["oru", "onru"], 2: ["iru", "irantu"], 3: ["mu", "munru"], 4: ["nal", "nanku"], 5: ["ai", "aintu"], 6: ["aru"], 7: ["elu", "er̤u"]},
    "Munda": {1: ["mid", "miad", "moy"], 2: ["bar", "barea", "ubar"], 3: ["pe", "pea", "upe"], 4: ["upun", "pon", "ipon"], 5: ["mone", "moloi"], 6: ["turui", "tibru"], 7: ["eae", "gul", "eyae"]},
    "Indo-Aryan": {1: ["eka", "aika"], 2: ["dva", "dvi"], 3: ["tri", "trayas"], 4: ["catur"], 5: ["panca"], 6: ["sas", "sat"], 7: ["sapta"]},
    "Sumerian": {1: ["dis", "as", "ge"], 2: ["min"], 3: ["es"], 4: ["limmu"], 5: ["ia"], 6: ["as"], 7: ["imin"]},
    "Akkadian": {1: ["isten"], 2: ["sina"], 3: ["salas"], 4: ["erbe"], 5: ["hamis"], 6: ["sedis"], 7: ["sebe"]},
    "Elamite": {1: ["ki"], 2: ["mar", "nub"], 3: ["ziti"], 4: ["kut"], 5: ["pas"], 6: ["sak"], 7: ["sit"]},
    "Burushaski": {1: ["hik", "hin", "han"], 2: ["altan", "alto", "altac"], 3: ["iski", "usko"], 4: ["walto", "walti"], 5: ["cundo"], 6: ["misindo", "bisindo"], 7: ["thalo"]},
}

# Target crest / celestial / lineage / epithet keywords (unbiased across all 7 languages)
CREST_REBUS_EN = {
    'star', 'shine', 'bright', 'light', 'sky', 'heaven', 'sun', 'moon', 'day', 'night', 'dawn',
    'dark', 'black', 'white', 'red', 'great', 'high', 'chief', 'lord', 'king', 'clan', 'house',
    'lineage', 'family', 'god', 'divine', 'sparkle', 'glitter', 'flash'
}
CREST_REBUS_DE = {
    'stern', 'glanz', 'hell', 'licht', 'himmel', 'sonne', 'mond', 'tag', 'nacht',
    'dunkel', 'schwarz', 'weiss', 'rot', 'gross', 'hoch', 'herr', 'konig', 'sippe',
    'haus', 'familie', 'gott', 'funkeln'
}

def run_compound_and_swap_tests(lex_objs):
    log("Running Step 1(c): Multi-Sign Graphic Compound & Swap Phonetic Tests...")
    rng = np.random.default_rng(20261125)
    NOUNS = blind_nouns()
    NI = {n: i for i, n in enumerate(NOUNS)}
    comp_swap_rows = []

    # ------------------------------------------------------------------
    # 1c-0: Verify [modifier/numeral] + [plain fish 220] & marked-fish grammar on HELD-OUT Mahadevan NEW TEXTS (1,183 lines)!
    # ------------------------------------------------------------------
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        import frame2_common as f2
    Mu = f2.M[~f2.M.partnered]
    new_toks = [tuple(x) for x in Mu.tok if x]
    lipi_toks = [tuple(x) for x in f2.d.tok if x]

    NUM_SIGNS = {'001': 1, '031': 1, '002': 2, '012': 2, '032': 2, '003': 3, '013': 3, '033': 3,
                 '004': 4, '014': 4, '034': 4, '005': 5, '015': 5, '035': 5, '006': 6, '016': 6, '036': 6, '007': 7, '017': 7}
    MOD_FISH_SIGNS = set(NUM_SIGNS) | {'415'}  # the exact signs decomposing before 220 in one_for_two.csv

    def count_mod_fish(tok_list):
        obs_mf, rev_fm = 0, 0
        for t in tok_list:
            for a, b in zip(t, t[1:]):
                if a in MOD_FISH_SIGNS and b == '220':
                    obs_mf += 1
                elif a == '220' and b in MOD_FISH_SIGNS:
                    rev_fm += 1
        return obs_mf, rev_fm

    lipi_mf, lipi_fm = count_mod_fish(lipi_toks)
    new_mf, new_fm = count_mod_fish(new_toks)
    log(f"  [Held-out check] [Num/415 + 220 fish] vs reverse [220 + Num/415]: "
        f"Lipi {lipi_mf} vs {lipi_fm} | Held-out New Texts (1,183 lines): {new_mf} vs {new_fm}")

    # ------------------------------------------------------------------
    # 1c-A: Test the Fish-Mark Decompositions (99 of 830 frames; 66 [y + 220] frames)
    #       Modifiers attested on/before fish 220:
    #       Numerals {2, 3, 4, 6, 7} (from 032, 003, 004/034, 016/006, 017) + Picture marks {'roof', 'fork', 'cage', 'wing'}
    #       (from 235 caret-hat/roof, 415 fork/branch, 226 cage, 240 whiskers/wings).
    #       Test 1c-A1 (Double-Rebus Crest Bridge): Do BOTH modifier and base ('fish') have strict/medium
    #       homophones into CREST_REBUS meanings, compared to 2,000 random (modifier, other_picture_base) pairs?
    #       Test 1c-A2 (Attested Dictionary Compound Headword Match): How many [modifier + fish] pairs match an
    #       attested compound headword (prefix_stem + base_stem) in each family's full dictionary pool, vs 2,000
    #       random base nouns in the SAME dictionary?
    # ------------------------------------------------------------------
    FISH_MODIFIERS = [('num', 2), ('num', 3), ('num', 4), ('num', 6), ('num', 7),
                      ('pic', 'roof'), ('pic', 'fork'), ('pic', 'hill')]  # 8 attested modifiers of 220

    FAMILY_FULL_DICTS = collections.OrderedDict([
        ("Dravidian", ["pdrav_2branch", "dedr_tamil", "tamil_wiktionary", "telugu_wiktionary"]),
        ("Munda", ["pmunda_cognates", "santali_campbell", "mundari_bhadra", "kharia_druart"]),
        ("Indo-Aryan", ["oia_cognates", "oia_turner", "sanskrit_mw"]),
        ("Elamite", ["elamite_roots"]),
        ("Sumerian", ["sumerian_roots", "sumerian_halloran"]),
        ("Akkadian", ["akkadian_roots"]),
        ("Burushaski", ["burushaski_all"]),
    ])

    for fam, cog_dlist in COGNATE_FAMILIES.items():
        L = lex_objs[cog_dlist[0]]
        crest_kw = CREST_REBUS_DE if L.de else CREST_REBUS_EN

        # Identify rows in L carrying a crest/celestial/epithet keyword in first 5 words of any sense
        has_crest_kw = np.zeros(L.n, dtype=bool)
        for i, g in enumerate(L.gl):
            for ws in sense_words(g, 5):
                if any(w in crest_kw or (w.endswith('s') and w[:-1] in crest_kw) for w in ws):
                    has_crest_kw[i] = True
                    break

        def has_rebus_to_crest(forms_set, excl_eids, dist):
            for nf in forms_set:
                for q in L.near_form(nf, dist):
                    if L.eid[q] not in excl_eids and has_crest_kw[q]:
                        return True
            return False

        def get_mod_forms(mtype, mval):
            forms = set()
            eids = set()
            if mtype == 'num':
                for st in NATIVE_NUM_STEMS[fam].get(mval, []):
                    nf = typo_00_lexicons.norm(st)
                    forms.add(nf)
                    for i in L.by_nf.get(nf, []):
                        nws = NUMERAL_WORDS_DE[mval] if L.de else NUMERAL_WORDS_EN[mval]
                        if any(w in nws for ws in sense_words(L.gl[i], 4) for w in ws):
                            eids.add(L.eid[i])
            else:
                for pw in L.is_pic.get(mval, []):
                    forms.add(L.nf[pw])
                    eids.add(L.eid[pw])
            return forms, eids

        def get_noun_forms(nn):
            pws = L.is_pic.get(nn, [])
            return {L.nf[pw] for pw in pws}, {L.eid[pw] for pw in pws}

        # Candidate alternate bases = all blind nouns covered by L except 'fish'
        alt_bases = [nn for nn in NOUNS if nn != 'fish' and L.is_pic.get(nn)]
        all_mods_pool = [('num', k) for k in (1, 2, 3, 4, 5, 6, 7)] + [('pic', nn) for nn in alt_bases]

        for dist in ('strict', 'medium'):
            fish_forms, fish_eids = get_noun_forms('fish')
            fish_ok = has_rebus_to_crest(fish_forms, fish_eids, dist)
            obs_double = 0
            hit_details = []
            for mtype, mval in FISH_MODIFIERS:
                mf, me = get_mod_forms(mtype, mval)
                mod_ok = has_rebus_to_crest(mf, me, dist)
                if fish_ok and mod_ok:
                    obs_double += 1
                    hit_details.append(f"{mval}+fish")

            # Control: 2,000 draws of (8 random modifiers from pool + 1 random covered base noun != 'fish')
            null_double = []
            for _ in range(2000):
                b_rand = alt_bases[rng.integers(len(alt_bases))] if alt_bases else 'man'
                bf, be = get_noun_forms(b_rand)
                b_ok = has_rebus_to_crest(bf, be, dist)
                if not b_ok:
                    null_double.append(0)
                    continue
                m_idxs = rng.choice(len(all_mods_pool), size=len(FISH_MODIFIERS), replace=False)
                cnt_d = 0
                for mi in m_idxs:
                    mt, mv = all_mods_pool[mi]
                    mf, me = get_mod_forms(mt, mv)
                    if has_rebus_to_crest(mf, me, dist):
                        cnt_d += 1
                null_double.append(cnt_d)
            null_arr = np.array(null_double, dtype=float)
            p_dbl = (1.0 + np.sum(null_arr >= obs_double - 1e-9)) / (1.0 + len(null_arr))
            z_dbl = 0.0 if null_arr.std() < 1e-9 else (obs_double - null_arr.mean()) / null_arr.std()

            comp_swap_rows.append({
                'test': '1c_fish_double_rebus', 'family': fam, 'dist': dist,
                'tested': len(FISH_MODIFIERS), 'observed': obs_double,
                'ctrl_mean': round(float(null_arr.mean()), 3), 'ctrl_sd': round(float(null_arr.std()), 3),
                'z': round(float(z_dbl), 3), 'P': round(float(p_dbl), 4),
                'details': ' '.join(hit_details)
            })
            log(f"  [1c-FishRebus] {fam:11s} | {dist:6s}: {obs_double}/{len(FISH_MODIFIERS)} double-rebus bridges "
                f"vs {null_arr.mean():.2f} random (z={z_dbl:+.2f}, P={p_dbl:.4f}) {hit_details}")

        # 1c-A2: Attested Dictionary Compound Headword Test in Full Family Pool
        # Collect all normalized headwords of length >= 4 in family's full dictionaries
        all_hws = set()
        for dn in FAMILY_FULL_DICTS[fam]:
            if dn in lex_objs:
                all_hws.update(nf for nf in lex_objs[dn].nf if len(nf) >= 4)
            else:
                p_tsv = os.path.join(TMP_LEX, f"{dn}.tsv")
                if os.path.exists(p_tsv):
                    with open(p_tsv, encoding="utf-8") as f:
                        for line in f:
                            parts = line.rstrip("\n").split("\t")
                            if len(parts) >= 4 and len(parts[3]) >= 4:
                                all_hws.add(parts[3])

        # Index headwords by suffix for fast lookup!
        by_suffix = collections.defaultdict(list)
        for w in all_hws:
            for slen in (3, 4, 5):
                if len(w) > slen + 1:
                    by_suffix[w[-slen:]].append(w[:-slen])

        def attested_compound(mod_stems, base_stems):
            for bs in base_stems:
                if len(bs) < 3:
                    continue
                bs_key = bs[:5] if len(bs) > 5 else bs
                if len(bs_key) not in (3, 4, 5):
                    continue
                prefixes = by_suffix.get(bs_key, [])
                if not prefixes:
                    continue
                for ms in mod_stems:
                    ms_pre = ms[:2] if len(ms) >= 2 else ms
                    if len(ms_pre) < 2:
                        continue
                    for pfx in prefixes:
                        if len(pfx) <= len(ms) + 2 and pfx.startswith(ms_pre):
                            return f"{pfx}+{bs_key}"
            return None

        fish_stems = {nf for nf in get_noun_forms('fish')[0] if len(nf) >= 3}
        # Also include strict homophones of fish (e.g. min 'star' = same nf 'min')
        obs_att = 0
        att_hits = []
        for mtype, mval in FISH_MODIFIERS:
            mstems = get_mod_forms(mtype, mval)[0]
            m_hit = attested_compound(mstems, fish_stems)
            if m_hit:
                obs_att += 1
                att_hits.append(f"{mval}->{m_hit}")

        # Control: same 8 modifiers paired with each random covered 3+-letter base noun (2,000 draws)
        alt_3 = [nn for nn in alt_bases if any(len(nf) >= 3 for nf in get_noun_forms(nn)[0])]
        null_att = []
        for _ in range(2000):
            if not alt_3:
                null_att.append(0)
                continue
            b_rand = alt_3[rng.integers(len(alt_3))]
            bstems = {nf for nf in get_noun_forms(b_rand)[0] if len(nf) >= 3}
            c_a = 0
            for mtype, mval in FISH_MODIFIERS:
                mstems = get_mod_forms(mtype, mval)[0]
                if attested_compound(mstems, bstems):
                    c_a += 1
            null_att.append(c_a)
        na_arr = np.array(null_att, dtype=float)
        p_att = (1.0 + np.sum(na_arr >= obs_att - 1e-9)) / (1.0 + len(na_arr))
        z_att = 0.0 if na_arr.std() < 1e-9 else (obs_att - na_arr.mean()) / na_arr.std()

        comp_swap_rows.append({
            'test': '1c_attested_lex_compounds', 'family': fam, 'dist': 'exact_stem',
            'tested': len(FISH_MODIFIERS), 'observed': obs_att,
            'ctrl_mean': round(float(na_arr.mean()), 3), 'ctrl_sd': round(float(na_arr.std()), 3),
            'z': round(float(z_att), 3), 'P': round(float(p_att), 4),
            'details': ' '.join(att_hits)
        })
        log(f"  [1c-LexCompound] {fam:11s}: {obs_att}/{len(FISH_MODIFIERS)} attested compounds "
            f"vs {na_arr.mean():.2f} random base (z={z_att:+.2f}, P={p_att:.4f}) {att_hits}")

    # ------------------------------------------------------------------
    # 1c-B: Swap Pairs Phonetic Test (All 108 pairs vs Filtered Non-Personal Allographic Swaps)
    # ------------------------------------------------------------------
    sp2 = [r for r in csv.DictReader(open(os.path.join(ROOT, "work_data", "lang_m2", "swap_pairs.csv"), encoding="utf-8"))
           if r['variant'] == 'B_3of3+2of3' and r['tested'] == 'True']
    cv2 = {r['sign']: r['v2_base'] for r in csv.DictReader(open(os.path.join(ROOT, "work_data", "frame", "classes_v2.csv"), encoding="utf-8"))}
    SG = {r['sign']: r['nouns'].split(';') for r in csv.DictReader(open(os.path.join(ROOT, "work_data", "lang_m2", "signs.csv"), encoding="utf-8"))
          if r['level'] in ('3of3', '2of3') and r['nouns']}

    all_swap_pairs = [(r['a'], r['b']) for r in sp2 if r['a'] in SG and r['b'] in SG]
    # Filtered allographic candidates: neither sign is open-class PERSONAL, and NOT known distinct-rank closers (740 vs 151/520) or distinct titles (090 vs 400)
    KNOWN_PARADIGMATIC = {('151', '740'), ('520', '740'), ('090', '400'), ('156', '740'), ('740', '820')}
    allo_swap_pairs = [
        (a, b) for (a, b) in all_swap_pairs
        if cv2.get(a) != 'PERSONAL' and cv2.get(b) != 'PERSONAL' and tuple(sorted((a, b))) not in KNOWN_PARADIGMATIC
    ]
    log(f"  [1c-Swaps] All swap pairs: {len(all_swap_pairs)} | Filtered non-PERSONAL non-distinct-rank swap pairs: {len(allo_swap_pairs)} {allo_swap_pairs}")

    pool_signs = sorted(SG.keys())
    for set_name, pair_list in (("1c_swaps_all108", all_swap_pairs), ("1c_swaps_closed_allo", allo_swap_pairs)):
        if not pair_list:
            continue
        rand_draws = []
        for _ in range(2000):
            out = []
            while len(out) < len(pair_list):
                a, b = rng.choice(pool_signs, 2, replace=False)
                if not (set(SG[a]) & set(SG[b])):
                    out.append((a, b))
            rand_draws.append(out)

        for fam, cog_dlist in COGNATE_FAMILIES.items():
            L = lex_objs[cog_dlist[0]]
            for dist in ('strict', 'medium'):
                # Build noun-noun sound-alike boolean matrix
                M_nn = np.zeros((len(NOUNS), len(NOUNS)), dtype=bool)
                for na in NOUNS:
                    for pw in L.is_pic.get(na, []):
                        for q in L.near_form(L.nf[pw], dist):
                            if L.eid[q] == L.eid[pw]:
                                continue
                            for nb in NOUNS:
                                if nb != na and q in L.pic_flag[nb]:
                                    M_nn[NI[na], NI[nb]] = M_nn[NI[nb], NI[na]] = True

                def pair_hit(a, b):
                    return any(M_nn[NI[x], NI[y]] for x in SG[a] for y in SG[b])

                obs_s = sum(pair_hit(a, b) for a, b in pair_list)
                hits_s = [f"{a}~{b}" for a, b in pair_list if pair_hit(a, b)]
                r_arr = np.array([sum(pair_hit(a, b) for a, b in ps) for ps in rand_draws], dtype=float)
                p_r = (1.0 + np.sum(r_arr >= obs_s - 1e-9)) / (1.0 + len(r_arr))
                z_r = 0.0 if r_arr.std() < 1e-9 else (obs_s - r_arr.mean()) / r_arr.std()

                comp_swap_rows.append({
                    'test': set_name, 'family': fam, 'dist': dist,
                    'tested': len(pair_list), 'observed': obs_s,
                    'ctrl_mean': round(float(r_arr.mean()), 3), 'ctrl_sd': round(float(r_arr.std()), 3),
                    'z': round(float(z_r), 3), 'P': round(float(p_r), 4),
                    'details': ' '.join(hits_s[:15])
                })
                if dist == 'strict' or set_name == '1c_swaps_closed_allo':
                    log(f"  [{set_name}] {fam:11s} | {dist:6s}: {obs_s}/{len(pair_list)} vs {r_arr.mean():.2f} (z={z_r:+.2f}, P={p_r:.4f})")

    pd.DataFrame(comp_swap_rows).to_csv(os.path.join(OUT_DIR, "compound_swap_results.csv"), index=False)
    return comp_swap_rows


# ==============================================================================
# EXPORT RESCUED CANDIDATES WITH MATCHED SAME-CLASS DECOYS
# ==============================================================================
def export_rescued_candidates(evidence, unit_hit_rows):
    """Export core-slot rebus candidates (strict & medium distance on T3_CoreGram_53) across
    candidate families, each paired 1-to-1 with a matched same-class DECOY from another unit,
    plus C3_clust chance hit rate so real vs decoy excess is explicit."""
    rng = np.random.default_rng(20261130)
    uh_df = pd.DataFrame(unit_hit_rows)
    if uh_df.empty:
        return

    # Index strict/medium evidence from cognate lexicons
    cog_dicts = {d[0]: fam for fam, d in COGNATE_FAMILIES.items()}
    ev_by_key = collections.defaultdict(list)
    for e in evidence:
        if e['dict'] in cog_dicts:
            fam = cog_dicts[e['dict']]
            ev_by_key[(fam, e['dist'], e['breadth'], e['noun'], e['cls'])].append(e)

    cand_out = []
    sub = uh_df[(uh_df['tier'] == 'T3_CoreGram_53') & (uh_df['real_hit'] == 1) & (uh_df['breadth'] == 'wide')]
    # Group by (family, dist) to pair each real hit with a matched same-class decoy
    for (fam, dist), grp in sub.groupby(['family', 'dist']):
        unit_evs = []
        for r in grp.itertuples():
            matches = []
            for nn in r.nouns.split('|'):
                matches.extend(ev_by_key.get((fam, dist, 'wide', nn, r.cls), []))
            if matches:
                # Prefer strict cross-cluster homophones (same_deriv_cluster == 0) first
                matches.sort(key=lambda x: (x['same_deriv_cluster'], len(x['soundalike'])))
                unit_evs.append((r, matches[0]))
        for idx_u, (r, best_ev) in enumerate(unit_evs):
            # Pick a matched decoy from same class if available, else another core class in same family
            same_cls = [x[1] for j, x in enumerate(unit_evs) if j != idx_u and x[0].cls == r.cls]
            any_oth = [x[1] for j, x in enumerate(unit_evs) if j != idx_u]
            pool = same_cls or any_oth
            decoy_ev = pool[rng.integers(len(pool))] if pool else None

            cand_out.append({
                'kind': 'REAL',
                'family': fam,
                'dictionary': best_ev['dict'],
                'dist': dist,
                'signs': r.signs,
                'nouns': r.nouns,
                'cls': r.cls,
                'cls_name': r.cls_name,
                'c3_clust_hit_rate': r.c3_clust_hit_rate,
                'excess_over_c3': round(1.0 - r.c3_clust_hit_rate, 4),
                'picture_word': best_ev['picture_word'],
                'picture_eid': best_ev['picture_eid'],
                'picture_gloss': best_ev['picture_gloss'],
                'rebus_word': best_ev['soundalike'],
                'rebus_eid': best_ev['soundalike_eid'],
                'rebus_gloss': best_ev['soundalike_gloss'],
                'same_deriv_cluster': best_ev['same_deriv_cluster'],
            })
            if decoy_ev is not None:
                cand_out.append({
                    'kind': 'DECOY_SAME_CLASS' if same_cls else 'DECOY_CORE',
                    'family': fam,
                    'dictionary': decoy_ev['dict'],
                    'dist': dist,
                    'signs': r.signs,
                    'nouns': r.nouns,
                    'cls': r.cls,
                    'cls_name': r.cls_name,
                    'c3_clust_hit_rate': r.c3_clust_hit_rate,
                    'excess_over_c3': round(0.0 - r.c3_clust_hit_rate, 4),
                    'picture_word': decoy_ev['picture_word'],
                    'picture_eid': decoy_ev['picture_eid'],
                    'picture_gloss': decoy_ev['picture_gloss'],
                    'rebus_word': decoy_ev['soundalike'],
                    'rebus_eid': decoy_ev['soundalike_eid'],
                    'rebus_gloss': decoy_ev['soundalike_gloss'],
                    'same_deriv_cluster': decoy_ev['same_deriv_cluster'],
                })

    out_path = os.path.join(OUT_DIR, "rebus_rescued_candidates.csv")
    pd.DataFrame(cand_out).to_csv(out_path, index=False)
    log(f"Exported {len(cand_out)} real+decoy candidate rows to {out_path}")


def main():
    tiers_units = build_unit_tiers()
    lex_objs, evidence, unit_hit_rows, sum_rows, grid_rows = run_rebus_rescues(tiers_units)
    run_embedding_redesign(tiers_units)
    run_compound_and_swap_tests(lex_objs)
    export_rescued_candidates(evidence, unit_hit_rows)
    log("All Step 1 Rebus Rescues completed!")

if __name__ == "__main__":
    main()
