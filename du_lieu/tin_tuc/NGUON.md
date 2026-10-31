# Nguon du lieu tin tuc / vi mo 2026

Tai ngay 2026-10-31 (~04:50-05:00 UTC). Phan sau 31/10 trong lich la lich du kien, chua co ket qua.

## Nguon
- FOMC: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm va cac statement `pressreleases/monetary2026MMDDa.htm` (7 ky da hop). Quyet dinh 14:00 ET, hop bao 14:30 ET.
- BLS (CPI, PPI, Employment Situation=NFP, JOLTS, ECI): bls.gov tra 403 cho curl (Access Denied), nen lay ban luu Wayback `web.archive.org/web/2026id_/https://www.bls.gov/schedule/2026/MM_sched.htm` (lich thang; ban chup Wayback, vi du thang 10 la 2026-10-19). Lich cac thang qua da phan anh ngay thuc te (vd NFP Th1 doi sang 11/02, tre do dong cua chinh phu). Rui ro: ban chup co the cu so voi ngay tai, ngay thang 10-12 co the doi sau ban chup. `nguon_url` ghi URL bls.gov goc.
- BEA (PCE = "Personal Income and Outlays", GDP cac dot uoc tinh): https://www.bea.gov/news/schedule/full (tai truc tiep). Gio 8:30 hoac 10:00 ET.
- Polymarket: gamma `https://gamma-api.polymarket.com/events?slug=<slug>`; gia `https://clob.polymarket.com/prices-history?market=<token_id>&startTs&endTs&fidelity=60`. `interval=max` chi tra thua (~12h/diem, thua dau market), `startTs/endTs` toi da 14 ngay/lan -> cat khuc 14 ngay, fidelity 60 (diem theo gio). Slug: january `fed-decision-in-january`; march `-march-885`; april `-april`; june `-june-825`; july `-july-181`; september `-september-762` (chinh) va `-september-568` (phu, khoi luong ~53k USD, chi 04/05-11/05); october `-october-20260617190323537`; december `-december-20260729232808632`. Khong co market thang 5 (khong co hop FOMC).

## File
| File | So dong (gom header) | Ghi chu |
|---|---|---|
| lich_kinh_te_2026.csv | 102 | 101 su kien: CPI 12, PPI 13 (thang 1 co 2 ky do lich dong cua), NFP 12, JOLTS 12, PCE 13, GDP 13, FOMC 8, khac 18 (hop bao FOMC 8, bien ban FOMC 6, ECI 4) |
| fomc_ket_qua_2026.csv | 8 | 7 ky da hop (27-28/01 ... 27-28/10); hop 8-9/12 chua dien ra |
| polymarket_fed.csv | 119197 | 9 chuoi (8 ky + 1 phu), xem duoi |
| _goc/ | | ban goc HTML da tai de tai lap (BLS/BEA/Fed) |
| _xay_dung.py, _tai_polymarket.py | | tai lap lich/ket qua tu `_goc/`; tai lai Polymarket qua mang |

Cot `ngay_gio_vn` = UTC+7 tinh bang zoneinfo (DST My dung: vd FOMC 28/01 14:00 EST = 29/01 02:00 VN; FOMC 29/04 14:00 EDT = 30/04 01:00 VN).

`xac_suat` Polymarket = gia token "Yes" cua tung ket qua (khong chuan hoa, tong ~1). Ket qua: No change, 25 bps decrease, 50+ bps decrease, 25(+) bps increase, 50+ bps increase (thang 1/3/4 chi co 4 muc, khong co 50+ increase). Diem cuoi cua moi chuoi thuong nam SAU gio quyet dinh (da chot 0/1): khi dung phai loc `ts <= t` (cong_cu/tin_tuc.py da lam).

## Phu song Polymarket (UTC)
| ky_hop | tu | den | so dong |
|---|---|---|---|
| 2026-01 | 2025-09-17 | 2026-01-28 | 12746 |
| 2026-03 | 2025-10-29 | 2026-03-18 | 13410 |
| 2026-04 | 2025-11-13 | 2026-04-29 | 14828 |
| 2026-06 | 2025-12-10 | 2026-06-17 | 20719 |
| 2026-07 | 2026-03-20 | 2026-07-29 | 14531 |
| 2026-09 | 2026-05-13 | 2026-09-16 | 15016 |
| 2026-09_phu | 2026-04-30 | 2026-05-11 | 1390 |
| 2026-10 | 2026-06-18 | 2026-10-28 | 15676 |
| 2026-12 | 2026-07-30 | 2026-10-31 (chua chot) | 10880 |

## Cho thieu / han che
- Khong co gia tri thuc te cua CPI/PPI/NFP/PCE/GDP/JOLTS (chi gio cong bo + ky); chua tim nguon cong khai on dinh cho so lieu va bang so voi du bao.
- Bien ban FOMC ky 27-28/10 va 8-9/12: chua co ngay cong bo tren trang Fed. Gio 14:00 ET cua bien ban la thong le, chua xac minh (ghi trong ghi_chu).
- Hop 8-9/12: chua co statement; market Polymarket cua no van mo.
- Gio chinh xac cua cac su kien BLS/BEA ngoai 8:30/10:00 khong co ngoai le; da lay dung theo cot gio cua trang nguon.
- Cot `phieu` trong fomc_ket_qua_2026.csv de trong cho 3 ky dau (28/01, 18/03, 29/04): statement tuong ung khong co cum "by a X-Y vote" dang van ban; xem `phan_doi`.
- Lich BLS qua Wayback: neu can chac chan hon, doi chieu voi bls.gov bang trinh duyet.

## Kiem tra toan ven (shasum -a 256, tai thoi diem tao)
```
eb2b926e261003326973d260b49c723cd4bac149a4a23ff4e85f21e96740d04f  fomc_ket_qua_2026.csv
81d3f0548a9b1b589186e2d7c49066be093a3b35d68bbc089245ef5eff009efc  lich_kinh_te_2026.csv
88c8f2e336a8ce04777fb1715a8ea3140cd8a6eacaaa2d99e0b56f58e6fff08c  polymarket_fed.csv
```
