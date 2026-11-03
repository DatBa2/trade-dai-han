import asyncio
import datetime as dt
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0,str(Path(tempfile.gettempdir())/'codex-okx-capture-deps'))
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parent

async def main():
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(channel='msedge',headless=True)
        async def chup(ma):
            context=await browser.new_context(viewport={'width':1920,'height':1180},locale='en-US',timezone_id='Asia/Ho_Chi_Minh')
            page=await context.new_page()
            url='https://www.okx.com/trade-swap/'+ma.lower()+'-usdt-swap'
            try:
                await page.goto(url,wait_until='domcontentloaded',timeout=60000)
                await page.wait_for_timeout(6000)
                skip=page.get_by_role('button',name='Skip',exact=True)
                if await skip.count(): await skip.click()
                await page.get_by_role('button',name='1D',exact=True).click(timeout=20000)
                await page.wait_for_timeout(2000)
                await page.mouse.click(1136,191)
                await page.wait_for_timeout(1200)
                await page.mouse.move(1500,550)
                for _ in range(12):
                    await page.mouse.wheel(0,-100)
                    await page.wait_for_timeout(90)
                await page.mouse.move(35,15)
                await page.wait_for_timeout(700)
                await page.screenshot(path=str(P/(ma+'_D1_OKX.png')))
                meta={'ma':ma,'url':page.url,'gio_chup_vn':dt.datetime.now().isoformat(timespec='seconds'),
                      'ghi_chu':'Screenshot D1 thực, cây cuối đang chạy không dùng xác nhận; chỉ báo nền là MA mặc định OKX.'}
                (P/(ma+'_anh_meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=1),encoding='utf-8')
                print('SCREENSHOT',ma,flush=True)
            except Exception as e:
                print('SCREENSHOT ERROR',ma,type(e).__name__,str(e),flush=True)
            await context.close()
        await asyncio.gather(*(chup(m) for m in ['DOGE','ETH','SUI']))
        await browser.close()

asyncio.run(main())
