# CÁCH DÙNG BOT V5

Bot v5 = Claude **nhập vai** người phân tích BTC kênh FAM Trading. Bạn gửi ảnh chart một coin ở thời điểm quá khứ →
bot đọc mã / khung / giờ nến cuối → lấy dữ liệu tới đúng giờ đó → nhận định như người đó → bạn tự đối chiếu với chart thật.

## 1. Gửi ảnh thế nào

Ảnh nên thấy rõ 3 thứ:
- **Tên coin** (góc trên trái TradingView, vd `BTCUSDT`, `ETHUSDT.P`).
- **Khung nến** (vd `4h`, `1D`, `1W`). Hợp lệ: 15m, 1H, 4H, 1D, 1W.
- **Trục thời gian** ở đáy chart, và **nến cuối cùng** nằm ở mép phải. Bot coi nến cuối là nến đang chạy → dùng dữ liệu
  tới lúc nó mở.

Mẹo:
- TradingView để múi giờ **UTC+7** (góc dưới phải). Để UTC thì ghi kèm "giờ UTC".
- Muốn chắc thì ghi luôn giờ: `nến cuối mở 14/08 11:00`.
- Nét vẽ sẵn trên ảnh (trendline, Fibo, hộp) được coi là **gợi ý của bạn**; bot vẫn kiểm theo luật của người đó.
- Ảnh mờ, thiếu tên coin hoặc thiếu trục thời gian → bot sẽ **hỏi lại**, không đoán.

## 2. Câu lệnh

Trong Claude Code, mở ở thư mục `trade_dai_han`:

| Cách | Gõ |
|---|---|
| Dán ảnh vào ô chat (Ctrl+V / kéo thả), rồi gõ | `/nhan-dinh` |
| Đưa đường dẫn ảnh | `/nhan-dinh ~/Desktop/eth_4h.png` |
| Không có ảnh, ghi thẳng | `/nhan-dinh ETH 4H "2026-08-14 11:00"` |
| Kèm lệnh đang có | `/nhan-dinh ~/Desktop/btc.png đang long 78.500` |

Chạy tay phần dữ liệu (không cần Claude):
```
python3 bot_v5/ngu_canh.py BTC 4H "2026-08-14 11:00"
```

## 3. Bot trả lời gì

Khuôn cố định (`bot_v5/MAU_TRA_LOI.md`): Kết luận H4 + D1 + W1 · Đường đi · Đích + khi nào view sai · Chỗ **VÀO** ·
Chỗ **TRÁNH** · Đang có lệnh thì **GIỮ hay ĐÓNG** · Râu nến · Trendline · Tin & Fed · Lời bình · dòng cuối
"Dữ liệu dùng tới: …".

- "View sai khi nến … ĐÓNG …" = chỗ bạn đóng lệnh bằng tay (bạn không dùng SL).
- T trước **01/07/2026** → bot ghi cảnh báo: model có thể nhớ giá thật giai đoạn đó, nên kết quả kiểm tra không sạch.
  Kiểm thử nghiêm túc thì chọn thời điểm **từ 07/2026 trở đi**.

## 4. Ghi lại để đối chiếu

Mỗi lần nhận định, bot tự lưu `bot_v5/doi_chieu/<ngày của T>_<MÃ>.md` (trùng thì thêm `_2`, `_3`). File có:
1. Giờ yêu cầu, giờ nến cuối dùng, lệnh lấy dữ liệu.
2. **Nguyên văn nhận định** + bảng tóm tắt (hướng / đích / hạn / view sai khi).
3. Mục **"Kết quả thật"** để trống — **bạn tự điền** sau khi xem chart thật:
   - **ĐÚNG** = giá chạm đích (râu cũng tính) trong hạn, TRƯỚC khi có nến đóng qua mốc sai.
   - **SAI** = nến đóng qua mốc sai trước.
   - **CHƯA RÕ** = hết hạn mà chưa chạm cả hai.
   - Ghi thêm: chỗ vào có phản ứng không, chỗ tránh có đúng không, râu có test lại không, trendline phá thật/giả đúng không,
     bot sai ở đâu.

Không chấm theo 24 giờ — hạn là vài ngày tới 2 tuần (theo đích bot ghi).
Bot **không đọc** các file đối chiếu cũ khi nhận định (vì có kết quả thật bạn đã ghi).
