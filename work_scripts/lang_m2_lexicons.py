#!/usr/bin/env python3
"""lang_m2 step 0: HOMONYM-AWARE DICTIONARIES.  Same table format as lang_m (entry id, headword, normalised form, skeleton, gloss);
the only change is the ENTRY ID, so that two words spelled alike count as two words when the dictionary itself prints them as two.

Where the source keeps homonyms apart (used here):
  DEDR (Tamil, Malayalam, Kannada, Telugu)  entry number = one etymon; copied unchanged from work_data/lang_m/lex/.
  Monier-Williams Sanskrit                  <hom>n</hom> numbers in mw.xml: entry = key1 + homonym number; sense lines (H1A, H2A ...)
                                            belong to the entry of their L-number's whole part.  Rows = one per entry, glosses joined.
  Wiktionary (Tamil, Telugu, Kannada, Akkadian, Proto-Indo-Iranian, Sumerian, Santali; kaikki.org dumps already on disk)
                                            entry = original word (cuneiform / script) + etymology_number.  The same romanised spelling
                                            under two etymologies, or written with two different cuneiform signs (Sumerian du / du3 /
                                            du7 ...), is two entries.  Parts of speech of one etymology are one entry.
  Halloran Sumerian Lexicon                 one entry per printed headword line (the sign index, e.g. du3, is dropped from the form but
                                            kept apart as an entry: this is the ePSD-style homonym index; ePSD itself is unreachable).
  Turner CDIAL (Old Indo-Aryan)             one entry per numbered headword line (CDIAL prints homonyms as separate numbered entries).
Not possible (copied unchanged from work_data/lang_m/lex/, same-spelled words stay merged): Santali Campbell, Santali Bodding vol 5,
  Mundari Bhadra (OCR prints no homonym numbers), Elamite Hinz-Koch, Burushaski Lorimer.
Output: /tmp/lang_m2/lex/<dict>.tsv (the Sanskrit table is ~30 MB, so all tables live in /tmp; rerun this script to rebuild) and
        work_data/lang_m2/lex_sizes.csv (words, entries, and how many normalised forms are shared by 2+ entries = strict homophones).
"""
import os, re, csv, json, html, shutil, unicodedata, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = '/home/claude/ivc'; LX = f'{ROOT}/work_data/lexicons'; M1 = f'{ROOT}/work_data/lang_m'
OUT = '/tmp/lang_m2/lex'; REP = f'{ROOT}/work_data/lang_m2'
os.makedirs(OUT, exist_ok=True); os.makedirs(REP, exist_ok=True)
def log(*a): print('[lang_m2_lexicons]', *a, flush=True)

MAP = {'ŋ': 'ng', 'ə': 'a', 'ɛ': 'e', 'ɔ': 'o', 'ʃ': 's', 'ß': 'ss', 'ø': 'o', 'æ': 'ae', 'ı': 'i', 'ł': 'l', 'đ': 'd', 'ʔ': '', 'ʼ': '',
       '¢': 'ng', '§': 's', 'ɨ': 'i', 'ʌ': 'a', 'ɖ': 'd', 'ʈ': 't', 'ɳ': 'n', 'ɭ': 'l', 'ɽ': 'r', 'ʂ': 's', 'ç': 'c'}
def norm(w):   # identical to lang_m_lexicons.norm
    w = w.lower(); w = ''.join(MAP.get(c, c) for c in w)
    w = unicodedata.normalize('NFD', w); w = ''.join(c for c in w if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', w)
def skel(n): return re.sub(r'[aeiou]', '', n)

sizes = []
def write(name, rows, how):
    kept = []
    for eid, hw, gl in rows:
        n = norm(hw)
        if len(n) < 2 or not skel(n) or not gl.strip(): continue
        kept.append((str(eid), hw, n, skel(n), re.sub(r'\s+', ' ', gl).strip()[:240]))
    with open(f'{OUT}/{name}.tsv', 'w', encoding='utf-8') as f:
        for k in kept: f.write('\t'.join(k) + '\n')
    by = collections.defaultdict(set)
    for k in kept: by[k[2]].add(k[0])
    homo = sum(1 for v in by.values() if len(v) > 1)
    sizes.append((name, len(kept), len({k[0] for k in kept}), homo, how))
    log(f'{name}: {len(kept)} words in {len({k[0] for k in kept})} entries; forms shared by 2+ entries {homo} ({how})')

def copy(name, how):
    rows = [l.rstrip('\n').split('\t') for l in open(f'{M1}/lex/{name}.tsv', encoding='utf-8')]
    write(name, [(r[0], r[1], r[4]) for r in rows], how)

for n in ['dedr_tamil', 'dedr_malayalam', 'dedr_kannada', 'dedr_telugu']: copy(n, 'kept apart: DEDR entry numbers')

def kaikki(path, romanise, rom_fallback_word=False):
    by = collections.OrderedDict()
    for line in open(path, encoding='utf-8'):
        e = json.loads(line)
        gl = '; '.join(g for s in e.get('senses', []) for g in s.get('glosses', [])[:1])
        if not gl or gl.lower().startswith(('alternative form', 'inflection of', 'plural of', 'romanization of')): continue
        word = e.get('word', '')
        hw = word
        if romanise:
            rom = [f['form'] for f in e.get('forms', []) if 'romanization' in f.get('tags', [])]
            if rom: hw = rom[0]
            elif not rom_fallback_word: continue
        hw = hw.lstrip('*')
        if ' ' in hw: continue
        key = (hw, word, e.get('etymology_number', 0))
        by.setdefault(key, []).append(gl)
    return [(f'{w}#{et}', hw, '; '.join(g)) for (hw, w, et), g in by.items()]

for name, fn, rom, fb in [('tamil_wiktionary', f'{M1}/raw/Tamil.jsonl', True, False), ('telugu_wiktionary', f'{M1}/raw/Telugu.jsonl', True, False),
                          ('kannada_wiktionary', f'{M1}/raw/Kannada.jsonl', True, False), ('akkadian_wiktionary', f'{M1}/raw/Akkadian.jsonl', False, False),
                          ('proto_indoiranian_wiktionary', f'{M1}/raw/Proto-Indo-Iranian.jsonl', False, False),
                          ('sumerian_wiktionary', f'{LX}/raw/kaikki_sumerian.jsonl', True, True),
                          ('santali_wiktionary', f'{LX}/raw/kaikki_santali.jsonl', True, True)]:
    write(name, kaikki(fn, rom, fb), 'kept apart: Wiktionary etymology number and original script')

# ---- Monier-Williams with homonym numbers
SL = {'A': 'ā', 'I': 'ī', 'U': 'ū', 'f': 'ṛ', 'F': 'ṝ', 'x': 'ḷ', 'X': 'ḹ', 'E': 'ai', 'O': 'au', 'K': 'kh', 'G': 'gh', 'N': 'ṅ', 'C': 'ch',
      'J': 'jh', 'Y': 'ñ', 'w': 'ṭ', 'W': 'ṭh', 'q': 'ḍ', 'Q': 'ḍh', 'R': 'ṇ', 'T': 'th', 'D': 'dh', 'P': 'ph', 'B': 'bh', 'S': 'ś', 'z': 'ṣ',
      'M': 'ṃ', 'H': 'ḥ', 'L': 'ḷ'}
def mw():
    p = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml'
    ent = collections.OrderedDict(); lmap = {}
    for line in open(p, encoding='utf-8'):
        m = re.search(r'<key1>([^<]+)</key1>(.*?)</h><body>(.*?)</body>.*?<L>([\d.]+)</L>', line)
        if not m: continue
        key, hpart, body, L = m.groups()
        hm = re.search(r'<hom>(\d+)</hom>', hpart)
        Lw = L.split('.')[0]
        if '.' in L and Lw in lmap: eid = lmap[Lw]          # a sense line of an entry already opened
        else:
            eid = f'{key}#{hm.group(1)}' if hm else key; lmap[Lw] = eid
        b = re.sub(r'<(s|ls|ab|lex)\b[^>]*>.*?</\1>', ' ', body); b = re.sub(r'<[^>]+>', ' ', html.unescape(b))
        b = re.sub(r'\s+', ' ', b).strip(' ,;'); b = re.split(r'[.\[]', b)[0].strip()[:120].lower()
        if not b: continue
        e = ent.setdefault(eid, [''.join(SL.get(c, c) for c in key), []])
        if len(e[1]) < 4: e[1].append(b)
    return [(eid, hw, '; '.join(g)) for eid, (hw, g) in ent.items()]
write('sanskrit_mw', mw(), 'kept apart: Monier-Williams homonym numbers')

# ---- Halloran with one entry per printed headword line (same parse as rival_lexicons.halloran, plus the entry id)
def nfc(s): return unicodedata.normalize('NFC', s)
def first_gloss(t, cap=200):
    t = re.sub(r'\s+', ' ', t).strip(); t = re.sub(r'(\w)- (\w)', r'\1\2', t)
    return re.match(r'([^.]*)', t).group(1).strip()[:cap].lower()
def halloran():
    L = open(f'{LX}/raw/sumerian_201604.txt', encoding='utf8', errors='ignore').read().split('\n')[205:]
    rows = []; cur = []; eno = 0
    POS = r"(?:n|v|adj|adv|prep|conj|pron|num|part)"
    for l in L:
        l = nfc(l).strip()
        if not l or l.startswith('Sumerian Lexicon'): continue
        m = re.match(r"^(%s)\.,?\s*(.*)$" % POS, l)
        if m and cur:
            g = first_gloss(m.group(2).replace(';', ','))
            if g: rows += [(f'{eno}:{k}', h, g) for k, h in enumerate(cur)]
            continue
        m = re.match(r"^([^:—\[\]]{1,45}?)\s*(?::|—|–)\s*(.*)$", l)
        if m and not re.match(r'^\(?cf', m.group(2)):
            heads = [re.sub(r'[^a-zšĝḫ]', '', re.sub(r'\(.*?\)', '', t).lower()) for t in re.split(r'[,;]', m.group(1))]
            heads = [h for h in heads if len(h) >= 2 and h not in ('and', 'prep', 'adj', 'see', 'also')][:3]
            t = re.sub(r"^(?:(?:%s)\.,?\s*)+" % POS, '', m.group(2).strip())
            g = first_gloss(t.replace(';', ',')); cur = heads; eno += 1
            if heads and g: rows += [(f'{eno}:{k}', h, g) for k, h in enumerate(heads)]
    # merge sense lines of one entry/head into one row
    by = collections.OrderedDict()
    for eid, h, g in rows: by.setdefault((eid, h), []).append(g)
    return [(eid.split(':')[0], h, '; '.join(g)) for (eid, h), g in by.items()]
write('sumerian_halloran', halloran(), 'kept apart: one entry per Halloran headword line (sign index)')

def turner():
    L = [nfc(l).strip() for l in open(f'{LX}/raw/turner_cdial.txt', encoding='utf8', errors='ignore').read().split('\n')]; rows = []
    head = re.compile(r"^\*?([a-zA-Zāīūṛṝḷṃṭḍṇśṣḥñĉčĝ̀-ͯ]{2,25})-(?:\s|$)")
    for i, l in enumerate(L):
        m = head.match(l)
        if not m: continue
        t = ' '.join(x for x in L[i:i + 3] if x)
        g = re.search(r"^[^‘'’]{0,40}[‘'’]([^'’‘]{2,80})[’']", t[m.end():])
        if g: rows.append((i, m.group(1), g.group(1).lower()))
    seen = set(); out = []
    for i, h, g in rows:                     # the same (headword, gloss) printed twice is one entry (OCR repeats)
        if (h, g) in seen: continue
        seen.add((h, g)); out.append((i, h, g))
    return out
write('oia_turner', turner(), 'kept apart: one entry per CDIAL headword line')

for n in ['santali_campbell', 'santali_bodding5', 'mundari_bhadra', 'elamite_hinzkoch', 'burushaski_lorimer']:
    copy(n, 'merged: source prints no homonym numbers (flat list)')

with open(f'{REP}/lex_sizes.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['dictionary', 'words', 'entries', 'forms_shared_by_2plus_entries', 'homonyms']); w.writerows(sizes)
log('done')
