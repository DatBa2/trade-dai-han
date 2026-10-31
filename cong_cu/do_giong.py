#!/usr/bin/env python3
"""Đo % GIỐNG: hướng H4 của bot v1 (luật cơ học) so với hướng H4 người đó nói trong phiếu (phieu/*.json).

Bot quyết định tại nến H4 BTC đã đóng ngay trước giờ live (live 10:00 VN → nến đóng 07:00 VN), chỉ dùng dữ liệu tới lúc đó:
  GIAM khi 2 nến H4 liên tiếp đóng dưới dải EMA34 (low), EMA89, EMA200 và D1 gần nhất < EMA34_high D1;
  TANG đối xứng; EMA34/89/200 H4 chụm (< 0,6% giá) hoặc kẹp giữa → PHAN_VAN.
Người đó: phần tử khung H4 trong phiếu (không có thì "chung", rồi phần tử đầu).
Cách dùng: python3 cong_cu/do_giong.py [--chi-tiet]
"""
import csv, datetime as dt, json, re, sys
from bisect import bisect_left
from collections import Counter
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
VN = dt.timedelta(hours=7)


def doc(ten):
    with (GOC / "du_lieu" / ten).open() as f:
        return [(dt.datetime.fromisoformat(r["ts_utc"]), float(r["high"]), float(r["low"]), float(r["close"])) for r in csv.DictReader(f)]


H4, D1 = doc("btc_4H.csv"), doc("btc_1Dutc.csv")


def ema_chuoi(xs, p):
    a, e, ra = 2 / (p + 1), xs[0], []
    for x in xs:
        e = x * a + e * (1 - a); ra.append(e)
    return ra


def chi_bao(n):
    return {"e34h": ema_chuoi([x[1] for x in n], 34), "e34l": ema_chuoi([x[2] for x in n], 34),
            "e34": ema_chuoi([x[3] for x in n], 34), "e89": ema_chuoi([x[3] for x in n], 89), "e200": ema_chuoi([x[3] for x in n], 200)}


CB4, CBD = chi_bao(H4), chi_bao(D1)
T4, TD = [x[0] for x in H4], [x[0] for x in D1]


def huong_bot(luc):
    """luc: UTC. Nến H4 cuối đã đóng = nến mở trước luc−4h."""
    i = bisect_left(T4, luc - dt.timedelta(hours=4) + dt.timedelta(seconds=1)) - 1
    j = bisect_left(TD, luc - dt.timedelta(days=1) + dt.timedelta(seconds=1)) - 1
    if i < 201 or j < 1:
        return None
    def tt(k):
        c = H4[k][3]
        if c < CB4["e34l"][k] and c < CB4["e89"][k] and c < CB4["e200"][k]: return "GIAM"
        if c > CB4["e34h"][k] and c > CB4["e89"][k] and c > CB4["e200"][k]: return "TANG"
        return "PHAN_VAN"
    e = [CB4["e34"][i], CB4["e89"][i], CB4["e200"][i]]
    if (max(e) - min(e)) / H4[i][3] < 0.006:
        return "PHAN_VAN"
    a, b = tt(i), tt(i - 1)
    if a != b or a == "PHAN_VAN":
        return "PHAN_VAN"
    dc = D1[j][3]
    if a == "GIAM" and not dc < CBD["e34h"][j]: return "PHAN_VAN"
    if a == "TANG" and not dc > CBD["e34l"][j]: return "PHAN_VAN"
    return a


def huong_nguoi(d):
    nd = d.get("nhan_dinh") or [{}]
    n = next((x for k in ("H4", "chung") for x in nd if x.get("khung") == k), nd[0])
    return n.get("huong")


def main():
    rows = []
    for p in sorted((GOC / "phieu").glob("2*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        gio = re.search(r"_(\d{2})(\d{2})_", p.name)
        bd = dt.datetime.fromisoformat(d["ngay"]) + (dt.timedelta(hours=int(gio[1]), minutes=int(gio[2])) if gio else dt.timedelta(hours=10)) - VN
        b, n = huong_bot(bd), huong_nguoi(d)
        if b and n in ("TANG", "GIAM", "PHAN_VAN"):
            rows.append((d["ngay"], n, b))
    N = len(rows)
    trung = sum(n == b for _, n, b in rows)
    co_huong = [(n, b) for _, n, b in rows if n != "PHAN_VAN" and b != "PHAN_VAN"]
    print(f"{N} buổi có phiếu + đủ dữ liệu")
    print(f"Giống hoàn toàn (cả PHÂN VÂN): {trung}/{N} = {trung / N:.0%}")
    if co_huong:
        k = sum(n == b for n, b in co_huong)
        print(f"Khi cả hai đều có hướng: cùng chiều {k}/{len(co_huong)} = {k / len(co_huong):.0%}")
    dem_n = Counter(n for _, n, _ in rows); dem_b = Counter(b for _, _, b in rows)
    tot_nhat = max(dem_n, key=dem_n.get)
    print(f"Mốc so sánh 'luôn đoán {tot_nhat}': {dem_n[tot_nhat]}/{N} = {dem_n[tot_nhat] / N:.0%}")
    print("Người đó:", dict(dem_n), "· Bot:", dict(dem_b))
    print("\nBảng chéo (dòng = người đó, cột = bot):")
    nh = ["TANG", "GIAM", "PHAN_VAN"]
    print(" " * 10 + "".join(f"{h:>10}" for h in nh))
    for a in nh:
        print(f"{a:10}" + "".join(f"{sum(1 for _, n, b in rows if n == a and b == c):>10}" for c in nh))
    thang = {}
    for ng, n, b in rows:
        t = thang.setdefault(ng[:7], [0, 0]); t[0] += n == b; t[1] += 1
    print("\nTheo tháng:", " · ".join(f"{k[5:]}: {v[0]}/{v[1]}" for k, v in sorted(thang.items())))
    if "--chi-tiet" in sys.argv:
        for r in rows: print(*r)


if __name__ == "__main__":
    main()
