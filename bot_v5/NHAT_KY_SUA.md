
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
