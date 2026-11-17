#!/usr/bin/env python3
"""lang_m step 3a: DICTIONARIES -> one table per dictionary: entry id, headword as printed, normalised form, consonant skeleton, gloss.

Sources (all already on disk except the Wiktionary sets, downloaded 2026-11-17 from kaikki.org into work_data/lang_m/raw/):
  Dravidian : DEDR (Burrow & Emeneau 1984) cut into its Tamil, Malayalam, Kannada and Telugu parts (work_data/lexicons/dedr/dedr_entries.tsv);
              a DEDR entry is one etymon, so two words count as different words only when they sit in different DEDR entries.
              Wiktionary Tamil, Telugu, Kannada (romanised headwords).  DEDR has no reconstructed forms; kaikki has no Proto-Dravidian set.
  Munda     : Santali (Campbell 1899; Bodding vol 5; Wiktionary), Mundari (Bhadra 1931): work_data/lexicons/tsv/
  Sumerian  : Halloran v3, Wiktionary Sumerian (tsv/)
  Indo-Aryan: Monier-Williams Sanskrit, Turner CDIAL Old Indo-Aryan headwords (tsv/); Proto-Indo-Iranian (Wiktionary reconstructions)
  Elamite   : Hinz & Koch 1987 (German glosses)
  Akkadian  : Wiktionary Akkadian
  Burushaski: Lorimer 1962 Yasin vocabulary (tsv/)
For the flat tsv lists, lines with the same printed headword are merged into one entry (so sense lines of one word are one word).

NORMALISED FORM (one rule for all): Unicode decomposed, accents / dots / length marks dropped, lower case, a few letters mapped
(sh-like s, ng, schwa -> a, open e/o -> e/o, h-with-breve -> h, zh-like l), then only a-z kept.  Vowel length is thus ignored.
SKELETON: the normalised form with the vowels a e i o u removed.
Output: work_data/lang_m/lex/<dict>.tsv  and  work_data/lang_m/lex_sizes.csv
"""
import os, re, csv, json, unicodedata, collections
ROOT = '/home/claude/ivc'; LX = f'{ROOT}/work_data/lexicons'; OUT = f'{ROOT}/work_data/lang_m'; RAW = f'{OUT}/raw'
os.makedirs(f'{OUT}/lex', exist_ok=True)
def log(*a): print('[lang_m_lexicons]', *a, flush=True)

MAP = {'ŋ': 'ng', 'ə': 'a', 'ɛ': 'e', 'ɔ': 'o', 'ʃ': 's', 'ß': 'ss', 'ø': 'o', 'æ': 'ae', 'ı': 'i', 'ł': 'l', 'đ': 'd', 'ʔ': '', 'ʼ': '',
       '¢': 'ng', '§': 's', 'ɨ': 'i', 'ʌ': 'a', 'ɖ': 'd', 'ʈ': 't', 'ɳ': 'n', 'ɭ': 'l', 'ɽ': 'r', 'ʂ': 's', 'ç': 'c'}
def norm(w):
    w = w.lower()
    w = ''.join(MAP.get(c, c) for c in w)
    w = unicodedata.normalize('NFD', w)
    w = ''.join(c for c in w if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', w)
def skel(n): return re.sub(r'[aeiou]', '', n)

def write(name, rows):
    """rows: list of (entry_id, headword, gloss)"""
    kept = []
    for eid, hw, gl in rows:
        n = norm(hw)
        if len(n) < 2 or not skel(n) or not gl.strip(): continue
        kept.append((str(eid), hw, n, skel(n), re.sub(r'\s+', ' ', gl).strip()[:400]))
    with open(f'{OUT}/lex/{name}.tsv', 'w', encoding='utf-8') as f:
        for k in kept: f.write('\t'.join(k) + '\n')
    log(f'{name}: {len(kept)} words in {len(set(k[0] for k in kept))} entries')
    return len(kept), len(set(k[0] for k in kept))

# ---------- DEDR ----------
LANGS = r'Ta|Ma|Ko|To|Ka|Koḍ|Tu|Te|Kol|Nk|Pa|Ga|Go|Kur|Malt|Br|Pe|Manḍ|Kuṛ|Kui|Kuwi|Konḍa|Koṇḍa|Pkt|Skt'
SPLIT = re.compile(r'(?:^|(?<=[\s(;.]))(' + LANGS + r')\.?\s(?=\S)')
WORDCH = re.compile(r"^[a-zA-ZÀ-ɏḀ-ỿ̀-ͯ·\-ʼ']+$")
POS = {'n.', 'adj.', 'adv.', 'v.', 'v.i.', 'v.t.', 'intr.', 'tr.', 'id.', 'pl.', 'interj.'}
def dedr():
    out = {'dedr_tamil': [], 'dedr_malayalam': [], 'dedr_kannada': [], 'dedr_telugu': []}
    want = {'Ta': 'dedr_tamil', 'Ma': 'dedr_malayalam', 'Ka': 'dedr_kannada', 'Te': 'dedr_telugu'}
    for line in open(f'{LX}/dedr/dedr_entries.tsv', encoding='utf-8'):
        eid, txt = line.rstrip('\n').split('\t', 1)
        txt = re.split(r'\s/\s*Cf\.|DED\(S\)|DEN\b|Previous Page| Cf\. \d', txt)[0]
        parts = SPLIT.split(txt)
        head_gloss = None
        for i in range(1, len(parts) - 1, 2):
            lang, seg = parts[i], parts[i + 1]
            seg = re.sub(r'\([^()]{0,60}\)', ' ', seg)
            prev = None
            for chunk in seg.split(';'):
                toks = chunk.strip().rstrip('.').split()
                if not toks: continue
                if toks[0] in POS and prev:
                    forms, gl = prev, ' '.join(toks[1:])
                else:
                    forms = []; k = 0
                    while k < len(toks):
                        t = toks[k]; k += 1
                        last = not t.endswith(',')
                        for f_ in t.rstrip(',').split('/'):
                            if WORDCH.match(f_) and f_ not in POS: forms.append(f_)
                        if last: break
                    gl = ' '.join(toks[k:])
                if not forms: continue
                prev = forms
                if lang == 'Ta' and head_gloss is None and gl: head_gloss = gl
                if lang in want:
                    for f_ in forms: out[want[lang]].append([eid, f_, gl])
        for k_ in out:   # cognate forms printed with no gloss of their own take the entry's first Tamil gloss
            for r in out[k_]:
                if r[0] == eid and not r[2]: r[2] = head_gloss or ''
    return out

# ---------- flat tsv lists ----------
def tsv(fn):
    by = collections.OrderedDict()
    for line in open(f'{LX}/tsv/{fn}', encoding='utf-8'):
        p = line.rstrip('\n').split('\t')
        if len(p) < 2: continue
        hw = p[0].strip()
        if ' ' in hw or len(hw) > 25: continue
        by.setdefault(hw, []).append(p[1])
    return [(i, hw, '; '.join(g)) for i, (hw, g) in enumerate(by.items())]

# ---------- Wiktionary (kaikki jsonl) ----------
def kaikki(fn, romanise):
    by = collections.OrderedDict()
    for line in open(f'{RAW}/{fn}', encoding='utf-8'):
        e = json.loads(line)
        gl = '; '.join(g for s in e.get('senses', []) for g in s.get('glosses', [])[:1])
        if not gl or gl.startswith(('alternative form', 'inflection of', 'plural of')): continue
        hw = e.get('word', '')
        if romanise:
            rom = [f['form'] for f in e.get('forms', []) if 'romanization' in f.get('tags', [])]
            if not rom: continue
            hw = rom[0]
        hw = hw.lstrip('*')
        if ' ' in hw: continue
        by.setdefault(hw, []).append(gl)
    return [(i, hw, '; '.join(g)) for i, (hw, g) in enumerate(by.items())]

sizes = []
for name, rows in dedr().items(): sizes.append((name, *write(name, rows)))
for name, fn in [('santali_campbell', 'santali_campbell.tsv'), ('santali_bodding5', 'santali_bodding_v5.tsv'),
                 ('santali_wiktionary', 'santali_wiktionary.tsv'), ('mundari_bhadra', 'mundari_bhadra.tsv'),
                 ('sumerian_halloran', 'sumerian_halloran.tsv'), ('sumerian_wiktionary', 'sumerian_wiktionary.tsv'),
                 ('sanskrit_mw', 'sanskrit_monier_williams.tsv'), ('oia_turner', 'indoaryan_turner.tsv'),
                 ('elamite_hinzkoch', 'elamite_hinzkoch.tsv'), ('burushaski_lorimer', 'burushaski_werchikwar_yasin.tsv')]:
    sizes.append((name, *write(name, tsv(fn))))
for name, fn, rom in [('tamil_wiktionary', 'Tamil.jsonl', True), ('telugu_wiktionary', 'Telugu.jsonl', True),
                      ('kannada_wiktionary', 'Kannada.jsonl', True), ('akkadian_wiktionary', 'Akkadian.jsonl', False),
                      ('proto_indoiranian_wiktionary', 'Proto-Indo-Iranian.jsonl', False)]:
    sizes.append((name, *write(name, kaikki(fn, rom))))
with open(f'{OUT}/lex_sizes.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['dictionary', 'words', 'entries']); w.writerows(sizes)
log('done')
