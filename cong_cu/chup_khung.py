#!/usr/bin/env python3
"""Cắt khung hình từ video YouTube tại các mốc giờ → so_tay/khung/<id>_<hhmmss>.jpg

Mỗi video hỏi YouTube 1 lần lấy link file (≤1080p để đọc được số trên trục giá), ffmpeg nhảy tới từng mốc lấy 1 khung.
Giãn tối thiểu GIAN_CACH giây giữa 2 lần gọi YouTube, kể cả khi nhiều tiến trình chạy cùng lúc (khoá file).
Cách dùng: python3 cong_cu/chup_khung.py <video_id> <hh:mm:ss> [<hh:mm:ss> ...]
"""
import fcntl, os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "so_tay" / "khung"
KHOA = GOC / "so_tay" / ".khoa_youtube"
GIAN_CACH = int(os.environ.get("GIAN_CACH", 60))  # chụp ảnh: user cho tăng tốc → chạy với GIAN_CACH=15


def cho_luot():
    KHOA.parent.mkdir(parents=True, exist_ok=True)
    f = KHOA.open("a+")
    fcntl.flock(f, fcntl.LOCK_EX)
    f.seek(0)
    cuoi = float(f.read() or 0)
    if time.time() - cuoi < GIAN_CACH:
        time.sleep(GIAN_CACH - (time.time() - cuoi))
    return f


def xong_luot(f):
    f.seek(0); f.truncate(); f.write(str(time.time())); f.flush()
    fcntl.flock(f, fcntl.LOCK_UN); f.close()


def giay(moc):
    h, m, s = map(int, moc.split(":"))
    return h * 3600 + m * 60 + s


def chup(vid, mocs):
    """Hỏi YouTube 1 lần lấy link file video (trong khoá, giãn 60 giây), rồi ffmpeg nhảy thẳng tới từng mốc
    trên file đó (tải trực tiếp từ máy chủ video, không gọi lại trang YouTube)."""
    RA.mkdir(parents=True, exist_ok=True)
    can = [m for m in mocs if not (RA / f"{vid}_{m.replace(':', '')}.jpg").exists()]
    if can:
        f = cho_luot()
        try:
            r = subprocess.run(["yt-dlp", "-g", "-f", "bv*[height<=1080][ext=mp4]/bv*[height<=1080]",
                                f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=120)
        finally:
            xong_luot(f)
        if "confirm you" in r.stderr or "429" in r.stderr:
            sys.exit(f"■ YouTube nghi bot — DỪNG: {r.stderr.strip()[-200:]}")
        url = r.stdout.strip().splitlines()[0] if r.stdout.strip() else None
        cat = lambda m: subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(giay(m) + 1), "-i", url, "-frames:v", "1",
                                        "-q:v", "2", str(RA / f"{vid}_{m.replace(':', '')}.jpg")], timeout=120)
        if url:
            with ThreadPoolExecutor(4) as ex:  # tải thẳng từ máy chủ video, không gọi lại trang YouTube
                list(ex.map(cat, can))
    return [(m, (RA / f"{vid}_{m.replace(':', '')}.jpg").exists()) for m in mocs]


if __name__ == "__main__":
    vid, mocs = sys.argv[1], sys.argv[2:]
    for moc, ok in chup(vid, mocs):
        print("✓" if ok else "✗", vid, moc)
