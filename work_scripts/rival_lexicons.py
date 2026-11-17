"""Turn every downloaded dictionary into one plain table per language: headword TAB first-sense gloss (lower case).
Run from /home/claude/ivc:  python3 work_scripts/rival_lexicons.py
Input : work_data/lexicons/raw/*   (downloads, see work_data/lexicons/SOURCES.md)   /tmp/dedr/dedr_text.txt (DEDR, from lang_dedr_fetch.py)
Output: work_data/lexicons/tsv/<name>.tsv   and a size report on screen.
A gloss is the text after the headword up to the first full stop (cap 200 characters), like the Tamil gloss of lang_pun_chance.py."""
import re, os, json, html, glob, unicodedata, collections
RAW = 'work_data/lexicons/raw'; OUT = 'work_data/lexicons/tsv'
os.makedirs(OUT, exist_ok=True)
def nfc(s): return unicodedata.normalize('NFC', s)
def first_gloss(t, cap=200):
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'(\w)- (\w)', r'\1\2', t)          # re-join words hyphenated at a line end
    m = re.match(r'([^.]*)', t)
    return m.group(1).strip()[:cap].lower()
def save(name, rows):
    seen = set(); out = []
    for h, g in rows:
        h = h.strip(); g = g.strip()
        if len(h) < 2 or not g: continue
        if (h, g) in seen: continue
        seen.add((h, g)); out.append((h, g))
    with open(f'{OUT}/{name}.tsv', 'w', encoding='utf8') as o:
        for h, g in out: o.write(f'{h}\t{g}\n')
    print(f'{name:28s} {len(out):7d} entries, {len(set(h for h,_ in out)):7d} distinct headwords')

def read_lines(f): return open(f, encoding='utf8', errors='ignore').read().split('\n')

# --- Dravidian: Tamil side of DEDR, identical parse to lang_pun_chance.py
def dedr():
    rows = []
    seen = set()
    for line in open('/tmp/dedr/dedr_text.txt', encoding='utf8'):
        m = re.match(r"^(\d+[a-z]?) Ta\. ([^\s,;(]+)\s+([^.]*)", nfc(line))
        if m and len(m.group(2)) >= 2 and m.group(3) and m.group(1) not in seen:
            seen.add(m.group(1)); rows.append((m.group(2), m.group(3).lower()))
    rows.append(('āḷ', 'man, servant')); rows.append(('maram', 'tree'))   # the two entries lang_pun_chance.py adds by hand
    save('dravidian_tamil_dedr', rows)

# --- Santali: Campbell 1899 (Santali-English), "Headword.  Gloss" at line start
def campbell():
    L = [l for l in read_lines(f'{RAW}/campbell_santali_english_1899.txt')]
    rows = []; cur = None; buf = []
    def flush():
        if cur: rows.append((cur, first_gloss(' '.join(buf))))
    for l in L:
        l = re.sub(r'\s+', ' ', nfc(l)).strip()
        if not l: continue
        m = re.match(r"^([A-Z][A-Za-z'’]{1,17})\. (\S.*)$", l)
        if m and not re.match(r'^(The|This|That|Cf|See|Ma|Is|It|He|She|In|On|To|An|Of|If|We|You|My|Do|No|Go|So|At|By|Be|As)$', m.group(1)):
            flush(); cur = m.group(1).lower(); buf = [m.group(2)]
        elif cur: buf.append(l)
    flush()
    save('santali_campbell', rows)

# --- Santali: Bodding, A Santal Dictionary vol 5 (1936), "headword, pos. gloss"
def bodding():
    L = read_lines(f'{RAW}/santal_dict_v5_bodding.txt'); rows = []; cur = None; buf = []
    POS = r"(?:n|v|adj|adv|prep|conj|num|pron|interj|part|a)\."
    def flush():
        if cur:
            t = ' '.join(buf)
            t = re.sub(r"^(?:(?:%s|[a-z]\.|m\.|f\.|s\.|t\.|r\.|[,;]|\s)+)" % POS, '', t)
            rows.append((cur, first_gloss(t)))
    for l in L:
        l = nfc(l).strip()
        if not l: continue
        m = re.match(r"^([a-zàáâèéêìíîòóôùúûḍṇṭñŋṅɛɔ'’][a-zàáâèéêìíîòóôùúûḍṇṭñŋṅɛɔ'’\-]{1,20})(?: \([^)]*\))?\s*,\s+((?:%s|[a-z]\.)\s*.*)$" % POS, l)
        if m: flush(); cur = m.group(1); buf = [m.group(2)]
        elif cur: buf.append(l)
    flush(); save('santali_bodding_v5', rows)

# --- Santali: Wiktionary (kaikki.org dump), romanised headword
def kaikki(src, name, lang):
    rows = []
    for l in open(f'{RAW}/{src}', encoding='utf8'):
        d = json.loads(l)
        rom = [f['form'] for f in d.get('forms', []) if 'romanization' in f.get('tags', [])]
        h = rom[0] if rom else d['word']
        for s in d['senses'][:2]:
            g = s.get('glosses') or []
            if g and not g[0].startswith('romanization of'): rows.append((h, g[0].lower()[:200]))
    save(name, rows)

# --- Mundari: Bhadra, Mundari-English dictionary (Calcutta 1931), "Headword—gloss"
def mundari():
    L = read_lines(f'{RAW}/mundari_english_calcutta.txt'); rows = []; cur = None; buf = []
    def flush():
        if cur: rows.append((cur, first_gloss(' '.join(buf).replace(';', ',').replace(' : ', ', '))))
    for l in L:
        l = nfc(l).strip()
        if not l: continue
        m = re.match(r"^([A-Z][A-Za-zàāèéìíòóùúḍṭ'’&\-]{1,20})(?:\s*[0-9]*)?\s*[—–-]\s*(\S.*)$", l)
        if m: flush(); cur = m.group(1).lower(); buf = [m.group(2)]
        elif cur and not re.match(r'^\d+$|MUNDARI-ENGLISH', l): buf.append(l)
    flush(); save('mundari_bhadra', rows)

# --- Burushaski (Hunza): Barken-Burushaski dictionary 2023, "headword : script [ipa] POS. gloss"
def barken():
    L = read_lines(f'{RAW}/burushaski_barken.txt'); rows = []; cur = None; buf = []
    def flush():
        if cur:
            t = ' '.join(buf)
            t = re.sub(r'^.*?\]\s*', '', t, count=1) if ']' in t[:80] else t
            t = re.sub(r'^(?:(?:N|V|ADJ|ADV|INT|PRON|PREP|CONJ|NUM|IMP|GER|PFX|SFX|POSTP|DET|PL|SG|[./A-Z]+)\.?\s*)+', '', t)
            rows.append((cur, first_gloss(t)))
    for l in L:
        l = nfc(l).strip()
        if not l: continue
        m = re.match(r"^([A-Za-z][A-Za-z'’:*\-]{1,20})\s*:\s*(.*)$", l)
        if m: flush(); cur = re.sub(r'[*:]', '', m.group(1)).lower(); buf = [m.group(2)]
        elif cur: buf.append(l)
    flush(); save('burushaski_barken_hunza', rows)

# --- Burushaski (Yasin): Lorimer's Werchikwar-English Vocabulary 1962 (re-OCR by rival_ocr_werchikwar.py)
def werchikwar(f):
    L = read_lines(f); rows = []; cur = None; buf = []
    def flush():
        if cur: rows.append((cur, first_gloss(' '.join(buf))))
    for l in L:
        l = nfc(l).strip()
        if not l: continue
        # entry: headword (possibly with a leading star or number), then a comma or class mark, then English
        m = re.match(r"^(?:\d+\.\s*)?\*?([a-zA-Zɛɔṭḍṇśṣḥ’'\-]{2,18})(?:\s*,\s*[^.]{0,40}?)?\s*,?\s*\b(n|v\.t|v\.i|v|adj|adv|s)\.(?:\s*[a-z]+\.)?,?\s+(.+)$", l)
        if m: flush(); cur = m.group(1).lower(); buf = [m.group(3)]
        elif cur: buf.append(l)
    flush(); save('burushaski_werchikwar_yasin', rows)

# --- Sumerian: Halloran's Sumerian Lexicon v3 (English). "reading, reading: n., gloss" then "v., gloss" lines for the same word
def halloran():
    L = read_lines(f'{RAW}/sumerian_201604.txt')[205:]; rows = []; cur = []     # lines before 205 are the introduction
    POS = r"(?:n|v|adj|adv|prep|conj|pron|num|part)"
    for l in L:
        l = nfc(l).strip()
        if not l or l.startswith('Sumerian Lexicon'): continue
        m = re.match(r"^(%s)\.,?\s*(.*)$" % POS, l)
        if m and cur:                                      # another sense line of the current word
            g = first_gloss(m.group(2).replace(';', ','))
            if g: rows += [(h, g) for h in cur]
            continue
        m = re.match(r"^([^:—\[\]]{1,45}?)\s*(?::|—|–)\s*(.*)$", l)
        if m and not re.match(r'^\(?cf', m.group(2)):
            heads = [re.sub(r'[^a-zšĝḫ]', '', re.sub(r'\(.*?\)', '', t).lower()) for t in re.split(r'[,;]', m.group(1))]
            heads = [h for h in heads if len(h) >= 2 and h not in ('and', 'prep', 'adj', 'see', 'also')][:3]
            t = re.sub(r"^(?:(?:%s)\.,?\s*)+" % POS, '', m.group(2).strip())
            g = first_gloss(t.replace(';', ','))
            cur = heads
            if heads and g: rows += [(h, g) for h in heads]
        else: cur = cur
    save('sumerian_halloran', rows)

# --- Elamite: Hinz and Koch, Elamisches Woerterbuch 1987 (German); headword with hyphens, dialect tag, German gloss. Personal names left out.
def elamite():
    rows = []
    for f in ('elamisches_hinz_koch_1.txt', 'elamisches_hinz_koch_2.txt'):
        L = read_lines(f'{RAW}/{f}'); cur = None; buf = []
        def flush():
            if cur: rows.append((cur, first_gloss(' '.join(buf))))
        for l in L:
            l = nfc(l).strip()
            if not l: continue
            m = re.match(r"^(?:[tfiIlr~\^\.]{0,3}|(?:v|h|hh|d|m|f|s|hw|tih|tuh)\.)\s*([a-zšḫṣṭ][a-zšḫṣṭ0-9\-]{1,30})\s+((?:a|m|n|ach|s)?[ES]|aB|sB|[mn]?E|achE|aE-sum\.)[,.]?\s+(\S.*)$", l)
            if m and not re.search(r'N\.pr|Ortsname|Gottheit', l[:70]):
                flush(); cur = m.group(1).lower(); buf = [m.group(3)]
            elif cur and not re.match(r'^(?:\S+ ){0,2}\d+:\d+', l): buf.append(l)
        flush()
    save('elamite_hinzkoch', rows)

# --- Indo-Aryan: Turner's Comparative Dictionary of the Indo-Aryan Languages (OCR), "NUMBER headword- pos. 'gloss'"
def turner():
    L = [nfc(l).strip() for l in read_lines(f'{RAW}/turner_cdial.txt')]; rows = []
    head = re.compile(r"^\*?([a-zA-Zāīūṛṝḷṃṭḍṇśṣḥñĉčĝ\u0300-\u036f]{2,25})-(?:\s|$)")
    for i, l in enumerate(L):
        m = head.match(l)
        if not m: continue
        t = ' '.join(x for x in L[i:i + 3] if x)
        g = re.search(r"^[^‘'’]{0,40}[‘'’]([^'’‘]{2,80})[’']", t[m.end():])
        if g: rows.append((m.group(1), g.group(1).lower()))
    save('indoaryan_turner', rows)

SL = {'A':'ā','I':'ī','U':'ū','f':'ṛ','F':'ṝ','x':'ḷ','X':'ḹ','E':'ai','O':'au','K':'kh','G':'gh','N':'ṅ','C':'ch','J':'jh','Y':'ñ','w':'ṭ','W':'ṭh','q':'ḍ','Q':'ḍh','R':'ṇ','T':'th','D':'dh','P':'ph','B':'bh','S':'ś','z':'ṣ','M':'ṃ','H':'ḥ','L':'ḷ'}
def slp1_to_iast(w): return ''.join(SL.get(c, c) for c in w)
# --- Indo-Aryan: Monier-Williams (the file the earlier Sanskrit run used), SLP1 key, English gloss
def mw():
    p = 'evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml'
    if not os.path.exists(p): print('mw.xml not on disk, skipped'); return
    rows = []
    for line in open(p, encoding='utf-8'):
        m = re.search(r'<key1>([^<]+)</key1>.*?<body>(.*?)</body>', line)
        if not m: continue
        b = re.sub(r'<(s|ls|ab|lex)\b[^>]*>.*?</\1>', ' ', m.group(2)); b = re.sub(r'<[^>]+>', ' ', html.unescape(b))
        b = re.sub(r'\s+', ' ', b).strip(' ,;')
        b = re.split(r'[.\[]', b)[0].strip()[:200].lower()
        if b: rows.append((slp1_to_iast(m.group(1)), b))
    save('sanskrit_monier_williams', rows)

if __name__ == '__main__':
    import sys
    dedr(); campbell(); bodding(); kaikki('kaikki_santali.jsonl', 'santali_wiktionary', 'sat'); mundari(); barken()
    if os.path.exists('/tmp/werch/ocr/all.txt'): werchikwar('/tmp/werch/ocr/all.txt')
    halloran(); kaikki('kaikki_sumerian.jsonl', 'sumerian_wiktionary', 'sux'); elamite(); turner(); mw()
