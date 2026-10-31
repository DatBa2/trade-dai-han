# Nhờ Codex KIỂM CHÉO (31/10/2026) — việc A: rút phiếu độc lập

Cảm ơn bản phản biện `CODEX_NHAN_XET.md` — đã nhận và đang xử lý các điểm P0. Việc này giải quyết **P0-10 (kiểm nhãn độc lập)**
và một phần **P0-05 (tách hướng / hành động / chặng)**.

## Việc A — rút phiếu ĐỘC LẬP cho 23 buổi
Danh sách: `kiem_cheo/danh_sach.txt` (mỗi dòng: `<tên buổi>\t<đường dẫn transcript đã làm sạch>`).
**KHÔNG đọc** `phieu/`, `moc/`, `so_tay/`, `thi/`, `nhan_dinh_bot/` (để nhãn của bạn độc lập với nhãn cũ do Sonnet rút).
Chỉ đọc transcript trong danh sách + quy tắc chung bên dưới.

Với mỗi buổi, đọc HẾT transcript, ghi `kiem_cheo/codex_phieu/<tên buổi>.json`:
```json
{
  "buoi": "<tên buổi>",
  "gia_btc_luc_noi": 0,
  "dau_buoi": {"huong_h4": "TANG|GIAM|PHAN_VAN", "trich": "…"},
  "cuoi_buoi": {"huong_h4": "TANG|GIAM|PHAN_VAN", "trich": "…"},
  "doi_y_giua_buoi": true,
  "huong_lon": {"D1": "TANG|GIAM|PHAN_VAN|null", "W1": "…", "chu_ky": "…"},
  "hanh_dong": "vao_long|vao_short|giu_lenh|dung_ngoai_cho_entry|dung_ngoai_vi_lap_lung|chot_loi",
  "duong_di": [{"huong": "TANG|GIAM", "dich": 0, "khung": "H4"}],
  "dich_chinh": 0,
  "moc_sai": {"gia": 0, "dieu_kien": "vd: 2 nến H4 đóng trên 82.000"},
  "pha_vo_gia": "chỗ người đó nói là fake out / trap (nếu có), null nếu không",
  "do_chac": "cao|vua|thap",
  "ghi_chu": ""
}
```
Định nghĩa (quan trọng — tách 3 thứ khác nhau):
- **huong_h4** = người đó NGHIÊNG giá H4 đi đâu tiếp (kể cả khi đang đứng ngoài). **PHÂN VÂN chỉ khi thật sự lấp lửng**: giá ở ngay mốc quyết định, nói rõ phải chờ nến xác nhận, không nghiêng bên nào. Đứng ngoài vì chưa tới điểm vào KHÔNG phải PHÂN VÂN.
- **hanh_dong** = việc người đó làm/khuyên làm ngay bây giờ (tách khỏi hướng).
- **duong_di** = các chặng theo thứ tự (vd quét lên 82k rồi về 78k = 2 chặng); `dich_chinh` = đích chặng cuối.
- Ghi cả **đầu buổi** và **cuối buổi** (người đó hay đổi ý sau khi nến H4 11:00 đóng).
- Số giá: phụ đề hay viết "80.000 năm" = 80.500, "80.008" = 80.800 (đọc theo mức giá của buổi). Không chắc thì để null, không bịa.
- Kiểm JSON hợp lệ (`python3 -m json.tool`).

Cuối cùng ghi `kiem_cheo/CODEX_BAO_CAO_A.md`: bảng 23 buổi (đầu buổi / cuối buổi / hành động / đích / mốc sai / phá vỡ giả) + những buổi bạn thấy KHÓ gán nhãn và vì sao.
KHÔNG sửa file nào ngoài `kiem_cheo/`.

## Việc B — soi RÒ RỈ trong bộ dựng đề + bộ chấm (gửi 31/10 ~10:20)
Việc A đã xong, cảm ơn. Bài thi đang chạy (10 agent đang ghi vào `thi/bai_lam/`) → **CHỈ ĐỌC, KHÔNG sửa/xoá/chạy ghi
bất kỳ file nào trong `thi/`, `cong_cu/`, `du_lieu/`**. Chỉ ghi 1 file: `kiem_cheo/CODEX_BAO_CAO_B.md`. Không đọc `thi/bai_lam/`.

Đọc: `thi/tao_ho_so.py`, `thi/cham.py`, `cong_cu/cham_dich.py`, `thi/KHOA_CHAM.md`, `thi/SO_TAY_T1_T6.md`, vài hồ sơ mẫu
`thi/ho_so/*.md` (đầu kỳ 07-01, giữa kỳ, cuối kỳ 10-30), `transcripts/gio_live.tsv`. Được đọc `phieu/` + `du_lieu/` để đối chiếu.

Kiểm theo đúng P0-06 / P0-07 / P0-08 bạn đã nêu, cụ thể:
1. **Mốc cắt**: hồ sơ buổi X có chứa nến/EMA/RSI/F&G/pivot/Fibo nào tính bằng dữ liệu SAU giờ kết thúc live X không?
   Nến H4/D1/W1 đang chạy dùng OHLC tạm hay OHLC cuối? Fractal có trễ xác nhận đúng chưa? Múi giờ D1 (1Dutc vs VN)?
2. **View người đó ở buổi trước** trong hồ sơ: chỉ lấy từ phiếu các buổi CÓ GIỜ KẾT THÚC < mốc cắt? Có buổi nào trùng ngày
   (sáng + đêm) bị lấy nhầm buổi sau? "Mốc đã bị phá" tính bằng nến trước mốc cắt?
3. **Sổ tay `SO_TAY_T1_T6.md`**: có con số, sự kiện, mức giá hay câu nào chỉ xuất hiện từ 07/2026 trở đi (rò rỉ thói quen/giá
   giai đoạn thi) không? Liệt kê dòng nghi vấn.
4. **Bộ chấm `thi/cham.py` + `cham_dich.py`**: có tham số nào chỉnh được sau khi thấy bài làm để làm điểm đẹp lên? Cách chấm
   PHÂN VÂN, buổi thiếu nhãn (08-27 bị loại), mốc so sánh (luôn GIẢM, chép buổi trước, giữ view, luật từ trên xuống) có
   tính trên CÙNG tập buổi với bot không? Chấm thị trường (đích trước SL, hạn 14 ngày) có dùng dữ liệu sai thời điểm không?
5. Băm sha256 hiện tại của 4 file khoá có khớp `thi/KHOA_CHAM.md` không (`shasum -a 256`).
6. Kiến thức của model chấm: model làm bài có mốc kiến thức ~06/2026 — còn đường rò nào khác (vd tên file/ID video, ngày
   trong tên hồ sơ gợi ý sự kiện)?

Ghi `kiem_cheo/CODEX_BAO_CAO_B.md`: mỗi phát hiện = mức (P0 rò thật / P1 có thể rò / P2 vệ sinh) + file:dòng + bằng chứng
(dòng code hoặc trích hồ sơ) + cách sửa. Không thấy rò ở mục nào thì ghi rõ "đã kiểm, không thấy" kèm cách đã kiểm.
