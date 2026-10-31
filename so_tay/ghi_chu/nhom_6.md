# Nhóm 6 — 20 buổi live 26/06 → 28/07/2026 (FAM Trading, người nói tự gọi "Eric")

Nguồn: 20 file zip_clean trong `_ds_6.txt`. Trích dạng `[ngày giờ]`; "N/20" = số buổi có ý đó (đếm bằng grep + đọc).

## 1. Bối cảnh giai đoạn
- BTC 57–67k. Nến tháng 6 "gần như là tháng xấu nhất từ đầu năm" [2026-07-01 00:08:43], đáy tạm ~57–58k; hồi 64 (06/7), về 62 (09/7), CPI tốt → 65 (15/7), 66–67 (22/7), bị từ chối ở 66 → 63k (28/7).
- Người đó coi là downtrend xác nhận từ 85k giữa tháng 4 [2026-07-13 00:19:41]; đã chốt spot BTC 86→120k [2026-06-30 01:01:06].
- Sự kiện: World Cup (tháng "coin luôn nát" [2026-07-01 00:08:10]), Mỹ nghỉ lễ 4/7, CPI 3.5% vs 4.2% [2026-07-15 00:13:19], FOMC 29–30/7 (61% giữ / 38% tăng [2026-07-27 00:30:20]), chiến tranh Mỹ–Iran (dầu 68→92), MicroStrategy bán BTC, thuế crypto VN 0,1% từ 1/7, Nghị định 284 phạt từ 1/9, VN-Index và lãi suất ngân hàng VN xấu đi.

## 2. Quy trình một buổi live
Thứ tự điển hình (~18/20 buổi):
1. **Mở (5–20 phút)**: báo lệnh đang chạy (TP/SL lệnh sáng), lướt vàng/dầu/alt nóng, trả lời vài câu. Có buổi tới phút 35 mới vào BTC [2026-07-09 00:35:01].
2. **BTC từ khung lớn xuống**: "khung tuần, và sau đó mới đi vào những khung nhỏ hơn" [2026-07-13 00:14:49]. Thứ 2/đầu tuần → khung tuần (06/7, 13/7, 21/7, 27/7); đầu/cuối tháng → nến tháng (30/6, 01/7, 27/7); ngày thường từ D1 → H4 → H1/30m → M5.
3. **Ra plan** ngay sau phần BTC (~10–15 phút): vùng chờ, mốc đổi view, TP/SL.
4. **Checklist chỉ số** (~5 phút, thứ tự gần cố định): BTC.D → USDT.D → Gap → (DXY) vàng/bạc/dầu → F&G → heatmap thanh lý → Hyblock → lịch tin.
5. ETH + altcoin top, rồi hỏi đáp; giữa chừng canh **nến H4 đóng lúc 11:00** ("10:59 nó nhảy sớm khoảng 3 giây" [2026-07-02 01:03:11]).
6. **Kết**: "view này… dùng đến…" + cập nhật Telegram/Discord [2026-07-01 00:53:01], [2026-07-24 01:02:47].
- Khác biệt: T6/trước ngày nghỉ → view cho cả cuối tuần [2026-07-16 00:16:24]; ngày có tin lớn → bài giảng vĩ mô (CPI [2026-07-15], thuế [2026-06-30], pháp lý [2026-07-21]); dùng Grok tóm tắt phát biểu FED [2026-07-16 00:29:12]; hẹn live 1h sáng đón lãi suất [2026-07-27 00:32:57].

## 3. Công cụ, nguồn dữ liệu, chỉ báo
| Công cụ | Dùng làm gì · cách đọc | Tin? | Trích |
|---|---|---|---|
| TradingView / chart Binance Futures | vẽ MA, Fibo, trendline; backtest "ít khi" | chính | [2026-07-06 00:22:19], [2026-07-02 00:31:35] |
| **MA 34/89/200** (có lúc gọi EMA), H1/H4/D1/W/M; MA200 30m ≈ MA610 5m; "MA xanh nhỏ" M5 | đọc **chuỗi test 34→89→200**; cản/đỡ | tin, nhưng tùy giai đoạn | "cấu trúc testing MA… không có sách vở nào dạy" [2026-07-06 00:27:40]; "cụm 34 89 tầm này nó không còn giá trị" [2026-07-24 00:25:10]; "bắt đầu… follow lại cái MA" [2026-07-28 00:05:21]; "như mình thì EMA" [2026-07-23 00:37:55] |
| Fibo thoái lui (đáy–đỉnh, 0.5/0.618) & mở rộng (đáy–đỉnh–điểm hồi, mức 1) | TP, vùng chờ, đích (19/20) | rất tin | [2026-06-29 00:32:57–00:36:12] |
| RSI mặc định 70/30 (D1, W) | chỉ đo sức mạnh; phân kỳ (8/20) | hạn chế | "RSI chỉ thể hiện sức mạnh chứ không phải… entry hay SL" [2026-07-09 01:05:51] |
| Heatmap thanh lý ("liquid", Coinglass) | cụm SL = nam châm / TP (20/20) | vừa | "thị trường chạy hai đầu… mình không đánh giá cao" [2026-07-01 00:26:02] |
| Hyblock ("hai block"; phụ đề đôi khi ghi "Hyperliquid") | chênh lệch long/short ($) → đọc NGƯỢC đám đông (12/20) | tin | "mình không nhảy vào team bị đông" [2026-07-06 00:34:52] |
| Fear & Greed (19/20) | <10 panic → mua; ~5 "nhắm mắt mua"; 20–30 nhập nhằng; 27+ hơi FOMO | rất tin | "chỉ cần bám theo mỗi chỉ số này là đủ chơi đủ xài" [2026-07-14 00:22:09] |
| USDT.D (18/20) | chạy ngược BTC; vẽ trendline/mô hình trên nó | tin | "thằng phá đám nhất" [2026-07-09 00:42:54] |
| BTC.D (19/20) | chỉ để xét altcoin | — | "không ảnh hưởng gì đến Bitcoin" [2026-07-14 00:29:59] |
| Gap CME (15/20) | gần như luôn "bỏ qua / mất giá trị" | không | "từ hồi CME chạy full thì không có gap nhiều nữa" [2026-07-09 00:43:27] |
| Vàng/bạc/dầu (20/20), Dow/Nasdaq, VN-Index | vàng cùng pha BTC; chứng khoán gãy → crypto gãy | tin | "vàng tăng thì đừng cố đi short BTC… indicator cực kỳ uy tín" [2026-07-03 00:24:30] |
| Funding (Binance), lịch tin, investing.com, blockchaincenter.net (rainbow, altseason, halving), Total1/3, ETH/BTC | phụ | phụ | [2026-07-07 00:10:05], [2026-06-29 00:42:27] |
| Báo giá trên sàn; Telegram (kèo nhanh), Discord, nhóm VIP | "bật thông báo… còn lại thì ra khỏi chart" | — | [2026-07-22 00:36:13] |
- Nền: lý thuyết Dow + price action căn bản; "Mình không có nhiều chiêu thức… chỉ có chừng này công cụ thôi" [2026-07-27 00:36:06]. Volume: "ảo lắm, không confirm được" [2026-07-07 00:59:32].

## 4. Cách ra nhận định
- **Chuỗi**: xu hướng khung lớn (đỉnh/đáy thấp dần, giá dưới MA) → khung nào đang "lái" → vùng cản/đỡ → kịch bản A/B → plan. "Phân tích… nhận diện các tín hiệu… đưa ra kịch bản. Kịch bản sau đó sẽ có phương án hành động… không đoán thị trường" [2026-07-14 00:23:51].
- **Nếu… thì**: "Mình chỉ biết nếu A thì sẽ đến B, còn nếu C thì sẽ đến D" [2026-06-30 00:20:14]; "theo kịch bản A B C… không phải là trade mà là ngồi phán" [2026-07-13 00:32:07].
- **Mốc đổi view = nến đóng**, có "điều kiện cần và đủ" (6/20): "nến H4 bắt buộc phải đóng qua 61.000" [2026-07-02 00:24:25]; "điều kiện đủ… thêm một cây nến nữa break ra" [2026-07-10 00:23:28]; đóng trên 66 = điều kiện cần "khoảng 50%", đủ khi nến sau xanh [2026-07-22 00:23:23].
- **Khung lái**: "không… chạy theo H4 mà… theo khung ngày với lại phục hồi khung tuần" [2026-07-21 00:17:12]; D1 và H4 ngược nhau → "cực kỳ khó chơi… lựa chọn một phe" [2026-07-07 00:21:24].
- **Phân kỳ** (5/20): "Lực bán yếu hơn không có nghĩa là lực mua mạnh hơn" [2026-06-26 00:19:03]; thang điểm bán 9→7 vs mua 1 [2026-07-13 00:16:58].
- **Xác suất**: nói % cụ thể ("65% là fake breakout" [2026-07-02 00:18:50], "trên 70% nó sẽ kéo lên 72" [2026-07-24 00:25:43], FED tăng "dưới 20%" [2026-07-24 00:30:00]); phân tích chỉ để nghiêng xác suất lên "50,8%" [2026-07-23 00:41:11].
- **Nhiều chặng**: quét lên lấy SL rồi rớt; "hồi quang phản chiếu" (8/20); chốt từng khúc 57→54→40→35 [2026-07-13 00:23:31].
- **Bộ lọc ngữ cảnh**: nến xanh thứ 2 không tin (6/20) "Chưa bao giờ mình tin tưởng vào cái cây nến xanh của ngày thứ hai" [2026-07-07 00:26:47]; D1 đỏ hôm trước → hạn chế long [2026-07-01 00:16:09]; F&G, thanh lý lệch, vàng, USDT.D; cầm lệnh qua tin → "50/50" [2026-07-15 00:08:53].
- **Kháng cự yếu dần**: "bị bán càng nhiều lần mà giá không sập thì vùng đó càng ngày sẽ càng yếu đi" [2026-07-27 00:11:23].

## 4b. BẢN ĐỒ CĂN CỨ CỦA CÁC CON SỐ
(Mốc giờ trong bảng thuộc ngày ở cột 1, năm 2026.)

| ngày | số/vùng | dùng làm gì | căn cứ họ nói | trích |
|---|---|---|---|---|
| 06-26 | 57.6/57.3 | TP short | Fibo mở rộng "non" + mô hình cờ | "cờ này cũng cho về… 573. 576" [00:04:30] |
| 06-26 | 59.8–60 | entry short | hỗ trợ 60 đã gãy + cụm SL heatmap | "lên 60k để quét stop loss của đám Liquid" [00:47:19] |
| 06-26 | 30k (23–30) | mua mạnh dài hạn | hỗ trợ khung lớn so mùa trước + trendline gãy + Fibo mở rộng 51/23 | "vào hàng mạnh ở giai đoạn từ 30" [00:11:25] |
| 06-26 | BTC 52 | đích nếu USDT.D phá | trendline USDT.D (10–10.5%) | [00:28:40] |
| 06-29 | 61.0–61.06 | đỉnh hồi / short | MA200 H1 + Fibo 1 mở rộng | "MA200 ở H1 cũng là một entry uy tín" [00:21:33] |
| 06-29 | 65 | hồi xa | MA200 H4 | "65 kéo nổi lên MA200 H4?" [00:06:18] |
| 06-29 | 58.0 | SL long | dưới râu + dưới MA + dưới Fibo 59 | [00:18:22] |
| 06-29 | 54 | đích short | H4 đóng dưới 59 | [00:17:17] |
| 06-29 | 36k / 27k | đáy xa | giảm 70% / 77% từ đỉnh | [00:26:30] |
| 06-29 | 60.15 | SL M5 | "điểm nút" đỉnh + chờ nến đóng | [00:55:40] |
| 06-29 | ETH 1100–1200 | gom ETH | ETH/BTC ~0.02 = đáy 2025 | [00:43:30] |
| 06-30 | 62 | đích nếu phá 61 | Fibo | [00:19:42] |
| 06-30 | 59.2 / 58.8 | TP scalp | cụm liquid | [00:59:52] |
| 07-01 | 52k | đích khung lớn | MA89 khung tháng (đáy mùa trước test MA89) | [00:10:52] |
| 07-01 | 66 | hồi tối đa | 50% thân nến tháng đỏ | [00:14:05] |
| 07-01 | 60.4 | short | MA200 H1 sau khi đã test 34, 89 | [00:19:59] |
| 07-01 | 59–61 | kháng cự; SL phải ngoài vùng | vùng sideway hỗ trợ cả tháng 6 đã thủng ("đồn" đổi chủ) | [00:18:20] |
| 07-02 | 62–63 | cản | Fibo D1 | [00:17:12] |
| 07-03 | 64 | đích long / chốt | MA200 H4 + RSI D1 ~50–55 | [00:14:40] |
| 07-03 | 68–69 | râu có thể vượt | tiền lệ râu vượt MA200 cũ (71→73–74) | [00:19:00] |
| 07-06 | 64 | cản để chốt lãi | MA34 D1 + MA200 H4 + Fibo = "ba cái cản" | [00:26:02] |
| 07-06 | 61.5–62 | mốc short đẹp | dưới điểm cross MA34×89 H4 | [00:30:24] |
| 07-06 | 62.07–62.09 | TP | MA200 30m ≈ MA610 5m | [00:32:37] |
| 07-07 | 64 | SL short | số tròn cản | "64 đang là một vùng giá chẵn" [00:25:14] |
| 07-07 | 62 / 57.5 | quét / đích xa | cụm thanh lý lớn; heatmap khung lớn | [00:29:29] |
| 07-07 | 11/2026; thu 2027 | đáy giá; hết downtrend | lịch halving, so 11/2022 & 9/2023 | [00:13:54] |
| 07-09 | 61.0 / 60.5 | TP short | Fibo + đám thanh lý 60–61 | [00:37:42], [00:47:18] |
| 07-10 | 61–60.5 | long đẹp | Fibo 0.5–0.618 H4 | [00:27:12] |
| 07-10 | 72 | đích tháng 7 | vai đầu vai ngược, biên ~10% | [00:28:49] |
| 07-13 | 62.1 | TP | Fibo 0.618 H1 | [00:28:19] |
| 07-13 | 57–58 | TP big short | đích tối đa mô hình hai đỉnh D1 | [00:23:31] |
| 07-13 | 54 → 43 → 35 | ải / đích | vùng thanh khoản dày khung tuần | [00:21:20] |
| 07-13 | 62.000 | nơi SL đám đông | số tròn; "hay quét qua sâu hơn… một tí" | [00:28:51] |
| 07-13 | 37k–20k | gom | giảm 70–80% từ đỉnh | [00:51:16] |
| 07-14 | 61 → 59 | mốc gãy / đích | neckline hai đỉnh H4 | [00:14:12] |
| 07-14 | 63 | đỉnh vùng DCA short | liquid + cụm MA | [00:29:59] |
| 07-15 | 66–67 | đích long | H4 trên MA200, MA bẻ lên | [00:23:03] |
| 07-16 | 61.6 | SL long | dưới trendline trợ giá ~62k | [00:15:50] |
| 07-16 | 63.7 | long tối ưu | MA200 + Fibo 0.5 + đáy râu | [00:20:37] |
| 07-21 | 70–73 | đích hồi tuần | trendline tuần + Fibo 0.5/0.618 tuần + MA34 tuần | [00:14:31] |
| 07-21 | 67 | đích D1 | MA89 D1 | [00:16:08] |
| 07-22 | 66 | kháng cự bị phá | đỉnh cũ (tắt MA để nhìn) + giá đóng nến | [00:22:52] |
| 07-22 | 65.0 | buy | Fibo + cụm thanh lý 65 | [00:30:43], [00:33:50] |
| 07-23 | 64 / 63 | mốc gãy xu hướng tăng | đáy H4 | [00:27:56] |
| 07-23 | 64–68 | biên tới FOMC | không nêu cụ thể | [00:31:39] |
| 07-24 | 68 | đích long / thoát short | "đường MA màu xanh" H4 | [00:25:10] |
| 07-24 | 72 | trước FED | **tự nhận "đoán mò… không có cơ sở"** | [00:28:25] |
| 07-24 | 53 | nếu FED tăng lãi | kịch bản tin (<20%) | [00:29:27] |
| 07-27 | 70–72 | đích | vùng trống thanh khoản bên trái + Fibo 0.5 D1 + MA200 D1 | [00:14:31], [00:16:06] |
| 07-27 | 64.06 | buy | trendline + hỗ trợ + Fibo mở rộng 1 + cản 5m — "tất cả hội tụ" | [00:22:53] |
| 07-28 | 62.5/62 & 60 | đích short | Fibo mở rộng | [00:06:23], [00:10:51] |
| 07-28 | 63–64 | sell khi hồi | Fibo hồi | [00:06:56] |

**Chọn hướng**: (1) xu hướng khung tuần/ngày cho thiên hướng; downtrend thì long chỉ là scalp ngược sóng. (2) Hướng ngắn hạn chỉ đổi khi **nến H4 (đôi khi H1/D1) đóng qua mốc đã báo trước** (61 → 64 → 66 → 68; chiều ngược 64.2). (3) Cần thêm lý do bổ trợ rồi mới chọn phe: 07-07 chọn short vì 3 lý do "downtrend + nến xanh thứ hai + thanh lý long nhiều hơn" [2026-07-07 00:23:02–00:24:38].
**Chọn vùng**: hay dùng nhất là Fibo (0.5/0.618, mức 1) và MA 34/89/200 các khung; kế đến đỉnh/đáy/râu cũ, vùng sideway cũ; số tròn; mô hình (neckline, vai đầu vai, cờ); cụm thanh lý (nam châm / TP). Tin nhất khi **2–4 căn cứ trùng nhau** ("ba cái cản", "tất cả hội tụ"). SL đặt ngoài cả vùng tranh chấp và ngoài số tròn đám đông; TP ở mốc gần nhất. Dài hạn dùng % giảm từ đỉnh, MA89 tháng, chu kỳ halving. Chỗ không có căn cứ thì tự nói "đoán mò" hoặc "chẳng qua là chúng ta nói chuyện thôi chứ nó không có bất kỳ logic nào" [2026-07-27 00:08:17].

## 5. Vào lệnh, quản lý lệnh và vốn
- **Rủi ro theo SL, không theo vốn lệnh**: "mất khoảng 5% tài khoản hoặc 2%… tối đa là 10%" [2026-07-14 00:50:41]; 500$ thì mỗi SL ≤ 25$ [2026-07-24 00:41:41].
- **Đòn bẩy suy từ SL**: đòn bẩy = 60% ÷ SL% (lệnh isolate, sàn cắt ở -80%) [2026-07-24 00:51:38]; BTC giai đoạn này "tối đa là x20… SL… khoảng 1000 giá" [2026-07-24 00:54:23]. Từng soi kèo member x30 bị thanh lý trước SL [2026-07-09 00:24:12].
- **Entry**: chia vol/limit DCA trong vùng ("chia nhỏ volume ra từ đây lên đến 63.000" [2026-07-14 00:06:29]); chờ test MA/Fibo + nến đảo [2026-07-02 01:05:17]; hai đáy chờ break + backtest [2026-07-07 00:56:53]; vào trước một phần nhỏ "để giữ chỗ" [2026-07-14 00:19:31].
- **SL**: vùng nhiễu thì SL theo nến đóng H1/H4, không limit vì "rất dễ bị lụm theo râu nến" [2026-07-02 00:21:32]; SL xa, ngoài vùng [2026-07-16 00:21:10]. Ăn TP1 xong kéo SL về entry (6/20).
- **TP**: scalp 1000–1500 giá, TP1 khi >500 giá [2026-07-07 00:32:37]; chia TP 61/60/59 [2026-07-14 00:21:05]; bán mạnh có thể "tháo TP luôn giữ về 54" [2026-06-29 00:41:51].
- **Ngược xu hướng**: vốn nhỏ, chốt sớm, "tuyệt đối không gồng" [2026-07-16 00:22:47]. Vùng nhiễu: "chọn một hướng và cố thủ" tới khi bị bẻ [2026-07-02 00:27:08].
- Hợp đồng tiêu chuẩn: mỗi lệnh độc lập, "DCA dương" = mở lệnh mới [2026-07-14 00:09:55]; đầu tháng "reset tài khoản" [2026-07-01 00:29:27].
- **Danh mục downtrend**: 10% stable, 20% alt (≤3 đồng), 70% chia đôi BTC/ETH; panic thì tiêu nốt 10%, hồi ~30% bán bớt đưa stable về 10% [2026-07-22 00:13:48–00:15:53] (buổi 27/7 lại nói 80% BTC+ETH, 10% dự phòng, 10% alt [2026-07-27 01:00:11]).
- **Gom spot**: ví dụ 50k cho BTC = 30k DCA mỗi ngày (82$ lúc 14h, "thời điểm giá hay dump nhất") + 20k chờ 3 cú flush 20–30% (10k/7k/3k) [2026-07-23 00:50:23–00:54:12]; vùng chính BTC dưới 50k, ETH dưới 1000 [2026-07-15 00:41:34]; 20k là "kịch bản xấu nhất… để… có một kế hoạch vốn" [2026-07-13 00:49:37].
- Future là công cụ tái tích lũy: "vốn to mà kiếm lợi nhuận nhỏ" [2026-07-22 00:45:12]. Không đặt mục tiêu theo ngày, chỉ theo tuần [2026-07-14 00:34:21].

## 6. Thiên hướng lớn và thay đổi
- **Dài hạn không đổi: bear**. Downtrend đi ~40% thời gian (287 ngày) [2026-07-07 00:09:01], tới 22/7 ~50% [2026-07-22 00:37:45]; đáy giá có thể ~11/2026, hết downtrend mùa thu 2027 [2026-07-07 00:13:54]; "giá… 50% mình đánh giá vẫn chưa thể là đáy" [2026-07-28 00:48:15]. Mọi nhịp tăng là hồi; nến tháng 7 xanh "không thể hiện… đã đi qua đáy" [2026-07-27 00:06:11].
- **Ngắn hạn đổi theo mốc nến**: short (26/6–2/7) → H4>61, đóng hết short, tìm long tới 64 (3/7) → short scalp ở 64 (6–9/7) → chờ long 61–60.5 (10/7) → short khi thủng 64 (13–14/7) → CPI tốt, "không nên short", long khi chỉnh (15–21/7, "tuyệt đối là không short" [2026-07-21 00:05:38]) → đích 70–72 (22–27/7) → 28/7 dính SL, quay lại sell khi hồi.

## 7. Đúng / sai nổi bật và phản ứng
- Đúng: 65–70% fake breakout + H4>61 → "bây giờ nó lên 64 thật" [2026-07-06 00:28:47]; 66–67 "đã đạt được rồi" [2026-07-22 00:04:06]; Pi về 2 số 0 [2026-07-10 00:46:04]; dầu chờ về 70 rồi lên 92.
- Sai: plan lên 70–72 hỏng 28/7 → nhận thẳng: "kế hoạch đó đã bị thất bại" [2026-07-28 00:02:40]; "cái plan của anh em đúng và cái plan của mình nó không có đúng" [2026-07-28 00:04:18]; xin lỗi người dính SL theo [2026-07-28 00:03:11]; nhận "nói trước bước không qua" về nến tháng [2026-07-28 00:28:38].
- Không đổ cho tin hay cá mập: "Mình đâu quan trọng đúng sai. Quan trọng là kiếm tiền thôi" [2026-07-28 00:49:24]. Sau chuỗi thắng vẫn "reset… phân tích lại từ đầu… khách quan" [2026-07-24 00:23:32]. Nhấn minh bạch: "chưa bao giờ một lệnh nào mà thắng thì mình post mà thua thì… im" [2026-06-29 00:30:52].

## 8. Giọng nói
- Xưng "mình", gọi "anh em / mọi người / các ông", tự gọi "Eric". Câu cửa miệng: "hồi quang phản chiếu" (8/20), "Đơn giản thế thôi" (8/20), "xổ số" cho kèo yếu (8/20), "nhịn đói", "ngồi rung đùi", "lãi không chốt thì trời chu đất diệt" [2026-06-30 00:54:10], "cố quá là quá cố" [2026-07-03 00:14:40].
- Dứt khoát khi đã có mốc ("tuyệt đối không short") nhưng luôn kèm kịch bản ngược. Hay mỉa "các thầy" vẽ đáy mới mỗi lần gãy [2026-06-26 00:14:37]. Từ chối "xem giúp" lệnh đã kẹt vì người hỏi chỉ cần "trấn an tâm lý" [2026-07-23 00:15:05]; tự nhận "chỉ phân tích… chứ không đưa ra bất kỳ kèo" [2026-07-09 01:06:57] dù vẫn post lệnh trong VIP/Telegram.
- Khuyên tâm lý: "Sợ thì đừng có chơi mà chơi thì đừng có sợ… vào vì cái gì thì… đi ra vì cái đó" [2026-07-23 00:20:59–00:22:35].

## 9. Tinh hoa (10 nguyên tắc)
1. Thuận xu hướng khung lớn, ngược sóng chỉ scalp nhỏ — "Xu hướng đó là những người có lực, có tiền họ đã ra quyết định" [2026-07-09 00:52:13].
2. Không đoán, chỉ dựng kịch bản nếu–thì rồi plan hành động — [2026-07-14 00:23:51].
3. Chỉ đổi phe khi nến đóng qua mốc báo trước (cần + đủ) — [2026-07-02 00:24:25].
4. Vùng tin được = nhiều căn cứ hội tụ — "tất cả hội tụ ở đây thì vị thế an toàn là chờ ở vùng này" [2026-07-27 00:22:53].
5. Kháng cự là chỗ chốt lãi, không phải chỗ vào lệnh ngược — "Vùng này là vùng chốt lãi chứ không phải vùng entry" [2026-07-22 00:25:59].
6. Phân kỳ / chỉ báo chỉ đo sức mạnh, không phải tín hiệu mua bán — [2026-07-13 00:16:27].
7. Tin chỉ là cớ, chu kỳ mới quyết định — "giá sập là do lực bán, giá tăng là do lực mua" [2026-07-14 01:00:02]; "yếu tố quan trọng nhất… là chu kỳ" [2026-07-22 00:16:29].
8. Rủi ro tính theo SL (2–5% tài khoản), đòn bẩy suy từ SL — [2026-07-14 00:50:41].
9. Vùng khó thì đi chậm, ăn ngắn, nhịn đói — "Cái đoạn nào mà khó chúng ta đi chậm thôi" [2026-07-24 00:40:33].
10. Cập nhật view theo từng cây nến, sai thì cắt — "Sau mỗi cây nến là thị trường lại thay đổi" [2026-07-24 00:58:50].

## 10. Khung hình cần xem
- `7D1Ve5hs4bU · 00:25:10` — "đường MA màu xanh" H4 ~68k là MA hay EMA, chu kỳ nào (07-22 phụ đề ghi "MA600": `3gr71JlVqR8 · 00:27:00`); xác nhận bộ 34/89/200 là MA hay EMA.
- `GRWl0b0z1nk · 00:34:18` — bảng "Hyperliquid" 400–500k$ lệnh long là Hyblock Capital hay dữ liệu vị thế Hyperliquid; bố cục màn hình.
- `YMlDceykaTw · 00:22:22–00:22:53` — điểm neo Fibo mở rộng ("Fibo Eric" đảo chiều) cho ra 64.06 và trendline hội tụ.
- `UzjWDBAiahs · 00:09:20–00:11:25` — so khung lớn mùa trước: neo Fibo mở rộng ra 51/23k và vùng hỗ trợ 30k.
