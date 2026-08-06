import { chromium } from 'playwright';

// 全站爬：找出每一個站內連結，逐一開起來看畫面上有沒有字。
// 用回應碼驗網站會漏掉「打得開但畫面是空的」，所以這裡只信畫面內容。
const base = process.argv[2].replace(/\/$/, '');
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1366, height: 900 } });

// 先收集全站連結
const seed = await ctx.newPage();
await seed.goto(base, { waitUntil: 'networkidle' });
await seed.waitForTimeout(1000);
// 捲到底讓延遲載入的區塊出現
const h = await seed.evaluate(() => document.body.scrollHeight);
for (let y = 0; y < h; y += 600) {
  await seed.evaluate((v) => window.scrollTo(0, v), y);
  await seed.waitForTimeout(120);
}
const hrefs = await seed.evaluate(() =>
  Array.from(document.querySelectorAll('a[href]'))
    .map((a) => a.getAttribute('href'))
    .filter((h) => h && h.startsWith('/'))
);
await seed.close();

const routes = [...new Set(hrefs)].sort();
console.log('站內連結 ' + routes.length + ' 個，逐一開啟檢查');
console.log('');

const broken = [];
for (const r of routes) {
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', (e) => errs.push(String(e).slice(0, 90)));
  let status = 0;
  try {
    const resp = await page.goto(base + r, { waitUntil: 'domcontentloaded', timeout: 20000 });
    status = resp ? resp.status() : 0;
    await page.waitForTimeout(1100);
  } catch (e) {
    errs.push('goto: ' + String(e).slice(0, 70));
  }
  const txt = (await page.evaluate(() => (document.body ? document.body.innerText : '') || '')).trim();
  const ok = status === 200 && txt.length > 250;
  if (!ok) broken.push({ r, status, len: txt.length, errs });
  console.log(
    (ok ? '  OK  ' : '  BAD ') +
    String(status).padEnd(5) +
    String(txt.length).padStart(6) + ' chars  ' + r +
    (errs.length ? '   ' + errs[0] : '')
  );
  await page.close();
}

console.log('');
console.log('壞掉 ' + broken.length + ' / ' + routes.length);
await browser.close();
