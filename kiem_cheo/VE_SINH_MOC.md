# Vệ sinh `moc/` — tài sản của mốc (P1-5), mốc đảo cận (P2), thống kê căn cứ chạy lại (P2)

Ngày 31/10/2026. Sao lưu nguyên trạng trước khi sửa: `moc/_ban_cu_2026-10-31/` (203 file = 180 JSON + 23 `_lo_*.txt`).
Script: `cong_cu/ve_sinh_moc.py` (sửa tại chỗ, giữ định dạng từng file; chạy lại cho cùng kết quả; `--chi-xem` chỉ in,
`--ngu-canh` in danh sách nghi theo transcript). Quy tắc rút mốc đã thêm trường `tai_san`: `cong_cu/QUY_TAC_RUT_MOC.md`.

## 1. Kết quả theo tài sản (3.368 mốc / 180 file)

| Tài sản | Dò tự động | Sau đọc tay (cuối cùng) |
|---|---:|---:|
| BTC | 3.260 | **3.362** |
| CHUA_RO | 99 | **4** |
| KHAC | 7 | 0 |
| DAU | 1 | **1** |
| SOL | 1 | **1** |
| ETH / VANG | 0 | 0 |

**6 mốc không phải BTC / chưa rõ** → `chac: false` (4 mốc đổi true→false, 2 mốc vốn đã false). Không xoá mốc nào.
Mọi mốc đều có trường `tai_san` (kiểm: 3.368/3.368, không còn `gia > gia_tren`).

## 2. Danh sách đổi (dòng = dòng trong file SAU khi sửa)

| Mốc | Tài sản | Giá | `chac` | Căn cứ đọc tay |
|---|---|---|---|---|
| `moc/2026-07-09_Fmb8AziZ6f4.json:44` | **DAU** | 60.000 | true→false | transcript 00:29:33 trả lời câu hỏi "con dầu ở vùng giá này còn giảm nữa không… khung tuần… giảm về quanh 60"; giá dầu 60 bị quy thành 60.000 (ca Codex nêu, `:42–52` cũ) |
| `moc/2026-08-10_8BGhoFetSaU.json:37` | **SOL** | 73.000–74.000 | true→false | transcript 00:51:53 "SOL thì không có gì để view… H4 của nó… chờ backtest về 73 74 rồi tính" (ca Codex nêu) |
| `moc/2026-04-07_HeBpJr0i6Bg.json:300` | CHUA_RO | 67.500 | true→false | 00:33:24 "Long 67k5 TP 74, 76, 78" nằm giữa đoạn "Qua view vàng dầu. Con dầu vẫn tăng… Dầu cứ lầm lì đi lên", nhưng 67k5/74/76/78 trùng hệt các mốc BTC vừa nêu ở 00:30–00:31 |
| `moc/2026-07-01_WNiQnpm2BLo.json:20` | CHUA_RO | 64.000–66.000 | true→false | 00:48:09 ngay sau "Swing dầu TP?… Long dầu… H4 đóng trên 61"; không rõ đã quay lại BTC chưa (61K cũng là mốc BTC #7 cùng buổi) |
| `moc/2026-03-16_uXm43DPUtPQ.json:309` | CHUA_RO | 73.800–73.900 | false (giữ) | 00:46:26–00:46:57 vừa nói dầu ("sway trong 71 đến 73") rồi trả lời câu hỏi FOMO ETH; "73k8, 73k9" không rõ của BTC hay dầu |
| `moc/2026-08-11_1005_KvVvliql8xI.json:37` | CHUA_RO | 57.000–58.000 | false (giữ) | đang xem USDT.D: "nó mà nổ đi lên một phát trên này là coi như là 57 hoặc 58" — không rõ mức BTC hay mức USDT.D |

**Đọc tay rồi giữ BTC (105 mốc tự động gắn khác BTC):**
- 97 mốc lệch > 40% không ghi chữ BTC: đều là view chu kỳ BTC dài hạn của người nói — gap CME 20K/22K, vùng gom 40–20K,
  giảm 70–77% từ đỉnh (27–37K), đỉnh 126K / lệnh short 124–125K, mục tiêu mùa sau 100–200K. Danh sách: `CHU_KY_BTC` trong script.
- 2 mốc "nhắc cả BTC lẫn ETH" mà lệch > 40%: câu ghi rõ "Bitcoin về 40.000" (`2026-02-03#15`, `2026-03-09#20`).
- 6 mốc tự động KHAC: altcoin/USDT.D chỉ là điều kiện tương quan, con số là BTC (`2026-01-06#11`, `2026-01-27#7`,
  `2026-08-14#8`, `2026-09-23#10`, `2026-09-25#15`); `2026-03-24#24` (người rút ghi "nói về altcoin") đọc transcript 01:00:57:
  là câu trả lời kịch bản BTC "lên 77… 80 83… không qua 74".
- Ngoài ra 9 mốc có chữ "vàng" là **màu đường/vùng tự vẽ** (đường vàng, ô tô vàng) — bộ lọc màu đã cho ra BTC, đọc tay xác nhận.

## 3. Cách dò

1. **Từ khoá** trong `trich` + `can_cu` (ghi chú trong ngoặc của người rút nằm trong `trich`), chuẩn hoá NFC, chữ thường:
   ETH (eth, ether), SOL (sol, solana), DAU (dầu, oil, wti, brent), VANG (vàng, gold, xau — **bỏ** cụm màu: "màu/đường/vùng/
   ô tô/line… vàng", "vàng sáng/chói"), KHAC (okb, bnb, near, zec, altcoin, alt, chứng khoán, cổ phiếu, S&P, nasdaq, dxy,
   usdt.d, btc.d, dominance, xrp, doge, sui, hype, ltc, link, avax, bạc, bch, wld); BTC (btc, bitcoin, bít, bit).
   Câu tự ghi "không phải BTC / không rõ BTC / không chắc là giá BTC" → không tính là rõ BTC.
2. **Độ lớn giá:** lệch = min(|mép/giá đóng D1 BTC hôm `ngay` − 1|) theo `du_lieu/btc_1Dutc.csv` (thiếu ngày 30/10 → ngày gần
   nhất trước đó). Lệch > 40% mà câu không rõ BTC → CHUA_RO.
3. Luật: có tài sản khác, không BTC → tài sản đó (nhiều loại → KHAC); có cả hai → BTC nếu lệch ≤ 40%, không thì CHUA_RO
   (đều đưa vào đọc tay); không từ khoá → BTC nếu lệch ≤ 40%, không thì CHUA_RO.
4. **Đọc tay** 158 mốc = 108 tự động khác BTC + 17 tự động BTC nhưng câu nhắc thêm tài sản khác + 9 chữ "vàng" màu + 21 mốc
   lệch xa có chữ BTC + 3 mốc nghi ở bước 5; đọc thêm transcript quanh `moc_gio` khi câu chưa đủ. Kết luận ghi vào `XAC_NHAN_TAY`.
5. **Dò thêm theo ngữ cảnh transcript** (vì dầu/SOL nói tắt "60", "73 74" trùng hàng nghìn của BTC, độ lớn giá không bắt được):
   cửa sổ [moc_gio − 60 s, + 20 s] nhắc ≥ 2 lần SOL/dầu/OKB/ZEC/HYPE/LTC/AAVE/BNB/NEAR/BTC.D/USDT.D và nhiều hơn số lần nhắc
   BTC → **40 mốc nghi**, đọc tay hết; thêm một lượt rộng hơn (gồm vàng/ETH, cửa sổ −75/+20 s, 57 mốc nghi mạnh). Kết quả: 2
   mốc đổi sang CHUA_RO (`2026-04-07#21`, `2026-07-01#14`) + 1 mốc từ lượt rộng (`2026-03-16#23`); còn lại là BTC (thanh
   lý/heatmap, "Bitcoin…", gap CME, vùng short BTC).

**Giới hạn:** 923 mốc không có `moc_gio` chỉ được dò bằng câu trích + độ lớn giá. Bước 5 là heuristic: một mốc dầu/SOL nằm
ngoài cửa sổ hoặc không nhắc tên tài sản vẫn có thể lọt. Người đọc tay: Claude, không nghe lại video.

**Ảnh hưởng ngoài `moc/`:** `cong_cu/kiem_can_cu.py`, `truy_nguoc.py`, `truy_fibo.py` đã bỏ mốc `chac:false`. `thi/tao_ho_so.py`
và `thi/cham.py` (không thuộc phạm vi sửa) đọc `moc/` nhưng **chưa lọc theo `tai_san`** — lần dựng hồ sơ thi sau nên bỏ mốc
`tai_san != "BTC"` (hiện chỉ hiện dấu "(?)" cho `chac:false`).

## 4. Mốc đảo cận `gia > gia_tren` → đã đổi chỗ (21)

| Mốc (dòng sau sửa) | Trước → sau | Vai trò | Câu trích |
|---|---|---|---|
| `moc/2026-03-10_TXnTpUkc78s.json:22` | 69.000 > 68.000 → 68.000–69.000 | entry | "điều chỉnh về 69.000 hoặc là 68.000" |
| `moc/2026-03-12_qJZk9q5A7rA.json:20` | 69.400 > 69.380 → 69.380–69.400 | khang_cu | "vùng 69k4, 69k38" |
| `moc/2026-03-31_bz8_iuwosGs.json:187` | 50.000 > 40.000 → 40.000–50.000 | dich | "swing short về 50, 40" |
| `moc/2026-04-01_Be-e74Mwx0U.json:287` | 66.300 > 66.000 → 66.000–66.300 | entry | "về 66.300, 66.000" |
| `moc/2026-04-03_vnCUK9ayUsI.json:153` | 65.000 > 64.000 → 64.000–65.000 | tp | "TP được ở giá 65 cho đến 64" |
| `moc/2026-04-03_vnCUK9ayUsI.json:277` | 40.000 > 20.000 → 20.000–40.000 | entry | "dump về 40 đến 20.000" |
| `moc/2026-04-06_b48t6sSiV90.json:6` | 50.000 > 40.000 → 40.000–50.000 | dich | "sập tiếp về 50 40.000" |
| `moc/2026-04-06_b48t6sSiV90.json:204` | 68.000 > 67.000 → 67.000–68.000 | entry | "quanh 6800 cho đến 6700 mấy" |
| `moc/2026-04-09_gx-69-TVn_w.json:136` | 70.000 > 69.000 → 69.000–70.000 | entry | "70.000, 6900 gì đó" |
| `moc/2026-04-14_LfNwCzyBHdM.json:218` | 73.900 > 73.800 → 73.800–73.900 | khac | "73k9, 73k8 … quét stop loss" |
| `moc/2026-04-16_usKAHnR-_VI.json:185` | 70.000 > 69.000 → 69.000–70.000 | ho_tro | "một gap ở 70 69" |
| `moc/2026-06-09_UmnCq7p4NlU.json:145` | 62.000 > 61.000 → 61.000–62.000 | tp | "TP thì 62.000 hoặc 61.000" |
| `moc/2026-06-09_UmnCq7p4NlU.json:157` | 61.000 > 60.000 → 60.000–61.000 | entry | "vùng 61.000 đến 60.000" |
| `moc/2026-06-22_eaj9NEm85O4.json:106` | 71.000 > 70.000 → 70.000–71.000 | dich | "vùng 71 70 này" |
| `moc/2026-06-25_gy-YwzytUiA.json:18` | 57.000 > 55.000 → 55.000–57.000 | dich | "về 57 55" |
| `moc/2026-06-26_UzjWDBAiahs.json:20` | 69.000 > 50.000 → 50.000–69.000 | ho_tro | "69 cho đến vùng 50" |
| `moc/2026-07-01_WNiQnpm2BLo.json:16` | 54.000 > 51.000 → 51.000–54.000 | dich | "từ 54 cho đến 52 51" |
| `moc/2026-08-10_8BGhoFetSaU.json:40` | 64.300 > 64.000 → 64.000–64.300 | entry | "64.300, 6400 gì đó" |
| `moc/2026-10-27_1002_2RB3G-MYjhE.json:34` | 75.000 > 74.000 → 74.000–75.000 | khac | "chờ về khoảng 75, 74" |
| `moc/2026-10-27_1002_2RB3G-MYjhE.json:38` | 54.000 > 45.000 → 45.000–54.000 | dich | "về được 54 đến 45" |
| `moc/2026-10-29_1005_wcDxLBw0TO4.json:172` | 78.000 > 77.999 → 77.999–78.000 | ho_tro | "78.00[?] cho đến 77.00[?]" — **nghi rút sai** (có lẽ 77.000–78.000), chỉ đổi chỗ, chưa sửa số |

Cùng buổi 10/8 có hai transcript (`zip_clean` và `phu_de`) nhưng chỉ một file mốc — không bị đếm thành hai mẫu.

## 5. `cong_cu/kiem_can_cu.py` chạy lại (P2 — giờ live thật)

Sửa `cong_cu/kiem_can_cu.py:86–115` (hàm `gio_live` + vòng đọc mốc): giờ bắt đầu = `transcripts/gio_live.tsv` (`bat_dau_vn`, cùng cách đọc như
`cong_cu/cham_dich.py::gio_live`, khoá = 11 ký tự cuối tên file), thiếu mới dùng HHMM tên file / 10:00; bỏ thêm mốc
`tai_san != BTC`. 180/180 buổi có giờ thật; so với giờ cũ **32 buổi lệch > 15 phút, 11 buổi lệch > 60 phút** (tối đa +866 phút,
`2026-07-29__TlYbqPT8nU`; nhiều buổi tối bị coi là 10:00).

| Chỉ số (mốc thật / ngẫu nhiên, gấp) | Trước (mốc cũ, giờ cũ) | Mốc sạch, giờ cũ | **Mốc sạch, giờ thật** |
|---|---|---|---|
| Số mốc xét | 2.716 | 2.712 | **2.712** |
| ≥ 1 căn cứ | 99,8% / 96,4% · 1,03 | 99,8% / 96,5% · 1,03 | 99,8% / 96,5% · 1,03 |
| Fibo | 40,0% / 40,8% · 0,98 | 39,9% / 40,9% · 0,98 | **40,2% / 41,0% · 0,98** |
| MA | 36,9% / 34,2% · 1,08 | 36,9% / 34,5% · 1,07 | **37,1% / 34,5% · 1,07** |
| Đỉnh/đáy cũ | 60,4% / 58,7% · 1,03 | 60,4% / 58,8% · 1,03 | 60,4% / 58,7% · 1,03 |
| Số tròn 1.000 | 91,3% / 53,8% · 1,70 | 91,3% / 54,2% · 1,69 | 91,3% / 53,8% · 1,70 |
| Số tròn 500 | 98,7% / 90,0% · 1,10 | 98,7% / 90,0% · 1,10 | 98,7% / 90,0% · 1,10 |
| Căn cứ NÓI ra khớp số liệu: Fibo / MA | 191/493 · 163/300 | 191/493 · 163/300 | **198/493 · 164/300** |

Thay đổi nhỏ; kết luận cũ giữ nguyên (Fibo không hơn mốc ngẫu nhiên; số tròn 1.000 gấp ~1,7). Theo vai trò, bỏ 4 mốc sai
tài sản làm khang_cu 354→353, dich 758→757, entry 287→286, day_cu 40→39. Số thập phân lấy bằng cách in 1 chữ số lẻ
(script in 0 chữ số). `so_tay/SO_LIEU_CAN_CU.md` vẫn là ảnh chụp 179/3.349 (đã ghi chú dòng đầu), chưa sinh lại.

## Phụ lục — P1-12 lệnh giấy (bản lưu, vì `giay/BAO_CAO.md` bị `chay_giay.py` sinh lại mỗi lần chạy)

`trang_thai_v1/v2.json` đứng ở 01:03 VN 31/10, `nen_cuoi = null`, không có `nhat_ky.csv`/`cron.log`. Nguyên nhân: **chưa cài
lịch** — `crontab -l` → "no crontab for badat", không có LaunchAgent gọi `chay_giay.py`; `giay/cai_lich.sh` chỉ in dòng
crontab. Script chỉ chạy 1 lần thủ công lúc 01:03, trước nến H4 đầu tiên sau mốc bắt đầu (03:00 VN). User tự bật:
`(crontab -l 2>/dev/null; echo '5 3,7,11,15,19,23 * * * cd /Users/badat/linhtinh/trade_dai_han && /opt/homebrew/bin/python3 giay/chay_giay.py >> giay/cron.log 2>&1') | crontab -`
rồi kiểm `crontab -l`; tuỳ chọn chạy bù ngay `python3 giay/chay_giay.py`.
