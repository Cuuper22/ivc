#!/usr/bin/env python3
"""
Key #3 Track B: Gulf Seal Photo/Orientation Audit, Re-Aligned Ventris Network,
& Ur III Guabba/Girsu/Ur Merchant Prosopography (key3b_gulf_ur3_audit.py).

Executes all three Track B audits cleanly and deterministically:
  - Test 3B-1: Physical Seal Face vs. Clay Impression & Animal-Compass Audit
               across all 48 verified Gulf/abroad/home-round seals.
               Outputs: work_data/key3b/gulf_orientation_physical_audit.csv
                        work_data/key3b/test3b1_orientation_summary.json
  - Test 3B-2: Re-Run Key #1's Ventris Network, Gulf Calque Grammar,
               MAN -> COSMO Order Test (5,000 shuffles), and Mainland Bigram
               Support BEFORE vs AFTER Mirror Orientation Correction.
               Outputs: work_data/key3b/test3b2_before_after_summary.csv
                        work_data/key3b/test3b2_realigned_ventris.json
  - Test 3B-3: Ur III (UET 3) & Girsu/Guabba/Irisagrig (lu2/dumu me-luh-ha)
               vs OB (UET 5) Merchant Prosopography + Two 5,000-Shuffle Tests:
               (a) Theophoric / Institutional Calque Test (Nanna/Moon vs rivals)
               (b) Non-Sumerian / Meluhhan Name Phonetic Test vs 11 locked
                   Proto-Dravidian roots + top Indus name-slot stems.
               Outputs: work_data/key3b/ur3_meluhha_prosopography.csv
                        work_data/key3b/test3b3_ur3_prosopography_stats.json
"""

import collections
import csv
import json
import math
import random
import re
from pathlib import Path

ROOT = Path("/home/antigravity/Cuuper22/ivc")
OUT_DIR = ROOT / "work_data" / "key3b"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 2026
random.seed(SEED)

# =============================================================================
# SHARED MATH & PARSING UTILITIES
# =============================================================================

def parse_toks(seq: str):
    return [t for t in seq.split("-") if t and t != "000" and t != "ALT" and not t.startswith("LE:")]

def get_faces(full_text: str):
    if not full_text:
        return []
    faces = []
    for face in full_text.split("|"):
        toks = [t for t in re.findall(r"\d{3}", face) if t != "000"]
        if toks:
            faces.append(toks)
    return faces

def binom_two_sided(k: int, n: int) -> float:
    if n <= 0:
        return 1.0
    m = min(k, n - k)
    tail = sum(math.comb(n, i) for i in range(m + 1)) * (0.5 ** n)
    return min(1.0, 2.0 * tail)

def fisher_exact_two_sided(a: int, b: int, c: int, d: int):
    r1, r2 = a + b, c + d
    c1, n = a + c, a + b + c + d
    odds = (a * d) / (b * c) if (b * c) > 0 else float("inf")
    denom = math.comb(n, c1)
    if denom == 0:
        return odds, 1.0, 1.0
    def hyp(x):
        return (math.comb(r1, x) * math.comb(r2, c1 - x)) / denom
    p_obs = hyp(a)
    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    p_two = sum(hyp(x) for x in range(lo, hi + 1) if hyp(x) <= p_obs + 1e-12)
    p_greater = sum(hyp(x) for x in range(a, hi + 1))
    return odds, min(1.0, p_two), min(1.0, p_greater)

def z_and_p(obs: float, null_arr):
    mu = sum(null_arr) / len(null_arr)
    sd = math.sqrt(sum((x - mu) ** 2 for x in null_arr) / len(null_arr))
    z = (obs - mu) / sd if sd > 1e-12 else 0.0
    p_ge = (sum(1 for x in null_arr if x >= obs) + 1) / (len(null_arr) + 1)
    p_le = (sum(1 for x in null_arr if x <= obs) + 1) / (len(null_arr) + 1)
    return mu, sd, z, p_ge, p_le

def to_skel(s: str) -> str:
    """Normalize transliteration/root to consonant skeleton with collapse of adjacent repeats."""
    s = s.lower().strip()
    # Replace common Sumerological/Dravidian/Indological digraphs & diacritics
    repls = [
        ("sz", "s"), ("š", "s"), ("ṣ", "s"), ("ś", "s"),
        ("ṭ", "t"), ("ḍ", "d"), ("ṇ", "n"), ("ṉ", "n"), ("ñ", "n"), ("ŋ", "n"), ("ṅ", "n"),
        ("ḷ", "l"), ("ḻ", "l"), ("ṟ", "r"), ("ṛ", "r"),
        ("ḫ", "h"), ("ḥ", "h"), ("ĝ", "g"), ("ā", "a"), ("ī", "i"), ("ū", "u"), ("ē", "e"), ("ō", "o"),
        ("'", ""), ("ʾ", ""), ("ʿ", ""),
    ]
    for k, v in repls:
        s = s.replace(k, v)
    s = re.sub(r"[^a-z]", "", s)
    cons = re.sub(r"[aeiouy]", "", s)
    out = []
    for ch in cons:
        if not out or out[-1] != ch:
            out.append(ch)
    return "".join(out)

# =============================================================================
# LOAD MAINLAND LIPI CORPUS & GULF VERIFIED MASTER
# =============================================================================

ABROAD_REGIONS = {"Persian Gulf", "Mesopotamia", "Iranian Plateau", "Central Asia"}

with open(ROOT / "work_data" / "gulf3" / "gulf3_verified.csv", newline="", encoding="utf-8") as f:
    GULF_VERIFIED = list(csv.DictReader(f))

with open(ROOT / "work_data" / "sem" / "objects_lipi.csv", newline="", encoding="utf-8") as f:
    LIPI_ROWS = list(csv.DictReader(f))

# Build mainland bigram & ordered-pair counts from is_event_rep=True mainland faces
mainland_adj = collections.Counter()
mainland_ord = collections.Counter()
mainland_home_seals = []
mainland_rep_count = 0

for r in LIPI_ROWS:
    if r.get("region") in ABROAD_REGIONS:
        continue
    if r.get("is_event_rep") != "True":
        continue
    faces = get_faces(r.get("full_text", ""))
    if not faces:
        continue
    mainland_rep_count += 1
    for toks in faces:
        if 2 <= len(toks) <= 8:
            mainland_home_seals.append(toks)
        for a, b in zip(toks, toks[1:]):
            mainland_adj[(a, b)] += 1
        # Ordered pairs (all distinct pairs in face)
        for i in range(len(toks)):
            for j in range(i + 1, len(toks)):
                if toks[i] != toks[j]:
                    mainland_ord[(toks[i], toks[j])] += 1

def score_direction_mainland(toks):
    fwd_adj = sum(mainland_adj[(a, b)] for a, b in zip(toks, toks[1:]))
    rev_adj = sum(mainland_adj[(b, a)] for a, b in zip(toks, toks[1:]))
    fwd_ord = sum(mainland_ord[(toks[i], toks[j])] for i in range(len(toks)) for j in range(i + 1, len(toks)) if toks[i] != toks[j])
    rev_ord = sum(mainland_ord[(toks[j], toks[i])] for i in range(len(toks)) for j in range(i + 1, len(toks)) if toks[i] != toks[j])
    p_adj = binom_two_sided(fwd_adj, fwd_adj + rev_adj)
    p_ord = binom_two_sided(fwd_ord, fwd_ord + rev_ord)
    return fwd_adj, rev_adj, p_adj, fwd_ord, rev_ord, p_ord

# =============================================================================
# TEST 3B-1: PHYSICAL SEAL FACE VS. CLAY IMPRESSION & ANIMAL-COMPASS AUDIT
# =============================================================================
print("=" * 78)
print("TEST 3B-1: PHYSICAL SEAL FACE VS. IMPRESSION & ANIMAL-COMPASS AUDIT (N=48)")
print("=" * 78)

# Direct visual audit observations verified on Gadd (1932) Plates I-III (33779.pdf pp. 14, 20, 26)
# and Laursen (2010) Figs. 8, 9, 11 (AAE 21:96-134).
# Fields: (plate_source, depicts_what, animal_motif, animal_facing_impression, animal_facing_stone, physical_note)
PHYSICAL_PLATE_AUDIT = {
    # Bahrain (Laursen Fig. 9 & Fig. 11)
    "G3-B01": ("Laursen 2010 Fig.9 #6 / Kjaerum 1994 #1726", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Intact bull faces RIGHT on impression; upper-left text broken after 091"),
    "G3-B02": ("Laursen 2010 Fig.9 #7 & Fig.11 #7 / Kjaerum 1994 #1725", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; Key#1 read R->L 160-090-055-060-190; Lipi stored L->R 190-060-055-090-160 (rev_ord 18:3 p=0.0015)"),
    "G3-B03": ("Laursen 2010 Fig.9 #8 & Fig.11 #8 / Srivastava 1991 #55", "clay_impression", "short-horned bull + bird", "RIGHT", "LEFT", "Both bull and bird face RIGHT on impression; standard R->L text"),
    "G3-B04": ("Laursen 2010 Fig.9 #9 & Fig.11 #9 / Al-Sindi 182", "clay_impression", "none (text-only)", "NA", "NA", "Text-only round seal (no animal motif); standard R->L 055-220-091-001-093-031"),
    "G3-B05": ("Laursen 2010 Fig.1a, Fig.9 #10 & Fig.11 #10", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; Parpola reads R->L"),
    "G3-B06": ("Laursen 2010 Fig.1b, Fig.9 #11 & Fig.11 #11", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; standard R->L 091-032-034"),
    "G3-B07": ("Laursen 2010 Fig.9 #56 / Al-Sindi 160 / BBM 20362", "clay_impression", "large bull + small inverted bull", "RIGHT", "LEFT", "Main lower bull faces RIGHT on impression (small upper inverted bull faces LEFT); flanking 740-740 symmetric"),
    # Failaka & UAE
    "G3-F01": ("Laursen 2010 Fig.9 #12 & Fig.11 #12 / Kjaerum 1983 #319", "clay_impression", "fragmentary/broken", "BROKEN", "BROKEN", "Lower field broken away; upper arc 090-001-761-890"),
    "G3-F02": ("Laursen 2010 Fig.9 #13 & Fig.11 #13 / Kjaerum 1983 #279", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "DECOUPLED POSITIVE-SCRIPT CUT: bull faces RIGHT on impression (negative cut on stone), while 2-register Indus text reads L->R on impression (924-803-[061]-415-[220]-604-090; mainland 87:0 adj, 170:13 ord)!"),
    "G3-F03": ("Lipi 148.1 (Failaka round)", "catalogue_impression", "short-horned bull", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Not in Laursen Fig.9; mainland ord 17:4 forward (p=0.0072)"),
    "G3-F04": ("Laursen 2010 Fig.10i (Kalba UAE bifacial)", "clay_impression", "none/bifacial", "NA", "NA", "Single sign 091"),
    # Mesopotamia (Gadd 1932 Plates I-III + Laursen Fig.9 & Fig.11)
    "G3-M01": ("Gadd 1932 Pl.I #2 (BM 122187) & Laursen Fig.9 #16", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Gadd Pl.I #2 explicitly shows raised-relief clay impression; bull faces RIGHT"),
    "G3-M02": ("Gadd 1932 Pl.I #3 (BM 122946/U.17342) & Laursen Fig.9 #17", "clay_impression", "bull (lower broken)", "BROKEN", "BROKEN", "Gadd Pl.I #3 shows clay impression; bull body broken below"),
    "G3-M03": ("Gadd 1932 Pl.I #4 (BM 122188) & Laursen Fig.9 #18", "clay_impression", "broken (horns only)", "BROKEN", "BROKEN", "Gadd Pl.I #4 shows clay impression; only horns survive"),
    "G3-M04": ("Gadd 1932 Pl.I #5 (U.17341) & Laursen Fig.9 #19", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Gadd Pl.I #5 clay impression; bull faces RIGHT, right side of text broken"),
    "G3-M05": ("Gadd 1932 Pl.II #15 (Penn U.8685) & Laursen Fig.9 #20", "clay_impression", "spotted short-horned bull", "RIGHT", "LEFT", "Gadd Pl.II #15 clay impression; spotted bull faces RIGHT"),
    "G3-M06": ("Gadd 1932 Pl.III #16 (BM 123208/U.17649, PG 1847) & Laursen Fig.9 #21", "clay_impression", "short-horned bull (Gaur)", "RIGHT", "LEFT", "DECOUPLED POSITIVE-SCRIPT CUT: Gadd Pl.III #16 clay impression photo confirms Gaur bull faces RIGHT (negative cut), while text reads L->R on impression (002-004-328-001-803-415 / Mah 015-717-001-803-415; mainland 35:0 adj, 128:18 ord)!"),
    "G3-M07": ("Sarzec & Heuzey pl.30.3 (Girsu) & Laursen Fig.9 #22", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; standard R->L confirmed 94:2 ord (p=1.18e-25)"),
    "G3-M08": ("Gadd 1932 Pl.III #17 (BM 120228) & Laursen Fig.9 #23", "clay_impression", "short-horned bull + manger", "RIGHT", "LEFT", "KEY2B ARTIFACT FIXED: Gadd Pl.III #17 clay impression shows bull facing RIGHT over Harappan manger & twin 740 jars at FAR LEFT (standard R->L 467-798-001-740-740; fwd_ord 316:58 p=4.3e-44)! Key2B rev_adj 27:4 was 740-001 reverse artifact — DO NOT FLIP!"),
    "G3-M09": ("Gadd 1932 Pl.III #18 (BM 129059) & Laursen Fig.9 #24", "both_stone_and_impression", "mating bull & cow", "LEFT", "RIGHT", "SOLE ANIMAL-LEFT EXCEPTION (1/20 = 5.0%): Gadd Pl.III #18 shows BOTH stone face (left, bulls RIGHT) and clay impression (right, bulls LEFT); Laursen Fig.9 #24 matches the impression!"),
    "G3-M10": ("Langdon 1932 p.48 & Laursen Fig.9 #25 & Fig.11 #25", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; standard R->L supported 46:28 ord (p=0.047)"),
    "G3-M11": ("Buchanan 1967/1981 #1088 (Yale Newell 23) & Laursen Fig.9 #26", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; standard R->L 160-384-133-001-090-061 confirmed 26:8 ord (p=0.0029)"),
    "G3-M12": ("Buchanan 1967/1981 #1089 (Yale Newell 876) & Laursen Fig.9 #27", "clay_impression", "water-bird / goose", "RIGHT", "LEFT", "DECOUPLED POSITIVE-SCRIPT CUT: Bird at bottom faces RIGHT toward leaf & horned quadruped sign 340 at top-left also faces RIGHT, while text reads L->R on impression (340-002-090-725-061; mainland 48:7 ord p=1.31e-8), locking 090...061 with Yale #26!"),
    # Iran
    "G3-I01": ("Amiet 1972 #1643 (Susa) & Laursen Fig.9 #14 & Fig.11 #14", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; standard R->L (7:2 ord)"),
    "G3-I02": ("Amiet 1973 pl.23 (Luristan) & Laursen Fig.9 #15 & Fig.11 #15", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; standard R->L (3:0 ord)"),
    "G3-I03": ("Amiet 1972 (Susa cylinder, Lipi 3882.1)", "clay_impression", "Indus bull (cylinder)", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Cylinder impression; ambiguous mainland order (70:78)"),
    "G3-I04": ("VDF 2021 NMI 2698 (Jalalabad cylinder)", "clay_impression", "Jiroft snake-man (cylinder)", "NA", "NA", "Standard forward confirmed 10:0 adj, 82:19 ord (p=1.66e-10)"),
    "G3-I05": ("BM 1960,0718.1.1 (Sistan cylinder)", "clay_impression", "bull/animal (cylinder)", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Cylinder impression; mildly reversed ord (3:11 p=0.057, below threshold)"),
    "G3-I06": ("Winkelmann 1999 / Laursen Fig.9 #28 (W. Iran Ligabue)", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; Linear Elamite reads R->L za-si-ri2 (Desset 2026)"),
    # Unknown WA/Gulf
    "G3-U01": ("Lipi 3887.1 (Unknown WA round)", "catalogue_impression", "unknown", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Short/incomplete; 2:0 adj, 3:0 ord forward"),
    "G3-U02": ("Lipi 3888.1 (Unknown WA cylinder)", "catalogue_impression", "unknown", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Cylinder; forward confirmed 26:3 ord (p=1.52e-5)"),
    "G3-U03": ("Lipi 5557.1 (Unknown WA cylinder)", "catalogue_impression", "unknown", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Fragmentary cylinder"),
    "G3-U04": ("Mahadevan M9904 (West Asia round)", "catalogue_impression", "unknown", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Ambiguous (0:0)"),
    "G3-U05": ("Mahadevan M9905 (West Asia round)", "catalogue_impression", "unknown", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Ambiguous (1:1)"),
    # Indus Home Round (Laursen Fig. 8)
    "G3-H01": ("Laursen 2010 Fig.8 #1 (Chanhu-daro C-32)", "clay_impression", "unicorn", "RIGHT", "LEFT", "Unicorn faces RIGHT on impression; forward 5:0 adj"),
    "G3-H02": ("Laursen 2010 Fig.9 #2 (Mohenjo-daro M-416)", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; forward 7:0 adj (p=0.0156)"),
    "G3-H03": ("Laursen 2010 Fig.8 #3 (Mohenjo-daro M-1369)", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; strong forward 36:2 adj, 212:26 ord (p=1.9e-37)"),
    "G3-H04": ("Laursen 2010 Fig.8 #4 (Mohenjo-daro M-417)", "clay_impression", "6-head animal whorl", "NA", "NA", "Radial 6-head whorl (no single facing direction); fragmentary text"),
    "G3-H05": ("Laursen 2010 Fig.8 #5 (Mohenjo-daro M-415)", "clay_impression", "short-horned bull", "RIGHT", "LEFT", "Bull faces RIGHT on impression; forward 1:0"),
    "G3-H06": ("Lipi 4247.1 (Dholavira Gulf-type round)", "catalogue_impression", "unknown/broken", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Strong forward 13:1 adj (p=0.0018)"),
    # Abroad Square Harappan Controls
    "G3-S01": ("Lipi 1971.1 (Kish square unicorn)", "catalogue_impression", "unicorn", "RIGHT", "LEFT", "Classic Harappan square seal; strong forward 164:2 adj, 850:67 ord (p=1.4e-173)"),
    "G3-S02": ("Lipi 1970.1 (Kish square unicorn)", "catalogue_impression", "unicorn", "RIGHT", "LEFT", "Classic Harappan square seal; forward 2:0"),
    "G3-S03": ("Lipi 3884.1 (Tell Umma clay bale tag)", "clay_impression", "none (clay tag)", "NA", "NA", "Ancient clay sealing impression; strong forward 44:12 adj, 132:63 ord (p=8.7e-7)"),
    "G3-S04": ("Lipi 3885.1 (Tello/Girsu square tiger)", "catalogue_impression", "tiger/bull", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Square control; mildly reversed ord 6:24 (p=0.0014; broken final 000)"),
    "G3-S05": ("Lipi 4155.1 (Gonur Depe square elephant)", "catalogue_impression", "elephant", "RIGHT", "LEFT", "Classic Harappan square seal; strong forward 185:12 adj, 1292:113 ord"),
    "G3-S06": ("Lipi 4173.1 (Salut Oman square bull)", "catalogue_impression", "short-horned bull", "RIGHT", "LEFT", "Classic Harappan square seal; strong forward 20:0 adj, 28:4 ord"),
    "G3-S07": ("Mahadevan M9851 (West Asia square)", "catalogue_impression", "unicorn/bull", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Strong forward 8:0 adj (p=0.0078)"),
    "G3-S08": ("Mahadevan M9842 (West Asia square)", "catalogue_impression", "unicorn/bull", "UNVERIFIED_PLATE", "UNVERIFIED_PLATE", "Forward 1:0"),
}

# Strict vs Expanded flip sets
STRICT_FLIP_UIDS = {"G3-F02", "G3-M06", "G3-M12"}          # Failaka #13, Ur #21, Yale #27
EXTENDED_FLIP_UIDS = STRICT_FLIP_UIDS | {"G3-B02"}         # + Qala'at #7 (restored to Lipi L->R 190-060-055-090-160)

audit_rows = []
laursen_animal_right = 0
laursen_animal_left = 0
abroad_animal_right = 0
abroad_animal_left = 0
gulf_round_tested = 0
gulf_round_strict_rev = 0
gulf_round_ext_rev = 0

for r in GULF_VERIFIED:
    uid = r["uid"]
    toks = parse_toks(r["seq_verified"])
    rev_toks = list(reversed(toks))
    fa, ra, pa, fo, ro, po = score_direction_mainland(toks)
    plate_src, depicts, motif, face_imp, face_stone, pnote = PHYSICAL_PLATE_AUDIT[uid]

    # Count Laursen Figs. 8-9 visually audited intact animal round seals
    if r["laursen"] and face_imp in ("RIGHT", "LEFT"):
        if face_imp == "RIGHT":
            laursen_animal_right += 1
        else:
            laursen_animal_left += 1
        if r["region"] in ("Persian Gulf", "Mesopotamia", "Iranian Plateau", "Mesopotamia/Gulf"):
            if face_imp == "RIGHT":
                abroad_animal_right += 1
            else:
                abroad_animal_left += 1

    # Clean direction verdict (fixing Key #2B's Gadd 17 false-positive!)
    if uid in STRICT_FLIP_UIDS:
        verdict = "CONFIRMED_REVERSED_POSITIVE_CUT"
        mech = "DECOUPLED_POSITIVE_SCRIPT_CUT (animal negative -> RIGHT; script positive -> L->R on clay, like KM 1650)"
        rec_seq = "-".join(rev_toks)
    elif uid == "G3-M08":
        verdict = "CONFIRMED_FORWARD_RL (Gadd17_rev_adj_artifact_fixed)"
        mech = "STANDARD_NEGATIVE_CUT (bull RIGHT, twin 740 jars at far LEFT = final; fwd_ord 316:58 p=4.3e-44)"
        rec_seq = r["seq_verified"]
    elif uid == "G3-B02":
        verdict = "TENSION_ORDER_REVERSED (Qalaat7_Key1_vs_Lipi)"
        mech = "BULL_RIGHT_SCRIPT_TENSION (bull RIGHT; R->L=160-090-055-060-190 fits Gulf calque; L->R=190-060-055-090-160 fits mainland ord 18:3 p=0.0015)"
        rec_seq = r["seq_verified"]  # strict keeps Key #1 R->L; Regime B tests flipped
    elif uid == "G3-S04":
        verdict = "REVERSED_ORDER_SQUARE_CONTROL"
        mech = "SQUARE_CONTROL_TENSION (broken final sign; ord 6:24 p=0.0014)"
        rec_seq = r["seq_verified"]
    elif (pa < 0.05 and fa > ra) or (po < 0.05 and fo > ro):
        verdict = "CONFIRMED_FORWARD_RL"
        mech = "STANDARD_NEGATIVE_CUT"
        rec_seq = r["seq_verified"]
    else:
        verdict = "AMBIGUOUS_KEEP_RL"
        mech = "STANDARD_NEGATIVE_CUT_ASSUMED"
        rec_seq = r["seq_verified"]

    if r["region"] in ("Persian Gulf", "Mesopotamia", "Iranian Plateau", "Mesopotamia/Gulf") and r["shape"] == "round" and r["seq_verified"] != "LE:za-si-ri2" and len(toks) >= 2:
        gulf_round_tested += 1
        if uid in STRICT_FLIP_UIDS:
            gulf_round_strict_rev += 1
        if uid in EXTENDED_FLIP_UIDS:
            gulf_round_ext_rev += 1

    audit_rows.append({
        "uid": uid,
        "laursen": r["laursen"],
        "gadd": r["gadd"],
        "lipi": r["lipi"],
        "site": r["site"],
        "region": r["region"],
        "shape": r["shape"],
        "plate_source": plate_src,
        "depicts_face_or_impression": depicts,
        "animal_motif": motif,
        "animal_facing_on_impression": face_imp,
        "animal_facing_on_stone": face_stone,
        "seq_key1_rl": r["seq_verified"],
        "seq_flipped_lr": "-".join(rev_toks) if toks else r["seq_verified"],
        "mainland_fwd_adj": fa,
        "mainland_rev_adj": ra,
        "p_adj": f"{pa:.3e}",
        "mainland_fwd_ord": fo,
        "mainland_rev_ord": ro,
        "p_ord": f"{po:.3e}",
        "direction_verdict": verdict,
        "physical_mechanism": mech,
        "recommended_aligned_seq": rec_seq,
        "notes": pnote,
    })

with open(OUT_DIR / "gulf_orientation_physical_audit.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(audit_rows[0].keys()))
    w.writeheader()
    w.writerows(audit_rows)

# Compare Gulf animal-facing RIGHT rate vs Mainland Konasukawa (2011) baseline (1,728 / 1,783 = 96.9%)
# and Gulf L->R positive-script rate vs Fuls (2022) Table 2.5 mainland L->R rate (215 / 4,476 = 4.80% of directional texts)
anim_tot = laursen_animal_right + laursen_animal_left
abroad_anim_tot = abroad_animal_right + abroad_animal_left
or_anim, p_anim_two, _ = fisher_exact_two_sided(laursen_animal_right, laursen_animal_left, 1728, 55)
or_ab_anim, p_ab_anim_two, _ = fisher_exact_two_sided(abroad_animal_right, abroad_animal_left, 1728, 55)
or_rev_strict, p_rev_strict_two, p_rev_strict_gt = fisher_exact_two_sided(gulf_round_strict_rev, gulf_round_tested - gulf_round_strict_rev, 215, 4261)
or_rev_ext, p_rev_ext_two, p_rev_ext_gt = fisher_exact_two_sided(gulf_round_ext_rev, gulf_round_tested - gulf_round_ext_rev, 215, 4261)

t3b1_summary = {
    "total_seals_audited": len(audit_rows),
    "laursen_intact_animal_round_seals": anim_tot,
    "animal_facing_right_on_impression": laursen_animal_right,
    "animal_facing_left_on_impression": laursen_animal_left,
    "gulf_animal_right_pct": round(100 * laursen_animal_right / anim_tot, 1),
    "abroad_only_intact_animal_round_seals": abroad_anim_tot,
    "abroad_animal_facing_right": abroad_animal_right,
    "abroad_animal_facing_left": abroad_animal_left,
    "abroad_animal_right_pct": round(100 * abroad_animal_right / abroad_anim_tot, 1),
    "abroad_animal_compass_vs_mainland_fisher": {"odds_ratio": round(or_ab_anim, 3), "p_two_sided": round(p_ab_anim_two, 4)},
    "sole_animal_left_exception": "G3-M09 (Gadd 18 / BM 129059 / Laursen #24 — verified directly on Gadd Pl. III #18 showing BOTH stone face and impression)",
    "mainland_animal_right_baseline_konasukawa2011": {"right": 1728, "left": 55, "total": 1783, "pct": 96.9},
    "animal_compass_vs_mainland_fisher": {"odds_ratio": round(or_anim, 3), "p_two_sided": round(p_anim_two, 4)},
    "gulf_round_directional_tested": gulf_round_tested,
    "strict_reversed_positive_script": {"count": gulf_round_strict_rev, "uids": sorted(STRICT_FLIP_UIDS), "pct": round(100 * gulf_round_strict_rev / gulf_round_tested, 1)},
    "extended_reversed_incl_qalaat7": {"count": gulf_round_ext_rev, "uids": sorted(EXTENDED_FLIP_UIDS), "pct": round(100 * gulf_round_ext_rev / gulf_round_tested, 1)},
    "mainland_lr_baseline_fuls2022_table2_5": {"lr": 215, "rl_and_other_dir": 4261, "total_directional": 4476, "pct": 4.8},
    "strict_rev_vs_mainland_fisher": {"odds_ratio": round(or_rev_strict, 2), "p_greater": round(p_rev_strict_gt, 4), "p_two_sided": round(p_rev_strict_two, 4)},
    "extended_rev_vs_mainland_fisher": {"odds_ratio": round(or_rev_ext, 2), "p_greater": round(p_rev_ext_gt, 4), "p_two_sided": round(p_rev_ext_two, 4)},
    "gadd17_fix_note": "G3-M08 (Gadd 17 / BM 120228) is 100% standard R->L (fwd_ord 316:58 p=4.29e-44; Gadd Pl. III #17 confirms twin 740 jars at far LEFT and bull facing RIGHT over manger). Key #2B's STRONG_REVERSED tag was a 740-001 reverse-adjacency artifact.",
}

with open(OUT_DIR / "test3b1_orientation_summary.json", "w", encoding="utf-8") as f:
    json.dump(t3b1_summary, f, indent=2)

print(f"  All Laursen intact animal round seals: {laursen_animal_right}/{anim_tot} ({t3b1_summary['gulf_animal_right_pct']}%) RIGHT on impression (Fisher P={p_anim_two:.4f})")
print(f"  Abroad-only Gulf intact animal seals:  {abroad_animal_right}/{abroad_anim_tot} ({t3b1_summary['abroad_animal_right_pct']}%) RIGHT on impression (Fisher P={p_ab_anim_two:.4f} vs Mainland 1,728/1,783 = 96.9%)")
print(f"    Sole exception: Gadd 18 (BM 129059) — verified on Gadd Pl. III #18 showing BOTH stone (RIGHT) & impression (LEFT).")
print(f"  Decoupled Positive-Script Rate (bull RIGHT on clay, text L->R on clay):")
print(f"    Strict (Failaka #13, Ur #21, Yale #27): {gulf_round_strict_rev}/{gulf_round_tested} ({t3b1_summary['strict_reversed_positive_script']['pct']}%) vs Mainland Fuls 215/4,476 (4.8%) -> OR={or_rev_strict:.2f}, P_gt={p_rev_strict_gt:.4f}")
print(f"    Extended (+ Qala'at #7):                {gulf_round_ext_rev}/{gulf_round_tested} ({t3b1_summary['extended_reversed_incl_qalaat7']['pct']}%) vs Mainland Fuls 215/4,476 (4.8%) -> OR={or_rev_ext:.2f}, P_gt={p_rev_ext_gt:.4f}")
print(f"  Gadd 17 (G3-M08) false-positive fixed: fwd_ord=316 vs rev_ord=58 (p=4.29e-44) + Gadd Pl. III #17 -> KEEP FORWARD!")


# =============================================================================
# TEST 3B-2: RE-RUN KEY #1'S VENTRIS NETWORK & GULF CALQUE BEFORE VS AFTER
# =============================================================================
print("\n" + "=" * 78)
print("TEST 3B-2: RE-ALIGNED VENTRIS NETWORK, GULF CALQUE & BIGRAM GRADIENT")
print("=" * 78)

# Exact Key #1 definitions from work_scripts/gulf3_key1_decipher.py & gulf3_audit_and_ventris.py
MAN_SIGNS_CALQUE = {"090", "091", "093", "095", "099", "121", "133", "139", "145", "160"}
MAN_SET_AUDIT2 = {"090", "091", "093", "095", "099", "121", "133", "145", "160"}
COSMO_NONFISH = {"190", "924", "604", "603", "405", "407", "413", "340"}
COSMO_ALL = COSMO_NONFISH | {"220", "235", "255"}
STROKE_NUMS = {"001", "002", "003", "004", "013", "031", "032", "033", "034"}

def has_twin_man(toks):
    if "091" in toks:
        return True
    return any(toks[i] in MAN_SIGNS_CALQUE and toks[i + 1] in MAN_SIGNS_CALQUE for i in range(len(toks) - 1))

def classify_calque(toks):
    if len(toks) < 2:
        return "single_sign"
    if toks[0] in MAN_SIGNS_CALQUE:
        if "001" in toks[1:-1]:
            return "head_man_plus_DISZ_bipartite"
        return "head_initial_LU_man"
    if "001" in toks[1:-1]:
        return "DISZ_bipartite"
    if any(t in MAN_SIGNS_CALQUE for t in toks):
        return "medial_or_final_man"
    return "other"

def order_stats(seqs, cset):
    mf_s = df_s = mf_p = tot_p = 0
    for seq in seqs:
        m_pos = [i for i, t in enumerate(seq) if t in MAN_SET_AUDIT2]
        c_pos = [i for i, t in enumerate(seq) if t in cset]
        if not m_pos or not c_pos:
            continue
        if min(m_pos) < min(c_pos):
            mf_s += 1
        else:
            df_s += 1
        for mi in m_pos:
            for ci in c_pos:
                tot_p += 1
                if mi < ci:
                    mf_p += 1
    return mf_s, df_s, mf_p, tot_p

# Pre-build length-matched mainland null pool for calque grammar (1,000 draws, deterministic)
by_len_home = collections.defaultdict(list)
for hs in mainland_home_seals:
    by_len_home[len(hs)].append(hs)
all_home_pool = [hs for hs in mainland_home_seals if 2 <= len(hs) <= 8]

def run_regime(name: str, flip_uids: set):
    rng = random.Random(SEED)
    # Prepare sequences for all 48 seals under this regime
    rows_reg = []
    for r in GULF_VERIFIED:
        toks = parse_toks(r["seq_verified"])
        if r["uid"] in flip_uids:
            toks = list(reversed(toks))
        rows_reg.append((r, toks))

    abroad_rc = [(r, toks) for r, toks in rows_reg
                 if r["region"] in ("Persian Gulf", "Mesopotamia", "Iranian Plateau", "Mesopotamia/Gulf")
                 and r["seq_verified"] != "LE:za-si-ri2" and r["shape"] in ("round", "cylinder")
                 and len(toks) >= 2]
    gulf_seqs = [toks for _, toks in abroad_rc]
    n_g = len(gulf_seqs)

    # 1. Gulf Calque Grammar Fit
    n_head_man = sum(1 for t in gulf_seqs if t[0] in MAN_SIGNS_CALQUE)
    n_final_man = sum(1 for t in gulf_seqs if t[-1] in MAN_SIGNS_CALQUE)
    n_any_man = sum(1 for t in gulf_seqs if any(x in MAN_SIGNS_CALQUE for x in t))
    n_twin = sum(1 for t in gulf_seqs if has_twin_man(t))
    n_disz = sum(1 for t in gulf_seqs if "001" in t[1:-1])
    n_calque = sum(1 for t in gulf_seqs if classify_calque(t) != "other")

    null_hm, null_tw, null_di = [], [], []
    for _ in range(1000):
        samp = [rng.choice(by_len_home.get(len(t), all_home_pool)) for t in gulf_seqs]
        null_hm.append(sum(1 for h in samp if h[0] in MAN_SIGNS_CALQUE))
        null_tw.append(sum(1 for h in samp if has_twin_man(h)))
        null_di.append(sum(1 for h in samp if "001" in h[1:-1]))
    mu_hm, sd_hm, z_hm, p_hm, _ = z_and_p(n_head_man, null_hm)
    mu_tw, sd_tw, z_tw, p_tw, _ = z_and_p(n_twin, null_tw)
    mu_di, sd_di, z_di, p_di, _ = z_and_p(n_disz, null_di)

    # 2. MAN -> COSMO Directional Order Test (5,000 shuffles inside each seal)
    mf_all, df_all, mfp_all, tp_all = order_stats(gulf_seqs, COSMO_ALL)
    mf_nf, df_nf, mfp_nf, tp_nf = order_stats(gulf_seqs, COSMO_NONFISH)
    null_mfa, null_mfpa, null_mfnf, null_mfpnf = [], [], [], []
    for _ in range(5000):
        rseqs = [rng.sample(seq, len(seq)) for seq in gulf_seqs]
        s_a = order_stats(rseqs, COSMO_ALL)
        s_n = order_stats(rseqs, COSMO_NONFISH)
        null_mfa.append(s_a[0])
        null_mfpa.append(s_a[2])
        null_mfnf.append(s_n[0])
        null_mfpnf.append(s_n[2])

    mu_mfa, _, z_mfa, p_mfa, _ = z_and_p(mf_all, null_mfa)
    mu_mfpa, _, z_mfpa, p_mfpa, _ = z_and_p(mfp_all, null_mfpa)
    mu_mfnf, _, z_mfnf, p_mfnf, _ = z_and_p(mf_nf, null_mfnf)
    mu_mfpnf, _, z_mfpnf, p_mfpnf, _ = z_and_p(mfp_nf, null_mfpnf)

    # Exact per-seal MAN vs COSMO_NONFISH details
    nf_details = []
    for r, seq in abroad_rc:
        ms = [(i, t) for i, t in enumerate(seq) if t in MAN_SET_AUDIT2]
        cs = [(i, t) for i, t in enumerate(seq) if t in COSMO_NONFISH]
        if ms and cs:
            nf_details.append({
                "uid": r["uid"],
                "site": r["site"],
                "seq": "-".join(seq),
                "order": "MAN->COSMO" if ms[0][0] < cs[0][0] else "COSMO->MAN",
            })

    # 3. Ventris Pair-Lock Network (unordered >=2 shared non-stroke signs + DIRECTED order agreement!)
    pair_locks = []
    same_order_locks = 0
    reversed_order_locks = 0
    same_order_contiguous = 0
    for i in range(len(abroad_rc)):
        r1, t1 = abroad_rc[i]
        lex1 = [x for x in t1 if x not in STROKE_NUMS]
        s1 = set(lex1)
        for j in range(i + 1, len(abroad_rc)):
            r2, t2 = abroad_rc[j]
            lex2 = [x for x in t2 if x not in STROKE_NUMS]
            sh = sorted(s1 & set(lex2))
            if len(sh) >= 2:
                # Check directed order consistency of shared signs (first occurrence of each shared sign)
                ord1 = sorted(sh, key=lambda x: t1.index(x))
                ord2 = sorted(sh, key=lambda x: t2.index(x))
                same_ord = (ord1 == ord2)
                if same_ord:
                    same_order_locks += 1
                else:
                    reversed_order_locks += 1
                # Check if shared pair is contiguous in at least one and same-order in both
                bg1 = set(zip(t1, t1[1:]))
                bg2 = set(zip(t2, t2[1:]))
                sh_pair = (ord1[0], ord1[1])
                contig_both = (sh_pair in bg1 and sh_pair in bg2)
                if same_ord and (sh_pair in bg1 or sh_pair in bg2):
                    same_order_contiguous += 1
                pair_locks.append({
                    "seal1": r1["uid"], "site1": r1["site"], "seq1": "-".join(t1),
                    "seal2": r2["uid"], "site2": r2["site"], "seq2": "-".join(t2),
                    "shared": "|".join(sh),
                    "order1": "->".join(ord1), "order2": "->".join(ord2),
                    "same_order": same_ord,
                    "contig_both": contig_both,
                })

    # Exact binomial test on Ventris pair-lock directional agreement!
    p_ventris_dir = binom_two_sided(same_order_locks, len(pair_locks))

    # Exact repeated contiguous 2-sign bigrams (non-stroke-only)
    bg_sites = collections.defaultdict(list)
    for r, toks in abroad_rc:
        for a, b in zip(toks, toks[1:]):
            if a in STROKE_NUMS and b in STROKE_NUMS:
                continue
            bg_sites[f"{a}-{b}"].append(f"{r['uid']}({r['site']})")
    rep_bigrams = {k: v for k, v in bg_sites.items() if len(v) >= 2}

    # 4. Mainland Bigram Support & Ordered-Pair Support Gradient across Seal Groups
    grp_defs = [
        ("Indus_Home_Round", lambda r: r["group"].startswith("Laursen_G1") or "Indus" in r["group"] or "Dholavira" in r["group"]),
        ("Abroad_Square", lambda r: r["group"] == "Abroad_Square"),
        ("Bahrain_Failaka", lambda r: "Bahrain" in r["group"] or "Failaka" in r["group"]),
        ("Iran_Round_Cyl", lambda r: r["group"].startswith("Laursen_G2") or "Iran" in r["group"]),
        ("Mesopotamia_Ur_Round", lambda r: "Mesopotamia" in r["group"]),
    ]
    gradient = {}
    for gname, pred in grp_defs:
        sub = [(r, toks) for r, toks in rows_reg if pred(r) and r["seq_verified"] != "LE:za-si-ri2" and len(toks) >= 2]
        bg_rates = []
        ord_rates = []
        zero_bg = 0
        tot_fwd_adj = 0
        tot_rev_adj = 0
        tot_fwd_ord = 0
        tot_rev_ord = 0
        for r, toks in sub:
            bgs = list(zip(toks, toks[1:]))
            sup = sum(1 for a, b in bgs if mainland_adj[(a, b)] > 0)
            bg_rates.append(sup / len(bgs))
            if sup == 0:
                zero_bg += 1
            fa, ra, _, fo, ro, _ = score_direction_mainland(toks)
            tot_fwd_adj += fa
            tot_rev_adj += ra
            tot_fwd_ord += fo
            tot_rev_ord += ro
            ord_rates.append(fo / (fo + ro) if (fo + ro) > 0 else 0.5)
        gradient[gname] = {
            "n": len(sub),
            "mean_bg_support_pct": round(100 * sum(bg_rates) / len(bg_rates), 1) if bg_rates else 0.0,
            "zero_bg_support": f"{zero_bg}/{len(sub)}",
            "tot_fwd_adj": tot_fwd_adj,
            "tot_rev_adj": tot_rev_adj,
            "tot_fwd_ord": tot_fwd_ord,
            "tot_rev_ord": tot_rev_ord,
            "ord_fwd_pct": round(100 * tot_fwd_ord / (tot_fwd_ord + tot_rev_ord), 1) if (tot_fwd_ord + tot_rev_ord) > 0 else 0.0,
        }

    # Key focal seal diagnostics
    focal = {}
    for uid in ("G3-F02", "G3-M06", "G3-M12", "G3-M11", "G3-B02", "G3-M08"):
        for r, toks in rows_reg:
            if r["uid"] == uid:
                fa, ra, pa, fo, ro, po = score_direction_mainland(toks)
                bgs = list(zip(toks, toks[1:]))
                sup = sum(1 for a, b in bgs if mainland_adj[(a, b)] > 0)
                focal[uid] = {
                    "site": r["site"],
                    "seq": "-".join(toks),
                    "bg_supported": f"{sup}/{len(bgs)}",
                    "fwd_adj": fa, "rev_adj": ra, "fwd_ord": fo, "rev_ord": ro,
                }

    return {
        "regime": name,
        "flipped_uids": sorted(flip_uids),
        "n_gulf_abroad": n_g,
        "calque_grammar": {
            "head_initial_man": n_head_man, "head_man_z": round(z_hm, 2), "head_man_p": round(p_hm, 4),
            "final_man": n_final_man,
            "any_man": n_any_man,
            "twin_man": n_twin, "twin_z": round(z_tw, 2),
            "disz_001_divider": n_disz, "disz_z": round(z_di, 2),
            "total_calque_fit": n_calque, "total_calque_pct": round(100 * n_calque / n_g, 1),
        },
        "man_to_cosmo_order": {
            "all_seals": f"{mf_all}/{mf_all + df_all}", "all_seals_pct": round(100 * mf_all / (mf_all + df_all), 1),
            "all_seals_z": round(z_mfa, 2), "all_seals_p": round(p_mfa, 4),
            "all_pairs": f"{mfp_all}/{tp_all}", "all_pairs_pct": round(100 * mfp_all / tp_all, 1),
            "all_pairs_z": round(z_mfpa, 2), "all_pairs_p": round(p_mfpa, 4),
            "nonfish_seals": f"{mf_nf}/{mf_nf + df_nf}", "nonfish_seals_pct": round(100 * mf_nf / (mf_nf + df_nf), 1),
            "nonfish_seals_z": round(z_mfnf, 2), "nonfish_seals_p": round(p_mfnf, 4),
            "nonfish_pairs": f"{mfp_nf}/{tp_nf}", "nonfish_pairs_pct": round(100 * mfp_nf / tp_nf, 1),
            "nonfish_pairs_z": round(z_mfpnf, 2), "nonfish_pairs_p": round(p_mfpnf, 4),
            "nonfish_details": nf_details,
        },
        "ventris_network": {
            "n_pair_locks": len(pair_locks),
            "same_order_locks": same_order_locks,
            "reversed_order_locks": reversed_order_locks,
            "same_order_pct": round(100 * same_order_locks / len(pair_locks), 1) if pair_locks else 0.0,
            "same_order_binom_p": round(p_ventris_dir, 4),
            "same_order_with_contiguity": same_order_contiguous,
            "repeated_contiguous_bigrams": rep_bigrams,
            "pair_locks": pair_locks,
        },
        "mainland_gradient": gradient,
        "focal_seals": focal,
    }

reg_before = run_regime("BEFORE_KEY1", set())
reg_strict = run_regime("AFTER_STRICT_3FLIP", STRICT_FLIP_UIDS)
reg_ext = run_regime("AFTER_EXTENDED_4FLIP_QALAAT7", EXTENDED_FLIP_UIDS)

t3b2_all = {
    "regimes": [reg_before, reg_strict, reg_ext],
}
with open(OUT_DIR / "test3b2_realigned_ventris.json", "w", encoding="utf-8") as f:
    json.dump(t3b2_all, f, indent=2)

# Write clean BEFORE vs AFTER summary CSV
summary_rows = []
for rg in [reg_before, reg_strict, reg_ext]:
    cg = rg["calque_grammar"]
    mc = rg["man_to_cosmo_order"]
    vn = rg["ventris_network"]
    gr = rg["mainland_gradient"]
    summary_rows.append({
        "regime": rg["regime"],
        "flipped_uids": ";".join(rg["flipped_uids"]),
        "head_initial_man": f"{cg['head_initial_man']}/{rg['n_gulf_abroad']}",
        "final_man": f"{cg['final_man']}/{rg['n_gulf_abroad']}",
        "total_calque_fit": f"{cg['total_calque_fit']}/{rg['n_gulf_abroad']} ({cg['total_calque_pct']}%)",
        "man_to_cosmo_nonfish_seals": f"{mc['nonfish_seals']} ({mc['nonfish_seals_pct']}%, z={mc['nonfish_seals_z']}, P={mc['nonfish_seals_p']})",
        "man_to_cosmo_nonfish_pairs": f"{mc['nonfish_pairs']} ({mc['nonfish_pairs_pct']}%, z={mc['nonfish_pairs_z']}, P={mc['nonfish_pairs_p']})",
        "man_to_cosmo_all_seals": f"{mc['all_seals']} ({mc['all_seals_pct']}%, z={mc['all_seals_z']}, P={mc['all_seals_p']})",
        "ventris_same_order_locks": f"{vn['same_order_locks']}/{vn['n_pair_locks']} ({vn['same_order_pct']}%, P={vn['same_order_binom_p']})",
        "n_repeated_contig_bigrams": len(vn["repeated_contiguous_bigrams"]),
        "bahrain_failaka_bg_pct": gr["Bahrain_Failaka"]["mean_bg_support_pct"],
        "bahrain_failaka_ord_fwd_pct": gr["Bahrain_Failaka"]["ord_fwd_pct"],
        "mesopotamia_ur_bg_pct": gr["Mesopotamia_Ur_Round"]["mean_bg_support_pct"],
        "mesopotamia_ur_ord_fwd_pct": gr["Mesopotamia_Ur_Round"]["ord_fwd_pct"],
    })

with open(OUT_DIR / "test3b2_before_after_summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
    w.writeheader()
    w.writerows(summary_rows)

for rg in [reg_before, reg_strict, reg_ext]:
    cg = rg["calque_grammar"]
    mc = rg["man_to_cosmo_order"]
    vn = rg["ventris_network"]
    gr = rg["mainland_gradient"]
    print(f"\n  [{rg['regime']}] (flipped={rg['flipped_uids']})")
    print(f"    Calque fit: {cg['total_calque_fit']}/{rg['n_gulf_abroad']} ({cg['total_calque_pct']}%) | head-MAN={cg['head_initial_man']} (z={cg['head_man_z']}) | final-MAN={cg['final_man']}")
    print(f"    MAN->COSMO non-fish seals: {mc['nonfish_seals']} ({mc['nonfish_seals_pct']}%, z={mc['nonfish_seals_z']:+.2f}, P={mc['nonfish_seals_p']:.4f}) | pairs: {mc['nonfish_pairs']} ({mc['nonfish_pairs_pct']}%, z={mc['nonfish_pairs_z']:+.2f}, P={mc['nonfish_pairs_p']:.4f})")
    print(f"    MAN->COSMO ALL seals:      {mc['all_seals']} ({mc['all_seals_pct']}%, z={mc['all_seals_z']:+.2f}, P={mc['all_seals_p']:.4f}) | pairs: {mc['all_pairs']} ({mc['all_pairs_pct']}%, z={mc['all_pairs_z']:+.2f}, P={mc['all_pairs_p']:.4f})")
    print(f"    Ventris pair-locks SAME-ORDER: {vn['same_order_locks']}/{vn['n_pair_locks']} ({vn['same_order_pct']}%, binom P={vn['same_order_binom_p']:.4f}) | repeated contig bigrams={len(vn['repeated_contiguous_bigrams'])}: {list(vn['repeated_contiguous_bigrams'].keys())}")
    print(f"    Mainland BG support: HomeRound={gr['Indus_Home_Round']['mean_bg_support_pct']}% | AbrSq={gr['Abroad_Square']['mean_bg_support_pct']}% | Bah/Fail={gr['Bahrain_Failaka']['mean_bg_support_pct']}% (ord_fwd={gr['Bahrain_Failaka']['ord_fwd_pct']}%) | Iran={gr['Iran_Round_Cyl']['mean_bg_support_pct']}% | Meso/Ur={gr['Mesopotamia_Ur_Round']['mean_bg_support_pct']}% (ord_fwd={gr['Mesopotamia_Ur_Round']['ord_fwd_pct']}%)")
    for pl in vn["pair_locks"]:
        if "G3-F02" in (pl["seal1"], pl["seal2"]) or "G3-M12" in (pl["seal1"], pl["seal2"]) or "G3-M06" in (pl["seal1"], pl["seal2"]):
            print(f"      LOCK {pl['seal1']}<->{pl['seal2']}: shared={pl['shared']} | {pl['order1']} vs {pl['order2']} | same_ord={pl['same_order']}")


# =============================================================================
# TEST 3B-3: UR III (UET 3) & GIRSU/GUABBA MELUHHA PROSOPOGRAPHY + 2 TESTS
# =============================================================================
print("\n" + "=" * 78)
print("TEST 3B-3: UR III SEA-MERCHANT & MELUHHA PROSOPOGRAPHY + CALQUE & PHONETIC TESTS")
print("=" * 78)

# 1. Load & merge ALL local CDLI tablets (JSONL + full 802-tablet Guabba/Girsu JSON) for corpus-wide baselines
cdli_docs = {}
for rel in ["work_data/abroad2/cdli_meluhha_atf.jsonl", "work_data/abroad3/cdli_east_atf.jsonl"]:
    p = ROOT / rel
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for ln in f:
                o = json.loads(ln)
                pid = "P" + str(o["id"]).lstrip("P").zfill(6)
                cdli_docs[pid] = o

guabba_full_path = ROOT / "work_data" / "abroad2" / "cdli_meluhha_guabba_full.json"
if guabba_full_path.exists():
    with open(guabba_full_path, encoding="utf-8") as f:
        for o in json.load(f):
            pid = "P" + str(o.get("id", "")).lstrip("P").zfill(6)
            ins = o.get("inscription") or {}
            atf_txt = ins.get("atf", "") if isinstance(ins, dict) else ""
            if atf_txt:
                o["atf"] = atf_txt
                # Prefer guabba_full metadata when existing entry lacks provenience/period
                if pid not in cdli_docs or not cdli_docs[pid].get("provenience"):
                    cdli_docs[pid] = o
print(f"  Merged local CDLI corpus size: {len(cdli_docs)} unique tablets")

# Automated corpus-level theophoric PN + institutional formula scan across Bronze Age cohorts
DEITY_PATTERNS = {
    "Moon_Nanna_Suen": re.compile(r"\{d\}(?:nanna|suen|zu-en|zuen)\b|-{d}(?:nanna|suen|zuen)\b|\b(?:nanna|suen)-(?:kam|an-dul3|i3-sa6|ma-an-sum2|in-tuh|i-din-nam|ma-gir|isz-me-a-ni)", re.I),
    "Sun_Utu_Samas": re.compile(r"\{d\}(?:utu|szamasz)\b|-{d}utu\b", re.I),
    "Enlil": re.compile(r"\{d\}en-lil2\b", re.I),
    "Enki_Ea": re.compile(r"\{d\}(?:en-ki|e2-a)\b|\be2-a-na-s,i-ir\b|\bszu-e2-a\b", re.I),
    "Lagash_Nanshe_Baba_Ningirsu_Lamma_Ninmarki": re.compile(r"\{d\}(?:nansze|ba-ba6|nin-gir2-su|lamma|nin-mar\{ki\}|ig-alim)\b", re.I),
    "Inzak_Dilmun": re.compile(r"\{d\}in-za-ak\b|\bin-za-ak\b|\bpa-ni-pa\b", re.I),
}
INST_PATTERNS = {
    "e2_nanna_or_tithe": re.compile(r"e2\s+\{d\}nanna|za3-(?:ub3|1\(u\))\s+\{d\}nanna|\{d\}nanna-a\s+sza3\s+ki-ag2", re.I),
    "e2_kiszib_sealhouse": re.compile(r"e2-kiszib3-ba", re.I),
    "e2_utu_samas": re.compile(r"e2\s+\{d\}(?:utu|szamasz)", re.I),
    "e2_ninmarki_nanshe_ningirsu": re.compile(r"e2\s+\{d\}(?:nin-mar|nansze|nin-gir2-su|ba-ba6)", re.I),
    "e2_enki": re.compile(r"e2\s+\{d\}en-ki", re.I),
}

# Filter out royal year-names (`mu {d}i-bi2-{d}suen`, `mu {d}amar-{d}suen`, `mu {d}szu-{d}suen`) when counting PN theophorics!
def strip_year_lines(atf: str) -> str:
    out = []
    for ln in atf.splitlines():
        s = ln.strip()
        if re.match(r"^\d+\.?\s*mu\s+", s, re.I):
            continue
        if s.startswith("#") or s.startswith("@") or s.startswith("$") or s.startswith("&"):
            continue
        out.append(s)
    return "\n".join(out)

PN_THEOPHORIC_PATS = {
    "Moon_Nanna_Suen": re.compile(r"\b(?:ur|lu2|arad2?|szu|amar|gimil|im-gur|en-nam|nig2-ga|nu-ur2)-\{d\}(?:nanna|suen|zu-en)\b|\{d\}(?:nanna|suen)-[a-z0-9-]+", re.I),
    "Sun_Utu_Samas": re.compile(r"\b(?:ur|lu2|arad2?|szu|amar|nu-ur2)-\{d\}(?:utu|szamasz)\b|\{d\}(?:utu|szamasz)-[a-z0-9-]+", re.I),
    "Enlil": re.compile(r"\b(?:ur|lu2|arad2?|szu|amar)-\{d\}en-lil2(?:-la2)?\b|\{d\}en-lil2-[a-z0-9-]+", re.I),
    "Enki_Ea": re.compile(r"\b(?:ur|lu2|arad2?|szu)-(?:\{d\})?(?:en-ki|e2-a)\b|\be2-a-[a-z0-9-]+", re.I),
    "Lagash_Local": re.compile(r"\b(?:ur|lu2|arad2?|szu)-\{d\}(?:nansze|ba-ba6|nin-gir2-su|lamma|nin-mar\{ki\}|ig-alim)\b", re.I),
    "Inzak_Dilmun": re.compile(r"\b(?:arad2?|warad)\s+\{d\}in-za-ak\b|\bin-za-ak\b", re.I),
}

corpus_cohort_pn = collections.defaultdict(collections.Counter)
corpus_cohort_inst = collections.defaultdict(collections.Counter)
corpus_cohort_ndocs = collections.Counter()

for pid, o in cdli_docs.items():
    per_raw = o.get("period") or ""
    per = (per_raw.get("period", "") if isinstance(per_raw, dict) else str(per_raw)).lower()
    prov_raw = o.get("provenience") or ""
    prov = (prov_raw.get("provenience", "") if isinstance(prov_raw, dict) else str(prov_raw)).lower()
    des = str(o.get("designation", ""))
    atf = o.get("atf", "") or ""
    if not atf:
        continue
    if "ur iii" in per and ("uet 3" in des.lower() or "ur (" in prov or prov == "ur"):
        coh = "CDLI_UR3_UR_UET3"
    elif "ur iii" in per and ("girsu" in prov or "lagash" in prov or "gu2-ab-ba" in atf.lower()):
        coh = "CDLI_UR3_GIRSU_GUABBA"
    elif "old babylon" in per and ("uet 5" in des.lower() or "ur (" in prov or "larsa" in prov):
        coh = "CDLI_OB_UR_LARSA"
    else:
        continue
    corpus_cohort_ndocs[coh] += 1
    body = strip_year_lines(atf)
    for dname, pat in PN_THEOPHORIC_PATS.items():
        # Exclude king names szu-suen, amar-suen, ibbi-suen if they somehow appear outside mu-lines
        hits = [m.group(0) for m in pat.finditer(body)
                if not re.search(r"i-bi2-\{d\}suen|amar-\{d\}suen|szu-\{d\}suen", m.group(0), re.I)]
        corpus_cohort_pn[coh][dname] += len(hits)
    for iname, pat in INST_PATTERNS.items():
        if pat.search(atf):
            corpus_cohort_inst[coh][iname] += 1

# 2. Curated, Source-Verified Prosopography Table (`ur3_meluhha_prosopography.csv`)
# Columns: pn_id, name_norm, atf_spelling, cohort, period, site, role_title, meluhha_direct_tag,
#          linguistic_origin, theophoric_deity, institution_context, source_tablets, notes
PROSOPOGRAPHY = [
    # --- COHORT 1: UR III UET 3 SEA-MERCHANTS & NANNA/MELUHHA-WORKSHOP OFFICIALS (UR) ---
    ("U3-01", "Lu-Enlilla", "lu2-{d}en-lil2-la2 dumu ka-mah", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "ga-esz8 (seafaring merchant)", "no", "Sumerian", "Enlil", "e2 {d}nanna / e2-kiszib3-ba / za3-ub3 {d}nanna", "UET 3, 1511 (P137837); UET 3, 1689 (P138015); UET 3, 0751 (P137075); U.16517 (P136357)", "Draws wool/cloth/oil from Nanna temple seal-house to buy Magan copper; pays ivory/copper tithe to Nanna"),
    ("U3-02", "ARAD-Nanna", "ARAD2-{d}nanna", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "ugula / dub-sar za3 1(u) (seal/gold issuer)", "no", "Sumerian", "Moon_Nanna_Suen", "Ur Palace / e2 {d}nanna craft orbit", "UET 3, 0672 (P136994); UET 3, 1193 (P137518); UET 3, 1498 (P137823)", "Issues red gold to mount 1 Dilmun stone seal (kiszib3 na4 dilmun); oversees lapis/carnelian seals & Meluhha craft goods"),
    ("U3-03", "Nanna-kam", "{d}nanna-kam", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "Meluhha wood/ivory & Magan issuer", "no", "Sumerian", "Moon_Nanna_Suen", "Ur craft archive / {d}nanna", "UET 3, 0751 (P137075); UET 3, 0818 (P137142); UET 3, 1498 (P137823)", "Issues mes me-luh-ha wood and gi ma2-gan{ki}; associated with Nanna tithe"),
    ("U3-04", "Nanna-andul", "{d}nanna-an-dul3", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen yr 1)", "Ur", "dub-sar (Dilmun ship wool scribe)", "no", "Sumerian", "Moon_Nanna_Suen", "Ur Dilmun ship dispatch", "UET 3, 1507 (P137833)", "Scribe on 10-talent wool loading onto Dilmun ship"),
    ("U3-05", "Ur-gur", "ur-gur", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen yr 1)", "Ur", "lu2 ma2-da-[x] (Dilmun ship agent)", "no", "Sumerian", "None_Secular", "Ur Dilmun ship dispatch", "UET 3, 1507 (P137833)", "Receives 10 talents wool loaded on boat to Dilmun"),
    ("U3-06", "Lu-Suen", "lu2-{d}suen", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "craft timber/boat issuer", "no", "Sumerian", "Moon_Nanna_Suen", "Ur craft archive (e2 nagar)", "UET 3, 1498 (P137823)", "Issues ship-building timber alongside Meluhha/Magan luxury goods"),
    ("U3-07", "Lu-Shu-Suen", "lu2-{d}szu-{d}suen", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "craft archive issuer", "no", "Sumerian", "Moon_Nanna_Suen", "Ur craft archive", "UET 3, 1498 (P137823)", "Royal-moon theophoric official in Meluhha/Magan craft ledger"),
    ("U3-08", "Ibbi-Suen-Enlilda-nirgal", "{d}i-bi2-{d}suen-{d}en-lil2-da-nir-gal2", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "craft archive issuer", "no", "Sumerian", "Moon_Nanna_Suen", "Ur craft archive", "UET 3, 1498 (P137823)", "Royal-moon + Enlil theophoric official in UET 3 1498"),
    ("U3-09", "Ahu-waqar", "a-hu-wa-qar", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "szabra (chief workshop director)", "no", "Akkadian", "None_Secular", "Ur craft workshop ({d}nanna colophons)", "UET 3, 0493, 0660, 0757, 0761, 0764, 0768, 0770, 0803, 0818, 1498", "Receives Meluhha ivory figurines, Meluhha ebony/mes wood, Magan reeds"),
    ("U3-10", "Dingir-su-rabi", "dingir-su-ra-bi2", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "ivory & Meluhha wood issuer", "no", "Akkadian", "Other_Deity", "Ur craft workshop", "UET 3, 0493, 0757, 0761, 0764, 0768, 0770, 1498", "Primary supplier of ivory & Meluhha figurines to Ahu-waqar"),
    ("U3-11", "Amar-Ishkur", "amar-{d}iszkur", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "Meluhha wood issuer", "no", "Sumerian", "Other_Deity", "Ur craft workshop", "UET 3, 0660 (P136982); UET 3, 1498 (P137823)", "Issues {gesz}ab-ba me-luh-ha"),
    ("U3-12", "Ur-Hendursag", "ur-{d}hendur-sag", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "Magan reed issuer", "no", "Sumerian", "Other_Deity", "Ur craft workshop", "UET 3, 0803 (P137127)", "Issues gi ma2-gan{ki} to Ahu-waqar"),
    ("U3-13", "Ur-Shulgi", "ur-{d}szul-gi(-ra)", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "export goods / wool issuer", "no", "Sumerian", "Other_Deity", "e2 {d}nanna / e2-kiszib3-ba", "UET 3, 1511 (P137837); UET 3, 1689 (P138015); UET 3, 1498 (P137823)", "Supplies textiles/goods for Lu-Enlilla's copper voyage"),
    ("U3-14", "Ur-Shulpae", "ur-{d}szul-pa-e3", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "oil/goods issuer", "no", "Sumerian", "Other_Deity", "e2 {d}nanna", "UET 3, 1511 (P137837)", "Supplies sesame oil from Nanna temple for copper voyage"),
    ("U3-15", "Lugal-gaba", "lugal-gaba", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "goods issuer", "no", "Sumerian", "None_Secular", "e2 {d}nanna", "UET 3, 1511 (P137837)", "Supplies export goods to Lu-Enlilla"),
    ("U3-16", "Lugal-Magan", "lugal-ma2-gan{ki}", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "Magan-named Ur official", "no", "Sumerian", "None_Secular", "Ur archive", "UET 3, 0299 (P136619)", "Ethnonymic/toponymic Magan name at Ur"),
    ("U3-17", "Lu-Magan", "lu2-ma2-gan{ki}", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "sagi (cupbearer) at e2-kiszib3-ba", "no", "Sumerian", "None_Secular", "e2-kiszib3-ba", "UET 3, 0883 (P137207)", "Conveyor at Ur seal-house"),
    ("U3-18", "Shu-kubum", "szu-ku8-bu-um", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "issuer on Magan tablet", "no", "Akkadian", "None_Secular", "Ur archive", "UET 3, 0299 (P136619)", "In Lugal-Magan transaction"),
    ("U3-19", "Inim-gina", "inim-gi-na", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "recipient on Magan tablet", "no", "Sumerian", "None_Secular", "Ur archive", "UET 3, 0299 (P136619)", "Also cf. lu2-inim-gi-na szabra in UET 3 0828"),
    ("U3-20", "Lu-inimgina", "lu2-inim-gi-na", "UR3_UET3_SEATRADE", "Ur III", "Ur", "szabra gesz-kin-ti (workshop steward)", "no", "Sumerian", "None_Secular", "gesz-kin-ti (Ur)", "UET 3, 0828 (P137152 / S005815)", "Superior on ARAD2-zu seal legend at Ur"),
    ("U3-21", "Puzur-Eshtar", "puzur4-esz18-dar", "UR3_UET3_SEATRADE", "Ur III", "Ur", "dub-sar (ARAD2-zu of Lu-inimgina)", "no", "Akkadian", "Other_Deity", "gesz-kin-ti (Ur)", "UET 3, 0828 (P137152 / S005815)", "Seal holder on Ur workshop tablet"),
    ("U3-22", "Ur-gu-edinna", "ur-gu2-edin-na", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "craft archive issuer", "no", "Sumerian", "None_Secular", "Ur craft archive", "UET 3, 1498 (P137823)", "Repeated metal/linen issuer in UET 3 1498"),
    ("U3-23", "Ur-Baba", "ur-{d}ba-ba6", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "craft archive wood issuer", "no", "Sumerian", "Lagash_Local", "Ur craft archive", "UET 3, 1498 (P137823)", "Wood issuer in Meluhha/Magan workshop ledger"),
    ("U3-24", "Lu-Baba", "lu2-{d}ba-ba6", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "craft archive issuer", "no", "Sumerian", "Lagash_Local", "Ur craft archive", "UET 3, 1498 (P137823)", "Leather/textile issuer in UET 3 1498"),
    ("U3-25", "Shu-Ea", "szu-e2-a", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "timber issuer", "no", "Akkadian", "Enki_Ea", "Ur craft archive", "UET 3, 1498 (P137823)", "Timber issuer in UET 3 1498"),
    ("U3-26", "Nur-Utu", "nu-ur2-{d}utu", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "reed/craft issuer", "no", "Akkadian", "Sun_Utu_Samas", "Ur craft archive", "UET 3, 1498 (P137823)", "Sole Sun-theophoric official in UET 3 1498!"),
    ("U3-27", "Lu-Shara", "lu2-{d}szara2", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "craft archive issuer", "no", "Sumerian", "Other_Deity", "Ur craft archive", "UET 3, 1498 (P137823)", "Issuer in UET 3 1498"),
    ("U3-28", "Ur-Eanna", "ur-e2-an-na", "UR3_UET3_SEATRADE", "Ur III (Ibbi-Suen)", "Ur", "craft archive issuer", "no", "Sumerian", "Other_Deity", "Ur craft archive", "UET 3, 1498 (P137823)", "Temple-name Ur-E2 compound in UET 3 1498"),
    ("U3-29", "Ur-Nanshe", "ur-{d}nansze", "UR3_UET3_SEATRADE", "Ur III", "Ur", "Magan expedition official", "no", "Sumerian", "Lagash_Local", "Ur Magan account", "UET 3, 1193 (P137518)", "Co-attested with ARAD2-Nanna & ma2-gan{ki} gu-la-kam"),
    ("U3-30", "Nanna-isa", "{d}nanna-i3-sa6", "UR3_UET3_SEATRADE", "Ur III", "Ur", "szusz3 (Nanna-temple/sea-trade orbit)", "no", "Sumerian", "Moon_Nanna_Suen", "Ur archive", "UET 3, 1689 (P138015); Oppenheim 1954", "Ur III Nanna-theophoric official in Lu-Enlilla dossier"),

    # --- COHORT 2: DIRECTLY MELUHHA-TAGGED PERSONNEL (UR III & OLD AKKADIAN) ---
    # Strictly distinguishes Sumerian/Akkadian assimilated names vs genuinely Non-Sumerian/Foreign Meluhhan names!
    ("ML-01", "Ur-Lamma", "ur-{d}lamma dumu me-luh-ha", "MELUHHA_DIRECT_TAGGED", "Ur III (Shulgi–Amar-Suen)", "Girsu/Guabba", "dumu me-luh-ha (barley/wool/votive official, seal holder)", "yes_dumu_meluhha", "Sumerian", "Lagash_Local", "e2 {d}nin-mar{ki} / gu2-ab-ba{ki}", "P108448 (CT 3 17); P123177 (OBTR 242); P136196 (UDT 64); P202783 (PPAC 5 612); P207485 (MVN 22 181); P318542 (PPAC 5 323)", "Assimilated Lagash Sumerian name; holds personal seal (kiszib3 ur-{d}lamma dumu me-luh-ha) for 425+ gur barley!"),
    ("ML-02", "Ur-Igalim", "ur-{d}ig-alim dumu me-luh-ha", "MELUHHA_DIRECT_TAGGED", "Ur III", "Girsu/Guabba", "dumu me-luh-ha (granary official)", "yes_dumu_meluhha", "Sumerian", "Lagash_Local", "Girsu/Guabba granary", "P124739 (Orient 16 131); Vermaak 2008 p.465", "Assimilated Lagash Sumerian name"),
    ("ML-03", "Lu-sunzida", "lu2-sun2-zi-da lu2 me-luh-ha-ke4", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Girsu/Lagash", "lu2 me-luh-ha (silver debtor, 10 shekels)", "yes_lu2_meluhha", "Sumerian", "None_Secular", "Lagash legal text", "P212982 (CT 50, 076); Parpola 1977", "Assimilated Sumerian name ('Man of the true wild cow')"),
    ("ML-04", "Lu-marza", "lu2-mar-za dumu me-luh-ha", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Lagash/Mesopotamia", "dumu me-luh-ha", "yes_dumu_meluhha", "Sumerian", "None_Secular", "Old Akkadian ledger", "P467759 (CUSAS 26, 259)", "Assimilated Sumerian name ('Man of rites/office')"),
    ("ML-05", "Nin-ana", "nin-an-na", "MELUHHA_DIRECT_TAGGED", "Ur III", "Girsu/Guabba", "woman of e2-duru5 me-luh-ha", "yes_eduru_meluhha", "Sumerian", "Other_Deity", "e2-duru5 me-luh-ha", "Parpola 1977 Text 1 (L 7157); Vermaak 2008", "Assimilated Sumerian name in Meluhha village"),
    ("ML-06", "Ur-Ishtaran", "ur-{d}isztaran", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Girsu/Lagash", "dub-sar (under ugula me-luh-ha, ARAD2 Nanshe)", "yes_ugula_meluhha", "Sumerian", "Other_Deity", "ARAD2 {d}nansze / ugula me-luh-ha", "P115261 (MVN 7, 411)", "Sumerian name in Nanshe/Meluhha squad"),
    ("ML-07", "Lugal-gigir", "lugal-{gesz}gigir", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Girsu/Lagash", "dub-sar (under ugula me-luh-ha)", "yes_ugula_meluhha", "Sumerian", "None_Secular", "ARAD2 {d}nansze / ugula me-luh-ha", "P115261 (MVN 7, 411)", "Sumerian name"),
    ("ML-08", "Tul-ta", "tul2-ta", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Girsu/Lagash", "tug2-du8 (fuller, under ugula me-luh-ha)", "yes_ugula_meluhha", "Sumerian", "None_Secular", "ARAD2 {d}nansze / ugula me-luh-ha", "P115261 (MVN 7, 411)", "Sumerian name"),
    ("ML-09", "Ur-a", "ur-a2", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Girsu/Lagash", "worker under ugula me-luh-ha", "yes_ugula_meluhha", "Sumerian", "None_Secular", "ARAD2 {d}nansze / ugula me-luh-ha", "P115261 (MVN 7, 411)", "Sumerian name"),
    ("ML-10", "Ur-shu", "ur-szu", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Girsu/Lagash", "worker under ugula me-luh-ha", "yes_ugula_meluhha", "Sumerian", "None_Secular", "ARAD2 {d}nansze / ugula me-luh-ha", "P115261 (MVN 7, 411)", "Sumerian name"),
    ("ML-11", "Utu-sa", "{d}utu-sa6", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Mesopotamia", "nu-banda3 ma2 me-luh-ha (Meluhha-ship captain)", "yes_ma2_meluhha", "Sumerian", "Sun_Utu_Samas", "Meluhha ship", "P326408 (CUSAS 20, 153)", "Sumerian Sun-theophoric ship overseer"),
    ("ML-12", "Anna-shum", "an-na-szum2", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Mesopotamia", "giri3-gen-na ma2 me-luh-ha-sze3 (agent to Meluhha ship)", "yes_ma2_meluhha", "Sumerian", "Other_Deity", "Meluhha ship", "P382354 (TCBI 1, 102)", "Sumerian name"),
    ("ML-13", "Shu-ilishu", "szu-i3-li2-su eme-bal me-luh-ha{ki}", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Mesopotamia (Louvre seal)", "eme-bal me-luh-ha{ki} (interpreter of Meluhha)", "yes_emebal_meluhha", "Akkadian", "Other_Deity", "Akkadian cylinder seal", "P525331 (CDLI seals 014339)", "Classic Akkadian PN ('He of his god'); famous Meluhha interpreter seal"),
    ("ML-14", "Ili-ahi", "i3-li2-a-hi lu2 me-luh", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Mesopotamia", "lu2 me-luh (Meluhhan alongside lu2 kiszib3 & maszkim ma2 dilmun)", "yes_lu2_meluhha", "Akkadian", "Other_Deity", "Akkadian port ledger", "P253274 (CUSAS 35, 288)", "Akkadian PN ('My god is my brother') carried by Meluhhan"),
    ("ML-15", "Gal-ili", "gal-i3-li2", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Girsu/Lagash", "ugula usz-bar (under ugula me-luh-ha)", "yes_ugula_meluhha", "Akkadian", "Other_Deity", "ARAD2 {d}nansze / ugula me-luh-ha", "P115261 (MVN 7, 411)", "Hybrid/Akkadian PN"),
    ("ML-16", "Ali-ahi", "a-li-a-hi dam-a-ni (lu2 me-luh-ha{ki}-me)", "MELUHHA_DIRECT_TAGGED", "Ur III (Shu-Suen)", "Irisagrig", "wife of sa6-ma-ar, lu2 me-luh-ha{ki}-me", "yes_lu2_meluhha", "Akkadian_or_Ambiguous", "None_Secular", "a-ru-a lugal / sipa a-dara4-me", "P453801 (Nisaba 15 371); P516138 (CUSAS 40 1354); P516366 (CUSAS 40 1582)", "Probable Akkadian PN ('Where is my brother?'); married to foreign Meluhhan sa6-ma-ar"),
    # --- GENUINELY NON-SUMERIAN / FOREIGN MELUHHA-TAGGED PNs (STRICT SET, N=6) ---
    ("ML-17", "Nanasa", "na-na-sa3 (lu2 me-luh-ha{ki}-me)", "MELUHHA_DIRECT_TAGGED", "Ur III (Shu-Suen)", "Irisagrig", "lu2 me-luh-ha{ki}-me, a-ru-a lugal, sipa a-dara4-me", "yes_lu2_meluhha", "Non-Sumerian/Foreign_Meluhhan", "None_Secular", "Royal ex-voto ibex-herders (Irisagrig)", "P453801 (Nisaba 15 371); P516138 (CUSAS 40 1354); P516366 (CUSAS 40 1582)", "GENUINELY NON-SUMERIAN UR III MELUHHAN PN! Oil-rationed 3x at Irisagrig"),
    ("ML-18", "Samar", "sa6-ma-ar (lu2 me-luh-ha{ki}-me)", "MELUHHA_DIRECT_TAGGED", "Ur III (Shu-Suen)", "Irisagrig", "lu2 me-luh-ha{ki}-me, a-ru-a lugal, sipa a-dara4-me", "yes_lu2_meluhha", "Non-Sumerian/Foreign_Meluhhan", "None_Secular", "Royal ex-voto ibex-herders (Irisagrig)", "P453801 (Nisaba 15 371); P516138 (CUSAS 40 1354); P516366 (CUSAS 40 1582)", "GENUINELY NON-SUMERIAN UR III MELUHHAN PN! Paired with na-na-sa3"),
    ("ML-19", "[...]ibra", "[...]-ib-ra lu2 me-luh-ha", "MELUHHA_DIRECT_TAGGED", "Old Akkadian (Naram-Sin)", "Mesopotamia (Naram-Sin inscr.)", "rebel king of Meluhha", "yes_lu2_meluhha", "Non-Sumerian/Foreign_Meluhhan", "None_Secular", "Naram-Sin Great Revolt inscription", "RIME 2.01.04.06; Parpola 1977; Potts 1994", "GENUINELY NON-SUMERIAN MELUHHAN ROYAL PN (partial onset broken)"),
    ("ML-20", "Dadi", "da-di3 lu2-tukul ma2 me-luh-ha-ka", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Umma/Lagash", "lu2-tukul ma2 me-luh-ha-ka (Meluhha-ship officer)", "yes_ma2_meluhha", "Non-Sumerian/Foreign_Meluhhan", "None_Secular", "Meluhha boat", "P212842 (BIN 08, 298)", "Non-Sumerian PN (Lallname / Semitic or foreign) on Meluhha ship"),
    ("ML-21", "Inusadu", "i-nu-sa-du2", "MELUHHA_DIRECT_TAGGED", "Old Akkadian", "Umma/Lagash", "co-recipient on Meluhha-ship oil tablet", "yes_ma2_meluhha", "Non-Sumerian/Foreign_Meluhhan", "None_Secular", "Meluhha boat", "P212842 (BIN 08, 298)", "GENUINELY NON-SUMERIAN PN directly following da-di3 lu2-tukul ma2 me-luh-ha-ka"),
    ("ML-22", "Meluhha", "me-luh-ha (ugula / PN)", "MELUHHA_DIRECT_TAGGED", "Old Akkadian / Ur III", "Girsu/Guabba", "ugula me-luh-ha / ethnonymic PN", "yes_ugula_meluhha", "Non-Sumerian/Foreign_Meluhhan", "None_Secular", "Girsu/Guabba", "P115261 (MVN 7, 411); Vermaak 2008 p.466", "Native toponym/ethnonym used as personal name"),
    # --- EXPANDED FOREIGN ASSOCIATES ON MELUHHA/MAGAN/DILMUN TABLETS ---
    ("ML-23", "Ba-alla", "ba-a-al-la", "MELUHHA_ASSOC_FOREIGN", "Ur III", "Girsu/Guabba", "barley account co-actor with Ur-Lamma dumu me-luh-ha", "assoc_meluhha_tablet", "Non-Sumerian/Foreign_Meluhhan", "None_Secular", "e2 {d}nin-mar{ki}", "P123177 (OBTR 242); P202783 (PPAC 5 612)", "Non-Sumerian name (mu ba-a-al-la-a-sze3) on Ur-Lamma dumu me-luh-ha barley ledgers"),
    ("ML-24", "Arab-irina", "a-ra-ab-iri-na", "MELUHHA_ASSOC_FOREIGN", "Ur III", "Girsu/Guabba", "a-ru-a ur-{d}lamma dumu me-luh-ha (votive servant)", "assoc_meluhha_tablet", "Non-Sumerian/Foreign_Meluhhan", "None_Secular", "Girsu/Guabba votive list", "P318542 (PPAC 5, 0323)", "Unusual non-standard PN dedicated by Ur-Lamma dumu me-luh-ha"),
    ("ML-25", "Wedum", "we-du-um", "MELUHHA_ASSOC_FOREIGN", "Ur III", "Girsu/Puzrish-Dagan", "lu2 kin-gi4-a na-du-be-li2 ensi2 ma2-gan{ki}", "assoc_magan", "Akkadian_or_Ambiguous", "None_Secular", "Magan embassy", "P108701", "Magan envoy"),
    ("ML-26", "Nadubeli", "na-du-be-li2", "MELUHHA_ASSOC_FOREIGN", "Ur III", "Magan (Girsu/Drehem tablet)", "ensi2 ma2-gan{ki} (governor of Magan)", "assoc_magan", "Akkadian_or_Ambiguous", "None_Secular", "Magan ruler", "P108701", "Magan governor"),

    # --- COHORT 3: UR III GIRSU/GUABBA GRANARY & MELUHHA-VILLAGE ASSOCIATED OFFICIALS ---
    ("GG-01", "Ur-Nanshe", "ur-{d}nansze", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu/Guabba", "father of ur-dam & ur-{d}ba-ba6", "no", "Sumerian", "Lagash_Local", "e2 {d}nin-mar{ki}", "P123177; P124739; P136196; P202783", "Core Lagash maritime/granary family"),
    ("GG-02", "Ur-Baba", "ur-{d}ba-ba6", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu/Guabba", "granary/barley official", "no", "Sumerian", "Lagash_Local", "gu2-ab-ba{ki} / e2-duru5 me-luh-ha", "P115266; P123177; P124739; P207485", "Co-attested with e2-duru5 me-luh-ha"),
    ("GG-03", "Lu-Ningirsu", "lu2-{d}nin-gir2-su", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu/Guabba", "dub-sar / granary official", "no", "Sumerian", "Lagash_Local", "Girsu/Guabba", "P207485; S003156; S003161", "Classic Girsu seal holder"),
    ("GG-04", "Ur-Ninmarki", "ur-{d}nin-mar{ki}", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu/Guabba", "dub-sar / Guabba temple orbit", "no", "Sumerian", "Lagash_Local", "e2 {d}nin-mar{ki} (Guabba)", "S002730; S005222", "Tutelary goddess of Guabba port"),
    ("GG-05", "Lu-Shulgi", "lu2-{d}szul-gi", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu/Guabba", "szabra of e2 {d}nin-mar{ki}", "no", "Sumerian", "Other_Deity", "e2 {d}nin-mar{ki}", "P123177; P202783", "Oversees Ur-Lamma dumu me-luh-ha accounts"),
    ("GG-06", "Ur-Eninnu", "ur-e2-ninnu dumu du-du", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu/Guabba", "seal holder for Ur-Lamma dumu me-luh-ha", "no", "Sumerian", "Lagash_Local", "Girsu", "P108448 (CT 3 17)", "Seals wool arrears on behalf of Ur-Lamma"),
    ("GG-07", "Ur-gigir", "ur-{gesz}gigir", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu/Guabba", "ka-guru7 (granary supervisor, e2-duru5 me-luh-ha)", "no", "Sumerian", "None_Secular", "gu2-ab-ba{ki} / e2-duru5 me-luh-ha", "P115266 (MVN 7 420)", "Issues 490 gur barley from Meluhha village"),
    ("GG-08", "Gudea", "gu3-de2-a dumu ur-{d}ba-ba6", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu/Guabba", "seal holder alongside Ur-Lamma dumu me-luh-ha", "no", "Sumerian", "None_Secular", "e2 {d}nin-mar{ki}", "P123177; P136196; P202783", "Co-sealer on barley accounts"),
    ("GG-09", "Ur-dam", "ur-dam dumu ur-{d}nansze", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu/Guabba", "seal holder alongside Ur-Lamma dumu me-luh-ha", "no", "Sumerian", "None_Secular", "e2 {d}nin-mar{ki}", "P123177; P136196; P202783", "Co-sealer on barley accounts"),
    ("GG-10", "Lu-Utu", "lu2-{d}utu", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu", "dub-sar dumu ba-zi", "no", "Sumerian", "Sun_Utu_Samas", "Girsu seal archive", "S003311 (P110431)", "Girsu seal legend"),
    ("GG-11", "Lu-Dumuzi", "lu2-{d}dumu-zi", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu", "gudu4 {d}inanna-ka", "no", "Sumerian", "Other_Deity", "Girsu seal archive", "S003079 (P374962)", "Girsu seal legend"),
    ("GG-12", "Ur-Ningeshzida", "ur-{d}nin-gesz-zi-da", "UR3_GIRSU_GUABBA_ASSOC", "Ur III", "Girsu", "i3-lah5 (oil official)", "no", "Sumerian", "Lagash_Local", "Girsu", "P207485 (MVN 22 181)", "Co-listed with Ur-Lamma dumu me-luh-ha"),

    # --- COHORT 4: OLD BABYLONIAN UET 5 UR ALIK TILMUN SEA-MERCHANTS (COMPARATOR) ---
    ("OB-01", "Ea-nasir", "e2-a-na-s,i-ir", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur (AH No.1 Old St.)", "alik Tilmun (Dilmun copper merchant)", "no", "Akkadian", "Enki_Ea", "Temple of Shamash / Ningal tithe / Palace", "UET 5, 0081 (P414985); UET 5, 0072; UET 5, 286/292/546/678/796", "Famous OB Dilmun copper trader (Oppenheim 1954; Leemans 1960)"),
    ("OB-02", "Nanni", "na-an-ni", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "Dilmun copper investor/client", "no", "Akkadian", "None_Secular", "Temple of Shamash (sealed tablet depository)", "UET 5, 0081 (P414985)", "Author of complaint tablet to Ea-nasir"),
    ("OB-03", "Gimil-Sin", "szu-{d}suen / gi-mil-{d}suen", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "Nanni's agent/messenger in Dilmun", "no", "Akkadian", "Moon_Nanna_Suen", "alik Tilmun network", "UET 5, 0081 (P414985)", "Messenger sent to Ea-nasir"),
    ("OB-04", "Sit-Sin", "s,i-it-{d}suen", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "messenger in Dilmun trade", "no", "Akkadian", "Moon_Nanna_Suen", "alik Tilmun network", "UET 5, 0081 (P414985)", "Mentioned in UET 5 0081"),
    ("OB-05", "Shumi-abum", "szu-mi-a-bu-um", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "copper trade partner (18 talents to palace)", "no", "Akkadian", "None_Secular", "Temple of Shamash / Palace", "UET 5, 0081 (P414985)", "Partner of Nanni"),
    ("OB-06", "Arbituram", "ar-bi-tu-ra-am", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "alik Tilmun copper client/merchant", "no", "Akkadian", "None_Secular", "Ningal temple tithe / Ea-nasir archive", "UET 5 (Oppenheim 1954; Leemans 1960)", "Complainant & Dilmun trader"),
    ("OB-07", "Appa", "ap-pa", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "Dilmun copper correspondent", "no", "Akkadian", "None_Secular", "Ea-nasir archive", "UET 5 (Leemans 1960)", "Correspondent of Ea-nasir"),
    ("OB-08", "Ilshu-ellassu", "il3-szu-el-la-su2 / il3-szu-til-la-su2", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "alik Tilmun partner", "no", "Akkadian", "Other_Deity", "Temple of Shamash", "UET 5, 0072 (Archibab T17165)", "Jointly addressed with Ea-nasir"),
    ("OB-09", "Ilum-gamil", "dingir-ga-mil", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "zabar-du8 / alik Tilmun", "no", "Akkadian", "Other_Deity", "Temple of Shamash / Ningal tithe", "UET 5, 0072; Oppenheim 1954", "Copper trade official & Ningal tithe donor"),
    ("OB-10", "Shumum-libshi", "szu-mu-um-li-ib-szi", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "alik Tilmun partner", "no", "Akkadian", "None_Secular", "Temple of Shamash", "UET 5, 0072", "Recipient of Ea-nasir's letter"),
    ("OB-11", "Ili-idinnam", "i3-li2-i-din-nam", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "copper complainant/trader", "no", "Akkadian", "Other_Deity", "Ea-nasir archive", "UET 5 (Leemans 1960)", "Correspondent of Ea-nasir"),
    ("OB-12", "Imgur-Sin", "im-gur-{d}suen", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "alik Tilmun (Ningal tithe donor)", "no", "Akkadian", "Moon_Nanna_Suen", "Temple of Ningal", "UET 5 Ningal tithes (Oppenheim 1954)", "Dedicates Dilmun ivory/copper tithe to Ningal"),
    ("OB-13", "Nanna-intuh", "{d}nanna-in-tuh", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "alik Tilmun (Ningal tithe donor)", "no", "Sumerian", "Moon_Nanna_Suen", "Temple of Ningal", "UET 5 Ningal tithes (Oppenheim 1954)", "Dedicates Dilmun tithe to Ningal"),
    ("OB-14", "Nigga-Nanna", "nig2-ga-{d}nanna", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "alik Tilmun (Ningal tithe donor)", "no", "Sumerian", "Moon_Nanna_Suen", "Temple of Ningal", "UET 5 Ningal tithes (Oppenheim 1954)", "Dedicates Dilmun tithe to Ningal"),
    ("OB-15", "Ur-Nanna", "ur-{d}nanna", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "Dilmun ship correspondent of king Rim-Sin", "no", "Sumerian", "Moon_Nanna_Suen", "Larsa Palace", "UET 5, 0036 (P414940)", "Receives royal letter on {gesz}ma2 dilmun-na{ki}"),
    ("OB-16", "Ur-Ninmarka", "ur-{d}nin-mar{ki}-ka", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "Dilmun voyage financier (nam-tab-ba)", "no", "Sumerian", "Lagash_Local", "nam-tab-ba partnership", "UET 5, 0367 (P283686)", "Finances Dilmun copper expedition (local CDLI)"),
    ("OB-17", "Lu-Meslamtaea", "lu2-{d}mes-lam-ta-e3-a", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "Dilmun voyage partner", "no", "Sumerian", "Other_Deity", "nam-tab-ba partnership", "UET 5, 0367 (P283686)", "Co-partner on Dilmun voyage (local CDLI)"),
    ("OB-18", "Nigsisa-abdiri", "nig2-si-sa2-ab-diri", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "Dilmun voyage partner", "no", "Sumerian", "None_Secular", "nam-tab-ba partnership", "UET 5, 0367 (P283686)", "Co-partner on Dilmun voyage (local CDLI)"),
    ("OB-19", "Suen-ilum", "{d}suen-i-lum", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "Dilmun voyage witness (sealed)", "no", "Akkadian", "Moon_Nanna_Suen", "nam-tab-ba witness", "UET 5, 0367 (P283686)", "Sealed witness on UET 5 0367"),
    ("OB-20", "Suen-asared", "{d}suen-a-sza-re-ed", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "Dilmun voyage witness (sealed)", "no", "Akkadian", "Moon_Nanna_Suen", "nam-tab-ba witness", "UET 5, 0367 (P283686)", "Sealed witness on UET 5 0367"),
    ("OB-21", "Suen-mutabbil", "{d}suen-mu-ta-bi-il", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "Dilmun voyage witness (sealed)", "no", "Akkadian", "Moon_Nanna_Suen", "nam-tab-ba witness", "UET 5, 0367 (P283686)", "Sealed witness on UET 5 0367"),
    ("OB-22", "Suen-idinnassu", "{d}suen-i-din-na-szu", "OB_UET5_ALIK_TILMUN", "Old Babylonian", "Ur", "Dilmun voyage witness (sealed)", "no", "Akkadian", "Moon_Nanna_Suen", "nam-tab-ba witness", "UET 5, 0367 (P283686)", "Sealed witness on UET 5 0367"),
    ("OB-23", "Kurum", "ku-ru-um", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "copper trade witness/party", "no", "Akkadian", "None_Secular", "Ea-nasir archive", "UET 5, 0072", "Named in UET 5 0072"),
    ("OB-24", "Erishum-matim", "e-ri-szu-um-ma-tim", "OB_UET5_ALIK_TILMUN", "Old Babylonian (Rim-Sin)", "Ur", "copper trade party", "no", "Akkadian", "None_Secular", "Ea-nasir archive", "UET 5, 0072", "Named in UET 5 0072"),
]

# Write ur3_meluhha_prosopography.csv
proso_dicts = []
for row in PROSOPOGRAPHY:
    proso_dicts.append({
        "pn_id": row[0],
        "name_norm": row[1],
        "atf_spelling": row[2],
        "skel": to_skel(row[1]),
        "cohort": row[3],
        "period": row[4],
        "site": row[5],
        "role_title": row[6],
        "meluhha_direct_tag": row[7],
        "linguistic_origin": row[8],
        "theophoric_deity": row[9],
        "institution_context": row[10],
        "source_tablets": row[11],
        "notes": row[12],
    })

with open(OUT_DIR / "ur3_meluhha_prosopography.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(proso_dicts[0].keys()))
    w.writeheader()
    w.writerows(proso_dicts)

# -----------------------------------------------------------------------------
# TEST 3B-3A: THEOPHORIC / INSTITUTIONAL CALQUE TEST (5,000 SHUFFLES)
# -----------------------------------------------------------------------------
print("\n  --- TEST 3B-3A: THEOPHORIC & INSTITUTIONAL CALQUE BASELINES (5,000 SHUFFLES) ---")

cohort_deity_counts = collections.defaultdict(collections.Counter)
for d in proso_dicts:
    cohort_deity_counts[d["cohort"]][d["theophoric_deity"]] += 1

def deity_breakdown(cnt: collections.Counter):
    tot = sum(cnt.values())
    theo_tot = tot - cnt["None_Secular"]
    return {
        "total_pns": tot,
        "theophoric_pns": theo_tot,
        "Moon_Nanna_Suen": cnt["Moon_Nanna_Suen"],
        "Moon_pct_all": round(100 * cnt["Moon_Nanna_Suen"] / tot, 1) if tot else 0.0,
        "Moon_pct_theo": round(100 * cnt["Moon_Nanna_Suen"] / theo_tot, 1) if theo_tot else 0.0,
        "Sun_Utu_Samas": cnt["Sun_Utu_Samas"],
        "Enlil": cnt["Enlil"],
        "Enki_Ea": cnt["Enki_Ea"],
        "Lagash_Local": cnt["Lagash_Local"],
        "Other_Deity": cnt["Other_Deity"],
        "None_Secular": cnt["None_Secular"],
    }

b_ur3 = deity_breakdown(cohort_deity_counts["UR3_UET3_SEATRADE"])
b_girsu = deity_breakdown(cohort_deity_counts["UR3_GIRSU_GUABBA_ASSOC"] + cohort_deity_counts["MELUHHA_DIRECT_TAGGED"])
b_ob = deity_breakdown(cohort_deity_counts["OB_UET5_ALIK_TILMUN"])

# 5,000-shuffle permutation test 1: Moon/Nanna enrichment in Ur III UET 3 vs Ur III Girsu/Meluhha (curated PNs)
rng3a = random.Random(SEED)
ur3_labels = [1 if d["theophoric_deity"] == "Moon_Nanna_Suen" else 0 for d in proso_dicts if d["cohort"] == "UR3_UET3_SEATRADE"]
girsu_labels = [1 if d["theophoric_deity"] == "Moon_Nanna_Suen" else 0 for d in proso_dicts if d["cohort"] in ("UR3_GIRSU_GUABBA_ASSOC", "MELUHHA_DIRECT_TAGGED")]
ob_labels = [1 if d["theophoric_deity"] == "Moon_Nanna_Suen" else 0 for d in proso_dicts if d["cohort"] == "OB_UET5_ALIK_TILMUN"]

pool_ur_girsu = ur3_labels + girsu_labels
obs_diff_ur_girsu = (sum(ur3_labels) / len(ur3_labels)) - (sum(girsu_labels) / len(girsu_labels))
null_diff_ur_girsu = []
for _ in range(5000):
    sh = pool_ur_girsu[:]
    rng3a.shuffle(sh)
    a_s = sh[:len(ur3_labels)]
    b_s = sh[len(ur3_labels):]
    null_diff_ur_girsu.append((sum(a_s) / len(a_s)) - (sum(b_s) / len(b_s)))
mu_ug, sd_ug, z_ug, p_ug_ge, _ = z_and_p(obs_diff_ur_girsu, null_diff_ur_girsu)
or_ug, p_ug_f2, p_ug_fgt = fisher_exact_two_sided(sum(ur3_labels), len(ur3_labels) - sum(ur3_labels), sum(girsu_labels), len(girsu_labels) - sum(girsu_labels))

# 5,000-shuffle permutation test 2: Moon/Nanna in Ur III UET 3 vs OB UET 5 (curated PNs)
pool_ur_ob = ur3_labels + ob_labels
obs_diff_ur_ob = (sum(ur3_labels) / len(ur3_labels)) - (sum(ob_labels) / len(ob_labels))
null_diff_ur_ob = []
for _ in range(5000):
    sh = pool_ur_ob[:]
    rng3a.shuffle(sh)
    a_s = sh[:len(ur3_labels)]
    b_s = sh[len(ur3_labels):]
    null_diff_ur_ob.append((sum(a_s) / len(a_s)) - (sum(b_s) / len(b_s)))
mu_uo, sd_uo, z_uo, p_uo_ge, p_uo_le = z_and_p(obs_diff_ur_ob, null_diff_ur_ob)
or_uo, p_uo_f2, _ = fisher_exact_two_sided(sum(ur3_labels), len(ur3_labels) - sum(ur3_labels), sum(ob_labels), len(ob_labels) - sum(ob_labels))

# 5,000-shuffle permutation test 3: Automated Full CDLI Corpus Moon/Nanna PN rate (Ur III UET 3 vs Ur III Girsu/Guabba)
u3_moon_hits = corpus_cohort_pn["CDLI_UR3_UR_UET3"]["Moon_Nanna_Suen"]
u3_tot_theo = sum(corpus_cohort_pn["CDLI_UR3_UR_UET3"].values())
gg_moon_hits = corpus_cohort_pn["CDLI_UR3_GIRSU_GUABBA"]["Moon_Nanna_Suen"]
gg_tot_theo = sum(corpus_cohort_pn["CDLI_UR3_GIRSU_GUABBA"].values())
ob_moon_hits = corpus_cohort_pn["CDLI_OB_UR_LARSA"]["Moon_Nanna_Suen"]
ob_tot_theo = sum(corpus_cohort_pn["CDLI_OB_UR_LARSA"].values())

cdli_pool = [1] * (u3_moon_hits + gg_moon_hits) + [0] * ((u3_tot_theo - u3_moon_hits) + (gg_tot_theo - gg_moon_hits))
obs_cdli_diff = (u3_moon_hits / u3_tot_theo) - (gg_moon_hits / gg_tot_theo) if u3_tot_theo and gg_tot_theo else 0.0
null_cdli_diff = []
for _ in range(5000):
    sh = cdli_pool[:]
    rng3a.shuffle(sh)
    a_s = sh[:u3_tot_theo]
    b_s = sh[u3_tot_theo:]
    null_cdli_diff.append((sum(a_s) / len(a_s)) - (sum(b_s) / len(b_s)))
mu_cd, sd_cd, z_cd, p_cd_ge, _ = z_and_p(obs_cdli_diff, null_cdli_diff)
or_cd, p_cd_f2, p_cd_fgt = fisher_exact_two_sided(u3_moon_hits, u3_tot_theo - u3_moon_hits, gg_moon_hits, gg_tot_theo - gg_moon_hits)

# Institutional test: e2 {d}nanna / Nanna-tithe tablets in Ur III UET 3 vs Girsu/Guabba
u3_inst_n = corpus_cohort_ndocs["CDLI_UR3_UR_UET3"]
u3_nanna_inst = corpus_cohort_inst["CDLI_UR3_UR_UET3"]["e2_nanna_or_tithe"]
gg_inst_n = corpus_cohort_ndocs["CDLI_UR3_GIRSU_GUABBA"]
gg_nanna_inst = corpus_cohort_inst["CDLI_UR3_GIRSU_GUABBA"]["e2_nanna_or_tithe"]
or_inst, p_inst_f2, p_inst_fgt = fisher_exact_two_sided(u3_nanna_inst, u3_inst_n - u3_nanna_inst, gg_nanna_inst, gg_inst_n - gg_nanna_inst)

print(f"  Curated UR3_UET3_SEATRADE (n={b_ur3['total_pns']}): Moon/Nanna={b_ur3['Moon_Nanna_Suen']} ({b_ur3['Moon_pct_all']}% all, {b_ur3['Moon_pct_theo']}% of theophorics) | Sun={b_ur3['Sun_Utu_Samas']} | Enlil={b_ur3['Enlil']} | Enki={b_ur3['Enki_Ea']} | Lagash={b_ur3['Lagash_Local']}")
print(f"  Curated UR3_GIRSU+MELUHHA (n={b_girsu['total_pns']}): Moon/Nanna={b_girsu['Moon_Nanna_Suen']} ({b_girsu['Moon_pct_all']}% all) | Sun={b_girsu['Sun_Utu_Samas']} | Lagash={b_girsu['Lagash_Local']}")
print(f"  Curated OB_UET5_ALIK_TILMUN (n={b_ob['total_pns']}): Moon/Nanna={b_ob['Moon_Nanna_Suen']} ({b_ob['Moon_pct_all']}% all, {b_ob['Moon_pct_theo']}% theo) | Sun={b_ob['Sun_Utu_Samas']} | Enki/Ea={b_ob['Enki_Ea']}")
print(f"    5,000-shuffle Ur III UET 3 vs Girsu/Meluhha Moon enrichment: diff={100*obs_diff_ur_girsu:+.1f}pp, z={z_ug:+.2f}, P_perm={p_ug_ge:.4f}, Fisher P_gt={p_ug_fgt:.4e}")
print(f"    5,000-shuffle Ur III UET 3 vs OB UET 5 Moon comparison:      diff={100*obs_diff_ur_ob:+.1f}pp, z={z_uo:+.2f}, P_two={p_uo_f2:.4f} (OB Ur ALSO stays Moon/Suen-heavy, shifting temple locus from Nanna seal-house to Shamash/Ningal!)")
print(f"  Automated Local CDLI Corpus Scan:")
print(f"    CDLI_UR3_UR_UET3 ({u3_inst_n} tablets): Moon_PN={u3_moon_hits}/{u3_tot_theo} ({100*u3_moon_hits/max(1,u3_tot_theo):.1f}% of theophoric hits) | e2_Nanna/tithe={u3_nanna_inst}/{u3_inst_n} ({100*u3_nanna_inst/max(1,u3_inst_n):.1f}%) | e2-kiszib3-ba={corpus_cohort_inst['CDLI_UR3_UR_UET3']['e2_kiszib_sealhouse']}/{u3_inst_n}")
print(f"    CDLI_UR3_GIRSU_GUABBA ({gg_inst_n} tablets): Moon_PN={gg_moon_hits}/{gg_tot_theo} ({100*gg_moon_hits/max(1,gg_tot_theo):.1f}%) | Lagash_PN={corpus_cohort_pn['CDLI_UR3_GIRSU_GUABBA']['Lagash_Local']}/{gg_tot_theo} | e2_Nanna/tithe={gg_nanna_inst}/{gg_inst_n}")
print(f"    CDLI_OB_UR_LARSA ({corpus_cohort_ndocs['CDLI_OB_UR_LARSA']} tablets): Moon_PN={ob_moon_hits}/{ob_tot_theo} ({100*ob_moon_hits/max(1,ob_tot_theo):.1f}%)")
print(f"    5,000-shuffle CDLI Ur III Ur vs Girsu Moon PN enrichment: z={z_cd:+.2f}, P_perm={p_cd_ge:.4f}, OR={or_cd:.2f}, Fisher P_gt={p_cd_fgt:.4e}")
print(f"    Institutional e2 Nanna / tithe Fisher Ur III Ur vs Girsu: {u3_nanna_inst}/{u3_inst_n} vs {gg_nanna_inst}/{gg_inst_n} -> OR={or_inst:.2f}, P_gt={p_inst_fgt:.4e}")

# -----------------------------------------------------------------------------
# TEST 3B-3B: NON-SUMERIAN / MELUHHAN NAME PHONETIC TEST (5,000 SHUFFLES)
# -----------------------------------------------------------------------------
print("\n  --- TEST 3B-3B: ASSIMILATION RATE & NON-SUMERIAN MELUHHAN PHONETIC TEST (5,000 SHUFFLES) ---")

direct_ml = [d for d in proso_dicts if d["cohort"] == "MELUHHA_DIRECT_TAGGED"]
n_ml_tot = len(direct_ml)
n_ml_sum = sum(1 for d in direct_ml if d["linguistic_origin"] == "Sumerian")
n_ml_akk = sum(1 for d in direct_ml if d["linguistic_origin"].startswith("Akkadian"))
n_ml_for = sum(1 for d in direct_ml if d["linguistic_origin"] == "Non-Sumerian/Foreign_Meluhhan")
print(f"  Direct Meluhha-tagged personnel (n={n_ml_tot}):")
print(f"    Sumerian-assimilated: {n_ml_sum}/{n_ml_tot} ({100*n_ml_sum/n_ml_tot:.1f}%)")
print(f"    Akkadian/Semitic:     {n_ml_akk}/{n_ml_tot} ({100*n_ml_akk/n_ml_tot:.1f}%)")
print(f"    Non-Sumerian/Foreign: {n_ml_for}/{n_ml_tot} ({100*n_ml_for/n_ml_tot:.1f}%) -> {[d['name_norm'] + '(' + d['skel'] + ')' for d in direct_ml if d['linguistic_origin'] == 'Non-Sumerian/Foreign_Meluhhan']}")

# Our 11 zero-artifact locked Proto-Dravidian roots (from MAP.md line 3 / Key #2A)
LOCKED_11_DRAV = [
    ("220", "mīṉ", "mn"),
    ("820", "kāl", "kl"),
    ("320", "paṭi", "pt"),
    ("090", "āḷ", "l"),
    ("154", "kā", "k"),
    ("740", "kuṭ-", "kt"),
    ("400", "cikk-", "ck"),
    ("705", "kalam", "klm"),
    ("520", "vēl", "vl"),
    ("850", "kaṇ", "kn"),
    ("390", "tai", "t"),
]
# Normalize 2+ consonant skeletons for rigorous consonant-skeleton matching (1-consonant roots like k/l/t match everything trivially!)
# Test BOTH:
#   (1) Strict 2+-consonant locked Dravidian roots (8 roots: mn, kl, pt, kt, ck, klm, vl, kn) — exact OR contiguous substring inside foreign PN skeleton
#   (2) Top 25 Indus personal-name stems from values_master4.csv (strict/wide status, >=2 consonants) + Gulf hub stems (il-kavar-min, kal, ati-il, panniru-min, kutu, al)

locked_2c_roots = [(s, r, sk) for s, r, sk in LOCKED_11_DRAV if len(sk) >= 2]
locked_2c_skels = sorted({sk for _, _, sk in locked_2c_roots})

# Load top Indus name-slot stems from values_master4.csv (strict/wide with >=2 consonants)
# plus Gulf hub Dravidian compound readings from Key #2B
indus_name_stems = []
with open(ROOT / "work_data" / "values_master4.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r.get("status") in ("strict", "wide"):
            sk = to_skel(r.get("sound", ""))
            if len(sk) >= 2:
                indus_name_stems.append((r["sign"].zfill(3), r["sound"], sk))

# Deduplicate stem skeletons (keep representative sign+sound)
stem_skel_map = {}
for sg, snd, sk in indus_name_stems:
    if sk not in stem_skel_map:
        stem_skel_map[sk] = f"{sg}:{snd}"
# Add explicit Gulf hub stems from Key #2B
for sg, snd in [("803-415", "il-kavar"), ("415-220", "kavar-min"), ("061", "kal"), ("717-803", "ati-il"), ("055-220", "panniru-min"), ("603", "kutu")]:
    sk = to_skel(snd)
    if len(sk) >= 2 and sk not in stem_skel_map:
        stem_skel_map[sk] = f"{sg}:{snd}"

all_stem_skels = sorted(stem_skel_map.keys())

# Strictly non-Sumerian Meluhhan PNs (N=6) & Expanded non-Sumerian Meluhha/Gulf PNs (N=10, incl. Ba-alla, Arab-irina, Rimum, Yagli-El)
strict_foreign_pns = [(d["name_norm"], d["skel"]) for d in direct_ml if d["linguistic_origin"] == "Non-Sumerian/Foreign_Meluhhan"]
expanded_foreign_pns = strict_foreign_pns + [
    ("Ba-alla", to_skel("Ba-alla")),
    ("Arab-irina", to_skel("Arab-irina")),
    ("Rimum", to_skel("Rimum")),
    ("Yagli-El", to_skel("Yagli-El")),
]

# Consonant inventory pool for honest 5,000-shuffle null (empirical consonant frequency across all Mesopotamian/Dravidian roots & names)
CONS_POOL = list("".join(sk for sk in all_stem_skels) + "".join(sk for _, sk in expanded_foreign_pns))

def eval_phonetic_hits(pn_list, root_skels):
    exact_hits = []
    substr_hits = []
    for nm, psk in pn_list:
        if len(psk) < 2:
            continue
        for rsk in root_skels:
            if psk == rsk:
                exact_hits.append((nm, psk, rsk))
            if rsk in psk or psk in rsk:
                substr_hits.append((nm, psk, rsk))
    return exact_hits, substr_hits

def run_phonetic_perm(pn_list, root_skels, n_perm=5000, seed_offset=0):
    rng = random.Random(SEED + seed_offset)
    ex, sub = eval_phonetic_hits(pn_list, root_skels)
    obs_ex = len(ex)
    obs_sub = len(sub)
    obs_pns_hit = len({nm for nm, _, _ in sub})
    null_ex, null_sub, null_pns = [], [], []
    # Shuffle consonant identities of the root skeletons preserving exact lengths (zero adjacent-repeat)
    root_lens = [len(sk) for sk in root_skels]
    for _ in range(n_perm):
        r_rand = []
        for L in root_lens:
            seq = []
            while len(seq) < L:
                ch = rng.choice(CONS_POOL)
                if not seq or seq[-1] != ch:
                    seq.append(ch)
            r_rand.append("".join(seq))
        rex, rsub = eval_phonetic_hits(pn_list, r_rand)
        null_ex.append(len(rex))
        null_sub.append(len(rsub))
        null_pns.append(len({nm for nm, _, _ in rsub}))
    mu_e, sd_e, z_e, p_e, _ = z_and_p(obs_ex, null_ex)
    mu_s, sd_s, z_s, p_s, _ = z_and_p(obs_sub, null_sub)
    mu_p, sd_p, z_p, p_p, _ = z_and_p(obs_pns_hit, null_pns)
    return {
        "n_pns": len(pn_list),
        "n_roots": len(root_skels),
        "exact_obs": obs_ex, "exact_null": round(mu_e, 2), "exact_z": round(z_e, 2), "exact_p": round(p_e, 4),
        "exact_matches": ex,
        "substr_obs": obs_sub, "substr_null": round(mu_s, 2), "substr_z": round(z_s, 2), "substr_p": round(p_s, 4),
        "pns_hit_obs": obs_pns_hit, "pns_hit_null": round(mu_p, 2), "pns_hit_z": round(z_p, 2), "pns_hit_p": round(p_p, 4),
        "substr_matches": sub,
    }

ph_strict_11 = run_phonetic_perm(strict_foreign_pns, locked_2c_skels, 5000, 11)
ph_exp_11 = run_phonetic_perm(expanded_foreign_pns, locked_2c_skels, 5000, 12)
ph_strict_all = run_phonetic_perm(strict_foreign_pns, all_stem_skels, 5000, 13)
ph_exp_all = run_phonetic_perm(expanded_foreign_pns, all_stem_skels, 5000, 14)

# Also check vowel-inclusive / voicing-tolerant check (e.g. b/p, d/t, g/k, s/c) on the 6 strict foreign Meluhhan PNs!
def voiced_fold(sk: str) -> str:
    return sk.translate(str.maketrans("bdgz", "ptks"))

locked_vf = sorted({voiced_fold(sk) for sk in locked_2c_skels})
strict_vf = [(nm, voiced_fold(sk)) for nm, sk in strict_foreign_pns]
ph_strict_11_vf = run_phonetic_perm(strict_vf, locked_vf, 5000, 15)

print(f"  1) Strict Foreign Meluhhan PNs (n=6) vs 8 2C+ Locked Dravidian Roots:")
print(f"     Exact={ph_strict_11['exact_obs']} (null={ph_strict_11['exact_null']}, P={ph_strict_11['exact_p']}) | Substr={ph_strict_11['substr_obs']} (null={ph_strict_11['substr_null']}, z={ph_strict_11['substr_z']:+.2f}, P={ph_strict_11['substr_p']}) | hits={ph_strict_11['substr_matches']}")
print(f"  2) Strict Foreign (n=6) Voicing-Folded vs 8 Locked Dravidian Roots:")
print(f"     Exact={ph_strict_11_vf['exact_obs']} (null={ph_strict_11_vf['exact_null']}, P={ph_strict_11_vf['exact_p']}) | Substr={ph_strict_11_vf['substr_obs']} (null={ph_strict_11_vf['substr_null']}, z={ph_strict_11_vf['substr_z']:+.2f}, P={ph_strict_11_vf['substr_p']}) | hits={ph_strict_11_vf['substr_matches']}")
print(f"  3) Expanded Foreign Meluhha/Gulf PNs (n=10) vs 8 2C+ Locked Dravidian Roots:")
print(f"     Exact={ph_exp_11['exact_obs']} (null={ph_exp_11['exact_null']}, P={ph_exp_11['exact_p']}) | Substr={ph_exp_11['substr_obs']} (null={ph_exp_11['substr_null']}, z={ph_exp_11['substr_z']:+.2f}, P={ph_exp_11['substr_p']}) | hits={ph_exp_11['substr_matches']}")
print(f"  4) Strict Foreign Meluhhan PNs (n=6) vs All {len(all_stem_skels)} Indus Name Stems (values_master4 + Gulf hubs):")
print(f"     Exact={ph_strict_all['exact_obs']} (null={ph_strict_all['exact_null']}, z={ph_strict_all['exact_z']:+.2f}, P={ph_strict_all['exact_p']}) | Substr={ph_strict_all['substr_obs']} (null={ph_strict_all['substr_null']}, z={ph_strict_all['substr_z']:+.2f}, P={ph_strict_all['substr_p']}) | hits={[(nm, psk, rsk, stem_skel_map.get(rsk,'')) for nm, psk, rsk in ph_strict_all['substr_matches']]}")
print(f"  5) Expanded Foreign (n=10) vs All {len(all_stem_skels)} Indus Name Stems:")
print(f"     Exact={ph_exp_all['exact_obs']} (null={ph_exp_all['exact_null']}, z={ph_exp_all['exact_z']:+.2f}, P={ph_exp_all['exact_p']}) | Substr={ph_exp_all['substr_obs']} (null={ph_exp_all['substr_null']}, z={ph_exp_all['substr_z']:+.2f}, P={ph_exp_all['substr_p']})")

# Save complete Test 3B-3 JSON
t3b3_out = {
    "prosopography_counts": {
        "total_curated_pns": len(proso_dicts),
        "by_cohort": dict(collections.Counter(d["cohort"] for d in proso_dicts)),
        "direct_meluhha_assimilation": {
            "total": n_ml_tot,
            "Sumerian": n_ml_sum, "Sumerian_pct": round(100 * n_ml_sum / n_ml_tot, 1),
            "Akkadian_or_Ambiguous": n_ml_akk, "Akkadian_pct": round(100 * n_ml_akk / n_ml_tot, 1),
            "Non_Sumerian_Foreign": n_ml_for, "Foreign_pct": round(100 * n_ml_for / n_ml_tot, 1),
        },
    },
    "test3b3a_theophoric_calque": {
        "curated_UR3_UET3_SEATRADE": b_ur3,
        "curated_UR3_GIRSU_MELUHHA": b_girsu,
        "curated_OB_UET5_ALIK_TILMUN": b_ob,
        "perm_curated_ur3_vs_girsu_moon": {
            "obs_diff_pp": round(100 * obs_diff_ur_girsu, 1), "z": round(z_ug, 2),
            "p_perm_ge": round(p_ug_ge, 4), "fisher_or": round(or_ug, 2) if math.isfinite(or_ug) else "inf",
            "fisher_p_gt": round(p_ug_fgt, 6), "fisher_p_two": round(p_ug_f2, 6),
        },
        "perm_curated_ur3_vs_ob_moon": {
            "obs_diff_pp": round(100 * obs_diff_ur_ob, 1), "z": round(z_uo, 2),
            "p_perm_ge": round(p_uo_ge, 4), "fisher_or": round(or_uo, 2), "fisher_p_two": round(p_uo_f2, 4),
        },
        "cdli_automated_scan": {
            "n_docs": dict(corpus_cohort_ndocs),
            "pn_theophoric_hits": {k: dict(v) for k, v in corpus_cohort_pn.items()},
            "institutional_tablet_hits": {k: dict(v) for k, v in corpus_cohort_inst.items()},
            "perm_cdli_ur3_vs_girsu_moon_pn": {
                "ur3_moon": u3_moon_hits, "ur3_tot_theo": u3_tot_theo,
                "girsu_moon": gg_moon_hits, "girsu_tot_theo": gg_tot_theo,
                "z": round(z_cd, 2), "p_perm_ge": round(p_cd_ge, 4),
                "fisher_or": round(or_cd, 2), "fisher_p_gt": f"{p_cd_fgt:.3e}",
            },
            "fisher_institutional_e2_nanna": {
                "ur3_tablets": f"{u3_nanna_inst}/{u3_inst_n}",
                "girsu_tablets": f"{gg_nanna_inst}/{gg_inst_n}",
                "odds_ratio": round(or_inst, 2), "p_gt": f"{p_inst_fgt:.3e}",
            },
        },
    },
    "test3b3b_phonetic_test": {
        "locked_11_dravidian_roots": LOCKED_11_DRAV,
        "strict_foreign_meluhhan_pns": strict_foreign_pns,
        "expanded_foreign_pns": expanded_foreign_pns,
        "strict6_vs_locked8_2c": ph_strict_11,
        "strict6_voicing_folded_vs_locked8": ph_strict_11_vf,
        "expanded10_vs_locked8_2c": ph_exp_11,
        "strict6_vs_all_indus_stems": ph_strict_all,
        "expanded10_vs_all_indus_stems": ph_exp_all,
    },
}

with open(OUT_DIR / "test3b3_ur3_prosopography_stats.json", "w", encoding="utf-8") as f:
    json.dump(t3b3_out, f, indent=2)

print("\nALL OUTPUTS WRITTEN TO:", OUT_DIR)
