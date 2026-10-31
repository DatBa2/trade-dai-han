# Bot v4 — DIỄN GIẢI chỗ thiết kế chưa nói rõ

Viết 31/10/2026, **TRƯỚC lần chạy dữ liệu thật đầu tiên** (trước đó động cơ chỉ chạy trên dữ liệu GIẢ — bước ngẫu nhiên do
script sinh ra ở thư mục nháp — để gỡ lỗi; chưa ai thấy con số lãi/lỗ nào của v4 trên dữ liệu thật).
Mỗi mục: **chỗ mơ hồ → cách chọn → vì sao**. Trong code chú thích `# DG n` trỏ về mục n dưới đây; `# TK x.y` trỏ `THIET_KE.md`.
Nguyên tắc chung khi phải chọn: (1) không nhìn trước; (2) bảo thủ với lãi/lỗ; (3) đọc sát chữ của thiết kế; (4) đơn giản để
Codex/user tự kiểm được. KHÔNG mục nào được chọn theo kết quả lãi/lỗ.

## A. Dữ liệu và thời gian

**DG 1 — Giờ đóng nến D1.** File chỉ có `ts_utc` (giờ MỞ). → Crypto (OKX 1Dutc): đóng = ts + 24h. Vàng/dầu (Yahoo, phiên CME):
`tai_du_lieu.py` ghi ts = 17:00 New York của ngày giao dịch − 23h, nên đóng = **ts + 23h** (= 17:00 NY, 21:00/22:00 UTC).
Vì sao: đúng cách file được tạo; không dùng "ts của phiên kế" vì lúc cắt dữ liệu phiên kế chưa có (nhìn trước).
H4: đóng = ts + 4h cho mọi tài sản.

**DG 2 — W1 dựng từ D1.** → Mỗi nến D1 thuộc tuần (thứ Hai 00:00 UTC) chứa **ngày giao dịch** của nó: crypto = ngày UTC của
ts; vàng/dầu = ngày UTC của (ts + 2h) (phiên thứ Hai mở 22:00/23:00 UTC Chủ nhật → thuộc tuần mới). W1: open = open D1 đầu,
high/low = max/min, close = close D1 cuối. **Giờ đóng W1 = thứ Hai 00:00 UTC tuần sau** (ranh giới tuần). Tuần chưa trọn
không bao giờ được dùng (giờ đóng > t). Tuần đầu dữ liệu có thể thiếu ngày đầu tuần (dữ liệu bắt đầu thứ Tư) — giữ lại vì
pha chỉ dùng close W1 và EMA của close. Vì sao: theo chỉ đạo điều phối (gán theo ngày giao dịch) và TK 1 "tuần bắt đầu thứ Hai".

**DG 3 — Pha ban đầu / giai đoạn khởi động.** EMA89 W1 cần 89 tuần → với dữ liệu từ 06/2022, EMA89 W1 của BTC chỉ có từ
~02/2024 (tức là trong kỳ 2024). → Máy trạng thái pha chạy liên tục từ nến W1 đầu tiên có EMA34: **khi chưa có lần nào điều kiện
TĂNG/GIẢM được thoả** (kể cả vì EMA89 chưa có) thì pha = close W1 so với EMA34 W1, tính lại mỗi tuần; **lần đầu điều kiện được
thoả** thì pha khoá theo điều kiện đó, từ đó chỉ đổi khi 2 W1 liên tiếp thoả điều kiện ngược (TK 3). Vì sao: đúng câu "nếu chưa
có điều kiện nào → theo close W1 so với EMA34 W1"; chạy liên tục từ đầu dữ liệu nên pha không phụ thuộc năm bắt đầu chạy
(2024/2025/2026 cho cùng pha ở cùng thời điểm) và không nhìn trước.

**DG 4 — Kỳ chạy.** → Năm Y: quyết định tại giờ đóng H4 t với 01/01/Y 00:00 UTC ≤ t < 01/01/(Y+1) 00:00 UTC
(2026: t < 31/10/2026 00:00 UTC = hết 30/10). Nến được quản lý tới giờ đóng ≤ hết kỳ; lệnh còn mở → `HET_KY` ở close nến
cuối cùng (giờ đóng ≤ hết kỳ) của tài sản đó; lệnh chờ chưa khớp → `HUY` (ly_do_huy `het_ky`). Không đặt lệnh tại đúng giờ
hết kỳ. Vì sao: "từ 01/01/Y 00:00 tới 31/12/Y" — quyết định đầu dùng nến 20:00–24:00 ngày 31/12 năm trước (đã đóng).

**DG 5 — Thiếu dữ liệu chỉ báo.** VÀNG/DẦU 4H chỉ có từ 2024-06-10, BNB từ 2022-12-21. → (a) View cần: pha W1, EMA34c/89/200 H4,
RSI14 D1; thiếu cái nào → view `CHUA_DU`, không lệnh, `ly_do_bo = thieu_du_lieu`. (b) **Đặt lệnh** (chính hoặc hồi) cần ĐỦ mọi
đại lượng của TK 5.1/5.3: dải EMA34 H4 (trên/dưới/giữa), EMA89/200/**610** H4, ATR14 H4, dải EMA34 D1, EMA89/200 D1; thiếu → không
lệnh, `ly_do_bo = "thieu_du_lieu: <tên>"`. Vì sao: chỉ đạo điều phối ("tài sản chưa đủ dữ liệu để tính EMA cần dùng thì KHÔNG đặt
lệnh"); không đặt lệnh với bộ mức thiếu (bản luật khác). Hệ quả: VÀNG/DẦU cần 610 nến H4 (~5 tháng giao dịch) → gần như không
có lệnh năm 2024 (chỉ có thể từ ~11/2024).

**DG 25 — Đường vốn `von.csv`.** → Một dòng mỗi giờ đóng H4 (hợp các giờ đóng của rổ) trong kỳ; `ts_utc` = **giờ ĐÓNG** nến;
`von` = số dư đã chốt + lãi/lỗ chưa chốt của vị thế đang mở theo close (chưa trừ phí ra); `von_chot` = số dư đã chốt;
`so_vi_the_mo`. Sụt giảm max tính trên `von` (kể cả đỉnh ban đầu 4.000$). Vì sao: sụt giảm phải thấy lỗ chưa chốt.

**DG 26 — Dữ liệu bị cắt (`cat_tai`, nhận định trực tiếp).** → Khi dữ liệu kết thúc TRƯỚC hết kỳ vì bị cắt, lệnh chưa xong giữ
trạng thái `DANG_CHO` (chưa khớp) / `DANG_MO` (đang mở), KHÔNG tự đóng `HET_KY`. Vì sao: nếu đóng giả ở nến cuối thì quyết định
ở nến cuối thấy "đã hết lệnh" → khác bản đủ (đây chính là lỗi kiểm cắt cụt bắt được trên dữ liệu giả); và nhận định trực tiếp cần
thấy lệnh đang mở. `HET_KY` chỉ khi thật sự hết kỳ.

**DG 27 — Mốc quyết định.** → Mỗi tài sản chỉ quyết định tại giờ đóng nến H4 CỦA NÓ (vàng/dầu không có nến cuối tuần / giờ nghỉ
→ không quyết định lúc đó). Dòng thời gian của rổ = hợp các giờ đóng. `quyet_dinh.csv` có 1 dòng cho mỗi (giờ đóng, tài sản có
nến đóng lúc đó).

## B. View (TK 3, TK 4)

**DG 6 — PHÂN VÂN "close nằm giữa min và max của 3 đường".** → Tính cả biên (min ≤ close ≤ max); 2 khoảng cách chia cho close H4.
Vì sao: không có lý do loại biên; xác suất bằng đúng biên ~0.

**DG 17 — "Huỷ sớm nếu view đổi".** → So **nhãn view** (TANG/GIAM/PHAN_VAN/CHUA_DU) ở mỗi lần đóng H4 sau khi đặt với nhãn lúc
đặt; khác → huỷ tại giờ đóng đó. Trong 1 nến: xét khớp trước (khớp xảy ra trong nến), chưa khớp mới huỷ ở giờ đóng. Đổi kiểu
(HỒI ↔ THUẬN) mà nhãn giữ nguyên (vd pha đổi GIẢM→TĂNG trong lúc lệnh hồi LONG đang chờ) → không huỷ. Áp dụng cho cả lệnh hồi.
Vì sao: đọc sát chữ "view đổi"; view là nhãn hướng H4.

## C. Mức, vùng, lệnh (TK 5.1 – 5.3, TK 6)

**DG 7 — Fractal khi high bằng nhau.** → Đỉnh ở i nếu h_i > max(3 nến trái) và h_i ≥ max(3 nến phải) (2 đỉnh bằng nhau liền kề
→ chỉ nến sớm hơn). Đáy đối xứng. Vì sao: tránh đếm trùng 1 đỉnh 2 lần; cách phổ biến (Bill Williams, backtest v1).

**DG 8 — "Gần nhất" của fractal.** → Theo **thời gian** (mới nhất) cho: A của nhịp, 3 đỉnh/đáy H4, 1 đỉnh/đáy D1, 3 mức S/R đổi
vai. Lấy N cái mới nhất TRƯỚC, rồi mới lọc theo khoảng (0,3%; 6%] (cái nằm ngoài khoảng bị bỏ, không thay bằng cái cũ hơn).
Vì sao: "nhịp H4 hiện tại" rõ ràng là theo thời gian; dùng cùng nghĩa cho cả mục để nhất quán.

**DG 9 — S/R đổi vai.** → SHORT: đáy fractal H4 đã xác nhận có giá **> close H4 hiện tại** (close hiện tại đã nằm dưới → đã bị
xuyên xuống, nay nằm trên giá); lấy 3 cái mới nhất thoả. LONG: đỉnh fractal H4 đã xác nhận có giá < close hiện tại.
Vì sao: "đã bị close H4 xuyên xuống" + "nay nằm trên giá" ⇔ giá đáy > close hiện tại (close hiện tại là 1 close H4 sau đáy).

**DG 10 — Nhịp Fibo A–B.** → B = low thấp nhất (SHORT) / high cao nhất (LONG) của các nến **sau** nến A tới nến hiện tại (gồm
nến hiện tại). Hợp lệ khi |A − B| ≥ 1,5 × ATR14 H4 **tại nến quyết định**. Mức Fibo = B + r·(A − B), r ∈ {0,5; 0,618}.
Vì sao: "từ A tới nay"; low của chính nến đỉnh không thuộc nhịp giảm sau đỉnh.

**DG 11 — Khoảng cách % và cách gom cụm.** → Mọi % ở 5.1/5.2 (khoảng (0,3%; 6%], 0,5%, 1%) chia cho **close H4 hiện tại**.
Gom: xếp mức từ GẦN giá nhất ra xa; mức kế tiếp vào cụm nếu cách mức liền trước ≤ 0,5% VÀ cách mức đầu cụm (gần giá nhất) ≤ 1%;
không thì mở cụm mới. Vì sao: "cụm liên tiếp, độ rộng ≤ 1%" + "chọn cụm gần giá nhất" → gom tham lam từ phía giá; 1 mẫu số chung
để dễ kiểm.

**DG 12 — Loại căn cứ (điểm).** → 10 loại: EMA34_H4 (biên trên cho SHORT / dưới cho LONG), EMA89_H4, EMA200_H4, EMA610_H4,
EMA34_D1 (biên tương ứng), EMA89_D1, EMA200_D1, FIBO_0.5, FIBO_0.618, FRACTAL (gộp đỉnh/đáy H4 + đỉnh/đáy D1 + S/R đổi vai).
Vì sao: "mỗi EMA tính riêng 1; Fibo mỗi cái 1; đỉnh/đáy fractal tính 1 cho cả nhóm".

**DG 13 — Số tròn.** → Bội số gần nhất của bước (BTC 1.000; ETH 100; BNB 10; OKB 1; vàng 50; dầu 1) so với **giá giữa cụm**;
nếu |giữa − bội| ≤ 0,1% × giữa → giá vào = giữa × (1 − 0,15%) cho SHORT / × (1 + 0,15%) cho LONG (về phía giá hiện tại), 1 lần.
Vì sao: đọc sát TK 5.3.

**DG 14 — Thứ tự tính SL.** → SL = mép xa của cụm ± max(0,3% × **giá vào sau khi lùi số tròn**, 0,5 × ATR14 H4 tại nến quyết
định); nếu khoảng SL/giá vào < SL tối thiểu của tài sản → SL = giá vào ± SL tối thiểu; sau đó khoảng SL/giá vào > 6% → bỏ lệnh.
Vì sao: "khoảng SL tối thiểu" là sàn áp sau công thức; điều kiện bỏ xét trên SL cuối.

**DG 15 — TP bất thường.** → (a) Nếu sau các luật TK 5.3 TP1 không nằm giữa giá vào và TP2 (TP1 ≥ TP2 tính theo hướng có lợi) →
TP1 = giá vào ± 1R (giống luật "TP1 < 0,5R → 1R"). (b) TP2 ≤ 0 → bỏ lệnh. TP1 = B × (1 ± 0,2%) (non 0,2% của B về phía giá vào).
Vì sao: TP1 ở sau TP2 là vô nghĩa (chốt 50% sau khi lẽ ra đã ra hết); dùng lại giá trị thay thế có sẵn trong thiết kế.

**DG 16 — Lệnh hồi dùng cơ chế nào của 5.3.** → Cùng: liệt kê mức + gom cụm (5.1–5.2, đối xứng), giá vào giữa cụm + lùi số tròn,
SL (kể cả sàn SL và bỏ > 6%), hiệu lực 6 nến, huỷ khi view đổi, khớp/phí/trượt/thứ tự trong nến (TK 7). Khác: rủi ro 1%, TP duy
nhất = EMA34(close) H4 tại nến đặt, cần (TP − vào)/khoảng SL ≥ 1,5 (theo hướng lệnh), chốt 100% ở TP (`ly_do_ra = TP`), dừng 48h,
không TP1, không dời SL. Vì sao: TK 6 chỉ nêu phần khác; phần còn lại "như 5.x".

## D. Khớp lệnh, quản lý, vốn (TK 5.3, TK 7)

**DG 18 — Giá khớp limit khi nến mở đã vượt.** → Limit vào lệnh: nến mở đã vượt giá limit theo hướng có lợi (SHORT: mở > limit;
LONG: mở < limit — chỉ xảy ra khi gap, vd vàng/dầu đầu tuần) → khớp ở **giá mở**. TP (limit) tương tự: mở đã vượt TP → khớp giá
mở. SL: theo TK 7 (gap qua SL → giá mở). Vì sao: lệnh limit trên sàn khớp ở giá tốt hơn khi giá nhảy qua; đối xứng với luật gap SL.
Khối lượng vẫn giữ như lúc đặt.

**DG 19 — Giờ của sự kiện và dừng theo giờ.** → Chỉ có OHLC 4H nên mọi sự kiện (khớp, TP1, ra, huỷ) ghi theo **giờ ĐÓNG** của
nến xảy ra sự kiện; `chay` chỉ cộng tiền / giải phóng chỗ tại giờ đó. Dừng theo giờ: hạn = giờ đóng nến khớp + 120h (hồi 48h);
ra (market) ở close của nến đầu tiên có giờ đóng ≥ hạn (crypto: nến khớp + 30 / + 12). Vì sao: không biết giờ khớp trong nến;
giờ đóng là lúc chắc chắn biết.

**DG 20 — Thứ tự trong 1 nến (sau nến khớp).** → (1) SL hiện tại (gap → giá mở); (2) lệnh chính chưa TP1 mà chạm TP1 → chốt 50%
ở TP1, dời SL về **giá khớp**; nếu cùng nến đó giá cũng đã chạm giá khớp → phần còn lại ra hoà vốn (`SL_HOA_VON`, bảo thủ);
(3) chạm TP2 (lệnh chính đã TP1) / TP (lệnh hồi) → ra hết; (4) dừng theo giờ ở close; (5) hết kỳ ở close.
Nến khớp: chỉ xét SL (TK 7). Vì sao: TK 7 "chạm cả TP và SL → SL trước (bảo thủ)" áp cả cho SL hoà vốn mới dời.

**DG 21 — Trượt giá.** → Mọi lệnh ra market (SL, SL hoà vốn, dừng theo giờ, hết kỳ): giá ra = giá kích hoạt × (1 + 0,02%) cho
SHORT (mua lại đắt hơn) / × (1 − 0,02%) cho LONG; phí 0,05% tính trên giá sau trượt. Vào lệnh và TP (limit): không trượt, phí
0,02%. `gia_ra` trong `lenh.csv` là giá SAU trượt.

**DG 22 — Khối lượng, đòn bẩy, ký quỹ.** → Rủi ro$ = 2% (hồi 1%) × **số dư đã chốt** tại lúc đặt lệnh (không tính lãi/lỗ chưa
chốt). Khối lượng = rủi ro$ / |giá đặt − SL|, cố định từ lúc đặt. Đòn bẩy = min(40% / SL%, 20) với SL% theo giá đặt; ký quỹ =
khối lượng × giá đặt / đòn bẩy. Kiểm "ký quỹ tổng ≤ 50% vốn" lúc đặt: ký quỹ mọi lệnh đang chiếm chỗ (lệnh chờ tính đủ, vị thế
đã chốt TP1 tính 50%) + lệnh mới ≤ 50% × số dư đã chốt; vượt → bỏ lệnh mới (`ky_quy_vuot_50%`). `R` = lai_usd / rủi ro$ dự kiến.

**DG 23 — Thứ tự xét khi nhiều tài sản cùng giờ.** → Trong 1 giờ đóng: trước hết cộng mọi sự kiện có giờ ≤ t (theo thứ tự lệnh
được đặt), rồi xét tài sản theo thứ tự `TAI_SAN` = BTC, ETH, OKB, BNB, VÀNG, DẦU (giới hạn 3 lệnh làm thứ tự này có ảnh hưởng).
Lệnh vừa ra / vừa huỷ ở t thì tài sản đó được xét đặt lệnh mới ngay tại t. Vì sao: cố định, đơn giản, không phụ thuộc kết quả.

**DG 24 — Thống kê.** → "Số lệnh" = lệnh đã khớp (không tính HUY); "thắng" = lai_usd > 0 (lệnh TP1 rồi hoà vốn thường dương →
thắng); hệ số LN = Σ lãi dương / |Σ lãi âm|.

## E. Khác

**DG 28 — Khởi tạo RSI/ATR Wilder.** → RSI n: TB lãi/lỗ đầu = trung bình cộng n thay đổi đầu → giá trị đầu ở nến thứ n+1 (chỉ số
n); sau đó TB = (TB·(n−1) + giá trị)/n; lỗ TB = 0 → 100. ATR n: TR nến đầu = H − L; ATR đầu = trung bình n TR đầu (chỉ số n−1);
sau đó Wilder. Vì sao: cách Wilder/TradingView phổ biến; TK 2 chỉ ghi "Wilder".

**DG 29 — `view_tai`.** → Cắt dữ liệu tại t rồi tính lại toàn bộ, trả view của lần đóng H4 cuối ≤ t; `gio_cat` = giờ đóng nến
đó (datetime UTC). Vì sao: bảo đảm nhận định / chấm độ giống không thể dùng dữ liệu sau t.

**DG 30 — Cột thêm trong `lenh.csv`.** → Sau 19 cột bắt buộc của TK 8 có thêm: `gia_dat` (giá limit), `gia_tp1` (giá khớp TP1),
`ti_le_tp1` (0,5 hoặc 0), `rui_ro_usd`, `ky_quy`, `gio_dung`, `ly_do_huy`, `vung`, `ghi` — để tự cộng lại:
lai_usd = kl·ti_le_tp1·(gia_tp1 − gia_vao)·x + kl·(1 − ti_le_tp1)·(gia_ra − gia_vao)·x − phi (x = +1 LONG / −1 SHORT).
Lệnh HUY: gia_vao trống, lãi 0, t_ra = giờ huỷ. Giờ trong CSV = giờ ĐÓNG nến, UTC, "YYYY-MM-DD HH:MM".

**DG 31 — Funding.** Bỏ qua (TK 7), không tính phí qua đêm.
