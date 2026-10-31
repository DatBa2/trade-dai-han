#!/usr/bin/env python3
"""Chọn các mốc giờ trong buổi live mà người đó đang VẼ / PHÂN TÍCH trên chart (nói dày từ khoá kẻ, Fibo, trendline…).

Đọc transcript zip_clean (có [hh:mm:ss] từng câu) hoặc phụ đề .vtt; chấm điểm từng cửa sổ 60 giây theo số từ khoá,
lấy N cửa sổ điểm cao nhất, cách nhau ≥ KHOANG_CACH giây. In ra các mốc hh:mm:ss (giữa cửa sổ, lúc hình đã lên).
Cách dùng: python3 cong_cu/chon_moc.py <file .txt|.vtt> [N=10]
"""
import re, sys
from pathlib import Path

TU_KHOA = ["kẻ", "vẽ", "trendline", "trend line", "fibo", "kháng cự", "hỗ trợ", "ma34", "ma 34", "ma89", "ma 89",
           "ma200", "ma 200", "mô hình", "vai đầu vai", "tam giác", "lá cờ", "cái nêm", "kênh giá", "hộp", "box",
           "râu", "vùng này", "chỗ này", "đường này", "heatmap", "thanh lý", "rsi", "phân kỳ", "volume", "khung h4",
           "khung d1", "nến h4", "nến ngày", "đỉnh", "đáy", "gap", "cản", "fake out", "breakout", "test lại"]
KHOANG_CACH = 150


def doc_cau(p):
    """[(giây, câu)]"""
    t = p.read_text(encoding="utf-8")
    if p.suffix == ".vtt":
        ra = []
        for khoi in re.split(r"\n\n+", t):
            m = re.search(r"(\d+):(\d+):(\d+)\.\d+ -->", khoi)
            if m:
                chu = re.sub(r"<[^>]+>", "", " ".join(l for l in khoi.split("\n") if "-->" not in l))
                ra.append((int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]), chu))
        return ra
    return [(int(h) * 3600 + int(m) * 60 + int(s), c) for h, m, s, c in re.findall(r"\[(\d+):(\d+):(\d+)\] (.*)", t)]


def chon(p, n=10):
    cau = doc_cau(p)
    diem = {}
    for g, c in cau:
        c = c.lower()
        diem[g // 60] = diem.get(g // 60, 0) + sum(c.count(k) for k in TU_KHOA)
    ra = []
    for phut, d in sorted(diem.items(), key=lambda x: -x[1]):
        if d < 3 or len(ra) >= n:
            break
        if all(abs(phut * 60 - x) >= KHOANG_CACH for x in ra):
            ra.append(phut * 60 + 30)
    return [f"{x // 3600:02d}:{x % 3600 // 60:02d}:{x % 60:02d}" for x in sorted(ra)]


if __name__ == "__main__":
    print(" ".join(chon(Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 10)))
