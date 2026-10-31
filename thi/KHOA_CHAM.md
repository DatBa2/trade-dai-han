# KHOÁ BÀI THI v3 — 31/10/2026 10:06

Khoá TRƯỚC khi sinh bài làm (Codex P0-11). Sửa bất kỳ file dưới đây sau thời điểm này = kết quả không còn là bài thi hợp lệ.

| File | sha256 |
|---|---|
| `thi/cham.py` | `1d28f2402c06fc46…` |
| `cong_cu/cham_dich.py` | `2c573d21212263bd…` |
| `thi/tao_ho_so.py` | `f98633998531a540…` |
| `thi/SO_TAY_T1_T6.md` | `196594481702a8d4…` |

## Thiết lập
- Model: Claude Opus 5.5 (`claude-opus-5-5`), mốc kiến thức theo nhà cung cấp: 06/2026. Buổi thi 01/07→30/10/2026.
- Chế độ: CÓ view người đó ở các buổi trước (họ nói công khai trước mốc cắt) + bản đồ mốc 5 buổi trước.
- Mốc cắt dữ liệu của bot = lúc KẾT THÚC live (giờ thật từ transcripts/gio_live.tsv); nhãn = view CUỐI buổi của người đó.
- Sổ tay thi chỉ từ T1–T6 (`thi/SO_TAY_T1_T6.md`).
- Chấm: hướng H4 (3 nhãn, có hướng, kappa, bootstrap 95%, McNemar) so với luôn GIẢM / chép buổi trước / giữ view / luật từ trên xuống, CÙNG tập buổi; đích-trước-SL hạn 14 ngày (`cong_cu/cham_dich.py`); đợt view; PHÂN VÂN riêng; phép thử đối xứng.
- Lộ đề đã biết, không gỡ được hoàn toàn: người thiết kế (tôi) đã xem toàn bộ 180 buổi khi viết đặc tả; luật "giữ view" và "chu kỳ 4 năm" do user nhấn mạnh sau khi xem dữ liệu cả năm.

## Khoá v2 (sau khi sửa P0 — xem `thi/SUA_P0.md`), 2026-10-31 10:47 VN
Khoá v1 ở trên GIỮ NGUYÊN (bản đó + bài làm lượt chẩn đoán nằm trong `thi/_snapshot_v3_chan_doan/`).
Đáp án chính v2: `thi/dap_an_v2/phieu/` — băm ở `thi/dap_an_v2/KHOA_DAP_AN.md`.

| Tệp | sha256 |
|---|---|
| `thi/cham.py` | `18a51a39674c2ff0a97f2a802d7648198dbbe20839e2a18c708cde7c90084500` |
| `cong_cu/cham_dich.py` | `e4fac3af3a581312b88017a49d3a7bacba55e232eb18a7314b13164a4ff34db7` |
| `cong_cu/dieu_kien.py` | `1605a5b12894b7e0a895d491c6e44f287ef994480195f28e95022de80846e51d` |
| `thi/tao_ho_so.py` | `a61bc9f480ea9c3e5cf8a4ee59749f57f58ce83d4508a79a6cfec13de25aea4c` |
| `thi/SO_TAY_T1_T6.md` | `196594481702a8d4e6978b573a19d3f5a08eaf297d57f85aa9c773cf28fd2119` |
| `thi/kiem_thu_cham.py` | `3e69dfae888582992117fd5dbe6cf9416d69c24a618628364922ef5301de92bc` |
| `thi/dap_an_v2/dung_dap_an.py` | `aecb2e75f5e8f2e2a88af86e0617cb0048fc329405b2b82ee23f9f57b86b3276` |

## Khoá v2.1 (P1-7: cờ `--ban 3` thêm volume + EMA tháng + mục "dữ liệu không có"), 2026-10-31 11:01 VN
- `thi/tao_ho_so.py`: `a4cc560d6fbcd76cee8d31c51fbad66c62c20eca616b5e353c94ace82b3c89c4` (thay hash v2 a61bc9f4…).
- Kiểm (Claude tự chạy): mặc định (bản 2) dựng lại vào thư mục tạm → `diff -rq` với `thi/ho_so_v2/` GIỐNG HỆT 77/77; `kiem_thu_cham.py` 8/8 PASS.
- `thi/ho_so_v3/` (77 hồ sơ, `--ban 3`) dành cho lượt thi Claude-suy-luận kế tiếp; kiểm cắt tương lai bản 3: 77/77 giống hệt.

## Khoá v2.2 + sự cố (2026-10-31 11:18 VN)
- `thi/tao_ho_so.py`: `6c5fbfe928889604352e8c7807604e4ee5fdfb9144351e7702ead7a1c77587a8` — thêm: bản 3 bỏ mốc `tai_san` ≠ BTC (P1-5); mặc định `--ra` theo bản
  (bản 3 → `thi/ho_so_v3`).
- **Sự cố (Claude gây ra):** lệnh `--ban 3 --kiem` (không có `--ra`) đã ghi đè `thi/ho_so_v2/` bằng hồ sơ bản 3. Đã KHÔI PHỤC: dựng lại bản 2 với
  `moc/` GỐC trong `thi/_snapshot_v3_chan_doan/moc` (thư mục gốc ảo bằng symlink, không đụng `moc/`) → 77 hồ sơ; kiểm: 19 dòng
  "ĐÃ KÍCH HOẠT → chưa kích hoạt" so với `thi/ho_so/` — khớp `thi/SUA_P0.md`. Đã sửa mặc định để không tái diễn.
- Lưu ý tái lập: `moc/` đã vệ sinh (P1-5: `tai_san`, `chac:false` cho 6 mốc không phải BTC; P2: đổi chỗ 21 mốc đảo cận) → dựng bản 2 với
  `moc/` HIỆN TẠI khác `thi/ho_so_v2/` ở 22 hồ sơ, CHỈ ở thứ tự 2 cận và dấu "(?)". Muốn tái lập byte-giống `ho_so_v2` → dùng moc snapshot.
