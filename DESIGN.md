# Bot nhận định BTC bắt chước 1 trader (hình mẫu)

> Giai đoạn: brainstorming xong 29/10/2026. **Hiện trạng 31/10/2026:** đã có 180 transcript + 180 phiếu nhận định +
> 180 file mốc (`moc/`, 3.368 mốc), 232 ảnh khung chart trích từ video (`so_tay/khung/`), sổ tay tinh hoa, bộ thi v3
> (`thi/`, đang phản biện), bot v4 luật máy đang làm (`bot_v4/`). Các yêu cầu user đã chốt bên dưới giữ nguyên.
> Mọi bổ sung của user ghi tiếp vào đây.

## Mục tiêu
Tái tạo **tư duy + thói quen** nhận định BTC của 1 người (livestream, giả định kênh FAM Trading 00:30).
Người đó là **hình mẫu ban đầu** — bot học tư duy + thói quen của họ, đồng thời học từ kết quả
thực tế để sửa sai, kể cả khi bot và người đó cùng sai (user chốt 29/10).
Bot đưa ra nhận định **khi user yêu cầu**, đối chiếu **theo từng ngày**.
Đầu vào học phải có **lời nói + hình chart đồng bộ trong video**, đủ ngữ cảnh để hiểu người đó
đang chỉ vào đâu và lập luận dựa trên hình nào (user chốt 29/10).

**Hai kết quả đánh giá riêng (làm rõ 01/11/2026 — README, DESIGN, NHAP_VAI từng lệch nhau giữa "bắt chước thuần" và
"học sửa sai theo thị trường"):**
- **Độ giống người hình mẫu** (cùng thời điểm T, bot nói giống người đó không) và **độ đúng thị trường** (lệnh TP hay SL
  trước, đích hay mốc sai trước) là hai điểm chấm riêng, báo riêng. Không tuyên bố "giống hơn" = "kiếm tiền tốt hơn".
- Bản mô phỏng (bot v5) tiếp tục làm đúng phương pháp người hình mẫu ("mô phỏng thuần", user chốt: "đừng tự thêm ý của
  bạn"). Sổ sai ghi cả lỗi cùng sai với người đó.
- "Học từ kết quả để sửa sai" (29/10) = đề xuất **cố ý khác hình mẫu** → ghi rõ là khác, có phiên bản riêng, kiểm riêng
  trên phiên mới sau khi sửa rồi mới áp dụng; không âm thầm đưa vào bản mô phỏng, không sửa chỉ để thắng lại ca đã biết.

## Đầu ra: DỨT KHOÁT, không nước đôi (user chốt 29/10)
- Ra **sau khi nến H4 đóng** (H4 = khung người đó nhắc nhiều nhất: 28 lần / 3 buổi mẫu, D1 16, H1 11).
- Nói thẳng "nến như này → sẽ chạy như này". 1 trong 3:
  - **TĂNG** / **GIẢM**: kèm đích giá + hạn + lệnh (vào / TP / SL) + lý do theo giọng người đó.
  - **PHÂN VÂN**: khó quá thì nói thẳng là không rõ + vì sao, không ra lệnh. Được phép — không bắt
    buộc lúc nào cũng có nhận định.
- CẤM nước đôi: "nếu thủng X thì… còn giữ thì…" (đưa 2 kịch bản để kiểu gì cũng đúng).
- GIỮ VIEW (user 31/10): mặc định giữ view buổi trước; chỉ đổi khi có tác động (nến đóng qua mốc sai, chạm đích, tin/biến động
  lớn, đầu tuần/đầu tháng view lại khung lớn). PHÂN VÂN chỉ khi giá lấp lửng ở mốc quyết định, phải chờ nến xác nhận.
  Phải chỉ ra PHÁ VỠ GIẢ (break trap / fake out) khi thấy.
- CHẤM (user 31/10): KHÔNG chấm theo 24h. ĐÚNG = chạm đích (râu cũng tính) trong hạn (vài ngày–2 tuần) TRƯỚC khi chạm SL /
  nến đóng qua mốc sai; SAI chỉ khi chạm SL/mốc sai trước. `cong_cu/cham_dich.py` (giữ nguyên cho bài thi đã khoá).
- CHẤM LỆNH (user 01/11, thay chữ "trong hạn" ở dòng trên cho bot v5): hỏi kết quả một lệnh thì điều quyết định là SAU KHI
  VÀO, TP hay SL / mốc đóng lệnh xảy ra trước. Hạn vẫn lưu nhưng là cột riêng (đúng / trễ hạn), không che hay thay kết
  quả TP/SL. User nói vào ngày 21/9 → xét từ lúc vào đó, không đổi thành lệnh chờ ngày khác. Thiếu giá vào / chiều / giờ
  → ghi thiếu, giới hạn kết luận, không tự điền. SL theo giá chạm ≠ mốc đóng theo NẾN ĐÓNG (đúng khung, đúng số cây).
  Kết quả lệnh ≠ độ đúng dự báo: lệnh thắng vẫn có thể sai đường đi / sai cách vào. TP chạm trước khi khớp không tính
  thắng; chưa khớp / đã huỷ / chưa ngã ngũ báo đúng tên; cùng nến chạm TP và SL → dữ liệu nhỏ hơn, vẫn không rõ → "không
  rõ thứ tự" (không suy từ OHLC). `bot_v5/cham_ke_hoach.py`.
- VIEW BUỔI TRƯỚC (01/11): = kế hoạch bot đã PHÁT HÀNH trước T (`bot_v5/ke_hoach.py truoc`). Không có → "KHỞI TẠO VIEW",
  không suy từ giá T−24h rồi nói như đã biết view hôm qua. Mô phỏng quá khứ không lấy nhận định phát hành sau T làm lịch sử.
- BẮT BUỘC thêm (user chốt 30/10): **(1) Râu nến** — râu trên/dưới gần nhất (giá, nến nào), có test lại không và vì sao;
  **(2) Vùng ổn** để vào lệnh (short và/hoặc long) — khoảng giá + LÝ DO vì sao ổn = các căn cứ hội tụ (râu, EMA Sonic R,
  đỉnh/đáy cũ đổi vai, mốc người đó đã nêu, cụm thanh lý/chỗ đám đông đặt SL). Giá đang ở giữa 2 vùng ổn thì nói rõ "không vào giữa".
- Người đó hay nói 2 kịch bản → nhãn học = **kịch bản chính** của họ (cái họ đặt lệnh theo / nghiêng
  về). ~~họ đứng ngoài → nhãn PHÂN VÂN~~ — thay bởi định nghĩa user chốt 31/10 (dòng "GIỮ VIEW" ở trên): đứng ngoài
  chờ entry vẫn ghi hướng nghiêng; PHÂN VÂN chỉ khi lấp lửng ở mốc quyết định, chờ nến xác nhận.
- Kèm ảnh chart minh họa nhận định, đánh dấu vùng giá / cấu trúc / điểm vào, TP, SL liên quan.
  Ghi rõ cặp giao dịch, khung thời gian, thời điểm dữ liệu; phân biệt ảnh nguồn với chú thích của bot.

## Ngữ cảnh hình ảnh (user chốt 29/10)
- Lấy khung hình trực tiếp từ video, ghép với đoạn lời nói bằng timestamp trong VTT/SRT;
  không chỉ dùng bản TXT đã bỏ thời gian hoặc ảnh thumbnail của video.
- Lấy ảnh lúc đổi chart/khung thời gian, thêm đường vẽ hoặc giải thích vùng giá, mô hình,
  Fibo, chỉ báo và lệnh. Khi câu nói như "vùng này", "đỉnh này" chưa rõ, xem thêm khung hình
  trước/sau cùng đoạn nói liên quan; giữ trình tự thao tác để hiểu ngữ cảnh.
- Mỗi phiếu nhận định giữ video ID, khoảng thời gian lời nói, đường dẫn ảnh và timestamp ảnh;
  trích xuất cặp giao dịch, khung nến, vùng giá, đường vẽ và quan hệ với lời giải thích.
- Ảnh mờ hoặc thông tin bị che thì ghi chưa đọc được và lấy thêm ảnh; không tự điền số giá.
- Khi bot tự nhận định, dùng chart tại thời điểm nhận định để minh họa; không dùng ảnh có nến
  tương lai hoặc ảnh do AI tưởng tượng làm bằng chứng thị trường.

## Sổ sai (user chốt 29/10)
Sai thì **ghi lại để sửa**, không dùng nước đôi để né sai.
- Mỗi dòng: thời điểm · nến · bot nói · người đó nói · giá thật · sai ở đâu (hướng / đích / hạn) ·
  nguyên nhân · đã sửa gì.
- **Lệch người đó** → kiểm tra bot hiểu/trích xuất sai hay có nhận định khác; đối chiếu kết quả
  thực tế để xác định lỗi cần sửa, không mặc định người đó luôn đúng.
- **Cả hai cùng sai giá** → vẫn phải học để sửa bot (sổ tay / dạy lại bộ não số), không chỉ ghi lại.
- Mỗi lần sửa phải có bằng chứng từ kết quả đã xảy ra và kiểm tra trên dữ liệu mới theo thời gian;
  không dùng kết quả tương lai làm đầu vào cho nhận định quá khứ.

## Quy ước giờ (P1-11, thêm 31/10)
Mọi nhận định / phiếu / bài làm / snapshot phải ghi **3 trường giờ riêng**, giờ VN (UTC+7) dạng `YYYY-MM-DD HH:MM`,
không dùng một trường cho cả ba:
- `gio_live` — giờ người đó nói (bắt đầu live thật từ `transcripts/gio_live.tsv` + mốc trong video), hoặc giờ user yêu cầu bot.
- `gio_cat` — giờ đóng của **nến đã đóng cuối cùng** được dùng làm dữ liệu (cutoff). Mọi dữ liệu (nến, chỉ báo, tin, dữ liệu
  phụ) phải có thời điểm công bố ≤ `gio_cat`.
- `gio_phat_hanh` — giờ nhận định được lưu/công bố. Luôn `gio_phat_hanh` ≥ `gio_cat`; chấm đúng/sai tính từ `gio_phat_hanh`.
Thiếu giờ thật thì ghi rõ nguồn giờ (tên file / mặc định 10:00) và cờ "giờ không chắc", không tự điền.

## Thước đo thành công
Theo dõi **độ giống người đó** để đánh giá việc học hình mẫu, đồng thời đo **độ đúng với thị trường
và khả năng giảm lỗi sau khi sửa**. Bắt chước đúng nhưng cùng sai vẫn là lỗi cần học để sửa.

| Thành phần | Chấm giống khi |
|---|---|
| Hướng | trùng TĂNG / GIẢM / PHÂN VÂN |
| Vùng giá chính (hỗ trợ/kháng cự) | lệch ≤ ngưỡng % (chốt sau khi xem dữ liệu) |
| Đích giá + hạn | đích lệch ≤ ngưỡng %, cùng hạn |
| Lệnh dự kiến | cùng chiều; giá vào/TP/SL lệch ≤ ngưỡng % |
| Lý do | cùng công cụ (Fibo, cấu trúc, tin…) |

Ghi giá thật sau 1 ngày / 3 ngày / 1 tuần và tại hạn dự báo để đánh giá hướng, đích, hạn,
và kết quả lệnh nếu có; dùng kết quả này cho vòng học sửa sai.

## Hướng: kết hợp
1. **Bộ não số** — học từ vài trăm phiếu nhận định cũ: đầu vào là thứ người đó hay nhìn (cấu trúc
   đỉnh/đáy, Fibo, vùng cản, volume, lịch tin) + **quan điểm gần nhất của người đó** (họ giữ view
   xuyên buổi: "view từ đêm qua không thay đổi nhiều"); đầu ra là 1 hướng + đích + hạn + lệnh.
2. **Tư duy & giọng** — Claude + "sổ tay thói quen" rút từ video diễn giải số của phần 1 theo cách
   người đó lập luận (cách vào lệnh, chốt ở cản, thái độ trước tin, cách đổi ý, câu cửa miệng).
3. **Đọc hình cùng lời nói** — phân tích chart và chú thích trên các khung hình đồng bộ, đưa
   bằng chứng hình ảnh vào phiếu nhận định và sổ tay; không suy luận chỉ từ transcript.

## Luồng
1. Video → chữ có timestamp + khung hình chart đồng bộ (`~/bin/yt2text` cho VOD,
   `~/bin/ytlive2text` cho live; Whisper luôn `--vad`; bổ sung bước trích ảnh từ video)
2. Chữ + ảnh → phiếu nhận định có cấu trúc (ngày giờ, giá lúc nói, thiên hướng, vùng,
   kịch bản, lệnh, lý do, tham chiếu đoạn nói và ảnh nguồn)
3. Phiếu → sổ tay thói quen + huấn luyện bộ não số
4. Sau nến đóng / khi user yêu cầu → bot ra 1 nhận định dứt khoát + ảnh chart có chú thích
5. Hằng ngày: bot ra nhận định trước live → live xong lấy phiếu thật → bảng so độ giống
6. Đối chiếu giá thực tế → ghi **sổ sai** → học và sửa bot, kể cả khi cùng sai với người đó
7. Kiểm tra bản sửa trên dữ liệu mới theo thời gian trước khi áp dụng

## Kiểm tra
- Chia theo thời gian: học trên video cũ, thi trên video mới bot chưa thấy.
- Kiểm tra ảnh có khớp đoạn nói, đúng cặp/khung nến, đọc đúng vùng giá và đường vẽ;
  chỉ dùng lời nói, ảnh và dữ liệu đã có tại thời điểm nhận định.
- Claude biết giá BTC tới ~06/2026 → phần 2 chỉ thi sạch trên video sau 06/2026 hoặc chạy tiếp từ nay.
- Hồi cứu hiện tại **không phải ngoài mẫu sạch** dù sổ tay đã bỏ ví dụ ≥ T: sổ tay vẫn giữ số tần suất / [đo] tổng hợp
  cả năm (có phần sau T); trendline chọn biến thể trên cả 180 buổi và đường chính chỉ khớp 13/33 (`hoc_v5/trendline/CHON.md`).
  Kết luận về độ đúng chỉ từ nhận định MỚI, khoá trước khi có diễn biến (01/11).
- Mỗi nhận định v5 khoá phiên bản: git commit, sha256 luật / sổ tay / code, sha256 hồ sơ tại T (`ke_hoach.py luu`). Ghi
  đủ ca sai, chưa khớp, chưa ngã ngũ. Phân loại lỗi: dữ liệu / rút nhãn · bắt chước · dự báo · thực thi. Mỗi bản sửa có lý
  do + bằng chứng, kiểm trên phiên mới sau khi sửa. So với mốc đơn giản cùng tập: hoãn tới khi có ≥ 20–30 nhận định mới.

## Không làm (giai đoạn đầu)
Tự vào lệnh · nhiều người hình mẫu.

## Rủi ro
- Ảnh chart có thể mờ, chuyển nhanh hoặc thiếu phần người đó nhìn; cần kiểm tra lời nói và
  ảnh cùng nhau, ghi rõ phần thiếu ngữ cảnh.
- Vài trăm mẫu là ít cho học máy.
- Người đó hay nói nước đôi → phải rút đúng kịch bản chính; rút sai thì bot học sai.
- Chi phí trích xuất: mỗi buổi ~10k chữ → làm thử 30 video trước.

## Dữ liệu
- Nguồn: https://www.youtube.com/@famtrading/streams (~179 buổi live; nhiều buổi/ngày, giờ không cố định)
- Lấy bằng `python3 cong_cu/lay_transcript.py`: lùi từ mới nhất về 16/09/2026, giãn 60 giây/lần gọi
  YouTube, ưu tiên phụ đề → `transcripts/phu_de/`, không có phụ đề → Whisper → `transcripts/whisper/`.
  File `NGAY_GIO(VN)_ID.txt/.vtt`; mục lục `transcripts/danh_sach.tsv`. Chạy lại được (bỏ qua buổi đã có).
- Transcript cũ 16–17/09 (trước khi có script) cất ở `transcripts/_cu/`
- Ảnh (cập nhật 31/10): đã trích 232 khung hình chart từ video vào `so_tay/khung/` (tên `<videoID>_<hhmmss>.jpg`, phủ
  57/180 buổi). Còn thiếu: gắn ảnh + timestamp đoạn nói vào từng phiếu/mốc/nhận định bot (P1-6); yêu cầu "lưu khung hình
  kèm mục lục timestamp liên kết với transcript; giữ VTT/SRT làm mốc đồng bộ" vẫn giữ nguyên.
- Giá BTC: TimescaleDB cổng 5433 (dùng chung với okx_bot / trendline_bot)
