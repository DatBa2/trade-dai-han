"""Snapshot vàng cho nhận định 03/11: sửa dữ liệu trong bản sao, không sửa nguồn."""
import csv
import json
import shutil
import sys
from pathlib import Path

P = Path(__file__).resolve().parent
GOC = P.parents[2]
sys.path.insert(0, str(GOC / 'bot_v5'))
import ngu_canh as NC
import nen as NG

cache = P / 'cache_vang_da_kiem'
cache.mkdir(exist_ok=True)
for p in NG.CACHE_MAC_DINH.iterdir():
    if p.suffix in ('.csv', '.json'):
        shutil.copy2(p, cache / p.name)

with (cache / 'yahoo_VANG_1d.csv').open(newline='') as f:
    rd = csv.DictReader(f)
    cot = rd.fieldnames
    ds = list(rd)
loai = [r for r in ds if r['mo_utc'] >= r['dong_utc']]
ds = [r for r in ds if r['mo_utc'] < r['dong_utc']]
with (cache / 'yahoo_VANG_1h.csv').open(newline='') as f:
    gio = [r for r in csv.DictReader(f)
           if '2026-11-01 23:00' <= r['mo_utc'] < '2026-11-02 22:00']
assert len(gio) == 23
assert [NG.tu_s_utc(r['mo_utc']) for r in gio] == list(range(
    NG.tu_s_utc('2026-11-01 23:00'), NG.tu_s_utc('2026-11-02 22:00'), 3600))
them = {'mo_utc': gio[0]['mo_utc'], 'dong_utc': gio[-1]['dong_utc'],
        'open': gio[0]['open'], 'high': str(max(float(r['high']) for r in gio)),
        'low': str(min(float(r['low']) for r in gio)), 'close': gio[-1]['close'],
        'vol': str(sum(float(r['vol']) for r in gio))}
ds.append(them)
ds.sort(key=lambda r: r['mo_utc'])
with (cache / 'yahoo_VANG_1d.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cot)
    w.writeheader()
    w.writerows(ds)
t = NC.doc_t('2026-11-03 07:00')
h = NC.tao_ho_so('VANG', '1D', t, 80, cache, True)
h['kiem_tra_du_lieu'] = {
    'dong_loi_da_loai': loai,
    'nen_D1_dung_lai_tu_23_nen_1H': them,
    'ghi_chu': 'OHLC phiên COMEX 18:00–17:00 New York; dựng từ 23 nến giờ đủ liên tiếp. Không phải settlement chính thức. Bản sao cache riêng, giữ nguồn gốc.',
}
for k in h['khung_ds']:
    for n in k.get('bang', []):
        assert n['mo_utc'] < n['dong_utc'] <= '2026-11-03 00:00'
(P / 'VANG_ngu_canh_da_kiem.json').write_text(json.dumps(h, ensure_ascii=False, indent=1), encoding='utf-8')
(P / 'VANG_ngu_canh_da_kiem.md').write_text(NC.ve_markdown(h), encoding='utf-8')
print(json.dumps(h['kiem_tra_du_lieu'], ensure_ascii=False, indent=1))
print(h['nen_cuoi'])
