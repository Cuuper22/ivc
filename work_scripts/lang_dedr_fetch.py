"""Download every page of the online DEDR (Burrow & Emeneau 1984, DSAL) and split it into numbered entries.
Output: /tmp/dedr/pages/pNNN.html and /tmp/dedr/dedr_entries.tsv (number<TAB>text). Prints progress."""
import os, re, html, subprocess, sys, time
os.makedirs("/tmp/dedr/pages", exist_ok=True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 520
for p in range(1, N+1):
    f = f"/tmp/dedr/pages/p{p:03d}.html"
    if os.path.exists(f) and os.path.getsize(f) > 5000: continue
    subprocess.run(["curl","-sS","-m","60","-o",f,f"https://dsal.uchicago.edu/cgi-bin/app/burrow_query.py?page={p}"])
    if p % 25 == 0: print(f"page {p}/{N}", flush=True)
ents = {}
for p in range(1, N+1):
    f = f"/tmp/dedr/pages/p{p:03d}.html"
    if not os.path.exists(f): continue
    t = open(f, encoding="utf8", errors="ignore").read()
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t); t = re.sub(r"\s+", " ", html.unescape(t))
    for m in re.finditer(r"(?:^| )(\d{1,4}[a-z]?A?) ((?:Ta|Ma|Ka|Tu|Te|Kod|Ko|To|Kol|Nk|Pa|Ga|Go|Konḍa|Pe|Manḍ|Kui|Kuwi|Kur|Malt|Br|Ir|PāMu|Koḍ|Kor|Bel)\. .*?)(?= DEDS? ?\(?\w*\)? ?\d+[a-z]?\.| DED\(N\) \d+\.| DED\(S\) \d+\.| DEN \d+\.|$)", t):
        ents.setdefault(m.group(1), m.group(2))
with open("/tmp/dedr/dedr_entries.tsv","w") as o:
    for k,v in ents.items(): o.write(f"{k}\t{v}\n")
print("entries", len(ents))

# Split pages into one line per numbered entry (NFC-normalised) for lang_dedr_grep.py -> /tmp/dedr/dedr_text.txt
import glob, unicodedata
with open('/tmp/dedr/dedr_text.txt', 'w') as out:
    for f in sorted(glob.glob('/tmp/dedr/pages/*.html')):
        t = open(f, encoding='utf8', errors='ignore').read()
        t = re.sub(r"<script.*?</script>", " ", t, flags=re.S); t = re.sub(r"<[^>]+>", " ", t)
        t = unicodedata.normalize('NFC', re.sub(r"\s+", " ", html.unescape(t)))
        for p in re.split(r" (?=\d{1,4}[a-z]?A? (?:\[|\(|Ta\.|Ma\.|Ka\.|Tu\.|Te\.|Ko\.|To\.|Koḍ\.|Kol\.|Nk\.|Pa\.|Ga\.|Go\.|Konḍa|Pe\.|Manḍ\.|Kui|Kuwi|Kur\.|Malt\.|Br\.|Ir\.|Kor\.|Bel\.|PāMu))", t):
            out.write(p.strip() + "\n")
print("wrote /tmp/dedr/dedr_text.txt")
