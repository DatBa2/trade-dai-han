#!/usr/bin/env python3
"""Chấm bài thi bot v3: so bài làm thi/bai_lam/<tên>.json với phiếu thật phieu/<tên>.json.

Hướng H4 của mỗi bên = phần tử khung H4, không có thì "chung" (không có cả hai → bỏ khỏi phần so hướng).
Chấm gồm:
  Mốc cắt C = lúc KẾT THÚC live (hs.ds_buoi); nhãn người đó = view cuối buổi. Mọi cách đoán chấm trên cùng tập, cùng thước.
  1. Độ chính xác 3 nhãn (chỉ số chính), macro-F1, balanced accuracy, khi cả 2 có hướng (kèm mẫu số),
     bảng chéo 3×3, kappa Cohen; tách live sáng/đêm và giờ thật/không chắc.
     Mốc so sánh trên cùng các buổi: luôn GIẢM · chép nguyên nhãn buổi trước · giữ view (hướng TĂNG/GIẢM
     gần nhất của người đó, bỏ qua buổi PHÂN VÂN) · luật từ trên xuống (EMA H4 34/89/200 chụm < 0,6% → PHÂN VÂN;
     không thì TĂNG khi đóng D1 ≤ EMA89 D1 × 1,01 và nhịp 24h > −1%; còn lại GIẢM).
     Bootstrap 2.000 lần → khoảng tin cậy 95% cho % trùng; McNemar (nhị thức chính xác) bot vs từng mốc.
  2. PHÂN VÂN chấm riêng: bot PV khi người PV (đúng) / bot PV khi người có hướng (bỏ lỡ) / bot có hướng khi người PV.
  3. Đợt view (chuỗi buổi liên tiếp cùng nhãn của người đó): % lần người đó đổi view mà bot đổi sang cùng nhãn
     ở cùng buổi hoặc lệch ≤ 1 buổi.
  4. Đúng/sai theo thị trường bằng cong_cu/cham_dich.py::cham (HAN_CO_DINH=336 giờ = 14 ngày) cho cả bot lẫn người:
     ĐÚNG = chạm đích (râu tính) trước khi bị vô hiệu; SAI = chạm SL hoặc H4 ĐÓNG qua mốc sai trước; CHƯA RÕ = hết hạn.
     Mọi bên tính từ C. Mốc so sánh có đích: chép nguyên view buổi trước, giữ view. Hạn chưa trôi hết → CHUA_HET_HAN.
  5. Phép thử đối xứng: đặt mốc phía kia cách giá cùng khoảng như đích (đường 2 chặng: mốc phía kia ít nhất tới đích
     chặng 1) → chiều được chọn có tới trước không (50% = không hơn tung đồng xu).
  6. Độ lệch đích / mốc sai (%) khi cả 2 cùng hướng và đều có số.
Cách dùng: python3 thi/cham.py [--bai-lam THƯ_MỤC] [--ra FILE.md]
"""
import datetime as dt, json, math, os, random, re, sys, unicodedata
from bisect import bisect_left
from collections import Counter
from pathlib import Path

os.environ["HAN_CO_DINH"] = "336"  # hạn cố định 14 ngày cho cd.cham (đọc lúc gọi)
THI = Path(__file__).resolve().parent
GOC = THI.parent
sys.path[:0] = [str(THI), str(GOC / "cong_cu")]
import tao_ho_so as hs  # noqa: E402
import cham_dich as cd  # noqa: E402

HAN = dt.timedelta(hours=336)
NHAN = ["TANG", "GIAM", "PHAN_VAN"]
VIET = {"TANG": "TĂNG", "GIAM": "GIẢM", "PHAN_VAN": "PHÂN VÂN", None: "—"}
MOC_SO = ["Luôn GIẢM", "Chép buổi trước", "Giữ view", "Luật từ trên xuống"]
SO_BOOT = 2000


# ───────────────────────── chuẩn hoá ─────────────────────────
def chuan_huong(x):
    if x is None:
        return None
    s = unicodedata.normalize("NFD", str(x)).encode("ascii", "ignore").decode().upper().strip().replace(" ", "_")
    if s in ("TANG", "LONG", "UP"): return "TANG"
    if s in ("GIAM", "SHORT", "DOWN"): return "GIAM"
    if s.replace("_", "") in ("PHANVAN", "PV", "DUNGNGOAI", "TRUNGLAP", "SIDEWAY"): return "PHAN_VAN"
    return None


def chuan_so(x):
    """'82000' → '82.000' để cd.so_trong đọc được (nó chỉ nhận dạng 82.000 / 82k / 82)."""
    return re.sub(r"(?<![\d.,])(\d{2,3})(\d{3})(?![\d.,])", r"\1.\2", x) if isinstance(x, str) else (
        chuan_so(f"{x:.0f}") if isinstance(x, (int, float)) else x)


def chuan_bai(d):
    """Bài làm/phiếu → dạng phiếu mà cd.cham hiểu; chỉ giữ 1 view H4 (hoặc chung)."""
    d = json.loads(json.dumps(d))
    for n in d.get("nhan_dinh") or []:
        n["huong"] = chuan_huong(n.get("huong"))
        k = str(n.get("khung") or "").upper()
        n["khung"] = {"4H": "H4", "CHUNG": "chung", "1D": "D1", "1W": "W1"}.get(k, n.get("khung"))
        n["vo_hieu_khi"] = chuan_so(n.get("vo_hieu_khi"))
        for k2 in ("duong_di",):
            n.setdefault(k2, None)
    for l in d.get("lenh") or []:
        l.setdefault("trang_thai", "de_xuat_moi")
        c = chuan_huong(l.get("chieu"))
        l["chieu"] = {"TANG": "LONG", "GIAM": "SHORT"}.get(c, l.get("chieu"))
    v = hs.huong_h4(d)
    d["nhan_dinh"] = [v] if v else []
    return d, (v.get("huong") if v else None)


# ───────────────────────── tách đích / mốc sai (cùng logic cd.cham) ─────────────────────────
def gia_luc(bat_dau):
    i0 = bisect_left(cd.T1, bat_dau)
    return (cd.H1[i0 - 1][3] if i0 else cd.H1[0][3]) if i0 < len(cd.H1) else None, i0


def tach_view(d, bat_dau):
    n = (d.get("nhan_dinh") or [{}])[0]; huong = n.get("huong")
    if huong not in ("TANG", "GIAM"):
        return None
    dich = (n.get("duong_di") or [{}])[-1].get("dich") if n.get("duong_di") else n.get("dich")
    if isinstance(dich, list):
        dich = [x for x in dich if isinstance(x, (int, float))]
        dich = (max(dich) if huong == "GIAM" else min(dich)) if dich else None
    gia, i0 = gia_luc(bat_dau)
    if not isinstance(dich, (int, float)) or gia is None or (huong == "GIAM" and dich >= gia) or (huong == "TANG" and dich <= gia):
        dich = None
    c1 = None
    dd = n.get("duong_di") or []
    if len(dd) >= 2 and dd[0].get("huong") not in (huong, None):
        x = dd[0].get("dich"); x = [v for v in (x if isinstance(x, list) else [x]) if isinstance(v, (int, float))]
        if x and gia:
            c1 = max(x) if huong == "GIAM" else min(x)
    nguong = gia if c1 is None else (max(c1, gia) if huong == "GIAM" else min(c1, gia))
    vh = n.get("vo_hieu_khi") or ""
    bat_loi = [] if re.search(r"\bM(5|15|30)\b|\b(5|15|30) phút|\bH1\b|scalp", vh, re.I) or nguong is None else \
        [v for v in cd.so_trong(vh) if (v > nguong if huong == "GIAM" else v < nguong)]
    moc_sai = (min(bat_loi) if huong == "GIAM" else max(bat_loi)) if bat_loi else None
    return {"huong": huong, "dich": dich, "gia": gia, "i0": i0, "c1": c1, "moc_sai": moc_sai}


def cham_thi_truong(d, bat_dau):
    if not d.get("nhan_dinh"):
        return "KHONG_VIEW", None
    kq, luc = cd.cham(d, bat_dau)
    het_du_lieu = cd.H1[-1][0] + dt.timedelta(hours=1)
    if kq in ("CHUA_RO", "SAI_HET_HAN", "CHUA_DU_LIEU") and bat_dau + HAN > het_du_lieu:
        kq = "CHUA_HET_HAN"
    return kq, luc


def doi_xung(d, bat_dau):
    """Mốc phía kia cùng khoảng cách (≥ đích chặng 1 nếu đường 2 chặng); chiều chọn tới trước → THANG."""
    v = tach_view(d, bat_dau) if d.get("nhan_dinh") else None
    if not v or v["dich"] is None:
        return None
    gia, dich, huong = v["gia"], v["dich"], v["huong"]
    kia = gia + abs(gia - dich) if huong == "GIAM" else gia - abs(gia - dich)
    tu_c1 = False
    if v["c1"] is not None and ((huong == "GIAM" and v["c1"] >= kia) or (huong == "TANG" and v["c1"] <= kia)):
        kia, tu_c1 = v["c1"], True  # chạm đúng đích chặng 1 là cố ý → phải vượt hẳn mới tính thua
    het = bat_dau + HAN
    for t, h, l, c in cd.H1[v["i0"]:]:
        if t >= het:
            return "CHUA_NGA_NGU"
        toi = l <= dich if huong == "GIAM" else h >= dich
        kia_cham = ((h > kia) if tu_c1 else (h >= kia)) if huong == "GIAM" else ((l < kia) if tu_c1 else (l <= kia))
        if toi and kia_cham:
            return "CUNG_NEN"
        if toi:
            return "THANG"
        if kia_cham:
            return "THUA"
    return "CHUA_HET_HAN"


# ───────────────────────── thống kê ─────────────────────────
def p_nhi_thuc(k, n):
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2 ** n)


def ty_le(a, b):
    return f"{a}/{b} = {a / b:.0%}" if b else "—"


def bat_doi_view(nguoi, may, truoc_nguoi):
    """Trả về [(chỉ số buổi người đổi, nhãn mới, độ lệch bot hoặc None)]. Bot đổi sang cùng nhãn ở j, |j−i| ≤ 1."""
    ra = []
    for i, x in enumerate(nguoi):
        cu = nguoi[i - 1] if i else truoc_nguoi
        if cu is None or x == cu:
            continue
        lech = None
        for j in (i, i - 1, i + 1):
            if 0 <= j < len(may) and may[j] == x and (j == 0 or may[j - 1] != x):
                lech = j - i; break
        ra.append((i, x, lech))
    return ra


# ───────────────────────── chính ─────────────────────────
def chi_so(v, ng):
    """v: nhãn dự đoán (có thể None = không có nhãn, tính là sai); ng: nhãn người đó."""
    n = len(ng)
    f1, rec = [], []
    for c in NHAN:
        tp = sum(1 for x, y in zip(v, ng) if x == c and y == c)
        fp = sum(1 for x, y in zip(v, ng) if x == c and y != c)
        fn = sum(1 for x, y in zip(v, ng) if x != c and y == c)
        f1.append(2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0)
        if tp + fn:
            rec.append(tp / (tp + fn))
    po = sum(x == y for x, y in zip(v, ng)) / n
    nh = set(v) | set(ng)
    pe = sum(sum(1 for x in v if x == c) * sum(1 for y in ng if y == c) for c in nh) / n ** 2
    return {"f1": sum(f1) / 3, "bacc": sum(rec) / len(rec) if rec else None, "kappa": None if pe == 1 else (po - pe) / (1 - pe)}


def nhom(b):
    gio = b.bat_dau.astimezone(hs.VN).hour
    return ("Live sáng (06–14h VN)" if 6 <= gio < 14 else "Live tối/đêm"), ("Giờ live thật" if b.chac else "Giờ không chắc")


def main():
    a = sys.argv[1:]
    thu_muc = Path(a[a.index("--bai-lam") + 1]) if "--bai-lam" in a else THI / "bai_lam"
    ra_file = Path(a[a.index("--ra") + 1]) if "--ra" in a else THI / "KET_QUA_THI.md"
    du = hs.DuLieu()
    tat_ca = hs.ds_buoi()
    thi = hs.buoi_thi(tat_ca)
    phieu = {b.ten: chuan_bai(hs.doc_json(b.phieu)) for b in tat_ca}
    nhan_nguoi = {k: v[1] for k, v in phieu.items()}
    dong, loai = [], []
    for b in thi:
        p = thu_muc / f"{b.ten}.json"
        if not p.exists():
            loai.append((b.ten, "không có bài làm")); continue
        nguoi_d, nguoi = phieu[b.ten]
        bot_d, bot = chuan_bai(hs.doc_json(p))
        truoc = hs.buoi_truoc(tat_ca, b)
        lien = truoc[-1] if truoc else None
        giu_b = next((x for x in reversed(truoc) if nhan_nguoi.get(x.ten) in ("TANG", "GIAM")), None)
        # luật từ trên xuống — chỉ dùng dữ liệu tới mốc cắt C (giống hồ sơ của bot)
        cat = hs.Cat(du, b.C)
        c4 = [n.c for n in cat.h4]
        e = [hs.ema(c4, k)[-1] for k in (34, 89, 200)]
        e89d = hs.ema([n.c for n in cat.d1], 89)[-1]
        p24 = hs.doi_gia_luc(cat, cat.T - dt.timedelta(hours=24))
        nhip = (cat.gia / p24 - 1) * 100
        if (max(e) - min(e)) / cat.gia * 100 < 0.6:
            luat = "PHAN_VAN"
        elif cat.d1[-1].c <= e89d * 1.01 and nhip > -1:
            luat = "TANG"
        else:
            luat = "GIAM"
        C = b.C.replace(tzinfo=None)  # cong_cu/cham_dich dùng giờ UTC không múi; mọi bên chấm từ cùng mốc C
        views = {"Bot": bot_d, "Người đó": nguoi_d,
                 "Chép view buổi trước": phieu[lien.ten][0] if lien else {"nhan_dinh": []},
                 "Giữ view": phieu[giu_b.ten][0] if giu_b else {"nhan_dinh": []}}
        dong.append(dict(b=b, nguoi=nguoi, bot=bot,
                         moc={"Luôn GIẢM": "GIAM", "Chép buổi trước": nhan_nguoi.get(lien.ten) if lien else None,
                              "Giữ view": nhan_nguoi.get(giu_b.ten) if giu_b else None, "Luật từ trên xuống": luat},
                         tt={k: cham_thi_truong(v, C) for k, v in views.items()},
                         dx={k: doi_xung(v, C) for k, v in views.items()},
                         vn=tach_view(nguoi_d, C), vb=tach_view(bot_d, C),
                         truoc_nguoi=nhan_nguoi.get(lien.ten) if lien else None))
    L = ["# Kết quả thi bot v3",
         f"Chấm lúc {dt.datetime.now(hs.VN):%Y-%m-%d %H:%M} VN · bài làm: `{thu_muc}` · {len(dong)}/{len(thi)} buổi thi có bài làm"
         f" · giá H1 có tới {cd.H1[-1][0] + hs.VN.utcoffset(None):%Y-%m-%d %H:%M} VN",
         "Quy ước: mốc cắt C = lúc KẾT THÚC live (giờ thật từ transcripts/gio_live.tsv; thiếu thì giờ không chắc). "
         "Bot chỉ thấy dữ liệu trước C; nhãn so sánh = view H4 (không có thì 'chung') CUỐI buổi của người đó. "
         "Mọi cách đoán chấm trên CÙNG tập buổi, cùng thước; chấm theo thị trường đều tính từ C."]
    if not dong:
        ra_file.write_text("\n".join(L + ["", "Không có bài làm nào."]) + "\n", encoding="utf-8"); print("Không có bài làm."); return
    so = []
    for r in dong:
        if not r["nguoi"]:
            loai.append((r["b"].ten, "phiếu người đó không có nhãn H4/chung"))
        elif not r["bot"]:
            loai.append((r["b"].ten, "bài làm không có nhãn H4/chung hợp lệ"))
        else:
            so.append(r)
    N = len(so)
    L.append(f"Tập so hướng: **{N}/{len(thi)}** buổi · bị loại {len(loai)}: "
             + ("; ".join(f"{t} ({ly})" for t, ly in loai) if len(loai) <= 8 else
                ", ".join(f"{ly}: {c}" for ly, c in Counter(ly for _, ly in loai).items()) + " (danh sách ở cuối)"))
    if not N:
        ra_file.write_text("\n".join(L) + "\n", encoding="utf-8"); print("Không có buổi so hướng được."); return

    # 1. trùng hướng + mốc so sánh
    pp = {"Bot": [r["bot"] for r in so]} | {m: [r["moc"][m] for r in so] for m in MOC_SO}
    ng = [r["nguoi"] for r in so]
    dung = {k: [int(x == y) for x, y in zip(v, ng)] for k, v in pp.items()}
    rnd = random.Random(2026)
    boot = {k: [] for k in pp}
    for _ in range(SO_BOOT):
        idx = [rnd.randrange(N) for _ in range(N)]
        for k in pp:
            boot[k].append(sum(dung[k][i] for i in idx) / N)
    pb = Counter(pp["Bot"]); pn = Counter(ng)
    L += ["", f"## 1. Trùng hướng H4 với người đó (cùng {N} buổi, cùng mẫu số)",
          f"Người đó: TĂNG {pn['TANG']} · GIẢM {pn['GIAM']} · PHÂN VÂN {pn['PHAN_VAN']} — Bot: TĂNG {pb['TANG']} · GIẢM {pb['GIAM']} · PHÂN VÂN {pb['PHAN_VAN']}",
          "| Cách đoán | Thiếu nhãn (tính sai) | Độ chính xác 3 nhãn | KTC 95% (bootstrap 2.000) | Macro-F1 | Balanced acc. | Khi cả 2 có hướng | Kappa | McNemar bot vs mốc (bot đúng–mốc sai / ngược lại, p) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k, v in pp.items():
        s = sorted(boot[k]); ci = f"{s[int(0.025 * SO_BOOT)]:.0%} – {s[int(0.975 * SO_BOOT) - 1]:.0%}"
        ch = [(x, y) for x, y in zip(v, ng) if x in ("TANG", "GIAM") and y in ("TANG", "GIAM")]
        cs = chi_so(v, ng)
        if k == "Bot":
            mc = "—"
        else:
            b_ = sum(1 for x, y in zip(dung["Bot"], dung[k]) if x and not y)
            c_ = sum(1 for x, y in zip(dung["Bot"], dung[k]) if y and not x)
            mc = f"{b_} / {c_}, p = {p_nhi_thuc(b_, b_ + c_):.3f}"
        bacc = "—" if cs["bacc"] is None else f"{cs['bacc']:.2f}"
        kp = "—" if cs["kappa"] is None else f"{cs['kappa']:.2f}"
        L.append(f"| {k} | {sum(x is None for x in v)} | **{ty_le(sum(dung[k]), N)}** | {ci} | {cs['f1']:.2f} | {bacc} | "
                 f"{ty_le(sum(x == y for x, y in ch), len(ch))} | {kp} | {mc} |")
    L.append("_Chỉ số chính = độ chính xác 3 nhãn trên toàn tập. 'Khi cả 2 có hướng' là chỉ số có điều kiện, luôn đọc kèm mẫu số. "
             "Chép buổi trước = nguyên nhãn buổi liền trước; Giữ view = hướng TĂNG/GIẢM gần nhất của người đó (bỏ qua buổi PHÂN VÂN)._")
    L += ["", "### Bảng chéo (dòng = người đó, cột = bot)", "| | " + " | ".join(VIET[h] for h in NHAN) + " | Tổng |",
          "|---|---|---|---|---|"]
    for x in NHAN:
        hang = [sum(1 for r in so if r["nguoi"] == x and r["bot"] == y) for y in NHAN]
        L.append(f"| **{VIET[x]}** | " + " | ".join(map(str, hang)) + f" | {sum(hang)} |")
    L.append("| Tổng | " + " | ".join(str(sum(1 for r in so if r["bot"] == y)) for y in NHAN) + f" | {N} |")
    # theo nhóm
    L += ["", "### Theo nhóm buổi (độ chính xác 3 nhãn)", "| Nhóm | Số buổi | " + " | ".join(pp) + " |", "|---|---|" + "---|" * len(pp)]
    for nh_ in ("Live sáng (06–14h VN)", "Live tối/đêm", "Giờ live thật", "Giờ không chắc"):
        idx = [i for i, r in enumerate(so) if nh_ in nhom(r["b"])]
        if idx:
            L.append(f"| {nh_} | {len(idx)} | " + " | ".join(ty_le(sum(dung[k][i] for i in idx), len(idx)) for k in pp) + " |")

    # 2. PHÂN VÂN
    a_ = sum(1 for r in so if r["bot"] == "PHAN_VAN" and r["nguoi"] == "PHAN_VAN")
    b_ = sum(1 for r in so if r["bot"] == "PHAN_VAN" and r["nguoi"] != "PHAN_VAN")
    c_ = sum(1 for r in so if r["bot"] != "PHAN_VAN" and r["nguoi"] == "PHAN_VAN")
    L += ["", "## 2. PHÂN VÂN (chấm riêng)", "| Trường hợp | Số buổi |", "|---|---|",
          f"| Bot PHÂN VÂN khi người đó PHÂN VÂN (đúng) | {a_} |", f"| Bot PHÂN VÂN khi người đó có hướng (bỏ lỡ) | {b_} |",
          f"| Bot có hướng khi người đó PHÂN VÂN (ép hướng) | {c_} |",
          f"| Độ chính xác khi bot nói PHÂN VÂN | {ty_le(a_, a_ + b_)} |", f"| Bắt được PHÂN VÂN của người đó | {ty_le(a_, a_ + c_)} |"]

    # 3. đợt view
    truoc0 = so[0]["truoc_nguoi"]
    doi = {k: bat_doi_view(ng, v, truoc0) for k, v in pp.items()}
    dot, i = [], 0
    while i < N:
        j = i
        while j + 1 < N and ng[j + 1] == ng[i]:
            j += 1
        dot.append((i, j)); i = j + 1
    L += ["", "## 3. Giữ view: đợt view và thời điểm đổi view",
          f"Người đó có **{len(dot)} đợt view** trên {N} buổi (đợt = chuỗi buổi liên tiếp cùng nhãn), "
          f"**{len(doi['Bot'])} lần đổi view** (tính cả lần đổi ở buổi đầu so với buổi ngay trước kỳ thi).",
          "| Cách đoán | Bắt đúng lúc đổi (lệch ≤ 1 buổi) | Cùng buổi | Sớm 1 buổi | Trễ 1 buổi |", "|---|---|---|---|---|"]
    for k, v in doi.items():
        lech = Counter(x[2] for x in v)
        bat = sum(1 for x in v if x[2] is not None)
        L.append(f"| {k} | {ty_le(bat, len(v))} | {lech[0]} | {lech[-1]} | {lech[1]} |")
    L.append("_Lưu ý: 'Chép buổi trước' luôn trễ đúng 1 buổi nên bắt được gần hết theo tiêu chí ±1; xem cột 'Cùng buổi'._")
    L += ["", "Các đợt view của người đó:", "| Từ buổi | Đến buổi | Nhãn | Số buổi | Bot cùng nhãn trong đợt |", "|---|---|---|---|---|"]
    for i, j in dot:
        L.append(f"| {so[i]['b'].ten[:15]} | {so[j]['b'].ten[:15]} | {VIET[ng[i]]} | {j - i + 1} | "
                 f"{sum(1 for t in range(i, j + 1) if pp['Bot'][t] == ng[i])}/{j - i + 1} |")

    # 4. đúng/sai theo thị trường — cùng tập `dong`, cùng mốc C
    ben = ["Bot", "Người đó", "Chép view buổi trước", "Giữ view"]
    L += ["", f"## 4. Đúng/sai theo thị trường (cd.cham, hạn 14 ngày từ C; râu chạm đích tính; SAI = chạm SL / H4 ĐÓNG qua mốc sai trước) — {len(dong)} buổi",
          "| Bên | ĐÚNG | SAI | SAI hết hạn (không mốc sai, không chạm đích) | CHƯA RÕ | Chưa hết hạn | Không đích | Đích sai phía | PHÂN VÂN/không view | % đúng (đã ngã ngũ) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k in ben:
        c = Counter(r["tt"][k][0] for r in dong)
        xong = c["DUNG"] + c["SAI"] + c["SAI_HET_HAN"]
        L.append(f"| {k} | {c['DUNG']} | {c['SAI']} | {c['SAI_HET_HAN']} | {c['CHUA_RO']} | {c['CHUA_HET_HAN']} | {c['KHONG_DICH']} | "
                 f"{c['DICH_SAI_PHIA']} | {c['PHAN_VAN'] + c['KHONG_VIEW']} | {ty_le(c['DUNG'], xong)} |")
    L.append("_Chép view buổi trước / Giữ view = nguyên view H4 (đích, vô hiệu, lệnh) của buổi đó, chấm lại từ C của buổi thi. "
             "Luôn GIẢM và Luật từ trên xuống không có đích → không chấm được theo thước này._")

    # 5. đối xứng
    L += ["", "## 5. Phép thử đối xứng (mốc phía kia cùng khoảng cách; đường 2 chặng: ít nhất tới đích chặng 1; 50% = không hơn tung đồng xu)",
          "| Bên | View có đích | Chiều chọn tới trước | Phía kia tới trước | Cùng nến H1 | Chưa ngã ngũ (14 ngày) | Chưa hết hạn | % thắng | p (nhị thức, vs 50%) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k in ben:
        c = Counter(r["dx"][k] for r in dong if r["dx"][k])
        t, th = c["THANG"], c["THUA"]
        L.append(f"| {k} | {sum(c.values())} | {t} | {th} | {c['CUNG_NEN']} | {c['CHUA_NGA_NGU']} | {c['CHUA_HET_HAN']} | "
                 f"{ty_le(t, t + th)} | {p_nhi_thuc(t, t + th):.3f} |")

    # 6. độ lệch đích / mốc sai
    def lech(k):
        xs = [abs(r["vb"][k] - r["vn"][k]) / r["vn"][k] * 100 for r in dong
              if r["vn"] and r["vb"] and r["vn"]["huong"] == r["vb"]["huong"] and r["vn"][k] and r["vb"][k]]
        if not xs:
            return "—", 0
        s = sorted(xs)
        return f"TB {sum(xs) / len(xs):.2f}% · trung vị {s[len(s) // 2]:.2f}% · ≤1%: {sum(x <= 1 for x in xs)}/{len(xs)}", len(xs)
    L += ["", "## 6. Độ lệch số bot vs người đó (khi cùng hướng và đều có số; đích/mốc sai tách như cd.cham)",
          "| Thứ | Số buổi | Lệch |", "|---|---|---|"]
    for k, ten in (("dich", "Đích"), ("moc_sai", "Mốc sai (vô hiệu)")):
        s, n = lech(k)
        L.append(f"| {ten} | {n} | {s} |")

    # 7. từng buổi
    L += ["", "## 7. Từng buổi (* = giờ live không chắc)",
          "| Buổi | C (VN) | Người | Bot | Trùng | Luật | Giữ view | Chép | Thị trường: người / bot | Đối xứng: người / bot | Đích N / B | Mốc sai N / B |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    so_ = lambda v, k: hs.g(v[k]) if v and v.get(k) else "—"
    for r in dong:
        L.append(f"| {r['b'].ten}{'' if r['b'].chac else ' *'} | {hs.vn(r['b'].C, '%m-%d %H:%M')} | {VIET[r['nguoi']]} | {VIET[r['bot']]} | "
                 f"{'✓' if r['nguoi'] and r['nguoi'] == r['bot'] else ('—' if not (r['nguoi'] and r['bot']) else '✗')} | "
                 f"{VIET[r['moc']['Luật từ trên xuống']]} | {VIET[r['moc']['Giữ view']]} | {VIET[r['moc']['Chép buổi trước']]} | "
                 f"{r['tt']['Người đó'][0]} / {r['tt']['Bot'][0]} | {r['dx']['Người đó'] or '—'} / {r['dx']['Bot'] or '—'} | "
                 f"{so_(r['vn'], 'dich')} / {so_(r['vb'], 'dich')} | {so_(r['vn'], 'moc_sai')} / {so_(r['vb'], 'moc_sai')} |")
    if loai:
        L += ["", f"## Buổi bị loại khỏi phần so hướng ({len(loai)})"] + [f"- {t}: {ly}" for t, ly in loai]
    ra_file.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✓ {len(dong)} buổi chấm, {N} buổi so hướng → {ra_file}")
    print("  độ chính xác 3 nhãn: " + " · ".join(f"{k}: {ty_le(sum(dung[k]), N)}" for k in pp))


if __name__ == "__main__":
    main()
