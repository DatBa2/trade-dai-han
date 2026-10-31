# Nhóm 2 — FAM Trading, 03/02 → 16/03/2026 (20 buổi, file zip_clean)

Nguồn trích: `[YYYY-MM-DD hh:mm:ss]`. Ngày 13/03 có 2 buổi: **13a** = IbTz3V-KlKs (sáng), **13b** = gRyoN4cBXZA (tối).
"lặp N/20" = số buổi có nhắc (đếm bằng grep + đọc).

## 1. Bối cảnh giai đoạn
- BTC sập 79k (03/02) → 73k → 70k → râu ~59–60k đêm 05/02, đóng ~62–64k = chạm đích "mô hình cờ" khung ngày đã báo từ trước. Sau đó đi ngang 66–72k suốt Tết (nghỉ live 17–25/02), hồi 64→70k (26/02), 28/02 tin chiến tranh Mỹ–Iran đạp 65→62k rồi hồi lại, 05/03 chạm 74k, 09/03 về 65k, 13–16/03 lên lại 72–74k.
- F&G gần như suốt giai đoạn ở mức 5–15 (lên được 22 vào 05/03). Vàng 5000–5400, bạc 75–105, dầu từ 59 vọt lên 115–120 (09/03) rồi dump về 88. CPI về 2.4, FED họp 19/3.
- Người đó bận/bệnh nên live không đều; từ 02/03 thêm live **buổi tối** để trade cùng người xem (11/03, 13b, 16/03): "Buổi sáng thuần phân tích thị trường crypto và lên kế hoạch giao dịch" [2026-03-02 00:14:57].

## 2. Quy trình một buổi live
**Buổi sáng (~10h), thứ tự điển hình (15/20 buổi):**
1. Mở bằng các lệnh đang chạy hoặc vừa chốt (vàng/dầu/BTC), review plan hôm qua, đôi khi mắng người cháy tài khoản [02-04 00:03:32], [03-05 00:23:21].
2. "View lại thị trường" BTC **từ khung lớn xuống**: (nến tháng khi sang tháng mới) → nến tuần → nến ngày → H4 → H1/30' → M5: "phân tích lại từ đầu từ khung lớn, dài hạn cho đến ngắn hạn rồi khung nhỏ" [2026-03-02 00:44:26].
3. Lượt chỉ số cố định: DOM (BTC.D) → USDT.D → gap CME → DXY/vàng/bạc/dầu → ETH → F&G → liquid (Coinglass heatmap) → Hyblock/Hyperliquid (khối lượng long/short) → tin tức trong ngày. Ví dụ: [02-03 00:17:09–00:22:23].
4. Chốt "plan": vùng chờ long/short, đích, mốc làm view sai. Sau đó Q&A (spot, altcoin, P2P, luật) chiếm 40–60% thời lượng.
5. Kết buổi: "Nhớ view thị trường ngày hôm nay ở đoạn đầu" [2026-02-04 00:47:00], "xem lại 30 phút đầu tiên" [2026-03-06 00:56:48].

**Khác biệt giữa các buổi:**
- Hôm thị trường đứng: "đi lướt lại một vòng và đưa cho anh em một plan là xong. Còn lại… trả lời các câu hỏi" [2026-02-27 00:13:56]; đôi khi trả lời Q&A trước rồi mới phân tích [03-04].
- Thứ 2 (đầu tuần): xem nến tuần vừa đóng; "nến màu xanh của ngày thứ hai không mang ý nghĩa nhiều" [2026-03-03 00:18:38].
- Thứ 6: thêm câu hỏi altcoin có sóng cuối tuần không, né tin non farm/PPI [2026-03-06 00:02:50].
- Có tin chiến tranh: mở bằng dầu/vàng ~15' [03-09].
- **Buổi tối** = trade trực tiếp M5/M15, ưu tiên Zoom vì YouTube "lệch pha với lệnh vào" [2026-03-11 00:11:37]; kết bằng "Ngủ là cắt, ngủ là chốt" [2026-03-13 00:55:35 (13b)].

## 3. Công cụ, nguồn dữ liệu, chỉ báo
| Công cụ | Dùng làm gì · cách đọc | Trích |
|---|---|---|
| TradingView (nến, BTCUSDT Perp Binance; Bitstamp cho lịch sử) | Nền tảng chính; khung tháng cần tài khoản trả phí | [02-11 00:26:18], [03-02 00:15:31] |
| **Fibo** thoái lui + mở rộng (lặp 20/20) | Thoái lui 0.5/0.618 (đôi khi 0.786) để chọn entry; mở rộng 1.0/1.618 để đặt TP; được "lock" (ghim) lại trên chart | "Fibo mở rộng thì làm TP, còn Fibo thoái lui thì mới lấy để làm entry" [2026-03-05 00:39:09] |
| **MA 34/89/200** (MA34 14/20, MA200 15/20, MA89 10/20; chữ "EMA" 7/20) | Lọc hướng + đích hồi; dùng trên mọi khung (tháng → M5) | "Test 34 xong là nó lên đến 89. Qua 89 nó đến 200." [2026-02-03 00:15:05] |
| Nến + volume (20/20) | Nến OHLC, râu, cặp nến; volume đột biến xác nhận lực; chỉ báo volume tên "FX Can…" | "Nến là chắc chắn là khi nào cũng phải nhìn" [2026-02-03 00:14:33] |
| Trendline, cấu trúc đỉnh/đáy, mô hình (cờ, hai đáy, vai đầu vai, cốc tay cầm) | Hay tắt MA đi để vẽ trendline/đọc cấu trúc | "Khi vào H1, tắt MA đi" [2026-02-11 00:03:39] |
| Gap CME (20/20) | Đích dài hạn (80–81k, 93k, 20k); cách xem: "gõ BTC thêm số 1 vào trên TradingView" | [2026-02-03 00:33:48] |
| Coinglass Liquidation Heatmap (liquid 20/20) | Cụm thanh lý = nam châm giá / nơi chốt; tin ít khi thị trường thiếu thanh khoản | "Liquid tầm này là không quan trọng lắm" [2026-02-04 00:14:48] |
| Hyblock ("hai block") / Hyperliquid | Khối lượng long/short đang mở; phe nào đông thì giá đi quét phe đó | "Khi nào tụi này bị thanh lý hết thì khả năng là ok để short lại" [2026-02-04 00:16:56] |
| F&G (15/20) | Thước đo tâm lý: 5–10 → không short, mua lướt | "Fear and Greed về 9 điểm thì khá là đẹp" [2026-02-06 00:04:12] |
| BTC.D, USDT.D (14/20, 9/20) | BTC.D: có nên chơi altcoin không; USDT.D: tăng → BTC giảm | "Hai thằng DOM này anh em đừng quan tâm làm gì" [2026-02-04 00:13:43] vs "USDT.D… thủng khỏi vùng 7.5… BTC 80 là sure" [2026-03-13 00:26:14 (13a)] |
| Vàng/bạc/dầu, DXY, chứng khoán Mỹ | **Bộ lọc rủi ro**, không phải tín hiệu vào lệnh | "Mình không dùng nó làm indicator để vào lệnh mà là để kiểm soát rủi ro" [2026-03-04 00:48:54] |
| RSI (2/20) | Chỉ để nhìn lực; xét phân kỳ khi ở vùng >70 / <30 | [2026-03-13 00:50:08 (13a)] |
| Volume profile, ATR | Biết nhưng ít dùng; "3 4 năm rồi mình không cập nhật thêm chỉ báo mới" | [2026-03-13 01:20:53 (13b)] |
| Sàn | BingX (future, 7 năm), MT5 (vàng/dầu), Binance (xem volume BTC), Bybit; OKX/MEXC/Bitget | [2026-02-27 00:24:41], [03-13b 01:09:35] |
| Kênh phát | Livestream YouTube, nhóm VIP (lệnh cụ thể), Telegram (post nhanh), Zoom tối, Twitter để đọc tin | "trong nhóm mình ưu tiên những cái nào có sự tính toán" [2026-03-10 00:49:26] |

**Tin/không tin:** tin phân tích kỹ thuật ("Mình biết nhờ phân tích kỹ thuật thôi" [2026-02-26 00:36:29]); không tin có tương quan cố định giữa vàng và BTC [02-04 00:23:51]; không tin tin tức ("Số liệu nó không đánh lừa" [2026-03-04 01:05:50]); không tin mấy tên mẫu nến (doji…) [2026-03-06 00:33:36]; SMC không hợp, WCF chỉ dùng khung tuần/ngày [03-06 00:45:24].

## 4. Cách ra nhận định
- **Bộ khung kịch bản "nếu… thì…"**: "anh em sẽ nghe rất nhiều từ 'nếu' và 'thì'" [2026-02-26 00:38:02]; "Chúng ta chỉ biết nếu nó tăng thì sao, nếu nó giảm thì sao" [2026-02-27 00:37:51].
- **Xu hướng lớn ≠ sóng đang đánh** (Dow, lặp 8/20): "Sóng chính là giảm mà sóng phụ ở đây là sóng hồi" [2026-02-03 00:16:08] → được long sóng hồi nhưng vol nhỏ.
- **Giá xa MA → hồi về test MA**, không đánh đuổi (lặp ≥8 buổi): "giá có một nguyên tắc là nếu nằm xa MA quá thì nó sẽ hồi lên test MA" [2026-02-26 00:36:59].
- **Luật nến ngày**: "cây nến ngày màu gì thì ngày hôm nay chúng ta không nên đánh ngược" [2026-02-04 00:06:47].
- **Cần đa khung đồng thuận**: "khi một xu hướng này không được đồng thuận thì chúng ta bắt buộc phải chờ" [2026-03-06 00:07:41].
- **Có vùng không trade**: "vùng 70 cho đến 73… 3000 giá chết chóc" [2026-02-27 00:31:47]; "Muốn nhận định phải có dữ liệu… thiếu dữ liệu thì chúng ta cần phải chờ" [2026-02-26 00:21:25].
- **Mốc làm view sai = nến ĐÓNG CỬA**, không tính râu (lặp 15/20): "nến H4 nào đóng cửa, phải nhớ từ đóng cửa chứ không tính cái râu" [2026-03-04 00:29:51].
- **Xác suất nói bằng số**: rời MA34 chưa test 89 → "trên 80% nó sẽ lên 89" [02-06 00:31:44]; râu nến coin quay lại test ~50% [02-06 00:38:23]; H4 đóng qua 71 → "90%… lên 75" [03-04 00:06:08]; phá trendline → "khoảng 70% là sẽ win" [02-27 00:37:18].
- **Phân tích đám đông / ngược đám đông**: "Short tầm này thì khác nào hòa mình vào đám đông" [2026-02-03 00:21:51]; tàu long "tứ phương là đồng đội thì có vẻ là không ổn" [2026-03-13 00:29:20 (13a)].
- **Tin chỉ để kiểm tra lực**: tin xấu mà giá vẫn hồi → "lực mua giữ giá tốt… cá nhân mình không short nữa" [2026-03-02 00:37:58]; "giá nó chạy trước tin" [2026-03-10 00:51:35].
- **Đường đi nhiều chặng**: "lên 75 sau đó về tiếp 52… rồi từ từ nó về 23.000" [2026-03-02 01:01:05].

## 4b. BẢN ĐỒ CĂN CỨ CỦA CÁC CON SỐ (BTC trừ khi ghi khác)
| Ngày | Con số/vùng | Dùng làm gì | CĂN CỨ người đó nêu | Trích |
|---|---|---|---|---|
| 02-03 | 79k | Mốc điều kiện cho long | Cản bên trái (đỉnh H1), H1 phải đóng vượt để phá cấu trúc đỉnh/đáy thấp | "H1 đóng cao hơn 79.000" [00:10:21], [00:21:20] |
| 02-03 | 80–81k | Đích hồi tối thiểu | MA34 H4 chưa test + gap 79k6–81k + "trống thanh khoản" | [00:09:51], [00:11:23], [00:34:20] |
| 02-03 | 76–77k | Vùng chờ long | Fibo 0.618/0.5 + cụm liquid 76k "Khít với Fibo" | [00:20:48], [00:41:18] |
| 02-03 | 81/84 hoặc 82/85 | Đích nếu hồi mạnh | Fibo mở rộng H1/30', đo tùy điểm back | [00:12:25–00:12:57] |
| 02-03 | 90k | Trần "khó hơn lên trời" | Xu hướng tuần + ngày đã confirm giảm | [00:13:28] |
| 02-03→02-06 | 62–65k | Đích khung ngày | TP mô hình cờ trên D1 (báo từ vùng 95–96k) | "mô hình cờ về hai đó" [02-05 00:15:12]; [02-26 00:14:03] |
| 02-04 | 78–79k | Đích hồi H1 | H1 test MA34 → tiếp MA89 H1 | [00:07:49] |
| 02-04 | 85k | Vùng short đẹp nhất | Fibo kéo lên 85 + lấp hết gap 81–84 | [00:12:09] |
| 02-04 | 78c8 → 79k2 → 81 | TP từng phần | Fibo, rồi cản H4, rồi các cản tiếp theo | [00:41:58] |
| 02-05 | 76k | Đích nhịp hồi kế tiếp | MA89 H1 (MA34 H1 chưa test 89 lần nào) | [00:09:40–00:10:14] |
| 02-05 | 69k | Có thể quét về rồi hồi | MA200 | [00:03:22] |
| 02-05 | 56k | Bác bỏ | "không có cơ sở" | [00:03:22] |
| 02-05 | −10% (BTC), −15–20% (ETH), −20% (alt) | Limit bắt râu spot, reset mỗi ngày | Biên độ % của nhịp vừa chạy | [00:17:22–00:18:31] |
| 02-06 | 60k | Không đặt SL | Số tròn → bị quét (đã quét 59k) | [00:10:12] |
| 02-06 | 53k | Bác bỏ | Tâm lý đám đông đã cực bi quan | [00:12:21] |
| 02-11 | 66k → 64k | Vùng long | Fibo 0.5 | [00:04:40] |
| 02-11 | >72k (vd 75) | Chờ để short | Cú quét SL của phe short + râu/cặp nến đảo chiều, hay xảy ra ở phiên Mỹ | [00:05:43–00:06:48] |
| 02-11 | 67k, 66k | Có thể bị quét trước khi bật | Liquid nhỏ 67k + heatmap "lệch volume" | [00:13:12], [00:17:56] |
| 02-16 | 80–84k | Trần nhịp hồi, "tìm đường mà té" | Râu nến tuần 80k + gap | [00:14:32] |
| 02-16 | 65k | Nến tuần tốt | Đã test lại râu/Fibo của râu tuần; giá trên MA200 tuần | [00:12:52] |
| 02-16 | 71k → 75 → 80 | Break lên | Đỉnh bằng 71 + đáy cao dần (H4) | [00:16:12–00:16:44] |
| 02-16 | 68k / 66k | Entry long | Trendline 1 + Fibo 0.5 (68k); trendline 2 (66k) | [00:17:16] |
| 02-16 | 65k | SL bắt buộc | Đáy giữ cấu trúc | [00:17:46] |
| 02-16 | <60 / >75 | Mốc phải view lại | Biên kế hoạch | [00:26:41] |
| 02-26 | 70–73k | Đích hồi | 73 = MA200 H4; vượt MA89 → "đi tiếp MA200" | [00:19:51], [00:38:34] |
| 02-26 | 72–74k | Vùng đứng ngoài; D1 đóng >74/75 → 82–83 | Vùng tranh chấp; trên đó là lấp gap | [00:20:22–00:20:54] |
| 02-26 | 59 → 55k | Thủng thì đánh xuống | Không nêu thêm | [00:14:35] |
| 02-26 | ~60k | Đích khung tuần | Vai đầu vai: biên từ đỉnh đến neckline | [00:31:19–00:31:50] |
| 02-26 | 60–80k (~3 tháng) | Vùng đi lòng vòng | Hỗ trợ cứng + thanh khoản lịch sử, so với 10/2022–4/2023 | [00:32:22–00:33:22] |
| 02-26 | 40→20k | Vùng mua spot | Gap 20k | [00:30:49] |
| 02-26 | 69k | Chốt scalp | Liquid nhỏ + test râu | [00:44:19], [00:39:39] |
| 02-27 | 66/65k | Limit long | Fibo 0.5 + hỗ trợ nến bên trái | [00:29:34] |
| 02-27 | 64k | Mốc sai (H4 đóng dưới → thoát hết long) | Đáy của nhịp tăng | [00:30:41] |
| 02-27 | 68k | Nhịp tăng vừa rồi = kill SL short + test MA | SL short trên H4 6800 + MA89 H4 trùng MA34 | [00:31:12] |
| 02-27 | 69k / 70k | TP long | Mô hình hai đáy kẹp MA34–89 trên H1 | [00:33:58] |
| 02-27 | 74k | Đích nếu phá trendline | Cờ 30' + cờ H1 | [00:36:14] |
| 03-02 | 74k ("làm tròn 75") | Kháng cự trung/dài hạn | MA34 khung tháng (lần đầu gãy) | [00:16:02] |
| 03-02 | 62k | Nến tuần đẹp | Râu tuần test lại râu cũ | [00:22:05] |
| 03-02 | 70.500 | Cản D1 / TP2 | "điểm chốt của hai cây nến ngày" (đóng cửa) + Fibo mở rộng đo 2 lần đều ra 70.5 | [00:25:20], [00:28:42] |
| 03-02 | 71k | Tệ nhất cũng lên tới | Chưa test MA34 D1 | [00:24:17] |
| 03-02 | 61k | SL nếu đánh khung ngày | Đáy D1; tính ra −75,6% ở x10, RR < 1:1 | [00:30:48–00:31:53] |
| 03-02 | 75 → 52 → 23k | Đường đi dài hạn | Fibo mở rộng khung tuần | [01:00:34–01:01:05] |
| 03-02 | 20k ±1000 | Đáy dự đoán | Gap 20k + mức giảm 80% | [00:58:28–00:59:30] |
| 03-03 | Entry 68.800 / SL 68.500 | Scalp M15 | Fibo + MA34 15' + hai đáy + hỗ trợ (đường vàng) | [00:09:00–00:10:32] |
| 03-03 | 70.5k & 75k | Đích tuần | Fibo mở rộng 1.0/1.618 được ghim; 2 lần đo hội tụ ở 70k | [00:23:17–00:24:18] |
| 03-03 | 70k | Đích đạt | Target mô hình cờ | [00:22:15] |
| 03-03 | 67–66k | Entry nếu điều chỉnh | Fibo 0.618 H1 + vùng trống thanh khoản | [00:21:13–00:21:44] |
| 03-03 | 66k (H4) → 50–52 | Mốc sai của sóng hồi | H4 đóng dưới MA34 → xác nhận cờ D1 | [00:28:39–00:30:11] |
| 03-03 | 70.500 | Đích + chỗ SL short | Liquid heatmap + Fibo "hội tụ rất nhiều anh tài" | [00:31:44] |
| 03-04 | 71k → 75k | Nếu H4 đóng xuyên 71 thì 90% lên 75 | Vùng nén lâu | [00:06:08] |
| 03-04 | 66k | Điều chỉnh về đâu | Vùng trống thanh khoản → về base; lịch sử test Fibo 0.5/0.618 | [00:14:38–00:15:10] |
| 03-04 | 67k / 66.5k | Mốc thoát long | H4 đóng dưới MA34 (~67k) / H1 đóng dưới 66.5 | [00:29:51], [00:32:38] |
| 03-05 | 75k; 73/78 | TP | Fibo mở rộng nhịp lớn (1.618 = 75) và nhịp nhỏ (70/73/78) | [00:35:18–00:35:52] |
| 03-05 | 74k | Kháng cự gần nhất | Đỉnh bên trái; dưới đó là trống thanh khoản | [00:35:52] |
| 03-05 | 78–79.8k | Cản xa | Fibo 0.5 thoái lui của cả nhịp giảm | [00:36:26], [00:37:00] |
| 03-05 | 80k / 85k | Có thể lên | MA89 D1 / MA200 D1 kéo xuống theo thời gian | [00:39:43–00:40:18] |
| 03-05 | 70.002–70.003 | Không đặt SL | Đó là SL của số đông | [00:50:13] |
| 03-06 | 70–71k | Hỗ trợ (cấm short) | Cụm râu dưới | [00:08:47] |
| 03-06 | 69k | Limit bắt râu | Trendline H1 + râu | [00:15:45] |
| 03-06 | 67k | "end game" | Đáy cấu trúc | [00:21:07] |
| 03-09 | 70/72k | Chờ để short | Test lại râu nến tuần | [00:28:38] |
| 03-09 | 64k / SL 62k | Entry an toàn (≈5R) vs market (RR 1.6) | Đáy, liquid 65k mới tạo | [00:36:40–00:37:48] |
| 03-09 | 68k | Đích scalp | MA89 30' (đã quay lại 89 rất nhanh) | [00:34:29] |
| 03-10 | 79.7k / 88k | Đích sóng lớn | Fibo mở rộng (thoái lui đáy 60–62 → đỉnh 74 → 65) trùng MA89 D1 / MA200 D1 | [00:30:28–00:31:01] |
| 03-10 | 75–78k, 84–88k | Vùng đích | Đo nhiều sóng (75/82, 77/84) → gộp thành vùng | [00:31:33–00:32:44] |
| 03-10 | 69k3–68k | Chờ nến để long (không limit) | Hỗ trợ 30' + liquid 68k + Fibo 68–67k4 + MA89 6800 | [00:37:03], [00:56:35], [00:57:08] |
| 03-11 | SL 69k / TP 72k | Scalp đêm | Hyblock: long mới mở 69k; 72k có lệnh mở dài | [00:20:18] |
| 03-11 | 74k | Đích cốc tay cầm H1 | Mô hình | [01:14:14] |
| 03-12 | 65.2k SL; break 71 → 75/78/80 | Long tại trendline | Trendline + đỉnh cao hơn | [00:24:07–00:27:17] |
| 03-12 | Short 78.5–84k, SL 90–92k, TP 53–54k | Kế hoạch swing (R:R 1:4) | Râu có thể quét tới 85 theo thanh khoản; vùng 92 "mới cắt" | [00:28:51–00:30:28] |
| 03-13a | 74.5 / 78 / 80k | TP (78 yếu nhất) | 74.5 = "kháng cự khá là chắc" | [00:24:43] |
| 03-13a | 70k | H4 đóng trên → long | Vùng break sideway 66–70 | [00:21:38] |
| 03-13a | 70 / 69 / 68k | Vùng quan sát, cấm limit | Dải SL long 69.7–68.8 trên heatmap | [00:27:47–00:28:17] |
| 03-13a | 71.600 | Đóng trên → thoát short | Fibo | [01:12:06] |
| 03-13b | 71k1 / 70k1–70k3 | TP short | Đáy M5 + Fibo mở rộng 70k1; volume profile 70k3 = "hỗ trợ cứng" | [00:57:14], [01:07:25] |
| 03-13b | 65k (68–69k) | Hết trend tăng | Đáy cấu trúc | [01:04:39] |
| 03-16 | 74k → 71k6 | Short nếu rụng | Fibo 0.618 M15 | [00:39:58] |
| 03-16 | 71–71.8k / 69k | Điều chỉnh đẹp / đứt sóng | Gap 71 "lấp gap… đủ về mặt kỹ thuật" | [00:46:18] |
| Vàng | 5130; 5440; 5350–5400 (sell); 4800/4600 | Đích/sell/TP | Fibo 0.6; Fibo; "vàng nó hay chạy lên Fibo 618"; Fibo mở rộng | [02-04 00:01:01], [03-02 00:11:45], [03-11 00:56:55], [03-13a 00:35:01] |
| Dầu | 59 mua, DCA tới 45; chốt 104–105; dự báo 150–200 | Kế hoạch dài | Hai đáy/backtest 2 lần trên biểu đồ tháng; đỉnh cũ 125; so với vàng 2022 | [03-05 01:06:20], [03-09 00:12:39], [03-11 01:03:24] |
| BNB | 630 (SL 605) → 700–725; 666 | Entry/TP | Fibo 0.618; MA200 + đỉnh bên trái | [03-13a 00:07:02], [03-06 00:22:42] |

**Người đó CHỌN HƯỚNG thế nào** (thứ tự hay dùng nhất):
1. Xu hướng khung lớn: giá nằm trên hay dưới MA khung ngày/tuần/tháng; màu nến ngày hôm trước [02-04 00:06:47].
2. Cấu trúc đỉnh/đáy H4: phá đỉnh cũ bên trái = đổi cấu trúc → "tầm này mình không short nữa" [2026-02-26 00:39:05].
3. Vị trí so với MA34/89 trên khung đang đánh: "giá nằm trên MA34 và trên 89 thì chúng ta không có short. Mà giá nằm dưới chúng ta không có long" [2026-03-12 00:25:11].
4. Khoảng cách giá–MA: xa MA → cấm đánh đuổi, chờ hồi về MA.
5. Bộ lọc phụ: đám đông (Hyblock/Hyperliquid, F&G thấp → không short), vàng/dầu/USDT.D (vàng tăng → "khoan lại"), phản ứng của giá sau tin.

**Người đó CHỌN VÙNG VỀ/ĐÍCH thế nào:**
- Entry = Fibo thoái lui 0.5/0.618 (đôi khi 0.786) kéo trên nhịp vừa chạy, "Đáy là điểm thấp nhất, đỉnh là điểm cao nhất của cái nhịp này" [2026-03-10 00:29:25]; rồi tìm thứ trùng với nó: hỗ trợ nến bên trái/râu cũ, trendline, MA, cụm thanh lý, vùng trống thanh khoản (giá về lại "base").
- Đích = Fibo mở rộng 1.0/1.618 đo trên nhiều nhịp → lấy chỗ trùng, cộng MA khung lớn, gap, râu/đỉnh cũ, target mô hình.
- Hội tụ: "Cái điểm nào nó giao hợp nhiều cái chỉ báo thì cái chỗ đó nó càng có giá trị" [2026-03-10 00:31:01]. Thực tế người đó tin khi có **≥2 căn cứ trùng**: 2 lần đo Fibo (70.5k), Fibo + liquid (76k, 70.5k), Fibo + MA D1 (79.7/88k), Fibo + trendline (68k), Fibo + gap (85k).
- Luôn nói **vùng, không phải điểm**: "các cái công cụ nó chỉ hỗ trợ chúng ta đến một cái mức độ tương đối" [2026-03-10 00:32:07]; né số tròn khi đặt SL.
- Thứ tự ưu tiên căn cứ: **Fibo** (có trong 20/20 buổi) ≈ **MA** (vừa lọc hướng vừa làm đích) > đỉnh/đáy/râu cũ và trendline > gap (đích xa, "phải qua được gap 81 thì mới view lên tiếp 93" [03-02 00:34:09]) > liquid/Hyblock (căn cứ phụ, hay nói "không quan trọng lắm"; cụm thanh lý mới tạo thì "chỉ dùng để làm plan" [03-09 00:38:23]) > F&G/DOM (dùng cho bối cảnh).

## 5. Vào lệnh, quản lý lệnh và vốn
- **Chờ xác nhận**: "long thì phải vào sau… cây có volume đột biến" [2026-02-26 00:16:42]; scalp cần "cây volume lớn nhảy vào… lực xả này phải bị triệt tiêu… Kết hợp giữa 30 phút với 5 phút" [2026-03-05 00:41:27–00:42:00]; "M5 rút chân kèm khối lượng" [02-03 00:45:15].
- **Limit hay chờ nến**: chỉ limit khi vùng có hội tụ; khi có nhiều cụm thanh lý thì "chúng ta không nên limit… chỉ note ra một vài các cái vùng giá" [2026-03-13 00:27:47 (13a)]; limit không khớp thì "hủy thôi" [03-10 01:06:29]; "đừng có limit short với những cái khung lớn" [03-10 00:34:15].
- **SL/TP đặt trước**: "khi vào lệnh thì phải có stop loss và TP trước đó rồi" [2026-02-04 00:42:38]; SL theo lý do vào lệnh: "tùy theo lý do vào lệnh là gì thì… thoát lệnh theo cái đó" [2026-03-04 00:37:40].
- **Né SL bị quét**: lấy điểm SL làm entry 2, chia vol 30–50% / 50% [2026-03-13 00:46:38 (13b)].
- **Chốt từng phần + kéo SL về entry**: chốt 50% → 20% → giữ 30% [2026-02-27 01:01:20]; lãi ~500 giá thì kéo SL về entry [03-06 00:16:16]; "Ai chưa TP thì nhớ kéo SL về entry, đừng tham từ dương thành âm" [2026-03-05 00:27:07].
- **Đòn bẩy theo biên độ**: "biên này nhân cho đòn bảy… không quá 60%" (biên 1–2% → x25–30, 4–5% → x10–15) [2026-02-26 00:57:37]; BTC thường x10; ngược xu hướng thì "đòn bẩy thấp volume nhỏ", isolate, không cross [02-04 00:11:35], [03-03 00:36:28].
- **Kiểm tra R:R trước khi vào** (03-02, 03-09, 03-12): ví dụ không vào market vì RR 1.6, chờ 64k để có ~5R [2026-03-09 00:36:40].
- **Kẹt lệnh**: "Hòa vốn là chắc chắn phải cắt" [2026-02-05 00:11:17]; đưa tài khoản về 0 rồi mới làm lại [02-26 00:23:01].
- **Không giữ lệnh qua đêm** khi scalp/vàng/dầu: "vào lệnh khi ngồi cầm chart và thoát lệnh khi hết cầm chart" [2026-03-13 00:55:35 (13b)].
- **Hệ thống 4/5 điều kiện**: "có năm điều kiện để vào lệnh. Nó đáp ứng được 4/5 là đã đủ" [2026-03-11 00:51:13].
- **Spot/DCA**: gom xuống, không gom lên [02-11 00:20:09]; kế hoạch 100k USD cho vùng 50→20k: 60% chia đều mua mỗi ngày, 40% để dành cho ngày sập 5–10% (mua gấp 10 lần) [2026-03-12 00:08:33–00:11:10]; hold không quá 20% vốn ở giá hiện tại [03-02 00:54:33]; bán đỉnh = bán dần theo vùng [03-16 00:36:16].
- **Đánh tin**: né giờ tin (phiên Mỹ 7:30–8:30 tối) (lặp 11/20); trade theo tin "hết tin là phải té" [03-04 01:01:01].

## 6. Thiên hướng lớn và cách thay đổi
- **Dài hạn không đổi**: 2026 là năm downtrend; BTC về 40→20k ("Kế hoạch của mình là mình mua từ 40 cho đến 20" [2026-02-26 00:29:16]); mua đẹp khoảng 2027–2028, tăng 2028–2029 [03-10 01:07:03]; gom lại "cuối quý ba" [03-04 01:08:21]; "2026 là một năm xấu mọi mặt" [03-02 00:41:48].
- **Ngắn hạn đổi 2 lần**: (1) 03–05/02 giữ view "không long, chờ hồi mới short" → 06/02 chạm 62k thì chuyển "đừng có short nữa… mua lướt" [2026-02-06 00:14:29]; (2) từ 26/02 nghiêng hẳn về long sóng hồi: H4 đổi cấu trúc + giá giữ được sau tin chiến tranh [02-26 00:39:05], [03-02 00:37:58]; đến 12–16/03 vẫn "Quan điểm của mình thì mình vẫn bullish cái đoạn này" [2026-03-12 00:24:40] nhưng nhắc đó chỉ là "hồi kỹ thuật".
- Vàng: từ "đừng short" (02-26, 03-02) chuyển sang "tập trung mình sell dần" [2026-03-13 00:34:00 (13a)]. Dầu: luôn "đừng có đi sell dầu" [03-11 01:03:24].

## 7. Đúng/sai nổi bật và cách phản ứng
- **Hay nhắc lại cái đúng**: đích cờ 62k báo từ 95–96k, "Lệch 500 giá" [2026-02-06 00:06:57], [02-26 00:35:27]; dầu mua từ 59 chốt 104–105 [03-09 00:12:39]; vàng chốt 5408 rồi giá sập [03-03 00:33:18]; giữ 10% lệnh short 124k [03-04 00:57:36].
- **Sai/thua thì nói thẳng, nhẹ nhàng**: "SL rồi không sao" [02-03 00:01:48]; "Lại bị tụi này nó lừa rồi. Nó quét về đúng cái điểm SL của mình" [2026-02-05 00:32:33]; hôm 16/03 nói "hôm nay livestream mất 1 triệu mấy" [00:53:04]; limit hụt 200 giá [03-10 01:05:22].
- Có lúc đổ cho "tụi này"/MM quét SL, cho Trump làm giá, nhưng không đổ lỗi cho tin tức. Khi có người nói "BTC sai hướng" thì cãi lại bằng lịch sử test Fibo [2026-03-04 00:14:38].

## 8. Giọng nói
- Xưng "mình", gọi "anh em / các bạn / các ông"; tự gọi "Eric"; nói nhanh, hay dùng ẩn dụ: đi săn chờ con mồi [03-06 00:27:01], đồn trú phe đỏ [03-02 00:25:54], đặt 20 cái bẫy ("kèo 1%") [03-06 00:55:13], tàu đông đồng đội [03-13a 00:29:51].
- Câu cửa miệng: "hồi quang phản chiếu", "xổ số", "té/cút/húp/lụm", "đừng có FOMO", "chờ" ("Mình nói rất nhiều đến chữ chờ" [02-26 00:15:40]), "Thà… ở ngoài nhìn chảy nước miếng còn hơn lau nước mắt" [02-03 00:21:51].
- Rất dứt khoát với điều cấm ("tuyệt đối không short"), nhưng khi bị hỏi đoán giá thì từ chối: "Mình đâu phải thầy bói" [02-26 00:25:35]; câu miễn trừ: "anh em đừng tin ai hết" [03-16 00:47:52].

## 9. Tinh hoa (8 nguyên tắc)
1. Chỉ cần Fibo + MA + nến + cấu trúc: "Fibo, MA, nến, cấu trúc sóng, cấu trúc thị trường… xài thoải mái là đủ ăn" [2026-03-05 00:36:26].
2. Trên MA34/89 thì không short, dưới thì không long; giá xa MA thì chờ nó hồi về MA [2026-03-12 00:25:11], [02-03 00:15:05].
3. Fibo thoái lui để vào, Fibo mở rộng để chốt; vùng nào hội tụ nhiều căn cứ thì đáng tin [2026-03-05 00:39:09], [03-10 00:31:01].
4. Mốc làm view sai là nến đóng cửa của khung đang đánh, không tính râu [2026-03-04 00:29:51].
5. Trade theo rủi ro chứ không theo lợi nhuận: "Đừng có đánh theo lợi nhuận… luôn trading theo rủi ro" [2026-03-03 00:03:50]; "hệ thống… luôn xoay quanh việc kiểm soát cái mất" [03-05 00:38:36].
6. Có vùng không được trade, có lúc phải chờ: "không phải vùng nào chúng ta cũng đánh được" [2026-02-26 00:21:25].
7. Đi ngược đám đông và phe đang đông lệnh: "cái tàu nào mà đông thành viên… không có ổn lắm" [2026-03-13 00:29:51 (13a)]; "Thị trường hoảng sợ chúng ta mua, thị trường FOMO chúng ta bán" [02-06 00:13:58].
8. Mọi thứ là kịch bản, không phải dự đoán: "Chúng ta chỉ dự tính các trường hợp xảy ra và lên kế hoạch thôi" [2026-02-27 00:46:46].

## 10. Khung hình cần xem (tối đa 4)
- `pbr4y9qP1Ys · 00:50:45` — tên thật và cài đặt của chỉ báo volume ("FX Can dưới volume").
- `7zFMbvqo3QI · 00:44:50–00:45:25` — giao diện Coinglass heatmap (bảng màu mới) và Hyblock ("Liquid hai block"): cột/khối lượng long-short họ đọc.
- `TXnTpUkc78s · 00:29:56–00:31:01` — Fibo thoái lui/mở rộng kéo từ điểm nào tới điểm nào; MA89/MA200 D1 nằm ở đâu.
- `4Z73-L_oWNY · 00:07:41` — trên H4, bộ 34/89/200 là MA hay EMA ("cụm EMA cắt qua nhau"); trong lời nói hai chữ này dùng lẫn lộn.
