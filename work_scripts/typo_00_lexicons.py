#!/usr/bin/env python3
"""typo_00_lexicons.py -- Build cognate-root / etymon-clustered and homonym-resolved lexicons
across all 7 candidate language families for the Rebus-Rescue Pincer (typo_01_rebus_rescue.py).

Outputs:
  /tmp/typo_lex/<name>.tsv  (columns: eid, cluster_id, hw, norm, skel, gloss)
  work_data/typo/cognate_lex_sizes.csv
"""
import os, re, csv, json, html, glob, unicodedata, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LX = os.path.join(ROOT, "work_data", "lexicons")
M1 = os.path.join(ROOT, "work_data", "lang_m")
TMP_LEX = "/tmp/typo_lex"
OUT_DIR = os.path.join(ROOT, "work_data", "typo")
os.makedirs(TMP_LEX, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

MAP = {
    'ŋ': 'ng', 'ə': 'a', 'ɛ': 'e', 'ɔ': 'o', 'ʃ': 's', 'ß': 'ss', 'ø': 'o', 'æ': 'ae',
    'ı': 'i', 'ł': 'l', 'đ': 'd', 'ʔ': '', 'ʼ': '', '¢': 'ng', '§': 's', 'ɨ': 'i',
    'ʌ': 'a', 'ɖ': 'd', 'ʈ': 't', 'ɳ': 'n', 'ɭ': 'l', 'ɽ': 'r', 'ʂ': 's', 'ç': 'c',
    'š': 's', 'ḫ': 'h', 'ĝ': 'g', 'ṯ': 't', 'ḏ': 'd', 'ẓ': 'z', 'ṣ': 's', 'ṭ': 't',
    'ḍ': 'd', 'ṇ': 'n', 'ṛ': 'r', 'ḷ': 'l', 'ṟ': 'r', 'ṉ': 'n', 'ḻ': 'l', 'ṅ': 'ng',
    'ñ': 'n', 'ś': 's', 'ṃ': 'm', 'ḥ': 'h', 'ɟ': 'j', 'ɲ': 'n', 'ɽ': 'r', 'ɭ': 'l',
}

def norm(w):
    w = str(w).lower().strip().lstrip('*')
    w = ''.join(MAP.get(c, c) for c in w)
    w = unicodedata.normalize('NFD', w)
    w = ''.join(c for c in w if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', w)

def skel(n):
    return re.sub(r'[aeiou]', '', n)

def nfc(s):
    return unicodedata.normalize('NFC', s)

STOP_WORDS = {
    'a', 'an', 'the', 'of', 'to', 'in', 'on', 'for', 'with', 'or', 'and', 'as', 'by',
    'at', 'from', 'be', 'is', 'are', 'one', 'who', 'that', 'which', 'kind', 'sort'
}

def content_words(g):
    ws = re.findall(r'[a-z]{3,}', norm_gloss(g))
    return {w for w in ws[:8] if w not in STOP_WORDS}

def norm_gloss(g):
    g = unicodedata.normalize('NFD', str(g).lower())
    g = ''.join(c for c in g if not unicodedata.combining(c)).replace('ß', 'ss')
    return re.sub(r'\s+', ' ', g).strip()

class UnionFind:
    def __init__(self):
        self.p = {}
    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra

sizes = []

def save_lex(name, family, tier, rows, note=""):
    """rows: list of (eid, cluster_id, hw, gloss)"""
    kept = []
    seen = set()
    for eid, cid, hw, gl in rows:
        n = norm(hw)
        sk = skel(n)
        gl_clean = re.sub(r'\s+', ' ', str(gl)).strip()[:300]
        if len(n) < 2 or not sk or not gl_clean:
            continue
        key = (str(eid), n, gl_clean[:80])
        if key in seen:
            continue
        seen.add(key)
        kept.append((str(eid), str(cid), hw, n, sk, gl_clean))
    out_path = os.path.join(TMP_LEX, f"{name}.tsv")
    with open(out_path, "w", encoding="utf-8") as f:
        for r in kept:
            f.write("\t".join(r) + "\n")
    by_nf = collections.defaultdict(set)
    by_sk = collections.defaultdict(set)
    for r in kept:
        by_nf[r[3]].add(r[0])
        by_sk[r[4]].add(r[0])
    homo_strict = sum(1 for v in by_nf.values() if len(v) > 1)
    homo_med = sum(1 for v in by_sk.values() if len(v) > 1)
    n_eids = len({r[0] for r in kept})
    n_cids = len({r[1] for r in kept})
    sizes.append({
        "dictionary": name,
        "family": family,
        "tier": tier,
        "rows": len(kept),
        "entries": n_eids,
        "deriv_clusters": n_cids,
        "strict_shared_forms": homo_strict,
        "medium_shared_skels": homo_med,
        "note": note,
    })
    print(f"[typo_00] {name:26s} ({family:10s} | {tier:8s}): {len(kept):6d} rows, {n_eids:6d} etyma, "
          f"{n_cids:6d} clusters, strict_homo={homo_strict:5d}, med_homo={homo_med:5d}")
    return kept


# ==============================================================================
# 1. DRAVIDIAN: Proto-Dravidian Multi-Branch Cognates & Cf. Derivational Clusters
# ==============================================================================
BRANCH_OF = {
    'Ta': 'SD1', 'Ma': 'SD1', 'Ko': 'SD1', 'To': 'SD1', 'Ka': 'SD1', 'Koḍ': 'SD1', 'Tu': 'SD1',
    'Te': 'SD2', 'Go': 'SD2', 'Konḍa': 'SD2', 'Koṇḍa': 'SD2', 'Pe': 'SD2', 'Manḍ': 'SD2', 'Kui': 'SD2', 'Kuwi': 'SD2',
    'Kol': 'CD', 'Nk': 'CD', 'Pa': 'CD', 'Ga': 'CD',
    'Kur': 'ND', 'Kuṛ': 'ND', 'Malt': 'ND', 'Br': 'ND',
}
LANGS_RE = r'Ta|Ma|Ko|To|Ka|Koḍ|Tu|Te|Kol|Nk|Pa|Ga|Go|Kur|Malt|Br|Pe|Manḍ|Kuṛ|Kui|Kuwi|Konḍa|Koṇḍa'
SPLIT_LANG = re.compile(r'(?:^|(?<=[\s(;.]))(' + LANGS_RE + r')\.?\s(?=\S)')
GLUED_ENTRY = re.compile(r'(?<=[.;])\s+(\d{1,4}[a-z]?)\s+(?=(?:' + LANGS_RE + r')\.\s)')
WORDCH = re.compile(r"^[a-zA-ZÀ-ɏḀ-ỿ\u0300-\u036f·\-ʼ']+$")
POS_SET = {'n.', 'adj.', 'adv.', 'v.', 'v.i.', 'v.t.', 'intr.', 'tr.', 'id.', 'pl.', 'interj.', 'vb.'}

def build_dravidian():
    raw_entries = []
    with open(os.path.join(LX, "dedr", "dedr_entries.tsv"), encoding="utf-8") as f:
        for line in f:
            eid, txt = line.rstrip("\n").split("\t", 1)
            # Split glued entries (e.g., "... DED(S, N) 3994. 4877 Kol. ...")
            pieces = GLUED_ENTRY.split(txt)
            raw_entries.append((eid.strip(), pieces[0]))
            for j in range(1, len(pieces) - 1, 2):
                raw_entries.append((pieces[j].strip(), pieces[j + 1]))

    uf = UnionFind()
    parsed = {}
    daughter_rows = {'dedr_tamil': [], 'dedr_malayalam': [], 'dedr_kannada': [], 'dedr_telugu': []}
    want_d = {'Ta': 'dedr_tamil', 'Ma': 'dedr_malayalam', 'Ka': 'dedr_kannada', 'Te': 'dedr_telugu'}

    for eid, full_txt in raw_entries:
        uf.find(eid)
        # Parse internal DEDR Cf. links (excluding Cf. Skt. / Turner numbers)
        cf_part = full_txt
        # Strip Turner CDIAL numbers after 'CDIAL' or 'Voc.' so we only link internal DEDR IDs
        cf_clean = re.sub(r'(?:CDIAL|Voc\.|DED\(S|BSOAS)[^.;]*', '', cf_part)
        for m in re.finditer(r'(?:\b[Cc]f\.|\bs\.v\.)\s*(\d{1,4}[a-z]?(?:\s*,\s*\d{1,4}[a-z]?)*)', cf_clean):
            for num_tok in re.findall(r'\d{1,4}[a-z]?', m.group(1)):
                uf.union(eid, num_tok)

        # Check if explicitly marked as Sanskrit/Prakrit loan into Dravidian
        main_txt = re.split(r'\s/\s*Cf\.|DED\(S|DEN\b|Previous Page', full_txt)[0]
        is_skt_loan = bool(re.search(r'<\s*(?:Skt|Pkt|IA)\b|DBIA', full_txt))

        parts = SPLIT_LANG.split(main_txt)
        branches = set()
        langs_seen = set()
        lang_forms = collections.defaultdict(list)  # lang -> [(form, gloss)]
        first_gloss_any = None

        for i in range(1, len(parts) - 1, 2):
            lang, seg = parts[i], parts[i + 1]
            if lang in BRANCH_OF:
                branches.add(BRANCH_OF[lang])
                langs_seen.add(lang)
            seg_clean = re.sub(r'\([^()]{0,60}\)', ' ', seg)
            prev = None
            for chunk in seg_clean.split(';'):
                toks = chunk.strip().rstrip('.').split()
                if not toks:
                    continue
                if toks[0] in POS_SET and prev:
                    forms, gl = prev, ' '.join(toks[1:])
                else:
                    forms = []
                    k = 0
                    while k < len(toks):
                        t = toks[k]
                        k += 1
                        last = not t.endswith(',')
                        for f_ in t.rstrip(',').split('/'):
                            if WORDCH.match(f_) and f_ not in POS_SET:
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

        # Daughter tables (for baseline comparison, with Cf. cluster_id)
        for lg, dname in want_d.items():
            for f_, gl_ in lang_forms.get(lg, []):
                g_use = gl_ if (gl_ and gl_ != 'id') else first_gloss_any
                daughter_rows[dname].append((eid, eid, f_, g_use))

        parsed[eid] = {
            'branches': branches,
            'langs': langs_seen,
            'lang_forms': lang_forms,
            'first_gloss': first_gloss_any,
            'is_skt_loan': is_skt_loan,
        }

    # Update daughter rows with Cf. cluster_id
    for dname, rlist in daughter_rows.items():
        upd = [(eid, uf.find(eid), hw, gl) for eid, _, hw, gl in rlist]
        save_lex(dname, "Dravidian", "daughter", upd, "DEDR daughter with Cf. clusters")

    # Build Proto-Dravidian Etymon-Collapsed Cognate Lexicons:
    # Priority order for conservative root form: Ta -> Ma -> Ka -> Te -> Kol -> Pa -> Go -> Kur -> Br
    PRIO = ['Ta', 'Ma', 'Ka', 'Ko', 'Tu', 'Te', 'Kol', 'Pa', 'Ga', 'Go', 'Konḍa', 'Kui', 'Kur', 'Kuṛ', 'Malt', 'Br']
    pdrav_2br = []
    pdrav_2lg = []
    pdrav_cf_merged = collections.OrderedDict()  # (cid, norm_root) -> (cid, hw, glosses)

    for eid, info in parsed.items():
        if info['is_skt_loan']:
            continue
        cid = uf.find(eid)
        # Collect primary root form (first headword of earliest-attested branch) + distinct core senses (e.g. Ta. mīn star in 4876!)
        root_hw = None
        core_forms = []
        gloss_parts = []
        for lg in PRIO:
            if lg in info['lang_forms']:
                for idx_f, (f_, gl_) in enumerate(info['lang_forms'][lg]):
                    if root_hw is None:
                        root_hw = f_
                        core_forms.append(f_)
                    # Keep distinct short root-level sense inside primary language (e.g. mīṉ 'star' under 4876 miṉ)
                    if lg in ('Ta', 'Ma', 'Ka', 'Te') and gl_ and gl_ != 'id':
                        if len(gloss_parts) < 5 and gl_ not in gloss_parts:
                            gloss_parts.append(gl_)
                        if len(norm(f_)) <= len(norm(root_hw)) + 1 and norm(f_) != norm(root_hw) and len(core_forms) < 2:
                            core_forms.append(f_)
                if root_hw is not None and len(gloss_parts) >= 2:
                    break
        if not root_hw:
            continue
        joined_gl = '; '.join(gloss_parts) if gloss_parts else info['first_gloss']

        if len(info['langs']) >= 2:
            for cf_hw in core_forms:
                pdrav_2lg.append((eid, cid, cf_hw, joined_gl))
        if len(info['branches']) >= 2:
            for cf_hw in core_forms:
                pdrav_2br.append((eid, cid, cf_hw, joined_gl))
                # Also build Cf-merged version where Cf-linked entries share eid = cid
                pdrav_cf_merged.setdefault((cid, norm(cf_hw)), [cid, cid, cf_hw, []])[3].append(joined_gl)

    save_lex("pdrav_2branch", "Dravidian", "cognate", pdrav_2br,
             "Proto-Dravidian DEDR etyma in >=2 primary branches (1 canonical root/etymon, Cf. clusters)")
    save_lex("pdrav_2lang", "Dravidian", "cognate_wide", pdrav_2lg,
             "DEDR etyma in >=2 Dravidian languages (1 canonical root/etymon, Cf. clusters)")
    cf_merged_rows = [(cid, cid, hw, '; '.join(gls[:4])) for (_, _), (cid, _, hw, gls) in pdrav_cf_merged.items()]
    save_lex("pdrav_2branch_cfmerged", "Dravidian", "root_merged", cf_merged_rows,
             "Proto-Dravidian >=2 branches with Cf. cross-references merged into single root eid")


# ==============================================================================
# 2. INDO-ARYAN: Turner CDIAL Inherited Cognates + PII + Homonym MW
# ==============================================================================
IA_DAUGHTERS = re.compile(r'\b(?:Pk|Pa|NiDoc|Ash|Wg|Kt|Pr|Dm|Tir|Pash|Shum|Gaw|Kal|Kho|Bshk|Tor|Mai|Phal|Sh|K|S|L|P|WPah|Ku|N|A|B|Or|Bi|Mth|Bhoj|Aw|H|Rj|G|M|Ko|Si|Md|Gy)\.')

def build_indo_aryan():
    # Parse Turner CDIAL with printed entry numbers, daughter counts, and cross-references
    txt = nfc(open(os.path.join(LX, "raw", "turner_cdial.txt"), encoding="utf-8", errors="ignore").read())
    lines = txt.split("\n")
    # Turner entries look like: "1234 *kūṭa- 1 'waterpot' ..." or headword lines
    ent_re = re.compile(r"^(?:(\d{1,5})\s+)?\*?([a-zA-Zāīūṛṝḷṃṭḍṇśṣḥñĉčĝ\u0300-\u036f]{2,25})-(?:\s+(\d+))?(?:\s|$)")
    uf = UnionFind()
    turner_all = []
    turner_2d = []
    ia_loan_skels = set()  # skeletons + content words for filtering IA loans in Munda!
    ia_loan_forms = collections.defaultdict(set)

    cur_no = 0
    for i, l in enumerate(lines):
        l_s = l.strip()
        m = ent_re.match(l_s)
        if not m:
            continue
        eno_str, hw, hom_no = m.group(1), m.group(2), m.group(3)
        block = ' '.join(x.strip() for x in lines[i:i + 6] if x.strip())
        gm = re.search(r"[‘'’]([^'’‘]{2,90})[’']", block[m.end():m.end() + 140])
        if not gm:
            continue
        gl = gm.group(1).lower().strip()
        cur_no += 1
        eid = eno_str if eno_str else f"T{cur_no}"
        if hom_no:
            eid = f"{eid}_{hom_no}"
        base_num = eno_str or eid
        uf.find(base_num)
        for cm in re.finditer(r"(?:see|cf\.)\s*(\d{1,5}(?:\s*,\s*\d{1,5})*)", block, flags=re.I):
            for ntok in re.findall(r'\d{1,5}', cm.group(1)):
                uf.union(base_num, ntok)
        ndaughters = len(set(IA_DAUGHTERS.findall(block)))
        turner_all.append((eid, base_num, hw, gl, ndaughters))
        nf = norm(hw)
        sk = skel(nf)
        if len(nf) >= 2:
            ia_loan_forms[nf] |= content_words(gl)
        if len(sk) >= 3:
            ia_loan_skels.add(sk)

    # Also cluster shared 3+ consonant verbal/nominal stems in Turner
    all_rows = [(eid, uf.find(bn), hw, gl) for eid, bn, hw, gl, _ in turner_all]
    cog_rows = [(eid, uf.find(bn), hw, gl) for eid, bn, hw, gl, nd in turner_all if nd >= 2]

    # Add Proto-Indo-Iranian Wiktionary reconstructions
    pii_rows = []
    for idx_l, line in enumerate(open(os.path.join(M1, "lex", "proto_indoiranian_wiktionary.tsv"), encoding="utf-8")):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 5:
            pii_rows.append((f"PII_{p[0]}", f"PII_{p[3][:3]}", p[1], p[4]))
            cog_rows.append((f"PII_{p[0]}", f"PII_{p[3][:3]}", p[1], p[4]))

    save_lex("oia_turner", "Indo-Aryan", "daughter", all_rows, "Turner CDIAL homonym-aware with cross-ref clusters")
    save_lex("proto_indoiranian", "Indo-Aryan", "daughter", pii_rows, "Proto-Indo-Iranian reconstructions")
    save_lex("oia_cognates", "Indo-Aryan", "cognate", cog_rows,
             "Turner CDIAL inherited OIA cognates (>=2 daughter languages) + Proto-Indo-Iranian")

    # Also build homonym-aware Monier-Williams if mw.xml exists
    mw_path = os.path.join(ROOT, "evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml")
    if os.path.exists(mw_path):
        SL = {'A': 'ā', 'I': 'ī', 'U': 'ū', 'f': 'ṛ', 'F': 'ṝ', 'x': 'ḷ', 'X': 'ḹ', 'E': 'ai', 'O': 'au',
              'K': 'kh', 'G': 'gh', 'N': 'ṅ', 'C': 'ch', 'J': 'jh', 'Y': 'ñ', 'w': 'ṭ', 'W': 'ṭh',
              'q': 'ḍ', 'Q': 'ḍh', 'R': 'ṇ', 'T': 'th', 'D': 'dh', 'P': 'ph', 'B': 'bh', 'S': 'ś',
              'z': 'ṣ', 'M': 'ṃ', 'H': 'ḥ', 'L': 'ḷ'}
        ent = collections.OrderedDict()
        lmap = {}
        with open(mw_path, encoding="utf-8") as f:
            for line in f:
                m = re.search(r'<key1>([^<]+)</key1>(.*?)</h><body>(.*?)</body>.*?<L>([\d.]+)</L>', line)
                if not m:
                    continue
                key, hpart, body, L = m.groups()
                hm = re.search(r'<hom>(\d+)</hom>', hpart)
                Lw = L.split('.')[0]
                if '.' in L and Lw in lmap:
                    eid = lmap[Lw]
                else:
                    eid = f'{key}#{hm.group(1)}' if hm else key
                    lmap[Lw] = eid
                b = re.sub(r'<(s|ls|ab|lex)\b[^>]*>.*?</\1>', ' ', body)
                b = re.sub(r'<[^>]+>', ' ', html.unescape(b))
                b = re.sub(r'\s+', ' ', b).strip(' ,;')
                b = re.split(r'[.\[]', b)[0].strip()[:120].lower()
                if not b:
                    continue
                hw = ''.join(SL.get(c, c) for c in key)
                e = ent.setdefault(eid, [hw, []])
                if len(e[1]) < 4:
                    e[1].append(b)
        mw_rows = [(eid, skel(norm(hw))[:3] or eid, hw, '; '.join(g)) for eid, (hw, g) in ent.items()]
        save_lex("sanskrit_mw", "Indo-Aryan", "daughter", mw_rows, "Monier-Williams Sanskrit with <hom> numbers")

    return ia_loan_forms, ia_loan_skels


# ==============================================================================
# 3. MUNDA: Proto-Munda (Zenodo 127) + Kharia (South Munda) + Homonym-Fixed
#           Santali & Mundari (North Munda) + Pre-IA Cognate Root Lexicon
# ==============================================================================
def split_printed_homonyms(tsv_path, prefix):
    """Keep separate printed paragraphs with the same headword as separate entries
    ONLY when their glosses share zero content words (genuine homonyms, not OCR repeats)."""
    by_hw = collections.defaultdict(list)
    with open(tsv_path, encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 2:
                continue
            hw, gl = p[0].strip(), p[1].strip()
            if ' ' in hw or len(hw) > 25 or not gl:
                continue
            # Filter obvious header noise
            if hw.lower() in ('mundari', 'santali', 'see', 'cf', 'ib', 'idem'):
                continue
            by_hw[hw].append(gl)

    out = []
    idx = 0
    for hw, gls in by_hw.items():
        # Cluster glosses of same hw that share any content word (same word/polysemy) vs zero overlap (homonym)
        clusters = []  # [(set_of_content_words, [glosses])]
        for g in gls:
            cw = content_words(g)
            merged = False
            for c_cw, c_gls in clusters:
                if (cw and c_cw and (cw & c_cw)) or (not cw and not c_cw):
                    c_cw |= cw
                    if g not in c_gls:
                        c_gls.append(g)
                    merged = True
                    break
            if not merged:
                clusters.append([set(cw), [g]])
        for hom_i, (_, c_gls) in enumerate(clusters):
            idx += 1
            eid = f"{prefix}_{idx}"
            cid = f"{prefix}_sk_{skel(norm(hw))[:3]}"
            out.append((eid, cid, hw, '; '.join(c_gls[:4])))
    return out

def parse_kharia():
    """Parse Kharia-English (Druart, second half of kharia_dict.txt) + English-Kharia (first half),
    excluding Hindi (h.) and Sadani (s.) Indo-Aryan loanwords."""
    txt = nfc(open(os.path.join(LX, "raw", "kharia_dict.txt"), encoding="utf-8", errors="ignore").read())
    pos = txt.find("KHARIA-ENGLISH")
    eng_kh = txt[:pos] if pos > 0 else ""
    kh_eng = txt[pos:] if pos > 0 else txt

    rows = []
    idx = 0
    # 1. Parse Kharia-English page blocks: margin list of Capitalized Kharia words, then "( page )", then paragraphs
    pages = re.split(r'\(\s*\d+\s*\)', kh_eng)
    # In Druart's layout: before page marker k is the headword list for page k, and after page marker k are the definitions!
    for p_i in range(len(pages) - 1):
        pre_lines = [l.strip() for l in pages[p_i].splitlines() if l.strip()]
        # Trailing block of short capitalized single-word lines are the headwords for the next page body
        hws = []
        for l in reversed(pre_lines):
            if re.match(r"^[A-Z][a-zA-Z'’\-]{1,18}\??$", l) and l.upper() != l:
                hws.append(l.rstrip('?'))
            elif hws and len(l) < 22 and re.match(r"^[A-Z]", l) and ' ' not in l:
                hws.append(l)
            elif len(hws) >= 3:
                break
        hws = list(reversed(hws))
        # Split page[p_i+1] into definition paragraphs (excluding trailing headword list of the next page)
        body_paras = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', pages[p_i + 1])]
        def_paras = []
        for bp in body_paras:
            if not bp or re.match(r"^(?:[A-Z][a-zA-Z'’\-]{1,18}\??\s*)+$", bp):
                continue
            def_paras.append(bp)
        if hws and abs(len(def_paras) - len(hws)) <= 4:
            for hw, df in zip(hws, def_paras[:len(hws)]):
                if re.match(r"^(?:h\.|s\.|h\s|hind)", df.lower()) or re.search(r"\b(?:s\.|h\.)\s", df.lower()[:25]):
                    continue
                gl = re.split(r'[.=]', df)[0].strip()
                gl = re.sub(r'\bcfr\b.*', '', gl, flags=re.I).strip(' ,;:')
                if len(gl) >= 3 and re.search(r'[a-z]{3,}', gl.lower()):
                    idx += 1
                    rows.append((f"KH_{idx}", f"KH_{skel(norm(hw))[:3]}", hw.lower(), gl.lower()[:160]))

    # 2. Also extract inline "word = english" or "pos. kharia_word" across both halves of kharia_dict.txt
    eng_pages = re.split(r'\(\s*\d+\s*\)', eng_kh)
    for p_i in range(len(eng_pages) - 1):
        pre_lines = [l.strip() for l in eng_pages[p_i].splitlines() if l.strip()]
        ehws = []
        for l in reversed(pre_lines):
            if re.match(r"^[A-Z][a-z]{2,18}$", l):
                ehws.append(l.lower())
            elif len(ehws) >= 3:
                break
        ehws = list(reversed(ehws))
        body_paras = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', eng_pages[p_i + 1])]
        def_paras = [bp for bp in body_paras if bp and not re.match(r"^(?:[A-Z][a-z]{2,18}\s*)+$", bp)]
        if ehws and abs(len(def_paras) - len(ehws)) <= 4:
            for e_gl, df in zip(ehws, def_paras[:len(ehws)]):
                if re.search(r'\b(?:h\.|s\.)', df[:20].lower()):
                    continue
                m = re.match(r"^(?:(?:n|v|a|adj|adv|pron|num|postp|prep|int|c|av|ady)\.\s*)+([a-zA-Z'’\-]{2,18})[.,\s]", df)
                if m:
                    kh_w = m.group(1).lower().strip(".,")
                    if len(norm(kh_w)) >= 2:
                        idx += 1
                        rows.append((f"KHE_{idx}", f"KH_{skel(norm(kh_w))[:3]}", kh_w, e_gl))

    # 3. Also salvage high-confidence clean entries from Hoffmann's Encyclopaedia Mundarica (encmund_v*.txt)
    for fn in sorted(glob.glob(os.path.join(LX, "raw", "encmund_v*.txt"))):
        for l in open(fn, encoding="utf-8", errors="ignore"):
            l = nfc(l).strip()
            m = re.match(r"^([a-z][a-zḍṭṇṛṅñāīūēō'\-]{2,14})\s*,\s*([a-z]{3,16}(?:\s+[a-z]{2,16}){0,3})\s*[.,]", l)
            if m and m.group(2) not in ('see', 'syn', 'same', 'var', 'also', 'the', 'with'):
                hw_e, gl_e = m.group(1), m.group(2)
                if len(norm(hw_e)) >= 2 and re.match(r'^(?:to\s+[a-z]+|[a-z]+)$', gl_e):
                    idx += 1
                    rows.append((f"EM_{idx}", f"EM_{skel(norm(hw_e))[:3]}", hw_e, gl_e))
    return rows

def build_munda(ia_loan_forms, ia_loan_skels):
    # 1. Homonym-aware North Munda & South Munda dictionaries
    camp = split_printed_homonyms(os.path.join(LX, "tsv", "santali_campbell.tsv"), "SC")
    bodd = split_printed_homonyms(os.path.join(LX, "tsv", "santali_bodding_v5.tsv"), "SB")
    mund = split_printed_homonyms(os.path.join(LX, "tsv", "mundari_bhadra.tsv"), "MB")
    khar = parse_kharia()

    # Santali Wiktionary (kaikki_santali.jsonl)
    swik = []
    for i, line in enumerate(open(os.path.join(LX, "raw", "kaikki_santali.jsonl"), encoding="utf-8")):
        d = json.loads(line)
        roms = [f['form'] for f in d.get('forms', []) if 'romanization' in f.get('tags', [])]
        hw = (roms[0] if roms else d.get('word', '')).lstrip('*')
        if ' ' in hw:
            continue
        et = d.get('etymology_number', 0)
        gls = [s['glosses'][0].lower() for s in d.get('senses', [])[:3] if s.get('glosses') and not s['glosses'][0].lower().startswith('romanization')]
        if gls:
            swik.append((f"SW_{d.get('word','')}#{et}", f"SW_{skel(norm(hw))[:3]}", hw, '; '.join(gls)))

    save_lex("santali_campbell", "Munda", "daughter", camp, "Campbell Santali with printed homonyms separated")
    save_lex("santali_bodding5", "Munda", "daughter", bodd, "Bodding Santali vol 5 with printed homonyms separated")
    save_lex("santali_wiktionary", "Munda", "daughter", swik, "Wiktionary Santali")
    save_lex("mundari_bhadra", "Munda", "daughter", mund, "Bhadra Mundari with printed homonyms separated")
    save_lex("kharia_druart", "Munda", "daughter", khar, "Druart/Floor Kharia (South Munda), Hindi/Sadani loans stripped")

    # 2. Parse Zenodo 127 Proto-Munda Cognates (Gold-standard PMunda reconstructions + daughter reflexes)
    pm_rows = []
    pm_known_norms = set()
    with open(os.path.join(LX, "raw", "zenodo_pmunda_cognates_127.csv"), encoding="utf-8") as f:
        r = csv.reader(f)
        hdr = next(r)
        for row in r:
            if len(row) < 28:
                continue
            cid_pm = f"PM_{row[0]}"
            gl = row[1].strip().lower()
            pm_rec = row[26].strip()
            # Collect Proto-Munda reconstruction + North/South Munda representative stems under this single etymon!
            forms_here = []
            for col_i in [26, 10, 16, 18, 4, 6, 8, 12, 20]:  # pmunda, kharia, santali, mundari, sora, remo, gutob, juang, ho
                val = row[col_i].strip()
                if val and val != '—':
                    for part in re.split(r'[;,/]', val):
                        part = re.sub(r'\(.*?\)', '', part).strip()
                        if len(norm(part)) >= 2:
                            forms_here.append(part)
                            pm_known_norms.add(norm(part))
            # Keep distinct normalized stems for this Proto-Munda etymon (capped at 4 representative stems so no bloat)
            seen_n = set()
            for fm in forms_here:
                nf = norm(fm)
                if nf not in seen_n and len(seen_n) < 4:
                    seen_n.add(nf)
                    pm_rows.append((cid_pm, cid_pm, fm, gl))

    # 3. Build Pre-Indo-Aryan Munda Cognate Lexicon (pmunda_cognates):
    #    Combine Zenodo 127 PMunda + cross-language Munda cognates attested in >=2 Munda languages
    #    (Santali, Mundari, Kharia) after filtering out Indo-Aryan loanwords!
    ENGLISH_LOANS = {'lat', 'lord', 'rail', 'skul', 'tikit', 'polis', 'jel', 'kort', 'botal', 'gila', 'tebil'}
    def is_ia_loan(hw, gl):
        nf = norm(hw)
        sk = skel(nf)
        if nf in pm_known_norms:
            return False
        if nf in ENGLISH_LOANS:
            return True
        cw = content_words(gl)
        # Exact normalized form + shared meaning in Turner OIA -> loanword!
        if nf in ia_loan_forms and (cw & ia_loan_forms[nf]):
            return True
        # 3+ consonant skeleton match + shared meaning in Turner OIA -> loanword!
        if len(sk) >= 3 and sk in ia_loan_skels:
            # Check prefix form match
            for k_nf in (nf, nf[:-1], nf + 'a'):
                if k_nf in ia_loan_forms and (cw & ia_loan_forms[k_nf]):
                    return True
        return False

    # Index non-loan entries by (skeleton, content_word) across the 3 Munda languages: Santali, Mundari, Kharia
    lang_buckets = {
        'Santali': [x for x in (camp + bodd + swik) if not is_ia_loan(x[2], x[3])],
        'Mundari': [x for x in mund if not is_ia_loan(x[2], x[3])],
        'Kharia':  [x for x in khar if not is_ia_loan(x[2], x[3])],
    }

    # Group cognates across >=2 Munda languages sharing skeleton (or prefix-2 skeleton for Kharia/North Munda) AND >=1 content gloss word
    by_sk_word = collections.defaultdict(lambda: collections.defaultdict(list))
    for lg_name, entries in lang_buckets.items():
        for eid, cid, hw, gl in entries:
            sk = skel(norm(hw))
            sk_key = sk[:3] if len(sk) >= 3 else sk
            for w in content_words(gl):
                by_sk_word[(sk_key, w)][lg_name].append((eid, hw, gl))

    uf_m = UnionFind()
    kept_munda_eids = {}
    for (sk_key, w), lg_map in by_sk_word.items():
        if len(lg_map) >= 2:  # Cognate attested in >=2 Munda languages (e.g. Santali+Mundari or North+South Kharia)!
            anchor = None
            for lg_name in ('Kharia', 'Mundari', 'Santali'):
                for eid, hw, gl in lg_map.get(lg_name, [])[:1]:
                    kept_munda_eids[eid] = (hw, gl)
                    if anchor is None:
                        anchor = eid
                    else:
                        uf_m.union(anchor, eid)

    # Collapse each cross-Munda cognate set into 1 canonical etymon (eid = cognate_root_id)
    cog_groups = collections.defaultdict(list)
    for eid, (hw, gl) in kept_munda_eids.items():
        cog_groups[uf_m.find(eid)].append((hw, gl))

    pm_cog_rows = list(pm_rows)
    for root_id, items in cog_groups.items():
        # Pick up to 2 distinct normalized forms and join unique glosses
        seen_nf = set()
        gls = []
        for _, gl in items:
            if gl not in gls and len(gls) < 3:
                gls.append(gl)
        joined_gl = '; '.join(gls)
        sk_cid = f"MC_{skel(norm(items[0][0]))[:2]}"
        for hw, _ in items:
            nf = norm(hw)
            if nf not in seen_nf and len(seen_nf) < 2:
                seen_nf.add(nf)
                pm_cog_rows.append((f"MC_{root_id}", sk_cid, hw, joined_gl))

    save_lex("pmunda_cognates", "Munda", "cognate", pm_cog_rows,
             "Zenodo 127 Proto-Munda + cross-Munda (Santali/Mundari/Kharia) cognates, IA loans stripped")


# ==============================================================================
# 4. ELAMITE, SUMERIAN, AKKADIAN, BURUSHASKI
# ==============================================================================
def build_elamite():
    # Separate printed homonyms in Hinz-Koch + extract bare roots stripped of class suffixes (-k, -r, -p, -me)
    hk_rows = split_printed_homonyms(os.path.join(LX, "tsv", "elamite_hinzkoch.tsv"), "EL")
    root_rows = []
    for eid, _, hw, gl in hk_rows:
        # First syllable / stem cluster for derivational C3
        syls = [s for s in hw.split('-') if s]
        stem_cid = f"ELC_{norm(syls[0])}" if syls else eid
        root_rows.append((eid, stem_cid, hw, gl))
        # Also strip final nominal class markers (-ik/-k, -ir/-r, -ip/-p, -me) under SAME eid so root matches!
        if len(syls) >= 2 and syls[-1] in ('ik', 'k', 'ir', 'r', 'ip', 'p', 'me', 'um'):
            bare = '-'.join(syls[:-1])
            if len(norm(bare)) >= 2:
                root_rows.append((eid, stem_cid, bare, gl))
    save_lex("elamite_hinzkoch", "Elamite", "daughter", hk_rows, "Hinz-Koch Elamite with printed homonyms separated")
    save_lex("elamite_roots", "Elamite", "cognate", root_rows, "Elamite lexical roots (class suffixes stripped, stem clusters)")

def build_sumerian():
    # Halloran Sumerian with sign-index homonyms separated + compound clustering
    L = open(os.path.join(LX, "raw", "sumerian_201604.txt"), encoding="utf-8", errors="ignore").read().split("\n")[205:]
    POS = r"(?:n|v|adj|adv|prep|conj|pron|num|part)"
    raw = []
    cur = []
    eno = 0
    for l in L:
        l = nfc(l).strip()
        if not l or l.startswith('Sumerian Lexicon'):
            continue
        m = re.match(r"^(%s)\.,?\s*(.*)$" % POS, l)
        if m and cur:
            g = re.match(r'([^.]*)', m.group(2).replace(';', ',')).group(1).strip()[:200].lower()
            if g:
                raw += [(f"SH_{eno}", h, h_raw, g) for h, h_raw in cur]
            continue
        m = re.match(r"^([^:—\[\]]{1,45}?)\s*(?::|—|–)\s*(.*)$", l)
        if m and not re.match(r'^\(?cf', m.group(2)):
            heads = []
            for t in re.split(r'[,;]', m.group(1)):
                h_raw = re.sub(r'\(.*?\)', '', t).strip().lower()
                h_clean = re.sub(r'[^a-zšĝḫ]', '', h_raw)
                if len(h_clean) >= 2 and h_clean not in ('and', 'prep', 'adj', 'see', 'also'):
                    heads.append((h_clean, h_raw))
            heads = heads[:3]
            t = re.sub(r"^(?:(?:%s)\.,?\s*)+" % POS, '', m.group(2).strip())
            g = re.match(r'([^.]*)', t.replace(';', ',')).group(1).strip()[:200].lower()
            cur = heads
            eno += 1
            if heads and g:
                raw += [(f"SH_{eno}", h, h_raw, g) for h, h_raw in heads]

    by = collections.OrderedDict()
    for eid, h, h_raw, g in raw:
        by.setdefault((eid, h), [h_raw, []])[1].append(g)

    hal_rows = []
    sum_simplex = []
    for (eid, h), (h_raw, gs) in by.items():
        parts = [re.sub(r'[^a-zšĝḫ]', '', x) for x in h_raw.split('-') if re.sub(r'[^a-zšĝḫ]', '', x)]
        cid = f"SUM_{norm(parts[0])}" if parts else eid
        gl = '; '.join(gs[:4])
        hal_rows.append((eid, cid, h, gl))
        # Simplex or 2-morpheme non-lu2/nig2 core roots
        if len(parts) <= 2 and (not parts or parts[0] not in ('lu', 'nig', 'nam')):
            sum_simplex.append((eid, cid, h, gl))

    # Wiktionary Sumerian
    sw_rows = []
    for line in open(os.path.join(LX, "raw", "kaikki_sumerian.jsonl"), encoding="utf-8"):
        d = json.loads(line)
        roms = [f['form'] for f in d.get('forms', []) if 'romanization' in f.get('tags', [])]
        hw_raw = (roms[0] if roms else d.get('word', '')).lower().lstrip('*')
        if ' ' in hw_raw:
            continue
        hw = re.sub(r'[0-9\-]', '', hw_raw)
        et = d.get('etymology_number', 0)
        gls = [s['glosses'][0].lower() for s in d.get('senses', [])[:3] if s.get('glosses') and not s['glosses'][0].lower().startswith(('romanization', 'alternative'))]
        if gls and len(norm(hw)) >= 2:
            eid = f"SUW_{d.get('word','')}#{et}"
            parts = [re.sub(r'[^a-zšĝḫ]', '', x) for x in hw_raw.split('-') if re.sub(r'[^a-zšĝḫ]', '', x)]
            cid = f"SUM_{norm(parts[0])}" if parts else eid
            sw_rows.append((eid, cid, hw, '; '.join(gls)))

    save_lex("sumerian_halloran", "Sumerian", "daughter", hal_rows, "Halloran Sumerian with sign-index homonyms")
    save_lex("sumerian_wiktionary", "Sumerian", "daughter", sw_rows, "Wiktionary Sumerian")
    save_lex("sumerian_roots", "Sumerian", "cognate", sum_simplex + sw_rows,
             "Sumerian core simplex roots + Wiktionary with compound-family clusters")

def build_akkadian():
    # Akkadian Wiktionary + triconsonantal root clustering (stripping Semitic m-/t-/š- prefixes for cluster_id)
    akk_rows = []
    with open(os.path.join(M1, "lex", "akkadian_wiktionary.tsv"), encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 5:
                continue
            eid, hw, nf, sk, gl = p[0], p[1], p[2], p[3], p[4]
            # Strip Akkadian mimation (-m) in a root variant and compute 3-consonant root cluster
            sk_nomim = sk[:-1] if (len(sk) >= 3 and nf.endswith(('um', 'am', 'im'))) else sk
            root_sk = sk_nomim[1:] if (len(sk_nomim) >= 4 and sk_nomim[0] in ('m', 't', 's')) else sk_nomim
            cid = f"AKK_{root_sk[:3]}"
            akk_rows.append((f"AK_{eid}", cid, hw, gl))
    save_lex("akkadian_wiktionary", "Akkadian", "daughter", akk_rows, "Akkadian Wiktionary")
    save_lex("akkadian_roots", "Akkadian", "cognate", akk_rows, "Akkadian with Semitic triconsonantal root clusters")

def build_burushaski():
    lor = split_printed_homonyms(os.path.join(LX, "tsv", "burushaski_werchikwar_yasin.tsv"), "BY")
    bar = split_printed_homonyms(os.path.join(LX, "tsv", "burushaski_barken_hunza.tsv"), "BH")
    # Also parse native Swadesh entries from starling_burushaski_swadesh.txt (confirming hir 'man', hun 'wood', etc.)
    swad = []
    sw_path = os.path.join(LX, "raw", "starling_burushaski_swadesh.txt")
    if os.path.exists(sw_path):
        txt = open(sw_path, encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r'\b\d+\s+([a-zA-Z\s/]{2,20}?)\s+([a-zA-Zšṣṭḍṇṛćčṅɣ\-]{2,15})\b', txt):
            gl_s, hw_s = m.group(1).strip().lower(), m.group(2).strip().lower()
            if gl_s in ('man', 'woman', 'fish', 'tree', 'bird', 'dog', 'sun', 'moon', 'star', 'water', 'stone', 'house', 'hand', 'eye', 'head', 'two', 'one'):
                swad.append((f"BSW_{len(swad)}", f"BUR_{skel(norm(hw_s))[:2]}", hw_s, gl_s))
    save_lex("burushaski_lorimer", "Burushaski", "daughter", lor, "Lorimer Yasin Burushaski with printed homonyms separated")
    # Merge cognate forms across Yasin + Hunza + Swadesh
    pooled = []
    for eid, _, hw, gl in (lor + bar + swad):
        cid = f"BUR_{skel(norm(hw))[:2]}"
        pooled.append((eid, cid, hw, gl))
    save_lex("burushaski_all", "Burushaski", "cognate", pooled, "Pooled Yasin + Hunza + Starling Burushaski")


def main():
    build_dravidian()
    ia_forms, ia_skels = build_indo_aryan()
    build_munda(ia_forms, ia_skels)
    build_elamite()
    build_sumerian()
    build_akkadian()
    build_burushaski()

    # Also copy remaining Wiktionary Dravidian tables with cluster_id = skel[:3] for completeness
    for wn in ("tamil_wiktionary", "telugu_wiktionary", "kannada_wiktionary"):
        wrows = []
        with open(os.path.join(M1, "lex", f"{wn}.tsv"), encoding="utf-8") as f:
            for line in f:
                p = line.rstrip("\n").split("\t")
                if len(p) >= 5:
                    wrows.append((f"{wn[:2]}_{p[0]}", f"{wn[:2]}_{p[3][:3]}", p[1], p[4]))
        save_lex(wn, "Dravidian", "daughter", wrows, f"{wn} table")

    out_csv = os.path.join(OUT_DIR, "cognate_lex_sizes.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sizes[0].keys()))
        w.writeheader()
        w.writerows(sizes)
    with open(os.path.join(TMP_LEX, "ready.flag"), "w") as f:
        f.write("ok\n")
    print(f"[typo_00] Wrote {len(sizes)} lexicons and {out_csv}")

if __name__ == "__main__":
    main()
