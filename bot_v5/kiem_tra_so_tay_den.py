#!/usr/bin/env python3
"""Kiểm `bot_v5/so_tay_den.py` (offline, ghi ra thư mục tạm, không đụng bot_v5/_so_tay_T/).
  (a) T = 2026-09-21 11:00, 2026-07-15 10:00, 2026-03-01 10:00: quét bằng regex ĐỘC LẬP (không dùng bộ nhận dạng của
      so_tay_den) mọi file output → không còn mốc ngày nào ≥ ngày của T (MM-DD, [MM-DD · …], MM-DD/DD, DD/MM, DD/MM/YYYY,
      MM/YYYY, 2026-MM-DD, ô tháng T7, nhãn **Tháng 7**, link YouTube / tên ảnh của buổi ≥ T); bảng đợt view: ngày đầu
      đợt + "Ngày tới lần đổi" < T.
  (b) T = 2025-12-01 10:00 (trước buổi đầu 2026-01-06): như (a) và không còn trích dẫn [MM-DD…] / link buổi nào.
  (c) Mọi T: dòng đầu "> Lọc theo T = …; bỏ N dòng có ngày ≥ T" đúng N; đủ mọi tiêu đề (#…) của bản gốc theo đúng thứ tự
      (gồm mọi tiêu đề case `## A1.`… và `# A.`…); <details> cân; mỗi bảng có hàng tiêu đề + hàng kẻ + số cột đều;
      giong_noi.md = phần C (tới trước PHẦN D) và còn bảng mẫu câu.
  (d) Số dòng còn lại hợp lý: T càng sớm còn càng ít (đơn điệu theo T); T = 2025-12-01 vẫn còn ≥ 35% dòng mỗi sổ tay;
      T = 2026-09-21 còn ≥ 85%; T = 2027-01-15 (sau mọi dữ liệu) không bỏ dòng nào.
  (e) Bộ nhận dạng: phân số / T7–CN / giờ / năm dự báo KHÔNG là ngày; các dạng ngày đều nhận ra; bảng tháng / cột
      "Ngày tới lần đổi"; bỏ cả dòng + dòng con; giọng nói bỏ từng câu mẫu; giá không ngày.
Dùng: python3 bot_v5/kiem_tra_so_tay_den.py   (exit 1 nếu có FAIL)
"""
import datetime as dt, io, re, sys, tempfile
from contextlib import redirect_stdout
from pathlib import Path

DAY = Path(__file__).resolve().parent
sys.path.insert(0, str(DAY))
import so_tay_den as STD  # noqa: E402

LOI = []
NAM = 2026
FILE_RA = [p.name for p in STD.NGUON] + ["giong_noi.md"]
CAC_T = [("2026-09-21 11:00", "a"), ("2026-07-15 10:00", "a"), ("2026-03-01 10:00", "a"), ("2025-12-01 10:00", "b")]


def kiem(dk, ten):
    print(("PASS " if dk else "FAIL ") + ten)
    if not dk:
        LOI.append(ten)


# ---------------- quét ngày độc lập (rộng tay hơn bộ lọc) ----------------
def _d(y, m, d):
    try:
        return dt.date(y, m, d)
    except ValueError:
        return None


def _thang(y, m):
    if y > NAM or not 1 <= m <= 12:
        return None
    return dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)


def _ngay_buoi():
    ra = {}
    for dong in (DAY.parent / "transcripts" / "danh_sach.tsv").read_text(encoding="utf-8").split("\n")[1:]:
        o = dong.split("\t")
        if len(o) > 1 and re.fullmatch(r"\d{4}-\d\d-\d\d", o[1]):
            ra[o[0]] = dt.date.fromisoformat(o[1])
    return ra


NGAY_BUOI = _ngay_buoi()


def quet_ngay(dong):
    """[(date, đoạn khớp)] — mọi thứ trông như ngày. Chỉ loại: phân số 'a/b =' / 'a/b/c', năm > 2026 (dự báo)."""
    ra = [(NGAY_BUOI[m[1]], m.group(0)) for m in re.finditer(r"(?:v=|/)([\w-]{11})(?:_\d{6}\.jpg|[&)\s])", dong)
          if m[1] in NGAY_BUOI]
    ra += [(NGAY_BUOI[m[1]], m.group(0)) for m in re.finditer(r"([\w-]{11})_\d{6}\.jpg", dong) if m[1] in NGAY_BUOI]
    s = re.sub(r"\((?:https?://|\.\./)[^)]*\)", "()", dong)

    def lay(r, ham):
        nonlocal s
        for m in re.finditer(r, s):
            x = ham(m)
            if x:
                ra.append((x, m.group(0)))
        s = re.sub(r, lambda m: " " * len(m.group(0)), s)

    lay(r"(20\d\d)-(\d\d)-(\d\d)", lambda m: _d(int(m[1]), int(m[2]), int(m[3])) if int(m[1]) <= NAM else None)
    lay(r"(\d{1,2})/(\d{1,2})/(20\d\d)", lambda m: _d(int(m[3]), int(m[2]), int(m[1])) if int(m[3]) <= NAM else None)
    lay(r"(?<!\d)(\d{1,2})/(20\d\d)", lambda m: _thang(int(m[2]), int(m[1])))
    lay(r"(?<![\d.,])(\d{2})-(\d{2})(?![\d:])", lambda m: _d(NAM, int(m[1]), int(m[2])))
    lay(r"(?<!\d)(\d{2})-(\d{2})/(\d{2})(?!\d)", lambda m: _d(NAM, int(m[1]), int(m[3])))

    def dm(m):
        sau = s[m.end():m.end() + 6]
        if re.match(r"\s*(?:=|\(\d+%)", sau) or sau.startswith("/"):   # phân số "10/22 = 45%", "11/17 (65%)"
            return None
        a, b = int(m[1]), int(m[2])
        return _d(NAM, b, a) or _d(NAM, a, b)
    lay(r"(?<![\d/.,])(\d{2})/(\d{2})(?![\d/])", dm)
    lay(r"(?:ngày\s+)(\d{1,2})/(\d{1,2})", lambda m: _d(NAM, int(m[2]), int(m[1])))
    m = re.match(r"^\s*(?:[-*+]\s+)?\*\*Tháng\s+(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?\*\*", dong)
    if m:
        ra.append((_thang(NAM, int(m[2] or m[1])), m.group(0)))
    if dong.lstrip().startswith("|"):
        for o in dong.strip().strip("|").split("|"):
            m = re.match(r"^\**\s*T(\d{1,2})\s*\**$", o.strip())
            if m:
                ra.append((_thang(NAM, int(m[1])), o.strip()))
    return [x for x in ra if x[0]]


def bang_dot_view(van):
    """(ngày đầu đợt, số ngày tới lần đổi) trong bảng có cột 'Ngày tới lần đổi'."""
    ra, cot = [], None
    for dong in van.split("\n"):
        if not dong.lstrip().startswith("|"):
            cot = None
            continue
        o = [x.strip() for x in dong.strip().strip("|").split("|")]
        if any("Ngày tới" in x for x in o):
            cot = next(k for k, x in enumerate(o) if "Ngày tới" in x)
            continue
        if cot is not None and cot < len(o) and re.fullmatch(r"\d+", o[cot]):
            m = re.search(r"(\d{2})-(\d{2})", dong)
            if m:
                ra.append((dt.date(NAM, int(m[1]), int(m[2])), int(o[cot])))
    return ra


# ---------------- cấu trúc Markdown ----------------
def so_cot(dong):
    s, code, n = dong.strip(), False, 0
    for i, ch in enumerate(s):
        if ch == "`":
            code = not code
        elif ch == "|" and not code and (i == 0 or s[i - 1] != "\\"):
            n += 1
    return n


def kiem_cau_truc(van, ten):
    dong = van.split("\n")
    ok_bang, i, so_bang = True, 0, 0
    while i < len(dong):
        if dong[i].lstrip().startswith("|"):
            j = i
            while j < len(dong) and dong[j].lstrip().startswith("|"):
                j += 1
            khoi = dong[i:j]
            so_bang += 1
            rong = len(khoi) == 2 and STD.GHI_CHU_BANG in "\n".join(dong[j:j + 3])   # bảng lọc hết, có ghi chú
            if ((len(khoi) < 3 and not rong) or not re.match(r"^\s*\|[\s:|-]+\|\s*$", khoi[1])
                    or len({so_cot(x) for x in khoi}) != 1):
                ok_bang = False
                print("     bảng hỏng:", ten, "dòng", i + 1, khoi[0][:80])
            i = j
        else:
            i += 1
    can = van.count("<details") == van.count("</details>")
    return ok_bang and can, so_bang


def tieu_de(van):
    return [x.rstrip() for x in van.split("\n") if re.match(r"^#{1,6} ", x)]


def goc(ten):
    if ten == "giong_noi.md":
        return STD.phan_c()
    return (DAY / "so_tay" / ten).read_text(encoding="utf-8")


def so_dong_con(van):
    return len(van.split("\n")) - 2     # trừ dòng "Lọc theo T" + dòng trống


# ---------------- kiểm theo T ----------------
def kiem_t(t_str, tmp, ten_kiem):
    han = STD.doc_t(t_str).date()
    ra = Path(tmp) / t_str[:10]
    tk = STD.tao(t_str, ra, in_ra=False)
    print(f"\n--- T = {t_str} (lọc mốc ≥ {han}) ---")
    for ten in FILE_RA:
        them = f", cắt {tk[ten]['muc']} câu mẫu" if tk[ten]["muc"] else ""
        print(f"     {ten}: bỏ {tk[ten]['bo']} dòng{them} (còn {tk[ten]['con']}/{tk[ten]['tong']})")
    sot, dem_trich, con = [], 0, {}
    for ten in FILE_RA:
        van = (ra / ten).read_text(encoding="utf-8")
        con[ten] = so_dong_con(van)
        dau = van.split("\n")[0]
        kiem(dau.startswith(f"> Lọc theo T = {t_str}") and f"bỏ {tk[ten]['bo']} dòng có ngày ≥ T" in dau,
             f"(c) T {t_str[:10]} {ten}: dòng đầu \"Lọc theo T = …; bỏ {tk[ten]['bo']} dòng có ngày ≥ T\"")
        for k, dong in enumerate(van.split("\n")[1:], 2):
            for d, khop in quet_ngay(dong):
                if d >= han:
                    sot.append(f"{ten}:{k} {khop!r} → {d}  | {dong.strip()[:110]}")
            dem_trich += len(re.findall(r"\[\d{2}-\d{2}[ \]·]", dong)) + len(re.findall(r"watch\?v=", dong))
        for d0, n in bang_dot_view(van):
            if d0 + dt.timedelta(days=n) >= han:
                sot.append(f"{ten}: bảng đợt view {d0} + {n} ngày ≥ T")
        ok, so_bang = kiem_cau_truc(van, ten)
        kiem(ok, f"(c) T {t_str[:10]} {ten}: {so_bang} bảng hợp lệ (tiêu đề + hàng kẻ + số cột đều), <details> cân")
        td_goc, td_moi = tieu_de(goc(ten)), tieu_de(van)
        so_case = len([x for x in td_goc if re.match(r"^(#{2,3} [A-Z]\d+\.|# [A-Z]\.)", x)])
        kiem(td_goc == td_moi, f"(c) T {t_str[:10]} {ten}: đủ {len(td_goc)}/{len(td_goc)} tiêu đề đúng thứ tự"
                               f" (trong đó {so_case} tiêu đề case)" if td_goc == td_moi else
             f"(c) T {t_str[:10]} {ten}: thiếu tiêu đề {sorted(set(td_goc) - set(td_moi))[:3]}")
    for x in sot[:15]:
        print("     SÓT:", x)
    kiem(not sot, f"({ten_kiem}) T {t_str}: không còn mốc ngày ≥ {han} trong {len(FILE_RA)} file (quét regex độc lập)")
    gn = (ra / "giong_noi.md").read_text(encoding="utf-8").split("\n", 2)[2]
    kiem(gn.startswith("# PHẦN C") and "| Tình huống | Mẫu câu thật |" in gn and "# PHẦN D" not in gn,
         f"(c) T {t_str[:10]} giong_noi.md: đúng phần C (tới trước PHẦN D), còn bảng mẫu câu")
    return tk, dem_trich, con


# ---------------- kiểm bộ nhận dạng / luật lọc ----------------
def kiem_nhan_dang():
    ca_khong = ["LẬT 10/22 = 45%", "khoảng 1/2 downtrend", "7/10 = 70%", "T7–CN chạy chung một nhịp", "[00:12:39]",
                "30/30/30", "EMA 34/89/200", "1/19 ảnh có MA", "11/17 (65%)", "Q1–Q2/2027", "halving 4/2028",
                "mép 84k), 2.313–7.000 giá", "giá 50-50", "đáy khoảng T11-12/2026", "(10/45 lệnh không quá mép)"]
    id_buoi, ngay_buoi = next(iter(NGAY_BUOI.items()))
    ca_co = {"[03-23 00:42:55](https://x/y)": [dt.date(2026, 3, 23)],
             "[01-07 · 00:09:11](https://x)": [dt.date(2026, 1, 7)],
             "**03-23/24, D1**": [dt.date(2026, 3, 23), dt.date(2026, 3, 24)],
             "01-12/01-19": [dt.date(2026, 1, 12), dt.date(2026, 1, 19)],
             "đáy 21/11/2025;": [dt.date(2025, 11, 21)],
             "cuối 11–12/2025": [dt.date(2025, 12, 31)],
             "(08/28 → 10/22, x)": [dt.date(2026, 8, 28), dt.date(2026, 10, 22)],
             "Ví dụ 02/10 H4": [dt.date(2026, 10, 2)],
             "| 16/10 sáng |": [dt.date(2026, 10, 16)],
             "(2026-01-06 → 2026-10-30)": [dt.date(2026, 1, 6), dt.date(2026, 10, 30)],
             "02-04 · D1": [dt.date(2026, 2, 4)],
             "- **Tháng 9–10**: dùng lại": [dt.date(2026, 10, 31)],
             f"[ảnh](../../so_tay/khung/{id_buoi}_002930.jpg)": [ngay_buoi],
             f"[00:12](https://www.youtube.com/watch?v={id_buoi}&t=5s)": [ngay_buoi]}
    ok = True
    for x in ca_khong:
        if STD.tim_ngay(x):
            ok = False
            print("     nhận nhầm là ngày:", x, STD.tim_ngay(x))
    for x, ky_vong in ca_co.items():
        if sorted(STD.tim_ngay(x)) != sorted(ky_vong):
            ok = False
            print("     nhận sai:", x, STD.tim_ngay(x), "≠", ky_vong)
    kiem(ok, f"(e) bộ nhận dạng ngày: {len(ca_khong)} ca KHÔNG phải ngày + {len(ca_co)} ca có ngày — đúng hết")

    han = dt.date(2026, 7, 1)
    van = ("| Tháng | Pha |\n|---|---|\n| T6 | a |\n| T9 | b |\n\n"
           "| # | Hướng | Từ → đến | Buổi | Ngày tới lần đổi |\n|---|---|---|---|---|\n"
           "| 1 | GIAM | 06-01 → 06-05 | 3 | 30 |\n| 2 | TANG | 07-01 → 07-02 | 2 | 3 |\n")
    moi, _ = STD.loc_van_ban(van, han)
    ok = ("| T6 |" in moi and "T9" not in moi and "06-01 → 06-05 | 3 | — |" in moi and "07-01" not in moi
          and kiem_cau_truc(moi, "mau")[0])
    kiem(ok, "(e) bảng: ô tháng T9 ≥ T bị bỏ, T6 giữ; 'Ngày tới lần đổi' vượt T → '—'; hàng đợt bắt đầu ≥ T bị bỏ")

    van = ("## X1. Luật\n- **Tần suất**: 7/10 = 70%.\n- **Ví dụ**:\n  - [05-02 · 00:01:00](https://x) \"a\" — giữ\n"
           "  - [07-03 · 00:01:00](https://x) \"b\"\n    - con của b, không ngày\n"
           "- **Kết luận**: đóng nến \"c\" [06-01]; \"d\" [08-01].\n- **Ví dụ khác**:\n  - [09-09] e\n"
           "- **Kết quả**: 06-20 vào 60k. **Đo:** không về.\n"
           "| Lúc | Lời |\n|---|---|\n| 1 | [09-01] x |\n")
    moi, tk = STD.loc_van_ban(van, han)
    ok = ("## X1. Luật" in moi and "7/10 = 70%" in moi and "\"a\" — giữ" in moi and "\"b\"" not in moi
          and "con của b" not in moi and "\"c\"" not in moi and "Ví dụ khác" not in moi and "Đo:" not in moi
          and "| Lúc | Lời |" in moi and STD.GHI_CHU_BANG in moi and tk["bo"] == 7)
    kiem(ok, f"(e) bỏ CẢ dòng có mốc ≥ T (kể cả dòng luật có 1 trích dẫn ≥ T) + dòng con; nhãn 'Ví dụ' trơ trọi bỏ;"
             f" 'Đo:' +{STD.BIEN_DO} ngày; bảng lọc hết còn tiêu đề + ghi chú (bỏ {tk['bo']}/7)")

    van = ("**Ẩn dụ**: ô tô (\"xe đâm\" [09-17]); đi săn; \"con cá\" [04-27].\n"
           "| Tình huống | Mẫu câu thật |\n|---|---|\n| **TĂNG** | \"đừng cản tàu\" [04-21] · \"bay thôi\" [09-21] |\n"
           "| **GIẢM** | \"đi củi\" [10-01] |\n")
    moi, tk = STD.loc_van_ban(van, dt.date(2026, 9, 1), theo_muc=True)
    ok = ("đi săn" in moi and "\"con cá\" [04-27]" in moi and "ô tô" not in moi and "\"đừng cản tàu\" [04-21]" in moi
          and "bay thôi" not in moi and "GIẢM" not in moi and tk["muc"] == 3 and tk["bo"] == 1
          and kiem_cau_truc(moi, "mau")[0])
    kiem(ok, "(e) giọng nói: bỏ từng câu mẫu có mốc ≥ T, hàng hết câu thì bỏ hàng")

    gd = STD.lap_gia_dau(["- 10-02 hộp 85,0–85,5k [10-02]\n- 01-06 vùng 91k\n| a | 59,8k (06/02) | 01-12 |"])
    ok = (gd.get(85.0) == dt.date(2026, 10, 2) and gd.get(91.0) == dt.date(2026, 1, 6)
          and gd.get(59.8) == dt.date(2026, 2, 6))
    moi, _ = STD.loc_van_ban("- vùng hẹp (85,0–85,5k)\n- số tròn (91k)\n", dt.date(2026, 9, 21), gia_dau=gd)
    ok = ok and "85,0" not in moi and "91k" in moi
    kiem(ok, "(e) giá không ngày: mức giá chỉ có từ ngày ≥ T (85,0–85,5k ← 10-02) bị bỏ, mức giá cũ (91k) giữ")


def main():
    kiem_nhan_dang()
    ket = {}
    with tempfile.TemporaryDirectory() as tmp:
        for t_str, ten_kiem in CAC_T:
            ket[t_str] = kiem_t(t_str, tmp, ten_kiem)
        _tk, con_trich, _ = ket["2025-12-01 10:00"]
        kiem(con_trich == 0, f"(b) T 2025-12-01: còn {con_trich} trích dẫn [MM-DD…] / link buổi (phải 0)")
        tk_sau = STD.tao("2027-01-15 10:00", Path(tmp) / "sau_het", in_ra=False)
        kiem(all(v["bo"] == 0 and v["muc"] == 0 for v in tk_sau.values()),
             "(d) T 2027-01-15: không bỏ dòng nào (" + ", ".join(f"{k} {v['bo']}" for k, v in tk_sau.items()) + ")")
        # CLI ghi đúng thư mục + in số dòng bỏ mỗi file
        buf = io.StringIO()
        with redirect_stdout(buf):
            ma = STD.main(["2026-09-21 11:00", "--ra", str(Path(tmp) / "cli")])
        ok = ma == 0 and all(f"{ten}: bỏ " in buf.getvalue() for ten in FILE_RA) and \
            sorted(p.name for p in (Path(tmp) / "cli").iterdir()) == sorted(FILE_RA)
        kiem(ok, "(c) CLI: ghi đúng 4 file, in số dòng bỏ mỗi file")
    # (d) số dòng còn lại đơn điệu theo T + ngưỡng
    thu_tu = ["2025-12-01 10:00", "2026-03-01 10:00", "2026-07-15 10:00", "2026-09-21 11:00"]
    ok_dd, ok_nguong, dong_in = True, True, []
    for ten in FILE_RA:
        day = [ket[t][2][ten] for t in thu_tu]
        tong = ket[thu_tu[0]][0][ten]["tong"]
        dong_in.append(f"{ten}: " + " → ".join(map(str, day)) + f" / {tong}")
        ok_dd &= all(a <= b for a, b in zip(day, day[1:])) and day[-1] <= tong
        if ten != "giong_noi.md":
            ok_nguong &= day[0] >= 0.35 * tong and day[-1] >= 0.85 * tong
    for x in dong_in:
        print("     còn lại (T 12-01 → 03-01 → 07-15 → 09-21):", x)
    kiem(ok_dd, "(d) số dòng còn lại tăng dần theo T ở mọi file")
    kiem(ok_nguong, "(d) sổ tay: T 2025-12-01 còn ≥ 35% dòng, T 2026-09-21 còn ≥ 85% dòng")
    tk0921 = ket["2026-09-21 11:00"][0]
    print("\nSố dòng bị lọc ở T = 2026-09-21 11:00:",
          " · ".join(f"{k}: bỏ {v['bo']}" + (f" + {v['muc']} câu mẫu" if v["muc"] else "") for k, v in tk0921.items()))
    print("KẾT QUẢ:", "PASS hết" if not LOI else f"{len(LOI)} FAIL")
    sys.exit(1 if LOI else 0)


if __name__ == "__main__":
    main()
