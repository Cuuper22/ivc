"""Item 4 follow-up: read the legend text, material and type on each CDLI composite seal record (CDLI has no photo for any: page shows its no-image placeholder).
Prediction first: every record has a Sumerian name-title-father legend (cuneiform cylinder); none is pictorial-only."""
import urllib.request,re,html,csv,json
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) Chrome/124'}
rows=list(csv.DictReader(open('/home/claude/ivc/work_data/abroad3/seal_records_24.csv')))
out=[]
for r in rows:
    h=urllib.request.urlopen(urllib.request.Request(f"https://cdli.earth/artifacts/{r['sid']}",headers=UA),timeout=60).read().decode()
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S); t=html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',t)))
    kind=re.search(r'\) (\w[\w ]*?) \(not impression\)|\) ([\w ]+seal[\w ]*) excavated',t)
    m=re.search(r'Seal Text Text object seal surface a (.*?) Consult previous',t)
    mat=re.search(r'Material\(s\) (\S+)',t)
    prov=re.search(r'Provenience (.*?) Material',t)
    out.append(dict(seal=r['seal'],P='P'+r['sid'],tablets=r['tablets'],material=mat.group(1) if mat else '',prov=prov.group(1) if prov else '',legend=m.group(1) if m else '',photo='none (CDLI placeholder)'))
    print(out[-1]['P'],out[-1]['prov'],out[-1]['material'],'|',out[-1]['legend'],'|',out[-1]['tablets'])
csv.DictWriter(open('/home/claude/ivc/work_data/abroad3/seal_legends.csv','w',newline=''),fieldnames=list(out[0])).writeheader()
w=csv.DictWriter(open('/home/claude/ivc/work_data/abroad3/seal_legends.csv','w',newline=''),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
