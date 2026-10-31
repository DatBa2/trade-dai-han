#!/usr/bin/env python3
"""BACKTEST CƠ HỌC — "bot bắt chước" người phân tích BTC kênh FAM Trading.

Một lệnh chạy lại toàn bộ:   python3 backtest/chay.py            (dùng CSV có sẵn trong du_lieu/)
                             python3 backtest/chay.py --tai-lai  (tải lại nến rồi chạy)
Chạy tùy chọn (không đụng KET_QUA.md), vd ngoài mẫu 2025:
    python3 backtest/chay.py --tu 2025-01-01 --den 2025-12-31 --tai-san BTC,ETH,OKB,BNB,VANG,DAU \
        --dien-giai gia|thoi_gian --thu-muc-du-lieu backtest/du_lieu_2025 [--ra THƯ_MỤC]
Báo cáo ngoài mẫu đầy đủ: python3 backtest/ngoai_mau.py

Mọi tham số CHỐT TRƯỚC theo đặc tả (không tối ưu). Chỉ dùng dữ liệu có trước thời điểm quyết định:
EMA là đệ quy nhân quả, đỉnh/đáy fractal chỉ dùng khi đã đủ 3 nến bên phải, D1 chỉ lấy nến đã đóng
trước giờ quyết định. Có kiểm tra cắt cụt dữ liệu (tu_kiem) để chứng minh không nhìn trước.
Đầu ra: lenh_A..E.csv, KET_QUA.md (giữ nguyên đoạn nhận xét viết tay), von.html, tu_kiem.txt.
"""
import bisect, csv, datetime as dt, json, random, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parent
DL = GOC / "du_lieu"
DIEN_GIAI = "gia"   # luật 8: "gia" = đỉnh/đáy fractal gần giá vào nhất THEO GIÁ (bản chốt); "thoi_gian" = mới nhất THEO THỜI GIAN (bản chạy đầu)
UTC = dt.timezone.utc
VN = dt.timezone(dt.timedelta(hours=7))
NGAY = 86400

# ---------------- THAM SỐ (chốt trước) ----------------
BAT_DAU = int(dt.datetime(2026, 1, 1, 0, 0, tzinfo=VN).timestamp())    # = 2025-12-31 17:00 UTC
KET_THUC = int(dt.datetime(2026, 10, 31, 0, 0, tzinfo=VN).timestamp())  # hết ngày 30/10 giờ VN
VON0 = 4000.0
PHI_VAO, PHI_RA = 0.0002, 0.0005
D_MIN = {"BTC": .012, "ETH": .012, "NEAR": .02, "ZEC": .02, "OKB": .02, "BNB": .02, "VANG": .008, "DAU": .015}
TEN = {"BTC": "BTC", "ETH": "ETH", "NEAR": "NEAR", "ZEC": "ZEC", "OKB": "OKB", "BNB": "BNB", "VANG": "Vàng", "DAU": "Dầu WTI"}
EMA_CHUM = 0.006        # luật 4
HOI_TU = 0.005          # luật 7: ±0,5%
SL_DEM = 0.002          # luật 8: ×1,002
SL_TOI_DA = 0.06        # luật 8
TP_LUI = 0.002          # luật 9: lùi 0,2%
RR_MIN = 1.5            # luật 9
NEN_CHO = 6             # luật 6: lệnh chờ hiệu lực 6 nến H4
NEN_GIU = 18            # luật 10
FRAC = 3                # fractal 3 nến mỗi bên
NGAY_CC, NGAY_XOAY = 30, 60
BAY_MAX, BAY_CHIA = 20, 0.60
SEED, SO_LAN_GD = 20261031, 200
COIN4 = ["BTC", "ETH", "NEAR", "ZEC"]
TAT_CA = COIN4 + ["OKB", "BNB", "VANG", "DAU"]
BIEN_THE = {
    "A": dict(mo_ta="Đúng luật (CHÍNH)", ts=COIN4, rui_ro=.02, loc_d1=True, toi_da=3),
    "B": dict(mo_ta="Bỏ lọc D1 (luật 3)", ts=COIN4, rui_ro=.02, loc_d1=False, toi_da=3),
    "C": dict(mo_ta="Như A, rủi ro 4%/lệnh", ts=COIN4, rui_ro=.04, loc_d1=True, toi_da=3),
    "D": dict(mo_ta="Như A, chỉ BTC+ETH", ts=["BTC", "ETH"], rui_ro=.02, loc_d1=True, toi_da=3),
    "E": dict(mo_ta="Luật A, 8 tài sản, tối đa 4 lệnh", ts=TAT_CA, rui_ro=.02, loc_d1=True, toi_da=4),
}


def ngay_vn(s):
    """'YYYY-MM-DD' → timestamp 00:00 giờ VN của ngày đó."""
    return int(dt.datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=VN).timestamp())


def cau_hinh(tu=None, den=None, thu_muc_du_lieu=None, dien_giai=None):
    """Đổi giai đoạn thi / thư mục dữ liệu / cách diễn giải luật 8. Không truyền gì = giữ mặc định (lần chạy 2026 gốc).
    tu, den: 'YYYY-MM-DD' (giờ VN, tính trọn ngày `den`: kết thúc lúc 00:00 VN ngày hôm sau)."""
    global BAT_DAU, KET_THUC, DL, DIEN_GIAI
    if tu:
        BAT_DAU = ngay_vn(tu)
    if den:
        KET_THUC = ngay_vn(den) + NGAY
    if thu_muc_du_lieu:
        DL = Path(thu_muc_du_lieu).resolve()
    if dien_giai:
        assert dien_giai in ("gia", "thoi_gian"), dien_giai
        DIEN_GIAI = dien_giai


def bien_the_tuy_chon(ds_ts):
    """Bộ biến thể khi chọn tài sản bằng --tai-san: A (rủi ro 2%, tối đa 3 lệnh) và E' (như A, tối đa 4 lệnh)."""
    n = len(ds_ts)
    return {"A": dict(mo_ta=f"Luật v1, {n} tài sản, tối đa 3 lệnh", ts=ds_ts, rui_ro=.02, loc_d1=True, toi_da=3),
            "E'": dict(mo_ta=f"Luật v1, {n} tài sản, tối đa 4 lệnh", ts=ds_ts, rui_ro=.02, loc_d1=True, toi_da=4)}


def vn(ts):
    return dt.datetime.fromtimestamp(ts, VN).strftime("%Y-%m-%d %H:%M")


def thang(ts):
    return dt.datetime.fromtimestamp(ts, VN).strftime("%Y-%m")


def thu_hai(ts):
    return dt.datetime.fromtimestamp(ts, VN).weekday() == 0


def g(x):
    return float(f"{x:.6g}")


def ema(xs, n):
    """EMA chuẩn (α = 2/(n+1)), khởi tạo bằng SMA n giá trị đầu; trước đó = None."""
    ra, a = [None] * len(xs), 2 / (n + 1)
    if len(xs) < n:
        return ra
    v = sum(xs[:n]) / n
    ra[n - 1] = v
    for i in range(n, len(xs)):
        v = a * xs[i] + (1 - a) * v
        ra[i] = v
    return ra


def doc_csv(p):
    ds = []
    with p.open() as f:
        for r in csv.DictReader(f):
            mo = int(dt.datetime.strptime(r["mo_utc"], "%Y-%m-%d %H:%M").replace(tzinfo=UTC).timestamp())
            dg = int(dt.datetime.strptime(r["dong_utc"], "%Y-%m-%d %H:%M").replace(tzinfo=UTC).timestamp())
            ds.append((mo, dg, float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])))
    return ds


class TaiSan:
    def __init__(self, ma, h4, d1):
        self.ma = ma
        self.mo = [r[0] for r in h4]; self.dong = [r[1] for r in h4]
        self.o = [r[2] for r in h4]; self.h = [r[3] for r in h4]; self.l = [r[4] for r in h4]; self.c = [r[5] for r in h4]
        self.chi_so = {t: i for i, t in enumerate(self.dong)}
        self.e34h, self.e34l, self.e34c = ema(self.h, 34), ema(self.l, 34), ema(self.c, 34)
        self.e89, self.e200 = ema(self.c, 89), ema(self.c, 200)
        self.d_dong = [r[1] for r in d1]; self.d_c = [r[5] for r in d1]
        self.d_e34h, self.d_e34l = ema([r[3] for r in d1], 34), ema([r[4] for r in d1], 34)
        self.d_e89, self.d_e200 = ema(self.d_c, 89), ema(self.d_c, 200)
        # nến D1 đã đóng gần nhất tại giờ đóng của từng nến H4
        self.d1i = [bisect.bisect_right(self.d_dong, t) - 1 for t in self.dong]
        # xu hướng H4 (luật 1)
        self.xu = []
        for i in range(len(self.c)):
            if self.e200[i] is None:
                self.xu.append(0); continue
            c = self.c[i]
            if c < self.e34l[i] and c < self.e89[i] and c < self.e200[i]:
                self.xu.append(-1)
            elif c > self.e34h[i] and c > self.e89[i] and c > self.e200[i]:
                self.xu.append(1)
            else:
                self.xu.append(0)
        # đỉnh/đáy fractal 3 nến mỗi bên (trái: lớn hơn hẳn; phải: không bị vượt) — xác nhận ở nến i+3
        n = len(self.c)
        self.dinh, self.day = [], []
        for i in range(FRAC, n - FRAC):
            if self.h[i] > max(self.h[i - FRAC:i]) and self.h[i] >= max(self.h[i + 1:i + 1 + FRAC]):
                self.dinh.append((i, self.h[i]))
            if self.l[i] < min(self.l[i - FRAC:i]) and self.l[i] <= min(self.l[i + 1:i + 1 + FRAC]):
                self.day.append((i, self.l[i]))
        self.dinh_i = [i for i, _ in self.dinh]; self.day_i = [i for i, _ in self.day]

    def xoay(self, loai, t, so_ngay):
        """Điểm xoay ĐÃ XÁC NHẬN tại nến t (i + 3 ≤ t), nằm trong `so_ngay` ngày gần nhất."""
        ds, idx = (self.dinh, self.dinh_i) if loai == "dinh" else (self.day, self.day_i)
        hi = bisect.bisect_right(idx, t - FRAC)
        moc = self.dong[t] - so_ngay * NGAY
        return [(i, p) for i, p in ds[:hi] if self.dong[i] >= moc]


def nap(ma):
    return TaiSan(ma, doc_csv(DL / f"{ma}_4H.csv"), doc_csv(DL / f"{ma}_1D.csv"))


# ---------------- LUẬT: quyết định tại lúc nến H4 t đóng ----------------
def quyet_dinh(a, t, loc_d1=True):
    """Trả (lý do, lệnh chờ hoặc None). Chỉ đọc dữ liệu tới nến t."""
    x = a.xu[t]
    if x == 0 or t < 1 or a.xu[t - 1] != x:
        return "khong_tin_hieu", None                      # luật 1 + 2
    k = a.d1i[t]
    if loc_d1:                                              # luật 3
        if k < 0 or a.d_e34h[k] is None:
            return "loc_d1", None
        if x < 0 and not a.d_c[k] < a.d_e34h[k]:
            return "loc_d1", None
        if x > 0 and not a.d_c[k] > a.d_e34l[k]:
            return "loc_d1", None
    bo = (a.e34c[t], a.e89[t], a.e200[t])                    # luật 4
    if (max(bo) - min(bo)) / a.c[t] < EMA_CHUM:
        return "ema_chum", None
    if thu_hai(a.dong[t]):                                  # luật 5
        return "thu_hai", None
    vao = a.e34l[t] if x < 0 else a.e34h[t]                 # luật 6
    lo, hi = vao * (1 - HOI_TU), vao * (1 + HOI_TU)
    cc = []                                                 # luật 7
    if lo <= a.e89[t] <= hi: cc.append("EMA89")
    if lo <= a.e200[t] <= hi: cc.append("EMA200")
    gan = [(i, p) for i, p in a.xoay("dinh", t, NGAY_CC) + a.xoay("day", t, NGAY_CC) if lo <= p <= hi]
    if gan:
        cc.append("Fractal")
    dau = a.xoay("dinh" if x < 0 else "day", t, NGAY_XOAY)
    fib = None
    if dau:
        i0, p0 = dau[-1]
        cuoi = min(a.l[i0 + 1:t + 1]) if x < 0 else max(a.h[i0 + 1:t + 1])
        fib = (i0, p0, cuoi)
        for r in (0.5, 0.618):
            if lo <= cuoi + r * (p0 - cuoi) <= hi:
                cc.append(f"Fibo{r}")
    if not cc:
        return "khong_hoi_tu", None
    d = D_MIN[a.ma]                                         # luật 8
    if x < 0:
        tren = [(i, p) for i, p in a.xoay("dinh", t, NGAY_XOAY) if p > vao]
        if DIEN_GIAI == "gia":
            nguon = min(tren, key=lambda e: (e[1], -e[0])) if tren else None   # gần nhất THEO GIÁ phía trên giá vào
        else:
            nguon = max(tren, key=lambda e: e[0]) if tren else None            # mới nhất THEO THỜI GIAN phía trên giá vào
        goc = max(nguon[1], vao * (1 + d)) if nguon else vao * (1 + d)
        sl = goc * (1 + SL_DEM)
    else:
        duoi = [(i, p) for i, p in a.xoay("day", t, NGAY_XOAY) if p < vao]
        if DIEN_GIAI == "gia":
            nguon = max(duoi, key=lambda e: (e[1], e[0])) if duoi else None    # gần nhất THEO GIÁ phía dưới giá vào
        else:
            nguon = max(duoi, key=lambda e: e[0]) if duoi else None            # mới nhất THEO THỜI GIAN phía dưới giá vào
        goc = min(nguon[1], vao * (1 - d)) if nguon else vao * (1 - d)
        sl = goc * (1 - SL_DEM)
    sl_nguon = "fractal" if nguon and goc == nguon[1] else "san_dmin"
    sl_pct = abs(sl - vao) / vao
    if sl_pct > SL_TOI_DA:
        return "sl_qua_xa", None
    # luật 9 — đích: điểm xoay phía bên kia, còn ở phía trước giá đóng hiện tại (chưa bị phá), gần nhất theo giá
    if x < 0:
        ung = sorted({p for i, p in a.xoay("day", t, NGAY_XOAY) if p < a.c[t]}, reverse=True)
    else:
        ung = sorted({p for i, p in a.xoay("dinh", t, NGAY_XOAY) if p > a.c[t]})
    if not ung:
        return "khong_co_dich", None
    tp1 = ung[0] * (1 + TP_LUI) if x < 0 else ung[0] * (1 - TP_LUI)
    if len(ung) > 1:
        tp2 = ung[1] * (1 + TP_LUI) if x < 0 else ung[1] * (1 - TP_LUI)
        tp2_nguon = "xoay_ke_tiep"
    else:
        tp2 = vao + x * 3 * abs(sl - vao)
        tp2_nguon = "3R"
        if (tp2 - tp1) * x <= 0:          # 3R chưa qua TP1 → đóng hết ở TP1
            tp2, tp2_nguon = tp1, "=TP1"
    rr = abs(tp1 - vao) / abs(sl - vao)
    if rr < RR_MIN:
        return "rr_thap", None
    return "dat_lenh", dict(ma=a.ma, chieu=x, t=t, vao=vao, sl=sl, sl_pct=sl_pct, tp1=tp1, tp2=tp2, rr=rr,
                            cc=cc, sl_nguon=sl_nguon, tp2_nguon=tp2_nguon,
                            sl_xoay=(nguon[0], nguon[1]) if nguon else None, tp1_xoay=ung[0], fib=fib)


# ---------------- MÔ PHỎNG DANH MỤC ----------------
class ViThe:
    pass


def cham(gia_muc, x, h, l, chieu_bat_loi):
    """chieu_bat_loi=True: mức nằm phía bất lợi (SL); False: phía có lợi (TP)."""
    if (x < 0) == chieu_bat_loi:     # short-SL hoặc long-TP: cần giá lên tới mức
        return h >= gia_muc
    return l <= gia_muc


def gia_thoat(muc, x, o, bat_loi):
    """Khớp ở mức; nếu nến mở cửa đã vượt mức (gap) thì khớp ở giá mở cửa."""
    if bat_loi:
        return max(muc, o) if x < 0 else min(muc, o)
    return min(muc, o) if x < 0 else max(muc, o)


def thoat(p, ti_le, gia, ts, so_du_ref):
    q = p.kl * ti_le
    lai = q * (gia - p.gia_khop) * p.chieu
    phi = q * gia * PHI_RA
    p.con -= ti_le
    p.lai += lai - phi; p.phi += phi
    so_du_ref[0] += lai - phi
    p.dong_ts = ts


def xu_ly_nen(p, a, k, so_du, nen_khop=False):
    """Diễn biến trong nến k của vị thế p. Trả True nếu đã đóng hết."""
    o, h, l, x = a.o[k], a.h[k], a.l[k], p.chieu
    ts = a.dong[k]
    if cham(p.sl, x, h, l, True):                          # luật 11: SL trước
        thoat(p, p.con, gia_thoat(p.sl, x, o, True), ts, so_du)
        p.kq += "SL" if not p.tp1_xong else "HV"
        return True
    if nen_khop:
        return False                                        # nến khớp: không tính TP (không biết thứ tự)
    if not p.tp1_xong and cham(p.tp1, x, h, l, False):
        if p.tp2 == p.tp1:
            thoat(p, p.con, gia_thoat(p.tp1, x, o, False), ts, so_du); p.kq += "TP1(hết)"; return True
        thoat(p, 0.5, gia_thoat(p.tp1, x, o, False), ts, so_du)
        p.tp1_xong, p.sl, p.kq = True, p.vao, "TP1+"
        if cham(p.sl, x, h, l, True):                      # cùng nến chạm lại giá vào → bảo thủ: hòa vốn
            thoat(p, p.con, p.sl, ts, so_du); p.kq += "HV"; return True
    if p.tp1_xong and cham(p.tp2, x, h, l, False):
        thoat(p, p.con, gia_thoat(p.tp2, x, o, False), ts, so_du); p.kq += "TP2"; return True
    return False


def mo_phong(ten, ts_ds, rui_ro, loc_d1, toi_da, TS):
    tai = [TS[m] for m in ts_ds]
    moc = sorted({t for a in tai for t in a.dong if BAT_DAU <= t <= KET_THUC})
    so_du = [VON0]
    vithe, cho, lenh, pheu, huy = {}, {}, [], Counter(), Counter()
    von = []
    for T in moc:
        nen = [(a, a.chi_so[T]) for a in tai if T in a.chi_so]
        # 1) diễn biến vị thế đang mở
        for a, k in nen:
            p = vithe.get(a.ma)
            if p and xu_ly_nen(p, a, k, so_du):
                lenh.append(p); del vithe[a.ma]
        # 2) lệnh chờ: khớp hay hủy do chạm TP1 trước
        for a, k in nen:
            q = cho.get(a.ma)
            if not q:
                continue
            x = q["chieu"]
            toi_vao = a.h[k] >= q["vao"] if x < 0 else a.l[k] <= q["vao"]
            if toi_vao and not thu_hai(T):
                del cho[a.ma]
                if len(vithe) >= toi_da:
                    huy["du_lenh_mo"] += 1; continue
                rr_usd = rui_ro * so_du[0]
                gtvt = rr_usd / q["sl_pct"]
                bay = min(BAY_MAX, BAY_CHIA / q["sl_pct"])
                kha_dung = so_du[0] - sum(v.ky_quy for v in vithe.values())
                if gtvt / bay > kha_dung:
                    if kha_dung <= 0:
                        huy["het_ky_quy"] += 1; continue
                    gtvt = kha_dung * bay; rr_usd = gtvt * q["sl_pct"]; huy["giam_kl_ky_quy"] += 1
                p = ViThe()
                p.__dict__.update(q)
                p.gia_khop = gia_thoat(q["vao"], x, a.o[k], True)  # limit: nếu giá mở cửa đã vượt qua mức thì khớp ở giá mở (tốt hơn)
                p.k_khop, p.khop_ts, p.sl0 = k, T, q["sl"]   # sl0 = SL ban đầu (p.sl sẽ dời về giá vào sau TP1)
                p.kl = gtvt / p.gia_khop; p.gtvt = gtvt; p.bay = bay; p.ky_quy = gtvt / bay; p.rui_ro_usd = rr_usd
                p.con, p.lai, p.phi, p.tp1_xong, p.kq = 1.0, 0.0, 0.0, False, ""
                phi = gtvt * PHI_VAO
                so_du[0] -= phi; p.lai -= phi; p.phi += phi
                vithe[a.ma] = p
                if xu_ly_nen(p, a, k, so_du, nen_khop=True):
                    lenh.append(p); del vithe[a.ma]
            elif (a.l[k] <= q["tp1"]) if x < 0 else (a.h[k] >= q["tp1"]):
                del cho[a.ma]; huy["cham_tp1_truoc"] += 1
        # 3) đóng nến: hết hạn vị thế, hủy lệnh chờ
        for a, k in nen:
            p = vithe.get(a.ma)
            if p and k - p.k_khop >= NEN_GIU:
                thoat(p, p.con, a.c[k], T, so_du); p.kq += "Hết hạn"
                lenh.append(p); del vithe[a.ma]
            q = cho.get(a.ma)
            if q:
                if a.xu[k] != q["chieu"]:
                    del cho[a.ma]; huy["mat_xu_huong"] += 1
                elif k - q["t"] >= NEN_CHO:
                    del cho[a.ma]; huy["het_han_cho"] += 1
        # 4) tín hiệu mới
        for a, k in nen:
            if a.ma in vithe or a.ma in cho:
                continue
            ly_do, q = quyet_dinh(a, k, loc_d1)
            pheu[ly_do] += 1
            if q:
                q["tin_hieu_ts"] = T
                cho[a.ma] = q
        # vốn theo giá thị trường
        mtm = so_du[0]
        for m, p in vithe.items():
            a = TS[m]
            j = bisect.bisect_right(a.dong, T) - 1
            mtm += p.kl * p.con * (a.c[j] - p.gia_khop) * p.chieu
        von.append((T, mtm))
    for m, p in list(vithe.items()):                       # cuối kỳ: đóng ở giá đóng cuối cùng
        a = TS[m]
        j = bisect.bisect_right(a.dong, KET_THUC) - 1
        thoat(p, p.con, a.c[j], a.dong[j], so_du); p.kq += "Cuối kỳ"
        lenh.append(p)
    von[-1] = (von[-1][0], so_du[0])
    for p in lenh:
        p.R = p.lai / p.rui_ro_usd
    lenh.sort(key=lambda p: p.khop_ts)
    return dict(ten=ten, lenh=lenh, von=von, so_du=so_du[0], pheu=pheu, huy=huy)


# ---------------- GIẢ DƯỢC ----------------
def mot_lenh_gia(a, k, x, sl_pct, tp1_pct, tp2_pct):
    """Vào lệnh ở giá đóng nến k, chiều x, cùng khoảng SL/TP và cơ chế quản lý. Trả (giá vào, [(ts, tỉ lệ, giá)])."""
    vao = a.c[k]
    sl, tp1, tp2 = vao * (1 - x * sl_pct), vao * (1 + x * tp1_pct), vao * (1 + x * tp2_pct)
    con, tp1_xong, ra = 1.0, False, []
    j_cuoi = bisect.bisect_right(a.dong, KET_THUC) - 1
    for j in range(k + 1, min(k + NEN_GIU, j_cuoi) + 1):
        o, h, l, ts = a.o[j], a.h[j], a.l[j], a.dong[j]
        if cham(sl, x, h, l, True):
            ra.append((ts, con, gia_thoat(sl, x, o, True))); return vao, ra
        if not tp1_xong and cham(tp1, x, h, l, False):
            if tp2 == tp1:
                ra.append((ts, con, gia_thoat(tp1, x, o, False))); return vao, ra
            ra.append((ts, 0.5, gia_thoat(tp1, x, o, False))); con, tp1_xong, sl = 0.5, True, vao
            if cham(sl, x, h, l, True):
                ra.append((ts, con, sl)); return vao, ra
        if tp1_xong and cham(tp2, x, h, l, False):
            ra.append((ts, con, gia_thoat(tp2, x, o, False))); return vao, ra
    j = min(k + NEN_GIU, j_cuoi)
    ra.append((a.dong[j], con, a.c[j]))
    return vao, ra


def gia_duoc(kq, TS, rui_ro, seed):
    rng = random.Random(seed)
    nen_thang = defaultdict(list)
    for m in {p.ma for p in kq["lenh"]}:
        a = TS[m]
        for k, t in enumerate(a.dong):
            if BAT_DAU <= t < KET_THUC and k + 1 < len(a.dong) and a.dong[k + 1] <= KET_THUC:  # còn ít nhất 1 nến sau
                nen_thang[(m, thang(t))].append(k)
    lai_ds, r_ds = [], []
    for _ in range(SO_LAN_GD):
        su_kien = []
        for n, p in enumerate(kq["lenh"]):
            a = TS[p.ma]
            k = rng.choice(nen_thang[(p.ma, thang(p.khop_ts))])
            x = rng.choice((-1, 1))
            tp1_pct = abs(p.tp1 - p.vao) / p.vao; tp2_pct = abs(p.tp2 - p.vao) / p.vao
            vao, ra = mot_lenh_gia(a, k, x, p.sl_pct, tp1_pct, tp2_pct)
            su_kien.append((a.dong[k], 1, n, vao, x, p.sl_pct, None))
            for ts, tl, gia in ra:
                su_kien.append((ts, 0, n, gia, x, tl, None))
        su_kien.sort(key=lambda e: (e[0], e[1]))
        so_du, mo, tong_r = VON0, {}, 0.0
        for ts, loai, n, gia, x, v, _ in su_kien:
            if loai == 1:
                rr = rui_ro * so_du; gt = rr / v
                mo[n] = [gt / gia, gia, rr, -gt * PHI_VAO]
                so_du -= gt * PHI_VAO
            else:
                kl, vao, rr, lai = mo[n]
                d = kl * v * (gia - vao) * x - kl * v * gia * PHI_RA
                so_du += d; mo[n][3] += d
        for n, (kl, vao, rr, lai) in mo.items():
            tong_r += lai / rr
        lai_ds.append(so_du - VON0); r_ds.append(tong_r)
    return lai_ds, r_ds


def phan_vi(ds, x):
    return 100 * (sum(1 for v in ds if v < x) + 0.5 * sum(1 for v in ds if v == x)) / len(ds)


def q(ds, p):
    s = sorted(ds); i = (len(s) - 1) * p; lo = int(i)
    return s[lo] + (s[min(lo + 1, len(s) - 1)] - s[lo]) * (i - lo)


# ---------------- THỐNG KÊ ----------------
def sut_giam(von):
    dinh, mx = -1e18, 0.0
    for _, v in von:
        dinh = max(dinh, v); mx = max(mx, (dinh - v) / dinh)
    return mx


def thong_ke(lenh):
    n = len(lenh)
    if not n:
        return dict(n=0, thang=0, r_tb=0, pf=0, lai=0, tong_r=0)
    duong = sum(p.lai for p in lenh if p.lai > 0); am = -sum(p.lai for p in lenh if p.lai < 0)
    return dict(n=n, thang=sum(p.lai > 0 for p in lenh) / n, r_tb=sum(p.R for p in lenh) / n,
                pf=duong / am if am else float("inf"), lai=sum(p.lai for p in lenh), tong_r=sum(p.R for p in lenh))


def mua_giu(TS, ds, von_moi):
    """Mua lúc bắt đầu (giá đóng H4 cuối cùng trước 01/01 00:00 VN), bán cuối kỳ; phí taker 0,05% mỗi đầu."""
    moc = sorted({t for m in ds for t in TS[m].dong if BAT_DAU <= t <= KET_THUC})
    gia0 = {}
    for m in ds:
        a = TS[m]; gia0[m] = a.c[bisect.bisect_right(a.dong, BAT_DAU) - 1]
    duong = []
    for T in moc:
        v = 0.0
        for m in ds:
            a = TS[m]; j = bisect.bisect_right(a.dong, T) - 1
            v += von_moi * (1 - PHI_RA) * a.c[j] / gia0[m]
        duong.append((T, v))
    duong[-1] = (duong[-1][0], duong[-1][1] * (1 - PHI_RA))
    return duong


# ---------------- TỰ KIỂM ----------------
def cat_cut(ma, t, TS):
    """Dựng lại tài sản chỉ với dữ liệu tới hết nến t (và D1 đã đóng tới lúc đó)."""
    a = TS[ma]
    h4 = [(a.mo[i], a.dong[i], a.o[i], a.h[i], a.l[i], a.c[i]) for i in range(t + 1)]
    d1 = [r for r in doc_csv(DL / f"{ma}_1D.csv") if r[1] <= a.dong[t]]
    return TaiSan(ma, h4, d1)


def kiem_rang_buoc(KQ, TS, bien_the=None):
    """Kiểm tự động các ràng buộc trên MỌI lệnh của mọi biến thể."""
    loi, dem = [], 0
    for k, kq in KQ.items():
        ds = kq["lenh"]
        for p in ds:
            dem += 1
            a = TS[p.ma]; t, f = p.t, p.k_khop
            if thu_hai(p.khop_ts) or thu_hai(p.tin_hieu_ts): loi.append(f"{k} {p.ma} {vn(p.khop_ts)}: thứ Hai")
            if not (f > t and f - t <= NEN_CHO): loi.append(f"{k} {p.ma}: khớp ngoài 6 nến")
            if not (BAT_DAU <= p.tin_hieu_ts <= KET_THUC): loi.append(f"{k} {p.ma}: tín hiệu ngoài kỳ")
            if (a.h[f] < p.vao) if p.chieu < 0 else (a.l[f] > p.vao): loi.append(f"{k} {p.ma} {vn(p.khop_ts)}: nến khớp không chạm giá vào")
            for j in range(t + 1, f):
                if (a.h[j] >= p.vao and not thu_hai(a.dong[j])) if p.chieu < 0 else (a.l[j] <= p.vao and not thu_hai(a.dong[j])):
                    loi.append(f"{k} {p.ma}: lẽ ra khớp sớm hơn")
                if (a.l[j] <= p.tp1) if p.chieu < 0 else (a.h[j] >= p.tp1):
                    loi.append(f"{k} {p.ma}: đã chạm TP1 trước khi khớp mà không hủy")
            if p.sl_pct < D_MIN[p.ma] - 1e-12 or p.sl_pct > SL_TOI_DA: loi.append(f"{k} {p.ma}: SL% sai")
            if p.rr < RR_MIN: loi.append(f"{k} {p.ma}: R:R < 1,5")
            if (p.dong_ts - p.khop_ts) > NEN_GIU * 4 * 3600 * 4: loi.append(f"{k} {p.ma}: giữ quá lâu")
        for i, x in enumerate(ds):
            dang_mo = [y for j, y in enumerate(ds) if j != i and y.khop_ts <= x.khop_ts < y.dong_ts]
            if len(dang_mo) + 1 > (bien_the or BIEN_THE)[k]["toi_da"]: loi.append(f"{k}: quá số lệnh mở lúc {vn(x.khop_ts)}")
            if any(y.ma == x.ma for y in dang_mo): loi.append(f"{k}: 2 lệnh cùng tài sản {x.ma} lúc {vn(x.khop_ts)}")
    return dem, loi


def tu_kiem(TS, KQ, ds_ts=None, bien_the=None, doi_chieu_ema=True):
    ds_ts = ds_ts or TAT_CA
    kq_A = KQ["A"]
    out = []
    rng = random.Random(SEED)
    tong = khop = 0
    for m in ds_ts:
        a = TS[m]
        ung = [k for k in range(len(a.dong)) if BAT_DAU <= a.dong[k] <= KET_THUC and a.xu[k] != 0 and a.xu[k] == a.xu[k - 1]]
        dat = [k for k in ung if quyet_dinh(a, k)[0] == "dat_lenh"]
        mau = rng.sample(dat, min(8, len(dat))) + rng.sample(ung, min(7, len(ung)))
        for k in mau:
            b = cat_cut(m, k, TS)
            tong += 1
            r1, r2 = quyet_dinh(a, k), quyet_dinh(b, k)
            if r1[0] == r2[0] and (r1[1] is None or all(abs(r1[1][f] - r2[1][f]) < 1e-9 * abs(r1[1][f]) for f in ("vao", "sl", "tp1", "tp2"))
                                   and r1[1]["cc"] == r2[1]["cc"]):
                khop += 1
            else:
                out.append(f"!! LỆCH {m} {vn(a.dong[k])}: {r1} vs {r2}")
    out.insert(0, f"Kiểm không nhìn trước: dựng lại chỉ báo với dữ liệu CẮT CỤT tại nến quyết định cho {tong} mẫu "
                  f"({len(ds_ts)} tài sản) → {khop}/{tong} cho cùng quyết định/giá vào/SL/TP/căn cứ.")
    dem, loi = kiem_rang_buoc(KQ, TS, bien_the)
    out.insert(1, f"Kiểm ràng buộc trên {dem} lệnh ({'A–E' if bien_the is None else '/'.join(KQ)}): không khớp/tín hiệu thứ Hai; khớp trong 6 nến và nến khớp có chạm giá vào; "
                  f"không có nến nào trước đó lẽ ra đã khớp hoặc đã chạm TP1; SL% trong [d_min, 6%]; R:R ≥ 1,5; "
                  f"không quá số lệnh mở; không 2 lệnh cùng tài sản → {len(loi)} lỗi." + ("".join("\n  !! " + e for e in loi[:20])))
    # lệnh mẫu đối chiếu tay
    lenh = kq_A["lenh"]
    rng2 = random.Random(SEED + 1)
    mau = sorted(rng2.sample(range(len(lenh)), min(4, len(lenh))))
    for n in mau:
        p = lenh[n]; a = TS[p.ma]; t = p.t; x = p.chieu
        out.append("")
        out.append(f"=== Lệnh mẫu #{n + 1}: {p.ma} {'SHORT' if x < 0 else 'LONG'} — tín hiệu {vn(a.dong[t])} VN, khớp {vn(p.khop_ts)}, kết quả {p.kq}, R={p.R:.2f}")
        for j in (t - 1, t):
            out.append(f"  nến H4 đóng {vn(a.dong[j])}: O={g(a.o[j])} H={g(a.h[j])} L={g(a.l[j])} C={g(a.c[j])} | EMA34 cao={g(a.e34h[j])} thấp={g(a.e34l[j])} đóng={g(a.e34c[j])} EMA89={g(a.e89[j])} EMA200={g(a.e200[j])} → xu={a.xu[j]}")
        k = a.d1i[t]
        out.append(f"  D1 đã đóng gần nhất: đóng lúc {vn(a.d_dong[k])} VN, close={g(a.d_c[k])}, EMA34 cao={g(a.d_e34h[k])} thấp={g(a.d_e34l[k])}")
        bo = (a.e34c[t], a.e89[t], a.e200[t])
        out.append(f"  độ chụm EMA = {(max(bo) - min(bo)) / a.c[t] * 100:.2f}% (cần ≥0,6%); thứ {dt.datetime.fromtimestamp(a.dong[t], VN).isoweekday() + 1 if dt.datetime.fromtimestamp(a.dong[t], VN).isoweekday() < 7 else 'CN'}")
        out.append(f"  giá vào = {'EMA34 thấp' if x < 0 else 'EMA34 cao'} = {g(p.vao)}; căn cứ: {', '.join(p.cc)}")
        if p.fib:
            i0, p0, cuoi = p.fib
            out.append(f"  nhịp Fibo: đầu {'đỉnh' if x < 0 else 'đáy'} {g(p0)} ({vn(a.dong[i0])}, xác nhận {vn(a.dong[i0 + 3])}) → cực trị {g(cuoi)}; 0.5={g(cuoi + .5 * (p0 - cuoi))} 0.618={g(cuoi + .618 * (p0 - cuoi))}")
        if p.sl_xoay:
            i0, p0 = p.sl_xoay
            out.append(f"  SL: {'đỉnh' if x < 0 else 'đáy'} fractal gần nhất {g(p0)} ({vn(a.dong[i0])}, xác nhận {vn(a.dong[i0 + 3])}); sàn d_min → {p.sl_nguon}; SL={g(p.sl0)} ({p.sl_pct * 100:.2f}%)")
        else:
            out.append(f"  SL: không có fractal phía {'trên' if x < 0 else 'dưới'} → sàn d_min; SL={g(p.sl0)} ({p.sl_pct * 100:.2f}%)")
        out.append(f"  TP1={g(p.tp1)} (từ điểm xoay {g(p.tp1_xoay)}), TP2={g(p.tp2)} ({p.tp2_nguon}), R:R TP1={p.rr:.2f}")
        for j in range(t + 1, min(p.k_khop + NEN_GIU, len(a.c) - 1) + 1):
            dau = "KHỚP→" if j == p.k_khop else ("      " if j < p.k_khop else "  giữ ")
            out.append(f"   {dau} {vn(a.dong[j])} O={g(a.o[j])} H={g(a.h[j])} L={g(a.l[j])} C={g(a.c[j])}")
            if a.dong[j] >= p.dong_ts:
                break
        out.append(f"  đóng lúc {vn(p.dong_ts)}; lãi {p.lai:+.2f}$ (phí {p.phi:.2f}$), khối lượng {g(p.gtvt)}$ x{p.bay:.1f}")
    if not doi_chieu_ema:
        return "\n".join(out)
    # mốc EMA đối chiếu với số đo trên ảnh chart (D3 sổ tay): D1 19/01 đường tím ~99,5k (họ tính EMA200 = 99.747)
    a = TS["BTC"]
    k = bisect.bisect_right(a.d_dong, int(dt.datetime(2026, 1, 20, 0, 0, tzinfo=UTC).timestamp())) - 1
    out.append("")
    out.append(f"Đối chiếu EMA200 D1 BTC ngày 19/01: của ta {g(a.d_e200[k])} (sổ tay: ảnh ~99,5k, EMA200 = 99.747). "
               f"Dữ liệu D1 chỉ từ 01/01/2025 nên EMA200 D1 khởi động ngắn; luật chỉ dùng dải EMA34 D1.")
    return "\n".join(out)


# ---------------- XUẤT ----------------
COT = ["tai_san", "chieu", "gio_tin_hieu", "gio_khop", "gio_dong", "gia_vao", "gia_khop", "sl", "sl_pct", "tp1", "tp2",
       "rr_tp1", "can_cu_hoi_tu", "sl_nguon", "tp2_nguon", "don_bay", "gia_tri_vi_the", "rui_ro_usd", "ket_qua", "R", "lai_usd", "phi_usd"]


def ghi_lenh(kq, p_out):
    with p_out.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(COT)
        for p in kq["lenh"]:
            w.writerow([p.ma, "SHORT" if p.chieu < 0 else "LONG", vn(p.tin_hieu_ts), vn(p.khop_ts), vn(p.dong_ts),
                        g(p.vao), g(p.gia_khop), g(p.sl0), round(p.sl_pct * 100, 3), g(p.tp1), g(p.tp2), round(p.rr, 2),
                        "EMA34+" + "+".join(p.cc), p.sl_nguon, p.tp2_nguon, round(p.bay, 1), round(p.gtvt, 2),
                        round(p.rui_ro_usd, 2), p.kq, round(p.R, 3), round(p.lai, 2), round(p.phi, 2)])


def tien(x):
    return f"{x:+,.0f}$".replace(",", ".")


def pct(x, so=1):
    return f"{x * 100:+.{so}f}%".replace(".", ",")


def pct0(x, so=1):
    return f"{x * 100:.{so}f}%".replace(".", ",")


def so(x, n=2):
    return f"{x:.{n}f}".replace(".", ",")


def bang(tieu_de, dong):
    s = "| " + " | ".join(tieu_de) + " |\n|" + "|".join("---" for _ in tieu_de) + "|\n"
    return s + "".join("| " + " | ".join(str(c) for c in d) + " |\n" for d in dong)


def nhom(lenh, khoa):
    d = defaultdict(list)
    for p in lenh:
        d[khoa(p)].append(p)
    return d


DANH_LY_DO = [("khong_tin_hieu", "Không đủ luật 1+2 (xu hướng H4 2 cây)"), ("loc_d1", "Bị lọc D1 (luật 3)"),
              ("ema_chum", "EMA chụm <0,6% (luật 4)"), ("thu_hai", "Thứ Hai (luật 5)"),
              ("khong_hoi_tu", "Thiếu căn cứ hội tụ (luật 7)"), ("sl_qua_xa", "SL >6% (luật 8)"),
              ("khong_co_dich", "Không có đáy/đỉnh làm TP1 (luật 9)"), ("rr_thap", "R:R TP1 <1,5 (luật 9)"),
              ("dat_lenh", "→ ĐẶT LỆNH CHỜ")]
DANH_HUY = [("cham_tp1_truoc", "Hủy: giá chạm TP1 trước khi khớp"), ("mat_xu_huong", "Hủy: mất xu hướng"),
            ("het_han_cho", "Hủy: hết 6 nến chưa khớp"), ("du_lenh_mo", "Hủy: đã đủ lệnh mở"),
            ("het_ky_quy", "Hủy: hết ký quỹ"), ("giam_kl_ky_quy", "Giảm khối lượng vì ký quỹ")]


def lam_bao_cao(KQ, BH, GD, TS, tu_kiem_txt):
    L = []
    w = L.append
    A, E = KQ["A"], KQ["E"]
    w("# KẾT QUẢ BACKTEST CƠ HỌC — bot bắt chước người phân tích BTC (FAM Trading)\n")
    w(f"_Sinh tự động bởi `backtest/chay.py` (chạy lại: `python3 backtest/chay.py`). Giai đoạn thi {vn(BAT_DAU)} → {vn(KET_THUC)} giờ VN · vốn 4.000$ · phí vào 0,02% / ra 0,05% · bỏ funding. "
      "Tài sản A–D: BTC, ETH, NEAR, ZEC (OKX); E thêm OKB, BNB (OKX), vàng GC=F, dầu CL=F (Yahoo)._\n")
    w("> **CẢNH BÁO IN-SAMPLE.** Bộ luật được chắt lọc từ chính các buổi live của năm 2026, tức đúng giai đoạn đang thi. "
      "Kết quả dưới đây là kiểm tra *trong mẫu*: nó cho biết bộ luật cơ học có tái tạo được lợi thế trên giai đoạn mà luật được học hay không, "
      "**không** phải bằng chứng về hiệu quả trong tương lai. Không có tham số nào được dò/tối ưu; chỉ chạy các biến thể A–E đã chốt trước.\n")
    # tổng
    w("## 1. Bảng tổng\n")
    rows = []
    for k, kq in KQ.items():
        st = thong_ke(kq["lenh"])
        gd = GD.get(k)
        rows.append([f"**{k}** — {BIEN_THE[k]['mo_ta']}", tien(kq["so_du"] - VON0), pct(kq["so_du"] / VON0 - 1), st["n"],
                     pct0(st["thang"], 0), so(st["r_tb"]), pct0(sut_giam(kq["von"])), so(st["pf"]) if st["pf"] != float("inf") else "∞",
                     f"{phan_vi(gd[0], kq['so_du'] - VON0):.0f}" if gd else "—"])
    for ten, duong in BH.items():
        rows.append([f"Mua & giữ {ten}", tien(duong[-1][1] - VON0), pct(duong[-1][1] / VON0 - 1), "—", "—", "—", pct0(sut_giam(duong)), "—", "—"])
    w(bang(["Chiến lược", "Lãi/lỗ", "%", "Số lệnh", "Tỉ lệ thắng", "R TB", "Sụt giảm lớn nhất", "Hệ số LN", "Phân vị giả dược"], rows))
    w("\n_R TB = lãi ròng (sau phí) ÷ số tiền rủi ro dự kiến của lệnh. Sụt giảm tính trên vốn theo giá thị trường mỗi nến H4. Mua & giữ: vốn 4.000$ chia đều, mua ở giá đóng H4 cuối trước 01/01 00:00 VN, bán cuối kỳ, phí 0,05% mỗi đầu._\n")
    w("### Giả dược (200 lần, seed cố định)\n")
    rows = []
    for k, (lai, rr) in GD.items():
        kq = KQ[k]; st = thong_ke(kq["lenh"])
        rows.append([k, tien(kq["so_du"] - VON0), tien(q(lai, .05)), tien(q(lai, .5)), tien(q(lai, .95)),
                     pct0(sum(v > 0 for v in lai) / len(lai), 0), f"{phan_vi(lai, kq['so_du'] - VON0):.0f}",
                     so(st["tong_r"], 1), so(q(rr, .5), 1), f"{phan_vi(rr, st['tong_r']):.0f}"])
    w(bang(["Biến thể", "Thật", "Giả dược P5", "P50", "P95", "% lần giả dược lãi", "Phân vị của thật ($)", "Tổng R thật", "Tổng R giả dược P50", "Phân vị (R)"], rows))
    w("\n_Giả dược: giữ đúng số lệnh, tài sản, tháng khớp, khoảng cách SL%/TP1%/TP2% và cơ chế quản lý (50% ở TP1 → dời SL về giá vào, SL trước nếu cùng nến, hết hạn 18 nến) của từng lệnh thật; "
      "chỉ thay thời điểm vào (một nến H4 ngẫu nhiên trong cùng tháng, vào ở giá đóng) và chiều (ngẫu nhiên 50/50). Rủi ro 2% vốn hiện có mỗi lệnh, không giới hạn số lệnh mở. "
      "Phân vị = % số lần giả dược thua kết quả thật._\n")
    # phễu
    w("## 2. Phễu tín hiệu (số lượt đánh giá lúc nến H4 đóng, khi tài sản chưa có lệnh/lệnh chờ)\n")
    rows = []
    for ma, ten in DANH_LY_DO:
        rows.append([ten] + [KQ[k]["pheu"].get(ma, 0) for k in KQ])
    for ma, ten in DANH_HUY:
        rows.append([ten] + [KQ[k]["huy"].get(ma, 0) for k in KQ])
    rows.append(["**Lệnh khớp**"] + [len(KQ[k]["lenh"]) for k in KQ])
    w(bang(["Bước"] + list(KQ), rows))
    w("\n_Luật kiểm theo thứ tự 1→9; mỗi lượt chỉ ghi lý do bị loại ĐẦU TIÊN. Một xu hướng kéo dài sinh tín hiệu ở mọi nến nên các con số là lượt nến, không phải số “cơ hội” độc lập._\n")
    # theo tháng
    w("## 3. Biến thể A theo THÁNG (theo tháng khớp lệnh)\n")
    rows = []
    von_thang = {}
    for T, v in A["von"]:
        von_thang[thang(T)] = v
    truoc = VON0
    g_thang = nhom(A["lenh"], lambda p: thang(p.khop_ts))
    for th in sorted(von_thang):
        ds = g_thang.get(th, [])
        st = thong_ke(ds)
        rows.append([th, st["n"], pct0(st["thang"], 0) if ds else "—", so(st["tong_r"], 1), tien(st["lai"]),
                     f"{von_thang[th]:,.0f}$".replace(",", "."), pct(von_thang[th] / truoc - 1)])
        truoc = von_thang[th]
    w(bang(["Tháng", "Số lệnh", "Thắng", "Tổng R", "Lãi lệnh khớp trong tháng", "Vốn cuối tháng", "Đổi vốn trong tháng"], rows))
    # theo coin
    def bang_ts(kq, ds_ma, ten_bh):
        rows = []
        gm = nhom(kq["lenh"], lambda p: p.ma)
        for m in ds_ma:
            ds = gm.get(m, [])
            st = thong_ke(ds)
            nl = sum(1 for p in ds if p.chieu > 0); ns = st["n"] - nl
            a = TS[m]
            g0 = a.c[bisect.bisect_right(a.dong, BAT_DAU) - 1]; g1 = a.c[bisect.bisect_right(a.dong, KET_THUC) - 1]
            rows.append([TEN[m], st["n"], f"{nl}/{ns}", pct0(st["thang"], 0) if ds else "—", so(st["r_tb"]) if ds else "—",
                         so(st["tong_r"], 1), tien(st["lai"]), pct(g1 / g0 - 1)])
        return bang(["Tài sản", "Số lệnh", "Long/Short", "Thắng", "R TB", "Tổng R", "Lãi/lỗ", "Giá 01/01→30/10 (mua & giữ)"], rows)
    w("\n## 4. Biến thể A theo COIN\n")
    w(bang_ts(A, COIN4, ""))
    w("\n## 5. Biến thể E theo TÀI SẢN (8 tài sản, tối đa 4 lệnh mở)\n")
    w(bang_ts(E, TAT_CA, ""))
    w("\n_Vàng = GC=F, dầu = CL=F (Yahoo, hợp đồng liên tục — có bước nhảy khi chuyển kỳ hạn). Nến H4 gộp từ H1, chỉ giữ nến có ≥3 giờ giao dịch; cuối tuần không có nến._\n")
    # top
    def dong_lenh(p):
        return [vn(p.khop_ts)[:10], TEN[p.ma], "SHORT" if p.chieu < 0 else "LONG", p.kq, so(p.R), tien(p.lai),
                f"SL {so(p.sl_pct * 100)}% ({'sàn d_min' if p.sl_nguon == 'san_dmin' else 'đỉnh/đáy'}), R:R {so(p.rr, 1)}, căn cứ {'+'.join(p.cc)}, giữ {round((p.dong_ts - p.khop_ts) / 3600)} giờ"]
    w("\n## 6. Biến thể A — 5 lệnh lãi nhất / 5 lệnh lỗ nhất\n")
    ds = sorted(A["lenh"], key=lambda p: p.lai)
    w("**Lãi nhất**\n\n" + bang(["Ngày khớp", "Tài sản", "Chiều", "Kết quả", "R", "Lãi", "Chi tiết"], [dong_lenh(p) for p in ds[::-1][:5]]))
    w("\n**Lỗ nhất**\n\n" + bang(["Ngày khớp", "Tài sản", "Chiều", "Kết quả", "R", "Lãi", "Chi tiết"], [dong_lenh(p) for p in ds[:5]]))
    w("\n_Kết quả: SL = chạm cắt lỗ trước TP1; TP1+HV = chốt 50% ở TP1 rồi phần còn lại về hòa vốn; TP1+TP2; Hết hạn = đóng sau 18 nến; TP1(hết) = TP2 trùng TP1 nên đóng hết ở TP1._\n")
    # phân tích
    w("\n## 7. Biến thể A — mổ xẻ theo nhóm\n")
    def bang_nhom(tieu, d):
        rows = []
        for kh in sorted(d, key=str):
            st = thong_ke(d[kh])
            rows.append([kh, st["n"], pct0(st["thang"], 0), so(st["r_tb"]), so(st["tong_r"], 1), tien(st["lai"])])
        return bang([tieu, "Số lệnh", "Thắng", "R TB", "Tổng R", "Lãi/lỗ"], rows)
    for nhan, kq in (("A", A), ("E", E)):
        w(f"**{nhan} — theo chiều**\n\n" + bang_nhom("Chiều", nhom(kq["lenh"], lambda p: "LONG" if p.chieu > 0 else "SHORT")))
        w(f"\n**{nhan} — theo kiểu kết thúc**\n\n" + bang_nhom("Kết quả", nhom(kq["lenh"], lambda p: p.kq)))
        w(f"\n**{nhan} — theo nguồn SL**\n\n" + bang_nhom("Nguồn SL", nhom(kq["lenh"], lambda p: "sàn d_min" if p.sl_nguon == "san_dmin" else "đỉnh/đáy fractal")))
        d = defaultdict(list)
        for p in kq["lenh"]:
            for c in p.cc:
                d[c].append(p)
        w(f"\n**{nhan} — theo căn cứ hội tụ (một lệnh có thể có nhiều căn cứ)**\n\n" + bang_nhom("Căn cứ", d))
        w(f"\n**{nhan} — theo số căn cứ ngoài EMA34**\n\n" + bang_nhom("Số căn cứ", nhom(kq["lenh"], lambda p: f"{len(p.cc)}")))
        w(f"\n**{nhan} — theo R:R tới TP1**\n\n" + bang_nhom("R:R", nhom(kq["lenh"], lambda p: "1,5–2" if p.rr < 2 else ("2–3" if p.rr < 3 else "≥3"))))
        w("")
    # nhận xét giữ nguyên
    w("\n## 8. Nhận xét\n")
    cu = (GOC / "KET_QUA.md").read_text() if (GOC / "KET_QUA.md").exists() else ""
    if "<!-- NHAN_XET -->" in cu and "<!-- /NHAN_XET -->" in cu:
        w(cu[cu.index("<!-- NHAN_XET -->"):cu.index("<!-- /NHAN_XET -->") + len("<!-- /NHAN_XET -->")])
    else:
        w("<!-- NHAN_XET -->\n_(chưa viết)_\n<!-- /NHAN_XET -->")
    w("\n## 9. Cách diễn giải đặc tả (các chỗ đặc tả để ngỏ — chọn một lần, không thử phương án khác)\n")
    w("""- **Fractal**: nến i là đỉnh nếu high[i] > high 3 nến trái và ≥ high 3 nến phải (đáy đối xứng); chỉ dùng từ khi nến i+3 đã đóng.
- **SL**: “đỉnh fractal gần nhất phía trên giá vào” = đỉnh fractal (60 ngày) **gần giá vào nhất theo giá** trong số các đỉnh cao hơn giá vào (LONG: đáy thấp hơn giá vào, gần nhất theo giá) — đọc theo chữ của đặc tả, đồng nhất với cách hiểu TP1. Không có thì dùng sàn d_min. _Minh bạch: lần chạy đầu tiên tôi hiểu là “đỉnh mới nhất theo thời gian” (A ra +136$, +3,4%); đọc lại câu chữ thì đổi sang theo giá và CHỐT luôn cách này trước khi xem kết quả mới — không chạy/so thêm phương án nào khác._
- **TP1**: đáy (SHORT) / đỉnh (LONG) fractal trong 60 ngày, **gần nhất theo giá**, và phải còn ở phía trước giá đóng của nến tín hiệu (đáy đã bị giá đóng xuyên qua coi như đã phá, không làm đích). Không có → bỏ lệnh (“không có đích”). TP2 = điểm xoay cùng loại kế tiếp xa hơn; không có → giá vào ∓ 3×SL; nếu 3×SL chưa qua TP1 thì đóng hết ở TP1.
- **Fibo**: nhịp = điểm xoay đã xác nhận gần nhất ngược chiều lệnh (đỉnh cho SHORT, đáy cho LONG, trong 60 ngày) → cực trị râu kể từ đó tới nến hiện tại; mức = cực trị + r×(đầu − cực trị).
- **Hội tụ**: đỉnh/đáy fractal 30 ngày tính cả đỉnh lẫn đáy; vì ngưỡng chỉ cần ≥1 căn cứ ngoài EMA34 nên đếm theo loại hay theo từng điểm cho cùng kết quả.
- **Thứ Hai** (giờ VN, theo giờ đóng nến H4): không đặt lệnh chờ mới và lệnh chờ cũ cũng **không được khớp** trong các nến đóng vào thứ Hai (vẫn tính vào 6 nến hiệu lực).
- **Một lệnh mỗi tài sản** tính cả lệnh chờ. Giới hạn 3 (E: 4) lệnh mở kiểm lúc khớp; đủ thì hủy lệnh chờ. Vốn để tính rủi ro = số dư đã chốt (gồm phần đã chốt TP1) lúc khớp.
- **Thứ tự trong nến**: (1) vị thế đang mở: SL trước, rồi TP1, TP2; nếu nến chạm TP1 mà cũng chạm lại giá vào → phần còn lại coi như hòa vốn (bảo thủ); (2) lệnh chờ: chạm giá vào → khớp (nến khớp chỉ kiểm SL, không tính TP vì không biết thứ tự); không chạm giá vào mà chạm TP1 → hủy; (3) lúc đóng nến: hết hạn 18 nến (đếm từ nến khớp), hủy lệnh chờ nếu xu hướng H4 không còn hoặc đã qua 6 nến; (4) tín hiệu mới. Nếu giá mở cửa đã vượt mức (gap) thì khớp ở giá mở cửa.
- **ZEC-USDT** chỉ có trên OKX từ 24/11/2025 → EMA200 H4 bắt đầu có từ ~27/12/2025, khởi động ngắn trong tháng 1. Vàng/dầu: D1 Yahoo, giờ đóng = 17:00 New York.
- Cuối kỳ (00:00 VN 31/10) lệnh còn mở đóng ở giá đóng nến H4 cuối cùng.
""")
    w("\n## 10. Tự kiểm\n")
    w("```\n" + tu_kiem_txt.split("\n\n=== ")[0] + "\n```\n")
    w("Chi tiết đối chiếu tay từng nến của các lệnh mẫu: `backtest/tu_kiem.txt`.\n")
    return "\n".join(L)


def lam_html(KQ, BH):
    def theo_ngay(duong):
        d = {}
        for T, v in duong:
            d[dt.datetime.fromtimestamp(T, VN).strftime("%Y-%m-%d")] = round(v, 2)
        return d
    chuoi = {f"{k} — {BIEN_THE[k]['mo_ta']}": theo_ngay(KQ[k]["von"]) for k in KQ}
    chuoi.update({f"Mua & giữ {t}": theo_ngay(d) for t, d in BH.items()})
    ngay = sorted(set().union(*[set(v) for v in chuoi.values()]))
    du = {}
    for ten, d in chuoi.items():
        last, arr = None, []
        for n in ngay:
            last = d.get(n, last); arr.append(last)
        du[ten] = arr
    bieu1 = [k for k in du if k[0] in "ABCD"] + ["Mua & giữ giỏ 4 coin", "Mua & giữ BTC"]
    bieu2 = [k for k in du if k.startswith("E")] + [k for k in du if k.startswith("A")] + ["Mua & giữ giỏ 8 tài sản"]
    tom = []
    for k, kq in KQ.items():
        st = thong_ke(kq["lenh"])
        tom.append([f"{k} — {BIEN_THE[k]['mo_ta']}", round(kq["so_du"]), round((kq["so_du"] / VON0 - 1) * 100, 1), st["n"], round(sut_giam(kq["von"]) * 100, 1)])
    for t, d in BH.items():
        tom.append([f"Mua & giữ {t}", round(d[-1][1]), round((d[-1][1] / VON0 - 1) * 100, 1), "—", round(sut_giam(d) * 100, 1)])
    mau = {}
    for t in du:   # màu cố định theo thực thể (không theo thứ tự trong từng biểu đồ)
        mau[t] = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 7}.get(t[0], 5 if "4 coin" in t else (6 if "BTC" in t else 8))
    data = json.dumps(dict(ngay=ngay, du=du, b1=bieu1, b2=bieu2, tom=tom, von0=VON0, mau=mau), ensure_ascii=False)
    html = TRANG.replace("__DATA__", data)
    (GOC / "von.html").write_text(html)


TRANG = r"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Đường vốn backtest</title>
<style>
:root{color-scheme:light;--surface:#fcfcfb;--text:#0b0b0b;--text2:#52514e;--muted:#898781;--grid:#e1e0d9;--axis:#c3c2b7;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--s5:#e87ba4;--s6:#008300;--s7:#6250d6;--s8:#e34948}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--surface:#1a1a19;--text:#f0efec;--text2:#c3c2b7;--grid:#2c2c2a;--axis:#383835;
--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s6:#008300;--s7:#9085e9;--s8:#e66767}}
:root[data-theme="dark"]{color-scheme:dark;--surface:#1a1a19;--text:#f0efec;--text2:#c3c2b7;--grid:#2c2c2a;--axis:#383835;
--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s6:#008300;--s7:#9085e9;--s8:#e66767}
body{margin:0;background:var(--surface);color:var(--text);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1100px;margin:0 auto;padding:20px 16px 40px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 6px}
p.ghi{color:var(--text2);margin:0 0 10px;font-size:14px}
.khung{position:relative;height:420px}
table{border-collapse:collapse;width:100%;font-size:14px;margin-top:8px;font-variant-numeric:tabular-nums}
th,td{padding:6px 8px;border-bottom:1px solid var(--grid);text-align:right}th:first-child,td:first-child{text-align:left}
th{color:var(--text2);font-weight:600}
.bang{overflow-x:auto}
</style></head><body><main>
<h1>Đường vốn backtest — bot bắt chước FAM (01/01 → 30/10/2026)</h1>
<p class="ghi">Vốn đầu 4.000$, giá trị theo giá thị trường lúc cuối mỗi ngày (giờ VN). Kết quả TRONG MẪU: luật học từ chính giai đoạn này.</p>
<h2>Biến thể A–D (4 coin) so với mua &amp; giữ</h2>
<p class="ghi">Đường B trùng khít A (lọc D1 không chặn lệnh nào được khớp) nên bị A che. Nét đứt = mua &amp; giữ.</p>
<div class="khung"><canvas id="c1" aria-label="Đường vốn biến thể A đến D và mua giữ"></canvas></div>
<h2>Biến thể E (8 tài sản) so với A và mua &amp; giữ 8 tài sản</h2>
<div class="khung"><canvas id="c2" aria-label="Đường vốn biến thể E"></canvas></div>
<h2>Bảng số cuối kỳ</h2>
<div class="bang"><table id="tb"><thead><tr><th>Chiến lược</th><th>Vốn cuối ($)</th><th>Lãi/lỗ (%)</th><th>Số lệnh</th><th>Sụt giảm lớn nhất (%)</th></tr></thead><tbody></tbody></table></div>
</main>
<script src="vendor/chart.umd.js"></script>
<script>
const D = __DATA__;
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const fmt = v => v == null ? "—" : v.toLocaleString("vi-VN", {maximumFractionDigits: 0}) + "$";
function ve(id, ten) {
  const ds = ten.map((t, i) => ({label: t, data: D.du[t], borderColor: css("--s" + D.mau[t]), backgroundColor: css("--s" + D.mau[t]),
    borderWidth: 2, pointRadius: 0, pointHoverRadius: 5, tension: 0, borderDash: t.startsWith("Mua") ? [6, 4] : []}));
  return new Chart(document.getElementById(id), {type: "line", data: {labels: D.ngay, datasets: ds},
    options: {maintainAspectRatio: false, animation: false, interaction: {mode: "index", intersect: false},
      plugins: {legend: {position: "top", labels: {color: css("--text2"), boxWidth: 14, boxHeight: 2}},
        tooltip: {callbacks: {label: c => " " + c.dataset.label + ": " + fmt(c.parsed.y)}}},
      scales: {x: {ticks: {color: css("--muted"), maxTicksLimit: 10, maxRotation: 0}, grid: {display: false}, border: {color: css("--axis")}},
        y: {ticks: {color: css("--muted"), callback: v => v.toLocaleString("vi-VN")}, grid: {color: css("--grid")}, border: {display: false}}}}});
}
ve("c1", D.b1); ve("c2", D.b2);
const tb = document.querySelector("#tb tbody");
for (const r of D.tom) { const tr = document.createElement("tr");
  tr.innerHTML = r.map((v, i) => `<td>${i == 1 ? v.toLocaleString("vi-VN") : (typeof v === "number" ? v.toLocaleString("vi-VN") : v)}</td>`).join(""); tb.appendChild(tr); }
</script></body></html>
"""


def doc_co(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Backtest luật v1. Không cờ nào = đúng lần chạy 2026 gốc (A–E, 8 tài sản) và ghi KET_QUA.md/von.html. "
                                 "Có cờ tùy chọn = chạy riêng, KHÔNG đụng KET_QUA.md; ghi lenh_*.csv + tu_kiem.txt vào --ra.")
    ap.add_argument("--tai-lai", action="store_true", help="(chỉ chế độ mặc định) tải lại nến vào du_lieu/ rồi chạy")
    ap.add_argument("--tu", help="ngày bắt đầu YYYY-MM-DD, 00:00 giờ VN (mặc định 2026-01-01)")
    ap.add_argument("--den", help="ngày kết thúc YYYY-MM-DD, tính trọn ngày giờ VN (mặc định 2026-10-30)")
    ap.add_argument("--tai-san", help="vd BTC,ETH,OKB,BNB,VANG,DAU → chạy A (2%%, tối đa 3 lệnh) và E' (2%%, tối đa 4 lệnh) trên đúng các tài sản này; "
                                      "bỏ trống = bộ A–E gốc")
    ap.add_argument("--dien-giai", choices=["gia", "thoi_gian"], help="luật 8 — đỉnh/đáy fractal gần nhất theo GIÁ (mặc định) hay mới nhất theo THỜI GIAN")
    ap.add_argument("--thu-muc-du-lieu", help="thư mục CSV nến (mặc định backtest/du_lieu)")
    ap.add_argument("--ra", help="thư mục ghi kết quả khi chạy tùy chọn (mặc định backtest/ngoai_mau/<tu>_<den>_<dien_giai>)")
    return ap.parse_args(argv)


def chay_tuy_chon(ds_ts=None):
    """Chạy theo cấu hình hiện tại (xem cau_hinh). ds_ts=None → bộ A–E gốc; có danh sách → A và E' trên đúng danh sách đó."""
    bt = bien_the_tuy_chon(ds_ts) if ds_ts else BIEN_THE
    ds = ds_ts or TAT_CA
    TS = {m: nap(m) for m in ds}
    KQ = {k: mo_phong(k, c["ts"], c["rui_ro"], c["loc_d1"], c["toi_da"], TS) for k, c in bt.items()}
    BH = {TEN[m]: mua_giu(TS, [m], VON0) for m in ds}
    BH[f"giỏ {len(ds)} tài sản"] = mua_giu(TS, ds, VON0 / len(ds))
    GD = {k: gia_duoc(KQ[k], TS, bt[k]["rui_ro"], SEED) for k in KQ if k in ("A", "E", "E'")}
    tk = tu_kiem(TS, KQ, ds, bt if ds_ts else None, doi_chieu_ema=False)
    return dict(bt=bt, ds=ds, TS=TS, KQ=KQ, BH=BH, GD=GD, tk=tk, tu=vn(BAT_DAU)[:10], den=vn(KET_THUC - 1)[:10], dien_giai=DIEN_GIAI)


def ghi_tuy_chon(R, thu_muc):
    thu_muc = Path(thu_muc); thu_muc.mkdir(parents=True, exist_ok=True)
    for k, kq in R["KQ"].items():
        ghi_lenh(kq, thu_muc / f"lenh_{k.replace(chr(39), 'p')}.csv")
    (thu_muc / "tu_kiem.txt").write_text(R["tk"] + "\n")


def in_tom_tat(R):
    print(f"Giai đoạn {R['tu']} → {R['den']} (giờ VN) · luật 8 theo {'GIÁ' if R['dien_giai'] == 'gia' else 'THỜI GIAN'} · dữ liệu {DL}")
    for k, kq in R["KQ"].items():
        st = thong_ke(kq["lenh"])
        gd = f" | giả dược P50 {q(R['GD'][k][0], .5):+.0f}$ → phân vị {phan_vi(R['GD'][k][0], kq['so_du'] - VON0):.0f}" if k in R["GD"] else ""
        print(f"{k}: {kq['so_du'] - VON0:+9.2f}$ ({(kq['so_du'] / VON0 - 1) * 100:+.1f}%), {st['n']} lệnh, thắng {st['thang'] * 100:.0f}%, "
              f"R TB {st['r_tb']:+.2f}, DD {sut_giam(kq['von']) * 100:.1f}%, PF {st['pf']:.2f}{gd}")
    for t, d in R["BH"].items():
        print(f"Mua & giữ {t}: {d[-1][1] - VON0:+.0f}$ ({(d[-1][1] / VON0 - 1) * 100:+.1f}%)")
    print(R["tk"].split("\n")[0]); print(R["tk"].split("\n")[1].split("\n")[0])


def main():
    co = doc_co()
    if any(v is not None for v in (co.tu, co.den, co.tai_san, co.dien_giai, co.thu_muc_du_lieu, co.ra)):
        cau_hinh(co.tu, co.den, co.thu_muc_du_lieu, co.dien_giai)
        ds_ts = [m.strip().upper() for m in co.tai_san.split(",")] if co.tai_san else None
        R = chay_tuy_chon(ds_ts)
        in_tom_tat(R)
        ra = Path(co.ra) if co.ra else GOC / "ngoai_mau" / f"{R['tu']}_{R['den']}_{R['dien_giai']}"
        ghi_tuy_chon(R, ra)
        print(f"✓ Đã ghi lenh_*.csv, tu_kiem.txt vào {ra}")
        return
    if co.tai_lai or not all((DL / f"{m}_4H.csv").exists() for m in TAT_CA):
        subprocess.run([sys.executable, str(GOC / "tai_du_lieu.py")], check=True)
    TS = {m: nap(m) for m in TAT_CA}
    KQ = {}
    for k, cfg in BIEN_THE.items():
        KQ[k] = mo_phong(k, cfg["ts"], cfg["rui_ro"], cfg["loc_d1"], cfg["toi_da"], TS)
        ghi_lenh(KQ[k], GOC / f"lenh_{k}.csv")
        st = thong_ke(KQ[k]["lenh"])
        print(f"{k}: {KQ[k]['so_du'] - VON0:+9.2f}$ ({(KQ[k]['so_du'] / VON0 - 1) * 100:+.1f}%), {st['n']} lệnh, thắng {st['thang'] * 100:.0f}%, "
              f"R TB {st['r_tb']:+.2f}, DD {sut_giam(KQ[k]['von']) * 100:.1f}%, PF {st['pf']:.2f}")
    BH = {}
    for m in COIN4:
        BH[m] = mua_giu(TS, [m], VON0)
    BH["giỏ 4 coin"] = mua_giu(TS, COIN4, VON0 / 4)
    for m in TAT_CA[4:]:
        BH[TEN[m]] = mua_giu(TS, [m], VON0)
    BH["giỏ 8 tài sản"] = mua_giu(TS, TAT_CA, VON0 / 8)
    for t, d in BH.items():
        print(f"Mua & giữ {t}: {d[-1][1] - VON0:+.0f}$ ({(d[-1][1] / VON0 - 1) * 100:+.1f}%)")
    GD = {}
    for k in ("A", "E"):
        GD[k] = gia_duoc(KQ[k], TS, BIEN_THE[k]["rui_ro"], SEED)
        lai = GD[k][0]
        print(f"Giả dược {k}: P5 {q(lai, .05):+.0f} P50 {q(lai, .5):+.0f} P95 {q(lai, .95):+.0f} → phân vị thật {phan_vi(lai, KQ[k]['so_du'] - VON0):.0f}")
    tk = tu_kiem(TS, KQ)
    (GOC / "tu_kiem.txt").write_text(tk + "\n")
    print(tk.split("\n")[0])
    (GOC / "KET_QUA.md").write_text(lam_bao_cao(KQ, BH, GD, TS, tk))
    lam_html(KQ, BH)
    print("✓ Đã ghi lenh_A..E.csv, KET_QUA.md, von.html, tu_kiem.txt")


if __name__ == "__main__":
    main()
