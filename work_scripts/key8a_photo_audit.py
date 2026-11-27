#!/usr/bin/env python3
"""key8a_photo_audit.py — Key #8A Feature 1: Photo-Audit Mini-Pass.

Generates crisp CISI photographic contact sheets paired with Mahadevan 1977 drawn
glyphs in work_data/key8a/ for:
  1. All 12 [MISSING] top FRESH390 signs:
     838, 136, 844, 250, 697, 698, 792, 515, 519, 794, 150, 042
     (sheet_042.png displays Mahadevan glyph 289.png + honest note '0 CISI photos')
     plus high-value [MISSING] FRESH signs 525, 702, 036, 263, 552, 204.
  2. Rescue / Dholavira / M284 / Gonur targets needing fresh sheets:
     315, 360, 921, 877, 880, 190, 267, 269, 456, 679, 370, 371, 285.
  3. Remaining 9 uninspected photographed Lipi 824 objects:
     work_data/key8a/sheet_824_remaining.png
     (Seals 824a: L-91, M-701, M-1297; Harappa tablets 824b: H-786, H-787, H-905,
      H-906, H-907, H-988).

Outputs:
  work_data/key8a/sheet_<sign>.png
  work_data/key8a/sheet_824_remaining.png
  work_data/key8a/selected_photos_key8a.csv
  work_data/key8a/photo_audit_key8a.csv
"""

import csv
import json
import os
import re
import sys
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(
    ROOT,
    "evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images",
)
MAP_PATH = os.path.join(
    ROOT,
    "evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/seal_id_and_image_mapping.json",
)
RAW_LIPI_PATH = os.path.join(ROOT, "evidence/tmp/lipi_current_inscriptions_20260526.csv")
SIGN_SHAPES_PATH = os.path.join(ROOT, "work_data/sign_shapes.csv")
CROSSWALK_PATH = os.path.join(ROOT, "work_data/lipi_mahadevan_crosswalk.csv")
ANCHORS_PATH = os.path.join(ROOT, "work_data/sem/sign_anchors.csv")
CORPUS_PATH = os.path.join(ROOT, "work_data/reader_v3/corpus_soundfree_readings.csv")
CLUSTER_PATH = os.path.join(ROOT, "work_data/key4d/verified_clusters_all.csv")
MAH_GLYPH_DIR = os.path.join(ROOT, "work_data/mahadevan_glyphs")

OUT_DIR = os.path.join(ROOT, "work_data/key8a")
os.makedirs(OUT_DIR, exist_ok=True)

MISSING_TOP12 = [
    "838", "136", "844", "250", "697", "698",
    "792", "515", "519", "794", "150", "042",
]
EXTRA_MISSING = ["525", "702", "036", "263", "552", "204"]
RESCUE_TARGETS = [
    "315", "360", "921", "877", "880", "190",
    "267", "269", "456", "679", "370", "371", "285",
]
ALL_SHEET_TARGETS = MISSING_TOP12 + EXTRA_MISSING + RESCUE_TARGETS

REMAINING_824_OBJS = [
    # (cisi_id, text_id, split_id, face_num)
    ("L-91", "2045.1", "824a", "1"),
    ("M-701", "3128.1", "824a", "1"),
    ("M-1297", "3602.1", "824a", "1"),
    ("H-786", "1677.1", "824b", "1"),
    ("H-787", "1678.1", "824b", "1"),
    ("H-905", "1787.1", "824b", "1"),
    ("H-906", "1788.1", "824b", "1"),
    ("H-907", "1789.2", "824b", "2"),
    ("H-988", "1864.1", "824b", "1"),
]

FACE_LETTERS = {"1": "a", "2": "b", "3": "c", "4": "d", "5": "e"}
# Explicit face-photo overrides for known inverted CISI plate labels (visually verified)
FACE_PHOTO_OVERRIDES = {
    ("H-764", "1"): "H-764_B.jpg",  # Face 1 (+697+) is plate B (UUU); plate A shows face 2 (740-717-790)
    ("H-765", "2"): "H-765_B.jpg",  # Face 2 (+697+) is plate B (UUU)
}
# Non-inscribed museum edge labels & unresolvable whole-vessel photos excluded from glyph sheets
EXCLUDED_PHOTO_FILES = {
    "M-494_E.jpg",      # Blank tablet edge painted with museum accession number "E 1515"
    "H-690_A_50_.jpg",  # Whole-pot photograph where the tiny shoulder stamp cannot be resolved
}
TIER_ORDER = {
    "TIER_1_NEW_REPLICATED": 0,
    "TIER_1B_MAH_FULL_REPLICATED": 1,
    "TIER_2_FDR_FWER": 2,
    "TIER_3_SLOT_OR_MULTITEXT_LEAD": 3,
}

# Verified visual observations from direct inspection of every generated CISI contact sheet & M77 glyph
VISUAL_AUDIT_NOTES = {
    "838": {
        "morphology": "Upright pointed oval/almond leaf or seed enclosing an inner central stem/vein (M386) or 3-pronged sprout (M389); confirmed on M-306_a, K-7_a, M-900_a",
        "discrepancy": "Wells [MISSING]; carved stone confirms oval seed/eye/leaf with inner shoot",
        "domain_a": "seed, leaf, sprout, eye, kernel, pod",
    },
    "136": {
        "morphology": "Standing human figure with horizontal shoulder-bar / yoke and vertical hanging cords/weights on both sides (M38); crystal clear on M-831_a, M-142_a, M-1162_a",
        "discrepancy": "Wells [MISSING]; clearly distinct from plain 140 (drooping arms) — carrying pole / yoke-bearer",
        "domain_a": "porter, yoke, pole, load, carrier, burden",
    },
    "844": {
        "morphology": "Two overlapping vertical ovals forming a central Venn-lens / double-almond (M406); sits directly before 390 (*tai) on M-166_a, M-115_a, M-907_a",
        "discrepancy": "Wells [MISSING]; carved stone & M406 clearly show two overlapping vertical ovals (Venn-lens / double-almond)",
        "domain_a": "oval, lens, pair, twin, eye",
    },
    "250": {
        "morphology": "Vertical crescent/arc crossed by curved/diagonal forked legs ')<' (M302); crystal clear on H-7_a (564x611), K-51_a, M-159_a",
        "discrepancy": "Wells [MISSING]; carved stone & M302 show vertical crescent/arc crossed by curved diagonal forked legs",
        "domain_a": "crescent, hook, arc, pincer, curve",
    },
    "697": {
        "morphology": "Lipi-vs-M77 crosswalk conflict: H-764_B.jpg (1656.1 +697+) and H-765_B.jpg (1657.2 +697+) show THREE side-by-side U-cups (UUU, continuing 697=UUU, 698=UU, 700=U, 702=U+2, 703=U+3), whereas M276 (83% crosswalk) is a diamond/rhombus enclosing a small top inner diamond with two diagonal strokes crossing the lower-left edge; M-495_a pos 1 is 390 (H-690_A_50_ unresolvable)",
        "discrepancy": "Wells [MISSING] AND direct carved-stone (UUU on H-764_B/H-765_B) vs Mahadevan (M276 crossed diamond) crosswalk conflict — demoted to testing_frontier_signs",
        "domain_a": "CONFLICT (UUU vs M276 crossed diamond — held)",
    },
    "698": {
        "morphology": "Tall U-shaped vessel / twin side-by-side U-cups on M-329_a (002-861-698) and U-cup on H-210_B (M-330_a shows ornate branched cup); M6 standing-man crosswalk is noisy EM on solo texts",
        "discrepancy": "Wells [MISSING] AND M6 crosswalk misleading — carved stone shows U-vessel/twin-cups, NOT standing man",
        "domain_a": "cup, vat, vessel, pot, ladle, scoop",
    },
    "792": {
        "morphology": "Doubled pair of tall upright ovals/rings with inner vertical slits (OO) side-by-side; crystal clear on M-953_a (792-740), M-853_a, M-926_a",
        "discrepancy": "Wells [MISSING] and M77 unmapped; clearly twin/paired ovals (doubled 838/798)",
        "domain_a": "pair, twin, eye, ring, double, couple",
    },
    "515": {
        "morphology": "Tall vertical post/shaft topped by a pointed roof/chevron cap with downward side ticks (M155); clear on M-779_a, M-1095_a, K-9_a",
        "discrepancy": "Wells [MISSING]; clearly single pointed roof-post/arrow-pillar (base of doubled 519)",
        "domain_a": "pillar, post, spear, arrow, roof, pole",
    },
    "519": {
        "morphology": "Twin/doubled pointed caret-capped vertical posts (^|^|) side-by-side; crystal clear on M-327_a, M-264_a, L-98_a",
        "discrepancy": "Wells [MISSING] and M292/M114 split noisy; carved stone proves exact doubled 515 (twin huts/pillars)",
        "domain_a": "hut, pillar, tent, fence, pair, post",
    },
    "794": {
        "morphology": "Bulging vertical oval body with twin splayed prongs at top and bottom (hourglass/waisted-drum outline, M58); crystal clear on M-89_a, M-1091_a, M-852_a",
        "discrepancy": "Wells [MISSING]; carved stone & M58 show bulging vertical oval body with twin splayed top/bottom prongs (hourglass-drum outline)",
        "domain_a": "drum, hourglass, waist, mortar, cup, pot",
    },
    "150": {
        "morphology": "Standing human figure under a flat horizontal top lintel/canopy with bent arms (M10); razor-sharp on M-1092_a.jpg, confirmed on M-252_a.jpg and M-495_b.jpg (M-494_E.jpg excluded as blank museum edge label)",
        "discrepancy": "Wells [MISSING]; carved stone & M10 show standing figure beneath flat horizontal top lintel/canopy with bent arms",
        "domain_a": "lintel, canopy, awning, arch, porch",
    },
    "042": {
        "morphology": "0 CISI photos in seal_images/; Mahadevan glyph M289 (289.png) shows right crescent ')' (920 *tiṅkaḷ) flanked by 4 corner stroke clusters (cage_4corners / side_brackets operator)",
        "discrepancy": "Wells [MISSING]; 0 CISI photos in seal_images/ (verified via Mahadevan 289.png); M289 confirms transparent Key #4A operator derivative of 920 (*tiṅkaḷ) + cage_4corners",
        "domain_a": "crescent, horn, arc, bracket, cage",
    },
    "525": {
        "morphology": "Stepped/crooked rectangular shutter/gate frame with twin horizontal bars between offset vertical posts (M254); confirmed on M-1390_A (1062x700) and H-774_A in 550-525-400",
        "discrepancy": "Wells [MISSING]; photo + M254 glyph confirm exact graphic/distributional allograph of locked 527",
        "domain_a": "gate, shutter, bar, frame, door, latch",
    },
    "702": {
        "morphology": "U-shaped cup (700) containing TWO short vertical strokes inside its open top (M329); crystal clear on M-192_a (contrasting directly with 700), H-408_a, H-450_a — exact 2-stroke mirror of locked 703 (U+3)",
        "discrepancy": "Wells [MISSING]; carved stone & M329 confirm transparent 700-series U-cup + 2 inner strokes operator derivative (*iru-aḷa/*iru-akal)",
        "domain_a": "cup, vessel, two-stroke measure (700+2 transparent operator)",
    },
    "036": {
        "morphology": "Six tall parallel vertical strokes (||||||); crystal clear on K-4_a and M-20_a",
        "discrepancy": "Wells [MISSING]; carved stone 100% confirms transparent numeral 6 (*āṟu)",
        "domain_a": "six, strokes, tally, count",
    },
    "263": {
        "morphology": "Left-facing profile bird/duck/waterfowl with upturned tail and legs (M76); crystal clear on M-700_a, M-631_a, M-366_a; Key #4D allograph of 260",
        "discrepancy": "Wells [MISSING]; photo confirms exact visual identity with 260 (M76 profile bird)",
        "domain_a": "bird, duck, heron, fowl, crane, crow",
    },
    "552": {
        "morphology": "Horizontal bowtie / double-triangle (><) closed on left, forked/open on right (M217); clear on M-162_a, M-126_a, M-198_a",
        "discrepancy": "Wells [MISSING]; photo confirms bowtie family (550/554/555 *nāṭu)",
        "domain_a": "bowtie, knot, hourglass, drum, tie",
    },
    "315": {
        "morphology": "Tall H-shaped wooden frame / portal with twin vertical posts joined by central horizontal bar (M186); clear on M-1100_a, L-39_a, M-274_a",
        "discrepancy": "Matches Wells 'Large H'; Key #4D twin of 360",
        "domain_a": "frame, gate, portal, loom, stool, bench",
    },
    "360": {
        "morphology": "Tall H-shaped wooden frame / portal with twin vertical posts joined by crossbar (M202); clear on M-932_a, M-129_a, M-954_a",
        "discrepancy": "Matches Wells 'Large H'; visually & Key #4D identical twin of 315",
        "domain_a": "frame, gate, portal, loom, stool, bench",
    },
    "921": {
        "morphology": "Curved vertical bow-stave '(' with central hand-grip / arrow-nock semicircle (M301); crisp on M-779_a, H-64_a, M-239_a",
        "discrepancy": "Wells calls it 'left parenthesis with semicircle' — carved stone clearly shows a drawn bow (*vil)",
        "domain_a": "bow, arch, arc, curve, bend",
    },
    "877": {
        "morphology": "Large quartered diamond divided by internal cross into 4 small diamonds/quarters (M284); crisp on M-874_a, M-217_a, M-880_a (where it sits directly beside 861 *kāṇam!)",
        "discrepancy": "Matches Wells 'Diamond with four small diamonds'; visually 4x tiled 861 (*kāṇam) quarters",
        "domain_a": "quarter, diamond, four, share, wheel, cross",
    },
    "880": {
        "morphology": "Outer diamond (861) enclosing an internal 6-spoked wheel (820) or 4-vertex diamond-wheel (M286); museum-grade clarity on M-6_a (692x739, directly beside 820!), M-296_a, M-225_a",
        "discrepancy": "Matches Wells 'Diamond...wagon wheel in center'; visually explicit 861+820 compound (*kāṇam + *kāl)",
        "domain_a": "wheel, diamond, quarter, spoke, cart, circle",
    },
    "190": {
        "morphology": "Central oval body with two pairs of splayed curved pincers/legs on left and right (M54); crystal clear on M-624_a (628x663), M-153_a, M-1087_a",
        "discrepancy": "Wells says 'squashed spider' — carved stone clearly shows crab/scorpion pincers + splayed legs",
        "domain_a": "crab, scorpion, spider, pincers, claw, insect",
    },
    "267": {
        "morphology": "Small upright bird/chick enclosed inside twin curved parentheses '(bird)' (M81); crisp on M-920_a, M-214_a, M-10_a",
        "discrepancy": "Matches Wells; literally a caged bird / bird in nest/coop (*kūṭu)",
        "domain_a": "birdcage, nest, coop, cage, bird, fowl",
    },
    "269": {
        "morphology": "Upright bird enclosed inside twin curved parentheses '(bird)' (M81); crisp on M-153_a, H-580_a, M-1127_a; visually & Key #4D identical to 267",
        "discrepancy": "Matches Wells; Key #4D cluster twin of 267/221 (caged bird / nest *kūṭu)",
        "domain_a": "birdcage, nest, coop, cage, bird, fowl",
    },
    "456": {
        "morphology": "455 three-triangle butterfly/knot capped by a flat horizontal table/roof bar on top (M234); museum-grade clarity on M-1264_a (542x240), M-219_a, M-1150_1_a",
        "discrepancy": "Matches Wells; transparent roof-hat derivative of 455 (parallel to 645->679)",
        "domain_a": "knot, hook, clasp, roof, cover, wing",
    },
    "679": {
        "morphology": "645 diagonal X-cross capped by a flat horizontal table/roof canopy bar on top (M139); crisp on M-267_a, M-653_a, H-421_a",
        "discrepancy": "Matches Wells 'An X with a table hat'; transparent roof/shelter derivative of 645",
        "domain_a": "roof, canopy, shelter, shed, cot, terrace",
    },
    "370": {
        "morphology": "Vertical spindle shaft passing through a round central whorl with dot (M397); clear on M-644_A (465x531), H-796_A, M-436_A",
        "discrepancy": "Wells calls it 'garlic motif' — carved stone shows drop-spindle with whorl (*katir); Key #4D twin of 371",
        "domain_a": "spindle, whorl, shaft, rod, pin, bulb",
    },
    "371": {
        "morphology": "Vertical spindle shaft passing through a round central whorl with dot (M397); museum-grade clarity on M-1_a (554x635), M-12_a (469x529), M-981_a",
        "discrepancy": "Wells calls it 'garlic motif' — carved stone shows textbook drop-spindle with whorl (*katir)",
        "domain_a": "spindle, whorl, shaft, rod, pin, bulb",
    },
    "285": {
        "morphology": "Domed/arched 4-legged body with a tufted/forked crest or plume rising from the top (M395); clear on K-28_a, L-85_a, M-1358_a",
        "discrepancy": "Wells says 'oval with strokes + small tree at top'; carved stone shows crested/tufted bird/tortoise/comb-body",
        "domain_a": "crest, tuft, plume, comb, tortoise, peacock",
    },
    "204": {
        "morphology": "Two vertical joined ovals with four splayed legs/bristles top-right and bottom-right (M56, Mahadevan arthropod block M54–M58); razor-sharp on M-396_a.jpg pos 1 and M-685_a.jpg pos 2",
        "discrepancy": "Matches Wells ('Two stacked leaves, with lines coming away on the right of each leaf'); carved stone & M56 show two joined vertical ovals with four splayed legs/bristles (arthropod/insect block)",
        "domain_a": "crab, spider, scorpion, beetle, insect",
    },
}


def load_font(size=14, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def parse_raw_text(text_str, direction):
    cleaned = str(text_str).strip()
    cleaned = re.sub(r"^[+\]\[]+|[+\]\[]+$", "", cleaned)
    raw_toks = [t.strip().zfill(3) for t in cleaned.split("-") if t.strip() and t.strip().isdigit()]
    if str(direction).strip() == "R/L":
        read_toks = raw_toks[::-1]
    else:
        read_toks = raw_toks[:]
    return raw_toks, read_toks


def pick_best_image(cisi_files, face_num="1", cisi=None):
    # Check explicit face-photo overrides for known inverted CISI plate labels first
    if cisi is not None and (cisi, str(face_num)) in FACE_PHOTO_OVERRIDES:
        fn = FACE_PHOTO_OVERRIDES[(cisi, str(face_num))]
        fp = os.path.join(IMG_DIR, fn)
        if os.path.exists(fp):
            with Image.open(fp) as im:
                w, h = im.size
            fsize = os.path.getsize(fp)
            return fn, w, h, fsize, [fn]

    letter = FACE_LETTERS.get(str(face_num), "a")
    scored = []
    for fn in cisi_files:
        if fn in EXCLUDED_PHOTO_FILES:
            continue
        fp = os.path.join(IMG_DIR, fn)
        if not os.path.exists(fp):
            continue
        try:
            with Image.open(fp) as im:
                w, h = im.size
        except Exception:
            continue
        fsize = os.path.getsize(fp)
        low = fn.lower()
        m_face = re.search(rf"_{letter}(?:[._]|$)", low)
        is_bis = "_bis" in low
        is_exact_letter = bool(m_face)
        # For non-primary faces (face 2+), require exact single-face match to avoid grabbing edge/wrong-face plates
        if str(face_num) != "1" and not is_exact_letter:
            continue
        is_other_face = bool(re.search(r"_[bcdef](?:[._]|$)", low)) and letter == "a"
        score = (
            (100 if is_exact_letter else (0 if is_other_face else 40))
            + (10 if not is_bis else 8)
            + min(w * h / 50000.0, 20.0)
        )
        scored.append((score, w * h, fsize, w, h, fn, is_exact_letter))
    if not scored:
        return None
    scored.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    best = scored[0]
    same_face = [x[5] for x in scored if x[6]]
    return best[5], best[3], best[4], best[2], same_face


def score_candidate_row(row, target_sign):
    read_toks = row["read_toks"]
    n = len(read_toks)
    typ = row["type"]
    cond = row["condition"]
    comp = row["complete"]
    has_000 = "000" in read_toks

    s = 0.0
    if comp == "Y" and not has_000:
        s += 100.0
    elif not has_000:
        s += 40.0

    if typ == "SEAL:S":
        s += 50.0
    elif typ == "SEAL:R":
        s += 38.0
    elif typ.startswith("SEAL"):
        s += 30.0
    elif typ in ("TAB:B", "TAB:I", "TAB:C"):
        s += 20.0
    else:
        s += 10.0

    if 2 <= n <= 5:
        s += 35.0
    elif n == 6:
        s += 25.0
    elif n == 7:
        s += 18.0
    elif n == 1:
        s += 22.0
    else:
        s += max(5.0, 20.0 - n)

    if cond == "Good":
        s += 15.0
    elif cond == "Fair":
        s += 7.0

    area = row["img_w"] * row["img_h"]
    s += min(area / 40000.0, 25.0)
    if str(row["id"]).endswith(".1"):
        s += 12.0
    if read_toks.count(target_sign) == 1:
        s += 3.0
    return s


def build_sign_meta():
    shapes_df = pd.read_csv(SIGN_SHAPES_PATH, dtype=str).fillna("")
    shapes_map = {}
    for _, r in shapes_df.iterrows():
        s = str(r.get("lipi_wells_number", "")).strip().zfill(3)
        shapes_map[s] = {
            "shape_desc": r.get("shape_description", "").strip(),
            "parpola": r.get("mayig_code", "").strip(),
        }

    cw_df = pd.read_csv(CROSSWALK_PATH, dtype=str).fillna("")
    cw_map = {}
    for _, r in cw_df.iterrows():
        s = str(r.get("lipi", "")).strip().zfill(3)
        m = str(r.get("mahadevan", "")).strip()
        if not m or m in ("0", "-"):
            continue
        cnt = int(float(r.get("text_positions", 0) or 0))
        share = float(r.get("share_of_lipi_sign", 0) or 0)
        cw_map.setdefault(s, []).append((cnt, m, share))

    anch_df = pd.read_csv(ANCHORS_PATH, dtype=str).fillna("")
    anch_map = {}
    for _, r in anch_df.iterrows():
        s = str(r.get("sign", "")).strip().zfill(3)
        tier = r.get("anchor_tier", "").strip()
        desc = r.get("pinned_domain", "").strip()
        slot = r.get("slot", "").strip()
        rank = TIER_ORDER.get(tier, 99)
        anch_map.setdefault(s, []).append((rank, f"{tier}: {desc} ({slot})"))
    best_anch = {}
    for s, lst in anch_map.items():
        lst.sort(key=lambda x: x[0])
        best_anch[s] = lst[0][1]

    cl_df = pd.read_csv(CLUSTER_PATH, dtype=str).fillna("")
    cl_map = {}
    for _, r in cl_df.iterrows():
        head = str(r.get("canonical", "")).strip().zfill(3)
        members = [x.strip().zfill(3) for x in str(r.get("members", "")).split("|") if x.strip()]
        for m in members:
            cl_map[m] = f"{head}-cl ({'|'.join(members)})"

    corp_df = pd.read_csv(CORPUS_PATH, dtype=str).fillna("")
    int_comb = Counter()
    int_lipi = Counter()
    int_new = Counter()
    left_nb = {}
    right_nb = {}
    sites_c = {}
    kinds_c = {}
    pos_c = {}
    for _, r in corp_df.iterrows():
        cat = r["catalogue"]
        part = r["partnered"]
        intact = r["intact"]
        if not ((cat == "Lipi" or part == "False") and intact == "True"):
            continue
        toks = [x.strip().zfill(3) for x in r["signs"].split("-") if x.strip() and x.strip().isdigit()]
        n = len(toks)
        for i, t in enumerate(toks):
            int_comb[t] += 1
            if cat == "Lipi":
                int_lipi[t] += 1
            else:
                int_new[t] += 1
            left_nb.setdefault(t, Counter())[toks[i - 1] if i > 0 else "BOS"] += 1
            right_nb.setdefault(t, Counter())[toks[i + 1] if i < n - 1 else "EOS"] += 1
            sites_c.setdefault(t, Counter())[r.get("site", "?")] += 1
            kinds_c.setdefault(t, Counter())[r.get("type", r.get("kind", "?"))] += 1
            pc = pos_c.setdefault(t, Counter())
            if n == 1:
                pc["solo"] += 1
            elif i == 0:
                pc["init"] += 1
            elif i == n - 1:
                pc["fin"] += 1
            else:
                pc["med"] += 1

    meta = {}
    for s in set(ALL_SHEET_TARGETS) | {"824"}:
        cw_list = sorted(cw_map.get(s, []), key=lambda x: x[0], reverse=True)
        mah_nums = []
        m77_parts = []
        for cnt, m, sh in cw_list[:3]:
            pct = f"{100.0 * sh:.0f}%"
            mah_nums.append((m, pct))
            m77_parts.append(f"M{m}({pct})")
        pc = pos_c.get(s, Counter())
        tot_p = sum(pc.values()) or 1
        meta[s] = {
            "m77_str": "/".join(m77_parts) if m77_parts else "M?",
            "mah_nums": mah_nums,
            "parpola": shapes_map.get(s, {}).get("parpola", ""),
            "shape_desc": shapes_map.get(s, {}).get("shape_desc", ""),
            "intact_total": f"{int_comb[s]} ({int_lipi[s]}L/{int_new[s]}N)",
            "intact_comb": int_comb[s],
            "intact_lipi": int_lipi[s],
            "intact_new": int_new[s],
            "top_anchor": best_anch.get(s, "-"),
            "top_L": ", ".join(f"{k}({v})" for k, v in left_nb.get(s, Counter()).most_common(4)),
            "top_R": ", ".join(f"{k}({v})" for k, v in right_nb.get(s, Counter()).most_common(4)),
            "init_pct": f"{100.0 * pc['init'] / tot_p:.0f}",
            "med_pct": f"{100.0 * pc['med'] / tot_p:.0f}",
            "fin_pct": f"{100.0 * pc['fin'] / tot_p:.0f}",
            "top_sites": ", ".join(f"{k}:{v}" for k, v in sites_c.get(s, Counter()).most_common(3)),
            "top_kinds": ", ".join(f"{k}:{v}" for k, v in kinds_c.get(s, Counter()).most_common(3)),
            "key4d_cluster": cl_map.get(s, "-"),
        }
    return meta


def make_contact_sheet(sign, meta_info, picked_rows, out_path):
    n_imgs = max(len(picked_rows), 1)
    left_w = 340
    cell_w = 400
    pad = 16
    header_h = 66
    body_h = 600
    total_w = left_w + pad + n_imgs * (cell_w + pad)
    total_h = header_h + body_h + pad

    canvas = Image.new("RGB", (total_w, total_h), (250, 250, 248))
    dr = ImageDraw.Draw(canvas)
    f_title = load_font(20, bold=True)
    f_bold = load_font(13, bold=True)
    f_reg = load_font(12, bold=False)
    f_sm = load_font(11, bold=False)

    dr.rectangle([0, 0, total_w, header_h], fill=(30, 42, 58))
    m77_str = meta_info.get("m77_str", "?")
    parp_str = meta_info.get("parpola", "")
    tot_str = meta_info.get("intact_total", "?")
    title = f"Key #8A Photo Audit — Lipi Sign {sign}  |  {m77_str}  {parp_str}  |  Intact: {tot_str}"
    dr.text((16, 10), title, fill=(255, 255, 255), font=f_title)
    sub = f"Wells shape_desc: {meta_info.get('shape_desc') or '[MISSING]'}"
    dr.text((16, 38), sub[:160], fill=(215, 230, 245), font=f_reg)

    lx, ly = 12, header_h + 12
    dr.rectangle([lx, ly, left_w - 6, total_h - pad], fill=(255, 255, 255), outline=(190, 195, 205))
    cur_y = ly + 10
    dr.text((lx + 10, cur_y), "Mahadevan 1977 Drawn Glyph(s):", fill=(20, 30, 50), font=f_bold)
    cur_y += 22

    mah_nums = meta_info.get("mah_nums", [])
    gx = lx + 12
    max_gh = 0
    for mn, share in mah_nums[:3]:
        gpath = os.path.join(MAH_GLYPH_DIR, f"{mn}.png")
        if os.path.exists(gpath):
            try:
                gim = Image.open(gpath).convert("RGBA")
                bg = Image.new("RGB", gim.size, (255, 255, 255))
                bg.paste(gim, mask=gim.split()[3] if len(gim.split()) == 4 else None)
                bg.thumbnail((92, 92))
                canvas.paste(bg, (gx, cur_y))
                dr.rectangle([gx - 1, cur_y - 1, gx + bg.width, cur_y + bg.height], outline=(160, 165, 175))
                dr.text((gx, cur_y + bg.height + 3), f"M{mn} ({share})", fill=(40, 40, 40), font=f_sm)
                gx += 102
                max_gh = max(max_gh, bg.height + 20)
            except Exception:
                pass
    cur_y += max(max_gh, 25) + 12

    info_lines = [
        ("Top Anchor:", meta_info.get("top_anchor", "-") or "-"),
        ("Top Left:", meta_info.get("top_L", "-") or "-"),
        ("Top Right:", meta_info.get("top_R", "-") or "-"),
        ("Positions:", f"init={meta_info.get('init_pct','?')}% med={meta_info.get('med_pct','?')}% fin={meta_info.get('fin_pct','?')}%"),
        ("Top Sites:", meta_info.get("top_sites", "-") or "-"),
        ("Top Kinds:", meta_info.get("top_kinds", "-") or "-"),
        ("4D Cluster:", meta_info.get("key4d_cluster", "-") or "-"),
    ]
    for k, v in info_lines:
        dr.text((lx + 10, cur_y), k, fill=(25, 60, 110), font=f_bold)
        cur_y += 16
        words = str(v).split()
        line = ""
        for w in words:
            if len(line) + len(w) + 1 > 42:
                dr.text((lx + 14, cur_y), line, fill=(35, 35, 35), font=f_sm)
                cur_y += 14
                line = w
            else:
                line = (line + " " + w).strip()
        if line:
            dr.text((lx + 14, cur_y), line, fill=(35, 35, 35), font=f_sm)
            cur_y += 16
        cur_y += 4
        if cur_y > total_h - 30:
            break

    if not picked_rows:
        cx = left_w + pad
        cy = header_h + 12
        dr.rectangle([cx, cy, cx + cell_w, total_h - pad], fill=(255, 250, 245), outline=(180, 120, 100))
        dr.text((cx + 20, cy + 40), "0 CISI photos available in seal_images/", fill=(160, 30, 30), font=f_bold)
        dr.text((cx + 20, cy + 70), "Inspected via Mahadevan 1977 drawn glyph", fill=(50, 50, 50), font=f_reg)
        if mah_nums:
            gpath = os.path.join(MAH_GLYPH_DIR, f"{mah_nums[0][0]}.png")
            if os.path.exists(gpath):
                gim = Image.open(gpath).convert("RGBA")
                bg = Image.new("RGB", gim.size, (255, 255, 255))
                bg.paste(gim, mask=gim.split()[3] if len(gim.split()) == 4 else None)
                bg = bg.resize((220, 220), Image.Resampling.LANCZOS)
                canvas.paste(bg, (cx + 90, cy + 120))
                dr.rectangle([cx + 89, cy + 119, cx + 310, cy + 340], outline=(120, 120, 120))
                dr.text((cx + 120, cy + 350), f"Enlarged M{mah_nums[0][0]} glyph", fill=(40, 40, 40), font=f_bold)
        canvas.save(out_path)
        return

    for idx, r in enumerate(picked_rows):
        cx = left_w + pad + idx * (cell_w + pad)
        cy = header_h + 12
        dr.rectangle([cx, cy, cx + cell_w, total_h - pad], fill=(255, 255, 255), outline=(180, 185, 195))

        cisi = r["cisi"]
        fn = r["img_file"]
        site = r["site"]
        typ = r["type"]
        direction = r["dir."]
        vis_seq = "-".join(r["vis_toks"])
        read_seq = "-".join(r["read_toks"])
        vis_pos = [i + 1 for i, t in enumerate(r["vis_toks"]) if t == sign]
        read_pos = [i + 1 for i, t in enumerate(r["read_toks"]) if t == sign]

        dr.text((cx + 8, cy + 6), f"#{idx+1}  {cisi} ({site}, {typ}) — {fn}", fill=(15, 35, 70), font=f_bold)
        dr.text((cx + 8, cy + 23), f"Read ({direction}): {read_seq}  [pos {read_pos}]", fill=(160, 25, 25), font=f_sm)
        dr.text((cx + 8, cy + 38), f"Raw L->R: {vis_seq}  [L->R pos {vis_pos}]", fill=(50, 50, 50), font=f_sm)
        dr.text((cx + 8, cy + 52), f"Res: {r['img_w']}x{r['img_h']} | Cond: {r['condition']} | Sym: {r['symbol']}", fill=(90, 90, 90), font=f_sm)

        fp = os.path.join(IMG_DIR, fn)
        im = Image.open(fp).convert("RGB")
        full_box_h = 340 if typ == "SEAL:S" else 460
        im_full = im.copy()
        im_full.thumbnail((cell_w - 16, full_box_h))
        px = cx + (cell_w - im_full.width) // 2
        py = cy + 72
        canvas.paste(im_full, (px, py))

        if typ == "SEAL:S":
            crop_h = int(im.height * 0.40)
            band = im.crop((0, 0, im.width, max(crop_h, 20)))
            scale = min((cell_w - 16) / band.width, 145 / band.height)
            band_z = band.resize(
                (max(1, int(band.width * scale)), max(1, int(band.height * scale))),
                Image.Resampling.LANCZOS,
            )
            by = cy + 72 + full_box_h + 10
            dr.text((cx + 8, by), "Zoomed top inscription band:", fill=(140, 30, 30), font=f_sm)
            bx = cx + (cell_w - band_z.width) // 2
            canvas.paste(band_z, (bx, by + 16))
            dr.rectangle([bx - 1, by + 15, bx + band_z.width, by + 16 + band_z.height], outline=(180, 40, 40))

    canvas.save(out_path)


def make_824_remaining_sheet(raw_df, img_map, out_path):
    """Build a 3x3 contact sheet for the 9 remaining uninspected photographed 824 objects."""
    cell_w = 420
    cell_h = 380
    pad = 14
    header_h = 62
    cols = 3
    rows = 3
    total_w = pad + cols * (cell_w + pad)
    total_h = header_h + pad + rows * (cell_h + pad)

    canvas = Image.new("RGB", (total_w, total_h), (248, 248, 245))
    dr = ImageDraw.Draw(canvas)
    f_title = load_font(19, bold=True)
    f_bold = load_font(13, bold=True)
    f_reg = load_font(12, bold=False)
    f_sm = load_font(11, bold=False)

    dr.rectangle([0, 0, total_w, header_h], fill=(30, 42, 58))
    dr.text((16, 10), "Key #8A — Remaining 9 Uninspected Photographed Lipi 824 Objects", fill=(255, 255, 255), font=f_title)
    dr.text((16, 36), "Row 1: Seals (824a: L-91, M-701, M-1297)   |   Rows 2–3: Harappa Tablets (824b: H-786, H-787, H-905, H-906, H-907, H-988)", fill=(215, 230, 245), font=f_reg)

    selected_rows = []
    for idx, (cisi, text_id, split_id, face_num) in enumerate(REMAINING_824_OBJS):
        sub = raw_df[raw_df["id"] == text_id]
        if sub.empty:
            continue
        r = sub.iloc[0]
        vis_toks, read_toks = parse_raw_text(r["text"], r["dir."])
        files = img_map.get(cisi, [])
        picked = pick_best_image(files, face_num=face_num, cisi=cisi)
        if not picked:
            continue
        fn, w, h, fsize, _ = picked

        col = idx % cols
        row_i = idx // cols
        cx = pad + col * (cell_w + pad)
        cy = header_h + pad + row_i * (cell_h + pad)
        border_col = (40, 110, 180) if split_id == "824a" else (180, 90, 30)
        dr.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=(255, 255, 255), outline=border_col, width=2)

        tag = f"[{split_id}] {cisi} ({r['site']}, {r['type']})"
        dr.text((cx + 8, cy + 6), tag, fill=border_col, font=f_bold)
        dr.text((cx + 8, cy + 23), f"Read ({r['dir.']}): {'-'.join(read_toks)}  |  File: {fn}", fill=(30, 30, 30), font=f_sm)
        dr.text((cx + 8, cy + 38), f"Raw L->R: {'-'.join(vis_toks)}  |  {w}x{h}  |  Complete: {r['complete']}", fill=(90, 90, 90), font=f_sm)

        fp = os.path.join(IMG_DIR, fn)
        im = Image.open(fp).convert("RGB")
        im_full = im.copy()
        im_full.thumbnail((cell_w - 16, 200))
        px = cx + (cell_w - im_full.width) // 2
        py = cy + 58
        canvas.paste(im_full, (px, py))

        # Zoom crop: top 40% for square seals, full scaled zoom for tablets/rect seals
        if r["type"] == "SEAL:S":
            band = im.crop((0, 0, im.width, max(int(im.height * 0.42), 20)))
        else:
            band = im
        scale = min((cell_w - 16) / band.width, 105 / band.height)
        band_z = band.resize(
            (max(1, int(band.width * scale)), max(1, int(band.height * scale))),
            Image.Resampling.LANCZOS,
        )
        by = cy + 265
        bx = cx + (cell_w - band_z.width) // 2
        canvas.paste(band_z, (bx, by))
        dr.rectangle([bx - 1, by - 1, bx + band_z.width, by + band_z.height], outline=(180, 40, 40))

        selected_rows.append({
            "target_sign": f"824_{split_id}",
            "rank": idx + 1,
            "text_id": text_id,
            "cisi": cisi,
            "site": r["site"],
            "type": r["type"],
            "dir": r["dir."],
            "complete": r["complete"],
            "read_seq": "-".join(read_toks),
            "vis_seq": "-".join(vis_toks),
            "img_file": fn,
            "img_res": f"{w}x{h}",
        })

    canvas.save(out_path)
    return selected_rows


def main():
    raw_df = pd.read_csv(RAW_LIPI_PATH, dtype=str).fillna("")
    with open(MAP_PATH, encoding="utf-8") as f:
        img_map = json.load(f)

    # Pre-parse tokens
    vis_list, read_list = [], []
    for _, r in raw_df.iterrows():
        vt, rt = parse_raw_text(r["text"], r["dir."])
        vis_list.append(vt)
        read_list.append(rt)
    raw_df["vis_toks"] = vis_list
    raw_df["read_toks"] = read_list

    meta = build_sign_meta()
    selected_all = []
    audit_rows = []

    for sign in ALL_SHEET_TARGETS:
        bucket = (
            "MISSING_TOP12" if sign in MISSING_TOP12
            else ("EXTRA_MISSING" if sign in EXTRA_MISSING else "RESCUE_TARGET")
        )
        cands = []
        seen_cisi = set()
        for _, r in raw_df.iterrows():
            if sign not in r["read_toks"]:
                continue
            cisi = r["cisi"].strip()
            if not cisi or cisi not in img_map:
                continue
            face_num = str(r["id"]).split(".")[-1] if "." in str(r["id"]) else "1"
            picked = pick_best_image(img_map[cisi], face_num=face_num, cisi=cisi)
            if not picked:
                continue
            fn, w, h, fsize, _ = picked
            rec = r.to_dict()
            rec["img_file"] = fn
            rec["img_w"] = w
            rec["img_h"] = h
            rec["score"] = score_candidate_row(rec, sign)
            if (cisi, face_num) in FACE_PHOTO_OVERRIDES:
                rec["score"] += 15.0
            cands.append(rec)

        cands.sort(key=lambda x: x["score"], reverse=True)
        picked_rows = []
        for c in cands:
            if c["cisi"] in seen_cisi:
                continue
            seen_cisi.add(c["cisi"])
            picked_rows.append(c)
            if len(picked_rows) >= 3:
                break

        out_png = os.path.join(OUT_DIR, f"sheet_{sign}.png")
        make_contact_sheet(sign, meta[sign], picked_rows, out_png)

        for rank, r in enumerate(picked_rows, 1):
            selected_all.append({
                "target_sign": sign,
                "rank": rank,
                "text_id": r["id"],
                "cisi": r["cisi"],
                "site": r["site"],
                "type": r["type"],
                "dir": r["dir."],
                "complete": r["complete"],
                "read_seq": "-".join(r["read_toks"]),
                "vis_seq": "-".join(r["vis_toks"]),
                "img_file": r["img_file"],
                "img_res": f"{r['img_w']}x{r['img_h']}",
            })

        note = VISUAL_AUDIT_NOTES.get(sign, {})
        audit_rows.append({
            "sign": sign,
            "bucket": bucket,
            "m77": meta[sign]["m77_str"],
            "intact_comb": meta[sign]["intact_comb"],
            "intact_lipi": meta[sign]["intact_lipi"],
            "intact_new": meta[sign]["intact_new"],
            "n_photos_sheet": len(picked_rows),
            "cisi_ids_inspected": "|".join(r["cisi"] for r in picked_rows) if picked_rows else "NONE (M77 glyph only)",
            "wells_shape_desc": meta[sign]["shape_desc"] or "[MISSING]",
            "carved_stone_morphology": note.get("morphology", "PENDING_VISUAL_INSPECTION"),
            "wells_discrepancy": note.get("discrepancy", "PENDING"),
            "visual_domain_a_candidate": note.get("domain_a", "PENDING"),
        })

    # Remaining 9 uninspected 824 objects
    out_824 = os.path.join(OUT_DIR, "sheet_824_remaining.png")
    sel_824 = make_824_remaining_sheet(raw_df, img_map, out_824)
    selected_all.extend(sel_824)

    # Save selected_photos_key8a.csv
    sel_path = os.path.join(OUT_DIR, "selected_photos_key8a.csv")
    with open(sel_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "target_sign", "rank", "text_id", "cisi", "site", "type",
            "dir", "complete", "read_seq", "vis_seq", "img_file", "img_res",
        ])
        w.writeheader()
        w.writerows(selected_all)

    # Save photo_audit_key8a.csv
    aud_path = os.path.join(OUT_DIR, "photo_audit_key8a.csv")
    with open(aud_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "sign", "bucket", "m77", "intact_comb", "intact_lipi", "intact_new",
            "n_photos_sheet", "cisi_ids_inspected", "wells_shape_desc",
            "carved_stone_morphology", "wells_discrepancy", "visual_domain_a_candidate",
        ])
        w.writeheader()
        w.writerows(audit_rows)

    print(f"[key8a_photo_audit] Generated {len(ALL_SHEET_TARGETS)} sign sheets + sheet_824_remaining.png in {OUT_DIR}")
    print(f"[key8a_photo_audit] Wrote {len(selected_all)} selected photo rows -> {sel_path}")
    print(f"[key8a_photo_audit] Wrote {len(audit_rows)} audit rows -> {aud_path}")


if __name__ == "__main__":
    main()
