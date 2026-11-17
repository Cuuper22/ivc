"""Find DEDR entries (Tamil side, also entries packed inside other lines) by Tamil headword.
usage: python3 goods_dedr3.py word ...   prints 'entry-number | start of entry'"""
import sys,re,unicodedata
P='/home/claude/ivc/work_data/lexicons/dedr/dedr_entries.tsv'
txt=' '.join(l.rstrip('\n').replace('\t',' ',1) for l in open(P,encoding='utf8'))
txt=unicodedata.normalize('NFC',txt)
ents=[(m.group(1),m.start()) for m in re.finditer(r'(?<![\w.])(\d{1,4}) (?:\([a-z]\) )?(?=(?:Ta|Ma|Ko|To|Ka|Koḍ|Tu|Te|Kol|Nk|Pa|Ga|Go|Kui|Kur|Br|Ir)\.)',txt)]
def entry(i):
    s=ents[i][1]; e=ents[i+1][1] if i+1<len(ents) else len(txt); return txt[s:e]
if __name__=='__main__':
    for w in sys.argv[1:]:
        w=unicodedata.normalize('NFC',w); n=0
        for i in range(len(ents)):
            t=entry(i); m=re.match(r'\d+ (?:\([a-z]\) )?Ta\. (.*?)(?= (?:Ma|Ko|To|Ka|Koḍ|Tu|Te)\. )',t)
            if not m: continue
            heads=re.split(r'[ ,;]+',re.sub(r'\(.*?\)','',m.group(1)))
            if w in heads[:15]:
                print(w,'|',ents[i][0],'|',t[:140].replace('\n',' ')); n+=1
        if n==0: print(w,'| none')
