# Tai chuoi gia Polymarket 'Fed decision in <thang>' 2026 (gamma + clob, chunk 14 ngay, fidelity 60). Chay: python3 -I _tai_polymarket.py trong thu muc nay.
import json,subprocess,datetime,time
from concurrent.futures import ThreadPoolExecutor
def get(u):
    for i in range(3):
        try:
            return json.loads(subprocess.run(['curl','-s','-m','60',u],capture_output=True,text=True).stdout)
        except Exception: time.sleep(2)
    return {}
S={'2026-01':['fed-decision-in-january'],'2026-03':['fed-decision-in-march-885'],'2026-04':['fed-decision-in-april'],
'2026-06':['fed-decision-in-june-825'],'2026-07':['fed-decision-in-july-181'],
'2026-09':['fed-decision-in-september-568','fed-decision-in-september-762'],
'2026-10':['fed-decision-in-october-20260617190323537'],'2026-12':['fed-decision-in-december-20260729232808632']}
iso=lambda s:int(datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())
now=int(time.time())
jobs=[]
for ky,slugs in S.items():
  for sl in slugs:
    ev=get('https://gamma-api.polymarket.com/events?slug='+sl)[0]
    a=iso(ev['startDate'])-86400; b=min(iso(ev['endDate'])+2*86400,now)
    for m in ev['markets']:
        tid=json.loads(m['clobTokenIds'])[0]
        lab=m.get('groupItemTitle')
        jobs.append((ky,sl,len(slugs)>1,lab,tid,a,b))
def run(j):
    ky,sl,multi,lab,tid,a,b=j
    out={};t=a
    while t<b:
        r=get(f'https://clob.polymarket.com/prices-history?market={tid}&startTs={t}&endTs={min(t+14*86400,b)}&fidelity=60')
        for p in r.get('history',[]): out[p['t']]=p['p']
        t+=14*86400
    return j,out
rows=[]
with ThreadPoolExecutor(6) as ex:
    for j,out in ex.map(run,jobs):
        ky,sl,multi,lab,tid,a,b=j
        ts=sorted(out); print(ky,sl[-6:],lab,len(ts),ts[0] if ts else None,ts[-1] if ts else None)
        for t in ts:
            rows.append((datetime.datetime.fromtimestamp(t,datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),(ky+'_phu' if sl.endswith('568') else ky),lab,out[t],tid))
import csv
rows.sort(key=lambda r:(r[1],r[2],r[0]))
with open('polymarket_fed.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['ts_utc','ky_hop','ket_qua','xac_suat','token_id']); w.writerows(rows)
