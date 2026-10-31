#!/usr/bin/env python3
"""Tải nến cho backtest → backtest/du_lieu/<MÃ>_4H.csv và <MÃ>_1D.csv.

- Coin (OKX public, chỉ nến đã đóng — phần tử cuối = "1"): 4H từ 2025-06-01, 1Dutc từ 2025-01-01.
- Vàng GC=F, dầu WTI CL=F (Yahoo): H1 range=730d gộp thành H4 căn UTC 00/04/08/12/16/20
  (chỉ giữ nến H4 có ≥3 nến H1 thật — CME nghỉ 1 giờ mỗi ngày nên 1 nến H4/ngày chỉ có 3 giờ;
  bỏ nến H4 chưa kết thúc); D1 lấy interval=1d range=2y, giờ đóng = 17:00 New York của ngày đó.

Cột CSV: mo_utc, dong_utc (giờ mở / giờ đóng nến, UTC), open, high, low, close, vol.
Cách dùng: python3 backtest/tai_du_lieu.py [MÃ ...]   (mặc định tải tất cả)
"""
import csv, datetime as dt, json, sys, time, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

THU_MUC = Path(__file__).resolve().parent / "du_lieu"
UTC = dt.timezone.utc
OKX = "https://www.okx.com/api/v5/market/history-candles?instId={}&bar={}&limit=100&after={}"
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval={}&range={}"
COIN = {"BTC": "BTC-USDT", "ETH": "ETH-USDT", "NEAR": "NEAR-USDT", "ZEC": "ZEC-USDT",
        "OKB": "OKB-USDT", "BNB": "BNB-USDT"}
YH = {"VANG": "GC=F", "DAU": "CL=F"}
GIO = 3600


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for lan in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # mạng chập chờn → thử lại
            if lan == 4:
                raise
            print("  thử lại:", e)
            time.sleep(2 + lan * 2)


def _ghi(ten, dong, thu_muc=None):
    thu_muc = Path(thu_muc) if thu_muc else THU_MUC
    thu_muc.mkdir(parents=True, exist_ok=True)
    p = thu_muc / ten
    with p.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mo_utc", "dong_utc", "open", "high", "low", "close", "vol"])
        for mo, dg, o, h, l, c, v in sorted(dong):
            w.writerow([_s(mo), _s(dg), o, h, l, c, v])
    print(f"✓ {p.name}: {len(dong)} nến, {_s(min(dong)[0])} → {_s(max(dong)[0])}")


def _s(ts):
    return dt.datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%d %H:%M")


def tai_okx(ma, khung, tu, do_dai):
    inst = COIN[ma]
    tu_ms = int(dt.datetime.fromisoformat(tu).replace(tzinfo=UTC).timestamp() * 1000)
    after, ra = int(time.time() * 1000), {}
    while after > tu_ms:
        d = _get(OKX.format(inst, khung, after))["data"]
        if not d:
            break
        for ts, o, h, l, c, v, *_, xac_nhan in d:
            if xac_nhan == "1" and int(ts) >= tu_ms:
                mo = int(ts) // 1000
                ra[mo] = (mo, mo + do_dai, o, h, l, c, v)
        after = int(d[-1][0])
        time.sleep(0.15)
    return list(ra.values())


def tai_yahoo(ma, d1_range="2y"):
    sym = YH[ma]
    # H1 → H4
    r = _get(YAHOO.format(sym, "1h", "730d"))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    gio = {}
    for i, ts in enumerate(r["timestamp"]):
        if ts % GIO or None in (q["open"][i], q["high"][i], q["low"][i], q["close"][i]):
            continue  # bỏ dòng rỗng và tick lẻ (không tròn giờ)
        gio[ts] = (q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i] or 0)
    bay_gio = time.time()
    nhom = {}
    for ts in sorted(gio):
        nhom.setdefault(ts - ts % (4 * GIO), []).append(ts)
    h4 = []
    for mo, ds in nhom.items():
        if len(ds) < 3 or mo + 4 * GIO > bay_gio:
            continue
        o = gio[ds[0]][0]; c = gio[ds[-1]][3]
        h = max(gio[t][1] for t in ds); l = min(gio[t][2] for t in ds); v = sum(gio[t][4] for t in ds)
        h4.append((mo, mo + 4 * GIO, o, h, l, c, v))
    # D1
    r = _get(YAHOO.format(sym, "1d", d1_range))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    ny = ZoneInfo(r["meta"].get("exchangeTimezoneName", "America/New_York"))
    d1 = []
    for i, ts in enumerate(r["timestamp"]):
        if None in (q["open"][i], q["high"][i], q["low"][i], q["close"][i]):
            continue
        ngay = dt.datetime.fromtimestamp(ts, ny).date()
        dong = int(dt.datetime(ngay.year, ngay.month, ngay.day, 17, 0, tzinfo=ny).timestamp())
        mo = dong - 23 * GIO  # phiên CME: 18:00 hôm trước → 17:00 (chỉ để ghi, không dùng tính toán)
        if dong > bay_gio:
            continue
        d1.append((mo, dong, q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i] or 0))
    return h4, d1


def main():
    ds = sys.argv[1:] or list(COIN) + list(YH)
    for ma in ds:
        print("Tải", ma)
        if ma in COIN:
            _ghi(f"{ma}_4H.csv", tai_okx(ma, "4H", "2025-06-01", 4 * GIO))
            _ghi(f"{ma}_1D.csv", tai_okx(ma, "1Dutc", "2025-01-01", 24 * GIO))
        else:
            h4, d1 = tai_yahoo(ma)
            _ghi(f"{ma}_4H.csv", h4)
            _ghi(f"{ma}_1D.csv", d1)


if __name__ == "__main__":
    main()
