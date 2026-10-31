"""Dung lich_kinh_te_2026.csv + fomc_ket_qua_2026.csv tu ban goc trong _goc/.
Chay: python3 -I _xay_dung.py (trong thu muc nay). Chi doc _goc/, khong goi mang."""
import re,csv,datetime
from zoneinfo import ZoneInfo
ET=ZoneInfo('America/New_York'); VN=ZoneInfo('Asia/Ho_Chi_Minh')
MON={m:i for i,m in enumerate('January February March April May June July August September October November December'.split(),1)}
MON3={k[:3]:v for k,v in MON.items()}
ky_th=lambda s:s
def vn(dt): return dt.astimezone(VN).strftime('%Y-%m-%d %H:%M')
def et(dt): return dt.strftime('%Y-%m-%d %H:%M')
def mk(y,m,d,hhmm):
    h,mi=map(int,hhmm.split(':')); return datetime.datetime(y,m,d,h,mi,tzinfo=ET)
def hm12(s):
    m=re.match(r'(\d+):(\d\d) ([AP])M',s); h=int(m[1])%12+(12 if m[3]=='P' else 0); return f'{h:02d}:{m[2]}'
def kyfmt(ref):
    ref=ref.strip()
    m=re.fullmatch(r'(\w+) (\d{4})',ref)
    if m and m[1] in MON: return f'Th{MON[m[1]]}/{m[2]}'
    m=re.fullmatch(r'(First|Second|Third|Fourth) Quarter (\d{4})',ref)
    if m: return 'Q%d/%s'%({'First':1,'Second':2,'Third':3,'Fourth':4}[m[1]],m[2])
    return ref
rows=[]
# ---- BLS
BLS_URL='https://www.bls.gov/schedule/2026/%02d_sched.htm'
import json
def bls_events():
    out=[]
    for m in range(1,13):
        t=open(f'_goc/bls_2026_{m:02d}_sched.html',encoding='utf8',errors='ignore').read()
        t=t[t.find('Month View'):]
        s=re.sub(r'<[^>]+>','|',t); s=s.replace('&nbsp;',''); s=re.sub(r'\s*\|[\s|]*','|',s)
        toks=[x for x in s.split('|') if x.strip()]
        k=toks.index('Friday')+1; cur=None; st='pre'; prev=0
        while k<len(toks):
            x=toks[k]
            if re.fullmatch(r'\d{1,2}',x):
                cur=int(x); k+=1
                if prev==0: st='pre' if cur>=20 else 'in'
                elif st=='pre' and cur<prev: st='in'
                elif st=='in' and cur<prev: st='post'
                prev=cur; continue
            if k+2<len(toks) and re.fullmatch(r'\d{1,2}:\d\d [AP]M',toks[k+2]):
                if st=='in': out.append((m,cur,toks[k],toks[k+1],toks[k+2]))
                k+=3; continue
            k+=1
    return out
KIND={'Consumer Price Index':'CPI','Producer Price Index':'PPI','Employment Situation':'NFP',
 'Job Openings and Labor Turnover Survey':'JOLTS','Employment Cost Index':'khac'}
seen=set()
for m,d,name,ref,tm in bls_events():
    if name not in KIND: continue
    key=(name,ref,m,d)
    if key in seen: continue
    seen.add(key)
    dt=mk(2026,m,d,hm12(tm))
    rows.append([KIND[name],et(dt),vn(dt),kyfmt(ref),BLS_URL%m,name if KIND[name]=='khac' else ''])
# ---- BEA
t=open('_goc/bea.html',encoding='utf8').read()
s=re.sub(r'<(script|style).*?</\1>','',t,flags=re.S); s=re.sub(r'<[^>]+>','|',s); s=re.sub(r'[\s|]*\|[\s|]*','|',s)
s=s[s.find('Year 2026'):]
s=s[:s.find('Year 2027')] if 'Year 2027' in s else s
toks=s.split('|'); k=0
while k<len(toks)-4:
    mm=re.fullmatch(r'(\w+) (\d{1,2})',toks[k])
    if mm and mm[1] in MON and re.fullmatch(r'\d{1,2}:\d\d [AP]M',toks[k+1]):
        title=toks[k+4]; dt=mk(2026,MON[mm[1]],int(mm[2]),hm12(toks[k+1])); k+=5
        if title.startswith('Personal Income and Outlays'):
            ref=title.split(', ',1)[1]
            r=re.fullmatch(r'(\w+) and (\w+) (\d{4})',ref)
            ky=f'Th{MON[r[1]]}-{MON[r[2]]}/{r[3]}' if r else kyfmt(ref)
            rows.append(['PCE',et(dt),vn(dt),ky,'https://www.bea.gov/news/schedule/full','Personal Income and Outlays (gom PCE)'])
        elif title.startswith('GDP (') or title.startswith('Gross Domestic Product, '):
            if title.startswith('GDP ('):
                est=re.match(r'GDP \((.*?)\)',title)[1]; ref=title.split('), ')[-1] if '), ' in title else title
                ref=re.sub(r'.*?(\d)(st|nd|rd|th) Quarter( and Year)? (\d{4}).*',lambda x:f'Q{x[1]}/{x[4]}',title.split('), ',1)[-1].split(', ')[-1]) if False else None
                q=re.search(r'(\d)(?:st|nd|rd|th) Quarter(?: and Year)? (\d{4})',title)
                ky=f'Q{q[1]}/{q[2]}'; note=f'GDP {est}'
            else:
                q=re.search(r'(\d)(?:st|nd|rd|th) Quarter (\d{4})',title); ky=f'Q{q[1]}/{q[2]}'; note='GDP (Updated Estimate)'
            rows.append(['GDP',et(dt),vn(dt),ky,'https://www.bea.gov/news/schedule/full',note])
    else: k+=1
# ---- FOMC
FOMC=[((1,27,28),'0128'),((3,17,18),'0318'),((4,28,29),'0429'),((6,16,17),'0617'),((7,28,29),'0729'),((9,15,16),'0916'),((10,27,28),'1028'),((12,8,9),None)]
FU='https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'
MIN={1:(2,18),3:(4,8),4:(5,20),6:(7,8),7:(8,19),9:(10,7)}
for (m,d1,d2),code in FOMC:
    dt=mk(2026,m,d2,'14:00'); ky=f'{d1}-{d2}/{m:02d}'
    u=f'https://www.federalreserve.gov/newsevents/pressreleases/monetary2026{code}a.htm' if code else FU
    rows.append(['FOMC',et(dt),vn(dt),'Hop '+ky,u,'Quyet dinh lai suat 14:00 ET'+(' (kem SEP/dot plot)' if m in (3,6,9,12) else '')])
    dt2=mk(2026,m,d2,'14:30')
    rows.append(['khac',et(dt2),vn(dt2),'Hop bao FOMC '+ky,FU,'Hop bao Chu tich Fed 14:30 ET'])
    if m in MIN:
        md=MIN[m]; dtm=mk(2026,md[0],md[1],'14:00')
        rows.append(['khac',et(dtm),vn(dtm),'Bien ban FOMC '+ky,FU,'Ngay cong bo theo trang Fed; gio 14:00 ET theo thong le (chua xac minh)'])
rows.sort(key=lambda r:(r[1],r[0]))
with open('lich_kinh_te_2026.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['su_kien','ngay_gio_et','ngay_gio_vn','ky','nguon_url','ghi_chu']); w.writerows(rows)
# ---- ket qua FOMC
def stm(code):
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',open(f'_goc/fomc_statement_2026{code}.html',encoding='utf8').read())).replace('\u2011','-')
res=[]
for (m,d1,d2),code in FOMC:
    if not code: continue
    s=stm(code)
    mt=re.search(r'decided to (maintain|raise|lower)[^.]*?(\d(?:-|‑)\d/\d(?: to \d(?:-|‑)\d/\d)?)? ?percent',s)
    sent=re.search(r'the Committee decided to [^.]*?percent(?!age)',s,re.I)[0]
    rg=re.findall(r'(\d(?:-\d/\d)?) to (\d(?:-\d/\d)?) percent',sent)[-1]
    fr=lambda x:(lambda p:(float(p[0])+float(p[1])/float(p[2])) if len(p)==3 else float(p[0]))(re.findall(r'\d+',x))
    lo,hi=fr(rg[0]),fr(rg[1])
    qd={'maintain':'giu nguyen','raise':'tang 25 bps','lower':'cat 25 bps'}[re.search(r'decided to (maintain|raise|lower)',sent)[1]]
    bps={'giu nguyen':0,'tang 25 bps':25,'cat 25 bps':-25}[qd]
    j=s.find('Voting against'); 
    di=re.sub(r' For media inquiries.*','',s[j:]) if j>0 else 'khong co'
    di=re.sub(r'\s+',' ',di)[:300]
    mv=re.search(r'by a (\d+) ?[–-] ?(\d+) vote',s)
    res.append([f'2026-{m:02d}-{d2:02d}',f'Hop {d1}-{d2}/{m:02d}',qd,bps,f'{lo:.2f}-{hi:.2f}',(f'{mv[1]}-{mv[2]}' if mv else ''),di,f'https://www.federalreserve.gov/newsevents/pressreleases/monetary2026{code}a.htm'])
with open('fomc_ket_qua_2026.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['ngay_quyet_dinh','ky_hop','quyet_dinh','thay_doi_bps','dai_lai_suat_sau_hop_pct','phieu','phan_doi','nguon_url']); w.writerows(res)
