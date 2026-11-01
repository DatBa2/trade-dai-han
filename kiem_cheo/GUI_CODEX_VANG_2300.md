# Nhờ Codex nhận định ĐỘC LẬP: VÀNG (XAU, mã `VANG`) 4H tại 2026-10-31 23:00 VN (song song với bot v5 của Claude)

Mục đích: có một nhận định thứ hai làm căn cứ đối chiếu. Bạn làm ĐỘC LẬP — KHÔNG đọc `bot_v5/doi_chieu/` (câu trả lời của bot
Claude), không đọc `bot_v5/_so_tay_T/` (thư mục bot đang dùng), không đọc các file CODEX_BTC_* cũ. Chỉ ghi vào `kiem_cheo/`.

Lưu ý: vàng nghỉ cuối tuần → nến H4 cuối đã đóng là 2026-10-31 07:00 VN (hồ sơ có cảnh báo "nến cuối cách T khá xa" — bình thường).
Dùng T = "2026-10-31 23:00" để lấy ngữ cảnh mới nhất (BTC, Polymarket, lịch tin); số liệu vàng chỉ tới nến đóng 07:00.

## Phương pháp (giống bot): nhập vai người phân tích BTC kênh FAM Trading, MÔ PHỎNG THUẦN
1. Đọc `bot_v5/NHAP_VAI.md` và `bot_v5/MAU_TRA_LOI.md` (khuôn 11 mục). Tuân thủ danh sách CẤM ĐỌC ở NHAP_VAI §1. Không dùng trí nhớ về giá sau T.
2. Sổ tay lọc theo T vào thư mục RIÊNG của bạn:
   `python3 bot_v5/so_tay_den.py "2026-10-31 23:00" --ra kiem_cheo/codex_so_tay_T_vang2300` → đọc cả 4 file trong thư mục đó.
3. Hồ sơ ngữ cảnh (dữ liệu ≤ T): `python3 bot_v5/ngu_canh.py VANG 4H "2026-10-31 23:00" --cache kiem_cheo/codex_cache_vang2300`
   (có thể thêm `VANG 1H … --so-nen 12`). Mọi con số phải lấy từ hồ sơ.
4. Phân tích từ trên xuống (chu kỳ → tháng → tuần → ngày → H4 → khung nhỏ). Người đó gần như chỉ trade BTC và chỉ "liếc vàng"
   → áp cách làm của họ sang vàng theo % (NHAP_VAI §5 "coin khác"), nói rõ chỗ nào là suy cách làm.

## Ghi `kiem_cheo/CODEX_VANG_2026-10-31_2300.md`
- Dòng đầu: tóm tắt 1 câu: hướng H4/D1/W1 + hành động lúc này (VÀO / CHỜ / KHÔNG LỆNH).
- Mục **"Vàng đang rơi vào case nào"**: mỗi dòng = mã case trong sổ tay đã lọc ([ST1 …]/[ST2 …]/[ST3 …]) · tên case · vì sao khớp
  (số trong hồ sơ) · người đó làm gì → áp vào vàng ra hành động gì. Case gần khớp mà thiếu điều kiện thì ghi "chưa khớp vì …".
- Rồi đủ 11 mục theo khuôn `MAU_TRA_LOI.md` phần A + dòng "Dữ liệu dùng tới".
- Thêm 1 mục ngắn: vàng lúc này nói gì cho BTC theo luật của người đó ("Vàng tăng thì đừng cố đi short BTC", "Vàng gãy thì Bitcoin cút").
- Cuối file: 3 dòng "chỗ mình không chắc / luật mơ hồ".
