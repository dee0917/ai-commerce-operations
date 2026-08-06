# -*- coding: utf-8 -*-
"""
第一關：情報篩選。

從每日開源情報挑出「有可能對建站有幫助」的候選，其餘全部擋掉並記下理由。
這一關只做確定性的機械判斷，不做品質判斷。品質判斷在第二關 verify.py，
而第二關的唯一依據是「拿它對這條產線做一次實際的事」的結果。

四道機械篩：
  1. 相關性：只收六類與建站直接相關的東西，其餘標 OUT_不相關
  2. 去重：這條產線自己評估過的（LEDGER.jsonl）標 OUT_已評估，不重複評估
  3. 活躍度：最後一次推送超過 180 天標 OUT_停止維護，封存的標 OUT_已封存
  4. 查得到才算數：查不到專案資料標 UNKNOWN，不會混進候選清單

去重為什麼不直接吃情報 repo 的 DECISIONS.md：
那本帳本回答的是「要不要裝進系統」，這一關回答的是「要不要接進產線」，兩個問題不同。
一個前端函式庫不會被「裝進系統」，但可能該被產線當成依賴採用。
所以 DECISIONS.md 的舊結論只會被帶進來當背景資訊（prior_decision 欄位），
不會直接判死。只有兩種情況例外，因為那兩種已經沒有東西可以決定：
  - 標籤是【已裝/已接】：已經採用過了
  - 理由裡提到要改 MCP 設定：這是硬紅線，任何情況都不碰
採用之後 adopt.py 會把結論寫回 DECISIONS.md，情報端才不會再推同一個東西。

輸入來源用環境變數 DIGEST_REPO 指定情報 repo 的位置，沒設就直接失敗，
不會安靜地跑出一份空清單。

用法：
    set DIGEST_REPO=<情報 repo 路徑>
    python screen.py                 只看最近 7 份情報
    python screen.py --days 30       看最近 30 份
    python screen.py --no-pull       不要更新情報 repo
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE_DIR = os.path.join(HERE, 'queue')

# 六類與建站直接相關的東西。每一條都是「強訊號」，
# 單獨出現就足以讓這個項目值得進第二關實測。
CATEGORIES = {
    '前端框架與元件庫': [
        'next.js', 'nextjs', 'react', 'vue', 'svelte', 'astro', 'remix', 'nuxt',
        'shadcn', 'radix', 'daisyui', 'tailwind', 'headless ui', 'component library',
        '元件庫', '前端框架', 'ui kit', 'design tokens',
    ],
    '設計系統與字體': [
        'design system', 'typography', 'webfont', 'web font', 'font subset',
        'variable font', 'font loading', '字體', '字型', '設計系統', 'color palette',
        '配色',
    ],
    '動效': [
        'gsap', 'framer motion', 'motion one', 'lottie', 'scroll animation',
        'view transition', 'animation library', '動效', '轉場', 'easing',
    ],
    '生圖與商品圖處理': [
        'image generation', 'text-to-image', 'diffusion', 'comfyui', 'flux',
        'background removal', 'rembg', 'upscale', 'image optimization',
        'image compression', 'sharp', 'squoosh', '去背', '生圖', '商品圖', '圖片壓縮',
    ],
    '電商後端與金流': [
        'stripe', 'paypal', 'checkout', 'shopping cart', 'medusa', 'saleor',
        'vendure', 'woocommerce', 'headless commerce', 'commerce api', 'payment',
        '金流', '購物車', '結帳', '訂單 api',
    ],
    '效能與 SEO': [
        'lighthouse', 'web vitals', 'core web vitals', 'pagespeed', 'sitemap',
        'structured data', 'schema.org', 'meta tags', 'accessibility', 'a11y',
        'bundle size', '效能檢測', '無障礙',
    ],
}

# 弱訊號：只有這些不足以構成候選，會被當成營運類或內容類擋掉。
WEAK = ['電商', 'ecommerce', 'e-commerce', 'commerce', 'shop', '網站', 'website']

# 負面訊號：這些是營運、內容、代理人基礎建設，不是建站工具。
NEGATIVE = [
    '選品', '客服', '投放', '社群', '發文', '物流', '比價', '爬蟲', '短影音',
    '影片', 'avatar', 'tiktok shop', 'context', 'session', 'memory', 'mcp',
    'agent skills', 'skill pack', 'boilerplate for agents', '記憶', '排程',
]


def die(msg):
    print('[FAIL] ' + msg)
    sys.exit(2)


def digest_repo():
    p = os.environ.get('DIGEST_REPO', '').strip().strip('"')
    if not p:
        die('沒有設定環境變數 DIGEST_REPO，不知道要去哪裡讀每日情報。'
            '這一關拒絕在沒有輸入的情況下產出空清單。')
    if not os.path.isdir(os.path.join(p, 'digests')):
        die('DIGEST_REPO 指到的位置沒有 digests 資料夾：' + p)
    return p


def run(cmd, cwd=None, timeout=120):
    """跑一個指令並保留退出碼。不用管線，不吞錯。"""
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, '', 'timeout'
    out = r.stdout.decode('utf-8', 'replace')
    err = r.stderr.decode('utf-8', 'replace')
    return r.returncode, out, err


def parse_digest(path):
    """一份情報拆成多個項目。以 GitHub 連結為錨點往回抓描述。"""
    text = io.open(path, encoding='utf-8', errors='replace').read()
    items = []
    buf = []
    for line in text.split('\n'):
        m = re.search(r'https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)', line)
        if m:
            name = m.group(2).rstrip('.,)')
            if name.endswith('.git'):
                name = name[:-4]
            slug = m.group(1) + '/' + name
            desc = '\n'.join(buf).strip()
            items.append({
                'slug': slug,
                'digest_file': os.path.basename(path),
                'digest_text': desc[:600],
            })
            buf = []
        else:
            if line.strip() == '':
                buf = []
            else:
                buf.append(line.strip())
    return items


def load_decisions(repo):
    """讀情報端的決策帳本，當背景資訊用。回傳 slug 小寫 -> 那一行。"""
    p = os.path.join(repo, 'DECISIONS.md')
    seen = {}
    if not os.path.isfile(p):
        return seen
    for line in io.open(p, encoding='utf-8', errors='replace'):
        m = re.search(r'([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)', line)
        if m and '|' in line:
            seen.setdefault(m.group(1).lower(), line.strip())
    return seen


def load_ledger():
    """讀這條產線自己的評估帳本，這才是本關的去重真相。"""
    p = os.path.join(HERE, 'LEDGER.jsonl')
    seen = {}
    if not os.path.isfile(p):
        return seen
    for line in io.open(p, encoding='utf-8', errors='replace'):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        seen[rec.get('slug', '').lower()] = rec
    return seen


def classify(text):
    """回傳命中的類別與命中的關鍵字。"""
    low = text.lower()
    hits = {}
    for cat, kws in CATEGORIES.items():
        got = [k for k in kws if k in low]
        if got:
            hits[cat] = got
    return hits


def gh_meta(slug):
    """查專案的真實狀態。查不到就回 None，絕不猜。"""
    rc, out, err = run(['gh', 'api', 'repos/' + slug,
                        '--jq', '{pushed_at,archived,stargazers_count,description,'
                                'license:(.license.spdx_id // "NONE")}'], timeout=60)
    if rc != 0:
        return None
    try:
        return json.loads(out.strip())
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=7)
    ap.add_argument('--no-pull', action='store_true')
    ap.add_argument('--stale-days', type=int, default=180)
    args = ap.parse_args()

    repo = digest_repo()
    if not args.no_pull:
        rc, out, err = run(['git', '-C', repo, 'pull', '--ff-only'], timeout=180)
        if rc != 0:
            print('[WARN] 情報 repo 更新失敗，改用本機既有內容。原因：' +
                  (err.strip() or out.strip())[:200])

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    files = []
    for f in sorted(os.listdir(os.path.join(repo, 'digests'))):
        m = re.search(r'(\d{4})-(\d{2})-(\d{2})', f)
        if not m:
            continue
        d = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
        if d >= cutoff:
            files.append(os.path.join(repo, 'digests', f))
    if not files:
        die('最近 %d 天沒有任何情報檔可讀。' % args.days)

    raw = []
    for f in files:
        raw.extend(parse_digest(f))

    # 同一個項目在多份情報重複出現時只留最新那筆
    dedup = {}
    for it in raw:
        dedup[it['slug'].lower()] = it
    items = list(dedup.values())

    decisions = load_decisions(repo)
    ledger = load_ledger()
    results = []
    for it in items:
        slug = it['slug']
        rec = dict(it)
        prior = decisions.get(slug.lower())
        rec['prior_decision'] = prior

        if slug.lower() in ledger:
            old = ledger[slug.lower()]
            rec['status'] = 'OUT_已評估'
            rec['reason'] = '本產線已於 %s 評估過，結論 %s。' % (
                old.get('date', '？'), old.get('verdict', '？'))
            results.append(rec)
            continue

        if prior and '【已裝/已接】' in prior:
            rec['status'] = 'OUT_已決定'
            rec['reason'] = '情報端已標記採用，沒有東西可以再決定：' + prior[:120]
            results.append(rec)
            continue

        if prior and 'MCP' in prior:
            rec['status'] = 'OUT_碰紅線'
            rec['reason'] = '牽涉 MCP 設定變更，任何情況都不碰：' + prior[:120]
            results.append(rec)
            continue

        meta = gh_meta(slug)
        if meta is None:
            rec['status'] = 'UNKNOWN'
            rec['reason'] = '查不到專案資料，可能已刪除或改名。狀態不明，不進候選也不判否決。'
            results.append(rec)
            continue
        rec['stars'] = meta.get('stargazers_count')
        rec['pushed_at'] = meta.get('pushed_at')
        rec['license'] = meta.get('license')
        rec['gh_description'] = meta.get('description') or ''

        # 分類只看專案自己說的話（名稱與 GitHub 描述）。
        # 情報稿裡的「給你」是我們自己寫的推薦語，裡面本來就充滿我們的技術棧名詞，
        # 拿它來分類會讓一堆不相干的東西誤判成建站工具。實測過：45 天窗口裡
        # 有 6 個項目是這樣誤判進來的。情報稿只留著給人看，不參與判斷。
        text = slug + ' ' + rec['gh_description']
        hits = classify(text)
        neg = [n for n in NEGATIVE if n in (text + ' ' + it['digest_text']).lower()]
        rec['categories'] = hits
        rec['negative_hits'] = neg

        if not hits:
            rec['status'] = 'OUT_不相關'
            weak = [w for w in WEAK if w in text.lower()]
            rec['reason'] = ('沒有命中六類建站相關訊號' +
                             ('，只有弱訊號 ' + '、'.join(weak) if weak else ''))
            results.append(rec)
            continue

        if meta.get('archived'):
            rec['status'] = 'OUT_已封存'
            rec['reason'] = '專案已被作者封存，不採用。'
            results.append(rec)
            continue

        pushed = meta.get('pushed_at')
        if pushed:
            dt = datetime.strptime(pushed, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - dt).days
            rec['days_since_push'] = age
            if age > args.stale_days:
                rec['status'] = 'OUT_停止維護'
                rec['reason'] = '最後推送在 %d 天前，超過 %d 天上限，不採用（星數不列入考量）。' % (
                    age, args.stale_days)
                results.append(rec)
                continue
        else:
            rec['status'] = 'UNKNOWN'
            rec['reason'] = '查不到最後推送時間，活躍度不明。'
            results.append(rec)
            continue

        rec['status'] = 'CANDIDATE'
        rec['reason'] = '命中 ' + '、'.join(hits.keys()) + '，且 %d 天內仍有推送。' % age
        if neg:
            rec['reason'] += '注意：同時帶有營運類訊號 ' + '、'.join(neg[:3]) + '，第二關要看清楚它到底改到建站的哪一步。'
        results.append(rec)

    order = {'CANDIDATE': 0, 'UNKNOWN': 1, 'OUT_不相關': 2, 'OUT_停止維護': 3,
             'OUT_已封存': 4, 'OUT_已決定': 5, 'OUT_已評估': 6, 'OUT_碰紅線': 7}
    results.sort(key=lambda r: (order.get(r['status'], 9), r['slug']))

    if not os.path.isdir(QUEUE_DIR):
        os.makedirs(QUEUE_DIR)
    payload = {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'window_days': args.days,
        'digest_files': [os.path.basename(f) for f in files],
        'stale_days': args.stale_days,
        'items': results,
    }
    tmp = os.path.join(QUEUE_DIR, 'pending.json.tmp')
    io.open(tmp, 'w', encoding='utf-8').write(
        json.dumps(payload, ensure_ascii=False, indent=2))
    os.replace(tmp, os.path.join(QUEUE_DIR, 'pending.json'))

    counts = {}
    for r in results:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    print('== 篩選結果（來源 %d 份情報，%d 個項目）==' % (len(files), len(results)))
    for k in sorted(counts, key=lambda x: order.get(x, 9)):
        print('  %-14s %d' % (k, counts[k]))
    print('')
    for r in results:
        if r['status'] in ('CANDIDATE', 'UNKNOWN'):
            print('  [%s] %s' % (r['status'], r['slug']))
            print('      ' + r['reason'])
    print('')
    print('候選清單寫進 queue/pending.json。第二關必須逐個實測，沒實測過的一律不准採用。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
