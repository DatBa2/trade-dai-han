#!/usr/bin/env python3
"""Tổng hợp 50 phiếu: nhận định H4 chính + giá thật lúc live + giá chạy sau đó → phieu/_tong_hop.csv

Nhận định chính = phần tử khung H4 (không có thì "chung", rồi phần tử đầu).
Đích = đích chặng cuối (`duong_di`) nếu có, không thì `dich`. Vùng [a, b] → mép gần (GIẢM lấy b, TĂNG lấy a).
Cửa sổ chấm = `han_gio` nếu có, không thì 24 giờ, tính từ giờ bắt đầu live.
Chỉ là đối chiếu PHỤ — mục tiêu chính của dự án là bot GIỐNG người đó, không phải đúng thị trường.
"""
import csv, datetime as dt, json
from collections import Counter
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
VN = dt.timedelta(hours=7)


def doc_gia():
    with (GOC / "du_lieu" / "btc_15m.csv").open() as f:
        return [(dt.datetime.fromisoformat(r["ts_utc"]), float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"]))
                for r in csv.DictReader(f)]


def chinh(d):
    nd = d.get("nhan_dinh") or [{}]
    return next((n for k in ("H4", "chung") for n in nd if n.get("khung") == k), nd[0])


def dich_cuoi(n):
    d = (n.get("duong_di") or [{}])[-1].get("dich") if n.get("duong_di") else n.get("dich")
    if isinstance(d, list):
        d = [x for x in d if isinstance(x, (int, float))]
        return (max(d) if n.get("huong") == "GIAM" else min(d)) if d else None
    return d if isinstance(d, (int, float)) else None


def main():
    gia = doc_gia()
    rows, dem = [], Counter()
    for p in sorted((GOC / "phieu").glob("2*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        n = chinh(d)
        bat_dau = dt.datetime.fromisoformat(f"{d['ngay']} {d['gio_vn']}") - VN
        han = n.get("han_gio") or 24
        cua_so = [g for g in gia if bat_dau <= g[0] < bat_dau + dt.timedelta(hours=han)]
        gia_live = cua_so[0][1] if cua_so else None
        dich = dich_cuoi(n)
        cham = dung = ""
        if cua_so and n.get("huong") in ("TANG", "GIAM"):
            cao, thap, dong = max(g[2] for g in cua_so), min(g[3] for g in cua_so), cua_so[-1][4]
            dung = "đúng" if (dong > gia_live) == (n["huong"] == "TANG") else "sai"
            if dich:
                cham = "chạm" if (thap <= dich if n["huong"] == "GIAM" else cao >= dich) else "không"
        dem[n.get("huong")] += 1
        rows.append({"buoi": p.stem, "khung": n.get("khung"), "huong": n.get("huong"), "do_chac": n.get("do_chac"),
                     "gia_noi": d.get("gia_btc_luc_noi") or "", "gia_that": round(gia_live) if gia_live else "",
                     "dich": dich or "", "han_gio": han, "nhieu_chang": "có" if n.get("duong_di") else "",
                     "so_lenh": len(d.get("lenh") or []), "huong_cuoi_cua_so": dung, "cham_dich": cham})
    with (GOC / "phieu" / "_tong_hop.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, list(rows[0])); w.writeheader(); w.writerows(rows)

    co_huong = [r for r in rows if r["huong_cuoi_cua_so"]]
    co_dich = [r for r in rows if r["cham_dich"]]
    lech = [abs(r["gia_noi"] - r["gia_that"]) / r["gia_that"] for r in rows if r["gia_noi"] and r["gia_that"]]
    print(f"{len(rows)} buổi · hướng chính: {dict(dem)}")
    print(f"độ chắc: {dict(Counter(r['do_chac'] for r in rows))} · nhiều chặng: {sum(1 for r in rows if r['nhieu_chang'])} · "
          f"buổi có lệnh: {sum(1 for r in rows if r['so_lenh'])}")
    print(f"giá người đó nói vs giá thật: {len(lech)} buổi có số, lệch trung bình {sum(lech) / len(lech):.1%}" if lech else "")
    print(f"[phụ] hướng đúng cuối cửa sổ: {sum(r['huong_cuoi_cua_so'] == 'đúng' for r in co_huong)}/{len(co_huong)} · "
          f"chạm đích: {sum(r['cham_dich'] == 'chạm' for r in co_dich)}/{len(co_dich)}")
    for h in ("TANG", "GIAM"):
        nh = [r for r in co_huong if r["huong"] == h]
        if nh:
            print(f"   {h}: đúng {sum(r['huong_cuoi_cua_so'] == 'đúng' for r in nh)}/{len(nh)}")


if __name__ == "__main__":
    main()
