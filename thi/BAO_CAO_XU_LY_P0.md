# Xử lý P0 theo báo cáo Codex (`kiem_cheo/TONG_QUAN_VA_THIEU_SOT_2026-10-31.md`) — 31/10/2026

## 0. Giữ nguyên lượt thi cũ
- `thi/_snapshot_v3_chan_doan/`: 77 hồ sơ, 77 bài làm, đáp án v1 (`phieu/`, `moc/`), mã chấm/dựng đề cũ, sổ tay thi, dữ liệu giá,
  `PROMPT_THI.md` (prompt + model + tự khai của agent), `MANIFEST.sha256` (587 file), `KET_QUA_CHAM_CU.md` (chấm bằng bộ chấm cũ,
  băm khớp `KHOA_CHAM.md` v1). Lượt này = **chẩn đoán**, không dùng để kết luận độc lập.

## 1. Đã sửa gì, kiểm bằng gì
| P0 | Sửa | Kiểm chứng |
|---|---|---|
| 1. Đáp án lệch định nghĩa / bất đồng | Đáp án v2: Opus rút MÙ 80 buổi (77 thi + 3 tranh chấp), schema tách hướng / chặng kế tiếp / đường đi / đích / hành động / vô hiệu có cấu trúc + câu trích. Luật chốt TRƯỚC: `dap_an_v2/QUY_TAC_PHAN_XU.md`; bảng `PHAN_XU.md`; khoá `KHOA_DAP_AN.md` | v1 = v2: 64/77 (TĂNG/GIẢM v1 giữ 58/60; lệch chủ yếu ở 16 PHÂN VÂN cũ → 5 TĂNG / 5 GIẢM / 6 PHÂN VÂN). Codex khớp v2 **17/19**, khớp v1 13/19; 19/05 và 23/10 (v1 lệch hẳn) v2 = Codex |
| 2. Giá tham chiếu nhìn trước | Giá = close nến 5m đã đóng ≤ C; quét từ nến 5m mở ≥ C (`du_lieu/btc_5m.csv`, 87.305 nến) | kt5 PASS |
| 3. Vô hiệu sai khung / bỏ nến đóng đầu | `cong_cu/dieu_kien.py` dùng chung chấm + đề: khung H4/D1/W1, 2 nến, nến mở trước C đóng sau C được tính; vế khung nhỏ chỉ bỏ đoạn đó. Đề sửa → `thi/ho_so_v2/` | kt1, kt2, kt3, kt6 PASS; cắt tương lai 77/77 giống hệt; 19 hồ sơ hết báo nhầm "ĐÃ KÍCH HOẠT" (khớp Codex) |
| 4. TP + SL cùng nến = ĐÚNG | Cùng nến 5m → xét 1m; vẫn cùng → CHƯA RÕ THỨ TỰ; báo riêng đúng ĐƯỜNG ĐI | kt4, kt8 PASS; dữ liệu thật: 0 ca cùng nến |
| P1-10 (cùng file) | Đối xứng thật (view đi ngược báo riêng); bootstrap khối tuần + KTC chênh lệch cặp; thiếu bài = sai | kt7 PASS |
Chi tiết file:dòng + hồi quy 180 phiếu: `thi/SUA_P0.md`. Kiểm thử: `python3 thi/kiem_thu_cham.py` → 8/8 PASS (cài lại lỗi cũ → 8/8 FAIL).
Khoá bộ chấm v2: `thi/KHOA_CHAM.md` (mục "Khoá v2"; khoá v1 giữ nguyên).

## 2. Kết quả bài thi v3 (bài làm cũ) — 3 cách chấm đã chốt trước
| Đáp án | Số buổi | **Bot** | Luôn GIẢM | Giữ view | Luật từ trên xuống | Chép buổi trước |
|---|---|---|---|---|---|---|
| (a) v1 Sonnet | 76 | 57% | 58% | 55% | 58% | 51% |
| **(b) v2 rút mù — chính** | 77 | **60%** | 64% | 65% | 61% | 60% |
| (c) đồng thuận v1 = v2 (= Codex) | 64 | 62% | 67% | 67% | 64% | 61% |
- KTC 95% chênh lệch cặp (khối tuần, v2): bot − luôn GIẢM −4 điểm (−19…+15), bot − giữ view −5 (−14…+5) → **bot KHÔNG hơn mốc đơn giản nào**.
- Đúng thị trường (đích trước SL/vô hiệu, 14 ngày, v2): **bot 20/62 = 32%** · người đó 34/65 = 52% · giữ view 53%. Bot dính SL 30 lần.
- Bắt lúc người đó đổi view (±1 buổi): bot 23/31 = 74% (cùng buổi 10) — tốt hơn giữ view (0 cùng buổi).

## 3. Bot sai ở đâu (v2, bảng chéo)
| Kiểu lệch | Số buổi | Ghi chú |
|---|---|---|
| Người GIẢM → bot TĂNG | **14** | 12/14 là mốc sai người đó nêu ĐÃ bị chạm thật, bot đổi theo luật sổ tay — người đó KHÔNG đổi ("hồi để short"). Chỉ 2/14 dính lỗi đề cũ |
| Bot PHÂN VÂN khi người có hướng | 10 | Bot PHÂN VÂN 14 lần, người đó chỉ 7 |
| Người TĂNG → bot GIẢM | 4 | |
- Đích / mốc sai khi cùng hướng: lệch trung vị 0,83% / 0,35% → **số giá bot đặt khá sát người đó**; sai chủ yếu ở HƯỚNG.

## 4. Còn lại / chưa làm
- Bài làm v3 làm trên đề cũ (47 hồ sơ sai trạng thái mốc). Kết quả hợp lệ hoàn toàn cần **thi lại trên `thi/ho_so_v2/`** (~10 agent Opus).
- T7–T10 đã tham gia phát triển → muốn kết luận bot v4 phải thi trên **buổi live mới** (từ 02/11), lưu dự báo TRƯỚC khi mở đáp án.
- P1 chưa làm: mốc SOL/dầu lẫn vào BTC (P1-5), gắn ảnh/giờ vào phiếu (P1-6), volume/M5 trong hồ sơ (P1-7), chính sách sổ sai (P1-8),
  live dùng SMA (P1-9), manifest đầy đủ (P1-11 phần còn lại), lệnh giấy chưa chạy (P1-12).
- Transcript tháng 8–10 (`lam_sach`) không có mốc giờ → câu trích chưa trỏ được tới phút video.
