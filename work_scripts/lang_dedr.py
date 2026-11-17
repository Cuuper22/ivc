"""Look up the Dravidian Etymological Dictionary (DEDR, Burrow & Emeneau 1984, DSAL online).
Usage: python3 lang_dedr.py "word" [matchtype]   (full-text search; matchtype default|exact|containing)
Prints each entry as plain text. Cache in /tmp/dedr_cache."""
import sys, re, html, os, urllib.parse, urllib.request, hashlib
def q(term, mt="containing"):
    os.makedirs("/tmp/dedr_cache", exist_ok=True)
    key = hashlib.md5((term+mt).encode()).hexdigest()
    p = f"/tmp/dedr_cache/{key}.html"
    if not os.path.exists(p):
        url = "https://dsal.uchicago.edu/cgi-bin/app/burrow_query.py?" + urllib.parse.urlencode({"qs": term, "matchtype": mt})
        os.system(f"curl -sS -m 60 '{url}' -o {p}")
    t = open(p, encoding="utf8", errors="ignore").read()
    ents = re.findall(r'<div class="hw_result">(.*?)</div>', t, re.S)
    if not ents:
        body = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
        ents = [body]
    out = []
    for e in ents:
        s = html.unescape(re.sub(r"<[^>]+>", " ", e))
        s = re.sub(r"\s+", " ", s).strip()
        out.append(s)
    return out
if __name__ == "__main__":
    mt = sys.argv[2] if len(sys.argv) > 2 else "containing"
    for e in q(sys.argv[1], mt):
        print("*", e[:1500]); print()
