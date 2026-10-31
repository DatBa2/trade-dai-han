#!/usr/bin/env python3
"""HẠ TẦNG BÀI THI bot v3 — tạo hồ sơ cho từng buổi thi (phiếu 2026-07-01 → 2026-10-30).

Yêu cầu số 1: hồ sơ CHỈ chứa dữ liệu đã CÓ THỂ BIẾT trước mốc cắt C.
  Giờ live thật: transcripts/gio_live.tsv (id, bat_dau_vn, phut, nguon_gio). Video chưa có trong file →
  HHMM trong tên phiếu (YYYY-MM-DD_HHMM_ID), không có thì 10:00 VN; thời lượng theo danh_sach.tsv, thiếu thì
  120 phút — gắn cờ "giờ không chắc".
  C = lúc KẾT THÚC live (bắt đầu + số phút), vì nhãn so sánh là view CUỐI buổi của người đó.
  T = giờ đóng nến H4 BTC (căn UTC) gần nhất đã đóng ≤ C.
Hợp đồng thời điểm (event_time + độ trễ công bố ≤ C): nến H4/D1/H1 = giờ đóng; W1/tháng hoàn tất = giờ đóng,
đang chạy = gộp tạm từ nến H4 đã đóng; fractal chỉ khi đủ nến bên phải đã đóng; F&G = mốc ngày + 1 giờ;
Yahoo = giờ đóng phiên + 30 phút; CMC = ảnh chụp + 1 giờ. Phiếu/mốc buổi trước chỉ dùng khi buổi đó đã kết thúc
trước khi buổi thi bắt đầu.
Cách bảo đảm: mọi chuỗi được CẮT tại C trước khi tính (lớp Cat); mọi dấu thời gian đã dùng được kiểm ≤ C
(sai là ném lỗi); --kiem còn dựng lại hồ sơ từ kho đã xoá sạch dữ liệu sau C và so phải GIỐNG HỆT.

Cách dùng (chạy từ bất kỳ đâu):
  python3 thi/tao_ho_so.py                  # tạo hồ sơ cho mọi buổi thi → thi/ho_so/
  python3 thi/tao_ho_so.py --chi A B        # chỉ các buổi có tên chứa A hoặc B
  python3 thi/tao_ho_so.py --kiem --chi A   # in bảng dấu thời gian + phép thử cắt tương lai (kiểm rò rỉ)
  python3 thi/tao_ho_so.py --tai-lai        # tải lại cache thi/du_lieu/ (nến bổ sung, F&G, Yahoo, CMC)
"""
import csv, datetime as dt, json, re, sys, time, urllib.request
from bisect import bisect_right
from collections import namedtuple
from pathlib import Path
from zoneinfo import ZoneInfo

THI = Path(__file__).resolve().parent
GOC = THI.parent
DL = THI / "du_lieu"
HS = THI / "ho_so"
UTC = dt.timezone.utc
VN = dt.timezone(dt.timedelta(hours=7))
NY = ZoneInfo("America/New_York")
GIO4, NGAY = dt.timedelta(hours=4), dt.timedelta(days=1)
TU_THI, DEN_THI = "2026-07-01", "2026-10-30"
THU = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
MAU_TEN = re.compile(r"^(\d{4}-\d{2}-\d{2})_(?:(\d{4})_)?(.{11})$")
PHUT_MAC_DINH = 120
OKX = "https://www.okx.com/api/v5/market/history-candles?instId=BTC-USDT&bar={}&limit=100&after={}"
# Yahoo daily: phiên đóng 16:00 NY (Nasdaq), 17:00 NY (hợp đồng tương lai CME/ICE, DXY) — như backtest/tai_du_lieu.py
YAHOO = {"Vàng (GC=F)": ("GC=F", (17, 0)), "Dầu WTI (CL=F)": ("CL=F", (17, 0)),
         "DXY (DX-Y.NYB)": ("DX-Y.NYB", (17, 0)), "Nasdaq (^IXIC)": ("^IXIC", (16, 0))}
CACHE_TU = dt.datetime(2026, 3, 1, tzinfo=UTC)          # cache ngoài (Yahoo/CMC) từ đây
TRE = {"fng": dt.timedelta(hours=1), "yahoo": dt.timedelta(minutes=30), "cmc": dt.timedelta(hours=1)}  # độ trễ công bố bảo thủ
NEN_BO_SUNG_TU = {"1Dutc": "2017-01-01", "4H": "2024-01-01"}  # lịch sử dài cho EMA200/610

Nen = namedtuple("Nen", "mo dong o h l c")


# ───────────────────────── tải + cache ─────────────────────────
def lay_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for lan in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception:
            if lan == 3:
                raise
            time.sleep(2 * (lan + 1))


def cache(ten, url_fn, tai_lai):
    p = DL / ten
    if tai_lai or not p.exists():
        DL.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(lay_json(url_fn()), ensure_ascii=False), encoding="utf-8")
        print(f"  ↓ {ten}", file=sys.stderr)
    return json.loads(p.read_text(encoding="utf-8"))


def tai_nen_bo_sung(khung, tai_lai):
    """Cùng API/quy ước với cong_cu/lay_nen.py (OKX, chỉ nến đã đóng) nhưng ghi vào thi/du_lieu/
    để không đụng file chung du_lieu/. Dùng cho lịch sử dài (EMA200/610) và nến sau dữ liệu sẵn có."""
    p = DL / f"btc_{khung}_bo_sung.csv"
    if p.exists() and not tai_lai:
        return p
    DL.mkdir(parents=True, exist_ok=True)
    tu_ms = int(dt.datetime.fromisoformat(NEN_BO_SUNG_TU[khung]).replace(tzinfo=UTC).timestamp() * 1000)
    after, ra = int(time.time() * 1000), {}
    while after > tu_ms:
        d = lay_json(OKX.format(khung, after))["data"]
        if not d:
            break
        for ts, o, h, l, c, v, *_, xac_nhan in d:
            if xac_nhan == "1" and int(ts) >= tu_ms:
                k = dt.datetime.fromtimestamp(int(ts) / 1000, UTC).strftime("%Y-%m-%d %H:%M")
                ra[k] = (k, o, h, l, c, v)
        after = int(d[-1][0])
        time.sleep(0.15)
    with p.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["ts_utc", "open", "high", "low", "close", "vol"]); w.writerows(sorted(ra.values()))
    print(f"  ↓ {p.name}: {len(ra)} nến {min(ra)} → {max(ra)}", file=sys.stderr)
    return p


def doc_csv(p):
    with p.open() as f:
        return {r["ts_utc"]: tuple(float(r[k]) for k in ("open", "high", "low", "close")) for r in csv.DictReader(f)}


def nap_nen(khung, do_dai, tai_lai):
    gop_ = doc_csv(tai_nen_bo_sung(khung, tai_lai))
    gop_.update(doc_csv(GOC / "du_lieu" / f"btc_{khung}.csv"))  # file chung du_lieu/ được ưu tiên khi trùng
    ra = []
    for k in sorted(gop_):
        mo = dt.datetime.strptime(k, "%Y-%m-%d %H:%M").replace(tzinfo=UTC)
        ra.append(Nen(mo, mo + do_dai, *gop_[k]))
    return ra


def lo_hong(nens, do_dai):
    return [(a.mo, b.mo) for a, b in zip(nens, nens[1:]) if b.mo - a.mo != do_dai]


# ───────────────────────── dữ liệu toàn bộ (nạp 1 lần) ─────────────────────────
class DuLieu:
    def __init__(self, tai_lai=False):
        self.h4 = nap_nen("4H", GIO4, tai_lai)
        self.d1 = nap_nen("1Dutc", NGAY, tai_lai)
        self.h1 = [Nen(mo, mo + dt.timedelta(hours=1), *v) for mo, v in
                   ((dt.datetime.strptime(k, "%Y-%m-%d %H:%M").replace(tzinfo=UTC), v)
                    for k, v in sorted(doc_csv(GOC / "du_lieu" / "btc_1H.csv").items()))]
        self.dong_h4 = [n.dong for n in self.h4]
        self.dong_d1 = [n.dong for n in self.d1]
        bay_gio = int(time.time())
        fng = cache("fng.json", lambda: "https://api.alternative.me/fng/?limit=0", tai_lai)["data"]
        self.fng = sorted((dt.datetime.fromtimestamp(int(x["timestamp"]), UTC), int(x["value"]), x["value_classification"])
                          for x in fng)
        self.yahoo = {}
        for ten, (ma, gio_dong) in YAHOO.items():
            url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(ma)}"
                   f"?interval=1d&period1={int(CACHE_TU.timestamp())}&period2={bay_gio}")
            r = cache(f"yahoo_{re.sub(r'[^A-Za-z0-9]', '_', ma)}.json", lambda u=url: u, tai_lai)["chart"]["result"][0]
            theo_ngay = {}
            for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]):
                if c is not None:
                    theo_ngay[dt.datetime.fromtimestamp(t, NY).date()] = c
            self.yahoo[ten] = [(d, dt.datetime.combine(d, dt.time(*gio_dong), NY).astimezone(UTC), theo_ngay[d])
                               for d in sorted(theo_ngay)]
        t0 = int(CACHE_TU.timestamp())
        g = cache("cmc_global.json", lambda: "https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/historical"
                  f"?format=chart&interval=1d&timeStart={t0}&timeEnd={bay_gio}", tai_lai)["data"]["quotes"]
        # ảnh chụp tại đúng mốc timestamp (đã đối chiếu: vốn hoá BTC ở 07-02T00:00 = giá đóng D1 07-01)
        self.cmc = sorted((dt.datetime.fromisoformat(q["timestamp"].replace("Z", "+00:00")), q["btcDominance"],
                           q["quote"][0]["totalMarketCap"]) for q in g)
        u = cache("cmc_usdt.json", lambda: "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical"
                  f"?id=825&convertId=2781&timeStart={t0}&timeEnd={bay_gio}&interval=1d", tai_lai)["data"]["quotes"]
        # vốn hoá USDT lúc ĐÓNG ngày (timeClose 23:59:59.999)
        self.usdt = sorted((dt.datetime.fromisoformat(q["timeClose"].replace("Z", "+00:00")), q["quote"]["marketCap"]) for q in u)

    def cat_tuong_lai(self, C):
        """Bản sao đã XOÁ mọi dữ liệu có event_time > C (dùng cho phép thử rò rỉ)."""
        x = object.__new__(DuLieu)
        x.h4 = [n for n in self.h4 if n.dong <= C]; x.d1 = [n for n in self.d1 if n.dong <= C]
        x.h1 = [n for n in self.h1 if n.dong <= C]
        x.dong_h4 = [n.dong for n in x.h4]; x.dong_d1 = [n.dong for n in x.d1]
        x.fng = [v for v in self.fng if v[0] <= C]
        x.yahoo = {k: [v for v in ds if v[1] <= C] for k, ds in self.yahoo.items()}
        x.cmc = [v for v in self.cmc if v[0] <= C]; x.usdt = [v for v in self.usdt if v[0] <= C]
        return x

    def gia_dong_luc(self, t):
        """Giá đóng của nến H4 đóng đúng lúc t (dùng cho chấm điểm, có thể là sau T)."""
        i = bisect_right(self.dong_h4, t) - 1
        return self.h4[i].c if i >= 0 and self.h4[i].dong == t else None


# ───────────────────────── buổi live ─────────────────────────
Buoi = namedtuple("Buoi", "ten ngay hhmm vid bat_dau ket_thuc C T phieu moc chac nguon_gio")


def moc_h4_truoc(luc):
    """Giờ đóng của nến H4 căn UTC gần nhất đã đóng tại/ trước `luc` (UTC)."""
    return luc.replace(hour=luc.hour // 4 * 4, minute=0, second=0, microsecond=0)


def ds_buoi():
    phut, that = {}, {}
    p = GOC / "transcripts" / "danh_sach.tsv"
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8"), delimiter="\t"):
            if (r.get("phut") or "").isdigit():
                phut[r["id"]] = int(r["phut"])
    p = GOC / "transcripts" / "gio_live.tsv"
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8"), delimiter="\t"):
            try:
                bd = dt.datetime.strptime(r["bat_dau_vn"].strip(), "%Y-%m-%d %H:%M").replace(tzinfo=VN).astimezone(UTC)
                that[r["id"]] = (bd, int(r["phut"]), r.get("nguon_gio") or "?")
            except (KeyError, ValueError, TypeError):
                pass
    mocs = {}
    for q in (GOC / "moc").glob("2*.json"):
        m = MAU_TEN.match(q.stem)
        if m:
            mocs[m[3]] = q
    ra = []
    for q in (GOC / "phieu").glob("2*.json"):
        m = MAU_TEN.match(q.stem)
        if not m:
            print(f"! bỏ qua tên lạ: {q.name}", file=sys.stderr); continue
        ngay, hhmm, vid = m.groups()
        if vid in that:
            bd, ph, nguon = that[vid]; chac = True
        else:
            bd = dt.datetime.strptime(ngay + (hhmm or "1000"), "%Y-%m-%d%H%M").replace(tzinfo=VN).astimezone(UTC)
            ph, nguon, chac = phut.get(vid, PHUT_MAC_DINH), ("tên file" if hhmm else "mặc định 10:00"), False
        C = bd + dt.timedelta(minutes=ph)
        ra.append(Buoi(q.stem, ngay, hhmm, vid, bd, C, C, moc_h4_truoc(C), q, mocs.get(vid), chac, nguon))
    ra.sort(key=lambda b: (b.bat_dau, b.ten))
    return ra


def buoi_thi(tat_ca):
    return [b for b in tat_ca if TU_THI <= b.ngay <= DEN_THI]


def buoi_truoc(tat_ca, b):
    """Các buổi đã KẾT THÚC trước khi buổi b bắt đầu (cũ → mới). Không bao giờ gồm b hay buổi sau b."""
    return [x for x in tat_ca if x.ket_thuc <= b.bat_dau and x.ten != b.ten]


def doc_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def huong_h4(phieu):
    """Hướng H4 của phiếu/bài làm: phần tử khung H4, không có thì 'chung'; không có cả hai → None."""
    nd = phieu.get("nhan_dinh") or []
    for k in ("H4", "chung"):
        for x in nd:
            if x.get("khung") == k:
                return x
    return None


# ───────────────────────── dữ liệu cắt tại T ─────────────────────────
def tuan(mo):
    bd = (mo - dt.timedelta(days=mo.weekday())).replace(hour=0, minute=0)
    return bd, bd + dt.timedelta(days=7)


def thang(mo):
    bd = mo.replace(day=1, hour=0, minute=0)
    return bd, (bd + dt.timedelta(days=32)).replace(day=1)


def ngay_utc(mo):
    bd = mo.replace(hour=0, minute=0)
    return bd, bd + NGAY


def gop(nens, khoa):
    ra = []
    for n in nens:
        bd, kt = khoa(n.mo)
        if ra and ra[-1][0] == bd:
            x = ra[-1]; x[3] = max(x[3], n.h); x[4] = min(x[4], n.l); x[5] = n.c; x[6] += 1
        else:
            ra.append([bd, kt, n.o, n.h, n.l, n.c, 1])
    return [(Nen(*x[:6]), x[6]) for x in ra]


class Cat:
    """Mọi dữ liệu của 1 buổi thi, đã cắt tại mốc C (kết thúc live). Mọi phép tính hồ sơ chỉ đọc từ đây."""

    def __init__(self, du, C):
        self.C = C
        self.T = T = moc_h4_truoc(C)  # giờ đóng nến H4 cuối ≤ C
        self.dau = []  # (tên nguồn, event_time, available_at)
        self.h4 = du.h4[:bisect_right(du.dong_h4, C)]
        self.d1 = du.d1[:bisect_right(du.dong_d1, C)]
        self.h1 = [n for n in du.h1 if n.dong <= C][-1:]
        self.gia = self.h4[-1].c
        # nến đang chạy (chưa đóng tại C) dựng tạm từ các nến H4 đã đóng ≤ C
        self.dang = {}
        for ten, khoa in (("D1", ngay_utc), ("W1", tuan), ("MN", thang)):
            bd, kt = khoa(T)
            con = [n for n in self.h4 if n.mo >= bd]
            self.dang[ten] = gop(con, lambda m, bd=bd, kt=kt: (bd, kt))[0][0] if con else None
        # W1/tháng đã hoàn tất: gộp từ D1 đã đóng, chỉ giữ bucket kết thúc ≤ C và đủ ngày
        self.w1 = [n for n, so in gop(self.d1, tuan) if n.dong <= C and so == 7]
        self.mn = [n for n, so in gop(self.d1, thang) if n.dong <= C and so == (n.dong - n.mo).days]
        self.fng = [x for x in du.fng if x[0] + TRE["fng"] <= C]
        self.yahoo = {k: [x for x in v if x[1] + TRE["yahoo"] <= C] for k, v in du.yahoo.items()}
        self.cmc = [x for x in du.cmc if x[0] + TRE["cmc"] <= C]
        self.usdt = [x for x in du.usdt if x[0] + TRE["cmc"] <= C]
        for ten, t in (("H4 (giờ đóng)", self.h4[-1].dong), ("D1 (giờ đóng)", self.d1[-1].dong),
                       ("W1 hoàn tất (giờ đóng)", self.w1[-1].dong), ("Tháng hoàn tất (giờ đóng)", self.mn[-1].dong)):
            self.dau.append((ten, t, t))
        if self.h1:
            self.dau.append(("H1 (giờ đóng, chỉ để báo giá gần nhất)", self.h1[-1].dong, self.h1[-1].dong))
        for ten, n in self.dang.items():
            if n:
                t = max(x.dong for x in self.h4 if x.mo >= n.mo)
                self.dau.append((f"{ten} đang chạy: nến H4 cuối gộp vào", t, t))
        if self.fng: self.dau.append(("Fear & Greed (mốc ngày UTC)", self.fng[-1][0], self.fng[-1][0] + TRE["fng"]))
        for k, v in self.yahoo.items():
            if v: self.dau.append((f"{k} (giờ đóng phiên)", v[-1][1], v[-1][1] + TRE["yahoo"]))
        if self.cmc: self.dau.append(("CMC BTC.D/tổng vốn hoá (ảnh chụp)", self.cmc[-1][0], self.cmc[-1][0] + TRE["cmc"]))
        if self.usdt: self.dau.append(("CMC vốn hoá USDT (đóng ngày)", self.usdt[-1][0], self.usdt[-1][0] + TRE["cmc"]))

    def kiem(self, buoi_dung, b):
        for ten, t, co in self.dau:
            if t > self.C or co > self.C:
                raise RuntimeError(f"RÒ RỈ: {ten} {t}/{co} > C {self.C}")
        for x in buoi_dung:
            if x.ket_thuc > b.bat_dau or x.ten == b.ten:
                raise RuntimeError(f"RÒ RỈ: buổi {x.ten} kết thúc {x.ket_thuc} sau khi buổi thi bắt đầu {b.bat_dau}")


# ───────────────────────── chỉ báo ─────────────────────────
def ema(xs, n):
    """EMA khởi tạo bằng SMA n nến đầu; thiếu nến → None."""
    if len(xs) < n:
        return None
    a, e = 2 / (n + 1), sum(xs[:n]) / n
    ra = [e]
    for x in xs[n:]:
        e = a * x + (1 - a) * e; ra.append(e)
    return ra


def rsi(xs, n=14):
    if len(xs) < n + 1:
        return None
    lai = [max(b - a, 0) for a, b in zip(xs, xs[1:])]
    lo = [max(a - b, 0) for a, b in zip(xs, xs[1:])]
    ag, al = sum(lai[:n]) / n, sum(lo[:n]) / n
    for g, l in zip(lai[n:], lo[n:]):
        ag, al = (ag * (n - 1) + g) / n, (al * (n - 1) + l) / n
    return 100.0 if al == 0 else 100 - 100 / (1 + ag / al)


def fractal(nens, k, tu):
    ra = []
    for i in range(k, len(nens) - k):
        n = nens[i]
        if n.mo < tu:
            continue
        if all(n.h > nens[j].h for j in range(i - k, i)) and all(n.h >= nens[j].h for j in range(i + 1, i + k + 1)):
            ra.append((i, "đỉnh", n.h))
        if all(n.l < nens[j].l for j in range(i - k, i)) and all(n.l <= nens[j].l for j in range(i + 1, i + k + 1)):
            ra.append((i, "đáy", n.l))
    return ra


def doi_gia_luc(cat, t):
    i = bisect_right([n.dong for n in cat.h4], t) - 1
    return cat.h4[i].c if i >= 0 and cat.h4[i].dong == t else None


# ───────────────────────── định dạng ─────────────────────────
def g(x):
    return "—" if x is None else f"{x:,.0f}".replace(",", ".")


def pct(x, dau=True):
    return "—" if x is None else (f"{x:+.2f}%" if dau else f"{x:.2f}%")


def vn(t, fmt="%Y-%m-%d %H:%M"):
    return t.astimezone(VN).strftime(fmt)


def bang_nen(ds, nhan):
    rows = ["| Nến | O | H | L | C | Thân % | Râu trên % | Râu dưới % | Biên % |", "|---|---|---|---|---|---|---|---|---|"]
    for n, dang in ds:
        than = (n.c - n.o) / n.o * 100
        rows.append(f"| {nhan(n)}{' (đang chạy, tới T)' if dang else ''} | {g(n.o)} | {g(n.h)} | {g(n.l)} | {g(n.c)} | "
                    f"{pct(than)} | {(n.h - max(n.o, n.c)) / n.o * 100:.2f}% | {(min(n.o, n.c) - n.l) / n.o * 100:.2f}% | "
                    f"{(n.h - n.l) / n.o * 100:.2f}% |")
    return "\n".join(rows)


# ───────────────────────── các phần hồ sơ ─────────────────────────
def phan_a(b, cat, truoc):
    gl = b.bat_dau.astimezone(VN)
    cung_thang = [x for x in truoc if x.bat_dau.astimezone(VN).strftime("%Y-%m") == gl.strftime("%Y-%m")]
    cung_tuan = [x for x in truoc if tuan(x.bat_dau.astimezone(VN).replace(tzinfo=UTC))[0] == tuan(gl.replace(tzinfo=UTC))[0]]
    L = ["## a. Thời điểm",
         f"- Giờ live: **{vn(b.bat_dau)} → {vn(b.ket_thuc, '%H:%M')} VN** ({THU[gl.weekday()]}, "
         f"{(b.ket_thuc - b.bat_dau).total_seconds() / 60:.0f} phút) · nguồn giờ: {b.nguon_gio}"
         + ("" if b.chac else " · **GIỜ KHÔNG CHẮC** (chưa có giờ live thật; thứ tự buổi trước có thể sai)"),
         f"- Thứ Hai: **{'CÓ' if gl.weekday() == 0 else 'không'}** · Ngày 1 của tháng: **{'CÓ' if gl.day == 1 else 'không'}** · "
         f"Buổi live đầu tiên của tháng: **{'CÓ' if not cung_thang else 'không'}** · Buổi đầu tiên của tuần: **{'CÓ' if not cung_tuan else 'không'}**",
         f"- **Mốc cắt dữ liệu C = {vn(cat.C)} VN** (lúc kết thúc live; nhận định của bạn được so với view CUỐI buổi của người đó)",
         f"- Nến H4 cuối đã đóng: mở {vn(cat.h4[-1].mo, '%H:%M')} → đóng **T = {vn(cat.T)} VN** ({cat.T:%Y-%m-%d %H:%M} UTC); "
         f"giá đóng H4 = **{g(cat.gia)}** (mọi so sánh giá trong hồ sơ dùng số này)"
         + (f" · giá đóng H1 gần nhất ({vn(cat.h1[-1].dong, '%H:%M')} VN): {g(cat.h1[-1].c)}" if cat.h1 else ""),
         "- Nguồn BTC: OKX BTC-USDT spot (chart người đó hay dùng có thể là Binance BTCUSDT.P — giá/râu/volume có thể lệch nhẹ).",
         "- Dữ liệu mới nhất đã dùng (thời điểm sự kiện → thời điểm coi là đã biết; đều ≤ C):"]
    L += [f"  - {ten}: {vn(t)}" + (f" → {vn(co)}" if co != t else "") + " VN" for ten, t, co in cat.dau]
    return "\n".join(L)


def phan_b(cat):
    L = ["## b. Nến BTC (OKX BTC-USDT, căn UTC; giờ ghi theo VN)", "### 12 nến H4 gần nhất (đã đóng; cột Nến = giờ MỞ nến theo VN)",
         bang_nen([(n, False) for n in cat.h4[-12:]], lambda n: vn(n.mo, "%Y-%m-%d %H:%M"))]
    d1 = [(n, False) for n in cat.d1[-10:]] + ([(cat.dang["D1"], True)] if cat.dang["D1"] else [])
    L += ["### 10 nến D1 gần nhất (ngày UTC, mở 07:00 VN)", bang_nen(d1, lambda n: n.mo.strftime("%Y-%m-%d") + f" {THU[n.mo.weekday()][4:]}")]
    w1 = [(n, False) for n in cat.w1[-8:]] + ([(cat.dang["W1"], True)] if cat.dang["W1"] else [])
    L += ["### 8 nến W1 gần nhất (tuần bắt đầu thứ Hai 00:00 UTC)", bang_nen(w1, lambda n: "tuần " + n.mo.strftime("%Y-%m-%d"))]
    mn = [(n, False) for n in cat.mn[-3:]] + ([(cat.dang["MN"], True)] if cat.dang["MN"] else [])
    L += ["### Nến tháng: 3 tháng trước + tháng hiện tại", bang_nen(mn, lambda n: "tháng " + n.mo.strftime("%Y-%m"))]
    if not cat.dang["MN"]:
        L.append(f"_Tháng {cat.T.strftime('%Y-%m')} chưa có nến nào đóng tại T (T là lúc mở tháng)._")
    return "\n".join(L)


NGUONG_CHUM = {"H4": 0.6, "D1": 1.5, "W1": 3.0}


def phan_c(cat):
    L = ["## c. EMA (không dùng SMA; tính trên nến ĐÃ ĐÓNG ≤ T, khởi tạo bằng SMA n nến đầu)",
         f"Giá so sánh = giá tại T: {g(cat.gia)}. Dốc = thay đổi của đường trong 5 nến gần nhất.",
         f"Lịch sử dùng: H4 từ {cat.h4[0].mo:%Y-%m-%d} ({len(cat.h4)} nến), D1 từ {cat.d1[0].mo:%Y-%m-%d} ({len(cat.d1)} nến), "
         f"W1 {len(cat.w1)} nến hoàn tất."]
    for khung, nens in (("H4", cat.h4), ("D1", cat.d1), ("W1", cat.w1)):
        c, h, l = [n.c for n in nens], [n.h for n in nens], [n.l for n in nens]
        dg = {"EMA34 high": ema(h, 34), "EMA34 low": ema(l, 34), "EMA34 close": ema(c, 34),
              "EMA89": ema(c, 89), "EMA200": ema(c, 200), "EMA610": ema(c, 610)}
        L += [f"### {khung}", "| Đường | Giá trị | Giá T so với đường | Dốc 5 nến |", "|---|---|---|---|"]
        for ten, s in dg.items():
            if s is None:
                L.append(f"| {ten} | không đủ ({len(nens)} nến < {ten.split()[0][3:]}) | — | — |"); continue
            v = s[-1]
            doc_ = (s[-1] / s[-6] - 1) * 100 if len(s) >= 6 else None
            L.append(f"| {ten} | {g(v)} | {'trên' if cat.gia > v else 'dưới'} {pct((cat.gia / v - 1) * 100)} | {pct(doc_)} |")
        if dg["EMA34 high"]:
            hi, lo = dg["EMA34 high"][-1], dg["EMA34 low"][-1]
            vt = "TRÊN dải" if cat.gia > hi else ("DƯỚI dải" if cat.gia < lo else "TRONG dải")
            L.append(f"- Dải EMA34 (low–high) {g(lo)}–{g(hi)}: giá **{vt}**")
        co = {k: dg[k][-1] for k in ("EMA34 close", "EMA89", "EMA200", "EMA610") if dg[k]}
        if len(co) >= 3:
            ba = [co[k] for k in ("EMA34 close", "EMA89", "EMA200") if k in co]
            gian = (max(ba) - min(ba)) / cat.gia * 100
            L.append(f"- Độ chụm EMA34/89/200 = (max−min)/giá = **{gian:.2f}%** → "
                     f"{'**CHỤM**' if gian < NGUONG_CHUM[khung] else 'không chụm'} (ngưỡng tham khảo {khung} < {NGUONG_CHUM[khung]}%)")
            thu_tu = sorted(co, key=co.get, reverse=True)
            L.append("- Thứ tự từ trên xuống: " + " > ".join(f"{k.replace(' close', '')}" for k in thu_tu)
                     + f" · giá đang ở vị trí {sum(cat.gia < v for v in co.values()) + 1}/{len(co) + 1} (1 = trên cùng)")
    return "\n".join(L)


def fibo_dong(nhan, a, b, gia):
    """Sóng từ điểm a=(thời điểm, giá) đến b. Mức hồi tính ngược từ b về a."""
    (ta, pa), (tb, pb) = a, b
    bien = pb - pa
    if bien == 0:
        return f"| {nhan} | phẳng | | | | | |"
    lv = {r: pb - r * bien for r in (0.382, 0.5, 0.618, 0.786)}
    hoi = (pb - gia) / bien
    return (f"| {nhan} | {'TĂNG' if bien > 0 else 'GIẢM'} {g(pa)} ({ta}) → {g(pb)} ({tb}) | "
            + " | ".join(g(lv[r]) for r in (0.382, 0.5, 0.618, 0.786)) + f" | {hoi:.3f} |")


def song_lon_nhat(nens, nhan):
    ih = max(range(len(nens)), key=lambda i: nens[i].h)
    il = min(range(len(nens)), key=lambda i: nens[i].l)
    H, Lw = (nhan(nens[ih]), nens[ih].h), (nhan(nens[il]), nens[il].l)
    return (Lw, H) if il < ih else (H, Lw)


def phan_d(cat):
    L = ["## d. Cấu trúc, Fibo, động lượng"]
    nh = lambda n: vn(n.mo, "%Y-%m-%d %H:%M")
    nd = lambda n: n.mo.strftime("%Y-%m-%d")
    for khung, nens, k, ngay, nhan in (("H4", cat.h4, 3, 30, nh), ("D1", cat.d1, 5, 180, nd)):
        fr = fractal(nens, k, cat.T - dt.timedelta(days=ngay))
        L += [f"### Đỉnh/đáy fractal {khung} ({ngay} ngày, {k} nến mỗi bên; chỉ nến đã đóng)",
              "| Lúc (mở nến) | Loại | Giá | Xác nhận lúc (nến thứ k bên phải đóng) | Sau đó (giá đóng tới C) |", "|---|---|---|---|---|"]
        for i, loai, p in fr:
            sau = [n.c for n in nens[i + 1:]]
            if loai == "đỉnh":
                tt = f"ĐÃ bị đóng vượt (max đóng {g(max(sau))})" if max(sau) > p else "chưa bị vượt"
            else:
                tt = f"ĐÃ bị đóng thủng (min đóng {g(min(sau))})" if min(sau) < p else "chưa bị thủng"
            L.append(f"| {nhan(nens[i])} | {loai} | {g(p)} | {vn(nens[i + k].dong)} | {tt} |")
        if not fr:
            L.append("| — | không có | | | |")
    # Fibo
    d1x = cat.d1 + ([cat.dang["D1"]] if cat.dang["D1"] else [])
    L += ["### Fibo hồi (mức = điểm cuối sóng lùi lại r × biên độ)",
          "Cột 'Giá T đã hồi' = (điểm cuối − giá T)/biên độ: 0 = đang ở điểm cuối sóng, 1 = về hết điểm đầu.",
          "| Sóng | Hướng: đầu → cuối | 0.382 | 0.5 | 0.618 | 0.786 | Giá T đã hồi |", "|---|---|---|---|---|---|---|"]
    a, b = song_lon_nhat(d1x[-180:], nd)
    L.append(fibo_dong("D1 lớn nhất 180 ngày", a, b, cat.gia))
    a, b = song_lon_nhat(d1x[-30:], nd)
    L.append(fibo_dong("D1 30 ngày", a, b, cat.gia))
    fr = fractal(cat.h4, 3, cat.T - dt.timedelta(days=30))
    xen = []  # nén các pivot cùng loại liên tiếp → giữ cực trị
    for i, loai, p in fr:
        if xen and xen[-1][1] == loai:
            if (loai == "đỉnh" and p >= xen[-1][2]) or (loai == "đáy" and p <= xen[-1][2]):
                xen[-1] = (i, loai, p)
        else:
            xen.append((i, loai, p))
    if len(xen) >= 2:
        (i1, _, p1), (i2, l2, p2) = xen[-2], xen[-1]
        L.append(fibo_dong("Nhịp H4 vừa hoàn tất (fractal → fractal)", (nh(cat.h4[i1]), p1), (nh(cat.h4[i2]), p2), cat.gia))
    if xen:
        i2, l2, p2 = xen[-1]
        sau = cat.h4[i2 + 1:]
        j = (min if l2 == "đỉnh" else max)(range(len(sau)), key=lambda t: sau[t].l if l2 == "đỉnh" else sau[t].h)
        cuc = sau[j].l if l2 == "đỉnh" else sau[j].h
        L.append(fibo_dong(f"Nhịp H4 đang chạy (từ {l2} fractal cuối)", (nh(cat.h4[i2]), p2), (nh(sau[j]), cuc), cat.gia))
    # động lượng
    r4, rd = rsi([n.c for n in cat.h4]), rsi([n.c for n in cat.d1])
    L += ["### Động lượng", f"- RSI14 H4: **{r4:.1f}** · RSI14 D1: **{rd:.1f}** (Wilder, nến đã đóng)"]
    doi = []
    for nhan_, gio in (("24h", 24), ("72h", 72), ("7 ngày", 168), ("30 ngày", 720)):
        p0 = doi_gia_luc(cat, cat.T - dt.timedelta(hours=gio))
        doi.append(f"{nhan_}: **{pct((cat.gia / p0 - 1) * 100) if p0 else '—'}**")
    L.append("- Thay đổi giá tới T: " + " · ".join(doi))
    e89 = ema([n.c for n in cat.d1], 89)
    if e89:
        L.append(f"- Khoảng cách tới EMA89 D1 ({g(e89[-1])}): giá T {pct((cat.gia / e89[-1] - 1) * 100)} · "
                 f"đóng D1 cuối ({g(cat.d1[-1].c)}) {pct((cat.d1[-1].c / e89[-1] - 1) * 100)}")
    return "\n".join(L)


def phan_e(cat):
    L = ["## e. Bối cảnh khác (chỉ giá trị đã công bố trước C)", "### Fear & Greed (alternative.me, giá trị ngày UTC)"]
    if cat.fng:
        L.append(" · ".join(f"{t:%m-%d}: **{v}** ({c})" for t, v, c in cat.fng[-7:]))
    else:
        L.append("không có dữ liệu")
    L += ["### Vĩ mô (Yahoo daily, phiên đã đóng ≥ 30 phút trước C)", "| Mã | Phiên đóng gần nhất | Giá đóng | 1 phiên | 5 phiên |", "|---|---|---|---|---|"]
    for ten, ds in cat.yahoo.items():
        if len(ds) < 6:
            L.append(f"| {ten} | không đủ dữ liệu | | | |"); continue
        d, _, c = ds[-1]
        L.append(f"| {ten} | {d:%Y-%m-%d} ({THU[d.weekday()]}) | {c:,.2f} | {pct((c / ds[-2][2] - 1) * 100)} | {pct((c / ds[-6][2] - 1) * 100)} |")
    L.append("### Độ thống trị — PROXY từ CoinMarketCap data-api (ảnh chụp 00:00 UTC), KHÔNG phải chuỗi CRYPTOCAP của TradingView")
    if len(cat.cmc) >= 8:
        t, d0, tong = cat.cmc[-1]
        L.append(f"- BTC.D (proxy) lúc {vn(t)} VN: **{d0:.2f}%** · đổi 1 ngày {d0 - cat.cmc[-2][1]:+.2f} điểm · 7 ngày {d0 - cat.cmc[-8][1]:+.2f} điểm")
        usdt = {x[0].date(): x[1] for x in cat.usdt}
        dom = []
        for t2, _, tong2 in cat.cmc[-8:]:
            m = usdt.get((t2 - NGAY).date())  # vốn hoá USDT lúc đóng ngày liền trước = cùng thời điểm ảnh chụp
            dom.append(m / tong2 * 100 if m else None)
        if dom[-1] is not None:
            L.append(f"- USDT.D (proxy = vốn hoá USDT / tổng vốn hoá) lúc {vn(t)} VN: **{dom[-1]:.2f}%**"
                     + (f" · đổi 1 ngày {dom[-1] - dom[-2]:+.2f} điểm" if dom[-2] is not None else "")
                     + (f" · 7 ngày {dom[-1] - dom[0]:+.2f} điểm" if dom[0] is not None else ""))
        else:
            L.append("- USDT.D: không có dữ liệu lịch sử cho ngày này")
    else:
        L.append("- BTC.D / USDT.D: không có dữ liệu lịch sử")
    return "\n".join(L)


VAI_TRO = {"ho_tro": "hỗ trợ", "khang_cu": "kháng cự", "dich": "đích", "entry": "vào lệnh", "tp": "TP", "sl": "SL",
           "vo_hieu": "vô hiệu", "khac": "khác", "nhac_lai": "nhắc lại", "day_cu": "đáy cũ", "dinh_cu": "đỉnh cũ"}


def trang_thai_moc(m, nens, gia_noi, gia_T):
    if not isinstance(m.get("gia"), (int, float)):
        return "không có số giá"
    lo, hi = sorted([m["gia"], m["gia_tren"] if isinstance(m.get("gia_tren"), (int, float)) else m["gia"]])
    vi_tri = "giá T trên vùng" if gia_T > hi else ("giá T dưới vùng" if gia_T < lo else "giá T trong vùng")
    if not nens:
        return f"chưa có nến H4 đóng sau lúc nói · {vi_tri}"
    cmax, cmin = max(n.c for n in nens), min(n.c for n in nens)
    hmax, lmin = max(n.h for n in nens), min(n.l for n in nens)
    cham = lmin <= hi and hmax >= lo
    vt, hg = m.get("vai_tro"), m.get("huong")
    tren = (lo > gia_noi) if isinstance(gia_noi, (int, float)) else (hg == "GIAM")  # mốc nằm trên giá lúc nói?
    if vt in ("ho_tro", "day_cu"):
        s = f"ĐÃ PHÁ (đóng H4 thấp nhất {g(cmin)})" if cmin < lo else ("giữ, đã test" if cham else "giữ, chưa test")
    elif vt in ("khang_cu", "dinh_cu"):
        s = f"ĐÃ PHÁ (đóng H4 cao nhất {g(cmax)})" if cmax > hi else ("giữ, đã test" if cham else "giữ, chưa test")
    elif vt == "vo_hieu":
        if tren:
            s = f"ĐÃ KÍCH HOẠT (đóng H4 cao nhất {g(cmax)})" if cmax > lo else "chưa kích hoạt"
        else:
            s = f"ĐÃ KÍCH HOẠT (đóng H4 thấp nhất {g(cmin)})" if cmin < hi else "chưa kích hoạt"
    elif vt == "dich":
        s = ("ĐÃ TỚI" if (hmax >= lo if tren else lmin <= hi) else "chưa tới")
    else:
        s = "đã chạm" if cham else "chưa chạm"
    return f"{s} · {vi_tri}"


def bang_moc(b, cat):
    if not b.moc:
        return "_Không có file mốc._"
    d = doc_json(b.moc)
    nens = [n for n in cat.h4 if n.dong > b.bat_dau]
    rows = [f"Bản đồ mốc (giá lúc nói ~{g(d.get('gia_btc_luc_noi'))}; trạng thái tính bằng {len(nens)} nến H4 ĐÓNG từ lúc nói tới C — "
            "phá = giá đóng H4 vượt mốc, chạm/tới = râu chạm):",
            "| Giá | Vai trò | Hướng | Khung | Căn cứ | Tới C |", "|---|---|---|---|---|---|"]
    for m in d.get("moc", []):
        gia = g(m.get("gia")) + (f"–{g(m['gia_tren'])}" if m.get("gia_tren") else "")
        cc = "; ".join(m.get("can_cu") or [])
        rows.append(f"| {gia} | {VAI_TRO.get(m.get('vai_tro'), m.get('vai_tro'))}{'' if m.get('chac', True) else ' (?)'} | "
                    f"{m.get('huong') or '—'} | {m.get('khung') or '—'} | {cc.replace('|', '/')} | "
                    f"{trang_thai_moc(m, nens, d.get('gia_btc_luc_noi'), cat.gia)} |")
    return "\n".join(rows)


def dong_nd(x):
    p = [f"**[{x.get('khung')}] {x.get('huong')}** (chắc: {x.get('do_chac')})"]
    for k, nhan in (("dich", "đích"), ("han", "hạn"), ("vo_hieu_khi", "vô hiệu khi"), ("kich_ban_phu", "kịch bản phụ")):
        if x.get(k) not in (None, "", []):
            p.append(f"{nhan}: {x[k]}")
    if x.get("ly_do"):
        p.append("lý do: " + "; ".join(x["ly_do"]))
    if x.get("trich"):
        p.append(f"trích: “{x['trich']}”")
    return "- " + " · ".join(p)


def phan_f(b, cat, truoc):
    L = ["## f. Lời người đó ở các buổi TRƯỚC (đã nói công khai, buổi đã kết thúc trước khi buổi này bắt đầu)"]
    if not truoc:
        return "\n".join(L + ["_Không có buổi nào trước T._"])
    lien = truoc[-1]
    L += [f"### Buổi liền trước: {lien.ten} — live {vn(lien.bat_dau)} VN (cách C {(cat.C - lien.bat_dau).total_seconds() / 3600:.0f} giờ)"
          + ("" if lien.chac else " · giờ không chắc"),
          "Phiếu đầy đủ:", "```json", json.dumps(doc_json(lien.phieu), ensure_ascii=False, indent=1), "```", bang_moc(lien, cat)]
    L.append("### 5 buổi trước đó: view khung lớn (D1/W1/chung) + bản đồ mốc")
    for x in reversed(truoc[-6:-1]):
        d = doc_json(x.phieu)
        L.append(f"#### {x.ten} — live {vn(x.bat_dau)} VN (cách C {(cat.C - x.bat_dau).total_seconds() / 86400:.1f} ngày)"
                 + ("" if x.chac else " · giờ không chắc"))
        lon = [n for n in d.get("nhan_dinh", []) if n.get("khung") in ("D1", "W1", "chung")]
        L += [dong_nd(n) for n in lon] or ["- (không có nhận định D1/W1/chung)"]
        L.append(bang_moc(x, cat))
    return "\n".join(L)


def lap_ho_so(du, tat_ca, b):
    cat = Cat(du, b.C)
    truoc = buoi_truoc(tat_ca, b)
    dung = truoc[-6:]
    cat.kiem(dung, b)
    phan = [f"# Hồ sơ buổi thi {b.ten}",
            "> Chỉ gồm dữ liệu đã biết được trước mốc C (kết thúc live). KHÔNG có phiếu/mốc/transcript của buổi này hay buổi sau.",
            phan_a(b, cat, truoc), phan_b(cat), phan_c(cat), phan_d(cat), phan_e(cat), phan_f(b, cat, truoc)]
    return "\n\n".join(phan) + "\n", cat, dung


def in_kiem(du, tat_ca, b, cat, dung, noi_dung):
    print(f"\n══ {b.ten}  live {vn(b.bat_dau)} → {vn(b.ket_thuc, '%H:%M')} VN ({b.nguon_gio}{'' if b.chac else ', GIỜ KHÔNG CHẮC'})"
          f"  →  C = {vn(cat.C)} VN · T(H4) = {vn(cat.T)} VN")
    for ten, t, co in cat.dau:
        print(f"   {'✓' if co <= cat.C else '✗ RÒ RỈ'} {ten:46} sự kiện {vn(t)} · biết lúc {vn(co)} VN")
    print(f"   nến H4 cuối mở {vn(cat.h4[-1].mo)} · D1 cuối mở {cat.d1[-1].mo:%Y-%m-%d} · "
          f"W1 cuối mở {cat.w1[-1].mo:%Y-%m-%d} · tháng cuối {cat.mn[-1].mo:%Y-%m}")
    for x in dung:
        print(f"   {'✓' if x.ket_thuc <= b.bat_dau else '✗ RÒ RỈ'} phiếu/mốc {x.ten:30} live {vn(x.bat_dau)} → hết "
              f"{vn(x.ket_thuc, '%H:%M')} VN{'' if x.chac else ' (giờ không chắc)'}")
    ngay_C = cat.C.astimezone(VN).strftime("%Y-%m-%d")
    than = "\n".join(l for l in noi_dung.splitlines() if not l.startswith(("# Hồ sơ buổi thi", "- Giờ live:")))
    sau = sorted({d for d in re.findall(r"\b(20\d\d-\d\d-\d\d)\b", than) if d > ngay_C})
    print(f"   ngày ISO > ngày C ({ngay_C}) trong hồ sơ (trừ tiêu đề + dòng giờ live): {sau or 'không có'}")
    print(f"   video ID buổi thi trong phần f: {'CÓ ✗' if b.vid in noi_dung.split('## f.')[1] else 'không ✓'}")
    # phép thử cắt tương lai: xoá mọi dữ liệu thị trường sau C và mọi buổi chưa kết thúc trước giờ live → hồ sơ phải y hệt
    du2 = du.cat_tuong_lai(cat.C)
    tat2 = [x for x in tat_ca if x.ket_thuc <= b.bat_dau] + [b]
    nd2 = lap_ho_so(du2, tat2, b)[0]
    print(f"   phép thử cắt tương lai (xoá dữ liệu sau C + phiếu chưa xong): {'GIỐNG HỆT ✓' if nd2 == noi_dung else 'KHÁC ✗ RÒ RỈ'}")
    return nd2 == noi_dung


def main():
    a = sys.argv[1:]
    tai_lai, kiem = "--tai-lai" in a, "--kiem" in a
    chi = a[a.index("--chi") + 1:] if "--chi" in a else []
    chi = [x for x in chi if not x.startswith("--")]
    du = DuLieu(tai_lai)
    for ten, nens, dd in (("H4", du.h4, GIO4), ("D1", du.d1, NGAY)):
        lh = lo_hong([n for n in nens if n.mo.year >= 2025], dd)
        if lh:
            print(f"! {ten} có {len(lh)} lỗ hổng từ 2025: {lh[:3]}", file=sys.stderr)
    tat_ca = ds_buoi()
    thi = [b for b in buoi_thi(tat_ca) if not chi or any(c in b.ten for c in chi)]
    print(f"Buổi thi: {len(buoi_thi(tat_ca))} · có giờ live thật: {sum(x.chac for x in buoi_thi(tat_ca))} "
          f"· giờ không chắc: {sum(not x.chac for x in buoi_thi(tat_ca))}", file=sys.stderr)
    HS.mkdir(parents=True, exist_ok=True)
    co = []
    for b in thi:
        nd, cat, dung = lap_ho_so(du, tat_ca, b)
        p = HS / f"{b.ten}.md"
        p.write_text(nd, encoding="utf-8")
        co.append(len(nd.encode()))
        if kiem and not in_kiem(du, tat_ca, b, cat, dung, nd):
            sys.exit("✗ phép thử cắt tương lai thất bại")
    if co:
        print(f"✓ {len(co)} hồ sơ → {HS.relative_to(GOC)}/ · trung bình {sum(co) / len(co) / 1024:.1f} KB "
              f"(min {min(co) / 1024:.1f}, max {max(co) / 1024:.1f})")


if __name__ == "__main__":
    main()
