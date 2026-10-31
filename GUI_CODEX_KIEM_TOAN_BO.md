# Nhờ Codex kiểm độc lập TOÀN BỘ việc Claude làm ngày 31/10 (sau báo cáo `kiem_cheo/TONG_QUAN_VA_THIEU_SOT_2026-10-31.md`)

User nghi Claude có thể "viết code để qua mặt". Hãy kiểm như người ngoài: chạy lại, tự tính lại, tìm chỗ gian/rò rỉ.
CHỈ ĐỌC + CHẠY; chỉ ghi kết luận vào `kiem_cheo/CODEX_KIEM_TOAN_BO.md` (và `kiem_cheo/CODEX_KIEM_V4.md` theo phần 3).
Mỗi phát hiện: mức (P0 gian/rò thật · P1 có thể sai · P2 vệ sinh) + file:dòng + bằng chứng + cách tái hiện.

## 1. Sửa P0 bộ thi (đọc `thi/BAO_CAO_XU_LY_P0.md`, `thi/SUA_P0.md`)
- Snapshot lượt thi cũ: `thi/_snapshot_v3_chan_doan/` — kiểm `MANIFEST.sha256` (`shasum -a 256 -c` trong thư mục đó).
- Đáp án v2: luật chốt trước `thi/dap_an_v2/QUY_TAC_PHAN_XU.md`; nhãn mù `thi/dap_an_v2/nhan/`; khoá `thi/dap_an_v2/KHOA_DAP_AN.md`.
  Kiểm: luật phân xử có thật sự được áp đúng không (`thi/dap_an_v2/dung_dap_an.py`); đọc 5 buổi bất đồng trong `PHAN_XU.md`
  với transcript + link giờ trong `bang_chung/<buổi>.json` — nhãn v2 có đúng lời người đó không.
- Bộ chấm: `python3 thi/kiem_thu_cham.py` (8 ca); hồi quy `python3 thi/hoi_quy_cham_dich.py`; chấm lại
  `python3 thi/cham.py --phieu thi/dap_an_v2/phieu --ra /tmp/x.md` phải ra đúng số trong `thi/KET_QUA_THI.md`.
- Khoá: `thi/KHOA_CHAM.md` (v1 → v2 → v2.1 → v2.2). **Sự cố tự khai ở mục v2.2**: Claude lỡ ghi đè `thi/ho_so_v2/` rồi dựng lại
  từ moc snapshot — kiểm việc khôi phục có đúng (so `thi/ho_so/` vs `thi/ho_so_v2/`: 19 dòng "ĐÃ KÍCH HOẠT → chưa kích hoạt").

## 2. Sửa P1/P2
`kiem_cheo/VE_SINH_MOC.md` (mốc SOL/dầu, đảo cận, giờ live thật trong `kiem_can_cu.py`, lệnh giấy), `cong_cu/anh_thi_truong.py` (SMA→EMA,
kiểm EMA200 H4 29/10 19h ≈ 81.635), `bang_chung/TONG_HOP.md` (giờ video cho câu trích — mở 10 mẫu ngẫu nhiên, câu có đúng ở giờ đó?),
`thi/tao_ho_so.py --ban 3` (volume, EMA tháng, bỏ mốc không phải BTC), `doi_chieu/SO_DOI_CHIEU.md`, `DESIGN.md`, `AGENTS.md`.

## 3. Bot v4 — làm theo `bot_v4/GUI_CODEX.md` (quan trọng nhất)
- Thiết kế khoá TRƯỚC code: `bot_v4/THIET_KE.md` (sha256 `cdfc577d…` trong `bot_v4/KHOA.md`, giờ khoá 10:56). Kiểm mtime/ nội dung các file
  code có sau giờ đó, và `bot_v4/NHAT_KY_SUA.md` (0 lần sửa sau lần chạy thật đầu tiên) có đúng không.
- **Lệch thiết kế tự khai:** giả dược mục 8 (kiểu A) bị lệch khi hiệu chỉnh trên dữ liệu ngẫu nhiên (phân vị ~7–9 thay vì 50) → agent báo cáo
  thêm kiểu B (limit cùng khoảng cách, đo R TB) — xem `bot_v4/KET_QUA.md` mục 4b. Kiểm lập luận hiệu chỉnh này có đúng không.
- **Thi lại hộ:** tự viết backtest độc lập BTC 2025 CHỈ từ `THIET_KE.md` (+ `DIEN_GIAI.md` cho chỗ mơ hồ) trước khi đọc `dong_co.py`,
  so danh sách lệnh với `bot_v4/ket_qua/2025_BTC/lenh.csv`; tự cộng lại lãi/lỗ 6 bộ kết quả từ `lenh.csv`.
- Kết quả Claude báo (để đối chiếu): mọi năm đều LỖ — 6 tài sản 2024 −62,6% · 2025 −69,4% · 2026 −58%; BTC −16,1% / −21% / −18,8%;
  không hơn giả dược; độ giống hướng 61% (= luật từ trên xuống, hơn "luôn GIẢM" 47%).
