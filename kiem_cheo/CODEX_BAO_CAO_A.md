# CODEX — Báo cáo Việc A: rút phiếu độc lập cho 23 buổi

Đã đọc **toàn bộ 23 transcript** theo `danh_sach.txt`, gồm cả phần đầu, hỏi đáp và cập nhật cuối buổi. Chỉ dùng danh sách, các transcript được chỉ định và quy tắc Việc A; không đọc `phieu/`, `moc/`, `so_tay/`, `thi/`, `nhan_dinh_bot/`. Không thực hiện Việc B. Các file đầu ra nằm trong `kiem_cheo/`.

Có 23 phiếu ở `codex_phieu/`; tên buổi trong bảng liên kết tới đúng JSON. Những bản `.md` không có timestamp được dẫn theo tên mục; bản `.txt` dẫn theo timestamp trong transcript. Nội dung là ý kiến người nói tại thời điểm buổi đó, không dùng buổi khác hoặc dữ liệu giá về sau để sửa nhãn.

## Cách đọc phiếu và bảng

- **Hướng H4** là thiên hướng người nói, tách khỏi lệnh đang làm. Short scalping ngược sóng không tự biến H4 thành GIAM; đứng ngoài chờ entry không tự biến H4 thành PHAN_VAN. Khi chặng điều chỉnh và xu hướng H4 dễ lẫn, ghi giới hạn và độ chắc trong phiếu.
- `duong_di` ghi các chặng của kịch bản được phân tích. Những chặng còn phụ thuộc xác nhận được nêu rõ trong `ghi_chu`; không có nghĩa mọi chặng sẽ xảy ra. Vì schema không có trường điều kiện cho từng chặng, cần đọc ghi chú cùng đường đi.
- `dich_chinh` khớp **đích của chặng cuối đã ghi**, không bắt buộc là TP của lệnh hiện tại. Ví dụ 25/3: H4 nghiêng tăng nhưng có chặng giảm sau hồi về 64.000; 6/1: short scalping hiện tại khác long dự kiến từ 91.000.
- Một vùng giá không bị thay bằng trung điểm hoặc một đầu vùng tùy ý: trường số để `null`, giữ nguyên vùng trong ghi chú/bảng. Số chỉ từ tiêu đề hoặc mức làm tròn được ghi rõ là xấp xỉ; không có giá hiện tại rõ thì `gia_btc_luc_noi=null`.
- **Mốc sai** có thể là điều kiện phải xét lại view, không nhất thiết là SL lệnh. Khi không có mốc số rõ, để `null`; không lấy mốc xác nhận vào lệnh hay mốc sai của phe đối diện thay thế.
- **Phá vỡ giả** phân biệt sự việc đã được người nói nhận diện với kịch bản giả định. Các đoạn chỉ mô tả quét thanh khoản, ví dụ lịch sử hoặc fake out của vàng/altcoin không được gán thành cú fake out BTC hiện tại.
- `do_chac` là độ chắc của **việc rút nhãn**, không phải xác suất dự báo giá đúng. `doi_y_giua_buoi` ghi thay đổi thiên hướng H4 nhận thấy trong buổi, không chỉ đổi TP; các trường hợp suy luận được đánh dấu cần kiểm chéo bên dưới.

Giá trong bảng tính bằng USD/BTC. Dấu `§` trong tóm tắt là vị trí/mục trong nguồn, không phải dữ liệu ngoài transcript.

## Bảng 23 buổi

| Buổi | Đầu H4 | Cuối H4 | Hành động hiện tại | Đích / chặng | Mốc sai / điều kiện xét lại | Phá vỡ giả |
|---|---|---|---|---|---|---|
| [2026-07-01_WNiQnpm2BLo](codex_phieu/2026-07-01_WNiQnpm2BLo.json) | GIAM | GIAM | Chờ hồi lấy entry short | null; hồi 60.000–60.400 → giảm 54.000–51.000 | 61.000; phá/đóng H4 trên đó phải xét lại | Có: phá xuống sáng rồi rút lên, §21:36–22:13 |
| [2026-07-09_Fmb8AziZ6f4](codex_phieu/2026-07-09_Fmb8AziZ6f4.json) | GIAM | GIAM | Vào short scalping | 60.500; TP1 61.000 | null; không có SL chung rõ | Cảnh báo trap short khi hồi test lại MA, chưa xác nhận cú mới |
| [2026-07-16_bwgz_kMSvfE](codex_phieu/2026-07-16_bwgz_kMSvfE.json) | TANG | TANG | Vào short nhỏ ngược H4 | 67.000; chỉnh 63.000–64.000 trước | 61.600; thủng là mất nhịp tăng | null; fake out được nói về vàng |
| [2026-07-27_YMlDceykaTw](codex_phieu/2026-07-27_YMlDceykaTw.json) | TANG | TANG | Chờ entry long | null; H4 67.000, D1 vùng 70.000–72.000 | null; 67.000 là cảnh báo cho short | null |
| [2026-07-31_SlGyokVNofU](codex_phieu/2026-07-31_SlGyokVNofU.json) | GIAM | GIAM | Chờ hồi lấy entry short | 60.000; trước 62.500 | 65.000; H4 vượt cản và D1 xác nhận | null; mô tả quét short rồi kill long, chưa gọi fake out BTC rõ |
| [2026-08-07_N-7XihrObp8](codex_phieu/2026-08-07_N-7XihrObp8.json) | TANG | GIAM | Vào short test nhỏ | null; quét 63.000–63.300/63.500 rồi xét hồi | null; H4 đỏ xuyên cụm hỗ trợ thì hủy long chờ | null |
| [2026-08-14_1004_xK38gQ-G6uA](codex_phieu/2026-08-14_1004_xK38gQ-G6uA.json) | GIAM | GIAM | Giữ short chờ TP tại hỗ trợ | null; 63.100–62.000 → pump trên 64.000 → 5x | null; 62.500 là điều kiện short đuổi | null; có dự phóng pump kill short, không gọi rõ fake/trap BTC |
| [2026-08-21_1003_oDD5qwLcZbw](codex_phieu/2026-08-21_1003_oDD5qwLcZbw.json) | TANG | TANG | Chờ entry; chưa khớp short M5 | 77.000; có thể quét 78.000 | null; M5 trên 75.000 chỉ hủy short scalping | null; các đoạn fake out là lịch sử/giảng cấu trúc |
| [2026-09-03_1012_8LXm3pVw9yI](codex_phieu/2026-09-03_1012_8LXm3pVw9yI.json) | GIAM | GIAM | Giữ short hôm trước | 76.000; TP1 đã nâng từ 75.000 | 79.000; nến trên đó phá cấu trúc giảm | Giả định: fake lên 81.000 rồi về 50.000; không là đường chính |
| [2026-09-15_1008_M1ZThKy2Ylk](codex_phieu/2026-09-15_1008_M1ZThKy2Ylk.json) | GIAM | GIAM | Đứng ngoài vì nhập nhằng | 76.000; TP1 short cũ 77.000 | 82.000; cần vượt để đánh sóng tăng, trên 83.000 rõ hơn | null |
| [2026-09-21_1001_I_U52BYUt0M](codex_phieu/2026-09-21_1001_I_U52BYUt0M.json) | GIAM | GIAM | Chờ quét râu lấy entry | 80.000; chờ quét 82.xxx trước | 83.000; hai D1 trên đó hoặc giữ 1–2 ngày bác giả định phá cao | Giả định quét 84.000–85.000 rồi tụt nhanh; chưa xảy ra |
| [2026-09-28_1006_G5Q1ATx_1ho](codex_phieu/2026-09-28_1006_G5Q1ATx_1ho.json) | GIAM | GIAM | Giữ short có entry đẹp, ăn ngắn | 82.400; TP1 82.600, sát 82.000 chốt dần | null; H1 lấy lại MA200 cần xét lại | null; heatmap 85.000 bị nghi dụ buy, chưa là cú phá cản giả |
| [2026-10-05_1013_5U5CVdTlwT8](codex_phieu/2026-10-05_1013_5U5CVdTlwT8.json) | PHAN_VAN | GIAM | Chờ xác nhận/entry short | 84.000; sau hồi vài trăm giá | 87.000; hai H4 đóng trên đó xác nhận tăng | Giả định quét 88.000 rồi trở dưới 87.000/86.000 |
| [2026-10-15_1005_5iN8iTFsmlY](codex_phieu/2026-10-15_1005_5iN8iTFsmlY.json) | GIAM | GIAM | Chờ hồi lấy entry; tránh long sớm | null; 80.000 → có thể hồi 82.000 → vùng 77.000–76.000 | null; hồi cần H4 rút râu và cây sau xanh | null; fake out nói về altcoin |
| [2026-10-23_1002_cb85mXIfTv8](codex_phieu/2026-10-23_1002_cb85mXIfTv8.json) | GIAM | GIAM | Chờ hồi quét short rồi xét entry | 78.000; vùng 77.000–78.000 | 82.000; D1 lấy lại thì cần xét lại view | Có: đánh giá nhịp lên 84.000 rồi rớt là phá cao |
| [2026-10-29_1005_wcDxLBw0TO4](codex_phieu/2026-10-29_1005_wcDxLBw0TO4.json) | GIAM | GIAM | Chờ hồi lấy entry; sell cũ có thể TP | null; hồi 80.500 → vùng 78.000–77.000 | null; lấy lại cụm ba MA H4 cần xét lại | Có: sau tin lên 81.700 rồi gãy được gọi trap |
| [2026-01-06_aQbHs7J80jc](codex_phieu/2026-01-06_aQbHs7J80jc.json) | TANG | GIAM | Giữ short scalping nhỏ | 95.800 của long chờ 91.000; short hiện tại chỉ khoảng 92.000 | null; không nêu SL số chung | Giả định fake xuống 91.000 dưới demand 92.000–93.000 |
| [2026-01-28_2_a0RdwC1t8](codex_phieu/2026-01-28_2_a0RdwC1t8.json) | TANG | TANG | Chờ entry long có cấu trúc M5 | 93.000; H4 có MA 90.000–91.000 trước | null; H4 dưới MA34 mới xét short, dưới vùng 86.000–85.500 mới confirm gãy | Có: ngày trước dụ short 87.000→86.000 rồi kéo lên |
| [2026-03-06_4Z73-L_oWNY](codex_phieu/2026-03-06_4Z73-L_oWNY.json) | TANG | TANG | Chờ entry long, tránh short hỗ trợ | 75.000; chỉnh 69.000 trước | 68.000 nguy hiểm; thủng tiếp 67.xxx là hết nhịp | null |
| [2026-03-25_byYCWvbkZyU](codex_phieu/2026-03-25_byYCWvbkZyU.json) | TANG | TANG | Chờ long 69.000 hoặc 68.000 có nến | 64.000 sau hồi 76.000/80.000; H4 trước mắt tăng | 67.000; SL lệnh sâu 66.998; long 69.000 riêng có SL 68.000 | null; có mô tả quét hai phe nhưng không gọi rõ fake/trap BTC |
| [2026-04-17_PH5pABMJ01k](codex_phieu/2026-04-17_PH5pABMJ01k.json) | TANG | TANG | Giữ lệnh BTC; lệnh mới chờ chỉnh | 78.000; chỉnh 73.000 trước | null; không tự lấy entry 73.000 làm SL | null |
| [2026-05-19_sWk33q2YCj4](codex_phieu/2026-05-19_sWk33q2YCj4.json) | GIAM | GIAM | Chờ entry, không short FOMO | 70.000 nếu gãy 75.000; trước có thể hồi 78.000–79.000 | null; SL short xổ số ghi 7700 thiếu rõ ràng | Có: ngày xanh trong chuỗi giảm gọi trap; hồi kill short là dự phòng |
| [2026-06-22_eaj9NEm85O4](codex_phieu/2026-06-22_eaj9NEm85O4.json) | TANG | PHAN_VAN | Chờ nến/entry; không mở long mới | 69.000 của nhánh giữ 64.000; cuối chưa chọn đường mới | 64.000; H4 cần giữ trên MA89/Fibo 50 để tăng | Có: H4 xanh test trendline lần hai bị gọi dụ/trap short |

## Những buổi khó gán nhãn

1. **31/7 — GIAM → GIAM, độ chắc thấp.** Phần H4 cụ thể đầu buổi vẫn giảm dưới trendline 65.000; cuối lại nói “BTC không gãy nữa”, ba/bốn cây H4 confirm. Tuy vậy, không có đích H4 tăng mới và vẫn chờ hồi 64.400. Chưa đủ để khẳng định đảo H4; giữ nhãn giảm với ghi chú về dừng giảm/hồi ngắn. Đây là một trong các phiếu nên kiểm chéo trước.
2. **7/8 — TANG → GIAM, độ chắc thấp.** Đầu phần H4 còn đánh giá cross MA và vùng hỗ trợ cho nhịp tăng; cuối gọi H4, D1 đều xấu. Ghi có thay đổi sắc thái, nhưng chính người nói lại bảo “giữ view”. Có thể đó chỉ là nhấn mạnh chặng giảm trước khi long tại 63.xxx, chưa phải đổi toàn bộ view. Không coi đây là một ca đảo hướng chắc chắn.
3. **15/9 — GIAM → GIAM, độ chắc vừa.** Người nói dành nhiều đoạn mô tả H4 dằng co và phải chờ break hai phía, gần PHAN_VAN. Tuy nhiên phần quan điểm cá nhân nói H4 dưới Fibo 0.5 không view lên, khung nhỏ cũng nghiêng giảm. Vì vậy giữ GIAM, đồng thời hành động là đứng ngoài vì nhập nhằng; không đồng nhất hai trường này.
4. **21/9 — GIAM → GIAM, độ chắc thấp.** W1/D1 tăng đẹp, H4 chưa có tuyên bố đảo cấu trúc dứt khoát; người nói lại nghiêng đường quét 82.xxx rồi điều chỉnh/kill long trong tuần. Nhãn GIAM ở đây phản ánh thiên hướng sau quét, không phủ định cấu trúc tăng hiện hữu. Nếu diễn giải “đi đâu tiếp” chỉ là cú quét gần nhất thì có thể đọc thành TANG; cần giữ cả đường đi và trích dẫn để phân xử. Các số 82.xxx bị mất chữ số, không khôi phục tùy ý.
5. **5/10 — PHAN_VAN → GIAM, độ chắc vừa.** Đầu thật sự phân nhánh tại 87.000/84.000 và chờ nến, nói 50/50. Cuối H4 đỏ và H1/H4 xấu làm thiên hướng giảm rõ hơn, dù phải hồi vài trăm giá trước. Ghi thay đổi H4; không coi đó là đã đủ điều kiện mở short market.
6. **6/1 — TANG → GIAM, độ chắc vừa.** Đầu dự kiến H4 quét 96.000–98.000, cuối H4 đỏ khiến ưu tiên điều chỉnh. Nhưng tới cuối vẫn gọi short đang giữ là cản tàu: “GIAM” cuối là thiên hướng chặng điều chỉnh, chưa phải cấu trúc tăng bị phá. Phải tách TP short khoảng 92.000 khỏi vùng chờ long 91.000 và TP long 95.800.
7. **22/6 — TANG → PHAN_VAN, độ chắc thấp.** Đầu rất nghiêng tăng tới 67.000/69.000; cuối bị đạp, yêu cầu chờ H4 và giữ 64.000. Ghi giảm độ tự tin sang chờ xác nhận, chưa có lời tuyên bố đảo view chính thức. Đích 69.000 vẫn thuộc nhánh tăng ban đầu, không phải một đường mới được chọn cuối buổi. Còn dễ lẫn long ETH với long BTC; không suy thành giữ long BTC chỉ từ lời nhắc lệnh long chung. Buổi này nói phiên Mỹ/đêm, không gán mặc định thời điểm cập nhật là 11:00 sáng.
8. **6/3, 16/7, 17/4 — phân biệt H4 với hành động/chặng nhỏ.** 6/3 H4 vẫn được gọi tăng nhưng D1 giảm và nến nhỏ xấu; 16/7 đang short nhỏ ngược H4 tăng; 17/4 cuối nến H4 xấu dễ về 73.000 nhưng vẫn giữ kế hoạch tăng 78.000. Không lấy chờ/short/chỉnh ngắn để tự gán PHAN_VAN hoặc đảo toàn bộ hướng H4. Độ chắc của từng chi tiết được nêu trong JSON.
9. **25/3 — đích cuối khác hướng H4 hiện tại.** H4/D1 hồi tăng, target 76.000 rồi 80.000; sau đó người nói nêu rõ tụt về 64.000. Vì yêu cầu đích chính bằng chặng cuối nên ghi 64.000, không dùng nó để gán H4 giảm ngay. Các nhánh entry 69.000 và 68.000 có SL khác nhau.
10. **14/8, 15/10, 29/10 — đích là vùng, nhánh sâu có điều kiện.** Để `null` cho đích vùng thay vì bịa số. 14/8 có ba chặng test râu→pump kill short→giảm 5x; 15/10 vùng sâu 76.000–77.000; 29/10 ưu tiên 77.000–78.000, muốn 75.000 hoặc thấp hơn phải có hai H4 dưới 77.000. Các con số 75/76 nói thêm sau nến đóng không được dùng để xóa điều kiện ban đầu.
11. **19/5 — H4 giảm nhưng entry hai phía đều phải chờ.** Chờ 75.000 có thể long hồi, hoặc 78.000–79.000 mới xét short; nếu short dày còn có thể quét 83.000. Không ghép “lên 83.000” thành chắc mất xu hướng giảm. SL cuối được chép “7700” nên để số `null`, giữ TP short xổ số 75.600 trong ghi chú.

Các cờ đổi thiên hướng được ghi ở **6/1, 22/6, 7/8 và 5/10**. Trong đó 22/6 và 7/8 có độ chắc thấp, là suy luận từ cách diễn đạt trước/sau diễn biến, không phải bốn lời tuyên bố đổi ý trực tiếp. Các buổi không đổi hướng vẫn có thể đổi TP, nhấn mạnh một chặng, hoặc nhận ra nhịp hồi ngắn.

## Kiểm tra đầu ra

Đã kiểm đủ 23 tên buổi theo danh sách, đủ các trường schema, giá trị enum và kiểu dữ liệu; `dich_chinh` khớp đích chặng cuối. Cả 23 file được kiểm riêng bằng `python 3 -m json.tool`. Không tạo chương trình bot, không đối chiếu phiếu cũ, không sửa dữ liệu transcript.
