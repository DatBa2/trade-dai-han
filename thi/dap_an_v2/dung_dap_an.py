#!/usr/bin/env python3
"""Dựng đáp án v2 (định dạng phiếu) từ nhãn mù thi/dap_an_v2/nhan/ — theo QUY_TAC_PHAN_XU.md.

  thi/dap_an_v2/phieu/ = bản sao 180 phiếu v1; 77 buổi thi thay phần H4 bằng nhãn mới cuối buổi
  (huong, do_chac, dich, duong_di, vo_hieu_khi, han_gio, doi_y) + lệnh mới + trường tách (hanh_dong, chang_ke_tiep).
  3 buổi tranh chấp ngoài kỳ thi chỉ dùng để đo nhiễu, KHÔNG thay vào đáp án.
Ghi thêm PHAN_XU.md (v1 / v2 / Codex từng buổi) và KHOA_DAP_AN.md (sha256).
Cách dùng: python3 thi/dap_an_v2/dung_dap_an.py
"""
import datetime as dt, hashlib, json, shutil, sys
from pathlib import Path

DA = Path(__file__).resolve().parent
GOC = DA.parent.parent
sys.path[:0] = [str(GOC / "thi"), str(GOC / "cong_cu")]
import tao_ho_so as hs  # noqa: E402

VIET = {"TANG": "TĂNG", "GIAM": "GIẢM", "PHAN_VAN": "PHÂN VÂN", None: "—"}


def so(x):
    return f"{x:,.0f}".replace(",", ".") if isinstance(x, (int, float)) else str(x)


def cau_vo_hieu(v):
    """{'gia','khung','so_nen','chieu'} → câu kiểu phiếu: '2 nến H4 đóng trên 82.000' (cả bộ chấm cũ lẫn mới đọc được)."""
    if not isinstance(v, dict) or not isinstance(v.get("gia"), (int, float)):
        return None
    n = v.get("so_nen") or 1
    return f"{'2 nến' if n >= 2 else 'nến'} {v.get('khung') or 'H4'} đóng {'trên' if v.get('chieu') == 'dong_tren' else 'dưới'} {so(v['gia'])}"


def h4_v1(d):
    nd = d.get("nhan_dinh") or []
    return next((x for k in ("H4", "chung") for x in nd if x.get("khung") == k), None)


def main():
    thi = {b.ten for b in hs.ds_buoi() if b.ngay >= "2026-07-01"}
    ra = DA / "phieu"
    if ra.exists():
        shutil.rmtree(ra)
    ra.mkdir()
    for p in (GOC / "phieu").glob("2*.json"):
        shutil.copy2(p, ra / p.name)
    codex = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (GOC / "kiem_cheo" / "codex_phieu").glob("*.json")}
    dong = []
    for p in sorted((DA / "nhan").glob("*.json")):
        n = json.loads(p.read_text(encoding="utf-8"))
        d = json.loads((GOC / "phieu" / p.name).read_text(encoding="utf-8"))
        cu = h4_v1(d)
        cb = n["cuoi_buoi"]
        c = (codex.get(p.stem) or {}).get("cuoi_buoi", {}).get("huong_h4")
        dong.append((p.stem, p.stem in thi, cu.get("huong") if cu else None, cb["thien_huong_h4"], cb.get("do_chac"), c, n.get("kho")))
        if p.stem not in thi:
            continue
        moi = {"khung": "H4", "huong": cb["thien_huong_h4"], "do_chac": cb.get("do_chac"), "dich": n.get("dich_chinh"),
               "han": None, "han_gio": n.get("han_gio"), "vo_hieu_khi": cau_vo_hieu(n.get("vo_hieu")),
               "vo_hieu_cau_truc": n.get("vo_hieu"), "kich_ban_phu": None,
               "duong_di": n.get("duong_di") if len(n.get("duong_di") or []) >= 2 else None,
               "doi_y": (n.get("ly_do_doi_y") or "đổi ý giữa buổi") if n.get("doi_y_giua_buoi") else None,
               "ly_do": [], "trich": cb.get("trich"), "nhan_v1": cu.get("huong") if cu else None}
        nd = [x for x in d.get("nhan_dinh") or [] if x.get("khung") not in ("H4", "chung")]
        d["nhan_dinh"] = [moi] + nd
        d["lenh"] = [dict(l, trang_thai=l.get("trang_thai") or "de_xuat_moi") for l in n.get("lenh") or []]
        d.update(hanh_dong=n.get("hanh_dong"), chang_ke_tiep=n.get("chang_ke_tiep"), khung_lon_v2=n.get("khung_lon"),
                 pha_vo_gia=n.get("pha_vo_gia"), nguon_nhan="dap_an_v2 (Opus 5.5 rút mù 31/10)",
                 gia_btc_luc_noi=n.get("gia_btc_luc_noi") if n.get("gia_btc_luc_noi") else d.get("gia_btc_luc_noi"))
        (ra / p.name).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

    ex = [r for r in dong if r[1]]
    L = ["# Phân xử nhãn — đáp án v1 (Sonnet) vs v2 (Opus rút mù) vs Codex (cuối buổi)",
         f"Dựng lúc {dt.datetime.now():%Y-%m-%d %H:%M} VN · luật: `QUY_TAC_PHAN_XU.md` (chốt trước). Đáp án chính = v2.", "",
         f"- Buổi thi: {len(ex)} · v1 = v2: **{sum(r[2] == r[3] for r in ex)}/{len(ex)}**",
         f"- Có nhãn Codex: {sum(1 for r in dong if r[5])} buổi · v2 = Codex {sum(r[3] == r[5] for r in dong if r[5])} · "
         f"v1 = Codex {sum(r[2] == r[5] for r in dong if r[5])}", "",
         "| Buổi | Thi | v1 | v2 (độ chắc) | Codex | Đa số 3 bên | Ghi chú khó (v2) |", "|---|---|---|---|---|---|---|"]
    for ten, la_thi, v1, v2, dc, c, kho in dong:
        if v1 == v2 and (c is None or c == v2):
            continue
        ba = [x for x in (v1, v2, c) if x]
        da = next((x for x in set(ba) if ba.count(x) >= 2), "không có")
        L.append(f"| {ten} | {'✓' if la_thi else ''} | {VIET[v1]} | {VIET[v2]} ({dc}) | {VIET.get(c, '—')} | {VIET.get(da, da)} | "
                 f"{(kho or '').replace('|', '/')[:160]} |")
    L += ["", "_Chỉ liệt kê buổi có bất đồng. Buổi không liệt kê: v1 = v2 (và = Codex nếu có)._"]
    (DA / "PHAN_XU.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    bam = lambda q: hashlib.sha256(q.read_bytes()).hexdigest()
    tong = hashlib.sha256("".join(bam(q) for q in sorted(ra.glob("*.json"))).encode()).hexdigest()
    K = ["# Khoá đáp án v2 (sha256) — khoá TRƯỚC khi chấm bot theo v2", f"Khoá lúc {dt.datetime.now():%Y-%m-%d %H:%M} VN", "",
         f"- `thi/dap_an_v2/phieu/` ({len(list(ra.glob('*.json')))} file, băm gộp theo tên): `{tong}`",
         f"- `thi/dap_an_v2/dung_dap_an.py`: `{bam(Path(__file__))}`",
         f"- `thi/dap_an_v2/QUY_TAC_PHAN_XU.md`: `{bam(DA / 'QUY_TAC_PHAN_XU.md')}`", "", "| Nhãn mù | sha256 |", "|---|---|"]
    K += [f"| {q.name} | `{bam(q)}` |" for q in sorted((DA / "nhan").glob("*.json"))]
    (DA / "KHOA_DAP_AN.md").write_text("\n".join(K) + "\n", encoding="utf-8")
    print(f"✓ {len(ex)} buổi thi thay nhãn · PHAN_XU.md · KHOA_DAP_AN.md (băm gộp {tong[:16]})")


if __name__ == "__main__":
    main()
