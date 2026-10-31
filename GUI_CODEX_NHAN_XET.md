# Nhờ Codex nhận xét & bổ sung — dự án "bot bắt chước người phân tích BTC" (31/10/2026)

Bạn là người phản biện độc lập. Đọc tài liệu dưới, chỉ ra **chỗ thiếu / sai / rủi ro**, và **bổ sung** những gì nên có
TRƯỚC khi chạy bài thi. Ghi kết quả vào **`trade_dai_han/CODEX_NHAN_XET.md`** (tiếng Việt, gạch đầu dòng, có mức ưu tiên).
KHÔNG sửa file nào khác. Thư mục gốc: `/Users/badat/linhtinh/trade_dai_han/`.

## 1. Mục tiêu dự án
- Tái tạo **tư duy + thói quen** của 1 người phân tích BTC (kênh YouTube FAM Trading, live ~10:00 sáng các ngày thường).
- Thước đo CHÍNH = bot **GIỐNG** người đó (hướng, vùng, đích, mốc sai); lãi/lỗ là thước đo phụ.
- Nhận định phải **dứt khoát** sau nến H4 đóng: TĂNG / GIẢM / PHÂN VÂN (được phép khi khó) + đích + hạn + lệnh;
  BẮT BUỘC có **râu nến** (test lại không, vì sao) và **vùng ổn** để vào lệnh kèm lý do hội tụ; CẤM nước đôi. (Xem `DESIGN.md`.)

## 2. Dữ liệu đã có
| Thứ | Ở đâu | Ghi chú |
|---|---|---|
| 180 transcript (06/01→30/10/2026) | `transcripts/zip_clean/` (130, có mốc [hh:mm:ss]), `transcripts/lam_sach/` (51) | đã làm sạch |
| 180 phiếu nhận định (hướng H4/D1/W1, đích, đường đi, mốc sai, lệnh, thói quen…) | `phieu/*.json` | quy tắc `cong_cu/QUY_TAC_RUT_NHAN_DINH.md` |
| 3.368 mốc giá + căn cứ người đó nói | `moc/*.json` | 82% có căn cứ |
| 232 ảnh chart live + ghi chú | `so_tay/khung/`, `so_tay/ghi_chu/hinh_anh_*.md` | xác minh EMA, Fibo, Hyblock |
| Sổ tay tinh hoa (48 luật L01–L48) | `so_tay/SO_TAY_TINH_HOA.md` | mục A0 = chu kỳ 4 năm |
| Số liệu căn cứ | `so_tay/SO_LIEU_CAN_CU.md` | |
| Bài học | `so_tay/BAI_HOC.md` | |
| Giá | `du_lieu/btc_*.csv`, `backtest/du_lieu*/` | OKX + Yahoo (vàng, dầu, CME) |

## 3. Đã biết về người đó (tóm tắt — chi tiết ở sổ tay)
- **Từ trên xuống**: chu kỳ 4 năm (halving) → tháng → tuần → ngày → H4 → M5. Đầu tuần/đầu tháng view lại khung lớn.
  Pha hiện tại: đỉnh chu kỳ 10–11/2025 → downtrend ~2 năm → đi ngang → uptrend theo halving 2028. TĂNG H4 năm 2026 phần lớn là "hồi kỹ thuật".
- Bộ chỉ báo (đã xác minh bằng ảnh + số): **EMA34 dải (high/low/close) vàng, EMA89 xanh dương, EMA200 tím, EMA610 xanh ngọc** (Sonic R), volume FxCanli, RSI14.
- Mỗi con số có căn cứ; chỉ tin vùng **2–4 căn cứ hội tụ** (Fibo 0.5/0.618, EMA, đỉnh/đáy/râu cũ đổi vai, gap CME (bỏ từ T7), cụm thanh lý).
  Fibo thoái lui neo râu nhịp gần; **Fibo mở rộng 3 điểm** (TP1 = 1, TP2 = 1.618); Fibo lớn **ghim** nhiều tuần (97,9k→59,8k).
- Chỉ đổi hướng khi **nến H4 đóng** qua mốc đã báo trước, **2 cây H4** mới chắc; râu không tính. Tin tức chỉ "hợp lý hoá đường giá".
- Dữ liệu tâm lý (F&G alternative.me, Hyblock delta, heatmap Coinglass) chỉ để lọc/chốt lời, không để vào lệnh.

## 4. Đã thử & kết quả (trung thực)
| Thử | Kết quả |
|---|---|
| Bot v1 = luật cơ học từ sổ tay (EMA H4 + 2 cây + hội tụ + SL/TP) | 2026 (đã học) +18%, **2025 (ngoài mẫu) −27,6%**, giả dược phân vị 17 |
| Bot v2 = v1 + 5 sửa (đi ngang, sau nến lớn, phá–test lại, SL nến đóng, TP Fibo mở rộng) | 2026 +48%, **2025 −42,9%** |
| % giống hướng H4 với người đó (180 buổi) | v1: **51%** khi cả 2 có hướng (32% tính cả PHÂN VÂN) |
| Luật 1 đặc trưng tốt nhất (nhịp 24h) | 58% ngoài mẫu (kiểm chéo) |
| **Luật từ trên xuống** (pha downtrend → mặc định GIẢM; TĂNG = hồi khi giá ≤ EMA89 D1 và 24h không sập) | **63%** ngoài mẫu (54–71%) |
| Mốc T7–T10 (77 buổi) | chép hướng buổi trước 51%; luôn GIẢM 57% |
| Người đó đúng hướng giá 24h | 55% (156 buổi) |
| Test thật 29–30/10 (bot nhập vai bằng Claude) | cùng hướng người đó 3/3 coin người đó nói; đích bot nông hơn |

## 5. Kế hoạch tiếp — BOT V3 (Claude suy luận) + BÀI THI (xin bạn phản biện)
**Bot v3**: mỗi buổi, 1 phiên Claude nhận "hồ sơ đầu vào" CHỈ gồm dữ liệu có trước giờ live, suy luận theo sổ tay **từ trên xuống**,
xuất phiếu cùng định dạng phiếu người đó (+ râu nến, vùng ổn, lệnh).
Hồ sơ đầu vào dự kiến:
1. Pha chu kỳ 4 năm + view khung lớn (W1/D1/"chung") người đó nói ở các buổi TRƯỚC.
2. Phiếu buổi liền trước của người đó (view, đích, mốc sai) + bản đồ mốc (`moc/`) của ~5 buổi trước, đánh dấu mốc đã bị phá.
3. Số liệu thị trường tại nến H4 đóng ngay trước live: nến H4/D1/W1 gần nhất, EMA 34(dải)/89/200/610 các khung, đỉnh/đáy fractal,
   Fibo các sóng lớn, RSI, nhịp 24h/72h/7 ngày, khoảng cách tới EMA89 D1, F&G lịch sử (alternative.me có API lịch sử), thứ trong tuần / đầu tháng.
4. KHÔNG có transcript/phiếu của chính buổi đang thi.
**Bài thi**: các buổi **01/07 → 30/10/2026** (77 buổi; sau mốc kiến thức ~06/2026 của model để tránh "biết trước giá").
Để tránh rò rỉ thói quen của chính giai đoạn thi, dự định dùng **sổ tay chỉ chắt từ các buổi T1–T6** (ghi chú `so_tay/ghi_chu/nhom_1..5.md`).
**Chấm**: (1) % trùng hướng H4 (so mốc 51% / 57% / 63%); (2) độ lệch đích & vùng so với người đó; (3) lệnh giấy 4.000$ theo nhận định bot;
(4) phụ: đúng hướng giá 24h.

## 6. Câu hỏi cụ thể cho bạn
1. Thiết kế bài thi còn **rò rỉ dữ liệu tương lai** ở đâu không (kể cả rò rỉ qua sổ tay, qua bản đồ mốc, qua kiến thức model)?
2. Hồ sơ đầu vào còn **thiếu thứ gì quan trọng** mà người đó luôn nhìn (USDT.D, BTC.D, heatmap, lịch tin, vàng/dầu, nến tháng…)? Thứ nào lấy được lịch sử, lấy từ đâu?
3. Thước đo "giống" như vậy đã đúng chưa? Nên chấm PHÂN VÂN thế nào? Có cần chấm theo **độ chắc** / theo **đích** / theo **đường đi 2 chặng**?
4. Mốc so sánh còn thiếu không (vd "chép view buổi trước + luật từ trên xuống")? Cỡ mẫu 77 buổi có đủ để kết luận không, kiểm định gì?
5. Có nên bỏ lệnh giấy/lãi lỗ khỏi bài thi đầu tiên để tập trung vào "giống" không?
6. Điểm mù lớn nhất của cả dự án theo bạn là gì? (vd: phiếu do Sonnet rút có thể lệch; người đó tự mâu thuẫn; live sáng vs tối…)
7. Bổ sung bất kỳ điều gì bạn thấy cần — kể cả phản đối cả hướng làm.
