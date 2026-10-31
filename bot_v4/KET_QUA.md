# KẾT QUẢ BOT V4 — backtest 2024 / 2025 / 2026 · giả dược · độ giống

_Sinh tự động bởi `bot_v4/bao_cao.py` lúc 2026-10-31 11:26 VN (chạy 16 giây). Chạy lại: `python3 bot_v4/bao_cao.py`. Thiết kế: [THIET_KE.md](THIET_KE.md) (mục 8)._

> **Tự cộng lại độc lập: KHỚP** — mọi lệnh, chuỗi von_sau và von.csv khớp tới 0,01$ (mục 1).

## 0. Dấu vân tay lúc chạy, khoá, giới hạn

| Tệp | sha256 lúc chạy | So với `bot_v4/KHOA.md` |
|---|---|---|
| `bot_v4/THIET_KE.md` | `cdfc577d13f29c3c0f3ec7572e417187dfd5ff229ceecde9a4f98e9204db30e9` | **KHỚP** |
| `bot_v4/dong_co.py` | `c05dfb7adfe12626cf48a589994f98ebd2955c93de1c1725393937c1f983529c` | **KHỚP** |
| `cong_cu/chi_bao.py` | `1f0a0cde1ccfa7b1d6ba6bc9f043b4bc8cd5a21e2212ae9d23073dd60f02a757` | **KHỚP** |
| `bot_v4/du_lieu/SHA256SUMS` | `e80152c64dcc79c4cdf9445d16b9b2ce9db24aedbcfc0120346e26409b947708` | **KHỚP** |
| `bot_v4/DIEN_GIAI.md` (mục khoá khác) | `f1398bcb250c8376a859e3e667b79389df6f507edc67f143d8bd9568c0fced37` | **KHỚP** |
| `bot_v4/chay.py` (mục khoá khác) | `ef635d2ec2ea117d96ae2a3da97a7062327d5f6c14864c1b756052fb71628e1a` | **KHỚP** |
| `bot_v4/kiem_tra.py` (mục khoá khác) | `80a7a5c71a46ae55ee6053f2609a7a3d9894c479e1cababa379520349b317af0` | **KHỚP** |

Dữ liệu: 12 tệp trong `SHA256SUMS`, **tất cả khớp** nội dung hiện tại.
- [`bot_v4/DIEN_GIAI.md`](DIEN_GIAI.md): 31 mục (DG 1 – DG 31)
- [`bot_v4/NHAT_KY_SUA.md`](NHAT_KY_SUA.md): 2 mục cấp 2; **0 lần sửa sau mốc 0** (chạy dữ liệu thật đầu tiên)

### Giới hạn trung thực (chép nguyên mục 0 `THIET_KE.md`)

> - v4 = **luật máy** bắt chước cách người đó ra quyết định + bài học từ bài thi v3 (`thi/BAO_CAO_XU_LY_P0.md`).
>   Đo 2 thứ: (1) **lãi/lỗ** vốn 4.000$; (2) **độ giống** hướng H4 với người đó trên 180 buổi.
> - Không dùng Claude suy luận cho backtest: model biết giá tới ~06/2026 → rò rỉ; và chi phí.
> - Giai đoạn: **2024** (kiểm phụ — chưa ai nhìn kết quả bất kỳ bot nào trên 2024), **2025**, **2026** (01/01 → 30/10).
>   Trung thực: luật lấy từ các buổi live 2026 → **2026 là trong mẫu**. Tôi (Claude) đã thấy kết quả v1/v2 trên 2025 (cả phân
>   tích từng thành phần) → **2025 không còn ngoài mẫu tuyệt đối**; v4 KHÔNG chọn thành phần theo kết quả đó (mọi luật dưới đây
>   có nguồn ở sổ tay / bài thi, ghi ở cột "Nguồn"). 2024 là năm sạch nhất. Kết luận thật chỉ có ở **buổi live mới từ 02/11**.
> - Tài sản: **BTC, ETH, OKB, BNB, VÀNG (GC=F), DẦU (CL=F)** — cùng rổ v1/v2 để so; báo thêm riêng **BTC**.
>

### Độ phủ dữ liệu (`bot_v4/du_lieu/NGUON.md`)

| TS | khung | ngày bắt đầu thực tế | ngày cuối | số nến | lỗ hổng>1 nến |
|---|---|---|---|---|---|
| BTC | 4H | 2022-06-01 00:00 | 2026-10-30 20:00 | 9678 | 0 |
| BTC | 1D | 2022-06-01 00:00 | 2026-10-30 00:00 | 1613 | 0 |
| ETH | 4H | 2022-06-01 00:00 | 2026-10-30 20:00 | 9678 | 0 |
| ETH | 1D | 2022-06-01 00:00 | 2026-10-30 00:00 | 1613 | 0 |
| OKB | 4H | 2022-06-01 00:00 | 2026-10-30 20:00 | 9678 | 0 |
| OKB | 1D | 2022-06-01 00:00 | 2026-10-30 00:00 | 1613 | 0 |
| BNB | 4H | 2022-12-21 00:00 | 2026-10-30 20:00 | 8460 | 0 |
| BNB | 1D | 2022-12-21 00:00 | 2026-10-30 00:00 | 1410 | 0 |
| VANG | 4H | 2024-06-10 00:00 | 2026-10-30 16:00 | 3454 | (140 nghỉ, bình thường) |
| VANG | 1D | 2022-06-01 22:00 | 2026-10-29 22:00 | 1111 | (241 nghỉ, bình thường) |
| DAU | 4H | 2024-06-10 00:00 | 2026-10-30 16:00 | 3404 | (161 nghỉ, bình thường) |
| DAU | 1D | 2022-06-01 22:00 | 2026-10-29 22:00 | 1110 | (242 nghỉ, bình thường) |

> **Cảnh báo dữ liệu:** VÀNG/DẦU 4H chỉ có từ **2024-06-10** (Yahoo giới hạn 1H ~2 năm), BNB từ **2022-12-21**. → Năm **2024** rổ 6 tài sản thực chất **thiếu vàng/dầu nửa đầu năm**, và EMA610 H4 của vàng/dầu chưa đủ khởi động (610 nến H4 ≈ 4–5 tháng giao dịch) tới khoảng cuối 2024. Xem số lệnh theo tài sản theo năm ở mục 5.

## 1. Tự cộng lại độc lập (lenh.csv → lãi từng lệnh → von_sau → von.csv)

Cách tính lại (không dùng mã động cơ, chỉ lenh.csv + quy tắc mục 7 + nến `bot_v4/du_lieu/` đọc riêng):

1. **Lãi từng lệnh** = chiều × KL × tỉ lệ TP1 × (giá chốt TP1 − vào) + chiều × KL × phần còn lại × (giá ra − vào) − phí, so với `lai_usd`; **phí** tính lại theo mục 7 (vào 0,02%; TP 0,02%; SL/hết giờ/hết kỳ 0,05% + trượt 0,02%) so với cột `phi`; và lãi tính độc lập hoàn toàn (giá + quy tắc phí, không dùng cột phí) so với `lai_usd`.
2. **R** = lai_usd ÷ (KL × |giá đặt − SL|) so với cột `R`.
3. **Dòng tiền**: phí vào lúc khớp, chốt TP1 lúc TP1, phần còn lại lúc ra → cộng dồn từ 4.000$ theo giờ → so `von_sau` từng lệnh, cột `von_chot` mọi dòng von.csv; cột `von` (theo giá) = đã chốt + lãi chưa chốt của vị thế đang mở theo close nến H4 (đọc độc lập).
4. **Giá + đường đi theo nến OHLC**: lệnh khớp ở nến SAU nến đặt (≤ 6 nến), nến đầu tiên chạm giá limit; giá vào = limit (hoặc giá mở nếu mở đã vượt); giữa khớp và ra không nến nào chạm SL/TP1/TP2 hay quá giờ dừng; nến ra đúng lý do (SL xét trước TP; SL/hết giờ/hết kỳ = mức hoặc giá mở/close × trượt 0,02%; TP = mức hoặc giá mở).

| Năm · rổ | Nguồn | Lệnh khớp | Lệch lãi lớn nhất | Vốn cuối tính lại | Kết quả |
|---|---|---|---|---|---|
| 2024 · 6 tài sản | `bot_v4/ket_qua/2024_6` | 399 | 0,000000$ | 1.497,66$ | **KHỚP** |
| 2024 · riêng BTC | `bot_v4/ket_qua/2024_BTC` | 120 | 0,000000$ | 3.356,77$ | **KHỚP** |
| 2025 · 6 tài sản | `bot_v4/ket_qua/2025_6` | 400 | 0,000000$ | 1.222,03$ | **KHỚP** |
| 2025 · riêng BTC | `bot_v4/ket_qua/2025_BTC` | 129 | 0,000000$ | 3.158,20$ | **KHỚP** |
| 2026 · 6 tài sản | `bot_v4/ket_qua/2026_6` | 331 | 0,000000$ | 1.680,86$ | **KHỚP** |
| 2026 · riêng BTC | `bot_v4/ket_qua/2026_BTC` | 92 | 0,000000$ | 3.246,13$ | **KHỚP** |

<details><summary>Chi tiết các phép kiểm khớp</summary>

- **2024 · 6 tài sản**: phí 399/399 lệnh đúng quy tắc mục 7 (trượt 0,02% nằm trong giá ra, phí market 0,05%); lãi tính độc lập (giá + quy tắc phí) vs lai_usd: lệch lớn nhất 0.000000$; R = lai_usd ÷ (KL × |giá đặt − SL|): 399/399 khớp; rui_ro_usd = KL × |giá đặt − SL|: 399/399 khớp; von_sau 399/399 khớp 4.000$ + dòng tiền cộng dồn (phí vào lúc khớp, TP1, lúc ra); von.csv `von_chot` 2197/2197 dòng khớp 4.000$ + dòng tiền đã xảy ra ≤ t; von.csv `von` (theo giá) 2197/2197 dòng khớp đã chốt + lãi chưa chốt (close nến H4 độc lập); giá vào/TP1/ra + đường đi 399/399 lệnh khớp nến OHLC độc lập (khớp, SL trước TP, hết giờ); tom_tat.json `von_cuoi` = 1,497.6596 vs tính lại 1,497.6596; tom_tat.json `lai_usd` = -2,502.3404 vs tính lại -2,502.3404; tom_tat.json `so_lenh` = 399.0000 vs tính lại 399.0000; rủi ro/vốn lúc đặt lệch tối đa 0.000 điểm % so với 2%/1%; đòn bẩy lệch min(40%/SL%, 20) tối đa 0.0000; lệnh chờ + mở đồng thời tối đa 3
- **2024 · riêng BTC**: phí 120/120 lệnh đúng quy tắc mục 7 (trượt 0,02% nằm trong giá ra, phí market 0,05%); lãi tính độc lập (giá + quy tắc phí) vs lai_usd: lệch lớn nhất 0.000000$; R = lai_usd ÷ (KL × |giá đặt − SL|): 120/120 khớp; rui_ro_usd = KL × |giá đặt − SL|: 120/120 khớp; von_sau 120/120 khớp 4.000$ + dòng tiền cộng dồn (phí vào lúc khớp, TP1, lúc ra); von.csv `von_chot` 2197/2197 dòng khớp 4.000$ + dòng tiền đã xảy ra ≤ t; von.csv `von` (theo giá) 2197/2197 dòng khớp đã chốt + lãi chưa chốt (close nến H4 độc lập); giá vào/TP1/ra + đường đi 120/120 lệnh khớp nến OHLC độc lập (khớp, SL trước TP, hết giờ); tom_tat.json `von_cuoi` = 3,356.7712 vs tính lại 3,356.7712; tom_tat.json `lai_usd` = -643.2288 vs tính lại -643.2288; tom_tat.json `so_lenh` = 120.0000 vs tính lại 120.0000; rủi ro/vốn lúc đặt lệch tối đa 0.000 điểm % so với 2%/1%; đòn bẩy lệch min(40%/SL%, 20) tối đa 0.0000; lệnh chờ + mở đồng thời tối đa 1
- **2025 · 6 tài sản**: phí 400/400 lệnh đúng quy tắc mục 7 (trượt 0,02% nằm trong giá ra, phí market 0,05%); lãi tính độc lập (giá + quy tắc phí) vs lai_usd: lệch lớn nhất 0.000000$; R = lai_usd ÷ (KL × |giá đặt − SL|): 400/400 khớp; rui_ro_usd = KL × |giá đặt − SL|: 400/400 khớp; von_sau 400/400 khớp 4.000$ + dòng tiền cộng dồn (phí vào lúc khớp, TP1, lúc ra); von.csv `von_chot` 2191/2191 dòng khớp 4.000$ + dòng tiền đã xảy ra ≤ t; von.csv `von` (theo giá) 2191/2191 dòng khớp đã chốt + lãi chưa chốt (close nến H4 độc lập); giá vào/TP1/ra + đường đi 400/400 lệnh khớp nến OHLC độc lập (khớp, SL trước TP, hết giờ); tom_tat.json `von_cuoi` = 1,222.0329 vs tính lại 1,222.0329; tom_tat.json `lai_usd` = -2,777.9671 vs tính lại -2,777.9671; tom_tat.json `so_lenh` = 400.0000 vs tính lại 400.0000; rủi ro/vốn lúc đặt lệch tối đa 0.000 điểm % so với 2%/1%; đòn bẩy lệch min(40%/SL%, 20) tối đa 0.0000; lệnh chờ + mở đồng thời tối đa 3
- **2025 · riêng BTC**: phí 129/129 lệnh đúng quy tắc mục 7 (trượt 0,02% nằm trong giá ra, phí market 0,05%); lãi tính độc lập (giá + quy tắc phí) vs lai_usd: lệch lớn nhất 0.000000$; R = lai_usd ÷ (KL × |giá đặt − SL|): 129/129 khớp; rui_ro_usd = KL × |giá đặt − SL|: 129/129 khớp; von_sau 129/129 khớp 4.000$ + dòng tiền cộng dồn (phí vào lúc khớp, TP1, lúc ra); von.csv `von_chot` 2191/2191 dòng khớp 4.000$ + dòng tiền đã xảy ra ≤ t; von.csv `von` (theo giá) 2191/2191 dòng khớp đã chốt + lãi chưa chốt (close nến H4 độc lập); giá vào/TP1/ra + đường đi 129/129 lệnh khớp nến OHLC độc lập (khớp, SL trước TP, hết giờ); tom_tat.json `von_cuoi` = 3,158.1971 vs tính lại 3,158.1971; tom_tat.json `lai_usd` = -841.8029 vs tính lại -841.8029; tom_tat.json `so_lenh` = 129.0000 vs tính lại 129.0000; rủi ro/vốn lúc đặt lệch tối đa 0.000 điểm % so với 2%/1%; đòn bẩy lệch min(40%/SL%, 20) tối đa 0.0000; lệnh chờ + mở đồng thời tối đa 1
- **2026 · 6 tài sản**: phí 331/331 lệnh đúng quy tắc mục 7 (trượt 0,02% nằm trong giá ra, phí market 0,05%); lãi tính độc lập (giá + quy tắc phí) vs lai_usd: lệch lớn nhất 0.000000$; R = lai_usd ÷ (KL × |giá đặt − SL|): 331/331 khớp; rui_ro_usd = KL × |giá đặt − SL|: 331/331 khớp; von_sau 331/331 khớp 4.000$ + dòng tiền cộng dồn (phí vào lúc khớp, TP1, lúc ra); von.csv `von_chot` 1819/1819 dòng khớp 4.000$ + dòng tiền đã xảy ra ≤ t; von.csv `von` (theo giá) 1819/1819 dòng khớp đã chốt + lãi chưa chốt (close nến H4 độc lập); giá vào/TP1/ra + đường đi 331/331 lệnh khớp nến OHLC độc lập (khớp, SL trước TP, hết giờ); tom_tat.json `von_cuoi` = 1,680.8577 vs tính lại 1,680.8577; tom_tat.json `lai_usd` = -2,319.1423 vs tính lại -2,319.1423; tom_tat.json `so_lenh` = 331.0000 vs tính lại 331.0000; rủi ro/vốn lúc đặt lệch tối đa 0.000 điểm % so với 2%/1%; đòn bẩy lệch min(40%/SL%, 20) tối đa 0.0000; lệnh chờ + mở đồng thời tối đa 3
- **2026 · riêng BTC**: phí 92/92 lệnh đúng quy tắc mục 7 (trượt 0,02% nằm trong giá ra, phí market 0,05%); lãi tính độc lập (giá + quy tắc phí) vs lai_usd: lệch lớn nhất 0.000000$; R = lai_usd ÷ (KL × |giá đặt − SL|): 92/92 khớp; rui_ro_usd = KL × |giá đặt − SL|: 92/92 khớp; von_sau 92/92 khớp 4.000$ + dòng tiền cộng dồn (phí vào lúc khớp, TP1, lúc ra); von.csv `von_chot` 1819/1819 dòng khớp 4.000$ + dòng tiền đã xảy ra ≤ t; von.csv `von` (theo giá) 1819/1819 dòng khớp đã chốt + lãi chưa chốt (close nến H4 độc lập); giá vào/TP1/ra + đường đi 92/92 lệnh khớp nến OHLC độc lập (khớp, SL trước TP, hết giờ); tom_tat.json `von_cuoi` = 3,246.1325 vs tính lại 3,246.1325; tom_tat.json `lai_usd` = -753.8675 vs tính lại -753.8675; tom_tat.json `so_lenh` = 92.0000 vs tính lại 92.0000; rủi ro/vốn lúc đặt lệch tối đa 0.000 điểm % so với 2%/1%; đòn bẩy lệch min(40%/SL%, 20) tối đa 0.0000; lệnh chờ + mở đồng thời tối đa 1

_Rủi ro/vốn và đòn bẩy chỉ là thông tin (vốn lúc đặt tính bằng vốn đã chốt; động cơ có thể dùng cách khác)._

</details>

## 2. Bảng chính: năm × rổ

| Năm | Rổ | Lãi$ | % | Số lệnh (L/S) | Huỷ | % thắng | R TB | t (R TB) | Tổng R | Sụt giảm max | Hệ số LN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024 | 6 tài sản | **-2.502$** | -62,6% | 399 (372/27) | 381 | 36% | -0,10 | -1,2 | -40,1 | 75,2% | 0,86 |
| 2024 | riêng BTC | **-643$** | -16,1% | 120 (111/9) | 128 | 32% | -0,05 | -0,3 | -6,4 | 37,7% | 0,91 |
| 2025 | 6 tài sản | **-2.778$** | -69,4% | 400 (357/43) | 394 | 38% | -0,12 | -1,7 | -49,9 | 75,2% | 0,77 |
| 2025 | riêng BTC | **-842$** | -21,0% | 129 (126/3) | 113 | 38% | -0,08 | -0,6 | -10,6 | 33,0% | 0,86 |
| 2026 (trong mẫu) | 6 tài sản | **-2.319$** | -58,0% | 331 (203/128) | 328 | 41% | -0,10 | -1,3 | -32,6 | 67,5% | 0,78 |
| 2026 (trong mẫu) | riêng BTC | **-754$** | -18,8% | 92 (48/44) | 107 | 41% | -0,08 | -0,6 | -7,5 | 29,7% | 0,81 |

_Lệnh = lệnh đã khớp; Huỷ = lệnh chờ hết hiệu lực/huỷ (không tính). % thắng = lai_usd > 0. R = cột `R` của lenh.csv (đã kiểm = lãi ÷ rủi ro SL danh nghĩa). t = R TB ÷ (độ lệch chuẩn R / √n): |t| < 2 = chưa phân biệt được với 0. Sụt giảm max tính trên cột `von` của von.csv (mỗi nến H4). Hệ số LN = Σ lãi ÷ Σ lỗ (USD)._

## 3. So với v1, v2 và mua-giữ BTC

| Bản | Năm | Rổ | Lãi$ | % | Số lệnh | % thắng | R TB | Sụt giảm | Hệ số LN | Phân vị giả dược — v4: ($ / tổng R / R TB) A (theo yêu cầu) · B (công bằng hơn); v1/v2: ($ / R) | Nguồn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **v4** | 2024 | 6 tài sản | -2.502$ | -62,6% | 399 | 36% | -0,10 | 75,2% | 0,86 | A 13 / 16 / 27 · B 8 / 12 / 33 | bản này |
| **v4** | 2024 | riêng BTC | -643$ | -16,1% | 120 | 32% | -0,05 | 37,7% | 0,91 | A 32 / 35 / 40 · B 32 / 35 / 43 | bản này |
| Mua-giữ BTC | 2024 | BTC | +4.844$ | +121,1% | 1 | — | — | 26,2% | — | — | `bot_v4/du_lieu/BTC_1D.csv` |
| v1 / v2 | 2024 | — | chưa từng chạy 2024 | | | | | | | | — |
| **v4** | 2025 | 6 tài sản | -2.778$ | -69,4% | 400 | 38% | -0,12 | 75,2% | 0,77 | A 9 / 11 / 25 · B 7 / 10 / 35 | bản này |
| **v4** | 2025 | riêng BTC | -842$ | -21,0% | 129 | 38% | -0,08 | 33,0% | 0,86 | A 39 / 37 / 48 · B 43 / 42 / 59 | bản này |
| v1 (luật 8 theo GIÁ, tối đa 3 lệnh) | 2025 | 6 tài sản | -1.105$ | -27,6% | 68 | 32% | -0,22 | 33,9% | 0,66 | 17 / 17 (200 lần, khác cách) | `backtest/KET_QUA_NGOAI_MAU.md:13` |
| v2 (tối đa 4 lệnh) | 2025 | 6 tài sản | -1.715$ | -42,9% | 264 | 40% | -0,06 | 55,4% | 0,87 | 41 / 45 (200 lần, khác cách) | `backtest/KET_QUA_V2.md:12` |
| v1 — chỉ lệnh BTC trong rổ 6 | 2025 | (BTC trong rổ 6) | -430$ | — | 11 | — | tổng R -5,4 | — | — | — | `backtest/KET_QUA_NGOAI_MAU.md:86` |
| v2 — chỉ lệnh BTC trong rổ 6 | 2025 | (BTC trong rổ 6) | -413$ | — | 62 | 35% | tổng R -3,0 | — | — | — | `backtest/KET_QUA_V2.md:79` |
| Mua-giữ BTC | 2025 | BTC | -258$ | -6,4% | 1 | — | — | 32,0% | — | — | `bot_v4/du_lieu/BTC_1D.csv` |
| **v4** | 2026 | 6 tài sản | -2.319$ | -58,0% | 331 | 41% | -0,10 | 67,5% | 0,78 | A 26 / 37 / 50 · B 19 / 34 / 58 | bản này |
| **v4** | 2026 | riêng BTC | -754$ | -18,8% | 92 | 41% | -0,08 | 29,7% | 0,81 | A 46 / 53 / 60 · B 39 / 48 / 58 | bản này |
| v1 (luật 8 theo GIÁ, tối đa 3 lệnh) | 2026 | 6 tài sản | +721$ | +18,0% | 55 | 42% | 0,18 | 25,9% | 1,27 | 92 / 92 (200 lần, khác cách) | `backtest/KET_QUA_NGOAI_MAU.md:17` |
| v2 (tối đa 4 lệnh) | 2026 | 6 tài sản | +1.927$ | +48,2% | 247 | 47% | 0,11 | 41,8% | 1,11 | 94 / 94 (200 lần, khác cách) | `backtest/KET_QUA_V2.md:14` |
| v1 — chỉ lệnh BTC trong rổ 6 | 2026 | (BTC trong rổ 6) | +61$ | — | 9 | — | tổng R 1,2 | — | — | — | `backtest/KET_QUA_NGOAI_MAU.md:98` |
| v2 — chỉ lệnh BTC trong rổ 6 | 2026 | (BTC trong rổ 6) | +708$ | — | 52 | 44% | tổng R 12,1 | — | — | — | `backtest/KET_QUA_V2.md:91` |
| Mua-giữ BTC | 2026 | BTC | -475$ | -11,9% | 1 | — | — | 39,5% | — | — | `bot_v4/du_lieu/BTC_1D.csv` |

Dòng nguồn trích nguyên văn (v1/v2 KHÔNG chạy lại ở đây; v1/v2 dùng dữ liệu `backtest/`, phân vị giả dược 200 lần đổi cả chiều 50/50 và vào ở giá đóng cùng tháng — không cùng cách với giả dược v4 ở mục 4):

- `backtest/KET_QUA_NGOAI_MAU.md:13` → `| 2025 (ngoài mẫu) | (i) theo GIÁ | **A** — Luật v1, 6 tài sản, tối đa 3 lệnh | -1.105$ | -27,6% | 68 | 32% | -0,22 | -1,4 | 33,9% | 0,66 | 17 | 17 |`
- `backtest/KET_QUA_NGOAI_MAU.md:17` → `| 2026 (trong mẫu, 6 TS) | (i) theo GIÁ | **A** — Luật v1, 6 tài sản, tối đa 3 lệnh | +721$ | +18,0% | 55 | 42% | 0,18 | 0,8 | 25,9% | 1,27 | 92 | 92 |`
- `backtest/KET_QUA_V2.md:12` → `| **v2** · 2025 (ngoài mẫu) | -1.715$ | -42,9% | 264 | 40% | -0,06 | -14,7 | 55,4% | 0,87 | 41 | 45 |`
- `backtest/KET_QUA_V2.md:14` → `| **v2** · 2026 (trong mẫu) | +1.927$ | +48,2% | 247 | 47% | 0,11 | 28,2 | 41,8% | 1,11 | 94 | 94 |`
- `backtest/KET_QUA_NGOAI_MAU.md:86` → `| BTC | 11 | 5/6 | 18% | -5,4 | -430$ | 8 | 4/4 | 12% | -5,5 | -422$ | -7,8% |`
- `backtest/KET_QUA_NGOAI_MAU.md:98` → `| BTC | 9 | 6/3 | 44% | 1,2 | +61$ | 7 | 5/2 | 57% | 1,9 | +139$ | -11,8% |`
- `backtest/KET_QUA_V2.md:79` → `| BTC | 11 | -5,4 | -430$ | 62 | 28/34 | 35% | -3,0 | -413$ | -7,8% |`
- `backtest/KET_QUA_V2.md:91` → `| BTC | 9 | 1,2 | +61$ | 52 | 25/27 | 44% | 12,1 | +708$ | -11,8% |`

_Mua-giữ BTC: mua ở close nến D1 đóng lúc bắt đầu kỳ (00:00 UTC 01/01), bán ở close D1 cuối kỳ (2026: D1 30/10), phí 0,05% mỗi đầu, sụt giảm theo close D1. v1/v2 ghi mua-giữ theo mốc 00:00 VN nên lệch nhẹ._

- Mua-giữ BTC 2024: 42.283,0 (2024-01-01 00:00 UTC) → 93.585,1 (2025-01-01 00:00 UTC)
- Mua-giữ BTC 2025: 93.585,1 (2025-01-01 00:00 UTC) → 87.638,9 (2026-01-01 00:00 UTC)
- Mua-giữ BTC 2026: 87.638,9 (2026-01-01 00:00 UTC) → 77.306,1 (2026-10-31 00:00 UTC)

## 4. Giả dược (1.000 lần/bộ, hạt giống gốc `20261031`)

| Năm · rổ | Kiểu | Lệnh mẫu | Thật $ | Giả dược P5 / P50 / P95 ($) | % lần giả dược lãi | **Phân vị thật ($)** | Tổng R thật | Giả dược tổng R P5 / P50 / P95 | **Phân vị thật (tổng R)** | R TB thật | Giả dược R TB P50 | **Phân vị thật (R TB)** | Lệnh giả dược khớp TB (bị bỏ vì quy tắc vốn TB) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024 · 6 tài sản | A | 399 | -2.502$ | -2.806$ / -1.504$ / +1.317$ | 15% | **13,4** | -40,1 | -54,7 / -15,1 / +25,8 | **16,0** | -0,101 | -0,050 | **27,2** | 299,6 (98,8) |
| 2024 · 6 tài sản | B | 780 | -2.502$ | -2.650$ / -1.351$ / +1.262$ | 16% | **7,9** | -40,1 | -49,4 / -14,3 / +22,2 | **12,2** | -0,101 | -0,060 | **32,9** | 239,5 (302,7) |
| 2024 · riêng BTC | A | 120 | -643$ | -1.542$ / -226$ / +2.226$ | 44% | **31,8** | -6,4 | -23,8 / -0,8 / +25,9 | **35,4** | -0,053 | -0,009 | **39,6** | 90,0 (29,9) |
| 2024 · riêng BTC | B | 248 | -643$ | -1.478$ / -218$ / +1.530$ | 40% | **32,3** | -6,4 | -23,1 / -1,4 / +19,2 | **35,3** | -0,053 | -0,020 | **42,8** | 70,8 (99,5) |
| 2025 · 6 tài sản | A | 400 | -2.778$ | -2.918$ / -1.826$ / +667$ | 10% | **9,2** | -49,9 | -59,9 / -23,2 / +18,1 | **11,4** | -0,125 | -0,077 | **24,9** | 301,3 (97,7) |
| 2025 · 6 tài sản | B | 794 | -2.778$ | -2.850$ / -1.778$ / +470$ | 8% | **6,6** | -49,9 | -59,1 / -24,0 / +12,3 | **10,2** | -0,125 | -0,095 | **35,2** | 252,7 (307,6) |
| 2025 · riêng BTC | A | 129 | -842$ | -1.691$ / -630$ / +838$ | 23% | **38,7** | -10,6 | -26,6 / -6,7 / +12,3 | **37,4** | -0,082 | -0,074 | **47,5** | 90,0 (38,8) |
| 2025 · riêng BTC | B | 242 | -842$ | -1.655$ / -704$ / +659$ | 16% | **42,8** | -10,6 | -26,1 / -8,4 / +9,6 | **41,8** | -0,082 | -0,114 | **58,7** | 73,7 (101,0) |
| 2026 · 6 tài sản | A | 331 | -2.319$ | -2.843$ / -1.770$ / +440$ | 9% | **25,8** | -32,6 | -59,0 / -24,4 / +10,8 | **36,6** | -0,098 | -0,097 | **49,6** | 250,4 (79,7) |
| 2026 · 6 tài sản | B | 659 | -2.319$ | -2.783$ / -1.696$ / +364$ | 9% | **19,4** | -32,6 | -56,4 / -24,2 / +9,7 | **34,0** | -0,098 | -0,118 | **58,3** | 202,2 (261,0) |
| 2026 · riêng BTC | A | 92 | -754$ | -1.702$ / -694$ / +830$ | 21% | **46,0** | -7,5 | -27,2 / -8,1 / +10,9 | **53,2** | -0,082 | -0,121 | **60,1** | 67,7 (24,2) |
| 2026 · riêng BTC | B | 199 | -754$ | -1.549$ / -596$ / +865$ | 24% | **38,8** | -7,5 | -24,0 / -7,0 / +11,8 | **47,6** | -0,082 | -0,122 | **58,5** | 57,7 (83,9) |

**Hai kiểu giả dược** (đều: 1 lệnh giả dược cho mỗi lệnh mẫu, cùng tài sản, chiều, loại chính/hồi, khoảng SL % theo giá đặt limit, TP1/TP2 theo bội R, giờ dừng theo cột `gio_dung` (chính 120h, hồi 48h); thời điểm đặt rút ngẫu nhiên ĐỀU trong các giờ ĐÓNG nến H4 của tài sản đó trong cùng kỳ; mô phỏng bằng `dong_co.mo_phong_lenh` — hiệu lực 6 nến, huỷ khi view đổi, khớp, SL trước TP, phí như lệnh thật):

- **A — đúng yêu cầu mục 8**: mẫu = lệnh thật ĐÃ KHỚP; limit đặt đúng giá close nến ngẫu nhiên (gần như khớp ngay nến sau).
- **B — công bằng với cách vào limit**: mẫu = MỌI lệnh đã đặt (cả lệnh bị huỷ); limit cách close nến ngẫu nhiên đúng tỉ lệ như lệnh thật (giá đặt ÷ close lúc đặt) → giữ cả cơ chế chờ hồi về vùng, tỉ lệ khớp; chỉ bỏ phần CHỌN vùng/thời điểm.

Quy tắc vốn như thật: xét theo thứ tự thời gian; khối lượng = rủi ro (chính 2% / hồi 1%) × số dư đã chốt ÷ khoảng SL; số dư cộng theo từng sự kiện tiền của `mo_phong_lenh` (phí vào, TP1, lúc ra) đúng giờ xảy ra; tối đa 3 lệnh chờ + mở trên rổ, mỗi tài sản 1, ký quỹ (KL × giá ÷ min(40%/SL%, 20); giảm nửa sau TP1) ≤ 50% số dư — lệnh vi phạm bị bỏ (cột cuối). Lệnh còn mở lúc hết kỳ đóng ở close cuối kỳ (`ket_thuc` = cuối kỳ). Hạt giống lần i = `20261031 + i` kèm tên bộ và kiểu (`random.Random("<20261031+i>|<năm>_<rổ>|<A/B>")`) → tái lập được, không phụ thuộc số tiến trình (mọi bộ chạy song song trong 1 Pool). **Phân vị = % số lần giả dược có kết quả THẤP HƠN thật** (≥ 95 mới đáng chú ý; ≈ 50 = không hơn ngẫu nhiên). Quy tắc vốn bỏ bớt lệnh giả dược (trùng giờ) nên số lệnh giả dược khớp ít hơn thật → tổng $ / tổng R so lệch về phía giả dược khi kỳ vọng mỗi lệnh âm; **R TB mỗi lệnh** không phụ thuộc số lệnh nên là thước chính.

### 4b. Hiệu chỉnh: hai kiểu giả dược trên dữ liệu KHÔNG có quy luật

Cùng động cơ (`dong_co.chay`, không sửa gì) chạy trên nến giả lập bước ngẫu nhiên (log-giá, 16 bước/nến H4, O/H/L/C lấy từ đường đi; hạt giống `777`; tạo trong thư mục tạm, không ghi đâu cả). Trên dữ liệu như vậy không chiến lược nào có lợi thế thật → giả dược CÔNG BẰNG phải cho phân vị rải quanh 50; phân vị dồn về 0 nghĩa là giả dược đó thiên lệch có lợi cho chính nó (làm bot trông tệ hơn thực chất).

| Năm · rổ (dữ liệu giả lập) | Lệnh | R TB bot | Phân vị A ($ / tổng R / R TB) | Phân vị B ($ / tổng R / R TB) |
|---|---|---|---|---|
| 2024 · 6 tài sản | 500 | -0,21 | 0 / 0 / 0 | 0 / 0 / 21 |
| 2024 · riêng BTC | 140 | -0,20 | 6 / 5 / 13 | 13 / 14 / 44 |
| 2025 · 6 tài sản | 499 | -0,10 | 0 / 0 / 1 | 26 / 30 / 58 |
| 2025 · riêng BTC | 126 | +0,04 | 22 / 22 / 19 | 76 / 77 / 72 |
| 2026 · 6 tài sản | 380 | -0,12 | 2 / 2 / 5 | 19 / 21 / 52 |
| 2026 · riêng BTC | 119 | -0,15 | 8 / 10 / 17 | 24 / 32 / 54 |

_Phân vị trung bình 6 bộ trên dữ liệu không quy luật — A: $ 6 · tổng R 7 · R TB 9 — B: $ 26 · tổng R 29 · R TB 50 (công bằng ≈ 50; chỉ 6 bộ nên nhiễu ±10). Đọc phân vị thật theo kiểu/thước được hiệu chỉnh gần 50 nhất._

## 5. Theo tài sản

Số lệnh khớp theo tài sản theo năm (rổ 6):

| Tài sản | 2024 | 2025 | 2026 |
|---|---|---|---|
| BTC | 116 | 120 | 86 |
| ETH | 112 | 115 | 98 |
| OKB | 90 | 66 | 60 |
| BNB | 74 | 38 | 40 |
| VANG | 5 | 26 | 30 |
| DAU | 2 | 35 | 17 |

**2024 · rổ 6**

| Tài sản | Lệnh (L/S) | % thắng | R TB | Tổng R | Lãi$ | Hệ số LN |
|---|---|---|---|---|---|---|
| BTC | 116 (109/7) | 31% | -0,05 | -5,8 | -503$ | 0,92 |
| ETH | 112 (100/12) | 38% | +0,01 | +0,9 | +310$ | 1,06 |
| OKB | 90 (86/4) | 36% | -0,20 | -18,3 | -1.288$ | 0,70 |
| BNB | 74 (72/2) | 41% | -0,19 | -14,3 | -925$ | 0,70 |
| VANG | 5 (5/0) | 40% | -0,20 | -1,0 | -38$ | 0,70 |
| DAU | 2 (0/2) | 0% | -0,79 | -1,6 | -59$ | 0,00 |

**2025 · rổ 6**

| Tài sản | Lệnh (L/S) | % thắng | R TB | Tổng R | Lãi$ | Hệ số LN |
|---|---|---|---|---|---|---|
| BTC | 120 (118/2) | 42% | -0,13 | -16,2 | -847$ | 0,76 |
| ETH | 115 (111/4) | 30% | -0,12 | -13,4 | -929$ | 0,77 |
| OKB | 66 (66/0) | 30% | -0,29 | -19,0 | -825$ | 0,61 |
| BNB | 38 (38/0) | 37% | -0,20 | -7,6 | -418$ | 0,62 |
| VANG | 26 (24/2) | 42% | +0,20 | +5,2 | +170$ | 1,29 |
| DAU | 35 (0/35) | 57% | +0,03 | +1,0 | +70$ | 1,12 |

**2026 · rổ 6**

| Tài sản | Lệnh (L/S) | % thắng | R TB | Tổng R | Lãi$ | Hệ số LN |
|---|---|---|---|---|---|---|
| BTC | 86 (43/43) | 43% | +0,02 | +1,3 | -119$ | 0,95 |
| ETH | 98 (27/71) | 39% | -0,10 | -9,7 | -818$ | 0,75 |
| OKB | 60 (57/3) | 47% | +0,02 | +1,2 | +26$ | 1,02 |
| BNB | 40 (36/4) | 45% | -0,20 | -8,0 | -458$ | 0,64 |
| VANG | 30 (30/0) | 30% | -0,50 | -14,9 | -820$ | 0,26 |
| DAU | 17 (10/7) | 35% | -0,14 | -2,4 | -130$ | 0,77 |

_Vốn dùng chung (rủi ro % vốn lúc đặt) nên $ theo tài sản phụ thuộc thứ tự lệnh; so bằng tổng R chắc hơn._

## 6. Lệnh chính (thuận pha) vs lệnh hồi (ngược pha)

| Năm · rổ | Loại | Lệnh (L/S) | % thắng | R TB | t | Tổng R | Lãi$ | Hệ số LN |
|---|---|---|---|---|---|---|---|---|
| 2024 · 6 tài sản | chính | 375 (372/3) | 37% | -0,07 | -0,8 | -25,9 | -1.985$ | 0,89 |
| 2024 · 6 tài sản | hồi | 24 (0/24) | 21% | -0,59 | -2,8 | -14,3 | -518$ | 0,36 |
| 2024 · riêng BTC | chính | 111 (111/0) | 32% | -0,03 | -0,2 | -3,3 | -509$ | 0,92 |
| 2024 · riêng BTC | hồi | 9 (0/9) | 22% | -0,35 | -0,6 | -3,1 | -134$ | 0,54 |
| 2025 · 6 tài sản | chính | 392 (357/35) | 38% | -0,13 | -1,7 | -49,4 | -2.749$ | 0,77 |
| 2025 · 6 tài sản | hồi | 8 (0/8) | 25% | -0,07 | -0,1 | -0,5 | -29$ | 0,81 |
| 2025 · riêng BTC | chính | 126 (126/0) | 39% | -0,06 | -0,4 | -7,4 | -730$ | 0,87 |
| 2025 · riêng BTC | hồi | 3 (0/3) | 0% | -1,08 | — | -3,2 | -112$ | 0,00 |
| 2026 · 6 tài sản | chính | 323 (198/125) | 41% | -0,12 | -1,6 | -38,8 | -2.476$ | 0,76 |
| 2026 · 6 tài sản | hồi | 8 (5/3) | 50% | +0,78 | +1,1 | +6,2 | +157$ | 2,56 |
| 2026 · riêng BTC | chính | 88 (44/44) | 41% | -0,12 | -0,8 | -10,3 | -860$ | 0,78 |
| 2026 · riêng BTC | hồi | 4 (4/0) | 50% | +0,70 | +0,7 | +2,8 | +106$ | 2,29 |

## 7. Theo lý do ra lệnh

| Năm · rổ | TP2 | TP | SL | SL_HOA_VON | HET_GIO | HET_KY | HUY | DANG_CHO | DANG_MO |
|---|---|---|---|---|---|---|---|---|---|
| 2024 · 6 tài sản | 36 · +8.154$ · R +114,2 | 2 · +228$ · R +4,7 | 255 · -18.507$ · R -270,5 | 79 · +3.367$ · R +48,5 | 26 · +4.259$ · R +63,0 | 1 · -5$ · R -0,2 | 381 | 0 | 0 |
| 2024 · riêng BTC | 11 · +3.171$ · R +39,9 | 1 · +139$ · R +3,9 | 82 · -6.883$ · R -87,9 | 18 · +1.001$ · R +12,7 | 7 · +1.926$ · R +24,9 | 1 · +3$ · R +0,1 | 128 | 0 | 0 |
| 2025 · 6 tài sản | 37 · +4.590$ · R +102,7 | 2 · +124$ · R +5,9 | 246 · -11.938$ · R -261,5 | 86 · +2.114$ · R +48,8 | 27 · +2.327$ · R +53,9 | 2 · +5$ · R +0,2 | 394 | 0 | 0 |
| 2025 · riêng BTC | 13 · +2.065$ · R +31,2 | 0 | 79 · -5.798$ · R -84,7 | 25 · +884$ · R +13,1 | 11 · +2.039$ · R +30,3 | 1 · -32$ · R -0,5 | 113 | 0 | 0 |
| 2026 · 6 tài sản | 38 · +4.522$ · R +95,0 | 2 · +112$ · R +4,9 | 195 · -10.372$ · R -207,3 | 77 · +2.119$ · R +43,0 | 19 · +1.299$ · R +31,9 | 0 | 328 | 0 | 0 |
| 2026 · riêng BTC | 12 · +1.736$ · R +26,1 | 1 · +76$ · R +2,0 | 54 · -3.991$ · R -58,0 | 19 · +780$ · R +10,9 | 6 · +646$ · R +11,5 | 0 | 107 | 0 | 0 |

_Ô = số lệnh · tổng lãi$ · tổng R. TP2 = phần còn lại ra ở TP2 (đã chốt 50% ở TP1 nếu có); TP = TP duy nhất (lệnh hồi); SL_HOA_VON = sau TP1 dời SL về giá vào; HET_GIO = dừng theo giờ; HET_KY = đóng ở close cuối kỳ; HUY = lệnh chờ không khớp._

## 8. Độ giống hướng H4 với người đó

> ## ⚠️ TRONG MẪU — luật v4 rút từ chính các buổi live 2026 này. Số dưới đây KHÔNG phải bằng chứng dự đoán; kết luận thật chỉ có ở buổi live mới từ 02/11/2026.

Mốc C = `bat_dau_vn + phut` (giờ VN → UTC) trong `transcripts/gio_live.tsv` (180 buổi; 180 buổi có phiếu). View bot = `dong_co.view_tai("BTC", C)`. Nhãn người đó = view khung H4 (không có thì "chung") trong phiếu: buổi từ 2026-07-01 → `thi/dap_an_v2/phieu/`, trước đó → `phieu/` (khớp theo video id). Luật từ trên xuống: định nghĩa trong docstring `thi/cham.py`, tính lại trên `bot_v4/du_lieu/BTC_*.csv` chỉ với nến đã đóng ≤ C. Mọi cách đoán chấm trên CÙNG tập buổi.

Kiểm rò rỉ: `gio_cat` do `view_tai` trả về > C ở **0** buổi (đạt).

### Cả 180 buổi (T1–T10)

179 buổi có nhãn người đó hợp lệ (loại 1 buổi nhãn không hợp lệ: 2026-01-20_GygVJDmjlgY).

| Cách đoán | Trùng 3 nhãn | Khi cả 2 có hướng | Bot − cách này (điểm %) |
|---|---|---|---|
| **Bot v4** (`view_tai`) | **109/179 = 61%** | 108/161 = 67% | — |
| Luôn GIẢM | **85/179 = 47%** | 85/164 = 52% | +13 |
| Luật từ trên xuống (thi/cham.py) | **110/179 = 61%** | 108/153 = 71% | -1 |

- McNemar bot vs luôn GIẢM: bot đúng–mốc sai 48 / mốc đúng–bot sai 24, p = 0,006 (nhị thức chính xác, hai phía).
- McNemar bot vs luật từ trên xuống: bot đúng–mốc sai 33 / mốc đúng–bot sai 34, p = 1,000 (nhị thức chính xác, hai phía).

Người đó: TĂNG 79 · GIẢM 85 · PHÂN VÂN 15 — Bot: TĂNG 75 · GIẢM 100 · PHÂN VÂN 4 · không hợp lệ 0

Bảng chéo (dòng = người đó, cột = bot):

| | TĂNG | GIẢM | PHÂN VÂN | Không hợp lệ | Tổng |
|---|---|---|---|---|---|
| **TĂNG** | 47 | 31 | 1 | 0 | 79 |
| **GIẢM** | 22 | 61 | 2 | 0 | 85 |
| **PHÂN VÂN** | 6 | 8 | 1 | 0 | 15 |
| Tổng | 75 | 100 | 4 | 0 | 179 |

### T1–T6 (trước 2026-07-01, nhãn `phieu/`)

102 buổi có nhãn người đó hợp lệ (loại 1 buổi nhãn không hợp lệ: 2026-01-20_GygVJDmjlgY).

| Cách đoán | Trùng 3 nhãn | Khi cả 2 có hướng | Bot − cách này (điểm %) |
|---|---|---|---|
| **Bot v4** (`view_tai`) | **62/102 = 61%** | 61/93 = 66% | — |
| Luôn GIẢM | **36/102 = 35%** | 36/94 = 38% | +25 |
| Luật từ trên xuống (thi/cham.py) | **63/102 = 62%** | 63/93 = 68% | -1 |

- McNemar bot vs luôn GIẢM: bot đúng–mốc sai 48 / mốc đúng–bot sai 22, p = 0,003 (nhị thức chính xác, hai phía).
- McNemar bot vs luật từ trên xuống: bot đúng–mốc sai 19 / mốc đúng–bot sai 20, p = 1,000 (nhị thức chính xác, hai phía).

Người đó: TĂNG 58 · GIẢM 36 · PHÂN VÂN 8 — Bot: TĂNG 75 · GIẢM 25 · PHÂN VÂN 2 · không hợp lệ 0

Bảng chéo (dòng = người đó, cột = bot):

| | TĂNG | GIẢM | PHÂN VÂN | Không hợp lệ | Tổng |
|---|---|---|---|---|---|
| **TĂNG** | 47 | 10 | 1 | 0 | 58 |
| **GIẢM** | 22 | 14 | 0 | 0 | 36 |
| **PHÂN VÂN** | 6 | 1 | 1 | 0 | 8 |
| Tổng | 75 | 25 | 2 | 0 | 102 |

### T7–T10 (từ 2026-07-01, nhãn `thi/dap_an_v2/phieu/`)

77 buổi có nhãn người đó hợp lệ (loại 0 buổi nhãn không hợp lệ).

| Cách đoán | Trùng 3 nhãn | Khi cả 2 có hướng | Bot − cách này (điểm %) |
|---|---|---|---|
| **Bot v4** (`view_tai`) | **47/77 = 61%** | 47/68 = 69% | — |
| Luôn GIẢM | **49/77 = 64%** | 49/70 = 70% | -3 |
| Luật từ trên xuống (thi/cham.py) | **47/77 = 61%** | 45/60 = 75% | +0 |

- McNemar bot vs luôn GIẢM: bot đúng–mốc sai 0 / mốc đúng–bot sai 2, p = 0,500 (nhị thức chính xác, hai phía).
- McNemar bot vs luật từ trên xuống: bot đúng–mốc sai 14 / mốc đúng–bot sai 14, p = 1,000 (nhị thức chính xác, hai phía).

Người đó: TĂNG 21 · GIẢM 49 · PHÂN VÂN 7 — Bot: TĂNG 0 · GIẢM 75 · PHÂN VÂN 2 · không hợp lệ 0

Bảng chéo (dòng = người đó, cột = bot):

| | TĂNG | GIẢM | PHÂN VÂN | Không hợp lệ | Tổng |
|---|---|---|---|---|---|
| **TĂNG** | 0 | 21 | 0 | 0 | 21 |
| **GIẢM** | 0 | 47 | 2 | 0 | 49 |
| **PHÂN VÂN** | 0 | 7 | 0 | 0 | 7 |
| Tổng | 0 | 75 | 2 | 0 | 77 |

_Phân bố (pha W1 → view bot) trên các buổi: GIẢM→GIẢM: 99, GIẢM→PHÂN VÂN: 2, GIẢM→TĂNG: 8, TĂNG→GIẢM: 1, TĂNG→PHÂN VÂN: 2, TĂNG→TĂNG: 68._

<details><summary>Từng buổi</summary>

| Buổi | C (VN) | gio_cat (VN) | Người đó | Bot (pha) | Trùng | Luật từ trên xuống | Nguồn nhãn |
|---|---|---|---|---|---|---|---|
| 2026-01-06_aQbHs7J80jc | 01-06 11:10 | 01-06 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-01-06_aQbHs7J80jc.json` |
| 2026-01-07_NOBgwE4Gdko | 01-07 11:22 | 01-07 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-01-07_NOBgwE4Gdko.json` |
| 2026-01-08_jX-0Hgy1S0E | 01-08 11:11 | 01-08 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-01-08_jX-0Hgy1S0E.json` |
| 2026-01-09_YLu3KxaMspQ | 01-09 11:09 | 01-09 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-01-09_YLu3KxaMspQ.json` |
| 2026-01-12_xwJagQCx1gY | 01-12 11:22 | 01-12 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-01-12_xwJagQCx1gY.json` |
| 2026-01-13_vg80vm31RLM | 01-13 11:17 | 01-13 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-01-13_vg80vm31RLM.json` |
| 2026-01-14_2ZyVfVN3n4Y | 01-14 11:11 | 01-14 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-01-14_2ZyVfVN3n4Y.json` |
| 2026-01-15_S30tBiADnLk | 01-15 11:33 | 01-15 11:00 | GIẢM | GIẢM (TĂNG) | ✓ | GIẢM | `phieu/2026-01-15_S30tBiADnLk.json` |
| 2026-01-16_SllvhCOjrkE | 01-16 11:14 | 01-16 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-01-16_SllvhCOjrkE.json` |
| 2026-01-19_rmCGKqaMkdw | 01-19 11:30 | 01-19 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-01-19_rmCGKqaMkdw.json` |
| 2026-01-20_GygVJDmjlgY | 01-20 11:13 | 01-20 11:00 | — | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-01-20_GygVJDmjlgY.json` |
| 2026-01-21_LRkYCtbojb0 | 01-21 11:18 | 01-21 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-01-21_LRkYCtbojb0.json` |
| 2026-01-22_WvCOBcm0bd0 | 01-22 10:57 | 01-22 07:00 | GIẢM | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-01-22_WvCOBcm0bd0.json` |
| 2026-01-23_ACM0WA7Rt3I | 01-23 11:23 | 01-23 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-01-23_ACM0WA7Rt3I.json` |
| 2026-01-26_KZ3cHk9a3yc | 01-26 11:29 | 01-26 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-01-26_KZ3cHk9a3yc.json` |
| 2026-01-27_Q2qX5gIvNC8 | 01-27 11:25 | 01-27 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-01-27_Q2qX5gIvNC8.json` |
| 2026-01-28_2_a0RdwC1t8 | 01-28 11:30 | 01-28 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-01-28_2_a0RdwC1t8.json` |
| 2026-01-29_8NrjverKQpo | 01-29 11:44 | 01-29 11:00 | PHÂN VÂN | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-01-29_8NrjverKQpo.json` |
| 2026-01-30_4PUqxjVBR4M | 01-30 11:43 | 01-30 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-01-30_4PUqxjVBR4M.json` |
| 2026-02-02_XD9H1FstBkE | 02-02 11:26 | 02-02 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-02-02_XD9H1FstBkE.json` |
| 2026-02-03_ewRoIMVREvw | 02-03 11:33 | 02-03 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-02-03_ewRoIMVREvw.json` |
| 2026-02-04_c6WnN4Q9EXo | 02-04 11:30 | 02-04 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-02-04_c6WnN4Q9EXo.json` |
| 2026-02-05_D6s6HggWgVQ | 02-05 11:22 | 02-05 11:00 | PHÂN VÂN | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-02-05_D6s6HggWgVQ.json` |
| 2026-02-06_PLl8AM0RxEM | 02-06 11:49 | 02-06 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-02-06_PLl8AM0RxEM.json` |
| 2026-02-11_MZ3XfAjYHqk | 02-11 11:20 | 02-11 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-02-11_MZ3XfAjYHqk.json` |
| 2026-02-16_0zDtKlmcydA | 02-16 13:56 | 02-16 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-02-16_0zDtKlmcydA.json` |
| 2026-02-26_7zFMbvqo3QI | 02-26 11:08 | 02-26 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-02-26_7zFMbvqo3QI.json` |
| 2026-02-27_9wE4YYq3P6Y | 02-27 11:02 | 02-27 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-02-27_9wE4YYq3P6Y.json` |
| 2026-03-02_GYgaZiYqRXY | 03-02 11:06 | 03-02 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-03-02_GYgaZiYqRXY.json` |
| 2026-03-03_xXKnEs9z81g | 03-03 11:09 | 03-03 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-03_xXKnEs9z81g.json` |
| 2026-03-04_OawlrpkFqQk | 03-04 11:09 | 03-04 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-04_OawlrpkFqQk.json` |
| 2026-03-05_pbr4y9qP1Ys | 03-05 11:09 | 03-05 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-05_pbr4y9qP1Ys.json` |
| 2026-03-06_4Z73-L_oWNY | 03-06 11:00 | 03-06 11:00 | PHÂN VÂN | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-03-06_4Z73-L_oWNY.json` |
| 2026-03-09_-jRLufOuVEE | 03-09 11:06 | 03-09 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-09_-jRLufOuVEE.json` |
| 2026-03-10_TXnTpUkc78s | 03-10 11:16 | 03-10 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-10_TXnTpUkc78s.json` |
| 2026-03-11_q-9RpBVzOhU | 03-11 23:20 | 03-11 23:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-03-11_q-9RpBVzOhU.json` |
| 2026-03-12_qJZk9q5A7rA | 03-12 11:13 | 03-12 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-03-12_qJZk9q5A7rA.json` |
| 2026-03-13_IbTz3V-KlKs | 03-13 11:13 | 03-13 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-13_IbTz3V-KlKs.json` |
| 2026-03-13_gRyoN4cBXZA | 03-13 23:30 | 03-13 23:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-13_gRyoN4cBXZA.json` |
| 2026-03-16_uXm43DPUtPQ | 03-16 11:10 | 03-16 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-16_uXm43DPUtPQ.json` |
| 2026-03-16_5DzdErSA8jk | 03-16 23:05 | 03-16 23:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-16_5DzdErSA8jk.json` |
| 2026-03-17_UKs5T1J0H9w | 03-17 11:12 | 03-17 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-17_UKs5T1J0H9w.json` |
| 2026-03-18_oyJGNnpopXw | 03-18 11:10 | 03-18 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-18_oyJGNnpopXw.json` |
| 2026-03-19_mBEBKzBb4kU | 03-19 11:15 | 03-19 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-03-19_mBEBKzBb4kU.json` |
| 2026-03-20_XLNjYQA8JPs | 03-20 11:13 | 03-20 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-20_XLNjYQA8JPs.json` |
| 2026-03-20_cxvXjQPayvY | 03-20 23:22 | 03-20 23:00 | GIẢM | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-03-20_cxvXjQPayvY.json` |
| 2026-03-23_bSnFyHqyo5c | 03-23 11:26 | 03-23 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-03-23_bSnFyHqyo5c.json` |
| 2026-03-24_xKTPieljFuY | 03-24 11:05 | 03-24 11:00 | PHÂN VÂN | PHÂN VÂN (TĂNG) | ✓ | TĂNG | `phieu/2026-03-24_xKTPieljFuY.json` |
| 2026-03-25_byYCWvbkZyU | 03-25 11:14 | 03-25 11:00 | TĂNG | PHÂN VÂN (TĂNG) | ✗ | TĂNG | `phieu/2026-03-25_byYCWvbkZyU.json` |
| 2026-03-26_35w3e47m3wY | 03-26 11:07 | 03-26 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | PHÂN VÂN | `phieu/2026-03-26_35w3e47m3wY.json` |
| 2026-03-27_1RmIBcPxX2I | 03-27 10:59 | 03-27 07:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-03-27_1RmIBcPxX2I.json` |
| 2026-03-30_KbxhGxmcYwg | 03-30 11:06 | 03-30 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-30_KbxhGxmcYwg.json` |
| 2026-03-31_bz8_iuwosGs | 03-31 11:10 | 03-31 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-03-31_bz8_iuwosGs.json` |
| 2026-04-01_Be-e74Mwx0U | 04-01 11:09 | 04-01 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-04-01_Be-e74Mwx0U.json` |
| 2026-04-02_orDQVRuxI1E | 04-02 11:01 | 04-02 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-04-02_orDQVRuxI1E.json` |
| 2026-04-03_vnCUK9ayUsI | 04-03 11:06 | 04-03 11:00 | PHÂN VÂN | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-04-03_vnCUK9ayUsI.json` |
| 2026-04-06_b48t6sSiV90 | 04-06 11:08 | 04-06 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-04-06_b48t6sSiV90.json` |
| 2026-04-07_HeBpJr0i6Bg | 04-07 11:07 | 04-07 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-04-07_HeBpJr0i6Bg.json` |
| 2026-04-08_l8hl1XtxPr4 | 04-08 11:07 | 04-08 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-04-08_l8hl1XtxPr4.json` |
| 2026-04-09_gx-69-TVn_w | 04-09 11:11 | 04-09 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-04-09_gx-69-TVn_w.json` |
| 2026-04-10_u6rbQNQWJAE | 04-10 11:25 | 04-10 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-04-10_u6rbQNQWJAE.json` |
| 2026-04-13_Fvz3aEsoOEE | 04-13 11:07 | 04-13 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | TĂNG | `phieu/2026-04-13_Fvz3aEsoOEE.json` |
| 2026-04-14_LfNwCzyBHdM | 04-14 11:15 | 04-14 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-04-14_LfNwCzyBHdM.json` |
| 2026-04-16_usKAHnR-_VI | 04-16 11:07 | 04-16 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | TĂNG | `phieu/2026-04-16_usKAHnR-_VI.json` |
| 2026-04-17_PH5pABMJ01k | 04-17 10:57 | 04-17 07:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-04-17_PH5pABMJ01k.json` |
| 2026-04-20_nN446WPRxPo | 04-20 11:33 | 04-20 11:00 | TĂNG | TĂNG (TĂNG) | ✓ | GIẢM | `phieu/2026-04-20_nN446WPRxPo.json` |
| 2026-04-21_AG126RfNCk4 | 04-21 11:30 | 04-21 11:00 | PHÂN VÂN | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-04-21_AG126RfNCk4.json` |
| 2026-04-24_ZTOmNH9I_wM | 04-24 11:08 | 04-24 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-04-24_ZTOmNH9I_wM.json` |
| 2026-04-27_9oEDyu-IfMM | 04-27 23:04 | 04-27 23:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-04-27_9oEDyu-IfMM.json` |
| 2026-04-28_lZw7Ts1eLWo | 04-28 11:06 | 04-28 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-04-28_lZw7Ts1eLWo.json` |
| 2026-04-29_-YYkW3NZT0M | 04-29 11:09 | 04-29 11:00 | GIẢM | TĂNG (TĂNG) | ✗ | GIẢM | `phieu/2026-04-29_-YYkW3NZT0M.json` |
| 2026-05-04_VUUbKp4bFSU | 05-04 11:07 | 05-04 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `phieu/2026-05-04_VUUbKp4bFSU.json` |
| 2026-05-05_Au_SuIIstcY | 05-05 11:07 | 05-05 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `phieu/2026-05-05_Au_SuIIstcY.json` |
| 2026-05-06_Ts0NVXvVnBw | 05-06 10:32 | 05-06 07:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `phieu/2026-05-06_Ts0NVXvVnBw.json` |
| 2026-05-06_ZEZOrGhyb6I | 05-06 23:12 | 05-06 23:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-05-06_ZEZOrGhyb6I.json` |
| 2026-05-07_FlYmDPPMwhY | 05-07 11:12 | 05-07 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-05-07_FlYmDPPMwhY.json` |
| 2026-05-08_mIEd9YU72Io | 05-08 11:10 | 05-08 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-05-08_mIEd9YU72Io.json` |
| 2026-05-11_jm7VS-lKW8w | 05-11 11:18 | 05-11 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-05-11_jm7VS-lKW8w.json` |
| 2026-05-12_MsCi4yFXqZA | 05-12 10:36 | 05-12 07:00 | PHÂN VÂN | GIẢM (GIẢM) | ✗ | GIẢM | `phieu/2026-05-12_MsCi4yFXqZA.json` |
| 2026-05-18_phLlmyf_8-w | 05-18 11:10 | 05-18 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-05-18_phLlmyf_8-w.json` |
| 2026-05-19_sWk33q2YCj4 | 05-19 11:07 | 05-19 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `phieu/2026-05-19_sWk33q2YCj4.json` |
| 2026-05-27_cFwCrK3RjcQ | 05-27 11:00 | 05-27 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-05-27_cFwCrK3RjcQ.json` |
| 2026-05-28_IY2JeSNTTfQ | 05-28 11:13 | 05-28 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-05-28_IY2JeSNTTfQ.json` |
| 2026-05-29_AmGhhyxkErs | 05-29 11:12 | 05-29 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `phieu/2026-05-29_AmGhhyxkErs.json` |
| 2026-06-01_cgTktZyPPt4 | 06-01 11:08 | 06-01 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `phieu/2026-06-01_cgTktZyPPt4.json` |
| 2026-06-02_5JIlkl46nss | 06-02 11:09 | 06-02 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `phieu/2026-06-02_5JIlkl46nss.json` |
| 2026-06-03_OVGlvdAXMKo | 06-03 11:17 | 06-03 11:00 | TĂNG | TĂNG (GIẢM) | ✓ | GIẢM | `phieu/2026-06-03_OVGlvdAXMKo.json` |
| 2026-06-04_59zOmIM_EOM | 06-04 11:10 | 06-04 11:00 | TĂNG | TĂNG (GIẢM) | ✓ | GIẢM | `phieu/2026-06-04_59zOmIM_EOM.json` |
| 2026-06-04_aPyIQ0I9e68 | 06-04 23:18 | 06-04 23:00 | TĂNG | TĂNG (GIẢM) | ✓ | GIẢM | `phieu/2026-06-04_aPyIQ0I9e68.json` |
| 2026-06-05_a6-MmsaBAfA | 06-05 11:02 | 06-05 11:00 | PHÂN VÂN | TĂNG (GIẢM) | ✗ | GIẢM | `phieu/2026-06-05_a6-MmsaBAfA.json` |
| 2026-06-08_WZ8PpZ9VA4Q | 06-08 11:10 | 06-08 11:00 | TĂNG | TĂNG (GIẢM) | ✓ | TĂNG | `phieu/2026-06-08_WZ8PpZ9VA4Q.json` |
| 2026-06-09_UmnCq7p4NlU | 06-09 10:50 | 06-09 07:00 | GIẢM | TĂNG (GIẢM) | ✗ | TĂNG | `phieu/2026-06-09_UmnCq7p4NlU.json` |
| 2026-06-10_38z3ITqKMkM | 06-10 11:10 | 06-10 11:00 | GIẢM | TĂNG (GIẢM) | ✗ | GIẢM | `phieu/2026-06-10_38z3ITqKMkM.json` |
| 2026-06-11_Xix-qwmyPkE | 06-11 11:08 | 06-11 11:00 | TĂNG | TĂNG (GIẢM) | ✓ | TĂNG | `phieu/2026-06-11_Xix-qwmyPkE.json` |
| 2026-06-12_x75V4Kb1fj4 | 06-12 11:07 | 06-12 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `phieu/2026-06-12_x75V4Kb1fj4.json` |
| 2026-06-15_yyy2aP8nOHc | 06-15 10:58 | 06-15 07:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `phieu/2026-06-15_yyy2aP8nOHc.json` |
| 2026-06-22_eaj9NEm85O4 | 06-22 21:44 | 06-22 19:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `phieu/2026-06-22_eaj9NEm85O4.json` |
| 2026-06-23_w3K-VXD_Tns | 06-23 10:53 | 06-23 07:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `phieu/2026-06-23_w3K-VXD_Tns.json` |
| 2026-06-24_ZrqOEgiFEF8 | 06-24 11:09 | 06-24 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-06-24_ZrqOEgiFEF8.json` |
| 2026-06-25_gy-YwzytUiA | 06-25 11:03 | 06-25 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-06-25_gy-YwzytUiA.json` |
| 2026-06-26_UzjWDBAiahs | 06-26 11:10 | 06-26 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `phieu/2026-06-26_UzjWDBAiahs.json` |
| 2026-06-29_wyCTvVbTVPE | 06-29 11:04 | 06-29 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `phieu/2026-06-29_wyCTvVbTVPE.json` |
| 2026-06-30_h3mwuQrqabM | 06-30 11:12 | 06-30 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `phieu/2026-06-30_h3mwuQrqabM.json` |
| 2026-07-01_WNiQnpm2BLo | 07-01 11:00 | 07-01 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `thi/dap_an_v2/phieu/2026-07-01_WNiQnpm2BLo.json` |
| 2026-07-02_w4bvsDte3bI | 07-02 11:07 | 07-02 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-02_w4bvsDte3bI.json` |
| 2026-07-03_IV0Mlz8kNPI | 07-03 11:12 | 07-03 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-03_IV0Mlz8kNPI.json` |
| 2026-07-06_GRWl0b0z1nk | 07-06 11:08 | 07-06 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `thi/dap_an_v2/phieu/2026-07-06_GRWl0b0z1nk.json` |
| 2026-07-07_uvBnzq6-k-M | 07-07 11:05 | 07-07 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `thi/dap_an_v2/phieu/2026-07-07_uvBnzq6-k-M.json` |
| 2026-07-09_Fmb8AziZ6f4 | 07-09 11:12 | 07-09 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-07-09_Fmb8AziZ6f4.json` |
| 2026-07-10_QwYznPgaAFY | 07-10 11:12 | 07-10 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-10_QwYznPgaAFY.json` |
| 2026-07-13_O3q2fmXlwhk | 07-13 11:09 | 07-13 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-07-13_O3q2fmXlwhk.json` |
| 2026-07-14_gpyn9kVPpn4 | 07-14 11:14 | 07-14 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `thi/dap_an_v2/phieu/2026-07-14_gpyn9kVPpn4.json` |
| 2026-07-15_-T8Wu5b89B4 | 07-15 10:59 | 07-15 07:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-15_-T8Wu5b89B4.json` |
| 2026-07-16_bwgz_kMSvfE | 07-16 11:08 | 07-16 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-16_bwgz_kMSvfE.json` |
| 2026-07-21_azP_1WdR-CE | 07-21 11:02 | 07-21 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-21_azP_1WdR-CE.json` |
| 2026-07-22_3gr71JlVqR8 | 07-22 11:16 | 07-22 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-22_3gr71JlVqR8.json` |
| 2026-07-23_IsyMSPIscsc | 07-23 11:16 | 07-23 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-23_IsyMSPIscsc.json` |
| 2026-07-24_7D1Ve5hs4bU | 07-24 11:04 | 07-24 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-24_7D1Ve5hs4bU.json` |
| 2026-07-27_YMlDceykaTw | 07-27 11:15 | 07-27 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-07-27_YMlDceykaTw.json` |
| 2026-07-28_1wDQbk0akZs | 07-28 11:45 | 07-28 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-07-28_1wDQbk0akZs.json` |
| 2026-07-29_2FMmTeLGCNY | 07-29 11:12 | 07-29 11:00 | PHÂN VÂN | GIẢM (GIẢM) | ✗ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-07-29_2FMmTeLGCNY.json` |
| 2026-07-29__TlYbqPT8nU | 07-30 01:23 | 07-29 23:00 | GIẢM | GIẢM (GIẢM) | ✓ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-07-29__TlYbqPT8nU.json` |
| 2026-07-30_qBG2h5D9CrE | 07-30 11:08 | 07-30 11:00 | PHÂN VÂN | GIẢM (GIẢM) | ✗ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-07-30_qBG2h5D9CrE.json` |
| 2026-07-31_SlGyokVNofU | 07-31 11:11 | 07-31 11:00 | GIẢM | PHÂN VÂN (GIẢM) | ✗ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-07-31_SlGyokVNofU.json` |
| 2026-08-03_U6juTGDLJek | 08-03 11:13 | 08-03 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `thi/dap_an_v2/phieu/2026-08-03_U6juTGDLJek.json` |
| 2026-08-04_K6QkKY6Og7o | 08-04 11:22 | 08-04 11:00 | GIẢM | PHÂN VÂN (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-08-04_K6QkKY6Og7o.json` |
| 2026-08-05_uw4QcusFtBc | 08-05 11:08 | 08-05 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `thi/dap_an_v2/phieu/2026-08-05_uw4QcusFtBc.json` |
| 2026-08-06__Ypby-_iFsg | 08-06 11:13 | 08-06 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-08-06__Ypby-_iFsg.json` |
| 2026-08-07_N-7XihrObp8 | 08-07 11:05 | 08-07 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-08-07_N-7XihrObp8.json` |
| 2026-08-10_1001_8BGhoFetSaU | 08-10 11:05 | 08-10 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-08-10_1001_8BGhoFetSaU.json` |
| 2026-08-11_1005_KvVvliql8xI | 08-11 11:06 | 08-11 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-08-11_1005_KvVvliql8xI.json` |
| 2026-08-12_1003_EaWaSL7aWT4 | 08-12 11:20 | 08-12 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-08-12_1003_EaWaSL7aWT4.json` |
| 2026-08-13_1006_hNxSX7GUKMs | 08-13 11:10 | 08-13 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-08-13_1006_hNxSX7GUKMs.json` |
| 2026-08-14_1004_xK38gQ-G6uA | 08-14 11:28 | 08-14 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-08-14_1004_xK38gQ-G6uA.json` |
| 2026-08-17_1006_tmR0aXnjOlA | 08-17 11:12 | 08-17 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | TĂNG | `thi/dap_an_v2/phieu/2026-08-17_1006_tmR0aXnjOlA.json` |
| 2026-08-18_0957__c0_SERWnz0 | 08-18 11:09 | 08-18 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | TĂNG | `thi/dap_an_v2/phieu/2026-08-18_0957__c0_SERWnz0.json` |
| 2026-08-19_1001_kfBEaOyHLkc | 08-19 11:08 | 08-19 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | PHÂN VÂN | `thi/dap_an_v2/phieu/2026-08-19_1001_kfBEaOyHLkc.json` |
| 2026-08-20_1003_eBveasTOjTs | 08-20 11:15 | 08-20 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-08-20_1003_eBveasTOjTs.json` |
| 2026-08-21_1003_oDD5qwLcZbw | 08-21 11:18 | 08-21 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-08-21_1003_oDD5qwLcZbw.json` |
| 2026-08-25_1003_nSxBbLai2mE | 08-25 11:18 | 08-25 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-08-25_1003_nSxBbLai2mE.json` |
| 2026-08-26_1001_I1DFCTsjQXE | 08-26 11:15 | 08-26 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-08-26_1001_I1DFCTsjQXE.json` |
| 2026-08-27_1006_ZJ5BVqdLJeE | 08-27 11:07 | 08-27 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-08-27_1006_ZJ5BVqdLJeE.json` |
| 2026-08-28_1007_KwvLRMMnVms | 08-28 11:11 | 08-28 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-08-28_1007_KwvLRMMnVms.json` |
| 2026-09-03_1012_8LXm3pVw9yI | 09-03 10:51 | 09-03 07:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-03_1012_8LXm3pVw9yI.json` |
| 2026-09-04_1014_eujLmRVw88k | 09-04 11:07 | 09-04 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-04_1014_eujLmRVw88k.json` |
| 2026-09-07_1007_0oycLOOqibw | 09-07 11:12 | 09-07 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-07_1007_0oycLOOqibw.json` |
| 2026-09-08_1002_gOwbzU0t2S0 | 09-08 11:10 | 09-08 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-08_1002_gOwbzU0t2S0.json` |
| 2026-09-14_1007_ykgTTK3EbP8 | 09-14 11:11 | 09-14 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-14_1007_ykgTTK3EbP8.json` |
| 2026-09-15_1008_M1ZThKy2Ylk | 09-15 11:13 | 09-15 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-15_1008_M1ZThKy2Ylk.json` |
| 2026-09-16_1008_31jXsidP5KE | 09-16 11:10 | 09-16 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-16_1008_31jXsidP5KE.json` |
| 2026-09-17_0026_7mETSY5t5Yg | 09-17 01:26 | 09-16 23:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-17_0026_7mETSY5t5Yg.json` |
| 2026-09-17_1002_1cUPKUmEnr4 | 09-17 11:00 | 09-17 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-17_1002_1cUPKUmEnr4.json` |
| 2026-09-18_1003_YPMgjMxL2io | 09-18 11:13 | 09-18 11:00 | PHÂN VÂN | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-09-18_1003_YPMgjMxL2io.json` |
| 2026-09-21_1001_I_U52BYUt0M | 09-21 11:18 | 09-21 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-21_1001_I_U52BYUt0M.json` |
| 2026-09-22_1003_N-_6NBs4ZW8 | 09-22 11:23 | 09-22 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-22_1003_N-_6NBs4ZW8.json` |
| 2026-09-23_1007_uK4vb9PoUIo | 09-23 11:15 | 09-23 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-09-23_1007_uK4vb9PoUIo.json` |
| 2026-09-24_1009_R_WfFHUJ5RI | 09-24 11:15 | 09-24 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-24_1009_R_WfFHUJ5RI.json` |
| 2026-09-25_1014_Wf7PeLs6l94 | 09-25 11:19 | 09-25 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-25_1014_Wf7PeLs6l94.json` |
| 2026-09-28_1006_G5Q1ATx_1ho | 09-28 11:08 | 09-28 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-28_1006_G5Q1ATx_1ho.json` |
| 2026-09-29_1002_3inGNRqb-UM | 09-29 11:14 | 09-29 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-09-29_1002_3inGNRqb-UM.json` |
| 2026-09-30_1003_3qAxAK71YAs | 09-30 11:09 | 09-30 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-09-30_1003_3qAxAK71YAs.json` |
| 2026-10-01_1005_56fLd04MSps | 10-01 11:14 | 10-01 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-01_1005_56fLd04MSps.json` |
| 2026-10-02_1001_AxRfx12h9Z0 | 10-02 11:06 | 10-02 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-02_1001_AxRfx12h9Z0.json` |
| 2026-10-05_1013_5U5CVdTlwT8 | 10-05 11:18 | 10-05 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-05_1013_5U5CVdTlwT8.json` |
| 2026-10-06_1001_CABZxVcYavM | 10-06 11:15 | 10-06 11:00 | PHÂN VÂN | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-10-06_1001_CABZxVcYavM.json` |
| 2026-10-07_1004_Rl-3RfG8EiY | 10-07 11:07 | 10-07 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-07_1004_Rl-3RfG8EiY.json` |
| 2026-10-13_1005_4ttwL_4CC9E | 10-13 11:07 | 10-13 11:00 | PHÂN VÂN | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-10-13_1005_4ttwL_4CC9E.json` |
| 2026-10-14_1009_BlA26qxNBTE | 10-14 11:22 | 10-14 11:00 | PHÂN VÂN | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-10-14_1009_BlA26qxNBTE.json` |
| 2026-10-15_1005_5iN8iTFsmlY | 10-15 11:13 | 10-15 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-15_1005_5iN8iTFsmlY.json` |
| 2026-10-16_1007_lSGpwulXi5s | 10-16 11:04 | 10-16 11:00 | PHÂN VÂN | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-10-16_1007_lSGpwulXi5s.json` |
| 2026-10-19_1001_-avZ2E3n2oE | 10-19 11:19 | 10-19 11:00 | TĂNG | GIẢM (GIẢM) | ✗ | GIẢM | `thi/dap_an_v2/phieu/2026-10-19_1001_-avZ2E3n2oE.json` |
| 2026-10-20_1017_zzhCJ1Bb_vg | 10-20 11:12 | 10-20 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-20_1017_zzhCJ1Bb_vg.json` |
| 2026-10-22_1009_yAEJBNZ56qs | 10-22 11:13 | 10-22 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-22_1009_yAEJBNZ56qs.json` |
| 2026-10-23_1002_cb85mXIfTv8 | 10-23 11:06 | 10-23 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-23_1002_cb85mXIfTv8.json` |
| 2026-10-26_1002_52C5f7Gf1NE | 10-26 11:11 | 10-26 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-26_1002_52C5f7Gf1NE.json` |
| 2026-10-27_1002_2RB3G-MYjhE | 10-27 11:20 | 10-27 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-27_1002_2RB3G-MYjhE.json` |
| 2026-10-28_1006_Gu1XtyNNH6I | 10-28 11:01 | 10-28 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-28_1006_Gu1XtyNNH6I.json` |
| 2026-10-29_0033_4Hg5YedKaAg | 10-29 01:23 | 10-28 23:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-29_0033_4Hg5YedKaAg.json` |
| 2026-10-29_1005_wcDxLBw0TO4 | 10-29 11:08 | 10-29 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-29_1005_wcDxLBw0TO4.json` |
| 2026-10-30_0955_f0JWA9aDHl8 | 10-30 11:24 | 10-30 11:00 | GIẢM | GIẢM (GIẢM) | ✓ | GIẢM | `thi/dap_an_v2/phieu/2026-10-30_0955_f0JWA9aDHl8.json` |

</details>

