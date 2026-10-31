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
