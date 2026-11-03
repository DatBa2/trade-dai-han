> Lọc theo T = 2026-11-03 11:00 (giờ VN); bỏ 7 dòng có ngày ≥ T (mọi mốc ≥ 2026-11-03; dòng kết quả "Đo:" tính thêm 30 ngày; dòng không ngày mà có mức giá chỉ xuất hiện từ T trở đi cũng bỏ). Ví dụ còn lại đều trước T — không mở bản gốc.

# SỔ TAY BOT V5 — Phần 3: ĐO / VẼ VÙNG → CHỖ VÀO, CHỖ TRÁNH

> **Số buổi đã dùng**: nhãn v5 `hoc_v5/nhan` = **180/180 buổi** · mốc `moc/*.json` = **180/180 buổi** (3.362 mốc BTC, bỏ 6 mốc `tai_san` ≠ BTC / chưa rõ) · ảnh `so_tay/khung/` + `so_tay/ghi_chu/hinh_anh_1..4.md` · số liệu `so_tay/SO_LIEU_CAN_CU.md`. **Cập nhật: 31/10/2026 12:40.**
> **Quy ước**: "giá" = 1 USD giá BTC. `[MM-DD hh:mm:ss]` = ngày 2026 + giờ trong video, bấm vào là mở đúng giây. «…» = nguyên lời người đó (phụ đề có thể sai chính tả). **Đo:** = số đo được từ nhãn/mốc/giá OKX 1H (`du_lieu/btc_1H.csv`), không phải lời người đó.
> **Nguyên tắc phần này**: chỉ ghi điều người đó NÓI hoặc LÀM (đo được). Không có luật, ngưỡng hay đề xuất của người viết. Chỗ nào người đó không nói thì ghi "không nói".
> Mỗi case: **Tình huống → Đo/vẽ gì → Con số + vùng (độ rộng thật) → Vào / tránh / chờ → Tần suất → Ví dụ thật.**

---

## 0. Một bảng tóm tắt

| Câu hỏi | Trả lời (nguồn ở mục tương ứng) |
|---|---|
| Vùng của người đó rộng bao nhiêu? | **Phần lớn chỉ nói 1 số** ("vùng 91"): 59–75% mốc vào/TP/hỗ trợ/kháng cự là 1 số. "Vùng 82" = «loanh quanh cứ cái đầu 82» (81.900 … 82.550). Khi nói 2 mép: **trung vị 1.000 giá (~1,3%)** cho vào/TP/hỗ trợ/kháng cự; đích D1 ~1.650, W1 ~3.000 (mục B). |
| Đo bằng gì? | Fibo thoái lui (vào), Fibo mở rộng 3 điểm (TP), EMA 34/89/200/610 nhiều khung, đỉnh/đáy/râu cũ + vùng cản cũ đổi vai, vùng sideway cũ; vùng tin khi **hội tụ** (mục A). |
| Vào ở đâu? | Thuận view: chờ giá **hồi về** vùng hội tụ (Đo: vùng vào cách giá lúc nói trung vị **1.500 giá**), chờ nến ở vùng, vào lệnh chia nhiều entry; hoặc phá + test lại (mục C). |
| Tránh ở đâu? | Vào khi giá chưa tới vùng / ở giữa; FOMO đuổi; short ngay hỗ trợ – long ngay kháng cự; vùng sẽ bị quét; ngược khung lớn; quanh tin / thứ Hai (mục D). |
| Đường đi | 109/180 buổi vẽ chặng 1 **ngược** chặng 2 (quét rồi mới đi); râu chưa test → về test (mục E). |

---

## A. CÁCH ĐO TỪNG CÔNG CỤ ĐỂ RA CON SỐ

### A1. Fibo thoái lui → vùng VÀO
- **Tình huống**: giá vừa chạy xong một nhịp (lên hoặc xuống) và đang hồi; cần chỗ vào thuận nhịp vừa chạy.
- **Đo/vẽ gì**
  - Kéo từ **đầu nhịp (mức 1) → cực trị mới nhất (mức 0)**, neo **râu**: «Đáy là điểm thấp nhất, đỉnh là điểm cao nhất của cái nhịp này chứ không phải cái điểm 70.000 hay 72.000» [03-10 00:29:56](https://www.youtube.com/watch?v=TXnTpUkc78s&t=1796s). Ảnh: 6/6 lần thấy công cụ đều mức 1 = đầu nhịp, mức 0 = cuối nhịp, neo râu, nhịp gần nhất trên khung đang mở (`hinh_anh_4.md` mục b).
  - Mức hiện: 0 / 0.236 / 0.382 / **0.5** / **0.618** / 0.786 / 1. «Mình hay follow theo đường 0.5 nên để 0.5 một màu khác…, 0.618 cũng màu khác» [09-18 00:12:43](https://www.youtube.com/watch?v=YPMgjMxL2io&t=763s).
  - Fibo sóng lớn được **ghim** thành đường ngang cam: «đo từ vùng 97 về đến vùng sâu nhất… là 59.800. Thì đây sẽ là Fibo 0.618» [05-11 00:15:01](https://www.youtube.com/watch?v=jm7VS-lKW8w&t=901s) (ảnh: 0.5 = 78.799,6; 0.618 = 83.417,9).
  - Sau nhiều lần dùng thì không vẽ nữa: >12 lần nói mức Fibo mà màn hình không có Fibo (`hinh_anh_4.md` mục b).
- **Con số + vùng**: vùng = khoảng **0.5 ↔ 0.618** của nhịp. Ví dụ 02/10 H4: 0.5 = 84.944, 0.618 = 85.520 → hộp vẽ **85,0–85,5k (~550 giá)**.
- **Vào / tránh / chờ**
  - Vai: «Fibo mở rộng thì làm TP, còn Fibo thoái lui thì mới lấy để làm entry» [03-05 00:39:09](https://www.youtube.com/watch?v=pbr4y9qP1Ys&t=2349s).
  - Fibo một mình thì không tin: «Fibo này thì mình không đánh giá cao lắm… nó về hỗ trợ này chẳng qua là nó hội tụ nhiều hỗ trợ thôi» [01-08 00:20:00](https://www.youtube.com/watch?v=jX-0Hgy1S0E&t=1200s).
  - Về vùng Fibo thì **chờ nến, không limit**: «Cái vùng 69k3 và 68k là các bạn nên chờ nến chứ không có nên limit» [03-10 00:39:47](https://www.youtube.com/watch?v=TXnTpUkc78s&t=2387s).
  - Giá đang kẹt ở mức Fibo, chưa rõ → đứng ngoài: «nó lên gặp ngay Fibo này nó khựng lại thì vùng này là vùng chúng ta không nên giao dịch» [04-21 00:19:09](https://www.youtube.com/watch?v=AG126RfNCk4&t=1149s).
- **Tần suất**: có trong `cach_lam` 143/180 buổi. Mốc có căn cứ Fibo: 549/3.349 (16%) (`SO_LIEU_CAN_CU.md`).
- **Ví dụ**
  1. **03-23/24, D1 59k → 76k, 0.5 = 67–68k**: «từ vùng 59.000 lên đến điểm cao nhất là 76.000, vùng hiện tại 68.000 này đang là Fibo 0.5» [03-23 00:42:55](https://www.youtube.com/watch?v=bSnFyHqyo5c&t=2575s); «Fibo 0.5 ở 67.00, và giá chạm đúng vùng này rất đẹp» [03-24 00:21:53](https://www.youtube.com/watch?v=xKTPieljFuY&t=1313s). **Đo:** râu thấp nhất 65.000 (29/03, quá mép ~2.000), sau đó 73.130 (09/04) và 79.462 (22/04).
  2. **10-02, H4 87.384 → 82.504**: hộp 85,0–85,5k giữa 0.5 và 0.618 + cản đỉnh cũ: «H4 đóng trên 85 là có sự confirm bởi vì nó qua được cái vùng Fibo 0.5» [10-02 00:11:43](https://www.youtube.com/watch?v=AxRfx12h9Z0&t=703s) (ảnh `AxRfx12h9Z0_001230.jpg`).
  3. **04-01, "công thức Fibo Eric" D1**: «nó đi lên lại trên vùng 0.5 này, đã về test 0.618 và đi lên lại… Nếu bây giờ anh em muốn swing thì cứ chia giải ra. 91 81 vậy thôi» [04-01 00:31:02](https://www.youtube.com/watch?v=Be-e74Mwx0U&t=1862s).

### A2. Fibo mở rộng 3 điểm ("Fibo Eric") → TP / ĐÍCH
- **Tình huống**: đã có nhịp + điểm hồi; cần chỗ chốt.
- **Đo/vẽ gì**: Trend-Based Fib Extension, 3 điểm **râu**: A đầu nhịp → B cuối nhịp → C điểm hồi; mức **1 = TP1, 1.618 = TP2** (ảnh 08/06, 27/07, 18/08 — `hinh_anh_3.md`, `hinh_anh_4.md`).
  - «62 này, hồi lên 69.9 sau đó điều chỉnh về lại 62… Fibo 1.618 cho kết quả ở 75.000» [03-17 00:17:59](https://www.youtube.com/watch?v=UKs5T1J0H9w&t=1079s).
  - «Từ đáy điểm đầu tiên là 59.000. Kéo lên đây là 64.000. Điểm hồi về lại là 60.000… Vùng Fibo 1.618 nó lại cho kết quả… 69.000» [06-12 00:22:47](https://www.youtube.com/watch?v=x75V4Kb1fj4&t=1367s).
  - Đo nhiều nhịp rồi gộp: «Nó lên đến 75 và 82… lấy cái điểm sau này… 77 và 84… Thì chúng ta kết hợp lại» → vùng 75–78 và 84–88 [03-10 00:31:33](https://www.youtube.com/watch?v=TXnTpUkc78s&t=1893s).
  - Khung lớn thì không tin: «Fibo extension nếu các bạn áp dụng ở trên những khung lớn quá thì không chính xác» [08-05 00:58:05](https://www.youtube.com/watch?v=uw4QcusFtBc&t=3485s).
- **Con số + vùng**: hộp quanh mức (ví dụ «một vùng ở 98.000, tức range trải dài từ 96 đến 100» [01-14 00:13:13](https://www.youtube.com/watch?v=2ZyVfVN3n4Y&t=793s), 4.000 giá ở D1). TP thực tế **non** hơn mức: «về khớp đúng TP1 tức là 62.468… biên độ dao động… khoảng 150 đến 200 giá» [08-04 00:14:31](https://www.youtube.com/watch?v=K6QkKY6Og7o&t=871s).
- **Vào / tránh / chờ**: là chỗ **ra**, không phải chỗ vào (xem A1). Mẫu đường đi: «lên Fibo 1 gãy về 0.5, test lên lại đúng Fibo 2 rồi gãy» [04-10 00:08:39](https://www.youtube.com/watch?v=u6rbQNQWJAE&t=519s).
- **Tần suất**: `cach_lam` 78/180 buổi.
- **Ví dụ**: (1) 03-17 vẽ lại H4 62 → 69,9 → 62 ⇒ 1.618 = 75k, dùng làm điểm thoát; **Đo:** OKX đỉnh 76.012 lúc 08:00 VN 17/03 (trước giờ live — họ đang giải thích lại nhịp vừa chạy). (2) 06-12 → TP1 65,9k: **Đo:** 15/06 đỉnh 67.300 (đạt); TP2 69k không tới, 24/06 về 59.107. (3) 08-18 H4: A 62.52 → B 63.39 → C 62.69 ⇒ 1.618 = **64.113,7**, giá chạm (ảnh `_c0_SERWnz0_002130.jpg`).

### A3. EMA (bộ Sonic R) nhiều khung → hỗ trợ / kháng cự / đích kế tiếp
- **Tình huống**: cần biết giá sẽ dừng ở đâu trên đường hồi hoặc đường đi tiếp.
- **Đo/vẽ gì**
  - EMA 34 (vàng + dải xám = EMA34 của high/low), 89 (xanh dương), 200 (tím), 610 (xanh ngọc) — ảnh + bài ghim Discord (`SO_TAY_TINH_HOA.md` D3, D4). Đo: "MA34" khớp **mép dải EMA34 gần giá** (H4 lệch 0,36%, H1 0,28%) (`SO_LIEU_CAN_CU.md` §3).
  - Cộng nhiều khung vào một số: «MA89 ở trên khung H1 hoặc MA200 ở trên khung 30 phút hoặc MA34 ở trên khung H4. Cái vùng này là cái vùng hỗ trợ tốt thì mới chờ được» [01-06 00:13:00](https://www.youtube.com/watch?v=aQbHs7J80jc&t=780s).
  - Thứ tự test: «Test 34 xong là nó lên đến 89. Qua 89 nó đến 200» [02-03 00:15:05](https://www.youtube.com/watch?v=ewRoIMVREvw&t=905s); rời MA34 mà chưa test 89 «trên 80% nó sẽ lên 89» [02-06 00:31:44](https://www.youtube.com/watch?v=PLl8AM0RxEM&t=1904s).
  - MA trượt theo thời gian: «Theo thời gian thì MA200 này sẽ chạy về đây và Fibo 618 cũng khớp về đây» [07-02 00:38:16](https://www.youtube.com/watch?v=w4bvsDte3bI&t=2296s).
- **Con số + vùng**: thường 1 số tròn nghìn ở mép EMA (91k, 82k, 76k…).
- **Vào / tránh / chờ**
  - MA bị test nhiều lần thì bỏ: «test MA34 rất là nhiều lần. Thì hiện tại cái MA34 này nó không còn giá trị nữa» [01-06 00:10:45](https://www.youtube.com/watch?v=aQbHs7J80jc&t=645s).
  - Giá xa MA → không short đuổi: «giá mà nằm xa khỏi MA thì chúng ta đừng có short đuổi ở đây» [02-03 00:15:05](https://www.youtube.com/watch?v=ewRoIMVREvw&t=905s).
  - Nửa cuối năm MA bị tắt nhiều (ảnh 24/07–05/08: 1/19 ảnh có MA) — «Ngày xưa mình hay dùng MA. Bây giờ mình vẫn dùng, nhưng mà mức độ phản ứng của giá đối với MA hiện tại mình đánh giá không cao bằng so với trendline» [08-18 00:23:09](https://www.youtube.com/watch?v=_c0_SERWnz0&t=1389s) (`hinh_anh_4.md` mục a).
- **Tần suất**: `cach_lam` 159/180 buổi; mốc có căn cứ MA 308/3.349 (9%).
- **Ví dụ**
  1. **01-06, 91k** (3 EMA hội tụ) → chờ long 91, TP 95,8k. **Đo:** chạm sau ~38 giờ (râu 89,3k ngày 08/01), 13/01 lên 96,5k — TP đạt.
  2. **04-06, 82k = MA200 D1**: «nó có thể đẩy lên đến 82 MA200 ở trên khung ngày. Đây mới thực sự là điểm để bắt đầu tìm điểm sell swing» [04-06 00:24:01](https://www.youtube.com/watch?v=b48t6sSiV90&t=1441s). **Đo:** 06/05 đỉnh 82.842, sau đó 01/07 về 57.809.
  3. **09-16, 76k = MA200 H4 + MA34 D1**: «Vùng 76 này là vùng hỗ trợ cho nên chúng ta không vào thêm vị thế bán quanh vùng 75.000» [09-16 00:14:48](https://www.youtube.com/watch?v=31jXsidP5KE&t=888s).

### A4. Đỉnh / đáy / râu cũ, cản cũ đổi vai
- **Tình huống**: giá quay lại gần một đỉnh/đáy/râu bên trái, hoặc vừa phá một cản.
- **Đo/vẽ gì**
  - Râu cũ: «Các bạn kiểm chứng lại tất cả các râu nến đã tạo ra, theo thời gian đều có những nhịp về test» [03-04 00:27:43](https://www.youtube.com/watch?v=OawlrpkFqQk&t=1663s); «Các râu đều có giá trị nhá. Không có râu nào là vô nghĩa hết, cứ bám theo râu» [09-15 00:08:37](https://www.youtube.com/watch?v=M1ZThKy2Ylk&t=517s).
  - Cản cũ bị phá → hỗ trợ: «Vùng này hôm qua là kháng cự, vùng 73. Nhưng mà một khi giá đã break out ra thì bây giờ nó sẽ là một vùng hỗ trợ cứng quanh 73» [04-14 00:37:25](https://www.youtube.com/watch?v=LfNwCzyBHdM&t=2245s).
  - Tính theo thân nến đóng: «Chúng ta tính theo điểm đóng nến. Điểm đóng thân nến» [04-17 00:14:30](https://www.youtube.com/watch?v=PH5pABMJ01k&t=870s).
  - Cách vẽ: hộp hoặc **2 đường ngang vàng, 1 ở râu, 1 ở giá đóng cửa** (`SO_TAY_TINH_HOA.md` D4) → vùng = khoảng giữa râu và thân.
- **Con số + vùng**: Đo: 75% mốc "đỉnh/đáy/râu cũ" khớp đúng đỉnh/đáy fractal thật (`SO_LIEU_CAN_CU.md` §3). Hộp D1 01–02/10 **80,9–82,0k** (đỉnh tháng 8–9 đổi vai).
- **Vào / tránh / chờ**: chờ giá về test lại vùng đã phá rồi mới vào (C3); đừng làm gì sớm hơn vùng: «Nhìn D1 đây là vùng hỗ trợ, cứ về đây tính, đừng làm gì sớm hơn vùng này» [09-28 00:21:06](https://www.youtube.com/watch?v=G5Q1ATx_1ho&t=1266s).
- **Tần suất**: `cach_lam` 97/180 buổi; mốc có căn cứ đỉnh/đáy/râu 508/3.349 (15%), lên **22% mốc tháng 10**.
- **Ví dụ**
  1. **04-14, 73k đổi vai** → **Đo:** 16/04 râu 73.303 giữ, 22/04 lên 79.462.
  2. **09-22, 82–83k**: «vùng hỗ trợ cứng hiện tại của thị trường là 82 và 83. Vì sao? Bởi vì trước đó đây là cản cứng, thì bây giờ nó trở thành vùng support» [09-22 00:27:30](https://www.youtube.com/watch?v=N-_6NBs4ZW8&t=1650s).
  3. **03-04, râu**: «Râu 62 thì về test, râu 60 thì về test 62, về test 63» [03-04 00:27:43](https://www.youtube.com/watch?v=OawlrpkFqQk&t=1663s).

### A5. Vùng sideway / base cũ
- **Tình huống**: phía trước có một khoảng giá từng đi ngang lâu.
- **Đo/vẽ gì**: hộp phủ cả vùng đi ngang cũ kéo sang phải.
  - «Trước đó nó là vùng base sideway, sau đó break rồi chạy mô hình cờ trên khung ngày… kéo về 6x» → 87–90 nay là cản [10-06 00:14:15](https://www.youtube.com/watch?v=CABZxVcYavM&t=855s).
  - Ảnh 24/07 (H1): hộp **63,85–64,35k** (vùng breakout cũ từ 17/07) + heatmap → «chờ buy ở cái vùng này hoàn toàn hợp lý» [07-24 00:35:30](https://www.youtube.com/watch?v=7D1Ve5hs4bU&t=2130s).
- **Con số + vùng**: hộp vẽ ~500 giá (H1) đến ~3.000 giá (D1).
- **Vào / tránh / chờ**: giá còn **trong** hộp thì chờ phá: «Khi thị trường chui vào một cái hộp, một cái biên ngang như thế này, thì kiểu gì anh em cũng phải chờ fake out» [09-29 00:37:06](https://www.youtube.com/watch?v=3inGNRqb-UM&t=2226s) (xem E2).

### A6. Hội tụ (cộng căn cứ) → vùng "cứng"
- **Tình huống**: nhiều công cụ cùng chỉ một số.
- **Lời người đó**: «cái điểm nào nó giao hợp nhiều cái chỉ báo thì cái chỗ đó nó càng có giá trị» [03-10 00:31:01](https://www.youtube.com/watch?v=TXnTpUkc78s&t=1861s); «một vùng giá mà nó quy tụ càng nhiều cản… thì vùng đó có xác suất đảo chiều càng cao» [08-05 00:24:17](https://www.youtube.com/watch?v=uw4QcusFtBc&t=1457s); «Bình thường chúng ta chỉ cần khoảng ba lý do là quá đủ rồi» [06-01 00:25:32](https://www.youtube.com/watch?v=cgTktZyPPt4&t=1532s).
- **Đo/vẽ gì**: hộp vàng tô mờ hoặc hộp viền đỏ tô ô liu chỗ trùng (ảnh, `hinh_anh_4.md` mục d).
- **Con số + vùng**: khi hội tụ, vùng hẹp lại ở chỗ trùng (85,0–85,5k; 81–82k).
- **Tần suất / đo**: mốc entry gần giá có ≥2 loại căn cứ nói ra: 53/286 (`moc`). **Đo thô** (chạm ≤7 ngày, TP cùng buổi ≤14 ngày, giá OKX 1H): entry ≥2 căn cứ đạt TP 10/25 = 40%; entry 0–1 căn cứ đạt 56/103 = 54% — **chưa thấy khác biệt rõ** (n nhỏ, TP ghép theo buổi).
- **Ví dụ**
  1. **03-24, 83k**: «Đột nhiên vùng 83 này trùng luôn với đường màu cam mình vẽ… Fibo 0.5 nằm ở 78 và Fibo 0.618 nằm ở 83» [03-24 00:26:04](https://www.youtube.com/watch?v=xKTPieljFuY&t=1564s) + Fibo mở rộng 1 → **Đo:** 06/05 đỉnh 82.842, không qua 83 (VD5 sổ tay).
  2. **01-06, 91k** (3 EMA, A3).
  3. **10-02, 85,0–85,5k** (Fibo 0.5 + 0.618 + cản đỉnh cũ, A1).

---

## B. ĐỘ RỘNG VÙNG CỦA NGƯỜI ĐÓ

### B1. Bảng chính (BTC, mốc cách giá lúc nói ≤30%)
"1 số" = người đó nói một con số ("vùng 91"). Cột độ rộng chỉ tính khi họ nói đủ 2 mép.

| Loại | n | % chỉ 1 số | n có 2 mép | Trung vị (giá) | p25–p75 (giá) | Trung vị % | p25–p75 % |
|---|---|---|---|---|---|---|---|
| Vùng vào (nói ra) | 448 | 59% | 183 | **1.000** | 500–1.000 | 1,29% | 0,78–1,60% |
| Vào trong lệnh | 293 | 55% | 132 | **1.000** | 500–1.000 | 1,29% | 0,79–1,61% |
| TP | 331 | 75% | 83 | **1.000** | 500–1.000 | 1,34% | 0,65–1,75% |
| Hỗ trợ | 510 | 67% | 167 | **1.000** | 1.000–1.000 | 1,36% | 1,17–1,65% |
| Kháng cự | 498 | 72% | 139 | **1.000** | 800–1.000 | 1,27% | 1,02–1,50% |
| Đích | 690 | 63% | 252 | **1.000** | 1.000–2.000 | 1,55% | 1,29–2,95% |
| SL | 156 | 88% | 19 | **700** | 175–1.000 | 1,08% | 0,26–1,50% |
| Mốc sai (vô hiệu) | 117 | 82% | 21 | **1.000** | 1.000–1.000 | 1,44% | 1,17–1,53% |
| **Vùng tránh** | 268 | 41% | 159 | **1.300** | 1.000–2.750 | 1,89% | 1,32–3,46% |

Đối chiếu bộ `moc` (180 buổi, rút độc lập):

| Loại | n | % chỉ 1 số | n có 2 mép | Trung vị (giá) | p25–p75 (giá) | Trung vị % | p25–p75 % |
|---|---|---|---|---|---|---|---|
| Entry | 288 | 60% | 114 | **1.000** | 1.000–1.075 | 1,46% | 1,08–1,76% |
| TP | 262 | 76% | 64 | **1.000** | 575–1.000 | 1,40% | 0,77–1,77% |
| Hỗ trợ | 399 | 66% | 134 | **1.000** | 1.000–1.000 | 1,32% | 1,12–1,54% |
| Kháng cự | 353 | 76% | 84 | **1.000** | 1.000–1.999 | 1,33% | 1,15–2,06% |
| Đích | 763 | 65% | 269 | **1.000** | 1.000–3.000 | 1,83% | 1,32–3,64% |
| SL | 111 | 91% | 10 | **1.000** | 575–1.000 | 1,18% | 0,73–1,50% |
| Mốc sai (vô hiệu) | 202 | 85% | 31 | **1.000** | 1.000–1.000 | 1,46% | 1,29–1,56% |

- Đọc nhanh: **vào / TP / hỗ trợ / kháng cự: trung vị 1.000 giá (~1,3%), p25–p75 thường 500–1.000**; đích rộng hơn (p75 2.000–3.000); vùng tránh rộng nhất (trung vị 1.300 giá; ví dụ cả khoảng giữa 76–78,5k ở D1).
- SL/vô hiệu gần như luôn là **1 số** (82–91%).

### B2. Độ rộng tăng theo khoảng cách và theo khung
| Cách giá lúc nói | n có 2 mép / tổng | % nói 2 mép | Trung vị (giá) | p25–p75 (giá) | Trung vị % |
|---|---|---|---|---|---|
| ≤2% | 268/963 | 28% | 1.000 | 300–1.000 | 1,12% |
| 2–5% | 289/786 | 37% | 1.000 | 1.000–1.000 | 1,36% |
| 5–15% | 204/582 | 35% | 1.500 | 1.000–3.000 | 1,96% |
| 15–30% | 63/146 | 43% | 3.000 | 1.000–5.750 | 3,82% |

| Khung người đó nói (moc) | n có 2 mép / tổng | Trung vị (giá) | p25–p75 (giá) | Trung vị % |
|---|---|---|---|---|
| M5 | 31/147 | 1.000 | 350–1.000 | 1,18% |
| M15 | 5/29 | 500 | 200–1.000 | 0,64% |
| M30 | 22/82 | 1.000 | 350–1.000 | 1,12% |
| H1 | 61/188 | 1.000 | 500–1.000 | 1,36% |
| H4 | 187/578 | 1.000 | 1.000–1.650 | 1,44% |
| D1 | 180/496 | 1.650 | 1.000–3.000 | 2,02% |
| W1 | 57/172 | 3.000 | 1.000–5.000 | 3,28% |
| MN | 5/14 | 1.000 | 1.000–9.999 | 1,90% |
| không nói | 228/704 | 1.000 | 1.000–2.000 | 1,48% |

- Gần giá (≤2%) và khung M5–H4: **≤1.000 giá**. Khung D1 ~1.650, khung tuần ~3.000. Vùng **swing** ở xa được nói rộng hơn: «Entry mình muốn đánh swing phải từ 98 cho đến khoảng 105» [01-20 00:25:34](https://www.youtube.com/watch?v=GygVJDmjlgY&t=1534s); «entry anh em sẽ phải rải ra từ 78.500 cho đến khoảng 84» [03-12 00:29:23](https://www.youtube.com/watch?v=qJZk9q5A7rA&t=1763s).

### B3. "Vùng X" nghĩa là gì — lời người đó
- «về đến cái vùng 82 là cái vùng hỗ trợ cứng 82. Vùng 82 thì có nghĩa là không phải là 8200 [82.000] mà nó có thể là 82008, 82006, 824, 82002, 82001, 82003, 82.550 kiểu như vậy loanh quanh cứ cái đầu 82… 81.900… cũng là loanh quanh cái vùng 82» [09-28 00:19:25](https://www.youtube.com/watch?v=G5Q1ATx_1ho&t=1165s) (phụ đề tự động, số đọc liền).
  → Theo đúng các số họ đọc: "vùng 82" = **đầu số 82**, từ 81.900 đến 82.550 (~650 giá).
- Sai số chấp nhận khi đạt đích: «biên độ dao động… khoảng 150 đến 200 giá» [08-04 00:14:31](https://www.youtube.com/watch?v=K6QkKY6Og7o&t=871s).

### B4. Số tròn và cách "non" / lệch
**Đo** (mỗi mép vùng / số đơn, nhãn v5, gần giá ≤30%):

| Loại | n mép | chẵn 1.000 | chẵn 500 | chẵn 100 | lẻ (<100) |
|---|---|---|---|---|---|
| Đích | 942 | 91% | 3% | 6% | 0% |
| **Vùng tránh** | 427 | 88% | 3% | 8% | 0% |
| Hỗ trợ | 677 | 81% | 4% | 13% | 1% |
| Kháng cự | 637 | 81% | 5% | 14% | 0% |
| Vùng vào (nói ra) | 631 | 73% | 8% | 18% | 1% |
| TP | 414 | 73% | 6% | 18% | 3% |
| SL | 175 | 63% | 7% | 23% | 6% |

- Đích/vùng tránh gần như luôn là số chẵn nghìn; **TP và SL** mới xuống tới số lẻ trăm / lẻ chục.

| Cách | Lời người đó / ví dụ |
|---|---|
| TP đặt **trước** mép gap / mức | Gap 88.002 → TP 88.000–88.100: «Cái lệnh short đêm qua TP ở 88.100» [01-21 00:01:54](https://www.youtube.com/watch?v=LRkYCtbojb0&t=114s) |
| TP lẻ ngay đáy/hỗ trợ | «TP ngay cái đáy này. 71 71060. TP1 ở đó» [03-13 00:42:52](https://www.youtube.com/watch?v=gRyoN4cBXZA&t=2572s); «chốt lệnh short ở 75k68 là vì nó nằm ngay hỗ trợ» [04-29 00:23:56](https://www.youtube.com/watch?v=-YYkW3NZT0M&t=1436s); «Mình để 73950 được 1/2 lệnh» [03-05 00:26:00](https://www.youtube.com/watch?v=pbr4y9qP1Ys&t=1560s) |
| SL né số chẵn / SL đám đông | «vì sao không nên SL60, bởi vì 60 là số chẵn thì nếu nó quét khả năng nó quét qua» [02-06 00:10:12](https://www.youtube.com/watch?v=PLl8AM0RxEM&t=612s); «70.002 70.003 đúng là stop loss của đại đa số luôn» [03-05 00:50:13](https://www.youtube.com/watch?v=pbr4y9qP1Ys&t=3013s); «Hôm qua mình cho anh em SL ở 66.998» [03-25 00:25:45](https://www.youtube.com/watch?v=byYCWvbkZyU&t=1545s) |
| Giá dừng **trước** số tròn đám đông chờ | «nếu market muốn đẩy lên thì nó sẽ không bao giờ về 80; nó chỉ về loanh quanh 82» [09-30 00:22:49](https://www.youtube.com/watch?v=3qAxAK71YAs&t=1369s) |
| Vùng thanh lý dừng thiếu vài chục giá | «nó chỉ quét lên đến 64.470 (thiếu 30 giá nữa)» [08-12 00:46:28](https://www.youtube.com/watch?v=EaWaSL7aWT4&t=2788s) |
| Entry lẻ khi có điểm cụ thể | «Mình vào là giá 71114» [03-13 00:11:42](https://www.youtube.com/watch?v=IbTz3V-KlKs&t=702s); «chờ ở vùng 69750» [03-11 00:20:18](https://www.youtube.com/watch?v=q-9RpBVzOhU&t=1218s); «đóng vượt qua 91.550» [01-13 00:22:57](https://www.youtube.com/watch?v=vg80vm31RLM&t=1377s) |

---

## C. CHỖ VÀO (vùng ổn) THEO VIEW TRUNG HẠN

**Đo hành vi chung** (nhãn v5, 180 buổi):
- Hành động cuối buổi: **đứng ngoài chờ entry 101 buổi**, giữ lệnh 52, vào ngay (long/short) chỉ 11, lấp lửng 9.
- Lệnh đề xuất mới: 242 lệnh ở 150/180 buổi (trung bình 1,3 lệnh/buổi, gồm cả lệnh 2 kịch bản). Vào: 1 số 107 · vùng 120 · không số 15 · có SL 70/242.
- Vùng vào cách giá lúc nói: trung vị **1.500 giá (2,0%)** → gần như luôn là chờ giá **về**, không vào giá đang chạy.
- Khoảng vào → TP: trung vị **4.000 giá (5,5%)**, p25–p75 2.313–7.000 giá.
- **Đo** (OKX 1H; T = giờ câu cuối buổi): 223 lệnh có vùng vào + chiều → **giá về chạm vùng 153 (69%)**, chạy tới TP mà không về 32 (14%), không về trong 7 ngày 38. Thời gian chờ tới vùng: trung vị 7 giờ (p75 23 giờ). Đã chạm và có TP: 112 → **đạt TP trong 14 ngày 45 (40%)**, thời gian chạm→TP trung vị 66 giờ. Lệnh đạt TP: giá đi **quá mép xa của vùng** trung vị 741 giá, p75 1.980 (10/45 lệnh không quá mép).

### C1. View TĂNG → chờ HỒI về hỗ trợ hội tụ rồi long
- **Tình huống**: D1/H4 tăng («Khung ngày như này thì không nên short» [01-06 00:08:36](https://www.youtube.com/watch?v=aQbHs7J80jc&t=516s)), giá đang ở trên cao.
- **Đo/vẽ gì**: Fibo thoái lui nhịp vừa chạy + EMA nhiều khung + râu/đáy cũ + gap/heatmap phía dưới (A1, A3, A4).
- **Con số + vùng**: 1 số hoặc ≤1.000 giá (91; 93–94; 67–68).
- **Vào / chờ**
  - Vùng là điều kiện cần, nến là điều kiện đủ: «Nếu mà long thì điều kiện cần để vào lệnh long đó là phải test lại cái râu 91.00 này» [01-19 00:20:31](https://www.youtube.com/watch?v=rmCGKqaMkdw&t=1231s); «không phải là cứ về test đây các bạn limit ở đây mà long là chết. Bởi vì đôi khi nó về lấp gap 88.000 thì sao?» (cùng chỗ).
  - «Vùng 94 cho đến 93 là vùng chúng ta sẽ chờ. Không phải là chúng ta cần limit long ở đoạn này» [01-16 00:10:59](https://www.youtube.com/watch?v=SllvhCOjrkE&t=659s).
  - Không về thì thôi: «Nó về thì đón, không về thì thôi» [09-30 00:12:55](https://www.youtube.com/watch?v=3qAxAK71YAs&t=775s).
- **Tần suất**: lệnh LONG đề xuất mới 145 (nhãn).

### C2. View GIẢM → chờ HỒI lên kháng cự hội tụ rồi short (swing)
- **Tình huống**: tuần/D1 giảm, giá đang hồi.
- **Đo/vẽ gì**: EMA D1/tuần, Fibo thoái lui sóng lớn (97,9k → 59,8k), gap, đỉnh cũ.
- **Con số + vùng**: swing nói rộng (5–7k giá) và **chia entry trong vùng**.
- **Vào / chờ**
  - «78 đến 80 cân nhắc short swing được» [03-12 00:28:51](https://www.youtube.com/watch?v=qJZk9q5A7rA&t=1731s); «Thì entry anh em sẽ phải rải ra từ 78.500 cho đến khoảng 84… Rải đến 84 còn SL 90 thì được» [03-12 00:29:23](https://www.youtube.com/watch?v=qJZk9q5A7rA&t=1763s); «Short ở 84, 85 và TP 53 là ăn được khoảng 30.000 giá. SL thì tầm khoảng 10.000 giá. Tỉ lệ 1:4 là đẹp» [03-12 00:30:28](https://www.youtube.com/watch?v=qJZk9q5A7rA&t=1828s).
  - «Nó sẽ phải hit được vùng 80 thì lúc đó mình mới tính đến chuyện swing short về 50, 40» [03-31 00:40:25](https://www.youtube.com/watch?v=bz8_iuwosGs&t=2425s).
  - Giá thấp hơn vùng swing thì chỉ scalp: «Vùng này mình chỉ đánh scalp chứ không swing, đôi khi sẽ mất cơ hội nhưng chấp nhận» [01-20 00:25:34](https://www.youtube.com/watch?v=GygVJDmjlgY&t=1534s).
  - **Vùng short chính đo trên nhịp D1, không trên nhịp H4 con; giá chưa tới thì giữ vùng qua buổi sau.** Giá thủng xuống,
    sinh ra một nhịp H4 con nhỏ (hồi vài nghìn giá rồi gãy) → người đó KHÔNG hạ vùng short xuống Fibo của nhịp con; cụm
    gần đó là chỗ "lấy được ít tiền".
- **Tần suất**: lệnh SHORT đề xuất mới 97 (nhãn).
- **Ví dụ**: (1) 03-12 → 04-06 → 05-11 vùng 78,5–84 / 82 (A3). **Đo:** 22/04 đỉnh 79.462, 06/05 đỉnh 82.842 (khớp tới ~82,8k, chưa tới mép 84k), 01/07 về 57.809 (~25.000 giá dưới 82,8k); TP 53–54k chưa tới. (2) 01-20 «98 cho đến 105»: **Đo:** không về (đỉnh sau đó 92.870) — họ không short swing; giá vẫn rơi về 60.000 (06/02). (3) 04-28 «77.000 cho đến 78.000 này có vẻ an toàn hơn short» [04-28 00:34:16](https://www.youtube.com/watch?v=lZw7Ts1eLWo&t=2056s).

### C3. PHÁ rồi TEST LẠI (breakout – backtest, "Fibo Eric")
- **Tình huống**: giá vừa phá một cản / mức Fibo bằng nến đóng.
- **Đo/vẽ gì**: mức vừa phá (cản cũ, Fibo 0.5, trendline); nến H4 đóng.
- **Vào / chờ**: «Nguyên tắc là không short ở hỗ trợ và không long ở kháng cự… Vùng kiểm tra này mới là điểm vào chứ không phải nhảy ngay vào ở điểm này» [04-01 00:13:42](https://www.youtube.com/watch?v=Be-e74Mwx0U&t=822s). Nửa cuối năm: «mình hay đánh market lắm, break là mình vào» [08-26 01:11:37](https://www.youtube.com/watch?v=I1DFCTsjQXE&t=4297s); nhưng «Chứ chỉ cứ mỗi trendline break là nhảy vào đánh thì không phải lúc nào cũng đúng. Đánh như vậy tiền đâu mà chịu cho nổi» [08-27 00:11:01](https://www.youtube.com/watch?v=ZJ5BVqdLJeE&t=661s).
- **Ví dụ**: (1) 04-14 73k đổi vai (A4; Đo: giữ 73,3k rồi +6k). (2) 10-02 «H4 đóng trên 85 là có sự confirm» (A1). (3) 04-01 tự rút từ lệnh sai: «Short ở điểm 66 ngày hôm qua… chúng ta short ở đây sai vì sao? Bởi vì đây là hỗ trợ» [04-01 00:13:42](https://www.youtube.com/watch?v=Be-e74Mwx0U&t=822s).

### C4. Vào ở ĐÍCH CHẶNG 1 (sau cú quét)
- **Tình huống**: vùng gần có đông người chờ; người đó cho rằng giá quét qua trước.
- **Vào / chờ**: «9293 demand thì chờ fake out, chờ check out xuống một phát, chờ check out xuống 91. Demand thì nó sẽ SL những lệnh long FOMO ở đó» [01-06 00:58:43](https://www.youtube.com/watch?v=aQbHs7J80jc&t=3523s). Lệnh long đặt ở 91 (đáy chặng 1), không ở 92–93.
- **Ví dụ**: 01-06 (Đo: 01/08 râu 89,3k rồi 96,5k). Xem E1.

### C5. Vào một lần hay chia? Limit hay chờ nến?
| Việc | Lời người đó |
|---|---|
| Chia entry (swing) | «Nếu bạn swing x5 thì lời khuyên của mình là chia nhỏ cái entry ra, chia từ vùng hiện tại vào 1x cho đến 59» [02-06 00:09:40](https://www.youtube.com/watch?v=PLl8AM0RxEM&t=580s); «Phải xác định chia ra nhiều entry. Ví dụ nó có một vùng liquid ở 89, thì hãy sẵn sàng chờ thêm ở vùng 89 hoặc 88» [01-22 00:29:59](https://www.youtube.com/watch?v=WvCOBcm0bd0&t=1799s); «cứ chia giải ra. 91 81» [04-01 00:31:35](https://www.youtube.com/watch?v=Be-e74Mwx0U&t=1895s) |
| Không DCA nhồi lệnh trong lúc giá đi ngược | «không nên vào đây một lệnh stop loss chúng ta vào thêm volume và về 71 chúng ta vào thêm… mình không khuyến khích điều đó» [03-16 00:20:38](https://www.youtube.com/watch?v=uXm43DPUtPQ&t=1238s) |
| Limit chỉ khi "khó khớp" | «khó khớp thì mới limit giống như hai đêm vừa rồi» [09-17 00:05:20](https://www.youtube.com/watch?v=7mETSY5t5Yg&t=320s); «Limit để ở xa. Khi nào đi ngủ thì bỏ» [03-11 00:31:06](https://www.youtube.com/watch?v=q-9RpBVzOhU&t=1866s) |
| Không limit khi chưa chắc | «Đừng limit trước là nguy hiểm bởi vì chưa chắc, biết đâu nó gãy luôn thì sao?» [01-16 00:11:33](https://www.youtube.com/watch?v=SllvhCOjrkE&t=693s); «Về đó cứ chờ nến thôi, không limit chờ đây» [10-19 01:04:42](https://www.youtube.com/watch?v=-avZ2E3n2oE&t=3882s) |
| Ngồi chờ khi giá chưa tới | «giá nó đang tận 70.000 năm thì bây giờ chúng ta làm gì? Ngồi chờ, đi uống cà phê, đọc sách, nghe nhạc» [03-25 00:30:30](https://www.youtube.com/watch?v=byYCWvbkZyU&t=1830s) |

---

## D. CHỖ TRÁNH

**Tần suất** (nhãn v5, 594 mục `vung_tranh` ở 180/180 buổi; đếm theo từ khóa trong lý do + trích, 1 mục có thể nhiều loại):

| Loại tránh | Số mục | Số buổi | % buổi |
|---|---|---|---|
| Vào khi giá chưa tới vùng / «giá hiện tại» | 217 | 141 | 78% |
| FOMO, đuổi, short đáy / long đỉnh, giá xa MA | 148 | 110 | 61% |
| Vùng sẽ bị quét / trap / thanh lý | 132 | 96 | 53% |
| Khác (không khớp từ khóa) | 112 | 85 | 47% |
| Chưa có nến/xác nhận; không limit | 78 | 70 | 39% |
| Giữa / nhập nhằng / 50-50 / sideway / hai đầu | 73 | 64 | 36% |
| Tin, thứ Hai, phiên Mỹ, đêm, đóng nến tuần/tháng | 63 | 46 | 26% |
| Ngược xu hướng khung lớn (cản tàu) | 57 | 54 | 30% |
| Short ngay hỗ trợ / long ngay kháng cự | 41 | 37 | 21% |
| R:R xấu, entry còn xa | 19 | 18 | 10% |
| SL ở số chẵn / trong vùng bị hút | 9 | 9 | 5% |

### D1. Vào khi giá CHƯA TỚI vùng / đang ở GIỮA
- **Tình huống**: giá nằm giữa vùng mua và vùng bán đã vẽ.
- **Đo/vẽ gì**: 2 vùng đã vẽ (dưới để long, trên để short); khoảng giữa không có căn cứ.
- **Con số + vùng**: chính khoảng giữa, nói rộng (vd 76–78,5k = 2.500 giá).
- **Tránh / chờ**: «Cho nên chúng ta có nguyên một vùng này không có gì để làm» (76–78,5k) [05-18 00:35:52](https://www.youtube.com/watch?v=phLlmyf_8-w&t=2152s); «Cứ còn trong vùng này thì đánh rất khó» (63–65k) [06-23 00:17:07](https://www.youtube.com/watch?v=w3K-VXD_Tns&t=1027s); «Bây giờ nếu chúng ta long lên thì sẽ bị cản trở bởi cái H4 này. Còn nếu chúng ta short xuống thì sẽ bị cản trở bởi khung ngày» [08-28 00:16:55](https://www.youtube.com/watch?v=KwvLRMMnVms&t=1015s); «cứ về đây tính, đừng làm gì sớm hơn vùng này» [09-28 00:21:06](https://www.youtube.com/watch?v=G5Q1ATx_1ho&t=1266s).
- **Ví dụ**: 05-18 (Đo: tuần sau 74,3–78,2k — không chạm 78,5k bên short), 03-25 (ngồi chờ), 06-23.

### D2. FOMO / đuổi giá (long đỉnh, short đáy, giá xa MA)
- **Tránh**: «Sáng nay bị FOMO long 94.000 hả? Thế thì lại mệt rồi» [01-06 00:05:50](https://www.youtube.com/watch?v=aQbHs7J80jc&t=350s); «Short ở đây là có chừng short đáy. Thị trường vẫn còn đang hồi» [06-08 00:19:42](https://www.youtube.com/watch?v=WZ8PpZ9VA4Q&t=1182s); «FOMO đáy này còn nguy hiểm hơn cả FOMO cao nữa» [06-26 00:21:09](https://www.youtube.com/watch?v=UzjWDBAiahs&t=1269s); «kẹp MA đoạn này mình không chơi nữa, vì trước đó nó đã chạy rồi» [09-30 00:36:45](https://www.youtube.com/watch?v=3qAxAK71YAs&t=2205s).
- **Ví dụ**: 01-06 (94k), 02-04 «đám short vào từ vùng 74 cho đến 73 này chắc chắn sẽ bị thanh lý» [02-04 00:09:29](https://www.youtube.com/watch?v=c6WnN4Q9EXo&t=569s), 07-22 «Đoạn này long FOMO sẽ cực kỳ rủi ro» [07-22 00:35:10](https://www.youtube.com/watch?v=3gr71JlVqR8&t=2110s).

### D3. Short ngay hỗ trợ / long ngay kháng cự ("vùng chốt lãi ≠ vùng entry")
- **Tránh**: «Nguyên tắc là không short ở hỗ trợ và không long ở kháng cự» [04-01 00:13:42](https://www.youtube.com/watch?v=Be-e74Mwx0U&t=822s); «Vùng này là vùng chốt lãi chứ không phải vùng entry. Anh em phải phân biệt» [07-22 00:25:59](https://www.youtube.com/watch?v=3gr71JlVqR8&t=1559s); «Vùng này là vùng cản, anh em đánh phải đánh nhỏ và té sớm, không phải vùng để ở lại lâu» [01-14 00:19:37](https://www.youtube.com/watch?v=2ZyVfVN3n4Y&t=1177s).
- **Ví dụ**: 04-20 «nếu anh em muốn short ở đây thì gần như đang short ngay hỗ trợ» [04-20 00:23:01](https://www.youtube.com/watch?v=nN446WPRxPo&t=1381s); 04-29 «75k9 thì hơi chia buồn» [04-29 00:40:45](https://www.youtube.com/watch?v=-YYkW3NZT0M&t=2445s); 09-16 76k (A3).

### D4. Vùng sẽ bị QUÉT (đông người, SL đám đông, số tròn)
- **Đo/vẽ gì**: heatmap/Hyblock (phe đông), số tròn, cụm SL.
- **Tránh**: demand 92–93 «sẽ SL những lệnh long FOMO ở đó» (C4); «cứ short ở đây mà SL trong vùng từ 61 cho đến 59 này thì kiểu gì cũng có xác suất bị hút rất cao» [07-01 00:21:05](https://www.youtube.com/watch?v=WNiQnpm2BLo&t=1265s); «nếu anh em vào chung một con tàu…» (70–71,3k, «50-50 quá») [03-13 01:01:23](https://www.youtube.com/watch?v=IbTz3V-KlKs&t=3683s); SL số chẵn (B4).
- **Ví dụ**: 01-06, 07-01, 03-05 (70.002–70.003).

### D5. Ngược xu hướng khung lớn ("cản tàu")
- **Tránh**: «long thì lại cản tàu đi bắt đáy là càng chết nữa» [02-05 00:10:14](https://www.youtube.com/watch?v=D6s6HggWgVQ&t=614s); «nếu đánh long thì về nguyên tắc hệ thống giao dịch nó sẽ bị xung đột» [05-29 00:29:12](https://www.youtube.com/watch?v=AmGhhyxkErs&t=1752s); «Scalping thì được, còn cứ cố đi cản tàu đoạn này thì rủi ro rất lớn. Đó là mình nói đối với khung tuần» [09-21 00:18:15](https://www.youtube.com/watch?v=I_U52BYUt0M&t=1095s).
- **Ví dụ**: 02-05, 05-29, 09-21.

### D6. Quanh tin, thứ Hai, phiên Mỹ, đêm
- **Tránh**: «Hôm nay là thứ hai… trong ngày hôm nay cho đến 10:00 sáng ngày mai thì các bạn hãy khoan vào bất kỳ lệnh short nào» [06-01 00:06:18](https://www.youtube.com/watch?v=cgTktZyPPt4&t=378s); «Phiên Mỹ nó hơi ẩu. Hôm nay thứ hai nó hơi trap» [07-13 01:07:19](https://www.youtube.com/watch?v=O3q2fmXlwhk&t=4039s); «Vùng 75k1 nói thiệt là nhấn một phát nó rơi về 74 luôn, bạn không kịp xử lý» (đêm tin Fed) [09-17 00:13:26](https://www.youtube.com/watch?v=7mETSY5t5Yg&t=806s); «hôm nay thứ hai, cho nên đánh đấm thận trọng» [09-28 01:02:01](https://www.youtube.com/watch?v=G5Q1ATx_1ho&t=3721s).

### D7. Limit / vào trước khi có nến ở vùng chưa chắc; R:R xấu
- **Tránh**: «Short ở 96 thì hoàn toàn không, thứ nhất entry đó còn xa đến tận 4000 giá so với hiện tại. Thứ hai nếu bạn short ở 96 thì không cần phải limit» [01-12 00:06:16](https://www.youtube.com/watch?v=xwJagQCx1gY&t=376s); «Ví dụ bây giờ chúng ta vào một vị thế ở 74.000 mua spot thì stop loss của bạn sẽ là 64.000… Cho nên chúng ta không chơi» [04-14 00:32:00](https://www.youtube.com/watch?v=LfNwCzyBHdM&t=1920s); «không nên như thế, bởi vì vùng Fibo…» (FOMO tin chắc gãy 80) [10-16 00:09:07](https://www.youtube.com/watch?v=lSGpwulXi5s&t=547s).

---

## E. ĐƯỜNG ĐI NHIỀU CHẶNG (quét rồi mới đi) · RÂU CHƯA TEST

### E1. Chặng 1 ngược chặng 2
- **Tình huống**: người đó có hướng chính nhưng nói giá sẽ đi ngược một đoạn trước (quét thanh khoản / test râu / test Fibo).
- **Lời người đó**: «Liquidation xem nào. 8900. Thế thì khả năng vẫn có cú quét về 8900 rồi mới lên» [01-22 00:25:58](https://www.youtube.com/watch?v=WvCOBcm0bd0&t=1558s); «chúng ta chưa biết nó sẽ quét lên đâu rồi mới gãy xuống. Tất nhiên về dài thì nó sẽ gãy xuống thôi» [01-27 00:25:58](https://www.youtube.com/watch?v=Q2qX5gIvNC8&t=1558s); «Nếu có một cây nến mạnh kiểu gì sau đó nó hay quay xuống lụm SL rồi mới lên lại» [04-17 00:54:25](https://www.youtube.com/watch?v=PH5pABMJ01k&t=3265s); «Lên 77.000 khả năng là bị đạp về 76 rồi mới lên tiếp 79» [04-21 00:21:13](https://www.youtube.com/watch?v=AG126RfNCk4&t=1273s); demand 92–93 bị quét xuống 91 (C4).
- **Tần suất (đo)**: `duong_di` có ≥2 chặng ở 147/180 buổi; **chặng 1 ngược chặng 2 ở 109/180 buổi**; có ghi `pha_vo_gia` 145/180.
- **Đo kết quả** (đích chặng 1 / chặng 2 = mép gần, ≤14 ngày, OKX 1H): 105 buổi đủ số: **đúng thứ tự (chạm chặng 1 rồi chặng 2) 37 (35%)**, đi thẳng chặng 2 không qua chặng 1 28 (27%), chỉ tới chặng 1 40 (38%), không chạm 0.
- **Vào**: entry đặt ở **đích chặng 1** (C4).
- **Ví dụ**: 01-06 (91 → 96–98, Đo: đúng thứ tự); 01-21 (lên 91 rồi xuống 80; Đo: đúng thứ tự); 01-26 (88 → 86; Đo: đúng thứ tự).
- **Sau chặng 1 là vùng QUYẾT ĐỊNH, không phải đích**: chặng 1 lên cản → gãy về test vùng Fibo bên dưới; giữ được thì
  mới có cơ sở tăng, nến đóng thủng thì đi tiếp xuống — ghi rõ mức nến cần đóng ở vùng đó.
  - [11-02 · 00:34:22](https://www.youtube.com/watch?v=MEKVe_u8BA8&t=2062s) «Nhịp này phải lên được 80 và sau đó phải rớt về.» · [11-02 · 00:38:37](https://www.youtube.com/watch?v=MEKVe_u8BA8&t=2317s) «Nếu trong trường hợp nó không giữ được cái vùng 78 đến 77 thì đây nó sẽ về 74.» · [11-02 · 00:39:02](https://www.youtube.com/watch?v=MEKVe_u8BA8&t=2342s) «Nó phải về đến tận 67 nó mới gặp tiếp hỗ trợ.» (ảnh `MEKVe_u8BA8_003910.jpg`: vòng đỏ quanh cây nến tăng thẳng tháng 8 — vùng nến tăng thẳng không có hỗ trợ ở giữa; ảnh `MEKVe_u8BA8_003805.jpg`: Fibo neo đỉnh nhỏ ngay trước cú xả, vùng quyết định = 0.5–0.786 trùng hộp hỗ trợ cũ + EMA34 tuần)

### E2. Hộp đi ngang → fake out một đầu trước
- «Nếu nó muốn giảm thì sẽ có một cú lên để fake rồi mới xuống; nếu muốn tăng thì sẽ có một cú giảm để fake rồi mới tăng» [09-29 00:37:06](https://www.youtube.com/watch?v=3inGNRqb-UM&t=2226s).
- «Nếu muốn short thì phải chờ fake out và chờ quét stop loss. Còn nếu muốn long thì phải chờ phản ứng ở 66 cho đến 65, 64» [02-11 00:09:22](https://www.youtube.com/watch?v=MZ3XfAjYHqk&t=562s).
- «Nói chung vùng này nó "kêu" cũng ác lắm: nó kêu hai đầu, cho các bạn chất đầy hàng lên tàu rồi nó lụm cả hai» [09-21 00:23:01](https://www.youtube.com/watch?v=I_U52BYUt0M&t=1381s).

### E3. Râu chưa test → về test
- **Lời người đó**: «Nhìn cây nến ngày rút chân lên như vậy thì khả năng kiểu gì cũng về test lại cái râu này 91 hoặc thấp hơn. Cho nên sáng giờ anh em thấy mình không cho lệnh long nào» [01-07 00:12:57](https://www.youtube.com/watch?v=NOBgwE4Gdko&t=777s); «Khi có râu nến H4 như vậy thì gần như chắc chắn nó sẽ về test vùng này, loanh quanh cái râu này khoảng 63.000 cho đến 62.000» [08-14 00:50:16](https://www.youtube.com/watch?v=xK38gQ-G6uA&t=3016s).
- Ngoại lệ họ nói: «nó không test lại cái râu này, chỉ đi một lần» [08-12 00:46:28](https://www.youtube.com/watch?v=EaWaSL7aWT4&t=2788s).
- **Vùng**: râu → thân (vd 62–63k = 1.000 giá).
- **Vào / tránh**: chưa test râu thì **không vào chiều đi tiếp**, chờ giá về râu (01-07).
- **Tần suất**: câu có "râu" + "test" ở 64/180 buổi.
- **Ví dụ**: 01-07 (Đo: 08/01 râu 89,3k — về test 91 và thấp hơn); 08-14 (Đo: 14/08 14:00 râu 62.522 — về đúng vùng 62–63k trong ngày); 03-04 (A4).

### E4. Đường Fibo: lên 1 → về 0.5 → lên 1.618
- «Nó đi rất chuẩn Fibo: lên Fibo 1 gãy về 0.5, test lên lại đúng Fibo 2 rồi gãy về» [04-10 00:08:39](https://www.youtube.com/watch?v=u6rbQNQWJAE&t=519s); «Đây 80, 90. Thông thường đối với nhịp này nó hay chạy kiểu này: lên Fibo 1 sau đó rớt về 0.5 rồi mới lên tiếp Fibo 2» [04-14 00:25:06](https://www.youtube.com/watch?v=LfNwCzyBHdM&t=1506s).
- Chỗ về 0.5 = chỗ vào lại; mức 1 = TP1 (A2).

---

## F. Cách đo (để chạy lại)
- Độ rộng: `hoc_v5/nhan/*.json` → `vung_nguoi_do` (loại vao/tp/ho_tro/khang_cu/dich/sl/vo_hieu), `vung_tranh`, `lenh.vao`; `moc/*.json` → `gia`/`gia_tren` theo `vai_tro`, `khung`. Chỉ BTC (10k–200k), mốc cách `gia_btc_luc_noi` ≤30%. Độ rộng = mép trên − mép dưới; % = độ rộng / giữa vùng.
- Chạm/đạt: nến OKX 1H mở sau giờ nói; LONG chạm khi low ≤ mép trên, SHORT khi high ≥ mép dưới; chờ ≤7 ngày; TP ≤14 ngày sau chạm; "quá mép" = giá đi quá mép xa của vùng trước khi đạt TP. Giờ nói = giờ bắt đầu live (`transcripts/gio_live.tsv`) + giờ trong video. Hạn chế: lệnh "phá rồi vào" bị tính như lệnh chờ hồi; giờ lấy câu cuối buổi.
- Giờ trích của buổi không có giờ trong nhãn (08/28 → 10/22, `lam_sach`) được dò lại trong phụ đề `.vtt` theo cụm 3 từ.
