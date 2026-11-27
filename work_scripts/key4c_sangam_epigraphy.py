#!/usr/bin/env python3
"""
Key #4C (Lever 3): Old Tamil Sangam & Early Tamil-Brahmi Epigraphic Lexicon Bridge
with Matched Rival Epigraphic Controls (Early Indo-Aryan/Prakrit Brahmi & Ur III Sumerian)
and 5,000-Shuffle Blind Statistical Tests.

Strictly rerunnable script. Saves all outputs to:
  work_data/key4c/
"""

import csv
import json
import math
import os
import re
import unicodedata
from collections import Counter, defaultdict

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = f"{BASE}/work_data/key4c"
os.makedirs(OUT_DIR, exist_ok=True)

N_SHUFFLES = 5000
RNG_SEED = 20261119


# =============================================================================
# Phonological normalization & Dravidian sandhi (aligned with key2a / key3a)
# =============================================================================
def strip_diacritics(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace("ḵ", "k").replace("ḥ", "h").replace("ṃ", "m").replace("ṅ", "n").replace("ñ", "n")
    return re.sub(r"[^a-z]", "", s)


def norm_phon(s: str) -> str:
    """Coarse Dravidian phonological key preserving stop/nasal/liquid classes (matching key3a)."""
    s = strip_diacritics(s)
    # Collapse geminates for robust sandhi comparison while keeping root structure
    s = re.sub(r"([a-z])\1+", r"\1", s)
    return s


def dravidian_sandhi_joins(a: str, b: str):
    """
    Generate standard Old Tamil / Proto-Dravidian compound sandhi surfaces from (root_a, root_b).
    Returns a set of normalized ascii forms AND collapsed phon forms.
    """
    a0 = strip_diacritics(a)
    b0 = strip_diacritics(b)
    if not a0 or not b0:
        return set(), set()

    V = set("aeiou")
    STOPS = set("kcttp")
    raw = set()
    raw.add(a0 + b0)

    # 1. Gemination of initial voiceless stop (talaikkuṭi, aṭikkuṭi, paṭikkāl, mukkāl, mummīṉ)
    if b0[0] in ("k", "c", "t", "p", "m", "n"):
        raw.add(a0 + b0[0] + b0)

    # 2. Glide insertion between vowels (kuṭi + āḷ -> kuṭiyāḷ; iṟai + āṉ -> iṟaiyāṉ)
    if a0[-1] in ("i", "e", "y") and b0[0] in V:
        raw.add(a0 + "y" + b0)
    if a0[-1] in ("u", "a", "o") and b0[0] in V:
        raw.add(a0 + "v" + b0)

    # 3. Final -u elision before vowel (iru + aṭi -> iraṭi; aṟu + ā -> aṟā; maruppu + a -> maruppa)
    if a0.endswith("u") and len(a0) >= 3 and b0[0] in V:
        raw.add(a0[:-1] + b0)
    # Final -i elision rarely, keep conservative

    # 4. Final -am -> -a + geminate / -att- strictly before CONSONANTS (kaḷam + pāy -> kaḷappāy; maram + kāl -> marakkāl)
    if a0.endswith("am") and len(a0) >= 4 and b0[0] not in V:
        stem = a0[:-1]  # kala
        raw.add(stem + b0)
        if b0[0] in ("k", "c", "t", "p"):
            raw.add(stem + b0[0] + b0)
        raw.add(stem + "tt" + b0)

    # 5. Final -l / -n assimilation (nal + min -> nalmin / nanmin; vel + ir -> velir)
    if a0.endswith("l") and b0.startswith("m"):
        raw.add(a0[:-1] + "n" + b0)
    if a0.endswith("n") and b0.startswith("k"):
        raw.add(a0 + b0)

    # 6. Numeral allomorphs in Old Tamil compounds:
    # iru -> ir before vowel (īraṭi), ir before plural suffix (-ir: vēḷ+iru -> vēḷir)
    if a0 == "iru" and b0[0] in V:
        raw.add("ir" + b0)
    if b0 == "iru" and a0[-1] not in V:
        raw.add(a0 + "ir")
    # mu -> mun / muv before vowel
    if a0 == "mu" and b0[0] in V:
        raw.add("muv" + b0)
    # ai -> aim before labial, ain before dental
    if a0 == "ai":
        if b0[0] in ("p", "m"):
            raw.add("aim" + b0)
        elif b0[0] in ("t", "n"):
            raw.add("ain" + b0)
        elif b0[0] in ("k",):
            raw.add("ain" + b0)
    # nal -> nan before nasal/t
    if a0 == "nal" and b0[0] in ("m", "n", "t"):
        raw.add("nan" + b0)
        if b0[0] == "t":
            raw.add("nat" + b0)

    phon = {norm_phon(x) for x in raw}
    return raw, phon


def ia_sandhi_joins(a: str, b: str):
    """Standard Sanskrit/Prakrit compound joins for matched Indo-Aryan control."""
    a0 = strip_diacritics(a)
    b0 = strip_diacritics(b)
    if not a0 or not b0:
        return set(), set()
    raw = {a0 + b0}
    # Basic vowel sandhi (a+a->a, a+i->e, a+u->o, final -a drop before vowel)
    if a0.endswith("a") and b0.startswith("a"):
        raw.add(a0[:-1] + b0)
    if a0.endswith("a") and b0.startswith("i"):
        raw.add(a0[:-1] + "e" + b0[1:])
    if a0.endswith("a") and b0.startswith("u"):
        raw.add(a0[:-1] + "o" + b0[1:])
    if a0.endswith("n") and len(a0) >= 4:
        raw.add(a0[:-1] + b0)  # rajan -> raja + X
    if a0.endswith("s") and len(a0) >= 4:
        raw.add(a0[:-1] + b0)
    if a0 == "dvi":
        raw.add("dva" + b0)
    if a0 == "catur":
        raw.add("catu" + b0)
    if a0 == "panca":
        raw.add("panca" + b0)
    phon = {norm_phon(x) for x in raw}
    return raw, phon


def sumerian_joins(a: str, b: str):
    """Standard Sumerian compound joins (hyphenated or concatenated, dropping digit indices)."""
    a0 = re.sub(r"\d+", "", a.lower()).strip()
    b0 = re.sub(r"\d+", "", b.lower()).strip()
    a1 = re.sub(r"[^a-z]", "", a0)
    b1 = re.sub(r"[^a-z]", "", b0)
    if not a1 or not b1:
        return set(), set()
    raw = {a1 + b1, a0 + "-" + b0}
    phon = {norm_phon(a1 + b1)}
    return raw, phon


def fisher_one_sided_gt(a, b, c, d):
    """Exact one-sided Fisher test P(X >= a) for 2x2 table [[a, b], [c, d]]."""
    n = a + b + c + d
    r1 = a + b
    c1 = a + c

    def log_comb(nn, kk):
        if kk < 0 or kk > nn:
            return float("-inf")
        return math.lgamma(nn + 1) - math.lgamma(kk + 1) - math.lgamma(nn - kk + 1)

    denom = log_comb(n, c1)
    p = 0.0
    lo = max(a, r1 + c1 - n)
    hi = min(r1, c1)
    for k in range(lo, hi + 1):
        p += math.exp(log_comb(r1, k) + log_comb(n - r1, c1 - k) - denom)
    return min(1.0, p)


def p_and_z(obs: float, null_arr: np.ndarray):
    """Empirical one-sided P-value (obs >= null) and z-score."""
    mean = float(np.mean(null_arr))
    std = float(np.std(null_arr, ddof=1)) if len(null_arr) > 1 else 0.0
    z = (obs - mean) / std if std > 1e-12 else (99.0 if obs > mean else 0.0)
    p = (int(np.sum(null_arr >= obs)) + 1) / (len(null_arr) + 1)
    return mean, std, z, p


# =============================================================================
# Load raw DEDR cleanly (splitting any merged lines & extracting all Tamil headwords)
# =============================================================================
def load_raw_dedr():
    path = f"{BASE}/work_data/lexicons/dedr/dedr_entries.tsv"
    entries = {}
    with open(path) as f:
        for line in f:
            if "\t" not in line:
                continue
            eid, txt = line.rstrip("\n").split("\t", 1)
            parts = re.split(
                r"(?<=\.)\s+(\d{1,4})\s+(?=(?:Ta|Ma|Ko|To|Ka|Koḍ|Tu|Te|Kol|Nk|Pa|Ga|Go|Konḍa|Pe|Manḍ|Kui|Kuwi|Kur|Malt|Br)\.)",
                txt,
            )
            entries[eid] = parts[0]
            for i in range(1, len(parts), 2):
                entries[parts[i]] = parts[i + 1]

    # Extract clean Tamil headwords AND 2-branch DEDR roots (for equal-length null draws)
    ta_headwords_ascii = set()
    ta_headwords_phon = set()
    all_2branch_roots = []  # (eid, root_ascii, len_root)

    lang_pat = re.compile(r"\b(Ta|Ma|Ko|To|Ka|Koḍ|Tu|Te|Kol|Nk|Pa|Ga|Go|Konḍa|Pe|Manḍ|Kui|Kuwi|Kur|Malt|Br)\.")
    south_langs = {"Ta", "Ma", "Ko", "To", "Ka", "Koḍ", "Tu"}
    other_langs = {"Te", "Kol", "Nk", "Pa", "Ga", "Go", "Konḍa", "Pe", "Manḍ", "Kui", "Kuwi", "Kur", "Malt", "Br"}

    for eid, txt in entries.items():
        txt_nfc = unicodedata.normalize("NFC", txt)
        langs = set(lang_pat.findall(txt_nfc))
        # Parse Tamil segment up to next language marker
        m_ta = re.search(r"\bTa\.\s+([^.]+)", txt_nfc)
        if m_ta:
            ta_seg = m_ta.group(1)
            # Extract headwords before glosses: tokens at start and after semicolons
            clauses = ta_seg.split(";")
            first_root = None
            for cl in clauses:
                cl = cl.strip()
                # Take leading comma-separated Tamil headwords (often italicized/diacriticized, before English words)
                # Heuristic: take first 1-3 tokens before English gloss words
                m_hw = re.match(r"^([a-zA-Zāīūēōṭḍṇṟṉḷḻṛṅñr̤\-]+(?:\s*,\s*[a-zA-Zāīūēōṭḍṇṟṉḷḻṛṅñr̤\-]+)*)", cl)
                if m_hw:
                    for hw in m_hw.group(1).split(","):
                        hw_clean = hw.strip().replace("-", "")
                        asc = strip_diacritics(hw_clean)
                        if 2 <= len(asc) <= 16:
                            ta_headwords_ascii.add(asc)
                            ta_headwords_phon.add(norm_phon(asc))
                            if first_root is None:
                                first_root = asc
            if first_root and (langs & south_langs) and (langs & other_langs):
                all_2branch_roots.append((eid, first_root, len(first_root)))

    return entries, ta_headwords_ascii, ta_headwords_phon, all_2branch_roots


# =============================================================================
# PART 1: Verified Old Tamil Sangam & Early Tamil-Brahmi Epigraphy Lexicon
#         (Pure Dravidian strictly separated from Prakrit/Sanskrit Loans!)
# =============================================================================
# Tuple schema:
# (id, form, category, etymology_layer, dedr_id, components, gloss, attestation_source)
SANGAM_EPIGRAPHY_ENTRIES = [
    # --- HOUSE / CLAN & ADMINISTRATIVE TITLES (PURE DRAVIDIAN) ---
    ("TAM01", "kuṭiyāḷ", "house_clan", "pure_dravidian", "1655+399", "kuṭi+āḷ", "house-tenant, estate manager/worker", "U. Madras Tamil Lexicon (Mal. kuṭiyāl); Sangam/Chola usage"),
    ("TAM02", "aṭikkuṭi", "house_clan", "pure_dravidian", "72+1655", "aṭi+kuṭi", "original/base/subordinate household", "U. Madras Tamil Lexicon (aṭikkuṭi/aṭikkuṭil)"),
    ("TAM03", "ciṟukuṭi", "house_clan", "pure_dravidian", "1594+1655", "ciṟu+kuṭi", "small village, hamlet, settlement", "Puṟanāṉūṟu 127, 329; Akaṉāṉūṟu 208; Malaipaṭukaṭām"),
    ("TAM04", "mutukuṭi", "house_clan", "pure_dravidian", "4954+1655", "mutu+kuṭi", "ancient noble clan/house", "Puṟanāṉūṟu 287, 312; Tolkāppiyam"),
    ("TAM05", "orukuṭi", "house_clan", "pure_dravidian", "990+1655", "oru+kuṭi", "single household/lineage", "Tirukkuṟaḷ 1029; Classical Tamil"),
    ("TAM06", "kuṭiyiṟai", "admin_title", "pure_dravidian", "1655+521", "kuṭi+iṟai", "household tax, tenant assessment", "Chola/Pandya inscriptions; U. Madras Tamil Lexicon"),
    ("TAM07", "vēḷir", "admin_title", "pure_dravidian", "5545", "vēḷ+ir", "Velir chieftains, hereditary lineage lords", "Puṟanāṉūṟu 24, 201; Tolkāppiyam; Tamil-Brahmi"),
    ("TAM08", "vēḷāḷaṉ", "admin_title", "pure_dravidian", "5545+399", "vēḷ+āḷ+aṉ", "landed chief, agricultural estate-holder", "Tolkāppiyam; Puṟanāṉūṟu; Tamil Lexicon"),
    ("TAM09", "kālāḷ", "admin_title", "pure_dravidian", "1479+399", "kāl+āḷ", "foot-soldier, infantryman", "Puṟanāṉūṟu; Patirruppattu; DEDR 1479"),
    ("TAM10", "kaṇkāṇi", "admin_title", "pure_dravidian", "1159+1443", "kaṇ+kāṇi", "overseer, supervisor, inspector of accounts", "Chola inscriptions; U. Madras Tamil Lexicon"),
    ("TAM11", "kāval", "admin_title", "pure_dravidian", "1416", "kā+val", "guard, watch, royal protection/garrison", "Puṟanāṉūṟu; Paṭṭiṉappālai 134"),
    ("TAM12", "kāvalaṉ", "admin_title", "pure_dravidian", "1416", "kāval+aṉ", "guardian, protector, king", "Puṟanāṉūṟu; Maturaikkāñci"),
    ("TAM13", "kāviti", "admin_title", "pure_dravidian", "1416?", "kāviti", "revenue minister/accountant title conferred on Velalas/merchants", "Tolkāppiyam Po. 30; Maturaikkāñci 499; Tamil-Brahmi Mangulam 3,6 (Mahadevan 2003)"),
    ("TAM14", "kiḻāṉ", "admin_title", "pure_dravidian", "1979", "kiḻa+aṉ", "village headman, hereditary proprietor/lord", "Puṟanāṉūṟu 35, 395; Tamil-Brahmi; U. Madras Tamil Lexicon"),
    ("TAM15", "kiḻavaṉ", "admin_title", "pure_dravidian", "1979", "kiḻa+vaṉ", "lord, owner, chief, elder", "Tolkāppiyam; Puṟanāṉūṟu"),
    ("TAM16", "aṭiyāṉ", "admin_title", "pure_dravidian", "72", "aṭi+āṉ", "servant, subordinate, devotee", "Sangam/Early Tamil; U. Madras Tamil Lexicon"),
    ("TAM17", "aṭiyār", "admin_title", "pure_dravidian", "72", "aṭi+ār", "servants, retainers, devotees", "Classical Tamil; DEDR 72"),
    ("TAM18", "talaivaṉ", "admin_title", "pure_dravidian", "3103", "talai+vaṉ", "chief, headman, commander, lord", "Tolkāppiyam; Puṟanāṉūṟu; DEDR 3103"),
    ("TAM19", "talaimai", "admin_title", "pure_dravidian", "3103", "talai+mai", "headship, leadership, pre-eminence", "Tolkāppiyam; DEDR 3103"),
    ("TAM20", "perumāṉ", "admin_title", "pure_dravidian", "4411", "peru+māṉ", "great lord, sovereign, noble", "Puṟanāṉūṟu 6, 38; Tamil-Brahmi"),
    ("TAM21", "iṟaiyāṉ", "admin_title", "pure_dravidian", "527", "iṟai+āṉ", "sovereign, lord, master", "Tolkāppiyam; Classical Tamil"),
    ("TAM22", "iṟaivaṉ", "admin_title", "pure_dravidian", "527", "iṟai+vaṉ", "king, supreme lord, chief", "Puṟanāṉūṟu; Tirukkuṟaḷ"),
    ("TAM23", "kōṉ", "admin_title", "pure_dravidian", "2177", "kō+ṉ", "king, chief, ruler", "Puṟanāṉūṟu; Tamil-Brahmi Pugalur (kō ātaṉ cel irumpoṟai, Mahadevan 2003)"),
    ("TAM24", "orutalai", "admin_title", "pure_dravidian", "990+3103", "oru+talai", "one side, certainty, steadfast/single-headed", "Puṟanāṉūṟu; Tirukkuṟaḷ 1196; U. Madras Tamil Lexicon"),
    ("TAM25", "īraṭi", "admin_title", "pure_dravidian", "474+72", "īr+aṭi", "two feet, couplet, double-step", "U. Madras Tamil Lexicon (īraṭi)"),
    ("TAM26", "paṭiyāḷ", "admin_title", "pure_dravidian", "3849+399", "paṭi+āḷ", "hired retainer paid in grain ration (paṭi)", "DEDR 3849; U. Madras Tamil Lexicon"),
    ("TAM27", "mīṉavaṉ", "admin_title", "pure_dravidian", "4885", "mīṉ+avaṉ", "fisherman; Pandya royal title (fish-emblem)", "Puṟanāṉūṟu; Maturaikkāñci; U. Madras Tamil Lexicon"),
    ("TAM28", "paratavar", "maritime_trade", "pure_dravidian", "3957", "paratu+avar", "coastal sea-traders, pearl-divers, fishermen", "Paṭṭiṉappālai 111; Maturaikkāñci 144, 316; DEDR 3957"),
    ("TAM29", "mūvēntar", "admin_title", "pure_dravidian", "5052+5529", "mū+vēntar", "the Three Crowned Kings (Chera, Chola, Pandya)", "Tolkāppiyam; Puṟanāṉūṟu 35, 357"),
    ("TAM30", "uṭaiyāṉ", "admin_title", "pure_dravidian", "593", "uṭai+āṉ", "owner, possessor, district chief", "Early Tamil/Chola epigraphy; DEDR 593"),
    ("TAM31", "paṇaiyāḷ", "admin_title", "pure_dravidian", "3891+399", "paṇai+āḷ", "farm/estate laborer, tenant", "U. Madras Tamil Lexicon (s.v. kuṭiyāḷ)"),
    ("TAM32", "kalavar", "maritime_trade", "pure_dravidian", "1305", "kalam+ar", "navigators, shipmen, mariners", "DEDR 1305; Classical Tamil"),
    ("TAM33", "kaḷamar", "admin_title", "pure_dravidian", "1376", "kaḷam+ar", "threshing-floor cultivators, warriors", "Puṟanāṉūṟu; Maturaikkāñci; DEDR 1376"),
    ("TAM34", "kaṉṉāṉ", "admin_title", "pure_dravidian", "1402", "kaṉ+āṉ", "brazier, coppersmith, metalworker", "DEDR 1402; U. Madras Tamil Lexicon"),
    ("TAM35", "paṭavaṉ", "maritime_trade", "pure_dravidian", "3838", "paṭaku+aṉ", "boatman, mariner", "DEDR 3838; Classical Tamil"),

    # --- ASTRAL & CALENDAR COMPOUNDS (PURE DRAVIDIAN) ---
    ("TAM36", "aṟumīṉ", "astral_calendar", "pure_dravidian", "2485+4876", "aṟu+mīṉ", "Pleiades (Six Stars / Kṛttikā)", "Paripāṭal 5.49; Piṅkalantai; U. Madras Tamil Lexicon"),
    ("TAM37", "mummīṉ", "astral_calendar", "pure_dravidian", "5052+4876", "mu+mīṉ", "5th nakṣatra Mṛgaśīrṣa (Three Stars in Orion)", "Divākaram; U. Madras Tamil Lexicon (mummīṉ)"),
    ("TAM38", "eḻumīṉ", "astral_calendar", "pure_dravidian", "910+4876", "eḻu+mīṉ", "Ursa Major (Seven Stars)", "Classical Tamil astronomy; Tamil Lexicon"),
    ("TAM39", "nāḷmīṉ", "astral_calendar", "pure_dravidian", "3656+4876", "nāḷ+mīṉ", "lunar asterism, day-star, constellation", "Puṟanāṉūṟu 229; Paṭṭiṉappālai; Tamil Lexicon"),
    ("TAM40", "vālmīṉ", "astral_calendar", "pure_dravidian", "5367+4876", "vāl+mīṉ", "comet (tailed star)", "Puṟanāṉūṟu 229; U. Madras Tamil Lexicon"),
    ("TAM41", "cemmīṉ", "astral_calendar", "pure_dravidian", "1931+4876", "cem+mīṉ", "Mars (red star), Arundhati, Ārdrā", "Puṟanāṉūṟu 60; Paripāṭal; U. Madras Tamil Lexicon"),
    ("TAM42", "veḷḷimīṉ", "astral_calendar", "pure_dravidian", "5496+4876", "veḷḷi+mīṉ", "Venus (bright white star)", "Puṟanāṉūṟu 385; Paṭṭiṉappālai 1"),
    ("TAM43", "vāṉmīṉ", "astral_calendar", "pure_dravidian", "5381+4876", "vāṉ+mīṉ", "sky-star, celestial star", "Akaṉāṉūṟu; U. Madras Tamil Lexicon"),
    ("TAM44", "tiṅkaḷ", "astral_calendar", "pure_dravidian", "3213", "tiṅkaḷ", "moon, lunar month", "Puṟanāṉūṟu; Tolkāppiyam; DEDR 3213"),
    ("TAM45", "muttiṅkaḷ", "astral_calendar", "pure_dravidian", "5052+3213", "mu+tiṅkaḷ", "three months, quarter-year period", "Classical Tamil; Tamil Lexicon"),

    # --- MARITIME, TRADE & COMMODITY TERMS (PURE DRAVIDIAN) ---
    ("TAM46", "kaḷappāy", "maritime_trade", "pure_dravidian", "1376+4088", "kaḷam+pāy", "mat spread on threshing floor for grain; cf. kalam+pāy ship-sail", "U. Madras Tamil Lexicon (kaḷappāy)"),
    ("TAM47", "paṭikkāl", "maritime_trade", "pure_dravidian", "3850+1479", "paṭi+kāl", "ladder, step-rung frame", "Paṭṭiṉappālai 142 (kuṟuntoṭai neṭumpaṭikkāl); U. Madras Tamil Lexicon"),
    ("TAM48", "paṭikkal", "metrology", "pure_dravidian", "3849+1298", "paṭi+kal", "stamped weighing stone, standard weight", "U. Madras Tamil Lexicon (Ka. paḍi-kallu)"),
    ("TAM49", "kalam", "maritime_trade", "pure_dravidian", "1305", "kalam", "seagoing ship, earthenware vessel, wholesale grain measure", "Puṟanāṉūṟu 126; Paṭṭiṉappālai 174; Maturaikkāñci 83; DEDR 1305"),
    ("TAM50", "pāy", "maritime_trade", "pure_dravidian", "4088", "pāy", "ship sail, woven mat", "Paṭṭiṉappālai; Maturaikkāñci; DEDR 4088"),
    ("TAM51", "pāymaram", "maritime_trade", "pure_dravidian", "4088+4711", "pāy+maram", "ship's mast (sail-wood)", "Paṭṭiṉappālai; U. Madras Tamil Lexicon"),
    ("TAM52", "paṭaku", "maritime_trade", "pure_dravidian", "3838", "paṭaku", "boat, coastal cargo vessel", "Maturaikkāñci; DEDR 3838"),
    ("TAM53", "tōṇi", "maritime_trade", "pure_dravidian", "3539?", "tōṇi", "dugout/cargo boat, dhoni", "Paṭṭiṉappālai; Puṟanāṉūṟu; Tamil Lexicon"),
    ("TAM54", "tuṟai", "maritime_trade", "pure_dravidian", "3370", "tuṟai", "seaport, harbor, river ford/quay", "Paṭṭiṉappālai 136; Puṟanāṉūṟu 126; DEDR 3370"),
    ("TAM55", "kūṭu", "maritime_trade", "pure_dravidian", "1883", "kūṭu", "granary, grain receptacle, store-enclosure", "Maturaikkāñci; DEDR 1883"),
    ("TAM56", "aṟuvai", "commodity", "pure_dravidian", "318", "aṟuvai", "woven cloth, textile piece", "Maturaikkāñci; Tamil-Brahmi Alagarmalai (aṟuvai vaṇikaṉ, Mahadevan 2003)"),
    ("TAM57", "kaṉ", "commodity", "pure_dravidian", "1402", "kaṉ", "copper, copper-work, metalwork", "Tolkāppiyam; DEDR 1402"),
    ("TAM58", "ceppu", "commodity", "pure_dravidian", "2772", "ceppu", "metal/ivory casket, vessel (cf. cempu copper)", "Puṟanāṉūṟu; DEDR 2772"),
    ("TAM59", "vaḷai", "commodity", "pure_dravidian", "5313", "vaḷai", "conch/shell bangle, ring", "Paṭṭiṉappālai; Maturaikkāñci 316; DEDR 5313"),
    ("TAM60", "eḷ", "commodity", "pure_dravidian", "854", "eḷ", "sesame seed (Sesamum indicum), sesame oil", "Puṟanāṉūṟu; Paṭṭiṉappālai; DEDR 854"),
    ("TAM61", "arici", "commodity", "pure_dravidian", "215", "arici", "husked rice/grain (borrowed into Greek oryza)", "Puṟanāṉūṟu; Perumpāṇāṟṟuppaṭai; DEDR 215"),
    ("TAM62", "tōkai", "commodity", "pure_dravidian", "3538", "tōkai", "peacock tail/plumage (borrowed into Heb. tukkiyyim)", "Puṟanāṉūṟu; Malaipaṭukaṭām; DEDR 3538"),
    ("TAM63", "parutti", "commodity", "pure_dravidian", "3976", "parutti", "cotton (Gossypium herbaceum)", "Puṟanāṉūṟu 125, 326; Maturaikkāñci; DEDR 3976"),
    ("TAM64", "nūl", "commodity", "pure_dravidian", "3726", "nūl", "spun cotton yarn, thread", "Puṟanāṉūṟu 125; Naṟṟiṇai; DEDR 3726"),
    ("TAM65", "maruppu", "commodity", "pure_dravidian", "4720", "maruppu", "ivory tusk, horn of beast", "Puṟanāṉūṟu; Paṭṭiṉappālai; DEDR 4720"),
    ("TAM66", "poṉ", "commodity", "pure_dravidian", "4570", "poṉ", "gold, precious metal", "Puṟanāṉūṟu; Tamil-Brahmi Alagarmalai (poṉ vāṇikaṉ, Mahadevan 2003); DEDR 4570"),
    ("TAM67", "uppu", "commodity", "pure_dravidian", "2674", "uppu", "salt", "Akaṉāṉūṟu; Tamil-Brahmi Alagarmalai (uppu vaṇikaṉ, Mahadevan 2003)"),
    ("TAM68", "irumpu", "commodity", "pure_dravidian", "486", "irumpu", "iron, metal tool/weapon", "Puṟanāṉūṟu; DEDR 486"),

    # --- METROLOGY & FRACTIONS (PURE DRAVIDIAN) ---
    ("TAM69", "paṭi", "metrology", "pure_dravidian", "3849", "paṭi", "standard capacity measure (~1.16 L = 1/8 marakkāl), daily grain ration", "Sangam; Chola inscriptions; DEDR 3849"),
    ("TAM70", "nāḻi", "metrology", "pure_dravidian", "3622?", "nāḻi", "standard capacity measure (= 1 paṭi = 1/8 marakkāl = 1/96 kalam)", "Puṟanāṉūṟu 189; Paṭṭiṉappālai; Chola inscriptions"),
    ("TAM71", "marakkāl", "metrology", "pure_dravidian", "4711+1479", "maram+kāl", "wooden grain measure (= 8 nāḻi/paṭi = 1/12 kalam ~9.24 L)", "Chola inscriptions; U. Madras Tamil Lexicon; DEDR 2208/5315"),
    ("TAM72", "kuṟuṇi", "metrology", "pure_dravidian", "1851", "kuṟu+nāḻi", "grain measure (= 8 nāḻi = 1 marakkāl = 1/12 kalam)", "Chola inscriptions; Nālaṭiyār; U. Madras Tamil Lexicon"),
    ("TAM73", "patakku", "metrology", "pure_dravidian", "3918?", "patakku", "grain measure (= 2 marakkāl/kuṟuṇi = 16 nāḻi = 1/6 kalam)", "Chola inscriptions; U. Madras Tamil Lexicon"),
    ("TAM74", "tūṇi", "metrology", "pure_dravidian", "—", "tūṇi", "grain measure (= 4 marakkāl = 2 patakku = 1/3 kalam ~37 L)", "Puṟanāṉūṟu; Chola inscriptions; U. Madras Tamil Lexicon"),
    ("TAM75", "vaḷḷam", "metrology", "pure_dravidian", "5315", "vaḷḷam", "grain measure (= 4 marakkāl = 1/3 kalam); also canoe/dish", "DEDR 5315 (Ta. vaḷḷam = 4 marakkāl); Tamil Lexicon"),
    ("TAM76", "kōṭṭai", "metrology", "pure_dravidian", "2208", "kōṭṭai", "large grain measure (= 21 marakkāl in medieval South Tamil)", "DEDR 2208; Chola/Pandya inscriptions; Tamil Lexicon"),
    ("TAM77", "paṟai", "metrology", "pure_dravidian", "4032", "paṟai", "grain measure (= 5 marakkāl); drum", "DEDR 4032; Tamil/Malayalam metrology"),
    ("TAM78", "kāṇi", "metrology", "pure_dravidian", "1443", "kāṇi", "fraction 1/80; hereditary land-share", "Chola inscriptions; U. Madras Tamil Lexicon"),
    ("TAM79", "kāl", "metrology", "pure_dravidian", "1479", "kāl", "quarter fraction (1/4); leg/wheel", "Tolkāppiyam; Sangam; Chola inscriptions; DEDR 1479"),
    ("TAM80", "arai", "metrology", "pure_dravidian", "229", "arai", "half fraction (1/2)", "Tolkāppiyam; Sangam; DEDR 229"),
    ("TAM81", "mukkāl", "metrology", "pure_dravidian", "5052+1479", "mu+kāl", "three-quarters fraction (3/4)", "Tolkāppiyam; Chola inscriptions; U. Madras Tamil Lexicon"),
    ("TAM82", "irukāl", "metrology", "pure_dravidian", "474+1479", "iru+kāl", "two-quarters / twice / two-legged", "Sangam; U. Madras Tamil Lexicon"),
    ("TAM83", "araikkāl", "metrology", "pure_dravidian", "229+1479", "arai+kāl", "one-eighth fraction (1/8)", "Chola inscriptions; U. Madras Tamil Lexicon"),
    ("TAM84", "paṉṉiru", "metrology", "pure_dravidian", "3918+474", "paṉ+iru", "twelve / dozen (compounding base)", "Tolkāppiyam; Tirumurukāṟṟuppaṭai"),
    ("TAM85", "niṟai", "metrology", "pure_dravidian", "3682", "niṟai", "weight standard, balance, fullness", "Tolkāppiyam; Puṟanāṉūṟu; DEDR 3682"),
    ("TAM86", "kaḻañcu", "metrology", "pure_dravidian", "1348", "kaḻañcu", "gold/metal weight standard (~5 g)", "Chola inscriptions; DEDR 1348"),

    # --- EXPLICITLY SEPARATED PRAKRIT / SANSKRIT LOANWORDS IN EARLY TAMIL-BRAHMI ---
    ("LOAN01", "nikama", "admin_title", "prakrit_sanskrit_loan", "LOAN<Skt.nigama", "nikama", "merchant guild, market town (< Pkt./Skt. nigama)", "Tamil-Brahmi Mangulam 3, 6 (Mahadevan 2003)"),
    ("LOAN02", "vaṇikaṉ", "maritime_trade", "prakrit_sanskrit_loan", "LOAN<Skt.vaṇij", "vaṇika+ṉ", "merchant, trader (< Pkt. vaṇija / Skt. vaṇij)", "Tamil-Brahmi Alagarmalai 1-10 (Mahadevan 2003)"),
    ("LOAN03", "cāttu", "maritime_trade", "prakrit_sanskrit_loan", "LOAN<Skt.sārtha", "cāttu", "merchant caravan (< Pkt. sattha / Skt. sārtha)", "Sangam / Tamil-Brahmi (cāttaṉ)"),
    ("LOAN04", "paṇṭam", "commodity", "prakrit_sanskrit_loan", "LOAN<Skt.bhāṇḍa", "paṇṭam", "merchandise, trade goods (< Pkt. bhaṇḍa / Skt. bhāṇḍa)", "Paṭṭiṉappālai; Maturaikkāñci (distinct from native DEDR 3898 belly)"),
    ("LOAN05", "tammam", "admin_title", "prakrit_sanskrit_loan", "LOAN<Skt.dharma", "tammam", "pious gift, religious law (< Pkt. dhamma)", "Tamil-Brahmi Mangulam 1 (dhammam, Mahadevan 2003)"),
    ("LOAN06", "amaṇaṉ", "admin_title", "prakrit_sanskrit_loan", "LOAN<Skt.śramaṇa", "amaṇa+ṉ", "Jain ascetic/monk (< Pkt. samaṇa)", "Tamil-Brahmi Pugalur 1, Kongarpuliyankulam (Mahadevan 2003)"),
    ("LOAN07", "upācaṉ", "admin_title", "prakrit_sanskrit_loan", "LOAN<Skt.upāsaka", "upāca+ṉ", "lay devotee (< Pkt. upāsaka)", "Tamil-Brahmi Kongarpuliyankulam (Mahadevan 2003)"),
    ("LOAN08", "atiṭṭāṉam", "admin_title", "prakrit_sanskrit_loan", "LOAN<Skt.adhiṣṭhāna", "atiṭṭāṉam", "stone bed/seat (< Pkt. adhiṭṭhāna)", "Tamil-Brahmi Sittannavasal 1, Pugalur (Mahadevan 2003)"),
    ("LOAN09", "eṭṭi", "admin_title", "prakrit_sanskrit_loan", "LOAN<Skt.śreṣṭhin", "eṭṭi", "chief merchant title (< Pkt. seṭṭhi / Skt. śreṣṭhin)", "Maturaikkāñci; Maṇimēkalai; Tamil Lexicon"),
    ("LOAN10", "kācu", "metrology", "prakrit_sanskrit_loan", "LOAN<Skt.karṣa", "kācu", "gold coin/weight (< Skt. karṣa / Pkt. kāsa)", "Sangam / Chola inscriptions (DEDR 1431 notes IA contact)"),
    ("LOAN11", "paṇam", "metrology", "prakrit_sanskrit_loan", "LOAN<Skt.paṇa", "paṇam", "coin, weight/money (< Skt./Pkt. paṇa)", "Tamil Lexicon; Early historic coinage"),
    ("LOAN12", "palam", "metrology", "prakrit_sanskrit_loan", "LOAN<Skt.pala", "palam", "weight unit (~35-48 g, < Skt. pala)", "DEDR 3849; Chola inscriptions"),
    ("LOAN13", "kāṇam", "metrology", "prakrit_sanskrit_loan", "LOAN<Skt.kārṣāpaṇa", "kāṇam", "gold weight/coin (< Pkt. kahāpaṇa)", "Puṟanāṉūṟu; Tamil Lexicon"),
    ("LOAN14", "kaṇi", "admin_title", "prakrit_sanskrit_loan", "LOAN<Skt.gaṇin", "kaṇi", "senior Jain preceptor/astronomer (< Pkt. gaṇin)", "Tamil-Brahmi Mangulam 1 (kaṇi nanta, Mahadevan 2003)"),
    ("LOAN15", "catiyaputo", "admin_title", "prakrit_sanskrit_loan", "LOAN<Pkt.satiyaputo", "catiyaputo", "Satiyaputa royal title (< Ashokan Pkt.)", "Tamil-Brahmi Jambai 1 (Mahadevan 2003)"),
]

# =============================================================================
# PART 2: Matched Equal-Size Rival Epigraphic Controls (86 IA + 86 Ur III = 172)
# Exact size match to the 86 pure-Dravidian Sangam/Tamil-Brahmi entries!
# =============================================================================
RIVAL_IA_ENTRIES = [
    # Administrative / Guild / Clan titles (35)
    ("IA01", "śreṣṭhin", "seṭṭhi", "admin_title", "guild head, chief merchant/banker", "Bharhut/Sanchi Brahmi (setthisa); Arthaśāstra"),
    ("IA02", "sārthavāha", "satthavāha", "maritime_trade", "caravan leader, merchant chief", "Sanchi/Mathura Brahmi; Arthaśāstra"),
    ("IA03", "gṛhapati", "gahapati", "house_clan", "householder, landed estate head", "Sanchi/Bharhut/Amaravati Brahmi (gahapatino)"),
    ("IA04", "grāmaṇī", "gāmaṇī", "admin_title", "village headman, chief", "Vedic/Ashokan/Early Brahmi"),
    ("IA05", "rājan", "rājā", "admin_title", "king, ruler", "Ashokan/Bharhut/Sanchi Brahmi"),
    ("IA06", "kumāra", "kumāra", "admin_title", "prince, royal governor", "Ashokan edicts; Arthaśāstra"),
    ("IA07", "dāsa", "dāsa", "admin_title", "servant, slave, retainer", "Sanchi/Bharhut Brahmi; Arthaśāstra"),
    ("IA08", "bhāṇḍāgāra", "bhaṇḍāgāra", "admin_title", "treasury, royal storehouse", "Arthaśāstra; Sohgaura/Early Brahmi"),
    ("IA09", "nigama", "nigama", "admin_title", "merchant guild, market town", "Bhattiprolu/Sanchi/Bharhut Brahmi"),
    ("IA10", "vaṇij", "vaṇija", "maritime_trade", "merchant, trader", "Sanchi/Bharhut Brahmi (vanijasa); Arthaśāstra"),
    ("IA11", "nāvika", "nāvika", "maritime_trade", "sailor, ship-captain, helmsman", "Arthaśāstra; Bharhut/Sanchi"),
    ("IA12", "amātya", "amacca", "admin_title", "minister, high royal counselor", "Arthaśāstra; Early Brahmi"),
    ("IA13", "mahāmātra", "mahāmāta", "admin_title", "high state officer, overseer", "Ashokan edicts (Dhauli/Girnar/Sanchi)"),
    ("IA14", "rājuka", "lajuka", "admin_title", "district revenue/judicial officer", "Ashokan Pillar Edict IV"),
    ("IA15", "lekhaka", "lekhaka", "admin_title", "scribe, clerk, accountant", "Sanchi Brahmi (lekhakasa); Arthaśāstra"),
    ("IA16", "kulaputra", "kulaputta", "house_clan", "man of noble family/house", "Early Buddhist/Brahmi epigraphy"),
    ("IA17", "śilpin", "sippi", "admin_title", "artisan, craftsman", "Arthaśāstra; Early Brahmi"),
    ("IA18", "kārmāra", "kammāra", "admin_title", "smith, metalworker", "Vedic/Early Brahmi (kamarasa)"),
    ("IA19", "kulika", "kulika", "house_clan", "guild alderman, head of family/craft", "Early Historic seals (Basarh/Vaishali)"),
    ("IA20", "kāyastha", "kāyastha", "admin_title", "scribe, revenue writer", "Early Historic epigraphy"),
    ("IA21", "śreṇī", "seṇi", "admin_title", "artisan/trade guild, corporation", "Arthaśāstra; Nasik/Junar Brahmi"),
    ("IA22", "pūga", "pūga", "admin_title", "mercantile association, guild", "Arthaśāstra; Pāṇini"),
    ("IA23", "gaṇa", "gaṇa", "admin_title", "corporate assembly, troop, guild", "Vedic/Early Brahmi"),
    ("IA24", "adhyakṣa", "ajjhakkha", "admin_title", "superintendent, department director", "Arthaśāstra Book II"),
    ("IA25", "samāhartṛ", "samāhatta", "admin_title", "collector-general of revenue", "Arthaśāstra Book II"),
    ("IA26", "sannidhātṛ", "sannidhāta", "admin_title", "director of stores/treasury", "Arthaśāstra Book II"),
    ("IA27", "paṇyādhyakṣa", "paṇyādhyakṣa", "admin_title", "superintendent of trade/commodities", "Arthaśāstra Book II.16"),
    ("IA28", "nāvadhyakṣa", "nāvadhyakṣa", "maritime_trade", "superintendent of shipping/ports", "Arthaśāstra Book II.28"),
    ("IA29", "pautavādhyakṣa", "pautavādhyakṣa", "metrology", "superintendent of weights & measures", "Arthaśāstra Book II.19"),
    ("IA30", "śulka", "sukka", "admin_title", "customs duty, toll, port tax", "Arthaśāstra Book II.21"),
    ("IA31", "bhāga", "bhāga", "admin_title", "king's grain share, tax-fraction", "Ashokan Lumbini (aṭhabhāgiye); Arthaśāstra"),
    ("IA32", "bali", "bali", "admin_title", "tribute, land-tax", "Ashokan Lumbini (ubalike); Vedic"),
    ("IA33", "kara", "kara", "admin_title", "tax, periodic assessment", "Arthaśāstra; Early Brahmi"),
    ("IA34", "kula", "kula", "house_clan", "family, clan, household", "Sanchi/Bharhut Brahmi; Arthaśāstra"),
    ("IA35", "gotra", "gotta", "house_clan", "patrilineal clan, lineage", "Sanchi/Bharhut Brahmi (Gotiputasa)"),
    # Astral & Calendar (10)
    ("IA36", "nakṣatra", "nakkhatta", "astral_calendar", "lunar mansion, asterism", "Vedic/Vedāṅga Jyotiṣa"),
    ("IA37", "kṛttikā", "kattikā", "astral_calendar", "Pleiades (first Vedic nakṣatra)", "Taittirīya Saṃhitā / Atharvaveda"),
    ("IA38", "mṛgaśīrṣa", "migasira", "astral_calendar", "5th nakṣatra (Orion)", "Vedic / Jyotiṣa"),
    ("IA39", "saptarṣi", "sattarisi", "astral_calendar", "Ursa Major (Seven Sages)", "Śatapatha Brāhmaṇa"),
    ("IA40", "rohiṇī", "rohiṇī", "astral_calendar", "Aldebaran (red star nakṣatra)", "Vedic / Jyotiṣa"),
    ("IA41", "tārā", "tārā", "astral_calendar", "star", "Vedic / Sanskrit"),
    ("IA42", "ketu", "ketu", "astral_calendar", "comet, banner-star", "Vedic / Jyotiṣa"),
    ("IA43", "māsa", "māsa", "astral_calendar", "lunar month", "Ashokan edicts; Vedic"),
    ("IA44", "trimāsa", "temāsa", "astral_calendar", "three-month season", "Sanskrit/Pali"),
    ("IA45", "cāturmāsya", "cātummāsa", "astral_calendar", "four-month period", "Vedic/Ashokan edicts"),
    # Maritime, Trade & Commodities (23)
    ("IA46", "nau", "nāvā", "maritime_trade", "ship, boat", "Rigveda; Arthaśāstra"),
    ("IA47", "pota", "pota", "maritime_trade", "vessel, ship", "Arthaśāstra; Pali Jātakas"),
    ("IA48", "plava", "plava", "maritime_trade", "raft, boat", "Vedic; Arthaśāstra"),
    ("IA49", "pattana", "paṭṭana", "maritime_trade", "port town, trade mart", "Arthaśāstra Book II.28"),
    ("IA50", "koṣṭhāgāra", "koṭṭhāgāra", "maritime_trade", "granary, royal grain depot", "Sohgaura copper-plate; Arthaśāstra Book II.15"),
    ("IA51", "bhāṇḍa", "bhaṇḍa", "commodity", "vessel, merchandise, goods", "Arthaśāstra; Early Brahmi"),
    ("IA52", "paṇya", "paṇiya", "commodity", "trade goods, wares", "Arthaśāstra Book II.16"),
    ("IA53", "vastra", "vattha", "commodity", "woven cloth, garment", "Vedic; Arthaśāstra"),
    ("IA54", "tāmra", "tamba", "commodity", "copper", "Arthaśāstra; Early Brahmi"),
    ("IA55", "kāṃsya", "kaṃsa", "commodity", "bronze, bell-metal", "Arthaśāstra"),
    ("IA56", "loha", "loha", "commodity", "metal, copper/iron", "Vedic; Arthaśāstra"),
    ("IA57", "suvarṇa", "suvaṇṇa", "commodity", "gold; gold weight unit", "Arthaśāstra Book II.19"),
    ("IA58", "rajata", "rajata", "commodity", "silver", "Vedic; Arthaśāstra"),
    ("IA59", "śaṅkha", "saṅkha", "commodity", "conch shell", "Arthaśāstra"),
    ("IA60", "tila", "tila", "commodity", "sesame seed", "Atharvaveda; Arthaśāstra"),
    ("IA61", "vrīhi", "vīhi", "commodity", "rice/paddy", "Atharvaveda; Arthaśāstra"),
    ("IA62", "yava", "yava", "commodity", "barley", "Rigveda; Arthaśāstra"),
    ("IA63", "mayūra", "mora", "commodity", "peacock", "Vedic; Ashokan Rock Edict I"),
    ("IA64", "karpāsa", "kappāsa", "commodity", "cotton", "Arthaśāstra Book II.23"),
    ("IA65", "sūtra", "sutta", "commodity", "spun thread, yarn", "Arthaśāstra Book II.23"),
    ("IA66", "danta", "danta", "commodity", "ivory tusk", "Sanchi Brahmi (dantakārehi); Arthaśāstra"),
    ("IA67", "lavaṇa", "loṇa", "commodity", "salt", "Arthaśāstra Book II.12"),
    ("IA68", "maṇi", "maṇi", "commodity", "bead, gem", "Vedic; Sanchi Brahmi"),
    # Metrology & Fractions (18 — Arthaśāstra Book II Ch. 19)
    ("IA69", "kuḍava", "kuḍuba", "metrology", "small capacity measure (1/4 prastha)", "Arthaśāstra II.19 (kuḍumba)"),
    ("IA70", "prastha", "pattha", "metrology", "capacity measure (= 4 kuḍavas = 1/4 āḍhaka)", "Arthaśāstra II.19"),
    ("IA71", "āḍhaka", "āḷhaka", "metrology", "capacity measure (= 4 prasthas = 1/4 droṇa)", "Arthaśāstra II.19"),
    ("IA72", "droṇa", "doṇa", "metrology", "standard grain measure (= 4 āḍhakas = 200 palas)", "Arthaśāstra II.19; Pāṇini"),
    ("IA73", "vārī", "vārī", "metrology", "large grain measure (= 16 droṇas)", "Arthaśāstra II.19"),
    ("IA74", "kumbha", "kumbha", "metrology", "large grain measure (= 20 droṇas); jar", "Arthaśāstra II.19"),
    ("IA75", "vaha", "vaha", "metrology", "cartload measure (= 10 kumbhas = 200 droṇas)", "Arthaśāstra II.19"),
    ("IA76", "khārī", "khārī", "metrology", "wholesale grain measure (= 16 droṇas)", "Pāṇini; Arthaśāstra"),
    ("IA77", "māṣa", "māsa", "metrology", "small weight unit (5/10 guñjā)", "Arthaśāstra II.19"),
    ("IA78", "karṣa", "kāsa", "metrology", "weight unit (= 16 māṣas = 1/4 pala)", "Arthaśāstra II.19"),
    ("IA79", "kārṣāpaṇa", "kahāpaṇa", "metrology", "standard silver punch-marked coin", "Arthaśāstra; Early Brahmi"),
    ("IA80", "pala", "pala", "metrology", "weight unit (= 4 karṣas ~38-48 g)", "Arthaśāstra II.19"),
    ("IA81", "tulā", "tulā", "metrology", "weight unit (= 100 palas); balance", "Arthaśāstra II.19"),
    ("IA82", "bhāra", "bhāra", "metrology", "heavy load weight (= 20 tulās = 2000 palas)", "Arthaśāstra II.19"),
    ("IA83", "pāda", "pāda", "metrology", "quarter fraction (1/4); foot", "Vedic; Arthaśāstra"),
    ("IA84", "ardha", "addha", "metrology", "half fraction (1/2)", "Vedic; Arthaśāstra"),
    ("IA85", "tripāda", "tipāda", "metrology", "three-quarters (3/4)", "Sanskrit/Prakrit"),
    ("IA86", "dvādaśa", "dvādasa", "metrology", "twelve (12)", "Vedic/Ashokan Brahmi"),
]

RIVAL_SUM_ENTRIES = [
    # Administrative / Guild / Household titles (35 — verified from Halloran & local CDLI ATF)
    ("SUM01", "lugal", "lugal", "admin_title", "king, master, owner", "CDLI Ur III / Halloran"),
    ("SUM02", "ensi2", "ensi", "admin_title", "city-governor, ruler", "CDLI Ur III / Halloran"),
    ("SUM03", "szagina", "sagina", "admin_title", "military governor, general", "CDLI Ur III / Halloran"),
    ("SUM04", "dub-sar", "dubsar", "admin_title", "scribe, accountant (tablet-writer)", "CDLI Ur III seals (P137152, P140868, P116503)"),
    ("SUM05", "ugula", "ugula", "admin_title", "overseer, foreman, captain", "CDLI Ur III / Halloran"),
    ("SUM06", "nu-banda3", "nubanda", "admin_title", "inspector, lieutenant, overseer", "CDLI Ur III / Halloran"),
    ("SUM07", "dam-gar3", "damgar", "maritime_trade", "merchant, commercial agent", "CDLI Ur III Meluhha/Dilmun texts / Halloran"),
    ("SUM08", "ma2-lah5", "malah", "maritime_trade", "sailor, ship-captain, boatman", "CDLI Ur III / Halloran"),
    ("SUM09", "arad2", "arad", "admin_title", "servant, slave, subordinate", "CDLI Ur III seals (P137152 ARAD2-zu)"),
    ("SUM10", "geme2", "geme", "admin_title", "female worker, servant", "CDLI Ur III / Halloran"),
    ("SUM11", "dumu", "dumu", "house_clan", "son, child, citizen of", "CDLI Ur III seals (21/22 local seals)"),
    ("SUM12", "e2-gal", "egal", "house_clan", "palace (great house)", "CDLI Ur III / Halloran"),
    ("SUM13", "e2-kiszib3-ba", "ekisiba", "admin_title", "sealed storehouse, depot", "CDLI Ur III / Halloran"),
    ("SUM14", "gudu4", "gudu", "admin_title", "anointed temple priest", "CDLI Ur III seal P374962"),
    ("SUM15", "sanga", "sanga", "admin_title", "chief temple administrator", "CDLI Ur III / Halloran"),
    ("SUM16", "szabra", "sabra", "admin_title", "chief household steward/manager", "CDLI Ur III seals P137152, P340176"),
    ("SUM17", "sza13-dub-ba", "saduba", "admin_title", "chief archivist/comptroller", "CDLI Ur III seal P140868"),
    ("SUM18", "kuruszda", "kurusda", "admin_title", "livestock fattener/official", "CDLI Ur III seal P464911"),
    ("SUM19", "szusz3", "sus", "admin_title", "cattle administrator", "CDLI Ur III seal P507131"),
    ("SUM20", "aga3-us2", "agaus", "admin_title", "soldier, gendarme, guard", "CDLI Ur III / Halloran"),
    ("SUM21", "lu2-kin-gi4-a", "lukingia", "admin_title", "messenger, royal envoy", "CDLI Ur III / Halloran"),
    ("SUM22", "sukkal", "sukkal", "admin_title", "chancellor, minister, envoy", "CDLI Ur III / Halloran"),
    ("SUM23", "sukkal-mah", "sukkalmah", "admin_title", "grand vizier", "CDLI Ur III / Halloran"),
    ("SUM24", "simug", "simug", "admin_title", "smith, metalworker", "CDLI Ur III / Halloran"),
    ("SUM25", "nagar", "nagar", "admin_title", "carpenter, shipwright", "CDLI Ur III / Halloran"),
    ("SUM26", "usz-bar", "usbar", "admin_title", "weaver, textile worker", "CDLI Ur III / Halloran"),
    ("SUM27", "bahar2", "bahar", "admin_title", "potter", "CDLI Ur III / Halloran"),
    ("SUM28", "zadim", "zadim", "admin_title", "lapidary, bead/stone cutter", "CDLI Ur III / Halloran"),
    ("SUM29", "ku3-dim2", "kudim", "admin_title", "goldsmith, silversmith", "CDLI Ur III / Halloran"),
    ("SUM30", "szu-ku6", "suku", "admin_title", "fisherman", "CDLI Ur III / Halloran"),
    ("SUM31", "engar", "engar", "admin_title", "plowman, farm manager", "CDLI Ur III / Halloran"),
    ("SUM32", "sipa", "sipa", "admin_title", "shepherd, herdsman", "CDLI Ur III / Halloran"),
    ("SUM33", "na-gada", "nagada", "admin_title", "head herdsman", "CDLI Ur III / Halloran"),
    ("SUM34", "lu2", "lu", "admin_title", "man, person, official of", "CDLI Ur III / Halloran"),
    ("SUM35", "e2", "e", "house_clan", "house, temple, household estate", "CDLI Ur III / Halloran"),
    # Astral & Calendar (10)
    ("SUM36", "mul", "mul", "astral_calendar", "star, constellation", "Halloran / Sumerian"),
    ("SUM37", "mul-mul", "mulmul", "astral_calendar", "Pleiades (star-cluster)", "Sumerian/Mesopotamian astronomy"),
    ("SUM38", "iti", "iti", "astral_calendar", "month, moonlight", "CDLI Ur III / Halloran"),
    ("SUM39", "mu", "mu", "astral_calendar", "year, name", "CDLI Ur III / Halloran"),
    ("SUM40", "ud", "ud", "astral_calendar", "day, sun", "CDLI Ur III / Halloran"),
    ("SUM41", "an", "an", "astral_calendar", "sky, heaven", "Halloran / Sumerian"),
    ("SUM42", "nanna", "nanna", "astral_calendar", "moon-god", "CDLI Ur III"),
    ("SUM43", "utu", "utu", "astral_calendar", "sun-god", "CDLI Ur III"),
    ("SUM44", "iti-esz", "ities", "astral_calendar", "three months", "Ur III administrative"),
    ("SUM45", "ud-sakar", "udsakar", "astral_calendar", "crescent moon, new-moon day", "CDLI Ur III / Halloran"),
    # Maritime, Trade & Commodities (23)
    ("SUM46", "ma2", "ma", "maritime_trade", "ship, boat, barge", "CDLI Ur III / Halloran"),
    ("SUM47", "ma2-gur8", "magur", "maritime_trade", "deep-draft cargo ship (Meluhha/Magan ship)", "CDLI Ur III Meluhha texts"),
    ("SUM48", "ma2-da-ga", "madaga", "maritime_trade", "cargo vessel", "CDLI Ur III"),
    ("SUM49", "kar", "kar", "maritime_trade", "quay, harbor, trading station", "CDLI Ur III / Halloran"),
    ("SUM50", "uru", "uru", "house_clan", "city, town", "CDLI Ur III / Halloran"),
    ("SUM51", "kalam", "kalam", "house_clan", "homeland, Sumer", "Halloran / Sumerian"),
    ("SUM52", "ma-da", "mada", "house_clan", "province, foreign land", "CDLI Ur III / Halloran"),
    ("SUM53", "sze", "se", "commodity", "barley, grain", "CDLI Ur III / Halloran"),
    ("SUM54", "ziz2", "ziz", "commodity", "emmer wheat", "CDLI Ur III / Halloran"),
    ("SUM55", "gig", "gig", "commodity", "wheat", "CDLI Ur III / Halloran"),
    ("SUM56", "i3-gesz", "iges", "commodity", "sesame oil", "CDLI Ur III Meluhha texts"),
    ("SUM57", "tug2", "tug", "commodity", "textile, garment, cloth", "CDLI Ur III / Halloran"),
    ("SUM58", "siki", "siki", "commodity", "wool, fleece", "CDLI Ur III / Halloran"),
    ("SUM59", "uruda", "uruda", "commodity", "copper", "CDLI Ur III Magan/Meluhha texts"),
    ("SUM60", "zabar", "zabar", "commodity", "bronze", "CDLI Ur III / Halloran"),
    ("SUM61", "ku3-babbar", "kubabbar", "commodity", "silver", "CDLI Ur III / Halloran"),
    ("SUM62", "ku3-sig17", "kusig", "commodity", "gold", "CDLI Ur III / Halloran"),
    ("SUM63", "an-na", "anna", "commodity", "tin", "CDLI Ur III / Halloran"),
    ("SUM64", "gug", "gug", "commodity", "carnelian (Meluhha trade good)", "CDLI Ur III / Halloran"),
    ("SUM65", "za-gin3", "zagin", "commodity", "lapis lazuli", "CDLI Ur III / Halloran"),
    ("SUM66", "zu2-am-si", "zuamsi", "commodity", "elephant ivory tusk", "CDLI Ur III / Halloran"),
    ("SUM67", "ku6", "ku", "commodity", "fish", "CDLI Ur III / Halloran"),
    ("SUM68", "gesz", "ges", "commodity", "wood, timber", "CDLI Ur III / Halloran"),
    # Metrology & Fractions (18 — Ur III Sexagesimal System)
    ("SUM69", "sila3", "sila", "metrology", "standard capacity measure (~1.0 L)", "CDLI Ur III (3,319+ local attestations)"),
    ("SUM70", "ban2", "ban", "metrology", "capacity measure (= 10 sila3 ~10 L)", "CDLI Ur III / Halloran"),
    ("SUM71", "barig", "barig", "metrology", "capacity measure (= 6 ban2 = 60 sila3 ~60 L)", "CDLI Ur III / Halloran"),
    ("SUM72", "gur", "gur", "metrology", "wholesale grain measure (= 5 barig = 300 sila3 ~300 L)", "CDLI Ur III / Halloran"),
    ("SUM73", "gin2", "gin", "metrology", "shekel weight (~8.33 g = 1/60 ma-na)", "CDLI Ur III / Halloran"),
    ("SUM74", "ma-na", "mana", "metrology", "mina weight (= 60 gin2 ~500 g)", "CDLI Ur III / Halloran"),
    ("SUM75", "gu2", "gu", "metrology", "talent weight (= 60 ma-na ~30 kg)", "CDLI Ur III / Halloran"),
    ("SUM76", "sze-ba", "seba", "metrology", "barley ration allowance", "CDLI Ur III / Halloran"),
    ("SUM77", "sar", "sar", "metrology", "garden-plot area (~36 m2)", "CDLI Ur III / Halloran"),
    ("SUM78", "iku", "iku", "metrology", "field area (= 100 sar)", "CDLI Ur III / Halloran"),
    ("SUM79", "esze3", "ese", "metrology", "field area (= 6 iku)", "CDLI Ur III / Halloran"),
    ("SUM80", "bur3", "bur", "metrology", "field area (= 3 esze3 = 18 iku)", "CDLI Ur III / Halloran"),
    ("SUM81", "igi-4-gal2", "igigal", "metrology", "one-quarter fraction (1/4)", "CDLI Ur III / Halloran"),
    ("SUM82", "szu-ri-a", "suria", "metrology", "one-half fraction (1/2)", "CDLI Ur III / Halloran"),
    ("SUM83", "igi-3-gal2", "igigal", "metrology", "one-third fraction (1/3)", "CDLI Ur III / Halloran"),
    ("SUM84", "igi-6-gal2", "igigal", "metrology", "one-sixth fraction (1/6)", "CDLI Ur III / Halloran"),
    ("SUM85", "kingusila", "kingusila", "metrology", "five-sixths fraction (5/6)", "Halloran / Sumerian"),
    ("SUM86", "u-min", "umin", "metrology", "twelve (12)", "Sumerian"),
]


# =============================================================================
# The 19 Sound-Locked Indus Signs + Basic Numerals (from Key #2A + Key #3A)
# =============================================================================
L19_DRAV = {
    "220": ["min"],          # *mīṉ / *miṉ (star/fish, DEDR 4885/4876)
    "820": ["kal"],          # *kāl (quarter/wheel, DEDR 1479)
    "320": ["pati"],         # *paṭi (ration/step, DEDR 3849/3850)
    "090": ["al"],           # *āḷ (manager/man, DEDR 399)
    "154": ["ka"],           # *kā (guard/pole, DEDR 1416)
    "740": ["kuti"],         # *kuṭi (house/pot, DEDR 1655)
    "400": ["cikka"],        # *cikka (junior/comb, DEDR 2495)
    "705": ["kalam"],        # *kalam / *kaḷam (kalam/ship/floor, DEDR 1305/1376)
    "520": ["vel"],          # *vēḷ (chief/spear, DEDR 5545)
    "850": ["kan"],          # *kaṉ / *kaṇ (copper/eye, DEDR 1402/1159)
    "390": ["tai"],          # *tai (weave/tree, DEDR 3473)
    "717": ["ati"],          # *aṭi (foot/servant, DEDR 72)
    "061": ["kal"],          # *kāl (leg/quarter, DEDR 1479)
    "235": ["olimin", "oli"],  # *oḷi-mīṉ (bright-star)
    "500": ["pay"],          # *pāy (sail/mat, DEDR 4088)
    "100": ["talai"],        # *talai (head/chief, DEDR 3103)
    "176": ["irai"],         # *iṟai (tax/lord, DEDR 521/527)
    "900": ["tinkal"],       # *tiṅkaḷ (moon/month, DEDR 3213)
    "923": ["maruppu"],      # *maruppu (horn/tusk, DEDR 4720)
}
NUMS_DRAV = {
    "001": ["oru"], "031": ["oru"],
    "002": ["iru"], "032": ["iru"],
    "003": ["mu"],  "033": ["mu"],
    "004": ["nal"], "034": ["nal"],
    "005": ["ai"],  "015": ["ai"], "035": ["ai"],
    "006": ["aru"], "016": ["aru"],
    "007": ["elu"], "017": ["elu"],
    "055": ["panniru"],
}

# Semantic-equivalent 19-sign mappings for Matched Rival Epigraphy Controls:
# Each Indus sign's iconic/functional meaning mapped to its standard IA & Sumerian lexical stems.
L19_IA = {
    "220": ["matsya", "tara"],
    "820": ["pada", "cakra"],
    "320": ["prastha", "pada"],
    "090": ["nara", "pati"],
    "154": ["pala", "raksa"],
    "740": ["grha", "kula", "kumbha"],
    "400": ["laghu", "bala"],
    "705": ["drona", "nau"],
    "520": ["rajan", "sresthin"],
    "850": ["tamra", "aksi"],
    "390": ["sutra", "vastra"],
    "717": ["dasa", "pada"],
    "061": ["pada"],
    "235": ["tara", "naksatra"],
    "500": ["pota", "kata"],
    "100": ["siras", "agra"],
    "176": ["kara", "bhaga"],
    "900": ["masa", "candra"],
    "923": ["danta", "srnga"],
}
NUMS_IA = {
    "001": ["eka"], "031": ["eka"],
    "002": ["dvi"], "032": ["dvi"],
    "003": ["tri"], "033": ["tri"],
    "004": ["catur"], "034": ["catur"],
    "005": ["panca"], "015": ["panca"], "035": ["panca"],
    "006": ["sat"], "016": ["sat"],
    "007": ["sapta"], "017": ["sapta"],
    "055": ["dvadasa"],
}

L19_SUM = {
    "220": ["ku", "mul"],
    "820": ["igigal", "giri"],
    "320": ["sila", "seba"],
    "090": ["lu", "ugula"],
    "154": ["ennu", "agaus"],
    "740": ["e", "dug"],
    "400": ["tur", "dumu"],
    "705": ["gur", "ma"],
    "520": ["lugal", "ensi"],
    "850": ["uruda", "igi"],
    "390": ["tug", "usbar"],
    "717": ["arad", "giri"],
    "061": ["igigal"],
    "235": ["mul"],
    "500": ["magur", "kid"],
    "100": ["sag"],
    "176": ["gu", "mas"],
    "900": ["iti"],
    "923": ["zuamsi", "si"],
}
NUMS_SUM = {
    "001": ["dis"], "031": ["dis"],
    "002": ["min"], "032": ["min"],
    "003": ["es"],  "033": ["es"],
    "004": ["limmu"], "034": ["limmu"],
    "005": ["ia"],  "015": ["ia"], "035": ["ia"],
    "006": ["as"], "016": ["as"],
    "007": ["imin"], "017": ["imin"],
    "055": ["umin"],
}


def extract_true_order_ngrams(json_path: str, allowed_signs: set, num_signs: set):
    """Extract true reading-order adjacent bigrams (distinct text counts) from faces."""
    with open(json_path) as f:
        recs = json.load(f)
    bg = Counter()
    tg = Counter()
    for r in recs:
        s2, s3 = set(), set()
        for face in r.get("faces", []):
            for a, b in zip(face, face[1:]):
                if a in allowed_signs and b in allowed_signs and not (a in num_signs and b in num_signs):
                    s2.add((a, b))
            for a, b, c in zip(face, face[1:], face[2:]):
                if a in allowed_signs and b in allowed_signs and c in allowed_signs:
                    if not (a in num_signs and b in num_signs and c in num_signs):
                        s3.add((a, b, c))
        for x in s2:
            bg[x] += 1
        for x in s3:
            tg[x] += 1
    return bg, tg, len(recs)


def match_bigrams_against_lexicon(bg_counts, sign_map, num_map, lex_ascii_map, lex_phon_map, join_fn):
    """
    Match observed bigrams (a, b) with count >= 1 against target lexicon.
    Returns list of match dicts and summary counts.
    Strict rule: requires exact ascii sandhi match OR exact phon match where len >= 5 (prevents short 3-4 letter noise).
    Also forbids trivial self-matches where a single root already equals the target word without contributing the other sign.
    """
    hits = []
    for (a, b), cnt in bg_counts.items():
        roots_a = sign_map.get(a) or num_map.get(a) or []
        roots_b = sign_map.get(b) or num_map.get(b) or []
        matched_entry = None
        matched_surface = None
        for ra in roots_a:
            for rb in roots_b:
                raw_set, phon_set = join_fn(ra, rb)
                # Prefer exact ASCII sandhi match first
                for surf in sorted(raw_set):
                    if surf in lex_ascii_map and surf != strip_diacritics(ra) and surf != strip_diacritics(rb):
                        matched_entry = lex_ascii_map[surf]
                        matched_surface = surf
                        break
                if matched_entry:
                    break
                # Fallback to normalized phonological match only for compounds >= 5 chars
                for ph in sorted(phon_set):
                    if len(ph) >= 5 and ph in lex_phon_map and ph != norm_phon(ra) and ph != norm_phon(rb):
                        matched_entry = lex_phon_map[ph]
                        matched_surface = ph
                        break
                if matched_entry:
                    break
            if matched_entry:
                break
        if matched_entry:
            hits.append({
                "pair": f"{a}-{b}",
                "a": a,
                "b": b,
                "roots": f"{roots_a[0]}+{roots_b[0]}",
                "surface": matched_surface,
                "entry": matched_entry,
                "count": cnt,
            })
    return hits


def run_test_4c1(ta_dedr_ascii, ta_dedr_phon, all_2branch_roots):
    print("\n================ TEST 4C-1: COMPOUND-EXPANSION UNLOCK (5,000 SHUFFLES) ================")
    all_keys = set(L19_DRAV) | set(NUMS_DRAV)
    num_keys = set(NUMS_DRAV)

    bg_lipi, tg_lipi, n_lipi = extract_true_order_ngrams(f"{BASE}/work_data/sem/events_lipi.json", all_keys, num_keys)
    bg_new, tg_new, n_new = extract_true_order_ngrams(f"{BASE}/work_data/sem/events_new.json", all_keys, num_keys)

    # Filter recurring Lipi bigrams (n >= 2) and all Lipi bigrams (n >= 1)
    bg_lipi_rec = {k: v for k, v in bg_lipi.items() if v >= 2}

    # Build pure-Dravidian Sangam/Tamil-Brahmi lookup maps (STRICTLY excluding Prakrit loans!)
    pure_entries = [e for e in SANGAM_EPIGRAPHY_ENTRIES if e[3] == "pure_dravidian"]
    loan_entries = [e for e in SANGAM_EPIGRAPHY_ENTRIES if e[3] == "prakrit_sanskrit_loan"]

    sangam_ascii = {}
    sangam_phon = {}
    for e in pure_entries:
        asc = strip_diacritics(e[1])
        ph = norm_phon(e[1])
        # Only multi-morpheme / compound-length words (>= 4 chars) can be compound targets
        if len(asc) >= 4:
            sangam_ascii[asc] = e
            if len(ph) >= 5 and ph not in sangam_phon:
                sangam_phon[ph] = e

    # Pure-DEDR map (from dedr_entries.tsv Tamil headwords only)
    dedr_ascii_map = {w: ("DEDR", w) for w in ta_dedr_ascii if len(w) >= 4}
    dedr_phon_map = {w: ("DEDR", w) for w in ta_dedr_phon if len(w) >= 5}

    # Combined DEDR + Pure-Dravidian Sangam
    comb_ascii = dict(dedr_ascii_map)
    comb_ascii.update(sangam_ascii)
    comb_phon = dict(dedr_phon_map)
    comb_phon.update(sangam_phon)

    # 1. Observed matches on recurring Lipi bigrams (n >= 2)
    hits_dedr_rec = match_bigrams_against_lexicon(bg_lipi_rec, L19_DRAV, NUMS_DRAV, dedr_ascii_map, dedr_phon_map, dravidian_sandhi_joins)
    hits_sangam_rec = match_bigrams_against_lexicon(bg_lipi_rec, L19_DRAV, NUMS_DRAV, sangam_ascii, sangam_phon, dravidian_sandhi_joins)
    hits_comb_rec = match_bigrams_against_lexicon(bg_lipi_rec, L19_DRAV, NUMS_DRAV, comb_ascii, comb_phon, dravidian_sandhi_joins)

    # Also check ALL Lipi bigrams (n >= 1) and unseen New bigrams (n >= 1)
    hits_sangam_all = match_bigrams_against_lexicon(bg_lipi, L19_DRAV, NUMS_DRAV, sangam_ascii, sangam_phon, dravidian_sandhi_joins)
    hits_sangam_new = match_bigrams_against_lexicon(bg_new, L19_DRAV, NUMS_DRAV, sangam_ascii, sangam_phon, dravidian_sandhi_joins)

    # Also check Prakrit loan contamination (should be 0!)
    loan_ascii = {strip_diacritics(e[1]): e for e in loan_entries if len(strip_diacritics(e[1])) >= 4}
    loan_phon = {norm_phon(e[1]): e for e in loan_entries if len(norm_phon(e[1])) >= 5}
    hits_loan_rec = match_bigrams_against_lexicon(bg_lipi_rec, L19_DRAV, NUMS_DRAV, loan_ascii, loan_phon, dravidian_sandhi_joins)

    # Deduplicate by target Sangam compound (e.g., 003-220 and 033-220 both read mummīṉ)
    def summarize_hits(hits, unseen_counts):
        by_word = defaultdict(list)
        for h in hits:
            w = h["entry"][1]
            by_word[w].append(h)
        n_pairs = len(hits)
        n_words = len(by_word)
        lipi_mass = sum(h["count"] for h in hits)
        new_mass = sum(unseen_counts.get((h["a"], h["b"]), 0) for h in hits)
        n_words_replicated = sum(
            1 for w, hs in by_word.items() if sum(unseen_counts.get((h["a"], h["b"]), 0) for h in hs) > 0
        )
        return n_pairs, n_words, lipi_mass, new_mass, n_words_replicated, by_word

    s_pairs, s_words, s_lmass, s_nmass, s_wrep, s_byw = summarize_hits(hits_sangam_rec, bg_new)
    d_pairs, d_words, d_lmass, d_nmass, d_wrep, d_byw = summarize_hits(hits_dedr_rec, bg_new)
    all_pairs, all_words, all_lmass, all_nmass, all_wrep, all_byw = summarize_hits(hits_sangam_all, bg_new)

    # Which Sangam compounds were MISSED by raw DEDR headwords?
    newly_unlocked = [w for w in s_byw if strip_diacritics(w) not in ta_dedr_ascii]
    newly_unlocked_all = [w for w in all_byw if strip_diacritics(w) not in ta_dedr_ascii]

    print(f"Observed recurring L19/NUM bigrams (Lipi>=2): {len(bg_lipi_rec)} pairs (total Lipi>=1: {len(bg_lipi)})")
    print(f"  Raw DEDR alone (Lipi>=2):     {d_pairs} pairs / {d_words} distinct forms / Lipi mass={d_lmass} / New mass={d_nmass}")
    print(f"  Pure-Drav Sangam (Lipi>=2):   {s_pairs} pairs / {s_words} distinct compounds / Lipi mass={s_lmass} / New mass={s_nmass} ({s_wrep}/{s_words} compounds in unseen New!)")
    print(f"  Pure-Drav Sangam (Lipi>=1):   {all_pairs} pairs / {all_words} distinct compounds / Lipi mass={all_lmass} / New mass={all_nmass} ({all_wrep}/{all_words} in unseen New!)")
    print(f"  Newly unlocked beyond DEDR:   {len(newly_unlocked)}/{s_words} (Lipi>=2): {sorted(newly_unlocked)}")
    print(f"  Prakrit/Skt loan hits:        {len(hits_loan_rec)} (strictly 0 contamination check!)")

    for w, hs in sorted(all_byw.items(), key=lambda kv: -sum(h["count"] for h in kv[1])):
        in_d = strip_diacritics(w) in ta_dedr_ascii
        lm = sum(h["count"] for h in hs)
        nm = sum(bg_new.get((h["a"], h["b"]), 0) for h in hs)
        pairs_str = ", ".join(f"{h['pair']}({h['count']}/{bg_new.get((h['a'],h['b']),0)})" for h in hs)
        ent = hs[0]["entry"]
        print(f"    -> {w:12s} [{ent[2]:15s}] in_DEDR={str(in_d):5s} Lipi={lm:3d} New={nm:2d} | {pairs_str} | {ent[6]}")

    # --- Matched Rival Epigraphy Controls (IA & Ur III Sumerian) ---
    ia_ascii = {}
    ia_phon = {}
    for e in RIVAL_IA_ENTRIES:
        for col in (e[1], e[2]):
            asc = strip_diacritics(col)
            ph = norm_phon(col)
            if len(asc) >= 4:
                ia_ascii[asc] = e
            if len(ph) >= 5 and ph not in ia_phon:
                ia_phon[ph] = e

    sum_ascii = {}
    sum_phon = {}
    for e in RIVAL_SUM_ENTRIES:
        asc = strip_diacritics(re.sub(r"\d+", "", e[1]))
        ph = norm_phon(asc)
        if len(asc) >= 4:
            sum_ascii[asc] = e
        if len(ph) >= 5 and ph not in sum_phon:
            sum_phon[ph] = e

    hits_ia_rec = match_bigrams_against_lexicon(bg_lipi_rec, L19_IA, NUMS_IA, ia_ascii, ia_phon, ia_sandhi_joins)
    hits_sum_rec = match_bigrams_against_lexicon(bg_lipi_rec, L19_SUM, NUMS_SUM, sum_ascii, sum_phon, sumerian_joins)
    hits_ia_all = match_bigrams_against_lexicon(bg_lipi, L19_IA, NUMS_IA, ia_ascii, ia_phon, ia_sandhi_joins)
    hits_sum_all = match_bigrams_against_lexicon(bg_lipi, L19_SUM, NUMS_SUM, sum_ascii, sum_phon, sumerian_joins)

    ia_p, ia_w, ia_lm, ia_nm, ia_wr, _ = summarize_hits(hits_ia_rec, bg_new)
    su_p, su_w, su_lm, su_nm, su_wr, _ = summarize_hits(hits_sum_rec, bg_new)
    print(f"\nMatched Rival Controls (equal-size 86-term epigraphic lexicons, Lipi>=2):")
    print(f"  Early Indo-Aryan/Prakrit:     {ia_p} pairs / {ia_w} compounds / Lipi mass={ia_lm} / New mass={ia_nm}")
    for h in hits_ia_rec:
        print(f"    IA hit: {h['pair']} ({h['roots']}) -> {h['entry'][1]} ({h['entry'][4]}), Lipi={h['count']}")
    print(f"  Ur III Sumerian:              {su_p} pairs / {su_w} compounds / Lipi mass={su_lm} / New mass={su_nm}")
    for h in hits_sum_rec:
        print(f"    SUM hit: {h['pair']} ({h['roots']}) -> {h['entry'][1]} ({h['entry'][4]}), Lipi={h['count']}")

    # --- 5,000-SHUFFLE NULL CONTROLS (Fast Precomputed Pair-Match Matrix!) ---
    rng = np.random.default_rng(RNG_SEED)
    l19_signs = sorted(L19_DRAV.keys())
    l19_roots = [L19_DRAV[s] for s in l19_signs]
    n_s = len(l19_signs)

    # Precompute match lookup for any (root_list_a, root_list_b) -> matched sangam compound id (or None)
    pair_cache = {}

    def check_pair_roots(ra_list, rb_list):
        key = (tuple(ra_list), tuple(rb_list))
        if key in pair_cache:
            return pair_cache[key]
        res = None
        for ra in ra_list:
            for rb in rb_list:
                raw_set, phon_set = dravidian_sandhi_joins(ra, rb)
                for surf in raw_set:
                    if surf in sangam_ascii and surf != strip_diacritics(ra) and surf != strip_diacritics(rb):
                        res = sangam_ascii[surf][1]
                        break
                if res:
                    break
                for ph in phon_set:
                    if len(ph) >= 5 and ph in sangam_phon and ph != norm_phon(ra) and ph != norm_phon(rb):
                        res = sangam_phon[ph][1]
                        break
                if res:
                    break
            if res:
                break
        pair_cache[key] = res
        return res

    # Observed recurring pairs list for fast vector evaluation
    rec_items = list(bg_lipi_rec.items())
    rec_new_w = [bg_new.get(k, 0) for k, _ in rec_items]
    all_items = list(bg_lipi.items())
    all_new_w = [bg_new.get(k, 0) for k, _ in all_items]

    # (a) 5,000 Random Sound Permutations across the 19 Locked Signs (numerals fixed)
    perm_rec_words = np.zeros(N_SHUFFLES)
    perm_rec_pairs = np.zeros(N_SHUFFLES)
    perm_rec_lmass = np.zeros(N_SHUFFLES)
    perm_rec_nmass = np.zeros(N_SHUFFLES)
    perm_all_words = np.zeros(N_SHUFFLES)
    perm_all_lmass = np.zeros(N_SHUFFLES)

    for t in range(N_SHUFFLES):
        p_idx = rng.permutation(n_s)
        pmap = {l19_signs[i]: l19_roots[p_idx[i]] for i in range(n_s)}
        w_rec = set()
        pr = lm = nm = 0
        for idx, ((a, b), cnt) in enumerate(rec_items):
            ra = pmap.get(a) or NUMS_DRAV.get(a)
            rb = pmap.get(b) or NUMS_DRAV.get(b)
            m = check_pair_roots(ra, rb)
            if m:
                w_rec.add(m)
                pr += 1
                lm += cnt
                nm += rec_new_w[idx]
        perm_rec_words[t] = len(w_rec)
        perm_rec_pairs[t] = pr
        perm_rec_lmass[t] = lm
        perm_rec_nmass[t] = nm

        w_all = set()
        lm_a = 0
        for (a, b), cnt in all_items:
            ra = pmap.get(a) or NUMS_DRAV.get(a)
            rb = pmap.get(b) or NUMS_DRAV.get(b)
            m = check_pair_roots(ra, rb)
            if m:
                w_all.add(m)
                lm_a += cnt
        perm_all_words[t] = len(w_all)
        perm_all_lmass[t] = lm_a

    # (b) 5,000 Random Equal-Length Root Draws from Clean 2-Branch DEDR
    by_len = defaultdict(list)
    seen_r = set()
    for _, r_asc, r_len in all_2branch_roots:
        if r_asc not in seen_r:
            seen_r.add(r_asc)
            by_len[r_len].append(r_asc)
    # Build pool per sign length (fallback to +/-1 if sparse)
    sign_pools = []
    for s in l19_signs:
        L = len(L19_DRAV[s][0])
        pool = list(by_len.get(L, []))
        if len(pool) < 30:
            pool += by_len.get(L - 1, []) + by_len.get(L + 1, [])
        sign_pools.append(pool)

    draw_rec_words = np.zeros(N_SHUFFLES)
    draw_rec_pairs = np.zeros(N_SHUFFLES)
    draw_rec_lmass = np.zeros(N_SHUFFLES)
    draw_rec_nmass = np.zeros(N_SHUFFLES)
    draw_all_words = np.zeros(N_SHUFFLES)

    for t in range(N_SHUFFLES):
        dmap = {}
        for i, s in enumerate(l19_signs):
            pool = sign_pools[i]
            dmap[s] = [pool[int(rng.integers(0, len(pool)))]]
        w_rec = set()
        pr = lm = nm = 0
        for idx, ((a, b), cnt) in enumerate(rec_items):
            ra = dmap.get(a) or NUMS_DRAV.get(a)
            rb = dmap.get(b) or NUMS_DRAV.get(b)
            m = check_pair_roots(ra, rb)
            if m:
                w_rec.add(m)
                pr += 1
                lm += cnt
                nm += rec_new_w[idx]
        draw_rec_words[t] = len(w_rec)
        draw_rec_pairs[t] = pr
        draw_rec_lmass[t] = lm
        draw_rec_nmass[t] = nm

        w_all = set()
        for (a, b), cnt in all_items:
            ra = dmap.get(a) or NUMS_DRAV.get(a)
            rb = dmap.get(b) or NUMS_DRAV.get(b)
            m = check_pair_roots(ra, rb)
            if m:
                w_all.add(m)
        draw_all_words[t] = len(w_all)

    stats = {
        "n_shuffles": N_SHUFFLES,
        "lipi_recurring_l19_num_bigrams": len(bg_lipi_rec),
        "lipi_all_l19_num_bigrams": len(bg_lipi),
        "raw_dedr_rec": {"pairs": d_pairs, "words": d_words, "lipi_mass": d_lmass, "new_mass": d_nmass},
        "sangam_pure_rec": {
            "pairs": s_pairs,
            "words": s_words,
            "lipi_mass": s_lmass,
            "new_mass": s_nmass,
            "words_replicated_in_new": s_wrep,
            "newly_unlocked_beyond_dedr": sorted(newly_unlocked),
        },
        "sangam_pure_all": {
            "pairs": all_pairs,
            "words": all_words,
            "lipi_mass": all_lmass,
            "new_mass": all_nmass,
            "words_replicated_in_new": all_wrep,
            "newly_unlocked_beyond_dedr": sorted(newly_unlocked_all),
        },
        "prakrit_loan_hits_rec": len(hits_loan_rec),
        "rival_ia_rec": {"pairs": ia_p, "words": ia_w, "lipi_mass": ia_lm, "new_mass": ia_nm, "hits": [h["entry"][1] for h in hits_ia_rec]},
        "rival_sum_rec": {"pairs": su_p, "words": su_w, "lipi_mass": su_lm, "new_mass": su_nm, "hits": [h["entry"][1] for h in hits_sum_rec]},
        "null_perm19_rec_words": dict(zip(["mean", "std", "z", "p"], p_and_z(s_words, perm_rec_words))),
        "null_perm19_rec_pairs": dict(zip(["mean", "std", "z", "p"], p_and_z(s_pairs, perm_rec_pairs))),
        "null_perm19_rec_lipi_mass": dict(zip(["mean", "std", "z", "p"], p_and_z(s_lmass, perm_rec_lmass))),
        "null_perm19_rec_new_mass": dict(zip(["mean", "std", "z", "p"], p_and_z(s_nmass, perm_rec_nmass))),
        "null_perm19_all_words": dict(zip(["mean", "std", "z", "p"], p_and_z(all_words, perm_all_words))),
        "null_perm19_all_lipi_mass": dict(zip(["mean", "std", "z", "p"], p_and_z(all_lmass, perm_all_lmass))),
        "null_draw19_rec_words": dict(zip(["mean", "std", "z", "p"], p_and_z(s_words, draw_rec_words))),
        "null_draw19_rec_pairs": dict(zip(["mean", "std", "z", "p"], p_and_z(s_pairs, draw_rec_pairs))),
        "null_draw19_rec_lipi_mass": dict(zip(["mean", "std", "z", "p"], p_and_z(s_lmass, draw_rec_lmass))),
        "null_draw19_rec_new_mass": dict(zip(["mean", "std", "z", "p"], p_and_z(s_nmass, draw_rec_nmass))),
        "null_draw19_all_words": dict(zip(["mean", "std", "z", "p"], p_and_z(all_words, draw_all_words))),
    }

    print("\n--- 5,000-Shuffle Summary (Test 4C-1) ---")
    for k in [
        "null_perm19_rec_words", "null_perm19_rec_lipi_mass", "null_perm19_rec_new_mass",
        "null_perm19_all_words", "null_draw19_rec_words", "null_draw19_rec_lipi_mass",
        "null_draw19_rec_new_mass", "null_draw19_all_words"
    ]:
        st = stats[k]
        print(f"  {k:28s}: null_mean={st['mean']:.2f}±{st['std']:.2f}, z={st['z']:+.2f}, P={st['p']:.5f}")

    # Save compound match table
    with open(f"{OUT_DIR}/test4c1_compound_matches.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pair", "roots", "matched_compound", "category", "in_raw_dedr", "lipi_texts", "unseen_new_texts", "dedr_id", "gloss", "attestation_source"])
        for h in sorted(hits_sangam_all, key=lambda x: (-x["count"], x["pair"])):
            ent = h["entry"]
            in_d = strip_diacritics(ent[1]) in ta_dedr_ascii
            w.writerow([h["pair"], h["roots"], ent[1], ent[2], in_d, h["count"], bg_new.get((h["a"], h["b"]), 0), ent[4], ent[6], ent[7]])

    return stats


# =============================================================================
# PART 3: Test 4C-2 — Structural Formula Alignment (Indus FRAME v3 vs
#         Early Tamil-Brahmi vs Prakrit Brahmi vs Ur III Sumerian, 5,000 Shuffles)
# =============================================================================
# Verified attested inscriptions for Tamil-Brahmi (Mahadevan 2003 + Keeladi/Kodumanal/Red Sea)
# and Prakrit Brahmi (Bharhut/Sanchi/Ashokan); Ur III seals are extracted DIRECTLY from local CDLI ATF!
# Columns: (tradition, id, medium, text_translit, slot_sequence, header_init, mod_before_gen, owner_before_title, num_before_comm, meas_before_num, pot_short, citation)
# Note: None = axis not instantiated in that specific inscription.
ATTESTED_TB_INSCRIPTIONS = [
    # Cave inscriptions (Mahadevan 2003, Early Tamil Epigraphy)
    ("Tamil-Brahmi", "TB_MGL1", "cave", "kaṇi nanta āciriyika kuvaṉkē tammam itta neṭuñcaḻiyaṉ paṇaṉ kaṭalaṉ vaḻuti koṭṭupitta paḷi", "TITLE+PN+DAT | KING+SERVANT+PN+VERB+OBJ", 1, 1, 1, None, None, None, "Mangulam 1 (Mahadevan 2003 #1, c. 2nd c. BCE)"),
    ("Tamil-Brahmi", "TB_MGL2", "cave", "kaṇi nanta āciriyika kuvaṉkē neṭuñcaḻiyaṉ cālaṉ iḷañcaṭikaṉ tantai caṭikaṉ ceyiya paḷi", "TITLE+PN+DAT | KING+KIN+PN+VERB+OBJ", 1, 1, 1, None, None, None, "Mangulam 2 (Mahadevan 2003 #2)"),
    ("Tamil-Brahmi", "TB_MGL3", "cave", "veḷa-aṟai nikamattōr koṭiōr ... kāviti kāḻitika anta ai ceyta paḷi", "PLACE+GUILD+GEN | TITLE+PN+VERB+OBJ", 1, 1, 0, None, None, None, "Mangulam 3 (Mahadevan 2003 #3)"),
    ("Tamil-Brahmi", "TB_MGL6", "cave", "veḷa-aṟai nikamatu kāviti kāḻitika anta ai ceyta paḷi", "PLACE+GUILD+GEN+TITLE+PN", 1, 1, 0, None, None, None, "Mangulam 6 (Mahadevan 2003 #6)"),
    ("Tamil-Brahmi", "TB_JMB1", "cave", "catiyaputo atiyaṉ neṭumāṉ añci ītta pāḷi", "TITLE/CLAN+PN+VERB+OBJ", 1, 1, 0, None, None, None, "Jambai 1 (Mahadevan 2003 #59, c. 1st c. CE)"),
    ("Tamil-Brahmi", "TB_PGL1", "cave", "mūtā amaṇaṉ yāṟṟūr ceṅkāyapaṉ uṟai kō ātaṉ cel irumpoṟai makaṉ peruṅkaṭuṅkōṉ makaṉ iḷaṅkaṭuṅkō iḷaṅkō āka aṟutta kal", "PLACE+PN+GEN | KING+PN+SON+PN+TITLE+VERB", 1, 1, 1, None, None, None, "Pugalur 1 (Mahadevan 2003 #56, c. 2nd c. CE)"),
    ("Tamil-Brahmi", "TB_STV1", "cave", "erumināṭu kumuḷūr piṟanta kāvuṭi īteṉku ciṟupōcil iḷayar ceyta atiṭṭāṉam", "PLACE+ORIGIN+PN+PLACE+CLAN+VERB+OBJ", 1, 1, 1, None, None, None, "Sittannavasal 1 (Mahadevan 2003 #38)"),
    ("Tamil-Brahmi", "TB_ALM1", "cave", "matirai poṉ-vāṇikaṉ cāttaṉ", "PLACE+OCCUPATION+PN", 1, 1, 0, None, None, None, "Alagarmalai 1 (Mahadevan 2003 #32)"),
    ("Tamil-Brahmi", "TB_ALM2", "cave", "veṇpalli aṟuvai-vāṇikaṉ eḷa-aṉ ātaṉ", "PLACE+OCCUPATION+PN", 1, 1, 0, None, None, None, "Alagarmalai 2 (Mahadevan 2003 #33)"),
    ("Tamil-Brahmi", "TB_ALM3", "cave", "uppu-vāṇikaṉ viya-aṉ kāṇaṉ", "OCCUPATION+PN", 1, 1, 0, None, None, None, "Alagarmalai 3 (Mahadevan 2003 #35)"),
    ("Tamil-Brahmi", "TB_ARP1", "cave", "neḻuveḷi cītaṉ atavaṉ koṭupitavaṉ", "PLACE+PN+VERB", 1, 1, 1, None, None, None, "Arittapatti 1 (Mahadevan 2003 #11)"),
    ("Tamil-Brahmi", "TB_PMK1", "hero_stone", "kal pēṭu tīyaṉ antavaṉ kūṭal ūr ākōḷ", "OBJ+PLACE+PN+EVENT", 1, 1, 1, None, None, None, "Pulimankombai Hero Stone 1 (TN Arch. 2006)"),
    # Potsherds, Seals & Rings (Kodumanal, Keeladi, Arikamedu, Quseir al-Qadim, Khor Rori, Anaikoddai)
    ("Tamil-Brahmi", "TB_KDM1", "pot", "kaṇṇaṉ ātaṉ", "CLAN/FATHER+PN", 1, 1, None, None, None, 1, "Kodumanal potsherd (Rajan / Mahadevan 2003)"),
    ("Tamil-Brahmi", "TB_KDM2", "pot", "paṇṇaṉ", "PN_SOLO", None, 1, None, None, None, 1, "Kodumanal potsherd (Mahadevan 2003)"),
    ("Tamil-Brahmi", "TB_KDM3", "pot", "akuraṉ", "PN_SOLO", None, 1, None, None, None, 1, "Kodumanal potsherd (TN Arch. 2020)"),
    ("Tamil-Brahmi", "TB_KDM4", "pot", "kūtaṉ ātaṉ", "CLAN+PN", 1, 1, None, None, None, 1, "Kodumanal potsherd (Mahadevan 2003)"),
    ("Tamil-Brahmi", "TB_KLD1", "pot", "kuviraṉ ātaṉ", "CLAN/FATHER+PN", 1, 1, None, None, None, 1, "Keeladi potsherd (TN Arch. 2019)"),
    ("Tamil-Brahmi", "TB_KLD2", "pot", "ātaṉ", "PN_SOLO", None, 1, None, None, None, 1, "Keeladi potsherd (TN Arch. 2019)"),
    ("Tamil-Brahmi", "TB_KLD3", "pot", "ticaṉ", "PN_SOLO", None, 1, None, None, None, 1, "Keeladi potsherd (TN Arch. 2019)"),
    ("Tamil-Brahmi", "TB_QSR1", "pot", "pāṉai oṟi", "VESSEL+FUNC", None, 1, None, None, None, 1, "Quseir al-Qadim Egypt amphora (Mahadevan 2003)"),
    ("Tamil-Brahmi", "TB_QSR2", "pot", "kaṇaṉ / cāttaṉ", "PN_GEN", None, 1, None, None, None, 1, "Quseir al-Qadim Egypt potsherd (Mahadevan 2003)"),
    ("Tamil-Brahmi", "TB_KHR1", "pot", "nantai kīraṉ", "HONORIFIC+PN", 1, 1, 0, None, None, 1, "Khor Rori Oman potsherd (c. 50 CE)"),
    ("Tamil-Brahmi", "TB_ANK1", "seal", "kōvētaṉ (with 3-sign megalithic graffiti above)", "GRAFFITI_CREST + TITLE/PN", 1, 1, 1, None, None, None, "Anaikoddai steatite seal, Jaffna (Raghupathy/Mahadevan)"),
    ("Tamil-Brahmi", "TB_KRR1", "ring", "peravataṉ", "PN_TITLE", None, 1, 1, None, None, None, "Karur silver signet ring (Mahadevan 2003)"),
    # Old Tamil / Chola epigraphic & Sangam measure/count clauses (separated cleanly into MEAS+NUM vs NUM+COMM)
    ("Tamil-Brahmi", "TB_ACC1", "account", "nel kalam mūṉṟu (paddy, kalam 3)", "COMM+MEASURE+NUM", None, None, None, None, 1, None, "Old Tamil / Chola epigraphic account order (SII; Tolkāppiyam)"),
    ("Tamil-Brahmi", "TB_ACC2", "account", "arici nāḻi iraṇṭu (rice, nāḻi 2)", "COMM+MEASURE+NUM", None, None, None, None, 1, None, "Old Tamil / Chola epigraphic account order (SII)"),
    ("Tamil-Brahmi", "TB_ACC3", "account", "ney uḻakku oṉṟu (ghee, uḻakku 1)", "COMM+MEASURE+NUM", None, None, None, None, 1, None, "Old Tamil / Chola epigraphic account order (SII)"),
    ("Tamil-Brahmi", "TB_ACC4", "account", "poṉ kaḻañcu aintu (gold, kaḻañcu 5)", "COMM+MEASURE+NUM", None, None, None, None, 1, None, "Old Tamil / Chola epigraphic account order (SII)"),
    ("Tamil-Brahmi", "TB_ACC5", "account", "pāl paṭi nāṉku (milk, paṭi 4)", "COMM+MEASURE+NUM", None, None, None, None, 1, None, "Old Tamil / Chola epigraphic account order (SII)"),
    ("Tamil-Brahmi", "TB_CNT1", "account", "mūṉṟu āṭu (three sheep / ordinary count)", "NUM+COMM", None, None, None, 1, None, None, "Sangam Old Tamil ordinary numeral-before-noun (Puṟanāṉūṟu)"),
    ("Tamil-Brahmi", "TB_CNT2", "account", "mūvēntar (three crowned kings)", "NUM+COMM", None, None, None, 1, None, None, "Sangam Old Tamil (Puṟanāṉūṟu 357; Tolkāppiyam)"),
    ("Tamil-Brahmi", "TB_CNT3", "account", "nālūr (four villages)", "NUM+COMM", None, None, None, 1, None, None, "Sangam Old Tamil (Puṟanāṉūṟu)"),
    ("Tamil-Brahmi", "TB_CNT4", "account", "aṟumīṉ (six stars / Pleiades)", "NUM+COMM", None, None, None, 1, None, None, "Paripāṭal 5.49"),
    ("Tamil-Brahmi", "TB_CNT5", "account", "irukāl / mukkāl (two/three quarters)", "NUM+COMM", None, None, None, 1, None, None, "Tolkāppiyam; Sangam"),
]

ATTESTED_PKT_INSCRIPTIONS = [
    # Sanchi & Bharhut votive Prakrit Brahmi inscriptions (Bühler EI II; Lüders CII II.2)
    ("Prakrit-Brahmi", "PKT_SNC1", "votive", "Vidisāto Vāsiṭhiputasa Ānaṃdasa āvesaṇisa dānaṃ", "PLACE+MATRONYM+PN+GEN+TITLE+GEN+HEAD", 1, 1, 1, None, None, None, "Sanchi South Gateway (Bühler EI II #1)"),
    ("Prakrit-Brahmi", "PKT_SNC2", "votive", "Ujeniyā Dhammagirino dānaṃ", "PLACE+PN+GEN+HEAD", 1, 1, None, None, None, None, "Sanchi Stupa I (Bühler EI II)"),
    ("Prakrit-Brahmi", "PKT_SNC3", "votive", "Pokharāya gahapatino Patithiyasa dānaṃ", "PLACE+TITLE+GEN+PN+GEN+HEAD", 1, 1, 0, None, None, None, "Sanchi Stupa I (Bühler EI II)"),
    ("Prakrit-Brahmi", "PKT_SNC4", "votive", "Ujeniyā seṭṭhisa Nāgapiyasa dānaṃ", "PLACE+TITLE+GEN+PN+GEN+HEAD", 1, 1, 0, None, None, None, "Sanchi Stupa I (Bühler EI II)"),
    ("Prakrit-Brahmi", "PKT_SNC5", "votive", "Vidisāya dantakārehi rūpakammaṃ kataṃ", "PLACE+GUILD+INSTR+WORK+VERB", 1, 1, None, None, None, None, "Sanchi South Gateway ivory-carvers guild"),
    ("Prakrit-Brahmi", "PKT_SNC6", "votive", "Idadatasa pavārikasa dānaṃ", "PN+GEN+TITLE+GEN+HEAD", None, 1, 1, None, None, None, "Sanchi Stupa I (Bühler EI II)"),
    ("Prakrit-Brahmi", "PKT_SNC7", "votive", "Setapathiyasa Yonasa dānaṃ", "PLACE+ETHNIC+GEN+HEAD", 1, 1, 1, None, None, None, "Sanchi Stupa I (Bühler EI II)"),
    ("Prakrit-Brahmi", "PKT_SNC8", "votive", "Nāgapiyasa Achāvaḍe seṭṭhisa dānaṃ", "PN+GEN+PLACE+TITLE+GEN+HEAD", 0, 1, 1, None, None, None, "Sanchi Stupa I (Bühler EI II)"),
    ("Prakrit-Brahmi", "PKT_SNC9", "votive", "Kākanāva-pabhāsasa lekhakasa Mulagirino dānaṃ", "PLACE+TITLE+GEN+PN+GEN+HEAD", 1, 1, 0, None, None, None, "Sanchi Stupa I (Bühler EI II)"),
    ("Prakrit-Brahmi", "PKT_SNC10", "votive", "Vidisāto vaṇijasa Sirigutasa dānaṃ", "PLACE+TITLE+GEN+PN+GEN+HEAD", 1, 1, 0, None, None, None, "Sanchi Stupa I (Bühler EI II)"),
    ("Prakrit-Brahmi", "PKT_BHR1", "votive", "Sugaṇaṃ raje raño Gāgīputasa Visadevasa pautena ... Vātsīputasa Dhanabhūtisa kāritaṃ toraṇaṃ", "DYNASTY+TITLE+PN+GENEALOGY+VERB", 1, 1, 0, None, None, None, "Bharhut East Gateway (Lüders CII II.2 A1)"),
    ("Prakrit-Brahmi", "PKT_BHR2", "votive", "Vedisā Cāpadevāyā Revatimitabhāriyāya paṭhamathabho dānaṃ", "PLACE+PN+RELATION+OBJ+HEAD", 1, 1, 1, None, None, None, "Bharhut Pillar (Lüders CII II.2 A34)"),
    ("Prakrit-Brahmi", "PKT_BHR3", "votive", "Bhojakaṭakāya Dighatapasiya sisiniyā dānaṃ", "PLACE+PN+TITLE+HEAD", 1, 1, 1, None, None, None, "Bharhut Railing (Lüders CII II.2)"),
    ("Prakrit-Brahmi", "PKT_BHR4", "votive", "Karahakaṭa nigamasa dānaṃ", "PLACE+GUILD+GEN+HEAD", 1, 1, None, None, None, None, "Bharhut Coping (Lüders CII II.2 A5)"),
    ("Prakrit-Brahmi", "PKT_BHR5", "votive", "Pāṭaliputā Nāgasenāya koḍiyāniyā dānaṃ", "PLACE+PN+CLAN+HEAD", 1, 1, 1, None, None, None, "Bharhut Railing (Lüders CII II.2)"),
    ("Prakrit-Brahmi", "PKT_BHR6", "votive", "Purikāyā gahapatino Budharakhitasa dānaṃ", "PLACE+TITLE+PN+GEN+HEAD", 1, 1, 0, None, None, None, "Bharhut Railing (Lüders CII II.2)"),
    ("Prakrit-Brahmi", "PKT_BHT1", "casket", "negamā Vachaghoṣa ... goṭhiyā", "GUILD+PN_LIST", 1, 1, 0, None, None, None, "Bhattiprolu Relic Casket (Bühler EI II)"),
    ("Prakrit-Brahmi", "PKT_BSR1", "seal", "śreṣṭhi-sārthavāha-kulika-nigamasya", "TITLE+TITLE+TITLE+GUILD+GEN", 0, 1, 0, None, None, None, "Vaishali/Basarh Early Historic Guild Seal"),
    ("Prakrit-Brahmi", "PKT_BSR2", "seal", "kumārāmātyādhikaraṇasya", "TITLE+OFFICE+GEN", 0, 1, 0, None, None, None, "Vaishali/Basarh Official Seal"),
    # Fair attested Early Historic Prakrit potsherds (Arikamedu & Salihundam: mix of short owner/monastic labels & longer donative formulas)
    ("Prakrit-Brahmi", "PKT_POT1", "pot", "yakhila (short Prakrit owner sherd)", "PN_SOLO", None, 1, None, None, None, 1, "Arikamedu Prakrit Brahmi potsherd (Mahadevan 1996 / Wheeler)"),
    ("Prakrit-Brahmi", "PKT_POT2", "pot", "buta / kasapasa (short Prakrit owner sherd)", "PN+GEN", None, 1, None, None, None, 1, "Arikamedu Prakrit Brahmi potsherd (Mahadevan 1996)"),
    ("Prakrit-Brahmi", "PKT_POT3", "pot", "saṃghasa (short monastic pot label)", "INSTITUTION+GEN", None, 1, None, None, None, 1, "Salihundam Buddhist monastic potsherd (Subrahmanyam 1964)"),
    ("Prakrit-Brahmi", "PKT_POT4", "pot", "ayasa ... bhikhusa dānaṃ (longer donative pot formula)", "TITLE+PN+TITLE+GEN+HEAD", None, 1, None, None, None, 0, "Salihundam / Early Historic monastic votive pottery (Salomon 1998)"),
    ("Prakrit-Brahmi", "PKT_POT5", "pot", "mahāsaṃghikānaṃ parigrahe (longer sectarian ownership formula)", "SECT+GEN+LOC", None, 1, None, None, None, 0, "Early Historic Gandhari/Prakrit monastic jar formula (Salomon 1998)"),
    # Sanskrit/Prakrit metrology & counting clauses (separated cleanly into MEAS+NUM vs NUM+COMM)
    ("Prakrit-Brahmi", "PKT_ACC1", "account", "catvāraḥ prasthāḥ āḍhakaḥ (4 prasthas = 1 āḍhaka)", "NUM+MEASURE", None, None, None, None, 0, None, "Arthaśāstra Book II.19"),
    ("Prakrit-Brahmi", "PKT_ACC2", "account", "catvāraḥ āḍhakāḥ droṇaḥ (4 āḍhakas = 1 droṇa)", "NUM+MEASURE", None, None, None, None, 0, None, "Arthaśāstra Book II.19"),
    ("Prakrit-Brahmi", "PKT_ACC3", "account", "ṣoḍaśa droṇāḥ vārī (16 droṇas = 1 vārī)", "NUM+MEASURE", None, None, None, None, 0, None, "Arthaśāstra Book II.19"),
    ("Prakrit-Brahmi", "PKT_ACC4", "account", "viṃśati droṇāḥ kumbhaḥ (20 droṇas = 1 kumbha)", "NUM+MEASURE", None, None, None, None, 0, None, "Arthaśāstra Book II.19"),
    ("Prakrit-Brahmi", "PKT_ACC5", "account", "daśa kumbhāḥ vahaḥ (10 kumbhas = 1 vaha)", "NUM+MEASURE", None, None, None, None, 0, None, "Arthaśāstra Book II.19"),
    ("Prakrit-Brahmi", "PKT_CNT1", "account", "trīṇi koṭṭhāgālāni (3 storehouses)", "NUM+COMM", None, None, None, 1, None, None, "Sohgaura Copper-Plate (3rd c. BCE)"),
    ("Prakrit-Brahmi", "PKT_CNT2", "account", "dve morā (2 peacocks)", "NUM+COMM", None, None, None, 1, None, None, "Ashokan Rock Edict I (Girnar)"),
    ("Prakrit-Brahmi", "PKT_CNT3", "account", "caturo rājāno (4 kings)", "NUM+COMM", None, None, None, 1, None, None, "Ashokan Rock Edict XIII"),
    ("Prakrit-Brahmi", "PKT_CNT4", "account", "pañca vāsāni (5 years)", "NUM+COMM", None, None, None, 1, None, None, "Ashokan Rock Edict III"),
    ("Prakrit-Brahmi", "PKT_CNT5", "account", "aṭhabhāgiye (1/8 share)", "NUM+COMM", None, None, None, 1, None, None, "Ashokan Lumbini Pillar Edict"),
]


def extract_local_ur3_formula_rows():
    """Extract real attested Ur III seal legends & measure syntax directly from local CDLI ATF."""
    rows = []
    seen = set()
    meas_num_before = 0
    meas_after = 0
    comm_num_before = 0
    comm_after = 0

    for fname in ["abroad2/cdli_meluhha_atf.jsonl", "abroad3/cdli_east_atf.jsonl"]:
        p = f"{BASE}/work_data/{fname}"
        with open(p) as f:
            for line in f:
                obj = json.loads(line)
                sid = str(obj.get("id") or obj.get("p_number") or obj.get("cdli_id"))
                atf = obj.get("atf", "") or obj.get("transliteration", "")
                # Measure & commodity counts directly from ATF
                meas_num_before += len(re.findall(r"\b\d+\([^)]+\)\s+(?:sila3|ban2|barig|gur|ma-na|gin2|gu2)\b", atf))
                meas_after += len(re.findall(r"\b(?:sila3|ban2|barig|gur|ma-na|gin2|gu2)\s+\d+\([^)]+\)", atf))
                comm_num_before += len(re.findall(r"\b\d+\([^)]+\)\s+(?:udu|masz2|gu4|tug2|sze|ku6|ma2)\b", atf))
                comm_after += len(re.findall(r"\b(?:udu|masz2|gu4|tug2|sze|ku6|ma2)\s+\d+\([^)]+\)", atf))

                if "@seal" in atf and sid not in seen:
                    seen.add(sid)
                    idx = atf.find("@seal")
                    blk = atf[idx:]
                    m = re.search(r"\n@(?:obverse|reverse|left|right|top|bottom)", blk)
                    if m:
                        blk = blk[:m.start()]
                    ls = [l.strip() for l in blk.splitlines() if l.strip() and not l.strip().startswith(("@", "$"))]
                    if not ls or any("illegible" in l.lower() for l in ls):
                        continue
                    joined = " | ".join(ls)
                    # Determine exact syntactic features of this Ur III seal:
                    # Ur III seal order is strictly head-initial: PN -> Title -> dumu Father -> ARAD2-zu
                    # 1. header_init (Place/Father/Origin before PN?): 0 (PN is ALWAYS first!)
                    # 2. mod_before_gen (Owner/Head-final genitive?): 0 (Sumerian filiation/genitive is HEAD-INITIAL: dumu Father, ARAD2 Master!)
                    # 3. owner_before_title (PN before Title?): 1 if dub-sar/szabra/gudu4/kuruszda follows PN
                    has_title = bool(re.search(r"dub#?-?\[?sar|szabra|gudu4|kuruszda|sza13-dub|szusz3", joined))
                    has_dumu = "dumu" in joined
                    rows.append((
                        "Ur-III-Sumerian",
                        f"UR3_P{sid}",
                        "seal",
                        joined[:140],
                        "PN -> TITLE -> dumu FATHER" if (has_title and has_dumu) else ("PN -> dumu FATHER" if has_dumu else "PN -> TITLE"),
                        0,  # PN initial, NEVER place/header opener
                        0 if has_dumu else None,  # Head-initial filiation/genitive (PN before dumu Father)
                        1 if has_title else None,  # PN precedes Title (dub-sar / szabra)
                        None,
                        None,
                        None,
                        f"Local CDLI ATF P{sid} ({fname.split('/')[-1]})",
                    ))

    # Add summary account lines grounded directly in the 3,519 measured CDLI measure phrases
    for k in range(5):
        rows.append((
            "Ur-III-Sumerian",
            f"UR3_ACC{k+1}",
            "account",
            f"CDLI Ur III accounting corpus (NUM+MEAS={meas_num_before}, MEAS+NUM={meas_after})",
            "NUM + MEASURE + COMM",
            None, None, None,
            1,  # NUM before COMM
            0,  # NUM before MEASURE (94.3% in local CDLI!)
            0,  # Tablets are multi-line ledgers, not ultra-short pot graffiti
            "Local CDLI ATF aggregate (cdli_meluhha_atf + cdli_east_atf)",
        ))
    return rows, {
        "ur3_meas_num_before": meas_num_before,
        "ur3_meas_after": meas_after,
        "ur3_comm_num_before": comm_num_before,
        "ur3_comm_after": comm_after,
    }


def measure_indus_fv3_axes():
    """Measure the 6 syntactic axes directly on corpus_parsed_v3.csv (Lipi & Mahadevan intact)."""
    out = {}
    for cat in ["Lipi", "Mahadevan"]:
        open_init = open_tot = 0
        place_nonfin = place_tot = 0
        crest_bef = crest_tot = 0
        clos_bef_tit = clos_tit_tot = 0
        num_bef_comm = num_comm_tot = 0
        meas_bef_num = meas_num_tot = 0
        pot_short = pot_tot = 0

        with open(f"{BASE}/work_data/fv3/corpus_parsed_v3.csv") as f:
            for r in csv.DictReader(f):
                if r["catalogue"] != cat or r["intact"] != "True":
                    continue
                signs = r["signs"].split("-")
                cls = r["v3_classes"].split("-")
                kind = r["object_kind"]
                n = len(signs)
                if kind == "pots":
                    pot_tot += 1
                    if n <= 3:
                        pot_short += 1
                if n < 2:
                    continue
                for i, c in enumerate(cls):
                    if c == "OPEN":
                        open_tot += 1
                        if i == 0:
                            open_init += 1
                    if c == "PLACE":
                        place_tot += 1
                        if i < n - 1:
                            place_nonfin += 1
                ci = [i for i, c in enumerate(cls) if c == "CREST"]
                cl = [i for i, c in enumerate(cls) if c == "CLOSER"]
                ti = [i for i, c in enumerate(cls) if c == "TITLE"]
                if ci and cl:
                    crest_tot += 1
                    if min(ci) < max(cl):
                        crest_bef += 1
                if cl and ti:
                    clos_tit_tot += 1
                    if min(cl) < max(ti):
                        clos_bef_tit += 1
                for i in range(n - 1):
                    c1, c2 = cls[i], cls[i + 1]
                    if "NUM" in c1 and c2 == "THING":
                        num_bef_comm += 1
                        num_comm_tot += 1
                    elif c1 == "THING" and "NUM" in c2:
                        num_comm_tot += 1
                    if c1 == "MEASURE" and "NUM" in c2:
                        meas_bef_num += 1
                        meas_num_tot += 1
                    elif "NUM" in c1 and c2 == "MEASURE":
                        meas_num_tot += 1

        # Combine OPEN-initial and PLACE-nonfinal as header_init
        hdr_init = open_init + place_nonfin
        hdr_tot = open_tot + place_tot
        out[cat] = {
            "header_init": (hdr_init, hdr_tot, hdr_init / hdr_tot if hdr_tot else 0.0),
            "open_init": (open_init, open_tot, open_init / open_tot if open_tot else 0.0),
            "place_nonfin": (place_nonfin, place_tot, place_nonfin / place_tot if place_tot else 0.0),
            "mod_before_gen": (crest_bef, crest_tot, crest_bef / crest_tot if crest_tot else 0.0),
            "owner_before_title": (clos_bef_tit, clos_tit_tot, clos_bef_tit / clos_tit_tot if clos_tit_tot else 0.0),
            "num_before_comm": (num_bef_comm, num_comm_tot, num_bef_comm / num_comm_tot if num_comm_tot else 0.0),
            "meas_before_num": (meas_bef_num, meas_num_tot, meas_bef_num / meas_num_tot if meas_num_tot else 0.0),
            "pot_short": (pot_short, pot_tot, pot_short / pot_tot if pot_tot else 0.0),
            "account_reversal_fisher_p": fisher_one_sided_gt(
                num_bef_comm, num_comm_tot - num_bef_comm, meas_num_tot - meas_bef_num, meas_bef_num
            ),
        }
    return out


def run_test_4c2():
    print("\n================ TEST 4C-2: STRUCTURAL FORMULA ALIGNMENT (5,000 SHUFFLES) ================")
    indus = measure_indus_fv3_axes()
    ur3_rows, ur3_acc = extract_local_ur3_formula_rows()

    all_rows = ATTESTED_TB_INSCRIPTIONS + ATTESTED_PKT_INSCRIPTIONS + ur3_rows
    # Save comparative formula corpus CSV
    with open(f"{OUT_DIR}/epigraphic_formulas_corpus.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tradition", "id", "medium", "text_translit", "slot_sequence", "header_init", "mod_before_gen", "owner_before_title", "num_before_comm", "meas_before_num", "pot_short", "citation"])
        for r in all_rows:
            w.writerow(r)

    axes = ["header_init", "mod_before_gen", "owner_before_title", "num_before_comm", "meas_before_num", "pot_short"]
    indus_vec = np.array([indus["Lipi"][ax][2] for ax in axes], dtype=float)
    indus_mah_vec = np.array([indus["Mahadevan"][ax][2] for ax in axes], dtype=float)

    print("Indus FRAME v3 Measured Syntactic Vector (Lipi intact / Mahadevan intact):")
    for ax in axes:
        l_k, l_n, l_p = indus["Lipi"][ax]
        m_k, m_n, m_p = indus["Mahadevan"][ax]
        print(f"  {ax:20s}: Lipi={l_k:4d}/{l_n:4d} ({l_p*100:5.1f}%)  |  Mah={m_k:4d}/{m_n:4d} ({m_p*100:5.1f}%)")
    print(f"  Indus Account-Order Reversal (NUM-THING vs MEAS-NUM) Fisher P: Lipi={indus['Lipi']['account_reversal_fisher_p']:.3e}, Mah={indus['Mahadevan']['account_reversal_fisher_p']:.3e}")
    print(f"  Local CDLI Ur III Measure Order: NUM-MEAS={ur3_acc['ur3_meas_num_before']} vs MEAS-NUM={ur3_acc['ur3_meas_after']} ({100*ur3_acc['ur3_meas_num_before']/(ur3_acc['ur3_meas_num_before']+ur3_acc['ur3_meas_after']):.1f}% NUM-before-MEAS)")

    # Compute tradition vectors directly from attested rows
    trad_vecs = {}
    trad_counts = {}
    for trad in ["Tamil-Brahmi", "Prakrit-Brahmi", "Ur-III-Sumerian"]:
        sub = [r for r in all_rows if r[0] == trad]
        vec = []
        cnts = {}
        for j, ax in enumerate(axes):
            vals = [r[5 + j] for r in sub if r[5 + j] is not None]
            # For Ur III meas_before_num & num_before_comm, use exact local CDLI corpus proportions!
            if trad == "Ur-III-Sumerian" and ax == "meas_before_num":
                k = ur3_acc["ur3_meas_after"]
                n = ur3_acc["ur3_meas_after"] + ur3_acc["ur3_meas_num_before"]
                p = k / n
            elif trad == "Ur-III-Sumerian" and ax == "num_before_comm":
                k = ur3_acc["ur3_comm_num_before"]
                n = ur3_acc["ur3_comm_num_before"] + ur3_acc["ur3_comm_after"]
                p = k / n
            else:
                k = sum(vals)
                n = len(vals)
                p = k / n if n > 0 else 0.5
            vec.append(p)
            cnts[ax] = (k, n, p)
        trad_vecs[trad] = np.array(vec, dtype=float)
        trad_counts[trad] = cnts

    # Alignment metrics: (1) 1 - MAE (0 to 1), (2) Directional signed cosine on (2p - 1) in [-1, +1]
    def alignment_score(v_ind, v_tr):
        mae_align = float(1.0 - np.mean(np.abs(v_ind - v_tr)))
        a = 2.0 * v_ind - 1.0
        b = 2.0 * v_tr - 1.0
        denom = float(np.linalg.norm(a) * np.linalg.norm(b))
        dir_cos = float(np.dot(a, b) / denom) if denom > 1e-12 else 0.0
        # Number of axes agreeing in majority direction (>0.5 vs <0.5)
        sign_agree = int(np.sum((a > 0) == (b > 0)))
        return mae_align, dir_cos, sign_agree

    obs_scores = {}
    for trad, v in trad_vecs.items():
        mae_a, dcos, s_ag = alignment_score(indus_vec, v)
        obs_scores[trad] = {"mae_align": mae_a, "dir_cos": dcos, "sign_agree": s_ag}
        print(f"\n  {trad:16s}: 1-MAE={mae_a:.4f}, dir_cos={dcos:+.4f}, sign_agree={s_ag}/6")
        for ax in axes:
            k, n, p = trad_counts[trad][ax]
            print(f"    {ax:20s}: {k:4d}/{n:4d} ({p*100:5.1f}%)")

    # 5,000-Shuffle Statistical Tests:
    # (a) Random binary-direction orientation null (5,000 random sign-flips p -> 1-p across the 6 axes)
    #     Tests whether Indus+Tamil-Brahmi 6-axis alignment exceeds random directional typologies!
    rng = np.random.default_rng(RNG_SEED + 1)
    null_flip_mae = np.zeros(N_SHUFFLES)
    null_flip_cos = np.zeros(N_SHUFFLES)
    for t in range(N_SHUFFLES):
        flips = rng.integers(0, 2, size=len(axes))
        v_rand = np.where(flips == 1, trad_vecs["Tamil-Brahmi"], 1.0 - trad_vecs["Tamil-Brahmi"])
        m_a, d_c, _ = alignment_score(indus_vec, v_rand)
        null_flip_mae[t] = m_a
        null_flip_cos[t] = d_c

    # (b) 5,000-Shuffle Label-Permutation Test between Tamil-Brahmi and Prakrit-Brahmi inscriptions
    #     AND between Tamil-Brahmi and Ur-III inscriptions (exact permutation test on alignment gap!)
    tb_sub = [r for r in all_rows if r[0] == "Tamil-Brahmi"]
    pkt_sub = [r for r in all_rows if r[0] == "Prakrit-Brahmi"]
    ur3_sub = [r for r in all_rows if r[0] == "Ur-III-Sumerian"]

    def perm_gap_test(group_a, group_b):
        combined = group_a + group_b
        n_a = len(group_a)
        n_tot = len(combined)

        def vec_from_rows(rows):
            v = []
            for j in range(len(axes)):
                vals = [r[5 + j] for r in rows if r[5 + j] is not None]
                v.append(sum(vals) / len(vals) if vals else 0.5)
            return np.array(v, dtype=float)

        obs_gap = alignment_score(indus_vec, vec_from_rows(group_a))[0] - alignment_score(indus_vec, vec_from_rows(group_b))[0]
        null_gaps = np.zeros(N_SHUFFLES)
        for t in range(N_SHUFFLES):
            idx = rng.permutation(n_tot)
            ga = [combined[i] for i in idx[:n_a]]
            gb = [combined[i] for i in idx[n_a:]]
            null_gaps[t] = alignment_score(indus_vec, vec_from_rows(ga))[0] - alignment_score(indus_vec, vec_from_rows(gb))[0]
        m, s, z, p = p_and_z(obs_gap, null_gaps)
        return {"obs_gap": obs_gap, "null_mean": m, "null_std": s, "z": z, "p": p}

    gap_tb_pkt = perm_gap_test(tb_sub, pkt_sub)
    gap_tb_ur3 = perm_gap_test(tb_sub, ur3_sub)
    flip_mae_stats = dict(zip(["mean", "std", "z", "p"], p_and_z(obs_scores["Tamil-Brahmi"]["mae_align"], null_flip_mae)))
    flip_cos_stats = dict(zip(["mean", "std", "z", "p"], p_and_z(obs_scores["Tamil-Brahmi"]["dir_cos"], null_flip_cos)))

    print("\n--- 5,000-Shuffle Summary (Test 4C-2) ---")
    print(f"  Tamil-Brahmi vs Random-Axis-Flip (1-MAE):  obs={obs_scores['Tamil-Brahmi']['mae_align']:.4f}, null={flip_mae_stats['mean']:.4f}±{flip_mae_stats['std']:.4f}, z={flip_mae_stats['z']:+.2f}, P={flip_mae_stats['p']:.5f}")
    print(f"  Tamil-Brahmi vs Random-Axis-Flip (dirCos): obs={obs_scores['Tamil-Brahmi']['dir_cos']:+.4f}, null={flip_cos_stats['mean']:+.4f}±{flip_cos_stats['std']:.4f}, z={flip_cos_stats['z']:+.2f}, P={flip_cos_stats['p']:.5f}")
    print(f"  Tamil-Brahmi vs Prakrit-Brahmi (1-MAE gap): obs_gap={gap_tb_pkt['obs_gap']:+.4f}, z={gap_tb_pkt['z']:+.2f}, P={gap_tb_pkt['p']:.5f}")
    print(f"  Tamil-Brahmi vs Ur-III-Sumerian (gap):      obs_gap={gap_tb_ur3['obs_gap']:+.4f}, z={gap_tb_ur3['z']:+.2f}, P={gap_tb_ur3['p']:.5f}")

    return {
        "indus_lipi": {ax: {"k": indus["Lipi"][ax][0], "n": indus["Lipi"][ax][1], "p": indus["Lipi"][ax][2]} for ax in axes},
        "indus_mah": {ax: {"k": indus["Mahadevan"][ax][0], "n": indus["Mahadevan"][ax][1], "p": indus["Mahadevan"][ax][2]} for ax in axes},
        "account_reversal_fisher_p_lipi": indus["Lipi"]["account_reversal_fisher_p"],
        "account_reversal_fisher_p_mah": indus["Mahadevan"]["account_reversal_fisher_p"],
        "ur3_cdli_counts": ur3_acc,
        "tradition_scores": obs_scores,
        "tradition_axes": {tr: {ax: {"k": trad_counts[tr][ax][0], "n": trad_counts[tr][ax][1], "p": trad_counts[tr][ax][2]} for ax in axes} for tr in trad_counts},
        "null_flip_mae": flip_mae_stats,
        "null_flip_cos": flip_cos_stats,
        "perm_gap_tb_vs_pkt": gap_tb_pkt,
        "perm_gap_tb_vs_ur3": gap_tb_ur3,
    }


# =============================================================================
# PART 4: Test 4C-3 — Metrology Term & Ladder Lock (5,000 Shuffles)
# =============================================================================
def run_test_4c3():
    print("\n================ TEST 4C-3: METROLOGY LADDER & SCALE LOCK (5,000 SHUFFLES) ================")
    # Load real Indus measured capacity ladder from work_data/met/unit_ladder.csv
    ladder = {}
    with open(f"{BASE}/work_data/met/unit_ladder.csv") as f:
        for r in csv.DictReader(f):
            ladder[r["unit_group"]] = r

    # Parse real Indus cup count distribution (438 total events: 431 Lipi + 7 New)
    def parse_dist(s):
        d = {}
        for tok in s.split():
            k, v = tok.split(":")
            d[int(k)] = int(v)
        return d

    cup_dist = parse_dist(ladder["cup"]["value_distribution"])        # {1:9, 2:126, 3:183, 4:116, 6:3, 7:1}
    kalam_dist = parse_dist(ladder["kalam"]["value_distribution"])    # {1:6, 2:15, 3:149, 4:2, 5:13, 12:2, 24:1}
    qtr_dist = parse_dist(ladder["quarter"]["value_distribution"])    # {1:6, 2:12, 3:1, 6:1, 9:1}
    cup_total = sum(cup_dist.values())
    kalam_total = sum(kalam_dist.values())

    # Indus observed core 4-rung capacity ladder:
    #   pati (0.125 cup = 1.16 L) --[x8]--> cup (1.0 cup = 9.24 L) --[x4]--> vallam (4.0 cup = 37.0 L) --[x3]--> kalam (12.0 cup = 110.9 L) --[x6]--> kottai (72.0 cup = 665.3 L)
    # Core 3 step-ratios: [8, 4, 3] (and cup->kalam = 12, fraction = 1/4)
    # Physical liter values of the 4 core rungs: [1.16, 9.24, 37.0, 110.9]
    indus_core_steps = (8, 4, 3)
    indus_cup_to_super = 12
    indus_liters = np.array([1.16, 9.24, 37.0, 110.9], dtype=float)

    # Historical capacity systems (strictly verified from Chola/Tamil Lexicon, Arthaśāstra II.19, Ur III CDLI):
    systems = {
        "Old_Tamil_Chola": {
            "rungs": ["paṭi/nāḻi", "marakkāl/kuṟuṇi", "vaḷḷam/tūṇi", "kalam"],
            "steps": (8, 4, 3),        # 8 paṭi = 1 marakkāl; 4 marakkāl = 1 tūṇi/vaḷḷam; 3 tūṇi = 1 kalam (=12 marakkāl = 96 paṭi)
            "cup_to_super": 12,        # 1 kalam = 12 marakkāl
            "has_quarter_base": True,  # kāl = 1/4, arai = 1/2, mukkāl = 3/4, araikkāl = 1/8
            "liters": np.array([1.30, 10.4, 41.6, 124.8], dtype=float),  # Chola/Madras historical mid-range (paṭi 1.1–1.5 L)
            "top_rung_note": "Medieval South Tamil kōṭṭai = 21 marakkāl (~218 L) vs Indus 575 = 6 kalam = 72 cups (665.3 L): top rung diverges!",
            "citation": "DEDR 3849/5315/1305/2208; Chola inscriptions; U. Madras Tamil Lexicon",
        },
        "Vedic_Arthasastra": {
            "rungs": ["kuḍava", "prastha", "āḍhaka", "droṇa"],
            "steps": (4, 4, 4),        # 4 kuḍava = 1 prastha; 4 prastha = 1 āḍhaka; 4 āḍhaka = 1 droṇa; 16 droṇa = vārī / 20 = kumbha
            "cup_to_super": 16,        # 1 vārī/khārī = 16 droṇa (or 4 āḍhaka = 1 droṇa; also 20 droṇa = kumbha)
            "has_quarter_base": True,  # pāda = 1/4
            "liters": np.array([0.17, 0.68, 2.72, 10.9], dtype=float),   # Royal droṇa = 200 palas (~8-11 L), āḍhaka ~2.7 L, prastha ~0.68 L, kuḍava ~0.17 L
            "top_rung_note": "Super-units are 16 droṇa (vārī/khārī ~174 L) and 20 droṇa (kumbha ~218 L); base-4/16/20, no ×8, ×3, or ×12!",
            "citation": "Kauṭilya Arthaśāstra Book II Ch. 19 (pautavādhyakṣa)",
        },
        "Ur_III_Sumerian": {
            "rungs": ["sila3", "ban2", "barig", "gur"],
            "steps": (10, 6, 5),       # 10 sila3 = 1 ban2; 6 ban2 = 1 barig; 5 barig = 1 gur (=300 sila3)
            "cup_to_super": 6,         # 6 ban2 = 1 barig (or 10 sila3 = 1 ban2, 30 ban2 = 1 gur)
            "has_quarter_base": False, # sexagesimal 1/6, 1/3, 1/2, 5/6 primary (igi-4-gal2 secondary)
            "liters": np.array([1.0, 10.0, 60.0, 300.0], dtype=float),
            "top_rung_note": "Base-10/6/5 sexagesimal: 5 and 10 are core factors, contradicting Indus 0/438 tall-5s on cups!",
            "citation": "Ur III CDLI standard (Powell 1987; local CDLI ATF)",
        },
    }

    # Score function for any candidate 3-step ladder (s1, s2, s3) + liter anchor L0:
    # 1. Exact step-ratio matches out of 3 against Indus (8, 4, 3): 0..3
    # 2. Cup-to-super (s2 * s3) divisor compatibility with the 438 real Indus cup events:
    #    fraction of the 438 cup counts that are proper divisors of (s2 * s3) AND < (s2 * s3)
    # 3. Log-liter scale similarity across the 4 rungs: exp(-mean(|log(L_sys / L_indus)|)) in (0, 1]
    # Composite score = (step_matches / 3) + divisor_compat + liter_sim  (max = 3.0)
    def score_metrology(steps, L0):
        s1, s2, s3 = steps
        step_match = sum(1 for a, b in zip(steps, indus_core_steps) if a == b)
        super_mult = s2 * s3
        # Proper divisors of super_mult (i.e. k < super_mult and super_mult % k == 0)
        div_hits = sum(v for k, v in cup_dist.items() if k < super_mult and super_mult % k == 0)
        div_compat = div_hits / cup_total
        # Check also that tall-5 is excluded if 5 does not divide super_mult
        # Reconstruct 4-rung liter vector from base L0 and steps
        ls = np.array([L0, L0 * s1, L0 * s1 * s2, L0 * s1 * s2 * s3], dtype=float)
        mean_log_err = float(np.mean(np.abs(np.log(ls / indus_liters))))
        liter_sim = float(math.exp(-mean_log_err))
        composite = (step_match / 3.0) + div_compat + liter_sim
        return {
            "step_matches": step_match,
            "super_mult": super_mult,
            "cup_divisor_hits": div_hits,
            "cup_divisor_rate": div_compat,
            "mean_log_liter_err": mean_log_err,
            "liter_sim": liter_sim,
            "composite_score": composite,
        }

    # Note: for Arthaśāstra, test BOTH kuḍava-anchored (0.17 L, steps 4,4,4) AND prastha-anchored (0.68 L, steps 4,4,16)
    # so we test the single strongest version of the rival!
    sys_results = {}
    for name, cfg in systems.items():
        res = score_metrology(cfg["steps"], cfg["liters"][0])
        sys_results[name] = res
        print(f"  {name:20s}: steps={cfg['steps']} (match={res['step_matches']}/3), cup->super={res['super_mult']:2d}, "
              f"cup_div_compat={res['cup_divisor_hits']}/{cup_total} ({res['cup_divisor_rate']*100:5.1f}%), "
              f"log_L_err={res['mean_log_liter_err']:.3f} (sim={res['liter_sim']:.3f}), COMPOSITE={res['composite_score']:.4f}/3.0")

    # Also test strongest alternative alignment of Arthaśāstra (prastha=0.68 L -> āḍhaka -> droṇa -> vārī, steps 4,4,16)
    arth_alt = score_metrology((4, 4, 16), 0.68)
    sys_results["Vedic_Arthasastra_shifted"] = arth_alt
    print(f"  {'Arthasastra_shifted':20s}: steps=(4, 4, 16) (match={arth_alt['step_matches']}/3), cup->super={arth_alt['super_mult']:2d}, "
          f"cup_div_compat={arth_alt['cup_divisor_hits']}/{cup_total} ({arth_alt['cup_divisor_rate']*100:5.1f}%), "
          f"log_L_err={arth_alt['mean_log_liter_err']:.3f} (sim={arth_alt['liter_sim']:.3f}), COMPOSITE={arth_alt['composite_score']:.4f}/3.0")

    # 5,000-Shuffle Monte Carlo Null over plausible ancient metrological step-ratio ladders
    # Universal ancient metrological step factor pool (attested across Egypt, Mesopotamia, India, China, Greece, Rome)
    step_pool = [2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 60]
    anchor_pool = [0.15, 0.25, 0.50, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0]
    rng = np.random.default_rng(RNG_SEED + 2)

    null_comp = np.zeros(N_SHUFFLES)
    null_steps = np.zeros(N_SHUFFLES)
    null_div = np.zeros(N_SHUFFLES)
    for t in range(N_SHUFFLES):
        st = tuple(int(step_pool[i]) for i in rng.integers(0, len(step_pool), size=3))
        l0 = float(anchor_pool[int(rng.integers(0, len(anchor_pool)))])
        r = score_metrology(st, l0)
        null_comp[t] = r["composite_score"]
        null_steps[t] = r["step_matches"]
        null_div[t] = r["cup_divisor_rate"]

    mc_stats = {}
    for name in ["Old_Tamil_Chola", "Vedic_Arthasastra", "Vedic_Arthasastra_shifted", "Ur_III_Sumerian"]:
        obs = sys_results[name]["composite_score"]
        m, s, z, p = p_and_z(obs, null_comp)
        mc_stats[name] = {"obs": obs, "null_mean": m, "null_std": s, "z": z, "p": p}
        print(f"  5,000-Shuffle vs Random Ancient Ladder [{name:25s}]: obs={obs:.4f}, null={m:.4f}±{s:.4f}, z={z:+.2f}, P={p:.5f}")

    # Save metrology comparison CSV
    with open(f"{OUT_DIR}/test4c3_metrology_comparison.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["system", "steps", "step_matches_of_3", "super_mult", "cup_divisor_hits", "cup_divisor_rate", "mean_log_liter_err", "liter_sim", "composite_score", "null_mean", "z_score", "empirical_p"])
        for name in ["Old_Tamil_Chola", "Vedic_Arthasastra", "Vedic_Arthasastra_shifted", "Ur_III_Sumerian"]:
            r = sys_results[name]
            mc = mc_stats[name]
            st_str = str(systems[name]["steps"]) if name in systems else "(4, 4, 16)"
            w.writerow([name, st_str, r["step_matches"], r["super_mult"], r["cup_divisor_hits"], f"{r['cup_divisor_rate']:.4f}", f"{r['mean_log_liter_err']:.4f}", f"{r['liter_sim']:.4f}", f"{r['composite_score']:.4f}", f"{mc['null_mean']:.4f}", f"{mc['z']:.2f}", f"{mc['p']:.5f}"])

    return {
        "cup_dist": cup_dist,
        "cup_total": cup_total,
        "kalam_dist": kalam_dist,
        "kalam_total": kalam_total,
        "systems": sys_results,
        "mc_stats": mc_stats,
    }


def write_lexicon_csvs(ta_dedr_ascii):
    # 1. sangam_epigraphy_lexicon.csv
    sangam_path = f"{OUT_DIR}/sangam_epigraphy_lexicon.csv"
    with open(sangam_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "form", "ascii_form", "phon_form", "category", "etymology_layer", "dedr_id", "in_raw_dedr_headwords", "components", "gloss", "attestation_source"])
        for row in SANGAM_EPIGRAPHY_ENTRIES:
            eid, form, cat, layer, dedr_id, comps, gloss, src = row
            asc = strip_diacritics(form)
            ph = norm_phon(form)
            in_d = asc in ta_dedr_ascii
            w.writerow([eid, form, asc, ph, cat, layer, dedr_id, in_d, comps, gloss, src])

    # 2. rival_epigraphy_lexicon.csv (verify MW Sanskrit & Halloran Sumerian presence locally!)
    mw_set = set()
    with open(f"{BASE}/work_data/lexicons/tsv/sanskrit_monier_williams.tsv") as f:
        for l in f:
            p = l.split("\t", 1)
            if p:
                mw_set.add(strip_diacritics(p[0]))
    hall_set = set()
    with open(f"{BASE}/work_data/lexicons/tsv/sumerian_halloran.tsv") as f:
        for l in f:
            p = l.split("\t", 1)
            if p:
                hall_set.add(strip_diacritics(p[0]))

    rival_path = f"{OUT_DIR}/rival_epigraphy_lexicon.csv"
    ia_verified = 0
    sum_verified = 0
    with open(rival_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "tradition", "form", "epigraphic_form", "ascii_form", "phon_form", "category", "verified_local_lexicon", "gloss", "attestation_source"])
        for row in RIVAL_IA_ENTRIES:
            rid, form, epif, cat, gloss, src = row
            asc = strip_diacritics(form)
            ph = norm_phon(form)
            v = asc in mw_set or strip_diacritics(epif) in mw_set
            if v:
                ia_verified += 1
            w.writerow([rid, "Early_IndoAryan_Prakrit", form, epif, asc, ph, cat, v, gloss, src])
        for row in RIVAL_SUM_ENTRIES:
            rid, form, epif, cat, gloss, src = row
            asc = strip_diacritics(re.sub(r"\d+", "", form))
            ph = norm_phon(asc)
            v = asc in hall_set or strip_diacritics(epif) in hall_set
            if v:
                sum_verified += 1
            w.writerow([rid, "Ur_III_Sumerian", form, epif, asc, ph, cat, v, gloss, src])

    pure_n = sum(1 for e in SANGAM_EPIGRAPHY_ENTRIES if e[3] == "pure_dravidian")
    loan_n = sum(1 for e in SANGAM_EPIGRAPHY_ENTRIES if e[3] == "prakrit_sanskrit_loan")
    pure_not_in_dedr = sum(1 for e in SANGAM_EPIGRAPHY_ENTRIES if e[3] == "pure_dravidian" and strip_diacritics(e[1]) not in ta_dedr_ascii)
    print(f"Wrote {sangam_path}: {pure_n} pure_dravidian ({pure_not_in_dedr} absent from raw DEDR headwords) + {loan_n} prakrit_sanskrit_loan")
    print(f"Wrote {rival_path}: {len(RIVAL_IA_ENTRIES)} IA ({ia_verified} verified in local MW) + {len(RIVAL_SUM_ENTRIES)} Ur III ({sum_verified} verified in local Halloran)")
    return {
        "sangam_pure_n": pure_n,
        "sangam_loan_n": loan_n,
        "sangam_pure_absent_from_dedr": pure_not_in_dedr,
        "rival_ia_n": len(RIVAL_IA_ENTRIES),
        "rival_ia_verified_mw": ia_verified,
        "rival_sum_n": len(RIVAL_SUM_ENTRIES),
        "rival_sum_verified_halloran": sum_verified,
    }


def main():
    print("Loading local DEDR & corpora...")
    entries, ta_dedr_ascii, ta_dedr_phon, all_2branch_roots = load_raw_dedr()
    print(f"Loaded {len(entries)} DEDR entries, {len(ta_dedr_ascii)} Tamil headwords, {len(all_2branch_roots)} 2-branch roots.")

    lex_meta = write_lexicon_csvs(ta_dedr_ascii)
    res_4c1 = run_test_4c1(ta_dedr_ascii, ta_dedr_phon, all_2branch_roots)
    res_4c2 = run_test_4c2()
    res_4c3 = run_test_4c3()

    summary = {
        "lexicon_meta": lex_meta,
        "test_4c1": res_4c1,
        "test_4c2": res_4c2,
        "test_4c3": res_4c3,
    }
    out_json = f"{OUT_DIR}/key4c_summary.json"
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nSaved complete JSON summary to {out_json}")


if __name__ == "__main__":
    main()
