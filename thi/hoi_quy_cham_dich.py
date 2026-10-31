#!/usr/bin/env python3
"""Hồi quy bộ chấm: cham_dich CŨ (thi/_snapshot_v3_chan_doan/cham_dich.py — chỉ đọc mã, chạy trên dữ liệu du_lieu/ hiện tại)
vs cham_dich MỚI (cong_cu/cham_dich.py) trên mọi phiếu phieu/ (hoặc thư mục truyền vào).

Ba phép so (đều hạn của view như main() cũ; bảng 3 dùng hạn cố định 336 giờ như bài thi):
  1. Toàn bộ thay đổi: cũ (C = giờ trong tên phiếu / 10:00 VN) → mới (C = kết thúc live theo gio_live.tsv khi có).
  2. Chỉ do bộ chấm: cùng C cũ cho cả hai bên → tách ảnh hưởng của P0-2/3/4 khỏi việc đổi C.
  3. Hạn cố định 336 giờ, cùng C mới cho cả hai bên (thước của bài thi).
Cách dùng: python3 thi/hoi_quy_cham_dich.py [thư mục phiếu=phieu] [--vi-du N] [--bai-lam]
  --bai-lam: thư mục là bài làm của bot → chuẩn hoá bằng thi/cham.py::chuan_bai như lúc chấm thi.
"""
import datetime as dt, json, os, sys, types
from bisect import bisect_left
from collections import Counter
from pathlib import Path

THI = Path(__file__).resolve().parent
GOC = THI.parent
sys.path.insert(0, str(GOC / "cong_cu"))
os.environ.pop("HAN_CO_DINH", None)
import cham_dich as moi  # noqa: E402


def nap_cu():
    """Nạp mã snapshot (không sửa file); __file__ giả trong cong_cu/ để GOC = gốc dự án → đọc du_lieu/ hiện tại."""
    src = (THI / "_snapshot_v3_chan_doan" / "cham_dich.py").read_text(encoding="utf-8")
    m = types.ModuleType("cham_dich_cu")
    m.__file__ = str(GOC / "cong_cu" / "_cham_dich_cu_ao.py")
    exec(compile(src, str(THI / "_snapshot_v3_chan_doan" / "cham_dich.py"), "exec"), m.__dict__)
    return m


def bang(cap, tieu_de):
    c = Counter((a, b) for a, b in cap if a != b)
    L = [f"### {tieu_de}", f"{len(cap)} phiếu · đổi kết quả: **{sum(c.values())}**", "| Chuyển | Số phiếu |", "|---|---|"]
    L += [f"| {a} → {b} | {n} |" for (a, b), n in c.most_common()]
    return L


def main():
    a = sys.argv[1:]
    thu_muc = GOC / (a[0] if a and not a[0].startswith("--") else "phieu")
    so_vd = int(a[a.index("--vi-du") + 1]) if "--vi-du" in a else 5
    cu = nap_cu()
    that = moi.gio_live()
    chuan = (lambda d: d)
    if "--bai-lam" in a:
        import cham as ch  # thi/cham.py (đặt HAN_CO_DINH=336 khi nạp → bỏ lại ngay)
        os.environ.pop("HAN_CO_DINH", None)
        chuan = lambda d: ch.chuan_bai(d)[0]
    hang = []
    for p in sorted(thu_muc.glob("2*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        d = dict(chuan(d), ngay=d.get("ngay") or p.stem[:10])
        gio = __import__("re").search(r"_(\d{2})(\d{2})_", p.name)
        C_cu = dt.datetime.fromisoformat(d["ngay"]) + (dt.timedelta(hours=int(gio[1]), minutes=int(gio[2])) if gio else dt.timedelta(hours=10)) - moi.VN
        C_moi, co_that = moi.moc_C(p, d, that)
        os.environ.pop("HAN_CO_DINH", None)
        kc, lc = cu.cham(d, C_cu)
        km_cungC, _ = moi.cham(d, C_cu)
        km, lm = moi.cham(d, C_moi)
        r = moi.cham_chi_tiet(d, C_moi)
        os.environ["HAN_CO_DINH"] = "336"
        kc336, _ = cu.cham(d, C_moi)
        km336, _ = moi.cham(d, C_moi)
        os.environ.pop("HAN_CO_DINH", None)
        i0 = bisect_left(cu.T1, C_cu)
        gia_cu = (cu.H1[i0 - 1][3] if i0 else cu.H1[0][3]) if i0 < len(cu.H1) else None
        hang.append(dict(ten=p.stem, kc=kc, lc=lc, km=km, lm=lm, km_cungC=km_cungC, kc336=kc336, km336=km336,
                         C_cu=C_cu, C_moi=C_moi, co_that=co_that, gia_cu=gia_cu, r=r, d=d,
                         vh=moi.chon_view(d).get("vo_hieu_khi")))
    L = [f"# Hồi quy cham_dich cũ → mới ({len(hang)} phiếu, `{thu_muc.relative_to(GOC)}`)", ""]
    L += bang([(h["kc"], h["km"]) for h in hang], "1. Toàn bộ (C cũ → C kết thúc live; bộ chấm cũ → mới; hạn của view)")
    L += [""] + bang([(h["kc"], h["km_cungC"]) for h in hang], "2. Chỉ do bộ chấm (cùng C cũ; hạn của view)")
    L += [""] + bang([(h["kc336"], h["km336"]) for h in hang], "3. Hạn cố định 336 giờ, cùng C mới (thước bài thi)")
    tong = lambda k: Counter(h[k] for h in hang)
    L += ["", "### Phân bố kết quả (hạn của view)", "| Kết quả | Cũ | Mới (cùng C cũ) | Mới (C mới) |", "|---|---|---|---|"]
    for k in sorted(set(tong("kc")) | set(tong("km")) | set(tong("km_cungC"))):
        L.append(f"| {k} | {tong('kc')[k]} | {tong('km_cungC')[k]} | {tong('km')[k]} |")
    L += ["", f"Số phiếu đổi C (có giờ live thật): {sum(h['co_that'] for h in hang)} · vô hiệu có câu nhưng chưa hiểu: "
          f"{sum(h['r']['vo_hieu_chua_hieu'] for h in hang)} · khung điều kiện vô hiệu: "
          f"{dict(Counter((h['r']['dieu_kien'] or {}).get('khung') for h in hang if h['r']['dieu_kien'] and h['r']['dieu_kien']['da_hieu']))}"
          f" · 2 nến: {sum(1 for h in hang if h['r']['dieu_kien'] and h['r']['dieu_kien'].get('so_nen') == 2)}"]
    # ví dụ: mọi phiếu đổi ở ít nhất 1 phép so; ưu tiên phép 2 (chỉ do bộ chấm), rồi 3 (thước bài thi), rồi 1
    L += ["", f"### Ví dụ (tối đa {so_vd}; ưu tiên ca đổi do bộ chấm khi giữ nguyên C)"]
    vd = [h for h in hang if h["kc"] != h["km_cungC"]] + [h for h in hang if h["kc336"] != h["km336"]] + \
         [h for h in hang if h["kc"] != h["km"]]
    da = []
    for h in vd:
        if h["ten"] not in [x["ten"] for x in da]:
            da.append(h)
    for h in da[:so_vd]:
        r = h["r"]
        r336 = moi.cham_chi_tiet(h["d"], h["C_moi"], 336)
        L.append(f"- **{h['ten']}** — (1) {h['kc']} → {h['km']} · (2) cùng C cũ: {h['kc']} → {h['km_cungC']} · "
                 f"(3) 336 giờ: {h['kc336']} → {h['km336']} ({r336['luc'] or '—'}, {r336['su_kien'] or '—'}) · "
                 f"C cũ {h['C_cu'] + moi.VN:%d/%m %H:%M} → C mới {h['C_moi'] + moi.VN:%d/%m %H:%M} VN · "
                 f"giá cũ (close H1 chứa C cũ) {h['gia_cu']} → giá mới (close 5m đã đóng ≤ C mới) {r['gia_tham_chieu']} · "
                 f"hướng {r['huong']} · đích {r['dich']} · mốc sai {r['moc_sai']} {(r['dieu_kien'] or {}).get('khung') or ''}"
                 f"{' ×2 nến' if (r['dieu_kien'] or {}).get('so_nen') == 2 else ''} · SL {r['sl']} · hạn view {r['han_view']['gio']} giờ"
                 f" · vô hiệu: “{h['vh']}”")
    print("\n".join(L))


if __name__ == "__main__":
    main()
