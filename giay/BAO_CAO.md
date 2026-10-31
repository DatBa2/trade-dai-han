# LỆNH GIẤY v1 vs v2 — chạy tiếp ngoài mẫu

_Sinh tự động bởi `giay/chay_giay.py` lúc **2026-10-31 01:03 VN**. Bắt đầu 2026-10-31 00:00 VN, mỗi bot vốn 4.000$, rủi ro 2%/lệnh, tối đa 4 lệnh, 6 tài sản BTC, ETH, OKB, BNB (OKX), vàng GC=F, dầu CL=F (Yahoo). Luật giữ nguyên như backtest (`backtest/v2.py`, bộ máy `buoc`)._

## Vì sao trạng thái không cập nhật (kiểm 31/10/2026 11:13 VN — mục viết tay, P1-12)

- **Quan sát:** `trang_thai_v1.json` / `trang_thai_v2.json` vẫn `cap_nhat_vn = 2026-10-31 01:03`, `nen_cuoi = null`,
  `so_nen_da_xu_ly = 0`; chưa có `giay/nhat_ky.csv`, chưa có `giay/cron.log`.
- **Nguyên nhân: chưa cài lịch chạy nào.** `crontab -l` → `no crontab for badat`; `launchctl list` / `~/Library/LaunchAgents`
  không có tác vụ nào gọi `chay_giay.py`. `giay/cai_lich.sh` theo thiết kế chỉ **in** dòng crontab, không cài (dòng 2, 18–19).
  `chay_giay.py` mới chạy đúng 1 lần thủ công lúc 01:03 VN — trước nến H4 đầu tiên đóng sau mốc bắt đầu (03:00 VN 31/10) —
  nên chưa xử lý nến nào. Không phải do máy ngủ hay lỗi script (chưa có lần chạy tự động nào để lỗi).
- **Hệ quả:** 4.000$ của mỗi bot hiện là số khởi tạo, **chưa** phải kết quả chạy ngoài mẫu.
- **Lệnh user tự chạy để bật** (máy đang múi +07; script không tự cài):
  ```
  cd /Users/badat/linhtinh/trade_dai_han
  bash giay/cai_lich.sh     # chỉ in lại dòng lịch để xem
  (crontab -l 2>/dev/null; echo '5 3,7,11,15,19,23 * * * cd /Users/badat/linhtinh/trade_dai_han && /opt/homebrew/bin/python3 giay/chay_giay.py >> giay/cron.log 2>&1') | crontab -
  crontab -l                # kiểm đã có dòng chay_giay.py
  python3 giay/chay_giay.py # (tuỳ chọn) chạy bù ngay các nến H4 từ 03:00 VN 31/10
  ```
  Gỡ: `crontab -l | grep -v chay_giay.py | crontab -`.
- **Kiểm sau khi bật:** sau mỗi mốc 03/07/11/15/19/23 giờ 05 VN, `nen_cuoi` ≠ null và `cap_nhat_vn` mới; có `giay/nhat_ky.csv`
  và `giay/cron.log`. Máy ngủ thì cron bỏ lượt đó, lần chạy sau tự xử lý bù (idempotent).
- *Lưu ý: file này do `chay_giay.py` sinh lại mỗi lần chạy nên mục này sẽ bị ghi đè; bản lưu ở `kiem_cheo/VE_SINH_MOC.md` (phụ lục).*

Nến H4 mới nhất trong bộ đệm: BTC 2026-10-30 23:00 · ETH 2026-10-30 23:00 · OKB 2026-10-30 23:00 · BNB 2026-10-30 23:00 · Vàng 2026-10-30 23:00 · Dầu WTI 2026-10-30 23:00 (giờ đóng, VN).

## Tóm tắt

| Bot | Nến cuối đã xử lý (VN) | Số mốc nến | Số dư đã chốt | Vốn theo giá TT | Lãi/lỗ | % | Lệnh đã đóng | Thắng | Tổng R | Vị thế mở | Lệnh chờ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **v1** | chưa có | 0 | 4 000.00$ | 4 000.00$ | +0$ | +0,00% | 0 | — | 0,0 | 0 | 0 |
| **v2** | chưa có | 0 | 4 000.00$ | 4 000.00$ | +0$ | +0,00% | 0 | — | 0,0 | 0 | 0 |


## Bot v1 — v1 — luật chay.py (vào EMA34, SL giá, TP fractal)

**Vị thế đang mở**

_Không có._

**Lệnh chờ (limit)**

_Không có._

**Lệnh đã đóng** (mới nhất trước, tối đa 30)

_Chưa có._

**Tín hiệu tại nến H4 vừa xử lý**

_Chưa xử lý nến nào sau mốc bắt đầu._

## Bot v2 — v2 — v1 + 5 thay đổi (đi ngang, nến lớn, phá mốc, SL nến đóng, TP Fibo mở rộng; vàng scalp)

**Vị thế đang mở**

_Không có._

**Lệnh chờ (limit)**

_Không có._

**Lệnh đã đóng** (mới nhất trước, tối đa 30)

_Chưa có._

**Tín hiệu tại nến H4 vừa xử lý**

_Chưa xử lý nến nào sau mốc bắt đầu._

## Xem trước (CHƯA tính vào lệnh giấy)

_Chưa có nến H4 nào đóng sau mốc bắt đầu. Đây là quyết định hai bot SẼ ra nếu xét tại nến đã đóng gần nhất — chỉ để kiểm, không đặt lệnh._

| Tài sản | Nến (VN) | v1 | v2 |
|---|---|---|---|
| BTC | 2026-10-30 23:00 | **ĐẶT SHORT** (Hồi về EMA34 (v1)) vào 79563.6 · SL 80679.4 · TP1 76672.0 · TP2 76653.0 · R:R 2,6 · căn cứ Fractal+Fibo0.5+Fibo0.618 | **ĐẶT SHORT** (Sau nến lớn → Fibo 0.5) vào 79244.7 · SL 80356.0 · TP1 73940.9 · TP2 70565.2 · R:R 4,8 · căn cứ Fibo0.5nhip+EMA34+Fractal |
| ETH | 2026-10-30 23:00 | **ĐẶT SHORT** (Hồi về EMA34 (v1)) vào 2301.73 · SL 2349.23 · TP1 2178.35 · TP2 2159.25 · R:R 2,6 · căn cứ Fractal+Fibo0.618 | **ĐẶT SHORT** (Hồi về EMA34 (v1)) vào 2301.73 · SL 2349.23 · TP1 2100.57 · TP2 1973.4 · R:R 4,2 · căn cứ Fractal+Fibo0.618 |
| OKB | 2026-10-30 23:00 | Không đủ luật 1+2 (xu hướng H4 2 cây) | Không đủ luật 1+2 (xu hướng H4 2 cây) |
| BNB | 2026-10-30 23:00 | **ĐẶT SHORT** (Hồi về EMA34 (v1)) vào 727.63 · SL 743.667 · TP1 679.486 · TP2 676.049 · R:R 3,0 · căn cứ Fractal+Fibo0.618 | Đi ngang: cắt EMA89 ≥ 6 lần/30 nến (TĐ1) |
| Vàng | 2026-10-30 23:00 | Không có đích (luật 9 / TĐ5) | **ĐẶT SHORT** (Hồi về EMA34 (v1)) vào 4029.49 · SL 4069.85 · TP1 3840.86 · TP2 3840.86 · R:R 4,7 · căn cứ Fractal+Fibo0.618 |
| Dầu WTI | 2026-10-30 23:00 | R:R TP1 <1,5 | **ĐẶT LONG** (Phá mốc → test lại) vào 103.92 · SL 101.008 · TP1 108.902 · TP2 112.109 · R:R 1,7 · căn cứ MocDoiVai+Fractal |


---
_Ghi chú: vàng/dầu Yahoo trễ ~10 phút nên nến H4 chốt lúc +5 phút có thể thiếu vài phút cuối; mốc đã xử lý không làm lại. Chi tiết từng sự kiện: `giay/nhat_ky.csv`. Trạng thái đầy đủ: `giay/trang_thai_v1.json`, `trang_thai_v2.json`._
