# BOT V4 — thiết kế CHỐT (31/10/2026, khoá sha256 ở `bot_v4/KHOA.md` TRƯỚC khi chạy backtest)

> Người viết: Claude (điều phối). Code do subagent viết ĐÚNG theo file này. Chỗ nào file này chưa nói → ghi cách hiểu vào
> `bot_v4/DIEN_GIAI.md` TRƯỚC lần chạy dữ liệu thật đầu tiên. Mọi thay đổi code sau lần chạy thật đầu tiên → ghi
> `bot_v4/NHAT_KY_SUA.md` (vì sao, trước/sau, kết quả mọi năm trước và sau sửa). KHÔNG đổi tham số vì thấy kết quả.

## 0. Mục tiêu và giới hạn trung thực
- v4 = **luật máy** bắt chước cách người đó ra quyết định + bài học từ bài thi v3 (`thi/BAO_CAO_XU_LY_P0.md`).
  Đo 2 thứ: (1) **lãi/lỗ** vốn 4.000$; (2) **độ giống** hướng H4 với người đó trên 180 buổi.
- Không dùng Claude suy luận cho backtest: model biết giá tới ~06/2026 → rò rỉ; và chi phí.
- Giai đoạn: **2024** (kiểm phụ — chưa ai nhìn kết quả bất kỳ bot nào trên 2024), **2025**, **2026** (01/01 → 30/10).
  Trung thực: luật lấy từ các buổi live 2026 → **2026 là trong mẫu**. Tôi (Claude) đã thấy kết quả v1/v2 trên 2025 (cả phân
  tích từng thành phần) → **2025 không còn ngoài mẫu tuyệt đối**; v4 KHÔNG chọn thành phần theo kết quả đó (mọi luật dưới đây
  có nguồn ở sổ tay / bài thi, ghi ở cột "Nguồn"). 2024 là năm sạch nhất. Kết luận thật chỉ có ở **buổi live mới từ 02/11**.
- Tài sản: **BTC, ETH, OKB, BNB, VÀNG (GC=F), DẦU (CL=F)** — cùng rổ v1/v2 để so; báo thêm riêng **BTC**.

## 1. Dữ liệu
- Nến 4H + 1D mỗi tài sản, `ts_utc` = giờ MỞ nến UTC, cột `ts_utc,open,high,low,close,vol`, từ **2022-06-01** (khởi động EMA)
  tới 2026-10-30 → `bot_v4/du_lieu/<TS>_{4H,1D}.csv` + `bot_v4/du_lieu/SHA256SUMS`. Crypto: OKX (USDT spot), vàng/dầu: Yahoo
  (cùng nguồn v1/v2, xem `backtest/tai_du_lieu.py`). W1 dựng từ 1D: tuần bắt đầu thứ Hai 00:00 UTC.
- Quyết định chỉ tại lúc **ĐÓNG nến H4**, chỉ dùng nến đã đóng (H4 ≤ t; D1 đã đóng ≤ t; W1 đã đóng ≤ t). Nến đang chạy KHÔNG dùng.
- Kỳ chạy năm Y: quyết định từ 01/01/Y 00:00 UTC tới 31/12/Y (2026: tới 30/10 cuối ngày); lệnh còn mở lúc hết kỳ đóng ở close cuối.

## 2. Chỉ báo (module chung `cong_cu/chi_bao.py`, có kiểm thử)
| Chỉ báo | Định nghĩa |
|---|---|
| EMA n | đệ quy α = 2/(n+1), khởi tạo = SMA n nến đầu; chưa đủ n nến → None |
| Dải EMA34 | EMA34 của high / low / close (biên trên / dưới / giữa) |
| EMA89/200/610 | của close |
| RSI14 | Wilder |
| ATR14 | Wilder, True Range |
| Fractal | đỉnh: high lớn nhất của 7 nến (3 trái, 3 phải); đáy tương tự với low. **Chỉ dùng sau khi nến phải thứ 3 đã đóng** |

## 3. Tầng 0 — PHA chu kỳ (W1) · Nguồn: sổ tay A0, L01, L03, L07
- Tại mỗi lần đóng W1: điều kiện TĂNG = close W1 > EMA34(close) W1 **và** EMA34 W1 > EMA89 W1; GIẢM = close < EMA34 và EMA34 < EMA89.
- Đổi pha chỉ khi **2 nến W1 liên tiếp** thoả điều kiện pha ngược (công tắc 2 cây, L07); còn lại giữ pha cũ. Pha ban đầu = pha
  tính được ở cuối giai đoạn khởi động (nếu chưa có điều kiện nào → theo close W1 so với EMA34 W1).

## 4. Tầng 1 — VIEW H4 (dùng cho lệnh + chấm độ giống) · Nguồn: A0, L05, L06 + bài thi v3
Bài học bài thi v3 (bắt buộc): (a) người đó **giữ view thuận pha rất dai** — nến đóng qua mốc sai KHÔNG làm đổi view
(12/14 lỗi chính của v3); (b) bot v3 **PHÂN VÂN thừa** (14 vs 7) → PHÂN VÂN chỉ ở điều kiện hẹp; (c) SL bot v3 quá sát (30 lần dính SL).
Thứ tự xét tại mỗi lần đóng H4:
1. **PHÂN VÂN** khi đồng thời: |EMA34c − EMA89| / close < 0,6% **và** |EMA89 − EMA200| / close < 0,6% (H4) **và** close H4 nằm
   giữa min và max của 3 đường đó. (L35, hẹp có chủ đích.)
2. **HỒI (ngược pha)**: pha GIẢM và RSI14 D1 (nến D1 đã đóng gần nhất) ≤ 30 → view **TĂNG** (hồi kỹ thuật). Pha TĂNG và RSI14 D1 ≥ 70 →
   view **GIẢM** (điều chỉnh). (A0 "TĂNG = hồi kỹ thuật", L33.)
3. Còn lại: view = **hướng pha** (GIẢM nếu pha GIẢM, TĂNG nếu pha TĂNG). KHÔNG đổi view vì nến H4/D1 đóng qua mốc (bài học a).

## 5. Lệnh THUẬN PHA (lệnh chính) · Nguồn: L19, L20, L24, L28, L29, L30, L32, A5
Xét tại mỗi lần đóng H4 khi view = hướng pha, tài sản không có vị thế và không có lệnh chờ.
**5.1 Mức kháng cự (cho SHORT; LONG đối xứng: mức hỗ trợ dưới giá)** — chỉ lấy mức nằm trong (0,3%; 6%] phía trên close H4:
- EMA H4: dải EMA34 biên trên, EMA89, EMA200, EMA610. EMA D1: dải EMA34 biên trên, EMA89, EMA200.
- Fibo thoái lui 0,5 và 0,618 của nhịp H4 hiện tại: A = đỉnh fractal H4 đã xác nhận gần nhất, B = low thấp nhất từ A tới nay
  (râu); chỉ dùng khi A − B ≥ 1,5 × ATR14 H4. (LONG: A = đáy fractal gần nhất, B = high cao nhất từ A.)
- 3 đỉnh fractal H4 đã xác nhận gần nhất + 1 đỉnh fractal D1 gần nhất (râu); **S/R đổi vai**: 3 đáy fractal H4 gần nhất đã bị
  close H4 xuyên xuống (nay nằm trên giá).
**5.2 Vùng hội tụ** — gom các mức cách nhau ≤ 0,5% (cụm liên tiếp, độ rộng cụm ≤ 1%). Điểm = số LOẠI căn cứ khác nhau trong cụm
(mỗi EMA tính riêng 1; Fibo 0,5 và 0,618 mỗi cái 1; đỉnh/đáy fractal tính 1 cho cả nhóm). Cần **≥ 2**. Chọn cụm GẦN giá nhất đạt ≥ 2.
**5.3 Lệnh** — limit tại GIỮA cụm; nếu cách bội số tròn (BTC 1.000; ETH 100; BNB 10; OKB 1; vàng 50; dầu 1) ≤ 0,1% giá → lùi 0,15%
về phía giá hiện tại (vào "non", L29). Hiệu lực **6 nến H4**; huỷ sớm nếu view đổi. Khớp khi nến SAU nến đặt lệnh chạm giá limit.
- **SL** = mép xa của cụm + max(0,3% × giá vào, 0,5 × ATR14 H4); khoảng SL tối thiểu theo tài sản: BTC/ETH 1,2%, OKB/BNB 2%,
  vàng 0,8%, dầu 1,5% (L30 "SL tối thiểu ~1.000 giá"); SL > 6% → bỏ lệnh. SL theo GIÁ chạm (lệnh dừng thật trên sàn).
- **TP** (Fibo Eric 3 điểm, L18/L32): với SHORT: A, B như 5.1, C = giá vào; TP2 = C − 1,618 × (A − B); TP1 = B (cản gần nhất),
  đặt non 0,2% về phía giá vào. Nếu nhịp không hợp lệ (A − B < 1,5 ATR) → TP2 = giá vào − 2,5 × khoảng SL, TP1 = giá vào − 1 × khoảng SL.
  **Bỏ lệnh nếu (TP2 − vào)/SL < 2** (L32). TP1 < 0,5R → TP1 = 1R.
- Quản lý: chạm TP1 → chốt 50%, dời SL về giá vào (A5); phần còn lại ra ở TP2 / SL hoà vốn / **dừng theo giờ 120 giờ** từ lúc khớp.

## 6. Lệnh HỒI (ngược pha) · Nguồn: L33, A0
- Khi view = HỒI (mục 4.2): tìm vùng hội tụ phía dưới giá (LONG) / phía trên (SHORT) như 5.1–5.2 (cùng danh sách mức, đối xứng).
- Rủi ro **1%** (một nửa lệnh chính). SL như 5.3. **TP duy nhất** = EMA34(close) H4 tại lúc đặt lệnh; cần TP ≥ 1,5R, không thì bỏ.
  Dừng theo giờ **48 giờ**. Không TP1/dời SL.

## 7. Quản lý vốn và khớp lệnh · Nguồn: A5, BAI_HOC D
- Vốn đầu **4.000$**, mỗi năm chạy lại từ 4.000$. Rủi ro lệnh chính **2%** vốn hiện tại (cùng v1/v2 để so), lệnh hồi 1%.
- Khối lượng = rủi ro$ / khoảng SL. Đòn bẩy = min(40% / SL%, 20) (an toàn thanh lý, BAI_HOC D). Tối đa **3** vị thế + lệnh chờ
  cùng lúc trên cả rổ; mỗi tài sản tối đa 1. Ký quỹ tổng ≤ 50% vốn — vượt thì bỏ lệnh mới.
- Phí: vào (limit) 0,02%; TP (limit) 0,02%; SL / dừng theo giờ / đóng cuối kỳ (market) 0,05% + **trượt giá 0,02%**. Bỏ funding (ghi rõ).
- Thứ tự trong 1 nến (chỉ có OHLC 4H): nến vừa khớp lệnh → chỉ xét SL (không TP) trong nến đó; nến chạm cả TP và SL → tính SL
  trước (bảo thủ); giá mở nến đã vượt SL (gap vàng/dầu) → khớp ở giá mở.

## 8. Đầu ra bắt buộc (để Codex/user tự cộng lại)
- `bot_v4/ket_qua/<nam>_<ro>/lenh.csv`: tai_san, loai (chinh|hoi), chieu, t_quyet_dinh, t_khop, gia_vao, sl, tp1, tp2, t_tp1,
  t_ra, gia_ra, ly_do_ra (TP2|TP|SL|SL_HOA_VON|HET_GIO|HET_KY|HUY), khoi_luong, don_bay, phi, lai_usd, R, von_sau.
- `von.csv` (đường vốn mỗi nến H4), `quyet_dinh.csv` (mỗi lần đóng H4 × tài sản: pha, view, lý do, vùng chọn hoặc lý do bỏ).
- `bot_v4/KET_QUA.md`: bảng năm × rổ (6 tài sản / riêng BTC): lãi$, %, số lệnh, % thắng, R TB, sụt giảm max, hệ số LN; theo tài
  sản; lệnh chính vs hồi; so **v1/v2** (số trong `backtest/KET_QUA_NGOAI_MAU.md`, `KET_QUA_V2.md`) và **mua-giữ BTC**;
  **giả dược**: 1.000 lần, mỗi lệnh thật thay bằng lệnh cùng tài sản/chiều/khoảng SL/TP (theo R)/giờ dừng nhưng thời điểm vào ngẫu
  nhiên trong cùng năm → phân vị của kết quả thật.
- **Độ giống**: view BTC tại C (lúc kết thúc live, `transcripts/gio_live.tsv`) của 180 buổi vs nhãn người đó (T1–T6: `phieu/`;
  T7–T10: `thi/dap_an_v2/phieu/`), cùng mẫu số với "luôn GIẢM" và luật từ trên xuống; ghi rõ là TRONG MẪU.

## 9. Kiểm tra bắt buộc (`python3 bot_v4/kiem_tra.py`, phải PASS trước khi báo kết quả)
1. Cắt cụt: 20 mốc T ngẫu nhiên (hạt giống cố định) — chạy với dữ liệu cắt tại T cho quyết định/lệnh trước T **giống hệt** bản đủ.
2. Fractal chỉ dùng sau 3 nến phải đã đóng; D1/W1 chỉ dùng nến đã đóng (kiểm bằng ca dựng tay).
3. EMA/RSI/ATR so với tính tay trên chuỗi nhỏ.
4. Cộng lại lãi/lỗ từ `lenh.csv` khớp `von.csv` tới 0,01$.
5. Tình huống khớp lệnh mục 7 (nến khớp + chạm SL; chạm cả TP và SL; gap qua SL).

## 10. Chạy lại (1 lệnh mỗi việc)
- `python3 bot_v4/tai_du_lieu.py` → dữ liệu + SHA256SUMS · `python3 bot_v4/kiem_tra.py` · `python3 bot_v4/chay.py --nam 2024|2025|2026 [--ro 6|BTC]`
- `python3 bot_v4/bao_cao.py` → `KET_QUA.md` (gọi chay + giả dược + độ giống) · `python3 bot_v4/nhan_dinh.py` → view + lệnh hiện tại
  (cùng động cơ, cho lệnh giấy / thi buổi live mới; ghi `gio_cat` = nến H4 đóng cuối cùng dùng, `gio_phat_hanh` riêng).

## 11. Không làm trong v4 (ghi rõ để không ai tưởng đã làm)
Tin tức/lịch kinh tế, Hyblock, heatmap, F&G, USDT.D, vàng-dẫn-BTC, gap CME, mô hình giá, tín hiệu M5/M30, chia nhiều entry,
reset tài khoản cuối tuần, funding. (Lý do: không có dữ liệu lịch sử đáng tin, hoặc luật chỉ xuất hiện 1 lần.)
