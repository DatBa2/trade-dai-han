# GIỮ / LẬT view H4 — toàn bộ 180 buổi (học < 2026-07-01 · kiểm ≥ 2026-07-01)

Tạo lúc 2026-10-31 12:35 · `python3 hoc_v5/giu_lat/dac_trung.py --nhan moi && python3 hoc_v5/giu_lat/phan_tich.py --nhan moi`.
Nhãn (MỚI): hoc hoc_v5: 101, hoc thi/dap_an_v2: 2, kiem hoc_v5: 77 → 180/180 buổi có nhãn hướng. Không đọc `thi/bai_lam/`, `thi/KET_QUA_THI.md`.
Đặc trưng buổi N chỉ dùng nến đã đóng ≤ C_N (C = bat_dau_vn + phut), nhãn các buổi trước N, lịch tin công bố trước, Polymarket ≤ C_N. **view** = hướng TĂNG/GIẢM gần nhất của người đó trước N (bỏ PHÂN VÂN) = mốc "Giữ view" của bộ chấm. **GIỮ** = nhãn N = view; **LẬT** = nhãn N ngược view; **PV** = nhãn N PHÂN VÂN.
Nguồn phụ: trendline CÓ (`hoc_v5/trendline/su_kien.csv`, biến thể `rau|3|dai|nhieu_cham` do agent trendline khoá trên CẢ 180 buổi → đặc trưng trendline ở tập kiểm không hoàn toàn ngoài mẫu); lịch kinh tế CÓ (`du_lieu/tin_tuc/lich_kinh_te_2026.csv`); Polymarket CÓ (`du_lieu/tin_tuc/polymarket_fed.csv`).

## Tóm tắt

- Giữ view (so với hướng gần nhất): **128/179 = 72%** buổi (học 76%, kiểm 65%); LẬT 24%, sang PV 4%.
- LẬT mạnh nhất khi: Giá đi ngược view ≥ 2% từ C buổi trước (61% vs 19%); Lúc C giá vẫn ở bên kia mốc sai (59% vs 20%); Giá H4 ngoài dải EMA34 phía SAI view (52% vs 16%).
- Hay BỎ QUA (LẬT không cao hơn nền): Giá D1 sai phía EMA200 (giữ 75%, n 106); Giá D1 sai phía EMA89 (giữ 76%, n 104); Râu chạm đích CHẶNG KẾ TIẾP buổi trước (giữ 73%, n 90).
- Mốc sai của chính họ bị phá mà vẫn GIỮ đa số: Râu chạm/qua mốc sai buổi trước (chưa cần đóng) (giữ 61%, n 33); ≥ 1 nến H4 ĐÓNG qua mốc sai buổi trước (giữ 58%, n 24); Đóng qua mốc sai ĐÚNG khung + số nến họ nói (giữ 55%, n 22).
- Bộ luật khoá (chọn trên học, K = 0): (không luật — giữ view).
- Ngoài mẫu (kiểm T7–T10, 77 buổi): bộ luật 50/77 = 65% · giữ view 65% · luôn GIẢM 64% · từ trên xuống 61%.

## 1. Ma trận chuyển nhãn N−1 → N
179 cặp buổi liền nhau (hàng = N−1, cột = N).

| N−1 \ N | TĂNG | GIẢM | PHÂN VÂN | Tổng | Giữ nguyên nhãn |
|---|---|---|---|---|---|
| TĂNG | 55 | 22 | 0 | 77 | 55/77 = 71% |
| GIẢM | 20 | 67 | 7 | 94 | 67/94 = 71% |
| PHÂN VÂN | 1 | 6 | 1 | 8 | 1/8 = 12% |
| **Tổng** | 76 | 95 | 8 | 179 | **123/179 = 69%** |

So với **view** (hướng gần nhất, bỏ PV), tách tập học / kiểm:

| view trước | Tập | n | GIỮ | LẬT | sang PV |
|---|---|---|---|---|---|
| TĂNG | tất cả | 77 | 55/77 = 71% | 22/77 = 29% | 0/77 = 0% |
| TĂNG | học | 56 | 44/56 = 79% | 12/56 = 21% | 0/56 = 0% |
| TĂNG | kiểm | 21 | 11/21 = 52% | 10/21 = 48% | 0/21 = 0% |
| GIẢM | tất cả | 102 | 73/102 = 72% | 21/102 = 21% | 8/102 = 8% |
| GIẢM | học | 46 | 34/46 = 74% | 11/46 = 24% | 1/46 = 2% |
| GIẢM | kiểm | 56 | 39/56 = 70% | 10/56 = 18% | 7/56 = 12% |
| **Tất cả** | tất cả | 179 | 128/179 = 72% | 43/179 = 24% | 8/179 = 4% |
| **Tất cả** | học | 102 | 78/102 = 76% | 23/102 = 23% | 1/102 = 1% |
| **Tất cả** | kiểm | 77 | 50/77 = 65% | 20/77 = 26% | 7/77 = 9% |

- Đợt TĂNG liên tiếp: 22 đợt, trung vị 2 buổi, dài nhất 13 buổi.
- Đợt GIẢM liên tiếp: 28 đợt, trung vị 2 buổi, dài nhất 12 buổi.
- Đợt PHÂN VÂN liên tiếp: 7 đợt, trung vị 1 buổi, dài nhất 2 buổi.
- Đổi giữa buổi (đầu buổi ≠ cuối buổi): 9/179 = 5%.
- Người đó TỰ NÓI so với buổi trước (`nhin_lai_view_truoc.giu_hay_doi`, 177 buổi): nói GIỮ 139 (nhãn cũng giữ 120), nói ĐỔI 38 (nhãn cũng đổi 32). Lệch: 'đổi' về lệnh/đích mà hướng H4 không đổi, hoặc so với buổi PV.

## 2. Tỉ lệ LẬT theo điều kiện (so với view) — 180 buổi
Có n / GIỮ / LẬT / PV = các buổi CÓ điều kiện; Không n / LẬT = buổi KHÔNG có. Δ = điểm % LẬT (có − không), tính trên tất cả · tập học · tập kiểm (dấu giống nhau ở 2 tập = ổn định). **Lời** = số buổi (học / tất cả) người đó nói tới điều kiện (regex trên câu trích trong nhãn); 'hành vi' = hành vi của chính họ ở buổi trước; '—' = không phải lời họ → chỉ mô tả, KHÔNG vào mô hình.

**Mốc sai & đích**

| Điều kiện | Có n | GIỮ | LẬT | PV | Không n | LẬT | Δ tất cả | Δ học | Δ kiểm | Lời |
|---|---|---|---|---|---|---|---|---|---|---|
| Râu chạm/qua mốc sai buổi trước (chưa cần đóng) | 33 | 61% | 13/33 = 39% | 0 | 81 | 20% | +20 | +32 | +6 | 37 / 61 |
| ≥ 1 nến H4 ĐÓNG qua mốc sai buổi trước | 24 | 58% | 10/24 = 42% | 0 | 90 | 21% | +21 | +28 | +11 | 42 / 84 |
| 2 nến H4 liên tiếp đóng qua mốc sai | 19 | 58% | 8/19 = 42% | 0 | 95 | 22% | +20 | +26 | +12 | 7 / 17 |
| Đóng qua mốc sai ĐÚNG khung + số nến họ nói | 22 | 55% | 10/22 = 45% | 0 | 92 | 21% | +25 | +32 | +16 | 37 / 70 |
| Nến D1 đóng qua mốc sai buổi trước | 19 | 58% | 8/19 = 42% | 0 | 95 | 22% | +20 | +31 | +7 | 19 / 30 |
| Lúc C giá vẫn ở bên kia mốc sai | 17 | 41% | 10/17 = 59% | 0 | 97 | 20% | +39 | +59 | +21 | 21 / 40 |
| Râu chạm ĐÍCH chính buổi trước | 41 | 71% | 10/41 = 24% | 2 | 130 | 25% | -0 | +4 | -7 | 62 / 89 |
| Râu chạm đích CHẶNG KẾ TIẾP buổi trước | 90 | 73% | 20/90 = 22% | 4 | 76 | 22% | -0 | +5 | -9 | 55 / 91 |

**Nến & volume**

| Điều kiện | Có n | GIỮ | LẬT | PV | Không n | LẬT | Δ tất cả | Δ học | Δ kiểm | Lời |
|---|---|---|---|---|---|---|---|---|---|---|
| Nến H4 phá mốc sai CÓ volume (≥ 1,5 × TB20) | 10 | 50% | 5/10 = 50% | 0 | 104 | 23% | +27 | +1 | +44 | 72 / 127 |
| Có nến H4 thân ≥ 1,5 ATR NGƯỢC view | 30 | 50% | 13/30 = 43% | 2 | 149 | 20% | +23 | +15 | +28 | 55 / 101 |
| Nến H4 lớn ngược view có volume ≥ 1,5 × TB20 | 24 | 50% | 10/24 = 42% | 2 | 155 | 21% | +20 | +6 | +27 | 72 / 127 |
| Nến H4 volume lớn nhất (≥ 2 × TB20) là nến NGƯỢC view | 51 | 69% | 12/51 = 24% | 4 | 128 | 24% | -1 | -2 | -2 | 72 / 127 |
| Có nến D1 volume ≥ 1,5 × TB20 (mọi màu) | 38 | 68% | 10/38 = 26% | 2 | 133 | 23% | +4 | +6 | +2 | 72 / 127 |
| Nến D1 NHẤN CHÌM ngược view | 20 | 65% | 7/20 = 35% | 0 | 159 | 23% | +12 | +22 | -1 | 7 / 11 |
| Nến D1 đóng gần nhất NGƯỢC màu view | 82 | 62% | 25/82 = 30% | 6 | 97 | 19% | +12 | +12 | +11 | 43 / 58 |

**Lịch**

| Điều kiện | Có n | GIỮ | LẬT | PV | Không n | LẬT | Δ tất cả | Δ học | Δ kiểm | Lời |
|---|---|---|---|---|---|---|---|---|---|---|
| Buổi thứ Hai | 36 | 81% | 7/36 = 19% | 0 | 143 | 25% | -6 | -12 | +6 | 81 / 133 |
| Buổi đầu tuần (buổi đầu của tuần ISO) | 42 | 76% | 9/42 = 21% | 1 | 137 | 25% | -3 | -9 | +4 | 81 / 133 |
| Buổi đầu tháng | 9 | 78% | 2/9 = 22% | 0 | 170 | 24% | -2 | -3 | -1 | 23 / 32 |

**EMA / RSI / pha**

| Điều kiện | Có n | GIỮ | LẬT | PV | Không n | LẬT | Δ tất cả | Δ học | Δ kiểm | Lời |
|---|---|---|---|---|---|---|---|---|---|---|
| Giá H4 ngoài dải EMA34 phía SAI view | 40 | 42% | 21/40 = 52% | 2 | 139 | 16% | +37 | +44 | +31 | 49 / 77 |
| Giá H4 sai phía EMA89 | 59 | 58% | 22/59 = 37% | 3 | 120 | 18% | +20 | +23 | +16 | 36 / 46 |
| Giá H4 sai phía EMA200 | 78 | 65% | 22/78 = 28% | 5 | 101 | 21% | +7 | +5 | +10 | 42 / 60 |
| Giá D1 ngoài dải EMA34 phía SAI view | 54 | 72% | 13/54 = 24% | 2 | 125 | 24% | +0 | +6 | -7 | 49 / 77 |
| Giá D1 sai phía EMA89 | 104 | 76% | 20/104 = 19% | 5 | 75 | 31% | -11 | -9 | -15 | 36 / 46 |
| Giá D1 sai phía EMA200 | 106 | 75% | 21/106 = 20% | 5 | 73 | 30% | -10 | -3 | -21 | 42 / 60 |
| RSI H4 quá mua/bán THEO chiều view (TĂNG ≥ 70 / GIẢM ≤ 30) | 12 | 75% | 3/12 = 25% | 0 | 167 | 24% | +1 | -3 | +25 | 12 / 34 |
| RSI D1 quá mua/bán THEO chiều view | 14 | 57% | 6/14 = 43% | 0 | 165 | 22% | +20 | +19 | +25 | 12 / 34 |
| View ngược pha W1 (bot_v4 TK 3) | 59 | 63% | 21/59 = 36% | 1 | 120 | 18% | +17 | +10 | +30 | 67 / 107 |
| EMA34/89/200 H4 chụm < 0,6% giá | 13 | 62% | 3/13 = 23% | 2 | 166 | 24% | -1 | -23 | -1 | 55 / 98 |

**Tin tức**

| Điều kiện | Có n | GIỮ | LẬT | PV | Không n | LẬT | Δ tất cả | Δ học | Δ kiểm | Lời |
|---|---|---|---|---|---|---|---|---|---|---|
| Có tin lớn (FOMC/CPI/NFP) ra GIỮA 2 buổi (sau tin) | 26 | 81% | 4/26 = 15% | 1 | 153 | 25% | -10 | -3 | -20 | 86 / 153 |
| Có tin lớn trong 24 giờ SAU C (trước tin, thường tối cùng ngày) | 24 | 67% | 6/24 = 25% | 2 | 155 | 24% | +1 | +15 | -18 | 86 / 153 |
| Có tin lớn trong 48 giờ sau C | 48 | 62% | 15/48 = 31% | 3 | 131 | 21% | +10 | +13 | +5 | 86 / 153 |
| Trong cửa sổ FOMC (≤ 72h trước / ≤ 24h sau quyết định) | 28 | 82% | 2/28 = 7% | 3 | 151 | 27% | -20 | -17 | -24 | 41 / 97 |
| Polymarket kỳ Fed tới ngược view: view TĂNG mà P(tăng lãi suất) ≥ 30%, view GIẢM mà P(giảm) ≥ 30% | 12 | 50% | 6/12 = 50% | 0 | 165 | 22% | +28 | +2 | +41 | 30 / 93 |
| Polymarket 7 ngày: (P giảm − P tăng lãi suất) đổi ≥ 10 điểm NGƯỢC view | 23 | 70% | 6/23 = 26% | 1 | 153 | 24% | +2 | +6 | -1 | 30 / 93 |
| Polymarket từ buổi trước: (P giảm − P tăng) đổi ≥ 5 điểm NGƯỢC view | 26 | 50% | 11/26 = 42% | 2 | 149 | 21% | +21 | +38 | +17 | 30 / 93 |
| Buổi trước người đó có nhắc tin tức | 173 | 72% | 40/173 = 23% | 8 | 4 | 75% | -52 | -45 | -75 | hành vi |
| Buổi trước người đó dặn chờ/né tin | 70 | 76% | 12/70 = 17% | 5 | 107 | 29% | -12 | -20 | -2 | hành vi |

**Hành vi buổi trước**

| Điều kiện | Có n | GIỮ | LẬT | PV | Không n | LẬT | Δ tất cả | Δ học | Δ kiểm | Lời |
|---|---|---|---|---|---|---|---|---|---|---|
| Buổi trước người đó PHÂN VÂN | 8 | 75% | 1/8 = 12% | 1 | 171 | 25% | -12 | -23 | -13 | hành vi |
| Buổi trước người đó nói độ chắc THẤP | 67 | 66% | 19/67 = 28% | 4 | 112 | 21% | +7 | +11 | +1 | hành vi |
| Buổi trước người đó đã đổi ý giữa buổi | 8 | 62% | 2/8 = 25% | 1 | 171 | 24% | +1 | +28 | -10 | hành vi |
| Buổi trước có chặng kế tiếp NGƯỢC view (chờ hồi) | 99 | 72% | 23/99 = 23% | 5 | 80 | 25% | -2 | -2 | -1 | hành vi |

**Giá đi (mô tả)**

| Điều kiện | Có n | GIỮ | LẬT | PV | Không n | LẬT | Δ tất cả | Δ học | Δ kiểm | Lời |
|---|---|---|---|---|---|---|---|---|---|---|
| Giá đi ngược view ≥ 2% từ C buổi trước | 23 | 39% | 14/23 = 61% | 0 | 156 | 19% | +42 | +45 | +39 | — |
| Có lúc giá đi ngược view ≥ 3% giữa 2 buổi | 28 | 54% | 13/28 = 46% | 0 | 151 | 20% | +27 | +22 | +33 | — |
| Giá đi THEO view ≥ 2% từ C buổi trước | 34 | 82% | 6/34 = 18% | 0 | 145 | 26% | -8 | -10 | -1 | — |
| Cách buổi trước ≥ 48 giờ | 45 | 76% | 10/45 = 22% | 1 | 134 | 25% | -2 | -4 | +0 | — |
| Luật từ trên xuống cho hướng khác view | 60 | 57% | 26/60 = 43% | 0 | 106 | 13% | +30 | +26 | +41 | — |

**Trendline**

| Điều kiện | Có n | GIỮ | LẬT | PV | Không n | LẬT | Δ tất cả | Δ học | Δ kiểm | Lời |
|---|---|---|---|---|---|---|---|---|---|---|
| Trendline chính (H4/D1) bị phá NGƯỢC view giữa 2 buổi (đóng H4; trừ phá giả đã biết) | 28 | 54% | 12/28 = 43% | 1 | 151 | 21% | +22 | +30 | +17 | 77 / 138 |
| … trendline H4 bị phá ngược view | 25 | 52% | 11/25 = 44% | 1 | 154 | 21% | +23 | +24 | +22 | 77 / 138 |
| … trendline D1 bị phá ngược view | 8 | 62% | 3/8 = 38% | 0 | 171 | 23% | +14 | +45 | -6 | 77 / 138 |
| … phá ngược view bằng 2 nến H4 | 23 | 61% | 9/23 = 39% | 0 | 156 | 22% | +17 | +36 | +3 | 7 / 17 |
| … phá ngược view có volume ≥ 1,5 × TB20 | 15 | 47% | 8/15 = 53% | 0 | 164 | 21% | +32 | +28 | +34 | 72 / 127 |
| Trendline chính bị phá THEO view | 38 | 84% | 6/38 = 16% | 0 | 141 | 26% | -10 | -15 | -1 | 77 / 138 |

Tỉ lệ LẬT nền = 43/179 = 24% (học 23/102 = 23%, kiểm 20/77 = 26%).

**Điều kiện đi cùng LẬT mạnh nhất** (≥ 8 buổi có; xếp: Δ dương ở CẢ học và kiểm trước, rồi theo Δ):
- Giá đi ngược view ≥ 2% từ C buổi trước: LẬT 14/23 = 61% vs 19% khi không có (Δ +42; học +45, kiểm +39) · lời: —.
- Lúc C giá vẫn ở bên kia mốc sai: LẬT 10/17 = 59% vs 20% khi không có (Δ +39; học +59, kiểm +21) · lời: 21 / 40.
- Giá H4 ngoài dải EMA34 phía SAI view: LẬT 21/40 = 52% vs 16% khi không có (Δ +37; học +44, kiểm +31) · lời: 49 / 77.
- … phá ngược view có volume ≥ 1,5 × TB20: LẬT 8/15 = 53% vs 21% khi không có (Δ +32; học +28, kiểm +34) · lời: 72 / 127.
- Luật từ trên xuống cho hướng khác view: LẬT 26/60 = 43% vs 13% khi không có (Δ +30; học +26, kiểm +41) · lời: —.
- Polymarket kỳ Fed tới ngược view: view TĂNG mà P(tăng lãi suất) ≥ 30%, view GIẢM mà P(giảm) ≥ 30%: LẬT 6/12 = 50% vs 22% khi không có (Δ +28; học +2, kiểm +41) · lời: 30 / 93.
- Nến H4 phá mốc sai CÓ volume (≥ 1,5 × TB20): LẬT 5/10 = 50% vs 23% khi không có (Δ +27; học +1, kiểm +44) · lời: 72 / 127.

**Điều kiện người đó hay BỎ QUA** (sự kiện ngược view xảy ra ≥ 8 buổi mà % LẬT ≤ nền 24% hoặc ≤ 20%):
- Giá D1 sai phía EMA200: 106 buổi, vẫn GIỮ 80/106 = 75%, LẬT 21/106 = 20%.
- Giá D1 sai phía EMA89: 104 buổi, vẫn GIỮ 79/104 = 76%, LẬT 20/104 = 19%.
- Râu chạm đích CHẶNG KẾ TIẾP buổi trước: 90 buổi, vẫn GIỮ 66/90 = 73%, LẬT 20/90 = 22%.
- Nến H4 volume lớn nhất (≥ 2 × TB20) là nến NGƯỢC view: 51 buổi, vẫn GIỮ 35/51 = 69%, LẬT 12/51 = 24%.
- Có tin lớn (FOMC/CPI/NFP) ra GIỮA 2 buổi (sau tin): 26 buổi, vẫn GIỮ 21/26 = 81%, LẬT 4/26 = 15%.

**Mốc sai / nến ngược view có làm tăng LẬT nhưng người đó vẫn GIỮ đa số** (≥ 8 buổi, GIỮ ≥ 50%):
- Râu chạm/qua mốc sai buổi trước (chưa cần đóng): 33 buổi, vẫn GIỮ 20/33 = 61% (LẬT 39%, PV 0).
- ≥ 1 nến H4 ĐÓNG qua mốc sai buổi trước: 24 buổi, vẫn GIỮ 14/24 = 58% (LẬT 42%, PV 0).
- Đóng qua mốc sai ĐÚNG khung + số nến họ nói: 22 buổi, vẫn GIỮ 12/22 = 55% (LẬT 45%, PV 0).
- 2 nến H4 liên tiếp đóng qua mốc sai: 19 buổi, vẫn GIỮ 11/19 = 58% (LẬT 42%, PV 0).
- Nến D1 đóng qua mốc sai buổi trước: 19 buổi, vẫn GIỮ 11/19 = 58% (LẬT 42%, PV 0).
- Nến H4 phá mốc sai CÓ volume (≥ 1,5 × TB20): 10 buổi, vẫn GIỮ 5/10 = 50% (LẬT 50%, PV 0).
- Nến D1 đóng gần nhất NGƯỢC màu view: 82 buổi, vẫn GIỮ 51/82 = 62% (LẬT 30%, PV 6).
- Có nến D1 volume ≥ 1,5 × TB20 (mọi màu): 38 buổi, vẫn GIỮ 26/38 = 68% (LẬT 26%, PV 2).

Lời người đó cho từng điều kiện (câu trích ưu tiên `nhin_lai_view_truoc`, mốc sai, nến+volume):

- Râu chạm/qua mốc sai buổi trước (chưa cần đóng) — 37 / 61 buổi; vd 2026-01-08 [00:14:51]: "Nhịp ngày hôm qua cái nến đỏ này đối với cá nhân mình thì không có gì mới lạ. Và ở đây cái râu này rõ ràng là trap. Hôm qua mình nói mọi người, H4 nó…"
- ≥ 1 nến H4 ĐÓNG qua mốc sai buổi trước — 42 / 84 buổi; vd 2026-01-08 : "nếu muốn long thì đoạn này ít nhất anh em phải chờ có một cây H4 đóng màu xanh lên trên khỏi MA34 tức là trên vùng giá 91.000 thì lúc đó chúng ta hẵn…"
- 2 nến H4 liên tiếp đóng qua mốc sai — 7 / 17 buổi; vd 2026-04-09 : "[00:31:45] Thủng cái đáy H4 này, thủng khỏi 67.500. Đóng nến H4 thủng 67.500 hoặc là đóng một cặp H4 thủng cái vùng này thì coi như ai về nhà nấy. [0…"
- Đóng qua mốc sai ĐÚNG khung + số nến họ nói — 37 / 70 buổi; vd 2026-01-21 [00:17:43]: "Hôm qua mình nói vùng 90, hôm qua có nói với anh em một yếu tố nếu cây nến ngày mà đóng dưới vùng 90 thì gần như là confirm và hiện tại nó thủng luôn…"
- Nến D1 đóng qua mốc sai buổi trước — 19 / 30 buổi; vd 2026-01-21 [00:17:43]: "Hôm qua mình nói vùng 90, hôm qua có nói với anh em một yếu tố nếu cây nến ngày mà đóng dưới vùng 90 thì gần như là confirm và hiện tại nó thủng luôn…"
- Lúc C giá vẫn ở bên kia mốc sai — 21 / 40 buổi; vd 2026-01-22 [00:12:58]: "Rõ ràng ở khung ngày thì anh em thấy là nó đã phá qua, thủng trend line, đóng một cây nến ngày tiếp theo có màu xanh. Như mình nói, nếu cây nến này m…"
- Râu chạm ĐÍCH chính buổi trước — 62 / 89 buổi; vd 2026-01-14 [00:13:13]: "Nhưng vùng này là vùng chúng ta đã đạt target đầu tiên, có target thì phải có hành động. Coi như xong mục tiêu đầu tiên."
- Râu chạm đích CHẶNG KẾ TIẾP buổi trước — 55 / 91 buổi; vd 2026-01-14 [00:13:13]: "Nhưng vùng này là vùng chúng ta đã đạt target đầu tiên, có target thì phải có hành động. Coi như xong mục tiêu đầu tiên."
- Nến H4 phá mốc sai CÓ volume (≥ 1,5 × TB20) — 72 / 127 buổi; vd 2026-01-08 [00:14:51]: "Nhịp ngày hôm qua cái nến đỏ này đối với cá nhân mình thì không có gì mới lạ. Và ở đây cái râu này rõ ràng là trap. Hôm qua mình nói mọi người, H4 nó…"
- Có nến H4 thân ≥ 1,5 ATR NGƯỢC view — 55 / 101 buổi; vd 2026-01-27 [00:18:01]: "Cho nên hiện tại mình chưa short lại đâu. Giai đoạn này anh em vẫn phải linh hoạt một tí, đánh hai chiều. Hiện tại ở đây vẫn có một cây nến xanh ngày…"
- Nến H4 lớn ngược view có volume ≥ 1,5 × TB20 — 72 / 127 buổi; vd 2026-01-08 [00:14:51]: "Nhịp ngày hôm qua cái nến đỏ này đối với cá nhân mình thì không có gì mới lạ. Và ở đây cái râu này rõ ràng là trap. Hôm qua mình nói mọi người, H4 nó…"
- Nến H4 volume lớn nhất (≥ 2 × TB20) là nến NGƯỢC view — 72 / 127 buổi; vd 2026-01-08 [00:14:51]: "Nhịp ngày hôm qua cái nến đỏ này đối với cá nhân mình thì không có gì mới lạ. Và ở đây cái râu này rõ ràng là trap. Hôm qua mình nói mọi người, H4 nó…"
- Có nến D1 volume ≥ 1,5 × TB20 (mọi màu) — 72 / 127 buổi; vd 2026-01-08 [00:14:51]: "Nhịp ngày hôm qua cái nến đỏ này đối với cá nhân mình thì không có gì mới lạ. Và ở đây cái râu này rõ ràng là trap. Hôm qua mình nói mọi người, H4 nó…"
- Nến D1 NHẤN CHÌM ngược view — 7 / 11 buổi; vd 2026-05-27 [00:16:40]: "Thấy nỗ lực tăng rất nhiều trong vòng 3 ngày nhưng chỉ cần một cây nến xảy ra đâu đó lúc đêm ngày hôm qua cho đến sáng ngày hôm nay, nhấn chìm luôn t…"
- Nến D1 đóng gần nhất NGƯỢC màu view — 43 / 58 buổi; vd 2026-01-16 [00:05:13]: "Đầu tiên chúng ta có một cây nến ngày màu đỏ đầu tiên sau chuỗi tăng trưởng từ vùng 90 lên đến 97. Như ngày hôm trước mình nói, những vùng này đã đạt…"
- Buổi thứ Hai — 81 / 133 buổi; vd 2026-01-12 [00:30:16]: "Đối với cây nến tuần đóng như thế này thì mình vẫn giữ view là có khả năng lên được vùng 96 cho đến 100. Lên đây thì khả năng là sẽ chạm ngưỡng và đi…"
- Buổi đầu tuần (buổi đầu của tuần ISO) — 81 / 133 buổi; vd 2026-01-12 [00:30:16]: "Đối với cây nến tuần đóng như thế này thì mình vẫn giữ view là có khả năng lên được vùng 96 cho đến 100. Lên đây thì khả năng là sẽ chạm ngưỡng và đi…"
- Buổi đầu tháng — 23 / 32 buổi; vd 2026-05-04 [00:26:33]: "Cây đầu tháng đã break H4 và đi lên. Vì sao điểm này là một nhịp quan trọng? Bởi vì trước đó nó đã tạo một xu hướng điều chỉnh đỉnh đáy thấp dần. Như…"
- Giá H4 ngoài dải EMA34 phía SAI view — 49 / 77 buổi; vd 2026-01-15 [00:13:05]: "Tầm này D1 khá là đẹp, vượt qua khỏi MA89. Khi vượt qua khỏi MA89 thì kế tiếp là MA200. Mình cũng nói với anh em là cái vùng 100 này, vùng 98, 99, 10…"
- Giá H4 sai phía EMA89 — 36 / 46 buổi; vd 2026-01-15 [00:13:05]: "Tầm này D1 khá là đẹp, vượt qua khỏi MA89. Khi vượt qua khỏi MA89 thì kế tiếp là MA200. Mình cũng nói với anh em là cái vùng 100 này, vùng 98, 99, 10…"
- Giá H4 sai phía EMA200 — 42 / 60 buổi; vd 2026-01-15 [00:13:05]: "Tầm này D1 khá là đẹp, vượt qua khỏi MA89. Khi vượt qua khỏi MA89 thì kế tiếp là MA200. Mình cũng nói với anh em là cái vùng 100 này, vùng 98, 99, 10…"
- Giá D1 ngoài dải EMA34 phía SAI view — 49 / 77 buổi; vd 2026-01-15 [00:13:05]: "Tầm này D1 khá là đẹp, vượt qua khỏi MA89. Khi vượt qua khỏi MA89 thì kế tiếp là MA200. Mình cũng nói với anh em là cái vùng 100 này, vùng 98, 99, 10…"
- Giá D1 sai phía EMA89 — 36 / 46 buổi; vd 2026-01-15 [00:13:05]: "Tầm này D1 khá là đẹp, vượt qua khỏi MA89. Khi vượt qua khỏi MA89 thì kế tiếp là MA200. Mình cũng nói với anh em là cái vùng 100 này, vùng 98, 99, 10…"
- Giá D1 sai phía EMA200 — 42 / 60 buổi; vd 2026-01-15 [00:13:05]: "Tầm này D1 khá là đẹp, vượt qua khỏi MA89. Khi vượt qua khỏi MA89 thì kế tiếp là MA200. Mình cũng nói với anh em là cái vùng 100 này, vùng 98, 99, 10…"
- RSI H4 quá mua/bán THEO chiều view (TĂNG ≥ 70 / GIẢM ≤ 30) — 12 / 34 buổi; vd 2026-01-15 [00:14:08]: "H4 này có phân kỳ, các bạn cũng nhìn thấy. RSI này nó đang quay trở lại. Phân kỳ thì không có nghĩa là giá nó sẽ điều chỉnh hẳn."
- RSI D1 quá mua/bán THEO chiều view — 12 / 34 buổi; vd 2026-01-15 [00:14:08]: "H4 này có phân kỳ, các bạn cũng nhìn thấy. RSI này nó đang quay trở lại. Phân kỳ thì không có nghĩa là giá nó sẽ điều chỉnh hẳn."
- View ngược pha W1 (bot_v4 TK 3) — 67 / 107 buổi; vd 2026-01-12 [00:30:16]: "Đối với cây nến tuần đóng như thế này thì mình vẫn giữ view là có khả năng lên được vùng 96 cho đến 100. Lên đây thì khả năng là sẽ chạm ngưỡng và đi…"
- EMA34/89/200 H4 chụm < 0,6% giá — 55 / 98 buổi; vd 2026-01-29 [00:02:28]: "Chủ yếu sau cái tin lãi suất ngày hôm qua thì giá nó lợi dụng tin để nó lên, như mình nói nếu mà nó tăng trước tin thì sau tin nó gãy, nếu sideway tr…"
- Có tin lớn (FOMC/CPI/NFP) ra GIỮA 2 buổi (sau tin) — 86 / 153 buổi; vd 2026-01-29 [00:02:28]: "Chủ yếu sau cái tin lãi suất ngày hôm qua thì giá nó lợi dụng tin để nó lên, như mình nói nếu mà nó tăng trước tin thì sau tin nó gãy, nếu sideway tr…"
- Có tin lớn trong 24 giờ SAU C (trước tin, thường tối cùng ngày) — 86 / 153 buổi; vd 2026-01-29 [00:02:28]: "Chủ yếu sau cái tin lãi suất ngày hôm qua thì giá nó lợi dụng tin để nó lên, như mình nói nếu mà nó tăng trước tin thì sau tin nó gãy, nếu sideway tr…"
- Có tin lớn trong 48 giờ sau C — 86 / 153 buổi; vd 2026-01-29 [00:02:28]: "Chủ yếu sau cái tin lãi suất ngày hôm qua thì giá nó lợi dụng tin để nó lên, như mình nói nếu mà nó tăng trước tin thì sau tin nó gãy, nếu sideway tr…"
- Trong cửa sổ FOMC (≤ 72h trước / ≤ 24h sau quyết định) — 41 / 97 buổi; vd 2026-01-29 [00:02:28]: "Chủ yếu sau cái tin lãi suất ngày hôm qua thì giá nó lợi dụng tin để nó lên, như mình nói nếu mà nó tăng trước tin thì sau tin nó gãy, nếu sideway tr…"
- Polymarket kỳ Fed tới ngược view: view TĂNG mà P(tăng lãi suất) ≥ 30%, view GIẢM mà P(giảm) ≥ 30% — 30 / 93 buổi; vd 2026-06-10 [00:16:13]: "View của ngày hôm qua mình đã nói rất rõ. Hôm thứ hai nó đóng cho chúng ta một cụm nến đảo chiều cực kỳ tốt, theo cá nhân mình xác suất xảy ra đảo ch…"
- Polymarket 7 ngày: (P giảm − P tăng lãi suất) đổi ≥ 10 điểm NGƯỢC view — 30 / 93 buổi; vd 2026-06-10 [00:16:13]: "View của ngày hôm qua mình đã nói rất rõ. Hôm thứ hai nó đóng cho chúng ta một cụm nến đảo chiều cực kỳ tốt, theo cá nhân mình xác suất xảy ra đảo ch…"
- Polymarket từ buổi trước: (P giảm − P tăng) đổi ≥ 5 điểm NGƯỢC view — 30 / 93 buổi; vd 2026-06-10 [00:16:13]: "View của ngày hôm qua mình đã nói rất rõ. Hôm thứ hai nó đóng cho chúng ta một cụm nến đảo chiều cực kỳ tốt, theo cá nhân mình xác suất xảy ra đảo ch…"
- Trendline chính (H4/D1) bị phá NGƯỢC view giữa 2 buổi (đóng H4; trừ phá giả đã biết) — 77 / 138 buổi; vd 2026-01-19 [00:11:06]: "Và bây giờ anh em thấy khung tuần cũng đã xong, khung ngày thì cũng đã chạm cái trendline ở trên này, chạm cái kênh giá đó. Hoàn toàn chúng ta không …"
- … trendline H4 bị phá ngược view — 77 / 138 buổi; vd 2026-01-19 [00:11:06]: "Và bây giờ anh em thấy khung tuần cũng đã xong, khung ngày thì cũng đã chạm cái trendline ở trên này, chạm cái kênh giá đó. Hoàn toàn chúng ta không …"
- … trendline D1 bị phá ngược view — 77 / 138 buổi; vd 2026-01-19 [00:11:06]: "Và bây giờ anh em thấy khung tuần cũng đã xong, khung ngày thì cũng đã chạm cái trendline ở trên này, chạm cái kênh giá đó. Hoàn toàn chúng ta không …"
- … phá ngược view bằng 2 nến H4 — 7 / 17 buổi; vd 2026-04-09 : "[00:31:45] Thủng cái đáy H4 này, thủng khỏi 67.500. Đóng nến H4 thủng 67.500 hoặc là đóng một cặp H4 thủng cái vùng này thì coi như ai về nhà nấy. [0…"
- … phá ngược view có volume ≥ 1,5 × TB20 — 72 / 127 buổi; vd 2026-01-08 [00:14:51]: "Nhịp ngày hôm qua cái nến đỏ này đối với cá nhân mình thì không có gì mới lạ. Và ở đây cái râu này rõ ràng là trap. Hôm qua mình nói mọi người, H4 nó…"
- Trendline chính bị phá THEO view — 77 / 138 buổi; vd 2026-01-19 [00:11:06]: "Và bây giờ anh em thấy khung tuần cũng đã xong, khung ngày thì cũng đã chạm cái trendline ở trên này, chạm cái kênh giá đó. Hoàn toàn chúng ta không …"

## 3. Lời người đó: vì sao GIỮ / vì sao ĐỔI
Nguồn: `nhin_lai_view_truoc` (140 buổi nói GIỮ, 38 buổi nói ĐỔI so với buổi trước). 1 buổi có thể thuộc nhiều nhóm (regex trên `vi_sao` = tóm tắt lý do họ tự nói). Câu trích (`trich`) là lời người đó; giờ = phút trong video. % = trong số buổi nói GIỮ / ĐỔI.

| Nhóm lý do | GIỮ | ĐỔI |
|---|---|---|
| Nến ĐÓNG xấu / thủng / gãy mốc (đã xảy ra) | 62 (44%) | 25 (66%) |
| Đầu tuần / tháng xem lại khung lớn | 29 (21%) | 13 (34%) |
| MA / Fibo / gap (vùng kỹ thuật) | 84 (60%) | 27 (71%) |
| Nến đảo chiều / lực mua bán / volume | 46 (33%) | 16 (42%) |
| Nến tuần/ngày (khung lớn) quyết định | 94 (67%) | 28 (74%) |
| Chạm đích / hoàn thành mục tiêu | 16 (11%) | 5 (13%) |
| Nhịp ngược chỉ là hồi / quét / trap / fake | 37 (26%) | 10 (26%) |
| Tâm lý / thanh lý / Fear&Greed | 22 (16%) | 4 (11%) |
| Tin tức / vĩ mô | 27 (19%) | 5 (13%) |
| Cấu trúc đỉnh/đáy, hỗ trợ chưa gãy | 32 (23%) | 6 (16%) |
| Đi đúng kịch bản / plan chưa bị tác động | 40 (29%) | 2 (5%) |
| (không vào nhóm nào) | 1 | 0 |

**Lý do GIỮ — câu trích:**
- *Đi đúng kịch bản / plan chưa bị tác động* (40): 2026-01-06 [00:03:58] (view trước TĂNG): "Các vùng giá thì như hôm qua chúng ta vẫn giữ nguyên cái plan của ngày hôm qua. Không có thay đổi gì nhiều lắm."; 2026-01-19 [00:11:06] (view trước GIẢM): "Và bây giờ anh em thấy khung tuần cũng đã xong, khung ngày thì cũng đã chạm cái trendline ở trên này, chạm cái kênh giá đó. Hoàn toàn chúng ta không …"
- *Cấu trúc đỉnh/đáy, hỗ trợ chưa gãy* (32): 2026-03-05 [00:06:07] (view trước TĂNG): "Hôm qua gần như là không ăn được thì chắc cũng không ai thua, bởi vì hôm qua mình báo mọi người là tuyệt đối không short ở đoạn này. Khi nó đã tạo mộ…"; 2026-03-11 [00:16:09] (view trước TĂNG): "Đà tăng H4 ở đây thì anh em thấy mặc dù nó bị cạn xuống đây, bị đạp trên line này, nhưng H4 nó giữ ở đây thì vẫn đang giữ được xu hướng phục hồi đi l…"
- *Nến ĐÓNG xấu / thủng / gãy mốc (đã xảy ra)* (62): 2026-01-21 [00:17:43] (view trước GIẢM): "Hôm qua mình nói vùng 90, hôm qua có nói với anh em một yếu tố nếu cây nến ngày mà đóng dưới vùng 90 thì gần như là confirm và hiện tại nó thủng luôn…"; 2026-01-22 [00:12:58] (view trước GIẢM): "Rõ ràng ở khung ngày thì anh em thấy là nó đã phá qua, thủng trend line, đóng một cây nến ngày tiếp theo có màu xanh. Như mình nói, nếu cây nến này m…"
- *Nến tuần/ngày (khung lớn) quyết định* (94): 2026-01-12 [00:30:16] (view trước TĂNG): "Đối với cây nến tuần đóng như thế này thì mình vẫn giữ view là có khả năng lên được vùng 96 cho đến 100. Lên đây thì khả năng là sẽ chạm ngưỡng và đi…"; 2026-01-15 [00:13:05] (view trước TĂNG): "Tầm này D1 khá là đẹp, vượt qua khỏi MA89. Khi vượt qua khỏi MA89 thì kế tiếp là MA200. Mình cũng nói với anh em là cái vùng 100 này, vùng 98, 99, 10…"
- *Chạm đích / hoàn thành mục tiêu* (16): 2026-01-14 [00:13:13] (view trước TĂNG): "Nhưng vùng này là vùng chúng ta đã đạt target đầu tiên, có target thì phải có hành động. Coi như xong mục tiêu đầu tiên."; 2026-01-09 [00:11:08] (view trước GIẢM): "Nó đi như cái này thì có thể là đang đi theo kịch bản hôm qua chúng ta nói: về đến gap đầu, về gap một. Sau đó đi lên test rồi đi về lại gap hai và đ…"
- *Nhịp ngược chỉ là hồi / quét / trap / fake* (37): 2026-01-28 [00:13:26] (view trước GIẢM): "Quay lại với Bitcoin. Ngày hôm qua có một pha fake out. Hôm qua chúng ta cũng nói lý do vì sao anh em không nên short trong ngày hôm qua, bởi vì nến …"; 2026-03-09 [00:30:15] (view trước TĂNG): "Tức là hoàn thành nhịp đầu tiên của cái nhịp phục hồi 72 theo phục hồi kỹ thuật. Chứ không có bất kỳ một cái up trend nào đây hết. Đây chỉ còn chẳng …"
- *MA / Fibo / gap (vùng kỹ thuật)* (84): 2026-01-07 [00:04:31] (view trước TĂNG): "Hôm qua mình bảo là khả năng về 91. Nó về test lại cái vùng gap mới. Test vùng gap ở 91 đêm ngày hôm qua. Về 9100, test H4."; 2026-01-09 [00:11:08] (view trước GIẢM): "Nó đi như cái này thì có thể là đang đi theo kịch bản hôm qua chúng ta nói: về đến gap đầu, về gap một. Sau đó đi lên test rồi đi về lại gap hai và đ…"
- *Nến đảo chiều / lực mua bán / volume* (46): 2026-01-20 [00:07:45] (view trước GIẢM): "Hôm qua chẳng qua cái nhịp long ở đây chúng ta kỳ vọng nó test râu và nó tạo hai đáy để làm gì? Chúng ta bắt một con sóng hồi ăn nhẹ khoảng 1000 giá …"; 2026-01-28 [00:13:26] (view trước GIẢM): "Quay lại với Bitcoin. Ngày hôm qua có một pha fake out. Hôm qua chúng ta cũng nói lý do vì sao anh em không nên short trong ngày hôm qua, bởi vì nến …"
- *Tin tức / vĩ mô* (27): 2026-01-29 [00:02:28] (view trước GIẢM): "Chủ yếu sau cái tin lãi suất ngày hôm qua thì giá nó lợi dụng tin để nó lên, như mình nói nếu mà nó tăng trước tin thì sau tin nó gãy, nếu sideway tr…"; 2026-03-02 [00:37:58] (view trước TĂNG): "Thị trường bị bán bởi tin này nhưng sau đó lực mua nhảy vào và phục hồi giá rất nhanh. Chứng tỏ đoạn này lực mua giữ giá tốt và lực bán suy yếu, vì t…"
- *Tâm lý / thanh lý / Fear&Greed* (22): 2026-03-17 [00:33:31] (view trước TĂNG): "Mình xem liquid. Hôm qua lúc livestream có một vùng liquid rất lớn nằm ở 74k8, đúng rồi, sau đó [00:34:02] đến khuya nó lụm thật. 4:00 sáng nó bay lê…"; 2026-04-13 [00:15:32] (view trước TĂNG): "Mục đích chính của nó là về test, nói chung kỹ thuật mọi con đường đều đổ về thành Rome. Vừa giết các lệnh long FOMO đòn bảy cao ở trên vùng 7273 này…"
- *Đầu tuần / tháng xem lại khung lớn* (29): 2026-01-12 [00:30:16] (view trước TĂNG): "Đối với cây nến tuần đóng như thế này thì mình vẫn giữ view là có khả năng lên được vùng 96 cho đến 100. Lên đây thì khả năng là sẽ chạm ngưỡng và đi…"; 2026-01-26 [00:07:53] (view trước GIẢM): "Mình hy vọng là nó fake breakout, tức là nó giả vờ gãy khỏi cái này bằng cách kéo lên những ngày thứ hai là ngày hôm nay, nhưng không chịu. Nó chỉ ké…"

**Lý do ĐỔI — câu trích:**
- *Đi đúng kịch bản / plan chưa bị tác động* (2): 2026-07-10 [00:17:43] (view trước —): "Hỏi: H4 đóng dưới MA200 thì short được không? Không. Đoạn này mình thấy các bạn chưa nên short lại đâu. Lực như thế này chúng ta không nên short nữa,…"; 2026-09-24  (view trước TĂNG): "Mình đã cảnh báo ở bài post trước: kháng cự hiện tại đâu đó khoảng 87.000; nếu muốn chinh phục 88 đến 90.000 thì tối thiểu phải có một cây H4 đóng tr…"
- *Cấu trúc đỉnh/đáy, hỗ trợ chưa gãy* (6): 2026-03-31 [00:21:05] (view trước GIẢM): "Hôm qua ở đây nó tạo một H4 hai đáy anh em. H4 hai đáy đi lên thì nhịp này biết đâu được nó lên được 71.000 mấy thì sao... [00:31:31] chúng ta nhìn H…"; 2026-05-04 [00:26:33] (view trước GIẢM): "Cây đầu tháng đã break H4 và đi lên. Vì sao điểm này là một nhịp quan trọng? Bởi vì trước đó nó đã tạo một xu hướng điều chỉnh đỉnh đáy thấp dần. Như…"
- *Nến ĐÓNG xấu / thủng / gãy mốc (đã xảy ra)* (25): 2026-01-08 [00:14:51] (view trước TĂNG): "Nhịp ngày hôm qua cái nến đỏ này đối với cá nhân mình thì không có gì mới lạ. Và ở đây cái râu này rõ ràng là trap. Hôm qua mình nói mọi người, H4 nó…"; 2026-01-30 [00:04:34] (view trước PHÂN VÂN): "Thủng 87k5 short, đúng rồi. Hôm qua mình bảo có hai vùng 87.000 và 88.000. Muốn short thì nó gãy vùng này là short, còn muốn long thì nó phải vượt qu…"
- *Nến tuần/ngày (khung lớn) quyết định* (28): 2026-01-16 [00:05:13] (view trước TĂNG): "Đầu tiên chúng ta có một cây nến ngày màu đỏ đầu tiên sau chuỗi tăng trưởng từ vùng 90 lên đến 97. Như ngày hôm trước mình nói, những vùng này đã đạt…"; 2026-03-16 [00:09:39] (view trước GIẢM): "Anh em thấy là chúng ta đã kết thúc một cây nến tuần cực kỳ đẹp. Và như tuần trước thì rõ ràng mình có nói là cây nến tuần này, một cây đóng nến râu …"
- *Chạm đích / hoàn thành mục tiêu* (5): 2026-02-06 [00:14:29] (view trước GIẢM): "Nói chung tinh thần của mình ngày hôm nay từ giờ đến cuối tuần thì lời khuyên của mình đối với anh em là đừng có short nữa. Mình nghĩ loanh quanh nhị…"; 2026-03-20 [00:23:09] (view trước TĂNG): "Còn giữ view hồi sáng không? View hồi sáng là không. Thực sự đoạn này phải đánh view ngắn thôi các bạn. Như mình nói lúc sáng thì nó đã lên đến view …"
- *Nhịp ngược chỉ là hồi / quét / trap / fake* (10): 2026-04-03 [00:30:58] (view trước GIẢM): "hôm qua mình cho các bạn sell short một lệnh nhẹ nhẹ nhưng cây H4 chiều ngày hôm qua nó trap ác quá... Nó đóng một cây H4 rất xanh. Và trên livestrea…"; 2026-03-13 [00:33:49] (view trước TĂNG): "Như lúc sáng mình báo anh em là chờ về 69, cuối cùng là nó đâu có về được. Nó lòng vòng nhấp nhấp ở đoạn 71 này sau đó vút luôn"
- *MA / Fibo / gap (vùng kỹ thuật)* (27): 2026-02-11 [00:02:04] (view trước TĂNG): "Những ngày vừa rồi vẫn quan sát thị trường liên tục nhưng như mọi người thấy thì market không chạy bao nhiêu cả và liên tục bị từ chối ở đường MA34 t…"; 2026-02-16 [00:16:12] (view trước GIẢM): "đang có một cái mô hình là đáy cao lên nhưng đỉnh đi bằng. Có nghĩa là gì? Vùng này là lực cản kháng cự liên tục đẩy giá xuống nhưng theo thời gian t…"
- *Nến đảo chiều / lực mua bán / volume* (16): 2026-01-08 [00:14:51] (view trước TĂNG): "Nhịp ngày hôm qua cái nến đỏ này đối với cá nhân mình thì không có gì mới lạ. Và ở đây cái râu này rõ ràng là trap. Hôm qua mình nói mọi người, H4 nó…"; 2026-01-16 [00:05:13] (view trước TĂNG): "Đầu tiên chúng ta có một cây nến ngày màu đỏ đầu tiên sau chuỗi tăng trưởng từ vùng 90 lên đến 97. Như ngày hôm trước mình nói, những vùng này đã đạt…"
- *Tin tức / vĩ mô* (5): 2026-03-24 [00:21:23] (view trước GIẢM): "khi giảm về 70 lại về đúng vùng 67000, trendline hai ngày vừa rồi, lại có tin Trump với Iran 48 giờ, mọi thứ tự động khớp với nhau... Về phân tích kỹ…"; 2026-06-11 [00:22:02] (view trước GIẢM): "Nhưng trước cái tin hôm qua thì giá đã được cứu và kéo lên cái cây màu xanh này, cây có tin. Quay lại cái tin một tí, tin hôm qua là tin rất tốt đối …"
- *Tâm lý / thanh lý / Fear&Greed* (4): 2026-02-06 [00:14:29] (view trước GIẢM): "Nói chung tinh thần của mình ngày hôm nay từ giờ đến cuối tuần thì lời khuyên của mình đối với anh em là đừng có short nữa. Mình nghĩ loanh quanh nhị…"; 2026-06-10 [00:16:13] (view trước TĂNG): "View của ngày hôm qua mình đã nói rất rõ. Hôm thứ hai nó đóng cho chúng ta một cụm nến đảo chiều cực kỳ tốt, theo cá nhân mình xác suất xảy ra đảo ch…"
- *Đầu tuần / tháng xem lại khung lớn* (13): 2026-05-04 [00:26:33] (view trước GIẢM): "Cây đầu tháng đã break H4 và đi lên. Vì sao điểm này là một nhịp quan trọng? Bởi vì trước đó nó đã tạo một xu hướng điều chỉnh đỉnh đáy thấp dần. Như…"; 2026-06-10 [00:16:13] (view trước TĂNG): "View của ngày hôm qua mình đã nói rất rõ. Hôm thứ hai nó đóng cho chúng ta một cụm nến đảo chiều cực kỳ tốt, theo cá nhân mình xác suất xảy ra đảo ch…"

**Đổi GIỮA buổi** (`ly_do_doi_y`, 8 buổi):
- *Cấu trúc đỉnh/đáy, hỗ trợ chưa gãy* (2): vd 2026-04-02 TĂNG→GIẢM: "Đầu buổi cho là 'chưa gãy', vùng 66-67k có thể tìm setup long; sau đó H4 đóng nến đỏ full lực ngay Fibo, giá rụng tiếp ('Hỏng rồi. Nát luôn'), mọi kh…"
- *Nến ĐÓNG xấu / thủng / gãy mốc (đã xảy ra)* (6): vd 2026-04-24 TĂNG→GIẢM: "Đầu buổi vẫn coi xu hướng tăng (chờ chỉnh về 72-73 rồi lên đủ target 80-82). Về sau nghiêng dần sang 'lên quét rồi gãy': nến D1 rút râu thân hẹp ngay…"
- *Nến tuần/ngày (khung lớn) quyết định* (3): vd 2026-04-24 TĂNG→GIẢM: "Đầu buổi vẫn coi xu hướng tăng (chờ chỉnh về 72-73 rồi lên đủ target 80-82). Về sau nghiêng dần sang 'lên quét rồi gãy': nến D1 rút râu thân hẹp ngay…"
- *Nhịp ngược chỉ là hồi / quét / trap / fake* (1): vd 2026-04-24 TĂNG→GIẢM: "Đầu buổi vẫn coi xu hướng tăng (chờ chỉnh về 72-73 rồi lên đủ target 80-82). Về sau nghiêng dần sang 'lên quét rồi gãy': nến D1 rút râu thân hẹp ngay…"
- *MA / Fibo / gap (vùng kỹ thuật)* (4): vd 2026-04-02 TĂNG→GIẢM: "Đầu buổi cho là 'chưa gãy', vùng 66-67k có thể tìm setup long; sau đó H4 đóng nến đỏ full lực ngay Fibo, giá rụng tiếp ('Hỏng rồi. Nát luôn'), mọi kh…"
- *Nến đảo chiều / lực mua bán / volume* (2): vd 2026-04-24 TĂNG→GIẢM: "Đầu buổi vẫn coi xu hướng tăng (chờ chỉnh về 72-73 rồi lên đủ target 80-82). Về sau nghiêng dần sang 'lên quét rồi gãy': nến D1 rút râu thân hẹp ngay…"
- *Tâm lý / thanh lý / Fear&Greed* (1): vd 2026-04-24 TĂNG→GIẢM: "Đầu buổi vẫn coi xu hướng tăng (chờ chỉnh về 72-73 rồi lên đủ target 80-82). Về sau nghiêng dần sang 'lên quét rồi gãy': nến D1 rút râu thân hẹp ngay…"
- *Đầu tuần / tháng xem lại khung lớn* (1): vd 2026-10-02 GIẢM→GIẢM: "Đầu buổi đánh chủ lực sale, kỳ vọng về 81–82. Sau khi H4 đóng xanh trên 85 và giá quét qua SL lệnh sale ở ~85, người nói bỏ sale ngắn hạn ('các lệnh …"

**Nến + volume** (`nen_volume`, 1233 lời ở 178 buổi): theo khung H4 421, D1 223, H1 144, M5 127, ? 101, M15 88, W1 66, M30 39, M1 6, MN 4, M30/M5 3, H1/M5 3, M1 (tháng) 3, H1/H4 2, H4/D1 1, H1/M30 1, H4/H1 1; có nói volume: 268/1233 = 22%.
- Họ rút ra từ nến: khác 577, đọc lực mạnh/yếu, volume 210, xác nhận xu hướng / đảo chiều 158, gạt đi: fake / trap / quét / chỉ là hồi 156, chờ nến đóng xác nhận (nếu/khi đóng … thì …) 132.
- Khi nói volume: volume lớn / tăng / vượt trội 108, khác 93, volume nhỏ / yếu / chưa có 67.
- Theo kết quả buổi: GIỮ (126 buổi): 6.9 lời nến/buổi, 24% là nến D1/W1, 22% có nói volume; LẬT (43 buổi): 7.2 lời nến/buổi, 21% là nến D1/W1, 20% có nói volume; PV (8 buổi): 6.1 lời nến/buổi, 27% là nến D1/W1, 27% có nói volume.
- 2026-01-07 [00:18:48] [M15] volume "Volume khủng; nhịp trả về không phải lực bán quá …" → "Hiện tại trong khung nhỏ, sau phiên lúc sáng có một cây nến mua lên khá to để đẩy lên. Volume khủng. Đẩy lên sau đó trả về lại. Những nhịp …"
- 2026-01-07 [00:20:58] [M15] volume "Volume mua nhảy vào; điều chỉnh không có volume b…" → "Volume mua nhảy vào nhưng giá điều chỉnh và có rút râu. EMA đi lên, mua đẹp. Nhưng đoạn này vì sao mình không mạnh dạn long ở giá market. B…"
- (gạt đi: fake / trap / quét / chỉ là hồi) 2026-01-06 [00:06:20] [H4]: "Tầm này anh em thấy là nó có một cái cặp H4 đóng xuống. Cây nến 7:00 và sáng ngày hôm nay thì nó đóng một cây nến H4 đỏ xuống."
- (chờ nến đóng xác nhận (nếu/khi đóng … thì …)) 2026-01-06 [00:08:36] [D1]: "Khung ngày như này thì không nên short. Cho đến khi nào có cái nến ngày màu đỏ rồi tính tiếp sau."
- (khác) 2026-01-06 [00:13:00] [M15]: "M5 đang có xu hướng hai đáy và bật lên. Đẹp. Nhưng long đoạn này thì nguy hiểm quá."
- (đọc lực mạnh/yếu, volume) 2026-01-07 [00:17:44] [H4]: "Bởi vì xu hướng H4 ở đây hiện tại đang rất đẹp. Giá đi lên test H4. MA xếp chồng lên nhau, đang tạo thành một đà tăng tốt."
- (xác nhận xu hướng / đảo chiều) 2026-01-07 [00:45:54] [H4]: "H4 này đóng đỏ rồi hả? Đóng đỏ thì khả năng chắc điều chỉnh tiếp. Thực tế H4 cũng không có ý nghĩa nhiều lắm, chủ yếu đoạn này anh em bật 3…"

**Tin tức người đó dùng** (`tin_tuc`, 569 lời ở 174/180 buổi): nguồn lich_kinh_te 196, khac 190, bao 99, ? 75, fedwatch 8, polymarket 1.
- Ảnh hưởng tới view (họ nói): khác / không nêu 251, né / tránh tin, chờ sau tin, đánh nhẹ 138, dùng tin để dự hướng (ra X thì giá Y) 114, không đổi view: tin chỉ hợp lý hoá đường giá / bỏ qua 66.
- Nhắc Polymarket / xác suất lãi suất: 21 lời ở 18 buổi.
- (né / tránh tin, chờ sau tin, đánh nhẹ) 2026-01-06 [00:20:01] [NFP (non farm)]: "Ngày hôm nay thứ ba, ngày mai có tin non farm. Ngày mai có tin non farm nhá mọi người. Non farm về việc làm. Non farm này thì cũng sẽ thay …"
- (khác / không nêu) 2026-01-06 [00:20:36] [CPI Mỹ]: "CPI của Mỹ thì đến tuần sau mới có."
- (không đổi view: tin chỉ hợp lý hoá đường giá / bỏ qua) 2026-01-08 [01:00:29] [Tin WLFI (quỹ của Trump), Trump bắt tổn…]: "Hôm qua có tin thằng đồng sáng lập quỹ WLFI của Trump, hôm trước đánh một coin X4 X5, lần trước là tin Trump bắt tổng thống Maduro của Vene…"
- (dùng tin để dự hướng (ra X thì giá Y)) 2026-01-09 [00:31:51] [Vĩ mô: Fed giảm lãi suất nhưng không bơ…]: "Cộng với đó là động thái lãi suất của FED cũng giảm. FED giảm lãi suất nhưng tiền thì không được bơm ra."

## 4. Mô hình luật NẾU–THÌ (mặc định GIỮ view) — chọn trên tập HỌC, đo trên tập KIỂM
Ứng viên = 47 điều kiện có lời người đó trong TẬP HỌC (≥ 3 buổi) hoặc là hành vi của họ + mọi cặp VÀ (1128 ứng viên): `vh_cham_rau`, `vh_dong_1h4`, `vh_dong_2h4`, `vh_dong_dung_khung`, `vh_dong_d1`, `vh_ben_kia`, `cham_dich`, `cham_chang1`, `vh_dong_vol`, `h4_lon_nguoc`, `h4_lon_nguoc_vol`, `vol_h4_nguoc`, `vol_d1_lon`, `d1_nhan_chim_nguoc`, `d1_cuoi_nguoc`, `thu_hai`, `dau_tuan`, `dau_thang`, `h4_sai_dai34`, `h4_sai_e89`, `h4_sai_e200`, `d1_sai_dai34`, `d1_sai_e89`, `d1_sai_e200`, `rsi_h4_cuc`, `rsi_d1_cuc`, `nguoc_pha_w1`, `chum_h4`, `tin_lon_giua`, `tin_lon_sap24`, `tin_lon_sap48`, `cua_so_fomc`, `pm_moi_truong_nguoc`, `pm_7n_nguoc`, `pm_nguoc`, `truoc_nhac_tin`, `truoc_cho_tin`, `truoc_pv`, `truoc_chac_thap`, `truoc_doi_y`, `truoc_chang1_nguoc`, `tl_pha_nguoc`, `tl_pha_nguoc_h4`, `tl_pha_nguoc_d1`, `tl_pha_nguoc_2nen`, `tl_pha_nguoc_vol`, `tl_pha_thuan`. Hành động: LẬT hoặc PHÂN VÂN. Học tham lam, mỗi luật thêm phải đúng thêm ≥ 2 buổi; tối đa K luật (K ∈ 0..5) chọn bằng kiểm chéo thời gian TRONG tập học.

Số buổi dùng (có view trước + nhãn N): 2026-01: 18, 2026-02: 9, 2026-03: 25, 2026-04: 18, 2026-05: 13, 2026-06: 19, 2026-07: 21, 2026-08: 19, 2026-09: 18, 2026-10: 19

**Chọn họ ứng viên + K bằng kiểm chéo A trong tập học** (mở rộng theo tháng: học T1–T2 thử T3, …, học T1–T5 thử T6; luật phải khớp ≥ 4 buổi chưa bị luật trước bắt và đúng thêm ≥ 2 buổi):

| K | chỉ điều kiện đơn | đơn + cặp VÀ |
|---|---|---|
| 0 | 58/75 = 77% | 58/75 = 77% |
| 1 | 55/75 = 73% | 55/75 = 73% |
| 2 | 55/75 = 73% | 55/75 = 73% |
| 3 | 55/75 = 73% | 55/75 = 73% |
| 4 | 55/75 = 73% | 55/75 = 73% |
| 5 | 55/75 = 73% | 55/75 = 73% |

Chẩn đoán K = 1 (họ đơn): luật số 1 học được ở mỗi lượt và kết quả khi đem thử tháng sau:

- học 01–02: không luật nào đủ điều kiện
- học 01–03: Giá H4 sai phía EMA89 → LẬT · lúc học khớp 10, đúng 6 (giữ view đúng 4) · tháng 04 khớp 5, đúng 1 (giữ view đúng 4)
- học 01–04: Giá H4 ngoài dải EMA34 phía SAI view → LẬT · lúc học khớp 9, đúng 6 (giữ view đúng 3) · tháng 05 khớp 3, đúng 1 (giữ view đúng 2)
- học 01–05: Giá H4 ngoài dải EMA34 phía SAI view → LẬT · lúc học khớp 12, đúng 7 (giữ view đúng 5) · tháng 06 khớp 5, đúng 3 (giữ view đúng 2)
→ **K = 0, họ = đơn** (cao nhất; hoà lấy K nhỏ, họ đơn).

**Kiểm chéo trong tập học, K = 0** (cùng buổi, % trùng nhãn 3 lớp):

| Lượt | n | Bộ luật | Giữ view | Luôn GIẢM | Luật từ trên xuống | Chép buổi trước |
|---|---|---|---|---|---|---|
| A: học 01–02 → thử 03 | 25 | 19/25 = 76% | 19/25 = 76% | 5/25 = 20% | 17/25 = 68% | 19/25 = 76% |
| A: học 01–03 → thử 04 | 18 | 15/18 = 83% | 15/18 = 83% | 5/18 = 28% | 15/18 = 83% | 15/18 = 83% |
| A: học 01–04 → thử 05 | 13 | 11/13 = 85% | 11/13 = 85% | 10/13 = 77% | 8/13 = 62% | 11/13 = 85% |
| A: học 01–05 → thử 06 | 19 | 13/19 = 68% | 13/19 = 68% | 10/19 = 53% | 12/19 = 63% | 13/19 = 68% |
| **A gộp T3–T6** | 75 | 58/75 = 77% | 58/75 = 77% | 30/75 = 40% | 52/75 = 69% | 58/75 = 77% |
| B: học 01–04 → thử 05+06 | 32 | 24/32 = 75% | 24/32 = 75% | 20/32 = 62% | 20/32 = 62% | 24/32 = 75% |
| B: học 01–05 → thử 06 | 19 | 13/19 = 68% | 13/19 = 68% | 10/19 = 53% | 12/19 = 63% | 13/19 = 68% |

- Luật học từ 01–02: (không luật — giữ view)
- Luật học từ 01–03: (không luật — giữ view)
- Luật học từ 01–04: (không luật — giữ view)
- Luật học từ 01–05: (không luật — giữ view)

**Bộ luật KHOÁ** (học trên toàn bộ tập học T1–T6, K = 0):

1. Còn lại: GIỮ view.

**(b) Kiểm theo thời gian: luật chọn trên buổi < 07/01, đo trên buổi ≥ 07/01** (cùng buổi, cùng thước):

| Lượt | n | Bộ luật | Giữ view | Luôn GIẢM | Luật từ trên xuống | Chép buổi trước |
|---|---|---|---|---|---|---|
| Trong mẫu: tập học T1–T6 | 102 | 78/102 = 76% | 78/102 = 76% | 46/102 = 45% | 67/102 = 66% | 77/102 = 75% |
| **Ngoài mẫu: tập kiểm T7–T10** | 77 | 50/77 = 65% | 50/77 = 65% | 49/77 = 64% | 47/77 = 61% | 46/77 = 60% |
|   kiểm 2026-07 | 21 | 13/21 = 62% | 13/21 = 62% | 9/21 = 43% | 14/21 = 67% | 11/21 = 52% |
|   kiểm 2026-08 | 19 | 11/19 = 58% | 11/19 = 58% | 11/19 = 58% | 4/19 = 21% | 11/19 = 58% |
|   kiểm 2026-09 | 18 | 14/18 = 78% | 14/18 = 78% | 15/18 = 83% | 15/18 = 83% | 13/18 = 72% |
|   kiểm 2026-10 | 19 | 12/19 = 63% | 12/19 = 63% | 14/19 = 74% | 14/19 = 74% | 11/19 = 58% |

Tham khảo (KHÔNG khoá): nếu ÉP thêm luật (học trên toàn tập học, họ đơn) rồi đo trên tập kiểm:

- K = 1: Lúc C giá vẫn ở bên kia mốc sai → LẬT → học 80%, kiểm 49/77 = 64% (giữ view kiểm 65%)
- K = 2: Lúc C giá vẫn ở bên kia mốc sai → LẬT → học 80%, kiểm 49/77 = 64% (giữ view kiểm 65%)
- K = 3: Lúc C giá vẫn ở bên kia mốc sai → LẬT → học 80%, kiểm 49/77 = 64% (giữ view kiểm 65%)

Tham khảo (KHÔNG khoá, trong mẫu): cùng thủ tục học trên cả 179 buổi → (không luật — giữ view); trùng 128/179 = 72% vs giữ view 128/179 = 72%.

## 5. Khi nào người đó PHÂN VÂN
8 buổi PHÂN VÂN / 180 buổi có nhãn (học 1, kiểm 7).

| Buổi | N−1 | view | chụm EMA H4 % | H4 vs dải34/89/200 | RSI H4 / D1 | cách EMA89 D1 % | giá đi % | mốc sai buổi trước | tin | Lời cuối buổi |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-01-29 | GIẢM | GIẢM | 1.93 | -1.0/-1.0/-1.0 | 42.7 / 45.6 | -4.98 | -0.83 | — | sau FOMC+khac/trước PPI | [00:11:04] "Thủng khỏi vùng 8700, đóng H4 dưới 87.000 thì chúng ta đánh theo nhịp short. Còn trên 88.00 thì chú…" |
| 2026-07-29 | GIẢM | GIẢM | 0.19 | -1.0/-1.0/-1.0 | 41.2 / 48.4 | -4.65 | 0.76 | — | trước FOMC+GDP+PCE+khac | [00:22:04] "Cực kỳ khó để mà gọi là chọn một cái phe nào. Thực tế là thị trường hiện tại nó cũng không biết là …" |
| 2026-07-30 | GIẢM | GIẢM | 0.13 | 0.0/-1.0/-1.0 | 48.8 / 48.7 | -4.47 | -0.15 | chưa chạm | sau khac/trước GDP+PCE+khac | [00:54:59] "Các bạn cố gắng bám view này thôi. Mình vẫn bám theo view này để chờ sự bứt phá khỏi xu hướng [00:5…" |
| 2026-09-18 | GIẢM | GIẢM | 2.35 | 1.0/1.0/1.0 | 57.1 / 51.0 | 6.6 | 1.05 | chưa chạm | — |  "Có thể tí nữa nó sẽ điều chỉnh trong ngắn hạn, Bitcoin đấy. Nhưng vì cây H4 này nên tạm thời không …" |
| 2026-10-06 | GIẢM | GIẢM | 4.46 | 1.0/1.0/1.0 | 53.2 / 64.5 | 13.03 | -0.39 | chưa chạm | trước khac |  "Tổng quát Bitcoin chỉ có thế: sideway, ta quan sát nó phá 85 hay phá lên khỏi 87." |
| 2026-10-13 | GIẢM | GIẢM | 1.83 | 0.0/-1.0/1.0 | 51.1 / 47.2 | 6.41 | -0.96 | — | sau khac/trước CPI |  "Quay lại thực tế: nến đóng ở đây thì cũng không lạ gì, nhưng tốt nhất đừng sell. Cây nến đóng ác, a…" |
| 2026-10-14 | PHÂN VÂN | GIẢM | 1.72 | 0.0/1.0/1.0 | 53.9 / 52.0 | 7.93 | 0.3 | — | trước CPI+PPI |  "Nếu tối nay ra tin mà thị trường vẫn ở trong vùng này thì tiếp theo vẫn cần ngồi chờ nến xem có phá…" |
| 2026-10-16 | GIẢM | GIẢM | 1.33 | -1.0/-1.0/1.0 | 46.4 / 48.8 | 6.41 | 1.43 | — | sau PPI |  "Hôm nay có vẻ là đói ăn nhá anh em ơi. Mình nghĩ từ giờ đến tối, chắc phải sau 9 giờ tối thị trường…" |

PV so với buổi có hướng (trung vị / tỉ lệ):

| Đặc trưng | PV | Có hướng |
|---|---|---|
| EMA34/89/200 H4 chụm (% giá) | 1.77 | 2.92 |
| RSI H4 | 49.95 | 50.75 |
| RSI D1 | 48.75 | 51.00 |
| Cách EMA89 D1 (%) | 6.41 | -4.06 |
| Giá đi từ C buổi trước (%) | 0.07 | -0.21 |
| Đi ngược view tối đa giữa 2 buổi (%) | 1.17 | 1.35 |
| Giờ từ buổi trước | 24.05 | 24.10 |
| Giá H4 TRONG dải EMA34 | 3/8 = 38% | 30/172 = 17% |
| Giá D1 TRONG dải EMA34 | 5/8 = 62% | 50/172 = 29% |
| EMA34/89/200 H4 chụm < 0,6% giá | 2/8 = 25% | 11/172 = 6% |
| Buổi trước người đó PHÂN VÂN | 1/8 = 12% | 7/171 = 4% |
| Buổi trước người đó nói độ chắc THẤP | 4/8 = 50% | 63/171 = 37% |
| ≥ 1 nến H4 ĐÓNG qua mốc sai buổi trước | 0/3 = 0% | 24/111 = 22% |
| Râu chạm/qua mốc sai buổi trước (chưa cần đóng) | 0/3 = 0% | 33/111 = 30% |
| Râu chạm ĐÍCH chính buổi trước | 2/7 = 29% | 39/164 = 24% |
| Có nến H4 thân ≥ 1,5 ATR NGƯỢC view | 2/8 = 25% | 28/171 = 16% |
| Nến D1 NHẤN CHÌM ngược view | 0/8 = 0% | 20/171 = 12% |
| Có tin lớn trong 24 giờ SAU C (trước tin, thường tối cùng ngày) | 2/8 = 25% | 22/171 = 13% |
| Có tin lớn (FOMC/CPI/NFP) ra GIỮA 2 buổi (sau tin) | 1/8 = 12% | 25/171 = 15% |
| Trong cửa sổ FOMC (≤ 72h trước / ≤ 24h sau quyết định) | 3/8 = 38% | 25/172 = 15% |
| Polymarket kỳ Fed tới ngược view: view TĂNG mà P(tăng lãi suất) ≥ 30%, view GIẢM mà P(giảm) ≥ 30% | 0/8 = 0% | 12/169 = 7% |
| Buổi thứ Hai | 0/8 = 0% | 36/172 = 21% |
| Luật từ trên xuống cho hướng khác view | 0/6 = 0% | 60/160 = 38% |

Buổi PV đến từ TĂNG 0, GIẢM 7, PHÂN VÂN 1; buổi sau PV đi về TĂNG 1, GIẢM 6, PHÂN VÂN 1.

## 6. Độ rộng vùng giá người đó nói (`vung_nguoi_do`)
178 buổi có trường này; bỏ 43 vùng lệch quá xa giá BTC (nghi tài sản khác). Độ rộng = |đến − từ| (1 số = 0); % = so với giá BTC lúc C của buổi.

| Loại | n | Là 1 điểm | Trung vị (giá) | p25–p75 (giá) | Trung vị % | p25–p75 % | Chỉ tính vùng > 0: trung vị giá / % |
|---|---|---|---|---|---|---|---|
| Vào lệnh | 460 | 60% | 0 | 0–1,000 | 0.00% | 0.00–1.11% | 1,000 / 1.30% (n 184) |
| TP | 328 | 75% | 0 | 0–62 | 0.00% | 0.00–0.07% | 1,000 / 1.37% (n 83) |
| SL | 156 | 88% | 0 | 0–0 | 0.00% | 0.00–0.00% | 700 / 1.09% (n 19) |
| Hỗ trợ | 510 | 67% | 0 | 0–1,000 | 0.00% | 0.00–1.12% | 1,000 / 1.30% (n 167) |
| Kháng cự | 500 | 72% | 0 | 0–300 | 0.00% | 0.00–0.45% | 1,000 / 1.31% (n 140) |
| Đích | 698 | 64% | 0 | 0–1,000 | 0.00% | 0.00–1.32% | 1,000 / 1.56% (n 251) |
| vo_hieu | 117 | 82% | 0 | 0–0 | 0.00% | 0.00–0.00% | 1,000 / 1.34% (n 21) |

## 7. Trung hạn (D1/W1): độ bền view, đích ≤ 60 ngày, giữ/đóng lệnh
178 buổi có `view_trung_han`. Đợt = các buổi liền nhau (trong các buổi CÓ nói view khung đó) cùng hướng; buổi không nói khung đó thì bỏ qua, không cắt đợt. Lật = buổi đầu tiên nói hướng khác.

### View D1 — 164 buổi, 66 đợt

| # | Hướng | Từ → đến | Buổi | Ngày | Kết thúc vì (lời buổi lật) |
|---|---|---|---|---|---|
| 1 | TĂNG | 2026-01-06 → 2026-01-16 | 9 | 13 | 2026-01-19 [00:12:11] "Còn đối với xu hướng hiện tại, những nhịp như hiện tại thì nó đang mang tính chất điều chỉnh ở trên khung ngà…" |
| 2 | GIẢM | 2026-01-19 → 2026-02-05 | 13 | 18 | 2026-02-06 [00:10:44] "Hôm nay là đầu tháng thì mình nghĩ chắc sẽ có nhịp hồi thôi. ... Nó sẽ dập lên nhấp xuống rất nhiều vòng rồi …" · nhìn lại [00:14:29]: "Nói chung tinh thần của mình ngày hôm nay từ giờ đến cuối tuần thì lời khuyên của mình đố…" |
| 3 | TĂNG | 2026-02-06 → 2026-03-05 | 6 | 28 | 2026-03-06 [00:06:01] "Đó là đối với D1 bởi vì đây hoàn toàn có thể là một nhịp lên test MA và rụng xuống tiếp, đi tiếp về 50 cho nê…" · đã nói mất view khi: Thủng về dưới 67.000 thì mới tính short |
| 4 | GIẢM | 2026-03-06 → 2026-03-06 | 1 | 3 | 2026-03-09 [00:30:46] "Những cái đáy vẫn liên tục được tạo lên đối với khung ngày. Và anh em thấy đó. Nếu ngày hôm nay nó đóng nến x…" |
| 5 | TĂNG | 2026-03-09 → 2026-03-10 | 2 | 3 | 2026-03-11 [00:43:05] "Có thể nó vẫn chạy cờ giảm nhưng mà cái nhịp này chúng ta ăn cái nhịp hồi lên đây. Ví dụ nó hồi lên đâu đó lo…" · đã nói mất view khi: Trade khung ngày thì SL phải ở 64.000 |
| 6 | GIẢM | 2026-03-11 → 2026-03-11 | 1 | 0 | 2026-03-12 [00:24:40] "Còn TP vùng này thì nếu mà nó break được qua khỏi cái vùng này thì anh em cứ tự tin mà đánh lên 75.000 và 78.…" |
| 7 | TĂNG | 2026-03-12 → 2026-03-19 | 7 | 8 | 2026-03-20 [00:10:42] "Đặc biệt là đối với các lệnh long bởi vì xu hướng ở trên khung ngày vẫn còn đang rất là nguy hiểm. Mình nhắc …" · đã nói mất view khi: Thủng 66–68 thì không giữ target; thủng 65 thì đảo chiều, về downtrend |
| 8 | GIẢM | 2026-03-20 → 2026-03-23 | 3 | 4 | 2026-03-24 [00:28:10] "nhịp tăng này sẽ kết thúc khi nến đóng cửa dưới 65.000, 7% từ giá hiện tại. Và lên thì mình nghĩ sẽ kéo lên đ…" · nhìn lại [00:21:23]: "khi giảm về 70 lại về đúng vùng 67000, trendline hai ngày vừa rồi, lại có tin Trump với I…" · đã nói mất view khi: H4 đóng trên 71k (nhịp giảm là fake breakout, vút lên 74-75k) |
| 9 | TĂNG | 2026-03-24 → 2026-03-26 | 3 | 3 | 2026-03-27 [00:20:00] "Nếu nó gãy qua khỏi cái vùng này thì khả năng là về 53 đợt này. Đợt này khả năng về 53 là dễ nếu nó gãy khỏi …" · nhìn lại [00:18:51]: "Chỉ duy nhất một cái là khác so với ngày hôm qua nhưng mà giống so với tối ngày hôm qua..…" · đã nói mất view khi: gãy 68k → nhịp tăng thất bại, về 57-58k |
| 10 | GIẢM | 2026-03-27 → 2026-03-30 | 2 | 4 | 2026-03-31 [00:29:22] "Cho nên mình nghĩ khả năng để nó lên lại trên này rất cao... Thì nếu lên thì khả năng tiếp tục nó sẽ lên test…" · nhìn lại [00:21:05]: "Hôm qua ở đây nó tạo một H4 hai đáy anh em. H4 hai đáy đi lên thì nhịp này biết đâu được …" · đã nói mất view khi: trụ được Fibo 0.618 / 65-66k hết tuần → còn hy vọng lên 81k/91k |
| 11 | TĂNG | 2026-03-31 → 2026-04-03 | 4 | 6 | 2026-04-06 [00:24:32] "nhịp này nếu nó khùng điên nó có thể đẩy lên đến 82 MA200 ở trên khung ngày. Đây mới thực sự là điểm để bắt đ…" · đã nói mất view khi: thủng 60k (thủng 66k là tín hiệu xấu đầu tiên; đóng ngày 65k/64k thì … |
| 12 | GIẢM | 2026-04-06 → 2026-04-07 | 2 | 2 | 2026-04-08 [00:28:38] "Cho nên mình đang rất kỳ vọng tuần này nó đẩy lên luôn 80. Đối với đi kiểu này thì 80 có khó gì đâu. Mình đan…" |
| 13 | TĂNG | 2026-04-08 → 2026-04-10 | 3 | 5 | 2026-04-13 [00:17:06] "Đối với D1 như này hoàn toàn có khả năng đây chỉ là một cây điều chỉnh. Nó điều chỉnh về đâu? Đây là nhịp tăn…" · đã nói mất view khi: Về lại 66k thì mới cần thay đổi xu hướng khung lớn; giá dao động 72-6… |
| 14 | GIẢM | 2026-04-13 → 2026-04-13 | 1 | 1 | 2026-04-14 [00:34:11] "Từ giờ đến tuần sau kỳ vọng nó sẽ lên được 80." |
| 15 | TĂNG | 2026-04-14 → 2026-04-28 | 8 | 15 | 2026-04-29 [00:28:05] "D1 vẫn đang xấu. Điểm hỗ trợ tiếp theo là 74. Khung ngày như này vẫn xấu, đẹp của khung ngày phải về 74 75 mớ…" · đã nói mất view khi: Thủng 70.000 thì mất xu hướng tăng |
| 16 | GIẢM | 2026-04-29 → 2026-04-29 | 1 | 5 | 2026-05-04 [00:24:58] "Vẫn còn biên độ để cho khung ngày nó còn một nhịp nữa. Hôm nay là ngày thứ hai. Mình dự đoán trong ngày hôm n…" · nhìn lại [00:26:33]: "Cây đầu tháng đã break H4 và đi lên. Vì sao điểm này là một nhịp quan trọng? Bởi vì trước…" · đã nói mất view khi: H4 đóng qua 77.000-77.300 thì qua nhịp điều chỉnh, đánh lên tiếp |
| 17 | TĂNG | 2026-05-04 → 2026-05-06 | 3 | 3 | 2026-05-07 [00:44:28] "Nó là cặp nến đảo chiều nhưng đảo chiều ở đây mới chỉ dừng ở góc độ đảo chiều điều chỉnh thôi chứ không phải …" |
| 18 | GIẢM | 2026-05-07 → 2026-05-07 | 1 | 1 | 2026-05-08 [00:21:36] "Khung ngày mình nói xấu mặc dù xu hướng ở khung ngày vẫn là xu hướng tăng. Cross và giá chẳng qua là nó đang …" · đã nói mất view khi: nến D1 đóng trên MA200 (~82k) → bỏ short, có thể lên 91; mất xu hướng… |
| 19 | TĂNG | 2026-05-08 → 2026-05-12 | 2 | 19 | 2026-05-27 [00:17:13] "Tầm này mà không kéo lên được một cây cực kỳ mạnh để bẻ đường MA này kéo đi lên thì gần như sau đó giá sẽ kéo…" |
| 20 | GIẢM | 2026-05-27 → 2026-06-04 | 6 | 9 | 2026-06-04 [00:36:01] "khả năng tệ cũng phải hồi một nhịp lên đâu đó và H4. Con này thì gãy rồi. Nó phải có một nhịp hồi lên đâu đó …" |
| 21 | TĂNG | 2026-06-04 → 2026-06-04 | 1 | 0 | 2026-06-05 [00:07:36] "vùng này nhận định về nhịp dài ở giá này rất khó, chưa thể hiện cụ thể gì. Chủ yếu phải chờ cây nến ngày hôm …" · nhìn lại [00:07:36]: "Các bạn thấy cụm nến H4 đêm ngày hôm qua là cụm nến nỗ lực cực kỳ. Hai cặp này rất nỗ lực…" |
| 22 | PHÂN VÂN | 2026-06-05 → 2026-06-05 | 1 | 3 | 2026-06-08 [00:21:18] "Cùng lắm nó sẽ hồi lên, test ở trên này. Chúng ta thấy khung ngày vẫn là MA nằm ở 71.000, 70.000 đến 71 thì n…" · đã nói mất view khi: Nến ngày đóng phủ nhận râu 61.000 là xấu |
| 23 | TĂNG | 2026-06-08 → 2026-06-09 | 2 | 2 | 2026-06-10 [00:17:17] "Nến ngày như này chúng ta nhận định là rất xấu. Xác suất có thể quay về đáy. Đáy anh em xác định là vùng 60.0…" · nhìn lại [00:16:13]: "View của ngày hôm qua mình đã nói rất rõ. Hôm thứ hai nó đóng cho chúng ta một cụm nến đả…" |
| 24 | GIẢM | 2026-06-10 → 2026-06-10 | 1 | 1 | 2026-06-11 [00:28:33] "Lệnh này có thể đến khoảng thứ ba tuần sau mới chạm cũng có. Hôm nay mình nói chưa chắc ngày mai các bạn đã n…" · nhìn lại [00:22:02]: "Nhưng trước cái tin hôm qua thì giá đã được cứu và kéo lên cái cây màu xanh này, cây có t…" |
| 25 | TĂNG | 2026-06-11 → 2026-06-23 | 4 | 13 | 2026-06-24 [00:17:29] "Chứ còn hiện tại là xu hướng thị trường rõ ràng là cái xu hướng giảm. Và nhịp này thì mình e rằng các bạn cũn…" · nhìn lại [00:16:26]: "Hôm qua chúng ta ở trong cái phiên live cái vùng 64 này, cái vùng 64 cho đến 63 này là mộ…" · đã nói mất view khi: H4 đóng thủng 63 thì bỏ plan 69; khi đó short theo xu hướng về 50 |
| 26 | GIẢM | 2026-06-24 → 2026-06-29 | 4 | 6 | 2026-06-30 [00:18:39] "Vùng này các bạn cứ cố nhận định nó sẽ lên cũng sai, cố nói giá này sẽ xuống cũng sai. Nếu chúng ta cứ ngồi t…" · đã nói mất view khi: Nến ngày đóng trên 62-63 thì có thể test lại 65 (nhưng xác suất thấp,… |
| 27 | PHÂN VÂN | 2026-06-30 → 2026-06-30 | 1 | 1 | 2026-07-01 [00:21:36] "Xu hướng thị trường chỉ chừng đó thôi. Tất cả những nhịp hiện tại đều là những nhịp hồi thôi. Hồi quang phản …" |
| 28 | GIẢM | 2026-07-01 → 2026-07-02 | 2 | 2 | 2026-07-03 [00:16:16] "Khung ngày hiện tại thể hiện đà tăng rất đẹp. H4 thì break ra khỏi vùng này." · đã nói mất view khi: Giá thoát hẳn khỏi vùng nhạy cảm 59-60 (giống vùng 99-100 trước đây) … |
| 29 | TĂNG | 2026-07-03 → 2026-07-03 | 1 | 3 | 2026-07-06 [01:00:25] "Còn lại nến dài thì cứ chờ thêm khi nào nó confirm gãy, có thể những vùng giá thấp hơn chúng ta sell vẫn dễ ă…" · nhìn lại [00:26:02]: "Vùng 64 đêm qua là vùng mình đã báo cho mọi người trước đó. Vừa MA34 trên khung D1, vừa M…" · đã nói mất view khi: H4 đóng dưới 61 (không long nữa); thủng 60 mới tìm short |
| 30 | GIẢM | 2026-07-06 → 2026-07-14 | 6 | 9 | 2026-07-15 [00:22:31] "nó giữ được ở đây và bẻ ngược trạng thái đi lên, và với cây nến ngày này thì kéo xu hướng thị trường bật tăng…" · nhìn lại [00:22:01]: "Hôm qua chúng ta còn thấy hai đỉnh trên D1, hôm qua còn thấy hai đáy nhưng mình nói rồi, …" · đã nói mất view khi: Về 60 (Fibo 0.618), đóng nến ngày trụ được rồi bật lên thành vai đầu … |
| 31 | TĂNG | 2026-07-15 → 2026-07-22 | 4 | 8 | 2026-07-23 [00:31:39] "Từ giờ đến cuối tuần và khả năng là từ giờ đến lúc FED ra lãi suất, đến ngày 30, thị trường sẽ nhập nhằng tro…" · đã nói mất view khi: H4 đóng dưới đáy 64 thì thị trường mới có xác suất gãy |
| 32 | PHÂN VÂN | 2026-07-23 → 2026-07-23 | 1 | 1 | 2026-07-24 [00:28:25] "Mình đoán là từ giờ đến đó giá nó sẽ lên 72. Có thể nó gãy về 64 63 gì mình không biết nhưng mình đoán từ giờ…" · đã nói mất view khi: Xuống dưới 64 hoặc 63 thì mới gãy xu hướng tăng |
| 33 | TĂNG | 2026-07-24 → 2026-07-27 | 2 | 4 | 2026-07-28 [00:05:21] "Chỉ có duy nhất ở đây chúng ta phải confirm lại với nhau là xu hướng D1 là gãy tăng tạo thành một cái xu hướn…" · nhìn lại [00:03:44]: "Hôm qua cái bạn nào đó bảo cho mình là cái trendline trên này thì nó đã phản ứng ở cái tr…" · đã nói mất view khi: Thủng vào vùng ~63.000 (đáy thứ sáu) mới tính short |
| 34 | GIẢM | 2026-07-28 → 2026-07-28 | 1 | 1 | 2026-07-29 [00:12:07] "Trừ khi là ngày mai chúng ta sẽ có một cái nến đóng trên lại cái đường MA này. Tức là trên cái vùng 64.000 th…" · đã nói mất view khi: Về 62/60 mà khựng lại, chơi vai đầu vai ngược ở đáy bật lên thì 'toan… |
| 35 | PHÂN VÂN | 2026-07-29 → 2026-07-30 | 3 | 2 | 2026-07-31 [00:11:34] "nếu các bạn để ý thì D1 vẫn là xu hướng đang cố đi lên đối với cụm nến ngày như thế này, nhưng 4 giờ thì vẫn …" |
| 36 | TĂNG | 2026-07-31 → 2026-07-31 | 1 | 3 | 2026-08-03 [00:25:47] "Nhịp này thì trước mắt là mình view giá nó có khả năng về test lại vùng 60.000 này. ... Các bạn đừng hỏi về 6…" |
| 37 | GIẢM | 2026-08-03 → 2026-08-03 | 1 | 1 | 2026-08-04 [00:20:21] "D1 thì thực tế đoạn này mình không quan tâm lắm. Nó vẫn đang chủ ở Fibo 0.5 nhưng ở vùng này như lúc nãy mình…" |
| 38 | PHÂN VÂN | 2026-08-04 → 2026-08-05 | 2 | 2 | 2026-08-06 [00:18:28] "Bởi vì như hôm trước mình nói, những động lực để giá lên 70 trở lên là vẫn còn, 70 hoặc 71 hoặc 72" · nhìn lại [00:19:02]: "Hôm trước mình vẫn view cho anh em góc nhìn đi xuống theo Fibo mở rộng này, nhưng hiện tạ…" · đã nói mất view khi: Break D1 lên khỏi 65 → 71–77 (ít nhất 71); không break → fail, tiếp t… |
| 39 | TĂNG | 2026-08-06 → 2026-08-06 | 1 | 1 | 2026-08-07 [00:56:35] "H4 chúng ta cũng xấu, D1 thì cũng xấu. H1 cũng xấu, H4 cũng vậy thôi." · đã nói mất view khi: Gãy lại dưới ~64 → nhịp phá cao (phá giả), short lại; D1 phải lên trê… |
| 40 | GIẢM | 2026-08-07 → 2026-08-07 | 1 | 3 | 2026-08-10 [00:22:16] "Đây là biên hẹp của thị trường nó chạy trong khung ngày D1. Thì rõ ràng là đoạn này, phạm vi cuối cùng của an…" · nhìn lại [00:19:34]: "Mặc dù là đối với mô hình này thì mình không khuyến khích long ở vùng này hôm trước là bở…" · đã nói mất view khi: D1 phá được cản 65 thì mới confirm lên |
| 41 | PHÂN VÂN | 2026-08-10 → 2026-08-11 | 2 | 2 | 2026-08-12 [00:14:00] "Thủng tiếp 62.000 thì tỉ lệ rất cao, trên 80%, nó sẽ về khoảng 55 đến 53. Đó là các cột mốc target trong thán…" · đã nói mất view khi: D1 đóng trên 66.500–67.000 → lên 70–72; test trendline 66 rồi fail → … |
| 42 | GIẢM | 2026-08-12 → 2026-08-14 | 3 | 5 | 2026-08-17 [00:18:20] "Bởi vì về bản chất nó đang đi sideway trong một cái biên rất là to; biên này là biên khung ngày. ... Thoát th…" |
| 43 | PHÂN VÂN | 2026-08-17 → 2026-08-18 | 2 | 3 | 2026-08-20  "Fibo mở rộng cũng cho kết quả khoảng trên 71. Vậy hôm nay các bạn biết khả năng cao giá sẽ đi đến đâu... Nếu …" · nhìn lại : "Hôm trước đã nói rất nhiều lần: khi giá breakout ra khỏi đoạn trendline này thì khả năng …" · đã nói mất view khi: Nến đóng vượt trên 65.000 (đẹp nhất D1; 2-3 cây H4 kéo xa quá thì cắt… |
| 44 | TĂNG | 2026-08-20 → 2026-08-21 | 2 | 5 | 2026-08-25  "Fake out rất hợp lý, từ đây nó mới đi xuống dễ. Mình không đánh giá nhịp này là nhịp tiếp tục con sóng để tăn…" · nhìn lại : "Khi nó đã break ra khỏi 78 thì sẽ đánh lên 79. Sáng hôm qua trên Telegram mình có post pl…" |
| 45 | GIẢM | 2026-08-25 → 2026-08-25 | 1 | 1 | 2026-08-26  "biên độ đi của thị trường từ giờ cho đến hết tuần này và qua hết tháng này, mình nghĩ sẽ không có những biên …" |
| 46 | PHÂN VÂN | 2026-08-26 → 2026-08-26 | 1 | 1 | 2026-08-27  "muốn lên 80 thì cần phải phá qua 79; muốn phá qua được 79 thì cần phải giữ được cái vùng 78.500 này. Muốn lên…" · đã nói mất view khi: nến ngày đóng trên MA 79k (và trên 83k thì long đuổi) |
| 47 | TĂNG | 2026-08-27 → 2026-08-27 | 1 | 1 | 2026-08-28  "Hiện tại nó đã đóng qua rồi, sau rất nhiều ngày nỗ lực. Nhưng đây mới là điều kiện cần của câu chuyện break đ…" · đã nói mất view khi: chưa đóng ngày qua 82-83k thì chưa lên được; thủng 78.5k thì về 77-78k |
| 48 | PHÂN VÂN | 2026-08-28 → 2026-08-28 | 1 | 6 | 2026-09-03  "Với nến ngày, giá vẫn chưa qua được đường MA ở đây và liên tục bị chặn. Tầm này giá sẽ chạy trong biên từ 79 …" |
| 49 | GIẢM | 2026-09-03 → 2026-09-03 | 1 | 1 | 2026-09-04  "Khung ngày đã có một cây nến xanh đóng lên khá ổn, nhưng xét ở RSI thì nó vẫn là phân kỳ khung ngày." · đã nói mất view khi: đóng nến trên 79.000 (khi đó đánh 79 lên 82, qua 83 thì lên 90) |
| 50 | PHÂN VÂN | 2026-09-04 → 2026-09-07 | 2 | 4 | 2026-09-08  "Nhưng nếu về khoảng 77 đến 76 mà vẫn trụ được thì ok, lúc đó RSI cộng với lực bán giảm dần theo thời gian, nó…" · đã nói mất view khi: lên: phá 82-83; xuống: nến ngày phá 78.000 [?] + MA + Fibo nhịp trước |
| 51 | GIẢM | 2026-09-08 → 2026-09-08 | 1 | 7 | 2026-09-15  "Còn nằm trong vùng này thì hai bên đang tranh chấp nhau, chưa rõ thằng nào thắng. Trong này có cả dấu hiệu tố…" · đã nói mất view khi: Về 77-76 mà trụ được, RSI và lực bán giảm dần -> thành vùng tái tích … |
| 52 | PHÂN VÂN | 2026-09-15 → 2026-09-15 | 1 | 1 | 2026-09-16  "Mình sẽ không vào vị thế buy vì nến ngày xấu, chờ xác nhận. Nếu ở đây nó muốn tăng thì cây nến ngày mai sẽ ph…" · đã nói mất view khi: Đóng nến ngày trên 82 → cờ tăng, đuổi 83 lên 92; thủng 76 → 75, 73, 72 |
| 53 | GIẢM | 2026-09-16 → 2026-09-17 | 3 | 2 | 2026-09-18  "Còn nếu thị trường nằm trong vùng từ 77 đến 78 thì sao? Đơn giản thôi, chúng ta không đưa ra quyết định vội, …" · đã nói mất view khi: Xác nhận giảm khi D1 thủng 76.000; qua lại 78k/cụm MA thì may ra lên |
| 54 | PHÂN VÂN | 2026-09-18 → 2026-09-18 | 1 | 3 | 2026-09-21  "Nghiêng cho hai đầu luôn, chưa biết đầu nào. Nhưng xét về trung hạn, tức là trong tuần này, thể nào cũng sẽ c…" · nhìn lại : "Khi nó đóng một cây nến tuần như thế này, trong khi tuần trước đóng một cây nến đỏ, thì c…" · đã nói mất view khi: Giữ trên 78 qua cuối tuần → tuần sau xác suất lên; test thất bại, gia… |
| 55 | GIẢM | 2026-09-21 → 2026-09-21 | 1 | 1 | 2026-09-22  "Kịch bản 1: nếu nến ngày hôm nay trả về lại vùng 82 thì chúng ta xem tiếp liệu 82 83 này có đỡ được nến hay k…" |
| 56 | TĂNG | 2026-09-22 → 2026-09-23 | 2 | 2 | 2026-09-24  "Mình nghĩ từ giờ đến cuối tuần thị trường điều chỉnh luôn là đẹp, hoặc điều chỉnh luôn đến hết tháng cũng đượ…" · nhìn lại : "Mình đã cảnh báo ở bài post trước: kháng cự hiện tại đâu đó khoảng 87.000; nếu muốn chinh…" · đã nói mất view khi: Thủng 85 → xét 82-83; thủng 82 → 80; thủng 80 → view 6x |
| 57 | GIẢM | 2026-09-24 → 2026-10-02 | 4 | 11 | 2026-10-05  "Cộng với đó giá cũng đã test đỉnh, đang test, cho nên khi anh em giao dịch trên vùng này thực sự rất khó. Nếu…" |
| 58 | PHÂN VÂN | 2026-10-05 → 2026-10-06 | 2 | 2 | 2026-10-07 [00:19:46] "Trendline và hỗ trợ cũng đã gãy rồi, và như mình giải thích trước đó vì sao những vùng hỗ trợ trên H4 mình kh…" |
| 59 | GIẢM | 2026-10-07 → 2026-10-13 | 2 | 7 | 2026-10-14 [00:18:24] "Đoạn này anh em đừng vội phán xu hướng quá sớm nha. Cho dù các bạn có view tăng hay giảm, theo đánh giá của m…" · đã nói mất view khi: Giá qua được 83.x (phụ đề '83.00') |
| 60 | PHÂN VÂN | 2026-10-14 → 2026-10-14 | 1 | 1 | 2026-10-15 [00:18:40] "Cho nên bây giờ: D1 điều chỉnh, H4 xu hướng giảm. Không có bất kỳ tín hiệu nào cho thấy xu hướng tăng có khả …" · nhìn lại [00:15:27]: "H4 thì ngày hôm qua đây ngày hôm qua nó lưỡng lự nhá hôm qua ở trên cái phiên live thì mì…" |
| 61 | GIẢM | 2026-10-15 → 2026-10-15 | 1 | 1 | 2026-10-16  "Mình nghĩ trong mấy ngày tới cho đến tuần sau giá sẽ không gãy 80, sẽ đi trong vùng 83 đến 80" · nhìn lại : "Vùng 80 tưởng chừng như D1 đã gãy rồi, cộng với H4 hôm qua cũng gãy, bây giờ nó vẫn đang …" |
| 62 | PHÂN VÂN | 2026-10-16 → 2026-10-16 | 1 | 3 | 2026-10-19  "Giữ được thì vẫn tiếp tục có xu hướng đi lên. Tệ thì cũng test lại vùng 87 [?] này. Xu hướng khung ngày vẫn l…" · nhìn lại : "Vùng này trong những buổi livestream tuần trước mình cũng có nói anh em là xem nó có giữ …" |
| 63 | TĂNG | 2026-10-19 → 2026-10-19 | 1 | 1 | 2026-10-20  "Đoạn này mình thấy xác suất để nó đi xuống sẽ cao hơn xác suất đi lên theo quan điểm cá nhân của mình" · nhìn lại : "Sau nến ngày hôm qua nó lên được 83 không thành công, bị phản ở vùng 83 này. Như hôm qua …" · đã nói mất view khi: Mất 80 (phá đáy tam giác) thì tuột rất nhanh |
| 64 | GIẢM | 2026-10-20 → 2026-10-20 | 1 | 2 | 2026-10-22  "Đối với những mô hình hai đáy như thế này thì xác suất rất là cao nó sẽ lên test lại vùng 86 thì nó mới gãy. …" · nhìn lại : "Nếu sáng hôm nay nó không có những nhịp bán như vậy, ví dụ nó đi sideway đi ngang, thì nh…" · đã nói mất view khi: Nến đóng break lên khỏi biên tam giác (hai cây H4 vượt 83) |
| 65 | TĂNG | 2026-10-22 → 2026-10-22 | 1 | 1 | 2026-10-23  "Nó có thể gãy về 77, 78 nên chúng ta không vào vị thế ở vùng này. Nếu thị trường xảy ra xác suất nó lên 90 th…" · đã nói mất view khi: Đảo chiều luôn ở 83-84 hoặc ở dưới 82 |
| 66 | GIẢM | 2026-10-23 → 2026-10-30 | 7 | 7 (còn chạy) |  |

Đợt D1 đã kết thúc: 65, trung vị 3 ngày (p25 1, p75 5, dài nhất 28); trung vị 2 buổi.

**Đích D1 chạm (râu, H4) trước khi họ bỏ view, ≤ 60 ngày** — 107 đích cùng hướng view (mỗi đích tính 1 lần, từ C buổi đầu nêu): chạm **36/105 = 34%** (2 chưa biết vì hết dữ liệu); thời gian tới đích trung vị 2.5 ngày (p25 0.8, p75 5.0).
- học: chạm 27/70.
- kiểm: chạm 9/37.
- Khoảng cách tới đích lúc nêu: trung vị 5.2% (p25 2.9, p75 10.1).

### View W1 — 120 buổi, 34 đợt

| # | Hướng | Từ → đến | Buổi | Ngày | Kết thúc vì (lời buổi lật) |
|---|---|---|---|---|---|
| 1 | GIẢM | 2026-01-06 → 2026-02-06 | 15 | 41 | 2026-02-16 [00:13:26] "Cái xu hướng ở đây vẫn là xu hướng giảm nhưng cái đoạn này thì rất dễ có một cú hồi nhẹ ở trong khung tuần, n…" · nhìn lại [00:16:12]: "đang có một cái mô hình là đáy cao lên nhưng đỉnh đi bằng. Có nghĩa là gì? Vùng này là lự…" |
| 2 | TĂNG | 2026-02-16 → 2026-02-16 | 1 | 10 | 2026-02-26 [00:33:22] "Có thể vùng 60 cho đến 80 này nó đi trong vòng 3 tháng đến tháng 5 thì nó mới gãy tiếp, từ 80 về đến bốn mấy." · đã nói mất view khi: Sập thủng 60 hoặc lên trên 75 thì phải view lại kế hoạch |
| 3 | GIẢM | 2026-02-26 → 2026-02-26 | 1 | 4 | 2026-03-02 [00:22:36] "Bây giờ điều kiện mình nghĩ là khá đầy đủ để giá phục hồi trong tuần này và những tuần kế tiếp, khoảng 1 đến …" |
| 4 | TĂNG | 2026-03-02 → 2026-03-02 | 1 | 4 | 2026-03-06 [00:12:02] "Dù sao đi nữa chúng ta vẫn biết là trên khung lớn vẫn là lực bán. Những nhịp chúng ta đang long là chúng ta đ…" |
| 5 | GIẢM | 2026-03-06 → 2026-03-13 | 5 | 10 | 2026-03-16 [00:13:47] "Nhưng từ đây lên đến 80 cũng đủ để anh em chúng ta ăn nhịp hồi trong vòng một vài ngày nếu thị trường nó hồi …" · nhìn lại [00:09:39]: "Anh em thấy là chúng ta đã kết thúc một cây nến tuần cực kỳ đẹp. Và như tuần trước thì rõ…" |
| 6 | TĂNG | 2026-03-16 → 2026-03-17 | 3 | 3 | 2026-03-19 [00:56:02] "Xét về khung lớn thì bây giờ có một vùng ở tận 64. Hi vọng nó còn một nhịp đi lên trong ngắn hạn để cho chúng…" |
| 7 | GIẢM | 2026-03-19 → 2026-04-02 | 8 | 15 | 2026-04-03 [01:02:55] "kỳ vọng là qua tuần sau chúng ta sẽ có những cái sự đột phá để nó phá ra khỏi cái vùng giá này. Phá lên hay p…" · nhìn lại [00:30:58]: "hôm qua mình cho các bạn sell short một lệnh nhẹ nhẹ nhưng cây H4 chiều ngày hôm qua nó t…" |
| 8 | PHÂN VÂN | 2026-04-03 → 2026-04-03 | 1 | 3 | 2026-04-06 [00:19:10] "Đoạn này nếu nó giữ được đoạn này mình nghĩ khả năng để nó đi lên lại rất cao. Điểm đầu tiên nó sẽ test lại l…" |
| 9 | TĂNG | 2026-04-06 → 2026-04-06 | 1 | 1 | 2026-04-07 [00:18:36] "khi mà nó gãy xuống dưới này, chúng ta hoàn toàn có thể đánh đuổi theo cái xu hướng giảm về đến cái vùng bốn …" · đã nói mất view khi: nến ngày đóng dưới 66k (khung tuần không giữ 65-66k) |
| 10 | GIẢM | 2026-04-07 → 2026-04-09 | 3 | 3 | 2026-04-10 [01:03:59] "Có khi nào khung tuần này của Bitcoin mà break được, nó lên lại Fibo ở đây, test khoảng 98 99 thì tưng bừng l…" |
| 11 | PHÂN VÂN | 2026-04-10 → 2026-04-10 | 1 | 3 | 2026-04-13 [00:12:20] "Đối với khung tuần thì vẫn có cửa để lên trên. Và cửa này thì vẫn có cơ hội để chúng ta dừng ở 78 80. Mình kh…" |
| 12 | TĂNG | 2026-04-13 → 2026-04-13 | 1 | 1 | 2026-04-14 [00:43:32] "Cho nên góc nhìn đối với khung dài này, ví dụ nó lên được 80 thì sau đó vẫn target là về 50. Sau đó là về 4x." · đã nói mất view khi: H4 đóng dưới 68-67k thì kết thúc nhịp phục hồi |
| 13 | GIẢM | 2026-04-14 → 2026-04-17 | 3 | 6 | 2026-04-20 [00:18:20] "Hai đáy thì khả năng nhịp này mình vẫn thấy tỉ lệ để lên lấp lại khoảng 80 rất cao" |
| 14 | TĂNG | 2026-04-20 → 2026-04-20 | 1 | 1 | 2026-04-21 [00:23:58] "Cho nên nhịp này mình nghĩ dễ có khả năng là đi lên luôn rồi sau đó nó về hẳn luôn dưới bốn mấy 50.000 thì cũ…" |
| 15 | GIẢM | 2026-04-21 → 2026-06-12 | 18 | 55 | 2026-06-15 [00:08:41] "Cây này chẳng qua hồi quang phản chiếu thôi. Cứ để cho nó lên thì chúng ta đã có những cột mốc nó có thể lên …" |
| 16 | TĂNG | 2026-06-15 → 2026-06-15 | 1 | 8 | 2026-06-23 [00:15:01] "Mình đã nhắc mọi người, nó sẽ cứ dập dìu như vậy cho đến hết World Cup, sau đó sẽ pump dump vài phát rồi sập." |
| 17 | GIẢM | 2026-06-23 → 2026-07-03 | 6 | 13 | 2026-07-06 [00:25:30] "Chúng ta biết có khả năng fake, tức là giả vờ đi lên để tiếp tục đi xuống. Tuy nhiên cái đó chúng ta dùng để …" · nhìn lại [00:26:02]: "Vùng 64 đêm qua là vùng mình đã báo cho mọi người trước đó. Vừa MA34 trên khung D1, vừa M…" |
| 18 | PHÂN VÂN | 2026-07-06 → 2026-07-09 | 2 | 7 | 2026-07-13 [00:19:41] "Thứ hai là xu hướng của khung tuần đã confirm rất rõ là downtrend rồi. Nếu chính thức xác nhận điều kiện cần …" · nhìn lại [00:08:31]: "Trước đó chúng ta chờ rất nhiều ngày để xem vùng 64 được break lên. ... Rõ ràng vùng này …" |
| 19 | GIẢM | 2026-07-13 → 2026-07-27 | 7 | 18 | 2026-07-31 [00:12:41] "Về bản chất vì sao nó có trạng thái như vậy là bởi vì chúng ta đang nằm trong sideway của khung lớn, nằm tron…" |
| 20 | PHÂN VÂN | 2026-07-31 → 2026-07-31 | 1 | 3 | 2026-08-03 [00:23:36] "Đối với xu hướng của thị trường trong trước mắt là trong tuần này mình thấy rất xấu thì chúng ta tạm thời bỏ …" |
| 21 | GIẢM | 2026-08-03 → 2026-08-06 | 3 | 7 | 2026-08-10 [00:21:10] "đôi khi nó vẫn là nhịp lên test ví dụ như test 68 test 72 rồi [00:21:41] nó mới gãy xuống là chuyện hết sức b…" · nhìn lại [00:19:34]: "Mặc dù là đối với mô hình này thì mình không khuyến khích long ở vùng này hôm trước là bở…" |
| 22 | TĂNG | 2026-08-10 → 2026-08-10 | 1 | 7 | 2026-08-17 [00:14:12] "những cái nhịp tăng, cho dù từ đây nó có lên đến 70 hay là 73.000 đi nữa, thì đối với quan điểm cá nhân của m…" |
| 23 | GIẢM | 2026-08-17 → 2026-08-26 | 6 | 10 | 2026-08-27  "Qua được 93 phải đến con boss cuối 120? — Đúng. Nhưng con đó mình nghĩ nó chưa xuất hiện trong giai đoạn này …" · đã nói mất view khi: nến tuần đóng qua 93-95k thì downtrend mới có khả năng kết thúc |
| 24 | TĂNG | 2026-08-27 → 2026-08-27 | 1 | 1 | 2026-08-28  "Vẫn có chứ, vẫn có xác suất đó. Nhưng để view tiếp cái plan đó thì mình cần phải thấy là Bitcoin vượt qua đượ…" |
| 25 | GIẢM | 2026-08-28 → 2026-09-04 | 3 | 10 | 2026-09-07  "Một là tăng, hai là đi ngang, hoặc là vòng vòng ở đây, hoặc là đến hết tuần này nó đấm gãy về lại thì qua tuầ…" · nhìn lại : "Nếu cây nến tuần này là một cây màu đỏ thì gần như confirm chắc chắn là nó sẽ tiếp tục đi…" · đã nói mất view khi: Lên trên 93 kéo các MA tuần lên, đỉnh cao hơn (đạt định nghĩa uptrend… |
| 26 | PHÂN VÂN | 2026-09-07 → 2026-09-07 | 1 | 7 | 2026-09-14  "Nến tuần này sẽ gặp hỗ trợ ở đường MA, tức 74.000, hoặc thậm chí khoảng 72–73.000. Đi xuống thì sẽ gặp hỗ trợ…" |
| 27 | GIẢM | 2026-09-14 → 2026-09-18 | 6 | 7 | 2026-09-21  "Nói chung hiện tại trên khung tuần Bitcoin đang thể hiện một gương mặt cực kỳ tươi. Cho nên cứ cố đi cản tàu …" · nhìn lại : "Khi nó đóng một cây nến tuần như thế này, trong khi tuần trước đóng một cây nến đỏ, thì c…" |
| 28 | TĂNG | 2026-09-21 → 2026-09-21 | 1 | 1 | 2026-09-22  "Hiện tại nến đã phá khung tuần nhưng chưa đóng cửa, tức là vẫn chưa xác nhận phá được xu hướng giảm trên khun…" · đã nói mất view khi: Chờ nến tuần qua 83k hoặc 2 nến ngày đóng trên 83k mới xác nhận; quét… |
| 29 | PHÂN VÂN | 2026-09-22 → 2026-09-23 | 2 | 2 | 2026-09-24  "Nhịp 74 chắc phải swing dài thì đúng, tất nhiên phải swing dài; nhưng chưa chắc trong nhịp này nó gãy về 74 l…" · nhìn lại : "Mình đã cảnh báo ở bài post trước: kháng cự hiện tại đâu đó khoảng 87.000; nếu muốn chinh…" |
| 30 | GIẢM | 2026-09-24 → 2026-09-25 | 2 | 4 | 2026-09-28  "Nếu nó giữ được thì chứng tỏ hỗ trợ này trụ được, lúc đó giá mới có cửa đi lên, sau khi nó trụ thì mới hành đ…" |
| 31 | TĂNG | 2026-09-28 → 2026-10-13 | 6 | 17 | 2026-10-15 [00:24:01] "vùng 82 và 83 vừa rồi đã bị gãy, thì cấu trúc trên khung tuần càng ngày càng giảm bớt mức độ uy tín cho con s…" · nhìn lại [00:15:27]: "H4 thì ngày hôm qua đây ngày hôm qua nó lưỡng lự nhá hôm qua ở trên cái phiên live thì mì…" · đã nói mất view khi: Nến tuần không giữ được trên 82.000 |
| 32 | PHÂN VÂN | 2026-10-15 → 2026-10-15 | 1 | 4 | 2026-10-19  "Nếu cứ tiếp tục đà này thì 90 vẫn là một mục tiêu ở trên này nhá. Đối với khung tuần, nó giữ được ở đây thì v…" · nhìn lại : "Vùng này trong những buổi livestream tuần trước mình cũng có nói anh em là xem nó có giữ …" |
| 33 | TĂNG | 2026-10-19 → 2026-10-19 | 1 | 1 | 2026-10-20  "Và cái sideway này sẽ khác với sideway của nhịp tăng trước đó của Bitcoin. Những nhịp trước khi nó tăng lên t…" · nhìn lại : "Sau nến ngày hôm qua nó lên được 83 không thành công, bị phản ở vùng 83 này. Như hôm qua …" |
| 34 | GIẢM | 2026-10-20 → 2026-10-30 | 6 | 10 (còn chạy) |  |

Đợt W1 đã kết thúc: 33, trung vị 6 ngày (p25 3, p75 10, dài nhất 55); trung vị 2 buổi.

**Đích W1 chạm (râu, H4) trước khi họ bỏ view, ≤ 60 ngày** — 69 đích cùng hướng view (mỗi đích tính 1 lần, từ C buổi đầu nêu): chạm **14/68 = 21%** (1 chưa biết vì hết dữ liệu); thời gian tới đích trung vị 15.4 ngày (p25 3.7, p75 23.5).
- học: chạm 13/43.
- kiểm: chạm 1/26.
- Khoảng cách tới đích lúc nêu: trung vị 15.0% (p25 9.6, p75 32.9).

### Giữ / đóng lệnh (`giu_dong`, 810 mục ở 174 buổi)

Quyết định: dong 425, giu 234, chot_mot_phan 123, gong 27, ? 1.

Phân loại theo `khi_nao` (tóm tắt điều kiện họ nói), mỗi mục vào nhóm khớp ĐẦU TIÊN (thứ tự trong bảng).

| Quyết định | Khi nào (nhóm) | Số | % của quyết định | Ví dụ |
|---|---|---|---|---|
| dong | chạm / gần TP, đích, vùng cản; đủ lãi | 271 | 64% | 2026-01-06 [00:05:50] "Không giữ lệnh từ thứ hai sang thứ ba; thứ hai tăng nóng thì chốt lãi trước khi đi ngủ" |
| dong | bị quét SL / cắt lỗ / sai thì cắt | 88 | 21% | 2026-01-08 [00:12:47] "Cắt nếu số lỗ không ảnh hưởng tài chính; chỉ gồng khi đặt trước ngưỡng lỗ chấp nhận (vd -200$) và mục tiêu lã…" |
| dong | nến xấu / gãy cấu trúc / view đổi | 20 | 5% | 2026-01-09 [00:23:13] "Phải thoát trước tin phiên Mỹ; scalping đến trưa hoặc chiều là té" |
| dong | khác | 18 | 4% | 2026-01-21 [00:59:03] "Hy vọng về bờ tối nay hoặc rạng sáng mai thì thoát" |
| dong | kiên nhẫn / chờ / giữ vì chưa có lý do | 17 | 4% | 2026-01-27 [00:37:53] "Không gồng" |
| dong | tin / sự kiện / cuối tuần / qua đêm | 10 | 2% | 2026-01-12 [00:28:02] "Giá test râu → chốt, đừng tham; lệnh có nhiều người theo thì đóng sớm trước tối thứ sáu" |
| dong | dời SL về entry / hoà vốn | 1 | 0% | 2026-07-29 [00:45:18] "Thoát sớm là hợp lý; giữ tới giờ thì âm ngược về hòa vốn" |
| giu | chạm / gần TP, đích, vùng cản; đủ lãi | 122 | 52% | 2026-01-06 [01:03:21] "Giữ nguyên TP đã đặt, không tháo TP; volume nhỏ vì là cản tàu" |
| giu | bị quét SL / cắt lỗ / sai thì cắt | 69 | 29% | 2026-01-07 [00:57:47] "Giữ tới TP 91.3k hoặc SL trên 93k; đánh nhỏ vì đang tranh chấp" |
| giu | kiên nhẫn / chờ / giữ vì chưa có lý do | 19 | 8% | 2026-01-15 [00:02:44] "Giữ tỷ trọng nhỏ 'cầm kỷ niệm'" |
| giu | nến xấu / gãy cấu trúc / view đổi | 13 | 6% | 2026-01-26 [00:50:47] "Lệnh dò nhỏ nên vẫn follow thêm nến rồi tính" |
| giu | khác | 9 | 4% | 2026-03-04 [01:04:13] "Còn bao nhiêu ăn bấy nhiêu, không nhồi thêm vol" |
| giu | tin / sự kiện / cuối tuần / qua đêm | 2 | 1% | 2026-06-15 [00:05:55] "Đã dặn giữ đến thứ hai" |
| chot_mot_phan | chạm / gần TP, đích, vùng cản; đủ lãi | 96 | 78% | 2026-01-06 [00:09:44] "Giá vào vùng 96-98 (lực yếu dần) thì chốt hoặc chốt bớt một phần" |
| chot_mot_phan | bị quét SL / cắt lỗ / sai thì cắt | 21 | 17% | 2026-01-14 [00:24:35] "TP1 hoặc kéo SL về entry ở vùng Fibo; chốt phần còn lại ~96.500" |
| chot_mot_phan | kiên nhẫn / chờ / giữ vì chưa có lý do | 3 | 2% | 2026-02-26 [00:39:39] "Đã chốt bớt sáng nay" |
| chot_mot_phan | khác | 2 | 2% | 2026-08-04 [00:06:54] "Cứ ăn nho nhỏ, không ăn to" |
| chot_mot_phan | nến xấu / gãy cấu trúc / view đổi | 1 | 1% | 2026-05-12 [00:35:34] "hiện tại nên chốt bớt" |
| gong | bị quét SL / cắt lỗ / sai thì cắt | 19 | 70% | 2026-01-07 [00:26:53] "Chỉ gồng khi dời SL về entry; về entry thì cắt hòa, tuyệt đối không gồng lỗ, không chuyển từ lướt sang gồng" |
| gong | chạm / gần TP, đích, vùng cản; đủ lãi | 8 | 30% | 2026-01-16 [00:16:28] "Nếu giá lên vùng liquid 97 mà lực mạnh quá thì cắt sớm (có thể lên 98); lực yếu thì gồng tiếp" |
| ? | nến xấu / gãy cấu trúc / view đổi | 1 | 100% | 2026-08-17 [00:23:05] "Ông nói hợp lý lúc vào nhưng nay đã bể xu hướng đó; không nói rõ đóng hay giữ" |

- Đóng/chốt ở buổi họ đổi view H4 (LẬT/PV): 146/548 = 27% lần đóng; tỉ lệ buổi đổi view trong mọi buổi có `giu_dong`: 28%.

## 8. Fed / lãi suất kỳ tới (Polymarket, cửa sổ FOMC) và view của người đó
Đặc trưng nhân quả tại C: kỳ FOMC KẾ TIẾP sau C; P(tăng)/P(giảm) lãi suất = Polymarket 'Fed decision in <tháng>' (chuẩn hoá tổng các kết quả = 100%, mốc giờ ≤ C); thay đổi 3/7 ngày cùng kỳ họp; cửa sổ FOMC = ≤ 72h trước / ≤ 24h sau quyết định; kỳ gần nhất + phiếu phản đối từ `du_lieu/tin_tuc/fomc_ket_qua_2026.csv`. Cột hướng = nhãn H4 cuối buổi N; D1 = view D1 trong `view_trung_han`.

**Theo P(TĂNG lãi suất) kỳ tới:**

| P(tăng) kỳ tới | Buổi (học/kiểm) | H4: TĂNG | GIẢM | PV | View D1: TĂNG / GIẢM | LẬT (so view) | P(tăng) trung vị |
|---|---|---|---|---|---|---|---|
| < 30% | 134 (96/38) | 47% | 49% | 4% | 60 / 52 | 25% | 1% |
| 30–70% | 37 (4/33) | 30% | 65% | 5% | 8 / 15 | 27% | 49% |
| > 70% | 6 (0/6) | 0% | 100% | 0% | 0 / 4 | 0% | 79% |
| không có dữ liệu | 3 | 100% | 0% | 0% | 2 / 1 | 0% | — |

**Theo thay đổi 7 ngày của P(tăng lãi suất) kỳ tới:**

| ΔP(tăng) 7 ngày | Buổi | H4: TĂNG | GIẢM | PV |
|---|---|---|---|---|
| tăng ≥ 10 điểm (diều hâu hơn) | 25 | 36% | 60% | 4% |
| −10…+10 | 128 | 42% | 53% | 5% |
| giảm ≥ 10 điểm (bồ câu hơn) | 23 | 43% | 52% | 4% |

**Trong vs ngoài cửa sổ FOMC:**

| | Buổi | H4: TĂNG | GIẢM | PV | LẬT (so view) | Đổi giữa buổi |
|---|---|---|---|---|---|---|
| Trong cửa sổ (≤ 72h trước / ≤ 24h sau) | 28 | 25% | 64% | 11% | 7% | 0% |
| Ngoài cửa sổ | 152 | 46% | 51% | 3% | 27% | 6% |

**Theo kỳ FOMC gần nhất trước C:**

| Kỳ gần nhất | Buổi | H4: TĂNG | GIẢM | PV |
|---|---|---|---|---|
| giữ nguyên, có phiếu muốn GIẢM lãi suất | 79 | 59% | 39% | 1% |
| giữ nguyên, có phiếu muốn TĂNG lãi suất | 32 | 25% | 72% | 3% |
| giữ nguyên, không phiếu phản đối theo hướng nào | 25 | 48% | 48% | 4% |
| TĂNG lãi suất | 27 | 11% | 70% | 19% |

**Lời người đó về Fed / lãi suất** (`tin_tuc`, 170 lời ở 104 buổi), theo nhóm P(tăng) kỳ tới của buổi đó:

- P(tăng) < 30%: 102 lời (trung tính / né 48, nghiêng GIẢM 41, nghiêng TĂNG 13; nghiêng theo từ khoá trong lời).
  - 2026-04-28 [00:46:27] [FOMC lãi suất] (H4 cuối buổi GIẢM): "Xem thử dự đoán lãi suất bao nhiêu phần trăm. Một ngày nữa, hiện tại là duy trì lãi suất. Duy trì lãi suất tức là không tăng không giảm lên đến 100% …" → Giữ nguyên là tín hiệu tốt: có thể tăng nhẹ sau tin rồi ~1 ngày sau dump theo bài phát bi…
  - 2026-01-27 [00:34:27] [FOMC (lãi suất)] (H4 cuối buổi GIẢM): "Khả năng là thị trường sẽ nhập nhằng cho đến ngày ra tin lãi suất. Khi gần ra tin lãi suất thì các bạn để ý, nếu trước tin nó chạy theo hướng nào thì…" → Thị trường nhập nhằng tới ngày ra tin; trước tin chạy hướng nào thì sau tin vài ngày thườ…
- P(tăng) 30–70%: 47 lời (nghiêng GIẢM 21, trung tính / né 14, nghiêng TĂNG 12; nghiêng theo từ khoá trong lời).
  - 2026-08-12 [00:27:14] [Lo ngại Fed tăng lãi suất tháng sau] (H4 cuối buổi GIẢM): "Tin CPI này là tin quan trọng nhất từ giờ đến ngày 19, và gần như đến hết tháng. Từ đầu tháng đến giờ thị trường chỉ chờ tin này, vì thị trường đang …" → Thị trường chờ CPI vì sợ Fed tăng lãi suất; ông nghĩ không có kịch bản tăng lãi suất, như…
  - 2026-07-29 [00:33:23] [Kết quả: FED giữ nguyên lãi suất 3.75] (H4 cuối buổi GIẢM): "Thị trường tăng rồi. Giữ nguyên lãi suất là chắc luôn. 3.75. ... Giữ nguyên lãi này thì nó đâu có tạo ra được cái sự hưng phấn bền vững. Phải giảm lã…" → Không phải tin tốt; giá tăng vì thị trường bị dọa rồi được giải tỏa tâm lý; giữ nguyên ch…
- P(tăng) > 70%: 20 lời (nghiêng GIẢM 13, nghiêng TĂNG 5, trung tính / né 2; nghiêng theo từ khoá trong lời).
  - 2026-09-14  [FOMC lãi suất] (H4 cuối buổi GIẢM): "Tuần này là tin lãi suất của Fed: đêm thứ tư 16, rạng sáng ngày 17. Thị trường đã dồn lực review và dự đoán lên đợt lãi suất này; trên các trang dự đ…" → Tăng thì đã được dự đoán: đạp xuống ngắn hạn rồi kéo lên rồi trả về bản chất (giảm); khôn…
  - 2026-09-16  [FOMC lãi suất + phát biểu chủ tịch Fed mới] (H4 cuối buổi GIẢM): "Tối nay 1:00 sáng chúng ta có tin quan trọng nhất của tháng 9: lãi suất của Fed; 1:30 chủ tịch mới [?] phát biểu quan điểm. Thị trường gần như 89,5% …" → Ván bài lật ngửa; quan trọng là phần phát biểu. Giá trước tin quyết định sau tin: phiên M…
- P(tăng) không có dữ liệu: 1 lời (nghiêng GIẢM 1; nghiêng theo từ khoá trong lời).
  - 2026-04-06 [00:39:07] [khả năng FED tăng lãi suất / không bơm tiền 2026] (H4 cuối buổi TĂNG): "Năm 2026 chắc chắn không phải là một năm để thị trường nó bơm tiền và nó kích hoạt tăng giá... Đây là tổng thị trường chứng khoán Dow Jones. Đây là đ…" → 2026 không phải năm bơm tiền kích giá; ủng hộ view dài hạn giảm

