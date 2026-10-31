# Kiểm chéo B — rò rỉ bộ dựng đề và bộ chấm

Ngày kiểm: 31/10/2026. Chỉ thực hiện Việc B trong `GUI_CODEX_KIEM_CHEO.md`.

**Kết luận:** chưa thấy dữ liệu thị trường sau mốc C lọt vào các phép tính của bộ dựng đề hiện tại. Tuy nhiên, **bộ chấm dùng giá tương lai làm giá tham chiếu tại C ở 75/77 buổi**, và có các lỗi xử lý TP/SL, giờ đóng H4, điều kiện vô hiệu có thể làm sai điểm thị trường. Bài thi cũng đã nhiễm thông tin qua quá trình thiết kế, như chính file khóa thừa nhận. Chưa đủ cơ sở gọi kết quả này là kiểm định ngoài mẫu sạch.

Không đọc, liệt kê hay chấm `thi/bai_lam/`. Không chạy `main()` của bộ dựng đề/bộ chấm, không tải mạng, không sinh lại hồ sơ trên đĩa. Các phép kiểm chạy Python `-B`, chỉ đọc và dựng kết quả trong RAM; phép kiểm toàn bộ hồ sơ chặn mở file để ghi, tạo thư mục và kết nối mạng. Các phản ví dụ chỉ thay dữ liệu trong RAM. File duy nhất tôi ghi là báo cáo này.

Mức đánh giá: **P0 rò thật** khi có bằng chứng sử dụng thông tin sai thời điểm hoặc đã dùng tập thi để thiết kế; **P1 có thể rò** khi chưa đủ chứng cứ kết luận rò. Với lỗi chấm đã tái hiện nhưng không phải rò đầu vào, tôi ghi rõ điều đó bên cạnh mức P1. **P2 vệ sinh** là thiếu sót tái lập/kiểm tra bổ trợ.

## 1. Phát hiện

### B01 — P0 rò thật: giá tham chiếu của bộ chấm nằm sau C; cửa sổ kết quả cũng lệch biên giờ

**Vị trí:** `cong_cu/cham_dich.py:23`, `:58–63`, `:82–98`; `thi/cham.py:80–82`, `:93–107`, `:125–135`, `:226`.

CSV lưu **giờ mở nến**. Mã lấy:

```python
i0 = bisect_left(T1, bat_dau)
gia = H1[i0 - 1][3]
```

Với C ở giữa giờ, `i0 - 1` chính là nến đang chạy tại C; giá đóng của nó chỉ biết được sau C. Giá này quyết định `DICH_SAI_PHIA`, chọn mốc sai/SL và khoảng cách của phép thử đối xứng. Đây là rò vào **giá khởi tạo phép chấm**, không phải bằng chứng giá đó đã được đưa cho model làm bài.

Đối chiếu dữ liệu thật:

| Buổi | C theo VN | Giá H1 đã đóng, được phép biết | Giá bộ chấm dùng | Giá ấy chỉ đóng lúc |
|---|---|---:|---:|---|
| 19/08 `kfBEaOyHLkc` | 11:08 | 64.330,7 lúc 11:00 | 64.318,1 | 12:00 VN |
| 30/10 `f0JWA9aDHl8` | 11:24 | 78.225,0 lúc 11:00 | 78.267,1 | 12:00 VN |

Hồ sơ tương ứng ghi đúng giá được phép biết tại `thi/ho_so/2026-08-19_1001_kfBEaOyHLkc.md:8–9` và `thi/ho_so/2026-10-30_0955_f0JWA9aDHl8.md:8–9`. Có **75/77 C không tròn giờ**; cả 75 trường hợp đều rơi vào lỗi chỉ mục trên nếu cần tính giá tham chiếu. Chưa đo số điểm thực tế bị đổi vì không đọc bài làm.

Ngoài ra, `H1[i0:]` bỏ phần từ C đến đầu giờ tiếp theo. Ở cuối cửa sổ, điều kiện `t < het` lại nhận toàn bộ OHLC của nến mở trước hạn nhưng đóng sau hạn. Phản ví dụ trong RAM: C = 01/07 04:15 UTC, hạn = 15/07 04:15; nến 15/07 04:00–05:00 chứa giá chạm đích được tính `DUNG`, dù không biết cú chạm nằm trước hay sau 04:15. `thi/cham.py:131–135` có cùng vấn đề biên hạn trong phép đối xứng. Dùng giá tương lai để đánh giá kết quả là cần thiết, nhưng chỉ trong đúng cửa sổ đã khóa.

**Cách sửa:** chọn giá khởi tạo bằng `close_time <= C`; tốt nhất truyền cùng giá tham chiếu với hồ sơ. Dùng dữ liệu đủ nhỏ để xử lý hai nến cắt ngang C và C+14 ngày, hoặc khóa thời điểm có hiệu lực sang biên nến và công bố đúng thời điểm đó. Không cho toàn bộ OHLC sau hạn chứng minh một cú chạm trước hạn. Sửa đồng thời `gia_luc`, `cham`, `doi_xung`.

### B02 — P0 rò thật qua thiết kế: tập T7–T10 đã tham gia viết luật

**Vị trí:** `thi/KHOA_CHAM.md:18`; `thi/SO_TAY_T1_T6.md:28–32`, `:67–76`, `:280`; `DESIGN.md:16`.

File khóa ghi rõ: người thiết kế đã xem **toàn bộ 180 buổi** khi viết đặc tả; luật “giữ view” và “chu kỳ 4 năm” được nhấn mạnh sau khi xem dữ liệu cả năm. Sổ tay biến các lựa chọn đó thành thiên hướng nền và quy tắc bắt buộc. Việc dẫn ví dụ T1–T6 cho một luật không xóa được ảnh hưởng của tập thi lên **việc chọn luật**.

Đây là bằng chứng nhiễm tập thi ở cấp quy trình, không phải phát hiện mới rằng sổ tay chứa một mức giá tương lai cụ thể. File khóa đã công khai vấn đề này; băm khớp không khắc phục được nó.

**Cách sửa:** công bố T7–T10 là đợt hồi cứu đã tham gia phát triển; khóa phiên bản hiện tại rồi xác nhận trên các buổi mới chưa dùng để thiết kế. Không sửa luật dựa vào kết quả đợt xác nhận rồi tiếp tục gọi cùng đợt đó là ngoài mẫu.

### B03 — P1, lỗi chấm đã xác nhận: TP và SL cùng H1 luôn được tính ĐÚNG

**Vị trí:** `cong_cu/cham_dich.py:88–93`; đối chiếu `thi/cham.py:134–137`.

```python
if cham_sl and not cham_dich:
    return "SAI", ...
if cham_dich:
    return "DUNG", ...
```

Phản ví dụ trong RAM: giá tham chiếu 60.000, GIẢM tới 59.000, SL 61.000; H1 tiếp theo có H=62.000, L=58.000. Hàm trả `DUNG`. OHLC đó cũng phù hợp với đường đi chạm SL trước rồi mới tới đích, nên không chứng minh được “đích trước SL”. Phép đối xứng đã có `CUNG_NEN`, nhưng phép chấm chính không có trạng thái tương ứng.

**Cách sửa:** dùng dữ liệu nhỏ hơn để phân giải, hoặc trả `CUNG_NEN_KHONG_RO_THU_TU` và báo riêng. Nếu dùng giả định bảo thủ thì khóa trước và áp dụng cho mọi bên. Không mặc định ưu tiên kết quả có lợi. Đây là lỗi chấm chắc chắn, chưa phải bằng chứng model được xem tương lai.

### B04 — P1, lỗi chấm đã xác nhận: bỏ nến H4 đầu tiên đóng sau C

**Vị trí:** `cong_cu/cham_dich.py:95–98`.

Điều kiện `H4[k][0] >= bat_dau` so **giờ mở H4** với C, trong khi điều kiện vô hiệu phụ thuộc **giờ đóng H4**. Ví dụ C=04:15 UTC: nến 04:00–08:00 đóng sau C nhưng bị bỏ vì 04:00 < 04:15.

Phản ví dụ trong RAM: GIẢM tới 59.000, mốc sai “H4 đóng trên 60.500”; nến 04:00–08:00 đóng 61.000, rồi H1 08:00–09:00 mới chạm 59.000. Hàm vẫn trả `DUNG`, thay vì `SAI` lúc 08:00. Thời gian trả cho vô hiệu ở dòng 98 còn là đầu H1 cuối, sớm hơn giờ H4 đóng một giờ.

**Cách sửa:** tạo sự kiện đóng H4 với `open + 4h > C`; chọn đúng nến bằng khóa thời gian bằng nhau, xử lý theo thứ tự sự kiện, trả giờ đóng thật. Không yêu cầu H4 phải mở sau C.

### B05 — P1, sai điều kiện vô hiệu: thay mọi khung bằng H4 và rút điều kiện chữ thành một con số

**Vị trí:** `thi/tao_ho_so.py:562–590`, `:593–611`; `cong_cu/cham_dich.py:71–81`, `:95–98`; `thi/cham.py:103–107`.

**Bằng chứng trên hồ sơ thật:** `thi/ho_so/2026-10-30_0955_f0JWA9aDHl8.md:438` ghi:

> 81.500–82.000 · vô hiệu · GIAM · D1 · đóng nến trên 81.500 hoặc 82 thì thôi view giảm · ĐÃ KÍCH HOẠT (đóng H4 cao nhất 81.776)

Mốc thuộc buổi 28/10. Các D1 đã đóng sau lúc buổi đó bắt đầu đến C 30/10 có close **81.350,9** và **78.007,2**, đều dưới 81.500; max close H4 là **81.776,2**. Nhãn kích hoạt D1 này vì vậy sai, dù tất cả nến được dùng đều trước C. Đây là lỗi diễn giải trạng thái mốc, không phải dùng nến tương lai.

`trang_thai_moc` không xét `khung`, điều kiện hai nến liên tiếp hoặc thời điểm phát biểu từng mốc. `bang_moc` lấy mọi H4 đóng sau **bắt đầu live nguồn**, kể cả khi mốc chỉ được nêu cuối live; râu của H4 còn có thể thuộc phần trước lúc nói. Bộ chấm cũng dùng H4 cho con số trong `vo_hieu_khi`, không thực thi đầy đủ D1/hai nến/điều kiện kết hợp. Chỉ cần chuỗi có `H1`/`scalp` thì còn bỏ toàn bộ mốc chữ, kể cả chuỗi chứa thêm điều kiện H4.

**Cách sửa:** lưu mốc có cấu trúc: giá/vùng, chiều so sánh, khung, râu hay đóng, số nến xác nhận, điều kiện kết hợp, thời điểm phát biểu. Tính trạng thái từ nguồn nến đúng khung và sau thời điểm có hiệu lực. Thiếu timestamp/không phân tích được điều kiện thì ghi “chưa xác định”, không tự khẳng định đã kích hoạt.

### B06 — P1, nguy cơ chọn mẫu: bài bot thiếu/lỗi được loại; điểm thị trường chưa so sánh theo cặp đủ điều kiện

**Vị trí:** `thi/cham.py:204–209`, `:245–263`, `:337–362`.

- Thiếu file bài làm: `continue`, không đi vào `dong`.
- Có file nhưng bot thiếu hướng hợp lệ: không vào `so`. Baseline thiếu nhãn được tính sai trong bảng, nhưng bot thiếu nhãn đã bị loại trước bảng.
- Điểm hướng của bot và bốn baseline **đúng là dùng cùng `so`**. Tuy nhiên `so` phụ thuộc tình trạng bài bot, nên có thể làm điểm tất cả bên đổi khi giữ/bỏ file hoặc làm nhãn không hợp lệ. Chưa có bằng chứng việc này đã xảy ra.
- Điểm thị trường của bốn bên dùng cùng `dong` về danh sách gốc, nhưng `% đúng` lấy mẫu số riêng `DUNG+SAI+SAI_HET_HAN`. Các bên có thể khác tập đã ngã ngũ, thiếu đích, đích sai phía và PHÂN VÂN. Phép đối xứng cũng lấy riêng `THANG+THUA`. Không thể coi hai tỷ lệ này tự động là so sánh trên cùng tập thực sự được tính điểm.

**08-27:** `phieu/2026-08-27_1006_ZJ5BVqdLJeE.json:8` là H1, dòng 30 là D1, không có H4/chung. Loại khỏi so hướng là phù hợp quy tắc đã khai báo, không phải bằng chứng chọn theo điểm bot. Tập nhãn hợp lệ độc lập với bot hiện có **76 buổi: GIẢM 44, TĂNG 16, PHÂN VÂN 16**. Nếu đủ bài hợp lệ, baseline luôn GIẢM là **44/76**, không phải 44/77. Phần thị trường vẫn có thể giữ buổi 08-27 với người `KHONG_VIEW`; cần công bố rõ hai tập khác nhau.

**Cách sửa:** khóa danh sách 76 buổi có nhãn trước khi đọc bài làm; thiếu/lỗi bài bot phải tính là lỗi và báo độ phủ. Chỉ ngoại lệ kỹ thuật được khóa trước mới được loại đồng thời cho tất cả bên. Với thị trường, giữ bảng trạng thái toàn bộ buổi và thêm so sánh cặp trên tập đủ điều kiện chung, kèm mẫu số/độ phủ; không dùng tỷ lệ đã ngã ngũ riêng làm bằng chứng thắng trực tiếp.

### B07 — P1 có thể rò/chỉnh điểm qua đầu vào: khóa bốn file chưa khóa được lần thi

**Vị trí:** `thi/KHOA_CHAM.md:3–10`; `thi/cham.py:194–209`; `thi/tao_ho_so.py:65–71`, `:104–106`, `:180–212`, `:226–227`; `cong_cu/cham_dich.py:21–27`.

Không thấy bộ chấm kiểm tra hash trước chạy. Manifest khóa chỉ chứa bốn tiền tố hash, chưa bao gồm `gio_live.tsv`, danh sách buổi, phiếu đáp án, mốc, CSV, cache nguồn phụ và hồ sơ đã gửi. Thay những file này có thể đổi C, nhãn, baseline, kết quả giá mà không đổi hash bốn file. `--bai-lam` cũng cho chọn một thư mục khác; kết hợp cơ chế bỏ bài thiếu ở B06 sẽ đổi tập chấm.

**Bằng chứng tái lập:** dựng lại cả 77 hồ sơ từ đầu vào hiện tại có **6 hồ sơ khác bản lưu**: 01/07, 02/07, 03/07, 06/07, 07/07, 09/07. Toàn bộ khác biệt tìm được chỉ ở tiêu đề buổi trước: giờ live, cờ chắc chắn và khoảng cách thời gian. Ví dụ `thi/ho_so/2026-07-01_WNiQnpm2BLo.md:203` ghi 30/06 bắt đầu 10:00, “giờ không chắc”; `gio_live.tsv` hiện cho 10:02, nguồn youtube. Không thấy giá, nhãn hay trạng thái mốc khác trong sáu bản so này. Không suy ra đã sửa sau khi xem bài làm; chỉ kết luận gói đầu vào chưa bất biến và chưa tái lập y hệt.

Trong lúc kiểm, `gio_live.tsv` còn tăng từ 98 dòng ở lần đọc đầu lên 109 dòng ở lần đọc sau; tôi không ghi file đó. Vì thư mục đang có công việc đồng thời, số dòng của file dữ liệu là tham chiếu tại lúc đọc, không phải định danh phiên bản bền vững.

**Cách sửa:** cho lần thi kế tiếp, lưu đầy đủ SHA-256 của mọi đầu vào, prompt, model/config, output thô, danh sách đủ điều kiện và phiên bản nguồn; kiểm manifest trước chấm. Dùng bản snapshot chỉ đọc, không tự cập nhật cache khi chấm. Đợt hiện tại cần ghi lại sai khác và phiên bản thực sự đã gửi cho từng lượt, không âm thầm sinh lại đề giữa kỳ.

### B08 — P1 có thể rò: `available_at` nguồn ngoài mới là giả định, chưa chứng minh phiên bản đã biết ở quá khứ

**Vị trí:** `thi/tao_ho_so.py:42–46`, `:65–71`, `:129–152`, `:287–304`.

F&G lấy timestamp ngày +1h; Yahoo gán giờ đóng phiên +30 phút; CMC gán timestamp/timeClose +1h. Các phép lọc thực thi đúng **những giả định này**. Tuy nhiên cache tải hồi cứu không có phiên bản đương thời, bằng chứng giờ công bố thực tế hoặc lịch sử sửa số. Với Yahoo, ngày timestamp được gán sang một giờ đóng giả định; với CMC, timestamp lịch sử được hiểu là ảnh chụp. Phép thử cắt tương lai không phát hiện được một hàng đã bị gán sai `available_at` hoặc một số quá khứ được sửa muộn.

Không tìm được hàng cụ thể chứng minh rò nguồn ngoài trong dữ liệu đã kiểm; vì vậy giữ mức **có thể rò**, không gọi P0.

**Cách sửa:** giữ response gốc/hash, `retrieved_at`, quy tắc và bằng chứng suy ra `available_at`; phân biệt thời điểm sự kiện với lúc công bố và phiên bản dữ liệu. Với nguồn chưa chứng minh được, công bố giả định/độ trễ đã khóa hoặc bỏ trường đó trong phép kiểm sạch. Không mô tả cache tải hôm nay như bản lưu đương thời.

### B09 — P1 có thể rò qua model/ngữ cảnh: ngày, ID và quyền mở kho vẫn là đường cần khóa

**Vị trí:** `thi/tao_ho_so.py:390–407`, `:634–650`; `thi/ho_so/2026-07-01_WNiQnpm2BLo.md:1`, `:6`, `:203`; `thi/KHOA_CHAM.md:13–18`.

Hồ sơ lộ ngày chính xác, video ID, tên buổi và toàn bộ phiếu buổi trước. Đây có thể là khóa tra cứu hoặc tín hiệu gợi nhớ sự kiện nếu lượt model có web/quyền mở đáp án/ngữ cảnh từ tác vụ trước. Mốc kiến thức “06/2026” ở file khóa không tự chứng minh lượt thi cô lập hoặc bảo đảm model không có tri thức mới hơn. Tôi không kiểm chứng mốc kiến thức nhà cung cấp và không đọc bài làm/log lượt thi.

Không thấy **phiếu hiện tại hoặc ID hiện tại trong phần f** của cả 77 hồ sơ. Phiếu trước thuộc T7–T10 là thông tin hợp lệ theo chế độ đã khai báo, miễn đúng thứ tự thời gian; không tự coi đó là rò. Ngày cũng có vai trò hợp lệ cho thứ Hai/đầu tháng, nên chỉ có ngày trong đề chưa đủ chứng minh rò.

**Cách sửa:** mỗi lượt chỉ nhận gói đã khóa; chặn web và quyền đọc `phieu/`, `moc/`, transcript/đáp án hiện tại hoặc tương lai; dùng ngữ cảnh mới. Dùng mã buổi vô nghĩa thay video ID. Nếu làm đối chứng che ngày, cung cấp riêng thứ/ngày đầu tuần-tháng và giữ nó là một biến thể phát triển đã khai báo, không chọn biến thể theo điểm rồi giữ tên bài thi cũ.

### B10 — P1, phép chấm chưa thực thi đủ kế hoạch: đường hai chặng và SL chưa gắn trạng thái có hiệu lực

**Vị trí:** `cong_cu/cham_dich.py:52`, `:64–81`, `:85–93`; `thi/cham.py:70–75`, `:227–229`.

Đường nhiều chặng chỉ được lấy đích cuối; chặng đầu chỉ làm dịch `nguong` chọn mốc sai/SL. Không có trạng thái yêu cầu chặng 1 đã xảy ra trước chặng 2. Một SL thật nằm trước đích chặng 1 còn có thể bị loại vì không vượt `nguong`. SL được lấy từ lệnh `de_xuat_moi` cùng chiều mà không kiểm tra đã có tín hiệu vào/đã khớp; lệnh `dang_giu` lại bị bỏ. `chuan_bai` mặc định bài thiếu trạng thái lệnh thành `de_xuat_moi`.

Khi chép nguyên view/lệnh buổi trước rồi bắt đầu chấm lại từ C hiện tại, không có cơ chế kiểm hạn gốc, lệnh đã chốt hay mốc đã vô hiệu trước C. Do đó đây là đối chứng “tái phát hành view cũ tại C”, chưa phải mô phỏng tiếp tục giữ một view/lệnh còn sống. Các quy tắc này có thể đổi điểm theo cách viết JSON; chưa đo tác động thực tế trên bài làm.

**Cách sửa:** khóa rõ chỉ chấm đích cuối hay cả thứ tự đường đi và đặt tên thước đo tương ứng. Tách vô hiệu của view khỏi SL của lệnh; SL chỉ có hiệu lực khi trạng thái lệnh phù hợp và không bị tự bỏ vì chặng dự báo. Nếu gọi là “giữ view”, cần mang theo thời điểm phát hành, hạn và trạng thái hiệu lực gốc; nếu tái phát hành, công bố đúng nghĩa đó.

### B11 — P2 vệ sinh: `--kiem` không phải lệnh chỉ đọc; thống kê chưa xử lý phụ thuộc thời gian

**Vị trí:** `thi/tao_ho_so.py:670–693`; `thi/cham.py:264–269`, `:282–284`, `:350–362`.

- `--kiem` vẫn gọi `HS.mkdir`, `p.write_text` trước kiểm; khởi tạo `DuLieu` còn có thể tải/ghi cache nếu thiếu. Tôi **không chạy CLI này**. Nên tách chế độ kiểm chỉ đọc, thất bại nếu cache thiếu, không ghi hồ sơ.
- Bootstrap hiện lấy mẫu từng buổi độc lập; McNemar/nhị thức cũng chưa xử lý sự phụ thuộc giữa các buổi gần nhau và cửa sổ 14 ngày chồng lấn. Điều này không phải rò đầu vào, nhưng có thể làm bằng chứng thống kê quá lạc quan. Nên khóa bootstrap theo khối thời gian và báo chênh lệch cặp; McNemar hiện tại chỉ là kiểm phụ. Mệnh đề đối xứng “50% = tung đồng xu” cũng cần ghi là giả thuyết chuẩn tham khảo, nhất là khi mốc phía kia được nới theo chặng 1.

## 2. Những mục đã kiểm, không thấy rò trực tiếp

### Mốc cắt, OHLC, EMA/RSI, pivot và Fibo

**Đã kiểm, không thấy** nến sau C lọt vào các phép tính bộ dựng đề hiện tại, theo quy ước timestamp của kho:

- `thi/tao_ho_so.py:104–110` đọc `1Dutc`, quy đổi giờ mở sang UTC và giờ đóng bằng cộng độ dài; `:274–276` cắt theo **giờ đóng <= C**, không phải chỉ lọc giờ mở/ngày.
- D1 mở 00:00 UTC = 07:00 VN; W1 bắt đầu thứ Hai 00:00 UTC. Không thấy dùng D1 theo 00:00 VN hoặc nhầm `1D` thay `1Dutc`. Ví dụ hồ sơ 01/07 dòng 44 và 58 ghi đúng quy ước.
- D1/W1/tháng đang chạy được gộp từ H4 **đã đóng tới T** (`:278–286`), không dùng OHLC cuối kỳ. Đây là OHLC tạm, có thể cũ hơn C tới gần 4h. H4 đang chạy không được đưa vào hồ sơ. EMA/RSI chỉ tính trên chuỗi đã cắt; không dùng nến đang chạy cho EMA hoàn tất.
- Fractal H4 k=3, D1 k=5 chỉ xét khi đủ k nến phải; giờ xác nhận là `nens[i+k].dong` (`:339–349`, `:477–491`). Đã kiểm **4.101 lượt pivot xuất hiện trên 77 hồ sơ**, không có giờ xác nhận sau C.
- Fibo D1 dùng chuỗi cắt và D1 tạm; Fibo H4 dùng pivot đã xác nhận và cực trị chỉ trong chuỗi cắt (`:496–523`). Không thấy lấy neo từ dữ liệu sau C. Đây là cách chọn sóng tự động được khai báo, chưa phải bằng chứng trùng neo người đó vẽ.
- Dựng trong RAM **cả 77 hồ sơ**, rồi xóa toàn bộ nến/nguồn ngoài sau C và buổi chưa kết thúc trước live: **77/77 kết quả giữ nguyên**. Đây là kiểm thuật toán cắt dữ liệu; không chứng minh thời điểm công bố nguồn ngoài hoặc độ sạch quá trình thiết kế (B02/B08).

Đọc đối chiếu hồ sơ đầu kỳ 01/07, giữa kỳ 19/08 và cuối kỳ 30/10; so toàn bộ hồ sơ lưu với bản dựng lại bằng máy. Sáu khác biệt chỉ là metadata buổi trước như B07; hai mẫu giữa/cuối trùng hoàn toàn ở lần kiểm.

Kho nến dùng để dựng tại lúc kiểm: H4 6.204 nến, D1 3.215 nến, H1 8.018 nến; không thấy lỗ thời gian trong các chuỗi này theo bước tương ứng. Không suy rộng thành chứng nhận độ chính xác giá/sàn.

### Buổi trước và trạng thái “mốc đã phá”

**Đã kiểm, không thấy** lấy nhầm phiếu buổi sau vào bộ dựng đề: `ds_buoi` ưu tiên giờ trong `gio_live.tsv`, sắp theo giờ bắt đầu thật; `buoi_truoc` yêu cầu kết thúc <= giờ bắt đầu buổi hiện tại (`thi/tao_ho_so.py:187–223`), còn chặt hơn chỉ yêu cầu kết thúc trước C. Mọi buổi trong sáu nguồn đã dùng của 77 hồ sơ đều qua kiểm `Cat.kiem`.

Đã đối chiếu các ca dễ sai ngày/thứ tự:

| Hồ sơ hiện tại | Nguồn liền trước được chọn | Nhận xét |
|---|---|---|
| `2026-07-29__TlYbqPT8nU` | live sáng 29/07 `2FMmTeLGCNY` | File mang ngày 29/07 nhưng live thật 30/07 00:26–01:23; mã dùng giờ thật, không lấy sáng 30/07 |
| 17/09 00:26 `7mETSY5t5Yg` | sáng 16/09 | Không lấy sáng 17/09 |
| 17/09 10:02 `1cUPKUmEnr4` | 17/09 00:26 `7mETSY5t5Yg`, hết 01:26 | Đúng thứ tự |
| 29/10 00:33 `4Hg5YedKaAg` | sáng 28/10 | Không lấy sáng 29/10 |
| 29/10 10:05 `wcDxLBw0TO4` | 29/10 00:33 `4Hg5YedKaAg`, hết 01:23 | Đúng thứ tự |
| 30/10 `f0JWA9aDHl8` | sáng 29/10 `wcDxLBw0TO4` | Đúng thứ tự |

Điều kiện code là `<=` chứ không phải `<`; không gặp nguồn chạm đúng giờ bắt đầu trong các nguồn đã dùng. Không thấy nến sau C được dùng cho “ĐÃ PHÁ”. **Nhưng điều kiện phá có thể sai khung/thời điểm phát biểu**, đã nêu B05; không thể kết luận toàn bộ nhãn trạng thái mốc là đúng.

### Sổ tay T1–T6

**Đã đọc toàn bộ 307 dòng; không thấy con số/sự kiện cụ thể nào được chứng minh chỉ xuất hiện từ tháng 7 trở đi.** Trích xuất được 230 tham chiếu ngày dạng dd/mm trong ngoặc vuông; tất cả tháng 1–6. Đã đối chiếu các mức dễ bị nghi ngờ với ghi chú T1–T6, không chỉ dò chuỗi ngày.

Các dòng cần lưu ý khi kiểm nguồn, nhưng **chưa đủ bằng chứng kết luận rò giá/sự kiện**:

| Dòng `thi/SO_TAY_T1_T6.md` | Nội dung nghi vấn ban đầu | Kết quả đối chiếu |
|---|---|---|
| 12, 20 | đỉnh 126K, cuối năm 35K, T4/2027 25K, đáy 28–30K | Có nguồn T6 trong `so_tay/ghi_chu/nhom_5.md:7`, `:113`, `:133–134`; các mốc tương lai là lời dự báo quá khứ, không tự thành rò |
| 25, 37 | gãy 63K, 59–60K, 63.003K | Có trong `nhom_5.md:7`, `:101`, trước tháng 7 |
| 31 | điều kiện bỏ nhãn hồi kỹ thuật, ghi “suy luận” | Không có nguồn phát biểu riêng; cần giữ tư cách luật người soạn, không khẳng định là phát hiện chỉ từ T1–T6 |
| 69–76, 280 | mặc định giữ view, viện dẫn `DESIGN.md` | Đường nhiễm thiết kế đã được thừa nhận ở B02; không tìm được câu giá T7–T10 mới ở đây |
| 90 | “đúng 4/4 thứ Hai tháng 6” | Không vượt cutoff T6; là thống kê chọn luật cần nguồn, không phải thống kê kỳ thi |
| 158 | Fibo 78.800 / 83.418 và nhịp 97,9K→59,8K | Tự ghi bối cảnh T3–T5; không thấy bằng chứng chỉ có từ tháng 7 |
| 287–307 | ví dụ dựng lại 24–25/06, hạn 27/06, mốc/SL cụ thể | Được gắn là ví dụ làm tròn; không thấy kết quả giá sau tháng 6 được đưa vào ví dụ. Các số dựng/suy luận cần phân biệt với trích nguyên văn |

Giới hạn: đây là rà nội dung và đối chiếu tài liệu nguồn cục bộ, không phải rút lại toàn bộ nhãn từ video. Không thể từ đó chứng nhận mọi câu đều được soạn độc lập với tập thi; B02 cho biết điều ngược lại ở cấp chọn luật.

### PHÂN VÂN, baseline và tham số cố định

- **Đã kiểm, không thấy** PHÂN VÂN bị loại khỏi chỉ số chính chỉ vì là PHÂN VÂN: `thi/cham.py:37`, `:245–263`, `:273–290`, `:304–313` tính ba lớp và báo riêng độ phủ PHÂN VÂN. Chỉ số “khi cả hai có hướng” là phụ, có mẫu số riêng. Ngoại lệ bot thiếu/lỗi nhãn là B06.
- **Đã kiểm, không thấy** baseline hướng nhìn vào đáp án buổi hiện tại trong logic đoán: chép/giữ view lấy phiếu đã kết thúc trước live; luật từ trên xuống dùng `Cat(du, C)` (`:210–225`). Cả bốn baseline hướng đi qua cùng `so` với bot. Luôn GIẢM/luật không có đích nên được ghi rõ không chấm thị trường, không bị ngầm tính bằng một thước khác.
- “Giữ view” baseline ở `:212` chỉ lấy hướng TĂNG/GIẢM gần nhất, bỏ PHÂN VÂN; **không có công tắc vô hiệu/chạm đích**. Đó là đúng định nghĩa code đã khóa, nhưng tên gọi không chứng minh nó thực thi luật giữ/đổi view đầy đủ trong sổ tay.
- **Đã kiểm, không thấy** tham số CLI cho tùy chỉnh 0,6% / 1,01 / −1% hay seed/bootstrap mà vẫn giữ nguyên hash code. `thi/cham.py:29` ép `HAN_CO_DINH=336`, nên biến môi trường bên ngoài không đổi được hạn khi chạy đúng bộ chấm thi. Chạy riêng `cham_dich.py` thì `HAN_MAC_DINH`/`HAN_CO_DINH` thay được qua môi trường (`:18`, `:82`) và CLI còn suy giờ bắt đầu từ tên file (`:107–108`), **không tương đương** bài chấm thi từ C.
- Wrapper `cham_thi_truong` có đổi kết quả chưa ngã ngũ sang `CHUA_HET_HAN` nếu dữ liệu chưa phủ hết 14 ngày (`thi/cham.py:110–117`). Kho H1 tại lúc kiểm đóng tới 31/10 02:00 UTC: **67/77 buổi đủ trọn cửa sổ, 10 buổi chưa đủ**. Không thấy wrapper ép hết hạn thành sai; những kết quả đã chạm đích/SL sớm vẫn được giữ là ngã ngũ. Các lỗi thời điểm B01/B04 vẫn áp dụng.

## 3. SHA-256 bốn file khóa

Đã chạy `rtk proxy shasum -a 256` và kiểm lại gần cuối lượt. Bốn hash không đổi giữa hai lần kiểm:

| File | SHA-256 hiện tại | So với `KHOA_CHAM.md:7–10` |
|---|---|---|
| `thi/cham.py` | `1d28f2402c06fc46e16c21c9ecb2f3902d60723e5a47cd9d1e8969506934f8b3` | Khớp tiền tố 16 ký tự đã ghi |
| `cong_cu/cham_dich.py` | `2c573d21212263bd2ec981eb584a0876ce5bdace83aabc8323417acd5a767df6` | Khớp tiền tố 16 ký tự đã ghi |
| `thi/tao_ho_so.py` | `f98633998531a540df10697ed9cb8ebff9439200270424f157503cfe0a369a88` | Khớp tiền tố 16 ký tự đã ghi |
| `thi/SO_TAY_T1_T6.md` | `196594481702a8d4e6978b573a19d3f5a08eaf297d57f85aa9c773cf28fd2119` | Khớp tiền tố 16 ký tự đã ghi |

File khóa dùng dấu `…`, không lưu đủ 64 ký tự; vì vậy kết luận chính xác là **khớp toàn bộ phần hash được công bố**, không thể đối chiếu hậu tố chưa lưu. Cũng không thể dùng hash hiện tại để chứng minh thời điểm khóa lịch sử hoặc chứng minh đầu vào khác chưa đổi.

SHA-256 `transcripts/gio_live.tsv` tại đợt kiểm cuối: `be100722171b1c3544ffb14bc87b74e66f69e6cba0f077054545e89b9fb980ab`. Đây là dấu nhận diện snapshot kiểm, không phải hash đã được khóa trước bài thi.

## 4. Phạm vi kết luận và hướng xử lý

Không sửa mã, đáp án, hồ sơ hay kết quả đang chạy. Các cách sửa ở trên là đề xuất cho phiên bản kế tiếp. Kết quả đợt hiện tại cần giữ nguyên và công bố kèm lỗi đã biết; sửa bộ chấm phải có phiên bản mới và báo rõ thay đổi quy tắc, không ghi đè lịch sử.

Ưu tiên xử lý: B01/B03/B04/B05 trước khi diễn giải điểm thị trường; B06/B07 trước khi khẳng định bot vượt baseline; B02/B08/B09 trước khi gọi lần xác nhận tiếp theo là sạch. Báo cáo này không kết luận bot được bao nhiêu điểm, agent nào đã đọc gì, hoặc đã có hành vi chỉnh điểm sau khi xem bài làm.
