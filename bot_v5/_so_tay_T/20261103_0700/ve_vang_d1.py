"""Ảnh chart giá thật và ảnh có chú thích, giữ riêng dữ liệu với dự báo."""
import csv
import datetime as dt
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parents[2] / 'cong_cu'))
from chi_bao import ema

h = json.loads((P / 'VANG_ngu_canh_da_kiem.json').read_text(encoding='utf-8'))
d1 = next(k for k in h['khung_ds'] if k['khung'] == '1D')
nen = d1['bang'][-65:]
with (P / 'cache_vang_da_kiem/yahoo_VANG_1d.csv').open(newline='') as f:
    full = [r for r in csv.DictReader(f) if r['dong_utc'] <= '2026-11-03 00:00']
full = full[-2066:]
assert len(full) == d1['so_nen_cua_so']
assert all(r['mo_utc'] < r['dong_utc'] for r in full)
close = [float(r['close']) for r in full]
duong_ema = {n: ema(close, n)[-len(nen):] for n in (34, 89, 200, 610)}
for n, xs in duong_ema.items():
    gia = d1['chi_bao']['ema']['ema34']['close'] if n == 34 else d1['chi_bao']['ema'][f'ema{n}']['gia']
    assert abs(xs[-1] - gia) < 1e-8

im = Image.new('RGB', (1700, 1120), '#0e1724')
d = ImageDraw.Draw(im)
font = lambda size: ImageFont.truetype('C:/Windows/Fonts/arial.ttf', size)
f, fs, fl = font(21), font(17), font(32)
trai, phai, tren, duoi = 85, 1240, 145, 845
buoc = (phai - trai) / (len(nen) + 13)
lo, hi = 3600, 4880
y = lambda p: duoi - (p - lo) / (hi - lo) * (duoi - tren)
x = lambda i: trai + (i + .5) * buoc
d.text((42, 22), 'VÀNG · GC=F · D1 · USD / troy oz', font=fl, fill='#f7f8fc')
d.text((42, 68), 'Yahoo Gold Futures | Phiên 02/11 đóng 03/11/2026 05:00 VN | C 3.956,6', font=f, fill='#b8c5d6')
d.text((42, 100), 'Nến ngày cuối dựng từ 23 nến H1 đủ phiên; không phải giá settlement. Khác XAUUSD và vàng SJC.', font=fs, fill='#b8c5d6')
for gia in range(3600, 4900, 100):
    d.line((trai, y(gia), phai, y(gia)), fill='#243245')
    d.text((15, y(gia)-10), f'{gia:,}', font=fs, fill='#91a5be')
cuoi = x(len(nen)-1) + buoc/2
d.rectangle((cuoi+1, tren, phai, duoi), fill='#142032')
d.text((cuoi+10, tren+10), 'VÙNG DỰ BÁO', font=fs, fill='#e8c886')
d.text((cuoi+10, tren+35), 'không có nến thật', font=fs, fill='#91a5be')
mau_ema = {34: '#f3cc73', 89: '#68b8fa', 200: '#d394ed', 610: '#6cc6b4'}
for n, xs in duong_ema.items():
    pts = [(x(i),y(v)) for i,v in enumerate(xs) if v is not None]
    d.line(pts, fill=mau_ema[n], width=2)
for i,n in enumerate(nen):
    mau = '#65cfba' if n['c'] >= n['o'] else '#ee7c89'
    d.line((x(i), y(n['h']), x(i), y(n['l'])), fill=mau, width=2)
    a,b = sorted((y(n['o']), y(n['c'])))
    d.rectangle((x(i)-4,a,x(i)+4,max(a+2,b)),fill=mau)
    if i % 10 == 0 or i == len(nen)-1:
        d.text((x(i)-22,duoi+10), n['nhan'][5:], font=fs, fill='#a9b7ca')
vmax = max(n['vol'] for n in nen)
for i,n in enumerate(nen):
    yy = 982 - n['vol']/vmax*83
    d.rectangle((x(i)-4,yy,x(i)+4,982),fill='#426a7c' if n['c'] >= n['o'] else '#885b70')
d.text((85,1000), 'Volume phiên', font=fs, fill='#a9b7ca')
for i,n in enumerate((34,89,200,610)):
    d.text((300+i*205,1000), f'EMA{n}: {duong_ema[n][-1]:,.1f}', font=fs,fill=mau_ema[n])
d.text((42,1060), 'Ảnh dựng từ OHLC thật trong snapshot. Tất cả giá chỉ tới cutoff 03/11/2026 07:00 VN.', font=f, fill='#b8c5d6')
d.text((1280,160), 'NẾN + EMA',font=fl,fill='#f7f8fc')
d.text((1280,205), 'Bản dữ liệu nguồn',font=f,fill='#b8c5d6')
im.save(P/'VANG_D1_nguon.png')

# Vẽ các chú thích kỹ thuật riêng trên bản sao của chart.
ann = im.copy()
d = ImageDraw.Draw(ann)
d.rectangle((1260,140,1690,820),fill='#0e1724')
d.text((1280,150),'KẾ HOẠCH CỦA BOT',font=font(25),fill='#f5d287')
d.text((1280,192),'GIẢM · độ chắc vừa',font=f,fill='#ed8f99')
def ngang(gia, mau, rong=2):
    d.line((trai,y(gia),phai,y(gia)),fill=mau,width=rong)
def vung(a,b,mau):
    layer = Image.new('RGBA',ann.size,(0,0,0,0))
    ld=ImageDraw.Draw(layer)
    ld.rectangle((trai,y(b),phai,y(a)),fill=mau)
    ann.paste(layer,(0,0),layer)
vung(3985,4015,(221,108,119,52))
vung(3875,3905,(93,206,177,52))
vung(3690,3720,(103,161,239,52))
d=ImageDraw.Draw(ann)
for gia,mau in ((4000,'#f2a6af'),(3890,'#7ce1c6'),(3705,'#8ebfff')):
    ngang(gia,mau)
ngang(4097.2,'#ffca79')

# Trendline: đúng hai giá neo của hồ sơ, ghép ngày theo nến có râu tương ứng.
i1=next(i for i,n in enumerate(nen) if abs(n['h']-4558.5)<.2)
i2=next(i for i,n in enumerate(nen) if abs(n['h']-4097.2001953125)<.2)
d.line((x(i1),y(4558.5),x(i2),y(4097.2)),fill='#ffd476',width=3)
d.line((x(i2),y(4097.2),cuoi,y(4045.8)),fill='#ffd476',width=3)
for i,gia in ((i1,4558.5),(i2,4097.2)):
    d.ellipse((x(i)-5,y(gia)-5,x(i)+5,y(gia)+5),outline='#ffd476',width=2)
d.text((x(i1)+10,y(4558.5)-28),'Trendline giảm D1 · 6 chạm',font=fs,fill='#ffd476')
d.text((x(i2)-145,y(4097.2)-32),'Đỉnh 4.097,2',font=fs,fill='#ffca79')
ib=next(i for i,n in enumerate(nen) if n['nhan']=='2026-10-30')
d.text((x(ib)-180,y(3879.3)+12),'Râu 30/10: 3.879,3',font=fs,fill='#83dbc3')

# Các đoạn mũi tên là dự báo, đặt trong khoảng trống bên phải.
duong=[(x(len(nen)-1),y(3956.6)),(x(len(nen)+3),y(4000)),
       (x(len(nen)+7),y(3890)),(x(len(nen)+11),y(3705))]
for a,b in zip(duong,duong[1:]):
    d.line((*a,*b),fill='#f4ddad',width=3)
    angle=math.atan2(b[1]-a[1],b[0]-a[0])
    pts=[b,(b[0]-12*math.cos(angle-.45),b[1]-12*math.sin(angle-.45)),
         (b[0]-12*math.cos(angle+.45),b[1]-12*math.sin(angle+.45))]
    d.polygon(pts,fill='#f4ddad')

dong = [
    ('CHỜ SHORT 3.985–4.015','#f2a6af'),
    ('Fibo 0,5: 3.988,3', '#b8c5d6'),
    ('Đáy cũ 3.989,1 + EMA34 H4','#b8c5d6'),
    ('Chờ H1 từ chối tăng tại vùng','#b8c5d6'),
    ('','white'),
    ('TP1: 3.875–3.905','#7ce1c6'),
    ('Đáy 3.879,3 + mốc tuần 3.901,3','#b8c5d6'),
    ('Hạn dự kiến: 04–06/11','#b8c5d6'),
    ('Nấc theo dõi tiếp: 3.844','#b8c5d6'),
    ('','white'),
    ('TP trung hạn: 3.690–3.720','#8ebfff'),
    ('EMA610 D1: 3.716,2','#b8c5d6'),
    ('Fibo tuần 0,618: 3.704,6','#b8c5d6'),
    ('Hạn dự kiến: 17/11','#b8c5d6'),
    ('','white'),
    ('VIEW SAI: D1 đóng trên 4.097,2','#ffca79'),
    ('Râu vượt không đủ xác nhận','#b8c5d6'),
    ('Không short đuổi tại hỗ trợ','#b8c5d6'),
]
for i,(s,mau) in enumerate(dong):
    d.text((1280,245+i*30),s,font=fs,fill=mau)
d.text((85,1030),'Vùng tô / trendline / mũi tên: chú thích và dự báo của bot; không phải diễn biến đã xảy ra.',font=fs,fill='#e5c587')
ann.save(P/'VANG_D1_nhan_dinh.png')
print('PASS: nến đúng thời gian, EMA khớp snapshot; đã lưu ảnh nguồn và ảnh chú thích.')
