import re
h=open('/home/claude/ivc/map_page/index.html').read()
js="\n".join(re.findall(r'<script[^>]*>(.*?)</script>',h,flags=re.S))
stub='''const mkEl=()=>({children:[],attrs:{},classList:{toggle(){},add(){},remove(){}},setAttribute(k,v){this.attrs[k]=v},appendChild(c){return c},addEventListener(){},querySelector(){return mkEl()},set textContent(v){},set innerHTML(v){},style:{}});
const els={};globalThis.document={getElementById:id=>els[id]||(els[id]=mkEl()),createElementNS:()=>mkEl(),createElement:()=>mkEl(),createTextNode:()=>mkEl()};
'''
open('/tmp/m.js','w').write(stub+js+'''
N.forEach(n=>pick(n[0]));clear();console.log('rows',rows.map(r=>r.length).join(','),els.sv.attrs.viewBox);
console.log('long labels',N.filter(n=>n[2].split('|').some(s=>s.length>12)).map(n=>n[2]));
rows.forEach(R=>{for(let i=1;i<R.length;i++)if(R[i].x-R[i-1].x<NW)console.log('overlap',R[i-1].id,R[i].id);});''')
