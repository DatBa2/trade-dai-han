#!/usr/bin/env python3
"""Kiểm 180 file nhãn học hoc_v5/nhan/*.json:
  1. đủ 180 buổi, tên trong file khớp tên file, đủ các trường mới;
  2. buổi từ 2026-07-01: các trường nhãn v2 giữ nguyên so với thi/dap_an_v2/nhan/;
  3. câu trích NGUYÊN VĂN: mọi chuỗi `trich` (lồng ở mọi trường) phải là chuỗi con của transcript đúng buổi
     (so sau khi bỏ dấu câu, chữ thường, gộp khoảng trắng; bỏ phần [?] và […]). Đoạn nối bằng "—"/"..." tách ra kiểm từng mẩu.
Cách dùng: python3 hoc_v5/kiem_nhan.py [--chi-tiet]
"""
import glob, json, re, sys, unicodedata
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
NHAN = GOC / "hoc_v5" / "nhan"
MOI = ["nhin_lai_view_truoc", "trendline", "nen_volume", "cach_lam", "vung_nguoi_do",
       "view_trung_han", "vung_tranh", "giu_dong", "tin_tuc"]
V2 = ["dau_buoi", "cuoi_buoi", "doi_y_giua_buoi", "chang_ke_tiep", "duong_di", "dich_chinh", "han_gio",
      "vo_hieu", "lenh", "hanh_dong", "khung_lon"]


def chuan(s):
    s = unicodedata.normalize("NFC", s or "").lower()
    s = re.sub(r"\[\d{1,2}:\d{2}(:\d{2})?\]|\[\?\]|\[…\]|\[\.\.\.\]", " ", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def cac_trich(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in ("trich", "cau") and isinstance(v, str):
                yield v
            else:
                yield from cac_trich(v)
    elif isinstance(x, list):
        for v in x:
            yield from cac_trich(v)


def transcript(ten):
    vid = re.match(r"\d{4}-\d{2}-\d{2}(?:_\d{4})?_(.+)$", ten)[1]
    c = [p for p in glob.glob(str(GOC / "transcripts/zip_clean" / f"*{vid}*")) + glob.glob(str(GOC / "transcripts/lam_sach" / f"*{vid}*"))
         + glob.glob(str(GOC / "transcripts/phu_de" / f"*{vid}*.txt")) if p.endswith((".txt", ".md"))]
    return " ".join(chuan(Path(p).read_text(encoding="utf-8", errors="ignore")) for p in c)


def main():
    files = sorted(NHAN.glob("2*.json"))
    loi, kem = [], []
    for p in files:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            loi.append((p.stem, f"JSON hỏng: {e}")); continue
        if d.get("buoi") != p.stem:
            loi.append((p.stem, f"buoi trong file = {d.get('buoi')}"))
        thieu = [k for k in MOI if k not in d]
        if thieu:
            loi.append((p.stem, f"thiếu trường {thieu}"))
        v2 = GOC / "thi/dap_an_v2/nhan" / p.name
        if p.stem >= "2026-07-01" and v2.exists():
            g = json.loads(v2.read_text(encoding="utf-8"))
            doi = [k for k in V2 if g.get(k) != d.get(k)]
            if doi:
                loi.append((p.stem, f"trường v2 bị đổi: {doi}"))
        tx = transcript(p.stem)
        tong = dung = 0
        for t in cac_trich(d):
            for manh in re.split(r"\s*(?:—|\.\.\.|…)\s*", t):
                m = chuan(manh)
                if len(m) < 12:
                    continue
                tong += 1
                dung += m in tx
        tl = dung / tong if tong else 1
        if tl < 0.8:
            kem.append((p.stem, dung, tong))
        if "--chi-tiet" in sys.argv:
            print(f"{p.stem}: trích nguyên văn {dung}/{tong}")
    print(f"Số file: {len(files)} (cần 180)")
    print(f"Lỗi cấu trúc: {len(loi)}")
    for x in loi:
        print("  ✗", *x)
    print(f"File có < 80% câu trích nguyên văn: {len(kem)}")
    for ten, a, b in kem:
        print(f"  ⚠ {ten}: {a}/{b}")


if __name__ == "__main__":
    main()
