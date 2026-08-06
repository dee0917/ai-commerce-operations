#!/usr/bin/env python3
"""
validate_live_flow.py — Phase 5.10 真連線驗證腳本

補上 validate_mock_flow.py 驗不到的那一半。那支驗的是假資料模式，
它從頭到尾沒有對真的後端發過一個請求，所以連線壞掉的站也能全綠通過。

這支驗兩件事：

  檢查一：金鑰有沒有被編譯進前端產物
      凡是 VITE_ 開頭的變數都會被編譯進瀏覽器程式碼。若把商店的 Consumer Key
      放進去，等於把讀寫全權金鑰公開發佈。掃 dist/ 全部檔案內容。

  檢查二：畫面上的商品是不是真的來自後端
      不能只看「有沒有報錯」。讀取失敗時前端會靜默退回假資料，畫面看起來完全正常。
      做法是在後端把某個商品改名成一組隨機碼（canary），再確認那組碼真的出現在
      畫面上，然後改回原名。改名成功而畫面沒出現，就是沒接通。

兩個檢查都自帶偵測能力測試：先造出「應該要被抓到」的東西，確認抓得到才算數。

Usage:
  python scripts/validate_live_flow.py <project_path> --site-url http://localhost:5174
  python scripts/validate_live_flow.py <project_path> --secrets-only
"""

import argparse
import io
import os
import re
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

# ─── 檢查一：金鑰特徵 ────────────────────────────────────────────────

SECRET_RULES = [
    ('woo_consumer_key',    re.compile(r'ck_[A-Za-z0-9]{20,}')),
    ('woo_consumer_secret', re.compile(r'cs_[A-Za-z0-9]{20,}')),
    ('consumer_key_param',  re.compile(r'consumer_key')),
    ('consumer_secret_param', re.compile(r'consumer_secret')),
    ('openai_like',         re.compile(r'sk-[A-Za-z0-9_\-]{20,}')),
    ('github_token',        re.compile(r'ghp_[A-Za-z0-9]{20,}')),
    ('aws_access_key',      re.compile(r'AKIA[0-9A-Z]{16}')),
    ('private_key_block',   re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY')),
]

# 這些副檔名不是文字，掃了只會拖慢速度
BINARY_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.svg',
              '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.webm', '.avif'}


def scan_tree(root: Path):
    """回傳 [(rule_name, 相對路徑, 命中的片段)]。"""
    hits = []
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() in BINARY_EXT:
            continue
        try:
            text = io.open(path, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        for name, pattern in SECRET_RULES:
            m = pattern.search(text)
            if m:
                hits.append((name, str(path.relative_to(root)), m.group(0)[:40]))
    return hits


def selftest_scanner() -> bool:
    """種出每一種該被抓到的東西，證明掃描器真的會叫。種的東西全部在暫存區。"""
    print('  [自我測試] 造出每一種該被抓到的樣本…')
    tmp = Path(tempfile.mkdtemp(prefix='livecheck_'))
    ok = True
    try:
        samples = {
            'woo_consumer_key':      'const k="ck_' + 'a1b2c3d4' * 5 + '";',
            'woo_consumer_secret':   'const s="cs_' + 'f9e8d7c6' * 5 + '";',
            'consumer_key_param':    'url.set("consumer_key", k);',
            'consumer_secret_param': 'url.set("consumer_secret", s);',
            'openai_like':           'const o="sk-' + 'A1b2C3d4' * 4 + '";',
            'github_token':          'const g="ghp_' + 'Z9y8X7w6' * 3 + '";',
            'aws_access_key':        'const a="AKIA' + 'ABCD1234EFGH5678' + '";',
            'private_key_block':     '-----BEGIN RSA PRIVATE KEY-----',
        }
        for name, content in samples.items():
            io.open(tmp / (name + '.js'), 'w', encoding='utf-8').write(content)
        io.open(tmp / 'clean.js', 'w', encoding='utf-8').write(
            'export const price = (v) => v.toFixed(2); // nothing sensitive here\n')

        found = scan_tree(tmp)
        for name, _ in SECRET_RULES:
            caught = [h for h in found if h[0] == name and h[1].startswith(name)]
            print('    %-22s %s' % (name, 'PASS' if caught else 'FAIL'))
            if not caught:
                ok = False

        false_pos = [h for h in found if h[1] == 'clean.js']
        print('    %-22s %s' % ('clean 對照組',
                                'PASS' if not false_pos else 'FAIL 誤報 %d' % len(false_pos)))
        if false_pos:
            ok = False
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        print('  [自我測試] 樣本已清除：%s' % (not tmp.exists()))
    return ok


def check_secrets(project: Path) -> bool:
    print('\n檢查一：金鑰有沒有被編譯進前端產物')
    dist = project / 'dist'
    if not dist.is_dir():
        print('  FAIL  找不到 dist/，請先執行 npm run build')
        return False

    hits = scan_tree(dist)
    if hits:
        print('  FAIL  在建置產物裡找到 %d 處金鑰特徵：' % len(hits))
        for name, rel, frag in hits[:20]:
            print('        %-22s %s  →  %s' % (name, rel, frag))
        print('        這些內容會被公開發佈給每一個訪客。')
        return False

    print('  PASS  dist/ 內沒有任何金鑰特徵')
    return True


# ─── 檢查二：真連線（canary） ────────────────────────────────────────

def load_woo_client(explicit: str = None):
    """找共用的 API client，不重造 OAuth 簽章。"""
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    here = Path(__file__).resolve().parent
    candidates += [
        here.parent / 'backend' / 'bin',
        here.parent.parent / 'production-line' / 'backend' / 'bin',
        here.parent.parent / 'backend' / 'bin',
    ]
    for c in candidates:
        if (c / 'woo_client.py').is_file():
            sys.path.insert(0, str(c))
            import woo_client
            return woo_client, c
    return None, None


def check_live(project: Path, site_url: str, env_file: str, client_path: str) -> bool:
    print('\n檢查二：畫面上的商品是不是真的來自後端')

    mod, found_at = load_woo_client(client_path)
    if mod is None:
        print('  FAIL  找不到 woo_client.py，無法改後端資料做 canary 驗證。')
        print('        用 --woo-client-path 指定它的位置，或用 --secrets-only 只跑檢查一。')
        return False
    print('  使用 API client：%s' % found_at)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('  FAIL  沒有安裝 playwright，無法確認畫面實際渲染了什麼。')
        return False

    mod.load_env(env_file)
    try:
        client = mod.WooClient()
    except SystemExit as exc:
        print('  FAIL  後端憑證不完整：%s' % exc)
        return False

    rows = client.get('products', per_page=1, orderby='date', order='desc')
    if not rows:
        print('  FAIL  後端一個商品都沒有，無法驗證。')
        return False

    target = rows[0]
    original_name = target['name']
    canary = 'LIVECHECK-%s' % uuid.uuid4().hex[:10].upper()
    marked_name = '%s %s' % (original_name, canary)

    print('  改名的商品：id=%s  原名=%r' % (target['id'], original_name))
    print('  canary：%s' % canary)

    ok = False
    restored = False
    try:
        client.request('PUT', 'products/%s' % target['id'], payload={'name': marked_name})

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_context(viewport={'width': 1280, 'height': 900}).new_page()
            api_calls = []
            page.on('response', lambda r: api_calls.append((r.status, r.url))
                    if 'wp-json' in r.url else None)

            page.goto(site_url, wait_until='networkidle')
            page.wait_for_timeout(3000)
            body_marked = page.inner_text('body')
            present = canary in body_marked

            print('  後端請求：%s' % (api_calls or '（完全沒有發出任何後端請求）'))
            print('  canary 出現在畫面上：%s' % present)

            # 還原，然後做反向對照：canary 必須消失。
            client.request('PUT', 'products/%s' % target['id'],
                           payload={'name': original_name})
            restored = True

            page.reload(wait_until='networkidle')
            page.wait_for_timeout(3000)
            gone = canary not in page.inner_text('body')
            print('  還原後 canary 消失：%s' % gone)

            browser.close()

        if present and gone:
            print('  PASS  畫面內容確實跟著後端一起變，這條線是通的')
            ok = True
        elif not present:
            print('  FAIL  後端改名成功，但畫面沒出現 canary。')
            if not api_calls:
                print('        前端完全沒有呼叫後端，等於在用寫死的假資料。')
            else:
                print('        前端有呼叫後端但畫面沒更新，很可能讀取失敗後靜默退回假資料。')
        else:
            print('  FAIL  還原之後 canary 還在，這個檢查沒有偵測能力，結果不算數。')
    finally:
        if not restored:
            try:
                client.request('PUT', 'products/%s' % target['id'],
                               payload={'name': original_name})
                print('  商品名稱已還原（例外處理路徑）')
            except Exception as exc:
                print('  ⚠️  還原失敗，請手動把商品 %s 的名稱改回 %r：%s'
                      % (target['id'], original_name, exc))

    return ok


def main():
    parser = argparse.ArgumentParser(description='驗證真連線與前端金鑰外洩')
    parser.add_argument('project_path')
    parser.add_argument('--site-url', default='http://localhost:5174',
                        help='已經跑起來的站台網址（dev server 或 dist 靜態伺服器）')
    parser.add_argument('--env-file', default='',
                        help='含後端憑證的 env 檔；預設找 production-line/backend/.env.backend')
    parser.add_argument('--woo-client-path', default='')
    parser.add_argument('--secrets-only', action='store_true',
                        help='只跑檢查一，不需要後端')
    args = parser.parse_args()

    project = Path(args.project_path)
    if not project.is_dir():
        sys.exit('找不到專案目錄：%s' % project)

    env_file = args.env_file
    if not env_file:
        guess = Path(__file__).resolve().parent.parent / 'backend' / '.env.backend'
        env_file = str(guess)

    print('=' * 62)
    print('  Phase 5.10 真連線驗證')
    print('  專案：%s' % project)
    print('=' * 62)

    print('\n偵測能力自我測試（不通過的話下面的結果不算數）')
    if not selftest_scanner():
        print('\n中止：掃描器沒有通過自我測試，本次結果一律不算數。')
        return 2

    results = {'secrets': check_secrets(project)}
    if args.secrets_only:
        print('\n（--secrets-only：跳過檢查二）')
    else:
        results['live'] = check_live(project, args.site_url, env_file, args.woo_client_path)

    print('\n' + '=' * 62)
    for name, passed in results.items():
        print('  %-10s %s' % (name, 'PASS' if passed else 'FAIL'))
    all_ok = all(results.values())
    print('  結論：%s' % ('READY' if all_ok else 'NOT-READY，不得交付'))
    print('=' * 62)
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
