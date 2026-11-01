#!/usr/bin/env python3
"""Kế hoạch có cấu trúc của bot v5 — bản máy kiểm / chấm được của câu trả lời tiếng Việt.

Mỗi lần nhận định, bot ghi câu trả lời vào `bot_v5/doi_chieu/<stem>.md` như cũ và thêm `bot_v5/ke_hoach/<stem>.json`
(cùng stem). File JSON chỉ chứa DỰ BÁO; kết quả chấm về sau nằm riêng ở `bot_v5/ket_qua/` (cham_ke_hoach.py).

  python3 bot_v5/ke_hoach.py kiem  <file.json>   → kiểm schema + nhất quán (có LỖI → exit 1)
  python3 bot_v5/ke_hoach.py luu   <file.json>   → kiểm + KHOÁ: git commit, sha256 luật/sổ tay/code, sha256 hồ sơ tại T
                                                   (dựng lại offline), chế độ hồi cứu/trực tiếp → ghi mục lục
                                                   `bot_v5/ke_hoach/SO_KE_HOACH.tsv` (sha256 file). Đã khoá → từ chối.
  python3 bot_v5/ke_hoach.py truoc <MÃ> "<T>"    → view bot ĐÃ PHÁT HÀNH trước T (gio_phat_hanh ≤ T, file khoá đúng sha)
                                                   + trạng thái tới T (chỉ dữ liệu giá ≤ T). Không có → "KHỞI TẠO VIEW".
Giờ trong JSON: giờ VN "YYYY-MM-DD HH:MM"; hạn ghi ngày "YYYY-MM-DD" = hết ngày đó (00:00 VN ngày sau).

Schema "ke_hoach_v5/1" (ví dụ đầy đủ: bot_v5/MAU_TRA_LOI.md phần B):
  ma, khung_hoi, gio_live, gio_cat, gio_phat_hanh, gia_dong, tep_doi_chieu, lenh_ho_so
  view_truoc  {loai: KHOI_TAO | TU_KE_HOACH, tep, ghi_chu}
  view        {H4|D1|W1: {huong: TANG|GIAM|PHAN_VAN, nhan, do_chac: thap|vua|cao, dich [a,b], han,
                          sai_khi {khung, phia: tren|duoi, gia, so_nen}, cho {tren, duoi} (PHAN_VAN)}}
  hanh_dong   VAO_NGAY | CHO_VUNG | CHO_XAC_NHAN | GIU | CHOT | DONG | KHONG_LENH
  duong_di    [{chang, vung [a,b], de, han}]
  ke_hoach    [{id, khung_view, hanh_dong, chieu: LONG|SHORT, luot, vao {vung [a,b]} | {gia},
                kich_hoat {khung, phia, gia, so_nen} (CHO_XAC_NHAN, nến đóng), xac_nhan {mo_ta, kiem_may},
                huy_truoc_khi_vao [{kieu: cham|dong, …}], het_han_cho, tp [{vung | gia, ty_le}], sl_cham {gia},
                dong_khi [{khung, phia, gia, so_nen}], han, can_cu [{ten, ho, khung}], ghi_chu_ghep}]
  lenh_user   {chieu, gia_vao, gio_vao} (khi user nói đang cầm lệnh) · thieu_du_lieu [..] · do_tin_chu_quan [..]
  khoa        null khi bot ghi; `luu` điền.
"""
import csv, datetime as dt, hashlib, json, subprocess, sys
from pathlib import Path

DAY = Path(__file__).resolve().parent
GOC = DAY.parent
KE_HOACH = DAY / "ke_hoach"
MUC_LUC = "SO_KE_HOACH.tsv"
COT_MUC_LUC = ["tep", "ma", "khung_hoi", "gio_cat", "gio_phat_hanh", "che_do", "sha256", "git", "gio_luu"]
SCHEMA = "ke_hoach_v5/1"
VN = dt.timezone(dt.timedelta(hours=7))

HUONG = {"TANG", "GIAM", "PHAN_VAN"}
DO_CHAC = {"thap", "vua", "cao"}
HANH_DONG = {"VAO_NGAY", "CHO_VUNG", "CHO_XAC_NHAN", "GIU", "CHOT", "DONG", "KHONG_LENH"}
CO_VAO = {"VAO_NGAY", "CHO_VUNG", "CHO_XAC_NHAN", "GIU"}  # kế hoạch có lệnh để chấm
KHUNG_VIEW = {"H4": "4H", "D1": "1D", "W1": "1W"}
KHUNG_DONG = {"1H", "4H", "1D", "1W"}
HO_CAN_CU = {"EMA", "FIBO", "DINH_DAY", "RAU", "TRENDLINE", "KHAC"}
VIEW_CU_NGAY = 7  # view bot phát hành trước T nhưng gio_cat cũ hơn số ngày này → coi như khởi tạo (ngưỡng chọn tay)
FILE_KHOA = ["bot_v5/NHAP_VAI.md", "bot_v5/MAU_TRA_LOI.md", ".claude/commands/nhan-dinh.md", "bot_v5/ngu_canh.py",
             "bot_v5/nen.py", "bot_v5/so_tay_den.py", "bot_v5/ke_hoach.py", "cong_cu/trendline.py", "cong_cu/chi_bao.py",
             "bot_v5/so_tay/1_huong_giu_lat_tin.md", "bot_v5/so_tay/2_trendline_nen_volume.md",
             "bot_v5/so_tay/3_do_ve_vung_vao_tranh.md"]


# ---------------- giờ ----------------
def doc_gio(s, cuoi_ngay=False):
    """Giờ VN → giây UTC. "YYYY-MM-DD" (chỉ ngày): cuoi_ngay → 00:00 VN ngày sau, không thì 00:00 VN ngày đó."""
    s = str(s).strip()
    if len(s) == 10:
        d = dt.datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=VN)
        if cuoi_ngay:
            d += dt.timedelta(days=1)
    else:
        d = dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M").replace(tzinfo=VN)
    return int(d.timestamp())


def gio_vn(t, ngan=False):
    d = dt.datetime.fromtimestamp(t, VN)
    return d.strftime("%d/%m %H:%M") if ngan else d.strftime("%Y-%m-%d %H:%M")


def bay_gio_vn():
    return dt.datetime.now(VN).strftime("%Y-%m-%d %H:%M")


# ---------------- mức giá ----------------
def vung(x):
    """{vung: [a, b]} | {gia: x} | [a, b] | số → (a, b) với a ≤ b; không hợp lệ → None."""
    if isinstance(x, dict):
        x = x.get("vung", x.get("gia"))
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return (float(x), float(x))
    if isinstance(x, (list, tuple)) and len(x) == 2 and all(isinstance(v, (int, float)) for v in x):
        a, b = float(x[0]), float(x[1])
        return (a, b) if a <= b else None
    return None


def muc_vao(p):
    """Mức chạm để coi là khớp lệnh chờ: LONG = mép trên vùng (giá đi xuống chạm), SHORT = mép dưới."""
    a, b = vung(p["vao"])
    return b if p["chieu"] == "LONG" else a


def muc_tp(p, i=0):
    """TP tính khi chạm MÉP GẦN: LONG = mép dưới vùng TP, SHORT = mép trên."""
    a, b = vung(p["tp"][i])
    return a if p["chieu"] == "LONG" else b


def phia_thuan(chieu):
    return "tren" if chieu == "LONG" else "duoi"


def phia_nguoc(chieu):
    return "duoi" if chieu == "LONG" else "tren"


def chieu_cua(huong):
    return {"TANG": "LONG", "GIAM": "SHORT"}.get(huong)


def _so(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _dk_dong(dk, ten, loi, khung_phai=None):
    if not isinstance(dk, dict):
        loi.append(f"{ten}: phải là object {{khung, phia, gia, so_nen}}")
        return False
    ok = True
    if dk.get("khung") not in KHUNG_DONG:
        loi.append(f"{ten}.khung = {dk.get('khung')!r}: phải là một trong {sorted(KHUNG_DONG)}")
        ok = False
    elif khung_phai and dk["khung"] != khung_phai:
        loi.append(f"{ten}.khung = {dk['khung']}: view khung này phải sai theo nến {khung_phai} ĐÓNG")
        ok = False
    if dk.get("phia") not in ("tren", "duoi"):
        loi.append(f"{ten}.phia phải là 'tren' hoặc 'duoi'")
        ok = False
    if not _so(dk.get("gia")):
        loi.append(f"{ten}.gia phải là số")
        ok = False
    n = dk.get("so_nen", 1)
    if not isinstance(n, int) or n < 1:
        loi.append(f"{ten}.so_nen phải là số nguyên ≥ 1")
        ok = False
    return ok


def _cung_dk(x, y):
    return (x.get("khung") == y.get("khung") and x.get("phia") == y.get("phia") and _so(x.get("gia"))
            and _so(y.get("gia")) and abs(x["gia"] - y["gia"]) <= 1e-3 * abs(y["gia"]))


def _giao(x, y):
    return x[0] <= y[1] and y[0] <= x[1]


# ---------------- kiểm ----------------
def kiem(kh):
    """→ (lỗi, cảnh báo, thông tin). Lỗi = không được lưu."""
    loi, cb, tt = [], [], []
    if kh.get("schema") != SCHEMA:
        loi.append(f"schema phải là {SCHEMA!r}")
    for k in ("ma", "khung_hoi", "gio_live", "gio_cat", "gio_phat_hanh", "gia_dong", "tep_doi_chieu", "view",
              "hanh_dong", "duong_di", "ke_hoach", "view_truoc"):
        if k not in kh:
            loi.append(f"thiếu trường {k}")
    if loi:
        return loi, cb, tt
    gio = {}
    for k in ("gio_live", "gio_cat", "gio_phat_hanh"):
        try:
            gio[k] = doc_gio(kh[k])
        except Exception:
            loi.append(f"{k} = {kh[k]!r}: không đọc được giờ VN 'YYYY-MM-DD HH:MM'")
    if len(gio) == 3 and gio["gio_phat_hanh"] < gio["gio_cat"]:
        loi.append("gio_phat_hanh < gio_cat (phát hành trước khi có dữ liệu)")
    T = gio.get("gio_cat")
    gd = kh["gia_dong"]
    if not _so(gd):
        loi.append("gia_dong phải là số")
        return loi, cb, tt
    vt = kh["view_truoc"]
    if not isinstance(vt, dict) or vt.get("loai") not in ("KHOI_TAO", "TU_KE_HOACH"):
        loi.append("view_truoc.loai phải là KHOI_TAO hoặc TU_KE_HOACH")
    elif vt["loai"] == "TU_KE_HOACH" and not vt.get("tep"):
        loi.append("view_truoc TU_KE_HOACH phải ghi tep (file kế hoạch trước, lấy từ `ke_hoach.py truoc`)")

    # ---- view 3 khung ----
    view = kh["view"]
    for kv, kd in KHUNG_VIEW.items():
        v = view.get(kv)
        if not isinstance(v, dict):
            loi.append(f"view.{kv}: thiếu")
            continue
        if v.get("huong") not in HUONG:
            loi.append(f"view.{kv}.huong phải là TANG / GIAM / PHAN_VAN")
            continue
        if v.get("do_chac") not in DO_CHAC:
            loi.append(f"view.{kv}.do_chac phải là thap / vua / cao")
        if v["huong"] == "PHAN_VAN":
            c = v.get("cho") or {}
            if not (_so(c.get("tren")) and _so(c.get("duoi")) and c["duoi"] < gd < c["tren"]):
                loi.append(f"view.{kv} PHAN_VAN: cần cho {{tren, duoi}} với duoi < gia_dong < tren")
            continue
        d = vung(v.get("dich"))
        if d is None:
            loi.append(f"view.{kv}.dich phải là [a, b] (a ≤ b) hoặc 1 số")
        elif v["huong"] == "TANG" and d[0] <= gd:
            loi.append(f"view.{kv} TANG nhưng mép dưới đích {d[0]} ≤ giá đóng {gd}")
        elif v["huong"] == "GIAM" and d[1] >= gd:
            loi.append(f"view.{kv} GIAM nhưng mép trên đích {d[1]} ≥ giá đóng {gd}")
        if _dk_dong(v.get("sai_khi"), f"view.{kv}.sai_khi", loi, kd):
            s = v["sai_khi"]
            phai = "duoi" if v["huong"] == "TANG" else "tren"
            if s["phia"] != phai:
                loi.append(f"view.{kv} {v['huong']}: sai_khi phải là nến đóng phía '{phai}'")
            elif (phai == "duoi" and s["gia"] >= gd) or (phai == "tren" and s["gia"] <= gd):
                loi.append(f"view.{kv}: mốc sai {s['gia']} nằm sai phía giá đóng {gd} (view đã sai ngay tại T?)")
        try:
            h = doc_gio(v.get("han"), cuoi_ngay=True)
            if T is not None and h <= T:
                loi.append(f"view.{kv}.han không sau gio_cat")
        except Exception:
            loi.append(f"view.{kv}.han: cần giờ/ngày VN")

    if kh["hanh_dong"] not in HANH_DONG:
        loi.append(f"hanh_dong phải là một trong {sorted(HANH_DONG)}")

    # ---- đường đi ----
    dd = kh["duong_di"]
    if not isinstance(dd, list):
        loi.append("duong_di phải là danh sách")
    else:
        for i, c in enumerate(dd, 1):
            if c.get("chang") != i:
                loi.append(f"duong_di[{i - 1}].chang phải là {i} (đúng thứ tự)")
            if vung(c.get("vung")) is None:
                loi.append(f"duong_di chặng {i}: vung phải là [a, b] hoặc 1 số")

    # ---- kế hoạch lệnh ----
    ids = set()
    for p in kh["ke_hoach"]:
        ten = f"ke_hoach[{p.get('id', '?')}]"
        if not p.get("id") or p["id"] in ids:
            loi.append(f"{ten}: id thiếu hoặc trùng")
        ids.add(p.get("id"))
        hd = p.get("hanh_dong")
        if hd not in HANH_DONG:
            loi.append(f"{ten}.hanh_dong không hợp lệ")
            continue
        if hd not in CO_VAO:
            continue
        if p.get("chieu") not in ("LONG", "SHORT"):
            loi.append(f"{ten}.chieu phải là LONG / SHORT")
            continue
        ch = p["chieu"]
        v_vao = vung(p.get("vao"))
        if hd == "CHO_XAC_NHAN":
            _dk_dong(p.get("kich_hoat"), f"{ten}.kich_hoat", loi)
            if v_vao is None and isinstance(p.get("kich_hoat"), dict) and _so(p["kich_hoat"].get("gia")):
                v_vao = (p["kich_hoat"]["gia"],) * 2
        if v_vao is None:
            loi.append(f"{ten}.vao phải là {{vung: [a, b]}} hoặc {{gia: x}}")
            continue
        if hd in ("VAO_NGAY", "GIU") and v_vao[0] != v_vao[1]:
            loi.append(f"{ten}: {hd} cần vao {{gia: x}} (1 giá)")
        if hd == "VAO_NGAY" and abs(v_vao[0] - gd) > 0.005 * gd:
            cb.append(f"{ten}: VAO_NGAY ở {v_vao[0]} lệch giá đóng {gd} > 0,5%")
        if hd == "GIU" and not isinstance(kh.get("lenh_user"), dict):
            loi.append(f"{ten}: GIU cần lenh_user {{chieu, gia_vao, gio_vao}} (lệnh user đang cầm)")
        tps = [vung(x) for x in p.get("tp") or []]
        if not tps or None in tps:
            loi.append(f"{ten}.tp: cần ≥ 1 TP dạng {{vung: [a, b]}} hoặc {{gia: x}}")
            continue
        thoat = [x for x in (p.get("dong_khi") or [])]
        sl = p.get("sl_cham")
        if not thoat and not sl:
            loi.append(f"{ten}: cần dong_khi (nến đóng) hoặc sl_cham (chạm giá) — lệnh phải có chỗ ra")
        for j, dk in enumerate(thoat):
            if _dk_dong(dk, f"{ten}.dong_khi[{j}]", loi) and dk["phia"] != phia_nguoc(ch):
                loi.append(f"{ten}.dong_khi[{j}]: lệnh {ch} đóng khi nến đóng phía '{phia_nguoc(ch)}'")
        if sl is not None and not (isinstance(sl, dict) and _so(sl.get("gia"))):
            loi.append(f"{ten}.sl_cham phải là {{gia: x}} hoặc null")
            sl = None
        # thứ tự giá: LONG: thoát < vào < TP; SHORT ngược lại
        ref = v_vao if hd != "GIU" else (gd, gd)
        tp_gan = [t[0] if ch == "LONG" else t[1] for t in tps]
        if ch == "LONG" and min(tp_gan) <= ref[1]:
            loi.append(f"{ten}: LONG nhưng TP {min(tp_gan)} không cao hơn vào {ref[1]}")
        if ch == "SHORT" and max(tp_gan) >= ref[0]:
            loi.append(f"{ten}: SHORT nhưng TP {max(tp_gan)} không thấp hơn vào {ref[0]}")
        muc_ra = [dk["gia"] for dk in thoat if isinstance(dk, dict) and _so(dk.get("gia"))]
        if sl:
            muc_ra.append(sl["gia"])
        for m in muc_ra:
            if (ch == "LONG" and m >= ref[0]) or (ch == "SHORT" and m <= ref[1]):
                loi.append(f"{ten}: mốc ra {m} nằm sai phía vùng vào {ref} của lệnh {ch}")
        for j, dk in enumerate(p.get("huy_truoc_khi_vao") or []):
            if not isinstance(dk, dict) or dk.get("kieu") not in ("cham", "dong"):
                loi.append(f"{ten}.huy_truoc_khi_vao[{j}]: kieu phải là 'cham' hoặc 'dong'")
            elif dk["kieu"] == "dong":
                _dk_dong(dk, f"{ten}.huy_truoc_khi_vao[{j}]", loi)
            elif dk.get("phia") not in ("tren", "duoi") or not _so(dk.get("gia")):
                loi.append(f"{ten}.huy_truoc_khi_vao[{j}]: cần phia + gia")
        for k in ("han", "het_han_cho"):
            if p.get(k) is not None:
                try:
                    doc_gio(p[k], cuoi_ngay=True)
                except Exception:
                    loi.append(f"{ten}.{k}: cần giờ/ngày VN")
        if not p.get("han"):
            loi.append(f"{ten}.han: cần hạn dự báo (để cột hạn riêng)")
        # thuộc đúng view nào; đích / mốc ra lấy từ view khác thì phải giải thích
        kvw = p.get("khung_view")
        v = view.get(kvw) if kvw in KHUNG_VIEW else None
        if v is None:
            loi.append(f"{ten}.khung_view phải là H4 / D1 / W1")
        elif v.get("huong") in ("TANG", "GIAM"):
            van_de = []
            if chieu_cua(v["huong"]) != ch and not p.get("luot"):
                loi.append(f"{ten}: {ch} ngược view {kvw} {v['huong']} — lệnh ngược view phải đánh dấu luot: true")
            d = vung(v.get("dich"))
            chang = [vung(c.get("vung")) for c in dd if vung(c.get("vung"))] if isinstance(dd, list) else []
            if d and not any(_giao(t, d) for t in tps) and not any(_giao(t, c) for t in tps for c in chang):
                van_de.append(f"TP không trùng đích view {kvw} {d} hay chặng nào của đường đi")
            if isinstance(v.get("sai_khi"), dict) and thoat and not any(_cung_dk(x, v["sai_khi"]) for x in thoat):
                van_de.append(f"dong_khi không chứa mốc sai view {kvw} ({v['sai_khi'].get('khung')} "
                              f"{v['sai_khi'].get('phia')} {v['sai_khi'].get('gia')})")
            if van_de and not str(p.get("ghi_chu_ghep") or "").strip():
                loi.append(f"{ten}: " + "; ".join(van_de) + " — ghép mức của kế hoạch khác thì ghi lý do ở ghi_chu_ghep")
            elif van_de:
                tt.append(f"{ten}: ghép mức có giải thích — {p['ghi_chu_ghep']}")
        if hd == "CHO_VUNG" and not (p.get("xac_nhan") or {}).get("kiem_may"):
            tt.append(f"{ten}: điều kiện vào khung nhỏ không kiểm bằng máy → bộ chấm chỉ báo 'giá chạm vùng'")
        cc = p.get("can_cu") or []
        ho = [c.get("ho") for c in cc if isinstance(c, dict)]
        sai_ho = [h for h in ho if h not in HO_CAN_CU]
        if sai_ho:
            loi.append(f"{ten}.can_cu.ho không hợp lệ: {sai_ho} (dùng {sorted(HO_CAN_CU)})")
        if any(not (isinstance(c, dict) and c.get("ten") and c.get("khung")) for c in cc):
            loi.append(f"{ten}.can_cu: mỗi căn cứ cần ten + ho + khung")
        nhom = sorted(set(h for h in ho if h in HO_CAN_CU))
        tt.append(f"{ten}: {len(cc)} căn cứ / {len(nhom)} họ ({', '.join(nhom) or '—'})")
        if len(cc) >= 3 and len(nhom) < 3:
            cb.append(f"{ten}: {len(cc)} căn cứ nhưng chỉ {len(nhom)} họ chỉ báo — hội tụ có thể đang đếm trùng")
    return loi, cb, tt


# ---------------- khoá + mục lục ----------------
def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _git(*args):
    try:
        return subprocess.run(["git", *args], cwd=GOC, capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return ""


def _sha_ho_so(kh):
    """Dựng lại hồ sơ tại T OFFLINE từ cache của bot (đúng dữ liệu bot đã thấy) → sha256 Markdown."""
    try:
        sys.path.insert(0, str(DAY))
        import ngu_canh as NC
        t = doc_gio(kh["gio_cat"])
        hs = NC.tao_ho_so(kh["ma"], kh["khung_hoi"], t, 30, None, True)
        return hashlib.sha256(NC.ve_markdown(hs).encode("utf-8")).hexdigest()
    except Exception as e:  # thiếu cache, mã lạ…
        return f"không dựng lại được: {type(e).__name__}: {e}"


def tao_khoa(kh, sha_ho_so=True):
    t = doc_gio(kh["gio_cat"])
    the = dt.datetime.fromtimestamp(t, VN).strftime("%Y%m%d_%H%M")
    files = list(FILE_KHOA) + sorted(str(p.relative_to(GOC)) for p in (DAY / "_so_tay_T" / the).glob("*.md"))
    sha = {f: sha256_file(GOC / f) for f in files if (GOC / f).exists()}
    ban = _git("status", "--porcelain", "--", *FILE_KHOA)
    return {
        "gio_luu": bay_gio_vn(),
        "git": _git("rev-parse", "HEAD") or "không có git",
        "file_chua_commit": [x[3:] for x in ban.splitlines()],
        "sha256": sha,
        "sha256_ho_so": _sha_ho_so(kh) if sha_ho_so else "bỏ qua",
        "che_do": "hoi_cuu" if doc_gio(kh["gio_phat_hanh"]) - t > 24 * 3600 else "truc_tiep",
    }


def doc_muc_luc(thu_muc=KE_HOACH):
    p = Path(thu_muc) / MUC_LUC
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def luu(duong, thu_muc=KE_HOACH, sha_ho_so=True):
    """Kiểm + khoá + ghi mục lục. → (ok, thông báo)."""
    duong, thu_muc = Path(duong), Path(thu_muc)
    kh = json.loads(duong.read_text(encoding="utf-8"))
    if kh.get("khoa"):
        return False, f"{duong.name}: đã khoá lúc {kh['khoa'].get('gio_luu')} — không sửa kế hoạch đã khoá"
    if any(r["tep"] == duong.name for r in doc_muc_luc(thu_muc)):
        return False, f"{duong.name}: đã có trong mục lục — đặt tên mới (_2, _3)"
    if duong.resolve().parent != thu_muc.resolve():
        return False, f"file phải nằm trong {thu_muc}"
    if Path(kh.get("tep_doi_chieu", "")).stem != duong.stem:
        return False, f"tên file ({duong.stem}) phải trùng stem của tep_doi_chieu ({kh.get('tep_doi_chieu')})"
    loi, cb, tt = kiem(kh)
    if loi:
        return False, "LỖI:\n" + "\n".join("  - " + x for x in loi)
    kh["khoa"] = tao_khoa(kh, sha_ho_so)
    duong.write_text(json.dumps(kh, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    p = thu_muc / MUC_LUC
    moi = not p.exists()
    with p.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COT_MUC_LUC, delimiter="\t")
        if moi:
            w.writeheader()
        w.writerow({"tep": duong.name, "ma": kh["ma"], "khung_hoi": kh["khung_hoi"], "gio_cat": kh["gio_cat"],
                    "gio_phat_hanh": kh["gio_phat_hanh"], "che_do": kh["khoa"]["che_do"],
                    "sha256": sha256_file(duong), "git": kh["khoa"]["git"][:12], "gio_luu": kh["khoa"]["gio_luu"]})
    ra = [f"ĐÃ KHOÁ {duong.name} · {kh['khoa']['che_do']} · git {kh['khoa']['git'][:12]}"]
    if kh["khoa"]["file_chua_commit"]:
        ra.append("  ⚠ file luật/code chưa commit: " + ", ".join(kh["khoa"]["file_chua_commit"]))
    ra += ["  ⚠ " + x for x in cb] + ["  · " + x for x in tt]
    return True, "\n".join(ra)


def kiem_khoa(duong, thu_muc=KE_HOACH):
    """File kế hoạch còn đúng như lúc khoá? → (ok, lý do)."""
    duong = Path(duong)
    for r in doc_muc_luc(thu_muc):
        if r["tep"] == duong.name:
            if sha256_file(duong) == r["sha256"]:
                return True, "đúng sha256 lúc khoá"
            return False, "ĐÃ BỊ SỬA sau khi khoá (sha256 khác mục lục)"
    return False, "chưa khoá (không có trong mục lục)"


# ---------------- view trước T ----------------
def tim_truoc(ma, T, thu_muc=KE_HOACH):
    """Kế hoạch mới nhất của MÃ có gio_phat_hanh ≤ T, file còn đúng sha. → (đường dẫn | None, cảnh báo)."""
    thu_muc = Path(thu_muc)
    cb, ung = [], []
    for r in doc_muc_luc(thu_muc):
        if r["ma"] != ma or doc_gio(r["gio_phat_hanh"]) > T:
            continue
        p = thu_muc / r["tep"]
        if not p.exists() or sha256_file(p) != r["sha256"]:
            cb.append(f"{r['tep']}: thiếu file hoặc đã bị sửa sau khoá → bỏ qua")
            continue
        ung.append((doc_gio(r["gio_phat_hanh"]), doc_gio(r["gio_cat"]), p))
    if not ung:
        return None, cb
    return max(ung)[2], cb


def _mo_ta_dk(dk):
    return f"nến {dk['khung']} ĐÓNG {'trên' if dk['phia'] == 'tren' else 'dưới'} {dk['gia']}" + (
        f" ({dk['so_nen']} cây)" if dk.get("so_nen", 1) > 1 else "")


def truoc(ma, T, thu_muc=KE_HOACH, gia=None, cache_dir=None, offline=False):
    """Văn bản ngắn cho bot đọc ở Bước 0: view đã phát hành trước T + trạng thái tới T (dữ liệu ≤ T)."""
    p, cb = tim_truoc(ma, T, thu_muc)
    ra = [f"# View trước T — {ma} · T = {gio_vn(T)} VN (chỉ kế hoạch có gio_phat_hanh ≤ T)"]
    ra += ["⚠ " + x for x in cb]
    if p is None:
        ra.append("KHỞI TẠO VIEW: chưa có nhận định nào của bot cho mã này phát hành trước T. Ghi dòng "
                  "\"View: KHỞI TẠO <hướng> (suy từ trạng thái T−24h, chưa có view đã phát hành)\" — không nói như đã "
                  "biết view hôm trước.")
        return "\n".join(ra), None
    kh = json.loads(p.read_text(encoding="utf-8"))
    tuoi = (T - doc_gio(kh["gio_cat"])) / 86400
    ra.append(f"Kế hoạch trước: {p.name} · dữ liệu tới {kh['gio_cat']} · phát hành {kh['gio_phat_hanh']} "
              f"· cách T {tuoi:.1f} ngày")
    if tuoi > VIEW_CU_NGAY:
        ra.append(f"QUÁ CŨ (> {VIEW_CU_NGAY} ngày) → coi như KHỞI TẠO VIEW; phần dưới chỉ để tham khảo.")
    loai = "KHOI_TAO" if tuoi > VIEW_CU_NGAY else "TU_KE_HOACH"
    for kv in ("H4", "D1", "W1"):
        v = kh["view"][kv]
        if v["huong"] == "PHAN_VAN":
            ra.append(f"- {kv}: PHÂN VÂN — chờ đóng trên {v['cho']['tren']} / dưới {v['cho']['duoi']}")
            continue
        ra.append(f"- {kv}: {v.get('nhan') or v['huong']} ({v['do_chac']}) · đích {list(vung(v['dich']))} · sai khi "
                  f"{_mo_ta_dk(v['sai_khi'])} · hạn {v['han']}")
    ra.append(f"- Hành động lúc đó: {kh['hanh_dong']}")
    for q in kh["ke_hoach"]:
        if q.get("hanh_dong") in CO_VAO:
            ra.append(f"- Kế hoạch {q['id']}: {q['chieu']} {q['hanh_dong']} vào {list(vung(q['vao']) or [])} · TP "
                      f"{[list(vung(x)) for x in q['tp']]} · đóng khi "
                      f"{'; '.join(_mo_ta_dk(d) for d in q.get('dong_khi') or []) or '—'}")
    import cham_ke_hoach as CH
    if gia is not None and gia.den > T:
        raise ValueError(f"nguồn giá có dữ liệu tới {gio_vn(gia.den)} > T — view trước T chỉ được dùng nến ≤ T")
    try:
        g = gia or CH.Gia(ma, CH.bat_dau_cua(kh) - 7 * 86400, T, cache_dir or CH.CACHE_CHAM, offline)
        ra.append(f"Trạng thái tới T (chỉ nến đóng ≤ {gio_vn(T)} VN):")
        ra += ["  " + x for x in CH.trang_thai_toi(kh, g)]
    except Exception as e:
        ra.append(f"Chưa tính được trạng thái tới T (thiếu dữ liệu giá: {type(e).__name__}) — tự xét bằng hồ sơ.")
    ra.append(f"→ Ghi view_truoc: {{\"loai\": \"{loai}\", \"tep\": \"{p.name}\"}}; dòng View: GIỮ / ĐỔI so với view "
              "này (nêu sự kiện a–d), hoặc KHỞI TẠO nếu quá cũ.")
    return "\n".join(ra), p


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) == 2 and a[0] == "kiem":
        loi, cb, tt = kiem(json.loads(Path(a[1]).read_text(encoding="utf-8")))
        for x in loi:
            print("LỖI  " + x)
        for x in cb:
            print("CẢNH BÁO  " + x)
        for x in tt:
            print("·  " + x)
        print("ĐẠT" if not loi else f"KHÔNG ĐẠT ({len(loi)} lỗi)")
        return 1 if loi else 0
    if len(a) == 2 and a[0] == "luu":
        ok, msg = luu(a[1])
        print(msg)
        return 0 if ok else 1
    if len(a) >= 3 and a[0] == "truoc":
        txt, _p = truoc(a[1].upper(), doc_gio(a[2]), offline="--offline" in a)
        print(txt)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
