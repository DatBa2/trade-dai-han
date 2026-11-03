
## Mục 3 — `bot_v5/ngu_canh.py` bổ sung (giữ nhân quả)

| Việc | Sửa gì | Chỗ |
|---|---|---|
| 3a Fibo nhịp GIẢM tuần | Hàm mới `nhip_giam_tu_dinh(nen, so)`: đỉnh cao nhất (râu) trong 104 nến tuần → đáy thấp nhất (râu) SAU đỉnh đó; thoái lui 0.236 / 0.382 / 0.5 / 0.618 đo từ đáy lên (hằng `FIBO_GIAM_TUAN`). Đỉnh là nến cuối → ghi "chưa có nhịp giảm sau đỉnh". JSON `fibo_tuan_nhip_giam`; Markdown mục 3, dòng "**Tuần — nhịp GIẢM từ đỉnh cao nhất …**" ngay dưới "Tuần — nhịp lớn", ghi neo + ngày tuần (tính cho mọi khung hỏi, kể cả 1W) | `ngu_canh.py`: `nhip_giam_tu_dinh`, `tao_ho_so`, `ve_markdown` |
| 3b Trạng thái lúc T−24h | Hàm mới `trang_thai_truoc(h4, d1, t, gio=24)`: nến H4 cuối ĐÓNG ≤ T−24h → giá đóng, dải EMA34 (TRÊN/TRONG/DƯỚI + 2 mép), EMA89 / EMA200 (trên/dưới + giá), phân loại L01; nến D1 cuối đã đóng ≤ T−24h → màu + O/đóng + thân %. EMA tính trên chuỗi cắt tại nến đó. Mục "0. Thời gian" in 3 dòng: trạng thái T−24h, nến D1, "So với lúc T" (H4 đóng, dải EMA34, L01). JSON `truoc_24h`. Tách 2 helper dùng chung `_loai_L01`, `_vi_tri_dai` (phân loại L01 của `phan_tich` giữ nguyên kết quả) | `ngu_canh.py`: `trang_thai_truoc`, `_md_truoc` |
| 3c Trendline +24h / +48h | Mỗi đường (H4/D1, chính + khác) thêm `gia_sau_24h` = giá tại T + dốc/ngày, `gia_sau_48h` = + 2×dốc (đường tuyến tính theo giá, `trendline.Duong.gia`). Markdown: "đường sau 24h ≈ …, sau 48h ≈ … (theo dốc)"; dòng trendline BTC ở mục 6 (coin khác BTC) cũng có | `ngu_canh.py`: `trendline_tai.gon`, `_md_trendline`, `_md_btc` |

**Kiểm** — `python3 bot_v5/kiem_tra_ngu_canh.py` → **PASS hết** (~30 giây, offline với cache sẵn có):
- (a) cắt cụt XOÁ / ĐẦU ĐỘC sau T: 6 ca, Markdown + JSON giống hệt. Ba phần mới nằm trong `hs`, nên (a) đã phủ.
- **(a3) mới**: đầu độc mọi nến / F&G có giờ đóng > T−24h (cả khoảng T−24h → T) → khối `truoc_24h` giống hệt, 6/6 ca.
- **(d) mới**, 6 ca × 3 kiểm:
  - T−24h: đúng nến H4/D1 (đóng ≤ T−24h < nến sau); EMA34 dải / 89 / 200 tính lại độc lập bằng `chi_bao.ema` khớp; dòng có trong Markdown.
  - Nhịp giảm tuần: đúng max râu 104 tuần, min râu sau đỉnh và công thức mức Fibo.
  - Trendline: mọi đường có +24h / +48h đúng = giá tại T + dốc × 1 / × 2, đủ trong Markdown.
- (c) EMA / RSI / bot_v4 / trendline cũ: vẫn PASS.
- Ví dụ BTC 4H 2026-09-21 11:00: T−24h = H4 2026-09-20 11:00 TRÊN dải EMA34, L01 TĂNG; D1 2026-09-19 xanh. Nhịp giảm tuần 126.200 (tuần 2025-10-06) → 57.809 (tuần 2026-06-29), 0.382 = 83.935, 0.5 = 92.005.

## Làm rõ chỗ mơ hồ — `NHAP_VAI.md` §3–§9 + `MAU_TRA_LOI.md` (31/10/2026)

| Việc | Sửa gì | Nguồn |
|---|---|---|
| a. Kẹp giữa | Định nghĩa: H4 đóng TRONG dải EMA34 hoặc giữa dải EMA34 và EMA89/200 → GIỮ hướng view đang có, hành động CHỜ, đổi chỉ khi có công tắc nến đóng; kẹp ≠ PHÂN VÂN trừ khi đủ L35 (Bước 5, §4.1, MAU mục 1 + bảng) | [03-12, 01-28, 04-28], L07, L35 |
| b. "GIẢM (điều chỉnh)" | Nhãn đối xứng của "TĂNG (hồi kỹ thuật)"; đích = hỗ trợ khung lớn chưa test = vùng LONG trung hạn. Quan hệ L06: hàng D1/W1 giữ hướng khung lớn (= "nhãn vẫn là GIẢM"), hàng H4 ghi hướng H4 thật kèm chữ đánh dấu; lệnh theo H4 = lệnh phụ (§4.1, MAU) | L05, L06, L33, [ST1 B4], [ST3 C1–C2], [04-06], A0 |
| c. Mốc sai | Số = giá RÂU đỉnh/đáy cấu trúc gần nhất của chính khung đó; điều kiện "nến <khung> ĐÓNG qua"; view vừa đổi vì công tắc → lấy lại mức công tắc; W1 khi giá đã bên kia đỉnh/đáy tuần mà tuần chưa đóng → cản/hỗ trợ tuần gần nhất phía bất lợi (§5, Bước 3, Bước 5, MAU bảng mục 3) | L25, L27, L03, L24, [03-04], [03-27], [ST1 B2, B3, D4, A5] |
| d. D1 ngược W1 | Trung hạn chính theo W1; lệnh theo D1 ngược W1 = lướt, vốn nhỏ, chốt sớm (§4.1, MAU mục 1 + bảng mục 1, 4) | L05, L33, [ST3 D5] [09-21], [05-04] |
| e. Độ chắc | "cao" cần thêm: không có khung xung đột; xung đột → tối đa "vừa" (bỏ "thấp vì xung đột") | L07, A4.3, L34, [07-07], [07-31] |
| f. Mục 3 tách 3 khung | "Đích H4 (chặng gần)" · "Đích D1" · "Đích W1", mỗi khung theo hướng của chính nó + "View <khung> sai khi: nến <khung> ĐÓNG …"; luật chung 1 ghi rõ đây là 3 view chứ không phải nước đôi; phần B "Tóm tắt để chấm" + "Chấm D1"/"Chấm W1" tách riêng | (định dạng) L20, L21, L25 |
| g. Không ảnh | Dòng "Ảnh: không có — user ghi thẳng `<MÃ> <KHUNG> "<T>"`", bỏ kiểm chéo giá ảnh (khuôn A, bảng "Đầu", phần B) | NHAP_VAI §2.4 (thủ tục) |
| h. Coin khác BTC | Ngưỡng "giá" BTC → dùng % [ST3 B1–B2] (vùng ~1,3%, đích D1 ~2%, W1 ~3%, tránh ~1,9%, non TP ≈ 0,2%); số tròn theo bậc giá của coin (§5, MAU luật chung 3) | [ST3 B1–B2], A4.7 [01-06], [05-27] |
| i. View đang giữ | Bước 0 dùng dòng "Trạng thái lúc T−24h" của hồ sơ: L01 H4 lúc T−24h → view hôm trước; kẹp → hướng D1 (rồi W1); rồi xét tác động §4.2 | [ST1 B1], B0, A2, L05 |
| Rò rỉ giá | Bỏ số/diễn biến thật: MAU luật chung 2 (số tháng 10 → số giả 1.208 / 1.150 / 1.240), luật chung 3 ("vùng 82" → "vùng N"); NHAP_VAI §5 "vùng 82 = 81.900→82.550" → "đầu số N", "[09-30] thủng 75…72…69" → "thủng mốc này lại về nấc tiếp…"; §6.3 "chốt 90% ở 90–100k" → "chốt dần ~90%"; A4.7 altcoin bỏ giá. Giữ bối cảnh chu kỳ ~126k (10/2025). §0–§2: quét không thấy giá thật | yêu cầu điều phối |

**Gỡ vì là ý riêng (không dẫn được về người đó)**
- MAU bảng mục 7: "KHÔNG test khi râu ngắn khung nhỏ đã đi xa và có EMA chắn giữa" (không nguồn) → thay bằng "râu lưng chừng không tính là căn cứ" (A4.9).
- MAU bảng mục 7: "KHÔNG test khi râu nằm ngược phía chặng 2" (trái L45 / [ST3 E3]: chặng 1 thường về test râu) → thay "râu ngược chặng 2 vẫn có thể là đích chặng 1 (L45)".
- NHAP_VAI §7: "Vàng (tuỳ chọn, khi BTC ở mốc quyết định)" → họ xem vàng gần như mọi buổi (A2 bước 5); Bước 7 bỏ "(vàng nếu cần)".
- NHAP_VAI §5: "Vùng rộng hơn mức đó = chưa đủ hội tụ" → viết lại theo [ST3 A6] "khi hội tụ, vùng hẹp lại ở chỗ trùng"; sửa số sai "vùng tránh trung vị 1.400" → 1.300 (~1,9%) theo [ST3 B1].
- MAU mục 2–3: "chặng 3 / đích 2 chỉ khi thuận khung tuần" gốc là dòng ▸ A4.10 → giữ ý nhưng dẫn lại về L05/L33.

**Còn nghi là ý riêng, CHƯA gỡ (để duyệt)**
- NHAP_VAI §6.3 "lệnh trung hạn: nến D1; H4 đóng qua là cảnh báo sớm" — L25 nói swing dùng D1 nhưng [03-27] họ ra swing khi H4 thủng đáy H4; "cảnh báo sớm" là cách người viết dung hoà.
- MAU bảng mục 2 hạn "chặng H4 ~1–3 ngày; đích W1 2–4 tuần" — cận trên do người viết chọn (số đo: D1 2,5 ngày, W1 15,4 ngày).
- NHAP_VAI Bước 1 "coin khác: thiên hướng theo BTC ('98% là trade Bitcoin')" — câu trích không chứng minh luật.
- NHAP_VAI §6.3 "chưa nói lệnh → trả lời cả LONG và SHORT", MAU luật chung 5 — yêu cầu của user, không phải luật người đó (giữ).
- Mốc sai lấy giá RÂU: A4.2 ghi "tính bằng giá đóng nến / không dùng râu" — đã hiểu là ĐIỀU KIỆN đóng nến, số vẫn là râu cực trị (theo chỉ đạo + L25 + fractal râu của hồ sơ).

## Sổ tay lọc theo T — chặn đọc đáp án ở/sau T (31/10/2026)

Vấn đề: `bot_v5/so_tay/*.md` và phần C `so_tay/SO_TAY_TINH_HOA.md` ghi view thật của người đó theo ngày (bảng đợt D1/W1,
bảng pha theo tháng, trích dẫn có ngày, "Đo:" diễn biến sau lúc nói) → thử ảnh ở T trong 2026 thì bot đọc được đáp án.

| Việc | Sửa gì | Chỗ |
|---|---|---|
| Lọc | `python3 bot_v5/so_tay_den.py "<T>"` → `bot_v5/_so_tay_T/` = 3 sổ tay + `giong_noi.md`. Bỏ CẢ dòng / hàng bảng có bất kỳ mốc ≥ NGÀY của T (cùng ngày cũng bỏ) + dòng con thụt sâu hơn + bảng ngay sau dòng bị bỏ kết thúc ':' + nhãn "Ví dụ" trơ trọi. Mốc: `[MM-DD · …](link)`, `[MM-DD]`, `MM-DD`, `MM-DD/DD`, `DD/MM`, `DD/MM/YYYY`, `MM/YYYY`, `2026-MM-DD`, ô `T7` / nhãn `**Tháng 9–10**` (tháng ≥ tháng của T), link YouTube + tên ảnh `<id>_<hhmmss>.jpg` (ngày buổi theo `transcripts/danh_sach.tsv`). Không tính: phân số `10/22 = 45%`, năm dự báo (`4/2028`, `Q2/2027`). Dòng có dấu hiệu kết quả ("Đo:", "đạt", "quá mép", "không về"…) tính thêm 30 ngày. Cột "Ngày tới lần đổi" vượt T → "—". Giọng nói: mỗi câu mẫu `"…" [MM-DD]` là một mục ví dụ → bỏ từng câu, hàng hết câu thì bỏ hàng. Thêm: dòng KHÔNG ngày nhưng có mức giá chỉ xuất hiện (có ngày) từ T trở đi → bỏ (vd "(85,0–85,5k; 81–82k)" lấy từ ví dụ 10-02). Giữ tiêu đề, `<details>`, hàng tiêu đề bảng (bảng lọc hết → 1 dòng ghi chú), luật + số [đo] không ngày. Dòng đầu mỗi file: "Lọc theo T = …; bỏ N dòng có ngày ≥ T" | `bot_v5/so_tay_den.py` (mới) |
| Kiểm | `python3 bot_v5/kiem_tra_so_tay_den.py` → **PASS hết**: 4 mốc T (2026-09-21 11:00, 07-15 10:00, 03-01 10:00, 2025-12-01 10:00) quét regex độc lập không còn mốc ≥ T; đủ mọi tiêu đề (case `## A1.`…, `# A.`…) đúng thứ tự; bảng / `<details>` hợp lệ; số dòng còn lại tăng dần theo T; T 2027-01-15 không bỏ gì; ca đơn vị nhận dạng ngày / bảng / giọng nói / giá không ngày | `bot_v5/kiem_tra_so_tay_den.py` (mới) |
| Lệnh | Thứ tự mới: (1) NHAP_VAI + MAU_TRA_LOI → (2) ảnh / tham số lấy MÃ, KHUNG, T → (3) `so_tay_den.py "<T>"` rồi đọc `bot_v5/_so_tay_T/` (cấm `bot_v5/so_tay/`, `SO_TAY_TINH_HOA.md`) → (4) `ngu_canh.py` … như cũ. `allowed-tools` thêm `so_tay_den.py` (+ biến thể `rtk proxy`) | `.claude/commands/nhan-dinh.md` |
| Luật | Đầu file: sổ tay đọc từ `bot_v5/_so_tay_T/`, mọi chỗ nhắc `bot_v5/so_tay/…` / phần C `SO_TAY_TINH_HOA.md` = bản lọc; [ST1–3] trỏ `_so_tay_T/`. §1.3: chỉ đọc bản lọc, dòng đầu phải khớp T. §1.4: CẤM `bot_v5/so_tay/` + `so_tay/SO_TAY_TINH_HOA.md` (bản gốc có view thật theo ngày, kể cả sau T); `thi/SO_TAY_T1_T6.md` chỉ khi T sau 2026-06-25 (ghi view tới 25/06). §0–§1: không có trích dẫn kèm giá thật | `bot_v5/NHAP_VAI.md` đầu file, §1 |

Số dòng bị lọc ở T = 2026-09-21 11:00: ST1 bỏ 50 / 536 · ST2 bỏ 32 / 452 · ST3 bỏ 28 / 330 · giọng nói bỏ 0 dòng + 11 câu mẫu.
T = 2026-03-01: ST1 200 · ST2 193 · ST3 87 · giọng nói 3 dòng + 37 câu.

**Còn để ý**
- Bỏ cả dòng (đúng yêu cầu) nên dòng LUẬT có trích dẫn ≥ T cũng mất (vd ST2 bảng tra nhanh "Phá = nến đóng cửa qua đường" khi T < 10-19); luật cốt lõi vẫn có trong NHAP_VAI. Muốn giữ phần luật thì đổi sang cắt theo vế câu (rủi ro: câu không ngày nối sau trích dẫn có thể còn lộ diễn biến).
- Số tần suất / [đo] tổng hợp cả năm (vd "GIẢM 105/119") và tiêu đề "2026 là năm downtrend" vẫn giữ theo yêu cầu — là thông tin gộp có cả sau T.
- NHAP_VAI §8 dòng "Nguồn: `so_tay/SO_TAY_TINH_HOA.md` phần C" và MAU_TRA_LOI mục 10 vẫn ghi đường dẫn gốc (ngoài phần được sửa) — đã phủ bằng câu "= bản lọc cùng tên" ở đầu NHAP_VAI; nên đổi chữ ở lượt sau.

## Đọc lại 180 buổi — giữ / lật view, vàng (02/11/2026)

21 subagent đọc trọn 180 transcript (`transcripts/zip_clean/` + `lam_sach/`), so với mục lục sổ tay hiện có; 311 phát
hiện, 1717/1728 câu trích khớp nguyên văn (kiểm bằng tìm chuỗi). Báo cáo từng lô để ngoài repo (scratchpad phiên).

| Việc | Sửa gì | Căn cứ |
|---|---|---|
| a. B3 nói "→ LẬT" trái số đo của chính nó (GIỮ 58%) | Đổi tiêu đề + bảng tra nhanh: nến đóng qua mốc sai = điều kiện CẦN (thoát lệnh), đổi nhãn khi đủ B11 | 373 ca mốc bị phá/quét trong 21 lô: GIỮ 268 = 72%; nến H4 đóng qua GIỮ 20 / LẬT 15 |
| b. B11 mới — thang ba tầng | Mốc lệnh → chỉ thoát lệnh; mốc cấu trúc + ≥ 2 thứ gãy → đổi nhãn; mốc tuần → chỉ nến tuần | 11/21 lô ghi LAM_RO B3; râu quét GIỮ 69 / LẬT 3; D1 đóng qua GIỮ 15 / LẬT 5; tuần GIỮ 6 / LẬT 0 |
| c. B12 mới — sóng hồi ngược khung tuần | "TĂNG (hồi kỹ thuật)" chỉ khi H4 qua đỉnh H4 gần nhất + cụm EMA và D1 đáy/đỉnh cao dần, chưa chạm cản khung lớn; còn lại GIẢM | Lỗi chính bài thi v3 (14 buổi người GIẢM, bot TĂNG); `dac_trung_moi.csv`: view GIẢM + H4 trên dải EMA34/EMA89 → người đó GIẢM 11 / TĂNG 8 (EMA lật đúng 42%, giữ view 58%) |
| d. NHAP_VAI Bước 0 / Bước 5 / §4.1 / §4.2 / §9 | Công thức EMA H4 = bộ lọc hành động; đòi đổi nhãn ngược W1 → xét B12; suy view T−24h ngược W1 → xét B12; §4.2 (a) trỏ B11 | như b, c |
| e. C7 mới — vàng / dầu | Quan hệ vàng–BTC đổi theo giai đoạn (01: không liên quan · 03: ngược · 06–07: cùng chiều · 08: chỉ lường rủi ro) → chỉ HOÃN; 2 câu vàng có ngày chuyển từ NHAP_VAI (không lọc theo T) sang sổ tay (có lọc) | 14/21 lô nhắc vàng; 5 lô ghi trái luật cũ L13 |

**Kiểm** — `python -X utf8 bot_v5/kiem_tra_so_tay_den.py` → PASS hết (sau khi đổi "11/19", "12/14", "02/11/2026" sang
chữ: bộ quét độc lập đọc chúng thành ngày). Lọc thử T = 01-10 / 03-01 / 08-20 / 10-31: B11, B12, C7 + dòng tần suất còn ở
mọi T; ví dụ bị cắt đúng ngày (0 → 9 ví dụ B11).

**Đã thử mà KHÔNG đưa vào luật** (mô phỏng khung quyết định hướng H4 trên 172 buổi có hướng, học < 07-01 / kiểm ≥ 07-01):
- Khung v5 hiện tại (suy view từ L01 H4 lúc T−24h + công tắc EMA): học 71% · kiểm 57% — thua "luôn GIẢM" ở tập kiểm (70%).
- Bất đối xứng cơ học (không lật ngược pha W1): học 63% · kiểm 70% = y hệt "luôn theo pha W1".
- Suy view có quán tính (chạy từng nến H4 từ T−30 ngày, ngược W1 phải giữ N nến): N = 1–12 → kiểm 51–56%.
- Cấu trúc fractal H4 (BOS, k = 3), lọc thêm D1: 69–71%, kém giữ view (75%, khi có view thật).
- "Đã lên trên EMA34 tuần → GIẢM": học 62% (−9) · kiểm 81% (+24) → phụ thuộc giai đoạn, không dùng.
→ Không quy tắc cơ học nào vượt mốc đơn giản ổn định ở cả hai giai đoạn (khớp `hoc_v5/giu_lat/GIU_LAT.md`). B11 / B12 là
  luật định tính theo lời người đó; **chưa chấm lại v5 hàng loạt** nên chưa có số chứng minh độ giống tăng.

**Còn để ý / chưa làm**
- Phát hiện chưa đưa vào: thứ Hai (nến D1 thứ Hai xanh hay đỏ đều không dùng đổi view; T2–T3 đang hồi thì chưa short
  tới thứ Tư), gap CME (nam châm / đích hồi, hoãn short — hồ sơ chưa có; `du_lieu/cme_btc_1h.csv` có sẵn), Hyblock /
  heatmap (chỉ hoãn short, không đổi nhãn), tin đỏ khi giá kẹt dưới cản lớn (quét lên rồi đảo).
- Dữ liệu họ dùng nhiều nhất mà hồ sơ không có: USDT.D / BTC.D (gần như mọi lô) — chỉ để cảnh báo / xác nhận.

## Đo lại độ giống: bản TRƯỚC vs SAU đợt đọc lại 180 buổi — thiết kế chốt TRƯỚC khi chạy (02/11/2026)

- **Mẫu**: 77 buổi thi v3 (`thi/ho_so_v3/`) xếp theo tên, lấy chỉ số 0, 4, 8, …, 76 → 20 buổi (07-01 → 10-30).
  T = mốc cắt C của hồ sơ v3 (giờ kết thúc live). Không chọn tay.
- **Đáp án**: nhãn H4 cuối buổi của người đó theo đáp án v2 (`thi/cham.py --phieu thi/dap_an_v2/phieu`, mục 7 cột
  "Người"). Trên mẫu: GIẢM 16 · TĂNG 3 · PHÂN VÂN 1. Mốc trên cùng 20 buổi: luôn GIẢM 16 · giữ view 13 · bot v3 12.
- **Hai bản**: TRƯỚC = HEAD (`NHAP_VAI.md`, `MAU_TRA_LOI.md`, 3 sổ tay, `ngu_canh.py` chưa có gap CME / BTC.D / USDT.D) ·
  SAU = bản làm việc khi đã thêm hết (B11, B12, C7 + các mục và dữ liệu mới của đợt này). Gói đầu vào dựng sẵn cho từng
  buổi: sổ tay lọc theo T + hồ sơ BTC 4H, BTC 1H (`--so-nen 12`), VANG 4H (`--so-nen 8`) tại T, chạy `--offline`.
- **Chạy**: mỗi buổi × mỗi bản = 1 subagent mới (cùng model với phiên chính) nhập vai theo `/nhan-dinh`, chỉ đọc gói của
  mình; tên gói che bằng A/B gán ngẫu nhiên từng buổi nên agent không biết bản nào mới.
- **Chỉ số chính**: số buổi trùng nhãn H4 (3 nhãn) trên 20 buổi, TRƯỚC vs SAU. Báo thêm: cặp lệch (SAU đúng–TRƯỚC sai /
  ngược lại), tách 5 buổi thuộc 14 ca lỗi v3 (07-28, 08-18, 08-25, 10-05, 10-20) với 15 buổi còn lại.
- **Giới hạn biết trước**: (1) B12 rút từ chính 14 ca lỗi v3 và sổ tay v5 rút từ cả 180 buổi → mọi số trên T7–T10 là
  TRONG MẪU, chỉ dùng để so trước/sau, không phải độ chính xác ngoài mẫu; (2) n = 20 → chênh 1–3 buổi chưa phân biệt được
  với nhiễu; (3) mỗi lần nhập vai có tính ngẫu nhiên, chỉ chạy 1 lần mỗi ô.

## Hoàn thiện phần còn lại của đợt đọc lại: dữ liệu ngoài chart + 4 nhóm luật (02/11/2026)

| Việc | Sửa gì | Căn cứ |
|---|---|---|
| a. Hồ sơ mục 7 — gap CME | `nen.py` thêm mã CME (Yahoo BTC=F 1h); `ngu_canh.gap_cme()`: gap = giá đóng trước kỳ nghỉ > 3 giờ vs giá mở sau, gốc ≥ 0,5%, lấp dần theo râu, lấp hết khi râu đi hết vùng; liệt kê ≤ 4 gap chưa lấp mỗi phía (±30%), gap vừa lấp 7 ngày, chênh CME − spot ở giờ đóng H4 | Khớp gap người đó nêu: 01-14 còn gap 88,1–88,8k (họ nói "gap 88"), 03-18 còn gap 80k + 92k ("gap 80 và 93"), 09-17 còn gap 92k ("gap 90 đến 92") |
| b. Hồ sơ mục 7 — BTC.D / USDT.D | `nen.lay_dom()`: proxy CMC theo ngày (như `thi/tao_ho_so.py`), biết sau ảnh chụp + 1 giờ; lưu cache dạng nến để phép thử đầu độc phủ luôn; hồ sơ in giá trị, đổi 1/7/30 ngày, vị trí so EMA34/89 ngày, cao/thấp 30 ngày | Mức % lệch chart TradingView người đó xem → luật chỉ dùng hướng |
| c. `kiem_tra_ngu_canh.py` (e) | BTC.D / USDT.D = dòng cache cuối biết ≤ T; mỗi gap tính lại từ CSV thô; tại 09-17 gap 92k còn phía trên | Đột biến cố ý cho CMC / CME nhìn quá T → (a) bắt được cả hai |
| d. ST1 C8 gap CME, C9 USDT.D / BTC.D, C10 phe đông | Cả ba chỉ HOÃN / làm đích, không đổi nhãn H4 một mình; C10 dặn thiếu dữ liệu thì không suy TĂNG từ "không short"; luật theo giai đoạn của gap gắn ngày ([05-11], [08-25]) để bộ lọc T ẩn đúng lúc | 10 / 17 / 19 trong 21 lô; 50 câu trích mới đều khớp nguyên văn đúng 1 buổi |
| e. ST1 A2 nến D1 thứ Hai | Xanh hay đỏ không tự đổi view, chỉ phòng thủ / hoãn short đầu tuần; ngoại lệ: nến thứ Hai thân lớn bị từ chối ở cản + Fibo | 8 trong 21 lô |
| f. ST1 C2 tin đỏ dưới cản lớn | Quét lên qua cản rồi đảo xuống trong 1–2 nến H4, kể cả tin "tốt"; dòng luật gắn [10-01] (lần đầu nói rõ) | 2 tin đỏ liền nhau (PCE, NFP) cùng một kiểu |
| g. NHAP_VAI §1.5, Bước 0, §7; MAU_TRA_LOI mục 9; README | Hồ sơ có gap CME + proxy USDT.D / BTC.D; trỏ tới C8–C10, A2 | |

**Kiểm** — `kiem_tra_so_tay_den.py` PASS hết; lọc thử T = 04-30 / 09-01 / 10-03: luật "từ 05-11", "từ 08-25" và luật
tin đỏ ẩn trước ngày của chúng, ví dụ cắt đúng ngày. `kiem_tra_ngu_canh.py` PASS hết (gồm (e)).

## Đo lại độ giống: kết quả (02/11/2026, theo thiết kế đã chốt ở trên)

40 lần nhập vai (20 buổi × 2 bản, Opus, gói che A/B), ~290 nghìn token mỗi lần. Nhãn H4 (đáp án v2):

| # | Buổi | Người | v3 | TRƯỚC | SAU | 14 ca lỗi v3 |
|---|---|---|---|---|---|---|
| 01 | 2026-07-01 | GIẢM | GIẢM | GIẢM | GIẢM |  |
| 02 | 2026-07-07 | GIẢM | GIẢM | TĂNG | GIẢM |  |
| 03 | 2026-07-14 | GIẢM | GIẢM | GIẢM | GIẢM |  |
| 04 | 2026-07-22 | TĂNG | TĂNG | TĂNG | TĂNG |  |
| 05 | 2026-07-28 | GIẢM | TĂNG | GIẢM | GIẢM | x |
| 06 | 2026-07-31 | GIẢM | PHÂN VÂN | GIẢM | GIẢM |  |
| 07 | 2026-08-06 | TĂNG | GIẢM | TĂNG | GIẢM |  |
| 08 | 2026-08-12 | GIẢM | PHÂN VÂN | GIẢM | GIẢM |  |
| 09 | 2026-08-18 | GIẢM | TĂNG | TĂNG | GIẢM | x |
| 10 | 2026-08-25 | GIẢM | TĂNG | TĂNG | TĂNG | x |
| 11 | 2026-09-03 | GIẢM | GIẢM | TĂNG | GIẢM |  |
| 12 | 2026-09-14 | GIẢM | GIẢM | TĂNG | GIẢM |  |
| 13 | 2026-09-17 | GIẢM | GIẢM | GIẢM | GIẢM |  |
| 14 | 2026-09-23 | TĂNG | TĂNG | TĂNG | TĂNG |  |
| 15 | 2026-09-29 | GIẢM | GIẢM | GIẢM | TĂNG |  |
| 16 | 2026-10-05 | GIẢM | TĂNG | TĂNG | TĂNG | x |
| 17 | 2026-10-14 | PHÂN VÂN | PHÂN VÂN | TĂNG | TĂNG |  |
| 18 | 2026-10-20 | GIẢM | TĂNG | TĂNG | TĂNG | x |
| 19 | 2026-10-27 | GIẢM | GIẢM | GIẢM | GIẢM |  |
| 20 | 2026-10-30 | GIẢM | GIẢM | GIẢM | GIẢM |  |

- **TRƯỚC 12/20 = 60% · SAU 14/20 = 70%**. Mốc trên cùng 20 buổi: luôn GIẢM 16, giữ view 13, bot v3 12.
- Cặp lệch: SAU đúng–TRƯỚC sai 4 (02, 09, 11, 12), TRƯỚC đúng–SAU sai 2 (07, 15) → McNemar chính xác p ≈ 0,69:
  **chưa phân biệt được với nhiễu**. 5 buổi thuộc 14 ca lỗi v3: 1 → 2; 15 buổi còn lại: 11 → 12.
- Cả hai bản vẫn **thua "luôn GIẢM"** (16/20). Hướng sai còn lại gần như một chiều: nói TĂNG khi người đó GIẢM (10, 15, 16, 18).
- **Vì sao B12 không cứu 16, 18, 15**: từ cuối tháng 9 giá đóng tuần trên EMA34 + EMA89 tuần, đỉnh tuần bị vượt → bot đọc
  W1 = TĂNG, nên "hồi ngược khung tuần" không áp dụng; người đó vẫn coi là nhịp hồi trong năm downtrend (A1). Ca 10:
  bot cho là đủ điều kiện B12 (2)(3) và cản lớn chưa chạm → "TĂNG (hồi kỹ thuật)", người đó vẫn GIẢM.
- **Không sửa luật theo kết quả này** (đây là tập đo, sửa theo nó = chỉnh theo đáp án). Ứng viên cho vòng sau, phải chốt
  trước rồi đo trên buổi live MỚI (sau 30/10): W1 không đổi sang TĂNG chỉ vì giá trên EMA tuần khi pha chu kỳ [ST1 A1]
  còn là downtrend — trùng phép thử "đã lên trên EMA34 tuần → GIẢM" ở mục trên (học 62% / kiểm 81%, phụ thuộc giai đoạn).

## v5 thành base, gỡ v3 (02/11/2026)

`thi/` (bộ thi v3: sổ tay T1–T6, hồ sơ, bài làm, bộ chấm, snapshot) gỡ khỏi repo — tra lại bằng `git show c19482b:thi/…`.
Giữ `thi/du_lieu/btc_*_bo_sung.csv` (`cong_cu/dieu_kien.py` → `hoc_v5/giu_lat/`) và `thi/dap_an_v2/nhan/` (`hoc_v5/kiem_nhan.py`).
NHAP_VAI: bỏ ngoại lệ "được đọc `thi/SO_TAY_T1_T6.md` khi T sau 06-25" (file không còn); `thi/` vẫn cấm đọc (còn nhãn đáp án).

## Buổi live mới đầu tiên ngoài mẫu: 02/11/2026 (bot trả lời TRƯỚC khi đọc transcript)

- Bot chạy `/nhan-dinh BTC 4H "2026-11-02 11:00"` lúc 14:16, file `bot_v5/doi_chieu/2026-11-02_BTC.md`. Sau đó mới tải
  transcript ([MEKVe_u8BA8](https://www.youtube.com/watch?v=MEKVe_u8BA8), live 10:08 → 11:10) bằng `cong_cu/lay_transcript.py --moi-nhat 1`
  (cài `yt-dlp` 2026.10.26 theo yêu cầu user). Bảng so sánh chi tiết nằm trong file đối chiếu.
- **Khớp**:
  - H4 / D1 / W1 cùng GIẢM;
  - chặng 1 hồi lên 79–80k rồi mới short, chờ nến H1 (bot đặt 79,6–80,2k, cao hơn ~500 giá);
  - hôm nay không short sớm;
  - BTC.D lên thì bỏ altcoin; F&G bỏ qua; vàng giảm.
- **Lệch**:
  1. Sau chặng 1, người đó đặt **vùng quyết định 78–77k** (giữ thì có cơ sở tăng, đóng dưới 77,5k thì về 75 / 74k). Bot đi thẳng
     xuống 76,3–76,9k, thiếu mốc này.
  2. **USDT.D**: bot đọc mức đổi 30 ngày (+0,46 → cảnh báo); người đó đọc mấy ngày gần nhất (đang nhích xuống → nhịp hồi).
  3. Bot không có Hyblock (500k short → lên quét 79k), dòng tiền ETF, dòng rút Binance, lịch bầu cử giữa kỳ Mỹ.
- **Sửa** (ví dụ gắn [11-02] nên bộ lọc T ẩn với T ≤ 02/11 — đã thử T = 02/11 11:00 → 0 dòng, 03/11 → hiện):
  - ST1 C9 + NHAP_VAI §7: hướng USDT.D theo mấy ngày gần nhất, không theo đổi 30 ngày.
  - ST3 E1: sau chặng 1 là vùng QUYẾT ĐỊNH, phải ghi mức nến cần đóng ở đó.
  - Thêm ví dụ 11-02 vào ST1 A2 (nến tuần "giữ nhịp chứ không phải đang tăng"), C6 (bầu cử = nhiễu, giảm volume),
    C10 (500k short → lên quét).
  - `kiem_tra_so_tay_den.py` PASS hết.
- **Chưa làm**: nhãn `hoc_v5/nhan/` cho buổi này; lịch tin `du_lieu/tin_tuc/` chưa có sự kiện chính trị.
- Một buổi chưa nói được gì về độ chính xác.
- Từ nay buổi 02/11 đã dùng để sửa luật, không còn là buổi kiểm sạch; buổi kiểm sạch tiếp theo bắt đầu từ 03/11.
- **Xem thêm ảnh** (02/11, sau khi user hỏi):
  - Chụp 15 khung bằng `cong_cu/chup_khung.py`. Script đã sửa để chạy trên Windows: khoá file bằng `msvcrt` khi không có
    `fcntl`; dùng `ffmpeg` của gói pip `imageio-ffmpeg` (cài theo yêu cầu user).
  - Hình vẽ cho thấy kế hoạch **hai hộp + hai nhánh**: hộp tím 79,4–80k để quan sát short, hộp vàng 77–78k là vùng quyết
    định. Nhánh tăng (phá kênh D1 → 81 / 86k) được vẽ kỹ ngang nhánh giảm (→ 74,2k → 67k). Lời nói nghiêng giảm.
  - **Lỗi rõ nhất của bot**: ghi "KHÔNG VÀO GIỮA 77,2–79,5k", tức đặt hộp hỗ trợ của người đó vào khoảng giữa. Hồ sơ có đủ
    căn cứ (EMA34 tuần đường giữa 77,007, Fibo 0.5 / 0.618 nhịp đang chạy 77,566 / 77,259, râu tuần test rồi đóng trên)
    nhưng bot không gom lại thành hỗ trợ.
  - Neo Fibo khác: người đó neo đỉnh nhỏ 79.820 ngay trước cú xả; hồ sơ neo pivot fractal 81.970.
  - Ghi vào ST3 E1: vùng nến tăng thẳng không có hỗ trợ ở giữa ("phải về đến tận 67") + ảnh.
  - Chưa sửa code Fibo: một buổi chưa đủ để đổi cách neo.

## Buổi live kiểm sạch: 03/11/2026 (bot trả lời 08:27–09:57, TRƯỚC buổi live 10:07)

- Bot: `doi_chieu/2026-11-03_BTC.md` (T 07:00), ETH, ZEC, VANG, XAU_OKX, XEP_HANG_20_COIN. Transcript
  [i0N3Yho0JvE](https://www.youtube.com/watch?v=i0N3Yho0JvE) tải bằng `lay_transcript.lay_phu_de` (phải đặt
  `PYTHONIOENCODING=utf-8`, không thì yt-dlp in tiêu đề cp1258 làm vỡ đọc stdout). 24 khung `so_tay/khung/i0N3Yho0JvE_*`.
- **Khớp**: BTC H4 / D1 / W1 cùng GIẢM; không short tại hỗ trợ; BTC.D lên, USDT.D đi ngang/giảm; ETH yếu hơn BTC; NEAR,
  SOL, GRAM đứng ngoài; vàng còn một nhịp về "38 mấy" (bot 3.875–3.905).
- **Lệch**:
  1. **Vùng short BTC**: người đó giữ 79,15–79,85k từ hôm qua ("tầm này gãy thì lấy được ít tiền"). Hộp = Fibo D1 nhịp
     81.970 → 76.265 (0.5 / 0.618) + EMA89 H4 + EMA34 D1 + đáy cũ đổi vai — hồ sơ có đủ. Bot đo trên nhịp H4 con
     78.866 → 76.700 → 77,9–78,05k, tức hạ vùng theo giá.
  2. **Thứ tự đường đi** (BTC và vàng): giá sát hỗ trợ → người đó cho test / quét hỗ trợ trước rồi hồi lớn; bot cho hồi nhỏ
     trước rồi về hỗ trợ. Hai mã cùng một buổi, chưa đủ để thành luật → chỉ ghi, theo dõi thêm.
  3. **Đích xa**: người đó 72k → 69–67k; bot W1 75k (vẫn đúng luật bậc thang). Vàng: người đó "đáy gần rồi", bot W1 3.700.
  4. Thiếu dữ liệu: Fibo D1 từ đỉnh đợt giảm (người đó neo 87.386 → 76.295, 0.5 = 81.840 "hồi lên 81"); cạnh dưới kênh
     giảm (đường hỗ trợ dốc xuống, ảnh `003510`); Hyblock / heatmap; tin hack Binance, rút ròng sàn / ETF.
- **Sửa** (ví dụ gắn [11-03], bộ lọc T ẩn với T ≤ 03/11):
  - NHAP_VAI §6.1 + ST3 C2: vùng vào chính đo trên nhịp D1 (hai pivot fractal D1 gần nhất), nhịp H4 con chỉ cho chỗ lướt;
    giá chưa tới thì giữ vùng qua buổi sau. Căn cứ: 11-02 + 11-03 cùng hộp 79–80k; 01-20 "giá thấp hơn vùng swing thì chỉ
    scalp"; ví dụ 10-02 (hộp 85,0–85,5k) cũng là nhịp D1.
  - ST1 C10: ví dụ 11-03 (delta −331k, heatmap 76,5k vừa bị lụm → không short tại đây).
  - ST1 C6: ví dụ 11-03 (hack → biên độ 18–20% hai chiều, nhưng không short theo tin).
- **Code** (user yêu cầu làm luôn): `ngu_canh.py` thêm hàm `nhip_sau_lon` → JSON `fibo[].nhip_sau_lon`, Markdown mục 3
  dòng "Nhịp ngược sau nhịp lớn" cho mọi khung trong `fibo`: từ cực trị cuối của nhịp lớn 90 nến tới cực trị ngược xa
  nhất sau đó. T = 03/11 07:00 D1: 87.399 → 76.265, 0.382 / 0.5 / 0.618 = 80.518 / 81.832 / 83.146 (người đó trên Binance:
  80.532 / 81.840 / 83.149). NHAP_VAI Bước 4 + §6.1 nhắc dòng này. `kiem_tra_ngu_canh.py`, `kiem_tra_so_tay_den.py` PASS.
- **Chưa làm**: trendline hỗ trợ dốc xuống / kênh giảm — phải đổi `cong_cu/trendline.py` (LOAI chỉ có kháng cự giảm và
  hỗ trợ tăng, biến thể khoá ở `hoc_v5/trendline/CHON.md`, dùng chung với `hoc_v5`) → cần thiết kế riêng; nhãn
  `hoc_v5/nhan/` cho 02/11, 03/11 (bộ nhãn khoá sha256 ở `hoc_v5/KHOA_NHAN.md`).
- Từ nay buổi 03/11 đã dùng để sửa luật; buổi kiểm sạch tiếp theo bắt đầu từ 04/11.

## Đổi nguồn dữ liệu: Binance perp cho crypto, OKX cho vàng, Chrome cho dữ liệu không có API (03/11/2026)

- User yêu cầu: dùng OKX / Binance / TradingView; cái gì không có API thì lấy bằng trình duyệt trên máy user.
- **`nen.py`**: crypto lấy Binance USDT-M perp `<MÃ>USDT` (fapi, đúng chart BTCUSDT.P Binance người đó xem) → Binance
  spot → OKX (spot / swap). Ánh xạ lưu `cache/nguon.json`; cache `binance_fapi_<SYM>_<khung>.csv/json` cùng định dạng
  OKX (khoảng giờ mở `phu`). Hai sàn cùng mốc mở nến (D1 00:00 UTC, tuần thứ Hai, tháng ngày 1) → hồ sơ không đổi cấu trúc.
  Kiểm: T = 03/11 07:00 đỉnh D1 87.385 = mức 1 Fibo người đó vẽ (87.385,7).
- **VANG**: Yahoo GC=F (futures) → OKX `XAU-USDT-SWAP` (Binance XAUUSDT perp chỉ có từ 12/2025, OKX từ 04/2025). Thiếu
  EMA200 tuần / EMA610 ngày; nến ngày theo UTC thay vì phiên New York. DAU, DXY, NASDAQ, CME vẫn Yahoo (sàn crypto không có).
- `ngu_canh.py`: `giai_nguon` thay `giai_inst`; mục gap CME + BTC.D / USDT.D theo `NG.la_crypto` (VANG không phải crypto).
- `kiem_tra_ngu_canh.py`: so `bot_v4/du_lieu` (dữ liệu OKX) bằng nến OKX dự phòng (`_chuoi_okx`); trendline so trên nến
  OKX; bỏ phép so EMA hồ sơ ↔ bot_v4 (hồ sơ giờ là Binance; EMA đã có phép tính lại độc lập ở (c)). PASS hết.
- **`chup_ngoai.py`** (mới) + `cong_cu/chup_web.mjs` ghi thêm `<tên>.txt` (chữ trên trang): Chrome ≥ 136 không cho điều
  khiển hồ sơ mặc định → mở cửa sổ Chrome riêng, hồ sơ cố định `%LOCALAPPDATA%/trade-dai-han/chrome`, cổng 9333. Trang:
  Coinglass heatmap (Binance BTC perp), thanh lý, long/short, OI, ETF, số dư sàn; TradingView CRYPTOCAP BTC.D / USDT.D H4.
  Chạy thử 03/11 ~14:00: đủ 8 trang có số thật (ETF ngày −398,6 tr USD, Binance 7 ngày −49.456 BTC, thanh lý 24h 379 tr
  USD với BTC 93,1% long, BTC.D 60,40%, USDT.D 7,026%; heatmap có cụm ~78,7k và ~76,2k).
- Chỉ dùng cho hỏi live (lúc chụp − T ≤ 4h) — NHAP_VAI §1.5, §7 C10, `/nhan-dinh` bước 4b. Backtest T quá khứ không đọc.
- **Hệ quả**: hồ sơ crypto từ nay lệch vài chục giá so với các bản OKX cũ (`doi_chieu/` trước 03/11 14:00); vàng đổi hẳn
  sản phẩm. Chưa có: Hyblock (cần tài khoản — đăng nhập một lần trong cửa sổ Chrome riêng rồi thêm URL vào `TRANG`).
