#!/usr/bin/env python3
"""Hieu chinh bien the trendline bang trendline nguoi do that su ve/nhac (hoc_v5/nhan/*.json truong `trendline`
+ hoc_v5/trendline/tham_chieu_anh.tsv doc tu anh chart). Luat so khop + luat chon: BIEN_THE.md (khai bao truoc).

Ra:  hoc_v5/trendline/khop_bien_the.tsv   (bang khop theo bien the: toan bo / truoc 07-01 / tu 07-01)
     hoc_v5/trendline/khop_chi_tiet.tsv   (tung lan nhac × bien the da chon)
     hoc_v5/trendline/volume_pha.tsv      (lan nhac pha/giu ↔ ti le volume nen pha)
     hoc_v5/trendline/CAN_ANH.tsv         (lan nhac trendline khong co anh + neo mo ho)
     in ra man hinh tom tat; CHON.md ghi tay tu ket qua nay (xem --ghi-chon).
Dung: python3 hoc_v5/trendline/hieu_chinh.py [--ghi-chon]
"""
import csv, datetime as dt, glob, json, re, sys
from collections import defaultdict
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "cong_cu"))
import trendline as T  # noqa: E402

RA = GOC / "hoc_v5" / "trendline"
VOL_LOI = []
NEN_VOL = []   # moi loi nguoi do noi ve nen + volume (truong nen_volume cap buoi), dien khi doc nhan
MOC_THI = "2026-07-01"
LECH = 0.005
KHUNG_SO = ("H4", "D1")
LOAI_SO = ("khang_cu_giam", "ho_tro_tang")

# anh xa nhan trang thai → trang thai may (BIEN_THE.md)
KHOP_TT = {
    "chua_pha": {"giu", "pha_gia"},
    "dang_giu": {"giu", "pha_gia"},
    "vua_pha": {"vua_pha_1n", "vua_pha_2n", "da_pha", "pha_roi_test_lai"},
    "pha_roi_test_lai": {"pha_roi_test_lai", "da_pha"},
    "da_pha": {"da_pha", "pha_roi_test_lai"},
    "pha_gia": {"pha_gia"},
}


def doc_gio_live():
    ra = {}
    with open(GOC / "transcripts" / "gio_live.tsv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            bd = dt.datetime.strptime(r["bat_dau_vn"], "%Y-%m-%d %H:%M")
            ra[r["id"]] = (bd, int(r["phut"]))
    return ra


def tim_id(ten, gl):
    """Video id tu ten buoi ('YYYY-MM-DD_id' hoac 'YYYY-MM-DD_HHMM_id'): id dai nhat trong gio_live ma ten ket thuc bang '_'+id."""
    ung = [v for v in gl if ten == v or ten.endswith("_" + v)]
    return max(ung, key=len) if ung else None


def giay_tu_gio(s):
    if not s:
        return None
    m = re.search(r"(\d+):(\d+):(\d+)", str(s))
    if not m:
        return None
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))


def t_utc(gl, vid, giay):
    bd, phut = gl[vid]
    if giay is None:
        giay = phut * 30  # giua buoi
    x = bd + dt.timedelta(seconds=giay) - dt.timedelta(hours=7)
    return int(x.replace(tzinfo=dt.timezone.utc).timestamp()), giay


def anh_co_san():
    ra = defaultdict(list)
    for p in (GOC / "so_tay" / "khung").glob("*.jpg"):
        m = re.match(r"(.+)_(\d{2})(\d{2})(\d{2})$", p.stem)
        if m:
            ra[m.group(1)].append(int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4)))
    return ra


def gia_tu_neo(neo, t):
    """Noi suy tuyen tinh tu >= 2 diem neo co ngay + gia (ngay = 00:00 UTC cua ngay do)."""
    ds = []
    for n in neo or []:
        if n and n.get("ngay") and n.get("gia"):
            try:
                x = T.ts_tu_chuoi(str(n["ngay"])[:10] + " 00:00")
            except ValueError:
                continue
            ds.append((x, float(n["gia"])))
    if len(ds) < 2:
        return None
    (x1, p1), (x2, p2) = ds[0], ds[-1]
    if x2 == x1:
        return None
    return p1 + (p2 - p1) / (x2 - x1) * (t - x1)


def doc_lan_nhac(gl):
    """Moi lan nguoi do nhac trendline BTC: tu nhan (moi buoi) + tu anh. Tra list dict."""
    ra = []
    for f in sorted(glob.glob(str(GOC / "hoc_v5" / "nhan" / "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        buoi = d.get("buoi") or Path(f).stem
        vid = tim_id(buoi, gl) or tim_id(Path(f).stem, gl)
        if vid is None:
            continue
        nv = []
        for e in d.get("nen_volume") or []:
            if isinstance(e, dict) and e.get("volume"):
                gy = giay_tu_gio(e.get("gio"))
                tt_, _ = t_utc(gl, vid, gy)
                NEN_VOL.append({"buoi": buoi, "vid": vid, "khung": e.get("khung"), "giay": gy, "t": tt_,
                                "volume": e["volume"], "nen": e.get("nen") or "", "ket_luan": e.get("ket_luan") or ""})
                if gy is not None:
                    nv.append((gy, e["volume"]))
        for i, tl in enumerate(d.get("trendline") or []):
            giay = giay_tu_gio(tl.get("gio"))
            t, giay2 = t_utc(gl, vid, giay)
            gia = tl.get("gia_duong_luc_noi")
            nguon_gia = "nhan" if gia else None
            if not gia:
                gia = gia_tu_neo(tl.get("diem_neo"), t)
                nguon_gia = "neo" if gia else None
            gan_vol = [v for gy, v in nv if giay is not None and abs(gy - giay) <= 180]
            ra.append({"buoi": buoi, "vid": vid, "giay": giay2, "co_gio": giay is not None, "t": t,
                       "khung": tl.get("khung"), "loai": tl.get("loai"), "gia_ref": float(gia) if gia else None,
                       "nguon_gia": nguon_gia, "trang_thai": tl.get("trang_thai"), "nguon": "nhan",
                       "nen_volume": tl.get("nen_volume") or " / ".join(gan_vol) or None, "trich": tl.get("trich") or "",
                       "neo": tl.get("diem_neo"), "ket_luan": tl.get("ket_luan_huong"), "stt": i})
    p = RA / "tham_chieu_anh.tsv"
    if p.exists():
        with open(p, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if r["video"] not in gl:
                    continue
                t, giay2 = t_utc(gl, r["video"], int(r["giay"]))
                # trung voi 1 lan nhac trong nhan (cung buoi/khung/loai, cach <= 300 giay) → giu ban anh (gia doc
                # tu chart), bo ban nhan de khong dem 2 lan
                ra = [x for x in ra if not (x["nguon"] == "nhan" and x["vid"] == r["video"] and x["khung"] == r["khung"]
                                            and x["loai"] in (r["loai"], "kenh") and abs(x["giay"] - giay2) <= 300)]
                ra.append({"buoi": r["buoi"], "vid": r["video"], "giay": giay2, "co_gio": True, "t": t,
                           "khung": r["khung"], "loai": r["loai"], "gia_ref": float(r["gia_ref"]),
                           "nguon_gia": "anh", "trang_thai": r["trang_thai"], "nguon": "anh",
                           "nen_volume": None, "trich": r["ghi_chu"], "neo": None, "ket_luan": None, "stt": 0})
    return ra


def so_mot(du, ln, bt, cache):
    """So 1 lan nhac voi 1 bien the. Tra dict ket qua hoac None neu khong so duoc (khung/loai ngoai pham vi)."""
    if ln["khung"] not in KHUNG_SO:
        return None
    if ln["loai"] in LOAI_SO:
        loai_ds = [ln["loai"]]
    elif ln["loai"] == "kenh" and ln["gia_ref"]:
        loai_ds = list(LOAI_SO)
    else:
        return None
    best = None
    for loai in loai_ds:
        key = (bt["neo"], bt["k"], bt["tuoi"], ln["t"], ln["khung"], loai)
        if key not in cache:
            cache[key] = T.duong_hieu_luc(du, ln["t"], bt, ln["khung"], loai)
        ds = cache[key]
        chinh = T.chon_chinh(ds, bt)
        r = {"loai_so": loai, "n_duong": len(ds), "chinh": chinh, "khop_chinh": None, "khop_tap": None,
             "lech_chinh": None, "duong_tt": chinh}
        if ln["gia_ref"]:
            g = ln["gia_ref"]
            if chinh:
                r["lech_chinh"] = (chinh["gia_t"] - g) / g
                r["khop_chinh"] = abs(r["lech_chinh"]) <= LECH
            else:
                r["khop_chinh"] = False
            gan = [x for x in ds if abs(x["gia_t"] - g) / g <= LECH]
            r["khop_tap"] = bool(gan)
            if r["khop_chinh"]:
                r["duong_tt"] = chinh
            elif gan:
                r["duong_tt"] = min(gan, key=lambda x: abs(x["gia_t"] - g))
        tt = ln["trang_thai"]
        if tt in KHOP_TT and ln["loai"] in LOAI_SO:
            d_ = r["duong_tt"]
            r["khop_tt"] = d_ is not None and d_["trang_thai"] in KHOP_TT[tt]
            # "vua pha" chi khop khi lan pha that <= 48h (duong D1 nay duoc liet ke toi 14 ngay sau pha)
            if r["khop_tt"] and tt == "vua_pha" and d_.get("da_pha_ngay") is not None:
                r["khop_tt"] = d_["da_pha_ngay"] * 24 < T.VUA_PHA_GIO
        else:
            r["khop_tt"] = None
        if best is None or (r["khop_chinh"] and not best["khop_chinh"]) or \
                (r["lech_chinh"] is not None and best["lech_chinh"] is not None and not best["khop_chinh"]
                 and abs(r["lech_chinh"]) < abs(best["lech_chinh"])):
            best = r
    return best


def tong(ket):
    """ket: list dict ket qua so. Tra (n_gia, k_chinh, k_tap, n_tt, k_tt, tb_duong)."""
    co_gia = [r for r in ket if r["khop_chinh"] is not None]
    co_tt = [r for r in ket if r["khop_tt"] is not None]
    n_g, n_t = len(co_gia), len(co_tt)
    return {"n_gia": n_g, "k_chinh": sum(r["khop_chinh"] for r in co_gia), "k_tap": sum(r["khop_tap"] for r in co_gia),
            "n_tt": n_t, "k_tt": sum(r["khop_tt"] for r in co_tt),
            "tb_duong": (sum(r["n_duong"] for r in ket) / len(ket)) if ket else 0}


def ti(a, b):
    return a / b if b else 0.0


def khoa_chon(bang, ds_bt):
    """Luat chon (BIEN_THE.md): ti le khop gia chinh → ti le khop trang thai → ti le khop tap → thu tu luoi."""
    thu_tu = {b["ten"]: i for i, b in enumerate(ds_bt)}
    return min(bang, key=lambda ten: (-ti(bang[ten]["k_chinh"], bang[ten]["n_gia"]),
                                      -ti(bang[ten]["k_tt"], bang[ten]["n_tt"]),
                                      -ti(bang[ten]["k_tap"], bang[ten]["n_gia"]), thu_tu[ten]))


YEU = re.compile(r"(không|chưa|ko)\s+(có\s+)?(volume|vol|lực|thanh khoản)|(volume|vol)\s+(vẫn\s+|rất\s+|càng\s+|hơi\s+)?"
                 r"(yếu|giảm|thấp|nhỏ|ít)|yếu|thiếu lực|không ăn thua|ít lực|chưa đủ lực|không ổn")
MANH = re.compile(r"(volume|vol)\s+(rất\s+)?(to|lớn|khủng|tốt|mạnh|tăng|đột biến|mua tốt|bán to)|bật volume|đột biến|khủng|"
                  r"full|có volume|có lực|áp đảo|nhảy vào|lực (bán|mua) (rất |còn |vẫn |khá )?(mạnh|khỏe|tốt)|cột .* to")


def loi_volume(txt):
    """Phan loai loi nguoi do noi ve volume/luc cua nen: 'manh' | 'yeu' | '?' (noi nhung khong ro) | '' (khong noi)."""
    if not txt:
        return ""
    s_ = str(txt).lower()
    if YEU.search(s_):
        return "yeu"
    if MANH.search(s_):
        return "manh"
    return "?"


def nhom_vol(x):
    if x is None:
        return "?"
    return "<0.8" if x < 0.8 else ("0.8-1.2" if x < 1.2 else (">=1.2"))


def main():
    gl = doc_gio_live()
    du = T.BoDuLieu.doc()
    lan = doc_lan_nhac(gl)
    ds_bt = T.danh_sach_bien_the()
    cache = {}
    kq = {}   # ten → list (ln, r)
    for bt in ds_bt:
        kq[bt["ten"]] = []
        for ln in lan:
            r = so_mot(du, ln, bt, cache)
            if r is not None:
                kq[bt["ten"]].append((ln, r))
    so_duoc = kq[ds_bt[0]["ten"]]
    pham = {"toan_bo": lambda ln: True, "truoc_0701": lambda ln: ln["buoi"][:10] < MOC_THI,
            "tu_0701": lambda ln: ln["buoi"][:10] >= MOC_THI}
    bang = {p: {} for p in pham}
    for ten, ds in kq.items():
        for p, f in pham.items():
            bang[p][ten] = tong([r for ln, r in ds if f(ln)])
    chon_tb = khoa_chon(bang["toan_bo"], ds_bt)
    chon_truoc = khoa_chon(bang["truoc_0701"], ds_bt)

    with open(RA / "khop_bien_the.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["bien_the", "pham_vi", "n_co_gia", "khop_gia_chinh", "ti_le_chinh", "khop_gia_tap", "ti_le_tap",
                    "n_co_trang_thai", "khop_trang_thai", "ti_le_tt", "tb_so_duong"])
        for bt in ds_bt:
            for p in pham:
                b = bang[p][bt["ten"]]
                w.writerow([bt["ten"], p, b["n_gia"], b["k_chinh"], f"{ti(b['k_chinh'], b['n_gia']):.3f}", b["k_tap"],
                            f"{ti(b['k_tap'], b['n_gia']):.3f}", b["n_tt"], b["k_tt"],
                            f"{ti(b['k_tt'], b['n_tt']):.3f}", f"{b['tb_duong']:.1f}"])

    # chi tiet theo bien the chon
    with open(RA / "khop_chi_tiet.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["buoi", "nguon", "giay", "t_utc", "khung", "loai", "loai_so", "gia_ref", "nguon_gia", "trang_thai_nhan",
                    "n_duong", "chinh_neo1", "chinh_neo2", "chinh_gia", "lech_pct", "khop_gia_chinh", "khop_gia_tap",
                    "tt_may", "khop_tt", "vol_pha"])
        for ln, r in kq[chon_tb]:
            c, d = r["chinh"], r["duong_tt"]
            w.writerow([ln["buoi"], ln["nguon"], ln["giay"], T.chuoi_tu_ts(ln["t"]), ln["khung"], ln["loai"], r["loai_so"],
                        ln["gia_ref"] or "", ln["nguon_gia"] or "", ln["trang_thai"], r["n_duong"],
                        f"{c['neo1_ts']} {c['neo1_gia']:.0f}" if c else "", f"{c['neo2_ts']} {c['neo2_gia']:.0f}" if c else "",
                        f"{c['gia_t']:.0f}" if c else "", f"{r['lech_chinh'] * 100:+.2f}" if r["lech_chinh"] is not None else "",
                        r["khop_chinh"] if r["khop_chinh"] is not None else "", r["khop_tap"] if r["khop_tap"] is not None else "",
                        d["trang_thai"] if d else "", r["khop_tt"] if r["khop_tt"] is not None else "",
                        f"{d['pha']['vol']:.2f}" if d and d["pha"] and d["pha"]["vol"] else ""])

    # volume: lan nhac co trang thai pha/giu hoac co nen_volume — doi chieu voi lan pha gan nhat cua duong (bien the chon)
    vol_rows = []
    for ln, r in kq[chon_tb]:
        d = r["duong_tt"]
        if ln["trang_thai"] not in ("vua_pha", "pha_roi_test_lai", "da_pha", "pha_gia") and not ln["nen_volume"]:
            continue
        pha = d["pha"] if d else None
        goi = "pha_gia" if ln["trang_thai"] == "pha_gia" else ("pha_that" if ln["trang_thai"] in KHOP_TT else "")
        vol_rows.append([ln["buoi"], ln["nguon"], ln["khung"], ln["loai"], ln["trang_thai"], goi, loi_volume(ln["nen_volume"]),
                         (ln["nen_volume"] or "").replace("\t", " ")[:200], d["trang_thai"] if d else "",
                         f"{pha['vol']:.2f}" if pha and pha["vol"] else "", nhom_vol(pha["vol"]) if pha else "",
                         pha["ket_qua"] if pha else ""])
    with open(RA / "volume_pha.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["buoi", "nguon", "khung", "loai", "trang_thai_nhan", "nguoi_goi", "loi_volume", "nen_volume_nhan", "tt_may",
                    "vol_ti_le", "nhom_vol", "ket_qua_pha_may"])
        w.writerows(vol_rows)

    # loi volume (moi khung H4, moi buoi) × ti le volume may do cua 2 nen H4 da dong gan nhat (lay lon hon)
    h4 = du.nen["H4"]
    lv_rows = []
    for e in NEN_VOL:
        if e["khung"] != "H4" or e["giay"] is None:
            continue
        n = h4.so_nen_dong(e["t"])
        tl = [T._ti_le_vol(h4, j) for j in (n - 1, n - 2) if j >= 0]
        tl = [x for x in tl if x is not None]
        vmax = max(tl) if tl else None
        lv_rows.append([e["buoi"], e["giay"], T.chuoi_tu_ts(e["t"]), loi_volume(e["volume"]),
                        f"{vmax:.2f}" if vmax is not None else "", nhom_vol(vmax), e["volume"].replace("\t", " ")[:150],
                        e["nen"].replace("\t", " ")[:100]])
    with open(RA / "volume_loi_h4.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["buoi", "giay", "t_utc", "loi_volume", "vol_max_2nen", "nhom_vol", "volume_nhan", "nen_nhan"])
        w.writerows(lv_rows)
    VOL_LOI.extend(lv_rows)

    # CAN_ANH: lan nhac (moi khung) khong co gia, khong co anh trong ±90s, neo mo ho
    anh = anh_co_san()
    can = []
    for ln in lan:
        if ln["nguon"] != "nhan" or ln["gia_ref"]:
            continue
        neo_ro = sum(1 for n in (ln["neo"] or []) if n and n.get("ngay") and n.get("gia"))
        if neo_ro >= 2:
            continue
        if any(abs(g - ln["giay"]) <= 90 for g in anh.get(ln["vid"], [])):
            continue
        can.append([ln["vid"], ln["giay"], ln["buoi"], ln["khung"] or "", ln["loai"] or "", ln["trang_thai"] or "",
                    "gio_giua_buoi" if not ln["co_gio"] else "", ln["trich"][:160].replace("\t", " ").replace("\n", " ")])
    with open(RA / "CAN_ANH.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["video_id", "giay", "buoi", "khung", "loai", "trang_thai", "ghi_chu", "trich"])
        w.writerows(sorted(can))

    # in tom tat
    tho = []
    for p in glob.glob(str(GOC / "hoc_v5" / "nhan" / "*.json")):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        tho += [(d.get("buoi") or Path(p).stem, tl) for tl in (d.get("trendline") or [])]
    so_buoi = len(glob.glob(str(GOC / "hoc_v5" / "nhan" / "*.json")))
    h4d1 = sum(1 for _, tl in tho if tl.get("khung") in KHUNG_SO)
    co_gia = sum(1 for _, tl in tho if tl.get("gia_duong_luc_noi"))
    truoc = sum(1 for b, _ in tho if b[:10] < MOC_THI)
    print(f"buoi co nhan: {so_buoi} | trendline nguoi do nhac (nhan): {len(tho)} (truoc 07-01: {truoc}; H4/D1: {h4d1}; "
          f"co gia duong: {co_gia}) + {sum(1 for x in lan if x['nguon'] == 'anh')} doc tu anh | "
          f"so duoc (H4/D1, loai hop): {len(so_duoc)} | CAN_ANH: {len(can)}")
    print(f"CHON toan bo: {chon_tb} | CHON truoc 07-01: {chon_truoc}")
    for p in pham:
        top = sorted(bang[p], key=lambda ten: (-ti(bang[p][ten]["k_chinh"], bang[p][ten]["n_gia"]),
                                              -ti(bang[p][ten]["k_tt"], bang[p][ten]["n_tt"])))[:6]
        print(f"-- {p}")
        for ten in top + [x for x in (chon_tb, chon_truoc) if x not in top]:
            b = bang[p][ten]
            print(f"  {ten:28s} gia chinh {b['k_chinh']}/{b['n_gia']}  tap {b['k_tap']}/{b['n_gia']}  tt {b['k_tt']}/{b['n_tt']}"
                  f"  tb duong {b['tb_duong']:.1f}")
    b = bang["tu_0701"][chon_truoc]
    print(f"KIEM THEO THOI GIAN: chon tren truoc 07-01 = {chon_truoc} → tu 07-01: gia chinh {b['k_chinh']}/{b['n_gia']}, "
          f"tt {b['k_tt']}/{b['n_tt']}")
    return bang, chon_tb, chon_truoc, kq, lan, can, vol_rows


def md(ten):
    return ten.replace("|", "\\|")


def ghi_chon(bang, chon_tb, chon_truoc, kq, lan, can, vol_rows):
    ds_bt = T.danh_sach_bien_the()
    tho_n = None
    L = []
    L.append("# Biến thể trendline ĐÃ KHOÁ")
    L.append("")
    L.append(f"BIEN_THE_KHOA: `{chon_tb}`")
    L.append("")
    L.append(f"Sinh bởi `python3 hoc_v5/trendline/hieu_chinh.py --ghi-chon` lúc {dt.datetime.now():%Y-%m-%d %H:%M} (VN). "
             "Luật so khớp + luật chọn khai báo trước trong `BIEN_THE.md`; chọn THUẦN theo độ khớp với đường người đó "
             "vẽ/nhắc (không dùng volume, không tiêu chí riêng).")
    L.append("")
    n_nhan = sum(1 for x in lan if x["nguon"] == "nhan")
    n_anh = sum(1 for x in lan if x["nguon"] == "anh")
    so = kq[chon_tb]
    L.append("## Dữ liệu so")
    L.append(f"- Lần nhắc trendline (mọi khung) đọc được giờ: {n_nhan} từ nhãn `hoc_v5/nhan/` + {n_anh} đọc từ ảnh chart "
             f"(`tham_chieu_anh.tsv`). So được (khung H4/D1, loại kháng cự giảm / hỗ trợ tăng, hoặc kênh có giá): {len(so)}.")
    b = bang["toan_bo"][chon_tb]
    L.append(f"- Có giá đường để so giá: {b['n_gia']}; có trạng thái để so: {b['n_tt']}.")
    L.append(f"- Lần nhắc cần ảnh thêm (không ảnh, neo mơ hồ): {len(can)} → `CAN_ANH.tsv`.")
    L.append("")
    L.append("## Bảng khớp (toàn bộ 180 buổi), 10 biến thể đầu theo luật chọn")
    L.append("| # | Biến thể | Khớp giá đường chính ≤0,5% | Khớp giá (có trong tập) | Khớp trạng thái | TB số đường |")
    L.append("|---|---|---|---|---|---|")
    thu_tu = {x["ten"]: i for i, x in enumerate(ds_bt)}
    xep = sorted(bang["toan_bo"], key=lambda ten: (-ti(bang["toan_bo"][ten]["k_chinh"], bang["toan_bo"][ten]["n_gia"]),
                                                   -ti(bang["toan_bo"][ten]["k_tt"], bang["toan_bo"][ten]["n_tt"]),
                                                   -ti(bang["toan_bo"][ten]["k_tap"], bang["toan_bo"][ten]["n_gia"]),
                                                   thu_tu[ten]))
    for i, ten in enumerate(xep[:10]):
        x = bang["toan_bo"][ten]
        L.append(f"| {i + 1} | `{md(ten)}` | {x['k_chinh']}/{x['n_gia']} ({ti(x['k_chinh'], x['n_gia']):.0%}) | "
                 f"{x['k_tap']}/{x['n_gia']} ({ti(x['k_tap'], x['n_gia']):.0%}) | {x['k_tt']}/{x['n_tt']} "
                 f"({ti(x['k_tt'], x['n_tt']):.0%}) | {x['tb_duong']:.1f} |")
    x = bang["toan_bo"][xep[-1]]
    L.append(f"| … | kém nhất `{md(xep[-1])}` | {x['k_chinh']}/{x['n_gia']} | {x['k_tap']}/{x['n_gia']} | {x['k_tt']}/{x['n_tt']} | {x['tb_duong']:.1f} |")
    L.append("")
    L.append("Bảng đủ 32 biến thể × 3 phạm vi: `khop_bien_the.tsv`; chi tiết từng lần nhắc với biến thể khoá: `khop_chi_tiet.tsv`.")
    L.append("")
    L.append("## Kiểm theo thời gian (chọn trên buổi trước 07-01 → đo trên buổi từ 07-01)")
    L.append("| Biến thể | Chọn trên | Trước 07-01: giá chính / trạng thái | Từ 07-01: giá chính / trạng thái |")
    L.append("|---|---|---|---|")
    for ten, nhan in ((chon_truoc, "trước 07-01"), (chon_tb, "toàn bộ (KHOÁ)")):
        a, c = bang["truoc_0701"][ten], bang["tu_0701"][ten]
        L.append(f"| `{md(ten)}` | {nhan} | {a['k_chinh']}/{a['n_gia']} ({ti(a['k_chinh'], a['n_gia']):.0%}) / "
                 f"{a['k_tt']}/{a['n_tt']} ({ti(a['k_tt'], a['n_tt']):.0%}) | {c['k_chinh']}/{c['n_gia']} "
                 f"({ti(c['k_chinh'], c['n_gia']):.0%}) / {c['k_tt']}/{c['n_tt']} ({ti(c['k_tt'], c['n_tt']):.0%}) |")
    tot = max(ti(bang["tu_0701"][t_]["k_chinh"], bang["tu_0701"][t_]["n_gia"]) for t_ in bang["tu_0701"])
    L.append(f"| (tham khảo) tốt nhất nếu chọn thẳng trên từ 07-01 | — | — | {tot:.0%} giá chính |")
    L.append("")
    L.append("## Volume khi phá (chỉ ghi, không dùng để chọn)")
    from collections import Counter
    cnt = Counter((r[5], r[10]) for r in vol_rows if r[5])
    L.append("| Người đó gọi | vol nến phá < 0,8 TB20 | 0,8–1,2 | ≥ 1,2 | máy không thấy lần phá |")
    L.append("|---|---|---|---|---|")
    for goi in ("pha_that", "pha_gia"):
        L.append(f"| {goi} | {cnt[(goi, '<0.8')]} | {cnt[(goi, '0.8-1.2')]} | {cnt[(goi, '>=1.2')]} | {cnt[(goi, '')]} |")
    lv = Counter((r[6], r[10]) for r in vol_rows if r[6])
    if lv:
        L.append("")
        L.append("Lời người đó nói về volume (trường `nen_volume`) × tỉ lệ volume máy đo:")
        L.append("| Lời | < 0,8 | 0,8–1,2 | ≥ 1,2 | không thấy phá |")
        L.append("|---|---|---|---|---|")
        for loi in ("manh", "yeu", "?"):
            L.append(f"| {loi} | {lv[(loi, '<0.8')]} | {lv[(loi, '0.8-1.2')]} | {lv[(loi, '>=1.2')]} | {lv[(loi, '')]} |")
    lh = Counter((r[3], r[5]) for r in VOL_LOI)
    L.append("")
    L.append("Mọi lời người đó tả volume nến H4 (trường `nen_volume` cấp buổi, khung H4) × tỉ lệ volume máy đo "
             "(lớn hơn của 2 nến H4 đã đóng gần nhất / TB20):")
    L.append("| Lời | < 0,8 | 0,8–1,2 | ≥ 1,2 |")
    L.append("|---|---|---|---|")
    for loi in ("manh", "yeu", "?"):
        L.append(f"| {loi} | {lh[(loi, '<0.8')]} | {lh[(loi, '0.8-1.2')]} | {lh[(loi, '>=1.2')]} |")
    L.append("")
    L.append("Chi tiết: `volume_pha.tsv`, `volume_loi_h4.tsv`.")
    return L


if __name__ == "__main__":
    kq_ = main()
    if "--ghi-chon" in sys.argv:
        L = ghi_chon(*kq_)
        p = RA / "CHON.md"
        cu = p.read_text(encoding="utf-8") if p.exists() else ""
        them = cu.split("<!-- GHI TAY -->", 1)[1] if "<!-- GHI TAY -->" in cu else "\n"
        p.write_text("\n".join(L) + "\n\n<!-- GHI TAY -->" + them, encoding="utf-8")
        print("da ghi", p)
