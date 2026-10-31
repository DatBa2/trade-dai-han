# Kiểm biến thể đã khoá bằng ảnh chart

Biến thể khoá: `rau|3|dai|nhieu_cham` (`CHON.md`). Ảnh KHÔNG dùng để đổi biến thể; phần "Đề xuất" ở cuối là để Claude quyết.
Giá đường trên ảnh đọc bằng pixel (nội suy theo trục giá, sai số ước ~0,1–0,3%); dữ liệu máy là OKX spot, ảnh là Binance perp (lệch ~0,1%).

## 1. Khung hình mới (chụp theo `CAN_ANH_dot1.tsv`, ±10 giây) — đã đọc 9 ảnh khung H4/D1
| Ảnh | Người đó nói | Trên ảnh | So với biến thể khoá |
|---|---|---|---|
| `vg80vm31RLM_001239` (01-13, D1) | trendline hỗ trợ "lần này" bị thủng | Không có trendline; chỉ cọ vàng vẽ đỉnh/đáy, đường cam FIBO 0.5 | Không kiểm được |
| `pbr4y9qP1Ys_003118` (03-05, H4) | "cây H4 này đã break ra khỏi trend line" | Không thấy trendline (chỉ Fibo mở rộng 1/1.618, "TP flag") | Không kiểm được giá; trạng thái máy `pha_roi_test_lai` (đường 71.746 → 70.969 bị phá 03-04) = khớp "vừa phá" |
| `-jRLufOuVEE_003242` (03-09, H4) | hỗ trợ H4 | **Hỗ trợ tăng dài** neo râu đáy 60.000 (06/02) → ~62,5k (24/02) → ~63,0k (28/02), giá đường lúc nói ≈ **64,56k**, giá 67,3k ở trên | **Lệch**: đường chính máy 65.052 → 66.543 (y 66.774, +3,4%). Đường người đó CÓ trong tập (60.000 → 62.500, y 64.209, −0,55%) nhưng chỉ 3 chạm < 4 chạm của đường ngắn. `rau\|3\|dai\|cuc_tri` (neo đáy thấp nhất) khớp −0,49% |
| `byYCWvbkZyU_002026` (03-25, D1) | "vùng 67.000… trụ lại" | Không có trendline (MA + Fibo) | Không kiểm được |
| `35w3e47m3wY_001020` (03-26, D1) | hỗ trợ D1 | Chart phóng quá to, 1 đường xanh dốc đứng, không đọc được | Không kiểm được |
| `KbxhGxmcYwg_000854` (03-30, D1) | phá rồi test lại | **Hỗ trợ tăng** neo râu đáy ~59,9k (06/02) qua ~63k (cuối 02), ≈ **67,6k** lúc nói; giá 66,97k đã nằm DƯỚI đường (gãy, đang test lại từ dưới) | **Lệch**: máy không còn đường hỗ trợ D1 nào (đường 60.000 → 62.500 đã gãy > 48h trước nên hết hiệu lực). Lỗi do cửa sổ 48h sau phá quá ngắn |
| `nN446WPRxPo_002238` (04-20, H4) | "đi khá nhịp nhàng theo đường trend này" | **Hỗ trợ tăng ngắn, dốc** từ đáy ~66,6k (05/04) qua ~67,7k (07/04), ~70,5k (13/04), ≈ **73,6k** lúc nói | **Lệch**: đường chính máy 62.500 → 66.000 (10 chạm, y 67.992, −7,6%). Đường người đó CÓ trong tập (66.607 → 67.730, y 73.827, +0,35%); biến thể `gan_gia` chọn đúng nó |
| `UmnCq7p4NlU_000946` (06-09, H4) | hỗ trợ H4 chưa phá | Không có trendline (Fibo thoái lui + hộp vàng 61–61,7k) | Không kiểm được |
| `AG126RfNCk4_001812` (04-21, H4) | kênh/hỗ trợ ~67k | Không có trendline (MA, đường cam) | Không kiểm được |

→ 9 ảnh: 6 không có/không đọc được trendline (người đó **nói** trendline nhưng không vẽ — "nhìn biết luôn"), 3 có đường: **0/3 khớp đường chính**, 2/3 đường người đó có trong tập của biến thể.

## 2. Mọi tham chiếu ảnh (10 trong `tham_chieu_anh.tsv` + 3 ảnh mới có đường) × vài biến thể
Lệch % giá đường chính so với giá đọc trên ảnh (`*` = ≤ 0,5%). Cột cuối: đường gần nhất trong TẬP của biến thể khoá.

| Ảnh | khoá `rau\|3\|dai\|nhieu_cham` | `rau\|3\|ngan\|nhieu_cham` | `rau\|3\|ngan\|gan_gia` | `rau\|3\|ngan\|cuc_tri` | `rau\|3\|dai\|cuc_tri` | `rau\|2\|ngan\|gan_gia` | tập (khoá) |
|---|---|---|---|---|---|---|---|
| 02-27 H4 kháng cự | +2,82 | +2,82 | +0,62 | +3,51 | +7,91 | +0,62 | 0,09 |
| 03-12 H4 kháng cự | −1,06 | −0,21* | −0,21* | −0,21* | −1,17 | −0,21* | 0,06 |
| 05-27 H4 kháng cự (đã gãy ~3 ngày) | +3,25 | +3,25 | +2,81 | +6,54 | +6,54 | +2,81 | 2,81 |
| 06-25 D1 hỗ trợ (gần ngang, dốc xuống) | +3,09 | +8,57 | +8,03 | +8,57 | +8,57 | +8,03 | 3,09 |
| 08-18 D1 kháng cự | −0,30* | −1,08 | +0,07* | +13,15 | −1,63 | +0,07* | 0,07 |
| 08-18 D1 hỗ trợ | −0,07* | −0,07* | +0,41* | +0,41* | +0,41* | +0,41* | 0,07 |
| 08-18 H4 kháng cự | −0,10* | −0,10* | −0,60 | −0,71 | +10,92 | −0,56 | 0,01 |
| 08-18 H4 hỗ trợ | +0,55 | +0,73 | +0,89 | +0,86 | +0,61 | +1,40 | 0,02 |
| 09-04 H4 kháng cự (vừa phá) | +0,18* | +0,18* | +1,25 | −0,83 | −0,83 | +1,57 | 0,18 |
| 10-02 H4 kháng cự (vừa phá) | −0,08* | −0,08* | +1,92 | −0,08* | −0,08* | +1,92 | 0,06 |
| 03-09 H4 hỗ trợ (mới) | +3,43 | +3,43 | +3,20 | +3,60 | −0,49* | +3,20 | 0,41 |
| 03-30 D1 hỗ trợ (mới, đã gãy > 48h) | – | – | – | – | – | – | – |
| 04-20 H4 hỗ trợ (mới) | −7,58 | −7,05 | +0,35* | −4,29 | −7,26 | +0,35* | 0,35 |
| **Khớp / 13** | **5** | 5 | 4 | 3 | 3 | 4 | **10 trong tập** |

## 3. Kết luận
- Trên ảnh, biến thể khoá khớp đường chính **5/13**, ngang `rau|3|ngan|nhieu_cham`, hơn các biến thể khác (3–4/13). Ảnh **không** cho thấy biến thể nào khác khớp rõ hơn → giữ khoá.
- Cách VẼ của máy đúng hướng: neo râu, nối râu đỉnh/đáy; đường người đó vẽ nằm trong tập đường của biến thể khoá ở **10/13** ảnh (lệch ≤ 0,41%). Phần trượt là **chọn đường nào làm đường chính**: lúc người đó dùng đường dài nhiều chạm (08-18, 10-02), lúc đường ngắn dốc sát giá (04-20), lúc đường từ đáy cực trị (03-09).
- 2 lần trượt do giới hạn mô hình, không do chọn: đường đã gãy > 48h người đó vẫn dùng (03-30, 05-27); hỗ trợ gần ngang hơi dốc xuống (06-25).

## 4. Đề xuất (KHÔNG áp dụng — để Claude quyết)
1. Giữ `rau|3|dai|nhieu_cham` làm đường chính, nhưng cho bot đọc thêm **đường gần giá nhất** trong cùng tập (đã có sẵn: `duong_hieu_luc()` trả mọi đường; `su_kien.csv` có `so_duong`). Đây không phải tiêu chí mới mà là đúng cách người đó dùng: hai loại đường cùng xuất hiện trên ảnh (04-20, 08-18).
2. Kéo dài hiệu lực sau phá cho đường **D1** (48h → ~5–7 ngày) để bắt "phá rồi test lại" nhiều ngày sau (03-30). Cần khai báo thành biến thể mới và chạy lại hiệu chỉnh trước khi dùng.
3. Cho phép hỗ trợ/kháng cự **gần ngang** (độ dốc ngược ≤ ~0,5%) — có 1 ảnh (06-25), người đó tự nói "không đánh giá cao trendline này" → ưu tiên thấp.
