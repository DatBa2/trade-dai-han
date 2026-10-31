# SỔ TAY BOT V5 — Phần 1: Hướng lớn · Giữ/lật view · Tin tức & Fed · Giữ/đóng lệnh trung hạn

> **Cập nhật**: 2026-10-31 12:41 · **Số buổi đã dùng**: 180 buổi có nhãn đầy đủ trong `hoc_v5/nhan/*.json` (2026-01-06 → 2026-10-30; T01: 19, T02: 9, T03: 25, T04: 18, T05: 13, T06: 19, T07: 21, T08: 19, T09: 18, T10: 19) · Bảng đo giữ/lật bằng giá: `hoc_v5/giu_lat/GIU_LAT.md` (tạo 2026-10-31 12:35).
> **Nguồn duy nhất là người đó** (BTC, kênh FAM Trading): câu trong "…" là lời họ, link mở đúng giây trong video. Phần **Tần suất** đếm trên nhãn từng buổi (`hoc_v5/nhan`) hoặc trên bảng đo giá (`GIU_LAT.md`), có ghi nguồn. Chỗ đánh **[đo]** là số máy đo trên giá/lịch (hành vi đo được của họ), không phải lời họ. Không có luật hay ý của người tổng hợp.
> **Từ ngữ**: *view* = hướng H4 TĂNG/GIẢM gần nhất của người đó trước buổi đang xét. **GIỮ** = buổi này cùng hướng. **LẬT** = ngược hướng. **PV** = phân vân. *Mốc sai* = mức giá họ nói "đóng qua đây thì view sai". *Nền* = tỉ lệ LẬT chung 24% (GIU_LAT).

## Bảng tra nhanh

| Mã | Tình huống | Người đó làm gì | Tần suất |
|---|---|---|---|
| A1 | Hỏi dài hạn / bất kỳ buổi nào | Pha chu kỳ: 2026 là năm downtrend, mọi nhịp tăng là hồi | view dài hạn GIẢM 105/119 = 88% buổi có nói |
| A2 | Thứ Hai, nến tuần vừa đóng | Đọc lại nến tuần, đặt view cho cả tuần | nhắc khung tuần 36/36 = 100% buổi thứ Hai |
| A3 | Buổi đầu tháng | Đọc nến tháng | 7/10 = 70% buổi đầu tháng |
| A4 | Đang có view D1/W1 | View D1 giữ trung vị 3 ngày, W1 6 ngày | 66 đợt D1 · 34 đợt W1 |
| A5 | Nến tuần/ngày đóng qua mốc lớn, chạm đích lớn | Đổi view lớn | xem A5 |
| B1 | Buổi mới, plan hôm qua chưa bị tác động | GIỮ view | GIỮ 128/179 = 72% |
| B2 | Râu quét qua mốc, nến chưa đóng | GIỮ, gọi là quét/fake/trap | [đo] GIỮ 61% |
| B3 | Nến H4/D1 ĐÓNG qua mốc sai | LẬT; 2 cây H4 thì chắc hơn | [đo] LẬT 10/22 = 45% |
| B4 | Giá chạy xa ngược view, H4 nằm sai phía MA | LẬT | [đo] LẬT 21/40 = 52% |
| B5 | Một cây nến lớn / nhấn chìm ngược view | LẬT hoặc bỏ lệnh | [đo] LẬT 10/24 = 42% |
| B6 | Nến D1 hôm qua đóng ngược màu view | Không đánh ngược màu nến ngày | [đo] LẬT 25/82 = 30% |
| B7 | Trendline bị nến đóng phá | Đi theo hướng phá | [đo] LẬT 12/28 = 43% |
| B8 | Giá chạm đích ("xong việc") | Hành động với lệnh; view thường GIỮ | [đo] GIỮ 71% |
| B9 | Giá kẹt giữa 2 mốc, sát tin | PHÂN VÂN, ngồi chờ nến phá | 8 buổi PHÂN VÂN / 180 buổi có nhãn (học 1, kiểm 7) |
| B10 | Nến H4 11:00 đóng ngay trên live | Đổi ý giữa buổi | 8/180 = 4% buổi |
| C1 | Tin lớn sắp ra (≤ 24h) | Né giờ tin, không giữ lệnh qua tin; view không đổi | dặn né/thận trọng 52/161 lời |
| C2 | Giá chạy trước tin | Đoán sau tin chạy ngược | 16 buổi |
| C3 | Tin đã ra | Tin là "cái cớ", GIỮ view | [đo] GIỮ 81% |
| C4 | Trước/sau FOMC, khi CPI/PPI/PCE ra | Đọc Fed theo KỲ TỚI + xác suất | 55 buổi |
| C5 | Đêm FOMC | Kết quả → hành động định sẵn | [đo] LẬT trong cửa sổ FOMC 2/28 = 7% |
| C6 | Tin chiến sự, Trump, hack, chủ tịch Fed | Xem giá phản ứng, không theo tin | 52 + 18 + 7 lời |
| D1 | Lệnh short từ đỉnh 124–126k | Giữ cả năm, chốt dần | 14 mục / 14 buổi |
| D2 | Giá chạm đích/cản đã định | Chốt ngay | 145 mục / 104 buổi |
| D3 | Lệnh lãi, nhiều đích | Chốt từng phần theo nấc | 123 mục chốt một phần |
| D4 | Lý do vào lệnh mất | Đóng | 158 mục / 106 buổi |
| D5 | Tin, đêm Chủ nhật, thứ Hai | Đóng lệnh ngắn; cuối tuần giữ chung nhịp | 41 mục / 38 buổi |
| D6 | Spot | Giữ phần dài hạn, chốt lướt theo F&G/cản, DCA đều | 102 mục / 84 buổi |
| D7 | Muốn gồng | Chỉ gồng khi SL đã về entry | 27 mục |
| D8 | Bot lưới short | Giữ tới vùng đích, đủ thì chốt | 13 mục / 12 buổi |

---

# A. KHUNG LỚN & CHU KỲ

## A1. Pha chu kỳ: 2026 là năm downtrend (đầu năm → nay)

- **Tình huống**: bất kỳ buổi nào, nhất là khi người xem hỏi "dài hạn", "bao giờ đáy", "có nên HODL".
- **Người đó nhìn/kiểm**: lịch halving (đáy trước halving khoảng 1 năm, đỉnh sau halving khoảng 1 năm); đỉnh mùa này 126k; % giảm từ đỉnh; Fibo khung tuần.
- **Kết luận + hành động**: view dài hạn GIẢM suốt năm; nhịp tăng nào cũng là "hồi"; spot chỉ gom ở vùng sâu. Giá đáy và thời điểm đáy được dời dần theo thời gian (bảng dưới).
- **Tần suất**: view dài hạn (nhãn `view_trung_han` khung M1) nêu ở 119 buổi: GIAM 105, TANG 11, PHAN_VAN 3 → GIẢM 105/119 = 88%. Buổi có nói chu kỳ / downtrend / mùa: 106/180 = 59%. Các buổi nêu TĂNG/PV ở khung dài (nhãn, kèm hạn họ nói): 03-31 TĂNG (tháng 4 (cảm nhận cá nhân, tăng rồi gãy tiếp)); 04-01 TĂNG (tháng 4 (có thể cuối tháng sập)); 04-07 TĂNG (trong tháng 4 (nến tháng 4 có thể xanh)); 04-17 TĂNG (tháng 4); 04-20 TĂNG (tháng 4); 05-27 PV (tháng 6); 06-08 PV (sideway tới khoảng tháng 10; cuối năm/đầu năm sau mới nhấn s); 08-13 TĂNG (nhiều năm tháng (không nêu cụ thể)); 08-17 TĂNG (từ đây đến cuối năm, sang năm); 08-21 TĂNG (tháng 9 (từ giờ đến hết 26 lòng vòng rồi lên)); 09-08 PV (đến cuối năm: nhịp tăng này có lẽ là nhịp tăng gần cuối cùng); 09-21 TĂNG (dài hạn 5 năm tới; gom trong ~2 năm); 10-01 TĂNG (không nói hạn); 10-13 TĂNG (Theo chu kỳ halving (chỉ là 'nếu'): đáy khoảng T11-12/2026, ); 10-27 TĂNG (Khoảng giữa năm sau hoặc trong năm 2027: thị trường quay đầu); 10-28 TĂNG (Dài hạn / mùa tới (BTC khoảng x3 là hết sức)).
- **Pha theo thời gian (lời họ)**:

| Tháng | Họ nói pha nào | Trích |
|---|---|---|
| T1 | Downtrend bắt đầu; gom 40k → 20k | [01-07 · 00:09:11](https://www.youtube.com/watch?v=NOBgwE4Gdko&t=551s) "Chờ vào down trend mua Bitcoin, ETH. Mình sẽ chờ Bitcoin từ 40 cho đến khoảng 20. Đó là vùng giá dự kiến của mình." |
| T1 | 2026 là năm của chu kỳ giảm | [01-21 · 00:20:29](https://www.youtube.com/watch?v=LRkYCtbojb0&t=1229s) "bởi vì bây giờ chúng ta đã bắt đầu qua năm 2026 rồi. 2026 đi một chu kỳ giảm. Sau này đến thời điểm này của sang năm tức là khoảng 11 tháng nữa nếu anh em mình còn livestream với nhau thì anh em có thể view lại" |
| T2 | Mới qua 1 tháng, còn 10 tháng rưỡi | [02-16 · 00:34:42](https://www.youtube.com/watch?v=0zDtKlmcydA&t=2082s) "Chúng ta sẽ tiếp tục chiến đấu trong năm Down Trend 2026. Từ giờ mới qua được 1 tháng, vẫn còn 10 tháng rưỡi down trend nữa. Cứ tự tin, tích cực gom, chờ giá tốt rồi mua." |
| T3 | Cuối downtrend: Q1–Q2/2027 | [03-18 · 01:01:07](https://www.youtube.com/watch?v=oyJGNnpopXw&t=3667s) "Cuối downtrend thì mình nghĩ là chắc loanh quanh khoảng, nếu mà sớm thì quý 1 năm 2027, tức là thời điểm này sang năm. Còn nếu mà trễ thì khoảng quý 2 năm 2027." |
| T3 | Đồng pha chu kỳ 4 năm | [03-30 · 00:07:06](https://www.youtube.com/watch?v=KbxhGxmcYwg&t=426s) "22 và 26 cách nhau 4 năm. Nếu anh em hay hỏi chu kỳ 4 năm thì hiện tại có vẻ khá đồng pha. Bên này cũng là vai đầu vai, có khả năng ba đỉnh, bên này cũng vậy." |
| T4 | Tháng 4 tăng (tự nhận cảm nhận), tháng 5 bán | [03-31 · 00:39:55](https://www.youtube.com/watch?v=bz8_iuwosGs&t=2395s) "theo cảm nhận cá nhân của mình là nhịp tháng tư này nó sẽ tăng... sóng chính của tháng tư mình nghĩ là sóng tăng... bởi vì nó tăng để sau đó nó gãy tiếp... Cho nên mình không dám short liều ở những vùng giá này." · [04-21 · 00:36:03](https://www.youtube.com/watch?v=AG126RfNCk4&t=2163s) "…Theo lịch sử, cứ hai tháng xanh là sẽ có một tháng 5 đỏ." |
| T5 | Đỉnh theo chu kỳ 4 năm; đã đi ~1/2 downtrend | [05-05 · 00:55:26](https://www.youtube.com/watch?v=Au_SuIIstcY&t=3326s) "Sau đó về đáy 1 năm sau. Đáy thông thường tạo trong vòng 2 năm sau khi lập đỉnh. Đó là theo chu kỳ 4 năm." · [05-28 · 00:53:45](https://www.youtube.com/watch?v=IY2JeSNTTfQ&t=3225s) "Các bạn hiểu là bây giờ chúng ta đang đi được khoảng 1/2 downtrend rồi. Còn không thì cũng đi được khoảng tầm 40% của downtrend rồi" |
| T6 | Đỉnh mùa = 126k; 40k khả thi, 20k là "bonus" | [06-04 · 00:24:04](https://www.youtube.com/watch?v=59zOmIM_EOM&t=1444s) "Còn lại đỉnh của thị trường mùa này thì gần như là đã xác định là 126 rồi, không có cãi gì hết. Giờ này đừng có chối là đỉnh mùa này có thể là 200 cái gì nữa. Mùa này là nó dừng ở 126 rồi. Thông thường giống như những mùa trước thì giá nó sẽ dump đâu đó khoảng 80% hoặc nhẹ thì khoảng 72%.…" · [06-24 · 00:30:03](https://www.youtube.com/watch?v=ZrqOEgiFEF8&t=1803s) "cho nên là mình nghĩ là con số 40.000 là khả thi." |
| T7 | Đáy chu kỳ đến trước halving 2028; chu kỳ là yếu tố số 1 | [07-07 · 00:11:47](https://www.youtube.com/watch?v=uvBnzq6-k-M&t=707s) "Ở đây anh em có thể thấy nếu xét theo halving năm 2024 thì chúng ta sẽ có một cái vùng đáy được tạo ra loanh quanh khoảng tầm tháng 9 của năm 2023." · [07-22 · 00:16:29](https://www.youtube.com/watch?v=3gr71JlVqR8&t=989s) "Đối với quan điểm của mình thì yếu tố quan trọng nhất của crypto đó là chu kỳ. Đó là yếu tố" |
| T8 | 40–45k vào 50% vốn; hết downtrend khi nến tuần đóng qua 93–95k | [08-12 · 00:05:22](https://www.youtube.com/watch?v=EaWaSL7aWT4&t=322s) "Tính toán thế nào thì mình nghĩ đâu đó khoảng 45.000 là chúng ta có thể vào 50% ... Vùng từ 40 đến 45 anh em có thể vào, tổng vốn rơi vào khoảng 50% ... Sau đó đến tầm 30–35 thì chúng ta đã vào được khoảng 80%. (kế hoạch DCA spot)" · [08-26 · 00:18:37](https://www.youtube.com/watch?v=I1DFCTsjQXE&t=1117s) "Khi nào nó đóng qua khỏi vùng 93 đến 95 này thì mình nghĩ xu hướng downtrend của chúng ta mới có khả năng được gọi là kết thúc." |
| T8 | Sau cú pump cuối tháng 8: tuần bị phá cấu trúc là "tín hiệu tốt" nhưng chưa phải uptrend | [08-25 · 00:14:52](https://www.youtube.com/watch?v=nSxBbLai2mE&t=892s) "Mình đánh giá nhịp này vẫn chưa khẳng định là nhịp tăng, mặc dù cấu trúc khung tuần đã bị phá đi, đó cũng là một tín hiệu tốt." · [08-21 · 00:42:27](https://www.youtube.com/watch?v=oDD5qwLcZbw&t=2547s) "Từ đây đến hết 26 [?] mình nghĩ chắc lòng vòng rồi lại lên, hoặc lên luôn cũng không biết chừng. Nói chung xu hướng tháng 9 vẫn là lên thôi." |
| T9 | Năm nay chưa hết downtrend, vẫn DCA | [09-08 · 01:05:58](https://www.youtube.com/watch?v=gOwbzU0t2S0&t=3958s) "Nếu lên đó chắc mình vẫn mua, vì quan điểm của mình là năm nay chưa hết downtrend, nên trong downtrend mình vẫn DCA hàng ngày bình thường." |
| T10 | Halving 4/2028 → cuối năm nay có đáy; đóng trên 100k mới hết downtrend | [10-13 · 00:55:34](https://www.youtube.com/watch?v=4ttwL_4CC9E&t=3334s) "Tháng 4 năm 2028 là halving, nên cũng khớp: khoảng cuối năm nay sẽ có đáy. Chu kỳ trước đáy xuất hiện khoảng tháng 11 hoặc 12 năm 2022, đến tháng 3-4 năm 2024 halving là khoảng 1 năm 3-4 tháng." · [10-19 · 00:49:30](https://www.youtube.com/watch?v=-avZ2E3n2oE&t=2970s) "Còn nếu nó đóng lại trên 100.000 thì hết downtrend. Đóng trên 100.000 thì hết đó." |
| T10 | Downtrend tới giữa/hết 2027, DCA tới giữa 2027; mùa sau mới tăng | [10-29 · 00:29:15](https://www.youtube.com/watch?v=wcDxLBw0TO4&t=1755s) "vô tình đồng bộ với plan của mình: downtrend sẽ kéo dài, xấu nhất đến hết 2027, còn không thì đến khoảng tháng 6 năm 2027, tức quý 2 năm 2027. Như các lần trước mình nói, mình DCA theo plan đến khoảng giữa năm 2027, chứ không phải hiện tại là hết downtrend rồi." · [10-28 · 00:35:40](https://www.youtube.com/watch?v=Gu1XtyNNH6I&t=2140s) "Dài hạn vẫn tăng nhưng cần những nhịp điều chỉnh rồi tăng thì đẹp. ... Mùa tới mình nghĩ Bitcoin khoảng x3 là hết sức, target x3 là happy." |

## A2. Thứ Hai: đọc lại nến tuần, đặt view cho cả tuần

- **Tình huống**: buổi đầu tuần, nến tuần vừa đóng (7:00 sáng thứ Hai giờ VN), hoặc cuối tuần thị trường đứng.
- **Người đó nhìn/kiểm**: nến tuần đóng ở đâu, râu đã test chưa, vị trí so với MA34/89/200 tuần và Fibo tuần; cuối tuần đứng thì "reset" view.
- **Kết luận + hành động**: view tuần dùng cho cả tuần; giữa tuần chỉ thu ngắn lại, không đổi view đầu tuần.
- **Tần suất**: buổi thứ Hai có nhắc khung/nến tuần 36/36 = 100% (ngày khác 97/144 = 67%); buổi đầu mỗi tuần 42/43 = 98%. Hướng H4 thứ Hai so với view trước (nhãn): GIỮ 29/36 = 81%. [đo] GIU_LAT: thứ Hai GIỮ 81%, LẬT 7/36 = 19% (nền 24%). Lần đổi hướng view W1 rơi vào buổi đầu tuần: 19/33 = 58%.
- **Ví dụ**:
  - [01-12 · 00:30:16](https://www.youtube.com/watch?v=xwJagQCx1gY&t=1816s) "Đối với cây nến tuần đóng như thế này thì mình vẫn giữ view là có khả năng lên được vùng 96 cho đến 100."
  - [08-10 · 00:16:32](https://www.youtube.com/watch?v=8BGhoFetSaU&t=992s) "Hai ngày cuối tuần vừa rồi thị trường nó đứng thành ra chúng ta reset hết tất cả những view rồi."
  - [09-21 · 00:33:58](https://www.youtube.com/watch?v=I_U52BYUt0M&t=2038s) "Đi vào trong tuần chúng ta view ngắn hơn nhưng không thay đổi so với view đầu tuần. Khi nào view trong tuần tác động lên view lớn thì mình sẽ thông báo để anh em điều chỉnh dự phòng kế hoạch dài hạn."

## A3. Đầu tháng: đọc nến tháng

- **Tình huống**: buổi đầu tháng (nến tháng vừa đóng).
- **Người đó nhìn/kiểm**: nến tháng xanh/đỏ, là "nến mua" hay "nến bán" (râu, giá mở/đóng), so với nến tháng trước.
- **Kết luận + hành động**: nến tháng xác nhận hoặc tăng độ tin cho view trung hạn ("giúp tăng tỉ lệ chính xác của view").
- **Tần suất**: buổi đầu tháng có nói nến/khung tháng 7/10 = 70%; tổng số buổi nhắc nến tháng 18. [đo] Buổi đầu tháng: GIỮ 78% (n = 9, ít mẫu).
- **Ví dụ**:
  - [04-01 · 00:24:30](https://www.youtube.com/watch?v=Be-e74Mwx0U&t=1470s) "Cây màu xanh nhưng không phải là cây nến mua mà là cây nến bán. Giá mở cửa ở 66.000, giá đóng cửa nến tháng ở 68.000... Trong cả quá trình giá đã nỗ lực lên đến 75.000 nhưng cuối cùng vẫn bị đạp xuống, tức là nỗ lực không thành công."
  - [06-01 · 00:17:52](https://www.youtube.com/watch?v=cgTktZyPPt4&t=1072s) "Tháng năm này là một cây sell rất rõ ràng, không cần phân tích nhiều và không bất ngờ. Cây nến này giúp tăng tỉ lệ chính xác của view là tiếp tục điều chỉnh đi xuống."
  - [10-01 · 00:12:19](https://www.youtube.com/watch?v=56fLd04MSps&t=739s) "Hôm nay là ngày 01 tháng 10, ngày đầu tiên của tháng 10, nên chúng ta view lại nến tháng. Khung tuần thì mình nói từ đầu tuần rồi, hôm nay mới giữa tuần, nến chưa đóng nên không có thay đổi gì."

## A4. View trung hạn D1/W1 bền bao lâu

- **Tình huống**: đã nêu view khung ngày (D1) hoặc khung tuần (W1).
- **Người đó nhìn/kiểm**: cấu trúc khung lớn có đổi chưa; view có hạn dùng ("đến thứ ba tuần sau").
- **Kết luận + hành động**: view H4 thay theo từng cây nến; view tuần giữ đến khi cấu trúc khung lớn đổi.
- **Tần suất** (nhãn, đợt = các buổi liền nhau cùng hướng, chỉ tính buổi có nói khung đó):
  - D1: 166 buổi, 66 đợt; một đợt kéo dài trung vị **3 ngày** (2 buổi), dài nhất 28 ngày. Hướng: GIAM 73, TANG 71, PHAN_VAN 22.
  - W1: 122 buổi, 34 đợt; trung vị **6 ngày**, dài nhất 55 ngày. Hướng: GIAM 94, TANG 19, PHAN_VAN 9.
  - Dài hạn (M1): 119 buổi, 21 đợt; trung vị 5 ngày, dài nhất 84 ngày.
  - [đo] GIU_LAT §7 (đích cùng hướng view, tính bằng râu H4, ≤ 60 ngày, trước khi họ bỏ view): D1 chạm 36/105 = 34%, thời gian tới đích trung vị 2.5 ngày; W1 chạm 14/68 = 21%, thời gian tới đích trung vị 15.4 ngày.
- **Ví dụ**:
  - [07-24 · 00:58:50](https://www.youtube.com/watch?v=7D1Ve5hs4bU&t=3530s) "Sau mỗi cây nến là thị trường lại thay đổi. Cứ sau mỗi cây nến đóng"
  - [06-12 · 00:30:24](https://www.youtube.com/watch?v=x75V4Kb1fj4&t=1824s) "Và view này thì anh em có thể lưu lại và mọi người có thể sử dụng nó cho đến khoảng thứ ba tuần sau."
  - [10-28 · 00:33:41](https://www.youtube.com/watch?v=Gu1XtyNNH6I&t=2021s) "Hỏi: Còn view Bitcoin về 4x, 5x nữa không? Vùng này mình vẫn giữ vì không có thay đổi gì nhiều trên khung lớn. Khi nào cấu trúc khung lớn thay đổi thì view mới cần cập nhật, hoặc khi qua một khoảng thời gian rất lâu thì cập nhật theo timing."

<details><summary>Bảng các đợt view W1 (nhãn)</summary>

| # | Hướng | Từ → đến | Buổi | Ngày tới lần đổi |
|---|---|---|---|---|
| 1 | GIAM | 01-06 → 02-06 | 15 | 41 |
| 2 | TANG | 02-16 → 02-16 | 1 | 10 |
| 3 | GIAM | 02-26 → 02-26 | 1 | 4 |
| 4 | TANG | 03-02 → 03-02 | 1 | 4 |
| 5 | GIAM | 03-06 → 03-13 | 5 | 10 |
| 6 | TANG | 03-16 → 03-17 | 3 | 3 |
| 7 | GIAM | 03-19 → 04-02 | 8 | 15 |
| 8 | PHAN_VAN | 04-03 → 04-03 | 1 | 3 |
| 9 | TANG | 04-06 → 04-06 | 1 | 1 |
| 10 | GIAM | 04-07 → 04-09 | 3 | 3 |
| 11 | PHAN_VAN | 04-10 → 04-10 | 1 | 3 |
| 12 | TANG | 04-13 → 04-13 | 1 | 1 |
| 13 | GIAM | 04-14 → 04-17 | 3 | 6 |
| 14 | TANG | 04-20 → 04-20 | 1 | 1 |
| 15 | GIAM | 04-21 → 06-12 | 19 | 55 |
| 16 | TANG | 06-15 → 06-15 | 1 | 7 |
| 17 | GIAM | 06-22 → 07-03 | 7 | 14 |
| 18 | PHAN_VAN | 07-06 → 07-09 | 2 | 7 |
| 19 | GIAM | 07-13 → 07-27 | 7 | 18 |
| 20 | PHAN_VAN | 07-31 → 07-31 | 1 | 3 |
| 21 | GIAM | 08-03 → 08-06 | 3 | 7 |
| 22 | TANG | 08-10 → 08-10 | 1 | 7 |
| 23 | GIAM | 08-17 → 08-26 | 6 | 10 |
| 24 | TANG | 08-27 → 08-27 | 1 | 1 |
| 25 | GIAM | 08-28 → 09-04 | 3 | 10 |
| 26 | PHAN_VAN | 09-07 → 09-07 | 1 | 7 |
| 27 | GIAM | 09-14 → 09-18 | 6 | 7 |
| 28 | TANG | 09-21 → 09-21 | 1 | 1 |
| 29 | PHAN_VAN | 09-22 → 09-23 | 2 | 2 |
| 30 | GIAM | 09-24 → 09-25 | 2 | 4 |
| 31 | TANG | 09-28 → 10-13 | 6 | 17 |
| 32 | PHAN_VAN | 10-15 → 10-15 | 1 | 4 |
| 33 | TANG | 10-19 → 10-19 | 1 | 1 |
| 34 | GIAM | 10-20 → 10-30 | 6 | còn chạy |

</details>

<details><summary>Bảng các đợt view D1 (nhãn)</summary>

| # | Hướng | Từ → đến | Buổi | Ngày tới lần đổi |
|---|---|---|---|---|
| 1 | TANG | 01-06 → 01-16 | 9 | 13 |
| 2 | GIAM | 01-19 → 02-05 | 13 | 18 |
| 3 | TANG | 02-06 → 03-05 | 6 | 28 |
| 4 | GIAM | 03-06 → 03-06 | 1 | 3 |
| 5 | TANG | 03-09 → 03-10 | 2 | 2 |
| 6 | GIAM | 03-11 → 03-11 | 1 | 1 |
| 7 | TANG | 03-12 → 03-19 | 7 | 8 |
| 8 | GIAM | 03-20 → 03-23 | 3 | 4 |
| 9 | TANG | 03-24 → 03-26 | 3 | 3 |
| 10 | GIAM | 03-27 → 03-30 | 2 | 4 |
| 11 | TANG | 03-31 → 04-03 | 4 | 6 |
| 12 | GIAM | 04-06 → 04-07 | 2 | 2 |
| 13 | TANG | 04-08 → 04-10 | 3 | 5 |
| 14 | GIAM | 04-13 → 04-13 | 1 | 1 |
| 15 | TANG | 04-14 → 04-28 | 8 | 15 |
| 16 | GIAM | 04-29 → 04-29 | 1 | 5 |
| 17 | TANG | 05-04 → 05-06 | 3 | 3 |
| 18 | GIAM | 05-07 → 05-07 | 1 | 1 |
| 19 | TANG | 05-08 → 05-12 | 2 | 11 |
| 20 | GIAM | 05-19 → 06-04 | 7 | 16 |
| 21 | TANG | 06-04 → 06-04 | 1 | 1 |
| 22 | PHAN_VAN | 06-05 → 06-05 | 1 | 3 |
| 23 | TANG | 06-08 → 06-09 | 2 | 2 |
| 24 | GIAM | 06-10 → 06-10 | 1 | 1 |
| 25 | TANG | 06-11 → 06-23 | 5 | 13 |
| 26 | GIAM | 06-24 → 06-29 | 4 | 6 |
| 27 | PHAN_VAN | 06-30 → 06-30 | 1 | 1 |
| 28 | GIAM | 07-01 → 07-02 | 2 | 2 |
| 29 | TANG | 07-03 → 07-03 | 1 | 3 |
| 30 | GIAM | 07-06 → 07-14 | 6 | 9 |
| 31 | TANG | 07-15 → 07-22 | 4 | 8 |
| 32 | PHAN_VAN | 07-23 → 07-23 | 1 | 1 |
| 33 | TANG | 07-24 → 07-27 | 2 | 4 |
| 34 | GIAM | 07-28 → 07-28 | 1 | 1 |
| 35 | PHAN_VAN | 07-29 → 07-30 | 3 | 2 |
| 36 | TANG | 07-31 → 07-31 | 1 | 3 |
| 37 | GIAM | 08-03 → 08-03 | 1 | 1 |
| 38 | PHAN_VAN | 08-04 → 08-05 | 2 | 2 |
| 39 | TANG | 08-06 → 08-06 | 1 | 1 |
| 40 | GIAM | 08-07 → 08-07 | 1 | 3 |
| 41 | PHAN_VAN | 08-10 → 08-11 | 2 | 2 |
| 42 | GIAM | 08-12 → 08-14 | 3 | 5 |
| 43 | PHAN_VAN | 08-17 → 08-18 | 2 | 3 |
| 44 | TANG | 08-20 → 08-21 | 2 | 5 |
| 45 | GIAM | 08-25 → 08-25 | 1 | 1 |
| 46 | PHAN_VAN | 08-26 → 08-26 | 1 | 1 |
| 47 | TANG | 08-27 → 08-27 | 1 | 1 |
| 48 | PHAN_VAN | 08-28 → 08-28 | 1 | 6 |
| 49 | GIAM | 09-03 → 09-03 | 1 | 1 |
| 50 | PHAN_VAN | 09-04 → 09-07 | 2 | 4 |
| 51 | GIAM | 09-08 → 09-08 | 1 | 7 |
| 52 | PHAN_VAN | 09-15 → 09-15 | 1 | 1 |
| 53 | GIAM | 09-16 → 09-17 | 3 | 2 |
| 54 | PHAN_VAN | 09-18 → 09-18 | 1 | 3 |
| 55 | GIAM | 09-21 → 09-21 | 1 | 1 |
| 56 | TANG | 09-22 → 09-23 | 2 | 2 |
| 57 | GIAM | 09-24 → 10-02 | 4 | 11 |
| 58 | PHAN_VAN | 10-05 → 10-06 | 2 | 2 |
| 59 | GIAM | 10-07 → 10-13 | 2 | 7 |
| 60 | PHAN_VAN | 10-14 → 10-14 | 1 | 1 |

</details>

## A5. Khi nào đổi view lớn (D1/W1/chu kỳ)

- **Tình huống**: nến tuần/ngày đóng qua mốc lớn; giá chạm đích lớn đã nêu từ lâu; nến tuần "khổng lồ".
- **Người đó nhìn/kiểm**: nến ĐÓNG (tuần/ngày) qua vùng cản/hỗ trợ lớn; đích lớn đã đủ chưa; tâm lý đám đông (F&G).
- **Kết luận + hành động**: đổi view khung lớn, nói rõ "đừng cản tàu" hoặc "đừng short nữa"; mốc hết downtrend họ nêu bằng một mức giá đóng nến (93–95k rồi 100k).
- **Tần suất**: view D1 đổi hướng 65 lần, W1 33 lần (nhãn). Buổi họ tự nói "đổi" có lý do khung lớn (nến tuần/ngày): 27/39 = 69%; có lý do đầu tuần/tháng: 17/39 = 44%; có lý do chạm đích: 16/39 = 41%.
- **Ví dụ**:
  - [02-06 · 00:14:29](https://www.youtube.com/watch?v=PLl8AM0RxEM&t=869s) "Nói chung tinh thần của mình ngày hôm nay từ giờ đến cuối tuần thì lời khuyên của mình đối với anh em là đừng có short nữa. Mình nghĩ loanh quanh nhịp hồi nó nằm đâu đây rồi. Bởi vì đây cũng full TP rồi. Những ngày trước thì nó còn TP chứ bây giờ là nó full TP, mô hình cờ chắc chắn nó sẽ không có vút lên một phát liền." (chạm đích cờ 62k, F&G 9)
  - [05-07 · 00:22:59](https://www.youtube.com/watch?v=FlYmDPPMwhY&t=1379s) "Với cộng đồng thì coi như chúng ta đã hoàn tất target lớn của 6 tháng đầu năm. Từ giờ đến tháng sáu mình nghĩ không còn gì để ra vào nhiều. Từ giờ chỉ chờ nó sập sâu đâu đó cuối năm rồi vào những vị thế khác."
  - [09-21 · 00:18:09](https://www.youtube.com/watch?v=I_U52BYUt0M&t=1089s) "Nói chung hiện tại trên khung tuần Bitcoin đang thể hiện một gương mặt cực kỳ tươi. Cho nên cứ cố đi cản tàu là điều không nên."
  - Mốc đổi view chu kỳ: [08-26 · 00:18:31](https://www.youtube.com/watch?v=I1DFCTsjQXE&t=1111s) "Khi nào nó đóng qua khỏi vùng 93 đến 95 này thì mình nghĩ xu hướng downtrend của chúng ta mới có khả năng được gọi là kết thúc." → sau đó [10-19 · 00:49:30](https://www.youtube.com/watch?v=-avZ2E3n2oE&t=2970s) "Còn nếu nó đóng lại trên 100.000 thì hết downtrend. Đóng trên 100.000 thì hết đó."

---

# B. GIỮ / LẬT VIEW H4

[đo] Tóm tắt GIU_LAT:
- Giữ view (so với hướng gần nhất): **128/179 = 72%** buổi (học 76%, kiểm 65%); LẬT 24%, sang PV 4%.
- LẬT mạnh nhất khi: Giá đi ngược view ≥ 2% từ C buổi trước (61% vs 19%); Lúc C giá vẫn ở bên kia mốc sai (59% vs 20%); Giá H4 ngoài dải EMA34 phía SAI view (52% vs 16%).
- Hay BỎ QUA (LẬT không cao hơn nền): Giá D1 sai phía EMA200 (giữ 75%, n 106); Giá D1 sai phía EMA89 (giữ 76%, n 104); Râu chạm đích CHẶNG KẾ TIẾP buổi trước (giữ 73%, n 90).
- Mốc sai của chính họ bị phá mà vẫn GIỮ đa số: Râu chạm/qua mốc sai buổi trước (chưa cần đóng) (giữ 61%, n 33); ≥ 1 nến H4 ĐÓNG qua mốc sai buổi trước (giữ 58%, n 24); Đóng qua mốc sai ĐÚNG khung + số nến họ nói (giữ 55%, n 22).
- Bộ luật khoá (chọn trên học, K = 0): (không luật — giữ view).
- Ngoài mẫu (kiểm T7–T10, 77 buổi): bộ luật 50/77 = 65% · giữ view 65% · luôn GIẢM 64% · từ trên xuống 61%.

## B1. Mặc định: GIỮ view của buổi trước

- **Tình huống**: buổi mới; chưa có nến đóng qua mốc sai; giá đi trong kịch bản.
- **Người đó nhìn/kiểm**: plan hôm qua đã bị tác động chưa; khung lớn có gì thay đổi không.
- **Kết luận + hành động**: nhắc lại plan và vùng giá cũ; "không có thay đổi gì nhiều".
- **Tần suất**: nhãn (hướng cuối buổi so với view): GIỮ 128/179 = 72%, LẬT 43/179 = 24%, PV 8/179 = 4%. Tự nói: "giữ" 141/180 = 78%, "đổi" 39/180 = 22%. Lý do họ nêu khi GIỮ: khung lớn 100/141 = 71%, nến đóng/chưa gãy 94/141 = 67%, râu/quét/fake 65/141 = 46%, đúng kịch bản 43/141 = 30%. [đo] Giữ view (so với hướng gần nhất): **128/179 = 72%** buổi (học 76%, kiểm 65%); LẬT 24%, sang PV 4%
- **Ví dụ**:
  - [01-06 · 00:03:58](https://www.youtube.com/watch?v=aQbHs7J80jc&t=238s) "Các vùng giá thì như hôm qua chúng ta vẫn giữ nguyên cái plan của ngày hôm qua. Không có thay đổi gì nhiều lắm."
  - [04-09 · 00:26:24](https://www.youtube.com/watch?v=gx-69-TVn_w&t=1584s) "Xu hướng của thị trường hiện tại thì vẫn đang trong xu hướng phục hồi, phục hồi là tăng. Và các mô hình khung lớn vẫn không có gì thay đổi."
  - [09-17 · 00:08:15](https://www.youtube.com/watch?v=1cUPKUmEnr4&t=495s) "Cái view từ đêm hôm qua đến giờ không thay đổi nhiều cho nên hôm nay mình đi nhanh."

## B2. Râu quét qua mốc, nến chưa đóng → GIỮ (gọi là quét / fake out / trap)

- **Tình huống**: râu nến chạm hoặc vượt mốc sai, hoặc có nhịp ngược ngắn, nhưng thân nến chưa đóng qua.
- **Người đó nhìn/kiểm**: giá ĐÓNG ở đâu (không tính râu); có rút chân không; nhịp đó có phải để quét thanh khoản/SL của phe FOMO.
- **Kết luận + hành động**: giữ view, gọi nhịp ngược là "quét", "fake out", "trap", "chỉ là hồi"; không đổi lệnh.
- **Tần suất**: [đo] râu chạm/qua mốc sai buổi trước: 33 buổi → GIỮ 61%, LẬT 13/33 = 39% (khi không có râu qua mốc: LẬT 20%) → râu qua mốc làm họ lật nhiều hơn, nhưng đa số lần vẫn GIỮ. Nhãn: buổi có lời gạt nhịp ngược là quét/fake/trap/hồi 143/180 = 79%; buổi tự nói GIỮ vì râu/quét/fake 65/141 = 46%.
- **Ví dụ**:
  - [01-28 · 00:13:26](https://www.youtube.com/watch?v=2_a0RdwC1t8&t=806s) "…Ngày hôm qua có một pha fake out. Hôm qua chúng ta cũng nói lý do vì sao anh em không nên short trong ngày hôm qua, bởi vì nến ngày trước đó là cây nến xanh, và đặc biệt nó đi một cặp có khả năng đảo chiều như thế này thì khả năng fake out cũng có.…"
  - [05-06 · 00:22:22](https://www.youtube.com/watch?v=Ts0NVXvVnBw&t=1342s) "Các bạn thấy râu nến nó vẫn quét lên trên này. Lực mua thì vẫn xanh. Chưa có bất kỳ một nến đỏ nào thì tạm thời chúng ta chưa cần phải quan tâm cái gì. Lực mua vẫn còn chứng tỏ là xu hướng hiện tại vẫn đang xu hướng phục hồi."
  - [10-23 · 00:18:59](https://www.youtube.com/watch?v=cb85mXIfTv8&t=1139s) "Tuy nhiên với nhịp hồi lên 84 hôm trước, chúng ta thừa biết xác suất cực kỳ cao đây là một nhịp phá cao đi lên (fake). Vì khi nó lên trên này thì rất đẹp và rất nhiều người đánh tiếp xu hướng đi lên. Bây giờ nó trap lại thì những người bị mắc kẹt ở trên này gần như vào thế rồi.…"

## B3. Nến H4/D1 ĐÓNG qua mốc sai → LẬT (2 cây H4 thì chắc hơn)

- **Tình huống**: nến đóng qua mốc họ đã báo trước, đúng khung và số nến họ nói.
- **Người đó nhìn/kiểm**: giá đóng của nến H4 (D1 cho view ngày); 1 cây hay 2 cây liền nhau.
- **Kết luận + hành động**: kích hoạt nhánh đã nói trước ("đóng dưới X thì short, trên Y thì long"); bỏ lệnh cũ.
- **Tần suất**: [đo] ≥ 1 nến H4 đóng qua mốc sai: 24 buổi → LẬT 10/24 = 42%; đóng đúng khung + số nến họ nói: LẬT 10/22 = 45%; nến D1 đóng qua: LẬT 8/19 = 42%; lúc lên live giá vẫn ở bên kia mốc: LẬT 10/17 = 59% (khi không có nến đóng qua: LẬT 21%). Kể cả khi nến H4 đã đóng qua mốc, họ vẫn GIỮ hướng 58% số buổi. Nhãn: buổi có câu "nếu/khi nến đóng … thì …" 147/180 = 82%; buổi nói "hai cây H4 / cặp H4" 18.
- **Ví dụ**:
  - [01-29 · 00:11:04](https://www.youtube.com/watch?v=8NrjverKQpo&t=664s) "Thủng khỏi vùng 8700, đóng H4 dưới 87.000 thì chúng ta đánh theo nhịp short." → hôm sau [01-30 · 00:04:34](https://www.youtube.com/watch?v=4PUqxjVBR4M&t=274s) "Thủng 87k5 short, đúng rồi. Hôm qua mình bảo có hai vùng 87.000 và 88.000. Muốn short thì nó gãy vùng này là short, còn muốn long thì nó phải vượt qua được đoạn này mới long. Đến khi nó gãy một cái là nó đi luôn."
  - [03-27 · 00:18:51](https://www.youtube.com/watch?v=1RmIBcPxX2I&t=1131s) "Cây nến D1 này đóng ở đây thì rất xấu. Đơn giản ngắn gọn. D1 ở đây rất xấu. Nó bị từ chối ngay cái vùng 72.000, là ở Fibo."
  - [10-14 · 00:28:02](https://www.youtube.com/watch?v=BlA26qxNBTE&t=1682s) "H4 thì tốt nhất đóng trên 84. Một cây H4 không đủ nhá, một cây H4 đôi khi dính fake, hai cây H4 thì confirm hơn, chắc hơn."

## B4. Giá chạy xa ngược view / H4 nằm sai phía MA → LẬT

- **Tình huống**: giá đi ngược view mạnh từ buổi trước; H4 nằm ngoài dải EMA34 phía ngược view hoặc sai phía EMA89.
- **Người đó nhìn/kiểm**: vị trí giá so với MA34/89 trên H4 (luật chọn phe của họ).
- **Kết luận + hành động**: giá trên MA34 và MA89 thì không short; dưới thì không long.
- **Tần suất**: [đo] H4 ngoài dải EMA34 phía sai view: 40 buổi → LẬT 21/40 = 52% (không có: 16%); H4 sai phía EMA89: LẬT 22/59 = 37%; giá đi ngược view ≥ 2%: LẬT 14/23 = 61%. Ngược lại, giá D1 sai phía EMA89/EMA200 thì họ vẫn GIỮ 76% / 75% → quyết định hướng H4 dựa vào MA trên H4, không phải D1.
- **Ví dụ**:
  - [03-12 · 00:25:11](https://www.youtube.com/watch?v=qJZk9q5A7rA&t=1511s) "Cái xu hướng này nó vẫn đang giữ được cái xu hướng tăng. Cho nên mình không short ở vị thế. Nguyên tắc là giá nằm trên MA34 và trên 89 thì chúng ta không có short. Mà giá nằm dưới chúng ta không có long. Thế thôi đối với đánh scalping."
  - [02-11 · 00:02:36](https://www.youtube.com/watch?v=MZ3XfAjYHqk&t=156s) "H4 này thì mọi người thấy H4 vẫn liên tục bị từ chối ở đường MA34, giá không thể nào đấm qua được."
  - [01-08 · 00:22:09](https://www.youtube.com/watch?v=jX-0Hgy1S0E&t=1329s) "nếu muốn long thì đoạn này ít nhất anh em phải chờ có một cây H4 đóng màu xanh lên trên khỏi MA34 tức là trên vùng giá 91.000"

## B5. Một cây nến lớn / nhấn chìm ngược view → LẬT hoặc bỏ lệnh

- **Tình huống**: một cây H4 thân lớn (thường kèm volume) hoặc cây D1 nhấn chìm, ngược hướng view.
- **Người đó nhìn/kiểm**: cây nến đóng ở vị trí nhạy (Fibo, MA); lực của nến; nến đó có xóa nỗ lực mấy ngày trước không.
- **Kết luận + hành động**: "một cây nến làm thay đổi cấu trúc" → bỏ lệnh theo view cũ, đổi hoặc chuyển sang nhập nhằng.
- **Tần suất**: [đo] H4 thân ≥ 1,5 ATR ngược view: 30 buổi → LẬT 13/30 = 43% (không có: 20%); có volume ≥ 1,5 × TB20: LẬT 10/24 = 42%; D1 nhấn chìm ngược view: LẬT 7/20 = 35%. Lý do "nến lớn/lực/volume" khi họ tự nói đổi: 14/39 = 36%.
- **Ví dụ**:
  - [05-27 · 00:16:40](https://www.youtube.com/watch?v=cFwCrK3RjcQ&t=1000s) "…trong vòng 3 ngày nhưng chỉ cần một cây nến xảy ra đâu đó lúc đêm ngày hôm qua cho đến sáng ngày hôm nay, nhấn chìm luôn tất cả những nỗ lực trước đó và gãy luôn, đâm xuyên qua và đi sâu xuống.…"
  - [04-03 · 00:30:58](https://www.youtube.com/watch?v=vnCUK9ayUsI&t=1858s) "hôm qua mình cho các bạn sell short một lệnh nhẹ nhẹ nhưng cây H4 chiều ngày hôm qua nó trap ác quá... Nó đóng một cây H4 rất xanh.…"
  - [10-16 · 00:07:34](https://www.youtube.com/watch?v=lSGpwulXi5s&t=454s) "Xu hướng ở đây, anh em thấy cái cây D1 này cộng với H4 đêm ngày hôm qua, chỉ một cây nến thôi nhưng nó làm thay đổi toàn bộ cấu trúc."

## B6. Nến D1 hôm qua đóng ngược màu view

- **Tình huống**: nến ngày gần nhất đóng màu ngược hướng view (nhất là cây đỏ đầu tiên sau chuỗi tăng).
- **Người đó nhìn/kiểm**: màu nến ngày hôm trước; vị trí đóng (đã chạm đích chưa).
- **Kết luận + hành động**: không đánh ngược màu nến ngày hôm trước. Nếu nến đỏ xuất hiện ngay sau khi đã chạm đích thì coi là điều chỉnh bình thường, view giữ.
- **Tần suất**: [đo] nến D1 gần nhất ngược màu view: 82 buổi → LẬT 25/82 = 30% (không có: 19%).
- **Ví dụ**:
  - [02-04 · 00:06:47](https://www.youtube.com/watch?v=c6WnN4Q9EXo&t=407s) "Đầu tiên khi xét theo góc độ kỹ thuật thì cây nến ngày màu gì thì ngày hôm nay chúng ta không nên đánh ngược cây nến ngày hôm trước. ... À quên, đoạn này short thì hoàn toàn không ổn."
  - [01-16 · 00:05:13](https://www.youtube.com/watch?v=SllvhCOjrkE&t=313s) "Đầu tiên chúng ta có một cây nến ngày màu đỏ đầu tiên sau chuỗi tăng trưởng từ vùng 90 lên đến 97. Như ngày hôm trước mình nói, những vùng này đã đạt vùng target đầu tiên quanh từ 96 đến 98.…" (LẬT)
  - [03-18 · 00:10:55](https://www.youtube.com/watch?v=oyJGNnpopXw&t=655s) "Đầu tiên chúng ta lại có một cây nến D1 màu đỏ. Cây này là cây nến cực kỳ quan trọng và nhắc nhở mọi người rằng chúng ta đã có sự điều chỉnh ở đây. Không có gì bất ngờ khi giá chạm đến vùng Fibo 1.618 của Fibo mở rộng trong đoạn này. Anh em thấy rõ ràng giá chạm đến vùng target là 1.618 là 75.200 và rút râu" (GIỮ: vừa chạm đích 1.618)

## B7. Trendline bị nến đóng phá → đi theo hướng phá

- **Tình huống**: nến H4 đóng vượt trendline / cạnh tam giác / kênh giá.
- **Người đó nhìn/kiểm**: nến đóng (không phải râu) qua trendline; trendline được test nhiều lần chưa; có cây H4 thứ hai không.
- **Kết luận + hành động**: ngừng đánh ngược hướng phá; chưa có nến đóng qua thì coi là chưa phá.
- **Tần suất**: [đo] trendline chính (H4/D1) bị nến H4 đóng phá NGƯỢC view giữa 2 buổi: 28 buổi → LẬT 12/28 = 43% (không có: 21%); bị phá THEO view: GIỮ 84%. Nhãn: trendline nêu ở 139 buổi (254 lần); "vừa phá" 55 lần; hướng họ rút ra từ lần phá trùng hướng H4 cuối buổi 30/47 = 64%.
- **Ví dụ**:
  - [05-04 · 00:26:33](https://www.youtube.com/watch?v=VUUbKp4bFSU&t=1593s) "Bởi vì trước đó nó đã tạo một xu hướng điều chỉnh đỉnh đáy thấp dần. Nhưng về đến vùng này bắt đầu nó kéo lên và nó break qua được cản đầu tiên là trend line với một cây nến H4 khá đẹp, khá lực."
  - [10-20 · 00:05:28](https://www.youtube.com/watch?v=zzhCJ1Bb_vg&t=328s) "Như hôm qua mình nói, đối với nhịp breakout đẹp nhất thì phải có hai cây nến H4 vượt qua thì mới an toàn được... Cụ thể đoạn này nó chạm trendline và chạm Fibo ở vùng 83, hôm qua gãy về 82 và 81 trong phiên nhỏ của ngày hôm qua."
  - [03-24 · 00:21:23](https://www.youtube.com/watch?v=xKTPieljFuY&t=1283s) "khi giảm về 70 lại về đúng vùng 67000, trendline hai ngày vừa rồi, lại có tin Trump với Iran 48 giờ, mọi thứ tự động khớp với nhau... Về phân tích kỹ thuật, giá chạm khẽ trendline ở đằng dưới này, thêm một cái rất đẹp nữa là vùng 67.000 này... Khả năng quét Bitcoin 64.000?…"

## B8. Giá chạm đích ("xong việc") → hành động với lệnh; view thường GIỮ

- **Tình huống**: râu chạm đích chính hoặc đích chặng đã nói.
- **Người đó nhìn/kiểm**: lệnh đang có; nến tại đích (có nến đóng ngược không); tâm lý (F&G).
- **Kết luận + hành động**: "có target thì phải có hành động" → chốt; view chỉ đổi khi có thêm nến đóng ngược ngay tại đích (cây D1 đỏ đầu tiên, H1 gãy).
- **Tần suất**: [đo] râu chạm đích chính: 41 buổi → GIỮ 71%, LẬT 10/41 = 24% (không chạm: 25%); chạm đích chặng kế tiếp: 90 buổi → GIỮ 73%, LẬT 20/90 = 22% (không chạm: 22%) → chạm đích không làm họ lật nhiều hơn. Nhãn: lý do "chạm đích" khi tự nói GIỮ 50/141 = 35%, khi ĐỔI 16/39 = 41%.
- **Ví dụ**:
  - [01-14 · 00:13:13](https://www.youtube.com/watch?v=2ZyVfVN3n4Y&t=793s) "Nhưng vùng này là vùng chúng ta đã đạt target đầu tiên, có target thì phải có hành động. Coi như xong mục tiêu đầu tiên." (GIỮ)
  - [03-20 · 00:23:09](https://www.youtube.com/watch?v=cxvXjQPayvY&t=1389s) "Còn giữ view hồi sáng không? View hồi sáng là không. Thực sự đoạn này phải đánh view ngắn thôi các bạn. Như mình nói lúc sáng thì nó đã lên đến view đó rồi... Long ở vùng lúc sáng lên đến vùng khoảng 71.00 là chúng ta chốt là đúng rồi. Chốt ở đó xong thì bây giờ nó về thì phải để cho nó chạy." (đổi sau khi chạm 71k và H1 gãy)
  - [02-06 · 00:14:29](https://www.youtube.com/watch?v=PLl8AM0RxEM&t=869s) "Nói chung tinh thần của mình ngày hôm nay từ giờ đến cuối tuần thì lời khuyên của mình đối với anh em là đừng có short nữa. Mình nghĩ loanh quanh nhịp hồi nó nằm đâu đây rồi. Bởi vì đây cũng full TP rồi. Những ngày trước thì nó còn TP chứ bây giờ là nó full TP, mô hình cờ chắc chắn nó sẽ không có vút lên một phát liền." (đổi: full TP 62k)

## B9. PHÂN VÂN thật sự

- **Tình huống**: giá kẹt giữa hai mốc công tắc, đi ngang chờ phá; thường sát tin lớn (CPI, FOMC); MA chụm.
- **Người đó nhìn/kiểm**: hai mốc: "đóng dưới X thì short, trên Y thì long, ở giữa ngồi im"; giờ tin.
- **Kết luận + hành động**: không chọn phe, không vào lệnh, chờ nến phá. Đứng ngoài vì giá lưng chừng KHÔNG phải phân vân: hướng vẫn giữ.
- **Tần suất**: [đo] GIU_LAT §5: 8 buổi PHÂN VÂN / 180 buổi có nhãn (học 1, kiểm 7). PV đến từ view GIẢM là chủ yếu (Buổi PV đến từ TĂNG 0, GIẢM 7, PHÂN VÂN 1; buổi sau PV đi về TĂNG 1, GIẢM 6, PHÂN VÂN 1). Ngày thứ Hai: 0/8 = 0% PV (buổi có hướng 36/172 = 21%). Trong cửa sổ FOMC: PV 3/8 = 38% so với buổi có hướng 25/172 = 15%. Giá H4 trong dải EMA34: PV 3/8 = 38% so với 30/172 = 17%; EMA34/89/200 H4 chụm: PV 2/8 = 25% so với 11/172 = 6%. Nhãn `hoc_v5`: cuối buổi PV 8/180 = 4%; đứng ngoài (mọi lý do) 110/180 = 61%.
- **Ví dụ**:
  - [01-29 · 00:11:04](https://www.youtube.com/watch?v=8NrjverKQpo&t=664s) "Thủng khỏi vùng 8700, đóng H4 dưới 87.000 thì chúng ta đánh theo nhịp short. Còn trên 88.00 thì chúng ta đánh theo nhịp long. Còn lại nếu nó cứ giao dịch ở trong vùng 88.00 cho đến 87.00 này thì các bạn ngồi im. Đó là plan ngày hôm nay."
  - [07-29 · 00:22:04](https://www.youtube.com/watch?v=2FMmTeLGCNY&t=1324s) "Cực kỳ khó để mà gọi là chọn một cái phe nào. Thực tế là thị trường hiện tại nó cũng không biết là nó nên đi đâu. Mình đánh giá hiện tại thị trường nó cũng không biết là nó nên lên hay là nên xuống. ... có những cái lúc mình không có nhìn ra được xu hướng mình cũng phải thừa nhận với anh em là mình chịu. Ví dụ như hiện tại."
  - [10-06 · 00:23:13](https://www.youtube.com/watch?v=CABZxVcYavM&t=1393s) "Tổng quát Bitcoin chỉ có thế: sideway, ta quan sát nó phá 85 hay phá lên khỏi 87."
  - [10-14 · 00:43:24](https://www.youtube.com/watch?v=BlA26qxNBTE&t=2604s) "Nếu tối nay ra tin mà thị trường vẫn ở trong vùng này thì tiếp theo vẫn cần ngồi chờ nến xem có phá qua được 84 hay thủng về 83. Nếu tin ra mà không giúp giá breakout khỏi vùng khó chịu hiện tại, không rõ xu hướng, thì chúng ta vẫn tiếp tục phải chờ."

## B10. Đổi ý giữa buổi

- **Tình huống**: cây H4 11:00 (giờ VN) đóng ngay trong lúc live, hoặc giá quét qua SL lệnh đang giữ.
- **Người đó nhìn/kiểm**: giá đóng cây H4 vừa xong so với mốc đã nói đầu buổi.
- **Kết luận + hành động**: đổi hướng ngay trên live, bỏ lệnh cũ.
- **Tần suất**: nhãn 8/180 = 4%; [đo] Đổi giữa buổi (đầu buổi ≠ cuối buổi): 9/179 = 5%.
- **Ví dụ**:
  - [07-02 · 01:02:39](https://www.youtube.com/watch?v=w4bvsDte3bI&t=3759s) "Nếu nó đóng lưng chừng 60.900. Mình cũng nghĩ khả năng nó chơi bài này. Thực tế nó đóng ra 60.000 thì cũng được, cũng giống như 61 thôi. Vùng này nó đã qua H4."
  - [04-02 · 00:42:55](https://www.youtube.com/watch?v=orDQVRuxI1E&t=2575s) "Hỏng rồi. Nát luôn."
  - [10-02 · 00:59:09](https://www.youtube.com/watch?v=AxRfx12h9Z0&t=3549s) "H4 này chắc còn một con nữa mút chỉ. Đi như thế này thì khỏi sale luôn nhá. Altcoin cũng không đánh được mà Bitcoin cũng không đánh nổi. Đoạn này thật chua."

---

# C. TIN TỨC & FED

Tin họ dùng (nhãn `tin_tuc`): 577 lời ở 176/180 = 98% buổi. Fed/FOMC/lãi suất 134, CPI 43, PPI 18, NFP 28, PCE/GDP 26, chiến sự 52, Trump/thuế 18, hack 7, ETF 4, khác 247.

## C1. Tin lớn sắp ra (trong ngày / 24h tới)

- **Tình huống**: CPI, PPI, NFP, PCE, FOMC ra tối nay hoặc ngày mai.
- **Người đó nhìn/kiểm**: lịch tin đỏ USD, giờ ra tin; giá đang chạy trước tin ra sao.
- **Kết luận + hành động**: né khung giờ tin (trước tin khoảng 1 tiếng đến sau tin 4–8 tiếng), không giữ lệnh qua tin, đánh nhẹ hoặc đứng ngoài; hướng H4 không đổi vì tin sắp ra.
- **Tần suất**: nhãn: tin lớn nói TRƯỚC khi ra 161 lời, trong đó dặn né/thận trọng/đứng ngoài 52; buổi có dặn né tin 80/176 = 45% số buổi có nói tin. [đo] có tin lớn trong 24h sau buổi: LẬT 6/24 = 25% (≈ nền 24%); buổi trước dặn chờ/né tin: buổi sau LẬT 12/70 = 17%.
- **Ví dụ**:
  - [10-28 · 00:12:23](https://www.youtube.com/watch?v=Gu1XtyNNH6I&t=743s) "Trước tin khoảng 1 tiếng và sau tin khoảng 4 hoặc 8 tiếng thị trường sẽ biến động; sau khoảng thời gian đó mọi thứ quay về đúng cấu trúc thị trường là thanh khoản cộng với cấu trúc giá. ... Hôm nay anh em đừng kỳ vọng trong ngày có sóng dễ đánh, vì hôm nay là ngày có tin"
  - [01-13 · 00:30:35](https://www.youtube.com/watch?v=vg80vm31RLM&t=1835s) "Tối nay chúng ta sẽ có tin cực kỳ quan trọng đó là CPI. Làm gì làm nhớ né giờ tin này ra bởi vì đây là tin quan trọng. Né giờ tin này. CPI rất quan trọng bởi vì bây giờ nó reset."
  - [03-18 · 01:09:06](https://www.youtube.com/watch?v=oyJGNnpopXw&t=4146s) "Thủng khỏi cái vùng 73k6, 73k7 này thì té. Bởi vì khả năng rất là cao nó có thể rụng về đến tận 72 cho đến 71.000. Dưới này có một cái gap nữa. Và tối nay là 1:00 sáng có tin. Cho nên các bạn tốt nhất là không giữ lệnh qua tin, cho nó chắc kèo"

## C2. Đọc đường giá TRƯỚC tin để đoán SAU tin

- **Tình huống**: vài ngày trước tin lớn, nhất là FOMC/CPI.
- **Người đó nhìn/kiểm**: trước tin giá đã tăng, đi ngang hay giảm.
- **Kết luận + hành động**: trước tin chạy hướng nào thì sau tin hay chạy ngược lại; trước tin đi ngang thì khoảng 12 tiếng sau tin mới chạy; giá tăng trước tin thì thận trọng vì dễ bị "lấy cớ" để xả.
- **Tần suất**: nhãn: 16 buổi nói rõ kiểu "trước tin … sau tin …"; tin lớn kèm dự hướng ("ra X thì giá Y") 26 lời.
- **Ví dụ**:
  - [01-27 · 00:34:27](https://www.youtube.com/watch?v=Q2qX5gIvNC8&t=2067s) "Khả năng là thị trường sẽ nhập nhằng cho đến ngày ra tin lãi suất. Khi gần ra tin lãi suất thì các bạn để ý, nếu trước tin nó chạy theo hướng nào thì thường sau tin một vài ngày nó chạy ngược lại."
  - [04-08 · 00:28:04](https://www.youtube.com/watch?v=l8hl1XtxPr4&t=1684s) "Thường trước tin chạy, đến tin nó đứng, sau tin nó mới chạy ngược lại nếu nó đảo."
  - [04-07 · 00:27:24](https://www.youtube.com/watch?v=HeBpJr0i6Bg&t=1644s) "…thì sau thứ sáu cho dù tin tốt hay tin xấu đi nữa thì sau một khoảng thời gian hấp thụ xong tin khoảng độ khoảng 12 tiếng sau tin thị trường sẽ bắt đầu tăng lại."
  - Kiểm lại sau tin: [01-29 · 00:02:28](https://www.youtube.com/watch?v=8NrjverKQpo&t=148s) "Chủ yếu sau cái tin lãi suất ngày hôm qua thì giá nó lợi dụng tin để nó lên, như mình nói nếu mà nó tăng trước tin thì sau tin nó gãy, nếu sideway trước tin thì sau tin nó tăng rồi lại gãy. Chung quy lại thì cái gì rồi cũng gãy thôi. Hôm qua cái nhịp này mình báo anh em trên tele là nó đến cái nơi cần đến."

## C3. Tin đã ra: tin là "cái cớ", GIỮ view

- **Tình huống**: sáng hôm sau một tin lớn.
- **Người đó nhìn/kiểm**: giá phản ứng thế nào, có phá cấu trúc không (tin xấu mà giá vẫn giữ = lực mua tốt).
- **Kết luận + hành động**: tin chỉ tác động 1–2 tiếng rồi giá trở về xu hướng; giữ view. Chỉ đổi khi giá phản ứng tạo cấu trúc mới tại vùng kỹ thuật (vd CPI 11/06).
- **Tần suất**: [đo] tin lớn ra giữa 2 buổi: 26 buổi → GIỮ 81%, LẬT 4/26 = 15% (không có tin giữa 2 buổi: LẬT 25%). Nhãn: buổi nói tin là "cái cớ" / "hợp lý hóa đường giá" / "cho vui" 36.
- **Ví dụ**:
  - [10-14 · 00:44:49](https://www.youtube.com/watch?v=BlA26qxNBTE&t=2689s) "Nhớ nhá: không phải cứ tin xấu thì thị trường giảm, tin tốt thì tăng, mà tin chỉ là cái cớ để thị trường có cơ sở làm giá tại thời điểm đó."
  - [06-12 · 00:38:32](https://www.youtube.com/watch?v=x75V4Kb1fj4&t=2312s) "…Thường những chỉ số như thế chỉ tác động giá trong ngắn hạn, loanh quanh một hai tiếng sau ra tin. Đến bây giờ chỉ số này không tác động đến thị trường được nữa. Thị trường trả về đúng trạng thái momentum, trả lại đúng động lực của nó.…"
  - Ngoại lệ đổi view: [06-11 · 00:22:02](https://www.youtube.com/watch?v=Xix-qwmyPkE&t=1322s) "Nhưng trước cái tin hôm qua thì giá đã được cứu và kéo lên cái cây màu xanh này, cây có tin."

## C4. Đọc Fed theo KỲ TỚI + xác suất

- **Tình huống**: trước/sau mỗi kỳ FOMC; khi CPI/PPI/PCE vừa ra.
- **Người đó nhìn/kiểm**: xác suất giữ/tăng/giảm lãi suất ở kỳ họp KẾ TIẾP (họ xem chủ yếu trên Investing/CME FedWatch; nhãn ghi nguồn "fedwatch" 8 lần; Polymarket chỉ nhắc 1 lần, 29/07 — ví dụ dưới); lộ trình Fed đã nói; số liệu lạm phát.
- **Kết luận + hành động**: kết quả kỳ hiện tại ít ý nghĩa nếu kỳ sau đã được định giá tăng; xác suất tăng cao → "thị trường sợ", "còn tâm trí đâu mà mua" → không có lực tăng; xác suất 30–60% thì "còn sai được", ~90% là "căng".
- **Tần suất**: nhãn: 134 lời về Fed; nói về kỳ tới / xác suất ở 55 buổi; [đo] GIU_LAT: Nhắc Polymarket / xác suất lãi suất: 21 lời ở 18 buổi. [đo] GIU_LAT §8 (Polymarket dùng làm thước đo thay cho Investing): P(tăng) kỳ tới > 70%: 6 buổi, H4 GIẢM 100%; 30–70%: 37 buổi, GIẢM 65%; < 30%: 134 buổi, GIẢM 49%. Kỳ gần nhất có phiếu muốn TĂNG: GIẢM 72%; kỳ gần nhất Fed TĂNG: GIẢM 70%.
- **Ví dụ đầy đủ 16/10 → 30/10/2026** (FOMC 27–28/10: giữ 3,75–4,00%, phiếu 10–2, 2 phiếu muốn tăng — `fomc_ket_qua_2026.csv`):

| Lúc | Lời người đó | [đo] Polymarket cùng lúc |
|---|---|---|
| 16/10 sáng | [10-16 · 00:36:12](https://www.youtube.com/watch?v=lSGpwulXi5s&t=2172s) "Nếu qua tuần sau vẫn duy trì được trên 60% thì mình nghĩ tháng 10 này sẽ không tăng lãi suất. Nhưng tháng 10 này nếu không tăng lãi suất thì cũng chưa chắc Bitcoin sẽ tăng nhá." | kỳ 10: giữ 71%, tăng 28% · kỳ 12: tăng ~80% |
| 28/10 sáng | [10-28 · 00:06:32](https://www.youtube.com/watch?v=Gu1XtyNNH6I&t=392s) "Xác suất giữ nguyên lãi suất 90% thì gần như chắc chắn sẽ giữ nguyên lãi suất rồi." | kỳ 10: giữ 96% |
| 28/10 sáng | [10-28 · 00:08:58](https://www.youtube.com/watch?v=Gu1XtyNNH6I&t=538s) "Hai đợt tăng lãi suất từ đó đến cuối năm mà đợt tháng 9 tăng một đợt, đợt tháng 10 này không tăng thì có nghĩa là cái đợt tháng 12 là gần như chắc chắn sẽ là một cái đợt tăng lãi suất để nhá." | kỳ 12: tăng ~78% |
| 28/10 sáng | [10-28 · 00:09:35](https://www.youtube.com/watch?v=Gu1XtyNNH6I&t=575s) "Cho nên việc không tăng ở kỳ tháng 10, cá nhân mình đánh giá là không có quá nhiều ý nghĩa tác động lên thị trường." | |
| 29/10 đêm (live tin) | [10-29 · 00:40:53](https://www.youtube.com/watch?v=4Hg5YedKaAg&t=2453s) "Gần 90% ngồi sợ tháng 12 tăng lãi suất thì còn tâm trí đâu mà mua. Anh em thấy thị trường nó lạ không?" | kỳ 12: tăng ~80% |
| 29/10 đêm | [10-29 · 00:41:29](https://www.youtube.com/watch?v=4Hg5YedKaAg&t=2489s) "Cho nên phân tích lãi suất với thị trường, anh em phải có view rộng ra một tí, phải hiểu bản chất lãi suất tác động đến cái gì, lạm phát này kia, chứ không có công thức cố định nào kiểu lãi suất tăng thì giá giảm, lãi suất giữ nguyên thì giá tăng." | |
| 29/10 sáng | [10-29 · 00:31:49](https://www.youtube.com/watch?v=wcDxLBw0TO4&t=1909s) "…Đây là điểm thị trường đang sợ ... Nếu không có thay đổi gì thì 80% là tăng lãi suất tháng 12, tức tháng 12 sẽ là một nhịp xấu." | kỳ 12: tăng ~81% |
| 29/10 sáng | [10-29 · 00:32:20](https://www.youtube.com/watch?v=wcDxLBw0TO4&t=1940s) "Đây là điểm thị trường đang sợ: cuối năm Fed còn tăng lãi suất thì làm sao đầu tư, làm sao thị trường tăng được?" | |
| 30/10 sáng | BTC về ~76–77k (tin hack Binance chồng lên — xem C6) | kỳ 12: tăng ~72% |

  Hướng H4 cuối buổi của họ (nhãn) 26/10 → 30/10: 10-26 GIAM · 10-27 GIAM · 10-28 GIAM · 10-29 đêm GIAM · 10-29 GIAM · 10-30 GIAM. Giá BTC lúc nói: 10-26 79500 · 10-27 80200 · 10-28 81000 · 10-29 81000 · 10-29 79500 · 10-30 77000.

- **Ví dụ khác**:
  - [02-16 · 00:23:23](https://www.youtube.com/watch?v=0zDtKlmcydA&t=1403s) "Kỳ kế tiếp là tháng 3, ngày 19 tháng này thì gần như FED nó sẽ không giảm lãi suất nữa bởi vì tốt rồi, đủ rồi, không cần phải dùng đến công cụ lãi suất nữa."
  - [09-15 · 00:29:56](https://www.youtube.com/watch?v=M1ZThKy2Ylk&t=1796s) "Xem Investing: 89% nghiêng vào xác suất tăng lãi suất. Thông thường theo kinh nghiệm của mình khi tỉ lệ này là 30, 40 hay 60 thì còn có xác suất sai sai một tí, chứ 89 thì nghe hay căng đấy, anh em thận trọng nhá."
  - [07-29 · 00:09:28](https://www.youtube.com/watch?v=2FMmTeLGCNY&t=568s) "Polymarket dự đoán 75% là không thay đổi gì. Thực tế thì không thay đổi gì thì cũng bình thường. Nhưng mà chắc không thay đổi gì thì về bản chất thị trường nó sẽ tăng nhẹ sau tin."
  - [09-17 · 00:28:34](https://www.youtube.com/watch?v=1cUPKUmEnr4&t=1714s) "Anh em hiểu: Fed tăng lãi suất thì sẽ thu hút dòng tiền quay trở lại trái phiếu, tiền gửi, các quỹ lớn."

> **Nguồn khác — chỉ để GIẢI THÍCH nguyên do, KHÔNG phải người hình mẫu** (kênh @doantoancoin, `transcripts/khac/doantoancoin/NGUYEN_DO.md`; phụ đề không có mốc giờ): lãi suất tăng/giữ cao → thanh khoản thu hẹp, người vay phải bán tài sản, "Cá mập không dám gom hàng khi lãi suất sắp tăng vì làn sóng bán tháo của nhỏ lẻ sẽ đổ tới" ([01/09](https://www.youtube.com/watch?v=BJGUNjteHZY)); Fed giữ nguyên ở kỳ này nhưng kỳ sau vẫn tăng thì "giữ nguyên là trung lập: như án tử đổi thành chung thân" ([12/09](https://www.youtube.com/watch?v=Ac3cxiYEgMI)). Người hình mẫu FAM nói cùng chiều ở 17/09 (dòng tiền quay về trái phiếu, tiền gửi) và 29/10 ("làm sao đầu tư, làm sao thị trường tăng được").

## C5. Đêm FOMC: kết quả → hành động định sẵn

- **Tình huống**: live đêm ra quyết định lãi suất (khoảng 1:00 sáng giờ VN).
- **Người đó nhìn/kiểm**: con số Fed công bố so với 3 nhánh đã định trước; quan điểm Fed "diều hâu hay bồ câu".
- **Kết luận + hành động**: giữ nguyên → long market; tăng 50 điểm → đánh xuống không cần nghĩ; tăng 25 điểm → "đấu trí" (khoảng 70% xấu). Tăng 25 điểm là tin xấu trung hạn. Trước giờ tin thì giữ an toàn, không giữ lệnh qua tin (C1).
- **Tần suất**: [đo] trong cửa sổ FOMC (≤ 72h trước / ≤ 24h sau): 28 buổi → GIỮ 82%, LẬT 2/28 = 7% (ngoài cửa sổ: LẬT 27%); hướng H4 trong cửa sổ: GIẢM 64%.
- **Ví dụ**:
  - [09-17 · 00:27:00](https://www.youtube.com/watch?v=7mETSY5t5Yg&t=1620s) "Tức là 50 điểm thì mặc định đánh xuống, không cần phải nghĩ, chỉ có là 25 điểm thì chúng ta mới cần phải đấu trí với thị trường thôi."
  - [09-17 · 00:58:33](https://www.youtube.com/watch?v=7mETSY5t5Yg&t=3513s) "Cơ bản mình chỉ muốn nhắc lại: tăng lãi suất 25 điểm là một tin xấu về trung hạn ở giai đoạn này của thị trường. Còn ngắn hạn thì thực tế không đáng kể."
  - [04-29 · 00:30:40](https://www.youtube.com/watch?v=-YYkW3NZT0M&t=1840s) "Cho nên chúng ta cần đảm bảo an toàn khi có tin là xong. Đó là việc duy nhất các bạn cần làm đối với phản ứng tin tức."

## C6. Tin khác: chiến sự, Trump, hack, chủ tịch Fed mới

- **Tình huống**: tin địa chính trị (Mỹ–Iran), phát biểu Trump, sàn bị hack, chủ tịch Fed phát biểu.
- **Người đó nhìn/kiểm**: giá phản ứng có giữ được không; tin có trùng vùng kỹ thuật không; thanh khoản sau tin.
- **Kết luận + hành động**: tin xấu mà giá vẫn hồi nhanh → lực mua tốt, thôi short; tin trùng vùng kỹ thuật thì "mọi thứ tự động khớp"; tin không dự đoán được (hack) thì không đoán, nhìn áp lực thanh khoản; lúc chủ tịch Fed phát biểu thì đứng ngoài.
- **Tần suất**: nhãn: chiến sự 52 lời, Trump/thuế 18, hack 7, ETF 4.
- **Ví dụ**:
  - [03-02 · 00:37:58](https://www.youtube.com/watch?v=GYgaZiYqRXY&t=2278s) "Thị trường bị bán bởi tin này nhưng sau đó lực mua nhảy vào và phục hồi giá rất nhanh. Chứng tỏ đoạn này lực mua giữ giá tốt và lực bán suy yếu, vì tin khủng như vậy mà phe mua vẫn giữ và cover được, nên cá nhân mình không short nữa."
  - [03-24 · 00:21:23](https://www.youtube.com/watch?v=xKTPieljFuY&t=1283s) "khi giảm về 70 lại về đúng vùng 67000, trendline hai ngày vừa rồi, lại có tin Trump với Iran 48 giờ, mọi thứ tự động khớp với nhau... Về phân tích kỹ thuật, giá chạm khẽ trendline ở đằng dưới này, thêm một cái rất đẹp nữa là vùng 67.000 này... Khả năng quét Bitcoin 64.000?…"
  - [10-30 · 00:14:37](https://www.youtube.com/watch?v=f0JWA9aDHl8&t=877s) "…Mình không dự đoán được sàn bị hack đâu ... Nhưng anh em xem livestream và view của mình thì tạm thời chúng ta vẫn đang đi đúng hướng nhá." · [10-30 · 00:53:20](https://www.youtube.com/watch?v=f0JWA9aDHl8&t=3200s) "Xem lại ngày Bybit bị hack (21 tháng 2 2025) thì thị trường cũng không có vấn đề gì lúc đó, nhưng sau đó mới xảy ra nhịp chạy: giảm từ 98 về 76 tạo đáy ngắn hạn rồi break lên. Cho nên đâu phải tin ra là giá chạy căng ngay ngày ra tin. Cái đáng sợ là áp lực lên thanh khoản"
  - [07-01 · 00:27:07](https://www.youtube.com/watch?v=WNiQnpm2BLo&t=1627s) "…Cho nên những thời điểm có các bài phát biểu này anh em nên tắt chart đi, vì nó biến động cũng ác lắm."

---

# D. GIỮ / ĐÓNG LỆNH TRUNG HẠN

Nhãn `giu_dong`: 819 quyết định ở 176 buổi (đóng 430, giữ 238, chốt một phần 123, gồng 27). [đo] Đóng/chốt ở buổi họ đổi view H4 (LẬT/PV): 146/548 = 27% lần đóng; tỉ lệ buổi đổi view trong mọi buổi có `giu_dong`: 28%

## D1. Lệnh short từ đỉnh 124–126k: giữ cả năm, chốt dần

- **Tình huống**: lệnh short mở quanh đỉnh 10/2025, giá đã giảm sâu.
- **Người đó nhìn/kiểm**: view chu kỳ (A1); vùng giá mà "xác định có khả năng là đáy để mua spot".
- **Kết luận + hành động**: đã chốt 90% ở vùng 90–100k, giữ 10% "kỷ niệm", ăn funding; chỉ chốt nốt khi xác định đáy.
- **Tần suất**: nhãn 14 mục / 14 buổi.
- **Ví dụ**:
  - [01-23 · 00:47:03](https://www.youtube.com/watch?v=ACM0WA7Rt3I&t=2823s) "Riêng cái lệnh Bitcoin, lệnh short của mình từ 125.000 từ bữa đến giờ cứ liên tục là dương phí funding"
  - [03-04 · 00:57:03](https://www.youtube.com/watch?v=OawlrpkFqQk&t=3423s) "Cho nên vùng đó là mình té 90% volume. Bây giờ giữ lại 10% thôi. 10% này thì có lẽ là mình sẽ giữ, chưa biết khi nào, có thể là 40.000 hoặc 20.000 gì đó."
  - [06-24 · 01:05:33](https://www.youtube.com/watch?v=ZrqOEgiFEF8&t=3933s) "Còn lệnh sell còn 126 con, khi nào chốt mình sẽ làm một video cho lệnh đó để anh em xem. Khi nào mình xác định là có khả năng là đáy của thị trường để mua spot thì bắt đầu có lẽ là mình sẽ chốt lệnh đó."
  - [09-18 · 00:59:26](https://www.youtube.com/watch?v=YPMgjMxL2io&t=3566s) "Từ ngày 6 tháng 10 đến bây giờ là 343 ngày, gần 365 ngày rồi nhá."

## D2. Giá chạm đích / vùng cản đã định → chốt ngay

- **Tình huống**: giá tới TP, đích, MA200 D1, vùng gap đã nói từ trước.
- **Người đó nhìn/kiểm**: đích đã đủ chưa; không đoán sau đó lên hay xuống.
- **Kết luận + hành động**: chốt ngay (kể cả nửa đêm), không tham; "có target thì phải có hành động".
- **Tần suất**: nhãn: đóng/chốt khi chạm đích, cản, đủ lãi 145 mục / 104 buổi. [đo] GIU_LAT §7: trong các lần ĐÓNG, nhóm "chạm / gần TP, đích, vùng cản; đủ lãi" chiếm 271 lần = 64%.
- **Ví dụ**:
  - [04-21 · 00:31:35](https://www.youtube.com/watch?v=AG126RfNCk4&t=1895s) "Việc của mình là cứ chờ lên trên này chúng ta chốt, đủ target của nhịp tăng lần này. Tất nhiên trưa nay mà nó lên 80 mình chốt trong 1 phút luôn."
  - [05-11 · 00:22:16](https://www.youtube.com/watch?v=jm7VS-lKW8w&t=1336s) "Đã chốt hết 82 cực kỳ đẹp. Lúc sáng mình cũng có chốt. 82 mình cũng đã chốt thêm một vài vị thế spot."
  - [05-18 · 00:11:54](https://www.youtube.com/watch?v=phLlmyf_8-w&t=714s) "Chốt 70% là ok. Chốt khoảng quanh 80% là đẹp. Mình chốt nhiều hơn, chốt chín mươi mấy phần trăm, gần như chốt sạch. Để lại một ít thuộc tài sản dài hạn thì không chốt."

## D3. Lệnh đang lãi, nhiều đích → chốt từng phần theo nấc định trước

- **Tình huống**: lệnh swing/spot lãi, phía trước có nhiều đích.
- **Người đó nhìn/kiểm**: các nấc đích (Fibo, cản), khối lượng ghi sẵn cho mỗi nấc.
- **Kết luận + hành động**: chốt 30% / 30% / 30%, chừa ít cho đích xa; chốt bớt ở vùng cản đầu tiên.
- **Tần suất**: nhãn: 123 mục chốt một phần (123 mục / 84 buổi).
- **Ví dụ**:
  - [04-17 · 00:18:48](https://www.youtube.com/watch?v=PH5pABMJ01k&t=1128s) "Ở 78 mình có thể tùy theo nhưng kế hoạch là có thể chốt 30%, lên 80 thì chốt 30%, lên 83 thì chốt 30% nữa và chừa lại 10% để lên 90 chốt thôi."
  - [01-06 · 00:09:44](https://www.youtube.com/watch?v=aQbHs7J80jc&t=584s) "nếu bắt được ở dưới này thì cái vùng này ai cảm thấy chốt lãi thì hoàn toàn có thể chốt. Hoặc là chúng ta cảm thấy lãi nó cũng lớn một tí thì có thể chốt bớt một phần."
  - [03-27 · 00:44:21](https://www.youtube.com/watch?v=1RmIBcPxX2I&t=2661s) "Đến thời điểm này nó đã dump khỏi như vậy thì nếu muốn tiết kiệm tiền thì có thể out luôn hoặc out bớt 1/2 volume ở giá hiện tại, giữ lại một ít vốn để khi nó dump về dưới này thì giảm thiểu rủi ro."

## D4. Lý do vào lệnh mất (nến đóng thủng mốc) → đóng

- **Tình huống**: lệnh swing đang giữ, nến H4/D1 đóng thủng đáy/đỉnh làm SL.
- **Người đó nhìn/kiểm**: nến đóng (không tính râu) qua mốc SL đã đặt từ lúc vào.
- **Kết luận + hành động**: rời lệnh; "vào vì lý do gì ra vì lý do đó".
- **Tần suất**: nhãn: đóng vì thủng/gãy/SL/sai 158 mục / 106 buổi.
- **Ví dụ**:
  - [03-27 · 00:24:53](https://www.youtube.com/watch?v=1RmIBcPxX2I&t=1493s) "H4 này hôm trước anh em nào mà swing thì hiện tại cũng out luôn. Bởi vì trong cái swing hôm trước thì stop loss là gì? Khi nó thủng vào cái đáy H4 gần nhất... bắt buộc chúng ta sẽ phải rời tàu."
  - [04-03 · 00:31:29](https://www.youtube.com/watch?v=vnCUK9ayUsI&t=1889s) "chờ xem nếu H4 ngày hôm qua mà nó đóng dưới khỏi đường 6600 này thì khả năng hôm qua chúng ta sẽ TP được ở giá 65 cho đến 64 nhưng không, sau đó nó vẫn kéo lên thì thôi, kéo lên thì chúng ta phải bỏ thôi... sau cây H4 ngày hôm qua chúng ta không thể giữ được lệnh short. Đừng tiếc bởi vì cái đó."
  - [06-09 · 00:14:03](https://www.youtube.com/watch?v=UmnCq7p4NlU&t=843s) "Trong trường hợp tệ hơn thì chúng ta có thể là DCA ở quanh cái vùng 60, DCA ở dưới cái vùng 60 này và khi mà nến H4 nó thủng 60 chúng ta mới nhảy thì cái stop loss nó sẽ thấp lại nó sẽ gần lại."

## D5. Theo lịch: tin, đêm Chủ nhật, thứ Hai → đóng lệnh ngắn; thứ Bảy–Chủ nhật giữ chung nhịp

- **Tình huống**: sắp có tin; tối Chủ nhật; thứ Hai tăng nóng; thứ Sáu.
- **Người đó nhìn/kiểm**: lịch trong tuần.
- **Kết luận + hành động**: không giữ lệnh từ thứ Hai sang thứ Ba; đêm Chủ nhật đóng hết, reset; thứ Sáu reset tài khoản; thứ Bảy–Chủ nhật chạy chung một nhịp nên giữ qua 2 ngày, xử lý trước khoảng 17h Chủ nhật.
- **Tần suất**: nhãn: đóng vì lịch 41 mục / 38 buổi; giữ vì lịch 9 mục / 8 buổi.
- **Ví dụ**:
  - [01-06 · 00:05:50](https://www.youtube.com/watch?v=aQbHs7J80jc&t=350s) "Tối qua đi ngủ là cắt ăn hết, chốt đi ngủ thôi. Bởi vì ngày thứ hai cho nên mình không giữ lệnh từ ngày thứ hai đến ngày thứ ba. Đặc biệt khi ngày thứ hai nó tăng nóng quá, hôm qua nó tăng khỏe quá thì thôi chúng ta chốt lãi ăn."
  - [05-11 · 00:27:56](https://www.youtube.com/watch?v=jm7VS-lKW8w&t=1676s) "Cứ đêm chủ nhật là đóng hết lệnh, reset. Đánh phải biết cái tính thời điểm là như vậy."
  - [01-09 · 00:55:28](https://www.youtube.com/watch?v=YLu3KxaMspQ&t=3328s) "Những ngày cuối tuần thì lưu ý mọi người đánh những nhịp liên tục hai ngày chứ không nhất thiết phải clear ngày. Bởi vì cuối tuần thì thông thường nó chạy chung một nhịp, hai ngày thứ bảy, chủ nhật chạy chung một nhịp sóng.…"

## D6. Spot: giữ phần dài hạn, chốt lướt theo F&G / vùng cản, DCA đều

- **Tình huống**: có spot mua ở vùng thấp; giá hồi lên vùng cản; F&G tăng.
- **Người đó nhìn/kiểm**: F&G (alternative.me) theo thang mùa downtrend; vùng cản D1; plan DCA dài hạn.
- **Kết luận + hành động**: phần lướt: F&G ~20 bớt FOMO, 30 chốt một ít, 50 phải chốt; chạm cản lớn thì chốt gần hết; phần dài hạn không chốt giữa chừng, DCA đều tới giữa 2027.
- **Tần suất**: nhãn: lệnh spot 102 mục / 84 buổi; dùng F&G để giữ/đóng 9 mục / 9 buổi.
- **Ví dụ**:
  - [06-12 · 00:36:52](https://www.youtube.com/watch?v=x75V4Kb1fj4&t=2212s) "Lên đến vùng khoảng 20 là bớt FOMO lại, tìm điểm chốt lãi. Lên đến vùng 30 là bắt đầu phải chốt một ít. Lên đến 50 là phải chốt, đừng nghe thị trường nó lừa."
  - [09-14 · 00:30:20](https://www.youtube.com/watch?v=ykgTTK3EbP8&t=1820s) "Việc DCA vẫn giữ, nhưng ở dưới đang ít hàng nên mình không muốn thoát ở vùng này, vì plan của mình là thoát hàng đâu đó khoảng 1 đến 2 năm nữa."
  - [10-29 · 00:29:15](https://www.youtube.com/watch?v=wcDxLBw0TO4&t=1755s) "vô tình đồng bộ với plan của mình: downtrend sẽ kéo dài, xấu nhất đến hết 2027, còn không thì đến khoảng tháng 6 năm 2027, tức quý 2 năm 2027. Như các lần trước mình nói, mình DCA theo plan đến khoảng giữa năm 2027, chứ không phải hiện tại là hết downtrend rồi."

## D7. Gồng: chỉ khi SL đã về entry

- **Tình huống**: lệnh đang lãi, muốn để chạy tiếp.
- **Người đó nhìn/kiểm**: SL đã kéo về entry chưa; lực nến khi tới đích.
- **Kết luận + hành động**: chỉ gồng khi SL ở entry; về entry thì cắt hòa; tuyệt đối không gồng lỗ; giữ view, không để sóng ngắn hạn "nuốt" góc nhìn.
- **Tần suất**: nhãn: 27 mục "gồng" (27 mục / 23 buổi).
- **Ví dụ**:
  - [01-07 · 00:26:53](https://www.youtube.com/watch?v=NOBgwE4Gdko&t=1613s) "phải xác định stop loss nằm ở entry. Tức là nếu trong trường hợp xấu nó về entry thì phải cắt hòa chứ không gồng lỗ. Tuyệt đối không gồng lỗ."
  - [01-16 · 00:16:28](https://www.youtube.com/watch?v=SllvhCOjrkE&t=988s) "Thằng này cứ để vậy cũng là một điểm để chúng ta gồng. Nếu trong lúc nó lên đây mà cảm thấy lực mạnh quá, không ổn thì có thể cắt sớm, bởi vì nó có thể lên đến 98. Hoặc nếu cảm thấy lực nó yếu thì có thể gồng bởi vì chúng ta đi đòn bẩy thấp thì tùy theo lực thị trường, tùy theo nến."
  - [06-11 · 00:28:33](https://www.youtube.com/watch?v=Xix-qwmyPkE&t=1713s) "Ví dụ đến chiều nó đập về giảm đâu đó khoảng 61004 sau đó cứ sideway ở đó thì tự khắc các bạn quên mất view này ngay. Các bạn sẽ bị những con sóng ngắn hạn nuốt mất góc nhìn dài hạn."

## D8. Bot lưới short: giữ tới vùng đích, đủ thì chốt

- **Tình huống**: bot lưới short BTC đang chạy (biên rộng).
- **Người đó nhìn/kiểm**: giá về vùng đích dự kiến chưa; lãi đã "đủ" chưa.
- **Kết luận + hành động**: giá càng lên càng nhồi thêm vol vào bot (không mở bot mới); về vùng đích (72–71k) hoặc thấy đủ thì đóng.
- **Tần suất**: nhãn: 13 mục / 12 buổi.
- **Ví dụ**:
  - [05-06 · 00:37:48](https://www.youtube.com/watch?v=ZEZOrGhyb6I&t=2268s) "bot của mình hiện tại nó chạy lên đến khoảng 95 96.000 mà có thể mình không mở thêm nhưng mà mình sẽ nhồi thêm vol ở trong bot hiện tại cho tiện cũng được."
  - [05-28 · 00:45:28](https://www.youtube.com/watch?v=IY2JeSNTTfQ&t=2728s) "Cứ đủ tiền thì chốt, đủ thì cứ chốt vẫn được. Nhưng mà cá nhân plan thì mình tính là về 72, còn không thì cứ thả đấy luôn."
  - [06-02 · 00:02:27](https://www.youtube.com/watch?v=5JIlkl46nss&t=147s) "Hôm qua chúng ta đã chốt con bot rồi mọi người. Con bot short của chúng ta ăn đến đó là được. Mặc dù thị trường hôm nay nếu giữ thì nó cũng đi được khoảng 2000 giá nữa. Nhưng không biết giá chạy đến đâu, chạy đến đây là đủ rồi."
