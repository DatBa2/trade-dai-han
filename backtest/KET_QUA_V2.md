# KẾT QUẢ BOT V2 (luật cơ học v1 + 5 thay đổi) — so với v1, 6 tài sản

_Sinh tự động bởi `backtest/v2.py` (chạy lại: `python3 backtest/v2.py`). Tài sản: BTC, ETH, OKB, BNB (OKX), vàng GC=F, dầu CL=F (Yahoo). Vốn 4.000$, rủi ro 2%/lệnh, tối đa 4 lệnh mở, phí vào 0,02% / ra 0,05%, bỏ funding. v1 = `chay.py` nguyên văn (luật 8 theo GIÁ), chạy trên đúng 6 tài sản, tối đa 4 lệnh. Tham số v2 chốt trước, không dò/tối ưu — mục **Diễn giải** (viết trước lần chạy đầu) ở cuối file._

> **2025 là NGOÀI MẪU** (luật học từ các buổi live 2026, chưa từng nhìn 2025). **2026 là TRONG MẪU**: 5 thay đổi của v2 được đề xuất sau khi xem lỗi của v1 trên chính 2026 (BAI_HOC.md mục B), nên số 2026 của v2 lạc quan có hệ thống. Thước đo chính là cột 2025.

## 1. Bảng tổng v1 vs v2

| Bản | Lãi/lỗ | % | Số lệnh | Thắng | R TB | Tổng R | Sụt giảm lớn nhất | Hệ số LN | Phân vị giả dược ($) | Phân vị (R) |
|---|---|---|---|---|---|---|---|---|---|---|
| **v1** · 2025 (ngoài mẫu) | -1.105$ | -27,6% | 68 | 32% | -0,22 | -15,1 | 33,9% | 0,66 | 17 | 17 |
| **v2** · 2025 (ngoài mẫu) | -1.715$ | -42,9% | 264 | 40% | -0,06 | -14,7 | 55,4% | 0,87 | 41 | 45 |
| **v1** · 2026 (trong mẫu) | +721$ | +18,0% | 55 | 42% | 0,18 | 9,8 | 25,9% | 1,27 | 92 | 92 |
| **v2** · 2026 (trong mẫu) | +1.927$ | +48,2% | 247 | 47% | 0,11 | 28,2 | 41,8% | 1,11 | 94 | 94 |


_R TB = lãi ròng sau phí ÷ rủi ro dự kiến (SL danh nghĩa). Sụt giảm tính trên vốn theo giá thị trường mỗi nến H4. Phân vị giả dược = % số lần giả dược thua kết quả thật (200 lần)._

**Mốc so sánh: mua & giữ** (vốn 4.000$ chia đều, mua ở giá đóng H4 cuối trước đầu kỳ, phí 0,05% mỗi đầu)

| Kỳ | Chiến lược | Lãi/lỗ | % | Sụt giảm lớn nhất |
|---|---|---|---|---|
| 2025 (ngoài mẫu) | Mua & giữ BTC | -317$ | -7,9% | 34,4% |
| 2025 (ngoài mẫu) | Mua & giữ ETH | -504$ | -12,6% | 61,8% |
| 2025 (ngoài mẫu) | Mua & giữ OKB | +4.690$ | +117,3% | 59,2% |
| 2025 (ngoài mẫu) | Mua & giữ BNB | +855$ | +21,4% | 39,8% |
| 2025 (ngoài mẫu) | Mua & giữ Vàng | +2.585$ | +64,6% | 10,4% |
| 2025 (ngoài mẫu) | Mua & giữ Dầu WTI | -775$ | -19,4% | 31,5% |
| 2025 (ngoài mẫu) | Mua & giữ giỏ 6 tài sản | +1.089$ | +27,2% | 39,1% |
| 2026 (trong mẫu) | Mua & giữ BTC | -474$ | -11,9% | 40,0% |
| 2026 (trong mẫu) | Mua & giữ ETH | -1.020$ | -25,5% | 54,1% |
| 2026 (trong mẫu) | Mua & giữ OKB | +104$ | +2,6% | 42,0% |
| 2026 (trong mẫu) | Mua & giữ BNB | -761$ | -19,0% | 43,2% |
| 2026 (trong mẫu) | Mua & giữ Vàng | -411$ | -10,3% | 30,0% |
| 2026 (trong mẫu) | Mua & giữ Dầu WTI | +3.191$ | +79,8% | 42,0% |
| 2026 (trong mẫu) | Mua & giữ giỏ 6 tài sản | +105$ | +2,6% | 28,6% |


### Giả dược (200 lần, seed cố định)

| Bản · kỳ | Thật | Giả dược P5 | P50 | P95 | % lần giả dược lãi | Phân vị ($) | Tổng R thật | Tổng R giả dược P50 | Phân vị (R) |
|---|---|---|---|---|---|---|---|---|---|
| v1 · 2025 (ngoài mẫu) | -1.105$ | -1.568$ | -545$ | +1.064$ | 31% | 17 | -15,1 | -5,7 | 17 |
| v2 · 2025 (ngoài mẫu) | -1.715$ | -2.995$ | -1.234$ | +1.912$ | 23% | 41 | -14,7 | -9,4 | 45 |
| v1 · 2026 (trong mẫu) | +721$ | -1.444$ | -518$ | +1.091$ | 26% | 92 | 9,8 | -5,6 | 92 |
| v2 · 2026 (trong mẫu) | +1.927$ | -2.760$ | -1.258$ | +2.287$ | 21% | 94 | 28,2 | -12,3 | 94 |


_Giả dược giữ đúng số lệnh, tài sản, tháng khớp, khoảng SL%/TP1%/TP2% và cách quản lý của từng lệnh thật (v2: SL nến đóng + chặn 2×, vàng 100% ở TP1 và 6 nến); chỉ thay thời điểm vào (nến ngẫu nhiên cùng tháng, vào ở giá đóng) và chiều (50/50)._

## 2. Đóng góp từng thay đổi (chỉ để quy công — v2 chính thức KHÔNG chọn theo bảng này)

| Bản | 2025 lãi | 2025 lệnh | 2025 tổng R | 2025 DD | 2026 lãi | 2026 lệnh | 2026 tổng R | 2026 DD |
|---|---|---|---|---|---|---|---|---|
| v1 | -1.105$ | 68 | -15,1 | 33,9% | +721$ | 55 | 9,8 | 25,9% |
| v1 + 1. Đứng ngoài khi đi ngang | -718$ | 61 | -8,9 | 29,1% | +684$ | 53 | 9,4 | 25,9% |
| v1 + 2. Sau nến lớn → Fibo 0.5 | -856$ | 73 | -10,8 | 27,9% | +300$ | 54 | 5,1 | 24,0% |
| v1 + 3. Phá mốc rồi test lại | -1.407$ | 78 | -20,3 | 36,4% | +721$ | 63 | 10,0 | 24,4% |
| v1 + 4. SL theo nến đóng (+ chặn 2×) | -1.920$ | 67 | -31,0 | 54,9% | +1.090$ | 55 | 14,3 | 29,4% |
| v1 + 5. TP Fibo mở rộng 1 / 1.618 | +927$ | 244 | 19,7 | 29,1% | -621$ | 215 | -3,3 | 43,7% |
| v1 + Vàng: chỉ TP1, 6 nến | -1.208$ | 69 | -16,9 | 35,3% | +633$ | 56 | 8,8 | 24,1% |
| **v2 (đủ)** | -1.715$ | 264 | -14,7 | 55,4% | +1.927$ | 247 | 28,2 | 41,8% |
| v2 − 1. Đứng ngoài khi đi ngang | -1.839$ | 284 | -16,9 | 56,7% | +909$ | 254 | 18,4 | 39,6% |
| v2 − 2. Sau nến lớn → Fibo 0.5 | -1.794$ | 270 | -17,8 | 55,0% | +2.001$ | 250 | 28,5 | 40,5% |
| v2 − 3. Phá mốc rồi test lại | -940$ | 223 | -1,4 | 44,8% | +604$ | 204 | 13,3 | 38,2% |
| v2 − 4. SL theo nến đóng (+ chặn 2×) | -604$ | 278 | 2,4 | 44,1% | +2.063$ | 261 | 28,7 | 34,9% |
| v2 − 5. TP Fibo mở rộng 1 / 1.618 | -1.519$ | 73 | -22,1 | 40,5% | +1.346$ | 59 | 16,4 | 23,0% |
| v2 − Vàng: chỉ TP1, 6 nến | -1.417$ | 261 | -8,8 | 51,4% | +2.232$ | 233 | 30,8 | 43,6% |


_“v1 + X” = v1 chỉ bật thêm thay đổi X; “v2 − X” = v2 tắt riêng X. Các thay đổi tương tác nhau (vd TĐ2 thay hẳn kiểu vào, TĐ5 đổi đích nên đổi luôn tập lệnh qua R:R), nên tổng các phần không bằng tổng thể._

## 3. Theo tài sản

**2025 (ngoài mẫu)**

| Tài sản | v1 lệnh | v1 tổng R | v1 lãi | v2 lệnh | v2 L/S | v2 thắng | v2 tổng R | v2 lãi | Giá cả kỳ |
|---|---|---|---|---|---|---|---|---|---|
| BTC | 11 | -5,4 | -430$ | 62 | 28/34 | 35% | -3,0 | -413$ | -7,8% |
| ETH | 19 | -8,3 | -577$ | 57 | 29/28 | 28% | -20,4 | -1.366$ | -12,5% |
| OKB | 13 | 0,2 | +11$ | 46 | 16/30 | 52% | 20,0 | +926$ | +117,5% |
| BNB | 11 | -7,5 | -488$ | 39 | 19/20 | 49% | 2,6 | -92$ | +21,5% |
| Vàng | 9 | 6,4 | +406$ | 23 | 21/2 | 57% | 0,5 | +23$ | +64,8% |
| Dầu WTI | 5 | -0,4 | -27$ | 37 | 10/27 | 32% | -14,4 | -792$ | -19,3% |


**2026 (trong mẫu)**

| Tài sản | v1 lệnh | v1 tổng R | v1 lãi | v2 lệnh | v2 L/S | v2 thắng | v2 tổng R | v2 lãi | Giá cả kỳ |
|---|---|---|---|---|---|---|---|---|---|
| BTC | 9 | 1,2 | +61$ | 52 | 25/27 | 44% | 12,1 | +708$ | -11,8% |
| ETH | 10 | 2,0 | +106$ | 49 | 24/25 | 45% | 3,9 | +227$ | -25,4% |
| OKB | 10 | 4,4 | +361$ | 36 | 20/16 | 50% | 8,4 | +708$ | +2,7% |
| BNB | 3 | 0,6 | +40$ | 35 | 17/18 | 46% | -4,2 | -589$ | -18,9% |
| Vàng | 12 | -1,4 | -122$ | 43 | 12/31 | 49% | -9,2 | -1.101$ | -10,2% |
| Dầu WTI | 11 | 3,0 | +276$ | 32 | 22/10 | 50% | 17,1 | +1.973$ | +79,9% |


_Lãi/lỗ theo tài sản cộng các lệnh khớp; vì vốn dùng chung (rủi ro 2% số dư lúc khớp) nên $ phụ thuộc thứ tự lệnh, so sánh bằng tổng R chắc hơn._

## 4. Theo tháng (tháng khớp lệnh)

**2025 (ngoài mẫu)**

| Tháng | v1 lệnh | v1 tổng R | v1 đổi vốn | v2 lệnh | v2 tổng R | v2 đổi vốn |
|---|---|---|---|---|---|---|
| 2025-01 | 7 | -6,2 | -11,8% | 26 | 3,1 | +6,1% |
| 2025-02 | 5 | 7,2 | +14,9% | 17 | -7,2 | -16,6% |
| 2025-03 | 6 | -1,0 | -1,9% | 23 | -4,2 | -10,3% |
| 2025-04 | 9 | -2,8 | -5,6% | 28 | 6,6 | +8,1% |
| 2025-05 | 4 | -1,4 | -3,0% | 24 | -4,2 | -12,3% |
| 2025-06 | 3 | -3,1 | -6,1% | 19 | -6,7 | -9,7% |
| 2025-07 | 5 | -2,4 | -4,8% | 20 | -5,2 | -8,3% |
| 2025-08 | 0 | 0,0 | +0,0% | 16 | 7,0 | +9,8% |
| 2025-09 | 2 | 0,8 | +1,6% | 18 | -1,0 | -10,8% |
| 2025-10 | 8 | -3,9 | -7,7% | 31 | -2,8 | -4,8% |
| 2025-11 | 6 | -1,7 | -3,5% | 17 | 7,6 | +14,4% |
| 2025-12 | 13 | -0,7 | -1,6% | 25 | -7,8 | -14,0% |


**2026 (trong mẫu)**

| Tháng | v1 lệnh | v1 tổng R | v1 đổi vốn | v2 lệnh | v2 tổng R | v2 đổi vốn |
|---|---|---|---|---|---|---|
| 2026-01 | 3 | -2,1 | -4,1% | 24 | 12,5 | +29,0% |
| 2026-02 | 8 | -6,4 | -10,3% | 22 | 0,6 | -8,7% |
| 2026-03 | 6 | -3,5 | -9,0% | 28 | -12,5 | -17,2% |
| 2026-04 | 6 | 10,8 | +23,3% | 23 | 13,7 | +35,7% |
| 2026-05 | 5 | 5,5 | +11,2% | 28 | 1,8 | -4,3% |
| 2026-06 | 7 | -2,4 | -9,0% | 23 | 24,7 | +49,6% |
| 2026-07 | 5 | 0,6 | +5,2% | 28 | -14,8 | -21,5% |
| 2026-08 | 6 | -0,0 | -0,3% | 16 | 1,1 | +1,1% |
| 2026-09 | 5 | 3,2 | +6,3% | 29 | -10,5 | -17,2% |
| 2026-10 | 4 | 4,2 | +8,3% | 26 | 11,5 | +19,0% |


## 5. Long / Short, kiểu vào, kiểu kết thúc

**2025 (ngoài mẫu) — theo chiều**

| Bản | Chiều | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|---|
| v1 | LONG | 32 | 34% | -0,23 | -7,3 | -579$ |
| v1 | SHORT | 36 | 31% | -0,22 | -7,8 | -526$ |
| v2 | LONG | 123 | 45% | 0,04 | 4,9 | -77$ |
| v2 | SHORT | 141 | 36% | -0,14 | -19,5 | -1.637$ |


**2025 (ngoài mẫu) — v2 theo kiểu vào**

| Kiểu vào | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| Hồi về EMA34 (v1) | 161 | 43% | 0,02 | 2,5 | -446$ |
| Phá mốc → test lại | 92 | 35% | -0,16 | -15,2 | -1.098$ |
| Sau nến lớn → Fibo 0.5 | 11 | 45% | -0,18 | -2,0 | -171$ |


**2025 (ngoài mẫu) — kiểu kết thúc (v1 | v2)**

| v1 | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| Hết hạn | 9 | 89% | 0,61 | 5,5 | +358$ |
| SL | 45 | 0% | -1,04 | -46,8 | -3.252$ |
| TP1+HV | 3 | 100% | 0,83 | 2,5 | +183$ |
| TP1+Hết hạn | 1 | 100% | 1,88 | 1,9 | +120$ |
| TP1+TP2 | 10 | 100% | 2,18 | 21,8 | +1.487$ |


| v2 | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| Hết hạn | 79 | 75% | 0,59 | 47,0 | +2.737$ |
| SL(khẩn) | 36 | 0% | -2,04 | -73,6 | -4.618$ |
| SL(đóng) | 102 | 0% | -1,25 | -127,3 | -7.672$ |
| TP1(hết) | 2 | 100% | 1,55 | 3,1 | +228$ |
| TP1+HV(đóng) | 5 | 100% | 1,33 | 6,6 | +372$ |
| TP1+Hết hạn | 20 | 100% | 2,89 | 57,8 | +3.352$ |
| TP1+TP2 | 20 | 100% | 3,58 | 71,7 | +3.886$ |


**2026 (trong mẫu) — theo chiều**

| Bản | Chiều | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|---|
| v1 | LONG | 32 | 50% | 0,45 | 14,5 | +1.104$ |
| v1 | SHORT | 23 | 30% | -0,20 | -4,7 | -383$ |
| v2 | LONG | 120 | 45% | 0,08 | 10,0 | +350$ |
| v2 | SHORT | 127 | 49% | 0,14 | 18,2 | +1.577$ |


**2026 (trong mẫu) — v2 theo kiểu vào**

| Kiểu vào | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| Hồi về EMA34 (v1) | 147 | 46% | -0,02 | -3,3 | -484$ |
| Phá mốc → test lại | 88 | 47% | 0,25 | 21,6 | +1.595$ |
| Sau nến lớn → Fibo 0.5 | 12 | 67% | 0,82 | 9,8 | +816$ |


**2026 (trong mẫu) — kiểu kết thúc (v1 | v2)**

| v1 | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| Hết hạn | 6 | 100% | 1,58 | 9,5 | +780$ |
| SL | 32 | 0% | -1,07 | -34,1 | -2.632$ |
| TP1+HV | 1 | 100% | 0,91 | 0,9 | +60$ |
| TP1+Hết hạn | 2 | 100% | 1,66 | 3,3 | +257$ |
| TP1+TP2 | 14 | 100% | 2,16 | 30,2 | +2.256$ |


| v2 | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| Hết hạn | 95 | 69% | 0,49 | 46,9 | +4.764$ |
| SL(khẩn) | 27 | 0% | -2,05 | -55,2 | -5.754$ |
| SL(đóng) | 75 | 0% | -1,28 | -96,4 | -10.327$ |
| TP1(hết) | 4 | 100% | 1,82 | 7,3 | +804$ |
| TP1+HV(đóng) | 3 | 100% | 0,78 | 2,3 | +228$ |
| TP1+Hết hạn | 31 | 100% | 2,81 | 87,0 | +8.539$ |
| TP1+TP2 | 12 | 100% | 3,02 | 36,2 | +3.672$ |


_Kết quả v2: SL(đóng) = nến H4 đóng qua SL; SL(khẩn) = chạm chặn khẩn cấp 2×; TP1+HV(đóng) = sau TP1 nến đóng qua giá vào; TP1+khẩn = sau TP1 chạm SL danh nghĩa cũ; TP1(hết) = đóng 100% ở TP1 (vàng); Hết hạn = 18 nến (vàng 6)._

## 6. Phễu tín hiệu (lượt nến H4 khi tài sản chưa có lệnh/lệnh chờ)

| Bước | v1 2025 | v2 2025 | v1 2026 | v2 2026 |
|---|---|---|---|---|
| Không đủ luật 1+2 (xu hướng H4 2 cây) | 5366 | 4281 | 4274 | 3249 |
| Bị lọc D1 (luật 3) | 40 | 39 | 38 | 38 |
| Đi ngang: cắt EMA89 ≥ 6 lần/30 nến (TĐ1) | 0 | 251 | 0 | 164 |
| EMA chụm <0,6% (luật 4) | 322 | 211 | 206 | 139 |
| Thứ Hai (luật 5) | 683 | 487 | 608 | 402 |
| Nến lớn nhưng không có nhịp (TĐ2) | 0 | 0 | 0 | 0 |
| Nến lớn: Fibo 0.5 đã ở sau giá (TĐ2) | 0 | 11 | 0 | 14 |
| Thiếu căn cứ hội tụ (luật 7) | 555 | 414 | 513 | 419 |
| SL >6% (luật 8) | 79 | 65 | 93 | 93 |
| Không có đích (luật 9 / TĐ5) | 380 | 57 | 256 | 37 |
| R:R TP1 <1,5 | 2177 | 404 | 1919 | 328 |
| → ĐẶT LỆNH CHỜ | 661 | 724 | 571 | 568 |
| Hủy: giá chạm TP1 trước khi khớp | 469 | 159 | 418 | 114 |
| Hủy: mất xu hướng | 34 | 46 | 25 | 24 |
| Hủy: hết 6 nến chưa khớp | 90 | 244 | 70 | 170 |
| Hủy: đã đủ lệnh mở | 0 | 11 | 0 | 9 |
| Hủy: hết ký quỹ | 0 | 0 | 0 | 0 |
| Giảm khối lượng vì ký quỹ | 0 | 0 | 0 | 0 |
| **Lệnh khớp** | 68 | 264 | 55 | 247 |


**Kiểu phá mốc (TĐ3), v2** — số lượt có sự kiện phá 2 cây và kết cục của ứng viên này

| Kỳ | Sự kiện | Được chọn đặt lệnh | Qua luật nhưng EMA34 gần giá hơn | Thiếu hội tụ | R:R thấp | Không có đích | SL quá xa |
|---|---|---|---|---|---|---|---|
| 2025 (ngoài mẫu) | 351 | 173 | 28 | 44 | 102 | 0 | 4 |
| 2026 (trong mẫu) | 277 | 127 | 37 | 47 | 63 | 0 | 3 |


**Soi thay đổi 4 (SL nến đóng) và 5 (TP Fibo) — vì sao số lệnh tăng ~4 lần**

| Kỳ | Bản | Lệnh chờ đặt | Khớp | Tỉ lệ khớp | Hủy vì chạm TP1 trước | SL ngay nến khớp | R:R TB | TP1 cách giá vào TB | Giữ TB (giờ) | Chạm SL danh nghĩa mà không thua trọn: lệnh / R lấy lại | Thua theo nến đóng/khẩn: lệnh / R lỗ thêm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025 | v1 | 661 | 68 | 10% | 469 | 17 | 2,50 | 4,63% | 29 | — | — |
| 2025 | v1 + SL nến đóng | 660 | 67 | 10% | 469 | 14 | 2,52 | 4,65% | 36 | 5 / 6,4R | 40 / -21,4R |
| 2025 | v1 + TP Fibo | 795 | 244 | 31% | 192 | 23 | 3,20 | 5,95% | 44 | — | — |
| 2025 | v2 | 724 | 264 | 36% | 159 | 14 | 3,27 | 6,20% | 47 | 25 / 45,5R | 138 / -57,4R |
| 2026 | v1 | 571 | 55 | 10% | 418 | 6 | 2,70 | 4,58% | 37 | — | — |
| 2026 | v1 + SL nến đóng | 571 | 55 | 10% | 418 | 4 | 2,70 | 4,58% | 49 | 10 / 18,2R | 23 / -12,6R |
| 2026 | v1 + TP Fibo | 692 | 215 | 31% | 166 | 21 | 2,86 | 5,46% | 43 | — | — |
| 2026 | v2 | 568 | 247 | 43% | 114 | 11 | 2,93 | 5,45% | 50 | 32 / 51,1R | 102 / -45,5R |


_“R lấy lại” và “R lỗ thêm” so với mốc thua trọn theo SL giá ≈ −1,04R (ước lượng thô: coi mọi lệnh chạm SL danh nghĩa là lẽ ra thua trọn)._


## 7. Lệnh mẫu v2 (đối chiếu tay đầy đủ trong `tu_kiem_v2.txt`)

| Kỳ | Khớp | Tài sản | Chiều | Kiểu vào | Kết quả | R | Lãi | Chi tiết |
|---|---|---|---|---|---|---|---|---|
| 2025 | 2025-04-04 19 | ETH | SHORT | Hồi về EMA34 (v1) | TP1+TP2 | 10,49 | +610$ | vào 1831.47, SL 1,40%, R:R 8,0, Fractal, giữ 68 giờ |
| 2025 | 2025-01-15 15 | OKB | LONG | Phá mốc → test lại | TP1+TP2 | 6,61 | +477$ | vào 49.29, SL 2,20%, R:R 5,1, MocDoiVai+EMA200+Fractal, giữ 52 giờ |
| 2025 | 2025-01-15 03 | BTC | LONG | Phá mốc → test lại | TP1+Hết hạn | 6,50 | +470$ | vào 96258.9, SL 1,40%, R:R 6,0, MocDoiVai+EMA200+Fractal, giữ 72 giờ |
| 2025 | 2025-03-16 19 | OKB | LONG | Phá mốc → test lại | TP1+Hết hạn | 6,74 | +371$ | vào 45.94, SL 2,20%, R:R 6,7, MocDoiVai+EMA200, giữ 72 giờ |
| 2025 | 2025-01-22 15 | OKB | LONG | Hồi về EMA34 (v1) | SL(khẩn) | -2,03 | -175$ | vào 57.6353, SL 2,20%, R:R 1,9, Fractal, giữ 4 giờ |
| 2025 | 2025-02-12 23 | ETH | SHORT | Hồi về EMA34 (v1) | SL(khẩn) | -2,04 | -173$ | vào 2659.99, SL 1,67%, R:R 3,1, Fractal+Fibo0.5+Fibo0.618, giữ 8 giờ |
| 2025 | 2025-02-08 15 | OKB | SHORT | Hồi về EMA34 (v1) | SL(khẩn) | -2,03 | -170$ | vào 47.0844, SL 2,20%, R:R 1,8, Fractal, giữ 20 giờ |
| 2026 | 2026-06-03 15 | OKB | SHORT | Phá mốc → test lại | TP1+Hết hạn | 7,64 | +757$ | vào 84.5, SL 2,20%, R:R 6,6, MocDoiVai+Fractal, giữ 72 giờ |
| 2026 | 2026-06-10 23 | Dầu WTI | SHORT | Hồi về EMA34 (v1) | TP1+Hết hạn | 6,27 | +737$ | vào 90.9275, SL 1,70%, R:R 6,0, Fibo0.5, giữ 124 giờ |
| 2026 | 2026-04-24 23 | Dầu WTI | LONG | Phá mốc → test lại | TP1+Hết hạn | 7,83 | +721$ | vào 93.36, SL 1,70%, R:R 6,7, MocDoiVai+EMA34+EMA89+Fractal+Fibo0.5, giữ 124 giờ |
| 2026 | 2026-08-22 03 | OKB | LONG | Hồi về EMA34 (v1) | TP1+TP2 | 5,34 | +654$ | vào 103.492, SL 2,20%, R:R 4,1, Fractal+Fibo0.5, giữ 8 giờ |
| 2026 | 2026-07-01 19 | Vàng | SHORT | Hồi về EMA34 (v1) | SL(khẩn) | -2,07 | -311$ | vào 4045.21, SL 1,00%, R:R 2,4, Fractal+Fibo0.5+Fibo0.618, giữ 4 giờ |
| 2026 | 2026-07-09 03 | OKB | SHORT | Phá mốc → test lại | SL(khẩn) | -2,03 | -298$ | vào 78.14, SL 2,20%, R:R 2,2, MocDoiVai+Fractal, giữ 32 giờ |
| 2026 | 2026-08-26 23 | OKB | LONG | Hồi về EMA34 (v1) | SL(khẩn) | -2,03 | -276$ | vào 113.005, SL 2,20%, R:R 1,6, Fibo0.5+Fibo0.618, giữ 52 giờ |


_Mỗi kỳ: 4 lệnh lãi nhất + 3 lệnh lỗ nhất._


## 8. Nhận xét

<!-- NHAN_XET -->
_Viết tay sau lần chạy đầu (31/10/2026); số lấy từ các bảng trên. Không có tham số nào được chỉnh sau khi xem kết quả._

**Tổng thể**
- **2025 ngoài mẫu: v2 KHÔNG tốt hơn v1.**
  - Tổng R gần như bằng nhau: −14,7R so với −15,1R.
  - Tính bằng tiền thì v2 lỗ nặng hơn (−1.715$ so với −1.105$) và sụt giảm sâu hơn (55% so với 34%), vì số lệnh gấp ~4 lần (264 so với 68).
  - Giả dược: v2 ở phân vị 41, tức không khác vào lệnh ngẫu nhiên. v1 ở phân vị 17, còn kém cả ngẫu nhiên.
  - Cả hai đều thua mua & giữ giỏ 6 tài sản (+27%).
- **2026 trong mẫu: v2 hơn v1** (+28,2R / +1.927$ so với +9,8R / +721$; giả dược 94 so với 92). Nhưng 5 thay đổi được nghĩ ra từ lỗi của chính năm 2026, nên con số này lạc quan có hệ thống. Chênh lệch giữa 2026 và 2025 là dấu hiệu khớp quá mức vào dữ liệu đã học.
- Số lệnh tăng chủ yếu do **thay đổi 5**. Đích Fibo mở rộng xa hơn đích fractal, nên lệnh chờ ít bị hủy vì "giá chạm TP1 trước":
  - Hủy vì lý do này: 469 → 159 (2025).
  - Tỉ lệ khớp: 10% → 36–43%.
  - Thời gian giữ trung bình: ~30 → ~50 giờ.

**Thay đổi nào giúp / không giúp** (đo bằng tổng R, xét hai cách: "v1 + X" và "v2 − X")

| Thay đổi | 2025 ngoài mẫu | 2026 trong mẫu | Đánh giá |
|---|---|---|---|
| 1. Đứng ngoài khi đi ngang | +6,2R / +2,2R | −0,4R / +9,8R | **Giúp hoặc không hại**, ổn định nhất |
| 2. Sau nến lớn → Fibo 0.5 | +4,3R / +3,1R | −4,7R / −0,3R | Không rõ. Chỉ ~11 lệnh/năm |
| 3. Phá mốc rồi test lại | −5,2R / −13,3R | +0,2R / +14,9R | **Hại ngoài mẫu**, chỉ đẹp trong mẫu. Phá mốc 2025: 92 lệnh −15,2R; 2026: 88 lệnh +21,6R |
| 4. SL theo nến đóng (+ chặn 2×) | −15,9R / −17,1R | +4,5R / −0,5R | **Hại**. Có cứu được lệnh bị râu quét, nhưng lệnh thua sâu hơn hẳn: SL(đóng) trung bình −1,25R, chặn khẩn −2,04R, so với SL giá −1,04R |
| 5. TP Fibo mở rộng 1 / 1.618 | +34,8R / +7,4R | −13,1R / +11,8R | **Giúp ngoài mẫu**, nhưng đổi chiều trong mẫu khi đứng một mình. Đổi hẳn bản chất bot: nhiều lệnh hơn, giữ lâu hơn |
| Vàng chỉ TP1, 6 nến | −1,8R / −5,9R | −1,0R / −2,6R | **Hại nhẹ, cả 4 phép đo** |

- Nhìn theo kiểu vào của v2 năm 2025:
  - Hồi về EMA34 + TP Fibo: +2,5R / 161 lệnh, trong khi v1 thuần là −15,1R.
  - Phá mốc: −15,2R. Nến lớn: −2,0R.
  - Phần lỗ ngoài mẫu đến từ kiểu phá mốc và từ cách cắt lỗ theo nến đóng.
- Theo tài sản, 2025: v2 lỗ nặng ở ETH (−20,4R) và dầu (−14,4R), lãi ở OKB (+20,0R). Theo chiều: SHORT −19,5R, LONG +4,9R.

**Chưa trả lời được**
- Mẫu nhỏ, mỗi bảng con chỉ vài chục lệnh. Đổi dấu giữa 2 năm là chuyện thường.
- Bảng quy công trên chỉ để hiểu, **không** dùng nó để ghép một "v3 tốt nhất" rồi báo lại số 2025. Làm vậy là tối ưu trên ngoài mẫu (lỗi C1, C2 trong BAI_HOC.md).

**Ý kiến của tôi (tách riêng, không phải kết luận từ số liệu)**
- v2 chưa chứng minh được lợi thế. Ứng viên đáng giữ nhất là thay đổi 1 (đi ngang) và thay đổi 5 (đích Fibo). Thay đổi 3, 4 và luật vàng nên coi là chưa đạt.
- Muốn thử bộ "v1 + 1 + 5" thì phải **ghi giả thuyết trước** và chỉ kiểm trên dữ liệu chưa thấy, tức lệnh giấy từ 31/10/2026. Không chấm lại trên 2025.
- Lệnh giấy chạy song song v1 và v2 đúng như đã chốt. Nên để chạy ít nhất 2–3 tháng (~100+ lệnh v2) rồi mới so.
<!-- /NHAN_XET -->

<!-- DIEN_GIAI -->
## Diễn giải (chốt trước khi chạy — chọn một lần, không thử phương án khác)

**Phạm vi.** 6 tài sản BTC, ETH, OKB, BNB (OKX), VÀNG GC=F, DẦU CL=F (Yahoo). Vốn 4.000$, rủi ro 2% số dư đã chốt, tối đa 4 lệnh mở, phí vào 0,02% / ra 0,05%. 2026: 01/01 00:00 → 31/10 00:00 VN, dữ liệu `du_lieu/` (trong mẫu). 2025: 01/01/2025 00:00 → 01/01/2026 00:00 VN, dữ liệu `du_lieu_2025/` (ngoài mẫu). v1 để so = `chay.py` nguyên văn (luật 8 theo GIÁ — bản chốt), chạy trên đúng 6 tài sản với tối đa 4 lệnh (= biến thể E' của `chay.py`).

**Giữ nguyên v1** (gọi lại hàm của `chay.py`, không sửa file đó): xu hướng H4 (giá đóng so với dải EMA34 high/low, EMA89, EMA200) + 2 cây liên tiếp; lọc D1 (luật 3 — không nằm trong 5 thay đổi nên giữ); EMA chụm < 0,6%; thứ Hai không đặt lệnh và không khớp; một lệnh mỗi tài sản (tính cả lệnh chờ); lệnh chờ hiệu lực 6 nến, hủy khi chạm TP1 trước, khi mất xu hướng hoặc hết 6 nến; vùng hội tụ ±0,5%; SL danh nghĩa = đỉnh/đáy fractal 60 ngày gần giá vào nhất theo giá, sàn d_min, ×1,002, trần 6%; R:R tới TP1 ≥ 1,5; giữ tối đa 18 nến; đòn bẩy min(20, 60%/SL%); kiểm ký quỹ; thứ tự xử lý trong nến; đóng hết lúc cuối kỳ.

**Thay đổi 1 — đứng ngoài khi đi ngang.** Dấu s(i) = (đóng(i) ≥ EMA89(i)). Một lần "cắt" ở nến i khi s(i) ≠ s(i−1). Đếm trên 29 cặp nến liền nhau nằm trong cửa sổ 30 nến t−29..t. ≥ 6 lần → không đặt lệnh chờ mới (mọi kiểu vào). Lệnh chờ/vị thế đã có không bị hủy vì luật này. Kiểm sau lọc D1, trước EMA chụm (chỉ ảnh hưởng thứ tự ghi phễu).

**Thay đổi 2 — sau nến sập/bùng.**
- ATR14 kiểu Wilder (khởi tạo bằng trung bình 14 TR đầu).
- Nến i là "nến lớn" khi |đóng − mở| ≥ 2,5 × ATR14 của nến i−1 (thước đo tính tới trước nến đó, để nến lớn không tự làm to thước), cùng chiều xu hướng (SHORT: nến đỏ; LONG: nến xanh), i ∈ t−5..t. Nhiều nến → lấy nến gần nhất.
- Nhịp: đầu A = điểm xoay fractal đã xác nhận gần nhất (đỉnh cho SHORT, đáy cho LONG, 60 ngày) có chỉ số ≤ nến lớn; cuối B = cực trị râu từ nến A tới nến t (tính cả nến A).
- Giá vào = Fibo 0.5 = B + 0,5 × (A − B). Nếu mức này không còn ở phía hồi so với giá đóng nến t (SHORT cần giá vào > giá đóng) → bỏ ("Fibo đã qua"). Không có A → bỏ ("không có nhịp").
- Khi luật này bật, đây là kiểu vào DUY NHẤT (không vào EMA34, không xét phá mốc).
- Hội tụ: Fibo 0.5 tính là 1 căn cứ; cần thêm ≥ 1 trong {mép dải EMA34 gần giá, EMA89, EMA200, đỉnh/đáy fractal 30 ngày} trong ±0,5% quanh giá vào.

**Thay đổi 3 — phá mốc rồi test lại.**
- Sự kiện tại nến t (đã qua luật 1+2): SHORT — có đáy fractal 30 ngày mức L với đóng(t) < L, đóng(t−1) < L và đóng(t−2) ≥ L (cú phá 2 cây vừa hoàn tất đúng ở nến t); LONG đối xứng với đỉnh fractal.
- Nhiều mốc bị phá cùng lúc → lấy mốc gần giá đóng nhất (trùng thì mốc mới hơn).
- Giá vào = đúng L, hiệu lực 6 nến (như v1).
- Hội tụ: mốc đổi vai tính là 1; cần thêm ≥ 1 trong {mép dải EMA34 gần giá, EMA89, EMA200, fractal 30 ngày khác chính mốc đó, Fibo 0.5/0.618 của nhịp v1} trong ±0,5%.
- Nếu cùng nến cả kiểu EMA34 (v1) lẫn phá mốc đều qua hết các luật → chọn giá vào gần giá đóng hơn. Không kiểu nào qua → phễu ghi lý do của kiểu EMA34; phá mốc thống kê riêng.

**Thay đổi 4 — SL theo nến đóng.**
- SL danh nghĩa tính như v1; khối lượng vẫn theo SL danh nghĩa.
- Thoát khi nến H4 ĐÓNG qua SL (SHORT: đóng > SL; LONG: đóng < SL), ở giá đóng của nến đó.
- Chặn khẩn cấp theo giá = giá vào + 2 × (SL − giá vào): chạm râu là thoát ở mức đó (hoặc giá mở nếu nhảy cóc qua).
- Sau TP1: SL về giá vào (vẫn theo nến đóng), chặn khẩn cấp dời về SL danh nghĩa ban đầu — tức luôn cách mức SL đang dùng một khoảng SL danh nghĩa.
- Thứ tự trong nến: (1) chặn khẩn cấp; (2) TP1 — nếu cùng nến chạm luôn chặn khẩn cấp mới thì coi như chạm sau (bảo thủ) — rồi TP2; (3) cuối nến kiểm giá đóng qua SL. Nến khớp chỉ kiểm (1) và (3), không tính TP (như v1).
- Không mô phỏng thanh lý sàn. Với đòn bẩy 60%/SL%, lệnh isolate bị thanh lý ở khoảng −80% ký quỹ ≈ 1,33× SL, tức là TRƯỚC mức chặn 2× (khi SL% > 2% hoặc đòn bẩy chưa chạm trần x20). Ở đây giả định ký quỹ đủ; đánh thật phải hạ đòn bẩy (≤ 40%/SL%). Một lệnh vì thế có thể lỗ quá 1R (tới ~2R).

**Thay đổi 5 — TP bằng Fibo mở rộng 3 điểm.**
- A = đầu nhịp, B = cực trị cuối nhịp, C = giá vào. Kiểu EMA34 và phá mốc dùng nhịp của v1: A = điểm xoay đã xác nhận gần nhất ngược chiều lệnh (60 ngày), B = cực trị râu sau A tới nến t. Kiểu nến lớn dùng nhịp chứa nến lớn (thay đổi 2).
- TP1 = C + 1,0 × (B − A); TP2 = C + 1,618 × (B − A); mỗi mức lùi 0,2% về phía giá vào.
- Không có nhịp, hoặc TP1 đã nằm sau giá đóng nến t (giá đã tới đích) → bỏ ("không có đích"). R:R tới TP1 < 1,5 → bỏ.
- Chạm TP1: đóng 50%, SL về giá vào (theo thay đổi 4). Chạm TP2: đóng phần còn lại. Hủy lệnh chờ khi chạm TP1 trước khi khớp: dùng TP1 mới.

**Riêng VÀNG.** TP2 = TP1 (đóng 100% ở TP1); vị thế hết hạn sau 6 nến kể từ nến khớp (thay vì 18). Lệnh chờ vẫn hiệu lực 6 nến. d_min vàng giữ 0,8%.

**Giả dược (200 lần, seed 20261031).** Như v1: giữ số lệnh, tài sản, tháng khớp và khoảng SL%/TP1%/TP2% của từng lệnh thật; thay thời điểm vào (nến ngẫu nhiên cùng tháng, vào ở giá đóng) và chiều (50/50). Quản lý theo đúng bản đang thử: v1 = SL giá, 18 nến; v2 = SL nến đóng + chặn 2×, vàng 100% ở TP1 và 6 nến.

**Đóng góp từng thay đổi.** Chỉ để quy công, KHÔNG dùng để chọn luật. Chạy thêm "v1 + một thay đổi" và "v2 bỏ một thay đổi" trên cả 2 kỳ. v2 chính thức là bộ đủ 5 thay đổi + luật vàng như trên, bất kể kết quả các bản phụ.

**Lệnh giấy.** Dùng đúng bộ máy này (`v2.buoc`), xử lý tuần tự từng mốc đóng nến H4 kể từ 31/10/2026 00:00 VN. Vàng/dầu Yahoo trễ ~10 phút nên nến H4 chốt lúc +5 phút có thể thiếu vài phút cuối; nến đã xử lý không làm lại.
<!-- /DIEN_GIAI -->

## Tự kiểm

```
[2025] Bộ máy v2 với mọi thay đổi TẮT vs chay.mo_phong (6 tài sản, tối đa 4): 68 vs 68 lệnh, 0 lệnh lệch, số dư 2895.218458 vs 2895.218458
[2025] quyet_dinh_v2(tắt hết) vs chay.quyet_dinh trên 11625 nến: 0 lệch
[2025] Giả dược bộ máy (chế độ v1) vs chay.gia_duoc: trùng khít
[2025] Kiểm ràng buộc 264 lệnh v2 (thứ Hai, khớp trong 6 nến, không khớp/chạm TP1 sớm hơn, SL% & R:R, ≤4 lệnh, 1 lệnh/tài sản, không vào khi đi ngang, đúng kiểu nến lớn, vàng không TP2, SL(đóng)/khẩn đúng nến, số nến giữ) → 0 lỗi
[2025] Không nhìn trước: dựng lại chỉ báo (EMA, ATR, fractal, D1) với dữ liệu CẮT tại nến quyết định cho 108 mẫu (lệnh thật + nến xu hướng + nến lớn + phá mốc) → 108/108 cùng quyết định/giá vào/SL/TP/căn cứ/kiểu
[2025] Đối chiếu ngoai_mau/…/lenh_Ep.csv (v1, 6 tài sản, tối đa 4, agent khác chạy): 68 lệnh, lãi -1104.80$ vs ta 68 lệnh, -1104.78$
[2026] Bộ máy v2 với mọi thay đổi TẮT vs chay.mo_phong (6 tài sản, tối đa 4): 55 vs 55 lệnh, 0 lệnh lệch, số dư 4720.937481 vs 4720.937481
[2026] quyet_dinh_v2(tắt hết) vs chay.quyet_dinh trên 9676 nến: 0 lệch
[2026] Giả dược bộ máy (chế độ v1) vs chay.gia_duoc: trùng khít
[2026] Kiểm ràng buộc 247 lệnh v2 (thứ Hai, khớp trong 6 nến, không khớp/chạm TP1 sớm hơn, SL% & R:R, ≤4 lệnh, 1 lệnh/tài sản, không vào khi đi ngang, đúng kiểu nến lớn, vàng không TP2, SL(đóng)/khẩn đúng nến, số nến giữ) → 0 lỗi
[2026] Không nhìn trước: dựng lại chỉ báo (EMA, ATR, fractal, D1) với dữ liệu CẮT tại nến quyết định cho 108 mẫu (lệnh thật + nến xu hướng + nến lớn + phá mốc) → 108/108 cùng quyết định/giá vào/SL/TP/căn cứ/kiểu
[2026] Đối chiếu ngoai_mau/…/lenh_Ep.csv (v1, 6 tài sản, tối đa 4, agent khác chạy): 55 lệnh, lãi +720.95$ vs ta 55 lệnh, +720.94$
```

Chi tiết (lệnh mẫu từng nến, phép thử cắt cụt): `backtest/tu_kiem_v2.txt`. Danh sách lệnh: `lenh_v1_2025.csv`, `lenh_v2_2025.csv`, `lenh_v1_2026.csv`, `lenh_v2_2026.csv`.
