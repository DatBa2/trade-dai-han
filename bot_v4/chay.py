#!/usr/bin/env python3
"""Chạy bot v4 cho 1 năm × 1 rổ → bot_v4/ket_qua/<nam>_<ro>/{lenh.csv, von.csv, quyet_dinh.csv, tom_tat.json}.

    python3 bot_v4/chay.py --nam 2024|2025|2026 [--ro 6|BTC] [--du-lieu THU_MUC] [--ra THU_MUC]

Luật nằm hết trong bot_v4/dong_co.py (TK = bot_v4/THIET_KE.md, DG = bot_v4/DIEN_GIAI.md).
"""
import argparse
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent
sys.path.insert(0, str(GOC))
import dong_co  # noqa: E402

RO = {"6": list(dong_co.TAI_SAN), "BTC": ["BTC"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nam", type=int, required=True, choices=[2024, 2025, 2026])
    ap.add_argument("--ro", default="6", choices=sorted(RO))
    ap.add_argument("--du-lieu", default=None, help="thư mục CSV nến (mặc định bot_v4/du_lieu)")
    ap.add_argument("--ra", default=None, help="thư mục ghi (mặc định bot_v4/ket_qua/<nam>_<ro>)")
    a = ap.parse_args()
    ds = RO[a.ro]
    du = dong_co.nap_ro(ds, a.du_lieu)
    kq = dong_co.chay(ds, a.nam, du_lieu=du)
    ra = Path(a.ra) if a.ra else GOC / "ket_qua" / f"{a.nam}_{a.ro}"
    tt = dong_co.ghi_ket_qua(kq, ra)
    pf = tt["he_so_ln"]
    print(f"{a.nam} rổ {a.ro}: lãi {tt['lai_usd']:+.2f}$ ({tt['lai_pct']:+.2%}) | lệnh khớp {tt['so_lenh']} "
          f"(huỷ {tt['so_lenh_huy']}) | thắng {tt['ti_le_thang']:.1%} | R TB {tt['R_tb']:+.3f} | "
          f"sụt giảm max {tt['sut_giam_max']:.2%} | hệ số LN {pf if pf is None else round(pf, 3)} → {ra}")


if __name__ == "__main__":
    main()
