import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
plans=json.loads((P/'ke_hoach.json').read_text(encoding='utf-8'))
im=Image.new('RGB',(2400,1900),'#0c1420')
d=ImageDraw.Draw(im)
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
f,fs=font(22),font(17)
d.text((25,18),'20 COIN LỚN TRÊN OKX · H4 · XẾP HẠNG ƯU TIÊN SETUP',font=font(34),fill='#f0f4fa')
d.text((25,64),'Nến đóng tới 03/11/2026 07:00 VN · 30 nến mỗi ô · Nền là OHLC thật; vùng vào / đích / mốc sai là chú thích của bot.',font=f,fill='#aabbcf')
d.text((25,98),'Top 5 đều CHỜ HỒI + H1 xác nhận, chưa vào market · Đây là ảnh tổng hợp từ dữ liệu; ảnh chụp web OKX D1 được lưu riêng.',font=f,fill='#e4c68f')
for idx,p in enumerate(plans):
    ma=p['ma']; hs=json.loads((P/(ma+'.json')).read_text(encoding='utf-8'))
    h4=next(k for k in hs['khung_ds'] if k['khung']=='4H')
    ns=h4['bang'];c=h4['chi_bao']['gia_dong']
    left=(idx%4)*600+15;top=150+(idx//4)*347
    d.rounded_rectangle((left,top,left+570,top+330),radius=10,fill='#121e2d',outline='#49586c' if idx<5 else '#29394c',width=2)
    d.text((left+12,top+10),'#'+str(idx+1)+' '+ma+' · C '+format(c,'.6g'),font=f,fill='#f2d18f' if idx<5 else '#e5edf7')
    xx1,xx2,yy1,yy2=left+15,left+555,top+52,top+260
    lo=min(n['l'] for n in ns);hi=max(n['h'] for n in ns)
    if idx<5:
        lo=min(lo,p['tp2'][0]);hi=max(hi,p['sai'])
    pad=(hi-lo)*.06;lo-=pad;hi+=pad
    y=lambda z:yy2-(z-lo)/(hi-lo)*(yy2-yy1)
    for j in range(4):
        yy=yy1+(yy2-yy1)*j/3
        d.line((xx1,yy,xx2,yy),fill='#26364a')
    if idx<5:
        for price,color in ((sum(p['vung'])/2,'#efa0af'),(sum(p['tp2'])/2,'#77d4bf'),(p['sai'],'#efc36c')):
            d.line((xx1,y(price),xx2,y(price)),fill=color,width=2)
    step=(xx2-xx1)/len(ns)
    for i,n in enumerate(ns):
        xx=xx1+(i+.5)*step
        col='#65c9b2' if n['c']>=n['o'] else '#e67d91'
        d.line((xx,y(n['h']),xx,y(n['l'])),fill=col,width=1)
        a,b=sorted((y(n['o']),y(n['c'])))
        d.rectangle((xx-4,a,xx+4,max(a+1,b)),fill=col)
    if idx<5:
        d.text((left+12,top+273),'Vào '+format(p['vung'][0],'.6g')+'–'+format(p['vung'][1],'.6g')+' | Sai '+format(p['sai'],'.6g'),font=fs,fill='#efb1bc')
        d.text((left+12,top+300),'Đích 2: '+format(p['tp2'][0],'.6g')+'–'+format(p['tp2'][1],'.6g'),font=fs,fill='#86ddc7')
    else:
        text=p['hanh_dong']
        if len(text)>48:text=text[:46]+'…'
        d.text((left+12,top+273),text,font=fs,fill='#bbc9d9')
        d.text((left+12,top+300),'RSI H4 '+format(h4['chi_bao']['rsi14'],'.1f')+' · '+('GIẢM' if h4['chi_bao']['phan_loai_L01'].startswith('GIẢM') else 'HỖN HỢP'),font=fs,fill='#97adc5')
im.save(P/'tong_hop_H4.png')
print('Saved',P/'tong_hop_H4.png')
