#!/usr/bin/env python3
"""Nguồn nến cho bot v5 — chỉ nến ĐÃ ĐÓNG ≤ T, cửa sổ cố định theo T (kết quả chỉ phụ thuộc T, không phụ thuộc lịch sử cache).

- Coin: OKX công khai `history-candles`, `<MÃ>-USDT` (spot) → không có thì `<MÃ>-USDT-SWAP`.
  Khung: 15m, 1H, 4H, 1D (=1Dutc, mở 07:00 VN), 1W (=1Wutc, thứ Hai 07:00 VN), 1M (=1Mutc).
  Header User-Agent, nghỉ NGHI giây giữa 2 lần gọi; chỉ lưu nến confirm = "1".
- VANG (GC=F), DAU (CL=F), DXY (DX-Y.NYB), NASDAQ (^IXIC): Yahoo chart API như `backtest/tai_du_lieu.py`
  (15m: 60 ngày gần nhất; 1h: 730 ngày → 1H và gộp 4H căn UTC 00/04/…; 1d: 10 năm → 1D, gộp 1W/1M theo lịch New York).
  CME (BTC=F) cùng đường Yahoo — ngu_canh dùng 1h để tìm gap CME.
- BTC.D / USDT.D: PROXY theo ngày từ CoinMarketCap data-api (như `thi/tao_ho_so.py`), `lay_dom()`; lưu cache dạng nến
  o=h=l=c (vol = vốn hoá) để phép thử đầu độc của `kiem_tra_ngu_canh.py` phủ luôn.
- Cache: `bot_v5/cache/<nguồn>.csv` (mo_utc, dong_utc, open, high, low, close, vol — giờ UTC) + `<nguồn>.json`
  (OKX: các khoảng giờ MỞ đã tải đủ `phu`; Yahoo: `lay_luc` = lúc tải, mọi nến đóng ≤ lay_luc đều có).
  `offline=True` → chỉ đọc cache, không gọi mạng (dùng cho kiểm cắt cụt).

Mỗi nến = NenGia(mo, dong, o, h, l, c, v, nhan): mo/dong = giây epoch UTC; nhan = nhãn hiển thị giờ VN
(khung trong ngày: giờ ĐÓNG VN "YYYY-MM-DD HH:MM"; 1D: ngày; 1W: ngày thứ Hai; 1M: "YYYY-MM").
"""
import calendar, csv, datetime as dt, json, time, urllib.error, urllib.parse, urllib.request
from collections import namedtuple
from pathlib import Path
from zoneinfo import ZoneInfo

THU_MUC = Path(__file__).resolve().parent
CACHE_MAC_DINH = THU_MUC / "cache"
UTC = dt.timezone.utc
VN = dt.timezone(dt.timedelta(hours=7))
NY = ZoneInfo("America/New_York")
NGAY = 86400
NGHI = 0.12  # giây giữa 2 lần gọi OKX (giới hạn 20 lần / 2 giây)

NenGia = namedtuple("NenGia", "mo dong o h l c v nhan")

KHUNG = ("15m", "1H", "4H", "1D", "1W", "1M")
GIAY = {"15m": 900, "1H": 3600, "4H": 14400, "1D": NGAY, "1W": 7 * NGAY}  # 1M: theo lịch
OKX_BAR = {"15m": "15m", "1H": "1H", "4H": "4H", "1D": "1Dutc", "1W": "1Wutc", "1M": "1Mutc"}
# cửa sổ dữ liệu lấy về (tính lùi từ T): đủ ấm EMA610 cho khung nhỏ, đủ "từ lúc niêm yết" cho khung lớn
CUA_SO = {"15m": 2500 * 900, "1H": 2500 * 3600, "4H": 2500 * 14400, "1D": 3000 * NGAY,
          "1W": 600 * 7 * NGAY, "1M": 200 * 31 * NGAY}
YAHOO = {"VANG": ("GC=F", 17), "DAU": ("CL=F", 17), "DXY": ("DX-Y.NYB", 17), "NASDAQ": ("^IXIC", 16), "CME": ("BTC=F", 17)}
YAHOO_IV = {"15m": ("15m", "60d", 900), "1h": ("1h", "730d", 3600), "1d": ("1d", "10y", None)}
OKX_URL = "https://www.okx.com/api/v5/market/history-candles?instId={}&bar={}&limit=100&after={}"
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval={}&range={}"


class LoiDuLieu(Exception):
    pass


# ---------------- thời gian ----------------
def utc_dt(x):
    return dt.datetime.fromtimestamp(x, UTC)


def s_utc(x):
    return utc_dt(x).strftime("%Y-%m-%d %H:%M")


def s_vn(x):
    return dt.datetime.fromtimestamp(x, VN).strftime("%Y-%m-%d %H:%M")


def tu_s_utc(s):
    return int(dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M").replace(tzinfo=UTC).timestamp())


def mo_nen_chua(t, khung):
    """Giờ mở (UTC, căn OKX) của nến khung `khung` chứa thời điểm t."""
    if khung in GIAY and khung != "1W":
        return t - t % GIAY[khung]
    if khung == "1W":
        ngay = t // NGAY
        return (ngay - (ngay + 3) % 7) * NGAY  # 1970-01-01 là thứ Năm → (ngay+3)%7 = 0 ứng thứ Hai
    d = utc_dt(t)
    return int(dt.datetime(d.year, d.month, 1, tzinfo=UTC).timestamp())


def dong_nen(mo, khung):
    if khung in GIAY:
        return mo + GIAY[khung]
    d = utc_dt(mo)
    y, m = (d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1)
    return int(dt.datetime(y, m, 1, tzinfo=UTC).timestamp())


def nhan_okx(mo, dong, khung):
    if khung in ("15m", "1H", "4H"):
        return s_vn(dong)
    if khung == "1M":
        return utc_dt(mo).strftime("%Y-%m")
    return utc_dt(mo).strftime("%Y-%m-%d")


# ---------------- mạng ----------------
_lan_cuoi = [0.0]


def _get_json(url, nghi=NGHI):
    cho = _lan_cuoi[0] + nghi - time.time()
    if cho > 0:
        time.sleep(cho)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for lan in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                _lan_cuoi[0] = time.time()
                return json.load(r)
        except urllib.error.HTTPError as e:
            _lan_cuoi[0] = time.time()
            if e.code in (400, 404):
                try:
                    return json.load(e)
                except Exception:
                    raise LoiDuLieu(f"HTTP {e.code} {url}")
            if lan == 4:
                raise
        except Exception:
            _lan_cuoi[0] = time.time()
            if lan == 4:
                raise
        time.sleep(2 + 2 * lan)


# ---------------- cache chung ----------------
def _doc_csv(p):
    ra = {}
    if p.exists():
        with p.open(newline="") as f:
            for r in csv.DictReader(f):
                mo = tu_s_utc(r["mo_utc"])
                ra[mo] = (mo, tu_s_utc(r["dong_utc"]), r["open"], r["high"], r["low"], r["close"], r["vol"])
    return ra


def _ghi_csv(p, ra):
    p.parent.mkdir(parents=True, exist_ok=True)
    tam = p.with_suffix(".tmp")
    with tam.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mo_utc", "dong_utc", "open", "high", "low", "close", "vol"])
        for mo in sorted(ra):
            r = ra[mo]
            w.writerow([s_utc(r[0]), s_utc(r[1])] + list(r[2:]))
    tam.replace(p)


def _doc_meta(p):
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def _ghi_meta(p, m):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")


def _gop_khoang(ds):
    ds = sorted([list(x) for x in ds if x[1] > x[0]])
    ra = []
    for a, b in ds:
        if ra and a <= ra[-1][1]:
            ra[-1][1] = max(ra[-1][1], b)
        else:
            ra.append([a, b])
    return ra


def _thieu(phu, a, b):
    """Các đoạn con của [a, b) chưa nằm trong `phu`."""
    ra, x = [], a
    for p, q in phu:
        if q <= x:
            continue
        if p >= b:
            break
        if p > x:
            ra.append((x, min(p, b)))
        x = max(x, q)
        if x >= b:
            break
    if x < b:
        ra.append((x, b))
    return ra


# ---------------- OKX ----------------
def giai_inst(ma, cache_dir=None, offline=False):
    """MÃ → instId OKX (spot ưu tiên, rồi swap). Lưu ánh xạ trong cache/inst.json."""
    cache_dir = Path(cache_dir or CACHE_MAC_DINH)
    p = cache_dir / "inst.json"
    m = _doc_meta(p)
    if ma in m:
        return m[ma]
    if offline:
        raise LoiDuLieu(f"{ma}: chưa có trong cache/inst.json (offline)")
    for inst in (f"{ma}-USDT", f"{ma}-USDT-SWAP"):
        j = _get_json(OKX_URL.format(inst, "1Dutc", int(time.time() * 1000)).replace("limit=100", "limit=1"))
        if j.get("code") == "0":
            m[ma] = inst
            _ghi_meta(p, m)
            return inst
    raise LoiDuLieu(f"{ma}: không có {ma}-USDT hay {ma}-USDT-SWAP trên OKX")


def _okx_tai(inst, khung, a, b):
    """Nến đã đóng có giờ mở trong [a, b) (giây). Trả {mo: dòng}. Hết dữ liệu cũ hơn → dừng (coi như đủ tới a)."""
    after, ra = b * 1000, {}
    while after > a * 1000:
        j = _get_json(OKX_URL.format(inst, OKX_BAR[khung], after))
        if j.get("code") != "0":
            raise LoiDuLieu(f"OKX {inst} {khung}: {j.get('code')} {j.get('msg')}")
        d = j["data"]
        if not d:
            break
        for ts, o, h, l, c, v, *_, xn in d:
            mo = int(ts) // 1000
            if xn == "1" and a <= mo < b:
                ra[mo] = (mo, dong_nen(mo, khung), o, h, l, c, v)
        moi = int(d[-1][0])
        if moi >= after:
            break
        after = moi
    return ra


def _chuoi_okx(ma, khung, t, cache_dir, offline):
    inst = giai_inst(ma, cache_dir, offline)
    ten = f"okx_{inst}_{khung}"
    p_csv, p_meta = Path(cache_dir) / f"{ten}.csv", Path(cache_dir) / f"{ten}.json"
    ra = _doc_csv(p_csv)
    meta = _doc_meta(p_meta)
    phu = _gop_khoang(meta.get("phu", []))
    a, b = t - CUA_SO[khung], mo_nen_chua(t, khung)  # cần mọi nến mở trong [a, b) (đều đóng ≤ t)
    thieu = _thieu(phu, a, b)
    if thieu and not offline:
        tran = mo_nen_chua(int(time.time()) - 120, khung)  # mọi nến mở trước mốc này đã đóng lúc tải
        for x, y in thieu:
            y = min(y, tran)
            if y <= x:
                continue
            ra.update(_okx_tai(inst, khung, x, y))
            phu = _gop_khoang(phu + [[x, y]])
        _ghi_csv(p_csv, ra)
        meta["phu"] = phu
        meta["inst"] = inst
        _ghi_meta(p_meta, meta)
    nen = []
    for mo in sorted(ra):
        mo_, dong, o, h, l, c, v = ra[mo]
        if mo >= a and dong <= t:
            nen.append(NenGia(mo, dong, float(o), float(h), float(l), float(c), float(v), nhan_okx(mo, dong, khung)))
    loai = "spot" if not inst.endswith("SWAP") else "perp (SWAP)"
    return f"OKX {loai} {inst}", nen


# ---------------- Yahoo ----------------
def _yahoo_dong_1d(ts, gio):
    ngay = dt.datetime.fromtimestamp(ts, NY).date()
    return int(dt.datetime(ngay.year, ngay.month, ngay.day, gio, 0, tzinfo=NY).timestamp())


def _yahoo_tai(sym, iv_key, gio):
    iv, rg, dur = YAHOO_IV[iv_key]
    j = _get_json(YAHOO_URL.format(urllib.parse.quote(sym, safe=""), iv, rg), nghi=0.5)
    r = j["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    bay_gio = time.time()
    ra = {}
    for i, ts in enumerate(r.get("timestamp") or []):
        if None in (q["open"][i], q["high"][i], q["low"][i], q["close"][i]):
            continue
        if dur:
            if ts % 900:
                continue  # tick lẻ (nến đang chạy) — bỏ
            dong = ts + dur
        else:
            dong = _yahoo_dong_1d(ts, gio)
        if dong > bay_gio:
            continue  # chưa đóng lúc tải
        ra[ts] = (ts, dong, repr(q["open"][i]), repr(q["high"][i]), repr(q["low"][i]), repr(q["close"][i]),
                  repr(q["volume"][i] or 0))
    return ra


def _yahoo_goc(ma, iv_key, t, cache_dir, offline):
    sym, gio = YAHOO[ma]
    ten = f"yahoo_{ma}_{iv_key}"
    p_csv, p_meta = Path(cache_dir) / f"{ten}.csv", Path(cache_dir) / f"{ten}.json"
    ra = _doc_csv(p_csv)
    meta = _doc_meta(p_meta)
    if meta.get("lay_luc", 0) < t and not offline:
        ra.update(_yahoo_tai(sym, iv_key, gio))
        _ghi_csv(p_csv, ra)
        meta.update({"lay_luc": int(time.time()), "sym": sym})
        _ghi_meta(p_meta, meta)
    return [(r[0], r[1], float(r[2]), float(r[3]), float(r[4]), float(r[5]), float(r[6])) for _, r in sorted(ra.items())]


def _gop(nhom, nhan_fn):
    ra = []
    for (mo_k, dong_k), ds in nhom:
        ra.append(NenGia(ds[0][0], dong_k, ds[0][2], max(x[3] for x in ds), min(x[4] for x in ds), ds[-1][5],
                         sum(x[6] for x in ds), nhan_fn(mo_k, dong_k)))
    return ra


def _chuoi_yahoo(ma, khung, t, cache_dir, offline):
    sym, gio = YAHOO[ma]
    a = t - CUA_SO[khung]
    if khung == "15m":
        goc = _yahoo_goc(ma, "15m", t, cache_dir, offline)
        nen = [NenGia(*x, s_vn(x[1])) for x in goc if x[1] <= t and x[0] >= a]
    elif khung == "1H":
        goc = _yahoo_goc(ma, "1h", t, cache_dir, offline)
        nen = [NenGia(*x, s_vn(x[1])) for x in goc if x[1] <= t and x[0] >= a]
    elif khung == "4H":
        goc = [x for x in _yahoo_goc(ma, "1h", t, cache_dir, offline) if x[0] >= a]
        nhom = {}
        for x in goc:
            k = x[0] - x[0] % 14400
            nhom.setdefault((k, k + 14400), []).append(x)
        nen = [n for n in _gop(sorted(nhom.items()), lambda mo, dg: s_vn(dg)) if n.dong <= t]
    else:
        goc = _yahoo_goc(ma, "1d", t, cache_dir, offline)
        if khung == "1D":
            nen = [NenGia(*x, dt.datetime.fromtimestamp(x[1], NY).strftime("%Y-%m-%d"))
                   for x in goc if x[1] <= t and x[0] >= a]
        else:
            nhom = {}
            for x in goc:
                ngay = dt.datetime.fromtimestamp(x[1], NY).date()
                if khung == "1W":
                    t2 = ngay - dt.timedelta(days=ngay.weekday())
                    t6 = t2 + dt.timedelta(days=4)
                    k = (int(dt.datetime(t2.year, t2.month, t2.day, tzinfo=NY).timestamp()),
                         int(dt.datetime(t6.year, t6.month, t6.day, gio, tzinfo=NY).timestamp()))
                else:
                    cuoi = calendar.monthrange(ngay.year, ngay.month)[1]
                    k = (int(dt.datetime(ngay.year, ngay.month, 1, tzinfo=NY).timestamp()),
                         int(dt.datetime(ngay.year, ngay.month, cuoi, gio, tzinfo=NY).timestamp()))
                nhom.setdefault(k, []).append(x)
            fn = ((lambda mo, dg: dt.datetime.fromtimestamp(mo, NY).strftime("%Y-%m-%d")) if khung == "1W"
                  else (lambda mo, dg: dt.datetime.fromtimestamp(mo, NY).strftime("%Y-%m")))
            nen = [n for n in _gop(sorted(nhom.items()), fn) if n.dong <= t and n.mo >= a]
    return f"Yahoo {sym}", nen


# ---------------- CoinMarketCap: BTC.D / USDT.D ----------------
CMC_TU = int(dt.datetime(2025, 1, 1, tzinfo=UTC).timestamp())
CMC_TRE = 3600  # ảnh chụp CMC coi như biết sau 1 giờ (độ trễ bảo thủ như thi/tao_ho_so.py)
CMC_GLOBAL = ("https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/historical"
              "?format=chart&interval=1d&timeStart={}&timeEnd={}")
CMC_USDT = ("https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical"
            "?id=825&convertId=2781&timeStart={}&timeEnd={}&interval=1d")


def _cmc_tai(ra):
    bay_gio = int(time.time())
    g = _get_json(CMC_GLOBAL.format(CMC_TU, bay_gio), nghi=1)["data"]["quotes"]
    u = _get_json(CMC_USDT.format(CMC_TU, bay_gio), nghi=1)["data"]["quotes"]
    tong = {}
    for q in g:
        mo = int(dt.datetime.fromisoformat(q["timestamp"].replace("Z", "+00:00")).timestamp())
        if mo % NGAY or mo + CMC_TRE > bay_gio:
            continue  # chỉ lấy ảnh chụp 00:00 UTC đã công bố
        tong[mo] = q["quote"][0]["totalMarketCap"]
        v = repr(q["btcDominance"])
        ra["BTC.D"][mo] = (mo, mo + CMC_TRE, v, v, v, v, repr(tong[mo]))
    for q in u:
        # vốn hoá USDT lúc đóng ngày (23:59:59.999) ghép với tổng vốn hoá ảnh chụp 00:00 hôm sau = cùng thời điểm
        mo = round(dt.datetime.fromisoformat(q["timeClose"].replace("Z", "+00:00")).timestamp())
        if mo in tong and mo + CMC_TRE <= bay_gio:
            v = repr(q["quote"]["marketCap"] / tong[mo] * 100)
            ra["USDT.D"][mo] = (mo, mo + CMC_TRE, v, v, v, v, repr(q["quote"]["marketCap"]))
    return bay_gio


def lay_dom(t, cache_dir=None, offline=False):
    """{"BTC.D": [(mo, dong, %)], "USDT.D": [...]} theo ngày, chỉ điểm có dong ≤ t (dong = ảnh chụp + CMC_TRE).
    PROXY: BTC.D = btcDominance của CMC; USDT.D = vốn hoá USDT / tổng vốn hoá CMC — không phải CRYPTOCAP TradingView."""
    cache_dir = Path(cache_dir or CACHE_MAC_DINH)
    tep = {"BTC.D": cache_dir / "cmc_BTCD_1D.csv", "USDT.D": cache_dir / "cmc_USDTD_1D.csv"}
    p_meta = cache_dir / "cmc_dom.json"
    ra = {k: _doc_csv(p) for k, p in tep.items()}
    meta = _doc_meta(p_meta)
    if meta.get("lay_luc", 0) < t and not offline:
        meta["lay_luc"] = _cmc_tai(ra)
        for k, p in tep.items():
            _ghi_csv(p, ra[k])
        _ghi_meta(p_meta, meta)
    return {k: [(r[0], r[1], float(r[5])) for _, r in sorted(v.items()) if r[1] <= t] for k, v in ra.items()}


# ---------------- API ----------------
def lay_chuoi(ma, khung, t, cache_dir=None, offline=False):
    """(mô tả nguồn, [NenGia]) — nến khung `khung` có giờ mở ≥ t − CUA_SO và giờ ĐÓNG ≤ t, tăng dần."""
    cache_dir = Path(cache_dir or CACHE_MAC_DINH)
    if khung not in KHUNG:
        raise LoiDuLieu(f"khung {khung} không hỗ trợ")
    if ma in YAHOO:
        return _chuoi_yahoo(ma, khung, t, cache_dir, offline)
    return _chuoi_okx(ma, khung, t, cache_dir, offline)
