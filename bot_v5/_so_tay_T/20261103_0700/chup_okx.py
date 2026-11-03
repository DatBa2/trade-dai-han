"""Chụp trang công khai OKX; không đăng nhập hoặc thao tác lệnh."""
import json
import os
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(tempfile.gettempdir()) / 'codex-okx-capture-deps'))
from playwright.sync_api import sync_playwright

P = Path(__file__).resolve().parent
with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1180}, locale='en-US', timezone_id='Asia/Ho_Chi_Minh')
    page = context.new_page()
    page.goto('https://www.okx.com/trade-swap/xau-usdt-swap', wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(7000)
    skip = page.get_by_role('button', name='Skip', exact=True)
    if skip.count():
        skip.click()
    page.get_by_role('button', name='1D', exact=True).click()
    page.wait_for_timeout(5000)
    page.mouse.click(1136, 191)
    page.wait_for_timeout(2000)
    page.screenshot(path=str(P / 'OKX_XAU_D1_toan_canh.png'))
    page.mouse.move(1500, 550)
    for _ in range(12):
        page.mouse.wheel(0, -100)
        page.wait_for_timeout(90)
    page.wait_for_timeout(1200)
    page.mouse.move(35, 15)
    page.wait_for_timeout(600)
    page.screenshot(path=str(P / 'OKX_XAU_D1_nguon.png'))
    # SVG thêm trên trang đang mở: giữ nguyên nến, trục giá và chỉ báo OKX.
    # Tọa độ theo chart D1 đã kiểm bằng mắt: 4.000 tại y≈681,5, 40 giá≈32px.
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1180" style="position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;z-index:2147483647;font-family:Arial">
    <rect x="900" y="673.5" width="946" height="24" fill="#ff7788" fill-opacity="0.16" stroke="#ff9daa"/>
    <rect x="900" y="761.3" width="946" height="16" fill="#65dfbe" fill-opacity="0.2" stroke="#65dfbe"/>
    <line x1="1100" y1="611.3" x2="1846" y2="611.3" stroke="#ffd176" stroke-width="2" stroke-dasharray="9 5"/>
    <line x1="1291" y1="505.4" x2="1706" y2="650.9" stroke="#fed17c" stroke-width="3"/>
    <text x="1100" y="592" fill="#ffd176" font-size="21">View D1 sai: ĐÓNG trên 4.088</text>
    <text x="920" y="664" fill="#ffb0bc" font-size="21">Chờ SHORT 3.980–4.010 · cần H1 xác nhận</text>
    <text x="920" y="803" fill="#8af3d4" font-size="21">TP gần 3.880–3.900 · đáy D1 3.880,6</text>
    <rect x="1210" y="115" width="600" height="255" rx="12" fill="#101b2a" fill-opacity="0.94" stroke="#8d9fb6"/>
    <text x="1235" y="151" fill="#f2f4f8" font-size="25">CHÚ THÍCH CỦA BOT · OKX XAUUSDT D1</text>
    <text x="1235" y="187" fill="#edb084" font-size="22">GIỮ GIẢM · H4 đang kẹp EMA34, chờ giá</text>
    <text x="1235" y="222" fill="#c2cfdf" font-size="20">Fibo hồi 0,5–0,618: 3.984,3–4.008,8</text>
    <text x="1235" y="255" fill="#c2cfdf" font-size="20">Hội tụ đáy cũ 3.980 + EMA89 H4 4.009,7</text>
    <text x="1235" y="288" fill="#c2cfdf" font-size="20">Trendline phụ: đỉnh D1 12/10 → 28/10</text>
    <text x="1235" y="321" fill="#f1d68a" font-size="19">Nến cuối 03/11 ĐANG CHẠY · bỏ khi xác nhận</text>
    <text x="1235" y="349" fill="#c2cfdf" font-size="17">Nhận định dùng nến đóng tới 03/11/2026 07:00 VN</text>
    </svg>'''
    page.evaluate('(svg)=>document.body.insertAdjacentHTML("beforeend",svg)', svg)
    page.screenshot(path=str(P / 'OKX_XAU_D1_chu_thich.png'))
    (P / 'OKX_capture_meta.json').write_text(json.dumps({'url': page.url, 'khung': '1D', 'gio_chup_vn': __import__('datetime').datetime.now().isoformat(timespec='seconds'), 'nen_cuoi': 'đang chạy; chỉ hiển thị, không dùng xác nhận', 'chu_thich': 'SVG chèn tại trình duyệt, nến OKX giữ nguyên'}, ensure_ascii=False, indent=1), encoding='utf-8')
    (P / 'OKX_dom.txt').write_text(page.locator('body').inner_text(), encoding='utf-8')
    print('URL', page.url)
    print('TITLE', page.title())
    print(page.locator('body').inner_text()[:12000])
    print('CONTROLS', page.locator('button').evaluate_all('(xs)=>xs.filter(x=>x.getAttribute("title")||x.getAttribute("aria-label")).map(x=>({text:x.innerText,title:x.getAttribute("title"),aria:x.getAttribute("aria-label")}))'))
    browser.close()
