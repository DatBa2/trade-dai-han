#!/usr/bin/env python3
"""Tải nến BTC-USDT 15 phút từ API công khai OKX → du_lieu/btc_15m.csv (giờ UTC).

Dùng để: điền giá thật lúc live vào phiếu, và chấm nhận định với giá chạy sau đó.
Chạy lại được: chỉ tải phần còn thiếu ở cuối file.
Cách dùng: python3 cong_cu/lay_gia.py [--tu 2026-08-01]
"""
import argparse, csv, datetime as dt, json, time, urllib.request
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent / "du_lieu" / "btc_15m.csv"
API = "https://www.okx.com/api/v5/market/history-candles?instId=BTC-USDT&bar=15m&limit=100&after={}"
COT = ["ts_utc", "open", "high", "low", "close", "vol"]


def tai(after_ms):
    req = urllib.request.Request(API.format(after_ms), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["data"]  # mới → cũ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tu", default="2026-08-01")
    tu_ms = int(dt.datetime.fromisoformat(ap.parse_args().tu).replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
    FILE.parent.mkdir(exist_ok=True)
    cu = {}
    if FILE.exists():
        with FILE.open() as f:
            cu = {r["ts_utc"]: r for r in csv.DictReader(f)}
    moc_cuoi = max((int(dt.datetime.fromisoformat(k).replace(tzinfo=dt.timezone.utc).timestamp() * 1000) for k in cu), default=tu_ms)

    after, moi = int(time.time() * 1000), {}
    while True:
        rows = tai(after)
        if not rows:
            break
        for ts, o, h, l, c, v, *_, xac_nhan in rows:
            if xac_nhan == "0":  # nến chưa đóng
                continue
            k = dt.datetime.fromtimestamp(int(ts) / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
            moi[k] = {"ts_utc": k, "open": o, "high": h, "low": l, "close": c, "vol": v}
        after = int(rows[-1][0])
        if after <= max(tu_ms, moc_cuoi - 15 * 60_000):
            break
        time.sleep(0.15)  # giới hạn API công khai 20 lần / 2 giây
    cu.update({k: v for k, v in moi.items() if k >= dt.datetime.fromtimestamp(tu_ms / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")})
    with FILE.open("w", newline="") as f:
        w = csv.DictWriter(f, COT); w.writeheader(); w.writerows(sorted(cu.values(), key=lambda r: r["ts_utc"]))
    ks = sorted(cu)
    print(f"✓ {FILE.name}: {len(ks)} nến 15m, {ks[0]} → {ks[-1]} UTC")


if __name__ == "__main__":
    main()
