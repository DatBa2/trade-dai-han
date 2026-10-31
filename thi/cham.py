#!/usr/bin/env python3
"""Chấm bài thi bot v3: so bài làm thi/bai_lam/<tên>.json với nhãn người đó <thư mục đáp án>/<tên>.json (--phieu, mặc định phieu).

Hướng H4 của mỗi bên = phần tử khung H4, không có thì "chung".
Chấm gồm:
  Mốc cắt C = lúc KẾT THÚC live (hs.ds_buoi); nhãn người đó = view cuối buổi. Mọi cách đoán chấm trên cùng tập, cùng thước.
  Mẫu số (Codex P1-10) = MỌI buổi thi mà nhãn người đó hợp lệ (có view H4/chung). Bot thiếu bài/không có nhãn hợp lệ
  = SAI; độ phủ của bot báo riêng.
  1. Độ chính xác 3 nhãn (chỉ số chính), macro-F1, balanced accuracy, khi cả 2 có hướng (kèm mẫu số),
     bảng chéo 3×3, kappa Cohen; tách live sáng/đêm và giờ thật/không chắc.
     Mốc so sánh trên cùng các buổi: luôn GIẢM · chép nguyên nhãn buổi trước · giữ view (hướng TĂNG/GIẢM
     gần nhất của người đó, bỏ qua buổi PHÂN VÂN) · luật từ trên xuống (EMA H4 34/89/200 chụm < 0,6% → PHÂN VÂN;
     không thì TĂNG khi đóng D1 ≤ EMA89 D1 × 1,01 và nhịp 24h > −1%; còn lại GIẢM).
     Bootstrap THEO KHỐI tuần ISO (2.000 lần, rút lại cả tuần) → KTC 95% cho % trùng VÀ cho CHÊNH LỆCH CẶP
     (bot − từng mốc so sánh, cùng buổi trong mỗi lần rút). McNemar (nhị thức chính xác) bot vs từng mốc.
  2. PHÂN VÂN chấm riêng.
  3. Đợt view: % lần người đó đổi view mà bot đổi sang cùng nhãn ở cùng buổi hoặc lệch ≤ 1 buổi.
  4. Đúng/sai theo thị trường bằng cong_cu/cham_dich.py::cham_chi_tiet cho bot, người đó và 2 mốc có đích:
     giá tham chiếu = close nến 5m cuối đã ĐÓNG ≤ C; diễn biến = nến 5m mở ≥ C; vô hiệu = nến đúng khung (H4/D1/W1,
     1–2 nến) đóng sau C; đích + SL cùng nến 5m → phân bằng 1m, vẫn cùng nến 1m → CHƯA RÕ THỨ TỰ (không tính đúng).
     Báo cả hạn cố định 14 ngày lẫn hạn tự nêu của view (trần 14 ngày, không nêu = 7 ngày). Hạn chưa trôi hết → CHUA_HET_HAN.
     View nhiều chặng: thêm bảng "đúng đường đi" (chạm đích chặng 1 rồi mới tới đích cuối, trước SL/vô hiệu).
  5. Phép thử đối xứng THẬT: mốc phía kia cách giá tham chiếu ĐÚNG BẰNG khoảng tới đích (không nới theo chặng 1);
     chiều chọn tới trước → thắng (50% = không hơn tung đồng xu). Phép thử chính chỉ gồm view KHÔNG có chặng đi ngược
     (1 chặng hoặc mọi chặng cùng hướng view); view có chặng cố ý đi ngược báo bảng riêng, không gộp.
  6. Độ lệch đích / mốc sai (%) khi cả 2 cùng hướng và đều có số.
Cách dùng: python3 thi/cham.py [--bai-lam THƯ_MỤC] [--phieu THƯ_MỤC_ĐÁP_ÁN] [--ra FILE.md]
"""
import datetime as dt, json, math, os, random, re, sys, unicodedata
from bisect import bisect_left
from collections import Counter, defaultdict
from pathlib import Path

os.environ["HAN_CO_DINH"] = "336"  # hạn cố định 14 ngày cho cd.cham (đọc lúc gọi)
THI = Path(__file__).resolve().parent
GOC = THI.parent
sys.path[:0] = [str(THI), str(GOC / "cong_cu")]
import tao_ho_so as hs  # noqa: E402
import cham_dich as cd  # noqa: E402

HAN_GIO = 336
HAN = dt.timedelta(hours=HAN_GIO)
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


# ───────────────────────── chấm theo thị trường ─────────────────────────
KHONG_VIEW = {"ket_qua": "KHONG_VIEW", "luc": None, "dich": None, "moc_sai": None, "gia_tham_chieu": None, "huong": None,
              "nhieu_chang": False, "di_nguoc": False, "vo_hieu_chua_hieu": False, "ket_qua_duong_di": None,
              "han_co_dinh": {"ket_qua": "KHONG_VIEW", "duong_di": None}, "han_view": {"ket_qua": "KHONG_VIEW", "duong_di": None}}


def cham_thi_truong(d, C):
    """cd.cham_chi_tiet với hạn cố định 14 ngày (kèm hạn tự nêu trong r['han_view'])."""
    if not d.get("nhan_dinh"):
        return dict(KHONG_VIEW, C=C)
    return cd.cham_chi_tiet(d, C, HAN_GIO)


def doi_xung(ct):
    """Mốc phía kia cách giá tham chiếu ĐÚNG BẰNG khoảng tới đích (đối xứng thật, không nới theo chặng 1).
    Chiều chọn tới trước → THANG; phía kia trước → THUA; cùng nến 5m → phân bằng 1m, vẫn cùng/thiếu 1m → CUNG_NEN."""
    if ct.get("dich") is None or ct.get("gia_tham_chieu") is None or ct["ket_qua"] in (
            "PHAN_VAN", "KHONG_DICH", "DICH_SAI_PHIA", "CHUA_DU_LIEU", "KHONG_VIEW"):
        return None
    gia, dich, huong, C = ct["gia_tham_chieu"], ct["dich"], ct["huong"], ct["C"]
    kia = gia + abs(gia - dich) if huong == "GIAM" else gia - abs(gia - dich)
    toi = (lambda h, l: l <= dich) if huong == "GIAM" else (lambda h, l: h >= dich)
    kia_cham = (lambda h, l: h >= kia) if huong == "GIAM" else (lambda h, l: l <= kia)
    M = cd.nen_5m()
    het = C + HAN
    for t, h, l, c in M[bisect_left(cd.T5, C):]:
        if t >= het:
            return "CHUA_NGA_NGU"
        a, b = toi(h, l), kia_cham(h, l)
        if a and b:
            return {"A": "THANG", "B": "THUA"}.get(cd.thu_tu_1m(t, toi, kia_cham), "CUNG_NEN")
        if a:
            return "THANG"
        if b:
            return "THUA"
    return "CHUA_HET_HAN"


# ───────────────────────── thống kê ─────────────────────────
def p_nhi_thuc(k, n):
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2 ** n)


def ty_le(a, b):
    return f"{a}/{b} = {a / b:.0%}" if b else "—"


def ktc(xs, dau=False):
    s = sorted(xs)
    a, b = s[int(0.025 * len(s))], s[int(0.975 * len(s)) - 1]
    return f"{a * 100:+.0f} – {b * 100:+.0f} điểm %" if dau else f"{a:.0%} – {b:.0%}"


def boot_khoi(so, dung, ben, so_lan=SO_BOOT, seed=2026):
    """Bootstrap theo KHỐI tuần ISO (giờ VN của C): mỗi lần rút có hoàn lại đủ số tuần, lấy cả tuần.
    Trả (tỷ lệ đúng từng bên, chênh lệch cặp bot − từng bên khác, số khối)."""
    tuan = defaultdict(list)
    for i, r in enumerate(so):
        tuan[r["b"].C.astimezone(hs.VN).isocalendar()[:2]].append(i)
    khoi = list(tuan.values())
    rnd = random.Random(seed)
    tl = {k: [] for k in ben}
    hieu = {k: [] for k in ben if k != "Bot"}
    for _ in range(so_lan):
        idx = [i for _ in khoi for i in rnd.choice(khoi)]
        a = {k: sum(dung[k][i] for i in idx) / len(idx) for k in ben}
        for k in ben:
            tl[k].append(a[k])
        for k in hieu:
            hieu[k].append(a["Bot"] - a[k])
    return tl, hieu, len(khoi)


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
    thu_muc = hs.duong_dan(a[a.index("--bai-lam") + 1]) if "--bai-lam" in a else THI / "bai_lam"
    thu_muc_phieu = a[a.index("--phieu") + 1] if "--phieu" in a else "phieu"
    ra_file = Path(a[a.index("--ra") + 1]) if "--ra" in a else THI / "KET_QUA_THI.md"
    du = hs.DuLieu()
    tat_ca = hs.ds_buoi(thu_muc_phieu)
    thi = hs.buoi_thi(tat_ca)
    phieu = {b.ten: chuan_bai(hs.doc_json(b.phieu)) for b in tat_ca}
    nhan_nguoi = {k: v[1] for k, v in phieu.items()}
    dong = []
    for b in thi:
        p = thu_muc / f"{b.ten}.json"
        co_bai = p.exists()
        nguoi_d, nguoi = phieu[b.ten]
        bot_d, bot = chuan_bai(hs.doc_json(p)) if co_bai else ({"nhan_dinh": []}, None)
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
        tt = {k: cham_thi_truong(v, C) for k, v in views.items()}
        dong.append(dict(b=b, nguoi=nguoi, bot=bot if bot in NHAN else None, co_bai=co_bai,
                         moc={"Luôn GIẢM": "GIAM", "Chép buổi trước": nhan_nguoi.get(lien.ten) if lien else None,
                              "Giữ view": nhan_nguoi.get(giu_b.ten) if giu_b else None, "Luật từ trên xuống": luat},
                         tt=tt, dx={k: doi_xung(v) for k, v in tt.items()},
                         truoc_nguoi=nhan_nguoi.get(lien.ten) if lien else None))
    M = cd.nen_5m()
    L = ["# Kết quả thi bot v3 (bộ chấm sau sửa P0 — thi/SUA_P0.md)",
         f"Chấm lúc {dt.datetime.now(hs.VN):%Y-%m-%d %H:%M} VN · bài làm: `{thu_muc}` · đáp án: `{hs.duong_dan(thu_muc_phieu)}` · "
         f"{sum(r['co_bai'] for r in dong)}/{len(thi)} buổi thi có bài làm"
         + (f" · nến 5m có tới {M[-1][0] + cd.NAM_PHUT + cd.VN:%Y-%m-%d %H:%M} VN" if M else " · CHƯA CÓ du_lieu/btc_5m.csv"),
         "Quy ước: mốc cắt C = lúc KẾT THÚC live (giờ thật từ transcripts/gio_live.tsv; thiếu thì giờ không chắc). "
         "Bot chỉ thấy dữ liệu trước C; nhãn so sánh = view H4 (không có thì 'chung') CUỐI buổi của người đó. "
         "Mọi cách đoán chấm trên CÙNG tập buổi, cùng thước; chấm theo thị trường đều tính từ C (giá tham chiếu = close nến 5m "
         "cuối đã đóng ≤ C; nến 5m chứa C bị bỏ → khoảng trống < 5 phút sau C không chấm)."]
    so, loai = [], []
    for r in dong:
        if r["nguoi"] not in NHAN:
            loai.append((r["b"].ten, "phiếu người đó không có nhãn H4/chung hợp lệ"))
        else:
            so.append(r)
    N = len(so)
    co_bai = sum(r["co_bai"] for r in so)
    hop_le = sum(r["bot"] is not None for r in so)
    L.append(f"Tập so hướng (mẫu số khoá): **{N}/{len(thi)}** buổi thi có nhãn người đó hợp lệ · bị loại {len(loai)}"
             + (": " + "; ".join(f"{t} ({ly})" for t, ly in loai) if loai else "") + ".")
    L.append(f"Độ phủ bot trên {N} buổi: có bài làm **{co_bai}/{N}** · nhãn H4/chung hợp lệ **{hop_le}/{N}** — "
             "buổi thiếu bài hoặc nhãn không hợp lệ được TÍNH SAI (không loại khỏi mẫu số).")
    if not N:
        ra_file.write_text("\n".join(L) + "\n", encoding="utf-8"); print("Không có buổi so hướng được."); return

    # 1. trùng hướng + mốc so sánh
    pp = {"Bot": [r["bot"] for r in so]} | {m: [r["moc"][m] for r in so] for m in MOC_SO}
    ng = [r["nguoi"] for r in so]
    dung = {k: [int(x == y) for x, y in zip(v, ng)] for k, v in pp.items()}
    tl, hieu, so_khoi = boot_khoi(so, dung, list(pp))
    pb = Counter(pp["Bot"]); pn = Counter(ng)
    L += ["", f"## 1. Trùng hướng H4 với người đó (cùng {N} buổi, cùng mẫu số)",
          f"Người đó: TĂNG {pn['TANG']} · GIẢM {pn['GIAM']} · PHÂN VÂN {pn['PHAN_VAN']} — Bot: TĂNG {pb['TANG']} · GIẢM {pb['GIAM']} · "
          f"PHÂN VÂN {pb['PHAN_VAN']} · thiếu/không hợp lệ {pb[None]}",
          f"| Cách đoán | Thiếu nhãn (tính sai) | Độ chính xác 3 nhãn | KTC 95% (bootstrap khối {so_khoi} tuần ISO) | "
          "Chênh bot − cách này (KTC 95% cặp, khối tuần) | Macro-F1 | Balanced acc. | Khi cả 2 có hướng | Kappa | "
          "McNemar bot vs mốc (bot đúng–mốc sai / ngược lại, p) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in pp.items():
        ch = [(x, y) for x, y in zip(v, ng) if x in ("TANG", "GIAM") and y in ("TANG", "GIAM")]
        cs = chi_so(v, ng)
        if k == "Bot":
            mc = hc = "—"
        else:
            b_ = sum(1 for x, y in zip(dung["Bot"], dung[k]) if x and not y)
            c_ = sum(1 for x, y in zip(dung["Bot"], dung[k]) if y and not x)
            mc = f"{b_} / {c_}, p = {p_nhi_thuc(b_, b_ + c_):.3f}"
            d0 = (sum(dung["Bot"]) - sum(dung[k])) / N
            hc = f"{d0 * 100:+.0f} điểm % ({ktc(hieu[k], True)})"
        bacc = "—" if cs["bacc"] is None else f"{cs['bacc']:.2f}"
        kp = "—" if cs["kappa"] is None else f"{cs['kappa']:.2f}"
        L.append(f"| {k} | {sum(x is None for x in v)} | **{ty_le(sum(dung[k]), N)}** | {ktc(tl[k])} | {hc} | {cs['f1']:.2f} | {bacc} | "
                 f"{ty_le(sum(x == y for x, y in ch), len(ch))} | {kp} | {mc} |")
    L.append("_Chỉ số chính = độ chính xác 3 nhãn trên toàn tập. Kết luận bot hơn/kém một mốc chỉ khi KTC của CHÊNH LỆCH CẶP "
             "không chứa 0 — không so hai khoảng tỷ lệ riêng. Bootstrap khối tuần giữ phụ thuộc giữa các buổi cùng tuần "
             "(view kéo dài, nhiều phiên/ngày). Chép buổi trước = nguyên nhãn buổi liền trước; Giữ view = hướng TĂNG/GIẢM "
             "gần nhất của người đó (bỏ qua buổi PHÂN VÂN)._")
    L += ["", "### Bảng chéo (dòng = người đó, cột = bot)", "| | " + " | ".join(VIET[h] for h in NHAN) + " | Thiếu/không hợp lệ | Tổng |",
          "|---|---|---|---|---|---|"]
    for x in NHAN:
        hang = [sum(1 for r in so if r["nguoi"] == x and r["bot"] == y) for y in NHAN + [None]]
        L.append(f"| **{VIET[x]}** | " + " | ".join(map(str, hang)) + f" | {sum(hang)} |")
    L.append("| Tổng | " + " | ".join(str(sum(1 for r in so if r["bot"] == y)) for y in NHAN + [None]) + f" | {N} |")
    # theo nhóm
    L += ["", "### Theo nhóm buổi (độ chính xác 3 nhãn)", "| Nhóm | Số buổi | " + " | ".join(pp) + " |", "|---|---|" + "---|" * len(pp)]
    for nh_ in ("Live sáng (06–14h VN)", "Live tối/đêm", "Giờ live thật", "Giờ không chắc"):
        idx = [i for i, r in enumerate(so) if nh_ in nhom(r["b"])]
        if idx:
            L.append(f"| {nh_} | {len(idx)} | " + " | ".join(ty_le(sum(dung[k][i] for i in idx), len(idx)) for k in pp) + " |")

    # 2. PHÂN VÂN
    a_ = sum(1 for r in so if r["bot"] == "PHAN_VAN" and r["nguoi"] == "PHAN_VAN")
    b_ = sum(1 for r in so if r["bot"] == "PHAN_VAN" and r["nguoi"] != "PHAN_VAN")
    c_ = sum(1 for r in so if r["bot"] in ("TANG", "GIAM") and r["nguoi"] == "PHAN_VAN")
    d_ = sum(1 for r in so if r["bot"] is None and r["nguoi"] == "PHAN_VAN")
    L += ["", "## 2. PHÂN VÂN (chấm riêng)", "| Trường hợp | Số buổi |", "|---|---|",
          f"| Bot PHÂN VÂN khi người đó PHÂN VÂN (đúng) | {a_} |", f"| Bot PHÂN VÂN khi người đó có hướng (bỏ lỡ) | {b_} |",
          f"| Bot có hướng khi người đó PHÂN VÂN (ép hướng) | {c_} |", f"| Bot thiếu nhãn khi người đó PHÂN VÂN | {d_} |",
          f"| Độ chính xác khi bot nói PHÂN VÂN | {ty_le(a_, a_ + b_)} |", f"| Bắt được PHÂN VÂN của người đó | {ty_le(a_, a_ + c_ + d_)} |"]

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

    # 4. đúng/sai theo thị trường — mọi buổi thi, cùng mốc C
    ben = ["Bot", "Người đó", "Chép view buổi trước", "Giữ view"]
    L += ["", f"## 4. Đúng/sai theo thị trường (cd.cham_chi_tiet; râu chạm đích tính; SAI = chạm SL / vô hiệu đúng khung trước) — {len(dong)} buổi thi",
          "Bot thiếu bài = 'PHÂN VÂN/không view'. CHƯA RÕ THỨ TỰ = đích và SL cùng nến 1m (hoặc thiếu 1m) — không tính đúng, "
          "không vào mẫu số % đúng. 'Vô hiệu chưa hiểu' = có câu vô hiệu nhưng không tách được mốc → chỉ xét SL/đích.",
          "| Hạn | Bên | ĐÚNG | SAI (SL / vô hiệu) | SAI hết hạn (không mốc sai, không chạm đích) | CHƯA RÕ | CHƯA RÕ THỨ TỰ | Chưa hết hạn | "
          "Không đích | Đích sai phía | PHÂN VÂN/không view | Vô hiệu chưa hiểu | % đúng (đã ngã ngũ) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for han, ten_han in (("han_co_dinh", "14 ngày"), ("han_view", "tự nêu (≤14 ngày; không nêu = 7)")):
        for k in ben:
            c = Counter(r["tt"][k][han]["ket_qua"] for r in dong)
            sl_ = sum(1 for r in dong if r["tt"][k][han]["ket_qua"] == "SAI" and str(r["tt"][k][han].get("su_kien")).startswith("sl"))
            xong = c["DUNG"] + c["SAI"] + c["SAI_HET_HAN"]
            L.append(f"| {ten_han} | {k} | {c['DUNG']} | {c['SAI']} ({sl_} / {c['SAI'] - sl_}) | {c['SAI_HET_HAN']} | {c['CHUA_RO']} | "
                     f"{c['CHUA_RO_THU_TU']} | {c['CHUA_HET_HAN']} | {c['KHONG_DICH']} | {c['DICH_SAI_PHIA']} | "
                     f"{c['PHAN_VAN'] + c['KHONG_VIEW'] + c['CHUA_DU_LIEU']} | {sum(r['tt'][k]['vo_hieu_chua_hieu'] for r in dong)} | "
                     f"{ty_le(c['DUNG'], xong)} |")
    L.append("_Chép view buổi trước / Giữ view = nguyên view H4 (đích, vô hiệu, lệnh) của buổi đó, chấm lại từ C của buổi thi "
             "(hạn tự nêu = hạn của view gốc). Luôn GIẢM và Luật từ trên xuống không có đích → không chấm được theo thước này._")
    # 4b. đúng đường đi
    L += ["", "### 4b. View nhiều chặng: đúng đích cuối vs đúng ĐƯỜNG ĐI (hạn 14 ngày)",
          "Đúng đường đi = chạm đích chặng 1 rồi mới tới đích cuối (lần lượt từng chặng), trước SL/vô hiệu. "
          "SAI_THU_TU = tới đích cuối khi chưa qua chặng trước.",
          "| Bên | View nhiều chặng chấm được | Đúng đích cuối (kết quả chính) | ĐÚNG đường đi | SAI | SAI thứ tự | CHƯA RÕ THỨ TỰ | Chưa rõ / hết hạn / chưa hết hạn |",
          "|---|---|---|---|---|---|---|---|"]
    for k in ben:
        ds = [r["tt"][k] for r in dong if r["tt"][k].get("ket_qua_duong_di")]
        c = Counter(x["ket_qua_duong_di"] for x in ds)
        L.append(f"| {k} | {len(ds)} | {sum(x['ket_qua'] == 'DUNG' for x in ds)} | {c['DUNG']} | {c['SAI']} | {c['SAI_THU_TU']} | "
                 f"{c['CHUA_RO_THU_TU']} | {c['CHUA_RO'] + c['SAI_HET_HAN'] + c['CHUA_HET_HAN']} |")

    # 5. đối xứng thật
    def bang_dx(chon, tieu_de):
        out = [tieu_de, "| Bên | View có đích | Chiều chọn tới trước | Phía kia tới trước | Cùng nến (1m không phân được) | "
               "Chưa ngã ngũ (14 ngày) | Chưa hết hạn | % thắng | p (nhị thức, vs 50%) |", "|---|---|---|---|---|---|---|---|---|"]
        for k in ben:
            c = Counter(r["dx"][k] for r in dong if r["dx"][k] and chon(r["tt"][k]))
            t, th = c["THANG"], c["THUA"]
            out.append(f"| {k} | {sum(c.values())} | {t} | {th} | {c['CUNG_NEN']} | {c['CHUA_NGA_NGU']} | {c['CHUA_HET_HAN']} | "
                       f"{ty_le(t, t + th)} | {p_nhi_thuc(t, t + th):.3f} |")
        return out
    L += ["", "## 5. Phép thử đối xứng THẬT (mốc phía kia cách giá tham chiếu đúng bằng khoảng tới đích; 50% = không hơn tung đồng xu)"]
    L += bang_dx(lambda x: not x.get("di_nguoc"), "### View không có chặng đi ngược (1 chặng hoặc mọi chặng cùng hướng) — phép thử chính")
    L += [""] + bang_dx(lambda x: x.get("di_nguoc"), "### View có chặng cố ý ĐI NGƯỢC (vd hồi lên rồi giảm) — báo riêng, KHÔNG gộp vào phép thử chính")
    L.append("_View có chặng đi ngược cố ý chạm phía kia trước nên biên đối xứng quanh giá phạt họ; bản cũ nới biên phía kia tới "
             "đích chặng 1 làm hai biên không còn đối xứng (bước ngẫu nhiên không lệch cũng > 50%) nên đã bỏ cách nới đó. "
             "Bảng riêng chỉ để tham khảo, không đọc như phép so với tung đồng xu._")

    # 6. độ lệch đích / mốc sai
    def lech(k):
        xs = [abs(r["tt"]["Bot"][k] - r["tt"]["Người đó"][k]) / r["tt"]["Người đó"][k] * 100 for r in dong
              if r["tt"]["Người đó"].get("huong") in ("TANG", "GIAM") and r["tt"]["Người đó"].get("huong") == r["tt"]["Bot"].get("huong")
              and r["tt"]["Người đó"].get(k) and r["tt"]["Bot"].get(k)
              and "DICH_SAI_PHIA" not in (r["tt"]["Người đó"]["ket_qua"], r["tt"]["Bot"]["ket_qua"])]
        if not xs:
            return "—", 0
        s = sorted(xs)
        return f"TB {sum(xs) / len(xs):.2f}% · trung vị {s[len(s) // 2]:.2f}% · ≤1%: {sum(x <= 1 for x in xs)}/{len(xs)}", len(xs)
    L += ["", "## 6. Độ lệch số bot vs người đó (khi cùng hướng và đều có số; đích/mốc sai tách như cd.cham_chi_tiet)",
          "| Thứ | Số buổi | Lệch |", "|---|---|---|"]
    for k, ten in (("dich", "Đích"), ("moc_sai", "Mốc sai (vô hiệu)")):
        s, n = lech(k)
        L.append(f"| {ten} | {n} | {s} |")

    # 7. từng buổi
    L += ["", "## 7. Từng buổi (* = giờ live không chắc; ∅ = không có bài làm)",
          "| Buổi | C (VN) | Người | Bot | Trùng | Luật | Giữ view | Chép | Thị trường 14 ngày: người / bot | Hạn tự nêu: người / bot | "
          "Đường đi: người / bot | Đối xứng: người / bot | Đích N / B | Mốc sai N / B |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    so_ = lambda v, k: hs.g(v[k]) if v.get(k) else "—"
    for r in dong:
        n_, b_ = r["tt"]["Người đó"], r["tt"]["Bot"]
        L.append(f"| {r['b'].ten}{'' if r['b'].chac else ' *'}{'' if r['co_bai'] else ' ∅'} | {hs.vn(r['b'].C, '%m-%d %H:%M')} | "
                 f"{VIET[r['nguoi']]} | {VIET[r['bot']]} | "
                 f"{'✓' if r['nguoi'] and r['nguoi'] == r['bot'] else ('—' if not r['nguoi'] else '✗')} | "
                 f"{VIET[r['moc']['Luật từ trên xuống']]} | {VIET[r['moc']['Giữ view']]} | {VIET[r['moc']['Chép buổi trước']]} | "
                 f"{n_['ket_qua']} / {b_['ket_qua']} | {n_['han_view']['ket_qua']} / {b_['han_view']['ket_qua']} | "
                 f"{n_.get('ket_qua_duong_di') or '—'} / {b_.get('ket_qua_duong_di') or '—'} | "
                 f"{r['dx']['Người đó'] or '—'} / {r['dx']['Bot'] or '—'} | "
                 f"{so_(n_, 'dich')} / {so_(b_, 'dich')} | {so_(n_, 'moc_sai')} / {so_(b_, 'moc_sai')} |")
    if loai:
        L += ["", f"## Buổi bị loại khỏi phần so hướng ({len(loai)})"] + [f"- {t}: {ly}" for t, ly in loai]
    ra_file.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✓ {len(dong)} buổi chấm, {N} buổi so hướng (bot có nhãn hợp lệ {hop_le}) → {ra_file}")
    print("  độ chính xác 3 nhãn: " + " · ".join(f"{k}: {ty_le(sum(dung[k]), N)}" for k in pp))


if __name__ == "__main__":
    main()
