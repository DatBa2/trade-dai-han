#!/usr/bin/env python3
"""Ảnh chụp thị trường tại nến H4 vừa đóng — những thứ người phân tích hay nhìn
(H4/H1/D1, dải EMA34 high/low/close + EMA89/200/610, RSI, cấu trúc đỉnh đáy, Fibo, volume, BTC.D, USDT.D, Fear & Greed).

EMA (sửa 31/10 theo P1-9, trước đó là SMA34/89/200): dùng chung `cong_cu/chi_bao.py::ema` — đệ quy α = 2/(n+1),
khởi tạo = SMA n nến đầu, cùng định nghĩa với builder thi. Để EMA200/610 hội tụ, chuỗi nến được nối lịch sử dài từ CSV
có sẵn (NGUON_DAI, chỉ ĐỌC) trước các nến vừa tải, cắt tại nến đã đóng cuối cùng của snapshot.

Đầu vào cho bot ra nhận định. Lưu du_lieu/anh/<YYYY-MM-DD_HHMM VN>.json và in bản tóm tắt.
Cách dùng: python3 cong_cu/anh_thi_truong.py   (tự cập nhật nến 15m trước)
"""
import csv, datetime as dt, json, subprocess, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chi_bao import ema  # noqa: E402 — EMA dùng chung (bot v4 TK 2 / thi)

GOC = Path(__file__).resolve().parent.parent
NGUON_DAI = {  # lịch sử dài cho EMA200/610 (nến đã đóng, giờ mở UTC); file nào có thì dùng, sau ghi đè trước
    "4H": ["thi/du_lieu/btc_4H_bo_sung.csv", "du_lieu/btc_4H.csv"],
    "1Dutc": ["thi/du_lieu/btc_1Dutc_bo_sung.csv", "du_lieu/btc_1Dutc.csv"],
}
VN = dt.timedelta(hours=7)
UA = {"User-Agent": "Mozilla/5.0"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return json.load(r)


def gop(nen15, gio):
    """Gộp nến 15m thành nến `gio` giờ (căn theo UTC), chỉ giữ nến đã đóng đủ."""
    nhom = {}
    for t, o, h, l, c, v in nen15:
        k = t.replace(minute=0, hour=t.hour - t.hour % gio)
        nhom.setdefault(k, []).append((o, h, l, c, v))
    ra = []
    for k in sorted(nhom):
        x = nhom[k]
        if len(x) == gio * 4:
            ra.append((k, x[0][0], max(i[1] for i in x), min(i[2] for i in x), x[-1][3], sum(i[4] for i in x)))
    return ra


def noi_lich_su(khung, moi):
    """Nến `moi` (vừa tải, ưu tiên) nối sau nến cũ trong các CSV NGUON_DAI[khung]; cắt tại nến cuối của `moi`."""
    gop = {}
    for rel in NGUON_DAI[khung]:
        p = GOC / rel
        if p.exists():
            with p.open() as f:
                for r in csv.DictReader(f):
                    t = dt.datetime.fromisoformat(r["ts_utc"])
                    gop[t] = (t, *(float(r[k]) for k in ("open", "high", "low", "close", "vol")))
    gop.update({x[0]: x for x in moi})
    return [gop[k] for k in sorted(gop) if k <= moi[-1][0]]


def dai_ema(nen):
    """Dải EMA34 (high/low/close) + EMA89/200/610 trên close, tại nến cuối của `nen`; thiếu nến → None."""
    cot = {"high": [x[2] for x in nen], "low": [x[3] for x in nen], "close": [x[4] for x in nen]}
    cuoi = lambda xs, n: (lambda v: round(v) if v is not None else None)(ema(xs, n)[-1]) if xs else None
    return {"EMA34_high": cuoi(cot["high"], 34), "EMA34_low": cuoi(cot["low"], 34), "EMA34_close": cuoi(cot["close"], 34),
            "EMA89": cuoi(cot["close"], 89), "EMA200": cuoi(cot["close"], 200), "EMA610": cuoi(cot["close"], 610),
            "so_nen_tinh": len(nen), "tu": nen[0][0].strftime("%Y-%m-%d") if nen else None}


def rsi(nen, n=14):
    d = [b[4] - a[4] for a, b in zip(nen, nen[1:])]
    up = sum(max(x, 0) for x in d[:n]) / n; dn = sum(max(-x, 0) for x in d[:n]) / n
    for x in d[n:]:
        up = (up * (n - 1) + max(x, 0)) / n; dn = (dn * (n - 1) + max(-x, 0)) / n
    return round(100 - 100 / (1 + up / dn), 1) if dn else 100.0


def dinh_day(nen, k=3):
    """Đỉnh/đáy fractal: cao/thấp nhất trong k nến mỗi bên."""
    dinh, day = [], []
    for i in range(k, len(nen) - k):
        cua_so = nen[i - k:i + k + 1]
        if nen[i][2] == max(x[2] for x in cua_so): dinh.append((nen[i][0], round(nen[i][2])))
        if nen[i][3] == min(x[3] for x in cua_so): day.append((nen[i][0], round(nen[i][3])))
    return dinh, day


def gio_vn(t):
    return (t + VN).strftime("%d/%m %H:%M")


def main():
    subprocess.run([sys.executable, str(GOC / "cong_cu" / "lay_gia.py")], check=True, capture_output=True)
    with (GOC / "du_lieu" / "btc_15m.csv").open() as f:
        n15 = [(dt.datetime.fromisoformat(r["ts_utc"]), *(float(r[k]) for k in ("open", "high", "low", "close", "vol")))
               for r in csv.DictReader(f)]
    h1, h4 = gop(n15, 1), gop(n15, 4)
    d1 = [(dt.datetime.fromtimestamp(int(x[0]) / 1000, dt.timezone.utc).replace(tzinfo=None), *map(float, x[1:6]))
          for x in reversed(get("https://www.okx.com/api/v5/market/candles?instId=BTC-USDT&bar=1Dutc&limit=300")["data"])
          if x[-1] == "1"]
    dong_h4 = h4[-1][0] + dt.timedelta(hours=4)
    dinh, day = dinh_day(h4[-120:])
    d30 = d1[-30:]
    cao30, thap30 = max(d30, key=lambda x: x[2]), min(d30, key=lambda x: x[3])
    di_xuong = cao30[0] < thap30[0]  # sóng gần nhất: đỉnh trước, đáy sau → Fibo hồi lên
    a, b = (cao30[2], thap30[3])
    fibo = {f: round(b + (a - b) * f) if di_xuong else round(a - (a - b) * f) for f in (0.382, 0.5, 0.618, 0.786)}
    try:
        fg = get("https://api.alternative.me/fng/?limit=2")["data"]
        fear_greed = [(int(x["value"]), x["value_classification"]) for x in fg]
    except Exception:
        fear_greed = None
    try:
        g = get("https://api.coingecko.com/api/v3/global")["data"]["market_cap_percentage"]
        dom = {"BTC.D": round(g["btc"], 2), "USDT.D": round(g["usdt"], 2)}
    except Exception:
        dom = None
    vol20 = sum(x[5] for x in h4[-21:-1]) / 20
    anh = {
        "nen_h4_vua_dong_vn": gio_vn(dong_h4), "gia": h4[-1][4],
        "h4_gan_nhat": [{"mo_vn": gio_vn(x[0]), "o": x[1], "h": x[2], "l": x[3], "c": x[4],
                         "mau": "xanh" if x[4] >= x[1] else "đỏ", "vol_x_tb20": round(x[5] / vol20, 2)} for x in h4[-8:]],
        "h1_gan_nhat": [{"mo_vn": gio_vn(x[0]), "o": x[1], "h": x[2], "l": x[3], "c": x[4]} for x in h1[-6:]],
        "d1_gan_nhat": [{"ngay": x[0].strftime("%d/%m"), "o": x[1], "h": x[2], "l": x[3], "c": x[4]} for x in d1[-7:]],
        "ema": {"cach_tinh": "EMA α=2/(n+1), khởi tạo SMA n (cong_cu/chi_bao.py); nến đã đóng",
                "H4": dai_ema(noi_lich_su("4H", h4)), "D1": dai_ema(noi_lich_su("1Dutc", d1))},
        "rsi": {"H1": rsi(h1[-200:]), "H4": rsi(h4[-200:]), "D1": rsi(d1[-200:])},
        "dinh_h4": [(gio_vn(t), p) for t, p in dinh[-4:]], "day_h4": [(gio_vn(t), p) for t, p in day[-4:]],
        "song_30_ngay": {"cao": (cao30[0].strftime("%d/%m"), cao30[2]), "thap": (thap30[0].strftime("%d/%m"), thap30[3]),
                         "fibo_hoi" if di_xuong else "fibo_dieu_chinh": fibo},
        "fear_greed": fear_greed, "dominance": dom,
    }
    ra = GOC / "du_lieu" / "anh" / f"{(dong_h4 + VN).strftime('%Y-%m-%d_%H%M')}.json"
    ra.parent.mkdir(exist_ok=True)
    ra.write_text(json.dumps(anh, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(anh, ensure_ascii=False, indent=1))
    print("→", ra.relative_to(GOC))


if __name__ == "__main__":
    main()
