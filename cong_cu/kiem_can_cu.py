#!/usr/bin/env python3
"""Kiểm bằng số liệu: mỗi mốc giá BTC người đó nêu (moc/*.json) trùng với căn cứ kỹ thuật nào, tính lại từ giá thật
tại đúng thời điểm nói — và so với mốc NGẪU NHIÊN cùng khoảng cách để biết trùng thật hay do may.

Căn cứ tính lại (chỉ dùng nến đã đóng trước lúc nói):
  MA34/89/200 (SMA và EMA) khung H1/H4/D1 · đỉnh/đáy fractal H4 (30 ngày) và D1 (120 ngày) ·
  Fibo 0.236–0.786 + mở rộng 1.272/1.618 của sóng D1 30 ngày, D1 90 ngày, H4 7 ngày · số tròn 1.000 / 500.
Trùng = lệch ≤ SAI_SO (0,3%). Vùng giá → xét cả 2 mép.
Lúc nói = giờ bắt đầu live thật (transcripts/gio_live.tsv) + moc_gio; thiếu → HHMM trong tên file / 10:00 VN (sửa 31/10, P2).
Chỉ xét mốc `chac` ≠ false và `tai_san` = BTC.
Cách dùng: python3 cong_cu/kiem_can_cu.py [--chi-tiet]
"""
import csv, datetime as dt, json, random, re, sys
from bisect import bisect_left
from collections import Counter, defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
SAI_SO = 0.003
VN = dt.timedelta(hours=7)


def doc(khung):
    with (GOC / "du_lieu" / f"btc_{khung}.csv").open() as f:
        return [(dt.datetime.fromisoformat(r["ts_utc"]), float(r["high"]), float(r["low"]), float(r["close"])) for r in csv.DictReader(f)]


NEN = {"H1": doc("1H"), "H4": doc("4H"), "D1": doc("1Dutc")}
DO_DAI = {"H1": dt.timedelta(hours=1), "H4": dt.timedelta(hours=4), "D1": dt.timedelta(days=1)}
MOC_THOI = {k: [x[0] for x in v] for k, v in NEN.items()}


def da_dong(khung, luc):
    """Nến khung `khung` đã đóng trước thời điểm UTC `luc`."""
    return NEN[khung][:bisect_left(MOC_THOI[khung], luc - DO_DAI[khung] + dt.timedelta(seconds=1))]


def can_cu(luc):
    ra = []  # (loại, nhãn, giá)
    for k in ("H1", "H4", "D1"):
        n = da_dong(k, luc)
        for p in (34, 89, 200):
            if len(n) >= p:
                ra.append(("MA", f"MA{p} {k} SMA", sum(x[3] for x in n[-p:]) / p))
                a = 2 / (p + 1); e = n[-3 * p][3] if len(n) >= 3 * p else n[0][3]
                for x in n[-3 * p + 1 if len(n) >= 3 * p else 1:]:
                    e = x[3] * a + e * (1 - a)
                ra.append(("MA", f"MA{p} {k} EMA", e))
    for k, ngay, w in (("H4", 30, 3), ("D1", 120, 3)):
        n = [x for x in da_dong(k, luc) if x[0] >= luc - dt.timedelta(days=ngay)]
        for i in range(w, len(n) - w):
            if n[i][1] == max(x[1] for x in n[i - w:i + w + 1]): ra.append(("đỉnh/đáy cũ", f"đỉnh {k} {n[i][0]:%d/%m}", n[i][1]))
            if n[i][2] == min(x[2] for x in n[i - w:i + w + 1]): ra.append(("đỉnh/đáy cũ", f"đáy {k} {n[i][0]:%d/%m}", n[i][2]))
    for k, ngay in (("D1", 30), ("D1", 90), ("H4", 7)):
        n = [x for x in da_dong(k, luc) if x[0] >= luc - dt.timedelta(days=ngay)]
        if len(n) < 3:
            continue
        cao = max(n, key=lambda x: x[1]); thap = min(n, key=lambda x: x[2])
        hi, lo, xuong = cao[1], thap[2], cao[0] < thap[0]
        for f in (0.236, 0.382, 0.5, 0.618, 0.786, 1.272, 1.618):
            gia = lo + (hi - lo) * f if xuong else hi - (hi - lo) * f
            ra.append(("Fibo", f"Fibo {f} sóng {k} {ngay}n", gia))
    return ra


def so_tron(gia):
    return [("số tròn 1.000", "1.000", round(gia / 1000) * 1000), ("số tròn 500", "500", round(gia / 500) * 500)]


def trung(gia, cc):
    return [(loai, nhan) for loai, nhan, g in cc + so_tron(gia) if abs(g - gia) / gia <= SAI_SO]


def loai_noi(s):
    s = s.lower()
    if "fibo" in s: return "Fibo"
    if re.search(r"\bma ?\d|ema|đường ma|cụm ma", s): return "MA"
    if re.search(r"đỉnh|đáy|râu|cũ", s): return "đỉnh/đáy cũ"
    if "tròn" in s or "tâm lý" in s: return "số tròn"
    if "trendline" in s or "trend" in s: return "trendline"
    if "thanh lý" in s or "heatmap" in s: return "thanh lý"
    if "gap" in s: return "gap"
    return "khác"


def gio_live():
    """id video → (giờ bắt đầu UTC không múi, số phút) từ transcripts/gio_live.tsv (cùng định nghĩa cong_cu/cham_dich.py)."""
    ra, p = {}, GOC / "transcripts" / "gio_live.tsv"
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8"), delimiter="\t"):
            try:
                ra[r["id"]] = (dt.datetime.strptime(r["bat_dau_vn"].strip(), "%Y-%m-%d %H:%M") - VN, int(r["phut"]))
            except (KeyError, ValueError, TypeError):
                pass
    return ra


def main():
    chi_tiet = "--chi-tiet" in sys.argv
    random.seed(7)
    that, gia_that, n_moc = Counter(), Counter(), 0
    noi, noi_dung = Counter(), Counter()
    vai = defaultdict(Counter)
    gio_that, so_buoi_that = gio_live(), 0
    for p in sorted((GOC / "moc").glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        vid = p.stem[-11:]  # ID YouTube luôn 11 ký tự cuối tên file
        if vid in gio_that:  # giờ bắt đầu live thật (như cong_cu/cham_dich.py::main)
            bat_dau = gio_that[vid][0]; so_buoi_that += 1
        else:  # dự phòng cũ: HHMM trong tên file, không có thì 10:00 VN
            gio_bd = re.search(r"_(\d{2})(\d{2})_", p.name)
            bat_dau = dt.datetime.fromisoformat(d["ngay"]) + (dt.timedelta(hours=int(gio_bd[1]), minutes=int(gio_bd[2])) if gio_bd else dt.timedelta(hours=10)) - VN
        for m in d.get("moc", []):
            if not m.get("chac", True) or not isinstance(m.get("gia"), (int, float)) or m.get("tai_san", "BTC") != "BTC":
                continue
            mg = m.get("moc_gio")
            luc = bat_dau + (dt.timedelta(seconds=sum(int(x) * k for x, k in zip(mg.split(":"), (3600, 60, 1)))) if mg else dt.timedelta(minutes=30))
            cc = can_cu(luc)
            if not cc:
                continue
            gia_live = da_dong("H1", luc)[-1][3]
            canh = [m["gia"]] + ([m["gia_tren"]] if isinstance(m.get("gia_tren"), (int, float)) else [])
            if any(abs(g / gia_live - 1) > 0.3 for g in canh):
                continue
            n_moc += 1
            tr = {x for g in canh for x in trung(g, cc)}
            for loai in {l for l, _ in tr}: that[loai] += 1
            that["ÍT NHẤT 1 CĂN CỨ"] += bool(tr)
            vai[m.get("vai_tro")]["tổng"] += 1; vai[m.get("vai_tro")]["trùng"] += bool(tr)
            # ngẫu nhiên: cùng khoảng cách tới giá lúc nói, đảo chiều ngẫu nhiên
            for _ in range(20):
                k = random.uniform(0.5, 1.5) * random.choice((-1, 1))
                gr = [gia_live * (1 + (g / gia_live - 1) * k) for g in canh]
                trr = {x for g in gr for x in trung(g, cc)}
                for loai in {l for l, _ in trr}: gia_that[loai] += 1 / 20
                gia_that["ÍT NHẤT 1 CĂN CỨ"] += bool(trr) / 20
            for s in m.get("can_cu") or []:
                l = loai_noi(s); noi[l] += 1
                if l in ("Fibo", "MA", "đỉnh/đáy cũ") and any(x[0] == l for x in tr): noi_dung[l] += 1
                if l == "số tròn" and any(x[0].startswith("số tròn") for x in tr): noi_dung[l] += 1
            if chi_tiet:
                print(f"{d['ngay']} {m.get('vai_tro'):9} {m['gia']:>8} nói: {', '.join(m.get('can_cu') or ['—'])[:50]:50} | tính: {', '.join(n for _, n in sorted(tr))[:90]}")
    print(f"\n{n_moc} mốc giá có số chắc chắn (tai_san BTC) · {so_buoi_that} buổi dùng giờ live thật transcripts/gio_live.tsv\n")
    print(f"{'Căn cứ':22} {'Mốc thật':>10} {'Mốc ngẫu nhiên':>15} {'Gấp':>6}")
    for loai in ["ÍT NHẤT 1 CĂN CỨ", "Fibo", "MA", "đỉnh/đáy cũ", "số tròn 1.000", "số tròn 500"]:
        a, b = that[loai] / n_moc, gia_that[loai] / n_moc
        print(f"{loai:22} {a:>10.0%} {b:>15.0%} {a / b if b else 0:>6.1f}")
    print("\nTheo vai trò (trùng ≥1 căn cứ):", {k: f"{v['trùng']}/{v['tổng']}" for k, v in vai.items()})
    print("Căn cứ người đó NÓI RA (số lần) và tỉ lệ số liệu tính lại khớp:",
          {k: f"{v} (khớp {noi_dung[k]})" if k in noi_dung or k in ('Fibo', 'MA', 'đỉnh/đáy cũ', 'số tròn') else v for k, v in noi.most_common()})


if __name__ == "__main__":
    main()
