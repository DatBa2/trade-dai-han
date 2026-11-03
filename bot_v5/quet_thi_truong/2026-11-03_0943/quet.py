"""Lưu dữ liệu cho lượt rà soát hiện tại, không sửa bot hoặc đặt lệnh."""
import concurrent.futures
import datetime as dt
import json
import shutil
import sys
import time
from pathlib import Path

P = Path(__file__).resolve().parent
GOC = P.parents[2]
sys.path.insert(0, str(GOC / 'bot_v5'))
import ngu_canh as NC
import nen as NG

T_VN = '2026-11-03 09:00'
T = NC.doc_t(T_VN)
cap = json.loads((P / 'von_hoa.json').read_text(encoding='utf-8'))['data']
sw = {x['instId']: x for x in json.loads((P / 'okx_swap.json').read_text(encoding='utf-8'))['data']['data']
      if x['state'] == 'live'}
excl = {'USDT', 'USDC', 'USDS', 'FIGR_HELOC', 'DAI', 'USDE', 'USD1', 'USDG', 'PYUSD', 'RLUSD',
        'USDY', 'USYC', 'BUIDL', 'EURSAFO', 'USDF', 'U', 'XAUT', 'PAXG'}
chon, bo = [], []
for r in cap:
    ma = r['symbol'].upper()
    if ma in excl:
        bo.append(dict(r, ly_do='stablecoin / tài sản quỹ / vàng token, ngoài phạm vi crypto biến động'))
    elif ma + '-USDT-SWAP' not in sw:
        bo.append(dict(r, ly_do='không có hợp đồng USDT perpetual live tương ứng trên OKX'))
    else:
        chon.append(r)
    if len(chon) == 20:
        break
(P / 'selection.json').write_text(json.dumps({'gio_chon_vn': dt.datetime.now().isoformat(timespec='seconds'),
    'gio_cat': T_VN, 'selected': chon, 'excluded': bo}, ensure_ascii=False, indent=1), encoding='utf-8')
cache = P / 'cache_perp'
cache.mkdir(exist_ok=True)
for f in NG.CACHE_MAC_DINH.iterdir():
    if f.suffix in ('.csv', '.json') and not (cache / f.name).exists():
        shutil.copy2(f, cache / f.name)
(cache / 'inst.json').write_text(json.dumps({r['symbol'].upper(): r['symbol'].upper() + '-USDT-SWAP'
    for r in chon}), encoding='utf-8')
NG.NGHI = .32  # hai luồng tải nến, giữ tốc độ gọi thấp hơn giới hạn công khai.
print('SELECTED', ', '.join(r['symbol'].upper() for r in chon), flush=True)


def xu_ly(r):
    ma = r['symbol'].upper()
    file = P / (ma + '.json')
    if file.exists():
        return json.loads(file.read_text(encoding='utf-8'))
    start = time.monotonic()
    try:
        hs = NC.tao_ho_so(ma, '4H', T, 30, cache, False)
        assert hs['nen_cuoi']['dong_vn'] == '2026-11-03 07:00'
        assert hs['nguon'] == 'OKX perp (SWAP) ' + ma + '-USDT-SWAP'
        hs['von_hoa_snapshot'] = r
        file.write_text(json.dumps(hs, ensure_ascii=False, indent=1), encoding='utf-8')
        (P / (ma + '.md')).write_text(NC.ve_markdown(hs), encoding='utf-8')
        print('DONE', ma, round(time.monotonic() - start, 1), 's', flush=True)
        return hs
    except Exception as e:
        err = {'ma': ma, 'loi': type(e).__name__ + ': ' + str(e)}
        (P / (ma + '_loi.json')).write_text(json.dumps(err, ensure_ascii=False, indent=1), encoding='utf-8')
        print('ERROR', ma, err['loi'], flush=True)
        return err


if __name__ == '__main__':
    # Điền BTC và nguồn phụ dùng chung trước; các coin còn lại chỉ ghi cache của chính nó.
    results = [xu_ly(chon[0])]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for r in pool.map(xu_ly, chon[1:]):
            results.append(r)
    (P / 'ket_qua_tai.json').write_text(json.dumps(
        [{'ma': r['ma'], 'loi': r.get('loi')} for r in results], ensure_ascii=False, indent=1), encoding='utf-8')
    print('FINISHED', len(results), flush=True)
