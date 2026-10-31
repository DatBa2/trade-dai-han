#!/usr/bin/env python3
"""Phan tich GIU / LAT view H4 cua nguoi do -> GIU_LAT.md + LUAT_KHOA.md.

(a) Tong quan TOAN BO 180 buoi (bang chuyen, dieu kien giu/lat, loi nguoi do, PHAN VAN, do rong vung, trung han, tin tuc).
(b) Kiem theo thoi gian: luat CHON chi tren tap HOC (buoi < 2026-07-01; so luat K chon bang kiem cheo thoi gian TRONG tap
    hoc), roi DO tren tap KIEM (buoi >= 2026-07-01) so voi moc so sanh tren cung buoi.
Mo hinh: mac dinh GIU view (huong TANG/GIAM gan nhat cua nguoi do); <= 5 luat "neu <dieu kien> thi LAT | PHAN VAN".
Dieu kien chi lay tu LOI / HANH VI cua nguoi do: dieu kien vao mo hinh khi >= 3 buoi TAP HOC nguoi do noi ve no (regex
tren cau trich trong nhan), hoac la hanh vi cua chinh ho o buoi truoc. Dieu kien '—' (khong phai loi ho) chi de mo ta.
Dau vao: dac_trung_<nguon>.csv + nhan_<nguon>.json (dac_trung.py). Khong doc thi/bai_lam/, thi/KET_QUA_THI.md.
Cach dung: python3 hoc_v5/giu_lat/phan_tich.py [--nhan moi|cu]
"""
import csv, datetime as dt, hashlib, json, re, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path

RA = Path(__file__).resolve().parent
GOC = RA.parents[1]
sys.path.insert(0, str(RA))
import dac_trung as dtg  # noqa: E402

NHAN = ["TANG", "GIAM", "PHAN_VAN"]
VIET = {"TANG": "TĂNG", "GIAM": "GIẢM", "PHAN_VAN": "PHÂN VÂN", None: "—", "": "—"}
DAU = {"TANG": 1, "GIAM": -1}
NGUOC = {"TANG": "GIAM", "GIAM": "TANG"}
MIN_LOI = 3        # so buoi TAP HOC toi thieu nguoi do noi ve 1 dieu kien de duoc dua vao mo hinh
MIN_GAIN = 2       # luat moi phai lam dung them >= 2 buoi tren tap dang hoc
MIN_HO_TRO = 4     # ... va phai khop >= 4 buoi (chua bi luat truoc bat) tren tap dang hoc
K_TOI_DA = 5
MOC = ["Giữ view", "Luôn GIẢM", "Luật từ trên xuống", "Chép buổi trước"]


def kd(s):
    return dtg.khong_dau(s or "").lower()


def so(x):
    if x in (None, ""):
        return None
    try:
        return float(x)
    except ValueError:
        return x


def ty(a, b):
    return f"{a}/{b} = {100 * a / b:.0f}%" if b else f"{a}/0"


def pt(a, b):
    return f"{100 * a / b:.0f}%" if b else "—"


def pct(xs, q):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    f = int(k)
    return xs[f] + (xs[min(f + 1, len(xs) - 1)] - xs[f]) * (k - f)


def cat(s, n=170):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[:n - 1] + "…"


# ───────────────────────── dieu kien (theo view) ─────────────────────────
def _sai_phia(r, cot):
    s, v = DAU.get(r["view"]), r.get(cot)
    if s is None or v is None:
        return None
    return v == -s


def _rsi_cuc(r, cot):
    s, v = DAU.get(r["view"]), r.get(cot)
    if s is None or v is None:
        return None
    return v >= 70 if s > 0 else v <= 30


def _co(r, cot):
    v = r.get(cot)
    return None if v is None else bool(v)


def _nguong(cot, nguong):
    return lambda r: None if r.get(cot) is None else r[cot] >= nguong


def _pm_moi_truong(r):
    s, a, b = DAU.get(r["view"]), r.get("pm_tang"), r.get("pm_giam")
    if s is None or a is None:
        return None
    return a >= 30 if s > 0 else b >= 30


def _pm_7n(r):
    s, v = DAU.get(r["view"]), r.get("pm_noi_long_d7")
    if s is None or v is None:
        return None
    return v <= -10 if s > 0 else v >= 10


def _pm_nguoc(r):
    s, v = DAU.get(r["view"]), r.get("pm_doi")
    if s is None or v is None:
        return None
    return v <= -5 if s > 0 else v >= 5


RX_VOL = r"\bvol(ume)?\b|khoi luong"
RX_PM = r"polymarket|xac suat|(tang|giam|cat|nang) lai suat|lai suat (tang|giam)|dong tien (dat|re)"
RX_MA = lambda n: rf"\b(e?ma) ?{n}\b"  # noqa: E731
RX_TIN = r"\bcpi\b|\bfomc\b|\bfed\b|non ?farm|\bnfp\b|lai suat|bang luong|\bppi\b|\bpce\b|tin (tuc|vi mo)"
# (ma, nhom, mo ta, ham(r) -> True/False/None, regex LOI nguoi do (khong dau, thuong) | "hanh_vi" | None = khong phai loi ho)
DK = [
    ("vh_cham_rau", "Mốc sai & đích", "Râu chạm/qua mốc sai buổi trước (chưa cần đóng)", lambda r: _co(r, "vh_cham_rau"),
     r"\brau\b[^.]{0,40}(cham|quet|qua|test|khong tinh|chua tinh)|(cham|quet)[^.]{0,20}\brau\b"),
    ("vh_dong_1h4", "Mốc sai & đích", "≥ 1 nến H4 ĐÓNG qua mốc sai buổi trước", lambda r: _co(r, "vh_dong_1h4"),
     r"\bh4\b[^.]{0,30}dong (tren|duoi|qua|gay|xuyen|ra)|dong (cua )?(cay |nen )?\bh4\b|(cay|nen) h4 (nao )?dong"),
    ("vh_dong_2h4", "Mốc sai & đích", "2 nến H4 liên tiếp đóng qua mốc sai", lambda r: _co(r, "vh_dong_2h4"),
     r"(2|hai) (cay|nen) (h4|4 ?h)|(2|hai) cay[^.]{0,12}dong"),
    ("vh_dong_dung_khung", "Mốc sai & đích", "Đóng qua mốc sai ĐÚNG khung + số nến họ nói", lambda r: _co(r, "vh_dong_dung_khung"),
     r"(\bh[14]\b|\bd1\b|nen ngay|cay ngay|nen tuan|cay tuan|khung ngay|khung tuan|\bm(15|30)\b)[^.]{0,30}dong (tren|duoi|qua|gay|xuyen|ra)"),
    ("vh_dong_d1", "Mốc sai & đích", "Nến D1 đóng qua mốc sai buổi trước", lambda r: _co(r, "vh_dong_d1"),
     r"(nen|cay|khung) ngay[^.]{0,30}dong (tren|duoi|qua|gay|xuyen|ra)|dong cua ngay|\bd1\b[^.]{0,20}dong"),
    ("vh_ben_kia", "Mốc sai & đích", "Lúc C giá vẫn ở bên kia mốc sai", lambda r: _co(r, "vh_ben_kia_luc_C"),
     r"(da|vua) (thung|pha|vuot|gay|mat)\b|thung (roi|xong)|pha (roi|xong)"),
    ("vh_dong_vol", "Nến & volume", "Nến H4 phá mốc sai CÓ volume (≥ 1,5 × TB20)",
     lambda r: None if r.get("vh_dong_1h4") is None else bool(r["vh_dong_1h4"] and (r.get("vh_vol_tb20") or 0) >= 1.5), RX_VOL),
    ("cham_dich", "Mốc sai & đích", "Râu chạm ĐÍCH chính buổi trước", lambda r: _co(r, "cham_dich_truoc"),
     r"(cham|ve|dat|toi|den|an) (duoc )?(dich|target|muc tieu|\btp\b)|chot (loi|lai|lenh)|da (ve|len|xuong) (den |toi )?\d"),
    ("cham_chang1", "Mốc sai & đích", "Râu chạm đích CHẶNG KẾ TIẾP buổi trước", lambda r: _co(r, "cham_chang1_truoc"),
     r"(cham|ve|dat|toi|den) (duoc )?(dich|target|vung)|da (ve|len|xuong) (den |toi )?\d"),
    ("h4_lon_nguoc", "Nến & volume", "Có nến H4 thân ≥ 1,5 ATR NGƯỢC view", lambda r: _co(r, "h4_lon_nguoc"),
     r"(cay|nen) (h4 )?(do |xanh )?(rat |qua )?(to|lon|manh|dai|khung)\b|(cay|nen) (dap|dam|xa)|dap (xuong|len)"),
    ("h4_lon_nguoc_vol", "Nến & volume", "Nến H4 lớn ngược view có volume ≥ 1,5 × TB20",
     lambda r: None if r.get("h4_lon_nguoc") is None else bool(r["h4_lon_nguoc"] and (r.get("h4_lon_nguoc_vol") or 0) >= 1.5), RX_VOL),
    ("vol_h4_nguoc", "Nến & volume", "Nến H4 volume lớn nhất (≥ 2 × TB20) là nến NGƯỢC view",
     lambda r: None if r.get("vol_h4_max_nguoc") is None else bool(r["vol_h4_max_nguoc"] and (r.get("vol_h4_max_tb20") or 0) >= 2), RX_VOL),
    ("vol_d1_lon", "Nến & volume", "Có nến D1 volume ≥ 1,5 × TB20 (mọi màu)", _nguong("vol_d1_max_tb20", 1.5), RX_VOL),
    ("d1_nhan_chim_nguoc", "Nến & volume", "Nến D1 NHẤN CHÌM ngược view", lambda r: _co(r, "d1_nhan_chim_nguoc"),
     r"nhan chim|engulf|bao trum|nuot"),
    ("d1_cuoi_nguoc", "Nến & volume", "Nến D1 đóng gần nhất NGƯỢC màu view", lambda r: _co(r, "d1_cuoi_nguoc"),
     r"(nen|cay) ngay (mau )?(do|xanh)|\bd1\b (dong )?(do|xanh)|ngay[^.]{0,10}dong (mau )?(do|xanh)"),
    ("thu_hai", "Lịch", "Buổi thứ Hai", lambda r: bool(r.get("thu_hai")), r"thu hai|dau tuan|nen tuan|dong (cua )?tuan"),
    ("dau_tuan", "Lịch", "Buổi đầu tuần (buổi đầu của tuần ISO)", lambda r: _co(r, "dau_tuan"), r"thu hai|dau tuan|nen tuan|dong (cua )?tuan"),
    ("dau_thang", "Lịch", "Buổi đầu tháng", lambda r: _co(r, "dau_thang"), r"dau thang|nen thang|dong (cua )?thang|khung thang"),
    ("h4_sai_dai34", "EMA / RSI / pha", "Giá H4 ngoài dải EMA34 phía SAI view", lambda r: _sai_phia(r, "h4_vs_dai34"), RX_MA(34)),
    ("h4_sai_e89", "EMA / RSI / pha", "Giá H4 sai phía EMA89", lambda r: _sai_phia(r, "h4_vs_e89"), RX_MA(89)),
    ("h4_sai_e200", "EMA / RSI / pha", "Giá H4 sai phía EMA200", lambda r: _sai_phia(r, "h4_vs_e200"), RX_MA(200)),
    ("d1_sai_dai34", "EMA / RSI / pha", "Giá D1 ngoài dải EMA34 phía SAI view", lambda r: _sai_phia(r, "d1_vs_dai34"), RX_MA(34)),
    ("d1_sai_e89", "EMA / RSI / pha", "Giá D1 sai phía EMA89", lambda r: _sai_phia(r, "d1_vs_e89"), RX_MA(89)),
    ("d1_sai_e200", "EMA / RSI / pha", "Giá D1 sai phía EMA200", lambda r: _sai_phia(r, "d1_vs_e200"), RX_MA(200)),
    ("rsi_h4_cuc", "EMA / RSI / pha", "RSI H4 quá mua/bán THEO chiều view (TĂNG ≥ 70 / GIẢM ≤ 30)", lambda r: _rsi_cuc(r, "rsi_h4"),
     r"\brsi\b|qua mua|qua ban"),
    ("rsi_d1_cuc", "EMA / RSI / pha", "RSI D1 quá mua/bán THEO chiều view", lambda r: _rsi_cuc(r, "rsi_d1"), r"\brsi\b|qua mua|qua ban"),
    ("nguoc_pha_w1", "EMA / RSI / pha", "View ngược pha W1 (bot_v4 TK 3)",
     lambda r: None if not r.get("pha_w1") or not r.get("view") else r["pha_w1"] != r["view"],
     r"khung tuan|nen tuan|\bw1\b|chu ky|xu huong (chinh|lon)"),
    ("chum_h4", "EMA / RSI / pha", "EMA34/89/200 H4 chụm < 0,6% giá", lambda r: None if r.get("chum_h4_pct") is None else r["chum_h4_pct"] < 0.6,
     r"(\bma\b|duong ma|\bema\b)[^.]{0,30}(chum|xoan|dan xen|quan|sat nhau|cat nhau)|di ngang|sideway|tich luy"),
    ("tin_lon_giua", "Tin tức", "Có tin lớn (FOMC/CPI/NFP) ra GIỮA 2 buổi (sau tin)", lambda r: _co(r, "tin_lon_giua"), RX_TIN),
    ("tin_lon_sap24", "Tin tức", "Có tin lớn trong 24 giờ SAU C (trước tin, thường tối cùng ngày)", lambda r: _co(r, "tin_lon_sap24"), RX_TIN),
    ("tin_lon_sap48", "Tin tức", "Có tin lớn trong 48 giờ sau C", lambda r: _co(r, "tin_lon_sap48"), RX_TIN),
    ("cua_so_fomc", "Tin tức", "Trong cửa sổ FOMC (≤ 72h trước / ≤ 24h sau quyết định)", lambda r: _co(r, "cua_so_fomc"),
     r"\bfomc\b|\bfed\b|lai suat|powell|chu tich"),
    ("pm_moi_truong_nguoc", "Tin tức", "Polymarket kỳ Fed tới ngược view: view TĂNG mà P(tăng lãi suất) ≥ 30%, view GIẢM mà P(giảm) ≥ 30%",
     _pm_moi_truong, RX_PM),
    ("pm_7n_nguoc", "Tin tức", "Polymarket 7 ngày: (P giảm − P tăng lãi suất) đổi ≥ 10 điểm NGƯỢC view", _pm_7n, RX_PM),
    ("pm_nguoc", "Tin tức", "Polymarket từ buổi trước: (P giảm − P tăng) đổi ≥ 5 điểm NGƯỢC view", _pm_nguoc, RX_PM),
    ("truoc_nhac_tin", "Tin tức", "Buổi trước người đó có nhắc tin tức", lambda r: _co(r, "truoc_nhac_tin"), "hanh_vi"),
    ("truoc_cho_tin", "Tin tức", "Buổi trước người đó dặn chờ/né tin", lambda r: _co(r, "truoc_cho_tin"), "hanh_vi"),
    ("truoc_pv", "Hành vi buổi trước", "Buổi trước người đó PHÂN VÂN",
     lambda r: None if not r.get("nhan_truoc") else r["nhan_truoc"] == "PHAN_VAN", "hanh_vi"),
    ("truoc_chac_thap", "Hành vi buổi trước", "Buổi trước người đó nói độ chắc THẤP",
     lambda r: None if not r.get("do_chac_truoc") else r["do_chac_truoc"] == "thap", "hanh_vi"),
    ("truoc_doi_y", "Hành vi buổi trước", "Buổi trước người đó đã đổi ý giữa buổi", lambda r: _co(r, "doi_y_truoc"), "hanh_vi"),
    ("truoc_chang1_nguoc", "Hành vi buổi trước", "Buổi trước có chặng kế tiếp NGƯỢC view (chờ hồi)", lambda r: _co(r, "chang1_nguoc_truoc"), "hanh_vi"),
    ("di_nguoc_2", "Giá đi (mô tả)", "Giá đi ngược view ≥ 2% từ C buổi trước",
     lambda r: None if r.get("di_theo_view") is None else r["di_theo_view"] <= -2, None),
    ("nguoc_max_3", "Giá đi (mô tả)", "Có lúc giá đi ngược view ≥ 3% giữa 2 buổi", _nguong("nguoc_max", 3), None),
    ("di_thuan_2", "Giá đi (mô tả)", "Giá đi THEO view ≥ 2% từ C buổi trước",
     lambda r: None if r.get("di_theo_view") is None else r["di_theo_view"] >= 2, None),
    ("qua_cuoi_tuan", "Giá đi (mô tả)", "Cách buổi trước ≥ 48 giờ", _nguong("gio_tu_truoc", 48), None),
    ("tren_xuong_khac", "Giá đi (mô tả)", "Luật từ trên xuống cho hướng khác view",
     lambda r: None if r.get("luat_tren_xuong") not in DAU or not r.get("view") else r["luat_tren_xuong"] != r["view"], None),
]
RX_TL = r"trend ?line|duong xu huong"
DK_TL = [
    ("tl_pha_nguoc", "Trendline", "Trendline chính (H4/D1) bị phá NGƯỢC view giữa 2 buổi (đóng H4; trừ phá giả đã biết)",
     lambda r: _co(r, "tl_pha_nguoc"), RX_TL),
    ("tl_pha_nguoc_h4", "Trendline", "… trendline H4 bị phá ngược view", lambda r: _co(r, "tl_pha_nguoc_h4"), RX_TL),
    ("tl_pha_nguoc_d1", "Trendline", "… trendline D1 bị phá ngược view", lambda r: _co(r, "tl_pha_nguoc_d1"), RX_TL),
    ("tl_pha_nguoc_2nen", "Trendline", "… phá ngược view bằng 2 nến H4", lambda r: _co(r, "tl_pha_nguoc_2nen"),
     r"(2|hai) (cay|nen) (h4|4 ?h)|(2|hai) cay[^.]{0,12}(vuot|dong)"),
    ("tl_pha_nguoc_vol", "Trendline", "… phá ngược view có volume ≥ 1,5 × TB20",
     lambda r: None if r.get("tl_pha_nguoc") is None else bool(r["tl_pha_nguoc"] and (r.get("tl_pha_nguoc_vol") or 0) >= 1.5), RX_VOL),
    ("tl_pha_thuan", "Trendline", "Trendline chính bị phá THEO view", lambda r: _co(r, "tl_pha_thuan"), RX_TL),
]
DK_MAP, MO_TA = {}, {}


# ───────────────────────── loi nguoi do ─────────────────────────
HANG_NGUON = {"nhin_lai.trich": 0, "vo_hieu.cau": 1, "nen_volume": 2, "trich_them": 3, "tin_tuc": 3, "trich_cuoi": 4,
              "trich_dau": 4, "view_trung_han": 4, "giu_dong": 5, "ly_do_doi_y": 6, "khung_lon": 7, "trendline": 7,
              "nhin_lai.vi_sao": 8}


def van_ban_buoi(n):
    """Moi loi nguoi do (cau trich + dien giai) cua 1 nhan -> [(nguon, gio, cau)]."""
    ra = []
    nl = n.get("nhin_lai") or {}
    for k in ("trich", "vi_sao"):
        if nl.get(k):
            ra.append(("nhin_lai." + k, nl.get("gio"), nl[k]))
    if n.get("ly_do_doi_y"):
        x = n["ly_do_doi_y"]
        ra.append(("ly_do_doi_y", None, x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)))
    for k in ("trich_dau", "trich_cuoi"):
        if n.get(k):
            ra.append((k, n.get("gio_" + k[6:]), n[k]))
    if n.get("vo_hieu") and n["vo_hieu"].get("cau"):
        ra.append(("vo_hieu.cau", None, n["vo_hieu"]["cau"]))
    for k, f in (("trich_them", "cau"), ("nen_volume", "trich"), ("tin_tuc", "trich"), ("view_trung_han", "trich"),
                 ("giu_dong", "trich")):
        for x in n.get(k) or []:
            if isinstance(x, dict) and x.get(f):
                ra.append((k, x.get("gio"), x[f]))
    for k, v in (n.get("khung_lon") or {}).items():
        if isinstance(v, str):
            ra.append(("khung_lon." + k, None, v))
    for x in n.get("trendline") or []:
        if isinstance(x, dict) and x.get("noi_tu"):
            ra.append(("trendline", None, "trendline " + str(x["noi_tu"])))
    return ra


def bang_chung_loi(nhan, regex):
    """(so buoi co loi khop regex, cau vi du tot nhat (ngay, gio, cau))."""
    if regex in (None, "hanh_vi"):
        return None, None
    m = re.compile(regex)
    so_buoi, tot = 0, None
    for ten, n in sorted(nhan.items()):
        trung = [(HANG_NGUON.get(ng.split(".")[0] if ng.startswith("khung_lon") else ng, 9), g is None, ng, g, c)
                 for ng, g, c in van_ban_buoi(n) if m.search(kd(c))]
        if trung:
            so_buoi += 1
            x = min(trung)
            if tot is None or x[:2] < tot[0]:
                tot = (x[:2], (ten[:10], x[3], x[4]))
    return so_buoi, (tot[1] if tot else None)


# ───────────────────────── mo hinh luat ─────────────────────────
def du_doan(r, luat):
    for ma, hanh in luat:
        if DK_MAP[ma](r) is True:
            return NGUOC[r["view"]] if hanh == "LAT" else "PHAN_VAN"
    return r["view"]


def hoc_luat(rows, ung, K):
    """Tham lam, them luat vao CUOI danh sach (luat truoc uu tien). Nhanh: tinh truoc tap buoi moi dieu kien khop."""
    khop = {ma: [i for i, r in enumerate(rows) if DK_MAP[ma](r) is True] for ma in ung}
    y = [r["nhan"] for r in rows]
    du = [r["view"] for r in rows]
    da = [False] * len(rows)
    luat = []
    for _ in range(K):
        tot = None
        for ma in ung:
            idx = [i for i in khop[ma] if not da[i]]
            if len(idx) < MIN_HO_TRO:
                continue
            truoc = sum(du[i] == y[i] for i in idx)
            for hanh in ("LAT", "PHAN_VAN"):
                sau = sum((NGUOC[rows[i]["view"]] if hanh == "LAT" else "PHAN_VAN") == y[i] for i in idx)
                k = (sau - truoc, -ma.count("&"), len(khop[ma]))
                if tot is None or k > tot[0]:
                    tot = (k, ma, hanh, idx)
        if tot is None or tot[0][0] < MIN_GAIN:
            break
        _, ma, hanh, idx = tot
        for i in idx:
            da[i] = True
            du[i] = NGUOC[rows[i]["view"]] if hanh == "LAT" else "PHAN_VAN"
        luat.append((ma, hanh))
    return luat


def moc_so(r):
    return {"Giữ view": r["view"], "Luôn GIẢM": "GIAM", "Luật từ trên xuống": r["luat_tren_xuong"],
            "Chép buổi trước": r["nhan_truoc"]}


def ten_luat(lu):
    return "; ".join(f"{MO_TA[ma]} → {'LẬT' if h == 'LAT' else 'PHÂN VÂN'}" for ma, h in lu) or "(không luật — giữ view)"


def dong_so_sanh(ten, ds, du_fn):
    d = [ten, str(len(ds)), ty(sum(du_fn(r) == r["nhan"] for r in ds), len(ds))]
    for k in MOC:
        d.append(ty(sum(moc_so(r)[k] == r["nhan"] for r in ds), len(ds)))
    return "| " + " | ".join(d) + " |"


HEAD_SS = ["| Lượt | n | Bộ luật | Giữ view | Luôn GIẢM | Luật từ trên xuống | Chép buổi trước |",
           "|---|---|---|---|---|---|---|"]


# ───────────────────────── nhom ly do ─────────────────────────
KHONG = r"(?<!chua )(?<!khong )(?<!chua bi )"
NHOM_LY_DO = [  # regex tren `vi_sao` (tom tat ly do nguoi do tu noi), khong dau
    ("Đi đúng kịch bản / plan chưa bị tác động", r"dung (kich ban|ke hoach|view|huong|du doan|bai|plan)|chua (bi )?tac dong|giu nguyen|"
     r"khong (co gi )?(khac|moi|thay doi)|nhu hom qua|van the|chay dung|di dung"),
    ("Cấu trúc đỉnh/đáy, hỗ trợ chưa gãy", r"(dinh|day)[^.]{0,20}(cao dan|thap dan|nang)|cau truc[^.]{0,20}(chua|khong) (doi|thay doi|gay)|"
     r"chua (thung|pha|gay|vuot|doi)|khong (thung|gay)|giu (duoc )?(ho tro|vung|day|cau truc|xu huong)"),
    ("Nến ĐÓNG xấu / thủng / gãy mốc (đã xảy ra)", KHONG + r"\b(thung|gay|pha vo|break|rot)\b|dong (h4|nen|d1|cay|nen ngay|nen tuan)?[^.]{0,12}"
     r"(xau|tren|duoi|vuot)|cum nen dao chieu|bi tu choi|fail"),
    ("Nến tuần/ngày (khung lớn) quyết định", r"nen (tuan|ngay|thang)|khung (ngay|tuan|lon)|\bd1\b|\bw1\b|xu huong (chinh|lon)"),
    ("Chạm đích / hoàn thành mục tiêu", r"cham (dich|tp|muc tieu|target|vung)|(hoan thanh|hoan tat|dat|xong|full) (het )?(target|muc tieu|tp)|"
     r"chot (loi|lai|lenh|xong|het)|da (ve|len) (dung|toi|den)"),
    ("Nhịp ngược chỉ là hồi / quét / trap / fake", r"chi la (hoi|dieu chinh|quet|nhip|phan ung|retest|gap)|\btrap\b|fake|quet (sl|stop|liquid|long|short)|"
     r"kill (long|short)|du (long|short)|hoi ky thuat|retest|hoi quang"),
    ("MA / Fibo / gap (vùng kỹ thuật)", r"\bma ?(34|89|200)?\b|\bema\b|fibo|\bgap\b"),
    ("Nến đảo chiều / lực mua bán / volume", r"dao chieu|nhan chim|rut (chan|rau)|\brau\b|cum nen|cap nen|luc (mua|ban|tang)|volume|no luc"),
    ("Tin tức / vĩ mô", RX_TIN + r"|tin (trump|tuc)|\btin\b|iran|chien su"),
    ("Tâm lý / thanh lý / Fear&Greed", r"fear|greed|thanh ly|liquid|tam ly|coinglass|hyblock|short (dong|tich luy)|fomo|bi quan"),
    ("Đầu tuần / tháng xem lại khung lớn", r"dau (tuan|thang)|thu hai|nen tuan dong"),
]


def loai_gd(nl):
    g = kd(str((nl or {}).get("giu_hay_doi") or ""))
    return "giu" if g.startswith("giu") else ("doi" if g.startswith("doi") or "lat" in g else None)


def nhom_ly_do(nhan):
    ra = {ten: {"giu": [], "doi": []} for ten, _ in NHOM_LY_DO}
    tong, kn = Counter(), {"giu": [], "doi": []}
    for t, n in sorted(nhan.items()):
        nl = n.get("nhin_lai") or {}
        loai = loai_gd(nl)
        if loai is None:
            continue
        tong[loai] += 1
        vb = kd(nl.get("vi_sao") or nl.get("trich") or "")
        co = False
        for ten, rx in NHOM_LY_DO:
            if re.search(rx, vb):
                ra[ten][loai].append((t[:10], nl.get("gio"), nl.get("trich") or nl.get("vi_sao"), nl.get("view_truoc")))
                co = True
        if not co:
            kn[loai].append(t[:10])
    return ra, tong, kn


# ───────────────────────── chinh ─────────────────────────
def doc(nguon):
    rows = [{k: so(v) for k, v in r.items()} for r in csv.DictReader((RA / f"dac_trung_{nguon}.csv").open(encoding="utf-8"))]
    for r in rows:
        for k in ("nhan", "nhan_dau", "view", "nhan_truoc", "luat_tren_xuong", "pha_w1", "do_chac_truoc", "tap"):
            r[k] = r.get(k) or None
        r["thang"] = str(r["thang"])
    meta = json.loads((RA / f"nhan_{nguon}.json").read_text(encoding="utf-8"))
    return rows, meta


def ket_qua(r):
    return "GIU" if r["nhan"] == r["view"] else ("PV" if r["nhan"] == "PHAN_VAN" else "LAT")


def main():
    a = sys.argv[1:]
    nguon = a[a.index("--nhan") + 1] if "--nhan" in a else ("moi" if (RA / "dac_trung_moi.csv").exists() else "cu")
    rows, meta = doc(nguon)
    nhan = meta["nhan"]
    nhan_hoc = {t: n for t, n in nhan.items() if t[:10] < dtg.TU_THI}
    ds_dk = DK + (DK_TL if meta.get("trendline") else [])
    thu_tu_nhom = list(dict.fromkeys(x[1] for x in ds_dk))
    ds_dk = sorted(ds_dk, key=lambda x: thu_tu_nhom.index(x[1]))  # gom theo nhom (sort on dinh)
    for ma, _, mo, f, _ in ds_dk:
        DK_MAP[ma], MO_TA[ma] = f, mo
    hop = [r for r in rows if r["view"] in DAU and r["nhan"] in NHAN]
    hoc = [r for r in hop if r["tap"] == "hoc"]
    kiem = [r for r in hop if r["tap"] == "kiem"]
    L = []
    p = L.append
    nn = Counter((r["tap"], r.get("nguon_nhan") or "—") for r in rows if r["nhan"] in NHAN)
    p(f"# GIỮ / LẬT view H4 — toàn bộ {len(rows)} buổi (học < 2026-07-01 · kiểm ≥ 2026-07-01)")
    p("")
    p(f"Tạo lúc {dt.datetime.now():%Y-%m-%d %H:%M} · `python3 hoc_v5/giu_lat/dac_trung.py --nhan {nguon} && "
      f"python3 hoc_v5/giu_lat/phan_tich.py --nhan {nguon}`.")
    p(f"Nhãn ({'MỚI' if nguon == 'moi' else 'CŨ phieu/'}): " + ", ".join(f"{t} {k}: {v}" for (t, k), v in sorted(nn.items())) +
      f" → {sum(nn.values())}/{len(rows)} buổi có nhãn hướng. Không đọc `thi/bai_lam/`, `thi/KET_QUA_THI.md`.")
    p("Đặc trưng buổi N chỉ dùng nến đã đóng ≤ C_N (C = bat_dau_vn + phut), nhãn các buổi trước N, lịch tin công bố trước, "
      "Polymarket ≤ C_N. **view** = hướng TĂNG/GIẢM gần nhất của người đó trước N (bỏ PHÂN VÂN) = mốc \"Giữ view\" của "
      "bộ chấm. **GIỮ** = nhãn N = view; **LẬT** = nhãn N ngược view; **PV** = nhãn N PHÂN VÂN.")
    bt = ""
    q = GOC / "hoc_v5" / "trendline" / "CHON.md"
    if q.exists():
        m_ = re.search(r"BIEN_THE_KHOA:\s*`?([^`\n]+)", q.read_text(encoding="utf-8"))
        bt = f", biến thể `{m_[1]}` do agent trendline khoá trên CẢ 180 buổi → đặc trưng trendline ở tập kiểm không hoàn toàn ngoài mẫu" if m_ else ""
    p("Nguồn phụ: trendline " + (f"CÓ (`hoc_v5/trendline/su_kien.csv`{bt})" if meta.get("trendline") else
                                 "**CHƯA CÓ** `hoc_v5/trendline/su_kien.csv` → không có đặc trưng trendline máy (chỉ lời người đó)")
      + "; lịch kinh tế " + ("CÓ (`du_lieu/tin_tuc/lich_kinh_te_2026.csv`)" if meta.get("lich_tin") else "CHƯA CÓ")
      + "; Polymarket " + ("CÓ (`du_lieu/tin_tuc/polymarket_fed.csv`)" if meta.get("polymarket") else "CHƯA CÓ") + ".")
    p("")
    TOM = len(L)  # cho chen tom tat sau

    # ── 1. ma tran chuyen
    p("## 1. Ma trận chuyển nhãn N−1 → N")
    cap = [(r["nhan_truoc"], r["nhan"], r["tap"]) for r in rows if r.get("nhan_truoc") in NHAN and r["nhan"] in NHAN]
    m = Counter((x, y) for x, y, _ in cap)
    p(f"{len(cap)} cặp buổi liền nhau (hàng = N−1, cột = N).")
    p("")
    p("| N−1 \\ N | TĂNG | GIẢM | PHÂN VÂN | Tổng | Giữ nguyên nhãn |")
    p("|---|---|---|---|---|---|")
    for x in NHAN:
        t = sum(m[(x, y)] for y in NHAN)
        p(f"| {VIET[x]} | " + " | ".join(str(m[(x, y)]) for y in NHAN) + f" | {t} | {ty(m[(x, x)], t)} |")
    p(f"| **Tổng** | {sum(m[(x, 'TANG')] for x in NHAN)} | {sum(m[(x, 'GIAM')] for x in NHAN)} | "
      f"{sum(m[(x, 'PHAN_VAN')] for x in NHAN)} | {len(cap)} | **{ty(sum(m[(x, x)] for x in NHAN), len(cap))}** |")
    p("")
    p("So với **view** (hướng gần nhất, bỏ PV), tách tập học / kiểm:")
    p("")
    p("| view trước | Tập | n | GIỮ | LẬT | sang PV |")
    p("|---|---|---|---|---|---|")
    tg = {}
    for v in ("TANG", "GIAM", None):
        for tap, ds in (("tất cả", hop), ("học", hoc), ("kiểm", kiem)):
            d = [r for r in ds if v is None or r["view"] == v]
            c = Counter(ket_qua(r) for r in d)
            if v is None:
                tg[tap] = (c, len(d))
            p(f"| {'**Tất cả**' if v is None else VIET[v]} | {tap} | {len(d)} | {ty(c['GIU'], len(d))} | {ty(c['LAT'], len(d))} | {ty(c['PV'], len(d))} |")
    p("")
    dot, cur, dem = [], None, 0
    for r in rows:
        if r["nhan"] not in NHAN:
            continue
        if r["nhan"] == cur:
            dem += 1
        else:
            if cur:
                dot.append((cur, dem))
            cur, dem = r["nhan"], 1
    if cur:
        dot.append((cur, dem))
    for v in NHAN:
        d = [k for x, k in dot if x == v]
        if d:
            p(f"- Đợt {VIET[v]} liên tiếp: {len(d)} đợt, trung vị {statistics.median(d):g} buổi, dài nhất {max(d)} buổi.")
    dg = [r for r in rows if r.get("nhan_dau") in NHAN and r["nhan"] in NHAN]
    if dg:
        p(f"- Đổi giữa buổi (đầu buổi ≠ cuối buổi): {ty(sum(r['nhan_dau'] != r['nhan'] for r in dg), len(dg))}.")
    tk = Counter()
    for r in hop:
        g = loai_gd((nhan.get(r["ten"]) or {}).get("nhin_lai"))
        if g:
            tk[(g, "giu" if r["nhan"] == r["view"] else "doi")] += 1
    if tk:
        p(f"- Người đó TỰ NÓI so với buổi trước (`nhin_lai_view_truoc.giu_hay_doi`, {sum(tk.values())} buổi): nói GIỮ "
          f"{tk[('giu', 'giu')] + tk[('giu', 'doi')]} (nhãn cũng giữ {tk[('giu', 'giu')]}), nói ĐỔI {tk[('doi', 'giu')] + tk[('doi', 'doi')]} "
          f"(nhãn cũng đổi {tk[('doi', 'doi')]}). Lệch: 'đổi' về lệnh/đích mà hướng H4 không đổi, hoặc so với buổi PV.")
    p("")

    # ── 2. dieu kien
    p("## 2. Tỉ lệ LẬT theo điều kiện (so với view) — 180 buổi")
    p("Có n / GIỮ / LẬT / PV = các buổi CÓ điều kiện; Không n / LẬT = buổi KHÔNG có. Δ = điểm % LẬT (có − không), tính trên "
      "tất cả · tập học · tập kiểm (dấu giống nhau ở 2 tập = ổn định). **Lời** = số buổi (học / tất cả) người đó nói tới điều "
      "kiện (regex trên câu trích trong nhãn); 'hành vi' = hành vi của chính họ ở buổi trước; '—' = không phải lời họ → chỉ mô "
      "tả, KHÔNG vào mô hình.")
    loi = {}
    bang = []
    nhom_cu = None
    for ma, nhom, mo, f, rx in ds_dk:
        bh, vd = bang_chung_loi(nhan_hoc, rx)
        bt, vdt = bang_chung_loi(nhan, rx)
        loi[ma] = (("hành vi" if rx == "hanh_vi" else "—") if rx in (None, "hanh_vi") else bh,
                   ("hành vi" if rx == "hanh_vi" else "—") if rx in (None, "hanh_vi") else f"{bh} / {bt}", vd or vdt)

        def tinh(ds):
            co = [r for r in ds if f(r) is True]
            ko = [r for r in ds if f(r) is False]
            lc = sum(ket_qua(r) == "LAT" for r in co)
            lk = sum(ket_qua(r) == "LAT" for r in ko)
            d = (lc / len(co) - lk / len(ko)) if co and ko else None
            return co, ko, lc, lk, d
        co, ko, lc, lk, d = tinh(hop)
        if not co and not ko:
            continue
        dh, dk_ = tinh(hoc)[4], tinh(kiem)[4]
        gc = sum(ket_qua(r) == "GIU" for r in co)
        pc = sum(ket_qua(r) == "PV" for r in co)
        bang.append(dict(ma=ma, nhom=nhom, mo=mo, n=len(co), giu=gc, lat=lc, pv=pc, nk=len(ko), latk=lk, d=d, dh=dh, dk=dk_))
        if nhom != nhom_cu:
            p("")
            p(f"**{nhom}**")
            p("")
            p("| Điều kiện | Có n | GIỮ | LẬT | PV | Không n | LẬT | Δ tất cả | Δ học | Δ kiểm | Lời |")
            p("|---|---|---|---|---|---|---|---|---|---|---|")
            nhom_cu = nhom
        f_ = lambda x: "—" if x is None else f"{100 * x:+.0f}"  # noqa: E731
        p(f"| {mo} | {len(co)} | {pt(gc, len(co))} | {ty(lc, len(co))} | {pc} | {len(ko)} | {pt(lk, len(ko))} | "
          f"{f_(d)} | {f_(dh)} | {f_(dk_)} | {loi[ma][1]} |")
    p("")
    c_all, n_all = tg["tất cả"]
    nen = c_all["LAT"] / n_all if n_all else 0
    p(f"Tỉ lệ LẬT nền = {ty(c_all['LAT'], n_all)} (học {ty(tg['học'][0]['LAT'], tg['học'][1])}, kiểm {ty(tg['kiểm'][0]['LAT'], tg['kiểm'][1])}).")
    p("")
    on_dinh = lambda b: b["dh"] is not None and b["dk"] is not None and b["dh"] > 0 and b["dk"] > 0  # noqa: E731
    manh = sorted([b for b in bang if b["n"] >= 8 and b["d"] is not None and b["d"] > 0], key=lambda b: (-on_dinh(b), -b["d"]))
    p("**Điều kiện đi cùng LẬT mạnh nhất** (≥ 8 buổi có; xếp: Δ dương ở CẢ học và kiểm trước, rồi theo Δ):")
    TOP_LAT = []
    for b in manh[:7]:
        TOP_LAT.append(b)
        dh = "—" if b["dh"] is None else f"{100 * b['dh']:+.0f}"
        dk_ = "—" if b["dk"] is None else f"{100 * b['dk']:+.0f}"
        p(f"- {b['mo']}: LẬT {ty(b['lat'], b['n'])} vs {pt(b['latk'], b['nk'])} khi không có (Δ {100 * b['d']:+.0f}; học {dh}, "
          f"kiểm {dk_}) · lời: {loi[b['ma']][1]}.")
    p("")
    SU_KIEN = {"vh_cham_rau", "vh_dong_1h4", "vh_dong_2h4", "vh_dong_dung_khung", "vh_dong_d1", "vh_ben_kia", "cham_dich",
               "cham_chang1", "h4_lon_nguoc", "d1_nhan_chim_nguoc", "d1_cuoi_nguoc", "vh_dong_vol", "h4_lon_nguoc_vol",
               "vol_h4_nguoc", "nguoc_max_3", "di_nguoc_2", "tin_lon_giua", "pm_nguoc", "pm_7n_nguoc", "pm_moi_truong_nguoc", "h4_sai_e89", "h4_sai_e200",
               "d1_sai_e89", "d1_sai_e200", "d1_sai_dai34", "h4_sai_dai34"}
    bo_qua = sorted([b for b in bang if b["ma"] in SU_KIEN and b["n"] >= 8 and b["lat"] / b["n"] <= max(nen, 0.2)],
                    key=lambda b: -b["n"])
    p(f"**Điều kiện người đó hay BỎ QUA** (sự kiện ngược view xảy ra ≥ 8 buổi mà % LẬT ≤ nền {100 * nen:.0f}% hoặc ≤ 20%):")
    TOP_BQ = []
    for b in bo_qua[:7]:
        TOP_BQ.append(b)
        p(f"- {b['mo']}: {b['n']} buổi, vẫn GIỮ {ty(b['giu'], b['n'])}, LẬT {ty(b['lat'], b['n'])}.")
    p("")
    van_giu = sorted([b for b in bang if b["nhom"] in ("Mốc sai & đích", "Nến & volume", "Trendline") and b["n"] >= 8
                      and b["giu"] / b["n"] >= 0.5 and b["d"] and b["d"] > 0], key=lambda b: (not b["ma"].startswith("vh_"), -b["n"]))
    p("**Mốc sai / nến ngược view có làm tăng LẬT nhưng người đó vẫn GIỮ đa số** (≥ 8 buổi, GIỮ ≥ 50%):")
    TOP_VG = []
    for b in van_giu[:8]:
        TOP_VG.append(b)
        p(f"- {b['mo']}: {b['n']} buổi, vẫn GIỮ {ty(b['giu'], b['n'])} (LẬT {pt(b['lat'], b['n'])}, PV {b['pv']}).")
    p("")
    p("Lời người đó cho từng điều kiện (câu trích ưu tiên `nhin_lai_view_truoc`, mốc sai, nến+volume):")
    p("")
    for ma, _, mo, f, rx in ds_dk:
        if loi[ma][2]:
            vd = loi[ma][2]
            p(f"- {mo} — {loi[ma][1]} buổi; vd {vd[0]} {vd[1] or ''}: \"{cat(vd[2], 150)}\"")
    p("")

    # ── 3. loi nguoi do
    p("## 3. Lời người đó: vì sao GIỮ / vì sao ĐỔI")
    nh, tong, kn = nhom_ly_do(nhan)
    if not tong:
        p("_Nhãn đang dùng không có `nhin_lai_view_truoc.giu_hay_doi`._")
    else:
        p(f"Nguồn: `nhin_lai_view_truoc` ({tong['giu']} buổi nói GIỮ, {tong['doi']} buổi nói ĐỔI so với buổi trước). 1 buổi có "
          "thể thuộc nhiều nhóm (regex trên `vi_sao` = tóm tắt lý do họ tự nói). Câu trích (`trich`) là lời người đó; giờ = phút "
          "trong video. % = trong số buổi nói GIỮ / ĐỔI.")
        p("")
        p("| Nhóm lý do | GIỮ | ĐỔI |")
        p("|---|---|---|")
        for ten, _ in sorted(NHOM_LY_DO, key=lambda x: -(len(nh[x[0]]["doi"]) / max(tong["doi"], 1) - len(nh[x[0]]["giu"]) / max(tong["giu"], 1))):
            p(f"| {ten} | {len(nh[ten]['giu'])} ({pt(len(nh[ten]['giu']), tong['giu'])}) | {len(nh[ten]['doi'])} ({pt(len(nh[ten]['doi']), tong['doi'])}) |")
        p(f"| (không vào nhóm nào) | {len(kn['giu'])} | {len(kn['doi'])} |")
        p("")
        for loai, tieu in (("giu", "GIỮ"), ("doi", "ĐỔI")):
            p(f"**Lý do {tieu} — câu trích:**")
            for ten, rx in NHOM_LY_DO:
                ds = sorted(nh[ten][loai], key=lambda x: (not re.search(rx, kd(x[2])), x[1] is None, x[0]))
                if ds:
                    vd = "; ".join(f"{x[0]} {x[1] or ''} (view trước {VIET.get(dtg.chuan_huong(x[3]), x[3])}): \"{cat(x[2], 150)}\""
                                   for x in ds[:2])
                    p(f"- *{ten}* ({len(ds)}): {vd}")
            p("")
    ng = defaultdict(list)
    so_ng = 0
    for t, n in sorted(nhan.items()):
        if n.get("doi_y_giua_buoi") and n.get("ly_do_doi_y"):
            so_ng += 1
            x = n["ly_do_doi_y"]
            vb = kd(x if isinstance(x, str) else json.dumps(x, ensure_ascii=False))
            for ten, rx in NHOM_LY_DO:
                if re.search(rx, vb):
                    ng[ten].append((t[:10], n.get("huong_dau"), n.get("huong"), x))
    if so_ng:
        p(f"**Đổi GIỮA buổi** (`ly_do_doi_y`, {so_ng} buổi):")
        for ten, _ in NHOM_LY_DO:
            if ng[ten]:
                x = ng[ten][0]
                p(f"- *{ten}* ({len(ng[ten])}): vd {x[0]} {VIET.get(x[1], x[1])}→{VIET.get(x[2], x[2])}: \"{cat(x[3], 150)}\"")
        p("")
    nv = [(t, x) for t, n in sorted(nhan.items()) for x in (n.get("nen_volume") or []) if isinstance(x, dict)]
    if nv:
        co_vol = [(t, x) for t, x in nv if x.get("volume") not in (None, "", "null")]
        kh = Counter(str(x.get("khung") or "?") for _, x in nv)
        p(f"**Nến + volume** (`nen_volume`, {len(nv)} lời ở {len({t for t, _ in nv})} buổi): theo khung " +
          ", ".join(f"{k} {v}" for k, v in kh.most_common()) + f"; có nói volume: {ty(len(co_vol), len(nv))}.")
        KL = [("chờ nến đóng xác nhận (nếu/khi đóng … thì …)", r"\b(neu|khi|phai|chua|cho)\b[^.]{0,30}(dong|xanh|do|vuot|thung|gay|test)"),
              ("gạt đi: fake / trap / quét / chỉ là hồi", r"fake|trap|quet|chi la|du (long|short)|kill|hoi quang|khong (tin|co gi|an thua)|binh thuong"),
              ("xác nhận xu hướng / đảo chiều", r"confirm|xac nhan|dao chieu|xu huong (giam|tang)|down ?trend|up ?trend|\bgay\b|break|vuot|that bai"),
              ("đọc lực mạnh/yếu, volume", r"\bluc\b|volume|\byeu\b|\bmanh\b")]
        kl, vdkl = Counter(), {}
        for t, x in nv:
            s_ = kd(f"{x.get('ket_luan') or ''} {x.get('volume') or ''}")
            g = next((ten for ten, rx in KL if re.search(rx, s_)), "khác")
            kl[g] += 1
            vdkl.setdefault(g, (t, x))
        p("- Họ rút ra từ nến: " + ", ".join(f"{k} {v}" for k, v in kl.most_common()) + ".")
        vk = Counter()
        for t, x in co_vol:
            s_ = kd(str(x.get("volume")))
            vk["volume lớn / tăng / vượt trội" if re.search(r"lon|\bto\b|cao|tang|manh|dot bien|nhieu|vuot|khung|khu?ng", s_) else
               "volume nhỏ / yếu / chưa có" if re.search(r"nho|thap|yeu|\bit\b|giam|can|khong co|chua", s_) else "khác"] += 1
        if vk:
            p("- Khi nói volume: " + ", ".join(f"{k} {v}" for k, v in vk.most_common()) + ".")
        # theo ket qua buoi (so voi view)
        kq_b = {r["ten"]: ket_qua(r) for r in rows if r["view"] in DAU and r["nhan"] in NHAN}
        theo = defaultdict(lambda: [0, 0, 0, set()])
        for t, x in nv:
            k = kq_b.get(t)
            if not k:
                continue
            theo[k][0] += 1
            theo[k][1] += str(x.get("khung") or "").upper() in ("D1", "W1")
            theo[k][2] += x.get("volume") not in (None, "", "null")
            theo[k][3].add(t)
        if theo:
            p("- Theo kết quả buổi: " + "; ".join(
                f"{ {'GIU': 'GIỮ', 'LAT': 'LẬT', 'PV': 'PV'}[k]} ({len(v[3])} buổi): {v[0] / len(v[3]):.1f} lời nến/buổi, "
                f"{pt(v[1], v[0])} là nến D1/W1, {pt(v[2], v[0])} có nói volume" for k, v in sorted(theo.items())) + ".")
        for t, x in co_vol[:2]:
            p(f"- {t[:10]} {x.get('gio') or ''} [{x.get('khung')}] volume \"{cat(x.get('volume'), 50)}\" → \"{cat(x.get('trich'), 140)}\"")
        for g, (t, x) in vdkl.items():
            p(f"- ({g}) {t[:10]} {x.get('gio') or ''} [{x.get('khung')}]: \"{cat(x.get('trich'), 140)}\"")
        p("")
    tt = [(t, x) for t, n in sorted(nhan.items()) for x in (n.get("tin_tuc") or []) if isinstance(x, dict)]
    if tt:
        sb = {t for t, _ in tt}
        p(f"**Tin tức người đó dùng** (`tin_tuc`, {len(tt)} lời ở {len(sb)}/{len(nhan)} buổi): nguồn " +
          ", ".join(f"{k or '?'} {v}" for k, v in Counter(x.get("nguon") for _, x in tt).most_common()) + ".")
        ah = Counter()
        vda = {}
        for t, x in tt:
            s = kd(x.get("anh_huong_view") or "")
            g = ("không đổi view: tin chỉ hợp lý hoá đường giá / bỏ qua" if re.search(
                    r"khong doi view|hop ly hoa|cho vui|khong (tap trung|quan tam|anh huong|dung|nhin|y nghia)|bac bo|loi dung tin|giu view", s)
                 else "né / tránh tin, chờ sau tin, đánh nhẹ" if re.search(
                    r"\bne\b|tranh|cho tin|dung ngoai|danh (it|nhe)|quan sat|than trong|can than|truoc tin|bien dong|nhieu|de y", s)
                 else "dùng tin để dự hướng (ra X thì giá Y)" if re.search(
                    r"neu ra|ra (xau|tot)|day (ve|len)|bearish|bullish|hoi phuc|dump|xau cho|tot cho|khop view|sap|giam|tang", s)
                 else "khác / không nêu")
            ah[g] += 1
            vda.setdefault(g, (t, x))
        p("- Ảnh hưởng tới view (họ nói): " + ", ".join(f"{k} {v}" for k, v in ah.most_common()) + ".")
        pm = [(t, x) for t, x in tt if re.search(r"polymarket|xac suat", kd(json.dumps(x, ensure_ascii=False)))]
        p(f"- Nhắc Polymarket / xác suất lãi suất: {len(pm)} lời ở {len({t for t, _ in pm})} buổi.")
        for g, (t, x) in vda.items():
            p(f"- ({g}) {t[:10]} {x.get('gio') or ''} [{cat(x.get('su_kien'), 40)}]: \"{cat(x.get('trich'), 140)}\"")
        p("")

    # ── 4. mo hinh
    p("## 4. Mô hình luật NẾU–THÌ (mặc định GIỮ view) — chọn trên tập HỌC, đo trên tập KIỂM")
    ung_don = [ma for ma, _, _, _, rx in ds_dk if rx == "hanh_vi" or (rx is not None and (loi[ma][0] or 0) >= MIN_LOI)]
    ung = list(ung_don)
    for i, x in enumerate(ung_don):
        for y in ung_don[i + 1:]:
            ma = f"{x}&{y}"
            DK_MAP[ma] = (lambda a_, b_: lambda r: DK_MAP[a_](r) is True and DK_MAP[b_](r) is True)(x, y)
            MO_TA[ma] = f"{MO_TA[x]} VÀ {MO_TA[y]}"
            ung.append(ma)
    p(f"Ứng viên = {len(ung_don)} điều kiện có lời người đó trong TẬP HỌC (≥ {MIN_LOI} buổi) hoặc là hành vi của họ + mọi cặp VÀ "
      f"({len(ung)} ứng viên): " + ", ".join(f"`{x}`" for x in ung_don) + ". Hành động: LẬT hoặc PHÂN VÂN. Học tham lam, mỗi "
      f"luật thêm phải đúng thêm ≥ {MIN_GAIN} buổi; tối đa K luật (K ∈ 0..{K_TOI_DA}) chọn bằng kiểm chéo thời gian TRONG tập học.")
    p("")
    thang_h = sorted({r["thang"] for r in hoc})
    p("Số buổi dùng (có view trước + nhãn N): " + ", ".join(f"{t}: {sum(r['thang'] == t for r in hop)}"
                                                           for t in sorted({r['thang'] for r in hop})))
    p("")

    HO = {"đơn": ung_don, "đơn + cặp VÀ": ung}

    def kiem_cheo(chia, K, ho="đơn"):
        kq = []
        for hoc_t, thu_t in chia:
            lu = hoc_luat([r for r in hoc if r["thang"] in hoc_t], HO[ho], K)
            kq += [(r, du_doan(r, lu), lu, thu_t) for r in hoc if r["thang"] in thu_t]
        return kq

    chia_A = [(thang_h[:k], [thang_h[k]]) for k in range(2, len(thang_h))]
    chia_B = [(thang_h[:4], thang_h[4:]), (thang_h[:5], thang_h[5:])]
    p("**Chọn họ ứng viên + K bằng kiểm chéo A trong tập học** (mở rộng theo tháng: học T1–T2 thử T3, …, học T1–T5 thử T6; "
      f"luật phải khớp ≥ {MIN_HO_TRO} buổi chưa bị luật trước bắt và đúng thêm ≥ {MIN_GAIN} buổi):")
    p("")
    p("| K | chỉ điều kiện đơn | đơn + cặp VÀ |")
    p("|---|---|---|")
    tot = None
    for K in range(K_TOI_DA + 1):
        o = []
        for ho in HO:
            kq = kiem_cheo(chia_A, K, ho)
            d = sum(du == r["nhan"] for r, du, _, _ in kq)
            o.append(ty(d, len(kq)))
            if tot is None or d > tot[2]:
                tot = (K, ho, d)
        p(f"| {K} | " + " | ".join(o) + " |")
    K, HO_CHON = tot[0], tot[1]
    ung = HO[HO_CHON]
    p("")
    p("Chẩn đoán K = 1 (họ đơn): luật số 1 học được ở mỗi lượt và kết quả khi đem thử tháng sau:")
    p("")
    for hoc_t, thu_t in chia_A:
        tr = [r for r in hoc if r["thang"] in hoc_t]
        te = [r for r in hoc if r["thang"] in thu_t]
        lu = hoc_luat(tr, ung_don, 1)
        if not lu:
            p(f"- học {hoc_t[0][5:]}–{hoc_t[-1][5:]}: không luật nào đủ điều kiện")
            continue
        ma, h = lu[0]
        f_tr = [r for r in tr if DK_MAP[ma](r) is True]
        f_te = [r for r in te if DK_MAP[ma](r) is True]
        dung = lambda ds: sum(du_doan(r, lu) == r["nhan"] for r in ds)  # noqa: E731
        p(f"- học {hoc_t[0][5:]}–{hoc_t[-1][5:]}: {MO_TA[ma]} → {'LẬT' if h == 'LAT' else 'PHÂN VÂN'} · lúc học khớp {len(f_tr)}, đúng "
          f"{dung(f_tr)} (giữ view đúng {sum(r['view'] == r['nhan'] for r in f_tr)}) · tháng {thu_t[0][5:]} khớp {len(f_te)}, đúng "
          f"{dung(f_te)} (giữ view đúng {sum(r['view'] == r['nhan'] for r in f_te)})")
    p(f"→ **K = {K}, họ = {HO_CHON}** (cao nhất; hoà lấy K nhỏ, họ đơn).")
    p("")
    kq_A = kiem_cheo(chia_A, K, HO_CHON)
    p(f"**Kiểm chéo trong tập học, K = {K}** (cùng buổi, % trùng nhãn 3 lớp):")
    p("")
    L.extend(HEAD_SS)
    ss_hoc = []
    gA = {id(r): du for r, du, _, _ in kq_A}
    for hoc_t, thu_t in chia_A:
        ds = [r for r, _, _, tt_ in kq_A if tt_ == thu_t]
        p(dong_so_sanh(f"A: học {hoc_t[0][5:]}–{hoc_t[-1][5:]} → thử {thu_t[0][5:]}", ds, lambda rr: gA[id(rr)]))
    p(dong_so_sanh("**A gộp T3–T6**", [r for r, _, _, _ in kq_A], lambda rr: gA[id(rr)]))
    ss_hoc.append(("A gộp T3–T6 (trong tập học)", [r for r, _, _, _ in kq_A], lambda rr: gA[id(rr)]))
    for hoc_t, thu_t in chia_B:
        kq = kiem_cheo([(hoc_t, thu_t)], K, HO_CHON)
        g = {id(r): du for r, du, _, _ in kq}
        ten = f"B: học {hoc_t[0][5:]}–{hoc_t[-1][5:]} → thử {'+'.join(t[5:] for t in thu_t)}"
        p(dong_so_sanh(ten, [r for r, _, _, _ in kq], lambda rr, g=g: g[id(rr)]))
        ss_hoc.append((ten, [r for r, _, _, _ in kq], lambda rr, g=g: g[id(rr)]))
    p("")
    for hoc_t, thu_t in chia_A:
        lu = next((x[2] for x in kq_A if x[3] == thu_t), [])
        p(f"- Luật học từ {hoc_t[0][5:]}–{hoc_t[-1][5:]}: {ten_luat(lu)}")
    p("")
    luat = hoc_luat(hoc, ung, K)
    p(f"**Bộ luật KHOÁ** (học trên toàn bộ tập học T1–T6, K = {K}):")
    p("")
    for i, (ma, h) in enumerate(luat, 1):
        fire = [r for r in hoc if DK_MAP[ma](r) is True]
        firek = [r for r in kiem if DK_MAP[ma](r) is True]
        p(f"{i}. NẾU {MO_TA[ma]} THÌ **{'LẬT' if h == 'LAT' else 'PHÂN VÂN'}** — học: khớp {len(fire)}, đúng "
          f"{ty(sum(du_doan(r, luat[:i]) == r['nhan'] for r in fire), len(fire))}; kiểm: khớp {len(firek)}, đúng "
          f"{ty(sum(du_doan(r, luat[:i]) == r['nhan'] for r in firek), len(firek))}")
    p(f"{len(luat) + 1}. Còn lại: GIỮ view.")
    p("")
    p("**(b) Kiểm theo thời gian: luật chọn trên buổi < 07/01, đo trên buổi ≥ 07/01** (cùng buổi, cùng thước):")
    p("")
    L.extend(HEAD_SS)
    ss_kiem = [("Trong mẫu: tập học T1–T6", hoc), ("**Ngoài mẫu: tập kiểm T7–T10**", kiem)]
    for t in sorted({r["thang"] for r in kiem}):
        ss_kiem.append((f"  kiểm {t}", [r for r in kiem if r["thang"] == t]))
    for ten, ds in ss_kiem:
        p(dong_so_sanh(ten, ds, lambda rr: du_doan(rr, luat)))
    p("")
    p("Tham khảo (KHÔNG khoá): nếu ÉP thêm luật (học trên toàn tập học, họ đơn) rồi đo trên tập kiểm:")
    p("")
    for K_ep in (1, 2, 3):
        lu = hoc_luat(hoc, HO["đơn"], K_ep)
        p(f"- K = {K_ep}: {ten_luat(lu)} → học {pt(sum(du_doan(r, lu) == r['nhan'] for r in hoc), len(hoc))}, "
          f"kiểm {ty(sum(du_doan(r, lu) == r['nhan'] for r in kiem), len(kiem))} (giữ view kiểm {pt(sum(r['view'] == r['nhan'] for r in kiem), len(kiem))})")
    p("")
    luat_180 = hoc_luat(hop, ung, K)
    p(f"Tham khảo (KHÔNG khoá, trong mẫu): cùng thủ tục học trên cả {len(hop)} buổi → {ten_luat(luat_180)}; "
      f"trùng {ty(sum(du_doan(r, luat_180) == r['nhan'] for r in hop), len(hop))} vs giữ view "
      f"{ty(sum(r['view'] == r['nhan'] for r in hop), len(hop))}.")
    p("")

    # ── 5. phan van
    p("## 5. Khi nào người đó PHÂN VÂN")
    pv = [r for r in rows if r["nhan"] == "PHAN_VAN"]
    kpv = [r for r in rows if r["nhan"] in DAU]
    p(f"{len(pv)} buổi PHÂN VÂN / {sum(r['nhan'] in NHAN for r in rows)} buổi có nhãn "
      f"(học {sum(r['tap'] == 'hoc' for r in pv)}, kiểm {sum(r['tap'] == 'kiem' for r in pv)}).")
    p("")
    if pv:
        p("| Buổi | N−1 | view | chụm EMA H4 % | H4 vs dải34/89/200 | RSI H4 / D1 | cách EMA89 D1 % | giá đi % | mốc sai buổi trước | tin | Lời cuối buổi |")
        p("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in pv:
            vh = "—" if not r.get("co_vh_truoc") else ("đóng qua 1H4" if r.get("vh_dong_1h4") else ("râu chạm" if r.get("vh_cham_rau") else "chưa chạm"))
            n_ = nhan.get(r["ten"]) or {}
            tin = "/".join(x for x in (r.get("tin_giua") and f"sau {r['tin_giua']}", r.get("tin_sap48") and f"trước {r['tin_sap48']}") if x) or "—"
            p(f"| {r['ngay']} | {VIET.get(r.get('nhan_truoc'))} | {VIET.get(r.get('view'))} | {r.get('chum_h4_pct')} | "
              f"{r.get('h4_vs_dai34')}/{r.get('h4_vs_e89')}/{r.get('h4_vs_e200')} | {r.get('rsi_h4')} / {r.get('rsi_d1')} | "
              f"{r.get('kc_e89_d1_pct')} | {r.get('di_pct') if r.get('di_pct') is not None else '—'} | {vh} | {tin} | "
              f"{n_.get('gio_cuoi') or ''} \"{cat(n_.get('trich_cuoi'), 100)}\" |")
        p("")
        p("PV so với buổi có hướng (trung vị / tỉ lệ):")
        p("")
        p("| Đặc trưng | PV | Có hướng |")
        p("|---|---|---|")
        for cot, ten in (("chum_h4_pct", "EMA34/89/200 H4 chụm (% giá)"), ("rsi_h4", "RSI H4"), ("rsi_d1", "RSI D1"),
                         ("kc_e89_d1_pct", "Cách EMA89 D1 (%)"), ("di_pct", "Giá đi từ C buổi trước (%)"),
                         ("nguoc_max", "Đi ngược view tối đa giữa 2 buổi (%)"), ("gio_tu_truoc", "Giờ từ buổi trước")):
            a_ = [r[cot] for r in pv if isinstance(r.get(cot), float)]
            b_ = [r[cot] for r in kpv if isinstance(r.get(cot), float)]
            if a_ and b_:
                p(f"| {ten} | {statistics.median(a_):.2f} | {statistics.median(b_):.2f} |")
        for cot, ten in (("h4_vs_dai34", "Giá H4 TRONG dải EMA34"), ("d1_vs_dai34", "Giá D1 TRONG dải EMA34")):
            a_ = [r for r in pv if r.get(cot) is not None]
            b_ = [r for r in kpv if r.get(cot) is not None]
            p(f"| {ten} | {ty(sum(r[cot] == 0 for r in a_), len(a_))} | {ty(sum(r[cot] == 0 for r in b_), len(b_))} |")
        for ma in ("chum_h4", "truoc_pv", "truoc_chac_thap", "vh_dong_1h4", "vh_cham_rau", "cham_dich", "h4_lon_nguoc",
                   "d1_nhan_chim_nguoc", "tin_lon_sap24", "tin_lon_giua", "cua_so_fomc", "pm_moi_truong_nguoc", "thu_hai", "tren_xuong_khac"):
            if ma not in DK_MAP:
                continue
            f = DK_MAP[ma]
            a_ = [f(r) for r in pv if f(r) is not None]
            b_ = [f(r) for r in kpv if f(r) is not None]
            p(f"| {MO_TA[ma]} | {ty(sum(a_), len(a_))} | {ty(sum(b_), len(b_))} |")
        p("")
        p("Buổi PV đến từ " + ", ".join(f"{VIET[x]} {sum(r.get('nhan_truoc') == x for r in pv)}" for x in NHAN) +
          "; buổi sau PV đi về " + ", ".join(f"{VIET[y]} {m[('PHAN_VAN', y)]}" for y in NHAN) + ".")
        p("")

    # ── 6. do rong vung
    gia_C = {r["ten"]: r.get("gia_C") for r in rows}
    p("## 6. Độ rộng vùng giá người đó nói (`vung_nguoi_do`)")
    w, sb, bo = defaultdict(list), 0, 0
    for t, n in nhan.items():
        vs = n.get("vung_nguoi_do")
        if not isinstance(vs, list):
            continue
        sb += 1
        g = gia_C.get(t) or n.get("gia_noi")
        for v in vs:
            if not isinstance(v, dict):
                continue
            x, y = dtg.so_list(v.get("tu")), dtg.so_list(v.get("den"))
            if not x and not y:
                continue
            x = (x or y)[0]; y = (y or [x])[0]
            if not g or not (0.6 * g <= x <= 1.6 * g and 0.6 * g <= y <= 1.6 * g):
                bo += 1; continue
            w[kd(str(v.get("loai") or "")).replace(" ", "_")].append((abs(y - x), abs(y - x) / g * 100))
    if not w:
        p("_Nhãn đang dùng chưa có `vung_nguoi_do`._")
    else:
        p(f"{sb} buổi có trường này; bỏ {bo} vùng lệch quá xa giá BTC (nghi tài sản khác). Độ rộng = |đến − từ| (1 số = 0); "
          "% = so với giá BTC lúc C của buổi.")
        p("")
        p("| Loại | n | Là 1 điểm | Trung vị (giá) | p25–p75 (giá) | Trung vị % | p25–p75 % | Chỉ tính vùng > 0: trung vị giá / % |")
        p("|---|---|---|---|---|---|---|---|")
        TEN_V = {"vao": "Vào lệnh", "tp": "TP", "sl": "SL", "ho_tro": "Hỗ trợ", "khang_cu": "Kháng cự", "dich": "Đích"}
        for loai in list(TEN_V) + sorted(k for k in w if k not in TEN_V):
            x = w.get(loai)
            if not x:
                continue
            gi, pc = [u for u, _ in x], [v for _, v in x]
            vz = [(u, v) for u, v in x if u > 0]
            p(f"| {TEN_V.get(loai, loai)} | {len(x)} | {pt(sum(u == 0 for u in gi), len(x))} | {statistics.median(gi):,.0f} | "
              f"{pct(gi, .25):,.0f}–{pct(gi, .75):,.0f} | {statistics.median(pc):.2f}% | {pct(pc, .25):.2f}–{pct(pc, .75):.2f}% | "
              + (f"{statistics.median([u for u, _ in vz]):,.0f} / {statistics.median([v for _, v in vz]):.2f}% (n {len(vz)})" if vz else "—") + " |")
    p("")

    # ── 7. trung han
    trung_han(L, rows, nhan)

    # ── 8. Fed / lai suat
    fed(L, rows, nhan)

    # ── tom tat (chen len dau)
    hk = sum(du_doan(r, luat) == r["nhan"] for r in kiem)
    tom = ["## Tóm tắt", "",
           f"- Giữ view (so với hướng gần nhất): **{ty(c_all['GIU'], n_all)}** buổi (học {pt(tg['học'][0]['GIU'], tg['học'][1])}, "
           f"kiểm {pt(tg['kiểm'][0]['GIU'], tg['kiểm'][1])}); LẬT {pt(c_all['LAT'], n_all)}, sang PV {pt(c_all['PV'], n_all)}.",
           "- LẬT mạnh nhất khi: " + "; ".join(f"{b['mo']} ({pt(b['lat'], b['n'])} vs {pt(b['latk'], b['nk'])})" for b in TOP_LAT[:3]) + ".",
           "- Hay BỎ QUA (LẬT không cao hơn nền): " + "; ".join(f"{b['mo']} (giữ {pt(b['giu'], b['n'])}, n {b['n']})" for b in TOP_BQ[:3]) + ".",
           "- Mốc sai của chính họ bị phá mà vẫn GIỮ đa số: " + "; ".join(f"{b['mo']} (giữ {pt(b['giu'], b['n'])}, n {b['n']})" for b in TOP_VG[:3]) + ".",
           f"- Bộ luật khoá (chọn trên học, K = {K}): {ten_luat(luat)}.",
           f"- Ngoài mẫu (kiểm T7–T10, {len(kiem)} buổi): bộ luật {ty(hk, len(kiem))} · giữ view "
           f"{pt(sum(r['view'] == r['nhan'] for r in kiem), len(kiem))} · luôn GIẢM {pt(sum(r['nhan'] == 'GIAM' for r in kiem), len(kiem))} · "
           f"từ trên xuống {pt(sum(r['luat_tren_xuong'] == r['nhan'] for r in kiem), len(kiem))}.", ""]
    L[TOM:TOM] = tom
    (RA / "GIU_LAT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    khoa(nguon, luat, K, ss_hoc, ss_kiem, loi, ung_don)
    print(f"GIU_LAT.md + LUAT_KHOA.md ({nguon}); K={K}; luat={luat}; kiem {hk}/{len(kiem)}")


# ───────────────────────── trung han ─────────────────────────
def trung_han(L, rows, nhan):
    p = L.append
    p("## 7. Trung hạn (D1/W1): độ bền view, đích ≤ 60 ngày, giữ/đóng lệnh")
    co = [r for r in rows if isinstance((nhan.get(r["ten"]) or {}).get("view_trung_han"), list)
          and (nhan.get(r["ten"]) or {}).get("view_trung_han")]
    if not co:
        p("_Nhãn đang dùng chưa có `view_trung_han` / `giu_dong`._")
        p("")
        return
    du = dtg.DuLieu()
    C = {r["ten"]: dt.datetime.strptime(r["C_vn"], "%Y-%m-%d %H:%M") - dtg.VN for r in rows}
    het_du_lieu = du.h4.n[-1].dong
    p(f"{len(co)} buổi có `view_trung_han`. Đợt = các buổi liền nhau (trong các buổi CÓ nói view khung đó) cùng hướng; "
      "buổi không nói khung đó thì bỏ qua, không cắt đợt. Lật = buổi đầu tiên nói hướng khác.")
    p("")
    for khung in ("D1", "W1"):
        ds = []
        for r in rows:
            n = nhan.get(r["ten"]) or {}
            vs = [v for v in (n.get("view_trung_han") or []) if isinstance(v, dict) and str(v.get("khung") or "").upper() == khung]
            h = next((dtg.chuan_huong(v.get("huong")) for v in vs if dtg.chuan_huong(v.get("huong"))), None)
            if h:
                ds.append((r, h, vs))
        if not ds:
            continue
        dot = []
        for r, h, vs in ds:
            if dot and dot[-1]["h"] == h:
                dot[-1]["b"].append((r, vs))
            else:
                dot.append({"h": h, "b": [(r, vs)]})
        p(f"### View {khung} — {len(ds)} buổi, {len(dot)} đợt")
        p("")
        p("| # | Hướng | Từ → đến | Buổi | Ngày | Kết thúc vì (lời buổi lật) |")
        p("|---|---|---|---|---|---|")
        dai = []
        for i, d in enumerate(dot):
            r0, r1 = d["b"][0][0], d["b"][-1][0]
            het = i + 1 < len(dot)
            ngay = ((C[dot[i + 1]["b"][0][0]["ten"]] if het else C[r1["ten"]]) - C[r0["ten"]]).total_seconds() / 86400
            dai.append((ngay, het, len(d["b"])))
            ly = ""
            if het:
                rn, vsn = dot[i + 1]["b"][0]
                v = vsn[0]
                nl = (nhan.get(rn["ten"]) or {}).get("nhin_lai") or {}
                ly = f"{rn['ngay']} {v.get('gio') or ''} \"{cat(v.get('trich'), 110)}\""
                if nl.get("trich") and loai_gd(nl) == "doi":
                    ly += f" · nhìn lại {nl.get('gio') or ''}: \"{cat(nl.get('trich'), 90)}\""
                mvk = next((x.get("mat_view_khi") for x in d["b"][-1][1] if x.get("mat_view_khi")), None)
                if mvk:
                    ly += f" · đã nói mất view khi: {cat(mvk if isinstance(mvk, str) else json.dumps(mvk, ensure_ascii=False), 70)}"
            p(f"| {i + 1} | {VIET[d['h']]} | {r0['ngay']} → {r1['ngay']} | {len(d['b'])} | {ngay:.0f}{'' if het else ' (còn chạy)'} | {ly} |")
        xong = [x for x, h, _ in dai if h]
        if xong:
            p("")
            p(f"Đợt {khung} đã kết thúc: {len(xong)}, trung vị {statistics.median(xong):.0f} ngày "
              f"(p25 {pct(xong, .25):.0f}, p75 {pct(xong, .75):.0f}, dài nhất {max(xong):.0f}); trung vị "
              f"{statistics.median([b for _, h, b in dai if h]):g} buổi.")
        # (b) dich
        tong = cham = chua_biet = 0
        tg, vd = [], []
        for i, d in enumerate(dot):
            bo_luc = C[dot[i + 1]["b"][0][0]["ten"]] if i + 1 < len(dot) else None
            da = set()
            for r, vs in d["b"]:
                for v in vs:
                    dich = dtg.so_list(v.get("dich"))
                    if not dich or tuple(dich) in da:
                        continue
                    da.add(tuple(dich))
                    t0 = C[r["ten"]]
                    han = t0 + dt.timedelta(days=60)
                    t1 = min(x for x in (bo_luc, han, het_du_lieu) if x is not None)
                    g0 = du.gia_luc(t0)
                    lo_, hi_ = min(dich), max(dich)
                    if lo_ <= g0 <= hi_:
                        continue
                    len_ = lo_ > g0
                    if (len_ and d["h"] != "TANG") or (not len_ and d["h"] != "GIAM"):
                        continue  # dich nguoc huong view (chang hoi) — khong tinh
                    luc = None
                    for nn in du.h4.n[du.h4.cuoi(t0) + 1:]:
                        if nn.mo >= t1:
                            break
                        if (len_ and nn.h >= lo_) or (not len_ and nn.l <= hi_):
                            luc = nn.mo; break
                    tong += 1
                    if luc:
                        cham += 1
                        tg.append((luc - t0).total_seconds() / 86400)
                    elif t1 == het_du_lieu and t1 < han and (bo_luc is None or bo_luc > het_du_lieu):
                        chua_biet += 1
                    vd.append((r["ngay"], VIET[d["h"]], dich, g0, luc, r["tap"]))
        p("")
        if tong:
            biet = tong - chua_biet
            p(f"**Đích {khung} chạm (râu, H4) trước khi họ bỏ view, ≤ 60 ngày** — {tong} đích cùng hướng view (mỗi đích tính 1 lần, "
              f"từ C buổi đầu nêu): chạm **{ty(cham, biet)}** ({chua_biet} chưa biết vì hết dữ liệu)" +
              (f"; thời gian tới đích trung vị {statistics.median(tg):.1f} ngày (p25 {pct(tg, .25):.1f}, p75 {pct(tg, .75):.1f})." if tg else "."))
            for tap in ("hoc", "kiem"):
                x = [v for v in vd if v[5] == tap]
                if x:
                    p(f"- {'học' if tap == 'hoc' else 'kiểm'}: chạm {sum(1 for v in x if v[4])}/{len(x)}.")
            cach = [abs(min(v[2], key=lambda z: abs(z - v[3])) / v[3] - 1) * 100 for v in vd]
            p(f"- Khoảng cách tới đích lúc nêu: trung vị {statistics.median(cach):.1f}% (p25 {pct(cach, .25):.1f}, p75 {pct(cach, .75):.1f}).")
        p("")
    # (c) giu / dong
    gd = [(r, x) for r in rows for x in ((nhan.get(r["ten"]) or {}).get("giu_dong") or []) if isinstance(x, dict)]
    p(f"### Giữ / đóng lệnh (`giu_dong`, {len(gd)} mục ở {len({r['ten'] for r, _ in gd})} buổi)")
    p("")
    if gd:
        qd = Counter(str(x.get("quyet_dinh") or "?") for _, x in gd)
        p("Quyết định: " + ", ".join(f"{k} {v}" for k, v in qd.most_common()) + ".")
        p("")
        NHOM_DONG = [  # phan loai theo `khi_nao` (tom tat), khop nhom DAU TIEN
            ("bị quét SL / cắt lỗ / sai thì cắt", r"\bsl\b|stop ?loss|cat (lo|tay|hoa)|quet|\bsai\b|lo "),
            ("chạm / gần TP, đích, vùng cản; đủ lãi", r"\btp\b|dich|target|cham|vung|can\b|du (roi|lai)|an (du|duoc|bot)|lai|\d"),
            ("nến xấu / gãy cấu trúc / view đổi", r"nen|gay|thung|pha|dong (tren|duoi|xanh|do)|view|xu huong|cau truc|yeu|luc"),
            ("tin / sự kiện / cuối tuần / qua đêm", r"\btin\b|cpi|fed|fomc|cuoi tuan|non ?farm|su kien|di ngu|qua dem|thu (hai|ba|sau|bay)|chu nhat"),
            ("dời SL về entry / hoà vốn", r"hoa von|ve entry|doi (sl|stop)|keo sl"),
            ("kiên nhẫn / chờ / giữ vì chưa có lý do", r"giu|kien nhan|cho|chua|thoai mai|gong")]
        p("Phân loại theo `khi_nao` (tóm tắt điều kiện họ nói), mỗi mục vào nhóm khớp ĐẦU TIÊN (thứ tự trong bảng).")
        p("")
        p("| Quyết định | Khi nào (nhóm) | Số | % của quyết định | Ví dụ |")
        p("|---|---|---|---|---|")
        nhom, vdn = Counter(), {}
        for r, x in gd:
            q = str(x.get("quyet_dinh") or "?")
            s = kd(x.get("khi_nao") or x.get("trich") or "")
            ten = next((t for t, rx in NHOM_DONG if re.search(rx, s)), "khác")
            nhom[(q, ten)] += 1
            vdn.setdefault((q, ten), (r["ngay"], x))
        for (q, ten), c in sorted(nhom.items(), key=lambda z: (-qd[z[0][0]], -z[1])):
            ng_, x = vdn[(q, ten)]
            p(f"| {q} | {ten} | {c} | {pt(c, qd[q])} | {ng_} {x.get('gio') or ''} \"{cat(x.get('khi_nao') or x.get('trich'), 110)}\" |")
        p("")
        # dong lenh khi view H4 doi?
        doi_buoi = {r["ten"] for r in rows if r.get("view") in DAU and r["nhan"] in NHAN and r["nhan"] != r["view"]}
        dg = [(r, x) for r, x in gd if str(x.get("quyet_dinh")) in ("dong", "chot_mot_phan")]
        p(f"- Đóng/chốt ở buổi họ đổi view H4 (LẬT/PV): {ty(sum(r['ten'] in doi_buoi for r, _ in dg), len(dg))} lần đóng; "
          f"tỉ lệ buổi đổi view trong mọi buổi có `giu_dong`: {pt(len({r['ten'] for r, _ in gd} & doi_buoi), len({r['ten'] for r, _ in gd}))}.")
    p("")


# ───────────────────────── Fed / lai suat ─────────────────────────
RX_FED = r"\bfed\b|fomc|lai suat|powell|chu tich (fed|moi)|polymarket|xac suat|dong tien (dat|re)|bom tien|hut tien|\bqe\b|\bqt\b"


def phan_bo(ds):
    c = Counter(r["nhan"] for r in ds if r["nhan"] in NHAN)
    n = sum(c.values())
    return n, " | ".join(f"{pt(c[x], n)}" for x in NHAN)


def view_d1(n):
    for v in (n or {}).get("view_trung_han") or []:
        if isinstance(v, dict) and str(v.get("khung") or "").upper() == "D1":
            h = dtg.chuan_huong(v.get("huong"))
            if h:
                return h
    return None


def fed(L, rows, nhan):
    p = L.append
    p("## 8. Fed / lãi suất kỳ tới (Polymarket, cửa sổ FOMC) và view của người đó")
    co = [r for r in rows if r["nhan"] in NHAN]
    if not any(r.get("gio_toi_fomc") is not None for r in rows):
        p("_Chưa có `du_lieu/tin_tuc/lich_kinh_te_2026.csv`._")
        p("")
        return
    p("Đặc trưng nhân quả tại C: kỳ FOMC KẾ TIẾP sau C; P(tăng)/P(giảm) lãi suất = Polymarket 'Fed decision in <tháng>' "
      "(chuẩn hoá tổng các kết quả = 100%, mốc giờ ≤ C); thay đổi 3/7 ngày cùng kỳ họp; cửa sổ FOMC = ≤ 72h trước / ≤ 24h sau "
      "quyết định; kỳ gần nhất + phiếu phản đối từ `du_lieu/tin_tuc/fomc_ket_qua_2026.csv`. Cột hướng = nhãn H4 cuối buổi N; "
      "D1 = view D1 trong `view_trung_han`.")
    p("")
    nhom = [("< 30%", lambda x: x < 30), ("30–70%", lambda x: 30 <= x <= 70), ("> 70%", lambda x: x > 70)]
    p("**Theo P(TĂNG lãi suất) kỳ tới:**")
    p("")
    p("| P(tăng) kỳ tới | Buổi (học/kiểm) | H4: TĂNG | GIẢM | PV | View D1: TĂNG / GIẢM | LẬT (so view) | P(tăng) trung vị |")
    p("|---|---|---|---|---|---|---|---|")
    for ten, f in nhom + [("không có dữ liệu", None)]:
        ds = [r for r in co if (r.get("pm_tang") is None if f is None else (r.get("pm_tang") is not None and f(r["pm_tang"])))]
        if not ds:
            continue
        n, pb = phan_bo(ds)
        d1 = Counter(view_d1(nhan.get(r["ten"])) for r in ds)
        lv = [r for r in ds if r["view"] in DAU]
        x = [r["pm_tang"] for r in ds if r.get("pm_tang") is not None]
        p(f"| {ten} | {n} ({sum(r['tap'] == 'hoc' for r in ds)}/{sum(r['tap'] == 'kiem' for r in ds)}) | {pb} | "
          f"{d1['TANG']} / {d1['GIAM']} | {pt(sum(ket_qua(r) == 'LAT' for r in lv), len(lv))} | "
          f"{statistics.median(x):.0f}% |" if x else f"| {ten} | {n} | {pb} | {d1['TANG']} / {d1['GIAM']} | "
          f"{pt(sum(ket_qua(r) == 'LAT' for r in lv), len(lv))} | — |")
    p("")
    p("**Theo thay đổi 7 ngày của P(tăng lãi suất) kỳ tới:**")
    p("")
    p("| ΔP(tăng) 7 ngày | Buổi | H4: TĂNG | GIẢM | PV |")
    p("|---|---|---|---|---|")
    for ten, f in (("tăng ≥ 10 điểm (diều hâu hơn)", lambda v: v >= 10), ("−10…+10", lambda v: -10 < v < 10),
                   ("giảm ≥ 10 điểm (bồ câu hơn)", lambda v: v <= -10)):
        ds = [r for r in co if r.get("pm_tang_d7") is not None and f(r["pm_tang_d7"])]
        if ds:
            n, pb = phan_bo(ds)
            p(f"| {ten} | {n} | {pb} |")
    p("")
    p("**Trong vs ngoài cửa sổ FOMC:**")
    p("")
    p("| | Buổi | H4: TĂNG | GIẢM | PV | LẬT (so view) | Đổi giữa buổi |")
    p("|---|---|---|---|---|---|---|")
    for ten, v in (("Trong cửa sổ (≤ 72h trước / ≤ 24h sau)", 1), ("Ngoài cửa sổ", 0)):
        ds = [r for r in co if r.get("cua_so_fomc") == v]
        n, pb = phan_bo(ds)
        lv = [r for r in ds if r["view"] in DAU]
        dg = [r for r in ds if r.get("nhan_dau") in NHAN]
        p(f"| {ten} | {n} | {pb} | {pt(sum(ket_qua(r) == 'LAT' for r in lv), len(lv))} | "
          f"{pt(sum(r['nhan_dau'] != r['nhan'] for r in dg), len(dg))} |")
    p("")
    p("**Theo kỳ FOMC gần nhất trước C:**")
    p("")
    p("| Kỳ gần nhất | Buổi | H4: TĂNG | GIẢM | PV |")
    p("|---|---|---|---|---|")
    for ten, f in (("giữ nguyên, có phiếu muốn GIẢM lãi suất", lambda r: r.get("fomc_truoc_qd", "").startswith("giu") and (r.get("fomc_truoc_pd_giam") or 0) > 0),
                   ("giữ nguyên, có phiếu muốn TĂNG lãi suất", lambda r: r.get("fomc_truoc_qd", "").startswith("giu") and (r.get("fomc_truoc_pd_tang") or 0) > 0),
                   ("giữ nguyên, không phiếu phản đối theo hướng nào", lambda r: r.get("fomc_truoc_qd", "").startswith("giu") and not (r.get("fomc_truoc_pd_giam") or 0) and not (r.get("fomc_truoc_pd_tang") or 0)),
                   ("TĂNG lãi suất", lambda r: r.get("fomc_truoc_qd", "").startswith("tang"))):
        ds = [r for r in co if isinstance(r.get("fomc_truoc_qd"), str) and f(r)]
        if ds:
            n, pb = phan_bo(ds)
            p(f"| {ten} | {n} | {pb} |")
    p("")
    # loi nguoi do ve Fed
    g = {r["ten"]: r for r in rows}
    loi = defaultdict(list)
    for t, n in sorted(nhan.items()):
        for x in n.get("tin_tuc") or []:
            if not isinstance(x, dict):
                continue
            if re.search(RX_FED, kd(f"{x.get('su_kien') or ''} {x.get('trich') or ''} {x.get('anh_huong_view') or ''}")):
                v = (g.get(t) or {}).get("pm_tang")
                k = "không có dữ liệu" if v is None else next(ten for ten, f in nhom if f(v))
                loi[k].append((t, x, (g.get(t) or {}).get("nhan")))
    tong = sum(len(v) for v in loi.values())
    p(f"**Lời người đó về Fed / lãi suất** (`tin_tuc`, {tong} lời ở {len({t for v in loi.values() for t, _, _ in v})} buổi), theo nhóm P(tăng) kỳ tới của buổi đó:")
    p("")
    for ten in [x for x, _ in nhom] + ["không có dữ liệu"]:
        ds = loi.get(ten) or []
        if not ds:
            continue
        ah = Counter()
        for t, x, h in ds:
            s_ = kd(f"{x.get('anh_huong_view') or ''} {x.get('trich') or ''}")
            ah["nghiêng GIẢM" if re.search(r"xau|giam|sap|dump|khong co luc|dong tien dat|bearish|ve (\d|day)", s_)
               else "nghiêng TĂNG" if re.search(r"tot|tang|hoi phuc|bullish|bom tien|dong tien re", s_) else "trung tính / né"] += 1
        p(f"- P(tăng) {ten}: {len(ds)} lời ({', '.join(f'{k} {v}' for k, v in ah.most_common())}; nghiêng theo từ khoá trong lời).")
        ds = sorted(ds, key=lambda z: (z[1].get("gio") is None, -len(str(z[1].get("anh_huong_view") or ""))))
        for t, x, h in ds[:2]:
            p(f"  - {t[:10]} {x.get('gio') or ''} [{cat(x.get('su_kien'), 50)}] (H4 cuối buổi {VIET.get(h)}): \"{cat(x.get('trich'), 150)}\""
              + (f" → {cat(x.get('anh_huong_view'), 90)}" if x.get("anh_huong_view") else ""))
    p("")



# ───────────────────────── khoa ─────────────────────────
def khoa(nguon, luat, K, ss_hoc, ss_kiem, loi, ung_don):
    L = []
    p = L.append
    dn = {"luat": [{"thu_tu": i + 1, "dieu_kien": ma, "hanh_dong": h} for i, (ma, h) in enumerate(luat)],
          "mac_dinh": "GIU_VIEW", "K": K, "nhan": nguon, "chon_tren": "buoi < 2026-07-01", "ung_vien": ung_don}
    s = json.dumps(dn, ensure_ascii=False, sort_keys=True)
    p("# LUẬT KHOÁ — GIỮ / LẬT view H4 (chọn CHỈ trên tập học, buổi < 2026-07-01)")
    p("")
    p(f"Khoá lúc {dt.datetime.now():%Y-%m-%d %H:%M}. Nhãn: **{nguon}**. Chọn luật + K chỉ bằng buổi < 07/01; buổi ≥ 07/01 chỉ để đo "
      "(bảng dưới). Sẽ được chấm lại cùng bot v5 trên buổi live mới.")
    p("")
    p("## Bộ luật (xét theo thứ tự; luật đầu tiên khớp thắng)")
    p("")
    p("Đầu vào tại buổi N: **view** = hướng TĂNG/GIẢM gần nhất của người đó trước N (bỏ PHÂN VÂN); nhãn buổi N−1 (đích / mốc sai "
      "/ độ chắc / tin tức); nến BTC đã đóng ≤ C_N (C = bat_dau_vn + phut); lịch tin công bố trước; Polymarket ≤ C_N. "
      "Định nghĩa điều kiện = bảng `DK` trong `hoc_v5/giu_lat/phan_tich.py` trên cột của `hoc_v5/giu_lat/dac_trung.py`.")
    p("")
    for i, (ma, h) in enumerate(luat, 1):
        p(f"{i}. NẾU {MO_TA[ma]} (`{ma}`) THÌ **{'LẬT sang hướng ngược view' if h == 'LAT' else 'PHÂN VÂN'}**")
        for x in ma.split("&"):
            if loi[x][0] == "hành vi":
                p(f"   - `{x}`: hành vi của chính người đó ở buổi trước")
            elif loi[x][2]:
                vd = loi[x][2]
                p(f"   - `{x}` — lời người đó ({loi[x][1]} buổi): {vd[0]} {vd[1] or ''} \"{cat(vd[2], 140)}\"")
    p(f"{len(luat) + 1}. Còn lại: **GIỮ view**.")
    p("")
    p("## Kết quả (cùng buổi, % trùng nhãn 3 lớp)")
    p("")
    L.extend(HEAD_SS)
    for ten, ds, f in ss_hoc:
        p(dong_so_sanh(ten, ds, f))
    for ten, ds in ss_kiem:
        p(dong_so_sanh(ten, ds, lambda rr: du_doan(rr, luat)))
    p("")
    p("## Băm")
    p("")
    p(f"- định nghĩa (JSON sort_keys): `{s}`")
    p(f"- sha256(định nghĩa) = `{hashlib.sha256(s.encode()).hexdigest()}`")
    for f in ("dac_trung.py", "phan_tich.py"):
        p(f"- sha256({f}) = `{hashlib.sha256((RA / f).read_bytes()).hexdigest()}`")
    (RA / "LUAT_KHOA.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
