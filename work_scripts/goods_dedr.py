"""Look up early-Dravidian words for goods in the local DEDR copy (Tamil side).
usage: python3 goods_dedr.py   -> writes goods_out/dedr_lookup.txt  (entry number, start of entry)"""
import re,unicodedata
P='/home/antigravity/Cuuper22/ivc/work_data/lexicons/dedr/dedr_entries.tsv'
E=[l.rstrip('\n').split('\t',1) for l in open(P,encoding='utf8')]
def n(s): return unicodedata.normalize('NFC',s)
Q={ 'sesame':r'\b(sesame|gingelly)',
 'cotton':r'\bcotton\b','cloth':r'\bcloth\b',
 'barley':r'barley','wheat':r'\bwheat','rice':r'\brice\b|paddy','millet':r'millet|Panicum|Setaria|Pennisetum',
 'date':r'\bdate[- ]palm|\bdates?\b','teak':r'\bteak','ebony':r'ebony|Diospyros','sissoo':r'Dalbergia|rosewood|blackwood',
 'timber':r'timber|\btree\b.{0,30}wood',
 'bead':r'\bbead','carnelian':r'carnelian|cornelian|agate','coral':r'\bcoral','pearl':r'pearl','conch':r'conch|chank','shell':r'\bshell\b','bangle':r'bangle|bracelet',
 'copper':r'\bcopper|brass','tin':r'\btin\b|\blead\b','gold':r'\bgold','silver':r'silver','ivory':r'ivory|\btusk','salt':r'\bsalt\b',
 'fish':r'\bfish\b','ghee':r'\bghee|clarified butter|butter','oil':r'\boil\b','cattle':r'\bcow\b|\bbull\b|\box\b|cattle','buffalo':r'buffalo','peacock':r'peacock|peafowl',
 'elephant':r'elephant','monkey':r'monkey','goat':r'\bgoat','sheep':r'\bsheep','dog':r'\bdog\b','pot':r'\bpot\b','basket':r'basket','granary':r'granary|storehouse|store-house','weigh':r'weigh|weight|balance','measure':r'\bmeasure','box':r'\bbox\b|chest','tool':r'adze|axe\b|chisel|\bknife|razor|\bsaw\b','bow':r'\bbow\b','hide':r'\bhide\b|leather|\bskin\b','boat':r'\bboat|\bship\b','stone':r'\bstone\b','seal':r'\bseal\b|signet','spindle':r'spindle|thread|spin\b','tamarind':r'tamarind','pulse':r'gram\b|pulse|lentil|pea\b','jujube':r'jujube|Zizyphus','mango':r'mango'}
import sys
out=open('/home/antigravity/Cuuper22/ivc/work_scripts/goods_out/dedr_lookup.txt','w')
for k,rx in Q.items():
    r=re.compile(rx,re.I); out.write(f'\n## {k}\n'); c=0
    for no,t in E:
        if not t.startswith('Ta.'): continue
        if r.search(t[:260]):
            out.write(f'{no}\t{t[:170]}\n'); c+=1
            if c>=14: break
out.close()
