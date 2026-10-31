# LUẬT KHOÁ — GIỮ / LẬT view H4 (chọn CHỈ trên tập học, buổi < 2026-07-01)

Khoá lúc 2026-10-31 12:35. Nhãn: **moi**. Chọn luật + K chỉ bằng buổi < 07/01; buổi ≥ 07/01 chỉ để đo (bảng dưới). Sẽ được chấm lại cùng bot v5 trên buổi live mới.

## Bộ luật (xét theo thứ tự; luật đầu tiên khớp thắng)

Đầu vào tại buổi N: **view** = hướng TĂNG/GIẢM gần nhất của người đó trước N (bỏ PHÂN VÂN); nhãn buổi N−1 (đích / mốc sai / độ chắc / tin tức); nến BTC đã đóng ≤ C_N (C = bat_dau_vn + phut); lịch tin công bố trước; Polymarket ≤ C_N. Định nghĩa điều kiện = bảng `DK` trong `hoc_v5/giu_lat/phan_tich.py` trên cột của `hoc_v5/giu_lat/dac_trung.py`.

1. Còn lại: **GIỮ view**.

## Kết quả (cùng buổi, % trùng nhãn 3 lớp)

| Lượt | n | Bộ luật | Giữ view | Luôn GIẢM | Luật từ trên xuống | Chép buổi trước |
|---|---|---|---|---|---|---|
| A gộp T3–T6 (trong tập học) | 75 | 58/75 = 77% | 58/75 = 77% | 30/75 = 40% | 52/75 = 69% | 58/75 = 77% |
| B: học 01–04 → thử 05+06 | 32 | 24/32 = 75% | 24/32 = 75% | 20/32 = 62% | 20/32 = 62% | 24/32 = 75% |
| B: học 01–05 → thử 06 | 19 | 13/19 = 68% | 13/19 = 68% | 10/19 = 53% | 12/19 = 63% | 13/19 = 68% |
| Trong mẫu: tập học T1–T6 | 102 | 78/102 = 76% | 78/102 = 76% | 46/102 = 45% | 67/102 = 66% | 77/102 = 75% |
| **Ngoài mẫu: tập kiểm T7–T10** | 77 | 50/77 = 65% | 50/77 = 65% | 49/77 = 64% | 47/77 = 61% | 46/77 = 60% |
|   kiểm 2026-07 | 21 | 13/21 = 62% | 13/21 = 62% | 9/21 = 43% | 14/21 = 67% | 11/21 = 52% |
|   kiểm 2026-08 | 19 | 11/19 = 58% | 11/19 = 58% | 11/19 = 58% | 4/19 = 21% | 11/19 = 58% |
|   kiểm 2026-09 | 18 | 14/18 = 78% | 14/18 = 78% | 15/18 = 83% | 15/18 = 83% | 13/18 = 72% |
|   kiểm 2026-10 | 19 | 12/19 = 63% | 12/19 = 63% | 14/19 = 74% | 14/19 = 74% | 11/19 = 58% |

## Băm

- định nghĩa (JSON sort_keys): `{"K": 0, "chon_tren": "buoi < 2026-07-01", "luat": [], "mac_dinh": "GIU_VIEW", "nhan": "moi", "ung_vien": ["vh_cham_rau", "vh_dong_1h4", "vh_dong_2h4", "vh_dong_dung_khung", "vh_dong_d1", "vh_ben_kia", "cham_dich", "cham_chang1", "vh_dong_vol", "h4_lon_nguoc", "h4_lon_nguoc_vol", "vol_h4_nguoc", "vol_d1_lon", "d1_nhan_chim_nguoc", "d1_cuoi_nguoc", "thu_hai", "dau_tuan", "dau_thang", "h4_sai_dai34", "h4_sai_e89", "h4_sai_e200", "d1_sai_dai34", "d1_sai_e89", "d1_sai_e200", "rsi_h4_cuc", "rsi_d1_cuc", "nguoc_pha_w1", "chum_h4", "tin_lon_giua", "tin_lon_sap24", "tin_lon_sap48", "cua_so_fomc", "pm_moi_truong_nguoc", "pm_7n_nguoc", "pm_nguoc", "truoc_nhac_tin", "truoc_cho_tin", "truoc_pv", "truoc_chac_thap", "truoc_doi_y", "truoc_chang1_nguoc", "tl_pha_nguoc", "tl_pha_nguoc_h4", "tl_pha_nguoc_d1", "tl_pha_nguoc_2nen", "tl_pha_nguoc_vol", "tl_pha_thuan"]}`
- sha256(định nghĩa) = `aedf78deec30e1f34f23bd764aa66178a10c25dec5665428fa8076f6c99c3528`
- sha256(dac_trung.py) = `551fc3c78143aaeebf7cdc8f888f768f2300cd76e9c1f64a35c711d8ecdcd948`
- sha256(phan_tich.py) = `d78dbb13806ce64beee15e10ce2f3fa6148a270fa0bf10a48795e5bcc01fda59`
