#!/usr/bin/env python3
"""Kiểm phiếu nhận định trong phieu/: JSON hợp lệ, giá trị đúng bộ, số giá hợp lý, có trích dẫn.

Cách dùng: python3 cong_cu/kiem_phieu.py
"""
import json
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
HUONG = {"TANG", "GIAM", "PHAN_VAN"}
KHUNG = {"M5", "M15", "H1", "H4", "D1", "W1", "chung"}
TRANG_THAI = {"de_xuat_moi", "dang_giu", "da_khop", "da_chot", "da_cat"}


def so_gia(x):
    if x is None:
        return []
    return [v for v in (x if isinstance(x, list) else [x]) if isinstance(v, (int, float))]


def kiem(p):
    loi = []
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return None, [f"JSON hỏng: {e}"]
    gia = d.get("gia_btc_luc_noi")
    hop_ly = (lambda v: abs(v - gia) / gia <= 0.35) if isinstance(gia, (int, float)) and gia else (lambda v: 40_000 <= v <= 150_000)
    nd = d.get("nhan_dinh") or []
    if not nd:
        loi.append("không có nhận định")
    for i, n in enumerate(nd):
        if n.get("huong") not in HUONG:
            loi.append(f"nd{i} hướng lạ: {n.get('huong')}")
        if n.get("khung") not in KHUNG:
            loi.append(f"nd{i} khung lạ: {n.get('khung')}")
        if not n.get("trich"):
            loi.append(f"nd{i} thiếu trích dẫn")
        lech = [v for v in so_gia(n.get("dich")) if not hop_ly(v)]
        if lech:
            loi.append(f"nd{i} đích lệch giá: {lech}")
    for i, l in enumerate(d.get("lenh") or []):
        if l.get("trang_thai") not in TRANG_THAI:
            loi.append(f"lệnh{i} trạng thái lạ: {l.get('trang_thai')}")
        lech = [v for k in ("vao", "tp", "sl") for v in so_gia(l.get(k)) if not hop_ly(v)]
        if lech:
            loi.append(f"lệnh{i} giá lệch: {lech}")
    return d, loi


if __name__ == "__main__":
    ds = sorted((GOC / "phieu").glob("*.json"))
    dem = {h: 0 for h in HUONG}
    for p in ds:
        d, loi = kiem(p)
        if d:
            chinh = next((n for n in d["nhan_dinh"] if n.get("khung") == "H4"), (d.get("nhan_dinh") or [{}])[0])
            dem[chinh.get("huong")] = dem.get(chinh.get("huong"), 0) + 1
            tom = f"{chinh.get('khung')} {chinh.get('huong')} · {len(d['nhan_dinh'])} nđ · {len(d.get('lenh') or [])} lệnh"
        else:
            tom = "—"
        print(f"{p.stem[:15]} {tom}" + (f"  ⚠ {'; '.join(loi)}" if loi else ""))
    print(f"\n{len(ds)} phiếu · hướng chính (ưu tiên H4): {dem}")
