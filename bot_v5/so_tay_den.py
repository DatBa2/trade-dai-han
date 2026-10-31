#!/usr/bin/env python3
"""Sổ tay LỌC THEO T cho bot v5 — chặn rò rỉ đáp án (view thật / diễn biến thật của người đó ở hoặc sau T).

Cách dùng (T là giờ VN, giống ngu_canh.py):
  python3 bot_v5/so_tay_den.py "2026-09-21 11:00"
  python3 bot_v5/so_tay_den.py "2026-09-21 11:00" --ra <thu_muc>     (mặc định bot_v5/_so_tay_T/)

Ghi ra thư mục đích 4 file: 3 sổ tay (bot_v5/so_tay/*.md) + giong_noi.md (phần C của so_tay/SO_TAY_TINH_HOA.md, từ dòng
`# PHẦN C` tới trước `# PHẦN D`). Luật lọc (han = NGÀY của T, cùng ngày cũng bỏ):
  - mốc ngày nhận dạng: `2026-MM-DD`, `DD/MM/YYYY`, `MM/YYYY` (cả tháng), `MM-DD` / `[MM-DD]` / `[MM-DD · hh:mm:ss](link)` /
    `MM-DD → MM-DD` / `MM-DD/DD`, `DD/MM` (năm 2026; không tính phân số kiểu `10/22 = 45%`), link YouTube `v=<id>` và
    tên ảnh `<id>_<hhmmss>.jpg` (= ngày của buổi, tra `transcripts/danh_sach.tsv`), ô tháng `| T7 |` và nhãn `**Tháng 7**`
    (cả tháng: tháng ≥ tháng của T thì bỏ);
  - dòng có dấu hiệu KẾT QUẢ sau lúc nói ("Đo:", "đạt", "quá mép", "không về"…) được cộng thêm BIEN_DO ngày;
  - bỏ CẢ DÒNG / hàng bảng có BẤT KỲ mốc ≥ han, kèm các dòng con thụt sâu hơn (gạch đầu dòng con của mục ví dụ đó),
    bảng ngay sau một dòng bị bỏ kết thúc bằng ':', và dòng nhãn trơ trọi (vd "- **Ví dụ**:") khi mọi dòng con đã bỏ;
  - riêng giong_noi.md: mỗi câu mẫu `"…" [MM-DD]` (ngăn bởi ` · `, `; `, `. `) là một mục ví dụ → bỏ từng câu, hàng / dòng
    không còn câu nào thì bỏ cả hàng / dòng;
  - cột "Ngày tới lần đổi" (bảng đợt view): ngày đầu đợt + N ≥ han → thay bằng "—" (lộ ngày đổi view);
  - dòng KHÔNG có ngày nhưng có mức giá BTC (`85,5k`, `81–82k`, `59.809`) mà mức đó chỉ xuất hiện (trong dòng có ngày,
    gắn mốc gần nhất) từ han trở đi → bỏ (vd "(85,0–85,5k; 81–82k)" lấy từ ví dụ tháng 10);
  - giữ tiêu đề, `<details>`, luật / số [đo] tổng hợp không kèm ngày; bảng luôn còn hàng tiêu đề + hàng kẻ.
Đầu mỗi file: 1 dòng "Lọc theo T = …; bỏ N dòng có ngày ≥ T". In số dòng bỏ mỗi file.
Kiểm: python3 bot_v5/kiem_tra_so_tay_den.py
"""
import argparse, datetime as dt, re, sys
from pathlib import Path

DAY = Path(__file__).resolve().parent
GOC = DAY.parent
NGUON = [DAY / "so_tay" / "1_huong_giu_lat_tin.md", DAY / "so_tay" / "2_trendline_nen_volume.md",
         DAY / "so_tay" / "3_do_ve_vung_vao_tranh.md"]
TINH_HOA = GOC / "so_tay" / "SO_TAY_TINH_HOA.md"
DANH_SACH = GOC / "transcripts" / "danh_sach.tsv"
RA_MAC_DINH = DAY / "_so_tay_T"
NAM = 2026          # năm của mốc không ghi năm (MM-DD, DD/MM, T7)
BIEN_DO = 30        # ngày: dòng kết quả ("Đo:"…) mô tả diễn biến SAU mốc → coi như kéo tới mốc + 30 ngày
VN = dt.timezone(dt.timedelta(hours=7))

# ======================= nhận dạng mốc ngày =======================
R_LINK = re.compile(r"\]\((?:https?://|\.\./|\./)[^)\s]*\)")
R_VIDEO = re.compile(r"(?:[?&]v=|youtu\.be/)([\w-]{11})")
R_ANH = re.compile(r"([\w-]{11})_\d{6}\.jpg")
R_DU_BAO = re.compile(r"(?<!\w)[TQ]\d{1,2}(?:\s*[-–]\s*[TQ]?\d{1,2})?/20\d\d")  # "T11-12/2026", "Q2/2027" = dự báo
R_ISO = re.compile(r"(?<!\d)(20\d\d)-(\d\d)-(\d\d)(?!\d)")
R_DMY = re.compile(r"(?<![\d/])(\d{1,2})/(\d{1,2})/(20\d\d)(?!\d)")
R_MY = re.compile(r"(?<![\d/])(\d{1,2})/(20\d\d)(?!\d)")
R_MD = re.compile(r"(?<![\w.,:-])(\d{2})-(\d{2})(?![\d:])(?:/(\d{2})(?![\d-]))?")
R_DM = re.compile(r"(?<![\w/.,])(\d{2})/(\d{2})(?![\d/])(?!\s*=)")
R_DM_NGAY = re.compile(r"(?:ngày\s+)(\d{1,2})/(\d{1,2})(?![\d/])|(?<![\w/.,])(\d{1,2})/(\d{1,2})(?![\d/])"
                       r"(?=\s+(?:sáng|đêm|chiều|tối|trưa)\b)")
R_THANG_O = re.compile(r"^\**\s*T(\d{1,2})\s*\**$")                      # ô bảng "T7"
R_NHAN_THANG = re.compile(r"^\s*(?:>\s*)?(?:[-*+]\s+)?\*\*Tháng\s+(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?\*\*")  # "- **Tháng 9–10**:"
R_KQ = re.compile(r"\bĐo\b(?!/)|\bđạt\b|quá mép|không về|không tới|rồi lên|rồi xuống|sau đó giá|giá rụng|rụng tiếp|lên tận|về đúng")

_NGAY_VIDEO = None


def ngay_video():
    """{video id: ngày buổi} từ transcripts/danh_sach.tsv (cột id, ngay) + tên file transcript YYYY-MM-DD_HHMM_ID.*"""
    global _NGAY_VIDEO
    if _NGAY_VIDEO is None:
        ra = {}
        try:
            for dong in DANH_SACH.read_text(encoding="utf-8").split("\n")[1:]:
                o = dong.split("\t")
                if len(o) >= 2 and re.fullmatch(r"\d{4}-\d\d-\d\d", o[1].strip()):
                    ra[o[0].strip()] = dt.date.fromisoformat(o[1].strip())
        except OSError:
            pass
        for p in (GOC / "transcripts").glob("*/20??-??-??_????_*.*"):
            m = re.match(r"(\d{4}-\d\d-\d\d)_\d{4}_([\w-]{11})\.\w+$", p.name)
            if m:
                ra.setdefault(m[2], dt.date.fromisoformat(m[1]))
        _NGAY_VIDEO = ra
    return _NGAY_VIDEO


def _ngay(y, m, d):
    try:
        return dt.date(y, m, d)
    except ValueError:
        return None


def _cuoi_thang(y, m):
    if not 1 <= m <= 12:
        return None
    return dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)


def tim_ngay_vt(s):
    """Mọi mốc ngày trong chuỗi s: list (vị trí ký tự, date). Mốc tháng = ngày cuối tháng (thận trọng)."""
    bang = ngay_video()
    ra = [(m.start(), bang[m[1]]) for r in (R_VIDEO, R_ANH) for m in r.finditer(s) if m[1] in bang]

    def xoa(m):
        return " " * (m.end() - m.start())

    # thay bằng khoảng trắng cùng độ dài → vị trí khớp chuỗi gốc
    s = R_LINK.sub(lambda m: "](" + " " * (len(m.group(0)) - 3) + ")", s)
    s = R_ANH.sub(xoa, R_DU_BAO.sub(xoa, s))

    def quet(r, ham):
        nonlocal s
        for m in r.finditer(s):
            x = ham(m)
            if x:
                ra.extend((m.start(), y) for y in (x if isinstance(x, list) else [x]))
        s = r.sub(xoa, s)

    # năm > NAM = mốc DỰ BÁO (vd "halving 4/2028", "Q2/2027"), không phải sự kiện đã xảy ra → không tính
    quet(R_ISO, lambda m: _ngay(int(m[1]), int(m[2]), int(m[3])) if int(m[1]) <= NAM else None)
    quet(R_DMY, lambda m: _ngay(int(m[3]), int(m[2]), int(m[1])) if int(m[3]) <= NAM else None)
    quet(R_MY, lambda m: _cuoi_thang(int(m[2]), int(m[1])) if int(m[2]) <= NAM else None)

    def md(m):
        a = _ngay(NAM, int(m[1]), int(m[2]))
        if not a:
            return None
        b = _ngay(NAM, int(m[1]), int(m[3])) if m[3] else None
        return [a] + ([b] if b else [])
    quet(R_MD, md)

    def dm(m):
        a = _ngay(NAM, int(m[2]), int(m[1]))
        if a:
            return a
        # DD/MM không hợp lệ: chỉ coi là MM/DD khi đứng cạnh mũi tên khoảng ngày (vd "08/28 → 10/22")
        canh = s[max(0, m.start() - 4):m.start()] + s[m.end():m.end() + 4]
        return _ngay(NAM, int(m[1]), int(m[2])) if "→" in canh else None
    quet(R_DM, dm)
    quet(R_DM_NGAY, lambda m: _ngay(NAM, int(m[2] or m[4]), int(m[1] or m[3])))
    m = R_NHAN_THANG.match(s)
    if m:
        ra.append((m.start(), _cuoi_thang(NAM, int(m[2] or m[1]))))
    return [(v, x) for v, x in ra if x]


def tim_ngay(s):
    """Mọi mốc ngày trong chuỗi s (list date)."""
    return [x for _, x in tim_ngay_vt(s)]


def ngay_hieu_luc(s):
    """Mốc dùng để so với han: mốc trong s; s có dấu hiệu kết quả (Đo:…) → thêm mốc lớn nhất + BIEN_DO."""
    ds = tim_ngay(s)
    if ds and R_KQ.search(s):
        ds.append(max(ds) + dt.timedelta(days=BIEN_DO))
    return ds


def qua_han(s, han):
    ds = ngay_hieu_luc(s)
    return bool(ds) and max(ds) >= han


# ======================= giá không kèm ngày =======================
# Dòng KHÔNG có ngày nhưng có mức giá BTC (vd "(85,0–85,5k; 81–82k)") thường lấy từ một ví dụ có ngày ở chỗ khác.
# gia_dau = {giá (nghìn, 1 số lẻ): ngày sớm nhất mức đó xuất hiện trong một dòng CÓ ngày (gắn với mốc ngày GẦN NHẤT
# trong dòng / ô bảng, vd "Đo: 22/04 đỉnh 79.462" → 22/04; "~126k (06/10/2025)" → 2025-10-06; ô bảng không có ngày →
# ngày lớn nhất của hàng)}.
# Mức giá chỉ xuất hiện từ ngày ≥ han → dòng không ngày đó coi như ví dụ sau T → bỏ.
R_GIA_K = re.compile(r"(?<![\d.,])(\d{2,3}(?:[.,]\d{1,3})?)(?:\s*[–-]\s*(\d{2,3}(?:[.,]\d{1,3})?))?\s*k\b")
R_GIA_NGHIN = re.compile(r"(?<![\d.,])(\d{2,3})\.(\d{3})(?![\d.])")


def tim_gia_vt(s):
    """Mức giá BTC (đơn vị nghìn, làm tròn 1 số lẻ, 20–130k) viết dạng `85,5k`, `81–82k`, `59.809`: list (vị trí, giá)."""
    s = R_LINK.sub(lambda m: "](" + " " * (len(m.group(0)) - 3) + ")", s)
    ra = []
    for m in R_GIA_K.finditer(s):
        for k in (1, 2):
            if m[k]:
                ra.append((m.start(k), round(float(m[k].replace(",", ".")), 1)))
    for m in R_GIA_NGHIN.finditer(s):
        ra.append((m.start(), round(int(m[1]) + int(m[2]) / 1000, 1)))
    return [(v, x) for v, x in ra if 20 <= x <= 130]


def tim_gia(s):
    return {x for _, x in tim_gia_vt(s)}


def lap_gia_dau(cac_van):
    gia_dau = {}
    for van in cac_van:
        for dong in van.split("\n"):
            ds = tim_ngay_vt(dong)
            if not ds:
                continue
            # hàng bảng: xét từng ô; ô không có ngày → lấy ngày lớn nhất của hàng (thận trọng)
            for phan in (tach_o(dong) if la_bang(dong) else [dong]):
                dp = tim_ngay_vt(phan)
                for vt, g in tim_gia_vt(phan):
                    d = (min(dp, key=lambda x: (abs(x[0] - vt), -x[1].toordinal()))[1] if dp
                         else max(x for _, x in ds))
                    if g not in gia_dau or d < gia_dau[g]:
                        gia_dau[g] = d
    return gia_dau


def gia_sau(s, han, gia_dau):
    """Dòng không ngày có mức giá chỉ xuất hiện (có ngày) từ han trở đi."""
    if not gia_dau or tim_ngay(s):
        return False
    return any(g in gia_dau and gia_dau[g] >= han for g in tim_gia(s))


# ======================= tách mục (chỉ dùng cho giong_noi.md) =======================
def tach_doan(s, trong_bang=False):
    """Tách s thành [(đoạn, dấu_nối_sau)] ở cấp ngoài cùng (không trong ngoặc, trích dẫn, `code`, **đậm**).
    Dấu nối: '. ' (hết câu), '; ', ' · ' (+ trong bảng: ', ' ngay trước một trích dẫn mới)."""
    ra, dau, i = [], 0, 0
    nong, nhay, code, dam = 0, False, False, False
    n = len(s)
    while i < n:
        ch = s[i]
        if ch == "`":
            code = not code
        elif code:
            pass
        elif s.startswith("**", i):
            dam = not dam
            i += 2
            continue
        elif ch in "([«“":
            nong += 1
        elif ch in ")]»”" and nong > 0:
            nong -= 1
        elif ch == '"':
            nhay = not nhay
        elif nong == 0 and not nhay and not dam:
            sep = None
            if s.startswith("; ", i):
                sep, cat, bo = "; ", i, 2
            elif s.startswith(" · ", i):
                sep, cat, bo = " · ", i, 3
            elif ch == "." and i + 1 < n and s[i + 1] == " " and i > dau:
                sep, cat, bo = " ", i + 1, 2
            elif trong_bang and s.startswith(", ", i) and i + 2 < n and s[i + 2] in '"«“':
                sep, cat, bo = ", ", i, 2
            if sep:
                ra.append((s[dau:cat], sep))
                i = dau = i + bo
                continue
        i += 1
    if dau < n:
        ra.append((s[dau:], ""))
    return [(d, p) for d, p in ra if d.strip()] or [(s, "")]


R_THUC_CHAT = re.compile(r"\[[^\]]*\]\([^)]*\)|\[[^\]]*\]|`[^`]*`|[\W\d_]+")


def co_thuc_chat(s):
    """Đoạn có chữ thật (không chỉ link / giờ / dấu)."""
    return len(R_THUC_CHAT.sub("", s)) >= 3


def noi_doan(doan):
    s = "".join(d + p for d, p in doan[:-1]) + (doan[-1][0] if doan else "")
    return s.rstrip().rstrip(";·,").rstrip()


def loc_muc(s, han, tk):
    """Bỏ từng mục (câu mẫu) có mốc ≥ han trong s. Trả chuỗi mới, hoặc None nếu không còn mục nào có chữ."""
    doan = tach_doan(s.strip(), trong_bang=True)
    giu = [x for x in doan if not qua_han(x[0], han)]
    if len(giu) == len(doan):
        return s
    tk["muc"] += len(doan) - len(giu)
    if not giu or not any(co_thuc_chat(x) for x, _ in giu):
        return None
    return noi_doan(giu)


# ======================= tiện ích dòng / bảng =======================
R_TIEN_TO = re.compile(r"^(\s*(?:>\s*)?(?:(?:[-*+]|\d+\.)\s+)?)(?:(\*\*([^*]{1,160})\*\*(?:\s*\([^()]*\))?\s*:?\s*))?")
R_CHI_NHAN = re.compile(r"^\s*(?:(?:[-*+]|\d+\.)\s+)?\*\*[^*]+\*\*\s*:?\s*$")


def tien_to(dong):
    """(tiền tố giữ nguyên: thụt lề + gạch đầu dòng + nhãn đậm kết thúc bằng ':', phần còn lại, có_nhãn)."""
    m = R_TIEN_TO.match(dong)
    a = m.group(1)
    nhan = bool(m.group(2) and not tim_ngay(m.group(3))
                and (m.group(2).rstrip().endswith(":") or m.group(3).rstrip().endswith(":")))
    if nhan:
        a += m.group(2)
    return a, dong[len(a):], nhan


def chi_nhan(dong):
    """Dòng chỉ có nhãn (vd "- **Ví dụ**:", "- **Vào / tránh / chờ**") — nội dung nằm ở các dòng con."""
    if R_CHI_NHAN.match(dong):
        return True
    a, b, nhan = tien_to(dong)
    return nhan and not b.strip()


def thut(dong):
    return len(dong) - len(dong.lstrip(" "))


def la_bang(dong):
    return dong.lstrip().startswith("|")


def la_khung(dong):
    """Dòng cấu trúc không bao giờ bỏ: tiêu đề, thẻ HTML (<details>…), kẻ ngang."""
    return dong.lstrip().startswith(("#", "<", "---"))


def tach_o(dong):
    """Tách hàng bảng thành ô (bỏ `|` ở 2 đầu), không cắt trong `code`."""
    s = dong.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    o, cur, code = [], "", False
    for i, ch in enumerate(s):
        if ch == "`":
            code = not code
        if ch == "|" and not code and (i == 0 or s[i - 1] != "\\"):
            o.append(cur)
            cur = ""
        else:
            cur += ch
    o.append(cur)
    return o


GHI_CHU_BANG = "_(bảng đã lọc hết hàng: mọi hàng có ngày ≥ ngày của T)_"


def loc_bang(khoi, han, tk, theo_muc=False, gia_dau=None):
    """Lọc một khối bảng. Hàng có mốc ≥ han (hoặc ô tháng ≥ tháng của T) → bỏ cả hàng; theo_muc → bỏ từng câu mẫu.
    Hàng tiêu đề + hàng kẻ luôn giữ; bảng bị lọc hết → thêm 1 dòng ghi chú sau bảng."""
    if len(khoi) < 2 or not re.match(r"^\s*\|[\s:|-]+\|?\s*$", khoi[1]):
        ra = [d for d in khoi if not (qua_han(d, han) or gia_sau(d, han, gia_dau))]
        tk["bo"] += len(khoi) - len(ra)
        return ra
    dau, ke = khoi[0], khoi[1]
    o_dau = [x.strip() for x in tach_o(dau)]
    i_doi = next((k for k, x in enumerate(o_dau) if "Ngày tới" in x), None)
    ra = []
    for d in khoi[2:]:
        o = tach_o(d)
        thang = [_cuoi_thang(NAM, int(m[1])) for m in (R_THANG_O.match(c.strip()) for c in o) if m]
        bo_hang = any(x and x >= han for x in thang) or gia_sau(d, han, gia_dau)
        moi = list(o)
        if not bo_hang and theo_muc:
            for k, c in enumerate(o):
                if not tim_ngay(c):
                    continue
                x = loc_muc(c, han, tk)
                if x is None:
                    bo_hang = True
                    break
                if x != c:
                    moi[k] = " " + x + " "
        elif not bo_hang:
            bo_hang = qua_han(d, han)
        if bo_hang:
            tk["bo"] += 1
            continue
        if i_doi is not None and i_doi < len(o):
            m = re.match(r"^\s*(\d+)\s*$", o[i_doi])
            tat_ca = [x for k, c in enumerate(o) if k != i_doi for x in tim_ngay(c)]
            if m and tat_ca and min(tat_ca) + dt.timedelta(days=int(m[1])) >= han:
                moi[i_doi] = " — "
        if moi != o:
            tk["sua"] += 1
            ra.append("|" + "|".join(moi) + "|")
        else:
            ra.append(d)
    if not ra:
        return [dau, ke, "", GHI_CHU_BANG]
    return [dau, ke] + ra


def _dem_con(ra, dong_goc):
    """Với mỗi dòng trong ra: (số dòng con còn giữ, số dòng con ở bản gốc). Con = dòng liền sau, thụt sâu hơn, không trống."""
    kq = {}
    for k, (x, i0) in enumerate(ra):
        t = thut(x)
        goc = 0
        j = i0 + 1
        while j < len(dong_goc) and dong_goc[j].strip() and thut(dong_goc[j]) > t and not la_bang(dong_goc[j]):
            goc += 1
            j += 1
        giu = 0
        q = k + 1
        while q < len(ra) and ra[q][0].strip() and thut(ra[q][0]) > t and not la_bang(ra[q][0]):
            giu += 1
            q += 1
        kq[k] = (giu, goc)
    return kq


# ======================= lọc cả file =======================
def loc_van_ban(van_ban, han, theo_muc=False, gia_dau=None):
    """Lọc cả file Markdown theo han (date). Trả (văn bản mới, thống kê {bo, sua, muc, tong}).
    theo_muc=False (sổ tay): bỏ CẢ DÒNG có mốc ≥ han. theo_muc=True (giọng nói): bỏ từng câu mẫu.
    gia_dau (từ lap_gia_dau): dòng không ngày mà có mức giá chỉ xuất hiện từ han trở đi cũng bỏ; None = không xét."""
    dong = van_ban.split("\n")
    tk = {"bo": 0, "sua": 0, "muc": 0, "tong": len(dong)}
    ra = []                # list (dòng, chỉ số dòng gốc)
    i = 0
    con_bo_thut = None     # thụt lề của dòng vừa bị bỏ → bỏ luôn các dòng con liền sau (thụt sâu hơn)
    bo_bang_sau = False    # dòng vừa bỏ kết thúc bằng ':' → bỏ luôn bảng ngay sau nó
    while i < len(dong):
        d = dong[i]
        if la_bang(d):
            j = i
            while j < len(dong) and la_bang(dong[j]):
                j += 1
            khoi = dong[i:j]
            if bo_bang_sau:
                tk["bo"] += len(khoi)
            else:
                ra += [(x, i) for x in loc_bang(khoi, han, tk, theo_muc, gia_dau)]
            bo_bang_sau, con_bo_thut = False, None
            i = j
            continue
        if not d.strip():
            ra.append((d, i))
            con_bo_thut = None
            i += 1
            continue
        t = thut(d)
        bo_bang_sau = False
        if con_bo_thut is not None and t > con_bo_thut and not la_khung(d):
            tk["bo"] += 1
            i += 1
            continue
        con_bo_thut = None
        moi = d
        if not la_khung(d) and gia_sau(d, han, gia_dau):
            moi = None
        elif not la_khung(d) and qua_han(d, han):
            if theo_muc:
                a, b, _nhan = tien_to(d)
                x = loc_muc(b, han, tk)
                moi = None if x is None else a + x
            else:
                moi = None
        if moi is None:
            tk["bo"] += 1
            con_bo_thut = t
            bo_bang_sau = d.rstrip().rstrip("*").rstrip().endswith(":")
        else:
            if moi != d:
                tk["sua"] += 1
            ra.append((moi, i))
        i += 1
    # bỏ dòng chỉ có nhãn mà mọi dòng con đều đã bị bỏ (vd "- **Ví dụ**:" trơ trọi)
    dem = _dem_con(ra, dong)
    bo_chi_so = set()
    for k, (x, _) in enumerate(ra):
        if x.strip() and not x.lstrip().startswith(("#", "<", "|", "---", ">")) and chi_nhan(x):
            con_giu, con_goc = dem[k]
            if con_goc > 0 and con_giu == 0:
                bo_chi_so.add(k)
                tk["bo"] += 1
    ra = [x for k, x in enumerate(ra) if k not in bo_chi_so]
    van = "\n".join(x for x, _ in ra)
    van = re.sub(r"\n{3,}", "\n\n", van)
    return van, tk


# ======================= chạy =======================
def doc_t(s):
    s = s.strip().replace("T", " ")
    if len(s) == 10:
        s += " 07:00"
    return dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M").replace(tzinfo=VN)


def phan_c():
    dong = TINH_HOA.read_text(encoding="utf-8").split("\n")
    a = next(i for i, x in enumerate(dong) if x.startswith("# PHẦN C"))
    b = next(i for i, x in enumerate(dong) if x.startswith("# PHẦN D"))
    return "\n".join(dong[a:b]).rstrip("\n -") + "\n"


def dong_dau(T, han, tk):
    s = (f"> Lọc theo T = {T.strftime('%Y-%m-%d %H:%M')} (giờ VN); bỏ {tk['bo']} dòng có ngày ≥ T"
         f" (mọi mốc ≥ {han.isoformat()}; dòng kết quả \"Đo:\" tính thêm {BIEN_DO} ngày; dòng không ngày mà có mức giá"
         f" chỉ xuất hiện từ T trở đi cũng bỏ)")
    if tk["muc"]:
        s += f", cắt {tk['muc']} câu mẫu có ngày ≥ T"
    return s + ". Ví dụ còn lại đều trước T — không mở bản gốc."


def tao(t_str, ra=None, in_ra=True):
    T = doc_t(t_str)
    han = T.date()
    # mặc định: thư mục RIÊNG theo T (bot_v5/_so_tay_T/<YYYYMMDD_HHMM>/) — nhiều phiên chạy song song không ghi đè nhau
    thu_muc = Path(ra) if ra else RA_MAC_DINH / T.strftime("%Y%m%d_%H%M")
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.glob("*.md"):
        p.unlink()
    nguon = [(p.name, p.read_text(encoding="utf-8"), False) for p in NGUON] + [("giong_noi.md", phan_c(), True)]
    gia_dau = lap_gia_dau([van for _, van, _ in nguon])
    thong_ke = {}
    for ten, van, theo_muc in nguon:
        moi, tk = loc_van_ban(van, han, theo_muc, gia_dau)
        moi = dong_dau(T, han, tk) + "\n\n" + moi
        (thu_muc / ten).write_text(moi, encoding="utf-8")
        tk["con"] = len(moi.split("\n")) - 2
        thong_ke[ten] = tk
        if in_ra:
            them = f", cắt {tk['muc']} câu mẫu" if tk["muc"] else ""
            print(f"{ten}: bỏ {tk['bo']} dòng có ngày ≥ T{them} (gốc {tk['tong']} dòng → còn {tk['con']})")
    if in_ra:
        print(f"→ đã ghi {thu_muc} (T = {T.strftime('%Y-%m-%d %H:%M')} VN; bỏ mọi mốc ≥ {han.isoformat()})")
    return thong_ke


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sổ tay lọc theo T (bỏ dòng / hàng bảng / ví dụ có ngày ≥ T)")
    ap.add_argument("t", help='"YYYY-MM-DD HH:MM" giờ VN')
    ap.add_argument("--ra", default=None, help="thư mục ghi (mặc định bot_v5/_so_tay_T)")
    a = ap.parse_args(argv)
    try:
        tao(a.t, a.ra)
    except ValueError as e:
        print(f"LỖI: T không đúng dạng \"YYYY-MM-DD HH:MM\": {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
