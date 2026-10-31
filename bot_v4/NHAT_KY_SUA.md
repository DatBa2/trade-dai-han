# Bot v4 — NHẬT KÝ SỬA (sau lần chạy dữ liệu thật đầu tiên)

Quy tắc: mọi thay đổi code sau lần chạy thật đầu tiên ghi ở đây — lỗi gì (chỉ lỗi code / sai thiết kế, KHÔNG chỉnh luật hay
tham số vì lãi lỗ), sửa gì, kết quả 3 năm TRƯỚC và SAU sửa.

## Mốc 0 — lần chạy dữ liệu thật đầu tiên (2026-10-31 04:18 UTC)

Trước mốc này động cơ chỉ chạy trên dữ liệu GIẢ (bước ngẫu nhiên) để gỡ lỗi; lỗi duy nhất tìm được ở đó (đóng `HET_KY` giả khi
dữ liệu bị cắt → kiểm cắt cụt lệch ở nến cuối) đã sửa và ghi ở DIEN_GIAI mục 26 TRƯỚC mốc này.
DIEN_GIAI.md viết xong trước mốc này. sha256 mã tại mốc 0:

| Tệp | sha256 |
|---|---|
| `bot_v4/dong_co.py` | `c05dfb7adfe12626cf48a589994f98ebd2955c93de1c1725393937c1f983529c` |
| `cong_cu/chi_bao.py` | `1f0a0cde1ccfa7b1d6ba6bc9f043b4bc8cd5a21e2212ae9d23073dd60f02a757` |
| `bot_v4/chay.py` | `ef635d2ec2ea117d96ae2a3da97a7062327d5f6c14864c1b756052fb71628e1a` |
| `bot_v4/kiem_tra.py` | `80a7a5c71a46ae55ee6053f2609a7a3d9894c479e1cababa379520349b317af0` |
| `bot_v4/DIEN_GIAI.md` | `f1398bcb250c8376a859e3e667b79389df6f507edc67f143d8bd9568c0fced37` |

Kết quả mốc 0 (`python3 bot_v4/chay.py --nam N --ro R`, 6 lượt song song) — `python3 bot_v4/kiem_tra.py`: **114/114 PASS**
(chạy 2 lần, lần 2 sau khi 6 thư mục ket_qua ghi xong):

| Năm | Rổ | Lãi $ | % | Lệnh khớp | % thắng | R TB | Sụt giảm max | Hệ số LN |
|---|---|---|---|---|---|---|---|---|
| 2024 | 6 | −2.502,34 | −62,56% | 399 | 35,6% | −0,101 | 75,23% | 0,865 |
| 2024 | BTC | −643,23 | −16,08% | 120 | 31,7% | −0,053 | 37,73% | 0,907 |
| 2025 | 6 | −2.777,97 | −69,45% | 400 | 37,5% | −0,125 | 75,19% | 0,769 |
| 2025 | BTC | −841,80 | −21,05% | 129 | 38,0% | −0,082 | 33,03% | 0,856 |
| 2026 | 6 | −2.319,14 | −57,98% | 331 | 41,1% | −0,098 | 67,47% | 0,776 |
| 2026 | BTC | −753,87 | −18,85% | 92 | 41,3% | −0,082 | 29,67% | 0,811 |

Soát tay 1 lệnh thật (BTC LONG đặt 2025-01-07 16:00): vùng 97.260,8–97.527,2 (fractal + EMA89 H4, 2 điểm) → giá vào giữa
97.394; SL = sàn 1,2% (96.225,3); khớp nến 16:00–20:00 (low 96.300,1); SL ở nến 20:00–24:00 (low 96.176,6) — đúng TK 5.3/7.

## Các lần sửa sau mốc 0

(Chưa có — mã không đổi kể từ mốc 0; sha256 như bảng trên.)
