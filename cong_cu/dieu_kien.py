#!/usr/bin/env python3
"""Điều kiện vô hiệu CÓ CẤU TRÚC + giá đóng theo ĐÚNG KHUNG — dùng chung cho bộ chấm (cong_cu/cham_dich.py)
và bộ dựng đề (thi/tao_ho_so.py) để hai bên không lệch nhau (Codex P0-3).

  phan_tich(cau, huong, nguong) → {gia, khung: H4|D1|W1, so_nen: 1|2, chieu: dong_tren|dong_duoi, da_hieu} hoặc None
      None = câu rỗng, hoặc câu nhắc khung nhỏ (M5/M15/M30/H1/"5 phút"/scalp) = mốc thoát lệnh, không phải mốc sai view.
      da_hieu=False = có câu nhưng không tìm được số phía bất lợi → bộ chấm ghi "chưa hiểu", KHÔNG coi là đã vô hiệu.
  lan_kich_hoat(dk, C, den) → giờ ĐÓNG của nến đầu tiên làm điều kiện thành đúng; chỉ xét nến có giờ đóng > C
      (nến mở trước C mà đóng sau C vẫn tính) và ≤ den; so_nen=2 = 2 nến liên tiếp cùng khung đều đóng qua mốc.
  khung_cua_moc / cuc_tri_dong: trạng thái mốc trong hồ sơ — mốc ghi D1/W1/tháng chỉ xét giá đóng của khung đó.

Nguồn nến (giờ trong CSV = giờ MỞ nến UTC): H4 = thi/du_lieu/btc_4H_bo_sung.csv + du_lieu/btc_4H.csv (file chung
ưu tiên khi trùng); D1 = thi/du_lieu/btc_1Dutc_bo_sung.csv + du_lieu/btc_1Dutc.csv (biên 00:00 UTC);
W1 = gộp từ D1, tuần bắt đầu thứ Hai 00:00 UTC, chỉ tuần đủ 7 nến D1. Kiểm thử thay mảng nến bằng dat_nen().
"""
import csv, datetime as dt, re
from bisect import bisect_right
from collections import namedtuple
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
Nen = namedtuple("Nen", "mo dong o h l c")  # cùng tên trường với thi/tao_ho_so.Nen → hàm dưới dùng được cả hai
DO_DAI = {"H4": dt.timedelta(hours=4), "D1": dt.timedelta(days=1)}
NGUON = {"H4": ("thi/du_lieu/btc_4H_bo_sung.csv", "du_lieu/btc_4H.csv"),
         "D1": ("thi/du_lieu/btc_1Dutc_bo_sung.csv", "du_lieu/btc_1Dutc.csv")}

KHUNG_NHO = re.compile(r"\bM(5|15|30)\b|\b(5|15|30) phút|\bH1\b|scalp", re.I)  # như cham_dich cũ
TU_KHUNG = [("W1", re.compile(r"\bW1\b|nến tuần|khung tuần|cây tuần|đóng tuần|weekly", re.I)),
            ("D1", re.compile(r"\bD1\b|nến ngày|khung ngày|cây ngày|đóng ngày|đóng cửa ngày|daily", re.I)),
            ("H4", re.compile(r"\bH4\b", re.I))]
XAC_NHAN = re.compile(r"(confirm|xác nhận)\s*(bằng|bởi)?\s*(nến\s*)?(W1|D1|nến tuần|nến ngày|khung tuần|khung ngày)", re.I)
HAI_NEN = re.compile(r"(?<![\d.,])(2|hai)\s*(cây|nến|H4|D1|W1)", re.I)
MOT_DEN = re.compile(r"(1|một)\s*(-|–|đến|tới|hoặc|hay)\s*$", re.I)  # "1-2 cây", "một đến hai cây" → vẫn là 1 cây
THU_TU = {"H4": 0, "D1": 1, "W1": 2}


# ───────────────────────── tách số / điều kiện ─────────────────────────
def so_trong_vt(text):
    """[(giá, vị trí đầu, vị trí cuối)] — số giá trong câu: '82.000' '81,5K' '81.5k' '82k' '79-80' (quy ra nghìn khi < 1000).
    Thứ tự nhánh regex: '82.000' trước, rồi '81,5', rồi '82' (bản cũ để '82' trước nên '81,5K' bị đọc thành 81.000)."""
    ra = []
    for m in re.finditer(r"(\d{2,3}[.,]\d{3}(?!\d)|\d{2,3}[.,]\d(?!\d)|\d{2,3})\s*(k|K|nghìn)?", text or ""):
        s = m.group(1)
        v = float(s.replace(".", "").replace(",", "")) if re.match(r"\d{2,3}[.,]\d{3}$", s) else float(s.replace(",", "."))
        if v < 1000:
            v *= 1000
        if 10_000 <= v <= 200_000:
            ra.append((v, m.start(), m.end()))
    return ra


def so_trong(text):
    """Các số giá trong câu (như cong_cu/cham_dich.so_trong cũ)."""
    return [v for v, _, _ in so_trong_vt(text)]


def _khung_doan(doan, vts):
    """Khung của số (các vị trí xuất hiện vts, theo thứ tự) trong đoạn: 'confirm/xác nhận bằng D1/W1' → khung đó;
    không thì từ khoá khung gần nhất ĐỨNG TRƯỚC lần xuất hiện sớm nhất có từ khoá đứng trước (nhóm 'A hoặc B' / 'A/B'
    → khung nhỏ hơn = sớm kích hoạt hơn); không có thì từ khoá ngay SAU số (≤ 25 ký tự, không cách bởi dấu ngoặc);
    không có → H4."""
    m = XAC_NHAN.search(doan)
    if m:
        return "W1" if re.search(r"W1|tuần", m.group(4), re.I) else "D1"
    tu = sorted((x.start(), x.end(), k) for k, p in TU_KHUNG for x in p.finditer(doan))
    for vt in vts:
        truoc = [x for x in tu if x[1] <= vt]
        if truoc:
            nhom = [truoc[-1]]
            for x in reversed(truoc[:-1]):  # gom các từ khoá nối nhau bằng "hoặc" / "/" / "hay"
                if re.fullmatch(r"\s*(hoặc|hay|/|,)\s*", doan[x[1]:nhom[-1][0]], re.I):
                    nhom.append(x)
                else:
                    break
            return min((x[2] for x in nhom), key=THU_TU.get)
    for vt in vts:
        sau = [x for x in tu if x[0] >= vt and x[0] - vt <= 25 and not re.search(r"[()]", doan[vt:x[0]])]
        if sau:
            return sau[0][2]
    return "H4"


def phan_tich(cau, huong, nguong):
    """Câu vo_hieu_khi → điều kiện vô hiệu có cấu trúc (xem docstring module).
    Giá = số phía bất lợi gần giá nhất (GIẢM: số > nguong nhỏ nhất; TĂNG: số < nguong lớn nhất), bỏ số dính chữ
    đứng trước (MA200, EMA34 là tên đường, không phải giá). Khung + số nến đọc trong đoạn (tách bằng ';') chứa số đó."""
    cau = cau or ""
    if not cau.strip() or huong not in ("TANG", "GIAM"):
        return None
    # chỉ bỏ ĐOẠN (tách ';') nói khung nhỏ/scalp — mốc thoát lệnh; đoạn H4/D1 cùng câu vẫn là mốc sai của view
    cau = ";".join(d for d in cau.split(";") if not KHUNG_NHO.search(d))
    if not cau.strip():
        return None
    chieu ="dong_tren" if huong == "GIAM" else "dong_duoi"
    so = [(v, a, b) for v, a, b in so_trong_vt(cau) if not (a and cau[a - 1].isalpha())]
    bat_loi = [x for x in so if nguong is not None and (x[0] > nguong if huong == "GIAM" else x[0] < nguong)]
    if not bat_loi:
        return {"gia": None, "khung": None, "so_nen": None, "chieu": chieu, "da_hieu": False}
    gia = (min if huong == "GIAM" else max)(x[0] for x in bat_loi)
    vt = next(a for v, a, b in bat_loi if v == gia)  # lần xuất hiện đầu tiên → đoạn chứa nó
    dau = cau.rfind(";", 0, vt) + 1
    cuoi = cau.find(";", vt); cuoi = len(cau) if cuoi < 0 else cuoi
    doan = cau[dau:cuoi]
    khung = _khung_doan(doan, [a - dau for v, a, b in bat_loi if v == gia and a < cuoi])
    so_nen = 1
    for m in HAI_NEN.finditer(doan):
        if not MOT_DEN.search(doan[:m.start()]):
            so_nen = 2; break
    return {"gia": gia, "khung": khung, "so_nen": so_nen, "chieu": chieu, "da_hieu": True}


def qua(dk, c):
    """Giá đóng c có đóng QUA mốc theo chiều của điều kiện không (so sánh ngặt như cham_dich cũ)."""
    return c > dk["gia"] if dk["chieu"] == "dong_tren" else c < dk["gia"]


# ───────────────────────── dữ liệu nến ─────────────────────────
NEN, DONG = {}, {}


def _doc(ten_file, do_dai):
    gop = {}
    for ten in ten_file:
        p = GOC / ten
        if p.exists():
            with p.open() as f:
                for r in csv.DictReader(f):
                    gop[r["ts_utc"]] = tuple(float(r[k]) for k in ("open", "high", "low", "close"))
    ra = []
    for k in sorted(gop):
        mo = dt.datetime.strptime(k, "%Y-%m-%d %H:%M")
        ra.append(Nen(mo, mo + do_dai, *gop[k]))
    return ra


def gop_tuan(d1):
    """W1 từ D1: tuần bắt đầu thứ Hai 00:00 UTC, chỉ giữ tuần đủ 7 nến D1 (tuần đang chạy chưa có nến W1 đóng)."""
    nhom = {}
    for n in d1:
        bd = (n.mo - dt.timedelta(days=n.mo.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        nhom.setdefault(bd, []).append(n)
    return [Nen(bd, bd + dt.timedelta(days=7), ds[0].o, max(x.h for x in ds), min(x.l for x in ds), ds[-1].c)
            for bd, ds in sorted(nhom.items()) if len(ds) == 7]


def dat_nen(khung, ds):
    """Thay mảng nến của 1 khung (kiểm thử). Đặt D1 thì W1 được dựng lại từ D1."""
    NEN[khung] = list(ds); DONG[khung] = [n.dong for n in NEN[khung]]
    if khung == "D1":
        dat_nen("W1", gop_tuan(NEN["D1"]))


def nap(khung):
    if khung not in NEN:
        if khung == "W1":
            nap("D1")
            if "W1" not in NEN:
                dat_nen("W1", gop_tuan(NEN["D1"]))
        else:
            dat_nen(khung, _doc(NGUON[khung], DO_DAI[khung]))
    return NEN[khung]


def _cung_mui(t, mau):
    """Đưa t về cùng kiểu (có/không múi giờ) với mốc mẫu của mảng nến."""
    if t is None or mau is None:
        return t
    if mau.tzinfo is None and t.tzinfo is not None:
        return t.astimezone(dt.timezone.utc).replace(tzinfo=None)
    if mau.tzinfo is not None and t.tzinfo is None:
        return t.replace(tzinfo=dt.timezone.utc)
    return t


def lan_kich_hoat(dk, C, den, nens=None):
    """Giờ ĐÓNG của nến đầu tiên làm điều kiện thành đúng (None nếu chưa). Chỉ xét nến có C < giờ đóng ≤ den.
    nens=None → dữ liệu chung theo dk['khung']; truyền nens khi cần mảng đã cắt (bộ dựng đề) hoặc khung khác."""
    if not dk or not dk.get("da_hieu"):
        return None
    if nens is None:
        nens, dong = nap(dk["khung"]), DONG[dk["khung"]]
    else:
        dong = [n.dong for n in nens]
    if not nens:
        return None
    C2, den2 = _cung_mui(C, nens[0].dong), _cung_mui(den, nens[0].dong)
    chuoi, truoc = 0, None
    for n in nens[bisect_right(dong, C2):]:
        if n.dong > den2:
            break
        if qua(dk, n.c):
            chuoi = chuoi + 1 if (chuoi and truoc == n.mo) else 1
            if chuoi >= dk["so_nen"]:
                return _cung_mui(n.dong, C)  # cùng kiểu múi giờ với C người gọi truyền vào
        else:
            chuoi = 0
        truoc = n.dong
    return None


# ───────────────────────── trạng thái mốc cho bộ dựng đề ─────────────────────────
def khung_cua_moc(khung):
    """Khung xét GIÁ ĐÓNG của 1 mốc trong hồ sơ: D1/W1/tháng giữ nguyên khung đó (3M dùng tạm nến tháng);
    không ghi khung hoặc khung ≤ H4 (H4, H1, M5…) → H4 như trước."""
    return {"D1": "D1", "1D": "D1", "W1": "W1", "1W": "W1", "MN": "MN", "3M": "MN"}.get(str(khung or "").upper(), "H4")


def cuc_tri_dong(chieu, tu, den, nens):
    """Giá đóng cao nhất (dong_tren) / thấp nhất (dong_duoi) của các nến có tu < giờ đóng ≤ den; không có → None."""
    c = [n.c for n in nens if tu < n.dong <= den]
    return (max(c) if chieu == "dong_tren" else min(c)) if c else None


def trang_thai_dong(gia, chieu, khung, tu, T, nens):
    """Trạng thái 1 mốc giá ĐÓNG tại thời điểm T (bộ dựng đề): chỉ dùng nến `khung` đã đóng trong (tu, T].
    Trả (đã đóng qua?, giá đóng cực trị theo chiều xét hoặc None nếu chưa có nến khung đó đóng)."""
    dk = {"gia": gia, "khung": khung, "so_nen": 1, "chieu": chieu, "da_hieu": True}
    return lan_kich_hoat(dk, tu, T, nens) is not None, cuc_tri_dong(chieu, tu, T, nens)
