#!/usr/bin/env python3
"""Chỉ báo dùng chung cho bot v4 — đúng mục 2 của `bot_v4/THIET_KE.md` (TK 2).

Mọi hàm đều NHÂN QUẢ: giá trị ở vị trí i chỉ dùng dữ liệu ở vị trí ≤ i (đệ quy trái → phải),
riêng fractal trả về chỉ số nến đỉnh/đáy i và chỉ được DÙNG khi nến i + k đã đóng (hàm `fractal_da_xac_nhan`).
Chưa đủ dữ liệu → None. Kiểm thử: `python3 bot_v4/kiem_tra.py` (nhóm 3: so với tính tay).
"""
import bisect


def ema(xs, n):
    """TK 2 — EMA n: đệ quy α = 2/(n+1), khởi tạo = SMA n giá trị đầu; trước đó (chưa đủ n) = None."""
    ra = [None] * len(xs)
    if len(xs) < n:
        return ra
    a = 2.0 / (n + 1)
    v = sum(xs[:n]) / n
    ra[n - 1] = v
    for i in range(n, len(xs)):
        v = a * xs[i] + (1 - a) * v
        ra[i] = v
    return ra


def _rsi_tu(lai, lo):
    if lo == 0:
        return 100.0 if lai > 0 else 50.0
    return 100.0 - 100.0 / (1.0 + lai / lo)


def rsi_wilder(c, n=14):
    """TK 2 — RSI n kiểu Wilder.
    Thay đổi d_i = c_i − c_{i−1} (i ≥ 1). Trung bình lãi/lỗ đầu = trung bình cộng n thay đổi đầu (d_1..d_n) → RSI đầu ở
    vị trí n; sau đó TB_i = (TB_{i−1}·(n−1) + giá_trị_i)/n. Lỗ TB = 0 → RSI 100 (hoặc 50 nếu cũng không lãi)."""
    ra = [None] * len(c)
    if len(c) < n + 1:
        return ra
    lai = [0.0] + [max(c[i] - c[i - 1], 0.0) for i in range(1, len(c))]
    lo = [0.0] + [max(c[i - 1] - c[i], 0.0) for i in range(1, len(c))]
    tb_lai = sum(lai[1:n + 1]) / n
    tb_lo = sum(lo[1:n + 1]) / n
    ra[n] = _rsi_tu(tb_lai, tb_lo)
    for i in range(n + 1, len(c)):
        tb_lai = (tb_lai * (n - 1) + lai[i]) / n
        tb_lo = (tb_lo * (n - 1) + lo[i]) / n
        ra[i] = _rsi_tu(tb_lai, tb_lo)
    return ra


def true_range(h, l, c):
    """TR_0 = H_0 − L_0 (chưa có close trước); TR_i = max(H−L, |H − C_{i−1}|, |L − C_{i−1}|)."""
    ra = []
    for i in range(len(h)):
        if i == 0:
            ra.append(h[0] - l[0])
        else:
            ra.append(max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])))
    return ra


def atr_wilder(h, l, c, n=14):
    """TK 2 — ATR n kiểu Wilder trên True Range: ATR đầu (vị trí n−1) = trung bình cộng TR_0..TR_{n−1};
    sau đó ATR_i = (ATR_{i−1}·(n−1) + TR_i)/n."""
    tr = true_range(h, l, c)
    ra = [None] * len(tr)
    if len(tr) < n:
        return ra
    v = sum(tr[:n]) / n
    ra[n - 1] = v
    for i in range(n, len(tr)):
        v = (v * (n - 1) + tr[i]) / n
        ra[i] = v
    return ra


def fractal(h, l, k=3):
    """TK 2 — Fractal 2k+1 nến (k trái, k phải). Trả (dinh, day): mỗi cái là list (i, giá) theo thứ tự thời gian.
    Đỉnh: h_i lớn nhất của 7 nến; nếu bằng nhau thì chỉ nến SỚM nhất là đỉnh (trái: lớn hơn hẳn; phải: ≥) — DG 7.
    Đáy đối xứng với low. Đỉnh/đáy ở i chỉ được DÙNG khi nến i + k đã đóng (xem `fractal_da_xac_nhan`).
    Hàm này cần nến i + k có trong dữ liệu mới công nhận i, nên khi dữ liệu bị cắt ở j thì không có fractal nào i > j − k."""
    dinh, day = [], []
    for i in range(k, len(h) - k):
        if h[i] > max(h[i - k:i]) and h[i] >= max(h[i + 1:i + k + 1]):
            dinh.append((i, h[i]))
        if l[i] < min(l[i - k:i]) and l[i] <= min(l[i + 1:i + k + 1]):
            day.append((i, l[i]))
    return dinh, day


def fractal_da_xac_nhan(ds, chi_so, t, k=3):
    """TK 2 — số lượng phần tử đầu của `ds` (list (i, giá)) đã xác nhận tại nến t: i + k ≤ t.
    `chi_so` = [i for i, _ in ds] (đã sắp tăng). Dùng: ds[:fractal_da_xac_nhan(...)]."""
    return bisect.bisect_right(chi_so, t - k)
