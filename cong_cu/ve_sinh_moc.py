#!/usr/bin/env python3
"""Vệ sinh moc/*.json (P1-5 + P2, 31/10/2026):
  1. Gắn `tai_san` cho MỌI mốc: BTC / ETH / SOL / VANG / DAU / KHAC / CHUA_RO.
     Dò tự động = từ khoá trong câu trích + căn cứ (ghi chú trong ngoặc nằm trong `trich`) + độ lớn giá so với giá
     đóng nến ngày BTC hôm đó (du_lieu/btc_1Dutc.csv; thiếu ngày → ngày gần nhất trước đó): lệch > 40% mà câu không
     rõ BTC → CHUA_RO. Sau đó áp bảng XAC_NHAN_TAY (đọc tay câu trích + transcript quanh moc_gio).
     Mốc không phải BTC (kể cả CHUA_RO) → `chac: false` (các công cụ đếm căn cứ đã bỏ mốc chac=false). Không xoá mốc.
  2. Mốc đảo cận (`gia > gia_tren`) → đổi chỗ hai mép.
Sửa tại chỗ, GIỮ NGUYÊN định dạng từng file (chỉ chèn khoá `tai_san` trước `chac` và thay đúng giá trị cần đổi),
sau đó kiểm lại bằng json.loads. Chạy lại nhiều lần cho cùng kết quả.
Dò thêm theo ngữ cảnh (--ngu-canh): cửa sổ transcript [moc_gio − 60 s, + 20 s] nhắc ≥ 2 lần tài sản có giá "trùng hàng
nghìn" với BTC khi nói tắt (SOL, dầu, OKB, ZEC, HYPE, LTC, AAVE, BNB, NEAR, BTC.D, USDT.D) và nhiều hơn số lần nhắc BTC
→ in danh sách nghi để đọc tay (không tự đổi; kết luận đọc tay ghi vào XAC_NHAN_TAY).
Cách dùng: python3 cong_cu/ve_sinh_moc.py [--chi-xem] [--ngu-canh]   (--chi-xem: chỉ in, không ghi file)
"""
import csv, json, re, sys, unicodedata
from bisect import bisect_right
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
NGUONG_LECH = 0.40

TU_KHOA = {
    "ETH": r"\beth\b|\bether|ethereum",
    "SOL": r"\bsol\b|solana",
    "DAU": r"\bdầu\b|\boil\b|\bwti\b|brent",
    "VANG": r"\bvàng\b|\bgold\b|\bxau\b",
    "KHAC": r"\bokb\b|\bbnb\b|\bnear\b|\bzec\b|altcoin|\balt\b|chứng khoán|cổ phiếu|s&p|nasdaq|\bdxy\b|usdt\.?d\b|btc\.?d\b"
            r"|dominance|\bxrp\b|\bdoge|\bsui\b|\bhype\b|\bltc\b|\blink\b|\bavax\b|\bbạc\b|silver|\bbch\b|\bwld\b",
}
BTC = r"\bbtc\b|bitcoin|\bbít\b|\bbit\b"
# "vàng" chỉ MÀU (đường vàng, vùng vàng, ô tô vàng…) — không phải giá vàng
MAU_VANG = r"(màu|đường|vùng|line|ô tô|ma|hộp|box|khối|vạch|nét)( màu)? vàng|vàng (sáng|chói|nhạt|đậm)"
PHU_DINH_BTC = r"không phải btc|không rõ btc|không chắc là giá btc|có thể không phải btc"

LY_DO_CHU_KY = ("đọc tay: view chu kỳ BTC dài hạn của người nói (gap CME 20K/22K, vùng gom 40–20K, giảm 70–77% từ "
                "đỉnh, đỉnh 126K/lệnh short 125K, mục tiêu mùa sau 120–200K) — xa giá hiện tại nhưng là BTC")
LY_DO_MAU_VANG = "đọc tay: 'vàng' là màu đường/vùng tự vẽ trên chart BTC, không phải giá vàng"
LY_DO_SO_SANH = "đọc tay: câu so sánh BTC với tài sản khác; con số là mức BTC"
LY_DO_USDT = "đọc tay: USDT.D/BTC.D/altcoin chỉ là điều kiện tương quan; con số là mức BTC"

# khoá "buoi#chỉ số mốc" → (tài sản, lý do). Đọc tay 31/10/2026.
XAC_NHAN_TAY = {
    # —— KHÔNG phải BTC / chưa rõ ——
    "2026-07-09_Fmb8AziZ6f4#3": ("DAU", "transcript 00:29:33: trả lời câu hỏi 'con dầu ở vùng giá này còn giảm nữa không… "
                                 "khung tuần… giảm về quanh 60'; số 60 là giá dầu bị quy thành 60.000"),
    "2026-08-10_8BGhoFetSaU#10": ("SOL", "transcript 00:51:53: 'SOL thì không có gì để view… H4 của nó… chờ backtest về "
                                  "73 74 rồi tính'; giá SOL bị quy thành 73–74K"),
    "2026-08-11_1005_KvVvliql8xI#10": ("CHUA_RO", "transcript: đang xem USDT.D ('nó mà nổ đi lên một phát trên này là coi "
                                       "như là 57 hoặc 58'); không rõ 57–58 là mức BTC hay mức USDT.D"),
    "2026-07-01_WNiQnpm2BLo#14": ("CHUA_RO", "transcript 00:48:09: ngay sau 'Swing dầu TP?… Long dầu… H4 đóng trên 61'; "
                                  "'64, 66' có thể là dầu, cũng có thể đã quay lại BTC (61K là mốc BTC #7)"),
    "2026-03-16_uXm43DPUtPQ#23": ("CHUA_RO", "transcript 00:46:26–00:46:57: vừa nói dầu ('sway trong 71 đến 73') rồi trả "
                                  "lời câu hỏi FOMO ETH; '73k8, 73k9' không rõ của BTC hay dầu"),
    "2026-04-07_HeBpJr0i6Bg#21": ("CHUA_RO", "transcript 00:33:24: câu nằm giữa đoạn 'Qua view vàng dầu. Con dầu vẫn tăng… "
                                  "Dầu cứ lầm lì đi lên', nhưng 67k5/74/76/78 trùng hệt các mốc BTC vừa nêu ở 00:30–00:31"),
    # —— dò tự động gắn khác BTC/CHUA_RO, đọc tay xác nhận là BTC ——
    "2026-02-03_ewRoIMVREvw#15": ("BTC", LY_DO_SO_SANH + " ('Bao giờ Bitcoin về 40.000 là gom')"),
    "2026-03-09_-jRLufOuVEE#20": ("BTC", LY_DO_SO_SANH + " ('Nếu BTC về 40.000 thì ETH…')"),
    "2026-01-06_aQbHs7J80jc#11": ("BTC", "đọc tay: 40–20K là vùng BTC để 'bay altcoin'; con số là BTC"),
    "2026-01-27_Q2qX5gIvNC8#7": ("BTC", "đọc tay: H4 BTC đóng trên 90K2/90K7 là điều kiện để long altcoin"),
    "2026-03-03_xXKnEs9z81g#1": ("BTC", LY_DO_MAU_VANG),
    "2026-03-24_xKTPieljFuY#24": ("BTC", "transcript 01:00:57: trả lời câu hỏi kịch bản BTC 'lên 77 rồi quay đầu' → '80 83… "
                                  "nếu gãy tiếp thì lên không qua được 74'; câu 'con này pump dump' sau đó mới là coin khác"),
    "2026-03-25_byYCWvbkZyU#5": ("BTC", LY_DO_MAU_VANG),
    "2026-06-01_cgTktZyPPt4#5": ("BTC", LY_DO_MAU_VANG),
    "2026-06-24_ZrqOEgiFEF8#5": ("BTC", LY_DO_MAU_VANG),
    "2026-07-07_uvBnzq6-k-M#2": ("BTC", LY_DO_MAU_VANG),
    "2026-08-14_1004_xK38gQ-G6uA#5": ("BTC", LY_DO_MAU_VANG),
    "2026-08-14_1004_xK38gQ-G6uA#8": ("BTC", LY_DO_USDT),
    "2026-09-08_1002_gOwbzU0t2S0#2": ("BTC", LY_DO_MAU_VANG),
    "2026-09-23_1007_uK4vb9PoUIo#10": ("BTC", LY_DO_USDT),
    "2026-09-25_1014_Wf7PeLs6l94#15": ("BTC", "transcript: USDT.D chạy mô hình cờ rồi giảm → BTC lên 90.000 (BTC ~84K)"),
    "2026-09-29_1002_3inGNRqb-UM#1": ("BTC", LY_DO_MAU_VANG),
    "2026-10-15_1005_5iN8iTFsmlY#2": ("BTC", LY_DO_MAU_VANG),
}
# Mốc lệch > 40% không có chữ BTC trong câu: đọc tay toàn bộ, đều là view chu kỳ BTC dài hạn
CHU_KY_BTC = """
2026-01-06_aQbHs7J80jc#10 2026-01-06_aQbHs7J80jc#13 2026-01-06_aQbHs7J80jc#14 2026-01-07_NOBgwE4Gdko#13
2026-01-08_jX-0Hgy1S0E#8 2026-01-08_jX-0Hgy1S0E#9 2026-01-16_SllvhCOjrkE#8 2026-01-20_GygVJDmjlgY#9
2026-01-27_Q2qX5gIvNC8#8 2026-01-27_Q2qX5gIvNC8#9 2026-01-28_2_a0RdwC1t8#9 2026-01-28_2_a0RdwC1t8#10
2026-02-02_XD9H1FstBkE#1 2026-02-02_XD9H1FstBkE#15 2026-02-06_PLl8AM0RxEM#1 2026-02-06_PLl8AM0RxEM#12
2026-02-11_MZ3XfAjYHqk#9 2026-02-11_MZ3XfAjYHqk#10 2026-02-26_7zFMbvqo3QI#17 2026-02-26_7zFMbvqo3QI#18
2026-02-27_9wE4YYq3P6Y#17 2026-02-27_9wE4YYq3P6Y#18 2026-03-02_GYgaZiYqRXY#7 2026-03-02_GYgaZiYqRXY#8
2026-03-02_GYgaZiYqRXY#30 2026-03-02_GYgaZiYqRXY#31 2026-03-02_GYgaZiYqRXY#33 2026-03-04_OawlrpkFqQk#22
2026-03-04_OawlrpkFqQk#23 2026-03-04_OawlrpkFqQk#24 2026-03-11_q-9RpBVzOhU#16 2026-03-12_qJZk9q5A7rA#0
2026-03-12_qJZk9q5A7rA#20 2026-03-12_qJZk9q5A7rA#21 2026-03-16_uXm43DPUtPQ#2 2026-03-17_UKs5T1J0H9w#22
2026-03-18_oyJGNnpopXw#19 2026-03-30_KbxhGxmcYwg#8 2026-03-30_KbxhGxmcYwg#16 2026-03-30_KbxhGxmcYwg#21
2026-04-01_Be-e74Mwx0U#9 2026-04-01_Be-e74Mwx0U#10 2026-04-02_orDQVRuxI1E#5 2026-04-03_vnCUK9ayUsI#19
2026-04-07_HeBpJr0i6Bg#9 2026-04-13_Fvz3aEsoOEE#4 2026-04-14_LfNwCzyBHdM#21 2026-04-24_ZTOmNH9I_wM#26
2026-04-28_lZw7Ts1eLWo#6 2026-05-05_Au_SuIIstcY#18 2026-05-11_jm7VS-lKW8w#3 2026-05-18_phLlmyf_8-w#16
2026-05-18_phLlmyf_8-w#17 2026-05-19_sWk33q2YCj4#17 2026-05-29_AmGhhyxkErs#15 2026-06-01_cgTktZyPPt4#13
2026-06-03_OVGlvdAXMKo#3 2026-06-03_OVGlvdAXMKo#4 2026-06-04_59zOmIM_EOM#5 2026-06-04_59zOmIM_EOM#6
2026-06-04_59zOmIM_EOM#9 2026-06-05_a6-MmsaBAfA#17 2026-06-05_a6-MmsaBAfA#21 2026-06-05_a6-MmsaBAfA#22
2026-06-08_WZ8PpZ9VA4Q#4 2026-06-08_WZ8PpZ9VA4Q#6 2026-06-08_WZ8PpZ9VA4Q#17 2026-06-09_UmnCq7p4NlU#13
2026-06-09_UmnCq7p4NlU#14 2026-06-09_UmnCq7p4NlU#21 2026-06-22_eaj9NEm85O4#16 2026-06-24_ZrqOEgiFEF8#12
2026-06-25_gy-YwzytUiA#17 2026-06-26_UzjWDBAiahs#16 2026-06-26_UzjWDBAiahs#20 2026-06-29_wyCTvVbTVPE#13
2026-06-29_wyCTvVbTVPE#14 2026-07-01_WNiQnpm2BLo#3 2026-07-01_WNiQnpm2BLo#15 2026-07-01_WNiQnpm2BLo#16
2026-07-06_GRWl0b0z1nk#18 2026-07-07_uvBnzq6-k-M#13 2026-07-13_O3q2fmXlwhk#8 2026-07-13_O3q2fmXlwhk#9
2026-07-13_O3q2fmXlwhk#26 2026-07-13_O3q2fmXlwhk#28 2026-07-23_IsyMSPIscsc#10 2026-08-05_uw4QcusFtBc#12
2026-08-05_uw4QcusFtBc#13 2026-08-12_1003_EaWaSL7aWT4#2 2026-08-12_1003_EaWaSL7aWT4#17 2026-08-13_1006_hNxSX7GUKMs#10
2026-08-14_1004_xK38gQ-G6uA#13 2026-08-19_1001_kfBEaOyHLkc#10 2026-08-19_1001_kfBEaOyHLkc#11
2026-08-19_1001_kfBEaOyHLkc#12 2026-08-19_1001_kfBEaOyHLkc#14 2026-08-21_1003_oDD5qwLcZbw#8
2026-08-25_1003_nSxBbLai2mE#7 2026-08-25_1003_nSxBbLai2mE#16 2026-08-25_1003_nSxBbLai2mE#17
2026-08-25_1003_nSxBbLai2mE#18 2026-08-25_1003_nSxBbLai2mE#23 2026-08-26_1001_I1DFCTsjQXE#21
2026-08-27_1006_ZJ5BVqdLJeE#12 2026-09-04_1014_eujLmRVw88k#8 2026-09-04_1014_eujLmRVw88k#16
2026-09-04_1014_eujLmRVw88k#24 2026-09-14_1007_ykgTTK3EbP8#18 2026-09-18_1003_YPMgjMxL2io#19
2026-09-23_1007_uK4vb9PoUIo#14 2026-10-07_1004_Rl-3RfG8EiY#17 2026-10-14_1009_BlA26qxNBTE#18
2026-10-14_1009_BlA26qxNBTE#19 2026-10-16_1007_lSGpwulXi5s#10 2026-10-16_1007_lSGpwulXi5s#11
2026-10-27_1002_2RB3G-MYjhE#9 2026-10-28_1006_Gu1XtyNNH6I#10
"""
for _k in CHU_KY_BTC.split():
    XAC_NHAN_TAY.setdefault(_k, ("BTC", LY_DO_CHU_KY))


def chuan(s):
    return unicodedata.normalize("NFC", s or "").lower()


def doc_gia_ngay():
    with (GOC / "du_lieu" / "btc_1Dutc.csv").open() as f:
        r = [(x["ts_utc"][:10], float(x["close"])) for x in csv.DictReader(f)]
    return [a for a, _ in r], [b for _, b in r]


NGAY, DONG = doc_gia_ngay()


def gia_btc(ngay):
    i = bisect_right(NGAY, ngay) - 1
    return DONG[max(i, 0)]


def do_tu_dong(m, ngay):
    """→ (tài sản, lý do, cần đọc tay?)"""
    t = chuan(m.get("trich", "") + " | " + " ; ".join(m.get("can_cu") or []))
    t_tai_san = re.sub(MAU_VANG, " ", t)
    khac = [k for k, p in TU_KHOA.items() if re.search(p, t_tai_san)]
    co_btc = bool(re.search(BTC, re.sub(r"btc\.?d\b", " ", t)))
    phu_dinh = bool(re.search(PHU_DINH_BTC, t))
    canh = [g for g in (m.get("gia"), m.get("gia_tren")) if isinstance(g, (int, float))]
    gb = gia_btc(ngay)
    lech = min(abs(g / gb - 1) for g in canh) if canh else 0
    xa = lech > NGUONG_LECH
    ly = f"lệch {lech:.0%} so với BTC đóng ngày {gb:,.0f}"
    if phu_dinh:
        ts = [k for k in khac if k != "KHAC"] or khac
        return (ts[0] if len(ts) == 1 else "CHUA_RO"), "câu tự ghi không phải/không rõ BTC; " + ly, True
    if khac and not co_btc:
        return (khac[0] if len(khac) == 1 else "KHAC"), "từ khoá " + "/".join(khac) + " không kèm BTC; " + ly, True
    if khac and co_btc:
        return ("CHUA_RO" if xa else "BTC"), "nhắc cả BTC lẫn " + "/".join(khac) + "; " + ly, True
    if xa and not co_btc:
        return "CHUA_RO", ly + " và câu không ghi BTC", True
    return "BTC", ly, False


def chia_moc(text):
    """Vị trí [đầu, cuối) của từng object trong mảng "moc" (quét ký tự, bỏ qua chuỗi)."""
    i = text.index("[", text.index('"moc"'))
    ra, sau, trong_chuoi, thoat, bat_dau = [], 0, False, False, None
    for k in range(i + 1, len(text)):
        c = text[k]
        if trong_chuoi:
            if thoat: thoat = False
            elif c == "\\": thoat = True
            elif c == '"': trong_chuoi = False
            continue
        if c == '"': trong_chuoi = True
        elif c in "{[":
            if sau == 0: bat_dau = k
            sau += 1
        elif c in "}]":
            if sau == 0: break
            sau -= 1
            if sau == 0: ra.append((bat_dau, k + 1))
    return ra


def thay_gia_tri(s, khoa, gia_tri):
    s2, n = re.subn(r'("%s"\s*:\s*)(-?\d+(?:\.\d+)?|null|true|false|"[^"]*")' % khoa, lambda x: x[1] + gia_tri, s, count=1)
    assert n == 1, (khoa, s[:80])
    return s2


def sua_object(s, tai_san, doi_can, chac_moi):
    if doi_can:
        o = json.loads(s)
        s = thay_gia_tri(s, "gia", json.dumps(o["gia_tren"]))
        s = thay_gia_tri(s, "gia_tren", json.dumps(o["gia"]))
    if chac_moi is not None:
        s = thay_gia_tri(s, "chac", "true" if chac_moi else "false")
    if '"tai_san"' in s:
        s = thay_gia_tri(s, "tai_san", json.dumps(tai_san))
    else:
        m = re.search(r'"chac"\s*:', s)
        dau_dong = s.rfind("\n", 0, m.start()) + 1
        thut = s[dau_dong:m.start()]
        chen = (f'"tai_san": "{tai_san}",\n{thut}' if thut.strip() == "" and dau_dong > 0 else f'"tai_san": "{tai_san}", ')
        s = s[:m.start()] + chen + s[m.start():]
    return s


NGU_CANH = {"SOL": r"\bsol\b|solana", "DAU": r"\bdầu\b|\boil\b|\bwti\b|brent", "OKB": r"\bokb\b", "ZEC": r"\bzec\b|zcash",
            "HYPE": r"\bhype\b", "LTC": r"\bltc\b|litecoin", "AAVE": r"\baave\b", "BTCD": r"btc\.? ?d\b|dominance",
            "USDTD": r"usdt\.? ?d\b", "BNB": r"\bbnb\b", "NEAR": r"\bnear\b"}


def nghi_ngu_canh():
    sys.path.insert(0, str(GOC / "cong_cu"))
    from chon_moc import doc_cau
    ra = []
    for p in sorted((GOC / "moc").glob("2*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        nguon = [GOC / "transcripts" / "zip_clean" / f"{d['buoi']}.txt"] + sorted((GOC / "transcripts" / "phu_de").glob(f"{d['buoi']}*.vtt"))
        nguon = [x for x in nguon if x.exists()]
        if not nguon:
            continue
        cau = doc_cau(nguon[0])
        for i, m in enumerate(d["moc"]):
            if not m.get("moc_gio"):
                continue
            t = sum(int(x) * k for x, k in zip(m["moc_gio"].split(":"), (3600, 60, 1)))
            w = chuan(" ".join(c for g, c in cau if t - 60 <= g <= t + 20))
            hit = {k: len(re.findall(p_, w)) for k, p_ in NGU_CANH.items()}
            hit = {k: v for k, v in hit.items() if v}
            nb = len(re.findall(BTC, w))
            if sum(hit.values()) >= 2 and sum(hit.values()) > nb:
                ra.append((f"{d['buoi']}#{i}", hit, nb, m))
    return ra


def main():
    if "--ngu-canh" in sys.argv:
        ds = nghi_ngu_canh()
        for khoa, hit, nb, m in ds:
            kl = XAC_NHAN_TAY.get(khoa, ("BTC (đọc tay, giữ)",))[0]
            print(f"| {khoa} | {m['gia']:,} | {hit} BTC×{nb} | {kl} | {m['trich'][:70]} |")
        print(f"{len(ds)} mốc nghi theo ngữ cảnh")
        return
    chi_xem = "--chi-xem" in sys.argv
    dem, dem_tu_dong, doi, dao, doc_tay = {}, {}, [], [], []
    for p in sorted((GOC / "moc").glob("2*.json")):
        text = p.read_text(encoding="utf-8")
        d = json.loads(text)
        span = chia_moc(text)
        assert len(span) == len(d["moc"]), p.name
        moi, cuoi, mong = [], 0, json.loads(text)
        for i, ((a, b), m) in enumerate(zip(span, d["moc"])):
            assert json.loads(text[a:b]) == m, (p.name, i)
            khoa = f"{d['buoi']}#{i}"
            ts_tu, ly_tu, can_doc = do_tu_dong(m, d["ngay"])
            dem_tu_dong[ts_tu] = dem_tu_dong.get(ts_tu, 0) + 1
            ts, ly = ts_tu, ly_tu
            if khoa in XAC_NHAN_TAY:
                ts, ly = XAC_NHAN_TAY[khoa]
            elif can_doc and ts_tu != "BTC":
                print(f"!! CHƯA ĐỌC TAY: {khoa} tự động={ts_tu} ({ly_tu}) | {m['trich'][:100]}", file=sys.stderr)
            if can_doc or khoa in XAC_NHAN_TAY:
                doc_tay.append((khoa, ts_tu, ts, ly, m))
            dem[ts] = dem.get(ts, 0) + 1
            gt = m.get("gia_tren")
            doi_can = isinstance(gt, (int, float)) and isinstance(m.get("gia"), (int, float)) and m["gia"] > gt
            chac_moi = False if ts != "BTC" and m.get("chac", True) else None
            dong = ("".join(moi) + text[cuoi:a]).count("\n") + 1  # dòng trong file SAU khi sửa
            if doi_can: dao.append((p.name, dong, m["gia"], gt, m["vai_tro"], m["trich"]))
            if ts != "BTC": doi.append((p.name, dong, ts, m["gia"], gt, m.get("chac", True), ly, m["trich"]))
            moi.append(text[cuoi:a]); moi.append(sua_object(text[a:b], ts, doi_can, chac_moi)); cuoi = b
            mm = mong["moc"][i]
            if doi_can: mm["gia"], mm["gia_tren"] = gt, m["gia"]
            if chac_moi is not None: mm["chac"] = chac_moi
            mm["tai_san"] = ts
        moi.append(text[cuoi:])
        moi = "".join(moi)
        assert json.loads(moi) == mong, p.name
        if not chi_xem and moi != text:
            p.write_text(moi, encoding="utf-8")
    thua = set(XAC_NHAN_TAY) - {k for k, *_ in doc_tay}
    assert not thua, f"khoá XAC_NHAN_TAY không khớp mốc nào: {sorted(thua)}"
    tong = sum(dem.values())
    print(f"Tổng {tong} mốc · sau đọc tay: {dict(sorted(dem.items()))} · dò tự động: {dict(sorted(dem_tu_dong.items()))}")
    print(f"Đọc tay {len(doc_tay)} mốc (gồm mọi mốc tự động gắn khác BTC/CHUA_RO + nghi theo ngữ cảnh transcript)")
    print("\n## Mốc không phải BTC / chưa rõ (đã đặt chac=false)")
    for f, dong, ts, g, gt, chac_cu, ly, tr in doi:
        print(f"| `moc/{f}:{dong}` | {ts} | {g:,}{'' if gt is None else f'–{gt:,}'} | {'true→false' if chac_cu else 'false (giữ)'} | {ly} | {tr[:90]} |")
    print(f"\n## Mốc đảo cận đã đổi chỗ ({len(dao)})")
    for f, dong, g, gt, vt, tr in dao:
        print(f"| `moc/{f}:{dong}` | {g:,} > {gt:,} → {gt:,}–{g:,} | {vt} | {tr[:80]} |")
    print("\n## Đọc tay: tự động khác BTC → xác nhận BTC")
    for khoa, tu, ts, ly, m in doc_tay:
        if tu != "BTC" and ts == "BTC":
            print(f"| {khoa} | {tu}→BTC | {m['gia']:,} | {m['trich'][:70]} |")


if __name__ == "__main__":
    main()
