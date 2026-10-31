import re,json
out=[]
for m in range(1,13):
    t=open(f'bls_s{m:02d}.html',encoding='utf8',errors='ignore').read()
    i=t.find('Month View'); t=t[i:]
    j=t.find('List View'); 
    s=re.sub(r'<[^>]+>','|',t); s=re.sub(r'&nbsp;','',s); s=re.sub(r'\s*\|[\s|]*','|',s)
    toks=[x for x in s.split('|') if x.strip()]
    day=None;k=0
    # find start after weekday headers
    k=toks.index('Friday')+1
    cur=None
    while k<len(toks):
        x=toks[k]
        if re.fullmatch(r'\d{1,2}',x): cur=int(x); k+=1; continue
        if k+2<len(toks) and re.fullmatch(r'\d{1,2}:\d\d [AP]M',toks[k+2]):
            out.append((m,cur,toks[k],toks[k+1],toks[k+2])); k+=3; continue
        k+=1
json.dump(out,open('bls_ev.json','w'))
for o in out[:25]: print(o)
print(len(out))
