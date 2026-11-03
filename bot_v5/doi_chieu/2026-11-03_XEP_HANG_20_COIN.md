# Rà soát 20 coin vốn hóa lớn trên OKX — 03/11/2026

> **Ưu tiên setup chờ SHORT: DOGE → ETH → SUI → ADA → BTC. Chưa đề xuất vào market ngay.**
> Đây là xếp hạng ưu tiên theo dõi/vào khi đủ xác nhận, không phải bảng xác suất thắng hoặc thứ tự lợi nhuận chắc chắn.

## 1. Phạm vi và thời điểm

| Trường | Giá trị |
|---|---|
| gio_live | Khoảng 2026-11-03 09:42 VN, lúc nhận yêu cầu |
| gio_cat của hồ sơ nến | 2026-11-03 09:00 VN; H1 cuối 09:00, H4 và D1 cuối 07:00 |
| gio_phat_hanh | 2026-11-03 09:57 VN |
| Snapshot vốn hóa | CoinGecko, cập nhật nguồn 09:41:53 VN, tải khoảng 09:43 |
| Giá tham chiếu gần phát hành | 2026-11-03T09:56:56 VN, OKX perpetual |
| Funding tham chiếu | 2026-11-03T09:48:38 VN |
| Sản phẩm phân tích | Hợp đồng USDT perpetual OKX, không dùng giá spot thay cho giá hợp đồng |

Phạm vi là **20 coin lớn nhất có hợp đồng USDT perpetual đang live trên OKX**, sau khi bỏ stablecoin, tài sản quỹ và vàng token. Vì vậy đây không phải đúng 20 dòng đầu của bảng vốn hóa toàn cầu; danh sách đi tới hạng vốn hóa #31. XMR, WBT, RAIN không có hợp đồng tương ứng, LEO chỉ có spot nên không được xếp hạng kèo long/short ở đây. Không âm thầm thay chúng bằng một đồng nhỏ rồi gọi là top 20 toàn thị trường.

Nguồn chọn danh sách: [CoinGecko](https://www.coingecko.com/). Danh sách gốc và loại trừ được lưu trong [selection.json](../quet_thi_truong/2026-11-03_0943/selection.json), có cả hạng vốn hóa và lý do loại. Vốn hóa là USD tổng hợp toàn cầu, giá lệnh là USDT trên OKX; hai trường này không đồng nhất.

Các quote/vốn hóa lấy sau cutoff nến được ghi riêng, chỉ dùng để xem giá hiện tại còn gần vùng không và khả năng giao dịch. Không dùng chúng để giả vờ một nến H4 sau 07:00 đã đóng. Đây là phân tích hiện tại với nhiều lớp thời gian được công khai, không phải bài backtest tại 09:00.

## 2. Dùng công cụ nào và dựa vào đâu để xếp hạng?

1. CoinGecko API `coins/markets`, sắp vốn hóa giảm dần: xác định danh sách hiện tại, không dùng danh sách ghi nhớ từ tháng trước.
2. OKX API công khai `public/instruments`: xác nhận đúng mã và trạng thái live. Mỗi mã trong cache riêng được ánh xạ rõ sang `MA-USDT-SWAP`.
3. `bot_v5/ngu_canh.py` + `nen.py`: lấy nến đóng H4/D1/W1, EMA34/89/200/610 khi đủ lịch sử, RSI, ATR, pivot 3–3, râu, Fibo và trendline. Snapshot JSON/Markdown từng coin được lưu riêng.
4. H1 dùng 600 nến tới 09:00, tính bằng cùng hàm `phan_tich()`, để kiểm thời điểm vào. Không đủ EMA610 H1 và không cố điền.
5. Ticker OKX hiện tại: kiểm khoảng cách tới vùng, spread tức thời và volume 24h. Volume USDT là ước tính `volCcy24h × last`, không phải độ sâu sổ lệnh hoặc bảo đảm trượt giá.
6. Funding hiện tại được ghi làm chi phí tham chiếu, không dùng để chọn hướng giá. Dương: long trả short; âm: short trả long ở kỳ tính nếu mức đó được áp dụng. Mức snapshot có thể đổi trước kỳ tính.
7. Xếp hạng do bot cân nhắc: cấu trúc nhiều khung → vùng hội tụ rõ và mốc sai → khoảng trống tới các nấc chốt → độ gần vùng hiện tại và khả năng giao dịch → yếu tố làm phải chờ. Không có mô hình đã kiểm định dự báo xác suất thắng của bảng này.

Sổ tay phương pháp được lọc đúng ngày trước khi đọc (`_so_tay_T/20261103_0900`). Không đọc kết quả thật trong các file nhận định cũ để chọn coin. Những nhận xét bên dưới là suy luận từ hồ sơ hiện tại.

## 3. Mặt bằng thị trường và hành động chung

- **15/20** coin có phân loại H4 giảm theo thứ tự giá dưới EMA34/89/200.
- DOGE, ADA và XLM đồng thuận giảm theo bộ EMA trên H4/D1/W1; CC có H4/D1 giảm nhưng thiếu EMA dài tuần.
- HYPE/UNI/NEAR còn các dấu hiệu mạnh hơn trên khung lớn, nên không gom chúng chung một nhóm short trung hạn chỉ vì vừa có nến đỏ.
- HYPE và TRX là hai trường hợp đáng theo dõi khả năng phục hồi; **chưa có long được xác nhận** trong bản này.
- SOL, ZEC, NEAR và XLM có các dấu hiệu quá bán/xa vùng vào ở khung liên quan. Giảm mạnh không đồng nghĩa đang là chỗ bán tốt.
- Nhóm đầu hiện đều dưới vùng short chờ: **đứng ngoài chờ hồi và xác nhận**, không biến thứ hạng #1 thành lệnh market.
- Bảng nhãn EMA là output kỹ thuật. “Hỗn hợp” có thể do thứ tự các EMA chưa đồng thuận dù giá dưới cả ba; không tự suy ra PHÂN VÂN hoặc TĂNG.

## 4. Xếp hạng đủ 20 coin

| Ưu tiên | Coin | Hạng vốn hóa | Giá OKX hiện tại | H4 / D1 / W1 theo EMA | Hành động | Vùng theo dõi |
|---:|---|---:|---:|---|---|---|
| 1 | **DOGE** | #12 | 0,07396 | GIẢM / GIẢM / GIẢM | CHỜ SHORT | 0,07520–0,07560 |
| 2 | **ETH** | #2 | 2.253,23 | GIẢM / hỗn hợp / hỗn hợp | CHỜ SHORT | 2.280,00–2.293,00 |
| 3 | **SUI** | #30 | 0,86540 | GIẢM / hỗn hợp / thiếu EMA | CHỜ SHORT | 0,89100–0,89900 |
| 4 | **ADA** | #18 | 0,18770 | GIẢM / GIẢM / GIẢM | CHỜ SHORT | 0,19100–0,19200 |
| 5 | **BTC** | #1 | 76.799,3 | GIẢM / hỗn hợp / hỗn hợp | CHỜ SHORT | 77.900,0–78.050,0 |
| 6 | **LINK** | #17 | 11,048 | GIẢM / hỗn hợp / hỗn hợp | CHỜ SHORT | 11,450–11,580 |
| 7 | **XRP** | #5 | 1,2486 | GIẢM / hỗn hợp / hỗn hợp | CHỜ SHORT | 1,2520–1,2580 |
| 8 | **XLM** | #19 | 0,16148 | GIẢM / GIẢM / GIẢM | CHỜ HỒI, CHƯA SHORT ĐUỔI | 0,16600–0,16720 |
| 9 | **LTC** | #26 | 53,650 | GIẢM / hỗn hợp / hỗn hợp | CHỜ SHORT | 54,900–55,350 |
| 10 | **AVAX** | #29 | 8,3270 | GIẢM / hỗn hợp / GIẢM | CHỜ SHORT | 8,6300–8,7400 |
| 11 | **BNB** | #4 | 695,74 | GIẢM / hỗn hợp / hỗn hợp | CHỜ SHORT | 708,00–714,00 |
| 12 | **UNI** | #25 | 6,8310 | hỗn hợp / hỗn hợp / hỗn hợp | THEO DÕI, CHỜ H4 ĐÓNG | chờ cấu trúc |
| 13 | **BCH** | #20 | 274,06 | hỗn hợp / hỗn hợp / GIẢM | THEO DÕI | chờ cấu trúc |
| 14 | **HYPE** | #10 | 83,419 | hỗn hợp / hỗn hợp / thiếu EMA | DANH SÁCH LONG THEO DÕI, CHƯA VÀO | chờ cấu trúc |
| 15 | **TRX** | #8 | 0,32051 | hỗn hợp / hỗn hợp / hỗn hợp | THEO DÕI SỨC MẠNH, KHÔNG LONG ĐUỔI | chờ cấu trúc |
| 16 | **ZEC** | #11 | 1.135,37 | hỗn hợp / hỗn hợp / thiếu EMA | CHỜ HỒI, KHÔNG SHORT ĐUỔI | 1.176,00–1.186,00 |
| 17 | **SOL** | #7 | 91,880 | GIẢM / hỗn hợp / hỗn hợp | CHỜ HỒI, KHÔNG BẮT ĐÁY | chờ cấu trúc |
| 18 | **NEAR** | #21 | 3,8010 | GIẢM / hỗn hợp / hỗn hợp | ĐỨNG NGOÀI CHỜ ỔN ĐỊNH | chờ cấu trúc |
| 19 | **CC** | #28 | 0,09309 | GIẢM / GIẢM / thiếu EMA | ƯU TIÊN THẤP | chờ cấu trúc |
| 20 | **GRAM** | #31 | 1,1760 | GIẢM / thiếu EMA / thiếu EMA | ƯU TIÊN THẤP | chờ cấu trúc |

GRAM là tên mới của Toncoin trong nguồn hiện tại; đã đối chiếu [thông báo OKX](https://www.okx.com/en-us/help/okx-to-support-ton-crypto-migration). Không ghép tùy tiện lịch sử mã TON cũ để làm đủ EMA cho GRAM.

## 5. Năm setup ưu tiên: vùng vào, đích và mốc sai

**Điều kiện chung:** giá phải tới vùng; H1 xuất hiện từ chối tăng rõ, tạo hai đỉnh không vượt tiếp rồi nến giảm đóng có lực. Chạm vùng là điều kiện cần, chưa phải lệnh. Snapshot H1 tới 09:00 chưa có xác nhận tại các vùng chờ của top 5.

| Hạng | Coin | Chờ SHORT | Chốt nấc 1 | Chốt nấc 2 | Hủy setup khi H4 ĐÓNG trên |
|---:|---|---:|---:|---:|---:|
| 1 | DOGE | 0,07520–0,07560 | 0,07310–0,07330 | 0,07200–0,07230 | 0,07630 |
| 2 | ETH | 2.280,00–2.293,00 | 2.235,00–2.247,00 | 2.200,00–2.220,00 | 2.318,09 |
| 3 | SUI | 0,89100–0,89900 | 0,86300–0,86500 | 0,84000–0,84500 | 0,90860 |
| 4 | ADA | 0,19100–0,19200 | 0,18580–0,18630 | 0,18200–0,18400 | 0,19480 |
| 5 | BTC | 77.900,0–78.050,0 | 76.450,0–76.550,0 | 74.850,0–75.000,0 | 78.831,1 |

Hạn dự kiến: nấc 1 khoảng 1–3 ngày, tới 06/11; nấc 2 vài ngày tới khoảng một tuần, tới 10/11. Không chạm trong hạn phải đánh giá lại; không tự kéo dài hạn để né sai. Các mốc sai trong bảng áp dụng cho **setup chờ vào theo H4**, không trộn với một view D1 dài hơn để giữ lệnh đã sai.

### Chi tiết từng setup

#### #1 — DOGE

**Vì sao xếp ở đây:** H4, D1 và W1 đồng thuận giảm; vùng hồi có EMA34 low H4, EMA89 H1 và Fibo hội tụ; thanh khoản tốt hơn nhiều coin cùng nhóm yếu.

**Vùng chờ 0,07520–0,07560 có các căn cứ:**

- EMA34 low H4 0.0755003.
- EMA89 H1 0.0755553.
- Fibo 0.5 nhịp hồi H4 0.075435.
- Fibo 0.382 nhịp giảm D1 0.0756384 sát mép vùng.

**Đích:** TP1 râu H1 0.07312 + Fibo D1 0.786 khoảng 0.0729688; TP2 đáy D1 0.07204 + hỗ trợ trendline D1 khoảng 0.0722013.

**Mốc sai:** nến H4 **ĐÓNG trên 0,07630**. Mốc là cực trị cấu trúc trong hồ sơ, không phải một stop theo giá được bảo đảm khớp.

**Điểm trừ:** Giá chưa tới vùng; đáy/râu 0.07312 có thể tạo nhịp bật, không short đuổi.

Funding tham chiếu: 0,00674% mỗi kỳ theo snapshot. Volume OKX 24h ước tính khoảng 157,30 triệu USDT.

Từ giữa vùng vào tới giữa đích nấc 2, khoảng cách lợi nhuận chia khoảng cách tới mốc sai khoảng **3,6111 lần**. Đây chỉ là phép so khoảng cách giá, **không phải tỷ lệ lãi/lỗ thực hiện**: chờ nến đóng, phí, funding, trượt giá và nấc hỗ trợ gần có thể làm kết quả khác.

[Hồ sơ DOGE](../quet_thi_truong/2026-11-03_0943/DOGE.md) · [JSON](../quet_thi_truong/2026-11-03_0943/DOGE.json) · [H1](../quet_thi_truong/2026-11-03_0943/DOGE_H1.json) · [Ảnh chụp D1 OKX](../quet_thi_truong/2026-11-03_0943/DOGE_D1_OKX.png)

#### #2 — ETH

**Vì sao xếp ở đây:** Vùng hồi hẹp có nhiều căn cứ gần nhau, thanh khoản OKX rất cao; giá dưới EMA34/89/200 H4 và dưới các EMA chính ngày.

**Vùng chờ 2.280,00–2.293,00 có các căn cứ:**

- EMA34 close H4 2281.8098.
- Đáy D1 cũ 2281.02 đổi vai.
- Fibo 0.5 D1 2281.34.
- Fibo hồi H4 0.618 khoảng 2286.7545.
- Trendline H4 tại cutoff khoảng 2291.671.

**Đích:** TP1 râu 2236.06 + đáy 2246.23 + Fibo D1 0.5 khoảng 2244.805; TP2 Fibo D1 0.618 nhịp lớn 2217.0234 + EMA34 low W1 2203.7066 + Fibo D1 0.786 nhịp hồi 2202.886.

**Mốc sai:** nến H4 **ĐÓNG trên 2.318,09**. Mốc là cực trị cấu trúc trong hồ sơ, không phải một stop theo giá được bảo đảm khớp.

**Điểm trừ:** D1 được máy gắn HỖN HỢP do thứ tự EMA; vẫn còn các hỗ trợ gần 2236/2246, không bỏ qua nấc chốt đầu.

Funding tham chiếu: 0,01000% mỗi kỳ theo snapshot. Volume OKX 24h ước tính khoảng 5.679,20 triệu USDT.

Từ giữa vùng vào tới giữa đích nấc 2, khoảng cách lợi nhuận chia khoảng cách tới mốc sai khoảng **2,4217 lần**. Đây chỉ là phép so khoảng cách giá, **không phải tỷ lệ lãi/lỗ thực hiện**: chờ nến đóng, phí, funding, trượt giá và nấc hỗ trợ gần có thể làm kết quả khác.

[Hồ sơ ETH](../quet_thi_truong/2026-11-03_0943/ETH.md) · [JSON](../quet_thi_truong/2026-11-03_0943/ETH.json) · [H1](../quet_thi_truong/2026-11-03_0943/ETH_H1.json) · [Ảnh chụp D1 OKX](../quet_thi_truong/2026-11-03_0943/ETH_D1_OKX.png)

#### #3 — SUI

**Vì sao xếp ở đây:** Vùng hồi có Fibo, EMA và trendline mất vai trò hỗ trợ chụm nhau; đích D1 còn khoảng trống đáng xem hơn BTC ngay trên đáy.

**Vùng chờ 0,89100–0,89900 có các căn cứ:**

- EMA34 low H4 0.8933442.
- Trendline hỗ trợ H4 mất vai trò tại 0.8926792.
- Trendline giảm H4 khoảng 0.893617.
- Fibo hồi H4 0.618 khoảng 0.8912954.
- Trendline giảm D1 khoảng 0.8957676.

**Đích:** TP1 râu H4 0.8633 + Fibo D1 nhịp hồi 0.618 khoảng 0.8595868 sát phía dưới, còn hỗ trợ gần; TP2 trendline hỗ trợ D1 khoảng 0.8402285 + Fibo D1 nhịp hồi 0.786 khoảng 0.8449036. Đáy 0.8262 là nấc xa hơn, không bỏ qua 0.840–0.845.

**Mốc sai:** nến H4 **ĐÓNG trên 0,90860**. Mốc là cực trị cấu trúc trong hồ sơ, không phải một stop theo giá được bảo đảm khớp.

**Điểm trừ:** Chưa đủ EMA200 tuần; giá hiện tại đã ở dưới vùng vào khoảng vài phần trăm, không bán đuổi.

Funding tham chiếu: 0,01000% mỗi kỳ theo snapshot. Volume OKX 24h ước tính khoảng 49,900 triệu USDT.

Từ giữa vùng vào tới giữa đích nấc 2, khoảng cách lợi nhuận chia khoảng cách tới mốc sai khoảng **3,8603 lần**. Đây chỉ là phép so khoảng cách giá, **không phải tỷ lệ lãi/lỗ thực hiện**: chờ nến đóng, phí, funding, trượt giá và nấc hỗ trợ gần có thể làm kết quả khác.

[Hồ sơ SUI](../quet_thi_truong/2026-11-03_0943/SUI.md) · [JSON](../quet_thi_truong/2026-11-03_0943/SUI.json) · [H1](../quet_thi_truong/2026-11-03_0943/SUI_H1.json) · [Ảnh chụp D1 OKX](../quet_thi_truong/2026-11-03_0943/SUI_D1_OKX.png)

#### #4 — ADA

**Vì sao xếp ở đây:** H4/D1/W1 đồng thuận giảm; hỗ trợ cũ vừa mất giao Fibo hồi, mốc sai gần và rõ.

**Vùng chờ 0,19100–0,19200 có các căn cứ:**

- Hỗ trợ H4 đã phá và test lại khoảng 0.1911084.
- Đáy H4 cũ 0.1916 đổi vai.
- Fibo hồi H4 0.618 khoảng 0.1914384.
- EMA34 high H1 0.1912532.
- Fibo D1 nhịp hồi 0.382 khoảng 0.1910846.

**Đích:** TP1 râu H4/H1 0.186; TP2 đáy D1 0.182 + hỗ trợ tuần cũ 0.18384.

**Mốc sai:** nến H4 **ĐÓNG trên 0,19480**. Mốc là cực trị cấu trúc trong hồ sơ, không phải một stop theo giá được bảo đảm khớp.

**Điểm trừ:** RSI D1 30.5 sát quá bán, thanh khoản thấp hơn DOGE/ETH/SUI; funding hiện âm nên short trả phí nếu mức này giữ tới kỳ tính.

Funding tham chiếu: -0,00692% mỗi kỳ theo snapshot. Volume OKX 24h ước tính khoảng 26,000 triệu USDT.

Từ giữa vùng vào tới giữa đích nấc 2, khoảng cách lợi nhuận chia khoảng cách tới mốc sai khoảng **2,5758 lần**. Đây chỉ là phép so khoảng cách giá, **không phải tỷ lệ lãi/lỗ thực hiện**: chờ nến đóng, phí, funding, trượt giá và nấc hỗ trợ gần có thể làm kết quả khác.

[Hồ sơ ADA](../quet_thi_truong/2026-11-03_0943/ADA.md) · [JSON](../quet_thi_truong/2026-11-03_0943/ADA.json) · [H1](../quet_thi_truong/2026-11-03_0943/ADA_H1.json)

#### #5 — BTC

**Vì sao xếp ở đây:** Thanh khoản cao, dễ đối chiếu cấu trúc và giữ view; Fibo hồi giao EMA34 low H4 quanh 78k.

**Vùng chờ 77.900,0–78.050,0 có các căn cứ:**

- EMA34 low H4 78020.9751.
- Fibo hồi H4 0.618 khoảng 78004.3374.
- Fibo D1 nhịp lớn 0.382 tính từ hai cực trị trong hồ sơ quanh 77.9k.

**Đích:** TP1 EMA200 D1 76462.6941 + đáy H4 76472; phải đi qua đáy D1 76260 trước khi nhắm TP2. TP2 đáy tuần 74896.6 + Fibo D1 nhịp lớn 0.5 quanh 74.9k.

**Mốc sai:** nến H4 **ĐÓNG trên 78.831,1**. Mốc là cực trị cấu trúc trong hồ sơ, không phải một stop theo giá được bảo đảm khớp.

**Điểm trừ:** Ngay dưới giá có EMA200 D1 và đáy 76260; cơ hội ngắn tại giá hiện tại kém hơn các coin đầu, phải có hồi mới xét.

Funding tham chiếu: 0,01000% mỗi kỳ theo snapshot. Volume OKX 24h ước tính khoảng 5.014,10 triệu USDT.

Từ giữa vùng vào tới giữa đích nấc 2, khoảng cách lợi nhuận chia khoảng cách tới mốc sai khoảng **3,5627 lần**. Đây chỉ là phép so khoảng cách giá, **không phải tỷ lệ lãi/lỗ thực hiện**: chờ nến đóng, phí, funding, trượt giá và nấc hỗ trợ gần có thể làm kết quả khác.

[Hồ sơ BTC](../quet_thi_truong/2026-11-03_0943/BTC.md) · [JSON](../quet_thi_truong/2026-11-03_0943/BTC.json) · [H1](../quet_thi_truong/2026-11-03_0943/BTC_H1.json)

## 6. Vì sao những coin còn lại chưa lên nhóm đầu?

### #6 — LINK — CHỜ SHORT

**Điểm đáng chú ý:** Fibo hồi 11.4655–11.578 giao EMA34 và trendline H4 11.4867.

**Lý do chờ/giảm ưu tiên:** Giá còn xa vùng; EMA200 D1 11.012 là hỗ trợ gần, không short sát 11.0.

Vùng theo dõi: **11,450–11,580**, chưa phải entry được xác nhận.

[Hồ sơ LINK](../quet_thi_truong/2026-11-03_0943/LINK.md) · [JSON](../quet_thi_truong/2026-11-03_0943/LINK.json) · [H1](../quet_thi_truong/2026-11-03_0943/LINK_H1.json)

### #7 — XRP — CHỜ SHORT

**Điểm đáng chú ý:** Vùng vào tương đối gần: Fibo H4 khoảng 1.2526–1.2553, EMA34 low 1.2549 và đáy D1 cũ 1.2539.

**Lý do chờ/giảm ưu tiên:** Cấu trúc gần còn giằng co; hỗ trợ tuần 1.2461/H4 khoảng 1.2449 dễ gây bật; chưa có nến H1 từ chối rõ tại vùng.

Vùng theo dõi: **1,2520–1,2580**, chưa phải entry được xác nhận.

[Hồ sơ XRP](../quet_thi_truong/2026-11-03_0943/XRP.md) · [JSON](../quet_thi_truong/2026-11-03_0943/XRP.json) · [H1](../quet_thi_truong/2026-11-03_0943/XRP_H1.json)

### #8 — XLM — CHỜ HỒI, CHƯA SHORT ĐUỔI

**Điểm đáng chú ý:** H4/D1/W1 giảm đồng thuận; vùng hồi có Fibo, đáy cũ và EMA34 low H4.

**Lý do chờ/giảm ưu tiên:** H1 RSI 19 tại cutoff, giá rất xa vùng hồi; volume OKX thấp hơn nhóm đầu.

Vùng theo dõi: **0,16600–0,16720**, chưa phải entry được xác nhận.

[Hồ sơ XLM](../quet_thi_truong/2026-11-03_0943/XLM.md) · [JSON](../quet_thi_truong/2026-11-03_0943/XLM.json) · [H1](../quet_thi_truong/2026-11-03_0943/XLM_H1.json)

### #9 — LTC — CHỜ SHORT

**Điểm đáng chú ý:** Fibo hồi 54.965–55.2989 giao trendline hỗ trợ mất vai trò 55.0287 và EMA34 low H4 55.3368.

**Lý do chờ/giảm ưu tiên:** D1/W1 chưa đồng thuận rõ như DOGE/ADA, ngay dưới còn hỗ trợ D1 quanh 53.27 và đáy 52.77.

Vùng theo dõi: **54,900–55,350**, chưa phải entry được xác nhận.

[Hồ sơ LTC](../quet_thi_truong/2026-11-03_0943/LTC.md) · [JSON](../quet_thi_truong/2026-11-03_0943/LTC.json) · [H1](../quet_thi_truong/2026-11-03_0943/LTC_H1.json)

### #10 — AVAX — CHỜ SHORT

**Điểm đáng chú ý:** EMA34 close/high H4 8.648–8.742 giao Fibo hồi 8.6545–8.7448 và đỉnh cũ 8.636.

**Lý do chờ/giảm ưu tiên:** Có hỗ trợ tăng H4 quanh 8.337 gần giá; thanh khoản trung bình, chưa có entry xác nhận.

Vùng theo dõi: **8,6300–8,7400**, chưa phải entry được xác nhận.

[Hồ sơ AVAX](../quet_thi_truong/2026-11-03_0943/AVAX.md) · [JSON](../quet_thi_truong/2026-11-03_0943/AVAX.json) · [H1](../quet_thi_truong/2026-11-03_0943/AVAX_H1.json)

### #11 — BNB — CHỜ SHORT

**Điểm đáng chú ý:** Fibo H4 0.618 khoảng 708.43, EMA34 low H4 709.70 và EMA89 D1 712.13 hội tụ.

**Lý do chờ/giảm ưu tiên:** EMA200 D1 khoảng 692.44 ngay dưới giá, tuần chưa giảm rõ; không short tại hỗ trợ.

Vùng theo dõi: **708,00–714,00**, chưa phải entry được xác nhận.

[Hồ sơ BNB](../quet_thi_truong/2026-11-03_0943/BNB.md) · [JSON](../quet_thi_truong/2026-11-03_0943/BNB.json) · [H1](../quet_thi_truong/2026-11-03_0943/BNB_H1.json)

### #12 — UNI — THEO DÕI, CHỜ H4 ĐÓNG

**Điểm đáng chú ý:** H1 đã đóng dưới dải EMA34, giá hiện tại dưới hỗ trợ H4 quanh 6.98 sau cutoff lớn.

**Lý do chờ/giảm ưu tiên:** H4 cuối 07:00 còn kẹp EMA; W1 trên EMA34, D1 còn trên EMA89/200; không dùng giá đang chạy để kết luận phá H4 đã xác nhận.

Chưa chốt vùng entry đủ rõ trong bản này.

[Hồ sơ UNI](../quet_thi_truong/2026-11-03_0943/UNI.md) · [JSON](../quet_thi_truong/2026-11-03_0943/UNI.json) · [H1](../quet_thi_truong/2026-11-03_0943/UNI_H1.json)

### #13 — BCH — THEO DÕI

**Điểm đáng chú ý:** H4 nằm dưới dải EMA34 nhưng EMA89/200 chụm; D1 còn quanh hỗ trợ 273.8–274.8.

**Lý do chờ/giảm ưu tiên:** Cấu trúc hỗn hợp và đang sát hỗ trợ, không có lợi thế rõ để chen vào nhóm đầu.

Chưa chốt vùng entry đủ rõ trong bản này.

[Hồ sơ BCH](../quet_thi_truong/2026-11-03_0943/BCH.md) · [JSON](../quet_thi_truong/2026-11-03_0943/BCH.json) · [H1](../quet_thi_truong/2026-11-03_0943/BCH_H1.json)

### #14 — HYPE — DANH SÁCH LONG THEO DÕI, CHƯA VÀO

**Điểm đáng chú ý:** W1 còn trên EMA34/89, D1 trên EMA89/200 và quanh EMA34 close; mạnh tương đối hơn nhiều altcoin.

**Lý do chờ/giảm ưu tiên:** H4 đã mất đáy 86.292, H1 yếu và giá đang về cụm 82.5–83.4; cần cấu trúc hồi mới, chưa có long xác nhận. Không chọn short trung hạn ngược W1.

Chưa chốt vùng entry đủ rõ trong bản này.

[Hồ sơ HYPE](../quet_thi_truong/2026-11-03_0943/HYPE.md) · [JSON](../quet_thi_truong/2026-11-03_0943/HYPE.json) · [H1](../quet_thi_truong/2026-11-03_0943/HYPE_H1.json)

### #15 — TRX — THEO DÕI SỨC MẠNH, KHÔNG LONG ĐUỔI

**Điểm đáng chú ý:** Là coin duy nhất trong lượt giá đầu tăng 24h; H1 đi lên, giá H4 đã vượt đỉnh 0.31615.

**Lý do chờ/giảm ưu tiên:** H4 còn trong dải EMA34 và dưới EMA89/200; D1 chưa khỏe, H1 RSI 72.3; vừa có biến động bất thường râu 0.36715/0.30058 nên không ép lệnh.

Chưa chốt vùng entry đủ rõ trong bản này.

[Hồ sơ TRX](../quet_thi_truong/2026-11-03_0943/TRX.md) · [JSON](../quet_thi_truong/2026-11-03_0943/TRX.json) · [H1](../quet_thi_truong/2026-11-03_0943/TRX_H1.json)

### #16 — ZEC — CHỜ HỒI, KHÔNG SHORT ĐUỔI

**Điểm đáng chú ý:** Mất nhiều đáy H4; vùng hồi có đáy cũ 1176.66/1181 và EMA34 low D1 gần vùng.

**Lý do chờ/giảm ưu tiên:** Giảm khoảng 9%/24h, ngay trên hỗ trợ 1118–1130; RSI H1 khoảng 31, biên độ lớn và tuần vẫn trên EMA34.

Vùng theo dõi: **1.176,00–1.186,00**, chưa phải entry được xác nhận.

[Hồ sơ ZEC](../quet_thi_truong/2026-11-03_0943/ZEC.md) · [JSON](../quet_thi_truong/2026-11-03_0943/ZEC.json) · [H1](../quet_thi_truong/2026-11-03_0943/ZEC_H1.json)

### #17 — SOL — CHỜ HỒI, KHÔNG BẮT ĐÁY

**Điểm đáng chú ý:** H4 dưới EMA34/89/200, mất các đáy 93.52/93.08.

**Lý do chờ/giảm ưu tiên:** RSI D1 25.7, H4 31; đã rơi khỏi đáy fractal gần nên chương trình không có hỗ trợ H4 phía dưới trong cửa sổ 150 nến. Thiếu hỗ trợ không có nghĩa chắc chắn sẽ giảm vô hạn.

Chưa chốt vùng entry đủ rõ trong bản này.

[Hồ sơ SOL](../quet_thi_truong/2026-11-03_0943/SOL.md) · [JSON](../quet_thi_truong/2026-11-03_0943/SOL.json) · [H1](../quet_thi_truong/2026-11-03_0943/SOL_H1.json)

### #18 — NEAR — ĐỨNG NGOÀI CHỜ ỔN ĐỊNH

**Điểm đáng chú ý:** H4 mất đáy 3.904, giá yếu rõ sau cú giảm khoảng 10.7%/24h.

**Lý do chờ/giảm ưu tiên:** H1 RSI 20.3, H4 27.3; EMA89 D1 3.761 ngay dưới và W1 còn mạnh, không short đuổi hoặc bắt đáy khi chưa có cấu trúc.

Chưa chốt vùng entry đủ rõ trong bản này.

[Hồ sơ NEAR](../quet_thi_truong/2026-11-03_0943/NEAR.md) · [JSON](../quet_thi_truong/2026-11-03_0943/NEAR.json) · [H1](../quet_thi_truong/2026-11-03_0943/NEAR_H1.json)

### #19 — CC — ƯU TIÊN THẤP

**Điểm đáng chú ý:** H4/D1 giảm, vùng Fibo 0.095815–0.096593 gần hỗ trợ cũ và EMA34 low H4.

**Lý do chờ/giảm ưu tiên:** Chỉ khoảng 1.6 triệu USDT volume OKX/24h ước tính, funding âm khá sâu -0.02388% tại snapshot; thiếu EMA89/200 tuần. Vốn hóa lớn không bảo đảm dễ giao dịch.

Chưa chốt vùng entry đủ rõ trong bản này.

[Hồ sơ CC](../quet_thi_truong/2026-11-03_0943/CC.md) · [JSON](../quet_thi_truong/2026-11-03_0943/CC.json) · [H1](../quet_thi_truong/2026-11-03_0943/CC_H1.json)

### #20 — GRAM — ƯU TIÊN THẤP

**Điểm đáng chú ý:** H4 giảm; vùng hồi quanh 1.2025–1.2099 có Fibo và trendline.

**Lý do chờ/giảm ưu tiên:** Lịch sử theo mã mới ngắn, thiếu EMA200 D1 và EMA34 W1; chỉ khoảng 2.4 triệu USDT volume OKX/24h. Không tự ghép lịch sử TON cũ vào GRAM.

Chưa chốt vùng entry đủ rõ trong bản này.

[Hồ sơ GRAM](../quet_thi_truong/2026-11-03_0943/GRAM.md) · [JSON](../quet_thi_truong/2026-11-03_0943/GRAM.json) · [H1](../quet_thi_truong/2026-11-03_0943/GRAM_H1.json)

## 7. Tin, giới hạn và cách dùng bảng

Lịch trong hồ sơ ghi JOLTS 03/11 22:00, NFP 06/11 20:30 VN; dataset chỉ có lịch, không có kết quả thực tế. Kiểm lại trước khi giữ lệnh qua tin. Polymarket trong repo còn snapshot cũ từ 31/10 nên không dùng để tăng độ chắc của xếp hạng này.

Phương pháp học chủ yếu từ BTC, chưa được kiểm định riêng cho cả 20 coin. Thứ hạng là nhận định tại một thời điểm, không phải bằng chứng chiến lược có lãi. Không đặt xác suất thắng 70–90% khi chưa đo được.

Dữ liệu mỗi coin có độ dài khác nhau; thiếu EMA thì để thiếu. Pivot chỉ được dùng khi có đủ ba nến bên phải đã đóng. Đáy/đỉnh của nhịp đang chạy được ghi chưa xác nhận, không đánh tráo thành pivot chắc chắn.

Bản này không tự vào lệnh. Khi giá tới vùng, cập nhật snapshot và đọc lại H1/H4; vùng tốt ở thời điểm hiện tại có thể mất giá trị trước khi khớp. Cần phân biệt coin đáng theo dõi với coin đã đủ điều kiện giao dịch.

## 8. Bằng chứng hình ảnh và dữ liệu

[Bảng chart H4 tổng hợp 20 coin](../quet_thi_truong/2026-11-03_0943/tong_hop_H4.png) là hình dựng từ OHLC thật, chỉ tới nến đóng 07:00; các mức đánh dấu top 5 là chú thích của bot.

Ảnh chụp web thật: [DOGE D1](../quet_thi_truong/2026-11-03_0943/DOGE_D1_OKX.png) · [ETH D1](../quet_thi_truong/2026-11-03_0943/ETH_D1_OKX.png) · [SUI D1](../quet_thi_truong/2026-11-03_0943/SUI_D1_OKX.png). Ảnh chụp sau cutoff có cây cuối đang chạy; không lấy cây này làm xác nhận. MA(5/10/20) mặc định trên ảnh khác các EMA tính trong hồ sơ.

Nguồn thô: [vốn hóa](../quet_thi_truong/2026-11-03_0943/von_hoa.json), [hợp đồng OKX](../quet_thi_truong/2026-11-03_0943/okx_swap.json), [quote/funding](../quet_thi_truong/2026-11-03_0943/gia_funding_moi.json), [kế hoạch và thứ hạng](../quet_thi_truong/2026-11-03_0943/ke_hoach.json).

## Nhận định thật của người đó (Claude ghi từ transcript, sau khi bot đã trả lời)

Buổi live [i0N3Yho0JvE](https://www.youtube.com/watch?v=i0N3Yho0JvE) 03/11 10:07, phần altcoin 01:06–01:18 (trả lời câu
hỏi viewer, không rà cả thị trường). Bot lưu bản này lúc 09:57, trước buổi live.

- **Chung**: «toàn bộ altcoin bây giờ… mức trung bình thôi chứ cũng không phải là mức quá tốt hay quá xấu»; ngắn hạn thì
  "follow theo nhịp chung của market". Không đưa setup short altcoin nào. Bot đưa 5 setup chờ short (DOGE, ETH, SUI, ADA,
  BTC) — người đó không bàn tới DOGE / SUI / ADA.
- **ETH**: viewer hỏi "sao ETH khỏe hơn BTC" → «Từ đỉnh… ETH nó mới gãy có 20%… Bitcoin thì nó gãy độ 11%» (00:32:12), tức
  ETH yếu hơn. Khớp với bot xếp ETH #2 chờ short.
- **BNB**: «khá là nhạy cảm ở cái đợt này… khoan đụng đã» (01:13:31; Binance vừa bị hack). Bot: #11 chờ short 708–714 —
  lệch nhẹ: người đó đứng ngoài cả hai phía vì tin.
- **NEAR**: «về đến 38 39 rồi… tiệm cận là xong được cái view hôm trước» (view cũ 3,6–3,7), không dám mua vì tâm lý. Bot:
  đứng ngoài chờ ổn định ✓.
- **SOL**: vai-đầu-vai D1 "đúng nhưng mà bây giờ nó gãy mất rồi", đang ở Fibo 0.5, "hội tụ đang gặp hỗ trợ". Bot: chờ hồi,
  không bắt đáy ✓.
- **GRAM**: chờ một cây fake out — «một cái cây nến bán xuống mạnh kèm với volume lớn», RSI cắm dưới 30 — mới đáng xem.
  Bot: ưu tiên thấp ✓.
- **BCH**: viewer thấy nêm đi lên → «cái nêm này là cái nêm của sóng giảm chứ không phải nêm của sóng tăng» (01:09:23),
  đánh theo sóng giảm. Bot: theo dõi, cấu trúc hỗn hợp — bot không nhận ra nêm giảm.
- **LINK**: chỉ nhắc FOMO ở 15 nay −30%. **AAVE** (ngoài danh sách bot): ở Fibo; H4 đóng xanh → 140 trong tuần, thủng
  0.618 → test 110; chỉ mua dưới 8x. **WLD**: bỏ.

## 9. Kết quả thật — để trống cho lần đối chiếu sau

- Ngày ghi:
- Coin nào thực sự tới vùng và có H1 xác nhận:
- Entry thực tế nếu có:
- Nấc 1/nấc 2 có chạm trước khi H4 đóng qua mốc sai không:
- Sai ở lựa chọn coin, hướng, vùng, đích hay hạn:
- Thứ hạng có giúp chọn được setup tốt hơn các coin bị bỏ qua không:

Không chấm bảng theo việc coin giảm bao nhiêu kể từ lúc quét nếu entry chưa khớp. Giá đi đúng hướng nhưng không tới vùng không tạo ra một giao dịch thắng.
