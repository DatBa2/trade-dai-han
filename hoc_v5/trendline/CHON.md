# Biến thể trendline ĐÃ KHOÁ

BIEN_THE_KHOA: `rau|3|dai|nhieu_cham`

Sinh bởi `python3 hoc_v5/trendline/hieu_chinh.py --ghi-chon` lúc 2026-10-31 12:37 (VN). Luật so khớp + luật chọn khai báo trước trong `BIEN_THE.md`; chọn THUẦN theo độ khớp với đường người đó vẽ/nhắc (không dùng volume, không tiêu chí riêng).

## Dữ liệu so
- Lần nhắc trendline (mọi khung) đọc được giờ: 247 từ nhãn `hoc_v5/nhan/` + 10 đọc từ ảnh chart (`tham_chieu_anh.tsv`). So được (khung H4/D1, loại kháng cự giảm / hỗ trợ tăng, hoặc kênh có giá): 88.
- Có giá đường để so giá: 33; có trạng thái để so: 80.
- Lần nhắc cần ảnh thêm (không ảnh, neo mơ hồ): 139 → `CAN_ANH.tsv`.

## Bảng khớp (toàn bộ 180 buổi), 10 biến thể đầu theo luật chọn
| # | Biến thể | Khớp giá đường chính ≤0,5% | Khớp giá (có trong tập) | Khớp trạng thái | TB số đường |
|---|---|---|---|---|---|
| 1 | `rau\|3\|dai\|nhieu_cham` | 13/33 (39%) | 24/33 (73%) | 60/80 (75%) | 17.4 |
| 2 | `rau\|3\|dai\|gan_gia` | 11/33 (33%) | 24/33 (73%) | 55/80 (69%) | 17.4 |
| 3 | `rau\|3\|ngan\|dai_nhat` | 10/33 (30%) | 23/33 (70%) | 59/80 (74%) | 8.2 |
| 4 | `rau\|3\|ngan\|nhieu_cham` | 10/33 (30%) | 23/33 (70%) | 57/80 (71%) | 8.2 |
| 5 | `rau\|3\|ngan\|cuc_tri` | 10/33 (30%) | 23/33 (70%) | 57/80 (71%) | 8.2 |
| 6 | `rau\|2\|dai\|nhieu_cham` | 10/33 (30%) | 25/33 (76%) | 56/80 (70%) | 26.0 |
| 7 | `rau\|3\|ngan\|gan_gia` | 10/33 (30%) | 22/33 (67%) | 54/80 (68%) | 8.3 |
| 8 | `rau\|2\|ngan\|nhieu_cham` | 10/33 (30%) | 24/33 (73%) | 52/80 (65%) | 13.2 |
| 9 | `rau\|2\|ngan\|dai_nhat` | 9/33 (27%) | 24/33 (73%) | 60/80 (75%) | 13.3 |
| 10 | `rau\|2\|ngan\|cuc_tri` | 9/33 (27%) | 24/33 (73%) | 59/80 (74%) | 13.3 |
| … | kém nhất `than\|2\|dai\|cuc_tri` | 3/33 | 16/33 | 56/80 | 9.7 |

Bảng đủ 32 biến thể × 3 phạm vi: `khop_bien_the.tsv`; chi tiết từng lần nhắc với biến thể khoá: `khop_chi_tiet.tsv`.

## Kiểm theo thời gian (chọn trên buổi trước 07-01 → đo trên buổi từ 07-01)
| Biến thể | Chọn trên | Trước 07-01: giá chính / trạng thái | Từ 07-01: giá chính / trạng thái |
|---|---|---|---|
| `rau\|3\|ngan\|cuc_tri` | trước 07-01 | 3/16 (19%) / 30/39 (77%) | 7/17 (41%) / 27/41 (66%) |
| `rau\|3\|dai\|nhieu_cham` | toàn bộ (KHOÁ) | 2/16 (12%) / 31/39 (79%) | 11/17 (65%) / 29/41 (71%) |
| (tham khảo) tốt nhất nếu chọn thẳng trên từ 07-01 | — | — | 65% giá chính |

## Volume khi phá (chỉ ghi, không dùng để chọn)
| Người đó gọi | vol nến phá < 0,8 TB20 | 0,8–1,2 | ≥ 1,2 | máy không thấy lần phá |
|---|---|---|---|---|
| pha_that | 8 | 3 | 14 | 16 |
| pha_gia | 0 | 0 | 0 | 0 |

Lời người đó nói về volume (trường `nen_volume`) × tỉ lệ volume máy đo:
| Lời | < 0,8 | 0,8–1,2 | ≥ 1,2 | không thấy phá |
|---|---|---|---|---|
| manh | 1 | 0 | 3 | 0 |
| yeu | 1 | 1 | 0 | 3 |
| ? | 4 | 1 | 1 | 4 |

Mọi lời người đó tả volume nến H4 (trường `nen_volume` cấp buổi, khung H4) × tỉ lệ volume máy đo (lớn hơn của 2 nến H4 đã đóng gần nhất / TB20):
| Lời | < 0,8 | 0,8–1,2 | ≥ 1,2 |
|---|---|---|---|
| manh | 6 | 8 | 6 |
| yeu | 5 | 1 | 2 |
| ? | 10 | 3 | 10 |

Chi tiết: `volume_pha.tsv`, `volume_loi_h4.tsv`.

<!-- GHI TAY -->

## Ghi tay (31/10, sau khi khoá — không đổi biến thể)
- **Lý do chọn**: đúng luật khai báo trước (tỉ lệ khớp giá đường chính cao nhất, hoà thì trạng thái). `rau|3|dai|nhieu_cham` đứng đầu cả giá chính (13/33) lẫn trạng thái (60/80) trên toàn bộ 180 buổi. Nhóm dẫn đầu đều là **neo râu** (7/7 biến thể đầu), **fractal 3-3** nhỉnh hơn 2-2 — khớp mô tả ảnh "nối râu đỉnh → râu đỉnh".
- **Chỗ yếu chính là chọn đường chính, không phải tìm đường**: đường người đó vẽ CÓ trong tập đường của biến thể ở 24/33 lần (73%), nhưng đường chính chỉ trúng 13/33 (39%). Ảnh cho thấy người đó lúc chọn đường dài nhiều chạm, lúc chọn đường ngắn dốc sát giá (04-20), lúc chọn đường từ đáy/đỉnh cực trị (03-09) — không luật `chon` đơn nào bắt hết (xem `KIEM_ANH.md`).
- **Không tổng quát ngược về đầu năm**: trước 07-01 chỉ 2/16 (tỉ lệ thấp ở mọi biến thể, tốt nhất 3/16); từ 07-01 11/17. Chọn trên trước 07-01 (`rau|3|ngan|cuc_tri`) → từ 07-01 được 7/17 (41%) giá chính, 27/41 trạng thái. Nửa đầu năm người đó ít vẽ trendline (1–3% mốc), giá nhãn hay là số tròn nghìn (66.000, 67.000, 68.000) nên ngưỡng 0,5% khắt khe; nửa sau có ảnh chart đọc giá chính xác hơn.
- **Giới hạn của mô hình** (không sửa vì đã khoá): (1) đường hết hiệu lực 48h sau phá → bỏ sót lúc người đó còn nhắc đường đã gãy nhiều ngày (03-30 D1, 05-27 H4); (2) chỉ có hỗ trợ TĂNG / kháng cự GIẢM → đường hỗ trợ gần ngang hơi dốc xuống (06-25 D1) không biểu diễn được; (3) kênh song song, khung H1/M15/W1 không so.
- **Volume**: chỉ 1 nhãn "phá giả" nên không kiểm được phá giả ↔ volume thấp. Với "phá thật" người đó gọi, nến phá máy tìm ra có volume ≥ 1,2×TB20 ở 14/25 lần, < 0,8× ở 8/25. Lời tả volume nến H4 ("volume to/khủng/bật volume" vs "không có volume/yếu") KHÔNG tách rõ theo tỉ lệ volume/TB20 của 2 nến H4 gần nhất → người đó nhiều khi nói volume khung nhỏ hoặc cả đoạn, nên cột `pha_vol` chỉ để tham khảo.

## Sửa sau khoá (31/10, Claude quyết — áp dụng đề xuất 2 của `KIEM_ANH.md`; biến thể khoá GIỮ NGUYÊN)
- `cong_cu/trendline.py`: `HIEU_LUC_SAU_PHA` thành theo khung `{"H4": 12, "D1": 84}` nến H4 → đường **D1 đã phá thật vẫn được LIỆT KÊ tối đa 14 ngày** sau nến phá (hết sớm hơn nếu close H4 quay lại phía cũ); H4 giữ 48h như cũ.
- Mỗi đường trả thêm `da_pha_ngay` (số ngày từ nến phá thật), `test_lai` (bool), `ghi_chu_pha` ("đã phá cách đây X ngày, đã/chưa test lại").
- Đường CHÍNH không đổi so với lúc khoá: `chon_chinh` chỉ xét đường chưa phá thật hoặc phá thật < 48h (`duoc_chon_chinh`). Vì vậy số khớp của biến thể khoá không đổi (giá chính 13/33, tập 24/33, trạng thái 60/80); TB số đường liệt kê 17,4 → 17,8. `hieu_chinh.py`: nhãn "vừa phá" chỉ khớp khi lần phá thật ≤ 48h.
- Kiểm thử: `hoc_v5/trendline/kiem_tra.py` PASS (thêm 6 mục D1 sau phá; cắt cụt 26 thời điểm × 4 biến thể lệch 0); `bot_v5/kiem_tra_ngu_canh.py` PASS (exit 0, không FAIL). `su_kien.csv` chạy lại (đường chính không đổi, cột `so_duong` D1 tăng).
- sha256 `cong_cu/trendline.py`: trước sửa `44bf19575f1b2aa21fc6edd881753625a41d8087c9ade895ce2ceb38ae948512` → sau sửa `55a4fbdecaec5034b7b54d526519116c011a9967c411cd8aacd8cb9c0c81ec87`.
