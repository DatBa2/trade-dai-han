#!/usr/bin/env python3
"""Tải nến BTC-USDT khung bất kỳ từ API công khai OKX → du_lieu/btc_<khung>.csv (giờ UTC = giờ MỞ nến, chỉ nến đã đóng).

Cách dùng: python3 cong_cu/lay_nen.py <1m|5m|15m|1H|4H|1Dutc> <từ ngày YYYY-MM-DD> [--noi]
  --noi : file đã có thì giữ nến cũ, chỉ tải phần mới hơn nến cuối trong file (đỡ gọi API).
1m không tải cả khoảng dài: bộ chấm gọi lay_1m(tu, den) khi cần phân thứ tự trong 1 nến 5m → cache du_lieu/btc_1m_cache.csv.
"""
import csv, datetime as dt, json, sys, time, urllib.request
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
API = "https://www.okx.com/api/v5/market/history-candles?instId=BTC-USDT&bar={}&limit=100&after={}"
NGHI = 0.12  # giây giữa 2 lần gọi (giới hạn OKX 20 lần / 2 giây)
COT = ["ts_utc", "open", "high", "low", "close", "vol"]
CACHE_1M = GOC / "du_lieu" / "btc_1m_cache.csv"


def goi(khung, after):
    """1 trang ≤ 100 nến có giờ mở < after (ms), mới → cũ. Thử lại 4 lần khi lỗi mạng."""
    req = urllib.request.Request(API.format(khung, after), headers={"User-Agent": "Mozilla/5.0"})
    for lan in range(4):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)["data"]
        except Exception:
            if lan == 3:
                raise
            time.sleep(2 * (lan + 1))


def tai(khung, tu_ms, den_ms):
    """Nến đã đóng có giờ mở trong [tu_ms, den_ms) → {'YYYY-MM-DD HH:MM': (ts, o, h, l, c, v)}."""
    after, ra = den_ms, {}
    while after > tu_ms:
        d = goi(khung, after)
        if not d:
            break
        for ts, o, h, l, c, v, *_, xac_nhan in d:
            if xac_nhan == "1" and tu_ms <= int(ts) < den_ms:
                k = dt.datetime.fromtimestamp(int(ts) / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
                ra[k] = (k, o, h, l, c, v)
        after = int(d[-1][0])
        time.sleep(NGHI)
    return ra


def doc_file(p):
    if not p.exists():
        return {}
    with p.open() as f:
        return {r["ts_utc"]: tuple(r[k] for k in COT) for r in csv.DictReader(f)}


def ghi_file(p, ra):
    with p.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(COT); w.writerows(sorted(ra.values()))


def ms(t):
    return int(t.replace(tzinfo=dt.timezone.utc).timestamp() * 1000) if t.tzinfo is None else int(t.timestamp() * 1000)


_CACHE_1M = None


def lay_1m(tu, den):
    """Nến 1m có giờ mở trong [tu, den) (datetime UTC, có hoặc không múi giờ) → [(mo naive UTC, h, l, c)].
    Đọc cache du_lieu/btc_1m_cache.csv; thiếu thì tải đúng khoảng đó từ OKX rồi ghi thêm vào cache."""
    global _CACHE_1M
    if _CACHE_1M is None:
        _CACHE_1M = doc_file(CACHE_1M)
    tu = tu.astimezone(dt.timezone.utc).replace(tzinfo=None) if tu.tzinfo else tu
    den = den.astimezone(dt.timezone.utc).replace(tzinfo=None) if den.tzinfo else den
    can = []
    t = tu
    while t < den:
        can.append(t.strftime("%Y-%m-%d %H:%M")); t += dt.timedelta(minutes=1)
    if any(k not in _CACHE_1M for k in can) and den <= dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) - dt.timedelta(minutes=1):
        moi = tai("1m", ms(tu), ms(den))
        if moi:
            _CACHE_1M.update(moi)
            CACHE_1M.parent.mkdir(parents=True, exist_ok=True)
            ghi_file(CACHE_1M, _CACHE_1M)
    return [(dt.datetime.strptime(k, "%Y-%m-%d %H:%M"), float(_CACHE_1M[k][2]), float(_CACHE_1M[k][3]), float(_CACHE_1M[k][4]))
            for k in can if k in _CACHE_1M]


def main():
    khung, tu = sys.argv[1], dt.datetime.fromisoformat(sys.argv[2]).replace(tzinfo=dt.timezone.utc)
    p = GOC / "du_lieu" / f"btc_{khung}.csv"
    ra = doc_file(p) if "--noi" in sys.argv else {}
    tu_ms = int(tu.timestamp() * 1000)
    if ra:
        tu_ms = max(tu_ms, ms(dt.datetime.strptime(max(ra), "%Y-%m-%d %H:%M")))  # chỉ tải phần mới hơn file
    ra.update(tai(khung, tu_ms, int(time.time() * 1000)))
    ghi_file(p, ra)
    print(f"✓ {p.name}: {len(ra)} nến, {min(ra)} → {max(ra)}")


if __name__ == "__main__":
    main()
