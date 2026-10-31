#!/usr/bin/env python3
"""Soát bản làm sạch: tỉ lệ từ, số chỗ [?], và bao nhiêu mốc GIÁ của bản gốc còn trong bản sạch.

Mốc giá = số dạng 75.000 / 75000 / 75K / 75 nghìn (≥ 10.000). "80.000 năm" ở bản gốc tính là 80.500.
Cách dùng: python3 cong_cu/soat_lam_sach.py [tên-file ...]   (không truyền = soát hết lam_sach/)
"""
import re, sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent / "transcripts"
LE = {"hai": 200, "ba": 300, "tư": 400, "bốn": 400, "năm": 500, "sáu": 600, "bảy": 700, "tám": 800, "chín": 900}


def moc_gia(t):
    ra = set()
    for m in re.finditer(r'(\d{2,3})(?:[.,](\d{3}|\d{2})|\s?[kK]\b|\s?nghìn)(?:\s+(hai|ba|tư|bốn|năm|sáu|bảy|tám|chín)\b)?', t):
        so = int(m.group(1)) * 1000
        if m.group(2) and len(m.group(2)) == 3:
            # phụ đề viết "80 nghìn 8" thành 80.008 → thực là 80.800
            le = m.group(2)
            so += int(le[2]) * 100 if le.startswith("00") else int(le)
        if m.group(3) and so % 1000 == 0:
            so += LE[m.group(3)]
        if 10_000 <= so <= 200_000:
            ra.add(so)
    return ra


def soat(md):
    goc = next((GOC / d / (md.stem + ".txt") for d in ("phu_de", "whisper")
                if (GOC / d / (md.stem + ".txt")).exists()), None)
    a, b = goc.read_text(encoding="utf-8"), md.read_text(encoding="utf-8")
    ga, gb = moc_gia(a), moc_gia(b)
    con = len(ga & gb) / len(ga) if ga else 1
    mat = sorted(ga - gb)
    print(f"{md.stem}: từ {len(b.split()) / len(a.split()):.0%} · [?] {b.count('[?]')} · "
          f"mốc giá còn {len(ga & gb)}/{len(ga)} ({con:.0%})" + (f" · mất {mat[:8]}" if mat else ""))


if __name__ == "__main__":
    ds = [GOC / "lam_sach" / f"{n}.md" for n in sys.argv[1:]] or sorted((GOC / "lam_sach").glob("*.md"))
    for md in ds:
        soat(md)
