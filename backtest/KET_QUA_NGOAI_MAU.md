# KIỂM TRA NGOÀI MẪU — luật v1 (đã khóa)

_Sinh tự động bởi `backtest/ngoai_mau.py` (chạy lại: `python3 backtest/ngoai_mau.py`). Dùng nguyên các hàm của `chay.py`; từng lần chạy lẻ tái tạo được bằng `python3 backtest/chay.py --tu … --den … --tai-san BTC,ETH,OKB,BNB,VANG,DAU --dien-giai gia|thoi_gian --thu-muc-du-lieu …`. Vốn 4.000$ · phí vào 0,02% / ra 0,05% · bỏ funding · rủi ro 2% vốn/lệnh._

> **Thiết kế kiểm tra.** Luật v1 được chắt lọc từ các buổi live **năm 2026** → **2025 (01/01–31/12) là dữ liệu bot chưa từng thấy (ngoài mẫu)**. Không sửa luật, không dò tham số. Chỉ đổi: giai đoạn, rổ tài sản (chủ dự án chốt **BTC, ETH, OKB, BNB, vàng GC=F, dầu CL=F** — bỏ NEAR, ZEC), và chạy luật 8 theo **cả hai** cách đọc câu “đỉnh fractal gần nhất phía trên giá vào”: **(i) gần nhất theo GIÁ** (bản đang chốt) và **(ii) mới nhất theo THỜI GIAN** (bản chạy đầu). 2026 chạy lại trên đúng 6 tài sản để so cùng rổ.

> Biến thể: **A** = 6 tài sản, rủi ro 2%, tối đa 3 lệnh mở; **E'** = như A, tối đa 4 lệnh mở.

## 1. Bảng tổng

| Giai đoạn | Luật 8 | Biến thể | Lãi/lỗ | % | Lệnh | Thắng | R TB | t (R TB) | Sụt giảm | Hệ số LN | Phân vị giả dược ($) | Phân vị (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025 (ngoài mẫu) | (i) theo GIÁ | **A** — Luật v1, 6 tài sản, tối đa 3 lệnh | -1.105$ | -27,6% | 68 | 32% | -0,22 | -1,4 | 33,9% | 0,66 | 17 | 17 |
| 2025 (ngoài mẫu) | (i) theo GIÁ | **E'** — Luật v1, 6 tài sản, tối đa 4 lệnh | -1.105$ | -27,6% | 68 | 32% | -0,22 | -1,4 | 33,9% | 0,66 | 17 | 17 |
| 2025 (ngoài mẫu) | (ii) theo THỜI GIAN | **A** — Luật v1, 6 tài sản, tối đa 3 lệnh | -715$ | -17,9% | 42 | 36% | -0,22 | -1,1 | 27,0% | 0,65 | 20 | 20 |
| 2025 (ngoài mẫu) | (ii) theo THỜI GIAN | **E'** — Luật v1, 6 tài sản, tối đa 4 lệnh | -715$ | -17,9% | 42 | 36% | -0,22 | -1,1 | 27,0% | 0,65 | 20 | 20 |
| 2026 (trong mẫu, 6 TS) | (i) theo GIÁ | **A** — Luật v1, 6 tài sản, tối đa 3 lệnh | +721$ | +18,0% | 55 | 42% | 0,18 | 0,8 | 25,9% | 1,27 | 92 | 92 |
| 2026 (trong mẫu, 6 TS) | (i) theo GIÁ | **E'** — Luật v1, 6 tài sản, tối đa 4 lệnh | +721$ | +18,0% | 55 | 42% | 0,18 | 0,8 | 25,9% | 1,27 | 92 | 92 |
| 2026 (trong mẫu, 6 TS) | (ii) theo THỜI GIAN | **A** — Luật v1, 6 tài sản, tối đa 3 lệnh | +779$ | +19,5% | 43 | 47% | 0,24 | 1,0 | 21,8% | 1,40 | 98 | 98 |
| 2026 (trong mẫu, 6 TS) | (ii) theo THỜI GIAN | **E'** — Luật v1, 6 tài sản, tối đa 4 lệnh | +779$ | +19,5% | 43 | 47% | 0,24 | 1,0 | 21,8% | 1,40 | 98 | 98 |
| _Tham chiếu: 2026 gốc_ | (i) theo GIÁ | **A** — Đúng luật (CHÍNH) | +1.383$ | +34,6% | 62 | 40% | 0,28 | 1,2 | 19,3% | 1,38 | 92 | 92 |
| _Tham chiếu: 2026 gốc_ | (i) theo GIÁ | **E** — Luật A, 8 tài sản, tối đa 4 lệnh | +2.056$ | +51,4% | 98 | 41% | 0,24 | 1,4 | 26,2% | 1,36 | 97 | 98 |
| _Tham chiếu: 2026 gốc_ | (ii) theo THỜI GIAN | **A** — Đúng luật (CHÍNH) | +136$ | +3,4% | 36 | 39% | 0,07 | 0,3 | 21,0% | 1,08 | 72 | 72 |
| _Tham chiếu: 2026 gốc_ | (ii) theo THỜI GIAN | **E** — Luật A, 8 tài sản, tối đa 4 lệnh | +511$ | +12,8% | 63 | 41% | 0,13 | 0,7 | 27,3% | 1,17 | 82 | 82 |


_t (R TB) = R TB ÷ (độ lệch chuẩn R / √số lệnh) — |t| < 2 nghĩa là chưa phân biệt được với 0. Sụt giảm tính trên vốn theo giá thị trường mỗi nến H4. Tham chiếu 2026 gốc = bộ A–E của `KET_QUA.md` (A: BTC/ETH/NEAR/ZEC; E: 8 tài sản), chạy lại với cả 2 cách đọc luật 8._

_A và E' **trùng nhau từng lệnh** ở cả 4 lần chạy: số lệnh mở cùng lúc cao nhất ở E' = 2025 (i): 3, 2025 (ii): 3, 2026 (i): 3, 2026 (ii): 3; số lệnh chờ của A bị hủy vì đã đủ 3 lệnh mở = 0, 0, 0, 0 — có lúc mở đủ 3 lệnh nhưng chưa lần nào có lệnh thứ 4 cần khớp, nên giới hạn 3 hay 4 cho cùng kết quả. Các bảng chi tiết dưới đây vì vậy chỉ ghi A._

### Giả dược (200 lần, seed cố định — như `KET_QUA.md`)

| Giai đoạn | Luật 8 | Biến thể | Thật | Giả dược P5 | P50 | P95 | % giả dược lãi | Phân vị ($) | Tổng R thật | Tổng R giả dược P50 | Phân vị (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025 (ngoài mẫu) | (i) theo GIÁ | A | -1.105$ | -1.568$ | -545$ | +1.064$ | 31% | 17 | -15,1 | -5,7 | 17 |
| 2025 (ngoài mẫu) | (ii) theo THỜI GIAN | A | -715$ | -1.121$ | -277$ | +1.228$ | 36% | 20 | -9,2 | -2,7 | 20 |
| 2026 (trong mẫu, 6 TS) | (i) theo GIÁ | A | +721$ | -1.444$ | -518$ | +1.091$ | 26% | 92 | 9,8 | -5,6 | 92 |
| 2026 (trong mẫu, 6 TS) | (ii) theo THỜI GIAN | A | +779$ | -1.255$ | -376$ | +661$ | 30% | 98 | 10,2 | -4,3 | 98 |
| 2026 gốc | (i) theo GIÁ | A | +1.383$ | -1.595$ | -388$ | +1.641$ | 33% | 92 | 17,2 | -3,8 | 92 |
| 2026 gốc | (i) theo GIÁ | E | +2.056$ | -1.916$ | -774$ | +1.282$ | 20% | 97 | 23,8 | -8,5 | 98 |
| 2026 gốc | (ii) theo THỜI GIAN | A | +136$ | -1.187$ | -297$ | +1.035$ | 34% | 72 | 2,7 | -3,1 | 72 |
| 2026 gốc | (ii) theo THỜI GIAN | E | +511$ | -1.457$ | -447$ | +1.165$ | 32% | 82 | 7,9 | -4,7 | 82 |


_Giả dược: giữ số lệnh, tài sản, tháng khớp, khoảng SL%/TP1%/TP2% và cơ chế quản lý của từng lệnh thật; chỉ thay thời điểm vào (nến H4 ngẫu nhiên cùng tháng, vào ở giá đóng) và chiều (50/50). E' trùng A nên giả dược cũng trùng. Phân vị = % số lần giả dược thua kết quả thật._

### Mua & giữ (vốn 4.000$; giỏ = chia đều 6 phần)

| Tài sản | 2025 lãi | 2025 % | 2025 sụt giảm | 2026 lãi | 2026 % | 2026 sụt giảm |
|---|---|---|---|---|---|---|
| BTC | -317$ | -7,9% | 34,4% | -474$ | -11,9% | 40,0% |
| ETH | -504$ | -12,6% | 61,8% | -1.020$ | -25,5% | 54,1% |
| OKB | +4.690$ | +117,3% | 59,2% | +104$ | +2,6% | 42,0% |
| BNB | +855$ | +21,4% | 39,8% | -761$ | -19,0% | 43,2% |
| Vàng | +2.585$ | +64,6% | 10,4% | -411$ | -10,3% | 30,0% |
| Dầu WTI | -775$ | -19,4% | 31,5% | +3.191$ | +79,8% | 42,0% |
| giỏ 6 tài sản | +1.089$ | +27,2% | 39,1% | +105$ | +2,6% | 28,6% |


_Mua ở giá đóng H4 cuối trước 00:00 VN ngày đầu kỳ, bán cuối kỳ, phí 0,05% mỗi đầu. 2026 = 01/01 → 30/10._

## 2. Năm 2025 theo THÁNG (biến thể A, theo tháng khớp lệnh)

| Tháng | (i) lệnh | thắng | tổng R | đổi vốn | vốn cuối | (ii) lệnh | thắng | tổng R | đổi vốn | vốn cuối | BTC (mua & giữ) | Giỏ 6 TS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025-01 | 7 | 1/7 | -6,2 | -11,8% | 3.526$ | 4 | 1/4 | -3,1 | -6,0% | 3.759$ | +10,4% | +4,5% |
| 2025-02 | 5 | 4/5 | 7,2 | +14,9% | 4.052$ | 3 | 2/3 | 5,0 | +10,0% | 4.137$ | -20,3% | -15,5% |
| 2025-03 | 6 | 3/6 | -1,0 | -1,9% | 3.973$ | 4 | 3/4 | 1,1 | +2,2% | 4.229$ | -0,7% | +1,9% |
| 2025-04 | 9 | 2/9 | -2,8 | -5,6% | 3.750$ | 6 | 1/6 | -3,0 | -5,9% | 3.979$ | +12,7% | +0,5% |
| 2025-05 | 4 | 1/4 | -1,4 | -3,0% | 3.639$ | 2 | 0/2 | -2,1 | -4,1% | 3.815$ | +11,2% | +8,1% |
| 2025-06 | 3 | 0/3 | -3,1 | -6,1% | 3.415$ | 1 | 0/1 | -1,0 | -2,1% | 3.735$ | +2,9% | +1,1% |
| 2025-07 | 5 | 1/5 | -2,4 | -4,8% | 3.252$ | 4 | 1/4 | -1,3 | -2,8% | 3.632$ | +10,0% | +12,1% |
| 2025-08 | 0 | — | 0,0 | +0,0% | 3.252$ | 0 | — | 0,0 | +0,0% | 3.632$ | -8,0% | +40,7% |
| 2025-09 | 2 | 1/2 | 0,8 | +1,6% | 3.304$ | 1 | 0/1 | -1,0 | -2,1% | 3.556$ | +4,0% | +5,3% |
| 2025-10 | 8 | 2/8 | -3,9 | -7,7% | 3.049$ | 5 | 2/5 | -0,8 | -1,7% | 3.495$ | -2,6% | -7,5% |
| 2025-11 | 6 | 2/6 | -1,7 | -3,5% | 2.943$ | 4 | 1/4 | -2,9 | -5,7% | 3.295$ | -17,0% | -16,4% |
| 2025-12 | 13 | 5/13 | -0,7 | -1,6% | 2.895$ | 8 | 4/8 | -0,1 | -0,3% | 3.285$ | -3,9% | +0,1% |


## 3. Theo TÀI SẢN (biến thể A)

**2025 (ngoài mẫu)**

| Tài sản | (i) lệnh | L/S | thắng | tổng R | lãi | (ii) lệnh | L/S | thắng | tổng R | lãi | Giá cả kỳ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 11 | 5/6 | 18% | -5,4 | -430$ | 8 | 4/4 | 12% | -5,5 | -422$ | -7,8% |
| ETH | 19 | 8/11 | 21% | -8,3 | -577$ | 8 | 5/3 | 38% | -0,3 | -23$ | -12,5% |
| OKB | 13 | 4/9 | 46% | 0,2 | +11$ | 9 | 2/7 | 56% | 1,0 | +102$ | +117,5% |
| BNB | 11 | 4/7 | 18% | -7,5 | -488$ | 7 | 2/5 | 14% | -5,0 | -379$ | +21,5% |
| Vàng | 9 | 9/0 | 67% | 6,4 | +406$ | 6 | 6/0 | 67% | 2,8 | +169$ | +64,8% |
| Dầu WTI | 5 | 2/3 | 40% | -0,4 | -27$ | 4 | 2/2 | 25% | -2,2 | -162$ | -19,3% |


**2026 (trong mẫu, 6 TS)**

| Tài sản | (i) lệnh | L/S | thắng | tổng R | lãi | (ii) lệnh | L/S | thắng | tổng R | lãi | Giá cả kỳ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 9 | 6/3 | 44% | 1,2 | +61$ | 7 | 5/2 | 57% | 1,9 | +139$ | -11,8% |
| ETH | 10 | 4/6 | 40% | 2,0 | +106$ | 9 | 4/5 | 44% | 3,0 | +184$ | -25,4% |
| OKB | 10 | 8/2 | 50% | 4,4 | +361$ | 7 | 6/1 | 43% | 0,4 | +40$ | +2,7% |
| BNB | 3 | 2/1 | 67% | 0,6 | +40$ | 2 | 1/1 | 50% | 0,6 | +37$ | -18,9% |
| Vàng | 12 | 4/8 | 33% | -1,4 | -122$ | 8 | 4/4 | 38% | -0,6 | -46$ | -10,2% |
| Dầu WTI | 11 | 8/3 | 36% | 3,0 | +276$ | 10 | 8/2 | 50% | 4,8 | +424$ | +79,9% |


_Vàng = GC=F, dầu = CL=F (Yahoo, hợp đồng liên tục — có bước nhảy khi chuyển kỳ hạn). H4 gộp từ H1 (chỉ giữ nến có ≥3 giờ giao dịch)._

## 4. LONG vs SHORT (biến thể A)

| Lần chạy | Chiều | Lệnh | Thắng | R TB | Tổng R | Lãi/lỗ |
|---|---|---|---|---|---|---|
| 2025 (i) | LONG | 32 | 34% | -0,23 | -7,3 | -579$ |
| 2025 (i) | SHORT | 36 | 31% | -0,22 | -7,8 | -526$ |
| 2025 (ii) | LONG | 21 | 33% | -0,35 | -7,4 | -609$ |
| 2025 (ii) | SHORT | 21 | 38% | -0,09 | -1,8 | -106$ |
| 2026 (i) | LONG | 32 | 50% | 0,45 | 14,5 | +1.104$ |
| 2026 (i) | SHORT | 23 | 30% | -0,20 | -4,7 | -383$ |
| 2026 (ii) | LONG | 28 | 50% | 0,39 | 10,9 | +804$ |
| 2026 (ii) | SHORT | 15 | 40% | -0,05 | -0,7 | -25$ |


## 5. Kiểu kết thúc và nguồn SL (biến thể A)

| Kết quả | 2025 (i) | 2025 (ii) | 2026 (i) | 2026 (ii) |
|---|---|---|---|---|
| Hết hạn | 9 lệnh / 5,5R | 8 lệnh / 3,7R | 6 lệnh / 9,5R | 6 lệnh / 10,1R |
| SL | 45 lệnh / -46,8R | 26 lệnh / -27,0R | 32 lệnh / -34,1R | 23 lệnh / -24,6R |
| TP1+HV | 3 lệnh / 2,5R | 3 lệnh / 2,5R | 1 lệnh / 0,9R | 2 lệnh / 1,5R |
| TP1+Hết hạn | 1 lệnh / 1,9R | 0 lệnh / 0,0R | 2 lệnh / 3,3R | 2 lệnh / 2,9R |
| TP1+TP2 | 10 lệnh / 21,8R | 5 lệnh / 11,5R | 14 lệnh / 30,2R | 10 lệnh / 20,3R |


| Nguồn SL | 2025 (i) | 2025 (ii) | 2026 (i) | 2026 (ii) |
|---|---|---|---|---|
| sàn d_min | 42 lệnh / -7,0R | 21 lệnh / 0,0R | 42 lệnh / 2,6R | 26 lệnh / 2,1R |
| đỉnh/đáy fractal | 26 lệnh / -8,2R | 21 lệnh / -9,3R | 13 lệnh / 7,2R | 17 lệnh / 8,1R |


_Với cùng một tín hiệu, (i) chọn đỉnh/đáy gần giá vào nhất trong tập ứng viên, (ii) chọn phần tử mới nhất của cùng tập (có thể trùng) → SL theo (ii) luôn rộng bằng hoặc hơn (i), R:R tới TP1 bằng hoặc thấp hơn → nhiều tín hiệu bị luật 8 (SL > 6%) và luật 9 (R:R < 1,5) loại hơn, nên ít lệnh hơn._

## 6. Nhận xét

<!-- NHAN_XET -->
_Viết tay sau khi chạy; số liệu lấy từ các bảng trên và `ngoai_mau/*/lenh_A.csv`. Luật không sửa; E' trùng A nên chỉ nói A._

**Luật v1 có giữ được ngoài mẫu (2025) không?**
- **Không giữ được.** Cả hai cách đọc luật 8 đều lỗ: (i) −1.105$ (−27,6%, 68 lệnh), (ii) −715$ (−17,9%, 42 lệnh). R TB như nhau −0,22; hệ số LN 0,66 / 0,65; sụt giảm 33,9% / 27,0%.
- Giả dược: phân vị **17** (i) và **20** (ii) — vào lệnh theo luật còn kém ~80% số lần vào ngẫu nhiên có cùng khung SL/TP. Trong mẫu (2026, cùng 6 tài sản) cùng bộ luật ở phân vị 92 / 98.
- Giới hạn của số liệu: t của R TB là −1,4 (i) và −1,1 (ii), nên 2025 cũng **chưa đủ để nói luật có lợi thế âm**. Điều nói được: ngoài mẫu **không có dấu hiệu** lợi thế dương, và lợi thế thấy trong mẫu (vốn đã yếu: t = 0,8–1,0 trên 6 tài sản) không lặp lại.
- Mua & giữ 2025: giỏ 6 tài sản +27,2% (sụt giảm 39,1%), vàng +64,6%, OKB +117,3%; BTC −7,9%, ETH −12,6%, dầu −19,4%. Bot thua cả BTC lẫn giỏ.

**Ngã rẽ phân tích (luật 8)**
- Trên bộ gốc 2026 (A, 4 coin), chỉ đổi cách đọc một câu đã làm kết quả chênh **+34,6% (i) vs +3,4% (ii)**. Cách (i) được chốt sau khi đã thấy (ii) cho +3,4%.
- Chênh lệch đó **không lặp lại** ở chỗ khác: 2026 cùng 6 tài sản thì (ii) lại nhỉnh hơn (+19,5% vs +18,0%); 2025 thì (ii) lỗ ít hơn (−17,9% vs −27,6%) chỉ vì ít lệnh hơn (42 vs 68) — R TB mỗi lệnh y hệt (−0,22).
- Tức là con số +34,6% trong `KET_QUA.md` phụ thuộc mạnh vào một lựa chọn diễn giải được chốt sau khi xem kết quả, cộng với rổ tài sản: bỏ NEAR/ZEC thì A 2026 còn +18,0% (từ +34,6%).

**Theo tháng 2025**
- Lỗ rải đều, không do một cú sốc: cả (i) và (ii) đều 9/12 tháng âm. (i) chỉ dương tháng 2 (+14,9%, thắng 4/5) và tháng 9 (+1,6%); (ii) dương tháng 2 (+10,0%) và tháng 3 (+2,2%).
- Nặng nhất: tháng 1 ở (i) (−11,8%, thắng 1/7). Tháng 8 không có lệnh nào khớp (có tín hiệu đặt lệnh chờ nhưng đều bị hủy) — đúng tháng OKB tăng từ 47 lên 174 và giỏ mua & giữ +40,7%.

**Theo tài sản 2025**
- Lỗ ở BTC (−5,4R / 11 lệnh, thắng 18%), ETH (−8,3R / 19 lệnh), BNB (−7,5R / 11 lệnh); OKB gần hòa (+0,2R) dù giá +117%; dầu −0,4R.
- Vàng là tài sản duy nhất lãi rõ: +6,4R / 9 lệnh, cả 9 đều LONG, thắng 67%, trong năm vàng tăng một chiều +64,8%. Ở 2026 vàng lại lỗ (−1,4R). Mỗi tài sản chỉ 5–19 lệnh — quá ít để xếp hạng tài sản.
- BTC+ETH (đối tượng chính của người phân tích): 2025 −13,7R / 30 lệnh (i); 2026 +3,2R / 19 lệnh.

**LONG vs SHORT**
- Mẫu hình 2026 “LONG lãi, SHORT lỗ” không lặp lại: 2025 (i) LONG −7,3R / 32 lệnh, SHORT −7,8R / 36 lệnh; (ii) LONG −7,4R, SHORT −1,8R. Năm 2025 không có chiều nào lãi.

**Lỗ đến từ đâu (A, 2025 (i))**
- 45/68 lệnh (66%) dính SL trước TP1 (2026: 32/55 = 58%); TP1+TP2 chỉ 10/68 lệnh (2026: 14/55).
- 17 lệnh dính SL ngay trong nến khớp, cộng lại −17,7R — nhiều hơn mức lỗ ròng cả năm (−15,1R). 2026: 6 lệnh (−6,3R). Đây là mô tả, không suy ra được rằng bỏ các lệnh đó thì sẽ lãi.
- Lãi tập trung như trong mẫu: 5 lệnh lãi nhất +918$, 63 lệnh còn lại −2.023$.

**Ý kiến của tôi (tách riêng, không phải kết luận từ số liệu)**
- Phân vị giả dược tụt từ 92–98 (trong mẫu) xuống 17–20 (ngoài mẫu) là dấu hiệu quen thuộc của bộ luật khớp với giai đoạn được học. Nhưng một năm, 42–68 lệnh, vẫn là mẫu nhỏ: chưa phân biệt được “luật không có lợi thế” với “luật chỉ hợp chế độ thị trường kiểu 2026”.
- Không nên đưa v1 ra tiền thật. Nên ghi nhận 2025 là kết quả chính thức của v1 và **không sửa luật để “cứu” 2025** — sửa sau khi xem 2025 thì 2025 hết là ngoài mẫu.
- Nếu làm v2: viết giả thuyết và chốt mọi cách diễn giải trước (bài học luật 8), rồi cần một giai đoạn chưa dùng (vd chạy giấy từ 11/2026). Hai ứng viên giả thuyết đáng ghi: lệnh dính SL ngay nến khớp, và lệnh chờ bị hủy vì giá chạy tới TP1 trước.
<!-- /NHAN_XET -->

## 7. Dữ liệu và cách diễn giải

- **2025** dùng `backtest/du_lieu_2025/`: OKX BTC/ETH/OKB/BNB-USDT 4H từ 01/06/2024, 1Dutc từ 01/12/2023 (khởi động EMA ~7 tháng H4, ~13 tháng D1); Yahoo GC=F/CL=F H1 `range=730d` (Yahoo thực tế trả từ 10/06/2024 → **phủ trọn 2025, không phải lùi ngày bắt đầu của vàng/dầu**; EMA200 H4 có từ đầu 08/2024) gộp H4, D1 `range=5y`. **2026** dùng `backtest/du_lieu/` như lần chạy gốc.
- Toàn bộ luật, tham số, thứ tự xử lý trong nến, cách tính phí/ký quỹ/giả dược: giữ nguyên `chay.py` (xem `KET_QUA.md` mục 9). Chỉ luật 8 có công tắc `--dien-giai`: `gia` = đỉnh (SHORT) / đáy (LONG) fractal 60 ngày đã xác nhận, phía trên/dưới giá vào, **gần giá vào nhất**; `thoi_gian` = trong cùng tập đó lấy cái **mới nhất**. Sau đó vẫn áp sàn d_min, ×1,002, trần 6% như cũ.
- `--den` tính trọn ngày giờ VN: 2025 kết thúc 00:00 VN 01/01/2026, lệnh còn mở đóng ở giá đóng H4 cuối cùng trước mốc đó; không dữ liệu nào sau mốc này được dùng (vòng lặp, giả dược và đóng cuối kỳ đều cắt tại KET_THUC).
- Danh sách lệnh từng lần chạy: `backtest/ngoai_mau/<từ>_<đến>_<gia|thoi_gian>/lenh_A.csv`, `lenh_Ep.csv` (E'), kèm `tu_kiem.txt`.

## 8. Tự kiểm

```
[2025 (ngoài mẫu) · luật 8 (i) theo GIÁ]
  Kiểm không nhìn trước: dựng lại chỉ báo với dữ liệu CẮT CỤT tại nến quyết định cho 90 mẫu (6 tài sản) → 90/90 cho cùng quyết định/giá vào/SL/TP/căn cứ.
  Kiểm ràng buộc trên 136 lệnh (A/E'): không khớp/tín hiệu thứ Hai; khớp trong 6 nến và nến khớp có chạm giá vào; không có nến nào trước đó lẽ ra đã khớp hoặc đã chạm TP1; SL% trong [d_min, 6%]; R:R ≥ 1,5; không quá số lệnh mở; không 2 lệnh cùng tài sản → 0 lỗi.
[2025 (ngoài mẫu) · luật 8 (ii) theo THỜI GIAN]
  Kiểm không nhìn trước: dựng lại chỉ báo với dữ liệu CẮT CỤT tại nến quyết định cho 90 mẫu (6 tài sản) → 90/90 cho cùng quyết định/giá vào/SL/TP/căn cứ.
  Kiểm ràng buộc trên 84 lệnh (A/E'): không khớp/tín hiệu thứ Hai; khớp trong 6 nến và nến khớp có chạm giá vào; không có nến nào trước đó lẽ ra đã khớp hoặc đã chạm TP1; SL% trong [d_min, 6%]; R:R ≥ 1,5; không quá số lệnh mở; không 2 lệnh cùng tài sản → 0 lỗi.
[2026 (trong mẫu, 6 TS) · luật 8 (i) theo GIÁ]
  Kiểm không nhìn trước: dựng lại chỉ báo với dữ liệu CẮT CỤT tại nến quyết định cho 90 mẫu (6 tài sản) → 90/90 cho cùng quyết định/giá vào/SL/TP/căn cứ.
  Kiểm ràng buộc trên 110 lệnh (A/E'): không khớp/tín hiệu thứ Hai; khớp trong 6 nến và nến khớp có chạm giá vào; không có nến nào trước đó lẽ ra đã khớp hoặc đã chạm TP1; SL% trong [d_min, 6%]; R:R ≥ 1,5; không quá số lệnh mở; không 2 lệnh cùng tài sản → 0 lỗi.
[2026 (trong mẫu, 6 TS) · luật 8 (ii) theo THỜI GIAN]
  Kiểm không nhìn trước: dựng lại chỉ báo với dữ liệu CẮT CỤT tại nến quyết định cho 90 mẫu (6 tài sản) → 90/90 cho cùng quyết định/giá vào/SL/TP/căn cứ.
  Kiểm ràng buộc trên 86 lệnh (A/E'): không khớp/tín hiệu thứ Hai; khớp trong 6 nến và nến khớp có chạm giá vào; không có nến nào trước đó lẽ ra đã khớp hoặc đã chạm TP1; SL% trong [d_min, 6%]; R:R ≥ 1,5; không quá số lệnh mở; không 2 lệnh cùng tài sản → 0 lỗi.
Dữ liệu chồng lấn du_lieu/ ↔ du_lieu_2025/ (6 tài sản, 4H+1D): 22930 nến chung, 0 nến lệch giá.
Chạy lại bộ A–E gốc (luật 8 theo giá, cấu hình mặc định) bằng đường gọi mới → trùng từng byte với lenh_A..E.csv cũ.
Diễn giải (ii) trên bộ gốc A 2026 (4 coin) cho +136$ (+3,4%) — khớp con số của lần chạy đầu ghi trong KET_QUA.md mục 9 (+136$, +3,4%).
Vàng: H1 Yahoo bắt đầu 2024-06-10; 805 nến H4 trước 01/01/2025; EMA200 H4 có từ 2024-07-31 → phủ trọn 2025. Ngày thường (T2–T6, UTC) không có nến H4 trong 2025: 5 (01/01, 18/04, 01/09, 28/11, 25/12).
Dầu WTI: H1 Yahoo bắt đầu 2024-06-10; 782 nến H4 trước 01/01/2025; EMA200 H4 có từ 2024-08-01 → phủ trọn 2025. Ngày thường (T2–T6, UTC) không có nến H4 trong 2025: 5 (01/01, 18/04, 01/09, 28/11, 25/12).
```

Chi tiết đối chiếu tay từng nến (4 lệnh mẫu mỗi lần chạy): `backtest/ngoai_mau/*/tu_kiem.txt`.
