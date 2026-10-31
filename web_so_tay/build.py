#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng trang web tĩnh đọc "Sổ tay tinh hoa" — chạy LOCAL, mở index.html bằng trình duyệt (file://), không cần mạng.

    cd trade_dai_han && python3 web_so_tay/build.py

Đọc:  so_tay/SO_TAY_TINH_HOA.md, so_tay/SO_LIEU_CAN_CU.md, moc/*.json, du_lieu/btc_4H.csv, du_lieu/btc_1Dutc.csv,
      so_tay/khung/*.jpg, so_tay/ghi_chu/hinh_anh_*.md (nếu có), doi_chieu/SO_DOI_CHIEU.md (nếu có),
      transcripts/danh_sach.tsv (giờ bắt đầu + tiêu đề buổi live, nếu có).
Ghi:  web_so_tay/index.html, web_so_tay/thumbs/*.jpg (ảnh thu nhỏ, tạo bằng `sips` của macOS nếu có).
Thư viện (tải sẵn 1 lần, nằm trong web_so_tay/vendor/): markdown (Python), lightweight-charts 4.2.3, Chart.js 4.4.7.
Mọi số liệu / đồ thị đều tính lại từ file mỗi lần chạy.
"""
from __future__ import annotations

import csv
import datetime as dt
import html
import json
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOC = HERE.parent
VENDOR = HERE / "vendor"
sys.path.insert(0, str(VENDOR / "py"))
try:
    import markdown
    from markdown.extensions.toc import slugify_unicode
except ImportError:  # pragma: no cover
    sys.exit("Thiếu thư viện markdown. Cài 1 lần:  python3 -m pip install --target web_so_tay/vendor/py markdown==3.7")

NAM = 2026
H4 = 4 * 3600
VN_S = 7 * 3600
CANH_BAO: list[str] = []

P_SO_TAY = GOC / "so_tay" / "SO_TAY_TINH_HOA.md"
P_SO_LIEU = GOC / "so_tay" / "SO_LIEU_CAN_CU.md"
P_DOI_CHIEU = GOC / "doi_chieu" / "SO_DOI_CHIEU.md"
P_MOC = GOC / "moc"
P_4H = GOC / "du_lieu" / "btc_4H.csv"
P_1D = GOC / "du_lieu" / "btc_1Dutc.csv"
P_KHUNG = GOC / "so_tay" / "khung"
P_GHI_CHU = GOC / "so_tay" / "ghi_chu"
P_DS = GOC / "transcripts" / "danh_sach.tsv"
P_THUMB = HERE / "thumbs"


# =====================================================================================
# Tiện ích chung
# =====================================================================================
def esc(s) -> str:
    return html.escape(str(s), quote=True)


def doc(p: Path) -> str | None:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def fmt_gia(x: float | None) -> str:
    if x is None:
        return ""
    return f"{x:,.0f}".replace(",", ".")


def fmt_pt(x: float, so=0) -> str:
    return f"{x:.{so}f}".replace(".", ",") + "%"


def tron(s: str) -> str:
    """Bỏ ký hiệu markdown → chữ thường."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def cat(s: str, n: int) -> str:
    s = s.strip()
    return s if len(s) <= n else s[: n - 1].rstrip(" ,;:") + "…"


RE_NGAY = re.compile(r"\[(\d{2})-(\d{2})\]")


def _span_ngay(m: re.Match) -> str:
    mm, dd = m.group(1), m.group(2)
    return f'<span class="ngay" data-ngay="{NAM}-{mm}-{dd}" title="Ngày {dd}/{mm}/{NAM}">{mm}-{dd}</span>'


def thay_ngay(text: str) -> str:
    """[MM-DD] → nhãn ngày (bỏ qua phần nằm trong `code`)."""
    parts = re.split(r"(`[^`\n]*`)", text)
    return "".join(p if p.startswith("`") else RE_NGAY.sub(_span_ngay, p) for p in parts)


RE_LIST = re.compile(r"^\s*([-*+]|\d+\.)\s")


def tien_xu_ly(md: str) -> str:
    """Chuẩn hoá markdown cho python-markdown: thụt lề danh sách con, dòng trống trước danh sách/bảng, tách trích dẫn."""
    out: list[str] = []
    prev = ""
    for ln in md.split("\n"):
        s = ln.rstrip()
        m = re.match(r"^( {1,3})([-*+]|\d+\.)\s", s)
        if m:
            s = "    " + s[len(m.group(1)):]
        la_list, la_bang, la_tdan = bool(RE_LIST.match(s)), s.lstrip().startswith("|"), s.startswith(">")
        p_list, p_bang, p_tdan = bool(RE_LIST.match(prev)), prev.lstrip().startswith("|"), prev.startswith(">")
        if prev.strip():
            if la_list and not p_list and not prev.startswith((" ", "\t")) and not p_tdan:
                out.append("")
            elif la_bang and not p_bang:
                out.append("")
            elif p_bang and s.strip() and not la_bang:
                out.append("")
            elif la_tdan and p_tdan:
                out.append(">")
            elif s.startswith("→") and not p_list:
                out.append("")
        out.append(s)
        prev = s
    return thay_ngay("\n".join(out))


_MD = markdown.Markdown(
    extensions=["tables", "toc", "sane_lists"],
    extension_configs={"toc": {"slugify": slugify_unicode, "toc_depth": "1-3"}},
)


def md_khoi(text: str) -> str:
    _MD.reset()
    return _MD.convert(tien_xu_ly(text))


def md_dong(text: str) -> str:
    h = md_khoi(text).strip()
    if h.startswith("<p>") and h.endswith("</p>") and h.count("<p>") == 1:
        h = h[3:-4]
    return h


def tach_o(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def bang_sau(lines: list[str], pat: str):
    """Bảng đầu tiên sau dòng khớp `pat` (dừng nếu gặp tiêu đề khác trước). Trả (tiêu đề, các hàng)."""
    rx = re.compile(pat)
    i = next((k for k, l in enumerate(lines) if rx.search(l)), None)
    if i is None:
        return None, []
    j = i + 1
    while j < len(lines) and not lines[j].lstrip().startswith("|"):
        if lines[j].startswith("#"):
            return None, []
        j += 1
    rows = []
    while j < len(lines) and lines[j].lstrip().startswith("|"):
        rows.append(tach_o(lines[j]))
        j += 1
    if len(rows) < 2:
        return None, []
    body = [r for r in rows[1:] if not re.fullmatch(r"[\s:|-]*", "|".join(r))]
    return rows[0], body


def trich_cac(s: str) -> list[tuple[str, str]]:
    """Các câu trích "…" kèm ngày [MM-DD] (nếu có) trong 1 ô."""
    return [(m.group(1), m.group(2) or "") for m in re.finditer(r'"([^"]+)"\s*(\[\d{2}-\d{2}\])?', s)]


# =====================================================================================
# Đọc dữ liệu
# =====================================================================================
def doc_nen(p: Path):
    rows = []
    if not p.exists():
        CANH_BAO.append(f"thiếu {p.relative_to(GOC)}")
        return rows
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                t = dt.datetime.strptime(r["ts_utc"][:16], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
                rows.append((int(t.timestamp()), float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])))
            except (ValueError, KeyError):
                continue
    rows.sort()
    return rows


def ema(vals: list[float], n: int) -> list[float | None]:
    """EMA chuẩn, khởi đầu bằng SMA của n giá trị đầu (trước đó = None)."""
    out: list[float | None] = [None] * len(vals)
    if len(vals) < n:
        return out
    k = 2 / (n + 1)
    e = sum(vals[:n]) / n
    out[n - 1] = e
    for i in range(n, len(vals)):
        e = vals[i] * k + e * (1 - k)
        out[i] = e
    return out


def doc_danh_sach() -> dict:
    ds = {}
    t = doc(P_DS)
    if not t:
        return ds
    for ln in t.splitlines()[1:]:
        c = ln.split("\t")
        if len(c) >= 7:
            ds[c[0]] = {"ngay": c[1], "gio": c[2], "phut": c[5], "tieu_de": c[6]}
    return ds


def doc_moc(ds: dict):
    buoi = []
    for p in sorted(P_MOC.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            CANH_BAO.append(f"bỏ qua {p.name}: {e}")
            continue
        stem = p.stem
        ngay = d.get("ngay") or stem[:10]
        rest = stem[11:]
        gio = None
        if len(rest) > 5 and rest[4] == "_" and rest[:4].isdigit():
            gio, vid = rest[:4], rest[5:]
        else:
            vid = rest
        info = ds.get(vid, {})
        gio = gio or info.get("gio") or "1000"
        buoi.append({
            "id": stem, "vid": vid, "ngay": ngay, "gio": gio,
            "tieu_de": info.get("tieu_de", ""), "gia_noi": d.get("gia_btc_luc_noi"),
            "moc": d.get("moc", []) or [],
        })
    buoi.sort(key=lambda b: (b["ngay"], b["gio"]))
    return buoi


def loai_can_cu(s: str) -> str:
    """Phân loại 1 câu căn cứ (cùng thứ tự ưu tiên với cong_cu/kiem_can_cu.py, thêm 'mô hình')."""
    s = s.lower()
    if "fibo" in s:
        return "fibo"
    if re.search(r"\bma ?\d|ema|đường ma|cụm ma|\bma\b", s):
        return "ma"
    if re.search(r"đỉnh|đáy|râu|cũ", s):
        return "dinhday"
    if "tròn" in s or "tâm lý" in s:
        return "tron"
    if "trendline" in s or "trend" in s:
        return "trend"
    if "thanh lý" in s or "heatmap" in s or "liquid" in s:
        return "thanhly"
    if "gap" in s:
        return "gap"
    if re.search(r"mô hình|cờ|vai đầu vai|tam giác|nêm|cốc", s):
        return "mohinh"
    return "khac"


TEN_CC = {"fibo": "Fibo", "ma": "MA/EMA", "dinhday": "Đỉnh/đáy cũ", "thanhly": "Thanh lý / heatmap",
          "gap": "Gap CME", "trend": "Trendline", "tron": "Số tròn", "mohinh": "Mô hình", "khac": "Khác"}


# =====================================================================================
# HÌNH 1 — Một buổi live (dòng thời gian từ bảng A2)
# =====================================================================================
def do_tan_suat(s: str):
    t = tron(s)
    m = re.search(r"(\d+)(?:\s*[–-]\s*(\d+))?/20", t)
    if m:
        lo = int(m.group(1))
        hi = int(m.group(2) or lo)
        return ("ty_le", lo / 20, hi / 20)
    if re.search(r"(?i)mọi buổi", t):
        v = 0.95 if "gần như" in t.lower() else 1.0
        return ("ty_le", v, v)
    nhom: set[int] = set()
    for a, b in re.findall(r"N(\d)(?:\s*[–-]\s*N?(\d))?", t):
        nhom.update(range(int(a), int(b or a) + 1))
    if nhom:
        return ("nhom", sorted(nhom))
    return None


def hinh_quy_trinh(lines):
    _, rows = bang_sau(lines, r"^## A2\.")
    if not rows:
        return None
    li = []
    for r in rows:
        so, buoc, _ct, ts = (r + ["", "", "", ""])[:4]
        tag = ""
        m = re.match(r"^\*\((.+?)\)\*\s*(.*)$", buoc)
        if m:
            tag, buoc = m.group(1), m.group(2)
        mb = re.match(r"^\*\*(.+?)\*\*\s*:?\s*(.*)$", buoc)
        tieu, phu = (mb.group(1), mb.group(2)) if mb else (buoc, "")
        do = do_tan_suat(ts)
        if do and do[0] == "ty_le":
            _, lo, hi = do
            meter = (f'<span class="thuoc" title="ước lượng từ nhãn tần suất"><i style="width:{lo*100:.0f}%"></i>'
                     f'<b style="left:{lo*100:.0f}%;width:{(hi-lo)*100:.0f}%"></b></span>')
        elif do:
            meter = '<span class="thuoc-nhom" title="nhóm giai đoạn có bước này">' + "".join(
                f'<i class="{"co" if k in do[1] else ""}">N{k}</i>' for k in range(1, 10)) + "</span>"
        else:
            meter = ""
        cls = "buoc truoc" if tag else "buoc"
        li.append(
            f'<li class="{cls}"><div class="buoc-so">{esc(so)}</div><div class="buoc-nd">'
            f'<div class="buoc-tieu">{md_dong(tieu)}{f" <span class=nhan-phu>{esc(tag)}</span>" if tag else ""}</div>'
            + (f'<div class="buoc-phu">{md_dong(phu)}</div>' if phu else "")
            + f'<div class="tan-suat">{meter}<span>{md_dong(ts)}</span></div></div></li>'
        )
    return {
        "tieu_de": "Một buổi live",
        "mo_ta": "Các bước theo đúng thứ tự trong buổi live sáng (~10h). Thanh màu = tần suất lấy từ cột “Tần suất” "
                 "(n/20 buổi mỗi nhóm), ô N1…N9 = nhóm giai đoạn có bước đó.",
        "than": f'<ol class="dong-tg">{"".join(li)}</ol>',
        "nguon": "Tính từ bảng A2 trong SO_TAY_TINH_HOA.md.",
    }


# =====================================================================================
# HÌNH 2 — Bản đồ công cụ (bảng A1)
# =====================================================================================
def tach_phay(s: str) -> list[str]:
    """Tách theo dấu phẩy ở mức ngoài cùng (không cắt trong ngoặc / ngoặc kép)."""
    out, buf, sau, nk = [], "", 0, False
    for ch in s:
        if ch == '"':
            nk = not nk
        elif ch == "(" and not nk:
            sau += 1
        elif ch == ")" and not nk:
            sau = max(0, sau - 1)
        if ch == "," and sau == 0 and not nk:
            out.append(buf.strip())
            buf = ""
        else:
            buf += ch
    if buf.strip():
        out.append(buf.strip())
    return out


def hinh_cong_cu(lines):
    _, rows = bang_sau(lines, r"^## A1\.")
    if not rows:
        return None
    cot = {"qd": [], "bl": [], "tk": [], "kd": []}
    nen_tang = []
    kd_trich = ""
    for r in rows:
        r = (r + [""] * 5)[:5]
        c0, c1, _c2, c3, c4 = r
        mb = re.match(r"^\*\*(.+?)\*\*", c0)
        ten = tron(mb.group(1)) if mb else tron(c0)
        if "không dùng" in ten.lower():
            for it in tach_phay(tron(c1)):
                m = re.match(r"^(.*?)\s*\((.*)\)\s*$", it)
                ten_i, ghi = (m.group(1), m.group(2)) if m else (it, "")
                cot["kd"].append({"ten": ten_i, "ghi": ghi})
            q = trich_cac(c4)
            kd_trich = q[0][0] if q else ""
            continue
        t3 = re.sub(r'"[^"]*"', "", tron(c3)).lower()   # bỏ câu trích để không bắt nhầm chữ "quyết định" trong lời nói
        if "quyết định" in t3:
            k = "qd"
        elif "bộ lọc" in t3:
            k = "bl"
        elif "tham khảo" in t3:
            k = "tk"
        else:
            nen_tang.append(cat(ten, 40))
            continue
        bo = ""
        mbo = re.search(r"[Tt]ừ tháng (\d+)[^.]*\bbỏ\b", tron(c3))
        if mbo:
            bo = f"bỏ từ T{mbo.group(1)}"
        cot[k].append({"ten": cat(ten, 54), "dung": cat(tron(c1), 90), "muc": cat(tron(c3), 96), "bo": bo})
    ten_cot = {"qd": ("Quyết định", "chọn hướng, vùng, đích"), "bl": ("Bộ lọc", "chỉ được HOÃN lệnh, không đổi hướng"),
               "tk": ("Tham khảo", "bối cảnh, ít khi dùng"), "kd": ("Không dùng", "tự nói không tin / không đưa vào hệ thống")}
    html_cot = []
    for k in ("qd", "bl", "tk", "kd"):
        t, phu = ten_cot[k]
        the = []
        for it in cot[k]:
            if k == "kd":
                the.append(f'<div class="the the-kd" title="{esc(it["ghi"])}"><b>{esc(it["ten"])}</b>'
                           + (f'<small>{esc(cat(it["ghi"], 60))}</small>' if it["ghi"] else "") + "</div>")
            else:
                the.append(f'<div class="the"><b>{esc(it["ten"])}</b>'
                           + (f' <span class="the-bo">{esc(it["bo"])}</span>' if it["bo"] else "")
                           + f'<span class="the-dung">{esc(it["dung"])}</span>'
                           f'<span class="the-muc">{esc(it["muc"])}</span></div>')
        html_cot.append(f'<div class="cot-cc cot-{k}"><div class="cot-dau"><b>{t}</b> <span class="dem">{len(cot[k])}</span>'
                        f'<small>{phu}</small></div>{"".join(the)}'
                        + (f'<p class="cot-trich">“{esc(kd_trich)}”</p>' if k == "kd" and kd_trich else "") + "</div>")
    chan = f'<p class="hinh-nguon">Nền tảng &amp; thực thi (không xếp loại): {esc(" · ".join(nen_tang))}.</p>' if nen_tang else ""
    return {
        "tieu_de": "Bản đồ công cụ",
        "mo_ta": "Mỗi công cụ trong bảng A1 xếp vào một cột theo cột “Mức tin”. Bộ lọc chỉ có quyền hoãn lệnh — "
                 "“Không short có nghĩa không phải là chúng ta đi long”.",
        "than": f'<div class="ban-do-cc">{"".join(html_cot)}</div>{chan}',
        "nguon": "Tính từ bảng A1 (cột “Công cụ”, “Dùng để làm gì”, “Mức tin”).",
    }


# =====================================================================================
# HÌNH 3 — Cây chọn hướng (A3 + B2 + B6)
# =====================================================================================
def mini_ema(kieu: str) -> str:
    """Hình nhỏ: giá (nến) so với 3 đường EMA34 / 89 / 200."""
    duong = {"ema34": 30, "ema89": 40, "ema200": 50}
    if kieu == "giua":
        duong = {"ema34": 18, "ema89": 46, "ema200": 54}
    elif kieu == "duoi":
        duong = {"ema34": 34, "ema89": 24, "ema200": 14}
    p = []
    for k, y in duong.items():
        p.append(f'<path d="M4 {y+4} C40 {y+1}, 80 {y-1}, 116 {y-3}" class="mn-{k}"/>')
    nen = {"tren": (12, 6), "giua": (28, 8), "duoi": (44, 8)}[kieu]
    y0, h = nen
    for i, x in enumerate((70, 84, 98)):
        yy = y0 + (i % 2) * 2
        p.append(f'<line x1="{x}" y1="{yy-3}" x2="{x}" y2="{yy+h+3}" class="mn-rau"/>'
                 f'<rect x="{x-3}" y="{yy}" width="6" height="{h}" rx="1" class="mn-nen"/>')
    return f'<svg viewBox="0 0 120 64" class="mini-ema" aria-hidden="true">{"".join(p)}</svg>'


def doc_luat(lines) -> dict:
    luat = {}
    for ln in lines:
        if ln.startswith("| L"):
            c = tach_o(ln)
            if re.fullmatch(r"L\d{2}", c[0]):
                luat[c[0]] = c[1:]
    return luat


def ngan_dk(s: str, n=60, cau_dau=False) -> str:
    t = tron(s).split("→")[0]
    if cau_dau:
        t = re.split(r"\.\s|;", t)[0]
    t = re.sub(r"\s*\([^)]*\)", "", t).strip()
    return cat(t, n)


def hinh_cay(lines, luat):
    _, rows = bang_sau(lines, r"^### Bộ luật nếu–thì")
    tim = {}
    for r in rows:
        r = (r + [""] * 4)[:4]
        thi = tron(r[2])
        for khoa, mau in (("tang", "Không short"), ("giam", "Được phép tìm short"), ("cho", "Ngồi chờ"), ("ct", "Đổi phe")):
            if thi.startswith(mau) and khoa not in tim:
                tim[khoa] = r

    def q(khoa, uu_tien=""):
        r = tim.get(khoa)
        if not r:
            return ""
        qs = trich_cac(r[3])
        if uu_tien:
            qs = [x for x in qs if uu_tien in x[0]] or qs
        if not qs:
            return ""
        t, d = qs[0]
        return f'<q>{esc(cat(t, 140))}</q>{(" " + thay_ngay(d)) if d else ""}'

    def dk(khoa, mac_dinh):
        r = tim.get(khoa)
        return esc(re.sub(r"\s*\((H4)\)", r" (\1)", tron(r[1]))) if r else mac_dinh

    ct_a, ct_b = "1 cây H4 đóng qua = “điều kiện cần” (~50%)", "Cây thứ 2 cùng phía = “điều kiện đủ”"
    if "ct" in tim:
        t = tron(tim["ct"][2])
        t = re.sub(r"^Đổi phe\.\s*", "", t).rstrip(".")
        ps = [x.strip() for x in t.split(";") if x.strip()]
        if len(ps) >= 2:
            ct_a, ct_b = ps[0], ps[1]
    pv = [(k, ngan_dk(luat[k][0], 90)) for k in sorted(luat) if "L34" <= k <= "L40"]
    loc = [(k, ngan_dk(luat[k][0], 58, True)) for k in sorted(luat) if "L09" <= k <= "L17"]
    pv_html = "".join(f"<li><code>{k}</code> {esc(t)}</li>" for k, t in pv) or "<li>(chưa đọc được bảng B6)</li>"
    loc_html = "".join(f'<span class="chip-loc"><code>{k}</code> {esc(t)}</span>' for k, t in loc)
    than = f"""
<div class="cay">
  <div class="cay-hang"><div class="nut-cay nut-dau">Nến H4 vừa <b>đóng</b> <small>03 · 07 · 11 · 15 · 19 · 23h giờ VN</small></div></div>
  <div class="mui"></div>
  <div class="cay-hang cay-pv">
    <div class="nut-cay nut-hoi">Trúng một cửa <b>PHÂN VÂN</b>? <small>B6 · L34–L40</small></div>
    <div class="nhanh-co"><span>có</span></div>
    <div class="nut-cay nut-pv"><b>PHÂN VÂN — lấp lửng ở mốc quyết định, chờ nến xác nhận (đứng ngoài chờ entry KHÔNG phải PHÂN VÂN)</b><ul>{pv_html}</ul></div>
  </div>
  <div class="mui"><span>không</span></div>
  <div class="cay-hang"><div class="nut-cay nut-hoi">Thứ tự <b>giá</b> so với <b class="t34">EMA34</b> · <b class="t89">EMA89</b> · <b class="t200">EMA200</b> trên H4 (đối chiếu D1) <small>L01 · L08</small></div></div>
  <div class="re-ba"><i></i><i></i><i></i></div>
  <div class="cay-ba">
    <div class="nhanh nhanh-tang">{mini_ema("tren")}<div class="dk">{dk("tang", "Giá đóng trên EMA34 và EMA89 (H4)")}</div>
      <div class="ket ket-tang">CẤM SHORT</div><div class="ket-phu">trên cả 3 đường → được tìm long</div><div class="trich">{q("tang")}</div></div>
    <div class="nhanh nhanh-cho">{mini_ema("giua")}<div class="dk">{dk("cho", "Giá kẹp giữa các MA")}</div>
      <div class="ket ket-cho">CHỜ</div><div class="ket-phu">hoặc các EMA chụm lại (L35)</div><div class="trich">{q("cho")}</div></div>
    <div class="nhanh nhanh-giam">{mini_ema("duoi")}<div class="dk">{dk("giam", "Giá đóng dưới cả EMA34, 89 và 200 (H4)")}</div>
      <div class="ket ket-giam">ĐƯỢC TÌM SHORT</div><div class="ket-phu">D1 cùng chiều thì “tuyệt đối” không đánh ngược</div><div class="trich">{q("giam")}</div></div>
  </div>
  <div class="mui"></div>
  <div class="cay-hang"><div class="nut-cay nut-hoi">Công tắc đổi phe: nến H4 <b>đóng</b> qua mốc đã báo trước — râu không tính <small>L07</small></div></div>
  <div class="cay-hang cay-ct">
    <div class="nut-cay nut-nho">{esc(ct_a)}<small>giữ hướng cũ, chỉ ghi cảnh báo</small></div>
    <div class="mui-ngang"></div>
    <div class="nut-cay nut-nho nut-dam">{esc(ct_b)}<small>→ đổi phe</small></div>
  </div>
  <div class="trich trich-giua">{q("ct", "hai cây")}</div>
  <div class="mui"></div>
  <div class="cay-hang"><div class="nut-cay nut-loc"><b>Bộ lọc HOÃN</b> — chỉ dời entry về vùng hồi, <b>không đảo hướng</b> <small>B2 · L09–L17</small><div class="ds-loc">{loc_html}</div></div></div>
</div>"""
    return {
        "tieu_de": "Cây chọn hướng",
        "mo_ta": "Trình tự B0: kiểm cửa PHÂN VÂN trước, rồi đọc thứ tự giá / EMA, rồi mới tới công tắc nến đóng và bộ lọc.",
        "than": than,
        "nguon": "Điều kiện và câu trích lấy từ bảng “Bộ luật nếu–thì” (A3), danh sách cửa PHÂN VÂN từ B6, bộ lọc từ B2.",
    }


# =====================================================================================
# HÌNH 4 — Căn cứ theo tháng (moc/*.json)
# =====================================================================================
def tinh_thang(buoi, so_tay_text):
    n = Counter()
    dem = defaultdict(Counter)
    co_cc = Counter()
    for b in buoi:
        th = b["ngay"][5:7]
        for m in b["moc"]:
            if not isinstance(m.get("gia"), (int, float)):
                continue
            n[th] += 1
            cc = [s for s in (m.get("can_cu") or []) if isinstance(s, str) and s.strip()]
            if cc:
                co_cc[th] += 1
            for k in {loai_can_cu(s) for s in cc}:
                dem[th][k] += 1
    thang = sorted(n)
    loai = ["fibo", "ma", "dinhday", "thanhly", "gap", "trend"]
    pt = {k: [round(dem[t][k] / n[t] * 100, 1) if n[t] else 0 for t in thang] for k in loai}
    cnt = {k: [dem[t][k] for t in thang] for k in loai}
    cme = None
    m = re.search(r"CME giao dịch 24/7 từ (\d{2})/(\d{2})", so_tay_text or "")
    if m:
        cme = {"ngay": f"{m.group(1)}/{m.group(2)}", "thang": m.group(2), "ngay_so": int(m.group(1))}
    gap = pt["gap"]
    gap_note = None
    if gap:
        i_dinh = max(range(len(gap)), key=lambda i: gap[i])
        for i in range(i_dinh + 1, len(gap)):
            if gap[i] < 2 and all(v < 5 for v in gap[i:]):
                gap_note = {"dinh": i_dinh, "tu": i, "min": min(gap[i:]), "max": max(gap[i:])}
                break
    return {
        "thang": thang, "nhan": [f"T{int(t)}" for t in thang], "n": [n[t] for t in thang],
        "co_cc": [co_cc[t] for t in thang], "loai": [{"key": k, "ten": TEN_CC[k]} for k in loai],
        "pt": pt, "cnt": cnt, "cme": cme, "gap_note": gap_note,
        "tong": sum(n.values()), "tong_co_cc": sum(co_cc.values()),
    }


def hinh_thang(T):
    if not T["thang"]:
        return None
    gn = T["gap_note"]
    them = ""
    if gn:
        them = (f" Gap CME đạt đỉnh {fmt_pt(T['pt']['gap'][gn['dinh']], 1)} ở {T['nhan'][gn['dinh']]}, "
                f"từ {T['nhan'][gn['tu']]} trở đi chỉ còn {fmt_pt(gn['min'], 1)}–{fmt_pt(gn['max'], 1)}.")
    bang = "<tr><th>Tháng</th><th>Số mốc</th>" + "".join(f"<th>{esc(l['ten'])}</th>" for l in T["loai"]) + "</tr>"
    for i, t in enumerate(T["nhan"]):
        bang += f"<tr><td>{t}</td><td>{T['n'][i]}</td>" + "".join(
            f"<td>{fmt_pt(T['pt'][l['key']][i])}</td>" for l in T["loai"]) + "</tr>"
    return {
        "tieu_de": "Căn cứ theo tháng",
        "mo_ta": f"% mốc giá trong tháng có nhắc tới từng loại căn cứ (1 mốc có thể có nhiều loại). "
                 f"Tổng {fmt_gia(T['tong'])} mốc, {fmt_pt(T['tong_co_cc'] / T['tong'] * 100)} có ít nhất 1 căn cứ.{them}",
        "than": '<div class="cj-khung cao-360"><canvas id="cj-thang" role="img" aria-label="Biểu đồ đường % mốc theo loại căn cứ từng tháng"></canvas></div>'
                f'<details class="xem-bang"><summary>Xem bảng số</summary><div class="bang"><table>{bang}</table></div></details>',
        "nguon": "Tính trực tiếp từ moc/*.json (trường can_cu của mọi mốc có giá là số), phân loại theo từ khoá như cong_cu/kiem_can_cu.py.",
    }


# =====================================================================================
# HÌNH 5 — EMA hay SMA (bảng trong SO_LIEU_CAN_CU.md)
# =====================================================================================
def so_pt(s: str):
    m = re.search(r"(\d+(?:,\d+)?)\s*%", tron(s))
    return float(m.group(1).replace(",", ".")) if m else None


def tinh_ema_sma(so_lieu_text):
    if not so_lieu_text:
        return None
    lines = so_lieu_text.split("\n")
    head, rows = bang_sau(lines, r"MA — người đó dùng EMA|SMA lệch")
    if not rows:
        i = next((k for k, l in enumerate(lines) if "SMA lệch" in l), None)
        if i is None:
            return None
        head, rows = bang_sau(lines[i - 1:], r".")
    out = []
    for r in rows:
        r = (r + [""] * 5)[:5]
        out.append({"ten": tron(r[0]), "n": tron(r[1]), "sma": so_pt(r[2]), "ema": so_pt(r[3]), "dai": so_pt(r[4]),
                    "ghi": tron(r[4]) if r[4] else ""})
    return out


def hinh_ema_sma(E):
    if not E:
        return None
    ema_tot = sum(1 for e in E if e["ema"] is not None and e["sma"] is not None and e["ema"] < e["sma"])
    return {
        "tieu_de": "EMA hay SMA",
        "mo_ta": f"Sai số trung vị giữa con số người đó nói (“MA34 H4 ở …”) và giá trị tính lại từ giá thật. "
                 f"Cột càng ngắn càng khớp. EMA khớp hơn SMA ở {ema_tot}/{len(E)} dòng; dải EMA34 (high/low) khớp nhất.",
        "than": '<div class="cj-khung cao-380"><canvas id="cj-ema" role="img" aria-label="Biểu đồ cột sai số SMA, EMA, dải EMA34"></canvas></div>',
        "nguon": "Tính từ bảng “Truy ngược công thức” trong SO_LIEU_CAN_CU.md.",
    }


# =====================================================================================
# HÌNH 6 — Sonic R trên chart thật  +  dữ liệu nến cho HÌNH "Mốc giá"
# =====================================================================================
def tinh_nen(n4):
    if not n4:
        return None
    c = [r[4] for r in n4]
    hi = [r[2] for r in n4]
    lo = [r[3] for r in n4]
    e34c, e34h, e34l = ema(c, 34), ema(hi, 34), ema(lo, 34)
    e89, e200, e610 = ema(c, 89), ema(c, 200), ema(c, 610)
    bd = dt.datetime(NAM - 1, 12, 1, tzinfo=dt.timezone.utc).timestamp()
    idx = [i for i, r in enumerate(n4) if r[0] >= bd]

    def r1(x):
        return None if x is None else round(x, 1)

    return {
        "t": [n4[i][0] + VN_S for i in idx],  # giờ VN, dạng "UTC giả" cho lightweight-charts
        "o": [n4[i][1] for i in idx], "h": [n4[i][2] for i in idx], "l": [n4[i][3] for i in idx], "c": [n4[i][4] for i in idx],
        "e34c": [r1(e34c[i]) for i in idx], "e34h": [r1(e34h[i]) for i in idx], "e34l": [r1(e34l[i]) for i in idx],
        "e89": [r1(e89[i]) for i in idx], "e200": [r1(e200[i]) for i in idx], "e610": [r1(e610[i]) for i in idx],
    }


def tinh_sonic(nen, so_nen=150):
    if not nen or len(nen["t"]) < 20:
        return None
    n = len(nen["t"])
    a = max(0, n - so_nen)
    ih = max(range(a, n), key=lambda i: nen["h"][i])
    il = min(range(a, n), key=lambda i: nen["l"][i])
    if il < ih:   # đáy trước, đỉnh sau → nhịp tăng: mức 1 ở đáy, 0 ở đỉnh
        dau, cuoi = (nen["t"][il], nen["l"][il]), (nen["t"][ih], nen["h"][ih])
        chieu = "tăng"
    else:
        dau, cuoi = (nen["t"][ih], nen["h"][ih]), (nen["t"][il], nen["l"][il])
        chieu = "giảm"
    muc = [{"r": r, "gia": round(cuoi[1] + r * (dau[1] - cuoi[1]), 1)} for r in (0, 0.236, 0.382, 0.5, 0.618, 0.786, 1)]
    return {"so_nen": so_nen, "dau": {"t": dau[0], "p": dau[1]}, "cuoi": {"t": cuoi[0], "p": cuoi[1]}, "chieu": chieu,
            "muc": muc, "tu": nen["t"][a], "den": nen["t"][-1]}


def ngay_vn(t_vn: int, gio=False) -> str:
    d = dt.datetime.fromtimestamp(t_vn, dt.timezone.utc)
    return d.strftime("%d/%m %H:%M") if gio else d.strftime("%d/%m/%Y")


def hinh_sonic(S):
    if not S:
        return None
    m = {x["r"]: x["gia"] for x in S["muc"]}
    return {
        "tieu_de": "Sonic R trên chart thật",
        "mo_ta": f"BTC H4, {S['so_nen']} nến gần nhất ({ngay_vn(S['tu'])} → {ngay_vn(S['den'] + H4)}, giờ VN). "
                 f"Dải EMA34 (EMA34 của high và low) tô mờ quanh đường EMA34 vàng, EMA89 xanh dương, EMA200 tím, EMA610 xanh ngọc. "
                 f"Fibo thoái lui kéo theo nhịp {S['chieu']} lớn nhất trong khung: mức 1 = {fmt_gia(S['dau']['p'])}, mức 0 = {fmt_gia(S['cuoi']['p'])} "
                 f"(0.382 = {fmt_gia(m[0.382])} · 0.5 = {fmt_gia(m[0.5])} · 0.618 = {fmt_gia(m[0.618])}). Kéo/cuộn để zoom.",
        "than": '<div class="lw-chu-giai" id="cg-sonic"></div><div class="lw-khung cao-440" id="lw-sonic"></div>',
        "nguon": "Minh hoạ cách bộ chỉ báo trông thế nào, không phải nhận định. Nến và EMA tính từ du_lieu/btc_4H.csv; "
                 "màu theo chart thật của người đó (mục D3: dải xám quanh EMA34 vàng, EMA89 xanh, EMA200 tím, EMA610 xanh ngọc; Fibo 0.5 vàng, 0.382/0.618 xanh ngọc).",
    }


# =====================================================================================
# HÌNH 7 — Hội tụ căn cứ (A4.10)
# =====================================================================================
def doc_gia(s: str):
    s = s.strip().replace("~", "")
    m = re.match(r"^(\d+(?:[.,]\d+)?)(?:\s*[–-]\s*(\d+(?:[.,]\d+)?))?\s*([kK])?", s)
    if not m:
        return None

    def mot(x, k):
        if not k and re.fullmatch(r"\d{1,3}\.\d{3}", x):
            return float(x.replace(".", ""))
        v = float(x.replace(",", "."))
        return v * 1000 if (k or v < 1000) else v

    k = bool(m.group(3))
    a = mot(m.group(1), k)
    b = mot(m.group(2), k) if m.group(2) else None
    return (a, b), s[m.end():].strip()


def tach_chip(s: str) -> list[str]:
    s = re.sub(r"\s*\(\d+ căn cứ\)", "", s)
    ps = re.split(r"\s+\+\s+|\s+hợp lưu\s+|\s+trùng\s+|;\s*", s)
    out = []
    for p in ps:
        p = p.strip(" .")
        if not p:
            continue
        sub = re.split(r"\s+và\s+(?=[A-ZĐ])", p)
        out.extend(x.strip(" .") for x in sub if x.strip(" ."))
    return out


def doc_vi_du(lines):
    _, rows = bang_sau(lines, r"^### A4\.10")
    vds = []
    for r in rows:
        if len(r) < 5:
            continue
        so, ngay_neu, con_so, can_cu, ket_qua = r[:5]
        # giá theo vai trò
        vai = []
        bolds = list(re.finditer(r"\*\*(.+?)\*\*", con_so))
        for i, b in enumerate(bolds):
            g = doc_gia(b.group(1))
            if not g:
                continue
            sau = con_so[b.end(): bolds[i + 1].start() if i + 1 < len(bolds) else len(con_so)]
            nhan = tron(sau).strip(" ,;")
            mp = re.match(r"^\(([^)]*)\)", nhan)
            nhan = mp.group(1) if mp else nhan
            vai.append({"gia": g[0], "nhan": cat(nhan.replace("là ", ""), 40)})
        # tách căn cứ thành các mức
        t = tron(can_cu)
        muc = []   # {gia:(a,b), nhan, chips[]}
        ghi = []
        khong = "(0 căn cứ)" in t
        cau = [c.strip() for c in re.split(r"\.\s+", t) if c.strip()]
        co_bang = any("=" in c for c in cau)
        tien_to = ""
        for c in cau:
            c = c.rstrip(".")
            m1 = re.match(r"^Mức\s+([\d.]+)\s*=\s*([\d.,–-]+k?)\s+trùng\s+(.+)$", c)
            if m1:
                g = doc_gia(m1.group(2))
                if g:
                    muc.append({"gia": g[0], "nhan": "", "chips": [f"{tien_to or 'Fibo'} {m1.group(1)}"] + tach_chip(m1.group(3))})
                continue
            m2 = re.match(r"^(\d[\d.,–-]*k?(?:\s+[^\s=]+)?)\s*=\s*(.+)$", c)
            if m2:
                g = doc_gia(m2.group(1))
                if g:
                    muc.append({"gia": g[0], "nhan": g[1], "chips": tach_chip(m2.group(2))})
                continue
            m3 = re.match(r"^(TP\d?|Đích|SL)\s*=\s*(.+)$", c)
            if m3:
                v = next((x for x in vai if m3.group(1).lower() in x["nhan"].lower()), None)
                if v:
                    muc.append({"gia": v["gia"], "nhan": m3.group(1), "chips": tach_chip(m3.group(2))})
                continue
            if co_bang:
                ghi.append(c)
                mf = re.match(r"^(Fibo [^\d]+)", c)
                if mf:
                    tien_to = mf.group(1).strip()
                continue
            # không có dấu "=": các vế ; là các nhóm căn cứ của mức chính
            for ve in c.split(";"):
                mk = re.search(r"(\d+(?:[.,]\d+)?k?)\s+thành\s+(kháng cự|hỗ trợ)", ve)
                if mk:
                    g = doc_gia(mk.group(1))
                    chips = [x for x in tach_chip(ve) if not re.search(r"thành\s+(kháng cự|hỗ trợ)", x)]
                    if g:
                        muc.append({"gia": g[0], "nhan": mk.group(2), "chips": chips})
                    continue
                if vai and not khong:
                    chips = tach_chip(ve)
                    goc = next((x for x in muc if x.get("chinh")), None)
                    if goc:
                        goc["chips"].extend(chips)
                    else:
                        muc.append({"gia": vai[0]["gia"], "nhan": vai[0]["nhan"], "chips": chips, "chinh": True})
        # gộp giá vai trò chưa có căn cứ vào mức gần (≤1,5%)
        vung = []
        for v in vai:
            a = v["gia"][0]
            gan = [x for x in muc if abs(x["gia"][0] - a) / a <= 0.015 and x["gia"][1] is None and v["gia"][1] is None]
            if any(x["gia"] == v["gia"] for x in muc):
                continue
            if gan:
                gan[0]["nhan"] = gan[0]["nhan"] or v["nhan"]
                continue
            vung.append(v)
        ngay = re.findall(r"(\d{2})-(\d{2})", ngay_neu)
        kq_ngay = [(int(mm), int(dd)) for dd, mm in re.findall(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?![\d/])", ket_qua)]
        kq_ngay += [(int(a), int(b)) for a, b in re.findall(r"\[(\d{2})-(\d{2})\]", ket_qua)]
        kq_ngay = [x for x in kq_ngay if 1 <= x[0] <= 12 and 1 <= x[1] <= 31]
        ket = [tron(x) for x in re.findall(r"\*\*(.+?)\*\*", ket_qua)]
        for x in muc:   # câu trích nguyên văn "…" không phải căn cứ → chuyển sang ghi chú
            q = [c for c in x["chips"] if re.fullmatch(r'"[^"]*"', c.strip())]
            x["chips"] = [c for c in x["chips"] if c not in q]
            ghi += [c.strip('"') for c in q]
        if ngay:
            d0 = (int(ngay[0][0]), int(ngay[0][1]))
            kq_ngay = [x for x in kq_ngay if x >= d0]
        so_chip = max((len(x["chips"]) for x in muc), default=0)
        vds.append({
            "so": tron(so), "ngay_neu": tron(ngay_neu), "ngay": [(int(a), int(b)) for a, b in ngay],
            "con_so": tron(con_so), "vai": vai, "muc": muc, "vung": vung, "ghi": ghi, "khong": khong,
            "ket_qua": tron(ket_qua), "ket_qua_md": ket_qua, "ket": ket, "kq_ngay": kq_ngay, "so_chip": 0 if khong else so_chip,
        })
    return vds


def chon_vi_du(vds, so=4):
    co = [v for v in vds if v["muc"] and v["ngay"]]
    co.sort(key=lambda v: (-v["so_chip"], int(re.sub(r"\D", "", v["so"]) or 0)))
    pick = co[:so]
    pick.sort(key=lambda v: int(re.sub(r"\D", "", v["so"]) or 0))
    return pick


def svg_hoi_tu(vd, n1d):
    if not n1d:
        return ""
    mm, dd = vd["ngay"][0]
    bd = dt.datetime(NAM, mm, dd, tzinfo=dt.timezone.utc)
    het = max([dt.datetime(NAM, a, b, tzinfo=dt.timezone.utc) for a, b in vd["kq_ngay"]] + [bd + dt.timedelta(days=7)])
    if len(vd["ngay"]) > 1:
        het = max(het, dt.datetime(NAM, *vd["ngay"][-1], tzinfo=dt.timezone.utc))
    t0 = (bd - dt.timedelta(days=10)).timestamp()
    t1 = (het + dt.timedelta(days=4)).timestamp()
    nen = [r for r in n1d if t0 <= r[0] <= t1]
    if len(nen) < 3:
        return ""
    gia_muc = []
    for x in vd["muc"]:
        gia_muc += [x["gia"][0]] + ([x["gia"][1]] if x["gia"][1] else [])
    for v in vd["vung"]:
        gia_muc += [v["gia"][0]] + ([v["gia"][1]] if v["gia"][1] else [])
    lo = min([r[3] for r in nen] + gia_muc)
    hi = max([r[2] for r in nen] + gia_muc)
    pad = (hi - lo) * 0.06
    lo, hi = lo - pad, hi + pad
    W, H = 760, 360
    x0, x1, y0, y1 = 56, 410, 30, H - 34
    cx0 = 440

    def Y(p):
        return y1 - (p - lo) / (hi - lo) * (y1 - y0)

    n = len(nen)
    bw = (x1 - x0) / n

    def X(i):
        return x0 + bw * (i + 0.5)

    o = [f'<svg viewBox="0 0 {W} {H}" class="svg-hoi-tu" role="img" aria-label="Hội tụ căn cứ {esc(vd["so"])}">']
    # lưới giá
    span = hi - lo
    buoc = next(s for s in (250, 500, 1000, 2000, 2500, 5000, 10000, 20000) if span / s <= 7)
    g = (int(lo // buoc) + 1) * buoc
    while g < hi:
        y = Y(g)
        o.append(f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" class="ht-luoi"/>'
                 f'<text x="{x0-6}" y="{y+4:.1f}" class="ht-truc" text-anchor="end">{g/1000:g}k</text>')
        g += buoc
    # trục thời gian
    buoc_n = max(1, n // 6)
    for i in range(0, n, buoc_n):
        d = dt.datetime.fromtimestamp(nen[i][0], dt.timezone.utc)
        o.append(f'<text x="{X(i):.1f}" y="{y1+18}" class="ht-truc" text-anchor="middle">{d:%d/%m}</text>')
    o.append(f'<line x1="{x0}" x2="{x1}" y1="{y1}" y2="{y1}" class="ht-day"/>')
    # vùng vai trò chưa có căn cứ riêng (vd "trần 82–83,3k")
    for v in vd["vung"]:
        a, b = v["gia"]
        if b:
            ya, yb = Y(max(a, b)), Y(min(a, b))
            o.append(f'<rect x="{x0}" y="{ya:.1f}" width="{x1-x0}" height="{yb-ya:.1f}" class="ht-vung"/>')
            o.append(f'<text x="{x0+6}" y="{ya+13:.1f}" class="ht-vung-chu">{esc(v["nhan"] or "vùng")} {fmt_gia(a)}–{fmt_gia(b)}</text>')
        else:
            o.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(a):.1f}" y2="{Y(a):.1f}" class="ht-vung-duong"/>'
                     f'<text x="{x0+6}" y="{Y(a)-4:.1f}" class="ht-vung-chu">{esc(v["nhan"])} {fmt_gia(a)}</text>')
    # nến ngày
    for i, r in enumerate(nen):
        _, op, h, l, c = r
        cls = "ht-tang" if c >= op else "ht-giam"
        x = X(i)
        yt, yb = Y(max(op, c)), Y(min(op, c))
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(h):.1f}" y2="{Y(l):.1f}" class="{cls} ht-rau"/>'
                 f'<rect x="{x-bw*0.32:.1f}" y="{yt:.1f}" width="{bw*0.64:.1f}" height="{max(1, yb-yt):.1f}" class="{cls}"/>')
    # mốc ngày nêu
    for k, (a, b) in enumerate(vd["ngay"][:2]):
        tn = dt.datetime(NAM, a, b, tzinfo=dt.timezone.utc).timestamp()
        idx = next((i for i, r in enumerate(nen) if r[0] >= tn), None)
        if idx is None:
            continue
        x = X(idx)
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y0-6}" y2="{y1}" class="ht-neu"/>'
                 f'<text x="{x+4:.1f}" y="{y0-10 + 12*k}" class="ht-neu-chu">nêu {b:02d}/{a:02d}</text>')
    # các mức có căn cứ + chồng nhãn
    muc = sorted(vd["muc"], key=lambda x: -x["gia"][0])
    khoi = []
    for x in muc:
        a, b = x["gia"]
        y = Y(a if not b else (a + b) / 2)
        cao = 20 + 21 * len(x["chips"])
        khoi.append({"m": x, "y": y, "cao": cao})
    tren = y0 - 14
    for k in khoi:
        k["top"] = max(k["y"] - k["cao"] / 2, tren)
        tren = k["top"] + k["cao"] + 8
    du = tren - 8 - (H - 4)
    if du > 0:
        for k in khoi:
            k["top"] -= du
    for k in khoi:
        x = k["m"]
        a, b = x["gia"]
        cc_cls = f"ht-muc ht-muc-{min(len(x['chips']), 4)}"
        if b:
            ya, yb = Y(max(a, b)), Y(min(a, b))
            o.append(f'<rect x="{x0}" y="{ya:.1f}" width="{x1-x0}" height="{max(2, yb-ya):.1f}" class="{cc_cls} ht-muc-vung"/>')
        else:
            o.append(f'<line x1="{x0}" x2="{x1+12}" y1="{k["y"]:.1f}" y2="{k["y"]:.1f}" class="{cc_cls}"/>')
        ty = k["top"] + 10
        o.append(f'<path d="M{x1+12} {k["y"]:.1f} C{x1+22} {k["y"]:.1f}, {cx0-14} {ty:.1f}, {cx0-4} {ty:.1f}" class="ht-noi"/>')
        ten = fmt_gia(a) + (f"–{fmt_gia(b)}" if b else "") + (f"  {x['nhan']}" if x["nhan"] else "")
        o.append(f'<text x="{cx0}" y="{ty+4:.1f}" class="ht-gia">{esc(ten)}'
                 f'<tspan class="ht-dem" dx="8">{len(x["chips"])} căn cứ</tspan></text>')
        for j, c in enumerate(x["chips"]):
            yy = k["top"] + 20 + 21 * j
            loai = loai_can_cu(c)
            chu = cat(c, 42)
            w = min(W - cx0 - 4, 28 + len(chu) * 6.7)
            o.append(f'<g class="ht-chip cc-{loai}"><title>{esc(TEN_CC[loai])}: {esc(c)}</title>'
                     f'<rect x="{cx0}" y="{yy:.1f}" width="{w:.0f}" height="18" rx="9"/>'
                     f'<circle cx="{cx0+10}" cy="{yy+9:.1f}" r="4"/>'
                     f'<text x="{cx0+19}" y="{yy+13:.1f}">{esc(chu)}</text></g>')
    o.append("</svg>")
    return "".join(o)


def hinh_hoi_tu(vds, n1d):
    pick = chon_vi_du(vds)
    if not pick:
        return None
    tabs, panes = [], []
    for i, v in enumerate(pick):
        svg = svg_hoi_tu(v, n1d)
        if not svg:
            continue
        ket = " · ".join(v["ket"]) or "—"
        xau = "truot" if re.search(r"(?i)trượt", ket) and not re.search(r"(?i)đạt", ket) else (
            "pha" if re.search(r"(?i)trượt", ket) else "dat")
        nhan_gia = " / ".join(f"{a/1000:g}" + (f"–{b/1000:g}" if b else "") + "k" for a, b in (x["gia"] for x in v["vai"])) or cat(v["con_so"], 18)
        tabs.append(f'<button class="tab-ht{" dang" if not tabs else ""}" data-i="{i}">{esc(v["so"])} · {esc(nhan_gia)}'
                    f' <span class="huy-{xau}">{esc(cat(ket, 28))}</span></button>')
        ghi = (f'<p class="ht-ghi"><b>Ghi:</b> {esc("; ".join(v["ghi"]))}</p>' if v["ghi"] else "")
        panes.append(f'<div class="pane-ht" data-i="{i}"{"" if not panes else " hidden"}>'
                     f'<p class="ht-tom"><b>{esc(v["so"])}</b> — nêu {esc(v["ngay_neu"])}: {esc(v["con_so"])}</p>'
                     f'<div class="cuon-ngang"><div class="svg-wrap">{svg}</div></div>{ghi}'
                     f'<p class="ht-kq huy-{xau}"><b>Kết quả:</b> {md_dong(v["ket_qua_md"])}</p></div>')
    if not panes:
        return None
    chu_giai = "".join(f'<span class="cg cc-{k}"><i></i>{esc(TEN_CC[k])}</span>'
                       for k in ("fibo", "ma", "dinhday", "thanhly", "gap", "trend", "mohinh", "khac"))
    return {
        "tieu_de": "Hội tụ căn cứ",
        "mo_ta": f"{len(panes)} ví dụ có nhiều căn cứ nhất trong mục A4.10 (tự chọn lúc dựng). Mỗi vạch là một mức giá, "
                 "các căn cứ trùng nhau chồng thành cột nhãn bên phải; nến ngày thật cho thấy giá đi thế nào sau khi nêu.",
        "than": f'<div class="tabs-ht">{"".join(tabs)}</div><div class="chu-giai-cc">{chu_giai}</div>{"".join(panes)}',
        "nguon": "Mức giá + căn cứ tách tự động từ bảng A4.10 (dấu “=”, “+”, “trùng”, “hợp lưu”); nến D1 từ du_lieu/btc_1Dutc.csv.",
    }


# =====================================================================================
# HÌNH 8 — Mốc giá người đó nêu trên chart thật (dữ liệu cho JS)
# =====================================================================================
def tinh_moc_js(buoi, vds):
    out = []
    for b in buoi:
        ms = []
        for m in b["moc"]:
            g = m.get("gia")
            if not isinstance(g, (int, float)):
                continue
            gt = m.get("gia_tren") if isinstance(m.get("gia_tren"), (int, float)) else None
            cc = [s for s in (m.get("can_cu") or []) if isinstance(s, str) and s.strip()]
            ms.append([g, gt, m.get("vai_tro") or "khac", m.get("khung") or "", cc, (m.get("trich") or "")[:400],
                       m.get("moc_gio") or "", m.get("huong") or "", 1 if m.get("chac", True) else 0])
        out.append({"id": b["id"], "ngay": b["ngay"], "gio": b["gio"], "td": b["tieu_de"], "gn": b["gia_noi"], "m": ms})
    # buổi tiêu biểu = ngày nêu của các ví dụ A4.10
    mau = []
    theo_ngay = defaultdict(list)
    for b in out:
        theo_ngay[b["ngay"]].append(b)
    for v in vds:
        if not v["ngay"]:
            continue
        a, d = v["ngay"][0]
        key = f"{NAM}-{a:02d}-{d:02d}"
        if theo_ngay.get(key):
            bb = max(theo_ngay[key], key=lambda x: len(x["m"]))
            mau.append({"nhan": f"{v['so']} · {d:02d}/{a:02d}", "id": bb["id"], "ghi": cat(v["con_so"], 60)})
    return out, mau


def hinh_moc(buoi_js):
    if not buoi_js:
        return None
    tong = sum(len(b["m"]) for b in buoi_js)
    return {
        "tieu_de": "Mốc giá người đó nêu trên chart thật",
        "mo_ta": f"Chọn 1 trong {len(buoi_js)} buổi live: nến H4 thật ~10 ngày trước và ~5 ngày sau buổi đó, bộ EMA Sonic R, "
                 f"và một đường ngang cho TỪNG mốc người đó nêu ({fmt_gia(tong)} mốc cả năm). Đường mờ chấm = trước giờ live, "
                 "đường đậm = từ lúc live trở đi. Nhãn = giá · vai trò · căn cứ người đó nói. Bấm một dòng trong bảng để làm nổi mốc đó.",
        "than": """
<div class="moc-dk">
  <label class="chon-buoi"><span>Buổi live</span><select id="chon-buoi"></select></label>
  <div class="nut-mau" id="nut-mau"></div>
</div>
<div class="moc-dk2"><div class="cg-vai" id="cg-vai"></div>
  <label class="o-chon"><input type="checkbox" id="hien-ema" checked> Bộ EMA</label></div>
<div class="lw-chu-giai" id="cg-moc"></div>
<div class="lw-khung cao-540" id="lw-moc"></div>
<p class="moc-tom" id="moc-tom"></p>
<div class="bang bang-moc"><table id="bang-moc"></table></div>""",
        "nguon": "Mốc + căn cứ + câu trích từ moc/*.json; giờ bắt đầu live từ tên file / transcripts/danh_sach.tsv (mặc định 10:00); "
                 "nến H4 từ du_lieu/btc_4H.csv. “Chạm trong 5 ngày” = có nến H4 sau lúc nói mà biên độ trùm mốc — chỉ là đối chiếu, không chấm đúng/sai.",
    }


# =====================================================================================
# HÌNH 9 — Ảnh chart từ livestream
# =====================================================================================
def doc_ghi_chu_anh():
    cap = {}
    for p in sorted(P_GHI_CHU.glob("hinh_anh_*.md")) if P_GHI_CHU.exists() else []:
        vid = None
        for ln in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^###\s+(?:Video\s+)?([A-Za-z0-9_-]{11})(?=[\s(—-]|$)", ln)
            if m:
                vid = m.group(1)
                continue
            if ln.startswith("## ") or ln.startswith("# "):
                vid = None
                continue
            if vid and ln.startswith("|"):
                c = tach_o(ln)
                mt = re.match(r"^(\d{2}):(\d{2}):(\d{2})", c[0]) if c else None
                if mt and len(c) >= 3:
                    cap[f"{vid}_{mt.group(1)}{mt.group(2)}{mt.group(3)}"] = {
                        "cap": c[1], "thay": c[2], "khop": c[3] if len(c) > 3 else "", "file": p.name}
    return cap


def tao_thumb(anh: list[Path]) -> bool:
    if not shutil.which("sips"):
        return False
    P_THUMB.mkdir(exist_ok=True)
    for p in anh:
        q = P_THUMB / p.name
        if q.exists() and q.stat().st_mtime >= p.stat().st_mtime:
            continue
        subprocess.run(["sips", "-Z", "480", "-s", "formatOptions", "68", str(p), "--out", str(q)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True


def tinh_anh(buoi, ds):
    anh = sorted(P_KHUNG.glob("*.jpg")) if P_KHUNG.exists() else []
    if not anh:
        return [], {}, 0
    co_thumb = tao_thumb(anh)
    cap = doc_ghi_chu_anh()
    vid_ngay = {b["vid"]: b["ngay"] for b in buoi}
    vid_td = {b["vid"]: b["tieu_de"] for b in buoi}
    for vid, info in ds.items():
        vid_ngay.setdefault(vid, info["ngay"])
        vid_td.setdefault(vid, info["tieu_de"])
    ds_anh = []
    for p in anh:
        vid, _, hms = p.stem.rpartition("_")
        if not vid or not re.fullmatch(r"\d{6}", hms):
            continue
        gio = f"{hms[:2]}:{hms[2:4]}:{hms[4:]}"
        c = cap.get(p.stem)
        thumb = f"thumbs/{p.name}" if co_thumb and (P_THUMB / p.name).exists() else f"../so_tay/khung/{p.name}"
        ds_anh.append({
            "ten": p.stem, "vid": vid, "gio": gio, "ngay": vid_ngay.get(vid, ""), "td": vid_td.get(vid, ""),
            "src": f"../so_tay/khung/{p.name}", "thumb": thumb,
            "cap_ngan": cat(tron(c["cap"]), 46) if c else "",
            "cap": (f'<p><b>{md_dong(c["cap"])}</b></p><p>{md_dong(c["thay"])}</p>'
                    + (f'<p class="lb-khop"><b>Khớp lời nói:</b> {md_dong(c["khop"])}</p>' if c["khop"] else "")) if c else "",
        })
    ds_anh.sort(key=lambda a: (a["ngay"] or "9999", a["vid"], a["gio"]))
    so_cap = sum(1 for a in ds_anh if a["cap"])
    return ds_anh, cap, so_cap


def hinh_anh(ds_anh, so_cap):
    if not ds_anh:
        return None
    nhom = defaultdict(list)
    for i, a in enumerate(ds_anh):
        nhom[(a["ngay"], a["vid"])].append((i, a))
    sec = []
    for (ngay, vid), ds in sorted(nhom.items()):
        td = ds[0][1]["td"]
        nd = f"{ngay[8:10]}/{ngay[5:7]}" if ngay else "?"
        co = sum(1 for _, a in ds if a["cap"])
        o = [f'<section class="nhom-anh{" chua-ghi" if not co else ""}"><h4><span class="na-ngay">{nd}</span> '
             f'{esc(cat(td, 80) or vid)} <small>{len(ds)} ảnh · {co} có ghi chú · <code>{esc(vid)}</code></small></h4><div class="luoi-anh">']
        for i, a in ds:
            o.append(f'<button class="o-anh{" co-ghi" if a["cap"] else ""}" data-i="{i}" title="Phóng to">'
                     f'<img loading="lazy" decoding="async" src="{esc(a["thumb"])}" alt="Ảnh live {esc(a["vid"])} lúc {a["gio"]}">'
                     f'<span class="oa-gio">{a["gio"]}</span>'
                     f'<span class="oa-cap">{esc(a["cap_ngan"]) if a["cap_ngan"] else "<i>chưa có ghi chú</i>"}</span></button>')
        o.append("</div></section>")
        sec.append("".join(o))
    return {
        "tieu_de": "Ảnh chart từ livestream",
        "mo_ta": f"{len(ds_anh)} ảnh chụp màn hình live của {len(nhom)} buổi, {so_cap} ảnh đã có ghi chú. "
                 "Bấm ảnh để phóng to; dùng ← → để qua lại, Esc để đóng.",
        "than": f'<label class="o-chon loc-anh"><input type="checkbox" id="chi-co-ghi"> Chỉ hiện ảnh đã có ghi chú</label>{"".join(sec)}',
        "nguon": "Ảnh: so_tay/khung/*.jpg. Chú thích: so_tay/ghi_chu/hinh_anh_*.md (ghép theo tên ảnh <video>_<hhmmss>).",
    }


# =====================================================================================
# Ghép trang
# =====================================================================================
def chen_hinh(lines: list[str], ten: str, heading: str, cach: str, mau_dong: str | None = None) -> bool:
    """Chèn dòng giữ chỗ @@HINH:ten@@ vào markdown.
    cach: 'truoc_bang' (trước bảng đầu tiên của mục) | 'cuoi_muc' (trước tiêu đề kế tiếp) | 'sau_bang' | 'truoc_dong' (dòng khớp mau_dong)."""
    rx = re.compile(heading)
    i = next((k for k, l in enumerate(lines) if rx.search(l)), None)
    if i is None:
        return False
    j = i + 1
    ket = None
    while j < len(lines):
        l = lines[j]
        if l.startswith("#"):
            break
        if cach == "truoc_bang" and l.lstrip().startswith("|"):
            ket = j
            break
        if cach == "sau_bang" and l.lstrip().startswith("|"):
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            ket = j
            break
        if cach == "truoc_dong" and mau_dong and re.search(mau_dong, l):
            ket = j
            break
        j += 1
    if ket is None:
        ket = j
        while ket > i + 1 and lines[ket - 1].strip() in ("", "---"):
            ket -= 1
    lines[ket:ket] = ["", f"@@HINH:{ten}@@", ""]
    return True


def html_hinh(h: dict, so: int, ma: str) -> str:
    return (f'<figure class="hinh" id="hinh-{ma}"><figcaption class="hinh-tieu"><span class="so">Hình {so}</span>{esc(h["tieu_de"])}</figcaption>'
            f'<p class="hinh-mo-ta">{h["mo_ta"] if "<" in h["mo_ta"] else esc(h["mo_ta"])}</p>{h["than"]}'
            f'<p class="hinh-nguon">{esc(h["nguon"])}</p></figure>')


def ha_tieu_de(md: str, ten_muc: str) -> str:
    """Hạ cấp tiêu đề của file phụ để ghép vào phụ lục: '# X' → '## ten_muc — X', '## ' → '### '."""
    out = []
    for ln in md.split("\n"):
        m = re.match(r"^(#{1,5})\s+(.*)$", ln)
        if m:
            lv = len(m.group(1))
            out.append(f"## {ten_muc} — {m.group(2)}" if lv == 1 else "#" * min(lv + 1, 6) + " " + m.group(2))
        else:
            out.append(ln)
    return "\n".join(out)


def gan_anh_vao_code(h: str, ds_anh) -> str:
    """`VID hh:mm:ss` trong bảng → thêm nút mở ảnh chụp gần nhất (±2 phút)."""
    theo_vid = defaultdict(list)
    for i, a in enumerate(ds_anh):
        hh, mm, ss = map(int, a["gio"].split(":"))
        theo_vid[a["vid"]].append((hh * 3600 + mm * 60 + ss, i))

    def thay(m):
        vid = m.group(1)
        s = int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
        ds = theo_vid.get(vid)
        if not ds:
            return m.group(0)
        d, i = min((abs(t - s), i) for t, i in ds)
        if d > 120:
            return m.group(0)
        return m.group(0) + f'<button class="nut-anh" data-i="{i}" title="Xem ảnh chụp lúc {ds_anh[i]["gio"]}">ảnh</button>'

    return re.sub(r"<code>([A-Za-z0-9_-]{11}) (\d{2}):(\d{2}):(\d{2})[^<]*</code>", thay, h)


def hau_xu_ly(h: str) -> str:
    h = h.replace("<table>", '<div class="bang"><table>').replace("</table>", "</table></div>")
    h = re.sub(r"<(li|p)>(\s*)▸", r'<\1 class="ykien">\2<span class="dau-yk">▸</span>', h)
    h = re.sub(r"(?<!>)▸", '<span class="dau-yk">▸</span>', h)
    return h


def muc_luc(h: str) -> str:
    o = []
    for m in re.finditer(r'<h([123]) id="([^"]+)">(.*?)</h\1>', h, re.S):
        lv, idd, txt = int(m.group(1)), m.group(2), re.sub(r"<[^>]+>", "", m.group(3))
        txt = html.unescape(txt)
        o.append(f'<li class="ml-{lv}"><a href="#{esc(idd)}">{esc(cat(txt, 70))}</a></li>')
    return "".join(o)


def main():
    so_tay = doc(P_SO_TAY)
    if not so_tay:
        sys.exit(f"Không thấy {P_SO_TAY}")
    so_lieu = doc(P_SO_LIEU)
    doi_chieu = doc(P_DOI_CHIEU)
    ds = doc_danh_sach()
    buoi = doc_moc(ds)
    n4 = doc_nen(P_4H)
    n1d = doc_nen(P_1D)
    lines = so_tay.split("\n")

    # --- tiêu đề trang ---
    tieu = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else "Sổ tay tinh hoa"
    ten_chinh, _, phu = tieu.partition(" — ")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]

    # --- tính số liệu + hình ---
    luat = doc_luat(lines)
    T = tinh_thang(buoi, so_tay)
    E = tinh_ema_sma(so_lieu)
    nen = tinh_nen(n4)
    S = tinh_sonic(nen)
    vds = doc_vi_du(lines)
    buoi_js, mau = tinh_moc_js(buoi, vds)
    ds_anh, _cap, so_cap = tinh_anh(buoi, ds)

    hinh = {
        "cong_cu": hinh_cong_cu(lines),
        "quy_trinh": hinh_quy_trinh(lines),
        "cay": hinh_cay(lines, luat),
        "moc": hinh_moc(buoi_js) if nen else None,
        "thang": hinh_thang(T),
        "ema": hinh_ema_sma(E),
        "sonic": hinh_sonic(S),
        "hoi_tu": hinh_hoi_tu(vds, n1d),
        "anh": hinh_anh(ds_anh, so_cap),
    }
    for k, v in hinh.items():
        if v is None:
            CANH_BAO.append(f"hình '{k}' bỏ qua (thiếu dữ liệu)")

    # --- chèn chỗ đặt hình vào markdown ---
    vi_tri = [
        ("cong_cu", r"^## A1\.", "truoc_bang", None),
        ("quy_trinh", r"^## A2\.", "truoc_bang", None),
        ("cay", r"^## A3\.", "cuoi_muc", None),
        ("moc", r"^### A4\.1\b", "cuoi_muc", None),
        ("thang", r"^### A4\.4\b", "truoc_bang", None),
        ("ema", r"^### A4\.6\b", "cuoi_muc", None),
        ("sonic", r"^### A4\.6\b", "cuoi_muc", None),
        ("hoi_tu", r"^### A4\.10\b", "sau_bang", None),
    ]
    du = []
    for ten, hd, cach, md in vi_tri:
        if hinh.get(ten) and not chen_hinh(lines, ten, hd, cach, md):
            du.append(ten)
    # phụ lục
    phu_luc = ["", "---", "", "# PHỤ LỤC", ""]
    if hinh.get("anh"):
        phu_luc += ["## P1. Ảnh chart từ livestream", "", "@@HINH:anh@@", ""]
    for ten in du:
        phu_luc += [f"@@HINH:{ten}@@", ""]
    if so_lieu:
        phu_luc += [ha_tieu_de(so_lieu, "P2"), ""]
    if doi_chieu:
        phu_luc += [ha_tieu_de(doi_chieu, "P3"), ""]
    md_all = "\n".join(lines + phu_luc)

    body = md_khoi(md_all)
    body = hau_xu_ly(body)
    dem = [0]
    da_dung = []

    def thay_hinh(m):
        ten = m.group(1)
        h = hinh.get(ten)
        if not h:
            return ""
        dem[0] += 1
        da_dung.append(ten)
        return html_hinh(h, dem[0], ten)

    body = re.sub(r"<p>@@HINH:(\w+)@@</p>", thay_hinh, body)
    body = gan_anh_vao_code(body, ds_anh)
    toc = muc_luc(body)

    du_lieu = {
        "nen": nen, "sonic": S, "thang": T, "ema": E, "buoi": buoi_js, "mau": mau,
        "anh": [{"src": a["src"], "ten": a["ten"], "gio": a["gio"], "ngay": a["ngay"], "td": a["td"], "cap": a["cap"]} for a in ds_anh],
    }
    js_data = json.dumps(du_lieu, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    bay_gio = dt.datetime.now().strftime("%d/%m/%Y %H:%M")
    meta = (f"Dựng lúc {bay_gio} từ {len(buoi)} buổi live · {fmt_gia(T['tong'])} mốc giá · "
            f"{len(nen['t']) if nen else 0} nến H4 · {len(ds_anh)} ảnh ({so_cap} có ghi chú)")
    trang = (TRANG.replace("__TITLE__", esc(ten_chinh.title() if ten_chinh.isupper() else ten_chinh))
             .replace("__TEN__", esc(ten_chinh))
             .replace("__PHU__", esc(phu))
             .replace("__META__", esc(meta))
             .replace("__TOC__", toc)
             .replace("__CSS__", CSS)
             .replace("__BODY__", body)
             .replace("__JS__", JS)
             .replace("__DATA__", js_data))
    ra = HERE / "index.html"
    ra.write_text(trang, encoding="utf-8")

    print(f"OK  {ra.relative_to(GOC)}  {ra.stat().st_size/1024:.0f} KB")
    print(f"    hình: {', '.join(da_dung)}")
    print(f"    {meta}")
    for c in CANH_BAO:
        print("    ! " + c)


# =====================================================================================
# CSS / JS / khung trang
# =====================================================================================
TRANG = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<script>try{var t=localStorage.getItem('sotay-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}catch(e){}</script>
<style>__CSS__</style>
</head>
<body>
<div class="thanh-tren"><button id="nut-ml" class="nut" aria-label="Mở mục lục">☰ Mục lục</button><span class="tt-ten">__TEN__</span><button class="nut nut-theme" aria-label="Đổi giao diện sáng/tối"></button></div>
<div class="khung">
  <nav id="muc-luc" class="muc-luc" aria-label="Mục lục">
    <div class="ml-dau"><a href="#dau" class="ml-ten">__TEN__</a><button class="nut nut-theme" aria-label="Đổi giao diện sáng/tối"></button></div>
    <ol class="ml-ds">__TOC__</ol>
  </nav>
  <main id="noi-dung">
    <header class="dau-trang" id="dau"><h1 class="tieu-chinh">__TEN__</h1><p class="tieu-phu">__PHU__</p><p class="meta">__META__</p></header>
    __BODY__
    <footer class="chan">Trang tĩnh chạy offline · biểu đồ nến: TradingView Lightweight Charts™ 4.2.3 (Apache-2.0) · đồ thị: Chart.js 4.4.7 (MIT) · dựng bằng <code>python3 web_so_tay/build.py</code></footer>
  </main>
</div>
<div class="nen-mo" id="nen-mo"></div>
<div id="lb" class="lb" hidden role="dialog" aria-modal="true" aria-label="Xem ảnh">
  <div class="lb-tren"><span id="lb-dem"></span><span id="lb-tieu"></span><button class="nut" id="lb-dong" aria-label="Đóng">✕</button></div>
  <div class="lb-giua"><button class="nut lb-nut" id="lb-truoc" aria-label="Ảnh trước">‹</button><img id="lb-anh" alt=""><button class="nut lb-nut" id="lb-sau" aria-label="Ảnh sau">›</button></div>
  <div class="lb-cap" id="lb-cap"></div>
</div>
<script type="application/json" id="du-lieu">__DATA__</script>
<script src="vendor/chart.umd.js"></script>
<script src="vendor/lightweight-charts.standalone.production.js"></script>
<script>__JS__</script>
</body>
</html>
"""

CSS = r"""
:root{color-scheme:light;
 --bg:#f6f5f1;--surface:#fff;--surface-2:#f0efea;--text:#1c1b19;--text-2:#4d4c47;--muted:#77766f;--border:#e2e0d8;--grid:#efeee8;
 --accent:#2a78d6;--accent-soft:#e6effb;--up:#26a69a;--down:#ef5350;
 --ema34:#d29a00;--ema34-dai:rgba(120,120,120,.17);--ema34-mep:rgba(120,120,120,.45);--ema89:#2a78d6;--ema200:#b03ca8;--ema610:#16a394;
 --fib-chinh:#16a394;--fib-5:#d29a00;--fib-phu:#9a998f;
 --cc-fibo:#2a78d6;--cc-ma:#6250d6;--cc-dinhday:#eb6834;--cc-thanhly:#d55181;--cc-gap:#e34948;--cc-trend:#1baf7a;--cc-tron:#a39400;--cc-mohinh:#8a6a3a;--cc-khac:#8f8e86;
 --vt-dich:#2a78d6;--vt-tp:#14a37f;--vt-ho_tro:#2e8b2e;--vt-khang_cu:#eb6834;--vt-entry:#6250d6;--vt-sl:#e34948;--vt-vo_hieu:#c2407a;--vt-khac:#8f8e86;
 --tang:#1a8f5a;--giam:#d63c3c;--cho:#b07a00;
 --yk-bg:#fff7e3;--yk-bd:#eda100;--pv-bg:#fff4e0;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;
 --bg:#111110;--surface:#1a1a19;--surface-2:#242422;--text:#f0efec;--text-2:#c3c2b7;--muted:#8f8e86;--border:#34332f;--grid:#262624;
 --accent:#3987e5;--accent-soft:#1c2a3c;--up:#26a69a;--down:#ef5350;
 --ema34:#e8b400;--ema34-dai:rgba(200,200,200,.12);--ema34-mep:rgba(200,200,200,.35);--ema89:#4a93ea;--ema200:#d06ccb;--ema610:#2bbfae;
 --fib-chinh:#2bbfae;--fib-5:#e8b400;--fib-phu:#77766f;
 --cc-fibo:#3987e5;--cc-ma:#9085e9;--cc-dinhday:#d95926;--cc-thanhly:#d55181;--cc-gap:#e66767;--cc-trend:#199e70;--cc-tron:#c9b94e;--cc-mohinh:#b08d57;--cc-khac:#8f8e86;
 --vt-dich:#3987e5;--vt-tp:#22b38e;--vt-ho_tro:#46ad46;--vt-khang_cu:#e0682f;--vt-entry:#9085e9;--vt-sl:#e66767;--vt-vo_hieu:#e07aa3;--vt-khac:#8f8e86;
 --tang:#3cbf7f;--giam:#ef6b6b;--cho:#d9a43a;
 --yk-bg:#2b2516;--yk-bd:#c98500;--pv-bg:#2a2214;
}}
:root[data-theme="dark"]{color-scheme:dark;
 --bg:#111110;--surface:#1a1a19;--surface-2:#242422;--text:#f0efec;--text-2:#c3c2b7;--muted:#8f8e86;--border:#34332f;--grid:#262624;
 --accent:#3987e5;--accent-soft:#1c2a3c;--up:#26a69a;--down:#ef5350;
 --ema34:#e8b400;--ema34-dai:rgba(200,200,200,.12);--ema34-mep:rgba(200,200,200,.35);--ema89:#4a93ea;--ema200:#d06ccb;--ema610:#2bbfae;
 --fib-chinh:#2bbfae;--fib-5:#e8b400;--fib-phu:#77766f;
 --cc-fibo:#3987e5;--cc-ma:#9085e9;--cc-dinhday:#d95926;--cc-thanhly:#d55181;--cc-gap:#e66767;--cc-trend:#199e70;--cc-tron:#c9b94e;--cc-mohinh:#b08d57;--cc-khac:#8f8e86;
 --vt-dich:#3987e5;--vt-tp:#22b38e;--vt-ho_tro:#46ad46;--vt-khang_cu:#e0682f;--vt-entry:#9085e9;--vt-sl:#e66767;--vt-vo_hieu:#e07aa3;--vt-khac:#8f8e86;
 --tang:#3cbf7f;--giam:#ef6b6b;--cho:#d9a43a;
 --yk-bg:#2b2516;--yk-bd:#c98500;--pv-bg:#2a2214;
}
*{box-sizing:border-box}
html{scroll-padding-top:14px}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-text-size-adjust:100%}
a{color:var(--accent)}
.nut{font:inherit;font-size:14px;background:var(--surface-2);color:var(--text);border:1px solid var(--border);border-radius:8px;padding:5px 10px;cursor:pointer;line-height:1.3}
.nut:hover{border-color:var(--accent)}
.khung{display:grid;grid-template-columns:300px minmax(0,1fr);min-height:100vh}
.muc-luc{position:sticky;top:0;height:100vh;overflow:auto;background:var(--surface);border-right:1px solid var(--border);padding:16px 12px 48px;font-size:13.5px;line-height:1.4;overscroll-behavior:contain}
.ml-dau{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:0 4px 12px}
.ml-ten{font-weight:700;color:var(--text);text-decoration:none;font-size:15px}
.ml-ds{list-style:none;margin:0;padding:0}
.ml-ds a{display:block;padding:4px 8px;border-radius:6px;color:var(--text-2);text-decoration:none;border-left:2px solid transparent}
.ml-ds a:hover{background:var(--surface-2);color:var(--text)}
.ml-ds a.dang{background:var(--accent-soft);color:var(--text);border-left-color:var(--accent)}
.ml-1{margin-top:12px}.ml-1 a{font-weight:700;color:var(--text);font-size:12.5px;letter-spacing:.02em;text-transform:uppercase}
.ml-2 a{font-weight:600}
.ml-3 a{padding-left:20px;font-size:12.5px}
main{padding:28px 44px 90px;max-width:1040px;width:100%;margin:0 auto;min-width:0}
.thanh-tren{display:none}
.nen-mo{display:none}
@media (max-width:920px){
 .khung{grid-template-columns:1fr}
 .muc-luc{position:fixed;inset:0 auto 0 0;width:min(86vw,340px);z-index:60;transform:translateX(-104%);transition:transform .2s ease;box-shadow:0 0 40px rgba(0,0,0,.25)}
 body.mo-ml .muc-luc{transform:none}
 body.mo-ml .nen-mo{display:block;position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:55}
 .thanh-tren{display:flex;align-items:center;gap:10px;position:sticky;top:0;z-index:50;background:var(--surface);border-bottom:1px solid var(--border);padding:8px 16px}
 .tt-ten{flex:1;font-weight:650;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
 html{scroll-padding-top:60px}
 main{padding:16px 16px 70px}
}
.dau-trang{margin:6px 0 18px}
.tieu-chinh{font-size:2rem;line-height:1.2;margin:0;border:0;padding:0}
.tieu-phu{margin:4px 0 6px;font-size:1.1rem;color:var(--text-2)}
.meta{margin:0;font-size:13px;color:var(--muted)}
main h1{font-size:1.55rem;line-height:1.25;margin:60px 0 14px;padding-top:14px;border-top:3px solid var(--text)}
main h2{font-size:1.3rem;line-height:1.3;margin:44px 0 10px}
main h3{font-size:1.07rem;line-height:1.35;margin:30px 0 8px}
main p,main li{max-width:78ch}
main ul,main ol{padding-left:1.4em}
main li{margin:3px 0}
hr{border:0;border-top:1px solid var(--border);margin:36px 0}
blockquote{margin:14px 0;padding:6px 16px;border-left:3px solid var(--accent);background:var(--surface);border-radius:0 8px 8px 0;color:var(--text-2);font-size:15px}
blockquote p{margin:6px 0}
code{font:12.5px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--surface-2);padding:1px 5px;border-radius:4px;border:1px solid var(--border)}
strong{font-weight:650}
.ngay{font:11.5px/1.3 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--surface-2);color:var(--text-2);padding:0 4px;border-radius:4px;white-space:nowrap;border:1px solid var(--border)}
.ngay.co-buoi{cursor:pointer;color:var(--accent);border-color:color-mix(in srgb,var(--accent) 35%,var(--border))}
.ngay.co-buoi:hover{background:var(--accent-soft)}
.ykien{background:var(--yk-bg);border-left:3px solid var(--yk-bd);padding:4px 10px;border-radius:0 6px 6px 0}
li.ykien{list-style:none;margin-left:-1.1em}
.dau-yk{color:var(--yk-bd);font-weight:700}
.bang{overflow-x:auto;margin:14px 0 22px;border:1px solid var(--border);border-radius:10px;background:var(--surface);-webkit-overflow-scrolling:touch}
.bang table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.5}
.bang th,.bang td{padding:7px 10px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}
.bang tr:last-child td{border-bottom:0}
.bang th{background:var(--surface-2);font-weight:650;white-space:nowrap}
.bang td{min-width:72px}
.bang td:first-child{font-weight:500}
@media (min-width:700px){.bang table{min-width:640px}}
.nut-anh{font:11px/1.2 inherit;margin-left:4px;padding:1px 6px;border-radius:10px;border:1px solid var(--accent);background:var(--accent-soft);color:var(--accent);cursor:pointer}
/* ---- hình ---- */
.hinh{margin:26px 0 34px;padding:18px 18px 12px;background:var(--surface);border:1px solid var(--border);border-radius:14px;max-width:none}
.hinh-tieu{font-weight:700;font-size:1.05rem;margin:0 0 4px}
.hinh-tieu .so{color:var(--accent);margin-right:8px;font-size:.85rem;text-transform:uppercase;letter-spacing:.04em}
.hinh-mo-ta{color:var(--text-2);font-size:14px;margin:0 0 14px;max-width:none}
.hinh-nguon{color:var(--muted);font-size:12.5px;margin:12px 0 0;max-width:none}
.cj-khung{position:relative;width:100%}
.cao-360{height:360px}.cao-380{height:380px}.cao-440{height:440px}.cao-540{height:540px}
.lw-khung{position:relative;width:100%;border:1px solid var(--border);border-radius:8px;overflow:hidden}
@media (max-width:600px){.cao-440{height:360px}.cao-540{height:430px}.cao-360,.cao-380{height:320px}}
.lw-chu-giai{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12.5px;color:var(--text-2);margin:0 0 6px;min-height:20px}
.lw-chu-giai i{display:inline-block;width:14px;height:3px;border-radius:2px;vertical-align:middle;margin-right:5px}
.lw-chu-giai .gt{font-variant-numeric:tabular-nums;color:var(--text)}
.xem-bang{margin-top:10px;font-size:14px}.xem-bang summary{cursor:pointer;color:var(--accent)}
.cuon-ngang{overflow-x:auto;-webkit-overflow-scrolling:touch}
.svg-wrap{min-width:600px}
/* timeline */
.dong-tg{list-style:none;margin:0;padding:0;position:relative;max-width:none}
.dong-tg:before{content:"";position:absolute;left:17px;top:8px;bottom:8px;width:2px;background:var(--border)}
.buoc{display:flex;gap:14px;margin:0 0 14px;max-width:none;position:relative}
.buoc-so{flex:none;width:36px;height:36px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;position:relative;z-index:1;box-shadow:0 0 0 4px var(--surface)}
.buoc.truoc .buoc-so{background:var(--surface);color:var(--accent);border:2px dashed var(--accent)}
.buoc-nd{flex:1;min-width:0;padding-top:5px}
.buoc-tieu{font-weight:650}
.buoc-phu{font-size:14px;color:var(--text-2);margin-top:1px}
.nhan-phu{font-size:11.5px;font-weight:600;color:var(--accent);border:1px solid var(--accent);border-radius:10px;padding:0 7px;margin-left:4px;white-space:nowrap}
.tan-suat{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:12.5px;color:var(--muted);margin-top:4px}
.thuoc{position:relative;flex:none;width:120px;height:8px;border-radius:4px;background:var(--surface-2);border:1px solid var(--border);overflow:hidden}
.thuoc i{position:absolute;left:0;top:0;bottom:0;background:var(--accent);border-radius:4px}
.thuoc b{position:absolute;top:0;bottom:0;background:var(--accent);opacity:.4}
.thuoc-nhom{display:inline-flex;gap:2px;flex:none}
.thuoc-nhom i{font:9.5px/1 ui-monospace,Menlo,monospace;font-style:normal;padding:3px 2px;border-radius:3px;background:var(--surface-2);color:var(--muted);border:1px solid var(--border)}
.thuoc-nhom i.co{background:var(--accent);color:#fff;border-color:var(--accent)}
/* bản đồ công cụ */
.ban-do-cc{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
@media (max-width:1100px){.ban-do-cc{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.ban-do-cc{grid-template-columns:1fr}}
.cot-cc{background:var(--surface-2);border-radius:10px;padding:8px;border-top:4px solid var(--c)}
.cot-qd{--c:var(--accent)}.cot-bl{--c:var(--cho)}.cot-tk{--c:var(--tang)}.cot-kd{--c:var(--muted)}
.cot-dau{padding:2px 4px 8px}.cot-dau b{font-size:15px}.cot-dau small{display:block;color:var(--muted);font-size:12px;line-height:1.35}
.dem{font-size:12px;background:var(--c);color:#fff;border-radius:9px;padding:0 7px;margin-left:4px;font-weight:700}
.the{background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--c);border-radius:8px;padding:7px 9px;margin:0 0 7px;font-size:13px;line-height:1.4}
.the b{display:inline;font-size:13.5px}
.the-dung{display:block;color:var(--text-2);margin-top:2px}
.the-muc{display:block;color:var(--muted);font-size:12px;margin-top:3px}
.the-bo{font-size:11px;color:var(--giam);border:1px solid var(--giam);border-radius:8px;padding:0 6px;white-space:nowrap}
.the-kd{opacity:.9}.the-kd b{text-decoration:line-through;text-decoration-color:var(--muted)}
.the-kd small{display:block;color:var(--muted);font-size:11.5px}
.cot-trich{font-size:12.5px;color:var(--text-2);font-style:italic;margin:8px 4px 2px}
/* cây quyết định */
.cay{display:flex;flex-direction:column;align-items:center;font-size:14px}
.cay-hang{display:flex;justify-content:center;align-items:stretch;gap:10px;width:100%}
.nut-cay{background:var(--surface-2);border:1px solid var(--border);border-radius:10px;padding:9px 14px;text-align:center;max-width:620px;line-height:1.45}
.nut-cay small{display:block;color:var(--muted);font-size:12px;margin-top:2px}
.nut-dau{background:var(--accent);color:#fff;border-color:var(--accent)}.nut-dau small{color:rgba(255,255,255,.85)}
.nut-hoi{border:2px solid var(--accent)}
.t34{color:var(--ema34)}.t89{color:var(--ema89)}.t200{color:var(--ema200)}
.mui{position:relative;width:2px;height:26px;background:var(--muted);margin:0 auto}
.mui:after{content:"";position:absolute;bottom:-1px;left:-5px;border:6px solid transparent;border-top-color:var(--muted);border-bottom:0}
.mui span{position:absolute;left:10px;top:3px;font-size:12px;color:var(--muted);white-space:nowrap}
.cay-pv{align-items:center}
.nhanh-co{position:relative;width:56px;height:2px;background:var(--cho);flex:none}
.nhanh-co:after{content:"";position:absolute;right:-1px;top:-5px;border:6px solid transparent;border-left-color:var(--cho);border-right:0}
.nhanh-co span{position:absolute;top:-19px;left:14px;font-size:12px;color:var(--cho)}
.nut-pv{background:var(--pv-bg);border-color:var(--cho);text-align:left;max-width:360px;font-size:13px}
.nut-pv b{color:var(--cho)}
.nut-pv ul{margin:6px 0 0;padding-left:0;list-style:none}
.nut-pv li{margin:3px 0;max-width:none}
.nut-pv code{font-size:11px}
.re-ba{position:relative;width:68%;height:20px;border:2px solid var(--muted);border-bottom:0;border-radius:10px 10px 0 0;margin-top:10px}
.re-ba:before{content:"";position:absolute;left:50%;top:-12px;width:2px;height:10px;background:var(--muted)}
.re-ba i{display:none}
.cay-ba{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;width:100%}
.nhanh{background:var(--surface-2);border:1px solid var(--border);border-radius:10px;padding:10px;text-align:center;display:flex;flex-direction:column;align-items:center}
.mini-ema{width:120px;height:64px;margin-bottom:4px}
.mn-ema34{stroke:var(--ema34);stroke-width:2.5;fill:none}.mn-ema89{stroke:var(--ema89);stroke-width:2.5;fill:none}.mn-ema200{stroke:var(--ema200);stroke-width:2.5;fill:none}
.mn-nen{fill:var(--text-2)}.mn-rau{stroke:var(--text-2);stroke-width:1.2}
.dk{font-size:13px;color:var(--text-2);min-height:2.8em}
.ket{margin:6px 0 2px;font-weight:800;font-size:15px;letter-spacing:.02em;padding:4px 12px;border-radius:8px;color:#fff}
.ket-tang{background:var(--tang)}.ket-giam{background:var(--giam)}.ket-cho{background:var(--cho)}
.ket-phu{font-size:12px;color:var(--muted)}
.trich{font-size:12.5px;color:var(--text-2);font-style:italic;margin-top:6px;max-width:560px;text-align:center}
.trich q{quotes:"“" "”"}
.cay-ct{align-items:center;margin-top:8px;flex-wrap:wrap}
.nut-nho{font-size:13px;max-width:280px}
.nut-dam{border:2px solid var(--tang)}
.mui-ngang{position:relative;width:40px;height:2px;background:var(--muted);flex:none}
.mui-ngang:after{content:"";position:absolute;right:-1px;top:-5px;border:6px solid transparent;border-left-color:var(--muted);border-right:0}
.trich-giua{margin:4px 0 0}
.nut-loc{border:1px dashed var(--cho);max-width:760px}
.ds-loc{display:flex;flex-wrap:wrap;gap:5px;justify-content:center;margin-top:8px}
.chip-loc{font-size:12px;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:2px 8px}
.chip-loc code{font-size:10.5px;padding:0 3px}
@media (max-width:700px){
 .cay-pv{flex-direction:column;align-items:center}.nhanh-co{width:2px;height:22px}.nhanh-co:after{right:-5px;top:auto;bottom:-1px;border:6px solid transparent;border-top-color:var(--cho);border-bottom:0}.nhanh-co span{left:8px;top:2px}
 .cay-ba{grid-template-columns:1fr}.re-ba{display:none}
 .cay-ct{flex-direction:column}.mui-ngang{width:2px;height:20px}.mui-ngang:after{right:-5px;top:auto;bottom:-1px;border:6px solid transparent;border-top-color:var(--muted);border-bottom:0}
}
/* hội tụ */
.tabs-ht{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.tab-ht{font:inherit;font-size:13px;background:var(--surface-2);color:var(--text);border:1px solid var(--border);border-radius:8px;padding:5px 10px;cursor:pointer}
.tab-ht.dang{border-color:var(--accent);box-shadow:inset 0 -2px 0 var(--accent)}
.tab-ht span{font-size:11.5px;margin-left:4px}
.huy-dat{color:var(--tang)}.huy-truot{color:var(--giam)}.huy-pha{color:var(--cho)}
.chu-giai-cc{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:12px;color:var(--text-2);margin:4px 0 8px}
.chu-giai-cc i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:4px;background:var(--c)}
.cc-fibo{--c:var(--cc-fibo)}.cc-ma{--c:var(--cc-ma)}.cc-dinhday{--c:var(--cc-dinhday)}.cc-thanhly{--c:var(--cc-thanhly)}.cc-gap{--c:var(--cc-gap)}
.cc-trend{--c:var(--cc-trend)}.cc-tron{--c:var(--cc-tron)}.cc-mohinh{--c:var(--cc-mohinh)}.cc-khac{--c:var(--cc-khac)}
.svg-hoi-tu{width:100%;height:auto;display:block;font-family:inherit}
.ht-luoi{stroke:var(--grid);stroke-width:1}.ht-day{stroke:var(--border)}
.ht-truc{fill:var(--muted);font-size:11px}
.ht-tang{fill:var(--up);stroke:var(--up)}.ht-giam{fill:var(--down);stroke:var(--down)}.ht-rau{stroke-width:1}
.ht-neu{stroke:var(--accent);stroke-dasharray:4 3;stroke-width:1.5}.ht-neu-chu{fill:var(--accent);font-size:11px;font-weight:600}
.ht-vung{fill:var(--muted);opacity:.14}.ht-vung-duong{stroke:var(--muted);stroke-dasharray:3 3}.ht-vung-chu{fill:var(--text-2);font-size:11px}
.ht-muc{stroke:var(--text);stroke-width:1.5;opacity:.75}.ht-muc-3,.ht-muc-4{stroke-width:2.5;opacity:1}
.ht-muc-vung{fill:var(--text);stroke:none;opacity:.12}.ht-muc-vung.ht-muc-3,.ht-muc-vung.ht-muc-4{opacity:.2}
.ht-noi{fill:none;stroke:var(--muted);stroke-width:1}
.ht-gia{fill:var(--text);font-size:12.5px;font-weight:700}.ht-dem{fill:var(--muted);font-size:11px;font-weight:500}
.ht-chip rect{fill:var(--surface-2);stroke:var(--c);stroke-width:1}
.ht-chip circle{fill:var(--c)}
.ht-chip text{fill:var(--text);font-size:11px}
.ht-tom{font-size:14px;margin:4px 0 8px}.ht-ghi{font-size:13px;color:var(--text-2);margin:6px 0 0}.ht-kq{font-size:13.5px;margin:6px 0 0}
.ht-kq b{color:var(--text)}
/* mốc giá */
.moc-dk{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:flex-end;margin-bottom:8px}
.chon-buoi{display:flex;flex-direction:column;gap:3px;font-size:12.5px;color:var(--muted);flex:1 1 340px;min-width:0}
.chon-buoi select{font:inherit;font-size:14px;color:var(--text);background:var(--surface-2);border:1px solid var(--border);border-radius:8px;padding:6px 8px;width:100%}
.nut-mau{display:flex;flex-wrap:wrap;gap:5px}
.nut-mau button{font:inherit;font-size:12.5px;background:var(--surface-2);color:var(--text);border:1px solid var(--border);border-radius:14px;padding:3px 10px;cursor:pointer}
.nut-mau button.dang{border-color:var(--accent);background:var(--accent-soft)}
.moc-dk2{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;margin-bottom:6px}
.cg-vai{display:flex;flex-wrap:wrap;gap:5px}
.cg-vai button{font:inherit;font-size:12px;background:var(--surface);color:var(--text);border:1px solid var(--border);border-radius:12px;padding:2px 9px;cursor:pointer}
.cg-vai button i{display:inline-block;width:12px;height:3px;border-radius:2px;vertical-align:middle;margin-right:5px}
.cg-vai button.tat{opacity:.4;text-decoration:line-through}
.o-chon{font-size:13px;color:var(--text-2);display:inline-flex;align-items:center;gap:5px;cursor:pointer}
.moc-tom{font-size:13.5px;color:var(--text-2);margin:8px 0 4px;max-width:none}
.bang-moc{max-height:440px;overflow:auto}
.bang-moc table{font-size:13px}
.bang-moc th{position:sticky;top:0;z-index:1}
.bang-moc tr{cursor:pointer}
.bang-moc tr:hover td{background:var(--surface-2)}
.bang-moc tr.chon td{background:var(--accent-soft)}
.bang-moc .vai{white-space:nowrap;font-weight:600}
.bang-moc .vai i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.bang-moc .so{font-variant-numeric:tabular-nums;white-space:nowrap}
.bang-moc .trich-o{color:var(--text-2);font-style:italic;min-width:220px}
.bang-moc .cham{color:var(--tang);white-space:nowrap}.bang-moc .chua{color:var(--muted)}
.khong-chac{font-size:11px;color:var(--cho);border:1px solid var(--cho);border-radius:6px;padding:0 4px;margin-left:3px}
/* ảnh */
.loc-anh{margin-bottom:6px}
.nhom-anh h4{margin:18px 0 8px;font-size:14.5px;line-height:1.4}
.nhom-anh h4 small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.na-ngay{display:inline-block;background:var(--accent);color:#fff;border-radius:6px;padding:0 6px;font-size:12.5px;margin-right:4px}
.luoi-anh{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.o-anh{display:flex;flex-direction:column;padding:0;border:1px solid var(--border);background:var(--surface-2);border-radius:8px;overflow:hidden;cursor:zoom-in;text-align:left;font:inherit;color:inherit;position:relative}
.o-anh:hover{border-color:var(--accent)}
.o-anh img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:var(--grid)}
.oa-gio{position:absolute;top:4px;left:4px;font:11px/1.2 ui-monospace,Menlo,monospace;background:rgba(0,0,0,.65);color:#fff;padding:1px 5px;border-radius:4px}
.oa-cap{font-size:11.5px;line-height:1.35;padding:5px 7px;color:var(--text-2);min-height:2.2em}
.o-anh.co-ghi{border-color:color-mix(in srgb,var(--accent) 40%,var(--border))}
body.chi-ghi .o-anh:not(.co-ghi),body.chi-ghi .nhom-anh.chua-ghi{display:none}
.lb{position:fixed;inset:0;z-index:100;background:rgba(10,10,10,.94);display:flex;flex-direction:column;color:#eee}
.lb[hidden]{display:none}
.lb-tren{display:flex;align-items:center;gap:12px;padding:8px 14px;font-size:13px}
.lb-tren #lb-tieu{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#bbb}
.lb .nut{background:#2a2a2a;color:#eee;border-color:#444}
.lb-giua{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;gap:8px;padding:0 8px}
.lb-giua img{max-width:calc(100% - 100px);max-height:100%;object-fit:contain;border-radius:4px;background:#000}
.lb-nut{font-size:26px;width:42px;height:60px;padding:0;flex:none}
.lb-cap{max-height:30vh;overflow:auto;padding:8px 18px 14px;font-size:13.5px;line-height:1.5;color:#ddd;border-top:1px solid #333}
.lb-cap p{margin:4px 0;max-width:none}.lb-cap code{background:#333;border-color:#444;color:#eee}.lb-cap .ngay{background:#333;color:#ccc;border-color:#444}
@media (max-width:600px){.lb-giua img{max-width:100%}.lb-nut{position:absolute;top:45%;z-index:2;background:rgba(40,40,40,.7)}#lb-truoc{left:4px}#lb-sau{right:4px}}
.chan{margin-top:60px;padding-top:14px;border-top:1px solid var(--border);font-size:12.5px;color:var(--muted)}
.loi-hinh{color:var(--giam);font-size:13px}
"""

JS = r"""
(function(){
'use strict';
var D=JSON.parse(document.getElementById('du-lieu').textContent);
var VE_LAI=[];
function cv(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim();}
function docMau(){var v={},vt=['dich','tp','ho_tro','khang_cu','entry','sl','vo_hieu','khac'],cc=['fibo','ma','dinhday','thanhly','gap','trend','tron','mohinh','khac'];
  vt.forEach(function(k){v[k]=cv('--vt-'+k);});var c={};cc.forEach(function(k){c[k]=cv('--cc-'+k);});
  return {surface:cv('--surface'),surface2:cv('--surface-2'),text:cv('--text'),text2:cv('--text-2'),muted:cv('--muted'),border:cv('--border'),grid:cv('--grid'),
   accent:cv('--accent'),up:cv('--up'),down:cv('--down'),ema34:cv('--ema34'),dai:cv('--ema34-dai'),mep:cv('--ema34-mep'),ema89:cv('--ema89'),ema200:cv('--ema200'),ema610:cv('--ema610'),
   fibChinh:cv('--fib-chinh'),fib5:cv('--fib-5'),fibPhu:cv('--fib-phu'),vai:v,cc:c};}
var MAU=docMau();
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function fmtGia(p){return Math.round(p).toLocaleString('vi-VN');}
function pad(n){return (n<10?'0':'')+n;}
function fmtTG(t){var d=new Date(t*1000);return pad(d.getUTCDate())+'/'+pad(d.getUTCMonth()+1)+' '+pad(d.getUTCHours())+':'+pad(d.getUTCMinutes());}
var FONT='-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';

/* ---------- giao diện sáng / tối ---------- */
var KEY='sotay-theme';
function layTheme(){try{return localStorage.getItem(KEY)||'auto';}catch(e){return 'auto';}}
var NHAN_THEME={auto:'◐ Tự động',light:'☀ Sáng',dark:'☾ Tối'};
function capNhatNut(v){document.querySelectorAll('.nut-theme').forEach(function(b){b.textContent=NHAN_THEME[v];b.title='Giao diện: '+NHAN_THEME[v]+' (bấm để đổi)';});}
function datTheme(v){if(v==='auto')document.documentElement.removeAttribute('data-theme');else document.documentElement.setAttribute('data-theme',v);
  try{localStorage.setItem(KEY,v);}catch(e){} capNhatNut(v); veLai();}
function veLai(){MAU=docMau();VE_LAI.forEach(function(f){try{f();}catch(e){console.error(e);}});}
capNhatNut(layTheme());
document.querySelectorAll('.nut-theme').forEach(function(b){b.addEventListener('click',function(){var o=['auto','light','dark'];datTheme(o[(o.indexOf(layTheme())+1)%3]);});});
try{matchMedia('(prefers-color-scheme: dark)').addEventListener('change',function(){if(layTheme()==='auto')veLai();});}catch(e){}

/* ---------- mục lục ---------- */
var nav=document.getElementById('muc-luc');
document.getElementById('nut-ml').addEventListener('click',function(){document.body.classList.toggle('mo-ml');});
document.getElementById('nen-mo').addEventListener('click',function(){document.body.classList.remove('mo-ml');});
nav.addEventListener('click',function(e){if(e.target.closest('a'))document.body.classList.remove('mo-ml');});
var links=[].slice.call(nav.querySelectorAll('a[href^="#"]')),linkMap={};links.forEach(function(a){linkMap[decodeURIComponent(a.getAttribute('href').slice(1))]=a;});
var heads=[].slice.call(document.querySelectorAll('main h1[id],main h2[id],main h3[id]'));
var cur=null,cho=false;
function capNhatML(){cho=false;var best=null;for(var i=0;i<heads.length;i++){if(heads[i].getBoundingClientRect().top<130)best=heads[i];else break;}
  if(best===cur)return;cur=best;links.forEach(function(a){a.classList.remove('dang');});if(!best)return;var a=linkMap[best.id];if(!a)return;a.classList.add('dang');
  var r=a.getBoundingClientRect(),nr=nav.getBoundingClientRect();if(r.top<nr.top+50||r.bottom>nr.bottom-30)nav.scrollTop+=(r.top-nr.top)-nr.height/3;}
addEventListener('scroll',function(){if(!cho){cho=true;requestAnimationFrame(capNhatML);}},{passive:true});capNhatML();

/* ---------- lightbox ---------- */
var ANH=D.anh||[],lb=document.getElementById('lb'),lbI=-1;
function moAnh(i){if(!ANH.length)return;lbI=(i+ANH.length)%ANH.length;var a=ANH[lbI];
  document.getElementById('lb-anh').src=a.src;document.getElementById('lb-anh').alt='Ảnh '+a.ten;
  document.getElementById('lb-dem').textContent=(lbI+1)+' / '+ANH.length;
  document.getElementById('lb-tieu').textContent=(a.ngay?a.ngay.slice(8,10)+'/'+a.ngay.slice(5,7)+' · ':'')+'phút '+a.gio+' · '+(a.td||a.ten);
  document.getElementById('lb-cap').innerHTML=a.cap||'<p><i>Chưa có ghi chú cho ảnh này.</i></p>';
  if(lb.hidden){lb.hidden=false;document.body.style.overflow='hidden';}}
function dongAnh(){lb.hidden=true;document.body.style.overflow='';lbI=-1;}
document.addEventListener('click',function(e){var b=e.target.closest('.o-anh,.nut-anh');if(b){e.preventDefault();moAnh(+b.dataset.i);}});
document.getElementById('lb-dong').onclick=dongAnh;document.getElementById('lb-truoc').onclick=function(){moAnh(lbI-1);};document.getElementById('lb-sau').onclick=function(){moAnh(lbI+1);};
lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('lb-giua'))dongAnh();});
document.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')dongAnh();else if(e.key==='ArrowLeft')moAnh(lbI-1);else if(e.key==='ArrowRight')moAnh(lbI+1);});
var tx=null;lb.addEventListener('touchstart',function(e){tx=e.touches[0].clientX;},{passive:true});
lb.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)moAnh(lbI+(dx<0?1:-1));tx=null;});
var chk=document.getElementById('chi-co-ghi');if(chk)chk.addEventListener('change',function(){document.body.classList.toggle('chi-ghi',chk.checked);});

/* ---------- tab hội tụ ---------- */
document.querySelectorAll('.tabs-ht').forEach(function(t){var fig=t.closest('figure');t.addEventListener('click',function(e){var b=e.target.closest('.tab-ht');if(!b)return;
  t.querySelectorAll('.tab-ht').forEach(function(x){x.classList.toggle('dang',x===b);});
  fig.querySelectorAll('.pane-ht').forEach(function(p){p.hidden=p.dataset.i!==b.dataset.i;});});});

/* ---------- lightweight-charts: tiện ích ---------- */
var LW=window.LightweightCharts;
function tickFmt(time,type){var d=new Date(time*1000);if(type===0)return String(d.getUTCFullYear());if(type===1)return 'Th'+(d.getUTCMonth()+1);
  if(type===2)return pad(d.getUTCDate())+'/'+pad(d.getUTCMonth()+1);return pad(d.getUTCHours())+':'+pad(d.getUTCMinutes());}
function tuyChonLW(){var M=MAU;return {layout:{background:{type:'solid',color:M.surface},textColor:M.text2,fontFamily:FONT,fontSize:11,attributionLogo:false},
  grid:{vertLines:{color:M.grid},horzLines:{color:M.grid}},rightPriceScale:{borderColor:M.border},timeScale:{borderColor:M.border}};}
function taoLW(el,them){var o=tuyChonLW();o.autoSize=true;o.crosshair={mode:LW.CrosshairMode.Normal};
  o.timeScale.timeVisible=true;o.timeScale.secondsVisible=false;o.timeScale.tickMarkFormatter=tickFmt;o.timeScale.rightOffset=4;
  o.localization={locale:'vi-VN',priceFormatter:fmtGia,timeFormatter:fmtTG};o.handleScroll={vertTouchDrag:false};o.rightPriceScale.scaleMargins={top:0.06,bottom:0.06};
  if(them){for(var k in them){o[k]=Object.assign(o[k]||{},them[k]);}}
  return LW.createChart(el,o);}
function mauNen(){var M=MAU;return {upColor:M.up,downColor:M.down,wickUpColor:M.up,wickDownColor:M.down,borderVisible:false,priceLineVisible:false};}
function duongOpt(c,w,style){return {color:c,lineWidth:w||2,lineStyle:style||0,priceLineVisible:false,lastValueVisible:false,crosshairMarkerVisible:false};}
/* primitive vẽ tự do trên pane */
function LopVe(fn,z){var self=this;this._fn=fn;this._z=z||'normal';
  this._view={zOrder:function(){return self._z;},renderer:function(){return {draw:function(target){target.useMediaCoordinateSpace(function(sc){if(self._chart)self._fn(sc.context,sc.mediaSize,self._chart,self._series);});}};}};}
LopVe.prototype.attached=function(p){this._chart=p.chart;this._series=p.series;this._req=p.requestUpdate;};
LopVe.prototype.detached=function(){this._chart=null;};
LopVe.prototype.paneViews=function(){return [this._view];};
LopVe.prototype.autoscaleInfo=function(){return this.tuDong?this.tuDong():null;};
LopVe.prototype.updateAllViews=function(){};
LopVe.prototype.capNhat=function(){if(this._req)this._req();};
function veDai(ctx,ch,se,pts,mau){var ts=ch.timeScale(),tr=[],du=[];
  for(var i=0;i<pts.length;i++){var p=pts[i];if(p.u==null||p.l==null)continue;var x=ts.timeToCoordinate(p.t);if(x===null)continue;
    var yu=se.priceToCoordinate(p.u),yl=se.priceToCoordinate(p.l);if(yu===null||yl===null)continue;tr.push([x,yu]);du.push([x,yl]);}
  if(tr.length<2)return;ctx.beginPath();ctx.moveTo(tr[0][0],tr[0][1]);for(i=1;i<tr.length;i++)ctx.lineTo(tr[i][0],tr[i][1]);
  for(i=du.length-1;i>=0;i--)ctx.lineTo(du[i][0],du[i][1]);ctx.closePath();ctx.fillStyle=mau;ctx.fill();}
function cat(N,a,b){var r={nen:[],e34h:[],e34l:[],e34c:[],e89:[],e200:[],e610:[],dai:[]};
  for(var i=a;i<b;i++){var t=N.t[i];r.nen.push({time:t,open:N.o[i],high:N.h[i],low:N.l[i],close:N.c[i]});
    if(N.e34h[i]!=null)r.e34h.push({time:t,value:N.e34h[i]});if(N.e34l[i]!=null)r.e34l.push({time:t,value:N.e34l[i]});
    if(N.e34c[i]!=null)r.e34c.push({time:t,value:N.e34c[i]});if(N.e89[i]!=null)r.e89.push({time:t,value:N.e89[i]});
    if(N.e200[i]!=null)r.e200.push({time:t,value:N.e200[i]});if(N.e610[i]!=null)r.e610.push({time:t,value:N.e610[i]});
    r.dai.push({t:t,u:N.e34h[i],l:N.e34l[i]});}
  return r;}
function boEMA(chart){var M=MAU;return {h:chart.addLineSeries(duongOpt(M.mep,1)),l:chart.addLineSeries(duongOpt(M.mep,1)),c:chart.addLineSeries(duongOpt(M.ema34,2)),
  e89:chart.addLineSeries(duongOpt(M.ema89,2)),e200:chart.addLineSeries(duongOpt(M.ema200,2)),e610:chart.addLineSeries(duongOpt(M.ema610,1))};}
function datEMA(b,r){b.h.setData(r.e34h);b.l.setData(r.e34l);b.c.setData(r.e34c);b.e89.setData(r.e89);b.e200.setData(r.e200);b.e610.setData(r.e610);}
function mauEMA(b){var M=MAU;b.h.applyOptions({color:M.mep});b.l.applyOptions({color:M.mep});b.c.applyOptions({color:M.ema34});b.e89.applyOptions({color:M.ema89});b.e200.applyOptions({color:M.ema200});b.e610.applyOptions({color:M.ema610});}
function chuGiaiEMA(el,se,b,them){function o(c,t,v){return '<span><i style="background:'+c+'"></i>'+t+(v!=null?' <span class="gt">'+fmtGia(v)+'</span>':'')+'</span>';}
  function ve(p){var M=MAU,d=p&&p.seriesData?p.seriesData:null;function g(s){var x=d&&d.get(s);return x?(x.value!=null?x.value:x.close):null;}
    var n=d&&d.get(se);var h=(n?'<span>'+fmtTG(p.time)+' · O <span class="gt">'+fmtGia(n.open)+'</span> H <span class="gt">'+fmtGia(n.high)+'</span> L <span class="gt">'+fmtGia(n.low)+'</span> C <span class="gt">'+fmtGia(n.close)+'</span></span>':'');
    el.innerHTML=h+o(M.ema34,'EMA34 + dải',g(b.c))+o(M.ema89,'EMA89',g(b.e89))+o(M.ema200,'EMA200',g(b.e200))+o(M.ema610,'EMA610',g(b.e610))+(them?them():'');}
  return ve;}

/* ---------- HÌNH: Sonic R ---------- */
function hinhSonic(){var el=document.getElementById('lw-sonic');if(!el||!D.nen||!D.sonic)return;if(!LW){el.innerHTML='<p class="loi-hinh">Thiếu vendor/lightweight-charts…js</p>';return;}
  var N=D.nen,S=D.sonic,n=N.t.length,a=Math.max(0,n-S.so_nen),r=cat(N,a,n);
  var chart=taoLW(el),se=chart.addCandlestickSeries(mauNen()),b=boEMA(chart);se.setData(r.nen);datEMA(b,r);
  var dai=new LopVe(function(ctx,size,ch,s){veDai(ctx,ch,s,r.dai,MAU.dai);},'bottom');se.attachPrimitive(dai);
  var fib=new LopVe(function(ctx,size,ch,s){var M=MAU,ts=ch.timeScale(),xa=ts.timeToCoordinate(S.dau.t),xb=ts.timeToCoordinate(S.cuoi.t);if(xa===null)return;
    var x0=Math.min(xa,xb==null?xa:xb),W=size.width;ctx.save();ctx.font='11px '+FONT;
    var y5=s.priceToCoordinate(S.muc[3].gia),y6=s.priceToCoordinate(S.muc[4].gia);
    if(y5!=null&&y6!=null){ctx.globalAlpha=0.08;ctx.fillStyle=M.fibChinh;ctx.fillRect(x0,Math.min(y5,y6),W-x0,Math.abs(y6-y5));ctx.globalAlpha=1;}
    S.muc.forEach(function(m){var y=s.priceToCoordinate(m.gia);if(y==null)return;var chinh=(m.r===0.382||m.r===0.5||m.r===0.618);
      var c=m.r===0.5?M.fib5:(chinh?M.fibChinh:M.fibPhu);ctx.strokeStyle=c;ctx.lineWidth=chinh?1.5:1;ctx.setLineDash(chinh?[]:[4,4]);
      ctx.beginPath();ctx.moveTo(x0,y);ctx.lineTo(W,y);ctx.stroke();
      var t=(m.r===0||m.r===1?String(m.r):m.r.toFixed(3).replace(/0+$/,''))+'  '+fmtGia(m.gia);ctx.fillStyle=chinh?M.text:M.muted;ctx.font=(chinh?'600 ':'')+'11px '+FONT;
      var w=ctx.measureText(t).width;ctx.globalAlpha=0.85;ctx.fillStyle=M.surface;ctx.fillRect(x0+3,y-15,w+8,14);ctx.globalAlpha=1;ctx.fillStyle=chinh?c:M.muted;ctx.fillText(t,x0+7,y-4);});
    if(xb!=null){ctx.setLineDash([3,3]);ctx.strokeStyle=M.muted;ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(xa,s.priceToCoordinate(S.dau.p));ctx.lineTo(xb,s.priceToCoordinate(S.cuoi.p));ctx.stroke();}
    ctx.restore();},'top');se.attachPrimitive(fib);
  var cg=chuGiaiEMA(document.getElementById('cg-sonic'),se,b,function(){return '<span><i style="background:'+MAU.fibChinh+'"></i>Fibo 0.382/0.618</span><span><i style="background:'+MAU.fib5+'"></i>Fibo 0.5</span>';});
  chart.subscribeCrosshairMove(cg);cg(null);chart.timeScale().fitContent();
  VE_LAI.push(function(){chart.applyOptions(tuyChonLW());se.applyOptions(mauNen());mauEMA(b);cg(null);dai.capNhat();fib.capNhat();});}

/* ---------- HÌNH: mốc giá trên chart thật ---------- */
var VAI={dich:['Đích','dich'],tp:['TP','tp'],ho_tro:['Hỗ trợ','ho_tro'],day_cu:['Đáy cũ','ho_tro'],khang_cu:['Kháng cự','khang_cu'],dinh_cu:['Đỉnh cũ','khang_cu'],
  entry:['Entry','entry'],sl:['SL','sl'],vo_hieu:['Mốc sai','vo_hieu'],nhac_lai:['Nhắc lại','khac'],khac:['Khác','khac']};
var NHOM=[['dich','Đích'],['tp','TP'],['entry','Entry'],['ho_tro','Hỗ trợ / đáy cũ'],['khang_cu','Kháng cự / đỉnh cũ'],['sl','SL'],['vo_hieu','Mốc sai (view fail)'],['khac','Khác']];
function vaiCua(v){return VAI[v]||[v,'khac'];}
function timNen(N,t){var lo=0,hi=N.t.length-1,r=-1;while(lo<=hi){var m=(lo+hi)>>1;if(N.t[m]<=t){r=m;lo=m+1;}else hi=m-1;}return r;}
function luc(b){var y=+b.ngay.slice(0,4),mo=+b.ngay.slice(5,7),d=+b.ngay.slice(8,10),g=b.gio||'1000';return Date.UTC(y,mo-1,d,+g.slice(0,2),+g.slice(2,4))/1000;}
function giay(s){if(!s)return 1800;var p=s.split(':').map(Number);return p.length===3?p[0]*3600+p[1]*60+p[2]:p[0]*60+(p[1]||0);}
function sauDo(N,it){var lo=Math.min(it.gia,it.tren==null?it.gia:it.tren),hi=Math.max(it.gia,it.tren==null?it.gia:it.tren),end=it.luc+5*86400,i=timNen(N,it.luc);
  if(i<0)return {txt:'—',cls:'chua'};var gan=Infinity;
  for(var k=i;k<N.t.length&&N.t[k]<=end;k++){if(N.l[k]<=hi&&N.h[k]>=lo){if(k===i)return {txt:'chạm ngay (nến đang chạy)',cls:'cham'};
      var g=(N.t[k]+7200-it.luc)/3600;return {txt:'chạm sau ~'+(g<48?Math.round(g)+' giờ':(g/24).toFixed(1).replace('.',',')+' ngày'),cls:'cham'};}
    var d=N.l[k]>hi?(N.l[k]-hi)/hi:(lo-N.h[k])/lo;if(d<gan)gan=d;}
  var thieu=N.t[N.t.length-1]+14400<end;return {txt:'chưa chạm'+(isFinite(gan)?' · gần nhất cách '+(gan*100).toFixed(1).replace('.',',')+'%':'')+(thieu?' · dữ liệu chưa đủ 5 ngày':''),cls:'chua'};}
function hinhMoc(){var el=document.getElementById('lw-moc'),sel=document.getElementById('chon-buoi');if(!el||!sel||!D.nen||!D.buoi||!D.buoi.length)return;
  if(!LW){el.innerHTML='<p class="loi-hinh">Thiếu vendor/lightweight-charts…js</p>';return;}
  var N=D.nen,B=D.buoi,st={items:[],an:{},chon:-1,live:0,tCuoi:0,ema:true},r=null;
  var chart=taoLW(el,{timeScale:{rightOffset:0}}),se=chart.addCandlestickSeries(mauNen()),b=boEMA(chart);
  var dai=new LopVe(function(ctx,size,ch,s){if(st.ema&&r)veDai(ctx,ch,s,r.dai,MAU.dai);},'bottom');se.attachPrimitive(dai);
  var lop=new LopVe(function(ctx,size,ch,s){veMoc(ctx,size,ch,s);},'top');lop.tuDong=function(){return st.auto?{priceRange:st.auto}:null;};se.attachPrimitive(lop);
  b.e610.applyOptions({autoscaleInfoProvider:function(){return null;}});
  function xCua(ts,t){var i=timNen(N,t);if(i<0)return null;var x=ts.timeToCoordinate(N.t[i]);if(x===null)return null;var x2=i+1<N.t.length?ts.timeToCoordinate(N.t[i+1]):null;
    var sp=x2!==null?x2-x:6;return x-sp/2+(t-N.t[i])/14400*sp;}
  function veMoc(ctx,size,ch,s){if(!st.items.length)return;var M=MAU,ts=ch.timeScale(),W=size.width,H=size.height;
    var xL=xCua(ts,st.live);if(xL===null)xL=0;var xE=ts.timeToCoordinate(st.tCuoi);if(xE===null)xE=W*0.7;
    var hep=W<560,lx=hep?Math.max(xE+8,W-118):Math.min(W-170,Math.max(xE+16,W*0.5)),maxW=W-lx-4;
    ctx.save();ctx.setLineDash([5,4]);ctx.strokeStyle=M.accent;ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(xL,0);ctx.lineTo(xL,H);ctx.stroke();ctx.setLineDash([]);
    ctx.font='600 11px '+FONT;ctx.fillStyle=M.accent;var g=st.gioLive;ctx.fillText('Live '+g,Math.min(xL+4,W-60),12);
    var lab=[];
    st.items.forEach(function(it){if(st.an[it.nhom])return;var y=s.priceToCoordinate(it.gia),y2=it.tren!=null?s.priceToCoordinate(it.tren):null;if(y===null)return;
      var c=M.vai[it.nhom]||M.muted,sl=st.chon===it.k;
      if(y2!==null){ctx.globalAlpha=sl?0.3:0.12;ctx.fillStyle=c;ctx.fillRect(xL,Math.min(y,y2),lx-4-xL,Math.abs(y2-y));}
      ctx.globalAlpha=sl?0.6:0.3;ctx.strokeStyle=c;ctx.lineWidth=1;ctx.setLineDash([2,4]);ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(xL,y);ctx.stroke();
      ctx.globalAlpha=sl?1:0.92;ctx.lineWidth=sl?3:1.6;ctx.setLineDash(it.nhom==='vo_hieu'||it.nhom==='sl'?[6,4]:[]);
      ctx.beginPath();ctx.moveTo(xL,y);ctx.lineTo(lx-4,y);if(y2!==null){ctx.moveTo(xL,y2);ctx.lineTo(lx-4,y2);}ctx.stroke();ctx.globalAlpha=1;ctx.setLineDash([]);
      var yc=y2!==null?(y+y2)/2:y;lab.push({it:it,y0:yc,y:Math.max(9,Math.min(H-9,yc)),c:c,ngoai:yc<0?'▲ ':(yc>H?'▼ ':'')});});
    lab.sort(function(a,b){return a.y-b.y;});var GAP=Math.max(11,Math.min(15,(H-18)/Math.max(1,lab.length)));
    for(var i=1;i<lab.length;i++)if(lab[i].y<lab[i-1].y+GAP)lab[i].y=lab[i-1].y+GAP;
    for(i=lab.length-1;i>=0;i--){var mx=i===lab.length-1?H-8:lab[i+1].y-GAP;if(lab[i].y>mx)lab[i].y=mx;}
    var fs=GAP<13||hep?10:11;
    lab.forEach(function(L){var it=L.it,sl=st.chon===it.k;ctx.font=(sl?'700 ':'600 ')+fs+'px '+FONT;
      var dau=L.ngoai+fmtGia(it.gia)+(it.tren!=null?'–'+fmtGia(it.tren):'')+' '+it.ten;
      while(dau.length>6&&ctx.measureText(dau).width>maxW-10)dau=dau.slice(0,-2)+'…';var w1=ctx.measureText(dau).width;
      ctx.font=(sl?'600 ':'')+fs+'px '+FONT;var cc=it.cc&&!hep?' · '+it.cc:'';var con=maxW-12-w1;var t2=cc;
      if(ctx.measureText(t2).width>con){while(t2.length>4&&ctx.measureText(t2+'…').width>con)t2=t2.slice(0,-1);t2=t2.length>4?t2+'…':'';}
      var w=w1+ctx.measureText(t2).width+12;
      ctx.strokeStyle=L.c;ctx.globalAlpha=0.7;ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(lx-4,Math.max(0,Math.min(H,L.y0)));ctx.lineTo(lx,L.y);ctx.stroke();ctx.globalAlpha=1;
      ctx.fillStyle=M.surface;ctx.globalAlpha=sl?0.98:0.88;ctx.fillRect(lx,L.y-GAP/2+1,w,GAP-2);ctx.globalAlpha=1;
      ctx.fillStyle=L.c;ctx.fillRect(lx,L.y-GAP/2+1,3,GAP-2);if(sl){ctx.strokeStyle=L.c;ctx.strokeRect(lx+0.5,L.y-GAP/2+1.5,w-1,GAP-3);}
      ctx.fillStyle=M.text;ctx.font=(sl?'700 ':'600 ')+fs+'px '+FONT;ctx.fillText(dau,lx+6,L.y+fs/2-1.5);
      ctx.fillStyle=M.text2;ctx.font=(sl?'600 ':'')+fs+'px '+FONT;ctx.fillText(t2,lx+6+w1,L.y+fs/2-1.5);});
    ctx.restore();}
  /* dropdown */
  var thang=null,og=null;B.forEach(function(x,i){var th=x.ngay.slice(5,7);if(th!==thang){thang=th;og=document.createElement('optgroup');og.label='Tháng '+(+th);sel.appendChild(og);}
    var o=document.createElement('option');o.value=i;var td=(x.td||'').replace(/\s*\|\s*Phân tích Bitcoin Live.*/i,'');
    o.textContent=x.ngay.slice(8,10)+'/'+th+' '+x.gio.slice(0,2)+':'+x.gio.slice(2)+' · '+x.m.length+' mốc'+(td?' · '+td:'');og.appendChild(o);});
  var mauEl=document.getElementById('nut-mau'),idx={};B.forEach(function(x,i){idx[x.id]=i;});
  (D.mau||[]).forEach(function(m){if(idx[m.id]==null)return;var bt=document.createElement('button');bt.textContent=m.nhan;bt.title=m.ghi;bt.dataset.i=idx[m.id];mauEl.appendChild(bt);});
  mauEl.addEventListener('click',function(e){var bt=e.target.closest('button');if(bt)chon(+bt.dataset.i);});
  sel.addEventListener('change',function(){chon(+sel.value);});
  var cgv=document.getElementById('cg-vai');
  function veCG(){var M=MAU,dem={};st.items.forEach(function(it){dem[it.nhom]=(dem[it.nhom]||0)+1;});
    cgv.innerHTML=NHOM.filter(function(g){return dem[g[0]];}).map(function(g){return '<button data-n="'+g[0]+'" class="'+(st.an[g[0]]?'tat':'')+'" title="Bấm để ẩn/hiện"><i style="background:'+M.vai[g[0]]+'"></i>'+g[1]+' '+dem[g[0]]+'</button>';}).join('');}
  cgv.addEventListener('click',function(e){var bt=e.target.closest('button');if(!bt)return;var n=bt.dataset.n;st.an[n]=!st.an[n];veCG();lop.capNhat();});
  document.getElementById('hien-ema').addEventListener('change',function(e){st.ema=e.target.checked;[b.h,b.l,b.c,b.e89,b.e200,b.e610].forEach(function(s){s.applyOptions({visible:st.ema});});dai.capNhat();});
  var bang=document.getElementById('bang-moc'),tom=document.getElementById('moc-tom');
  function chon(i){var x=B[i];if(!x)return;sel.value=i;mauEl.querySelectorAll('button').forEach(function(bt){bt.classList.toggle('dang',+bt.dataset.i===i);});
    st.live=luc(x);st.gioLive=x.gio.slice(0,2)+':'+x.gio.slice(2);var a=timNen(N,st.live-10*86400),z=timNen(N,st.live+5*86400);a=Math.max(0,a);z=Math.max(a+1,z+1);
    r=cat(N,a,Math.min(N.t.length,z));se.setData(r.nen);datEMA(b,r);st.tCuoi=r.nen.length?r.nen[r.nen.length-1].time:0;
    var iL=timNen(N,st.live);se.setMarkers(iL>=a&&iL<z?[{time:N.t[iL],position:'aboveBar',color:MAU.accent,shape:'arrowDown'}]:[]);
    var lo=Infinity,hi=-Infinity;r.nen.forEach(function(c){if(c.low<lo)lo=c.low;if(c.high>hi)hi=c.high;});var mn=lo,mx=hi;
    x.m.forEach(function(m){[m[0],m[1]].forEach(function(g){if(g!=null&&g>=lo*0.93&&g<=hi*1.07){if(g<mn)mn=g;if(g>mx)mx=g;}});});st.auto={minValue:mn,maxValue:mx};
    var gom={},items=[];x.m.forEach(function(m,j){var v=vaiCua(m[2]),key=m[0]+'|'+m[1]+'|'+v[1];var it={k:j,gia:m[0],tren:m[1],vai:m[2],ten:v[0],nhom:v[1],khung:m[3],cc:m[4].join(' + '),trich:m[5],mg:m[6],huong:m[7],chac:m[8],luc:st.live+giay(m[6])};
      if(gom[key]){var g=gom[key];if(it.cc&&g.cc.indexOf(it.cc)<0)g.cc=g.cc?g.cc+' + '+it.cc:it.cc;if(g.ten.indexOf(it.ten)<0)g.ten+=', '+it.ten;g.dup.push(j);}else{it.dup=[j];gom[key]=it;items.push(it);}});
    st.items=items;st.chon=-1;veCG();
    var n=x.m.length,coCC=x.m.filter(function(m){return m[4].length;}).length,cham=0,rows=[];
    x.m.forEach(function(m,j){var v=vaiCua(m[2]),it={gia:m[0],tren:m[1],luc:st.live+giay(m[6])},sd=sauDo(N,it);if(sd.cls==='cham')cham++;
      var iR=timNen(N,it.luc),ref=iR>0?N.c[iR-1]:null,ds=ref?((m[0]-ref)/ref*100):null;
      rows.push('<tr data-k="'+(gom[m[0]+'|'+m[1]+'|'+v[1]]||{}).k+'"><td class="so">'+esc(m[6]||'—')+'</td><td class="so"><b>'+fmtGia(m[0])+(m[1]!=null?'–'+fmtGia(m[1]):'')+'</b>'+(ds!=null?'<br><small>'+(ds>0?'+':'')+ds.toFixed(1).replace('.',',')+'%</small>':'')+'</td>'+
        '<td class="vai"><i style="background:'+MAU.vai[v[1]]+'"></i>'+esc(v[0])+(m[8]?'':'<span class="khong-chac" title="không chắc">?</span>')+'</td><td>'+esc(m[3]||'')+'</td>'+
        '<td>'+(m[4].length?esc(m[4].join(' + ')):'<span class="chua">— không nêu</span>')+'</td><td class="trich-o">'+(m[5]?'“'+esc(m[5])+'”':'')+'</td><td class="'+sd.cls+'">'+esc(sd.txt)+'</td></tr>');});
    bang.innerHTML='<thead><tr><th>Phút</th><th>Giá<br><small>so giá lúc nói</small></th><th>Vai trò</th><th>Khung</th><th>Căn cứ người đó nói</th><th>Câu trích</th><th>Giá chạm trong 5 ngày?</th></tr></thead><tbody>'+rows.join('')+'</tbody>';
    tom.innerHTML='Buổi <b>'+x.ngay.slice(8,10)+'/'+x.ngay.slice(5,7)+'</b>, live lúc '+st.gioLive+(x.gn?' (BTC ~'+fmtGia(x.gn)+')':'')+': <b>'+n+'</b> mốc, <b>'+coCC+'</b> mốc ('+(n?Math.round(coCC/n*100):0)+'%) có căn cứ nói ra ngay lúc nêu; '+cham+' mốc được giá chạm trong 5 ngày sau.'+(x.td?' <span style="color:var(--muted)">'+esc(x.td)+'</span>':'');
    var L=r.nen.length;chart.timeScale().setVisibleLogicalRange({from:-1,to:L-1+Math.round(L*(el.clientWidth<560?0.62:0.42))});lop.capNhat();dai.capNhat();}
  bang.addEventListener('click',function(e){var tr=e.target.closest('tr[data-k]');if(!tr)return;var k=+tr.dataset.k;st.chon=st.chon===k?-1:k;
    bang.querySelectorAll('tr').forEach(function(t){t.classList.toggle('chon',st.chon>=0&&+t.dataset.k===st.chon);});lop.capNhat();});
  var cg=chuGiaiEMA(document.getElementById('cg-moc'),se,b);chart.subscribeCrosshairMove(cg);cg(null);
  window.__chonBuoi=function(ngay){var i=-1;B.forEach(function(x,j){if(x.ngay===ngay&&(i<0||x.m.length>B[i].m.length))i=j;});if(i<0)return false;chon(i);return true;};
  window.__coBuoi={};B.forEach(function(x){window.__coBuoi[x.ngay]=1;});
  var md=(D.mau||[]).filter(function(m){return idx[m.id]!=null;});chon(md.length?idx[md[md.length-1].id]:B.length-1);
  VE_LAI.push(function(){chart.applyOptions(tuyChonLW());se.applyOptions(mauNen());mauEMA(b);veCG();cg(null);chon(+sel.value);});}

/* ---------- Chart.js ---------- */
function datCJ(){var M=MAU;Chart.defaults.font.family=FONT;Chart.defaults.font.size=12;Chart.defaults.color=M.text2;Chart.defaults.borderColor=M.grid;}
function hinhThang(){var el=document.getElementById('cj-thang');if(!el||!D.thang)return;if(!window.Chart){el.parentNode.innerHTML='<p class="loi-hinh">Thiếu vendor/chart.umd.js</p>';return;}
  var T=D.thang,ch=null;
  var ghiChu={id:'ghiChu',afterDatasetsDraw:function(c){var M=MAU,x=c.scales.x,y=c.scales.y,a=c.chartArea,ctx=c.ctx;ctx.save();
    if(T.cme){var i=T.thang.indexOf(T.cme.thang);if(i>=0){var x0=x.getPixelForValue(i),x1=i+1<T.thang.length?x.getPixelForValue(i+1):x0+40,xx=x0+(x1-x0)*Math.min(1,(T.cme.ngay_so-15)/30)+(x1-x0)*0;
      ctx.setLineDash([5,4]);ctx.strokeStyle=M.cc.gap;ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(xx,a.top);ctx.lineTo(xx,a.bottom);ctx.stroke();ctx.setLineDash([]);
      ctx.fillStyle=M.text2;ctx.font='600 11.5px '+FONT;ctx.textAlign='left';ctx.fillText('CME chạy 24/7 từ '+T.cme.ngay,Math.min(xx+5,a.right-150),a.top+12);}}
    var gn=T.gap_note,gi=T.loai.map(function(l){return l.key;}).indexOf('gap'),meta=c.getDatasetMeta(gi);
    if(gn&&meta&&!meta.hidden){var p=meta.data[gn.dinh];if(p){ctx.fillStyle=M.cc.gap;ctx.font='700 12px '+FONT;ctx.textAlign='center';ctx.fillText('đỉnh '+String(T.pt.gap[gn.dinh]).replace('.',',')+'%',p.x,p.y-10);}
      var q=meta.data[gn.tu];if(q){ctx.font='700 11.5px '+FONT;ctx.textAlign='left';ctx.fillStyle=M.cc.gap;var tq='gap CME từ '+T.nhan[gn.tu]+' chỉ còn '+String(gn.min).replace('.',',')+'–'+String(gn.max).replace('.',',')+'%';
        ctx.fillText(tq,Math.min(q.x-20,a.right-ctx.measureText(tq).width-4),a.top+30);ctx.strokeStyle=M.cc.gap;ctx.setLineDash([2,3]);ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(q.x,a.top+36);ctx.lineTo(q.x,q.y-8);ctx.stroke();ctx.setLineDash([]);}}
    ctx.restore();}};
  function ve(){datCJ();var M=MAU;if(ch)ch.destroy();
    ch=new Chart(el,{type:'line',data:{labels:T.nhan,datasets:T.loai.map(function(l){var g=l.key==='gap';return {label:l.ten,data:T.pt[l.key],borderColor:M.cc[l.key],backgroundColor:M.cc[l.key],
      borderWidth:g?3.5:2,pointRadius:g?4:2.5,pointHoverRadius:6,cubicInterpolationMode:'monotone',order:g?0:1};})},
      options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},layout:{padding:{top:6}},
        plugins:{legend:{position:'top',labels:{usePointStyle:true,pointStyle:'circle',boxWidth:8,boxHeight:8,padding:12}},
          tooltip:{callbacks:{title:function(it){var i=it[0].dataIndex;return 'Tháng '+(+T.thang[i])+' · '+T.n[i]+' mốc';},
            label:function(it){var k=T.loai[it.datasetIndex].key;return ' '+it.dataset.label+': '+String(it.parsed.y).replace('.',',')+'% ('+T.cnt[k][it.dataIndex]+' mốc)';}}}},
        scales:{y:{beginAtZero:true,ticks:{callback:function(v){return v+'%';}},grid:{color:M.grid},border:{display:false}},x:{grid:{display:false}}}},plugins:[ghiChu]});}
  ve();VE_LAI.push(ve);}
function hinhEMA(){var el=document.getElementById('cj-ema');if(!el||!D.ema)return;if(!window.Chart){el.parentNode.innerHTML='<p class="loi-hinh">Thiếu vendor/chart.umd.js</p>';return;}
  var E=D.ema,ch=null;
  var nhanMin={id:'nhanMin',afterDatasetsDraw:function(c){var M=MAU,ctx=c.ctx;ctx.save();ctx.font='600 11px '+FONT;ctx.fillStyle=M.text;ctx.textBaseline='middle';
    E.forEach(function(e,i){var best=-1,bv=Infinity;c.data.datasets.forEach(function(d,j){var v=d.data[i];if(v!=null&&v<bv&&!c.getDatasetMeta(j).hidden){bv=v;best=j;}});
      if(best<0)return;var el=c.getDatasetMeta(best).data[i];if(el)ctx.fillText(String(bv).replace('.',',')+'%',el.x+5,el.y);});ctx.restore();}};
  function ve(){datCJ();var M=MAU;if(ch)ch.destroy();
    ch=new Chart(el,{type:'bar',data:{labels:E.map(function(e){return e.ten+' (n='+e.n+')';}),datasets:[
      {label:'SMA',data:E.map(function(e){return e.sma;}),backgroundColor:M.muted,borderRadius:4,borderSkipped:false},
      {label:'EMA',data:E.map(function(e){return e.ema;}),backgroundColor:M.ema89,borderRadius:4,borderSkipped:false},
      {label:'Dải EMA34 (high/low), lấy mép gần giá',data:E.map(function(e){return e.dai;}),backgroundColor:M.ema34,borderRadius:4,borderSkipped:false}]},
      options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,layout:{padding:{right:40}},
        plugins:{legend:{position:'top',labels:{usePointStyle:true,pointStyle:'rectRounded',boxWidth:10,padding:12}},
          tooltip:{callbacks:{label:function(it){var e=E[it.dataIndex];return ' '+it.dataset.label+': '+String(it.parsed.x).replace('.',',')+'%'+(it.datasetIndex===2&&e.ghi?' — '+e.ghi:'');}}}},
        datasets:{bar:{barPercentage:0.86,categoryPercentage:0.78}},
        scales:{x:{beginAtZero:true,title:{display:true,text:'Sai số trung vị so với con số người đó nói (%) — thấp hơn = khớp hơn'},ticks:{callback:function(v){return v+'%';}},grid:{color:M.grid},border:{display:false}},
          y:{grid:{display:false}}}},plugins:[nhanMin]});}
  ve();VE_LAI.push(ve);}

/* ---------- nhãn ngày → mở buổi live ---------- */
function ganNgay(){var co=window.__coBuoi||{};document.querySelectorAll('.ngay[data-ngay]').forEach(function(s){if(co[s.dataset.ngay]){s.classList.add('co-buoi');s.title+=' — bấm để xem mốc giá buổi này trên chart';}});
  document.addEventListener('click',function(e){var s=e.target.closest('.ngay.co-buoi');if(!s||!window.__chonBuoi)return;if(window.__chonBuoi(s.dataset.ngay)){var f=document.getElementById('hinh-moc');if(f)f.scrollIntoView({behavior:'smooth',block:'start'});}});}

[hinhSonic,hinhMoc,hinhThang,hinhEMA,ganNgay].forEach(function(f){try{f();}catch(e){console.error(e);}});
})();
"""

if __name__ == "__main__":
    main()
