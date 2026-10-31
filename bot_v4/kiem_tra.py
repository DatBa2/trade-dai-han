#!/usr/bin/env python3
"""Kiểm tra bắt buộc của bot v4 — đúng mục 9 của bot_v4/THIET_KE.md (TK 9). Phải PASS hết trước khi báo kết quả.

    python3 bot_v4/kiem_tra.py [--du-lieu THU_MUC]

Nhóm 1  Cắt cụt: 20 mốc T ngẫu nhiên (hạt giống cố định) — chạy với dữ liệu cắt tại T → quyết định / lệnh / vốn trước T
        GIỐNG HỆT bản đủ; view_tai(T) (tự cắt) = view bản đủ.
Nhóm 2  Fractal chỉ dùng sau 3 nến phải đã đóng; D1/W1 chỉ dùng nến đã đóng (ca dựng tay); đổi dữ liệu TƯƠNG LAI không
        làm đổi view / lệnh hiện tại.
Nhóm 3  EMA / RSI / ATR / fractal so với tính tay trên chuỗi nhỏ.
Nhóm 4  Cộng lại lãi/lỗ từ lenh.csv khớp von.csv tới 0,01$; tự tính lại lãi + phí từng lệnh; ràng buộc lệnh (SL, R:R,
        khớp trong 6 nến, không khớp sớm hơn, ≤ 3 lệnh, ≤ 1 lệnh/tài sản).
Nhóm 5  Tình huống khớp lệnh TK 7 (nến khớp + chạm SL; chạm cả TP và SL; gap qua SL; ...).
"""
import argparse
import bisect
import csv
import datetime as dt
import math
import random
import sys
import tempfile
from pathlib import Path

GOC = Path(__file__).resolve().parent
sys.path.insert(0, str(GOC))
import dong_co as D  # noqa: E402
from cong_cu.chi_bao import atr_wilder, ema, fractal, fractal_da_xac_nhan, rsi_wilder  # noqa: E402

UTC = dt.timezone.utc
KQ = []


def kiem(nhom, ten, ok, chi_tiet=""):
    KQ.append((nhom, ten, bool(ok), chi_tiet))
    print(f"[{'PASS' if ok else 'FAIL'}] N{nhom} {ten}" + (f" — {chi_tiet}" if chi_tiet and not ok else ""))


def gan(a, b, tol=1e-9):
    return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def ts(s):
    return D.ts_tu_chuoi(s)


# ============================ NHÓM 3: chỉ báo vs tính tay ============================
def nhom3():
    e = ema([1, 2, 3, 4, 5, 6], 3)
    kiem(3, "EMA3 [1..6] = [-,-,2,3,4,5]", e[:2] == [None, None] and all(gan(a, b) for a, b in zip(e[2:], [2, 3, 4, 5])),
         str(e))
    e = ema([10, 11, 12, 13, 20], 3)          # SMA(10,11,12)=11; 0,5·13+0,5·11=12; 0,5·20+0,5·12=16
    kiem(3, "EMA3 [10,11,12,13,20] = [-,-,11,12,16]", e[:2] == [None, None] and all(gan(a, b) for a, b in zip(e[2:], [11, 12, 16])), str(e))
    e = ema([1.0] * 33, 34)
    kiem(3, "EMA34 chưa đủ 34 nến → toàn None", all(v is None for v in e))
    xs = [100 + 3 * math.sin(i / 3) + i * 0.1 for i in range(60)]
    e = ema(xs, 34)
    tay = sum(xs[:34]) / 34
    for i in range(34, 60):
        tay = 2 / 35 * xs[i] + (1 - 2 / 35) * tay
    kiem(3, "EMA34 = SMA34 rồi α=2/35 (tính tay vòng lặp)", gan(e[59], tay) and e[32] is None and gan(e[33], sum(xs[:34]) / 34))
    # RSI n=3: c=[10,11,10,12,13,12]; thay đổi +1,-1,+2,+1,-1
    # TB lãi đầu (1+0+2)/3=1, lỗ (0+1+0)/3=1/3 → RSI=75; i=4: lãi (2+1)/3=1, lỗ (2/3)/3=2/9 → RS 4,5 → 81,818..;
    # i=5: lãi 2/3, lỗ (4/9+1)/3=13/27 → RS 18/13 → 100−1300/31
    r = rsi_wilder([10, 11, 10, 12, 13, 12], 3)
    kiem(3, "RSI3 Wilder tính tay [75; 81,818; 58,065]", r[:3] == [None] * 3 and gan(r[3], 75.0)
         and gan(r[4], 100 - 100 / 5.5) and gan(r[5], 100 - 1300 / 31), str(r))
    r = rsi_wilder([1, 2, 3, 4, 5], 3)
    kiem(3, "RSI chỉ tăng → 100", gan(r[3], 100.0) and gan(r[4], 100.0))
    # ATR n=3: TR = [2, 3, 2, 3] → ATR[2] = 7/3, ATR[3] = (7/3·2 + 3)/3 = 23/9
    a = atr_wilder([10, 12, 11, 13], [8, 9, 9, 10], [9, 11, 10, 12], 3)
    kiem(3, "ATR3 Wilder tính tay [7/3; 23/9]", a[:2] == [None, None] and gan(a[2], 7 / 3) and gan(a[3], 23 / 9), str(a))
    h = [1, 2, 3, 9, 3, 2, 1, 5, 4, 3, 2, 1]
    dinh, _ = fractal(h, [x - 0.5 for x in h], 3)
    kiem(3, "Fractal đỉnh tính tay: (3, 9) và (7, 5)", dinh == [(3, 9), (7, 5)], str(dinh))
    h = [1, 1, 1, 5, 5, 1, 1, 1, 1]
    dinh, _ = fractal(h, [0.5] * 9, 3)
    kiem(3, "Fractal đỉnh bằng nhau → chỉ nến sớm nhất (DG 7)", dinh == [(3, 5)], str(dinh))
    l = [9, 8, 7, 1, 7, 8, 9, 9, 9]
    _, day = fractal([x + 1 for x in l], l, 3)
    kiem(3, "Fractal đáy tính tay: (3, 1)", day == [(3, 1)], str(day))


# ============================ dữ liệu giả cho nhóm 2, 5 ============================
def du_gia(ma, nen_h4, bd="2024-03-04 00:00", d1=None):
    """Dựng du từ list (o, h, l, c) H4 liên tục bắt đầu `bd`; d1 = list (ts_utc_mo, o, h, l, c) (tuỳ chọn)."""
    t0 = ts(bd)
    h4 = [D._nen(t0 + i * 4 * 3600, t0 + (i + 1) * 4 * 3600, o, h, l, c, 1.0) for i, (o, h, l, c) in enumerate(nen_h4)]
    dd = [D._nen(mo, D.gio_dong_d1(ma, mo), o, h, l, c, 1.0) for mo, o, h, l, c in (d1 or [])]
    return D.dung_du_lieu(ma, h4, dd)


# ============================ NHÓM 2: nhân quả, ca dựng tay ============================
def nhom2(du_that):
    # (a) fractal: đỉnh ở nến 10 → chưa dùng ở nến 12 (mới 2 nến phải), dùng được từ nến 13
    hs = [100 + i * 0.1 for i in range(10)] + [120] + [101, 100.5, 100.2, 100.1, 100.0, 99.9]
    nen = [(x - 0.2, x, x - 1, x - 0.5) for x in hs]
    du = du_gia("BTC", nen)
    cb = du["cb"]
    kiem(2, "Fractal: đỉnh nến 10 có trong danh sách", (10, 120) in cb.dinh, str(cb.dinh))
    n12 = fractal_da_xac_nhan(cb.dinh, cb.dinh_i, 12)
    n13 = fractal_da_xac_nhan(cb.dinh, cb.dinh_i, 13)
    kiem(2, "Fractal: tại nến 12 CHƯA dùng đỉnh 10, tại nến 13 dùng được",
         all(i != 10 for i, _ in cb.dinh[:n12]) and any(i == 10 for i, _ in cb.dinh[:n13]))
    cb12 = D.cat_du_lieu(du, cb.dong[12])["cb"]
    kiem(2, "Fractal: dữ liệu cắt ở nến 12 không hề có đỉnh 10", all(i != 10 for i, _ in cb12.dinh), str(cb12.dinh))
    # (b) D1 crypto: nến D1 2024-03-04 đóng 2024-03-05 00:00
    d1 = [(ts("2024-03-04 00:00") + i * 86400, 1, 2, 0.5, 1.5) for i in range(5)]
    du = du_gia("BTC", [(1, 2, 0.5, 1.5)] * 30, d1=d1)
    cb = du["cb"]
    k_20 = cb.chi_so[ts("2024-03-05 20:00")]
    k_00 = cb.chi_so[ts("2024-03-06 00:00")]
    kiem(2, "D1 crypto: lúc đóng H4 05/03 20:00 dùng D1 04/03 (chưa dùng 05/03)", cb.d1i[k_20] == 0, str(cb.d1i[k_20]))
    kiem(2, "D1 crypto: lúc đóng H4 06/03 00:00 dùng D1 05/03", cb.d1i[k_00] == 1, str(cb.d1i[k_00]))
    # (c) D1 vàng: phiên "05/03" có ts_utc 2024-03-04 23:00 (giờ mùa đông NY: đóng 17:00 = 22:00 UTC)
    d1v = [(ts("2024-03-03 23:00"), 1, 2, 0.5, 1.5), (ts("2024-03-04 23:00"), 1, 2, 0.5, 1.5)]
    du = du_gia("VANG", [(1, 2, 0.5, 1.5)] * 30, d1=d1v)
    cb = du["cb"]
    kiem(2, "D1 vàng: giờ đóng phiên = ts + 23h (05/03 22:00 UTC)", cb.d_dong[1] == ts("2024-03-05 22:00"))
    kiem(2, "D1 vàng: lúc đóng H4 05/03 20:00 chưa dùng phiên 05/03; lúc 06/03 00:00 đã dùng",
         cb.d1i[cb.chi_so[ts("2024-03-05 20:00")]] == 0 and cb.d1i[cb.chi_so[ts("2024-03-06 00:00")]] == 1)
    # (d) W1 crypto: tuần 04/03 (thứ Hai) đóng 11/03 00:00
    d1 = [(ts("2024-03-04 00:00") + i * 86400, 1, 2, 0.5, 1.5) for i in range(14)]
    du = du_gia("BTC", [(1, 2, 0.5, 1.5)] * 60, d1=d1)
    cb = du["cb"]
    kiem(2, "W1: tuần đầu mở thứ Hai 04/03 00:00, đóng 11/03 00:00",
         du["W1"][0]["ts_utc"] == ts("2024-03-04 00:00") and du["W1"][0]["dong"] == ts("2024-03-11 00:00"))
    kiem(2, "W1: lúc đóng H4 CN 10/03 20:00 chưa có W1 nào đã đóng; 11/03 00:00 có W1 04/03",
         cb.w1i[cb.chi_so[ts("2024-03-10 20:00")]] == -1 and cb.w1i[cb.chi_so[ts("2024-03-11 00:00")]] == 0)
    du_c = D.cat_du_lieu(du, ts("2024-03-10 20:00"))
    kiem(2, "W1: dữ liệu cắt giữa tuần → không có W1 dở dang", len(du_c["W1"]) == 0, str(len(du_c["W1"])))
    kiem(2, "W1 vàng: phiên mở CN 10/03 23:00 UTC thuộc tuần thứ Hai 11/03",
         D.thu_hai_cua_tuan("VANG", ts("2024-03-10 23:00")) == ts("2024-03-11 00:00")
         and D.thu_hai_cua_tuan("VANG", ts("2024-03-07 23:00")) == ts("2024-03-04 00:00"))
    # (e) đổi dữ liệu TƯƠNG LAI (×1,7 mọi nến đóng sau t) — view, lệnh tại t không đổi (dữ liệu thật BTC)
    if du_that is not None:
        cb = du_that["cb"]
        rng = random.Random(20261031)
        sai = []
        ks = [k for k in range(len(cb.dong)) if ts("2024-01-01 00:00") <= cb.dong[k] < ts("2026-10-01 00:00")]
        for k in rng.sample(ks, 8):
            t = cb.dong[k]
            h4 = [r if r["dong"] <= t else dict(r, open=r["open"] * 1.7, high=r["high"] * 1.7, low=r["low"] * 1.7,
                                                  close=r["close"] * 1.7) for r in du_that["4H"]]
            d1 = [r if r["dong"] <= t else dict(r, open=r["open"] * 1.7, high=r["high"] * 1.7, low=r["low"] * 1.7,
                                                  close=r["close"] * 1.7) for r in du_that["1D"]]
            cb2 = D.dung_du_lieu("BTC", h4, d1)["cb"]
            a = (cb.view[k], cb.kieu[k], cb.ly_do[k], D.lap_lenh(cb, "BTC", k, 1, "chinh"), D.lap_lenh(cb, "BTC", k, -1, "chinh"))
            b = (cb2.view[k], cb2.kieu[k], cb2.ly_do[k], D.lap_lenh(cb2, "BTC", k, 1, "chinh"), D.lap_lenh(cb2, "BTC", k, -1, "chinh"))
            if a != b:
                sai.append(D.chuoi_gio(t))
        kiem(2, "Đổi giá tương lai ×1,7 → view + lệnh LONG/SHORT tại t không đổi (8 mốc BTC)", not sai, str(sai))


# ============================ NHÓM 5: tình huống khớp TK 7 ============================
def nhom5():
    F_VAO, F_TP, F_MK, TR = D.P["phi_vao"], D.P["phi_tp"], D.P["phi_market"], D.P["truot"]
    kl = 10.0
    phang = (99.0, 99.4, 98.6, 99.0)

    def chay_short(nen, **kw):
        du = du_gia("BTC", [(99, 99.5, 98.5, 99)] + nen + [phang] * 40)
        return du, D.mo_phong_lenh("BTC", "SHORT", "chinh", du["cb"].dong[0], 100.0, 102.0, 98.0, 95.0, 120, du, kl, **kw)

    khop = (99.5, 100.5, 99.2, 99.8)
    # 5a: nến khớp chạm cả SL (và TP) → chỉ xét SL, ra SL ngay trong nến khớp
    du, r = chay_short([(99.5, 102.5, 97.0, 99.0)])
    gia_sl = 102.0 * (1 + TR)
    lai = kl * (100 - gia_sl) - kl * 100 * F_VAO - kl * gia_sl * F_MK
    kiem(5, "Nến khớp chạm SL+TP → SL trong nến khớp, không TP1",
         r["ly_do_ra"] == "SL" and r["t_khop"] == r["t_ra"] == du["cb"].dong[1] and r["t_tp1"] is None
         and gan(r["gia_ra"], gia_sl) and gan(r["lai_usd"], lai), f"{r['ly_do_ra']} {r['lai_usd']} vs {lai}")
    kiem(5, "Phí: vào 0,02% + SL 0,05% trên giá sau trượt 0,02%; R = lãi / rủi ro dự kiến",
         gan(r["phi"], kl * 100 * F_VAO + kl * gia_sl * F_MK) and gan(r["R"], lai / (kl * 2.0)))
    # 5b: nến sau chạm cả TP1 và SL → SL trước
    du, r = chay_short([khop, (99.8, 102.5, 97.5, 99.0)])
    kiem(5, "Nến chạm cả TP1 và SL → tính SL trước", r["ly_do_ra"] == "SL" and r["t_tp1"] is None
         and r["t_ra"] == du["cb"].dong[2], r["ly_do_ra"])
    # 5c: gap: nến mở đã trên SL → ra ở giá mở (+trượt)
    du, r = chay_short([khop, (103.0, 104.0, 102.8, 103.5)])
    kiem(5, "Gap mở trên SL → ra ở giá mở 103 (+trượt)", r["ly_do_ra"] == "SL" and gan(r["gia_ra"], 103.0 * (1 + TR)),
         str(r["gia_ra"]))
    # 5d: TP1 rồi cùng nến chạm lại giá vào → chốt 50% ở TP1, phần còn lại hoà vốn (bảo thủ, DG 20)
    du, r = chay_short([khop, (99.6, 100.2, 97.9, 99.0)])
    gia_hv = 100.0 * (1 + TR)
    lai = 5 * (100 - 98) - 5 * 98 * F_TP + 5 * (100 - gia_hv) - 5 * gia_hv * F_MK - kl * 100 * F_VAO
    kiem(5, "TP1 chốt 50% + dời SL về giá vào; cùng nến chạm giá vào → SL_HOA_VON",
         r["ly_do_ra"] == "SL_HOA_VON" and r["t_tp1"] == du["cb"].dong[2] and gan(r["gia_tp1"], 98.0)
         and gan(r["lai_usd"], lai), f"{r['ly_do_ra']} {r['lai_usd']} vs {lai}")
    # 5e: TP1 rồi TP2 ở nến sau
    du, r = chay_short([khop, (99.6, 99.8, 97.9, 98.2), (98.2, 98.5, 94.9, 95.5)])
    lai = 5 * 2 - 5 * 98 * F_TP + 5 * 5 - 5 * 95 * F_TP - kl * 100 * F_VAO
    kiem(5, "TP1 rồi TP2 (phí TP limit 0,02%, không trượt)", r["ly_do_ra"] == "TP2" and gan(r["lai_usd"], lai)
         and r["t_ra"] == du["cb"].dong[3], f"{r['ly_do_ra']} {r['lai_usd']} vs {lai}")
    # 5f: nến khớp chạm TP nhưng không chạm SL → không chốt trong nến khớp; TP1 ở nến sau
    du, r = chay_short([(99.5, 100.3, 94.0, 99.0), (99.0, 99.5, 97.9, 98.5)])
    kiem(5, "Nến khớp chạm TP (không SL) → không chốt trong nến khớp", r["t_tp1"] == du["cb"].dong[2], D.chuoi_gio(r["t_tp1"]))
    # 5g: không chạm trong 6 nến sau → HUY ở giờ đóng nến thứ 6; nến 7 chạm không tính
    du, r = chay_short([phang] * 6 + [(99, 101, 98.5, 100)])
    kiem(5, "Không khớp trong 6 nến → HUY ở nến 6", r["ly_do_ra"] == "HUY" and r["t_ra"] == du["cb"].dong[6]
         and r["t_khop"] is None and r["lai_usd"] == 0.0, f"{r['ly_do_ra']} {D.chuoi_gio(r['t_ra'])}")
    # 5h: view đổi khi chờ → huỷ ở giờ đóng nến đổi view
    du = du_gia("BTC", [(99, 99.5, 98.5, 99)] + [phang] * 10)
    du["cb"].view = ["GIAM"] * 3 + ["PHAN_VAN"] * (len(du["cb"].view) - 3)
    r = D.mo_phong_lenh("BTC", -1, "chinh", du["cb"].dong[0], 100.0, 102.0, 98.0, 95.0, 120, du, kl)
    kiem(5, "View đổi khi lệnh chờ → HUY ở giờ đóng nến đổi view", r["ly_do_ra"] == "HUY" and r["t_ra"] == du["cb"].dong[3]
         and r["ly_do_huy"].startswith("doi_view"), r["ly_do_huy"])
    # 5i: gap qua giá limit + qua SL ngay nến khớp → khớp ở giá mở, ra ở giá mở
    du, r = chay_short([(103.0, 104.0, 102.5, 103.5)])
    kiem(5, "Gap mở qua limit và SL → khớp 103, SL ra 103 (+trượt)", gan(r["gia_vao"], 103.0) and r["ly_do_ra"] == "SL"
         and gan(r["gia_ra"], 103.0 * (1 + TR)), f"{r['gia_vao']} {r['gia_ra']}")
    # 5j: lệnh hồi LONG: khớp gap dưới limit ở giá mở; TP duy nhất; dừng 48h
    nen = [(101, 101.5, 100.5, 101)] + [(99.0, 100.5, 98.5, 99.5)] + [(99.8, 100.5, 99.0, 99.8)] * 20
    du = du_gia("ETH", nen)
    r = D.mo_phong_lenh("ETH", "LONG", "hoi", du["cb"].dong[0], 100.0, 98.0, None, 104.0, 48, du, kl)
    gia = 99.8 * (1 - TR)
    kiem(5, "Hồi LONG: khớp ở giá mở 99 (gap dưới limit); dừng 48h ở close nến khớp+12",
         gan(r["gia_vao"], 99.0) and r["ly_do_ra"] == "HET_GIO" and r["t_ra"] == du["cb"].dong[13] and gan(r["gia_ra"], gia),
         f"{r['gia_vao']} {r['ly_do_ra']} {D.chuoi_gio(r['t_ra'])}")
    nen = [(101, 101.5, 100.5, 101), (100.5, 100.8, 99.5, 100.2), (100.2, 104.5, 100.1, 104.2)] + [phang] * 5
    du = du_gia("ETH", nen)
    r = D.mo_phong_lenh("ETH", "LONG", "hoi", du["cb"].dong[0], 100.0, 98.0, None, 104.0, 48, du, kl)
    lai = kl * 4 - kl * 104 * F_TP - kl * 100 * F_VAO
    kiem(5, "Hồi LONG: TP duy nhất 100% (ly_do TP), không TP1", r["ly_do_ra"] == "TP" and r["t_tp1"] is None
         and gan(r["lai_usd"], lai), f"{r['ly_do_ra']} {r['lai_usd']}")
    # 5k: dừng 120h lệnh chính; hết kỳ
    du, r = chay_short([khop])
    kiem(5, "Lệnh chính dừng 120h = close nến khớp+30", r["ly_do_ra"] == "HET_GIO" and r["t_ra"] == du["cb"].dong[31],
         D.chuoi_gio(r["t_ra"]))
    du, r = chay_short([khop], ket_thuc=None)
    du2 = du_gia("BTC", [(99, 99.5, 98.5, 99), khop] + [phang] * 40)
    r = D.mo_phong_lenh("BTC", -1, "chinh", du2["cb"].dong[0], 100.0, 102.0, 98.0, 95.0, 120, du2, kl,
                        ket_thuc=du2["cb"].dong[4])
    kiem(5, "Hết kỳ → HET_KY ở close nến cuối kỳ (+trượt)", r["ly_do_ra"] == "HET_KY" and r["t_ra"] == du2["cb"].dong[4]
         and gan(r["gia_ra"], 99.0 * (1 + TR)))


# ============================ NHÓM 1: cắt cụt ============================
COT_QD = ["ts", "tai_san", "pha", "view", "kieu", "ly_do", "hanh_dong", "vung", "ly_do_bo"]
COT_DAT = ["tai_san", "loai", "chieu", "t_quyet_dinh", "gia_dat", "sl", "tp1", "tp2", "khoi_luong", "don_bay", "vung"]


def nhom1(du6, day_du):
    rng = random.Random(20261031)                  # hạt giống cố định
    sai_tong = []
    for lan in range(20):
        nam = [2024, 2025, 2026][lan % 3]
        bd, kt = D.ky_chay(nam)
        T = rng.randint(bd + 14 * 86400, kt - 3600)      # giây bất kỳ (không cần tròn nến)
        cut = D.chay(D.TAI_SAN, nam, du_lieu=du6, cat_tai=T)
        full = day_du[nam]
        t_cuoi = cut.von[-1][0]                    # nến đóng cuối cùng ≤ T trong bản cắt
        sai = []
        if any(q["ts"] > T for q in cut.quyet_dinh) or any(t > T for t, _ in cut.von):
            sai.append("ban_cat_co_moc_sau_T")
        qa = [tuple(q[c] for c in COT_QD) for q in full.quyet_dinh if q["ts"] <= t_cuoi]
        qb = [tuple(q[c] for c in COT_QD) for q in cut.quyet_dinh]
        if qa != qb:
            sai.append(f"quyet_dinh ({len(qa)} vs {len(qb)})")
        la = [tuple(r.get(c) for c in COT_DAT) for r in full.lenh if r["t_quyet_dinh"] <= t_cuoi]
        lb = [tuple(r.get(c) for c in COT_DAT) for r in cut.lenh]
        if la != lb:
            sai.append(f"lenh_dat ({len(la)} vs {len(lb)})")
        bo = {"su_kien"}
        xong_a = [{c: v for c, v in r.items() if c not in bo} for r in full.lenh
                  if r["t_quyet_dinh"] <= t_cuoi and r["t_ra"] <= t_cuoi]
        xong_b = [{c: v for c, v in r.items() if c not in bo} for r in cut.lenh if r["t_ra"] is not None]
        if xong_a != xong_b:
            sai.append(f"lenh_xong ({len(xong_a)} vs {len(xong_b)})")
        # lệnh còn dở ở bản cắt (DANG_CHO / DANG_MO) = lệnh bản đủ chưa xong tới t_cuoi, cùng trạng thái khớp
        mo_a = [(r["t_quyet_dinh"], r["tai_san"], r["t_khop"] if (r["t_khop"] or 1e18) <= t_cuoi else None,
                 r["t_tp1"] if (r["t_tp1"] or 1e18) <= t_cuoi else None)
                for r in full.lenh if r["t_quyet_dinh"] <= t_cuoi and r["t_ra"] > t_cuoi]
        mo_b = [(r["t_quyet_dinh"], r["tai_san"], r["t_khop"], r["t_tp1"]) for r in cut.lenh if r["t_ra"] is None]
        if mo_a != mo_b or any(r["ly_do_ra"] not in ("DANG_CHO", "DANG_MO") for r in cut.lenh if r["t_ra"] is None):
            sai.append(f"lenh_dang_do ({len(mo_a)} vs {len(mo_b)})")
        va = [(t, v, vc) for (t, v), (_, vc) in zip(full.von, full.von_chot) if t <= t_cuoi]
        vb = [(t, v, vc) for (t, v), (_, vc) in zip(cut.von, cut.von_chot)]
        if va != vb:
            sai.append("von")
        if sai:
            sai_tong.append(f"{nam} T={D.chuoi_gio(T)}: {sai}")
        kiem(1, f"Cắt cụt #{lan + 1:02d} {nam} T={D.chuoi_gio(T)} ({len(qb)} quyết định, {len(lb)} lệnh, "
                f"{len(xong_b)} xong, {len(mo_b)} dở dang)", not sai, "; ".join(sai))
    # view_tai tự cắt dữ liệu tại T = view của bản đủ ở nến H4 đóng cuối ≤ T
    sai = []
    cb = du6["BTC"]["cb"]
    for _ in range(20):
        T = rng.randint(ts("2024-01-01 00:00"), ts("2026-10-30 23:00"))
        v = D.view_tai("BTC", T, du6["BTC"])
        k = bisect.bisect_right(cb.dong, T) - 1
        if (v["view"], v["pha"], v["ly_do"], v["gio_cat_ts"]) != (cb.view[k], cb.pha[k], cb.ly_do[k], cb.dong[k]):
            sai.append(D.chuoi_gio(T))
    kiem(1, "view_tai(BTC, T) cắt dữ liệu = view bản đủ (20 mốc)", not sai, str(sai))


# ============================ NHÓM 4: cộng lại + ràng buộc ============================
def _f(s):
    return float(s) if s not in ("", None) else None


def kiem_thu_muc(tm, du6, nhan):
    lenh = list(csv.DictReader(open(tm / "lenh.csv")))
    von = list(csv.DictReader(open(tm / "von.csv")))
    v0 = D.P["von_dau"]
    tong = sum(_f(r["lai_usd"]) for r in lenh)
    v_cuoi = _f(von[-1]["von_chot"])
    kiem(4, f"{nhan}: von cuối {v_cuoi:.2f} = 4000 + Σ lai_usd lenh.csv ({v0 + tong:.2f})",
         abs(v_cuoi - (v0 + tong)) <= 0.01 and abs(_f(von[-1]["von"]) - v_cuoi) <= 0.01)
    # mọi dòng von.csv không có vị thế mở: von = von_chot = 4000 + Σ lai_usd các lệnh đã ra (t_ra ≤ ts)
    ra = sorted((r["t_ra"], _f(r["lai_usd"])) for r in lenh)
    sai, j, cong = 0, 0, v0
    for v in von:
        while j < len(ra) and ra[j][0] <= v["ts_utc"]:
            cong += ra[j][1]
            j += 1
        if v["so_vi_the_mo"] == "0" and (abs(_f(v["von"]) - cong) > 0.01 or abs(_f(v["von_chot"]) - cong) > 0.01):
            sai += 1
    kiem(4, f"{nhan}: {sum(v['so_vi_the_mo'] == '0' for v in von)} dòng von.csv không vị thế mở = 4000 + Σ lãi lệnh đã ra",
         sai == 0, f"{sai} dòng lệch")
    # von_sau của lệnh ra cuối cùng = von cuối
    khop = [r for r in lenh if r["ly_do_ra"] != "HUY"]
    # tự tính lại lãi + phí từng lệnh từ giá
    F_VAO, F_TP, F_MK, TR = D.P["phi_vao"], D.P["phi_tp"], D.P["phi_market"], D.P["truot"]
    sai_lai, sai_phi = [], []
    for r in khop:
        x = 1 if r["chieu"] == "LONG" else -1
        kl, vao, gra, tl = _f(r["khoi_luong"]), _f(r["gia_vao"]), _f(r["gia_ra"]), _f(r["ti_le_tp1"])
        lai = -_f(r["phi"])
        lai += kl * tl * (_f(r["gia_tp1"]) - vao) * x if tl else 0.0
        lai += kl * (1 - tl) * (gra - vao) * x
        if abs(lai - _f(r["lai_usd"])) > 0.01:
            sai_lai.append(r["t_quyet_dinh"])
        phi_ra = F_TP if r["ly_do_ra"] in ("TP", "TP2") else F_MK
        phi = kl * vao * F_VAO + (kl * tl * _f(r["gia_tp1"]) * F_TP if tl else 0.0) + kl * (1 - tl) * gra * phi_ra
        if abs(phi - _f(r["phi"])) > 0.01:
            sai_phi.append(r["t_quyet_dinh"])
        if abs(_f(r["R"]) - _f(r["lai_usd"]) / _f(r["rui_ro_usd"])) > 1e-6:
            sai_lai.append("R@" + r["t_quyet_dinh"])
    kiem(4, f"{nhan}: tự tính lại lãi từng lệnh (kl × chênh giá − phí) khớp 0,01$ ({len(khop)} lệnh)", not sai_lai, str(sai_lai[:5]))
    kiem(4, f"{nhan}: tự tính lại phí từng lệnh (vào 0,02%, TP 0,02%, market 0,05%)", not sai_phi, str(sai_phi[:5]))
    # trượt giá: lệnh ra market có giá ra = mức × (1 ∓ 0,02%) — kiểm SL (không gap): gia_ra ≈ sl × (1 − x·0,02%) hoặc
    # mở nến trước đó; ở đây kiểm SL hoà vốn sau TP1: gia_ra = gia_vao × (1 − x·trượt) khi không gap
    # ràng buộc lệnh
    sai_rb = []
    for r in lenh:
        x = 1 if r["chieu"] == "LONG" else -1
        ma, dat, sl = r["tai_san"], _f(r["gia_dat"]), _f(r["sl"])
        sp = abs(dat - sl) / dat
        if sp < D.P["sl_min"][ma] - 1e-12 or sp > D.P["sl_max"] + 1e-12 or (sl - dat) * x >= 0:
            sai_rb.append(f"SL% {ma} {r['t_quyet_dinh']}")
        tp2 = _f(r["tp2"])
        rr = (tp2 - dat) * x / abs(dat - sl)
        if r["loai"] == "chinh":
            tp1 = _f(r["tp1"])
            if rr < D.P["tp2_min_R"] - 1e-9 or (tp1 - dat) * x / abs(dat - sl) < D.P["tp1_min_R"] - 1e-9 or (tp1 - tp2) * x >= 0:
                sai_rb.append(f"TP {ma} {r['t_quyet_dinh']}")
        elif rr < D.P["hoi_tp_min_R"] - 1e-9:
            sai_rb.append(f"TP hoi {ma} {r['t_quyet_dinh']}")
        cb = du6[ma]["cb"]
        k = cb.chi_so[ts(r["t_quyet_dinh"])]
        f = cb.chi_so[ts(r["t_khop"])] if r["t_khop"] else None
        if f is not None:
            if not (k < f <= k + D.P["so_nen_hieu_luc"]):
                sai_rb.append(f"khop_ngoai_6_nen {ma} {r['t_quyet_dinh']}")
            if (cb.h[f] < dat) if x < 0 else (cb.l[f] > dat):
                sai_rb.append(f"nen_khop_khong_cham {ma} {r['t_quyet_dinh']}")
            for j in range(k + 1, f):
                if (cb.h[j] >= dat) if x < 0 else (cb.l[j] <= dat):
                    sai_rb.append(f"le_ra_khop_som {ma} {r['t_quyet_dinh']}")
    kiem(4, f"{nhan}: ràng buộc lệnh (SL min/≤6%, TP2 ≥ 2R, TP1 ≥ 0,5R, hồi ≥ 1,5R, khớp trong 6 nến, không khớp sớm)",
         not sai_rb, str(sai_rb[:5]))
    # ≤ 3 lệnh chiếm chỗ cùng lúc trên rổ, ≤ 1 / tài sản (khoảng [t_quyet_dinh, t_ra))
    su = []
    for r in lenh:
        su.append((r["t_ra"], 0, r["tai_san"]))
        su.append((r["t_quyet_dinh"], 1, r["tai_san"]))
    su.sort()
    dang, theo, vuot = 0, {}, []
    for t, loai, ma in su:
        if loai == 0:
            dang -= 1
            theo[ma] -= 1
        else:
            dang += 1
            theo[ma] = theo.get(ma, 0) + 1
            if dang > D.P["toi_da_lenh"] or theo[ma] > 1:
                vuot.append(f"{t} {ma}")
    kiem(4, f"{nhan}: ≤ 3 lệnh (chờ + mở) cùng lúc trên rổ, ≤ 1 mỗi tài sản", not vuot, str(vuot[:5]))


def nhom4(du6, day_du):
    for nam, kq in day_du.items():
        kiem(4, f"chạy đủ {nam}: mọi lệnh đều đã kết thúc (không DANG_CHO/DANG_MO), có t_ra",
             all(r["t_ra"] is not None and r["ly_do_ra"] in ("TP2", "TP", "SL", "SL_HOA_VON", "HET_GIO", "HET_KY", "HUY")
                 for r in kq.lenh))
    with tempfile.TemporaryDirectory() as tm:
        for nam, kq in day_du.items():
            D.ghi_ket_qua(kq, Path(tm) / f"{nam}_6")
            kiem_thu_muc(Path(tm) / f"{nam}_6", du6, f"chạy mới {nam} rổ 6")
    tm_kq = GOC / "ket_qua"
    if tm_kq.exists():
        for tm in sorted(p for p in tm_kq.iterdir() if (p / "lenh.csv").exists()):
            kiem_thu_muc(tm, du6, f"ket_qua/{tm.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--du-lieu", default=None)
    a = ap.parse_args()
    print("== Nhóm 3: chỉ báo vs tính tay ==")
    nhom3()
    print("== Nhóm 5: tình huống khớp lệnh TK 7 ==")
    nhom5()
    du6 = D.nap_ro(D.TAI_SAN, a.du_lieu)
    print("== Nhóm 2: nhân quả (ca dựng tay + đổi tương lai) ==")
    nhom2(du6["BTC"])
    day_du = {nam: D.chay(D.TAI_SAN, nam, du_lieu=du6) for nam in (2024, 2025, 2026)}
    print("== Nhóm 1: cắt cụt 20 mốc ==")
    nhom1(du6, day_du)
    print("== Nhóm 4: cộng lại lãi/lỗ + ràng buộc ==")
    nhom4(du6, day_du)
    n_ok = sum(1 for k in KQ if k[2])
    print(f"\nTỔNG: {n_ok}/{len(KQ)} PASS" + ("" if n_ok == len(KQ) else "  ← CÓ FAIL"))
    for nhom in (1, 2, 3, 4, 5):
        ds = [k for k in KQ if k[0] == nhom]
        print(f"  Nhóm {nhom}: {sum(k[2] for k in ds)}/{len(ds)}")
    sys.exit(0 if n_ok == len(KQ) else 1)


if __name__ == "__main__":
    main()
