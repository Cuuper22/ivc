"""New idea from the cuneiform side: Ur III cloth is graded 1..5 ('N-kam us2', e.g. CM 26,136 line 1, fourth grade). If the number before a tree sign is a cloth GRADE it should sit in 1..5 and 1-2 should be common; if it is a LOT COUNT it should run 3 to 8 and avoid 1-2.
Prediction first: against the grade idea (earlier job: 96% of counts before 390 are 3 or more)."""
import sys
sys.path.insert(0,'/home/claude/ivc/work_scripts')
from cotton_common import *
d=faces()
for tree in ['390','405','407']:
    c=collections.Counter()
    for t in d.toks:
        for i in range(1,len(t)):
            if t[i]==tree and t[i-1] in CNT:
                s,v=CNT[t[i-1]]
                c[(s,v)]+=1
    tot=sum(c.values())
    print(tree,'counted places',tot,'by (series,value):',sorted(c.items()))
    print('   value 1-2:',sum(v for (s,k),v in c.items() if k<=2),' value 3-5:',sum(v for (s,k),v in c.items() if 3<=k<=5),' value 6+:',sum(v for (s,k),v in c.items() if k>=6))
