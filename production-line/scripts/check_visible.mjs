import { chromium } from 'playwright';

// innerText 會把 opacity:0 的文字也算進來，所以「有字」不等於「看得見」。
// 這支改成量**實際看得見的像素**：檢查元素的 computed opacity 與 visibility。
const base = process.argv[2].replace(/\/$/, '');
const routes = process.argv.slice(3);
const W = 1280;
const H = 585; // 對齊使用者截圖的可視高度

const browser = await chromium.launch();
for (const r of routes) {
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  const errs = [];
  page.on('pageerror', (e) => errs.push('JS: ' + String(e).slice(0, 120)));
  await page.goto(base + r, { waitUntil: 'networkidle', timeout: 25000 });
  await page.waitForTimeout(1500);

  const info = await page.evaluate(() => {
    const all = Array.from(document.querySelectorAll('body *'));
    let hidden = 0;
    let visible = 0;
    const hiddenSamples = [];
    for (const el of all) {
      if (!el.textContent || !el.textContent.trim()) continue;
      const cs = getComputedStyle(el);
      const op = parseFloat(cs.opacity);
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) continue;
      if (op < 0.05 || cs.visibility === 'hidden' || cs.display === 'none') {
        hidden++;
        if (hiddenSamples.length < 3) {
          hiddenSamples.push(
            el.tagName.toLowerCase() + '.' + (el.className || '').toString().slice(0, 40) +
            ' opacity=' + cs.opacity + ' transform=' + cs.transform.slice(0, 30)
          );
        }
      } else {
        visible++;
      }
    }
    // 首屏實際看得見的文字
    const inView = Array.from(document.querySelectorAll('body *')).filter((el) => {
      const rc = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return rc.top < window.innerHeight && rc.bottom > 0 && rc.height > 0 &&
             parseFloat(cs.opacity) > 0.05 && cs.visibility !== 'hidden';
    }).length;
    return { hidden, visible, inView, hiddenSamples, bodyText: (document.body.innerText || '').trim().length };
  });

  console.log(
    r.padEnd(28) +
    ' innerText=' + String(info.bodyText).padStart(5) +
    ' 可見元素=' + String(info.visible).padStart(4) +
    ' 隱形元素=' + String(info.hidden).padStart(4) +
    ' 首屏可見=' + String(info.inView).padStart(4) +
    (info.hidden > info.visible ? '   <<< 大部分是隱形的' : '')
  );
  info.hiddenSamples.forEach((s) => console.log('        隱形樣本: ' + s));
  if (errs.length) console.log('        ' + errs[0]);
  await page.close();
}
await browser.close();
