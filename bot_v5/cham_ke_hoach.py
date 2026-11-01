#!/usr/bin/env python3
"""Chấm kế hoạch bot v5 THEO ĐÚNG THỨ TỰ THỜI GIAN — kết quả LỆNH tách khỏi độ đúng DỰ BÁO; HẠN là cột riêng.

Đầu vào: file kế hoạch `bot_v5/ke_hoach/<stem>.json` (ke_hoach.py) + nến OKX đã đóng (cache RIÊNG `bot_v5/cache_cham/`,
không dùng chung cache hồ sơ). Không bao giờ ghi vào file kế hoạch; `--ghi` → file mới trong `bot_v5/ket_qua/`.

Báo riêng cho từng kế hoạch lệnh:
  A. Kích hoạt: khớp / chỉ "giá chạm vùng" (điều kiện khung nhỏ không kiểm bằng máy) / chưa khớp / đã huỷ / hết hạn chờ;
     TP chạm TRƯỚC khi khớp → ghi rõ, KHÔNG tính thắng.
  B. Sau khi vào: TP hay SL (chạm giá) / mốc đóng lệnh (nến ĐÓNG đúng khung, đủ số cây LIÊN TIẾP) xảy ra trước;
     chưa chạm gì khi hết dữ liệu → CHƯA NGÃ NGŨ + mốc dữ liệu cuối.
  C. Thời gian tới kết quả, mức đi ngược lớn nhất (MAE) và đi thuận lớn nhất (MFE).
  D. (phần dự báo) đích từng khung trước/sau mốc sai; đường đi đúng hay sai thứ tự chặng.
  E. Hạn: trong hạn / trễ hạn / chưa tới hạn — cột riêng, KHÔNG đổi kết quả TP/SL.
Thứ tự trong 1 nến: nến gốc 1H; nến có ≥ 2 sự kiện mà thứ tự quyết định kết quả → xét nến 15m → 5m → 1m của đúng nến
đó; vẫn chung 1 nến nhỏ nhất (hoặc không có dữ liệu nhỏ) → KHÔNG RÕ THỨ TỰ. Không suy thứ tự trong nến từ OHLC. Ngoại
lệ duy nhất (ghi rõ trong báo cáo): giá mở nến đã ở trong/vượt vùng vào → khớp tại giá mở, mọi chạm khác trong nến là
sau khi vào; giá phải qua vùng vào trước khi tới SL/mốc nằm xa hơn vùng vào (tính liên tục của giá, không phải đoán).
Giả định khớp (luôn in ra): lệnh chờ vùng khớp ở mép gần (LONG: mép trên) hoặc giá mở nếu mở đã trong vùng; VÀO NGAY
khớp ở giá kế hoạch ghi (= giá đóng T); chờ xác nhận nến đóng → khớp ở giá đóng cây xác nhận; TP tính khi chạm mép gần.
Mốc bắt đầu: hồi cứu (phát hành > 24h sau gio_cat) → gio_cat; trực tiếp → gio_phat_hanh (bỏ phần nến trước đó).

Dùng:
  python3 bot_v5/cham_ke_hoach.py <ke_hoach.json> [--den "YYYY-MM-DD HH:MM"] [--offline] [--cache DIR] [--ghi]
  Lệnh của user (giờ/giá do user nói; thiếu thì báo thiếu, không tự điền):
  python3 bot_v5/cham_ke_hoach.py <ke_hoach.json> --lenh-user LONG --theo <id kế hoạch>
          (--vao-luc "YYYY-MM-DD HH:MM" | --vao-ngay YYYY-MM-DD) [--gia-vao X]
  python3 bot_v5/cham_ke_hoach.py --ma BTC --lenh-user SHORT --vao-luc "…" --tp 70300-70700 [--sl X]
          [--dong-khi "1D tren 72000 1"] [--han "YYYY-MM-DD"]
"""
import argparse, datetime as dt, hashlib, json, sys
from pathlib import Path

DAY = Path(__file__).resolve().parent
sys.path.insert(0, str(DAY))
import nen as NG  # noqa: E402
import ke_hoach as KH  # noqa: E402

CACHE_CHAM = DAY / "cache_cham"
KET_QUA = DAY / "ket_qua"
GIAY = NG.GIAY
NHO = ["15m", "5m", "1m"]
TEN_KQ = {"TP": "TP trước", "SL": "SL (chạm giá) trước", "DONG": "mốc đóng lệnh (nến đóng) trước",
          "KHONG_RO": "KHÔNG RÕ THỨ TỰ", "CHUA_NGA_NGU": "CHƯA NGÃ NGŨ"}


# ---------------- nến ----------------
class Gia:
    """Nến ĐÃ ĐÓNG của 1 mã, giờ mở ≥ tu, giờ đóng ≤ den (giây UTC). Không trả nến nào đóng sau den.
    `nap` = {khung: [NenGia]} cho kiểm thử (khi đó không gọi nguồn nào)."""

    def __init__(self, ma, tu, den, cache_dir=CACHE_CHAM, offline=False, nap=None):
        self.ma, self.tu, self.den = ma, int(tu), int(den)
        self.cache_dir, self.offline, self.nap = Path(cache_dir), offline, nap
        self._kho, self._nho, self.loi = {}, {}, []
        self.nguon = "dữ liệu nạp sẵn (kiểm thử)" if nap is not None else "?"
        self.goc = "1H" if self.nen("1H") else "4H"

    def _lay(self, khung, a, b):
        if self.nap is not None:
            return [n for n in self.nap.get(khung, []) if n.mo >= a and n.dong <= min(b, self.den)]
        try:
            self.nguon, ds = NG.lay_khoang(self.ma, khung, a, min(b, self.den), self.cache_dir, self.offline)
            return ds
        except Exception as e:
            self.loi.append(f"{khung}: {type(e).__name__}: {e}")
            return []

    def nen(self, khung):
        if khung not in self._kho:
            self._kho[khung] = self._lay(khung, NG.mo_nen_chua(self.tu, khung), self.den)
        return self._kho[khung]

    def nen_trong(self, khung, a, b):
        """Nến khung nhỏ phủ ĐỦ [a, b) — thiếu cây nào → None (không phân xử bằng dữ liệu lủng)."""
        k = (khung, a, b)
        if k not in self._nho:
            ds = [n for n in self._lay(khung, a, b) if a <= n.mo and n.dong <= b] if b <= self.den else []
            self._nho[k] = ds if len(ds) == (b - a) // GIAY[khung] else None
        return self._nho[k]

    def du_lieu_toi(self):
        g = self.nen(self.goc)
        return g[-1].dong if g else self.tu

    def lung(self, tu):
        """Các khoảng thiếu nến gốc từ `tu` tới hết dữ liệu."""
        ra, truoc = [], None
        for n in self.nen(self.goc):
            if n.dong <= tu:
                truoc = n.dong
                continue
            if truoc is not None and n.mo > truoc:
                ra.append((truoc, n.mo))
            truoc = n.dong
        return ra


class SuKien:
    """Xảy ra trong [a, b) của 1 nến `khung`; a == b → đúng thời điểm (nến đóng / giá mở)."""

    def __init__(self, a, b, khung, mo_ta=""):
        self.a, self.b, self.khung, self.mo_ta = a, b, khung, mo_ta

    def chu(self):
        if self.a == self.b:
            return f"{KH.gio_vn(self.a, True)} VN"
        return f"{KH.gio_vn(self.a, True)}–{KH.gio_vn(self.b, True)[-5:]} VN (nến {self.khung})"


def cham(n, phia, muc):
    return n.h >= muc if phia == "tren" else n.l <= muc


def tim_dong(gia, tu, dk):
    """Thời điểm `so_nen` nến khung dk LIÊN TIẾP đóng qua mức (chỉ nến có giờ đóng > tu; râu không tính)."""
    dem = 0
    for n in gia.nen(dk["khung"]):
        if n.dong <= tu:
            continue
        qua = n.c > dk["gia"] if dk["phia"] == "tren" else n.c < dk["gia"]
        dem = dem + 1 if qua else 0
        if dem >= dk.get("so_nen", 1):
            return n.dong
    return None


def mo_ta_dk(dk):
    return KH._mo_ta_dk(dk)


def tg(giay):
    giay = max(0, int(giay))
    d, h, m = giay // 86400, (giay % 86400) // 3600, (giay % 3600) // 60
    if d:
        return f"{d} ngày {h} giờ"
    return f"{h} giờ" + (f" {m} phút" if m else "") if h else f"{m} phút"


def han_chu(t):
    """Hạn ghi bằng ngày được lưu là 00:00 VN ngày sau → in "hết DD/MM"."""
    d = dt.datetime.fromtimestamp(t, KH.VN)
    if d.hour == 0 and d.minute == 0:
        return "hết " + (d - dt.timedelta(days=1)).strftime("%d/%m/%Y")
    return KH.gio_vn(t)


# ---------------- máy trạng thái 1 lệnh ----------------
class May:
    """CHO (chờ khớp) → VAO (đã vào) → xong. Kết quả chính = sự kiện đầu tiên sau khi vào: TP1 / SL / mốc đóng."""

    def __init__(self, gia, lenh, bat_dau):
        self.g, self.L, self.bd = gia, lenh, bat_dau
        ch = lenh["chieu"]
        self.p_tp, self.p_ra = KH.phia_thuan(ch), KH.phia_nguoc(ch)
        self.trang = "CHO"
        self.vao = None          # SuKien
        self.gia_vao = None
        self.tp_truoc = None     # TP chạm khi chưa khớp
        self.huy = None          # (lý do, SuKien)
        self.kq = None           # (loại, SuKien, mô tả)
        self.tp_sau = []         # TP các nấc sau (phần còn lại) [(i, SuKien)]
        self.ra_sau = None       # phần còn lại ra lúc nào
        self.i_tp = 0
        self.xong = False
        self.gia_dinh = list(lenh.get("gia_dinh", []))
        self.ghi_chu = []
        self.cuc = {"cao": None, "thap": None}   # cực trị trên nến chắc chắn sau khi vào, trước nến kết quả
        self.khong_du_lieu = False
        ts = [t for t in (tim_dong(gia, bat_dau, dk) for dk in lenh.get("huy_dong", [])) if t]
        self.t_huy_dong = min(ts) if ts else None
        self.t_kich = tim_dong(gia, bat_dau, lenh["kich_hoat"]) if lenh["kieu_vao"] == "dong" else None
        self.t_ra_dong = None

    # -- chuyển trạng thái --
    def _vao(self, sk, gia_vao, gia_dinh=None):
        self.trang, self.vao, self.gia_vao = "VAO", sk, gia_vao
        if gia_dinh:
            self.gia_dinh.append(gia_dinh)
        ts = [t for t in (tim_dong(self.g, sk.a, dk) for dk in self.L.get("dong_khi", [])) if t]
        self.t_ra_dong = min(ts) if ts else None

    def _ket(self, loai, sk, mo_ta=""):
        if self.kq is None:
            self.kq = (loai, sk, mo_ta)
            if loai != "TP" or self.i_tp + 1 >= len(self.L["tp"]):
                self.xong = True
            else:
                self.i_tp += 1
        else:  # phần còn lại sau TP1
            if loai == "TP":
                self.tp_sau.append((self.i_tp, sk))
                self.i_tp += 1
                if self.i_tp >= len(self.L["tp"]):
                    self.xong = True
            else:
                self.ra_sau = (loai, sk, mo_ta)
                self.xong = True

    def _khong_ro(self, n, khung, vi_sao):
        sk = SuKien(n.mo, n.dong, khung)
        if self.trang == "CHO" or self.kq is None:
            self.kq = ("KHONG_RO", sk, vi_sao)
        else:
            self.ra_sau = ("KHONG_RO", sk, vi_sao)
        self.xong = True

    # -- sự kiện theo nến đóng / mốc giờ --
    def truoc_moc(self, t):
        """Áp các sự kiện tại thời điểm ≤ t (nến đóng, hết hạn chờ) — gọi trước khi xét nến mở lúc t."""
        if self.xong:
            return
        if self.trang == "CHO":
            ds = []
            if self.L.get("het_han_cho") and self.L["het_han_cho"] <= t:
                ds.append((self.L["het_han_cho"], "HET_HAN_CHO"))
            if self.t_huy_dong and self.t_huy_dong <= t:
                ds.append((self.t_huy_dong, "HUY"))
            if self.t_kich and self.t_kich <= t:
                ds.append((self.t_kich, "KICH"))
            if not ds:
                return
            ds.sort()
            if len(ds) > 1 and ds[0][0] == ds[1][0] and "KICH" in (ds[0][1], ds[1][1]):
                self.kq = ("KHONG_RO", SuKien(ds[0][0], ds[0][0], "—"), "xác nhận vào và huỷ/hết hạn cùng lúc")
                self.xong = True
                return
            t0, loai = ds[0]
            if loai == "KICH":
                dk = self.L["kich_hoat"]
                n = next(x for x in self.g.nen(dk["khung"]) if x.dong == t0)
                self._vao(SuKien(t0, t0, dk["khung"], "nến xác nhận đóng"), n.c,
                          f"chờ xác nhận: khớp ở giá đóng cây xác nhận {n.c} lúc {KH.gio_vn(t0, True)}")
                self.truoc_moc(t)
            else:
                ly_do = "hết hạn chờ khớp" if loai == "HET_HAN_CHO" else "điều kiện huỷ (nến đóng) xảy ra trước khi khớp"
                self.huy = (ly_do, SuKien(t0, t0, "—"))
                self.xong = True
        elif self.t_ra_dong and self.t_ra_dong <= t:
            self._ket("DONG", SuKien(self.t_ra_dong, self.t_ra_dong, "đóng"),
                      "; ".join(mo_ta_dk(dk) for dk in self.L["dong_khi"]))

    # -- xét 1 nến --
    def buoc(self, n, khung):
        if self.xong:
            return
        if self.trang == "CHO":
            self._buoc_cho(n, khung)
        else:
            self._buoc_vao(n, khung)

    def _chia_nho(self, n, khung):
        for k2 in NHO:
            if GIAY[k2] >= GIAY[khung]:
                continue
            ds = self.g.nen_trong(k2, n.mo, n.dong)
            if ds is None:
                continue
            for m in ds:
                if self.xong:
                    break
                self.truoc_moc(m.mo)
                self.buoc(m, k2)
            return True
        return False

    def _buoc_cho(self, n, khung):
        L = self.L
        ch_vao = L["kieu_vao"] == "vung" and cham(n, L["phia_vao"], L["muc_vao"])
        ch_tp = cham(n, self.p_tp, L["tp"][0])
        ch_huy = [x for x in L.get("huy_cham", []) if cham(n, *x)]
        if not ch_vao:
            if ch_huy:
                self.huy = ("điều kiện huỷ (chạm giá) xảy ra trước khi khớp", SuKien(n.mo, n.dong, khung))
                self.xong = True
            if ch_tp and self.tp_truoc is None:
                self.tp_truoc = SuKien(n.mo, n.dong, khung)
                if L.get("huy_khi_tp_truoc") and not self.xong:
                    self.huy = ("TP đã chạm trước khi khớp (kế hoạch ghi huỷ khi đó)", self.tp_truoc)
                    self.xong = True
            return
        mv = L["muc_vao"]
        mo_da_khop = n.o <= mv if L["chieu"] == "LONG" else n.o >= mv
        if mo_da_khop:  # khớp tại giá mở → mọi chạm khác trong nến là sau khi vào
            self._vao(SuKien(n.mo, n.mo, khung, "giá mở đã trong vùng"), n.o,
                      f"giá mở nến {khung} {KH.gio_vn(n.mo, True)} ({n.o}) đã trong/vượt vùng vào → khớp tại giá mở")
            self._buoc_vao(n, khung, nen_vao=True)
            return
        if not ch_tp and not ch_huy:
            self._vao(SuKien(n.mo, n.dong, khung, "chạm vùng"), mv, None)
            if self.L.get("sl") is not None and cham(n, self.p_ra, self.L["sl"]):
                self._ket("SL", SuKien(n.mo, n.dong, khung), "SL chạm ngay trong nến khớp (giá phải qua vùng vào "
                          "trước khi tới SL — tính liên tục của giá)")
            return
        if self._chia_nho(n, khung):
            return
        cai = "TP" if ch_tp else "điều kiện huỷ"
        self._khong_ro(n, khung, f"nến vừa chạm vùng vào vừa chạm {cai}; không có nến nhỏ hơn để biết cái nào trước")

    def _buoc_vao(self, n, khung, nen_vao=False):
        L = self.L
        ch_tp = cham(n, self.p_tp, L["tp"][self.i_tp])
        ch_sl = L.get("sl") is not None and cham(n, self.p_ra, L["sl"])
        if ch_tp and ch_sl:
            if self._chia_nho(n, khung):
                return
            self._khong_ro(n, khung, "cùng nến chạm cả TP và SL; không có nến nhỏ hơn để biết cái nào trước")
            return
        sk = SuKien(n.mo, n.dong, khung)
        if ch_tp:
            self._ket("TP", sk)
            while not self.xong and self.kq and cham(n, self.p_tp, L["tp"][self.i_tp]):
                self._ket("TP", sk)  # nấc TP sau chạm cùng nến
            return
        if ch_sl:
            self._ket("SL", sk)
            return
        het_hoan_toan = (self.vao.a == self.vao.b and n.mo >= self.vao.a) or n.mo >= self.vao.b
        if self.kq is None and het_hoan_toan:
            for k, v, f in (("cao", n.h, max), ("thap", n.l, min)):
                c = self.cuc[k]
                if c is None or f(v, c[0]) != c[0]:
                    self.cuc[k] = (v, n.mo)

    def chay(self):
        L = self.L
        goc = [n for n in self.g.nen(self.g.goc) if n.mo >= self.bd]
        if goc and goc[0].mo > self.bd and L["kieu_vao"] != "ngay":
            self.ghi_chu.append(f"mốc bắt đầu {KH.gio_vn(self.bd, True)} nằm giữa nến {self.g.goc} → xét từ nến kế tiếp "
                                f"{KH.gio_vn(goc[0].mo, True)} (bỏ {tg(goc[0].mo - self.bd)})")
        if L["kieu_vao"] == "ngay":
            t0 = L.get("gio_vao") or self.bd
            dau = next((n for n in goc if n.mo >= t0), None)
            if dau is None:
                self.khong_du_lieu = True
                return self
            if dau.mo > t0:
                self.ghi_chu.append(f"giờ vào {KH.gio_vn(t0, True)} nằm giữa nến {self.g.goc} → xét từ nến kế tiếp "
                                    f"{KH.gio_vn(dau.mo, True)} (bỏ {tg(dau.mo - t0)})")
            gv = L.get("gia_vao")
            self._vao(SuKien(dau.mo, dau.mo, self.g.goc, "vào ngay"), gv, None)
            goc = [n for n in goc if n.mo >= dau.mo]
        for n in goc:
            if self.xong:
                break
            self.truoc_moc(n.mo)
            self.buoc(n, self.g.goc)
        if not self.xong:
            self.truoc_moc(self.g.du_lieu_toi())
        return self

    # -- tóm tắt --
    def ket_qua(self):
        """dict đủ A–E cho báo cáo."""
        L, toi = self.L, self.g.du_lieu_toi()
        r = {"toi": toi, "gia_dinh": self.gia_dinh, "ghi_chu": self.ghi_chu, "tp_truoc": self.tp_truoc}
        if self.vao is None:
            if self.khong_du_lieu:
                r["A"] = ("KHONG_DU_LIEU", None)
            elif self.huy:
                r["A"] = ("DA_HUY", self.huy)
            elif self.kq and self.kq[0] == "KHONG_RO":
                r["A"] = ("KHONG_RO", self.kq)
            else:
                r["A"] = ("CHUA_KHOP", None)
            return r
        r["A"] = ("VAO", self.vao)
        r["gia_vao"] = self.gia_vao
        if self.kq is None:
            r["B"] = ("CHUA_NGA_NGU", None, "")
        else:
            r["B"] = self.kq
        r["tp_sau"], r["ra_sau"] = self.tp_sau, self.ra_sau
        # C. MAE / MFE: cực trị trên nến chắc chắn sau lúc vào và trước nến kết quả, cộng mức kết quả
        cao, thap = self.cuc["cao"], self.cuc["thap"]

        def _max(c, v, t):
            return (v, t) if c is None or v > c[0] else c

        def _min(c, v, t):
            return (v, t) if c is None or v < c[0] else c
        if self.kq and self.kq[0] == "TP":
            m, t = L["tp"][0], self.kq[1].a
            if L["chieu"] == "LONG":
                cao = _max(cao, m, t)
            else:
                thap = _min(thap, m, t)
        elif self.kq and self.kq[0] == "SL":
            m, t = L["sl"], self.kq[1].a
            if L["chieu"] == "LONG":
                thap = _min(thap, m, t)
            else:
                cao = _max(cao, m, t)
        r["cao"], r["thap"] = cao, thap
        return r


# ---------------- chuẩn hoá lệnh từ kế hoạch ----------------
def bat_dau_cua(kh):
    """Hồi cứu (phát hành > 24h sau gio_cat) → tính từ gio_cat; trực tiếp → từ gio_phat_hanh."""
    t_cat, t_ph = KH.doc_gio(kh["gio_cat"]), KH.doc_gio(kh["gio_phat_hanh"])
    return t_cat if t_ph - t_cat > 24 * 3600 else t_ph


def lenh_tu_ke_hoach(kh, p):
    ch = p["chieu"]
    L = {"id": p["id"], "chieu": ch, "tp": [KH.muc_tp(p, i) for i in range(len(p["tp"]))],
         "tp_vung": [KH.vung(x) for x in p["tp"]], "ty_le": [x.get("ty_le") for x in p["tp"]],
         "sl": (p.get("sl_cham") or {}).get("gia"), "dong_khi": list(p.get("dong_khi") or []),
         "huy_cham": [(d["phia"], d["gia"]) for d in p.get("huy_truoc_khi_vao") or [] if d["kieu"] == "cham"],
         "huy_dong": [d for d in p.get("huy_truoc_khi_vao") or [] if d["kieu"] == "dong"],
         "het_han_cho": KH.doc_gio(p["het_han_cho"], True) if p.get("het_han_cho") else None,
         "huy_khi_tp_truoc": bool(p.get("huy_khi_tp_truoc")), "han": KH.doc_gio(p["han"], True),
         "kiem_may": bool((p.get("xac_nhan") or {}).get("kiem_may")), "hanh_dong": p["hanh_dong"], "gia_dinh": []}
    hd = p["hanh_dong"]
    if hd == "CHO_VUNG":
        L.update(kieu_vao="vung", vung_vao=KH.vung(p["vao"]), muc_vao=KH.muc_vao(p), phia_vao=KH.phia_nguoc(ch))
        L["gia_dinh"].append(f"lệnh chờ khớp ở mép gần vùng {list(L['vung_vao'])} = {L['muc_vao']} khi giá chạm "
                             "(hoặc giá mở nếu mở đã trong vùng)")
        if not L["kiem_may"]:
            L["gia_dinh"].append("điều kiện vào khung nhỏ (" + ((p.get("xac_nhan") or {}).get("mo_ta") or "—")
                                 + ") KHÔNG kiểm bằng máy → chỉ biết GIÁ CHẠM VÙNG, chưa khẳng định lệnh khớp hợp lệ")
    elif hd == "CHO_XAC_NHAN":
        L.update(kieu_vao="dong", kich_hoat=p["kich_hoat"])
    else:  # VAO_NGAY / GIU
        lu = kh.get("lenh_user") or {}
        gv = KH.vung(p["vao"])[0]
        L.update(kieu_vao="ngay", gia_vao=gv)
        if hd == "GIU" and lu.get("gio_vao"):
            L["gio_vao"] = KH.doc_gio(lu["gio_vao"])
        L["gia_dinh"].append(f"vào ngay: khớp ở giá kế hoạch ghi {gv} tại nến đầu tiên sau mốc bắt đầu")
    L["tp_chu"] = f"chạm mép gần TP {[list(v) for v in L['tp_vung']]}"
    return L


def lenh_view(kh, kv):
    v = kh["view"][kv]
    ch = KH.chieu_cua(v["huong"])
    d = KH.vung(v["dich"])
    return {"id": f"view {kv}", "chieu": ch, "kieu_vao": "ngay", "gia_vao": kh["gia_dong"],
            "tp": [d[0] if ch == "LONG" else d[1]], "tp_vung": [d], "ty_le": [None], "sl": None,
            "dong_khi": [v["sai_khi"]], "han": KH.doc_gio(v["han"], True), "gia_dinh": []}


# ---------------- báo cáo ----------------
def _pct(a, b):
    return f"{(a - b) / b * 100:+.2f}%"


def _han(t_kq, han, toi):
    if t_kq is None:
        return f"chưa tới hạn ({han_chu(han)})" if toi < han else f"QUÁ HẠN ({han_chu(han)}) mà chưa có kết quả"
    if t_kq.b <= han:
        return f"TRONG HẠN ({han_chu(han)})"
    if t_kq.a >= han:
        return f"TRỄ HẠN {tg(t_kq.a - han)} (hạn {han_chu(han)}) — kết quả vẫn giữ nguyên"
    return f"sát hạn (cùng nến với hạn {han_chu(han)})"


def dong_lenh(L, r, bd, ten_lenh="Lệnh"):
    ra = []
    toi = r["toi"]
    a = r["A"]
    tp_tr = r["tp_truoc"]
    if a[0] == "KHONG_DU_LIEU":
        ra.append(f"- A. Kích hoạt: KHÔNG CÓ DỮ LIỆU sau giờ vào (dữ liệu tới {KH.gio_vn(toi)} VN)")
        return ra
    if a[0] == "CHUA_KHOP":
        s = f"CHƯA KHỚP tới hết dữ liệu ({KH.gio_vn(toi)} VN)"
        if tp_tr:
            s += f" · TP đã chạm TRƯỚC khi khớp lúc {tp_tr.chu()} → không tính thắng (lỡ lệnh)"
        ra.append("- A. Kích hoạt: " + s)
        return ra
    if a[0] == "DA_HUY":
        ra.append(f"- A. Kích hoạt: ĐÃ HUỶ trước khi khớp — {a[1][0]} lúc {a[1][1].chu()}")
        if tp_tr:
            ra.append(f"  · TP đã chạm trước đó lúc {tp_tr.chu()} (không tính thắng)")
        return ra
    if a[0] == "KHONG_RO":
        ra.append(f"- A. Kích hoạt: KHÔNG RÕ THỨ TỰ — {a[1][2]} ({a[1][1].chu()})")
        return ra
    sk = a[1]
    if L["kieu_vao"] == "vung":
        s = (f"GIÁ CHẠM VÙNG vào lúc {sk.chu()}" if not L.get("kiem_may") else f"KHỚP lúc {sk.chu()}")
        if not L.get("kiem_may"):
            s += " (điều kiện khung nhỏ chưa kiểm → chưa khẳng định lệnh khớp hợp lệ)"
    elif L["kieu_vao"] == "dong":
        s = f"XÁC NHẬN (nến đóng) lúc {sk.chu()}"
    else:
        s = f"VÀO lúc {sk.chu()}"
    if tp_tr:
        s += (f" · ⚠ TP đã chạm TRƯỚC khi khớp lúc {tp_tr.chu()} → phần đó KHÔNG tính thắng; kết quả dưới chỉ đúng "
              "nếu lệnh chờ vẫn treo sau khi TP đã chạm (kế hoạch không ghi huỷ khi đó)")
    if L.get("han") and sk.a >= L["han"]:
        s += f" · khớp SAU hạn dự báo ({han_chu(L['han'])})"
    ra.append("- A. Kích hoạt: " + s)
    gv = r.get("gia_vao")
    b = r["B"]
    if b[0] == "CHUA_NGA_NGU":
        ra.append(f"- B. Sau khi vào: CHƯA NGÃ NGŨ — chưa chạm TP, SL hay mốc đóng tới {KH.gio_vn(toi)} VN (dữ liệu cuối)")
    elif b[0] == "KHONG_RO":
        ra.append(f"- B. Sau khi vào: KHÔNG RÕ THỨ TỰ — {b[2]} ({b[1].chu()})")
    else:
        chi_tiet = {"TP": f"chạm TP {L['tp'][0]}", "SL": f"chạm SL {L.get('sl')}", "DONG": b[2]}[b[0]]
        ra.append(f"- B. Sau khi vào: **{TEN_KQ[b[0]]}** — {chi_tiet} lúc {b[1].chu()}"
                  + (f" ({b[2]})" if b[0] == "SL" and b[2] else ""))
        for i, s2 in r.get("tp_sau", []):
            ra.append(f"  · phần còn lại: TP{i + 1} {L['tp'][i]} chạm lúc {s2.chu()}")
        if r.get("ra_sau"):
            x = r["ra_sau"]
            ra.append(f"  · phần còn lại: {TEN_KQ.get(x[0], x[0])} lúc {x[1].chu()} {x[2]}")
    # C
    t_kq = b[1] if b[0] in ("TP", "SL", "DONG") else None
    c = []
    if t_kq:
        sai_so = max(t_kq.b - t_kq.a, sk.b - sk.a)
        c.append(f"tới kết quả ≈ {tg(t_kq.a - sk.a)}" + (f" (±{tg(sai_so)})" if sai_so else ""))
    for k, ten in (("thap" if L["chieu"] == "LONG" else "cao", "đi ngược nhất (MAE)"),
                   ("cao" if L["chieu"] == "LONG" else "thap", "đi thuận nhất (MFE)")):
        v = r.get(k)
        if v:
            c.append(f"{ten} {v[0]}" + (f" ({_pct(v[0], gv)})" if gv else "") + f" lúc ~{KH.gio_vn(v[1], True)}")
        elif t_kq:
            c.append(f"{ten}: không đo được (không có nến trọn vẹn giữa lúc vào và kết quả)")
    if not gv:
        c.append("THIẾU giá vào → không tính % lãi/lỗ")
    ra.append("- C. " + (" · ".join(c) if c else "chưa đủ dữ liệu"))
    if L.get("han"):
        ra.append("- E. Hạn: " + _han(t_kq, L["han"], toi))
    for x in r["gia_dinh"]:
        ra.append(f"  · giả định: {x}")
    for x in r["ghi_chu"]:
        ra.append(f"  · ghi chú: {x}")
    return ra


def duong_di(kh, g, bd):
    """D: chặng nào chạm trước (vùng giao [thấp, cao] của nến gốc)."""
    ra, t = [], []
    for c in kh["duong_di"]:
        a, b = KH.vung(c["vung"])
        n = next((x for x in g.nen(g.goc) if x.mo >= bd and x.l <= b and x.h >= a), None)
        t.append(n)
        ra.append(f"  - chặng {c['chang']} {[a, b]}: " + (f"chạm lúc {SuKien(n.mo, n.dong, g.goc).chu()}" if n
                                                          else "chưa chạm"))
    sai = []
    for i in range(1, len(t)):
        if t[i] and (t[i - 1] is None or t[i].mo < t[i - 1].mo):
            sai.append(f"chặng {i + 1} tới trước chặng {i}")
        elif t[i] and t[i - 1] and t[i].mo == t[i - 1].mo:
            sai.append(f"chặng {i} và {i + 1} cùng nến (không rõ thứ tự)")
    dau = ("SAI THỨ TỰ — " + "; ".join(sai)) if sai else (
        "ĐÚNG THỨ TỰ" if t and all(t) else "chưa đủ chặng để xét")
    return [f"- D. Đường đi: {dau}"] + ra, bool(sai)


def bao_cao(kh, g, ten_tep="", khoa_txt="", lenh_user=None):
    bd = bat_dau_cua(kh)
    toi = g.du_lieu_toi()
    che_do = ("hồi cứu (tính từ gio_cat)" if KH.doc_gio(kh["gio_phat_hanh"]) - KH.doc_gio(kh["gio_cat"]) > 24 * 3600
              else "trực tiếp (tính từ gio_phat_hanh)")
    ra = [f"# Chấm kế hoạch {kh['ma']} {kh['khung_hoi']} — nhận định tại T = {kh['gio_cat']} VN", "",
          f"- Kế hoạch: `{ten_tep}` · phát hành {kh['gio_phat_hanh']} · {che_do} · bắt đầu {KH.gio_vn(bd)} VN",
          f"- Khoá: {khoa_txt or '—'}",
          f"- Giá: {g.nguon} · nến gốc {g.goc} · dữ liệu tới {KH.gio_vn(toi)} VN · chấm lúc {KH.bay_gio_vn()} VN",
          f"- Bộ chấm: cham_ke_hoach.py sha256 {KH.sha256_file(__file__)[:12]}"]
    for a, b in g.lung(bd)[:5]:
        ra.append(f"- ⚠ thiếu nến {g.goc} từ {KH.gio_vn(a)} tới {KH.gio_vn(b)} VN")
    for x in g.loi[:3]:
        ra.append(f"- ⚠ lỗi tải nến {x}")
    ra += ["", "## 1. Kết quả LỆNH theo kế hoạch (A kích hoạt · B TP/SL/mốc đóng trước · C thời gian, MAE/MFE · E hạn)"]
    co = False
    for p in kh["ke_hoach"]:
        if p["hanh_dong"] not in KH.CO_VAO:
            ra.append(f"\n### {p['id']} — {p['hanh_dong']} (không có lệnh để chấm)")
            continue
        co = True
        L = lenh_tu_ke_hoach(kh, p)
        r = May(g, L, bd).chay().ket_qua()
        ra.append(f"\n### {p['id']} — {p['chieu']} {p['hanh_dong']} vào {list(KH.vung(p['vao']) or [])} · "
                  f"TP {[list(v) for v in L['tp_vung']]} · ra: "
                  + "; ".join([mo_ta_dk(d) for d in L["dong_khi"]] + ([f"SL chạm {L['sl']}"] if L["sl"] else []))
                  + f" · hạn {p['han']}")
        ra += dong_lenh(L, r, bd)
    if not co:
        ra.append("- (không có kế hoạch lệnh)")
    ra += ["", "## 2. Độ đúng DỰ BÁO (tách khỏi kết quả lệnh) — đích của khung trước hay mốc sai (nến đóng) trước",
           "| Khung | Hướng | Đích | Mốc sai | Kết quả | Lúc | Râu chạm mốc sai (không tính) | Hạn |",
           "|---|---|---|---|---|---|---|---|"]
    dung = False
    for kv in ("H4", "D1", "W1"):
        v = kh["view"][kv]
        if v["huong"] == "PHAN_VAN":
            ra.append(f"| {kv} | PHÂN VÂN | — | chờ {v['cho']} | không chấm hướng | — | — | — |")
            continue
        L = lenh_view(kh, kv)
        m = May(g, L, bd).chay()
        r = m.ket_qua()
        b = r["B"]
        ten = {"TP": "ĐÍCH TRƯỚC", "DONG": "SAI TRƯỚC", "KHONG_RO": "KHÔNG RÕ", "CHUA_NGA_NGU": "CHƯA NGÃ NGŨ"}[b[0]]
        dung = dung or b[0] == "TP"
        s = v["sai_khi"]
        nr = next((x for x in g.nen(g.goc) if x.mo >= bd and cham(x, s["phia"], s["gia"])), None)
        t_kq = b[1] if b[0] in ("TP", "DONG") else None
        ra.append(f"| {kv} | {v.get('nhan') or v['huong']} | {list(KH.vung(v['dich']))} | {mo_ta_dk(s)} | {ten} | "
                  f"{t_kq.chu() if t_kq else '—'} | {SuKien(nr.mo, nr.dong, g.goc).chu() if nr else 'không'} | "
                  f"{_han(t_kq, L['han'], toi)} |")
    dd, sai_thu_tu = duong_di(kh, g, bd)
    ra += [""] + dd
    if dung and sai_thu_tu:
        ra.append("  → ĐÚNG hướng/đích nhưng SAI THỨ TỰ đường đi: kế hoạch vào ở chặng 1 có thể lỡ dù dự báo đích đúng.")
    if lenh_user:
        ra += ["", "## 3. Lệnh của user"] + lenh_user
    ra += ["", "_Quy ước: TP tính khi chạm mép gần; mốc đóng = nến ĐÓNG đúng khung, đủ số cây liên tiếp (râu không tính); "
           "cùng nến → xét 15m/5m/1m, vẫn chung nến → KHÔNG RÕ; hạn chỉ là cột riêng, không đổi kết quả._"]
    return "\n".join(ra)


def cham_user(g, L, cac_gio, bd_txt):
    """Lệnh user: mỗi giờ vào có thể (giờ chính xác → 1; chỉ biết ngày → mọi nến gốc trong ngày), gộp giờ cùng kết quả."""
    ra, thieu = [], []
    if L.get("gia_vao") is None:
        thieu.append("giá vào")
    if len(cac_gio) > 1:
        thieu.append("giờ vào chính xác")
    ra.append(f"- Lệnh: {L['chieu']} · vào {bd_txt} · giá vào {L.get('gia_vao') or 'THIẾU'} · TP "
              f"{[list(v) for v in L['tp_vung']]} · ra: "
              + "; ".join([mo_ta_dk(d) for d in L["dong_khi"]] + ([f"SL chạm {L['sl']}"] if L.get("sl") else []))
              + (f" · TP/mốc lấy theo {L['nguon']}" if L.get("nguon") else ""))
    if thieu:
        ra.append(f"- ⚠ THIẾU {', '.join(thieu)} → chỉ kết luận thứ tự TP / mốc ra theo mức tuyệt đối; không tự điền.")
    nhom = []
    for t in cac_gio:
        L2 = dict(L, gio_vao=t, gia_dinh=[])
        r = May(g, L2, t).chay().ket_qua()
        b = r.get("B", ("KHONG_DU_LIEU", None, ""))
        n_vao = next((n for n in g.nen(g.goc) if n.mo >= t), None)
        phu_thuoc = L.get("gia_vao") is None and n_vao is not None and (
            cham(n_vao, KH.phia_thuan(L["chieu"]), L["tp"][0])
            or (L.get("sl") is not None and cham(n_vao, KH.phia_nguoc(L["chieu"]), L["sl"])))
        khoa = ("PHU_THUOC_GIA", None) if phu_thuoc else (b[0], b[1].a if b[1] else None)
        if nhom and nhom[-1][0] == khoa:
            nhom[-1][2] = t
        else:
            nhom.append([khoa, t, t, "", r, L2])
    for khoa, a, b, canh, r, L2 in nhom:
        kq = r.get("B", ("KHONG_DU_LIEU", None, ""))
        moc = f"vào {KH.gio_vn(a, True)}" + (f" → {KH.gio_vn(b, True)}" if b != a else "")
        if khoa[0] == "PHU_THUOC_GIA":
            ra.append(f"- {moc}: PHỤ THUỘC GIÁ VÀO — nến lúc vào đã chạm mép TP/SL; thiếu giá vào nên không biết lệnh "
                      "vào trên hay dưới mức đó → không kết luận")
            continue
        if kq[0] in ("TP", "SL", "DONG"):
            s = f"**{TEN_KQ[kq[0]]}** lúc {kq[1].chu()}" + (f" — {kq[2]}" if kq[0] == "DONG" else "")
        elif kq[0] == "KHONG_RO":
            s = f"KHÔNG RÕ THỨ TỰ — {kq[2]} ({kq[1].chu()})"
        elif kq[0] == "KHONG_DU_LIEU":
            s = "không có dữ liệu sau giờ vào"
        else:
            s = f"CHƯA NGÃ NGŨ tới {KH.gio_vn(r['toi'])} VN"
        ra.append(f"- {moc}: {s}")
        them = [x[2:] for x in dong_lenh(L2, r, a) if x.startswith(("- C.", "- E.", "  · ghi chú"))]
        if b != a:
            them = [x + " (tính cho giờ vào sớm nhất của nhóm)" if x.startswith("C.") else x for x in them]
        ra += ["  " + x for x in them]
    return ra


# ---------------- trạng thái tới T (cho ke_hoach.py truoc) ----------------
def trang_thai_toi(kh, g):
    """Mỗi dòng 1 view / kế hoạch: đã xảy ra gì tới g.den (chỉ dữ liệu ≤ T)."""
    bd = bat_dau_cua(kh)
    ra = []
    for kv in ("H4", "D1", "W1"):
        v = kh["view"][kv]
        if v["huong"] == "PHAN_VAN":
            continue
        r = May(g, lenh_view(kh, kv), bd).chay().ket_qua()
        b = r["B"]
        s = {"TP": f"đích ĐÃ CHẠM lúc {b[1].chu() if b[1] else ''} (xong việc → xét giữ/đổi)",
             "DONG": f"mốc sai ĐÃ BỊ NẾN ĐÓNG QUA lúc {b[1].chu() if b[1] else ''} (tác động a → xét đổi view)",
             "KHONG_RO": "không rõ thứ tự", "CHUA_NGA_NGU": "chưa chạm đích, chưa sai → view còn hiệu lực"}[b[0]]
        ra.append(f"view {kv}: {s}")
    for p in kh["ke_hoach"]:
        if p["hanh_dong"] not in KH.CO_VAO:
            continue
        r = May(g, lenh_tu_ke_hoach(kh, p), bd).chay().ket_qua()
        a = r["A"]
        if a[0] == "CHUA_KHOP":
            s = "đang CHỜ (chưa chạm vùng vào)" + (" · TP đã chạm trước → lỡ" if r["tp_truoc"] else "")
        elif a[0] == "DA_HUY":
            s = f"ĐÃ HUỶ ({a[1][0]})"
        elif a[0] == "KHONG_RO":
            s = "không rõ thứ tự khớp"
        else:
            b = r["B"]
            s = f"đã chạm vùng/vào lúc {a[1].chu()} → " + (
                "ĐANG CÓ LỆNH (chưa TP/mốc đóng)" if b[0] == "CHUA_NGA_NGU" else f"ĐÃ KẾT THÚC: {TEN_KQ[b[0]]}")
        ra.append(f"kế hoạch {p['id']}: {s}")
    return ra


# ---------------- CLI ----------------
def _dk_tu_chu(s):
    x = s.split()
    return {"khung": x[0], "phia": x[1], "gia": float(x[2]), "so_nen": int(x[3]) if len(x) > 3 else 1}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Chấm kế hoạch v5 theo thứ tự thời gian")
    ap.add_argument("ke_hoach", nargs="?")
    ap.add_argument("--den", help="cắt dữ liệu tại giờ VN này (mặc định: bây giờ)")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--cache", default=str(CACHE_CHAM))
    ap.add_argument("--ghi", action="store_true", help="ghi báo cáo vào bot_v5/ket_qua/ (file mới)")
    ap.add_argument("--ma")
    ap.add_argument("--lenh-user", choices=["LONG", "SHORT"])
    ap.add_argument("--theo", help="id kế hoạch lấy TP / mốc ra cho lệnh user")
    ap.add_argument("--vao-luc")
    ap.add_argument("--vao-ngay")
    ap.add_argument("--gia-vao", type=float)
    ap.add_argument("--tp", action="append", default=[])
    ap.add_argument("--sl", type=float)
    ap.add_argument("--dong-khi", action="append", default=[])
    ap.add_argument("--han")
    a = ap.parse_args(argv)
    den = KH.doc_gio(a.den) if a.den else int(dt.datetime.now(dt.timezone.utc).timestamp())
    kh, ten, khoa_txt = None, "", ""
    if a.ke_hoach:
        p = Path(a.ke_hoach)
        kh = json.loads(p.read_text(encoding="utf-8"))
        loi, _cb, _tt = KH.kiem(kh)
        if loi:
            print("Kế hoạch không hợp lệ:\n" + "\n".join("  - " + x for x in loi), file=sys.stderr)
            return 1
        ten = str(p)
        ok, ly_do = KH.kiem_khoa(p, p.parent)
        khoa_txt = (f"git {kh['khoa']['git'][:12]}, {ly_do}" if kh.get("khoa") else "") or ly_do
        if not ok:
            khoa_txt = "⚠ " + khoa_txt
    ma = (kh or {}).get("ma") or (a.ma or "").upper()
    if not ma:
        print("Cần file kế hoạch hoặc --ma", file=sys.stderr)
        return 2
    # lệnh user
    user_txt, gio_user = None, []
    if a.lenh_user or a.vao_luc or a.vao_ngay or a.gia_vao:
        if not a.lenh_user:
            print("THIẾU chiều lệnh (--lenh-user LONG|SHORT) — không tự đoán.", file=sys.stderr)
            return 2
        if not (a.vao_luc or a.vao_ngay):
            print("THIẾU giờ vào (--vao-luc hoặc --vao-ngay) — không tự giả định giờ vào.", file=sys.stderr)
            return 2
        if a.theo:
            q = next((x for x in (kh or {}).get("ke_hoach", []) if x["id"] == a.theo), None)
            if q is None:
                print(f"không có kế hoạch id {a.theo}", file=sys.stderr)
                return 2
            L = lenh_tu_ke_hoach(kh, q)
            L.update(chieu=a.lenh_user, kieu_vao="ngay", gia_vao=a.gia_vao, gia_dinh=[],
                     nguon=f"kế hoạch {a.theo} (user chưa nêu TP/mốc riêng)")
            if a.lenh_user != q["chieu"]:
                print("Chiều lệnh user ngược kế hoạch được dẫn — TP/mốc ra không dùng chung được.", file=sys.stderr)
                return 2
        else:
            tps = [KH.vung([float(x) for x in s.split("-")] if "-" in s[1:] else float(s)) for s in a.tp]
            if not tps or (a.sl is None and not a.dong_khi):
                print("Lệnh user không theo kế hoạch: cần --tp và --sl hoặc --dong-khi.", file=sys.stderr)
                return 2
            L = {"chieu": a.lenh_user, "kieu_vao": "ngay", "gia_vao": a.gia_vao, "tp_vung": tps,
                 "tp": [t[0] if a.lenh_user == "LONG" else t[1] for t in tps], "ty_le": [None] * len(tps),
                 "sl": a.sl, "dong_khi": [_dk_tu_chu(s) for s in a.dong_khi],
                 "han": KH.doc_gio(a.han, True) if a.han else None, "gia_dinh": []}
        if a.vao_luc:
            gio_user, bd_txt = [KH.doc_gio(a.vao_luc)], a.vao_luc
        else:
            t0 = KH.doc_gio(a.vao_ngay)
            gio_user, bd_txt = list(range(t0, t0 + 86400, 3600)), f"ngày {a.vao_ngay} (không rõ giờ)"
    moc = ([bat_dau_cua(kh)] if kh else []) + gio_user
    if not moc:
        print("Không có file kế hoạch thì cần lệnh user (--lenh-user + giờ vào).", file=sys.stderr)
        return 2
    g = Gia(ma, min(moc) - 7 * 86400, den, a.cache, a.offline)
    if not g.nen(g.goc):
        print(f"Không có dữ liệu giá {ma} cho khoảng cần chấm (offline: {a.offline}).", file=sys.stderr)
        return 1
    if gio_user:
        user_txt = cham_user(g, L, [t for t in gio_user if t < g.du_lieu_toi()], bd_txt)
    if kh:
        txt = bao_cao(kh, g, ten, khoa_txt, user_txt)
    else:
        txt = "\n".join([f"# Lệnh user {ma}", f"- Giá: {g.nguon} · dữ liệu tới {KH.gio_vn(g.du_lieu_toi())} VN"]
                        + user_txt)
    print(txt)
    if a.ghi:
        stem = Path(a.ke_hoach).stem if a.ke_hoach else f"user_{ma}"
        KET_QUA.mkdir(exist_ok=True)
        out = KET_QUA / f"{stem}__toi_{dt.datetime.fromtimestamp(g.du_lieu_toi(), KH.VN).strftime('%Y%m%d_%H%M')}.md"
        if out.exists():
            print(f"\n(không ghi: {out} đã có — kết quả cũ không bị ghi đè)", file=sys.stderr)
            return 0
        out.write_text(txt + "\n\n## Phân loại lỗi (điền tay — không sửa phần trên)\n"
                       "- Nhóm: dữ liệu/rút nhãn · bắt chước (lệch người hình mẫu cùng T — chỉ khi có buổi live) · "
                       "dự báo (hướng / đích / đường đi / hạn) · thực thi (vào / chốt / đóng)\n- Ghi chú:\n",
                       encoding="utf-8")
        print(f"\nĐã ghi {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
