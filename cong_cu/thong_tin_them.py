#!/usr/bin/env python3
"""Thông tin ngoài nến: phái sinh BTC (funding, OI, long/short, taker, thanh lý, tường lệnh),
ETH, và vĩ mô (vàng, DXY, S&P500, Nasdaq, dầu). Toàn API công khai, không cần khoá.

Lưu du_lieu/anh/<YYYY-MM-DD_HHMM VN>_them.json và in tóm tắt. Nguồn nào lỗi thì ghi lỗi, không dừng.
Cách dùng: python3 cong_cu/thong_tin_them.py
"""
import datetime as dt, json, urllib.request
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
VN = dt.timezone(dt.timedelta(hours=7))
OKX = "https://www.okx.com/api/v5"


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=20) as r:
        return json.load(r)


def gio(ms):
    return dt.datetime.fromtimestamp(int(ms) / 1000, VN).strftime("%d/%m %H:%M")


def funding():
    now = get(f"{OKX}/public/funding-rate?instId=BTC-USDT-SWAP")["data"][0]
    lich_su = get(f"{OKX}/public/funding-rate-history?instId=BTC-USDT-SWAP&limit=9")["data"]
    return {"hien_tai_%": round(float(now["fundingRate"]) * 100, 4),
            "9_ky_gan_%": [round(float(x["realizedRate"]) * 100, 4) for x in lich_su]}


def oi():
    d = get(f"{OKX}/rubik/stat/contracts/open-interest-volume?ccy=BTC&period=1H")["data"][:25]  # mới → cũ
    return {"oi_usd_ty": round(float(d[0][1]) / 1e9, 2), "doi_24h_%": round((float(d[0][1]) / float(d[24][1]) - 1) * 100, 2),
            "doi_4h_%": round((float(d[0][1]) / float(d[4][1]) - 1) * 100, 2)}


def long_short():
    d = get(f"{OKX}/rubik/stat/contracts/long-short-account-ratio?ccy=BTC&period=1H")["data"][:25]
    return {"hien_tai": float(d[0][1]), "24h_truoc": float(d[24][1])}


def taker():
    d = get(f"{OKX}/rubik/stat/taker-volume?ccy=BTC&instType=CONTRACTS&period=1H")["data"]
    def ty_le(xs):
        ban, mua = sum(float(x[1]) for x in xs), sum(float(x[2]) for x in xs)
        return round(mua / ban, 3) if ban else None
    return {"mua/ban_4h": ty_le(d[:4]), "mua/ban_24h": ty_le(d[:24])}


def thanh_ly():
    d = get(f"{OKX}/public/liquidation-orders?instType=SWAP&uly=BTC-USDT&state=filled&limit=100")["data"]
    ct = [x for blk in d for x in blk.get("details", [])]
    # side=sell → vị thế LONG bị thanh lý; sz theo hợp đồng 0.01 BTC
    long_btc = sum(float(x["sz"]) * 0.01 for x in ct if x["side"] == "sell")
    short_btc = sum(float(x["sz"]) * 0.01 for x in ct if x["side"] == "buy")
    return {"so_lenh": len(ct), "tu": gio(min(x["ts"] for x in ct)) if ct else None,
            "long_bi_thanh_ly_btc": round(long_btc, 2), "short_bi_thanh_ly_btc": round(short_btc, 2)}


def tuong_lenh():
    b = get(f"{OKX}/market/books?instId=BTC-USDT-SWAP&sz=400")["data"][0]
    def gom(rows):  # gom theo bậc 250 USD, sz hợp đồng → BTC
        m = {}
        for px, sz, *_ in rows:
            k = int(float(px) // 250 * 250); m[k] = m.get(k, 0) + float(sz) * 0.01
        return sorted(m.items(), key=lambda x: -x[1])[:4]
    return {"gia_giua": round((float(b["bids"][0][0]) + float(b["asks"][0][0])) / 2),
            "tuong_mua(bậc, BTC)": [(k, round(v, 1)) for k, v in gom(b["bids"])],
            "tuong_ban(bậc, BTC)": [(k, round(v, 1)) for k, v in gom(b["asks"])]}


def eth():
    t = {i: get(f"{OKX}/market/ticker?instId={i}")["data"][0] for i in ("ETH-USDT", "ETH-BTC")}
    return {k: {"gia": float(v["last"]), "24h_%": round((float(v["last"]) / float(v["sodUtc0"]) - 1) * 100, 2)} for k, v in t.items()}


def vi_mo():
    ra = {}
    for ten, ma in {"vang": "GC=F", "DXY": "DX-Y.NYB", "SP500": "^GSPC", "Nasdaq": "^IXIC", "dau_WTI": "CL=F"}.items():
        try:
            m = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ma}?range=5d&interval=1d")["chart"]["result"][0]["meta"]
            ra[ten] = {"gia": round(m["regularMarketPrice"], 2),
                       "so_phien_truoc_%": round((m["regularMarketPrice"] / m["chartPreviousClose"] - 1) * 100, 2)}
        except Exception as e:
            ra[ten] = f"lỗi: {e}"
    return ra


def main():
    ra = {"luc_vn": dt.datetime.now(VN).strftime("%d/%m %H:%M")}
    for ten, f in [("funding", funding), ("open_interest", oi), ("long_short_tai_khoan", long_short),
                   ("taker", taker), ("thanh_ly_gan_day", thanh_ly), ("tuong_lenh_perp", tuong_lenh),
                   ("eth", eth), ("vi_mo", vi_mo)]:
        try:
            ra[ten] = f()
        except Exception as e:
            ra[ten] = f"lỗi: {e}"
    p = GOC / "du_lieu" / "anh" / f"{dt.datetime.now(VN).strftime('%Y-%m-%d_%H%M')}_them.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(ra, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(ra, ensure_ascii=False, indent=1))
    print("→", p.relative_to(GOC))


if __name__ == "__main__":
    main()
