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

## 4. Ghi lại và chấm kết quả

Mỗi lần nhận định, bot lưu 2 file cùng tên (trùng thì thêm `_2`, `_3`):
1. `bot_v5/doi_chieu/<ngày của T>_<MÃ>.md` — giờ yêu cầu, giờ nến cuối dùng, lệnh lấy dữ liệu, **nguyên văn nhận định**.
2. `bot_v5/ke_hoach/<cùng tên>.json` — bản máy chấm được: hướng H4/D1/W1, đích + mốc sai từng khung, hành động, chỗ vào,
   TP, điều kiện đóng lệnh (khung, số cây), đường đi, căn cứ, phần thiếu dữ liệu. `ke_hoach.py luu` **khoá** file này
   (git commit + sha256 luật / sổ tay / code + sha256 hồ sơ tại T) và ghi `bot_v5/ke_hoach/SO_KE_HOACH.tsv`; sửa sau
   khoá sẽ bị phát hiện.

Chấm (chạy tay, cần mạng lần đầu để tải nến sau T vào `bot_v5/cache_cham/`):
```
python3 bot_v5/cham_ke_hoach.py bot_v5/ke_hoach/<tên>.json            # in báo cáo
python3 bot_v5/cham_ke_hoach.py bot_v5/ke_hoach/<tên>.json --ghi      # + lưu bot_v5/ket_qua/<tên>__toi_<giờ dữ liệu cuối>.md
```
Báo cáo tách riêng:
- **Kết quả LỆNH** từng kế hoạch: A. có kích hoạt không (chỉ "giá chạm vùng" khi điều kiện H1/M15 chưa kiểm; TP chạm
  TRƯỚC khi khớp → không tính thắng; chưa khớp / đã huỷ) · B. sau khi vào **TP hay SL / mốc đóng lệnh tới trước** ·
  C. thời gian tới kết quả, đi ngược / đi thuận lớn nhất · E. hạn: trong / trễ hạn (cột riêng, không đổi kết quả).
- **Độ đúng DỰ BÁO** từng khung: đích trước hay mốc sai (nến ĐÓNG) trước; râu chạm mốc sai ghi riêng, không tính;
  D. đường đi đúng hay sai thứ tự chặng. Lệnh thắng vẫn có thể sai đường đi.
- Cùng 1 nến chạm cả TP và SL → xét nến 15m / 5m / 1m; vẫn không tách được → **KHÔNG RÕ THỨ TỰ** (không đoán từ OHLC).
- Hết dữ liệu chưa chạm gì → **CHƯA NGÃ NGŨ** kèm giờ dữ liệu cuối.
- Hỏi lại thời điểm quá khứ (phát hành > 24h sau T) = **hồi cứu**: chấm từ T; trực tiếp: chấm từ giờ phát hành.

Hỏi kết quả **lệnh của bạn** (giờ / giá do bạn nói; thiếu thì bot báo thiếu, không tự điền):
```
python3 bot_v5/cham_ke_hoach.py bot_v5/ke_hoach/<tên>.json --lenh-user LONG --theo <id kế hoạch> --vao-luc "2026-09-21 11:00" --gia-vao 120.2
python3 bot_v5/cham_ke_hoach.py bot_v5/ke_hoach/<tên>.json --lenh-user LONG --theo <id> --vao-ngay 2026-09-21   # không rõ giờ
python3 bot_v5/cham_ke_hoach.py --ma BTC --lenh-user SHORT --vao-luc "…" --tp 70300-70700 --dong-khi "1D tren 72000 1"
```
Lệnh bạn vào ngày 21/9 được xét từ đúng lúc vào đó — không bị đổi thành lệnh chờ của bot. Chỉ biết ngày → xét mọi giờ
trong ngày, giờ nào nến lúc vào đã chạm TP/SL thì báo "PHỤ THUỘC GIÁ VÀO".

Ghi chú tay (bot sai ở đâu, phân loại lỗi: dữ liệu / bắt chước / dự báo / thực thi) → ghi vào cuối file trong
`bot_v5/ket_qua/`, không sửa file nhận định / kế hoạch. Bot **không đọc** `ket_qua/`, `cache_cham/`, file đối chiếu cũ.
View hôm trước bot chỉ lấy qua `ke_hoach.py truoc` (file phát hành trước T); hỏi thời điểm quá khứ → luôn "KHỞI TẠO VIEW".

Kiểm bộ chấm (offline, ~2 giây): `python3 bot_v5/kiem_tra_cham.py`.
