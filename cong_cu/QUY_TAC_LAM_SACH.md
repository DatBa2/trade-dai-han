# Quy tắc làm sạch transcript

Bản sạch dùng để học **tư duy + thói quen + giọng nói** của người phân tích BTC (kênh FAM Trading).
Đây là **LÀM SẠCH, KHÔNG PHẢI TÓM TẮT**. Bỏ thì bỏ hẳn câu thừa, còn câu nào giữ thì giữ đủ ý và giữ lời của người nói.

## GIỮ (đầy đủ, theo đúng thứ tự trong buổi)
- Mọi nội dung thị trường: giá, mốc, vùng hỗ trợ/kháng cự, khung (H1, H4, D1…), chỉ báo (Fibo, EMA, RSI, volume…),
  cấu trúc đỉnh/đáy, mẫu nến, thanh khoản, funding, ETF, dòng tiền, USDT.D, BTC.D, altcoin, tin vĩ mô (Fed, CPI…).
- Lập luận **vì sao** (cái này quan trọng nhất).
- Kịch bản, nhận định, dự đoán, kể cả khi nói nước đôi — ghi đúng như người đó nói, không tự chọn hộ.
- Lệnh: vào/limit, TP, SL, dời SL, chốt, giữ lệnh, lệnh đã khớp từ buổi trước, lời/lỗ.
- Quản lý vốn, đòn bẩy, tâm lý, kỷ luật, lời khuyên cho người xem.
- Câu hỏi người xem về thị trường/lệnh **mà người đó trả lời** → ghi `> Hỏi: …` rồi câu trả lời.
- Giọng nói đặc trưng: "anh em", "nhá", "đấy", câu cửa miệng, cách nhấn mạnh. KHÔNG viết lại thành văn trang trọng.

## BỎ
- Chào hỏi, đọc tên người xem, cảm ơn, xin like/subscribe, chờ người vào, kiểm tra tiếng/hình.
- Chuyện ngoài lề không dính thị trường (bóng đá, đời tư…), quảng cáo.
- Câu hỏi người xem mà người đó không trả lời.
- Từ đệm vô nghĩa đứng riêng ("Ok.", "Rồi.", "Xem nào.") và chữ lặp do phụ đề/nói vấp.
- Câu đứt dở không còn ý.

## SỬA
- Lỗi nhận dạng giọng nói, nhất là thuật ngữ: "tráp" → trap, "Oncoin" → altcoin, "phi bô" → Fibo, "rou/râ" → râu…
- Chính tả, dấu câu; chia đoạn theo chủ đề.
- **Số giá: giữ nguyên như người đó nói** ("76", "76 nghìn", "76K" để nguyên). Chỉ sửa khi chắc chắn là nghe nhầm.
  Không chắc → giữ chữ gốc và thêm `[?]` ngay sau.
- **BẪY SỐ KIỂU NÓI VIỆT** — phụ đề hay viết chữ số lẻ sau "nghìn" thành chữ: "80.000 năm" / "80 nghìn năm" /
  "80.00 năm" = **80.500** (tám mươi nghìn năm trăm), KHÔNG phải 80.000. Tương tự "nghìn hai" = .200, "nghìn ba" = .300,
  "nghìn tư/bốn" = .400, "nghìn sáu" = .600, "nghìn bảy" = .700, "nghìn tám" = .800, "nghìn chín" = .900.
  Ghi dạng đủ (80.500). Nếu chữ sau có thể là nghĩa khác (vd "năm" = năm/year) → giữ gốc + `[?]`.
  Phụ đề còn viết "80 nghìn 8" thành **"80.008" = 80.800** ("78.001" = 78.100, "80.005" = 80.500) khi giá BTC quanh 80K.
  TUYỆT ĐỐI không bỏ phần lẻ (đổi "80.000 năm" thành "80.000" là SAI giá).
- TUYỆT ĐỐI không thêm ý, không diễn giải, không bịa số, không thêm nhận xét của mình.

## Định dạng file ra (`transcripts/lam_sach/<cùng tên>.md`)
```
# <YYYY-MM-DD HH:MM> — <tiêu đề buổi trong danh_sach.tsv>
Nguồn: <id> · phụ đề | whisper · gốc <N> từ → sạch <M> từ

## <Chủ đề đoạn, ngắn — vd "Nhìn lại lệnh hôm qua", "Khung D1", "Tin Fed", "Kịch bản hôm nay", "Altcoin">
<đoạn văn>

## …
```
Thường bản sạch còn khoảng 40–80% số từ bản gốc (buổi dày nội dung có thể ~80%). Ít hơn 30% là đã cắt quá tay — kiểm lại.
