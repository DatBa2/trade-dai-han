#!/usr/bin/env python3
"""Bang su kien trendline cho MOI buoi (180 buoi trong transcripts/gio_live.tsv) bang bien the DA KHOA (CHON.md).
C = luc ket thuc live (bat_dau_vn + phut, doi UTC). Khoang = (C buoi truoc, C buoi nay]; buoi dau: (C − 24h, C].
Moi buoi 4 dong: khung H4/D1 × loai khang_cu_giam/ho_tro_tang.
  Tai C: duong chinh (neo, gia duong, cach % toi gia, so cham, tuoi, trang thai, lan pha gan nhat + volume).
  Trong khoang: duong chinh tai C buoi truoc co bi pha khong (chieu, 1/2 nen, pha gia/that, test lai, ti le volume)
  + dem moi duong con hieu luc tai C truoc bi pha trong khoang (pha that / pha gia / chua ro).
Chi TINH (khong cham). Dung: python3 hoc_v5/trendline/su_kien.py [ten_bien_the]  → hoc_v5/trendline/su_kien.csv
"""
import csv, datetime as dt, sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "cong_cu"))
import trendline as T  # noqa: E402

RA = GOC / "hoc_v5" / "trendline"


def bien_the_khoa():
    p = RA / "CHON.md"
    for dong in p.read_text(encoding="utf-8").splitlines():
        if dong.startswith("BIEN_THE_KHOA:"):
            return dong.split(":", 1)[1].strip().strip("`")
    raise SystemExit("CHON.md chua co dong BIEN_THE_KHOA:")


def doc_buoi():
    ra = []
    with open(GOC / "transcripts" / "gio_live.tsv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            bd = dt.datetime.strptime(r["bat_dau_vn"], "%Y-%m-%d %H:%M")
            c = bd + dt.timedelta(minutes=int(r["phut"])) - dt.timedelta(hours=7)
            ra.append({"buoi": f"{bd:%Y-%m-%d}_{r['id']}", "id": r["id"], "ngay": f"{bd:%Y-%m-%d}",
                       "C": int(c.replace(tzinfo=dt.timezone.utc).timestamp())})
    ra.sort(key=lambda z: z["C"])
    return ra


def f2(x, nd=1):
    return "" if x is None else f"{x:.{nd}f}"


def main():
    ten = sys.argv[1] if len(sys.argv) > 1 else bien_the_khoa()
    bt = T.bien_the(ten)
    du = T.BoDuLieu.doc()
    buoi = doc_buoi()
    cot = ["buoi", "giai_doan", "C_utc", "C_truoc_utc", "gia_C", "khung", "loai", "so_duong",
           "chinh_id", "neo1_ts", "neo1_gia", "neo2_ts", "neo2_gia", "doc_ngay", "gia_duong_C", "cach_pct", "so_cham",
           "tuoi_ngay", "trang_thai_C", "pha_gan_t", "pha_gan_2nen", "pha_gan_vol", "pha_gan_ket_qua",
           "chinh_truoc_id", "chinh_truoc_pha", "chieu_pha", "t_pha", "pha_2nen", "pha_ket_qua", "pha_test_lai",
           "pha_vol", "so_duong_pha_khoang", "so_pha_that", "so_pha_gia", "so_pha_chua_ro", "bien_the"]
    dong = []
    for i, b in enumerate(buoi):
        C = b["C"]
        C0 = buoi[i - 1]["C"] if i else C - T.NGAY
        gia = du.gia_tai(C)
        for kh in T.KHUNG:
            for lo in T.LOAI:
                ds = T.duong_hieu_luc(du, C, bt, kh, lo)
                c = T.chon_chinh(ds, bt)
                c0, sk = T.su_kien_khoang(du, bt, kh, lo, C0, C)
                pc = [z for z in sk if z["la_chinh"]]
                p1 = pc[0] if pc else None
                r = {"buoi": b["buoi"], "giai_doan": "truoc_0701" if b["ngay"] < "2026-07-01" else "tu_0701",
                     "C_utc": T.chuoi_tu_ts(C), "C_truoc_utc": T.chuoi_tu_ts(C0), "gia_C": f2(gia), "khung": kh, "loai": lo,
                     "so_duong": len(ds), "bien_the": ten}
                if c:
                    ph = c["pha"]
                    r.update({"chinh_id": c["id"], "neo1_ts": c["neo1_ts"], "neo1_gia": f2(c["neo1_gia"]),
                              "neo2_ts": c["neo2_ts"], "neo2_gia": f2(c["neo2_gia"]), "doc_ngay": f2(c["doc_ngay"]),
                              "gia_duong_C": f2(c["gia_t"]), "cach_pct": f2(c["cach_pct"], 2), "so_cham": c["so_cham"],
                              "tuoi_ngay": f2(c["tuoi_ngay"]), "trang_thai_C": c["trang_thai"],
                              "pha_gan_t": T.chuoi_tu_ts(ph["t_pha"]) if ph else "",
                              "pha_gan_2nen": int(ph["hai_nen"]) if ph else "", "pha_gan_vol": f2(ph["vol"], 2) if ph else "",
                              "pha_gan_ket_qua": ph["ket_qua"] if ph else ""})
                r["chinh_truoc_id"] = c0["id"] if c0 else ""
                r["chinh_truoc_pha"] = int(p1 is not None) if c0 else ""
                if p1:
                    r.update({"chieu_pha": p1["chieu"], "t_pha": T.chuoi_tu_ts(p1["t_pha"]), "pha_2nen": int(p1["hai_nen"]),
                              "pha_ket_qua": p1["ket_qua"], "pha_test_lai": int(p1["test_lai"]), "pha_vol": f2(p1["vol"], 2)})
                r["so_duong_pha_khoang"] = len({z["id"] for z in sk})
                r["so_pha_that"] = sum(1 for z in sk if z["ket_qua"] == "pha_that")
                r["so_pha_gia"] = sum(1 for z in sk if z["ket_qua"] == "pha_gia")
                r["so_pha_chua_ro"] = sum(1 for z in sk if z["ket_qua"] == "chua_ro")
                dong.append(r)
    with open(RA / "su_kien.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cot)
        w.writeheader()
        for r in dong:
            w.writerow({k: r.get(k, "") for k in cot})
    print(f"su_kien.csv: {len(buoi)} buoi × 4 = {len(dong)} dong, bien the {ten}")


if __name__ == "__main__":
    main()
