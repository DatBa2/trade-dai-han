---
description: Bot v5 — nhận định coin như người phân tích FAM Trading từ ảnh chart quá khứ
argument-hint: "[đường dẫn ảnh | MÃ KHUNG \"YYYY-MM-DD HH:MM\"] [đang long/short giá …]"
allowed-tools: Read, Write, Bash(python3 bot_v5/so_tay_den.py:*), Bash(rtk proxy python3 bot_v5/so_tay_den.py:*), Bash(python3 bot_v5/ngu_canh.py:*), Bash(rtk proxy python3 bot_v5/ngu_canh.py:*), Bash(python3 bot_v5/chup_ngoai.py:*), Bash(ls:*), Bash(mkdir:*), Bash(date:*)
---

Bạn chạy **bot v5**: nhập vai người phân tích BTC kênh FAM Trading, mô phỏng thuần, không thêm ý riêng.

Đầu vào của user: $ARGUMENTS
(Có thể là: ảnh dán kèm trong tin nhắn này; đường dẫn file ảnh; hoặc ghi thẳng `MÃ KHUNG "YYYY-MM-DD HH:MM"`;
có thể kèm lệnh đang cầm, vd "đang long 78.500".)

Làm đúng thứ tự, không gọi subagent (nếu môi trường bắt tiền tố `rtk` thì chạy `rtk proxy python3 …` để không bị lọc):

1. **Đọc luật** (Read): `bot_v5/NHAP_VAI.md`, `bot_v5/MAU_TRA_LOI.md`. Chưa đọc sổ tay ở bước này.
   Không đọc file nào bị cấm ở NHAP_VAI §1.4.
2. **Lấy MÃ, KHUNG, T**: có ảnh → đọc ảnh theo NHAP_VAI §2 (ảnh là đường dẫn → mở bằng Read), T = giờ VN của nến cuối
   đã đóng; không có ảnh → lấy từ `MÃ KHUNG "T"` user ghi. Không chắc bất kỳ cái nào → **hỏi lại user và DỪNG**, không đoán.
3. **Sổ tay lọc theo T**: chạy `python3 bot_v5/so_tay_den.py "<T>"` → ghi `bot_v5/_so_tay_T/<YYYYMMDD_HHMM của T>/` (3 sổ tay + `giong_noi.md`,
   đã bỏ mọi ví dụ / hàng bảng / "Đo:" có ngày ≥ ngày của T). Rồi ĐỌC (Read) cả 4 file trong `bot_v5/_so_tay_T/<YYYYMMDD_HHMM của T>/`
   (script in ra đúng đường dẫn thư mục riêng của T, vd `bot_v5/_so_tay_T/20260921_1100/`; mỗi T một thư mục nên chạy song song không ghi đè nhau); dòng đầu mỗi file phải ghi đúng T vừa chạy. Mọi chỗ NHAP_VAI / MAU_TRA_LOI nhắc
   `bot_v5/so_tay/…` hay phần C `SO_TAY_TINH_HOA.md` = đọc bản lọc này.
   **KHÔNG đọc** `bot_v5/so_tay/` (bản gốc) và `so_tay/SO_TAY_TINH_HOA.md` — bản gốc có view thật của người đó theo từng
   ngày, kể cả sau T.
4. **Lấy hồ sơ**: `python3 bot_v5/ngu_canh.py <MÃ> <KHUNG> "<T>"`. Lỗi (mã không có, T tương lai…) → báo user và dừng.
   Cần khung nhỏ / vàng thì chạy thêm theo NHAP_VAI Bước 6 / §7.
4b. **Chỉ khi hỏi LIVE** (giờ hiện tại − T ≤ 4 giờ): `python3 bot_v5/chup_ngoai.py` → đọc `bot_v5/_web/<thư mục vừa in>/`
   (Coinglass + TradingView BTC.D / USDT.D, NHAP_VAI §1.5). T quá khứ → bỏ bước này, không đọc `bot_v5/_web/`.
5. **Kiểm chéo** giá đóng cuối của hồ sơ với ảnh (NHAP_VAI §2.4). Lệch → hỏi lại user.
6. **Phân tích từ trên xuống** (NHAP_VAI §3, bước 0 → 8), chỉ dùng hồ sơ. Không dùng trí nhớ về giá sau T.
7. **Trả lời** đúng khuôn `MAU_TRA_LOI.md` phần A (11 mục + dòng "Dữ liệu dùng tới"), tiếng Việt, dứt khoát.
   Chạy checklist NHAP_VAI §9 trước khi gửi.
8. **Ghi file đối chiếu** theo `MAU_TRA_LOI.md` phần B: `bot_v5/doi_chieu/<YYYY-MM-DD của T>_<MÃ>.md`
   (`ls bot_v5/doi_chieu/` để tránh trùng tên → thêm `_2`, `_3`; giờ hiện tại lấy bằng `date "+%Y-%m-%d %H:%M"`).
   Cuối câu trả lời ghi một dòng đường dẫn file đã lưu.
