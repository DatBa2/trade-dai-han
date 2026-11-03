// Chụp trang web bằng Chrome có giao diện thật (điều khiển qua cổng nội bộ 9333 — Chrome DevTools Protocol).
// Dùng cho trang không có API / chặn trình duyệt chạy ngầm (Coinglass heatmap…).
// Chuẩn bị: mở Chrome riêng: "Google Chrome" --user-data-dir=<thư mục trống> --remote-debugging-port=9333
// Cách dùng: node cong_cu/chup_web.mjs <url> <file.png> [rộng=1600] [cao=2200] [chờ_ms=15000] [chữ_cần_cuộn_tới] [các_bước_JSON]
//   các_bước: [{"bam":"chữ"}, {"go":"chữ"}, {"cho":2000}] — bấm chuột thật vào phần tử có chữ đó / gõ chữ / chờ
const [url, ra, rong = 1600, cao = 2200, cho = 15000, cuonToi = '', buocJson = '[]'] = process.argv.slice(2);
const fs = await import('node:fs');
const tab = await (await fetch('http://127.0.0.1:9333/json/new?about:blank', { method: 'PUT' })).json();
const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));
let id = 0; const cho_tl = new Map();
ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.id && cho_tl.has(m.id)) { cho_tl.get(m.id)(m); cho_tl.delete(m.id); } });
const goi = (method, params = {}) => new Promise(r => { const i = ++id; cho_tl.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ngu = ms => new Promise(r => setTimeout(r, ms));

await goi('Emulation.setDeviceMetricsOverride', { width: +rong, height: +cao, deviceScaleFactor: 1, mobile: false });
await goi('Page.enable');
await goi('Page.navigate', { url });
await ngu(+cho);
// bấm chấp nhận cookie nếu có, rồi cuộn tới tiêu đề cần chụp
await goi('Runtime.evaluate', { expression: `(() => {
  const b = [...document.querySelectorAll('button')].find(x => /^(Accept|Accept All|Đồng ý)/i.test((x.innerText||'').trim()));
  if (b) b.click();
  const t = ${JSON.stringify(cuonToi)};
  if (t) { const h = [...document.querySelectorAll('h1,h2,h3,div,span')].find(x => (x.innerText||'').trim() === t); if (h) h.scrollIntoView(); }
  return 'ok'; })()` });
await ngu(3000);
for (const b of JSON.parse(buocJson)) {
  if (b.cho) await ngu(b.cho);
  if (b.go) { await goi('Input.insertText', { text: b.go }); await ngu(1500); }
  if (b.bam) {
    const r = await goi('Runtime.evaluate', { returnByValue: true, expression: `(() => {
      const t = ${JSON.stringify(b.bam)};
      const ds = [...document.querySelectorAll('body *')].filter(x => x.offsetParent && (x.innerText||x.value||'').trim() === t);
      const el = ds[ds.length - 1]; if (!el) return null;
      el.scrollIntoView({block: 'center'}); const q = el.getBoundingClientRect();
      return { x: q.x + q.width / 2, y: q.y + q.height / 2 }; })()` });
    const v = r.result.result.value;
    if (!v) { console.log('✗ không thấy:', b.bam); continue; }
    for (const type of ['mousePressed', 'mouseReleased'])
      await goi('Input.dispatchMouseEvent', { type, x: v.x, y: v.y, button: 'left', clickCount: 1 });
    await ngu(2000);
  }
}
if (cuonToi) await goi('Runtime.evaluate', { expression: `(() => { const h = [...document.querySelectorAll('h1,h2,h3,div,span')].find(x => (x.innerText||'').trim().startsWith(${JSON.stringify(cuonToi.split(' ')[0])}) && (x.innerText||'').includes('Liquidation Heatmap')); if (h) h.scrollIntoView(); })()` });
await ngu(4000);
const anh = await goi('Page.captureScreenshot', { format: 'png' });
fs.writeFileSync(ra, Buffer.from(anh.result.data, 'base64'));
// chữ trên trang cạnh ảnh: số liệu đọc được bằng máy, không phải đoán từ pixel
const chu = await goi('Runtime.evaluate', { returnByValue: true, expression: '(document.body && document.body.innerText || "").slice(0, 200000)' });
fs.writeFileSync(ra.replace(/\.png$/i, '') + '.txt', chu.result.result.value || '');
await fetch(`http://127.0.0.1:9333/json/close/${tab.id}`);
console.log('✓', ra);
ws.close();
