#!/usr/bin/env python3
"""LỆNH GIẤY v1 + v2 — chạy tiếp NGOÀI MẪU từ 31/10/2026 00:00 giờ VN, mỗi bot vốn 4.000$.

Chạy:  python3 giay/chay_giay.py            (cron 5 phút sau mỗi nến H4 đóng — xem giay/cai_lich.sh)
       python3 giay/chay_giay.py --khong-tai (không tải mạng, chỉ dùng bộ đệm giay/du_lieu/ — để kiểm)

Mỗi lần chạy:
 1. Tải nến mới nhất (OKX: BTC ETH OKB BNB — chỉ nến đã xác nhận; Yahoo: vàng GC=F, dầu CL=F — H1 gộp H4 như
    backtest/tai_du_lieu.py) và gộp vào bộ đệm giay/du_lieu/ (lần đầu chép từ backtest/du_lieu_2025/).
 2. Với từng bot (v1 = luật chay.py, v2 = luật backtest/v2.py) xử lý TUẦN TỰ mọi mốc nến H4 đã đóng sau mốc cuối
    đã xử lý bằng đúng bộ máy backtest (v2.buoc): đặt limit, khớp, SL/TP/hết hạn, hủy lệnh chờ, tín hiệu mới.
 3. Lưu trạng thái giay/trang_thai_v1.json, trang_thai_v2.json; nối sự kiện mới vào giay/nhat_ky.csv; viết giay/BAO_CAO.md.

Idempotent theo thời điểm nến: mốc đã xử lý (nen_cuoi) không làm lại; nhật ký bỏ qua dòng trùng khóa
(bot, giờ nến, sự kiện, tài sản, lý do). Máy ngủ / lỡ lịch thì lần chạy sau tự xử lý bù các nến bị lỡ.
Mốc xử lý tối đa = nến H4 đã xác nhận mới nhất có ở CẢ 4 coin OKX (tải lỗi → dừng, không xử lý dở).
"""
import csv, datetime as dt, fcntl, json, os, sys, time, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

GIAY = Path(__file__).resolve().parent
GOC = GIAY.parent
sys.path.insert(0, str(GOC / "backtest"))
import v2 as V  # noqa: E402
C = V.C

DL = GIAY / "du_lieu"
NGUON_GOC = GOC / "backtest" / "du_lieu_2025"
UTC = dt.timezone.utc
VN = dt.timezone(dt.timedelta(hours=7))
GIO = 3600
BAT_DAU = int(dt.datetime(2026, 10, 31, 0, 0, tzinfo=VN).timestamp())
BOT = {"v1": dict(co=V.CO_V1, mo_ta="v1 — luật chay.py (vào EMA34, SL giá, TP fractal)"),
       "v2": dict(co=V.CO_V2, mo_ta="v2 — v1 + 5 thay đổi (đi ngang, nến lớn, phá mốc, SL nến đóng, TP Fibo mở rộng; vàng scalp)")}
OKX_INST = {"BTC": "BTC-USDT", "ETH": "ETH-USDT", "OKB": "OKB-USDT", "BNB": "BNB-USDT"}
YH = {"VANG": "GC=F", "DAU": "CL=F"}
COT_NK = ["gio_chay_vn", "bot", "gio_nen_vn", "su_kien", "tai_san", "chieu", "gia", "ly_do", "chi_tiet", "lai_usd", "so_du_usd"]
TEN_LY_DO = dict(V.DANH_LY_DO)
TEN_LY_DO.update(dang_co_lenh="Đang có lệnh mở / lệnh chờ", dat_lenh="ĐẶT LỆNH CHỜ")


# ---------------- TẢI DỮ LIỆU ----------------
def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for lan in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception:
            if lan == 3:
                raise
            time.sleep(2 + 3 * lan)


def _s(ts):
    return dt.datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%d %H:%M")


def doc_dem(ten):
    p = DL / ten
    if not p.exists():
        src = NGUON_GOC / ten
        if not src.exists():
            src = GOC / "backtest" / "du_lieu" / ten
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src.read_text())
    ds = {}
    with p.open() as f:
        for r in csv.DictReader(f):
            mo = int(dt.datetime.strptime(r["mo_utc"], "%Y-%m-%d %H:%M").replace(tzinfo=UTC).timestamp())
            dg = int(dt.datetime.strptime(r["dong_utc"], "%Y-%m-%d %H:%M").replace(tzinfo=UTC).timestamp())
            ds[dg] = (mo, dg, r["open"], r["high"], r["low"], r["close"], r["vol"])
    return ds


def ghi_dem(ten, ds):
    p = DL / ten
    tam = p.with_suffix(".tmp")
    with tam.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mo_utc", "dong_utc", "open", "high", "low", "close", "vol"])
        for dg in sorted(ds):
            mo, dg, o, h, l, c, v = ds[dg]
            w.writerow([_s(mo), _s(dg), o, h, l, c, v])
    os.replace(tam, p)


def okx_moi(inst, bar, do_dai, tu_mo):
    """Nến ĐÃ XÁC NHẬN từ (gần) tu_mo tới nay. Dùng /candles (300 nến mới nhất), thiếu thì lùi bằng /history-candles."""
    ra = {}
    d = _get(f"https://www.okx.com/api/v5/market/candles?instId={inst}&bar={bar}&limit=300")["data"]
    for ts, o, h, l, c, v, *_, xn in d:
        if xn == "1":
            mo = int(ts) // 1000
            ra[mo + do_dai] = (mo, mo + do_dai, o, h, l, c, v)
    after = min((int(r[0]) for r in d), default=int(time.time() * 1000))
    while after // 1000 > tu_mo:
        d = _get(f"https://www.okx.com/api/v5/market/history-candles?instId={inst}&bar={bar}&limit=100&after={after}")["data"]
        if not d:
            break
        for ts, o, h, l, c, v, *_, xn in d:
            if xn == "1":
                mo = int(ts) // 1000
                ra[mo + do_dai] = (mo, mo + do_dai, o, h, l, c, v)
        after = int(d[-1][0])
        time.sleep(0.15)
    return ra


def yahoo_moi(sym, so_ngay_thieu):
    """H1 → H4 căn UTC (giữ nến ≥3 giờ, đã kết thúc) và D1 (đóng 17:00 New York) — như backtest/tai_du_lieu.py."""
    bay_gio = time.time()
    r = _get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1h&range={'1mo' if so_ngay_thieu < 25 else '730d'}")["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    gio = {}
    for i, ts in enumerate(r["timestamp"]):
        if ts % GIO or None in (q["open"][i], q["high"][i], q["low"][i], q["close"][i]):
            continue
        gio[ts] = (q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i] or 0)
    h4 = {}
    if gio:
        dau = min(gio)
        nhom = {}
        for ts in sorted(gio):
            nhom.setdefault(ts - ts % (4 * GIO), []).append(ts)
        for mo, ds in nhom.items():
            if mo < dau or len(ds) < 3 or mo + 4 * GIO > bay_gio:   # bỏ nến cắt dở ở đầu cửa sổ tải, nến thiếu giờ, nến chưa xong
                continue
            o = gio[ds[0]][0]; c = gio[ds[-1]][3]
            h = max(gio[t][1] for t in ds); l = min(gio[t][2] for t in ds); v = sum(gio[t][4] for t in ds)
            h4[mo + 4 * GIO] = (mo, mo + 4 * GIO, o, h, l, c, v)
    r = _get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range={'3mo' if so_ngay_thieu < 60 else '2y'}")["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    ny = ZoneInfo(r["meta"].get("exchangeTimezoneName", "America/New_York"))
    d1 = {}
    for i, ts in enumerate(r["timestamp"]):
        if None in (q["open"][i], q["high"][i], q["low"][i], q["close"][i]):
            continue
        ngay = dt.datetime.fromtimestamp(ts, ny).date()
        dong = int(dt.datetime(ngay.year, ngay.month, ngay.day, 17, 0, tzinfo=ny).timestamp())
        if dong > bay_gio:
            continue
        d1[dong] = (dong - 23 * GIO, dong, q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i] or 0)
    return h4, d1


def cap_nhat_du_lieu(tai):
    """Gộp nến mới vào bộ đệm. Trả {mã: giờ đóng nến H4 mới nhất}."""
    moi_nhat = {}
    for ma in V.TAI_SAN:
        h4, d1 = doc_dem(f"{ma}_4H.csv"), doc_dem(f"{ma}_1D.csv")
        if tai:
            cuoi4, cuoi1 = max(h4), max(d1)
            if ma in OKX_INST:
                h4.update(okx_moi(OKX_INST[ma], "4H", 4 * GIO, cuoi4 - 4 * GIO - 2 * 86400))
                d1.update(okx_moi(OKX_INST[ma], "1Dutc", 86400, cuoi1 - 86400 - 3 * 86400))
            else:
                n4, n1 = yahoo_moi(YH[ma], (time.time() - cuoi4) / 86400)
                h4.update(n4); d1.update(n1)
            ghi_dem(f"{ma}_4H.csv", h4); ghi_dem(f"{ma}_1D.csv", d1)
        moi_nhat[ma] = max(h4)
    return moi_nhat


# ---------------- TRẠNG THÁI ----------------
def _ob(d):
    return V.Ob(d)


def doc_tt(bot):
    p = GIAY / f"trang_thai_{bot}.json"
    if not p.exists():
        tt = V.tt_moi(V.VON0)
        tt.update(bot=bot, mo_ta=BOT[bot]["mo_ta"], co=BOT[bot]["co"], bat_dau_vn=C.vn(BAT_DAU), tao_luc_vn=C.vn(time.time()),
                  tin_hieu={}, so_nen_da_xu_ly=0)
        return tt
    tt = json.loads(p.read_text())
    tt["vithe"] = {k: _ob(v) for k, v in tt["vithe"].items()}
    tt["cho"] = {k: _ob(v) for k, v in tt["cho"].items()}
    tt["lenh"] = [_ob(v) for v in tt["lenh"]]
    tt["von"] = [tuple(v) for v in tt["von"]]
    return tt


def ghi_tt(bot, tt):
    p = GIAY / f"trang_thai_{bot}.json"
    tam = p.with_suffix(".tmp")
    tam.write_text(json.dumps(tt, ensure_ascii=False, indent=1))
    os.replace(tam, p)


def mtm(tt, TS):
    v = tt["so_du"]
    for m, p in tt["vithe"].items():
        a = TS[m]
        v += p.kl * p.con * (a.c[-1] - p.gia_khop) * p.chieu
    return v


# ---------------- NHẬT KÝ ----------------
def _khoa(r):
    return (r["bot"], r["gio_nen_vn"], r["su_kien"], r["tai_san"], r["ly_do"])


def ghi_nhat_ky(dong_moi):
    p = GIAY / "nhat_ky.csv"
    co_san = set()
    if p.exists():
        with p.open() as f:
            co_san = {_khoa(r) for r in csv.DictReader(f)}
    moi = [r for r in dong_moi if _khoa(r) not in co_san]
    if not moi:
        return 0
    dau = not p.exists()
    with p.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COT_NK)
        if dau:
            w.writeheader()
        for r in moi:
            w.writerow(r)
    return len(moi)


def su_kien_sang_dong(bot, e, gio_chay):
    ct = {k: (C.g(v) if isinstance(v, float) else v) for k, v in e.items()
          if k not in ("ts", "su_kien", "ma", "chieu", "gia", "ly_do", "lai", "so_du") and v is not None}
    return dict(gio_chay_vn=gio_chay, bot=bot, gio_nen_vn=C.vn(e["ts"]), su_kien=e["su_kien"], tai_san=e["ma"],
                chieu="SHORT" if e["chieu"] < 0 else "LONG", gia=C.g(e["gia"]), ly_do=e.get("ly_do", e.get("kieu", "")),
                chi_tiet=json.dumps(ct, ensure_ascii=False), lai_usd=round(e["lai"], 2) if "lai" in e else "",
                so_du_usd=round(e["so_du"], 2) if "so_du" in e else "")


# ---------------- BÁO CÁO ----------------
def _ch(x):
    return "SHORT" if x < 0 else "LONG"


def mo_ta_tin_hieu(ly_do, q):
    if q:
        return (f"**ĐẶT {_ch(q.chieu)}** ({V.TEN_KIEU[q.kieu]}) vào {C.g(q.vao)} · SL {C.g(q.sl)} · TP1 {C.g(q.tp1)} · TP2 {C.g(q.tp2)} · "
                f"R:R {C.so(q.rr, 1)} · căn cứ {'+'.join(q.cc) or 'EMA34'}")
    return TEN_LY_DO.get(ly_do, ly_do)


def lam_bao_cao(TT, TS, moi_nhat, xem_truoc, gio_chay):
    L = []
    w = L.append
    w("# LỆNH GIẤY v1 vs v2 — chạy tiếp ngoài mẫu\n")
    w(f"_Sinh tự động bởi `giay/chay_giay.py` lúc **{gio_chay} VN**. Bắt đầu {C.vn(BAT_DAU)} VN, mỗi bot vốn 4.000$, rủi ro 2%/lệnh, tối đa 4 lệnh, "
      f"6 tài sản BTC, ETH, OKB, BNB (OKX), vàng GC=F, dầu CL=F (Yahoo). Luật giữ nguyên như backtest (`backtest/v2.py`, bộ máy `buoc`)._\n")
    w("Nến H4 mới nhất trong bộ đệm: " + " · ".join(f"{C.TEN[m]} {C.vn(t)}" for m, t in moi_nhat.items()) + " (giờ đóng, VN).\n")
    w("## Tóm tắt\n")
    rows = []
    for bot, tt in TT.items():
        st = C.thong_ke(tt["lenh"])
        v = mtm(tt, TS)
        rows.append([f"**{bot}**", C.vn(tt["nen_cuoi"]) if tt["nen_cuoi"] else "chưa có", tt.get("so_nen_da_xu_ly", 0),
                     f"{tt['so_du']:,.2f}$".replace(",", " "), f"{v:,.2f}$".replace(",", " "), C.tien(v - V.VON0), C.pct(v / V.VON0 - 1, 2),
                     st["n"], C.pct0(st["thang"], 0) if st["n"] else "—", C.so(st["tong_r"], 1), len(tt["vithe"]), len(tt["cho"])])
    w(C.bang(["Bot", "Nến cuối đã xử lý (VN)", "Số mốc nến", "Số dư đã chốt", "Vốn theo giá TT", "Lãi/lỗ", "%", "Lệnh đã đóng",
              "Thắng", "Tổng R", "Vị thế mở", "Lệnh chờ"], rows))
    for bot, tt in TT.items():
        w(f"\n## Bot {bot} — {BOT[bot]['mo_ta']}\n")
        w("**Vị thế đang mở**\n")
        if tt["vithe"]:
            rows = []
            for m, p in tt["vithe"].items():
                a = TS[m]
                tam = p.kl * p.con * (a.c[-1] - p.gia_khop) * p.chieu
                rows.append([C.TEN[m], _ch(p.chieu), V.TEN_KIEU[p.kieu], C.vn(p.khop_ts), C.g(p.gia_khop), C.g(p.sl),
                             C.g(p.sl_kc) if p.sl_dong else "—", C.g(p.tp1), C.g(p.tp2), "rồi" if p.tp1_xong else "chưa",
                             f"{int(p.con * 100)}%", C.g(a.c[-1]), C.tien(p.lai + tam), C.vn(p.khop_ts + p.het_han * 4 * GIO)])
            w(C.bang(["Tài sản", "Chiều", "Kiểu vào", "Khớp (VN)", "Giá khớp", "SL" + (" (nến đóng)" if BOT[bot]["co"]["sl_dong"] else ""),
                      "Chặn khẩn", "TP1", "TP2", "Đã TP1", "Còn", "Giá hiện", "Lãi tạm tính", "Hết hạn ~ (VN)"], rows))
        else:
            w("_Không có._")
        w("\n**Lệnh chờ (limit)**\n")
        if tt["cho"]:
            rows = []
            for m, q in tt["cho"].items():
                rows.append([C.TEN[m], _ch(q.chieu), V.TEN_KIEU[q.kieu], C.vn(q.tin_hieu_ts), C.g(q.vao), C.g(q.sl), C.g(q.tp1), C.g(q.tp2),
                             C.so(q.rr, 1), "+".join(q.cc) or "EMA34", f"{C.vn(q.tin_hieu_ts + C.NEN_CHO * 4 * GIO)} (≈6 nến)"])
            w(C.bang(["Tài sản", "Chiều", "Kiểu vào", "Đặt lúc (VN)", "Giá vào", "SL", "TP1", "TP2", "R:R", "Căn cứ", "Hết hiệu lực"], rows))
        else:
            w("_Không có._")
        w("\n**Lệnh đã đóng** (mới nhất trước, tối đa 30)\n")
        if tt["lenh"]:
            rows = []
            for p in sorted(tt["lenh"], key=lambda p: -p.dong_ts)[:30]:
                rows.append([C.TEN[p.ma], _ch(p.chieu), V.TEN_KIEU[p.kieu], C.vn(p.khop_ts), C.vn(p.dong_ts), C.g(p.gia_khop), p.kq,
                             C.so(p.lai / p.rui_ro_usd), C.tien(p.lai)])
            w(C.bang(["Tài sản", "Chiều", "Kiểu vào", "Khớp", "Đóng", "Giá khớp", "Kết quả", "R", "Lãi/lỗ"], rows))
        else:
            w("_Chưa có._")
        w("\n**Tín hiệu tại nến H4 vừa xử lý**\n")
        rows = []
        for m in V.TAI_SAN:
            th = tt["tin_hieu"].get(m)
            if th:
                rows.append([C.TEN[m], th["gio_nen_vn"], th["mo_ta"]])
        w(C.bang(["Tài sản", "Nến (VN)", "Quyết định"], rows) if rows else "_Chưa xử lý nến nào sau mốc bắt đầu._")
    if xem_truoc:
        w("\n## Xem trước (CHƯA tính vào lệnh giấy)\n")
        w("_Chưa có nến H4 nào đóng sau mốc bắt đầu. Đây là quyết định hai bot SẼ ra nếu xét tại nến đã đóng gần nhất — chỉ để kiểm, không đặt lệnh._\n")
        rows = [[C.TEN[m], gio, mo_ta_tin_hieu(*xem_truoc["v1"][m]), mo_ta_tin_hieu(*xem_truoc["v2"][m])] for m, gio in xem_truoc["gio"].items()]
        w(C.bang(["Tài sản", "Nến (VN)", "v1", "v2"], rows))
    w("\n---\n_Ghi chú: vàng/dầu Yahoo trễ ~10 phút nên nến H4 chốt lúc +5 phút có thể thiếu vài phút cuối; mốc đã xử lý không làm lại. "
      "Chi tiết từng sự kiện: `giay/nhat_ky.csv`. Trạng thái đầy đủ: `giay/trang_thai_v1.json`, `trang_thai_v2.json`._\n")
    (GIAY / "BAO_CAO.md").write_text("\n".join(L))


# ---------------- CHẠY ----------------
def main():
    tai = "--khong-tai" not in sys.argv
    GIAY.mkdir(exist_ok=True)
    with (GIAY / ".khoa").open("w") as khoa:
        try:
            fcntl.flock(khoa, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Đang có một lần chạy khác — bỏ qua."); return
        gio_chay = C.vn(time.time())
        moi_nhat = cap_nhat_du_lieu(tai)
        TS = {m: V.nap(m, DL) for m in V.TAI_SAN}
        gioi_han = min(moi_nhat[m] for m in OKX_INST)              # mọi coin OKX đã có nến này
        TT, dong_nk = {}, []
        for bot, cfg in BOT.items():
            tt = doc_tt(bot)
            moc = sorted({t for m in V.TAI_SAN for t in TS[m].dong
                          if BAT_DAU <= t <= gioi_han and (tt["nen_cuoi"] is None or t > tt["nen_cuoi"])})
            for T in moc:
                ev = []
                ra = V.buoc(tt, T, TS, V.TAI_SAN, cfg["co"], ghi=ev.append)
                for m, (ly_do, q, info) in ra.items():
                    tt["tin_hieu"][m] = dict(gio_nen_vn=C.vn(T), ly_do=ly_do, mo_ta=mo_ta_tin_hieu(ly_do, q))
                tt["so_nen_da_xu_ly"] = tt.get("so_nen_da_xu_ly", 0) + 1
                dong_nk += [su_kien_sang_dong(bot, e, gio_chay) for e in ev]
            for p in tt["lenh"]:
                p.R = p.lai / p.rui_ro_usd
            tt["cap_nhat_vn"] = gio_chay
            tt["von_theo_gia_tt"] = mtm(tt, TS)
            ghi_tt(bot, tt)
            TT[bot] = tt
            print(f"{bot}: xử lý {len(moc)} mốc nến mới (tới {C.vn(tt['nen_cuoi']) if tt['nen_cuoi'] else '—'}); số dư {tt['so_du']:.2f}$, "
                  f"vốn theo giá {tt['von_theo_gia_tt']:.2f}$, {len(tt['vithe'])} vị thế, {len(tt['cho'])} lệnh chờ, {len(tt['lenh'])} lệnh đã đóng")
        n = ghi_nhat_ky(dong_nk)
        xem_truoc = None
        if all(tt["nen_cuoi"] is None for tt in TT.values()):
            xem_truoc = {"gio": {}, "v1": {}, "v2": {}}
            for m in V.TAI_SAN:
                a = TS[m]
                k = len(a.dong) - 1
                xem_truoc["gio"][m] = C.vn(a.dong[k])
                for bot in BOT:
                    r, q, _ = V.quyet_dinh_v2(a, k, BOT[bot]["co"])
                    xem_truoc[bot][m] = (r, q)
        lam_bao_cao(TT, TS, moi_nhat, xem_truoc, gio_chay)
        print(f"Nhật ký: +{n} dòng mới. ✓ Đã ghi giay/BAO_CAO.md")


if __name__ == "__main__":
    main()
