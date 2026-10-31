# Nguồn dữ liệu bot v4

Tải lúc 2026-10-31 04:00 UTC bằng `bot_v4/tai_du_lieu.py`. Khoảng yêu cầu 2022-06-01 -> 2026-10-30 UTC.

- Crypto (BTC, ETH, OKB, BNB): OKX spot `<X>-USDT`, `/api/v5/market/history-candles`, chỉ nến confirm=1; 4H và 1Dutc.
- VANG = Yahoo `GC=F`, DAU = Yahoo `CL=F`. 4H dựng từ 1H (Yahoo chỉ cho ~730 ngày) gộp theo UTC 00/04/08/12/16/20, giữ nến có >=3 nến 1H. 1D: interval=1d, ts_utc = 17:00 New York của ngày đó trừ 23h (giờ mở phiên, như backtest).

| TS | khung | ngày bắt đầu thực tế | ngày cuối | số nến | lỗ hổng>1 nến |
|---|---|---|---|---|---|
| BTC | 4H | 2022-06-01 00:00 | 2026-10-30 20:00 | 9678 | 0 |
| BTC | 1D | 2022-06-01 00:00 | 2026-10-30 00:00 | 1613 | 0 |
| ETH | 4H | 2022-06-01 00:00 | 2026-10-30 20:00 | 9678 | 0 |
| ETH | 1D | 2022-06-01 00:00 | 2026-10-30 00:00 | 1613 | 0 |
| OKB | 4H | 2022-06-01 00:00 | 2026-10-30 20:00 | 9678 | 0 |
| OKB | 1D | 2022-06-01 00:00 | 2026-10-30 00:00 | 1613 | 0 |
| BNB | 4H | 2022-12-21 00:00 | 2026-10-30 20:00 | 8460 | 0 |
| BNB | 1D | 2022-12-21 00:00 | 2026-10-30 00:00 | 1410 | 0 |
| VANG | 4H | 2024-06-10 00:00 | 2026-10-30 16:00 | 3454 | (140 nghỉ, bình thường) |
| VANG | 1D | 2022-06-01 22:00 | 2026-10-29 22:00 | 1111 | (241 nghỉ, bình thường) |
| DAU | 4H | 2024-06-10 00:00 | 2026-10-30 16:00 | 3404 | (161 nghỉ, bình thường) |
| DAU | 1D | 2022-06-01 22:00 | 2026-10-29 22:00 | 1110 | (242 nghỉ, bình thường) |
