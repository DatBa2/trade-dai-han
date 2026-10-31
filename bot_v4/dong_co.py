#!/usr/bin/env python3
"""ĐỘNG CƠ BOT V4 — viết đúng `bot_v4/THIET_KE.md` (khoá sha256 ở `bot_v4/KHOA.md`).

Quy ước chú thích:  "# TK x.y" = mục x.y của THIET_KE.md;  "# DG n" = mục n của `bot_v4/DIEN_GIAI.md`
(cách hiểu chỗ thiết kế chưa nói rõ, ghi TRƯỚC lần chạy dữ liệu thật đầu tiên).  Mọi hằng số nằm trong THAM_SO.

NHÂN QUẢ (không nhìn trước):
- Chỉ báo tính đệ quy trái → phải (`cong_cu/chi_bao.py`): giá trị ở nến i chỉ dùng nến ≤ i.
- Quyết định tại GIỜ ĐÓNG nến H4 t, chỉ dùng: nến H4 có giờ đóng ≤ t; nến D1 có giờ đóng ≤ t; nến W1 có giờ đóng ≤ t;
  fractal ở nến i chỉ dùng khi nến i+3 đã đóng (TK 1, TK 2).
- Mô phỏng lệnh (`mo_phong_lenh`) đi tới tương lai của RIÊNG lệnh đó, nhưng `chay` chỉ cộng tiền / giải phóng chỗ
  tại đúng giờ sự kiện xảy ra (hàng đợi sự kiện), nên quyết định ở t chỉ thấy sự kiện có giờ ≤ t.
- `chay(..., cat_tai=T)` CẮT dữ liệu thô tại T rồi tính lại MỌI chỉ báo từ đầu — dùng cho kiểm cắt cụt (TK 9.1).

Thời gian: số nguyên giây UTC (epoch). Nến: dict {ts_utc (giờ MỞ), dong (giờ ĐÓNG), open, high, low, close, vol}.
Trong KetQua mọi giờ là epoch giây UTC; trong CSV là chuỗi "YYYY-MM-DD HH:MM" UTC.

Giao diện: TAI_SAN, THAM_SO, nap_du_lieu, chay, view_tai, mo_phong_lenh, ghi_ket_qua, tom_tat.
"""
import bisect
import csv
import datetime as dt
import hashlib
import heapq
import json
import math
import sys
from pathlib import Path
from types import SimpleNamespace

GOC = Path(__file__).resolve().parent
if str(GOC.parent) not in sys.path:
    sys.path.insert(0, str(GOC.parent))
from cong_cu.chi_bao import atr_wilder, ema, fractal, fractal_da_xac_nhan, rsi_wilder  # noqa: E402

UTC = dt.timezone.utc
GIO = 3600
NGAY = 86400
THU_MUC_DU_LIEU = GOC / "du_lieu"

TAI_SAN = ["BTC", "ETH", "OKB", "BNB", "VANG", "DAU"]   # TK 0 — thứ tự này cũng là thứ tự xét cùng giờ (DG 23)
CRYPTO = ("BTC", "ETH", "OKB", "BNB")

# ======================= THAM SỐ — toàn bộ hằng số của thiết kế, không có tham số ẩn =======================
THAM_SO = {
    # TK 1 — dữ liệu / kỳ chạy
    "du_lieu_tu": "2022-06-01",
    "het_du_lieu_utc": "2026-10-31 00:00",          # 2026 chạy tới hết 30/10 (DG 4)
    "gio_dong_d1_crypto_h": 24,                      # DG 1: nến 1Dutc OKX mở 00:00 UTC, đóng sau 24h
    "gio_dong_d1_vang_dau_h": 23,                    # DG 1: phiên CME: ts_utc = 17:00 New York − 23h → đóng = ts + 23h
    "lech_ngay_gd_vang_dau_h": 2,                    # DG 2: ngày giao dịch vàng/dầu = ngày UTC của (ts_utc + 2h)
    # TK 2 — chỉ báo
    "ema_dai": 34, "ema_89": 89, "ema_200": 200, "ema_610": 610,
    "rsi_n": 14, "atr_n": 14, "fractal_k": 3,
    # TK 3 — pha W1
    "pha_ema_nhanh": 34, "pha_ema_cham": 89, "pha_so_tuan_doi": 2,
    # TK 4 — view H4
    "phan_van_nguong": 0.006,                        # |EMA34c−EMA89|/close và |EMA89−EMA200|/close < 0,6%
    "hoi_rsi_qua_ban": 30.0, "hoi_rsi_qua_mua": 70.0,
    # TK 5.1 — mức
    "muc_gan_min": 0.003, "muc_xa_max": 0.06,        # mức trong (0,3%; 6%] tính từ close H4
    "fibo_ti_le": [0.5, 0.618], "fibo_nhip_min_atr": 1.5,
    "so_fractal_h4": 3, "so_fractal_d1": 1, "so_sr_doi_vai": 3,
    # TK 5.2 — vùng hội tụ
    "gom_cach_max": 0.005, "gom_rong_max": 0.01, "diem_min": 2,
    # TK 5.3 — lệnh chính
    "buoc_tron": {"BTC": 1000.0, "ETH": 100.0, "BNB": 10.0, "OKB": 1.0, "VANG": 50.0, "DAU": 1.0},
    "tron_gan": 0.001, "tron_lui": 0.0015,
    "so_nen_hieu_luc": 6,
    "sl_dem_pct": 0.003, "sl_dem_atr": 0.5,
    "sl_min": {"BTC": 0.012, "ETH": 0.012, "OKB": 0.02, "BNB": 0.02, "VANG": 0.008, "DAU": 0.015},
    "sl_max": 0.06,
    "tp2_fibo_mo_rong": 1.618, "tp1_non": 0.002,
    "tp2_du_phong_R": 2.5, "tp1_du_phong_R": 1.0,
    "tp2_min_R": 2.0, "tp1_min_R": 0.5, "tp1_thay_the_R": 1.0,
    "chot_tp1": 0.5, "gio_dung_chinh": 120,
    # TK 6 — lệnh hồi
    "hoi_tp_min_R": 1.5, "gio_dung_hoi": 48,
    # TK 7 — vốn, khớp, phí
    "von_dau": 4000.0, "rui_ro_chinh": 0.02, "rui_ro_hoi": 0.01,
    "don_bay_chia": 0.40, "don_bay_max": 20.0,
    "toi_da_lenh": 3, "ky_quy_max": 0.50,
    "phi_vao": 0.0002, "phi_tp": 0.0002, "phi_market": 0.0005, "truot": 0.0002,
    "funding": "bo qua (TK 7)",
}
P = THAM_SO


# ======================= thời gian =======================
def ts_tu_chuoi(s):
    return int(dt.datetime.strptime(s.strip(), "%Y-%m-%d %H:%M").replace(tzinfo=UTC).timestamp())


def chuoi_gio(ts):
    return "" if ts is None else dt.datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%d %H:%M")


def ve_ts(t):
    """int/float epoch, datetime (không múi giờ = UTC) hoặc chuỗi 'YYYY-MM-DD HH:MM' (UTC) → epoch giây."""
    if isinstance(t, (int, float)):
        return int(t)
    if isinstance(t, dt.datetime):
        if t.tzinfo is None:
            t = t.replace(tzinfo=UTC)
        return int(t.timestamp())
    if isinstance(t, str):
        return ts_tu_chuoi(t)
    raise TypeError(f"không hiểu thời điểm {t!r}")


def ky_chay(nam):
    """TK 1 + DG 4 — (bắt đầu, kết thúc) của kỳ năm `nam`: quyết định tại giờ đóng H4 t với bat_dau ≤ t < ket_thuc;
    nến được quản lý tới giờ đóng ≤ ket_thuc. 2026: kết thúc 2026-10-31 00:00 UTC (hết ngày 30/10)."""
    bd = int(dt.datetime(nam, 1, 1, tzinfo=UTC).timestamp())
    kt = int(dt.datetime(nam + 1, 1, 1, tzinfo=UTC).timestamp())
    return bd, min(kt, ts_tu_chuoi(P["het_du_lieu_utc"]))


# ======================= dữ liệu =======================
def gio_dong_d1(ma, mo):
    """DG 1 — giờ đóng nến D1."""
    return mo + (P["gio_dong_d1_crypto_h"] if ma in CRYPTO else P["gio_dong_d1_vang_dau_h"]) * GIO


def doc_csv(p):
    """Đọc CSV nến (`ts_utc,open,high,low,close,vol`, ts_utc = giờ MỞ). Chấp nhận thêm định dạng cũ của backtest
    (`mo_utc,dong_utc,...`) để chạy thử. Trả list (mo, o, h, l, c, v) sắp theo thời gian."""
    ra = []
    with open(p, newline="") as f:
        for r in csv.DictReader(f):
            s = r.get("ts_utc") or r.get("mo_utc")
            ra.append((ts_tu_chuoi(s), float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"]),
                       float(r.get("vol") or 0.0)))
    ra.sort()
    return ra


def _nen(mo, dong, o, h, l, c, v):
    return {"ts_utc": mo, "dong": dong, "open": o, "high": h, "low": l, "close": c, "vol": v}


def thu_hai_cua_tuan(ma, mo_d1):
    """DG 2 — giờ 00:00 UTC thứ Hai của tuần chứa NGÀY GIAO DỊCH của nến D1.
    Crypto: ngày UTC của ts_utc. Vàng/dầu: ngày UTC của (ts_utc + 2h) (phiên thứ Hai mở 22:00/23:00 UTC Chủ nhật)."""
    lech = 0 if ma in CRYPTO else P["lech_ngay_gd_vang_dau_h"] * GIO
    ngay = dt.datetime.fromtimestamp(mo_d1 + lech, UTC).date()
    thu_hai = ngay - dt.timedelta(days=ngay.weekday())
    return int(dt.datetime(thu_hai.year, thu_hai.month, thu_hai.day, tzinfo=UTC).timestamp())


def dung_w1(ma, d1):
    """TK 1 — W1 dựng từ D1, tuần bắt đầu thứ Hai 00:00 UTC; giờ đóng W1 = thứ Hai 00:00 UTC tuần sau (DG 2)."""
    tuan = {}
    for r in d1:
        tuan.setdefault(thu_hai_cua_tuan(ma, r["ts_utc"]), []).append(r)
    ra = []
    for mo in sorted(tuan):
        ds = tuan[mo]
        ra.append(_nen(mo, mo + 7 * NGAY, ds[0]["open"], max(x["high"] for x in ds), min(x["low"] for x in ds),
                       ds[-1]["close"], sum(x["vol"] for x in ds)))
    return ra


def dung_du_lieu(ma, h4, d1, cat=None):
    """Dựng bộ dữ liệu 1 tài sản từ nến thô rồi TÍNH LẠI mọi chỉ báo.
    cat (epoch) ≠ None: chỉ giữ nến H4/D1/W1 có giờ đóng ≤ cat (coi như dữ liệu chỉ có tới đó — TK 9.1)."""
    if cat is not None:
        h4 = [r for r in h4 if r["dong"] <= cat]
        d1 = [r for r in d1 if r["dong"] <= cat]
    w1 = dung_w1(ma, d1)
    if cat is not None:
        w1 = [r for r in w1 if r["dong"] <= cat]
    return {"ma": ma, "4H": h4, "1D": d1, "W1": w1, "cat": cat, "cb": tinh_chi_bao(ma, h4, d1, w1)}


def cat_du_lieu(du, t):
    """Bản sao `du` chỉ còn dữ liệu có giờ đóng ≤ t, chỉ báo tính lại từ đầu."""
    return dung_du_lieu(du["ma"], du["4H"], du["1D"], cat=ve_ts(t))


def nap_du_lieu(tai_san, thu_muc=None):
    """Nạp 1 tài sản: {"ma", "4H", "1D", "W1" (dựng từ 1D), "cb" (chỉ báo), "sha256"}."""
    tm = Path(thu_muc) if thu_muc else THU_MUC_DU_LIEU
    ra_tho = {}
    sha = {}
    for khung in ("4H", "1D"):
        p = tm / f"{tai_san}_{khung}.csv"
        sha[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
        buoc = 4 * GIO if khung == "4H" else None
        ra_tho[khung] = [_nen(mo, mo + buoc if buoc else gio_dong_d1(tai_san, mo), o, h, l, c, v)
                         for mo, o, h, l, c, v in doc_csv(p)]
    du = dung_du_lieu(tai_san, ra_tho["4H"], ra_tho["1D"])
    du["sha256"] = sha
    du["thu_muc"] = str(tm)
    return du


def _lay_du(du_lieu, tai_san):
    """Chấp nhận du của 1 tài sản (có khoá "cb") hoặc dict {mã: du}."""
    if du_lieu is None:
        return nap_du_lieu(tai_san)
    if "cb" in du_lieu:
        return du_lieu
    return du_lieu[tai_san]


# ======================= chỉ báo + pha + view =======================
def tinh_pha(c, e34, e89):
    """TK 3 — pha tại mỗi nến W1 j (trạng thái SAU khi W1 j đóng).
    Điều kiện TĂNG: close > EMA34 và EMA34 > EMA89; GIẢM: close < EMA34 và EMA34 < EMA89.
    Đổi pha chỉ khi 2 nến W1 LIÊN TIẾP thoả điều kiện pha ngược (L07).
    DG 3: trước khi có điều kiện nào thoả (kể cả lúc EMA89 W1 chưa đủ nến) pha = close W1 so với EMA34 W1, tính lại
    mỗi tuần; lần đầu có điều kiện thoả thì pha khoá theo điều kiện đó và từ đây chỉ đổi theo công tắc 2 cây."""
    pha = [None] * len(c)
    hien, da_khoa, dem = None, False, 0
    for j in range(len(c)):
        if e34[j] is None:
            continue
        dk = None
        if e89[j] is not None:
            if c[j] > e34[j] and e34[j] > e89[j]:
                dk = "TANG"
            elif c[j] < e34[j] and e34[j] < e89[j]:
                dk = "GIAM"
        if not da_khoa:
            if dk is not None:
                hien, da_khoa, dem = dk, True, 0
            else:
                hien = "TANG" if c[j] > e34[j] else "GIAM"
        else:
            if dk is not None and dk != hien:
                dem += 1
                if dem >= P["pha_so_tuan_doi"]:
                    hien, dem = dk, 0
            else:
                dem = 0
        pha[j] = hien
    return pha


def tinh_chi_bao(ma, h4, d1, w1):
    cb = SimpleNamespace(ma=ma)
    # --- H4 (TK 2)
    cb.mo = [r["ts_utc"] for r in h4]
    cb.dong = [r["dong"] for r in h4]
    cb.o = [r["open"] for r in h4]
    cb.h = [r["high"] for r in h4]
    cb.l = [r["low"] for r in h4]
    cb.c = [r["close"] for r in h4]
    cb.chi_so = {t: i for i, t in enumerate(cb.dong)}
    cb.e34h, cb.e34l, cb.e34c = ema(cb.h, P["ema_dai"]), ema(cb.l, P["ema_dai"]), ema(cb.c, P["ema_dai"])
    cb.e89, cb.e200, cb.e610 = ema(cb.c, P["ema_89"]), ema(cb.c, P["ema_200"]), ema(cb.c, P["ema_610"])
    cb.atr = atr_wilder(cb.h, cb.l, cb.c, P["atr_n"])
    cb.dinh, cb.day = fractal(cb.h, cb.l, P["fractal_k"])
    cb.dinh_i, cb.day_i = [i for i, _ in cb.dinh], [i for i, _ in cb.day]
    # --- D1 (TK 2)
    cb.d_dong = [r["dong"] for r in d1]
    cb.d_h = [r["high"] for r in d1]
    cb.d_l = [r["low"] for r in d1]
    cb.d_c = [r["close"] for r in d1]
    cb.d_e34h, cb.d_e34l = ema(cb.d_h, P["ema_dai"]), ema(cb.d_l, P["ema_dai"])
    cb.d_e89, cb.d_e200 = ema(cb.d_c, P["ema_89"]), ema(cb.d_c, P["ema_200"])
    cb.d_rsi = rsi_wilder(cb.d_c, P["rsi_n"])
    cb.d_dinh, cb.d_day = fractal(cb.d_h, cb.d_l, P["fractal_k"])
    cb.d_dinh_i, cb.d_day_i = [i for i, _ in cb.d_dinh], [i for i, _ in cb.d_day]
    # --- W1 (TK 3)
    cb.w_dong = [r["dong"] for r in w1]
    cb.w_c = [r["close"] for r in w1]
    cb.w_e34, cb.w_e89 = ema(cb.w_c, P["pha_ema_nhanh"]), ema(cb.w_c, P["pha_ema_cham"])
    cb.w_pha = tinh_pha(cb.w_c, cb.w_e34, cb.w_e89)
    # --- TK 1: tại giờ đóng H4 t chỉ dùng D1/W1 có giờ đóng ≤ t
    cb.d1i = [bisect.bisect_right(cb.d_dong, t) - 1 for t in cb.dong]
    cb.w1i = [bisect.bisect_right(cb.w_dong, t) - 1 for t in cb.dong]
    # --- TK 3 + TK 4: pha và view tại mỗi lần đóng H4
    cb.pha, cb.view, cb.kieu, cb.ly_do = [], [], [], []
    for k in range(len(cb.dong)):
        pha, view, kieu, ly_do = _view_tai_nen(cb, k)
        cb.pha.append(pha)
        cb.view.append(view)
        cb.kieu.append(kieu)
        cb.ly_do.append(ly_do)
    return cb


def _view_tai_nen(cb, k):
    """TK 4 — view H4 tại lần đóng nến k. Trả (pha, view, kieu, ly_do).
    view ∈ TANG / GIAM / PHAN_VAN / CHUA_DU;  kieu ∈ THUAN / HOI / PHAN_VAN / CHUA_DU."""
    j, d = cb.w1i[k], cb.d1i[k]
    pha = cb.w_pha[j] if j >= 0 else None                         # TK 3: W1 đã đóng ≤ t
    rsi = cb.d_rsi[d] if d >= 0 else None                         # TK 4.2: D1 đã đóng gần nhất
    e34, e89, e200, c = cb.e34c[k], cb.e89[k], cb.e200[k], cb.c[k]
    thieu = [ten for ten, v in (("pha_W1", pha), ("EMA34c_H4", e34), ("EMA89_H4", e89), ("EMA200_H4", e200),
                                ("RSI14_D1", rsi)) if v is None]
    if thieu:                                                     # DG 5: thiếu dữ liệu → không có view, không lệnh
        return pha, "CHUA_DU", "CHUA_DU", "thieu_du_lieu: " + ",".join(thieu)
    # TK 4.1 — PHÂN VÂN (hẹp): 2 khoảng cách < 0,6% và close nằm giữa min, max của 3 đường (DG 6: tính cả biên)
    k1, k2 = abs(e34 - e89) / c, abs(e89 - e200) / c
    if k1 < P["phan_van_nguong"] and k2 < P["phan_van_nguong"] and min(e34, e89, e200) <= c <= max(e34, e89, e200):
        return pha, "PHAN_VAN", "PHAN_VAN", f"phan_van: |34-89|={k1:.3%} |89-200|={k2:.3%} close giua 3 EMA"
    # TK 4.2 — HỒI ngược pha theo RSI14 D1
    if pha == "GIAM" and rsi <= P["hoi_rsi_qua_ban"]:
        return pha, "TANG", "HOI", f"hoi: pha GIAM, RSI14_D1={rsi:.2f}<=30"
    if pha == "TANG" and rsi >= P["hoi_rsi_qua_mua"]:
        return pha, "GIAM", "HOI", f"hoi: pha TANG, RSI14_D1={rsi:.2f}>=70"
    # TK 4.3 — còn lại: view = hướng pha (không đổi vì nến đóng qua mốc)
    return pha, pha, "THUAN", f"thuan_pha {pha}, RSI14_D1={rsi:.2f}"


def thieu_chi_bao(cb, k):
    """DG 5 — tên các đại lượng mà TK 4 + TK 5.1 + TK 5.3 cần nhưng chưa có (None) tại nến k."""
    d = cb.d1i[k]
    can = [("EMA34h_H4", cb.e34h[k]), ("EMA34l_H4", cb.e34l[k]), ("EMA34c_H4", cb.e34c[k]), ("EMA89_H4", cb.e89[k]),
           ("EMA200_H4", cb.e200[k]), ("EMA610_H4", cb.e610[k]), ("ATR14_H4", cb.atr[k])]
    if d < 0:
        can.append(("D1", None))
    else:
        can += [("EMA34h_D1", cb.d_e34h[d]), ("EMA34l_D1", cb.d_e34l[d]), ("EMA89_D1", cb.d_e89[d]),
                ("EMA200_D1", cb.d_e200[d]), ("RSI14_D1", cb.d_rsi[d])]
    can.append(("pha_W1", cb.pha[k]))
    return [ten for ten, v in can if v is None]


# ======================= TK 5.1 – 5.3: mức, vùng, lệnh =======================
def tim_nhip(cb, k, chieu):
    """TK 5.1 — nhịp H4 hiện tại. SHORT (chieu −1): A = đỉnh fractal H4 đã xác nhận gần nhất (theo thời gian),
    B = low thấp nhất từ nến sau A tới nến k (râu, DG 10). LONG: A = đáy fractal gần nhất, B = high cao nhất.
    hop_le = |A − B| ≥ 1,5 × ATR14 H4 tại k. Không có fractal → None."""
    if chieu < 0:
        n = fractal_da_xac_nhan(cb.dinh, cb.dinh_i, k, P["fractal_k"])
        if n == 0:
            return None
        i_a, a = cb.dinh[n - 1]
        b = min(cb.l[i_a + 1:k + 1])
    else:
        n = fractal_da_xac_nhan(cb.day, cb.day_i, k, P["fractal_k"])
        if n == 0:
            return None
        i_a, a = cb.day[n - 1]
        b = max(cb.h[i_a + 1:k + 1])
    return {"i_a": i_a, "A": a, "B": b, "hop_le": abs(a - b) >= P["fibo_nhip_min_atr"] * cb.atr[k]}


def liet_ke_muc(cb, k, chieu):
    """TK 5.1 — danh sách mức (gia, loai, ghi_chu) phía TRÊN close (SHORT, chieu −1) hoặc DƯỚI close (LONG, chieu +1),
    chỉ giữ mức cách close trong (0,3%; 6%] (DG 11: % tính trên close H4 tại k)."""
    c, d = cb.c[k], cb.d1i[k]
    tren = chieu < 0
    ra = []

    def them(gia, loai, ghi):
        if gia is None:
            return
        kc = -chieu * (gia - c) / c                    # khoảng cách về phía lệnh, >0 nghĩa là đúng phía
        if P["muc_gan_min"] < kc <= P["muc_xa_max"]:
            ra.append((gia, loai, ghi))

    # EMA H4: dải EMA34 biên trên (SHORT) / biên dưới (LONG), EMA89, EMA200, EMA610
    them(cb.e34h[k] if tren else cb.e34l[k], "EMA34_H4", "EMA34 bien " + ("tren" if tren else "duoi") + " H4")
    them(cb.e89[k], "EMA89_H4", "EMA89 H4")
    them(cb.e200[k], "EMA200_H4", "EMA200 H4")
    them(cb.e610[k], "EMA610_H4", "EMA610 H4")
    # EMA D1 (nến D1 đã đóng gần nhất): dải EMA34 biên trên/dưới, EMA89, EMA200
    if d >= 0:
        them(cb.d_e34h[d] if tren else cb.d_e34l[d], "EMA34_D1", "EMA34 bien " + ("tren" if tren else "duoi") + " D1")
        them(cb.d_e89[d], "EMA89_D1", "EMA89 D1")
        them(cb.d_e200[d], "EMA200_D1", "EMA200 D1")
    # Fibo 0,5 / 0,618 của nhịp hiện tại (chỉ khi nhịp hợp lệ)
    nhip = tim_nhip(cb, k, chieu)
    if nhip and nhip["hop_le"]:
        a, b = nhip["A"], nhip["B"]
        for r in P["fibo_ti_le"]:
            them(b + r * (a - b), f"FIBO_{r}", f"Fibo {r} A={a:.6g} B={b:.6g}")
    # Fractal (cả nhóm tính 1 loại — TK 5.2). DG 8: "gần nhất" = theo thời gian; lấy N cái gần nhất rồi mới lọc khoảng.
    kf = P["fractal_k"]
    if tren:
        ds, ds_i, ds_sr, ds_sr_i, d_ds, d_ds_i = cb.dinh, cb.dinh_i, cb.day, cb.day_i, cb.d_dinh, cb.d_dinh_i
    else:
        ds, ds_i, ds_sr, ds_sr_i, d_ds, d_ds_i = cb.day, cb.day_i, cb.dinh, cb.dinh_i, cb.d_day, cb.d_day_i
    n = fractal_da_xac_nhan(ds, ds_i, k, kf)
    for i, p in ds[max(0, n - P["so_fractal_h4"]):n]:
        them(p, "FRACTAL", ("dinh" if tren else "day") + f" H4 @{chuoi_gio(cb.dong[i])}")
    if d >= 0:
        nd = fractal_da_xac_nhan(d_ds, d_ds_i, d, kf)
        for i, p in d_ds[max(0, nd - P["so_fractal_d1"]):nd]:
            them(p, "FRACTAL", ("dinh" if tren else "day") + f" D1 @{chuoi_gio(cb.d_dong[i])}")
    # S/R đổi vai (DG 9): SHORT: đáy fractal H4 đã xác nhận nay nằm TRÊN close (đã bị close xuyên xuống);
    # LONG: đỉnh fractal H4 đã xác nhận nay nằm DƯỚI close. Lấy 3 cái gần nhất theo thời gian.
    n = fractal_da_xac_nhan(ds_sr, ds_sr_i, k, kf)
    dem = 0
    for i, p in reversed(ds_sr[:n]):
        if dem >= P["so_sr_doi_vai"]:
            break
        if (p > c) if tren else (p < c):
            dem += 1
            them(p, "FRACTAL", ("day" if tren else "dinh") + f" H4 doi vai @{chuoi_gio(cb.dong[i])}")
    return ra


def gom_cum(muc, c, chieu):
    """TK 5.2 — gom mức thành cụm liên tiếp, đi từ mức GẦN giá nhất ra xa (DG 11): mức kế tiếp vào cụm nếu cách mức
    liền trước ≤ 0,5% và cách mức đầu cụm ≤ 1% (độ rộng cụm ≤ 1%); % tính trên close H4."""
    ds = sorted(muc, key=lambda m: (-chieu * (m[0] - c), m[1], m[2]))
    cum, hien = [], []
    for m in ds:
        if hien and abs(m[0] - hien[-1][0]) / c <= P["gom_cach_max"] and abs(m[0] - hien[0][0]) / c <= P["gom_rong_max"]:
            hien.append(m)
        else:
            if hien:
                cum.append(hien)
            hien = [m]
    if hien:
        cum.append(hien)
    return cum


def diem_cum(cum):
    """TK 5.2 — điểm = số LOẠI căn cứ khác nhau (mỗi EMA 1, Fibo 0,5 và 0,618 mỗi cái 1, nhóm fractal 1) — DG 12."""
    return len({m[1] for m in cum})


def mo_ta_cum(cum):
    lo, hi = min(m[0] for m in cum), max(m[0] for m in cum)
    return f"{lo:.6g}-{hi:.6g} diem={diem_cum(cum)} [" + "; ".join(f"{m[1]}:{m[0]:.6g}" for m in cum) + "]"


def lap_lenh(cb, ma, k, chieu, loai):
    """TK 5.1–5.3 (loai "chinh") và TK 6 (loai "hoi"). Trả (ke_hoach | None, mo_ta_vung, ly_do_bo)."""
    c = cb.c[k]
    muc = liet_ke_muc(cb, k, chieu)
    cums = gom_cum(muc, c, chieu)
    chon = next((cu for cu in cums if diem_cum(cu) >= P["diem_min"]), None)   # TK 5.2: cụm GẦN giá nhất đạt ≥ 2
    if chon is None:
        tot = max((diem_cum(cu) for cu in cums), default=0)
        return None, "", f"khong_co_vung_du_2_diem ({len(muc)} muc, diem cao nhat {tot})"
    vung = mo_ta_cum(chon)
    lo, hi = min(m[0] for m in chon), max(m[0] for m in chon)
    # TK 5.3 — limit tại GIỮA cụm; gần bội số tròn (≤ 0,1%) → lùi 0,15% về phía giá hiện tại (DG 13)
    giua = (lo + hi) / 2
    buoc = P["buoc_tron"][ma]
    boi = math.floor(giua / buoc + 0.5) * buoc
    vao, lui_tron = giua, False
    if abs(giua - boi) <= P["tron_gan"] * giua:
        vao, lui_tron = giua * (1 + chieu * P["tron_lui"]), True
    # TK 5.3 — SL = mép xa của cụm + max(0,3% × giá vào, 0,5 × ATR14 H4); sàn SL tối thiểu theo tài sản; > 6% → bỏ (DG 14)
    mep_xa = hi if chieu < 0 else lo
    sl = mep_xa - chieu * max(P["sl_dem_pct"] * vao, P["sl_dem_atr"] * cb.atr[k])
    if abs(vao - sl) / vao < P["sl_min"][ma]:
        sl = vao * (1 - chieu * P["sl_min"][ma])
    kc = abs(vao - sl)
    if kc / vao > P["sl_max"]:
        return None, vung, f"sl_qua_6% ({kc / vao:.2%})"
    ghi = []
    if lui_tron:
        ghi.append(f"lui_so_tron({boi:.6g})")
    if loai == "chinh":
        # TK 5.3 — TP Fibo Eric 3 điểm: A, B như 5.1, C = giá vào
        nhip = tim_nhip(cb, k, chieu)
        if nhip and nhip["hop_le"]:
            a, b = nhip["A"], nhip["B"]
            tp2 = vao + chieu * P["tp2_fibo_mo_rong"] * abs(a - b)
            tp1 = b * (1 - chieu * P["tp1_non"])                  # TP1 = B, non 0,2% về phía giá vào
            ghi.append("tp_fibo")
        else:                                                      # nhịp không hợp lệ → 2,5R / 1R
            tp2 = vao + chieu * P["tp2_du_phong_R"] * kc
            tp1 = vao + chieu * P["tp1_du_phong_R"] * kc
            ghi.append("tp_du_phong_R")
        if tp2 <= 0:                                               # DG 15
            return None, vung, "tp2_am"
        r2 = chieu * (tp2 - vao) / kc
        if r2 < P["tp2_min_R"]:                                    # TK 5.3 (L32): (TP2 − vào)/SL < 2 → bỏ
            return None, vung, f"tp2_duoi_2R ({r2:.2f}R)"
        if chieu * (tp1 - vao) / kc < P["tp1_min_R"]:              # TK 5.3: TP1 < 0,5R → TP1 = 1R
            tp1 = vao + chieu * P["tp1_thay_the_R"] * kc
            ghi.append("tp1=1R")
        if chieu * (tp1 - vao) >= chieu * (tp2 - vao):             # DG 15: TP1 không nằm trước TP2 → TP1 = 1R
            tp1 = vao + chieu * P["tp1_thay_the_R"] * kc
            ghi.append("tp1_qua_tp2->1R")
        gio_dung, rui_ro = P["gio_dung_chinh"], P["rui_ro_chinh"]
    else:
        # TK 6 — TP duy nhất = EMA34(close) H4 tại lúc đặt; cần ≥ 1,5R (DG 16: vùng / giá vào / SL / hiệu lực như 5.3)
        tp2, tp1 = cb.e34c[k], None
        r = chieu * (tp2 - vao) / kc
        if r < P["hoi_tp_min_R"]:
            return None, vung, f"tp_hoi_duoi_1.5R ({r:.2f}R)"
        gio_dung, rui_ro = P["gio_dung_hoi"], P["rui_ro_hoi"]
    return ({"tai_san": ma, "loai": loai, "chieu": chieu, "vao": vao, "sl": sl, "tp1": tp1, "tp2": tp2,
             "gio_dung": gio_dung, "rui_ro": rui_ro, "vung": vung, "ghi": ",".join(ghi)}, vung, "")


# ======================= TK 5.3, 6, 7: mô phỏng 1 lệnh =======================
def _chieu_so(chieu):
    if chieu in (1, -1):
        return chieu
    s = str(chieu).upper()
    if s in ("LONG", "TANG", "+1"):
        return 1
    if s in ("SHORT", "GIAM", "-1"):
        return -1
    raise ValueError(f"chiều không hợp lệ: {chieu!r}")


def mo_phong_lenh(tai_san, chieu, loai, t_dat, gia_vao, sl, tp1, tp2, gio_dung, du_lieu, khoi_luong,
                  ket_thuc=None, huy_khi_doi_view=True):
    """Mô phỏng 1 lệnh limit từ lúc đặt (giờ đóng nến H4 t_dat) tới lúc ra — đúng TK 5.3, 6, 7.

    chieu: +1/"LONG" hoặc −1/"SHORT".  loai: "chinh" (TP1 50% + dời SL về giá vào + TP2) | "hoi" (TP duy nhất = tp2,
    tp1 bỏ qua).  gio_dung: giờ dừng tính từ lúc khớp (120 / 48).  khoi_luong: số đơn vị tài sản (cố định, DG 22).
    ket_thuc: epoch; mặc định = hết kỳ của năm chứa t_dat (TK 1).  huy_khi_doi_view: TK 5.3 huỷ sớm nếu view đổi.
    Trả dict cột lenh.csv (TK 8) + su_kien [(t, tien, ten)] để `chay` cộng vốn đúng giờ. Mọi giờ = giờ ĐÓNG nến (DG 19).
    """
    du = _lay_du(du_lieu, tai_san)
    cb = du["cb"]
    x = _chieu_so(chieu)
    t_dat = ve_ts(t_dat)
    k = bisect.bisect_right(cb.dong, t_dat) - 1
    if k < 0:
        raise ValueError("t_dat trước nến H4 đầu tiên")
    if ket_thuc is None:
        ket_thuc = ky_chay(dt.datetime.fromtimestamp(t_dat, UTC).year)[1]
    ket_thuc = ve_ts(ket_thuc)
    j_cuoi = bisect.bisect_right(cb.dong, ket_thuc) - 1
    # DG 26: dữ liệu bị CẮT trước hết kỳ (kiểm cắt cụt / nhận định trực tiếp) → lệnh chưa xong thì để DANG_CHO / DANG_MO,
    # KHÔNG bịa ra lúc ra (HET_KY chỉ dùng khi thật sự hết kỳ).
    du_bi_cat = du.get("cat") is not None and du["cat"] < ket_thuc
    kl = float(khoi_luong)
    kc_sl = abs(gia_vao - sl)
    sl_pct = kc_sl / gia_vao
    don_bay = min(P["don_bay_chia"] / sl_pct, P["don_bay_max"])            # TK 7 (DG 22: theo giá đặt)
    kq = {"tai_san": tai_san, "loai": loai, "chieu": "LONG" if x > 0 else "SHORT", "t_quyet_dinh": cb.dong[k],
          "t_khop": None, "gia_vao": None, "sl": sl, "tp1": tp1 if loai == "chinh" else None, "tp2": tp2,
          "t_tp1": None, "t_ra": None, "gia_ra": None, "ly_do_ra": None, "khoi_luong": kl, "don_bay": don_bay,
          "phi": 0.0, "lai_usd": 0.0, "R": 0.0, "von_sau": None,
          # cột thêm (để tự cộng lại): giá limit đặt, giá khớp TP1, tỉ lệ đã chốt ở TP1, rủi ro $, ký quỹ, lý do huỷ
          "gia_dat": gia_vao, "gia_tp1": None, "ti_le_tp1": 0.0, "rui_ro_usd": kl * kc_sl,
          "ky_quy": kl * gia_vao / don_bay, "gio_dung": gio_dung, "ly_do_huy": "", "su_kien": []}

    def huy(j, ly_do):
        kq.update(t_ra=cb.dong[j], ly_do_ra="HUY", ly_do_huy=ly_do)
        kq["su_kien"].append((cb.dong[j], 0.0, "huy"))
        return kq

    # --- TK 5.3: chờ khớp trong 6 nến SAU nến đặt; huỷ sớm nếu view đổi (DG 17: xét khớp trong nến trước, huỷ ở giờ đóng)
    view_dat = cb.view[k]
    f = None
    het = min(k + P["so_nen_hieu_luc"], j_cuoi)
    for j in range(k + 1, het + 1):
        if (cb.h[j] >= gia_vao) if x < 0 else (cb.l[j] <= gia_vao):
            f = j
            break
        if huy_khi_doi_view and cb.view[j] != view_dat:
            return huy(j, f"doi_view {view_dat}->{cb.view[j]}")
    if f is None:
        if k + P["so_nen_hieu_luc"] <= j_cuoi:
            return huy(k + P["so_nen_hieu_luc"], "het_6_nen")
        if du_bi_cat:
            kq["ly_do_ra"] = "DANG_CHO"
            return kq
        return huy(max(het, k), "het_ky")

    # --- khớp: giá limit; nếu nến mở đã vượt giá limit theo hướng có lợi → khớp ở giá mở (DG 18)
    khop = max(gia_vao, cb.o[f]) if x < 0 else min(gia_vao, cb.o[f])
    phi_vao = kl * khop * P["phi_vao"]                                     # TK 7: phí vào limit 0,02%
    kq.update(t_khop=cb.dong[f], gia_vao=khop, phi=phi_vao, lai_usd=-phi_vao)
    kq["su_kien"].append((cb.dong[f], -phi_vao, "phi_vao"))
    con = 1.0
    sl_ht = sl
    tp1_xong = False
    han = cb.dong[f] + gio_dung * GIO                                       # DG 19

    def ra(j, gia, ti_le, market, ly_do, cuoi):
        if market:                                                # TK 7: market 0,05% + trượt 0,02% bất lợi (DG 21)
            gia = gia * (1 - x * P["truot"])
        q = kl * ti_le
        phi = q * gia * (P["phi_market"] if market else P["phi_tp"])
        tien = q * (gia - khop) * x - phi
        kq["phi"] += phi
        kq["lai_usd"] += tien
        kq["su_kien"].append((cb.dong[j], tien, ly_do))
        if cuoi:
            kq.update(t_ra=cb.dong[j], gia_ra=gia, ly_do_ra=ly_do)
        return gia

    for j in range(f, j_cuoi + 1):
        o, h, l, c = cb.o[j], cb.h[j], cb.l[j], cb.c[j]
        # (1) TK 7: SL xét TRƯỚC (bảo thủ); SL theo giá chạm; giá mở đã vượt SL (gap) → ra ở giá mở
        if (h >= sl_ht) if x < 0 else (l <= sl_ht):
            gia = max(sl_ht, o) if x < 0 else min(sl_ht, o)
            ra(j, gia, con, True, "SL_HOA_VON" if tp1_xong else "SL", True)
            break
        if j > f:                                                           # TK 7: nến vừa khớp chỉ xét SL
            # (2) TK 5.3: chạm TP1 → chốt 50%, dời SL về giá vào (A5)
            if loai == "chinh" and not tp1_xong and ((l <= tp1) if x < 0 else (h >= tp1)):
                gia = min(tp1, o) if x < 0 else max(tp1, o)                 # DG 18: mở đã vượt TP → khớp giá mở
                kq["gia_tp1"] = ra(j, gia, P["chot_tp1"], False, "TP1", False)
                kq["t_tp1"], kq["ti_le_tp1"] = cb.dong[j], P["chot_tp1"]
                con -= P["chot_tp1"]
                sl_ht, tp1_xong = khop, True
                # DG 20: cùng nến đã chạm lại giá vào → coi như SL hoà vốn khớp (bảo thủ)
                if (h >= sl_ht) if x < 0 else (l <= sl_ht):
                    ra(j, sl_ht, con, True, "SL_HOA_VON", True)
                    break
            # (3) TP2 (lệnh chính, sau TP1) / TP duy nhất (lệnh hồi — TK 6)
            if (loai != "chinh" or tp1_xong) and ((l <= tp2) if x < 0 else (h >= tp2)):
                gia = min(tp2, o) if x < 0 else max(tp2, o)
                ra(j, gia, con, False, "TP2" if loai == "chinh" else "TP", True)
                break
        # (4) TK 5.3 / TK 6: dừng theo giờ — ra ở close nến đầu tiên có giờ đóng ≥ giờ khớp + gio_dung
        if cb.dong[j] >= han:
            ra(j, c, con, True, "HET_GIO", True)
            break
        # (5) TK 1: hết kỳ → đóng ở close cuối (DG 26: dữ liệu bị cắt → vẫn mở)
        if j == j_cuoi:
            if du_bi_cat:
                kq["ly_do_ra"] = "DANG_MO"
            else:
                ra(j, c, con, True, "HET_KY", True)
            break
    kq["R"] = kq["lai_usd"] / kq["rui_ro_usd"] if kq["rui_ro_usd"] > 0 else 0.0
    return kq


# ======================= TK 7: chạy cả rổ =======================
class KetQua:
    """lenh: list dict (cột TK 8 + cột thêm); von: list (ts, von theo giá thị trường); von_chot: list (ts, số dư đã
    chốt); so_mo: list (ts, số vị thế đang mở); quyet_dinh: list dict (ts, tai_san, pha, view, kieu, ly_do, hanh_dong,
    vung, ly_do_bo); thong_tin: dict."""

    def __init__(self):
        self.lenh, self.von, self.von_chot, self.so_mo, self.quyet_dinh, self.thong_tin = [], [], [], [], [], {}


def nap_ro(ds_tai_san, thu_muc=None):
    return {m: nap_du_lieu(m, thu_muc) for m in ds_tai_san}


def chay(ds_tai_san, nam, du_lieu=None, cat_tai=None):
    """Chạy rổ `ds_tai_san` cho năm `nam` (TK 1, 5, 6, 7). du_lieu: {mã: du} (None → nạp từ bot_v4/du_lieu).
    cat_tai (datetime/epoch UTC): coi như dữ liệu chỉ có tới đó (cắt thô rồi tính lại chỉ báo)."""
    ds = list(ds_tai_san)
    du_lieu = dict(du_lieu or {})
    for m in ds:
        if m not in du_lieu:
            du_lieu[m] = nap_du_lieu(m)
    if cat_tai is not None:
        cat = ve_ts(cat_tai)
        du_lieu = {m: cat_du_lieu(du_lieu[m], cat) for m in ds}
    bd, kt = ky_chay(nam)
    moc = sorted({t for m in ds for t in du_lieu[m]["cb"].dong if bd <= t <= kt})   # DG 27: hợp các giờ đóng H4
    kq = KetQua()
    so_du = P["von_dau"]
    hang = []          # hàng đợi sự kiện tiền: (giờ, thứ tự, tiền, chỉ số lệnh, là sự kiện cuối)
    dang = []          # chỉ số lệnh đang chiếm chỗ (lệnh chờ hoặc vị thế) — TK 7
    stt = 0

    def ap_su_kien(t):
        nonlocal so_du
        while hang and hang[0][0] <= t:
            _, _, tien, i, cuoi = heapq.heappop(hang)
            so_du += tien
            if cuoi:
                kq.lenh[i]["von_sau"] = so_du
                dang.remove(i)

    for t in moc:
        ap_su_kien(t)                       # sự kiện xảy ra trong các nến đóng tại ≤ t (đã biết ở t)
        if t < kt:                          # DG 4: quyết định tại giờ đóng H4 trong [bat_dau, ket_thuc)
            for m in ds:
                cb = du_lieu[m]["cb"]
                k = cb.chi_so.get(t)
                if k is None:
                    continue
                qd = {"ts": t, "tai_san": m, "pha": cb.pha[k] or "", "view": cb.view[k], "kieu": cb.kieu[k],
                      "ly_do": cb.ly_do[k], "hanh_dong": "", "vung": "", "ly_do_bo": ""}
                kq.quyet_dinh.append(qd)
                if any(kq.lenh[i]["tai_san"] == m for i in dang):        # TK 5: không có vị thế, không lệnh chờ
                    qd["hanh_dong"] = "DANG_CO_LENH"
                    continue
                if cb.kieu[k] == "PHAN_VAN":                              # TK 4.1
                    qd["hanh_dong"], qd["ly_do_bo"] = "KHONG_XET", "phan_van"
                    continue
                if cb.kieu[k] == "CHUA_DU":                               # DG 5
                    qd["hanh_dong"], qd["ly_do_bo"] = "KHONG_XET", "thieu_du_lieu"
                    continue
                thieu = thieu_chi_bao(cb, k)
                if thieu:                                                 # DG 5
                    qd["hanh_dong"], qd["ly_do_bo"] = "BO", "thieu_du_lieu: " + ",".join(thieu)
                    continue
                chieu = 1 if cb.view[k] == "TANG" else -1
                loai = "chinh" if cb.kieu[k] == "THUAN" else "hoi"        # TK 5 (thuận pha) / TK 6 (hồi)
                kh, vung, ly_do_bo = lap_lenh(cb, m, k, chieu, loai)
                qd["vung"] = vung
                if kh is None:
                    qd["hanh_dong"], qd["ly_do_bo"] = "BO", ly_do_bo
                    continue
                if len(dang) >= P["toi_da_lenh"]:                        # TK 7: tối đa 3 vị thế + lệnh chờ
                    qd["hanh_dong"], qd["ly_do_bo"] = "BO", "du_3_lenh"
                    continue
                # TK 7: khối lượng = rủi ro$ / khoảng SL; rủi ro theo số dư ĐÃ CHỐT lúc đặt (DG 22)
                rui_ro_usd = kh["rui_ro"] * so_du
                kl = rui_ro_usd / abs(kh["vao"] - kh["sl"])
                don_bay = min(P["don_bay_chia"] / (abs(kh["vao"] - kh["sl"]) / kh["vao"]), P["don_bay_max"])
                ky_quy = kl * kh["vao"] / don_bay
                # DG 22: ký quỹ đang dùng — lệnh chờ / vị thế tính đủ, vị thế đã chốt TP1 tính 50%
                dang_ky_quy = sum(kq.lenh[i]["ky_quy"] * (0.5 if (kq.lenh[i]["t_tp1"] is not None
                                                                   and kq.lenh[i]["t_tp1"] <= t) else 1.0)
                                  for i in dang)
                if dang_ky_quy + ky_quy > P["ky_quy_max"] * so_du:         # TK 7: ký quỹ tổng ≤ 50% vốn
                    qd["hanh_dong"], qd["ly_do_bo"] = "BO", "ky_quy_vuot_50%"
                    continue
                r = mo_phong_lenh(m, chieu, loai, t, kh["vao"], kh["sl"], kh["tp1"], kh["tp2"], kh["gio_dung"],
                                  du_lieu[m], kl, ket_thuc=kt)
                r["vung"], r["ghi"] = kh["vung"], kh["ghi"]
                i = len(kq.lenh)
                kq.lenh.append(r)
                dang.append(i)
                for n, (ts_e, tien, _) in enumerate(r["su_kien"]):
                    stt += 1
                    cuoi = n == len(r["su_kien"]) - 1 and r["t_ra"] is not None   # DANG_MO: chưa có sự kiện cuối
                    heapq.heappush(hang, (ts_e, stt, tien, i, cuoi))
                qd["hanh_dong"] = "DAT_LENH"
        # đường vốn: số dư đã chốt + lãi/lỗ chưa chốt của vị thế đang mở theo close (DG 25)
        mtm, so_mo = so_du, 0
        for i in dang:
            r = kq.lenh[i]
            if r["t_khop"] is None or r["t_khop"] > t:
                continue
            cb = du_lieu[r["tai_san"]]["cb"]
            gia = cb.c[bisect.bisect_right(cb.dong, t) - 1]
            con = 1.0 - (r["ti_le_tp1"] if (r["t_tp1"] is not None and r["t_tp1"] <= t) else 0.0)
            mtm += r["khoi_luong"] * con * (gia - r["gia_vao"]) * (1 if r["chieu"] == "LONG" else -1)
            so_mo += 1
        kq.von.append((t, mtm))
        kq.von_chot.append((t, so_du))
        kq.so_mo.append((t, so_mo))
    if moc:
        ap_su_kien(moc[-1])                 # sự kiện cùng giờ cuối (vd lệnh đặt ở nến cuối bị huỷ ngay)
    kq.thong_tin = {"nam": nam, "ro": ds, "bat_dau": chuoi_gio(bd), "ket_thuc": chuoi_gio(kt),
                    "cat_tai": chuoi_gio(ve_ts(cat_tai)) if cat_tai is not None else "",
                    "von_cuoi": so_du, "sha256": {m: du_lieu[m].get("sha256", {}) for m in ds}}
    return kq


# ======================= view tại 1 thời điểm (độ giống, nhận định) =======================
def view_tai(tai_san, t_utc, du_lieu=None):
    """TK 4 — view H4 tại thời điểm t (UTC): CẮT dữ liệu tại t rồi tính lại, lấy lần đóng H4 cuối ≤ t.
    Trả {"pha","view","kieu","ly_do","gio_cat" (datetime UTC giờ đóng nến H4 cuối dùng),"gio_cat_ts"}."""
    t = ve_ts(t_utc)
    du = _lay_du(du_lieu, tai_san)
    cb = cat_du_lieu(du, t)["cb"]
    if not cb.dong:
        return {"pha": None, "view": "CHUA_DU", "kieu": "CHUA_DU", "ly_do": "khong_co_nen_H4", "gio_cat": None,
                "gio_cat_ts": None}
    k = len(cb.dong) - 1
    return {"pha": cb.pha[k], "view": cb.view[k], "kieu": cb.kieu[k], "ly_do": cb.ly_do[k],
            "gio_cat": dt.datetime.fromtimestamp(cb.dong[k], UTC), "gio_cat_ts": cb.dong[k]}


# ======================= đầu ra TK 8 =======================
COT_LENH = ["tai_san", "loai", "chieu", "t_quyet_dinh", "t_khop", "gia_vao", "sl", "tp1", "tp2", "t_tp1", "t_ra",
            "gia_ra", "ly_do_ra", "khoi_luong", "don_bay", "phi", "lai_usd", "R", "von_sau"]
COT_LENH_THEM = ["gia_dat", "gia_tp1", "ti_le_tp1", "rui_ro_usd", "ky_quy", "gio_dung", "ly_do_huy", "vung", "ghi"]
COT_GIO = {"t_quyet_dinh", "t_khop", "t_tp1", "t_ra"}


def _o(v, cot=""):
    if v is None:
        return ""
    if cot in COT_GIO:
        return chuoi_gio(v)
    if isinstance(v, float):
        return repr(v)
    return v


def sut_giam_max(von, von_dau=None):
    dinh, mx = (von_dau if von_dau is not None else -1e18), 0.0
    for _, v in von:
        dinh = max(dinh, v)
        if dinh > 0:
            mx = max(mx, (dinh - v) / dinh)
    return mx


def _thong_ke(ds):
    n = len(ds)
    duong = sum(r["lai_usd"] for r in ds if r["lai_usd"] > 0)
    am = -sum(r["lai_usd"] for r in ds if r["lai_usd"] < 0)
    return {"so_lenh": n, "lai_usd": sum(r["lai_usd"] for r in ds),
            "ti_le_thang": (sum(1 for r in ds if r["lai_usd"] > 0) / n) if n else 0.0,
            "R_tb": (sum(r["R"] for r in ds) / n) if n else 0.0,
            "he_so_ln": (duong / am) if am > 0 else (None if duong == 0 else float("inf"))}


def tom_tat(kq):
    """Tóm tắt: lệnh = lệnh ĐÃ KHỚP (không tính HUY); thắng = lai_usd > 0 (DG 24); sụt giảm trên von theo giá (DG 25)."""
    v0 = P["von_dau"]
    khop = [r for r in kq.lenh if r["ly_do_ra"] not in ("HUY", "DANG_CHO", "DANG_MO")]
    v_cuoi = kq.von_chot[-1][1] if kq.von_chot else v0
    tt = {"nam": kq.thong_tin.get("nam"), "ro": kq.thong_tin.get("ro"), "bat_dau": kq.thong_tin.get("bat_dau"),
          "ket_thuc": kq.thong_tin.get("ket_thuc"), "von_dau": v0, "von_cuoi": v_cuoi, "lai_usd": v_cuoi - v0,
          "lai_pct": (v_cuoi - v0) / v0, "sut_giam_max": sut_giam_max(kq.von, v0),
          "so_lenh_dat": len(kq.lenh), "so_lenh_huy": sum(1 for r in kq.lenh if r["ly_do_ra"] == "HUY"),
          "so_lenh_con_mo": sum(1 for r in kq.lenh if r["ly_do_ra"] in ("DANG_CHO", "DANG_MO"))}
    tt.update(_thong_ke(khop))
    tt["theo_tai_san"] = {m: _thong_ke([r for r in khop if r["tai_san"] == m]) for m in kq.thong_tin.get("ro", [])}
    tt["theo_loai"] = {lo: _thong_ke([r for r in khop if r["loai"] == lo]) for lo in ("chinh", "hoi")}
    ly = {}
    for r in khop:
        ly[r["ly_do_ra"]] = ly.get(r["ly_do_ra"], 0) + 1
    tt["ly_do_ra"] = ly
    dem = {}
    for q in kq.quyet_dinh:
        key = q["hanh_dong"] + (":" + q["ly_do_bo"].split(" ")[0].split(":")[0] if q["ly_do_bo"] else "")
        dem[key] = dem.get(key, 0) + 1
    tt["dem_quyet_dinh"] = dict(sorted(dem.items()))
    tt["sha256_du_lieu"] = kq.thong_tin.get("sha256")
    tt["tham_so"] = THAM_SO
    return tt


def ghi_ket_qua(kq, thu_muc):
    tm = Path(thu_muc)
    tm.mkdir(parents=True, exist_ok=True)
    with (tm / "lenh.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COT_LENH + COT_LENH_THEM)
        for r in kq.lenh:
            w.writerow([_o(r.get(c), c) for c in COT_LENH + COT_LENH_THEM])
    with (tm / "von.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ts_utc", "von", "von_chot", "so_vi_the_mo"])   # ts_utc = giờ ĐÓNG nến H4 (DG 25)
        for (t, v), (_, vc), (_, n) in zip(kq.von, kq.von_chot, kq.so_mo):
            w.writerow([chuoi_gio(t), repr(v), repr(vc), n])
    with (tm / "quyet_dinh.csv").open("w", newline="") as f:
        w = csv.writer(f)
        cot = ["ts", "tai_san", "pha", "view", "kieu", "ly_do", "hanh_dong", "vung", "ly_do_bo"]
        w.writerow(["ts_utc"] + cot[1:])
        for q in kq.quyet_dinh:
            w.writerow([chuoi_gio(q["ts"])] + [q[c] for c in cot[1:]])
    tt = tom_tat(kq)
    (tm / "tom_tat.json").write_text(json.dumps(tt, ensure_ascii=False, indent=2, default=str) + "\n")
    return tt


if __name__ == "__main__":
    print(json.dumps(THAM_SO, ensure_ascii=False, indent=2))
