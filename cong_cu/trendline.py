#!/usr/bin/env python3
"""Trendline BTC nhan qua (H4 + D1) — bat chuoc cach nguoi do ve va danh gia pha trendline.

Luat (so tay A1, A4, B; ghi chu anh hinh_anh_*.md):
  - Duong KHANG CU GIAM noi >= 2 dinh fractal ha dan; duong HO TRO TANG noi >= 2 day fractal nang dan; tren H4 va D1.
  - Hop le khi khong co close (cung khung voi duong) nao xuyen duong giua 2 neo (dung sai TOL_XUYEN).
  - Pha = nen H4 DONG vuot duong ("rau khong tinh"); ghi 1 nen / 2 nen lien tiep; pha gia = trong K_GIA nen H4 sau do
    co close quay lai phia cu; test lai = sau pha that, rau cham duong ma close van o phia moi.
  - Moi su kien pha ghi ti le volume nen pha / trung binh VOL_N nen H4 da dong truoc no (chi ghi, khong loc).
NHAN QUA: tai thoi diem t (giay epoch UTC) chi dung nen co gio DONG <= t. Pivot fractal i chi dung khi nen i+k da dong.
  Duong duoc tinh truoc tren toan bo du lieu nhung moi thong tin (luc biet duong, su kien, cham) deu gan gio dong nen,
  truy van tai t chi doc phan <= t → cat du lieu tai t cho cung ket qua (kiem: hoc_v5/trendline/kiem_tra.py).
Bien the: xem hoc_v5/trendline/BIEN_THE.md (luoi neo × k × tuoi × chon); ban khoa: hoc_v5/trendline/CHON.md.

Dung:
  python3 cong_cu/trendline.py "2026-03-12 04:00" [ten_bien_the]     # in duong con hieu luc + duong chinh tai gio UTC do
"""
import bisect, csv, datetime as dt, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chi_bao import fractal  # noqa: E402

GOC = Path(__file__).resolve().parent.parent
DU_LIEU = GOC / "bot_v4" / "du_lieu"
GIAY = {"H4": 4 * 3600, "D1": 86400}
NGAY = 86400

# ---- phan co dinh (BIEN_THE.md) ----
TOL_XUYEN = 0.0          # close vuot duong qua ti le nay moi tinh la xuyen (giua 2 neo)
TOL_CHAM = 0.003         # rau trong ±0,3% gia duong = 1 lan cham
K_GIA = 3                # so nen H4 sau nen pha de xet pha gia
# so nen H4 duong con duoc LIET KE sau nen pha that: H4 48h; D1 14 ngay (sua sau khoa 31/10: nguoi do van nhac duong D1
# da gay nhieu ngay, vd 30/03). Duong CHINH van chi chon trong duong chua pha that hoac pha that < VUA_PHA_GIO (nhu luc khoa).
HIEU_LUC_SAU_PHA = {"H4": 12, "D1": 84}
VUA_PHA_GIO = 48         # pha that trong 48h gan nhat van tinh "vua pha" khi so trang thai + van duoc chon lam duong chinh
VOL_N = 20               # trung binh volume cua 20 nen H4 da dong truoc nen pha
TUOI = {"ngan": {"H4": 30 * NGAY, "D1": 120 * NGAY}, "dai": {"H4": 90 * NGAY, "D1": 365 * NGAY}}
LOAI = ("khang_cu_giam", "ho_tro_tang")
KHUNG = ("H4", "D1")

TRUC = {"neo": ("rau", "than"), "k": (2, 3), "tuoi": ("ngan", "dai"),
        "chon": ("nhieu_cham", "gan_gia", "dai_nhat", "cuc_tri")}


def danh_sach_bien_the():
    """Luoi 32 bien the theo dung thu tu khai bao (thu tu nay dung lam luat hoa cuoi cung)."""
    ra = []
    for neo in TRUC["neo"]:
        for k in TRUC["k"]:
            for tuoi in TRUC["tuoi"]:
                for chon in TRUC["chon"]:
                    ra.append({"ten": f"{neo}|{k}|{tuoi}|{chon}", "neo": neo, "k": k, "tuoi": tuoi, "chon": chon})
    return ra


def bien_the(ten):
    for b in danh_sach_bien_the():
        if b["ten"] == ten:
            return b
    raise KeyError(ten)


# ---- thoi gian ----
def ts_tu_chuoi(s):
    """'YYYY-MM-DD HH:MM' (UTC) → giay epoch."""
    return int(dt.datetime.strptime(s.strip()[:16], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).timestamp())


def chuoi_tu_ts(x):
    return dt.datetime.fromtimestamp(x, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")


# ---- du lieu ----
class Nen:
    __slots__ = ("khung", "dur", "mo", "o", "h", "l", "c", "v")

    def __init__(self, khung, mo, o, h, l, c, v):
        self.khung, self.dur = khung, GIAY[khung]
        self.mo, self.o, self.h, self.l, self.c, self.v = mo, o, h, l, c, v

    def __len__(self):
        return len(self.mo)

    def so_nen_dong(self, t):
        """So nen co gio dong (mo + dur) <= t."""
        return bisect.bisect_right(self.mo, t - self.dur)

    def cat(self, t):
        n = self.so_nen_dong(t)
        return Nen(self.khung, self.mo[:n], self.o[:n], self.h[:n], self.l[:n], self.c[:n], self.v[:n])


def doc_nen(khung, thu_muc=DU_LIEU, tai_san="BTC"):
    ten = {"H4": "4H", "D1": "1D"}[khung]
    mo, o, h, l, c, v = [], [], [], [], [], []
    with open(Path(thu_muc) / f"{tai_san}_{ten}.csv", newline="") as f:
        for r in csv.DictReader(f):
            mo.append(ts_tu_chuoi(r["ts_utc"]))
            o.append(float(r["open"])); h.append(float(r["high"])); l.append(float(r["low"]))
            c.append(float(r["close"])); v.append(float(r["vol"]))
    return Nen(khung, mo, o, h, l, c, v)


class BoDuLieu:
    """H4 + D1 cung tai san, kem bo nho dem duong da tinh (theo khung, loai, k, neo)."""

    def __init__(self, h4, d1):
        self.nen = {"H4": h4, "D1": d1}
        self._dem = {}

    @classmethod
    def doc(cls, thu_muc=DU_LIEU):
        return cls(doc_nen("H4", thu_muc), doc_nen("D1", thu_muc))

    def cat(self, t):
        return BoDuLieu(self.nen["H4"].cat(t), self.nen["D1"].cat(t))

    def gia_tai(self, t):
        """Close H4 cuoi cung da dong tai t."""
        h4 = self.nen["H4"]
        n = h4.so_nen_dong(t)
        return h4.c[n - 1] if n else None

    def duong(self, khung, loai, k, neo):
        key = (khung, loai, k, neo)
        if key not in self._dem:
            self._dem[key] = liet_ke_duong(self, khung, loai, k, neo)
        return self._dem[key]


# ---- duong ----
class Duong:
    __slots__ = ("id", "khung", "loai", "neo", "k", "ia", "ib", "xa", "pa", "xb", "pb", "m", "t_biet",
                 "cham", "ev")

    def gia(self, x):
        return self.pa + self.m * (x - self.xa)


def _ti_le_vol(h4, j):
    if j < VOL_N:
        return None
    tb = sum(h4.v[j - VOL_N:j]) / VOL_N
    return h4.v[j] / tb if tb > 0 else None


def _su_kien_h4(d, h4, j0, x_het):
    """Chay may trang thai tren close H4 tu nen j0 (nen dau sau neo 2). Moi su kien gan gio DONG nen H4 lam ra no.
    Tra (ev, j_pha_that) — j_pha_that = chi so nen pha cua lan pha that (None neu chua)."""
    tren = d.loai == "khang_cu_giam"   # pha = close vuot len tren; ho tro: close xuong duoi
    n = len(h4)
    dur = h4.dur
    ev = []

    def vuot(j):
        y = d.gia(h4.mo[j])
        return (h4.c[j] > y) if tren else (h4.c[j] < y)

    j = j0
    while j < n and h4.mo[j] <= x_het:
        if not vuot(j):
            j += 1
            continue
        ev.append((h4.mo[j] + dur, "pha", {"j": j, "vol": _ti_le_vol(h4, j), "dong": h4.c[j],
                                           "duong": d.gia(h4.mo[j])}))
        quay = None
        con_thieu = False
        for q in range(1, K_GIA + 1):
            if j + q >= n:
                con_thieu = True
                break
            if vuot(j + q):
                if q == 1:
                    ev.append((h4.mo[j + 1] + dur, "xac_nhan_2n", {}))
            else:
                quay = j + q
                break
        if quay is not None:
            ev.append((h4.mo[quay] + dur, "pha_gia", {"j": quay}))
            j = quay + 1
            continue
        if con_thieu:
            return ev, None
        j_pha = j
        ev.append((h4.mo[j + K_GIA] + dur, "pha_that", {"j_pha": j_pha}))
        # sau pha that: test lai / that bai / het han (tu nen ngay sau nen pha)
        n_sau = HIEU_LUC_SAU_PHA[d.khung]
        for q in range(j_pha + 1, min(n, j_pha + n_sau + 1)):
            y = d.gia(h4.mo[q])
            if q > j_pha + K_GIA and not vuot(q):
                ev.append((h4.mo[q] + dur, "that_bai", {"j": q}))
                ev.sort(key=lambda e: e[0])
                return ev, j_pha
            cham = (h4.l[q] <= y * (1 + TOL_CHAM)) if tren else (h4.h[q] >= y * (1 - TOL_CHAM))
            if cham and vuot(q):
                ev.append((h4.mo[q] + dur, "test_lai", {"j": q}))
        if j_pha + n_sau < n:
            ev.append((h4.mo[j_pha + n_sau] + dur, "het_han", {}))
        ev.sort(key=lambda e: e[0])
        return ev, j_pha
    return ev, None


def liet_ke_duong(du, khung, loai, k, neo):
    """Moi duong hop le (khung, loai) theo fractal k, neo rau/than; tinh truoc su kien + cham (deu gan gio dong nen)."""
    F, h4 = du.nen[khung], du.nen["H4"]
    if neo == "rau":
        s_h, s_l = F.h, F.l
    else:
        s_h = [max(a, b) for a, b in zip(F.o, F.c)]
        s_l = [min(a, b) for a, b in zip(F.o, F.c)]
    dinh, day = fractal(s_h, s_l, k)
    tren = loai == "khang_cu_giam"
    piv = dinh if tren else day
    x, c, dur = F.mo, F.c, F.dur
    span = TUOI["dai"][khung]
    he = 1.0 / (1 + TOL_XUYEN) if tren else 1.0 / (1 - TOL_XUYEN)
    ra = []
    for ai, (a, pa) in enumerate(piv):
        xa = x[a]
        run = float("-inf") if tren else float("inf")
        j = a + 1
        for b, pb in piv[ai + 1:]:
            if x[b] - xa > span:
                break
            while j < b:
                r = (c[j] * he - pa) / (x[j] - xa)
                run = max(run, r) if tren else min(run, r)
                j += 1
            if (tren and run >= 0) or (not tren and run <= 0):
                break  # da co close vuot muc neo 1 → khong con neo 2 nao hop le
            m = (pb - pa) / (x[b] - xa)
            if tren:
                ok = pb < pa and m >= run
            else:
                ok = pb > pa and m <= run
            if not ok or b + k >= len(F):
                continue
            d = Duong()
            d.khung, d.loai, d.neo, d.k = khung, loai, neo, k
            d.ia, d.ib, d.xa, d.pa, d.xb, d.pb, d.m = a, b, xa, pa, x[b], pb, m
            d.id = f"{khung}:{loai}:{neo}{k}:{chuoi_tu_ts(xa)}>{chuoi_tu_ts(x[b])}"
            d.t_biet = x[b + k] + dur
            x_het = xa + span
            j0 = bisect.bisect_left(h4.mo, x[b] + dur)   # nen H4 dau tien mo sau khi nen neo 2 dong
            d.ev, _ = _su_kien_h4(d, h4, j0, x_het)
            # duong da bi pha (bat ky) truoc khi biet duong → bo (nguoi ve khong ve duong da bi xuyen)
            if any(e[1] == "pha" and e[0] <= d.t_biet for e in d.ev):
                continue
            # cham tren khung cua duong, tu neo 1 toi het tuoi (gioi han boi lan pha that da biet tai t: xem _thong_tin)
            cham, truoc = [], False
            q = a
            while q < len(F) and x[q] <= x_het:
                y = d.gia(x[q])
                if tren:
                    co = abs(F.h[q] - y) <= TOL_CHAM * y and c[q] <= y
                else:
                    co = abs(F.l[q] - y) <= TOL_CHAM * y and c[q] >= y
                if q == a or q == b:
                    co = True
                if co and not truoc:
                    cham.append(x[q] + dur)
                truoc = co
                q += 1
            d.cham = cham
            ra.append(d)
    return ra


def trang_thai(d, t):
    """Trang thai duong tai t tu su kien <= t: giu | vua_pha_1n | vua_pha_2n | pha_gia | da_pha | pha_roi_test_lai |
    het_hieu_luc. Tra (trang_thai, thong tin lan pha gan nhat hoac None)."""
    st, pha, test = "giu", None, False
    for te, kind, info in d.ev:
        if te > t:
            break
        if kind == "pha":
            st, test = "vua_pha_1n", False
            pha = {"t_pha": te, "vol": info["vol"], "hai_nen": False, "gia_duong": info["duong"],
                   "dong": info["dong"], "ket_qua": "chua_ro"}
        elif kind == "xac_nhan_2n":
            st = "vua_pha_2n"
            pha["hai_nen"] = True
        elif kind == "pha_gia":
            st = "pha_gia"
            pha["ket_qua"] = "pha_gia"
        elif kind == "pha_that":
            st = "pha_roi_test_lai" if test else "da_pha"
            pha["ket_qua"] = "pha_that"
        elif kind == "test_lai":
            test = True
            if st == "da_pha":
                st = "pha_roi_test_lai"
        elif kind in ("het_han", "that_bai"):
            st = "het_hieu_luc"
    return st, pha


def _thong_tin(d, t, gia):
    st, pha = trang_thai(d, t)
    y = d.gia(t)
    # cham chi dem toi nen pha that (neu tai t da biet la pha that); pha gia / chua ro → dem tat ca cham <= t
    t_cham = pha["t_pha"] if pha and pha["ket_qua"] == "pha_that" else t
    # so ngay tu nen pha THAT (chi khi da xac nhan tai t); None neu chua pha that
    da_pha_ngay = (t - pha["t_pha"]) / NGAY if pha and pha["ket_qua"] == "pha_that" and st in ("da_pha", "pha_roi_test_lai") \
        else None
    return {"id": d.id, "khung": d.khung, "loai": d.loai,
            "neo1_ts": chuoi_tu_ts(d.xa), "neo1_gia": d.pa, "neo2_ts": chuoi_tu_ts(d.xb), "neo2_gia": d.pb,
            "doc_ngay": d.m * NGAY, "gia_t": y, "cach_pct": (y - gia) / gia * 100 if gia else None,
            "so_cham": bisect.bisect_right(d.cham, min(t, t_cham)), "tuoi_ngay": (t - d.xa) / NGAY,
            "trang_thai": st, "pha": pha, "_d": d,
            "da_pha_ngay": da_pha_ngay, "test_lai": st == "pha_roi_test_lai",
            "ghi_chu_pha": (f"đã phá cách đây {da_pha_ngay:.1f} ngày, "
                            + ("đã test lại" if st == "pha_roi_test_lai" else "chưa test lại")) if da_pha_ngay is not None else ""}


def duong_hieu_luc(du, t, bt, khung, loai):
    """Cac duong con hieu luc tai t cua bien the bt (dict) cho (khung, loai): da biet (t_biet <= t), tuoi neo 1 <= tuoi,
    chua het hieu luc. Moi phan tu la dict thong tin (xem _thong_tin)."""
    gia = du.gia_tai(t)
    tuoi = TUOI[bt["tuoi"]][khung]
    ra = []
    for d in du.duong(khung, loai, bt["k"], bt["neo"]):
        if d.t_biet > t or d.xa < t - tuoi:
            continue
        tt = _thong_tin(d, t, gia)
        if tt["trang_thai"] == "het_hieu_luc":
            continue
        ra.append(tt)
    return ra


def duoc_chon_chinh(r):
    """Duong duoc xet lam duong chinh: chua pha that, hoac pha that chua toi VUA_PHA_GIO (y nhu luc khoa bien the — duong D1
    da pha lau hon chi duoc LIET KE, khong lam duong chinh)."""
    return r["da_pha_ngay"] is None or r["da_pha_ngay"] * 24 < VUA_PHA_GIO


def chon_chinh(ds, bt):
    """Duong chinh theo luat bt['chon'] (BIEN_THE.md), trong cac duong duoc_chon_chinh."""
    ds = [r for r in ds if duoc_chon_chinh(r)]
    if not ds:
        return None
    kc = lambda r: abs(r["cach_pct"]) if r["cach_pct"] is not None else 1e9  # noqa: E731
    ch = bt["chon"]
    if ch == "nhieu_cham":
        key = lambda r: (-r["so_cham"], kc(r), r["id"])  # noqa: E731
    elif ch == "gan_gia":
        key = lambda r: (kc(r), -r["so_cham"], r["id"])  # noqa: E731
    elif ch == "dai_nhat":
        key = lambda r: (r["_d"].xa, -r["so_cham"], kc(r), r["id"])  # noqa: E731
    elif ch == "cuc_tri":
        dau = -1 if ds[0]["loai"] == "khang_cu_giam" else 1
        key = lambda r: (dau * r["neo1_gia"], -r["so_cham"], kc(r), r["id"])  # noqa: E731
    else:
        raise ValueError(ch)
    return min(ds, key=key)


def tai_thoi_diem(du, t, bt):
    """Ket qua day du tai t: {(khung, loai): {'duong': [...], 'chinh': {...}|None}}."""
    ra = {}
    for khung in KHUNG:
        for loai in LOAI:
            ds = duong_hieu_luc(du, t, bt, khung, loai)
            ra[(khung, loai)] = {"duong": ds, "chinh": chon_chinh(ds, bt)}
    return ra


def su_kien_khoang(du, bt, khung, loai, t0, t1):
    """Su kien pha trong (t0, t1] tren cac duong con hieu luc tai t0 (chua pha that) cua bien the; ket qua lan pha
    nhin tai t1. Tra (chinh_t0, ds_pha) — chinh_t0 = duong chinh tai t0, ds_pha = list dict pha (kem 'la_chinh')."""
    ds0 = [r for r in duong_hieu_luc(du, t0, bt, khung, loai)
           if r["trang_thai"] in ("giu", "pha_gia", "vua_pha_1n", "vua_pha_2n")]
    chinh0 = chon_chinh(ds0, bt)
    ra = []
    for r in ds0:
        d = r["_d"]
        for te, kind, info in d.ev:
            if kind != "pha" or te <= t0 or te > t1:
                continue
            # lay ket qua cua DUNG lan pha te (co the co nhieu lan): duyet lai toi t1
            kq = {"t_pha": te, "vol": info["vol"], "hai_nen": False, "ket_qua": "chua_ro", "test_lai": False}
            for te2, k2, _i2 in d.ev:
                if te2 <= te or te2 > t1:
                    continue
                if k2 == "xac_nhan_2n" and kq["ket_qua"] == "chua_ro" and not kq["hai_nen"]:
                    kq["hai_nen"] = True
                elif k2 == "pha_gia" and kq["ket_qua"] == "chua_ro":
                    kq["ket_qua"] = "pha_gia"
                    break
                elif k2 == "pha_that" and kq["ket_qua"] == "chua_ro":
                    kq["ket_qua"] = "pha_that"
                elif k2 == "test_lai" and kq["ket_qua"] == "pha_that":
                    kq["test_lai"] = True
                elif k2 == "pha":
                    break
            kq.update({"id": d.id, "gia_duong": info["duong"], "dong": info["dong"],
                       "chieu": "len" if loai == "khang_cu_giam" else "xuong",
                       "la_chinh": chinh0 is not None and chinh0["id"] == d.id})
            ra.append(kq)
    ra.sort(key=lambda z: z["t_pha"])
    return chinh0, ra


def _in(du, t, bt):
    gia = du.gia_tai(t)
    print(f"t = {chuoi_tu_ts(t)} UTC  gia H4 = {gia}  bien the {bt['ten']}")
    for (khung, loai), v in tai_thoi_diem(du, t, bt).items():
        c = v["chinh"]
        print(f"[{khung} {loai}] {len(v['duong'])} duong")
        if c:
            print(f"   CHINH {c['neo1_ts']} {c['neo1_gia']:.1f} → {c['neo2_ts']} {c['neo2_gia']:.1f}  gia_t {c['gia_t']:.1f}"
                  f" ({c['cach_pct']:+.2f}%)  cham {c['so_cham']}  tuoi {c['tuoi_ngay']:.1f}d  {c['trang_thai']}"
                  + (f"  pha vol x{c['pha']['vol']:.2f}" if c["pha"] and c["pha"]["vol"] else ""))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    t = ts_tu_chuoi(sys.argv[1])
    ten = sys.argv[2] if len(sys.argv) > 2 else None
    if ten is None:
        p = GOC / "hoc_v5" / "trendline" / "CHON.md"
        ten = "rau|2|ngan|cuc_tri"
        if p.exists():
            for dong in p.read_text(encoding="utf-8").splitlines():
                if dong.startswith("BIEN_THE_KHOA:"):
                    ten = dong.split(":", 1)[1].strip().strip("`")
    _in(BoDuLieu.doc(), t, bien_the(ten))
