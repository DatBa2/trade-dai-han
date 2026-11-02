# trade_dai_han — Bot bắt chước một người phân tích BTC

Tái tạo **tư duy + thói quen** nhận định thị trường của một người phân tích BTC (kênh YouTube FAM Trading) từ 180 buổi
livestream (06/01 → 30/10/2026), rồi dựng bot nhận định **giống người đó** (không chèn ý riêng). Thước đo chính là độ giống;
lãi/lỗ là phụ. Thiết kế + mọi yêu cầu đã chốt: [`DESIGN.md`](DESIGN.md).

## Dùng ngay: bot v5 (nhận định từ ảnh chart)

Trong Claude Code, ở thư mục này:

```
/nhan-dinh                                   ← dán ảnh chart (coin bất kỳ, thời điểm quá khứ)
/nhan-dinh ZEC 4H "2026-10-31 11:00"         ← hoặc ghi thẳng MÃ KHUNG "giờ VN nến cuối đã đóng"
/nhan-dinh BTC 1D "2026-08-20 07:00" đang long 64.000
```

Bot đọc ảnh → lấy ngữ cảnh **đúng tại thời điểm T, không dữ liệu sau T** (`bot_v5/ngu_canh.py`: nến + volume, dải EMA34 /
EMA89/200/610, trendline kẻ theo cách người đó, Fibo, đỉnh đáy, râu chưa test, lịch tin, Fed kỳ tới + Polymarket, F&G, BTC) →
đọc sổ tay đã lọc theo T (`bot_v5/so_tay_den.py`) → trả lời 11 mục: hướng H4/D1/W1, đường đi, đích + mốc sai theo nến đóng,
chỗ VÀO, chỗ TRÁNH, GIỮ/ĐÓNG lệnh, râu, trendline, tin & Fed, lời bình → lưu `bot_v5/doi_chieu/<ngày T>_<MÃ>.md` để ghi kết
quả thật về sau. Hướng dẫn: [`bot_v5/CACH_DUNG.md`](bot_v5/CACH_DUNG.md). Ảnh trước 07/2026: model có thể nhớ diễn biến → bài thử
không sạch (bot tự in cảnh báo).

## Luồng dự án

| Bước | Ở đâu | Ghi chú |
|---|---|---|
| 1. Thu transcript | `cong_cu/lay_transcript.py` → `transcripts/` | phụ đề trước, Whisper `--vad` dự phòng; giãn cách gọi YouTube |
| 2. Làm sạch | `transcripts/lam_sach/`, `transcripts/zip_clean/` | quy tắc `cong_cu/QUY_TAC_LAM_SACH.md` |
| 3. Phiếu + mốc giá (v1, Sonnet) | `phieu/` (180), `moc/` (3.368 mốc) | `cong_cu/QUY_TAC_RUT_*.md` |
| 4. Ảnh chart từ video | `so_tay/khung/` (321 ảnh), `so_tay/ghi_chu/` | `cong_cu/chup_khung.py` |
| 5. Sổ tay tinh hoa | `so_tay/SO_TAY_TINH_HOA.md`, `web_so_tay/` (web local) | 48 luật L01–L48 |
| 6. Nhãn học đầy đủ (v5, Opus rút mù) | `hoc_v5/nhan/` (180 buổi) | trendline, nến+volume, cách đo vẽ, vùng hẹp, view trung hạn, vùng tránh, giữ/đóng, tin & Polymarket; khoá `hoc_v5/KHOA_NHAN.md` |
| 7. Phân tích hành vi | `hoc_v5/giu_lat/`, `hoc_v5/trendline/` | giữ/lật view; thuật toán trendline hiệu chỉnh theo đường người đó vẽ |
| 8. Sổ tay bot v5 | `bot_v5/so_tay/` (95 case) + `NHAP_VAI.md` + `MAU_TRA_LOI.md` | mọi luật có nguồn = lời / hành vi người đó |
| Tin tức | `du_lieu/tin_tuc/`, `cong_cu/tin_tuc.py` | lịch kinh tế 2026, kết quả FOMC, Polymarket theo giờ |
| Nguồn phụ | `transcripts/khac/doantoancoin/` | kênh khác, chỉ để hiểu nguyên do vĩ mô — không phải hình mẫu |

## Các phiên bản bot và kết quả (trung thực)

| Bản | Cách làm | Kết quả chính |
|---|---|---|
| v5 (base) | Claude nhập vai thuần + sổ tay 180 buổi + ngữ cảnh tại T | 20 buổi T7–T10 (trong mẫu, 02/11/2026): trùng hướng H4 **70%** (bản trước đợt đọc lại 60%) — vẫn thua "luôn GIẢM" 80%; chênh trước/sau chưa phân biệt được với nhiễu — `bot_v5/NHAT_KY_SUA.md` |

Đã gỡ khỏi repo (02/11/2026): v1, v2 (luật máy từ sổ tay, `backtest/` + paper trading `giay/`) — 2025 ngoài mẫu lỗ
(v1 −27,6%, v2 −42,9%); v3 (Claude theo sổ tay T1–T6, bộ thi `thi/`) — trùng hướng H4 60% trên 77 buổi T7–T10, không hơn
"luôn GIẢM" 64%; v4 (luật máy khoá thiết kế trước, `bot_v4/`) — lỗ mọi năm, không hơn giả dược. Code + kết quả còn trong
lịch sử git (`git show c19482b:thi/BAO_CAO_XU_LY_P0.md`, `git show c19482b:bot_v4/KET_QUA.md`). Chỉ giữ dữ liệu bản cũ
mà phần còn lại đọc: `bot_v4/du_lieu/`, `thi/du_lieu/btc_*_bo_sung.csv`, `thi/dap_an_v2/nhan/`.

Hành vi người đó đo được (180 buổi, `hoc_v5/giu_lat/GIU_LAT.md`): giữ view buổi trước **72%**; không luật máy nào đoán lúc lật
tốt hơn "giữ view"; lật nhiều khi giá ra ngoài dải EMA34 H4 phía sai view (52% vs 16%); xác suất Fed tăng lãi kỳ tới > 70% →
6/6 buổi GIẢM; view D1 bền trung vị ~3 ngày, W1 ~6 ngày; đích D1 chạm 34%, W1 21% trước khi họ bỏ view. Độ khớp nhãn giữa các
người rút nhãn độc lập ~83–89% (trần đo được của "độ giống").

## Kiểm chứng & chống "chỉnh theo kết quả"

- Bot v5: sổ tay lọc theo T (`bot_v5/kiem_tra_so_tay_den.py`), ngữ cảnh cắt cụt (`bot_v5/kiem_tra_ngu_canh.py`).
- Phản biện / kiểm độc lập bởi Codex: `CODEX_NHAN_XET.md`, `kiem_cheo/` (`GUI_CODEX_KIEM_TOAN_BO.md` để Codex chạy lại toàn bộ).

## Giới hạn

- Model biết giá tới ~06/2026 → thử sạch chỉ với thời điểm sau 07/2026 hoặc buổi live mới.
- T7–T10 đã tham gia phát triển → kết luận thật cần thi trên buổi mới, dự báo lưu trước khi mở đáp án.
- Người đó gần như chỉ phân tích BTC → bot áp cho coin khác là suy cách làm, độ tin thấp hơn.
- Không có dữ liệu lịch sử Hyblock / heatmap thanh lý / số liệu CPI-NFP thực tế. USDT.D / BTC.D trong hồ sơ bot v5 chỉ là
  proxy CoinMarketCap theo ngày (mức % lệch chart TradingView người đó xem); gap CME tính từ Yahoo BTC=F 1h.
- Transcript và ảnh khung hình thuộc kênh YouTube gốc — repo để riêng tư, chỉ dùng nghiên cứu.
