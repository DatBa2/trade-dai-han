import csv
import json
from pathlib import Path

P = Path(__file__).resolve().parent
select = json.loads((P / 'selection.json').read_text(encoding='utf-8'))['selected']
tick = {r['instId']: r for r in json.loads((P / 'okx_ticker_swap.json').read_text(encoding='utf-8'))['data']['data']}
rows = []
for r in select:
    ma = r['symbol'].upper()
    p = P / (ma + '.json')
    if not p.exists():
        continue
    h = json.loads(p.read_text(encoding='utf-8'))
    ks = {k['khung']: k for k in h['khung_ds']}
    z = tick[ma + '-USDT-SWAP']
    o = {'ma': ma, 'rank_cap': r['market_cap_rank'], 'cap_B': round(r['market_cap']/1e9, 2),
         'last_now': float(z['last']), 'doi24h_pct': round((float(z['last'])/float(z['open24h'])-1)*100, 2),
         'OKX_vol24h_M_usdt_xap_xi': round(float(z['volCcy24h'])*float(z['last'])/1e6, 1),
         'spread_bps': round((float(z['askPx'])-float(z['bidPx']))/float(z['last'])*1e4, 2)}
    for k in ('4H', '1D', '1W'):
        d = ks[k]
        if 'chi_bao' not in d:
            o[k] = {'thieu': d.get('thieu')}
            continue
        c = d['chi_bao']
        e = c['ema']
        o[k] = {'c': c['gia_dong'], 'L01': c['phan_loai_L01'], 'rsi': round(c['rsi14'], 1) if c['rsi14'] is not None else None,
                'atr': round(c['atr14'], 7) if c['atr14'] else None,
                'ema34': [e['ema34'].get(x) for x in ('low','close','high')],
                'ema89': e['ema89'].get('gia'), 'ema200': e['ema200'].get('gia'),
                'SR_tren': [x['gia'] for x in d['bac_thang']['tren'][:3]],
                'SR_duoi': [x['gia'] for x in d['bac_thang']['duoi'][:3]],
                'dinh': d['fractal']['dinh'][-2:], 'day': d['fractal']['day'][-2:],
                'vol': round(c['vol_x_tb20_nen_cuoi'], 2) if c['vol_x_tb20_nen_cuoi'] else None,
                'rau': d['rau_dai'][:2],
                'last3': [{a:n[a] for a in ('nhan','o','h','l','c','vol_x_tb20')} for n in d['bang'][-3:]]}
    for fb in h['fibo']:
        if fb['khung']=='4H':
            o['fibo_H4'] = fb
    o['trend_chinh'] = [dict(khung=g['khung'],loai=g['loai'],**line)
                       for g in h['trendline'].get('nhom',[]) for line in g['duong'] if line['chinh']]
    rows.append(o)
(P / 'tom_tat.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
for o in rows:
    h4, d1 = o['4H'], o['1D']
    print(o['ma'], 'last',o['last_now'],'24h',o['doi24h_pct'],'liqM',o['OKX_vol24h_M_usdt_xap_xi'],
          '| H4',h4.get('L01'), 'RSI',h4.get('rsi'), '| D1',d1.get('L01'),'RSI',d1.get('rsi'),
          '| support',h4.get('SR_duoi'),'res',h4.get('SR_tren'))
print('TOTAL',len(rows))
