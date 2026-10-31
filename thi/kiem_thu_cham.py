#!/usr/bin/env python3
"""Kiểm thử bộ chấm + bộ dựng đề sau sửa P0 (thi/SUA_P0.md). Chạy OFFLINE: chặn mạng, thay mảng nến trong bộ nhớ
(cong_cu/dieu_kien.dat_nen, cong_cu/cham_dich.dat_5m, cham_dich.lay_1m giả), không đọc/ghi file dữ liệu.

  1. H4 mở trước C, đóng sau C qua mốc → SAI
  2. Mốc ghi D1: H4 đóng qua nhưng D1 chưa → không vô hiệu; D1 đóng qua → SAI
  3. "2 cây H4": 1 nến qua rồi nến sau quay lại → không vô hiệu; 2 nến liên tiếp → SAI
  4. Đích + SL cùng nến 5m: 1m phân được → đúng thứ tự; cùng nến 1m / thiếu 1m → CHUA_RO_THU_TU
  5. Giá tham chiếu không dùng nến chưa đóng tại C; nến 5m chứa C không được dùng để chạm đích
  6. Trạng thái mốc D1 trong đề không bị kích hoạt bởi close H4
  7. Phép thử đối xứng đối xứng thật (không nới theo chặng 1); view có chặng đi ngược được tách riêng
  8. Đường đi 2 chặng: chạm đích cuối mà không qua chặng 1 → ket_qua_duong_di ≠ DUNG
Cách dùng: python3 thi/kiem_thu_cham.py
"""
import datetime as dt, sys, urllib.request
from pathlib import Path

THI = Path(__file__).resolve().parent
sys.path[:0] = [str(THI), str(THI.parent / "cong_cu")]


def _chan_mang(*a, **k):
    raise RuntimeError("kiểm thử offline: không được gọi mạng")


urllib.request.urlopen = _chan_mang
import cham_dich as cd  # noqa: E402
import dieu_kien as dkm  # noqa: E402
import tao_ho_so as hs  # noqa: E402
import cham as ch  # noqa: E402

UTC = dt.timezone.utc
P = dt.timedelta(minutes=5)
GOC_T = dt.datetime(2030, 1, 7)  # thứ Hai, ngoài vùng dữ liệu thật


def t_(ngay, gio, phut=0):
    return dt.datetime(2030, 1, ngay, gio, phut)


def nen5(gia=60000, gio=96, sua=None):
    """Nến 5m phẳng (h = gia+50, l = gia−50) từ GOC_T trong `gio` giờ; sua = {giờ mở: (h, l, c)}."""
    ds, t = [], GOC_T
    while t < GOC_T + dt.timedelta(hours=gio):
        ds.append((t, *(sua or {}).get(t, (gia + 50, gia - 50, gia))))
        t += P
    return ds


def nen_khung(do_dai, so, gia=60000, sua=None, mui=None):
    """Nến khung (H4/D1) từ GOC_T: close = gia, trừ sua = {giờ mở: close}."""
    ds = []
    for i in range(so):
        mo = GOC_T + do_dai * i
        c = (sua or {}).get(mo, gia)
        mo2 = mo.replace(tzinfo=mui) if mui else mo
        ds.append(dkm.Nen(mo2, mo2 + do_dai, gia, max(gia, c) + 50, min(gia, c) - 50, c))
    return ds


def dat(h4=None, d1=None, m5=None):
    dkm.dat_nen("H4", h4 if h4 is not None else nen_khung(dt.timedelta(hours=4), 24))
    dkm.dat_nen("D1", d1 if d1 is not None else nen_khung(dt.timedelta(days=1), 4))
    cd.dat_5m(m5 if m5 is not None else nen5())


def phieu(huong, dich, vo_hieu=None, sl=None, duong_di=None, han_gio=None):
    d = {"nhan_dinh": [{"khung": "H4", "huong": huong, "dich": dich, "vo_hieu_khi": vo_hieu, "duong_di": duong_di,
                        "han_gio": han_gio}], "lenh": []}
    if sl:
        d["lenh"].append({"chieu": "SHORT" if huong == "GIAM" else "LONG", "sl": sl, "trang_thai": "de_xuat_moi"})
    return d


# ───────────────────────── các phép thử ─────────────────────────
def kt1_h4_mo_truoc_C_dong_sau_C():
    C = t_(7, 10, 30)
    dat(h4=nen_khung(dt.timedelta(hours=4), 24, sua={t_(7, 8): 62500}))  # H4 08:00–12:00 UTC: mở trước C, đóng sau C
    r = cd.cham_chi_tiet(phieu("GIAM", 55000, "H4 đóng trên 62.000"), C, 48)
    assert r["dieu_kien"]["khung"] == "H4" and r["dieu_kien"]["so_nen"] == 1, r["dieu_kien"]
    assert r["ket_qua"] == "SAI" and r["su_kien"] == "vo_hieu", r["ket_qua"]
    assert r["luc"] == "07/01 19:00", r["luc"]  # giờ ĐÓNG 12:00 UTC = 19:00 VN
    assert dkm.lan_kich_hoat(r["dieu_kien"], C, C + dt.timedelta(hours=48)) == t_(7, 12)


def kt2_moc_D1():
    C = t_(7, 10, 30)
    h4 = nen_khung(dt.timedelta(hours=4), 24, sua={t_(7, 8): 62500})  # H4 đóng qua 62K lúc 12:00
    d1 = nen_khung(dt.timedelta(days=1), 4, sua={t_(7, 0): 61000, t_(8, 0): 62500})  # D1 ngày 7 chưa qua, ngày 8 qua
    dat(h4=h4, d1=d1)
    d = phieu("GIAM", 55000, "nến ngày đóng trên 62.000")
    r = cd.cham_chi_tiet(d, C, 30)  # hạn tới 08/01 16:30 UTC: chỉ có D1 ngày 7 đóng (61.000)
    assert r["dieu_kien"]["khung"] == "D1", r["dieu_kien"]
    assert r["ket_qua"] == "CHUA_RO", (r["ket_qua"], "H4 đóng qua không được làm vô hiệu mốc D1")
    r = cd.cham_chi_tiet(d, C, 72)
    assert r["ket_qua"] == "SAI" and r["su_kien"] == "vo_hieu" and r["luc"] == "09/01 07:00", (r["ket_qua"], r["luc"])


def kt3_hai_nen_H4():
    C = t_(7, 10, 30)
    h4 = nen_khung(dt.timedelta(hours=4), 24, sua={t_(7, 8): 62500, t_(7, 12): 61000, t_(7, 16): 62500, t_(7, 20): 62600})
    dat(h4=h4)
    d = phieu("GIAM", 55000, "2 cây H4 đóng trên 62.000 thì sai")
    r = cd.cham_chi_tiet(d, C, 12)  # tới 22:30: nến đóng 12:00 qua, 16:00 quay lại, 20:00 qua → chưa có 2 nến liên tiếp
    assert r["dieu_kien"]["so_nen"] == 2, r["dieu_kien"]
    assert r["ket_qua"] == "CHUA_RO", r["ket_qua"]
    r = cd.cham_chi_tiet(d, C, 48)  # nến đóng 20:00 và 00:00 cùng qua → SAI lúc 00:00 UTC
    assert r["ket_qua"] == "SAI" and r["luc"] == "08/01 07:00", (r["ket_qua"], r["luc"])
    assert dkm.phan_tich("H4 đóng trên 85.000 (1-2 cây)", "GIAM", 80000)["so_nen"] == 1


def kt4_dich_sl_cung_nen_5m():
    C = t_(7, 10, 30)
    t5 = t_(7, 12)
    dat(m5=nen5(sua={t5: (61100, 58900, 60000)}))  # cùng nến 5m chạm đích 59K và SL 61K
    d = phieu("GIAM", 59000, sl=61000)
    m1 = lambda *x: [(t5 + dt.timedelta(minutes=i), *x[i], 60000) for i in range(5)]
    cd.lay_1m = lambda t: m1((60100, 58900), (60100, 59900), (60100, 59900), (61100, 59900), (60100, 59900))
    r = cd.cham_chi_tiet(d, C, 48)
    assert r["ket_qua"] == "DUNG" and r["su_kien"] == "dich (1m)", r["ket_qua"]
    cd.lay_1m = lambda t: m1((60100, 59900), (61100, 59900), (60100, 58900), (60100, 59900), (60100, 59900))
    assert cd.cham_chi_tiet(d, C, 48)["ket_qua"] == "SAI"
    cd.lay_1m = lambda t: m1((60100, 59900), (61100, 58900), (60100, 59900), (60100, 59900), (60100, 59900))
    assert cd.cham_chi_tiet(d, C, 48)["ket_qua"] == "CHUA_RO_THU_TU"
    cd.lay_1m = lambda t: []  # thiếu 1m → vẫn không mặc định ĐÚNG
    assert cd.cham_chi_tiet(d, C, 48)["ket_qua"] == "CHUA_RO_THU_TU"


def kt5_gia_tham_chieu_va_nen_chua_C():
    sua = {t_(7, 10, 25): (60050, 59950, 60000), t_(7, 10, 30): (64000, 58000, 64000)}  # nến 10:30–10:35 chứa C
    dat(m5=nen5(sua=sua))
    d = phieu("GIAM", 59000)
    C = t_(7, 10, 32)
    r = cd.cham_chi_tiet(d, C, 24)
    assert r["gia_tham_chieu"] == 60000 and r["gio_gia"] == t_(7, 10, 30), (r["gia_tham_chieu"], r["gio_gia"])
    assert r["ket_qua"] == "SAI_HET_HAN", r["ket_qua"]  # râu 58.000 của nến chứa C không được tính chạm đích
    r = cd.cham_chi_tiet(d, t_(7, 10, 30), 24)  # C đúng biên nến: nến 10:30 mở ≥ C → được tính
    assert r["gia_tham_chieu"] == 60000 and r["ket_qua"] == "DUNG", r["ket_qua"]


def kt6_trang_thai_moc_D1_trong_de():
    mo = dt.datetime(2030, 1, 7, tzinfo=UTC)
    tu, T = mo + dt.timedelta(hours=2), mo + dt.timedelta(days=2, hours=12)
    h4 = nen_khung(dt.timedelta(hours=4), 15, 62400, sua={GOC_T + dt.timedelta(hours=8): 61699}, mui=UTC)  # 1 close H4 thủng 62K
    d1_giu = nen_khung(dt.timedelta(days=1), 2, 62400, sua={GOC_T + dt.timedelta(days=1): 62300}, mui=UTC)  # D1 không thủng
    d1_pha = nen_khung(dt.timedelta(days=1), 2, 62400, sua={GOC_T + dt.timedelta(days=1): 61500}, mui=UTC)  # D1 ngày 2 thủng
    m = {"gia": 62000, "gia_tren": None, "vai_tro": "vo_hieu", "huong": "TANG", "khung": "D1"}
    nen = lambda d1: {"H4": h4, "D1": d1, "W1": [], "MN": []}
    s = hs.trang_thai_moc(m, nen(d1_giu), tu, T, 63000, 62400)
    assert s.startswith("chưa kích hoạt"), s
    s = hs.trang_thai_moc(m, nen(d1_pha), tu, T, 63000, 62400)
    assert s.startswith("ĐÃ KÍCH HOẠT (đóng D1 thấp nhất 61.500)"), s
    s = hs.trang_thai_moc(dict(m, khung="H4"), nen(d1_giu), tu, T, 63000, 62400)  # mốc H4 vẫn xét H4 như cũ
    assert s.startswith("ĐÃ KÍCH HOẠT (đóng H4 thấp nhất 61.699)"), s
    s = hs.trang_thai_moc(dict(m, vai_tro="ho_tro"), nen(d1_giu), tu, T, 63000, 62400)
    assert s.startswith("giữ"), s
    d1_sau_T = d1_giu + [dkm.Nen(mo + dt.timedelta(days=2), mo + dt.timedelta(days=3), 62000, 62100, 61000, 61000)]
    s = hs.trang_thai_moc(m, nen(d1_sau_T), tu, T, 63000, 62400)  # D1 đóng SAU T không được dùng
    assert s.startswith("chưa kích hoạt"), s


def kt7_doi_xung_that():
    C = t_(7, 10, 30)
    # giá 60.000, đích 59.000 (cách 1.000) → biên phía kia đúng 61.000; chặng 1 hồi tới 61.500 (bản cũ nới biên tới đây)
    sua = {t_(7, 12): (61200, 59950, 61000), t_(7, 14): (60050, 58900, 59000)}
    dat(m5=nen5(sua=sua))
    d = phieu("GIAM", 59000, duong_di=[{"huong": "TANG", "dich": 61500}, {"huong": "GIAM", "dich": 59000}])
    ct = ch.cham_thi_truong(d, C)
    assert ct["di_nguoc"] is True  # có chặng cố ý đi ngược → bảng riêng, không vào phép thử chính
    assert ch.doi_xung(ct) == "THUA", ch.doi_xung(ct)  # 61.200 chạm biên đối xứng 61.000 trước khi tới 59.000
    dat(m5=nen5(sua={t_(7, 12): (60999, 59950, 60500), t_(7, 14): (60050, 58900, 59000)}))
    ct = ch.cham_thi_truong(phieu("GIAM", 59000), C)
    assert ct["di_nguoc"] is False and ch.doi_xung(ct) == "THANG"  # 60.999 chưa chạm biên 61.000
    dat(m5=nen5(sua={t_(7, 12): (61000, 59950, 60500), t_(7, 14): (60050, 58900, 59000)}))
    assert ch.doi_xung(ch.cham_thi_truong(phieu("TANG", 61000), C)) == "THANG"
    assert ch.doi_xung(ch.cham_thi_truong(phieu("GIAM", 59000), C)) == "THUA"  # biên 61.000 cách đúng 1.000


def kt8_duong_di_hai_chang():
    C = t_(7, 10, 30)
    dd = [{"huong": "TANG", "dich": 61000}, {"huong": "GIAM", "dich": 58000}]
    d = phieu("GIAM", 58000, duong_di=dd)
    dat(m5=nen5(sua={t_(7, 12): (60050, 57900, 58000)}))  # đi thẳng xuống đích cuối, không hồi lên 61.000
    r = cd.cham_chi_tiet(d, C, 48)
    assert r["ket_qua"] == "DUNG", r["ket_qua"]  # kết quả chính (đích cuối) vẫn ĐÚNG
    assert r["ket_qua_duong_di"] not in ("DUNG",) and r["ket_qua_duong_di"] == "SAI_THU_TU", r["ket_qua_duong_di"]
    dat(m5=nen5(sua={t_(7, 11): (61050, 59950, 61000), t_(7, 12): (60050, 57900, 58000)}))  # hồi 61.000 rồi mới giảm
    assert cd.cham_chi_tiet(d, C, 48)["ket_qua_duong_di"] == "DUNG"


def main():
    goc_lay_1m = cd.lay_1m
    ds = [kt1_h4_mo_truoc_C_dong_sau_C, kt2_moc_D1, kt3_hai_nen_H4, kt4_dich_sl_cung_nen_5m, kt5_gia_tham_chieu_va_nen_chua_C,
          kt6_trang_thai_moc_D1_trong_de, kt7_doi_xung_that, kt8_duong_di_hai_chang]
    qua = 0
    for f in ds:
        cd.lay_1m = lambda t: []
        try:
            f(); qua += 1; print(f"PASS  {f.__name__}")
        except AssertionError as e:
            print(f"FAIL  {f.__name__}: {e!r}")
        finally:
            cd.lay_1m = goc_lay_1m
    print(f"{qua}/{len(ds)} PASS")
    sys.exit(0 if qua == len(ds) else 1)


if __name__ == "__main__":
    main()
