#!/usr/bin/env python3
"""GIU / LAT view H4 — dac trung cho moi buoi N (toan bo 180 buoi; tap HOC = truoc 2026-07-01, tap KIEM = tu 2026-07-01).

Nhan: hoc_v5/nhan/<buoi>.json (nhan moi), thieu thi thi/dap_an_v2/nhan/<buoi>.json (user cho phep doc tu 31/10 ~11:55);
che do `cu` = phieu/<buoi>.json. KHONG doc thi/bai_lam/, thi/KET_QUA_THI.md, kiem_cheo/codex_phieu/.
Luat chi duoc CHON tren tap hoc (phan_tich.py); tap kiem chi de do lai (kiem theo thoi gian).

Moc C cua buoi = bat_dau_vn + phut (transcripts/gio_live.tsv). Dac trung buoi N chi dung:
  - nen DA DONG <= C_N (H4/D1: bot_v4/du_lieu/BTC_4H.csv, BTC_1D.csv, gio MO nen UTC; 5m: du_lieu/btc_5m.csv dung cho
    gia tai C va cham bang RAU trong cua so (C_{N-1}, C_N]; khung nho M15/M30/H1 cua moc vo hieu gop tu 5m),
  - nhan cac buoi TRUOC N (view N-1, dich/vo hieu N-1 ...), lich tin (du_lieu/tin_tuc/, neu co) chi tin da biet truoc.
  Cot `nhan`, `nhan_dau` = view cuoi / dau buoi N = DICH de hoc, KHONG phai dac trung.

"view" = huong TANG/GIAM gan nhat cua nguoi do truoc N (bo qua buoi PHAN VAN) = moc "Giu view" cua thi/cham.py.
Moi dac trung "nguoc"/"thuan" tinh theo view nay.

Cach dung: python3 hoc_v5/giu_lat/dac_trung.py [--nhan moi|cu|tu_dong] [--pham-vi tat_ca|hoc]
  -> hoc_v5/giu_lat/dac_trung_<nguon>.csv  + nhan_<nguon>.json (nhan da chuan hoa, cho phan_tich.py)
"""
import bisect, csv, datetime as dt, json, math, re, sys, unicodedata
from collections import namedtuple
from pathlib import Path

RA = Path(__file__).resolve().parent
GOC = RA.parents[1]
sys.path.insert(0, str(GOC / "cong_cu"))
import dieu_kien  # noqa: E402  (chi dung phan_tich() de doc cau vo hieu cua nhan cu)

TU_THI = "2026-07-01"
V2_DUOC_DUNG = {"2026-03-06_4Z73-L_oWNY", "2026-05-19_sWk33q2YCj4", "2026-06-22_eaj9NEm85O4"}
MAU_TEN = re.compile(r"^(\d{4}-\d{2}-\d{2})_(?:(\d{4})_)?(.{11})$")
VN = dt.timedelta(hours=7)
GIO4, NGAY, PHUT5 = dt.timedelta(hours=4), dt.timedelta(days=1), dt.timedelta(minutes=5)
KHUNG_PHUT = {"M5": 5, "M15": 15, "M30": 30, "H1": 60}
TL_CSV = GOC / "hoc_v5" / "trendline" / "su_kien.csv"

Nen = namedtuple("Nen", "mo dong o h l c v")
Buoi = namedtuple("Buoi", "ten ngay vid bat_dau C")


# ───────────────────────── buoi + nhan ─────────────────────────
def ds_buoi(pham_vi="tat_ca"):
    """Buoi live (ten lay tu phieu/; pham_vi='hoc' -> chi ngay < TU_THI), sap theo gio bat dau that."""
    gio = {r["id"]: r for r in csv.DictReader((GOC / "transcripts" / "gio_live.tsv").open(encoding="utf-8"), delimiter="\t")}
    ra = []
    for p in (GOC / "phieu").glob("2*.json"):
        m = MAU_TEN.match(p.stem)
        if not m or (pham_vi == "hoc" and m[1] >= TU_THI):
            continue
        r = gio[m[3]]
        bd = dt.datetime.strptime(r["bat_dau_vn"].strip(), "%Y-%m-%d %H:%M") - VN  # UTC, khong mui
        ra.append(Buoi(p.stem, m[1], m[3], bd, bd + dt.timedelta(minutes=int(r["phut"]))))
    ra.sort(key=lambda b: (b.bat_dau, b.ten))
    return ra


def chuan_huong(x):
    if x is None:
        return None
    s = khong_dau(str(x)).upper().strip().replace(" ", "_")
    if s in ("TANG", "LONG", "UP"):
        return "TANG"
    if s in ("GIAM", "SHORT", "DOWN"):
        return "GIAM"
    if s.replace("_", "") in ("PHANVAN", "PV", "DUNGNGOAI", "TRUNGLAP", "SIDEWAY"):
        return "PHAN_VAN"
    return None


def khong_dau(s):
    s = (s or "").replace("đ", "d").replace("Đ", "D")
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()


def so_list(x):
    """dich: so | [a, b] | {"tu","den"} | None -> list so (>= 10.000 de bo so khong phai gia BTC)."""
    if x is None:
        return []
    if isinstance(x, (int, float)):
        return [float(x)] if 10_000 <= x <= 300_000 else []
    if isinstance(x, dict):
        return so_list([x.get("tu"), x.get("den")]) or so_list(x.get("gia")) or so_list(x.get("dich"))
    if isinstance(x, (list, tuple)):
        ra = []
        for y in x:
            ra += so_list(y)
        return ra
    return []


def doc_nhan_moi(ten):
    p = GOC / "hoc_v5" / "nhan" / f"{ten}.json"
    if not p.exists():
        p = GOC / "thi" / "dap_an_v2" / "nhan" / f"{ten}.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    cb, db = d.get("cuoi_buoi") or {}, d.get("dau_buoi") or {}
    huong = chuan_huong(cb.get("thien_huong_h4"))
    dich = so_list(d.get("dich_chinh"))
    if not dich:  # chang cuoi cua duong_di
        for leg in reversed(d.get("duong_di") or []):
            if so_list(leg.get("dich")):
                dich = so_list(leg.get("dich")); break
    vh = d.get("vo_hieu")
    if isinstance(vh, dict) and so_list(vh.get("gia")):
        chieu = vh.get("chieu") or ("dong_duoi" if huong == "TANG" else "dong_tren")
        vh = {"gia": so_list(vh.get("gia"))[0], "khung": str(vh.get("khung") or "H4").upper(),
              "so_nen": int(vh.get("so_nen") or 1), "chieu": chieu, "cau": vh.get("cau")}
    else:
        vh = None
    ck = d.get("chang_ke_tiep") or {}
    return {"ten": ten, "nguon": str(p.relative_to(GOC)), "huong": huong, "huong_dau": chuan_huong(db.get("thien_huong_h4")),
            "do_chac": cb.get("do_chac"), "gio_cuoi": cb.get("gio"), "trich_cuoi": cb.get("trich"),
            "gio_dau": db.get("gio"), "trich_dau": db.get("trich"),
            "doi_y_giua_buoi": bool(d.get("doi_y_giua_buoi")), "ly_do_doi_y": d.get("ly_do_doi_y"),
            "dich": dich, "chang1": {"huong": chuan_huong(ck.get("huong")), "dich": so_list(ck.get("dich"))} if ck else None,
            "vo_hieu": vh, "gia_noi": d.get("gia_btc_luc_noi"), "hanh_dong": d.get("hanh_dong"),
            "nhin_lai": d.get("nhin_lai_view_truoc"), "trendline": d.get("trendline"),
            "nen_volume": d.get("nen_volume"), "vung_nguoi_do": d.get("vung_nguoi_do"),
            "view_trung_han": d.get("view_trung_han"), "vung_tranh": d.get("vung_tranh"), "giu_dong": d.get("giu_dong"),
            "khung_lon": d.get("khung_lon"), "lenh": d.get("lenh"), "trich_them": d.get("trich_them"),
            "tin_tuc": d.get("tin_tuc")}


def doc_nhan_cu(ten):
    d = json.loads((GOC / "phieu" / f"{ten}.json").read_text(encoding="utf-8"))
    nd = d.get("nhan_dinh") or []
    h = next((x for x in nd if x.get("khung") == "H4"), None) or next((x for x in nd if x.get("khung") == "chung"), None)
    huong = chuan_huong(h.get("huong")) if h else None
    gia_noi = d.get("gia_btc_luc_noi")
    vh = None
    if h and huong in ("TANG", "GIAM"):
        k = dieu_kien.phan_tich(h.get("vo_hieu_khi"), huong, gia_noi)
        if k and k.get("da_hieu"):
            vh = {"gia": k["gia"], "khung": k["khung"] or "H4", "so_nen": k["so_nen"], "chieu": k["chieu"],
                  "cau": h.get("vo_hieu_khi")}
    return {"ten": ten, "nguon": f"phieu/{ten}.json", "huong": huong, "huong_dau": None,
            "do_chac": h.get("do_chac") if h else None, "doi_y_giua_buoi": bool(h and h.get("doi_y")),
            "ly_do_doi_y": h.get("doi_y") if h else None, "dich": so_list(h.get("dich")) if h else [],
            "chang1": None, "vo_hieu": vh, "gia_noi": gia_noi, "hanh_dong": None,
            "nhin_lai": {"vi_sao": d.get("nhin_lai_truoc"), "giu_hay_doi": None} if d.get("nhin_lai_truoc") else None,
            "trendline": None, "nen_volume": None, "vung_nguoi_do": None, "view_trung_han": None,
            "vung_tranh": None, "giu_dong": None, "khung_lon": None, "lenh": d.get("lenh"), "trich_them": None,
            "trich_cuoi": h.get("trich") if h else None, "gio_cuoi": None, "tin_tuc": d.get("tin_tuc")}


# ───────────────────────── nen + chi bao ─────────────────────────
def doc_nen(p, do_dai):
    ra = []
    with open(p, newline="") as f:
        for r in csv.DictReader(f):
            mo = dt.datetime.strptime(r["ts_utc"], "%Y-%m-%d %H:%M")
            ra.append(Nen(mo, mo + do_dai, float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"]),
                          float(r.get("vol") or 0)))
    ra.sort()
    return ra


def gop(nens, khoa, do_dai_fn, du=None):
    """Gop nen nho thanh nen lon theo khoa(mo) -> gio mo nen lon. du = so nen nho toi thieu (None = khong kiem)."""
    nhom = {}
    for n in nens:
        nhom.setdefault(khoa(n.mo), []).append(n)
    ra = []
    for bd in sorted(nhom):
        ds = nhom[bd]
        if du is not None and len(ds) < du:
            continue
        ra.append(Nen(bd, bd + do_dai_fn(bd), ds[0].o, max(x.h for x in ds), min(x.l for x in ds), ds[-1].c,
                      sum(x.v for x in ds)))
    return ra


def ema(xs, n):
    ra = [None] * len(xs)
    if len(xs) < n:
        return ra
    a, v = 2.0 / (n + 1), sum(xs[:n]) / n
    ra[n - 1] = v
    for i in range(n, len(xs)):
        v = a * xs[i] + (1 - a) * v
        ra[i] = v
    return ra


def rsi(c, n=14):
    ra = [None] * len(c)
    if len(c) < n + 1:
        return ra
    lai = [0.0] + [max(c[i] - c[i - 1], 0.0) for i in range(1, len(c))]
    lo = [0.0] + [max(c[i - 1] - c[i], 0.0) for i in range(1, len(c))]
    gl, gs = sum(lai[1:n + 1]) / n, sum(lo[1:n + 1]) / n
    f = lambda a, b: 100.0 if b == 0 else 100 - 100 / (1 + a / b)  # noqa: E731
    ra[n] = f(gl, gs)
    for i in range(n + 1, len(c)):
        gl, gs = (gl * (n - 1) + lai[i]) / n, (gs * (n - 1) + lo[i]) / n
        ra[i] = f(gl, gs)
    return ra


def atr(ns, n=14):
    tr = [ns[0].h - ns[0].l] + [max(x.h - x.l, abs(x.h - p.c), abs(x.l - p.c)) for p, x in zip(ns, ns[1:])]
    ra = [None] * len(tr)
    if len(tr) < n:
        return ra
    v = sum(tr[:n]) / n
    ra[n - 1] = v
    for i in range(n, len(tr)):
        v = (v * (n - 1) + tr[i]) / n
        ra[i] = v
    return ra


def tb_vol(ns, n=20):
    """TB volume 20 nen TRUOC nen i (khong gom i)."""
    v = [x.v for x in ns]
    return [None if i < n else sum(v[i - n:i]) / n for i in range(len(v))]


def tinh_pha(c, e34, e89):
    """bot_v4/THIET_KE.md muc 3 (= bot_v4/dong_co.tinh_pha): dieu kien TANG: close>EMA34 va EMA34>EMA89, GIAM nguoc lai;
    doi pha chi khi 2 nen W1 lien tiep thoa dieu kien pha nguoc; truoc khi khoa = close so EMA34."""
    pha, hien, khoa, dem = [None] * len(c), None, False, 0
    for j in range(len(c)):
        if e34[j] is None:
            continue
        dk = None
        if e89[j] is not None:
            if c[j] > e34[j] > e89[j]:
                dk = "TANG"
            elif c[j] < e34[j] < e89[j]:
                dk = "GIAM"
        if not khoa:
            if dk:
                hien, khoa, dem = dk, True, 0
            else:
                hien = "TANG" if c[j] > e34[j] else "GIAM"
        elif dk and dk != hien:
            dem += 1
            if dem >= 2:
                hien, dem = dk, 0
        else:
            dem = 0
        pha[j] = hien
    return pha


class Khung:
    def __init__(self, ns):
        self.n = ns
        self.dong = [x.dong for x in ns]
        c = [x.c for x in ns]
        self.e34c, self.e34h, self.e34l = ema(c, 34), ema([x.h for x in ns], 34), ema([x.l for x in ns], 34)
        self.e89, self.e200 = ema(c, 89), ema(c, 200)
        self.rsi, self.atr, self.tbv = rsi(c), atr(ns), tb_vol(ns)

    def cuoi(self, C):
        """chi so nen cuoi DA DONG <= C."""
        return bisect.bisect_right(self.dong, C) - 1

    def trong(self, tu, den):
        """chi so cac nen co tu < gio dong <= den."""
        return range(bisect.bisect_right(self.dong, tu), bisect.bisect_right(self.dong, den))


class DuLieu:
    def __init__(self):
        self.h4 = Khung(doc_nen(GOC / "bot_v4" / "du_lieu" / "BTC_4H.csv", GIO4))
        self.d1 = Khung(doc_nen(GOC / "bot_v4" / "du_lieu" / "BTC_1D.csv", NGAY))
        w = gop(self.d1.n, lambda m: (m - dt.timedelta(days=m.weekday())).replace(hour=0, minute=0),
                lambda bd: dt.timedelta(days=7), du=7)
        self.w1 = Khung(w)
        self.w1.pha = tinh_pha([x.c for x in w], self.w1.e34c, ema([x.c for x in w], 89))
        self.m5 = doc_nen(GOC / "du_lieu" / "btc_5m.csv", PHUT5)
        self.m5_dong = [x.dong for x in self.m5]
        self.nho = {}

    def khung_nho(self, ten):
        if ten not in self.nho:
            p = KHUNG_PHUT[ten]
            ns = self.m5 if p == 5 else gop(self.m5, lambda m: m.replace(minute=m.minute // p * p) if p < 60
                                               else m.replace(minute=0), lambda bd: dt.timedelta(minutes=p), du=p // 5)
            self.nho[ten] = Khung(ns)
        return self.nho[ten]

    def gia_luc(self, C):
        i = bisect.bisect_right(self.m5_dong, C) - 1
        if i >= 0 and C - self.m5[i].dong < dt.timedelta(hours=1):
            return self.m5[i].c
        return self.h4.n[self.h4.cuoi(C)].c

    def cuc_tri(self, tu, den):
        """(max high, min low) cua nen 5m nam tron trong (tu, den]; khong co 5m -> dung H4."""
        i0 = bisect.bisect_left(self.m5_dong, tu + PHUT5)
        i1 = bisect.bisect_right(self.m5_dong, den)
        if i1 > i0:
            ds = self.m5[i0:i1]
        else:
            ds = [self.h4.n[i] for i in self.h4.trong(tu, den)]
        if not ds:
            return None, None
        return max(x.h for x in ds), min(x.l for x in ds)


# ───────────────────────── tung loai dac trung ─────────────────────────
DAU = {"TANG": 1, "GIAM": -1}


def qua(chieu, gia, c):
    return c > gia if chieu == "dong_tren" else c < gia


def dong_qua(k, idx, chieu, gia, so_nen):
    """Lan dau co so_nen nen lien tiep (trong idx) dong qua moc -> chi so nen do, khong co -> None."""
    chuoi, truoc = 0, None
    for i in idx:
        if qua(chieu, gia, k.n[i].c):
            chuoi = chuoi + 1 if (chuoi and truoc == i - 1) else 1
            if chuoi >= so_nen:
                return i
        else:
            chuoi = 0
        truoc = i
    return None


def cham_vung(vung, gia_tu, hi, lo):
    """Dich (list so) duoc RAU cham trong cua so? Huong dich = phia cua dich so voi gia_tu. Gia dang trong vung -> None."""
    if not vung or hi is None:
        return None
    a, b = min(vung), max(vung)
    if a > gia_tu:
        return hi >= a
    if b < gia_tu:
        return lo <= b
    return None


def nhan_chim(k, i):
    """+1 nhan chim tang, -1 nhan chim giam (than nen i bao than nen i-1 nguoc mau), 0 khong."""
    if i < 1:
        return 0
    a, b = k.n[i - 1], k.n[i]
    if b.c < b.o and a.c > a.o and b.o >= a.c and b.c <= a.o:
        return -1
    if b.c > b.o and a.c < a.o and b.o <= a.c and b.c >= a.o:
        return 1
    return 0


def vi_tri_dai(k, i):
    x = k.n[i].c
    if k.e34h[i] is None:
        return None
    return 1 if x > k.e34h[i] else (-1 if x < k.e34l[i] else 0)


def tren(k, i, e):
    v = getattr(k, e)[i]
    return None if v is None else (1 if k.n[i].c > v else -1)


def luat_tren_xuong(du, C):
    """Moc 'Luat tu tren xuong' cua thi/cham.py: EMA H4 34/89/200 chum < 0,6% -> PHAN_VAN; khong thi TANG khi dong D1
    <= EMA89 D1 x 1,01 va nhip 24h > -1%; con lai GIAM. Gia = close H4 cuoi da dong; 24h = close H4 dong luc T-24h."""
    h, d = du.h4, du.d1
    i, j = h.cuoi(C), d.cuoi(C)
    gia = h.n[i].c
    e = [h.e34c[i], h.e89[i], h.e200[i]]
    T = h.n[i].dong
    k24 = bisect.bisect_right(h.dong, T - dt.timedelta(hours=24)) - 1
    p24 = h.n[k24].c if h.n[k24].dong == T - dt.timedelta(hours=24) else gia
    if (max(e) - min(e)) / gia * 100 < 0.6:
        return "PHAN_VAN"
    if d.n[j].c <= d.e89[j] * 1.01 and (gia / p24 - 1) * 100 > -1:
        return "TANG"
    return "GIAM"


def doc_trendline():
    """hoc_v5/trendline/su_kien.csv (agent khac lam; bien the da khoa) -> {video id: [dong csv]}; chua co -> None.
    Moi buoi 4 dong (khung H4/D1 x loai khang_cu_giam/ho_tro_tang); khoang = (C buoi truoc, C]."""
    if not TL_CSV.exists():
        return None
    ra = {}
    with TL_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ra.setdefault((r.get("buoi") or "")[-11:], []).append(r)
    return ra


def dac_trung_tl(ev, s):
    """Dac trung trendline theo view s (+1 TANG / -1 GIAM). Pha NGUOC view = view TANG ma ho tro tang bi pha (xuong),
    view GIAM ma khang cu giam bi pha (len). Pha gia (da biet tai C) khong tinh la pha."""
    r = {"tl_co_du_lieu": int(bool(ev))}
    if not ev or not s:
        return r
    for kh in ("H4", "D1", ""):
        ng = [e for e in ev if (not kh or e.get("khung") == kh) and e.get("chinh_truoc_pha") == "1"
              and e.get("pha_ket_qua") != "pha_gia"
              and ((s > 0 and e.get("loai") == "ho_tro_tang") or (s < 0 and e.get("loai") == "khang_cu_giam"))]
        th = [e for e in ev if (not kh or e.get("khung") == kh) and e.get("chinh_truoc_pha") == "1"
              and e.get("pha_ket_qua") != "pha_gia"
              and ((s > 0 and e.get("loai") == "khang_cu_giam") or (s < 0 and e.get("loai") == "ho_tro_tang"))]
        hau = f"_{kh.lower()}" if kh else ""
        r[f"tl_pha_nguoc{hau}"] = int(bool(ng))
        r[f"tl_pha_thuan{hau}"] = int(bool(th))
        if not kh:
            r["tl_pha_nguoc_2nen"] = int(any(e.get("pha_2nen") == "1" for e in ng))
            v = [float(e["pha_vol"]) for e in ng if e.get("pha_vol")]
            r["tl_pha_nguoc_vol"] = max(v) if v else None
    return r


TIN_LON = {"FOMC", "CPI", "NFP"}
TIN_DIR = GOC / "du_lieu" / "tin_tuc"


def doc_lich_tin():
    """du_lieu/tin_tuc/lich_kinh_te_2026.csv (agent khac dung) -> [(gio UTC, su_kien)] sap theo gio; chua co -> None.
    Lich cong bo truoc nen biet truoc C (dung duoc ca 'sap co tin')."""
    p = TIN_DIR / "lich_kinh_te_2026.csv"
    if not p.exists():
        return None
    ra = []
    with p.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                t = dt.datetime.strptime(r["ngay_gio_vn"].strip(), "%Y-%m-%d %H:%M") - VN
            except (KeyError, ValueError):
                continue
            ra.append((t, (r.get("su_kien") or "").strip(), (r.get("ghi_chu") or "") + " " + (r.get("ky") or "")))
    ra.sort()
    return ra


def doc_polymarket(lich):
    """du_lieu/tin_tuc/polymarket_fed.csv -> {gio quyet dinh FOMC UTC: [(gio, P_tang, P_giam)]} (moc gio, chuan hoa tong
    cac ket qua = 1); chua co -> None. Thi truong 'Fed decision in <thang>'; ket qua increase / decrease / No change."""
    p = TIN_DIR / "polymarket_fed.csv"
    if not p.exists() or not lich:
        return None
    hop = {t.strftime("%Y-%m"): t for t, sk, _ in lich if sk == "FOMC"}
    tam = {}
    with p.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ky = r["ky_hop"]
            if ky not in hop:
                continue
            ts = dt.datetime.strptime(r["ts_utc"][:13], "%Y-%m-%dT%H")
            tam.setdefault(hop[ky], {}).setdefault(ts, {})[r["ket_qua"]] = float(r["xac_suat"])
    ra = {}
    for gio_hop, d in tam.items():
        ds = []
        for ts in sorted(d):
            v = d[ts]
            tong = sum(v.values())
            if len(v) < 3 or tong <= 0:
                continue
            ds.append((ts, sum(x for k, x in v.items() if "increase" in k) / tong,
                       sum(x for k, x in v.items() if "decrease" in k) / tong))
        ra[gio_hop] = ds
    return ra


def pm_luc(pm, t, gio_hop=None):
    """(gio hop FOMC ke tiep sau t (hoac gio_hop chi dinh), P_tang, P_giam) moi nhat <= t trong 12h; khong co -> None."""
    if not pm:
        return None, None, None
    if gio_hop is None:
        sau = sorted(g for g in pm if g > t)
        if not sau:
            return None, None, None
        gio_hop = sau[0]
    ds = pm.get(gio_hop) or []
    i = bisect.bisect_right([x[0] for x in ds], t) - 1
    if i < 0 or t - ds[i][0] > dt.timedelta(hours=12):
        return gio_hop, None, None
    return gio_hop, ds[i][1], ds[i][2]


def doc_fomc_ket_qua():
    """du_lieu/tin_tuc/fomc_ket_qua_2026.csv -> [(gio quyet dinh UTC ~18:00, quyet_dinh, so phan doi muon TANG, ... muon GIAM)]."""
    p = TIN_DIR / "fomc_ket_qua_2026.csv"
    if not p.exists():
        return None
    ra = []
    with p.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = dt.datetime.strptime(r["ngay_quyet_dinh"], "%Y-%m-%d") + dt.timedelta(hours=18)  # 14:00 ET ~ 18:00/19:00 UTC
            tang = giam = 0
            for doan in re.split(r";", r.get("phan_doi") or ""):
                ten = doan.split("who")[0]
                n = len(re.findall(r"[A-Z][a-z]+ (?:[A-Z]\. )?[A-Z][a-z]+", ten))
                if "raise" in doan:
                    tang += n
                elif "lower" in doan:
                    giam += n
            ra.append((t, r["quyet_dinh"], tang, giam))
    return sorted(ra)


def dac_trung_buoi(du, b, truoc, nhan, view, tl, lich=None, pm=None, fkq=None):
    """1 dong dac trung cho buoi b. truoc = Buoi N-1 (hoac None). nhan = {ten: nhan chuan hoa}. view = TANG/GIAM/None."""
    r = {"ten": b.ten, "ngay": b.ngay, "thang": b.ngay[:7], "tap": "hoc" if b.ngay < TU_THI else "kiem",
         "C_vn": (b.C + VN).strftime("%Y-%m-%d %H:%M"), "thu_vn": (b.bat_dau + VN).weekday()}
    nb = nhan.get(b.ten) or {}
    r["nguon_nhan"] = (nb.get("nguon") or "").split("/")[0] + ("/dap_an_v2" if "dap_an_v2" in (nb.get("nguon") or "") else "")
    r["nhan"], r["nhan_dau"] = nb.get("huong"), nb.get("huong_dau")
    r["view"] = view
    h, d = du.h4, du.d1
    i4, i1 = h.cuoi(b.C), d.cuoi(b.C)
    gia = du.gia_luc(b.C)
    r["gia_C"] = round(gia, 1)
    # --- vi tri EMA / RSI tai C (nen da dong)
    for ten, k, i in (("h4", h, i4), ("d1", d, i1)):
        r[f"{ten}_vs_dai34"] = vi_tri_dai(k, i)
        r[f"{ten}_vs_e89"] = tren(k, i, "e89")
        r[f"{ten}_vs_e200"] = tren(k, i, "e200")
        r[f"rsi_{ten}"] = round(k.rsi[i], 1) if k.rsi[i] is not None else None
    r["kc_e89_d1_pct"] = round((d.n[i1].c / d.e89[i1] - 1) * 100, 2)
    e = [h.e34c[i4], h.e89[i4], h.e200[i4]]
    r["chum_h4_pct"] = round((max(e) - min(e)) / h.n[i4].c * 100, 2)
    iw = du.w1.cuoi(b.C)
    r["pha_w1"] = du.w1.pha[iw] if iw >= 0 else None
    r["d1_cuoi_mau"] = 1 if d.n[i1].c > d.n[i1].o else -1
    r["d1_cuoi_nhan_chim"] = nhan_chim(d, i1)
    r["luat_tren_xuong"] = luat_tren_xuong(du, b.C)
    r["thu_hai"] = int(r["thu_vn"] == 0)
    if lich is not None:
        fomc = [t for t, sk, _ in lich if sk == "FOMC"]
        sau = [t for t in fomc if t > b.C]
        truoc_f = [t for t in fomc if t <= b.C]
        r["gio_toi_fomc"] = round((sau[0] - b.C).total_seconds() / 3600, 1) if sau else None
        r["gio_tu_fomc"] = round((b.C - truoc_f[-1]).total_seconds() / 3600, 1) if truoc_f else None
        r["cua_so_fomc"] = int(bool((sau and sau[0] - b.C <= dt.timedelta(hours=72)) or
                                    (truoc_f and b.C - truoc_f[-1] <= dt.timedelta(hours=24))))
    if fkq:
        x = [k for k in fkq if k[0] <= b.C]
        if x:
            r["fomc_truoc_qd"], r["fomc_truoc_pd_tang"], r["fomc_truoc_pd_giam"] = x[-1][1], x[-1][2], x[-1][3]
    if truoc is None:
        return r
    np_ = nhan.get(truoc.ten) or {}
    r["ten_truoc"] = truoc.ten
    r["nhan_truoc"] = np_.get("huong")
    r["do_chac_truoc"] = np_.get("do_chac")
    r["doi_y_truoc"] = int(bool(np_.get("doi_y_giua_buoi")))
    r["gio_tu_truoc"] = round((b.C - truoc.C).total_seconds() / 3600, 1)
    r["dau_tuan"] = int(b.bat_dau.isocalendar()[:2] != truoc.bat_dau.isocalendar()[:2])
    r["dau_thang"] = int(b.ngay[:7] != truoc.ngay[:7])
    g0 = du.gia_luc(truoc.C)
    r["gia_truoc"] = round(g0, 1)
    r["di_pct"] = round((gia / g0 - 1) * 100, 2)
    hi, lo = du.cuc_tri(truoc.C, b.C)
    s = DAU.get(view)
    if s:
        r["di_theo_view"] = round(r["di_pct"] * s, 2)
        r["nguoc_max"] = round(((g0 - lo) / g0 if s > 0 else (hi - g0) / g0) * 100, 2) if hi else None
        r["thuan_max"] = round(((hi - g0) / g0 if s > 0 else (g0 - lo) / g0) * 100, 2) if hi else None
    # --- dich / chang 1 cua buoi truoc (rau tinh, cua so (C_{N-1}, C_N])
    r["co_dich_truoc"] = int(bool(np_.get("dich")))
    r["cham_dich_truoc"] = cham_vung(np_.get("dich"), g0, hi, lo)
    c1 = np_.get("chang1") or {}
    r["chang1_nguoc_truoc"] = int(bool(c1.get("huong") and np_.get("huong") in DAU and c1["huong"] != np_["huong"]))
    r["cham_chang1_truoc"] = cham_vung(c1.get("dich"), g0, hi, lo) if c1.get("dich") else None
    # --- vo hieu cua buoi truoc
    vh = np_.get("vo_hieu")
    r["co_vh_truoc"] = int(bool(vh))
    if vh:
        r["vh_khung"], r["vh_so_nen"] = vh["khung"], vh["so_nen"]
        r["vh_cach_pct"] = round((vh["gia"] / g0 - 1) * 100, 2)
        r["vh_cham_rau"] = int(bool(hi is not None and (lo < vh["gia"] if vh["chieu"] == "dong_duoi" else hi > vh["gia"])))
        idx = h.trong(truoc.C, b.C)
        a1, a2 = dong_qua(h, idx, vh["chieu"], vh["gia"], 1), dong_qua(h, idx, vh["chieu"], vh["gia"], 2)
        r["vh_dong_1h4"], r["vh_dong_2h4"] = int(a1 is not None), int(a2 is not None)
        kh = vh["khung"]
        k = {"H4": h, "D1": d, "W1": du.w1}.get(kh) or (du.khung_nho(kh) if kh in KHUNG_PHUT else h)
        r["vh_dong_dung_khung"] = int(dong_qua(k, k.trong(truoc.C, b.C), vh["chieu"], vh["gia"], vh["so_nen"]) is not None)
        r["vh_dong_d1"] = int(dong_qua(d, d.trong(truoc.C, b.C), vh["chieu"], vh["gia"], 1) is not None)
        r["vh_ben_kia_luc_C"] = int(qua(vh["chieu"], vh["gia"], gia))
        r["vh_vol_tb20"] = round(h.n[a1].v / h.tbv[a1], 2) if a1 is not None and h.tbv[a1] else None
    # --- nen trong cua so: H4 lon (than >= 1,5 ATR nen truoc), volume, D1 nhan chim
    idx4 = list(h.trong(truoc.C, b.C))
    lon_ng, lon_th, vmax, vmax_mau = [], [], None, None
    for i in idx4:
        n = h.n[i]
        if h.tbv[i]:
            q = n.v / h.tbv[i]
            if vmax is None or q > vmax:
                vmax, vmax_mau = q, (1 if n.c > n.o else -1)
        if h.atr[i - 1] and abs(n.c - n.o) >= 1.5 * h.atr[i - 1]:
            mau = 1 if n.c > n.o else -1
            q = round(n.v / h.tbv[i], 2) if h.tbv[i] else None
            (lon_ng if s and mau != s else lon_th).append(q)
    r["vol_h4_max_tb20"] = round(vmax, 2) if vmax else None
    if s and vmax_mau:
        r["vol_h4_max_nguoc"] = int(vmax_mau != s)
    r["h4_lon_nguoc"] = int(bool(lon_ng)) if s else None
    r["h4_lon_nguoc_vol"] = max([q for q in lon_ng if q] or [0]) or None
    r["h4_lon_thuan"] = int(bool(lon_th)) if s else None
    idx1 = list(d.trong(truoc.C, b.C))
    r["so_d1_dong"] = len(idx1)
    vd = [d.n[i].v / d.tbv[i] for i in idx1 if d.tbv[i]]
    r["vol_d1_max_tb20"] = round(max(vd), 2) if vd else None
    if s:
        nc = [nhan_chim(d, i) for i in idx1]
        r["d1_nhan_chim_nguoc"] = int(-s in nc)
        r["d1_nhan_chim_thuan"] = int(s in nc)
        r["d1_dong_nguoc_cs"] = int(any((1 if d.n[i].c > d.n[i].o else -1) != s for i in idx1))
        r["d1_cuoi_nguoc"] = int(r["d1_cuoi_mau"] != s)
    # --- tin tuc: lich kinh te (cong bo truoc) + Polymarket (gia da co <= C) + loi nguoi do o buoi truoc
    if lich is not None:
        giua = [sk for t, sk, _ in lich if truoc.C < t <= b.C]
        sap24 = [sk for t, sk, _ in lich if b.C < t <= b.C + dt.timedelta(hours=24)]
        sap48 = [sk for t, sk, _ in lich if b.C < t <= b.C + dt.timedelta(hours=48)]
        r["tin_lon_giua"] = int(any(x in TIN_LON for x in giua))
        r["tin_giua"] = "+".join(sorted(set(giua)))
        r["tin_lon_sap24"] = int(any(x in TIN_LON for x in sap24))
        r["tin_lon_sap48"] = int(any(x in TIN_LON for x in sap48))
        r["tin_sap48"] = "+".join(sorted(set(sap48)))

    if pm is not None:
        g1, t1, d1_ = pm_luc(pm, b.C)
        if t1 is not None:
            r["pm_tang"], r["pm_giam"] = round(t1 * 100, 1), round(d1_ * 100, 1)
            r["pm_noi_long"] = round((d1_ - t1) * 100, 1)
            for ngay in (3, 7):
                _, t0, d0 = pm_luc(pm, b.C - dt.timedelta(days=ngay), g1)
                if t0 is not None:
                    r[f"pm_tang_d{ngay}"] = round((t1 - t0) * 100, 1)
                    r[f"pm_noi_long_d{ngay}"] = round(((d1_ - t1) - (d0 - t0)) * 100, 1)
            _, t0, d0 = pm_luc(pm, truoc.C, g1)
            if t0 is not None:
                r["pm_doi"] = round(((d1_ - t1) - (d0 - t0)) * 100, 1)
    tt = np_.get("tin_tuc")
    if isinstance(tt, list):
        r["truoc_nhac_tin"] = int(bool(tt))
        vb = khong_dau(json.dumps(tt, ensure_ascii=False)).lower()
        r["truoc_cho_tin"] = int(bool(re.search(r"cho tin|ne (tin|ngay)|sau (khi )?(co )?tin|truoc tin|doi tin", vb)))
    # --- trendline (neu co file su kien)
    if tl is not None:
        r.update(dac_trung_tl(tl.get(b.vid, []), s))
    return r


def main():
    a = sys.argv[1:]
    che_do = a[a.index("--nhan") + 1] if "--nhan" in a else "tu_dong"
    ds = ds_buoi(a[a.index("--pham-vi") + 1] if "--pham-vi" in a else "tat_ca")
    if che_do == "tu_dong":
        co = sum((GOC / "hoc_v5" / "nhan" / f"{b.ten}.json").exists() or b.ten in V2_DUOC_DUNG
                 for b in ds if b.ngay < TU_THI)
        che_do = "moi" if co >= 90 else "cu"
        print(f"tu_dong: {co} buoi tap hoc co nhan moi -> dung nhan {che_do}")
    doc = doc_nhan_moi if che_do == "moi" else doc_nhan_cu
    nhan = {}
    for b in ds:
        x = doc(b.ten)
        if x is not None:
            nhan[b.ten] = x
    du = DuLieu()
    tl = doc_trendline()
    lich = doc_lich_tin()
    pm = doc_polymarket(lich)
    fkq = doc_fomc_ket_qua()
    dong, view = [], None
    for k, b in enumerate(ds):
        truoc = ds[k - 1] if k else None
        if truoc and truoc.C > b.bat_dau:
            raise RuntimeError(f"buoi {truoc.ten} ket thuc sau khi {b.ten} bat dau")
        if truoc is not None and truoc.ten in nhan and nhan[truoc.ten]["huong"] in DAU:
            view = nhan[truoc.ten]["huong"]
        dong.append(dac_trung_buoi(du, b, truoc, nhan, view, tl, lich, pm, fkq))
    cot = []
    for r in dong:
        for c in r:
            if c not in cot:
                cot.append(c)
    p = RA / f"dac_trung_{che_do}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cot)
        w.writeheader()
        for r in dong:
            w.writerow({c: ("" if r.get(c) is None else int(r[c]) if isinstance(r[c], bool) else r[c]) for c in cot})
    (RA / f"nhan_{che_do}.json").write_text(json.dumps({"che_do": che_do, "so_buoi": len(ds), "co_nhan": len(nhan),
                                                         "trendline": tl is not None, "lich_tin": lich is not None,
                                                         "polymarket": pm is not None, "nhan": nhan},
                                                        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(dong)} buoi, {len(nhan)} co nhan ({che_do}), trendline: {'co' if tl is not None else 'CHUA CO'}, "
          f"lich tin: {'co' if lich else 'CHUA CO'}, polymarket: {'co' if pm else 'CHUA CO'} -> {p}")


if __name__ == "__main__":
    main()
