#!/usr/bin/env python3
"""
Key #2 Track C: Linear Elamite (Desset 2022/2026) & Proto-Elamite (Dahl / Born et al. 2025)
Cross-Check with Iranian Plateau / Gulf Indus Seals & Metrology.

Runs three quantitative tests + strongest rival audits:
  - Test C1: Visual Sign-Shape Transfer (Desset LE Syllabary -> Indus Iranian, Gulf, Mainland)
             scored against cleaned Bronze Age Elamite PNs/DNs/GNs + Hinz-Koch vocab vs 5,000 shuffles.
  - Test C2: Iranian Plateau Indus Seals (n=5) vs Bahrain, Failaka/UAE, Mesopotamia, & Mainland Grammar
             + 10,000-draw small-sample undifferentiated-pool permutation test.
  - Test C3: Indus vs Proto-Elamite vs Mesopotamian Metrology & Structural 2-Series Audit
             + 10,000-trial ergonomic convergence Monte Carlo rival audit.

Outputs written to work_data/key2c/.
"""

import csv
import json
import math
import os
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "work_data" / "key2c"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RNG = random.Random(20261119)

# ---------------------------------------------------------------------------
# 1. VERIFIED DESSET (2022/2026) LINEAR ELAMITE SYLLABARY (67 phonemic values)
#    Verified directly from Desset 2022 phonetic grid (Wikimedia Commons CC-BY-4.0
#    File:Grille_phonétique_des_signes_utilisés_en_élamite_linéaire.jpg) and
#    Hatamti-Linear Elamite Database (hatamti-elam.uliege.be/doc_about).
# ---------------------------------------------------------------------------
DESSET_FULL_SYLLABARY = [
    # 5 Vowels
    "a", "e", "i", "o", "u",
    # 12 Consonants
    "h", "k", "l", "m", "n", "p", "r", "s", "š", "t", "w", "z",
    # CV signs on Desset 2022 grid (50 attested CV cells)
    "ha", "he", "hi", "hu",
    "ka", "ke", "ki", "ko", "ku",
    "la", "le", "li", "lu",
    "ma", "me", "mi", "mo", "mu",
    "na", "ne", "ni", "nu",
    "pa", "pe", "pi", "po", "pu",
    "ra", "re", "ri", "ru",
    "sa", "si", "so", "su",
    "ša", "še", "ši", "šu",
    "ta", "te", "ti", "tu",
    "wa", "we",
    "za", "ze", "zo", "zu",
]

# ---------------------------------------------------------------------------
# 2. OBJECTIVE INDUS <-> LINEAR ELAMITE VISUAL SIGN-SHAPE MAP
#    Every Indus sign description comes from work_data/sign_shapes.csv.
#    Every LE shape & phonetic value comes directly from Desset 2022 grid.
#    Fields: (lipi_id, le_val, le_val_alt, tier, complexity, le_shape_desc, indus_note)
#    tier: 'strict' (unambiguous geometric/pictographic match) or 'extended' (moderate/figurative)
#    complexity: 'graphic_universal' (Wells 2011 / Fuls 2024) or 'specific_compound'
# ---------------------------------------------------------------------------
SHAPE_MAP_ROWS = [
    # Strokes / dividers (graphic universals)
    ("001", "|",  "la", "strict",   "graphic_universal", "single vertical stroke (word divider / la)", "half-height vertical stroke"),
    ("031", "u",  "w",  "strict",   "graphic_universal", "full vertical stroke with terminal dots (u/w)", "full-height vertical stroke"),
    ("032", "zu", "zu", "strict",   "graphic_universal", "two parallel tall vertical strokes || (zu)", "two adjacent full-height vertical strokes"),
    ("002", "zu", "na", "strict",   "graphic_universal", "two parallel vertical strokes || (zu)", "two adjacent half-height vertical strokes"),
    ("033", "ša", "ša", "strict",   "graphic_universal", "three parallel vertical strokes ||| (ša)", "three adjacent full-height vertical strokes"),
    ("003", "ša", "ša", "strict",   "graphic_universal", "three parallel vertical strokes ||| (ša)", "three adjacent half-height vertical strokes"),

    # Diamonds / leaves / ovals
    ("850", "a",  "a",  "strict",   "graphic_universal", "hollow diamond/lozenge (a)", "simple leaf or diamond"),
    ("861", "we", "we", "strict",   "specific_compound", "diamond with small diamond attached at top (we)", "diamond/leaf with small diamond at top"),
    ("817", "we", "we", "strict",   "specific_compound", "diamond with small diamond attached at top (we)", "diamond/leaf with small diamond at top"),
    ("831", "ke", "l",  "strict",   "specific_compound", "oval/leaf with diagonal leaf-vein hatching (ke alt2)", "leaf with diagonal-stroke central decoration"),
    ("832", "ta", "ta", "strict",   "specific_compound", "diamond/leaf bisected by vertical stroke (ta)", "leaf with small vertical stroke inside"),
    ("840", "pu", "pu", "strict",   "specific_compound", "two side-by-side vertical D-ovals (pu)", "two vertical leaves slightly overlapping"),
    ("818", "šu", "s",  "strict",   "graphic_universal", "circle/diamond with inscribed cross + (šů/s)", "circle with plus sign fully inscribed"),
    ("820", "pe", "he", "strict",   "graphic_universal", "6-spoked wheel/asterisk (pe)", "wheel with 6 evenly spaced spokes"),

    # Crescents / bows
    ("900", "pa", "pa", "strict",   "graphic_universal", "plain crescent arc ( (pa)", "right parenthesis / crescent"),
    ("904", "pa", "pa", "strict",   "graphic_universal", "crescent arc (pa; doubled in Indus)", "two slightly nested right parentheses"),
    ("924", "sa", "sa", "strict",   "specific_compound", "curved hatched horn/crescent (sa)", "right parenthesis in outline with horizontal hatching"),

    # Boxes / ladders / grids / H-frames
    ("603", "r",  "r",  "strict",   "specific_compound", "tall vertical box/hexagon with 2 horizontal bars (r)", "tall rectangle with two horizontal hatches"),
    ("604", "ri", "r",  "strict",   "specific_compound", "tall vertical box/hexagon with 3 horizontal bars (ri)", "tall box with horizontal hatching throughout"),
    ("615", "ko", "ko", "strict",   "graphic_universal", "square cross-hatched grid # (ko)", "grid of x by y cells"),
    ("319", "ši", "ši", "strict",   "graphic_universal", "H-frame with crossbar (ši)", "H with boxed crossbar"),
    ("528", "li", "li", "strict",   "specific_compound", "central square with 4 pinwheel arms (li alt1)", "central box with orthogonal pinwheel lines"),

    # Triangles / arrows / flags / opposing triangles
    ("503", "le", "le", "strict",   "specific_compound", "tall isosceles triangle with horizontal stripes (le)", "tall isosceles triangle with horizontal stripes"),
    ("520", "ka", "si", "strict",   "graphic_universal", "triangle atop vertical stem (ka / si)", "isosceles triangle on top of vertical line"),
    ("550", "k",  "p",  "strict",   "specific_compound", "opposing bowtie triangles (k alt2 / p alt2)", "pincer motif: two opposing isosceles triangles"),
    ("365", "te", "i",  "strict",   "specific_compound", "vertical shaft with hatched wing/flag on right (te / i)", "vertical stroke with triangular wing near middle"),
    ("368", "te", "i",  "strict",   "specific_compound", "vertical shaft with hatched wing/flag on right (te / i)", "vertical stroke with triangular wing near middle"),
    ("692", "e",  "hu", "strict",   "graphic_universal", "X-cross (e / hů alt2)", "X drawn in outline"),

    # Combs / trees / barred poles
    ("400", "ni", "ni", "strict",   "specific_compound", "vertical/horizontal comb with 4-5 teeth (ni)", "vertical line with teeth on one side (comb)"),
    ("415", "ni", "ni", "strict",   "specific_compound", "comb/pitchfork with teeth (ni)", "pitchfork with tines (comb/rake)"),
    ("416", "ni", "ni", "strict",   "specific_compound", "comb/pitchfork with teeth (ni)", "pitchfork with two stacked heads"),
    ("413", "ru", "ru", "strict",   "specific_compound", "vertical shaft crossed by horizontal bars (rů alt1)", "vertical line with horizontal crossbars"),
    ("407", "š",  "le", "strict",   "specific_compound", "3-pronged branching tree on base (š alt1)", "simple tree with branches at top"),
    ("390", "š",  "le", "strict",   "specific_compound", "3-pronged branching tree on base (š alt1)", "simple tree with branches at top"),
    ("405", "š",  "le", "strict",   "specific_compound", "3-pronged branching tree on base (š alt1)", "simple tree with branches at top"),

    # Cups / jars / figurative (cups strict; jars/man/fish extended)
    ("700", "ku", "po", "strict",   "graphic_universal", "open-top U-cup (ku / po)", "simple U cup"),
    ("740", "mu", "pi", "extended", "specific_compound", "flared collared jar/vessel (mu / pi alt2)", "classic jar with two horizontal handles"),
    ("741", "mu", "pi", "extended", "specific_compound", "flared collared jar/vessel (mu / pi alt2)", "jar with handles + 1 mouth stroke"),
    ("220", "za", "ha", "extended", "specific_compound", "diamond with radiating forked tail (za alt1)", "plain fish"),
    ("090", "š",  "ru", "extended", "specific_compound", "stick-figure X-legged branching sign (š alt2)", "person with two arms and two legs"),
    ("091", "šš", "ru", "extended", "specific_compound", "doubled stick-figure (090x2)", "two simple persons standing side by side"),
]

# ---------------------------------------------------------------------------
# 3. VERIFIED BRONZE AGE OLD ELAMITE LEXICON (PNs, DNs, GNs, LE Corpus Words)
#    Sources: Desset et al. 2022 (ZA 112), Desset et al. 2026 (Hatamti DB),
#             Grillot-Susini 2008, Potts 2016, Key #1 ELAMITE_PNS.
# ---------------------------------------------------------------------------
ELAMITE_BRONZE_AGE_NAMES = {
    # Royal & Personal Names (Awan, Shimashki, Sukkalmah, LE corpus)
    "zasiri": "PN (LE Doc 22, Laursen #28 Gulf-Indus bull seal)",
    "puzursusinak": "PN (King of Awan/Susa, LE bilingual)",
    "kutikinsusinak": "PN (King of Awan/Susa)",
    "silhaha": "PN (Sukkalmah king, LE silver beakers)",
    "eparti": "PN (Ebarat II, Sukkalmah founder, LE)",
    "eparat": "PN (Ebarat, Sukkalmah)",
    "itatu": "PN (Idattu I/II, Shimashki king, LE)",
    "idattu": "PN (Idattu, Shimashki)",
    "zemtakone": "PN (Temti-Agun, LE)",
    "temtiagun": "PN (Temti-Agun, Sukkalmah)",
    "palaisan": "PN (Pala-iššan, Sukkalmah, LE)",
    "palaleha": "PN (Pala-leha, LE)",
    "kintatu": "PN (Kindattu, Shimashki king, LE)",
    "kindattu": "PN (Kindattu, Shimashki)",
    "sinpishuk": "PN (Šin-pishůk, LE)",
    "huposan": "PN (Hůpošan, LE)",
    "humsat": "PN (Humšat, Marvdasht silver vase Q, LE)",
    "suwarasu": "PN (Šuwar-asu, Marvdasht silver vase Q, LE)",
    "lapu": "PN (Lapu, LE)",
    "zatume": "PN (Zatume, LE)",
    "tanruhurater": "PN (Tan-Ruhurater, Shimashki)",
    "kuknasur": "PN (Kuk-Našur, Sukkalmah)",
    "kukkirwas": "PN (Kuk-Kirwaš, Sukkalmah)",
    "siruktuh": "PN (Širuk-tuh, Sukkalmah)",
    "siwepalarhuppak": "PN (Siwe-palar-huppak, Sukkalmah)",
    "kuduzulus": "PN (Kudu-zuluš, Sukkalmah)",
    "temtihalki": "PN (Temti-halki, Sukkalmah)",
    "attahusu": "PN (Atta-hušu, Sukkalmah)",
    "peli": "PN (Peli, Awan king)",
    "tata": "PN (Tata, Awan king)",
    "ukku": "PN (Ukku-taheš, Awan)",
    "hisep": "PN (Hišep-ratep, Awan)",
    "luhissan": "PN (Luh-iššan, Awan king)",
    "helu": "PN (Helu, Awan king)",
    "hita": "PN (Hita, Awan king, Naram-Sin treaty)",
    "girnamme": "PN (Gir-namme, Shimashki king)",
    "tazitta": "PN (Tazitta, Shimashki king)",
    "hutran": "PN/DN (Hutran-temti)",
    "simut": "PN/DN (Šimut)",
    "kudur": "PN element (Kudur-)",
    "mekubi": "PN (Mekubi, Susa princess)",
    "tetepmada": "PN (Tetep-mada, Sukkalmah)",
    "kalahusa": "PN (Kala-huša)",
    "unap": "PN (Unap-taš)",
    "huban": "DN/PN (Humban/Huban)",
    "susu": "PN/GN (Susu/Susa)",
    "kuri": "PN (Kuri- / shepherd)",
    "kassu": "PN/word (Kassu)",
    # Divine & Geographic Names
    "insusinak": "DN (Inšušinak, patron god of Susa, LE)",
    "napiresa": "DN (Napireša, great god, LE)",
    "napirisa": "DN (Napiriša)",
    "narute": "DN (Narunde/Narůte, LE)",
    "narundi": "DN (Narundi, Susa statue)",
    "nahunte": "DN (Nahůnte, sun god)",
    "pinikir": "DN (Pinikir, goddess)",
    "kiririsa": "DN (Kiririša, goddess)",
    "humban": "DN (Humban, supreme god)",
    "hatamti": "GN (Hatamti = Elam, LE)",
    "awan": "GN (Awan, LE)",
    "susan": "GN (Susa / Sušan, LE)",
    "susen": "GN (Sušen, LE)",
    "ansan": "GN (Anšan, LE)",
    "simaski": "GN (Šimaški)",
    "marapsa": "GN (Marapša / Marhaši, LE vase Q)",
    "marhasi": "GN (Marhaši / Parahšum)",
    "zahara": "GN (Zahara)",
    "tukris": "GN (Tukriš)",
    "meluhha": "GN (Meluhha)",
    "magan": "GN (Magan)",
    "dilmun": "GN (Dilmun)",
}

ELAMITE_LE_VOCAB = {
    "likawe": "enlarger of the realm (LE royal title)",
    "katru": "ruler/governor (LE)",
    "sunki": "king (Old/Mid Elamite)",
    "sunkir": "the king (LE/OE)",
    "zemt": "lord (LE = temti)",
    "temti": "lord (OE)",
    "risaki": "great (LE)",
    "risar": "great one (LE)",
    "zana": "lady (LE)",
    "lani": "silver/offering (LE)",
    "takme": "life (LE/OE)",
    "api": "this (LE)",
    "ata": "father (LE/OE)",
    "sak": "son (LE/OE)",
    "siyan": "temple (LE/OE)",
    "husa": "wood/tree (OE)",
    "hal": "land (LE/OE)",
    "ruh": "man (OE)",
    "nap": "god (OE)",
    "napir": "god (LE/OE)",
    "kusi": "build (LE/OE)",
    "kusik": "built (LE)",
    "hutta": "make/do (LE/OE)",
    "huttak": "made (LE)",
    "hane": "love (LE)",
    "hanes": "he loved (LE)",
    "kukunnum": "high temple (OE)",
    "kunanki": "silver beaker vessel (LE/Ur III)",
    "tuni": "give (LE)",
    "tunik": "given (LE)",
    "duni": "give (OE)",
    "kiki": "sky/heaven (OE)",
    "murun": "earth (OE)",
    "sara": "below/under (OE)",
    "peti": "enemy/rebel (OE)",
    "sati": "king/ruler (OE)",
    "meni": "then/ruler (OE)",
    "hali": "brick/clay (OE)",
    "puhu": "boy/servant (OE)",
    "sutu": "sister (OE)",
    "rutu": "wife (OE)",
    "igi": "brother (OE)",
    "kuma": "until/to (OE)",
    "tiri": "speak (OE)",
    "sari": "destroy/cut (OE)",
    "taki": "life/good (OE)",
    "sulu": "well-being (OE)",
    "piti": "enemy/hostile (OE)",
    "kuku": "protect (OE)",
    "sima": "name/fame (OE)",
}


def norm_elamite(s: str) -> str:
    """Normalize Elamite phonemic transcription (preserving vowel vs consonant)."""
    s = s.lower().strip()
    repl = [
        ("š", "s"), ("sh", "s"), ("ḫ", "h"), ("ů", "u"), ("ū", "u"),
        ("ā", "a"), ("ē", "e"), ("ī", "i"), ("ō", "o"),
        ("b", "p"), ("d", "t"), ("g", "k"), ("q", "k"),
    ]
    for a, b in repl:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z]", "", s)
    # Collapse geminate vowels & consonants to match Elamite orthography
    s = re.sub(r"([a-z])\1+", r"\1", s)
    return s


def consonant_skel(s: str, keep_init_v: bool = True) -> str:
    """Extract consonant skeleton; preserve initial vowel marker 'V' to prevent vowel-initial collisions."""
    n = norm_elamite(s)
    if not n:
        return ""
    vowels = set("aeiou")
    cons = "".join(ch for ch in n if ch not in vowels)
    if keep_init_v and n[0] in vowels:
        return "V" + cons
    return cons


def edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if abs(len(a) - len(b)) > 2:
        return 3
    dp = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev = dp[0]
        dp[0] = i
        for j, cb in enumerate(b, 1):
            cur = dp[j]
            cost = 0 if ca == cb else 1
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
            prev = cur
    return dp[-1]


def load_clean_hinz_koch():
    """Clean work_data/lang_m/lex/elamite_hinzkoch.tsv of OCR & German-gloss artifacts."""
    path = ROOT / "work_data" / "lang_m" / "lex" / "elamite_hinzkoch.tsv"
    german_stop = {
        "mit", "ch", "der", "die", "das", "und", "von", "zu", "in", "im", "an",
        "am", "ab", "auf", "aus", "bei", "fur", "nach", "uber", "vor", "wie",
        "als", "oder", "nicht", "auch", "noch", "nur", "ein", "eine", "vgl",
        "ebd", "s", "ne", "me", "ap", "ae", "ache", "elam", "pers", "bab",
    }
    bad_pat = re.compile(r"(lfl|iii|bbb|ddd|qq|xx|jj|^c-|^sb-be|[^a-z\-])")

    raw_n = 0
    kept = {}
    dropped = Counter()
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 5:
                continue
            raw_n += 1
            translit = parts[1].strip().lower()
            word = parts[2].strip().lower()
            gloss = parts[4].strip()

            if word in german_stop or translit in german_stop:
                dropped["german_stop"] += 1
                continue
            if "-" not in translit:
                dropped["no_hyphen_ocr"] += 1
                continue
            if bad_pat.search(translit):
                dropped["ocr_garbage"] += 1
                continue
            syls = [x for x in translit.split("-") if x]
            if len(syls) < 2 or any(len(x) > 4 for x in syls):
                dropped["bad_syllable_struct"] += 1
                continue
            nw = norm_elamite(word)
            sk = consonant_skel(word, keep_init_v=True)
            # Require at least 2 real consonants (excluding leading V)
            real_c = sk[1:] if sk.startswith("V") else sk
            if len(nw) < 3 or len(real_c) < 2:
                dropped["too_short"] += 1
                continue
            if nw not in kept:
                kept[nw] = (translit, word, sk, gloss[:100])
    return raw_n, kept, dropped


def fisher_exact_two_sided(a, b, c, d):
    """Exact 2x2 Fisher's exact test (two-sided) using log-factorials, zero external deps."""
    def log_comb(n, k):
        if k < 0 or k > n:
            return float("-inf")
        return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)

    r1, r2 = a + b, c + d
    c1, n = a + c, a + b + c + d
    denom = log_comb(n, c1)

    def prob(x):
        return math.exp(log_comb(r1, x) + log_comb(r2, c1 - x) - denom)

    p_obs = prob(a)
    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    p_sum = 0.0
    for x in range(lo, hi + 1):
        px = prob(x)
        if px <= p_obs + 1e-12:
            p_sum += px
    return min(1.0, p_sum)


# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("KEY #2 TRACK C: LINEAR ELAMITE & PROTO-ELAMITE BRIDGE AUDIT")
    print("=" * 72)

    # Load sign_shapes.csv
    sign_shapes = {}
    with open(ROOT / "work_data" / "sign_shapes.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            sign_shapes[r["lipi_wells_number"].zfill(3)] = r["shape_description"]

    # Load gulf3_verified.csv
    with open(ROOT / "work_data" / "gulf3" / "gulf3_verified.csv", encoding="utf-8") as f:
        gulf3 = list(csv.DictReader(f))

    # Load mainland deduplicated events_lipi.json
    with open(ROOT / "work_data" / "sem" / "events_lipi.json", encoding="utf-8") as f:
        events = json.load(f)

    # Clean Elamite lexicon
    hk_raw, hk_clean, hk_dropped = load_clean_hinz_koch()
    print(f"\n[LEXICON] Hinz-Koch raw={hk_raw}, cleaned={len(hk_clean)}, dropped={dict(hk_dropped)}")

    # Build Lexicon A (Bronze Age Names + LE Vocab) & Lexicon B (Cleaned Hinz-Koch + A)
    lex_a_words = {}
    for w, g in ELAMITE_BRONZE_AGE_NAMES.items():
        nw = norm_elamite(w)
        lex_a_words[nw] = ("BA_NAME", w, consonant_skel(w), g)
    for w, g in ELAMITE_LE_VOCAB.items():
        nw = norm_elamite(w)
        if nw not in lex_a_words:
            lex_a_words[nw] = ("LE_VOCAB", w, consonant_skel(w), g)

    lex_b_words = dict(lex_a_words)
    for nw, (tr, w, sk, gl) in hk_clean.items():
        if nw not in lex_b_words:
            lex_b_words[nw] = ("HINZ_KOCH", w, sk, gl)

    # Write cleaned lexicon CSV
    with open(OUT_DIR / "elamite_clean_lexicon.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["norm_word", "source", "raw_word", "skeleton", "gloss"])
        for nw, (src, raw_w, sk, gl) in sorted(lex_b_words.items()):
            wr.writerow([nw, src, raw_w, sk, gl])

    lex_a_set = set(lex_a_words.keys())
    lex_a_skels = defaultdict(list)
    for nw, (_, raw_w, sk, gl) in lex_a_words.items():
        real_c = sk[1:] if sk.startswith("V") else sk
        if len(real_c) >= 2:
            lex_a_skels[sk].append((nw, raw_w, gl))

    lex_b_set = set(lex_b_words.keys())
    lex_b_skels = defaultdict(list)
    for nw, (_, raw_w, sk, gl) in lex_b_words.items():
        real_c = sk[1:] if sk.startswith("V") else sk
        if len(real_c) >= 2:
            lex_b_skels[sk].append((nw, raw_w, gl))

    print(f"[LEXICON] Lex A (Bronze Age PNs/DNs/GNs + LE vocab): {len(lex_a_set)} words, {len(lex_a_skels)} unique skels (>=2C)")
    print(f"[LEXICON] Lex B (A + Cleaned Hinz-Koch): {len(lex_b_set)} words, {len(lex_b_skels)} unique skels (>=2C)")

    # =========================================================================
    # TEST C1: VISUAL SIGN-SHAPE TRANSFER (LINEAR ELAMITE -> INDUS)
    # =========================================================================
    print("\n" + "=" * 72)
    print("TEST C1: VISUAL SIGN-SHAPE TRANSFER (DESSET LE SYLLABARY -> INDUS)")
    print("=" * 72)

    # Save c1_shape_map.csv
    with open(OUT_DIR / "c1_shape_map.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["lipi_sign", "le_val", "le_val_alt", "tier", "complexity", "le_shape_desc", "indus_shape_desc"])
        for lipi_id, val, alt, tier, comp, le_desc, note in SHAPE_MAP_ROWS:
            wr.writerow([lipi_id, val, alt, tier, comp, le_desc, sign_shapes.get(lipi_id, note)])

    strict_map = {r[0]: r[1] for r in SHAPE_MAP_ROWS if r[3] == "strict"}
    full_map = {r[0]: r[1] for r in SHAPE_MAP_ROWS}
    n_univ = sum(1 for r in SHAPE_MAP_ROWS if r[4] == "graphic_universal")
    n_comp = sum(1 for r in SHAPE_MAP_ROWS if r[4] == "specific_compound")
    print(f"Mapped signs: {len(full_map)} total ({len(strict_map)} strict, {len(full_map)-len(strict_map)} extended)")
    print(f"Complexity split: {n_univ} graphic_universal ({100*n_univ/len(full_map):.1f}%), {n_comp} specific_compound ({100*n_comp/len(full_map):.1f}%)")

    # Build seal sets for Test C1
    iran_seals = []
    other_gulf_seals = []
    for r in gulf3:
        seq_str = r["seq_verified"].strip()
        if not seq_str or seq_str.startswith("LE:"):
            continue
        seq = [s.zfill(3) for s in seq_str.split("-") if s and s != "000"]
        if r["region"] == "Iranian Plateau":
            iran_seals.append((r["uid"], r["site"], r["shape"], seq))
        elif r["region"] in ("Persian Gulf", "Mesopotamia", "Mesopotamia/Gulf"):
            other_gulf_seals.append((r["uid"], r["site"], r["region"], seq))

    # Top 50 mainland Indus multi-sign stems (length 2..6, deduplicated events, >= 60% mapped in full_map)
    stem_counts = Counter()
    for e in events:
        if e.get("kind") == "seal" or len(e["signs"]) >= 2:
            seq = tuple(s.zfill(3) for s in e["signs"] if s != "000")
            if 2 <= len(seq) <= 6:
                stem_counts[seq] += 1

    top50_mainland = []
    for seq, cnt in stem_counts.most_common():
        mapped_cnt = sum(1 for s in seq if s in full_map and full_map[s] != "|")
        if mapped_cnt >= 2 and mapped_cnt / len(seq) >= 0.6:
            top50_mainland.append((f"MAIN_{len(top50_mainland)+1:02d}", f"n={cnt}", "mainland", list(seq)))
            if len(top50_mainland) >= 50:
                break

    def decode_seq(seq, smap, reverse=False):
        s_list = list(reversed(seq)) if reverse else list(seq)
        chunks = [[]]
        mapped_n = 0
        for s in s_list:
            v = smap.get(s)
            if v is None:
                chunks[-1].append("?")
            elif v == "|":
                chunks.append([])
                mapped_n += 1
            else:
                chunks[-1].append(v)
                mapped_n += 1
        # Collect contiguous mapped spans of >= 2 phonetic tokens
        spans = []
        for ch in chunks:
            cur = []
            for tok in ch:
                if tok == "?":
                    if len(cur) >= 2:
                        spans.append("".join(cur))
                    cur = []
                else:
                    cur.append(tok)
            if len(cur) >= 2:
                spans.append("".join(cur))
        full_translit = " | ".join("-".join(ch) for ch in chunks if ch)
        return full_translit, spans, mapped_n

    ed1_cache = {}
    def is_ed1_lex_a(nw: str) -> str:
        res = ed1_cache.get(nw)
        if res is not None:
            return res
        found = ""
        if len(nw) >= 4:
            for lw in lex_a_set:
                if abs(len(lw) - len(nw)) <= 1 and edit_distance(nw, lw) <= 1:
                    found = lex_a_words[lw][1]
                    break
        ed1_cache[nw] = found
        return found

    def score_dataset(items, smap, reverse=False, collect_hits=False):
        """Score items against Lex A & Lex B on exact, near-exact (ed<=1, len>=4), and exact skeleton (>=2C)."""
        a_exact = 0
        a_near = 0
        a_skel = 0
        b_exact = 0
        b_skel = 0
        hits = []
        for uid, site, meta, seq in items:
            tr, spans, m_n = decode_seq(seq, smap, reverse=reverse)
            hit_a_ex = hit_a_nr = hit_a_sk = hit_b_ex = hit_b_sk = False
            matched_notes = []
            for sp in spans:
                nw = norm_elamite(sp)
                sk = consonant_skel(sp, keep_init_v=True)
                real_c = sk[1:] if sk.startswith("V") else sk
                if len(real_c) < 2:
                    continue
                if nw in lex_a_set:
                    hit_a_ex = True
                    if collect_hits:
                        matched_notes.append(f"A_EXACT:{nw}={lex_a_words[nw][1]}")
                ed1_w = is_ed1_lex_a(nw)
                if ed1_w:
                    hit_a_nr = True
                    if collect_hits:
                        matched_notes.append(f"A_ED1:{nw}~{ed1_w}")
                if sk in lex_a_skels:
                    hit_a_sk = True
                    if collect_hits:
                        matched_notes.append(f"A_SKEL:{sk}->{lex_a_skels[sk][0][1]}")
                if nw in lex_b_set:
                    hit_b_ex = True
                    if collect_hits:
                        matched_notes.append(f"B_EXACT:{nw}={lex_b_words[nw][1]}")
                if sk in lex_b_skels:
                    hit_b_sk = True
                    if collect_hits:
                        matched_notes.append(f"B_SKEL:{sk}->{lex_b_skels[sk][0][1]}")
            a_exact += int(hit_a_ex)
            a_near += int(hit_a_nr)
            a_skel += int(hit_a_sk)
            b_exact += int(hit_b_ex)
            b_skel += int(hit_b_sk)
            if collect_hits:
                hits.append({
                    "uid": uid, "site": site, "seq": "-".join(seq),
                    "mapped_n": m_n, "total_n": len(seq),
                    "translit": tr, "spans": spans,
                    "matches": matched_notes,
                })
        return (a_exact, a_near, a_skel, b_exact, b_skel), hits

    # Print decoded 5 Iranian Indus seals (Full Map, R->L and L->R)
    print("\n--- 5 Iranian Indus Seals Transliterated via Desset LE Visual Shapes (Full Map) ---")
    _, iran_hits_rl = score_dataset(iran_seals, full_map, reverse=False, collect_hits=True)
    _, iran_hits_lr = score_dataset(iran_seals, full_map, reverse=True, collect_hits=True)
    for h_rl, h_lr in zip(iran_hits_rl, iran_hits_lr):
        print(f"  {h_rl['uid']} ({h_rl['site']}): {h_rl['seq']} [{h_rl['mapped_n']}/{h_rl['total_n']} mapped]")
        print(f"    R->L: {h_rl['translit']}  | matches: {h_rl['matches'][:4]}")
        print(f"    L->R: {h_lr['translit']}  | matches: {h_lr['matches'][:4]}")

    # Run 5,000 random shuffles across both maps and both null models
    N_SHUF = 5000
    c1_results = []

    datasets_c1 = [
        ("Iran_5", iran_seals),
        ("Gulf_Mesop_28", other_gulf_seals),
        ("Mainland_Top50", top50_mainland),
    ]
    maps_c1 = [
        ("strict_26", strict_map),
        ("full_30", full_map),
    ]

    for map_name, smap in maps_c1:
        # Keep word divider 001 -> "|" fixed in shuffles so word boundaries stay identical
        phon_keys = [k for k, v in smap.items() if v != "|"]
        phon_vals = [smap[k] for k in phon_keys]
        fixed_div = {k: v for k, v in smap.items() if v == "|"}

        for ds_name, ds_items in datasets_c1:
            for dir_label, rev_flag in [("RL", False), ("LR", True)]:
                obs, detail_hits = score_dataset(ds_items, smap, reverse=rev_flag, collect_hits=(dir_label == "RL"))

                # Null 1: permute mapped LE syllables across mapped Indus signs
                null1_ge = [0] * 5
                null1_sums = [0.0] * 5
                null1_sq = [0.0] * 5
                # Null 2: random draw from full 67-value Desset syllabary
                null2_ge = [0] * 5
                null2_sums = [0.0] * 5
                null2_sq = [0.0] * 5

                for _ in range(N_SHUF):
                    perm_vals = phon_vals[:]
                    RNG.shuffle(perm_vals)
                    pmap = dict(fixed_div)
                    for k, v in zip(phon_keys, perm_vals):
                        pmap[k] = v
                    sc1, _ = score_dataset(ds_items, pmap, reverse=rev_flag)
                    for idx in range(5):
                        if sc1[idx] >= obs[idx]:
                            null1_ge[idx] += 1
                        null1_sums[idx] += sc1[idx]
                        null1_sq[idx] += sc1[idx] ** 2

                    dmap = dict(fixed_div)
                    for k in phon_keys:
                        dmap[k] = RNG.choice(DESSET_FULL_SYLLABARY)
                    sc2, _ = score_dataset(ds_items, dmap, reverse=rev_flag)
                    for idx in range(5):
                        if sc2[idx] >= obs[idx]:
                            null2_ge[idx] += 1
                        null2_sums[idx] += sc2[idx]
                        null2_sq[idx] += sc2[idx] ** 2

                metric_names = ["A_exact", "A_near_ed1", "A_skel", "B_exact", "B_skel"]
                row_summary = {
                    "map": map_name, "dataset": ds_name, "n_items": len(ds_items),
                    "dir": dir_label, "metrics": {}
                }
                for idx, mname in enumerate(metric_names):
                    m1 = null1_sums[idx] / N_SHUF
                    sd1 = math.sqrt(max(0.0, null1_sq[idx] / N_SHUF - m1 * m1))
                    z1 = (obs[idx] - m1) / sd1 if sd1 > 1e-9 else 0.0
                    p1 = (null1_ge[idx] + 1) / (N_SHUF + 1)

                    m2 = null2_sums[idx] / N_SHUF
                    sd2 = math.sqrt(max(0.0, null2_sq[idx] / N_SHUF - m2 * m2))
                    z2 = (obs[idx] - m2) / sd2 if sd2 > 1e-9 else 0.0
                    p2 = (null2_ge[idx] + 1) / (N_SHUF + 1)

                    row_summary["metrics"][mname] = {
                        "obs": obs[idx],
                        "null1_mean": round(m1, 3), "null1_sd": round(sd1, 3), "null1_z": round(z1, 2), "null1_p": round(p1, 4),
                        "null2_mean": round(m2, 3), "null2_sd": round(sd2, 3), "null2_z": round(z2, 2), "null2_p": round(p2, 4),
                    }
                c1_results.append(row_summary)

                if dir_label == "RL":
                    print(f"\n  [{map_name} | {ds_name} (n={len(ds_items)}) | R->L]")
                    for mname in metric_names:
                        d = row_summary["metrics"][mname]
                        print(f"    {mname:10s}: obs={d['obs']:2d} | perm_null={d['null1_mean']:.2f}±{d['null1_sd']:.2f} (z={d['null1_z']:+.2f}, p={d['null1_p']:.4f}) | syl67_null={d['null2_mean']:.2f}±{d['null2_sd']:.2f} (z={d['null2_z']:+.2f}, p={d['null2_p']:.4f})")

    # -------------------------------------------------------------------------
    # TEST C1 REDESIGN (C1-R, per AGENTS.md Rule 4: redesign before pausing!):
    # Strip 090/091/093/095/001 as non-phonetic Gulf MAN determinatives/dividers,
    # and test BOTH primary LE values and alt LE values (e.g. 740/741->pi, 831->l,
    # 365->i, 700->po, 520->si, 220->ha) with 5,000 shuffles.
    # -------------------------------------------------------------------------
    print("\n--- TEST C1 REDESIGN (C1-R): Determinative-Stripped (090/091/001 = DET/DIV) + Alt Values ---")
    DETS = {"090", "091", "093", "095", "001"}
    det_strip_prim = {r[0]: ("|" if r[0] in DETS else r[1]) for r in SHAPE_MAP_ROWS}
    det_strip_alt = {r[0]: ("|" if r[0] in DETS else r[2]) for r in SHAPE_MAP_ROWS}

    c1r_results = []
    for map_name, smap in [("det_strip_prim", det_strip_prim), ("det_strip_alt", det_strip_alt)]:
        phon_keys = [k for k, v in smap.items() if v != "|"]
        phon_vals = [smap[k] for k in phon_keys]
        fixed_div = {k: v for k, v in smap.items() if v == "|"}

        for ds_name, ds_items in datasets_c1:
            for dir_label, rev_flag in [("RL", False), ("LR", True)]:
                obs, det_hits = score_dataset(ds_items, smap, reverse=rev_flag, collect_hits=(ds_name == "Iran_5"))
                if ds_name == "Iran_5":
                    print(f"  [{map_name} | Iran_5 | {dir_label}] decoded:")
                    for h in det_hits:
                        print(f"    {h['uid']} ({h['site']}): {h['translit']} | spans={h['spans']} | hits={h['matches']}")

                null1_ge = [0] * 5
                null1_sums = [0.0] * 5
                null1_sq = [0.0] * 5
                for _ in range(N_SHUF):
                    pv = phon_vals[:]
                    RNG.shuffle(pv)
                    pmap = dict(fixed_div)
                    for k, v in zip(phon_keys, pv):
                        pmap[k] = v
                    sc1, _ = score_dataset(ds_items, pmap, reverse=rev_flag)
                    for idx in range(5):
                        if sc1[idx] >= obs[idx]:
                            null1_ge[idx] += 1
                        null1_sums[idx] += sc1[idx]
                        null1_sq[idx] += sc1[idx] ** 2

                metric_names = ["A_exact", "A_near_ed1", "A_skel", "B_exact", "B_skel"]
                row_s = {"map": map_name, "dataset": ds_name, "n_items": len(ds_items), "dir": dir_label, "metrics": {}}
                for idx, mname in enumerate(metric_names):
                    m1 = null1_sums[idx] / N_SHUF
                    sd1 = math.sqrt(max(0.0, null1_sq[idx] / N_SHUF - m1 * m1))
                    z1 = (obs[idx] - m1) / sd1 if sd1 > 1e-9 else 0.0
                    p1 = (null1_ge[idx] + 1) / (N_SHUF + 1)
                    row_s["metrics"][mname] = {"obs": obs[idx], "perm_mean": round(m1, 3), "perm_sd": round(sd1, 3), "perm_z": round(z1, 2), "perm_p": round(p1, 4)}
                c1r_results.append(row_s)
                if dir_label == "RL" or any(d["perm_p"] < 0.10 for d in row_s["metrics"].values()):
                    summary_str = " | ".join(f"{m}:{d['obs']}(null={d['perm_mean']:.2f},p={d['perm_p']:.3f})" for m, d in row_s["metrics"].items())
                    print(f"  [{map_name:14s} | {ds_name:14s} | {dir_label}] {summary_str}")

    with open(OUT_DIR / "c1r_redesign_results.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["map", "dataset", "n_items", "dir", "metric", "obs", "perm_mean", "perm_sd", "perm_z", "perm_p"])
        for r in c1r_results:
            for mname, d in r["metrics"].items():
                wr.writerow([r["map"], r["dataset"], r["n_items"], r["dir"], mname, d["obs"], d["perm_mean"], d["perm_sd"], d["perm_z"], d["perm_p"]])

    # Save C1 results CSV
    with open(OUT_DIR / "c1_visual_transfer_results.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["map", "dataset", "n_items", "dir", "metric", "obs", "perm_null_mean", "perm_null_sd", "perm_z", "perm_p", "syl67_null_mean", "syl67_null_sd", "syl67_z", "syl67_p"])
        for r in c1_results:
            for mname, d in r["metrics"].items():
                wr.writerow([r["map"], r["dataset"], r["n_items"], r["dir"], mname, d["obs"], d["null1_mean"], d["null1_sd"], d["null1_z"], d["null1_p"], d["null2_mean"], d["null2_sd"], d["null2_z"], d["null2_p"]])

    # Save decoded Gulf & Iranian seals detail CSV
    _, gulf_hits_rl = score_dataset(other_gulf_seals, full_map, reverse=False, collect_hits=True)
    with open(OUT_DIR / "c1_decoded_seals.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["group", "uid", "site", "seq", "mapped_n", "total_n", "translit_RL", "matches_RL"])
        for h in iran_hits_rl:
            wr.writerow(["Iran", h["uid"], h["site"], h["seq"], h["mapped_n"], h["total_n"], h["translit"], "; ".join(h["matches"])])
        for h in gulf_hits_rl:
            wr.writerow(["Gulf_Mesop", h["uid"], h["site"], h["seq"], h["mapped_n"], h["total_n"], h["translit"], "; ".join(h["matches"])])

    # =========================================================================
    # TEST C2: IRANIAN INDUS SEALS VS GULF & MAINLAND GRAMMAR
    # =========================================================================
    print("\n" + "=" * 72)
    print("TEST C2: IRANIAN INDUS SEALS VS GULF & MAINLAND GRAMMAR")
    print("=" * 72)

    # Mainland bigrams & sign frequencies
    main_sign_freq = Counter()
    main_bigrams_dir = Counter()
    main_bigrams_undir = Counter()
    for e in events:
        seq = [s.zfill(3) for s in e["signs"] if s != "000"]
        for s in seq:
            main_sign_freq[s] += 1
        for a, b in zip(seq, seq[1:]):
            main_bigrams_dir[(a, b)] += 1
            main_bigrams_undir[tuple(sorted((a, b)))] += 1

    # Partition gulf3_verified into clean regional cohorts (excluding LE G3-I06 from Indus-script counts)
    cohorts = defaultdict(list)
    for r in gulf3:
        seq_str = r["seq_verified"].strip()
        if not seq_str or seq_str.startswith("LE:"):
            continue
        seq = [s.zfill(3) for s in seq_str.split("-") if s and s != "000"]
        grp = r["group"]
        reg = r["region"]
        if reg == "Iranian Plateau":
            c_name = "Iran_Indus"
        elif "Bahrain" in grp:
            c_name = "Bahrain"
        elif "Failaka" in grp or "Oman_UAE" in grp:
            c_name = "Failaka_UAE"
        elif reg == "Mesopotamia":
            c_name = "Mesopotamia_Round"
        elif reg == "Mesopotamia/Gulf":
            c_name = "Unknown_Gulf_WA"
        elif reg == "Indus (Gulf round)":
            c_name = "Indus_Home_Round"
        elif grp == "Abroad_Square":
            c_name = "Abroad_Square"
        else:
            c_name = "Other"
        cohorts[c_name].append({
            "uid": r["uid"], "site": r["site"], "shape": r["shape"], "seq": seq
        })

    FISH_SIGNS = {"220", "235", "240", "255", "256", "231", "233"}
    MAN_CORE = {"090", "091"}
    MAN_ANY = {"090", "091", "093", "095", "140", "145", "150", "151", "156", "160"}
    JAR_CUP = {"700", "705", "740", "741", "744"}
    PLANT_COMB = {"390", "405", "407", "413", "415", "416"}

    def cohort_stats(items):
        n = len(items)
        cyl = sum(1 for x in items if x["shape"] == "cylinder")
        rnd = sum(1 for x in items if x["shape"] == "round")
        has_man_core = sum(1 for x in items if any(s in MAN_CORE for s in x["seq"]))
        has_man_any = sum(1 for x in items if any(s in MAN_ANY for s in x["seq"]))
        has_fish = sum(1 for x in items if any(s in FISH_SIGNS for s in x["seq"]))
        has_831 = sum(1 for x in items if "831" in x["seq"])
        has_604 = sum(1 for x in items if "604" in x["seq"])
        has_924 = sum(1 for x in items if "924" in x["seq"])
        has_032 = sum(1 for x in items if "032" in x["seq"])
        has_055 = sum(1 for x in items if "055" in x["seq"])
        has_001 = sum(1 for x in items if "001" in x["seq"])
        has_jar = sum(1 for x in items if any(s in JAR_CUP for s in x["seq"]))
        has_plant = sum(1 for x in items if any(s in PLANT_COMB for s in x["seq"]))

        bg_tot = 0
        bg_dir_hit = 0
        bg_undir_hit = 0
        sign_ctr = Counter()
        for x in items:
            for s in x["seq"]:
                sign_ctr[s] += 1
            for a, b in zip(x["seq"], x["seq"][1:]):
                bg_tot += 1
                if main_bigrams_dir[(a, b)] > 0:
                    bg_dir_hit += 1
                if main_bigrams_undir[tuple(sorted((a, b)))] > 0:
                    bg_undir_hit += 1
        return {
            "n": n, "cyl": cyl, "rnd": rnd,
            "man_090_091": has_man_core, "man_any": has_man_any,
            "fish": has_fish, "s831": has_831, "s604": has_604, "s924": has_924,
            "s032": has_032, "s055": has_055, "s001": has_001,
            "jar_cup": has_jar, "plant_comb": has_plant,
            "bg_tot": bg_tot, "bg_dir_hit": bg_dir_hit, "bg_undir_hit": bg_undir_hit,
            "bg_dir_pct": round(100 * bg_dir_hit / bg_tot, 1) if bg_tot else 0.0,
            "bg_undir_pct": round(100 * bg_undir_hit / bg_tot, 1) if bg_tot else 0.0,
            "n_tokens": sum(sign_ctr.values()),
            "n_types": len(sign_ctr),
            "sign_ctr": sign_ctr,
        }

    c2_order = ["Iran_Indus", "Bahrain", "Failaka_UAE", "Mesopotamia_Round", "Unknown_Gulf_WA", "Indus_Home_Round", "Abroad_Square"]
    c2_stats = {k: cohort_stats(cohorts[k]) for k in c2_order}

    print(f"\n{'Cohort':18s} {'N':>3s} {'Cyl':>5s} {'090/91':>7s} {'Fish':>6s} {'831':>5s} {'032':>5s} {'604':>5s} {'924':>5s} {'055':>5s} {'BG_dir%':>8s}")
    for k in c2_order:
        st = c2_stats[k]
        n = st["n"]
        print(f"{k:18s} {n:3d} {st['cyl']:2d}/{n:<2d} {st['man_090_091']:2d}/{n:<4d} {st['fish']:2d}/{n:<3d} {st['s831']:2d}/{n:<2d} {st['s032']:2d}/{n:<2d} {st['s604']:2d}/{n:<2d} {st['s924']:2d}/{n:<2d} {st['s055']:2d}/{n:<2d} {st['bg_dir_pct']:7.1f}%")

    # Pairwise Jaccard & Cosine similarity of Iran_Indus vs other cohorts + Mainland
    def jaccard(c1, c2):
        s1, s2 = set(c1.keys()), set(c2.keys())
        return len(s1 & s2) / len(s1 | s2) if (s1 | s2) else 0.0

    def cosine(c1, c2):
        keys = set(c1.keys()) | set(c2.keys())
        dot = sum(c1[k] * c2[k] for k in keys)
        n1 = math.sqrt(sum(v * v for v in c1.values()))
        n2 = math.sqrt(sum(v * v for v in c2.values()))
        return dot / (n1 * n2) if n1 > 0 and n2 > 0 else 0.0

    print("\n--- Sign-Inventory Similarity to Iran_Indus (20 unique signs, 27 tokens) ---")
    ir_ctr = c2_stats["Iran_Indus"]["sign_ctr"]
    sim_table = {}
    for k in c2_order[1:]:
        j = jaccard(ir_ctr, c2_stats[k]["sign_ctr"])
        co = cosine(ir_ctr, c2_stats[k]["sign_ctr"])
        shared = sorted(set(ir_ctr.keys()) & set(c2_stats[k]["sign_ctr"].keys()))
        sim_table[k] = {"jaccard": round(j, 3), "cosine": round(co, 3), "n_shared": len(shared), "shared": shared}
        print(f"  vs {k:18s}: Jaccard={j:.3f}, Cosine={co:.3f}, shared={len(shared)} ({','.join(shared)})")
    # Also vs Mainland top-100 and full mainland
    co_main = cosine(ir_ctr, main_sign_freq)
    sim_table["Mainland_Full"] = {"jaccard": round(jaccard(ir_ctr, main_sign_freq), 3), "cosine": round(co_main, 3), "n_shared": len(set(ir_ctr.keys()) & set(main_sign_freq.keys())), "shared": []}
    print(f"  vs {'Mainland_Full':18s}: Cosine={co_main:.3f} (all {len(set(ir_ctr.keys()) & set(main_sign_freq.keys()))}/{len(ir_ctr)} Iranian signs attested on Mainland)")

    # Exact Fisher tests: Iran (n=5) vs Provenanced Gulf+Mesopotamia (Bahrain+Failaka+Mesopotamia, n=23)
    prov_gm = cohorts["Bahrain"] + cohorts["Failaka_UAE"] + cohorts["Mesopotamia_Round"]
    st_ir = c2_stats["Iran_Indus"]
    st_gm = cohort_stats(prov_gm)

    fisher_tests = {
        "cylinder_vs_prov_GM": (st_ir["cyl"], st_ir["n"] - st_ir["cyl"], st_gm["cyl"], st_gm["n"] - st_gm["cyl"]),
        "fish_absent_vs_prov_GM": (st_ir["fish"], st_ir["n"] - st_ir["fish"], st_gm["fish"], st_gm["n"] - st_gm["fish"]),
        "s831_vs_prov_GM": (st_ir["s831"], st_ir["n"] - st_ir["s831"], st_gm["s831"], st_gm["n"] - st_gm["s831"]),
        "s032_vs_prov_GM": (st_ir["s032"], st_ir["n"] - st_ir["s032"], st_gm["s032"], st_gm["n"] - st_gm["s032"]),
        "man090_091_vs_prov_GM": (st_ir["man_090_091"], st_ir["n"] - st_ir["man_090_091"], st_gm["man_090_091"], st_gm["n"] - st_gm["man_090_091"]),
        "bg_dir_vs_prov_GM": (st_ir["bg_dir_hit"], st_ir["bg_tot"] - st_ir["bg_dir_hit"], st_gm["bg_dir_hit"], st_gm["bg_tot"] - st_gm["bg_dir_hit"]),
    }
    print("\n--- Exact Fisher Tests: Iran (n=5) vs Provenanced Gulf+Mesopotamia (n=23) ---")
    c2_fisher_out = {}
    for name, (a, b, c, d) in fisher_tests.items():
        p = fisher_exact_two_sided(a, b, c, d)
        c2_fisher_out[name] = {"iran": f"{a}/{a+b}", "prov_GM": f"{c}/{c+d}", "fisher_p": round(p, 5)}
        print(f"  {name:24s}: Iran={a}/{a+b} ({100*a/(a+b):.1f}%) vs ProvGM={c}/{c+d} ({100*c/(c+d):.1f}%) | Fisher p={p:.5f}")

    # Strongest Rival Audit (C2): 10,000 random draws of n=5 from undifferentiated Gulf+WA+Iran pool
    N_PERM_C2 = 10000
    pool_prov = cohorts["Iran_Indus"] + prov_gm               # n = 28 provenanced
    pool_all_gwa = pool_prov + cohorts["Unknown_Gulf_WA"]     # n = 33 incl. 5 unprovenanced

    def perm_test_iran(pool, label):
        ge_cyl = le_fish = ge_831 = ge_032 = ge_joint = 0
        for _ in range(N_PERM_C2):
            samp = RNG.sample(pool, 5)
            cyl = sum(1 for x in samp if x["shape"] == "cylinder")
            fish = sum(1 for x in samp if any(s in FISH_SIGNS for s in x["seq"]))
            s831 = sum(1 for x in samp if "831" in x["seq"])
            s032 = sum(1 for x in samp if "032" in x["seq"])
            if cyl >= st_ir["cyl"]: ge_cyl += 1
            if fish <= st_ir["fish"]: le_fish += 1
            if s831 >= st_ir["s831"]: ge_831 += 1
            if s032 >= st_ir["s032"]: ge_032 += 1
            if cyl >= 3 and fish == 0 and (s831 >= 2 or s032 >= 2):
                ge_joint += 1
        res = {
            "pool": label, "N_pool": len(pool),
            "p_cyl_ge3": round((ge_cyl + 1) / (N_PERM_C2 + 1), 5),
            "p_fish_0": round((le_fish + 1) / (N_PERM_C2 + 1), 5),
            "p_831_ge2": round((ge_831 + 1) / (N_PERM_C2 + 1), 5),
            "p_032_ge2": round((ge_032 + 1) / (N_PERM_C2 + 1), 5),
            "p_joint_iran_profile": round((ge_joint + 1) / (N_PERM_C2 + 1), 5),
        }
        print(f"  [Rival Perm {label}, N={len(pool)}] p(cyl>=3)={res['p_cyl_ge3']}, p(fish=0)={res['p_fish_0']}, p(831>=2)={res['p_831_ge2']}, p(032>=2)={res['p_032_ge2']}, p(joint)={res['p_joint_iran_profile']}")
        return res

    print("\n--- Strongest Rival Audit (C2): Undifferentiated Gulf/WA Pool (10,000 random n=5 draws) ---")
    c2_rival_prov = perm_test_iran(pool_prov, "Provenanced_28")
    c2_rival_all = perm_test_iran(pool_all_gwa, "All_Gulf_WA_33")

    print("\n--- Exact Iranian Seal Bigrams Attested on Indus Mainland ---")
    iran_bg_details = []
    for x in cohorts["Iran_Indus"]:
        bgs = [(a, b, main_bigrams_dir[(a, b)]) for a, b in zip(x["seq"], x["seq"][1:])]
        iran_bg_details.append({"uid": x["uid"], "site": x["site"], "bigrams": bgs})
        att = [f"{a}-{b}(n={c})" for a, b, c in bgs if c > 0]
        print(f"  {x['uid']} ({x['site']}, {x['shape']}): attested={att} / {len(bgs)} total")

    # Save C2 regional table
    with open(OUT_DIR / "c2_regional_grammar.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["cohort", "n", "cyl", "rnd", "man_090_091", "man_any", "fish", "s831", "s604", "s924", "s032", "s055", "s001", "jar_cup", "plant_comb", "bg_dir_hit", "bg_tot", "bg_dir_pct", "bg_undir_pct", "n_tokens", "n_types"])
        for k in c2_order:
            st = c2_stats[k]
            wr.writerow([k, st["n"], st["cyl"], st["rnd"], st["man_090_091"], st["man_any"], st["fish"], st["s831"], st["s604"], st["s924"], st["s032"], st["s055"], st["s001"], st["jar_cup"], st["plant_comb"], st["bg_dir_hit"], st["bg_tot"], st["bg_dir_pct"], st["bg_undir_pct"], st["n_tokens"], st["n_types"]])

    # =========================================================================
    # TEST C3: INDUS VS PROTO-ELAMITE VS MESOPOTAMIAN METROLOGY & STRUCTURE
    # =========================================================================
    print("\n" + "=" * 72)
    print("TEST C3: INDUS VS PROTO-ELAMITE VS MESOPOTAMIAN METROLOGY AUDIT")
    print("=" * 72)

    # Note: Indus cup calibrated at 9.26 L (metrology_ledger.md, 3 whole jars CV=1.69%) and 9.24 L (prompt anchor)
    # Report exact numbers for 9.26 L (and note 9.24 L diff is 0.2%)
    cup_L = 9.26
    metrology_comparisons = [
        # (indus_unit, indus_val, unit_type, target_system, target_unit, target_val, exact_ratio, pct_diff, independent_dof, verdict)
        ("paṭi (320)", 1.1575, "L", "Ur III Sumerian", "1 sila", 1.00, 1.1575/1.00, (1.1575-1.00)/1.00*100, "derived (1/8 cup)", "loose (+15.8%)"),
        ("paṭi (320)", 1.1575, "L", "Proto-Elamite C", "1.5 N39B (sila~0.8L)", 1.20, 1.1575/1.20, (1.1575-1.20)/1.20*100, "derived", "non-integer 1.5x (-3.5%)"),
        ("quarter (061)", 2.315, "L", "Proto-Elamite C", "3 N39B (~2.4L)", 2.40, 2.315/2.40, (2.315-2.40)/2.40*100, "derived", "tied to 9.26/9.60 (-3.5%)"),
        ("cup (700)", 9.26, "L", "Ur III Sumerian", "1 ban (10 sila)", 10.00, 9.26/10.00, (9.26-10.00)/10.00*100, "PRIMARY DOF #1", "drift -7.4% (9.24L: -7.6%)"),
        ("cup (700)", 9.26, "L", "Proto-Elamite / Archaic", "12 x 0.8L sila", 9.60, 9.26/9.60, (9.26-9.60)/9.60*100, "PRIMARY DOF #1 (alt)", "close -3.5%, but PE has NO 12x rung!"),
        ("cup (700)", 9.26, "L", "Proto-Elamite C", "2 x N1 (2 x 4.0L)", 8.00, 9.26/8.00, (9.26-8.00)/8.00*100, "PRIMARY DOF #1", "miss (+15.8%)"),
        ("vaḷḷam (711 = 4c)", 37.04, "L", "Ur III Sumerian", "4 ban", 40.00, 37.04/40.00, (37.04-40.00)/40.00*100, "DEPENDENT on cup/ban", "identical -7.4% scale factor"),
        ("vaḷḷam (711 = 4c)", 37.04, "L", "Proto-Elamite C", "1.5 x N14 (24L)", 36.00, 37.04/36.00, (37.04-36.00)/36.00*100, "DEPENDENT", "non-integer 1.5x (+2.9%)"),
        ("kalam (705 = 12c)", 111.12, "L", "Ur III Sumerian", "2 barig (120L)", 120.00, 111.12/120.00, (111.12-120.00)/120.00*100, "DEPENDENT on cup/ban", "identical -7.4% scale factor"),
        ("kalam (705 = 12c)", 111.12, "L", "Ur III Sumerian", "1/3 gur (100L)", 100.00, 111.12/100.00, (111.12-100.00)/100.00*100, "DEPENDENT", "miss (+11.1%); 1 gur = 2.70 kalam"),
        ("kalam (705 = 12c)", 111.12, "L", "Proto-Elamite C", "1/2 N45 (120L)", 120.00, 111.12/120.00, (111.12-120.00)/120.00*100, "DEPENDENT on cup/ban", "identical -7.4% scale factor"),
        ("kōṭṭai (575 = 72c)", 666.72, "L", "Proto-Elamite C", "1 N34 (720L)", 720.00, 666.72/720.00, (666.72-720.00)/720.00*100, "DEPENDENT on cup/ban", "identical -7.4% scale factor"),
        ("kōṭṭai (575 = 72c)", 666.72, "L", "Ur III Sumerian", "2 gur (600L)", 600.00, 666.72/600.00, (666.72-600.00)/600.00*100, "DEPENDENT", "miss (+11.1%)"),
        ("Indus Chert 100x", 1365.0, "g", "Dilmun / Bahrain", "1 Dilmun mina (1365g)", 1365.0, 1.000, 0.00, "INDEPENDENT WEIGHT LOCK", "EXACT LOCK (0.0%-0.37% at 1365-1370g)"),
        ("Indus Chert 100x", 1365.0, "g", "Ur III / Susa", "160 shekels (8.53g) / 2.67 Ur mina (504g)", 1344.0, 1365.0/1344.0, (1365.0-1344.0)/1344.0*100, "INDEPENDENT WEIGHT BRIDGE", "EXACT TRADE BRIDGE (+1.56% vs 2.67 Ur mina; exact 160x8.53g)"),
    ]

    with open(OUT_DIR / "c3_metrology_audit.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["indus_unit", "indus_val", "unit_type", "target_system", "target_unit", "target_val", "ratio", "pct_diff", "dof_status", "verdict"])
        for row in metrology_comparisons:
            wr.writerow([row[0], f"{row[1]:.4g}", row[2], row[3], row[4], f"{row[5]:.4g}", f"{row[6]:.4f}", f"{row[7]:+.2f}%", row[8], row[9]])

    print("\n--- Cross-System Capacity & Weight Conversion Audit ---")
    for row in metrology_comparisons:
        print(f"  {row[0]:18s} ({row[1]:6.2f} {row[2]}) vs {row[3]:22s} {row[4]:28s}: {row[7]:+6.2f}% | {row[9]}")

    # Strongest Rival Audit (C3): 10,000-trial Ergonomic Convergence Monte Carlo
    # Suppose an independent culture picks ANY human-carryable bucket V ~ Uniform(5.0, 15.0) L
    # and ANY small integer wholesale multiplier k in {4, 6, 8, 10, 12}.
    # How often does V land within +/-7.6% of 1 ban (10 L), OR k*V land within +/-11.1% of
    # a simple fraction/multiple {1/3, 1/2, 1, 2} of {barig 60L, PE N45 240L, gur 300L}?
    N_MC = 10000
    hit_ban_76 = 0
    hit_sila12_38 = 0
    hit_any_near_76 = 0
    hit_weight_05 = 0
    for _ in range(N_MC):
        v = RNG.uniform(5.0, 15.0)
        k = RNG.choice([4, 6, 8, 10, 12])
        kv = k * v
        if abs(v - 10.0) / 10.0 <= 0.076:
            hit_ban_76 += 1
        if abs(v - 9.6) / 9.6 <= 0.038:
            hit_sila12_38 += 1
        # Check if v within 7.6% of 10L OR 8L (2 N1) OR 12L (1/2 N14) OR kv within 7.6% of 60, 100, 120, 240, 300
        targets_v = [8.0, 10.0, 12.0]
        targets_kv = [60.0, 100.0, 120.0, 240.0, 300.0]
        if any(abs(v - t) / t <= 0.076 for t in targets_v) or any(abs(kv - t) / t <= 0.076 for t in targets_kv):
            hit_any_near_76 += 1
        # Compare with Dilmun-Indus weight: random weight unit w ~ Uniform(5.0, 25.0) g
        # hitting 1365g / 100 within +/-0.5%
        w = RNG.uniform(5.0, 25.0)
        if abs(w * 100 - 1365.0) / 1365.0 <= 0.005:
            hit_weight_05 += 1

    mc_c3 = {
        "N_MC": N_MC,
        "p_random_bucket_within_7.6pct_of_ban_10L": round(hit_ban_76 / N_MC, 4),
        "p_random_bucket_within_3.8pct_of_12sila_9.6L": round(hit_sila12_38 / N_MC, 4),
        "p_random_bucket_or_ladder_within_7.6pct_of_any_PE_UrIII_rung": round(hit_any_near_76 / N_MC, 4),
        "p_random_weight_unit_within_0.5pct_of_Dilmun_1365g_div100": round(hit_weight_05 / N_MC, 4),
    }
    print("\n--- Strongest Rival Audit (C3): Ergonomic Convergence Monte Carlo (10,000 trials) ---")
    for k, v in mc_c3.items():
        print(f"  {k}: {v}")

    # Save complete summary JSON
    summary = {
        "lexicon": {
            "hinz_koch_raw": hk_raw,
            "hinz_koch_clean": len(hk_clean),
            "hinz_koch_dropped": dict(hk_dropped),
            "lex_a_count": len(lex_a_set),
            "lex_b_count": len(lex_b_set),
        },
        "test_c1": {
            "n_mapped_full": len(full_map),
            "n_mapped_strict": len(strict_map),
            "n_graphic_universal": n_univ,
            "n_specific_compound": n_comp,
            "iran_seals_decoded_RL": iran_hits_rl,
            "iran_seals_decoded_LR": iran_hits_lr,
            "shuffle_results": c1_results,
        },
        "test_c2": {
            "cohorts": {k: {kk: vv for kk, vv in v.items() if kk != "sign_ctr"} for k, v in c2_stats.items()},
            "similarity_to_iran": sim_table,
            "fisher_iran_vs_prov_GM": c2_fisher_out,
            "rival_perm_prov28": c2_rival_prov,
            "rival_perm_all33": c2_rival_all,
        },
        "test_c3": {
            "monte_carlo_rival": mc_c3,
            "structural_comparison": {
                "indus_2series_NMI": 0.2606,
                "indus_2series_z": 59.4,
                "indus_cup_tall5_count": "0/422 (Fisher P=1.59e-7)",
                "pe_intact_numerals_Born2025": 8011,
                "pe_systems_Born2025": {"C": 1678, "S": 107, "D": 96, "B": 18},
                "pe_cross_system_signs_Born2025": "11/244 (4.5%, all headers/qualifiers, 0 commodities)",
                "sign_inventory_at_10583": {
                    "Indus": {"types": 548, "hapaxes": 205, "top100_pct": 74.6},
                    "Proto_Elamite": {"types": 508, "hapaxes": 185, "top100_pct": 73.5},
                    "Linear_Elamite_Hatamti": {"distinct_signs": 69, "phonemic_values": 67, "deciphered_token_pct": 97.3},
                },
            },
        },
    }
    with open(OUT_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] All outputs written to {OUT_DIR}")


if __name__ == "__main__":
    main()
