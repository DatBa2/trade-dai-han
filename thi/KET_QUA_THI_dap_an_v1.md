# Kết quả thi bot v3 (bộ chấm sau sửa P0 — thi/SUA_P0.md)
Chấm lúc 2026-10-31 10:47 VN · bài làm: `/Users/badat/linhtinh/trade_dai_han/thi/bai_lam` · đáp án: `/Users/badat/linhtinh/trade_dai_han/phieu` · 77/77 buổi thi có bài làm · nến 5m có tới 2026-10-31 10:25 VN
Quy ước: mốc cắt C = lúc KẾT THÚC live (giờ thật từ transcripts/gio_live.tsv; thiếu thì giờ không chắc). Bot chỉ thấy dữ liệu trước C; nhãn so sánh = view H4 (không có thì 'chung') CUỐI buổi của người đó. Mọi cách đoán chấm trên CÙNG tập buổi, cùng thước; chấm theo thị trường đều tính từ C (giá tham chiếu = close nến 5m cuối đã đóng ≤ C; nến 5m chứa C bị bỏ → khoảng trống < 5 phút sau C không chấm).
Tập so hướng (mẫu số khoá): **76/77** buổi thi có nhãn người đó hợp lệ · bị loại 1: 2026-08-27_1006_ZJ5BVqdLJeE (phiếu người đó không có nhãn H4/chung hợp lệ).
Độ phủ bot trên 76 buổi: có bài làm **76/76** · nhãn H4/chung hợp lệ **76/76** — buổi thiếu bài hoặc nhãn không hợp lệ được TÍNH SAI (không loại khỏi mẫu số).

## 1. Trùng hướng H4 với người đó (cùng 76 buổi, cùng mẫu số)
Người đó: TĂNG 16 · GIẢM 44 · PHÂN VÂN 16 — Bot: TĂNG 25 · GIẢM 38 · PHÂN VÂN 13 · thiếu/không hợp lệ 0
| Cách đoán | Thiếu nhãn (tính sai) | Độ chính xác 3 nhãn | KTC 95% (bootstrap khối 18 tuần ISO) | Chênh bot − cách này (KTC 95% cặp, khối tuần) | Macro-F1 | Balanced acc. | Khi cả 2 có hướng | Kappa | McNemar bot vs mốc (bot đúng–mốc sai / ngược lại, p) |
|---|---|---|---|---|---|---|---|---|---|
| Bot | 0 | **43/76 = 57%** | 42% – 70% | — | 0.51 | 0.52 | 37/53 = 70% | 0.28 | — |
| Luôn GIẢM | 0 | **44/76 = 58%** | 45% – 70% | -1 điểm % (-17 – +16 điểm %) | 0.24 | 0.33 | 44/60 = 73% | 0.00 | 15 / 16, p = 1.000 |
| Chép buổi trước | 1 | **39/76 = 51%** | 38% – 65% | +5 điểm % (-4 – +14 điểm %) | 0.43 | 0.43 | 35/49 = 71% | 0.15 | 10 / 6, p = 0.454 |
| Giữ view | 0 | **42/76 = 55%** | 43% – 67% | +1 điểm % (-9 – +11 điểm %) | 0.37 | 0.41 | 42/60 = 70% | 0.12 | 11 / 10, p = 1.000 |
| Luật từ trên xuống | 0 | **44/76 = 58%** | 45% – 72% | -1 điểm % (-14 – +12 điểm %) | 0.52 | 0.53 | 40/52 = 77% | 0.27 | 14 / 15, p = 1.000 |
_Chỉ số chính = độ chính xác 3 nhãn trên toàn tập. Kết luận bot hơn/kém một mốc chỉ khi KTC của CHÊNH LỆCH CẶP không chứa 0 — không so hai khoảng tỷ lệ riêng. Bootstrap khối tuần giữ phụ thuộc giữa các buổi cùng tuần (view kéo dài, nhiều phiên/ngày). Chép buổi trước = nguyên nhãn buổi liền trước; Giữ view = hướng TĂNG/GIẢM gần nhất của người đó (bỏ qua buổi PHÂN VÂN)._

### Bảng chéo (dòng = người đó, cột = bot)
| | TĂNG | GIẢM | PHÂN VÂN | Thiếu/không hợp lệ | Tổng |
|---|---|---|---|---|---|
| **TĂNG** | 9 | 4 | 3 | 0 | 16 |
| **GIẢM** | 12 | 28 | 4 | 0 | 44 |
| **PHÂN VÂN** | 4 | 6 | 6 | 0 | 16 |
| Tổng | 25 | 38 | 13 | 0 | 76 |

### Theo nhóm buổi (độ chính xác 3 nhãn)
| Nhóm | Số buổi | Bot | Luôn GIẢM | Chép buổi trước | Giữ view | Luật từ trên xuống |
|---|---|---|---|---|---|---|
| Live sáng (06–14h VN) | 73 | 41/73 = 56% | 41/73 = 56% | 37/73 = 51% | 39/73 = 53% | 42/73 = 58% |
| Live tối/đêm | 3 | 2/3 = 67% | 3/3 = 100% | 2/3 = 67% | 3/3 = 100% | 2/3 = 67% |
| Giờ live thật | 76 | 43/76 = 57% | 44/76 = 58% | 39/76 = 51% | 42/76 = 55% | 44/76 = 58% |

## 2. PHÂN VÂN (chấm riêng)
| Trường hợp | Số buổi |
|---|---|
| Bot PHÂN VÂN khi người đó PHÂN VÂN (đúng) | 6 |
| Bot PHÂN VÂN khi người đó có hướng (bỏ lỡ) | 7 |
| Bot có hướng khi người đó PHÂN VÂN (ép hướng) | 10 |
| Bot thiếu nhãn khi người đó PHÂN VÂN | 0 |
| Độ chính xác khi bot nói PHÂN VÂN | 6/13 = 46% |
| Bắt được PHÂN VÂN của người đó | 6/16 = 38% |

## 3. Giữ view: đợt view và thời điểm đổi view
Người đó có **38 đợt view** trên 76 buổi (đợt = chuỗi buổi liên tiếp cùng nhãn), **37 lần đổi view** (tính cả lần đổi ở buổi đầu so với buổi ngay trước kỳ thi).
| Cách đoán | Bắt đúng lúc đổi (lệch ≤ 1 buổi) | Cùng buổi | Sớm 1 buổi | Trễ 1 buổi |
|---|---|---|---|---|
| Bot | 25/37 = 68% | 7 | 7 | 11 |
| Luôn GIẢM | 0/37 = 0% | 0 | 0 | 0 |
| Chép buổi trước | 35/37 = 95% | 0 | 6 | 29 |
| Giữ view | 21/37 = 57% | 0 | 3 | 18 |
| Luật từ trên xuống | 9/37 = 24% | 5 | 4 | 0 |
_Lưu ý: 'Chép buổi trước' luôn trễ đúng 1 buổi nên bắt được gần hết theo tiêu chí ±1; xem cột 'Cùng buổi'._

Các đợt view của người đó:
| Từ buổi | Đến buổi | Nhãn | Số buổi | Bot cùng nhãn trong đợt |
|---|---|---|---|---|
| 2026-07-01_WNiQ | 2026-07-01_WNiQ | GIẢM | 1 | 1/1 |
| 2026-07-02_w4bv | 2026-07-02_w4bv | PHÂN VÂN | 1 | 0/1 |
| 2026-07-03_IV0M | 2026-07-03_IV0M | TĂNG | 1 | 1/1 |
| 2026-07-06_GRWl | 2026-07-09_Fmb8 | GIẢM | 3 | 2/3 |
| 2026-07-10_QwYz | 2026-07-10_QwYz | TĂNG | 1 | 0/1 |
| 2026-07-13_O3q2 | 2026-07-14_gpyn | GIẢM | 2 | 1/2 |
| 2026-07-15_-T8W | 2026-07-27_YMlD | TĂNG | 7 | 7/7 |
| 2026-07-28_1wDQ | 2026-07-28_1wDQ | GIẢM | 1 | 0/1 |
| 2026-07-29_2FMm | 2026-07-29_2FMm | PHÂN VÂN | 1 | 1/1 |
| 2026-07-29__TlY | 2026-07-29__TlY | GIẢM | 1 | 0/1 |
| 2026-07-30_qBG2 | 2026-07-30_qBG2 | PHÂN VÂN | 1 | 0/1 |
| 2026-07-31_SlGy | 2026-08-05_uw4Q | GIẢM | 4 | 3/4 |
| 2026-08-06__Ypb | 2026-08-06__Ypb | TĂNG | 1 | 0/1 |
| 2026-08-07_N-7X | 2026-08-07_N-7X | PHÂN VÂN | 1 | 1/1 |
| 2026-08-10_1001 | 2026-08-10_1001 | TĂNG | 1 | 0/1 |
| 2026-08-11_1005 | 2026-08-11_1005 | PHÂN VÂN | 1 | 0/1 |
| 2026-08-12_1003 | 2026-08-14_1004 | GIẢM | 3 | 2/3 |
| 2026-08-17_1006 | 2026-08-17_1006 | TĂNG | 1 | 0/1 |
| 2026-08-18_0957 | 2026-08-19_1001 | GIẢM | 2 | 1/2 |
| 2026-08-20_1003 | 2026-08-20_1003 | PHÂN VÂN | 1 | 0/1 |
| 2026-08-21_1003 | 2026-08-21_1003 | TĂNG | 1 | 0/1 |
| 2026-08-25_1003 | 2026-08-25_1003 | GIẢM | 1 | 0/1 |
| 2026-08-26_1001 | 2026-08-26_1001 | PHÂN VÂN | 1 | 0/1 |
| 2026-08-28_1007 | 2026-09-22_1003 | GIẢM | 13 | 8/13 |
| 2026-09-23_1007 | 2026-09-23_1007 | TĂNG | 1 | 1/1 |
| 2026-09-24_1009 | 2026-09-28_1006 | GIẢM | 3 | 3/3 |
| 2026-09-29_1002 | 2026-09-30_1003 | PHÂN VÂN | 2 | 1/2 |
| 2026-10-01_1005 | 2026-10-01_1005 | GIẢM | 1 | 0/1 |
| 2026-10-02_1001 | 2026-10-06_1001 | PHÂN VÂN | 3 | 1/3 |
| 2026-10-07_1004 | 2026-10-07_1004 | GIẢM | 1 | 1/1 |
| 2026-10-13_1005 | 2026-10-14_1009 | PHÂN VÂN | 2 | 1/2 |
| 2026-10-15_1005 | 2026-10-15_1005 | GIẢM | 1 | 1/1 |
| 2026-10-16_1007 | 2026-10-16_1007 | PHÂN VÂN | 1 | 1/1 |
| 2026-10-19_1001 | 2026-10-19_1001 | TĂNG | 1 | 0/1 |
| 2026-10-20_1017 | 2026-10-22_1009 | GIẢM | 2 | 0/2 |
| 2026-10-23_1002 | 2026-10-23_1002 | TĂNG | 1 | 0/1 |
| 2026-10-26_1002 | 2026-10-29_1005 | GIẢM | 5 | 5/5 |
| 2026-10-30_0955 | 2026-10-30_0955 | PHÂN VÂN | 1 | 0/1 |

## 4. Đúng/sai theo thị trường (cd.cham_chi_tiet; râu chạm đích tính; SAI = chạm SL / vô hiệu đúng khung trước) — 77 buổi thi
Bot thiếu bài = 'PHÂN VÂN/không view'. CHƯA RÕ THỨ TỰ = đích và SL cùng nến 1m (hoặc thiếu 1m) — không tính đúng, không vào mẫu số % đúng. 'Vô hiệu chưa hiểu' = có câu vô hiệu nhưng không tách được mốc → chỉ xét SL/đích.
| Hạn | Bên | ĐÚNG | SAI (SL / vô hiệu) | SAI hết hạn (không mốc sai, không chạm đích) | CHƯA RÕ | CHƯA RÕ THỨ TỰ | Chưa hết hạn | Không đích | Đích sai phía | PHÂN VÂN/không view | Vô hiệu chưa hiểu | % đúng (đã ngã ngũ) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 ngày | Bot | 20 | 42 (30 / 12) | 0 | 1 | 0 | 0 | 0 | 0 | 14 | 0 | 20/62 = 32% |
| 14 ngày | Người đó | 25 | 19 (7 / 12) | 5 | 5 | 0 | 2 | 3 | 1 | 17 | 13 | 25/49 = 51% |
| 14 ngày | Chép view buổi trước | 21 | 15 (5 / 10) | 9 | 5 | 0 | 2 | 3 | 6 | 16 | 18 | 21/45 = 47% |
| 14 ngày | Giữ view | 29 | 17 (5 / 12) | 11 | 6 | 0 | 2 | 3 | 9 | 0 | 22 | 29/57 = 51% |
| tự nêu (≤14 ngày; không nêu = 7) | Bot | 16 | 31 (21 / 10) | 0 | 16 | 0 | 0 | 0 | 0 | 14 | 0 | 16/47 = 34% |
| tự nêu (≤14 ngày; không nêu = 7) | Người đó | 14 | 13 (5 / 8) | 13 | 16 | 0 | 0 | 3 | 1 | 17 | 13 | 14/40 = 35% |
| tự nêu (≤14 ngày; không nêu = 7) | Chép view buổi trước | 15 | 9 (5 / 4) | 14 | 14 | 0 | 0 | 3 | 6 | 16 | 18 | 15/38 = 39% |
| tự nêu (≤14 ngày; không nêu = 7) | Giữ view | 20 | 11 (5 / 6) | 19 | 15 | 0 | 0 | 3 | 9 | 0 | 22 | 20/50 = 40% |
_Chép view buổi trước / Giữ view = nguyên view H4 (đích, vô hiệu, lệnh) của buổi đó, chấm lại từ C của buổi thi (hạn tự nêu = hạn của view gốc). Luôn GIẢM và Luật từ trên xuống không có đích → không chấm được theo thước này._

### 4b. View nhiều chặng: đúng đích cuối vs đúng ĐƯỜNG ĐI (hạn 14 ngày)
Đúng đường đi = chạm đích chặng 1 rồi mới tới đích cuối (lần lượt từng chặng), trước SL/vô hiệu. SAI_THU_TU = tới đích cuối khi chưa qua chặng trước.
| Bên | View nhiều chặng chấm được | Đúng đích cuối (kết quả chính) | ĐÚNG đường đi | SAI | SAI thứ tự | CHƯA RÕ THỨ TỰ | Chưa rõ / hết hạn / chưa hết hạn |
|---|---|---|---|---|---|---|---|
| Bot | 63 | 20 | 9 | 42 | 11 | 0 | 1 |
| Người đó | 37 | 15 | 8 | 14 | 7 | 0 | 8 |
| Chép view buổi trước | 36 | 16 | 8 | 9 | 8 | 0 | 11 |
| Giữ view | 47 | 24 | 15 | 10 | 9 | 0 | 13 |

## 5. Phép thử đối xứng THẬT (mốc phía kia cách giá tham chiếu đúng bằng khoảng tới đích; 50% = không hơn tung đồng xu)
### View không có chặng đi ngược (1 chặng hoặc mọi chặng cùng hướng) — phép thử chính
| Bên | View có đích | Chiều chọn tới trước | Phía kia tới trước | Cùng nến (1m không phân được) | Chưa ngã ngũ (14 ngày) | Chưa hết hạn | % thắng | p (nhị thức, vs 50%) |
|---|---|---|---|---|---|---|---|---|
| Bot | 6 | 2 | 3 | 0 | 1 | 0 | 2/5 = 40% | 1.000 |
| Người đó | 20 | 9 | 9 | 0 | 2 | 0 | 9/18 = 50% | 1.000 |
| Chép view buổi trước | 17 | 3 | 11 | 0 | 3 | 0 | 3/14 = 21% | 0.057 |
| Giữ view | 19 | 4 | 11 | 0 | 4 | 0 | 4/15 = 27% | 0.118 |

### View có chặng cố ý ĐI NGƯỢC (vd hồi lên rồi giảm) — báo riêng, KHÔNG gộp vào phép thử chính
| Bên | View có đích | Chiều chọn tới trước | Phía kia tới trước | Cùng nến (1m không phân được) | Chưa ngã ngũ (14 ngày) | Chưa hết hạn | % thắng | p (nhị thức, vs 50%) |
|---|---|---|---|---|---|---|---|---|
| Bot | 57 | 18 | 36 | 0 | 3 | 0 | 18/54 = 33% | 0.020 |
| Người đó | 36 | 7 | 24 | 0 | 4 | 1 | 7/31 = 23% | 0.003 |
| Chép view buổi trước | 35 | 11 | 15 | 0 | 8 | 1 | 11/26 = 42% | 0.557 |
| Giữ view | 46 | 17 | 17 | 0 | 11 | 1 | 17/34 = 50% | 1.000 |
_View có chặng đi ngược cố ý chạm phía kia trước nên biên đối xứng quanh giá phạt họ; bản cũ nới biên phía kia tới đích chặng 1 làm hai biên không còn đối xứng (bước ngẫu nhiên không lệch cũng > 50%) nên đã bỏ cách nới đó. Bảng riêng chỉ để tham khảo, không đọc như phép so với tung đồng xu._

## 6. Độ lệch số bot vs người đó (khi cùng hướng và đều có số; đích/mốc sai tách như cd.cham_chi_tiet)
| Thứ | Số buổi | Lệch |
|---|---|---|
| Đích | 35 | TB 1.11% · trung vị 0.80% · ≤1%: 20/35 |
| Mốc sai (vô hiệu) | 20 | TB 1.61% · trung vị 0.77% · ≤1%: 11/20 |

## 7. Từng buổi (* = giờ live không chắc; ∅ = không có bài làm)
| Buổi | C (VN) | Người | Bot | Trùng | Luật | Giữ view | Chép | Thị trường 14 ngày: người / bot | Hạn tự nêu: người / bot | Đường đi: người / bot | Đối xứng: người / bot | Đích N / B | Mốc sai N / B |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-07-01_WNiQnpm2BLo | 07-01 11:00 | GIẢM | GIẢM | ✓ | TĂNG | GIẢM | GIẢM | SAI / SAI | SAI / SAI | SAI / SAI | THUA / THUA | 54.000 / 57.500 | 61.000 / 60.789 |
| 2026-07-02_w4bvsDte3bI | 07-02 11:07 | PHÂN VÂN | TĂNG | ✗ | TĂNG | GIẢM | GIẢM | PHAN_VAN / DUNG | PHAN_VAN / CHUA_RO | — / DUNG | — / THANG | — / 63.800 | — / 60.000 |
| 2026-07-03_IV0Mlz8kNPI | 07-03 11:12 | TĂNG | TĂNG | ✓ | TĂNG | GIẢM | PHÂN VÂN | DUNG / DUNG | SAI_HET_HAN / DUNG | DUNG / SAI_THU_TU | THANG / THANG | 64.000 / 63.500 | — / 60.800 |
| 2026-07-06_GRWl0b0z1nk | 07-06 11:08 | GIẢM | TĂNG | ✗ | TĂNG | TĂNG | TĂNG | DICH_SAI_PHIA / SAI | DICH_SAI_PHIA / SAI | — / SAI | — / THUA | 65.000 / 65.300 | — / 62.444 |
| 2026-07-07_uvBnzq6-k-M | 07-07 11:05 | GIẢM | GIẢM | ✓ | TĂNG | GIẢM | GIẢM | DUNG / DUNG | CHUA_RO / DUNG | — / DUNG | THANG / THUA | 62.000 / 62.200 | 64.000 / 64.706 |
| 2026-07-09_Fmb8AziZ6f4 | 07-09 11:12 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | SAI / SAI | SAI / SAI | — / SAI | THUA / THUA | 61.000 / 60.000 | 63.000 / 63.000 |
| 2026-07-10_QwYznPgaAFY | 07-10 11:12 | TĂNG | PHÂN VÂN | ✗ | TĂNG | GIẢM | GIẢM | DUNG / PHAN_VAN | SAI_HET_HAN / PHAN_VAN | SAI_THU_TU / — | THUA / — | 66.000 / — | — / — |
| 2026-07-13_O3q2fmXlwhk | 07-13 11:09 | GIẢM | TĂNG | ✗ | GIẢM | TĂNG | TĂNG | SAI / DUNG | CHUA_RO / CHUA_RO | SAI / SAI_THU_TU | THUA / THANG | 61.000 / 65.800 | 64.000 / 61.000 |
| 2026-07-14_gpyn9kVPpn4 | 07-14 11:14 | GIẢM | GIẢM | ✓ | TĂNG | GIẢM | GIẢM | SAI / SAI | SAI / SAI | SAI / SAI | THUA / THUA | 61.000 / 61.000 | 64.000 / 64.000 |
| 2026-07-15_-T8Wu5b89B4 | 07-15 10:59 | TĂNG | TĂNG | ✓ | TĂNG | GIẢM | GIẢM | DUNG / SAI | CHUA_RO / CHUA_RO | — / SAI | THUA / THUA | 66.000 / 66.500 | — / 63.400 |
| 2026-07-16_bwgz_kMSvfE | 07-16 11:08 | TĂNG | TĂNG | ✓ | TĂNG | TĂNG | TĂNG | CHUA_RO / SAI | CHUA_RO / SAI | CHUA_RO / SAI | CHUA_NGA_NGU / THUA | 67.000 / 66.300 | 61.600 / 63.000 |
| 2026-07-21_azP_1WdR-CE | 07-21 11:02 | TĂNG | TĂNG | ✓ | TĂNG | TĂNG | TĂNG | CHUA_RO / DUNG | CHUA_RO / DUNG | — / SAI_THU_TU | THUA / THANG | 67.000 / 66.800 | 62.000 / 63.700 |
| 2026-07-22_3gr71JlVqR8 | 07-22 11:16 | TĂNG | TĂNG | ✓ | TĂNG | TĂNG | TĂNG | SAI / SAI | CHUA_RO / SAI | SAI / SAI | THUA / THUA | 67.000 / 67.300 | 64.000 / 65.000 |
| 2026-07-23_IsyMSPIscsc | 07-23 11:16 | TĂNG | TĂNG | ✓ | TĂNG | TĂNG | TĂNG | SAI / SAI | SAI / SAI | SAI / SAI | THUA / THUA | 68.000 / 67.000 | 64.000 / 64.000 |
| 2026-07-24_7D1Ve5hs4bU | 07-24 11:04 | TĂNG | TĂNG | ✓ | TĂNG | TĂNG | TĂNG | CHUA_RO / SAI | CHUA_RO / SAI | CHUA_RO / SAI | THUA / THUA | 68.000 / 68.000 | 62.000 / 65.000 |
| 2026-07-27_YMlDceykaTw | 07-27 11:15 | TĂNG | TĂNG | ✓ | TĂNG | TĂNG | TĂNG | SAI_HET_HAN / SAI | SAI_HET_HAN / SAI | SAI_HET_HAN / SAI | CHUA_NGA_NGU / THUA | 70.000 / 67.900 | — / 63.700 |
| 2026-07-28_1wDQbk0akZs | 07-28 11:45 | GIẢM | TĂNG | ✗ | PHÂN VÂN | TĂNG | TĂNG | CHUA_RO / CHUA_RO | CHUA_RO / CHUA_RO | CHUA_RO / CHUA_RO | THUA / CHUA_NGA_NGU | 62.000 / 70.000 | 66.000 / 62.500 |
| 2026-07-29_2FMmTeLGCNY | 07-29 11:12 | PHÂN VÂN | PHÂN VÂN | ✓ | PHÂN VÂN | GIẢM | GIẢM | PHAN_VAN / PHAN_VAN | PHAN_VAN / PHAN_VAN | — / — | — / — | — / — | — / — |
| 2026-07-29__TlYbqPT8nU | 07-30 01:23 | GIẢM | TĂNG | ✗ | PHÂN VÂN | GIẢM | PHÂN VÂN | SAI_HET_HAN / SAI | SAI_HET_HAN / SAI | SAI_HET_HAN / SAI | CHUA_NGA_NGU / THUA | 62.000 / 65.800 | — / 63.500 |
| 2026-07-30_qBG2h5D9CrE | 07-30 11:08 | PHÂN VÂN | GIẢM | ✗ | PHÂN VÂN | GIẢM | GIẢM | PHAN_VAN / DUNG | PHAN_VAN / DUNG | — / DUNG | — / THANG | — / 62.500 | — / 69.000 |
| 2026-07-31_SlGyokVNofU | 07-31 11:11 | GIẢM | PHÂN VÂN | ✗ | PHÂN VÂN | GIẢM | PHÂN VÂN | DUNG / PHAN_VAN | DUNG / PHAN_VAN | — / — | THANG / — | 62.500 / — | 65.000 / — |
| 2026-08-03_U6juTGDLJek | 08-03 11:13 | GIẢM | GIẢM | ✓ | TĂNG | GIẢM | GIẢM | SAI_HET_HAN / SAI | SAI_HET_HAN / SAI | — / SAI | THUA / THUA | 61.000 / 60.700 | — / 63.800 |
| 2026-08-04_K6QkKY6Og7o | 08-04 11:22 | GIẢM | GIẢM | ✓ | TĂNG | GIẢM | GIẢM | SAI / SAI | SAI / SAI | SAI / SAI | CHUA_NGA_NGU / CHUA_NGA_NGU | 60.500 / 60.700 | 70.000 / 64.000 |
| 2026-08-05_uw4QcusFtBc | 08-05 11:08 | GIẢM | GIẢM | ✓ | TĂNG | GIẢM | GIẢM | SAI / SAI | SAI / CHUA_RO | — / SAI | CHUA_NGA_NGU / CHUA_NGA_NGU | 60.500 / 60.500 | 65.000 / — |
| 2026-08-06__Ypby-_iFsg | 08-06 11:13 | TĂNG | GIẢM | ✗ | PHÂN VÂN | GIẢM | GIẢM | DUNG / SAI | DUNG / SAI | SAI_THU_TU / SAI | THANG / THUA | 65.000 / 60.500 | — / 65.000 |
| 2026-08-07_N-7XihrObp8 | 08-07 11:05 | PHÂN VÂN | PHÂN VÂN | ✓ | PHÂN VÂN | TĂNG | TĂNG | PHAN_VAN / PHAN_VAN | PHAN_VAN / PHAN_VAN | — / — | — / — | — / — | — / — |
| 2026-08-10_1001_8BGhoFetSaU | 08-10 11:05 | TĂNG | PHÂN VÂN | ✗ | TĂNG | TĂNG | PHÂN VÂN | DUNG / PHAN_VAN | SAI_HET_HAN / PHAN_VAN | DUNG / — | THUA / — | 66.500 / — | — / — |
| 2026-08-11_1005_KvVvliql8xI | 08-11 11:06 | PHÂN VÂN | GIẢM | ✗ | PHÂN VÂN | TĂNG | TĂNG | PHAN_VAN / SAI | PHAN_VAN / CHUA_RO | — / SAI | — / THUA | — / 62.500 | — / 64.900 |
| 2026-08-12_1003_EaWaSL7aWT4 | 08-12 11:20 | GIẢM | PHÂN VÂN | ✗ | PHÂN VÂN | TĂNG | PHÂN VÂN | SAI_HET_HAN / PHAN_VAN | SAI_HET_HAN / PHAN_VAN | SAI_HET_HAN / — | THUA / — | 62.000 / — | — / — |
| 2026-08-13_1006_hNxSX7GUKMs | 08-13 11:10 | GIẢM | GIẢM | ✓ | PHÂN VÂN | GIẢM | GIẢM | DUNG / SAI | SAI_HET_HAN / CHUA_RO | DUNG / SAI | THANG / THUA | 62.800 / 62.300 | — / 64.497 |
| 2026-08-14_1004_xK38gQ-G6uA | 08-14 11:28 | GIẢM | GIẢM | ✓ | PHÂN VÂN | GIẢM | GIẢM | KHONG_DICH / SAI | KHONG_DICH / CHUA_RO | — / SAI | — / THUA | — / 62.150 | — / 64.014 |
| 2026-08-17_1006_tmR0aXnjOlA | 08-17 11:12 | TĂNG | GIẢM | ✗ | TĂNG | GIẢM | GIẢM | DUNG / SAI | CHUA_RO / SAI | SAI_THU_TU / SAI | THANG / THUA | 64.000 / 60.000 | 62.000 / 64.400 |
| 2026-08-18_0957__c0_SERWnz0 | 08-18 11:09 | GIẢM | TĂNG | ✗ | TĂNG | TĂNG | TĂNG | SAI / DUNG | CHUA_RO / DUNG | SAI / SAI_THU_TU | THUA / THANG | 63.000 / 65.400 | 65.000 / 63.377 |
| 2026-08-19_1001_kfBEaOyHLkc | 08-19 11:08 | GIẢM | GIẢM | ✓ | PHÂN VÂN | GIẢM | GIẢM | SAI / SAI | SAI / SAI | — / SAI | THUA / THUA | 63.000 / 63.200 | 65.000 / 65.000 |
| 2026-08-20_1003_eBveasTOjTs | 08-20 11:15 | PHÂN VÂN | TĂNG | ✗ | GIẢM | GIẢM | GIẢM | PHAN_VAN / DUNG | PHAN_VAN / DUNG | — / SAI_THU_TU | — / THANG | — / 70.500 | — / 67.300 |
| 2026-08-21_1003_oDD5qwLcZbw | 08-21 11:18 | TĂNG | GIẢM | ✗ | GIẢM | GIẢM | PHÂN VÂN | DUNG / SAI | DUNG / SAI | — / SAI | THANG / THUA | 77.000 / 71.600 | — / 76.600 |
| 2026-08-25_1003_nSxBbLai2mE | 08-25 11:18 | GIẢM | TĂNG | ✗ | GIẢM | TĂNG | TĂNG | DUNG / SAI | DUNG / CHUA_RO | SAI_THU_TU / SAI | THANG / THUA | 79.000 / 82.800 | — / 76.681 |
| 2026-08-26_1001_I1DFCTsjQXE | 08-26 11:15 | PHÂN VÂN | GIẢM | ✗ | GIẢM | GIẢM | GIẢM | PHAN_VAN / SAI | PHAN_VAN / SAI | — / SAI | — / THUA | — / 76.700 | — / 79.971 |
| 2026-08-27_1006_ZJ5BVqdLJeE | 08-27 11:07 | — | PHÂN VÂN | — | GIẢM | GIẢM | PHÂN VÂN | KHONG_VIEW / PHAN_VAN | KHONG_VIEW / PHAN_VAN | — / — | — / — | — / — | — / — |
| 2026-08-28_1007_KwvLRMMnVms | 08-28 11:11 | GIẢM | TĂNG | ✗ | GIẢM | GIẢM | — | DUNG / SAI | DUNG / SAI | — / SAI | THANG / THUA | 79.000 / 82.800 | 80.400 / 78.500 |
| 2026-09-03_1012_8LXm3pVw9yI | 09-03 10:51 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | SAI / SAI | SAI / SAI | SAI / SAI | THUA / THUA | 75.000 / 76.000 | 79.000 / 79.256 |
| 2026-09-04_1014_eujLmRVw88k | 09-04 11:07 | GIẢM | TĂNG | ✗ | GIẢM | GIẢM | GIẢM | CHUA_RO / SAI | CHUA_RO / CHUA_RO | — / SAI | CHUA_NGA_NGU / THUA | 72.000 / 83.000 | 83.000 / 79.000 |
| 2026-09-07_1007_0oycLOOqibw | 09-07 11:12 | GIẢM | PHÂN VÂN | ✗ | GIẢM | GIẢM | GIẢM | DUNG / PHAN_VAN | DUNG / PHAN_VAN | — / — | THANG / — | 78.000 / — | — / — |
| 2026-09-08_1002_gOwbzU0t2S0 | 09-08 11:10 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | DUNG / DUNG | DUNG / DUNG | — / DUNG | THANG / THANG | 77.000 / 77.000 | — / 80.000 |
| 2026-09-14_1007_ykgTTK3EbP8 | 09-14 11:11 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | DUNG / SAI | DUNG / SAI | — / SAI | THUA / THANG | 76.000 / 75.200 | 83.000 / 79.000 |
| 2026-09-15_1008_M1ZThKy2Ylk | 09-15 11:13 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | DUNG / DUNG | DUNG / DUNG | — / DUNG | THANG / THANG | 77.000 / 75.300 | 81.000 / 79.000 |
| 2026-09-16_1008_31jXsidP5KE | 09-16 11:10 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | SAI_HET_HAN / SAI | SAI_HET_HAN / SAI | SAI_HET_HAN / SAI | THUA / THUA | 74.000 / 73.200 | — / 77.900 |
| 2026-09-17_0026_7mETSY5t5Yg | 09-17 01:26 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | SAI / SAI | SAI / SAI | SAI / SAI | THUA / THUA | 73.000 / 74.200 | — / 77.000 |
| 2026-09-17_1002_1cUPKUmEnr4 | 09-17 11:00 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | SAI / SAI | SAI / SAI | — / SAI | THUA / THUA | 73.000 / 73.700 | 78.000 / 77.400 |
| 2026-09-18_1003_YPMgjMxL2io | 09-18 11:13 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | SAI / SAI | SAI / SAI | SAI / SAI | THUA / THUA | 75.000 / 73.000 | 78.000 / 78.000 |
| 2026-09-21_1001_I_U52BYUt0M | 09-21 11:18 | GIẢM | TĂNG | ✗ | GIẢM | GIẢM | GIẢM | SAI / DUNG | CHUA_RO / DUNG | SAI / SAI_THU_TU | THUA / THANG | 80.000 / 83.000 | 83.000 / 80.133 |
| 2026-09-22_1003_N-_6NBs4ZW8 | 09-22 11:23 | GIẢM | TĂNG | ✗ | GIẢM | GIẢM | GIẢM | DUNG / SAI | SAI_HET_HAN / CHUA_RO | DUNG / SAI | THUA / CHUA_NGA_NGU | 84.000 / 89.800 | — / 83.000 |
| 2026-09-23_1007_uK4vb9PoUIo | 09-23 11:15 | TĂNG | TĂNG | ✓ | GIẢM | GIẢM | GIẢM | SAI / SAI | SAI / SAI | — / SAI | THUA / THUA | 88.000 / 89.800 | 85.000 / 85.111 |
| 2026-09-24_1009_R_WfFHUJ5RI | 09-24 11:15 | GIẢM | GIẢM | ✓ | GIẢM | TĂNG | TĂNG | SAI / DUNG | CHUA_RO / CHUA_RO | SAI / DUNG | THUA / THUA | 82.000 / 82.700 | 86.000 / 85.500 |
| 2026-09-25_1014_Wf7PeLs6l94 | 09-25 11:19 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | SAI / SAI | CHUA_RO / CHUA_RO | SAI / SAI | THUA / THUA | 82.500 / 82.200 | 86.000 / 85.600 |
| 2026-09-28_1006_G5Q1ATx_1ho | 09-28 11:08 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | DUNG / SAI | SAI_HET_HAN / CHUA_RO | DUNG / SAI | THUA / THUA | 82.000 / 81.600 | — / 85.000 |
| 2026-09-29_1002_3inGNRqb-UM | 09-29 11:14 | PHÂN VÂN | GIẢM | ✗ | GIẢM | GIẢM | GIẢM | PHAN_VAN / SAI | PHAN_VAN / SAI | — / SAI | — / THUA | — / 82.200 | — / 84.374 |
| 2026-09-30_1003_3qAxAK71YAs | 09-30 11:09 | PHÂN VÂN | PHÂN VÂN | ✓ | GIẢM | GIẢM | PHÂN VÂN | PHAN_VAN / PHAN_VAN | PHAN_VAN / PHAN_VAN | — / — | — / — | — / — | — / — |
| 2026-10-01_1005_56fLd04MSps | 10-01 11:14 | GIẢM | PHÂN VÂN | ✗ | GIẢM | GIẢM | PHÂN VÂN | SAI / PHAN_VAN | SAI / PHAN_VAN | SAI / — | THUA / — | 82.000 / — | 85.000 / — |
| 2026-10-02_1001_AxRfx12h9Z0 | 10-02 11:06 | PHÂN VÂN | TĂNG | ✗ | GIẢM | GIẢM | GIẢM | PHAN_VAN / DUNG | PHAN_VAN / DUNG | — / SAI_THU_TU | — / THANG | — / 87.200 | — / 84.400 |
| 2026-10-05_1013_5U5CVdTlwT8 | 10-05 11:18 | PHÂN VÂN | TĂNG | ✗ | GIẢM | GIẢM | PHÂN VÂN | PHAN_VAN / SAI | PHAN_VAN / SAI | — / SAI | — / THUA | — / 87.400 | — / 85.000 |
| 2026-10-06_1001_CABZxVcYavM | 10-06 11:15 | PHÂN VÂN | PHÂN VÂN | ✓ | GIẢM | GIẢM | PHÂN VÂN | PHAN_VAN / PHAN_VAN | PHAN_VAN / PHAN_VAN | — / — | — / — | — / — | — / — |
| 2026-10-07_1004_Rl-3RfG8EiY | 10-07 11:07 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | PHÂN VÂN | DUNG / DUNG | DUNG / DUNG | DUNG / SAI_THU_TU | THANG / THANG | 81.000 / 82.700 | — / 85.000 |
| 2026-10-13_1005_4ttwL_4CC9E | 10-13 11:07 | PHÂN VÂN | GIẢM | ✗ | GIẢM | GIẢM | GIẢM | PHAN_VAN / DUNG | PHAN_VAN / DUNG | — / DUNG | — / THANG | — / 80.700 | — / 84.200 |
| 2026-10-14_1009_BlA26qxNBTE | 10-14 11:22 | PHÂN VÂN | PHÂN VÂN | ✓ | GIẢM | GIẢM | PHÂN VÂN | PHAN_VAN / PHAN_VAN | PHAN_VAN / PHAN_VAN | — / — | — / — | — / — | — / — |
| 2026-10-15_1005_5iN8iTFsmlY | 10-15 11:13 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | PHÂN VÂN | DUNG / SAI | DUNG / CHUA_RO | — / SAI | THANG / THUA | 80.000 / 78.000 | 84.000 / 83.000 |
| 2026-10-16_1007_lSGpwulXi5s | 10-16 11:04 | PHÂN VÂN | PHÂN VÂN | ✓ | GIẢM | GIẢM | GIẢM | PHAN_VAN / PHAN_VAN | PHAN_VAN / PHAN_VAN | — / — | — / — | — / — | — / — |
| 2026-10-19_1001_-avZ2E3n2oE | 10-19 11:19 | TĂNG | PHÂN VÂN | ✗ | GIẢM | GIẢM | PHÂN VÂN | DUNG / PHAN_VAN | CHUA_RO / PHAN_VAN | SAI_THU_TU / — | THANG / — | 84.000 / — | 80.000 / — |
| 2026-10-20_1017_zzhCJ1Bb_vg | 10-20 11:12 | GIẢM | TĂNG | ✗ | GIẢM | TĂNG | TĂNG | KHONG_DICH / DUNG | KHONG_DICH / DUNG | — / DUNG | — / THANG | — / 84.000 | — / 81.000 |
| 2026-10-22_1009_yAEJBNZ56qs | 10-22 11:13 | GIẢM | TĂNG | ✗ | GIẢM | GIẢM | GIẢM | CHUA_HET_HAN / SAI | CHUA_RO / SAI | CHUA_HET_HAN / SAI | CHUA_HET_HAN / THUA | 76.000 / 86.500 | 86.000 / 82.000 |
| 2026-10-23_1002_cb85mXIfTv8 | 10-23 11:06 | TĂNG | GIẢM | ✗ | GIẢM | GIẢM | GIẢM | CHUA_HET_HAN / DUNG | SAI_HET_HAN / CHUA_RO | — / SAI_THU_TU | THUA / THANG | 83.000 / 78.000 | — / 83.000 |
| 2026-10-26_1002_52C5f7Gf1NE | 10-26 11:11 | GIẢM | GIẢM | ✓ | GIẢM | TĂNG | TĂNG | DUNG / SAI | DUNG / SAI | DUNG / SAI | THUA / THUA | 78.000 / 78.000 | — / 81.000 |
| 2026-10-27_1002_2RB3G-MYjhE | 10-27 11:20 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | DUNG / SAI | DUNG / SAI | SAI_THU_TU / SAI | THUA / THANG | 78.000 / 77.000 | — / 81.070 |
| 2026-10-28_1006_Gu1XtyNNH6I | 10-28 11:01 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | KHONG_DICH / DUNG | KHONG_DICH / DUNG | — / SAI_THU_TU | — / THANG | — / 77.000 | — / 83.000 |
| 2026-10-29_0033_4Hg5YedKaAg | 10-29 01:23 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | DUNG / DUNG | SAI_HET_HAN / DUNG | SAI_THU_TU / DUNG | THANG / THANG | 78.000 / 78.000 | — / 82.060 |
| 2026-10-29_1005_wcDxLBw0TO4 | 10-29 11:08 | GIẢM | GIẢM | ✓ | GIẢM | GIẢM | GIẢM | DUNG / SAI | DUNG / SAI | DUNG / SAI | THUA / THUA | 78.000 / 78.000 | — / 81.798 |
| 2026-10-30_0955_f0JWA9aDHl8 | 10-30 11:24 | PHÂN VÂN | GIẢM | ✗ | GIẢM | GIẢM | GIẢM | PHAN_VAN / DUNG | PHAN_VAN / DUNG | — / SAI_THU_TU | — / THANG | — / 76.500 | — / 80.000 |

## Buổi bị loại khỏi phần so hướng (1)
- 2026-08-27_1006_ZJ5BVqdLJeE: phiếu người đó không có nhãn H4/chung hợp lệ
