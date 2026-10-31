#!/usr/bin/env python3
"""Truy ngược CÔNG THỨC người đó dùng để ra con số, từ moc/*.json + giá thật:

1. MA: khi nói "MA<n> <khung>" thì con số khớp SMA hay EMA hơn, sai số bao nhiêu.
2. Fibo: khi nói "Fibo <tỉ lệ>" thì sóng nào cho ra đúng con số — thử các giả thuyết kéo Fibo
   (D1 30/60/90/180 ngày, H4 7/14 ngày, tuần 26 tuần, cặp đỉnh/đáy lớn gần nhất D1) và so với tỉ lệ ngẫu nhiên.
3. Đỉnh/đáy/râu cũ: con số có trùng đỉnh/đáy fractal thật không.
Sai số cho phép SAI_SO (0,6%) vì người nói hay làm tròn ("69" thay cho 68.730).
Cách dùng: python3 cong_cu/truy_nguoc.py
"""
import datetime as dt, json, random, re
from collections import Counter, defaultdict
from pathlib import Path
import kiem_can_cu as K

GOC = Path(__file__).resolve().parent.parent
SAI_SO = 0.006
TI_LE = (0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618)


def _tuan():
    nhom = {}
    for t, h, l, c in K.NEN["D1"]:
        k = t - dt.timedelta(days=t.weekday())
        nhom.setdefault(k, []).append((h, l, c))
    return [(k, max(x[0] for x in v), min(x[1] for x in v), v[-1][2]) for k, v in sorted(nhom.items())]


K.NEN["W1"] = _tuan(); K.MOC_THOI["W1"] = [x[0] for x in K.NEN["W1"]]; K.DO_DAI["W1"] = dt.timedelta(days=7)


def ema(xs, p):
    a = 2 / (p + 1); e = xs[0]
    for x in xs[1:]:
        e = x * a + e * (1 - a)
    return e


def _doc_cme():
    import csv
    with (GOC / "du_lieu" / "cme_btc_1h.csv").open() as f:
        return [(dt.datetime.fromisoformat(r["ts_utc"]), float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"]))
                for r in csv.DictReader(f)]


CME = _doc_cme()


def gap_cme(luc):
    """Gap CME thật (hợp đồng BTC=F, Yahoo H1): chỗ nghỉ > 20 giờ; mép = giá đóng trước nghỉ và giá mở sau nghỉ.
    Chỉ giữ gap CHƯA LẤP tính tới lúc nói (giá CME sau đó chưa quay về giá đóng trước nghỉ), trong 26 tuần."""
    n = [x for x in CME if x[0] < luc]; ra = []
    for i in range(1, len(n)):
        if n[i][0] - n[i - 1][0] > dt.timedelta(hours=20) and n[i][0] > luc - dt.timedelta(weeks=26):
            dong, mo = n[i - 1][4], n[i][1]
            if not any(x[3] <= dong <= x[2] for x in n[i:]):
                ra += [dong, mo]
    return ra


def sma_ema(khung, p, luc):
    n = K.da_dong(khung, luc)
    if len(n) < p:
        return None, None
    s = sum(x[3] for x in n[-p:]) / p
    a = 2 / (p + 1); e = n[max(0, len(n) - 4 * p)][3]
    for x in n[max(1, len(n) - 4 * p + 1):]:
        e = x[3] * a + e * (1 - a)
    return s, e


def song(luc):
    """Các giả thuyết sóng để kéo Fibo: {tên: (đầu, cuối)} theo thứ tự thời gian."""
    ra = {}
    def tu_cua_so(ten, khung, ngay):
        n = [x for x in K.da_dong(khung, luc) if x[0] >= luc - dt.timedelta(days=ngay)]
        if len(n) > 3:
            cao = max(n, key=lambda x: x[1]); thap = min(n, key=lambda x: x[2])
            ra[ten] = (cao[1], thap[2]) if cao[0] < thap[0] else (thap[2], cao[1])
    for ngay in (30, 60, 90, 180):
        tu_cua_so(f"D1 {ngay} ngày", "D1", ngay)
    for ngay in (7, 14):
        tu_cua_so(f"H4 {ngay} ngày", "H4", ngay)
    tu_cua_so("tuần 26 tuần", "D1", 182)
    n = K.da_dong("D1", luc)[-200:]; w = 5
    piv = [(n[i][0], "H", n[i][1]) for i in range(w, len(n) - w) if n[i][1] == max(x[1] for x in n[i - w:i + w + 1])]
    piv += [(n[i][0], "L", n[i][2]) for i in range(w, len(n) - w) if n[i][2] == min(x[2] for x in n[i - w:i + w + 1])]
    piv.sort()
    if len(piv) >= 2:
        # cặp đỉnh–đáy lớn gần nhất: điểm xoay cuối và điểm xoay khác loại trước nó
        cuoi = piv[-1]; truoc = next((p for p in reversed(piv[:-1]) if p[1] != cuoi[1]), None)
        if truoc:
            ra["cặp xoay D1 gần nhất"] = (truoc[2], cuoi[2])
    return ra


def muc_fibo(dau, cuoi, r):
    return cuoi - (cuoi - dau) * r  # r<1: thoái lui về phía đầu; r>1: mở rộng vượt đầu


def main():
    random.seed(3)
    ma = defaultdict(lambda: {"SMA": [], "EMA": []})
    fibo_khop, fibo_ngau, n_fibo = Counter(), Counter(), 0
    dinh_day = [0, 0]; gap_dem = [0, 0]
    for p in sorted((GOC / "moc").glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        gio = re.search(r"_(\d{2})(\d{2})_", p.name)
        bd = dt.datetime.fromisoformat(d["ngay"]) + (dt.timedelta(hours=int(gio[1]), minutes=int(gio[2])) if gio else dt.timedelta(hours=10)) - K.VN
        for m in d.get("moc", []):
            if not m.get("chac", True) or not isinstance(m.get("gia"), (int, float)):
                continue
            mg = m.get("moc_gio")
            luc = bd + (dt.timedelta(seconds=sum(int(x) * k for x, k in zip(mg.split(":"), (3600, 60, 1)))) if mg else dt.timedelta(minutes=30))
            canh = [m["gia"]] + ([m["gia_tren"]] if isinstance(m.get("gia_tren"), (int, float)) else [])
            gan = lambda v: min(abs(v - g) / g for g in canh)
            for cc in m.get("can_cu") or []:
                s = cc.lower()
                for so, khung in re.findall(r"(?:e?ma)\s?(34|89|200|610)\s*(?:khung\s*)?(h1|h4|d1|w1|ngày|tuần|4h|1h)?", s):
                    khung = {"ngày": "D1", "tuần": "W1", "4h": "H4", "1h": "H1", "": None}.get(khung, khung.upper() if khung else None)
                    for k in ([khung] if khung else ["H4", "D1"]):
                        sm, em = sma_ema(k, int(so), luc)
                        if sm:
                            ma[f"MA{so} {k}"]["SMA"].append(gan(sm)); ma[f"MA{so} {k}"]["EMA"].append(gan(em))
                            if so == "34":  # dải rồng Sonic R: EMA34 của high và low
                                n = K.da_dong(k, luc)[-200:]
                                ma[f"MA{so} {k}"].setdefault("dải EMA34", []).append(min(gan(ema([x[1] for x in n], 34)), gan(ema([x[2] for x in n], 34)), gan(em)))
                tl = re.findall(r"fibo(?:nacci)?\s*(?:mở rộng\s*)?(0[.,]\d+|1[.,]\d+|1\b)", s)
                if tl:
                    r = float(tl[0].replace(",", ".")); n_fibo += 1
                    for ten, (dau, cuoi) in song(luc).items():
                        if gan(muc_fibo(dau, cuoi, r)) <= SAI_SO: fibo_khop[ten] += 1
                        if gan(muc_fibo(dau, cuoi, random.choice(TI_LE))) <= SAI_SO: fibo_ngau[ten] += 1
                if "gap" in s:
                    gaps = gap_cme(luc); gap_dem[1] += 1; gap_dem[0] += any(gan(g) <= SAI_SO for g in gaps)
                if re.search(r"đỉnh|đáy|râu", s):
                    piv = [g for loai, nhan, g in K.can_cu(luc) if loai == "đỉnh/đáy cũ"]
                    dinh_day[1] += 1; dinh_day[0] += any(gan(g) <= SAI_SO for g in piv)
    print("=== 1. MA người đó nói: SMA hay EMA? (sai số trung vị, % khớp ≤0,6%) ===")
    for k, v in sorted(ma.items(), key=lambda x: -len(x[1]["SMA"])):
        if len(v["SMA"]) >= 3:
            tv = lambda xs: sorted(xs)[len(xs) // 2]
            print(f"  {k:10} n={len(v['SMA']):3}  " + "  ·  ".join(
                f"{t} {tv(xs):.2%} (khớp {sum(x <= SAI_SO for x in xs) / len(xs):.0%})" for t, xs in v.items()))
    print(f"\n=== 2. Fibo người đó nói (n={n_fibo}): giả thuyết sóng nào cho đúng con số ===")
    for ten in sorted(set(fibo_khop) | set(fibo_ngau), key=lambda t: -fibo_khop[t]):
        print(f"  {ten:24} khớp {fibo_khop[ten] / n_fibo:5.0%}   (tỉ lệ ngẫu nhiên: {fibo_ngau[ten] / n_fibo:4.0%})")
    print(f"\n=== 3. 'đỉnh/đáy/râu cũ' khớp đỉnh/đáy thật: {dinh_day[0]}/{dinh_day[1]} ===")
    print(f"=== 4. 'gap CME' khớp mép gap CME chưa lấp (BTC=F thật): {gap_dem[0]}/{gap_dem[1]} ===")


if __name__ == "__main__":
    main()
