"""grep the local DEDR text (built by lang_dedr_fetch.py).
usage: python3 lang_dedr_grep.py REGEX [maxchars]"""
import re, sys, unicodedata
rx = re.compile(unicodedata.normalize("NFC", sys.argv[1])); n = int(sys.argv[2]) if len(sys.argv) > 2 else 400
seen=set()
for line in open('/tmp/dedr/dedr_text.txt'):
    if rx.search(line):
        k=line[:60]
        if k in seen: continue
        seen.add(k); print(line.strip()[:n]); print()
