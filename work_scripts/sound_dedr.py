#!/usr/bin/env python3
"""Look up Tamil forms in the local DEDR copy (work_data/lexicons/dedr/dedr_entries.tsv).
usage: python3 sound_dedr.py word1 word2 ...   -> entry numbers + opening of each entry that has the
word as a whole token in its Tamil (Ta.) part."""
import re, sys, unicodedata
F = '/home/antigravity/Cuuper22/ivc/work_data/lexicons/dedr/dedr_entries.tsv'
E = []
for line in open(F, encoding='utf-8'):
    if '\t' in line:
        n, t = line.rstrip('\n').split('\t', 1); E.append((n, unicodedata.normalize('NFC', t)))
def ta_part(t):
    m = re.search(r'Ta\. (.*?)(?= (?:Ma|Ko|To|Ka|Koḍ|Tu|Te|Kol|Nk|Pa|Ga|Go|Konḍa|Kui|Kuwi|Kur|Malt|Br|Ir|Kur)\. |$)', t)
    return m.group(1) if m else ''
def look(w, n=230):
    w = unicodedata.normalize('NFC', w); rx = re.compile(r'(?<![\wḷḻṟṉṇṭṅñāīūēō])' + re.escape(w) + r'(?![\wḷḻṟṉṇṭṅñāīūēō])')
    return [(k, t[:n]) for k, t in E if rx.search(ta_part(t))]
if __name__ == '__main__':
    for w in sys.argv[1:]:
        r = look(w)
        print(f'== {w}: {len(r)} entries')
        for k, t in r[:4]: print(f'  {k}: {t}')
