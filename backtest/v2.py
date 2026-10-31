#!/usr/bin/env python3
"""BOT V2 — luật cơ học v1 (`chay.py`) + ĐÚNG 5 thay đổi chốt trước, 6 tài sản (BTC ETH OKB BNB VÀNG DẦU).

Chạy lại toàn bộ:  python3 backtest/v2.py
  → KET_QUA_V2.md (giữ nguyên khối Diễn giải + Nhận xét viết tay), lenh_v1_<kỳ>.csv, lenh_v2_<kỳ>.csv, tu_kiem_v2.txt
Kỳ: 2025 (ngoài mẫu, du_lieu_2025/) và 2026-01-01→2026-10-30 (trong mẫu, du_lieu/).

Bộ máy `buoc()` xử lý MỘT mốc đóng nến H4 trên trạng thái JSON được → dùng chung cho lệnh giấy (giay/chay_giay.py).
Với CO_V1 (tắt hết thay đổi) bộ máy cho ra đúng từng lệnh của chay.mo_phong — có kiểm trong tu_kiem_v2.txt.
Không sửa chay.py; chỉ gọi lại hàm của nó.
"""
import bisect, csv, datetime as dt, random, sys
from collections import Counter, defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parent
sys.path.insert(0, str(GOC))
import chay as C  # noqa: E402

# ---------------- THAM SỐ (chốt trước — xem mục Diễn giải) ----------------
TAI_SAN = ["BTC", "ETH", "OKB", "BNB", "VANG", "DAU"]
VON0 = 4000.0
RUI_RO = 0.02
TOI_DA = 4
DI_NGANG_NEN, DI_NGANG_CAT = 30, 6          # thay đổi 1
NEN_LON_NEN, NEN_LON_ATR, ATR_N = 6, 2.5, 14  # thay đổi 2
FIB_VAO = 0.5                                # thay đổi 2: lấy 0.5
SL_KHAN = 2.0                                # thay đổi 4: chặn khẩn cấp 2× khoảng SL
FIB_TP1, FIB_TP2 = 1.0, 1.618                # thay đổi 5
VANG_GIU = 6                                 # vàng: hết hạn 6 nến, TP1 đóng 100%
KY = {
    "2025": dict(tu="2025-01-01", den="2025-12-31", du_lieu=GOC / "du_lieu_2025", nhan="2025 (ngoài mẫu)"),
    "2026": dict(tu="2026-01-01", den="2026-10-30", du_lieu=GOC / "du_lieu", nhan="2026 (trong mẫu)"),
}
CO_V1 = dict(di_ngang=False, nen_lon=False, pha_moc=False, sl_dong=False, tp_fibo=False, vang_scalp=False)
CO_V2 = {k: True for k in CO_V1}
TEN_CO = {"di_ngang": "1. Đứng ngoài khi đi ngang", "nen_lon": "2. Sau nến lớn → Fibo 0.5",
          "pha_moc": "3. Phá mốc rồi test lại", "sl_dong": "4. SL theo nến đóng (+ chặn 2×)",
          "tp_fibo": "5. TP Fibo mở rộng 1 / 1.618", "vang_scalp": "Vàng: chỉ TP1, 6 nến"}
TEN_KIEU = {"ema34": "Hồi về EMA34 (v1)", "pha_moc": "Phá mốc → test lại", "nen_lon": "Sau nến lớn → Fibo 0.5"}


class Ob(dict):
    """dict dùng được như object (p.lai) và ghi thẳng ra JSON."""
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        self[k] = v


# ---------------- DỮ LIỆU ----------------
def bo_sung(a):
    """Thêm ATR14 Wilder và dấu cắt EMA89 cho một C.TaiSan (đều nhân quả)."""
    n = len(a.c)
    tr = [a.h[0] - a.l[0]] + [max(a.h[i] - a.l[i], abs(a.h[i] - a.c[i - 1]), abs(a.l[i] - a.c[i - 1])) for i in range(1, n)]
    atr = [None] * n
    if n >= ATR_N:
        v = sum(tr[:ATR_N]) / ATR_N
        atr[ATR_N - 1] = v
        for i in range(ATR_N, n):
            v = (v * (ATR_N - 1) + tr[i]) / ATR_N
            atr[i] = v
    a.atr = atr
    cat = [0] * n
    for i in range(1, n):
        if a.e89[i] is not None and a.e89[i - 1] is not None:
            cat[i] = int((a.c[i] >= a.e89[i]) != (a.c[i - 1] >= a.e89[i - 1]))
    a.cat89 = cat
    return a


def nap(ma, thu_muc):
    thu_muc = Path(thu_muc)
    return bo_sung(C.TaiSan(ma, C.doc_csv(thu_muc / f"{ma}_4H.csv"), C.doc_csv(thu_muc / f"{ma}_1D.csv")))


def cat_cut(a, t, thu_muc):
    """Dựng lại tài sản chỉ với dữ liệu tới hết nến t (D1 đã đóng tới lúc đó)."""
    h4 = [(a.mo[i], a.dong[i], a.o[i], a.h[i], a.l[i], a.c[i]) for i in range(t + 1)]
    d1 = [r for r in C.doc_csv(Path(thu_muc) / f"{a.ma}_1D.csv") if r[1] <= a.dong[t]]
    return bo_sung(C.TaiSan(a.ma, h4, d1))


# ---------------- LUẬT ----------------
def nhip_v1(a, t, x):
    """Nhịp như v1: điểm xoay đã xác nhận gần nhất ngược chiều lệnh (60 ngày) → cực trị râu sau nó tới nến t."""
    dau = a.xoay("dinh" if x < 0 else "day", t, C.NGAY_XOAY)
    if not dau:
        return None
    i0, p0 = dau[-1]
    cuoi = min(a.l[i0 + 1:t + 1]) if x < 0 else max(a.h[i0 + 1:t + 1])
    return (i0, p0, cuoi)


def tim_nen_lon(a, t, x):
    """Thay đổi 2: nến gần nhất trong t−5..t có thân ≥ 2,5×ATR14(nến trước) cùng chiều xu hướng."""
    for i in range(t, t - NEN_LON_NEN, -1):
        if i < 1 or a.atr[i - 1] is None:
            continue
        than = a.c[i] - a.o[i]
        if than * x > 0 and abs(than) >= NEN_LON_ATR * a.atr[i - 1]:
            return i
    return None


def tim_pha_moc(a, t, x):
    """Thay đổi 3: mốc fractal 30 ngày vừa bị 2 nến liên tiếp đóng qua (hoàn tất đúng ở nến t)."""
    if t < 2:
        return None
    if x < 0:
        ds = [(i, p) for i, p in a.xoay("day", t, C.NGAY_CC) if a.c[t] < p and a.c[t - 1] < p and a.c[t - 2] >= p]
        return min(ds, key=lambda e: (e[1], -e[0])) if ds else None
    ds = [(i, p) for i, p in a.xoay("dinh", t, C.NGAY_CC) if a.c[t] > p and a.c[t - 1] > p and a.c[t - 2] <= p]
    return max(ds, key=lambda e: (e[1], e[0])) if ds else None


def danh_gia(a, t, x, kieu, vao, nhip, moc, co):
    """Luật 7→9 cho một kiểu vào. Trả (lý do, lệnh chờ | None)."""
    lo, hi = vao * (1 - C.HOI_TU), vao * (1 + C.HOI_TU)
    cc = ["MocDoiVai"] if kieu == "pha_moc" else (["Fibo0.5nhip"] if kieu == "nen_lon" else [])
    n_goc = len(cc)
    if kieu != "ema34":
        mep = a.e34l[t] if x < 0 else a.e34h[t]
        if lo <= mep <= hi: cc.append("EMA34")
    if lo <= a.e89[t] <= hi: cc.append("EMA89")
    if lo <= a.e200[t] <= hi: cc.append("EMA200")
    bo_moc = ("day" if x < 0 else "dinh", moc[0]) if moc else None
    gan = [(i, p) for loai in ("dinh", "day") for i, p in a.xoay(loai, t, C.NGAY_CC) if lo <= p <= hi and (loai, i) != bo_moc]
    if gan:
        cc.append("Fractal")
    if kieu != "nen_lon" and nhip:
        i0, p0, cuoi = nhip
        for r in (0.5, 0.618):
            if lo <= cuoi + r * (p0 - cuoi) <= hi:
                cc.append(f"Fibo{r}")
    if len(cc) == n_goc:
        return "khong_hoi_tu", None
    d = C.D_MIN[a.ma]                                             # luật 8 (như v1)
    if x < 0:
        tren = [(i, p) for i, p in a.xoay("dinh", t, C.NGAY_XOAY) if p > vao]
        if C.DIEN_GIAI == "gia":
            nguon = min(tren, key=lambda e: (e[1], -e[0])) if tren else None
        else:
            nguon = max(tren, key=lambda e: e[0]) if tren else None
        goc = max(nguon[1], vao * (1 + d)) if nguon else vao * (1 + d)
        sl = goc * (1 + C.SL_DEM)
    else:
        duoi = [(i, p) for i, p in a.xoay("day", t, C.NGAY_XOAY) if p < vao]
        if C.DIEN_GIAI == "gia":
            nguon = max(duoi, key=lambda e: (e[1], e[0])) if duoi else None
        else:
            nguon = max(duoi, key=lambda e: e[0]) if duoi else None
        goc = min(nguon[1], vao * (1 - d)) if nguon else vao * (1 - d)
        sl = goc * (1 - C.SL_DEM)
    sl_nguon = "fractal" if nguon and goc == nguon[1] else "san_dmin"
    sl_pct = abs(sl - vao) / vao
    if sl_pct > C.SL_TOI_DA:
        return "sl_qua_xa", None
    tp1_xoay = None
    if co["tp_fibo"]:                                             # thay đổi 5
        if not nhip:
            return "khong_co_dich", None
        i0, p0, cuoi = nhip
        if (cuoi - p0) * x <= 0:
            return "khong_co_dich", None
        lui = (1 + C.TP_LUI) if x < 0 else (1 - C.TP_LUI)
        tp1 = (vao + FIB_TP1 * (cuoi - p0)) * lui
        tp2 = (vao + FIB_TP2 * (cuoi - p0)) * lui
        tp2_nguon = "Fibo1.618"
        if (tp1 >= a.c[t]) if x < 0 else (tp1 <= a.c[t]):
            return "khong_co_dich", None
    else:                                                         # luật 9 v1
        if x < 0:
            ung = sorted({p for i, p in a.xoay("day", t, C.NGAY_XOAY) if p < a.c[t]}, reverse=True)
        else:
            ung = sorted({p for i, p in a.xoay("dinh", t, C.NGAY_XOAY) if p > a.c[t]})
        if not ung:
            return "khong_co_dich", None
        tp1 = ung[0] * (1 + C.TP_LUI) if x < 0 else ung[0] * (1 - C.TP_LUI)
        tp1_xoay = ung[0]
        if len(ung) > 1:
            tp2 = ung[1] * (1 + C.TP_LUI) if x < 0 else ung[1] * (1 - C.TP_LUI)
            tp2_nguon = "xoay_ke_tiep"
        else:
            tp2 = vao + x * 3 * abs(sl - vao)
            tp2_nguon = "3R"
            if (tp2 - tp1) * x <= 0:
                tp2, tp2_nguon = tp1, "=TP1"
    vang = co["vang_scalp"] and a.ma == "VANG"
    if vang:
        tp2, tp2_nguon = tp1, "=TP1(vàng)"
    rr = abs(tp1 - vao) / abs(sl - vao)
    if rr < C.RR_MIN:
        return "rr_thap", None
    return "dat_lenh", Ob(ma=a.ma, chieu=x, t=t, vao=vao, sl=sl, sl_pct=sl_pct, tp1=tp1, tp2=tp2, rr=rr, cc=cc,
                          sl_nguon=sl_nguon, tp2_nguon=tp2_nguon, sl_xoay=(nguon[0], nguon[1]) if nguon else None,
                          tp1_xoay=tp1_xoay, fib=nhip, kieu=kieu, moc=moc,
                          het_han=VANG_GIU if vang else C.NEN_GIU, sl_dong=co["sl_dong"])


def quyet_dinh_v2(a, t, co):
    """Quyết định lúc nến H4 t đóng. Trả (lý do, lệnh chờ | None, info). Chỉ đọc dữ liệu tới nến t."""
    info = {}
    x = a.xu[t]
    if x == 0 or t < 1 or a.xu[t - 1] != x:
        return "khong_tin_hieu", None, info                       # luật 1 + 2
    k = a.d1i[t]                                                  # luật 3
    if k < 0 or a.d_e34h[k] is None:
        return "loc_d1", None, info
    if x < 0 and not a.d_c[k] < a.d_e34h[k]:
        return "loc_d1", None, info
    if x > 0 and not a.d_c[k] > a.d_e34l[k]:
        return "loc_d1", None, info
    if co["di_ngang"]:                                            # thay đổi 1
        n_cat = sum(a.cat89[max(1, t - DI_NGANG_NEN + 2):t + 1])
        info["cat89"] = n_cat
        if n_cat >= DI_NGANG_CAT:
            return "di_ngang", None, info
    bo = (a.e34c[t], a.e89[t], a.e200[t])                          # luật 4
    if (max(bo) - min(bo)) / a.c[t] < C.EMA_CHUM:
        return "ema_chum", None, info
    if C.thu_hai(a.dong[t]):                                      # luật 5
        return "thu_hai", None, info
    ung_vien = []
    i_lon = tim_nen_lon(a, t, x) if co["nen_lon"] else None       # thay đổi 2
    if i_lon is not None:
        info["nen_lon"] = i_lon
        dau = [(i, p) for i, p in a.xoay("dinh" if x < 0 else "day", t, C.NGAY_XOAY) if i <= i_lon]
        if not dau:
            return "khong_nhip", None, info
        i0, p0 = dau[-1]
        cuoi = min(a.l[i0:t + 1]) if x < 0 else max(a.h[i0:t + 1])
        vao = cuoi + FIB_VAO * (p0 - cuoi)
        if (vao <= a.c[t]) if x < 0 else (vao >= a.c[t]):
            return "fibo_da_qua", None, info
        ung_vien.append(("nen_lon", vao, (i0, p0, cuoi), None))
    else:
        nhip = nhip_v1(a, t, x)
        ung_vien.append(("ema34", a.e34l[t] if x < 0 else a.e34h[t], nhip, None))   # luật 6 v1
        if co["pha_moc"]:                                         # thay đổi 3
            moc = tim_pha_moc(a, t, x)
            if moc:
                ung_vien.append(("pha_moc", moc[1], nhip, moc))
    kq = [danh_gia(a, t, x, kieu, vao, nhip, moc, co) for kieu, vao, nhip, moc in ung_vien]
    if len(ung_vien) > 1:
        info["pha_moc"] = kq[1][0]
    dat = [q for _, q in kq if q]
    if not dat:
        return kq[0][0], None, info
    q = min(dat, key=lambda q: abs(q.vao - a.c[t]))
    return "dat_lenh", q, info


# ---------------- BỘ MÁY MÔ PHỎNG (một mốc nến) ----------------
def tt_moi(von0=VON0):
    return dict(so_du=von0, vithe={}, cho={}, lenh=[], pheu={}, huy={}, pha_moc={}, von=[], nen_cuoi=None)


def _dem(d, k, n=1):
    d[k] = d.get(k, 0) + n


def _thoat(p, ti_le, gia, ts, tt, ghi, ly_do):
    q = p.kl * ti_le
    lai = q * (gia - p.gia_khop) * p.chieu
    phi = q * gia * C.PHI_RA
    p.con -= ti_le
    p.lai += lai - phi
    p.phi += phi
    tt["so_du"] += lai - phi
    p.dong_ts = ts
    if ghi:
        ghi(dict(ts=ts, su_kien="THOAT", ma=p.ma, chieu=p.chieu, gia=gia, ti_le=ti_le, lai=lai - phi, ly_do=ly_do,
                 so_du=tt["so_du"]))


def xu_ly(p, a, k, tt, nen_khop=False, ghi=None):
    """Diễn biến trong nến k của vị thế p. Trả True nếu đã đóng hết."""
    o, h, l, c, x, ts = a.o[k], a.h[k], a.l[k], a.c[k], p.chieu, a.dong[k]
    if not p.sl_dong:                                             # v1: SL theo giá (chay.xu_ly_nen)
        if C.cham(p.sl, x, h, l, True):
            kq = "SL" if not p.tp1_xong else "HV"
            _thoat(p, p.con, C.gia_thoat(p.sl, x, o, True), ts, tt, ghi, kq)
            p.kq += kq
            return True
        if nen_khop:
            return False
        if not p.tp1_xong and C.cham(p.tp1, x, h, l, False):
            if p.tp2 == p.tp1:
                _thoat(p, p.con, C.gia_thoat(p.tp1, x, o, False), ts, tt, ghi, "TP1(hết)")
                p.kq += "TP1(hết)"
                return True
            _thoat(p, 0.5, C.gia_thoat(p.tp1, x, o, False), ts, tt, ghi, "TP1")
            p.tp1_xong, p.sl, p.kq = True, p.vao, "TP1+"
            if C.cham(p.sl, x, h, l, True):
                _thoat(p, p.con, p.sl, ts, tt, ghi, "HV")
                p.kq += "HV"
                return True
        if p.tp1_xong and C.cham(p.tp2, x, h, l, False):
            _thoat(p, p.con, C.gia_thoat(p.tp2, x, o, False), ts, tt, ghi, "TP2")
            p.kq += "TP2"
            return True
        return False
    # v2: SL theo nến đóng + chặn khẩn cấp theo giá
    if C.cham(p.sl_kc, x, h, l, True):
        kq = "khẩn" if p.tp1_xong else "SL(khẩn)"
        _thoat(p, p.con, C.gia_thoat(p.sl_kc, x, o, True), ts, tt, ghi, kq)
        p.kq += kq
        return True
    if not nen_khop:
        if not p.tp1_xong and C.cham(p.tp1, x, h, l, False):
            if p.tp2 == p.tp1:
                _thoat(p, p.con, C.gia_thoat(p.tp1, x, o, False), ts, tt, ghi, "TP1(hết)")
                p.kq += "TP1(hết)"
                return True
            _thoat(p, 0.5, C.gia_thoat(p.tp1, x, o, False), ts, tt, ghi, "TP1")
            p.tp1_xong, p.sl, p.sl_kc, p.kq = True, p.vao, p.sl0, "TP1+"
            if C.cham(p.sl_kc, x, h, l, True):                    # cùng nến chạm chặn mới → coi như chạm sau (bảo thủ)
                _thoat(p, p.con, p.sl_kc, ts, tt, ghi, "khẩn")
                p.kq += "khẩn"
                return True
        if p.tp1_xong and C.cham(p.tp2, x, h, l, False):
            _thoat(p, p.con, C.gia_thoat(p.tp2, x, o, False), ts, tt, ghi, "TP2")
            p.kq += "TP2"
            return True
    if (c > p.sl) if x < 0 else (c < p.sl):                       # nến ĐÓNG qua SL → thoát ở giá đóng
        kq = "HV(đóng)" if p.tp1_xong else "SL(đóng)"
        _thoat(p, p.con, c, ts, tt, ghi, kq)
        p.kq += kq
        return True
    return False


def _so_nen(a, ts_dau, k):
    """Số nến từ nến đóng lúc ts_dau tới nến k (= k − chỉ số nến ts_dau)."""
    return k - bisect.bisect_left(a.dong, ts_dau)


def buoc(tt, T, TS, ds_ma, co, toi_da=TOI_DA, rui_ro=RUI_RO, ghi=None, quyet=None):
    """Xử lý một mốc đóng nến H4 T (UTC ts) cho mọi tài sản có nến tại T — đúng thứ tự của chay.mo_phong.
    Trả {mã: (lý do, lệnh chờ | None, info)} của bước tín hiệu mới (chỉ tài sản được xét)."""
    vithe, cho, pheu, huy = tt["vithe"], tt["cho"], tt["pheu"], tt["huy"]
    nen = [(TS[m], TS[m].chi_so[T]) for m in ds_ma if T in TS[m].chi_so]
    # 1) vị thế đang mở
    for a, k in nen:
        p = vithe.get(a.ma)
        if p and xu_ly(p, a, k, tt, ghi=ghi):
            tt["lenh"].append(p); del vithe[a.ma]
    # 2) lệnh chờ: khớp hay hủy vì chạm TP1 trước
    for a, k in nen:
        q = cho.get(a.ma)
        if not q:
            continue
        x = q.chieu
        toi_vao = a.h[k] >= q.vao if x < 0 else a.l[k] <= q.vao
        if toi_vao and not C.thu_hai(T):
            del cho[a.ma]
            if len(vithe) >= toi_da:
                _dem(huy, "du_lenh_mo")
                if ghi: ghi(dict(ts=T, su_kien="HUY", ma=a.ma, chieu=x, gia=q.vao, ly_do="đủ lệnh mở"))
                continue
            rr_usd = rui_ro * tt["so_du"]
            gtvt = rr_usd / q.sl_pct
            bay = min(C.BAY_MAX, C.BAY_CHIA / q.sl_pct)
            kha_dung = tt["so_du"] - sum(v.ky_quy for v in vithe.values())
            if gtvt / bay > kha_dung:
                if kha_dung <= 0:
                    _dem(huy, "het_ky_quy")
                    if ghi: ghi(dict(ts=T, su_kien="HUY", ma=a.ma, chieu=x, gia=q.vao, ly_do="hết ký quỹ"))
                    continue
                gtvt = kha_dung * bay; rr_usd = gtvt * q.sl_pct; _dem(huy, "giam_kl_ky_quy")
            p = Ob(q)
            p.gia_khop = C.gia_thoat(q.vao, x, a.o[k], True)
            p.k_khop, p.khop_ts, p.sl0 = k, T, q.sl
            p.sl_kc = q.vao + SL_KHAN * (q.sl - q.vao)
            p.kl = gtvt / p.gia_khop; p.gtvt = gtvt; p.bay = bay; p.ky_quy = gtvt / bay; p.rui_ro_usd = rr_usd
            p.con, p.lai, p.phi, p.tp1_xong, p.kq = 1.0, 0.0, 0.0, False, ""
            phi = gtvt * C.PHI_VAO
            tt["so_du"] -= phi; p.lai -= phi; p.phi += phi
            vithe[a.ma] = p
            if ghi: ghi(dict(ts=T, su_kien="KHOP", ma=a.ma, chieu=x, gia=p.gia_khop, gtvt=gtvt, bay=bay, rui_ro=rr_usd,
                             sl=p.sl, sl_kc=p.sl_kc if p.sl_dong else None, tp1=p.tp1, tp2=p.tp2, so_du=tt["so_du"]))
            if xu_ly(p, a, k, tt, nen_khop=True, ghi=ghi):
                tt["lenh"].append(p); del vithe[a.ma]
        elif (a.l[k] <= q.tp1) if x < 0 else (a.h[k] >= q.tp1):
            del cho[a.ma]; _dem(huy, "cham_tp1_truoc")
            if ghi: ghi(dict(ts=T, su_kien="HUY", ma=a.ma, chieu=x, gia=q.vao, ly_do="giá chạm TP1 trước khi khớp"))
    # 3) đóng nến: hết hạn vị thế, hủy lệnh chờ
    for a, k in nen:
        p = vithe.get(a.ma)
        if p and _so_nen(a, p.khop_ts, k) >= p.het_han:
            _thoat(p, p.con, a.c[k], T, tt, ghi, "Hết hạn"); p.kq += "Hết hạn"
            tt["lenh"].append(p); del vithe[a.ma]
        q = cho.get(a.ma)
        if q:
            if a.xu[k] != q.chieu:
                del cho[a.ma]; _dem(huy, "mat_xu_huong")
                if ghi: ghi(dict(ts=T, su_kien="HUY", ma=a.ma, chieu=q.chieu, gia=q.vao, ly_do="mất xu hướng"))
            elif _so_nen(a, q.tin_hieu_ts, k) >= C.NEN_CHO:
                del cho[a.ma]; _dem(huy, "het_han_cho")
                if ghi: ghi(dict(ts=T, su_kien="HUY", ma=a.ma, chieu=q.chieu, gia=q.vao, ly_do="hết 6 nến chưa khớp"))
    # 4) tín hiệu mới
    ra = {}
    for a, k in nen:
        if a.ma in vithe or a.ma in cho:
            ra[a.ma] = ("dang_co_lenh", None, {})
            continue
        ly_do, q, info = (quyet or quyet_dinh_v2)(a, k, co)
        ra[a.ma] = (ly_do, q, info)
        _dem(pheu, ly_do)
        if "pha_moc" in info:
            _dem(tt["pha_moc"], "su_kien")
            _dem(tt["pha_moc"], "dat" if q is not None and q.kieu == "pha_moc" else info["pha_moc"])
        if q:
            q.tin_hieu_ts = T
            cho[a.ma] = q
            if ghi: ghi(dict(ts=T, su_kien="DAT", ma=a.ma, chieu=q.chieu, gia=q.vao, sl=q.sl, tp1=q.tp1, tp2=q.tp2,
                             rr=q.rr, kieu=q.kieu, can_cu="+".join(q.cc)))
    # vốn theo giá thị trường
    mtm = tt["so_du"]
    for m, p in vithe.items():
        a = TS[m]
        j = bisect.bisect_right(a.dong, T) - 1
        mtm += p.kl * p.con * (a.c[j] - p.gia_khop) * p.chieu
    tt["von"].append((T, mtm))
    tt["nen_cuoi"] = T
    return ra


def chay_ky(TS, ds_ma, co, bat_dau, ket_thuc, toi_da=TOI_DA, rui_ro=RUI_RO):
    """Backtest một kỳ bằng bộ máy buoc (tương đương chay.mo_phong khi co = CO_V1)."""
    tt = tt_moi()
    moc = sorted({t for m in ds_ma for t in TS[m].dong if bat_dau <= t <= ket_thuc})
    for T in moc:
        buoc(tt, T, TS, ds_ma, co, toi_da, rui_ro)
    for m, p in list(tt["vithe"].items()):
        a = TS[m]
        j = bisect.bisect_right(a.dong, ket_thuc) - 1
        _thoat(p, p.con, a.c[j], a.dong[j], tt, None, "Cuối kỳ"); p.kq += "Cuối kỳ"
        tt["lenh"].append(p)
    tt["vithe"] = {}
    tt["von"][-1] = (tt["von"][-1][0], tt["so_du"])
    for p in tt["lenh"]:
        p.R = p.lai / p.rui_ro_usd
    tt["lenh"].sort(key=lambda p: p.khop_ts)
    return dict(lenh=tt["lenh"], von=tt["von"], so_du=tt["so_du"], pheu=Counter(tt["pheu"]), huy=Counter(tt["huy"]),
                pha_moc=Counter(tt["pha_moc"]))


# ---------------- GIẢ DƯỢC ----------------
def mot_lenh_gia(a, k, x, sl_pct, tp1_pct, tp2_pct, het_han, sl_dong, ket_thuc):
    vao = a.c[k]
    sl, tp1, tp2 = vao * (1 - x * sl_pct), vao * (1 + x * tp1_pct), vao * (1 + x * tp2_pct)
    sl_kc = vao * (1 - x * SL_KHAN * sl_pct)
    con, tp1_xong, ra = 1.0, False, []
    j_cuoi = bisect.bisect_right(a.dong, ket_thuc) - 1
    for j in range(k + 1, min(k + het_han, j_cuoi) + 1):
        o, h, l, c, ts = a.o[j], a.h[j], a.l[j], a.c[j], a.dong[j]
        if not sl_dong:
            if C.cham(sl, x, h, l, True):
                ra.append((ts, con, C.gia_thoat(sl, x, o, True))); return vao, ra
            if not tp1_xong and C.cham(tp1, x, h, l, False):
                if tp2 == tp1:
                    ra.append((ts, con, C.gia_thoat(tp1, x, o, False))); return vao, ra
                ra.append((ts, 0.5, C.gia_thoat(tp1, x, o, False))); con, tp1_xong, sl = 0.5, True, vao
                if C.cham(sl, x, h, l, True):
                    ra.append((ts, con, sl)); return vao, ra
            if tp1_xong and C.cham(tp2, x, h, l, False):
                ra.append((ts, con, C.gia_thoat(tp2, x, o, False))); return vao, ra
            continue
        if C.cham(sl_kc, x, h, l, True):
            ra.append((ts, con, C.gia_thoat(sl_kc, x, o, True))); return vao, ra
        if not tp1_xong and C.cham(tp1, x, h, l, False):
            if tp2 == tp1:
                ra.append((ts, con, C.gia_thoat(tp1, x, o, False))); return vao, ra
            ra.append((ts, 0.5, C.gia_thoat(tp1, x, o, False))); con, tp1_xong = 0.5, True
            sl_kc, sl = sl, vao
            if C.cham(sl_kc, x, h, l, True):
                ra.append((ts, con, sl_kc)); return vao, ra
        if tp1_xong and C.cham(tp2, x, h, l, False):
            ra.append((ts, con, C.gia_thoat(tp2, x, o, False))); return vao, ra
        if (c > sl) if x < 0 else (c < sl):
            ra.append((ts, con, c)); return vao, ra
    j = min(k + het_han, j_cuoi)
    ra.append((a.dong[j], con, a.c[j]))
    return vao, ra


def gia_duoc(lenh, TS, bat_dau, ket_thuc, rui_ro=RUI_RO, seed=C.SEED, so_lan=C.SO_LAN_GD):
    """Cùng thuật toán chay.gia_duoc; quản lý theo đúng từng lệnh (SL giá/đóng nến, số nến giữ)."""
    rng = random.Random(seed)
    nen_thang = defaultdict(list)
    for m in {p.ma for p in lenh}:
        a = TS[m]
        for k, t in enumerate(a.dong):
            if bat_dau <= t < ket_thuc and k + 1 < len(a.dong) and a.dong[k + 1] <= ket_thuc:
                nen_thang[(m, C.thang(t))].append(k)
    lai_ds, r_ds = [], []
    for _ in range(so_lan):
        su_kien = []
        for n, p in enumerate(lenh):
            a = TS[p.ma]
            k = rng.choice(nen_thang[(p.ma, C.thang(p.khop_ts))])
            x = rng.choice((-1, 1))
            tp1_pct = abs(p.tp1 - p.vao) / p.vao; tp2_pct = abs(p.tp2 - p.vao) / p.vao
            vao, ra = mot_lenh_gia(a, k, x, p.sl_pct, tp1_pct, tp2_pct, p.het_han, p.sl_dong, ket_thuc)
            su_kien.append((a.dong[k], 1, n, vao, x, p.sl_pct, None))
            for ts, tl, gia in ra:
                su_kien.append((ts, 0, n, gia, x, tl, None))
        su_kien.sort(key=lambda e: (e[0], e[1]))
        so_du, mo, tong_r = VON0, {}, 0.0
        for ts, loai, n, gia, x, v, _ in su_kien:
            if loai == 1:
                rr = rui_ro * so_du; gt = rr / v
                mo[n] = [gt / gia, gia, rr, -gt * C.PHI_VAO]
                so_du -= gt * C.PHI_VAO
            else:
                kl, vao, rr, lai = mo[n]
                d = kl * v * (gia - vao) * x - kl * v * gia * C.PHI_RA
                so_du += d; mo[n][3] += d
        for n, (kl, vao, rr, lai) in mo.items():
            tong_r += lai / rr
        lai_ds.append(so_du - VON0); r_ds.append(tong_r)
    return lai_ds, r_ds


# ---------------- THỐNG KÊ / BÁO CÁO ----------------
def nhom_kq(kq):
    """Gom kiểu kết thúc cho bảng."""
    return kq


def tom(kq_chay):
    st = C.thong_ke(kq_chay["lenh"])
    return dict(st, so_du=kq_chay["so_du"], dd=C.sut_giam(kq_chay["von"]))


def dong_tom(ten, kq_chay, gd=None):
    s = tom(kq_chay)
    pv = f"{C.phan_vi(gd[0], s['so_du'] - VON0):.0f}" if gd else "—"
    pvr = f"{C.phan_vi(gd[1], s['tong_r']):.0f}" if gd else "—"
    return [ten, C.tien(s["so_du"] - VON0), C.pct(s["so_du"] / VON0 - 1), s["n"], C.pct0(s["thang"], 0) if s["n"] else "—",
            C.so(s["r_tb"]), C.so(s["tong_r"], 1), C.pct0(s["dd"]), C.so(s["pf"]) if s["pf"] != float("inf") else "∞", pv, pvr]


TIEU_TOM = ["Bản", "Lãi/lỗ", "%", "Số lệnh", "Thắng", "R TB", "Tổng R", "Sụt giảm lớn nhất", "Hệ số LN", "Phân vị giả dược ($)", "Phân vị (R)"]


def bang_nhom(tieu, d, thu_tu=None):
    rows = []
    for kh in (thu_tu or sorted(d, key=str)):
        ds = d.get(kh, [])
        st = C.thong_ke(ds)
        rows.append([kh, st["n"], C.pct0(st["thang"], 0) if ds else "—", C.so(st["r_tb"]) if ds else "—",
                     C.so(st["tong_r"], 1), C.tien(st["lai"])])
    return C.bang([tieu, "Số lệnh", "Thắng", "R TB", "Tổng R", "Lãi/lỗ"], rows)


COT = ["tai_san", "chieu", "kieu_vao", "gio_tin_hieu", "gio_khop", "gio_dong", "gia_vao", "gia_khop", "sl", "sl_pct",
       "chan_khan_cap", "tp1", "tp2", "rr_tp1", "can_cu_hoi_tu", "sl_nguon", "tp2_nguon", "giu_toi_da_nen", "don_bay",
       "gia_tri_vi_the", "rui_ro_usd", "ket_qua", "R", "lai_usd", "phi_usd"]


def ghi_lenh(lenh, duong_dan):
    with Path(duong_dan).open("w", newline="") as f:
        w = csv.writer(f); w.writerow(COT)
        for p in lenh:
            kieu = p.get("kieu", "ema34")
            w.writerow([p.ma, "SHORT" if p.chieu < 0 else "LONG", kieu, C.vn(p.tin_hieu_ts), C.vn(p.khop_ts), C.vn(p.dong_ts),
                        C.g(p.vao), C.g(p.gia_khop), C.g(p.sl0), round(p.sl_pct * 100, 3),
                        C.g(p.vao + SL_KHAN * (p.sl0 - p.vao)) if p.get("sl_dong") else "", C.g(p.tp1), C.g(p.tp2),
                        round(p.rr, 2), ("EMA34+" if kieu == "ema34" else "") + "+".join(p.cc), p.sl_nguon, p.tp2_nguon,
                        p.get("het_han", C.NEN_GIU), round(p.bay, 1), round(p.gtvt, 2), round(p.rui_ro_usd, 2), p.kq,
                        round(p.R, 3), round(p.lai, 2), round(p.phi, 2)])


def chi_tiet_lenh(a, p, tieu):
    """In nến-theo-nến một lệnh để đối chiếu tay."""
    out = []
    t, x = p.t, p.chieu
    kieu = p.get("kieu", "ema34")
    out.append(f"=== {tieu}: {p.ma} {'SHORT' if x < 0 else 'LONG'} kiểu {kieu} — tín hiệu {C.vn(a.dong[t])} VN, khớp {C.vn(p.khop_ts)}, "
               f"kết quả {p.kq}, R={p.R:.2f}, lãi {p.lai:+.2f}$")
    for j in (t - 1, t):
        out.append(f"  nến đóng {C.vn(a.dong[j])}: O={C.g(a.o[j])} H={C.g(a.h[j])} L={C.g(a.l[j])} C={C.g(a.c[j])} | EMA34 cao={C.g(a.e34h[j])} "
                   f"thấp={C.g(a.e34l[j])} EMA89={C.g(a.e89[j])} EMA200={C.g(a.e200[j])} ATR14={C.g(a.atr[j])} → xu={a.xu[j]}")
    out.append(f"  số lần cắt EMA89 trong 30 nến = {sum(a.cat89[max(1, t - DI_NGANG_NEN + 2):t + 1])} (đứng ngoài nếu ≥ {DI_NGANG_CAT})")
    i_lon = tim_nen_lon(a, t, x)
    if i_lon is not None:
        out.append(f"  nến lớn: {C.vn(a.dong[i_lon])} thân {C.g(abs(a.c[i_lon] - a.o[i_lon]))} ≥ 2,5×ATR {C.g(a.atr[i_lon - 1])} = {C.g(2.5 * a.atr[i_lon - 1])}")
    if p.get("moc"):
        i, L = p.moc
        out.append(f"  mốc bị phá: {'đáy' if x < 0 else 'đỉnh'} fractal {C.g(L)} ({C.vn(a.dong[i])}); đóng t−2={C.g(a.c[t - 2])} t−1={C.g(a.c[t - 1])} t={C.g(a.c[t])}")
    if p.fib:
        i0, p0, cuoi = p.fib
        out.append(f"  nhịp: A={C.g(p0)} ({C.vn(a.dong[i0])}) → B={C.g(cuoi)}; 0.5={C.g(cuoi + .5 * (p0 - cuoi))} 0.618={C.g(cuoi + .618 * (p0 - cuoi))}; "
                   f"mở rộng từ C={C.g(p.vao)}: 1.0={C.g(p.vao + (cuoi - p0))} 1.618={C.g(p.vao + 1.618 * (cuoi - p0))}")
    out.append(f"  giá vào={C.g(p.vao)}; căn cứ: {'+'.join(p.cc)}; SL danh nghĩa={C.g(p.sl0)} ({p.sl_pct * 100:.2f}%, {p.sl_nguon})"
               + (f"; chặn khẩn cấp={C.g(p.vao + SL_KHAN * (p.sl0 - p.vao))}" if p.get("sl_dong") else "")
               + f"; TP1={C.g(p.tp1)} TP2={C.g(p.tp2)} ({p.tp2_nguon}); R:R={p.rr:.2f}; giữ tối đa {p.get('het_han', C.NEN_GIU)} nến")
    for j in range(t + 1, min(p.k_khop + p.get("het_han", C.NEN_GIU), len(a.c) - 1) + 1):
        dau = "KHỚP→" if j == p.k_khop else ("      " if j < p.k_khop else "  giữ ")
        out.append(f"   {dau} {C.vn(a.dong[j])} O={C.g(a.o[j])} H={C.g(a.h[j])} L={C.g(a.l[j])} C={C.g(a.c[j])}")
        if a.dong[j] >= p.dong_ts:
            break
    out.append(f"  đóng lúc {C.vn(p.dong_ts)}; giá khớp {C.g(p.gia_khop)}; khối lượng {C.g(p.gtvt)}$ x{p.bay:.1f}; rủi ro {p.rui_ro_usd:.2f}$")
    return out


def soi_sl_khop(kq, TS):
    """Được/mất của SL nến đóng so với SL giá (ước lượng: lệnh thua trọn theo SL giá ≈ −1,04R) và thống kê khớp lệnh."""
    cuu = cuu_r = sau = sau_r = 0
    for p in kq["lenh"]:
        a = TS[p.ma]; f = p.k_khop; k = bisect.bisect_left(a.dong, p.dong_ts)
        if p.get("sl_dong") and any(C.cham(p.sl0, p.chieu, a.h[j], a.l[j], True) for j in range(f, k + 1)) and p.R > -0.95:
            cuu += 1; cuu_r += p.R + 1.04
        if p.kq in ("SL(đóng)", "SL(khẩn)"):
            sau += 1; sau_r += p.R + 1.04
    n, dat = len(kq["lenh"]), kq["pheu"].get("dat_lenh", 0)
    return dict(n=n, cuu=cuu, cuu_r=cuu_r, sau=sau, sau_r=sau_r, dat=dat, ti_le_khop=n / max(dat, 1),
                huy_tp1=kq["huy"].get("cham_tp1_truoc", 0),
                sl_ngay=sum(1 for p in kq["lenh"] if p.kq.startswith("SL") and p.khop_ts == p.dong_ts),
                tp1_pct=sum(abs(p.tp1 - p.vao) / p.vao for p in kq["lenh"]) / max(n, 1),
                rr=sum(p.rr for p in kq["lenh"]) / max(n, 1), gio=sum((p.dong_ts - p.khop_ts) / 3600 for p in kq["lenh"]) / max(n, 1))


def kiem_rang_buoc(lenh, TS, co, toi_da=TOI_DA):
    loi = []
    for p in lenh:
        a = TS[p.ma]; t, f = p.t, p.k_khop
        if C.thu_hai(p.khop_ts) or C.thu_hai(p.tin_hieu_ts): loi.append(f"{p.ma} {C.vn(p.khop_ts)}: thứ Hai")
        if not (f > t and f - t <= C.NEN_CHO): loi.append(f"{p.ma}: khớp ngoài 6 nến")
        if (a.h[f] < p.vao) if p.chieu < 0 else (a.l[f] > p.vao): loi.append(f"{p.ma} {C.vn(p.khop_ts)}: nến khớp không chạm giá vào")
        for j in range(t + 1, f):
            if ((a.h[j] >= p.vao) if p.chieu < 0 else (a.l[j] <= p.vao)) and not C.thu_hai(a.dong[j]):
                loi.append(f"{p.ma}: lẽ ra khớp sớm hơn")
            if (a.l[j] <= p.tp1) if p.chieu < 0 else (a.h[j] >= p.tp1):
                loi.append(f"{p.ma}: đã chạm TP1 trước khi khớp mà không hủy")
        if p.sl_pct < C.D_MIN[p.ma] - 1e-12 or p.sl_pct > C.SL_TOI_DA: loi.append(f"{p.ma}: SL% sai")
        if p.rr < C.RR_MIN: loi.append(f"{p.ma}: R:R < 1,5")
        so_nen = bisect.bisect_left(a.dong, p.dong_ts) - f
        if so_nen > p.het_han: loi.append(f"{p.ma} {C.vn(p.khop_ts)}: giữ {so_nen} nến > {p.het_han}")
        if co["di_ngang"] and sum(a.cat89[max(1, t - DI_NGANG_NEN + 2):t + 1]) >= DI_NGANG_CAT: loi.append(f"{p.ma}: vào khi đi ngang")
        if co["nen_lon"] and (tim_nen_lon(a, t, p.chieu) is not None) != (p.kieu == "nen_lon"): loi.append(f"{p.ma}: sai kiểu nến lớn")
        if p.ma == "VANG" and co["vang_scalp"] and (p.tp2 != p.tp1 or "TP2" in p.kq): loi.append("vàng có TP2")
        if p.sl_dong and "SL(đóng)" in p.kq:
            k = bisect.bisect_left(a.dong, p.dong_ts)
            if not ((a.c[k] > p.sl0) if p.chieu < 0 else (a.c[k] < p.sl0)): loi.append(f"{p.ma}: SL(đóng) nhưng giá đóng chưa qua SL")
            for j in range(f, k):
                if (a.c[j] > p.sl0) if p.chieu < 0 else (a.c[j] < p.sl0): loi.append(f"{p.ma}: lẽ ra SL(đóng) sớm hơn")
        if p.sl_dong and p.kq == "SL(khẩn)":
            k = bisect.bisect_left(a.dong, p.dong_ts)
            if not C.cham(p.vao + SL_KHAN * (p.sl0 - p.vao), p.chieu, a.h[k], a.l[k], True): loi.append(f"{p.ma}: khẩn mà không chạm")
    for i, x in enumerate(lenh):
        dang_mo = [y for j, y in enumerate(lenh) if j != i and y.khop_ts <= x.khop_ts < y.dong_ts]
        if len(dang_mo) + 1 > toi_da: loi.append(f"quá số lệnh mở lúc {C.vn(x.khop_ts)}")
        if any(y.ma == x.ma for y in dang_mo): loi.append(f"2 lệnh cùng tài sản {x.ma} lúc {C.vn(x.khop_ts)}")
    return loi


DANH_LY_DO = [("khong_tin_hieu", "Không đủ luật 1+2 (xu hướng H4 2 cây)"), ("loc_d1", "Bị lọc D1 (luật 3)"),
              ("di_ngang", "Đi ngang: cắt EMA89 ≥ 6 lần/30 nến (TĐ1)"),
              ("ema_chum", "EMA chụm <0,6% (luật 4)"), ("thu_hai", "Thứ Hai (luật 5)"),
              ("khong_nhip", "Nến lớn nhưng không có nhịp (TĐ2)"), ("fibo_da_qua", "Nến lớn: Fibo 0.5 đã ở sau giá (TĐ2)"),
              ("khong_hoi_tu", "Thiếu căn cứ hội tụ (luật 7)"), ("sl_qua_xa", "SL >6% (luật 8)"),
              ("khong_co_dich", "Không có đích (luật 9 / TĐ5)"), ("rr_thap", "R:R TP1 <1,5"),
              ("dat_lenh", "→ ĐẶT LỆNH CHỜ")]


def lam_bao_cao(R):
    L = []
    w = L.append
    cu = (GOC / "KET_QUA_V2.md").read_text() if (GOC / "KET_QUA_V2.md").exists() else ""

    def khoi(ten):
        a, b = f"<!-- {ten} -->", f"<!-- /{ten} -->"
        return cu[cu.index(a):cu.index(b) + len(b)] if a in cu and b in cu else f"{a}\n_(chưa viết)_\n{b}"

    w("# KẾT QUẢ BOT V2 (luật cơ học v1 + 5 thay đổi) — so với v1, 6 tài sản\n")
    w("_Sinh tự động bởi `backtest/v2.py` (chạy lại: `python3 backtest/v2.py`). Tài sản: BTC, ETH, OKB, BNB (OKX), vàng GC=F, dầu CL=F (Yahoo). "
      "Vốn 4.000$, rủi ro 2%/lệnh, tối đa 4 lệnh mở, phí vào 0,02% / ra 0,05%, bỏ funding. v1 = `chay.py` nguyên văn (luật 8 theo GIÁ), "
      "chạy trên đúng 6 tài sản, tối đa 4 lệnh. Tham số v2 chốt trước, không dò/tối ưu — mục **Diễn giải** (viết trước lần chạy đầu) ở cuối file._\n")
    w("> **2025 là NGOÀI MẪU** (luật học từ các buổi live 2026, chưa từng nhìn 2025). **2026 là TRONG MẪU**: 5 thay đổi của v2 được đề xuất "
      "sau khi xem lỗi của v1 trên chính 2026 (BAI_HOC.md mục B), nên số 2026 của v2 lạc quan có hệ thống. Thước đo chính là cột 2025.\n")
    # 1. bảng tổng
    w("## 1. Bảng tổng v1 vs v2\n")
    rows = []
    for ky in KY:
        for bn in ("v1", "v2"):
            rows.append(dong_tom(f"**{bn}** · {KY[ky]['nhan']}", R[ky][bn], R[ky]["gd"][bn]))
    w(C.bang(TIEU_TOM, rows))
    w("\n_R TB = lãi ròng sau phí ÷ rủi ro dự kiến (SL danh nghĩa). Sụt giảm tính trên vốn theo giá thị trường mỗi nến H4. "
      "Phân vị giả dược = % số lần giả dược thua kết quả thật (200 lần)._\n")
    rows = []
    for ky in KY:
        for ten, d in R[ky]["bh"].items():
            rows.append([KY[ky]["nhan"], f"Mua & giữ {ten}", C.tien(d[-1][1] - VON0), C.pct(d[-1][1] / VON0 - 1), C.pct0(C.sut_giam(d))])
    w("**Mốc so sánh: mua & giữ** (vốn 4.000$ chia đều, mua ở giá đóng H4 cuối trước đầu kỳ, phí 0,05% mỗi đầu)\n")
    w(C.bang(["Kỳ", "Chiến lược", "Lãi/lỗ", "%", "Sụt giảm lớn nhất"], rows))
    # giả dược
    w("\n### Giả dược (200 lần, seed cố định)\n")
    rows = []
    for ky in KY:
        for bn in ("v1", "v2"):
            lai, rr = R[ky]["gd"][bn]; s = tom(R[ky][bn])
            rows.append([f"{bn} · {KY[ky]['nhan']}", C.tien(s["so_du"] - VON0), C.tien(C.q(lai, .05)), C.tien(C.q(lai, .5)), C.tien(C.q(lai, .95)),
                         C.pct0(sum(v > 0 for v in lai) / len(lai), 0), f"{C.phan_vi(lai, s['so_du'] - VON0):.0f}",
                         C.so(s["tong_r"], 1), C.so(C.q(rr, .5), 1), f"{C.phan_vi(rr, s['tong_r']):.0f}"])
    w(C.bang(["Bản · kỳ", "Thật", "Giả dược P5", "P50", "P95", "% lần giả dược lãi", "Phân vị ($)", "Tổng R thật", "Tổng R giả dược P50", "Phân vị (R)"], rows))
    w("\n_Giả dược giữ đúng số lệnh, tài sản, tháng khớp, khoảng SL%/TP1%/TP2% và cách quản lý của từng lệnh thật (v2: SL nến đóng + chặn 2×, "
      "vàng 100% ở TP1 và 6 nến); chỉ thay thời điểm vào (nến ngẫu nhiên cùng tháng, vào ở giá đóng) và chiều (50/50)._\n")
    # 2. đóng góp từng thay đổi
    w("## 2. Đóng góp từng thay đổi (chỉ để quy công — v2 chính thức KHÔNG chọn theo bảng này)\n")
    rows = []
    for nhan, kq25, kq26 in R["quy_cong"]:
        s5, s6 = tom(kq25), tom(kq26)
        rows.append([nhan, C.tien(s5["so_du"] - VON0), s5["n"], C.so(s5["tong_r"], 1), C.pct0(s5["dd"]),
                     C.tien(s6["so_du"] - VON0), s6["n"], C.so(s6["tong_r"], 1), C.pct0(s6["dd"])])
    w(C.bang(["Bản", "2025 lãi", "2025 lệnh", "2025 tổng R", "2025 DD", "2026 lãi", "2026 lệnh", "2026 tổng R", "2026 DD"], rows))
    w("\n_“v1 + X” = v1 chỉ bật thêm thay đổi X; “v2 − X” = v2 tắt riêng X. Các thay đổi tương tác nhau (vd TĐ2 thay hẳn kiểu vào, TĐ5 đổi đích nên đổi luôn tập lệnh qua R:R), nên tổng các phần không bằng tổng thể._\n")
    # 3. theo tài sản
    w("## 3. Theo tài sản\n")
    for ky in KY:
        rows = []
        g1, g2 = C.nhom(R[ky]["v1"]["lenh"], lambda p: p.ma), C.nhom(R[ky]["v2"]["lenh"], lambda p: p.ma)
        for m in TAI_SAN:
            s1, s2 = C.thong_ke(g1.get(m, [])), C.thong_ke(g2.get(m, []))
            a = R[ky]["TS"][m]
            b0, b1 = C.ngay_vn(KY[ky]["tu"]), C.ngay_vn(KY[ky]["den"]) + C.NGAY
            g0 = a.c[bisect.bisect_right(a.dong, b0) - 1]; gk = a.c[bisect.bisect_right(a.dong, b1) - 1]
            ds2 = g2.get(m, [])
            rows.append([C.TEN[m], s1["n"], C.so(s1["tong_r"], 1), C.tien(s1["lai"]), s2["n"],
                         f"{sum(p.chieu > 0 for p in ds2)}/{sum(p.chieu < 0 for p in ds2)}", C.pct0(s2["thang"], 0) if ds2 else "—",
                         C.so(s2["tong_r"], 1), C.tien(s2["lai"]), C.pct(gk / g0 - 1)])
        w(f"**{KY[ky]['nhan']}**\n")
        w(C.bang(["Tài sản", "v1 lệnh", "v1 tổng R", "v1 lãi", "v2 lệnh", "v2 L/S", "v2 thắng", "v2 tổng R", "v2 lãi", "Giá cả kỳ"], rows))
        w("")
    w("_Lãi/lỗ theo tài sản cộng các lệnh khớp; vì vốn dùng chung (rủi ro 2% số dư lúc khớp) nên $ phụ thuộc thứ tự lệnh, so sánh bằng tổng R chắc hơn._\n")
    # 4. theo tháng
    w("## 4. Theo tháng (tháng khớp lệnh)\n")
    for ky in KY:
        rows = []
        thang_ds = sorted({C.thang(T) for T, _ in R[ky]["v1"]["von"]} | {C.thang(T) for T, _ in R[ky]["v2"]["von"]})
        vt = {bn: {} for bn in ("v1", "v2")}
        for bn in vt:
            for T, v in R[ky][bn]["von"]:
                vt[bn][C.thang(T)] = v
        g = {bn: C.nhom(R[ky][bn]["lenh"], lambda p: C.thang(p.khop_ts)) for bn in vt}
        truoc = {"v1": VON0, "v2": VON0}
        for th in thang_ds:
            dong = [th]
            for bn in ("v1", "v2"):
                st = C.thong_ke(g[bn].get(th, []))
                v = vt[bn].get(th, truoc[bn])
                dong += [st["n"], C.so(st["tong_r"], 1), C.pct(v / truoc[bn] - 1)]
                truoc[bn] = v
            rows.append(dong)
        w(f"**{KY[ky]['nhan']}**\n")
        w(C.bang(["Tháng", "v1 lệnh", "v1 tổng R", "v1 đổi vốn", "v2 lệnh", "v2 tổng R", "v2 đổi vốn"], rows))
        w("")
    # 5. long/short, kiểu vào, kiểu thoát
    w("## 5. Long / Short, kiểu vào, kiểu kết thúc\n")
    for ky in KY:
        w(f"**{KY[ky]['nhan']} — theo chiều**\n")
        rows = []
        for bn in ("v1", "v2"):
            for ch, ten in ((1, "LONG"), (-1, "SHORT")):
                ds = [p for p in R[ky][bn]["lenh"] if p.chieu == ch]
                st = C.thong_ke(ds)
                rows.append([bn, ten, st["n"], C.pct0(st["thang"], 0) if ds else "—", C.so(st["r_tb"]) if ds else "—", C.so(st["tong_r"], 1), C.tien(st["lai"])])
        w(C.bang(["Bản", "Chiều", "Số lệnh", "Thắng", "R TB", "Tổng R", "Lãi/lỗ"], rows))
        w(f"\n**{KY[ky]['nhan']} — v2 theo kiểu vào**\n")
        w(bang_nhom("Kiểu vào", C.nhom(R[ky]["v2"]["lenh"], lambda p: TEN_KIEU[p.kieu])))
        w(f"\n**{KY[ky]['nhan']} — kiểu kết thúc (v1 | v2)**\n")
        w(bang_nhom("v1", C.nhom(R[ky]["v1"]["lenh"], lambda p: p.kq)))
        w("")
        w(bang_nhom("v2", C.nhom(R[ky]["v2"]["lenh"], lambda p: p.kq)))
        w("")
    w("_Kết quả v2: SL(đóng) = nến H4 đóng qua SL; SL(khẩn) = chạm chặn khẩn cấp 2×; TP1+HV(đóng) = sau TP1 nến đóng qua giá vào; "
      "TP1+khẩn = sau TP1 chạm SL danh nghĩa cũ; TP1(hết) = đóng 100% ở TP1 (vàng); Hết hạn = 18 nến (vàng 6)._\n")
    # 6. phễu
    w("## 6. Phễu tín hiệu (lượt nến H4 khi tài sản chưa có lệnh/lệnh chờ)\n")
    rows = []
    cot = [(ky, bn) for ky in KY for bn in ("v1", "v2")]
    for ma, ten in DANH_LY_DO:
        rows.append([ten] + [R[ky][bn]["pheu"].get(ma, 0) for ky, bn in cot])
    for ma, ten in C.DANH_HUY:
        rows.append([ten] + [R[ky][bn]["huy"].get(ma, 0) for ky, bn in cot])
    rows.append(["**Lệnh khớp**"] + [len(R[ky][bn]["lenh"]) for ky, bn in cot])
    w(C.bang(["Bước"] + [f"{bn} {ky}" for ky, bn in cot], rows))
    rows = []
    for ky in KY:
        pm = R[ky]["v2"]["pha_moc"]
        rows.append([KY[ky]["nhan"], pm.get("su_kien", 0), pm.get("dat", 0), pm.get("dat_lenh", 0), pm.get("khong_hoi_tu", 0), pm.get("rr_thap", 0),
                     pm.get("khong_co_dich", 0), pm.get("sl_qua_xa", 0)])
    w("\n**Kiểu phá mốc (TĐ3), v2** — số lượt có sự kiện phá 2 cây và kết cục của ứng viên này\n")
    w(C.bang(["Kỳ", "Sự kiện", "Được chọn đặt lệnh", "Qua luật nhưng EMA34 gần giá hơn", "Thiếu hội tụ", "R:R thấp", "Không có đích", "SL quá xa"], rows))
    # soi TĐ4 + TĐ5
    w("\n**Soi thay đổi 4 (SL nến đóng) và 5 (TP Fibo) — vì sao số lệnh tăng ~4 lần**\n")
    rows = []
    for ky in KY:
        for nhan, kq in R[ky]["soi"]:
            s = soi_sl_khop(kq, R[ky]["TS"])
            rows.append([KY[ky]["nhan"][:4], nhan, s["dat"], s["n"], C.pct0(s["ti_le_khop"], 0), s["huy_tp1"], s["sl_ngay"], C.so(s["rr"]),
                         C.pct0(s["tp1_pct"], 2), f"{s['gio']:.0f}",
                         f"{s['cuu']} / {C.so(s['cuu_r'], 1)}R" if kq["lenh"] and kq["lenh"][0].get("sl_dong") else "—",
                         f"{s['sau']} / {C.so(s['sau_r'], 1)}R" if kq["lenh"] and kq["lenh"][0].get("sl_dong") else "—"])
    w(C.bang(["Kỳ", "Bản", "Lệnh chờ đặt", "Khớp", "Tỉ lệ khớp", "Hủy vì chạm TP1 trước", "SL ngay nến khớp", "R:R TB", "TP1 cách giá vào TB",
              "Giữ TB (giờ)", "Chạm SL danh nghĩa mà không thua trọn: lệnh / R lấy lại", "Thua theo nến đóng/khẩn: lệnh / R lỗ thêm"], rows))
    w("\n_“R lấy lại” và “R lỗ thêm” so với mốc thua trọn theo SL giá ≈ −1,04R (ước lượng thô: coi mọi lệnh chạm SL danh nghĩa là lẽ ra thua trọn)._\n")
    # 7. lệnh mẫu
    w("\n## 7. Lệnh mẫu v2 (đối chiếu tay đầy đủ trong `tu_kiem_v2.txt`)\n")
    rows = []
    for ky in KY:
        ds = sorted(R[ky]["v2"]["lenh"], key=lambda p: p.lai)
        for p in ds[::-1][:4] + ds[:3]:
            rows.append([KY[ky]["nhan"][:4], C.vn(p.khop_ts)[:13], C.TEN[p.ma], "SHORT" if p.chieu < 0 else "LONG", TEN_KIEU[p.kieu], p.kq,
                         C.so(p.R), C.tien(p.lai), f"vào {C.g(p.vao)}, SL {C.so(p.sl_pct * 100)}%, R:R {C.so(p.rr, 1)}, {'+'.join(p.cc)}, giữ {round((p.dong_ts - p.khop_ts) / 3600)} giờ"])
    w(C.bang(["Kỳ", "Khớp", "Tài sản", "Chiều", "Kiểu vào", "Kết quả", "R", "Lãi", "Chi tiết"], rows))
    w("\n_Mỗi kỳ: 4 lệnh lãi nhất + 3 lệnh lỗ nhất._\n")
    w("\n## 8. Nhận xét\n")
    w(khoi("NHAN_XET"))
    w("\n" + khoi("DIEN_GIAI"))
    w("\n## Tự kiểm\n")
    w("```\n" + R["tu_kiem_tom"] + "\n```\n")
    w("Chi tiết (lệnh mẫu từng nến, phép thử cắt cụt): `backtest/tu_kiem_v2.txt`. Danh sách lệnh: `lenh_v1_2025.csv`, `lenh_v2_2025.csv`, `lenh_v1_2026.csv`, `lenh_v2_2026.csv`.\n")
    return "\n".join(L)


# ---------------- CHẠY ----------------
def dat_ky(ky):
    C.cau_hinh(tu=KY[ky]["tu"], den=KY[ky]["den"], thu_muc_du_lieu=KY[ky]["du_lieu"])
    return C.BAT_DAU, C.KET_THUC


def so_lenh(l1, l2):
    """So 2 danh sách lệnh (chay.mo_phong vs bộ máy) — trả số lệch."""
    if len(l1) != len(l2):
        return max(len(l1), len(l2))
    lech = 0
    for a, b in zip(l1, l2):
        if (a.ma, a.khop_ts, a.dong_ts, a.kq, a.chieu) != (b.ma, b.khop_ts, b.dong_ts, b.kq, b.chieu) or abs(a.lai - b.lai) > 1e-6:
            lech += 1
    return lech


def main():
    out, tom_tat = [], []
    R = {}
    for ky in KY:
        bd, kt = dat_ky(ky)
        TS = {m: nap(m, KY[ky]["du_lieu"]) for m in TAI_SAN}
        v1_goc = C.mo_phong("v1", TAI_SAN, RUI_RO, True, TOI_DA, TS)           # v1 = chay.py nguyên văn
        v1 = chay_ky(TS, TAI_SAN, CO_V1, bd, kt)
        v2 = chay_ky(TS, TAI_SAN, CO_V2, bd, kt)
        lech = so_lenh(v1_goc["lenh"], v1["lenh"])
        tom_tat.append(f"[{ky}] Bộ máy v2 với mọi thay đổi TẮT vs chay.mo_phong (6 tài sản, tối đa 4): {len(v1['lenh'])} vs {len(v1_goc['lenh'])} lệnh, "
                       f"{lech} lệnh lệch, số dư {v1['so_du']:.6f} vs {v1_goc['so_du']:.6f}")
        # quyết định từng nến: v2 tắt hết == chay.quyet_dinh
        lech_qd = tong_qd = 0
        for m in TAI_SAN:
            a = TS[m]
            for k in range(len(a.dong)):
                if not (bd <= a.dong[k] <= kt):
                    continue
                tong_qd += 1
                r1, q1 = C.quyet_dinh(a, k)
                r2, q2, _ = quyet_dinh_v2(a, k, CO_V1)
                if r1 != r2 or (q1 and any(abs(q1[f] - q2[f]) > 1e-9 * abs(q1[f]) for f in ("vao", "sl", "tp1", "tp2", "rr")) or (q1 and q1["cc"] != q2["cc"])):
                    lech_qd += 1
        tom_tat.append(f"[{ky}] quyet_dinh_v2(tắt hết) vs chay.quyet_dinh trên {tong_qd} nến: {lech_qd} lệch")
        gd1 = C.gia_duoc(v1_goc, TS, RUI_RO, C.SEED)
        for p in v1["lenh"]:
            p.setdefault("het_han", C.NEN_GIU)
        gd1b = gia_duoc(v1["lenh"], TS, bd, kt)
        tom_tat.append(f"[{ky}] Giả dược bộ máy (chế độ v1) vs chay.gia_duoc: {'trùng khít' if gd1 == gd1b else 'LỆCH'}")
        gd2 = gia_duoc(v2["lenh"], TS, bd, kt)
        loi = kiem_rang_buoc(v2["lenh"], TS, CO_V2)
        tom_tat.append(f"[{ky}] Kiểm ràng buộc {len(v2['lenh'])} lệnh v2 (thứ Hai, khớp trong 6 nến, không khớp/chạm TP1 sớm hơn, SL% & R:R, "
                       f"≤4 lệnh, 1 lệnh/tài sản, không vào khi đi ngang, đúng kiểu nến lớn, vàng không TP2, SL(đóng)/khẩn đúng nến, số nến giữ) → {len(loi)} lỗi"
                       + "".join("\n  !! " + e for e in loi[:15]))
        # không nhìn trước: dựng lại với dữ liệu cắt cụt
        rng = random.Random(C.SEED + int(ky))
        tong = khop = 0
        for m in TAI_SAN:
            a = TS[m]
            ung = [k for k in range(len(a.dong)) if bd <= a.dong[k] <= kt and a.xu[k] != 0 and a.xu[k] == a.xu[k - 1]]
            dat = sorted({p.t for p in v2["lenh"] if p.ma == m})
            lon = [k for k in ung if tim_nen_lon(a, k, a.xu[k]) is not None]
            pm = [k for k in ung if tim_pha_moc(a, k, a.xu[k])]
            mau = (rng.sample(dat, min(6, len(dat))) + rng.sample(ung, min(6, len(ung))) + rng.sample(lon, min(3, len(lon)))
                   + rng.sample(pm, min(3, len(pm))))
            for k in mau:
                b = cat_cut(a, k, KY[ky]["du_lieu"])
                r1, q1, _ = quyet_dinh_v2(a, k, CO_V2)
                r2, q2, _ = quyet_dinh_v2(b, k, CO_V2)
                tong += 1
                if r1 == r2 and (q1 is None or (all(abs(q1[f] - q2[f]) <= 1e-9 * abs(q1[f]) for f in ("vao", "sl", "tp1", "tp2")) and q1.cc == q2.cc and q1.kieu == q2.kieu)):
                    khop += 1
                else:
                    out.append(f"!! LỆCH cắt cụt {ky} {m} {C.vn(a.dong[k])}: {r1} vs {r2}")
        tom_tat.append(f"[{ky}] Không nhìn trước: dựng lại chỉ báo (EMA, ATR, fractal, D1) với dữ liệu CẮT tại nến quyết định cho {tong} mẫu "
                       f"(lệnh thật + nến xu hướng + nến lớn + phá mốc) → {khop}/{tong} cùng quyết định/giá vào/SL/TP/căn cứ/kiểu")
        # mua & giữ
        bh = {C.TEN[m]: C.mua_giu(TS, [m], VON0) for m in TAI_SAN}
        bh["giỏ 6 tài sản"] = C.mua_giu(TS, TAI_SAN, VON0 / len(TAI_SAN))
        R[ky] = dict(v1=v1, v2=v2, gd=dict(v1=gd1b, v2=gd2), bh=bh, TS=TS)
        ghi_lenh(v1["lenh"], GOC / f"lenh_v1_{ky}.csv")
        ghi_lenh(v2["lenh"], GOC / f"lenh_v2_{ky}.csv")
        # đối chiếu số của agent chạy v1 (nếu có)
        p_ep = GOC / "ngoai_mau" / f"{KY[ky]['tu']}_{KY[ky]['den']}_gia" / "lenh_Ep.csv"
        if p_ep.exists():
            with p_ep.open() as f:
                ds = list(csv.DictReader(f))
            tong_lai = sum(float(r["lai_usd"]) for r in ds)
            tom_tat.append(f"[{ky}] Đối chiếu ngoai_mau/…/lenh_Ep.csv (v1, 6 tài sản, tối đa 4, agent khác chạy): {len(ds)} lệnh, lãi {tong_lai:+.2f}$ "
                           f"vs ta {len(v1['lenh'])} lệnh, {v1['so_du'] - VON0:+.2f}$")
        # lệnh mẫu
        mau_l = []
        for kieu in ("ema34", "pha_moc", "nen_lon"):
            ds = [p for p in v2["lenh"] if p.kieu == kieu]
            if ds:
                mau_l.append((f"Lệnh mẫu {ky} kiểu {kieu}", ds[len(ds) // 2]))
        for nhan, dk in (("SL(đóng)", lambda p: p.kq == "SL(đóng)"), ("chặn khẩn", lambda p: "khẩn" in p.kq), ("vàng", lambda p: p.ma == "VANG"),
                         ("TP1+TP2", lambda p: p.kq == "TP1+TP2")):
            ds = [p for p in v2["lenh"] if dk(p)]
            if ds:
                mau_l.append((f"Lệnh mẫu {ky} {nhan}", ds[0]))
        for nhan, p in mau_l:
            out.append("")
            out += chi_tiet_lenh(TS[p.ma], p, nhan)
        st1, st2 = tom(v1), tom(v2)
        print(f"[{ky}] v1: {st1['so_du'] - VON0:+.0f}$ {st1['n']} lệnh tổng R {st1['tong_r']:+.1f} DD {st1['dd'] * 100:.1f}% | "
              f"v2: {st2['so_du'] - VON0:+.0f}$ {st2['n']} lệnh tổng R {st2['tong_r']:+.1f} DD {st2['dd'] * 100:.1f}% "
              f"(giả dược phân vị {C.phan_vi(gd2[0], st2['so_du'] - VON0):.0f})")
    # quy công
    qc = [("v1", R["2025"]["v1"], R["2026"]["v1"])]
    for k in CO_V1:
        hang = []
        for ky in KY:
            bd, kt = dat_ky(ky)
            hang.append(chay_ky(R[ky]["TS"], TAI_SAN, dict(CO_V1, **{k: True}), bd, kt))
        qc.append((f"v1 + {TEN_CO[k]}", *hang))
    qc.append(("**v2 (đủ)**", R["2025"]["v2"], R["2026"]["v2"]))
    for k in CO_V1:
        hang = []
        for ky in KY:
            bd, kt = dat_ky(ky)
            hang.append(chay_ky(R[ky]["TS"], TAI_SAN, dict(CO_V2, **{k: False}), bd, kt))
        qc.append((f"v2 − {TEN_CO[k]}", *hang))
    R["quy_cong"] = qc
    for i, ky in enumerate(KY):
        R[ky]["soi"] = [("v1", R[ky]["v1"]), ("v1 + SL nến đóng", qc[4][1 + i]), ("v1 + TP Fibo", qc[5][1 + i]), ("v2", R[ky]["v2"])]
    for nhan, a5, a6 in qc:
        print(f"  {nhan:45s} 2025 {a5['so_du'] - VON0:+7.0f}$ ({len(a5['lenh'])}) | 2026 {a6['so_du'] - VON0:+7.0f}$ ({len(a6['lenh'])})")
    R["tu_kiem_tom"] = "\n".join(tom_tat)
    (GOC / "tu_kiem_v2.txt").write_text("\n".join(tom_tat) + "\n" + "\n".join(out) + "\n")
    print("\n".join(tom_tat))
    (GOC / "KET_QUA_V2.md").write_text(lam_bao_cao(R))
    C.cau_hinh(tu="2026-01-01", den="2026-10-30", thu_muc_du_lieu=GOC / "du_lieu")
    print("✓ Đã ghi KET_QUA_V2.md, lenh_v1_/lenh_v2_2025|2026.csv, tu_kiem_v2.txt")


if __name__ == "__main__":
    main()
