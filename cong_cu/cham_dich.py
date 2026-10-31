#!/usr/bin/env python3
"""Chấm 1 nhận định theo cách người đó tự đánh giá (không chấm theo 24h):
  ĐÚNG    = trong hạn, giá CHẠM ĐÍCH (râu cũng tính) TRƯỚC khi bị vô hiệu.
  SAI     = bị vô hiệu trước: chạm SL của lệnh (theo giá) hoặc điều kiện vô hiệu thành đúng (nến ĐÚNG KHUNG ghi trong
            câu ĐÓNG qua mốc sai, đủ số nến — cong_cu/dieu_kien.py).
  CHUA_RO = hết hạn mà chưa chạm cả hai (có mốc sai/SL). SAI_HET_HAN = không có mốc sai/SL, hết hạn chưa chạm đích.
  CHUA_RO_THU_TU = đích và SL chạm trong CÙNG nến 1m (hoặc thiếu nến 1m) → không biết cái nào trước. KHÔNG mặc định ĐÚNG.
  CHUA_HET_HAN = chưa có sự kiện quyết định mà dữ liệu chưa phủ hết hạn.
Thời điểm (Codex P0-2/3/4); C = lúc nhận định, giờ UTC không múi:
  - Giá tham chiếu = close của nến 5m CUỐI CÙNG có giờ ĐÓNG ≤ C (close đã tồn tại tại C).
  - Diễn biến quét bằng nến 5m có giờ MỞ ≥ C. Nến 5m chứa C (mở < C < đóng) bị bỏ: có KHOẢNG TRỐNG < 5 PHÚT ngay sau C
    không được chấm (đổi lại không dùng giá trước C để tính chạm đích/SL).
  - Chạm đích/SL tính tại giờ MỞ nến 5m; vô hiệu tính tại giờ ĐÓNG nến khung của nó (H4/D1/W1, 1–2 nến, chỉ nến có
    giờ đóng > C — nến mở trước C mà đóng sau C ĐƯỢC tính). Vô hiệu có giờ đóng ≤ giờ mở nến 5m chạm đích → SAI.
  - Đích + SL cùng nến 5m → tải 1m của đúng 5 phút đó (cong_cu/lay_nen.lay_1m, cache du_lieu/btc_1m_cache.csv).
Hạn: trả cả hạn cố định (HAN_CO_DINH, mặc định 336 giờ) lẫn hạn của chính view (han_gio, trần 336, không có thì 168).
  cham() giữ hành vi cũ: có biến môi trường HAN_CO_DINH → hạn cố định, không thì hạn của view.
Đích: đường đi nhiều chặng → đích chặng cuối; vùng [a, b] → mép gần (GIẢM: b, TĂNG: a). Mốc sai: số trong vo_hieu_khi
phía bất lợi gần giá nhất (đường 2 chặng ngược hướng: phải xa hơn đích chặng 1); không có thì SL của lệnh cùng chiều;
không có cả hai → chỉ xét chạm đích trong hạn (không chạm = SAI_HET_HAN).
ket_qua_duong_di (view ≥ 2 chặng): ĐÚNG khi chạm lần lượt đích từng chặng (chặng 1 trước) rồi mới tới đích cuối, trước
SL/vô hiệu; tới đích cuối khi chưa qua chặng trước → SAI_THU_TU. Báo riêng, không thay kết quả chính.
Cách dùng: python3 cong_cu/cham_dich.py [thư mục phiếu=phieu] [--chi-tiet]
  C = giờ bắt đầu thật + số phút (transcripts/gio_live.tsv) khi có; không thì HHMM trong tên phiếu / 10:00 VN như cũ.
"""
import csv, datetime as dt, json, os, re, sys
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dieu_kien  # noqa: E402
import lay_nen  # noqa: E402
from dieu_kien import so_trong  # noqa: E402,F401  (giữ cd.so_trong cho code cũ)

GOC = Path(__file__).resolve().parent.parent
VN = dt.timedelta(hours=7)
NAM_PHUT = dt.timedelta(minutes=5)
HAN_MAC_DINH = int(os.environ.get("HAN_MAC_DINH", 168))  # giờ; view không nói hạn
HAN_TRAN = 336
TRE_GIA_TOI_DA = dt.timedelta(hours=1)  # nến 5m tham chiếu cách C quá mức này → coi như thiếu dữ liệu
MAU_TEN = re.compile(r"^(\d{4}-\d{2}-\d{2})_(?:(\d{4})_)?(.{11})$")


def doc(ten):
    with (GOC / "du_lieu" / ten).open() as f:
        return [(dt.datetime.fromisoformat(r["ts_utc"]), float(r["high"]), float(r["low"]), float(r["close"])) for r in csv.DictReader(f)]


H1, H4 = doc("btc_1H.csv"), doc("btc_4H.csv")  # giữ cho code cũ đọc cd.H1/cd.T1; bộ chấm mới dùng 5m
T1, T4 = [x[0] for x in H1], [x[0] for x in H4]
M5, T5 = None, None


def dat_5m(ds):
    """Thay mảng nến 5m [(giờ mở UTC, high, low, close)] (kiểm thử)."""
    global M5, T5
    M5 = list(ds); T5 = [x[0] for x in M5]


def nen_5m():
    if M5 is None:
        dat_5m(doc("btc_5m.csv") if (GOC / "du_lieu" / "btc_5m.csv").exists() else [])
    return M5


def lay_1m(t5):
    """5 nến 1m của nến 5m mở lúc t5 → [(giờ mở, high, low, close)] (kiểm thử thay hàm này)."""
    return lay_nen.lay_1m(t5, t5 + NAM_PHUT)


def thu_tu_1m(t5, a, b):
    """Trong nến 5m mở t5, a/b: hàm (high, low) → bool. 'A' = a xảy ra ở nến 1m sớm hơn b, 'B' = ngược lại,
    'CUNG' = cùng nến 1m, 'THIEU' = không đủ 5 nến 1m hoặc 1m không khớp 5m."""
    try:
        ds = lay_1m(t5)
    except Exception as e:  # mạng lỗi → không đoán
        print(f"! không tải được 1m {t5}: {e}", file=sys.stderr)
        return "THIEU"
    if len(ds) < 5:
        return "THIEU"
    ia = next((i for i, (_, h, l, _) in enumerate(ds) if a(h, l)), None)
    ib = next((i for i, (_, h, l, _) in enumerate(ds) if b(h, l)), None)
    if ia is None or ib is None:
        return "THIEU"
    return "A" if ia < ib else ("B" if ib < ia else "CUNG")


def chon_view(d):
    nd = d.get("nhan_dinh") or [{}]
    return next((x for k in ("H4", "chung") for x in nd if x.get("khung") == k), nd[0])


def so_list(x):
    return [v for v in (x if isinstance(x, list) else [x]) if isinstance(v, (int, float))]


def gia_tham_chieu(C):
    """(close, giờ đóng, chỉ số nến 5m đầu tiên có giờ mở ≥ C) — close của nến 5m cuối có giờ đóng ≤ C."""
    M = nen_5m()
    i = bisect_right(T5, C - NAM_PHUT) - 1
    if i < 0 or C - (M[i][0] + NAM_PHUT) > TRE_GIA_TOI_DA:
        return None, None, bisect_left(T5, C)
    return M[i][3], M[i][0] + NAM_PHUT, bisect_left(T5, C)


def cham_chi_tiet(d, C, han_gio=None):
    """Chấm đầy đủ 1 phiếu/bài làm tại mốc C (datetime UTC không múi). han_gio = hạn cố định (None → HAN_CO_DINH/336).
    Trả dict: ket_qua/luc/su_kien (theo hạn cố định), han_co_dinh + han_view {gio, ket_qua, luc, su_kien, duong_di},
    ket_qua_duong_di, gia_tham_chieu, gio_gia, C, huong, dich, nguong, moc_sai, dieu_kien, sl, vo_hieu_chua_hieu, chang."""
    han_cd = int(han_gio or os.environ.get("HAN_CO_DINH") or HAN_TRAN)
    n = chon_view(d); huong = n.get("huong")
    hg = n.get("han_gio")
    han_v = min(hg if isinstance(hg, (int, float)) and hg > 0 else HAN_MAC_DINH, HAN_TRAN)
    dd = n.get("duong_di") or []
    r = {"C": C, "huong": huong, "gia_tham_chieu": None, "gio_gia": None, "dich": None, "nguong": None, "moc_sai": None,
         "dieu_kien": None, "sl": None, "vo_hieu_chua_hieu": False, "chang": None, "nhieu_chang": len(dd) >= 2,
         "di_nguoc": len(dd) >= 2 and any(x.get("huong") not in (huong, None) for x in dd[:-1])}  # có chặng cố ý đi ngược view

    def xong(ma):
        for k, gio in (("han_co_dinh", han_cd), ("han_view", han_v)):
            r[k] = {"gio": gio, "ket_qua": ma, "luc": None, "su_kien": None, "duong_di": None}
        r.update(ket_qua=ma, luc=None, su_kien=None, ket_qua_duong_di=None)
        return r

    if huong not in ("TANG", "GIAM"):
        return xong("PHAN_VAN")
    dich = dd[-1].get("dich") if dd else n.get("dich")
    if isinstance(dich, list):
        dich = so_list(dich)
        dich = (max(dich) if huong == "GIAM" else min(dich)) if dich else None
    if not isinstance(dich, (int, float)):
        return xong("KHONG_DICH")
    r["dich"] = dich
    gia, gio_gia, i0 = gia_tham_chieu(C)
    if gia is None:
        return xong("CHUA_DU_LIEU")
    r.update(gia_tham_chieu=gia, gio_gia=gio_gia)
    if (huong == "GIAM" and dich >= gia) or (huong == "TANG" and dich <= gia):
        return xong("DICH_SAI_PHIA")  # đích nằm phía bên kia giá lúc nói (thường là chặng 1 / lỗi phiếu)
    # đường đi 2 chặng: chặng 1 ngược hướng là CÓ CHỦ ĐÍCH → mốc sai/SL phải nằm xa hơn đích chặng 1
    nguong = gia
    if len(dd) >= 2 and dd[0].get("huong") not in (huong, None):
        c1 = so_list(dd[0].get("dich"))
        if c1:
            nguong = max(c1 + [gia]) if huong == "GIAM" else min(c1 + [gia])
    r["nguong"] = nguong
    dk = dieu_kien.phan_tich(n.get("vo_hieu_khi"), huong, nguong)
    r["dieu_kien"] = dk
    r["vo_hieu_chua_hieu"] = bool(dk) and not dk["da_hieu"]
    moc_sai = dk["gia"] if dk and dk["da_hieu"] else None
    r["moc_sai"] = moc_sai

    def so_dau(x):
        x = x[0] if isinstance(x, list) and x else x
        return x if isinstance(x, (int, float)) else None
    sl = next((so_dau(l.get("sl")) for l in d.get("lenh") or [] if so_dau(l.get("sl")) is not None
               and l.get("trang_thai") == "de_xuat_moi" and l.get("chieu") == ("SHORT" if huong == "GIAM" else "LONG")
               and (so_dau(l.get("sl")) > nguong if huong == "GIAM" else so_dau(l.get("sl")) < nguong)), None)
    r["sl"] = sl

    # ── quét sự kiện tới hạn dài nhất ──
    M = nen_5m()
    het_max = C + dt.timedelta(hours=max(han_cd, han_v))
    het_du_lieu = M[-1][0] + NAM_PHUT if M else C
    toi = (lambda h, l: l <= dich) if huong == "GIAM" else (lambda h, l: h >= dich)
    sl_cham = None if sl is None else ((lambda h, l: h >= sl) if huong == "GIAM" else (lambda h, l: l <= sl))
    t_d = t_s = None
    for t, h, l, c in M[i0:]:
        if t >= het_max:
            break
        if t_d is None and toi(h, l):
            t_d = t
        if sl_cham and t_s is None and sl_cham(h, l):
            t_s = t
        if t_d is not None and (sl_cham is None or t_s is not None):
            break
    t_v = dieu_kien.lan_kich_hoat(dk, C, het_max) if moc_sai is not None else None
    nho = {}

    def thu_tu(t, a, b):
        if (t, a, b) not in nho:
            nho[(t, a, b)] = thu_tu_1m(t, a, b)
        return nho[(t, a, b)]

    # ── đường đi nhiều chặng: lần lượt từng chặng ──
    chang, dd_su_kien = None, None  # dd_su_kien = (giờ mở nến 5m, loại: xong | sai_thu_tu | chua_ro_thu_tu)
    if len(dd) >= 2:
        chang = []
        for x in dd:
            hk, v = x.get("huong"), so_list(x.get("dich"))
            if hk not in ("TANG", "GIAM") or not v:
                chang = None; break
            chang.append((hk, max(v) if hk == "GIAM" else min(v)))
        r["chang"] = chang
    if chang:
        def ham(k):
            hk, muc = chang[k]
            return (lambda h, l: l <= muc) if hk == "GIAM" else (lambda h, l: h >= muc)
        cham_k = [ham(k) for k in range(len(chang))]
        cuoi, k = len(chang) - 1, 0
        for t, h, l, c in M[i0:]:
            if t >= het_max:
                break
            if k < cuoi and cham_k[cuoi](h, l) and not cham_k[k](h, l):
                dd_su_kien = (t, "sai_thu_tu"); break  # tới đích cuối khi chưa qua chặng k
            if not cham_k[k](h, l):
                continue
            if k == cuoi:
                dd_su_kien = (t, "xong"); break
            k += 1
            if not cham_k[k](h, l):
                continue
            # chặng kế cũng chạm trong CÙNG nến 5m → phân thứ tự bằng 1m
            o = thu_tu(t, cham_k[k - 1], cham_k[k])
            if k == cuoi:
                dd_su_kien = (t, {"A": "xong", "B": "sai_thu_tu"}.get(o, "chua_ro_thu_tu")); break
            if o == "A":
                k += 1  # chặng giữa qua đúng thứ tự ngay trong nến này; chặng sau xét từ nến kế (bảo thủ)
        r["cham_chang_cuoi"] = cham_k[cuoi]

    def khong_su_kien(het):
        if het > het_du_lieu:
            return "CHUA_HET_HAN", None, None
        return ("CHUA_RO" if (moc_sai is not None or sl is not None) else "SAI_HET_HAN"), None, None

    def quyet(het):
        """Sự kiện đầu tiên trong hạn (vô hiệu: giờ đóng ≤ het; chạm: giờ mở nến 5m < het)."""
        ev = []
        if t_v is not None and t_v <= het:
            ev.append((t_v, 0, "vo_hieu"))  # cùng giờ với nến 5m mở lúc đó → vô hiệu (đã đóng) xếp trước
        if t_d is not None and t_d < het:
            ev.append((t_d, 1, "dich"))
        if t_s is not None and t_s < het:
            ev.append((t_s, 1, "sl"))
        if not ev:
            return khong_su_kien(het)
        t, _, loai = min(ev)
        if loai == "vo_hieu":
            return "SAI", t, "vo_hieu"
        if t_d == t and t_s == t:  # đích và SL cùng nến 5m
            o = thu_tu(t, toi, sl_cham)
            return {"A": ("DUNG", t, "dich (1m)"), "B": ("SAI", t, "sl (1m)")}.get(o, ("CHUA_RO_THU_TU", t, f"dich+sl cùng nến ({o})"))
        return ("DUNG" if loai == "dich" else "SAI"), t, loai

    def quyet_dd(het):
        if not chang:
            return None
        ev = []
        if t_v is not None and t_v <= het:
            ev.append((t_v, 0, "vo_hieu"))
        if t_s is not None and t_s < het:
            ev.append((t_s, 1, "sl"))
        if dd_su_kien and dd_su_kien[0] < het:
            ev.append((dd_su_kien[0], 1, dd_su_kien[1]))
        if not ev:
            return khong_su_kien(het)[0]
        t, _, loai = min(ev, key=lambda x: (x[0], x[1]))  # cùng giờ: SL xếp trước sự kiện đường đi → xét 1m bên dưới
        if loai == "vo_hieu":
            return "SAI"
        if loai == "sl":
            if dd_su_kien and dd_su_kien[0] == t and dd_su_kien[1] == "xong":  # SL và đích cuối cùng nến 5m
                o = thu_tu(t, r["cham_chang_cuoi"], sl_cham)
                return {"A": "DUNG", "B": "SAI"}.get(o, "CHUA_RO_THU_TU")
            return "SAI"
        return {"xong": "DUNG", "sai_thu_tu": "SAI_THU_TU", "chua_ro_thu_tu": "CHUA_RO_THU_TU"}[loai]

    for k, gio in (("han_co_dinh", han_cd), ("han_view", han_v)):
        het = C + dt.timedelta(hours=gio)
        ma, t, sk = quyet(het)
        r[k] = {"gio": gio, "ket_qua": ma, "luc": (t + VN).strftime("%d/%m %H:%M") if t else None, "su_kien": sk,
                "duong_di": quyet_dd(het)}
    r.pop("cham_chang_cuoi", None)
    r.update(ket_qua=r["han_co_dinh"]["ket_qua"], luc=r["han_co_dinh"]["luc"], su_kien=r["han_co_dinh"]["su_kien"],
             ket_qua_duong_di=r["han_co_dinh"]["duong_di"])
    return r


def cham(d, bat_dau):
    """Chữ ký cũ: (kết quả, lúc). Có biến môi trường HAN_CO_DINH → hạn cố định; không thì hạn của view."""
    r = cham_chi_tiet(d, bat_dau)
    h = r["han_co_dinh"] if os.environ.get("HAN_CO_DINH") else r["han_view"]
    return h["ket_qua"], h["luc"]


def gio_live():
    """id video → (giờ bắt đầu UTC không múi, số phút) từ transcripts/gio_live.tsv."""
    ra, p = {}, GOC / "transcripts" / "gio_live.tsv"
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8"), delimiter="\t"):
            try:
                ra[r["id"]] = (dt.datetime.strptime(r["bat_dau_vn"].strip(), "%Y-%m-%d %H:%M") - VN, int(r["phut"]))
            except (KeyError, ValueError, TypeError):
                pass
    return ra


def moc_C(p, d, that):
    """C của 1 phiếu: giờ live thật + số phút (kết thúc live) khi có; không thì HHMM trong tên / 10:00 VN (như cũ)."""
    m = MAU_TEN.match(p.stem)
    if m and m[3] in that:
        bd, ph = that[m[3]]
        return bd + dt.timedelta(minutes=ph), True
    gio = re.search(r"_(\d{2})(\d{2})_", p.name)
    return dt.datetime.fromisoformat(d["ngay"]) + (dt.timedelta(hours=int(gio[1]), minutes=int(gio[2])) if gio else dt.timedelta(hours=10)) - VN, False


def main():
    thu_muc = GOC / (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "phieu")
    dem, thang = Counter(), defaultdict(Counter)
    that = gio_live()
    so_that = chua_hieu = 0
    for p in sorted(thu_muc.glob("2*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        C, co_that = moc_C(p, d, that)
        so_that += co_that
        r = cham_chi_tiet(d, C)
        chua_hieu += r["vo_hieu_chua_hieu"]
        kq, luc = cham(d, C)
        dem[kq] += 1; thang[d["ngay"][:7]][kq] += 1
        if "--chi-tiet" in sys.argv:
            print(d["ngay"], chon_view(d).get("huong"), kq, luc or "", f"C={C:%m-%d %H:%M}Z", f"giá={r['gia_tham_chieu']}",
                  f"vô hiệu={r['dieu_kien']}" if r["dieu_kien"] else "")
    co = dem["DUNG"] + dem["SAI"] + dem["SAI_HET_HAN"]
    print(f"{sum(dem.values())} phiếu ({so_that} có giờ live thật → C = kết thúc live): {dict(dem)}")
    print(f"vô hiệu có câu nhưng không hiểu được: {chua_hieu}")
    if co:
        print(f"ĐÚNG {dem['DUNG']}/{co} = {dem['DUNG'] / co:.0%}  (đã ngã ngũ: đúng + sai + hết hạn không chạm đích; "
              f"chưa rõ {dem['CHUA_RO']}, chưa rõ thứ tự {dem['CHUA_RO_THU_TU']})")
    for t in sorted(thang):
        c = thang[t]; n = c["DUNG"] + c["SAI"] + c["SAI_HET_HAN"]
        print(f"  {t}: đúng {c['DUNG']}/{n}" + (f" = {c['DUNG'] / n:.0%}" if n else "") + f" · phân vân {c['PHAN_VAN']} · chưa rõ {c['CHUA_RO']}")


if __name__ == "__main__":
    main()
