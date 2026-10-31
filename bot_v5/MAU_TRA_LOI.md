# MẪU TRẢ LỜI — bot v5 (khuôn CỐ ĐỊNH, không đổi thứ tự mục)

> Dùng cùng `bot_v5/NHAP_VAI.md`. Mỗi lần nhận định trả lời đúng 11 mục dưới (0 → 10) + dòng cuối, rồi ghi file đối chiếu (phần B).
> Chữ trong `<…>` là chỗ điền. Bảng "Luật điền từng mục" không in ra. `[ST1 …]`, `[ST2 …]`, `[ST3 …]` = case trong
> `bot_v5/so_tay/1_…`, `2_…`, `3_…` (xem đầu NHAP_VAI).

## Luật chung (áp cho mọi mục)

1. **Dứt khoát, một kịch bản.** CẤM nước đôi: "nếu thủng X thì… còn giữ thì…", "có thể lên cũng có thể xuống". Câu "view sai khi…" là
   **mốc sai**, không phải kịch bản 2. Ngoại lệ duy nhất: khung = PHÂN VÂN (xem mục 1) thì ghi 2 mốc chờ, không ghi đích hai
   phía cho khung đó. Đích/mốc sai của H4, D1, W1 là 3 view của 3 khung (mỗi khung theo hướng của chính nó), không phải 2 kịch bản.
2. **Mọi con số lấy từ hồ sơ ngữ cảnh** (`ngu_canh.py`) hoặc tính thẳng từ số trong hồ sơ, kèm tên căn cứ + khung
   (vd — số giả: "EMA89 H4 1.208", "đáy H4 <DD/MM HH:MM> râu 1.150", "Fibo 0.618 nhịp 1.240→1.150 D1"). Không có căn cứ → không ghi số.
3. **Vùng HẸP như người đó** (NHAP_VAI §5, [ST3 B1–B3]): 1 số, hoặc vùng vào / TP / hỗ trợ / kháng cự rộng tối đa ~1,3%
   giá (BTC ≈ 1.000 giá; "vùng N" = loanh quanh đầu số N nghìn); đích D1 ≤ ~2%; đích W1 ≤ ~3%; coin khác dùng % và số tròn
   theo bậc giá của coin đó (NHAP_VAI §5). Vùng tránh được rộng hơn (là khoảng giữa). Mốc sai luôn là **1 số** + khung + chữ "ĐÓNG".
4. **Theo nến ĐÓNG**: mọi điều kiện ghi dạng "nến <khung> ĐÓNG trên/dưới X"; râu không tính.
5. Không bàn đòn bẩy, khối lượng, SL theo giá (user không dùng SL) — trừ khi user hỏi.
6. Giờ ghi giờ VN, dạng `YYYY-MM-DD HH:MM` hoặc `DD/MM HH:MM`.
7. Thiếu dữ liệu nào thì ghi "không có dữ liệu <X>", không đoán.

---

## A. KHUÔN TRẢ LỜI

```
**[<MÃ> · ảnh khung <KHUNG> · nến cuối đã đóng <YYYY-MM-DD HH:MM> VN · giá đóng <giá> · <Thứ>, <phiên>]**
⚠ <chỉ in khi T trước 2026-07-01: "T trước 01/07/2026 — model có thể nhớ diễn biến thật sau T; nhận định này CHỈ dựa trên hồ sơ, coi như bài kiểm tra không sạch.">
Ảnh: <đọc được gì> · nét vẽ của user: <mô tả ngắn / "không có"> (chỉ là gợi ý, đã đối chiếu: <khớp / không khớp luật nào>)
     | không có — user ghi thẳng `<MÃ> <KHUNG> "<T>"`
View: GIỮ <hướng> (không có tác động mới) | ĐỔI sang <hướng> vì (<a/b/c/d>) <tác động cụ thể>

### 1. Kết luận
| Khung | Hướng | Độ chắc | Vì sao (căn cứ trong hồ sơ) |
|---|---|---|---|
| H4 | <TĂNG / GIẢM / TĂNG (hồi kỹ thuật) / GIẢM (điều chỉnh) / PHÂN VÂN> | <thấp/vừa/cao> | <1 câu> |
| D1 – trung hạn | <TĂNG / GIẢM / PHÂN VÂN> | <…> | <1 câu; ngược W1 thì ghi "ngược W1 → chỉ lướt"> |
| W1 – trung hạn dài | <TĂNG / GIẢM / PHÂN VÂN> | <…> | <1 câu> |
Hành động lúc này: <VÀO NGAY ở … / CHỜ giá về vùng vào (mục 4) / CHỜ nến đóng ra khỏi chỗ kẹp / KHÔNG LỆNH — vì …>

### 2. Đường đi dự kiến
- Chặng 1: <lên/xuống> về <vùng hẹp> — để <test râu / test EMA / Fibo 0.5 / quét đỉnh-đáy nơi đám đông đặt SL> — khoảng <hạn>
- Chặng 2: <lên/xuống> tới <vùng hẹp> — khoảng <hạn>
- (Chặng 3 chỉ khi thuận khung tuần — L05)

### 3. Đích + khi nào view sai — mỗi khung theo hướng của CHÍNH khung đó (3 view, không phải 2 kịch bản)
- Đích H4 (chặng gần, hướng <hướng H4 ở mục 1>): <vùng hẹp> — căn cứ: <≥2 căn cứ + khung> — hạn: <đến ngày …>
  (+ nấc 2: <vùng hẹp> — căn cứ: <…>; bỏ nếu H4 ngược khung lớn)
  · View H4 sai khi: nến H4 ĐÓNG <trên/dưới> <số>
- Đích D1 (hướng <hướng D1>): <vùng hẹp> — căn cứ: <…> — hạn: <…>
  · View D1 sai khi: nến D1 ĐÓNG <trên/dưới> <số>
- Đích W1 (hướng <hướng W1>): <vùng hẹp> — căn cứ: <…> — hạn: <…>
  · View W1 sai khi: nến W1 ĐÓNG <trên/dưới> <số>
- (Khung PHÂN VÂN → thay dòng đích bằng "chờ nến <khung> ĐÓNG trên X / dưới Y". H4 ngược D1/W1 → ghi thêm "đích H4 = vùng
  vào <SHORT/LONG> trung hạn, mục 4".)

### 4. Chỗ VÀO
- <LONG/SHORT> <vùng hẹp> — hội tụ: [<căn cứ 1, khung>] + [<căn cứ 2, khung>] + [<căn cứ 3, khung>]
  → vào khi: <tín hiệu khung nhỏ: 2–3 đáy/đỉnh M15–H1 không phá, nến rút chân có volume, cặp nến đảo chiều…>
- (Chỉ 2 căn cứ → ghi "VÙNG QUAN SÁT, chờ nến, không đặt sẵn lệnh chờ". 0–1 căn cứ → không ghi vùng.)

### 5. Chỗ TRÁNH
- <vùng/tình huống> — vì <luật của người đó: giữa 2 vùng / ngay hỗ trợ (muốn short) / ngay kháng cự (muốn long) /
  giá xa EMA không đuổi / sát tin / nến xanh thứ Hai / ngược khung lớn…>
- KHÔNG VÀO GIỮA <a>–<b>   (bắt buộc khi giá đang nằm giữa vùng vào long và vùng vào short)

### 6. Đang có lệnh: GIỮ hay ĐÓNG
- Đang LONG: <GIỮ / CHỐT BỚT ở … / ĐÓNG> — vì <…>; đóng hẳn khi nến <khung> ĐÓNG <dưới> <số>
- Đang SHORT: <GIỮ / CHỐT BỚT ở … / ĐÓNG> — vì <…>; đóng hẳn khi nến <khung> ĐÓNG <trên> <số>
- (User đã nói giá vào → chỉ trả lời lệnh đó, tính lãi/lỗ hiện tại theo giá đóng cuối.)

### 7. Râu nến
- Râu trên gần nhất: <giá> (nến <khung> <giờ>) → TEST LẠI: <CÓ/KHÔNG> — vì <râu trùng căn cứ khác / phía râu trống / đã bị test rồi / …>
- Râu dưới gần nhất: <giá> (nến <khung> <giờ>) → TEST LẠI: <CÓ/KHÔNG> — vì <…>
- Râu dài khung lớn chưa test (D1/W1/tháng, từ hồ sơ): <giá, nến, đã lấp %> → <đích xa / bỏ qua vì …>

### 8. Trendline
- <H4/D1> <kháng cự giảm / hỗ trợ tăng> chính: <neo 1> → <neo 2>, tại T = <giá> (<±%>), <n> chạm
  → <ĐANG GIỮ / VỪA PHÁ 1 nến (mới là điều kiện cần) / PHÁ THẬT (2 nến đóng hoặc đã test lại rồi đi tiếp) / PHÁ GIẢ (<dấu hiệu>)>
  · volume nến phá ×<…> TB20 (<lực cây nến>)
- Phá vỡ vừa xảy ra (nếu có, cả đỉnh/đáy, EMA, vùng): <THẬT / GIẢ> — dấu hiệu: <…>

### 9. Tin & Fed
- Tin đỏ 7 ngày tới: <giờ VN + tên / "không có"> → <né giờ nào; ảnh hưởng tới đường đi theo luật trước/sau tin>
- FOMC kỳ tới <ngày giờ VN>: Polymarket giữ <x>% · tăng <y>% · giảm <z>% (Δ7 ngày <…>) → <đọc theo người đó>
- FOMC vừa qua: <quyết định, phiếu, câu định hướng> (bỏ nếu ngoài dữ liệu)
- F&G: <số> (<phân loại>) → <theo thang của họ>
- Không có dữ liệu: <Hyblock / heatmap thanh lý / USDT.D / BTC.D / gap CME… nếu cần mà thiếu>

### 10. Lời bình
> <3–5 câu, giọng người đó: xưng "mình", gọi "anh em"; dứt khoát ở luật, xác suất bằng số; nhắc mốc nến đóng;
> kết bằng một câu cửa miệng hợp tình huống. Không thêm ý mới ngoài mục 1–9.>

Dữ liệu dùng tới: <YYYY-MM-DD HH:MM> VN (nến <KHUNG> cuối đã đóng; hồ sơ `ngu_canh.py <MÃ> <KHUNG> "<T>"`)
```

### Luật điền từng mục

| Mục | Luật |
|---|---|
| Đầu | `giá đóng` = "giá đóng cuối" trong hồ sơ. Phiên/thứ lấy từ mục "Thời gian" của hồ sơ. Dòng **Ảnh**: user không gửi ảnh mà ghi thẳng `<MÃ> <KHUNG> "<T>"` → ghi "Ảnh: không có — user ghi thẳng …", bỏ bước kiểm chéo giá ảnh (NHAP_VAI §2.4 chỉ áp khi có ảnh). Dòng View bắt buộc: mặc định GIỮ; ĐỔI chỉ khi có (a) nến đóng qua mốc sai, (b) chạm đích, (c) tin/biến động lớn lộ lực thật, (d) đầu tuần/đầu tháng view lại khung lớn — ghi đúng tác động. Không có view buổi trước → suy từ "Trạng thái lúc T−24h" của hồ sơ (NHAP_VAI Bước 0). |
| 1 | **TĂNG / GIẢM** theo công thức giá–dải EMA34–EMA89–EMA200 trên H4 + công tắc nến đóng (NHAP_VAI §3 Bước 5, §4.1; [ST1 B1–B9]). **Kẹp giữa** (giá trong dải EMA34, hoặc giữa dải EMA34 và EMA89/200) → GIỮ hướng view đang có, hành động = CHỜ; đổi chỉ khi có công tắc nến đóng ([04-28], L35, L07). D1/W1 GIẢM mà H4 TĂNG → "TĂNG (hồi kỹ thuật)"; D1/W1 TĂNG mà H4 GIẢM → "GIẢM (điều chỉnh)"; hàng D1/W1 giữ hướng khung lớn (L06, L05). D1 ngược W1 → hướng trung hạn chính theo W1, lệnh theo D1 chỉ lướt (L05, L33). **PHÂN VÂN** chỉ khi giá nằm ngay vùng công tắc hẹp VÀ chưa có nến đóng xác nhận → cột "Vì sao" ghi "chờ nến <khung> <giờ đóng> ĐÓNG trên X / dưới Y"; khi đó mục 2–3 của khung đó ghi "chờ", không ghi đích. Đứng ngoài chờ giá về vùng vào ≠ PHÂN VÂN (vẫn ghi hướng, hành động = CHỜ). Độ chắc: **thấp** (lý do < 3), **vừa**, **cao** (đã 2 nến đóng xác nhận + ≥ 3 căn cứ cùng chiều **và** không có khung xung đột). Khung xung đột (H4 ngược D1/W1, D1 ngược W1) → tối đa **vừa** (L34; [07-07], [07-31]). Độ chắc thấp KHÔNG tự thành PHÂN VÂN. |
| 2 | Chặng 1 = chỗ giá đi "để làm gì" trước (test râu chưa test, test EMA kế tiếp, Fibo 0.5, quét đỉnh/đáy sát giá nơi đám đông chờ); chặng 2 = hướng chính [ST3 E1–E4]. Đích chặng 1 ngược hướng chính = **chỗ VÀO** ở mục 4 [ST3 C4]. Hạn: chặng H4 trong ngày → ~1 ngày ("View H4 dùng trong ngày", A6); đích D1 vài ngày (đo: trung vị 2,5 ngày); đích W1 ~2 tuần (đo: trung vị 15 ngày) (A6 "hạn dùng của view"; [ST1 A4]: view D1 bền trung vị 3 ngày, W1 6 ngày; đo: đích D1 chạm trung vị 2,5 ngày, W1 15,4 ngày). |
| 3 | **Mỗi khung một dòng đích theo hướng của CHÍNH khung đó** (hướng ở mục 1) — 3 view của 3 khung, không phải nước đôi. Đích = nấc kế tiếp (không nhảy nấc, L21), có ≥ 2 căn cứ (tốt nhất ≥ 3) trong cùng vùng hẹp (L20): Fibo mở rộng 1 / 1.618, EMA kế tiếp chưa test (34 → 89 → 200 → 610, theo giá trị EMA hiện tại), đỉnh/đáy/râu cũ, S/R đổi vai, Fibo thoái lui khung lớn [ST3 A2–A6]. H4 "hồi kỹ thuật"/"điều chỉnh" → đích H4 = kháng cự/hỗ trợ khung lớn chưa test = chỗ VÀO trung hạn ở mục 4 (L06, [ST3 C1–C2]); chỉ ghi nấc 1 (lệnh ngược khung lớn TP ngắn, không gồng — L33). **Mốc sai mỗi khung** (NHAP_VAI §5): giá RÂU của đỉnh (view GIẢM) / đáy (view TĂNG) cấu trúc gần nhất của khung đó, điều kiện "nến <khung> ĐÓNG qua", né số tròn (L25, L27, [03-04]); view vừa đổi vì một mức công tắc bị đóng qua → mốc sai = lấy lại mức công tắc đó ([ST1 B3], [ST1 D4]); W1 khi giá đã ở bên kia đỉnh/đáy tuần mà nến tuần chưa đóng → cản/hỗ trợ tuần gần nhất phía bất lợi ([ST1 A5], L03). |
| 4 | ≥ 3 căn cứ hội tụ → vùng vào; 2 → vùng quan sát; trung hạn ưu tiên vùng **thuận view W1, rồi D1** [ST3 C1–C3]; D1 ngược W1 thì vùng thuận D1 chỉ ghi "lướt" (L05). Lệnh ngược khung lớn (hồi kỹ thuật / điều chỉnh, "cản tàu") chỉ ghi "lướt, vốn nhỏ, chốt sớm" — không phải chỗ vào trung hạn (L33, [ST3 D5]). Vùng là điều kiện cần, nến khung nhỏ là điều kiện đủ [ST2 C1]. |
| 5 | Ít nhất 1 dòng. Lấy từ chỗ tránh của họ (NHAP_VAI §6.2, §7; [ST3 D1–D7]) — mỗi dòng nêu luật nào. |
| 6 | Luôn trả lời CẢ hai phía khi user không nói lệnh (không phải nước đôi — mỗi phía 1 quyết định). Theo [ST1 D1–D7]: chốt ngay / chốt từng nấc ở đích hoặc cản đã định; đóng khi nến đóng qua mốc làm lý do vào lệnh hoặc view đổi; lệnh ngắn đóng trước tin / đêm Chủ nhật; giữ khi view còn nguyên và chỉ có râu chạm mốc. |
| 7 | Lấy râu từ bảng nến + "Râu dài chưa bị test hết" trong hồ sơ [ST3 E3], [ST2 C2]. CÓ khi: râu dài D1/tuần chưa test [ST3 E3]; râu trùng ≥ 1 căn cứ khác (hội tụ, [ST3 A6]); phía râu "trống thanh khoản" (ít thân nến) — họ dời entry sâu tới râu (L28); râu rút chân mà lực bên kia vẫn áp đảo [ST2 C2]. KHÔNG khi: râu đã test (hồ sơ ghi "đã lấp" cao); thân nến đã phá vùng thì râu chỉ là test — thân quan trọng hơn râu ([ST2 C2], A1); râu lưng chừng — không tính là căn cứ (A4.9). Râu ngược chặng 2 vẫn có thể là đích chặng 1 (L45). |
| 8 | Lấy đường **CHÍNH** H4 và D1 trong mục Trendline của hồ sơ [ST2 B1–B7]. PHÁ THẬT = nến đóng qua (râu không tính); 1 cây = điều kiện cần, cây thứ 2 cùng phía hoặc test lại rồi đi tiếp = đủ. Qua đường mà ngay đó còn cản khác → chưa tính là break. PHÁ GIẢ = chưa đóng đã vượt / để râu rồi quay về / cây sau đóng ngược lại / đang trong hộp đi ngang / lực bên kia bẻ lại. Volume nến phá: ghi ra, nhưng KHÔNG dùng làm điều kiện thật/giả của trendline (người đó hầu như không dùng — [ST2 B3]). |
| 9 | Tin chỉ quyết định GIỜ, không quyết định hướng ("tin chỉ là cái cớ") [ST1 C1–C6]. Polymarket = thước đo thay cho FedWatch người đó xem. Ghi rõ dữ liệu chỉ có lịch, không có số CPI/NFP thực tế. |
| 10 | 3–5 câu. Dùng mẫu câu thật ở `bot_v5/_so_tay_T/<YYYYMMDD_HHMM của T>/giong_noi.md` (bản đã lọc theo T); không chép nguyên câu có số giá của ngày khác. |
| Dòng cuối | Bắt buộc. Giờ = giờ ĐÓNG của nến cuối trong hồ sơ ("Nến cuối dùng … → đóng …"). |

### Ví dụ ĐỊNH DẠNG (số giả, mã giả — chỉ để thấy cách viết, không phải case thật)

```
### 4. Chỗ VÀO
- SHORT 1.204–1.212 — hội tụ: [EMA89 H4 1.208] + [Fibo 0.618 nhịp 1.240→1.150 H4 = 1.206] + [đáy H4 cũ đổi vai 1.211]
  → vào khi: H1 tạo 2 đỉnh không vượt 1.215, nến đỏ đóng có volume vượt

### 5. Chỗ TRÁNH
- KHÔNG VÀO GIỮA 1.165–1.200 — giá đang lưng chừng giữa vùng long và vùng short, "đang nằm ở giữa… tốt nhất là không nên đụng"
- Không short đuổi quanh 1.150–1.160 — đây là hỗ trợ (đáy D1 + râu dưới H4), "không short ở hỗ trợ"
```

---

## B. FILE ĐỐI CHIẾU — `bot_v5/doi_chieu/<YYYY-MM-DD>_<MÃ>.md`

- `<YYYY-MM-DD>` = **ngày của T** (giờ VN), `<MÃ>` viết hoa (BTC, ETH, VANG…). Trùng tên → thêm `_2`, `_3`…
- Tạo thư mục nếu chưa có. Không sửa file đối chiếu cũ (phần user đã ghi kết quả).

```
# <MÃ> <KHUNG> — nhận định tại <T> VN

| Trường | Giá trị |
|---|---|
| gio_live (giờ user yêu cầu) | <giờ hiện tại VN> |
| gio_cat (nến cuối đã đóng dùng làm dữ liệu) | <YYYY-MM-DD HH:MM> VN |
| gio_phat_hanh (giờ bot trả lời) | <giờ hiện tại VN> |
| Lệnh hồ sơ | `python3 bot_v5/ngu_canh.py <MÃ> <KHUNG> "<T>"` |
| Giá đóng cuối (hồ sơ) | <giá> |
| Ảnh | <đường dẫn ảnh nếu có / "dán trong chat" / "không có — user ghi thẳng `<MÃ> <KHUNG> "<T>"`"> · nét vẽ user: <…> |
| Cảnh báo | <T trước 01/07/2026: có / không> |

## Nhận định của bot
<dán NGUYÊN VĂN câu trả lời theo khuôn A>

## Tóm tắt để chấm
| Khung | Hướng | Đích của khung này (theo hướng của chính nó) | Hạn | View sai khi (nến đóng) |
|---|---|---|---|---|
| H4 | <TĂNG / GIẢM / TĂNG (hồi kỹ thuật) / GIẢM (điều chỉnh) / PHÂN VÂN> | <= "Đích H4 (chặng gần)" mục 3> | <…> | nến H4 ĐÓNG <trên/dưới> <số> |
| D1 | <…> | <= "Đích D1" mục 3> | <…> | nến D1 ĐÓNG <trên/dưới> <số> |
| W1 | <…> | <= "Đích W1" mục 3> | <…> | nến W1 ĐÓNG <trên/dưới> <số> |
Chỗ VÀO: <…> · Chỗ TRÁNH: <…>
(Mỗi hàng chấm riêng theo hướng + đích + mốc sai của chính khung đó; PHÂN VÂN ghi "chờ nến … ĐÓNG trên X / dưới Y" ở cột đích.)

## Kết quả thật (USER ghi sau — bot không điền, không đọc phần này khi nhận định)
- Ngày ghi:
- Diễn biến sau T (cao nhất / thấp nhất trong hạn, kèm ngày):
- Chấm H4: ĐÚNG / SAI / CHƯA RÕ — (ĐÚNG = chạm đích, râu cũng tính, trong hạn TRƯỚC khi nến đóng qua mốc sai; SAI = nến đóng qua mốc sai trước; CHƯA RÕ = hết hạn chưa chạm cả hai)
- Chấm D1: ĐÚNG / SAI / CHƯA RÕ —
- Chấm W1: ĐÚNG / SAI / CHƯA RÕ —
- Đường đi: đúng thứ tự chặng 1 → chặng 2? —
- Chỗ VÀO có phản ứng không: —
- Chỗ TRÁNH có đúng là nên tránh không: —
- Râu: test lại đúng như bot nói? —
- Trendline: phá thật/giả đúng? —
- Bot sai ở đâu (hướng / đích / hạn / vùng / râu / trendline) + ghi chú:
```
