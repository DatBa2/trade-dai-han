#!/usr/bin/env python3
"""Chấm 1 nhận định với giá thật (nến 15m OKX): trong cửa sổ có chạm chặng 1 / đích / mốc vô hiệu không, cái nào trước.

Cách dùng: python3 cong_cu/cham_gia.py <COIN> <giờ VN "YYYY-MM-DD HH:MM"> <TANG|GIAM> <đích> [chặng1] [mốc_sai] [giờ_hạn=24]
  mốc_sai: giá mà nếu chạm thì coi như sai hướng (vd view GIẢM thì là mốc phía trên)
"""
import datetime as dt, json, sys, time, urllib.request

VN = dt.timedelta(hours=7)


def nen_15m(coin, tu, den):
    url = "https://www.okx.com/api/v5/market/history-candles?instId={}-USDT&bar=15m&limit=100&after={}"
    ra, after = [], int((den - VN).replace(tzinfo=dt.timezone.utc).timestamp() * 1000) + 15 * 60_000
    while True:
        req = urllib.request.Request(url.format(coin, after), headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)["data"]
        if not d:
            break
        for x in d:
            t = dt.datetime.fromtimestamp(int(x[0]) / 1000, dt.timezone.utc).replace(tzinfo=None) + VN
            if tu <= t < den:
                ra.append((t, *map(float, x[1:5])))
        after = int(d[-1][0])
        if dt.datetime.fromtimestamp(after / 1000, dt.timezone.utc).replace(tzinfo=None) + VN <= tu:
            break
        time.sleep(0.15)
    return sorted(ra)


def main():
    coin, luc, huong, dich = sys.argv[1], dt.datetime.fromisoformat(sys.argv[2]), sys.argv[3], float(sys.argv[4])
    chang1 = float(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != "-" else None
    moc_sai = float(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] != "-" else None
    han = float(sys.argv[7]) if len(sys.argv) > 7 else 24
    nen = nen_15m(coin, luc, min(luc + dt.timedelta(hours=han), dt.datetime.now() + dt.timedelta(minutes=15)))
    if not nen:
        print("chưa có nến"); return
    len_ = lambda gia: next((t for t, o, h, l, c in nen if h >= gia), None)
    xuong = lambda gia: next((t for t, o, h, l, c in nen if l <= gia), None)
    cham = {"đích": (xuong if huong == "GIAM" else len_)(dich)}
    if chang1:  # chặng 1 ngược hướng chính
        cham["chặng 1"] = (len_ if huong == "GIAM" else xuong)(chang1)
    if moc_sai:
        cham["mốc sai"] = (len_ if huong == "GIAM" else xuong)(moc_sai)
    mo, dong = nen[0][1], nen[-1][4]
    print(f"{coin} {luc:%d/%m %H:%M} {huong} đích {dich:g}: mở {mo:g} → giá cuối {dong:g} ({(dong / mo - 1) * 100:+.2f}%) · "
          f"cao {max(x[2] for x in nen):g} thấp {min(x[3] for x in nen):g} · {len(nen)} nến tới {nen[-1][0]:%d/%m %H:%M}")
    for k, t in sorted(cham.items(), key=lambda kv: kv[1] or dt.datetime.max):
        print(f"   {k}: {'CHẠM lúc ' + t.strftime('%d/%m %H:%M') if t else 'không chạm'}")
    print(f"   hướng theo giá cuối: {'ĐÚNG' if (dong > mo) == (huong == 'TANG') else 'SAI'}")


if __name__ == "__main__":
    main()
