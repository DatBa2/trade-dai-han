# Quy tắc rút MỐC GIÁ BTC (1 buổi live → 1 file JSON)

Mục đích: kiểm bằng số liệu xem mỗi con số người đó nêu dựa trên căn cứ gì (Fibo, MA, đỉnh/đáy cũ, trendline,
gap, thanh lý, số tròn…). Ghi **MỌI mốc giá BTC** người đó nêu có vai trò phân tích (không ghi giá kể chuyện vu vơ
kiểu "hồi xưa mua 20K"). Chỉ BTC (bỏ ETH, altcoin, vàng). Không bịa; căn cứ chỉ ghi khi người đó NÓI RA.

Bẫy số phụ đề: "X.000 năm" = X.500, "X.008" = X.800, "80.00" có thể là 80.000 hoặc thiếu lẻ → không chắc thì `"chac": false`.
Người đó hay nói tắt "76", "7x", "8 mấy" = 76.000, 70–79K… → quy ra số đầy đủ; dải "7x" → `gia_duoi` 70000, `gia_tren` 79999.

## Định dạng `moc/<tên file gốc bỏ đuôi>.json`
```json
{
  "buoi": "2026-01-06_aQbHs7J80jc",
  "ngay": "2026-01-06",
  "gia_btc_luc_noi": 94000,
  "moc": [
    {
      "gia": 92500, "gia_tren": null,
      "vai_tro": "ho_tro",
      "huong": "GIAM",
      "khung": "H4",
      "can_cu": ["Fibo 0.618 sóng 89.000→96.000", "MA89 H4"],
      "moc_gio": "00:23:10",
      "chac": true,
      "trich": "về 92.5 là Fibo 0.618 trùng MA89 khung H4 anh em ạ"
    }
  ]
}
```
| Trường | Ghi gì |
|---|---|
| `gia` / `gia_tren` | 1 mốc → `gia`, `gia_tren: null`; vùng → `gia` = cận dưới, `gia_tren` = cận trên |
| `vai_tro` | `dich` · `ho_tro` · `khang_cu` · `entry` · `sl` · `tp` · `vo_hieu` (mốc làm view sai) · `dinh_cu` · `day_cu` · `khac` |
| `huong` | mốc này phục vụ view TANG / GIAM / null |
| `khung` | khung người đó đang xem khi nói (`M15` `H1` `H4` `D1` `W1` hoặc null) |
| `can_cu` | danh sách căn cứ người đó NÓI cho mốc này, ghi cụ thể nhất có thể: `"Fibo 0.5"`, `"Fibo 0.618 sóng A→B"`, `"MA34 D1"`, `"MA200 H4"`, `"đỉnh cũ 15/01"`, `"râu nến ngày 20/01"`, `"trendline đáy"`, `"gap CME"`, `"cụm thanh lý / heatmap"`, `"số tròn"`, `"vùng giá trị / volume"`, `"mô hình vai đầu vai"`, `"đáy 2 / 2 đáy"`… Không nói → `[]` |
| `moc_gio` | mốc [hh:mm:ss] của câu (file zip_clean có sẵn); file không có mốc → null |
| `tai_san` | (thêm 31/10) `BTC` · `ETH` · `SOL` · `VANG` · `DAU` · `KHAC` · `CHUA_RO`. Câu đang nói coin/hàng hoá khác (kể cả khi số nghe giống giá BTC, vd dầu "60", SOL "73 74") → ghi đúng tài sản + `chac: false`; không chắc đang nói BTC → `CHUA_RO` + `chac: false`. Gắn/kiểm lại bằng `cong_cu/ve_sinh_moc.py` |
| `chac` | false nếu số nghe không chắc (bẫy phụ đề) — hoặc mốc không phải BTC / chưa rõ tài sản |

Cùng một mốc nhắc lại nhiều lần → ghi 1 lần (lần nói rõ căn cứ nhất). Cùng giá nhưng 2 vai trò → 2 dòng.
Mốc kỳ vọng cũ đem ra nhắc lại ("hôm qua mình kỳ vọng 69.500") → `vai_tro: "nhac_lai"`.
Số do NGƯỜI XEM nói → bỏ, trừ khi người đó dùng lại làm mốc của mình. "5x" → `gia` 50000, `gia_tren` 59999.
**Căn cứ ghi CÀNG CỤ THỂ CÀNG TỐT** (máy sẽ truy ngược công thức): Fibo thì ghi mức + kéo từ đâu tới đâu + khung
(vd "Fibo 0.618 kéo từ đáy 60K ngày 06/02 lên đỉnh 76K, khung D1"); MA thì ghi số + khung (+ "EMA" nếu nói); đỉnh/đáy thì ghi ngày.
JSON hợp lệ (`python3 -m json.tool`).
