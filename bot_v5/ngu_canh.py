#!/usr/bin/env python3
"""Hồ sơ NGỮ CẢNH tại thời điểm T cho bot v5 — đúng thứ người phân tích (FAM Trading) nhìn (sổ tay A1, A4, A5, A6).

Cách dùng (T là giờ VN, nến cuối dùng = nến ĐÃ ĐÓNG có giờ đóng ≤ T):
  python3 bot_v5/ngu_canh.py BTC 4H "2026-08-14 11:00"
  python3 bot_v5/ngu_canh.py ETH 1D "2026-10-01 07:00" --json
  python3 bot_v5/ngu_canh.py VANG 4H "2026-09-21 11:00" --so-nen 20
Tuỳ chọn: --json (in JSON thay Markdown) · --so-nen N (số nến mỗi bảng, mặc định 30) · --utc (T là giờ UTC)
          --cache DIR (thư mục cache, mặc định bot_v5/cache) · --offline (chỉ đọc cache, không gọi mạng)
MÃ: mọi coin OKX `<MÃ>-USDT` (spot, không có thì -USDT-SWAP); VANG, DAU, DXY, NASDAQ qua Yahoo.
KHUNG: 15m / 1H / 4H / 1D / 1W (chấp nhận cả H4, D1, W1, H1, M15).

NHÂN QUẢ: mọi chuỗi nến được cắt ở giờ ĐÓNG ≤ T trước khi tính (EMA, RSI, fractal, Fibo, trendline); cửa sổ dữ liệu cố
định theo T; tin/Polymarket/FOMC/F&G chỉ lấy bản ghi có thời điểm ≤ T (lịch công bố tương lai thì biết trước nên hợp lệ).
Crypto có thêm mục 7: gap CME (Yahoo BTC=F 1h, nến đóng ≤ T) và BTC.D / USDT.D proxy CMC (ảnh chụp ngày + 1 giờ ≤ T).
Kiểm: python3 bot_v5/kiem_tra_ngu_canh.py
"""
import argparse, bisect, datetime as dt, html, json, math, re, sys, time
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "cong_cu"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import chi_bao  # noqa: E402
import tin_tuc  # noqa: E402
import trendline as TL  # noqa: E402
import nen as NG  # noqa: E402

UTC, VN, NGAY = NG.UTC, NG.VN, NG.NGAY
MOC_NHO = dt.datetime(2026, 7, 1, tzinfo=VN)
FNG_URL = "https://api.alternative.me/fng/?limit=0"
K_FRACTAL = 3
VOL_VUOT = 1.5
FIBO_TL = (0.382, 0.5, 0.618, 0.786)
FIBO_MR = (1.0, 1.618)
FIBO_GIAM_TUAN = (0.236, 0.382, 0.5, 0.618)  # thoái lui nhịp giảm từ đỉnh chu kỳ (0.382 cản yếu, 0.5 cản mạnh [10-01])
TEN_KHUNG = {"15m": "M15", "1H": "H1", "4H": "H4", "1D": "D1", "1W": "W1 (tuần)", "1M": "Tháng"}
CHUAN_KHUNG = {"15M": "15m", "M15": "15m", "1H": "1H", "H1": "1H", "4H": "4H", "H4": "4H", "1D": "1D", "D1": "1D",
               "D": "1D", "1W": "1W", "W1": "1W", "W": "1W"}
THU = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


# ======================= tiện ích =======================
def so_le(ref):
    if not ref or ref <= 0:
        return 2
    return max(0, min(10, 4 - int(math.floor(math.log10(ref)))))


def fg(x, d):
    return "—" if x is None else f"{x:,.{d}f}"


def fp(x, d=2):
    return "—" if x is None else f"{x:+.{d}f}%"


def fv(x):
    if x is None:
        return "—"
    a = abs(x)
    for nguong, hau in ((1e9, "B"), (1e6, "M"), (1e3, "k")):
        if a >= nguong:
            return f"{x / nguong:.2f}{hau}"
    return f"{x:.2f}"


def pct(a, b):
    return None if a is None or b in (None, 0) else (a - b) / b * 100


def vn(ts):
    return NG.s_vn(ts)


def doc_t(s, la_utc=False):
    s = s.strip().replace("T", " ")
    if len(s) == 10:
        s += " 07:00"
    d = dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M")
    return int(d.replace(tzinfo=UTC if la_utc else VN).timestamp())


# ======================= phân tích 1 khung =======================
def _loai_L01(gia, e34h, e34l, e34c, e89, e200):
    """Phân loại kiểu L01 tại một nến: TĂNG / GIẢM / HỖN HỢP theo giá – dải EMA34 – EMA89 – EMA200."""
    if None in (e34h, e89, e200):
        return "chưa đủ dữ liệu EMA200"
    if gia > e34h and e34c > e89 > e200:
        return "TĂNG (giá > dải 34 > 89 > 200)"
    if gia < e34l and e34c < e89 < e200:
        return "GIẢM (giá < dải 34 < 89 < 200)"
    return "HỖN HỢP"


def _vi_tri_dai(gia, hi, lo):
    return "TRÊN dải" if gia > hi else ("DƯỚI dải" if gia < lo else "TRONG dải")


def _cham(lo, hi, ds_l, ds_h, i0):
    """Số đợt (chuỗi nến liền nhau = 1) có râu cắt vùng [lo_i, hi_i] từ nến i0 tới cuối."""
    dem, truoc = 0, False
    for i in range(i0, len(ds_h)):
        if lo[i] is None:
            truoc = False
            continue
        co = ds_l[i] <= hi[i] and ds_h[i] >= lo[i]
        if co and not truoc:
            dem += 1
        truoc = co
    return dem


def _trang_thai_muc(kieu, i, muc, h, l, c, nhan):
    """Đỉnh (kieu='dinh') / đáy sau nến i: đóng vượt? râu quét? còn nguyên?"""
    rau = False
    for j in range(i + 1, len(c)):
        if (kieu == "dinh" and c[j] > muc) or (kieu == "day" and c[j] < muc):
            return f"đã bị ĐÓNG {'vượt' if kieu == 'dinh' else 'thủng'} ({nhan[j]})"
        if (kieu == "dinh" and h[j] > muc) or (kieu == "day" and l[j] < muc):
            rau = True
    return "râu quét qua, chưa đóng qua" if rau else "còn nguyên"


def phan_tich(nen, khung, so_nen):
    n = len(nen)
    o = [x.o for x in nen]; h = [x.h for x in nen]; l = [x.l for x in nen]
    c = [x.c for x in nen]; v = [x.v for x in nen]; nhan = [x.nhan for x in nen]
    e34h, e34l, e34c = chi_bao.ema(h, 34), chi_bao.ema(l, 34), chi_bao.ema(c, 34)
    e89, e200, e610 = chi_bao.ema(c, 89), chi_bao.ema(c, 200), chi_bao.ema(c, 610)
    rsi = chi_bao.rsi_wilder(c, 14)
    atr = chi_bao.atr_wilder(h, l, c, 14)
    vx = [None] * n
    for i in range(20, n):
        tb = sum(v[i - 20:i]) / 20
        vx[i] = v[i] / tb if tb > 0 else None

    def rau_dai(i):
        than = abs(c[i] - o[i])
        rt, rd = h[i] - max(o[i], c[i]), min(o[i], c[i]) - l[i]
        san = 0.5 * atr[i] if atr[i] else 0
        return (rt > 2 * than and rt >= san and rt > 0), (rd > 2 * than and rd >= san and rd > 0)

    bang = []
    for i in range(max(0, n - so_nen), n):
        rt_d, rd_d = rau_dai(i)
        ghi = []
        if vx[i] is not None and vx[i] >= VOL_VUOT:
            ghi.append("VOL VƯỢT")
        if rt_d:
            ghi.append("râu trên dài")
        if rd_d:
            ghi.append("râu dưới dài")
        bang.append({"nhan": nhan[i], "mo_utc": NG.s_utc(nen[i].mo), "dong_utc": NG.s_utc(nen[i].dong),
                     "o": o[i], "h": h[i], "l": l[i], "c": c[i],
                     "than_pct": pct(c[i], o[i]), "rau_tren_pct": (h[i] - max(o[i], c[i])) / o[i] * 100,
                     "rau_duoi_pct": (min(o[i], c[i]) - l[i]) / o[i] * 100, "vol": v[i], "vol_x_tb20": vx[i],
                     "vol_vuot": bool(vx[i] is not None and vx[i] >= VOL_VUOT), "rau_tren_dai": rt_d,
                     "rau_duoi_dai": rd_d, "rsi14": rsi[i]})

    cuoi = n - 1
    gia = c[cuoi]
    i30 = max(0, n - 30)

    def duong(ten, ds):
        x = ds[cuoi]
        if x is None:
            return {"ten": ten, "gia": None}
        doc5 = pct(x, ds[cuoi - 5]) if cuoi >= 5 and ds[cuoi - 5] is not None else None
        return {"ten": ten, "gia": x, "cach_pct": pct(gia, x), "vi_tri": "trên" if gia > x else "dưới",
                "doc_5_nen_pct": doc5, "so_dot_cham_30": _cham(ds, ds, l, h, i30)}

    ema = {"ema89": duong("EMA89", e89), "ema200": duong("EMA200", e200), "ema610": duong("EMA610", e610)}
    if e34h[cuoi] is not None:
        hi, lo = e34h[cuoi], e34l[cuoi]
        vt = _vi_tri_dai(gia, hi, lo)
        mep = hi if abs(gia - hi) <= abs(gia - lo) else lo
        ema["ema34"] = {"ten": "EMA34 dải", "high": hi, "close": e34c[cuoi], "low": lo, "vi_tri": vt,
                        "mep_gan": mep, "cach_mep_pct": pct(gia, mep),
                        "doc_5_nen_pct": pct(e34c[cuoi], e34c[cuoi - 5]) if cuoi >= 5 and e34c[cuoi - 5] else None,
                        "so_dot_cham_30": _cham(e34l, e34h, l, h, i30)}
    else:
        ema["ema34"] = {"ten": "EMA34 dải", "high": None}
    # thứ tự + phân loại kiểu L01
    ds = [("giá", gia), ("EMA34", e34c[cuoi]), ("EMA89", e89[cuoi]), ("EMA200", e200[cuoi]), ("EMA610", e610[cuoi])]
    ds = [x for x in ds if x[1] is not None]
    thu_tu = " > ".join(t for t, _ in sorted(ds, key=lambda z: -z[1]))
    loai = _loai_L01(gia, e34h[cuoi], e34l[cuoi], e34c[cuoi], e89[cuoi], e200[cuoi])
    r30 = [x for x in rsi[i30:] if x is not None]
    chi = {"gia_dong": gia, "ema": ema, "thu_tu": thu_tu, "phan_loai_L01": loai,
           "rsi14": rsi[cuoi], "rsi_min_30": min(r30) if r30 else None, "rsi_max_30": max(r30) if r30 else None,
           "atr14": atr[cuoi], "vol_x_tb20_nen_cuoi": vx[cuoi]}

    # fractal (râu + thân của nến pivot), trạng thái sau đó
    dinh, day = chi_bao.fractal(h, l, K_FRACTAL)
    fr = {"dinh": [], "day": []}
    for kieu, ds_p in (("dinh", dinh), ("day", day)):
        for i, p in ds_p[-8:]:
            than = max(o[i], c[i]) if kieu == "dinh" else min(o[i], c[i])
            fr[kieu].append({"nhan": nhan[i], "rau": p, "than": than, "cach_pct": pct(p, gia),
                             "trang_thai": _trang_thai_muc(kieu, i, p, h, l, c, nhan)})
    # bậc thang S/R: mọi đỉnh/đáy fractal trong ~150 nến gần nhất (W1/M: cả cửa sổ), gần giá nhất mỗi phía
    i_tu = 0 if khung in ("1W", "1M") else max(0, n - 150)
    muc = []
    for kieu, ds_p in (("đỉnh", dinh), ("đáy", day)):
        for i, p in ds_p:
            if i < i_tu:
                continue
            doi_vai = (kieu == "đáy" and p > gia) or (kieu == "đỉnh" and p < gia)
            muc.append({"gia": p, "loai": kieu, "nhan": nhan[i], "cach_pct": pct(p, gia), "doi_vai": doi_vai})
    tren = sorted([m for m in muc if m["gia"] > gia], key=lambda m: m["gia"])[:5]
    duoi = sorted([m for m in muc if m["gia"] <= gia], key=lambda m: -m["gia"])[:5]

    # râu dài chưa test lại hết (100 nến gần nhất)
    rau = []
    for i in range(max(0, n - 100), n):
        rt_d, rd_d = rau_dai(i)
        for co, phia in ((rt_d, "trên"), (rd_d, "dưới")):
            if not co:
                continue
            if phia == "trên":
                goc, dau = max(o[i], c[i]), h[i]
                xa = max(h[i + 1:]) if i + 1 < n else None
                lap = 0.0 if xa is None else max(0.0, min(1.0, (xa - goc) / (dau - goc)))
            else:
                goc, dau = min(o[i], c[i]), l[i]
                xa = min(l[i + 1:]) if i + 1 < n else None
                lap = 0.0 if xa is None else max(0.0, min(1.0, (goc - xa) / (goc - dau)))
            if lap >= 1.0:
                continue
            rau.append({"nhan": nhan[i], "phia": phia, "goc_than": goc, "dau_rau": dau, "giua_rau": (goc + dau) / 2,
                        "dai_x_than": (abs(dau - goc) / abs(c[i] - o[i])) if c[i] != o[i] else None,
                        "da_lap_pct": lap * 100, "chua_cham": lap == 0.0, "cach_dau_rau_pct": pct(dau, gia)})
    rau = sorted(rau, key=lambda r: r["nhan"], reverse=True)[:8]
    return {"chi_bao": chi, "bang": bang, "fractal": fr, "bac_thang": {"tren": tren, "duoi": duoi}, "rau_dai": rau}


def nen_dang_chay(lon_nen, nho_ds, t):
    """Nến khung lớn ĐANG CHẠY tại t, dựng từ nến khung nhỏ đã đóng ≤ t (không phải dữ liệu sau t)."""
    if not lon_nen:
        return None
    D = lon_nen[-1].dong
    for ten, nho in nho_ds:
        if not nho or nho[0].mo > D:
            continue
        ds = [x for x in nho if x.mo >= D and x.dong <= t]
        if not ds:
            return None
        return {"tu_nen": ten, "mo_vn": vn(D), "den_vn": vn(ds[-1].dong), "so_nen_nho": len(ds), "o": ds[0].o,
                "h": max(x.h for x in ds), "l": min(x.l for x in ds), "c": ds[-1].c, "vol": sum(x.v for x in ds)}
    return None


def trang_thai_truoc(h4, d1, t, gio=24):
    """Trạng thái lúc T−gio: nến H4 cuối đã ĐÓNG ≤ T−gio (L01, giá so với dải EMA34 / EMA89 / EMA200 H4) + nến D1 cuối
    đã đóng ≤ T−gio (màu, đóng). EMA tính trên cùng cửa sổ H4 của T nhưng chỉ đọc tại nến ≤ T−gio (EMA đệ quy → nhân quả)."""
    tm = t - gio * 3600
    ra = {"gio_truoc": gio, "luc_vn": vn(tm), "h4": None, "d1": None}
    j = bisect.bisect_right([x.dong for x in h4], tm) - 1
    if j >= 0:
        h = [x.h for x in h4[:j + 1]]; l = [x.l for x in h4[:j + 1]]; c = [x.c for x in h4[:j + 1]]
        e34h, e34l, e34c = chi_bao.ema(h, 34)[-1], chi_bao.ema(l, 34)[-1], chi_bao.ema(c, 34)[-1]
        e89, e200 = chi_bao.ema(c, 89)[-1], chi_bao.ema(c, 200)[-1]
        gia = c[-1]
        ra["h4"] = {"nhan": h4[j].nhan, "dong": gia, "than_pct": pct(gia, h4[j].o),
                    "ema34_high": e34h, "ema34_low": e34l, "ema34_close": e34c, "ema89": e89, "ema200": e200,
                    "vi_tri_dai_34": None if e34h is None else _vi_tri_dai(gia, e34h, e34l),
                    "vi_tri_89": None if e89 is None else ("trên" if gia > e89 else "dưới"),
                    "vi_tri_200": None if e200 is None else ("trên" if gia > e200 else "dưới"),
                    "phan_loai_L01": _loai_L01(gia, e34h, e34l, e34c, e89, e200)}
    k = bisect.bisect_right([x.dong for x in d1], tm) - 1
    if k >= 0:
        x = d1[k]
        ra["d1"] = {"nhan": x.nhan, "o": x.o, "c": x.c, "than_pct": pct(x.c, x.o),
                    "mau": "xanh" if x.c > x.o else ("đỏ" if x.c < x.o else "doji")}
    return ra


# ======================= Fibo =======================
def zigzag(h, l, k=K_FRACTAL):
    dinh, day = chi_bao.fractal(h, l, k)
    pts = sorted([(i, p, "H") for i, p in dinh] + [(i, p, "L") for i, p in day], key=lambda x: (x[0], x[2] != "H"))
    zz = []
    for i, p, kind in pts:
        if zz and zz[-1][2] == kind:
            if (kind == "H" and p > zz[-1][1]) or (kind == "L" and p < zz[-1][1]):
                zz[-1] = (i, p, kind)
            continue
        if zz and ((kind == "H" and p <= zz[-1][1]) or (kind == "L" and p >= zz[-1][1])):
            continue
        zz.append((i, p, kind))
    return zz


def _muc_tl(a, b, gia):
    """Thoái lui của nhịp a→b: mức = b + (a − b)·r (đo từ điểm cuối b lùi về a)."""
    return [{"ty_le": r, "gia": b + (a - b) * r, "cach_pct": pct(b + (a - b) * r, gia)} for r in FIBO_TL]


def _diem(nen, i, p, kind):
    return {"nhan": nen[i].nhan, "gia": p, "loai": "đỉnh" if kind == "H" else "đáy"}


def fibo_khung(nen, khung, n_lon):
    h = [x.h for x in nen]; l = [x.l for x in nen]
    n = len(nen)
    gia = nen[-1].c
    ra = {"khung": khung, "gia": gia}
    zz = zigzag(h, l)
    if len(zz) >= 2:
        A, B = zz[-2], zz[-1]
        ra["nhip_gan_nhat"] = {"tu": _diem(nen, *A), "den": _diem(nen, *B),
                               "chieu": "tăng" if B[2] == "H" else "giảm", "muc": _muc_tl(A[1], B[1], gia)}
        sau = range(B[0] + 1, n)
        if len(sau):
            if B[2] == "H":
                j = max(sau, key=lambda i: (h[i], -i))
                if h[j] > B[1]:
                    dc = {"tu": _diem(nen, *A), "den": _diem(nen, j, h[j], "H"), "chieu": "tăng (nối dài, đỉnh chưa xác nhận)",
                          "muc": _muc_tl(A[1], h[j], gia)}
                else:
                    j = min(sau, key=lambda i: (l[i], -i))
                    dc = {"tu": _diem(nen, *B), "den": _diem(nen, j, l[j], "L"), "chieu": "giảm (đang chạy, đáy chưa xác nhận)",
                          "muc": _muc_tl(B[1], l[j], gia)}
                    if l[j] > A[1]:
                        dc["mo_rong_3_diem"] = _mo_rong(nen, A, B, (j, l[j], "L"), gia, h, l, chua_xn=True)
            else:
                j = min(sau, key=lambda i: (l[i], -i))
                if l[j] < B[1]:
                    dc = {"tu": _diem(nen, *A), "den": _diem(nen, j, l[j], "L"), "chieu": "giảm (nối dài, đáy chưa xác nhận)",
                          "muc": _muc_tl(A[1], l[j], gia)}
                else:
                    j = max(sau, key=lambda i: (h[i], -i))
                    dc = {"tu": _diem(nen, *B), "den": _diem(nen, j, h[j], "H"), "chieu": "tăng (đang chạy, đỉnh chưa xác nhận)",
                          "muc": _muc_tl(B[1], h[j], gia)}
                    if h[j] < A[1]:
                        dc["mo_rong_3_diem"] = _mo_rong(nen, A, B, (j, h[j], "H"), gia, h, l, chua_xn=True)
            ra["nhip_dang_chay"] = dc
    if len(zz) >= 3:
        ra["mo_rong_3_diem"] = _mo_rong(nen, zz[-3], zz[-2], zz[-1], gia, h, l)
    ra["nhip_lon"] = nhip_lon(nen, n_lon)
    return ra


def _mo_rong(nen, P1, P2, P3, gia, h, l, chua_xn=False):
    len_ = P2[1] > P1[1]
    muc = []
    for r in FIBO_MR:
        x = P3[1] + (P2[1] - P1[1]) * r
        sau = range(P3[0] + 1, len(nen))
        cham = any(h[i] >= x for i in sau) if len_ else any(l[i] <= x for i in sau)
        muc.append({"ty_le": r, "gia": x, "cach_pct": pct(x, gia), "da_cham_sau_diem_3": cham})
    return {"diem_1": _diem(nen, *P1), "diem_2": _diem(nen, *P2), "diem_3": _diem(nen, *P3),
            "diem_3_chua_xac_nhan": chua_xn, "huong_dich": "lên" if len_ else "xuống", "muc": muc}


def nhip_lon(nen, so):
    ds = nen[-so:]
    if len(ds) < 5:
        return None
    gia = nen[-1].c
    imax = max(range(len(ds)), key=lambda i: (ds[i].h, -i))
    imin = min(range(len(ds)), key=lambda i: (ds[i].l, -i))
    hi, lo = ds[imax].h, ds[imin].l
    if imax > imin:
        return {"so_nen": len(ds), "tu": {"nhan": ds[imin].nhan, "gia": lo, "loai": "đáy"},
                "den": {"nhan": ds[imax].nhan, "gia": hi, "loai": "đỉnh"}, "chieu": "tăng", "muc": _muc_tl(lo, hi, gia)}
    return {"so_nen": len(ds), "tu": {"nhan": ds[imax].nhan, "gia": hi, "loai": "đỉnh"},
            "den": {"nhan": ds[imin].nhan, "gia": lo, "loai": "đáy"}, "chieu": "giảm", "muc": _muc_tl(hi, lo, gia)}


def nhip_giam_tu_dinh(nen, so):
    """Nhịp GIẢM từ đỉnh cao nhất (râu) trong `so` nến gần nhất tới đáy thấp nhất (râu) SAU đỉnh đó.
    Fibo thoái lui đo từ đáy lên: mức = đáy + (đỉnh − đáy)·r, r ∈ FIBO_GIAM_TUAN."""
    ds = nen[-so:]
    if len(ds) < 5:
        return None
    gia = nen[-1].c
    imax = max(range(len(ds)), key=lambda i: (ds[i].h, -i))
    ra = {"so_nen": len(ds), "tu": {"nhan": ds[imax].nhan, "gia": ds[imax].h, "loai": "đỉnh"}}
    if imax == len(ds) - 1:
        ra.update({"den": None, "ghi_chu": "đỉnh cao nhất là nến cuối đã đóng — chưa có nhịp giảm sau đỉnh"})
        return ra
    imin = min(range(imax + 1, len(ds)), key=lambda i: (ds[i].l, -i))
    hi, lo = ds[imax].h, ds[imin].l
    ra.update({"den": {"nhan": ds[imin].nhan, "gia": lo, "loai": "đáy"}, "chieu": "giảm",
               "day_la_nen_cuoi": imin == len(ds) - 1,
               "muc": [{"ty_le": r, "gia": lo + (hi - lo) * r, "cach_pct": pct(lo + (hi - lo) * r, gia)} for r in FIBO_GIAM_TUAN]})
    return ra


# ======================= Trendline =======================
def bien_the_khoa():
    p = GOC / "hoc_v5" / "trendline" / "CHON.md"
    if p.exists():
        for dong in p.read_text(encoding="utf-8").splitlines():
            if dong.startswith("BIEN_THE_KHOA:"):
                return dong.split(":", 1)[1].strip().strip("`"), "khoá theo hoc_v5/trendline/CHON.md"
    return "rau|3|dai|nhieu_cham", "TẠM (chưa có CHON.md)"


TT_TL = {"giu": "đang giữ (chưa phá)", "vua_pha_1n": "VỪA PHÁ 1 nến H4 (chưa xác nhận)",
         "vua_pha_2n": "VỪA PHÁ 2 nến H4 liên tiếp", "pha_gia": "PHÁ GIẢ (close đã quay lại)",
         "da_pha": "ĐÃ PHÁ THẬT (≤48h)", "pha_roi_test_lai": "phá thật RỒI TEST LẠI", "het_hieu_luc": "hết hiệu lực"}
TEN_LOAI = {"khang_cu_giam": "Kháng cự giảm (nối đỉnh hạ dần)", "ho_tro_tang": "Hỗ trợ tăng (nối đáy nâng dần)"}


def _nhan_vol(x):
    if x is None:
        return "không rõ vol"
    return "CÓ volume" if x >= 1.2 else ("volume yếu" if x < 0.8 else "volume trung bình")


def _tl_nen(khung, ds):
    dur = TL.GIAY[khung]
    return TL.Nen(khung, [x.dong - dur for x in ds], [x.o for x in ds], [x.h for x in ds], [x.l for x in ds],
                  [x.c for x in ds], [x.v for x in ds])


def _nhan_neo(khung, s_utc_mo):
    mo = NG.tu_s_utc(s_utc_mo)
    return vn(mo + TL.GIAY[khung]) if khung == "H4" else NG.utc_dt(mo).strftime("%Y-%m-%d")


def trendline_tai(h4, d1, t, rut_gon=False):
    ten, nguon = bien_the_khoa()
    bt = TL.bien_the(ten)
    if len(h4) < 30 or len(d1) < 10:
        return {"bien_the": ten, "nguon_bien_the": nguon, "loi": "không đủ nến H4/D1"}
    du = TL.BoDuLieu(_tl_nen("H4", h4), _tl_nen("D1", d1))
    kq = TL.tai_thoi_diem(du, t, bt)
    nhom = []
    for (khung, loai), v in kq.items():
        chinh = v["chinh"]
        ds = sorted(v["duong"], key=lambda r: abs(r["cach_pct"]) if r["cach_pct"] is not None else 1e9)
        khac = [r for r in ds if not chinh or r["id"] != chinh["id"]][: (0 if rut_gon else 4)]

        def gon(r, la_chinh):
            pha = r["pha"]
            return {"id": r["id"], "chinh": la_chinh, "neo1": _nhan_neo(r["khung"], r["neo1_ts"]), "neo1_gia": r["neo1_gia"],
                    "neo2": _nhan_neo(r["khung"], r["neo2_ts"]), "neo2_gia": r["neo2_gia"], "gia_tai_T": r["gia_t"],
                    "cach_pct": r["cach_pct"], "doc_moi_ngay": r["doc_ngay"],
                    "gia_sau_24h": r["gia_t"] + r["doc_ngay"], "gia_sau_48h": r["gia_t"] + 2 * r["doc_ngay"],
                    "so_cham": r["so_cham"],
                    "tuoi_ngay": r["tuoi_ngay"], "trang_thai": r["trang_thai"],
                    "pha": None if not pha else {"luc_vn": vn(pha["t_pha"]), "vol_x_tb20": pha["vol"],
                                                 "vol": _nhan_vol(pha["vol"]), "hai_nen": pha["hai_nen"],
                                                 "ket_qua": pha["ket_qua"], "gia_duong": pha["gia_duong"],
                                                 "dong": pha["dong"]}}
        _c0, sk = TL.su_kien_khoang(du, bt, khung, loai, t - 3 * NGAY, t)
        su_kien = [{"luc_vn": vn(z["t_pha"]), "id": z["id"], "chieu": "lên" if z["chieu"] == "len" else "xuống",
                    "vol_x_tb20": z["vol"],
                    "vol": _nhan_vol(z["vol"]), "hai_nen": z["hai_nen"], "ket_qua": z["ket_qua"],
                    "test_lai": z["test_lai"], "gia_duong": z["gia_duong"], "dong": z["dong"], "la_chinh": z["la_chinh"]}
                   for z in sk]
        nhom.append({"khung": khung, "loai": loai, "so_duong": len(ds),
                     "duong": ([gon(chinh, True)] if chinh else []) + [gon(r, False) for r in khac],
                     "su_kien_72h": su_kien})
    return {"bien_the": ten, "nguon_bien_the": nguon, "nhom": nhom}


# ======================= Tin / Fed / F&G =======================
TEN_KQ = {"No change": "giữ nguyên", "25 bps decrease": "giảm 25bps", "50+ bps decrease": "giảm ≥50bps",
          "25 bps increase": "tăng 25bps", "25+ bps increase": "tăng ≥25bps", "50+ bps increase": "tăng ≥50bps"}
THU_TU_KQ = ["50+ bps decrease", "25 bps decrease", "No change", "25 bps increase", "25+ bps increase", "50+ bps increase"]


def _pm_tai(chuoi, tau):
    ra = {}
    for kq, (ts, p) in chuoi.items():
        k = bisect.bisect_right(ts, tau) - 1
        if k >= 0:
            ra[kq] = (p[k], ts[k])
    return ra


def trich_thong_cao(ngay_et):
    """2–3 câu NGUYÊN VĂN về định hướng chính sách từ thông cáo FOMC (du_lieu/tin_tuc/_goc/fomc_statement_YYYYMMDD.html)."""
    p = Path(tin_tuc.THU_MUC) / "_goc" / f"fomc_statement_{ngay_et}.html"
    if not p.exists():
        return None
    s = p.read_text(encoding="utf-8", errors="replace")
    ps = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x))).strip()
          for x in re.findall(r"<p[^>]*>(.*?)</p>", s, flags=re.S)]
    i0 = next((i for i, x in enumerate(ps) if x.startswith("For release at")), None)
    if i0 is None:
        return None
    than = []
    for i, x in enumerate(ps[i0:]):
        if x.startswith(("For media inquiries", "Implementation Note")):
            break
        if i == 0:
            x = re.sub(r"^For release at .*?Share\s*(-->\s*)*", "", x)
        if x.startswith("Voting") or not x:
            continue
        than.append(x)
    cau = []
    for x in than:
        cau += [z.strip() for z in re.split(r"(?<=[.!?])\s+(?=[A-Z])", x) if z.strip()]
    tu = ["will", "would", "additional", "adjust", "determine", "timing", "timel", "prepared", "further", "future",
          "price stability", "bias"]
    phu = {"inflation": 0.6, "uncertain": 0.4, "risk": 0.4}  # trọng số thấp: chỉ lấp chỗ khi thông cáo ít câu định hướng
    diem = []
    for k, z in enumerate(cau):
        if z.startswith(("The Federal Open Market Committee approved", "The Committee seeks to achieve")):
            continue
        d = sum(1 for w in tu if w in z.lower()) + sum(x for w, x in phu.items() if w in z.lower())
        if d:
            diem.append((-d, k, z))
    chon = sorted(sorted(diem)[:3], key=lambda x: x[1])
    return {"file": f"du_lieu/tin_tuc/_goc/{p.name}", "cau": [z for _, _, z in chon]}


def fed_tai(t):
    d = tin_tuc._nap()
    fomc = [e for e in d["ev"] if e["su_kien"] == "FOMC"]
    ts_list = [int(e["ts_utc"].timestamp()) for e in fomc]
    k = bisect.bisect_right(ts_list, t)
    ra = {"cua_so_fomc": None, "ky_toi": None, "ky_vua_qua": None}
    # (1) Polymarket kỳ tới
    if k < len(fomc):
        e = fomc[k]
        t_qd = ts_list[k]
        kh = "2026-%02d" % e["ts_utc"].astimezone(tin_tuc.ET).month
        chuoi = d["pm"].get(kh, {})
        snap = {}
        for ten, tau in (("T", t), ("1d", t - NGAY), ("3d", t - 3 * NGAY), ("7d", t - 7 * NGAY)):
            x = _pm_tai(chuoi, dt.datetime.fromtimestamp(tau, UTC))
            tong = sum(p for p, _ in x.values())
            snap[ten] = {kq: {"yes": p, "chuan_hoa_pct": p / tong * 100 if tong else None, "ts_utc": ts.strftime("%Y-%m-%dT%H:%M:%SZ")}
                         for kq, (p, ts) in x.items()}
            snap[ten + "_tong_yes"] = tong
        dong = []
        for kq in sorted(snap["T"], key=lambda z: THU_TU_KQ.index(z) if z in THU_TU_KQ else 99):
            now_ = snap["T"][kq]["chuan_hoa_pct"]
            dong.append({"ket_qua": kq, "ten": TEN_KQ.get(kq, kq), "yes": snap["T"][kq]["yes"], "pct": now_,
                         **{f"doi_{x}": (now_ - snap[x][kq]["chuan_hoa_pct"]) if kq in snap[x] else None
                            for x in ("1d", "3d", "7d")}})
        moi = max((v["ts_utc"] for v in snap["T"].values()), default=None)
        ra["ky_toi"] = {"ky": e["ky"], "quyet_dinh_vn": vn(t_qd), "con_gio": (t_qd - t) / 3600, "polymarket_ma": kh,
                        "tong_yes": snap["T_tong_yes"], "ts_moi_nhat_utc": moi, "ket_qua": dong}
        if t_qd - t <= 72 * 3600:
            ra["cua_so_fomc"] = f"TRƯỚC FOMC {e['ky']}: còn {(t_qd - t) / 3600:.1f} giờ (quyết định {vn(t_qd)} VN)"
    # (2) kỳ gần nhất đã công bố ≤ T
    if k > 0:
        e = fomc[k - 1]
        t_qd = ts_list[k - 1]
        kq = d["kq"].get(e["ky"])
        ngay_et = e["ts_utc"].astimezone(tin_tuc.ET).strftime("%Y%m%d")
        ra["ky_vua_qua"] = {"ky": e["ky"], "quyet_dinh_vn": vn(t_qd), "cach_gio": (t - t_qd) / 3600,
                            "ket_qua": kq, "thong_cao": trich_thong_cao(ngay_et)}
        if t - t_qd <= 24 * 3600 and ra["cua_so_fomc"] is None:
            ra["cua_so_fomc"] = f"SAU FOMC {e['ky']}: {(t - t_qd) / 3600:.1f} giờ sau quyết định ({vn(t_qd)} VN)"
    return ra


def lay_fng(t, cache_dir, offline):
    p = Path(cache_dir) / "fng.json"
    ds = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    if (not ds or ds[-1][0] < t - t % NGAY) and not offline and t <= time.time():
        try:
            j = NG._get_json(FNG_URL, nghi=0.5)
            moi = {int(x["timestamp"]): [int(x["timestamp"]), int(x["value"]), x["value_classification"]] for x in j["data"]}
            for x in ds:
                moi.setdefault(x[0], x)
            ds = [moi[k] for k in sorted(moi)]
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(ds), encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            print(f"(cảnh báo: không tải được F&G: {e})", file=sys.stderr)
    ds = [x for x in ds if x[0] <= t]
    if not ds:
        return None
    cuoi = ds[-1]
    d30 = [x[1] for x in ds if x[0] > t - 30 * NGAY]
    tuan = [x for x in ds if x[0] > cuoi[0] - 7 * NGAY]
    return {"ngay_utc": NG.utc_dt(cuoi[0]).strftime("%Y-%m-%d"), "gia_tri": cuoi[1], "phan_loai": cuoi[2],
            "7_ngay": [[NG.utc_dt(x[0]).strftime("%m-%d"), x[1]] for x in tuan],
            "min_30": min(d30), "max_30": max(d30)}


# ======================= ngoài chart: gap CME, BTC.D, USDT.D =======================
GAP_NGHI = 3 * 3600   # giờ mở 2 nến CME 1h liền nhau cách > 3 giờ = nghỉ cuối tuần / lễ (nghỉ 1 giờ mỗi ngày không tính)
GAP_MIN_PCT = 0.5     # gap gốc nhỏ hơn → bỏ ("gap nhỏ thì bỏ qua")
GAP_CON_PCT = 0.1     # phần chưa lấp còn < 0,1% giá → coi như đã lấp
GAP_NGAY = 400
GAP_XA_PCT = 30


def gap_cme(t, cache_dir, offline):
    """Gap CME (Yahoo BTC=F 1h, nến đóng ≤ t): giá đóng trước kỳ nghỉ vs giá mở sau kỳ nghỉ. Lấp dần theo râu các nến
    sau đó; chỉ coi là lấp hết khi râu đi hết vùng (chạm một phần = phần còn lại vẫn là gap)."""
    try:
        goc = NG._yahoo_goc("CME", "1h", t, cache_dir, offline)
    except Exception as e:  # noqa: BLE001
        print(f"(cảnh báo: không tải được CME: {e})", file=sys.stderr)
        goc = NG._yahoo_goc("CME", "1h", t, cache_dir, True)
    nen = [x for x in goc if x[1] <= t and x[0] >= t - GAP_NGAY * NGAY]
    if len(nen) < 100:
        return {"loi": f"chỉ có {len(nen)} nến CME 1h đóng ≤ T"}
    gia, dong_cuoi = nen[-1][5], nen[-1][1]
    ds = []
    for i in range(1, len(nen)):
        a, b = nen[i - 1], nen[i]
        if b[0] - a[0] <= GAP_NGHI or abs(b[2] / a[5] - 1) * 100 < GAP_MIN_PCT:
            continue
        tang = b[2] > a[5]  # gap tăng → giá phải về lấp phía dưới
        lo, hi = min(a[5], b[2]), max(a[5], b[2])
        con_lo, con_hi, lap = lo, hi, None
        for x in nen[i:]:
            if tang:
                con_hi = min(con_hi, x[4])
            else:
                con_lo = max(con_lo, x[3])
            if con_hi - con_lo < GAP_CON_PCT / 100 * gia:
                lap = x[1]
                break
        ds.append({"tao_vn": vn(b[0]), "chieu": "tăng" if tang else "giảm", "lo": lo, "hi": hi,
                   "con_lo": con_lo, "con_hi": con_hi, "da_lap_pct": 100 * (1 - (con_hi - con_lo) / (hi - lo)),
                   "lap_luc": lap})
    ra = {"gia_cme": gia, "nen_cuoi_vn": vn(dong_cuoi), "nghi": dong_cuoi < t - GAP_NGHI, "tren": [], "duoi": [],
          "vua_lap_7_ngay": [dict(g, lap_vn=vn(g["lap_luc"])) for g in ds if g["lap_luc"] and g["lap_luc"] > t - 7 * NGAY]}
    for g in ds:
        if g["lap_luc"]:
            continue
        g["cach_pct"] = pct(g["con_lo"] if g["con_lo"] > gia else g["con_hi"], gia)
        if abs(g["cach_pct"]) <= GAP_XA_PCT:
            ra["tren" if g["con_lo"] > gia else "duoi"].append(g)
    for k in ("tren", "duoi"):
        ra[k] = sorted(ra[k], key=lambda g: abs(g["cach_pct"]))[:4]
    # chênh CME − spot ở giờ đóng H4 gần nhất có cả hai → quy gap về giá spot gần đúng
    ra["chenh_spot"] = None
    try:
        _n, h4 = NG.lay_chuoi("BTC", "4H", t, cache_dir, offline)
        spot = {x.dong: x.c for x in h4}
        for x in reversed(nen[-48:]):
            if x[1] in spot:
                ra["chenh_spot"] = x[5] - spot[x[1]]
                break
    except NG.LoiDuLieu:
        pass
    return ra


def dom_tai(t, cache_dir, offline):
    """BTC.D / USDT.D proxy CMC theo ngày (điểm đã công bố ≤ t), cửa sổ 365 ngày trước t."""
    try:
        ds = NG.lay_dom(t, cache_dir, offline)
    except Exception as e:  # noqa: BLE001
        print(f"(cảnh báo: không tải được CMC: {e})", file=sys.stderr)
        ds = NG.lay_dom(t, cache_dir, True)
    ra = {}
    for k, chuoi in ds.items():
        chuoi = [x for x in chuoi if x[0] >= t - 365 * NGAY]
        if len(chuoi) < 90:
            ra[k] = {"loi": f"chỉ có {len(chuoi)} ngày ≤ T"}
            continue
        v = [x[2] for x in chuoi]
        e34, e89 = chi_bao.ema(v, 34)[-1], chi_bao.ema(v, 89)[-1]
        th30 = chuoi[-30:]
        ra[k] = {"ngay_vn": vn(chuoi[-1][0]), "gia_tri": v[-1], "doi_1": v[-1] - v[-2], "doi_7": v[-1] - v[-8],
                 "doi_30": v[-1] - v[-31], "ema34": e34, "ema89": e89,
                 "cao_30": max(th30, key=lambda x: x[2]), "thap_30": min(th30, key=lambda x: x[2]),
                 "10_ngay": [[dt.datetime.fromtimestamp(x[0], VN).strftime("%m-%d"), x[2]] for x in chuoi[-10:]]}
    return ra


# ======================= thời gian =======================
def thoi_gian(t):
    d = dt.datetime.fromtimestamp(t, VN)
    g = d.hour + d.minute / 60
    phien = ("phiên Á" if 6 <= g < 14 else "phiên Âu" if 14 <= g < 20 else "phiên Mỹ" if (g >= 20 or g < 4)
             else "cuối phiên Mỹ / nghỉ")
    ra = {"thu": THU[d.weekday()], "gio_vn": d.strftime("%H:%M"), "phien": phien,
          "h4_dang_chay_dong_luc": vn(NG.mo_nen_chua(t, "4H") + 14400),
          "d1_dang_chay_dong_luc": vn(NG.mo_nen_chua(t, "1D") + NGAY),
          "w1_dang_chay_dong_luc": vn(NG.mo_nen_chua(t, "1W") + 7 * NGAY),
          "thang_dang_chay_dong_luc": vn(NG.dong_nen(NG.mo_nen_chua(t, "1M"), "1M")), "co": []}
    if d.weekday() == 0:
        ra["co"].append("THỨ HAI: buổi khung tuần (view lại nến tuần vừa đóng; nến D1 thứ Hai xanh hay đỏ không tự đổi view)")
    if d.weekday() == 4:
        ra["co"].append("THỨ SÁU: thận trọng, view dùng cho cả cuối tuần")
    if d.weekday() >= 5:
        ra["co"].append("CUỐI TUẦN: T7–CN thường chạy chung một nhịp")
    if d.day <= 3:
        ra["co"].append("ĐẦU THÁNG: view lại nến tháng")
    cuoi_thang = (d + dt.timedelta(days=3)).month != d.month
    if cuoi_thang:
        ra["co"].append("CUỐI THÁNG: sắp đóng nến tháng")
    return ra


# ======================= hồ sơ =======================
def tao_ho_so(ma, khung, t, so_nen=30, cache_dir=None, offline=False):
    ma = ma.upper()
    khung = CHUAN_KHUNG.get(khung.upper(), khung)
    if khung not in ("15m", "1H", "4H", "1D", "1W"):
        raise NG.LoiDuLieu(f"khung {khung} không hỗ trợ (15m/1H/4H/1D/1W)")
    if t > time.time():
        raise NG.LoiDuLieu("T ở tương lai")
    if ma not in NG.YAHOO:
        NG.giai_inst(ma, cache_dir, offline)  # mã không có trên OKX → báo lỗi ngay, không thử từng khung
    ds_khung = [k for k in ("1M", "1W", "1D", "4H") if k != khung]
    ds_khung = sorted(set(ds_khung + [khung]), key=lambda k: NG.KHUNG.index(k), reverse=True)
    chuoi, nguon = {}, None
    for k in ds_khung:
        try:
            nguon_k, chuoi[k] = NG.lay_chuoi(ma, k, t, cache_dir, offline)
            nguon = nguon or nguon_k
        except NG.LoiDuLieu as e:
            chuoi[k] = []
            if k == khung:
                raise
            print(f"(cảnh báo {k}: {e})", file=sys.stderr)
    hoi = chuoi[khung]
    if not hoi:
        raise NG.LoiDuLieu(f"{ma} {khung}: không có nến nào đóng ≤ T")
    gia = hoi[-1].c
    hs = {"ma": ma, "nguon": nguon, "khung": khung, "t_vn": vn(t), "t_utc": NG.s_utc(t), "so_le": so_le(gia),
          "nen_cuoi": {"mo_vn": vn(hoi[-1].mo), "dong_vn": vn(hoi[-1].dong), "close": gia},
          "canh_bao": [], "thoi_gian": thoi_gian(t)}
    hs["truoc_24h"] = trang_thai_truoc(chuoi.get("4H", []), chuoi.get("1D", []), t)
    if t < MOC_NHO.timestamp():
        hs["canh_bao"].append("T trước 2026-07-01: model có thể NHỚ diễn biến thật sau T — tuyệt đối chỉ dựa trên hồ sơ này.")
    if hoi[-1].dong < t - 3 * NG.GIAY.get(khung, 7 * NGAY):
        hs["canh_bao"].append(f"Nến {khung} cuối cách T khá xa ({vn(hoi[-1].dong)}) — thị trường nghỉ hoặc thiếu dữ liệu.")
    # 1–2. từng khung
    nho_ds = sorted([(k, chuoi[k]) for k in ds_khung if chuoi[k]], key=lambda z: NG.KHUNG.index(z[0]))
    hs["khung_ds"] = []
    for k in ds_khung:
        ds = chuoi[k]
        muc = {"khung": k, "ten": TEN_KHUNG[k], "so_nen_cua_so": len(ds)}
        if len(ds) < 5:
            muc["thieu"] = f"chỉ có {len(ds)} nến đã đóng ≤ T"
        else:
            muc.update(phan_tich(ds, k, so_nen))
            nho = [z for z in nho_ds if NG.KHUNG.index(z[0]) < NG.KHUNG.index(k)]
            muc["dang_chay"] = nen_dang_chay(ds, nho, t)
        hs["khung_ds"].append(muc)
    # 3. Fibo
    hs["fibo"] = []
    for k in dict.fromkeys([khung, "1D"]):
        if len(chuoi.get(k, [])) >= 10:
            hs["fibo"].append(fibo_khung(chuoi[k], k, 90))
    if khung != "1W" and len(chuoi.get("1W", [])) >= 10:
        hs["fibo_tuan_nhip_lon"] = nhip_lon(chuoi["1W"], 104)
    if len(chuoi.get("1W", [])) >= 10:
        hs["fibo_tuan_nhip_giam"] = nhip_giam_tu_dinh(chuoi["1W"], 104)
    # 4. Trendline
    try:
        hs["trendline"] = trendline_tai(chuoi.get("4H", []), chuoi.get("1D", []), t)
    except Exception as e:  # noqa: BLE001
        hs["trendline"] = {"loi": f"{type(e).__name__}: {e}"}
    # 5. Tin, Fed, F&G
    tin = tin_tuc.ngu_canh_tai(t)
    hs["tin"] = {"sap_toi_7_ngay": [dict(x, vn=vn(NG.tu_s_utc(x["ts_utc"].replace("T", " ")))) for x in tin["sap_toi_7_ngay"]],
                 "vua_qua_3_ngay": [dict(x, vn=vn(NG.tu_s_utc(x["ts_utc"].replace("T", " ")))) for x in tin["vua_qua_3_ngay"]]}
    hs["fed"] = fed_tai(t)
    hs["fng"] = lay_fng(t, cache_dir or NG.CACHE_MAC_DINH, offline)
    if ma not in NG.YAHOO:  # gap CME + độ thống trị chỉ có nghĩa với crypto
        hs["gap_cme"] = gap_cme(t, Path(cache_dir or NG.CACHE_MAC_DINH), offline)
        hs["dom"] = dom_tai(t, cache_dir, offline)
    # BTC trước (nếu mã khác BTC)
    if ma != "BTC":
        hs["btc"] = tom_tat_btc(t, cache_dir, offline)
    return hs


def tom_tat_btc(t, cache_dir, offline):
    ra = {}
    try:
        _n, h4 = NG.lay_chuoi("BTC", "4H", t, cache_dir, offline)
        _n, d1 = NG.lay_chuoi("BTC", "1D", t, cache_dir, offline)
    except Exception as e:  # noqa: BLE001
        return {"loi": str(e)}
    for k, ds in (("4H", h4), ("1D", d1)):
        if len(ds) < 5:
            continue
        p = phan_tich(ds, k, 6)
        ra[k] = {"chi_bao": p["chi_bao"], "bang": p["bang"], "bac_thang": p["bac_thang"],
                 "rau_dai": p["rau_dai"][:3], "dang_chay": nen_dang_chay(d1, [("4H", h4)], t) if k == "1D" else None}
    if h4:
        ra["doi_24h_pct"] = pct(h4[-1].c, h4[-7].c) if len(h4) >= 7 else None
    if d1:
        ra["doi_7d_pct"] = pct(d1[-1].c, d1[-8].c) if len(d1) >= 8 else None
    try:
        tl = trendline_tai(h4, d1, t, rut_gon=True)
        ra["trendline"] = tl
    except Exception as e:  # noqa: BLE001
        ra["trendline"] = {"loi": str(e)}
    return ra


# ======================= Markdown =======================
def _md_chi_bao(c, d):
    e = c["ema"]
    L = []
    e34 = e["ema34"]
    if e34.get("high") is not None:
        L.append(f"- **EMA34 dải** H/C/L = {fg(e34['high'], d)} / {fg(e34['close'], d)} / {fg(e34['low'], d)} → giá **{e34['vi_tri']}**"
                 f" (mép gần {fg(e34['mep_gan'], d)}, cách {fp(e34['cach_mep_pct'])}); dốc 5 nến {fp(e34['doc_5_nen_pct'])};"
                 f" số đợt râu chạm dải trong 30 nến: {e34['so_dot_cham_30']}")
    else:
        L.append("- EMA34 dải: chưa đủ dữ liệu")
    for k in ("ema89", "ema200", "ema610"):
        x = e[k]
        if x["gia"] is None:
            L.append(f"- {x['ten']}: chưa đủ dữ liệu")
        else:
            L.append(f"- **{x['ten']}** = {fg(x['gia'], d)} → giá {x['vi_tri']} ({fp(x['cach_pct'])}); dốc 5 nến {fp(x['doc_5_nen_pct'])};"
                     f" đợt chạm/30 nến: {x['so_dot_cham_30']}")
    L.append(f"- **Thứ tự**: {c['thu_tu']} → phân loại L01: **{c['phan_loai_L01']}**")
    L.append(f"- **RSI14** = {fg(c['rsi14'], 1)} (min/max 30 nến: {fg(c['rsi_min_30'], 1)} / {fg(c['rsi_max_30'], 1)})"
             f" · ATR14 = {fg(c['atr14'], d)} · vol nến cuối ×TB20 = {fg(c['vol_x_tb20_nen_cuoi'], 2)}")
    return L


def _md_bang(bang, d):
    L = ["| Nến | O | H | L | C | Thân % | Râu trên % | Râu dưới % | Vol | ×TB20 | RSI | Ghi chú |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in bang:
        L.append(f"| {r['nhan']} | {fg(r['o'], d)} | {fg(r['h'], d)} | {fg(r['l'], d)} | {fg(r['c'], d)} | {fp(r['than_pct'])}"
                 f" | {r['rau_tren_pct']:.2f} | {r['rau_duoi_pct']:.2f} | {fv(r['vol'])} | {fg(r['vol_x_tb20'], 2)}"
                 f" | {fg(r['rsi14'], 1)} | {', '.join(x for x in [('**VOL VƯỢT**' if r['vol_vuot'] else '')] + (['râu trên dài'] if r['rau_tren_dai'] else []) + (['râu dưới dài'] if r['rau_duoi_dai'] else []) if x)} |")
    return L


def _md_muc(m, d):
    return f"{fg(m['gia'], d)} ({fp(m['cach_pct'])})"


def ve_markdown(hs):
    d = hs["so_le"]
    L = [f"# Hồ sơ ngữ cảnh — {hs['ma']} {hs['khung']} tại {hs['t_vn']} (giờ VN)", ""]
    L.append(f"- **Mã**: {hs['ma']} · nguồn: {hs['nguon']} · **khung hỏi**: {hs['khung']}")
    L.append(f"- **T** = {hs['t_vn']} VN = {hs['t_utc']} UTC · {hs['thoi_gian']['thu']}")
    nc = hs["nen_cuoi"]
    L.append(f"- **Nến cuối dùng** ({hs['khung']}): mở {nc['mo_vn']} → đóng {nc['dong_vn']} VN · **giá đóng cuối = {fg(nc['close'], d)}**")
    L.append("- Chỉ dùng nến ĐÃ ĐÓNG ≤ T; mọi chỉ báo/Fibo/trendline tính trên dữ liệu cắt tại T; tin/Polymarket/F&G/gap CME/CMC ≤ T.")
    for c in hs["canh_bao"]:
        L.append(f"- ⚠ **{c}**")
    tg = hs["thoi_gian"]
    L += ["", "## 0. Thời gian (A6)",
          f"- {tg['thu']} {tg['gio_vn']} VN · {tg['phien']}",
          f"- Nến đang chạy đóng lúc (VN): H4 {tg['h4_dang_chay_dong_luc']} · D1 {tg['d1_dang_chay_dong_luc']} · "
          f"tuần {tg['w1_dang_chay_dong_luc']} · tháng {tg['thang_dang_chay_dong_luc']}"]
    for c in tg["co"]:
        L.append(f"- {c}")
    if hs["fed"].get("cua_so_fomc"):
        L.append(f"- ⚠ **CỬA SỔ FOMC**: {hs['fed']['cua_so_fomc']}")
    L += _md_truoc(hs, d)

    # tóm tắt khung
    L += ["", "## 1. Các khung (từ lớn xuống nhỏ)", "",
          "| Khung | Nến cuối | Đóng | Thân % | Vol ×TB20 | Dải EMA34 | EMA89 | EMA200 | EMA610 | L01 | RSI14 |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in hs["khung_ds"]:
        if "thieu" in m:
            L.append(f"| {m['ten']} | thiếu dữ liệu ({m['thieu']}) |  |  |  |  |  |  |  |  |  |")
            continue
        c, r = m["chi_bao"], m["bang"][-1]
        e = c["ema"]
        cell = lambda x: "—" if x["gia"] is None else f"{x['vi_tri']} {fp(x['cach_pct'], 1)}"  # noqa: E731
        L.append(f"| {m['ten']} | {r['nhan']} | {fg(c['gia_dong'], d)} | {fp(r['than_pct'])} | {fg(r['vol_x_tb20'], 2)} |"
                 f" {e['ema34'].get('vi_tri', '—')} | {cell(e['ema89'])} | {cell(e['ema200'])} | {cell(e['ema610'])} |"
                 f" {c['phan_loai_L01'].split(' (')[0]} | {fg(c['rsi14'], 1)} |")
    for m in hs["khung_ds"]:
        L += ["", f"### Khung {m['ten']} ({m['khung']}) — {m['so_nen_cua_so']} nến trong cửa sổ"]
        if "thieu" in m:
            L.append(f"- Thiếu dữ liệu: {m['thieu']}")
            continue
        L += _md_chi_bao(m["chi_bao"], d)
        dc = m.get("dang_chay")
        if dc:
            L.append(f"- **Nến {m['ten']} đang chạy** (CHƯA đóng; dựng từ {dc['so_nen_nho']} nến {dc['tu_nen']} đã đóng,"
                     f" {dc['mo_vn']} → {dc['den_vn']} VN): O {fg(dc['o'], d)} · H {fg(dc['h'], d)} · L {fg(dc['l'], d)} ·"
                     f" C {fg(dc['c'], d)} ({fp(pct(dc['c'], dc['o']))}) · vol {fv(dc['vol'])}")
        L.append("")
        L += _md_bang(m["bang"], d)
        fr = m["fractal"]
        L += ["", f"**Đỉnh/đáy fractal {K_FRACTAL}-{K_FRACTAL} đã xác nhận** (râu = giá cực trị; thân = đỉnh/đáy thân nến pivot):"]
        for kieu, ten in (("dinh", "Đỉnh"), ("day", "Đáy")):
            if fr[kieu]:
                L.append(f"- {ten}: " + "; ".join(f"{x['nhan']} râu {fg(x['rau'], d)} / thân {fg(x['than'], d)} ({fp(x['cach_pct'])}, {x['trang_thai']})"
                                                for x in reversed(fr[kieu])))
        bt = m["bac_thang"]
        L.append("- **Bậc thang S/R gần giá** (fractal râu; *đổi vai* = đáy cũ nằm trên giá / đỉnh cũ nằm dưới giá):")
        L.append("  - Phía trên: " + ("; ".join(f"{x['loai']} {x['nhan']} {_md_muc(x, d)}" + (" *đổi vai*" if x["doi_vai"] else "")
                                              for x in bt["tren"]) or "không có"))
        L.append("  - Phía dưới: " + ("; ".join(f"{x['loai']} {x['nhan']} {_md_muc(x, d)}" + (" *đổi vai*" if x["doi_vai"] else "")
                                              for x in bt["duoi"]) or "không có"))
        if m["rau_dai"]:
            L.append("- **Râu dài (râu > 2× thân, ≥ 0,5 ATR) chưa bị test hết** (100 nến gần nhất, mới → cũ):")
            for x in m["rau_dai"]:
                L.append(f"  - {x['nhan']} râu {x['phia']}: thân {fg(x['goc_than'], d)} → đầu râu {fg(x['dau_rau'], d)}"
                         f" ({fp(x['cach_dau_rau_pct'])}), 50% râu {fg(x['giua_rau'], d)} · "
                         + ("**CHƯA CHẠM LẠI**" if x["chua_cham"] else f"đã lấp {x['da_lap_pct']:.0f}%"))
        else:
            L.append("- Râu dài chưa test: không có")

    # Fibo
    L += ["", "## 3. Fibo (neo râu; thoái lui đo từ điểm cuối nhịp lùi về điểm đầu)"]
    for f in hs["fibo"]:
        L += ["", f"### Fibo {TEN_KHUNG[f['khung']]}"]
        for key, ten in (("nhip_gan_nhat", "Nhịp gần nhất (2 pivot fractal xác nhận cuối)"),
                         ("nhip_dang_chay", "Nhịp đang chạy (từ pivot cuối tới cực trị sau đó)"),
                         ("nhip_lon", "Nhịp lớn (đỉnh/đáy cao-thấp nhất 90 nến)")):
            x = f.get(key)
            if not x:
                continue
            L.append(f"- **{ten}** — {x['chieu']}: {x['tu']['loai']} {fg(x['tu']['gia'], d)} ({x['tu']['nhan']}) → "
                     f"{x['den']['loai']} {fg(x['den']['gia'], d)} ({x['den']['nhan']}): "
                     + " · ".join(f"{m['ty_le']} = {_md_muc(m, d)}" for m in x["muc"]))
            if x.get("mo_rong_3_diem"):
                L.append("  - " + _md_mr(x["mo_rong_3_diem"], d))
        if f.get("mo_rong_3_diem"):
            L.append("- **Fibo mở rộng 3 điểm (3 pivot xác nhận cuối)**: " + _md_mr(f["mo_rong_3_diem"], d))
    if hs.get("fibo_tuan_nhip_lon"):
        x = hs["fibo_tuan_nhip_lon"]
        L.append(f"- **Tuần — nhịp lớn {x['so_nen']} nến**: {x['tu']['loai']} {fg(x['tu']['gia'], d)} ({x['tu']['nhan']}) → "
                 f"{x['den']['loai']} {fg(x['den']['gia'], d)} ({x['den']['nhan']}): "
                 + " · ".join(f"{m['ty_le']} = {_md_muc(m, d)}" for m in x["muc"]))
    if hs.get("fibo_tuan_nhip_giam"):
        x = hs["fibo_tuan_nhip_giam"]
        if x.get("den"):
            L.append(f"- **Tuần — nhịp GIẢM từ đỉnh cao nhất {x['so_nen']} nến** (neo râu; thoái lui đo từ đáy lên): đỉnh "
                     f"{fg(x['tu']['gia'], d)} (tuần {x['tu']['nhan']}) → đáy thấp nhất sau đỉnh {fg(x['den']['gia'], d)}"
                     f" (tuần {x['den']['nhan']}{', là nến tuần cuối đã đóng' if x['day_la_nen_cuoi'] else ''}): "
                     + " · ".join(f"{m['ty_le']} = {_md_muc(m, d)}" for m in x["muc"]))
        else:
            L.append(f"- **Tuần — nhịp GIẢM từ đỉnh cao nhất {x['so_nen']} nến**: đỉnh {fg(x['tu']['gia'], d)}"
                     f" (tuần {x['tu']['nhan']}) — {x['ghi_chu']}")

    # Trendline
    L += ["", "## 4. Trendline (cong_cu/trendline.py; phá = close H4 vượt đường, râu không tính)"]
    L += _md_trendline(hs["trendline"], d)

    # Tin
    L += ["", "## 5. Tin tức, Fed, F&G"]
    t5 = hs["tin"]
    L.append("- **Sắp tới 7 ngày** (giờ VN): " + ("; ".join(f"{x['vn']} {x['su_kien']} ({x['ky']})" for x in t5["sap_toi_7_ngay"]) or "không có"))
    L.append("- **3 ngày qua**: " + ("; ".join(f"{x['vn']} {x['su_kien']} ({x['ky']})"
                                             + (f" → {x['ket_qua']['quyet_dinh']} {x['ket_qua']['thay_doi_bps']:+d}bps, dải {x['ket_qua']['dai_lai_suat_sau_hop_pct']}%"
                                                if x.get("ket_qua") else "") for x in t5["vua_qua_3_ngay"]) or "không có"))
    L.append("  - (Dataset chỉ có LỊCH công bố, không có số liệu thực tế CPI/NFP…)")
    L += _md_fed(hs["fed"])
    fn = hs["fng"]
    if fn:
        L.append(f"- **Fear & Greed** (alternative.me) ngày {fn['ngay_utc']}: **{fn['gia_tri']}** ({fn['phan_loai']}) · 7 ngày: "
                 + ", ".join(f"{a} {b}" for a, b in fn["7_ngay"]) + f" · min/max 30 ngày {fn['min_30']}/{fn['max_30']}")
    else:
        L.append("- Fear & Greed: không có dữ liệu ≤ T")
    if "btc" in hs:
        L += ["", "## 6. BTC tại T (người đó luôn nhìn BTC trước)"]
        L += _md_btc(hs["btc"])
    if "gap_cme" in hs:
        L += ["", "## 7. Ngoài chart: gap CME · BTC.D · USDT.D (chỉ làm đích / lý do HOÃN — [ST1 C8, C9])"]
        L += _md_gap(hs["gap_cme"]) + _md_dom(hs["dom"])
    L += ["", "---", "Chú thích: Nến = giờ ĐÓNG VN (khung trong ngày) hoặc ngày mở (D1/W1), tháng (M). Thân % = (C−O)/O; râu % so với O."
          f" ×TB20 = vol / TB 20 nến trước; **VOL VƯỢT** khi ≥ {VOL_VUOT}×. Râu dài = râu > 2× thân và ≥ 0,5 ATR14."
          " EMA đệ quy khởi tạo SMA (cong_cu/chi_bao.py) trên cửa sổ cố định theo T; RSI Wilder 14."]
    return "\n".join(L) + "\n"


def _md_gap(g):
    if "loi" in g:
        return [f"- Gap CME: {g['loi']}"]
    ch = g["chenh_spot"]
    L = [f"- **Gap CME** (Yahoo BTC=F 1h đã đóng ≤ T; gap = giá đóng trước kỳ nghỉ > 3 giờ so với giá mở sau, gốc ≥ "
         f"{GAP_MIN_PCT}%; lấp = râu đi hết vùng): CME {fg(g['gia_cme'], 0)} (nến 1h đóng {g['nen_cuoi_vn']} VN"
         + (", CME đang nghỉ" if g["nghi"] else "") + ")"
         + (f" · chênh CME − spot {ch:+,.0f} → ≈ spot = mức CME − ({ch:,.0f})" if ch is not None else "")]

    def mot(x):
        sp = f" (≈ spot {fg(x['con_lo'] - ch, 0)}–{fg(x['con_hi'] - ch, 0)})" if ch is not None else ""
        lap = f", đã lấp {x['da_lap_pct']:.0f}%" if x["da_lap_pct"] >= 1 else ""
        return (f"CME {fg(x['con_lo'], 0)}–{fg(x['con_hi'], 0)}{sp} · gap {x['chieu']} mở {x['tao_vn'][:10]}"
                f" (gốc {fg(x['lo'], 0)}–{fg(x['hi'], 0)}{lap}) · cách {fp(x['cach_pct'], 1)}")
    L.append("  - Chưa lấp, phía trên: " + ("; ".join(mot(x) for x in g["tren"]) or "không có"))
    L.append("  - Chưa lấp, phía dưới: " + ("; ".join(mot(x) for x in g["duoi"]) or "không có"))
    L.append("  - Vừa lấp xong trong 7 ngày: " + ("; ".join(f"gap {x['chieu']} {fg(x['lo'], 0)}–{fg(x['hi'], 0)} (mở {x['tao_vn'][:10]})"
                                                          f" lấp lúc {x['lap_vn']}" for x in g["vua_lap_7_ngay"]) or "không có"))
    return L


def _md_dom(dm):
    L = []
    for k, ghi in (("BTC.D", "btcDominance CMC"), ("USDT.D", "vốn hoá USDT / tổng vốn hoá CMC")):
        x = dm.get(k, {"loi": "không có"})
        if "loi" in x:
            L.append(f"- **{k}**: {x['loi']}")
            continue
        vt = lambda e: "—" if e is None else ("trên" if x["gia_tri"] > e else "dưới") + f" {e:.2f}"  # noqa: E731
        L.append(f"- **{k}** (proxy = {ghi}, ảnh chụp ngày): **{x['gia_tri']:.2f}%** lúc {x['ngay_vn']} VN · đổi 1 / 7 / 30 ngày "
                 f"{x['doi_1']:+.2f} / {x['doi_7']:+.2f} / {x['doi_30']:+.2f} điểm · EMA34 ngày: {vt(x['ema34'])} · EMA89 ngày: "
                 f"{vt(x['ema89'])} · cao / thấp 30 ngày {x['cao_30'][2]:.2f} ({vn(x['cao_30'][0])[:10]}) / {x['thap_30'][2]:.2f}"
                 f" ({vn(x['thap_30'][0])[:10]}) · 10 ngày: " + ", ".join(f"{a} {b:.2f}" for a, b in x["10_ngay"]))
    L.append("  - Proxy CMC, KHÔNG phải chuỗi CRYPTOCAP của TradingView mà người đó xem: mức tuyệt đối có thể lệch → đọc HƯỚNG /"
             " vị trí so với EMA / đỉnh đáy gần, đừng so thẳng với mức % họ nêu.")
    return L


def _md_truoc(hs, d):
    """Mục 0: trạng thái lúc T−24h (để suy "view đang giữ" ở Bước 0) + so với lúc T."""
    tr = hs.get("truoc_24h") or {}
    L = []
    x = tr.get("h4")
    if not x:
        return [f"- **Trạng thái lúc T−{tr.get('gio_truoc', 24)}h**: không có nến H4 đã đóng ≤ {tr.get('luc_vn', '—')}"]
    dai = "—" if x["ema34_high"] is None else f"{x['vi_tri_dai_34']} ({fg(x['ema34_low'], d)}–{fg(x['ema34_high'], d)})"
    e89 = "—" if x["ema89"] is None else f"{x['vi_tri_89']} {fg(x['ema89'], d)}"
    e200 = "—" if x["ema200"] is None else f"{x['vi_tri_200']} {fg(x['ema200'], d)}"
    L.append(f"- **Trạng thái lúc T−{tr['gio_truoc']}h** ({tr['luc_vn']} VN — để suy \"view đang giữ\"): H4 nến đóng {x['nhan']}"
             f" giá đóng {fg(x['dong'], d)} ({fp(x['than_pct'])}) · dải EMA34 H4: {dai} · EMA89 H4: {e89} · EMA200 H4: {e200}"
             f" · L01 H4: **{x['phan_loai_L01']}**")
    y = tr.get("d1")
    if y:
        L.append(f"  - Nến D1 cuối đã đóng lúc T−{tr['gio_truoc']}h (ngày {y['nhan']}): **{y['mau']}** O {fg(y['o'], d)} → đóng"
                 f" {fg(y['c'], d)} ({fp(y['than_pct'])})")
    m = next((z for z in hs.get("khung_ds", []) if z["khung"] == "4H" and "chi_bao" in z), None)
    if m:
        c = m["chi_bao"]
        L.append(f"  - So với lúc T: H4 đóng {fg(c['gia_dong'], d)} · dải EMA34 H4 {c['ema']['ema34'].get('vi_tri', '—')}"
                 f" · L01 H4 {c['phan_loai_L01']}")
    return L


def _md_mr(x, d):
    s = (f"{x['diem_1']['loai']} {fg(x['diem_1']['gia'], d)} ({x['diem_1']['nhan']}) → {x['diem_2']['loai']} "
         f"{fg(x['diem_2']['gia'], d)} ({x['diem_2']['nhan']}) → {x['diem_3']['loai']} {fg(x['diem_3']['gia'], d)} "
         f"({x['diem_3']['nhan']}{', CHƯA xác nhận' if x['diem_3_chua_xac_nhan'] else ''}); đích {x['huong_dich']}: ")
    return s + " · ".join(f"{m['ty_le']} = {_md_muc(m, d)}{' (đã chạm)' if m['da_cham_sau_diem_3'] else ''}" for m in x["muc"])


def _md_trendline(tl, d):
    L = []
    if tl.get("loi"):
        return [f"- Lỗi/thiếu: {tl['loi']}"]
    L.append(f"- Biến thể `{tl['bien_the']}` ({tl['nguon_bien_the']}); đường chính chọn theo luật của biến thể; giá đường = tại T;"
             " neo H4 ghi giờ ĐÓNG nến (VN), neo D1 ghi ngày.")
    for g in tl["nhom"]:
        kh = "H4" if g["khung"] == "H4" else "D1"
        L.append(f"- **{kh} · {TEN_LOAI[g['loai']]}**: {g['so_duong']} đường còn hiệu lực")
        for r in g["duong"]:
            pha = r["pha"]
            s = (f"  - {'**CHÍNH**' if r['chinh'] else 'khác'}: {fg(r['neo1_gia'], d)} ({r['neo1']}) → {fg(r['neo2_gia'], d)} ({r['neo2']})"
                 f" · tại T = **{fg(r['gia_tai_T'], d)}** ({fp(r['cach_pct'])} so với giá) · dốc {fg(r['doc_moi_ngay'], d)}/ngày"
                 f" · đường sau 24h ≈ {fg(r['gia_sau_24h'], d)}, sau 48h ≈ {fg(r['gia_sau_48h'], d)} (theo dốc)"
                 f" · {r['so_cham']} chạm · tuổi {r['tuoi_ngay']:.0f} ngày · {TT_TL.get(r['trang_thai'], r['trang_thai'])}")
            if pha:
                s += (f" · lần phá gần nhất {pha['luc_vn']}: close {fg(pha['dong'], d)} vs đường {fg(pha['gia_duong'], d)},"
                      f" {'2 nến' if pha['hai_nen'] else '1 nến'}, vol ×{fg(pha['vol_x_tb20'], 2)} ({pha['vol']}), kết quả {pha['ket_qua']}")
            L.append(s)
        sk = g["su_kien_72h"]
        if sk:
            chinh = [z for z in sk if z["la_chinh"]]
            khac = [z for z in sk if not z["la_chinh"]]
            for z in chinh + khac[-2:]:
                L.append(f"  - Phá trong 72h qua{' (ĐƯỜNG CHÍNH lúc T−72h)' if z['la_chinh'] else ''}: {z['luc_vn']} phá {z['chieu']},"
                         f" close {fg(z['dong'], d)} vs đường {fg(z['gia_duong'], d)} · {'2 nến' if z['hai_nen'] else '1 nến'}"
                         f" · vol ×{fg(z['vol_x_tb20'], 2)} ({z['vol']}) · kết quả {z['ket_qua']}{' · đã test lại' if z['test_lai'] else ''}")
            if len(khac) > 2:
                dem = {}
                for z in khac:
                    dem[z["ket_qua"]] = dem.get(z["ket_qua"], 0) + 1
                L.append(f"  - Tổng sự kiện phá 72h trên đường khác: {len(khac)} ("
                         + ", ".join(f"{k} {v}" for k, v in sorted(dem.items())) + ")")
    return L


def _md_fed(f):
    L = []
    if f.get("cua_so_fomc"):
        L.append(f"- ⚠ **CỬA SỔ FOMC** — {f['cua_so_fomc']} (trước tin giá đi chậm/biến động; sau tin 4–8 giờ quay về cấu trúc)")
    kv = f.get("ky_vua_qua")
    if kv:
        kq = kv["ket_qua"]
        s = f"- **FOMC gần nhất đã công bố** ({kv['ky']}, {kv['quyet_dinh_vn']} VN, {kv['cach_gio']:.0f} giờ trước T): "
        if kq:
            s += (f"{kq['quyet_dinh']} {kq['thay_doi_bps']:+d}bps → dải {kq['dai_lai_suat_sau_hop_pct']}%"
                  + (f" · phiếu {kq['phieu']}" if kq.get("phieu") else "")
                  + (f" · phản đối: \"{kq['phan_doi']}\"" if kq.get("phan_doi") not in (None, "", "khong co")
                     else " · không ai phản đối"))
        else:
            s += "không có kết quả trong dataset"
        L.append(s)
        tc = kv.get("thong_cao")
        if tc and tc["cau"]:
            L.append(f"  - Định hướng (trích nguyên văn thông cáo, `{tc['file']}`):")
            for z in tc["cau"]:
                L.append(f"    > {z}")
    kt = f.get("ky_toi")
    if kt:
        L.append(f"- **Polymarket — kỳ FOMC KẾ TIẾP** {kt['ky']} (quyết định {kt['quyet_dinh_vn']} VN, còn {kt['con_gio'] / 24:.1f} ngày;"
                 f" dữ liệu mới nhất {kt['ts_moi_nhat_utc'] or '—'} UTC). Giá token Yes thô tổng = {kt['tong_yes']:.3f} → **chuẩn hoá tổng = 100%**;"
                 " Δ = thay đổi điểm % (chuẩn hoá) so với 1/3/7 ngày trước:")
        if kt["ket_qua"]:
            L += ["", "| Kết quả | Yes thô | % chuẩn hoá | Δ1 ngày | Δ3 ngày | Δ7 ngày |", "|---|---|---|---|---|---|"]
            for r in kt["ket_qua"]:
                L.append(f"| {r['ten']} | {r['yes']:.3f} | {r['pct']:.1f}% | {_dd(r['doi_1d'])} | {_dd(r['doi_3d'])} | {_dd(r['doi_7d'])} |")
            L.append("")
        else:
            L.append("  - chưa có dữ liệu Polymarket ≤ T cho kỳ này")
    elif not kv:
        L.append("- Fed/Polymarket: ngoài phạm vi dữ liệu 2026")
    return L


def _dd(x):
    return "—" if x is None else f"{x:+.1f}"


def _lap(z):
    return "chưa chạm" if z["chua_cham"] else f"lấp {z['da_lap_pct']:.0f}%"


def _md_btc(b):
    if b.get("loi"):
        return [f"- Lỗi: {b['loi']}"]
    d = so_le(b["4H"]["chi_bao"]["gia_dong"]) if "4H" in b else 0
    L = [f"- Đổi 24h: {fp(b.get('doi_24h_pct'))} · đổi 7 ngày: {fp(b.get('doi_7d_pct'))}"]
    for k in ("1D", "4H"):
        if k not in b:
            continue
        x = b[k]
        c = x["chi_bao"]
        e = c["ema"]
        L.append(f"- **BTC {TEN_KHUNG[k]}**: đóng {fg(c['gia_dong'], d)} · dải EMA34 {e['ema34'].get('vi_tri', '—')} ·"
                 f" EMA89 {fg(e['ema89']['gia'], d)} · EMA200 {fg(e['ema200']['gia'], d)} · EMA610 {fg(e['ema610']['gia'], d)} ·"
                 f" thứ tự {c['thu_tu']} → **{c['phan_loai_L01']}** · RSI {fg(c['rsi14'], 1)}")
        L.append("  - Nến cuối: " + " | ".join(f"{r['nhan']} O{fg(r['o'], d)} H{fg(r['h'], d)} L{fg(r['l'], d)} C{fg(r['c'], d)}"
                                             f" ({fp(r['than_pct'])}, vol×{fg(r['vol_x_tb20'], 2)})" for r in x["bang"][-4:]))
        bt = x["bac_thang"]
        L.append("  - S/R gần: trên " + ("; ".join(f"{z['loai']} {_md_muc(z, d)}" for z in bt["tren"][:3]) or "—")
                 + " · dưới " + ("; ".join(f"{z['loai']} {_md_muc(z, d)}" for z in bt["duoi"][:3]) or "—"))
        if x["rau_dai"]:
            L.append("  - Râu dài chưa test hết: " + "; ".join(f"{z['nhan']} râu {z['phia']} tới {fg(z['dau_rau'], d)} ({_lap(z)})"
                                                           for z in x["rau_dai"]))
        if x.get("dang_chay"):
            dc = x["dang_chay"]
            L.append(f"  - Nến D1 đang chạy: O {fg(dc['o'], d)} H {fg(dc['h'], d)} L {fg(dc['l'], d)} C {fg(dc['c'], d)}")
    tl = b.get("trendline", {})
    if tl and not tl.get("loi"):
        for g in tl["nhom"]:
            for r in g["duong"]:
                if r["chinh"]:
                    L.append(f"  - Trendline BTC {g['khung']} {TEN_LOAI[g['loai']].split(' (')[0]} chính: tại T {fg(r['gia_tai_T'], d)}"
                             f" ({fp(r['cach_pct'])}) · sau 24h ≈ {fg(r['gia_sau_24h'], d)}, sau 48h ≈ {fg(r['gia_sau_48h'], d)}"
                             f" · {r['so_cham']} chạm · {TT_TL.get(r['trang_thai'], r['trang_thai'])}")
    return L


# ======================= main =======================
def main(argv=None):
    ap = argparse.ArgumentParser(description="Hồ sơ ngữ cảnh tại T (chỉ dữ liệu ≤ T)")
    ap.add_argument("ma")
    ap.add_argument("khung")
    ap.add_argument("t", help='"YYYY-MM-DD HH:MM" giờ VN (hoặc UTC nếu --utc)')
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--so-nen", type=int, default=30)
    ap.add_argument("--utc", action="store_true")
    ap.add_argument("--cache", default=None)
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args(argv)
    t = doc_t(a.t, a.utc)
    try:
        hs = tao_ho_so(a.ma, a.khung, t, a.so_nen, a.cache, a.offline)
    except NG.LoiDuLieu as e:
        print(f"LỖI: {e}", file=sys.stderr)
        return 2
    print(json.dumps(hs, ensure_ascii=False, indent=1) if a.json else ve_markdown(hs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
