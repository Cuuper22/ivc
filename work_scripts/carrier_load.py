import csv,re,sys
def load():
    rows=list(csv.DictReader(open('/home/claude/ivc/research/data/open_prototype/lipi/metadata_filtered.csv')))
    for r in rows:
        t=r['text'].strip('+')
        r['toks']=[s for s in re.split(r'[-:]',t) if s]  # stored order (reverse of reading)
    return rows
