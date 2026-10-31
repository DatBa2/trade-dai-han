# Nhờ Codex KIỂM ĐỘC LẬP bot v4 (31/10/2026)

Bot v4 = luật máy bắt chước cách người đó ra quyết định (BTC + rổ 6 tài sản), thiết kế khoá ở `bot_v4/THIET_KE.md`.
Code do subagent Claude viết; Claude cũng viết bộ báo cáo. **Bạn là người kiểm độc lập**: mục tiêu là tìm chỗ sai,
chỗ rò rỉ tương lai, chỗ code lệch thiết kế, chỗ sửa luật theo kết quả — không phải xác nhận cho đẹp.

## Quy tắc
- **CHỈ ĐƯỢC GHI**: `kiem_cheo/CODEX_KIEM_V4.md` (kết luận), thư mục nháp `kiem_cheo/codex_v4/` (backtest độc lập, log),
  và bản sao `bot_v4_codex/` (cùng cấp với `bot_v4/`, để chạy lại mà không ghi đè số gốc). **KHÔNG sửa/xoá/ghi đè bất kỳ
  file nào trong `bot_v4/`, `cong_cu/`, `thi/`, `phieu/`, `transcripts/`.** Không chạy `python3 bot_v4/tai_du_lieu.py`,
  `bot_v4/chay.py`, `bot_v4/bao_cao.py` trên thư mục gốc (chúng ghi đè `bot_v4/du_lieu/`, `bot_v4/ket_qua/`, `KET_QUA.md`).
- Python 3 stdlib. Mọi lệnh chạy từ gốc dự án `trade_dai_han/`.
- **Thứ tự bắt buộc** để giữ độc lập: (a) → (d) TRƯỚC khi đọc `bot_v4/dong_co.py`, `bot_v4/ket_qua/`, `bot_v4/KET_QUA.md`
  → rồi (b), (c), (e), (f) → (g).

## Tệp liên quan
| Tệp | Vai trò |
|---|---|
| `bot_v4/THIET_KE.md` | thiết kế chốt (mục 0–11). Code ghi `# TK x.y` ở chỗ cài từng mục |
| `bot_v4/KHOA.md` | sha256 khoá (thiết kế; các mục khoá thêm ghi tiếp bên dưới) |
| `bot_v4/DIEN_GIAI.md` | cách hiểu chỗ thiết kế chưa nói — phải viết TRƯỚC lần chạy dữ liệu thật đầu tiên |
| `bot_v4/NHAT_KY_SUA.md` | mọi sửa code sau lần chạy thật đầu tiên (vì sao, trước/sau, kết quả mọi năm trước và sau) |
| `bot_v4/tai_du_lieu.py` → `bot_v4/du_lieu/` | nến 4H + 1D, `SHA256SUMS`, `NGUON.md` |
| `cong_cu/chi_bao.py` | EMA / RSI Wilder / ATR Wilder / fractal (TK 2) |
| `bot_v4/dong_co.py` | động cơ: `nap_du_lieu`, `view_tai`, `mo_phong_lenh`, `chay` |
| `bot_v4/kiem_tra.py` | kiểm tra bắt buộc TK 9 (phải PASS) |
| `bot_v4/chay.py` | `--nam 2024|2025|2026 --ro 6|BTC` → `bot_v4/ket_qua/<nam>_<ro>/{lenh,von,quyet_dinh}.csv, tom_tat.json` |
| `bot_v4/bao_cao.py` → `bot_v4/KET_QUA.md` | bảng TK 8, tự cộng lại, so v1/v2/mua-giữ, giả dược 1.000 lần, độ giống 180 buổi |
| `bot_v4/nhan_dinh.py` | view + lệnh hiện tại trên nến OKX mới nhất → `nhan_dinh_bot/v4_<YYYY-MM-DD_HHMM>.json` |

## (a) Kiểm hash khoá
```bash
shasum -a 256 bot_v4/THIET_KE.md            # so với dòng THIET_KE.md trong bot_v4/KHOA.md
cat bot_v4/KHOA.md                          # mọi dòng | `tệp` | `sha256` | khác (DIEN_GIAI, mã, dữ liệu) → shasum từng tệp
(cd bot_v4/du_lieu && shasum -a 256 -c SHA256SUMS)
ls -la -T bot_v4/ bot_v4/ket_qua/*/ 2>/dev/null   # giờ sửa: THIET_KE.md không được mới hơn giờ khoá (10:56 31/10)
```
Đối chiếu thêm với bảng hash ở **mục 0 của `bot_v4/KET_QUA.md`** (hash lúc chạy báo cáo) — đọc bảng này SAU bước (d).
Lệch bất kỳ → P0.

## (d) Backtest ĐỘC LẬP BTC 2025 — chỉ từ THIET_KE.md (làm ngay sau (a))
1. **Không mở** `bot_v4/dong_co.py`, `cong_cu/chi_bao.py`, `bot_v4/ket_qua/`, `bot_v4/KET_QUA.md`, `bot_v4/DIEN_GIAI.md` trước khi
   xong bước này. Chỉ đọc `bot_v4/THIET_KE.md` + dữ liệu `bot_v4/du_lieu/BTC_4H.csv`, `BTC_1D.csv` (cột ts_utc = giờ MỞ nến UTC).
2. Viết `kiem_cheo/codex_v4/backtest_doc_lap.py` (stdlib, tự viết chỉ báo — không import `cong_cu/chi_bao.py`):
   rổ **chỉ BTC**, năm **2025** (quyết định 2025-01-01 00:00 → 2025-12-31, lệnh còn mở đóng ở close cuối kỳ), vốn 4.000$,
   đủ mục 1–7: pha W1 (công tắc 2 cây), view H4 (PHÂN VÂN hẹp / HỒI theo RSI D1 / theo pha), mức + vùng hội tụ, limit,
   SL/TP/TP1 50% + dời SL, dừng theo giờ, phí + trượt, thứ tự trong nến, giới hạn lệnh.
3. Chỗ THIET_KE.md không nói rõ → **tự chọn, ghi lại** cách hiểu của bạn trong log (đừng đoán theo code người khác).
4. Ghi `kiem_cheo/codex_v4/lenh_BTC_2025.csv` cùng cột với lenh.csv (TK 8) + `kiem_cheo/codex_v4/view_BTC_2025.csv`
   (mỗi lần đóng H4: pha, view).
5. Sau đó mới so với `bot_v4/ket_qua/2025_BTC/lenh.csv` và `quyet_dinh.csv`:
   - % lần đóng H4 trùng pha, trùng view (phải gần 100%; lệch = chỉ ra mục TK nào hai bên hiểu khác).
   - Ghép lệnh theo (t_quyet_dinh, chieu): trùng / chỉ bên bạn / chỉ bên động cơ; với lệnh trùng so gia_vao, sl, tp1, tp2,
     t_khop, t_ra, ly_do_ra, lai_usd. Mỗi chênh lệch → tìm nguyên nhân (lúc này mới được mở `dong_co.py`), ghi bên nào lệch
     THIET_KE.md, hay thiết kế mơ hồ (khi đó: `DIEN_GIAI.md` có ghi trước không?).
   - So tổng: số lệnh, lãi$, tổng R.

## (b) Đọc THIET_KE → so code từng mục
```bash
grep -n "# TK" bot_v4/*.py cong_cu/chi_bao.py
```
Với từng mục **1, 2, 3, 4.1–4.3, 5.1, 5.2, 5.3, 6, 7, 8, 9, 10** của THIET_KE.md: code cài ở đâu (file:dòng), có đúng không, có thêm
gì thiết kế KHÔNG có (bộ lọc, tham số, ngưỡng lạ) không, mục 11 ("không làm") có lén làm không. Chú ý các chi tiết dễ sai:
- Fractal 7 nến (3 trái, 3 phải), đỉnh = high lớn nhất; xử lý bằng nhau; "3 đỉnh fractal H4 đã xác nhận gần nhất" (theo thời gian).
- Mức phải nằm trong (0,3%; 6%] so với close; cụm ≤ 0,5% liên tiếp và rộng ≤ 1%; điểm = số LOẠI căn cứ (fractal cả nhóm = 1).
- Bội số tròn (BTC 1.000, ETH 100, BNB 10, OKB 1, vàng 50, dầu 1) ≤ 0,1% giá → lùi 0,15% về phía giá.
- SL = mép xa cụm + max(0,3% giá vào, 0,5 ATR14 H4); SL tối thiểu theo tài sản; SL > 6% bỏ; TP2 = C − 1,618 × (A − B);
  TP1 = B non 0,2%; (TP2 − vào)/SL < 2 → bỏ; TP1 < 0,5R → 1R. Lệnh hồi: TP = EMA34 H4 lúc đặt, cần ≥ 1,5R, dừng 48h.
- Vốn: rủi ro 2% / 1% vốn HIỆN TẠI; đòn bẩy min(40%/SL%, 20); tối đa 3 lệnh chờ + mở; ký quỹ ≤ 50%.

## (c) Chạy lại → số phải khớp
Chạy trong bản sao để không ghi đè số gốc (bản sao phải cùng cấp `bot_v4/` để `cong_cu/`, `transcripts/` vẫn đúng đường dẫn):
```bash
rsync -a --delete --exclude ket_qua --exclude KET_QUA.md --exclude __pycache__ bot_v4/ bot_v4_codex/
python3 bot_v4_codex/kiem_tra.py                                   # phải PASS cả 5 nhóm TK 9
for n in 2024 2025 2026; do for r in 6 BTC; do python3 bot_v4_codex/chay.py --nam $n --ro $r; done; done
for d in bot_v4/ket_qua/*/; do diff -q "$d" "bot_v4_codex/ket_qua/$(basename $d)/"; done   # phải giống hệt
python3 bot_v4_codex/bao_cao.py --ra bot_v4_codex/KET_QUA.md
diff <(grep -v "Sinh tự động" bot_v4/KET_QUA.md) <(grep -v "Sinh tự động" bot_v4_codex/KET_QUA.md | sed 's/bot_v4_codex/bot_v4/g')
```
- `lenh.csv`, `von.csv`, `quyet_dinh.csv` phải **giống hệt từng byte**; `KET_QUA.md` chỉ được khác dòng giờ chạy
  (giả dược dùng hạt giống cố định → phải ra đúng số).
- Sau đó tải lại dữ liệu **trong bản sao**: `python3 bot_v4_codex/tai_du_lieu.py` rồi
  `diff bot_v4/du_lieu/SHA256SUMS bot_v4_codex/du_lieu/SHA256SUMS`. Giá có thể khác nhỏ nếu sàn/Yahoo sửa dữ liệu:
  với mỗi tệp khác, đếm số nến khác và chênh lệch tương đối lớn nhất (OHLC). Chạy lại `chay.py` trên dữ liệu mới và báo số
  lệnh/lãi thay đổi bao nhiêu (độ nhạy với dữ liệu) — đây là thông tin, không phải lỗi, trừ khi chênh lớn.
- Tự cộng lại độc lập (đừng tin mục 1 của KET_QUA.md): từ `lenh.csv`, tính lại lãi từng lệnh = chiều × KL × (giá ra − vào)
  (có TP1: hai nửa) − phí, so `lai_usd`; cộng dồn so `von_sau` và `von.csv`; phí so quy tắc TK 7.

## (e) Soi rò rỉ tương lai
1. **Nến đang chạy**: tại quyết định lúc đóng nến H4 t, mọi H4 dùng phải có giờ đóng ≤ t; D1 đã đóng ≤ t (D1 UTC đóng 00:00);
   W1 (thứ Hai 00:00 UTC) đã đóng ≤ t. Tìm mọi chỗ chỉ số `[-1]`, `bisect`, `<=`/`<` quanh giờ mở/đóng.
2. **Fractal**: chỉ dùng sau khi nến phải thứ 3 ĐÃ ĐÓNG (đỉnh ở nến i dùng được từ lúc đóng nến i+3). Kiểm cả fractal D1 và
   "S/R đổi vai" (đáy fractal bị close xuyên — close đó phải đã đóng).
3. **D1/W1 của vàng/dầu**: `ts_utc` 1D Yahoo = giờ mở phiên (17:00 New York − 23h); phiên dài ~23h. Động cơ coi D1 đóng lúc nào?
   Nếu coi đóng SỚM hơn giờ đóng phiên thật → rò. H4 vàng/dầu dựng từ 1H (nến thiếu giờ).
4. **Phép thử cắt cụt tự làm**: chọn ≥ 10 mốc T ngẫu nhiên, ghi bản dữ liệu đã XOÁ mọi nến mở ≥ T vào thư mục tạm, gọi
   `dong_co.nap_du_lieu(ts, thu_muc=TẠM)` + `chay` / `view_tai` → quyết định/lệnh đặt trước T phải giống hệt bản đủ.
   Xem `kiem_tra.py` nhóm 1 có thật sự cắt dữ liệu (không chỉ lọc kết quả) không.
5. **Khớp lệnh** (TK 7): nến khớp chỉ xét SL; nến chạm cả TP và SL → SL; gap qua SL → giá mở; lệnh limit khớp từ nến SAU nến đặt.
   Có chỗ nào dùng close/high/low của nến chưa tới để quyết định trong nến hiện tại không?
6. **Báo cáo**: `bot_v4/bao_cao.py` — giả dược có dùng dữ liệu sau cuối kỳ không (truyền `ket_thuc` = cuối kỳ); có 2 kiểu:
   A (đúng mục 8: lệnh đã khớp, limit = close nến ngẫu nhiên) và B (mọi lệnh đã đặt, limit cách close đúng tỉ lệ như lệnh thật).
   Mục 4b chạy CÙNG động cơ trên dữ liệu bước ngẫu nhiên: phân vị công bằng phải ≈ 50 — kiểm lại kết luận "A lệch về 0,
   B theo R TB ≈ 50" (đổi `HAT_GIONG_HC` vài lần, xem có còn đúng không). Độ giống: C = `bat_dau_vn + phut` (VN → UTC),
   `gio_cat` của `view_tai` ≤ C; nhãn buổi từ 2026-07-01 lấy `thi/dap_an_v2/phieu/`, trước đó `phieu/`. "Luật từ trên xuống"
   tính lại trong bao_cao.py phải trùng cột "Luật" của `thi/KET_QUA_THI.md` mục 7 (77 buổi T7–T10).
7. `bot_v4/nhan_dinh.py`: `gio_cat` (nến H4 đóng cuối dùng) tách khỏi `gio_phat_hanh`; chỉ dùng nến OKX confirm = 1;
   không ghi đè `bot_v4/du_lieu/`.

## (f) Có sửa luật theo kết quả không
- `DIEN_GIAI.md` có trước lần chạy thật đầu tiên không (so giờ sửa tệp với giờ tạo `bot_v4/ket_qua/*`, và hash trong KHOA.md
  nếu đã khoá)?
- Mỗi mục `NHAT_KY_SUA.md`: lý do có phải lỗi cài đặt so với THIET_KE (hợp lệ) hay là đổi tham số / thêm bộ lọc vì thấy kết quả
  (vi phạm)? Có ghi kết quả MỌI năm trước và sau sửa không? Sửa có chỉ làm đẹp 2025/2026 mà 2024 xấu đi không?
- Có thay đổi code nào KHÔNG được ghi (so `# TK` / hằng số trong code với THIET_KE.md; tìm tham số không có trong thiết kế)?

## (g) Kết luận → `kiem_cheo/CODEX_KIEM_V4.md`
- Mỗi phát hiện: **mức** (P0 = sai số/rò rỉ làm kết quả không dùng được · P1 = có thể sai/lệch thiết kế · P2 = vệ sinh) +
  file:dòng + bằng chứng (dòng code, số liệu, lệnh tái hiện) + cách sửa.
- Từng bước (a)–(f): "đã kiểm, kết quả …" kèm cách đã kiểm; bước nào không làm được thì ghi rõ vì sao.
- Bảng so (d): view trùng %, lệnh trùng / chỉ bạn / chỉ động cơ, chênh lãi$.
- Câu kết luận: số trong `bot_v4/KET_QUA.md` **dùng được / dùng được có điều kiện / không dùng được**, vì sao.
