#!/usr/bin/env python3
"""Chụp dữ liệu KHÔNG có API miễn phí bằng Chrome thật trên máy (Coinglass, TradingView BTC.D / USDT.D) → ảnh + chữ.

CHỈ DÙNG CHO HỎI LIVE: trang web chỉ cho số liệu lúc chụp, không xem lại được quá khứ. `/nhan-dinh` với T là nến vừa
đóng (lúc chụp − T ≤ 4 giờ) mới được đọc thư mục này; T quá khứ thì bỏ, ghi "không có dữ liệu <X>".

Chrome ≥ 136 không cho điều khiển hồ sơ mặc định → mở cửa sổ Chrome riêng với hồ sơ cố định HO_SO (giữ đăng nhập,
cookie qua các lần chạy; trang cần tài khoản thì đăng nhập một lần trong cửa sổ đó). Chụp bằng `cong_cu/chup_web.mjs`
(cổng 9333), mỗi trang ra <ten>.png + <ten>.txt (chữ trên trang) + meta.json (giờ chụp VN).

Cách dùng: python -X utf8 bot_v5/chup_ngoai.py [ten_trang ...] [--ra <thu_muc>]
  mặc định chụp mọi trang trong TRANG → bot_v5/_web/<YYYYMMDD_HHMM giờ chụp VN>/
"""
import argparse, datetime as dt, json, os, subprocess, sys, time, urllib.request
from pathlib import Path

DAY = Path(__file__).resolve().parent
GOC = DAY.parent
CONG = 9333
HO_SO = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "trade-dai-han" / "chrome"
CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
VN = dt.timezone(dt.timedelta(hours=7))

# ten: (url, rộng, cao, chờ ms) — những thứ người đó xem mà hồ sơ không có (NHAP_VAI §1.5, ST1 C9–C10)
TRANG = {
    "cg_heatmap": ("https://www.coinglass.com/pro/futures/LiquidationHeatMap", 1600, 1300, 25000),
    "cg_thanh_ly": ("https://www.coinglass.com/LiquidationData", 1600, 2200, 20000),
    "cg_long_short": ("https://www.coinglass.com/LongShortRatio", 1600, 2200, 20000),
    "cg_oi": ("https://www.coinglass.com/BitcoinOpenInterest", 1600, 2200, 20000),
    "cg_etf": ("https://www.coinglass.com/etf/bitcoin", 1600, 2600, 20000),
    "cg_so_du_san": ("https://www.coinglass.com/Balance", 1600, 2600, 20000),
    "tv_btc_d": ("https://www.tradingview.com/chart/?symbol=CRYPTOCAP%3ABTC.D&interval=240", 1600, 1000, 15000),
    "tv_usdt_d": ("https://www.tradingview.com/chart/?symbol=CRYPTOCAP%3AUSDT.D&interval=240", 1600, 1000, 15000),
}


def cdp_song():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{CONG}/json/version", timeout=2):
            return True
    except OSError:
        return False


def mo_chrome():
    if cdp_song():
        return
    exe = next((p for p in CHROME if Path(p).exists()), None)
    if not exe:
        sys.exit("■ Không thấy chrome.exe")
    HO_SO.mkdir(parents=True, exist_ok=True)
    subprocess.Popen([exe, f"--remote-debugging-port={CONG}", f"--user-data-dir={HO_SO}", "--no-first-run",
                      "--no-default-browser-check", "about:blank"])
    for _ in range(30):
        time.sleep(1)
        if cdp_song():
            return
    sys.exit(f"■ Chrome không mở cổng {CONG}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("trang", nargs="*", help=f"mặc định tất cả: {', '.join(TRANG)}")
    ap.add_argument("--ra", default=None)
    a = ap.parse_args()
    ds = a.trang or list(TRANG)
    sai = [x for x in ds if x not in TRANG]
    if sai:
        sys.exit(f"■ Không có trang: {sai}")
    mo_chrome()
    luc = dt.datetime.now(VN)
    ra = Path(a.ra) if a.ra else DAY / "_web" / luc.strftime("%Y%m%d_%H%M")
    ra.mkdir(parents=True, exist_ok=True)
    meta = {"chup_luc_vn": luc.strftime("%Y-%m-%d %H:%M"), "chi_dung_khi": "T là nến vừa đóng, chup_luc − T ≤ 4 giờ",
            "trang": {}}
    for ten in ds:
        url, rong, cao, cho = TRANG[ten]
        r = subprocess.run(["node", str(GOC / "cong_cu" / "chup_web.mjs"), url, str(ra / f"{ten}.png"),
                            str(rong), str(cao), str(cho)], capture_output=True, text=True, encoding="utf-8")
        ok = r.returncode == 0 and (ra / f"{ten}.png").exists()
        meta["trang"][ten] = {"url": url, "ok": ok, "luc_vn": dt.datetime.now(VN).strftime("%Y-%m-%d %H:%M")}
        print(("✓ " if ok else "✗ ") + ten, "" if ok else (r.stderr or r.stdout).strip()[-300:])
    (ra / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print("■", ra)


if __name__ == "__main__":
    main()
