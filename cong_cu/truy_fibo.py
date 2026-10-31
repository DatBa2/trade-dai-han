#!/usr/bin/env python3
"""Dò điểm neo Fibo người đó dùng: với mỗi mốc moc/*.json có căn cứ "Fibo <tỉ lệ>", thử mọi cặp
(đỉnh thứ kH gần nhất, đáy thứ kL gần nhất) trên D1 và H4 (đỉnh/đáy fractal rộng W nến mỗi bên),
xem cặp nào cho ra đúng con số (lệch ≤ SAI_SO). So với tỉ lệ Fibo ngẫu nhiên để loại trùng do may.

Thứ tự thời gian quyết định chiều: đáy trước đỉnh sau = sóng tăng → thoái lui = đỉnh − (đỉnh−đáy)·r;
đỉnh trước đáy sau = sóng giảm → hồi = đáy + (đỉnh−đáy)·r. r > 1 là mở rộng.
Cách dùng: python3 cong_cu/truy_fibo.py
"""
import datetime as dt, json, random, re
from collections import Counter
from pathlib import Path
import kiem_can_cu as K

GOC = Path(__file__).resolve().parent.parent
SAI_SO = 0.005
W = 5
LUI = {"D1": dt.timedelta(days=300), "H4": dt.timedelta(days=60)}
TI_LE = (0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618)


def diem_xoay(khung, luc):
    n = [x for x in K.da_dong(khung, luc) if x[0] >= luc - LUI[khung]]
    dinh = [(n[i][0], n[i][1]) for i in range(W, len(n) - W) if n[i][1] == max(x[1] for x in n[i - W:i + W + 1])]
    day = [(n[i][0], n[i][2]) for i in range(W, len(n) - W) if n[i][2] == min(x[2] for x in n[i - W:i + W + 1])]
    return dinh[::-1][:4], day[::-1][:4]  # gần nhất trước


def muc(dinh, day, r):
    (td, h), (tl, l) = dinh, day
    return h - (h - l) * r if tl < td else l + (h - l) * r


def main():
    random.seed(11)
    khop, ngau, n = Counter(), Counter(), 0
    khop_bat_ky = ngau_bat_ky = 0
    for p in sorted((GOC / "moc").glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        gio = re.search(r"_(\d{2})(\d{2})_", p.name)
        bd = dt.datetime.fromisoformat(d["ngay"]) + (dt.timedelta(hours=int(gio[1]), minutes=int(gio[2])) if gio else dt.timedelta(hours=10)) - K.VN
        for m in d.get("moc", []):
            if not m.get("chac", True) or not isinstance(m.get("gia"), (int, float)):
                continue
            tl = next((re.findall(r"fibo[^0-9]{0,15}(0[.,]\d+|1[.,]\d+|1\b|2\b)", c.lower()) for c in m.get("can_cu") or [] if "fibo" in c.lower()), None)
            if not tl:
                continue
            r = float(tl[0].replace(",", "."))
            mg = m.get("moc_gio")
            luc = bd + (dt.timedelta(seconds=sum(int(x) * k for x, k in zip(mg.split(":"), (3600, 60, 1)))) if mg else dt.timedelta(minutes=30))
            canh = [m["gia"]] + ([m["gia_tren"]] if isinstance(m.get("gia_tren"), (int, float)) else [])
            gan = lambda v: min(abs(v - g) / g for g in canh) <= SAI_SO
            n += 1; a = b = False
            r_ng = random.choice([x for x in TI_LE if x != r])
            for khung in ("D1", "H4"):
                dinh, day = diem_xoay(khung, luc)
                for i, dd in enumerate(dinh):
                    for j, dy in enumerate(day):
                        ten = f"{khung} đỉnh#{i + 1} × đáy#{j + 1}"
                        if gan(muc(dd, dy, r)): khop[ten] += 1; a = True
                        if gan(muc(dd, dy, r_ng)): ngau[ten] += 1; b = True
            khop_bat_ky += a; ngau_bat_ky += b
    print(f"{n} mốc có 'Fibo <tỉ lệ>' · khớp ít nhất 1 cặp neo: {khop_bat_ky / n:.0%} (tỉ lệ ngẫu nhiên: {ngau_bat_ky / n:.0%})\n")
    print(f"{'Cặp neo (#1 = gần nhất)':28} {'khớp':>6} {'ngẫu nhiên':>11}")
    for ten, c in khop.most_common(14):
        print(f"{ten:28} {c / n:>6.0%} {ngau[ten] / n:>11.0%}")


if __name__ == "__main__":
    main()
