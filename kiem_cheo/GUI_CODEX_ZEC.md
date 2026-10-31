# Nhờ Codex nhận định ĐỘC LẬP: ZEC 4H tại 2026-10-31 11:00 VN (song song với bot v5 của Claude)

Mục đích: có một nhận định thứ hai làm căn cứ đối chiếu. Bạn làm ĐỘC LẬP — KHÔNG đọc `bot_v5/doi_chieu/` (câu trả lời của bot
Claude), không đọc `bot_v5/_so_tay_T/` (thư mục bot đang dùng). Chỉ ghi vào `kiem_cheo/` (file kết quả + thư mục sổ tay lọc riêng).

## Phương pháp (giống bot): nhập vai người phân tích BTC kênh FAM Trading, MÔ PHỎNG THUẦN
1. Đọc `bot_v5/NHAP_VAI.md` (luật, quy trình từ trên xuống, định nghĩa TĂNG/GIẢM/PHÂN VÂN, giữ/lật view, mốc sai, vùng hẹp, vào/tránh,
   giữ/đóng, tin & Fed) và `bot_v5/MAU_TRA_LOI.md` (khuôn 11 mục). Tuân thủ danh sách CẤM ĐỌC ở NHAP_VAI §1 (không đọc `bot_v5/so_tay/`
   gốc, `so_tay/SO_TAY_TINH_HOA.md`, transcript, phiếu, …). Không dùng trí nhớ về giá sau T.
2. Sổ tay lọc theo T vào thư mục RIÊNG của bạn:
   `python3 bot_v5/so_tay_den.py "2026-10-31 11:00" --ra kiem_cheo/codex_so_tay_T` → đọc cả 4 file trong `kiem_cheo/codex_so_tay_T/`.
3. Hồ sơ ngữ cảnh (dữ liệu ≤ T): `python3 bot_v5/ngu_canh.py ZEC 4H "2026-10-31 11:00"` (có thể thêm `ZEC 1H … --so-nen 12`).
   Mọi con số phải lấy từ hồ sơ.
4. Phân tích từ trên xuống (chu kỳ → tháng → tuần → ngày → H4 → khung nhỏ; nhìn BTC trước — mục "BTC tại T" của hồ sơ).

## Ghi `kiem_cheo/CODEX_ZEC_2026-10-31.md`
- Dòng đầu: **Trả lời câu hỏi của user: "ZEC còn có thể về 1040 nữa không?"** — dứt khoát CÓ/KHÔNG (trong hạn nào), theo cách người đó:
  1040 nằm phía nào so với giá, có căn cứ nào ở 1040 trong hồ sơ, là nấc thứ mấy, cần nến nào ĐÓNG qua đâu để mở đường, khi nào coi như
  không về. Nếu 1040 không khớp bậc giá của ZEC thì nói rõ.
- Mục **"ZEC đang rơi vào case nào"**: mỗi dòng = mã case trong sổ tay đã lọc ([ST1 …]/[ST2 …]/[ST3 …]) · tên case · vì sao khớp (số trong
  hồ sơ) · người đó làm gì → áp vào ZEC ra hành động gì. Case gần khớp mà thiếu điều kiện thì ghi "chưa khớp vì …".
- Rồi đủ 11 mục theo khuôn `MAU_TRA_LOI.md` phần A (kết luận H4/D1/W1, đường đi, đích + mốc sai theo nến đóng, chỗ VÀO, chỗ TRÁNH,
  GIỮ/ĐÓNG cho cả long và short, râu, trendline, tin & Fed, lời bình, dòng "Dữ liệu dùng tới").
- Cuối file: 3 dòng "chỗ mình không chắc / luật mơ hồ".
