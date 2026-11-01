#!/usr/bin/env python3
"""Kiểm hành vi bộ chấm v5 + kế hoạch có cấu trúc + view trước T (offline, không gọi mạng).
  (1) Thứ tự thời gian của LỆNH: TP trước khi khớp không tính thắng · chưa khớp · huỷ trước khi vào · chưa ngã ngũ
      (kèm mốc dữ liệu cuối) · khớp tại giá mở · khớp rồi SL cùng nến (tính liên tục).
  (2) Cùng nến chạm TP và SL: không có nến nhỏ → KHÔNG RÕ (dù hình dạng OHLC nghiêng phía nào); có 15m → đúng thứ tự;
      15m lủng 1 cây → coi như không có; chung 1 cây 15m nhỏ nhất → KHÔNG RÕ.
  (3) SL chạm giá ≠ mốc đóng lệnh theo nến ĐÓNG: râu qua mốc không tính; đúng khung (4H ≠ 1D); đủ số cây LIÊN TIẾP.
  (4) Hạn là cột riêng: TP sau hạn vẫn là TP, cột hạn ghi TRỄ HẠN.
  (5) Lệnh user: thiếu chiều / giờ → từ chối; thiếu giá → ghi THIẾU, không tính %; vào lúc nến đã chạm TP → PHỤ THUỘC GIÁ.
  (6) Kiểm kế hoạch: thứ tự giá, đúng khung mốc sai, ghép đích/mốc khác view phải giải thích, lệnh ngược view, đếm họ
      căn cứ, giờ phát hành.
  (7) Khoá + mục lục: ghi được 1 lần, từ chối ghi lại, phát hiện sửa sau khoá; `--ghi` không đè kết quả cũ.
  (8) View trước T: không có → KHỞI TẠO; phát hành sau T không dùng (kể cả gio_cat < T); dữ liệu sau T bị đầu độc →
      văn bản giống hệt; file bị sửa → bỏ qua; quá cũ → khởi tạo; Gia không bao giờ trả nến đóng sau den.
  (10) Chờ xác nhận nến đóng · nhiều nấc TP · trực tiếp phát hành giữa nến · mốc bắt đầu hồi cứu/trực tiếp.
  (9) Hồi quy OKB 21/09 (dữ liệu thật trong bot_v5/kiem_tra_cham/du_lieu/): TP 21/09 trước khi về vùng chờ mua 28/09
      → kế hoạch chờ và lệnh user vào ngay được chấm thành 2 trường hợp riêng; đường đi sai thứ tự; trễ hạn.
Dùng: python3 bot_v5/kiem_tra_cham.py   (exit 1 nếu có FAIL)
"""
import contextlib, io, json, sys, tempfile
from pathlib import Path

DAY = Path(__file__).resolve().parent
sys.path.insert(0, str(DAY))
import nen as NG  # noqa: E402
import ke_hoach as KH  # noqa: E402
import cham_ke_hoach as CH  # noqa: E402

LOI = []
T0 = KH.doc_gio("2027-01-04 07:00")  # thứ Hai 00:00 UTC — căn đủ 1H / 4H / 1D / 1W
H = 3600
FIX = DAY / "kiem_tra_cham"


def cli(args):
    """Chạy CLI bộ chấm, nuốt stdout (chỉ lấy mã thoát)."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return CH.main(args)


def kiem(dk, ten):
    print(("PASS " if dk else "FAIL ") + ten)
    if not dk:
        LOI.append(ten)


# ---------------- dữ liệu giả ----------------
def nen_1h(dong, t0=T0, sua=None):
    """dong = giá đóng từng giờ (giá mở = đóng giờ trước, cây đầu mở = đóng đầu); sua = {i: (o, h, l, c)}."""
    ra, truoc = [], dong[0]
    for i, c in enumerate(dong):
        o = truoc
        h, l = max(o, c) + 0.1, min(o, c) - 0.1
        if sua and i in sua:
            o, h, l, c = sua[i]
        ra.append(NG.NenGia(t0 + i * H, t0 + (i + 1) * H, o, h, l, c, 1.0, ""))
        truoc = c
    return ra


def gop(ds, giay):
    nhom = {}
    for n in ds:
        nhom.setdefault(n.mo - (n.mo - T0) % giay, []).append(n)
    return [NG.NenGia(k, k + giay, v[0].o, max(x.h for x in v), min(x.l for x in v), v[-1].c, 1.0, "")
            for k, v in sorted(nhom.items()) if len(v) == giay // H]


def nap(ds, them=None):
    d = {"1H": ds, "4H": gop(ds, 4 * H), "1D": gop(ds, 24 * H)}
    d.update(them or {})
    return d


def gia(ds, them=None, den=None):
    return CH.Gia("TST", T0, den or ds[-1].dong, nap=nap(ds, them))


def lenh(**k):
    L = {"chieu": "LONG", "kieu_vao": "vung", "vung_vao": (95.0, 96.0), "muc_vao": 96.0, "phia_vao": "duoi",
         "tp": [110.0], "tp_vung": [(110.0, 111.0)], "ty_le": [None], "sl": None, "dong_khi": [], "huy_cham": [],
         "huy_dong": [], "het_han_cho": None, "han": T0 + 1000 * H, "kiem_may": False, "gia_dinh": []}
    L.update(k)
    return L


def chay(g, L, bd=T0):
    return CH.May(g, L, bd).chay().ket_qua()


# ---------------- (1) thứ tự thời gian của lệnh ----------------
def kiem_1():
    ds = nen_1h([100, 104, 108, 111, 106, 100, 95.5, 99, 104, 110.5, 108])
    r = chay(gia(ds), lenh())
    kiem(r["tp_truoc"] is not None and r["tp_truoc"].a == T0 + 3 * H, "(1a) TP chạm trước khi khớp được ghi đúng nến")
    kiem(r["A"][0] == "VAO" and r["A"][1].a == T0 + 6 * H, "(1a) khớp (chạm vùng) ở nến về vùng, sau TP")
    kiem(r["B"][0] == "TP" and r["B"][1].a == T0 + 9 * H, "(1a) TP sau khi khớp là lần chạm SAU entry, không phải lần trước")
    txt = "\n".join(CH.dong_lenh(lenh(), r, T0))
    kiem("KHÔNG tính thắng" in txt and "GIÁ CHẠM VÙNG" in txt and "chưa khẳng định lệnh khớp hợp lệ" in txt,
         "(1a) báo cáo: TP trước entry không tính thắng; chỉ nói 'giá chạm vùng' khi chưa kiểm điều kiện khung nhỏ")
    r = chay(gia(ds), lenh(huy_khi_tp_truoc=True))
    kiem(r["A"][0] == "DA_HUY" and r["A"][1][1].a == T0 + 3 * H, "(1b) kế hoạch ghi huỷ khi TP trước → ĐÃ HUỶ, không khớp")
    ds2 = nen_1h([100, 102, 104, 103, 101, 100])
    r = chay(gia(ds2), lenh())
    txt = "\n".join(CH.dong_lenh(lenh(), r, T0))
    kiem(r["A"][0] == "CHUA_KHOP" and KH.gio_vn(ds2[-1].dong) in txt, "(1c) chưa chạm vùng → CHƯA KHỚP + mốc dữ liệu cuối")
    ds3 = nen_1h([100, 102, 104, 106, 103, 100, 95.5, 99])  # 4H đóng 106 (> 105) lúc T0+4h, rồi mới về vùng
    r = chay(gia(ds3), lenh(huy_dong=[{"khung": "4H", "phia": "tren", "gia": 105.0, "so_nen": 1}]))
    kiem(r["A"][0] == "DA_HUY" and r["A"][1][1].a == T0 + 4 * H, "(1d) điều kiện huỷ (nến 4H đóng) trước khi khớp → ĐÃ HUỶ")
    r = chay(gia(ds3), lenh(huy_cham=[("tren", 105.5)]))
    kiem(r["A"][0] == "DA_HUY", "(1d) điều kiện huỷ chạm giá trước khi khớp → ĐÃ HUỶ")
    ds4 = nen_1h([100, 101, 99, 103, 98, 102])
    r = chay(gia(ds4), lenh(kieu_vao="ngay", gia_vao=100.0, dong_khi=[{"khung": "1D", "phia": "duoi", "gia": 90.0}]))
    txt = "\n".join(CH.dong_lenh(lenh(kieu_vao="ngay"), r, T0))
    kiem(r["B"][0] == "CHUA_NGA_NGU" and "CHƯA NGÃ NGŨ" in txt and KH.gio_vn(ds4[-1].dong) in txt,
         "(1e) đã vào, chưa chạm gì → CHƯA NGÃ NGŨ + mốc dữ liệu cuối")
    ds5 = nen_1h([95.5, 99, 104, 110.5])
    r = chay(gia(ds5), lenh())
    kiem(r["A"][1].a == r["A"][1].b == T0 and r["gia_vao"] == 95.5 and any("giá mở" in x for x in r["gia_dinh"]),
         "(1f) giá mở đã trong vùng → khớp tại giá mở, có ghi giả định")
    ds6 = nen_1h([100, 100, 92, 95], sua={2: (100, 100.5, 89, 92)})
    r = chay(gia(ds6), lenh(sl=90.0))
    kiem(r["A"][0] == "VAO" and r["B"][0] == "SL" and r["B"][1].a == T0 + 2 * H and "liên tục" in r["B"][2],
         "(1g) cùng nến chạm vùng vào rồi SL (giá mở trên vùng) → vào rồi SL, ghi rõ là tính liên tục")
    ds7 = nen_1h([100, 100, 105, 104], sua={2: (100, 111, 95.5, 105)})
    r = chay(gia(ds7), lenh())
    kiem(r["A"][0] == "KHONG_RO", "(1h) cùng nến chạm vùng vào và TP, không có nến nhỏ → KHÔNG RÕ thứ tự khớp")


# ---------------- (2) cùng nến TP + SL ----------------
def _15m(t, ohlc):
    return [NG.NenGia(t + i * 900, t + (i + 1) * 900, *x, 1.0, "") for i, x in enumerate(ohlc)]


def kiem_2():
    L = lenh(kieu_vao="ngay", gia_vao=100.0, sl=90.0)
    for ten, x in (("đóng sát đỉnh", (100, 111, 89, 110.9)), ("đóng sát đáy", (100, 111, 89, 89.1))):
        ds = nen_1h([100, 100, 100, 100], sua={2: x})
        r = chay(gia(ds), L)
        kiem(r["B"][0] == "KHONG_RO", f"(2a) cùng nến TP+SL, không có 15m, nến {ten} → KHÔNG RÕ (không suy từ OHLC)")
    ds = nen_1h([100, 100, 100, 100], sua={2: (100, 111, 89, 105)})
    sl_truoc = _15m(T0 + 2 * H, [(100, 101, 89.5, 95), (95, 104, 94, 103), (103, 111, 102, 108), (108, 109, 104, 105)])
    r = chay(gia(ds, {"15m": sl_truoc}), L)
    kiem(r["B"][0] == "SL" and r["B"][1].khung == "15m" and r["B"][1].a == T0 + 2 * H,
         "(2b) có 15m: SL ở cây 15m đầu → SL trước")
    tp_truoc = _15m(T0 + 2 * H, [(100, 104, 99, 103), (103, 111, 102, 108), (108, 109, 89, 95), (95, 106, 94, 105)])
    r = chay(gia(ds, {"15m": tp_truoc}), L)
    kiem(r["B"][0] == "TP" and r["B"][1].a == T0 + 2 * H + 900, "(2c) có 15m: TP ở cây 15m thứ 2 → TP trước")
    r = chay(gia(ds, {"15m": tp_truoc[:3]}), L)
    kiem(r["B"][0] == "KHONG_RO", "(2d) 15m thiếu 1 cây → không dùng dữ liệu lủng → KHÔNG RÕ")
    cung = _15m(T0 + 2 * H, [(100, 111, 89, 105), (105, 106, 104, 105), (105, 106, 104, 105), (105, 106, 104, 105)])
    r = chay(gia(ds, {"15m": cung}), L)
    kiem(r["B"][0] == "KHONG_RO", "(2e) chung 1 cây 15m, không có 5m → KHÔNG RÕ")
    m5 = [NG.NenGia(T0 + 2 * H + i * 300, T0 + 2 * H + (i + 1) * 300, *x, 1.0, "")
          for i, x in enumerate([(100, 101, 89, 95), (95, 111, 94, 105), (105, 106, 104, 105)])]
    r = chay(gia(ds, {"15m": cung, "5m": m5}), L)
    kiem(r["B"][0] == "SL" and r["B"][1].khung == "5m", "(2f) chung cây 15m → xét 5m: SL trước")


# ---------------- (3) SL chạm giá vs mốc đóng theo nến đóng ----------------
def kiem_3():
    dong = [95] * 7 + [89] + [95] * 16  # 4H (04–08 UTC) đóng 89; D1 đóng 95
    ds = nen_1h(dong, sua={10: (95, 95.5, 85, 95)})  # râu xuống 85 nhưng đóng 95
    base = dict(kieu_vao="ngay", gia_vao=100.0)
    r = chay(gia(ds), lenh(**base, dong_khi=[{"khung": "1D", "phia": "duoi", "gia": 90.0, "so_nen": 1}]))
    kiem(r["B"][0] == "CHUA_NGA_NGU", "(3a) mốc 1D: nến 4H đóng dưới + râu xuyên mốc nhưng D1 đóng trên → KHÔNG đóng lệnh")
    r = chay(gia(ds), lenh(**base, dong_khi=[{"khung": "4H", "phia": "duoi", "gia": 90.0, "so_nen": 1}]))
    kiem(r["B"][0] == "DONG" and r["B"][1].a == T0 + 8 * H, "(3b) mốc 4H: đóng lệnh đúng lúc nến 4H ĐÓNG (08:00 UTC)")
    r = chay(gia(ds), lenh(**base, sl=88.0, dong_khi=[{"khung": "1D", "phia": "duoi", "gia": 90.0}]))
    kiem(r["B"][0] == "SL" and r["B"][1].a == T0 + 10 * H, "(3c) SL chạm giá 88: râu 85 → SL, khác mốc nến đóng")
    # 2 cây liên tiếp: 4H đóng dưới, trên, dưới, dưới → kích hoạt ở cây thứ 4
    d2 = [95, 95, 95, 89, 95, 95, 95, 95, 95, 95, 95, 89, 95, 95, 95, 89, 95]
    ds = nen_1h(d2)
    r = chay(gia(ds), lenh(**base, dong_khi=[{"khung": "4H", "phia": "duoi", "gia": 90.0, "so_nen": 2}]))
    kiem(r["B"][0] == "DONG" and r["B"][1].a == T0 + 16 * H, "(3d) so_nen = 2: chỉ tính 2 cây 4H ĐÓNG LIÊN TIẾP")


# ---------------- (4) hạn là cột riêng ----------------
def kiem_4():
    ds = nen_1h([100, 102, 104, 106, 108, 110.5, 109])
    L = lenh(kieu_vao="ngay", gia_vao=100.0, han=T0 + 3 * H)
    r = chay(gia(ds), L)
    txt = "\n".join(CH.dong_lenh(L, r, T0))
    kiem(r["B"][0] == "TP" and "TRỄ HẠN" in txt and "TP trước" in txt, "(4) TP sau hạn vẫn là TP; cột hạn ghi TRỄ HẠN")


# ---------------- (5) lệnh user (CLI) ----------------
def kiem_5():
    kh = FIX / "okb_2026-09-21.json"
    co = ["--den", "2026-11-01 07:00", "--offline", "--cache", str(FIX / "du_lieu")]
    kiem(cli([str(kh), *co, "--vao-luc", "2026-09-21 11:00"]) == 2, "(5a) thiếu chiều lệnh → từ chối, không đoán")
    kiem(cli([str(kh), *co, "--lenh-user", "LONG", "--theo", "long_cho"]) == 2, "(5b) thiếu giờ vào → từ chối")
    kiem(cli([str(kh), *co, "--lenh-user", "SHORT", "--theo", "long_cho", "--vao-luc", "2026-09-21 11:00"]) == 2,
         "(5c) chiều user ngược kế hoạch được dẫn → từ chối dùng chung TP/mốc")


# ---------------- (6) kiểm kế hoạch ----------------
def _mau():
    return json.loads((FIX / "okb_2026-09-21.json").read_text(encoding="utf-8"))


def kiem_6():
    loi, cb, tt = KH.kiem(_mau())
    kiem(not loi, "(6a) kế hoạch OKB chuyển từ đối chiếu cũ hợp lệ")
    kiem(any("5 căn cứ / 4 họ" in x for x in tt), "(6a) báo số căn cứ theo họ chỉ báo")
    k = _mau()
    k["ke_hoach"][0]["tp"] = [{"vung": [110.0, 112.0]}]
    kiem(any("TP" in x and "không cao hơn" in x for x in KH.kiem(k)[0]), "(6b) LONG mà TP dưới vùng vào → LỖI")
    k = _mau()
    k["ke_hoach"][0]["dong_khi"] = [{"khung": "4H", "phia": "duoi", "gia": 114.4, "so_nen": 1}]
    kiem(any("ghi_chu_ghep" in x for x in KH.kiem(k)[0]), "(6c) mốc đóng lấy từ view H4 cho kế hoạch thuộc D1, không giải thích → LỖI")
    k["ke_hoach"][0]["ghi_chu_ghep"] = "đóng sớm theo H4 vì lệnh lướt"
    kiem(not KH.kiem(k)[0], "(6c) có giải thích ghép → hợp lệ")
    k = _mau()
    k["view"]["H4"]["sai_khi"]["khung"] = "1D"
    kiem(any("view khung này phải sai theo nến 4H" in x for x in KH.kiem(k)[0]), "(6d) mốc sai view H4 phải là nến 4H đóng")
    k = _mau()
    k["ke_hoach"][0].update(chieu="SHORT", vao={"vung": [123.5, 124.0]}, tp=[{"vung": [116.0, 116.8]}],
                            dong_khi=[{"khung": "1D", "phia": "tren", "gia": 126.0, "so_nen": 1}], ghi_chu_ghep="x")
    kiem(any("luot: true" in x for x in KH.kiem(k)[0]), "(6e) SHORT ngược view D1 TĂNG không đánh dấu lướt → LỖI")
    k = _mau()
    k["ke_hoach"][0]["can_cu"] = [{"ten": f"Fibo {i}", "ho": "FIBO", "khung": "4H"} for i in range(3)] + [
        {"ten": "EMA34", "ho": "EMA", "khung": "4H"}]
    kiem(any("đếm trùng" in x for x in KH.kiem(k)[1]), "(6f) 4 căn cứ nhưng 2 họ → cảnh báo hội tụ đếm trùng")
    k = _mau()
    k["gio_phat_hanh"] = "2026-09-21 10:00"
    kiem(any("gio_phat_hanh < gio_cat" in x for x in KH.kiem(k)[0]), "(6g) phát hành trước gio_cat → LỖI")
    k = _mau()
    k["view"]["D1"]["sai_khi"]["gia"] = 121.0
    kiem(any("sai phía" in x for x in KH.kiem(k)[0]), "(6h) mốc sai đã bị vượt ngay tại T → LỖI")


# ---------------- (7) khoá + mục lục + ghi kết quả ----------------
def kiem_7():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        p = td / "2026-09-21_OKB.json"
        p.write_text(json.dumps(_mau(), ensure_ascii=False), encoding="utf-8")
        ok, msg = KH.luu(p, td, sha_ho_so=False)
        kh = json.loads(p.read_text(encoding="utf-8"))
        kiem(ok and kh["khoa"]["che_do"] == "hoi_cuu" and len(KH.doc_muc_luc(td)) == 1
             and "bot_v5/NHAP_VAI.md" in kh["khoa"]["sha256"], "(7a) khoá: ghi git + sha256 luật, chế độ hồi cứu, mục lục")
        ok2, msg2 = KH.luu(p, td, sha_ho_so=False)
        kiem(not ok2 and "đã khoá" in msg2, "(7b) khoá lần 2 → từ chối")
        kiem(KH.kiem_khoa(p, td)[0], "(7c) file chưa sửa → đúng sha")
        p.write_text(p.read_text(encoding="utf-8").replace("120.19", "120.2"), encoding="utf-8")
        kiem(not KH.kiem_khoa(p, td)[0] and "SỬA" in KH.kiem_khoa(p, td)[1], "(7d) sửa sau khoá → phát hiện")
        q = td / "khac.json"
        q.write_text(json.dumps(_mau(), ensure_ascii=False), encoding="utf-8")
        kiem(not KH.luu(q, td, sha_ho_so=False)[0], "(7e) tên file khác stem file đối chiếu → từ chối")
        cu = CH.KET_QUA
        CH.KET_QUA = td / "ket_qua"
        try:
            a = [str(FIX / "okb_2026-09-21.json"), "--den", "2026-11-01 07:00", "--offline", "--cache",
                 str(FIX / "du_lieu"), "--ghi"]
            cli(a)
            f = list((td / "ket_qua").glob("*.md"))
            noi = f[0].read_text(encoding="utf-8") if f else ""
            cli(a)
            kiem(len(f) == 1 and "Phân loại lỗi" in noi and f[0].read_text(encoding="utf-8") == noi
                 and (FIX / "okb_2026-09-21.json").read_text(encoding="utf-8").count('"khoa": null') == 1,
                 "(7f) --ghi: file kết quả riêng, có mục phân loại lỗi, chạy lại không đè, không đụng file kế hoạch")
        finally:
            CH.KET_QUA = cu


# ---------------- (8) view trước T ----------------
def _kh_tst(gio_cat, gio_ph):
    k = _mau()
    k.update(ma="TST", gio_cat=KH.gio_vn(gio_cat), gio_phat_hanh=KH.gio_vn(gio_ph), gio_live=KH.gio_vn(gio_ph),
             gia_dong=100.0, tep_doi_chieu=f"bot_v5/doi_chieu/{KH.gio_vn(gio_cat)[:10]}_TST_{gio_ph}.md")
    k["view"] = {kv: {"huong": "TANG", "nhan": "TĂNG", "do_chac": "vua", "dich": [110.0, 111.0],
                      "han": KH.gio_vn(gio_cat + 72 * H),
                      "sai_khi": {"khung": kd, "phia": "duoi", "gia": 90.0, "so_nen": 1}}
                 for kv, kd in KH.KHUNG_VIEW.items()}
    k["duong_di"] = [{"chang": 1, "vung": [95.0, 96.0]}, {"chang": 2, "vung": [110.0, 111.0]}]
    k["ke_hoach"] = [{"id": "long_cho", "khung_view": "D1", "hanh_dong": "CHO_VUNG", "chieu": "LONG",
                      "vao": {"vung": [95.0, 96.0]}, "xac_nhan": {"mo_ta": "", "kiem_may": False},
                      "tp": [{"vung": [110.0, 111.0]}], "dong_khi": [{"khung": "1D", "phia": "duoi", "gia": 90.0}],
                      "han": KH.gio_vn(gio_cat + 72 * H), "can_cu": []}]
    return k


def _luu_tst(td, k):
    p = td / (Path(k["tep_doi_chieu"]).stem + ".json")
    p.write_text(json.dumps(k, ensure_ascii=False), encoding="utf-8")
    ok, msg = KH.luu(p, td, sha_ho_so=False)
    assert ok, msg
    return p


def kiem_8():
    that = nen_1h([100, 99, 98, 97, 95.5, 99, 102, 104, 106, 103] + [104] * 40)
    T = T0 + 30 * H
    doc = [n if n.dong <= T else n._replace(o=n.o * 1.37, h=n.h * 1.37 + 50, l=n.l * 0.5, c=n.c * 1.37) for n in that]
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        txt, p = KH.truoc("TST", T, td, gia=CH.Gia("TST", T0 - 7 * 86400, T, nap=nap(that)))
        kiem(p is None and "KHỞI TẠO VIEW" in txt, "(8a) chưa có kế hoạch nào → KHỞI TẠO VIEW, không nói như đã biết view")
        _luu_tst(td, _kh_tst(T0, T + 5 * H))  # hồi cứu kiểu: gio_cat < T nhưng phát hành SAU T
        txt, p = KH.truoc("TST", T, td, gia=CH.Gia("TST", T0 - 7 * 86400, T, nap=nap(that)))
        kiem(p is None and "KHỞI TẠO VIEW" in txt, "(8b) kế hoạch phát hành sau T (dù gio_cat < T) → KHÔNG dùng làm lịch sử")
        p1 = _luu_tst(td, _kh_tst(T0, T0 + 600))  # phát hành trước T
        a, pa = KH.truoc("TST", T, td, gia=CH.Gia("TST", T0 - 7 * 86400, T, nap=nap(that)))
        b, pb = KH.truoc("TST", T, td, gia=CH.Gia("TST", T0 - 7 * 86400, T, nap=nap(doc)))
        kiem(pa == p1 and a == b, "(8c) dùng kế hoạch phát hành trước T; đầu độc mọi nến sau T → văn bản GIỐNG HỆT")
        kiem("đã chạm vùng/vào" in a and "ĐANG CÓ LỆNH" in a, "(8c) trạng thái tới T: kế hoạch chờ đã chạm vùng, đang có lệnh")
        try:
            KH.truoc("TST", T, td, gia=CH.Gia("TST", T0 - 7 * 86400, T + 5 * H, nap=nap(that)))
            kiem(False, "(8d) nguồn giá có dữ liệu sau T → phải từ chối")
        except ValueError:
            kiem(True, "(8d) nguồn giá có dữ liệu sau T → từ chối")
        p1.write_text(p1.read_text(encoding="utf-8").replace('"vua"', '"cao"'), encoding="utf-8")
        txt, p = KH.truoc("TST", T, td, gia=CH.Gia("TST", T0 - 7 * 86400, T, nap=nap(that)))
        kiem(p is None and "bị sửa" in txt, "(8e) kế hoạch bị sửa sau khoá → bỏ qua, có cảnh báo")
        _luu_tst(td, _kh_tst(T0 - 10 * 86400, T0 - 10 * 86400 + 600))
        g = CH.Gia("TST", T0 - 20 * 86400, T, nap=nap(that))
        txt, p = KH.truoc("TST", T, td, gia=g)
        kiem(p is not None and "QUÁ CŨ" in txt and '"KHOI_TAO"' in txt, "(8f) kế hoạch quá cũ → coi như khởi tạo")
    g = CH.Gia("TST", T0, T, nap=nap(that))
    kiem(all(n.dong <= T for k in ("1H", "4H", "1D") for n in g.nen(k)), "(8g) Gia không trả nến nào đóng sau den")


# ---------------- (9) hồi quy OKB 21/09 ----------------
def kiem_9():
    kh = _mau()
    g = CH.Gia("OKB", CH.bat_dau_cua(kh) - 7 * 86400, KH.doc_gio("2026-11-01 07:00"), FIX / "du_lieu", offline=True)
    kiem(g.goc == "1H" and g.du_lieu_toi() == KH.doc_gio("2026-11-01 07:00"), "(9a) dữ liệu OKB offline đủ, nến gốc 1H")
    L = CH.lenh_tu_ke_hoach(kh, kh["ke_hoach"][0])
    r = chay(g, L, CH.bat_dau_cua(kh))
    kiem(r["tp_truoc"] is not None and KH.gio_vn(r["tp_truoc"].a) == "2026-09-21 18:00",
         "(9b) kế hoạch chờ mua: TP 123.0 chạm 21/09 18:00 VN TRƯỚC khi về vùng → không tính thắng")
    kiem(r["A"][0] == "VAO" and KH.gio_vn(r["A"][1].a)[:10] == "2026-09-28",
         "(9c) giá chỉ chạm vùng chờ mua 115.8–116.8 ngày 28/09")
    kiem(r["B"][0] == "TP" and KH.gio_vn(r["B"][1].a)[:10] == "2026-10-05", "(9d) sau khi chạm vùng 28/09: TP chạm 05/10")
    txt = "\n".join(CH.dong_lenh(L, r, CH.bat_dau_cua(kh)))
    kiem("TRỄ HẠN" in txt and "chưa khẳng định lệnh khớp hợp lệ" in txt, "(9e) cột hạn: TRỄ HẠN; vào chỉ là 'giá chạm vùng'")
    U = dict(L, kieu_vao="ngay", gia_vao=None, gia_dinh=[])
    t_user = KH.doc_gio("2026-09-21 11:00")
    ru = chay(g, dict(U, gio_vao=t_user), t_user)
    kiem(ru["A"][1].a == t_user and ru["B"][0] == "TP" and KH.gio_vn(ru["B"][1].a) == "2026-09-21 18:00",
         "(9f) lệnh user vào 21/09 11:00: xét từ đúng lúc đó (không đổi thành lệnh chờ 28/09) → TP 21/09 18:00 trước")
    cu = "\n".join(CH.cham_user(g, U, [t_user], "2026-09-21 11:00"))
    kiem("THIẾU giá vào" in cu and "(+" not in cu and "(-" not in cu,
         "(9g) thiếu giá vào → ghi THIẾU, không tính % lãi/lỗ")
    t_ngay = KH.doc_gio("2026-09-21")
    cn = "\n".join(CH.cham_user(g, U, list(range(t_ngay, t_ngay + 86400, H)), "ngày 2026-09-21"))
    kiem("vào 21/09 00:00 → 21/09 17:00: **TP trước**" in cn and "PHỤ THUỘC GIÁ VÀO" in cn,
         "(9h) chỉ biết ngày 21/09: vào trước 18:00 → TP trước; vào khi nến đã chạm TP → PHỤ THUỘC GIÁ VÀO")
    bc = CH.bao_cao(kh, g, "okb")
    kiem("SAI THỨ TỰ — chặng 2 tới trước chặng 1" in bc and "ĐÚNG hướng/đích nhưng SAI THỨ TỰ" in bc,
         "(9i) dự báo: đúng đích nhưng sai thứ tự đường đi (chặng 2 trước chặng 1)")
    kiem("| H4 | TĂNG | [123.0, 124.2] | nến 4H ĐÓNG dưới 114.4 | ĐÍCH TRƯỚC" in bc
         and "| W1 | TĂNG | [129.1, 131.0] | nến 1W ĐÓNG dưới 101.6 | ĐÍCH TRƯỚC" in bc,
         "(9j) độ đúng dự báo chấm riêng từng khung")
    sha1 = KH._sha_ho_so(kh)
    kiem(len(sha1) == 64 and sha1 == KH._sha_ho_so(kh), "(9k) khoá nguồn dữ liệu: hồ sơ tại T dựng lại offline, sha256 ổn định")


# ---------------- (10) nhánh còn lại ----------------
def kiem_10():
    ds = nen_1h([100, 101, 102, 104, 103, 103, 104, 106, 104, 104, 105, 107, 108, 109, 111, 110])
    L = lenh(kieu_vao="dong", kich_hoat={"khung": "4H", "phia": "tren", "gia": 103.5, "so_nen": 2})
    r = chay(gia(ds), L)
    kiem(r["A"][0] == "VAO" and r["A"][1].a == T0 + 8 * H and r["gia_vao"] == 106 and r["B"][0] == "TP",
         "(10a) chờ xác nhận 2 nến 4H đóng trên 103.5 → vào lúc cây thứ 2 đóng, giá = giá đóng cây đó, rồi TP")
    ds = nen_1h([100, 103, 106, 110.5, 112, 115.5, 113])
    L = lenh(kieu_vao="ngay", gia_vao=100.0, tp=[110.0, 115.0], tp_vung=[(110, 111), (115, 116)], ty_le=[0.5, 0.5])
    r = chay(gia(ds), L)
    kiem(r["B"][0] == "TP" and r["B"][1].a == T0 + 3 * H and r["tp_sau"] and r["tp_sau"][0][1].a == T0 + 5 * H,
         "(10b) nhiều nấc TP: kết quả chính = TP1, phần còn lại ghi TP2 riêng")
    ds = nen_1h([100, 99, 98, 97, 95.5, 99])
    m = CH.May(gia(ds), lenh(), T0 + 1800).chay()
    kiem(m.vao is not None and m.vao.a == T0 + 4 * H and any("nằm giữa nến" in x for x in m.ghi_chu),
         "(10c) trực tiếp: phát hành giữa nến → xét từ nến kế tiếp, có ghi phần bỏ qua")
    k = _mau()
    k["gio_phat_hanh"] = "2026-09-21 11:40"
    kiem(CH.bat_dau_cua(k) == KH.doc_gio("2026-09-21 11:40") and CH.bat_dau_cua(_mau()) == KH.doc_gio("2026-09-21 11:00"),
         "(10d) mốc bắt đầu: trực tiếp = giờ phát hành; hồi cứu (> 24h) = gio_cat")


def main():
    for f in (kiem_1, kiem_2, kiem_3, kiem_4, kiem_5, kiem_6, kiem_7, kiem_8, kiem_9, kiem_10):
        f()
    print(f"\n{'PASS hết' if not LOI else f'{len(LOI)} FAIL'}")
    return 1 if LOI else 0


if __name__ == "__main__":
    sys.exit(main())
