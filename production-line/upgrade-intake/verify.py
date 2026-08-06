# -*- coding: utf-8 -*-
"""
第二關：實測驗證。這一關是整條流程唯一有權力說「可以採用」的地方。

規矩只有一條：**拿它對這條產線做一次實際的事，看結果有沒有發生。**
下面這些一律不算通過，程式碼層面直接擋：
  - 安裝成功（recipe 沒有 build 也沒有產出物斷言，直接判定 recipe 無效）
  - 能 import（沒有畫面斷言的 recipe 一樣無效）
  - 伺服器回 200（判斷用的是實際畫得出來的元素數與文字量，不是回應碼）

三種結論，不是兩種：
  PASS          做出來的事真的發生了，證據齊全
  FAIL          做出來的事沒有發生，或中途出錯
  INCONCLUSIVE  逾時、外部服務不可用、或過程中出現退回退路的跡象
                這一種**不准當成通過**，也不記成失敗，要重跑或改條件

自我驗證：每次跑之前先做一次能力測試，用一個空白頁與一個正常頁對照，
證明這支檢查器真的分得出「畫得出來」與「畫不出來」。分不出來就整份結果作廢。

用法：
    python verify.py --recipe recipes/facebook__astryx.json
    python verify.py --selftest-only
"""
import argparse
import io
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
VERIF_DIR = os.path.join(HERE, 'verifications')
QUEUE_DIR = os.path.join(HERE, 'queue')

# 出現這些字樣代表過程中有東西悄悄走了退路，或外部服務根本沒回應。
# 這時就算畫面看起來對，也不准判 PASS。
# 來源：PITFALLS「外部服務壞掉時安靜退回退路，然後回報成功」。
FALLBACK_MARKERS = [
    'falling back to', 'fell back to', 'using placeholder', 'placeholder image',
    'mock mode', 'offline mode', 'service unavailable', 'ECONNREFUSED',
    'ETIMEDOUT', 'ENOTFOUND', '退回', '改用預設',
]


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sanitize(text):
    """把本機路徑洗掉再寫進 repo。證據要能公開，不能夾帶使用者的目錄結構。"""
    if not isinstance(text, str):
        return text
    t = text
    for root in [tempfile.gettempdir(), os.path.expanduser('~')]:
        for form in [root, root.replace('\\', '/'), root.replace('\\', '\\\\')]:
            t = t.replace(form, '<PATH>')
    t = re.sub(r'[A-Za-z]:[\\/](?:[^\s"\'<>|]+[\\/])*[^\s"\'<>|]*', '<PATH>', t)
    return t


def resolve(cmd):
    """Windows 上 npm 與 npx 是 .cmd，直接丟名字給 subprocess 會找不到。
    見 PITFALLS「Windows 上找不到 npm」。"""
    out = list(cmd)
    found = shutil.which(out[0])
    if found:
        out[0] = found
    return out


def run(cmd, cwd, timeout, log):
    cmd = resolve(cmd)
    started = time.time()
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        log.append({'cmd': cmd, 'rc': 124, 'seconds': timeout,
                    'stdout': '', 'stderr': '逾時 %d 秒後仍未結束' % timeout})
        return 124, '', 'timeout'
    except FileNotFoundError as e:
        log.append({'cmd': cmd, 'rc': 127, 'seconds': 0, 'stdout': '', 'stderr': str(e)})
        return 127, '', str(e)
    out = r.stdout.decode('utf-8', 'replace')
    err = r.stderr.decode('utf-8', 'replace')
    log.append({'cmd': cmd, 'rc': r.returncode, 'seconds': round(time.time() - started, 1),
                'stdout': out[-4000:], 'stderr': err[-4000:]})
    return r.returncode, out, err


def free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


def node_env():
    """render_check.mjs 需要 playwright，但它住的資料夾沒有 node_modules。
    把全域 node_modules 指給它，找不到就照原樣跑，讓它自己報錯，不假裝沒事。"""
    env = dict(os.environ)
    try:
        r = subprocess.run(resolve(['npm', 'root', '-g']), capture_output=True, timeout=60)
        root = r.stdout.decode('utf-8', 'replace').strip()
        if r.returncode == 0 and root:
            env['NODE_PATH'] = root + os.pathsep + env.get('NODE_PATH', '')
    except Exception:
        pass
    return env


def render(base_url, route, shot, must_texts):
    cmd = resolve(['node', os.path.join(HERE, 'render_check.mjs'),
                   base_url, route, shot] + list(must_texts))
    try:
        r = subprocess.run(cmd, cwd=HERE, capture_output=True, timeout=180, env=node_env())
    except subprocess.TimeoutExpired:
        return {'ok': False, 'error': '瀏覽器檢查逾時', 'timeout': True}
    txt = r.stdout.decode('utf-8', 'replace').strip()
    try:
        return json.loads(txt[txt.index('{'):])
    except Exception:
        return {'ok': False,
                'error': '檢查器沒有吐出可解析的結果：' +
                         (txt[-300:] or r.stderr.decode('utf-8', 'replace')[-300:])}


def wait_port(p, port, tries):
    for _ in range(tries):
        try:
            s = socket.create_connection(('127.0.0.1', port), timeout=0.5)
            s.close()
            return p
        except Exception:
            if p.poll() is not None:
                return None
            time.sleep(0.5)
    p.kill()
    return None


def serve_cmd(cmd, cwd, port, ready_timeout=120):
    """給 SSR 專案用：跑它自己的伺服器，不是丟靜態檔。
    起不來就回 None，讓上層判 INCONCLUSIVE，不會拿舊畫面充數。"""
    cmd = resolve([c.replace('{port}', str(port)) for c in cmd])
    env = dict(os.environ)
    env['PORT'] = str(port)
    p = subprocess.Popen(cmd, cwd=cwd, env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return wait_port(p, port, ready_timeout * 2)


def serve(directory, port):
    cmd = resolve([sys.executable, '-m', 'http.server', str(port),
                   '--directory', directory, '--bind', '127.0.0.1'])
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        try:
            s = socket.create_connection(('127.0.0.1', port), timeout=0.5)
            s.close()
            return p
        except Exception:
            time.sleep(0.25)
    p.kill()
    return None


THRESHOLD_VISIBLE = 12
THRESHOLD_TEXT = 120


def selftest():
    """證明這支檢查器分得出畫得出來與畫不出來。分不出來的話結果不算數。"""
    tmp = tempfile.mkdtemp(prefix='intake_selftest_')
    empty = os.path.join(tmp, 'empty')
    full = os.path.join(tmp, 'full')
    os.makedirs(empty)
    os.makedirs(full)
    # 一定要寫 charset，否則瀏覽器會把 UTF-8 的中文解成亂碼，
    # 中文比對就會假性失敗。這是能力測試自己抓出來的第一個問題。
    head = '<!doctype html><html><head><meta charset="utf-8"></head>'
    io.open(os.path.join(empty, 'index.html'), 'w', encoding='utf-8').write(
        head + '<body></body></html>')
    rows = ''.join(
        '<div class="row"><h3>商品 %d</h3><p>這是一段足夠長的商品描述文字，用來確認頁面真的畫得出東西。</p>'
        '<span>NT$ %d</span><button>加入購物車</button></div>' % (i, 1000 + i)
        for i in range(1, 9))
    io.open(os.path.join(full, 'index.html'), 'w', encoding='utf-8').write(
        head + '<body><main><h1>正常頁</h1>' + rows + '</main></body></html>')

    result = {'at': now()}
    for name, d in (('empty', empty), ('full', full)):
        port = free_port()
        srv = serve(d, port)
        if not srv:
            shutil.rmtree(tmp, ignore_errors=True)
            return False, {'error': '本機伺服器起不來，能力測試無法進行'}
        try:
            r = render('http://127.0.0.1:%d' % port, '/', '-', ['加入購物車'])
        finally:
            srv.kill()
        result[name] = {'visible': r.get('visible'), 'bodyText': r.get('bodyText'),
                        'missingTexts': r.get('missingTexts'), 'error': r.get('error')}
    shutil.rmtree(tmp, ignore_errors=True)

    e, f = result.get('empty', {}), result.get('full', {})
    # 檢查器自己爆掉不算「抓到空白頁」。量不到就是量不到，不能當成偵測成功。
    catches_empty = (e.get('error') is None and
                     (e.get('visible') or 0) < THRESHOLD_VISIBLE and
                     (e.get('bodyText') or 0) < THRESHOLD_TEXT)
    passes_full = (f.get('visible') or 0) >= THRESHOLD_VISIBLE and \
                  (f.get('bodyText') or 0) >= THRESHOLD_TEXT and not f.get('missingTexts')
    ok = catches_empty and passes_full
    result['catches_empty_page'] = catches_empty
    result['passes_real_page'] = passes_full
    result['verdict'] = 'HARNESS_OK' if ok else 'HARNESS_BROKEN'
    if not os.path.isdir(QUEUE_DIR):
        os.makedirs(QUEUE_DIR)
    io.open(os.path.join(QUEUE_DIR, 'selftest.json'), 'w', encoding='utf-8').write(
        json.dumps(result, ensure_ascii=False, indent=2))
    return ok, result


def validate_recipe(rec):
    """擋掉「只安裝」「只 import」這種假驗證。"""
    problems = []
    if not rec.get('repo'):
        problems.append('缺 repo')
    if not rec.get('replaces_or_adds'):
        problems.append('缺 replaces_or_adds：沒有寫清楚它要替換或補上產線的哪一項，'
                        '這種驗證做完也不知道要不要採用')
    exp = rec.get('expect') or {}
    has_render = bool(exp.get('routes'))
    has_artifacts = bool(exp.get('artifacts'))
    if not (rec.get('build') or has_artifacts):
        problems.append('既沒有 build 也沒有產出物斷言：安裝成功不算驗證')
    if not (has_render or has_artifacts):
        problems.append('沒有任何結果斷言：能 import 不算驗證')
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--recipe')
    ap.add_argument('--selftest-only', action='store_true')
    ap.add_argument('--skip-selftest', action='store_true')
    ap.add_argument('--keep-sandbox', action='store_true')
    args = ap.parse_args()

    if not args.skip_selftest or args.selftest_only:
        ok, st = selftest()
        print('== 檢查器能力測試 ==')
        print('  空白頁抓得出來：%s' % ('PASS' if st.get('catches_empty_page') else 'FAIL'))
        print('  正常頁不誤殺：  %s' % ('PASS' if st.get('passes_real_page') else 'FAIL'))
        if not ok:
            print('!! 檢查器本身沒有偵測能力，任何驗證結果都不算數。')
            print(json.dumps(st, ensure_ascii=False, indent=2))
            return 2
        if args.selftest_only:
            return 0

    if not args.recipe:
        print('[FAIL] 沒有指定 --recipe')
        return 2
    rec_path = args.recipe if os.path.isabs(args.recipe) else os.path.join(HERE, args.recipe)
    rec = json.load(io.open(rec_path, encoding='utf-8'))

    problems = validate_recipe(rec)
    if problems:
        print('== 驗證腳本無效，拒絕執行 ==')
        for p in problems:
            print('  - ' + p)
        return 2

    slug = rec['repo']
    safe = slug.replace('/', '__')
    outdir = os.path.join(VERIF_DIR, safe)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    sandbox = os.path.join(tempfile.gettempdir(), 'ecom-upgrade-intake', safe)
    if os.path.isdir(sandbox):
        shutil.rmtree(sandbox, ignore_errors=True)
    os.makedirs(sandbox)

    log = []
    report = {
        'repo': slug,
        'type': rec.get('type'),
        'replaces_or_adds': rec['replaces_or_adds'],
        'started_at': now(),
        'verdict': None,
        'why': [],
        'measurements': {},
    }

    # 準備沙箱：樣板 + recipe 自帶的區塊原始碼
    tpl = rec.get('template', 'vite-react')
    tpl_dir = os.path.join(HERE, 'templates', tpl)
    if not os.path.isdir(tpl_dir):
        print('[FAIL] 找不到樣板 ' + tpl)
        return 2
    shutil.copytree(tpl_dir, sandbox, dirs_exist_ok=True)
    for dest, src in (rec.get('files') or {}).items():
        s = os.path.join(HERE, src)
        d = os.path.join(sandbox, dest)
        if not os.path.isdir(os.path.dirname(d)):
            os.makedirs(os.path.dirname(d))
        shutil.copyfile(s, d)

    verdict = None
    # 步驟
    for step in rec.get('steps', []):
        print('  -> ' + step['name'])
        rc, out, err = run(step['cmd'], os.path.join(sandbox, step.get('cwd', '.')),
                           step.get('timeout', 600), log)
        if rc == 124:
            verdict = ('INCONCLUSIVE', '步驟「%s」逾時，狀態不明。不判通過也不判失敗。' % step['name'])
            break
        if rc != 0:
            verdict = ('FAIL', '步驟「%s」退出碼 %d：%s' % (step['name'], rc, (err or out)[-300:]))
            break

    # 建置
    if verdict is None and rec.get('build'):
        print('  -> 建置')
        rc, out, err = run(rec['build']['cmd'],
                           os.path.join(sandbox, rec['build'].get('cwd', '.')),
                           rec['build'].get('timeout', 900), log)
        if rc == 124:
            verdict = ('INCONCLUSIVE', '建置逾時，狀態不明。')
        elif rc != 0:
            verdict = ('FAIL', '建置失敗，退出碼 %d：%s' % (rc, (err or out)[-400:]))

    # 畫面
    exp = rec.get('expect') or {}
    if verdict is None and exp.get('routes'):
        sv = rec.get('serve', {})
        port = free_port()
        srv = None
        if sv.get('cmd'):
            srv = serve_cmd(sv['cmd'], os.path.join(sandbox, sv.get('cwd', '.')), port,
                            sv.get('ready_timeout', 120))
            if not srv:
                verdict = ('INCONCLUSIVE', '專案自己的伺服器起不來，畫面沒看到，狀態不明。')
        else:
            dist = os.path.join(sandbox, sv.get('dir', 'dist'))
            if not os.path.isdir(dist):
                verdict = ('FAIL', '建置說成功了，但產出目錄不存在：' + sv.get('dir', 'dist'))
            else:
                srv = serve(dist, port)
                if not srv:
                    verdict = ('INCONCLUSIVE', '本機伺服器起不來，畫面沒看到，狀態不明。')
        if verdict is None and srv:
            try:
                for route in exp['routes']:
                    shot = os.path.join(outdir, 'screenshot%s.png' %
                                        (route.rstrip('/').replace('/', '_') or '_home'))
                    r = render('http://127.0.0.1:%d' % port, route, shot,
                               exp.get('must_contain_text', []))
                    report['measurements'][route] = {
                        k: r.get(k) for k in
                        ('bodyText', 'visible', 'inView', 'hidden', 'missingTexts',
                         'consoleErrors', 'pageErrors', 'error')
                    }
                    if r.get('timeout'):
                        verdict = ('INCONCLUSIVE', '瀏覽器檢查逾時，畫面狀態不明。')
                        break
                    if not r.get('ok'):
                        verdict = ('FAIL', '頁面打不開或檢查失敗：' + str(r.get('error'))[:300])
                        break
                    if (r.get('visible') or 0) < exp.get('min_visible_elements', THRESHOLD_VISIBLE):
                        verdict = ('FAIL', '%s 實際畫得出來的元素只有 %s 個，低於門檻 %s。'
                                           '頁面打得開不等於畫得出來。' %
                                   (route, r.get('visible'),
                                    exp.get('min_visible_elements', THRESHOLD_VISIBLE)))
                        break
                    if (r.get('bodyText') or 0) < exp.get('min_body_text', THRESHOLD_TEXT):
                        verdict = ('FAIL', '%s 看得見的文字只有 %s 字，低於門檻 %s。' %
                                   (route, r.get('bodyText'),
                                    exp.get('min_body_text', THRESHOLD_TEXT)))
                        break
                    if r.get('missingTexts'):
                        verdict = ('FAIL', '%s 少了應該出現的內容：%s' %
                                   (route, '、'.join(r['missingTexts'])))
                        break
                    if exp.get('no_console_error', True) and (r.get('pageErrors') or
                                                             r.get('consoleErrors')):
                        verdict = ('FAIL', '%s 主控台有錯誤：%s' %
                                   (route, (r.get('pageErrors') or r.get('consoleErrors'))[0]))
                        break
                    sz = os.path.getsize(shot) if os.path.isfile(shot) else 0
                    report['measurements'][route]['screenshot_bytes'] = sz
                    if sz < exp.get('screenshot_min_bytes', 8000):
                        verdict = ('FAIL', '%s 截不到有內容的圖（%d 位元組），沒有證據就不算通過。' %
                                   (route, sz))
                        break
            finally:
                srv.kill()

    # 產出物斷言（生圖與圖片處理類用這個）
    if verdict is None and exp.get('artifacts'):
        for a in exp['artifacts']:
            p = os.path.join(sandbox, a['path'])
            if not os.path.isfile(p):
                verdict = ('FAIL', '應該產生的檔案不存在：' + a['path'])
                break
            size = os.path.getsize(p)
            report['measurements'][a['path']] = {'bytes': size}
            if size < a.get('min_bytes', 1):
                verdict = ('FAIL', '%s 只有 %d 位元組，等於沒產出。' % (a['path'], size))
                break
            if a.get('must_differ_from'):
                src = os.path.join(sandbox, a['must_differ_from'])
                if os.path.isfile(src) and open(src, 'rb').read() == open(p, 'rb').read():
                    verdict = ('FAIL', '%s 跟輸入一模一樣，工具其實沒有動它。' % a['path'])
                    break

    # 退路偵測：整個過程的輸出掃一次
    all_out = '\n'.join((l.get('stdout', '') + '\n' + l.get('stderr', '')) for l in log)
    marks = []
    for line in all_out.split('\n'):
        for m in FALLBACK_MARKERS:
            if m.lower() in line.lower():
                marks.append(line.strip()[:200])
                break
    report['fallback_signals'] = [sanitize(m) for m in marks[:10]]

    if verdict is None:
        if marks:
            verdict = ('INCONCLUSIVE',
                       '畫面斷言都過了，但過程中出現退回退路或外部服務不可用的跡象，'
                       '這種情況不准判通過。第一條：' + sanitize(marks[0]))
        else:
            verdict = ('PASS', '建置退出碼 0，畫面實際畫得出來，指定內容都在，主控台無錯誤，截圖有內容。')

    report['verdict'] = verdict[0]
    report['why'] = [sanitize(verdict[1])]
    report['finished_at'] = now()
    report['log'] = [{'cmd': ' '.join(os.path.basename(c) if i == 0 else c
                                      for i, c in enumerate(l['cmd'])),
                      'rc': l['rc'], 'seconds': l.get('seconds'),
                      'tail': sanitize((l.get('stderr') or l.get('stdout') or '')[-600:])}
                     for l in log]

    io.open(os.path.join(outdir, 'report.json'), 'w', encoding='utf-8').write(
        json.dumps(report, ensure_ascii=False, indent=2))
    if not args.keep_sandbox:
        shutil.rmtree(sandbox, ignore_errors=True)

    print('')
    print('== %s：%s ==' % (slug, report['verdict']))
    print('   ' + report['why'][0])
    print('   證據寫在 verifications/%s/' % safe)
    return 0 if report['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
