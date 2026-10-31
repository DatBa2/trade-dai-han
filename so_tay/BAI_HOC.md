# Bài học rút ra (31/10/2026) — từ bài test 29–30/10 và backtest 2026

## A. Bắt chước người đó (so bot với người thật)
| # | Bài học | Bằng chứng | Sửa |
|---|---|---|---|
| A1 | Hướng thì giống, **đích bot đặt nông** hơn người đó | 30/10: BTC 80,5K vs 77–78K; ETH 2.300 vs 2.1–2.2K; NEAR 4,30 vs 3,9 — người đó đúng | Đích = đích người đó nêu gần nhất; hỗ trợ gần chỉ là TP1 |
| A2 | Bot **bỏ view quá sớm** khi nến xanh sau tin | 29/10 bot hạ đích sau GDP; người đó vẫn giữ sale và đúng | Mốc sai = mốc khung lớn; "tin chỉ hợp lý hoá đường giá, sau 4–8 giờ quay về cấu trúc" |
| A3 | Tài sản người đó **không nói** thì bot không có gì để bắt chước | ZEC: bot suy luật chung → sai cả 2 lần | Người đó im lặng → bot PHÂN VÂN |
| A4 | Nhận định thiếu **râu nến + vùng ổn kèm lý do** | User nhắc 30/10 | Bắt buộc trong mọi nhận định (DESIGN.md) |
| A5 | Tôi (độc lập) **để một tin vĩ mô đảo hướng** khi cấu trúc khung lớn chưa đổi | 29/10 tôi TĂNG vì GDP tốt → 1/4; người đó 3/3 | Không đổi hướng vì tin khi H4/D1 chưa đóng qua mốc |

## B. Từ backtest luật cơ học (in-sample 2026, 4.000$)
| # | Bài học | Bằng chứng | Hướng sửa (v2, chưa chạy) |
|---|---|---|---|
| B1 | Lãi đến từ **ít lệnh thắng lớn** theo xu hướng mạnh | 5 lệnh +2.080$, 57 lệnh còn lại −698$; thắng chỉ 40% | Giữ TP2 xa, không tối ưu tỉ lệ thắng |
| B2 | **Short pullback trong cú sập bị quét** | T2: 9 short, 8 dính SL, 3 lệnh cùng SL 1 nến | Người đó: "không short market sau nến H4 đỏ full vì dễ hồi" → sau nến sập lớn, chờ hồi về Fibo 0.5–0.618 của cú sập |
| B3 | Chờ hồi về EMA34 thì **lỡ xu hướng mạnh nhất** | 76% lệnh chờ huỷ vì giá chạy luôn | Thêm kiểu vào thứ 2: phá mốc + test lại (bản đồ mốc / vùng hội tụ) |
| B4 | **Stop theo giá bị râu quét** | 10 lệnh dính SL ngay nến khớp | Người đó SL theo **nến đóng** qua mốc → thử |
| B5 | **Đi ngang thì luật xu hướng sinh tín hiệu giả** | T10: 0/6 (giá kẹp 79–82K) | Nhận diện sideway (EMA chụm / giá cắt qua lại) → đứng ngoài hoặc đánh biên |
| B6 | Luật thừa thì bỏ | Lọc D1 chặn 18/3.000 lượt (B = A) | Giữ bộ luật gọn |
| B7 | Vàng không đánh chung luật crypto | Vàng −1,4R (12 lệnh) | Người đó: vàng "không gồng, scalping" |

## C. Quy trình nghiên cứu (lỗi của chính tôi)
| # | Bài học | Làm gì từ nay |
|---|---|---|
| C1 | **Ngã rẽ phân tích**: đổi cách hiểu 1 luật sau khi thấy kết quả (+3,4% → +34,6%) | Chốt định nghĩa trước, ghi lại; luôn báo cả 2 con số |
| C2 | Kiểm trên dữ liệu đã học (in-sample) → lạc quan | Chạy luật đã khoá trên **2025** (ngoài mẫu) + chạy giấy từ 31/10 |
| C3 | **Đo nhầm thước**: dự án đặt mục tiêu "GIỐNG người đó", backtest lại đo LÃI | Đo **% hướng bot trùng phiếu người đó** trên 180 buổi trước khi tối ưu lãi |
| C4 | Ít mẫu, lãi dồn vài lệnh | Không kết luận từ 1 lần chạy; xem phân phối, giả dược |

## D. Kết quả 3 kiểm tra (31/10 ~01:10)
| Kiểm tra | Kết quả | Bài học |
|---|---|---|
| % giống v1 vs 180 phiếu | 32% (cùng chiều 51%); 1 đặc trưng tốt nhất (nhịp 24h) chỉ 58% | Luật chỉ báo không bắt được cách người đó chọn hướng; tinh hoa nằm ở bản đồ mốc + bối cảnh |
| v1 ngoài mẫu 2025 (6 tài sản) | −27,6% / −17,9%; giả dược phân vị 17–20 | Lãi 2026 là khớp dữ liệu đã học |
| v2 ngoài mẫu 2025 | −42,9% (264 lệnh); 2026 in-sample +48% | Sửa luật theo chỗ lỗ in-sample làm in-sample đẹp, ngoài mẫu tệ hơn |
| Từng thay đổi v2 trên 2025 (chỉ để hiểu) | Giúp: đứng ngoài khi đi ngang, TP Fibo mở rộng. Hại: phá mốc–test lại, SL theo nến đóng (lệnh thua sâu hơn), vàng chỉ TP1 | Không dùng để chọn lại luật (sẽ lại là khớp dữ liệu) |
| Thực thi | Đòn bẩy 60%/SL% có thể bị sàn thanh lý trước chặn khẩn 2× | Đánh thật hạ đòn bẩy ≤ 40%/SL% |
→ Hướng luật cơ học thuần đã thử 2 bản, cả 2 lỗ ngoài mẫu. Hướng tiếp: Claude suy luận theo sổ tay + bản đồ mốc, thi trên buổi từ tháng 7/2026 (sau mốc kiến thức).
