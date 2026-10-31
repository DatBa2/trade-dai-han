#!/usr/bin/env python3
"""Chấm 1 nhận định theo cách người đó tự đánh giá (không chấm theo 24h):
  ĐÚNG    = trong hạn của view, giá CHẠM ĐÍCH (râu cũng tính) TRƯỚC khi bị vô hiệu.
  SAI     = bị vô hiệu trước: chạm SL của lệnh (theo giá) hoặc nến H4 ĐÓNG qua mốc sai (luật nến đóng của người đó).
  CHƯA RÕ = hết hạn mà chưa chạm cả hai.
Hạn = han_gio của view, không có thì 7 ngày, tối đa 14 ngày. Đích có đường đi nhiều chặng → đích chặng cuối;
vùng [a, b] → chạm mép gần (GIẢM: b, TĂNG: a). Mốc sai: số trong `vo_hieu_khi` nằm phía bất lợi gần giá nhất;
không có thì SL của lệnh cùng chiều; không có cả hai → chỉ xét chạm đích trong hạn (không chạm = SAI_HET_HAN).
Cách dùng: python3 cong_cu/cham_dich.py [thư mục phiếu=phieu] [--chi-tiet]
"""
import csv, datetime as dt, json, re, sys
from bisect import bisect_left
from collections import Counter, defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
VN = dt.timedelta(hours=7)
HAN_MAC_DINH = int(__import__("os").environ.get("HAN_MAC_DINH", 168))  # giờ; view không nói hạn


def doc(ten):
    with (GOC / "du_lieu" / ten).open() as f:
        return [(dt.datetime.fromisoformat(r["ts_utc"]), float(r["high"]), float(r["low"]), float(r["close"])) for r in csv.DictReader(f)]


H1, H4 = doc("btc_1H.csv"), doc("btc_4H.csv")
T1, T4 = [x[0] for x in H1], [x[0] for x in H4]


def so_trong(text):
    """Các số giá trong câu: '82.000' '81,5K' '81.5k' '82k' '79-80' (quy ra nghìn khi < 1000)."""
    ra = []
    for m in re.finditer(r"(\d{2,3}(?:[.,]\d{3})?|\d{2,3}[.,]\d)\s*(k|K|nghìn)?", text or ""):
        s = m.group(1)
        v = float(s.replace(".", "").replace(",", "")) if re.match(r"\d{2,3}[.,]\d{3}$", s) else float(s.replace(",", "."))
        if v < 1000:
            v *= 1000
        if 10_000 <= v <= 200_000:
            ra.append(v)
    return ra


def chon_view(d):
    nd = d.get("nhan_dinh") or [{}]
    return next((x for k in ("H4", "chung") for x in nd if x.get("khung") == k), nd[0])


def cham(d, bat_dau):
    n = chon_view(d); huong = n.get("huong")
    if huong not in ("TANG", "GIAM"):
        return "PHAN_VAN", None
    dich = (n.get("duong_di") or [{}])[-1].get("dich") if n.get("duong_di") else n.get("dich")
    if isinstance(dich, list):
        dich = [x for x in dich if isinstance(x, (int, float))]
        dich = (max(dich) if huong == "GIAM" else min(dich)) if dich else None
    if not isinstance(dich, (int, float)):
        return "KHONG_DICH", None
    i0 = bisect_left(T1, bat_dau)
    if i0 >= len(H1):
        return "CHUA_DU_LIEU", None
    gia = H1[i0 - 1][3] if i0 else H1[0][3]
    if (huong == "GIAM" and dich >= gia) or (huong == "TANG" and dich <= gia):
        return "DICH_SAI_PHIA", None  # đích nằm phía bên kia giá lúc nói (thường là chặng 1 / lỗi phiếu)
    # đường đi 2 chặng: chặng 1 ngược hướng là CÓ CHỦ ĐÍCH → mốc sai/SL phải nằm xa hơn đích chặng 1
    nguong = gia
    dd = n.get("duong_di") or []
    if len(dd) >= 2 and dd[0].get("huong") not in (huong, None):
        c1 = dd[0].get("dich"); c1 = [x for x in (c1 if isinstance(c1, list) else [c1]) if isinstance(x, (int, float))]
        if c1:
            nguong = max(c1 + [gia]) if huong == "GIAM" else min(c1 + [gia])
    vh = n.get("vo_hieu_khi") or ""
    # mốc thoát lệnh khung nhỏ (scalp) không phải mốc sai của view H4
    bat_loi = [] if re.search(r"\bM(5|15|30)\b|\b(5|15|30) phút|\bH1\b|scalp", vh, re.I) else \
        [v for v in so_trong(vh) if (v > nguong if huong == "GIAM" else v < nguong)]
    moc_sai = (min(bat_loi) if huong == "GIAM" else max(bat_loi)) if bat_loi else None
    def so_dau(x):
        x = x[0] if isinstance(x, list) and x else x
        return x if isinstance(x, (int, float)) else None
    sl = next((so_dau(l.get("sl")) for l in d.get("lenh") or [] if so_dau(l.get("sl")) is not None
               and l.get("trang_thai") == "de_xuat_moi" and l.get("chieu") == ("SHORT" if huong == "GIAM" else "LONG")
               and (so_dau(l.get("sl")) > nguong if huong == "GIAM" else so_dau(l.get("sl")) < nguong)), None)
    han = int(__import__("os").environ["HAN_CO_DINH"]) if __import__("os").environ.get("HAN_CO_DINH") else min(n.get("han_gio") or HAN_MAC_DINH, 336)
    het = bat_dau + dt.timedelta(hours=han)
    j0 = bisect_left(T4, bat_dau)
    for t, h, l, c in H1[i0:]:
        if t >= het:
            break
        cham_dich = l <= dich if huong == "GIAM" else h >= dich
        cham_sl = sl is not None and (h >= sl if huong == "GIAM" else l <= sl)
        if cham_sl and not cham_dich:
            return "SAI", (t + VN).strftime("%d/%m %H:%M")
        if cham_dich:
            return "DUNG", (t + VN).strftime("%d/%m %H:%M")
        # nến H4 đóng qua mốc sai: kiểm ở giờ đóng của nến H4
        if moc_sai is not None and (t + dt.timedelta(hours=1)).hour % 4 == 0:
            k = bisect_left(T4, t - dt.timedelta(hours=3))
            if k < len(H4) and H4[k][0] >= bat_dau and (H4[k][3] > moc_sai if huong == "GIAM" else H4[k][3] < moc_sai):
                return "SAI", (t + VN).strftime("%d/%m %H:%M")
    return ("CHUA_RO" if (moc_sai or sl) else "SAI_HET_HAN"), None


def main():
    thu_muc = GOC / (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "phieu")
    dem, thang = Counter(), defaultdict(Counter)
    for p in sorted(thu_muc.glob("2*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        gio = re.search(r"_(\d{2})(\d{2})_", p.name)
        bd = dt.datetime.fromisoformat(d["ngay"]) + (dt.timedelta(hours=int(gio[1]), minutes=int(gio[2])) if gio else dt.timedelta(hours=10)) - VN
        kq, luc = cham(d, bd)
        dem[kq] += 1; thang[d["ngay"][:7]][kq] += 1
        if "--chi-tiet" in sys.argv:
            print(d["ngay"], chon_view(d).get("huong"), kq, luc or "")
    co = dem["DUNG"] + dem["SAI"] + dem["SAI_HET_HAN"]
    print(f"{sum(dem.values())} phiếu: {dict(dem)}")
    if co:
        print(f"ĐÚNG {dem['DUNG']}/{co} = {dem['DUNG'] / co:.0%}  (đã ngã ngũ: đúng + sai + hết hạn không chạm đích; chưa rõ {dem['CHUA_RO']})")
    for t in sorted(thang):
        c = thang[t]; n = c["DUNG"] + c["SAI"] + c["SAI_HET_HAN"]
        print(f"  {t}: đúng {c['DUNG']}/{n}" + (f" = {c['DUNG'] / n:.0%}" if n else "") + f" · phân vân {c['PHAN_VAN']} · chưa rõ {c['CHUA_RO']}")


if __name__ == "__main__":
    main()
