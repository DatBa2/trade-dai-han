#!/usr/bin/env python3
"""Lấy transcript livestream FAM Trading, lùi từ buổi mới nhất về MOC_DAU.

Đường 1: phụ đề YouTube tiếng Việt      → transcripts/phu_de/
Đường 2: buổi không có phụ đề → Whisper → transcripts/whisper/
Giãn GIAN_CACH giây giữa 2 lần gọi YouTube để không bị coi là spam.
Chạy lại được: buổi đã có trong danh_sach.tsv thì bỏ qua, không gọi YouTube.

Cách dùng: python3 cong_cu/lay_transcript.py [--tu-ngay YYYY-MM-DD] [--them N] [--chuyen-lai]
"""
import argparse, csv, datetime as dt, re, subprocess, sys, time
from pathlib import Path

KENH = "https://www.youtube.com/@famtrading/streams"
MOC_DAU = dt.date(2026, 9, 16)
MOI_NHAT = 0             # >0: chỉ lấy N video mới nhất, bỏ qua mốc ngày
GIAN_CACH = 60
DUNG_SAU_CU = 3          # gặp liên tiếp 3 buổi cũ hơn MOC_DAU thì dừng
VN = dt.timezone(dt.timedelta(hours=7))
GOC = Path(__file__).resolve().parent.parent / "transcripts"
PHU_DE, WHISPER = GOC / "phu_de", GOC / "whisper"
DANH_SACH = GOC / "danh_sach.tsv"
COT = ["id", "ngay", "gio", "nguon", "so_tu", "phut", "tieu_de"]
MODEL = Path.home() / ".cache/whisper/ggml-large-v3-turbo.bin"
VAD = Path.home() / ".cache/whisper/ggml-silero-v5.1.2.bin"
# YouTube nghi bot → dừng hẳn, không cố gọi tiếp
CHAN = ("confirm you", "HTTP Error 429", "Too Many Requests")

_lan_goi_cuoi = 0.0


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def goi_yt(args):
    """Gọi yt-dlp, tự giãn GIAN_CACH giây kể từ lần gọi trước."""
    global _lan_goi_cuoi
    cho = _lan_goi_cuoi + GIAN_CACH - time.time()
    if _lan_goi_cuoi and cho > 0:
        time.sleep(cho)
    _lan_goi_cuoi = time.time()
    r = subprocess.run(["yt-dlp", "--extractor-args", "youtube:lang=vi", *args],
                       capture_output=True, text=True)
    if any(c in r.stderr for c in CHAN):
        log("■ YouTube chặn/nghi bot — DỪNG. Lỗi:", r.stderr.strip()[-300:])
        sys.exit(2)
    return r


def vtt_sang_txt(vtt, txt):
    """Gộp VTT thành văn bản liền mạch.
    Xét TỪNG DÒNG chứ không cả khối: phụ đề auto dạng cuộn (<c>) lặp lại dòng trước ở đầu mỗi khối,
    gộp cả khối như ~/bin/yt2text thì chữ bị nhân đôi/ba."""
    blocks = re.split(r'\n\n+', vtt.read_text(encoding='utf-8'))
    out, prev = [], None
    for b in blocks:
        for l in b.strip().split('\n'):
            if not l or '-->' in l or l.strip().isdigit() or l.startswith(('WEBVTT', 'Kind:', 'Language:')):
                continue
            s = re.sub(r'<[^>]+>', '', l).strip()
            if s and s != prev:
                out.append(s); prev = s
    t = re.sub(r'\s+', ' ', ' '.join(out))
    t = re.sub(r'(?<=[.!?]) (?=[A-ZĐÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĨŨƠƯ])', '\n', t)
    txt.write_text(t, encoding='utf-8')
    return len(t.split())


def doc_danh_sach():
    if not DANH_SACH.exists():
        return {}
    with DANH_SACH.open(encoding='utf-8') as f:
        return {r["id"]: r for r in csv.DictReader(f, delimiter='\t')}


def ghi_danh_sach(rows):
    xep = sorted(rows.values(), key=lambda r: (r["ngay"], r["gio"]), reverse=True)
    with DANH_SACH.open("w", encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, COT, delimiter='\t')
        w.writeheader(); w.writerows(xep)


def lay_ids():
    r = goi_yt(["--flat-playlist", "--playlist-end", str(MOI_NHAT or 200), "--print", "%(id)s", KENH])
    return [l.strip() for l in r.stdout.splitlines() if l.strip()]


def lay_phu_de(vid):
    """Trả về dict hàng danh sách; nguon = phu_de / cho_whisper / cu / bo_qua."""
    r = goi_yt(["--skip-download", "--no-simulate", "--write-subs", "--write-auto-subs",
                "--sub-langs", "vi", "--sub-format", "vtt",
                "--print", "%(release_timestamp)s|%(timestamp)s|%(live_status)s|%(duration)s|%(title)s",
                "-o", str(PHU_DE / f"{vid}.%(ext)s"), f"https://www.youtube.com/watch?v={vid}"])
    dong = [l for l in r.stdout.splitlines() if l.count("|") >= 4]
    if not dong:
        log(f"  ✗ {vid}: không đọc được thông tin —", r.stderr.strip()[-200:])
        return None
    rel, ts, trang_thai, dur, tieu_de = dong[-1].split("|", 4)
    moc = next((int(x) for x in (rel, ts) if x.isdigit()), None)
    luc = dt.datetime.fromtimestamp(moc, VN) if moc else None
    hang = {"id": vid, "ngay": luc.strftime("%Y-%m-%d") if luc else "?",
            "gio": luc.strftime("%H%M") if luc else "?", "nguon": "", "so_tu": "",
            "phut": str(round(int(dur) / 60)) if dur.isdigit() else "", "tieu_de": tieu_de}
    vtt = next(PHU_DE.glob(f"{vid}.vi*.vtt"), None)
    if trang_thai in ("is_live", "is_upcoming"):
        hang["nguon"] = "bo_qua"
    elif luc and luc.date() < MOC_DAU and not MOI_NHAT:
        hang["nguon"] = "cu"
    elif vtt and vtt.stat().st_size > 0:
        ten = PHU_DE / f"{hang['ngay']}_{hang['gio']}_{vid}"
        vtt.rename(ten.with_suffix(".vtt"))
        hang["nguon"], hang["so_tu"] = "phu_de", str(vtt_sang_txt(ten.with_suffix(".vtt"), ten.with_suffix(".txt")))
    else:
        hang["nguon"] = "cho_whisper"
    if hang["nguon"] != "phu_de" and vtt:
        vtt.unlink()
    return hang


def chay_whisper(hang):
    vid = hang["id"]
    goi_yt(["-f", "ba[language^=vi]/ba", "-x", "--audio-format", "wav",
            "--postprocessor-args", "-ar 16000 -ac 1",
            "-o", str(WHISPER / f"{vid}.%(ext)s"), f"https://www.youtube.com/watch?v={vid}"])
    wav = WHISPER / f"{vid}.wav"
    if not wav.exists():
        log(f"  ✗ {vid}: tải audio thất bại")
        return False
    ten = WHISPER / f"{hang['ngay']}_{hang['gio']}_{vid}"
    # VAD cắt đoạn im lặng → chặn ảo giác "Hãy subscribe cho kênh..."
    subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(wav), "-l", "vi", "-t", "8", "-sns",
                    "--vad", "--vad-model", str(VAD), "-ovtt", "-of", str(ten)],
                   capture_output=True)
    wav.unlink()
    vtt = ten.with_suffix(".vtt")
    if not vtt.exists():
        log(f"  ✗ {vid}: Whisper không ra file")
        return False
    hang["nguon"], hang["so_tu"] = "whisper", str(vtt_sang_txt(vtt, ten.with_suffix(".txt")))
    return True


def main():
    global GIAN_CACH, MOC_DAU, KENH, MOI_NHAT, GOC, PHU_DE, WHISPER, DANH_SACH
    ap = argparse.ArgumentParser()
    ap.add_argument("--tu-ngay", default=MOC_DAU.isoformat(), help="lùi tới ngày này (mặc định 2026-09-16)")
    ap.add_argument("--them", type=int, default=0, help="dừng sau khi lấy được thêm N buổi mới")
    ap.add_argument("--chuyen-lai", action="store_true", help="chỉ dựng lại .txt từ .vtt đã có, không gọi YouTube")
    ap.add_argument("--kenh", default=KENH, help="URL tab video/streams của kênh (mặc định kênh FAM)")
    ap.add_argument("--thu-muc", default=str(GOC), help="thư mục gốc chứa phu_de/, whisper/, danh_sach.tsv")
    ap.add_argument("--moi-nhat", type=int, default=0, help="lấy N video mới nhất của kênh, bỏ qua mốc ngày")
    ap.add_argument("--gian-cach", type=int, default=GIAN_CACH, help="giây giãn giữa 2 lần gọi YouTube (mặc định 60)")
    a = ap.parse_args()
    GIAN_CACH = a.gian_cach
    KENH, MOI_NHAT = a.kenh, a.moi_nhat
    GOC = Path(a.thu_muc).resolve()
    PHU_DE, WHISPER, DANH_SACH = GOC / "phu_de", GOC / "whisper", GOC / "danh_sach.tsv"
    MOC_DAU = dt.date.fromisoformat(a.tu_ngay)
    PHU_DE.mkdir(parents=True, exist_ok=True); WHISPER.mkdir(parents=True, exist_ok=True)
    rows = doc_danh_sach()

    if a.chuyen_lai:
        n = 0
        for vtt in [*PHU_DE.glob("*.vtt"), *WHISPER.glob("*.vtt")]:
            vid = vtt.stem.split("_", 2)[2]
            if vid in rows:
                rows[vid]["so_tu"] = str(vtt_sang_txt(vtt, vtt.with_suffix(".txt"))); n += 1
        ghi_danh_sach(rows)
        log(f"■ Dựng lại {n} file .txt")
        return

    ids = lay_ids()
    log(f"▶ Kênh có {len(ids)} buổi live trong danh sách; lùi từ mới nhất về {MOC_DAU}")
    lam, cu_lien = 0, 0
    for vid in ids:
        if a.them and lam >= a.them:
            log(f"■ Đã lấy thêm đủ {a.them} buổi")
            break
        hang = rows.get(vid)
        # buổi từng bị gạt vì cũ hơn mốc cũ, nay nằm trong mốc mới → lấy lại
        if hang is None or (hang["nguon"] == "cu" and hang["ngay"] >= a.tu_ngay):
            hang = lay_phu_de(vid)
            if hang is None:
                continue
            if hang["nguon"] in ("phu_de", "cho_whisper"):
                lam += 1
            rows[vid] = hang; ghi_danh_sach(rows)
            log(f"  {hang['ngay']} {hang['gio']} {vid} → {hang['nguon']} {hang['so_tu']}  {hang['tieu_de'][:60]}")
        if hang["nguon"] == "cu":
            cu_lien += 1
            if cu_lien >= DUNG_SAU_CU:
                log(f"■ Đã lùi qua {MOC_DAU} — hết phần phụ đề")
                break
        else:
            cu_lien = 0

    cho = [h for h in rows.values() if h["nguon"] == "cho_whisper"]
    log(f"▶ Whisper cho {len(cho)} buổi không có phụ đề")
    for hang in sorted(cho, key=lambda h: (h["ngay"], h["gio"]), reverse=True):
        log(f"  Whisper {hang['ngay']} {hang['id']} ({hang['phut']} phút)…")
        if chay_whisper(hang):
            ghi_danh_sach(rows)
            log(f"  ✓ {hang['id']} → whisper {hang['so_tu']} từ")
    log("■ XONG")


if __name__ == "__main__":
    main()
