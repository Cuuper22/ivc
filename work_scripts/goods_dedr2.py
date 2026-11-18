"""Direct DEDR (Tamil side) look-ups by Tamil headword. usage: python3 goods_dedr2.py word1 word2 ...
Prints entry number and start of entry for every entry whose first Tamil headwords include the word."""
import sys,re,unicodedata
P='/home/antigravity/Cuuper22/ivc/work_data/lexicons/dedr/dedr_entries.tsv'
E=[l.rstrip('\n').split('\t',1) for l in open(P,encoding='utf8')]
for w in sys.argv[1:]:
    w=unicodedata.normalize('NFC',w)
    for no,t in E:
        m=re.match(r'Ta\. (.*?)(?: Ma\.| Ko\.| Ka\.| Te\.| Tu\.| To\.|$)',t)
        if not m: continue
        heads=re.split(r'[ ,;]+',re.sub(r'\(.*?\)','',m.group(1)))
        if w in heads[:12]:
            print(w,'|',no,'|',t[:150]); 
