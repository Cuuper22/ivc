#!/usr/bin/env python3
"""
Key #8B — Test 8B-1: Four-Tier Sangam / Tamil-Brahmi / Chola Epigraphy Validation
Across BOTH the 227-Sign (220 strictly phonetic) Key #7A Lexicon AND the
272-Sign (266 is_phonetic_locked / 262 strictly phonetic) Key #8A Lexicon.

Four Strictly Separated Tiers (N = 5,000 deterministic shuffles each):
  Tier 1 (Frozen Zero-Circularity):
      Exact untouched 170-word Pure-Dravidian Sangam/Chola lexicon + 30-loan
      Prakrit negative control from `work_data/key7b/test7b1_sangam_expanded_lexicon.csv`,
      tested on 227-sign and 272-sign corpora (with exogenous 824a/824b split),
      strictly isolating Wave-5/6 bigrams (>=1 sign and BOTH signs from Waves 5-6),
      plus 5,000 family-level permutations, 5,000 equal-length 2-branch DEDR draws,
      MW-verified Early IA/Prakrit rival, and Halloran-verified Ur III Sumerian rival.
  Tier 2 (Expanded Strictly-Attested Wave-5/6 Compounds w/ 1:1 Rival Controls):
      Adds verifiable, attested Old Tamil / Sangam / Chola SII / U. Madras Tamil
      Lexicon / DEDR pure-Dravidian compounds built from Wave-5/6 roots (both
      hitting and equally attested non-hitting compounds for an unbiased null;
      zero invented forms; Prakrit loans strictly quarantined) matched with
      MW-verified IA/Prakrit and Halloran-verified Ur III Sumerian additions,
      5,000 family-level permutations + 5,000 DEDR draws, isolating Waves 5-6.
  Tier 3 (Non-Numeral Lexical-Lexical Only):
      Strips ALL numeral roots (*oru, *iru, *mū, *nāl, *ai, *āṟu, *ēḻ, *eṭṭu,
      *oṉpatu, *pattu, *paṉṉiru, *24) and tests purely lexical-lexical compound
      hits & token mass across Pure Dravidian vs MW Early IA/Prakrit vs Halloran
      Ur III Sumerian (5,000 family-level permutations each).
  Tier 4 (Automated Uncurated Phoneme-Preserving Dictionary Check):
      Zero hand-curation! Matches all recurring Indus adjacent sign-pair sandhi
      outputs against the raw on-disk DEDR/Tamil dictionary tables
      (`work_data/lang_m/lex/dedr_tamil.tsv` + `work_data/lang_m/lex/tamil_wiktionary.tsv`
      + `work_data/lexicons/dedr/dedr_entries.tsv`) using strict phoneme-preserving
      sandhi (both exact consonant-place + vowel-length AND consonant-place-only)
      vs 5,000 family-level root permutations.

Strictly rerunnable and portable (`ROOT = Path(__file__).resolve().parent.parent`).
Outputs:
  - work_data/key8b/test8b1_sangam_227plus.json
  - work_data/key8b/test8b1_compound_matches_key8.csv
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "work_data" / "key8b"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LEX6A_PATH = ROOT / "work_data" / "key6a" / "master_lexicon_after_key6a.csv"
LEX7A_PATH = ROOT / "work_data" / "key7a" / "master_lexicon_after_key7a.csv"
LEX8A_PATH = ROOT / "work_data" / "key8a" / "master_lexicon_after_key8a.csv"
SPLIT824_PATH = ROOT / "work_data" / "key8a" / "split_824_corpus.csv"
FROZEN_170_PATH = ROOT / "work_data" / "key7b" / "test7b1_sangam_expanded_lexicon.csv"
RIVAL_K4C_PATH = ROOT / "work_data" / "key4c" / "rival_epigraphy_lexicon.csv"
EVENTS_LIPI_PATH = ROOT / "work_data" / "sem" / "events_lipi.json"
EVENTS_NEW_PATH = ROOT / "work_data" / "sem" / "events_new.json"
DEDR_ENTRIES_PATH = ROOT / "work_data" / "lexicons" / "dedr" / "dedr_entries.tsv"
DEDR_TAMIL_PATH = ROOT / "work_data" / "lang_m" / "lex" / "dedr_tamil.tsv"
WIKT_TAMIL_PATH = ROOT / "work_data" / "lang_m" / "lex" / "tamil_wiktionary.tsv"
MW_PATH = ROOT / "work_data" / "lexicons" / "tsv" / "sanskrit_monier_williams.tsv"
HALL_PATH = ROOT / "work_data" / "lexicons" / "tsv" / "sumerian_halloran.tsv"

N_PERM = 5000
RNG_SEED = 20261181


# =============================================================================
# 1. PHONOLOGICAL NORMALIZATION & SANDHI (EXACT KEY #4C / #7B + PHONEME-PRESERVING)
# =============================================================================
def strip_diacritics(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace("ḵ", "k").replace("ḥ", "h").replace("ṃ", "m").replace("ṅ", "n").replace("ñ", "n")
    return re.sub(r"[^a-z]", "", s)


def norm_phon(s: str) -> str:
    s = strip_diacritics(s)
    return re.sub(r"([a-z])\1+", r"\1", s)


def dravidian_sandhi_joins_v2(a: str, b: str):
    """Standard Old Tamil / Tolkāppiyam compound sandhi (exact Key #7B rules, symmetric)."""
    a0 = strip_diacritics(a)
    b0 = strip_diacritics(b)
    if not a0 or not b0:
        return set(), set()

    V = set("aeiou")
    raw = {a0 + b0}

    # 1. Gemination of initial voiceless stop / nasal
    if b0[0] in ("k", "c", "t", "p", "m", "n"):
        raw.add(a0 + b0[0] + b0)
    # 2. Glide insertion between vowels
    if a0[-1] in ("i", "e", "y") and b0[0] in V:
        raw.add(a0 + "y" + b0)
    if a0[-1] in ("u", "a", "o") and b0[0] in V:
        raw.add(a0 + "v" + b0)
    # 3. Final -u elision before vowel
    if a0.endswith("u") and len(a0) >= 3 and b0[0] in V:
        raw.add(a0[:-1] + b0)
    # 4. Final -am -> -a(CC) / -att- before consonants
    if a0.endswith("am") and len(a0) >= 4 and b0[0] not in V:
        stem = a0[:-1]
        raw.add(stem + b0)
        if b0[0] in ("k", "c", "t", "p"):
            raw.add(stem + b0[0] + b0)
        raw.add(stem + "tt" + b0)
    # 5. Final -l/-n assimilation
    if a0.endswith("l") and b0.startswith("m"):
        raw.add(a0[:-1] + "n" + b0)
    # 6. Numeral allomorphs
    if a0 == "iru" and b0[0] in V:
        raw.add("ir" + b0)
    if b0 == "iru" and a0[-1] not in V:
        raw.add(a0 + "ir")
    if a0 == "mu" and b0[0] in V:
        raw.add("muv" + b0)
    if a0 == "ai":
        if b0[0] in ("p", "m"):
            raw.add("aim" + b0)
        elif b0[0] in ("t", "n", "k"):
            raw.add("ain" + b0)
    if a0 == "nal" and b0[0] in ("m", "n", "t"):
        raw.add("nan" + b0)
        if b0[0] == "t":
            raw.add("nat" + b0)
    # 7. Neṭil-toṭar kuṟṟiyalukaram doubling (-tu / -ru -> -ttu / -rru)
    if len(a0) >= 4 and a0.endswith(("tu", "ru")) and a0[-3] in V:
        c = a0[-2]
        dbl_stem = a0[:-1] + c + "u"
        raw.add(dbl_stem + b0)
        if b0[0] in ("k", "c", "t", "p"):
            raw.add(dbl_stem + b0[0] + b0)
        if b0[0] in V:
            raw.add(a0[:-1] + c + b0)
    # 8. Final -l -> -r / -t before voiceless stops & gemination before vowel
    if a0.endswith("l") and len(a0) >= 2 and b0[0] in ("k", "c", "t", "p"):
        raw.add(a0[:-1] + "r" + b0)
        raw.add(a0[:-1] + "t" + b0)
    if a0.endswith("l") and len(a0) <= 3 and b0[0] in V:
        raw.add(a0 + "l" + b0)

    phon = {norm_phon(x) for x in raw}
    return raw, phon


def ia_sandhi_joins(a: str, b: str):
    a0 = strip_diacritics(a)
    b0 = strip_diacritics(b)
    if not a0 or not b0:
        return set(), set()
    raw = {a0 + b0}
    if a0.endswith("a") and b0.startswith("a"):
        raw.add(a0[:-1] + b0)
    if a0.endswith("a") and b0.startswith("i"):
        raw.add(a0[:-1] + "e" + b0[1:])
    if a0.endswith("a") and b0.startswith("u"):
        raw.add(a0[:-1] + "o" + b0[1:])
    if a0.endswith("n") and len(a0) >= 4:
        raw.add(a0[:-1] + b0)
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
    a0 = re.sub(r"\d+", "", a.lower()).strip()
    b0 = re.sub(r"\d+", "", b.lower()).strip()
    a1 = re.sub(r"[^a-z]", "", a0)
    b1 = re.sub(r"[^a-z]", "", b0)
    if not a1 or not b1:
        return set(), set()
    raw = {a1 + b1, a0 + "-" + b0}
    phon = {norm_phon(a1 + b1)}
    return raw, phon


def phon_preserve_norm(s: str, keep_vowel_len: bool = True) -> str:
    """Phoneme-preserving Tamil normalization keeping ṭ/ḍ/ṇ/ṟ/ṉ/ḷ/ḻ/ṅ/ñ distinct."""
    s = unicodedata.normalize("NFC", s.lower().strip()).replace("r\u0324", "ḻ")
    s = s.replace("ḵ", "k").replace("ḥ", "h").replace("ṃ", "m").replace("ṁ", "m")
    if not keep_vowel_len:
        s = s.translate(str.maketrans({"ā": "a", "ī": "i", "ū": "u", "ē": "e", "ō": "o"}))
        return re.sub(r"[^a-zṭḍṇṟṉḷḻṅñśṣ]", "", s)
    return re.sub(r"[^a-zāīūēōṭḍṇṟṉḷḻṅñśṣ]", "", s)


def phon_preserve_sandhi(a: str, b: str, keep_vowel_len: bool = True) -> set[str]:
    """Phoneme-preserving Old Tamil sandhi for Tier 4 uncurated dictionary test."""
    a0 = phon_preserve_norm(a, keep_vowel_len=keep_vowel_len)
    b0 = phon_preserve_norm(b, keep_vowel_len=keep_vowel_len)
    if not a0 or not b0:
        return set()
    V = set("aeiouāīūēō")
    raw = {a0 + b0}
    if b0[0] in ("k", "c", "t", "p", "m", "n"):
        raw.add(a0 + b0[0] + b0)
    if a0[-1] in ("i", "ī", "e", "ē", "y") and b0[0] in V:
        raw.add(a0 + "y" + b0)
    if a0[-1] in ("u", "ū", "a", "ā", "o", "ō") and b0[0] in V:
        raw.add(a0 + "v" + b0)
    if a0.endswith("u") and len(a0) >= 3 and b0[0] in V:
        raw.add(a0[:-1] + b0)
    if a0.endswith("am") and len(a0) >= 4 and b0[0] not in V:
        stem = a0[:-1]
        raw.add(stem + b0)
        if b0[0] in ("k", "c", "t", "p"):
            raw.add(stem + b0[0] + b0)
        raw.add(stem + "tt" + b0)
    if len(a0) >= 4 and a0.endswith(("ṭu", "ṟu")) and a0[-3] in V:
        c = a0[-2]
        dbl = a0[:-1] + c + "u"
        raw.add(dbl + b0)
        if b0[0] in ("k", "c", "t", "p"):
            raw.add(dbl + b0[0] + b0)
        if b0[0] in V:
            raw.add(a0[:-1] + c + b0)
    if a0.endswith("l") and len(a0) >= 2 and b0[0] in ("k", "c", "t", "p"):
        raw.add(a0[:-1] + "ṟ" + b0)
    if a0.endswith("ḷ") and len(a0) >= 2 and b0[0] in ("k", "c", "t", "p"):
        raw.add(a0[:-1] + "ṭ" + b0)
    if a0.endswith("l") and len(a0) <= 3 and b0[0] in V:
        raw.add(a0 + "l" + b0)
    if a0.endswith("ḷ") and len(a0) <= 3 and b0[0] in V:
        raw.add(a0 + "ḷ" + b0)
    if a0 == "iru" and b0[0] in V:
        raw.add("īr" + b0 if keep_vowel_len else "ir" + b0)
        raw.add("ir" + b0)
    if b0 == "iru" and a0[-1] not in V:
        raw.add(a0 + "ir")
    if a0 in ("mū", "mu"):
        raw.add("mu" + b0)
        if b0[0] in ("k", "c", "t", "p", "m", "n"):
            raw.add("mu" + b0[0] + b0)
        if b0[0] in V:
            raw.add("muv" + b0)
    if a0 == "ai":
        if b0[0] in ("p", "m"):
            raw.add("aim" + b0)
        elif b0[0] in ("t", "n", "k"):
            raw.add("ain" + b0)
    if a0 in ("nāl", "nal"):
        if b0[0] in ("m", "n", "t"):
            raw.add("naṉ" + b0)
            raw.add("nan" + b0)
        if b0[0] in ("k", "c", "t", "p"):
            raw.add(("nāṟ" if keep_vowel_len else "naṟ") + b0)
    return raw


def p_and_z(obs: float, null_arr: np.ndarray) -> dict[str, float]:
    mean = float(np.mean(null_arr))
    std = float(np.std(null_arr, ddof=1)) if len(null_arr) > 1 else 0.0
    z = (obs - mean) / std if std > 1e-12 else (99.0 if obs > mean else 0.0)
    p = (int(np.sum(null_arr >= obs)) + 1) / (len(null_arr) + 1)
    return {"mean": round(mean, 4), "std": round(std, 4), "z": round(float(z), 4), "p": round(float(p), 5)}


# =============================================================================
# 2. COMPLETE 227-SIGN & 272-SIGN CANONICAL ROOT, FAMILY & RIVAL MAPS
# =============================================================================
NUMS_DRAV_163 = {
    "001": ["oru"], "031": ["oru"],
    "002": ["iru"], "032": ["iru"],
    "003": ["mu"], "013": ["mu"], "033": ["mu"],
    "004": ["nal"], "014": ["nal"], "034": ["nal"],
    "005": ["ai"], "015": ["ai"], "035": ["ai"],
    "006": ["aru"], "016": ["aru"],
    "007": ["elu"], "017": ["elu"],
    "008": ["en"],
    "025": ["onpatu"], "027": ["onpatu"],
    "028": ["pattu"],
    "055": ["panniru"],
    "056": ["irupattunal"],
}
NUMS_DRAV_227 = dict(NUMS_DRAV_163)
NUMS_DRAV_227.update({"048": ["elu"], "049": ["elu"]})
NUMS_DRAV_272 = dict(NUMS_DRAV_227)
NUMS_DRAV_272.update({"018": ["en", "ettu"], "036": ["aru"]})

NUMS_DIAC_272 = {
    "001": ["oru"], "031": ["oru"],
    "002": ["iru"], "032": ["iru"],
    "003": ["mū"], "013": ["mū"], "033": ["mū"],
    "004": ["nāl"], "014": ["nāl"], "034": ["nāl"],
    "005": ["ai"], "015": ["ai"], "035": ["ai"],
    "006": ["āṟu"], "016": ["āṟu"], "036": ["āṟu"],
    "007": ["ēḻ"], "017": ["ēḻ"], "048": ["ēḻ"], "049": ["ēḻ"],
    "008": ["eṇ"], "018": ["eṇ", "eṭṭu"],
    "025": ["oṉpatu"], "027": ["oṉpatu"],
    "028": ["pattu"],
    "055": ["paṉṉiru"],
    "056": ["irupattunāl"],
}

# Exact 163-sign lexical roots + families (identical to Key #7B)
# Schema: sign -> (ascii_roots, diac_roots, family_id)
LEX_163 = {
    # Wave 1 (Key #4C L19)
    "220": (["min"], ["mīṉ"], "220_min"),
    "820": (["kal"], ["kāl"], "820_kal"),
    "320": (["pati"], ["paṭi"], "320_pati"),
    "090": (["al"], ["āḷ"], "090_al"),
    "154": (["ka"], ["kā"], "154_ka"),
    "740": (["kuti"], ["kuṭi"], "740_kuti"),
    "400": (["cikka"], ["cikka"], "400_cikka"),
    "705": (["kalam"], ["kalam", "kaḷam"], "705_kalam"),
    "520": (["vel"], ["vēḷ"], "520_vel"),
    "850": (["kan"], ["kaṇ"], "850_kan"),
    "390": (["tai"], ["tai"], "390_tai"),
    "717": (["ati"], ["aṭi"], "717_ati"),
    "061": (["kal"], ["kāl"], "820_kal"),
    "235": (["olimin", "oli"], ["oḷimīṉ", "oḷi"], "235_olimin"),
    "500": (["pay"], ["pāy"], "500_pay"),
    "100": (["talai"], ["talai"], "100_talai"),
    "176": (["irai"], ["iṟai"], "176_irai"),
    "900": (["tinkal"], ["tiṅkaḷ"], "900_tinkal"),
    "923": (["maruppu"], ["maruppu"], "923_maruppu"),
    # Wave 1/2A Loans
    "790": (["valai"], ["vaḷai"], "790_valai"),
    "215": (["arici"], ["arici"], "215_arici"),
    "216": (["arici"], ["arici"], "215_arici"),
    "854": (["el"], ["eḷ"], "854_el"),
    # Waves 2-3 allographs & operators
    "222": (["min"], ["mīṉ"], "220_min"),
    "226": (["min"], ["mīṉ"], "220_min"),
    "236": (["olimin"], ["oḷimīṉ"], "235_olimin"),
    "231": (["ulmin"], ["uḷmīṉ"], "231_ulmin"),
    "232": (["ulmin"], ["uḷmīṉ"], "231_ulmin"),
    "233": (["vetimin"], ["veṭimīṉ"], "233_vetimin"),
    "234": (["vetimin"], ["veṭimīṉ"], "233_vetimin"),
    "240": (["katirmin"], ["katirmīṉ"], "240_katirmin"),
    "241": (["katirmin"], ["katirmīṉ"], "240_katirmin"),
    "242": (["katirmin"], ["katirmīṉ"], "240_katirmin"),
    "062": (["kal"], ["kāl"], "820_kal"),
    "821": (["irukal"], ["irukāl"], "821_irukal"),
    "322": (["pati"], ["paṭi"], "320_pati"),
    "323": (["pati"], ["paṭi"], "320_pati"),
    "324": (["pati"], ["paṭi"], "320_pati"),
    "325": (["pati"], ["paṭi"], "320_pati"),
    "097": (["al"], ["āḷ"], "090_al"),
    "219": (["al"], ["āḷ"], "090_al"),
    "091": (["irual"], ["iruāḷ"], "091_irual"),
    "093": (["ulal"], ["uḷāḷ"], "093_ulal"),
    "151": (["ka"], ["kā"], "154_ka"),
    "153": (["ka"], ["kā"], "154_ka"),
    "155": (["ka"], ["kā"], "154_ka"),
    "156": (["ka"], ["kā"], "154_ka"),
    "157": (["ka"], ["kā"], "154_ka"),
    "158": (["ka"], ["kā"], "154_ka"),
    "159": (["olika"], ["oḷikā"], "159_olika"),
    "160": (["olika"], ["oḷikā"], "159_olika"),
    "161": (["olika"], ["oḷikā"], "159_olika"),
    "741": (["orukuti"], ["orukuṭi"], "741_orukuti"),
    "742": (["irukuti"], ["irukuṭi"], "742_irukuti"),
    "743": (["irukuti"], ["irukuṭi"], "742_irukuti"),
    "744": (["irukuti"], ["irukuṭi"], "742_irukuti"),
    "745": (["mukuti"], ["mukuṭi"], "745_mukuti"),
    "746": (["mukuti"], ["mukuṭi"], "745_mukuti"),
    "747": (["mukuti"], ["mukuṭi"], "745_mukuti"),
    "748": (["nalkuti"], ["nālkuṭi"], "748_nalkuti"),
    "402": (["cikka"], ["cikka"], "400_cikka"),
    "704": (["kalam"], ["kalam", "kaḷam"], "705_kalam"),
    "706": (["kalam"], ["kalam", "kaḷam"], "705_kalam"),
    "707": (["kalam"], ["kalam", "kaḷam"], "705_kalam"),
    "392": (["tai"], ["tai"], "390_tai"),
    "405": (["tai"], ["tai"], "390_tai"),
    "406": (["tai"], ["tai"], "390_tai"),
    "408": (["tai"], ["tai"], "390_tai"),
    "409": (["tai"], ["tai"], "390_tai"),
    "716": (["ati"], ["aṭi"], "717_ati"),
    "101": (["talai"], ["talai"], "100_talai"),
    "103": (["talai"], ["talai"], "100_talai"),
    "177": (["irai"], ["iṟai"], "176_irai"),
    "178": (["irai"], ["iṟai"], "176_irai"),
    "175": (["irai"], ["iṟai"], "176_irai"),
    "899": (["tinkal"], ["tiṅkaḷ"], "900_tinkal"),
    "920": (["tinkal"], ["tiṅkaḷ"], "900_tinkal"),
    "904": (["irutinkal"], ["irutiṅkaḷ"], "904_irutinkal"),
    "927": (["irutinkal"], ["irutiṅkaḷ"], "904_irutinkal"),
    "832": (["ulvalai"], ["uḷvaḷai"], "832_ulvalai"),
    # Waves 2-3 new lexical/grammatical roots
    "700": (["ala", "akal"], ["aḷa", "akal"], "700_ala"),
    "703": (["muala"], ["mūaḷa"], "703_muala"),
    "861": (["kanam", "kan"], ["kāṇam", "kaṇ"], "861_kanam"),
    "817": (["kanam", "kan"], ["kāṇam", "kaṇ"], "861_kanam"),
    "060": (["ul"], ["uḷ"], "060_ul"),
    "590": (["mutai"], ["mūṭai"], "590_mutai"),
    "592": (["mutai"], ["mūṭai"], "590_mutai"),
    "615": (["accu"], ["accu"], "615_accu"),
    "617": (["iruaccu"], ["iruaccu"], "617_iruaccu"),
    "415": (["kavar"], ["kavar"], "415_kavar"),
    "407": (["koti"], ["kōṭi"], "407_koti"),
    "806": (["kampu"], ["kampu"], "806_kampu"),
    "803": (["kampu"], ["kampu"], "806_kampu"),
    "804": (["kampu"], ["kampu"], "806_kampu"),
    "807": (["kampu"], ["kampu"], "806_kampu"),
    "798": (["totu"], ["toṭu"], "798_totu"),
    "193": (["totu"], ["toṭu"], "798_totu"),
    "797": (["totu"], ["toṭu"], "798_totu"),
    "195": (["totu"], ["toṭu"], "798_totu"),
    "255": (["mutal"], ["mutal"], "255_mutal"),
    "840": (["inai"], ["iṇai"], "840_inai"),
    "760": (["kuruku"], ["kuruku"], "760_kuruku"),
    "752": (["kuruku"], ["kuruku"], "760_kuruku"),
    "368": (["koti", "kotu"], ["koṭi", "koṭu"], "368_koti"),
    "690": (["kattu"], ["kaṭṭu"], "690_kattu"),
    "550": (["natu"], ["nāṭu"], "550_natu"),
    "555": (["natu"], ["nāṭu"], "550_natu"),
    "892": (["vil"], ["vil"], "892_vil"),
    "140": (["amma"], ["ammā"], "140_amma"),
    "503": (["malai"], ["mālai", "malai"], "503_malai"),
    "495": (["malai"], ["mālai", "malai"], "503_malai"),
    "491": (["malai"], ["mālai", "malai"], "503_malai"),
    "575": (["kottai"], ["kōṭṭai"], "575_kottai"),
    "711": (["vallam"], ["vaḷḷam"], "711_vallam"),
    "440": (["mukku"], ["mukku"], "440_mukku"),
    "435": (["totti"], ["tōṭṭi"], "435_totti"),
    "436": (["totti"], ["tōṭṭi"], "435_totti"),
    "125": (["vilal"], ["vilāḷ"], "125_vilal"),
    "845": (["vari"], ["vari"], "845_vari"),
    "416": (["turai", "irukavar"], ["tuṟai", "irukavar"], "416_turai"),
    "413": (["ari"], ["ari"], "413_ari"),
    # Wave 4 (Key #6A)
    "142": (["kol"], ["kōl"], "142_kol"),
    "595": (["mutaivari"], ["mūṭaivari"], "595_mutaivari"),
    "350": (["totti"], ["toṭṭi"], "350_totti_yard"),
    "460": (["kanni"], ["kaṇṇi"], "460_kanni"),
    "463": (["kanni"], ["kaṇṇi"], "460_kanni"),
    "482": (["ko"], ["kō"], "482_ko"),
    "480": (["tutai"], ["tūtai"], "480_tutai"),
    "335": (["kodame", "catti"], ["koṭame", "caṭṭi"], "335_kodame"),
    "540": (["parai"], ["paṟai"], "540_parai"),
    "630": (["kutu"], ["kūṭu"], "630_kutu"),
    "632": (["kutu"], ["kūṭu"], "630_kutu"),
    "634": (["kutu"], ["kūṭu"], "630_kutu"),
    "635": (["kutu"], ["kūṭu"], "630_kutu"),
    "637": (["kutu"], ["kūṭu"], "630_kutu"),
    "171": (["tunku", "nirai"], ["tūṅku", "niṟai"], "171_tunku"),
    "831": (["alaku"], ["alaku"], "831_alaku"),
    "833": (["alaku"], ["alaku"], "831_alaku"),
    "165": (["kun"], ["kūṉ"], "165_kun"),
    "104": (["tantu"], ["taṇṭu"], "104_tantu"),
}

# Wave 5 (Key #7A) phonetic signs (55 lexical + 2 numeral 048/049 = 57 phonetic; +7 structural = 64 -> 227 total!)
LEX_W5 = {
    "585": (["palli"], ["paḷḷi"], "585_palli"),
    "527": (["ulalai", "mettu"], ["uḻalai", "meṭṭu"], "527_mettu"),
    "526": (["ulalai", "mettu"], ["uḻalai", "meṭṭu"], "527_mettu"),
    "384": (["aku", "takatu"], ["āku", "takaṭu"], "384_aku"),
    "095": (["al"], ["āḷ"], "090_al"),
    "621": (["arai", "pati"], ["aṟai", "paṭi"], "621_arai"),
    "297": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "298": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "299": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "300": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "301": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "304": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "293": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "295": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "305": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "291": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "510": (["tattam"], ["taṭṭam"], "510_tattam"),
    "511": (["tattam"], ["taṭṭam"], "510_tattam"),
    "513": (["tattam"], ["taṭṭam"], "510_tattam"),
    "890": (["vil"], ["vil"], "892_vil"),
    "167": (["mukku", "kuntani"], ["mukku", "kuntāṇi"], "440_mukku"),
    "868": (["mukku", "kuntani"], ["mukku", "kuntāṇi"], "440_mukku"),
    "243": (["katirminvari"], ["katirmīṉvari"], "243_katirminvari"),
    "137": (["al"], ["āḷ"], "090_al"),
    "139": (["al"], ["āḷ"], "090_al"),
    "636": (["kutu"], ["kūṭu"], "630_kutu"),
    "639": (["kutu"], ["kūṭu"], "630_kutu"),
    "605": (["mutaivari"], ["mūṭaivari"], "595_mutaivari"),
    "468": (["parai"], ["pārai"], "468_parai"),
    "467": (["parai"], ["pārai"], "468_parai"),
    "472": (["parai"], ["pārai"], "468_parai"),
    "470": (["parai"], ["pārai"], "468_parai"),
    "475": (["parai"], ["pārai"], "468_parai"),
    "469": (["parai"], ["pārai"], "468_parai"),
    "471": (["parai"], ["pārai"], "468_parai"),
    "474": (["parai"], ["pārai"], "468_parai"),
    "484": (["kovari"], ["kōvari"], "484_kovari"),
    "067": (["kovari"], ["kōvari"], "484_kovari"),
    "906": (["kantalam"], ["kaṇṭāḷam"], "906_kantalam"),
    "391": (["tontu"], ["toṇṭu"], "391_tontu"),
    "336": (["mutai", "tompai"], ["mūṭai", "tompai"], "590_mutai"),
    "337": (["mutai", "tompai"], ["mūṭai", "tompai"], "590_mutai"),
    "338": (["mutai", "tompai"], ["mūṭai", "tompai"], "590_mutai"),
    # Note: 422-cl *iṟu/*pāl uses ["pal"] in ASCII to avoid false numeral 'iru' sandhi collision, and ["iṟu", "pāl"] in phoneme-preserving!
    "422": (["pal"], ["pāl", "iṟu"], "422_pal"),
    "423": (["pal"], ["pāl", "iṟu"], "422_pal"),
    "426": (["pal"], ["pāl", "iṟu"], "422_pal"),
    "421": (["pal"], ["pāl", "iṟu"], "422_pal"),
    "427": (["pal"], ["pāl", "iṟu"], "422_pal"),
    "429": (["pal"], ["pāl", "iṟu"], "422_pal"),
    "430": (["pal"], ["pāl", "iṟu"], "422_pal"),
    "347": (["ma"], ["mā"], "347_ma"),
    "345": (["ma"], ["mā"], "347_ma"),
    "341": (["ma"], ["mā"], "347_ma"),
    "342": (["ma"], ["mā"], "347_ma"),
    "343": (["ma"], ["mā"], "347_ma"),
}

# Wave 6 / Key #8A phonetic signs (40 lexical + 2 numeral 018/036 = 42 phonetic; +3 structural = 45 -> 272 total!)
LEX_W6 = {
    "042": (["kattutinkal"], ["kaṭṭutiṅkaḷ"], "042_kattutinkal"),
    "064": (["panai"], ["paṇai"], "064_panai"),
    "111": (["kutam"], ["kuṭam"], "111_kutam"),
    "136": (["ka"], ["kā"], "154_ka"),
    "267": (["kutu"], ["kūṭu"], "630_kutu"),
    "269": (["kutu"], ["kūṭu"], "630_kutu"),
    "221": (["kutu"], ["kūṭu"], "630_kutu"),
    "285": (["cutu"], ["cūṭu"], "285_cutu"),
    "286": (["cutu"], ["cūṭu"], "285_cutu"),
    "287": (["cutu"], ["cūṭu"], "285_cutu"),
    "292": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "294": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "302": (["kon", "matanku"], ["kōṇ", "maṭaṅku"], "297_kon"),
    "354": (["totti"], ["toṭṭi"], "350_totti_yard"),
    "353": (["totti"], ["toṭṭi"], "350_totti_yard"),
    "371": (["katir"], ["katir"], "371_katir"),
    "370": (["katir"], ["katir"], "371_katir"),
    "388": (["aracu", "aku"], ["aracu", "āku"], "388_aracu"),
    "382": (["aracu", "aku"], ["aracu", "āku"], "388_aracu"),
    "411": (["ari"], ["ari"], "413_ari"),
    "465": (["parai"], ["pārai"], "468_parai"),
    "473": (["parai"], ["pārai"], "468_parai"),
    "501": (["pay"], ["pāy"], "500_pay"),
    "525": (["ulalai", "mettu"], ["uḻalai", "meṭṭu"], "527_mettu"),
    "552": (["natu"], ["nāṭu"], "550_natu"),
    "554": (["natu"], ["nāṭu"], "550_natu"),
    "645": (["kata", "katam"], ["kaṭa", "kaṭam"], "645_kata"),
    "679": (["kutai", "maccu"], ["kuṭai", "maccu"], "679_kutai"),
    "702": (["iruala"], ["iruaḷa"], "702_iruala"),
    "776": (["malai"], ["mālai", "malai"], "503_malai"),
    "783": (["malai"], ["mālai", "malai"], "503_malai"),
    "785": (["malai"], ["mālai", "malai"], "503_malai"),
    "792": (["metti"], ["meṭṭi"], "792_metti"),
    "824a": (["kanam", "kan"], ["kāṇam", "kaṇ"], "861_kanam"),
    "824b": (["nalkanam"], ["nālkāṇam"], "877_nalkanam"),
    "877": (["nalkanam"], ["nālkāṇam"], "877_nalkanam"),
    "880": (["kanamkal"], ["kāṇamkāl"], "880_kanamkal"),
    "905": (["irutinkal"], ["irutiṅkaḷ"], "904_irutinkal"),
    "921": (["vil"], ["vil"], "892_vil"),
    "924": (["varitinkal"], ["varitiṅkaḷ"], "924_varitinkal"),
}

LEX_227 = {**LEX_163, **LEX_W5}
LEX_272 = {**LEX_227, **LEX_W6}

# Semantic-equivalent Early IA/Prakrit & Ur III Sumerian maps for ALL 262 phonetic signs
NUMS_IA_272 = {
    "001": ["eka"], "031": ["eka"],
    "002": ["dvi"], "032": ["dvi"],
    "003": ["tri"], "013": ["tri"], "033": ["tri"],
    "004": ["catur"], "014": ["catur"], "034": ["catur"],
    "005": ["panca"], "015": ["panca"], "035": ["panca"],
    "006": ["sat"], "016": ["sat"], "036": ["sat"],
    "007": ["sapta"], "017": ["sapta"], "048": ["sapta"], "049": ["sapta"],
    "008": ["asta"], "018": ["asta"],
    "025": ["nava"], "027": ["nava"],
    "028": ["dasa"],
    "055": ["dvadasa"],
    "056": ["caturvimsati"],
}

NUMS_SUM_272 = {
    "001": ["as", "dis"], "031": ["as", "dis"],
    "002": ["min"], "032": ["min"],
    "003": ["es"], "013": ["es"], "033": ["es"],
    "004": ["limmu"], "014": ["limmu"], "034": ["limmu"],
    "005": ["ia"], "015": ["ia"], "035": ["ia"],
    "006": ["as"], "016": ["as"], "036": ["as"],
    "007": ["imin"], "017": ["imin"], "048": ["imin"], "049": ["imin"],
    "008": ["ussu"], "018": ["ussu"],
    "025": ["ilimmu"], "027": ["ilimmu"],
    "028": ["u"],
    "055": ["udis"],
    "056": ["nimin"],
}

SIGN_IA_272 = {
    # Waves 1-4 (exact Key #4C / Key #7B semantic equivalents)
    "220": ["matsya", "tara"], "820": ["cakra", "pada"], "320": ["prastha", "pada"],
    "090": ["nara", "pati"], "154": ["pala", "raksa"], "740": ["grha", "kula"],
    "400": ["laghu", "ksudra"], "705": ["drona", "nau"], "520": ["sura", "pati"],
    "850": ["aksa", "tamra"], "390": ["vastra", "vaya"], "717": ["pada", "dasa"],
    "061": ["pada"], "235": ["tara", "jyotis"], "500": ["nau", "plava"],
    "100": ["siras", "mukhya"], "176": ["kara", "bhaga"], "900": ["masa", "candra"],
    "923": ["danta"], "790": ["valaya"], "215": ["vrihi"], "216": ["vrihi"], "854": ["tila"],
    "222": ["matsya", "tara"], "226": ["matsya", "tara"], "236": ["tara"],
    "231": ["tara"], "232": ["tara"], "233": ["usastara"], "234": ["usastara"],
    "240": ["rasmitara"], "241": ["rasmitara"], "242": ["rasmitara"],
    "062": ["pada"], "821": ["dvipada"],
    "322": ["prastha"], "323": ["prastha"], "324": ["prastha"], "325": ["prastha"],
    "097": ["nara", "pati"], "219": ["nara", "pati"], "091": ["dvinara"], "093": ["antarnara"],
    "151": ["pala", "raksa"], "153": ["pala"], "155": ["pala"], "156": ["pala"], "157": ["pala"], "158": ["pala"],
    "159": ["grhapala"], "160": ["grhapala"], "161": ["grhapala"],
    "741": ["ekagrha"], "742": ["dvigrha"], "743": ["dvigrha"], "744": ["dvigrha"],
    "745": ["trigrha"], "746": ["trigrha"], "747": ["trigrha"], "748": ["caturgrha"],
    "402": ["laghu"], "704": ["drona", "nau"], "706": ["drona", "nau"], "707": ["drona", "nau"],
    "392": ["vastra"], "405": ["vastra"], "406": ["vastra"], "408": ["vastra"], "409": ["vastra"],
    "716": ["dasa"], "101": ["siras"], "103": ["siras"],
    "177": ["kara", "bhaga"], "178": ["kara", "bhaga"], "175": ["kara", "bhaga"],
    "899": ["masa"], "920": ["masa"], "904": ["dvimasa"], "927": ["dvimasa"],
    "832": ["antarvalaya"], "700": ["adhaka", "mana"], "703": ["triadhaka"],
    "861": ["bhaga", "karsa"], "817": ["bhaga", "karsa"], "060": ["antar"],
    "590": ["bhanda", "bhara"], "592": ["bhanda"],
    "615": ["ksetra", "vema"], "617": ["dviksetra"], "415": ["sakha"], "407": ["navavastra"],
    "806": ["yava", "dhanya"], "803": ["yava", "dhanya"], "804": ["yava"], "807": ["yava"],
    "798": ["sreni", "bandha"], "193": ["sreni"], "797": ["sreni"], "195": ["sreni"],
    "255": ["mukhya", "mula"], "840": ["yugma", "samaya"],
    "760": ["putra", "kumara"], "752": ["putra", "kumara"], "368": ["dhvaja", "dana"],
    "690": ["bandha", "kosa"], "550": ["janapada", "desa", "grama"], "555": ["janapada", "grama"],
    "892": ["kraya", "panya", "dhanus"], "140": ["matr", "devi"],
    "503": ["mala", "giri"], "495": ["mala"], "491": ["mala"],
    "575": ["kumbha", "kostha"], "711": ["drona", "adhaka"], "440": ["ghata", "kona"],
    "435": ["bhrta", "pala"], "436": ["bhrta"], "125": ["vanija"],
    "845": ["sulka", "kara", "bali"], "416": ["pattana", "tirtha"], "413": ["dhanya", "bhaga"],
    "142": ["danda", "karmara"], "595": ["bhandasulka"], "350": ["gostha", "vrtti"],
    "460": ["sraj", "ankura"], "463": ["sraj"], "482": ["rajan", "nrpa"],
    "480": ["kudava", "patra"], "335": ["pitaka"], "540": ["bheri", "khari"],
    "630": ["kosthagara", "sala"], "632": ["kosthagara"], "634": ["kosthagara"], "635": ["kosthagara"], "637": ["kosthagara"],
    "171": ["tula"], "831": ["sali", "patra"], "833": ["sali"],
    "165": ["kunda", "sthalika"], "104": ["danda", "kara"],
    # Wave 5 (Key #7A) semantic equivalents
    "585": ["mandira", "sala", "vihara"],
    "527": ["dvara"], "526": ["dvara"],
    "384": ["patra", "patta"],
    "095": ["nara", "pati"],
    "621": ["kosa", "kostha"],
    "297": ["kona", "bhaga"], "298": ["kona", "bhaga"], "299": ["kona", "bhaga"],
    "300": ["kona", "bhaga"], "301": ["kona", "bhaga"], "304": ["kona", "bhaga"],
    "293": ["kona", "bhaga"], "295": ["kona", "bhaga"], "305": ["kona", "bhaga"], "291": ["kona", "bhaga"],
    "510": ["patra", "sthala"], "511": ["patra", "sthala"], "513": ["patra", "sthala"],
    "890": ["kraya", "panya", "dhanus"],
    "167": ["kunda", "patra"], "868": ["kunda", "patra"],
    "243": ["rasmitarasulka"],
    "137": ["nara", "pati"], "139": ["nara", "pati"],
    "636": ["kosthagara", "sala"], "639": ["kosthagara", "sala"],
    "605": ["bhandasulka"],
    "468": ["hala", "langala"], "467": ["hala"], "472": ["hala"], "470": ["hala"],
    "475": ["hala"], "469": ["hala"], "471": ["hala"], "474": ["hala"],
    "484": ["rajasulka"], "067": ["rajasulka"],
    "906": ["bhanda", "bhara"],
    "391": ["seva", "karmakara"],
    "336": ["bhanda", "pitaka"], "337": ["bhanda", "pitaka"], "338": ["bhanda", "pitaka"],
    "422": ["bhaga", "amsa"], "423": ["bhaga", "amsa"], "426": ["bhaga", "amsa"],
    "421": ["bhaga", "amsa"], "427": ["bhaga", "amsa"], "429": ["bhaga", "amsa"], "430": ["bhaga", "amsa"],
    "347": ["maha", "mrga"], "345": ["maha", "mrga"], "341": ["maha", "mrga"], "342": ["maha", "mrga"], "343": ["maha", "mrga"],
    # Wave 6 (Key #8A) semantic equivalents
    "042": ["bandhamasa"],
    "064": ["sakha", "valaya"],
    "111": ["kumbha", "ghata"],
    "136": ["pala", "raksa"],
    "267": ["kosthagara", "sala"], "269": ["kosthagara", "sala"], "221": ["kosthagara", "sala"],
    "285": ["cuda", "kalapa"], "286": ["cuda", "kalapa"], "287": ["cuda", "kalapa"],
    "292": ["kona", "bhaga"], "294": ["kona", "bhaga"], "302": ["kona", "bhaga"],
    "354": ["gostha", "vrtti"], "353": ["gostha", "vrtti"],
    "371": ["tarku", "rasmi"], "370": ["tarku", "rasmi"],
    "388": ["rajan", "patra"], "382": ["rajan", "patra"],
    "411": ["dhanya", "bhaga"],
    "465": ["hala"], "473": ["hala"],
    "501": ["nau", "plava"],
    "525": ["dvara"],
    "552": ["janapada", "desa", "grama"], "554": ["janapada", "desa", "grama"],
    "645": ["rna", "kara"],
    "679": ["chattra", "harmya"],
    "702": ["dviadhaka"],
    "776": ["mala"], "783": ["mala"], "785": ["mala"],
    "792": ["srestha", "yugma"],
    "824a": ["bhaga", "karsa"],
    "824b": ["caturbhaga"], "877": ["caturbhaga"],
    "880": ["bhagapada"],
    "905": ["dvimasa"],
    "921": ["kraya", "panya", "dhanus"],
    "924": ["masasulka"],
}

SIGN_SUM_272 = {
    # Waves 1-4 (exact Key #4C / Key #7B semantic equivalents)
    "220": ["mul", "ku"], "820": ["igigal", "su"], "320": ["sila"],
    "090": ["lu"], "154": ["ennu"], "740": ["e"],
    "400": ["tur"], "705": ["gur", "ma"], "520": ["en", "lugal"],
    "850": ["igi", "uruda"], "390": ["tug"], "717": ["arad", "giri"],
    "061": ["igigal"], "235": ["mul"], "500": ["ma"],
    "100": ["sag"], "176": ["gu", "mas"], "900": ["iti"], "923": ["zu"],
    "790": ["har"], "215": ["se"], "216": ["se"], "854": ["iges"],
    "222": ["mul"], "226": ["mul"], "236": ["mul"],
    "231": ["mul"], "232": ["mul"], "233": ["mul"], "234": ["mul"],
    "240": ["mul"], "241": ["mul"], "242": ["mul"],
    "062": ["igigal"], "821": ["minigigal"],
    "322": ["sila"], "323": ["sila"], "324": ["sila"], "325": ["sila"],
    "097": ["lu"], "219": ["lu"], "091": ["minlu"], "093": ["salu"],
    "151": ["ennu"], "153": ["ennu"], "155": ["ennu"], "156": ["ennu"], "157": ["ennu"], "158": ["ennu"],
    "159": ["ennu"], "160": ["ennu"], "161": ["ennu"],
    "741": ["dise"], "742": ["mine"], "743": ["mine"], "744": ["mine"],
    "745": ["ese"], "746": ["ese"], "747": ["ese"], "748": ["limmue"],
    "402": ["tur"], "704": ["gur", "ma"], "706": ["gur", "ma"], "707": ["gur", "ma"],
    "392": ["tug"], "405": ["tug"], "406": ["tug"], "408": ["tug"], "409": ["tug"],
    "716": ["arad"], "101": ["sag"], "103": ["sag"],
    "177": ["gu", "mas"], "178": ["gu", "mas"], "175": ["gu", "mas"],
    "899": ["iti"], "920": ["iti"], "904": ["miniti"], "927": ["miniti"],
    "832": ["sahar"], "700": ["ban"], "703": ["esban"],
    "861": ["gin", "ha"], "817": ["gin", "ha"], "060": ["sa"],
    "590": ["gu", "sa"], "592": ["gu"], "615": ["iku", "asa"], "617": ["miniku"],
    "415": ["pa"], "407": ["tug"], "806": ["se", "ziz"], "803": ["se"], "804": ["se"], "807": ["se"],
    "798": ["e", "kesda"], "193": ["kesda"], "797": ["kesda"], "195": ["kesda"],
    "255": ["sag", "mah"], "840": ["tab", "min"], "760": ["dumu"], "752": ["dumu"],
    "368": ["su", "ba"], "690": ["kesda", "dub"],
    "550": ["mada", "kalam", "uru"], "555": ["mada", "uru"],
    "892": ["sam", "damgar"], "140": ["ama", "nin"],
    "503": ["kur", "za"], "495": ["kur"], "491": ["kur"],
    "575": ["gur", "guru"], "711": ["barig"], "440": ["dug"],
    "435": ["ugula", "lu"], "436": ["ugula"], "125": ["damgar"],
    "845": ["mas", "gu"], "416": ["kar"], "413": ["se", "mas"],
    "142": ["gidru", "simug"], "595": ["gumas"], "350": ["turas", "e"],
    "460": ["pa"], "463": ["pa"], "482": ["lugal"], "480": ["sila", "dug"],
    "335": ["pisan"], "540": ["balag", "barig"],
    "630": ["ekisiba", "guru"], "632": ["ekisiba"], "634": ["ekisiba"], "635": ["ekisiba"], "637": ["ekisiba"],
    "171": ["mana", "la"], "831": ["se", "ges"], "833": ["se"],
    "165": ["uruda", "dug"], "104": ["gu", "mas"],
    # Wave 5 (Key #7A)
    "585": ["es", "egal", "uru"],
    "527": ["ka", "abul"], "526": ["ka", "abul"],
    "384": ["dub", "pa"],
    "095": ["lu"],
    "621": ["ganun", "e"],
    "297": ["ub", "ha"], "298": ["ub", "ha"], "299": ["ub", "ha"],
    "300": ["ub", "ha"], "301": ["ub", "ha"], "304": ["ub", "ha"],
    "293": ["ub", "ha"], "295": ["ub", "ha"], "305": ["ub", "ha"], "291": ["ub", "ha"],
    "510": ["pisan", "ban"], "511": ["pisan", "ban"], "513": ["pisan", "ban"],
    "890": ["sam", "damgar"],
    "167": ["dug", "har"], "868": ["dug", "har"],
    "243": ["mulmas"],
    "137": ["lu"], "139": ["lu"],
    "636": ["ekisiba", "guru"], "639": ["ekisiba", "guru"],
    "605": ["gumas"],
    "468": ["apin"], "467": ["apin"], "472": ["apin"], "470": ["apin"],
    "475": ["apin"], "469": ["apin"], "471": ["apin"], "474": ["apin"],
    "484": ["lugalmas"], "067": ["lugalmas"],
    "906": ["gu", "sa"],
    "391": ["arad", "kin"],
    "336": ["pisan", "gu"], "337": ["pisan", "gu"], "338": ["pisan", "gu"],
    "422": ["ba", "ha"], "423": ["ba", "ha"], "426": ["ba", "ha"],
    "421": ["ba", "ha"], "427": ["ba", "ha"], "429": ["ba", "ha"], "430": ["ba", "ha"],
    "347": ["gal", "mah"], "345": ["gal", "mah"], "341": ["gal", "mah"], "342": ["gal", "mah"], "343": ["gal", "mah"],
    # Wave 6 (Key #8A)
    "042": ["kesdaiti"],
    "064": ["pa", "har"],
    "111": ["dug"],
    "136": ["ennu"],
    "267": ["ekisiba", "guru"], "269": ["ekisiba", "guru"], "221": ["ekisiba", "guru"],
    "285": ["sag", "sa"], "286": ["sag", "sa"], "287": ["sag", "sa"],
    "292": ["ub", "ha"], "294": ["ub", "ha"], "302": ["ub", "ha"],
    "354": ["turas", "e"], "353": ["turas", "e"],
    "371": ["bala", "su"], "370": ["bala", "su"],
    "388": ["lugal", "ges"], "382": ["lugal", "ges"],
    "411": ["se", "mas"],
    "465": ["apin"], "473": ["apin"],
    "501": ["ma"],
    "525": ["ka", "abul"],
    "552": ["mada", "kalam", "uru"], "554": ["mada", "kalam", "uru"],
    "645": ["gu", "mas"],
    "679": ["an", "e"],
    "702": ["minban"],
    "776": ["kur", "za"], "783": ["kur", "za"], "785": ["kur", "za"],
    "792": ["mah", "tab"],
    "824a": ["gin", "ha"],
    "824b": ["limmuha"], "877": ["limmuha"],
    "880": ["ginigigal"],
    "905": ["miniti"],
    "921": ["sam", "damgar"],
    "924": ["itimas"],
}


# =============================================================================
# 3. TIER 2 STRICTLY-ATTESTED WAVE-5/6 PURE-DRAVIDIAN COMPOUNDS (ZERO INVENTIONS!)
#    Includes BOTH hitting AND equally attested non-hitting Old Tamil / Sangam /
#    Chola SII / U. Madras Tamil Lexicon compounds so the 5,000-shuffle null is
#    100% unbiased. Matched with MW-verified IA & Halloran-verified Ur III!
# =============================================================================
WAVE56_PURE_DRAVIDIAN_ADDITIONS = [
    # --- *paḷḷi (585: temple/palace/hamlet/shrine, DEDR 4018) ---
    ("TAM178", "paḷḷikkuṭi", "house_clan", "pure_dravidian", "4018+1655", "paḷḷi+kuṭi", "shrine/hamlet household, palace settlement", "Chola inscriptions (SII); U. Madras Tamil Lexicon"),
    ("TAM179", "paḷḷiyāḷ", "admin_title", "pure_dravidian", "4018+399", "paḷḷi+āḷ", "temple/palace attendant, hamlet labourer", "U. Madras Tamil Lexicon (paḷḷiyāḷ); Chola SII"),
    ("TAM180", "paḷḷikkaṭṭu", "house_clan", "pure_dravidian", "4018+1147", "paḷḷi+kaṭṭu", "founding a hamlet/settlement; royal alliance", "U. Madras Tamil Lexicon (paḷḷikkaṭṭu); DEDR 4018+1147"),
    ("TAM181", "paḷḷiyaṟai", "house_clan", "pure_dravidian", "4018+322", "paḷḷi+aṟai", "inner royal/temple chamber", "Sangam; Chola inscriptions (SII); Tamil Lexicon"),
    ("TAM182", "paḷḷippaṭi", "metrology", "pure_dravidian", "4018+3849", "paḷḷi+paṭi", "temple/shrine daily grain allowance", "Chola inscriptions (SII; Subbarayalu)"),
    ("TAM183", "paḷḷivari", "admin_title", "pure_dravidian", "4018+5266", "paḷḷi+vari", "hamlet/temple revenue levy", "Chola inscriptions (SII)"),
    ("TAM184", "paḷḷikkūṭam", "house_clan", "pure_dravidian", "4018+1882", "paḷḷi+kūṭu", "assembly-hall / school enclosure", "U. Madras Tamil Lexicon (paḷḷikkūṭam)"),
    ("TAM185", "ēḻpaḷḷi", "house_clan", "pure_dravidian", "910+4018", "ēḻ+paḷḷi", "seven hamlets / seven-shrine district", "Classical Tamil toponymy (cf. SII Eḻupaḷḷi)"),
    # --- *aracu (388/382: royal / pipal-king emblem, DEDR 201/202) ---
    ("TAM186", "aracukuṭi", "house_clan", "pure_dravidian", "201+1655", "aracu+kuṭi", "royal household / crown-tenant family", "U. Madras Tamil Lexicon (aracu+kuṭi); Chola SII"),
    ("TAM187", "kuṭiyaracu", "admin_title", "pure_dravidian", "1655+201", "kuṭi+aracu", "civic/householders' rule", "U. Madras Tamil Lexicon; Tamil Wiktionary"),
    ("TAM188", "aracunāṭu", "admin_title", "pure_dravidian", "201+3638", "aracu+nāṭu", "royal province / crown district", "Chola inscriptions (SII)"),
    ("TAM189", "aracuvēḷ", "admin_title", "pure_dravidian", "201+5545", "aracu+vēḷ", "royal chieftain / sovereign lord", "Sangam royal title compounds (aracu+vēḷ)"),
    ("TAM190", "aracukkōl", "admin_title", "pure_dravidian", "201+2237", "aracu+kōl", "royal sceptre / standard crown gauge", "U. Madras Tamil Lexicon (aracukkōl)"),
    ("TAM191", "aracukāval", "admin_title", "pure_dravidian", "201+1416", "aracu+kā", "royal guard / crown protection", "Chola SII (aracu-kāval)"),
    ("TAM192", "aracuvari", "admin_title", "pure_dravidian", "201+5266", "aracu+vari", "royal tax / crown assessment", "Chola inscriptions (SII)"),
    # --- *aṟai / *paṭi (621: chamber / treasury / sill-measure, DEDR 322 / 3849) ---
    ("TAM193", "kuṭippaṭi", "metrology", "pure_dravidian", "1655+3849", "kuṭi+paṭi", "household allowance / family ration scale", "Chola inscriptions (SII); U. Madras Tamil Lexicon"),
    ("TAM194", "kuṭiyaṟai", "house_clan", "pure_dravidian", "1655+322", "kuṭi+aṟai", "household chamber / family room", "U. Madras Tamil Lexicon (kuṭi+aṟai)"),
    ("TAM195", "aṟaikkūṭu", "house_clan", "pure_dravidian", "322+1883", "aṟai+kūṭu", "store-chamber / locked enclosure", "U. Madras Tamil Lexicon"),
    ("TAM196", "kallaṟai", "house_clan", "pure_dravidian", "1298+322", "kāl+aṟai", "stone vault / chamber", "Sangam; U. Madras Tamil Lexicon (kallaṟai)"),
    ("TAM197", "aṟaikkāval", "admin_title", "pure_dravidian", "322+1416", "aṟai+kā", "treasury/chamber watchman", "Chola inscriptions (SII)"),
    # --- *mā (347-cl: great / deer / 1/20 land-unit, DEDR 4780/4786) ---
    ("TAM198", "mānāṭu", "admin_title", "pure_dravidian", "4786+3638", "mā+nāṭu", "great district / provincial assembly", "Chola inscriptions (SII); Tamil Lexicon (mānāṭu)"),
    ("TAM199", "mākāṇam", "metrology", "pure_dravidian", "4786+1444", "mā+kāṇam", "great district / major land-share", "U. Madras Tamil Lexicon (mākāṇam)"),
    ("TAM200", "māvēḷ", "admin_title", "pure_dravidian", "4786+5545", "mā+vēḷ", "great chieftain / grand lord", "Sangam (Puṟanāṉūṟu; māvēḷ)"),
    ("TAM201", "mākuṭi", "house_clan", "pure_dravidian", "4786+1655", "mā+kuṭi", "great clan / noble household", "Sangam; U. Madras Tamil Lexicon (mākuṭi)"),
    ("TAM202", "mākkalam", "maritime_trade", "pure_dravidian", "4786+1305", "mā+kalam", "great vessel / ocean-going ship", "Sangam (Puṟanāṉūṟu; mākkalam)"),
    ("TAM203", "mākkō", "admin_title", "pure_dravidian", "4786+2177", "mā+kō", "great king / sovereign", "Sangam (Puṟanāṉūṟu; mākōtai/mākkō)"),
    # --- *pāl (422-cl: division / portion / share, DEDR 4097) ---
    ("TAM204", "muppāl", "metrology", "pure_dravidian", "5052+4097", "mū+pāl", "three divisions / threefold share", "Tirukkuṟaḷ; Sangam; Tamil Lexicon (muppāl)"),
    ("TAM205", "irupāl", "metrology", "pure_dravidian", "474+4097", "iru+pāl", "two divisions / both sides-shares", "Tolkāppiyam; U. Madras Tamil Lexicon (irupāl)"),
    ("TAM206", "nāṟpāl", "metrology", "pure_dravidian", "3655+4097", "nāl+pāl", "four divisions / fourfold quarter", "Tolkāppiyam; Sangam (nāṟpāl)"),
    ("TAM207", "orupāl", "metrology", "pure_dravidian", "990+4097", "oru+pāl", "one side / single share", "Sangam; U. Madras Tamil Lexicon (orupāl)"),
    ("TAM208", "aimpāl", "metrology", "pure_dravidian", "2826+4097", "ai+pāl", "fivefold division", "Tolkāppiyam; Classical Tamil (aimpāl)"),
    # --- *kūṭu / *mūṭai / *kaṭam / *katir / *kuṭai / *meṭṭu / *toṭṭi / *eṭṭu / *āṟu ---
    ("TAM209", "kūṭṭukkaṭṭu", "house_clan", "pure_dravidian", "1882+1147", "kūṭu+kaṭṭu", "joined frame/pack, granary-store assembly", "U. Madras Tamil Lexicon (kūṭṭukkaṭṭu)"),
    ("TAM210", "kūṭṭukkal", "house_clan", "pure_dravidian", "1882+1479", "kūṭu+kāl", "joint quarter / masonry pillar", "DEDR 1720 / Tamil Lexicon"),
    ("TAM211", "nāṭṭumeṭṭu", "admin_title", "pure_dravidian", "3638+5059", "nāṭu+meṭṭu", "district custom-house / provincial toll-station", "Chola/Vijayanagara inscriptions; DEDR 3638+5059"),
    ("TAM212", "mūṭaikkuṭi", "house_clan", "pure_dravidian", "5037+1655", "mūṭai+kuṭi", "bale-packing/granary household", "Chola commercial guild compounds; DEDR 5037+1655"),
    ("TAM213", "iṟaimūṭai", "commodity", "pure_dravidian", "521+5037", "iṟai+mūṭai", "tribute grain-sack / tax-bale", "Chola revenue records (SII); DEDR 521+5037"),
    ("TAM214", "katirkkaṭṭu", "commodity", "pure_dravidian", "1193+1147", "katir+kaṭṭu", "bound grain-sheaf / harvest bundle", "U. Madras Tamil Lexicon (katirkkaṭṭu); Tamil Wiktionary"),
    ("TAM215", "katirkkoṭi", "commodity", "pure_dravidian", "1193+2049", "katir+koṭi", "rayed banner / sheaf-standard", "Classical Tamil (katir+koṭi)"),
    ("TAM216", "kaṭavuḷ", "admin_title", "pure_dravidian", "1109+698", "kaṭa+uḷ", "transcendent lord / inner passage-deity", "Sangam; DEDR 1109 (kaṭavuḷ)"),
    ("TAM217", "kaṭamvari", "admin_title", "pure_dravidian", "1113+5266", "kaṭam+vari", "tax-obligation / revenue duty", "Chola SII (kaṭamai/kaṭam + vari)"),
    ("TAM218", "taṇṭukkaṭam", "admin_title", "pure_dravidian", "3054+1113", "taṇṭu+kaṭam", "collected revenue duty / levy obligation", "Chola SII (taṇṭu + kaṭam)"),
    ("TAM219", "kuṭikkuṭai", "admin_title", "pure_dravidian", "1655+1663", "kuṭi+kuṭai", "shelter/canopy of the subjects/households", "Tirukkuṟaḷ 389; Sangam (kuṭi+kuṭai)"),
    ("TAM220", "kuṭimaccu", "house_clan", "pure_dravidian", "1655+4631", "kuṭi+maccu", "upper-storey house / terraced dwelling", "U. Madras Tamil Lexicon (maccu; DEDR 1655+4631)"),
    ("TAM221", "toṭṭikkuṭi", "house_clan", "pure_dravidian", "3485+1655", "toṭṭi+kuṭi", "cattle-yard/enclosure household", "U. Madras Tamil Lexicon; DEDR 3485+1655"),
    ("TAM222", "mālaikkuṭi", "house_clan", "pure_dravidian", "4827+1655", "mālai+kuṭi", "garland-makers' / hill-lineage household", "Chola SII; DEDR 4827+1655"),
    ("TAM223", "kōṇakkāl", "metrology", "pure_dravidian", "2209+1479", "kōṇ+kāl", "corner-pillar / angled quarter-post", "U. Madras Tamil Lexicon (kōṇakkāl)"),
    ("TAM224", "viṟpaṉai", "maritime_trade", "pure_dravidian", "5421+3894", "vil+paṇai", "sale / commercial vending", "DEDR 5421 (viṟpaṉai); Tamil Lexicon"),
    ("TAM225", "eṭṭukkāl", "metrology", "pure_dravidian", "784+1479", "eṭṭu+kāl", "eight quarters / eight-pillared hall", "U. Madras Tamil Lexicon (eṭṭukkāl)"),
    ("TAM226", "āṟukāl", "metrology", "pure_dravidian", "2485+1479", "āṟu+kāl", "six quarters / six-footed", "Classical Tamil (āṟukāl)"),
    ("TAM227", "kuṭanāṭu", "house_clan", "pure_dravidian", "1649+3638", "kuṭam+nāṭu", "western province (Kuttanad / Kuṭanāṭu)", "Sangam (Akaṉāṉūṟu; Kuṭanāṭu)"),
]

# Key #7B + Wave-5/6 Rival IA additions (strictly filtered against MW TSV at runtime!)
RIVAL_IA_CANDIDATES = [
    # Key #7B additions
    ("IA87", "rājagṛha", "rājagaha", "house_clan", "royal house/city", "Early Brahmi / MW"),
    ("IA88", "rājakula", "rājakula", "house_clan", "royal family/court", "Arthaśāstra / MW"),
    ("IA89", "rājadharma", "rājadhamma", "admin_title", "royal law", "Ashokan / MW"),
    ("IA90", "rājaputra", "rājaputta", "admin_title", "prince", "Arthaśāstra / MW"),
    ("IA91", "rājabhāga", "rājabhāga", "admin_title", "king's grain share", "Arthaśāstra / MW"),
    ("IA92", "rājakara", "rājakara", "admin_title", "royal tax", "Arthaśāstra / MW"),
    ("IA93", "grāmakula", "gāmakula", "house_clan", "village family", "MW"),
    ("IA94", "grāmabhāga", "gāmabhāga", "admin_title", "village share", "Arthaśāstra / MW"),
    ("IA95", "grāmakara", "gāmakara", "admin_title", "village tax", "Arthaśāstra / MW"),
    ("IA96", "grāmapati", "gāmapati", "admin_title", "village lord", "Vedic / MW"),
    ("IA97", "grāmapāla", "gāmapāla", "admin_title", "village guard", "Arthaśāstra / MW"),
    ("IA98", "deśapati", "desapati", "admin_title", "district lord", "MW"),
    ("IA99", "deśakara", "desakara", "admin_title", "district tax", "MW"),
    ("IA100", "janapada", "janapada", "house_clan", "district, province", "Ashokan / MW"),
    ("IA101", "antargrāma", "antogāma", "house_clan", "within the village", "MW"),
    ("IA102", "antardeśa", "antodesa", "house_clan", "interior district", "MW"),
    ("IA103", "antargṛha", "antogaha", "house_clan", "inner house", "MW"),
    ("IA104", "kṣetrapati", "khettapati", "admin_title", "field owner", "Rigveda / MW"),
    ("IA105", "kṣetrapāla", "khettapāla", "admin_title", "field guard", "MW"),
    ("IA106", "dhānyakoṣṭha", "dhaññakoṭṭha", "maritime_trade", "grain bin", "Arthaśāstra / MW"),
    ("IA107", "bhāṇḍapāla", "bhaṇḍapāla", "admin_title", "storekeeper", "Arthaśāstra / MW"),
    ("IA108", "daṇḍapāla", "daṇḍapāla", "admin_title", "chief magistrate", "Arthaśāstra / MW"),
    ("IA109", "daṇḍadhara", "daṇḍadhara", "admin_title", "sceptre-holder", "MW"),
    ("IA110", "śulkapāla", "sukkapāla", "admin_title", "toll-guard", "Arthaśāstra / MW"),
    ("IA111", "dvipāda", "dvipāda", "metrology", "two quarters", "Vedic / MW"),
    ("IA112", "dvibhāga", "dvibhāga", "metrology", "two shares", "Arthaśāstra / MW"),
    ("IA113", "tribhāga", "tribhāga", "metrology", "three shares", "Arthaśāstra / MW"),
    ("IA114", "caturbhāga", "catubhāga", "metrology", "four shares / quarter", "Arthaśāstra / MW"),
    ("IA115", "ekagṛha", "ekagaha", "house_clan", "single house", "MW"),
    ("IA116", "dvigṛha", "dvigaha", "house_clan", "two houses", "MW"),
    ("IA117", "trigṛha", "tigaha", "house_clan", "three houses", "MW"),
    ("IA118", "dvidroṇa", "dvidoṇa", "metrology", "two droṇas", "MW"),
    ("IA119", "tridroṇa", "tidoṇa", "metrology", "three droṇas", "MW"),
    ("IA120", "dviprastha", "dvipattha", "metrology", "two prasthas", "MW"),
    ("IA121", "śreṇīpati", "seṇipati", "admin_title", "guild master", "Early Brahmi / MW"),
    ("IA122", "koṣṭhapāla", "koṭṭhapāla", "admin_title", "granary guard", "Arthaśāstra / MW"),
    ("IA123", "koṣṭhagṛha", "koṭṭhagaha", "house_clan", "storehouse", "MW"),
    ("IA124", "tulāmāna", "tulāmāna", "metrology", "balance measure", "MW"),
    # Wave-5/6 MW-verified additions (matched 1:1 with Wave-5/6 concepts!)
    ("IA125", "mahāgṛha", "mahāgaha", "house_clan", "great house", "MW"),
    ("IA126", "mahākula", "mahākula", "house_clan", "great noble clan", "MW"),
    ("IA127", "mahārāja", "mahārāja", "admin_title", "great king", "MW"),
    ("IA128", "mahāgrāma", "mahāgāma", "house_clan", "great village", "MW"),
    ("IA129", "mahādvāra", "mahādvāra", "admin_title", "great gate", "MW"),
    ("IA130", "mahākośa", "mahākosa", "admin_title", "great treasury", "MW"),
    ("IA131", "mahāśālā", "mahāsālā", "house_clan", "great hall", "MW"),
    ("IA132", "mahāmātṛ", "mahāmātu", "admin_title", "great mother", "MW"),
    ("IA133", "mahādaṇḍa", "mahādaṇḍa", "admin_title", "great fine/staff", "MW"),
    ("IA134", "mahābhāga", "mahābhāga", "admin_title", "great share/illustrious", "MW"),
    ("IA135", "mahākara", "mahākara", "admin_title", "great tax/revenue", "MW"),
    ("IA136", "mahāmālā", "mahāmālā", "commodity", "great garland", "MW"),
    ("IA137", "mahābhāṇḍa", "mahābhaṇḍa", "commodity", "great merchandise/store", "MW"),
    ("IA138", "mahādroṇa", "mahādoṇa", "metrology", "great droṇa measure", "MW"),
    ("IA139", "rājadvāra", "rājadvāra", "admin_title", "royal gate", "MW"),
    ("IA140", "rājamandira", "rājamandira", "house_clan", "royal palace", "MW"),
    ("IA141", "rājaprāsāda", "rājapāsāda", "house_clan", "royal pavilion", "MW"),
    ("IA142", "rājadaṇḍa", "rājadaṇḍa", "admin_title", "royal sceptre/fine", "MW"),
    ("IA143", "dvārapāla", "dvārapāla", "admin_title", "gatekeeper", "MW"),
    ("IA144", "gṛhadvāra", "gahadvāra", "house_clan", "house-gate", "MW"),
    ("IA145", "kośagṛha", "kosagaha", "house_clan", "treasury-house", "MW"),
    ("IA146", "kośapāla", "kosapāla", "admin_title", "treasurer", "MW"),
    ("IA147", "kumbhakāra", "kumbhakāra", "commodity", "potter", "MW"),
    ("IA148", "aṣṭapada", "aṭṭhapada", "metrology", "eightfold/eight-footed", "MW"),
    ("IA149", "ṣaṭpada", "chappada", "metrology", "six-footed/six-part", "MW"),
    ("IA150", "ṣaṭkula", "chakkula", "house_clan", "six clans", "MW"),
    ("IA151", "chattrapati", "chattapati", "admin_title", "lord of the royal umbrella", "MW"),
    ("IA152", "chattradhara", "chattadhara", "admin_title", "umbrella-bearer", "MW"),
    ("IA153", "ṛṇagraha", "iṇagaha", "admin_title", "debt-collector", "MW"),
    ("IA154", "ṛṇadāna", "iṇadāna", "admin_title", "debt payment", "MW"),
    ("IA155", "patrapāla", "pattapāla", "admin_title", "leaf/record keeper", "MW"),
    ("IA156", "cūḍāmaṇi", "cūḷāmaṇi", "commodity", "crest-jewel", "MW"),
    ("IA157", "kalāpaka", "kalāpaka", "commodity", "bundle/band", "MW"),
]

# Key #7B + Wave-5/6 Halloran-verified Ur III Sumerian additions (strictly filtered against Halloran TSV at runtime!)
RIVAL_SUM_CANDIDATES = [
    ("SUM87", "lugal-e2", "lugale", "house_clan", "king's house", "Halloran / CDLI"),
    ("SUM88", "e2-lugal", "elugal", "house_clan", "royal estate", "Halloran / CDLI"),
    ("SUM89", "e2-dumu", "edumu", "house_clan", "son's estate", "Halloran / CDLI"),
    ("SUM90", "e2-dub-ba", "eduba", "admin_title", "tablet house", "Halloran / CDLI"),
    ("SUM91", "lu2-e2", "lue", "admin_title", "man of the house", "Halloran / CDLI"),
    ("SUM92", "gu2-e2", "gue", "admin_title", "estate tribute", "Halloran / CDLI"),
    ("SUM93", "ma2-gur", "magur", "maritime_trade", "deep-draft barge", "Halloran"),
    # Wave-5/6 Halloran-verified dictionary compounds (all verified in sumerian_halloran.tsv!)
    ("SUM94", "an-ba", "anba", "commodity", "open-air refuse/offering", "Halloran"),
    ("SUM95", "an-bala", "anbala", "maritime_trade", "conclude a sale", "Halloran"),
    ("SUM96", "an-mul", "anmul", "astral_calendar", "starry sky", "Halloran"),
    ("SUM97", "an-pa", "anpa", "astral_calendar", "zenith", "Halloran"),
    ("SUM98", "an-se", "anse", "commodity", "pack animal / equid", "Halloran"),
    ("SUM99", "ba-gal", "bagal", "metrology", "high tide / great portion", "Halloran"),
    ("SUM100", "ba-har", "bahar", "commodity", "potter", "Halloran"),
    ("SUM101", "dub-ba", "dubba", "admin_title", "archive / tablet-share", "Halloran"),
    ("SUM102", "dub-sag", "dubsag", "admin_title", "leader / head-list", "Halloran"),
    ("SUM103", "dug-gal", "duggal", "commodity", "great vessel / pleased", "Halloran"),
    ("SUM104", "dumu-gal", "dumugal", "house_clan", "eldest son", "Halloran"),
    ("SUM105", "dumu-ka", "dumuka", "house_clan", "grandson", "Halloran"),
    ("SUM106", "dumu-lu", "dumulu", "house_clan", "gentleman", "Halloran"),
    ("SUM107", "dumu-sag", "dumusag", "house_clan", "first-born child", "Halloran"),
    ("SUM108", "dumu-tab", "dumutab", "house_clan", "twin sons", "Halloran"),
    ("SUM109", "es-su", "essu", "commodity", "ear of barley", "Halloran"),
    ("SUM110", "ges-tug", "gestug", "admin_title", "understanding/ear", "Halloran"),
    ("SUM111", "gu-dub", "gudub", "admin_title", "align with string", "Halloran"),
    ("SUM112", "gu-dug", "gudug", "admin_title", "purification priest", "Halloran"),
    ("SUM113", "gu-gal", "gugal", "commodity", "chick peas / great tax", "Halloran"),
    ("SUM114", "gu-gur", "gugur", "metrology", "gather/amass grain", "Halloran"),
    ("SUM115", "gu-kin", "gukin", "admin_title", "entire inhabited world", "Halloran"),
    ("SUM116", "gur-dub", "gurdub", "commodity", "reed basket", "Halloran"),
    ("SUM117", "ka-guru", "kaguru", "admin_title", "granary supervisor", "Halloran"),
    ("SUM118", "ka-lu", "kalu", "commodity", "bowl/vessel", "Halloran"),
    ("SUM119", "kar-as", "karas", "admin_title", "encampment", "Halloran"),
    ("SUM120", "kin-gal", "kingal", "admin_title", "commander/director", "Halloran"),
    ("SUM121", "lu-gal", "lugal", "admin_title", "king/master", "Halloran"),
    ("SUM122", "sag-apin", "sagapin", "admin_title", "chief ploughman", "Halloran"),
    ("SUM123", "uru-gal", "urugal", "house_clan", "great city", "Halloran"),
    ("SUM124", "e-gal", "egal", "house_clan", "palace (great house)", "Halloran"),
    ("SUM125", "e-mah", "emah", "house_clan", "exalted house/shrine", "Halloran"),
    ("SUM126", "es-mah", "esmah", "house_clan", "exalted sanctuary", "Halloran"),
    ("SUM127", "ka-gal", "kagal", "admin_title", "great gate", "Halloran"),
    ("SUM128", "lu-mah", "lumah", "admin_title", "exalted priest", "Halloran"),
    ("SUM129", "sag-mah", "sagmah", "admin_title", "supreme head", "Halloran"),
    ("SUM130", "ugula-e", "ugulae", "admin_title", "house overseer", "Halloran"),
]


# =============================================================================
# 4. DATA LOADERS (PORTABLE, ZERO HARDCODED PATHS)
# =============================================================================
def load_split824() -> dict[str, str]:
    obj_split: dict[str, str] = {}
    with SPLIT824_PATH.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            oid = r["text_id"].strip().split(".")[0]
            obj_split[oid] = r["split_id"].strip()
    return obj_split


def load_raw_dedr_2branch():
    entries: dict[str, str] = {}
    with DEDR_ENTRIES_PATH.open(encoding="utf-8") as f:
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

    lang_pat = re.compile(r"\b(Ta|Ma|Ko|To|Ka|Koḍ|Tu|Te|Kol|Nk|Pa|Ga|Go|Konḍa|Pe|Manḍ|Kui|Kuwi|Kur|Malt|Br)\.")
    south = {"Ta", "Ma", "Ko", "To", "Ka", "Koḍ", "Tu"}
    other = {"Te", "Kol", "Nk", "Pa", "Ga", "Go", "Konḍa", "Pe", "Manḍ", "Kui", "Kuwi", "Kur", "Malt", "Br"}

    all_2branch = []
    for eid, txt in entries.items():
        txt_nfc = unicodedata.normalize("NFC", txt)
        langs = set(lang_pat.findall(txt_nfc))
        m_ta = re.search(r"\bTa\.\s+([^.]+)", txt_nfc)
        if not m_ta:
            continue
        first_root = None
        for cl in m_ta.group(1).split(";"):
            m_hw = re.match(r"^([a-zA-Zāīūēōṭḍṇṟṉḷḻṛṅñr̤\-]+(?:\s*,\s*[a-zA-Zāīūēōṭḍṇṟṉḷḻṛṅñr̤\-]+)*)", cl.strip())
            if m_hw:
                for hw in m_hw.group(1).split(","):
                    asc = strip_diacritics(hw.strip().replace("-", ""))
                    if 2 <= len(asc) <= 16:
                        first_root = asc
                        break
            if first_root:
                break
        if first_root and (langs & south) and (langs & other):
            all_2branch.append((eid, first_root, len(first_root)))
    return all_2branch


def extract_bigrams(json_path: Path, allowed: set[str], num_signs: set[str], obj_split824: dict[str, str], allow_num_num: bool = False):
    with json_path.open(encoding="utf-8") as f:
        recs = json.load(f)
    bg: Counter[tuple[str, str]] = Counter()
    for r in recs:
        oid = str(r.get("id", "")).strip()
        sp = obj_split824.get(oid)
        s2: set[tuple[str, str]] = set()
        for face in r.get("faces", []):
            f2 = [sp if (t == "824" and sp) else t for t in face]
            for a, b in zip(f2, f2[1:]):
                if a in allowed and b in allowed:
                    if (not allow_num_num) and (a in num_signs and b in num_signs):
                        continue
                    s2.add((a, b))
        for pair in s2:
            bg[pair] += 1
    return bg, len(recs)


def build_target_maps(entries_list, multi_col: bool = False, strip_digits: bool = False):
    amap, pmap = {}, {}
    for e in entries_list:
        cols = (e[1], e[2]) if multi_col else (e[1],)
        for c in cols:
            c_use = re.sub(r"\d+", "", c) if strip_digits else c
            asc = strip_diacritics(c_use)
            ph = norm_phon(c_use)
            if len(asc) >= 4 and asc not in amap:
                amap[asc] = e
            if len(ph) >= 5 and ph not in pmap:
                pmap[ph] = e
    return amap, pmap


def make_fast_checker(amap, pmap, join_fn):
    all_keys = list(amap.keys()) + list(pmap.keys())
    v_first = {w[0] for w in all_keys if w}
    cache = {}

    def check(ra_list, rb_list):
        key = (tuple(ra_list), tuple(rb_list))
        if key in cache:
            return cache[key]
        res = None
        for ra in ra_list:
            a0 = strip_diacritics(ra)
            if not a0 or a0[0] not in v_first:
                continue
            na0 = norm_phon(a0)
            for rb in rb_list:
                b0 = strip_diacritics(rb)
                if not b0:
                    continue
                nb0 = norm_phon(b0)
                rset, pset = join_fn(ra, rb)
                for s in sorted(rset):
                    if s in amap and s != a0 and s != b0:
                        res = amap[s][1]
                        break
                if res:
                    break
                for ph in sorted(pset):
                    if len(ph) >= 5 and ph in pmap and ph != na0 and ph != nb0:
                        res = pmap[ph][1]
                        break
                if res:
                    break
            if res:
                break
        cache[key] = res
        return res

    return check


def match_detailed(items, smap, nmap, amap, pmap, join_fn, bg_lipi, bg_new):
    hits = []
    for (a, b), cnt in items:
        ra_list = smap.get(a) or nmap.get(a) or []
        rb_list = smap.get(b) or nmap.get(b) or []
        m_ent = m_surf = m_ra = m_rb = None
        for ra in ra_list:
            a0 = strip_diacritics(ra)
            na0 = norm_phon(a0)
            for rb in rb_list:
                b0 = strip_diacritics(rb)
                nb0 = norm_phon(b0)
                rset, pset = join_fn(ra, rb)
                for s in sorted(rset):
                    if s in amap and s != a0 and s != b0:
                        m_ent, m_surf, m_ra, m_rb = amap[s], s, ra, rb
                        break
                if m_ent:
                    break
                for ph in sorted(pset):
                    if len(ph) >= 5 and ph in pmap and ph != na0 and ph != nb0:
                        m_ent, m_surf, m_ra, m_rb = pmap[ph], ph, ra, rb
                        break
                if m_ent:
                    break
            if m_ent:
                break
        if m_ent:
            hits.append({
                "pair": f"{a}-{b}",
                "a": a,
                "b": b,
                "roots": f"{m_ra}+{m_rb}",
                "surface": m_surf,
                "entry": m_ent,
                "count": cnt,
                "lipi_count": bg_lipi.get((a, b), 0),
                "new_count": bg_new.get((a, b), 0),
            })
    return hits


def eval_with_perms_and_draws(
    cut_name: str,
    items: list[tuple[tuple[str, str], int]],
    smap: dict[str, list[str]],
    nmap: dict[str, list[str]],
    fam_map: dict[str, str],
    amap: dict,
    pmap: dict,
    join_fn,
    bg_lipi: Counter,
    bg_new: Counter,
    rng: np.random.Generator,
    fixed_lex_signs: set[str] | None = None,
    by_len_dedr: dict[int, list[str]] | None = None,
):
    checker = make_fast_checker(amap, pmap, join_fn)
    fixed_set = fixed_lex_signs or set()

    # Observed stats
    obs_w: set[str] = set()
    obs_p = obs_lm = obs_nm = 0
    for (a, b), _ in items:
        ra = smap.get(a) or nmap.get(a)
        rb = smap.get(b) or nmap.get(b)
        if not ra or not rb:
            continue
        m = checker(ra, rb)
        if m:
            obs_w.add(m)
            obs_p += 1
            obs_lm += bg_lipi.get((a, b), 0)
            obs_nm += bg_new.get((a, b), 0)

    if not items:
        return {
            "cut": cut_name,
            "n_bigrams_tested": 0,
            "obs_words": 0,
            "obs_pairs": 0,
            "obs_lipi_mass": 0,
            "obs_new_mass": 0,
            "obs_word_list": [],
            "perm_words": {"mean": 0.0, "std": 0.0, "z": 0.0, "p": 1.0},
            "perm_pairs": {"mean": 0.0, "std": 0.0, "z": 0.0, "p": 1.0},
            "perm_lipi_mass": {"mean": 0.0, "std": 0.0, "z": 0.0, "p": 1.0},
            "perm_new_mass": {"mean": 0.0, "std": 0.0, "z": 0.0, "p": 1.0},
        }

    # Build family slots (permutable vs fixed)
    perm_fams: dict[str, list[str]] = defaultdict(list)
    for s in sorted(smap.keys()):
        if s not in fixed_set:
            perm_fams[fam_map[s]].append(s)
    fkeys = sorted(perm_fams.keys())
    froots = [smap[perm_fams[fk][0]] for fk in fkeys]
    n_f = len(fkeys)

    sign_to_slot: dict[str, int] = {}
    for i, fk in enumerate(fkeys):
        for s in perm_fams[fk]:
            sign_to_slot[s] = i

    fixed_roots: list[list[str]] = []
    fixed_lookup: dict[tuple[str, ...], int] = {}
    for s in sorted(fixed_set | set(nmap.keys())):
        if s not in sign_to_slot:
            rlist = tuple(smap.get(s) or nmap[s])
            if rlist not in fixed_lookup:
                fixed_lookup[rlist] = n_f + len(fixed_roots)
                fixed_roots.append(list(rlist))
            sign_to_slot[s] = fixed_lookup[rlist]

    all_slot_roots = list(froots) + fixed_roots
    n_tot = len(all_slot_roots)

    word_to_id: dict[str, int] = {}
    match_mat = np.zeros((n_tot, n_tot), dtype=np.int32)
    for i in range(n_tot):
        ri = all_slot_roots[i]
        for j in range(n_tot):
            m = checker(ri, all_slot_roots[j])
            if m:
                wid = word_to_id.setdefault(m, len(word_to_id) + 1)
                match_mat[i, j] = wid

    slot_a = np.array([sign_to_slot[a] for (a, _), _ in items], dtype=np.int32)
    slot_b = np.array([sign_to_slot[b] for (_, b), _ in items], dtype=np.int32)
    item_lipi = np.array([bg_lipi.get(k, 0) for k, _ in items], dtype=np.int32)
    item_new = np.array([bg_new.get(k, 0) for k, _ in items], dtype=np.int32)

    p_words = np.zeros(N_PERM)
    p_pairs = np.zeros(N_PERM)
    p_lmass = np.zeros(N_PERM)
    p_nmass = np.zeros(N_PERM)
    full_perm = np.arange(n_tot, dtype=np.int32)
    for t in range(N_PERM):
        if n_f > 1:
            full_perm[:n_f] = rng.permutation(n_f)
        wids = match_mat[full_perm[slot_a], full_perm[slot_b]]
        hm = wids > 0
        if np.any(hm):
            p_words[t] = len(np.unique(wids[hm]))
            p_pairs[t] = int(np.sum(hm))
            p_lmass[t] = int(np.sum(item_lipi[hm]))
            p_nmass[t] = int(np.sum(item_new[hm]))

    out = {
        "cut": cut_name,
        "n_bigrams_tested": len(items),
        "obs_words": len(obs_w),
        "obs_pairs": obs_p,
        "obs_lipi_mass": obs_lm,
        "obs_new_mass": obs_nm,
        "obs_word_list": sorted(obs_w),
        "perm_words": p_and_z(len(obs_w), p_words),
        "perm_pairs": p_and_z(obs_p, p_pairs),
        "perm_lipi_mass": p_and_z(obs_lm, p_lmass),
        "perm_new_mass": p_and_z(obs_nm, p_nmass),
    }

    # Optional 5,000 equal-length 2-branch DEDR root draws (for Dravidian tests)
    if by_len_dedr is not None and n_f > 0:
        def get_pool(rstr: str) -> list[str]:
            L = len(strip_diacritics(rstr))
            pool = list(by_len_dedr.get(L, []))
            if len(pool) < 30:
                pool += by_len_dedr.get(L - 1, []) + by_len_dedr.get(L + 1, [])
            return pool if pool else by_len_dedr[4]

        fpools = [get_pool(r[0]) for r in froots]
        r_to_id: dict[tuple[str, ...], int] = {}
        id_to_rlist: list[list[str]] = []
        for pl in fpools:
            for w in pl:
                tw = (w,)
                if tw not in r_to_id:
                    r_to_id[tw] = len(id_to_rlist)
                    id_to_rlist.append([w])
        for rl in fixed_roots:
            tw = tuple(rl)
            if tw not in r_to_id:
                r_to_id[tw] = len(id_to_rlist)
                id_to_rlist.append(list(rl))

        r_meta = []
        for rl in id_to_rlist:
            fa, fb = set(), set()
            for w in rl:
                a0 = strip_diacritics(w)
                p0 = norm_phon(a0)
                fa.add(a0[: max(1, len(a0) - 1)])
                fa.add(p0[: max(1, len(p0) - 1)])
                if a0 == "nal":
                    fa.add("na")
                fb.add(a0)
                fb.add(p0)
                if a0 == "iru":
                    fb.add("ir")
            r_meta.append((fa, fb))

        all_targets = set(amap.keys()) | set(pmap.keys())
        cand_pairs = set()
        for W in all_targets:
            a_hits = [rid for rid, (fa, _) in enumerate(r_meta) if any(W.startswith(p) for p in fa)]
            if not a_hits:
                continue
            b_hits = [rid for rid, (_, fb) in enumerate(r_meta) if any(W.endswith(s) for s in fb)]
            for ria in a_hits:
                for rib in b_hits:
                    cand_pairs.add((ria, rib))

        sparse_hits: dict[int, dict[int, str]] = defaultdict(dict)
        for ria, rib in cand_pairs:
            m = checker(id_to_rlist[ria], id_to_rlist[rib])
            if m:
                sparse_hits[ria][rib] = m

        pool_ids = [np.array([r_to_id[(w,)] for w in pl], dtype=np.int32) for pl in fpools]
        fixed_ids = [r_to_id[tuple(rl)] for rl in fixed_roots]
        slot_pair_mass: dict[tuple[int, int], int] = defaultdict(int)
        for sa, sb, lm_v in zip(slot_a.tolist(), slot_b.tolist(), item_lipi.tolist()):
            slot_pair_mass[(sa, sb)] += lm_v
        out_edges: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for (sa, sb), lm_v in slot_pair_mass.items():
            out_edges[sa].append((sb, lm_v))
        active_sa = sorted(out_edges.keys())

        rand_rids = np.empty((N_PERM, n_tot), dtype=np.int32)
        for i in range(n_f):
            pids = pool_ids[i]
            rand_rids[:, i] = pids[rng.integers(0, len(pids), size=N_PERM)]
        for k, fid in enumerate(fixed_ids):
            rand_rids[:, n_f + k] = fid

        d_words = np.zeros(N_PERM)
        d_lmass = np.zeros(N_PERM)
        for t in range(N_PERM):
            row = rand_rids[t].tolist()
            wd = set()
            lmd = 0
            for sa in active_sa:
                hmap = sparse_hits.get(row[sa])
                if hmap is None:
                    continue
                for sb, lm_v in out_edges[sa]:
                    m = hmap.get(row[sb])
                    if m is not None:
                        wd.add(m)
                        lmd += lm_v
            d_words[t] = len(wd)
            d_lmass[t] = lmd

        out["dedr_draw_words"] = p_and_z(len(obs_w), d_words)
        out["dedr_draw_lipi_mass"] = p_and_z(obs_lm, d_lmass)

    return out


# =============================================================================
# 5. TIER 4: AUTOMATED UNCURATED PHONEME-PRESERVING DICTIONARY CHECK
# =============================================================================
def run_tier4_automated(
    lex_label: str,
    diac_smap: dict[str, list[str]],
    diac_nmap: dict[str, list[str]],
    fam_map: dict[str, str],
    items: list[tuple[tuple[str, str], int]],
    bg_lipi: Counter,
    bg_new: Counter,
    dict_map: dict[str, tuple[str, str, str]],
    keep_vowel_len: bool,
    rng: np.random.Generator,
):
    """Completely uncurated dictionary match with 5,000 family-level permutations."""
    perm_fams: dict[str, list[str]] = defaultdict(list)
    for s in sorted(diac_smap.keys()):
        perm_fams[fam_map[s]].append(s)
    fkeys = sorted(perm_fams.keys())
    froots = [diac_smap[perm_fams[fk][0]] for fk in fkeys]
    n_f = len(fkeys)

    sign_to_slot: dict[str, int] = {}
    for i, fk in enumerate(fkeys):
        for s in perm_fams[fk]:
            sign_to_slot[s] = i

    fixed_roots: list[list[str]] = []
    fixed_lookup: dict[tuple[str, ...], int] = {}
    for s in sorted(diac_nmap.keys()):
        if s not in sign_to_slot:
            rl = tuple(diac_nmap[s])
            if rl not in fixed_lookup:
                fixed_lookup[rl] = n_f + len(fixed_roots)
                fixed_roots.append(list(rl))
            sign_to_slot[s] = fixed_lookup[rl]

    all_slot_roots = list(froots) + fixed_roots
    n_tot = len(all_slot_roots)

    word_to_id: dict[str, int] = {}
    id_to_meta: dict[int, tuple[str, str, str, str]] = {}
    match_mat = np.zeros((n_tot, n_tot), dtype=np.int32)
    for i in range(n_tot):
        for j in range(n_tot):
            found = None
            for ra in all_slot_roots[i]:
                na = phon_preserve_norm(ra, keep_vowel_len=keep_vowel_len)
                for rb in all_slot_roots[j]:
                    nb = phon_preserve_norm(rb, keep_vowel_len=keep_vowel_len)
                    for surf in sorted(phon_preserve_sandhi(ra, rb, keep_vowel_len=keep_vowel_len)):
                        if (
                            surf in dict_map
                            and surf != na
                            and surf != nb
                            and len(surf) >= len(na) + 2
                            and len(surf) >= len(nb) + 2
                        ):
                            found = (surf, ra, rb, dict_map[surf])
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                surf, ra, rb, (src, form, gloss) = found
                wid = word_to_id.setdefault(surf, len(word_to_id) + 1)
                id_to_meta[wid] = (form, src, gloss, f"{ra}+{rb}")
                match_mat[i, j] = wid

    slot_a = np.array([sign_to_slot[a] for (a, _), _ in items], dtype=np.int32)
    slot_b = np.array([sign_to_slot[b] for (_, b), _ in items], dtype=np.int32)
    item_lipi = np.array([bg_lipi.get(k, 0) for k, _ in items], dtype=np.int32)
    item_new = np.array([bg_new.get(k, 0) for k, _ in items], dtype=np.int32)

    obs_wids = match_mat[slot_a, slot_b]
    hm_obs = obs_wids > 0
    obs_words = len(np.unique(obs_wids[hm_obs])) if np.any(hm_obs) else 0
    obs_pairs = int(np.sum(hm_obs))
    obs_lm = int(np.sum(item_lipi[hm_obs])) if np.any(hm_obs) else 0
    obs_nm = int(np.sum(item_new[hm_obs])) if np.any(hm_obs) else 0

    matched_rows = []
    for idx in np.where(hm_obs)[0].tolist():
        (a, b), _ = items[idx]
        wid = int(obs_wids[idx])
        form, src, gloss, rpair = id_to_meta[wid]
        matched_rows.append({
            "pair": f"{a}-{b}",
            "roots": rpair,
            "matched_headword": form,
            "source": src,
            "gloss": gloss,
            "lipi_mass": int(item_lipi[idx]),
            "new_mass": int(item_new[idx]),
        })
    matched_rows.sort(key=lambda x: (-x["lipi_mass"], -x["new_mass"], x["pair"]))

    p_words = np.zeros(N_PERM)
    p_pairs = np.zeros(N_PERM)
    p_lm = np.zeros(N_PERM)
    p_nm = np.zeros(N_PERM)
    fp = np.arange(n_tot, dtype=np.int32)
    for t in range(N_PERM):
        fp[:n_f] = rng.permutation(n_f)
        wids = match_mat[fp[slot_a], fp[slot_b]]
        hm = wids > 0
        if np.any(hm):
            p_words[t] = len(np.unique(wids[hm]))
            p_pairs[t] = int(np.sum(hm))
            p_lm[t] = int(np.sum(item_lipi[hm]))
            p_nm[t] = int(np.sum(item_new[hm]))

    return {
        "label": lex_label,
        "keep_vowel_length": keep_vowel_len,
        "dictionary_size": len(dict_map),
        "n_bigrams_tested": len(items),
        "obs_words": obs_words,
        "obs_pairs": obs_pairs,
        "obs_lipi_mass": obs_lm,
        "obs_new_mass": obs_nm,
        "perm_words": p_and_z(obs_words, p_words),
        "perm_pairs": p_and_z(obs_pairs, p_pairs),
        "perm_lipi_mass": p_and_z(obs_lm, p_lm),
        "perm_new_mass": p_and_z(obs_nm, p_nm),
        "top_matches": matched_rows[:40],
    }


# =============================================================================
# 6. MAIN DRIVER
# =============================================================================
def main():
    print("=" * 84)
    print("KEY #8B — TEST 8B-1: 4-TIER SANGAM / TAMIL-BRAHMI / CHOLA EPIGRAPHY (227 & 272 SIGNS)")
    print("=" * 84)
    rng = np.random.default_rng(RNG_SEED)

    # Verify master lexicon sizes on disk
    with LEX6A_PATH.open(encoding="utf-8") as f:
        s163_disk = {r["sign"].strip() for r in csv.DictReader(f)}
    with LEX7A_PATH.open(encoding="utf-8") as f:
        s227_disk = {r["sign"].strip() for r in csv.DictReader(f)}
    with LEX8A_PATH.open(encoding="utf-8") as f:
        r8_disk = list(csv.DictReader(f))
    s272_disk = {r["sign"].strip() for r in r8_disk}
    s266_strict_disk = {r["sign"].strip() for r in r8_disk if r["is_phonetic_locked"] == "True"}
    assert len(s163_disk) == 163
    assert len(s227_disk) == 227
    assert len(s272_disk) == 272
    assert len(s266_strict_disk) == 266

    smap_227 = {k: v[0] for k, v in LEX_227.items()}
    smap_272 = {k: v[0] for k, v in LEX_272.items()}
    diac_227 = {k: v[1] for k, v in LEX_227.items()}
    diac_272 = {k: v[1] for k, v in LEX_272.items()}
    fam_227 = {k: v[2] for k, v in LEX_227.items()}
    fam_272 = {k: v[2] for k, v in LEX_272.items()}
    assert len(smap_227) + len(NUMS_DRAV_227) == 220, f"Expected 220 phonetic in Key 7A, got {len(smap_227) + len(NUMS_DRAV_227)}"
    assert len(smap_272) + len(NUMS_DRAV_272) == 262, f"Expected 262 phonetic in Key 8A, got {len(smap_272) + len(NUMS_DRAV_272)}"

    smap_ia_227 = {k: SIGN_IA_272[k] for k in smap_227}
    smap_sum_227 = {k: SIGN_SUM_272[k] for k in smap_227}
    nmap_ia_227 = {k: NUMS_IA_272[k] for k in NUMS_DRAV_227}
    nmap_sum_227 = {k: NUMS_SUM_272[k] for k in NUMS_DRAV_227}
    smap_ia_272 = {k: SIGN_IA_272[k] for k in smap_272}
    smap_sum_272 = {k: SIGN_SUM_272[k] for k in smap_272}

    obj_split824 = load_split824()

    # Load 2-branch DEDR root pool for random equal-length draws
    all_2branch = load_raw_dedr_2branch()
    by_len_dedr: dict[int, list[str]] = defaultdict(list)
    seen_r: set[str] = set()
    for _, r_asc, r_len in all_2branch:
        if r_asc not in seen_r:
            seen_r.add(r_asc)
            by_len_dedr[r_len].append(r_asc)

    # Load exact frozen 170 pure Dravidian + 30 Prakrit loans from Key #7B CSV (unchanged!)
    frozen_170_pure = []
    frozen_30_loans = []
    with FROZEN_170_PATH.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tup = (
                r["id"], r["form"], r["category"], r["etymology_layer"],
                r["dedr_id"], r["components"], r["gloss"], r["attestation_source"],
            )
            if r["etymology_layer"] == "pure_dravidian":
                frozen_170_pure.append(tup)
            else:
                frozen_30_loans.append(tup)
    assert len(frozen_170_pure) == 170, f"Expected 170 frozen pure Dravidian, got {len(frozen_170_pure)}"
    assert len(frozen_30_loans) == 30, f"Expected 30 frozen Prakrit loans, got {len(frozen_30_loans)}"

    # Load Key #4C rival IA (86) & Sumerian (86) from CSV, then filter additions against MW & Halloran on disk!
    k4c_ia = []
    k4c_sum = []
    with RIVAL_K4C_PATH.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tup = (r["id"], r["form"], r["epigraphic_form"], r["category"], r["gloss"], r["attestation_source"])
            if "IndoAryan" in r["tradition"]:
                k4c_ia.append(tup)
            else:
                k4c_sum.append(tup)

    mw_set: set[str] = set()
    with MW_PATH.open(encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if p:
                mw_set.add(strip_diacritics(p[0]))
    hall_set: set[str] = set()
    with HALL_PATH.open(encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if p:
                hall_set.add(strip_diacritics(re.sub(r"\d+", "", p[0])))

    # Tier-1 rival lexicons (exact Key #7B size: K4C + pre-Wave5 MW/Halloran verified)
    t1_ia = list(k4c_ia)
    seen_ia = {strip_diacritics(e[1]) for e in t1_ia}
    for e in RIVAL_IA_CANDIDATES:
        num = int(e[0][2:])
        if num <= 124:
            k1, k2 = strip_diacritics(e[1]), strip_diacritics(e[2])
            if (k1 in mw_set or k2 in mw_set) and k1 not in seen_ia:
                t1_ia.append(e)
                seen_ia.add(k1)

    t1_sum = list(k4c_sum)
    seen_sum = {strip_diacritics(re.sub(r"\d+", "", e[1])) for e in t1_sum}
    for e in RIVAL_SUM_CANDIDATES:
        num = int(e[0][3:])
        if num <= 93:
            k1 = strip_diacritics(re.sub(r"\d+", "", e[1]))
            if (k1 in hall_set or strip_diacritics(e[2]) in hall_set) and k1 not in seen_sum:
                t1_sum.append(e)
                seen_sum.add(k1)

    # Tier-2 expanded lexicons (+50 Pure Dravidian, +MW-verified IA, +Halloran-verified Ur III)
    t2_pure = frozen_170_pure + WAVE56_PURE_DRAVIDIAN_ADDITIONS
    t2_ia = list(t1_ia)
    for e in RIVAL_IA_CANDIDATES:
        num = int(e[0][2:])
        if num >= 125:
            k1, k2 = strip_diacritics(e[1]), strip_diacritics(e[2])
            if (k1 in mw_set or k2 in mw_set) and k1 not in seen_ia:
                t2_ia.append(e)
                seen_ia.add(k1)

    t2_sum = list(t1_sum)
    for e in RIVAL_SUM_CANDIDATES:
        num = int(e[0][3:])
        if num >= 94:
            k1 = strip_diacritics(re.sub(r"\d+", "", e[1]))
            if (k1 in hall_set or strip_diacritics(e[2]) in hall_set) and k1 not in seen_sum:
                t2_sum.append(e)
                seen_sum.add(k1)

    # Extract true-order bigrams for 227-sign (220 phonetic) and 272-sign (262 phonetic)
    allow_227 = set(smap_227) | set(NUMS_DRAV_227)
    allow_272 = set(smap_272) | set(NUMS_DRAV_272)
    bg227_lipi, n_lipi_recs = extract_bigrams(EVENTS_LIPI_PATH, allow_227, set(NUMS_DRAV_227), obj_split824)
    bg227_new, n_new_recs = extract_bigrams(EVENTS_NEW_PATH, allow_227, set(NUMS_DRAV_227), obj_split824)
    bg272_lipi, _ = extract_bigrams(EVENTS_LIPI_PATH, allow_272, set(NUMS_DRAV_272), obj_split824)
    bg272_new, _ = extract_bigrams(EVENTS_NEW_PATH, allow_272, set(NUMS_DRAV_272), obj_split824)

    bg227_lipi_rec = {k: v for k, v in bg227_lipi.items() if v >= 2}
    bg227_comb = Counter(bg227_lipi)
    bg227_comb.update(bg227_new)
    bg227_comb_rec = {k: v for k, v in bg227_comb.items() if v >= 2}

    bg272_lipi_rec = {k: v for k, v in bg272_lipi.items() if v >= 2}
    bg272_comb = Counter(bg272_lipi)
    bg272_comb.update(bg272_new)
    bg272_comb_rec = {k: v for k, v in bg272_comb.items() if v >= 2}

    # Build maps
    f170_a, f170_p = build_target_maps(frozen_170_pure)
    t2p_a, t2p_p = build_target_maps(t2_pure)
    loan_a, loan_p = build_target_maps(frozen_30_loans)
    t1ia_a, t1ia_p = build_target_maps(t1_ia, multi_col=True)
    t1su_a, t1su_p = build_target_maps(t1_sum, strip_digits=True)
    t2ia_a, t2ia_p = build_target_maps(t2_ia, multi_col=True)
    t2su_a, t2su_p = build_target_maps(t2_sum, strip_digits=True)

    # Wave sets for strict isolation
    W14_SET = set(LEX_163.keys()) | set(NUMS_DRAV_163.keys())
    W14_LEX = set(LEX_163.keys())

    # -------------------------------------------------------------------------
    # TIER 1: FROZEN 170-WORD ZERO-CIRCULARITY VALIDATION (227 & 272 SIGNS)
    # -------------------------------------------------------------------------
    print("\n--- TIER 1: FROZEN 170-WORD ZERO-CIRCULARITY BENCHMARK ---")
    c227_full = list(bg227_lipi_rec.items())
    c227_w5_ge1 = [(k, v) for k, v in bg227_lipi_rec.items() if (k[0] not in W14_SET or k[1] not in W14_SET)]
    c227_w5_both = [(k, v) for k, v in bg227_lipi_rec.items() if (k[0] not in W14_SET and k[1] not in W14_SET)]

    c272_full = list(bg272_lipi_rec.items())
    c272_comb_full = list(bg272_comb_rec.items())
    c272_w56_ge1 = [(k, v) for k, v in bg272_lipi_rec.items() if (k[0] not in W14_SET or k[1] not in W14_SET)]
    c272_w56_both = [(k, v) for k, v in bg272_lipi_rec.items() if (k[0] not in W14_SET and k[1] not in W14_SET)]
    c272_w56_ge1_comb = [(k, v) for k, v in bg272_comb_rec.items() if (k[0] not in W14_SET or k[1] not in W14_SET)]
    c272_w56_both_comb = [(k, v) for k, v in bg272_comb_rec.items() if (k[0] not in W14_SET and k[1] not in W14_SET)]

    t1_227_full = eval_with_perms_and_draws("t1_227_full_lipi_ge2", c227_full, smap_227, NUMS_DRAV_227, fam_227, f170_a, f170_p, dravidian_sandhi_joins_v2, bg227_lipi, bg227_new, rng, by_len_dedr=by_len_dedr)
    t1_227_w5_ge1 = eval_with_perms_and_draws("t1_227_w5_ge1_lipi_ge2", c227_w5_ge1, smap_227, NUMS_DRAV_227, fam_227, f170_a, f170_p, dravidian_sandhi_joins_v2, bg227_lipi, bg227_new, rng, fixed_lex_signs=W14_LEX, by_len_dedr=by_len_dedr)
    t1_227_w5_both = eval_with_perms_and_draws("t1_227_w5_both_lipi_ge2", c227_w5_both, smap_227, NUMS_DRAV_227, fam_227, f170_a, f170_p, dravidian_sandhi_joins_v2, bg227_lipi, bg227_new, rng, fixed_lex_signs=W14_LEX, by_len_dedr=by_len_dedr)

    t1_272_full = eval_with_perms_and_draws("t1_272_full_lipi_ge2", c272_full, smap_272, NUMS_DRAV_272, fam_272, f170_a, f170_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, by_len_dedr=by_len_dedr)
    t1_272_comb = eval_with_perms_and_draws("t1_272_full_comb_ge2", c272_comb_full, smap_272, NUMS_DRAV_272, fam_272, f170_a, f170_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, by_len_dedr=by_len_dedr)
    t1_272_w56_ge1 = eval_with_perms_and_draws("t1_272_w56_ge1_lipi_ge2", c272_w56_ge1, smap_272, NUMS_DRAV_272, fam_272, f170_a, f170_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, fixed_lex_signs=W14_LEX, by_len_dedr=by_len_dedr)
    t1_272_w56_both = eval_with_perms_and_draws("t1_272_w56_both_lipi_ge2", c272_w56_both, smap_272, NUMS_DRAV_272, fam_272, f170_a, f170_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, fixed_lex_signs=W14_LEX, by_len_dedr=by_len_dedr)

    # Prakrit 30-loan negative control (both 227 and 272!)
    prak_227_hits = match_detailed(c227_full, smap_227, NUMS_DRAV_227, loan_a, loan_p, dravidian_sandhi_joins_v2, bg227_lipi, bg227_new)
    prak_272_hits = match_detailed(c272_full, smap_272, NUMS_DRAV_272, loan_a, loan_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new)
    prak_272_comb_hits = match_detailed(c272_comb_full, smap_272, NUMS_DRAV_272, loan_a, loan_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new)

    def summarize_prak(hits):
        ws = sorted({h["entry"][1] for h in hits})
        return {
            "words": len(ws),
            "pairs": len(hits),
            "lipi_mass": sum(h["lipi_count"] for h in hits),
            "new_mass": sum(h["new_count"] for h in hits),
            "word_list": ws,
        }

    prak_ctrl = {
        "words": len({h["entry"][1] for h in prak_272_hits}),
        "pairs": len(prak_272_hits),
        "lipi_mass": sum(h["lipi_count"] for h in prak_272_hits),
        "new_mass": sum(h["new_count"] for h in prak_272_hits),
        "key7a_227_lipi_ge2": summarize_prak(prak_227_hits),
        "key8a_272_lipi_ge2": summarize_prak(prak_272_hits),
        "key8a_272_comb_ge2": summarize_prak(prak_272_comb_hits),
    }

    # Tier-1 Rival controls on 227 & 272
    t1_ia_227 = eval_with_perms_and_draws("t1_ia_227_lipi_ge2", c227_full, smap_ia_227, nmap_ia_227, fam_227, t1ia_a, t1ia_p, ia_sandhi_joins, bg227_lipi, bg227_new, rng)
    t1_sum_227 = eval_with_perms_and_draws("t1_sum_227_lipi_ge2", c227_full, smap_sum_227, nmap_sum_227, fam_227, t1su_a, t1su_p, sumerian_joins, bg227_lipi, bg227_new, rng)
    t1_ia_272 = eval_with_perms_and_draws("t1_ia_272_lipi_ge2", c272_full, smap_ia_272, NUMS_IA_272, fam_272, t1ia_a, t1ia_p, ia_sandhi_joins, bg272_lipi, bg272_new, rng)
    t1_sum_272 = eval_with_perms_and_draws("t1_sum_272_lipi_ge2", c272_full, smap_sum_272, NUMS_SUM_272, fam_272, t1su_a, t1su_p, sumerian_joins, bg272_lipi, bg272_new, rng)

    print(f"  [T1 227 Full] words={t1_227_full['obs_words']} pairs={t1_227_full['obs_pairs']} lipi={t1_227_full['obs_lipi_mass']} (P_perm={t1_227_full['perm_words']['p']:.5f}, P_draw={t1_227_full['dedr_draw_words']['p']:.5f})")
    print(f"  [T1 272 Full] words={t1_272_full['obs_words']} pairs={t1_272_full['obs_pairs']} lipi={t1_272_full['obs_lipi_mass']} (P_perm={t1_272_full['perm_words']['p']:.5f}, P_draw={t1_272_full['dedr_draw_words']['p']:.5f})")
    print(f"  [T1 272 W56>=1] words={t1_272_w56_ge1['obs_words']} pairs={t1_272_w56_ge1['obs_pairs']} lipi={t1_272_w56_ge1['obs_lipi_mass']} (P_perm={t1_272_w56_ge1['perm_words']['p']:.5f}, P_draw={t1_272_w56_ge1['dedr_draw_words']['p']:.5f})")
    print(f"  [T1 Prakrit 30 Loans] 227={prak_ctrl['key7a_227_lipi_ge2']['words']}/{prak_ctrl['key7a_227_lipi_ge2']['pairs']} | 272={prak_ctrl['words']}/{prak_ctrl['pairs']} | 272_comb={prak_ctrl['key8a_272_comb_ge2']['words']}/{prak_ctrl['key8a_272_comb_ge2']['pairs']}")
    print(f"  [T1 Rival IA 272 ({len(t1_ia)})] words={t1_ia_272['obs_words']} lipi={t1_ia_272['obs_lipi_mass']} (P_perm_w={t1_ia_272['perm_words']['p']:.5f}, P_perm_m={t1_ia_272['perm_lipi_mass']['p']:.5f})")
    print(f"  [T1 Rival SUM 272 ({len(t1_sum)})] words={t1_sum_272['obs_words']} lipi={t1_sum_272['obs_lipi_mass']} (P_perm_w={t1_sum_272['perm_words']['p']:.5f}, P_perm_m={t1_sum_272['perm_lipi_mass']['p']:.5f})")

    # -------------------------------------------------------------------------
    # TIER 2: EXPANDED STRICTLY-ATTESTED WAVE-5/6 COMPOUNDS w/ 1:1 RIVAL CONTROLS
    # -------------------------------------------------------------------------
    print("\n--- TIER 2: EXPANDED ATTESTED SANGAM/CHOLA WAVE-5/6 COMPOUNDS (1:1 RIVALS) ---")
    t2_227_full = eval_with_perms_and_draws("t2_227_full_lipi_ge2", c227_full, smap_227, NUMS_DRAV_227, fam_227, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg227_lipi, bg227_new, rng, by_len_dedr=by_len_dedr)
    t2_227_w5_ge1 = eval_with_perms_and_draws("t2_227_w5_ge1_lipi_ge2", c227_w5_ge1, smap_227, NUMS_DRAV_227, fam_227, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg227_lipi, bg227_new, rng, fixed_lex_signs=W14_LEX, by_len_dedr=by_len_dedr)
    t2_227_w5_both = eval_with_perms_and_draws("t2_227_w5_both_lipi_ge2", c227_w5_both, smap_227, NUMS_DRAV_227, fam_227, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg227_lipi, bg227_new, rng, fixed_lex_signs=W14_LEX, by_len_dedr=by_len_dedr)

    t2_272_full = eval_with_perms_and_draws("t2_272_full_lipi_ge2", c272_full, smap_272, NUMS_DRAV_272, fam_272, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, by_len_dedr=by_len_dedr)
    t2_272_comb = eval_with_perms_and_draws("t2_272_full_comb_ge2", c272_comb_full, smap_272, NUMS_DRAV_272, fam_272, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, by_len_dedr=by_len_dedr)
    t2_272_w56_ge1 = eval_with_perms_and_draws("t2_272_w56_ge1_lipi_ge2", c272_w56_ge1, smap_272, NUMS_DRAV_272, fam_272, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, fixed_lex_signs=W14_LEX, by_len_dedr=by_len_dedr)
    t2_272_w56_both = eval_with_perms_and_draws("t2_272_w56_both_lipi_ge2", c272_w56_both, smap_272, NUMS_DRAV_272, fam_272, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, fixed_lex_signs=W14_LEX, by_len_dedr=by_len_dedr)
    t2_272_w56_ge1_comb = eval_with_perms_and_draws("t2_272_w56_ge1_comb_ge2", c272_w56_ge1_comb, smap_272, NUMS_DRAV_272, fam_272, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, fixed_lex_signs=W14_LEX, by_len_dedr=by_len_dedr)

    # Tier-2 Rival controls (MW-verified IA & Halloran-verified Ur III)
    t2_ia_272 = eval_with_perms_and_draws("t2_ia_272_lipi_ge2", c272_full, smap_ia_272, NUMS_IA_272, fam_272, t2ia_a, t2ia_p, ia_sandhi_joins, bg272_lipi, bg272_new, rng)
    t2_ia_272_w56 = eval_with_perms_and_draws("t2_ia_272_w56_ge1_lipi_ge2", c272_w56_ge1, smap_ia_272, NUMS_IA_272, fam_272, t2ia_a, t2ia_p, ia_sandhi_joins, bg272_lipi, bg272_new, rng, fixed_lex_signs=W14_LEX)
    t2_sum_272 = eval_with_perms_and_draws("t2_sum_272_lipi_ge2", c272_full, smap_sum_272, NUMS_SUM_272, fam_272, t2su_a, t2su_p, sumerian_joins, bg272_lipi, bg272_new, rng)
    t2_sum_272_w56 = eval_with_perms_and_draws("t2_sum_272_w56_ge1_lipi_ge2", c272_w56_ge1, smap_sum_272, NUMS_SUM_272, fam_272, t2su_a, t2su_p, sumerian_joins, bg272_lipi, bg272_new, rng, fixed_lex_signs=W14_LEX)

    # Unseen New texts independent check (all >= 1)
    bg272_new_all = [(k, v) for k, v in bg272_new.items() if v >= 1]
    t2_new_hits = match_detailed(bg272_new_all, smap_272, NUMS_DRAV_272, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new)
    t2_new_w56_hits = [h for h in t2_new_hits if (h["a"] not in W14_SET or h["b"] not in W14_SET)]

    print(f"  Lexicons: Pure-Drav={len(t2_pure)} (170+{len(WAVE56_PURE_DRAVIDIAN_ADDITIONS)}) | MW-IA={len(t2_ia)} | Halloran-SUM={len(t2_sum)}")
    print(f"  [T2 227 Full] words={t2_227_full['obs_words']} pairs={t2_227_full['obs_pairs']} lipi={t2_227_full['obs_lipi_mass']} new={t2_227_full['obs_new_mass']} (z={t2_227_full['perm_words']['z']:+.2f}, P_perm={t2_227_full['perm_words']['p']:.5f}, P_draw={t2_227_full['dedr_draw_words']['p']:.5f})")
    print(f"  [T2 272 Full] words={t2_272_full['obs_words']} pairs={t2_272_full['obs_pairs']} lipi={t2_272_full['obs_lipi_mass']} new={t2_272_full['obs_new_mass']} (z={t2_272_full['perm_words']['z']:+.2f}, P_perm={t2_272_full['perm_words']['p']:.5f}, P_mass={t2_272_full['perm_lipi_mass']['p']:.5f}, P_draw={t2_272_full['dedr_draw_words']['p']:.5f})")
    print(f"  [T2 272 Comb] words={t2_272_comb['obs_words']} pairs={t2_272_comb['obs_pairs']} lipi={t2_272_comb['obs_lipi_mass']} new={t2_272_comb['obs_new_mass']} (z={t2_272_comb['perm_words']['z']:+.2f}, P_perm={t2_272_comb['perm_words']['p']:.5f})")
    print(f"  [T2 272 W56>=1] words={t2_272_w56_ge1['obs_words']} pairs={t2_272_w56_ge1['obs_pairs']} lipi={t2_272_w56_ge1['obs_lipi_mass']} new={t2_272_w56_ge1['obs_new_mass']} (z={t2_272_w56_ge1['perm_words']['z']:+.2f}, P_perm_w={t2_272_w56_ge1['perm_words']['p']:.5f}, P_perm_m={t2_272_w56_ge1['perm_lipi_mass']['p']:.5f}, P_draw={t2_272_w56_ge1['dedr_draw_words']['p']:.5f})")
    print(f"  [T2 272 W56_BOTH] words={t2_272_w56_both['obs_words']} pairs={t2_272_w56_both['obs_pairs']} lipi={t2_272_w56_both['obs_lipi_mass']} (P_perm_w={t2_272_w56_both['perm_words']['p']:.5f}, P_draw={t2_272_w56_both['dedr_draw_words']['p']:.5f})")
    print(f"  [T2 Rival IA 272] words={t2_ia_272['obs_words']} lipi={t2_ia_272['obs_lipi_mass']} (z={t2_ia_272['perm_words']['z']:+.2f}, P_w={t2_ia_272['perm_words']['p']:.5f}, P_m={t2_ia_272['perm_lipi_mass']['p']:.5f}) | W56: words={t2_ia_272_w56['obs_words']} (P_w={t2_ia_272_w56['perm_words']['p']:.5f})")
    print(f"  [T2 Rival SUM 272] words={t2_sum_272['obs_words']} lipi={t2_sum_272['obs_lipi_mass']} (z={t2_sum_272['perm_words']['z']:+.2f}, P_w={t2_sum_272['perm_words']['p']:.5f}, P_m={t2_sum_272['perm_lipi_mass']['p']:.5f}) | W56: words={t2_sum_272_w56['obs_words']} (P_w={t2_sum_272_w56['perm_words']['p']:.5f})")

    # -------------------------------------------------------------------------
    # TIER 3: NON-NUMERAL LEXICAL-LEXICAL ONLY (STRIP ALL NUMERALS!)
    # -------------------------------------------------------------------------
    print("\n--- TIER 3: NON-NUMERAL LEXICAL-LEXICAL ONLY (ZERO NUMERALS) ---")
    num_set_227 = set(NUMS_DRAV_227.keys())
    num_set_272 = set(NUMS_DRAV_272.keys())
    c227_lexonly = [(k, v) for k, v in bg227_lipi_rec.items() if k[0] not in num_set_227 and k[1] not in num_set_227]
    c272_lexonly = [(k, v) for k, v in bg272_lipi_rec.items() if k[0] not in num_set_272 and k[1] not in num_set_272]
    c272_lexonly_comb = [(k, v) for k, v in bg272_comb_rec.items() if k[0] not in num_set_272 and k[1] not in num_set_272]

    t3_drav_227_f170 = eval_with_perms_and_draws("t3_drav_227_frozen170_lexonly", c227_lexonly, smap_227, {}, fam_227, f170_a, f170_p, dravidian_sandhi_joins_v2, bg227_lipi, bg227_new, rng, by_len_dedr=by_len_dedr)
    t3_drav_272_f170 = eval_with_perms_and_draws("t3_drav_272_frozen170_lexonly", c272_lexonly, smap_272, {}, fam_272, f170_a, f170_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, by_len_dedr=by_len_dedr)
    t3_drav_272_t2 = eval_with_perms_and_draws("t3_drav_272_expanded_lexonly", c272_lexonly, smap_272, {}, fam_272, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, by_len_dedr=by_len_dedr)
    t3_drav_272_t2_comb = eval_with_perms_and_draws("t3_drav_272_expanded_lexonly_comb", c272_lexonly_comb, smap_272, {}, fam_272, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new, rng, by_len_dedr=by_len_dedr)
    t3_ia_272_t2 = eval_with_perms_and_draws("t3_ia_272_lexonly", c272_lexonly, smap_ia_272, {}, fam_272, t2ia_a, t2ia_p, ia_sandhi_joins, bg272_lipi, bg272_new, rng)
    t3_sum_272_t2 = eval_with_perms_and_draws("t3_sum_272_lexonly", c272_lexonly, smap_sum_272, {}, fam_272, t2su_a, t2su_p, sumerian_joins, bg272_lipi, bg272_new, rng)

    print(f"  [T3 Drav 272 Frozen170 Lex-Only] words={t3_drav_272_f170['obs_words']} lipi={t3_drav_272_f170['obs_lipi_mass']} (z={t3_drav_272_f170['perm_words']['z']:+.2f}, P_w={t3_drav_272_f170['perm_words']['p']:.5f}, P_m={t3_drav_272_f170['perm_lipi_mass']['p']:.5f})")
    print(f"  [T3 Drav 272 Expanded Lex-Only]  words={t3_drav_272_t2['obs_words']} lipi={t3_drav_272_t2['obs_lipi_mass']} (z={t3_drav_272_t2['perm_words']['z']:+.2f}, P_w={t3_drav_272_t2['perm_words']['p']:.5f}, P_m={t3_drav_272_t2['perm_lipi_mass']['p']:.5f})")
    print(f"  [T3 MW IA 272 Lex-Only]          words={t3_ia_272_t2['obs_words']} lipi={t3_ia_272_t2['obs_lipi_mass']} (z={t3_ia_272_t2['perm_words']['z']:+.2f}, P_w={t3_ia_272_t2['perm_words']['p']:.5f}, P_m={t3_ia_272_t2['perm_lipi_mass']['p']:.5f})")
    print(f"  [T3 Halloran SUM 272 Lex-Only]   words={t3_sum_272_t2['obs_words']} lipi={t3_sum_272_t2['obs_lipi_mass']} (z={t3_sum_272_t2['perm_words']['z']:+.2f}, P_w={t3_sum_272_t2['perm_words']['p']:.5f}, P_m={t3_sum_272_t2['perm_lipi_mass']['p']:.5f})")

    # -------------------------------------------------------------------------
    # TIER 4: AUTOMATED UNCURATED PHONEME-PRESERVING DICTIONARY CHECK
    # -------------------------------------------------------------------------
    print("\n--- TIER 4: AUTOMATED UNCURATED PHONEME-PRESERVING DICTIONARY CHECK ---")
    dict_strict: dict[str, tuple[str, str, str]] = {}
    dict_cplace: dict[str, tuple[str, str, str]] = {}
    for src_tag, pth in [("DEDR", DEDR_TAMIL_PATH), ("WIKT", WIKT_TAMIL_PATH)]:
        with pth.open(encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 5:
                    continue
                hw = parts[1].strip()
                gloss = parts[4].strip()[:90]
                src_id = f"DEDR:{parts[0]}" if src_tag == "DEDR" else "WIKT"
                ks = phon_preserve_norm(hw, keep_vowel_len=True)
                kc = phon_preserve_norm(hw, keep_vowel_len=False)
                if len(ks) >= 5 and ks not in dict_strict:
                    dict_strict[ks] = (src_id, hw, gloss)
                if len(kc) >= 5 and kc not in dict_cplace:
                    dict_cplace[kc] = (src_id, hw, gloss)

    diac_nmap_227 = {k: NUMS_DIAC_272[k] for k in NUMS_DRAV_227}
    diac_nmap_272 = {k: NUMS_DIAC_272[k] for k in NUMS_DRAV_272}

    t4_227_strict = run_tier4_automated("t4_227_uncurated_exact_phoneme", diac_227, diac_nmap_227, fam_227, c227_full, bg227_lipi, bg227_new, dict_strict, True, rng)
    t4_272_strict = run_tier4_automated("t4_272_uncurated_exact_phoneme", diac_272, diac_nmap_272, fam_272, c272_full, bg272_lipi, bg272_new, dict_strict, True, rng)
    t4_272_cplace = run_tier4_automated("t4_272_uncurated_consonant_place", diac_272, diac_nmap_272, fam_272, c272_full, bg272_lipi, bg272_new, dict_cplace, False, rng)
    t4_272_lexonly_strict = run_tier4_automated("t4_272_uncurated_exact_phoneme_lexonly", diac_272, {}, fam_272, c272_lexonly, bg272_lipi, bg272_new, dict_strict, True, rng)

    for res4 in (t4_227_strict, t4_272_strict, t4_272_cplace, t4_272_lexonly_strict):
        print(
            f"  [{res4['label']:38s}] words={res4['obs_words']:2d} pairs={res4['obs_pairs']:2d} "
            f"lipi={res4['obs_lipi_mass']:3d} (null_w={res4['perm_words']['mean']:.2f}, z={res4['perm_words']['z']:+.2f}, "
            f"P_w={res4['perm_words']['p']:.5f}, P_m={res4['perm_lipi_mass']['p']:.5f})"
        )

    # -------------------------------------------------------------------------
    # EXPORT COMPOUND MATCHES CSV (`work_data/key8b/test8b1_compound_matches_key8.csv`)
    # -------------------------------------------------------------------------
    hits_t2_comb = match_detailed(c272_comb_full, smap_272, NUMS_DRAV_272, t2p_a, t2p_p, dravidian_sandhi_joins_v2, bg272_lipi, bg272_new)
    frozen_id_set = {e[0] for e in frozen_170_pure}
    csv_path = OUT_DIR / "test8b1_compound_matches_key8.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "pair", "roots", "matched_compound", "category", "origin_lexicon",
            "wave_cut", "is_non_numeral", "lipi_texts", "unseen_new_texts", "comb_texts",
            "dedr_id", "gloss", "attestation_source",
        ])
        for h in sorted(hits_t2_comb, key=lambda x: (-x["lipi_count"], -x["new_count"], x["pair"])):
            ent = h["entry"]
            orig = "Tier1_Frozen170" if ent[0] in frozen_id_set else "Tier2_Wave56_Expanded"
            in_w56_a = h["a"] not in W14_SET
            in_w56_b = h["b"] not in W14_SET
            if in_w56_a and in_w56_b:
                wcut = "BOTH_WAVES_5_6"
            elif in_w56_a or in_w56_b:
                wcut = "ONE_WAVE_5_6"
            else:
                wcut = "WAVES_1_4_ONLY"
            is_non_num = (h["a"] not in num_set_272) and (h["b"] not in num_set_272)
            w.writerow([
                h["pair"], h["roots"], ent[1], ent[2], orig, wcut, is_non_num,
                h["lipi_count"], h["new_count"], h["lipi_count"] + h["new_count"],
                ent[4], ent[6], ent[7],
            ])
    print(f"\n[CSV] Wrote {csv_path} ({len(hits_t2_comb)} matched pairs)")

    # Build Wave-5/6 novel compound summary table
    w56_by_word: dict[str, list[dict]] = defaultdict(list)
    for h in hits_t2_comb:
        if (h["a"] not in W14_SET) or (h["b"] not in W14_SET):
            w56_by_word[h["entry"][1]].append(h)
    w56_compound_table = []
    for w_name, hs in sorted(w56_by_word.items(), key=lambda kv: -sum(x["lipi_count"] + x["new_count"] for x in kv[1])):
        ent = hs[0]["entry"]
        w56_compound_table.append({
            "compound": w_name,
            "origin": "Tier1_Frozen170" if ent[0] in frozen_id_set else "Tier2_Wave56_Expanded",
            "both_w56": any((x["a"] not in W14_SET and x["b"] not in W14_SET) for x in hs),
            "non_numeral": any((x["a"] not in num_set_272 and x["b"] not in num_set_272) for x in hs),
            "lipi_mass": sum(x["lipi_count"] for x in hs),
            "new_mass": sum(x["new_count"] for x in hs),
            "pairs": ", ".join(f"{x['pair']}({x['lipi_count']}/{x['new_count']})" for x in sorted(hs, key=lambda z: -(z["lipi_count"] + z["new_count"]))),
            "dedr_id": ent[4],
            "gloss": ent[6],
            "source": ent[7],
        })

    # Assemble JSON matching verify_key8_e2e.py exact schema
    out_json = {
        "n_permutations": N_PERM,
        "rng_seed": RNG_SEED,
        "corpus_counts": {
            "lipi_records": n_lipi_recs,
            "new_records": n_new_recs,
            "key7a_signs_total": 227,
            "key7a_signs_phonetic": len(allow_227),
            "key8a_signs_total": 272,
            "key8a_signs_strict_locked": 266,
            "key8a_signs_phonetic": len(allow_272),
            "lipi_ge2_bigrams_227": len(bg227_lipi_rec),
            "lipi_ge2_bigrams_272": len(bg272_lipi_rec),
            "comb_ge2_bigrams_272": len(bg272_comb_rec),
        },
        "lexicon_sizes": {
            "tier1_frozen_pure_dravidian": len(frozen_170_pure),
            "tier1_quarantined_prakrit_loans": len(frozen_30_loans),
            "tier1_mw_rival_ia": len(t1_ia),
            "tier1_halloran_rival_sumerian": len(t1_sum),
            "tier2_expanded_pure_dravidian": len(t2_pure),
            "tier2_mw_rival_ia": len(t2_ia),
            "tier2_halloran_rival_sumerian": len(t2_sum),
            "tier4_uncurated_strict_phoneme_dict": len(dict_strict),
            "tier4_uncurated_cplace_dict": len(dict_cplace),
        },
        "headline_attested_compounds": t2_272_full["obs_words"],
        "headline_attested_compounds_comb": t2_272_comb["obs_words"],
        "prakrit_loan_control": prak_ctrl,
        "tier1_frozen_170": {
            "key7a_227_full_lipi_ge2": t1_227_full,
            "key7a_227_w5_ge1_lipi_ge2": t1_227_w5_ge1,
            "key7a_227_w5_both_lipi_ge2": t1_227_w5_both,
            "key8a_272_full_lipi_ge2": t1_272_full,
            "key8a_272_full_comb_ge2": t1_272_comb,
            "key8a_272_w56_ge1_lipi_ge2": t1_272_w56_ge1,
            "key8a_272_w56_both_lipi_ge2": t1_272_w56_both,
            "rival_ia_227": t1_ia_227,
            "rival_sumerian_227": t1_sum_227,
            "rival_ia_272": t1_ia_272,
            "rival_sumerian_272": t1_sum_272,
        },
        "tier2_expanded_attested_w56": {
            "key7a_227_full_lipi_ge2": t2_227_full,
            "key7a_227_w5_ge1_lipi_ge2": t2_227_w5_ge1,
            "key7a_227_w5_both_lipi_ge2": t2_227_w5_both,
            "key8a_272_full_lipi_ge2": t2_272_full,
            "key8a_272_full_comb_ge2": t2_272_comb,
            "key8a_272_w56_ge1_lipi_ge2": t2_272_w56_ge1,
            "key8a_272_w56_both_lipi_ge2": t2_272_w56_both,
            "key8a_272_w56_ge1_comb_ge2": t2_272_w56_ge1_comb,
            "rival_ia_272": t2_ia_272,
            "rival_ia_272_w56": t2_ia_272_w56,
            "rival_sumerian_272": t2_sum_272,
            "rival_sumerian_272_w56": t2_sum_272_w56,
            "unseen_new_full_272": {
                "words": len({h["entry"][1] for h in t2_new_hits}),
                "pairs": len(t2_new_hits),
                "new_mass": sum(h["new_count"] for h in t2_new_hits),
                "word_list": sorted({h["entry"][1] for h in t2_new_hits}),
            },
            "unseen_new_w56": {
                "words": len({h["entry"][1] for h in t2_new_w56_hits}),
                "pairs": len(t2_new_w56_hits),
                "new_mass": sum(h["new_count"] for h in t2_new_w56_hits),
                "word_list": sorted({h["entry"][1] for h in t2_new_w56_hits}),
            },
            "w56_compound_table": w56_compound_table,
        },
        "tier3_non_numeral_lexical_only": {
            "key7a_227_frozen170": t3_drav_227_f170,
            "key8a_272_frozen170": t3_drav_272_f170,
            "key8a_272_expanded": t3_drav_272_t2,
            "key8a_272_expanded_comb": t3_drav_272_t2_comb,
            "rival_ia_272_lexonly": t3_ia_272_t2,
            "rival_sumerian_272_lexonly": t3_sum_272_t2,
        },
        "tier4_automated_dedr_tamil_dict": {
            "key7a_227_exact_phoneme": t4_227_strict,
            "key8a_272_exact_phoneme": t4_272_strict,
            "key8a_272_consonant_place": t4_272_cplace,
            "key8a_272_exact_phoneme_lexonly": t4_272_lexonly_strict,
        },
    }

    json_path = OUT_DIR / "test8b1_sangam_227plus.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(out_json, f, indent=2, ensure_ascii=False)
    print(f"[JSON] Wrote {json_path}")
    print("[DONE] key8b_sangam_227plus.py completed cleanly!")


if __name__ == "__main__":
    main()
