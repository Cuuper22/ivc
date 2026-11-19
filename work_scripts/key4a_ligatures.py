#!/usr/bin/env python3
"""key4a_ligatures.py -- Key #4 Track A (Lever 1): Diacritic, Modifier & Graphic Ligature Cracker.

Strictly rerunnable, zero-artifact pipeline executing 4 analyses:
  1. Systematic Catalog of All Diacritic, Modifier, Allograph & Graphic Ligature Families
     anchored to our 19 sound-locked signs (+ 4 trade loans + basic numerals), built directly
     from work_data/sign_shapes.csv, work_data/signlist/{mark_families.csv, merge_groups.csv},
     work_data/lipi_mahadevan_crosswalk.csv, and work_data/reader_v3/corpus_soundfree_readings.csv.
  2. Cross-Base Distributional Operator Tests (5,000 Shuffled Base-Compound Pairings):
     Tests 7 graphic operators (`cage_4corners`, `internal_vert_stroke`, `multi_stroke_inside`,
     `side_brackets`, `roof_caret_hat`, `horiz_hatching`, `doubling_graphic`) plus adjacent
     corpus doubling (`doubling_adjacent_XX`) for consistent shifts in slot position (dPos),
     finality (dFin, dF400), seal enrichment (dSeal), pre-numeral rate (dBefN), and
     prefix-vs-suffix neighbor-preservation asymmetry (cL, cR, cL - cR).
  3. Distributional Allograph Identity Tests (5,000 Random-Pair Shuffles):
     Rigorously separates true allograph variants (`705~706/704`, `154~156/158/155/153/151`,
     `390~392/405/406/407`, `861~817`, `900~904/927`, `820~821`, `061~063`, `100~101/103`,
     `176~175`, `760~752`, `803~806`, `745~746`) from semantic/grammatical modifiers using
     exact X_Y frame swaps, left/right neighbor cosines, positional delta, and Mahadevan M77 merge.
  4. Zero-Artifact Proto-Dravidian DEDR Phonetic & Compound Lock (5,000 Cluster-Preserving Shuffles):
     Reuses the exact zero-artifact DEDR parser and InMemoryLex from key2a_rebus_lock.py and
     key3a_sound_sweep.py (strict zero regex word overlap assertion) across 20 targeted unsolved
     modified/ligature signs (`240, 233, 231, 226, 255, 741, 700, 861, 840, 832, 803, 920,
     125, 892, 140, 095, 413, 503, 595, 391`), plus exact token & 100%-face coverage jump across
     all 4,227 intact accessible faces (3,600 Lipi + 627 unseen Mahadevan intact).

Outputs -> work_data/key4a/
"""

import os
import re
import sys
import csv
import json
import math
import time
import collections
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "work_scripts"))

import key2a_rebus_lock as k2
import key3a_sound_sweep as k3

OUT_DIR = os.path.join(ROOT, "work_data", "key4a")
os.makedirs(OUT_DIR, exist_ok=True)

N_SHUF = int(os.environ.get("KEY4A_NSHUF", 5000))
T0 = time.time()


def log(*args):
    print(f"[key4a {time.time() - T0:6.1f}s]", *args, flush=True)


# ==============================================================================
# 0. CONSTANTS & LOCKED BASE INVENTORY
# ==============================================================================
LOCKED11 = {
    "220": "*mīṉ (fish/star)",
    "820": "*kāl (wheel/quarter)",
    "320": "*paṭi (step/ration)",
    "090": "*āḷ (man/manager)",
    "154": "*kā (pole/guard)",
    "740": "*kuṭ- (jar/house)",
    "400": "*cikk- (comb/junior)",
    "705": "*kalam (measure/ship)",
    "520": "*vēḷ (spear/chief)",
    "850": "*kaṇ/kaṉ (eye/copper)",
    "390": "*tai (young-tree/weave)",
}

LOCKED8_BOOT = {
    "717": "*aṭi (foot/servant)",
    "061": "*kāl (leg/quarter)",
    "235": "*oḷi-mīṉ (roofed-fish/bright-star)",
    "500": "*pāy (sail)",
    "100": "*talai (3-head/chief)",
    "176": "*iru/iṟai (sit/tax)",
    "900": "*tiṅkaḷ (moon/month)",
    "923": "*maruppu (horn/tusk)",
}

LOCKED19 = {**LOCKED11, **LOCKED8_BOOT}

LOANS4 = {
    "854": "*eḷ (sesame)",
    "838": "*eḷ (sesame-seed)",
    "790": "*vaḷai (bangle/leaf)",
    "215": "*arici (rice)",
}

BASIC_NUMS = {
    "001": "*oru (1)", "031": "*oru (1)",
    "002": "*iru (2)", "032": "*iru (2)",
    "003": "*mū (3)", "033": "*mū (3)",
    "004": "*nāl (4)", "034": "*nāl (4)",
    "015": "*ai (5)", "055": "*paṉṉiru (12)",
}

ALL_NUM_SIGNS = {
    "001", "002", "003", "004", "005", "006", "007",
    "012", "013", "014", "015", "016", "017", "018", "019", "020",
    "025", "026", "027", "028", "029",
    "031", "032", "033", "034", "035", "036", "037", "055", "056",
}


# ==============================================================================
# 1. EXACT STATISTICAL & CORPUS HELPERS
# ==============================================================================
def p_and_z_two_sided(obs, null_arr, direction="greater"):
    null_arr = np.asarray(null_arr, dtype=np.float64)
    mu = float(null_arr.mean())
    sd = float(null_arr.std(ddof=1)) if len(null_arr) > 1 else 0.0
    z = 0.0 if sd < 1e-12 else (obs - mu) / sd
    if direction == "greater":
        p = float((1.0 + np.sum(null_arr >= obs - 1e-12)) / (1.0 + len(null_arr)))
    elif direction == "less":
        p = float((1.0 + np.sum(null_arr <= obs + 1e-12)) / (1.0 + len(null_arr)))
    else:
        p = float((1.0 + np.sum(np.abs(null_arr - mu) >= abs(obs - mu) - 1e-12)) / (1.0 + len(null_arr)))
    return round(mu, 4), round(sd, 4), round(z, 3), round(p, 5)


def cosine_counter(c1, c2):
    if not c1 or not c2:
        return 0.0
    keys = set(c1.keys()) & set(c2.keys())
    if not keys:
        return 0.0
    num = sum(c1[k] * c2[k] for k in keys)
    d1 = math.sqrt(sum(v * v for v in c1.values()))
    d2 = math.sqrt(sum(v * v for v in c2.values()))
    return num / (d1 * d2) if (d1 > 0 and d2 > 0) else 0.0


def load_corpus_and_metadata():
    """Load the exact 4,227 intact accessible faces (3,600 Lipi + 627 unseen M77),
    sign_shapes.csv, lipi_mahadevan_crosswalk.csv, signlist/mark_families.csv,
    signlist/merge_groups.csv, and reader_v3/soundfree_lexicon.csv."""
    with open(os.path.join(ROOT, "work_data", "reader_v3", "corpus_soundfree_readings.csv"), encoding="utf-8") as f:
        r3 = list(csv.DictReader(f))

    lipi_intact = [r for r in r3 if r["catalogue"] == "Lipi" and r["intact"] == "True"]
    new_intact = [r for r in r3 if r["catalogue"] != "Lipi" and r["partnered"] == "False" and r["intact"] == "True"]
    all_intact = lipi_intact + new_intact

    shapes = {}
    mayig = {}
    with open(os.path.join(ROOT, "work_data", "sign_shapes.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = r["lipi_wells_number"].strip()
            shapes[s] = r["shape_description"].strip()
            mayig[s] = r["mayig_code"].strip()

    crosswalk = {}
    with open(os.path.join(ROOT, "work_data", "lipi_mahadevan_crosswalk.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("rank_for_lipi_sign") == "1":
                crosswalk[r["lipi"].strip()] = (r["mahadevan"].strip(), float(r.get("share_of_lipi_sign") or 0.0))

    mark_fam = {}
    with open(os.path.join(ROOT, "work_data", "signlist", "mark_families.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            mark_fam[r["compound"].strip()] = (r["base"].strip(), r["mark_type"].strip(), r["mark"].strip())

    merge_grps = {}
    with open(os.path.join(ROOT, "work_data", "signlist", "merge_groups.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            grp = r["group"].strip()
            for m in r["members"].split("|"):
                merge_grps[m.strip()] = grp

    sf_lex = {}
    with open(os.path.join(ROOT, "work_data", "reader_v3", "soundfree_lexicon.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            sf_lex[r["sign"].strip()] = r

    log(f"Loaded corpus: Lipi intact={len(lipi_intact)}, Unseen M77 intact={len(new_intact)}, Total={len(all_intact)}")
    return lipi_intact, new_intact, all_intact, shapes, mayig, crosswalk, mark_fam, merge_grps, sf_lex


def build_sign_profiles(rows):
    """Compute complete distributional profile for every sign in `rows`."""
    stats = collections.defaultdict(lambda: {
        "n": 0, "pos_sum": 0.0, "init": 0, "med": 0, "fin": 0, "solo": 0,
        "f400": 0, "aN": 0, "bN": 0,
        "seal": 0, "tab": 0, "cop": 0, "tag": 0, "other": 0,
        "L": collections.Counter(), "R": collections.Counter(),
        "frames": collections.Counter(),
    })
    for r in rows:
        toks = [t for t in r["signs"].split("-") if t and t != "000"]
        L = len(toks)
        if L == 0:
            continue
        k = r["object_kind"].lower()
        if "seal" in k and "impr" not in k and "tag" not in k:
            kc = "seal"
        elif "copper" in k:
            kc = "cop"
        elif "tab" in k or "min" in k:
            kc = "tab"
        elif "tag" in k or "impr" in k:
            kc = "tag"
        else:
            kc = "other"

        for i, t in enumerate(toks):
            st = stats[t]
            st["n"] += 1
            st["pos_sum"] += (i / (L - 1)) if L > 1 else 0.5
            if L == 1:
                st["solo"] += 1
            elif i == 0:
                st["init"] += 1
            elif i == L - 1:
                st["fin"] += 1
            else:
                st["med"] += 1
            st[kc] += 1
            ln = toks[i - 1] if i > 0 else "^"
            rn = toks[i + 1] if i < L - 1 else "$"
            st["L"][ln] += 1
            st["R"][rn] += 1
            if ln in ALL_NUM_SIGNS:
                st["aN"] += 1
            if rn in ALL_NUM_SIGNS:
                st["bN"] += 1
            if rn in ("$", "400"):
                st["f400"] += 1
            if not (ln == "^" and rn == "$"):
                st["frames"][(ln, rn)] += 1

    profs = {}
    for s, st in stats.items():
        n = st["n"]
        profs[s] = {
            "n": n,
            "pos": st["pos_sum"] / n,
            "I": st["init"] / n,
            "M": st["med"] / n,
            "F": st["fin"] / n,
            "F400": st["f400"] / n,
            "aN": st["aN"] / n,
            "bN": st["bN"] / n,
            "seal": st["seal"] / n,
            "tab": st["tab"] / n,
            "cop": st["cop"] / n,
            "tag": st["tag"] / n,
            "L": st["L"],
            "R": st["R"],
            "frames": st["frames"],
        }
    return profs


# ==============================================================================
# 2. SYSTEMATIC DIACRITIC & LIGATURE CATALOG
# ==============================================================================
# (sign, family, base_sign, relation_type, diacritic_op, graphic_note)
CATALOG_ENTRIES = [
    # --- 1. FISH FAMILY (220 *mīṉ) ---
    ("220", "Fish (220 *mīṉ)", "220", "BASE_LOCKED", "base", "Plain fish (*mīṉ)"),
    ("235", "Fish (220 *mīṉ)", "220", "LOCKED_BOOT", "roof_caret_hat", "Fish + caret hat (*oḷi-mīṉ)"),
    ("240", "Fish (220 *mīṉ)", "220", "DIACRITIC", "whiskers_fins", "Fish + side whiskers/cheeks"),
    ("233", "Fish (220 *mīṉ)", "220", "DIACRITIC", "horiz_crossbar", "Fish + horizontal crossbar through body"),
    ("231", "Fish (220 *mīṉ)", "220", "DIACRITIC", "internal_vert_stroke", "Fish + small vertical stroke inside body"),
    ("226", "Fish (220 *mīṉ)", "220", "DIACRITIC", "cage_4corners", "Fish + 4 small vertical strokes at corners"),
    ("236", "Fish (220 *mīṉ)", "235", "DIACRITIC", "cage_4corners", "Roofed fish (235) + 4-corner cage"),
    ("241", "Fish (220 *mīṉ)", "240", "DIACRITIC", "cage_4corners", "Whiskered fish (240) + 4-corner cage"),
    ("232", "Fish (220 *mīṉ)", "231", "DIACRITIC", "cage_4corners", "Vert-stroke fish (231) + 4-corner cage"),
    ("234", "Fish (220 *mīṉ)", "233", "DIACRITIC", "cage_4corners", "Barred fish (233) + 4-corner cage"),
    ("222", "Fish (220 *mīṉ)", "220", "DIACRITIC", "side_brackets", "Fish inside parentheses"),
    ("243", "Fish (220 *mīṉ)", "220", "DIACRITIC", "roof_caret_hat", "Hatched fish + caret hat"),
    ("242", "Fish (220 *mīṉ)", "220", "ALLOGRAPH_CAND", "whiskers_fins", "Fish + cheek whiskers (variant of 240)"),
    ("244", "Fish (220 *mīṉ)", "220", "LIGATURE", "joined_object", "Fish + bird wings and 3-feather tail"),
    ("227", "Fish (220 *mīṉ)", "220", "DIACRITIC", "other", "Fish + extra legs"),
    ("228", "Fish (220 *mīṉ)", "220", "DIACRITIC", "other", "Fish + extra legs"),
    ("255", "Fish/Gharial (255)", "220", "DISTINCT_ANIMAL", "other", "Asymmetric aquatic animal / gharial (M51)"),
    ("256", "Fish/Gharial (255)", "255", "LIGATURE", "joined_object", "255 + tall vertical stroke on left"),
    ("940", "Fish (220 *mīṉ)", "220", "LIGATURE", "side_brackets", "Fish + bird inside parentheses"),
    ("942", "Fish (220 *mīṉ)", "220", "LIGATURE", "side_brackets", "Bird + fish inside parentheses"),
    ("944", "Fish (220 *mīṉ)", "220", "LIGATURE", "cage_4corners", "Fish + table-box + 4-corner cage"),

    # --- 2. JAR FAMILY (740 *kuṭi) ---
    ("740", "Jar (740 *kuṭi)", "740", "BASE_LOCKED", "base", "Classic handled jar (*kuṭi/*kuṭam)"),
    ("741", "Jar (740 *kuṭi)", "740", "DIACRITIC", "internal_vert_stroke", "Jar + 1 vertical stroke inside mouth"),
    ("742", "Jar (740 *kuṭi)", "740", "DIACRITIC", "multi_stroke_inside", "Jar + 2 vertical strokes inside mouth"),
    ("743", "Jar (740 *kuṭi)", "740", "DIACRITIC", "multi_stroke_inside", "Jar + 2 vertical strokes inside mouth (var)"),
    ("744", "Jar (740 *kuṭi)", "740", "DIACRITIC", "multi_stroke_inside", "Jar + 2 vertical strokes inside mouth (var)"),
    ("745", "Jar (740 *kuṭi)", "740", "DIACRITIC", "multi_stroke_inside", "Jar + 3 vertical strokes inside mouth"),
    ("746", "Jar (740 *kuṭi)", "740", "ALLOGRAPH_CAND", "multi_stroke_inside", "Jar + 3 vertical strokes inside mouth (M345=745)"),
    ("747", "Jar (740 *kuṭi)", "740", "DIACRITIC", "multi_stroke_inside", "Jar + 3 vertical strokes inside mouth (var)"),
    ("748", "Jar (740 *kuṭi)", "740", "DIACRITIC", "multi_stroke_inside", "Jar + 4 vertical strokes inside mouth"),
    ("749", "Jar (740 *kuṭi)", "745", "DIACRITIC", "roof_caret_hat", "Jar + 3 strokes + caret overlay"),
    ("751", "Jar (740 *kuṭi)", "740", "LIGATURE", "joined_object", "Jar + wagon wheel (820) + double pitchfork inside"),

    # --- 3. CUP / VESSEL FAMILY (700 / 705 *kalam) ---
    ("700", "Cup/Vessel (700/705)", "700", "BASE_UNSOLVED", "base", "Simple U cup (~9.24 L)"),
    ("705", "Cup/Vessel (700/705)", "700", "BASE_LOCKED", "internal_vert_stroke", "U + long vertical stroke (*kalam, M336)"),
    ("706", "Cup/Vessel (700/705)", "705", "ALLOGRAPH_CAND", "internal_vert_stroke", "U + long vertical stroke (M336 = 705)"),
    ("704", "Cup/Vessel (700/705)", "705", "ALLOGRAPH_CAND", "internal_vert_stroke", "U + long vertical stroke (M336 = 705)"),
    ("707", "Cup/Vessel (700/705)", "705", "ALLOGRAPH_CAND", "internal_vert_stroke", "U + long vertical stroke (var)"),
    ("701", "Cup/Vessel (700/705)", "700", "DIACRITIC", "multi_stroke_inside", "U + 2 small vertical strokes inside top"),
    ("703", "Cup/Vessel (700/705)", "700", "DIACRITIC", "multi_stroke_inside", "U + 3 small vertical strokes inside top"),
    ("710", "Cup/Vessel (700/705)", "700", "LIGATURE", "joined_object", "U + tree motif (390) at bottom"),
    ("711", "Cup/Vessel (700/705)", "700", "LIGATURE", "joined_object", "U + X near bottom"),
    ("712", "Cup/Vessel (700/705)", "700", "LIGATURE", "joined_object", "U + wagon wheel (820) near bottom"),
    ("752", "Cup/Vessel (700/705)", "700", "LIGATURE", "joined_object", "U + decorated branching at top (M358)"),
    ("760", "Cup/Vessel (700/705)", "700", "LIGATURE", "joined_object", "U + decorated branching at top (M347)"),
    ("753", "Cup/Vessel (700/705)", "700", "LIGATURE", "joined_object", "U + tree handles + wagon wheel (820) inside"),

    # --- 4. TREE / COMB FAMILY (390 *tai / 400 *cikk-) ---
    ("390", "Tree/Comb (390/400)", "390", "BASE_LOCKED", "base", "Simple tree with branches at top (*tai, M162)"),
    ("392", "Tree/Comb (390/400)", "390", "ALLOGRAPH_CAND", "allograph", "Simple tree with branches at top (M162 = 390)"),
    ("405", "Tree/Comb (390/400)", "390", "ALLOGRAPH_CAND", "allograph", "Simple tree with branches at top (M169)"),
    ("407", "Tree/Comb (390/400)", "390", "ALLOGRAPH_CAND", "allograph", "Simple tree with branches at top (M169 = 405)"),
    ("406", "Tree/Comb (390/400)", "390", "ALLOGRAPH_CAND", "allograph", "Simple tree with branches at top (M169 = 405)"),
    ("408", "Tree/Comb (390/400)", "390", "DIACRITIC", "other", "Simple tree variant (M141)"),
    ("391", "Tree/Comb (390/400)", "390", "DIACRITIC", "roof_caret_hat", "3-pronged tree + caret hat (M163)"),
    ("393", "Tree/Comb (390/400)", "390", "DIACRITIC", "cage_4corners", "Simple tree + 4-corner cage"),
    ("394", "Tree/Comb (390/400)", "390", "LIGATURE", "joined_object", "Simple tree + pitchfork head"),
    ("400", "Tree/Comb (390/400)", "400", "BASE_LOCKED", "base", "One-sided comb (*cikk-, M176)"),
    ("402", "Tree/Comb (390/400)", "400", "ALLOGRAPH_CAND", "allograph", "One-sided comb variant (P098 = 400)"),
    ("413", "Tree/Comb (390/400)", "400", "DISTINCT_DOUBLE", "doubling_graphic", "Double-sided comb / cereal-stalk (M177)"),

    # --- 5. PORTER / MAN FAMILY (090 *āḷ / 154 *kā / 100 *talai) ---
    ("090", "Porter/Man (090/154/100)", "090", "BASE_LOCKED", "base", "Plain person (*āḷ, M1)"),
    ("091", "Porter/Man (090/154/100)", "090", "DIACRITIC", "doubling_graphic", "Two simple persons side by side (090+090)"),
    ("093", "Porter/Man (090/154/100)", "090", "DIACRITIC", "internal_vert_stroke", "Person + small vertical stroke between legs (M3)"),
    ("095", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person + short stick (M18)"),
    ("097", "Porter/Man (090/154/100)", "090", "DIACRITIC", "side_brackets", "Person bracketed by tall vertical lines (M2)"),
    ("098", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person + extra raised arm"),
    ("100", "Porter/Man (090/154/100)", "090", "LOCKED_BOOT", "joined_object", "Person with 3 heads (*talai, M8)"),
    ("101", "Porter/Man (090/154/100)", "100", "DIACRITIC", "side_brackets", "3-headed person (100) + right-paren brackets (M9)"),
    ("103", "Porter/Man (090/154/100)", "100", "DIACRITIC", "side_brackets", "3-headed person (100) + right-paren brackets (M9=101)"),
    ("104", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person + half-height caret at foot"),
    ("110", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person + U (700)"),
    ("111", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person + U (700)"),
    ("118", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person standing on 2 wagon wheels (090+820)"),
    ("125", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person + bow & arrow (090+892, M28)"),
    ("127", "Porter/Man (090/154/100)", "125", "DIACRITIC", "doubling_graphic", "Person + 2 bows & arrows"),
    ("130", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person + pitchfork (090+415)"),
    ("137", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person + leaf on thigh"),
    ("140", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Woman with round breasts & raised arm (M17)"),
    ("142", "Porter/Man (090/154/100)", "090", "LIGATURE", "joined_object", "Person + staff (M25)"),
    ("143", "Porter/Man (090/154/100)", "142", "DIACRITIC", "doubling_graphic", "Person + 2 staves"),
    ("144", "Porter/Man (090/154/100)", "142", "DIACRITIC", "cage_4corners", "Person + staff + 4-corner cage"),
    ("154", "Porter/Man (090/154/100)", "154", "BASE_LOCKED", "base", "Person carrying 2 burdens, jar handles (*kā, M15)"),
    ("156", "Porter/Man (090/154/100)", "154", "ALLOGRAPH_CAND", "allograph", "Person carrying 2 burdens, jar handles (M15 = 154)"),
    ("158", "Porter/Man (090/154/100)", "154", "ALLOGRAPH_CAND", "allograph", "Person carrying 2 burdens, jar handles (M15 = 154)"),
    ("155", "Porter/Man (090/154/100)", "154", "ALLOGRAPH_CAND", "allograph", "Person carrying 2 burdens, jar handles (M15 = 154)"),
    ("153", "Porter/Man (090/154/100)", "154", "ALLOGRAPH_CAND", "allograph", "Person carrying 2 burdens, jar handles (M15 = 154)"),
    ("151", "Porter/Man (090/154/100)", "154", "ALLOGRAPH_CAND", "base_plain", "Plain person carrying 2 burdens (M12, base of 154)"),
    ("159", "Porter/Man (090/154/100)", "154", "LIGATURE", "joined_object", "Porter carrying 2 burdens + diamond head (M14)"),
    ("161", "Porter/Man (090/154/100)", "154", "LIGATURE", "joined_object", "Porter carrying 2 burdens + diamond head (M14 = 159)"),

    # --- 6. DIAMOND / LEAF / FIELD FAMILY (850 *kaṇ/kaṉ, 790 *vaḷai) ---
    ("850", "Diamond/Leaf (850/790)", "850", "BASE_LOCKED", "base", "Simple diamond/eye (*kaṇ/kaṉ, M261)"),
    ("861", "Diamond/Leaf (850/790)", "850", "DIACRITIC", "doubling_graphic", "Diamond + small diamond attached at top (M267)"),
    ("817", "Diamond/Leaf (850/790)", "861", "ALLOGRAPH_CAND", "allograph", "Diamond + small diamond attached at top (M267 = 861)"),
    ("868", "Diamond/Leaf (850/790)", "861", "DIACRITIC", "other", "861 + doubled lower-left interior edge"),
    ("877", "Diamond/Leaf (850/790)", "850", "DIACRITIC", "other", "Diamond + 4 small diamonds at vertices"),
    ("878", "Diamond/Leaf (850/790)", "877", "DIACRITIC", "cage_4corners", "877 + 4-corner cage"),
    ("880", "Diamond/Leaf (850/790)", "877", "LIGATURE", "joined_object", "877 + wagon wheel (820) in center"),
    ("790", "Diamond/Leaf (850/790)", "790", "BASE_LOAN", "base", "Simple leaf/diamond (*vaḷai, M373)"),
    ("832", "Diamond/Leaf (850/790)", "790", "DIACRITIC", "internal_vert_stroke", "Leaf + small vertical stroke inside (M375)"),
    ("840", "Diamond/Leaf (850/790)", "790", "DIACRITIC", "doubling_graphic", "Two overlapping vertical leaves (M403)"),
    ("845", "Diamond/Leaf (850/790)", "840", "DIACRITIC", "horiz_hatching", "Two overlapping leaves + diagonal hatches (M407)"),
    ("803", "Diamond/Leaf (850/790)", "790", "LIGATURE", "joined_object", "Leaf + tree (390) at bottom (M387)"),
    ("806", "Diamond/Leaf (850/790)", "790", "LIGATURE", "joined_object", "Leaf + tree (390) at bottom (M389)"),
    ("804", "Diamond/Leaf (850/790)", "803", "DIACRITIC", "cage_4corners", "803 + 4-corner cage (M388)"),
    ("807", "Diamond/Leaf (850/790)", "806", "DIACRITIC", "cage_4corners", "806 + 4-corner cage"),
    ("798", "Diamond/Leaf (850/790)", "790", "LIGATURE", "joined_object", "Leaf + pincers on right (M53)"),
    ("808", "Diamond/Leaf (850/790)", "790", "DIACRITIC", "other", "Leaf + small dot inside"),
    ("812", "Diamond/Leaf (850/790)", "790", "DIACRITIC", "horiz_hatching", "Leaf + hatched square inside"),
    ("825", "Diamond/Leaf (850/790)", "790", "DIACRITIC", "horiz_hatching", "Leaf + cross-hatching throughout"),

    # --- 7. OTHER LOCKED FAMILIES (900, 923, 820, 061, 176, 500, 520, 320, 590, 892, Nums) ---
    ("900", "Moon/Crescent (900/923)", "900", "LOCKED_BOOT", "base", "Right parenthesis / moon (*tiṅkaḷ, M287)"),
    ("904", "Moon/Crescent (900/923)", "900", "DIACRITIC", "doubling_graphic", "Two nested right parens (2× 900, M294)"),
    ("927", "Moon/Crescent (900/923)", "904", "ALLOGRAPH_CAND", "doubling_graphic", "Two nested right parens (M294 = 904)"),
    ("905", "Moon/Crescent (900/923)", "904", "DIACRITIC", "other", "904 + outward tooth at top (M295)"),
    ("920", "Moon/Crescent (900/923)", "900", "LIGATURE", "joined_object", "Right paren (900) + small leaf at middle (M293)"),
    ("922", "Moon/Crescent (900/923)", "920", "DIACRITIC", "other", "920 + crossing stroke at top"),
    ("923", "Moon/Crescent (900/923)", "923", "LOCKED_BOOT", "base", "Outline crescent/tusk (*maruppu, M296)"),
    ("924", "Moon/Crescent (900/923)", "923", "DIACRITIC", "horiz_hatching", "Outline crescent + horizontal hatching (M297)"),
    ("820", "Wheel/Leg (820/061)", "820", "BASE_LOCKED", "base", "6-spoke wheel (*kāl, M391)"),
    ("821", "Wheel/Leg (820/061)", "820", "ALLOGRAPH_CAND", "doubling_graphic", "Wheel variant (M391 = 820)"),
    ("061", "Wheel/Leg (820/061)", "061", "LOCKED_BOOT", "base", "Reversed lambda / leg (*kāl, M124)"),
    ("063", "Wheel/Leg (820/061)", "061", "ALLOGRAPH_CAND", "allograph", "Reversed lambda / leg variant (M125)"),
    ("176", "Seated (176 *iru/iṟai)", "176", "LOCKED_BOOT", "base", "Seated person + 4 back-strokes (*iru/iṟai, M48)"),
    ("175", "Seated (176 *iru/iṟai)", "176", "ALLOGRAPH_CAND", "base_plain", "Plain seated person, no back-strokes (M205)"),
    ("500", "Sail/Triangle (500 *pāy)", "500", "LOCKED_BOOT", "internal_vert_stroke", "Tall triangle + vertical divider (*pāy, M209)"),
    ("502", "Sail/Triangle (500 *pāy)", "500", "DIACRITIC", "horiz_hatching", "500 + horizontal hatching (M210)"),
    ("503", "Sail/Triangle (500 *pāy)", "490", "DIACRITIC", "horiz_hatching", "Tall triangle + horizontal stripes (M204)"),
    ("504", "Sail/Triangle (500 *pāy)", "503", "LIGATURE", "joined_object", "503 + serifed T on top (M206)"),
    ("520", "Spear (520 *vēḷ)", "520", "BASE_LOCKED", "base", "Triangle on vertical line (*vēḷ, M211)"),
    ("521", "Spear (520 *vēḷ)", "520", "LIGATURE", "joined_object", "Pitchfork + triangular spear tine in middle (M212)"),
    ("320", "Stair/Ladder (320 *paṭi)", "320", "BASE_LOCKED", "base", "Step/ladder ration unit (*paṭi)"),
    ("321", "Stair/Ladder (320 *paṭi)", "322", "LIGATURE", "joined_object", "Double-bar H + diagonal to tall stroke (M183)"),
    ("323", "Stair/Ladder (320 *paṭi)", "322", "ALLOGRAPH_CAND", "allograph", "Double-bar H variant (M182)"),
    ("590", "Chest/Forge (590)", "590", "BASE_UNSOLVED", "base", "Square + vertical bar at top (M249)"),
    ("592", "Chest/Forge (590)", "590", "DIACRITIC", "cage_4corners", "590 + 4-corner cage"),
    ("595", "Chest/Forge (590)", "590", "DIACRITIC", "horiz_hatching", "590 + horizontal striping (citadel forge)"),
    ("892", "Bow/Trade (892/125)", "892", "BASE_UNSOLVED", "base", "Standalone bow & arrow (component of 125, M307)"),
    ("895", "Bow/Trade (892/125)", "892", "DIACRITIC", "cage_4corners", "Bow & arrow + 4-corner cage"),
    ("048", "Numeral Compounds", "007", "DIACRITIC", "side_brackets", "7 short strokes bracketed by parens"),
    ("049", "Numeral Compounds", "007", "DIACRITIC", "side_brackets", "7 short strokes bracketed by parens (var)"),
    ("044", "Numeral Compounds", "033", "DIACRITIC", "roof_caret_hat", "3 tall strokes + caret hat"),
    ("045", "Numeral Compounds", "033", "LIGATURE", "joined_object", "3 tall strokes + small tree (390)"),
    ("046", "Numeral Compounds", "033", "LIGATURE", "joined_object", "3 tall strokes + small tree (390)"),
    ("057", "Numeral Compounds", "055", "DIACRITIC", "side_brackets", "Dozen (055) + right-paren brackets"),
    ("217", "Loan Compounds", "215", "DIACRITIC", "side_brackets", "Rice (215) + 2 tall vertical cage strokes"),
    ("617", "Field-Grid (615)", "615", "DIACRITIC", "doubling_graphic", "Twin field-grid (2× 615)"),
]


def build_catalog(lipi_intact, new_intact, profs, shapes, mayig, crosswalk, mark_fam, merge_grps, sf_lex):
    c_l = collections.Counter()
    c_n = collections.Counter()
    for r in lipi_intact:
        c_l.update(t for t in r["signs"].split("-") if t and t != "000")
    for r in new_intact:
        c_n.update(t for t in r["signs"].split("-") if t and t != "000")

    rows = []
    for s, fam, base, rel, op, gnote in CATALOG_ENTRIES:
        p = profs.get(s)
        pb = profs.get(base)
        m77, mshare = crosswalk.get(s, ("", 0.0))
        sf = sf_lex.get(s, {})
        cL = round(cosine_counter(pb["L"], p["L"]), 3) if (p and pb) else ""
        cR = round(cosine_counter(pb["R"], p["R"]), 3) if (p and pb) else ""
        rows.append({
            "sign": s,
            "family": fam,
            "base_sign": base,
            "relation_type": rel,
            "diacritic_operator": op,
            "lipi_intact": c_l[s],
            "new_intact": c_n[s],
            "total_intact": c_l[s] + c_n[s],
            "m77_code": m77,
            "m77_share": round(mshare, 3),
            "mayig_code": mayig.get(s, ""),
            "merge_group": merge_grps.get(s, ""),
            "mark_fam_base": mark_fam[s][0] if s in mark_fam else "",
            "mark_fam_type": mark_fam[s][1] if s in mark_fam else "",
            "mean_pos": round(p["pos"], 3) if p else "",
            "init_rate": round(p["I"], 3) if p else "",
            "med_rate": round(p["M"], 3) if p else "",
            "fin_rate": round(p["F"], 3) if p else "",
            "f400_rate": round(p["F400"], 3) if p else "",
            "seal_rate": round(p["seal"], 3) if p else "",
            "bef_num_rate": round(p["bN"], 3) if p else "",
            "cos_L_base": cL,
            "cos_R_base": cR,
            "v3_class": sf.get("v3_class", ""),
            "soundfree_gloss": sf.get("soundfree_gloss", ""),
            "shape_desc": shapes.get(s, ""),
            "graphic_note": gnote,
        })

    out_csv = os.path.join(OUT_DIR, "key4a_catalog.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    log(f"Wrote {len(rows)} catalog entries -> {out_csv}")
    return rows


# ==============================================================================
# 3. CROSS-BASE DISTRIBUTIONAL OPERATOR TESTS (5,000 SHUFFLES)
# ==============================================================================
OPERATOR_PAIRS = {
    "cage_4corners": [
        ("220", "226"), ("231", "232"), ("233", "234"), ("235", "236"),
        ("240", "241"), ("590", "592"), ("803", "804"), ("142", "144"),
    ],
    "internal_vert_stroke": [
        ("740", "741"), ("700", "705"), ("700", "706"), ("220", "231"),
        ("790", "832"), ("090", "093"), ("440", "443"), ("550", "556"),
    ],
    "multi_stroke_inside": [
        ("740", "741"), ("740", "742"), ("740", "745"), ("740", "746"),
        ("700", "705"), ("700", "706"), ("700", "703"),
        ("220", "231"), ("790", "832"), ("090", "093"),
    ],
    "side_brackets": [
        ("007", "048"), ("007", "049"), ("090", "097"),
        ("100", "101"), ("100", "103"), ("220", "222"),
    ],
    "roof_caret_hat": [
        ("220", "235"), ("220", "243"), ("390", "391"), ("455", "456"),
    ],
    "horiz_hatching": [
        ("923", "924"), ("500", "502"), ("590", "595"), ("600", "603"),
        ("840", "845"), ("480", "484"), ("382", "388"), ("790", "812"), ("790", "825"),
    ],
    "doubling_graphic": [
        ("090", "091"), ("790", "840"), ("900", "904"), ("900", "927"),
        ("615", "617"), ("850", "861"), ("850", "817"), ("415", "416"),
        ("415", "417"), ("400", "413"), ("820", "821"), ("125", "127"), ("142", "143"),
    ],
}


def run_operator_tests(all_intact, profs):
    log("=== RUNNING CROSS-BASE DISTRIBUTIONAL OPERATOR TESTS (5,000 SHUFFLES) ===")
    rng = np.random.default_rng(42)

    # Eligible sign pool (n >= 3 in intact corpus) for null base-compound pairings
    pool = sorted([s for s, p in profs.items() if p["n"] >= 3])
    pool_idx = {s: i for i, s in enumerate(pool)}
    P = len(pool)

    # Precompute metric vectors and full cosine matrices on pool for instant 5,000 shuffles
    vec_pos = np.array([profs[s]["pos"] for s in pool])
    vec_fin = np.array([profs[s]["F"] for s in pool])
    vec_f400 = np.array([profs[s]["F400"] for s in pool])
    vec_seal = np.array([profs[s]["seal"] for s in pool])
    vec_bN = np.array([profs[s]["bN"] for s in pool])

    # Precompute cosine matrices for bases & compounds appearing in OPERATOR_PAIRS
    all_op_signs = sorted({x for pairs in OPERATOR_PAIRS.values() for pair in pairs for x in pair if x in pool_idx})
    cosL_map = {}
    cosR_map = {}
    for s in all_op_signs:
        ps = profs[s]
        cL_arr = np.array([cosine_counter(ps["L"], profs[t]["L"]) for t in pool])
        cR_arr = np.array([cosine_counter(ps["R"], profs[t]["R"]) for t in pool])
        cosL_map[s] = cL_arr
        cosR_map[s] = cR_arr

    pair_rows = []
    op_summary = {}

    for op_name, pairs in OPERATOR_PAIRS.items():
        valid = [(b, c) for b, c in pairs if b in pool_idx and c in pool_idx]
        k = len(valid)
        b_idxs = np.array([pool_idx[b] for b, _ in valid])
        c_idxs = np.array([pool_idx[c] for _, c in valid])

        obs_dpos = float(np.mean(vec_pos[c_idxs] - vec_pos[b_idxs]))
        obs_dfin = float(np.mean(vec_fin[c_idxs] - vec_fin[b_idxs]))
        obs_df400 = float(np.mean(vec_f400[c_idxs] - vec_f400[b_idxs]))
        obs_dseal = float(np.mean(vec_seal[c_idxs] - vec_seal[b_idxs]))
        obs_dbN = float(np.mean(vec_bN[c_idxs] - vec_bN[b_idxs]))

        cL_vals = np.array([cosL_map[b][pool_idx[c]] for b, c in valid])
        cR_vals = np.array([cosR_map[b][pool_idx[c]] for b, c in valid])
        obs_cL = float(np.mean(cL_vals))
        obs_cR = float(np.mean(cR_vals))
        obs_asym = float(np.mean(cL_vals - cR_vals))

        # 5,000 exact shuffles: keep the exact base signs fixed and pair each with a random
        # distinct sign from the corpus pool (controls for base distribution!)
        null_dpos = np.empty(N_SHUF)
        null_dfin = np.empty(N_SHUF)
        null_df400 = np.empty(N_SHUF)
        null_dseal = np.empty(N_SHUF)
        null_dbN = np.empty(N_SHUF)
        null_cL = np.empty(N_SHUF)
        null_cR = np.empty(N_SHUF)
        null_asym = np.empty(N_SHUF)

        for it in range(N_SHUF):
            rand_c = rng.integers(0, P, size=k)
            # avoid self-match
            same = (rand_c == b_idxs)
            while np.any(same):
                rand_c[same] = rng.integers(0, P, size=int(np.sum(same)))
                same = (rand_c == b_idxs)
            null_dpos[it] = np.mean(vec_pos[rand_c] - vec_pos[b_idxs])
            null_dfin[it] = np.mean(vec_fin[rand_c] - vec_fin[b_idxs])
            null_df400[it] = np.mean(vec_f400[rand_c] - vec_f400[b_idxs])
            null_dseal[it] = np.mean(vec_seal[rand_c] - vec_seal[b_idxs])
            null_dbN[it] = np.mean(vec_bN[rand_c] - vec_bN[b_idxs])
            rcL = np.array([cosL_map[valid[j][0]][rand_c[j]] for j in range(k)])
            rcR = np.array([cosR_map[valid[j][0]][rand_c[j]] for j in range(k)])
            null_cL[it] = np.mean(rcL)
            null_cR[it] = np.mean(rcR)
            null_asym[it] = np.mean(rcL - rcR)

        # Also test WITHIN-SET permutation (shuffling the real compounds among the real bases) for cL/cR
        # Directional sign-agreement counts
        n_pos_dpos = int(np.sum((vec_pos[c_idxs] - vec_pos[b_idxs]) > 0))
        n_neg_dpos = int(np.sum((vec_pos[c_idxs] - vec_pos[b_idxs]) < 0))
        n_pos_f400 = int(np.sum((vec_f400[c_idxs] - vec_f400[b_idxs]) > 0))
        n_neg_f400 = int(np.sum((vec_f400[c_idxs] - vec_f400[b_idxs]) < 0))
        n_pos_seal = int(np.sum((vec_seal[c_idxs] - vec_seal[b_idxs]) > 0))

        # Pick two-sided p for shifts and directional p for cL/cR
        res = {
            "k_pairs": k,
            "n_shuf": N_SHUF,
            "dPos": {"obs": round(obs_dpos, 4), "pos_cnt": n_pos_dpos, "neg_cnt": n_neg_dpos,
                     **dict(zip(["null_mu", "null_sd", "z", "p_two"], p_and_z_two_sided(obs_dpos, null_dpos, "two")))},
            "dFin": {"obs": round(obs_dfin, 4),
                     **dict(zip(["null_mu", "null_sd", "z", "p_two"], p_and_z_two_sided(obs_dfin, null_dfin, "two")))},
            "dF400": {"obs": round(obs_df400, 4), "pos_cnt": n_pos_f400, "neg_cnt": n_neg_f400,
                      **dict(zip(["null_mu", "null_sd", "z", "p_two"], p_and_z_two_sided(obs_df400, null_df400, "two")))},
            "dSeal": {"obs": round(obs_dseal, 4), "pos_cnt": n_pos_seal,
                      **dict(zip(["null_mu", "null_sd", "z", "p_two"], p_and_z_two_sided(obs_dseal, null_dseal, "two")))},
            "dBefN": {"obs": round(obs_dbN, 4),
                      **dict(zip(["null_mu", "null_sd", "z", "p_two"], p_and_z_two_sided(obs_dbN, null_dbN, "two")))},
            "cosL": {"obs": round(obs_cL, 4),
                     **dict(zip(["null_mu", "null_sd", "z", "p_gt"], p_and_z_two_sided(obs_cL, null_cL, "greater")))},
            "cosR": {"obs": round(obs_cR, 4),
                     **dict(zip(["null_mu", "null_sd", "z", "p_gt"], p_and_z_two_sided(obs_cR, null_cR, "greater")))},
            "asym_cL_minus_cR": {"obs": round(obs_asym, 4),
                                 **dict(zip(["null_mu", "null_sd", "z", "p_two"], p_and_z_two_sided(obs_asym, null_asym, "two")))},
        }
        op_summary[op_name] = res

        log(f"  OP {op_name:22s} (k={k:2d}): "
            f"dPos={obs_dpos:+.3f}(P={res['dPos']['p_two']:.4f}) "
            f"dF400={obs_df400:+.3f}(P={res['dF400']['p_two']:.4f}) "
            f"dSeal={obs_dseal:+.3f}(P={res['dSeal']['p_two']:.4f}) "
            f"cL={obs_cL:.3f}(P={res['cosL']['p_gt']:.4f}) "
            f"cR={obs_cR:.3f}(P={res['cosR']['p_gt']:.4f}) "
            f"cL-cR={obs_asym:+.3f}(P={res['asym_cL_minus_cR']['p_two']:.4f})")

        for j, (b, c) in enumerate(valid):
            pb, pc = profs[b], profs[c]
            pair_rows.append({
                "operator": op_name, "base": b, "compound": c,
                "n_base": pb["n"], "n_comp": pc["n"],
                "pos_base": round(pb["pos"], 3), "pos_comp": round(pc["pos"], 3),
                "dPos": round(pc["pos"] - pb["pos"], 3),
                "fin_base": round(pb["F"], 3), "fin_comp": round(pc["F"], 3),
                "dFin": round(pc["F"] - pb["F"], 3),
                "f400_base": round(pb["F400"], 3), "f400_comp": round(pc["F400"], 3),
                "dF400": round(pc["F400"] - pb["F400"], 3),
                "seal_base": round(pb["seal"], 3), "seal_comp": round(pc["seal"], 3),
                "dSeal": round(pc["seal"] - pb["seal"], 3),
                "bN_base": round(pb["bN"], 3), "bN_comp": round(pc["bN"], 3),
                "dBefN": round(pc["bN"] - pb["bN"], 3),
                "cosL": round(float(cL_vals[j]), 3),
                "cosR": round(float(cR_vals[j]), 3),
                "cL_minus_cR": round(float(cL_vals[j] - cR_vals[j]), 3),
            })

    # Also evaluate ADJACENT BIGRAM DOUBLING X-X vs single X (for recurring X-X, n >= 4)
    xx_stats = collections.defaultdict(lambda: {"n": 0, "pos_sum": 0.0, "fin": 0, "f400": 0, "seal": 0, "L": collections.Counter(), "R": collections.Counter()})
    for r in all_intact:
        toks = [t for t in r["signs"].split("-") if t and t != "000"]
        L = len(toks)
        k_str = r["object_kind"].lower()
        is_seal = ("seal" in k_str and "impr" not in k_str and "tag" not in k_str)
        i = 0
        while i < L - 1:
            if toks[i] == toks[i + 1]:
                s = toks[i]
                st = xx_stats[s]
                st["n"] += 1
                st["pos_sum"] += (i / (L - 2)) if L > 2 else 0.5
                if i + 2 == L:
                    st["fin"] += 1
                rn = toks[i + 2] if i + 2 < L else "$"
                ln = toks[i - 1] if i > 0 else "^"
                if rn in ("$", "400"):
                    st["f400"] += 1
                if is_seal:
                    st["seal"] += 1
                st["L"][ln] += 1
                st["R"][rn] += 1
                i += 2
            else:
                i += 1

    xx_rows = []
    for s, st in sorted(xx_stats.items(), key=lambda kv: -kv[1]["n"]):
        if st["n"] >= 4 and s in profs:
            pb = profs[s]
            n = st["n"]
            xx_rows.append({
                "sign": s, "n_XX": n, "n_single": pb["n"],
                "pos_single": round(pb["pos"], 3), "pos_XX": round(st["pos_sum"] / n, 3),
                "dPos": round(st["pos_sum"] / n - pb["pos"], 3),
                "f400_single": round(pb["F400"], 3), "f400_XX": round(st["f400"] / n, 3),
                "dF400": round(st["f400"] / n - pb["F400"], 3),
                "seal_single": round(pb["seal"], 3), "seal_XX": round(st["seal"] / n, 3),
                "dSeal": round(st["seal"] / n - pb["seal"], 3),
                "cosL": round(cosine_counter(pb["L"], st["L"]), 3),
                "cosR": round(cosine_counter(pb["R"], st["R"]), 3),
            })
    op_summary["doubling_adjacent_XX"] = {
        "k_signs": len(xx_rows),
        "mean_dPos": round(float(np.mean([r["dPos"] for r in xx_rows])), 4) if xx_rows else 0.0,
        "mean_dF400": round(float(np.mean([r["dF400"] for r in xx_rows])), 4) if xx_rows else 0.0,
        "mean_dSeal": round(float(np.mean([r["dSeal"] for r in xx_rows])), 4) if xx_rows else 0.0,
        "mean_cosL": round(float(np.mean([r["cosL"] for r in xx_rows])), 4) if xx_rows else 0.0,
        "mean_cosR": round(float(np.mean([r["cosR"] for r in xx_rows])), 4) if xx_rows else 0.0,
        "rows": xx_rows,
    }

    with open(os.path.join(OUT_DIR, "key4a_operator_tests.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(pair_rows[0].keys()))
        w.writeheader()
        w.writerows(pair_rows)
    with open(os.path.join(OUT_DIR, "key4a_operator_summary.json"), "w", encoding="utf-8") as f:
        json.dump(op_summary, f, indent=2)
    return op_summary, pair_rows


# ==============================================================================
# 4. ALLOGRAPH IDENTITY TESTS (5,000 SHUFFLES)
# ==============================================================================
ALLOGRAPH_PAIRS = [
    ("705", "706", "705 *kalam (M336) vs 706 (M336)"),
    ("705", "704", "705 *kalam (M336) vs 704 (M336)"),
    ("154", "158", "154 *kā (M15) vs 158 (M15)"),
    ("154", "156", "154 *kā (M15) vs 156 (M15)"),
    ("154", "155", "154 *kā (M15) vs 155 (M15)"),
    ("154", "153", "154 *kā (M15) vs 153 (M15)"),
    ("154", "151", "154 *kā (M15) vs 151 plain porter (M12)"),
    ("154", "161", "154 *kā (M15) vs 161 diamond-head porter (M14)"),
    ("390", "392", "390 *tai (M162) vs 392 (M162)"),
    ("390", "405", "390 *tai (M162) vs 405 tree (M169)"),
    ("390", "407", "390 *tai (M162) vs 407 tree (M169)"),
    ("390", "406", "390 *tai (M162) vs 406 tree (M169)"),
    ("405", "407", "405 tree (M169) vs 407 tree (M169)"),
    ("861", "817", "861 diamond-top (M267) vs 817 (M267)"),
    ("900", "904", "900 *tiṅkaḷ (M287) vs 904 double-crescent (M294)"),
    ("904", "927", "904 double-crescent (M294) vs 927 (M294)"),
    ("820", "821", "820 *kāl (M391) vs 821 wheel (M391)"),
    ("061", "063", "061 *kāl (M124) vs 063 leg (M125)"),
    ("100", "101", "100 *talai (M8) vs 101 bracketed (M9)"),
    ("100", "103", "100 *talai (M8) vs 103 bracketed (M9)"),
    ("176", "175", "176 *iru/iṟai (M48) vs 175 plain seated (M205)"),
    ("745", "746", "745 3-stroke jar (M345) vs 746 (M345)"),
    ("760", "752", "760 branching-U (M347) vs 752 (M358)"),
    ("803", "806", "803 leaf-tree (M387) vs 806 (M389)"),
]


def run_allograph_tests(profs, crosswalk, mayig):
    log("=== RUNNING DISTRIBUTIONAL ALLOGRAPH IDENTITY TESTS (5,000 SHUFFLES) ===")
    rng = np.random.default_rng(1042)
    pool = sorted([s for s, p in profs.items() if p["n"] >= 4])
    P = len(pool)

    rows = []
    for a, b, label in ALLOGRAPH_PAIRS:
        if a not in profs or b not in profs:
            continue
        pa, pb = profs[a], profs[b]
        cL = cosine_counter(pa["L"], pb["L"])
        cR = cosine_counter(pa["R"], pb["R"])
        cMean = 0.5 * (cL + cR)
        dPos = abs(pa["pos"] - pb["pos"])
        shared_frames = set(pa["frames"].keys()) & set(pb["frames"].keys())
        n_swaps = len(shared_frames)

        # 5,000 random partner draws for sign `a` from pool (n >= 4)
        null_cMean = np.empty(N_SHUF)
        null_cR = np.empty(N_SHUF)
        null_swaps = np.empty(N_SHUF)
        cands = [s for s in pool if s != a]
        # Precompute against all cands once (only ~180 signs!)
        cand_cL = np.array([cosine_counter(pa["L"], profs[t]["L"]) for t in cands])
        cand_cR = np.array([cosine_counter(pa["R"], profs[t]["R"]) for t in cands])
        cand_cM = 0.5 * (cand_cL + cand_cR)
        fa_keys = set(pa["frames"].keys())
        cand_sw = np.array([len(fa_keys & set(profs[t]["frames"].keys())) for t in cands])

        draws = rng.integers(0, len(cands), size=N_SHUF)
        null_cMean = cand_cM[draws]
        null_cR = cand_cR[draws]
        null_swaps = cand_sw[draws]

        _, _, z_cM, p_cM = p_and_z_two_sided(cMean, null_cMean, "greater")
        _, _, z_cR, p_cR = p_and_z_two_sided(cR, null_cR, "greater")
        _, _, z_sw, p_sw = p_and_z_two_sided(n_swaps, null_swaps, "greater")

        mA = crosswalk.get(a, ("", 0))[0]
        mB = crosswalk.get(b, ("", 0))[0]
        same_m77 = (mA != "" and mA == mB)
        same_mayig = (mayig.get(a, "") != "" and mayig.get(a, "") == mayig.get(b, ""))

        rows.append({
            "sign_a": a, "sign_b": b, "label": label,
            "n_a": pa["n"], "n_b": pb["n"],
            "m77_a": mA, "m77_b": mB, "same_m77": same_m77, "same_mayig": same_mayig,
            "abs_dPos": round(dPos, 3),
            "cosL": round(cL, 3), "cosR": round(cR, 3), "cosMean": round(cMean, 3),
            "p_cosMean": p_cM, "p_cosR": p_cR,
            "exact_frame_swaps": n_swaps, "p_swaps": p_sw,
            "sample_swaps": "; ".join(f"{x}_{y}" for x, y in sorted(shared_frames)[:5]),
        })
        log(f"  {a}-{b} (M77 {mA}/{mB}, sameM77={same_m77}): cL={cL:.2f} cR={cR:.2f} (P={p_cR:.4f}) "
            f"cM={cMean:.2f} (P={p_cM:.4f}) swaps={n_swaps:2d} (P={p_sw:.4f}) |dPos|={dPos:.2f}")

    out_csv = os.path.join(OUT_DIR, "key4a_allograph_tests.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return rows


# ==============================================================================
# 5. ZERO-ARTIFACT PROTO-DRAVIDIAN DEDR LIGATURE & MODIFIER TEST (5,000 SHUFFLES)
# ==============================================================================
# Strictly zero regex word overlap between rxA (visual modifier/pictograph) and rxB (corpus/archaeological domain)!
# Format: (sign, family, base, visual_label, rxA_visual, rxB_domain, curated_root, curated_evid, status)
LIGATURE_DEDR_SPECS = [
    (
        "125/892", "Porter/Bow", "090", "bow/archer (892 standalone & 125 = 090 *āḷ + bow)",
        r"\b(bow|bowman|bowmen|archer|arrow|bowstring|quiver)\b",
        r"\b(sell|sale|price|value|trade|merchant|market|barter|shop|vend)\b",
        "*vil / *vil-āḷ", "DEDR 5422 vil ('bow, archer') <-> DEDR 5421 vil ('sell, sale') [2-br PhonEx]; 125 = *vil-āḷ, 892 = *vil",
        "building on it",
    ),
    (
        "255", "Fish/Gharial", "255", "gharial/crocodile/reptile (Mound F granary)",
        r"\b(crocodile|alligator|gharial|lizard|gecko|iguana|chameleon|reptile)\b",
        r"\b(first|beginning|principal|capital|stock|store|ration|account|chief|head)\b",
        "*mutal", "DEDR 4952 mutalai ('crocodile') <-> DEDR 4950 mutal ('first, principal, capital') [2-br PhonSt]",
        "building on it",
    ),
    (
        "233", "Fish", "220", "horizontal dividing bar / split (+ 220 *mīṉ)",
        r"\b(split|crack|divide|bisect|separate|apportion|chop|hack|fissure)\b",
        r"\b(dawn|bright|brightness|light|lustre|shine|glitter|splendour|star|morning)\b",
        "*veṭi-mīṉ / *vāku-mīṉ", "DEDR 5473 veṭi ('split, crack') <-> 5475 veṭi ('dawn, break of day') [2-br PhonEx]; 5202 vaku <-> 5332 vāku ('brightness') [2-br PhonEx]",
        "building on it",
    ),
    (
        "240", "Fish", "220", "side whiskers / oblique cheek-slashes / fins (+ 220 *mīṉ)",
        r"\b(incline|slant|wing|feather|fin|whisker|cheek|barb|bristle)\b",
        r"\b(brilliance|bright|light|lustre|shine|glitter|splendour|eminent|illustrious|star|white)\b",
        "*cāy-mīṉ / *ciṟai-mīṉ?", "DEDR 2456 cāy ('incline, slant') <-> 2457 cāy ('brilliance, light') [2-br PhonEx]; 2591 ciṟai ('wing') <-> 2589 ciṟa ('eminent') [2-lg PhonSt]",
        "testing it",
    ),
    (
        "231", "Fish", "220", "1 internal vertical stroke (+ 220 *mīṉ)",
        r"\b(inside|interior|inner|within|eaves|core|middle)\b",
        r"\b(great|master|chief|king|lord|ruler|star|bright|house|abode)\b",
        "*uḷ-mīṉ / *iṟai-mīṉ", "Operator-locked [220 *mīṉ + internal stroke]; DEDR 698 uḷ ('inside') / DEDR 528 iṟai ('inside') <-> 527 iṟai ('great, chief') [2-br PhonEx]",
        "building on it",
    ),
    (
        "226", "Fish", "220", "4 corner strokes / cage (+ 220 *mīṉ)",
        r"\b(cage|birdcage|coop|nest|fence|enclosure|yard|surround|four)\b",
        r"\b(house|abode|family|lineage|village|town|fort|precinct|day|star|servant|guard)\b",
        "*mīṉ-kūṭu / *mīṉ-nāḷ", "Operator-locked 8/8 finalizer [220 *mīṉ + 4-corner cage]; DEDR 1883 kūṭu ('cage') <-> 1655 kuṭi ('house') [2-br PhonSt]",
        "building on it",
    ),
    (
        "741", "Jar", "740", "1 internal vertical stroke (+ 740 *kuṭi)",
        r"\b(inside|interior|inner|within|one|single)\b",
        r"\b(house|abode|family|lineage|place|part|ward|chief|master|belong)\b",
        "*uḷ-kuṭi / *oru-kuṭi", "Operator-locked 10/10 construct-state medializer [740 *kuṭi + 1 internal stroke]; DEDR 698 uḷ / 990 oru + 1655 kuṭi",
        "building on it",
    ),
    (
        "413", "Tree/Comb", "400", "double-sided stalk / ear of grain (M177)",
        r"\b(ear of paddy|paddy|rice|wheat|barley|millet|corn|stalk|spike|chaff)\b",
        r"\b(tax|duty|tribute|cut|reap|harvest|measure|granary|store|loan|debt)\b",
        "*ari", "DEDR 215 ari ('ear of paddy, rice, husked grain') <-> DEDR 216 ari ('tax, duty') & 212 ari ('cut, reap') [2-br PhonEx]",
        "building on it",
    ),
    (
        "140", "Porter/Man", "090", "woman with round breasts & raised arm (M17)",
        r"\b(woman|female|mother|breast|bosom|wife|maiden|girl)\b",
        r"\b(house|home|lady|mistress|goddess|matron|fort|town|village|citadel|chief|ruler)\b",
        "*ammā / *il", "DEDR 183 ammā ('mother, matron, lady, goddess') [Pan-Drav DIRECT]; DEDR 494 il ('wife, mistress' <-> 'house') [Pan-Drav DIRECT]",
        "testing it",
    ),
    (
        "595", "Chest/Forge", "590", "striped furnace / kiln / box + bar (citadel forge)",
        r"\b(oven|furnace|kiln|hearth|fireplace|fire|flame|blaze|heat|hot|burn)\b",
        r"\b(melt|smelt|cook|boil|copper|bronze|iron|metal|smith|forge|citadel|arsenal)\b",
        "*aṭu / *kaṉal", "DEDR 76 aṭu ('oven, furnace, melt') [Pan-Drav DIRECT]; DEDR 1406 kaṉal ('fire, hot, burn', pairs w/ 850 *kaṉ)",
        "testing it",
    ),
    (
        "503", "Sail/Triangle", "490", "horizontally striped hill / slope (VS estate)",
        r"\b(hill|mountain|slope|declivity|ridge|bank|embankment|mound|summit)\b",
        r"\b(rent|lease|hire|share|crop|field|land|estate|village|dyer|cloth|weave)\b",
        "*vāram / *karai", "DEDR 5360 vāram ('mountain slope') <-> 5359 vāram ('rent, lease of land, crop share') [2-lg PhonEx]; 1293 karai ('ridge/land/cloth-border')",
        "testing it",
    ),
    (
        "095", "Porter/Man", "090", "person + short stick/hammer (copper tablets)",
        r"\b(stick|club|rod|staff|pole|hammer|sledge|cane|baton)\b",
        r"\b(beat|strike|pound|smith|copper|bronze|metal|guard|watch|protect|chief|ruler)\b",
        "*koṭṭu-āḷ / *aṟai-āḷ?", "DEDR 2063 koṭṭu ('hammer/beat'), 2349 cammaṭṭi ('smith's hammer'), 1417/1416 kā ('pole/guard' duplicates 154)",
        "testing it",
    ),
    (
        "920", "Moon/Crescent", "900", "crescent (900) + leaf at middle (office opener)",
        r"\b(moon|crescent|moonlight|lunar)\b",
        r"\b(month|season|period|office|duty|tax|ration|allowance|day|time)\b",
        "*tiṅkaḷ-[il]", "Compositional [900 *tiṅkaḷ moon/month + leaf]; DEDR 3213 tiṅkaḷ ('moon' <-> 'month') [Pan-Drav DIRECT]",
        "testing it",
    ),
    (
        "861", "Diamond/Leaf", "850", "diamond + small diamond at top (M267 = 817)",
        r"\b(eye|bud|sprout|shoot|kernel|seed|gem|jewel|summit|crown|top|prow)\b",
        r"\b(head|chief|first|front|begin|number|count|calculation|measure|weight|unit|span)\b",
        "*alaku / *ucci?", "Multiple rivals (DEDR 237/238 alaku 'head/blade' <-> 'number/calculation' [2-lg PhonEx]; 579 ucci 'crown/top'); 861=817 M267 locked",
        "testing it",
    ),
    (
        "840", "Diamond/Leaf", "790", "two overlapping leaves (doubled 790 *vaḷai)",
        r"\b(bangle|bracelet|ring|circle|shell|leaf|petal|pair|couple|twin)\b",
        r"\b(measure|weight|craft|smith|vessel|pot|cloth|thread|sack|bundle|trade|guild)\b",
        "*2× vaḷai?", "Distributional pair of 790 (cL=0.82); no unique single-root DEDR rebus beyond base *vaḷai",
        "testing it",
    ),
    (
        "832", "Diamond/Leaf", "790", "leaf + 1 internal vertical stroke (M375)",
        r"\b(leaf|seed|sesame|kernel|pod|bean|grain)\b",
        r"\b(tax|duty|measure|oil|press|house|abode|inner|inside|count)\b",
        "*uḷ-vaḷai / *eḷ-uḷ?", "Obeys internal_vert_stroke operator on 790 (dF400=-0.14, dSeal=+0.16); DEDR 215/216 ari overlaps 413",
        "testing it",
    ),
    (
        "803", "Diamond/Leaf", "790", "leaf + tree (390) at bottom (M387)",
        r"\b(leaf|foliage|shoot|sprout|twig|branch)\b",
        r"\b(house|home|abode|lineage|clan|family|chief|lord)\b",
        "*il-tai?", "Graphic ligature [leaf + 390 tree]; DEDR 497 ilai ('leaf') <-> 494 il ('house') fails 3-char stem cutoff",
        "testing it",
    ),
    (
        "700", "Cup/Vessel", "700", "simple U cup (~9.24 L, base of 705 *kalam)",
        r"\b(cup|bowl|pot|vessel|jar|dish|pitcher|basin)\b",
        r"\b(measure|capacity|ration|allowance|grain|portion|handful|weight)\b",
        "*akal / *aḷ?", "Multiple broad vessel<->measure rivals in DEDR (high shuffle baseline); base of locked 705 *kalam",
        "testing it",
    ),
    (
        "391", "Tree/Comb", "390", "3-pronged tree + caret hat (smithy copper)",
        r"\b(tree|plant|shoot|sapling|twig|branch|roof|cover|hat)\b",
        r"\b(smith|forge|copper|bronze|iron|metal|fire|burn|kiln|furnace)\b",
        "null", "Compositional [390 *tai + caret hat], but zero clean Proto-Dravidian tree/roof <-> smith/copper rebus",
        "null",
    ),
]


def run_dedr_ligature_tests():
    log("=== RUNNING ZERO-ARTIFACT DEDR LIGATURE & MODIFIER TESTS (5,000 SHUFFLES) ===")
    etyma_2br, etyma_2lg, forms_phon, forms_ascii, eid_to_cid = k3.load_clean_dedr()
    lex2b = k3.InMemoryLex(etyma_2br)
    lex2l = k3.InMemoryLex(etyma_2lg)

    # Strict zero-overlap assertion on regex token vocabularies!
    for spec in LIGATURE_DEDR_SPECS:
        s, _, _, _, rxA_s, rxB_s, _, _, _ = spec
        wA = set(re.findall(r"[a-z]+", rxA_s.lower())) - {"b"}
        wB = set(re.findall(r"[a-z]+", rxB_s.lower())) - {"b"}
        ov = wA & wB
        assert not ov, f"Regex word overlap on sign {s}: {ov}"
    log(f"Zero-overlap regex hygiene verified across all {len(LIGATURE_DEDR_SPECS)} independent ligature specs!")

    M = len(LIGATURE_DEDR_SPECS)

    def eval_lex(lex, seed):
        rng = np.random.default_rng(seed)
        inA = np.zeros((M, lex.E), dtype=bool)
        inB = np.zeros((M, lex.E), dtype=bool)
        for idx, spec in enumerate(LIGATURE_DEDR_SPECS):
            inA[idx] = lex.match_regex_bool(re.compile(spec[4], re.I))
            inB[idx] = lex.match_regex_bool(re.compile(spec[5], re.I))

        cids = lex.cid_int
        res = {}
        # 1. Distinct-cluster rebus tests (PhonEx, PhonSt, AscEx)
        for mode in ("phon_exact", "phon_stem", "ascii_exact"):
            us, vs = lex.edges[mode]
            diff_cid = (cids[us] != cids[vs])
            us_d, vs_d = us[diff_cid], vs[diff_cid]

            real_vec = np.zeros(M, dtype=np.int32)
            for idx in range(M):
                hit = np.any((inA[idx, us_d] & inB[idx, vs_d]) | (inB[idx, us_d] & inA[idx, vs_d]))
                real_vec[idx] = int(hit)

            # 5,000 exact cluster-preserving sound shuffles
            null_mat = np.zeros((N_SHUF, M), dtype=np.int8)
            for it in range(N_SHUF):
                perm = lex.make_cluster_perm(rng)
                pu = perm[us_d]
                pv = perm[vs_d]
                # vectorized over all M signs via matrix indexing
                a_u = inA[:, pu]
                b_v = inB[:, pv]
                b_u = inB[:, pu]
                a_v = inA[:, pv]
                null_mat[it] = np.any((a_u & b_v) | (b_u & a_v), axis=1).astype(np.int8)

            tot_obs = int(real_vec.sum())
            tot_null = null_mat.sum(axis=1)
            mu, sd, z, p = p_and_z_two_sided(tot_obs, tot_null, "greater")
            per_sign_p = [round(float((1.0 + np.sum(null_mat[:, j] >= real_vec[j])) / (1.0 + N_SHUF)) if real_vec[j] > 0 else 1.0, 5) for j in range(M)]
            per_sign_rate = [round(float(null_mat[:, j].mean()), 4) for j in range(M)]
            res[mode] = {
                "obs": tot_obs, "n": M, "null_mu": mu, "null_sd": sd, "z": z, "p": p,
                "real_vec": [int(x) for x in real_vec],
                "per_sign_p": per_sign_p,
                "per_sign_null_rate": per_sign_rate,
            }

        # 2. Direct Pan-Dravidian Polysemy (5,000 Domain-B Permutations across the M signs)
        pair_mat = np.zeros((M, M), dtype=np.int8)
        for i in range(M):
            for j in range(M):
                pair_mat[i, j] = int(np.any(inA[i] & inB[j]))
        diag_real = np.diag(pair_mat)
        obs_dir = int(diag_real.sum())
        null_dir = np.empty(N_SHUF, dtype=np.int32)
        for it in range(N_SHUF):
            perm_j = rng.permutation(M)
            null_dir[it] = int(pair_mat[np.arange(M), perm_j].sum())
        mu_d, sd_d, z_d, p_d = p_and_z_two_sided(obs_dir, null_dir, "greater")
        off_rate = [round(float((pair_mat[i].sum() - pair_mat[i, i]) / max(1, M - 1)), 4) for i in range(M)]
        res["direct_polysemy_domperm"] = {
            "obs": obs_dir, "n": M, "null_mu": mu_d, "null_sd": sd_d, "z": z_d, "p": p_d,
            "real_vec": [int(x) for x in diag_real],
            "per_sign_offdiag_rate": off_rate,
        }
        return res, inA, inB

    res_2b, inA_2b, inB_2b = eval_lex(lex2b, seed=2042)
    res_2l, inA_2l, inB_2l = eval_lex(lex2l, seed=3042)

    def extract_best_bridges(lex, maskA, maskB):
        out = []
        # Direct
        for i in np.where(maskA & maskB)[0][:3]:
            out.append(f"DIRECT DEDR {lex.eids[i]} {lex.hws[i]} ({'; '.join(lex.senses[i])[:50]})")
        cids = lex.cid_int
        for mode in ("phon_exact", "phon_stem", "ascii_exact"):
            us, vs = lex.edges[mode]
            m = (cids[us] != cids[vs]) & ((maskA[us] & maskB[vs]) | (maskB[us] & maskA[vs]))
            for k in np.where(m)[0][:3]:
                u, v = us[k], vs[k]
                if not (maskA[u] and maskB[v]):
                    u, v = v, u
                out.append(f"{mode.upper()} DEDR {lex.eids[u]} {lex.hws[u]} <-> {lex.eids[v]} {lex.hws[v]}")
        return out[:5]

    rows = []
    for idx, (s, fam, base, vlab, rxA, rxB, croot, cevid, status) in enumerate(LIGATURE_DEDR_SPECS):
        b2b = extract_best_bridges(lex2b, inA_2b[idx], inB_2b[idx])
        b2l = extract_best_bridges(lex2l, inA_2l[idx], inB_2l[idx])
        rows.append({
            "sign": s, "family": fam, "base": base, "visual_desc": vlab,
            "nA_2br": int(inA_2b[idx].sum()), "nB_2br": int(inB_2b[idx].sum()),
            "direct_2br": res_2b["direct_polysemy_domperm"]["real_vec"][idx],
            "phonex_2br": res_2b["phon_exact"]["real_vec"][idx],
            "phonst_2br": res_2b["phon_stem"]["real_vec"][idx],
            "ascex_2br": res_2b["ascii_exact"]["real_vec"][idx],
            "phonex_2lg": res_2l["phon_exact"]["real_vec"][idx],
            "phonst_2lg": res_2l["phon_stem"]["real_vec"][idx],
            "p_shuf_phonex_2br": res_2b["phon_exact"]["per_sign_p"][idx],
            "p_shuf_phonst_2br": res_2b["phon_stem"]["per_sign_p"][idx],
            "p_shuf_ascex_2br": res_2b["ascii_exact"]["per_sign_p"][idx],
            "null_rate_phonex_2br": res_2b["phon_exact"]["per_sign_null_rate"][idx],
            "null_rate_phonst_2br": res_2b["phon_stem"]["per_sign_null_rate"][idx],
            "offdiag_direct_2br": res_2b["direct_polysemy_domperm"]["per_sign_offdiag_rate"][idx],
            "top_dedr_2br": " | ".join(b2b),
            "top_dedr_2lg": " | ".join(b2l),
            "candidate_root": croot,
            "evidence": cevid,
            "status": status,
        })

    out_csv = os.path.join(OUT_DIR, "key4a_dedr_ligatures.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    summary = {
        "n_shuf": N_SHUF,
        "n_signs": M,
        "pdrav_2branch": {k: {kk: vv for kk, vv in v.items() if kk in ("obs", "n", "null_mu", "null_sd", "z", "p")}
                          for k, v in res_2b.items()},
        "pdrav_2lang": {k: {kk: vv for kk, vv in v.items() if kk in ("obs", "n", "null_mu", "null_sd", "z", "p")}
                        for k, v in res_2l.items()},
        "status_counts": dict(collections.Counter(r["status"] for r in rows)),
    }
    with open(os.path.join(OUT_DIR, "key4a_dedr_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    for tag, d in [("2-Branch", summary["pdrav_2branch"]), ("2-Lang  ", summary["pdrav_2lang"])]:
        log(f"  DEDR {tag}: PhonEx={d['phon_exact']['obs']}/{M} (null={d['phon_exact']['null_mu']}, z={d['phon_exact']['z']}, P={d['phon_exact']['p']}) | "
            f"PhonSt={d['phon_stem']['obs']}/{M} (null={d['phon_stem']['null_mu']}, z={d['phon_stem']['z']}, P={d['phon_stem']['p']}) | "
            f"AscEx={d['ascii_exact']['obs']}/{M} (P={d['ascii_exact']['p']}) | "
            f"DirectPoly={d['direct_polysemy_domperm']['obs']}/{M} (z={d['direct_polysemy_domperm']['z']}, P={d['direct_polysemy_domperm']['p']})")

    for r in rows:
        log(f"    {r['sign']} [{r['status']:14s}] {r['candidate_root']:24s} | "
            f"2br Ex={r['phonex_2br']}(p={r['p_shuf_phonex_2br']:.4f}) St={r['phonst_2br']}(p={r['p_shuf_phonst_2br']:.4f}) Dir={r['direct_2br']}")
    return summary, rows


# ==============================================================================
# 6. EXACT TOKEN & 100%-FACE COVERAGE JUMP ACROSS ALL 4,227 INTACT FACES
# ==============================================================================
# Strictly separated Key #4A epistemic tiers (zero overlap with LOCKED19 | LOANS4 | BASIC_NUMS):
KEY4A_BUILD_ALLOGRAPHS = {
    # Verified Mahadevan-identical & 5,000-shuffle distributionally locked allographs of our 19 sound-locked signs
    "706": ("705 *kalam (M336 allograph, 17 swaps, P=0.0024)", "Allograph"),
    "704": ("705 *kalam (M336 allograph, shares rare R:167/255)", "Allograph"),
    "156": ("154 *kā (M15 yoke-load/guard allograph, 5 swaps, P=0.0092)", "Allograph"),
    "158": ("154 *kā (M15 closer allograph, 6 swaps, P=0.0024)", "Allograph"),
    "155": ("154 *kā (M15 allograph, cM=0.76, P=0.0076)", "Allograph"),
    "153": ("154 *kā (M15 allograph, cR=1.00, P=0.0036)", "Allograph"),
    "151": ("154 *kā (M12 plain porter base, cR=0.984, P_cR=0.0250)", "Allograph"),
    "392": ("390 *tai (M162 allograph, cM=0.74, P=0.0116)", "Allograph"),
    "405": ("390 *tai (M169 tree allograph, 13 swaps, P=0.0050)", "Allograph"),
    "406": ("390 *tai (M169 tree allograph, 5 swaps, P=0.0074)", "Allograph"),
    "407": ("390 *tai (M169 copper-tablet tree allograph, 10 swaps, P=0.0162)", "Allograph"),
}

KEY4A_BUILD_OPERATORS = {
    # Compositional operator-locked derivatives of our 19 sound-locked signs
    "741": ("*uḷ-kuṭi / *oru-kuṭi [740 + 1 internal stroke]", "Operator: internal_vert_stroke"),
    "742": ("*iru-kuṭi [740 + 2 internal strokes]", "Operator: multi_stroke_inside"),
    "743": ("*iru-kuṭi [740 + 2 internal strokes]", "Operator: multi_stroke_inside"),
    "744": ("*iru-kuṭi [740 + 2 internal strokes]", "Operator: multi_stroke_inside"),
    "745": ("*mū-kuṭi [740 + 3 internal strokes]", "Operator: multi_stroke_inside"),
    "746": ("*mū-kuṭi [740 + 3 internal strokes, M345]", "Operator: multi_stroke_inside"),
    "747": ("*mū-kuṭi [740 + 3 internal strokes]", "Operator: multi_stroke_inside"),
    "748": ("*nāl-kuṭi [740 + 4 internal strokes]", "Operator: multi_stroke_inside"),
    "231": ("*uḷ-mīṉ / *iṟai-mīṉ [220 + 1 internal stroke]", "Operator: internal_vert_stroke"),
    "226": ("*mīṉ-[CAGE] [220 + 4-corner finalizer]", "Operator: cage_4corners"),
    "236": ("*oḷi-mīṉ-[CAGE] [235 + 4-corner finalizer]", "Operator: cage_4corners"),
    "232": ("*uḷ-mīṉ-[CAGE] [231 + 4-corner finalizer]", "Operator: cage_4corners"),
    "222": ("*[BRACKET]-mīṉ [220 + side brackets]", "Operator: side_brackets"),
    "101": ("*[BRACKET]-talai [100 + side brackets, cR=0.95]", "Operator: side_brackets"),
    "103": ("*[BRACKET]-talai [100 + side brackets, cR=0.82]", "Operator: side_brackets"),
    "093": ("*uḷ-āḷ [090 + 1 internal stroke]", "Operator: internal_vert_stroke"),
    "097": ("*[BRACKET]-āḷ [090 + side brackets]", "Operator: side_brackets"),
    "904": ("*iru-tiṅkaḷ [2× 900 *tiṅkaḷ, cR=0.905, P_cR=0.049]", "Operator: dual_crescent"),
    "927": ("*iru-tiṅkaḷ [2× 900 *tiṅkaḷ, M294, cR=0.947, P=0.0038]", "Operator: dual_crescent"),
}

KEY4A_BUILD_DEDR_NEW = {
    # Newly DEDR zero-artifact phonetic ligatures (verified against 5,000 cluster-preserving shuffles)
    "125": ("*vil-āḷ [090 *āḷ + 892 *vil bow/sell, 2-br PhonEx, P=0.049]", "DEDR Ligature Lock"),
    "892": ("*vil [bow/sell, DEDR 5422/5421, 2-br PhonEx, P=0.049]", "DEDR Ligature Component"),
    "255": ("*mutal [crocodile->first/principal, DEDR 4952/4950, 2-br PhonSt]", "DEDR Rebus Lock"),
    "233": ("*veṭi-mīṉ / *vāku-mīṉ [split->dawn/bright + *mīṉ, 2-br PhonEx]", "DEDR Diacritic Lock"),
    "234": ("*veṭi-mīṉ-[CAGE] [233 + 4-corner finalizer]", "Operator: cage_4corners"),
    "413": ("*ari [ear-of-grain->tax/cut, DEDR 215/216/212, 2-br PhonEx]", "DEDR Rebus Lock"),
}

KEY4A_TESTING_IT = {
    "240": ("*cāy-mīṉ / *ciṟai-mīṉ? [220 + whiskers/fins]", "Testing: Fish Diacritic"),
    "241": ("240-[CAGE] [240 + 4-corner finalizer]", "Testing: Caged 240"),
    "242": ("240 variant", "Testing: Fish Diacritic"),
    "243": ("Hatched roofed fish", "Testing: Fish Diacritic"),
    "861": ("M267 Diamond+top-diamond (allograph of 817, P=0.0034)", "Testing: M267 Opener"),
    "817": ("M267 Diamond+top-diamond (allograph of 861, P=0.0034)", "Testing: M267 Opener"),
    "700": ("*akal / *aḷ? [cup ~9.24 L, base of 705]", "Testing: Cup Base"),
    "703": ("700 + 3 internal strokes", "Testing: Cup + 3 Strokes"),
    "711": ("700 + X", "Testing: Cup Ligature"),
    "752": ("700 + tree branches (allograph of 760, P=0.0246)", "Testing: Cup-Tree Ligature"),
    "760": ("700 + tree branches (allograph of 752, P=0.0246)", "Testing: Cup-Tree Ligature"),
    "920": ("*tiṅkaḷ-[il]? [900 + leaf, office opener]", "Testing: Moon+Leaf Ligature"),
    "924": ("*kōṭu~*kōṭai? [hatched 923]", "Testing: Hatched Crescent"),
    "803": ("*il-tai? [790 leaf + 390 tree, 16 swaps w/ 806]", "Testing: Leaf-Tree Ligature"),
    "806": ("*il-tai? [790 leaf + 390 tree, 16 swaps w/ 803]", "Testing: Leaf-Tree Ligature"),
    "804": ("803-[CAGE]", "Testing: Caged 803"),
    "807": ("806-[CAGE]", "Testing: Caged 806"),
    "840": ("2× 790 *vaḷai? [paired leaves]", "Testing: Doubled Leaf"),
    "845": ("Hatched 840", "Testing: Hatched Paired Leaf"),
    "832": ("790 + 1 internal stroke", "Testing: Leaf + Stroke"),
    "140": ("*ammā / *il [woman w/ raised arm]", "Testing: Direct Polysemy"),
    "595": ("*aṭu / *kaṉal [striped furnace]", "Testing: Direct Polysemy"),
    "503": ("*vāram / *karai [striped hill]", "Testing: Direct/Rebus"),
    "095": ("090 + short stick", "Testing: Man+Stick"),
    "091": ("090 + 090 (clause-initial pair)", "Testing: Doubled Man"),
    "159": ("154 + diamond head (M14)", "Testing: Porter Variant"),
    "161": ("154 + diamond head (M14)", "Testing: Porter Variant"),
    "592": ("590-[CAGE]", "Testing: Caged Chest"),
    "821": ("820 wheel variant (M391, failed shuffle P=0.29)", "Testing: Unverified Allograph"),
    "063": ("Leg variant (M343 != M124, failed shuffle P=0.20)", "Testing: Unverified Allograph"),
    "175": ("Plain seated base of 176 (cL=0.91, cR=0.20, diverges right)", "Testing: Uncaged Base of 176"),
}

KEY4A_NULL = {
    "391": ("390 + caret hat (zero clean tree/roof<->smithy DEDR rebus)", "Null"),
}


def compute_coverage(lipi_intact, new_intact, all_intact):
    log("=== COMPUTING EXACT TOKEN & FACE COVERAGE JUMP (4,227 INTACT FACES) ===")
    base_11 = set(LOCKED11.keys())
    base_19 = set(LOCKED19.keys())
    base_19_lb = base_19 | set(LOANS4.keys()) | set(BASIC_NUMS.keys())

    # Assert zero overlap between baseline and Key #4A tiers
    b_allo = set(KEY4A_BUILD_ALLOGRAPHS.keys())
    b_oper = set(KEY4A_BUILD_OPERATORS.keys())
    b_dedr = set(KEY4A_BUILD_DEDR_NEW.keys())
    b_all = b_allo | b_oper | b_dedr
    t_set = set(KEY4A_TESTING_IT.keys())
    n_set = set(KEY4A_NULL.keys())

    assert not (base_19_lb & b_all), f"Overlap base & build: {base_19_lb & b_all}"
    assert not (b_allo & b_oper) and not (b_allo & b_dedr) and not (b_oper & b_dedr), "Overlap inside build tiers!"
    assert not ((base_19_lb | b_all) & t_set), f"Overlap & testing: {(base_19_lb | b_all) & t_set}"

    tiers = [
        ("01_key2a_11_locked", base_11),
        ("02_key3a_19_locked", base_19),
        ("03_baseline_19_plus_loans_bnums", base_19_lb),
        ("04_plus_4a_allographs_build", base_19_lb | b_allo),
        ("05_plus_4a_allographs_and_operators_build", base_19_lb | b_allo | b_oper),
        ("06_plus_4a_ALL_building_on_it", base_19_lb | b_all),
        ("07_plus_4a_building_AND_testing_it", base_19_lb | b_all | t_set),
    ]

    cov_out = {}
    for sname, sub in [
        ("lipi_intact_3600", lipi_intact),
        ("new_unpartnered_intact_627", new_intact),
        ("combined_intact_4227", all_intact),
    ]:
        tot_tok = 0
        face_toks = []
        for r in sub:
            toks = [t for t in r["signs"].split("-") if t and t != "000"]
            if toks:
                face_toks.append(toks)
                tot_tok += len(toks)

        slice_res = {"n_faces": len(face_toks), "total_tokens": tot_tok, "tiers": {}}
        for tname, sset in tiers:
            c_tok = sum(1 for toks in face_toks for t in toks if t in sset)
            c_100 = sum(1 for toks in face_toks if all(t in sset for t in toks))
            slice_res["tiers"][tname] = {
                "n_signs_in_tier": len(sset),
                "tokens": c_tok,
                "token_pct": round(100.0 * c_tok / tot_tok, 2),
                "faces_100pct": c_100,
                "faces_100pct_pct": round(100.0 * c_100 / len(face_toks), 2),
            }
        cov_out[sname] = slice_res

    # Per-sign incremental contribution table
    c_l = collections.Counter(t for r in lipi_intact for t in r["signs"].split("-") if t and t != "000")
    c_n = collections.Counter(t for r in new_intact for t in r["signs"].split("-") if t and t != "000")
    tot_all = sum(c_l.values()) + sum(c_n.values())

    bd_rows = []
    for tier_lbl, d in [
        ("building_on_it:allograph", KEY4A_BUILD_ALLOGRAPHS),
        ("building_on_it:operator", KEY4A_BUILD_OPERATORS),
        ("building_on_it:dedr_ligature", KEY4A_BUILD_DEDR_NEW),
        ("testing_it", KEY4A_TESTING_IT),
        ("null", KEY4A_NULL),
    ]:
        for s, (gloss, subcat) in sorted(d.items(), key=lambda kv: -(c_l[kv[0]] + c_n[kv[0]])):
            nl, nn = c_l[s], c_n[s]
            nt = nl + nn
            bd_rows.append({
                "tier": tier_lbl, "subcat": subcat, "sign": s, "reading_gloss": gloss,
                "lipi_intact": nl, "new_intact": nn, "total_intact": nt,
                "pct_of_4227_tokens": round(100.0 * nt / tot_all, 3),
            })

    with open(os.path.join(OUT_DIR, "key4a_coverage.json"), "w", encoding="utf-8") as f:
        json.dump(cov_out, f, indent=2)
    with open(os.path.join(OUT_DIR, "key4a_coverage_breakdown.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(bd_rows[0].keys()))
        w.writeheader()
        w.writerows(bd_rows)

    for sname in ("lipi_intact_3600", "new_unpartnered_intact_627", "combined_intact_4227"):
        sl = cov_out[sname]
        log(f"  COVERAGE [{sname}] (faces={sl['n_faces']}, tok={sl['total_tokens']}):")
        for tname, tv in sl["tiers"].items():
            log(f"    {tname:42s}: {tv['tokens']:5d} tok ({tv['token_pct']:5.2f}%) | 100%-faces={tv['faces_100pct']:4d} ({tv['faces_100pct_pct']:5.2f}%)")
    return cov_out, bd_rows


def main():
    log(f"Starting Key #4A Diacritic, Modifier & Graphic Ligature Cracker (N_SHUF={N_SHUF})")
    lipi_intact, new_intact, all_intact, shapes, mayig, crosswalk, mark_fam, merge_grps, sf_lex = load_corpus_and_metadata()
    profs = build_sign_profiles(all_intact)

    build_catalog(lipi_intact, new_intact, profs, shapes, mayig, crosswalk, mark_fam, merge_grps, sf_lex)
    run_operator_tests(all_intact, profs)
    run_allograph_tests(profs, crosswalk, mayig)
    run_dedr_ligature_tests()
    compute_coverage(lipi_intact, new_intact, all_intact)
    log("All Key #4A analyses completed cleanly!")


if __name__ == "__main__":
    main()
