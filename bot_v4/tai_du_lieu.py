#!/usr/bin/env python3
"""Tải nến cho bot v4 -> bot_v4/du_lieu/<TS>_4H.csv, <TS>_1D.csv, SHA256SUMS, NGUON.md.

Cột CSV: ts_utc,open,high,low,close,vol  (ts_utc = giờ MỞ nến UTC, YYYY-MM-DD HH:MM).
Khoảng: 2022-06-01 00:00 UTC -> hết 2026-10-30 UTC.

- Crypto BTC/ETH/OKB/BNB: OKX spot <X>-USDT, history-candles, chỉ nến đã đóng (confirm=="1");
  4H và 1Dutc (biên ngày 00:00 UTC). Nghỉ 0,12 s/lần gọi.
- VANG=GC=F, DAU=CL=F (Yahoo), GIỐNG backtest/tai_du_lieu.py:
  * 4H dựng từ 1H gộp theo UTC 00/04/08/12/16/20, chỉ giữ nến 4H có >=3 nến 1H thật (CME nghỉ 1h/ngày).
    Yahoo chỉ cho 1H ~730 ngày -> 4H của vàng/dầu KHÔNG tới được 2022-06; lấy tối đa được,
    ngày bắt đầu thực tế ghi trong NGUON.md.
  * 1D: interval=1d (có thể lấy từ 2022-06 bằng period1/period2); ts_utc = giờ mở phiên =
    (17:00 New York của ngày đó) - 23h, như backtest (mo_utc). Phiên thứ Hai mở tối Chủ nhật UTC.
Cách dùng: python3 bot_v4/tai_du_lieu.py
"""
import csv, datetime as dt, hashlib, json, sys, time, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

THU_MUC = Path(__file__).resolve().parent / "du_lieu"
UTC = dt.timezone.utc
OKX = "https://www.okx.com/api/v5/market/history-candles?instId={}&bar={}&limit=100&after={}"
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval={}&range={}"
YAHOO_P = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1d&period1={}&period2={}"
COIN = {"BTC": "BTC-USDT", "ETH": "ETH-USDT", "OKB": "OKB-USDT", "BNB": "BNB-USDT"}
YH = {"VANG": "GC=F", "DAU": "CL=F"}
GIO = 3600
TU = dt.datetime(2022, 6, 1, tzinfo=UTC)
DEN = dt.datetime(2026, 10, 31, tzinfo=UTC)  # loại trừ
TU_S, DEN_S = int(TU.timestamp()), int(DEN.timestamp())
LOG = []


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for lan in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            if lan == 5:
                raise
            print("  thử lại:", e)
            time.sleep(2 + lan * 2)


def _s(ts):
    return dt.datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%d %H:%M")


def _ghi(ten, dong):
    dong = sorted({d[0]: d for d in dong if TU_S <= d[0] < DEN_S}.values())
    THU_MUC.mkdir(parents=True, exist_ok=True)
    with (THU_MUC / ten).open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ts_utc", "open", "high", "low", "close", "vol"])
        for mo, o, h, l, c, v in dong:
            w.writerow([_s(mo), o, h, l, c, v])
    print(f"ok {ten}: {len(dong)} nến, {_s(dong[0][0])} -> {_s(dong[-1][0])}")
    return dong


def tai_okx(ma, khung):
    inst = COIN[ma]
    after, ra = DEN_S * 1000, {}
    while after > TU_S * 1000:
        d = _get(OKX.format(inst, khung, after))["data"]
        if not d:
            break
        for ts, o, h, l, c, v, *_, xn in d:
            mo = int(ts) // 1000
            if xn == "1" and TU_S <= mo < DEN_S:
                ra[mo] = (mo, o, h, l, c, v)
        after = int(d[-1][0])
        time.sleep(0.12)
    return list(ra.values())


def tai_yahoo(ma):
    sym = YH[ma]
    r = _get(YAHOO.format(sym, "1h", "730d"))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    gio = {}
    for i, ts in enumerate(r["timestamp"]):
        if ts % GIO or None in (q["open"][i], q["high"][i], q["low"][i], q["close"][i]):
            continue
        gio[ts] = (q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i] or 0)
    bay_gio = time.time()
    nhom = {}
    for ts in sorted(gio):
        nhom.setdefault(ts - ts % (4 * GIO), []).append(ts)
    h4 = []
    for mo, ds in nhom.items():
        if len(ds) < 3 or mo + 4 * GIO > bay_gio:
            continue
        h4.append((mo, gio[ds[0]][0], max(gio[t][1] for t in ds), min(gio[t][2] for t in ds),
                   gio[ds[-1]][3], sum(gio[t][4] for t in ds)))
    r = _get(YAHOO_P.format(sym, TU_S - 5 * 86400, DEN_S + 2 * 86400))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    ny = ZoneInfo(r["meta"].get("exchangeTimezoneName", "America/New_York"))
    d1 = []
    for i, ts in enumerate(r["timestamp"]):
        if None in (q["open"][i], q["high"][i], q["low"][i], q["close"][i]):
            continue
        ng = dt.datetime.fromtimestamp(ts, ny).date()
        dong = int(dt.datetime(ng.year, ng.month, ng.day, 17, 0, tzinfo=ny).timestamp())
        if dong > bay_gio:
            continue
        d1.append((dong - 23 * GIO, q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i] or 0))
    return h4, d1


def kiem(ma, khung, dong, crypto):
    buoc = (4 if khung == "4H" else 24) * GIO
    lo = sum(1 for a, b in zip(dong, dong[1:]) if b[0] - a[0] > buoc)
    return (ma, khung, _s(dong[0][0]), _s(dong[-1][0]), len(dong), lo if crypto else f"({lo} nghỉ, bình thường)")


def main():
    bang = []
    for ma in COIN:
        print("Tải", ma)
        for k, b in (("4H", "4H"), ("1D", "1Dutc")):
            bang.append(kiem(ma, k, _ghi(f"{ma}_{k}.csv", tai_okx(ma, b)), True))
    for ma in YH:
        print("Tải", ma)
        h4, d1 = tai_yahoo(ma)
        bang.append(kiem(ma, "4H", _ghi(f"{ma}_4H.csv", h4), False))
        bang.append(kiem(ma, "1D", _ghi(f"{ma}_1D.csv", d1), False))
    print(f"{'TS':6}{'khung':6}{'đầu':18}{'cuối':18}{'nến':>6}  lỗ hổng>1 nến")
    for b in bang:
        print(f"{b[0]:6}{b[1]:6}{b[2]:18}{b[3]:18}{b[4]:>6}  {b[5]}")
    tong = []
    for p in sorted(THU_MUC.glob("*.csv")):
        tong.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}")
    (THU_MUC / "SHA256SUMS").write_text("\n".join(tong) + "\n")
    gio_tai = dt.datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    md = [f"# Nguồn dữ liệu bot v4\n\nTải lúc {gio_tai} bằng `bot_v4/tai_du_lieu.py`. Khoảng yêu cầu 2022-06-01 -> 2026-10-30 UTC.\n",
          "- Crypto (BTC, ETH, OKB, BNB): OKX spot `<X>-USDT`, `/api/v5/market/history-candles`, chỉ nến confirm=1; 4H và 1Dutc.",
          "- VANG = Yahoo `GC=F`, DAU = Yahoo `CL=F`. 4H dựng từ 1H (Yahoo chỉ cho ~730 ngày) gộp theo UTC 00/04/08/12/16/20, "
          "giữ nến có >=3 nến 1H. 1D: interval=1d, ts_utc = 17:00 New York của ngày đó trừ 23h (giờ mở phiên, như backtest).\n",
          "| TS | khung | ngày bắt đầu thực tế | ngày cuối | số nến | lỗ hổng>1 nến |", "|---|---|---|---|---|---|"]
    md += [f"| {b[0]} | {b[1]} | {b[2]} | {b[3]} | {b[4]} | {b[5]} |" for b in bang]
    (THU_MUC / "NGUON.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
