import json
import sys
from pathlib import Path
P = Path(__file__).resolve().parent
rows = json.loads((P/'tom_tat.json').read_text(encoding='utf-8'))
for r in rows:
    if len(sys.argv)>1 and r['ma'] not in sys.argv[1:]:
        continue
    print('\n===',r['ma'],'now',r['last_now'],'===')
    for k in ('4H','1D','1W'):
        a=r[k]
        if 'thieu' in a:
            print(k,a)
            continue
        def rr(v): return round(v,7) if isinstance(v,(int,float)) else v
        print(k,'c',a['c'],'EMA34',[rr(v) for v in a['ema34']], '89',rr(a['ema89']),'200',rr(a['ema200']),
              'RSI',a['rsi'],'ATR',a['atr'],'lastpivotHIGH',[(z['nhan'],z['rau']) for z in a['dinh']],
              'LOW',[(z['nhan'],z['rau']) for z in a['day']])
    fb=r['fibo_H4']
    for name in ('nhip_dang_chay','nhip_gan_nhat'):
        v=fb.get(name)
        if v:
            print(name, v['chieu'],v['tu']['gia'],'->',v['den']['gia'],
                  [(z['ty_le'],round(z['gia'],7)) for z in v['muc'] if z['ty_le'] in (.5,.618)])
    print('TREND',[(z['khung'],z['loai'],round(z['gia_tai_T'],7),z['trang_thai']) for z in r['trend_chinh']])
