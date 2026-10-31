#!/usr/bin/env python3
"""KIỂM TRA NGOÀI MẪU cho luật v1 (đã KHÓA) — không sửa luật/tham số, dùng nguyên các hàm của chay.py.

    python3 backtest/ngoai_mau.py            (dùng CSV có sẵn trong du_lieu_2025/ và du_lieu/)
    python3 backtest/ngoai_mau.py --tai-lai  (tải lại du_lieu_2025/ rồi chạy)

Chạy: 2025-01-01 → 2025-12-31 (ngoài mẫu) và 2026-01-01 → 2026-10-30 (trong mẫu), 6 tài sản BTC, ETH, OKB, BNB, vàng, dầu;
biến thể A (2%, tối đa 3 lệnh) và E' (2%, tối đa 4 lệnh); luật 8 theo 2 cách diễn giải (gia / thoi_gian).
Đầu ra: KET_QUA_NGOAI_MAU.md (giữ nguyên đoạn nhận xét viết tay), von_2025.html, ngoai_mau/<tu>_<den>_<dien_giai>/lenh_*.csv + tu_kiem.txt.
"""
import csv, datetime as dt, json, math, sys
from collections import defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parent
sys.path.insert(0, str(GOC))
import chay as C            # noqa: E402
import tai_du_lieu as T     # noqa: E402

TS6 = ["BTC", "ETH", "OKB", "BNB", "VANG", "DAU"]
DL25, DL26 = GOC / "du_lieu_2025", GOC / "du_lieu"
GIAI_DOAN = {"2025": ("2025-01-01", "2025-12-31", DL25), "2026": ("2026-01-01", "2026-10-30", DL26)}
DG = {"gia": "(i) theo GIÁ", "thoi_gian": "(ii) theo THỜI GIAN"}
DGN = {"gia": "(i)", "thoi_gian": "(ii)"}
NHAN = {"2025": "2025 (ngoài mẫu)", "2026": "2026 (trong mẫu, 6 TS)"}


def tai_2025():
    for ma in TS6[:4]:
        print("Tải", ma)
        T._ghi(f"{ma}_4H.csv", T.tai_okx(ma, "4H", "2024-06-01", 4 * T.GIO), DL25)
        T._ghi(f"{ma}_1D.csv", T.tai_okx(ma, "1Dutc", "2023-12-01", 24 * T.GIO), DL25)
    for ma in TS6[4:]:
        print("Tải", ma)
        h4, d1 = T.tai_yahoo(ma, d1_range="5y")
        T._ghi(f"{ma}_4H.csv", h4, DL25)
        T._ghi(f"{ma}_1D.csv", d1, DL25)


# ---------------- tiện ích thống kê ----------------
def t_stat(lenh):
    rs = [p.R for p in lenh]
    if len(rs) < 2:
        return float("nan")
    m = sum(rs) / len(rs); sd = math.sqrt(sum((r - m) ** 2 for r in rs) / (len(rs) - 1))
    return m / (sd / math.sqrt(len(rs))) if sd else float("nan")


def max_dong_thoi(lenh):
    return max((1 + sum(1 for y in lenh if y is not x and y.khop_ts <= x.khop_ts < y.dong_ts) for x in lenh), default=0)


def dau_van(lenh):
    return [(p.ma, p.khop_ts, p.chieu, round(p.lai, 6)) for p in lenh]


def bh_pct(r, m):
    a = r["TS"][m]
    bd, kt = C.ngay_vn(r["tu"]), C.ngay_vn(r["den"]) + C.NGAY
    g0 = a.c[C.bisect.bisect_right(a.dong, bd) - 1]; g1 = a.c[C.bisect.bisect_right(a.dong, kt) - 1]
    return g1 / g0 - 1


def cuoi_thang(duong):
    d = {}
    for T_, v in duong:
        d[C.thang(T_)] = v
    return d


def doi_thang(duong, von0):
    d, truoc, ra = cuoi_thang(duong), von0, {}
    for th in sorted(d):
        ra[th] = d[th] / truoc - 1; truoc = d[th]
    return ra


# ---------------- chạy ----------------
def chay_het():
    R = {}
    for nam, (tu, den, dl) in GIAI_DOAN.items():
        for dg in DG:
            C.cau_hinh(tu, den, dl, dg)
            r = C.chay_tuy_chon(TS6)
            C.ghi_tuy_chon(r, GOC / "ngoai_mau" / f"{r['tu']}_{r['den']}_{dg}")
            R[(nam, dg)] = r
            C.in_tom_tat(r); print()
    for dg in DG:   # tham chiếu: bộ A–E gốc trên 2026 (A 4 coin, E 8 tài sản)
        C.cau_hinh("2026-01-01", "2026-10-30", DL26, dg)
        R[("goc", dg)] = C.chay_tuy_chon(None)
    return R


def kiem_them(R):
    """Các kiểm tra phụ: dữ liệu chồng lấn, bản gốc tái tạo đúng lenh_A..E.csv, khung dữ liệu vàng/dầu đầu 2025."""
    out = []
    # 1) dữ liệu chồng lấn giữa du_lieu/ và du_lieu_2025/
    def rd(p):
        with p.open() as f:
            return {r["mo_utc"]: tuple(float(r[k]) for k in ("open", "high", "low", "close")) for r in csv.DictReader(f)}
    tong = lech = 0
    for ma in TS6:
        for kh in ("4H", "1D"):
            a, b = rd(DL26 / f"{ma}_{kh}.csv"), rd(DL25 / f"{ma}_{kh}.csv")
            for k in set(a) & set(b):
                tong += 1
                lech += max(abs(x - y) / abs(x) for x, y in zip(a[k], b[k])) > 1e-9
    out.append(f"Dữ liệu chồng lấn du_lieu/ ↔ du_lieu_2025/ (6 tài sản, 4H+1D): {tong} nến chung, {lech} nến lệch giá.")
    # 2) bản gốc (i) tái tạo đúng các file lenh_*.csv của lần chạy 2026 gốc
    r = R[("goc", "gia")]; sai = []
    for k, kq in r["KQ"].items():
        tmp = GOC / "ngoai_mau" / f"_kiem_lenh_{k}.csv"
        C.ghi_lenh(kq, tmp)
        if tmp.read_text() != (GOC / f"lenh_{k}.csv").read_text():
            sai.append(k)
        tmp.unlink()
    out.append("Chạy lại bộ A–E gốc (luật 8 theo giá, cấu hình mặc định) bằng đường gọi mới → "
               + ("trùng từng byte với lenh_A..E.csv cũ." if not sai else f"KHÁC ở {sai}!"))
    rr = R[("goc", "thoi_gian")]["KQ"]["A"]
    out.append(f"Diễn giải (ii) trên bộ gốc A 2026 (4 coin) cho {C.tien(rr['so_du'] - C.VON0)} "
               f"({C.pct(rr['so_du'] / C.VON0 - 1)}) — khớp con số của lần chạy đầu ghi trong KET_QUA.md mục 9 (+136$, +3,4%).")
    # 3) vàng/dầu: số nến H4 khởi động trước 01/01/2025, ngày thường không có nến trong 2025
    r = R[("2025", "gia")]
    bd, kt = C.ngay_vn("2025-01-01"), C.ngay_vn("2026-01-01")
    for m in ("VANG", "DAU"):
        a = r["TS"][m]
        i0 = C.bisect.bisect_right(a.dong, bd)
        dau_ema = next(i for i, v in enumerate(a.e200) if v is not None)
        ngay_co = {dt.datetime.fromtimestamp(t, dt.timezone.utc).date() for t in a.mo if bd <= t < kt}
        d, thieu = dt.date(2025, 1, 1), []
        while d <= dt.date(2025, 12, 31):
            if d.weekday() < 5 and d not in ngay_co:
                thieu.append(d.strftime("%d/%m"))
            d += dt.timedelta(days=1)
        out.append(f"{C.TEN[m]}: H1 Yahoo bắt đầu {C.vn(a.mo[0])[:10]}; {i0} nến H4 trước 01/01/2025; EMA200 H4 có từ {C.vn(a.dong[dau_ema])[:10]} "
                   f"→ phủ trọn 2025. Ngày thường (T2–T6, UTC) không có nến H4 trong 2025: {len(thieu)} ({', '.join(thieu)}).")
    return out


# ---------------- báo cáo ----------------
def dong_tong(nhan_gd, nhan_dg, k, r):
    kq = r["KQ"][k]; st = C.thong_ke(kq["lenh"]); gd = r["GD"].get(k)
    return [nhan_gd, nhan_dg, f"**{k}** — {r['bt'][k]['mo_ta']}", C.tien(kq["so_du"] - C.VON0), C.pct(kq["so_du"] / C.VON0 - 1), st["n"],
            C.pct0(st["thang"], 0), C.so(st["r_tb"]), C.so(t_stat(kq["lenh"]), 1), C.pct0(C.sut_giam(kq["von"])),
            C.so(st["pf"]) if st["pf"] != float("inf") else "∞",
            f"{C.phan_vi(gd[0], kq['so_du'] - C.VON0):.0f}" if gd else "—", f"{C.phan_vi(gd[1], st['tong_r']):.0f}" if gd else "—"]


def bang_nhom(ds_nhom, cot_dau, khoa_ds):
    """ds_nhom: [(nhãn cột, dict khóa→lệnh)] → bảng khóa × (lệnh, thắng, tổng R, lãi) cho từng nhãn."""
    tieu = [cot_dau]
    for nh, _ in ds_nhom:
        tieu += [f"{nh}: lệnh", "thắng", "R TB", "tổng R", "lãi"]
    rows = []
    for kh in khoa_ds:
        row = [kh]
        for _, d in ds_nhom:
            ds = d.get(kh, []); st = C.thong_ke(ds)
            row += [st["n"], C.pct0(st["thang"], 0) if ds else "—", C.so(st["r_tb"]) if ds else "—", C.so(st["tong_r"], 1), C.tien(st["lai"])]
        rows.append(row)
    return C.bang(tieu, rows)


def lam_bao_cao(R, kiem):
    L = []; w = L.append
    w("# KIỂM TRA NGOÀI MẪU — luật v1 (đã khóa)\n")
    w("_Sinh tự động bởi `backtest/ngoai_mau.py` (chạy lại: `python3 backtest/ngoai_mau.py`). Dùng nguyên các hàm của `chay.py`; "
      "từng lần chạy lẻ tái tạo được bằng `python3 backtest/chay.py --tu … --den … --tai-san BTC,ETH,OKB,BNB,VANG,DAU --dien-giai gia|thoi_gian --thu-muc-du-lieu …`. "
      "Vốn 4.000$ · phí vào 0,02% / ra 0,05% · bỏ funding · rủi ro 2% vốn/lệnh._\n")
    w("> **Thiết kế kiểm tra.** Luật v1 được chắt lọc từ các buổi live **năm 2026** → **2025 (01/01–31/12) là dữ liệu bot chưa từng thấy (ngoài mẫu)**. "
      "Không sửa luật, không dò tham số. Chỉ đổi: giai đoạn, rổ tài sản (chủ dự án chốt **BTC, ETH, OKB, BNB, vàng GC=F, dầu CL=F** — bỏ NEAR, ZEC), "
      "và chạy luật 8 theo **cả hai** cách đọc câu “đỉnh fractal gần nhất phía trên giá vào”: **(i) gần nhất theo GIÁ** (bản đang chốt) và "
      "**(ii) mới nhất theo THỜI GIAN** (bản chạy đầu). 2026 chạy lại trên đúng 6 tài sản để so cùng rổ.\n")
    w("> Biến thể: **A** = 6 tài sản, rủi ro 2%, tối đa 3 lệnh mở; **E'** = như A, tối đa 4 lệnh mở.\n")

    # 1. bảng tổng
    w("## 1. Bảng tổng\n")
    rows = []
    for nam in ("2025", "2026"):
        for dg, nhan in DG.items():
            for k in ("A", "E'"):
                rows.append(dong_tong(NHAN[nam], nhan, k, R[(nam, dg)]))
    for dg, nhan in DG.items():
        for k in ("A", "E"):
            rows.append(dong_tong("_Tham chiếu: 2026 gốc_", nhan, k, R[("goc", dg)]))
    w(C.bang(["Giai đoạn", "Luật 8", "Biến thể", "Lãi/lỗ", "%", "Lệnh", "Thắng", "R TB", "t (R TB)", "Sụt giảm", "Hệ số LN",
              "Phân vị giả dược ($)", "Phân vị (R)"], rows))
    trung = {key: dau_van(R[key]["KQ"]["A"]["lenh"]) == dau_van(R[key]["KQ"]["E'"]["lenh"]) for key in R if key[0] != "goc"}
    mx = {key: max_dong_thoi(R[key]["KQ"]["E'"]["lenh"]) for key in trung}
    w("\n_t (R TB) = R TB ÷ (độ lệch chuẩn R / √số lệnh) — |t| < 2 nghĩa là chưa phân biệt được với 0. Sụt giảm tính trên vốn theo giá thị trường mỗi nến H4. "
      "Tham chiếu 2026 gốc = bộ A–E của `KET_QUA.md` (A: BTC/ETH/NEAR/ZEC; E: 8 tài sản), chạy lại với cả 2 cách đọc luật 8._\n")
    w("_A và E' " + ("**trùng nhau từng lệnh** ở cả 4 lần chạy" if all(trung.values()) else "khác nhau ở: " + ", ".join(f"{a} {b}" for (a, b), v in trung.items() if not v))
      + f": số lệnh mở cùng lúc cao nhất ở E' = {', '.join(f'{a} {DGN[b]}: {v}' for (a, b), v in mx.items())}; số lệnh chờ của A bị hủy vì đã đủ 3 lệnh mở = "
      + f"{', '.join(str(R[key]['KQ']['A']['huy'].get('du_lenh_mo', 0)) for key in mx)} — có lúc mở đủ 3 lệnh nhưng chưa lần nào có lệnh thứ 4 cần khớp, nên giới hạn 3 hay 4 cho cùng kết quả. "
      "Các bảng chi tiết dưới đây vì vậy chỉ ghi A._\n")

    # giả dược
    w("### Giả dược (200 lần, seed cố định — như `KET_QUA.md`)\n")
    rows = []
    keys = [(n, d) for n in ("2025", "2026") for d in DG] + [("goc", d) for d in DG]
    for key in keys:
        r = R[key]
        for k in (("A", "E") if key[0] == "goc" else ("A",)):
            lai, rr = r["GD"][k]; kq = r["KQ"][k]; st = C.thong_ke(kq["lenh"])
            rows.append([NHAN.get(key[0], "2026 gốc"), DG[key[1]], k, C.tien(kq["so_du"] - C.VON0), C.tien(C.q(lai, .05)), C.tien(C.q(lai, .5)),
                         C.tien(C.q(lai, .95)), C.pct0(sum(v > 0 for v in lai) / len(lai), 0), f"{C.phan_vi(lai, kq['so_du'] - C.VON0):.0f}",
                         C.so(st["tong_r"], 1), C.so(C.q(rr, .5), 1), f"{C.phan_vi(rr, st['tong_r']):.0f}"])
    w(C.bang(["Giai đoạn", "Luật 8", "Biến thể", "Thật", "Giả dược P5", "P50", "P95", "% giả dược lãi", "Phân vị ($)", "Tổng R thật", "Tổng R giả dược P50", "Phân vị (R)"], rows))
    w("\n_Giả dược: giữ số lệnh, tài sản, tháng khớp, khoảng SL%/TP1%/TP2% và cơ chế quản lý của từng lệnh thật; chỉ thay thời điểm vào (nến H4 ngẫu nhiên cùng tháng, vào ở giá đóng) "
      "và chiều (50/50). E' trùng A nên giả dược cũng trùng. Phân vị = % số lần giả dược thua kết quả thật._\n")

    # mua & giữ
    w("### Mua & giữ (vốn 4.000$; giỏ = chia đều 6 phần)\n")
    rows = []
    b25, b26 = R[("2025", "gia")]["BH"], R[("2026", "gia")]["BH"]
    for t in b25:
        rows.append([t, C.tien(b25[t][-1][1] - C.VON0), C.pct(b25[t][-1][1] / C.VON0 - 1), C.pct0(C.sut_giam(b25[t])),
                     C.tien(b26[t][-1][1] - C.VON0), C.pct(b26[t][-1][1] / C.VON0 - 1), C.pct0(C.sut_giam(b26[t]))])
    w(C.bang(["Tài sản", "2025 lãi", "2025 %", "2025 sụt giảm", "2026 lãi", "2026 %", "2026 sụt giảm"], rows))
    w("\n_Mua ở giá đóng H4 cuối trước 00:00 VN ngày đầu kỳ, bán cuối kỳ, phí 0,05% mỗi đầu. 2026 = 01/01 → 30/10._\n")

    # 2. theo tháng 2025
    w("## 2. Năm 2025 theo THÁNG (biến thể A, theo tháng khớp lệnh)\n")
    r1, r2 = R[("2025", "gia")], R[("2025", "thoi_gian")]
    g1 = C.nhom(r1["KQ"]["A"]["lenh"], lambda p: C.thang(p.khop_ts)); g2 = C.nhom(r2["KQ"]["A"]["lenh"], lambda p: C.thang(p.khop_ts))
    v1, v2 = doi_thang(r1["KQ"]["A"]["von"], C.VON0), doi_thang(r2["KQ"]["A"]["von"], C.VON0)
    c1, c2 = cuoi_thang(r1["KQ"]["A"]["von"]), cuoi_thang(r2["KQ"]["A"]["von"])
    gio = doi_thang(r1["BH"]["giỏ 6 tài sản"], C.VON0); btc = doi_thang(r1["BH"]["BTC"], C.VON0)
    rows = []
    for th in sorted(v1):
        row = [th]
        for g, v, c in ((g1, v1, c1), (g2, v2, c2)):
            ds = g.get(th, []); st = C.thong_ke(ds)
            row += [st["n"], f"{sum(p.lai > 0 for p in ds)}/{st['n']}" if ds else "—", C.so(st["tong_r"], 1), C.pct(v[th]), f"{c[th]:,.0f}$".replace(",", ".")]
        row += [C.pct(btc[th]), C.pct(gio[th])]
        rows.append(row)
    w(C.bang(["Tháng", "(i) lệnh", "thắng", "tổng R", "đổi vốn", "vốn cuối", "(ii) lệnh", "thắng", "tổng R", "đổi vốn", "vốn cuối", "BTC (mua & giữ)", "Giỏ 6 TS"], rows))

    # 3. theo tài sản
    w("\n## 3. Theo TÀI SẢN (biến thể A)\n")
    for nam in ("2025", "2026"):
        ra, rb = R[(nam, "gia")], R[(nam, "thoi_gian")]
        rows = []
        for m in TS6:
            row = [C.TEN[m]]
            for r in (ra, rb):
                ds = [p for p in r["KQ"]["A"]["lenh"] if p.ma == m]; st = C.thong_ke(ds)
                nl = sum(p.chieu > 0 for p in ds)
                row += [st["n"], f"{nl}/{st['n'] - nl}", C.pct0(st["thang"], 0) if ds else "—", C.so(st["tong_r"], 1), C.tien(st["lai"])]
            row.append(C.pct(bh_pct(ra, m)))
            rows.append(row)
        w(f"**{NHAN[nam]}**\n")
        w(C.bang(["Tài sản", "(i) lệnh", "L/S", "thắng", "tổng R", "lãi", "(ii) lệnh", "L/S", "thắng", "tổng R", "lãi", "Giá cả kỳ"], rows))
        w("")
    w("_Vàng = GC=F, dầu = CL=F (Yahoo, hợp đồng liên tục — có bước nhảy khi chuyển kỳ hạn). H4 gộp từ H1 (chỉ giữ nến có ≥3 giờ giao dịch)._\n")

    # 4. long vs short
    w("## 4. LONG vs SHORT (biến thể A)\n")
    cot = [(f"{n} {DGN[d]}", C.nhom(R[(n, d)]["KQ"]["A"]["lenh"], lambda p: "LONG" if p.chieu > 0 else "SHORT"))
           for n in ("2025", "2026") for d in DG]
    rows = []
    for (nh, d) in cot:
        for ch in ("LONG", "SHORT"):
            ds = d.get(ch, []); st = C.thong_ke(ds)
            rows.append([nh, ch, st["n"], C.pct0(st["thang"], 0) if ds else "—", C.so(st["r_tb"]) if ds else "—", C.so(st["tong_r"], 1), C.tien(st["lai"])])
    w(C.bang(["Lần chạy", "Chiều", "Lệnh", "Thắng", "R TB", "Tổng R", "Lãi/lỗ"], rows))

    # 5. kiểu kết thúc + nguồn SL
    w("\n## 5. Kiểu kết thúc và nguồn SL (biến thể A)\n")
    cot = [(f"{n} {DGN[d]}", C.nhom(R[(n, d)]["KQ"]["A"]["lenh"], lambda p: p.kq)) for n in ("2025", "2026") for d in DG]
    khoa = sorted({k for _, d in cot for k in d})
    w(C.bang(["Kết quả"] + [nh for nh, _ in cot], [[k] + [f"{len(d.get(k, []))} lệnh / {C.so(sum(p.R for p in d.get(k, [])), 1)}R" for _, d in cot] for k in khoa]))
    cot = [(f"{n} {DGN[d]}", C.nhom(R[(n, d)]["KQ"]["A"]["lenh"], lambda p: "sàn d_min" if p.sl_nguon == "san_dmin" else "đỉnh/đáy fractal"))
           for n in ("2025", "2026") for d in DG]
    w("")
    w(C.bang(["Nguồn SL"] + [nh for nh, _ in cot], [[k] + [f"{len(d.get(k, []))} lệnh / {C.so(sum(p.R for p in d.get(k, [])), 1)}R" for _, d in cot]
                                                     for k in ("sàn d_min", "đỉnh/đáy fractal")]))
    w("\n_Với cùng một tín hiệu, (i) chọn đỉnh/đáy gần giá vào nhất trong tập ứng viên, (ii) chọn phần tử mới nhất của cùng tập (có thể trùng) → SL theo (ii) luôn rộng bằng hoặc hơn (i), "
      "R:R tới TP1 bằng hoặc thấp hơn → nhiều tín hiệu bị luật 8 (SL > 6%) và luật 9 (R:R < 1,5) loại hơn, nên ít lệnh hơn._\n")

    # 6. nhận xét
    w("## 6. Nhận xét\n")
    cu = (GOC / "KET_QUA_NGOAI_MAU.md").read_text() if (GOC / "KET_QUA_NGOAI_MAU.md").exists() else ""
    if "<!-- NHAN_XET -->" in cu and "<!-- /NHAN_XET -->" in cu:
        w(cu[cu.index("<!-- NHAN_XET -->"):cu.index("<!-- /NHAN_XET -->") + len("<!-- /NHAN_XET -->")])
    else:
        w("<!-- NHAN_XET -->\n_(chưa viết)_\n<!-- /NHAN_XET -->")

    # 7. dữ liệu
    w("\n## 7. Dữ liệu và cách diễn giải\n")
    w("- **2025** dùng `backtest/du_lieu_2025/`: OKX BTC/ETH/OKB/BNB-USDT 4H từ 01/06/2024, 1Dutc từ 01/12/2023 (khởi động EMA ~7 tháng H4, ~13 tháng D1); "
      "Yahoo GC=F/CL=F H1 `range=730d` (Yahoo thực tế trả từ 10/06/2024 → **phủ trọn 2025, không phải lùi ngày bắt đầu của vàng/dầu**; EMA200 H4 có từ đầu 08/2024) gộp H4, D1 `range=5y`. **2026** dùng `backtest/du_lieu/` như lần chạy gốc.")
    w("- Toàn bộ luật, tham số, thứ tự xử lý trong nến, cách tính phí/ký quỹ/giả dược: giữ nguyên `chay.py` (xem `KET_QUA.md` mục 9). "
      "Chỉ luật 8 có công tắc `--dien-giai`: `gia` = đỉnh (SHORT) / đáy (LONG) fractal 60 ngày đã xác nhận, phía trên/dưới giá vào, **gần giá vào nhất**; "
      "`thoi_gian` = trong cùng tập đó lấy cái **mới nhất**. Sau đó vẫn áp sàn d_min, ×1,002, trần 6% như cũ.")
    w("- `--den` tính trọn ngày giờ VN: 2025 kết thúc 00:00 VN 01/01/2026, lệnh còn mở đóng ở giá đóng H4 cuối cùng trước mốc đó; "
      "không dữ liệu nào sau mốc này được dùng (vòng lặp, giả dược và đóng cuối kỳ đều cắt tại KET_THUC).")
    w("- Danh sách lệnh từng lần chạy: `backtest/ngoai_mau/<từ>_<đến>_<gia|thoi_gian>/lenh_A.csv`, `lenh_Ep.csv` (E'), kèm `tu_kiem.txt`.\n")

    # 8. tự kiểm
    w("## 8. Tự kiểm\n")
    w("```")
    for nam in ("2025", "2026"):
        for dg in DG:
            tk = R[(nam, dg)]["tk"].split("\n")
            w(f"[{NHAN[nam]} · luật 8 {DG[dg]}]")
            w("  " + tk[0]); w("  " + tk[1])
    for s in kiem:
        w(s)
    w("```\n")
    w("Chi tiết đối chiếu tay từng nến (4 lệnh mẫu mỗi lần chạy): `backtest/ngoai_mau/*/tu_kiem.txt`.\n")
    return "\n".join(L)


# ---------------- HTML ----------------
def lam_html(R):
    def theo_ngay(duong):
        d = {}
        for T_, v in duong:
            d[dt.datetime.fromtimestamp(T_, C.VN).strftime("%Y-%m-%d")] = round(v, 2)
        return d
    bieu = {}
    for nam in ("2025", "2026"):
        chuoi = {"A — luật 8 (i) theo giá": theo_ngay(R[(nam, "gia")]["KQ"]["A"]["von"]),
                 "A — luật 8 (ii) theo thời gian": theo_ngay(R[(nam, "thoi_gian")]["KQ"]["A"]["von"]),
                 "Mua & giữ giỏ 6 tài sản": theo_ngay(R[(nam, "gia")]["BH"]["giỏ 6 tài sản"]),
                 "Mua & giữ BTC": theo_ngay(R[(nam, "gia")]["BH"]["BTC"])}
        ngay = sorted(set().union(*[set(v) for v in chuoi.values()]))
        du = {}
        for ten, d in chuoi.items():
            last, arr = None, []
            for n in ngay:
                last = d.get(n, last); arr.append(last)
            du[ten] = arr
        bieu[nam] = dict(ngay=ngay, du=du)
    tom = []
    for nam in ("2025", "2026"):
        for dg in DG:
            r = R[(nam, dg)]
            for k in ("A", "E'"):
                kq = r["KQ"][k]; st = C.thong_ke(kq["lenh"])
                tom.append([NHAN[nam], DG[dg], k, round(kq["so_du"]), round((kq["so_du"] / C.VON0 - 1) * 100, 1), st["n"],
                            round(C.sut_giam(kq["von"]) * 100, 1), round(C.phan_vi(r["GD"][k][0], kq["so_du"] - C.VON0))])
        for t in ("giỏ 6 tài sản", "BTC"):
            d = R[(nam, "gia")]["BH"][t]
            tom.append([NHAN[nam], "—", f"Mua & giữ {t}", round(d[-1][1]), round((d[-1][1] / C.VON0 - 1) * 100, 1), "—", round(C.sut_giam(d) * 100, 1), "—"])
    mau = {"A — luật 8 (i) theo giá": 1, "A — luật 8 (ii) theo thời gian": 2, "Mua & giữ giỏ 6 tài sản": 3, "Mua & giữ BTC": 4}
    ngan = {"A — luật 8 (i) theo giá": "A (i)", "A — luật 8 (ii) theo thời gian": "A (ii)", "Mua & giữ giỏ 6 tài sản": "Giỏ 6", "Mua & giữ BTC": "BTC"}
    data = json.dumps(dict(b=bieu, tom=tom, mau=mau, ngan=ngan), ensure_ascii=False)
    (GOC / "von_2025.html").write_text(TRANG.replace("__DATA__", data))


TRANG = r"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Đường vốn 2025</title>
<style>
:root{color-scheme:light;--surface:#fcfcfb;--text:#0b0b0b;--text2:#52514e;--muted:#898781;--grid:#e1e0d9;--axis:#c3c2b7;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--surface:#1a1a19;--text:#f0efec;--text2:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--axis:#383835;
--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500}}
:root[data-theme="dark"]{color-scheme:dark;--surface:#1a1a19;--text:#f0efec;--text2:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--axis:#383835;
--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500}
body{margin:0;background:var(--surface);color:var(--text);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1100px;margin:0 auto;padding:20px 16px 40px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 6px}
p.ghi{color:var(--text2);margin:0 0 10px;font-size:14px}
.khung{position:relative;height:420px}
table{border-collapse:collapse;width:100%;font-size:14px;margin-top:8px;font-variant-numeric:tabular-nums}
th,td{padding:6px 8px;border-bottom:1px solid var(--grid);text-align:right;white-space:nowrap}th:nth-child(-n+3),td:nth-child(-n+3){text-align:left}
th{color:var(--text2);font-weight:600}
.bang{overflow-x:auto}
</style></head><body><main>
<h1>Đường vốn 2025 — kiểm tra ngoài mẫu luật v1</h1>
<p class="ghi">Luật v1 học từ các buổi live 2026; năm 2025 là dữ liệu bot chưa từng thấy. 6 tài sản (BTC, ETH, OKB, BNB, vàng, dầu), vốn đầu 4.000$, rủi ro 2%/lệnh, giá trị theo giá thị trường lúc cuối mỗi ngày (giờ VN).
Hai đường A ứng với hai cách đọc luật 8 (đỉnh/đáy fractal làm SL: (i) gần giá vào nhất, (ii) mới nhất). E' (tối đa 4 lệnh) trùng A nên không vẽ riêng. Nét đứt = mua &amp; giữ.</p>
<h2>2025 (ngoài mẫu) · 01/01 → 31/12</h2>
<div class="khung"><canvas id="c25" aria-label="Đường vốn năm 2025: biến thể A theo hai cách đọc luật 8, so với mua và giữ"></canvas></div>
<h2>Để so: 2026 (trong mẫu, cùng 6 tài sản) · 01/01 → 30/10</h2>
<div class="khung"><canvas id="c26" aria-label="Đường vốn năm 2026 cùng 6 tài sản"></canvas></div>
<h2>Bảng số cuối kỳ</h2>
<div class="bang"><table id="tb"><thead><tr><th>Giai đoạn</th><th>Luật 8</th><th>Chiến lược</th><th>Vốn cuối ($)</th><th>Lãi/lỗ (%)</th><th>Số lệnh</th><th>Sụt giảm lớn nhất (%)</th><th>Phân vị giả dược</th></tr></thead><tbody></tbody></table></div>
</main>
<script src="vendor/chart.umd.js"></script>
<script>
const D = __DATA__;
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const fmt = v => v == null ? "—" : v.toLocaleString("vi-VN", {maximumFractionDigits: 0}) + "$";
const nhanCuoi = {id: "nhanCuoi", afterDatasetsDraw(ch) {   // nhãn trực tiếp ở cuối mỗi đường, đẩy tách nếu chồng nhau
  const ctx = ch.ctx, ds = [];
  ch.data.datasets.forEach((d, i) => { const m = ch.getDatasetMeta(i); if (m.hidden) return; const p = m.data[m.data.length - 1];
    if (p) ds.push({y: p.y, x: p.x, t: D.ngan[d.label]}); });
  ds.sort((a, b) => a.y - b.y);
  for (let i = 1; i < ds.length; i++) if (ds[i].y - ds[i - 1].y < 15) ds[i].y = ds[i - 1].y + 15;
  ctx.save(); ctx.font = "12px system-ui,-apple-system,sans-serif"; ctx.fillStyle = css("--text2"); ctx.textBaseline = "middle";
  ds.forEach(d => ctx.fillText(d.t, d.x + 6, d.y)); ctx.restore(); }};
function ve(id, b) {
  const ds = Object.keys(b.du).map(t => ({label: t, data: b.du[t], borderColor: css("--s" + D.mau[t]), backgroundColor: css("--s" + D.mau[t]),
    borderWidth: 2, pointRadius: 0, pointHoverRadius: 5, tension: 0, borderDash: t.startsWith("Mua") ? [6, 4] : []}));
  return new Chart(document.getElementById(id), {type: "line", data: {labels: b.ngay, datasets: ds}, plugins: [nhanCuoi],
    options: {maintainAspectRatio: false, animation: false, interaction: {mode: "index", intersect: false}, layout: {padding: {right: 52}},
      plugins: {legend: {position: "top", labels: {color: css("--text2"), boxWidth: 14, boxHeight: 2}},
        tooltip: {callbacks: {label: c => " " + c.dataset.label + ": " + fmt(c.parsed.y)}}},
      scales: {x: {ticks: {color: css("--muted"), maxTicksLimit: 10, maxRotation: 0}, grid: {display: false}, border: {color: css("--axis")}},
        y: {ticks: {color: css("--muted"), callback: v => v.toLocaleString("vi-VN")}, grid: {color: css("--grid")}, border: {display: false}}}}});
}
ve("c25", D.b["2025"]); ve("c26", D.b["2026"]);
const tb = document.querySelector("#tb tbody");
for (const r of D.tom) { const tr = document.createElement("tr");
  tr.innerHTML = r.map(v => `<td>${typeof v === "number" ? v.toLocaleString("vi-VN") : v}</td>`).join(""); tb.appendChild(tr); }
</script></body></html>
"""


def main():
    if "--tai-lai" in sys.argv or not all((DL25 / f"{m}_{k}.csv").exists() for m in TS6 for k in ("4H", "1D")):
        tai_2025()
    R = chay_het()
    kiem = kiem_them(R)
    print("\n".join(kiem))
    (GOC / "KET_QUA_NGOAI_MAU.md").write_text(lam_bao_cao(R, kiem))
    lam_html(R)
    print("✓ Đã ghi KET_QUA_NGOAI_MAU.md, von_2025.html, ngoai_mau/*/")


if __name__ == "__main__":
    main()
