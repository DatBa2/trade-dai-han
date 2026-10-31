# Quy tắc rút phiếu nhận định (1 buổi live → 1 file JSON)

Phiếu là **nhãn để bot học bắt chước** người phân tích. Sai phiếu = bot học sai. Chỉ ghi điều người đó NÓI RA;
không suy diễn thêm, không tự phân tích chart. Mọi phán đoán quan trọng phải kèm câu trích nguyên văn.

Nguồn: `transcripts/lam_sach/<tên>.md` (bản sạch). Chỗ nào bản sạch có `[?]` hoặc số mơ hồ ảnh hưởng tới
hướng/đích/lệnh → mở bản gốc `transcripts/phu_de/<tên>.txt` để đối chiếu. Bẫy số: "X.000 năm" = X.500, "X.008" = X.800.

## Luật chọn HƯỚNG (quan trọng nhất)
- Chỉ 3 giá trị: `TANG` / `GIAM` / `PHAN_VAN`.
- Người đó hay nói 2 kịch bản ("nếu thủng… còn giữ…") → chọn **kịch bản chính** = cái họ nghiêng về / nói là xác suất cao /
  đặt lệnh theo / nhắc lại nhiều lần. Kịch bản kia ghi vào `kich_ban_phu`.
- `PHAN_VAN` chỉ khi họ thật sự không nghiêng bên nào: "đứng ngoài", "chưa rõ", "chờ tin", "sideway không đánh".
- Hướng tính theo **BTC**, không theo altcoin.
- Nhận định ở nhiều khung → mỗi khung một phần tử trong `nhan_dinh` (vd H4 giảm nhưng D1/tuần vẫn tăng).
- **Đổi ý giữa buổi** → `huong` lấy theo view **CUỐI buổi** (mới nhất); ghi view cũ vào `doi_y`
  (vd `"đầu buổi GIAM cao → cuối buổi chờ quét 83.000 rồi mới sale"`). Không đổi ý → `doi_y: null`.
- **Đường đi nhiều chặng** ("quét lên 82 rồi mới rớt về 78") → ghi `duong_di` theo thứ tự:
  `[{"huong": "TANG", "dich": 82000}, {"huong": "GIAM", "dich": 78000}]`; `huong` = hướng chặng CUỐI (đích chính).
  Chỉ 1 chặng → `duong_di: null`.
- Có vị thế nhưng không nghiêng hướng (vd "sale dò nhưng nhập nhằng") → `huong: PHAN_VAN`, lệnh vẫn ghi vào `lenh`.

## Định dạng `phieu/<tên>.json`
```json
{
  "buoi": "2026-10-29_1005_wcDxLBw0TO4",
  "ngay": "2026-10-29",
  "gio_vn": "10:05",
  "gia_btc_luc_noi": 79500,
  "nhan_dinh": [
    {
      "khung": "H4",
      "huong": "GIAM",
      "do_chac": "cao",
      "dich": [77000, 78000],
      "han": "trong ngày",
      "han_gio": 24,
      "vo_hieu_khi": "H4 đóng trên 80.000",
      "kich_ban_phu": "hồi lên 80.000 rồi mới giảm",
      "ly_do": ["H4 đóng nến đỏ dưới 80.000", "đỉnh thấp dần", "tăng chậm xả nhanh = phân phối"],
      "trich": "Hôm nay Bitcoin view xuống phải không? Đối với nến H4 mà nếu nó đóng ở đây thì đúng rồi."
    }
  ],
  "vung_gia": {"khang_cu": [80000, 81000], "ho_tro": [77000, 78000]},
  "lenh": [
    {"chieu": "SHORT", "loai": "limit", "vao": 81000, "tp": [78000], "sl": 82000,
     "trang_thai": "de_xuat_moi", "trich": "…"}
  ],
  "nhin_lai_truoc": "Đêm qua quét SL entry 81.500 sau khi TP; xu hướng không đổi.",
  "cong_cu": ["H4", "Fibo 0.5", "RSI M5", "cấu trúc đỉnh đáy", "BTC.D"],
  "tin_tuc": [{"tin": "FOMC", "danh_gia": "tin ra thị trường quét 2 đầu, hợp lý hoá đường giá"}],
  "thoi_quen": ["chờ nến H4 đóng mới khẳng định", "cảnh báo FOMO khi đám đông tin uptrend"],
  "cau_cua_mieng": ["anh em hãy biết sợ nhá"],
  "altcoin": [{"coin": "ETH", "huong": "GIAM", "ghi": "về support nhưng trước đó gãy, phòng giảm sâu"}],
  "ghi_chu": ""
}
```

## Giải thích trường
| Trường | Ghi gì |
|---|---|
| `gia_btc_luc_noi` | giá BTC người đó nhắc là giá hiện tại lúc live; không có → `null` |
| `khung` | `M5` `M15` `H1` `H4` `D1` `W1` hoặc `"chung"` nếu không nói khung |
| `do_chac` | `cao` (chắc chắn, "gần như chắc chắn") · `vua` · `thap` ("có thể", "mình đoán") |
| `dich` | 1 số hoặc [thấp, cao]; không nói → `null` |
| `han` / `han_gio` | lời gốc + quy ra giờ: trong ngày 24 · vài ngày 72 · tuần này/cuối tuần 168 · không nói → `null` |
| `vo_hieu_khi` | mốc mà người đó nói "nếu thế này thì view sai/đổi" — KHÔNG phải nước đôi, là điểm cắt |
| `lenh.trang_thai` | `de_xuat_moi` · `dang_giu` · `da_khop` · `da_chot` · `da_cat` |
| `nhin_lai_truoc` | người đó tự đánh giá nhận định/lệnh buổi trước đúng/sai thế nào |
| `thoi_quen` | hành vi lặp lại có thể bắt chước (cách vào lệnh, chờ xác nhận, thái độ trước tin, quản lý vốn) |
| `cau_cua_mieng` | 1–5 câu đặc trưng giọng nói, trích nguyên văn |
| `altcoin` | nhận định ETH/altcoin/BTC.D ngắn gọn (không tính vào hướng BTC); không nói → `[]` |

Số giá ghi dạng số nguyên đầy đủ (79500, không phải "79.5K"). Không có thông tin → `null` hoặc `[]`, KHÔNG bịa.
JSON phải hợp lệ (kiểm bằng `python3 -m json.tool <file>`).
