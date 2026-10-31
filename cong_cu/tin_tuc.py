#!/usr/bin/env python3
"""Ngu canh tin tuc vi mo + Polymarket (Fed) theo thoi diem t, NHAN QUA.

Doc du_lieu/tin_tuc/{lich_kinh_te_2026,fomc_ket_qua_2026,polymarket_fed}.csv.

ngu_canh_tai(t_utc) -> dict:
  sap_toi_7_ngay : su kien co gio cong bo trong (t, t+7 ngay]. Lich cong bo biet truoc nen hop le.
  vua_qua_3_ngay : su kien da cong bo trong (t-3 ngay, t]. FOMC kem 'ket_qua' CHI khi gio quyet dinh <= t.
                   Khong co so lieu thuc te (CPI/NFP... bao nhieu) - dataset khong chua.
  polymarket     : xac suat MOI NHAT co ts <= t cho ky FOMC ke tiep (quyet dinh > t), hoac None.
                   'xac_suat' la gia token Yes cua tung ket qua (tong khong dung 1 tuyet doi).
Chay truc tiep file nay de chay kiem thu nhan qua.
"""
import csv
import bisect
import datetime as dt
import os
from zoneinfo import ZoneInfo

THU_MUC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'du_lieu', 'tin_tuc')
ET = ZoneInfo('America/New_York')
UTC = dt.timezone.utc
_cache = {}


def _utc(t):
    """Nhan datetime (naive = UTC), chuoi ISO, hoac epoch giay -> datetime aware UTC."""
    if isinstance(t, (int, float)):
        return dt.datetime.fromtimestamp(t, UTC)
    if isinstance(t, str):
        t = dt.datetime.fromisoformat(t.replace('Z', '+00:00'))
    return t.replace(tzinfo=UTC) if t.tzinfo is None else t.astimezone(UTC)


def _doc(ten):
    with open(os.path.join(THU_MUC, ten), encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def _nap():
    if _cache:
        return _cache
    ev = []
    for r in _doc('lich_kinh_te_2026.csv'):
        ts = dt.datetime.strptime(r['ngay_gio_et'], '%Y-%m-%d %H:%M').replace(tzinfo=ET).astimezone(UTC)
        ev.append({'su_kien': r['su_kien'], 'ky': r['ky'], 'ts_utc': ts, 'ghi_chu': r['ghi_chu']})
    ev.sort(key=lambda e: e['ts_utc'])
    _cache['ev'] = ev
    _cache['ts'] = [e['ts_utc'] for e in ev]
    kq = {}
    for r in _doc('fomc_ket_qua_2026.csv'):
        kq[r['ky_hop']] = {'quyet_dinh': r['quyet_dinh'], 'thay_doi_bps': int(r['thay_doi_bps']),
                           'dai_lai_suat_sau_hop_pct': r['dai_lai_suat_sau_hop_pct'], 'phieu': r['phieu'],
                           'phan_doi': r['phan_doi']}
    _cache['kq'] = kq
    pm = {}  # ky_hop -> ket_qua -> ([ts], [p])
    for r in _doc('polymarket_fed.csv'):
        if r['ky_hop'].endswith('_phu'):
            continue
        ts = dt.datetime.strptime(r['ts_utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=UTC)
        a = pm.setdefault(r['ky_hop'], {}).setdefault(r['ket_qua'], ([], []))
        a[0].append(ts)
        a[1].append(float(r['xac_suat']))
    _cache['pm'] = pm
    return _cache


def _xuat(e):
    return {'su_kien': e['su_kien'], 'ky': e['ky'], 'ts_utc': e['ts_utc'].strftime('%Y-%m-%dT%H:%M:%SZ'),
            'ghi_chu': e['ghi_chu']}


def ngu_canh_tai(t_utc):
    t = _utc(t_utc)
    d = _nap()
    ev, tss = d['ev'], d['ts']
    # sap toi: (t, t+7d]
    i0 = bisect.bisect_right(tss, t)
    i1 = bisect.bisect_right(tss, t + dt.timedelta(days=7))
    sap = [_xuat(e) for e in ev[i0:i1]]
    # vua qua: (t-3d, t]  -> chi su kien da cong bo <= t
    j0 = bisect.bisect_right(tss, t - dt.timedelta(days=3))
    qua = []
    for e in ev[j0:i0]:
        x = _xuat(e)
        if e['su_kien'] == 'FOMC':
            kq = d['kq'].get(e['ky'])
            if kq:
                x['ket_qua'] = dict(kq)
        qua.append(x)
    # polymarket cho ky FOMC ke tiep (quyet dinh > t)
    pmk = None
    nxt = next((e for e in ev[i0:] if e['su_kien'] == 'FOMC'), None)
    if nxt:
        kh = '2026-%02d' % nxt['ts_utc'].astimezone(ET).month
        out, ts_max = {}, None
        for kqua, (ts, p) in d['pm'].get(kh, {}).items():
            k = bisect.bisect_right(ts, t) - 1
            if k >= 0:
                out[kqua] = {'xac_suat': p[k], 'ts_utc': ts[k].strftime('%Y-%m-%dT%H:%M:%SZ')}
                ts_max = ts[k] if ts_max is None or ts[k] > ts_max else ts_max
        pmk = {'ky_hop': nxt['ky'], 'ngay_quyet_dinh_utc': nxt['ts_utc'].strftime('%Y-%m-%dT%H:%M:%SZ'),
               'ket_qua': out, 'ts_moi_nhat_utc': ts_max.strftime('%Y-%m-%dT%H:%M:%SZ') if ts_max else None} if out else None
    return {'t_utc': t.strftime('%Y-%m-%dT%H:%M:%SZ'), 'sap_toi_7_ngay': sap, 'vua_qua_3_ngay': qua, 'polymarket': pmk}


def kiem_thu():
    d = _nap()
    fomc = [e for e in d['ev'] if e['su_kien'] == 'FOMC']
    ds = dt.timedelta(seconds=1)
    for e in fomc:
        tc = e['ts_utc']
        truoc = ngu_canh_tai(tc - ds)
        assert not any('ket_qua' in x for x in truoc['vua_qua_3_ngay']), e['ky']
        assert not any(x['su_kien'] == 'FOMC' and x['ky'] == e['ky'] for x in truoc['vua_qua_3_ngay']), e['ky']
        assert any(x['su_kien'] == 'FOMC' and x['ky'] == e['ky'] for x in truoc['sap_toi_7_ngay']), e['ky']
        pm = truoc['polymarket']
        if pm:
            assert pm['ky_hop'] == e['ky']
            assert all(v['ts_utc'] <= truoc['t_utc'] for v in pm['ket_qua'].values())
        sau = ngu_canh_tai(tc)
        if e['ky'] in d['kq']:
            fx = [x for x in sau['vua_qua_3_ngay'] if x['su_kien'] == 'FOMC' and x['ky'] == e['ky']]
            assert fx and 'ket_qua' in fx[0], e['ky']
            assert sau['polymarket'] is None or sau['polymarket']['ky_hop'] != e['ky']
    # t truoc moi du lieu -> khong loi
    assert ngu_canh_tai('2025-01-01T00:00:00Z')['polymarket'] is None
    print('kiem_thu OK:', len(fomc), 'ky FOMC, nhan qua dung')


if __name__ == '__main__':
    kiem_thu()
    import json
    print(json.dumps(ngu_canh_tai('2026-09-16T17:59:59Z'), ensure_ascii=False, indent=1)[:1800])
