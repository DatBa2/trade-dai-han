"""Vẽ lại OHLC trong snapshot đã cắt, không gọi mạng."""
import datetime as dt
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

GOC = Path(__file__).resolve().parent
FONT = 'C:/Windows/Fonts/arial.ttf'
CAU_HINH = {
    'BTC': ('BTC_ngu_canh_live.json', (77900, 78050), (76500, 76600), 78866),
    'ETH': ('ETH_ngu_canh.json', (2280, 2295), (2235, 2248), 2318),
    'ZEC': ('ZEC_ngu_canh.json', (1177, 1187), (1119, 1124), 1210.5),
}


def ve(ma, ten, vao, dich, sai):
    p = GOC / ten
    hs = json.loads(p.read_text(encoding='utf-16'))
    p.write_text(json.dumps(hs, ensure_ascii=False, indent=1), encoding='utf-8')
    assert hs['nen_cuoi']['dong_vn'] == '2026-11-03 07:00'
    nen = next(k['bang'] for k in hs['khung_ds'] if k['khung'] == '4H')
    assert all(n['nhan'] <= hs['nen_cuoi']['dong_vn'] for n in nen)
    im = Image.new('RGB', (1360, 720), '#101823')
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 18)
    f_nho = ImageFont.truetype(FONT, 15)
    f_lon = ImageFont.truetype(FONT, 26)
    d.text((38, 20), f'{ma}/USDT · OKX spot · H4 · Nến đóng tới 03/11/2026 07:00 VN', font=f_lon, fill='#f2f5fa')
    d.text((38, 58), 'Nến: dữ liệu nguồn · Vùng SHORT / đích / mốc sai: chú thích của bot · Không có nến tương lai', font=f, fill='#b4c0cf')
    trai, phai, tren, duoi = 60, 1045, 115, 605
    thap = min(min(n['l'] for n in nen), dich[0])
    cao = max(max(n['h'] for n in nen), vao[1], sai)
    dem = (cao - thap) * .1
    thap, cao = thap - dem, cao + dem
    y = lambda gia: duoi - (gia - thap) / (cao - thap) * (duoi - tren)
    for i in range(6):
        gia = thap + (cao - thap) * i / 5
        yy = y(gia)
        d.line((trai, yy, phai, yy), fill='#283343')
        d.text((5, yy - 9), f'{gia:,.0f}', font=f_nho, fill='#8a9bad')
    for vung, mau, nhan in ((vao, '#472a32', 'SHORT chờ xác nhận'), (dich, '#173c35', 'Đích H4')):
        d.rectangle((trai, y(vung[1]), phai, y(vung[0])), fill=mau)
        yy = y(sum(vung) / 2)
        d.line((trai, yy, phai, yy), fill='#d39373' if vung == vao else '#66cbb0', width=2)
        d.text((1060, yy - 11), nhan, font=f_nho, fill='#eef3f9')
        d.text((1060, yy + 10), f'{vung[0]:,}–{vung[1]:,}', font=f, fill='#eef3f9')
    d.line((trai, y(sai), phai, y(sai)), fill='#f2b85c', width=2)
    d.text((1060, y(sai) - 20), 'Sai: H4 ĐÓNG trên', font=f_nho, fill='#f2b85c')
    d.text((1060, y(sai) + 1), f'{sai:,}', font=f, fill='#f2b85c')
    buoc = (phai - trai) / len(nen)
    for i, n in enumerate(nen):
        x = trai + (i + .5) * buoc
        mau = '#5bceb2' if n['c'] >= n['o'] else '#ef7883'
        d.line((x, y(n['h']), x, y(n['l'])), fill=mau, width=2)
        yy1, yy2 = sorted((y(n['o']), y(n['c'])))
        d.rectangle((x - 7, yy1, x + 7, max(yy1 + 2, yy2)), fill=mau)
        if i % 6 == 0 or i == len(nen) - 1:
            d.text((x - 37, duoi + 12), n['nhan'][5:10], font=f_nho, fill='#b4c0cf')
            d.text((x - 37, duoi + 32), n['nhan'][11:], font=f_nho, fill='#b4c0cf')
    d.text((60, 674), f'Giá đóng cuối: {hs["nen_cuoi"]["close"]:,} USDT · Snapshot lưu kèm · Mốc sai theo nến đóng, không phải bảo đảm khớp giá', font=f, fill='#b4c0cf')
    im.save(GOC / f'{ma}_H4.png')
    print(ma, hs['nguon'], hs['nen_cuoi'], 'chart OK')


if __name__ == '__main__':
    for ma, (ten, vao, dich, sai) in CAU_HINH.items():
        ve(ma, ten, vao, dich, sai)
