#!/usr/bin/env python3
"""Sign list step 5 yardsticks, built from raw open data where no published top-50 figure was found.

1. UR III CUNEIFORM (Sumerian, 21st century BC), CDLI open data (github cdli-gh/data: cdliatf_unblocked.atf, cdli_cat.csv;
   download to /tmp/cdli/). Texts whose catalogue period starts 'Ur III'. Every transliterated reading is turned into its
   cuneiform sign through the Nuolenna sign list (github tosaja/Nuolenna sign_list.txt, reading -> Unicode sign), so two
   readings of one sign count as one sign. A numeral like 3(disz) is one sign token '3(disz)'. Readings the list does not
   know are dropped and counted. Broken / restored marks (# ? ! [ ] < >) are stripped; 'x' and '...' are dropped.
2. LINEAR B word list (types, not running text): the hyphenated transliterations of the Linear B Lexicon on archive.org
   (LinearBLexicon djvu text, /tmp/linb/lex2.txt), syllabograms counted over distinct words.
For each: signs, tokens, used once, signs covering 50 / 80 / 95%, top-50 share; and for Ur III the same after drawing whole
texts at random until the token count equals the Indus first catalogue (17,034), 200 draws, and its growth (distinct signs
at 25% / 50% / 100% of that sample).
Run: python3 -I work_scripts/signlist_6_yardsticks.py   Output: work_data/signlist/yardsticks.csv, log_yardsticks.txt
"""
import re, csv, collections, sys, os
import numpy as np
OUT = '/home/antigravity/Cuuper22/ivc/work_data/signlist'
fh = open(f'{OUT}/log_yardsticks.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); fh.write(s + '\n'); fh.flush()

SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
def norm(r):
    r = r.lower().replace('sz', 'š').replace('s,', 'ṣ').replace('t,', 'ṭ').replace("s'", 'ś').replace('j', 'ŋ')
    r = r.replace('h', 'ḫ')
    m = re.match(r'^([^\d]+)(\d+)$', r)
    if m: r = m.group(1) + m.group(2).translate(SUB)
    return r
SL = {}
for line in open('/tmp/cdli/sl.txt', encoding='utf-8'):
    p = line.rstrip('\n').split('\t')
    if len(p) == 2: SL[p[0]] = p[1]
ids = set(open('/tmp/cdli/ur3_ids.txt').read().split())
texts = []; cur = None; unknown = collections.Counter(); known = 0
for line in open('/tmp/cdli/atf.atf', encoding='utf-8', errors='ignore'):
    if line.startswith('&P'):
        pid = line[2:8].lstrip('0') or '0'
        cur = [] if pid in ids else None
        if cur is not None: texts.append(cur)
        continue
    if cur is None or not re.match(r'^\d+[\'.]', line): continue
    body = line.split('.', 1)[1] if '.' in line else ''
    for w in body.split():
        w = re.sub(r'[#?!\[\]<>*]', '', w)
        if not w or w in ('...', 'x', ',', '|', '$', '...]'): continue
        w = w.replace('{', '-').replace('}', '-')
        for part in re.split(r'[-.:+]', w):
            if not part or part in ('x', '...', 'X'): continue
            m = re.match(r'^(\d+(?:/\d+)?)\((\w+)\)$', part)
            if m: cur.append(f'{m.group(1)}({m.group(2).lower()})'); known += 1; continue
            if re.match(r'^\d', part) or '(' in part or '|' in part or '~' in part: unknown[part] += 1; continue
            n = norm(part)
            if n not in SL: n = n.replace('ḫ', 'h')
            if n in SL: cur.append(SL[n]); known += 1
            else: unknown[n] += 1
texts = [t for t in texts if t]
say(f'Ur III texts with signs: {len(texts)}; sign tokens kept {known}; readings dropped {sum(unknown.values())} '
    f'({sum(unknown.values()) / (known + sum(unknown.values())):.1%}); commonest dropped: {unknown.most_common(8)}')

def stats(counter, label):
    c = np.array(sorted(counter.values(), reverse=True)); tot = c.sum(); cum = np.cumsum(c) / tot
    d = dict(system=label, signs=len(c), tokens=int(tot), used_once=int((c == 1).sum()),
             cover50=int(np.searchsorted(cum, .5) + 1), cover80=int(np.searchsorted(cum, .8) + 1), cover95=int(np.searchsorted(cum, .95) + 1),
             top50_share=round(float(cum[min(49, len(c) - 1)]), 3))
    say(label, d); return d
rows = []; MATCH = {}
allc = collections.Counter(s for t in texts for s in t)
rows.append(stats(allc, 'Ur III cuneiform, all texts'))
rng = np.random.default_rng(3)
target = 17034; draws = []
for i in range(200):
    order = rng.permutation(len(texts)); c = collections.Counter(); n = 0; seen_at = {}
    for j in order:
        c.update(texts[j]); n += len(texts[j])
        for frac in (0.25, 0.5):
            if frac not in seen_at and n >= frac * target: seen_at[frac] = len(c)
        if n >= target: break
    v = np.array(sorted(c.values(), reverse=True)); cum = np.cumsum(v) / v.sum()
    draws.append((len(c), int((v == 1).sum()), float(cum[49]), int(np.searchsorted(cum, .5) + 1), int(np.searchsorted(cum, .8) + 1),
                  int(np.searchsorted(cum, .95) + 1), seen_at[0.25], seen_at[0.5]))
D = np.array(draws)
rows.append(dict(system='Ur III cuneiform, random texts to 17,034 tokens (200 draws, mean)', signs=round(D[:, 0].mean(), 1), tokens=target,
                 used_once=round(D[:, 1].mean(), 1), cover50=round(D[:, 3].mean(), 1), cover80=round(D[:, 4].mean(), 1),
                 cover95=round(D[:, 5].mean(), 1), top50_share=round(D[:, 2].mean(), 3),
                 at25=round(D[:, 6].mean(), 1), at50=round(D[:, 7].mean(), 1)))
say('Ur III at Indus size:', rows[-1])
# Proto-cuneiform (Uruk IV and III) and proto-Elamite: CDLI writes sign NAMES (ABGAL, M288, |M327+M342|), so each name is
# one sign; variant suffixes (~a, ~b) are dropped (variants merged, as the Indus merge does); a numeral n(Nxx) is one token
# 'Nxx' (a numeral sign kind; repeated units of one kind count once per notation); stats with and without numerals.
def names(idfile):
    keep = set(open(idfile).read().split()); T = []; cur = None
    for line in open('/tmp/cdli/atf.atf', encoding='utf-8', errors='ignore'):
        if line.startswith('&P'):
            pid = line[2:8].lstrip('0') or '0'; cur = [] if pid in keep else None
            if cur is not None: T.append(cur)
            continue
        if cur is None or not re.match(r'^\d+[A-Z]?[\'.]', line): continue
        body = line.split(' ', 1)[1] if ' ' in line else ''
        for w in body.split():
            w = re.sub(r'[#?!\[\]<>*]', '', w)
            if not w or w in (',', '...', 'X', 'x', '$'): continue
            m = re.match(r'^\d+(?:/\d+)?\((N\w+)\)$', w)
            if m: cur.append('#' + re.sub(r'~.*', '', m.group(1))); continue
            if w.startswith('|') or re.match(r'^[A-Z][A-Z0-9@~_&+.]*$', w):
                cur.append(re.sub(r'~\w+', '', w))
    return [t for t in T if t]
for idf, label in (('/tmp/cdli/uruk_ids.txt', 'Proto-cuneiform (Uruk IV-III)'), ('/tmp/cdli/pe_ids.txt', 'Proto-Elamite')):
    T = names(idf)
    say(f'{label}: {len(T)} texts')
    for lab2, TT in ((label + ', all signs', T), (label + ', without numerals', [[x for x in t if not x.startswith('#')] for t in T])):
        TT = [t for t in TT if t]
        c = collections.Counter(x for t in TT for x in t)
        rows.append(stats(c, lab2))
        if 'without' in lab2: MATCH[label] = TT

# size-matched: every system's texts drawn at random until 10,583 tokens (the proto-Elamite non-numeral total), 200 draws
MATCH['Indus, true signs (this job)'] = [l.split() for l in open(f'{OUT}/indus_true_tokens.txt')]
MATCH['Ur III cuneiform'] = texts
target = sum(len(t) for t in MATCH['Proto-Elamite'])
for label, TT in MATCH.items():
    rng = np.random.default_rng(11); R = []
    for i in range(200):
        c = collections.Counter(); n = 0
        for j in rng.permutation(len(TT)):
            c.update(TT[j]); n += len(TT[j])
            if n >= target: break
        v = np.array(sorted(c.values(), reverse=True)); cum = np.cumsum(v) / v.sum()
        R.append((len(c), (v == 1).sum(), cum[49], np.searchsorted(cum, .5) + 1, np.searchsorted(cum, .95) + 1))
    R = np.array(R, dtype=float)
    d = dict(system=f'{label}, at {target} tokens (200 draws, mean)', signs=round(R[:, 0].mean(), 1), tokens=target, used_once=round(R[:, 1].mean(), 1),
             cover50=round(R[:, 3].mean(), 1), cover95=round(R[:, 4].mean(), 1), top50_share=round(R[:, 2].mean(), 3))
    say('matched:', d); rows.append(d)

# Linear B word list
t = open('/tmp/linb/lex2.txt', encoding='utf-8', errors='ignore').read()
words = set(re.findall(r'(?<![\w-])((?:[aeiou]|[dkmnpqrstwjzh]{1,2}[aeiou]\d?)(?:-(?:[aeiou]|[dkmnpqrstwjzh]{1,2}[aeiou]\d?))+)(?![\w-])', t))
lb = collections.Counter(s for w in words for s in w.split('-'))
say(f'Linear B word list: {len(words)} distinct words')
rows.append(stats(lb, 'Linear B syllabograms, word list types'))
with open(f'{OUT}/yardsticks.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=sorted({k for r in rows for k in r}, key=lambda k: list(rows[1]).index(k) if k in rows[1] else 99)); w.writeheader(); w.writerows(rows)
