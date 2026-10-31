#!/usr/bin/env python3
"""Kiem thu cong_cu/trendline.py.
  1. CAT CUT: du lieu cat tai t (chi nen dong <= t) cho CUNG ket qua tai t voi du lieu day du (moi duong: id, gia, cham,
     trang thai, lan pha; duong chinh; su kien trong khoang) — nhieu thoi diem × nhieu bien the.
  2. CA DUNG TAY: chuoi nen gia lap co 1 duong khang cu giam / ho tro tang biet truoc → kiem neo, gia duong, cham,
     pha 1 nen / 2 nen, pha gia, pha that + test lai, ti le volume, duong bi xuyen giua 2 neo thi khong hop le.
Dung: python3 hoc_v5/trendline/kiem_tra.py   (in PASS/FAIL tung muc; exit 1 neu co FAIL)
"""
import random, sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "cong_cu"))
import trendline as T  # noqa: E402

LOI = []


def kiem(dk, ten):
    print(("PASS " if dk else "FAIL ") + ten)
    if not dk:
        LOI.append(ten)


def _chu_ky(du, t, bt):
    """Anh chup ket qua tai t (bo truong _d, lam tron float de so)."""
    ra = {}
    for key, v in T.tai_thoi_diem(du, t, bt).items():
        ds = []
        for r in v["duong"]:
            ds.append((r["id"], round(r["gia_t"], 6), r["so_cham"], r["trang_thai"],
                       None if not r["pha"] else (r["pha"]["t_pha"], r["pha"]["hai_nen"], r["pha"]["ket_qua"],
                                                  None if r["pha"]["vol"] is None else round(r["pha"]["vol"], 9))))
        ra[key] = (sorted(ds), v["chinh"]["id"] if v["chinh"] else None)
    return ra


def _khoang(du, bt, t0, t1):
    ra = {}
    for kh in T.KHUNG:
        for lo in T.LOAI:
            c0, ds = T.su_kien_khoang(du, bt, kh, lo, t0, t1)
            ra[(kh, lo)] = (c0["id"] if c0 else None,
                            [(z["id"], z["t_pha"], z["hai_nen"], z["ket_qua"], z["test_lai"]) for z in ds])
    return ra


def kiem_cat_cut():
    du = T.BoDuLieu.doc()
    h4 = du.nen["H4"]
    rng = random.Random(31)
    t_dau, t_cuoi = T.ts_tu_chuoi("2026-01-05 00:00"), h4.mo[-1]
    ds_t = [rng.randrange(t_dau, t_cuoi) for _ in range(14)]
    # them cac moc nhay cam: dung luc dong nen H4, ngay sau, 1 giay truoc
    for s in ("2026-02-25 20:00", "2026-03-12 04:00", "2026-08-18 04:00", "2026-10-02 04:00"):
        x = T.ts_tu_chuoi(s)
        ds_t += [x, x - 1, x + 1]
    ds_bt = [T.bien_the(n) for n in ("rau|2|ngan|nhieu_cham", "than|3|dai|cuc_tri", "rau|3|dai|gan_gia",
                                     "than|2|ngan|dai_nhat")]
    sai = 0
    for t in ds_t:
        du_cat = du.cat(t)
        for bt in ds_bt:
            if _chu_ky(du, t, bt) != _chu_ky(du_cat, t, bt):
                sai += 1
                print("   lech tai", T.chuoi_tu_ts(t), bt["ten"])
            t0 = t - 3 * T.NGAY
            if _khoang(du, bt, t0, t) != _khoang(du_cat, bt, t0, t):
                sai += 1
                print("   lech su kien khoang tai", T.chuoi_tu_ts(t), bt["ten"])
    kiem(sai == 0, f"cat cut: {len(ds_t)} thoi diem × {len(ds_bt)} bien the, ket qua tai t trung nhau (lech {sai})")


def _du_gia_lap():
    """Chuoi H4 gia lap 120 nen tu 2026-01-01 00:00. Gia nen = 100 + rang cua, 2 dinh fractal ro o nen 20 (h=130)
    va nen 40 (h=120) → duong khang cu giam doc −0,5/nen. D1 dung tu H4 (6 nen/ngay)."""
    x0 = T.ts_tu_chuoi("2026-01-01 00:00")
    n = 120
    mo = [x0 + i * 4 * 3600 for i in range(n)]
    o, h, l, c, v = [], [], [], [], []
    for i in range(n):
        base = 100.0
        o.append(base); c.append(base); h.append(base + 1); l.append(base - 1); v.append(10.0)
    h[20], c[20], o[20] = 130.0, 101.0, 100.0
    h[40], c[40], o[40] = 120.0, 101.0, 100.0
    # day fractal: nen 10 (l=80) va nen 30 (l=85) → ho tro tang doc +0,25/nen
    l[10], l[30] = 80.0, 85.0
    # gia tri duong khang cu tai nen i = 130 − 0,5 (i − 20) → nen 60: 110; nen 70: 105
    # nen 60: pha 1 nen roi quay lai (pha gia) ; nen 70-71: pha 2 nen, khong quay → pha that; nen 74: test lai
    c[60], h[60], v[60] = 111.0, 111.5, 30.0       # vuot 110
    c[61], h[61] = 100.0, 101.0                    # quay lai → pha gia
    for i in range(70, 90):
        c[i], o[i], h[i], l[i] = 112.0, 111.0, 113.0, 110.5
    l[74] = 103.1  # duong tai 74 = 103 → rau trong ±0,3% (≤ 103,309) ma close 112 van tren → test lai
    h4 = T.Nen("H4", mo, o, h, l, c, v)
    # D1: gop 6 nen
    dmo, do, dh, dl, dc, dv = [], [], [], [], [], []
    for s in range(0, n - 5, 6):
        dmo.append(mo[s]); do.append(o[s]); dh.append(max(h[s:s + 6])); dl.append(min(l[s:s + 6]))
        dc.append(c[s + 5]); dv.append(sum(v[s:s + 6]))
    d1 = T.Nen("D1", dmo, do, dh, dl, dc, dv)
    return T.BoDuLieu(h4, d1), mo


def kiem_dung_tay():
    du, mo = _du_gia_lap()
    bt = {"ten": "tay", "neo": "rau", "k": 2, "tuoi": "dai", "chon": "nhieu_cham"}
    ds = [d for d in du.duong("H4", "khang_cu_giam", 2, "rau") if d.ia == 20 and d.ib == 40]
    kiem(len(ds) == 1, "dung tay: tim ra duong khang cu 130 (nen 20) → 120 (nen 40)")
    if not ds:
        return
    d = ds[0]
    kiem(abs(d.gia(mo[60]) - 110.0) < 1e-9, "dung tay: gia duong tai nen 60 = 110")
    kiem(d.t_biet == mo[42] + 4 * 3600, "dung tay: duong chi biet khi nen 42 (40 + k) dong")
    t59 = mo[59] + 4 * 3600
    tt = [r for r in T.duong_hieu_luc(du, t59, bt, "H4", "khang_cu_giam") if r["id"] == d.id]
    kiem(bool(tt) and tt[0]["trang_thai"] == "giu", "dung tay: truoc nen 60 trang thai = giu")
    t60 = mo[60] + 4 * 3600
    tt = [r for r in T.duong_hieu_luc(du, t60, bt, "H4", "khang_cu_giam") if r["id"] == d.id]
    kiem(bool(tt) and tt[0]["trang_thai"] == "vua_pha_1n", "dung tay: nen 60 dong vuot → vua_pha_1n")
    kiem(bool(tt) and tt[0]["pha"]["vol"] is not None and abs(tt[0]["pha"]["vol"] - 3.0) < 1e-9,
         "dung tay: ti le volume nen pha = 30 / TB 20 nen truoc (10) = 3,0")
    t61 = mo[61] + 4 * 3600
    tt = [r for r in T.duong_hieu_luc(du, t61, bt, "H4", "khang_cu_giam") if r["id"] == d.id]
    kiem(bool(tt) and tt[0]["trang_thai"] == "pha_gia", "dung tay: nen 61 dong quay lai → pha_gia")
    t71 = mo[71] + 4 * 3600
    tt = [r for r in T.duong_hieu_luc(du, t71, bt, "H4", "khang_cu_giam") if r["id"] == d.id]
    kiem(bool(tt) and tt[0]["trang_thai"] == "vua_pha_2n", "dung tay: nen 70 + 71 dong vuot → vua_pha_2n")
    t73 = mo[73] + 4 * 3600
    tt = [r for r in T.duong_hieu_luc(du, t73, bt, "H4", "khang_cu_giam") if r["id"] == d.id]
    kiem(bool(tt) and tt[0]["trang_thai"] == "da_pha", "dung tay: 3 nen sau khong quay lai → da_pha")
    t74 = mo[74] + 4 * 3600
    tt = [r for r in T.duong_hieu_luc(du, t74, bt, "H4", "khang_cu_giam") if r["id"] == d.id]
    kiem(bool(tt) and tt[0]["trang_thai"] == "pha_roi_test_lai", "dung tay: rau nen 74 cham duong → pha_roi_test_lai")
    t_het = mo[70 + T.HIEU_LUC_SAU_PHA["H4"]] + 4 * 3600
    tt = [r for r in T.duong_hieu_luc(du, t_het, bt, "H4", "khang_cu_giam") if r["id"] == d.id]
    kiem(not tt, "dung tay: het hieu luc sau 12 nen H4 tu nen pha")
    # cham: 2 neo (20, 40) → it nhat 2; nen 60 bi pha (khong tinh)
    tt = [r for r in T.duong_hieu_luc(du, t59, bt, "H4", "khang_cu_giam") if r["id"] == d.id]
    kiem(bool(tt) and tt[0]["so_cham"] == 2, "dung tay: so cham truoc khi pha = 2 (2 neo)")
    # su kien khoang
    c0, sk = T.su_kien_khoang(du, bt, "H4", "khang_cu_giam", t59 - 1, t73)
    cua_d = [z for z in sk if z["id"] == d.id]
    kiem([z["ket_qua"] for z in cua_d] == ["pha_gia", "pha_that"] and cua_d[1]["hai_nen"],
         "dung tay: su kien khoang (59, 73] = pha gia roi pha that 2 nen")
    # ho tro tang 80 (nen 10) → 85 (nen 30)
    hs = [x for x in du.duong("H4", "ho_tro_tang", 2, "rau") if x.ia == 10 and x.ib == 30]
    kiem(len(hs) == 1 and abs(hs[0].m * 4 * 3600 - 0.25) < 1e-9, "dung tay: tim ra ho tro tang 80 → 85 (doc +0,25/nen)")
    # duong bi xuyen giua 2 neo: them close 129 o nen 30 → duong 130→120 khong con hop le
    du2, _ = _du_gia_lap()
    du2.nen["H4"].c[30] = 128.0
    du2.nen["H4"].h[30] = 128.5
    ds2 = [x for x in du2.duong("H4", "khang_cu_giam", 2, "rau") if x.ia == 20 and x.ib == 40]
    kiem(not ds2, "dung tay: close xuyen duong giua 2 neo → khong hop le")
    # neo than: dinh than nen 20 = max(o, c) = 101 → khong co duong 20→40 kieu than voi gia 130
    dt_ = [x for x in du.duong("H4", "khang_cu_giam", 2, "than") if x.pa == 130.0]
    kiem(not dt_, "dung tay: neo than khong dung rau 130")


def kiem_d1_sau_pha():
    """Sua sau khoa: duong D1 da pha that van duoc LIET KE toi 14 ngay (kem so ngay tu lan pha, test lai chua) nhung KHONG
    duoc chon lam duong chinh khi da pha >= 48h; het 14 ngay thi het. Kiem tren du lieu that."""
    du = T.BoDuLieu.doc()
    bt = T.bien_the("rau|3|dai|nhieu_cham")
    mau = None
    for loai in T.LOAI:
        for d in du.duong("D1", loai, 3, "rau"):
            kinds = [e[1] for e in d.ev]
            if "pha_that" in kinds and "het_han" in kinds and "that_bai" not in kinds:
                mau = d
                break
        if mau:
            break
    kiem(mau is not None, "D1 sau pha: tim duoc duong D1 pha that, het han 14 ngay, khong that bai")
    if not mau:
        return
    t_pha = next(e[0] for e in mau.ev if e[1] == "pha")
    pha_that = [e for e in mau.ev if e[1] == "pha_that"][0]
    j_pha = pha_that[2]["j_pha"]
    t_pha = du.nen["H4"].mo[j_pha] + 4 * 3600
    t_het = next(e[0] for e in mau.ev if e[1] == "het_han")
    kiem(abs((t_het - t_pha) - 14 * T.NGAY) < 1, "D1 sau pha: het han dung 14 ngay sau nen pha")
    tuoi = T.TUOI[bt["tuoi"]]["D1"]
    t3 = t_pha + 3 * T.NGAY
    if mau.xa >= t3 - tuoi:
        ds = T.duong_hieu_luc(du, t3, bt, "D1", mau.loai)
        r = [x for x in ds if x["id"] == mau.id]
        kiem(bool(r) and r[0]["trang_thai"] in ("da_pha", "pha_roi_test_lai") and abs(r[0]["da_pha_ngay"] - 3) < 1e-9
             and "đã phá cách đây 3.0 ngày" in r[0]["ghi_chu_pha"],
             "D1 sau pha: 3 ngay sau pha van liet ke, ghi 'da pha cach day 3.0 ngay, test lai chua'")
        c = T.chon_chinh(ds, bt)
        kiem(c is None or c["id"] != mau.id, "D1 sau pha: duong pha > 48h khong duoc chon lam duong chinh")
    ds = T.duong_hieu_luc(du, t_het + 1, bt, "D1", mau.loai)
    kiem(all(x["id"] != mau.id for x in ds), "D1 sau pha: qua 14 ngay thi khong con liet ke")
    # H4 van 48h
    kiem(T.HIEU_LUC_SAU_PHA["H4"] * 4 == T.VUA_PHA_GIO, "H4 sau pha: van het hieu luc sau 48h")


if __name__ == "__main__":
    kiem_dung_tay()
    kiem_d1_sau_pha()
    kiem_cat_cut()
    print("TONG:", "PASS" if not LOI else f"FAIL ({len(LOI)})")
    sys.exit(1 if LOI else 0)
