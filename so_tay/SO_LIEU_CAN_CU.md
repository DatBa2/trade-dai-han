> **Ảnh chụp số liệu lúc 179 buổi / 3.349 mốc, ngày 30/10/2026; kho hiện 180 / 3.368** (31/10/2026: 3.368 mốc, 6 mốc không phải BTC/chưa rõ tài sản đã đặt `chac:false` — xem `kiem_cheo/VE_SINH_MOC.md`). Không dùng các số dưới như thống kê kho hiện tại; chạy lại `cong_cu/kiem_can_cu.py` để có số mới.

# Số liệu kiểm căn cứ (179 buổi, 3.349 mốc giá BTC) — 30/10/2026

Nguồn: `moc/*.json` (agent rút mọi mốc giá + căn cứ người đó NÓI RA), đối chiếu giá thật OKX (H1/H4/D1) và hợp đồng
CME BTC=F (Yahoo H1). Script: `cong_cu/kiem_can_cu.py`, `cong_cu/truy_nguoc.py`, `cong_cu/truy_fibo.py`.

## 1. Mức độ "có căn cứ"
- 82% mốc giá (2.742/3.349) có căn cứ người đó nói ra ngay khi nêu số.
- Vai trò mốc: đích 991 · hỗ trợ 456 · kháng cự 417 · entry 373 · TP 290 · mốc làm view sai 226 · SL 129.
- Loại căn cứ (số mốc, 1 mốc có thể nhiều loại): Fibo 549 · đỉnh/đáy/râu cũ 508 · cụm thanh lý/heatmap 443 · MA 308 ·
  gap CME 304 · trendline 112 · số tròn 57 · khác 1.149 (vùng S/R cũ đổi vai, mô hình, OI options, đóng nến…).

## 2. Thay đổi theo thời gian (% mốc dùng mỗi căn cứ)
| Tháng | Fibo | MA | Đỉnh/đáy cũ | Thanh lý | Gap CME | Trendline |
|---|---|---|---|---|---|---|
| 01 | 17% | 17% | 13% | 14% | 15% | 2% |
| 02 | 9% | 6% | 15% | 9% | 18% | 1% |
| 03 | 18% | 10% | 14% | 14% | 10% | 2% |
| 04 | 18% | 8% | 11% | 13% | 16% | 2% |
| 05 | 19% | 7% | 8% | 14% | **32%** | 3% |
| 06 | 23% | 9% | 18% | 8% | 7% | 3% |
| 07 | 16% | 12% | 17% | 10% | **1%** | 5% |
| 08 | 14% | 8% | 17% | 17% | 3% | **8%** |
| 09 | 10% | 6% | 17% | 18% | 1% | 3% |
| 10 | 15% | 9% | **22%** | 13% | 1% | 5% |
→ Gap CME gần như biến mất từ tháng 7 (CME giao dịch 24/7 từ 29/05; người đó nói 15/06 "gap không còn uy tín").
→ Nửa cuối năm dựa nhiều hơn vào đỉnh/đáy/vùng cũ đổi vai và cụm thanh lý; trendline tăng (người đó 18/08: "2026 giá phản ứng trendline tốt hơn MA").

## 3. Truy ngược công thức (con số người đó nói có tính lại được không)
**MA — người đó dùng EMA (hệ Sonic R), không phải SMA:**
| Người đó nói | n | SMA lệch trung vị | EMA lệch trung vị | Dải EMA34 (high/low) |
|---|---|---|---|---|
| MA34 H4 | 65 | 1,80% | 1,02% | **0,36% (khớp 54%)** |
| MA34 H1 | 6 | 1,09% | 0,61% | **0,28% (khớp 83%)** |
| MA34 D1 | 53 | 2,59% | 2,33% | 0,90% |
| MA89 H4 | 55 | 1,46% | 1,21% | |
| MA200 H4 | 76 | 2,27% | **1,15%** | |
| MA200 H1 | 12 | 1,64% | **0,85%** | |
| MA89 D1 | 48 | 3,55% | 2,35% | |
| MA200 D1 | 47 | 10,3% | 6,8% (không khớp — có thể nói lỏng/khung khác) | |
→ "MA34" của người đó = **dải rồng EMA34** (EMA34 của high, low, close); người đó lấy mép dải gần giá. MA89/MA200 = EMA.

**Đỉnh/đáy/râu cũ:** 346/464 = **75%** khớp đúng đỉnh/đáy fractal thật trên chart.
**Gap CME:** 123/298 = **41%** khớp đúng mép gap CME chưa lấp (giá hợp đồng BTC=F thật; phần còn lại là gap cũ/đã lấp/vùng gap).
**Fibo:** KHÔNG tái lập được bằng công thức cố định — thử 8 cửa sổ sóng (H4 7/14 ngày, D1 30/60/90/180 ngày, tuần, cặp xoay)
và mọi cặp đỉnh/đáy gần nhất #1–#4 trên H4/D1: khớp ≈ tỉ lệ ngẫu nhiên (57% vs 56%). → Người đó chọn điểm neo Fibo
**theo mắt, từng sóng một** (thường không nói kéo từ đâu); cần xem ảnh chart để biết cách chọn. Nhiều mốc Fibo còn là
"Fibo mở rộng 3 điểm" (Fibo Eric) — không phải thoái lui 2 điểm.
