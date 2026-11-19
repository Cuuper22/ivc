#!/usr/bin/env python3
"""
Key #4D (Lever 4): Allograph Collapser
======================================
Multi-signal palaeographic & distributional engine that separates:
  1. Tier 1 — Verified Pure Calligraphic Allographs (free variation across slots & media)
  2. Tier 2 — Verified Workshop / Regional / Medium Calligraphic Allographs
              (same underlying sign & grammar slot, zero/depleted co-occurrence, high
              neighbor substitutability, differentiated by carving medium/site/period)
  3. FALSE MERGERS caught in Mahadevan (1977), Parpola (Mayig), and crosswalk tables
  4. Distinct Graphic Compounds / Ligatures (extra roof/stroke/enclosure/mark)

Validates strictly out-of-sample with ZERO overfitting via:
  - 5-fold cross-validation on Lipi (4,476 deduplicated copy events)
  - Out-of-domain generalization on held-out unseen Mahadevan `new texts` (990 events)
  - Both exact uncollapsed Brown-Class Generative Bits-per-Sign (exact prior-invariant
    normalization), Context-Only Pooling Bits-per-Sign, and Collapsed-Alphabet Entropy
  - Benchmarked against 2,000 frequency-matched random sign-merge partitions AND a
    False-Merger Negative Control.

Computes exact sign-inventory compression (638 -> N_true) and exact token & 100%-face
coverage jump across all 4,227 intact accessible faces (3,600 Lipi + 627 unseen M77).

Strictly rerunnable, deterministic (seed=20261119), stdlib + numpy only.
Outputs written to: work_data/key4d/
"""

import csv
import json
import math
import os
import re
import time
from collections import Counter, defaultdict
import numpy as np

ROOT = "/home/antigravity/Cuuper22/ivc"
OUT_DIR = os.path.join(ROOT, "work_data", "key4d")
os.makedirs(OUT_DIR, exist_ok=True)

SEED = 20261119
N_RAND_MERGES = 2000

# ==============================================================================
# 0. SOUND-LOCKED INVENTORY (Key #2A 11 + Key #3A 8 Promoted = 19, + 3 Loans + Basic Nums)
# ==============================================================================
LOCKED11 = {
    "220": ("*mīṉ", "star / fish (K2A)"),
    "820": ("*kāl", "quarter / wheel (K2A)"),
    "320": ("*paṭi", "ration / step (K2A)"),
    "090": ("*āḷ", "manager / man (K2A)"),
    "154": ("*kā", "guard / pole (K2A)"),
    "740": ("*kuṭi", "house / pot (K2A)"),
    "400": ("*cikka", "junior / comb (K2A)"),
    "705": ("*kalam", "ship / kalam (K2A)"),
    "520": ("*vēḷ", "chief / spear (K2A)"),
    "850": ("*kaṉ", "copper / eye (K2A)"),
    "390": ("*tai", "weave / tree (K2A)"),
}

PROMOTED8 = {
    "717": ("*aṭi", "foot / servant (K3A)"),
    "061": ("*kāl", "leg / quarter (K3A)"),
    "235": ("*oḷi-mīṉ", "capped-fish / star-crest (K3A)"),
    "500": ("*pāy", "sail (K3A)"),
    "100": ("*talai", "head / lineage-chief (K3A)"),
    "176": ("*iru~*iṟu", "sit / tax-issuer (K3A)"),
    "900": ("*tiṅkaḷ", "moon / month (K3A)"),
    "923": ("*maruppu", "horn / elephant-tusk (K3A)"),
}

LOCKED19 = {**LOCKED11, **PROMOTED8}

LOAN_ANCHORS = {
    "854": ("*eḷ", "sesame [loan]"),
    "838": ("*eḷ", "sesame-seed [loan]"),
    "790": ("*vaḷai", "bangle [loan]"),
    "215": ("*arici", "rice [loan]"),
}

BASIC_NUMS = {
    "001": ("*oru", "1 short [num]"),
    "031": ("*oru", "1 tall [num]"),
    "002": ("*iru", "2 short / header [num]"),
    "032": ("*iru", "2 tall [num]"),
    "003": ("*mū", "3 short [num]"),
    "033": ("*mū", "3 tall [num]"),
    "004": ("*nāl", "4 short [num]"),
    "034": ("*nāl", "4 tall [num]"),
    "015": ("*ai", "5 stacked [num]"),
    "055": ("*paṉṉiru", "12 / dozen [num]"),
}

ALL_NUM_SIGNS = set(BASIC_NUMS.keys()) | {
    "005", "006", "007", "016", "017", "027", "028", "029",
    "035", "036", "037", "056", "M94", "X94",
}
MEASURE_SIGNS = {
    "320", "321", "323", "061", "062", "063", "700", "701", "703",
    "711", "705", "706", "575", "171", "480", "645", "590",
}

ALL_SOUND_TARGETS = {**LOCKED19, **LOAN_ANCHORS, **BASIC_NUMS}

# Known classic split-test controls (explicitly evaluated even across different P/M codes)
SPLIT_BENCHMARK_PAIRS = [
    ("002", "032"), ("001", "031"), ("003", "033"), ("004", "034"),
    ("740", "741"), ("740", "742"), ("741", "742"), ("740", "745"),
    ("220", "235"), ("220", "233"), ("220", "231"), ("220", "240"),
    ("090", "093"), ("090", "097"), ("090", "100"),
    ("151", "154"), ("154", "161"), ("154", "159"),
    ("900", "920"), ("850", "790"), ("711", "717"), ("320", "321"),
    ("175", "176"), ("390", "408"), ("525", "527"),
]


# ==============================================================================
# 1. PURE-MATH STATISTICAL HELPERS (EXACT CHI2 GAMMAINCC & FISHER EXACT)
# ==============================================================================
def _gser(a, x):
    """Lower incomplete gamma P(a, x) via series."""
    gln = math.lgamma(a)
    if x <= 0.0:
        return 0.0
    ap = a
    summ = 1.0 / a
    delt = summ
    for _ in range(300):
        ap += 1.0
        delt *= x / ap
        summ += delt
        if abs(delt) < abs(summ) * 1e-13:
            break
    return summ * math.exp(-x + a * math.log(x) - gln)


def _gcf(a, x):
    """Upper incomplete gamma Q(a, x) via Lentz continued fraction."""
    gln = math.lgamma(a)
    b = x + 1.0 - a
    c = 1.0 / 1e-30
    d = 1.0 / b
    h = d
    for i in range(1, 300):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < 1e-30:
            d = 1e-30
        c = b + an / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delt = d * c
        h *= delt
        if abs(delt - 1.0) < 1e-13:
            break
    return math.exp(-x + a * math.log(x) - gln) * h


def chi2_sf(stat, df):
    """Exact survival function P(Chi2_df >= stat)."""
    if df <= 0 or stat <= 0.0:
        return 1.0
    a = 0.5 * df
    x = 0.5 * stat
    if x < a + 1.0:
        return max(0.0, min(1.0, 1.0 - _gser(a, x)))
    return max(0.0, min(1.0, _gcf(a, x)))


def log_comb(n, k):
    if k < 0 or k > n:
        return -1e300
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def hypergeom_le(k, M, n, N):
    """P(X <= k) for X ~ Hypergeom(pop=M, successes=n, draws=N)."""
    lo = max(0, N - (M - n))
    hi = min(k, n, N)
    if hi < lo:
        return 0.0
    denom = log_comb(M, N)
    probs = [math.exp(log_comb(n, j) + log_comb(M - n, N - j) - denom) for j in range(lo, hi + 1)]
    return min(1.0, sum(probs))


def hypergeom_ge(k, M, n, N):
    """P(X >= k) for X ~ Hypergeom(pop=M, successes=n, draws=N)."""
    lo = max(k, N - (M - n))
    hi = min(n, N)
    if lo > hi:
        return 0.0
    denom = log_comb(M, N)
    probs = [math.exp(log_comb(n, j) + log_comb(M - n, N - j) - denom) for j in range(lo, hi + 1)]
    return min(1.0, sum(probs))


def contingency_chi2(c1, c2, min_col_sum=1):
    """Pearson chi-square & exact p-value for two Counter dicts (merging tiny tail into 'OTHER' if needed)."""
    keys = [k for k in (set(c1.keys()) | set(c2.keys())) if c1.get(k, 0) + c2.get(k, 0) >= min_col_sum]
    if len(keys) < 2:
        return 0.0, 0, 1.0
    n1 = sum(c1.get(k, 0) for k in keys)
    n2 = sum(c2.get(k, 0) for k in keys)
    if n1 == 0 or n2 == 0:
        return 0.0, 0, 1.0
    N = n1 + n2
    stat = 0.0
    for k in keys:
        o1, o2 = c1.get(k, 0), c2.get(k, 0)
        tot = o1 + o2
        e1 = tot * n1 / N
        e2 = tot * n2 / N
        if e1 > 0:
            stat += (o1 - e1) ** 2 / e1
        if e2 > 0:
            stat += (o2 - e2) ** 2 / e2
    df = len(keys) - 1
    return stat, df, chi2_sf(stat, df)


def contingency_chi2_collapsed(c1, c2, top_k=6):
    """Collapse sparse categorical distributions (site/kind) to top_k shared categories + OTHER for stable df."""
    tot = Counter()
    for k, v in c1.items():
        tot[k] += v
    for k, v in c2.items():
        tot[k] += v
    if len(tot) <= top_k:
        return contingency_chi2(c1, c2)
    keep = {k for k, _ in tot.most_common(top_k - 1)}
    nc1, nc2 = Counter(), Counter()
    for k, v in c1.items():
        nc1[k if k in keep else "__OTHER__"] += v
    for k, v in c2.items():
        nc2[k if k in keep else "__OTHER__"] += v
    return contingency_chi2(nc1, nc2)


def cosine_counters(c1, c2):
    if not c1 or not c2:
        return 0.0
    keys = set(c1.keys()) & set(c2.keys())
    if not keys:
        return 0.0
    num = sum(c1[k] * c2[k] for k in keys)
    d1 = math.sqrt(sum(v * v for v in c1.values()))
    d2 = math.sqrt(sum(v * v for v in c2.values()))
    return num / (d1 * d2) if d1 > 0 and d2 > 0 else 0.0


# ==============================================================================
# 2. LOAD ALL REPOSITORY DATA TABLES
# ==============================================================================
def load_all_data():
    # 2a. Intact accessible corpus (3,600 Lipi + 627 unseen M77 = 4,227 faces, 638 Lipi types)
    with open(os.path.join(ROOT, "work_data/reader_v3/corpus_soundfree_readings.csv"), encoding="utf-8") as f:
        r3_rows = list(csv.DictReader(f))
    lipi_intact_faces = [r for r in r3_rows if r["catalogue"] == "Lipi" and r["intact"] == "True"]
    new_intact_faces = [
        r for r in r3_rows
        if r["catalogue"] != "Lipi" and r["partnered"] == "False" and r["intact"] == "True"
    ]
    intact_lipi_cnt = Counter()
    intact_new_cnt = Counter()
    for r in lipi_intact_faces:
        for t in r["signs"].split("-"):
            if t and t != "000" and not t.startswith("X"):
                intact_lipi_cnt[t] += 1
    for r in new_intact_faces:
        for t in r["signs"].split("-"):
            if t and t != "000" and not t.startswith("X"):
                intact_new_cnt[t] += 1
    intact_signs = sorted(set(intact_lipi_cnt.keys()) | set(intact_new_cnt.keys()))

    # 2b. Soundfree lexicon (FRAME v3 anchored signs & classes)
    v3_lex = {}
    with open(os.path.join(ROOT, "work_data/reader_v3/soundfree_lexicon.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            v3_lex[r["sign"].strip()] = r

    # 2c. Deduplicated copy events (Lipi & Unseen New)
    with open(os.path.join(ROOT, "work_data/sem/events_lipi.json"), encoding="utf-8") as f:
        ev_lipi = json.load(f)
    with open(os.path.join(ROOT, "work_data/sem/events_new.json"), encoding="utf-8") as f:
        ev_new = json.load(f)

    # 2d. Sign shapes & Parpola P-codes
    shapes = {}
    parpola_p = {}
    with open(os.path.join(ROOT, "work_data/sign_shapes.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = r["lipi_wells_number"].strip()
            p = r["mayig_code"].strip()
            d = r["shape_description"].strip()
            shapes[s] = d
            if p:
                parpola_p[s] = p

    # 2e. Sign meta
    sign_meta = {}
    with open(os.path.join(ROOT, "work_data/sem/sign_meta.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = r["sign"].strip()
            sign_meta[s] = r
            if s not in parpola_p and r["mayig_p"].strip():
                parpola_p[s] = r["mayig_p"].strip()

    # 2f. Lipi -> Mahadevan M crosswalk (rank 1, share >= 0.35; also record all top hits)
    mah_m = {}
    mah_m_detail = defaultdict(list)
    with open(os.path.join(ROOT, "work_data/lipi_mahadevan_crosswalk.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = r["lipi"].strip()
            m = r["mahadevan"].strip()
            rk = int(r["rank_for_lipi_sign"])
            sh = float(r["share_of_lipi_sign"])
            pos = int(r["text_positions"])
            mah_m_detail[s].append((rk, m, sh, pos))
            if rk == 1 and sh >= 0.35:
                mah_m[s] = m
    for s, r in sign_meta.items():
        if s not in mah_m and r["mahadevan_m"].strip():
            # Only add from sign_meta if not explicitly low-share multi-split (<0.35)
            if s not in mah_m_detail:
                mah_m[s] = r["mahadevan_m"].strip()

    # 2g. research/data/sign_crosswalk/crosswalk_edges.csv
    ce_lipi_to_p = defaultdict(list)
    ce_p_to_m = defaultdict(set)
    with open(os.path.join(ROOT, "research/data/sign_crosswalk/crosswalk_edges.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fsys, fid = r["from_sign_uid"].split(":", 1)
            tsys, tid = r["to_sign_uid"].split(":", 1)
            if fsys == "lipi_numeric" and tsys == "mayig_p":
                sh = float(r["top_share"] or 0.0)
                sup = int(r["support_count"] or 0)
                if sh >= 0.5 and sup >= 2:
                    ce_lipi_to_p[fid].append((tid, r["mapping_state"], sh, sup))
            elif fsys == "mayig_p" and tsys == "mayig_mahadevan_m":
                ce_p_to_m[fid].add(tid)

    # 2h. Graphic compound / mark families & eye judgements
    mark_pairs = set()
    mark_base_of = {}
    with open(os.path.join(ROOT, "work_data/signlist/mark_families.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            c, b = r["compound"].strip(), r["base"].strip()
            mt = r["mark_type"].strip()
            mark_base_of[c] = (b, mt, r["mark"].strip())
            mark_pairs.add(tuple(sorted((c, b))))

    eye_judge = {}
    with open(os.path.join(ROOT, "work_data/signlist/eye/eye_judgements.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pair = tuple(sorted((r["a"].strip(), r["b"].strip())))
            eye_judge[pair] = (r["eye"].strip(), r["note"].strip())

    return {
        "lipi_intact_faces": lipi_intact_faces,
        "new_intact_faces": new_intact_faces,
        "intact_lipi_cnt": intact_lipi_cnt,
        "intact_new_cnt": intact_new_cnt,
        "intact_signs": intact_signs,
        "v3_lex": v3_lex,
        "ev_lipi": ev_lipi,
        "ev_new": ev_new,
        "shapes": shapes,
        "parpola_p": parpola_p,
        "sign_meta": sign_meta,
        "mah_m": mah_m,
        "mah_m_detail": mah_m_detail,
        "ce_lipi_to_p": ce_lipi_to_p,
        "ce_p_to_m": ce_p_to_m,
        "mark_pairs": mark_pairs,
        "mark_base_of": mark_base_of,
        "eye_judge": eye_judge,
    }


# ==============================================================================
# 3. SIGNAL 2: VISUAL SHAPE SIMILARITY & GRAPHIC COMPOUND / LIGATURE FILTER
# ==============================================================================
STOPWORDS = {
    "a", "an", "the", "of", "with", "at", "in", "on", "to", "from", "and", "or",
    "by", "for", "is", "as", "be", "may", "possibly", "perhaps", "near", "each",
    "coming", "off", "out", "into", "going", "very", "then", "also", "see",
}

MODIFIER_PATTERNS = [
    ("hat", r"\b(hat|caret|capped|roof|table)\b"),
    ("brackets", r"\b(bracketed|parenthes|paren|caged|surrounded|enclosed)\b"),
    ("hatching", r"\b(hatch|hatched|hatching|cross[- ]?hatch|striped)\b"),
    ("inside_mark", r"\b(inside|in the body|between legs|through body|in mouth|in center)\b"),
    ("appendage", r"\b(tooth|whiskers|flag|flags|pitchfork|tree|sunburst|dot|dots|circle|diamond|triangle|cross|extra|legs)\b"),
    ("tall_vs_short", r"\b(full-height|tall|half-height|short)\b"),
    ("stroke_count", r"\b(no|single|one|two|three|four|five|six|seven|eight|nine|ten)\b"),
]


def shape_tokens(desc):
    if not desc:
        return set()
    return set(re.findall(r"[a-z]+", desc.lower())) - STOPWORDS


def shape_jaccard(d1, d2):
    if not d1 or not d2:
        return -1.0
    if d1 == d2:
        return 1.0
    w1, w2 = shape_tokens(d1), shape_tokens(d2)
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / len(w1 | w2)


def detect_graphic_compound_veto(a, b, data):
    """
    Strictly separate true calligraphic allographs from distinct graphic compounds/ligatures.
    Returns (is_veto: bool, reason: str).
    """
    pair = tuple(sorted((a, b)))
    eye = data["eye_judge"].get(pair)
    if eye and eye[0] in ("different", "base+mark"):
        return True, f"eye_veto:{eye[0]}({eye[1][:40]})"

    pa = data["parpola_p"].get(a, "")
    pb = data["parpola_p"].get(b, "")
    da = data["shapes"].get(a, "")
    db = data["shapes"].get(b, "")

    # 1. Explicit compound -> base mark addition from mark_families.csv
    if pair in data["mark_pairs"] and (pa != pb or not pa):
        # Allow stacked vs inline same numeral count (e.g. 005/015, 004/014, 006/016, 007/017)
        if not (pa and pa == pb):
            return True, "mark_family_base_plus_mark"

    # 2. If both have Parpola codes and they are DIFFERENT, check graphic modifier asymmetry
    if pa and pb and pa != pb and da and db:
        la, lb = da.lower(), db.lower()
        # Allow pure left/right mirror (e.g. M050 deer facing right vs left)
        norm_lr_a = re.sub(r"\b(left|right)\b", "DIR", la)
        norm_lr_b = re.sub(r"\b(left|right)\b", "DIR", lb)
        if norm_lr_a == norm_lr_b:
            return False, "mirror_orientation_only"
        # Allow pure stacked vs inline numeral strokes with SAME count (e.g. 003/013)
        if ("vertical stroke" in la and "vertical stroke" in lb and
                not any(k in la or k in lb for k in ["hat", "caret", "bracket", "paren", "tree", "box", "caged"])):
            # Check height class: short/half-height vs tall/full-height is a VETO!
            a_tall = ("full-height" in la or "tall" in la)
            b_tall = ("full-height" in lb or "tall" in lb)
            if a_tall != b_tall:
                return True, "numeral_tall_vs_short"
            # Check count equality (e.g., 003 "three" vs 013 "two ... over one" -> both 3)
            def extract_stroke_num(txt):
                word_to_n = {"one": 1, "single": 1, "two": 2, "three": 3, "four": 4,
                             "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
                if "over" in txt or "above" in txt:
                    parts = re.split(r"\b(?:over|above)\b", txt)
                    s_tot = 0
                    for pt in parts:
                        ms = re.findall(r"\b(one|single|two|three|four|five|six|seven|eight|nine|ten)\b", pt)
                        if ms:
                            s_tot += word_to_n[ms[0]]
                    if "the same" in txt:
                        # e.g. four above the same above the same = 12
                        ms = re.findall(r"\b(one|single|two|three|four|five|six|seven|eight|nine|ten)\b", parts[0])
                        if ms:
                            return word_to_n[ms[0]] * len(parts)
                    return s_tot if s_tot > 0 else None
                ms = re.findall(r"\b(one|single|two|three|four|five|six|seven|eight|nine|ten)\b", txt)
                return word_to_n[ms[0]] if ms else None

            na, nb = extract_stroke_num(la), extract_stroke_num(lb)
            if na is not None and nb is not None:
                if na != nb:
                    return True, f"numeral_count_diff:{na}_vs_{nb}"
                return False, "same_numeral_count_layout"

        # Check explicit modifier token asymmetry across different Parpola codes
        for mod_name, pat in MODIFIER_PATTERNS:
            ma = set(re.findall(pat, la))
            mb = set(re.findall(pat, lb))
            if ma != mb:
                # Special allowance: identical Mahadevan M AND eye says alike/one glyph
                if eye and eye[0] in ("alike", "one glyph"):
                    return False, f"eye_confirmed_{eye[0]}"
                return True, f"modifier_diff:{mod_name}({sorted(ma)} vs {sorted(mb)})"

        # Different P-codes and low shape Jaccard (< 0.45): completely different pictographs
        jac = shape_jaccard(da, db)
        if jac < 0.45:
            if eye and eye[0] in ("alike", "one glyph"):
                return False, f"eye_confirmed_{eye[0]}"
            return True, f"distinct_pictographs(P:{pa}!={pb},jac={jac:.2f})"

    # 3. Same Parpola P-code: check explicit numeral count difference (e.g. P141 025..029)
    # P141 has same description for 025..029 ("Three rows of off-center or slanted small vertical strokes") -> NOT vetoed unless distribution splits them
    return False, ""


# ==============================================================================
# 4. SIGNAL 3: DISTRIBUTIONAL PROFILES FROM DEDUPLICATED LIPI COPY EVENTS
# ==============================================================================
def build_distributional_profiles(ev_lipi):
    N_ev = len(ev_lipi)
    ev_presence = defaultdict(set)
    left_nb = defaultdict(Counter)
    right_nb = defaultdict(Counter)
    left_nb_nobnd = defaultdict(Counter)
    right_nb_nobnd = defaultdict(Counter)
    frames = defaultdict(Counter)
    pos_bins = defaultdict(lambda: Counter())  # 0=init, 1=mid, 2=final
    pos_vals = defaultdict(list)
    solo_cnt = Counter()
    kind_cnt = defaultdict(Counter)
    site_cnt = defaultdict(Counter)
    time_cnt = defaultdict(Counter)
    slot_cnt = defaultdict(Counter)
    tok_cnt = Counter()

    for idx, ev in enumerate(ev_lipi):
        site = ev.get("site", "") or "Unknown"
        kind = ev.get("kind", "") or "other"
        tbin = ev.get("time_bin", "") or ""
        fslots = ev.get("face_slots", [])
        for fi, face in enumerate(ev["faces"]):
            slots = fslots[fi] if fi < len(fslots) else []
            n = len(face)
            has_dmg = ("000" in face)
            for i, s in enumerate(face):
                if not s or s == "000" or s.startswith("X"):
                    continue
                tok_cnt[s] += 1
                ev_presence[s].add(idx)
                kind_cnt[s][kind] += 1
                site_cnt[s][site] += 1
                if tbin:
                    time_cnt[s][tbin] += 1
                if i < len(slots):
                    slot_cnt[s][slots[i]] += 1
                L = "^" if i == 0 else face[i - 1]
                R = "$" if i == n - 1 else face[i + 1]
                if L != "000":
                    left_nb[s][L] += 1
                    if L != "^":
                        left_nb_nobnd[s][L] += 1
                if R != "000":
                    right_nb[s][R] += 1
                    if R != "$":
                        right_nb_nobnd[s][R] += 1
                if L != "000" and R != "000":
                    frames[s][(L, R)] += 1
                if not has_dmg:
                    if n == 1:
                        solo_cnt[s] += 1
                    else:
                        pos_vals[s].append(i / (n - 1))
                        if i == 0:
                            pos_bins[s]["init"] += 1
                        elif i == n - 1:
                            pos_bins[s]["final"] += 1
                        else:
                            pos_bins[s]["mid"] += 1

    return {
        "N_ev": N_ev,
        "ev_presence": ev_presence,
        "left_nb": left_nb,
        "right_nb": right_nb,
        "left_nb_nobnd": left_nb_nobnd,
        "right_nb_nobnd": right_nb_nobnd,
        "frames": frames,
        "pos_bins": pos_bins,
        "pos_vals": pos_vals,
        "solo_cnt": solo_cnt,
        "kind_cnt": kind_cnt,
        "site_cnt": site_cnt,
        "time_cnt": time_cnt,
        "slot_cnt": slot_cnt,
        "tok_cnt": tok_cnt,
    }


def diagnose_workshop_driver(a, b, prof, p_kind, p_site, p_time):
    """Identify if a pair is driven by carving medium (ctab/mtab/pot), regional site, or period."""
    drivers = []
    if p_kind < 0.05:
        ka, kb = prof["kind_cnt"][a], prof["kind_cnt"][b]
        na, nb = max(1, sum(ka.values())), max(1, sum(kb.values()))
        # Largest absolute share difference
        diffs = sorted(
            ((kb.get(k, 0) / nb - ka.get(k, 0) / na, k) for k in set(ka) | set(kb)),
            key=lambda x: abs(x[0]),
            reverse=True,
        )
        if diffs:
            d, k = diffs[0]
            who = b if d > 0 else a
            drivers.append(f"medium:{k}({who}:{100*(kb[k]/nb if d>0 else ka[k]/na):.0f}% vs {100*(ka[k]/na if d>0 else kb[k]/nb):.0f}%)")
    if p_site < 0.05:
        sa, sb = prof["site_cnt"][a], prof["site_cnt"][b]
        na, nb = max(1, sum(sa.values())), max(1, sum(sb.values()))
        diffs = sorted(
            ((sb.get(k, 0) / nb - sa.get(k, 0) / na, k) for k in set(sa) | set(sb)),
            key=lambda x: abs(x[0]),
            reverse=True,
        )
        if diffs:
            d, k = diffs[0]
            who = b if d > 0 else a
            drivers.append(f"site:{k}({who}:{100*(sb[k]/nb if d>0 else sa[k]/na):.0f}% vs {100*(sa[k]/na if d>0 else sb[k]/nb):.0f}%)")
    if p_time < 0.05:
        ta, tb = prof["time_cnt"][a], prof["time_cnt"][b]
        na, nb = max(1, sum(ta.values())), max(1, sum(tb.values()))
        diffs = sorted(
            ((tb.get(k, 0) / nb - ta.get(k, 0) / na, k) for k in set(ta) | set(tb)),
            key=lambda x: abs(x[0]),
            reverse=True,
        )
        if diffs:
            d, k = diffs[0]
            who = b if d > 0 else a
            drivers.append(f"period:{k}({who}:{100*(tb[k]/nb if d>0 else ta[k]/na):.0f}%)")
    return "; ".join(drivers)


# ==============================================================================
# 5. GENERATE & SCORE ALL CANDIDATE PAIRS ACROSS THE 638 INTACT SIGN INVENTORY
# ==============================================================================
def build_candidates_and_classify(data, prof):
    intact_set = set(data["intact_signs"])

    # Index cross-catalogue groups restricted to the 638 intact Lipi signs
    by_p = defaultdict(list)
    for s in data["intact_signs"]:
        p = data["parpola_p"].get(s, "")
        if p:
            by_p[p].append(s)
    # Add crosswalk_edges lipi->P mergers
    by_ce_p = defaultdict(list)
    for s, lst in data["ce_lipi_to_p"].items():
        if s in intact_set:
            for tid, st, sh, sup in lst:
                by_ce_p[tid].append(s)

    by_m = defaultdict(list)
    for s in data["intact_signs"]:
        m = data["mah_m"].get(s, "")
        if m:
            by_m[m].append(s)
    # Also add P->M chain from crosswalk_edges
    by_ce_m = defaultdict(set)
    for s in data["intact_signs"]:
        p = data["parpola_p"].get(s, "")
        for m in data["ce_p_to_m"].get(p, ()):
            by_ce_m[m].add(s)

    cand_sources = defaultdict(set)

    def add_group(grp, tag):
        g = sorted(set(x for x in grp if x in intact_set))
        for i in range(len(g)):
            for j in range(i + 1, len(g)):
                cand_sources[(g[i], g[j])].add(tag)

    for p, grp in by_p.items():
        if len(grp) >= 2:
            add_group(grp, f"Parpola:{p}")
    for p, grp in by_ce_p.items():
        if len(grp) >= 2:
            add_group(grp, f"CE_P:{p}")
    for m, grp in by_m.items():
        if len(grp) >= 2:
            add_group(grp, f"Mahadevan:M{m}")
    for m, grp in by_ce_m.items():
        if len(grp) >= 2:
            add_group(grp, f"CE_PM:{m}")

    # Signal 2a: High shape Jaccard (>= 0.72) across different P-codes
    described = [s for s in data["intact_signs"] if s in data["shapes"]]
    tok_cache = {s: shape_tokens(data["shapes"][s]) for s in described}
    for i in range(len(described)):
        sa = described[i]
        wa = tok_cache[sa]
        if len(wa) < 3:
            continue
        for j in range(i + 1, len(described)):
            sb = described[j]
            wb = tok_cache[sb]
            if len(wb) < 3:
                continue
            jac = len(wa & wb) / len(wa | wb)
            if jac >= 0.72:
                cand_sources[(sa, sb)].add("ShapeSim>=0.72")

    # Signal 2b: Wells numerical neighborhood (<=3) for undocumented rare signs sharing a swap frame or cos >= 0.5
    num_intact = sorted(s for s in data["intact_signs"] if s.isdigit())
    for i in range(len(num_intact)):
        sa = num_intact[i]
        ia = int(sa)
        for j in range(i + 1, len(num_intact)):
            sb = num_intact[j]
            if int(sb) - ia > 3:
                break
            if (sa in data["shapes"]) and (sb in data["shapes"]):
                continue
            # Require distributional hint so we don't generate noise
            swp = sum(1 for f in prof["frames"][sa] if f in prof["frames"][sb])
            if swp >= 1:
                cand_sources[(sa, sb)].add("WellsAdj<=3+Swap")

    # Add split-test benchmarks
    for a, b in SPLIT_BENCHMARK_PAIRS:
        if a in intact_set and b in intact_set:
            cand_sources[tuple(sorted((a, b)))].add("SplitBenchmark")

    rows = []
    for (a, b), srcs in sorted(cand_sources.items()):
        pa = data["parpola_p"].get(a, "")
        pb = data["parpola_p"].get(b, "")
        ma = data["mah_m"].get(a, "")
        mb = data["mah_m"].get(b, "")
        same_p = bool(pa and pb and pa == pb) or any(s.startswith("CE_P:") for s in srcs)
        same_p_strict = bool(pa and pb and pa == pb)
        same_m = bool(ma and mb and ma == mb) or any(s.startswith("CE_PM:") for s in srcs)
        same_m_strict = bool(ma and mb and ma == mb)
        both_pm = same_p_strict and same_m_strict

        da, db = data["shapes"].get(a, ""), data["shapes"].get(b, "")
        sjac = shape_jaccard(da, db)
        wdist = abs(int(a) - int(b)) if (a.isdigit() and b.isdigit()) else 999
        is_comp_veto, comp_reason = detect_graphic_compound_veto(a, b, data)

        na_ev, nb_ev = prof["tok_cnt"][a], prof["tok_cnt"][b]
        na_int = data["intact_lipi_cnt"][a]
        nb_int = data["intact_lipi_cnt"][b]
        min_n = min(na_ev, nb_ev)

        # Neighbor vectors
        v1 = {("L", k): v for k, v in prof["left_nb"][a].items()}
        v1.update({("R", k): v for k, v in prof["right_nb"][a].items()})
        v2 = {("L", k): v for k, v in prof["left_nb"][b].items()}
        v2.update({("R", k): v for k, v in prof["right_nb"][b].items()})
        lr_cos = cosine_counters(v1, v2)

        v1nb = {("L", k): v for k, v in prof["left_nb_nobnd"][a].items()}
        v1nb.update({("R", k): v for k, v in prof["right_nb_nobnd"][a].items()})
        v2nb = {("L", k): v for k, v in prof["left_nb_nobnd"][b].items()}
        v2nb.update({("R", k): v for k, v in prof["right_nb_nobnd"][b].items()})
        lr_cos_nobnd = cosine_counters(v1nb, v2nb)

        swaps = sum(1 for f in prof["frames"][a] if f in prof["frames"][b])

        # Position stats
        pos_a = float(np.mean(prof["pos_vals"][a])) if prof["pos_vals"][a] else -1.0
        pos_b = float(np.mean(prof["pos_vals"][b])) if prof["pos_vals"][b] else -1.0
        pos_diff = abs(pos_a - pos_b) if (pos_a >= 0 and pos_b >= 0) else 0.0
        pos_chi, pos_df, p_pos = contingency_chi2(prof["pos_bins"][a], prof["pos_bins"][b])

        # Grammar slot stats
        slot_chi, slot_df, p_slot = contingency_chi2(prof["slot_cnt"][a], prof["slot_cnt"][b])
        dom_slot_a = prof["slot_cnt"][a].most_common(1)[0] if prof["slot_cnt"][a] else ("", 0)
        dom_slot_b = prof["slot_cnt"][b].most_common(1)[0] if prof["slot_cnt"][b] else ("", 0)
        dom_share_a = dom_slot_a[1] / max(1, sum(prof["slot_cnt"][a].values()))
        dom_share_b = dom_slot_b[1] / max(1, sum(prof["slot_cnt"][b].values()))
        same_strong_slot = (dom_slot_a[0] != "" and dom_slot_a[0] == dom_slot_b[0] and dom_share_a >= 0.80 and dom_share_b >= 0.80)

        # Kind, site, period stats
        kind_chi, kind_df, p_kind = contingency_chi2_collapsed(prof["kind_cnt"][a], prof["kind_cnt"][b], top_k=6)
        kind_cos = cosine_counters(prof["kind_cnt"][a], prof["kind_cnt"][b])
        site_chi, site_df, p_site = contingency_chi2_collapsed(prof["site_cnt"][a], prof["site_cnt"][b], top_k=6)
        time_chi, time_df, p_time = contingency_chi2(prof["time_cnt"][a], prof["time_cnt"][b])

        # Co-occurrence exclusion
        ev_a, ev_b = prof["ev_presence"][a], prof["ev_presence"][b]
        cooc_obs = len(ev_a & ev_b)
        cooc_exp = len(ev_a) * len(ev_b) / prof["N_ev"]
        cooc_ratio = (cooc_obs / cooc_exp) if cooc_exp > 0 else 0.0
        p_cooc_depl = hypergeom_le(cooc_obs, prof["N_ev"], len(ev_a), len(ev_b))
        p_cooc_exc = hypergeom_ge(cooc_obs, prof["N_ev"], len(ev_a), len(ev_b))
        cooc_excess_veto = (cooc_obs >= 2 and cooc_obs > cooc_exp) or (cooc_obs >= 3 and cooc_ratio >= 0.5)

        # Special object-functional clash check: ctab vs bangle (e.g. 850 copper vs 790 bangle)
        ctab_a, ctab_b = prof["kind_cnt"][a].get("ctab", 0), prof["kind_cnt"][b].get("ctab", 0)
        bang_a, bang_b = prof["kind_cnt"][a].get("bangle", 0), prof["kind_cnt"][b].get("bangle", 0)
        p_ctab_bangle = 1.0
        if (ctab_a >= 5 and bang_b >= 4 and ctab_b == 0 and bang_a == 0) or (ctab_b >= 5 and bang_a >= 4 and ctab_a == 0 and bang_b == 0):
            # Exact Fisher 2x2 on (ctab, bangle)
            m_tot = ctab_a + ctab_b + bang_a + bang_b
            p_ctab_bangle = hypergeom_le(0, m_tot, ctab_a + ctab_b, ctab_a + bang_a) * 2.0
            p_ctab_bangle = min(1.0, p_ctab_bangle)

        # Two DIFFERENT core locked/loan signs clash (e.g. 850 *kaṉ vs 790 *vaḷai, 002 vs 032, 220 vs 235)
        distinct_locked_clash = False
        if a in LOCKED19 and b in LOCKED19 and a != b:
            distinct_locked_clash = True
        if (a in LOCKED19 and b in LOAN_ANCHORS) or (b in LOCKED19 and a in LOAN_ANCHORS):
            distinct_locked_clash = True

        workshop_driver = diagnose_workshop_driver(a, b, prof, p_kind, p_site, p_time)

        # ------------------------------------------------------------------
        # TIERED CLASSIFICATION LOGIC (Pure Corpus Measures — Zero v2_class Circularity!)
        # ------------------------------------------------------------------
        verdict = "UNRESOLVED_RARE"
        reason = ""

        # Pure positional compatibility: statistically indistinguishable OR tiny shift (<0.15) with extreme neighbor match
        pos_divergent_strong = (min_n >= 8 and p_pos < 0.005 and pos_diff >= 0.15)
        pos_ok = (p_pos >= 0.01) or (pos_diff < 0.15 and lr_cos >= 0.80) or (min_n <= 4 and p_pos >= 0.005)
        # Note: p_slot is still logged for transparency, never used to veto rare signs against v2_class frequency cutoffs

        # A. Graphic compound / ligature veto
        if is_comp_veto:
            if same_p or same_m:
                verdict = "FALSE_MERGER"
                reason = f"catalogue_lumped_compound:{comp_reason}"
            else:
                verdict = "GRAPHIC_COMPOUND"
                reason = comp_reason

        # B. Functional contradiction / FALSE MERGER test
        elif (
            distinct_locked_clash
            or p_ctab_bangle < 0.005
            or cooc_excess_veto
            or pos_divergent_strong
            or (min_n >= 10 and lr_cos < 0.25 and swaps == 0)
            or (min_n >= 8 and lr_cos < 0.15)
        ):
            if same_p or same_m or "SplitBenchmark" in srcs:
                verdict = "FALSE_MERGER"
                rparts = []
                if distinct_locked_clash:
                    rparts.append("distinct_locked_signs")
                if p_ctab_bangle < 0.005:
                    rparts.append(f"ctab_vs_bangle_p={p_ctab_bangle:.5f}")
                if cooc_excess_veto:
                    rparts.append(f"cooc_excess({cooc_obs}>{cooc_exp:.1f})")
                if pos_divergent_strong:
                    rparts.append(f"pos_div(p={p_pos:.2e},d={pos_diff:.2f})")
                if min_n >= 8 and lr_cos < 0.25:
                    rparts.append(f"low_ctx_cos({lr_cos:.2f})")
                reason = ";".join(rparts)
            else:
                verdict = "DISTINCT_NON_ALLOGRAPH"
                reason = "distributional_divergence"

        # C. Verified Allograph Candidates (must have cross-catalogue visual support: same_P or same_M!)
        elif same_p_strict or same_m_strict:
            cooc_clean = (
                (cooc_obs == 0)
                or (cooc_exp >= 4.0 and cooc_ratio < 0.25)
                or (cooc_obs == 1 and min_n >= 10 and cooc_ratio <= 1.3 and lr_cos >= 0.80)
            )
            kind_pure_ok = (p_kind >= 0.05)
            site_pure_ok = (p_site >= 0.05)
            has_workshop_diff = (p_kind < 0.05) or (p_site < 0.05) or (p_time < 0.05)

            if min_n >= 5:
                # Medium/High-frequency pair: strict separation of Tier 1 Pure vs Tier 2 Workshop
                if cooc_clean and pos_ok and kind_pure_ok and site_pure_ok and (
                    lr_cos >= 0.35 or swaps >= 1 or (both_pm and lr_cos >= 0.20)
                ):
                    verdict = "VERIFIED_PURE"
                    reason = f"pure_allograph(cos={lr_cos:.2f},swp={swaps},p_pos={p_pos:.2f},p_kind={p_kind:.2f},p_site={p_site:.2f})"
                elif cooc_clean and pos_ok and has_workshop_diff and (
                    (lr_cos >= 0.60 and swaps >= 2)
                    or (lr_cos >= 0.70 and swaps >= 1)
                    or (both_pm and lr_cos >= 0.80)
                ):
                    verdict = "VERIFIED_WORKSHOP"
                    reason = f"workshop_allograph(cos={lr_cos:.2f},swp={swaps},p_pos={p_pos:.2f},{workshop_driver})"
                elif cooc_clean and pos_ok and kind_pure_ok and not site_pure_ok and (lr_cos >= 0.35 or swaps >= 1):
                    # Pure medium, site-differentiated -> Tier 2 Workshop/Regional
                    verdict = "VERIFIED_WORKSHOP"
                    reason = f"regional_allograph(cos={lr_cos:.2f},swp={swaps},{workshop_driver})"
                elif not pos_ok or (min_n >= 5 and lr_cos < 0.25):
                    verdict = "FALSE_MERGER"
                    reason = f"divergent_medium_freq(cos={lr_cos:.2f},p_pos={p_pos:.3f},p_kind={p_kind:.3f})"
                else:
                    verdict = "UNRESOLVED_MEDIUM"
                    reason = f"borderline(cos={lr_cos:.2f},swp={swaps},p_pos={p_pos:.3f},p_kind={p_kind:.3f})"
            else:
                # Rare pair (min_n <= 4): requires explicit human-expert visual-equivalence + non-zero context support
                visual_strong = same_p_strict or (same_m_strict and wdist <= 5) or both_pm
                no_contradiction = (cooc_obs == 0) and pos_ok and (p_kind >= 0.01)
                ctx_support = (lr_cos >= 0.25) or (swaps >= 1) or both_pm
                if visual_strong and no_contradiction and ctx_support:
                    if p_kind < 0.05 or p_site < 0.01:
                        verdict = "VERIFIED_WORKSHOP"
                        reason = f"rare_workshop_allograph(min_n={min_n},cos={lr_cos:.2f},swp={swaps},{workshop_driver})"
                    else:
                        verdict = "VERIFIED_PURE"
                        reason = f"rare_pure_allograph(min_n={min_n},cos={lr_cos:.2f},swp={swaps},P={same_p_strict},M={same_m_strict},wd={wdist})"
                elif visual_strong and (cooc_obs == 0) and (not pos_ok or p_kind < 0.01):
                    verdict = "FALSE_MERGER"
                    reason = f"rare_pos_or_kind_div(p_pos={p_pos:.3f},p_kind={p_kind:.3f})"
                else:
                    verdict = "UNRESOLVED_RARE"
                    reason = f"insufficient_rare_ctx(min_n={min_n},cos={lr_cos:.2f},swp={swaps},wd={wdist})"
        else:
            # Non-P/M pair (e.g. CE_PM mirror)
            if "CE_PM:" in " ".join(srcs) and not is_comp_veto and cooc_obs == 0 and pos_ok and p_kind >= 0.05 and (lr_cos >= 0.35 or swaps >= 1):
                verdict = "VERIFIED_PURE"
                reason = f"ce_pm_mirror_allograph(cos={lr_cos:.2f},swp={swaps})"
            else:
                verdict = "UNRESOLVED_RARE"
                reason = "no_direct_P_or_M_merger"

        rows.append({
            "a": a, "b": b,
            "n_ev_a": na_ev, "n_ev_b": nb_ev,
            "n_intact_a": na_int, "n_intact_b": nb_int,
            "sources": "|".join(sorted(srcs)),
            "parpola_a": pa, "parpola_b": pb, "same_P": same_p_strict,
            "mah_a": ma, "mah_b": mb, "same_M": same_m_strict,
            "both_PM": both_pm,
            "shape_jaccard": round(sjac, 3),
            "wells_dist": wdist,
            "comp_veto": is_comp_veto, "comp_reason": comp_reason,
            "lr_cos": round(lr_cos, 4),
            "lr_cos_nobnd": round(lr_cos_nobnd, 4),
            "swap_frames": swaps,
            "pos_a": round(pos_a, 3), "pos_b": round(pos_b, 3), "pos_diff": round(pos_diff, 3),
            "p_pos": round(p_pos, 6),
            "dom_slot_a": f"{dom_slot_a[0]}({dom_share_a:.2f})",
            "dom_slot_b": f"{dom_slot_b[0]}({dom_share_b:.2f})",
            "p_slot": round(p_slot, 6),
            "kind_cos": round(kind_cos, 4),
            "p_kind": round(p_kind, 6),
            "p_site": round(p_site, 6),
            "p_time": round(p_time, 6),
            "cooc_obs": cooc_obs,
            "cooc_exp": round(cooc_exp, 3),
            "cooc_ratio": round(cooc_ratio, 3),
            "p_cooc_depl": round(p_cooc_depl, 6),
            "workshop_driver": workshop_driver,
            "verdict": verdict,
            "reason": reason,
            "shape_a": da[:80], "shape_b": db[:80],
        })

    return rows


# ==============================================================================
# 6. VETO-CONSTRAINED CLUSTERING (ZERO TRANSITIVE CHAINING ARTIFACTS)
# ==============================================================================
def build_clusters(cand_rows, allowed_verdicts, data):
    """
    Greedy highest-evidence-first union-find with strict pairwise veto checking:
    two clusters never merge if ANY cross-pair is a FALSE_MERGER or GRAPHIC_COMPOUND
    or links two distinct LOCKED19/LOAN signs!
    """
    veto_pairs = set()
    pure_only_mode = ("VERIFIED_WORKSHOP" not in allowed_verdicts)
    for r in cand_rows:
        if r["verdict"] in ("FALSE_MERGER", "GRAPHIC_COMPOUND", "DISTINCT_NON_ALLOGRAPH") or r["comp_veto"]:
            veto_pairs.add((r["a"], r["b"]))
        elif pure_only_mode and r["verdict"] == "VERIFIED_WORKSHOP":
            # Prevent a rare intermediate bridge from pulling a medium/site-divergent Tier 2 sign into Tier 1 Pure
            veto_pairs.add((r["a"], r["b"]))

    # Also veto merging any two distinct core sound targets (except same-value numerals like 005/015, 004/014)
    def locked_conflict(s1, s2):
        if s1 in LOCKED19 and s2 in LOCKED19 and s1 != s2:
            return True
        if (s1 in LOCKED19 and s2 in LOAN_ANCHORS) or (s2 in LOCKED19 and s1 in LOAN_ANCHORS):
            return True
        if s1 in LOAN_ANCHORS and s2 in LOAN_ANCHORS and LOAN_ANCHORS[s1][0] != LOAN_ANCHORS[s2][0]:
            return True
        if s1 in BASIC_NUMS and s2 in BASIC_NUMS and BASIC_NUMS[s1][0] != BASIC_NUMS[s2][0]:
            return True
        return False

    # Rank candidate edges by evidence strength
    edges = [r for r in cand_rows if r["verdict"] in allowed_verdicts]
    edges.sort(
        key=lambda r: (
            1 if r["verdict"] == "VERIFIED_PURE" else 0,
            1 if r["both_PM"] else 0,
            r["swap_frames"],
            r["lr_cos"],
        ),
        reverse=True,
    )

    parent = {s: s for s in data["intact_signs"]}
    members = {s: {s} for s in data["intact_signs"]}
    used_edges = []

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for r in edges:
        ra, rb = find(r["a"]), find(r["b"])
        if ra == rb:
            used_edges.append(r)
            continue
        # Check cross-cluster vetoes
        blocked = False
        for x in members[ra]:
            for y in members[rb]:
                p = tuple(sorted((x, y)))
                if p in veto_pairs or locked_conflict(x, y):
                    blocked = True
                    break
            if blocked:
                break
        if blocked:
            continue
        # Merge rb into ra
        parent[rb] = ra
        members[ra] |= members[rb]
        del members[rb]
        used_edges.append(r)

    # Choose canonical representative per cluster:
    # priority: LOCKED19 > LOAN_ANCHORS > BASIC_NUMS > highest intact Lipi frequency
    clusters = {}
    sign_to_canon = {}
    for root, mset in members.items():
        def canon_key(s):
            tier = 3 if s in LOCKED19 else (2 if s in LOAN_ANCHORS else (1 if s in BASIC_NUMS else 0))
            return (tier, data["intact_lipi_cnt"][s], -int(s) if s.isdigit() else 0)
        canon = max(mset, key=canon_key)
        # Never allow a low-frequency LOAN_ANCHOR (like 838 n=13) to take over a 10x larger cluster unless same_P/M
        if canon in LOAN_ANCHORS and data["intact_lipi_cnt"][canon] * 5 < sum(data["intact_lipi_cnt"][x] for x in mset):
            canon = max(mset, key=lambda s: data["intact_lipi_cnt"][s])
        clusters[canon] = sorted(mset, key=lambda s: (-data["intact_lipi_cnt"][s], s))
        for s in mset:
            sign_to_canon[s] = canon

    return clusters, sign_to_canon, used_edges


# ==============================================================================
# 7. HELD-OUT PERPLEXITY ENGINE (5-FOLD LIPI CV + UNSEEN NEW TEXTS + 2,000 RAND)
# ==============================================================================
def extract_sequences_from_events(events, vocab_to_id):
    """Extract clean intact sign sequences (split at damaged '000' or unmapped 'X' tokens)."""
    seqs = []
    for ev_idx, ev in enumerate(events):
        ev_seqs = []
        for face in ev["faces"]:
            cur = []
            for s in face:
                if s in vocab_to_id:
                    cur.append(vocab_to_id[s])
                else:
                    if cur:
                        ev_seqs.append(cur)
                        cur = []
            if cur:
                ev_seqs.append(cur)
        seqs.append((ev_idx, ev_seqs))
    return seqs


def seqs_to_bigram_arrays(ev_seq_list):
    """Flatten list of (ev_idx, [[id,...], ...]) into (prev_arr, curr_arr) with BOS=0, EOS=1."""
    prevs, currs = [], []
    for _, seqs in ev_seq_list:
        for seq in seqs:
            p = 0  # BOS
            for x in seq:
                prevs.append(p)
                currs.append(x)
                p = x
            prevs.append(p)
            currs.append(1)  # EOS
    return np.array(prevs, dtype=np.int32), np.array(currs, dtype=np.int32)


def eval_brown_and_context_bps(tr_prev, tr_curr, te_prev, te_curr, cmap, V_total, alpha_bi=1.0, alpha_uni=0.05):
    """
    Evaluate EXACT prior-invariant held-out bits-per-sign on test transitions (te_prev, te_curr):
      1. brown_bps:    Exact uncollapsed generative Brown-class bigram:
                       P(x_t | x_{t-1}) = P_bi(c(x_t) | c(x_{t-1})) * P_emit(x_t | c(x_t))
      2. ctx_pool_bps: Context-only pooling (uncollapsed target x_t, collapsed context c(x_{t-1})):
                       P(x_t | c(x_{t-1}))
      3. coll_bps:     Collapsed-alphabet bigram entropy H(c(x_t) | c(x_{t-1}))
                       (strictly fair when compared against frequency-matched random merges of
                        IDENTICAL cluster structure!)
    V_total includes BOS(0), EOS(1), and all signs 2..V_total-1.
    Non-BOS vocabulary size V_eff = V_total - 1 (EOS + signs).
    """
    C = int(cmap.max()) + 1
    V_eff = V_total - 1  # EOS + signs

    # Class sizes |c| for non-BOS symbols (ids 1..V_total-1)
    c_size = np.bincount(cmap[1:], minlength=C).astype(np.float64)

    # Training unigram counts (exact sign & class)
    tr_u_sign = np.bincount(tr_curr, minlength=V_total).astype(np.float64)
    tr_u_cls = np.bincount(cmap[tr_curr], minlength=C).astype(np.float64)
    N_tok = float(tr_curr.size)

    # Prior-invariant unigram class distribution P_u(c) & sign distribution P_u(x)
    denom_u = N_tok + alpha_uni * V_eff
    P_u_cls = (tr_u_cls + alpha_uni * c_size) / denom_u
    P_u_sign = (tr_u_sign + alpha_uni) / denom_u

    # Intra-class emission P_emit(x | c(x))
    emit_denom = tr_u_cls[cmap] + alpha_uni * c_size[cmap]
    P_emit = (tr_u_sign + alpha_uni) / np.maximum(emit_denom, 1e-12)

    # Class bigram counts via flat bincount
    tr_c1 = cmap[tr_prev]
    tr_c2 = cmap[tr_curr]
    tr_c1_cnt = np.bincount(tr_c1, minlength=C).astype(np.float64)
    flat_tr = tr_c1 * C + tr_c2
    # Use sparse lookup via sorted unique keys or dense matrix (C <= 720 -> C*C <= 520k floats = 4MB, super fast!)
    bi_cls = np.bincount(flat_tr, minlength=C * C).astype(np.float64)

    te_c1 = cmap[te_prev]
    te_c2 = cmap[te_curr]
    n_c1c2 = bi_cls[te_c1 * C + te_c2]
    n_c1 = tr_c1_cnt[te_c1]
    P_bi_cls = (n_c1c2 + alpha_bi * P_u_cls[te_c2]) / (n_c1 + alpha_bi)

    # 1. Brown-class generative uncollapsed BPS
    P_brown = P_bi_cls * P_emit[te_curr]
    brown_bps = float(-np.mean(np.log2(P_brown)))

    # 3. Collapsed-alphabet bigram BPS
    coll_bps = float(-np.mean(np.log2(P_bi_cls)))

    # 2. Context-only pooling P(x_t | c(x_{t-1}))
    flat_ctx = tr_c1 * V_total + tr_curr
    bi_ctx = np.bincount(flat_ctx, minlength=C * V_total).astype(np.float64)
    n_c1x2 = bi_ctx[te_c1 * V_total + te_curr]
    P_ctx = (n_c1x2 + alpha_bi * P_u_sign[te_curr]) / (n_c1 + alpha_bi)
    ctx_bps = float(-np.mean(np.log2(P_ctx)))

    return brown_bps, ctx_bps, coll_bps


def make_cmap(clusters, vocab_to_id, V_total):
    """Build dense integer array cmap[0..V_total-1] -> compact class IDs 0..C-1."""
    raw = np.arange(V_total, dtype=np.int32)
    for canon, mlist in clusters.items():
        if len(mlist) <= 1:
            continue
        if canon not in vocab_to_id:
            continue
        cid = vocab_to_id[canon]
        for s in mlist:
            if s in vocab_to_id:
                raw[vocab_to_id[s]] = cid
    # Compress to 0..C-1
    _, inv = np.unique(raw, return_inverse=True)
    return inv.astype(np.int32)


def sample_freq_matched_random_cmap(clusters, vocab_to_id, freq_by_id, V_total, rng):
    """
    Generate a random sign-merge partition with the EXACT same number of multi-sign clusters
    and EXACT same cluster sizes, matching EVERY merged member's log2-frequency band!
    """
    # Build frequency bands over sign IDs 2..V_total-1
    sign_ids = np.arange(2, V_total, dtype=np.int32)
    freqs = np.array([freq_by_id[i] for i in sign_ids], dtype=np.float64)
    bands = np.floor(np.log2(np.maximum(freqs, 1.0))).astype(np.int32)
    band_to_ids = defaultdict(list)
    for sid, b in zip(sign_ids, bands):
        band_to_ids[int(b)].append(int(sid))

    # Extract target multi-sign cluster band signatures
    target_sigs = []
    for canon, mlist in clusters.items():
        ids = [vocab_to_id[s] for s in mlist if s in vocab_to_id]
        if len(ids) >= 2:
            sigs = [int(math.floor(math.log2(max(freq_by_id[i], 1)))) for i in ids]
            target_sigs.append(sigs)

    # Shuffle available pools per band
    pools = {}
    for b, lst in band_to_ids.items():
        arr = lst[:]
        rng.shuffle(arr)
        pools[b] = arr
    all_bands = sorted(pools.keys())

    def pop_from_band(b):
        if pools.get(b):
            return pools[b].pop()
        # Nearest non-empty band
        for delta in range(1, 20):
            for nb in (b - delta, b + delta):
                if pools.get(nb):
                    return pools[nb].pop()
        return None

    raw = np.arange(V_total, dtype=np.int32)
    for sigs in target_sigs:
        picked = []
        for b in sigs:
            x = pop_from_band(b)
            if x is not None:
                picked.append(x)
        if len(picked) >= 2:
            head = picked[0]
            for x in picked[1:]:
                raw[x] = head
    _, inv = np.unique(raw, return_inverse=True)
    return inv.astype(np.int32)


def run_perplexity_suite(data, clusters_pure, clusters_all, cand_rows):
    t0 = time.time()
    # Vocabulary: all signs appearing in Lipi (708) or New (190) -> union
    all_signs = sorted(
        set(data["intact_signs"])
        | {s for ev in data["ev_lipi"] for f in ev["faces"] for s in f if s and s != "000" and not s.startswith("X")}
        | {s for ev in data["ev_new"] for f in ev["faces"] for s in f if s and s != "000" and not s.startswith("X")}
    )
    vocab_to_id = {s: i + 2 for i, s in enumerate(all_signs)}
    V_total = len(all_signs) + 2

    lipi_seqs = extract_sequences_from_events(data["ev_lipi"], vocab_to_id)
    new_seqs = extract_sequences_from_events(data["ev_new"], vocab_to_id)

    # Compute Lipi token frequency per id for frequency-matched null sampling
    full_lp_prev, full_lp_curr = seqs_to_bigram_arrays(lipi_seqs)
    full_nw_prev, full_nw_curr = seqs_to_bigram_arrays(new_seqs)
    freq_by_id = np.bincount(full_lp_curr, minlength=V_total)

    # 5-fold deterministic split over Lipi events
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(lipi_seqs))
    fold_ids = np.zeros(len(lipi_seqs), dtype=np.int32)
    for idx, ev_i in enumerate(perm):
        fold_ids[ev_i] = idx % 5

    folds = []
    for k in range(5):
        tr_list = [lipi_seqs[i] for i in range(len(lipi_seqs)) if fold_ids[i] != k]
        te_list = [lipi_seqs[i] for i in range(len(lipi_seqs)) if fold_ids[i] == k]
        folds.append((*seqs_to_bigram_arrays(tr_list), *seqs_to_bigram_arrays(te_list)))

    # Build cmaps
    cmap_base = np.arange(V_total, dtype=np.int32)
    cmap_pure = make_cmap(clusters_pure, vocab_to_id, V_total)
    cmap_all = make_cmap(clusters_all, vocab_to_id, V_total)

    # Negative control: merge caught FALSE_MERGER pairs (top 30 false mergers by frequency)
    fm_rows = [r for r in cand_rows if r["verdict"] == "FALSE_MERGER"]
    fm_rows.sort(key=lambda r: min(r["n_ev_a"], r["n_ev_b"]), reverse=True)
    fm_clusters = {}
    used_fm = set()
    for r in fm_rows:
        if r["a"] not in used_fm and r["b"] not in used_fm:
            fm_clusters[r["a"]] = [r["a"], r["b"]]
            used_fm.add(r["a"])
            used_fm.add(r["b"])
            if len(fm_clusters) >= 25:
                break
    cmap_fm = make_cmap(fm_clusters, vocab_to_id, V_total)

    # Non-Mahadevan-shared subset on unseen new texts: ONLY clusters where >=2 members appear in events_new!
    new_tok_cnt = Counter(s for ev in data["ev_new"] for f in ev["faces"] for s in f if s and s != "000" and not s.startswith("X"))
    clusters_both_in_new = {
        c: [s for s in mlist if new_tok_cnt[s] > 0]
        for c, mlist in clusters_all.items()
        if sum(1 for s in mlist if new_tok_cnt[s] > 0) >= 2
    }
    cmap_both_in_new = make_cmap(clusters_both_in_new, vocab_to_id, V_total)

    # Unconfounded False-Merger Control (both signs appear in unseen new texts, e.g. 002/032, 740/741, 790/850, 900/920, 550/555)
    fm_new_rows = [
        r for r in cand_rows
        if r["verdict"] in ("FALSE_MERGER", "GRAPHIC_COMPOUND")
        and new_tok_cnt[r["a"]] > 0 and new_tok_cnt[r["b"]] > 0
    ]
    fm_new_rows.sort(key=lambda r: min(new_tok_cnt[r["a"]], new_tok_cnt[r["b"]]), reverse=True)
    fm_new_clusters = {}
    used_fmn = set()
    for r in fm_new_rows:
        if r["a"] not in used_fmn and r["b"] not in used_fmn:
            fm_new_clusters[r["a"]] = [r["a"], r["b"]]
            used_fmn.add(r["a"])
            used_fmn.add(r["b"])
            if len(fm_new_clusters) >= 15:
                break
    cmap_fm_new = make_cmap(fm_new_clusters, vocab_to_id, V_total)

    def eval_5fold(cmap, alpha_bi=1.0):
        bs, cs, ks = [], [], []
        tot_n = 0
        for tr_p, tr_c, te_p, te_c in folds:
            b, c, k = eval_brown_and_context_bps(tr_p, tr_c, te_p, te_c, cmap, V_total, alpha_bi=alpha_bi)
            w = te_c.size
            bs.append(b * w)
            cs.append(c * w)
            ks.append(k * w)
            tot_n += w
        return sum(bs) / tot_n, sum(cs) / tot_n, sum(ks) / tot_n

    def eval_new(cmap, alpha_bi=1.0):
        return eval_brown_and_context_bps(full_lp_prev, full_lp_curr, full_nw_prev, full_nw_curr, cmap, V_total, alpha_bi=alpha_bi)

    # Evaluate deterministic models across alpha sensitivity {0.5, 1.0, 2.0}
    models = {
        "baseline_unmerged": cmap_base,
        "verified_pure": cmap_pure,
        "verified_pure_plus_workshop": cmap_all,
        "false_merger_neg_control": cmap_fm,
        "false_merger_both_in_new_ctrl": cmap_fm_new,
        "both_in_new_subset": cmap_both_in_new,
    }
    res_models = {}
    for name, cm in models.items():
        cv_b, cv_c, cv_k = eval_5fold(cm, alpha_bi=1.0)
        nw_b, nw_c, nw_k = eval_new(cm, alpha_bi=1.0)
        cv_b05, _, _ = eval_5fold(cm, alpha_bi=0.5)
        cv_b20, _, _ = eval_5fold(cm, alpha_bi=2.0)
        nw_b05, _, _ = eval_new(cm, alpha_bi=0.5)
        nw_b20, _, _ = eval_new(cm, alpha_bi=2.0)
        res_models[name] = {
            "n_classes_total": int(cm.max()) + 1 - 2,
            "lipi_5fold_brown_bps": cv_b,
            "lipi_5fold_ctx_bps": cv_c,
            "lipi_5fold_coll_bps": cv_k,
            "new_brown_bps": nw_b,
            "new_ctx_bps": nw_c,
            "new_coll_bps": nw_k,
            "lipi_5fold_brown_a05": cv_b05,
            "lipi_5fold_brown_a20": cv_b20,
            "new_brown_a05": nw_b05,
            "new_brown_a20": nw_b20,
        }

    # 2,000 Frequency-Matched Random Sign Merges for BOTH Pure and Pure+Workshop!
    null_records = {}
    for tag, clus in [("pure", clusters_pure), ("all", clusters_all)]:
        cv_b_arr = np.empty(N_RAND_MERGES, dtype=np.float64)
        cv_c_arr = np.empty(N_RAND_MERGES, dtype=np.float64)
        cv_k_arr = np.empty(N_RAND_MERGES, dtype=np.float64)
        nw_b_arr = np.empty(N_RAND_MERGES, dtype=np.float64)
        nw_c_arr = np.empty(N_RAND_MERGES, dtype=np.float64)
        nw_k_arr = np.empty(N_RAND_MERGES, dtype=np.float64)
        for it in range(N_RAND_MERGES):
            rcmap = sample_freq_matched_random_cmap(clus, vocab_to_id, freq_by_id, V_total, rng)
            cv_b_arr[it], cv_c_arr[it], cv_k_arr[it] = eval_5fold(rcmap, alpha_bi=1.0)
            nw_b_arr[it], nw_c_arr[it], nw_k_arr[it] = eval_new(rcmap, alpha_bi=1.0)
        mkey = "verified_pure" if tag == "pure" else "verified_pure_plus_workshop"
        obs = res_models[mkey]

        def summarize(obs_val, arr):
            mu = float(np.mean(arr))
            sd = float(np.std(arr, ddof=1))
            z = (obs_val - mu) / sd if sd > 0 else 0.0
            # Lower bits-per-sign is BETTER -> one-sided empirical P(null <= obs)
            p = (int(np.sum(arr <= obs_val)) + 1) / (len(arr) + 1)
            return {
                "obs": obs_val, "null_mean": mu, "null_sd": sd,
                "delta_vs_null": obs_val - mu, "z": z, "p_emp": p,
                "n_rand_better_or_eq": int(np.sum(arr <= obs_val)),
            }

        null_records[tag] = {
            "lipi_5fold_brown_bps": summarize(obs["lipi_5fold_brown_bps"], cv_b_arr),
            "lipi_5fold_ctx_bps": summarize(obs["lipi_5fold_ctx_bps"], cv_c_arr),
            "lipi_5fold_coll_bps": summarize(obs["lipi_5fold_coll_bps"], cv_k_arr),
            "new_brown_bps": summarize(obs["new_brown_bps"], nw_b_arr),
            "new_ctx_bps": summarize(obs["new_ctx_bps"], nw_c_arr),
            "new_coll_bps": summarize(obs["new_coll_bps"], nw_k_arr),
            "_raw": {
                "cv_b": cv_b_arr, "cv_c": cv_c_arr, "cv_k": cv_k_arr,
                "nw_b": nw_b_arr, "nw_c": nw_c_arr, "nw_k": nw_k_arr,
            },
        }

    # Also 2,000 random merges for the non-Mahadevan-shared both_in_new subset!
    bn_nw_b = np.empty(N_RAND_MERGES, dtype=np.float64)
    bn_nw_c = np.empty(N_RAND_MERGES, dtype=np.float64)
    bn_nw_k = np.empty(N_RAND_MERGES, dtype=np.float64)
    for it in range(N_RAND_MERGES):
        rcmap = sample_freq_matched_random_cmap(clusters_both_in_new, vocab_to_id, freq_by_id, V_total, rng)
        bn_nw_b[it], bn_nw_c[it], bn_nw_k[it] = eval_new(rcmap, alpha_bi=1.0)
    obs_bn = res_models["both_in_new_subset"]
    null_records["both_in_new_subset"] = {
        "n_clusters": len(clusters_both_in_new),
        "clusters": clusters_both_in_new,
        "new_brown_bps": {
            "obs": obs_bn["new_brown_bps"],
            "null_mean": float(np.mean(bn_nw_b)),
            "null_sd": float(np.std(bn_nw_b, ddof=1)),
            "delta_vs_null": obs_bn["new_brown_bps"] - float(np.mean(bn_nw_b)),
            "z": (obs_bn["new_brown_bps"] - float(np.mean(bn_nw_b))) / max(float(np.std(bn_nw_b, ddof=1)), 1e-12),
            "p_emp": (int(np.sum(bn_nw_b <= obs_bn["new_brown_bps"])) + 1) / (N_RAND_MERGES + 1),
        },
        "new_ctx_bps": {
            "obs": obs_bn["new_ctx_bps"],
            "null_mean": float(np.mean(bn_nw_c)),
            "null_sd": float(np.std(bn_nw_c, ddof=1)),
            "delta_vs_null": obs_bn["new_ctx_bps"] - float(np.mean(bn_nw_c)),
            "z": (obs_bn["new_ctx_bps"] - float(np.mean(bn_nw_c))) / max(float(np.std(bn_nw_c, ddof=1)), 1e-12),
            "p_emp": (int(np.sum(bn_nw_c <= obs_bn["new_ctx_bps"])) + 1) / (N_RAND_MERGES + 1),
        },
        "new_coll_bps": {
            "obs": obs_bn["new_coll_bps"],
            "null_mean": float(np.mean(bn_nw_k)),
            "null_sd": float(np.std(bn_nw_k, ddof=1)),
            "delta_vs_null": obs_bn["new_coll_bps"] - float(np.mean(bn_nw_k)),
            "z": (obs_bn["new_coll_bps"] - float(np.mean(bn_nw_k))) / max(float(np.std(bn_nw_k, ddof=1)), 1e-12),
            "p_emp": (int(np.sum(bn_nw_k <= obs_bn["new_coll_bps"])) + 1) / (N_RAND_MERGES + 1),
        },
    }

    elapsed = time.time() - t0
    return {
        "elapsed_sec": round(elapsed, 2),
        "n_rand_merges": N_RAND_MERGES,
        "lipi_transitions": int(full_lp_curr.size),
        "new_transitions": int(full_nw_curr.size),
        "models": res_models,
        "null_benchmarks": {
            k: {mk: mv for mk, mv in v.items() if mk != "_raw"}
            for k, v in null_records.items()
        },
        "_null_raw": {k: v["_raw"] for k, v in null_records.items() if "_raw" in v},
        "false_merger_control_pairs": fm_clusters,
    }


# ==============================================================================
# 8. INVENTORY COMPRESSION, CHAO1, SOUND INHERITANCE & COVERAGE BOOST
# ==============================================================================
def compute_chao1(counts_dict):
    S_obs = sum(1 for v in counts_dict.values() if v > 0)
    f1 = sum(1 for v in counts_dict.values() if v == 1)
    f2 = sum(1 for v in counts_dict.values() if v == 2)
    chao1 = S_obs + (f1 * f1) / (2.0 * f2) if f2 > 0 else S_obs + f1 * (f1 - 1) / 2.0
    return S_obs, f1, f2, round(chao1, 1)


def compute_inventory_and_coverage(data, clusters_pure, s2c_pure, clusters_all, s2c_all, cand_rows):
    # Lookup pair row helper
    pair_lookup = {}
    for r in cand_rows:
        pair_lookup[(r["a"], r["b"])] = r
        pair_lookup[(r["b"], r["a"])] = r

    # Inventory stats on 638 intact Lipi signs
    raw_cnt = dict(data["intact_lipi_cnt"])
    pure_cnt = Counter()
    all_cnt = Counter()
    for s, n in raw_cnt.items():
        pure_cnt[s2c_pure.get(s, s)] += n
        all_cnt[s2c_all.get(s, s)] += n

    inv_raw = compute_chao1(raw_cnt)
    inv_pure = compute_chao1(pure_cnt)
    inv_all = compute_chao1(all_cnt)

    # Top-50 / Top-100 / cover80 / cover95 stats
    def cover_stats(cdict):
        vals = sorted(cdict.values(), reverse=True)
        tot = sum(vals)
        acc = 0
        c50 = c80 = c95 = len(vals)
        for idx, v in enumerate(vals, 1):
            acc += v
            if c50 == len(vals) and acc >= 0.50 * tot:
                c50 = idx
            if c80 == len(vals) and acc >= 0.80 * tot:
                c80 = idx
            if c95 == len(vals) and acc >= 0.95 * tot:
                c95 = idx
        return {
            "n_types": len(vals),
            "singletons": sum(1 for v in vals if v == 1),
            "le5": sum(1 for v in vals if v <= 5),
            "cover50": c50, "cover80": c80, "cover95": c95,
            "top50_share": round(sum(vals[:50]) / tot, 4),
            "top100_share": round(sum(vals[:100]) / tot, 4),
        }

    # Sound-inheriting allographs for our 19 locked + 3 loans + basic numerals
    inherited_rows = []
    pure_members_of_target = {}
    all_members_of_target = {}

    for s in data["intact_signs"]:
        if s in ALL_SOUND_TARGETS:
            continue
        cp = s2c_pure.get(s, s)
        ca = s2c_all.get(s, s)
        if cp in ALL_SOUND_TARGETS:
            tier = "TIER1_PURE"
            target = cp
        elif ca in ALL_SOUND_TARGETS:
            tier = "TIER2_WORKSHOP"
            target = ca
        else:
            continue

        t_group = (
            "LOCKED11_K2A" if target in LOCKED11 else
            "PROMOTED8_K3A" if target in PROMOTED8 else
            "LOAN_K2A" if target in LOAN_ANCHORS else
            "BASIC_NUM"
        )
        pr = pair_lookup.get((target, s))
        if tier == "TIER1_PURE" and pr is not None and pr["verdict"] == "VERIFIED_WORKSHOP":
            tier = "TIER2_WORKSHOP"
        inherited_rows.append({
            "allograph": s,
            "canonical_target": target,
            "target_group": t_group,
            "inherited_root": ALL_SOUND_TARGETS[target][0],
            "inherited_gloss": ALL_SOUND_TARGETS[target][1],
            "tier": tier,
            "lipi_intact_toks": data["intact_lipi_cnt"][s],
            "new_intact_toks": data["intact_new_cnt"][s],
            "total_intact_toks": data["intact_lipi_cnt"][s] + data["intact_new_cnt"][s],
            "same_P": pr["same_P"] if pr else "",
            "parpola_code": data["parpola_p"].get(s, ""),
            "same_M": pr["same_M"] if pr else "",
            "mah_code": data["mah_m"].get(s, ""),
            "lr_cos": pr["lr_cos"] if pr else "",
            "swap_frames": pr["swap_frames"] if pr else "",
            "cooc_obs": pr["cooc_obs"] if pr else "",
            "cooc_exp": pr["cooc_exp"] if pr else "",
            "p_pos": pr["p_pos"] if pr else "",
            "p_slot": pr["p_slot"] if pr else "",
            "p_kind": pr["p_kind"] if pr else "",
            "p_site": pr["p_site"] if pr else "",
            "workshop_driver": pr["workshop_driver"] if pr else "",
            "shape_desc": data["shapes"].get(s, "")[:80],
        })
        if tier == "TIER1_PURE":
            pure_members_of_target[s] = target
        all_members_of_target[s] = target

    inherited_rows.sort(key=lambda r: (r["tier"], -r["total_intact_toks"], r["canonical_target"], r["allograph"]))

    # Coverage calculations across Lipi intact (3,600), Unseen M77 intact (627), and Combined (4,227)
    # Match Key #3A exact FV3 anchored definition: soundfree_gloss does NOT start with "Unanchored"
    fv3_anchored = {
        s for s, r in data["v3_lex"].items()
        if not r["soundfree_gloss"].startswith("Unanchored")
    } | set(LOCKED19.keys()) | set(LOAN_ANCHORS.keys()) | ALL_NUM_SIGNS | MEASURE_SIGNS
    slices = [
        ("lipi_intact_3600", data["lipi_intact_faces"]),
        ("new_intact_627", data["new_intact_faces"]),
        ("combined_intact_4227", data["lipi_intact_faces"] + data["new_intact_faces"]),
    ]

    def eval_coverage(s2c_map, label):
        out = {}
        # Expand sets via verified allograph inheritance
        def expand(base_set):
            return set(base_set) | {s for s, c in s2c_map.items() if c in base_set}

        S_11 = expand(set(LOCKED11.keys()))
        S_19 = expand(set(LOCKED19.keys()))
        S_11_lb = expand(set(LOCKED11.keys()) | set(LOAN_ANCHORS.keys()) | set(BASIC_NUMS.keys()))
        S_19_lb = expand(set(LOCKED19.keys()) | set(LOAN_ANCHORS.keys()) | set(BASIC_NUMS.keys()))
        S_19_nm = expand(set(LOCKED19.keys()) | set(LOAN_ANCHORS.keys()) | ALL_NUM_SIGNS | MEASURE_SIGNS)
        S_fv3 = expand(fv3_anchored)

        for sname, rows in slices:
            n_faces = len(rows)
            n_toks = 0
            c11 = c19 = c11lb = c19lb = c19nm = cfv3 = 0
            f11 = f19 = f11lb = f19lb = f19nm = ffv3 = 0
            for r in rows:
                toks = [t for t in r["signs"].split("-") if t]
                n_toks += len(toks)
                h11 = sum(1 for t in toks if t in S_11)
                h19 = sum(1 for t in toks if t in S_19)
                h11lb = sum(1 for t in toks if t in S_11_lb)
                h19lb = sum(1 for t in toks if t in S_19_lb)
                h19nm = sum(1 for t in toks if t in S_19_nm)
                hfv3 = sum(1 for t in toks if t in S_fv3)
                c11 += h11
                c19 += h19
                c11lb += h11lb
                c19lb += h19lb
                c19nm += h19nm
                cfv3 += hfv3
                L = len(toks)
                if L > 0:
                    if h11 == L: f11 += 1
                    if h19 == L: f19 += 1
                    if h11lb == L: f11lb += 1
                    if h19lb == L: f19lb += 1
                    if h19nm == L: f19nm += 1
                    if hfv3 == L: ffv3 += 1
            out[sname] = {
                "faces": n_faces, "tokens": n_toks,
                "tok_11": c11, "pct_11": round(100.0 * c11 / n_toks, 2),
                "tok_19": c19, "pct_19": round(100.0 * c19 / n_toks, 2),
                "tok_11_loan_bnum": c11lb, "pct_11_loan_bnum": round(100.0 * c11lb / n_toks, 2),
                "tok_19_loan_bnum": c19lb, "pct_19_loan_bnum": round(100.0 * c19lb / n_toks, 2),
                "tok_19_all_nm": c19nm, "pct_19_all_nm": round(100.0 * c19nm / n_toks, 2),
                "tok_fv3_anchored": cfv3, "pct_fv3_anchored": round(100.0 * cfv3 / n_toks, 2),
                "faces100_11": f11, "pct_f100_11": round(100.0 * f11 / n_faces, 2),
                "faces100_19": f19, "pct_f100_19": round(100.0 * f19 / n_faces, 2),
                "faces100_11_lb": f11lb, "pct_f100_11_lb": round(100.0 * f11lb / n_faces, 2),
                "faces100_19_lb": f19lb, "pct_f100_19_lb": round(100.0 * f19lb / n_faces, 2),
                "faces100_19_nm": f19nm, "pct_f100_19_nm": round(100.0 * f19nm / n_faces, 2),
                "faces100_fv3": ffv3, "pct_f100_fv3": round(100.0 * ffv3 / n_faces, 2),
            }
        return out

    cov_base = eval_coverage({}, "baseline")
    cov_pure = eval_coverage(s2c_pure, "pure")
    cov_all = eval_coverage(s2c_all, "pure_plus_workshop")

    # Find newly 100%-sound-locked faces unlocked by allograph inheritance!
    S19lb_base = set(LOCKED19.keys()) | set(LOAN_ANCHORS.keys()) | set(BASIC_NUMS.keys())
    S19lb_all = S19lb_base | {s for s, c in s2c_all.items() if c in S19lb_base}
    newly_unlocked_faces = []
    for r in data["lipi_intact_faces"] + data["new_intact_faces"]:
        toks = [t for t in r["signs"].split("-") if t]
        if len(toks) >= 2 and all(t in S19lb_all for t in toks) and not all(t in S19lb_base for t in toks):
            inh = [(t, s2c_all[t]) for t in toks if t not in S19lb_base]
            newly_unlocked_faces.append({
                "catalogue": r["catalogue"], "id": r["id"], "ref_id": r["ref_id"],
                "site": r["site"], "kind": r["object_kind"], "length": len(toks),
                "signs": r["signs"],
                "inherited_signs": "; ".join(f"{a}->{c}({ALL_SOUND_TARGETS[c][0]})" for a, c in inh),
                "gloss": " + ".join(f"{t}({ALL_SOUND_TARGETS[s2c_all.get(t,t)][0]})" for t in toks),
            })
    newly_unlocked_faces.sort(key=lambda x: (-x["length"], x["catalogue"], x["id"]))

    return {
        "inventory": {
            "raw_638": {"S_obs": inv_raw[0], "f1": inv_raw[1], "f2": inv_raw[2], "chao1": inv_raw[3], **cover_stats(raw_cnt)},
            "after_pure": {"S_obs": inv_pure[0], "f1": inv_pure[1], "f2": inv_pure[2], "chao1": inv_pure[3], **cover_stats(pure_cnt)},
            "after_pure_plus_workshop": {"S_obs": inv_all[0], "f1": inv_all[1], "f2": inv_all[2], "chao1": inv_all[3], **cover_stats(all_cnt)},
        },
        "inherited_rows": inherited_rows,
        "coverage": {
            "baseline": cov_base,
            "tier1_pure": cov_pure,
            "tier1_plus_tier2_workshop": cov_all,
        },
        "newly_unlocked_100pct_sound_faces": newly_unlocked_faces,
    }


# ==============================================================================
# 9. MAIN RUNNER & OUTPUT WRITER
# ==============================================================================
def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    t_start = time.time()
    print("[Key #4D] Loading all repository tables...", flush=True)
    data = load_all_data()
    print(
        f"  Loaded {len(data['lipi_intact_faces'])} Lipi intact + {len(data['new_intact_faces'])} unseen M77 intact "
        f"= {len(data['lipi_intact_faces']) + len(data['new_intact_faces'])} faces; "
        f"{len(data['intact_signs'])} distinct intact Lipi sign types; "
        f"{len(data['ev_lipi'])} Lipi events + {len(data['ev_new'])} New events.",
        flush=True,
    )

    print("[Key #4D] Building distributional profiles...", flush=True)
    prof = build_distributional_profiles(data["ev_lipi"])

    print("[Key #4D] Running Multi-Signal Allograph Candidate Engine...", flush=True)
    cand_rows = build_candidates_and_classify(data, prof)
    v_cnt = Counter(r["verdict"] for r in cand_rows)
    print(f"  Evaluated {len(cand_rows)} candidate pairs: {dict(v_cnt)}", flush=True)

    print("[Key #4D] Clustering (veto-constrained, zero chaining)...", flush=True)
    clusters_pure, s2c_pure, edges_pure = build_clusters(cand_rows, {"VERIFIED_PURE"}, data)
    clusters_all, s2c_all, edges_all = build_clusters(cand_rows, {"VERIFIED_PURE", "VERIFIED_WORKSHOP"}, data)

    multi_pure = {k: v for k, v in clusters_pure.items() if len(v) >= 2}
    multi_all = {k: v for k, v in clusters_all.items() if len(v) >= 2}
    print(
        f"  Tier 1 (Pure): {len(multi_pure)} clusters, 638 -> {len(clusters_pure)} (-{638 - len(clusters_pure)} types)\n"
        f"  Tier 1+2 (Pure+Workshop): {len(multi_all)} clusters, 638 -> {len(clusters_all)} (-{638 - len(clusters_all)} types)",
        flush=True,
    )

    print(f"[Key #4D] Running Held-Out Perplexity Suite ({N_RAND_MERGES} freq-matched random merges)...", flush=True)
    perp = run_perplexity_suite(data, clusters_pure, clusters_all, cand_rows)
    print(f"  Perplexity suite completed in {perp['elapsed_sec']}s.", flush=True)

    print("[Key #4D] Computing Inventory Compression & Sound Coverage Jump...", flush=True)
    cov_pkg = compute_inventory_and_coverage(data, clusters_pure, s2c_pure, clusters_all, s2c_all, cand_rows)

    # Save all CSV / JSON outputs
    write_csv(os.path.join(OUT_DIR, "all_candidates.csv"), cand_rows)

    fm_rows = [r for r in cand_rows if r["verdict"] == "FALSE_MERGER"]
    fm_rows.sort(key=lambda r: (-(1 if (r["same_P"] or r["same_M"]) else 0), -min(r["n_ev_a"], r["n_ev_b"]), r["p_slot"]))
    write_csv(os.path.join(OUT_DIR, "false_mergers.csv"), fm_rows)

    def fmt_clusters(cl_dict):
        out = []
        for canon, mlist in sorted(cl_dict.items(), key=lambda kv: (-sum(data["intact_lipi_cnt"][x] for x in kv[1]), kv[0])):
            if len(mlist) < 2:
                continue
            out.append({
                "canonical": canon,
                "n_members": len(mlist),
                "members": "|".join(mlist),
                "lipi_intact_toks": sum(data["intact_lipi_cnt"][x] for x in mlist),
                "new_intact_toks": sum(data["intact_new_cnt"][x] for x in mlist),
                "parpola_codes": "|".join(sorted({data["parpola_p"].get(x, "") for x in mlist if data["parpola_p"].get(x, "")})),
                "mah_codes": "|".join(sorted({data["mah_m"].get(x, "") for x in mlist if data["mah_m"].get(x, "")})),
                "sound_target": ALL_SOUND_TARGETS[canon][0] if canon in ALL_SOUND_TARGETS else "",
                "shape_desc": data["shapes"].get(canon, "")[:90],
            })
        return out

    write_csv(os.path.join(OUT_DIR, "verified_clusters_pure.csv"), fmt_clusters(clusters_pure))
    write_csv(os.path.join(OUT_DIR, "verified_clusters_all.csv"), fmt_clusters(clusters_all))
    write_csv(os.path.join(OUT_DIR, "sound_inheriting_allographs.csv"), cov_pkg["inherited_rows"])
    write_csv(os.path.join(OUT_DIR, "newly_unlocked_100pct_sound_faces.csv"), cov_pkg["newly_unlocked_100pct_sound_faces"])

    with open(os.path.join(OUT_DIR, "perplexity_results.json"), "w", encoding="utf-8") as f:
        json.dump({k: v for k, v in perp.items() if k != "_null_raw"}, f, indent=2)

    # Save compact coverage comparison CSV
    cov_csv_rows = []
    for scheme, sl_dict in cov_pkg["coverage"].items():
        for sname, metrics in sl_dict.items():
            cov_csv_rows.append({"scheme": scheme, "slice": sname, **metrics})
    write_csv(os.path.join(OUT_DIR, "coverage_comparison.csv"), cov_csv_rows)

    summary = {
        "runtime_sec": round(time.time() - t_start, 2),
        "candidate_verdicts": dict(v_cnt),
        "n_clusters_pure": len(multi_pure),
        "n_clusters_all": len(multi_all),
        "inventory": cov_pkg["inventory"],
        "perplexity_models": perp["models"],
        "perplexity_null_benchmarks": perp["null_benchmarks"],
        "n_sound_inheriting_pure": sum(1 for r in cov_pkg["inherited_rows"] if r["tier"] == "TIER1_PURE"),
        "n_sound_inheriting_workshop": sum(1 for r in cov_pkg["inherited_rows"] if r["tier"] == "TIER2_WORKSHOP"),
        "n_newly_unlocked_100pct_sound_faces": len(cov_pkg["newly_unlocked_100pct_sound_faces"]),
        "coverage": cov_pkg["coverage"],
    }
    with open(os.path.join(OUT_DIR, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Crisp stdout summary
    print("\n================ KEY #4D SUMMARY ================")
    inv = cov_pkg["inventory"]
    print(f"Inventory compression (638 intact): Raw={inv['raw_638']['S_obs']} (Chao1 {inv['raw_638']['chao1']}) "
          f"-> Pure={inv['after_pure']['S_obs']} (-{638 - inv['after_pure']['S_obs']}, Chao1 {inv['after_pure']['chao1']}) "
          f"-> Pure+Workshop={inv['after_pure_plus_workshop']['S_obs']} (-{638 - inv['after_pure_plus_workshop']['S_obs']}, Chao1 {inv['after_pure_plus_workshop']['chao1']})")

    bm = perp["models"]["baseline_unmerged"]
    pm = perp["models"]["verified_pure"]
    am = perp["models"]["verified_pure_plus_workshop"]
    fm = perp["models"]["false_merger_neg_control"]
    print("\n--- Held-Out Bits-per-Sign (Lower = Better) ---")
    print(f"5-Fold Lipi CV Brown-Class (uncollapsed): Base={bm['lipi_5fold_brown_bps']:.4f} | Pure={pm['lipi_5fold_brown_bps']:.4f} "
          f"| Pure+W={am['lipi_5fold_brown_bps']:.4f} | FalseMergerCtrl={fm['lipi_5fold_brown_bps']:.4f}")
    nb_all = perp["null_benchmarks"]["all"]
    nb_pure = perp["null_benchmarks"]["pure"]
    print(f"  vs 2,000 freq-matched rand (Pure+W): null={nb_all['lipi_5fold_brown_bps']['null_mean']:.4f} "
          f"z={nb_all['lipi_5fold_brown_bps']['z']:.2f} P={nb_all['lipi_5fold_brown_bps']['p_emp']:.5f}")
    print(f"  vs 2,000 freq-matched rand (Pure):   null={nb_pure['lipi_5fold_brown_bps']['null_mean']:.4f} "
          f"z={nb_pure['lipi_5fold_brown_bps']['z']:.2f} P={nb_pure['lipi_5fold_brown_bps']['p_emp']:.5f}")
    print(f"5-Fold Lipi CV Context-Only:              Base={bm['lipi_5fold_ctx_bps']:.4f} | Pure={pm['lipi_5fold_ctx_bps']:.4f} "
          f"| Pure+W={am['lipi_5fold_ctx_bps']:.4f} | RandNull={nb_all['lipi_5fold_ctx_bps']['null_mean']:.4f} "
          f"(z={nb_all['lipi_5fold_ctx_bps']['z']:.2f}, P={nb_all['lipi_5fold_ctx_bps']['p_emp']:.5f})")
    print(f"Unseen M77 New Texts Brown-Class:         Base={bm['new_brown_bps']:.4f} | Pure={pm['new_brown_bps']:.4f} "
          f"| Pure+W={am['new_brown_bps']:.4f} | FalseMergerCtrl={fm['new_brown_bps']:.4f}")
    print(f"  vs 2,000 freq-matched rand (Pure+W): null={nb_all['new_brown_bps']['null_mean']:.4f} "
          f"z={nb_all['new_brown_bps']['z']:.2f} P={nb_all['new_brown_bps']['p_emp']:.5f}")
    print(f"Unseen M77 Context-Only:                  Base={bm['new_ctx_bps']:.4f} | Pure+W={am['new_ctx_bps']:.4f} "
          f"| RandNull={nb_all['new_ctx_bps']['null_mean']:.4f} (z={nb_all['new_ctx_bps']['z']:.2f}, P={nb_all['new_ctx_bps']['p_emp']:.5f})")
    bn = perp["null_benchmarks"]["both_in_new_subset"]
    print(f"Unseen M77 Both-In-New Subset ({bn['n_clusters']} cl):   Obs={bn['new_brown_bps']['obs']:.4f} "
          f"| RandNull={bn['new_brown_bps']['null_mean']:.4f} (z={bn['new_brown_bps']['z']:.2f}, P={bn['new_brown_bps']['p_emp']:.5f})")

    print(f"\nSound-inheriting allographs: {summary['n_sound_inheriting_pure']} Tier-1 Pure + {summary['n_sound_inheriting_workshop']} Tier-2 Workshop")
    for r in cov_pkg["inherited_rows"]:
        print(f"  [{r['tier']:<14}] {r['allograph']} -> {r['canonical_target']} ({r['inherited_root']}, {r['target_group']}) "
              f"L={r['lipi_intact_toks']} N={r['new_intact_toks']} cos={r['lr_cos']} swp={r['swap_frames']} "
              f"cooc={r['cooc_obs']}/{r['cooc_exp']} p_sl={r['p_slot']} p_k={r['p_kind']} {r['workshop_driver']}")

    print("\n--- Coverage Jump (Combined 4,227 Intact Accessible Faces = 15,370 tokens) ---")
    for sch in ("baseline", "tier1_pure", "tier1_plus_tier2_workshop"):
        c = cov_pkg["coverage"][sch]["combined_intact_4227"]
        print(f"  {sch:<26}: 11SL={c['pct_11']:.2f}% | 19SL={c['pct_19']:.2f}% | 19+L+BN={c['pct_19_loan_bnum']:.2f}% "
              f"(100%-faces={c['faces100_19_lb']}/{c['faces']}={c['pct_f100_19_lb']:.2f}%) | FV3={c['pct_fv3_anchored']:.2f}% "
              f"(100%-faces={c['faces100_fv3']}/{c['faces']}={c['pct_f100_fv3']:.2f}%)")
    print(f"Done in {summary['runtime_sec']}s.")


if __name__ == "__main__":
    main()
