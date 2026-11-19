#!/usr/bin/env python3
"""key2a_rebus_lock.py -- Key #2 Track A: Mainland Phonetic Sound-Lock Across 7 Cognate Families.

Three clean, pure-dictionary, zero-artifact tests (zero OCR/footnote/parenthetical leaks, zero
ALL-CAPS running page headers, zero English/German meta-headwords, zero prepositional-object gloss
leaks, zero vowel-drop onset distortions), evaluated across ALL 7 cognate language families
(Proto-Dravidian, Proto-Munda, OIA/Indo-Aryan, Elamite, Sumerian, Akkadian, Burushaski) plus 5
sensitivity/daughter audit lexicons, each with 5,000 exact derivational-cluster-preserving
sound-shuffled controls (vectorized via exact static homophone edge arrays for bit-for-bit exactness)
and domain/base-noun permutation controls, checked against the 7-family Bonferroni bar (P < 0.0071):

  Test A1: Expanded Multi-Sign Graphic Compound Rebus Lock
    - A1a: [Mod + 220 Fish] Strict Astral Double-Rebus across all 12 attested corpus modifiers
           (numerals 1..7 + graphic marks 415/rake-fork, 235/roof, 233/split, 226/cage, 240/wing)
           AND the 9 Unseen-Mahadevan-New-Texts-replicated subset. Base 220 must bridge strictly
           to ASTRAL/BRIGHTNESS (star/constellation/shine/glitter), tested under Phoneme-Exact
           (preserving retroflexes/coronals!) AND ASCII-Exact, vs 5,000 sound shuffles (P_sound)
           AND 5,000 random-picture-base draws (P_base).
    - A1b: Attested Astral Dictionary Compound Word Test for [Mod + Fish] (exact concatenation
           mod_stem + fish_stem -> strictly astral gloss in clean family pool, zero fuzzy substrings!).
    - A1c: All 10 Non-Fish 149-Set & Mark-Families Graphic Compounds (one_for_two.csv + mark_families.csv,
           verified on Lipi & unseen Mahadevan new texts).

  Test A2: Physical Anchors Dual-Domain Phonetic Bridge (sign_anchors.csv + blind pictures)
    - A2a: Full Automated TIER_1 + TIER_1B cross-domain bridge (all 51 non-ideogram signs, zero hand-picking).
    - A2b: Concrete Physical-Object Automated TIER_1 + TIER_1B subset (tight 3-5 word material glosses).
    - A2c: Clean Wave 2B 12-Sign Dual-Domain Anchor Set (zero gloss-phrase/OCR/ASCII artifacts).
    Each scored on Phoneme-Exact, Phoneme-Stem, ASCII-Exact, and Distinct-Sense Polysemy + Phoneme-Exact,
    vs 5,000 sound shuffles (P_sound) + 5,000 domain-B permutations (P_dom).

  Test A3: Expanded Bronze Age Meluhha / Indus Loanword Skeleton Lock
    - A3a: 10 Strictly Near Eastern / Mediterranean External Trade Loans (ellu, pīru/pīlu, tukkī,
           karpāsu, mēsu/musukkannu, uruda/werûm, dar-meluhha, qōp/uqūpu, óryza, koland-/kalam).
    - A3b: All 14 Bronze Age Indus Loans & Balanced Non-IE Rigvedic/Early-Vedic Substrate Words
           (+ khala, valaya, kuṇḍa, lāṅgala; self-sources strictly excluded from scoring!).
    - A3c: Strictly Sign-Anchored 8-Item Subset (the 8 loans mapped directly onto anchored Indus signs).

Outputs -> work_data/key2a/
"""

import os
import re
import sys
import csv
import json
import math
import time
import unicodedata
import collections
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_LEX = "/tmp/typo_lex"
OUT_DIR = os.path.join(ROOT, "work_data", "key2a")
os.makedirs(OUT_DIR, exist_ok=True)

N_SHUF = int(os.environ.get("KEY2A_NSHUF", 5000))
T0 = time.time()


def log(*args):
    print(f"[key2a {time.time() - T0:6.1f}s]", *args, flush=True)


# ==============================================================================
# 0. ZERO-ARTIFACT PHONOLOGICAL & GLOSS HYGIENE ENGINE
# ==============================================================================
CHAR_MAP = {
    'ŋ': 'ng', 'ə': 'a', 'ɛ': 'e', 'ɔ': 'o', 'ʃ': 's', 'ß': 'ss', 'ø': 'o', 'æ': 'ae',
    'ı': 'i', 'ł': 'l', 'đ': 'd', 'ʔ': '', 'ʼ': '', '¢': 'ng', '§': 's', 'ɨ': 'i',
    'ʌ': 'a', 'ɖ': 'd', 'ʈ': 't', 'ɳ': 'n', 'ɭ': 'l', 'ɽ': 'r', 'ʂ': 's', 'ç': 'c',
    'š': 's', 'ḫ': 'h', 'ĝ': 'g', 'ṯ': 't', 'ḏ': 'd', 'ẓ': 'z', 'ṣ': 's', 'ṭ': 't',
    'ḍ': 'd', 'ṇ': 'n', 'ṛ': 'r', 'ḷ': 'l', 'ṟ': 'r', 'ṉ': 'n', 'ḻ': 'l', 'ṅ': 'ng',
    'ñ': 'n', 'ś': 's', 'ṃ': 'm', 'ḥ': 'h', 'ɟ': 'j', 'ɲ': 'n',
}

# Phoneme-preserving map: keeps retroflexes, alveolars, palatals, sibilants, and uvulars DISTINCT!
# (Prevents fake Dravidian ASCII collisions like ur̤u/ūṟu/uru, kāl/kaḷ, aracu/aṟai, and OIA/Akk collisions.)
PHON_MAP = {
    'ṭ': 'T', 'ḍ': 'D', 'ṇ': 'N', 'ḷ': 'L', 'ḻ': 'Z', 'ṟ': 'R', 'ṉ': 'Q',
    'ṛ': 'R', 'ṣ': 'S', 'ś': 'C', 'š': 'S', 'ḫ': 'H', 'ĝ': 'G', 'ŋ': 'G', 'ṅ': 'G',
    'ñ': 'J', 'ɲ': 'J', 'ɖ': 'D', 'ʈ': 'T', 'ɳ': 'N', 'ɭ': 'L', 'ɽ': 'R', 'ʂ': 'S',
    'ʃ': 'S', 'ç': 'C', 'ṯ': 'T', 'ḏ': 'D', 'ẓ': 'Z', 'ḥ': 'H',
    'ə': 'a', 'ɛ': 'e', 'ɔ': 'o', 'ɨ': 'i', 'ʌ': 'a', 'ï': 'i', 'ë': 'e', 'ů': 'u',
    'ä': 'a', 'ö': 'o', 'ü': 'u', 'æ': 'a', 'ø': 'o', 'ß': 'ss', 'ʔ': '', 'ʼ': '',
}

BAD_HEADWORDS = {
    'to', 'be', 'of', 'in', 'on', 'at', 'by', 'or', 'and', 'the', 'an', 'id', 'cf', 'see',
    'var', 'pl', 'sg', 'lit', 'esp', 'fig', 'also', 'same', 'as', 'one', 'who', 'from',
    'with', 'for', 'not', 'no', 'so', 'do', 'go', 'up', 'out', 'make', 'have', 'give',
    'take', 'become', 'break', 'cut', 'cause', 'is', 'are', 'was', 'that', 'this', 'its',
    'mit', 'von', 'und', 'bei', 'der', 'die', 'das', 'dem', 'den', 'des', 'ein', 'eine',
    'aus', 'auf', 'fur', 'fuer', 'oder', 'auch', 'nicht', 'noch', 'wie', 'als', 'zur',
    'zum', 'nach', 'uber', 'ueber', 'unter', 'durch', 'aber', 'nur', 'sein', 'seine',
}

VOWELS = set("aeiou")


def norm_ascii(w):
    w = str(w).lower().strip().lstrip('*')
    w = ''.join(CHAR_MAP.get(c, c) for c in w)
    w = unicodedata.normalize('NFD', w)
    w = ''.join(c for c in w if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', w)


def norm_phon(w):
    """Phoneme-preserving normalizer: keeps consonant place/manner diacritics distinct (ṭ->T, ḷ->L,
    ḻ/r̤->Z, ṟ->R, ṇ->N, ṉ->Q, ś->C, ṣ/š->S, ḫ->H), folds vowel length (ā->a, ī->i, etc.)."""
    w = unicodedata.normalize('NFC', str(w).lower().strip().lstrip('*'))
    # Decomposed multi-codepoint DEDR consonants (e.g., r + combining diaeresis below \u0324 = r̤)
    w = (w.replace('r\u0324', 'Z').replace('r\u0323', 'R').replace('n\u0331', 'Q')
          .replace('r\u0331', 'R').replace('l\u0323', 'L').replace('t\u0323', 'T')
          .replace('d\u0323', 'D').replace('n\u0323', 'N').replace('s\u0323', 'S')
          .replace('s\u0301', 'C').replace('s\u030c', 'S').replace('h\u032e', 'H'))
    w = ''.join(PHON_MAP.get(c, c) for c in w)
    w = unicodedata.normalize('NFD', w)
    w = ''.join(c for c in w if not unicodedata.combining(c))
    return re.sub(r'[^a-zA-Z]', '', w)


def stem_key(k):
    """Conservative inflectional-tail stripped stem (works identically on ASCII or Phoneme keys!)."""
    if len(k) <= 3:
        return k
    kl = k.lower()
    for suf in ('am', 'um', 'im', 'ai'):
        if kl.endswith(suf) and len(k) - len(suf) >= 3:
            return k[:-len(suf)]
    if kl[-1] in 'aiu' and len(k) >= 4:
        return k[:-1]
    return k


def onset_skel_degem(nf):
    """Onset-preserving degeminated consonantal skeleton: NEVER drops an initial vowel into a fake
    consonant onset! Prefixes 'V' if word begins with a vowel (e.g., el -> 'Vl', akal -> 'Vkl')."""
    if not nf:
        return ""
    cons = re.sub(r'[aeiou]', '', nf)
    s = ('V' + cons) if nf[0] in VOWELS else cons
    if not s:
        return ""
    out = [s[0]]
    for c in s[1:]:
        if c != out[-1]:
            out.append(c)
    return ''.join(out)


def clean_gloss_clauses(raw_gl):
    """Strip parenthetical (...), unclosed trailing (..., bracketed [...], OCR junk, and
    prepositional object tails ('of a/an/the X', 'for catching X', 'in a X'), returning clean
    ';'-separated distinct senses."""
    g = str(raw_gl).replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    for _ in range(3):
        g = re.sub(r'\([^()]*\)', ' ', g)
        g = re.sub(r'\[[^\[\]]*\]', ' ', g)
    # Strip any unclosed trailing parenthetical/bracket fragment (e.g. Sumerian '(cf' or '('child' +')
    g = re.sub(r'[\(\[].*$', ' ', g)
    g = re.sub(r'\S*[£§¢~<>|{}]\S*', ' ', g)
    g = unicodedata.normalize('NFD', g.lower())
    g = ''.join(c for c in g if not unicodedata.combining(c)).replace('ß', 'ss')
    senses = []
    for seg in g.split(';'):
        seg = re.sub(r'\s+', ' ', seg).strip(' ,.:;-_')
        if len(seg) < 2:
            continue
        sub_cleaned = []
        for sub in seg.split(','):
            s = sub.strip()
            if not s:
                continue
            # Keep "kind/sort/species/variety of X" intact by deleting the classifier prefix first
            s = re.sub(r'\b(?:a\s+)?(?:kind|sort|species|variety|type|class)\s+of\s+', '', s)
            # Cut off prepositional/participial object tails ("for catching X", "of a/an/the X", "in a/an/the X")
            s = re.sub(
                r'\b(?:for|from|like|as|with|without|against|into|onto|upon|made\s+of|used\s+for|used\s+in|catching|resembling)\b.*',
                '', s
            )
            s = re.sub(r'\b(?:of|in|on|at|to)\s+(?:a|an|the|one|two|three)\b.*', '', s)
            s = re.sub(
                r'\b(?:mouth|flower|blossom|skin|shell|head|handle|juice|caste|color|colour|shape|size|sound|smell|'
                r'part|side|end|edge|top|bottom|back|front|middle|female|male|young|offspring|dimness|state|act|halter|'
                r'headstall|string|cord|rope|strap|thong)\s+of\b.*',
                '', s
            )
            s = s.strip(' ,.:;-_')
            if s:
                sub_cleaned.append(s)
        if sub_cleaned:
            senses.append(' , '.join(sub_cleaned))
    return senses


def build_fixed_pdrav_2branch():
    """Rebuild pdrav_2branch & pdrav_2lang directly from raw work_data/lexicons/dedr/dedr_entries.tsv
    fixing ONLY the 4 verified general parser bugs in typo_00_lexicons.py (zero hand-edited words!):
      (1) Split glued entries including '(a)/(b)' ONLY outside parentheses and NEVER after 's.v.'/'cf.'/'nos.'
          (recovers DEDR 1159 kaṇ 'eye', 1479 kāl 'leg/quarter', 5545 vēḷ 'chief' AND prevents splitting
          DEDR 1305 kalam inside '(s.v. 155 Ta. appam)', restoring 1305's Te./Br. cognates!).
      (2) Never overwrite a longer entry with a shorter cross-ref snippet.
      (3) Only exclude Sanskrit/Prakrit loans when '< Skt'/'< Pkt' appears in the primary header (first 120 chars),
          not when a trailing Kui compound cites '(cf. DBIA 122)' (restores DEDR 910 ēr̤u 'seven').
      (4) Preserve `prev` headword across empty morphological parenthetical chunks like `(-pp-, -tt-)` so
          subsequent `n. circle, bangle, bracelet` chunks attach to the headword (fixes DEDR 5313 vaḷai).
    """
    sys.path.insert(0, os.path.join(ROOT, "work_scripts"))
    import typo_00_lexicons as t0

    dedr_path = os.path.join(ROOT, "work_data", "lexicons", "dedr", "dedr_entries.tsv")
    # Split glued entries ONLY at top-level (outside parentheses) and never after s.v./cf./nos.
    glued_cand = re.compile(
        r'(?<=[.;])\s+(\d{1,4}[a-z]?)(?:\s*\([a-z]\))?\s+(?=(?:' + t0.LANGS_RE + r')\.\s)'
    )

    def split_top_level_glued(eid0, txt):
        """Return list of (eid, chunk_txt) splitting only when parenthesis depth == 0 and not preceded by s.v./cf."""
        cuts = []
        for m in glued_cand.finditer(txt):
            pos = m.start()
            prefix = txt[:pos]
            # Check paren depth
            if prefix.count('(') > prefix.count(')'):
                continue
            # Check if immediately preceded by s.v. / cf. / Cf. / nos. / no. / see
            tail = prefix[-18:].lower()
            if re.search(r'(?:s\.v\.|cf\.|nos?\.|see)\s*$', tail):
                continue
            cuts.append((pos, m.end(), m.group(1).strip()))
        if not cuts:
            return [(eid0, txt)]
        out = [(eid0, txt[:cuts[0][0]])]
        for idx, (_, end_pos, sub_eid) in enumerate(cuts):
            nxt_start = cuts[idx + 1][0] if idx + 1 < len(cuts) else len(txt)
            out.append((sub_eid, txt[end_pos:nxt_start]))
        return out

    raw_entries = collections.OrderedDict()
    with open(dedr_path, encoding="utf-8") as f:
        for line in f:
            eid, txt = line.rstrip("\n").split("\t", 1)
            eid = eid.strip()
            for sub_eid, sub_txt in split_top_level_glued(eid, txt):
                if sub_eid not in raw_entries or len(sub_txt) > len(raw_entries[sub_eid]):
                    raw_entries[sub_eid] = sub_txt

    uf = t0.UnionFind()
    rows_2br = []
    rows_2lg = []
    PRIO = ['Ta', 'Ma', 'Ka', 'Ko', 'Tu', 'Te', 'Kol', 'Pa', 'Ga', 'Go', 'Konḍa', 'Kui', 'Kur', 'Kuṛ', 'Malt', 'Br']

    for eid, full_txt in raw_entries.items():
        uf.find(eid)
        cf_clean = re.sub(r'(?:CDIAL|Voc\.|DED\(S|BSOAS)[^.;]*', '', full_txt)
        for m in re.finditer(r'(?:\b[Cc]f\.|\bs\.v\.)\s*(\d{1,4}[a-z]?(?:\s*,\s*\d{1,4}[a-z]?)*)', cf_clean):
            for num_tok in re.findall(r'\d{1,4}[a-z]?', m.group(1)):
                uf.union(eid, num_tok)

        main_txt = re.split(r'\s/\s*Cf\.|DED\(S|DEN\b|Previous Page', full_txt)[0]
        if re.search(r'<\s*(?:Skt|Pkt|IA)\b', main_txt[:120]):
            continue

        parts = t0.SPLIT_LANG.split(main_txt)
        branches = set()
        langs_seen = set()
        lang_forms = collections.defaultdict(list)
        first_gloss_any = None

        for i in range(1, len(parts) - 1, 2):
            lang, seg = parts[i], parts[i + 1]
            if lang in t0.BRANCH_OF:
                branches.add(t0.BRANCH_OF[lang])
                langs_seen.add(lang)
            seg_clean = re.sub(r'\([^()]{0,60}\)', ' ', seg)
            prev = None
            for chunk in seg_clean.split(';'):
                toks = chunk.strip().rstrip('.').split()
                if not toks:
                    continue
                if toks[0] in t0.POS_SET and prev:
                    forms, gl = prev, ' '.join(toks[1:])
                elif toks[0] in ('to', 'tr.', 'intr.') and prev:
                    # Continuation gloss after stripped stem paradigm like `(-pp-, -tt-) to surround (tr.)`
                    forms, gl = prev, ' '.join(toks)
                else:
                    forms = []
                    k = 0
                    while k < len(toks):
                        t = toks[k]
                        k += 1
                        last = not t.endswith(',')
                        for f_ in t.rstrip(',').split('/'):
                            if t0.WORDCH.match(f_) and f_ not in t0.POS_SET and norm_ascii(f_) not in BAD_HEADWORDS:
                                forms.append(f_)
                        if last:
                            break
                    gl = ' '.join(toks[k:])
                if not forms:
                    continue
                prev = forms
                gl_clean = gl.strip()
                if gl_clean and gl_clean != 'id' and first_gloss_any is None:
                    first_gloss_any = gl_clean
                for f_ in forms:
                    lang_forms[lang].append((f_, gl_clean))

        if not lang_forms or not first_gloss_any:
            continue

        root_hw = None
        core_forms = []
        gloss_parts = []
        for lg in PRIO:
            if lg in lang_forms:
                for f_, gl_ in lang_forms[lg]:
                    nf_f = norm_ascii(f_)
                    if len(nf_f) < 2 or nf_f in BAD_HEADWORDS:
                        continue
                    if root_hw is None:
                        root_hw = f_
                        core_forms.append(f_)
                    if lg in ('Ta', 'Ma', 'Ka', 'Te') and gl_ and gl_ != 'id':
                        if len(gloss_parts) < 5 and gl_ not in gloss_parts:
                            gloss_parts.append(gl_)
                        if len(nf_f) <= len(norm_ascii(root_hw)) + 1 and nf_f != norm_ascii(root_hw) and len(core_forms) < 2:
                            core_forms.append(f_)
                if root_hw is not None and len(gloss_parts) >= 2:
                    break
        if not root_hw:
            continue
        joined_gl = '; '.join(gloss_parts) if gloss_parts else first_gloss_any
        cid = uf.find(eid)
        if len(langs_seen) >= 2:
            for cf_hw in core_forms:
                nf_c = norm_ascii(cf_hw)
                rows_2lg.append((eid, cid, cf_hw, nf_c, re.sub(r'[aeiou]', '', nf_c), joined_gl))
        if len(branches) >= 2:
            for cf_hw in core_forms:
                nf_c = norm_ascii(cf_hw)
                rows_2br.append((eid, cid, cf_hw, nf_c, re.sub(r'[aeiou]', '', nf_c), joined_gl))

    for out_name, rlist in (("pdrav_2branch_fixed", rows_2br), ("pdrav_2lang_fixed", rows_2lg)):
        with open(os.path.join(TMP_LEX, f"{out_name}.tsv"), "w", encoding="utf-8") as fh:
            for r in rlist:
                fh.write("\t".join(r) + "\n")
    log(f"Built bug-fixed DEDR cognate lexicons: pdrav_2branch_fixed={len(rows_2br)} rows "
        f"({len({r[0] for r in rows_2br})} etyma), pdrav_2lang_fixed={len(rows_2lg)} rows ({len({r[0] for r in rows_2lg})} etyma)")


class CleanCognateLex:
    """Zero-artifact cognate lexicon with precomputed exact static homophone edge arrays for
    5,000x vectorized cluster-preserving sound shuffling."""

    def __init__(self, fam_label, dict_name, is_de=False):
        self.fam = fam_label
        self.dict_name = dict_name
        self.is_de = is_de
        path = os.path.join(TMP_LEX, f"{dict_name}.tsv")

        eid_data = collections.OrderedDict()
        dropped = collections.Counter()

        with open(path, encoding="utf-8") as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 6:
                    continue
                eid, cid, hw, _, _, gl = parts[:6]
                if hw.isupper() and len(hw) >= 2:
                    dropped['allcaps_header'] += 1
                    continue
                nf = norm_ascii(hw)
                ph = norm_phon(hw)
                hw_lo = hw.strip().lower().strip('*-.,;() ')
                if len(nf) < 2 or nf in BAD_HEADWORDS or hw_lo in BAD_HEADWORDS:
                    dropped['meta_hw'] += 1
                    continue
                senses = clean_gloss_clauses(gl)
                if not senses:
                    dropped['empty_gloss'] += 1
                    continue

                if eid not in eid_data:
                    eid_data[eid] = {
                        'eid': eid, 'cid': cid, 'hws': [],
                        'phons': [], 'phon_stems': [],
                        'asciis': [], 'ascii_stems': [],
                        'skels': [], 'senses': [],
                    }
                rec = eid_data[eid]
                if ph not in rec['phons']:
                    rec['hws'].append(hw)
                    rec['phons'].append(ph)
                    rec['phon_stems'].append(stem_key(ph))
                if nf not in rec['asciis']:
                    rec['asciis'].append(nf)
                    rec['ascii_stems'].append(stem_key(nf))
                    rec['skels'].append(onset_skel_degem(nf))
                for s in senses:
                    if s not in rec['senses']:
                        rec['senses'].append(s)

        self.etyma = list(eid_data.values())
        self.E = len(self.etyma)
        self.dropped = dict(dropped)

        self.eids = [e['eid'] for e in self.etyma]
        self.cids = [e['cid'] for e in self.etyma]
        cid_map = {c: idx for idx, c in enumerate(dict.fromkeys(self.cids))}
        self.cid_int = np.array([cid_map[c] for c in self.cids], dtype=np.int32)
        self.hws = [e['hws'][0] for e in self.etyma]
        self.phons = [e['phons'] for e in self.etyma]
        self.phon_stems = [e['phon_stems'] for e in self.etyma]
        self.asciis = [e['asciis'] for e in self.etyma]
        self.ascii_stems = [e['ascii_stems'] for e in self.etyma]
        self.skels = [e['skels'] for e in self.etyma]
        self.senses = [e['senses'] for e in self.etyma]

        # Build cluster-preserving permutation strata
        cid_groups = collections.OrderedDict()
        for i, c in enumerate(self.cids):
            cid_groups.setdefault(c, []).append(i)
        size_buckets = collections.defaultdict(list)
        for _, idxs in cid_groups.items():
            size_buckets[len(idxs)].append(idxs)
        self._perm_strata = [np.array(v, dtype=np.int32) for v in size_buckets.values() if len(v) >= 2]
        sing_idxs = [i for v in size_buckets.values() if len(v) == 1 for grp in v for i in grp]
        self._sing_idxs = np.array(sing_idxs, dtype=np.int32)

        # Precompute EXACT static undirected homophone edge lists (u < v) for all 4 resolutions!
        self.edges = {}
        self.key_maps = {}
        for mode, key_lists in (
            ('phon_exact', self.phons),
            ('phon_stem', self.phon_stems),
            ('ascii_exact', self.asciis),
            ('ascii_stem', self.ascii_stems),
        ):
            kmap = collections.defaultdict(list)
            for i, ks in enumerate(key_lists):
                for k in set(ks):
                    kmap[k].append(i)
            self.key_maps[mode] = kmap
            us, vs = [], []
            seen_pair = set()
            for idxs in kmap.values():
                if len(idxs) < 2:
                    continue
                m = len(idxs)
                for a in range(m):
                    u = idxs[a]
                    for b in range(a + 1, m):
                        v = idxs[b]
                        pair = (u, v) if u < v else (v, u)
                        if pair not in seen_pair:
                            seen_pair.add(pair)
                            us.append(pair[0])
                            vs.append(pair[1])
            self.edges[mode] = (np.array(us, dtype=np.int32), np.array(vs, dtype=np.int32))

    def make_cluster_perm(self, rng):
        """Return cluster-preserving bijection inv[0..E-1] mapping form-slot u -> etymon inv[u]."""
        perm = np.arange(self.E, dtype=np.int32)
        for src in self._perm_strata:
            dst = src[rng.permutation(len(src))]
            perm[src.ravel()] = dst.ravel()
        if len(self._sing_idxs) >= 2:
            perm[self._sing_idxs] = self._sing_idxs[rng.permutation(len(self._sing_idxs))]
        return perm

    def match_regex_per_sense(self, rx):
        res = []
        for ss in self.senses:
            hits = {k for k, s in enumerate(ss) if rx.search(s)}
            res.append(hits)
        return res

    def match_regex_bool(self, rx):
        return np.array([any(rx.search(s) for s in ss) for ss in self.senses], dtype=bool)

    def find_real_bridge(self, mode, maskA, maskB):
        """Find first real distinct-cluster homophone (ea, eb, shared_key) between maskA & maskB."""
        kmap = self.key_maps[mode]
        a_idxs = np.flatnonzero(maskA)
        b_idxs = set(np.flatnonzero(maskB).tolist())
        key_lists = {
            'phon_exact': self.phons, 'phon_stem': self.phon_stems,
            'ascii_exact': self.asciis, 'ascii_stem': self.ascii_stems,
        }[mode]
        for ea in a_idxs:
            ca = self.cid_int[ea]
            for k in key_lists[ea]:
                for eb in kmap.get(k, ()):
                    if eb in b_idxs and eb != ea and self.cid_int[eb] != ca:
                        return (int(ea), int(eb), k)
        return None


PRIMARY_7_FAMILIES = [
    ("Dravidian", "pdrav_2branch_fixed", False),
    ("Munda", "pmunda_cognates", False),
    ("Indo-Aryan", "oia_cognates", False),
    ("Elamite", "elamite_roots", True),
    ("Sumerian", "sumerian_roots", False),
    ("Akkadian", "akkadian_roots", False),
    ("Burushaski", "burushaski_all", False),
]

AUDIT_EXTRA_LEX = [
    ("Dravidian_RawPDrav", "pdrav_2branch", False),
    ("Dravidian_2Lang", "pdrav_2lang_fixed", False),
    ("Dravidian_Tamil", "dedr_tamil", False),
    ("Indo-Aryan_Turner", "oia_turner", False),
    ("Munda_Santali", "santali_campbell", False),
]

COMPOUND_POOLS = {
    "Dravidian": ["pdrav_2branch_fixed", "pdrav_2lang_fixed", "dedr_tamil", "tamil_wiktionary", "telugu_wiktionary"],
    "Dravidian_RawPDrav": ["pdrav_2branch", "dedr_tamil", "tamil_wiktionary", "telugu_wiktionary"],
    "Dravidian_2Lang": ["pdrav_2lang_fixed", "dedr_tamil", "tamil_wiktionary", "telugu_wiktionary"],
    "Munda": ["pmunda_cognates", "santali_campbell", "mundari_bhadra", "kharia_druart"],
    "Indo-Aryan": ["oia_cognates", "oia_turner", "sanskrit_mw"],
    "Elamite": ["elamite_roots", "elamite_hinzkoch"],
    "Sumerian": ["sumerian_roots", "sumerian_halloran", "sumerian_wiktionary"],
    "Akkadian": ["akkadian_roots"],
    "Burushaski": ["burushaski_all"],
}

NATIVE_NUMS = {
    "Dravidian": {1: ["oru", "onru"], 2: ["iru", "irantu"], 3: ["mu", "munru"], 4: ["nal", "nanku"], 5: ["ai", "aintu"], 6: ["aru"], 7: ["elu", "eru"]},
    "Dravidian_RawPDrav": {1: ["oru", "onru"], 2: ["iru", "irantu"], 3: ["mu", "munru"], 4: ["nal", "nanku"], 5: ["ai", "aintu"], 6: ["aru"], 7: ["elu", "eru"]},
    "Dravidian_2Lang": {1: ["oru", "onru"], 2: ["iru", "irantu"], 3: ["mu", "munru"], 4: ["nal", "nanku"], 5: ["ai", "aintu"], 6: ["aru"], 7: ["elu", "eru"]},
    "Dravidian_Tamil": {1: ["oru", "onru"], 2: ["iru", "irantu"], 3: ["mu", "munru"], 4: ["nal", "nanku"], 5: ["ai", "aintu"], 6: ["aru"], 7: ["elu", "eru"]},
    "Munda": {1: ["mid", "miad", "moy"], 2: ["bar", "barea", "ubar"], 3: ["pe", "pea", "upe"], 4: ["upun", "pon"], 5: ["mone", "moloi"], 6: ["turui", "tibru"], 7: ["eae", "gul"]},
    "Munda_Santali": {1: ["mid", "mit"], 2: ["bar", "barea"], 3: ["pe", "pea"], 4: ["pon", "ponea"], 5: ["mone"], 6: ["turui"], 7: ["eae", "eyae"]},
    "Indo-Aryan": {1: ["eka", "aika"], 2: ["dva", "dvi"], 3: ["tri", "trayas"], 4: ["catur"], 5: ["panca"], 6: ["sas", "sat"], 7: ["sapta"]},
    "Indo-Aryan_Turner": {1: ["eka", "aika"], 2: ["dva", "dvi"], 3: ["tri", "trayas"], 4: ["catur"], 5: ["panca"], 6: ["sas", "sat"], 7: ["sapta"]},
    "Elamite": {1: ["ki"], 2: ["mar", "nub"], 3: ["ziti"], 4: ["kut"], 5: ["pas"], 6: ["sak"], 7: ["sit"]},
    "Sumerian": {1: ["dis", "as", "ge"], 2: ["min"], 3: ["es"], 4: ["limmu"], 5: ["ia"], 6: ["as"], 7: ["imin"]},
    "Akkadian": {1: ["isten"], 2: ["sina"], 3: ["salas"], 4: ["erbe"], 5: ["hamis"], 6: ["sedis"], 7: ["sebe"]},
    "Burushaski": {1: ["hik", "hin", "han"], 2: ["altan", "alto"], 3: ["iski", "usko"], 4: ["walto", "walti"], 5: ["cundo"], 6: ["misindo", "bisindo"], 7: ["thalo"]},
}


def p_and_z(obs, null_arr):
    null_arr = np.asarray(null_arr, dtype=np.float64)
    mu = float(null_arr.mean())
    sd = float(null_arr.std(ddof=1)) if len(null_arr) > 1 else 0.0
    z = 0.0 if sd < 1e-12 else (obs - mu) / sd
    p = float((1.0 + np.sum(null_arr >= obs - 1e-12)) / (1.0 + len(null_arr)))
    return round(mu, 3), round(sd, 3), round(z, 3), round(p, 5)


def fisher_combined_p(p_list):
    """Exact Fisher combined chi-square p-value for independent tests (2k df, closed form for k=3)."""
    p_clean = [max(min(float(p), 1.0), 1e-12) for p in p_list]
    stat = -2.0 * sum(math.log(p) for p in p_clean)
    k = len(p_clean)
    # Upper-tail survival function of chi2(2k) = exp(-x/2) * sum_{j=0}^{k-1} (x/2)^j / j!
    half = stat / 2.0
    s = 0.0
    term = 1.0
    for j in range(k):
        if j > 0:
            term *= half / j
        s += term
    return round(stat, 3), round(min(1.0, math.exp(-half) * s), 6)


# ==============================================================================
# TEST A1: EXPANDED MULTI-SIGN GRAPHIC COMPOUND REBUS LOCK
# ==============================================================================
FISH_MODS_ALL12 = [
    ("1+220 (031/001)", True,  9, 4,  "num", r"\b(one|single)\b", r"\b(eins|ein)\b", 1),
    ("2+220 (032/002)", True,  77, 16,"num", r"\b(two|pair|double|twin)\b", r"\b(zwei|beide|paar)\b", 2),
    ("3+220 (003/033)", True,  23, 2, "num", r"\b(three|triple)\b", r"\b(drei)\b", 3),
    ("4+220 (004/034)", False, 6, 0,  "num", r"\b(four)\b", r"\b(vier)\b", 4),
    ("5+220 (005)",     False, 2, 0,  "num", r"\b(five)\b", r"\b(fuenf|funf)\b", 5),
    ("6+220 (016/006)", True,  17, 2, "num", r"\b(six)\b", r"\b(sechs)\b", 6),
    ("7+220 (017)",     False, 1, 0,  "num", r"\b(seven)\b", r"\b(sieben)\b", 7),
    ("415+220 (rake/fork/comb)", True, 87, 15, "pic", r"\b(rake|comb|fork|branch|prong|tine)\b", r"\b(rechen|kamm|gabel|zweig|ast)\b", None),
    ("235 (roof/hat+fish)",      True, 234, 28,"pic", r"\b(roof|cover|shelter|hat|shade|peak)\b", r"\b(dach|decke|schutz|hut|gipfel)\b", None),
    ("233 (split/cut+fish)",     True, 189, 24,"pic", r"\b(split|cleave|divide|halve|cut|slice)\b", r"\b(spalten|teilen|schneiden)\b", None),
    ("226 (cage/enclose+fish)",  True, 38, 8,  "pic", r"\b(cage|enclosure|box|frame|fence|pen)\b", r"\b(kafig|gehege|kasten|zaun)\b", None),
    ("240 (wing/fin+fish)",      True, 316, 40,"pic", r"\b(wing|fin|feather|ear|cheek)\b", r"\b(flugel|flosse|feder|ohr|wange)\b", None),
]

# STRICT astral/brightness target for BASE 220 (fish -> star/shine/glitter ONLY!)
BASE_ASTRAL_EN = re.compile(r"\b(star|stars|planet|constellation|asterism|shine|glitter|flash|sparkle|radiant)\b", re.I)
BASE_ASTRAL_DE = re.compile(r"\b(stern|gestirn|glanz|glanzen|leucht|funkel)\b", re.I)

# Modifier epithet target (astral/brightness/color/ruler — no bloated 'day/night/light/man'!)
MOD_CREST_EN = re.compile(
    r"\b(star|stars|planet|constellation|shine|bright|glitter|flash|black|dark|white|red|green|blue|gold|"
    r"chief|lord|king|ruler|sky|heaven|divine|sacred)\b", re.I
)
MOD_CREST_DE = re.compile(
    r"\b(stern|gestirn|glanz|hell|leucht|schwarz|dunkel|weiss|rot|grun|blau|gold|"
    r"herr|konig|furst|himmel|gott|heilig)\b", re.I
)

# Strictly astral gloss for attested dictionary compounds (A1b)
STRICT_ASTRAL_COMP_EN = re.compile(
    r"\b(star|stars|planet|constellation|asterism|pleiades|venus|mars|mercury|saturn|jupiter|ursa|comet|meteor|nakshatra)\b", re.I
)
STRICT_ASTRAL_COMP_DE = re.compile(r"\b(stern|gestirn|planet|komet)\b", re.I)

FISH_EN = re.compile(r"\b(fish|fishes|carp)\b", re.I)
FISH_DE = re.compile(r"\b(fisch|fische)\b", re.I)

NONFISH_COMPOUNDS = [
    ("741=740+400 (jar+comb)", 233, 30,
     r"\b(comb|rake|harrow)\b", r"\b(kamm|rechen)\b",
     r"\b(jar|pot|waterpot|pitcher)\b", r"\b(krug|topf|gefass)\b",
     r"\b(small|junior|servant|house|family|measure|portion)\b",
     r"\b(klein|diener|haus|familie|mass|anteil)\b"),
    ("705=700+1 (cup+1stroke)", 202, 32,
     r"\b(one|single|stick|line)\b", r"\b(eins|stab|linie)\b",
     r"\b(cup|bowl|jar|pot|vessel)\b", r"\b(becher|schale|krug|topf)\b",
     r"\b(ship|boat|measure|bushel|grain|threshing|port)\b",
     r"\b(schiff|boot|mass|getreide|korn|hafen)\b"),
    ("048=503+7 (hill+7)", 3, 0,
     r"\b(hill|mountain|peak|tent)\b", r"\b(berg|hugel|gipfel|zelt)\b",
     r"\b(seven)\b", r"\b(sieben)\b",
     r"\b(high|rise|great|chief|lord|citadel|fort)\b",
     r"\b(hoch|gross|herr|burg|festung)\b"),
    ("798/832=2+790 (2+leaf/eye)", 6, 0,
     r"\b(two|pair|double)\b", r"\b(zwei|paar)\b",
     r"\b(leaf|eye|seed|petal)\b", r"\b(blatt|auge|samen)\b",
     r"\b(bangle|bracelet|ring|circle|merchant|copper)\b",
     r"\b(ring|kreis|kaufmann|kupfer)\b"),
    ("804=803+740 (leaf-fork+jar)", 17, 4,
     r"\b(leaf|fork|branch|tree)\b", r"\b(blatt|gabel|zweig|baum)\b",
     r"\b(jar|pot|pitcher)\b", r"\b(krug|topf)\b",
     r"\b(house|family|field|crop|grain|allotment)\b",
     r"\b(haus|familie|feld|ernte|getreide)\b"),
    ("741=877+740 (window/diamond+jar)", 7, 3,
     r"\b(window|grid|diamond|net|eye)\b", r"\b(fenster|gitter|netz|auge)\b",
     r"\b(jar|pot|pitcher)\b", r"\b(krug|topf)\b",
     r"\b(house|palace|court|seal|measure|fort)\b",
     r"\b(haus|palast|hof|siegel|mass|stadt)\b"),
    ("073=255+070 (bird/fish+arrow/tree)", 7, 1,
     r"\b(bird|fowl|fish)\b", r"\b(vogel|fisch)\b",
     r"\b(arrow|spear|tree|dart)\b", r"\b(pfeil|speer|baum)\b",
     r"\b(chief|lord|prince|star|bright|hunter|noble)\b",
     r"\b(herr|furst|stern|waffe|jager)\b"),
    ("924=hat+923 (hat+horn/moon)", 9, 2,
     r"\b(hat|roof|cover|leaf)\b", r"\b(hut|dach|decke|blatt)\b",
     r"\b(horn|tusk|moon|crescent|bow)\b", r"\b(horn|zahn|mond|bogen)\b",
     r"\b(elephant|ivory|month|trade|foreign|merchant)\b",
     r"\b(elefant|elfenbein|monat|handel|fremd)\b"),
    ("125=man+bow (090+bow)", 55, 10,
     r"\b(bow|arrow|arc)\b", r"\b(bogen|pfeil)\b",
     r"\b(man|male|person|warrior)\b", r"\b(mann|mensch|krieger)\b",
     r"\b(guard|archer|hunter|chief|servant|agent|soldier)\b",
     r"\b(wachter|jager|herr|diener|soldat)\b"),
    ("142=man+staff (090+staff)", 79, 28,
     r"\b(staff|stick|rod|spear|arrow)\b", r"\b(stab|stock|speer|pfeil)\b",
     r"\b(man|male|person)\b", r"\b(mann|mensch)\b",
     r"\b(ruler|chief|king|officer|guard|overseer)\b",
     r"\b(herrscher|herr|konig|beamter|wachter)\b"),
]

# Pool of ~25 blind picture nouns for A1a random-base-noun control (P_base)
ALT_BASE_NOUNS = [
    ("man", r"\b(man|male|husband)\b", r"\b(mann|gatte)\b"),
    ("jar", r"\b(jar|pot|waterpot|pitcher)\b", r"\b(krug|topf)\b"),
    ("cup", r"\b(cup|bowl|goblet)\b", r"\b(becher|schale)\b"),
    ("comb", r"\b(comb|carding)\b", r"\b(kamm)\b"),
    ("rake", r"\b(rake|harrow)\b", r"\b(rechen|harke)\b"),
    ("ladder", r"\b(ladder|step|stair)\b", r"\b(leiter|stufe|treppe)\b"),
    ("box", r"\b(box|chest|casket)\b", r"\b(kasten|truhe)\b"),
    ("hill", r"\b(hill|mountain|peak)\b", r"\b(berg|hugel)\b"),
    ("roof", r"\b(roof|thatch|gable)\b", r"\b(dach)\b"),
    ("house", r"\b(house|dwelling|abode)\b", r"\b(haus|wohnung)\b"),
    ("leaf", r"\b(leaf|leaves|petal)\b", r"\b(blatt|laub)\b"),
    ("tree", r"\b(tree|shrub|bush)\b", r"\b(baum|strauch)\b"),
    ("bow", r"\b(bow|arc)\b", r"\b(bogen)\b"),
    ("arrow", r"\b(arrow|dart|spear)\b", r"\b(pfeil|speer)\b"),
    ("staff", r"\b(staff|stick|rod)\b", r"\b(stab|stock)\b"),
    ("wheel", r"\b(wheel|chariot|cart)\b", r"\b(rad|wagen)\b"),
    ("horn", r"\b(horn|tusk|antler)\b", r"\b(horn|zahn)\b"),
    ("grid", r"\b(grid|net|lattice|fence)\b", r"\b(gitter|netz|zaun)\b"),
    ("seed", r"\b(seed|kernel|grain)\b", r"\b(samen|kern|korn)\b"),
    ("bird", r"\b(bird|fowl|hen|cock)\b", r"\b(vogel|huhn)\b"),
    ("gate", r"\b(gate|door|portal)\b", r"\b(tor|tur)\b"),
    ("eye", r"\b(eye|eyes|pupil)\b", r"\b(auge|augen)\b"),
    ("hand", r"\b(hand|palm|arm)\b", r"\b(hand|arm)\b"),
    ("dog", r"\b(dog|hound)\b", r"\b(hund)\b"),
    ("bull", r"\b(bull|ox|cow)\b", r"\b(stier|ochse|rind)\b"),
]


def eval_edges_vectorized(L, mode, inA_mat, inB_mat, perm=None, excl_same_flag=None):
    """Exact vectorized distinct-cluster homophone check for K pairs simultaneously!
    inA_mat, inB_mat: bool arrays of shape (K, E).
    If excl_same_flag is True, an edge (ea, eb) cannot count if eb is also in inA_mat[k] (i.e. both fish).
    Returns bool array of length K."""
    U, V = L.edges[mode]
    K = inA_mat.shape[0]
    if len(U) == 0:
        return np.zeros(K, dtype=bool)
    if perm is None:
        eu, ev = U, V
    else:
        eu = perm[U]
        ev = perm[V]
    diff_c = (L.cid_int[eu] != L.cid_int[ev])
    if not np.any(diff_c):
        return np.zeros(K, dtype=bool)
    eu = eu[diff_c]
    ev = ev[diff_c]
    if excl_same_flag:
        # Both directions: (ea in A and eb in B and not eb in A) OR (eb in A and ea in B and not ea in A)
        a_u = inA_mat[:, eu]
        a_v = inA_mat[:, ev]
        b_u = inB_mat[:, eu]
        b_v = inB_mat[:, ev]
        return np.any((a_u & b_v & (~a_v)) | (a_v & b_u & (~a_u)), axis=1)
    else:
        return np.any((inA_mat[:, eu] & inB_mat[:, ev]) | (inA_mat[:, ev] & inB_mat[:, eu]), axis=1)


def run_test_a1(lex_map):
    log("=== TEST A1: EXPANDED MULTI-SIGN GRAPHIC COMPOUND REBUS LOCK ===")
    summary_rows = []
    match_rows = []

    # Preload clean STRICTLY ASTRAL compound dictionaries per family (zero ALL-CAPS / parentheticals!)
    astral_comp_cache = {}
    for fam_key, pool_names in COMPOUND_POOLS.items():
        is_de = (fam_key == "Elamite")
        ast_rx = STRICT_ASTRAL_COMP_DE if is_de else STRICT_ASTRAL_COMP_EN
        entries = []
        seen_nf = set()
        for dn in pool_names:
            p = os.path.join(TMP_LEX, f"{dn}.tsv")
            if not os.path.exists(p):
                continue
            with open(p, encoding="utf-8") as fh:
                for line in fh:
                    ps = line.rstrip("\n").split("\t")
                    if len(ps) < 6:
                        continue
                    hw, gl = ps[2], ps[5]
                    if hw.isupper() and len(hw) >= 2:
                        continue
                    nf = norm_ascii(hw)
                    if len(nf) < 5 or nf in BAD_HEADWORDS or nf in seen_nf:
                        continue
                    senses = clean_gloss_clauses(gl)
                    if not senses:
                        continue
                    cgl = ' ; '.join(senses)
                    if ast_rx.search(cgl):
                        seen_nf.add(nf)
                        entries.append((nf, hw, cgl))
        astral_comp_cache[fam_key] = entries

    for fam_label, L in lex_map.items():
        rng = np.random.default_rng(20261119)
        is_de = L.is_de
        fish_rx = FISH_DE if is_de else FISH_EN
        base_ast_rx = BASE_ASTRAL_DE if is_de else BASE_ASTRAL_EN
        mod_cr_rx = MOD_CREST_DE if is_de else MOD_CREST_EN

        is_fish = L.match_regex_bool(fish_rx)
        is_base_ast = L.match_regex_bool(base_ast_rx)
        is_mod_cr = L.match_regex_bool(mod_cr_rx)

        # Build matrix (13, E): row 0 = fish->base_astral, rows 1..12 = 12 modifiers->mod_crest
        inA = np.zeros((13, L.E), dtype=bool)
        inB = np.zeros((13, L.E), dtype=bool)
        inA[0] = is_fish
        inB[0] = is_base_ast
        new9_mask = np.array([m[1] for m in FISH_MODS_ALL12], dtype=bool)
        for k, (mlab, in_new, ln, nn, mkind, rx_en, rx_de, nval) in enumerate(FISH_MODS_ALL12):
            rx = re.compile(rx_de if is_de else rx_en, re.I)
            inA[k + 1] = L.match_regex_bool(rx)
            inB[k + 1] = is_mod_cr

        # Also prepare alternate picture base nouns for P_base control!
        alt_base_masks = []
        for (bn, rx_en, rx_de) in ALT_BASE_NOUNS:
            m = L.match_regex_bool(re.compile(rx_de if is_de else rx_en, re.I))
            if np.any(m):
                alt_base_masks.append(m)
        alt_mat_A = np.array(alt_base_masks, dtype=bool) if alt_base_masks else np.zeros((1, L.E), dtype=bool)
        alt_mat_B = np.broadcast_to(is_base_ast, alt_mat_A.shape)

        for mode in ('phon_exact', 'ascii_exact'):
            real_hits = eval_edges_vectorized(L, mode, inA, inB, perm=None, excl_same_flag=True)
            fish_ok = bool(real_hits[0])
            mod_hits = real_hits[1:]
            obs_all12 = int(mod_hits.sum()) if fish_ok else 0
            obs_new9 = int(mod_hits[new9_mask].sum()) if fish_ok else 0
            obs_mod_only = int(mod_hits.sum())

            # Record audited real matches
            if fish_ok:
                fb = L.find_real_bridge(mode, is_fish, is_base_ast & (~is_fish))
                for k, (mlab, in_new, ln, nn, mkind, rx_en, rx_de, nval) in enumerate(FISH_MODS_ALL12):
                    if mod_hits[k]:
                        mb = L.find_real_bridge(mode, inA[k + 1], is_mod_cr & (~inA[k + 1]))
                        if fb and mb:
                            match_rows.append({
                                'test': f'A1a_fish_astral_{mode}', 'family': fam_label, 'dict': L.dict_name,
                                'item': mlab, 'in_new_texts': int(in_new),
                                'mod_word': f"{L.hws[mb[0]]} ({L.eids[mb[0]]})", 'mod_gloss': L.senses[mb[0]][0][:85],
                                'mod_rebus': f"{L.hws[mb[1]]} ({L.eids[mb[1]]})", 'mod_rebus_gloss': L.senses[mb[1]][0][:85],
                                'base_word': f"{L.hws[fb[0]]} ({L.eids[fb[0]]})", 'base_rebus': f"{L.hws[fb[1]]} ({L.eids[fb[1]]})",
                                'base_rebus_gloss': L.senses[fb[1]][0][:85], 'shared_key': f"{mb[2]} + {fb[2]}",
                            })

            # 5,000 Vectorized Cluster-Preserving Sound Shuffles!
            sh_all12 = np.zeros(N_SHUF)
            sh_new9 = np.zeros(N_SHUF)
            sh_mod = np.zeros(N_SHUF)
            sh_fok = np.zeros(N_SHUF)
            for t in range(N_SHUF):
                p = L.make_cluster_perm(rng)
                h = eval_edges_vectorized(L, mode, inA, inB, perm=p, excl_same_flag=True)
                f_ = h[0]
                mh = h[1:]
                sh_fok[t] = float(f_)
                sh_mod[t] = float(mh.sum())
                if f_:
                    sh_all12[t] = float(mh.sum())
                    sh_new9[t] = float(mh[new9_mask].sum())

            # Random-base-noun control (fraction of alternate picture bases that bridge to astral!)
            alt_base_ok = eval_edges_vectorized(L, mode, alt_mat_A, alt_mat_B, perm=None, excl_same_flag=True)
            alt_rate = float(alt_base_ok.mean()) if len(alt_base_masks) > 0 else 0.0
            # Under random base + same 12 modifiers: P_base = P(random base hits astral) * 1 (exact!)
            p_base = round(alt_rate if obs_all12 > 0 else 1.0, 5)

            mu12, sd12, z12, p12 = p_and_z(obs_all12, sh_all12)
            mu9, sd9, z9, p9 = p_and_z(obs_new9, sh_new9)
            mum, sdm, zm, pm = p_and_z(obs_mod_only, sh_mod)
            summary_rows.append({
                'subtest': f'A1a_fish12_{mode}', 'family': fam_label, 'dict': L.dict_name, 'n_etyma': L.E,
                'tested': 12, 'obs': obs_all12, 'shuf_mean': mu12, 'z': z12, 'P_sound': p12,
                'obs_new9': obs_new9, 'shuf_mean_new9': mu9, 'P_sound_new9': p9,
                'fish_bridge': int(fish_ok), 'fish_shuf_rate': round(float(sh_fok.mean()), 4),
                'alt_base_astral_rate': round(alt_rate, 4), 'P_base_exact': p_base,
                'mod_only': obs_mod_only, 'mod_only_P': pm,
            })
            log(f"  [A1a {mode:11s} {fam_label:18s}] Fish12={obs_all12:2d}/12 (mu={mu12:.2f} z={z12:+.2f} Psnd={p12:.5f} | "
                f"fishRate={sh_fok.mean():.3f} altBaseRate={alt_rate:.3f}) | New9={obs_new9}/9 (Psnd={p9:.5f})")

        # ------------------------------------------------------------------
        # A1b: Attested STRICTLY ASTRAL Dictionary Compound Headwords ([Mod + Fish])
        # Exact concatenation mod_stem + fish_stem (ZERO fuzzy letter-dropping!), strictly astral gloss!
        # ------------------------------------------------------------------
        if fam_label in astral_comp_cache:
            comp_entries = astral_comp_cache[fam_label]
            # Index astral compounds by suffix len 3..5 -> set of exact prefixes
            ast_by_suf = collections.defaultdict(list)
            for c_nf, c_hw, c_gl in comp_entries:
                for slen in (3, 4, 5):
                    if len(c_nf) >= slen + 2:
                        ast_by_suf[c_nf[-slen:]].append((c_nf[:-slen], c_hw, c_gl))

            fish_eidxs = np.flatnonzero(is_fish)
            mod_eidxs_list = [np.flatnonzero(inA[k + 1]) for k in range(12)]
            # Pre-extract per-etymon stem sets (len >= 2 for mods, 3..5 for fish)
            e_f_stems = [{s for s in (L.asciis[i] + L.ascii_stems[i]) if 3 <= len(s) <= 5} for i in range(L.E)]
            e_m_stems = [{s for s in (L.asciis[i] + L.ascii_stems[i]) if len(s) >= 2} for i in range(L.E)]
            # Also map which etyma have ANY fish stem that appears as an astral suffix (huge speedup!)
            has_ast_suf = np.array([any(s in ast_by_suf for s in e_f_stems[i]) for i in range(L.E)], dtype=bool)

            # Expand modifier stems with standard native numeral stems for real check? NO — keep 100% pure
            # dictionary etyma so real and shuffle use the EXACT same mapping! (We also check native numerals in audit.)
            def eval_a1b(perm=None, record=False):
                # Map fish_eidxs -> form-slots via perm (if perm is inv, wait: perm[u]=e, or slot=perm[e])
                f_slots = fish_eidxs if perm is None else perm[fish_eidxs]
                f_slots = f_slots[has_ast_suf[f_slots]]
                if len(f_slots) == 0:
                    return 0, 0
                cand_pfxs = {}
                for fs_slot in f_slots:
                    for fs in e_f_stems[fs_slot]:
                        for pfx, chw, cgl in ast_by_suf.get(fs, ()):
                            cand_pfxs[pfx] = (fs, chw, cgl)
                if not cand_pfxs:
                    return 0, 0
                # Total distinct astral compounds ending in fish stem
                tot_ast_fish = len({v[1] for v in cand_pfxs.values()})
                hits = 0
                for k, me in enumerate(mod_eidxs_list):
                    if len(me) == 0:
                        continue
                    mslots = me if perm is None else perm[me]
                    found = None
                    for ms_slot in mslots:
                        for ms in e_m_stems[ms_slot]:
                            if ms in cand_pfxs:
                                found = (ms, cand_pfxs[ms])
                                break
                        if found:
                            break
                    if found:
                        hits += 1
                        if record:
                            ms, (fs, chw, cgl) = found
                            match_rows.append({
                                'test': 'A1b_attested_astral_compound', 'family': fam_label, 'dict': L.dict_name,
                                'item': FISH_MODS_ALL12[k][0], 'in_new_texts': int(FISH_MODS_ALL12[k][1]),
                                'mod_word': ms, 'mod_gloss': '', 'mod_rebus': chw, 'mod_rebus_gloss': cgl[:100],
                                'base_word': fs, 'base_rebus': chw, 'base_rebus_gloss': cgl[:100],
                                'shared_key': f"{ms}+{fs}={chw}",
                            })
                return hits, tot_ast_fish

            r_c, r_tot = eval_a1b(perm=None, record=True)
            sh_c = np.zeros(N_SHUF)
            sh_tot = np.zeros(N_SHUF)
            for t in range(N_SHUF):
                a_, b_ = eval_a1b(perm=L.make_cluster_perm(rng), record=False)
                sh_c[t], sh_tot[t] = a_, b_
            muc, sdc, zc, pc = p_and_z(r_c, sh_c)
            mut, sdt, zt, pt = p_and_z(r_tot, sh_tot)
            summary_rows.append({
                'subtest': 'A1b_attested_astral_comp12', 'family': fam_label, 'dict': L.dict_name, 'n_etyma': L.E,
                'tested': 12, 'obs': r_c, 'shuf_mean': muc, 'z': zc, 'P_sound': pc,
                'obs_new9': r_tot, 'shuf_mean_new9': mut, 'P_sound_new9': pt,
                'fish_bridge': int(r_tot > 0), 'fish_shuf_rate': round(float((sh_tot > 0).mean()), 4),
                'alt_base_astral_rate': 0.0, 'P_base_exact': 1.0,
                'mod_only': r_tot, 'mod_only_P': pt,
            })
            log(f"  [A1b AstralComp  {fam_label:18s}] Mod+Fish AstralComp={r_c}/12 (mu={muc:.3f} z={zc:+.2f} P={pc:.5f}) | "
                f"Total *-fish astral words={r_tot} (mu={mut:.2f} z={zt:+.2f} P={pt:.5f})")

        # ------------------------------------------------------------------
        # A1c: Non-Fish 149-Set & Mark-Families 10 Graphic Compounds
        # ------------------------------------------------------------------
        K_nf = len(NONFISH_COMPOUNDS)
        nf_inA = np.zeros((2 * K_nf, L.E), dtype=bool)
        nf_inB = np.zeros((2 * K_nf, L.E), dtype=bool)
        for k, (cid_lab, ln, nn, men, mde, ben, bde, ten, tde) in enumerate(NONFISH_COMPOUNDS):
            t_mask = L.match_regex_bool(re.compile(tde if is_de else ten, re.I))
            nf_inA[2 * k] = L.match_regex_bool(re.compile(mde if is_de else men, re.I))
            nf_inB[2 * k] = t_mask
            nf_inA[2 * k + 1] = L.match_regex_bool(re.compile(bde if is_de else ben, re.I))
            nf_inB[2 * k + 1] = t_mask

        for mode in ('phon_exact', 'ascii_exact'):
            rh = eval_edges_vectorized(L, mode, nf_inA, nf_inB, perm=None, excl_same_flag=True)
            obs_dual = int(np.sum(rh[0::2] & rh[1::2]))
            if obs_dual > 0:
                for k, (cid_lab, ln, nn, *_) in enumerate(NONFISH_COMPOUNDS):
                    if rh[2 * k] and rh[2 * k + 1]:
                        mb = L.find_real_bridge(mode, nf_inA[2 * k], nf_inB[2 * k] & (~nf_inA[2 * k]))
                        bb = L.find_real_bridge(mode, nf_inA[2 * k + 1], nf_inB[2 * k + 1] & (~nf_inA[2 * k + 1]))
                        if mb and bb:
                            match_rows.append({
                                'test': f'A1c_nonfish_{mode}', 'family': fam_label, 'dict': L.dict_name,
                                'item': cid_lab, 'in_new_texts': int(nn > 0),
                                'mod_word': f"{L.hws[mb[0]]} ({L.eids[mb[0]]})", 'mod_gloss': L.senses[mb[0]][0][:80],
                                'mod_rebus': f"{L.hws[mb[1]]} ({L.eids[mb[1]]})", 'mod_rebus_gloss': L.senses[mb[1]][0][:80],
                                'base_word': f"{L.hws[bb[0]]} ({L.eids[bb[0]]})", 'base_rebus': f"{L.hws[bb[1]]} ({L.eids[bb[1]]})",
                                'base_rebus_gloss': L.senses[bb[1]][0][:80], 'shared_key': f"{mb[2]} + {bb[2]}",
                            })
            sh_nf = np.zeros(N_SHUF)
            for t in range(N_SHUF):
                h = eval_edges_vectorized(L, mode, nf_inA, nf_inB, perm=L.make_cluster_perm(rng), excl_same_flag=True)
                sh_nf[t] = float(np.sum(h[0::2] & h[1::2]))
            mun, sdn, zn, pn = p_and_z(obs_dual, sh_nf)
            summary_rows.append({
                'subtest': f'A1c_nonfish10_{mode}', 'family': fam_label, 'dict': L.dict_name, 'n_etyma': L.E,
                'tested': K_nf, 'obs': obs_dual, 'shuf_mean': mun, 'z': zn, 'P_sound': pn,
                'obs_new9': 0, 'shuf_mean_new9': 0.0, 'P_sound_new9': 1.0,
                'fish_bridge': 0, 'fish_shuf_rate': 0.0, 'alt_base_astral_rate': 0.0, 'P_base_exact': 1.0,
                'mod_only': 0, 'mod_only_P': 1.0,
            })
            log(f"  [A1c {mode:11s} {fam_label:18s}] NonFish10 Dual={obs_dual:2d}/10 (mu={mun:.2f} z={zn:+.2f} Psnd={pn:.5f})")

    return summary_rows, match_rows


# ==============================================================================
# TEST A2: PHYSICAL ANCHORS DUAL-DOMAIN PHONETIC BRIDGE (ZERO GLOSS ARTIFACTS!)
# ==============================================================================
# Concrete physical-object/material domains (tight 3-5 word glosses!) vs broader site-mound domains
CONCRETE_DOMAINS = {
    "copper_tool_vs_all": (r"\b(copper|bronze|metal|blade|axe)\b", r"\b(kupfer|bronze|metall|klinge|axt)\b", {"axe", "hammer"}),
    "copper_tool_vs_ctab": (r"\b(copper|bronze|metal|ingot|weight)\b", r"\b(kupfer|bronze|metall|gewicht)\b", {"axe"}),
    "mtab_all": (r"\b(grain|barley|ration|allowance|measure)\b", r"\b(getreide|gerste|ration|lohn|mass)\b", {"cup", "jar", "bowl", "grain", "seed"}),
    "har_F_granary": (r"\b(grain|barley|granary|threshing|measure)\b", r"\b(getreide|gerste|speicher|mass)\b", {"grain", "seed"}),
    "tag_all": (r"\b(ship|boat|sail|seal|cargo)\b", r"\b(schiff|boot|segel|siegel|fracht)\b", {"ship", "boat", "sail"}),
    "circuit_maritime_coastal": (r"\b(ship|boat|sea|port|sail)\b", r"\b(schiff|boot|meer|hafen|segel)\b", {"ship", "boat", "fish"}),
    "site_chanhu_workshops": (r"\b(cotton|thread|yarn|cloth|bead)\b", r"\b(baumwolle|faden|garn|stoff|perle)\b", {"bead", "cloth"}),
    "ivory_bone_rod": (r"\b(ivory|tusk|bone|small|junior)\b", r"\b(elfenbein|zahn|knochen|klein|jung)\b", {"horn", "tusk", "staff"}),
    "pot_all": (r"\b(measure|capacity|bushel|oil|ration)\b", r"\b(mass|menge|ol|ration)\b", {"jar", "pot", "cup", "bowl"}),
    "ctab_elephant": (r"\b(elephant|ivory|tusk)\b", r"\b(elefant|elfenbein|zahn)\b", {"horn", "tusk", "elephant"}),
    "ctab_bull_gaur_unicorn": (r"\b(bull|cow|ox|cattle|copper)\b", r"\b(stier|rind|ochse|kupfer)\b", {"bull", "ox", "cow", "horn"}),
    "ctab_human_archer": (r"\b(archer|hunter|bowman|guard|month)\b", r"\b(jager|wachter|monat)\b", {"bow", "arrow", "man", "moon"}),
}

ALL_SOURCE_DOMAINS = dict(CONCRETE_DOMAINS)
ALL_SOURCE_DOMAINS.update({
    "copper_tablet_vs_all": (r"\b(field|allotment|share|portion|estate)\b", r"\b(feld|anteil|teil|besitz)\b", {"grid", "field", "square"}),
    "har_mound_AB": (r"\b(fort|citadel|palace|chief|bangle)\b", r"\b(burg|palast|herr|ring)\b", {"house", "tower"}),
    "md_citadel": (r"\b(fort|citadel|temple|priest|palace)\b", r"\b(burg|tempel|priester|palast)\b", {"house", "tower"}),
    "md_VS_MN_craft": (r"\b(dye|cloth|kiln|craft|workshop)\b", r"\b(farbe|stoff|handwerk|werkstatt)\b", {"jar", "pot"}),
    "md_HR_elite": (r"\b(house|family|lineage|merchant|chief)\b", r"\b(haus|familie|sippe|kaufmann|herr)\b", {"house", "man"}),
    "ctab_rhinoceros": (r"\b(star|bright|clan|lord|chief)\b", r"\b(stern|sippe|herr)\b", {"horn"}),
    "circuit_eastern_headwaters": (r"\b(wheat|grain|cotton|river|plough)\b", r"\b(weizen|getreide|fluss|pflug)\b", {"plant", "leaf"}),
    "circuit_overland_west_north": (r"\b(foreign|trade|merchant|caravan|copper)\b", r"\b(fremd|handel|kaufmann|kupfer)\b", {"hill"}),
    "circuit_gulf_oman": (r"\b(servant|agent|officer|foreign|ship)\b", r"\b(diener|beamter|fremd|schiff)\b", {"man", "ship"}),
})

PIC_NOUN_KW = {
    "man": (r"\b(man|male|husband|warrior)\b", r"\b(mann|gatte|krieger)\b"),
    "fish": (r"\b(fish|fishes|carp)\b", r"\b(fisch|fische)\b"),
    "jar": (r"\b(jar|pot|waterpot|pitcher|urn)\b", r"\b(krug|topf|urne)\b"),
    "cup": (r"\b(cup|bowl|goblet|pot)\b", r"\b(becher|schale|topf)\b"),
    "comb": (r"\b(comb|carding)\b", r"\b(kamm)\b"),
    "rake": (r"\b(rake|harrow)\b", r"\b(rechen|harke)\b"),
    "ladder": (r"\b(ladder|step|stair|rung)\b", r"\b(leiter|stufe|treppe)\b"),
    "box": (r"\b(box|chest|casket|coffer)\b", r"\b(kasten|truhe|kiste)\b"),
    "hill": (r"\b(hill|mountain|peak|mound)\b", r"\b(berg|hugel|gipfel)\b"),
    "roof": (r"\b(roof|thatch|gable|canopy)\b", r"\b(dach|decke)\b"),
    "tent": (r"\b(tent|hut|pavilion)\b", r"\b(zelt|hutte)\b"),
    "house": (r"\b(house|dwelling|abode)\b", r"\b(haus|wohnung)\b"),
    "leaf": (r"\b(leaf|leaves|petal|frond)\b", r"\b(blatt|blatter|laub)\b"),
    "tree": (r"\b(tree|shrub|bush|timber)\b", r"\b(baum|strauch|busch)\b"),
    "fork": (r"\b(fork|prong|branch|bough)\b", r"\b(gabel|zweig|ast)\b"),
    "bow": (r"\b(bow|arc)\b", r"\b(bogen)\b"),
    "arrow": (r"\b(arrow|dart|spear|lance)\b", r"\b(pfeil|speer|lanze)\b"),
    "staff": (r"\b(staff|stick|rod|club)\b", r"\b(stab|stock|keule)\b"),
    "wheel": (r"\b(wheel|chariot|cart|wagon)\b", r"\b(rad|wagen|karren)\b"),
    "sun": (r"\b(sun|sunshine)\b", r"\b(sonne)\b"),
    "moon": (r"\b(moon|crescent)\b", r"\b(mond)\b"),
    "horn": (r"\b(horn|tusk|antler)\b", r"\b(horn|zahn|geweih)\b"),
    "grid": (r"\b(grid|net|lattice|fence)\b", r"\b(gitter|netz|zaun)\b"),
    "window": (r"\b(window|aperture|lattice)\b", r"\b(fenster|offnung)\b"),
    "seed": (r"\b(seed|kernel|pip|grain)\b", r"\b(samen|kern|korn)\b"),
    "bird": (r"\b(bird|fowl|hen|cock)\b", r"\b(vogel|huhn)\b"),
    "flag": (r"\b(flag|banner|standard)\b", r"\b(fahne|banner)\b"),
    "shield": (r"\b(shield|buckler)\b", r"\b(schild)\b"),
    "gate": (r"\b(gate|door|portal)\b", r"\b(tor|tur)\b"),
    "hourglass": (r"\b(drum|waist|cone)\b", r"\b(trommel|kegel)\b"),
    "book": (r"\b(tablet|slab|board)\b", r"\b(tafel|brett)\b"),
}

CLEAN_WAVE2B_12 = [
    ("705", "measure/threshing/grain <-> ship/boat",
     r"\b(measure|bushel|threshing|grain|barley)\b", r"\b(mass|getreide|korn|gerste)\b",
     r"\b(ship|boat|canoe|raft|sailor|navigator)\b", r"\b(schiff|boot|kahn|segel)\b"),
    ("820", "wheel/cart <-> quarter/fourth/leg",
     r"\b(wheel|chariot|wagon|cart|spoke)\b", r"\b(rad|wagen|karren|speiche)\b",
     r"\b(quarter|fourth|fraction|precinct|leg|foot)\b", r"\b(viertel|bezirk|bein|fuss)\b"),
    ("220", "fish <-> star/constellation/shine",
     r"\b(fish|fishes|carp)\b", r"\b(fisch|fische)\b",
     r"\b(star|stars|constellation|planet|asterism|shine|glitter|flash)\b", r"\b(stern|gestirn|glanz|leucht)\b"),
    ("740", "water_jar/pot <-> house/family/lineage",
     r"\b(jar|pot|waterpot|pitcher|jug|urn)\b", r"\b(krug|topf|urne|gefass)\b",
     r"\b(house|household|family|lineage|clan|dwelling|abode)\b", r"\b(haus|familie|sippe|wohnung|heim)\b"),
    ("520", "spear/lance/dart <-> chief/ruler/prince",
     r"\b(spear|lance|javelin|dart|pike|trident)\b", r"\b(speer|lanze|spiess|pfeil)\b",
     r"\b(chief|chieftain|prince|king|ruler|lord|noble)\b", r"\b(furst|fuerst|herrscher|konig|herr)\b"),
    ("400", "comb/rake <-> small/junior/subordinate",
     r"\b(comb|rake|harrow|carding)\b", r"\b(kamm|rechen|harke)\b",
     r"\b(small|little|young|junior|minor|servant)\b", r"\b(klein|jung|knabe|diener)\b"),
    ("861", "enclosure/field/court <-> share/portion/weight/property",
     r"\b(enclosure|courtyard|court|plot|land|field)\b", r"\b(hof|feld|platz|gehege|land)\b",
     r"\b(share|portion|allotment|property|fraction|weight)\b", r"\b(anteil|teil|besitz|gewicht)\b"),
    ("320", "step/stair/ladder <-> allowance/ration/capacity_measure",
     r"\b(step|stair|ladder|rung|threshold|sill)\b", r"\b(stufe|treppe|leiter|schwelle)\b",
     r"\b(allowance|ration|measure|capacity|wage|stipend|weight)\b", r"\b(ration|lohn|mass|gewicht)\b"),
    ("090", "man/male/husband <-> servant/agent/governor/rule",
     r"\b(man|male|husband|warrior)\b", r"\b(mann|gatte|krieger)\b",
     r"\b(servant|slave|labourer|agent|manage|rule|governor|officer)\b", r"\b(diener|knecht|beamter|verwalter|herrschen)\b"),
    ("154", "carrying_pole/yoke <-> guard/protect/watch",
     r"\b(yoke|carrying|pole|shoulder|burden|load|porter)\b", r"\b(joch|stange|last|tragen|trager)\b",
     r"\b(guard|protect|watch|keeper|warder|defend|preserve|shelter)\b", r"\b(wachter|schutzen|huten|bewahren)\b"),
    ("850", "eye/sight/pupil <-> copper/bronze/metal/blade",
     r"\b(eye|eyes|sight|pupil|vision)\b", r"\b(auge|augen|blick)\b",
     r"\b(copper|bronze|metal|brass|ore|blade|axe|chisel)\b", r"\b(kupfer|bronze|metall|erz|klinge|axt)\b"),
    ("390", "tree/branch/bough <-> cotton/thread/cloth/yarn",
     r"\b(tree|shrub|bush|bough|branch|timber)\b", r"\b(baum|strauch|busch|zweig)\b",
     r"\b(cotton|thread|yarn|cloth|fibre|fiber|linen|textile)\b", r"\b(baumwolle|faden|garn|stoff|gewebe)\b"),
]


def build_auto_tier1_pairs(domain_dict):
    sa = list(csv.DictReader(open(os.path.join(ROOT, "work_data", "sem", "sign_anchors.csv"), encoding="utf-8")))
    sg = {r['sign']: r for r in csv.DictReader(open(os.path.join(ROOT, "work_data", "lang_m2", "signs.csv"), encoding="utf-8"))}
    pairs = []
    seen_sign = set()
    for r in sa:
        if r['anchor_tier'] not in ('TIER_1_NEW_REPLICATED', 'TIER_1B_MAH_FULL_REPLICATED'):
            continue
        s = r['sign']
        if s in seen_sign:
            continue
        pic = sg.get(s)
        if not pic or pic['level'] not in ('3of3', '2of3') or not pic['nouns']:
            continue
        src_dom = r['source_domain']
        if src_dom not in domain_dict:
            continue
        dom_en, dom_de, overlap_nouns = domain_dict[src_dom]
        # Take ONLY the first (primary) non-ideogram blind noun to prevent multi-noun OR inflation!
        nouns = [n for n in pic['nouns'].split(';') if n in PIC_NOUN_KW and n not in overlap_nouns]
        if not nouns:
            continue
        seen_sign.add(s)
        n0 = nouns[0]
        pairs.append((s, f"{n0} <-> {src_dom}", PIC_NOUN_KW[n0][0], PIC_NOUN_KW[n0][1], dom_en, dom_de))
    return pairs


def run_test_a2(lex_map):
    log("=== TEST A2: PHYSICAL ANCHORS DUAL-DOMAIN PHONETIC BRIDGE ===")
    auto_all = build_auto_tier1_pairs(ALL_SOURCE_DOMAINS)
    auto_conc = build_auto_tier1_pairs(CONCRETE_DOMAINS)
    log(f"  Auto-extracted TIER_1+1B pairs: All={len(auto_all)} | Concrete-Material={len(auto_conc)} | CleanWave2B=12")

    summary_rows = []
    match_rows = []

    suites = [
        ("A2a_AutoTier1_All51", auto_all),
        ("A2b_AutoTier1_Concrete", auto_conc),
        ("A2c_Wave2B_12_Clean", CLEAN_WAVE2B_12),
    ]

    for suite_name, pairs in suites:
        K = len(pairs)
        arK = np.arange(K)
        for fam_label, L in lex_map.items():
            rng = np.random.default_rng(20261122)
            is_de = L.is_de

            sA, sB = [], []
            inA = np.zeros((K, L.E), dtype=bool)
            inB = np.zeros((K, L.E), dtype=bool)
            for k, (sgn, plab, enA, deA, enB, deB) in enumerate(pairs):
                rxA = re.compile(deA if is_de else enA, re.I)
                rxB = re.compile(deB if is_de else enB, re.I)
                sa = L.match_regex_per_sense(rxA)
                sb = L.match_regex_per_sense(rxB)
                sA.append(sa)
                sB.append(sb)
                inA[k] = [bool(x) for x in sa]
                inB[k] = [bool(x) for x in sb]

            # Distinct-sense polysemy matrix (K x K) — invariant under sound shuffle, varies under P_dom!
            M_poly = np.zeros((K, K), dtype=bool)
            poly_eids = {}
            for ka in range(K):
                a_idxs = np.flatnonzero(inA[ka])
                for kb in range(K):
                    for ei in a_idxs:
                        if inB[kb, ei] and any(a != b for a in sA[ka][ei] for b in sB[kb][ei]):
                            M_poly[ka, kb] = True
                            if ka == kb:
                                poly_eids[ka] = int(ei)
                            break

            # Evaluate all 3 phonetic resolutions vectorized!
            res = {}
            for mode in ('phon_exact', 'phon_stem', 'ascii_exact'):
                real_h = eval_edges_vectorized(L, mode, inA, inB, perm=None, excl_same_flag=False)
                obs = int(real_h.sum())

                # Exact K x K domain bridge matrix for P_dom!
                U, V = L.edges[mode]
                M_dom = np.zeros((K, K), dtype=bool)
                if len(U) > 0:
                    diff_c = (L.cid_int[U] != L.cid_int[V])
                    eu, ev = U[diff_c], V[diff_c]
                    if len(eu) > 0:
                        # (K, M) @ (M, K) > 0 via integer matrix multiply!
                        Au = inA[:, eu].astype(np.int16)
                        Av = inA[:, ev].astype(np.int16)
                        Bu = inB[:, eu].astype(np.int16)
                        Bv = inB[:, ev].astype(np.int16)
                        M_dom = ((Au @ Bv.T) + (Av @ Bu.T)) > 0

                # 5,000 sound shuffles + 5,000 domain-B permutations!
                sh_snd = np.zeros(N_SHUF)
                sh_dom = np.zeros(N_SHUF)
                sh_pe_snd = np.zeros(N_SHUF)
                sh_pe_dom = np.zeros(N_SHUF)
                diag_poly = np.diag(M_poly)
                M_pe_dom = M_dom | M_poly
                for t in range(N_SHUF):
                    p = L.make_cluster_perm(rng)
                    h = eval_edges_vectorized(L, mode, inA, inB, perm=p, excl_same_flag=False)
                    sh_snd[t] = float(h.sum())
                    sh_pe_snd[t] = float(np.sum(h | diag_poly))
                    pb = rng.permutation(K)
                    sh_dom[t] = float(M_dom[arK, pb].sum())
                    sh_pe_dom[t] = float(M_pe_dom[arK, pb].sum())

                obs_pe = int(np.sum(real_h | diag_poly))
                res[mode] = (
                    obs, p_and_z(obs, sh_snd), p_and_z(obs, sh_dom),
                    obs_pe, p_and_z(obs_pe, sh_pe_snd), p_and_z(obs_pe, sh_pe_dom),
                    real_h,
                )

            # Record detailed audited matches for every sign hitting phon_exact, phon_stem, ascii_exact, or poly
            for k in range(K):
                for mode in ('phon_exact', 'phon_stem', 'ascii_exact'):
                    if res[mode][6][k]:
                        br = L.find_real_bridge(mode, inA[k], inB[k])
                        if br:
                            ea, eb, key = br
                            match_rows.append({
                                'suite': suite_name, 'family': fam_label, 'dict': L.dict_name,
                                'sign': pairs[k][0], 'pair': pairs[k][1], 'mode': mode.upper(), 'shared_key': key,
                                'word_A': f"{L.hws[ea]} ({L.eids[ea]})", 'gloss_A': ' ; '.join(L.senses[ea])[:105],
                                'word_B': f"{L.hws[eb]} ({L.eids[eb]})", 'gloss_B': ' ; '.join(L.senses[eb])[:105],
                            })
                            break
                else:
                    if k in poly_eids:
                        ea = poly_eids[k]
                        match_rows.append({
                            'suite': suite_name, 'family': fam_label, 'dict': L.dict_name,
                            'sign': pairs[k][0], 'pair': pairs[k][1], 'mode': 'DISTINCT_SENSE_POLYSEMY',
                            'shared_key': L.phons[ea][0],
                            'word_A': f"{L.hws[ea]} ({L.eids[ea]})", 'gloss_A': ' ; '.join(L.senses[ea])[:105],
                            'word_B': f"{L.hws[ea]} ({L.eids[ea]})", 'gloss_B': ' ; '.join(L.senses[ea])[:105],
                        })

            pe_o, pe_s, pe_d, ppe_o, ppe_s, ppe_d, _ = res['phon_exact']
            ps_o, ps_s, ps_d, _, _, _, _ = res['phon_stem']
            ae_o, ae_s, ae_d, ape_o, ape_s, ape_d, _ = res['ascii_exact']

            summary_rows.append({
                'suite': suite_name, 'family': fam_label, 'dict': L.dict_name, 'n_etyma': L.E, 'K_signs': K,
                'phon_exact': pe_o, 'pe_snd_mu': pe_s[0], 'pe_snd_z': pe_s[2], 'pe_snd_P': pe_s[3],
                'pe_dom_mu': pe_d[0], 'pe_dom_z': pe_d[2], 'pe_dom_P': pe_d[3],
                'phon_stem': ps_o, 'ps_snd_mu': ps_s[0], 'ps_snd_z': ps_s[2], 'ps_snd_P': ps_s[3],
                'ps_dom_P': ps_d[3],
                'ascii_exact': ae_o, 'ae_snd_mu': ae_s[0], 'ae_snd_z': ae_s[2], 'ae_snd_P': ae_s[3],
                'ae_dom_P': ae_d[3],
                'poly_plus_phon': ppe_o, 'ppe_snd_P': ppe_s[3], 'ppe_dom_P': ppe_d[3],
                'poly_plus_ascii': ape_o, 'ape_snd_P': ape_s[3], 'ape_dom_P': ape_d[3],
            })
            log(f"  [{suite_name[:12]} {fam_label:18s}] PhonEx={pe_o:2d}/{K} (mu={pe_s[0]:.2f} z={pe_s[2]:+.2f} Psnd={pe_s[3]:.5f} Pdom={pe_d[3]:.5f}) | "
                f"PhonSt={ps_o:2d}/{K} (Psnd={ps_s[3]:.5f} z={ps_s[2]:+.2f}) | AscEx={ae_o:2d}/{K} (Psnd={ae_s[3]:.5f})")

    return summary_rows, match_rows


# ==============================================================================
# TEST A3: EXPANDED BRONZE AGE MELUHHA / INDUS LOANWORD SKELETON LOCK
# ==============================================================================
# Every target skeleton comes strictly from the externally attested loanword (onset-preserving degeminated!).
# Self-source families are strictly excluded from scoring to guarantee zero circularity!
BRONZE_AGE_LOANS = [
    # --- PANEL A3a: 10 Strictly Near Eastern / Mediterranean External Trade Loans ---
    ("01_sesame_ellu", "A3a_NearEast", False, "oilseed", "Akk. ellu ('pure sesame oil')", {"Akkadian"},
     {"Vl"}, r"\b(sesame|sesamum|gingelly|gingily|oilseed)\b", r"\b(sesam|olsaat)\b"),
    ("02_ivory_pilu", "A3a_NearEast", True, "923", "Akk. pīru/pīlu, OP pīru ('elephant/ivory')", {"Akkadian"},
     {"pl", "pr"}, r"\b(elephant|ivory|tusk|tooth)\b", r"\b(elefant|elfenbein|zahn)\b"),
    ("03_peacock_tukki", "A3a_NearEast", False, "bird", "Heb. tukkī, Gk. taōs ('peacock')", set(),
     {"tk"}, r"\b(peacock|peafowl)\b", r"\b(pfau)\b"),
    ("04_cotton_karpasu", "A3a_NearEast", True, "390", "Akk. karpāsu, Heb. karpas, Gk. karpasos ('cotton')",
     {"Akkadian", "Indo-Aryan", "Indo-Aryan_Turner"},
     {"krp", "krps"}, r"\b(cotton|lint|gossypium)\b", r"\b(baumwolle)\b"),
    ("05_meluhha_wood_mesu", "A3a_NearEast", True, "390/405/407", "Sum. giš-mes-me-luh-ha, Akk. mēsu/musukkannu",
     {"Sumerian", "Akkadian"},
     {"ms", "msk"}, r"\b(sissoo|rosewood|dalbergia|ebony|timber|tree|wood)\b", r"\b(baum|holz|ebenholz)\b"),
    ("06_copper_uruda", "A3a_NearEast", True, "850", "Sum. uruda, Akk. werûm ('copper')", {"Sumerian", "Akkadian"},
     {"Vrt", "Vrd", "wr"}, r"\b(copper|bronze)\b", r"\b(kupfer|bronze)\b"),
    ("07_meluhha_fowl_dar", "A3a_NearEast", False, "bird", "Sum. dar-me-luh-ha (Akk. loan tarlugallum < dar-lugal)",
     {"Sumerian", "Akkadian"},
     {"tr", "dr"}, r"\b(francolin|partridge|pheasant|fowl|rooster|cock|hen|quail)\b", r"\b(huhn|rebhuhn|fasan|vogel)\b"),
    ("08_monkey_qop", "A3a_NearEast", False, "animal", "Heb. qōp, Akk. uqūpu, Eg. gjf ('Indian monkey/ape')", {"Akkadian"},
     {"kp", "Vkp"}, r"\b(monkey|ape|baboon|macaque|langur)\b", r"\b(affe)\b"),
    ("09_rice_oryza", "A3a_NearEast", False, "grain", "Gk. óryza, OP *vrīzi ('rice')", set(),
     {"Vrc", "Vrs", "Vrz", "wrs", "wrc", "vrh", "vrj"}, r"\b(rice|paddy|oryza)\b", r"\b(reis)\b"),
    ("10_ship_koland", "A3a_NearEast", True, "705", "Gk. kolandio-phōnta / Indian Ocean ship-vessel", set(),
     {"klm", "kln", "klnt"}, r"\b(ship|boat|vessel|sailor|navigator)\b", r"\b(schiff|boot|gefass)\b"),

    # --- PANEL A3b addition: 4 Balanced Non-IE Rigvedic/Early-Vedic Harappan Substrate Loans ---
    ("11_threshing_khala", "A3b_IndusSub", True, "705/615", "RV khala- ('threshing-floor', non-IE substrate)",
     {"Indo-Aryan", "Indo-Aryan_Turner"},
     {"kl", "khl", "klm"}, r"\b(threshing|granary|open space)\b", r"\b(tenne|dreschplatz)\b"),
    ("12_bangle_valaya", "A3b_IndusSub", True, "790", "Skt. valaya- ('bangle/bracelet', non-IE substrate)",
     {"Indo-Aryan", "Indo-Aryan_Turner"},
     {"vl", "bl", "wl"}, r"\b(bangle|bracelet|armlet|hoop)\b|\bring\b(?!\s*-?\s*dove)", r"\b(armband|armreif|ring)\b"),
    ("13_jar_kunda", "A3b_IndusSub", True, "740", "Skt. kuṇḍa- ('round pot/jar', non-IE substrate)",
     {"Indo-Aryan", "Indo-Aryan_Turner"},
     {"knt", "knd", "kt", "kd"}, r"\b(jar|pot|pitcher|waterpot|bowl|urn)\b", r"\b(krug|topf|schale|urne)\b"),
    ("14_plough_langala", "A3b_IndusSub", False, "tool", "RV lāṅgala- ('plough', classic Austroasiatic/Indus substrate)",
     {"Indo-Aryan", "Indo-Aryan_Turner"},
     {"lng", "ngl", "nkl", "nkr"}, r"\b(plough|plow)\b", r"\b(pflug)\b"),
]


def run_test_a3(lex_map):
    log("=== TEST A3: EXPANDED BRONZE AGE MELUHHA / INDUS LOANWORD SKELETON LOCK ===")
    summary_rows = []
    match_rows = []

    panels = [
        ("A3a_NearEast_10", [x for x in BRONZE_AGE_LOANS if x[1] == "A3a_NearEast"]),
        ("A3b_AllBronzeAge_14", BRONZE_AGE_LOANS),
        ("A3c_SignAnchored_8", [x for x in BRONZE_AGE_LOANS if x[2]]),
    ]

    for pname, loan_list in panels:
        for fam_label, L in lex_map.items():
            rng = np.random.default_rng(20261128)
            is_de = L.is_de

            ext_items = [x for x in loan_list if fam_label not in x[5]]
            K_ext = len(ext_items)

            # Vectorized precomputation: for each loan k, build boolean mask of:
            #  sem_mat[k, i] = etymon i has the target meaning
            #  sk_mat[k, u]  = form-slot u matches target_skels
            sem_mat = np.zeros((K_ext, L.E), dtype=bool)
            sk_mat = np.zeros((K_ext, L.E), dtype=bool)

            for k, (lid, panel, is_anch, sgn, att, self_fams, target_skels, en_rx, de_rx) in enumerate(ext_items):
                rx = re.compile(de_rx if is_de else en_rx, re.I)
                sem_mat[k] = L.match_regex_bool(rx)
                for u in range(L.E):
                    for sk in L.skels[u]:
                        if sk in target_skels or (len(sk) >= 3 and sk[:3] in target_skels) or (len(sk) >= 2 and sk[:2] in target_skels):
                            sk_mat[k, u] = True
                            break

            # Real hits!
            real_hits = np.any(sem_mat & sk_mat, axis=1)
            obs_ext = int(real_hits.sum())

            # Record audited real matches
            for k, (lid, panel, is_anch, sgn, att, self_fams, target_skels, en_rx, de_rx) in enumerate(ext_items):
                if real_hits[k]:
                    e_hit = int(np.flatnonzero(sem_mat[k] & sk_mat[k])[0])
                    # Find exact matching skel & nf
                    hit_sk, hit_nf = L.skels[e_hit][0], L.asciis[e_hit][0]
                    for sk, nf in zip(L.skels[e_hit], L.asciis[e_hit]):
                        if sk in target_skels or (len(sk) >= 3 and sk[:3] in target_skels) or (len(sk) >= 2 and sk[:2] in target_skels):
                            hit_sk, hit_nf = sk, nf
                            break
                    match_rows.append({
                        'panel': pname, 'family': fam_label, 'dict': L.dict_name,
                        'loan_id': lid, 'sign_anchor': sgn, 'attestation': att,
                        'matched_word': f"{L.hws[e_hit]} ({L.eids[e_hit]})", 'norm': hit_nf, 'onset_skel': hit_sk,
                        'target_skels': '|'.join(sorted(target_skels)), 'gloss': ' ; '.join(L.senses[e_hit])[:110],
                    })

            # 5,000 Vectorized Cluster-Preserving Sound Shuffles!
            sh_ext = np.zeros(N_SHUF)
            for t in range(N_SHUF):
                p = L.make_cluster_perm(rng)
                sh_ext[t] = float(np.sum(np.any(sem_mat & sk_mat[:, p], axis=1)))

            mu_e, sd_e, z_e, p_e = p_and_z(obs_ext, sh_ext)

            summary_rows.append({
                'panel': pname, 'family': fam_label, 'dict': L.dict_name, 'n_etyma': L.E,
                'ext_tested': K_ext, 'ext_hits': obs_ext,
                'ext_shuf_mean': mu_e, 'ext_shuf_sd': sd_e, 'ext_z': z_e, 'ext_P': p_e,
                'n_self_excluded': len(loan_list) - K_ext,
            })
            log(f"  [{pname:19s} {fam_label:18s}] EXT={obs_ext:2d}/{K_ext:2d} vs {mu_e:.2f} (z={z_e:+.2f}, P={p_e:.5f})")

    return summary_rows, match_rows


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    log(f"Starting Key #2 Track A Vectorized Production Run (N_SHUF={N_SHUF} cluster-preserving shuffles)")
    build_fixed_pdrav_2branch()

    lex_map = collections.OrderedDict()
    for fam, dname, is_de in PRIMARY_7_FAMILIES + AUDIT_EXTRA_LEX:
        L = CleanCognateLex(fam, dname, is_de=is_de)
        lex_map[fam] = L
        pe_n = len(L.edges['phon_exact'][0])
        ae_n = len(L.edges['ascii_exact'][0])
        log(f"  Loaded {fam:18s} ({dname:20s}): {L.E:5d} clean etyma | phon_edges={pe_n:5d} ascii_edges={ae_n:5d} | dropped={L.dropped}")

    a1_sum, a1_matches = run_test_a1(lex_map)
    a2_sum, a2_matches = run_test_a2(lex_map)
    a3_sum, a3_matches = run_test_a3(lex_map)

    # Compute Fisher combined 3-test meta-P across primary 7 families + audit Dravidian variants!
    a1_idx = {(r['subtest'], r['family']): r for r in a1_sum}
    a2_idx = {(r['suite'], r['family']): r for r in a2_sum}
    a3_idx = {(r['panel'], r['family']): r for r in a3_sum}

    meta_rows = []
    log("=== JOINT 3-TEST FISHER META-ANALYSIS (A1 x A2 x A3) ===")
    for fam in list(lex_map.keys()):
        p_a1 = a1_idx[('A1a_fish12_phon_exact', fam)]['P_sound']
        p_a1_comp = a1_idx.get(('A1b_attested_astral_comp12', fam), {}).get('P_sound_new9', 1.0)
        p_a2_pe = a2_idx[('A2c_Wave2B_12_Clean', fam)]['pe_snd_P']
        p_a2_ps = a2_idx[('A2c_Wave2B_12_Clean', fam)]['ps_snd_P']
        p_a3_14 = a3_idx[('A3b_AllBronzeAge_14', fam)]['ext_P']
        p_a3_anch = a3_idx[('A3c_SignAnchored_8', fam)]['ext_P']
        chi_strict, p_strict = fisher_combined_p([p_a1, p_a2_pe, p_a3_14])
        chi_core, p_core = fisher_combined_p([p_a1_comp, p_a2_ps, p_a3_anch])
        meta_rows.append({
            'family': fam, 'dict': lex_map[fam].dict_name,
            'P_A1a_phon': p_a1, 'P_A1b_astral_fish': p_a1_comp,
            'P_A2c_phon_exact': p_a2_pe, 'P_A2c_phon_stem': p_a2_ps,
            'P_A3b_all14': p_a3_14, 'P_A3c_anchored8': p_a3_anch,
            'Fisher_Strict3_Chi2': chi_strict, 'Fisher_Strict3_P': p_strict,
            'Fisher_Core3_Chi2': chi_core, 'Fisher_Core3_P': p_core,
            'Bonf_7fam_Pass_Strict': int(p_strict < 0.05 / 7.0),
            'Bonf_7fam_Pass_Core': int(p_core < 0.05 / 7.0),
        })
        log(f"  [META {fam:18s}] Strict3(A1a_ph={p_a1:.4f}, A2c_ph={p_a2_pe:.4f}, A3b={p_a3_14:.4f}) -> P={p_strict:.6f} | "
            f"Core3(A1b={p_a1_comp:.4f}, A2c_st={p_a2_ps:.4f}, A3c={p_a3_anch:.4f}) -> P={p_core:.6f}")

    write_csv(os.path.join(OUT_DIR, "test_a1_compounds_summary.csv"), a1_sum)
    write_csv(os.path.join(OUT_DIR, "test_a1_matched_words.csv"), a1_matches)
    write_csv(os.path.join(OUT_DIR, "test_a2_anchors_summary.csv"), a2_sum)
    write_csv(os.path.join(OUT_DIR, "test_a2_matched_words.csv"), a2_matches)
    write_csv(os.path.join(OUT_DIR, "test_a3_loans_summary.csv"), a3_sum)
    write_csv(os.path.join(OUT_DIR, "test_a3_matched_words.csv"), a3_matches)
    write_csv(os.path.join(OUT_DIR, "meta_joint_3test.csv"), meta_rows)

    with open(os.path.join(OUT_DIR, "key2a_summary.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "n_shuf": N_SHUF,
            "bonferroni_7fam_alpha": round(0.05 / 7.0, 5),
            "test_a1": a1_sum,
            "test_a2": a2_sum,
            "test_a3": a3_sum,
            "meta_joint": meta_rows,
        }, fh, indent=2)

    log("All Key #2 Track A tests completed cleanly!")


if __name__ == "__main__":
    main()
