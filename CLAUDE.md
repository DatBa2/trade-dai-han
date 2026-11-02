# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Dự án

Tái tạo tư duy + thói quen nhận định BTC của một người phân tích (kênh YouTube FAM Trading) từ 180 buổi livestream
(06/01 → 30/10/2026). Thước đo chính là **độ giống người đó**, lãi/lỗ là phụ. Yêu cầu user đã chốt: `DESIGN.md`.

**Base để phát triển: bot v5** (`bot_v5/`, lệnh `/nhan-dinh`). v1, v2, v3 (bộ thi `thi/`), v4 đã gỡ khỏi repo ngày
02/11/2026 — đừng dựng lại; cần tra thì `git show c19482b:<đường dẫn>`. Của v3 chỉ còn `thi/du_lieu/btc_*_bo_sung.csv`
(nến bổ sung `cong_cu/dieu_kien.py` đọc) và `thi/dap_an_v2/nhan/` (nhãn T7–T10 mà `hoc_v5/kiem_nhan.py` so) — không xoá.
`AGENTS.md` là hướng dẫn cũ cho Codex, đã lỗi thời.

## Môi trường Windows

- Chỉ có `python` 3.11 (không có `python3`). Console cp1258 → in tiếng Việt crash `UnicodeEncodeError`.
  **Luôn chạy `python -X utf8 <script>`**. Docs/docstring ghi `python3` thì đổi thành vậy.
- `allowed-tools` của `/nhan-dinh` chỉ whitelist `python3 bot_v5/...` → trên máy này sẽ hỏi quyền.
- Chỉ stdlib, không có dependency manifest; script tự `sys.path.insert(0, GOC / "cong_cu")`. Chạy từ thư mục gốc repo.

## Lệnh

Không có test framework: mỗi phần có script tự kiểm in PASS/FAIL, exit 1 khi FAIL; chạy một test = chạy đúng script đó.
Đều offline (dùng cache có sẵn):

```
python -X utf8 bot_v5/kiem_tra_so_tay_den.py     # sổ tay lọc theo T không còn ngày ≥ T
python -X utf8 bot_v5/kiem_tra_ngu_canh.py       # xoá / đầu độc dữ liệu sau T → hồ sơ giống hệt
python -X utf8 hoc_v5/kiem_nhan.py               # 180 file nhãn, trích dẫn phải nguyên văn trong transcripts/
python -X utf8 hoc_v5/trendline/kiem_tra.py
```

```
python -X utf8 bot_v5/so_tay_den.py "2026-09-21 11:00"            # → bot_v5/_so_tay_T/20260921_1100/
python -X utf8 bot_v5/ngu_canh.py BTC 4H "2026-08-14 11:00"       # --json · --so-nen N · --utc · --offline
```

## Kiến trúc

**Luồng dữ liệu** (tầng trước là input chỉ đọc của tầng sau): `transcripts/` → phiếu + mốc giá (`phieu/`, `moc/`) →
nhãn v5 rút mù (`hoc_v5/nhan/`) → phân tích hành vi (`hoc_v5/giu_lat/`, `hoc_v5/trendline/`) → sổ tay
(`so_tay/SO_TAY_TINH_HOA.md`, `bot_v5/so_tay/`) → bot v5.

**v5 — Claude nhập vai, code chỉ chuẩn bị dữ liệu.** Lập luận nằm trong `bot_v5/NHAP_VAI.md` (quy trình từ trên xuống,
định nghĩa TĂNG/GIẢM/PHÂN VÂN, giữ view) + `bot_v5/MAU_TRA_LOI.md` (khuôn 11 mục + file đối chiếu). `/nhan-dinh`: đọc 2
file luật → MÃ/KHUNG/T → `so_tay_den.py` → đọc 4 file sổ tay đã lọc → `ngu_canh.py` → phân tích → lưu
`bot_v5/doi_chieu/<ngày T>_<MÃ>.md` (user tự điền "Kết quả thật"). Mọi sửa ghi vào `bot_v5/NHAT_KY_SUA.md`.
- `nen.py`: nến OKX (`<MÃ>-USDT`, fallback `-USDT-SWAP`) + Yahoo (VANG, DAU, DXY, NASDAQ, CME = BTC=F) + proxy
  BTC.D / USDT.D từ CoinMarketCap (`lay_dom`, lưu cache dạng nến để phép thử đầu độc phủ luôn); cache `bot_v5/cache/`
  giờ UTC; cửa sổ cố định theo T nên kết quả chỉ phụ thuộc T.
- `ngu_canh.py`: EMA34/89/200/610, RSI, fractal, Fibo, trendline, râu chưa test, lịch tin + FOMC + Polymarket
  (`du_lieu/tin_tuc/*.csv`), F&G, tóm tắt BTC; mục 7 (chỉ crypto): gap CME chưa lấp + BTC.D / USDT.D proxy.
- `so_tay_den.py`: bỏ mọi dòng sổ tay có mốc ngày ≥ ngày của T để chặn lộ view thật của người đó.

**Đo độ giống**: chưa có công cụ chấm trong repo (bộ chấm v3 đã gỡ). Nhãn hướng H4 cuối buổi của người đó: `hoc_v5/nhan/`
(180 buổi). Lần đo gần nhất (02/11/2026, 20 buổi T7–T10, bản trước/sau, trong mẫu) + thiết kế chốt trước: `bot_v5/NHAT_KY_SUA.md`.
Kết luận thật cần buổi live MỚI (sau 30/10/2026), dự báo lưu trước khi xem đáp án.

**Thư viện chung `cong_cu/`**: `chi_bao.py`, `trendline.py`, `tin_tuc.py`, `dieu_kien.py`, `cham_dich.py`, `lay_nen.py` —
dùng chung cho hoc_v5, bot_v5. `trendline.py` đọc nến từ `bot_v4/du_lieu/`, `dieu_kien.py` đọc thêm
`thi/du_lieu/btc_*_bo_sung.csv` — hai chỗ sót lại của bản cũ, không xoá.

## Bất biến

- **Không nhìn tương lai**: mọi dữ liệu cắt ở nến **đã đóng** ≤ T trước khi tính. Sửa `nen.py`, `ngu_canh.py`,
  `so_tay_den.py` → chạy lại 2 script kiểm bot_v5, phải PASS. Model biết giá tới ~06/2026 → T < 2026-07-01 phải in cảnh báo.
- **Giờ VN (UTC+7)**, `YYYY-MM-DD HH:MM`. H4 đóng 03/07/11/15/19/23h; D1 07:00; tuần 07:00 thứ Hai.
  Ghi 3 trường riêng `gio_live`, `gio_cat`, `gio_phat_hanh` (DESIGN.md "Quy ước giờ").
- **Khi chạy `/nhan-dinh`**: không subagent, không WebSearch/WebFetch, không đọc file cấm ở `NHAP_VAI.md` §1.4
  (`bot_v5/so_tay/` gốc, `so_tay/SO_TAY_TINH_HOA.md`, `transcripts/`, `phieu/`, `moc/`, `bang_chung/`, `hoc_v5/`, `thi/`,
  `so_tay/ghi_chu/`, `so_tay/khung/`, `nhan_dinh_bot/`, `doi_chieu/`, `bot_v5/doi_chieu/`) — đọc là thấy đáp án.
- **File khoá sha256 — không sửa** (sửa = kết quả cũ mất hiệu lực); cần đổi thì báo user, làm bản mới:
  - `hoc_v5/KHOA_NHAN.md` (bộ nhãn), `hoc_v5/giu_lat/LUAT_KHOA.md` (gồm `dac_trung.py`, `phan_tich.py`).
  - `cong_cu/cham_dich.py`, `cong_cu/dieu_kien.py`, `thi/dap_an_v2/nhan/` (từng khoá trong `thi/KHOA_CHAM.md` đã gỡ;
    kết quả `hoc_v5/giu_lat/` dựa vào chúng).
- **Trung thực, không chỉnh theo kết quả**: thiết kế/luật chốt trước khi chạy; luật sổ tay phải có nguồn là lời/hành vi
  người đó. Phản biện độc lập bằng Codex: prompt `GUI_CODEX_*.md`, kết quả `CODEX_NHAN_XET.md`, `kiem_cheo/`.
- **Thu transcript** (`cong_cu/lay_transcript.py`): giữ giãn cách 60 giây/lần gọi YouTube, dừng khi bị chặn, Whisper
  luôn `--vad`; không đụng `transcripts/_cu/`, phụ đề gốc, schema `transcripts/danh_sach.tsv`.

## Commit

Subject ngắn, mệnh lệnh, tiếng Anh. Tách commit code với commit nhập dữ liệu hàng loạt.
