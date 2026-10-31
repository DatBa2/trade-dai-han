# Sổ đối chiếu: bot vs người đó vs giá thật

Mỗi nhận định của bot một dòng. Cột "người đó" điền từ phiếu buổi live kế tiếp; cột "giá thật" điền khi hết hạn.
Thước đo CHÍNH = giống người đó. Giá thật là phụ.

| Bot ra lúc | Bot H4 | Đích / hạn | Người đó (buổi sau) | Giống? | Giá thật hết hạn | Ghi chú |
|---|---|---|---|---|---|---|
| 29/10 22:54 (coi như nến 19:00 đóng ở 81.705; đóng thật 81.776) | GIẢM thấp, quét 82.500 → 80.500 | 80.500 / 24h (tới 22:54 30/10) | qua đêm vẫn giữ lệnh sale (chốt 80% sáng 30/10), view 24/10 "về 77–78K cuối tháng" ĐÚNG; 30/10 H4 PHÂN VÂN chơi 2 đầu | ✅ hướng · ⚠ đích bot nông (80.5 vs 77–78) | GIẢM −5,1%, chạm 80.500 lúc 03:00, không quét 82.500 | file `nhan_dinh_bot/2026-10-29_2300.json` |
| 29/10 23:05 · **ETH** 2.367 | GIẢM vừa, hồi 2.395 → 2.300 | 2.300 / 24h | GIẢM, về 2.100–2.200, thủng 2.300 | ✅ hướng · ⚠ đích bot nông | −5,4%, chạm 2.300 lúc 03:30, thấp 2.174 | `nhan_dinh_bot/2026-10-29_2300_alt.json` |
| 29/10 23:05 · **ZEC** 1.361 | TĂNG thấp, về 1.330 → 1.400 | 1.400 / 24h | không nhắc ZEC | — | −9%, chạm mốc sai, thấp 1.182 | `nhan_dinh_bot/2026-10-29_2300_alt.json` · 23:10 lên thẳng 1.398, sai chặng 1 |
| 29/10 23:11 · **ZEC** cập nhật 1.390 | TĂNG thấp, về 1.358 → 1.484 | 1.484 / 24h | không nhắc ZEC | — | −9%, sai | `nhan_dinh_bot/2026-10-29_2311_cap_nhat_va_doc_lap.json` |
| 29/10 23:18 · **NEAR** 4.625 | GIẢM vừa, hồi 4.80 → 4.30 | 4.30 / 24h | GIẢM, chạm mốc 3.89–3.91 "xong việc rồi" | ✅ hướng · ⚠ đích bot nông | −5,5%, chạm 4.30 lúc 03:30, thấp 3.906 | `nhan_dinh_bot/2026-10-29_2318_NEAR.json` |
| 30/10 23:45 · **BTC** 77.425 (thứ Sáu) | GIẢM vừa, hồi 78.600 → 75.000 (TP1 76.300) | 75.000 / hết cuối tuần | chờ live 02/11 | | | `nhan_dinh_bot/2026-10-30_2345.json` · lần đầu dùng sổ tay + 2 luật sửa |
| 30/10 23:45 · **ETH** 2.233 | GIẢM vừa, hồi 2.300 → 2.150 | 2.150 / hết cuối tuần | chờ live 02/11 | | | |
| 30/10 23:45 · **NEAR** 4,309 | PHÂN VÂN (đích 3,9 đã xong; chờ hồi 4,42–4,60 mới tìm short) | — | chờ live 02/11 | | | |
| 30/10 23:45 · **ZEC** 1.236 | PHÂN VÂN (EMA H4 chụm 1.233–1.284) | — | chờ live 02/11 | | | |

## Nhận định độc lập của Claude (không bắt chước — để so xem ai sát giá hơn)

| Lúc | Coin | Hướng | Đích / hạn | Sai khi | Giá thật hết hạn |
|---|---|---|---|---|---|
| 29/10 23:11 | BTC 81.857 | TĂNG thấp | 82.500 / 24h | H4 đóng dưới 81.000 | ❌ chạm mốc sai 00:00, −5% |
| 29/10 23:11 | ETH 2.374 | TĂNG thấp | 2.400 / 24h | H4 đóng dưới 2.340 | ❌ −5,4% |
| 29/10 23:11 | ZEC 1.390 | TĂNG vừa | 1.450 / 24h | H4 đóng dưới 1.330 | ❌ −9% |
| 29/10 23:18 | NEAR 4.625 | GIẢM thấp | 4.45 / 24h | H4 đóng trên 4.82 | ✅ chạm 01:30 |
| 30/10 23:45 | BTC 77.425 | GIẢM thấp | 76.000 / 48h | H4 đóng trên 79.000 | |
| 30/10 23:45 | ETH 2.233 | GIẢM vừa | 2.170 / 48h | H4 đóng trên 2.345 | |
| 30/10 23:45 | NEAR 4,309 | TĂNG thấp | 4,42 / 48h | H4 đóng dưới 4,12 | |
| 30/10 23:45 | ZEC 1.236 | PHÂN VÂN | — | — | |

## Sổ sai
Mỗi lần bot sai — **lệch người đó HOẶC sai giá thật** — ghi vì sao + đã sửa gì. **Cả hai cùng sai giá → vẫn phải học để
sửa bot** (sổ tay / bộ não số), không chỉ ghi lại — theo `DESIGN.md` mục "Sổ sai" (dòng 51–53). *(Sửa 31/10 theo P1-8; bản
cũ ghi "Cả hai cùng sai giá → chỉ ghi, không sửa", trái yêu cầu user.)*

**Phân loại lỗi** (mỗi dòng ghi 1 loại chính, có thể kèm loại phụ):

| Loại | Khi nào | Sửa ở đâu |
|---|---|---|
| `RUT_NHAN` — rút nhãn | phiếu / mốc / đáp án rút sai lời người đó (sai hướng, sai tài sản, sai số, sai giờ, lấy nhầm kịch bản phụ) | phiếu, `moc/`, quy tắc rút |
| `BAT_CHUOC` — bắt chước | dữ liệu đầu vào đúng nhưng bot khác người đó (hướng / đích / mốc sai / lệnh / lý do) | sổ tay, luật bot |
| `DU_BAO` — dự báo thị trường | bot sai so với giá thật (chạm SL / mốc sai trước đích, hết hạn không chạm) — **kể cả khi người đó cũng sai** | luật bot, sổ tay (ghi rõ "khác người đó có chủ đích") |
| `THUC_THI` — thực thi | ý đúng nhưng khâu chạy lỗi: nến chưa đóng, sai giờ cắt dữ liệu, limit không khớp, lịch chạy không chạy, lỗi script / dữ liệu | công cụ, lịch chạy, đầu vào |

**Mỗi lần sửa bắt buộc có:** (1) **phiên bản** (tên luật + số phiên bản / ngày, hoặc hash file sổ tay / commit);
(2) **bằng chứng đã xảy ra** (file nhận định, giá thật, câu trích người đó); (3) **kiểm trên buổi MỚI** sau ngày sửa — không
chấm lại chính các buổi đã dùng để rút luật, không dùng giá tương lai làm đầu vào cho nhận định quá khứ. Chưa kiểm thì ghi
"chưa kiểm", không coi là đã sửa xong.

| Ngày | Loại lỗi | Bot nói | Người đó nói | Sai ở đâu | Vì sao | Đã sửa (phiên bản) | Bằng chứng | Kiểm trên buổi mới |
|---|---|---|---|---|---|---|---|---|
| 29/10 23:10 | `DU_BAO` | ZEC về 1.330 rồi lên 1.400 | (chưa có) | chặng 1 sai: giá lên thẳng 1.398 | bot áp luật "chờ RSI hạ, về test râu" nhưng không tính short squeeze (long/short 0,55, thanh lý short lớn) | thêm phái sinh vào đầu vào bot; với coin bị đông short thì không giả định có nhịp chỉnh trước (30/10, chưa gắn số phiên bản) | `nhan_dinh_bot/2026-10-29_2300_alt.json`; giá thật −9%, chạm mốc sai | chưa kiểm |
| 30/10 | `BAT_CHUOC` (+ `DU_BAO`: đích nông) | BTC: thấy H4 xanh trên cụm MA → coi view sáng bị vô hiệu, hạ đích 77–78K xuống 80.500 | vẫn giữ lệnh sale qua đêm, đích 77–78K giữ nguyên (và đúng) | đích nông, áp luật vô hiệu quá sớm | bot lấy mốc vô hiệu của khung nhỏ (buổi 10:05) thay vì mốc khung lớn người đó đặt 28/10 (H4 đóng trên 82.000 / D1 trên 81.500–82.000) | luật bot: vô hiệu = mốc CHẶT NHẤT của khung lớn trong các buổi gần đây; chưa chạm thì GIỮ đích cũ của người đó (30/10, chưa gắn số phiên bản) | `nhan_dinh_bot/2026-10-29_2300.json`; phiếu 30/10; giá thật −5,1% | áp dụng lần đầu ở nhận định 30/10 23:45 — chờ live 02/11 |
| 30/10 | `BAT_CHUOC` | ETH 2.300, NEAR 4.30 | ETH 2.100–2.200, NEAR 3.89–3.91 | đích nông ở cả 3 coin | bot tự chọn hỗ trợ gần nhất làm đích thay vì đích người đó đã nêu | luật bot: đích = đích người đó nêu gần nhất (phiếu), hỗ trợ gần chỉ làm TP1 (30/10, chưa gắn số phiên bản) | `nhan_dinh_bot/2026-10-29_2300_alt.json`, `…_2318_NEAR.json` | áp dụng lần đầu ở nhận định 30/10 23:45 — chờ live 02/11 |

## Lệnh giấy (mô phỏng, vốn giả định 1.000$) — `nhan_dinh_bot/lenh_2026-10-31_0010.json`
| Đặt lúc | Lệnh | Vào | SL | TP (50% / 50%) | Đòn bẩy · rủi ro | Kết quả |
|---|---|---|---|---|---|---|
| 31/10 00:10 | BTC SHORT limit 2 tầng | 78.450 / 78.750 (TB 78.600) | 79.650 | 76.250 / 75.200 | x20 · 20$ (2%) | |
| 31/10 00:10 | ETH SHORT limit 2 tầng | 2.290 / 2.305 (TB 2.297,5) | 2.360 | 2.185 / 2.120 | x20 · 10$ (1%) | |
| 31/10 00:10 | BTC LONG 75K — KHÔNG đặt (R:R tới TP1 chỉ 1,0) | (75.050 / 75.350) | (74.150) | (76.250 / 77.700) | — | |
| 31/10 00:15 · **bản x2, vốn 4.000$** (user yêu cầu) | BTC SHORT 0,0762 + 0,0762 BTC | 78.450 / 78.750 | 79.650 | 76.250 / 75.200 | x20 · 160$ (4%) · ký quỹ 599$ | |
| 31/10 00:15 · bản x2, vốn 4.000$ | ETH SHORT 0,64 + 0,64 ETH | 2.290 / 2.305 | 2.360 | 2.185 / 2.120 | x20 · 80$ (2%) · ký quỹ 147$ | |
