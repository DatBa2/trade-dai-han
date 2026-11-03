"""Dựng báo cáo từ snapshot + quyết định phân tích ghi riêng trong ke_hoach.json."""
import datetime as dt
import json
import re
from pathlib import Path

P=Path(__file__).resolve().parent
OUT=P.parents[1]/'doi_chieu/2026-11-03_XEP_HANG_20_COIN.md'
plans=json.loads((P/'ke_hoach.json').read_text(encoding='utf-8'))
rows={r['ma']:r for r in json.loads((P/'tom_tat.json').read_text(encoding='utf-8'))}
selection=json.loads((P/'selection.json').read_text(encoding='utf-8'))
market=json.loads((P/'gia_funding_moi.json').read_text(encoding='utf-8'))
tickdata=json.loads((P/'ticker_chot.json').read_text(encoding='utf-8')) if (P/'ticker_chot.json').exists() else {'lay_luc_vn':market['lay_luc_vn'],'data':market['ticker']}
ticks={r['instId']:r for r in tickdata['data']['data']}
fund={j['data'][0]['instId']:j['data'][0] for j in market['funding'] if j.get('data')}
prefix='../quet_thi_truong/2026-11-03_0943/'

def f(x):
    if x is None:return 'thiếu'
    a=abs(x)
    dec=1 if a>=10000 else 2 if a>=100 else 3 if a>=10 else 4 if a>=1 else 5
    return format(x,',.'+str(dec)+'f').replace(',','X').replace('.',',').replace('X','.')
def zone(z):return '–'.join(f(v) for v in z)
def label(a):
    s=a.get('L01','thiếu')
    return 'GIẢM' if s.startswith('GIẢM') else 'TĂNG' if s.startswith('TĂNG') else 'thiếu EMA' if 'chưa đủ' in s else 'hỗn hợp'
now=dt.datetime.now().strftime('%Y-%m-%d %H:%M')
L=['# Rà soát 20 coin vốn hóa lớn trên OKX — 03/11/2026','',
   '> **Ưu tiên setup chờ SHORT: DOGE → ETH → SUI → ADA → BTC. Chưa đề xuất vào market ngay.**',
   '> Đây là xếp hạng ưu tiên theo dõi/vào khi đủ xác nhận, không phải bảng xác suất thắng hoặc thứ tự lợi nhuận chắc chắn.','',
   '## 1. Phạm vi và thời điểm','',
   '| Trường | Giá trị |','|---|---|',
   '| gio_live | Khoảng 2026-11-03 09:42 VN, lúc nhận yêu cầu |',
   '| gio_cat của hồ sơ nến | 2026-11-03 09:00 VN; H1 cuối 09:00, H4 và D1 cuối 07:00 |',
   '| gio_phat_hanh | '+now+' VN |',
   '| Snapshot vốn hóa | CoinGecko, cập nhật nguồn 09:41:53 VN, tải khoảng 09:43 |',
   '| Giá tham chiếu gần phát hành | '+tickdata['lay_luc_vn']+' VN, OKX perpetual |',
   '| Funding tham chiếu | '+market['lay_luc_vn']+' VN |',
   '| Sản phẩm phân tích | Hợp đồng USDT perpetual OKX, không dùng giá spot thay cho giá hợp đồng |','',
   'Phạm vi là **20 coin lớn nhất có hợp đồng USDT perpetual đang live trên OKX**, sau khi bỏ stablecoin, tài sản quỹ và vàng token. Vì vậy đây không phải đúng 20 dòng đầu của bảng vốn hóa toàn cầu; danh sách đi tới hạng vốn hóa #31. XMR, WBT, RAIN không có hợp đồng tương ứng, LEO chỉ có spot nên không được xếp hạng kèo long/short ở đây. Không âm thầm thay chúng bằng một đồng nhỏ rồi gọi là top 20 toàn thị trường.','',
   'Nguồn chọn danh sách: [CoinGecko](https://www.coingecko.com/). Danh sách gốc và loại trừ được lưu trong [selection.json]('+prefix+'selection.json), có cả hạng vốn hóa và lý do loại. Vốn hóa là USD tổng hợp toàn cầu, giá lệnh là USDT trên OKX; hai trường này không đồng nhất.','',
   'Các quote/vốn hóa lấy sau cutoff nến được ghi riêng, chỉ dùng để xem giá hiện tại còn gần vùng không và khả năng giao dịch. Không dùng chúng để giả vờ một nến H4 sau 07:00 đã đóng. Đây là phân tích hiện tại với nhiều lớp thời gian được công khai, không phải bài backtest tại 09:00.','',
   '## 2. Dùng công cụ nào và dựa vào đâu để xếp hạng?','',
   '1. CoinGecko API `coins/markets`, sắp vốn hóa giảm dần: xác định danh sách hiện tại, không dùng danh sách ghi nhớ từ tháng trước.',
   '2. OKX API công khai `public/instruments`: xác nhận đúng mã và trạng thái live. Mỗi mã trong cache riêng được ánh xạ rõ sang `MA-USDT-SWAP`.',
   '3. `bot_v5/ngu_canh.py` + `nen.py`: lấy nến đóng H4/D1/W1, EMA34/89/200/610 khi đủ lịch sử, RSI, ATR, pivot 3–3, râu, Fibo và trendline. Snapshot JSON/Markdown từng coin được lưu riêng.',
   '4. H1 dùng 600 nến tới 09:00, tính bằng cùng hàm `phan_tich()`, để kiểm thời điểm vào. Không đủ EMA610 H1 và không cố điền.',
   '5. Ticker OKX hiện tại: kiểm khoảng cách tới vùng, spread tức thời và volume 24h. Volume USDT là ước tính `volCcy24h × last`, không phải độ sâu sổ lệnh hoặc bảo đảm trượt giá.',
   '6. Funding hiện tại được ghi làm chi phí tham chiếu, không dùng để chọn hướng giá. Dương: long trả short; âm: short trả long ở kỳ tính nếu mức đó được áp dụng. Mức snapshot có thể đổi trước kỳ tính.',
   '7. Xếp hạng do bot cân nhắc: cấu trúc nhiều khung → vùng hội tụ rõ và mốc sai → khoảng trống tới các nấc chốt → độ gần vùng hiện tại và khả năng giao dịch → yếu tố làm phải chờ. Không có mô hình đã kiểm định dự báo xác suất thắng của bảng này.','',
   'Sổ tay phương pháp được lọc đúng ngày trước khi đọc (`_so_tay_T/20261103_0900`). Không đọc kết quả thật trong các file nhận định cũ để chọn coin. Những nhận xét bên dưới là suy luận từ hồ sơ hiện tại.','',
   '## 3. Mặt bằng thị trường và hành động chung','',
   '- **15/20** coin có phân loại H4 giảm theo thứ tự giá dưới EMA34/89/200.',
   '- DOGE, ADA và XLM đồng thuận giảm theo bộ EMA trên H4/D1/W1; CC có H4/D1 giảm nhưng thiếu EMA dài tuần.',
   '- HYPE/UNI/NEAR còn các dấu hiệu mạnh hơn trên khung lớn, nên không gom chúng chung một nhóm short trung hạn chỉ vì vừa có nến đỏ.',
   '- HYPE và TRX là hai trường hợp đáng theo dõi khả năng phục hồi; **chưa có long được xác nhận** trong bản này.',
   '- SOL, ZEC, NEAR và XLM có các dấu hiệu quá bán/xa vùng vào ở khung liên quan. Giảm mạnh không đồng nghĩa đang là chỗ bán tốt.',
   '- Nhóm đầu hiện đều dưới vùng short chờ: **đứng ngoài chờ hồi và xác nhận**, không biến thứ hạng #1 thành lệnh market.',
   '- Bảng nhãn EMA là output kỹ thuật. “Hỗn hợp” có thể do thứ tự các EMA chưa đồng thuận dù giá dưới cả ba; không tự suy ra PHÂN VÂN hoặc TĂNG.','',
   '## 4. Xếp hạng đủ 20 coin','',
   '| Ưu tiên | Coin | Hạng vốn hóa | Giá OKX hiện tại | H4 / D1 / W1 theo EMA | Hành động | Vùng theo dõi |',
   '|---:|---|---:|---:|---|---|---|']
for p in plans:
    ma=p['ma'];r=rows[ma];z=ticks[ma+'-USDT-SWAP']
    L.append('| '+str(p['rank'])+' | **'+ma+'** | #'+str(r['rank_cap'])+' | '+f(float(z['last']))+' | '+
             ' / '.join(label(r[k]) for k in ('4H','1D','1W'))+' | '+p['hanh_dong']+' | '+(zone(p['vung']) if p.get('vung') else 'chờ cấu trúc')+' |')
L+=['','GRAM là tên mới của Toncoin trong nguồn hiện tại; đã đối chiếu [thông báo OKX](https://www.okx.com/en-us/help/okx-to-support-ton-crypto-migration). Không ghép tùy tiện lịch sử mã TON cũ để làm đủ EMA cho GRAM.','',
    '## 5. Năm setup ưu tiên: vùng vào, đích và mốc sai','',
    '**Điều kiện chung:** giá phải tới vùng; H1 xuất hiện từ chối tăng rõ, tạo hai đỉnh không vượt tiếp rồi nến giảm đóng có lực. Chạm vùng là điều kiện cần, chưa phải lệnh. Snapshot H1 tới 09:00 chưa có xác nhận tại các vùng chờ của top 5.','',
    '| Hạng | Coin | Chờ SHORT | Chốt nấc 1 | Chốt nấc 2 | Hủy setup khi H4 ĐÓNG trên |',
    '|---:|---|---:|---:|---:|---:|']
for p in plans[:5]:
    L.append('| '+str(p['rank'])+' | '+p['ma']+' | '+zone(p['vung'])+' | '+zone(p['tp1'])+' | '+zone(p['tp2'])+' | '+f(p['sai'])+' |')
L+=['','Hạn dự kiến: nấc 1 khoảng 1–3 ngày, tới 06/11; nấc 2 vài ngày tới khoảng một tuần, tới 10/11. Không chạm trong hạn phải đánh giá lại; không tự kéo dài hạn để né sai. Các mốc sai trong bảng áp dụng cho **setup chờ vào theo H4**, không trộn với một view D1 dài hơn để giữ lệnh đã sai.','',
    '### Chi tiết từng setup','']
for p in plans[:5]:
    ma=p['ma'];r=rows[ma];fr=fund[ma+'-USDT-SWAP'];mid=sum(p['vung'])/2;tp=sum(p['tp2'])/2
    rr=(mid-tp)/(p['sai']-mid)
    L+=['#### #'+str(p['rank'])+' — '+ma,'',
        '**Vì sao xếp ở đây:** '+p['ly_do'],'',
        '**Vùng chờ '+zone(p['vung'])+' có các căn cứ:**','']
    L+=['- '+s+'.' for s in p['can_cu']]
    L+=['','**Đích:** '+p['dich_can_cu']+'.','',
        '**Mốc sai:** nến H4 **ĐÓNG trên '+f(p['sai'])+'**. Mốc là cực trị cấu trúc trong hồ sơ, không phải một stop theo giá được bảo đảm khớp.','',
        '**Điểm trừ:** '+p['tru'],'',
        'Funding tham chiếu: '+f(float(fr['fundingRate'])*100)+'% mỗi kỳ theo snapshot. Volume OKX 24h ước tính khoảng '+f(r['OKX_vol24h_M_usdt_xap_xi'])+' triệu USDT.','',
        'Từ giữa vùng vào tới giữa đích nấc 2, khoảng cách lợi nhuận chia khoảng cách tới mốc sai khoảng **'+f(rr)+' lần**. Đây chỉ là phép so khoảng cách giá, **không phải tỷ lệ lãi/lỗ thực hiện**: chờ nến đóng, phí, funding, trượt giá và nấc hỗ trợ gần có thể làm kết quả khác.','',
        '[Hồ sơ '+ma+']('+prefix+ma+'.md) · [JSON]('+prefix+ma+'.json) · [H1]('+prefix+ma+'_H1.json)'+
        (' · [Ảnh chụp D1 OKX]('+prefix+ma+'_D1_OKX.png)' if (P/(ma+'_D1_OKX.png')).exists() else ''), '']
L+=['## 6. Vì sao những coin còn lại chưa lên nhóm đầu?','']
for p in plans[5:]:
    ma=p['ma']
    L+=['### #'+str(p['rank'])+' — '+ma+' — '+p['hanh_dong'],'',
        '**Điểm đáng chú ý:** '+p['ly_do'],'',
        '**Lý do chờ/giảm ưu tiên:** '+p['tru'],'',
        ('Vùng theo dõi: **'+zone(p['vung'])+'**, chưa phải entry được xác nhận.' if p.get('vung') else 'Chưa chốt vùng entry đủ rõ trong bản này.'),'',
        '[Hồ sơ '+ma+']('+prefix+ma+'.md) · [JSON]('+prefix+ma+'.json) · [H1]('+prefix+ma+'_H1.json)','']
L+=['## 7. Tin, giới hạn và cách dùng bảng','',
    'Lịch trong hồ sơ ghi JOLTS 03/11 22:00, NFP 06/11 20:30 VN; dataset chỉ có lịch, không có kết quả thực tế. Kiểm lại trước khi giữ lệnh qua tin. Polymarket trong repo còn snapshot cũ từ 31/10 nên không dùng để tăng độ chắc của xếp hạng này.','',
    'Phương pháp học chủ yếu từ BTC, chưa được kiểm định riêng cho cả 20 coin. Thứ hạng là nhận định tại một thời điểm, không phải bằng chứng chiến lược có lãi. Không đặt xác suất thắng 70–90% khi chưa đo được.','',
    'Dữ liệu mỗi coin có độ dài khác nhau; thiếu EMA thì để thiếu. Pivot chỉ được dùng khi có đủ ba nến bên phải đã đóng. Đáy/đỉnh của nhịp đang chạy được ghi chưa xác nhận, không đánh tráo thành pivot chắc chắn.','',
    'Bản này không tự vào lệnh. Khi giá tới vùng, cập nhật snapshot và đọc lại H1/H4; vùng tốt ở thời điểm hiện tại có thể mất giá trị trước khi khớp. Cần phân biệt coin đáng theo dõi với coin đã đủ điều kiện giao dịch.','',
    '## 8. Bằng chứng hình ảnh và dữ liệu','',
    '[Bảng chart H4 tổng hợp 20 coin]('+prefix+'tong_hop_H4.png) là hình dựng từ OHLC thật, chỉ tới nến đóng 07:00; các mức đánh dấu top 5 là chú thích của bot.','',
    'Ảnh chụp web thật: [DOGE D1]('+prefix+'DOGE_D1_OKX.png) · [ETH D1]('+prefix+'ETH_D1_OKX.png) · [SUI D1]('+prefix+'SUI_D1_OKX.png). Ảnh chụp sau cutoff có cây cuối đang chạy; không lấy cây này làm xác nhận. MA(5/10/20) mặc định trên ảnh khác các EMA tính trong hồ sơ.','',
    'Nguồn thô: [vốn hóa]('+prefix+'von_hoa.json), [hợp đồng OKX]('+prefix+'okx_swap.json), [quote/funding]('+prefix+'gia_funding_moi.json), [kế hoạch và thứ hạng]('+prefix+'ke_hoach.json).','',
    '## 9. Kết quả thật — để trống cho lần đối chiếu sau','',
    '- Ngày ghi:', '- Coin nào thực sự tới vùng và có H1 xác nhận:', '- Entry thực tế nếu có:',
    '- Nấc 1/nấc 2 có chạm trước khi H4 đóng qua mốc sai không:', '- Sai ở lựa chọn coin, hướng, vùng, đích hay hạn:',
    '- Thứ hạng có giúp chọn được setup tốt hơn các coin bị bỏ qua không:', '',
    'Không chấm bảng theo việc coin giảm bao nhiêu kể từ lúc quét nếu entry chưa khớp. Giá đi đúng hướng nhưng không tới vùng không tạo ra một giao dịch thắng.']
OUT.parent.mkdir(exist_ok=True)
OUT.write_text('\n'.join(L)+'\n',encoding='utf-8')
print('REPORT',OUT.resolve())
print('Ranks',len(plans),'top5 all waiting',all(float(ticks[p['ma']+'-USDT-SWAP']['last'])<p['vung'][0] for p in plans[:5]))
