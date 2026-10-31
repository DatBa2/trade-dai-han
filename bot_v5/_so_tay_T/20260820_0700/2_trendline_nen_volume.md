> Lọc theo T = 2026-08-20 07:00 (giờ VN); bỏ 46 dòng có ngày ≥ T (mọi mốc ≥ 2026-08-20; dòng kết quả "Đo:" tính thêm 30 ngày; dòng không ngày mà có mức giá chỉ xuất hiện từ T trở đi cũng bỏ). Ví dụ còn lại đều trước T — không mở bản gốc.

# SỔ TAY BOT V5 — Phần 2: Trendline, nến và volume

> Chỉ ghi điều người đó NÓI (có trích, giờ, link) hoặc điều ĐO ĐƯỢC (ảnh chart, hiệu chỉnh máy). Không có luật nào do người viết tự thêm.
> Chỗ người đó nói hai kiểu khác nhau thì ghi cả hai, kèm ngày, để người duyệt quyết định.

## Cách đọc

- Mỗi case gồm: **Tình huống** → **Người đó kẻ/nhìn gì** → **Phá thật / phá giả** → **Kết luận + hành động** → **Tần suất** → **Ví dụ**.
- Ví dụ ghi theo dạng `MM-DD` · khung · [giờ trong video](link) — "trích nguyên văn" · ảnh nếu có. Ảnh nằm ở `so_tay/khung/`.
- **Tần suất** = số buổi có ít nhất một câu khớp (đếm bằng biểu thức chính quy trên mọi trường của nhãn buổi đó), trên tổng 180 buổi. Đây là "người đó có nhắc", không phải "điều đó đúng". Riêng số liệu trendline thì đếm từ trường `trendline` của nhãn (254 lần nhắc trong 139 buổi).
- Nguồn đo bằng máy: `hoc_v5/trendline/CHON.md`, `khop_chi_tiet.tsv`, `tham_chieu_anh.tsv`, `volume_pha.tsv`; mô tả ảnh: `so_tay/ghi_chu/hinh_anh_1..4.md`.

## Tóm tắt một trang

| # | Điều người đó làm | Câu gốc tiêu biểu |
|---|---|---|
| 1 | Kẻ kháng cự giảm từ **râu đỉnh cao nhất qua râu đỉnh thấp hơn**, kéo dài sang phải; kẻ hỗ trợ tăng từ **râu đáy thấp nhất qua các đáy cao dần** (ảnh: 12/39 thời điểm thấy đường thẳng, đều neo râu trừ 2 ngoại lệ — A0) | "đánh dấu những cái điểm phản ứng của giá… đáy nó cứ cao dần" [01-13] |
| 2 | Hay **tắt MA** rồi mới nhìn trendline/mô hình | "tắt cái MA đi thì anh em cũng thấy cái trendline này" [02-27] |
| 5 | Phá rồi **về test lại** đường mà giữ được thì tin hướng mới | "break lên và về backtest lại, và tạo đáy sau cao hơn" [02-27] |
| 7 | Volume dùng để **đọc lực của cây nến**, nhất là khung nhỏ lúc vào lệnh; rất ít khi đem volume ra để xác nhận một cú phá trendline | 6/80 lần báo phá có nhắc volume/lực |
| 8 | Nến xanh volume nhỏ sau nến đỏ volume lớn là **trap** | "cây xanh này bằng khoảng 1/5 volume bán… Cú này là cú trap" [01-30] |

---

# A. CÁCH KẺ TRENDLINE

### A0. Bằng chứng ảnh: người đó thật sự kẻ thế nào
Người đó **gần như không nói điểm neo bằng lời** (chỉ 17/254 lần nhắc trendline có kèm giá điểm neo), nên ảnh chart là nguồn chính. Đã đọc ảnh chụp ±10 giây quanh **39 thời điểm** có nhắc trendline (`hoc_v5/trendline/CAN_ANH.tsv`, ảnh `so_tay/khung/<video>_<hhmmss>.jpg`), cộng 10 ảnh đã đo trước đó (`tham_chieu_anh.tsv`). Kết quả 39 thời điểm: **thấy đường thẳng kẻ bằng công cụ Trend Line: 12** · **chỉ có nét cọ vẽ tay: 8** · **không thấy đường nào trên màn hình: 19** (lời nói có, màn hình không có — chart khác, Telegram, coin khác, hoặc chưa vẽ).

**Đường thẳng (công cụ Trend Line, màu xanh ngọc), BTC:**

| Buổi · khung · giờ | Thấy gì trên ảnh | Ảnh |
|---|---|---|
| 01-12 · D1 · [00:35:08](https://www.youtube.com/watch?v=xwJagQCx1gY&t=2108s) | Kênh song song (Parallel Channel xanh lá mảnh, tô nền) dốc lên từ đáy 21/11/2025; **cạnh dưới bắt đầu ~83k, không ở râu thấp nhất ~80,6k**; cạnh trên tới ~97k. MA tắt | [ảnh](../../so_tay/khung/xwJagQCx1gY_003508.jpg) |
| 01-09 · M30 · [00:14:27](https://www.youtube.com/watch?v=YLu3KxaMspQ&t=867s) | Fibo thoái lui neo râu 89.248,3 → 91.613,9 + một đường xanh ngọc dốc xuống kéo dài sang phải; **không thấy rõ điểm neo** | [ảnh](../../so_tay/khung/YLu3KxaMspQ_001427.jpg) |
| 03-05 · H4 · [00:31:38](https://www.youtube.com/watch?v=pbr4y9qP1Ys&t=1898s) | Kháng cự giảm từ ~71,7k (06/02) nối các đỉnh thấp dần, kéo dài sang phải; **cây H4 cuối đóng vượt lên, con trỏ đặt đúng chỗ phá** | [ảnh](../../so_tay/khung/pbr4y9qP1Ys_003138.jpg) |
| 03-09 · D1 · [00:31:28](https://www.youtube.com/watch?v=-jRLufOuVEE&t=1888s) | Kênh 2 đường: **cạnh dưới neo râu đáy thấp nhất ~59,8k (06/02)** đi qua 2 râu đáy ~62,5k và ~63k; cạnh trên song song chạm râu đỉnh ~74,4k; khoanh tròn Fibo mở rộng 1.618 = 75.260,6 | [ảnh](../../so_tay/khung/-jRLufOuVEE_003128.jpg) |
| 03-09 · H4 · [00:33:02](https://www.youtube.com/watch?v=-jRLufOuVEE&t=1982s) | Cùng đường đáy từ râu ~59,8k, vẽ lại trên H4 (qua râu ~62,2k, ~63k). **Không thấy** đường "phục hồi ngắn hạn đã gãy" mà lời nói nhắc | [ảnh](../../so_tay/khung/-jRLufOuVEE_003302.jpg) |
| 03-11 · H4 · [00:43:15](https://www.youtube.com/watch?v=q-9RpBVzOhU&t=2595s) | Cùng đường đáy từ râu ~59,8k qua 3–4 râu đáy tới ~66k; **cọ vàng vẽ đường đi dự kiến: về chạm đường rồi bật lên ~74k** | [ảnh](../../so_tay/khung/q-9RpBVzOhU_004315.jpg) |
| 03-26 · D1 · [00:10:40](https://www.youtube.com/watch?v=35w3e47m3wY&t=640s) | Đường đáy từ râu ~60k (06/02) qua râu đáy ~63k, ~65,5k, ~67k; **cọ vàng ∪ đánh dấu từng lần chạm (4 chạm)** | [ảnh](../../so_tay/khung/35w3e47m3wY_001040.jpg) |
| 03-30 · D1 · [00:08:54](https://www.youtube.com/watch?v=KbxhGxmcYwg&t=534s) | Vẫn đường đó; nến D1 cuối đã đóng dưới đường, giá đang nằm sát đường từ phía dưới ("đang lên test lại trendline") | [ảnh](../../so_tay/khung/KbxhGxmcYwg_000854.jpg) |
| 04-17 · D1 · [00:17:53](https://www.youtube.com/watch?v=PH5pABMJ01k&t=1073s) | Kháng cự giảm dài **từ râu đỉnh cao nhất ~126k (06/10/2025) qua râu đỉnh ~107k (11/2025)**, kéo dài sang 2026; Fibo mở rộng (0.5 = 72.963 · 1 = 81.040 · 1.618 = 91.023,3); **mũi tên trắng: phá lên đường → lên ~81k → về test lại đường / Fibo 0.5 → lên 1.618** | [ảnh](../../so_tay/khung/PH5pABMJ01k_001753.jpg) |
| 04-20 · H4 · [00:22:38](https://www.youtube.com/watch?v=nN446WPRxPo&t=1358s) | Hỗ trợ tăng nối các râu đáy ~66k → ~68,6k → ~70,7k, kéo dài; giá đang test đường ở ~74k | [ảnh](../../so_tay/khung/nN446WPRxPo_002238.jpg) |
| 04-21 · H1 · [00:26:49](https://www.youtube.com/watch?v=AG126RfNCk4&t=1609s) | Kháng cự giảm **từ râu đỉnh cao nhất của nhịp** qua râu đỉnh thấp hơn, kéo dài sang phải; giá đã phá lên, con trỏ ở điểm phá | [ảnh](../../so_tay/khung/AG126RfNCk4_002649.jpg) |
| 06-04 · H4 · [01:05:55](https://www.youtube.com/watch?v=aPyIQ0I9e68&t=3955s) | Đường hỗ trợ gần ngang nối các đáy từ đầu năm tới 06 (~62,9k → ~61k), **đi phía trên râu thấp nhất 06/02**; giá vừa râu chạm đường. **Không thấy** đường giảm "nối đỉnh bên tay trái" mà lời nói nhắc | [ảnh](../../so_tay/khung/aPyIQ0I9e68_010555.jpg) |

**Chỉ có nét cọ (brush vàng 4px), không có đường thẳng:** 01-13 D1 [00:12:39] ∩/∪ đánh dấu đỉnh/đáy chu kỳ 2024–2025 ([ảnh](../../so_tay/khung/vg80vm31RLM_001239.jpg)) và [00:14:43] ∪ dưới 2 đáy cuối 11–12/2025 ([ảnh](../../so_tay/khung/vg80vm31RLM_001443.jpg)); 03-04 M30 [00:37:50] 3 nét ngang ~68,5k / ~67,9k / ~66,4k làm biên ([ảnh](../../so_tay/khung/OawlrpkFqQk_003750.jpg)); 03-05 M5 [01:05:23] một nét ở đáy ngang ~72,36k, không vẽ đường đỉnh ([ảnh](../../so_tay/khung/pbr4y9qP1Ys_010523.jpg)); 03-09 D1 [00:30:56] ∪ dưới 4 đáy cao dần + mũi tên lên — **30 giây sau mới kẻ đường thẳng** (ảnh 00:31:28 ở bảng trên) ([ảnh](../../so_tay/khung/-jRLufOuVEE_003056.jpg)); 03-10 M15 [00:59:27] zigzag "xuống lên xuống lên" ([ảnh](../../so_tay/khung/TXnTpUkc78s_005927.jpg)); 03-11 H4 [01:06:12] cốc + tay cầm và "trendline rộng, dài" vẽ cọ nối râu đỉnh ~79k (đầu 02) → ~74k (04/03) ([ảnh](../../so_tay/khung/q-9RpBVzOhU_010612.jpg)); 03-25 M15 [00:37:28] nét chéo từ đỉnh ~71,8k + vòng khoanh cú quét đáy ~69k + mũi tên lên ([ảnh](../../so_tay/khung/byYCWvbkZyU_003728.jpg)).

**Không thấy đường kẻ** (ghi đúng, không đoán): 01-13 H4 `vg80vm31RLM_001748`; 01-29 D1 `8NrjverKQpo_001012`; 02-02 `XD9H1FstBkE_000509/000529` (màn hình Telegram), `XD9H1FstBkE_002644` W1 (chỉ có đường ngang FIBO 0.5 87.523,5 và "TP flag" 62.309,1, không thấy neckline); 02-04 `c6WnN4Q9EXo_004635` (Diamond vẽ cọ nhưng trên **LINK** W1, không phải BTC); 02-05 `D6s6HggWgVQ_001502` (ETH), `_001522` D1 (chỉ TP flag); 03-04 H1 `OawlrpkFqQk_000545` (Fibo); 03-10 D1 `TXnTpUkc78s_002650`; 03-24 M30 `xKTPieljFuY_003639`; 03-25 H4 `byYCWvbkZyU_002046`; 03-27 `1RmIBcPxX2I_001350/001410`; 04-17 H1 `PH5pABMJ01k_002036` (hộp xám 74,8–75,6k); 04-21 H4 `AG126RfNCk4_001812`; 05-12 H4 `MsCi4yFXqZA_002107`; 05-18 W1 `phLlmyf_8-w_001814`; 06-05 `a6-MmsaBAfA_010323` (USDT.D); 06-09 H4 `UmnCq7p4NlU_000946` (Fibo + hộp vàng 0.5–0.618), H1 `_001341`; 06-10 H1 `38z3ITqKMkM_002938`, M15 `_002958`.

**Điều rút ra từ ảnh (chỉ là điều nhìn thấy):**
1. **Neo bằng râu**: mọi đường thẳng nhìn rõ đều bắt đầu ở **cực trị râu** của nhịp — hỗ trợ từ râu đáy thấp nhất (59,8k ngày 06/02), kháng cự từ râu đỉnh cao nhất (126k; 71.041,7; 74.096,7; 87,25k). Ngoại lệ: cạnh dưới kênh 01-12/01-19 và đường hỗ trợ 06-04 không đi qua râu thấp nhất.
2. **Một đường dùng nhiều buổi, nhiều khung**: đường đáy từ râu 59,8k xuất hiện ở 03-09 (D1 và H4), 03-11 (H4), 03-26 (D1), 03-30 (D1, lúc đã thủng và test lại từ dưới).
3. **Luôn kéo dài sang phải** quá giá hiện tại (04-17 kéo sang nhiều tháng).
4. **Mỗi lúc thường chỉ 1 đường thẳng**; kênh thì 2. Hay đặt cùng Fibo (thoái lui hoặc mở rộng) trên cùng chart.
5. **Đánh dấu phá / test lại**: con trỏ đặt đúng điểm phá (03-05, 04-21); mũi tên vẽ kịch bản "phá → về test lại → đi tiếp" (04-17); cọ vẽ "về chạm đường rồi bật" (03-11); cọ ∪ khoanh từng lần chạm (03-26).
6. **Thứ tự**: có lần đánh dấu đáy bằng cọ trước rồi mới kẻ đường thẳng (03-09, cách nhau ~30 giây). Khung nhỏ (M5/M15/M30) hay chỉ vẽ cọ (nét ngang, zigzag) thay vì đường thẳng.

### A1. Kẻ kháng cự giảm: nối râu đỉnh
- **Tình huống**: giá đang làm các đỉnh thấp dần (nhịp điều chỉnh / downtrend), cần biết chỗ cản và chỗ "break lên".
- **Người đó kẻ gì**: dùng công cụ Trend Line của TradingView, **neo 1 ở râu đỉnh cao nhất của nhịp**, đi qua **râu đỉnh thấp hơn kế tiếp**, rồi kéo dài sang phải (điểm neo 2 thường đặt ở vùng tương lai). Neo bằng **râu**, không bằng thân. Khung hay vẽ là H4 và D1; khi vào lệnh thì vẽ cả M5, M15, M30, H1.
  - Hiệu chỉnh máy khớp nhất với đường người đó vẽ: **`rau|3|dai|nhieu_cham`** = neo râu, đỉnh fractal 3-3, neo đầu tối đa 90 ngày (H4) / 365 ngày (D1), chọn đường có nhiều lần chạm nhất. Trên 180 buổi: khớp giá đường chính ≤0,5% 13/33 (39%), có đường khớp trong tập 24/33 (73%), khớp trạng thái 60/80 (75%); chọn trên buổi trước 07-01 rồi đo trên buổi từ 07-01: 11/17 (65%) giá chính, 29/41 (71%) trạng thái (`CHON.md`, sinh 12:37). Không biến thể "neo thân" nào lọt top 10.
- **Phá thật / giả**: xem nhóm B.
- **Kết luận + hành động**: chưa phá thì đường là cản ("trendline là một đường cản"); phá lên bằng nến đóng thì thôi short (B2).
- **Tần suất**: 70/254 lần nhắc trendline là kháng cự giảm; 29/180 buổi có nói "đỉnh thấp dần".
- **Ví dụ**:
  - **02-27** H4 · [00:29:00](https://www.youtube.com/watch?v=9wE4YYq3P6Y&t=1740s) — "Ví dụ ở đây mình tắt cái MA đi thì anh em cũng thấy cái trendline này, nhịp giảm này cũng đồng với nhịp về test trendline." · [ảnh](../../so_tay/khung/9wE4YYq3P6Y_002930.jpg): đường xanh ngọc từ râu đỉnh 71.041,7, giá đã phá lên và đang về test.
  - **03-12** H4 · [00:23:36](https://www.youtube.com/watch?v=qJZk9q5A7rA&t=1416s) — "Thì ở đây nó có một cái trendline trên. Hôm qua chúng ta chốt lãi ở cái vùng này… Nó qua khỏi 71.000 và đóng nến ở trên cái vùng này thì tức là tạo một cái đỉnh cao hơn" · [ảnh 00:27:30](../../so_tay/khung/qJZk9q5A7rA_002730.jpg): neo râu đỉnh 74.096,7.
  - **06-04** M30/H1 · [01:06:05](https://www.youtube.com/watch?v=aPyIQ0I9e68&t=3965s) — "không phá qua được đỉnh bên tay trái này thì cũng cay thật. Nó ăn ngay trendline này không lên được anh em… H1 gặp trendline đứng luôn."

### A2. Kẻ hỗ trợ tăng: nối các đáy cao dần
- **Tình huống**: giá đang hồi / tăng, các đáy sau cao hơn đáy trước; cần chỗ chờ long và mốc gãy.
- **Người đó kẻ gì**: đánh dấu các điểm giá phản ứng (cọ ∪ dưới từng đáy), rồi nối **các râu đáy cao dần**, neo đầu ở râu đáy thấp nhất của nhịp (ảnh 03-09/03-11/03-26: neo râu ~59,8k ngày 06/02; 04-20 H4: râu ~66k → ~68,6k → ~70,7k; 06-25 D1 nối 2 râu đáy ~59,1k → ~59,0k). Có thể có **trendline 1, trendline 2** song song phía dưới (02-16). Tắt MA khi kẻ.
- **Phá thật / giả**: "thủng trendline thì mới thủng hỗ trợ thôi chứ chưa phá vỡ cấu trúc xu hướng" — phải nến đóng và giao dịch dưới đường (06-30); gãy mà đáy vẫn giữ thì chưa coi là hết tăng (03-09, 07-22).
- **Kết luận + hành động**: giữ đường → chờ long gần đường, SL khi thủng đường hoặc đáy gần nhất (03-12: SL dưới 65.200; 04-07: an toàn thủng 66k, tham lam thủng 65k). Đóng H4 thủng đường → "xu hướng này nó thất bại", cấu trúc mới đỉnh đáy thấp dần (06-12).
- **Tần suất**: 66/254 lần nhắc là hỗ trợ tăng; 41/180 buổi có nói "đáy cao dần".
- **Ví dụ**:
  - **01-13** D1 · [00:14:33](https://www.youtube.com/watch?v=vg80vm31RLM&t=873s) — "Rất nhiều lần nó điều chỉnh nhưng mà nó có một cái công thức chung đó là đáy cao dần… bạn mua Bitcoin vào ngày 29 tháng 12… 87.000. Trong khi đó người khác họ mua trước đó 10 ngày… 85.000. Và người mua sau bạn khoảng độ 10 ngày… 90.000"
  - **02-16** H4 · [00:15:41](https://www.youtube.com/watch?v=0zDtKlmcydA&t=941s) — "Tiếp theo tắt MA đi. Cái đoạn này mình thấy rằng chúng ta có một vài trendline… Ban đầu nó bán lên tận 62, 60 sau đó bán lên tận 65, 66. Tiếp theo… 68 đến 69 thôi. Càng ngày cái vùng này nó càng kéo lên." · [00:17:16](https://www.youtube.com/watch?v=0zDtKlmcydA&t=1036s) — "nó về cái trendline 2 này. Thì chúng ta lại thả tiếp ở cái vùng này."
  - **04-20** H4 · [00:22:28](https://www.youtube.com/watch?v=nN446WPRxPo&t=1348s) — "nó đang đi khá nhịp nhàng theo đường trine này… nếu nó gãy khỏi cái này thì nó sẽ fail và nó đi về luôn. Còn nếu nó vẫn giữ được thì chúng ta vẫn có cơ sở để lên tiếp." · [ảnh 00:22:38](../../so_tay/khung/nN446WPRxPo_002238.jpg): đường nối 3 râu đáy, giá đang test đường.
  - **03-26** D1 · [00:10:30](https://www.youtube.com/watch?v=35w3e47m3wY&t=630s) — "Vẫn nằm trên trendline và giữ được xu hướng tăng ở trên khung ngày, xu hướng phục hồi vẫn kéo đáy đi lên" · [ảnh 00:10:40](../../so_tay/khung/35w3e47m3wY_001040.jpg): đường từ râu ~60k qua 3 râu đáy, cọ ∪ khoanh 4 lần chạm.
  - **08-17 → 08-18** H1 · [08-17 00:21:08](https://www.youtube.com/watch?v=tmR0aXnjOlA&t=1268s) — "nó kéo ba bốn cây râu nến ở H1 và test cái đường trendline này. Hiện tại H1 nó đang giữ cái xu hướng phục hồi" → [08-18 00:24:45](https://www.youtube.com/watch?v=_c0_SERWnz0&t=1485s) — "Đây chính là cái đường trend H1 này… nó test, nó rút về đây mấy cái râu nến này… Khớp trendline đi lên… không cần nhìn Fibo, vẽ mỗi cái trendline ra nhìn cũng ghê. Đi như kẻ chỉ luôn." · [ảnh 00:24:30](../../so_tay/khung/_c0_SERWnz0_002430.jpg)

### A3. Kênh song song / biên giá
- **Tình huống**: giá chạy lên xuống đều giữa hai đường.
- **Người đó kẻ gì**: công cụ **Parallel Channel** (có đường giữa nét đứt) hoặc 2 đường thẳng song song (03-09 D1: cạnh dưới neo râu đáy thấp nhất ~59,8k, cạnh trên chạm râu đỉnh ~74,4k), hoặc 2 nét cọ song song. Ở M15 có lúc chỉ vẽ zigzag bằng cọ (03-10). Ảnh 01-12/01-19 D1: neo 93.168,3 (20/11/2025) → 99.138,4 (02/02/2026); **cạnh trên chạm râu đỉnh** ~97,9k, **cạnh dưới không trùng râu thấp nhất** (`hinh_anh_1.md`). Kênh thường được gọi luôn là "mô hình cờ" (D1).
- **Phá thật / giả**: kênh cong, không còn song song, đã fail ở các đỉnh gần đây → "mô hình kênh này không còn giá trị nữa", gãy thì chỉ coi là gãy đáy (04-27).
- **Kết luận + hành động**: chạm cạnh trên → "nếu có điểm đẹp thì sell xuống" (01-19); khung nhỏ thì "ăn theo từng nhịp" trong biên (03-10 M15).
- **Tần suất**: 67/254 lần nhắc là kênh/cờ; 23/180 buổi nói "kênh giá / kênh song song".
- **Ví dụ**:
  - **01-19** D1 · [00:10:03](https://www.youtube.com/watch?v=rmCGKqaMkdw&t=603s) — "Nhìn lại khung ngày này, các bạn sẽ thấy trendline này, cái kênh giá này. Mô hình cờ, kênh giá giảm này." · [00:11:39](https://www.youtube.com/watch?v=rmCGKqaMkdw&t=699s) — "Nó lên chạm vùng trên này thì nếu có điểm đẹp thì sell xuống." · [ảnh 00:10:30](../../so_tay/khung/rmCGKqaMkdw_001030.jpg)
  - **03-10** M15 · [00:59:17](https://www.youtube.com/watch?v=TXnTpUkc78s&t=3557s) — "Xuống lên xuống lên xuống lên. Nó đi một cái biên cứ khoảng như vậy… Thì chúng ta ăn theo từng nhịp này thôi." · [ảnh 00:59:27](../../so_tay/khung/TXnTpUkc78s_005927.jpg): chỉ có zigzag vẽ cọ, không có kênh thẳng.
  - **03-09** D1 · [00:31:18](https://www.youtube.com/watch?v=-jRLufOuVEE&t=1878s) — "nếu mà nó hồi cái lực này mà hồi tốt thì nó vẫn còn khả năng chạy kênh song song này lên đến đây" · [ảnh 00:31:28](../../so_tay/khung/-jRLufOuVEE_003128.jpg): kênh 2 đường thẳng, khoanh Fibo 1.618 = 75.260,6 ở biên trên.
  - **04-27** H4 · [00:41:49](https://www.youtube.com/watch?v=9oEDyu-IfMM&t=2509s) — "Thực tế cái này chạy lâu quá rồi, mình không đánh nữa. Bây giờ nó đã bắt đầu cong cong, không còn song song nữa. Nó đã fail từ lần này và bây giờ là lần đỉnh này, mô hình kênh này không còn giá trị nữa."

### A4. Tắt MA / indicator rồi mới nhìn trendline
- **Tình huống**: chart nhiều đường MA che cấu trúc.
- **Người đó làm gì**: tắt MA (có lúc xóa hết indicator) để thấy đỉnh/đáy, trendline, vai đầu vai. Ảnh nửa cuối năm: MA gần như tắt 24/07–05/08 (1/19 ảnh có MA), trendline xuất hiện ~29/101 ảnh so với ~6/75 ảnh đầu năm (`hinh_anh_4.md`). Lý do họ tự nói (08-18): giá phản ứng với trendline tốt hơn MA trong năm 2026.
- **Kết luận + hành động**: không phải luật hướng; là cách nhìn trước khi kẻ.
- **Tần suất**: 12/180 buổi có nói "tắt MA / xóa indicator".
- **Ví dụ**:
  - **01-13** D1 · [00:11:57](https://www.youtube.com/watch?v=vg80vm31RLM&t=717s) — (nhãn: "Xóa hết indicator, chỉ giữ trend trên khung ngày; đánh dấu đáy-đỉnh").
  - **02-11** H1 · [00:03:39](https://www.youtube.com/watch?v=MZ3XfAjYHqk&t=219s) — "Khi vào H1, tắt MA đi, mọi người sẽ thấy hiện tại giá đang đi theo kiểu giảm dần về đỉnh, những đỉnh thấp dần."
  - **08-18** H1 · [00:23:51](https://www.youtube.com/watch?v=_c0_SERWnz0&t=1431s) — "ngày xưa là mình hay dùng MA… bây giờ mình vẫn dùng nhưng mà cái mức độ phản ứng của giá đối với MA hiện tại mình đánh giá không cao bằng so với cái trendline… nhìn trendline thì nó rất là ngớ ngẩn, nó rất là trẻ con… Nhưng mà giai đoạn nguyên cả cái năm 2026 này mình thấy thị trường nó phản ứng rất là tốt đối với những cái đường [trend]." · [ảnh 00:24:30](../../so_tay/khung/_c0_SERWnz0_002430.jpg)

### A5. Chọn khung
- **Tình huống**: cùng lúc có đường ở nhiều khung.
- **Kết luận + hành động**: phá đường khung tuần mới là đổi xu hướng lớn: "Cho đến khi nào cái trendline này của khung tuần nó bị mất đi thì may ra nó mới phá được cái xu hướng giảm" [07-21]. Phá ở khung nhỏ chỉ cho lệnh nhỏ: "5 phút chưa giải quyết được vấn đề gì… phải chờ… đóng những cây nến H1 hoặc H4" [03-30].
- **Ví dụ**:
  - **07-21** W1 · [00:12:58](https://www.youtube.com/watch?v=azP_1WdR-CE&t=778s) — "Trendline này nó sẽ dừng đâu đó khoảng tầm 70 đến 72, nó không qua được thì nó sẽ gãy cái trendline này nó đi xuống tiếp."
  - **03-30** M5 · [00:14:11](https://www.youtube.com/watch?v=KbxhGxmcYwg&t=851s) — "5 phút chưa giải quyết được vấn đề gì… phải chờ nỗ lực nhiều hơn nữa và đóng những cây nến H1 hoặc H4"

### A6. Đường nào đáng tin, khi nào bỏ đường cũ / vẽ lại
- **Tình huống**: trên chart có nhiều đường; một đường đã bị test nhiều lần; một mô hình chạy lần hai.
- **Người đó nói gì** (hai ý ngược nhau, ghi cả hai):
  - (b) **Test quá nhiều = hết hiệu lực**: "trendline này thì nó khó bởi vì nó test nhiều quá rồi cho nên mức độ hữu hiệu của cái trendline này nó không cao" [03-11]; đường hỗ trợ bị test lần thứ ba: "Mình thì không đánh giá cao trendline này" [06-25]; cờ chạy lần hai "mức độ hiệu quả nó không còn được giữ nữa" [03-31].
- **Bỏ / vẽ lại**: kênh cong, fail ở đỉnh → bỏ (A3, 04-27). Vẽ sai thì vẽ lại: "Cờ nó phải vẽ như này mới đúng" [01-21, [00:17:43](https://www.youtube.com/watch?v=LRkYCtbojb0&t=1063s)]; "Cờ lúc nãy vẽ còn hơi ẩu… canh từng tí một thì phải vẽ như thế mới đúng" [06-25, ảnh: vẽ lại bằng công cụ trendline nối râu đỉnh]. Vẽ lệch một chút vẫn dùng: "trendline này mình vẽ không thẳng lắm nhưng mà nó cũng vậy thôi" [03-31, [00:33:35](https://www.youtube.com/watch?v=bz8_iuwosGs&t=2015s)].
- **Tần suất**: 23/180 buổi có câu kiểu "test nhiều lần / lần thứ hai, thứ ba".
- **Ví dụ**:
  - **03-11** H4 · [00:42:03](https://www.youtube.com/watch?v=q-9RpBVzOhU&t=2523s) — "Chẳng lẽ chạy theo biên độ tiếp tục thêm một lần nữa, mình nghĩ trendline này thì nó khó bởi vì nó test nhiều quá rồi cho nên mức độ hữu hiệu của cái trendline này nó không cao."
  - **06-25** D1 · [00:15:07](https://www.youtube.com/watch?v=gy-YwzytUiA&t=907s) — "đây là lần gần như là lần thứ ba nó test vùng giá này. Và ở đây nó có một trendline nữa. Mình thì không đánh giá cao trendline này hỗ trợ cho giá lắm." · [ảnh](../../so_tay/khung/gy-YwzytUiA_001530.jpg): nối 2 râu đáy ~59,1k → ~59,0k. Vẽ lại cờ: [ảnh 01:00:30](../../so_tay/khung/gy-YwzytUiA_010030.jpg)

### A7. Trendline làm một căn cứ trong vùng hội tụ
- **Tình huống**: chọn vùng chờ vào lệnh hoặc vùng chốt.
- **Người đó làm gì**: trendline được cộng với Fibo / MA / đỉnh cũ / gap; vùng nhiều thứ trùng nhau mới chờ. Trong thống kê mốc của sổ tay tinh hoa, trendline là căn cứ của 112 mốc; tỉ trọng mốc có trendline: tháng 1 2%, tháng 7 5%, **tháng 8 8%**, tháng 10 5% (`SO_TAY_TINH_HOA.md` A4.1, A7).
- **Kết luận + hành động**: "Nhiều phương pháp vẫn cho chung một kết quả thì… chờ ở đây cho chắc kèo" [01-09].
- **Ví dụ**:
  - **01-09** M30 · [00:14:17](https://www.youtube.com/watch?v=YLu3KxaMspQ&t=857s) — "Nếu đánh theo back test nhịp này khung nhỏ 30 phút, nếu đánh trendline thì khả năng cũng chung một kết quả. Nhiều phương pháp vẫn cho chung một kết quả thì có thể là anh em chúng ta chờ ở đây cho chắc kèo." · [ảnh](../../so_tay/khung/YLu3KxaMspQ_001407.jpg)
  - **03-23** D1 · [00:41:51](https://www.youtube.com/watch?v=bSnFyHqyo5c&t=2511s) — "Vùng 68 này đang là vùng hỗ trợ cứng. Vừa là hỗ trợ trendline của khung ngày, vừa là hỗ trợ của H4 Fibo."
  - **08-12** H1 · [00:11:47](https://www.youtube.com/watch?v=EaWaSL7aWT4&t=707s) — "Scalp ngắn mình kỳ vọng nó quét lên khoảng 64, tức Fibo 0.618… Trendline cũng có một cản ở khoảng 64. Nhịp này có lẽ chúng ta sẽ chờ ở 64."

---

# B. PHÁ TRENDLINE

Thống kê trạng thái người đó báo khi nhắc trendline (254 lần): chưa phá 90 · đang giữ 77 · vừa phá 55 · phá rồi test lại 25 · tự gọi là phá giả 3. Trong 194 lần có nêu điều kiện phá, **57 lần ghi rõ "đóng (nến/cửa)"**.

### B1. Phá thật = nến đóng cửa qua đường; râu không tính
- **Tình huống**: giá chọc qua trendline.
- **Người đó nhìn gì**: **giá đóng nến** của khung đang xét (H4 là chính; H1/M30 khi scalp; D1/W1 với đường khung lớn). Râu không tính. Một cây đóng qua mới là **điều kiện cần**; **điều kiện đủ** là cây thứ hai cùng phía, hoặc test lại rồi đi tiếp.
- **Kết luận + hành động**: xem B2. Mốc sai / SL cũng đặt theo nến đóng: "có bất kỳ cây nến H4 nào đóng cửa, phải nhớ từ đóng cửa chứ không tính cái râu" [03-04].
- **Tần suất**: 57/194 điều kiện phá có chữ "đóng"; 27/180 buổi nói "hai cây H4 / thêm một cây H4"; 3/180 buổi nói thẳng "không tính râu".
- **Ví dụ**:
  - **04-07** D1 · [00:14:43](https://www.youtube.com/watch?v=HeBpJr0i6Bg&t=883s) — "Có một cái tín hiệu tốt đó là nó break ra được khỏi cái trend giảm này… Chúng ta không biết là nó có fake hay không nhưng mà… điều kiện cần là break ra là đã đủ rồi… Còn bây giờ chúng ta thiếu cái điều kiện đủ nữa thôi. Test lại và break lên tiếp."
  - **07-21** H4 · [00:17:12](https://www.youtube.com/watch?v=azP_1WdR-CE&t=1032s) — "H4 thì như hiện tại nó đã break ra khỏi cái trendline này… Nhưng để chắc hơn thì bây giờ có lẽ chúng ta nên chờ thêm một cây H4 nữa"
  - **07-31** H4 · [00:10:02](https://www.youtube.com/watch?v=SlGyokVNofU&t=602s) — "khoảng ba bốn cây nến tạo râu và không qua được vùng trend line… Vùng này bây giờ gặp cản thì miễn sao giá break lên trên khỏi thằng này và đóng H4 vượt qua và confirm với đó" (nhãn: confirm bằng nến D1 đóng)
  - **06-30** M30 · [00:21:54](https://www.youtube.com/watch?v=h3mwuQrqabM&t=1314s) — "nếu nó thủng khỏi trendline này thì chưa đâu, bởi vì thủng trendline thì mới thủng hỗ trợ thôi chứ chưa phá vỡ cấu trúc xu hướng. Nó phải xuyên qua khỏi 30 phút và bắt đầu đóng nến và giao dịch ở dưới này"

### B2. Sau phá thật: đổi phe / ngừng đánh ngược
- **Tình huống**: nến đã đóng qua đường.
- **Người đó làm gì**: phá kháng cự giảm → **không short nữa**, tìm long khi về test; phá hỗ trợ tăng → **xu hướng tăng thất bại**, short thuận xu hướng. Phá mô hình khung lớn (cờ D1, vai đầu vai W1) → đi theo đích của mô hình (D1, D2).
- **Phá thật / giả**: như B1.
- **Tần suất**: 55 + 25 = 80 lần báo "vừa phá / phá rồi test lại".
- **Ví dụ**:
  - **03-05** H4 · [00:31:28](https://www.youtube.com/watch?v=pbr4y9qP1Ys&t=1888s) — "mọi người đo trend line và cây H4 này đã break ra khỏi trend line, phá lên. Dưới này cũng trend line và nó đảo chiều. Chúng ta đâu có lý do gì để đi short ở đây." · [ảnh 00:31:38](../../so_tay/khung/pbr4y9qP1Ys_003138.jpg): cây H4 cuối đóng vượt đường kháng cự giảm, con trỏ ở điểm phá.
  - **06-12** H4 · [00:27:12](https://www.youtube.com/watch?v=x75V4Kb1fj4&t=1632s) — "Nếu mà H4 đóng thủng khỏi cái này, thủng khỏi trend line này thì coi như là xu hướng này nó thất bại… lúc này bắt đầu tạo ra một cấu trúc mới. Cấu trúc sóng giảm đỉnh đáy sau thấp hơn trước ở trong H4."
  - **08-06** H4 · [00:14:09](https://www.youtube.com/watch?v=_Ypby-_iFsg&t=849s) — "Bây giờ anh em vào H4 thì rõ ràng thấy nó đã phá qua trendline này. Một lý do nữa chúng ta không giữ cố lệnh short là vì nó đã phá qua trendline."
  - **07-28** D1 (hỗ trợ gãy, họ nhận sai) · [00:04:18](https://www.youtube.com/watch?v=1wDQbk0akZs&t=258s) — "cái đường trendline này rất là dễ để giúp cho giá đi lên… Bị dính cái này thì cái plan đi lên của mình nó đã bị fail rồi… bây giờ đã có câu trả lời là cái plan của anh em đúng và cái plan của mình nó không có đúng." (nhãn: nến D1 nhấn chìm gãy xu hướng tăng)

### B3. Phá + volume (lực của cây nến phá)
- **Tình huống**: cây nến phá trendline có / không có lực.
- **Người đó nhìn gì**: khi có nhắc, họ nói về **lực của cây nến** ("cây nến H4 khá đẹp, khá lực", "full lực bán", "lực mua không bẻ được") nhiều hơn là con số volume. Ở khung M1–M5 khi scalp thì họ đòi volume mua đi kèm cú break.
- **Đo bằng máy** (`volume_pha.tsv`, volume nến H4 phá / TB 20 nến trước, chỉ ghi, không dùng để chọn đường): trong 41 lần người đó gọi là phá thật so được: ≥1,2× TB: 14 · 0,8–1,2×: 3 · <0,8×: 8 · máy không thấy cú phá: 16. Lần người đó gọi phá giả có số liệu: 0.
- **Kết luận + hành động**: không có câu nào của họ nói "phá trendline mà không có volume thì là phá giả". Khi họ nhắc lực/volume lúc phá, nó đi cùng hướng với kết luận phá thật (01-21, 05-04) hoặc là lý do bỏ hy vọng "trap" (06-24).
- **Ví dụ**:
  - **01-21** D1 · [00:17:43](https://www.youtube.com/watch?v=LRkYCtbojb0&t=1063s) — "Hiện tại nó đã break out rồi, đã break ra khỏi trendline này rồi… Anh em nhìn cây nến ngày như thế này mà đòi đi long thì chắc cũng nát người. Nhìn volume này, volume lớn chứ đâu phải ít. Và đóng một cây full lực bán như thế này. Thủng tất cả hỗ trợ rồi."
  - **05-04** H4 · [00:26:33](https://www.youtube.com/watch?v=VUUbKp4bFSU&t=1593s) — "trước đó nó đã tạo một xu hướng điều chỉnh đỉnh đáy thấp dần. Nhưng về đến vùng này bắt đầu nó kéo lên và nó break qua được cản đầu tiên là trend line với một cây nến H4 khá đẹp, khá lực."
  - **03-03** M1/M5 · [00:25:20](https://www.youtube.com/watch?v=xXKnEs9z81g&t=1520s) — "Nó break qua được nhịp này thì M1 này. Break qua được cái đoạn này thì chơi được. Một trendline, hai trendline. Đang thiếu volume mua. Volume bán nó nhảy vào rất nhanh."
  - **08-06** · [00:20:41](https://www.youtube.com/watch?v=_Ypby-_iFsg&t=1241s) — "chưa phá lên được khỏi trendline này. Lúc nãy mình kỳ vọng nó sẽ phá lên nhưng vẫn chưa phá được thì chúng ta cứ chờ. Volume mua đoạn này vẫn đang nhảy vào và áp đảo."

### B4. Phá rồi test lại (backtest) → giữ hướng mới
- **Tình huống**: sau cú phá, giá quay về chạm lại đường.
- **Người đó nhìn gì**: giá về đúng đường rồi bật đi theo hướng phá, hoặc tạo đáy/đỉnh mới theo hướng phá. Neckline vai đầu vai cũng được test lại theo cách này.
- **Phá thật / giả**: test lại thất bại (không lấy lại được phía cũ) = **break thật** (01-26). Đang backtest mà đáy sau cao hơn = tiếp tục hướng phá (02-27).
- **Kết luận + hành động**: không đánh ngược trong lúc backtest ("Cho nên đoạn này tốt nhất là chưa nên short" [02-27]); muốn long sau phá thì chờ phá + về test mới vào (06-10, 07-13 cờ: "các bạn phải chờ breakout và xác nhận. Lên đây, backtest ở đây, và đi lên, lúc đó chúng ta mới vào lệnh" [[00:08:31](https://www.youtube.com/watch?v=O3q2fmXlwhk&t=511s)]).
- **Tần suất**: 25/254 lần nhắc trendline ở trạng thái "phá rồi test lại"; 85/180 buổi nói "backtest / test lại".
- **Ví dụ**:
  - **01-26** D1 · [00:07:21](https://www.youtube.com/watch?v=KZ3cHk9a3yc&t=441s) — "có một cái đường trend line, cái kênh giá này hôm trước mình vẽ từ lúc nó chưa break ra… Nó chỉ kéo lên đúng cái đường trend line này khoảng 91 đêm ngày thứ sáu, là có một pha quét lên đúng 91 luôn và nó rớt xuống… Mô hình cờ, break rồi."
  - **02-27** H4 · [00:29:00](https://www.youtube.com/watch?v=9wE4YYq3P6Y&t=1740s) — "Coi như là đôi khi đây là một nhịp break lên và về backtest lại, và tạo đáy sau cao hơn để tiếp tục xu hướng phục hồi. Cho nên đoạn này tốt nhất là chưa nên short." · [ảnh](../../so_tay/khung/9wE4YYq3P6Y_002930.jpg)
  - **06-23** H4 · [00:20:23](https://www.youtube.com/watch?v=w3K-VXD_Tns&t=1223s) — "nó cũng là một nhịp break trendline ở đây và đang backtest, nên hoàn toàn có thể đây là nhịp backtest và tiếp tục đi lên. Củng cố thêm lý do vì sao mình không short."
  - **04-17** D1 · [00:17:43](https://www.youtube.com/watch?v=PH5pABMJ01k&t=1063s) — "Ví dụ nó đi kênh giá thì đợt này nó sẽ lên đến vùng này nó cũng hợp lý hóa cái kênh giá đúng không?" · [ảnh 00:17:53](../../so_tay/khung/PH5pABMJ01k_001753.jpg): **mũi tên vẽ tay "phá lên đường kháng cự từ râu 126k → lên ~81k → về test lại đường / Fibo 0.5 72.963 → đi lên Fibo 1.618 91.023"**.
  - **03-30** D1 · [00:08:44](https://www.youtube.com/watch?v=KbxhGxmcYwg&t=524s) — "hôm qua nó đóng một cây nến ngày ở vùng này nhưng cây này không có ý nghĩa nhiều lắm, ngoài câu chuyện hiện tại giá đang lên test lại trendline này. Còn thực sự xu hướng khung ngày này gần như sắp gãy." · [ảnh 00:08:54](../../so_tay/khung/KbxhGxmcYwg_000854.jpg): đường hỗ trợ từ râu ~60k, nến D1 cuối đã đóng dưới, giá sát đường từ dưới.
  - **06-22** H4 · [00:13:52](https://www.youtube.com/watch?v=eaj9NEm85O4&t=832s) — "Điểm này là điểm bất thường, thông thường nó test ở đây trendline sau cây nến đỏ này là không bao giờ nó lên test lần hai. Nó sẽ đi luôn bởi vì nó chỉ test một lần thôi." (nhãn gọi là phá giả)
  - **07-27** H1 · [00:21:51](https://www.youtube.com/watch?v=YMlDceykaTw&t=1311s) — "Ngắn hạn thì ở đây trendline mình đang thấy nó đã break trendline rồi, thì lúc sáng mình đang chờ nó về đến đoạn này thì mình sẽ vào"

### B5. Phá giả / chưa tin
- **Tình huống**: giá vừa vượt đường, hoặc vượt rồi quay lại, hoặc giá đang đi ngang trong hộp.
- **Người đó nhìn gì**: (1) nến **chưa đóng** mà đã vượt; (2) nến phá để lại **râu** rồi quay về; (3) cây sau đóng ngược lại (D1 đóng xanh lại sau khi thủng); (4) bối cảnh **hộp đi ngang** (D7); (5) lực phía bên kia có bẻ lại được không.
- **Phá thật / giả**: họ gọi "fake out / trap" khi giá chọc qua rồi quay lại nhanh, thường kèm cây volume lớn ở khung nhỏ (07-01). Ngược lại, có lần họ mong là trap nhưng lực không bẻ lại được → nhận là thủng thật (06-24).
- **Tần suất**: 106/180 buổi có nói "fake / trap / dụ / đánh lừa" (mọi ngữ cảnh, không chỉ trendline); 3 lần nhắc trendline được họ gọi thẳng là phá giả.
- **Ví dụ**:
  - **01-22** D1 · [00:12:58](https://www.youtube.com/watch?v=WvCOBcm0bd0&t=778s) — "Rõ ràng ở khung ngày thì anh em thấy là nó đã phá qua, thủng trend line, đóng một cây nến ngày tiếp theo có màu xanh." (nhãn: nến D1 hôm nay xanh nữa thì có thể fake out; đỏ đấm sâu thì đi 7x–6x)
  - **06-24** H4 · [00:15:54](https://www.youtube.com/watch?v=ZrqOEgiFEF8&t=954s) — "Tối ngày thứ hai chúng ta còn hy vọng là thị trường nó trap cái nhịp này trendline. Nhưng mà rõ ràng là gì? Lực mua không nổi, lực mua yếu quá không có bẻ được cái chart này, không có bẻ được xu hướng."
  - **07-01** M5 · [00:21:36](https://www.youtube.com/watch?v=WNiQnpm2BLo&t=1296s) — "có một cây volume rất lớn 5 phút nó break out và nhanh chóng rút lên. Mình đang đánh giá nhịp này là nhịp quét stop loss của phe long trước khi tăng cũng như là một nhịp fake out"
  - **08-10** H4 · [01:02:34](https://www.youtube.com/watch?v=8BGhoFetSaU&t=3754s) — "Đẹp nhất là cứ phải chờ nó về đến vùng này, 63.000 hay 64.000… Đừng thấy nó thủng trendline này mà cứ cố cắm đầu xuống tận dưới. Đôi khi nó thủng kỹ thuật thôi… H4 của nó vẫn giữ xu hướng tăng"
  - **04-01** D1 · [00:32:08](https://www.youtube.com/watch?v=Be-e74Mwx0U&t=1928s) — "Mình đang sợ là nó trap cho anh em short… Backtest ở trên mô hình cờ này. Break down và đang backtest lên. Đoạn này nếu các bạn đánh theo mô hình này thì các bạn sẽ đánh short ở vùng khoảng 69."

### B6. Giá chạm trendline nhưng chưa phá
- **Tình huống**: giá về chạm đường hỗ trợ, hoặc lên chạm đường kháng cự.
- **Kết luận + hành động**: hỗ trợ: "Nếu mà anh em nào muốn chơi muốn chờ trendline thì đoạn này vẫn có thể chờ lại ở cái vùng này… SL chỉ cần đặt ở dưới khoảng 65.200" [03-12]; "Đừng có gãy khỏi cái trendline này là ok thôi… SL khi nào nó thủng khỏi, nếu an toàn thủng 66.000 hoặc… tham lam… 65.000" [04-07]. Kháng cự: "Đường trendline nó lên test đúng ở đó nó gãy thì bình thường… Nhưng không có nghĩa là nó đi như thế này chúng ta vào short" [06-23].
- **Tần suất**: 77 + 90 lần nhắc trendline ở trạng thái đang giữ / chưa phá.
- **Ví dụ**:
  - **03-24** D1 · [00:21:23](https://www.youtube.com/watch?v=xKTPieljFuY&t=1283s) — "Về phân tích kỹ thuật, giá chạm khẽ trendline ở đằng dưới này, thêm một cái rất đẹp nữa là vùng 67.000 này, hôm qua trên livestream mình đã nói."
  - **06-03** khung nhỏ · [01:09:11](https://www.youtube.com/watch?v=OVGlvdAXMKo&t=4151s) — "lúc nãy mình có vẽ trendline này ra cho các bạn. Mình bảo nếu có chờ thì chờ ở trendline này. Đúng là khớp ngay ở đoạn này. Bắt được một tí."
  - **04-02** H4 · [00:05:29](https://www.youtube.com/watch?v=orDQVRuxI1E&t=329s) — "Đây thì vẫn bị đạp ở trendline cho nên là cái đoạn này thì gãy cũng bình thường thôi… đây là một cái vùng trendline là một cái vùng kháng cự." · [ảnh](../../so_tay/khung/orDQVRuxI1E_000530.jpg)
  - **06-23** · [00:40:05](https://www.youtube.com/watch?v=w3K-VXD_Tns&t=2405s) — "Đường trendline nó lên test đúng ở đó nó gãy thì bình thường. Bản chất là trendline thôi, trendline là một đường cản… Nhưng không có nghĩa là nó đi như thế này chúng ta vào short."
  - **07-27** H1 · [00:19:46](https://www.youtube.com/watch?v=YMlDceykaTw&t=1186s) — "hiện tại giá đang nằm ở trendline này cho nên long rất nguy hiểm. Điều này không sai… trendline này không sai, nhưng nếu chúng ta short ở đây là không đúng… Gặp cản thì bị bán xuống nhưng không có nghĩa là nó không lên tiếp được."

- Thêm (ảnh): **03-11** H4 · [00:42:03](https://www.youtube.com/watch?v=q-9RpBVzOhU&t=2523s) — "Chẳng lẽ tầm này market nó vẫn chạy tiếp cái trendline này thì về đâu đó khoảng 66.000. Rồi lại bật lên đâu đó khoảng độ 74." · [ảnh 00:43:15](../../so_tay/khung/q-9RpBVzOhU_004315.jpg): cọ vẽ đường đi về chạm đường đáy (~66k) rồi bật lên ~74k.

### B7. Qua trendline nhưng còn cản khác → chưa tính là break
- **Tình huống**: giá vượt trendline nhưng ngay trên/dưới còn đỉnh cũ, cản ngang, MA, hoặc trendline thứ hai.
- **Người đó nhìn gì**: đếm các "lớp cản" còn lại; phá trendline phải kèm vượt đỉnh bên trái / vùng ngang mới tính là đổi cấu trúc.
- **Kết luận + hành động**: "muốn đánh được long thực sự thì sẽ phải chờ nó break ra khỏi trendline này" và vượt "ít nhất một đỉnh mới" rồi về test [06-10]; H4 đã break "Còn mỗi cái trend line cao này thôi" [07-10]; cốc tay cầm chỉ có giá trị khi "đi qua khỏi trend line" [03-11].
- **Ví dụ**:
  - **02-26** H4 · [00:38:34](https://www.youtube.com/watch?v=7zFMbvqo3QI&t=2314s) — "H4 bắt đầu có xu hướng đảo chiều. Thứ nhất là nó phá qua trend này. Thứ hai là giá đang vượt qua được MA89, thường nó sẽ có xu hướng đi tiếp MA200."
  - **06-10** M30 · [00:29:48](https://www.youtube.com/watch?v=38z3ITqKMkM&t=1788s) — "Trendline này thực tế đang chạy theo MA… muốn đánh được long thực sự thì sẽ phải chờ nó break ra khỏi trendline này. Tức là break ra khỏi xu hướng giảm này thì mới an toàn." (ảnh ±10 giây `38z3ITqKMkM_002938` H1 và `_002958` M15: **không thấy** đường kẻ)
  - **07-10** H4 · [01:06:18](https://www.youtube.com/watch?v=QwYznPgaAFY&t=3978s) — "Trên H4 thì nó break rồi. Còn mỗi cái trend line cao này thôi, còn mỗi trendline ở trên cao này thôi."

---

# C. ĐỌC NẾN + VOLUME

Số liệu: 1252 câu nói về nến trong nhãn, 268 câu có nhắc volume (128/180 buổi). Khung của câu có volume: H4 69 · H1 37 · M30 14 · M15 22 · M5 35 · D1 36 · W1 6. Chỉ báo volume trên chart là **FxCanli_Volume_Hacim** (3 vạch vàng mép phải) đặt ở đáy chart (`SO_TAY_TINH_HOA.md` D3).

### C1. Vùng giá = điều kiện cần; nến đảo chiều + volume ở khung nhỏ = điều kiện đủ
- **Tình huống**: giá về vùng chờ (Fibo, trendline, hỗ trợ).
- **Người đó nhìn gì**: vào M5/M15/M30 tìm **nến rút chân / rút lên xanh**, **volume mua vượt** các cây trước, không tạo đáy thấp hơn.
- **Kết luận + hành động**: có nến đẹp + volume mua → vào; "Còn nếu thấy lực [xả liên tục]" → không vào (03-25); nhãn 03-05: nến bán đâm thủng thì bỏ entry.
- **Tần suất**: 54/180 buổi nói "rút chân / rút râu / nến rút".
- **Ví dụ**:
  - **03-25** M5/M15 · [00:27:54](https://www.youtube.com/watch?v=byYCWvbkZyU&t=1674s) — "xác định vùng giá nó chỉ là điều kiện cần thôi. Còn điều kiện đủ là gì? Nó phải tạo được những cây nến đảo chiều… khung nhỏ 5 phút, 15 phút gì đó mà thấy có những cây nến rất đẹp. Cộng với đó là volume mua hoặc các tín hiệu đảo chiều đẹp thì lúc đó chúng ta mới có thể nhảy vào."
  - **02-03** M5 · [00:45:15](https://www.youtube.com/watch?v=ewRoIMVREvw&t=2715s) — "Nếu hồi về 769 thì 765 rồi chờ xem hình thái nến M5 rút chân kèm khối lượng mới vào long. Cơ bản thì có hình thái nến rút lên xanh là cũng được rồi. Bởi vì về dưới đó thì đôi khi khối lượng nó cũng duy trì."
  - **01-07** M5 · [00:28:00](https://www.youtube.com/watch?v=NOBgwE4Gdko&t=1680s) — "Cây M5 này còn tạm tạm là vào cái vol nhỏ này bởi vì volume mua nó bắt đầu vượt trội hơn so với những volume mở trước này."

### C2. Râu nến: "râu sinh ra để test"; râu không uy tín khi không có lực; thân quan trọng hơn râu
- **Tình huống**: nến để lại râu dài ở hỗ trợ/kháng cự.
- **Người đó nhìn gì**: râu có kèm lực (volume) bên đúng phía không; thân nến đã phá vùng chưa.
- **Kết luận + hành động**: râu rút chân mà lực bán vẫn áp đảo → râu sẽ bị test lại, không tin (01-08). H4 có râu nhưng volume yếu → "không có uy tín" (04-01). Thân nến phá vùng thì râu chỉ là test (06-08 W1). Nhiều râu mà chưa có cây xả mạnh → chưa thấy cửa hồi (06-26).
- **Tần suất**: 65/180 buổi có câu "râu… test / test… râu".
- **Ví dụ**:
  - **01-08** H4 · [00:14:51](https://www.youtube.com/watch?v=jX-0Hgy1S0E&t=891s) — "H4 nó tạo cái râu này. Rút chân ở đây. Test lên đi lên một cây và bật volume lên. Chúng ta thấy lực mua với lực bán này thì rõ ràng lực bán áp đảo và cái râu nến này thì khả năng về test rất cao rồi."
  - **04-01** H1/H4 · [00:59:12](https://www.youtube.com/watch?v=Be-e74Mwx0U&t=3552s) — "Cây H1 này của Bitcoin khá là mạnh nhưng mà volume yếu quá. H4 thì vẫn là tạo một cái râu nhưng mà râu như này thì không có uy tín tí nào."
  - **03-19** M30 · [01:09:28](https://www.youtube.com/watch?v=mBEBKzBb4kU&t=4168s) — "Râu này sinh ra là để test xu hướng. Đây là xu hướng đang ở hỗ trợ H4."
  - **06-08** W1 · [00:19:06](https://www.youtube.com/watch?v=WZ8PpZ9VA4Q&t=1146s) — "Nhìn thân nến này, các bạn nhìn râu nến thì có thể là test nhưng thân nến này đã phá vỡ vùng hỗ trợ quan trọng… vùng này chỉ cần một cây nến là nó phá qua. Lực bán ở đây cực kỳ kinh khủng" · [ảnh](../../so_tay/khung/WZ8PpZ9VA4Q_001930.jpg)

### C3. Nến tăng mà volume thấp → trap / hồi yếu / kill short
- **Tình huống**: xuất hiện nến xanh đẹp (đảo chiều theo sách) hoặc giá kéo lên.
- **Người đó nhìn gì**: so volume cây xanh với các cây đỏ trước nó; xem lên "có lực" hay "yếu ớt".
- **Kết luận + hành động**: volume cây xanh nhỏ hơn hẳn → trap, không long; kéo lên không volume → chỉ hồi kỹ thuật / kill short, không FOMO.
- **Tần suất**: 52/180 buổi có câu "volume yếu / không có volume / thiếu volume / thanh khoản yếu".
- **Ví dụ**:
  - **01-30** H4 · [00:09:53](https://www.youtube.com/watch?v=4PUqxjVBR4M&t=593s) — "Nhìn một cây H4 màu xanh kẹp sau một cây màu đỏ như này, ông nào học lý thuyết nến đảo chiều thì chắc chắn dính cú này nếu không nhìn volume. Các bạn thấy volume bán áp đảo không? Hai cây đỏ, cây xanh này bằng khoảng 1/5 volume bán. Cho nên để đảo chiều được thì hơi khó. Cú này là cú trap." · [ảnh](../../so_tay/khung/4PUqxjVBR4M_000930.jpg)
  - **05-11** H4 · [00:26:53](https://www.youtube.com/watch?v=jm7VS-lKW8w&t=1613s) — "Nó kéo một cây H4 rất là đẹp như này. Nhưng mà nhìn volume này. Cũng có nhưng mà không phải là quá xuất sắc… volume này cũng thuộc loại dụ cũng ác… Vì sao mình không long ở đoạn này? Bởi vì mình biết nhịp này nó lên để nó kill short."
  - **06-10** M30 · [00:27:35](https://www.youtube.com/watch?v=38z3ITqKMkM&t=1655s) — "Nó trên mà nhìn cao to đẹp trai vạm vỡ, lực lưỡng, có sức khỏe thì chơi, chứ nó trên mà kiểu yếu ớt như thế này chơi làm gì. Volume này yếu đuối như thế này thì chơi làm gì cho mệt."
  - **01-13** M30 · [00:32:02](https://www.youtube.com/watch?v=vg80vm31RLM&t=1922s) — "Cây 30 phút này xanh nhưng không có volume. Thị trường không có thanh khoản, rất yếu."

### C4. Nến bán lớn + volume lớn: sau nhịp tăng là xấu, sau nhịp giảm dài là gần cạn
- **Tình huống**: cây đỏ thân dài, volume lớn.
- **Người đó nhìn gì**: **vị trí** của cây đó trong sóng (sau tăng hay sau một chuỗi giảm dài) và có phân kỳ không.
- **Kết luận + hành động**: sau tăng / giữa xu hướng → khó hồi ngay, không long ("Về cơ bản volume như cây này, cây nến màu đỏ và volume đỏ lớn thì gần như rất khó để hồi" [01-20]). Sau chuỗi giảm dài → "nhịp dốc sức gần cuối", sắp hồi; nhưng **không mua ở cây xanh ngay sau**, chờ test lại đáy rồi chia nhỏ (04-13, theo nhãn). Short lúc đó "không phải là lựa chọn sáng suốt" (06-04).
- **Tần suất**: 40/180 buổi có câu "volume lớn / khủng / đột biến / cột to"; 16/180 buổi nói "full lực".
- **Ví dụ**:
  - **03-02** tháng · [00:19:19](https://www.youtube.com/watch?v=GYgaZiYqRXY&t=1159s) — "Nến bán sau một nhịp tăng là nến cực kỳ xấu. Nhưng nến bán mạnh kèm volume lớn trong một nhịp đã giảm rất lâu trước đó thì gần như là nhịp dốc sức gần cuối, hoặc sau đó nó muốn giảm tiếp thì phải hồi lên lấy sức rồi mới tiếp tục nhịp mới."
  - **04-13** D1 · [00:57:23](https://www.youtube.com/watch?v=Fvz3aEsoOEE&t=3443s) — "Thứ nhất là trước đó là một nhịp bán, thứ hai là một cây nến đỏ kèm với khối lượng bán cực kỳ khủng. Đây là khả năng tạo đáy" (nhãn: không mua ở nến xanh mà chờ test lại đáy rồi chia nhỏ mua)
  - **06-04** H4 · [00:16:56](https://www.youtube.com/watch?v=59zOmIM_EOM&t=1016s) — "Nến nhấn chìm rất là đẹp luôn nhưng mà nó vẫn cắm xuống là cắm xuống. Phân kỳ hiện tại thì đang phân kỳ H4 với lại volume lớn như thế này thì mình nghĩ là nó sẽ khó để xả tiếp… Bắt buộc nó phải hồi thì nó mới có lực để xả. Cho nên tầm này nếu các bạn lựa chọn short thì mình nghĩ không phải là lựa chọn sáng suốt."
  - **01-20** H4 · [00:33:11](https://www.youtube.com/watch?v=GygVJDmjlgY&t=1991s) — "một cây H4 màu đỏ kèm volume bán lớn thì không thể nào tăng tiếp ngay lập tức được. Sau đó đi kèm với một cây có rút chân, có volume bán lớn vượt trội thì mới có khả năng hồi nhẹ một tí."

### C5. Nến bán volume thấp → chỉ là điều chỉnh, dễ hồi
- **Tình huống**: nến đỏ nhưng volume bán bình thường / thấp hơn các ngày trước.
- **Kết luận + hành động**: "xét theo volume thì nó không phải là xấu" [04-07]; "mang tính điều chỉnh là cao" [04-13]; "Vùng này rất dễ hồi… chủ yếu để quét stop loss của các anh em short" [07-01]. Không phải tín hiệu short đuổi.
- **Ví dụ**:
  - **04-07** D1 · [00:09:53](https://www.youtube.com/watch?v=HeBpJr0i6Bg&t=593s) — "Cái volume bán này so với những ngày trước thì cũng bình thường chứ không phải là cao đâu. Trước đó volume mua rất là nhiều… Nếu xét theo volume thì nó không phải là xấu đâu."
  - **04-13** D1 · [00:16:34](https://www.youtube.com/watch?v=Fvz3aEsoOEE&t=994s) — "khung ngày D1 có cây màu đỏ lực bán. Nhưng các bạn thấy lực bán này đâu có quá lớn… Cho nên mang tính điều chỉnh là cao."
  - **07-01** D1 · [00:15:39](https://www.youtube.com/watch?v=WNiQnpm2BLo&t=939s) — "Vẫn là một cây nến bán. Nhưng nến bán này thì volume không nhiều. Vùng này rất dễ hồi… hồi lên chủ yếu để quét stop loss của các anh em short dưới đáy này thôi."

### C6. Cây volume đột biến: vào SAU cây đó; lực xả phải bị triệt tiêu / hấp thụ
- **Tình huống**: sau một nhịp xả, xuất hiện cây volume mua đột biến; hoặc đang xả mà muốn bắt đáy.
- **Người đó nhìn gì**: phải thấy một cây volume lớn nhảy vào trước; sau đó lực xả phải bị triệt tiêu (nến mua hấp thụ, phá lên trên các ngày bán). Cụm nến mua lớn thường bị điều chỉnh sâu về Fibo 0.618–0.786 của nhịp trước.
- **Kết luận + hành động**: không bắt đáy trước cây volume; vào sau cây đó và chờ giá về test lại (02-26). Sau cụm mua lớn "Đừng FOMO long market, chờ về" (03-10).
- **Tần suất**: 14/180 buổi nói "triệt tiêu / hấp thụ".
- **Ví dụ**:
  - **02-26** D1 · [00:16:42](https://www.youtube.com/watch?v=7zFMbvqo3QI&t=1002s) — "Về nguyên tắc nếu anh em long thì phải vào sau khi cây nến này. Sau cây có volume đột biến thì chúng ta mới nhảy vào để long như cái nhịp ngày hôm qua. Sau lên 66 nó về test lại 64"
  - **03-05** M30 · [00:40:51](https://www.youtube.com/watch?v=pbr4y9qP1Ys&t=2451s) — "cần một điều kiện là phải có một nến đẹp và lực mua nhảy vào… Muốn biết lực mua phải nhìn vào volume. Hoặc đi vào 5 phút khung nhỏ… Nhưng chờ một cây volume lớn nhảy vào trước" (nhãn: sau cây volume lớn thường có lực xả, lực xả phải bị triệt tiêu)
  - **03-19** D1 · [00:38:28](https://www.youtube.com/watch?v=mBEBKzBb4kU&t=2308s) — "hai cây nến D1 bán xuống thì rõ ràng chúng ta không có bất kỳ cơ sở nào để nghĩ rằng đoạn này có thể hồi lên… đến ngày kế tiếp chúng ta thấy có một lực mua đột biến kéo cây đến ngày này phá lên trên khỏi hai ngày vừa…"
  - **03-10** M30 · [00:34:53](https://www.youtube.com/watch?v=TXnTpUkc78s&t=2093s) — "Xuất hiện những cái cụm mua lớn có lực nhảy vào thì sau đó đều điều chỉnh sâu gần như là về lại gần bằng với cái đáy trước. Nó chỉ về đến độ khoảng Fibo 786 của cái đáy trước đó trong cái khung nhỏ."

### C7. Volume giảm khi giá tăng (phân kỳ volume); combo RSI–volume–nến; phân kỳ ≠ đảo chiều
- **Tình huống**: giá đi lên nhưng volume (và RSI) yếu dần; hoặc giá phá đáy mà RSI không phá.
- **Người đó nhìn gì**: volume theo **cả quá trình**, không chỉ 1–2 cây (05-05). RSI và volume cùng phân kỳ ở đỉnh.
- **Tần suất**: 38/180 buổi nói "phân kỳ"; 47/180 buổi nói RSI.
- **Ví dụ**:
  - **05-05** · [00:45:32](https://www.youtube.com/watch?v=Au_SuIIstcY&t=2732s) — "Nếu nó đang đi lên dốc mà lực này chạy nhanh, chạy khỏe, tức volume tăng lên thì lực tăng sẽ được duy trì và nó sẽ đi lên tiếp. Còn nếu càng lên cao mà volume, lực này càng ngày càng yếu thì đến một thời điểm nào đó càng lên cao nó càng đuối, dễ gãy xuống."
  - **04-10** H1 · [00:23:06](https://www.youtube.com/watch?v=u6rbQNQWJAE&t=1386s) — "với lực đi như này và phân kỳ trên đỉnh H1, RSI phân kỳ, volume phân kỳ thì rất dễ xảy ra điều chỉnh ở vùng này."
  - **06-26** D1 · [00:19:03](https://www.youtube.com/watch?v=UzjWDBAiahs&t=1143s) — "phân kỳ nó chỉ thể hiện là vùng này bắt đầu lực bán nó yếu hơn vùng trước đó chứ nó không thể hiện câu chuyện là đảo chiều… Lực bán yếu hơn không có nghĩa là lực mua mạnh hơn."

### C8. Bộ nến đảo chiều họ gọi tên
- **Tình huống**: cuối nhịp giảm/tăng.
- **Người đó nhìn gì**: bộ 3 nến (full bán → rút lên nhỏ → xanh kẹp lại); cặp nến xanh–đỏ; nhấn chìm; H4 đóng xanh có thân (không phải râu hẹp).
- **Kết luận + hành động**: bộ 3 nến D1 → nhãn ghi "khả năng phục hồi ngắn hạn rất cao; không short hôm nay" (06-08). Cặp xanh–đỏ + liquid dưới → không short đuổi (04-27). Nhấn chìm đẹp vẫn có lúc "cắm xuống là cắm xuống" (06-04) — họ không coi nhấn chìm là đủ.
- **Tần suất**: 8/180 buổi nói "nhấn chìm".
- **Ví dụ**:
  - **06-08** D1 · [00:20:15](https://www.youtube.com/watch?v=WZ8PpZ9VA4Q&t=1215s) — "Nó bao gồm ba cây nến. Một cây nến bán xuống full lực bán, một nến rút lên nhỏ và sau đó kẹp lại một nến xanh, lực mua cũng tốt. Bộ này là một trong những bộ nến đảo chiều mình đánh giá là rất mạnh." · [ảnh 00:19:30](../../so_tay/khung/WZ8PpZ9VA4Q_001930.jpg)
  - **04-27** M5 · [00:35:43](https://www.youtube.com/watch?v=9oEDyu-IfMM&t=2143s) — "Có nhiều cây nến bán phun lực nhưng lại xuất hiện một cặp nến xanh đỏ như này, cộng với đó bên này có liquid thì cũng không nên short đuổi đoạn này kẻo chết."
  - **04-02** H4 · [00:48:04](https://www.youtube.com/watch?v=orDQVRuxI1E&t=2884s) — "Nếu có volume một tí, đừng đóng mấy cái cây nến mà râu hẹp như này thôi. Còn nếu đóng cây nến xanh mà có lực lên đây thì khả năng lên được cao. Còn nếu đóng nến đỏ thì chắc chắn là gãy về dưới này rồi." · [ảnh](../../so_tay/khung/orDQVRuxI1E_004830.jpg)

### C9. Thanh khoản yếu → quét hai đầu, nến không có ý nghĩa
- **Tình huống**: volume thấp, giá lên xuống lắt nhắt.
- **Kết luận + hành động**: "Nó sẽ đảo lên đảo xuống và quét hai đầu" [06-11]; "thanh khoản yếu nên nó cứ húp hai đầu" [06-23]; H4 đóng không thanh khoản "cũng không có ý nghĩa gì" [04-03].
- **Tần suất**: 60/180 buổi nói "hai đầu".
- **Ví dụ**:
  - **06-11** H4 · [00:32:58](https://www.youtube.com/watch?v=Xix-qwmyPkE&t=1978s) — "Khả năng bây giờ không có nhiều volume lắm, volume tầm này chắc đang build… Khối lượng như thế này không quá đảm bảo cho một nhịp phục hồi căng. Nó sẽ đảo lên đảo xuống và quét hai đầu."
  - **06-23** H4 · [00:23:12](https://www.youtube.com/watch?v=w3K-VXD_Tns&t=1392s) — "Vùng này thanh khoản yếu nên nó cứ húp hai đầu, đỏ tí thì lên húp, xanh tí thì gãy xuống húp, khối lượng không nhiều"
  - **04-03** H4 · [01:00:44](https://www.youtube.com/watch?v=vnCUK9ayUsI&t=3644s) — "Cứ cắm cắm ở đây rất là nhiều cây M5 râu. Chờ H4 rồi. H4 này thì cũng không có ý nghĩa gì. Một cây không có thanh khoản."

### C10. Thái độ với volume đổi trong năm (ghi cả hai)
- **Tháng 1**: "Chỉ có vài indicator bắt buộc phải dùng là RSI và volume. Đó là hai cái tối thiểu các bạn phải hiểu." — **01-30** · [00:22:01](https://www.youtube.com/watch?v=4PUqxjVBR4M&t=1321s)
- **Tháng 7**: "Cây volume này cũng chưa chắc đâu… Volume bán cũng mạnh chứ đâu phải yếu. Volume ở đoạn này nó cũng ảo lắm, không confirm được quá nhiều điều." — **07-07** · [00:59:32](https://www.youtube.com/watch?v=uvBnzq6-k-M&t=3572s)
- Bot nên biết: volume có trong 156/180 buổi, nhưng chưa có câu nào nói volume là điều kiện bắt buộc để công nhận một cú phá trendline (B3).

---

# D. MÔ HÌNH DÙNG KÈM

### D1. Cờ (flag) — đo cột cờ, xác nhận khi breakout
- **Tình huống**: sau một nhịp mạnh, giá đi kênh ngược chiều / đi ngang hẹp.
- **Kết luận + hành động**: cờ khung lớn chạy thì "tỉ lệ để nó hồi lên cực kỳ ít" [02-06, [00:07:59](https://www.youtube.com/watch?v=PLl8AM0RxEM&t=479s)]. **Cờ lần thứ hai** trên cùng khung thì họ không tin ("mức độ hiệu quả nó không còn được giữ nữa" [03-31]; "Mô hình này không có chạy được đâu" [03-10, [00:27:14](https://www.youtube.com/watch?v=TXnTpUkc78s&t=1634s)]). Cờ đi ngang hẹp **không phải** cờ tăng dù trước đó tăng (05-12).
- **Tần suất**: 68/180 buổi nói "mô hình cờ / cờ giảm / cờ tăng".
- **Ví dụ**:
  - **01-20 → 02-26** D1 (cờ giảm, đích 62k — case dài nhất năm): [01-20 00:08:17](https://www.youtube.com/watch?v=GygVJDmjlgY&t=497s) — "khung nến ngày thì nó có mô hình cờ giảm như thế này… Nếu cái vùng này nó break phá ra khỏi 90 thì thậm chí là về bảy mấy cũng có" → [01-29 00:10:02](https://www.youtube.com/watch?v=8NrjverKQpo&t=602s) — "Mình đã ghi ở đây là TP FL này 62.000 chứ không phải là 72.000" · [ảnh](../../so_tay/khung/8NrjverKQpo_000952.jpg) → [02-26 00:35:27](https://www.youtube.com/watch?v=7zFMbvqo3QI&t=2127s) — "Anh em thấy mô hình cờ này đã hoàn tất rồi… nó cho chúng ta một con số có cơ sở là 62.000, và nó về đến 62.000 và rút lên hai lần."
  - **03-02 → 03-03** M30 (cờ tăng nhỏ): [03-02 01:15:05](https://www.youtube.com/watch?v=GYgaZiYqRXY&t=4505s) — "30 phút ở đây thì có thể nó chạy mô hình cờ cũng đẹp này… Từ đây lên đây thì nó bằng từ đây lên đây thôi. Lên 70.000." → [03-03 00:21:44](https://www.youtube.com/watch?v=xXKnEs9z81g&t=1304s) — "Đúng theo target mô hình cờ là xong luôn. 70.000 là đúng luôn target của mô hình cờ."
  - **03-31** D1 (cờ lần hai) · [00:28:52](https://www.youtube.com/watch?v=bz8_iuwosGs&t=1732s) — "nhịp này là nhịp một này, cờ này, nhịp này nhịp hai, cờ này thì mình cũng không tin… đây là lần thứ hai nó chạy mô hình cờ này thì mức độ hiệu quả nó không còn được giữ nữa"
  - **05-12** H4 · [00:20:57](https://www.youtube.com/watch?v=MsCi4yFXqZA&t=1257s) — "Không, mình không nghĩ đó là mô hình cờ tăng. Nó chỉ là mô hình cờ đi sideway, đang tích lũy, tức là đi hẹp… đôi khi nó break dưới thì nó lại cắm đầu đi xuống" · [ảnh](../../so_tay/khung/MsCi4yFXqZA_002047.jpg)

### D2. Vai đầu vai — neckline là trendline; đích = đỉnh đầu → neckline
- **Tình huống**: ba đỉnh, đỉnh giữa cao nhất, ở cuối một nhịp tăng (khung tuần/ngày) hoặc khung nhỏ.
- **Người đó kẻ gì**: đầu năm vẽ cọ 3 vòng cung; 06-08 dùng công cụ Head and Shoulders của TradingView, mũi tên đo biên độ (`hinh_anh_4.md`). Neckline gọi là "trendline" / "đường màu vàng". Tắt MA mới thấy (06-01).
- **Phá thật / giả**: nến tuần/ngày đóng gãy neckline; sau đó hay có nhịp **lên test lại neckline** (05-18, 06-01). Chỉ dùng **ở trên đỉnh**: "Vai đầu vai nó chỉ áp dụng ở trên đỉnh thôi" [04-02, [00:23:47](https://www.youtube.com/watch?v=orDQVRuxI1E&t=1427s)].
- **Kết luận + hành động**: "biên độ TP sẽ bằng khoảng cách từ đỉnh về trendline" [06-08] → đích 59–60k [02-26], đáy 52 [06-08]. Vai đầu vai ngược ở khung nhỏ: chờ break lên rồi quay về tạo vai mới long (03-05).
- **Tần suất**: 47/180 buổi nói "vai đầu vai / neckline / đường cổ".
- **Ví dụ**:
  - **02-02** W1 · [00:26:34](https://www.youtube.com/watch?v=XD9H1FstBkE&t=1594s) — "nhìn vào đây thì ông nào cũng biết là vai đầu vai rồi. Nến tuần này nó gãy rồi." (ảnh `XD9H1FstBkE_002644`: **không thấy** neckline vẽ trên chart)
  - **02-26** W1 · [00:31:19](https://www.youtube.com/watch?v=7zFMbvqo3QI&t=1879s) — "Đối với một mô hình vai đầu vai thì nó đi từ đây về đây. Biên nó giảm sẽ bằng vùng phá neckline từ cái đỉnh về đến neckline… Neckline cứ gọi là đường màu vàng này đi… 5960 thì gần như là nó xong target"
  - **06-08** W1 · [00:13:02](https://www.youtube.com/watch?v=WZ8PpZ9VA4Q&t=782s) — "Chúng ta có một trendline ở đây, một mô hình vai đầu vai như vậy và gãy xuống. Thông thường đối với những mô hình vai đầu vai thì biên độ TP sẽ bằng khoảng cách từ đỉnh về trendline… rõ ràng đây là đáy 52." · [ảnh](../../so_tay/khung/WZ8PpZ9VA4Q_001330.jpg)
  - **05-18** W1 · [00:18:04](https://www.youtube.com/watch?v=phLlmyf_8-w&t=1084s) — "Các bạn thấy rõ ràng ở đây là vai đầu vai, sau đó đã phá qua và nhịp này là nhịp lên test nhịp một. Nó test ngay vùng cản… Vai đầu vai đâm xuống, tức là đang downtrend."
  - **06-01** D1 · [00:22:12](https://www.youtube.com/watch?v=cgTktZyPPt4&t=1332s) — "khi tắt MA đi thì đây là vai đầu vai, có neckline, nhịp đi lên để test lại neckline, cũng hợp lệ, vẫn là 75." · [ảnh](../../so_tay/khung/cgTktZyPPt4_002141.jpg)

### D3. Hai đỉnh / hai đáy (đọc kèm volume)
- **Tình huống**: giá test đỉnh/đáy cũ lần hai.
- **Người đó nhìn gì**: volume lúc thủng / lúc bật; phân kỳ; có neckline/trendline bị phá chưa.
- **Tần suất**: 33/180 buổi nói "hai đỉnh"; 76/180 buổi nói "hai đáy".
- **Ví dụ**:
  - **04-01** · [00:12:34](https://www.youtube.com/watch?v=Be-e74Mwx0U&t=754s) — "rõ ràng ở đây là hai đỉnh, thủng ở đây, kèm theo đó là volume bán cực kỳ mạnh. Thoát khỏi ở những vùng này là chuyện hết sức thường tình."
  - **03-12** H1 · [00:25:43](https://www.youtube.com/watch?v=qJZk9q5A7rA&t=1543s) — "Xuất hiện những cây nến bán liên tục nhưng mà không có volume lớn… Nếu các bạn vào đây các bạn short hai đỉnh, mình nghĩ là khả năng rất là dễ bị lừa."
  - **02-05** · [00:41:20](https://www.youtube.com/watch?v=D6s6HggWgVQ&t=2480s) — "Như này thì có vẻ là dụ short. Volume này cũng đẹp. Hai đáy này khả năng lên được… Đừng có short."

### D4. Đỉnh thấp dần + đáy đi ngang → dễ gãy xuống
- **Tình huống**: các đỉnh bị đạp thấp dần, đáy giữ ngang.
- **Người đó nhìn gì**: nối các đỉnh thấp dần (trendline) + đường ngang ở đáy; đọc là "lực bán liên tục xuất hiện", "lực mua càng ngày càng yếu".
- **Phá thật / giả**: thủng đáy ngang → gãy tiếp; muốn long thì phải break lên đường đỉnh rồi quay về tạo vai đầu vai ngược (03-05).
- **Kết luận + hành động**: nghiêng giảm; không long; thủng đáy ngang thì đi theo.
- **Tần suất**: 29/180 buổi nói "đỉnh thấp dần"; 6/180 buổi nói "đáy ngang / đáy bằng".
- **Ví dụ**:
  - **02-11** H1 · [00:03:39](https://www.youtube.com/watch?v=MZ3XfAjYHqk&t=219s) — "Đặc biệt đoạn này là đỉnh thấp dần nhưng đáy lại đi ngang. Đối với mô hình đỉnh thấp dần mà đáy đi ngang như này thì chúng ta hiểu là giá đang bị từ chối liên tục ở vùng trên, tức là lực bán liên tục xuất hiện." → [00:21:13](https://www.youtube.com/watch?v=MZ3XfAjYHqk&t=1273s) — "Thủng rồi. Bắt đầu thủng hỗ trợ rồi."
  - **07-01** H4 · [00:16:43](https://www.youtube.com/watch?v=WNiQnpm2BLo&t=1003s) — "Anh em thấy không, đáy nó liên tục được giữ nhưng cái đỉnh này cứ bị đạp xuống liên tục. Chứng tỏ là cứ xuống dưới này là sẽ có phe mua họ đỡ nhưng đỡ một hồi là không nổi."
  - **06-25** M5 · [00:20:00](https://www.youtube.com/watch?v=gy-YwzytUiA&t=1200s) — "mô hình mà đỉnh cứ giảm dần và đáy nó cố trụ thì có nghĩa là lực mua này càng ngày càng yếu thì vẫn có xác suất nó thủng khỏi đoạn này." · [ảnh](../../so_tay/khung/gy-YwzytUiA_002030.jpg)

### D5. Đáy cao dần + đỉnh đi ngang → dễ break lên
- **Tình huống**: các đáy nâng dần, đỉnh chạm cùng một mức.
- **Người đó nhìn gì**: trendline đáy + đường ngang đỉnh; mốc break là đỉnh ngang.
- **Kết luận + hành động**: "rất dễ break out lên. Thành ra… chúng ta không short" [04-17]; nến H4 break qua đỉnh ngang → đi tiếp tới MA/đích kế (02-16: 71 → 75 → 80; 03-16: 73,5 → 79).
- **Tần suất**: 9/180 buổi nói "đỉnh đi ngang / đỉnh bằng".
- **Ví dụ**:
  - **02-16** H4 · [00:16:44](https://www.youtube.com/watch?v=0zDtKlmcydA&t=1004s) — "Bây giờ chỉ cần nến H4 break ra khỏi được 71 này thì gần như là cái cửa để nó đi lên 75 sau đó là lên 80 khá là dễ… H4. Anh em lưu ý giúp mình cái mô hình này."
  - **03-16** H4 · [00:22:16](https://www.youtube.com/watch?v=uXm43DPUtPQ&t=1336s) — "Đáy nó kéo cao dần lên và đỉnh nó đi ngang. Thì mô hình này là hoàn toàn dễ breakout và đi lên tiếp."
  - **04-17** H4 · [00:20:26](https://www.youtube.com/watch?v=PH5pABMJ01k&t=1226s) — "một mô hình mà đáy cao dần và đỉnh nó bằng nhau thì rất dễ break out lên. Thành ra đối với việc dễ break out như này chúng ta không short." · [ảnh](../../so_tay/khung/PH5pABMJ01k_002016.jpg)

### D6. Tam giác cân / biên hẹp dần → chờ nến đóng ra khỏi biên
- **Tình huống**: đỉnh thấp dần + đáy cao dần, giá bị bó hẹp.
- **Kết luận + hành động**: chưa ra khỏi biên → chưa có hướng.
- **Tần suất**: 15/180 buổi nói "tam giác".
- **Ví dụ**:
  - **03-18** H1 · [00:17:08](https://www.youtube.com/watch?v=oyJGNnpopXw&t=1028s) — "Giá vẫn chưa qua được vùng cản theo trendline tam giác này. Giá đang đi hẹp dần, đi sideway, đi ngang."
  - **08-18** D1 · [00:09:30](https://www.youtube.com/watch?v=_c0_SERWnz0&t=570s) — (ảnh) tam giác 2 trendline xanh ngọc; lời nói: "bị cản ở cái trend line này tức là bị bó hẹp trong cái biên này. Cộng với đây là Fibo" · [ảnh](../../so_tay/khung/_c0_SERWnz0_000930.jpg)

### D7. Hộp đi ngang → fake out một đầu trước
- **Tình huống**: giá đi ngang trong một biên/hộp.
- **Người đó nhìn gì**: hai cạnh hộp; cú chọc ra một đầu rồi quay lại.
- **Phá thật / giả**: cú chọc đầu tiên ra khỏi hộp thường là **fake**: muốn giảm thì fake lên trước, muốn tăng thì fake xuống trước.
- **Tần suất**: 13/180 buổi nói "hộp / biên hẹp / bó hẹp"; 115/180 buổi nói "sideway / đi ngang"; 60/180 buổi nói "hai đầu".
- **Ví dụ**:
  - **03-09** M5 · [00:35:36](https://www.youtube.com/watch?v=-jRLufOuVEE&t=2136s) — "Vẫn là volume khá là nhỏ và kill long short hai đầu thôi."

### D8. Mô hình ít gặp
- **Cốc tay cầm** (5 buổi): chỉ có giá trị khi qua được trendline phía trên — **03-11** H4 · [01:06:02](https://www.youtube.com/watch?v=q-9RpBVzOhU&t=3962s) — "Đó cũng là cốc tay cầm nhưng nó phải đi qua khỏi trend line. Đây có một trend line rộng, trend line dài." · [ảnh 01:06:12](../../so_tay/khung/q-9RpBVzOhU_010612.jpg): cọ vẽ cốc + tay cầm, "trendline" vẽ cọ nối râu đỉnh ~79k → ~74k
- **Diamond** (2 buổi): **02-04** · [00:46:25](https://www.youtube.com/watch?v=c6WnN4Q9EXo&t=2785s) — "Cái mô hình Diamond này kiểu gì cũng rớt thôi các bạn ơi, rồi về dưới này đơn giản." (ảnh 00:46:35 `c6WnN4Q9EXo_004635`: Diamond vẽ cọ trên chart **LINK** tuần, không phải BTC)

---

# MÂU THUẪN / CHƯA RÕ (không tự giải, để người duyệt chọn)

| # | Chủ đề | Lời A | Lời B |
|---|---|---|---|
| 3 | Volume | "bắt buộc phải dùng là RSI và volume" [01-30] | "Volume ở đoạn này nó cũng ảo lắm, không confirm được quá nhiều điều" [07-07] |
| 5 | Neo đường | đa số đường thẳng trên ảnh neo ở râu cực trị (râu đáy 59,8k; râu đỉnh 126k, 71.041,7, 74.096,7, 87,25k) | cạnh dưới kênh 01-12/01-19 và đường hỗ trợ 06-04 không đi qua râu thấp nhất — chưa biết neo theo gì |
| 6 | Volume khi phá | không có câu nào nói "phá không volume = phá giả" | máy đo: 14/41 lần phá thật có volume ≥1,2× TB20, 8 lần <0,8× (mẫu nhỏ) |
