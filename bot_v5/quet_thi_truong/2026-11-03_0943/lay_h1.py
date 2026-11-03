import datetime as dt
import json
import sys
from pathlib import Path
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[2]/'bot_v5'))
import ngu_canh as NC
import nen as NG
NG.NGHI=.6
NG.CUA_SO['1H']=600*3600
t=NC.doc_t('2026-11-03 09:00')
selection=json.loads((P/'selection.json').read_text(encoding='utf-8'))['selected']
for r in selection:
    ma=r['symbol'].upper()
    p=P/(ma+'_H1.json')
    if p.exists(): continue
    try:
        source,nen=NG.lay_chuoi(ma,'1H',t,P/'cache_perp',False)
        hs=NC.phan_tich(nen,'1H',30)
        hs.update(ma=ma,nguon=source,gio_cat='2026-11-03 09:00',so_nen=len(nen))
        assert nen[-1].dong<=t
        p.write_text(json.dumps(hs,ensure_ascii=False,indent=1),encoding='utf-8')
        print('H1',ma,len(nen),nen[-1].nhan,flush=True)
    except Exception as e:
        print('H1 ERROR',ma,type(e).__name__,str(e),flush=True)
