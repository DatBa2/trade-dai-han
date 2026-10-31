# Kiểm tra tổng quan và phần còn thiếu — 31/10/2026

Kiểm tra bởi Codex cùng 3 agent: dữ liệu/nhãn; bài thi/bộ chấm; sổ tay/ảnh/công cụ. Đọc trạng thái trên đĩa khoảng **10:09–10:16 VN**. Claude đang sinh bài làm v3 đồng thời; số bài làm tăng trong lúc kiểm tra, đạt 58/77 lúc 10:16. Không coi bài làm chưa đủ 77 là lỗi hoàn tất. Chỉ thêm báo cáo này, không sửa mã, đáp án hoặc bài làm đang chạy.

**Kết luận:** Claude đã xây được phần nghiên cứu và hạ tầng đáng kể, nhưng chưa đủ căn cứ công bố v3 vượt bài thi. Các điểm cản chính là đáp án chưa được phân xử, bộ chấm sai thời điểm/điều kiện vô hiệu, và yêu cầu học từ hình ảnh cùng vòng sửa sai chưa đi hết luồng.

## Project thực tế đang làm gì

Mục tiêu gốc trong `DESIGN.md` là bot nhận định BTC học cách phân tích của FAM Trading, giữ view có lý do, ra một hướng cùng đích/hạn/mốc sai, râu nến và vùng vào có căn cứ. Bot phải dùng lời nói cùng chart, đo độ giống người và độ đúng thị trường, rồi sửa lỗi kể cả khi cả hai cùng sai. Chưa có yêu cầu tự đặt lệnh thật.

Hiện trạng đã vượt phần mô tả “chưa code”:

| Thành phần | Trạng thái đã kiểm |
|---|---|
| Kho transcript | 180 video ID duy nhất, 181 tệp sạch; 10/8 có hai bản nguồn |
| Nhãn | 180 phiếu và 180 tệp mốc, tổng 3.368 mốc; không thiếu đối ứng video |
| Nghiên cứu chart | 232 ảnh thuộc 57/180 buổi, có ghi chú đọc chart cùng đoạn lời nói |
| Sổ tay | Có bản toàn kỳ và bản thi T1–T6; hai bản chưa đồng bộ hết quy tắc |
| Bot cơ học | Có v1/v2, báo cáo ngoài mẫu và luồng lệnh giấy riêng |
| Bot v3 | Có bộ dựng đề, 77 hồ sơ, bộ chấm và bài làm đang được Claude sinh |
| Kiểm nhãn độc lập | Có 23 phiếu Codex; chưa thấy kết quả phân xử 6 bất đồng |
| Vận hành hoàn chỉnh | Chưa thấy một luồng đã kiểm chứng xuyên suốt từ dữ liệu → dự báo có chart → đối chiếu → sửa → kiểm bản sửa trên buổi mới |

## Những phần Claude đã xử lý đúng

- `thi/tao_ho_so.py` đã dùng giờ live từ `transcripts/gio_live.tsv`, cắt nến đã đóng, phân biệt nến đang chạy, dùng EMA và RSI, có lịch sử dài và giờ xác nhận fractal. **77/77 buổi thi có giờ live theo bảng nguồn.** Đây không còn là tình trạng mặc định toàn bộ live lúc 10h của bản đánh giá cũ.
- Kiểm offline bằng các hàm của builder, chặn mạng: **77/77 hồ sơ giống hệt sau khi xóa dữ liệu thị trường sau C và loại các buổi chưa kết thúc trước giờ live.** Kết quả này xác nhận phép cắt dữ liệu của builder trong phạm vi kiểm tra; không xác nhận bộ chấm, nhãn, sổ tay hay phiên suy luận đã độc lập.
- Đã có baseline cùng tập, macro-F1, balanced accuracy, kappa, bảng chéo và báo riêng PHÂN VÂN. Có xử lý `CHUA_HET_HAN` trong lớp chấm thi.
- Đã có râu nến, vùng ổn, giữ view và phá vỡ giả trong sổ tay thi/bài làm mới; đã có sổ sai và một số lần sửa. Không đúng nếu nói các phần này hoàn toàn chưa làm.
- Bốn tiền tố hash trong `thi/KHOA_CHAM.md` khớp mã/sổ tay trên đĩa lúc kiểm. Tài liệu cũng đã thừa nhận việc T7–T10 tham gia quá trình phát triển.

## P0 — cần giải quyết trước khi kết luận từ bài thi

### 1. Đáp án còn bất đồng, định nghĩa hướng còn trộn với chặng cuối

**6/23 phiếu** có hướng H4 cuối buổi khác giữa Claude và Codex: 6/3, 19/5, 22/6, 7/8, 5/10, 23/10. Đây là tỷ lệ bất đồng trên mẫu được chọn, không phải tỷ lệ lỗi toàn kho; không mặc định Codex đúng. Hai ca 19/5 và 23/10 khác hẳn TĂNG/GIẢM; một số ca còn lại độ chắc thấp hoặc vừa.

Ví dụ `phieu/2026-10-23_1002_cb85mXIfTv8.json:9` là TĂNG, nhưng câu trích ở dòng 22 nghiêng mạnh về test 78K; phần sau buổi lại có lời về quét lên 83K. Cần phân xử từ đúng đoạn/video, tách H4, hồi ngắn và đường đi, không sửa chỉ theo câu đầu tiên.

Còn **14/132 nhận định nhiều chặng** có hướng khác chặng cuối, trái quy tắc hiện hành tại `cong_cu/QUY_TAC_RUT_NHAN_DINH.md:18`. Ví dụ 19/5: trường H4=TĂNG nhưng đường đi kết thúc GIẢM 75K. Bộ chấm lại ghép trường hướng với đích cuối, dễ thành đích sai phía. Đây vừa là dữ liệu không nhất quán vừa là dấu hiệu schema chưa biểu diễn đủ ngữ nghĩa.

**Xử lý:** chốt riêng thiên hướng H4, chặng kế tiếp, đường đi, đích chính và hành động; phân xử mẫu bất đồng, lưu nguyên nhãn cũ cùng bản sửa và câu/ảnh nguồn. Không tự ép toàn kho sang hướng chặng cuối. Khóa phiên bản đáp án trước khi so điểm bot.

### 2. Giá tham chiếu trong bộ chấm có nhìn tới giá đóng sau thời điểm C

`thi/cham.py:80` và `cong_cu/cham_dich.py:58` dùng `bisect_left` trên **giờ mở H1**, rồi lấy close của nến ngay trước vị trí đó. Với **75/77 cutoff nằm giữa giờ**, close được chọn chưa tồn tại tại C.

Ví dụ 2/7: C = **04:07 UTC**, hàm lấy close của nến mở 04:00, chỉ biết lúc **05:00**, rồi bắt đầu kiểm diễn biến từ 05:00. Vừa dùng giá tương lai làm giá tham chiếu, vừa bỏ 53 phút ngay sau nhận định. Lỗi thuộc bộ chấm; phép cắt tương lai 77/77 của builder không phát hiện được lỗi này.

**Xử lý:** chọn giá có thời điểm công bố ≤ C; dùng dữ liệu nhỏ hơn H1 cho đoạn sau C trong nến đang chạy, hoặc khai báo khoảng đó chưa thể chấm. Lưu riêng giờ mở, giờ đóng, giờ phát hành dự báo và giờ quan sát sự kiện.

### 3. Điều kiện vô hiệu bị rút thành một cây H4, còn bỏ lần đóng đầu tiên sau C

`cong_cu/cham_dich.py:73–98` tách số trong câu nhưng không thực thi đủ khung và số nến: “hai H4” hoặc “D1 đóng” đều có thể thành một lần đóng H4. Dòng 97 còn yêu cầu giờ **mở H4 ≥ C**, khiến cây đã mở trước C nhưng đóng sau C bị bỏ qua.

Lỗi tương tự đi vào **đề thi**: `thi/tao_ho_so.py:562` (`trang_thai_moc`) dùng min/max close H4 cho cả mốc ghi D1/W1. Kiểm theo khung thật tìm được **19 hồ sơ** có ít nhất một mốc D1/W1 bị gắn “ĐÃ KÍCH HOẠT” khi chưa có close đúng khung. Ví dụ đề 9/7 đánh dấu mốc D1 62K của 7/7 bằng H4 61.699 dù D1 chưa đóng thủng.

**Xử lý:** lưu điều kiện có cấu trúc gồm giá/vùng, khung nến, số nến xác nhận, chiều, thời điểm bắt đầu hiệu lực. Dùng chung bộ tính trạng thái cho hồ sơ và chấm. Nếu chưa giải được điều kiện thì ghi chưa xác minh, không khẳng định đã vô hiệu.

### 4. TP và SL cùng nến H1 luôn được tính ĐÚNG

`cong_cu/cham_dich.py:90–93` chỉ cho SAI khi chạm SL mà chưa chạm đích; nếu cả hai chạm thì nhánh kế tiếp trả ĐÚNG. Dữ liệu OHLC H1 không chứng minh được thứ tự này.

Ví dụ tổng hợp đã chạy offline: LONG, TP 110K, SL 95K, một H1 có high 111K/low 94K → hàm trả ĐÚNG. Chưa tìm được ca cùng nến này trong 77 phiếu người với SL mà parser hiện chấp nhận; vì vậy chưa khẳng định lỗi đã làm tăng số thắng trên tập hiện tại.

Đường đi hai chặng cũng mới được lấy đích cuối và nới vùng xét mốc sai, chưa kiểm đúng thứ tự chặng. Vì vậy “đích cuối đã chạm” không đồng nghĩa kế hoạch hồi rồi giảm đã đúng.

**Xử lý:** sự kiện cùng nến phải để chưa rõ thứ tự hoặc tìm dữ liệu nhỏ hơn; báo riêng đúng đích và đúng đường đi. Không ưu tiên thắng ngầm. Hạn 14 ngày trong bài thi hiện là thước cố định phụ, cần giữ thêm kết quả theo hạn bot/người thực sự đã nêu.

## P1 — phần quan trọng còn thiếu hoặc chưa nối xong

### 5. Mốc của SOL/dầu lọt vào bản đồ BTC

- `moc/2026-08-10_8BGhoFetSaU.json:37`: mốc 73–74K được gán chắc, nhưng phần trích tự ghi đang nói H4 SOL; transcript cùng video xác nhận đoạn đó đang SOL.
- `moc/2026-07-09_Fmb8AziZ6f4.json:42–52`: có mốc 60K với `chac:true`, nhưng câu nguồn tự ghi “nói về dầu, không phải BTC”.

**Xử lý:** thêm tài sản, người phát biểu và loại ngữ cảnh vào mốc; cách ly các ca đã phát hiện, kiểm lại cả nhóm nghi ngờ. Không đưa mốc tài sản khác vào hội tụ BTC dù số trông hợp lý.

### 6. Có kho ảnh nghiên cứu, chưa có liên kết bằng chứng tới từng phiếu/bài làm

**0/180 phiếu** có trường timestamp đoạn nói và đường dẫn ảnh; **0/180 tệp mốc** có đường dẫn ảnh. **923/3.368 mốc** thiếu `moc_gio`, trong đó 50 tệp không có timestamp nào. 232 ảnh chỉ phủ 57/180 buổi. Các JSON nhận định/lệnh trong `nhan_dinh_bot/` cũng không tham chiếu chart.

Ghi chú ảnh đã làm khá kỹ, có xem lời trước/sau và ghi cặp/khung, nhưng chưa được gắn vào đúng hướng/đích/mốc sai của phiếu như `DESIGN.md:39–43` yêu cầu. Thi v3 hiện chủ yếu nhận bảng số và lời quá khứ, chưa chứng minh năng lực đọc chart cùng lời nói.

**Xử lý:** ưu tiên gắn video ID, khoảng VTT, ảnh cùng timestamp, cặp/khung và phần chưa đọc được vào các nhãn đang tranh luận. Dựng chart tới C cho từng dự báo bot, đánh dấu vùng/TP/SL, giữ riêng ảnh nguồn và chú thích bot.

### 7. Hồ sơ thiếu tín hiệu mà sổ tay vẫn yêu cầu dùng; bài làm đã có khẳng định vượt bằng chứng

`thi/tao_ho_so.py:49,99` bỏ volume khỏi cấu trúc nến dù CSV có sẵn; phần EMA chỉ có H4/D1/W1, không EMA tháng. H1 chỉ còn một giá đóng, không có chuỗi M5/M30. Hyblock/heatmap hiện tại chưa có, chỉ có lời/mốc của buổi trước. Trong khi sổ tay thi yêu cầu MA34 tháng (dòng 31), trap theo volume (128), phá thật có volume (136), tín hiệu M5/M30 (217).

Ví dụ bài làm mới `thi/bai_lam/2026-08-10_1001_8BGhoFetSaU.json:99` dùng “biên nến 0,1–0,4% không có volume (G3)” để kết luận phá giả; hồ sơ tương ứng không có số liệu volume. Biên giá nhỏ không tự chứng minh volume thấp. Bài 22/9 dòng 98 cũng khẳng định “volume vượt” khi gói đề không có chuỗi volume hiện tại. Đây là căn cứ chưa đủ nguồn xác minh, không thể tính như một xác nhận quan sát được.

**Xử lý:** bổ sung input có cutoff hoặc ghi danh sách trường thiếu và cấm dùng chúng như quan sát đã xác nhận. Mốc thanh lý cũ phải giữ ngày nguồn, không được tự biến thành heatmap hiện tại. Chấm tính có nguồn của căn cứ, không chỉ đếm số lý do.

### 8. Mục tiêu sửa sai bị thu hẹp thành bắt chước

`doi_chieu/SO_DOI_CHIEU.md:32` ghi **“Cả hai cùng sai giá → chỉ ghi, không sửa.”**, trái trực tiếp `DESIGN.md:51–53`. Bắt chước để đánh giá học hình mẫu là hợp lý, nhưng không thay thế vòng giảm lỗi thị trường mà user đã yêu cầu.

**Xử lý:** sửa chính sách, tách lỗi rút nhãn, lỗi bắt chước, lỗi dự báo thị trường và lỗi thực thi. Mỗi lần sửa cần phiên bản, bằng chứng đã xảy ra và kết quả trên buổi mới; không chỉ thêm một luật sau khi nhìn kết quả rồi chấm lại cùng buổi.

### 9. Luồng live và luồng thi đang dùng hai bộ quy tắc/chỉ báo khác nhau

`cong_cu/anh_thi_truong.py:35–36,94–95` còn SMA34/89/200, chưa phải dải EMA34/89/200/610. Tính lại offline 29/10 19h VN: SMA200 H4 **82.855,5**, EMA200 **81.635,1**, chênh khoảng **1.220 USD**; snapshot lưu trên đĩa khớp SMA. Builder thi mới đã dùng EMA đúng.

`so_tay/SO_TAY_TINH_HOA.md:443,470` còn coi D1/H4 trái chiều hoặc chờ không có lệnh là PHÂN VÂN. `thi/SO_TAY_T1_T6.md:68–76,104–106` đã sửa thành giữ view, tách hướng khỏi hành động. Nhận định live 30/10 vẫn dẫn sổ tay chính tại `nhan_dinh_bot/2026-10-30_2345.json:3`.

**Xử lý:** gom công thức chỉ báo và quy tắc quyết định thành nguồn có phiên bản dùng chung. Kết quả v3 trong bài thi không tự chứng minh pipeline live đã được sửa tương ứng.

### 10. Kiểm định thống kê và mẫu số chưa bảo vệ đủ kết luận

- `thi/cham.py:126–129` nới mốc phía kia theo chặng đầu, nhưng `:350–357` vẫn gọi phép thử đối xứng và kiểm so với 50%. Ví dụ giá 100, đích 90, chặng đầu 130 tạo hai biên 90/130; chúng không đối xứng. Ngay mô hình bước ngẫu nhiên không lệch, xác suất tới 90 trước 130 là 75%, không phải 50%. Cần giữ hai biên đối xứng hoặc bỏ kết luận so với tung xu.
- Có **7 phiếu người** bị nới một phía như vậy. Ví dụ 6/8: giá 64.734, đích 65.000, mốc đối diện 64.000; hai khoảng cách là 266 và 734 USD. Đây là lỗi của giả thuyết so sánh, độc lập với việc model có giỏi hay không.
- `:266–269` bootstrap từng buổi độc lập; chưa xét phụ thuộc thời gian, nhiều phiên cùng ngày và view kéo dài. Cần bootstrap khối và khoảng tin cậy của **chênh lệch cặp** bot–baseline; tránh kết luận thắng từ hai khoảng tỷ lệ riêng.
- `:245–252` loại bài bot thiếu nhãn hợp lệ khỏi tập chính, trong khi nhãn thiếu ở baseline được tính sai. Cần giữ các buổi có đáp án hợp lệ trong mẫu số đã khóa, tính lỗi bot/thiếu output là lỗi và báo riêng độ phủ.
- Độ giống mới chấm hướng, sai số đích/mốc sai ở những buổi cùng hướng và có số. Chưa đủ phép chấm vùng vào, hạn thực, lệnh, đường đi, râu và nguồn căn cứ theo thiết kế. Các trường `null` của người nói có thể hợp lệ; phải báo độ phủ, không bịa để đủ trường.

### 11. Khóa mã đã có, nhưng chưa khóa đầy đủ thí nghiệm

`thi/KHOA_CHAM.md:5–10` mới ghi hash bốn tệp. Bộ chấm vẫn đọc trực tiếp kho `phieu/`, `moc/`, bảng giờ, cache và bài làm hiện tại. Chưa tìm thấy trong `thi/` manifest khóa từng hồ sơ/đáp án, prompt đầy đủ, input/output thô, lần retry và cấu hình model mỗi lượt. Chưa thể xác minh từ các JSON kết quả rằng từng phiên suy luận được cách ly khỏi đáp án/future tools. Đây là thiếu bằng chứng kiểm toán, chưa phải bằng chứng model đã xem lén.

Có **6/77 hồ sơ trên đĩa** khác kết quả dựng lại bằng code hiện tại (1,2,3,6,7,9/7); diff quan sát được chỉ là metadata giờ thật/cờ giờ không chắc của các buổi tháng 6 trước đó, không thấy nến/nhãn/mốc đổi. Cần đồng bộ snapshot để tái lập đúng đầu vào đã thi; không diễn giải sáu ca này thành sáu đề sai số liệu.

Ngoài ra, `gio_vn` của bài làm 1/7 là 10:05 nhưng hồ sơ dùng cutoff 11:00 và giá nến đóng 11:00 (`thi/bai_lam/2026-07-01_WNiQnpm2BLo.json:4`, `thi/ho_so/2026-07-01_WNiQnpm2BLo.md:8`). Nếu đọc JSON như dự báo phát hành 10:05 sẽ thành nhận định có dữ liệu tương lai. Phải có trường riêng giờ live, cutoff và giờ phát hành; đừng dùng một trường cho cả ba.

**Xử lý:** giữ nguyên lần thi đang chạy làm bản chẩn đoán; lưu snapshot/hash đầy đủ của đầu vào, đáp án, prompt và đầu ra từng lượt. Sửa lỗi thành phiên bản mới và công bố ảnh hưởng, không âm thầm đổi đáp án/cách chấm để giữ tên một bài thi đã khóa. T7–T10 vẫn là đánh giá hồi cứu đã tham gia phát triển; cần đợt buổi mới lưu dự báo trước khi mở đáp án. Theo `DESIGN.md:86`, luồng vận hành ra trước live còn là một chế độ khác với bài thi hiện chốt dữ liệu cuối live.

### 12. Lệnh giấy chưa có bằng chứng đã chạy tiếp

Lúc kiểm khoảng 10:14 VN, cả `giay/trang_thai_v1.json` và `trang_thai_v2.json` vẫn cập nhật lần cuối **01:03:56**, `nen_cuoi=null`, `so_nen_da_xu_ly=0`; chưa có `giay/nhat_ky.csv`. `giay/cai_lich.sh:1–5` chỉ in hướng dẫn lịch, không cài lịch. Đây là trạng thái quan sát được; chưa kết luận nguyên nhân do lịch, máy ngủ hay tác vụ ngoài repo.

**Xử lý:** kiểm lịch thực tế và một lần xử lý nến thành công cùng nhật ký/giờ cập nhật; thêm phát hiện dữ liệu hoặc tác vụ quá hạn. Chưa thể gọi các tệp vốn 4.000 USD hiện tại là kết quả chạy ngoài mẫu đã tích lũy.

## P2 — vệ sinh dữ liệu/tài liệu

- `DESIGN.md:3,112` còn ghi chưa code/chưa trích ảnh. `AGENTS.md` ghi cờ `--toi-da`, nhưng CLI hiện dùng `--them`; chạy `--help` xác nhận. Cần cập nhật hiện trạng, giữ nguyên các yêu cầu user đã chốt.
- `so_tay/SO_LIEU_CAN_CU.md` là snapshot 179 buổi/3.349 mốc; không dùng nó như thống kê kho hiện tại 180/3.368. Gắn ngày/hash dữ liệu cho các báo cáo sinh ra.
- 21 mốc đảo cận `gia > gia_tren`; builder đã sort hai mép nhưng dữ liệu gốc/validator vẫn cần chuẩn hóa. Không nhầm hai transcript của 10/8 thành hai mẫu.
- Các script cũ `cong_cu/cham_dich.py:107–109`, `kiem_can_cu.py:92–98` chưa dùng chung bảng giờ thật. Ví dụ live 22/6 thực tế 20:47, phiếu cũ vẫn 10:00; tên video 29/7 có live thực tế sang 30/7 00:26. Builder thi đã sửa, cần chạy lại các thống kê cũ thực sự bị ảnh hưởng.

## Thứ tự làm tiếp cho Claude

1. Giữ snapshot lần chạy hiện tại; đánh dấu đây là lượt chẩn đoán chưa đủ điều kiện kết luận độc lập.
2. Phân xử 6 nhãn bất đồng, chốt schema hướng/chặng/hành động; cách ly các mốc sai tài sản.
3. Sửa bộ chấm thời điểm, điều kiện nến, TP/SL cùng nến; sửa trạng thái mốc trong đề. Kiểm bằng các tình huống nhỏ có thứ tự thời gian biết trước.
4. Đồng bộ snapshot hồ sơ, công thức EMA và bộ luật live/thi; bổ sung dữ liệu thiếu hoặc buộc bot ghi không đủ căn cứ.
5. Gắn lời nói–ảnh vào phiếu và chart vào dự báo; bổ sung chấm tuân thủ/nguồn căn cứ.
6. Khóa toàn bộ manifest rồi đánh giá lại với nhãn hồi cứu đúng nghĩa; thiết lập đợt buổi mới, dự báo lưu trước đáp án và kiểm được vòng học sửa sai.

## Phạm vi kiểm chứng

Kiểm cấu trúc toàn bộ 180 phiếu/180 tệp mốc và 23 phiếu độc lập; đọc trực tiếp mẫu bất đồng/đáng ngờ; kiểm mã các đường dựng hồ sơ, chấm và snapshot; phép cắt tương lai 77 buổi; kiểm cú pháp AST **24 tệp Python** và CLI `lay_transcript.py --help`. Mọi kiểm tra đều offline, không tải video hay sửa dữ liệu nguồn. Không nghe lại toàn bộ 180 video hoặc xem trực quan lại toàn bộ 232 ảnh; các bất đồng diễn giải còn cần phân xử từ nguồn. Các phát hiện là trạng thái lúc kiểm, có thể được Claude sửa sau báo cáo này.

Các ví dụ tổng hợp đã kiểm bằng cách thay dữ liệu nến trong bộ nhớ, không thay file: H4 mở trước C nhưng đóng sau C bị bỏ; điều kiện D1 bị áp bằng H4; TP/SL cùng H1 được trả ĐÚNG. Tệp Python đều qua kiểm cú pháp, nhưng các lỗi trên là lỗi hành vi nên kiểm cú pháp không phát hiện được.

Bốn hash đầy đủ đã kiểm lúc 10:11 VN, làm mốc nhận diện phiên bản đang được phản biện:

| Tệp | SHA-256 |
|---|---|
| `thi/cham.py` | `1d28f2402c06fc46e16c21c9ecb2f3902d60723e5a47cd9d1e8969506934f8b3` |
| `cong_cu/cham_dich.py` | `2c573d21212263bd2ec981eb584a0876ce5bdace83aabc8323417acd5a767df6` |
| `thi/tao_ho_so.py` | `f98633998531a540df10697ed9cb8ebff9439200270424f157503cfe0a369a88` |
| `thi/SO_TAY_T1_T6.md` | `196594481702a8d4e6978b573a19d3f5a08eaf297d57f85aa9c773cf28fd2119` |
