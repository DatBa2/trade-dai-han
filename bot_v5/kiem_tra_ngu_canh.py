#!/usr/bin/env python3
"""Kiểm `bot_v5/ngu_canh.py`.
  (a) CẮT CỤT: hồ sơ tại T với cache đầy đủ == hồ sơ khi
        (a1) XOÁ mọi nến có giờ đóng > T (mọi khung, mọi mã), F&G sau T, Polymarket sau T, kết quả FOMC + thông cáo sau T;
        (a2) ĐẦU ĐỘC mọi dữ liệu sau T (giá ×1,37, vol ×5, F&G = 99, Polymarket = 0,999)
      → Markdown + JSON phải GIỐNG HỆT (chạy offline trên bản sao cache / bản sao du_lieu/tin_tuc).
        (a3) ĐẦU ĐỘC mọi nến/F&G có giờ đóng > T−24h → khối "trạng thái lúc T−24h" phải GIỐNG HỆT (chỉ dùng dữ liệu ≤ T−24h).
  (b) 3 ca: BTC 4H 2026-08-14 11:00 · ETH 1D 2026-10-01 07:00 · SOL 4H 2026-09-21 11:00 → in độ dài + phần đầu.
  (c) EMA/RSI trong hồ sơ khớp `cong_cu/chi_bao.py` tính lại độc lập; nến OKX (nguồn dự phòng) khớp
      `bot_v4/du_lieu/BTC_*.csv`; `trendline_tai` trên nến OKX khớp `trendline.BoDuLieu.doc()` (dữ liệu bot_v4) tại T.
      Hồ sơ BTC dùng Binance perp nên không so thẳng hồ sơ với dữ liệu bot_v4 (OKX).
  (d) phần mới có mặt + tính đúng: trạng thái T−24h (nến H4/D1 đúng mốc, EMA/L01 tính lại độc lập), nhịp GIẢM tuần từ đỉnh
      cao nhất (đỉnh = max râu 104 tuần, đáy = min râu sau đỉnh, mức Fibo), trendline giá đường sau 24h/48h = tại T + dốc×1/×2.
  (e) mục 7 ngoài chart (BTC 4H 2026-08-14): BTC.D / USDT.D = dòng CSV cache cuối có giờ biết ≤ T; mỗi gap CME liệt kê
      tính lại từ CSV thô (mở ≤ T, phần còn lại = râu cực trị sau khi mở, chưa bị đi hết); tại 2026-09-17 gap 01-20
      (92.075–92.730) còn phía trên.
Dùng: python3 bot_v5/kiem_tra_ngu_canh.py [--khong-a]   (lần đầu cần mạng để điền cache; exit 1 nếu có FAIL)
"""
import csv, datetime as dt, json, shutil, sys, tempfile
from pathlib import Path

DAY = Path(__file__).resolve().parent
GOC = DAY.parent
sys.path.insert(0, str(DAY))
sys.path.insert(0, str(GOC / "cong_cu"))
import ngu_canh as NC  # noqa: E402
import nen as NG  # noqa: E402
import chi_bao  # noqa: E402
import tin_tuc  # noqa: E402
import trendline as TL  # noqa: E402

CA = [("BTC", "4H", "2026-08-14 11:00"), ("ETH", "1D", "2026-10-01 07:00"), ("SOL", "4H", "2026-09-21 11:00")]
CA_THEM = [("BTC", "15m", "2026-10-06 03:00"), ("VANG", "4H", "2026-09-21 11:00"), ("ETH", "1W", "2026-09-28 07:00")]
LOI = []


def kiem(dk, ten):
    print(("PASS " if dk else "FAIL ") + ten)
    if not dk:
        LOI.append(ten)


# ---------------- chuẩn bị bản sao dữ liệu ----------------
def _sao_cache(t, kieu, dich):
    """Bản sao cache: kieu='xoa' bỏ nến dong > t; 'doc' đầu độc nến dong > t."""
    dich.mkdir(parents=True, exist_ok=True)
    for p in NG.CACHE_MAC_DINH.iterdir():
        if p.suffix == ".csv":
            with p.open(newline="") as f:
                ds = list(csv.DictReader(f))
            ra = []
            for r in ds:
                if NG.tu_s_utc(r["dong_utc"]) <= t:
                    ra.append(r)
                elif kieu == "doc":
                    r = dict(r)
                    for k in ("open", "high", "low", "close"):
                        r[k] = repr(float(r[k]) * 1.37)
                    r["vol"] = repr(float(r["vol"]) * 5)
                    ra.append(r)
            with (dich / p.name).open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["mo_utc", "dong_utc", "open", "high", "low", "close", "vol"])
                w.writeheader()
                w.writerows(ra)
        elif p.name == "fng.json":
            ds = json.loads(p.read_text(encoding="utf-8"))
            if kieu == "xoa":
                ds = [x for x in ds if x[0] <= t]
            else:
                ds = [x if x[0] <= t else [x[0], 99, "Extreme Greed"] for x in ds]
            (dich / p.name).write_text(json.dumps(ds), encoding="utf-8")
        elif p.is_file():
            shutil.copy(p, dich / p.name)


def _sao_tin(t, kieu, dich):
    """Bản sao du_lieu/tin_tuc: Polymarket / kết quả FOMC / thông cáo sau t bị xoá hoặc đầu độc. Lịch công bố giữ (biết trước)."""
    goc = Path(tin_tuc.THU_MUC)
    (dich / "_goc").mkdir(parents=True, exist_ok=True)
    shutil.copy(goc / "lich_kinh_te_2026.csv", dich / "lich_kinh_te_2026.csv")
    tu = dt.datetime.fromtimestamp(t, NG.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    with (goc / "polymarket_fed.csv").open(newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        cot = rd.fieldnames
        ds = []
        for r in rd:
            if r["ts_utc"] <= tu:
                ds.append(r)
            elif kieu == "doc":
                r["xac_suat"] = "0.999"
                ds.append(r)
    with (dich / "polymarket_fed.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cot)
        w.writeheader()
        w.writerows(ds)

    def qd_ts(ngay):  # giờ quyết định FOMC 14:00 ET
        d = dt.datetime.strptime(ngay, "%Y-%m-%d").replace(hour=14, tzinfo=tin_tuc.ET)
        return d.timestamp()
    with (goc / "fomc_ket_qua_2026.csv").open(newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        cot = rd.fieldnames
        ds = []
        for r in rd:
            if qd_ts(r["ngay_quyet_dinh"]) <= t:
                ds.append(r)
            elif kieu == "doc":
                r.update({"quyet_dinh": "DOC", "thay_doi_bps": "500", "phan_doi": "DOC"})
                ds.append(r)
    with (dich / "fomc_ket_qua_2026.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cot)
        w.writeheader()
        w.writerows(ds)
    for p in (goc / "_goc").glob("fomc_statement_*.html"):
        ngay = p.stem.split("_")[-1]
        if qd_ts(f"{ngay[:4]}-{ngay[4:6]}-{ngay[6:]}") <= t:
            shutil.copy(p, dich / "_goc" / p.name)
        elif kieu == "doc":
            (dich / "_goc" / p.name).write_text("<p>For release at 2:00 p.m. Share The Committee will DOC.</p>", encoding="utf-8")


def _chay(ma, khung, t, cache_dir=None, offline=False, thu_tin=None):
    goc_tin = tin_tuc.THU_MUC
    try:
        if thu_tin:
            tin_tuc.THU_MUC = str(thu_tin)
            tin_tuc._cache.clear()
        hs = NC.tao_ho_so(ma, khung, t, 30, cache_dir, offline)
        return NC.ve_markdown(hs), json.dumps(hs, ensure_ascii=False, sort_keys=True), hs
    finally:
        tin_tuc.THU_MUC = goc_tin
        tin_tuc._cache.clear()


# ---------------- (a) ----------------
def kiem_cat_cut(ds_ca, ket_qua):
    for ma, khung, s in ds_ca:
        t = NC.doc_t(s)
        md0, js0, _hs = ket_qua[(ma, khung, s)]
        for kieu, ten in (("xoa", "XOÁ sau T"), ("doc", "ĐẦU ĐỘC sau T")):
            with tempfile.TemporaryDirectory() as tmp:
                c, tn = Path(tmp) / "cache", Path(tmp) / "tin"
                _sao_cache(t, kieu, c)
                _sao_tin(t, kieu, tn)
                md1, js1, _ = _chay(ma, khung, t, c, True, tn)
            kiem(md0 == md1 and js0 == js1, f"(a) cắt cụt {ten}: {ma} {khung} {s} — Markdown {len(md0)} ký tự + JSON giống hệt")
            if md0 != md1:
                a, b = md0.splitlines(), md1.splitlines()
                for i, (x, y) in enumerate(zip(a, b)):
                    if x != y:
                        print("   khác dòng", i + 1, "\n   ĐỦ :", x[:220], "\n   CẮT:", y[:220])
                        break


def kiem_truoc_24h(ds_ca, ket_qua):
    """(a3) Đầu độc dữ liệu sau T−24h (cả khoảng T−24h → T) → khối truoc_24h không đổi."""
    for ma, khung, s in ds_ca:
        t = NC.doc_t(s)
        _md0, _js0, hs0 = ket_qua[(ma, khung, s)]
        with tempfile.TemporaryDirectory() as tmp:
            c, tn = Path(tmp) / "cache", Path(tmp) / "tin"
            _sao_cache(t - 24 * 3600, "doc", c)
            _sao_tin(t, "xoa", tn)
            _md1, _js1, hs1 = _chay(ma, khung, t, c, True, tn)
        a = json.dumps(hs0["truoc_24h"], ensure_ascii=False, sort_keys=True)
        b = json.dumps(hs1["truoc_24h"], ensure_ascii=False, sort_keys=True)
        kiem(a == b and hs0["truoc_24h"]["h4"] is not None,
             f"(a3) {ma} {khung} {s}: trạng thái T−24h giống hệt khi đầu độc mọi nến đóng > T−24h")


# ---------------- (d) ----------------
def kiem_phan_moi(ma, khung, t, md, hs):
    _n, h4 = NG.lay_chuoi(ma, "4H", t)
    _n, d1 = NG.lay_chuoi(ma, "1D", t)
    tm = t - 24 * 3600
    tr = hs["truoc_24h"]
    x, y = tr["h4"], tr["d1"]
    j = max(i for i, z in enumerate(h4) if z.dong <= tm)
    c = [z.c for z in h4[:j + 1]]; h = [z.h for z in h4[:j + 1]]; l = [z.l for z in h4[:j + 1]]
    e34h, e34l, e89, e200 = chi_bao.ema(h, 34)[-1], chi_bao.ema(l, 34)[-1], chi_bao.ema(c, 89)[-1], chi_bao.ema(c, 200)[-1]
    vt = "TRÊN dải" if c[-1] > e34h else ("DƯỚI dải" if c[-1] < e34l else "TRONG dải")
    k = max(i for i, z in enumerate(d1) if z.dong <= tm)
    ok = (x["nhan"] == h4[j].nhan and h4[j].dong <= tm < (h4[j + 1].dong if j + 1 < len(h4) else t + 1)
          and x["dong"] == c[-1] and x["ema34_high"] == e34h and x["ema34_low"] == e34l and x["ema89"] == e89
          and x["ema200"] == e200 and x["vi_tri_dai_34"] == vt and y["nhan"] == d1[k].nhan and y["c"] == d1[k].c
          and d1[k].dong <= tm and "Trạng thái lúc T−24h" in md)
    kiem(ok, f"(d) {ma} {khung}: T−24h = nến H4 {x['nhan']} ({x['vi_tri_dai_34']}, L01 {x['phan_loai_L01'].split(' (')[0]})"
             f" + D1 {y['nhan']} {y['mau']}; EMA tính lại khớp; có trong Markdown")
    ng = hs.get("fibo_tuan_nhip_giam")
    _n, w1 = NG.lay_chuoi(ma, "1W", t)
    ds = w1[-104:]
    imax = max(range(len(ds)), key=lambda i: (ds[i].h, -i))
    if imax == len(ds) - 1:
        ok = ng["den"] is None
    else:
        lo = min(z.l for z in ds[imax + 1:])
        hi = ds[imax].h
        ok = (ng["tu"]["gia"] == hi and ng["den"]["gia"] == lo and ng["tu"]["nhan"] == ds[imax].nhan
              and all(abs(m["gia"] - (lo + (hi - lo) * m["ty_le"])) < 1e-9 * hi for m in ng["muc"])
              and [m["ty_le"] for m in ng["muc"]] == [0.236, 0.382, 0.5, 0.618] and "nhịp GIẢM từ đỉnh cao nhất" in md)
    kiem(ok, f"(d) {ma} {khung}: nhịp GIẢM tuần {ng['tu']['gia']:.6g} ({ng['tu']['nhan']}) → "
             f"{(ng['den'] or {}).get('gia', 0):.6g} ({(ng['den'] or {}).get('nhan', '—')}) đúng max râu / min râu sau đỉnh + Fibo")
    tl = hs["trendline"]
    dem, ok = 0, "loi" not in tl
    for g in tl.get("nhom", []):
        for r in g["duong"]:
            dem += 1
            ok = ok and abs(r["gia_sau_24h"] - (r["gia_tai_T"] + r["doc_moi_ngay"])) < 1e-9 * abs(r["gia_tai_T"]) \
                and abs(r["gia_sau_48h"] - (r["gia_tai_T"] + 2 * r["doc_moi_ngay"])) < 1e-9 * abs(r["gia_tai_T"])
    kiem(ok and dem > 0 and md.count("đường sau 24h") == dem,
         f"(d) {ma} {khung}: {dem} trendline có giá đường sau 24h/48h = tại T + dốc×1/×2, đủ trong Markdown")


# ---------------- (c) ----------------
def kiem_ema(hs, ma, khung, t):
    for m in hs["khung_ds"]:
        if "thieu" in m:
            continue
        _n, ds = NG.lay_chuoi(ma, m["khung"], t)
        c = [x.c for x in ds]; h = [x.h for x in ds]; l = [x.l for x in ds]
        e = m["chi_bao"]["ema"]
        ok = (e["ema34"].get("high") == chi_bao.ema(h, 34)[-1] and e["ema34"].get("low") == chi_bao.ema(l, 34)[-1]
              and e["ema34"].get("close") == chi_bao.ema(c, 34)[-1] and e["ema89"]["gia"] == chi_bao.ema(c, 89)[-1]
              and e["ema200"]["gia"] == chi_bao.ema(c, 200)[-1] and e["ema610"]["gia"] == chi_bao.ema(c, 610)[-1]
              and m["chi_bao"]["rsi14"] == chi_bao.rsi_wilder(c, 14)[-1]
              and [r["rsi14"] for r in m["bang"]] == chi_bao.rsi_wilder(c, 14)[-len(m["bang"]):]
              and m["chi_bao"]["gia_dong"] == c[-1] and ds[-1].dong <= t)
        kiem(ok, f"(c) {ma} {m['khung']}: EMA34 dải/89/200/610 + RSI14 trong hồ sơ == chi_bao.py tính lại; nến cuối đóng ≤ T")


def kiem_bot_v4(t):
    """BTC: nến OKX (nguồn dự phòng) tải về == bot_v4/du_lieu."""
    for khung, ten in (("4H", "BTC_4H.csv"), ("1D", "BTC_1D.csv")):
        _n, ds = NG._chuoi_okx("BTC", khung, t, NG.CACHE_MAC_DINH, False)
        dur = NG.GIAY[khung]
        v4 = {}
        with (GOC / "bot_v4" / "du_lieu" / ten).open(newline="") as f:
            for r in csv.DictReader(f):
                mo = NG.tu_s_utc(r["ts_utc"])
                if mo + dur <= t:
                    v4[mo] = (float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"]))
        chung = [x for x in ds if x.mo in v4]
        lech = sum(1 for x in chung if (x.o, x.h, x.l, x.c) != v4[x.mo])
        kiem(len(chung) > 100 and lech == 0, f"(c) BTC {khung}: {len(chung)} nến OKX trùng giờ với bot_v4/du_lieu, lệch OHLC {lech}")


def kiem_trendline(t):
    tl = NC.trendline_tai(NG._chuoi_okx("BTC", "4H", t, NG.CACHE_MAC_DINH, False)[1],
                          NG._chuoi_okx("BTC", "1D", t, NG.CACHE_MAC_DINH, False)[1], t)
    du = TL.BoDuLieu.doc()
    bt = TL.bien_the(tl["bien_the"])
    kq = TL.tai_thoi_diem(du, t, bt)
    ok = True
    for g in tl["nhom"]:
        v = kq[(g["khung"], g["loai"])]
        id5 = sorted(r["id"] for r in g["duong"])
        c5 = next((r["id"] for r in g["duong"] if r["chinh"]), None)
        c4 = v["chinh"]["id"] if v["chinh"] else None
        ids4 = {r["id"] for r in v["duong"]}
        if c5 != c4 or g["so_duong"] != len(v["duong"]) or not set(id5) <= ids4:
            ok = False
            print(f"     {g['khung']} {g['loai']}: chính v5 {c5} / v4 {c4}; số đường {g['so_duong']} / {len(v['duong'])}")
    kiem(ok, f"(c) trendline BTC tại T: đường chính + số đường còn hiệu lực khớp trendline.BoDuLieu.doc() (biến thể {tl['bien_the']})")


def kiem_ngoai_chart(hs, t):
    def doc(ten):
        with (NG.CACHE_MAC_DINH / ten).open(newline="") as f:
            return [(NG.tu_s_utc(r["mo_utc"]), NG.tu_s_utc(r["dong_utc"]), float(r["open"]), float(r["high"]),
                     float(r["low"]), float(r["close"])) for r in csv.DictReader(f)]
    for k, ten in (("BTC.D", "cmc_BTCD_1D.csv"), ("USDT.D", "cmc_USDTD_1D.csv")):
        cuoi = max((r for r in doc(ten) if r[1] <= t), key=lambda r: r[1])
        x = hs["dom"][k]
        kiem(abs(x["gia_tri"] - cuoi[5]) < 1e-9 and x["ngay_vn"] == NC.vn(cuoi[0]),
             f"(e) {k} = dòng cache cuối biết ≤ T ({NC.vn(cuoi[1])} VN, {cuoi[5]:.2f}%)")
    cme = [r for r in doc("yahoo_CME_1h.csv") if r[1] <= t]
    g = hs["gap_cme"]
    kiem(abs(g["gia_cme"] - cme[-1][5]) < 1e-9, f"(e) giá CME = nến 1h cuối đóng ≤ T ({cme[-1][5]:,.0f})")
    ds = g["tren"] + g["duoi"]
    for x in ds:
        mo = NG.tu_s_utc(dt.datetime.strptime(x["tao_vn"], "%Y-%m-%d %H:%M").replace(
            tzinfo=dt.timezone(dt.timedelta(hours=7))).astimezone(dt.timezone.utc).strftime("%Y-%m-%d %H:%M"))
        sau = [r for r in cme if r[0] >= mo]
        con = (x["con_lo"], min(x["hi"], min(r[4] for r in sau))) if x["chieu"] == "tăng" else \
              (max(x["lo"], max(r[3] for r in sau)), x["hi"])
        kiem(mo <= t and abs(con[0] - x["con_lo"]) < 1e-6 and abs(con[1] - x["con_hi"]) < 1e-6 and con[1] > con[0],
             f"(e) gap {x['chieu']} mở {x['tao_vn']}: còn {x['con_lo']:,.0f}–{x['con_hi']:,.0f} tính lại từ CSV thô khớp, chưa lấp")
    g9 = NC.gap_cme(NC.doc_t("2026-09-17 11:00"), NG.CACHE_MAC_DINH, True)
    kiem(any(x["lo"] == 92075 and x["hi"] == 92730 for x in g9["tren"]),
         "(e) T = 2026-09-17 11:00: gap 01-20 92.075–92.730 còn phía trên (tháng 9 người đó nhắc gap kéo lên 90–92)")


def main():
    bo_a = "--khong-a" in sys.argv
    ket_qua = {}
    for ma, khung, s in CA + CA_THEM:
        ket_qua[(ma, khung, s)] = _chay(ma, khung, NC.doc_t(s))  # cache đầy đủ (tải nếu thiếu)
    print("=== (b) 3 ca ===")
    for ca in CA:
        md, js, _hs = ket_qua[ca]
        print(f"\n----- {' '.join(ca)}: {len(md)} ký tự, {len(md.splitlines())} dòng Markdown; JSON {len(js)} ký tự -----")
        print("\n".join(md.splitlines()[:22]))
    print("\n=== (a) cắt cụt ===")
    if not bo_a:
        kiem_cat_cut(CA + CA_THEM, ket_qua)
        kiem_truoc_24h(CA + CA_THEM, ket_qua)
    print("\n=== (c) EMA / dữ liệu / trendline ===")
    for ca in CA + CA_THEM:
        kiem_ema(ket_qua[ca][2], ca[0], ca[1], NC.doc_t(ca[2]))
    hs_btc = ket_qua[CA[0]][2]
    kiem_bot_v4(NC.doc_t(CA[0][2]))
    kiem_trendline(NC.doc_t(CA[0][2]))
    print("\n=== (d) phần mới: T−24h · nhịp GIẢM tuần · trendline sau 24h/48h ===")
    for ca in CA + CA_THEM:
        kiem_phan_moi(ca[0], ca[1], NC.doc_t(ca[2]), ket_qua[ca][0], ket_qua[ca][2])
    print("\n=== (e) mục 7: gap CME · BTC.D · USDT.D ===")
    kiem_ngoai_chart(hs_btc, NC.doc_t(CA[0][2]))
    print("\nKẾT QUẢ:", "PASS hết" if not LOI else f"{len(LOI)} FAIL")
    sys.exit(1 if LOI else 0)


if __name__ == "__main__":
    main()
