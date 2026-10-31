#!/usr/bin/env python3
"""Nhan dinh bot v4 tren nen MOI NHAT (TK 10) -> in ra + ghi nhan_dinh_bot/v4_<YYYY-MM-DD_HHMM>.json (gio VN luc chay).

- Du lieu: nen BTC/ETH 4H + 1D (1Dutc) moi nhat tu OKX spot <X>-USDT, CHI nen da dong (confirm == "1"), ghi vao THU MUC TAM
  (khong bao gio ghi de bot_v4/du_lieu/). Lich su cu chep tu bot_v4/du_lieu/ roi noi phan moi tai tu OKX (nen trung gio:
  lay ban OKX moi tai); --tai-het: tai lai toan bo tu 2022-06-01 (giong tai_du_lieu.py).
- Luat: CHI goi ham dong co (dong_co.view_tai + dong_co.chay voi cat_tai = gio_cat), khong viet lai luat o day.
- Hai moc gio tach rieng (Codex P1-11): `gio_cat` = gio DONG cua nen H4 cuoi cung dong co duoc dung;
  `gio_phat_hanh` = luc chay script. Lenh dat tai gio_cat co hieu luc 6 nen H4 (TK 5.3).
Cach dung:
  python3 bot_v4/nhan_dinh.py              # tai nen moi + nhan dinh + ghi JSON
  python3 bot_v4/nhan_dinh.py --khong-ghi  # chi in
  python3 bot_v4/nhan_dinh.py --tai-het    # tai lai toan bo lich su tu OKX
"""
import argparse, csv, datetime as dt, hashlib, json, shutil, sys, tempfile, time, urllib.request
from pathlib import Path

V4 = Path(__file__).resolve().parent
GOC = V4.parent
UTC = dt.timezone.utc
VN = dt.timezone(dt.timedelta(hours=7))
G4 = dt.timedelta(hours=4)
TAI_SAN = ["BTC", "ETH"]
COIN = {"BTC": "BTC-USDT", "ETH": "ETH-USDT"}
KHUNG = {"4H": "4H", "1D": "1Dutc"}
BUOC = {"4H": G4, "1D": dt.timedelta(days=1)}
TU = dt.datetime(2022, 6, 1, tzinfo=UTC)
OKX_MOI = "https://www.okx.com/api/v5/market/candles?instId={}&bar={}&limit=300"
OKX_CU = "https://www.okx.com/api/v5/market/history-candles?instId={}&bar={}&limit=100&after={}"


# ───────────────────────── tai nen ─────────────────────────
def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for lan in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            if str(d.get("code", "0")) != "0":
                raise RuntimeError(f"OKX code {d.get('code')}: {d.get('msg')}")
            return d["data"]
        except Exception as e:
            if lan == 4:
                raise
            print("  thử lại:", e, file=sys.stderr)
            time.sleep(2 + 2 * lan)


def _s(ms):
    return dt.datetime.fromtimestamp(int(ms) // 1000, UTC).strftime("%Y-%m-%d %H:%M")


def tai_okx(ts, khung, tu_ms):
    """Moi nen DA DONG (confirm=1) co gio mo >= tu_ms -> {ms: [ts_utc, o, h, l, c, vol]}."""
    inst, bar = COIN[ts], KHUNG[khung]
    ra = {}
    d = _get(OKX_MOI.format(inst, bar))
    after = None
    while d:
        for x in d:
            mo, o, h, l, c, v, xn = int(x[0]), x[1], x[2], x[3], x[4], x[5], x[-1]
            if xn == "1" and mo >= tu_ms:
                ra[mo] = [_s(mo), o, h, l, c, v]
        after = min(int(x[0]) for x in d)
        if after <= tu_ms:
            break
        time.sleep(0.12)
        d = _get(OKX_CU.format(inst, bar, after))
    return ra


def doc_csv(p):
    if not p.exists():
        return {}
    with p.open() as f:
        return {int(dt.datetime.strptime(r["ts_utc"], "%Y-%m-%d %H:%M").replace(tzinfo=UTC).timestamp() * 1000):
                [r["ts_utc"], r["open"], r["high"], r["low"], r["close"], r["vol"]] for r in csv.DictReader(f)}


def chuan_bi_du_lieu(thu_muc, tai_het):
    """Ghi <TS>_{4H,1D}.csv vao thu_muc tam. Tra {ten tep: (so nen, nen dau, nen cuoi, so nen moi tu OKX)}."""
    tt = {}
    for ts in TAI_SAN:
        for khung in ("4H", "1D"):
            ten = f"{ts}_{khung}.csv"
            cu = {} if tai_het else doc_csv(V4 / "du_lieu" / ten)
            tu_ms = int(TU.timestamp() * 1000) if not cu else max(cu) - 10 * int(BUOC[khung].total_seconds() * 1000)
            print(f"  tải {ten} từ {_s(tu_ms)} UTC …", file=sys.stderr)
            moi = tai_okx(ts, khung, tu_ms)
            gop = {**cu, **moi}
            with (thu_muc / ten).open("w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["ts_utc", "open", "high", "low", "close", "vol"])
                for k in sorted(gop):
                    w.writerow(gop[k])
            tt[ten] = (len(gop), gop[min(gop)][0], gop[max(gop)][0], len(set(moi) - set(cu)))
    return tt


# ───────────────────────── goi dong co ─────────────────────────
def tg(x):
    if x is None or x == "":
        return None
    if isinstance(x, dt.datetime):
        return x if x.tzinfo else x.replace(tzinfo=UTC)
    if isinstance(x, (int, float)):
        return dt.datetime.fromtimestamp(x, UTC)
    s = str(x).strip().replace("T", " ")
    for f in ("%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            d = dt.datetime.strptime(s, f)
            return d if d.tzinfo else d.replace(tzinfo=UTC)
        except ValueError:
            pass
    return None


def json_hoa(x):
    if isinstance(x, dt.datetime):
        return x.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC")
    if isinstance(x, dict):
        return {str(k): json_hoa(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [json_hoa(v) for v in x]
    if hasattr(x, "_asdict"):
        return json_hoa(x._asdict())
    if isinstance(x, float):
        return round(x, 8)
    return x


def gio_dong_cuoi(thu_muc, ts):
    with (thu_muc / f"{ts}_4H.csv").open() as f:
        cuoi = list(csv.DictReader(f))[-1]
    return tg(cuoi["ts_utc"]) + G4, float(cuoi["close"])


def phan_tich_vung(s):
    """'lo-hi diem=n [loai:gia; ...]' (dong_co.mo_ta_cum) -> dict; chuoi rong -> None."""
    if not s:
        return None
    try:
        dau, _, can_cu = s.partition(" [")
        khoang, diem = dau.split(" diem=")
        lo, hi = khoang.split("-", 1) if not khoang.startswith("-") else (khoang, "")
        return {"khoang": [float(lo), float(hi)], "diem": int(diem),
                "can_cu": [x.strip() for x in can_cu.rstrip("]").split(";") if x.strip()], "mo_ta": s}
    except ValueError:
        return {"mo_ta": s}


def nhan_dinh(dc, thu_muc):
    """Goi dong co tren du lieu moi: view_tai + chay(cat_tai = gio_cat). Ky chay cua dong co ket thuc o
    THAM_SO['het_du_lieu_utc'] (2026-10-30, TK 1 cho backtest) -> nang moc nay TRONG BO NHO de dong co xet toi gio_cat
    (khong doi luat, khong sua tep). Lenh cho/dang mo = lenh con hieu luc tai gio_cat (dong co dong o HET_KY / huy 'het_ky')."""
    dc.THAM_SO["het_du_lieu_utc"] = "2100-01-01 00:00"
    du = {ts: dc.nap_du_lieu(ts, thu_muc) for ts in TAI_SAN}
    cuoi = {ts: gio_dong_cuoi(thu_muc, ts) for ts in TAI_SAN}
    gio_cat = min(t for t, _ in cuoi.values())  # cung 1 moc cho ca ro (BTC/ETH giao dich 24/7)
    gc = int(gio_cat.timestamp())  # epoch, cung don vi voi kq.quyet_dinh["ts"]
    kq = dc.chay(TAI_SAN, gio_cat.year, du_lieu=du, cat_tai=gio_cat)
    ra = []
    for ts in TAI_SAN:
        v = dc.view_tai(ts, gio_cat, du[ts])
        qd = next((q for q in reversed(kq.quyet_dinh) if q["tai_san"] == ts and q["ts"] == gc), None)
        lenh = []
        for x in kq.lenh:
            if x["tai_san"] != ts:
                continue
            # DG 26 cua dong co: du lieu cat truoc het ky -> lenh chua xong = DANG_CHO (chua khop) / DANG_MO (da khop)
            if x["ly_do_ra"] == "DANG_MO":
                trang = "DANG_MO"
            elif x["ly_do_ra"] == "DANG_CHO":
                trang = "CHO_KHOP"
            else:
                continue
            lenh.append({"trang_thai": trang, "loai": x["loai"], "chieu": x["chieu"], "t_quyet_dinh": tg(x["t_quyet_dinh"]),
                         "hieu_luc_den": tg(x["t_quyet_dinh"]) + 6 * G4 if trang == "CHO_KHOP" else None,
                         "vao": x["gia_dat"], "gia_khop": x["gia_vao"], "t_khop": tg(x["t_khop"]), "sl": x["sl"],
                         "sl_hien_tai": x["gia_vao"] if x.get("t_tp1") is not None else x["sl"],
                         "tp1": x["tp1"], "tp2": x["tp2"], "t_tp1": tg(x.get("t_tp1")), "gio_dung": x.get("gio_dung"),
                         "khoi_luong_von_4000": x["khoi_luong"], "don_bay": x["don_bay"], "vung": phan_tich_vung(x.get("vung")),
                         "ghi": x.get("ghi")})
        ra.append({"tai_san": ts, "gia_dong_h4_cuoi": cuoi[ts][1], "gio_cat": gio_cat, "pha": v.get("pha"), "view": v.get("view"),
                   "kieu": v.get("kieu"), "ly_do": v.get("ly_do"), "gio_cat_view": v.get("gio_cat"),
                   "hanh_dong_luc_cat": qd.get("hanh_dong") if qd else None,
                   "ly_do_bo_luc_cat": (qd.get("ly_do_bo") or None) if qd else None,
                   "vung_on": phan_tich_vung(qd.get("vung")) if qd and qd.get("vung") else (lenh[0]["vung"] if lenh else None),
                   "lenh": lenh})
    return gio_cat, ra


def main():
    a = argparse.ArgumentParser(description="Nhận định bot v4 trên nến OKX mới nhất")
    a.add_argument("--khong-ghi", action="store_true")
    a.add_argument("--tai-het", action="store_true")
    a = a.parse_args()
    gio_phat_hanh = dt.datetime.now(UTC)
    sys.path.insert(0, str(V4))
    import dong_co as dc  # noqa: E402
    tam = Path(tempfile.mkdtemp(prefix="v4_nhan_dinh_"))
    try:
        tt = chuan_bi_du_lieu(tam, a.tai_het)
        gio_cat, ds = nhan_dinh(dc, tam)
    finally:
        shutil.rmtree(tam, ignore_errors=True)
    ket = {"phien_ban": "bot v4", "gio_phat_hanh": gio_phat_hanh, "gio_phat_hanh_vn": gio_phat_hanh.astimezone(VN).strftime("%Y-%m-%d %H:%M VN"),
           "gio_cat": gio_cat, "gio_cat_vn": gio_cat.astimezone(VN).strftime("%Y-%m-%d %H:%M VN"),
           "ghi_chu_gio": "gio_cat = giờ ĐÓNG nến H4 cuối cùng động cơ dùng (nến đã đóng); gio_phat_hanh = lúc chạy script",
           "du_lieu": {"nguon": "OKX spot <X>-USDT, chỉ nến confirm=1 (4H, 1Dutc); lịch sử cũ chép từ bot_v4/du_lieu/" if not a.tai_het
                       else "OKX spot <X>-USDT, tải lại toàn bộ từ 2022-06-01, chỉ nến confirm=1",
                       "tep": {k: {"so_nen": v[0], "nen_dau": v[1], "nen_cuoi_mo_luc": v[2], "nen_moi_tu_okx": v[3]} for k, v in tt.items()}},
           "sha256": {t: hashlib.sha256((V4 / t).read_bytes()).hexdigest() for t in ("THIET_KE.md", "dong_co.py") if (V4 / t).exists()},
           "ghi_chu_dong_co": "gọi dong_co.chay(['BTC','ETH'], năm của gio_cat, cat_tai=gio_cat) + dong_co.view_tai; vốn mô phỏng 4.000$ từ "
                              "01/01 năm đó; THAM_SO['het_du_lieu_utc'] nâng trong bộ nhớ để kỳ chạy tới gio_cat (không đổi luật). "
                              "Lệnh CHO_KHOP hiệu lực 6 nến H4 từ t_quyet_dinh, huỷ sớm nếu view đổi (TK 5.3).",
           "tai_san": ds}
    ket = json_hoa(ket)
    print(f"Bot v4 · phát hành {ket['gio_phat_hanh_vn']} · dùng nến H4 đóng lúc {ket['gio_cat_vn']}")
    for x in ket["tai_san"]:
        print(f"- {x['tai_san']}: giá {x['gia_dong_h4_cuoi']:,.2f} · pha {x['pha']} · view {x['view']} ({x['kieu']}) · {x['ly_do']}")
        print(f"    lúc cắt: {x['hanh_dong_luc_cat']}" + (f" ({x['ly_do_bo_luc_cat']})" if x["ly_do_bo_luc_cat"] else ""))
        if x["vung_on"]:
            print(f"    vùng ổn: {x['vung_on'].get('mo_ta')}")
        for l in x["lenh"]:
            print(f"    lệnh {l['trang_thai']} {l['loai']} {l['chieu']}: vào {l['vao']:,.2f} · SL {l['sl']:,.2f} (hiện {l['sl_hien_tai']:,.2f}) · "
                  f"TP1 {l['tp1'] if l['tp1'] is None else format(l['tp1'], ',.2f')} · TP2 {l['tp2']:,.2f}"
                  + (f" · chờ khớp tới {l['hieu_luc_den']}" if l["hieu_luc_den"] else f" · khớp {l['t_khop']} giá {l['gia_khop']:,.2f}"))
        if not x["lenh"]:
            print("    không có lệnh chờ/đang mở")
    if not a.khong_ghi:
        p = GOC / "nhan_dinh_bot" / f"v4_{dt.datetime.fromisoformat(gio_phat_hanh.isoformat()).astimezone(VN):%Y-%m-%d_%H%M}.json"
        p.parent.mkdir(exist_ok=True)
        p.write_text(json.dumps(ket, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"✓ {p.relative_to(GOC)}")


if __name__ == "__main__":
    main()
