# Biến thể trendline — khai báo TRƯỚC khi so với trendline người đó vẽ

Ghi lúc 2026-10-31 ~11:50 (VN), trước khi chạy bất kỳ so khớp nào với `hoc_v5/nhan/*.json` hay ảnh.
Mã: `cong_cu/trendline.py` (hàm `danh_sach_bien_the()` sinh đúng lưới dưới đây, tên biến thể = `neo|k|tuoi|chon`).

## Căn cứ từ sổ tay (chỉ dùng những gì người đó làm/nói)
- Phá = "nến H4 phải đóng cửa vượt qua khỏi trendline" [10-19]; "râu không tính" → phá xét bằng CLOSE H4.
- "Hai cây nến H4 vượt qua thì mới an toàn" → ghi riêng phá 1 nến / 2 nến liên tiếp.
- Trendline mạnh = được test nhiều lần [08-27] → đếm số chạm.
- Ảnh: nối **râu đỉnh cao nhất → râu đỉnh thấp hơn kế tiếp**, kéo dài sang phải (H4 02-27, 03-12); tam giác/cờ nối râu.
- Người đó xét nến KÈM VOLUME khi phá (bổ sung của user) → mỗi sự kiện phá ghi tỉ lệ volume nến phá / TB 20 nến H4 đã
  đóng trước đó. Volume CHỈ được ghi lại, KHÔNG dùng để lọc hay chọn biến thể.

## Phần cố định (mọi biến thể)
| Tham số | Giá trị | Ghi chú |
|---|---|---|
| Khung đường | H4, D1 | OKX spot `bot_v4/du_lieu/BTC_4H.csv`, `BTC_1D.csv`; x của nến = giờ MỞ (UTC) |
| Loại | `khang_cu_giam` (≥2 đỉnh fractal, neo sau THẤP hơn neo trước), `ho_tro_tang` (≥2 đáy fractal, neo sau CAO hơn) | đường thẳng theo thời gian (thang giá tuyến tính) |
| Hợp lệ giữa 2 neo | không close nào (khung của đường) vượt đường; dung sai `TOL_XUYEN` = 0 | tham số được |
| Pivot | fractal `chi_bao.fractal` (k trái, k phải); chỉ dùng khi nến i+k đã đóng | nhân quả |
| Chạm | râu (high với kháng cự, low với hỗ trợ) trong ±0,3% giá đường, close không vượt; cụm nến chạm liền nhau = 1 lần; 2 neo tính là chạm | |
| Phá | close H4 vượt đường (kể cả đường D1, giá trị đường tính tại giờ mở nến H4) | |
| Phá 2 nến | nến H4 kế tiếp cũng đóng vượt | |
| Phá giả | trong 3 nến H4 sau nến phá có close quay lại phía cũ → `pha_gia`, đường vẫn còn | |
| Phá thật | 3 nến H4 sau nến phá không quay lại → `da_pha` tính từ nến phá | |
| Test lại | sau phá thật, râu chạm đường (±0,3%) mà close vẫn ở phía mới → `pha_roi_test_lai` | |
| Hết hiệu lực | 12 nến H4 (48 giờ) sau nến phá thật, hoặc close quay lại phía cũ sau phá thật; neo 1 quá tuổi | trong 48h sau phá, đường vẫn được xét làm đường chính (để bắt "vừa phá", "phá rồi test lại") |
| Vừa phá | trạng thái `vua_pha_1n`/`vua_pha_2n` (chưa đủ 3 nến xác nhận) hoặc `da_pha`/`pha_roi_test_lai` (luôn ≤ 48h vì hết hiệu lực sau 48h) | dùng khi so trạng thái |
| Đường sinh ra đã bị xuyên | bỏ (có close H4 vượt đường trước lúc pivot neo 2 được xác nhận) | |

(Sửa 31/10 ~12:05, vẫn TRƯỚC khi so với nhãn/ảnh: "hết hiệu lực" 18 nến → 12 nến cho trùng cửa sổ "vừa phá" 48h; lý do: thử tại 02-27 thấy đường đã phá nhiều ngày vẫn được chọn làm đường chính.)
(User bổ sung 31/10: hiệu chỉnh trên TOÀN BỘ 180 buổi khi có nhãn, kèm bảng kiểm theo thời gian: chọn trên buổi < 2026-07-01 → đo trên buổi ≥ 2026-07-01.)
| Volume | v(nến phá) / TB v của 20 nến H4 đóng trước nó | chỉ ghi |

## Lưới biến thể (2 × 2 × 2 × 4 = 32)
| Trục | Giá trị | Ý nghĩa |
|---|---|---|
| `neo` | `rau` / `than` | neo + fractal theo râu (high/low) hay theo thân (max/min(open, close)) |
| `k` | `2` / `3` | fractal 2-2 (5 nến) hay 3-3 (7 nến) |
| `tuoi` | `ngan` / `dai` | tuổi tối đa của neo 1 tính tới t: ngắn = H4 30 ngày, D1 120 ngày; dài = H4 90 ngày, D1 365 ngày |
| `chon` | `nhieu_cham` / `gan_gia` / `dai_nhat` / `cuc_tri` | chọn đường CHÍNH trong các đường còn hiệu lực cùng khung + loại |

Luật `chon` (kèm luật hoà):
- `nhieu_cham`: nhiều chạm nhất → hoà thì gần giá nhất.
- `gan_gia`: |giá đường − close H4 gần nhất| nhỏ nhất → hoà thì nhiều chạm.
- `dai_nhat`: neo 1 sớm nhất (đường dài nhất) → hoà thì nhiều chạm → gần giá.
- `cuc_tri`: neo 1 là đỉnh cao nhất (kháng cự) / đáy thấp nhất (hỗ trợ) trong các đường còn hiệu lực → hoà thì nhiều chạm → gần giá
  (đúng mô tả ảnh "râu đỉnh cao nhất → râu đỉnh thấp hơn kế tiếp").

## Cách so khớp và CHỌN (khai báo trước)
- Thời điểm nói t = `bat_dau_vn` (transcripts/gio_live.tsv) + giờ trong câu trích; không có giờ → giữa buổi. Đổi UTC = −7h.
- Chỉ so trendline BTC khung **H4/D1**, loại `khang_cu_giam`/`ho_tro_tang` (loại `kenh` có giá thì so với cả 2 loại, lấy lệch nhỏ hơn).
  H1/M15/W1 và `khac` chỉ đếm, không so.
- Giá tham chiếu của 1 trendline người đó nhắc: `gia_duong_luc_noi`; không có thì nội suy từ ≥2 `diem_neo` có ngày+giá;
  không có thì từ ghi chú ảnh (`so_tay/ghi_chu/hinh_anh_*.md`, buổi tập học). Không có giá → chỉ so trạng thái.
- **Khớp giá (chính)** = giá đường CHÍNH của biến thể (cùng khung + loại) tại t lệch ≤ 0,5% giá tham chiếu.
- Khớp giá (tập) = có ít nhất 1 đường còn hiệu lực cùng khung + loại lệch ≤ 0,5% (báo kèm số đường trung bình).
- **Khớp trạng thái** = trạng thái của đường chính (hoặc của đường khớp giá nếu có) ánh xạ đúng nhãn:
  `chua_pha`/`dang_giu` ↔ `giu`/`pha_gia`; `vua_pha` ↔ `vua_pha_1n`/`vua_pha_2n`/`da_pha` ≤ 48h/`pha_roi_test_lai` ≤ 48h;
  `pha_roi_test_lai` ↔ `pha_roi_test_lai` hoặc `da_pha`; `da_pha` ↔ `da_pha`/`pha_roi_test_lai`; `pha_gia` ↔ `pha_gia`.
- **Luật chọn 1 biến thể**: tỉ lệ khớp giá (chính) cao nhất → hoà thì tỉ lệ khớp trạng thái → hoà thì tỉ lệ khớp giá (tập)
  → hoà thì biến thể đứng trước trong lưới (thứ tự: neo rau trước than, k 2 trước 3, tuoi ngan trước dai,
  chon nhieu_cham, gan_gia, dai_nhat, cuc_tri). Không thêm tiêu chí nào khác (kể cả volume).
