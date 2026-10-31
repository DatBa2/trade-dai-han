#!/usr/bin/env python3
"""P1-6 — gắn câu trích (đáp án v2 / phiếu / mốc) với giờ trong video + ảnh khung gần nhất.

Nguồn giờ: transcripts/phu_de/*.vtt (cue có giờ, mịn) và transcripts/zip_clean/*.txt (dòng [hh:mm:ss], thô,
nội suy theo số từ trong đoạn). Câu trích thường lấy từ bản làm sạch nên dò cả hai, ưu tiên VTT nếu đủ ngưỡng.
Khớp mờ: chuẩn hoá (bỏ dấu câu, chữ thường) → chọn cửa sổ từ có nhiều unigram/bigram trùng → SequenceMatcher
mức từ; do_giong = tỉ lệ từ của câu trích khớp được. Ngưỡng = 0,6; dưới ngưỡng → khong_tim_thay.
Chỉ đọc nguồn, chỉ ghi bang_chung/. Chạy: python3 cong_cu/gan_bang_chung.py
"""
import glob, json, os, re, random, collections
from difflib import SequenceMatcher

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUONG = 0.6
CUA_SO_ANH = 90
HAT_GIONG = 20261031
RA = os.path.join(GOC, "bang_chung")


def chuan(s):
    s = re.sub(r"\[\d\d:\d\d:\d\d\]", " ", s.lower())
    return re.findall(r"[^\W_]+", s)


def hms(s):
    h, m, x = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(x)


def doc_vtt(p):
    cue = []  # (giay_bat_dau, giay_het, text)
    cur = None
    for dong in open(p, encoding="utf-8").read().splitlines():
        m = re.match(r"(\d+:\d\d:\d\d[.,]\d+|\d\d:\d\d[.,]\d+) --> (\d+:\d\d:\d\d[.,]\d+|\d\d:\d\d[.,]\d+)", dong)
        if m:
            a, b = (x.replace(",", ".") for x in m.groups())
            a = a if a.count(":") == 2 else "00:" + a
            b = b if b.count(":") == 2 else "00:" + b
            cur = [hms(a), hms(b), []]
            cue.append(cur)
        elif cur is not None and dong.strip() and not dong.startswith(("WEBVTT", "Kind:", "Language:")):
            cur[2].append(re.sub(r"<[^>]+>", "", dong.strip()))
    return cue


def dung_luong_vtt(p):
    """-> (tokens, giay_theo_token). Bỏ cue lặp liền kề (phụ đề cuộn)."""
    toks, ts = [], []
    truoc = None
    for a, b, tx in doc_vtt(p):
        t = " ".join(tx)
        if t == truoc:
            continue
        truoc = t
        w = chuan(t)
        for i, x in enumerate(w):
            toks.append(x)
            ts.append(a + (b - a) * i / max(len(w), 1))
    return toks, ts


def dung_luong_zip(p):
    dong = []
    for l in open(p, encoding="utf-8").read().splitlines():
        m = re.match(r"\[(\d\d:\d\d:\d\d)\]\s*(.*)", l)
        if m:
            dong.append((hms(m.group(1)), chuan(m.group(2))))
    toks, ts = [], []
    for k, (a, w) in enumerate(dong):
        b = dong[k + 1][0] if k + 1 < len(dong) else a + 60
        b = min(b, a + 15 + 0.6 * len(w))  # tốc độ nói ~ 0,6 s/từ, tránh trải qua khoảng nghỉ
        for i, x in enumerate(w):
            toks.append(x)
            ts.append(a + (b - a) * i / max(len(w), 1))
    return toks, ts


class Luong:
    def __init__(self, toks, ts):
        self.t, self.ts = toks, ts
        self.vt = collections.defaultdict(list)

    def khop(self, q):
        """-> (do_giong, giay) cho 1 đoạn q (list từ)."""
        T, m = self.t, len(q)
        if m < 3 or len(T) < 3:
            return 0.0, None
        qs = set(q)
        qb = {(q[i], q[i + 1]) for i in range(m - 1)}
        n = len(T)
        h = [0] * (n + 1)
        for i in range(n):
            v = 1 if T[i] in qs else 0
            if i + 1 < n and (T[i], T[i + 1]) in qb:
                v += 2
            h[i + 1] = h[i] + v
        W = int(m * 1.5) + 5
        diem = [(h[min(i + W, n)] - h[i], i) for i in range(0, n, 1)]
        diem.sort(reverse=True)
        chon = []
        for d, i in diem:
            if d <= 0:
                break
            if all(abs(i - j) > m for j in chon):
                chon.append(i)
            if len(chon) >= 3:
                break
        tot = (0.0, None)
        for s in chon:
            a = max(0, s - 5)
            win = T[a:s + W + 5]
            sm = SequenceMatcher(None, q, win, autojunk=False)
            blocks = [b for b in sm.get_matching_blocks() if b.size]
            if not blocks:
                continue
            cov = sum(b.size for b in blocks) / m
            # chỉ tính khối ≥2 từ cho vị trí
            kh = [b for b in blocks if b.size >= 2] or blocks
            vi = a + kh[0].b
            if cov > tot[0]:
                tot = (cov, self.ts[vi])
        return tot


def tach_doan(s):
    out = []
    for p in re.split(r"\.\.\.|…", s):
        w = chuan(p)
        if len(w) >= 4:
            out.append(w)
    return out


def tim(luong, trich):
    doan = tach_doan(trich)
    if not doan:
        return 0.0, None
    dai = [d for d in doan if len(d) >= 6] or doan
    tot = (0.0, None)
    for d in dai:
        r = luong.khop(d)
        if r[0] > tot[0]:
            tot = r
    return tot


def lay_trich(o, duong=""):
    """Duyệt JSON: mọi trường 'trich' (chuỗi), phần tử 'trich_them' (chuỗi hoặc {cau})."""
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{duong}.{k}" if duong else k
            if k == "trich" and isinstance(v, str) and v.strip():
                out.append((p, v))
            elif k == "trich_them" and isinstance(v, list):
                for i, x in enumerate(v):
                    s = x if isinstance(x, str) else (x.get("cau") if isinstance(x, dict) else None)
                    if s:
                        out.append((f"{p}[{i}]", s))
            else:
                out += lay_trich(v, p)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += lay_trich(v, f"{duong}[{i}]")
    return out


def anh_theo_video():
    d = collections.defaultdict(list)
    for p in glob.glob(os.path.join(GOC, "so_tay/khung/*.jpg")):
        m = re.match(r"(.+)_(\d\d)(\d\d)(\d\d)\.jpg$", os.path.basename(p))
        if m:
            d[m.group(1)].append((int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4)), os.path.relpath(p, GOC)))
    return d


def vid(buoi):
    return buoi[-11:]


def main():
    anh = anh_theo_video()
    os.makedirs(RA, exist_ok=True)
    nguon = [("dap_an_v2", "thi/dap_an_v2/nhan"), ("phieu", "phieu"), ("moc", "moc")]
    buoi_ds = sorted({os.path.basename(f)[:-5] for _, d in nguon for f in glob.glob(os.path.join(GOC, d, "*.json"))})
    tk = []
    for buoi in buoi_ds:
        v = vid(buoi)
        vt = glob.glob(os.path.join(GOC, f"transcripts/phu_de/*_{v}.vtt"))
        zp = glob.glob(os.path.join(GOC, f"transcripts/zip_clean/*_{v}.txt"))
        L_vtt = Luong(*dung_luong_vtt(vt[0])) if vt else None
        L_zip = Luong(*dung_luong_zip(zp[0])) if zp else None
        ds = []
        for ten, d in nguon:
            f = os.path.join(GOC, d, buoi + ".json")
            if not os.path.exists(f):
                continue
            for truong, tr in lay_trich(json.load(open(f, encoding="utf-8"))):
                rv = tim(L_vtt, tr) if L_vtt else (0.0, None)
                rz = tim(L_zip, tr) if L_zip else (0.0, None)
                chon = None
                if rv[1] is not None and rv[0] >= NGUONG and rv[0] >= rz[0] - 0.1:
                    chon = (rv, "vtt")
                elif rz[1] is not None and rz[0] >= NGUONG:
                    chon = (rz, "zip_clean_noi_suy")
                elif rv[1] is not None and rv[0] >= NGUONG:
                    chon = (rv, "vtt")
                muc = {"nguon": ten, "truong": truong, "trich": tr}
                if chon is None:
                    muc.update(giay=None, do_giong=round(max(rv[0], rz[0]), 3), nguon_gio="khong_tim_thay",
                               url=None, anh=[])
                else:
                    (dg, gs), kind = chon
                    g = int(gs)
                    gan = sorted(((abs(t - g), t, p) for t, p in anh.get(v, []) if abs(t - g) <= CUA_SO_ANH))
                    muc.update(giay=g, do_giong=round(dg, 3), nguon_gio=kind,
                               url=f"https://www.youtube.com/watch?v={v}&t={g}s",
                               anh=[{"file": p, "giay": t, "lech": t - g} for _, t, p in gan[:3]])
                ds.append(muc)
                tk.append((buoi, muc))
        json.dump(ds, open(os.path.join(RA, buoi + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tong_hop(tk)


def tong_hop(tk):
    L = ["# Bằng chứng: câu trích ↔ giờ video ↔ ảnh", "",
         f"Sinh bởi `cong_cu/gan_bang_chung.py`; ngưỡng khớp {NGUONG}; cửa sổ ảnh ±{CUA_SO_ANH}s.", ""]

    def bang(nhom, tieu):
        c = collections.defaultdict(lambda: [0, 0, 0])
        for b, m in tk:
            k = nhom(b, m)
            c[k][0] += 1
            c[k][1] += m["giay"] is not None
            c[k][2] += bool(m["anh"])
        L.extend([f"## {tieu}", "", "| nhóm | số câu | có giờ | % | có ảnh | % |", "|---|---:|---:|---:|---:|---:|"])
        for k in sorted(c):
            n, g, a = c[k]
            L.append(f"| {k} | {n} | {g} | {100*g/n:.1f} | {a} | {100*a/n:.1f} |")
        L.append("")

    bang(lambda b, m: "TỔNG", "Toàn bộ")
    bang(lambda b, m: m["nguon"], "Theo nguồn")
    bang(lambda b, m: b[:7], "Theo tháng")
    bang(lambda b, m: m["nguon_gio"], "Theo kiểu nguồn giờ")
    nb = len({b for b, _ in tk})
    ba = len({b for b, m in tk if m["anh"]})
    L += [f"Số buổi: {nb}; buổi có ít nhất 1 câu gắn ảnh: {ba}.", ""]
    ok = [(b, m) for b, m in tk if m["giay"] is not None]
    random.Random(HAT_GIONG).shuffle(ok)
    L += ["## 10 mẫu ngẫu nhiên (hạt giống cố định) để mở video đối chiếu", ""]
    for b, m in ok[:10]:
        L += [f"- **{b}** · {m['nguon']} · `{m['truong']}` · khớp {m['do_giong']} ({m['nguon_gio']})",
              f"  - trích: {m['trich'][:220]}",
              f"  - video: {m['url']}",
              f"  - ảnh: {', '.join(a['file'] for a in m['anh']) or '(không)'}"]
    open(os.path.join(RA, "TONG_HOP.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
