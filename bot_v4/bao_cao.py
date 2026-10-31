#!/usr/bin/env python3
"""Bao cao bot v4 -> bot_v4/KET_QUA.md (dung muc 8 THIET_KE.md).

Viec lam (chi doc ket qua + goi ham dong co, KHONG viet lai luat):
  1. Doc bot_v4/ket_qua/<nam>_<ro>/{lenh.csv,von.csv,tom_tat.json} cho nam 2024/2025/2026 x ro 6 / BTC
     (thieu -> chay `python3 bot_v4/chay.py --nam N --ro R`; khong co chay.py -> goi dong_co.chay trong bo nho).
  2. Tu cong lai DOC LAP: lai tung lenh tinh lai tu gia vao/ra/khoi luong/phi (+ TP1 chot 50%) so voi cot lai_usd,
     chuoi von_sau, von.csv; phi so voi quy tac muc 7. Lech > 0,01$ -> LOI in to trong bao cao.
  3. Bang: lai$, %, so lenh, % thang, R TB, t-stat R, sut giam max, he so LN; theo tai san; chinh vs hoi; theo ly do ra.
  4. So sanh v1/v2 (trich dung dong nguon backtest/KET_QUA_NGOAI_MAU.md, KET_QUA_V2.md) + mua-giu BTC (BTC_1D.csv).
  5. Gia duoc 1.000 lan (hat giong co dinh): moi lenh that -> lenh cung tai san/chieu/loai/SL%/TP theo R/gio dung,
     thoi diem dat ngau nhien deu tai gio DONG nen H4 trong cung ky; mo phong bang dong_co.mo_phong_lenh, cung quy tac
     von (rui ro % von da chot, toi da 3 lenh cho+mo, moi tai san 1, ky quy <= 50%) -> phan vi theo $ va tong R.
  6. Do giong: 180 buoi transcripts/gio_live.tsv, C = bat_dau_vn + phut (VN -> UTC); view bot = dong_co.view_tai("BTC", C);
     nhan nguoi do: buoi tu 2026-07-01 -> thi/dap_an_v2/phieu/, truoc do -> phieu/ (khung H4, khong co thi "chung").
     So voi "luon GIAM" va "luat tu tren xuong" (dinh nghia docstring thi/cham.py) tren CUNG buoi. TRONG MAU.
Cach dung:
  python3 bot_v4/bao_cao.py                       # day du (1.000 lan gia duoc)
  python3 bot_v4/bao_cao.py --so-gia-duoc 50      # thu nhanh
  python3 bot_v4/bao_cao.py --v4 DIR --ra FILE    # thu muc dong co/ket qua khac (thu voi dong co gia lap)
"""
import argparse, csv, datetime as dt, hashlib, heapq, importlib.util, inspect, json, math, multiprocessing as mp, os, random, re
import statistics, subprocess, sys, time, unicodedata
from bisect import bisect_right
from collections import Counter, defaultdict
from pathlib import Path

V4_MAC_DINH = Path(__file__).resolve().parent
GOC = V4_MAC_DINH.parent
UTC = dt.timezone.utc
VN = dt.timezone(dt.timedelta(hours=7))
G4 = dt.timedelta(hours=4)
NAM = [2024, 2025, 2026]
RO = ["6", "BTC"]
TEN_RO = {"6": "6 tài sản", "BTC": "riêng BTC"}
TAI_SAN_6 = ["BTC", "ETH", "OKB", "BNB", "VANG", "DAU"]
VON0 = 4000.0
SO_GIA_DUOC = 1000
HAT_GIONG = 20261031
# TK 7 (dung de KIEM, khong de chay luat)
PHI_LIMIT, PHI_MARKET, TRUOT = 0.0002, 0.0005, 0.0002
RUI_RO = {"chinh": 0.02, "hoi": 0.01}
GIO_DUNG = {"chinh": 120, "hoi": 48}
TOI_DA_LENH, KY_QUY_TOI_DA = 3, 0.5
NGUONG = 0.01  # $
LY_DO = ["TP2", "TP", "SL", "SL_HOA_VON", "HET_GIO", "HET_KY", "HUY", "DANG_CHO", "DANG_MO"]
VIET = {"TANG": "TĂNG", "GIAM": "GIẢM", "PHAN_VAN": "PHÂN VÂN", None: "—"}
NHAN = ["TANG", "GIAM", "PHAN_VAN"]


# ───────────────────────── tien ich ─────────────────────────
def tg(x):
    """datetime/str -> datetime UTC co mui gio; rong -> None."""
    if x is None or x == "":
        return None
    if isinstance(x, dt.datetime):
        return x if x.tzinfo else x.replace(tzinfo=UTC)
    if isinstance(x, (int, float)):
        return dt.datetime.fromtimestamp(x, UTC)
    s = str(x).strip().replace("T", " ").replace("Z", "+00:00")
    for f in ("%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            d = dt.datetime.strptime(s, f)
            return d if d.tzinfo else d.replace(tzinfo=UTC)
        except ValueError:
            pass
    return dt.datetime.fromisoformat(s).astimezone(UTC)


def so(x):
    if x is None or x == "" or (isinstance(x, str) and x.strip().lower() in ("none", "nan", "null")):
        return None
    return float(x)


def sha(p):
    p = Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def tuong_doi(p):
    try:
        return str(Path(p).resolve().relative_to(GOC))
    except ValueError:
        return str(p)


def usd(x, dau=True):
    if x is None:
        return "—"
    s = f"{abs(x):,.0f}".replace(",", ".")
    return ("+" if x >= 0 else "-") + s + "$" if dau else ("-" if x < 0 else "") + s + "$"


def so_vn(x, k=2):
    """1234.5 -> '1.234,50'."""
    return "—" if x is None else f"{x:,.{k}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def phay(x, k=2, dau=False):
    if x is None:
        return "—"
    s = f"{x:+.{k}f}" if dau else f"{x:.{k}f}"
    return s.replace(".", ",")


def pt(x, k=1, dau=True):
    return "—" if x is None else phay(x * 100, k, dau) + "%"


def ty_le(a, b):
    return f"{a}/{b} = {a / b:.0%}" if b else "—"


def chuan_huong(x):
    """Giong thi/cham.py::chuan_huong."""
    if x is None:
        return None
    s = unicodedata.normalize("NFD", str(x)).encode("ascii", "ignore").decode().upper().strip().replace(" ", "_")
    if s in ("TANG", "LONG", "UP"):
        return "TANG"
    if s in ("GIAM", "SHORT", "DOWN"):
        return "GIAM"
    if s.replace("_", "") in ("PHANVAN", "PV", "DUNGNGOAI", "TRUNGLAP", "SIDEWAY"):
        return "PHAN_VAN"
    return None


def ky(nam):
    """Ky chay nam Y (TK 1): [tu, den) UTC."""
    tu = dt.datetime(nam, 1, 1, tzinfo=UTC)
    den = dt.datetime(2026, 10, 31, tzinfo=UTC) if nam == 2026 else dt.datetime(nam + 1, 1, 1, tzinfo=UTC)
    return tu, den


# ───────────────────────── du lieu nen (doc doc lap, khong qua dong co) ─────────────────────────
def doc_nen(thu_muc, ts, khung):
    """[(mo, dong, o, h, l, c)] tu <ts>_<khung>.csv; dong = mo + 4h / 1 ngay."""
    p = Path(thu_muc) / f"{ts}_{khung}.csv"
    buoc = G4 if khung == "4H" else dt.timedelta(days=1)
    ra = []
    with p.open() as f:
        for r in csv.DictReader(f):
            mo = tg(r["ts_utc"])
            ra.append((mo, mo + buoc, float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])))
    return ra


def ema_cuoi(xs, n):
    """EMA khoi tao SMA n nen dau (giong thi/tao_ho_so.ema); thieu -> None."""
    if len(xs) < n:
        return None
    a, e = 2 / (n + 1), sum(xs[:n]) / n
    for x in xs[n:]:
        e = a * x + (1 - a) * e
    return e


# ───────────────────────── dong co ─────────────────────────
def nap_dong_co(v4):
    p = Path(v4) / "dong_co.py"
    if not p.exists():
        return None
    sys.path.insert(0, str(Path(v4)))
    spec = importlib.util.spec_from_file_location("dong_co", p)
    m = importlib.util.module_from_spec(spec)
    sys.modules["dong_co"] = m
    spec.loader.exec_module(m)
    return m


COT_LENH = ["tai_san", "loai", "chieu", "t_quyet_dinh", "t_khop", "gia_vao", "sl", "tp1", "tp2", "t_tp1", "t_ra", "gia_ra",
            "ly_do_ra", "khoi_luong", "don_bay", "phi", "lai_usd", "R", "von_sau"]
COT_THEM = ["gia_dat", "gia_tp1", "ti_le_tp1", "rui_ro_usd", "ky_quy", "gio_dung", "ly_do_huy", "vung", "ghi"]
COT_TG = {"t_quyet_dinh", "t_khop", "t_tp1", "t_ra"}
COT_CHU = {"tai_san", "loai", "chieu", "ly_do_ra", "ly_do_huy", "vung", "ghi"}


def chuan_lenh(r):
    x = {}
    for k in COT_LENH + COT_THEM:
        v = r.get(k) if isinstance(r, dict) else getattr(r, k, None)
        x[k] = tg(v) if k in COT_TG else (("" if v is None else str(v)).strip() if k in COT_CHU else so(v))
    x["chieu"] = x["chieu"].upper()
    x["loai"] = x["loai"].lower()
    x["ly_do_ra"] = x["ly_do_ra"].upper()
    return x


def chuan_von(r):
    r = dict(r) if isinstance(r, dict) else dict(r._asdict())
    x = {}
    for k, v in r.items():
        if k in ("ts_utc", "t", "ts", "thoi_gian", "luc"):
            x["t"] = tg(v)
        else:
            try:
                x[k] = so(v)
            except (TypeError, ValueError):
                x[k] = v
    return x


def doc_ket_qua(v4, dc, nam, ro, ghi_chu):
    d = Path(v4) / "ket_qua" / f"{nam}_{ro}"
    if not (d / "lenh.csv").exists() and (Path(v4) / "chay.py").exists():
        print(f"  thiếu {d.name} -> chạy chay.py --nam {nam} --ro {ro}", file=sys.stderr)
        subprocess.run([sys.executable, str(Path(v4) / "chay.py"), "--nam", str(nam), "--ro", ro], check=False)
    if (d / "lenh.csv").exists():
        with (d / "lenh.csv").open(encoding="utf-8") as f:
            lenh = [chuan_lenh(r) for r in csv.DictReader(f)]
        von = []
        if (d / "von.csv").exists():
            with (d / "von.csv").open(encoding="utf-8") as f:
                von = [chuan_von(r) for r in csv.DictReader(f)]
        tt = json.loads((d / "tom_tat.json").read_text(encoding="utf-8")) if (d / "tom_tat.json").exists() else None
        return {"lenh": lenh, "von": von, "tom_tat": tt, "nguon": tuong_doi(d)}
    if dc is None:
        return None
    ghi_chu.append(f"{nam}_{ro}: không có `{tuong_doi(d)}` và không có chay.py → gọi `dong_co.chay` trong bộ nhớ.")
    kq = dc.chay(TAI_SAN_6 if ro == "6" else [ro], nam)
    von_chot = dict(getattr(kq, "von_chot", []) or [])
    von = [{"t": tg(t), "von": v, **({"von_chot": von_chot[t]} if t in von_chot else {})} for t, v in kq.von]
    return {"lenh": [chuan_lenh(r) for r in kq.lenh], "von": von, "tom_tat": None, "nguon": "dong_co.chay (bộ nhớ)"}


CON_MO = ("DANG_CHO", "DANG_MO")  # DG 26 dong co: chi khi du lieu bi cat truoc het ky (khong co trong backtest ca nam)


def da_khop(x):
    """Lenh da khop VA da ra (tinh vao thong ke)."""
    return x["t_khop"] is not None and x["ly_do_ra"] not in ("HUY",) + CON_MO


# ───────────────────────── thong ke ─────────────────────────
def cot_von(von):
    """Cot von dung tinh sut giam: uu tien cot theo gia thi truong."""
    if not von:
        return None
    cot = [k for k, v in von[0].items() if k != "t" and isinstance(v, float)]
    for ung in ("von_thi_truong", "von_tt", "von_mtm", "mtm", "equity", "von_theo_gia", "von"):
        if ung in cot:
            return ung
    return next((k for k in cot if "von" in k), cot[0] if cot else None)


def sut_giam(chuoi):
    dinh, mx = None, 0.0
    for v in chuoi:
        if v is None:
            continue
        dinh = v if dinh is None else max(dinh, v)
        if dinh > 0:
            mx = max(mx, (dinh - v) / dinh)
    return mx


def thong_ke(lenh, von=None):
    k = [x for x in lenh if da_khop(x)]
    lai = sum(x["lai_usd"] for x in k)
    Rs = [x["R"] for x in k if x["R"] is not None]
    duong = sum(x["lai_usd"] for x in k if x["lai_usd"] > 0)
    am = -sum(x["lai_usd"] for x in k if x["lai_usd"] < 0)
    tb = statistics.mean(Rs) if Rs else None
    t = None
    if len(Rs) >= 2 and statistics.stdev(Rs) > 1e-9:
        t = tb / (statistics.stdev(Rs) / math.sqrt(len(Rs)))
    dd = None
    c = cot_von(von)
    if c:
        dd = sut_giam([r.get(c) for r in von])
    else:  # khong co von.csv -> sut giam tren von da chot
        v, ch = VON0, [VON0]
        for x in sorted(k, key=lambda x: x["t_ra"]):
            v += x["lai_usd"]; ch.append(v)
        dd = sut_giam(ch)
    return {"n": len(k), "huy": sum(1 for x in lenh if not da_khop(x)), "lai": lai, "pct": lai / VON0,
            "thang": sum(1 for x in k if x["lai_usd"] > 0) / len(k) if k else None, "R_tb": tb, "t": t,
            "tong_R": sum(Rs), "dd": dd, "pf": (duong / am if am > 0 else (math.inf if duong > 0 else None)),
            "long": sum(1 for x in k if x["chieu"] == "LONG"), "short": sum(1 for x in k if x["chieu"] == "SHORT")}


def pf_s(x):
    return "—" if x is None else ("∞" if x == math.inf else phay(x, 2))


# ───────────────────────── tu cong lai doc lap ─────────────────────────
def gia_dat(x):
    return x["gia_dat"] if x.get("gia_dat") is not None else x["gia_vao"]


def gia_tp1(x):
    return x["gia_tp1"] if x.get("gia_tp1") is not None else x["tp1"]


def ti_le_tp1(x):
    return x["ti_le_tp1"] if x.get("ti_le_tp1") else 0.5


def phi_ky_vong(x, truot_la_phi):
    """Phi theo TK 7 tinh tu gia/khoi luong (2 cach hieu truot gia: cong vao phi, hoac da nam trong gia ra)."""
    return sum(-t for _, t, _ in dong_tien(x, truot_la_phi, chi_phi=True))


def dong_tien(x, truot_la_phi, chi_phi=False):
    """Dong tien DOC LAP cua 1 lenh da khop (TK 7): [(gio, tien, thu tu)] = phi vao luc khop, chot TP1, luc ra.
    Tinh tu gia vao/ra/khoi luong + quy tac phi; KHONG dung cot phi/lai_usd. chi_phi=True -> chi tra (am) phan phi."""
    d = 1 if x["chieu"] == "LONG" else -1
    kl, vao = x["khoi_luong"], x["gia_vao"]
    ev = [(x["t_khop"], -PHI_LIMIT * kl * vao, 0)]
    con = 1.0
    if x["t_tp1"] is not None:
        q, g = kl * ti_le_tp1(x), gia_tp1(x)
        ev.append((x["t_tp1"], (0 if chi_phi else d * q * (g - vao)) - PHI_LIMIT * q * g, 1))
        con -= ti_le_tp1(x)
    q = kl * con
    ty = PHI_LIMIT if x["ly_do_ra"] in ("TP2", "TP") else PHI_MARKET + (TRUOT if truot_la_phi else 0)
    ev.append((x["t_ra"], (0 if chi_phi else d * q * (x["gia_ra"] - vao)) - ty * q * x["gia_ra"], 2))
    return ev


class ChiMucNen:
    """Tra nen H4 theo gio dong (du lieu doc lap)."""

    def __init__(self, nen4):
        self.n = nen4
        self.dong = {ts: [x[1] for x in v] for ts, v in nen4.items()}

    def chi_so(self, ts, t):
        i = bisect_right(self.dong[ts], t) - 1
        return i if i >= 0 and self.dong[ts][i] == t else None

    def close_luc(self, ts, t):
        i = bisect_right(self.dong[ts], t) - 1
        return self.n[ts][i][5] if i >= 0 else None


def gan(a, b):
    return a is not None and b is not None and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def kiem_gia_nen(lenh, cm):
    """Gia vao/ra va duong di cua tung lenh so voi nen OHLC doc lap (TK 5.3, 6, 7; khop o gia mo khi mo da vuot muc = DG 18
    cua dong co; cung nen TP1 roi cham lai gia vao -> SL hoa von = DG 20). Tra list loi."""
    loi = []
    for i, x in enumerate(lenh):
        if not da_khop(x):
            continue
        ts, d = x["tai_san"], (1 if x["chieu"] == "LONG" else -1)
        N = cm.n[ts]
        ten = f"lệnh #{i + 1} {ts} {x['chieu']} đặt {x['t_quyet_dinh']:%Y-%m-%d %H:%M}"
        q, f, e = (cm.chi_so(ts, x["t_quyet_dinh"]), cm.chi_so(ts, x["t_khop"]), cm.chi_so(ts, x["t_ra"]))
        p = cm.chi_so(ts, x["t_tp1"]) if x["t_tp1"] is not None else None
        if None in (q, f, e) or (x["t_tp1"] is not None and p is None):
            loi.append(f"{ten}: giờ đặt/khớp/TP1/ra không trùng giờ đóng nến H4 nào")
            continue
        cham = (lambda n, m: n[4] <= m) if d == 1 else (lambda n, m: n[3] >= m)     # gia di NGUOC (cham muc duoi long)
        toi = (lambda n, m: n[3] >= m) if d == 1 else (lambda n, m: n[4] <= m)      # gia di THUAN (cham muc tren long)
        gd, sl, vao = gia_dat(x), x["sl"], x["gia_vao"]
        # khop: nen SAU nen dat, trong 6 nen, nen dau tien cham gia limit
        if not (q < f <= q + 6):
            loi.append(f"{ten}: nến khớp cách nến đặt {f - q} nến (phải 1–6)")
        if any(cham(N[j], gd) for j in range(q + 1, f)):
            loi.append(f"{ten}: có nến chạm giá limit trước nến khớp")
        if not cham(N[f], gd):
            loi.append(f"{ten}: nến khớp không chạm giá limit {gd}")
        if not gan(vao, min(gd, N[f][2]) if d == 1 else max(gd, N[f][2])):
            loi.append(f"{ten}: giá vào {vao} ≠ limit/giá mở {min(gd, N[f][2]) if d == 1 else max(gd, N[f][2])}")
        han = x["t_khop"] + dt.timedelta(hours=x.get("gio_dung") or GIO_DUNG.get(x["loai"], 120))
        # duong di giua nen khop va nen ra: khong duoc cham SL / TP1 / TP2 / qua gio som hon
        tp2_xet = (lambda j: x["loai"] != "chinh" or (p is not None and j >= p))
        for j in range(f, e):                           # thu tu trong 1 nen (TK 7): SL -> TP1 -> (DG 20) -> TP2 -> het gio
            n = N[j]
            if cham(n, sl if (p is None or j <= p) else vao):
                loi.append(f"{ten}: nến đóng {n[1]:%Y-%m-%d %H:%M} chạm SL nhưng lệnh chưa ra"); break
            if j > f:
                if x["loai"] == "chinh" and (p is None or j < p) and toi(n, x["tp1"]):
                    loi.append(f"{ten}: nến đóng {n[1]:%Y-%m-%d %H:%M} chạm TP1 nhưng không chốt"); break
                if p is not None and j == p and cham(n, vao):
                    loi.append(f"{ten}: nến TP1 chạm lại giá vào nhưng không ra hoà vốn"); break
                if tp2_xet(j) and toi(n, x["tp2"]):
                    loi.append(f"{ten}: nến đóng {n[1]:%Y-%m-%d %H:%M} chạm TP2/TP nhưng không ra"); break
            if n[1] >= han:
                loi.append(f"{ten}: quá giờ dừng ở nến {n[1]:%Y-%m-%d %H:%M} nhưng không ra"); break
        if x["ly_do_ra"] not in ("SL", "SL_HOA_VON"):    # nen ra: SL xet truoc moi thu khac
            if cham(N[e], sl if (p is None or p >= e) else vao) or (p == e and x["ly_do_ra"] != "SL_HOA_VON" and cham(N[e], vao)):
                loi.append(f"{ten}: nến ra chạm SL nhưng ghi {x['ly_do_ra']} (SL phải tính trước)")
            if x["ly_do_ra"] in ("HET_GIO", "HET_KY") and e > f and ((x["loai"] == "chinh" and p is None and toi(N[e], x["tp1"]))
                                                                    or (tp2_xet(e) and toi(N[e], x["tp2"]))):
                loi.append(f"{ten}: nến ra chạm TP nhưng ghi {x['ly_do_ra']}")
        if p is not None:
            if not (f < p <= e) or not toi(N[p], x["tp1"]):
                loi.append(f"{ten}: nến TP1 không hợp lệ")
            elif x.get("gia_tp1") is not None and not gan(x["gia_tp1"], max(x["tp1"], N[p][2]) if d == 1 else min(x["tp1"], N[p][2])):
                loi.append(f"{ten}: giá chốt TP1 {x['gia_tp1']} ≠ TP1/giá mở")
        n, ly = N[e], x["ly_do_ra"]
        if ly in ("SL", "SL_HOA_VON"):
            muc = sl if ly == "SL" else vao
            goc = muc if (ly == "SL_HOA_VON" and p == e) else (min(muc, n[2]) if d == 1 else max(muc, n[2]))
            if (ly == "SL_HOA_VON") != (p is not None):
                loi.append(f"{ten}: {ly} nhưng t_tp1 = {x['t_tp1']}")
            if not cham(n, muc) or not gan(x["gia_ra"], goc * (1 - d * TRUOT)):
                loi.append(f"{ten}: {ly} giá ra {x['gia_ra']} ≠ {goc * (1 - d * TRUOT)} (mức/giá mở × trượt 0,02%) hoặc nến không chạm")
        elif ly in ("TP2", "TP"):
            goc = max(x["tp2"], n[2]) if d == 1 else min(x["tp2"], n[2])
            if e == f or not toi(n, x["tp2"]) or not gan(x["gia_ra"], goc):
                loi.append(f"{ten}: {ly} giá ra {x['gia_ra']} ≠ {goc} hoặc nến không chạm / là nến khớp")
        elif ly in ("HET_GIO", "HET_KY"):
            if not gan(x["gia_ra"], n[5] * (1 - d * TRUOT)):
                loi.append(f"{ten}: {ly} giá ra {x['gia_ra']} ≠ close × (1 ∓ 0,02%) = {n[5] * (1 - d * TRUOT)}")
            if ly == "HET_GIO" and n[1] < han:
                loi.append(f"{ten}: HET_GIO trước giờ dừng")
        else:
            loi.append(f"{ten}: lý do ra lạ {ly}")
    return loi


def tu_cong_lai(lenh, von, tom_tat, cm):
    """Tra ve dict: loi (list), thong tin (list), so lieu. Moi so tinh lai tu gia/khoi luong + quy tac TK 7 + nen doc lap."""
    loi, tin = [], []
    k = [(i, x) for i, x in enumerate(lenh) if da_khop(x)]
    for i, x in enumerate(lenh):
        if not da_khop(x) and abs(x["lai_usd"] or 0) > NGUONG:
            loi.append(f"lệnh #{i + 1} {x['tai_san']} {x['ly_do_ra']} không khớp mà lai_usd = {x['lai_usd']:.4f}")
    # 1. so hoc: lai_usd = lai gop (tu gia) - cot phi
    lech_lai = []
    for i, x in k:
        d = 1 if x["chieu"] == "LONG" else -1
        kl, con = x["khoi_luong"], 1.0
        gop = 0.0
        if x["t_tp1"] is not None:
            gop += d * kl * ti_le_tp1(x) * (gia_tp1(x) - x["gia_vao"])
            con -= ti_le_tp1(x)
        gop += d * kl * con * (x["gia_ra"] - x["gia_vao"])
        lech_lai.append(abs(gop - x["phi"] - x["lai_usd"]))
        if abs(gop - x["phi"] - x["lai_usd"]) > NGUONG:
            loi.append(f"lệnh #{i + 1} {x['tai_san']} {x['chieu']} khớp {x['t_khop']:%Y-%m-%d %H:%M}: lãi gộp − phí = "
                       f"{gop - x['phi']:.4f}$ ≠ lai_usd {x['lai_usd']:.4f}$")
    # 2. phi theo quy tac TK 7 (chon cach hieu truot gia khop nhat, bao ro)
    cach = {c: [abs(phi_ky_vong(x, c) - x["phi"]) for _, x in k] for c in (False, True)}
    tot = min(cach, key=lambda c: (sum(v > NGUONG for v in cach[c]), not c))
    sai_phi = [j for j, v in enumerate(cach[tot]) if v > NGUONG]
    ten_cach = "trượt 0,02% cộng vào phí" if tot else "trượt 0,02% nằm trong giá ra, phí market 0,05%"
    if sai_phi:
        x = k[sai_phi[0]][1]
        loi.append(f"phí: {len(sai_phi)}/{len(k)} lệnh lệch quy tắc mục 7 > 0,01$ (cách hiểu khớp nhất: {ten_cach}); vd "
                   f"{x['tai_san']} khớp {x['t_khop']:%Y-%m-%d %H:%M}: phí {x['phi']:.4f} vs {phi_ky_vong(x, tot):.4f}")
    else:
        tin.append(f"phí {len(k)}/{len(k)} lệnh đúng quy tắc mục 7 ({ten_cach})")
    # 3. lai doc lap hoan toan (gia + quy tac phi) vs lai_usd
    ev_all, lech_dl = [], 0.0
    for i, x in k:
        ev = dong_tien(x, tot)
        lech_dl = max(lech_dl, abs(sum(t for _, t, _ in ev) - x["lai_usd"]))
        ev_all += [(t, i, n, tien) for t, tien, n in ev]
    (loi if lech_dl > NGUONG else tin).append(f"lãi tính độc lập (giá + quy tắc phí) vs lai_usd: lệch lớn nhất {lech_dl:.6f}$")
    # 4. R va rui ro
    lech_R = sai_rr = 0
    for i, x in k:
        rr = x["khoi_luong"] * abs(gia_dat(x) - x["sl"])
        if x.get("rui_ro_usd") is not None and abs(rr - x["rui_ro_usd"]) > NGUONG:
            sai_rr += 1
        if x["R"] is not None and rr > 0 and abs(x["lai_usd"] / rr - x["R"]) > 1e-4:
            lech_R += 1
    (loi if lech_R or sai_rr else tin).append(
        f"R = lai_usd ÷ (KL × |giá đặt − SL|): {len(k) - lech_R}/{len(k)} khớp; rui_ro_usd = KL × |giá đặt − SL|: "
        f"{len(k) - sai_rr}/{len(k)} khớp")
    # 5. von_sau: cong don dong tien theo (gio, thu tu lenh, thu tu su kien)
    ev_all.sort()
    cong, v, von_sau_tinh = [], VON0, {}
    for t, i, n, tien in ev_all:
        v += tien
        cong.append((t, v))
        if n == 2:
            von_sau_tinh[i] = v
    sai_vs = [i for i, x in k if x["von_sau"] is not None and abs(von_sau_tinh[i] - x["von_sau"]) > NGUONG]
    if sai_vs:
        x = lenh[sai_vs[0]]
        loi.append(f"von_sau: {len(sai_vs)}/{len(k)} lệnh lệch dòng tiền cộng dồn; vd lệnh #{sai_vs[0] + 1} {x['tai_san']} ra "
                   f"{x['t_ra']:%Y-%m-%d %H:%M}: {x['von_sau']:.4f} vs {von_sau_tinh[sai_vs[0]]:.4f}")
    else:
        tin.append(f"von_sau {len(k)}/{len(k)} khớp 4.000$ + dòng tiền cộng dồn (phí vào lúc khớp, TP1, lúc ra)")
    von_cuoi = VON0 + sum(tien for *_, tien in ev_all)
    tcong = [t for t, _ in cong]

    def chot_luc(t):
        j = bisect_right(tcong, t) - 1
        return cong[j][1] if j >= 0 else VON0
    # 6. von.csv: von_chot (da chot) + von (theo gia: + lai chua chot vi the dang mo theo close nen doc lap)
    if von:
        cot_s = [c for c, val in von[0].items() if c != "t" and isinstance(val, float)]
        c_chot = next((c for c in ("von_chot", "von_da_chot") if c in cot_s), None)
        if c_chot:
            sai = [r for r in von if abs(chot_luc(r["t"]) - r[c_chot]) > NGUONG]
            if sai:
                loi.append(f"von.csv `{c_chot}`: {len(sai)}/{len(von)} dòng lệch 4.000$ + dòng tiền đã xảy ra ≤ t; dòng đầu "
                           f"{sai[0]['t']:%Y-%m-%d %H:%M}: {sai[0][c_chot]:.4f} vs {chot_luc(sai[0]['t']):.4f}")
            else:
                tin.append(f"von.csv `{c_chot}` {len(von)}/{len(von)} dòng khớp 4.000$ + dòng tiền đã xảy ra ≤ t")
        if "von" in cot_s:
            sai = []
            for r in von:
                t = r["t"]
                mtm = chot_luc(t)
                for i, x in k:
                    if x["t_khop"] <= t < x["t_ra"]:
                        con = 1.0 - (ti_le_tp1(x) if x["t_tp1"] is not None and x["t_tp1"] <= t else 0.0)
                        mtm += (1 if x["chieu"] == "LONG" else -1) * x["khoi_luong"] * con * (cm.close_luc(x["tai_san"], t) - x["gia_vao"])
                if abs(mtm - r["von"]) > NGUONG:
                    sai.append((r, mtm))
            if sai:
                loi.append(f"von.csv `von` (theo giá): {len(sai)}/{len(von)} dòng lệch đã chốt + lãi chưa chốt theo close; "
                           f"dòng đầu {sai[0][0]['t']:%Y-%m-%d %H:%M}: {sai[0][0]['von']:.4f} vs {sai[0][1]:.4f}")
            else:
                tin.append(f"von.csv `von` (theo giá) {len(von)}/{len(von)} dòng khớp đã chốt + lãi chưa chốt (close nến H4 độc lập)")
        if abs(von[-1].get(c_chot or "von", von_cuoi) - von_cuoi) > NGUONG:
            loi.append(f"von.csv dòng cuối ≠ vốn cuối tính lại {von_cuoi:.4f}")
    else:
        loi.append("không có von.csv để đối chiếu đường vốn")
    # 7. gia vao/ra + duong di so voi nen OHLC
    lg = kiem_gia_nen(lenh, cm)
    if lg:
        loi += [f"giá/đường đi: {x}" for x in lg[:20]] + ([f"giá/đường đi: … tổng {len(lg)} lỗi"] if len(lg) > 20 else [])
    else:
        tin.append(f"giá vào/TP1/ra + đường đi {len(k)}/{len(k)} lệnh khớp nến OHLC độc lập (khớp, SL trước TP, hết giờ)")
    # 8. tom_tat.json
    if tom_tat:
        for kk, gt in (("von_cuoi", von_cuoi), ("lai_usd", von_cuoi - VON0), ("so_lenh", len(k))):
            if isinstance(tom_tat.get(kk), (int, float)):
                (loi if abs(tom_tat[kk] - gt) > NGUONG else tin).append(f"tom_tat.json `{kk}` = {tom_tat[kk]:,.4f} vs tính lại {gt:,.4f}")
    return {"loi": loi, "tin": tin, "von_cuoi": von_cuoi, "lech_lai_max": max(lech_lai + [lech_dl]) if k else 0.0,
            "n": len(k), "cach_phi": ten_cach}


def kiem_von_lenh(lenh, von):
    """Thong tin (khong phai loi): rui ro/von luc dat, don bay, toi da lenh dong thoi."""
    tv = [r["t"] for r in von]
    lech_rr, lech_db = [], []
    for x in lenh:
        if not da_khop(x):
            continue
        j = bisect_right(tv, x["t_quyet_dinh"]) - 1
        v = (von[j].get("von_chot") or von[j].get("von")) if j >= 0 else VON0
        rr = x["khoi_luong"] * abs(gia_dat(x) - x["sl"]) / v
        lech_rr.append(abs(rr - RUI_RO.get(x["loai"], rr)))
        slp = abs(gia_dat(x) - x["sl"]) / gia_dat(x)
        if x["don_bay"] is not None:
            lech_db.append(abs(x["don_bay"] - min(0.4 / slp, 20)))
    su_kien = []
    for x in lenh:
        if x["t_quyet_dinh"] and x["t_ra"]:
            su_kien += [(x["t_quyet_dinh"], 1), (x["t_ra"], -1)]
    dang, mx = 0, 0
    for _, d in sorted(su_kien, key=lambda p: (p[0], p[1])):
        dang += d
        mx = max(mx, dang)
    return {"rr_max": max(lech_rr) if lech_rr else None, "db_max": max(lech_db) if lech_db else None, "dong_thoi": mx}


# ───────────────────────── gia duoc ─────────────────────────
_G = {}  # du lieu dung chung cho tien trinh con (fork)


def ve(x):
    """datetime/epoch/chuoi -> epoch giay (int); None -> None."""
    if x is None or x == "":
        return None
    if isinstance(x, (int, float)):
        return int(x)
    return int(tg(x).timestamp())


def mau_gia_duoc(lenh, kieu, gia_dong):
    """Mau gia duoc. A (dung yeu cau): moi lenh THAT da khop -> limit dat dung gia dong nen ngau nhien.
    B (do nhay): moi lenh DA DAT (ca lenh huy) -> limit cach gia dong dung ti le nhu lenh that (gia_dat / close luc dat).
    Ca hai giu: tai san, chieu, loai, SL % (theo gia dat), TP1/TP2 theo boi R, gio dung, rui ro."""
    ra = []
    for x in lenh:
        if kieu == "A" and not da_khop(x):
            continue
        if x["t_quyet_dinh"] is None or gia_dat(x) is None:
            continue
        g = gia_dat(x)
        kc = abs(g - x["sl"])
        c_dat = gia_dong[x["tai_san"]].get(ve(x["t_quyet_dinh"]))
        if kieu == "B" and not c_dat:
            continue
        ra.append({"ts": x["tai_san"], "chieu": x["chieu"], "loai": x["loai"], "sl_pct": kc / g,
                   "lech": 1.0 if kieu == "A" else g / c_dat,
                   "tp1_R": abs(x["tp1"] - g) / kc if x["tp1"] is not None else None,
                   "tp2_R": abs(x["tp2"] - g) / kc if x["tp2"] is not None else None,
                   "gio_dung": x.get("gio_dung") or GIO_DUNG.get(x["loai"], 120), "rui_ro": RUI_RO.get(x["loai"], 0.02)})
    return ra


def mot_lan_gia_duoc(khoa, i):
    """1 lan gia duoc cho bo <nam>_<ro>; hat giong = chuoi (HAT_GIONG, bo, i) -> tai lap, khong phu thuoc so tien trinh.
    Quy tac von giong dong co (TK 7): so du da chot cong theo tung su kien tien (phi vao, TP1, ra) dung gio xay ra;
    moi tai san 1 lenh; toi da 3 lenh cho + mo; ky quy (giam nua sau TP1) <= 50% so du."""
    g = _G[khoa]
    dc = _G["dc"]
    rnd = random.Random(f"{HAT_GIONG + i}|{khoa}")        # hat giong con = hat giong goc + chi so lan (kem ten bo|kieu)
    ds = sorted(((rnd.choice(g["ung_vien"][m["ts"]]), j, m) for j, m in enumerate(g["mau"])), key=lambda p: (p[0], p[1]))
    so_du, hang, dang, stt, tong_R, n_khop, bo = VON0, [], {}, 0, 0.0, 0, 0
    for t, j, m in ds:
        while hang and hang[0][0] <= t:
            _, _, tien, id_, cuoi = heapq.heappop(hang)
            so_du += tien
            if cuoi:
                dang.pop(id_, None)
        if any(v[0] == m["ts"] for v in dang.values()) or len(dang) >= TOI_DA_LENH:
            bo += 1
            continue
        gia = g["gia_dong"][m["ts"]][t] * m["lech"]
        d = 1 if m["chieu"] == "LONG" else -1
        kc = gia * m["sl_pct"]
        sl = gia - d * kc
        tp1 = gia + d * m["tp1_R"] * kc if m["tp1_R"] is not None else None
        tp2 = gia + d * m["tp2_R"] * kc if m["tp2_R"] is not None else None
        kl = m["rui_ro"] * so_du / kc
        ky_quy = kl * gia / min(0.4 / m["sl_pct"], 20)
        if sum(v[1] * (0.5 if v[2] is not None and v[2] <= t else 1.0) for v in dang.values()) + ky_quy > KY_QUY_TOI_DA * so_du:
            bo += 1
            continue
        r = dc.mo_phong_lenh(m["ts"], m["chieu"], m["loai"], t, gia, sl, tp1, tp2, m["gio_dung"], g["du"][m["ts"]], kl, **g["kw"])
        r = r if isinstance(r, dict) else r._asdict()
        ev = r.get("su_kien") or [(r.get("t_ra") or t + 6 * 4 * 3600, so(r.get("lai_usd")) or 0.0, "ra")]
        for n, (te, tien, _) in enumerate(ev):
            stt += 1
            heapq.heappush(hang, (ve(te), stt, tien, j, n == len(ev) - 1))
        dang[j] = (m["ts"], ky_quy, ve(r.get("t_tp1")))
        if r.get("t_khop") is not None and str(r.get("ly_do_ra", "")).upper() != "HUY":
            n_khop += 1
            tong_R += so(r.get("R")) if r.get("R") not in (None, "") else (so(r.get("lai_usd")) or 0.0) / (kl * kc)
    while hang:
        so_du += heapq.heappop(hang)[2]
    return so_du - VON0, tong_R, n_khop, bo


def _chay_khoi(args):
    khoa, tu, den = args
    return [mot_lan_gia_duoc(khoa, i) for i in range(tu, den)]


def chuan_bi_gia_duoc(dc, khoa, nam, lenh, du_dc, nen4, kieu):
    """Dat du lieu bo <khoa> (vd '2025_6|A') vao _G (truoc khi fork Pool). Tra so lenh mau (0 = khong co)."""
    tu, den = ky(nam)
    gia_dong = {ts: {ve(n[1]): n[5] for n in nen4[ts]} for ts in set(x["tai_san"] for x in lenh)}
    mau = mau_gia_duoc(lenh, kieu, gia_dong)
    ung_vien = {ts: [ve(n[1]) for n in nen4[ts] if tu <= n[1] < den] for ts in set(m["ts"] for m in mau)}
    tham = inspect.signature(dc.mo_phong_lenh).parameters
    _G[khoa] = {"mau": mau, "ung_vien": ung_vien, "gia_dong": gia_dong, "du": {ts: du_dc[ts] for ts in ung_vien},
                "kw": {"ket_thuc": ve(den)} if "ket_thuc" in tham else {}}
    _G["dc"] = dc
    return len(mau)


KIEU_GD = ["A", "B"]
HAT_GIONG_HC = 777


def tao_buoc_ngau_nhien(thu_muc):
    """Nen gia gia lap KHONG co quy luat: buoc ngau nhien log, 16 buoc / nen H4 (O/H/L/C lay tu duong di -> rau nen
    nhat quan voi duong gia), 1D gop tu 6 nen H4 tu 00:00 UTC. Hat giong co dinh HAT_GIONG_HC + chi so tai san."""
    gia0 = {"BTC": 30000.0, "ETH": 1800.0, "OKB": 15.0, "BNB": 300.0, "VANG": 1900.0, "DAU": 80.0}
    for k, ts in enumerate(TAI_SAN_6):
        rnd = random.Random(HAT_GIONG_HC + k)
        t, het, p, h4 = dt.datetime(2022, 6, 1, tzinfo=UTC), dt.datetime(2026, 10, 31, tzinfo=UTC), gia0[ts], []
        while t < het:
            o = h = l = p
            for _ in range(16):
                p *= math.exp(rnd.gauss(0, 0.003))
                h, l = max(h, p), min(l, p)
            h4.append((t, o, h, l, p))
            t += G4
        d1 = {}
        for x in h4:
            d1.setdefault(x[0].replace(hour=0), []).append(x)
        d1 = [(d, v[0][1], max(y[2] for y in v), min(y[3] for y in v), v[-1][4]) for d, v in sorted(d1.items())]
        for ten, ds in (("4H", h4), ("1D", d1)):
            with (Path(thu_muc) / f"{ts}_{ten}.csv").open("w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["ts_utc", "open", "high", "low", "close", "vol"])
                for x in ds:
                    w.writerow([x[0].strftime("%Y-%m-%d %H:%M"), *[repr(v) for v in x[1:]], "1.0"])


def hieu_chinh(dc, ds_nam):
    """Chay dong co (dc.chay) tren du lieu buoc ngau nhien cho moi nam x ro; tra {(nam, ro): {lenh, tk, du, nen4}}."""
    import tempfile
    ra = {}
    with tempfile.TemporaryDirectory(prefix="v4_hieu_chinh_") as tm:
        tao_buoc_ngau_nhien(tm)
        nen4 = {ts: doc_nen(tm, ts, "4H") for ts in TAI_SAN_6}
        du = {ts: dc.nap_du_lieu(ts, tm) for ts in TAI_SAN_6}
        for nam in ds_nam:
            for ro in RO:
                ds = TAI_SAN_6 if ro == "6" else [ro]
                kq = dc.chay(ds, nam, du_lieu={ts: du[ts] for ts in ds})
                lenh = [chuan_lenh(r) for r in kq.lenh]
                ra[(nam, ro)] = {"lenh": lenh, "tk": thong_ke(lenh, None), "du": du, "nen4": nen4}
    return ra


def chay_gia_duoc(ds_khoa, so_lan):
    """Gia duoc cho MOI bo cung luc: 1 Pool (so loi may), viec = khoi 10 lan cua 1 bo, xen ke cac bo."""
    viec = [(k, a, min(a + 10, so_lan)) for a in range(0, so_lan, 10) for k in ds_khoa]
    so_tt = max(1, os.cpu_count() or 2)
    try:
        with mp.get_context("fork").Pool(so_tt) as pool:
            kq = pool.map(_chay_khoi, viec, chunksize=1)
    except (OSError, ValueError, RuntimeError):
        kq = [_chay_khoi(v) for v in viec]
    gop = {k: [] for k in ds_khoa}
    for (k, a, _), ds in sorted(zip(viec, kq), key=lambda p: (p[0][0], p[0][1])):
        gop[k] += ds
    return {k: {"lai": [x[0] for x in v], "R": [x[1] for x in v], "n": [x[2] for x in v], "bo": [x[3] for x in v],
                "so_mau": len(_G[k]["mau"])} for k, v in gop.items()}, so_tt


def pv_that(gd, t):
    """(phan vi $, phan vi tong R, phan vi R TB/lenh) cua ket qua that = % lan gia duoc THAP HON that."""
    if not gd:
        return None, None, None
    rtb = [r / n for r, n in zip(gd["R"], gd["n"]) if n]
    return (sum(x < t["lai"] for x in gd["lai"]) / len(gd["lai"]) * 100,
            sum(x < t["tong_R"] for x in gd["R"]) / len(gd["R"]) * 100,
            sum(x < t["R_tb"] for x in rtb) / len(rtb) * 100 if rtb and t["R_tb"] is not None else None)


def pv_s(gd, t):
    a, b, c = pv_that(gd, t)
    return "—" if a is None else f"{a:.0f} / {b:.0f} / {'—' if c is None else f'{c:.0f}'}"


def phan_vi(xs, p):
    s = sorted(xs)
    return s[min(len(s) - 1, max(0, int(round(p / 100 * (len(s) - 1)))))]


# ───────────────────────── do giong ─────────────────────────
def huong_phieu(p):
    """Huong H4 cua phieu (giong thi/tao_ho_so.huong_h4 + chuan khung cua thi/cham.chuan_bai)."""
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    nd = d.get("nhan_dinh") or []
    for k in ("H4", "chung"):
        for x in nd:
            kh = str(x.get("khung") or "")
            kh = {"4H": "H4", "CHUNG": "chung"}.get(kh.upper(), kh)
            if kh == k:
                return chuan_huong(x.get("huong"))
    return None


def luat_tu_tren_xuong(h4, d1, dong_h4, dong_d1, C):
    """Dinh nghia docstring thi/cham.py: EMA H4 34/89/200 chum < 0,6% -> PHAN VAN; khong thi TANG khi dong D1 <= EMA89 D1 x 1,01
    va nhip 24h > -1%; con lai GIAM. Chi nen da dong <= C."""
    i = bisect_right(dong_h4, C)
    c4 = [n[5] for n in h4[:i]]
    gia, T = h4[i - 1][5], h4[i - 1][1]
    e = [ema_cuoi(c4, k) for k in (34, 89, 200)]
    j = bisect_right(dong_d1, C)
    d1c = [n[5] for n in d1[:j]]
    e89d = ema_cuoi(d1c, 89)
    k24 = bisect_right(dong_h4, T - dt.timedelta(hours=24)) - 1
    p24 = h4[k24][5] if k24 >= 0 and h4[k24][1] == T - dt.timedelta(hours=24) else None
    if (max(e) - min(e)) / gia * 100 < 0.6:
        return "PHAN_VAN"
    if p24 is not None and d1c[-1] <= e89d * 1.01 and (gia / p24 - 1) * 100 > -1:
        return "TANG"
    return "GIAM"


def do_giong(dc, du_btc, nen_btc4, nen_btc1):
    buoi = []
    with (GOC / "transcripts" / "gio_live.tsv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            bd = dt.datetime.strptime(r["bat_dau_vn"].strip(), "%Y-%m-%d %H:%M").replace(tzinfo=VN)
            buoi.append((r["id"], bd, int(r["phut"])))
    p1 = {Path(p).stem[-11:]: Path(p) for p in (GOC / "phieu").glob("2*.json")}
    p2 = {Path(p).stem[-11:]: Path(p) for p in (GOC / "thi" / "dap_an_v2" / "phieu").glob("2*.json")}
    dong_h4 = [n[1] for n in nen_btc4]
    dong_d1 = [n[1] for n in nen_btc1]
    ra, thieu, ro_ri = [], [], 0
    for vid, bd, phut in buoi:
        C = (bd + dt.timedelta(minutes=phut)).astimezone(UTC)
        ngay = (p1.get(vid) or p2.get(vid)).stem[:10] if (p1.get(vid) or p2.get(vid)) else bd.strftime("%Y-%m-%d")
        nguon = p2 if ngay >= "2026-07-01" else p1
        p = nguon.get(vid)
        if p is None:
            thieu.append(vid)
            continue
        v = dc.view_tai("BTC", C, du_btc)
        v = v if isinstance(v, dict) else v._asdict()
        gc = tg(v.get("gio_cat"))
        if gc is not None and gc > C:
            ro_ri += 1
        ra.append({"ten": p.stem, "ngay": ngay, "C": C, "nguoi": huong_phieu(p), "bot": chuan_huong(v.get("view")),
                   "pha": chuan_huong(v.get("pha")), "gio_cat": gc, "nguon": tuong_doi(p),
                   "luat": luat_tu_tren_xuong(nen_btc4, nen_btc1, dong_h4, dong_d1, C), "giam": "GIAM"})
    return ra, thieu, ro_ri, len(buoi)


def bang_do_giong(ds, nhan_nhom):
    so_ = [r for r in ds if r["nguoi"] in NHAN]
    N = len(so_)
    L = []
    if not N:
        return [f"_{nhan_nhom}: không có buổi có nhãn hợp lệ._"]
    L += [f"{N} buổi có nhãn người đó hợp lệ (loại {len(ds) - N} buổi nhãn không hợp lệ" +
          (": " + ", ".join(r["ten"] for r in ds if r["nguoi"] not in NHAN) if len(ds) > N else "") + ").",
          "", "| Cách đoán | Trùng 3 nhãn | Khi cả 2 có hướng | Bot − cách này (điểm %) |", "|---|---|---|---|"]
    dung = {}
    for k, ten in (("bot", "**Bot v4** (`view_tai`)"), ("giam", "Luôn GIẢM"), ("luat", "Luật từ trên xuống (thi/cham.py)")):
        dung[k] = sum(r[k] == r["nguoi"] for r in so_)
        ch = [r for r in so_ if r[k] in ("TANG", "GIAM") and r["nguoi"] in ("TANG", "GIAM")]
        chenh = "—" if k == "bot" else f"{(dung['bot'] - dung[k]) / N * 100:+.0f}"
        L.append(f"| {ten} | **{ty_le(dung[k], N)}** | {ty_le(sum(r[k] == r['nguoi'] for r in ch), len(ch))} | {chenh} |")
    # McNemar bot vs moc
    L.append("")
    for k, ten in (("giam", "luôn GIẢM"), ("luat", "luật từ trên xuống")):
        b_ = sum(1 for r in so_ if r["bot"] == r["nguoi"] and r[k] != r["nguoi"])
        c_ = sum(1 for r in so_ if r[k] == r["nguoi"] and r["bot"] != r["nguoi"])
        n_ = b_ + c_
        p = min(1.0, 2 * sum(math.comb(n_, i) for i in range(0, min(b_, c_) + 1)) / 2 ** n_) if n_ else 1.0
        L.append(f"- McNemar bot vs {ten}: bot đúng–mốc sai {b_} / mốc đúng–bot sai {c_}, p = {phay(p, 3)} (nhị thức chính xác, hai phía).")
    pn, pb = Counter(r["nguoi"] for r in so_), Counter(r["bot"] for r in so_)
    L += ["", f"Người đó: TĂNG {pn['TANG']} · GIẢM {pn['GIAM']} · PHÂN VÂN {pn['PHAN_VAN']} — Bot: TĂNG {pb['TANG']} · "
              f"GIẢM {pb['GIAM']} · PHÂN VÂN {pb['PHAN_VAN']} · không hợp lệ {pb[None]}", "",
          "Bảng chéo (dòng = người đó, cột = bot):", "",
          "| | TĂNG | GIẢM | PHÂN VÂN | Không hợp lệ | Tổng |", "|---|---|---|---|---|---|"]
    for x in NHAN:
        hang = [sum(1 for r in so_ if r["nguoi"] == x and r["bot"] == y) for y in NHAN + [None]]
        L.append(f"| **{VIET[x]}** | " + " | ".join(map(str, hang)) + f" | {sum(hang)} |")
    L.append("| Tổng | " + " | ".join(str(sum(1 for r in so_ if r["bot"] == y)) for y in NHAN + [None]) + f" | {N} |")
    return L


# ───────────────────────── trich v1/v2 ─────────────────────────
def tim_dong(p, *mau):
    """[(so dong, noi dung)] cac dong chua TAT CA chuoi trong mau."""
    ra = []
    for i, d in enumerate(Path(p).read_text(encoding="utf-8").splitlines(), 1):
        if all(m in d for m in mau):
            ra.append((i, d))
    return ra


def o_bang(d):
    return [c.strip() for c in d.strip().strip("|").split("|")]


def trich_v1_v2():
    """Tra (bang so sanh, dong nguon). Chi lay dong khop DUY NHAT; khong khop -> ghi ro."""
    f1 = GOC / "backtest" / "KET_QUA_NGOAI_MAU.md"
    f2 = GOC / "backtest" / "KET_QUA_V2.md"
    hang, nguon = [], []

    def lay(f, mau, ban, nam_, ro, cot):
        ds = tim_dong(f, *mau)
        if len(ds) != 1:
            nguon.append(f"- `{tuong_doi(f)}`: tìm {mau} → {len(ds)} dòng (cần đúng 1) — BỎ")
            return
        i, d = ds[0]
        o = o_bang(d)
        hang.append({"ban": ban, "nam": nam_, "ro": ro, **{k: o[j] for k, j in cot.items()}, "nguon": f"{tuong_doi(f)}:{i}"})
        nguon.append(f"- `{tuong_doi(f)}:{i}` → `{d.strip()}`")

    c1 = {"lai": 3, "pct": 4, "n": 5, "thang": 6, "R_tb": 7, "t": 8, "dd": 9, "pf": 10, "pv": 11, "pvR": 12}
    lay(f1, ("| 2025 (ngoài mẫu) | (i) theo GIÁ | **A**",), "v1 (luật 8 theo GIÁ, tối đa 3 lệnh)", 2025, "6", c1)
    lay(f1, ("| 2026 (trong mẫu, 6 TS) | (i) theo GIÁ | **A**",), "v1 (luật 8 theo GIÁ, tối đa 3 lệnh)", 2026, "6", c1)
    c2 = {"lai": 1, "pct": 2, "n": 3, "thang": 4, "R_tb": 5, "tong_R": 6, "dd": 7, "pf": 8, "pv": 9, "pvR": 10}
    lay(f2, ("| **v2** · 2025 (ngoài mẫu) |",), "v2 (tối đa 4 lệnh)", 2025, "6", c2)
    lay(f2, ("| **v2** · 2026 (trong mẫu) |",), "v2 (tối đa 4 lệnh)", 2026, "6", c2)
    # BTC trong ro 6 (KHONG phai chay rieng BTC): bang theo tai san
    nguon_btc = []
    for f, ten, mau_muc, cot in ((f1, "v1", "**2025 (ngoài mẫu)**", {"n": 1, "tong_R": 4, "lai": 5}),
                                 (f1, "v1", "**2026 (trong mẫu, 6 TS)**", {"n": 1, "tong_R": 4, "lai": 5}),
                                 (f2, "v2", "**2025 (ngoài mẫu)**", {"n": 4, "thang": 6, "tong_R": 7, "lai": 8}),
                                 (f2, "v2", "**2026 (trong mẫu)**", {"n": 4, "thang": 6, "tong_R": 7, "lai": 8})):
        dong = Path(f).read_text(encoding="utf-8").splitlines()
        bd = next((i for i, d in enumerate(dong) if d.strip() == mau_muc), None)
        if bd is None:
            continue
        j = next((i for i in range(bd, min(bd + 15, len(dong))) if dong[i].startswith("| BTC |")), None)
        if j is None:
            continue
        o = o_bang(dong[j])
        nam_ = 2025 if "2025" in mau_muc else 2026
        nguon_btc.append({"ban": ten, "nam": nam_, **{k: o[c] for k, c in cot.items()}, "nguon": f"{tuong_doi(f)}:{j + 1}",
                          "dong": dong[j].strip()})
    return hang, nguon, nguon_btc


# ───────────────────────── mua giu BTC ─────────────────────────
def mua_giu(nen1, nam):
    tu, den = ky(nam)
    dau = [n for n in nen1 if n[1] <= tu]
    trong = [n for n in nen1 if tu < n[1] <= den]
    if not dau or not trong:
        return None
    p0 = dau[-1][5]
    sl = VON0 * (1 - PHI_MARKET) / p0
    gt = [sl * n[5] for n in trong]
    cuoi = gt[-1] * (1 - PHI_MARKET)
    return {"p0": p0, "p1": trong[-1][5], "t0": dau[-1][1], "t1": trong[-1][1], "lai": cuoi - VON0, "pct": cuoi / VON0 - 1,
            "dd": sut_giam([VON0 * (1 - PHI_MARKET)] + gt)}


# ───────────────────────── phan dau bao cao ─────────────────────────
def dem_muc(p):
    """Mo ta so muc: DIEN_GIAI -> so muc '**DG n'; NHAT_KY_SUA -> so tieu de sau '## Cac lan sua sau moc 0'."""
    if not p.exists():
        return None
    d = p.read_text(encoding="utf-8").splitlines()
    dg = [x for x in d if re.match(r"^\*\*DG \d+", x)]
    if dg:
        return f"{len(dg)} mục (DG 1 – DG {re.match(r'^\*\*DG (\d+)', dg[-1])[1]})"
    i = next((j for j, x in enumerate(d) if x.startswith("## ") and "sau mốc 0" in x), None)
    if i is not None:
        sua = [x for x in d[i + 1:] if re.match(r"^#{2,4}\s", x)]
        return f"{len([x for x in d if x.startswith('## ')])} mục cấp 2; **{len(sua)} lần sửa sau mốc 0** (chạy dữ liệu thật đầu tiên)"
    return f"{sum(1 for x in d if re.match(r'^##\s', x))} mục"


def muc_0_thiet_ke(v4):
    p = Path(v4) / "THIET_KE.md"
    d = (p if p.exists() else V4_MAC_DINH / "THIET_KE.md").read_text(encoding="utf-8").splitlines()
    bd = next(i for i, x in enumerate(d) if x.startswith("## 0."))
    kt = next(i for i in range(bd + 1, len(d)) if d[i].startswith("## "))
    return d[bd:kt]


def nhan_tep(p, v4):
    """Ten tep de doi chieu KHOA.md: tep trong thu muc v4 -> 'bot_v4/<tuong doi>' (chay trong ban sao van so dung khoa)."""
    try:
        return "bot_v4/" + str(Path(p).resolve().relative_to(Path(v4).resolve()))
    except ValueError:
        return tuong_doi(p)


def kiem_khoa(v4):
    """Doc moi dong '| `tep` | `sha` |' trong KHOA.md -> [(tep, sha khoa, sha hien tai)]; 'bot_v4/...' tinh trong thu muc v4."""
    p = Path(v4) / "KHOA.md"
    if not p.exists():
        p = V4_MAC_DINH / "KHOA.md"
    ra = []
    if p.exists():
        for m in re.finditer(r"\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`", p.read_text(encoding="utf-8")):
            t = m[1]
            tep = Path(v4) / t[len("bot_v4/"):] if t.startswith("bot_v4/") else GOC / t
            ra.append((t, m[2], sha(tep)))
    return ra


def kiem_sha256sums(thu_muc):
    p = Path(thu_muc) / "SHA256SUMS"
    if not p.exists():
        return None, []
    sai = []
    n = 0
    for d in p.read_text().splitlines():
        if not d.strip():
            continue
        h, ten = d.split(None, 1)
        n += 1
        if sha(Path(thu_muc) / ten.strip()) != h:
            sai.append(ten.strip())
    return n, sai


def bang_nguon_du_lieu(thu_muc):
    p = Path(thu_muc) / "NGUON.md"
    if not p.exists():
        return []
    return [d for d in p.read_text(encoding="utf-8").splitlines() if d.startswith("|")]


# ───────────────────────── chinh ─────────────────────────
def main():
    a = argparse.ArgumentParser(description="Báo cáo bot v4 → KET_QUA.md")
    a.add_argument("--v4", default=str(V4_MAC_DINH), help="thư mục chứa dong_co.py, ket_qua/, du_lieu/")
    a.add_argument("--ra", default=None, help="file báo cáo (mặc định <v4>/KET_QUA.md)")
    a.add_argument("--so-gia-duoc", type=int, default=SO_GIA_DUOC)
    a.add_argument("--nam", type=int, nargs="*", default=NAM)
    a.add_argument("--khong-hieu-chinh", dest="hieu_chinh", action="store_false",
                   help="bỏ phần hiệu chỉnh giả dược trên dữ liệu bước ngẫu nhiên")
    a = a.parse_args()
    v4 = Path(a.v4).resolve()
    ra_file = Path(a.ra) if a.ra else v4 / "KET_QUA.md"
    thu_muc_du = v4 / "du_lieu"
    bat_dau = time.time()
    dc = nap_dong_co(v4)
    if dc is None:
        sys.exit(f"Không thấy {v4 / 'dong_co.py'}")
    ghi_chu = []
    # du lieu nen doc lap (cho gia duoc, mua giu, luat tu tren xuong)
    nen4 = {ts: doc_nen(thu_muc_du, ts, "4H") for ts in TAI_SAN_6}
    nen1 = {ts: doc_nen(thu_muc_du, ts, "1D") for ts in TAI_SAN_6}
    du_dc = {ts: dc.nap_du_lieu(ts, thu_muc_du) for ts in TAI_SAN_6}
    cm = ChiMucNen(nen4)

    # 1. ket qua + tu cong lai + chuan bi gia duoc (A theo yeu cau, B do nhay)
    KQ, ds_gd = {}, []
    for nam in a.nam:
        for ro in RO:
            print(f"· {nam} rổ {ro}", file=sys.stderr)
            kq = doc_ket_qua(v4, dc, nam, ro, ghi_chu)
            if kq is None:
                ghi_chu.append(f"{nam}_{ro}: KHÔNG có kết quả")
                continue
            kq["tk"] = thong_ke(kq["lenh"], kq["von"])
            kq["kiem"] = tu_cong_lai(kq["lenh"], kq["von"], kq["tom_tat"], cm)
            kq["von_lenh"] = kiem_von_lenh(kq["lenh"], kq["von"])
            kq["gd"] = {}
            for kieu in KIEU_GD:
                if chuan_bi_gia_duoc(dc, f"{nam}_{ro}|{kieu}", nam, kq["lenh"], du_dc, nen4, kieu):
                    ds_gd.append(f"{nam}_{ro}|{kieu}")
            KQ[(nam, ro)] = kq
    # 1b. hieu chinh gia duoc: dong co chay tren du lieu buoc ngau nhien (khong co quy luat) -> phan vi phai quanh 50
    HC = {}
    if a.hieu_chinh:
        print("· hiệu chỉnh: chạy động cơ trên dữ liệu bước ngẫu nhiên", file=sys.stderr)
        HC = hieu_chinh(dc, a.nam)
        for (nam, ro), h in HC.items():
            for kieu in KIEU_GD:
                if chuan_bi_gia_duoc(dc, f"HC_{nam}_{ro}|{kieu}", nam, h["lenh"], h["du"], h["nen4"], kieu):
                    ds_gd.append(f"HC_{nam}_{ro}|{kieu}")
    t0 = time.time()
    gd, so_tt = chay_gia_duoc(ds_gd, a.so_gia_duoc) if ds_gd else ({}, 0)
    for k, v in gd.items():
        ten, kieu = k.split("|")
        if ten.startswith("HC_"):
            n_, r_ = ten[3:].split("_")
            HC[(int(n_), r_)].setdefault("gd", {})[kieu] = v
        else:
            n_, r_ = ten.split("_")
            KQ[(int(n_), r_)]["gd"][kieu] = v
    print(f"· giả dược {a.so_gia_duoc} lần × {len(ds_gd)} bộ, {so_tt} tiến trình: {time.time() - t0:.0f}s", file=sys.stderr)

    # 2. do giong
    print("· độ giống 180 buổi", file=sys.stderr)
    dg, dg_thieu, dg_ro_ri, dg_tong = do_giong(dc, du_dc["BTC"], nen4["BTC"], nen1["BTC"])

    # ─────── viet bao cao ───────
    L = []
    W = L.append
    tong_loi = sum(len(k["kiem"]["loi"]) for k in KQ.values())
    W("# KẾT QUẢ BOT V4 — backtest 2024 / 2025 / 2026 · giả dược · độ giống")
    W("")
    W(f"_Sinh tự động bởi `bot_v4/bao_cao.py` lúc {dt.datetime.now(VN):%Y-%m-%d %H:%M} VN "
      f"(chạy {time.time() - bat_dau:.0f} giây). Chạy lại: `python3 bot_v4/bao_cao.py`. Thiết kế: [THIET_KE.md](THIET_KE.md) (mục 8)._")
    W("")
    if tong_loi:
        W(f"> # ❌ LỖI TỰ CỘNG LẠI: {tong_loi} chỗ lệch > 0,01$ — xem mục 1. KHÔNG dùng số bên dưới trước khi sửa.")
    else:
        W("> **Tự cộng lại độc lập: KHỚP** — mọi lệnh, chuỗi von_sau và von.csv khớp tới 0,01$ (mục 1).")
    W("")

    # 0. dau van tay
    W("## 0. Dấu vân tay lúc chạy, khoá, giới hạn")
    W("")
    khoa = {t: (h, ht) for t, h, ht in kiem_khoa(v4)}
    chi_bao = [p for p in (v4 / "chi_bao.py", GOC / "cong_cu" / "chi_bao.py") if p.exists()]
    W("| Tệp | sha256 lúc chạy | So với `bot_v4/KHOA.md` |")
    W("|---|---|---|")
    da_in = set()
    for p in [v4 / "THIET_KE.md", v4 / "dong_co.py"] + chi_bao + [thu_muc_du / "SHA256SUMS"]:
        t = nhan_tep(p, v4)
        da_in.add(t)
        h = sha(p)
        so_khoa = "chưa khoá" if t not in khoa else ("**KHỚP**" if khoa[t][0] == h else f"**LỆCH** (khoá `{khoa[t][0][:16]}…`)")
        W(f"| `{t}` | `{h}` | {so_khoa} |")
    if not chi_bao:
        W("| `chi_bao.py` | (không thấy ở bot_v4/ hay cong_cu/) | — |")
    for t, (h, ht) in khoa.items():
        if t not in da_in:
            W(f"| `{t}` (mục khoá khác) | `{ht}` | {'**KHỚP**' if h == ht else '**LỆCH**'} |")
    n_sum, sai_sum = kiem_sha256sums(thu_muc_du)
    W("")
    W(f"Dữ liệu: {n_sum} tệp trong `SHA256SUMS`, " + ("**tất cả khớp** nội dung hiện tại." if not sai_sum else
                                                     f"**LỆCH: {', '.join(sai_sum)}**."))
    for ten in ("DIEN_GIAI.md", "NHAT_KY_SUA.md"):
        n = dem_muc(v4 / ten)
        W(f"- [`bot_v4/{ten}`]({ten}): " + ("**chưa có tệp**" if n is None else n))
    W("")
    W("### Giới hạn trung thực (chép nguyên mục 0 `THIET_KE.md`)")
    W("")
    for d in muc_0_thiet_ke(v4)[1:]:
        W("> " + d if d.strip() else ">")
    W("")
    W("### Độ phủ dữ liệu (`bot_v4/du_lieu/NGUON.md`)")
    W("")
    L.extend(bang_nguon_du_lieu(thu_muc_du))
    W("")
    W("> **Cảnh báo dữ liệu:** VÀNG/DẦU 4H chỉ có từ **2024-06-10** (Yahoo giới hạn 1H ~2 năm), BNB từ **2022-12-21**. "
      "→ Năm **2024** rổ 6 tài sản thực chất **thiếu vàng/dầu nửa đầu năm**, và EMA610 H4 của vàng/dầu chưa đủ khởi động "
      "(610 nến H4 ≈ 4–5 tháng giao dịch) tới khoảng cuối 2024. Xem số lệnh theo tài sản theo năm ở mục 5.")
    W("")

    # 1. tu cong lai
    W("## 1. Tự cộng lại độc lập (lenh.csv → lãi từng lệnh → von_sau → von.csv)")
    W("")
    W("Cách tính lại (không dùng mã động cơ, chỉ lenh.csv + quy tắc mục 7 + nến `bot_v4/du_lieu/` đọc riêng):")
    W("")
    W("1. **Lãi từng lệnh** = chiều × KL × tỉ lệ TP1 × (giá chốt TP1 − vào) + chiều × KL × phần còn lại × (giá ra − vào) − phí, "
      "so với `lai_usd`; **phí** tính lại theo mục 7 (vào 0,02%; TP 0,02%; SL/hết giờ/hết kỳ 0,05% + trượt 0,02%) so với cột `phi`; "
      "và lãi tính độc lập hoàn toàn (giá + quy tắc phí, không dùng cột phí) so với `lai_usd`.")
    W("2. **R** = lai_usd ÷ (KL × |giá đặt − SL|) so với cột `R`.")
    W("3. **Dòng tiền**: phí vào lúc khớp, chốt TP1 lúc TP1, phần còn lại lúc ra → cộng dồn từ 4.000$ theo giờ → so `von_sau` "
      "từng lệnh, cột `von_chot` mọi dòng von.csv; cột `von` (theo giá) = đã chốt + lãi chưa chốt của vị thế đang mở theo close "
      "nến H4 (đọc độc lập).")
    W("4. **Giá + đường đi theo nến OHLC**: lệnh khớp ở nến SAU nến đặt (≤ 6 nến), nến đầu tiên chạm giá limit; giá vào = limit "
      "(hoặc giá mở nếu mở đã vượt); giữa khớp và ra không nến nào chạm SL/TP1/TP2 hay quá giờ dừng; nến ra đúng lý do (SL xét "
      "trước TP; SL/hết giờ/hết kỳ = mức hoặc giá mở/close × trượt 0,02%; TP = mức hoặc giá mở).")
    W("")
    W("| Năm · rổ | Nguồn | Lệnh khớp | Lệch lãi lớn nhất | Vốn cuối tính lại | Kết quả |")
    W("|---|---|---|---|---|---|")
    for (nam, ro), k in KQ.items():
        kk = k["kiem"]
        W(f"| {nam} · {TEN_RO[ro]} | `{k['nguon']}` | {kk['n']} | {so_vn(kk['lech_lai_max'], 6)}$ | {so_vn(kk['von_cuoi'], 2)}$ | "
          + ("**KHỚP**" if not kk["loi"] else f"**❌ {len(kk['loi'])} LỖI**") + " |")
    W("")
    for (nam, ro), k in KQ.items():
        kk = k["kiem"]
        if kk["loi"]:
            W(f"### ❌ LỖI {nam} · {TEN_RO[ro]}")
            for x in kk["loi"][:25]:
                W(f"- **{x}**")
            if len(kk["loi"]) > 25:
                W(f"- … và {len(kk['loi']) - 25} lỗi nữa")
            W("")
    W("<details><summary>Chi tiết các phép kiểm khớp</summary>")
    W("")
    for (nam, ro), k in KQ.items():
        vl = k["von_lenh"]
        W(f"- **{nam} · {TEN_RO[ro]}**: " + "; ".join(k["kiem"]["tin"])
          + (f"; rủi ro/vốn lúc đặt lệch tối đa {vl['rr_max'] * 100:.3f} điểm % so với 2%/1%" if vl["rr_max"] is not None else "")
          + (f"; đòn bẩy lệch min(40%/SL%, 20) tối đa {vl['db_max']:.4f}" if vl["db_max"] is not None else "")
          + f"; lệnh chờ + mở đồng thời tối đa {vl['dong_thoi']}")
    W("")
    W("_Rủi ro/vốn và đòn bẩy chỉ là thông tin (vốn lúc đặt tính bằng vốn đã chốt; động cơ có thể dùng cách khác)._")
    W("")
    W("</details>")
    W("")

    # 2. bang chinh
    W("## 2. Bảng chính: năm × rổ")
    W("")
    W("| Năm | Rổ | Lãi$ | % | Số lệnh (L/S) | Huỷ | % thắng | R TB | t (R TB) | Tổng R | Sụt giảm max | Hệ số LN |")
    W("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for (nam, ro), k in KQ.items():
        t = k["tk"]
        W(f"| {nam}{' (trong mẫu)' if nam == 2026 else ''} | {TEN_RO[ro]} | **{usd(t['lai'])}** | {pt(t['pct'])} | "
          f"{t['n']} ({t['long']}/{t['short']}) | {t['huy']} | {pt(t['thang'], 0, False)} | {phay(t['R_tb'], 2, True)} | "
          f"{phay(t['t'], 1, True)} | {phay(t['tong_R'], 1, True)} | {pt(t['dd'], 1, False)} | {pf_s(t['pf'])} |")
    W("")
    c = cot_von(next(iter(KQ.values()))["von"]) if KQ else None
    W(f"_Lệnh = lệnh đã khớp; Huỷ = lệnh chờ hết hiệu lực/huỷ (không tính). % thắng = lai_usd > 0. R = cột `R` của lenh.csv "
      f"(đã kiểm = lãi ÷ rủi ro SL danh nghĩa). t = R TB ÷ (độ lệch chuẩn R / √n): |t| < 2 = chưa phân biệt được với 0. "
      f"Sụt giảm max tính trên cột `{c}` của von.csv (mỗi nến H4). Hệ số LN = Σ lãi ÷ Σ lỗ (USD)._")
    W("")

    # 3. so sanh
    W("## 3. So với v1, v2 và mua-giữ BTC")
    W("")
    hang, nguon, nguon_btc = trich_v1_v2()
    W("| Bản | Năm | Rổ | Lãi$ | % | Số lệnh | % thắng | R TB | Sụt giảm | Hệ số LN | Phân vị giả dược — v4: ($ / tổng R / R TB) A (theo yêu cầu) · B (công bằng hơn); v1/v2: ($ / R) | Nguồn |")
    W("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for nam in a.nam:
        for ro in RO:
            if (nam, ro) in KQ:
                t = KQ[(nam, ro)]["tk"]
                gd = KQ[(nam, ro)]["gd"]
                pv = f"A {pv_s(gd.get('A'), t)} · B {pv_s(gd.get('B'), t)}"
                W(f"| **v4** | {nam} | {TEN_RO[ro]} | {usd(t['lai'])} | {pt(t['pct'])} | {t['n']} | {pt(t['thang'], 0, False)} | "
                  f"{phay(t['R_tb'], 2, True)} | {pt(t['dd'], 1, False)} | {pf_s(t['pf'])} | {pv} | bản này |")
        for h in hang:
            if h["nam"] == nam:
                W(f"| {h['ban']} | {nam} | {TEN_RO[h['ro']]} | {h['lai']} | {h['pct']} | {h['n']} | {h['thang']} | {h['R_tb']} | "
                  f"{h['dd']} | {h['pf']} | {h['pv']} / {h['pvR']} (200 lần, khác cách) | `{h['nguon']}` |")
        for h in nguon_btc:
            if h["nam"] == nam:
                W(f"| {h['ban']} — chỉ lệnh BTC trong rổ 6 | {nam} | (BTC trong rổ 6) | {h['lai']} | — | {h['n']} | "
                  f"{h.get('thang', '—')} | tổng R {h['tong_R']} | — | — | — | `{h['nguon']}` |")
        mg = mua_giu(nen1["BTC"], nam)
        if mg:
            W(f"| Mua-giữ BTC | {nam} | BTC | {usd(mg['lai'])} | {pt(mg['pct'])} | 1 | — | — | {pt(mg['dd'], 1, False)} | — | — | "
              f"`bot_v4/du_lieu/BTC_1D.csv` |")
        if nam == 2024:
            W("| v1 / v2 | 2024 | — | chưa từng chạy 2024 | | | | | | | | — |")
    W("")
    W("Dòng nguồn trích nguyên văn (v1/v2 KHÔNG chạy lại ở đây; v1/v2 dùng dữ liệu `backtest/`, phân vị giả dược 200 lần "
      "đổi cả chiều 50/50 và vào ở giá đóng cùng tháng — không cùng cách với giả dược v4 ở mục 4):")
    W("")
    L.extend(nguon)
    for h in nguon_btc:
        W(f"- `{h['nguon']}` → `{h['dong']}`")
    W("")
    W("_Mua-giữ BTC: mua ở close nến D1 đóng lúc bắt đầu kỳ (00:00 UTC 01/01), bán ở close D1 cuối kỳ (2026: D1 30/10), "
      "phí 0,05% mỗi đầu, sụt giảm theo close D1. v1/v2 ghi mua-giữ theo mốc 00:00 VN nên lệch nhẹ._")
    W("")
    for nam in a.nam:
        mg = mua_giu(nen1["BTC"], nam)
        if mg:
            W(f"- Mua-giữ BTC {nam}: {so_vn(mg['p0'], 1)} ({mg['t0']:%Y-%m-%d %H:%M} UTC) → {so_vn(mg['p1'], 1)} ({mg['t1']:%Y-%m-%d %H:%M} UTC)")
    W("")

    # 4. gia duoc
    W(f"## 4. Giả dược ({so_vn(a.so_gia_duoc, 0)} lần/bộ, hạt giống gốc `{HAT_GIONG}`)")
    W("")
    W("| Năm · rổ | Kiểu | Lệnh mẫu | Thật $ | Giả dược P5 / P50 / P95 ($) | % lần giả dược lãi | **Phân vị thật ($)** | "
      "Tổng R thật | Giả dược tổng R P5 / P50 / P95 | **Phân vị thật (tổng R)** | R TB thật | Giả dược R TB P50 | "
      "**Phân vị thật (R TB)** | Lệnh giả dược khớp TB (bị bỏ vì quy tắc vốn TB) |")
    W("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for (nam, ro), k in KQ.items():
        t = k["tk"]
        for kieu in KIEU_GD:
            gd = k["gd"].get(kieu)
            if not gd:
                W(f"| {nam} · {TEN_RO[ro]} | {kieu} | 0 | — | — | — | — | — | — | — | — | — | — | — |")
                continue
            n = len(gd["lai"])
            p1, p2, p3 = pv_that(gd, t)
            rtb = [r / m for r, m in zip(gd["R"], gd["n"]) if m]
            W(f"| {nam} · {TEN_RO[ro]} | {kieu} | {gd['so_mau']} | {usd(t['lai'])} | {usd(phan_vi(gd['lai'], 5))} / "
              f"{usd(phan_vi(gd['lai'], 50))} / {usd(phan_vi(gd['lai'], 95))} | {sum(x > 0 for x in gd['lai']) / n:.0%} | "
              f"**{phay(p1, 1)}** | {phay(t['tong_R'], 1, True)} | "
              f"{phay(phan_vi(gd['R'], 5), 1, True)} / {phay(phan_vi(gd['R'], 50), 1, True)} / {phay(phan_vi(gd['R'], 95), 1, True)} | "
              f"**{phay(p2, 1)}** | {phay(t['R_tb'], 3, True)} | {phay(phan_vi(rtb, 50), 3, True)} | **{phay(p3, 1)}** | "
              f"{phay(statistics.mean(gd['n']), 1)} ({phay(statistics.mean(gd['bo']), 1)}) |")
    W("")
    W("**Hai kiểu giả dược** (đều: 1 lệnh giả dược cho mỗi lệnh mẫu, cùng tài sản, chiều, loại chính/hồi, khoảng SL % theo giá đặt "
      "limit, TP1/TP2 theo bội R, giờ dừng theo cột `gio_dung` (chính 120h, hồi 48h); thời điểm đặt rút ngẫu nhiên ĐỀU trong các giờ "
      "ĐÓNG nến H4 của tài sản đó trong cùng kỳ; mô phỏng bằng `dong_co.mo_phong_lenh` — hiệu lực 6 nến, huỷ khi view đổi, khớp, "
      "SL trước TP, phí như lệnh thật):")
    W("")
    W("- **A — đúng yêu cầu mục 8**: mẫu = lệnh thật ĐÃ KHỚP; limit đặt đúng giá close nến ngẫu nhiên (gần như khớp ngay nến sau).")
    W("- **B — công bằng với cách vào limit**: mẫu = MỌI lệnh đã đặt (cả lệnh bị huỷ); limit cách close nến ngẫu nhiên đúng tỉ lệ "
      "như lệnh thật (giá đặt ÷ close lúc đặt) → giữ cả cơ chế chờ hồi về vùng, tỉ lệ khớp; chỉ bỏ phần CHỌN vùng/thời điểm.")
    W("")
    W(f"Quy tắc vốn như thật: xét theo thứ tự thời gian; khối lượng = rủi ro (chính 2% / hồi 1%) × số dư đã chốt ÷ khoảng SL; "
      f"số dư cộng theo từng sự kiện tiền của `mo_phong_lenh` (phí vào, TP1, lúc ra) đúng giờ xảy ra; tối đa {TOI_DA_LENH} lệnh chờ + "
      f"mở trên rổ, mỗi tài sản 1, ký quỹ (KL × giá ÷ min(40%/SL%, 20); giảm nửa sau TP1) ≤ 50% số dư — lệnh vi phạm bị bỏ (cột "
      f"cuối). Lệnh còn mở lúc hết kỳ đóng ở close cuối kỳ (`ket_thuc` = cuối kỳ). Hạt giống lần i = `{HAT_GIONG} + i` kèm tên bộ "
      f"và kiểu (`random.Random(\"<{HAT_GIONG}+i>|<năm>_<rổ>|<A/B>\")`) → tái lập được, không phụ thuộc số tiến trình (mọi bộ chạy "
      f"song song trong 1 Pool). **Phân vị = % số lần giả dược có kết quả THẤP HƠN thật** (≥ 95 mới đáng chú ý; ≈ 50 = không hơn ngẫu nhiên). "
      f"Quy tắc vốn bỏ bớt lệnh giả dược (trùng giờ) nên số lệnh giả dược khớp ít hơn thật → tổng $ / tổng R so lệch về phía giả dược "
      f"khi kỳ vọng mỗi lệnh âm; **R TB mỗi lệnh** không phụ thuộc số lệnh nên là thước chính.")
    W("")
    if HC:
        W("### 4b. Hiệu chỉnh: hai kiểu giả dược trên dữ liệu KHÔNG có quy luật")
        W("")
        W(f"Cùng động cơ (`dong_co.chay`, không sửa gì) chạy trên nến giả lập bước ngẫu nhiên (log-giá, 16 bước/nến H4, O/H/L/C lấy "
          f"từ đường đi; hạt giống `{HAT_GIONG_HC}`; tạo trong thư mục tạm, không ghi đâu cả). Trên dữ liệu như vậy không chiến lược nào "
          "có lợi thế thật → giả dược CÔNG BẰNG phải cho phân vị rải quanh 50; phân vị dồn về 0 nghĩa là giả dược đó thiên lệch có lợi "
          "cho chính nó (làm bot trông tệ hơn thực chất).")
        W("")
        W("| Năm · rổ (dữ liệu giả lập) | Lệnh | R TB bot | Phân vị A ($ / tổng R / R TB) | Phân vị B ($ / tổng R / R TB) |")
        W("|---|---|---|---|---|")
        for (nam, ro), h in HC.items():
            t = h["tk"]
            W(f"| {nam} · {TEN_RO[ro]} | {t['n']} | {phay(t['R_tb'], 2, True)} | {pv_s(h.get('gd', {}).get('A'), t)} | "
              f"{pv_s(h.get('gd', {}).get('B'), t)} |")
        W("")
        o = []
        for kieu in KIEU_GD:
            ds = [pv_that(h.get("gd", {}).get(kieu), h["tk"]) for h in HC.values() if h.get("gd", {}).get(kieu)]
            if ds:
                o.append(f"{kieu}: $ {phay(statistics.mean(x[0] for x in ds), 0)} · tổng R {phay(statistics.mean(x[1] for x in ds), 0)} · "
                         f"R TB {phay(statistics.mean(x[2] for x in ds if x[2] is not None), 0)}")
        W("_Phân vị trung bình 6 bộ trên dữ liệu không quy luật — " + " — ".join(o)
          + " (công bằng ≈ 50; chỉ 6 bộ nên nhiễu ±10). Đọc phân vị thật theo kiểu/thước được hiệu chỉnh gần 50 nhất._")
        W("")

    # 5. theo tai san
    W("## 5. Theo tài sản")
    W("")
    W("Số lệnh khớp theo tài sản theo năm (rổ 6):")
    W("")
    W("| Tài sản | " + " | ".join(str(n) for n in a.nam) + " |")
    W("|---|" + "---|" * len(a.nam))
    for ts in TAI_SAN_6:
        o = []
        for nam in a.nam:
            k = KQ.get((nam, "6"))
            o.append(str(sum(1 for x in k["lenh"] if da_khop(x) and x["tai_san"] == ts)) if k else "—")
        W(f"| {ts} | " + " | ".join(o) + " |")
    W("")
    for nam in a.nam:
        k = KQ.get((nam, "6"))
        if not k:
            continue
        W(f"**{nam} · rổ 6**")
        W("")
        W("| Tài sản | Lệnh (L/S) | % thắng | R TB | Tổng R | Lãi$ | Hệ số LN |")
        W("|---|---|---|---|---|---|---|")
        for ts in TAI_SAN_6:
            t = thong_ke([x for x in k["lenh"] if x["tai_san"] == ts])
            W(f"| {ts} | {t['n']} ({t['long']}/{t['short']}) | {pt(t['thang'], 0, False)} | {phay(t['R_tb'], 2, True)} | "
              f"{phay(t['tong_R'], 1, True)} | {usd(t['lai'])} | {pf_s(t['pf'])} |")
        W("")
    W("_Vốn dùng chung (rủi ro % vốn lúc đặt) nên $ theo tài sản phụ thuộc thứ tự lệnh; so bằng tổng R chắc hơn._")
    W("")

    # 6. chinh vs hoi
    W("## 6. Lệnh chính (thuận pha) vs lệnh hồi (ngược pha)")
    W("")
    W("| Năm · rổ | Loại | Lệnh (L/S) | % thắng | R TB | t | Tổng R | Lãi$ | Hệ số LN |")
    W("|---|---|---|---|---|---|---|---|---|")
    for (nam, ro), k in KQ.items():
        for loai in ("chinh", "hoi"):
            t = thong_ke([x for x in k["lenh"] if x["loai"] == loai])
            W(f"| {nam} · {TEN_RO[ro]} | {'chính' if loai == 'chinh' else 'hồi'} | {t['n']} ({t['long']}/{t['short']}) | "
              f"{pt(t['thang'], 0, False)} | {phay(t['R_tb'], 2, True)} | {phay(t['t'], 1, True)} | {phay(t['tong_R'], 1, True)} | "
              f"{usd(t['lai'])} | {pf_s(t['pf'])} |")
    W("")

    # 7. ly do ra
    W("## 7. Theo lý do ra lệnh")
    W("")
    W("| Năm · rổ | " + " | ".join(LY_DO) + " |")
    W("|---|" + "---|" * len(LY_DO))
    for (nam, ro), k in KQ.items():
        o = []
        for ly in LY_DO:
            ds = [x for x in k["lenh"] if x["ly_do_ra"] == ly]
            if ly in ("HUY",) + CON_MO:
                o.append(str(len(ds)))
            else:
                o.append(f"{len(ds)} · {usd(sum(x['lai_usd'] for x in ds))} · R {phay(sum(x['R'] or 0 for x in ds), 1, True)}"
                         if ds else "0")
        W(f"| {nam} · {TEN_RO[ro]} | " + " | ".join(o) + " |")
    la = Counter(x["ly_do_ra"] for k in KQ.values() for x in k["lenh"]) - Counter({x: 10 ** 9 for x in LY_DO})
    W("")
    W("_Ô = số lệnh · tổng lãi$ · tổng R. TP2 = phần còn lại ra ở TP2 (đã chốt 50% ở TP1 nếu có); TP = TP duy nhất (lệnh hồi); "
      "SL_HOA_VON = sau TP1 dời SL về giá vào; HET_GIO = dừng theo giờ; HET_KY = đóng ở close cuối kỳ; HUY = lệnh chờ không khớp._"
      + (f" Lý do lạ: {dict(la)}." if la else ""))
    W("")

    # 8. do giong
    W("## 8. Độ giống hướng H4 với người đó")
    W("")
    W("> ## ⚠️ TRONG MẪU — luật v4 rút từ chính các buổi live 2026 này. Số dưới đây KHÔNG phải bằng chứng dự đoán; "
      "kết luận thật chỉ có ở buổi live mới từ 02/11/2026.")
    W("")
    W(f"Mốc C = `bat_dau_vn + phut` (giờ VN → UTC) trong `transcripts/gio_live.tsv` ({dg_tong} buổi; {len(dg)} buổi có phiếu"
      + (f"; thiếu phiếu: {', '.join(dg_thieu)}" if dg_thieu else "") + "). View bot = `dong_co.view_tai(\"BTC\", C)`. "
      "Nhãn người đó = view khung H4 (không có thì \"chung\") trong phiếu: buổi từ 2026-07-01 → `thi/dap_an_v2/phieu/`, "
      "trước đó → `phieu/` (khớp theo video id). Luật từ trên xuống: định nghĩa trong docstring `thi/cham.py`, tính lại trên "
      "`bot_v4/du_lieu/BTC_*.csv` chỉ với nến đã đóng ≤ C. Mọi cách đoán chấm trên CÙNG tập buổi.")
    W("")
    W(f"Kiểm rò rỉ: `gio_cat` do `view_tai` trả về > C ở **{dg_ro_ri}** buổi" + (" (phải = 0 — **LỖI**)." if dg_ro_ri else " (đạt)."))
    W("")
    for ten_nhom, loc in (("Cả 180 buổi (T1–T10)", lambda r: True), ("T1–T6 (trước 2026-07-01, nhãn `phieu/`)", lambda r: r["ngay"] < "2026-07-01"),
                          ("T7–T10 (từ 2026-07-01, nhãn `thi/dap_an_v2/phieu/`)", lambda r: r["ngay"] >= "2026-07-01")):
        W(f"### {ten_nhom}")
        W("")
        L.extend(bang_do_giong([r for r in dg if loc(r)], ten_nhom))
        W("")
    pha = Counter((r["pha"], r["bot"]) for r in dg)
    W("_Phân bố (pha W1 → view bot) trên các buổi: " + ", ".join(f"{VIET[p]}→{VIET[v]}: {n}" for (p, v), n in sorted(
        pha.items(), key=lambda x: (str(x[0][0]), str(x[0][1])))) + "._")
    W("")
    W("<details><summary>Từng buổi</summary>")
    W("")
    W("| Buổi | C (VN) | gio_cat (VN) | Người đó | Bot (pha) | Trùng | Luật từ trên xuống | Nguồn nhãn |")
    W("|---|---|---|---|---|---|---|---|")
    for r in dg:
        W(f"| {r['ten']} | {r['C'].astimezone(VN):%m-%d %H:%M} | {r['gio_cat'].astimezone(VN):%m-%d %H:%M} | "
          f"{VIET[r['nguoi']]} | {VIET[r['bot']]} ({VIET[r['pha']]}) | {'✓' if r['nguoi'] and r['nguoi'] == r['bot'] else '✗'} | "
          f"{VIET[r['luat']]} | `{r['nguon']}` |" if r["gio_cat"] else
          f"| {r['ten']} | {r['C'].astimezone(VN):%m-%d %H:%M} | — | {VIET[r['nguoi']]} | {VIET[r['bot']]} | "
          f"{'✓' if r['nguoi'] and r['nguoi'] == r['bot'] else '✗'} | {VIET[r['luat']]} | `{r['nguon']}` |")
    W("")
    W("</details>")
    W("")
    if ghi_chu:
        W("## Ghi chú chạy")
        W("")
        for x in ghi_chu:
            W(f"- {x}")
        W("")
    ra_file.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✓ {ra_file} ({tong_loi} lỗi tự cộng lại, {time.time() - bat_dau:.0f}s)")
    for (nam, ro), k in KQ.items():
        t = k["tk"]
        print(f"  {nam} {ro:>3}: {usd(t['lai']):>8} {t['n']:>4} lệnh  R TB {phay(t['R_tb'], 2, True)}  DD {pt(t['dd'], 1, False)}  "
              f"giả dược $/R A {pv_s(k['gd'].get('A'), t)} B {pv_s(k['gd'].get('B'), t)}  kiểm {'KHỚP' if not k['kiem']['loi'] else 'LỖI'}")
    for (nam, ro), h in HC.items():
        print(f"  hiệu chỉnh {nam} {ro:>3} (ngẫu nhiên): R TB {phay(h['tk']['R_tb'], 2, True)}  A {pv_s(h.get('gd', {}).get('A'), h['tk'])}  "
              f"B {pv_s(h.get('gd', {}).get('B'), h['tk'])}")
    so_ = [r for r in dg if r["nguoi"] in NHAN]
    if so_:
        print(f"  độ giống: bot {sum(r['bot'] == r['nguoi'] for r in so_)}/{len(so_)} · luôn GIẢM "
              f"{sum(r['giam'] == r['nguoi'] for r in so_)} · luật {sum(r['luat'] == r['nguoi'] for r in so_)}")


if __name__ == "__main__":
    main()
