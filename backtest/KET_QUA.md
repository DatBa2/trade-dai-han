# KẾT QUẢ BACKTEST CƠ HỌC — bot bắt chước người phân tích BTC (FAM Trading)

_Sinh tự động bởi `backtest/chay.py` (chạy lại: `python3 backtest/chay.py`). Giai đoạn thi 2026-01-01 00:00 → 2026-10-31 00:00 giờ VN · vốn 4.000$ · phí vào 0,02% / ra 0,05% · bỏ funding. Tài sản A–D: BTC, ETH, NEAR, ZEC (OKX); E thêm OKB, BNB (OKX), vàng GC=F, dầu CL=F (Yahoo)._

> **CẢNH BÁO IN-SAMPLE.** Bộ luật được chắt lọc từ chính các buổi live của năm 2026, tức đúng giai đoạn đang thi. Kết quả dưới đây là kiểm tra *trong mẫu*: nó cho biết bộ luật cơ học có tái tạo được lợi thế trên giai đoạn mà luật được học hay không, **không** phải bằng chứng về hiệu quả trong tương lai. Không có tham số nào được dò/tối ưu; chỉ chạy các biến thể A–E đã chốt trước.

## 1. Bảng tổng

| Chiến lược | Lãi/lỗ | % | Số lệnh | Tỉ lệ thắng | R TB | Sụt giảm lớn nhất | Hệ số LN | Phân vị giả dược |
|---|---|---|---|---|---|---|---|---|
| **A** — Đúng luật (CHÍNH) | +1.383$ | +34,6% | 62 | 40% | 0,28 | 19,3% | 1,38 | 92 |
| **B** — Bỏ lọc D1 (luật 3) | +1.383$ | +34,6% | 62 | 40% | 0,28 | 19,3% | 1,38 | — |
| **C** — Như A, rủi ro 4%/lệnh | +2.649$ | +66,2% | 62 | 40% | 0,28 | 35,4% | 1,31 | — |
| **D** — Như A, chỉ BTC+ETH | +222$ | +5,5% | 19 | 42% | 0,17 | 13,8% | 1,25 | — |
| **E** — Luật A, 8 tài sản, tối đa 4 lệnh | +2.056$ | +51,4% | 98 | 41% | 0,24 | 26,2% | 1,36 | 97 |
| Mua & giữ BTC | -474$ | -11,9% | — | — | — | 40,0% | — | — |
| Mua & giữ ETH | -1.020$ | -25,5% | — | — | — | 54,1% | — | — |
| Mua & giữ NEAR | +7.445$ | +186,1% | — | — | — | 49,0% | — | — |
| Mua & giữ ZEC | +5.715$ | +142,9% | — | — | — | 63,1% | — | — |
| Mua & giữ giỏ 4 coin | +2.917$ | +72,9% | — | — | — | 45,5% | — | — |
| Mua & giữ OKB | +104$ | +2,6% | — | — | — | 42,0% | — | — |
| Mua & giữ BNB | -761$ | -19,0% | — | — | — | 43,2% | — | — |
| Mua & giữ Vàng | -411$ | -10,3% | — | — | — | 30,0% | — | — |
| Mua & giữ Dầu WTI | +3.191$ | +79,8% | — | — | — | 42,0% | — | — |
| Mua & giữ giỏ 8 tài sản | +1.724$ | +43,1% | — | — | — | 31,7% | — | — |


_R TB = lãi ròng (sau phí) ÷ số tiền rủi ro dự kiến của lệnh. Sụt giảm tính trên vốn theo giá thị trường mỗi nến H4. Mua & giữ: vốn 4.000$ chia đều, mua ở giá đóng H4 cuối trước 01/01 00:00 VN, bán cuối kỳ, phí 0,05% mỗi đầu._

### Giả dược (200 lần, seed cố định)

| Biến thể | Thật | Giả dược P5 | P50 | P95 | % lần giả dược lãi | Phân vị của thật ($) | Tổng R thật | Tổng R giả dược P50 | Phân vị (R) |
|---|---|---|---|---|---|---|---|---|---|
| A | +1.383$ | -1.595$ | -388$ | +1.641$ | 33% | 92 | 17,2 | -3,8 | 92 |
| E | +2.056$ | -1.916$ | -774$ | +1.282$ | 20% | 97 | 23,8 | -8,5 | 98 |


_Giả dược: giữ đúng số lệnh, tài sản, tháng khớp, khoảng cách SL%/TP1%/TP2% và cơ chế quản lý (50% ở TP1 → dời SL về giá vào, SL trước nếu cùng nến, hết hạn 18 nến) của từng lệnh thật; chỉ thay thời điểm vào (một nến H4 ngẫu nhiên trong cùng tháng, vào ở giá đóng) và chiều (ngẫu nhiên 50/50). Rủi ro 2% vốn hiện có mỗi lệnh, không giới hạn số lệnh mở. Phân vị = % số lần giả dược thua kết quả thật._

## 2. Phễu tín hiệu (số lượt đánh giá lúc nến H4 đóng, khi tài sản chưa có lệnh/lệnh chờ)

| Bước | A | B | C | D | E |
|---|---|---|---|---|---|
| Không đủ luật 1+2 (xu hướng H4 2 cây) | 3204 | 3204 | 3204 | 1654 | 5824 |
| Bị lọc D1 (luật 3) | 18 | 0 | 18 | 13 | 43 |
| EMA chụm <0,6% (luật 4) | 118 | 119 | 118 | 97 | 227 |
| Thứ Hai (luật 5) | 475 | 476 | 475 | 241 | 842 |
| Thiếu căn cứ hội tụ (luật 7) | 684 | 686 | 684 | 165 | 1032 |
| SL >6% (luật 8) | 142 | 142 | 142 | 41 | 194 |
| Không có đáy/đỉnh làm TP1 (luật 9) | 105 | 105 | 105 | 60 | 301 |
| R:R TP1 <1,5 (luật 9) | 883 | 890 | 883 | 619 | 2183 |
| → ĐẶT LỆNH CHỜ | 588 | 594 | 588 | 279 | 880 |
| Hủy: giá chạm TP1 trước khi khớp | 448 | 453 | 448 | 219 | 647 |
| Hủy: mất xu hướng | 22 | 23 | 22 | 11 | 36 |
| Hủy: hết 6 nến chưa khớp | 53 | 53 | 53 | 28 | 95 |
| Hủy: đã đủ lệnh mở | 0 | 0 | 0 | 0 | 0 |
| Hủy: hết ký quỹ | 0 | 0 | 0 | 0 | 0 |
| Giảm khối lượng vì ký quỹ | 0 | 0 | 0 | 0 | 0 |
| **Lệnh khớp** | 62 | 62 | 62 | 19 | 98 |


_Luật kiểm theo thứ tự 1→9; mỗi lượt chỉ ghi lý do bị loại ĐẦU TIÊN. Một xu hướng kéo dài sinh tín hiệu ở mọi nến nên các con số là lượt nến, không phải số “cơ hội” độc lập._

## 3. Biến thể A theo THÁNG (theo tháng khớp lệnh)

| Tháng | Số lệnh | Thắng | Tổng R | Lãi lệnh khớp trong tháng | Vốn cuối tháng | Đổi vốn trong tháng |
|---|---|---|---|---|---|---|
| 2026-01 | 4 | 25% | -2,2 | -181$ | 3.819$ | -4,5% |
| 2026-02 | 9 | 11% | -6,5 | -475$ | 3.344$ | -12,4% |
| 2026-03 | 7 | 57% | 6,8 | +464$ | 3.949$ | +18,1% |
| 2026-04 | 9 | 67% | 10,0 | +790$ | 4.598$ | +16,4% |
| 2026-05 | 6 | 67% | 4,2 | +395$ | 4.993$ | +8,6% |
| 2026-06 | 6 | 33% | 5,3 | +505$ | 5.498$ | +10,1% |
| 2026-07 | 7 | 43% | 2,8 | +279$ | 5.945$ | +8,1% |
| 2026-08 | 4 | 25% | -0,7 | -88$ | 5.688$ | -4,3% |
| 2026-09 | 4 | 75% | 3,6 | +412$ | 6.100$ | +7,2% |
| 2026-10 | 6 | 0% | -6,2 | -717$ | 5.383$ | -11,8% |


## 4. Biến thể A theo COIN

| Tài sản | Số lệnh | Long/Short | Thắng | R TB | Tổng R | Lãi/lỗ | Giá 01/01→30/10 (mua & giữ) |
|---|---|---|---|---|---|---|---|
| BTC | 9 | 6/3 | 44% | 0,13 | 1,2 | +91$ | -11,8% |
| ETH | 10 | 4/6 | 40% | 0,20 | 2,0 | +198$ | -25,4% |
| NEAR | 20 | 14/6 | 40% | 0,42 | 8,4 | +532$ | +186,4% |
| ZEC | 23 | 12/11 | 39% | 0,24 | 5,6 | +561$ | +143,1% |


## 5. Biến thể E theo TÀI SẢN (8 tài sản, tối đa 4 lệnh mở)

| Tài sản | Số lệnh | Long/Short | Thắng | R TB | Tổng R | Lãi/lỗ | Giá 01/01→30/10 (mua & giữ) |
|---|---|---|---|---|---|---|---|
| BTC | 9 | 6/3 | 44% | 0,13 | 1,2 | +73$ | -11,8% |
| ETH | 10 | 4/6 | 40% | 0,20 | 2,0 | +157$ | -25,4% |
| NEAR | 20 | 14/6 | 40% | 0,42 | 8,4 | +473$ | +186,4% |
| ZEC | 23 | 12/11 | 39% | 0,24 | 5,6 | +461$ | +143,1% |
| OKB | 10 | 8/2 | 50% | 0,44 | 4,4 | +550$ | +2,7% |
| BNB | 3 | 2/1 | 67% | 0,21 | 0,6 | +36$ | -18,9% |
| Vàng | 12 | 4/8 | 33% | -0,12 | -1,4 | -96$ | -10,2% |
| Dầu WTI | 11 | 8/3 | 36% | 0,27 | 3,0 | +402$ | +79,9% |


_Vàng = GC=F, dầu = CL=F (Yahoo, hợp đồng liên tục — có bước nhảy khi chuyển kỳ hạn). Nến H4 gộp từ H1, chỉ giữ nến có ≥3 giờ giao dịch; cuối tuần không có nến._


## 6. Biến thể A — 5 lệnh lãi nhất / 5 lệnh lỗ nhất

**Lãi nhất**

| Ngày khớp | Tài sản | Chiều | Kết quả | R | Lãi | Chi tiết |
|---|---|---|---|---|---|---|
| 2026-07-08 | ZEC | LONG | Hết hạn | 4,90 | +517$ | SL 2,20% (sàn d_min), R:R 7,8, căn cứ Fractal, giữ 72 giờ |
| 2026-06-02 | NEAR | LONG | TP1+TP2 | 4,91 | +490$ | SL 2,20% (sàn d_min), R:R 4,2, căn cứ Fractal, giữ 16 giờ |
| 2026-06-27 | ZEC | SHORT | TP1+TP2 | 4,54 | +458$ | SL 2,20% (sàn d_min), R:R 3,7, căn cứ Fractal, giữ 52 giờ |
| 2026-09-04 | NEAR | LONG | TP1+TP2 | 3,02 | +336$ | SL 2,20% (sàn d_min), R:R 2,9, căn cứ Fibo0.5, giữ 12 giờ |
| 2026-03-14 | NEAR | LONG | TP1+TP2 | 4,07 | +280$ | SL 2,20% (sàn d_min), R:R 3,4, căn cứ Fractal, giữ 68 giờ |


**Lỗ nhất**

| Ngày khớp | Tài sản | Chiều | Kết quả | R | Lãi | Chi tiết |
|---|---|---|---|---|---|---|
| 2026-10-11 | ZEC | SHORT | SL | -1,03 | -126$ | SL 2,20% (sàn d_min), R:R 1,9, căn cứ Fractal, giữ 4 giờ |
| 2026-07-21 | NEAR | LONG | SL | -1,03 | -124$ | SL 2,20% (sàn d_min), R:R 1,8, căn cứ EMA200+Fractal+Fibo0.5, giữ 4 giờ |
| 2026-10-22 | ZEC | LONG | SL | -1,03 | -123$ | SL 2,20% (sàn d_min), R:R 5,2, căn cứ EMA89+Fractal, giữ 4 giờ |
| 2026-07-31 | NEAR | SHORT | SL | -1,03 | -122$ | SL 2,20% (sàn d_min), R:R 2,9, căn cứ Fibo0.618, giữ 40 giờ |
| 2026-08-01 | ZEC | SHORT | SL | -1,03 | -122$ | SL 2,20% (sàn d_min), R:R 1,7, căn cứ Fractal+Fibo0.618, giữ 28 giờ |


_Kết quả: SL = chạm cắt lỗ trước TP1; TP1+HV = chốt 50% ở TP1 rồi phần còn lại về hòa vốn; TP1+TP2; Hết hạn = đóng sau 18 nến; TP1(hết) = TP2 trùng TP1 nên đóng hết ở TP1._


## 7. Biến thể A — mổ xẻ theo nhóm

**A — theo chiều**

| Chiều | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| LONG | 36 | 47% | 0,61 | 21,8 | +1.800$ |
| SHORT | 26 | 31% | -0,18 | -4,7 | -417$ |


**A — theo kiểu kết thúc**

| Kết quả | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| Hết hạn | 7 | 100% | 1,73 | 12,1 | +1.282$ |
| SL | 37 | 0% | -1,04 | -38,3 | -3.623$ |
| TP1+HV | 2 | 100% | 0,82 | 1,6 | +159$ |
| TP1+Hết hạn | 1 | 100% | 1,63 | 1,6 | +146$ |
| TP1+TP2 | 15 | 100% | 2,67 | 40,1 | +3.420$ |


**A — theo nguồn SL**

| Nguồn SL | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| sàn d_min | 49 | 37% | 0,24 | 11,8 | +799$ |
| đỉnh/đáy fractal | 13 | 54% | 0,41 | 5,3 | +584$ |


**A — theo căn cứ hội tụ (một lệnh có thể có nhiều căn cứ)**

| Căn cứ | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| EMA200 | 6 | 17% | -0,58 | -3,5 | -453$ |
| EMA89 | 2 | 50% | 0,33 | 0,7 | -1$ |
| Fibo0.5 | 10 | 50% | 0,30 | 3,0 | +327$ |
| Fibo0.618 | 15 | 27% | -0,41 | -6,1 | -550$ |
| Fractal | 50 | 40% | 0,31 | 15,3 | +1.204$ |


**A — theo số căn cứ ngoài EMA34**

| Số căn cứ | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| 1 | 46 | 43% | 0,47 | 21,7 | +1.901$ |
| 2 | 11 | 36% | -0,11 | -1,3 | -183$ |
| 3 | 5 | 20% | -0,66 | -3,3 | -336$ |


**A — theo R:R tới TP1**

| R:R | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| 1,5–2 | 16 | 62% | 0,53 | 8,5 | +608$ |
| 2–3 | 27 | 33% | 0,00 | 0,1 | -69$ |
| ≥3 | 19 | 32% | 0,45 | 8,5 | +844$ |


**E — theo chiều**

| Chiều | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| LONG | 58 | 48% | 0,53 | 31,0 | +2.818$ |
| SHORT | 40 | 30% | -0,18 | -7,2 | -762$ |


**E — theo kiểu kết thúc**

| Kết quả | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| Hết hạn | 11 | 100% | 1,82 | 20,0 | +2.082$ |
| SL | 58 | 0% | -1,05 | -60,9 | -5.675$ |
| TP1+HV | 3 | 100% | 0,85 | 2,6 | +217$ |
| TP1+Hết hạn | 2 | 100% | 1,66 | 3,3 | +310$ |
| TP1+TP2 | 24 | 100% | 2,45 | 58,8 | +5.121$ |


**E — theo nguồn SL**

| Nguồn SL | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| sàn d_min | 76 | 38% | 0,21 | 15,6 | +1.115$ |
| đỉnh/đáy fractal | 22 | 50% | 0,37 | 8,2 | +941$ |


**E — theo căn cứ hội tụ (một lệnh có thể có nhiều căn cứ)**

| Căn cứ | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| EMA200 | 7 | 29% | -0,20 | -1,4 | -192$ |
| EMA89 | 3 | 67% | 0,95 | 2,8 | +167$ |
| Fibo0.5 | 28 | 50% | 0,31 | 8,6 | +988$ |
| Fibo0.618 | 30 | 30% | -0,34 | -10,2 | -870$ |
| Fractal | 76 | 42% | 0,32 | 24,2 | +2.104$ |


**E — theo số căn cứ ngoài EMA34**

| Số căn cứ | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| 1 | 65 | 42% | 0,38 | 24,5 | +2.025$ |
| 2 | 21 | 38% | 0,02 | 0,4 | +166$ |
| 3 | 11 | 36% | -0,30 | -3,3 | -379$ |
| 4 | 1 | 100% | 2,09 | 2,1 | +245$ |


**E — theo R:R tới TP1**

| R:R | Số lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|
| 1,5–2 | 35 | 51% | 0,27 | 9,6 | +665$ |
| 2–3 | 37 | 35% | 0,07 | 2,7 | +218$ |
| ≥3 | 26 | 35% | 0,44 | 11,5 | +1.174$ |



## 8. Nhận xét

<!-- NHAN_XET -->
_Viết tay sau khi chạy; các con số lấy từ bảng trên và `lenh_A.csv`/`lenh_E.csv`. Đây là kết quả **trong mẫu** (luật học từ chính 2026)._

**Tổng thể**
- A lãi +1.383$ (+34,6%) sau 62 lệnh, R TB +0,28, hệ số LN 1,38, sụt giảm lớn nhất 19,3%. So với mua & giữ: hơn BTC (−11,9%) và ETH (−25,5%), nhưng kém giỏ 4 coin (+72,9%; sụt giảm 45,5%) vì NEAR (+186%) và ZEC (+143%) tăng rất mạnh.
- Giả dược: A ở phân vị 92, E ở phân vị 97. Tức là vào lệnh theo luật tốt hơn phần lớn các lần vào ngẫu nhiên có cùng khung SL/TP. Nhưng A **chưa qua mốc 95**, và R TB +0,28 với độ lệch chuẩn 1,8R trên 62 lệnh cho t ≈ 1,2 (E: t ≈ 1,4). **Chưa đủ để nói đây là lợi thế thống kê.**
- Kết quả **mong manh**:
  - 5 lệnh lãi nhất cộng lại +2.080$, nhiều hơn cả tổng lãi. 57 lệnh còn lại lỗ −698$ (−4,3R).
  - Chỉ đổi cách hiểu một câu chữ ở luật 8 (lấy đỉnh SL theo thời gian thay vì theo giá) là A rơi từ +34,6% xuống +3,4% (xem mục 9).

**Theo tháng (A)**
- Lỗ dồn vào tháng 2 (−12,4%, thắng 1/9 lệnh), tháng 10 (−11,8%, thắng 0/6), tháng 1 (−4,5%) và tháng 8 (−4,3%). Các tháng 3–7 và tháng 9 đều lãi.
- Cả 9 lệnh tháng 2 đều là SHORT, 8 lệnh dính SL. Đây là giai đoạn ngay sau cú sập về 60k (05–06/02): giá hồi lên ~70k rồi đi ngang trong vùng 63–70k.
- Riêng nến 23:00 ngày 13/02, 3 lệnh SHORT (BTC, ETH, NEAR) cùng khớp và cùng dính SL ngay trong nến đó, mất −3,1R một lúc. Giới hạn "tối đa 3 lệnh" không chặn được rủi ro tương quan.

**Theo coin (A, E)**
- Lãi chủ yếu đến từ NEAR (+8,4R, riêng LONG +12,6R) và ZEC (+5,6R).
- BTC (+1,2R / 9 lệnh) và ETH (+2,0R / 10 lệnh) gần hòa. Biến thể D (chỉ BTC+ETH) lãi +5,5% sau 19 lệnh, quá ít lệnh để kết luận.
- Như vậy, trên chính tài sản mà người phân tích tập trung (BTC), bộ luật cơ học gần như không tạo ra lãi trong giai đoạn này.
- Ở E: vàng là tài sản duy nhất lỗ (−1,4R / 12 lệnh). OKB (+4,4R) và dầu (+3,0R) lãi. Dầu và vàng là hợp đồng tương lai liên tục, có bước nhảy khi chuyển kỳ hạn.

**Luật nào gây lỗ / luật nào không có tác dụng**
- **Chiều SHORT lỗ, LONG lãi**: SHORT 26 lệnh, thắng 31%, −4,7R; LONG 36 lệnh, +21,8R. E cho kết quả cùng chiều (SHORT −7,2R).
  - Năm 2026 người phân tích nghiêng hẳn về downtrend, vậy mà phần SHORT cơ học lại thua.
  - Số liệu không cho biết nguyên nhân. Chỉ ghi nhận rằng altcoin tăng mạnh trong kỳ.
- **Luật 3 (lọc D1) gần như không bao giờ chặn lệnh**: chỉ 18 trên ~3.000 lượt đã có tín hiệu xu hướng 2 cây, nên B cho kết quả y hệt A.
  - Khi giá H4 đã nằm dưới (hoặc trên) cả 3 EMA H4 thì giá D1 hầu như luôn nằm đúng phía của dải EMA34 D1.
  - Trong đặc tả này, luật 3 là luật thừa.
- **Luật 6 + điều kiện hủy khi chạm TP1 loại phần lớn cơ hội**: 448/588 lệnh chờ (76%) bị hủy vì giá chạy tới TP1 trước khi hồi về EMA34. Chỉ ~11% lệnh chờ được khớp.
  - Trong số lệnh khớp, 10/37 lệnh SL dính SL **ngay trong nến khớp** (−10,4R). Đây là trường hợp giá vượt qua EMA34 một mạch rồi chạy thẳng tới SL.
- **Luật 7 (hội tụ)**: thêm căn cứ không làm kết quả tốt hơn.
  - 1 căn cứ ngoài EMA34: +0,47R/lệnh (46 lệnh). 2 căn cứ: −0,11R (11 lệnh). 3 căn cứ: −0,66R (5 lệnh).
  - Theo loại: Fibo 0.618 −6,1R (15 lệnh), EMA200 −3,5R (6 lệnh).
  - Mẫu quá nhỏ nên chỉ là dấu hiệu, không phải kết luận. Dù vậy nó ngược với ý "≥3 căn cứ là vùng cứng" trong sổ tay.
- **Luật 8**: sàn d_min quyết định SL ở 49/62 lệnh. Trên thực tế, SL phần lớn là phần trăm cố định (1,2% hoặc 2%), không đặt theo cấu trúc giá.
- **Luật 10 (hết hạn 18 nến)**: 7 lệnh hết hạn đều lãi (+12,1R), trong đó có lệnh lãi nhất (ZEC LONG +4,9R). TP1+TP2 đóng góp +40,1R qua 15 lệnh; SL lấy đi −38,3R qua 37 lệnh.
- **C (rủi ro 4%)**: lãi gần gấp đôi (+66,2%) nhưng sụt giảm cũng gần gấp đôi (35,4%), còn R TB giữ nguyên. Tức là "x2" chỉ phóng to cả lãi lẫn rủi ro chứ không tạo thêm lợi thế.
- Giới hạn 3 lệnh (E: 4) và ký quỹ **không lần nào bị chạm** (0 lệnh bị hủy vì hết chỗ). Vì vậy A–D và E có cùng tập lệnh trên phần tài sản chung.

**Đối chiếu tay** (`tu_kiem.txt`): đã dò từng nến cho 4 lệnh mẫu và thấy khớp.
- ZEC LONG 07/07: giá vào = EMA34 cao 455,15. Lệnh khớp ở nến thứ 6, khi râu thấp chạm 451,92. Hết 18 nến thì đóng ở 504,46, ra +4,90R.
- ETH SHORT 13/02: SL = sàn 1,2% × 1,002 = 2.022,5. TP1 = đáy 1.902,23 × 1,002. Nến khớp có đỉnh 2.050,6, vượt SL nên dính SL ngay trong nến đó.
- Các mốc D1 và đỉnh/đáy fractal dùng trong quyết định đều đã đóng hoặc đã xác nhận trước giờ ra quyết định.

**Ý kiến của tôi (tách riêng, không phải kết luận từ số liệu)**
- Đây mới là bằng chứng yếu, lại đo trong mẫu. Bước kiểm tra có giá trị tiếp theo là chạy **nguyên văn** bộ luật này trên giai đoạn ngoài mẫu (ví dụ nửa cuối 2025, hoặc từ 11/2026 trở đi), không sửa luật.
- Nếu muốn sửa luật thì ghi giả thuyết trước rồi mới kiểm. Hai ứng viên đáng xem: bỏ luật 3 (vì thừa) và cách xử lý lệnh chờ khi giá chạy tới TP1 trước.
<!-- /NHAN_XET -->

## 9. Cách diễn giải đặc tả (các chỗ đặc tả để ngỏ — chọn một lần, không thử phương án khác)

- **Fractal**: nến i là đỉnh nếu high[i] > high 3 nến trái và ≥ high 3 nến phải (đáy đối xứng); chỉ dùng từ khi nến i+3 đã đóng.
- **SL**: “đỉnh fractal gần nhất phía trên giá vào” = đỉnh fractal (60 ngày) **gần giá vào nhất theo giá** trong số các đỉnh cao hơn giá vào (LONG: đáy thấp hơn giá vào, gần nhất theo giá) — đọc theo chữ của đặc tả, đồng nhất với cách hiểu TP1. Không có thì dùng sàn d_min. _Minh bạch: lần chạy đầu tiên tôi hiểu là “đỉnh mới nhất theo thời gian” (A ra +136$, +3,4%); đọc lại câu chữ thì đổi sang theo giá và CHỐT luôn cách này trước khi xem kết quả mới — không chạy/so thêm phương án nào khác._
- **TP1**: đáy (SHORT) / đỉnh (LONG) fractal trong 60 ngày, **gần nhất theo giá**, và phải còn ở phía trước giá đóng của nến tín hiệu (đáy đã bị giá đóng xuyên qua coi như đã phá, không làm đích). Không có → bỏ lệnh (“không có đích”). TP2 = điểm xoay cùng loại kế tiếp xa hơn; không có → giá vào ∓ 3×SL; nếu 3×SL chưa qua TP1 thì đóng hết ở TP1.
- **Fibo**: nhịp = điểm xoay đã xác nhận gần nhất ngược chiều lệnh (đỉnh cho SHORT, đáy cho LONG, trong 60 ngày) → cực trị râu kể từ đó tới nến hiện tại; mức = cực trị + r×(đầu − cực trị).
- **Hội tụ**: đỉnh/đáy fractal 30 ngày tính cả đỉnh lẫn đáy; vì ngưỡng chỉ cần ≥1 căn cứ ngoài EMA34 nên đếm theo loại hay theo từng điểm cho cùng kết quả.
- **Thứ Hai** (giờ VN, theo giờ đóng nến H4): không đặt lệnh chờ mới và lệnh chờ cũ cũng **không được khớp** trong các nến đóng vào thứ Hai (vẫn tính vào 6 nến hiệu lực).
- **Một lệnh mỗi tài sản** tính cả lệnh chờ. Giới hạn 3 (E: 4) lệnh mở kiểm lúc khớp; đủ thì hủy lệnh chờ. Vốn để tính rủi ro = số dư đã chốt (gồm phần đã chốt TP1) lúc khớp.
- **Thứ tự trong nến**: (1) vị thế đang mở: SL trước, rồi TP1, TP2; nếu nến chạm TP1 mà cũng chạm lại giá vào → phần còn lại coi như hòa vốn (bảo thủ); (2) lệnh chờ: chạm giá vào → khớp (nến khớp chỉ kiểm SL, không tính TP vì không biết thứ tự); không chạm giá vào mà chạm TP1 → hủy; (3) lúc đóng nến: hết hạn 18 nến (đếm từ nến khớp), hủy lệnh chờ nếu xu hướng H4 không còn hoặc đã qua 6 nến; (4) tín hiệu mới. Nếu giá mở cửa đã vượt mức (gap) thì khớp ở giá mở cửa.
- **ZEC-USDT** chỉ có trên OKX từ 24/11/2025 → EMA200 H4 bắt đầu có từ ~27/12/2025, khởi động ngắn trong tháng 1. Vàng/dầu: D1 Yahoo, giờ đóng = 17:00 New York.
- Cuối kỳ (00:00 VN 31/10) lệnh còn mở đóng ở giá đóng nến H4 cuối cùng.


## 10. Tự kiểm

```
Kiểm không nhìn trước: dựng lại chỉ báo với dữ liệu CẮT CỤT tại nến quyết định cho 120 mẫu (8 tài sản) → 120/120 cho cùng quyết định/giá vào/SL/TP/căn cứ.
Kiểm ràng buộc trên 303 lệnh (A–E): không khớp/tín hiệu thứ Hai; khớp trong 6 nến và nến khớp có chạm giá vào; không có nến nào trước đó lẽ ra đã khớp hoặc đã chạm TP1; SL% trong [d_min, 6%]; R:R ≥ 1,5; không quá số lệnh mở; không 2 lệnh cùng tài sản → 0 lỗi.
```

Chi tiết đối chiếu tay từng nến của các lệnh mẫu: `backtest/tu_kiem.txt`.
