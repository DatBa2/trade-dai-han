# Đáp án v2 — luật phân xử (CHỐT 31/10/2026 trước khi có nhãn mới; không sửa sau khi thấy kết quả)

Lý do làm v2 (báo cáo `kiem_cheo/TONG_QUAN_VA_THIEU_SOT_2026-10-31.md` P0-1 + đối chiếu của Claude):
- Đáp án v1 (`phieu/`, Sonnet) rút PHÂN VÂN theo định nghĩa CŨ ("đứng ngoài" = PHÂN VÂN): 16/76 buổi thi; bot thi theo định nghĩa MỚI.
- Codex độc lập lệch v1 ở 6/23 buổi (3 trong kỳ thi: 07/08, 05/10, 23/10); 4 phiếu thi có hướng ≠ chặng cuối.

Cách làm:
1. Opus 5.5 rút nhãn MÙ cho 77 buổi thi + 3 buổi tranh chấp ngoài kỳ (06/03, 19/05, 22/06): chỉ đọc transcript,
   KHÔNG xem phiếu v1, nhãn Codex, bài làm bot, hồ sơ thi. Schema tách: thiên hướng H4 / chặng kế tiếp / đường đi /
   đích chính / hành động / mốc vô hiệu có cấu trúc (giá, khung, số nến) / trích dẫn kèm [giờ].
2. **Đáp án chính v2 = nhãn mới cuối buổi** cho cả 77 buổi (một người rút, một định nghĩa).
3. Báo cáo độ nhạy (đã chốt trước, báo cả 3, không chọn cái đẹp):
   (a) chấm theo v1; (b) chấm theo v2; (c) chỉ tập ĐỒNG THUẬN (v1 = v2, và = Codex nếu có).
4. Buổi v2 ≠ v1 và có nhãn Codex: ghi đa số 3 bên vào `PHAN_XU.md` để tham khảo; KHÔNG thay đáp án chính.
5. Đáp án v2 khoá bằng sha256 (`KHOA_DAP_AN.md`) TRƯỚC khi chạy chấm bot theo v2.
6. Nhãn cũ v1 giữ nguyên trong `phieu/` và `thi/_snapshot_v3_chan_doan/phieu/`.
