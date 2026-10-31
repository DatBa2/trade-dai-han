# Sửa P0 bộ chấm + bộ dựng đề — 31/10/2026

Theo `kiem_cheo/TONG_QUAN_VA_THIEU_SOT_2026-10-31.md` (P0-2, P0-3, P0-4, P1-10, một phần P2). Không đụng `thi/_snapshot_v3_chan_doan/`,
`thi/bai_lam/`, `thi/ho_so/`, `phieu/`, `moc/`, `thi/SO_TAY_T1_T6.md`, `DESIGN.md`, `thi/dap_an_v2/`, `thi/KHOA_CHAM.md`.
Các file mã đã khoá trong `thi/KHOA_CHAM.md` đã sửa → kết quả chấm mới là **phiên bản mới**, không còn là lần thi v3 đã khoá
(bản chẩn đoán vẫn giữ ở `thi/_snapshot_v3_chan_doan/`).

| File | Việc |
|---|---|
| `cong_cu/lay_nen.py` | sửa: tải 1m/5m, nghỉ 0,12 s/lần, `--noi`, `lay_1m()` có cache |
| `cong_cu/dieu_kien.py` | **mới**: điều kiện vô hiệu có cấu trúc + giá đóng theo đúng khung, dùng chung chấm/dựng đề |
| `cong_cu/cham_dich.py` | viết lại `cham()`; thêm `cham_chi_tiet()`; `main()` lấy C = kết thúc live |
| `thi/tao_ho_so.py` | `trang_thai_moc` theo đúng khung; `--phieu`, `--ra` (mặc định `thi/ho_so_v2`, chặn ghi `thi/ho_so`) |
| `thi/cham.py` | `--phieu`; dùng `cham_chi_tiet`; 2 hạn; CHƯA RÕ THỨ TỰ; đúng đường đi; P1-10 (đối xứng thật, bootstrap khối, mẫu số) |
| `thi/kiem_thu_cham.py` | **mới**: 8 phép thử offline |
| `thi/hoi_quy_cham_dich.py` | **mới**: so cham_dich cũ (snapshot, chỉ đọc) với mới |
| `du_lieu/btc_5m.csv` | **mới**: 87.305 nến 5m OKX BTC-USDT, 2026-01-01 00:00 → 2026-10-31 03:20 UTC, 0 lỗ hổng |
| `du_lieu/btc_1m_cache.csv` | **mới**: cache 1m (hiện 5 nến, 1 lần phân thứ tự) |
| `thi/ho_so_v2/` | **mới**: 77 hồ sơ dựng lại |

## Kiểm chứng tổng
- `python3 thi/kiem_thu_cham.py` → **8/8 PASS** (chặn mạng, thay mảng nến trong bộ nhớ). Thêm phép thử đột biến (chạy ngoài repo):
  cài lại từng hành vi CŨ vào bộ nhớ → **8/8 phép thử FAIL đúng chỗ** (nến mở ≥ C; luôn H4; luôn 1 nến; cùng nến = ĐÚNG; giá nến chứa C;
  mốc D1 xét H4; nới biên theo chặng 1; đường đi = đích cuối) → bộ thử thật sự bắt được các lỗi cũ.
- `python3 thi/tao_ho_so.py --kiem` → 77 hồ sơ vào `thi/ho_so_v2/`, phép thử cắt tương lai **77/77 GIỐNG HỆT**, 0 dòng RÒ RỈ.
- `python3 thi/hoi_quy_cham_dich.py` (180 phiếu) và `... thi/bai_lam --bai-lam` (77 bài bot): bảng ở mục G.
- `python3 thi/cham.py --ra <scratch>` chạy được (1,4 s); không ghi `thi/KET_QUA_THI.md`.

## A. Dữ liệu nến nhỏ
- `cong_cu/lay_nen.py:18–44` (`goi`, `tai`): history-candles OKX công khai, header User-Agent, nghỉ `NGHI = 0.12` s, chỉ nến `confirm=1`,
  thử lại 4 lần. `--noi` chỉ tải phần mới hơn file (`:88–97`).
- `lay_1m(tu, den)` (`:66–85`): đọc `du_lieu/btc_1m_cache.csv`; thiếu thì tải đúng khoảng đó rồi ghi thêm; không tải nến chưa đóng.

## P0-2. Giá tham chiếu nhìn tới close sau C
- **Lỗi:** `bisect_left` trên giờ MỞ H1 rồi lấy close nến trước đó = close của nến H1 CHỨA C (chưa tồn tại tại C), và bỏ diễn biến tới hết giờ đó.
- **Sửa:** `cong_cu/cham_dich.py:98–105` `gia_tham_chieu(C)` = close của nến 5m cuối có **giờ đóng ≤ C** (cách C quá 1 giờ → CHUA_DU_LIEU);
  quét diễn biến từ nến 5m có **giờ mở ≥ C** (`:135`, `:163–176`). Nến 5m chứa C bị bỏ → khoảng trống < 5 phút sau C không chấm
  (ghi trong docstring `:9–12`). `thi/cham.py` không còn `gia_luc`/`tach_view` theo H1; phép đối xứng dùng cùng giá tham chiếu và 5m.
- **Kiểm:** `kt5_gia_tham_chieu_va_nen_chua_C` PASS (C = 10:32: giá = close nến 10:25–10:30; râu 58.000 của nến 10:30–10:35 không làm ĐÚNG;
  C = 10:30 đúng biên thì nến 10:30 được tính). Hồi quy: ví dụ 2026-03-12 ở mục G.

## P0-3. Điều kiện vô hiệu rút thành 1 cây H4 + bỏ nến đóng đầu tiên sau C (chấm và đề)
- **Lỗi:** chấm chỉ so close H4 và đòi giờ MỞ H4 ≥ C (`_snapshot.../cham_dich.py:97`); “2 nến”, “D1/W1 đóng” đều thành 1 close H4.
  Đề: `trang_thai_moc` dùng min/max close H4 cho mốc D1/W1.
- **Sửa (module chung `cong_cu/dieu_kien.py`):**
  - `phan_tich(cau, huong, nguong)` `:83–107` → `{gia, khung H4|D1|W1, so_nen 1|2, chieu dong_tren|dong_duoi, da_hieu}` hoặc None.
    Khung nhỏ (M5/M15/M30/H1/“5 phút”/scalp) → None như cũ (`:27`). Khung đọc trong đoạn (tách `;`) chứa số được chọn (`_khung_doan` `:57–80`):
    “confirm/xác nhận bằng D1/W1” → khung đó; không thì từ khoá khung gần nhất đứng trước số (nhóm “H4 hoặc D1”, “H4/D1” → khung nhỏ hơn);
    không có thì từ khoá ngay sau số (≤ 25 ký tự, không qua dấu ngoặc); mặc định H4. Số nến: “2/hai cây|nến|H4|D1|W1” → 2, trừ “1-2 cây”,
    “một đến hai cây” → 1 (`:32–33`). Giá: số phía bất lợi gần giá nhất như cũ; bỏ số dính chữ phía trước (MA200, EMA34).
    `so_trong_vt` `:38–49` đổi thứ tự nhánh regex để “81,5K”/“76.5” đọc đúng 81.500/76.500 (bản cũ đọc thành 81.000/76.000).
  - `lan_kich_hoat(dk, C, den, nens=None)` `:173–197`: giờ ĐÓNG nến đầu tiên làm điều kiện đúng, chỉ nến có C < giờ đóng ≤ den
    (nến mở trước C đóng sau C ĐƯỢC tính); so_nen=2 = 2 nến liền nhau cùng khung đều đóng qua. H4 = `btc_4H_bo_sung` + `btc_4H`,
    D1 = `btc_1Dutc_bo_sung` + `btc_1Dutc`, W1 dựng từ D1 (thứ Hai 00:00 UTC, đủ 7 ngày) `:134–141`.
  - `khung_cua_moc`, `trang_thai_dong` `:200–217`: trạng thái mốc trong đề — D1/W1/tháng xét close của chính khung đó, không suy từ H4.
- **Chấm:** `cong_cu/cham_dich.py:148–151` dùng `phan_tich`; `:178` `lan_kich_hoat`; `quyet()` `:227–244`: vô hiệu tính tại giờ ĐÓNG nến khung,
  chạm đích/SL tại giờ MỞ nến 5m; vô hiệu đóng ≤ giờ mở nến 5m chạm đích → SAI. Có câu mà không tách được mốc → cờ `vo_hieu_chua_hieu`
  (không khẳng định đã vô hiệu; 180 phiếu: 18 câu).
- **Đề:** `thi/tao_ho_so.py:580–612` `trang_thai_moc(m, nen, tu, T, ...)`: chạm/tới = râu H4 (như cũ); phá/kích hoạt = close đúng khung của
  mốc, chỉ nến đã đóng trong (lúc nói, T] lấy từ lớp `Cat` (đã cắt tại C) `:620`. Tiêu đề bảng mốc ghi rõ cách tính (`:621–624`).
- **Kiểm:** `kt1_h4_mo_truoc_C_dong_sau_C`, `kt2_moc_D1`, `kt3_hai_nen_H4`, `kt6_trang_thai_moc_D1_trong_de` đều PASS.
- **Hồ sơ v2 so với `thi/ho_so/`** (77/77 khác vì tiêu đề bảng mốc đổi chữ, 6 dòng/hồ sơ):
  - **47 hồ sơ đổi CHỮ trạng thái mốc, 96 dòng**: `ĐÃ KÍCH HOẠT → chưa kích hoạt` 19 dòng ở **19 hồ sơ** (mốc vô hiệu D1/W1 —
    khớp con số 19 của Codex, gồm ví dụ 9/7 mốc D1 62.000 bị gắn kích hoạt bởi close H4 61.699); `ĐÃ PHÁ → giữ, đã test` 71;
    `ĐÃ PHÁ → giữ, chưa test` 6. 44 hồ sơ có mốc D1/W1 đổi; 3 hồ sơ chỉ đổi mốc tháng (MN). Chiều đổi chỉ có “đã → chưa” (close D1/W1/tháng
    là tập con của close H4). Danh sách đầy đủ ở Phụ lục.
  - 242 dòng chỉ đổi nhãn trong ngoặc, cùng trạng thái (“đóng H4 cao nhất X” → “đóng D1/W1 … Y”): D1 208, W1 34.
  - 21 dòng metadata ở 6 hồ sơ 1, 2, 3, 6, 7, 9/7: giờ live buổi tháng 6 nay đã có trong `transcripts/gio_live.tsv`
    (“10:00 · giờ không chắc” → giờ thật) — không do sửa P0, đúng 6 ca Codex nêu ở P1-11.

## P0-4. TP và SL cùng nến luôn tính ĐÚNG
- **Sửa:** `cong_cu/cham_dich.py:67–86` `lay_1m`, `thu_tu_1m`: đích + SL cùng nến 5m → tải 5 nến 1m của đúng 5 phút đó; cùng nến 1m,
  thiếu 1m hoặc 1m lệch 5m → `CHUA_RO_THU_TU` (`:242–244`). Không nhánh nào mặc định ĐÚNG. Cùng logic cho cặp đích cuối/SL của đường đi
  (`:258–262`) và cho phép đối xứng (`thi/cham.py:98–121`).
- **Đường đi ≥ 2 chặng** (`:186–220`, `quyet_dd` `:246–265`): kết quả chính giữ cách cũ (đích cuối + `nguong`); thêm `ket_qua_duong_di`:
  ĐÚNG khi chạm lần lượt đích từng chặng (chặng 1 trước) rồi mới tới đích cuối, trước SL/vô hiệu; tới đích cuối khi chưa qua chặng trước
  → `SAI_THU_TU`; 2 chặng chạm cùng nến 5m → 1m, không phân được → `CHUA_RO_THU_TU`.
- **Hạn:** `cham_chi_tiet` trả `han_co_dinh` (HAN_CO_DINH, mặc định 336 giờ) và `han_view` (han_gio của view, trần 336, không có thì 168),
  mỗi cái có `ket_qua/luc/su_kien/duong_di`; chưa có sự kiện mà dữ liệu chưa phủ hết hạn → `CHUA_HET_HAN`. `cham()` giữ chữ ký và hành vi
  cũ (có biến HAN_CO_DINH → hạn cố định, không thì hạn view).
- **Kiểm:** `kt4_dich_sl_cung_nen_5m` (1m: đích trước → ĐÚNG; SL trước → SAI; cùng nến 1m → CHUA_RO_THU_TU; thiếu 1m → CHUA_RO_THU_TU) và
  `kt8_duong_di_hai_chang` (đi thẳng tới đích cuối: kết quả chính ĐÚNG, đường đi SAI_THU_TU; hồi chặng 1 trước → đường đi ĐÚNG) PASS.
- **Trên dữ liệu thật:** 0 ca đích+SL cùng nến 5m trong 180 phiếu và trong 77 buổi thi (bot, người đó, 2 mốc so sánh) → lỗi P0-4 không làm
  đổi số hiện tại; 1 ca phép đối xứng cùng nến 5m (26/8 04:15 UTC, mốc Chép/Giữ view) được 1m phân: đích trước.

## P2 (làm kèm). `cham_dich.main()` lấy C = kết thúc live
- `cong_cu/cham_dich.py:286–306` `gio_live()`, `moc_C()`: có giờ live thật → C = bắt đầu + số phút; không thì HHMM trong tên/10:00 VN như cũ.
  Hiện 180/180 phiếu có giờ thật (gio_live.tsv được cập nhật lúc 10:35 bởi tiến trình khác).

## P1-10. Thống kê và mẫu số (thi/cham.py)
1. **Đối xứng thật** `thi/cham.py:98–121`: biên phía kia = giá tham chiếu ± đúng khoảng tới đích, bỏ hẳn phần nới theo chặng 1.
   Phép thử chính chỉ gồm view KHÔNG có chặng cố ý đi ngược (1 chặng hoặc mọi chặng cùng hướng); view có chặng đi ngược báo bảng riêng,
   ghi rõ không so với tung đồng xu (`:375–389`, cờ `di_nguoc` ở `cham_dich.py:118–119`). Lý do tách theo “đi ngược” thay vì “≥ 2 chặng”:
   55/62 view có hướng của bot có chặng 1 ngược hướng; mọi chặng cùng hướng không làm lệch phép thử. Kết quả mới: phép thử chính bot 2/5,
   người đó 9/18 (bảng cũ gộp: bot 24/58, người 19/49). **Kiểm:** `kt7_doi_xung_that` PASS.
2. **Bootstrap khối tuần ISO** `:140–157`: rút lại cả tuần (18 khối trên 76 buổi), 2.000 lần, KTC 95% cho % trùng và cho **chênh lệch cặp**
   bot − từng mốc trong cùng lần rút (`:269`, cột mới ở bảng 1). Kết quả trên bài v3: bot − Luôn GIẢM −1 điểm % (−17…+16), − Chép buổi trước
   +5 (−4…+14), − Giữ view +1 (−9…+11), − Luật từ trên xuống −1 (−14…+12) → **không chênh lệch nào khác 0**. KTC riêng của bot rộng ra
   46–68% → 42–70%.
3. **Mẫu số** `:249–261`: mọi buổi thi có nhãn người đó hợp lệ (76/77; loại 27/8 vì phiếu không có view H4/chung); bot thiếu bài hoặc nhãn không
   hợp lệ = SAI, không loại; dòng “Độ phủ bot” báo riêng (76/76 có bài, 76/76 nhãn hợp lệ). Bảng chéo thêm cột “Thiếu/không hợp lệ”.
- Không có phép thử tự động riêng cho (2)–(3); đã kiểm bằng chạy thật: có `--phieu` sửa 1 nhãn (buổi 1/7 GIẢM→TĂNG) trong bản sao ở scratch
  → phân bố nhãn người đó, độ chính xác các bên và hồ sơ 2/7 (phiếu buổi liền trước) đổi đúng 1 chỗ.

## E/D. Tham số thư mục
- `thi/cham.py --phieu DIR`: danh sách buổi, nhãn người đó, Chép buổi trước, Giữ view đều đọc từ DIR (`hs.ds_buoi(DIR)`).
- `thi/tao_ho_so.py --phieu DIR` (`:193–229`), `--ra DIR` mặc định `thi/ho_so_v2` (`:37`, `:704–708`); `--ra thi/ho_so` bị chặn
  (“✗ không ghi vào thi/ho_so/”), đã thử.

## G. Hồi quy cham_dich cũ → mới
`python3 thi/hoi_quy_cham_dich.py` — mã cũ nạp từ `thi/_snapshot_v3_chan_doan/cham_dich.py` (exec, không sửa file), cả hai chạy trên
cùng dữ liệu `du_lieu/` hiện tại.

**180 phiếu `phieu/`**

| Phép so | Đổi | Chuyển |
|---|---|---|
| 1. Toàn bộ: C cũ (tên/10:00) + bộ cũ → C kết thúc live + bộ mới, hạn view | 4 | DICH_SAI_PHIA→DUNG 1 · DUNG→SAI 1 · SAI_HET_HAN→DUNG 1 · CHUA_RO→SAI 1 |
| 2. Chỉ do bộ chấm (cùng C cũ, hạn view) | 1 | CHUA_RO→SAI 1 |
| 3. Thước bài thi (cùng C mới, 336 giờ) | 4 | DICH_SAI_PHIA→DUNG 1 · SAI→DUNG 1 · CHUA_RO→CHUA_HET_HAN 1 · SAI_HET_HAN→CHUA_HET_HAN 1 |

Phân bố (hạn view) cũ → mới: DUNG 47→48 · SAI 31→33 · CHUA_RO 37→36 · SAI_HET_HAN 25→24 · DICH_SAI_PHIA 7→6 · KHONG_DICH 9 · PHAN_VAN 24.
Điều kiện vô hiệu hiểu được: H4 71, D1 7, W1 1; 2 nến: 1.

**77 bài làm bot `thi/bai_lam/`** (`--bai-lam`, chuẩn hoá như lúc chấm thi): **0 đổi** ở cả 3 phép so (bot: H4 61, D1 1, 2 nến 3).
Bảng thị trường 14 ngày của bot giữ nguyên 20 ĐÚNG / 42 SAI / 1 CHƯA RÕ như `KET_QUA_CHAM_CU.md`; chỉ “Chép view buổi trước” đổi
20→21 ĐÚNG, 7→6 đích sai phía (do giá tham chiếu mới).

**Ví dụ có giải thích**
1. `2026-06-22_eaj9NEm85O4` (phép 2: CHUA_RO → SAI, cùng C cũ 22/6 10:00 VN = 03:00 UTC) — TĂNG, mốc “H4 đóng dưới … 64.000”. Nến H4
   00:00–04:00 UTC mở trước C, đóng 04:00 ở 63.970,7 < 64.000. Bản cũ đòi giờ mở ≥ C nên bỏ nến này → CHUA_RO trong hạn 24 giờ; bản mới
   SAI lúc 22/6 11:00 VN. Đúng lỗi dòng 97 (P0-3).
2. `2026-04-24_ZTOmNH9I_wM` (phép 3: SAI → DUNG) — GIẢM, đích 75.000, câu “D1 đóng vượt 79.000 thì lực lên rất tốt”. Bản cũ coi là close
   H4 > 79.000 → SAI 27/4 10:00; bản mới đọc khung D1, không có close D1 > 79.000 trước khi giá chạm 75.000 lúc 30/4 01:05 → ĐÚNG (P0-3 khung).
3. `2026-03-12_qJZk9q5A7rA` (phép 3: DICH_SAI_PHIA → DUNG, C 04:13 UTC) — GIẢM, đích 69.400. Bản cũ lấy close H1 04:00–05:00 (biết lúc
   05:00, sau C) = 69.363,8 < đích → “đích sai phía”; bản mới lấy close 5m đã đóng 04:10 = 69.645 → đích hợp lệ, chạm lúc 11:35 VN (P0-2).
4. `2026-10-22_1009_yAEJBNZ56qs` (phép 3: CHUA_RO → CHUA_HET_HAN) — C 22/10, hạn 336 giờ kéo tới 5/11 nhưng 5m chỉ tới 31/10. Bản cũ
   coi như đã hết hạn; bản mới báo chưa hết hạn (tương tự 23/10: SAI_HET_HAN → CHUA_HET_HAN).
5. `2026-04-27_9oEDyu-IfMM` (phép 1: DUNG → SAI; phép 2 không đổi) — đổi do C: live thật 22:xx, kết thúc 23:04 VN chứ không phải 10:00.
   Giá lúc C 76.790 (thay vì 79.120 lúc 10:00); mốc “H4 đóng trên 77.000” bị close H4 lúc 28/4 07:00 VN chạm trước khi tới đích 76.300
   (18:00) → SAI. Ca này là hệ quả P2 (C thật), không phải lỗi bộ chấm.
6. `2026-05-06_ZEZOrGhyb6I` (phép 1: SAI_HET_HAN → DUNG) — cũng do C: kết thúc live 23:12 thay vì 10:00, cửa sổ 24 giờ dời theo nên
   kịp chạm đích 80.000 lúc 7/5 22:15.

Nhận xét: trên dữ liệu hiện có, các lỗi P0-2/3/4 có thật (8 phép thử + đột biến) nhưng hiếm khi lật kết quả của 180 phiếu (1 ca do bộ
chấm ở hạn view, 4 ca ở thước 336 giờ) và **không lật kết quả thị trường nào của 77 bài bot**. Thay đổi lớn nhất của báo cáo thi đến từ
P1-10 (phép đối xứng tách “đi ngược”, KTC rộng hơn, chênh lệch cặp) và từ đề: **bot v3 đã làm bài trên `thi/ho_so/` cũ** — 19 hồ sơ có mốc
vô hiệu D1/W1 bị báo “ĐÃ KÍCH HOẠT” sai, 47 hồ sơ có ít nhất 1 trạng thái mốc sai.

## Chưa làm được / còn vướng
- **Bài làm v3 chưa được sinh lại trên `thi/ho_so_v2/`**; độ chính xác hướng 43/76 hiện vẫn là kết quả trên đề có trạng thái mốc sai.
- Câu vô hiệu nhắc khung nhỏ ở BẤT KỲ đâu → None theo đúng yêu cầu “như code cũ”; điều này bỏ mất điều kiện H4/D1 hợp lệ trong câu hỗn hợp
  ở **11 phiếu** (13/1, 4/3, 10/3, 6/4, 8/4, 14/4, 10/6, 15/6, 3/7, 4/8, 21/8; vd 8/4 “H4 đóng dưới 68.000 …; scalping SL dưới 71.000”).
  Nên lọc khung nhỏ theo từng đoạn `;` — chưa làm vì trái yêu cầu.
- Đọc khung/số nến từ câu tự do là luật tay; câu mơ hồ (“H4 hoặc D1 …”, “confirm bằng D1”, “nến ngày xanh đóng cửa … test 100.000”) chưa đối
  chiếu video. 18/180 phiếu có câu vô hiệu không tách được mốc (cờ `vo_hieu_chua_hieu`). Vùng mốc sai (“77.000–77.700”) vẫn lấy số gần giá nhất.
- Trạng thái mốc trong đề: chưa đọc “2 nến” từ `trich` của mốc (luôn 1 nến); mốc `3M` (1 mốc) dùng tạm nến tháng; mốc khung H1/M5 vẫn xét H4.
- Khoảng < 5 phút ngay sau C không được chấm (đã ghi rõ); thiếu 1m → CHUA_RO_THU_TU thay vì đoán.
- Đường đi: 2 chặng chạm cùng nến 5m chỉ được tính khi 1m xác nhận đúng thứ tự; chặng giữa của đường 3 chặng xét bảo thủ (chặng sau từ nến kế);
  chặng thiếu hướng/số → không có `ket_qua_duong_di`.
- (2)–(3) của P1-10 kiểm bằng chạy thật, chưa có phép thử tự động riêng.
- `thi/cham.py` vẫn mặc định ghi `thi/KET_QUA_THI.md` khi không có `--ra` (giữ như cũ, file đó hiện không tồn tại); nếu muốn tránh ghi đè
  nhầm kết quả khoá, có thể đổi mặc định — chưa đổi vì ngoài yêu cầu.
- `thi/KHOA_CHAM.md` chưa được cập nhật hash mới (thư mục khoá, không được sửa).

## Phụ lục — hồ sơ `thi/ho_so_v2/` đổi chữ trạng thái mốc so với `thi/ho_so/` (số dòng theo `thi/ho_so/`)
Hồ sơ đổi trạng thái: 47 · dòng: 96 · {'ĐÃ PHÁ → giữ, đã test': 71, 'ĐÃ KÍCH HOẠT → chưa kích hoạt': 19, 'ĐÃ PHÁ → giữ, chưa test': 6} · chỉ đổi nhãn khung: {'D1': 208, 'W1': 34}

- `2026-07-02_w4bvsDte3bI`: dòng 404 mốc 59.000–60.000 (hỗ trợ (?), MN): ĐÃ PHÁ (đóng H4 thấp nhất 58.618) → giữ, đã test; dòng 427 mốc 61.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 61.066) → giữ, đã test
- `2026-07-03_IV0Mlz8kNPI`: dòng 396 mốc 59.000–60.000 (hỗ trợ (?), MN): ĐÃ PHÁ (đóng H4 thấp nhất 58.618) → giữ, đã test
- `2026-07-06_GRWl0b0z1nk`: dòng 427 mốc 59.000–60.000 (hỗ trợ (?), MN): ĐÃ PHÁ (đóng H4 thấp nhất 58.618) → giữ, đã test
- `2026-07-07_uvBnzq6-k-M`: dòng 468 mốc 59.000–60.000 (hỗ trợ (?), MN): ĐÃ PHÁ (đóng H4 thấp nhất 58.618) → giữ, đã test
- `2026-07-09_Fmb8AziZ6f4`: dòng 391 mốc 62.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 thấp nhất 61.699) → chưa kích hoạt; dòng 482 mốc 59.000–60.000 (hỗ trợ (?), MN): ĐÃ PHÁ (đóng H4 thấp nhất 58.618) → giữ, đã test
- `2026-07-10_QwYznPgaAFY`: dòng 422 mốc 62.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 thấp nhất 61.699) → chưa kích hoạt; dòng 512 mốc 59.000–60.000 (hỗ trợ (?), MN): ĐÃ PHÁ (đóng H4 thấp nhất 58.618) → giữ, đã test
- `2026-07-13_O3q2fmXlwhk`: dòng 456 mốc 62.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 thấp nhất 61.699) → chưa kích hoạt
- `2026-07-14_gpyn9kVPpn4`: dòng 520 mốc 62.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 thấp nhất 61.699) → chưa kích hoạt
- `2026-07-15_-T8Wu5b89B4`: dòng 533 mốc 62.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 thấp nhất 61.699) → chưa kích hoạt
- `2026-07-16_bwgz_kMSvfE`: dòng 509 mốc 62.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 thấp nhất 61.699) → chưa kích hoạt
- `2026-07-23_IsyMSPIscsc`: dòng 368 mốc 50.000 (đỉnh cũ, W1): ĐÃ PHÁ (đóng H4 cao nhất 66.219) → giữ, chưa test
- `2026-07-24_7D1Ve5hs4bU`: dòng 402 mốc 50.000 (đỉnh cũ, W1): ĐÃ PHÁ (đóng H4 cao nhất 66.219) → giữ, chưa test
- `2026-08-10_1001_8BGhoFetSaU`: dòng 384 mốc 65.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test; dòng 397 mốc 64.700–65.000 (kháng cự (?), D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test; dòng 410 mốc 65.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 65.230) → chưa kích hoạt
- `2026-08-11_1005_KvVvliql8xI`: dòng 390 mốc 65.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test; dòng 402 mốc 64.700–65.000 (kháng cự (?), D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test; dòng 415 mốc 65.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 65.230) → chưa kích hoạt
- `2026-08-12_1003_EaWaSL7aWT4`: dòng 400 mốc 65.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test; dòng 412 mốc 64.700–65.000 (kháng cự (?), D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test; dòng 425 mốc 65.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 65.230) → chưa kích hoạt
- `2026-08-13_1006_hNxSX7GUKMs`: dòng 438 mốc 65.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test; dòng 450 mốc 64.700–65.000 (kháng cự (?), D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test; dòng 463 mốc 65.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 65.230) → chưa kích hoạt
- `2026-08-14_1004_xK38gQ-G6uA`: dòng 441 mốc 65.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test; dòng 453 mốc 64.700–65.000 (kháng cự (?), D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test
- `2026-08-17_1006_tmR0aXnjOlA`: dòng 468 mốc 65.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 65.230) → giữ, đã test
- `2026-08-21_1003_oDD5qwLcZbw`: dòng 383 mốc 73.000 (vô hiệu, W1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 74.518) → chưa kích hoạt; dòng 451 mốc 68.000–71.000 (kháng cự, W1): ĐÃ PHÁ (đóng H4 cao nhất 74.518) → giữ, đã test
- `2026-09-08_1002_gOwbzU0t2S0`: dòng 351 mốc 79.000 (hỗ trợ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 78.834) → giữ, đã test
- `2026-09-16_1008_31jXsidP5KE`: dòng 390 mốc 77.500 (hỗ trợ (?), W1): ĐÃ PHÁ (đóng H4 thấp nhất 75.641) → giữ, đã test
- `2026-09-17_0026_7mETSY5t5Yg`: dòng 397 mốc 76.000 (hỗ trợ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 75.775) → giữ, đã test; dòng 444 mốc 77.500 (hỗ trợ (?), W1): ĐÃ PHÁ (đóng H4 thấp nhất 75.641) → giữ, đã test
- `2026-09-17_1002_1cUPKUmEnr4`: dòng 440 mốc 76.000 (hỗ trợ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 75.775) → giữ, đã test; dòng 486 mốc 77.500 (hỗ trợ (?), W1): ĐÃ PHÁ (đóng H4 thấp nhất 75.641) → giữ, đã test
- `2026-09-18_1003_YPMgjMxL2io`: dòng 407 mốc 76.000 (hỗ trợ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 75.775) → giữ, đã test; dòng 453 mốc 77.500 (hỗ trợ (?), W1): ĐÃ PHÁ (đóng H4 thấp nhất 75.641) → giữ, đã test
- `2026-09-21_1001_I_U52BYUt0M`: dòng 447 mốc 76.000 (hỗ trợ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 75.775) → giữ, đã test; dòng 493 mốc 77.500 (hỗ trợ (?), W1): ĐÃ PHÁ (đóng H4 thấp nhất 75.641) → giữ, đã test
- `2026-09-22_1003_N-_6NBs4ZW8`: dòng 355 mốc 83.000 (kháng cự, W1): ĐÃ PHÁ (đóng H4 cao nhất 86.618) → giữ, đã test; dòng 374 mốc 82.000 (đỉnh cũ (?), W1): ĐÃ PHÁ (đóng H4 cao nhất 86.618) → giữ, đã test; dòng 454 mốc 76.000 (hỗ trợ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 75.775) → giữ, đã test
- `2026-09-23_1007_uK4vb9PoUIo`: dòng 393 mốc 83.000 (kháng cự, W1): ĐÃ PHÁ (đóng H4 cao nhất 86.711) → giữ, đã test; dòng 412 mốc 82.000 (đỉnh cũ (?), W1): ĐÃ PHÁ (đóng H4 cao nhất 86.711) → giữ, đã test; dòng 491 mốc 76.000 (hỗ trợ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 75.775) → giữ, đã test
- `2026-09-24_1009_R_WfFHUJ5RI`: dòng 371 mốc 83.000 (kháng cự, W1): ĐÃ PHÁ (đóng H4 cao nhất 86.711) → giữ, đã test; dòng 390 mốc 82.000 (đỉnh cũ (?), W1): ĐÃ PHÁ (đóng H4 cao nhất 86.711) → giữ, đã test
- `2026-09-25_1014_Wf7PeLs6l94`: dòng 447 mốc 83.000 (kháng cự, W1): ĐÃ PHÁ (đóng H4 cao nhất 86.711) → giữ, đã test; dòng 466 mốc 82.000 (đỉnh cũ (?), W1): ĐÃ PHÁ (đóng H4 cao nhất 86.711) → giữ, đã test
- `2026-09-29_1002_3inGNRqb-UM`: dòng 386 mốc 75.000 (đỉnh cũ, W1): ĐÃ PHÁ (đóng H4 cao nhất 83.500) → giữ, chưa test
- `2026-09-30_1003_3qAxAK71YAs`: dòng 379 mốc 75.000 (đỉnh cũ, W1): ĐÃ PHÁ (đóng H4 cao nhất 84.351) → giữ, chưa test
- `2026-10-01_1005_56fLd04MSps`: dòng 437 mốc 75.000 (đỉnh cũ, W1): ĐÃ PHÁ (đóng H4 cao nhất 84.351) → giữ, chưa test
- `2026-10-02_1001_AxRfx12h9Z0`: dòng 477 mốc 75.000 (đỉnh cũ, W1): ĐÃ PHÁ (đóng H4 cao nhất 85.507) → giữ, chưa test
- `2026-10-13_1005_4ttwL_4CC9E`: dòng 501 mốc 82.000–83.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 81.031) → giữ, đã test
- `2026-10-14_1009_BlA26qxNBTE`: dòng 361 mốc 82.000 (vô hiệu, W1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 83.858) → chưa kích hoạt
- `2026-10-15_1005_5iN8iTFsmlY`: dòng 350 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.920) → giữ, đã test; dòng 374 mốc 81.000–82.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 80.920) → giữ, đã test; dòng 374 mốc 82.000 (vô hiệu, W1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 83.858) → chưa kích hoạt; dòng 393 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.920) → giữ, đã test
- `2026-10-16_1007_lSGpwulXi5s`: dòng 372 mốc 81.000 (đáy cũ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.920) → giữ, đã test; dòng 398 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.920) → giữ, đã test; dòng 421 mốc 81.000–82.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 80.920) → giữ, đã test; dòng 421 mốc 82.000 (vô hiệu, W1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 83.858) → chưa kích hoạt; dòng 440 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.920) → giữ, đã test
- `2026-10-19_1001_-avZ2E3n2oE`: dòng 379 mốc 81.000 (đáy cũ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 404 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 427 mốc 81.000–82.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 446 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test
- `2026-10-20_1017_zzhCJ1Bb_vg`: dòng 428 mốc 81.000 (đáy cũ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 453 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 476 mốc 81.000–82.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 495 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test
- `2026-10-22_1009_yAEJBNZ56qs`: dòng 424 mốc 81.000 (đáy cũ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 426 mốc 84.000–85.000 (vô hiệu, W1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 84.540) → chưa kích hoạt; dòng 449 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 472 mốc 81.000–82.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 491 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test
- `2026-10-23_1002_cb85mXIfTv8`: dòng 441 mốc 81.000 (đáy cũ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test; dòng 443 mốc 84.000–85.000 (vô hiệu, W1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 84.540) → chưa kích hoạt; dòng 466 mốc 81.000–83.000 (hỗ trợ (?), D1): ĐÃ PHÁ (đóng H4 thấp nhất 80.877) → giữ, đã test
- `2026-10-26_1002_52C5f7Gf1NE`: dòng 437 mốc 80.000 (hỗ trợ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 79.600) → giữ, đã test; dòng 459 mốc 84.000–85.000 (vô hiệu, W1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 84.540) → chưa kích hoạt
- `2026-10-27_1002_2RB3G-MYjhE`: dòng 402 mốc 80.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 79.600) → giữ, đã test; dòng 500 mốc 80.000 (hỗ trợ, D1): ĐÃ PHÁ (đóng H4 thấp nhất 79.600) → giữ, đã test
- `2026-10-28_1006_Gu1XtyNNH6I`: dòng 371 mốc 80.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 79.600) → giữ, đã test; dòng 376 mốc 81.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 81.145) → giữ, đã test
- `2026-10-29_0033_4Hg5YedKaAg`: dòng 367 mốc 81.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 81.329) → giữ, đã test; dòng 404 mốc 80.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 79.600) → giữ, đã test; dòng 409 mốc 81.000 (kháng cự, D1): ĐÃ PHÁ (đóng H4 cao nhất 81.329) → giữ, đã test
- `2026-10-29_1005_wcDxLBw0TO4`: dòng 416 mốc 81.500–82.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 81.577) → chưa kích hoạt; dòng 449 mốc 80.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 79.600) → giữ, đã test
- `2026-10-30_0955_f0JWA9aDHl8`: dòng 438 mốc 81.500–82.000 (vô hiệu, D1): ĐÃ KÍCH HOẠT (đóng H4 cao nhất 81.776) → chưa kích hoạt; dòng 471 mốc 80.000 (hỗ trợ, W1): ĐÃ PHÁ (đóng H4 thấp nhất 78.007) → giữ, đã test

## Bổ sung khi nghiệm thu (Claude, 31/10 ~10:55)
- `cong_cu/dieu_kien.py::phan_tich`: trước đây câu vô hiệu có nhắc khung nhỏ (M5/H1/scalp) bị bỏ CẢ CÂU → mất vế H4/D1 hợp lệ
  (11 phiếu). Nay chỉ bỏ ĐOẠN (tách `;`) nói khung nhỏ. Kiểm: `"H4 đóng dưới 68.000 …; scalping SL dưới 71.000"` → H4 68.000;
  `"2 cây H4 đóng trên 82.000; SL scalp M15 trên 81.200"` → H4 82.000, 2 nến; `"SL M15 trên 81.200"` → None. Kiểm thử vẫn 8/8 PASS.
  Sửa TRƯỚC khi chạy chấm chính thức theo đáp án v2; áp như nhau cho bot, người đó và mọi mốc so sánh.
