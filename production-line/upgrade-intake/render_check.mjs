// 第二關的眼睛：開真的瀏覽器看真的畫面，把量到的東西吐成 JSON。
//
// 為什麼不用回應碼：頁面打得開不等於畫得出來。伺服器回 200、HTML 有內容、
// 但 JS 掛掉導致整片空白，回應碼一樣是 200。見 PITFALLS「用回應碼驗網站」。
//
// 可見度的判斷沿用 scripts/check_visible.mjs 的做法：opacity 與 visibility 都要算，
// 因為 innerText 會把 opacity:0 的字也算進去。
//
// 用法：node render_check.mjs <base-url> <route> <screenshot-path> [必須出現的字...]
// 輸出：單行 JSON 到 stdout。

// 用 createRequire 而不是直接 import，因為這支腳本住在沒有 node_modules 的資料夾裡。
// createRequire 會吃 NODE_PATH，呼叫端（verify.py）會把全域 node_modules 指過來。
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const [base, route, shotPath, ...mustTexts] = process.argv.slice(2);
const out = {
  ok: false,
  route,
  bodyText: 0,
  visible: 0,
  inView: 0,
  hidden: 0,
  consoleErrors: [],
  pageErrors: [],
  missingTexts: [],
  screenshot: null,
  error: null,
};

const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', (e) => out.pageErrors.push(String(e).slice(0, 200)));
  page.on('console', (m) => {
    if (m.type() === 'error') out.consoleErrors.push(m.text().slice(0, 200));
  });

  await page.goto(base.replace(/\/$/, '') + route, {
    waitUntil: 'networkidle',
    timeout: 30000,
  });
  await page.waitForTimeout(1500);

  const info = await page.evaluate(() => {
    const all = Array.from(document.querySelectorAll('body *'));
    let hidden = 0;
    let visible = 0;
    for (const el of all) {
      if (!el.textContent || !el.textContent.trim()) continue;
      const cs = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) continue;
      if (parseFloat(cs.opacity) < 0.05 || cs.visibility === 'hidden' || cs.display === 'none') {
        hidden++;
      } else {
        visible++;
      }
    }
    const inView = all.filter((el) => {
      const rc = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return rc.top < window.innerHeight && rc.bottom > 0 && rc.height > 0 &&
             parseFloat(cs.opacity) > 0.05 && cs.visibility !== 'hidden';
    }).length;
    return {
      hidden,
      visible,
      inView,
      bodyText: (document.body.innerText || '').trim().length,
      html: document.body.innerText || '',
    };
  });

  out.bodyText = info.bodyText;
  out.visible = info.visible;
  out.inView = info.inView;
  out.hidden = info.hidden;
  out.missingTexts = mustTexts.filter((t) => !info.html.includes(t));

  if (shotPath && shotPath !== '-') {
    await page.screenshot({ path: shotPath, fullPage: true });
    out.screenshot = shotPath;
  }
  out.ok = true;
} catch (e) {
  out.error = String(e).slice(0, 400);
} finally {
  await browser.close();
}

process.stdout.write(JSON.stringify(out));
