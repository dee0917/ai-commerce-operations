#!/usr/bin/env python3
"""
design_history.py — 設計基因的「訂位式」登記（Phase 1.05 第 3、4、6 條）

為什麼要有這支：

  舊做法是「站建成之後才回寫 data/design-history.json」。讀取（挑基因）與
  回寫（登記基因）之間隔著整個建站流程，中間可能隔幾十分鐘。
  兩個站平行建置時，站二讀到的是站一還沒回寫的舊資料，防重複規則完全失效。
  2026-08-04 實測：站二鎖定設計基因的時間比站一完工早 188 秒，
  兩個站都選了 warm-paper 底＋襯線標題。

  新做法是訂位：**選定基因的那一刻就登記**，狀態先記成 in_progress，
  站交付後再 commit 成 completed，中途放棄就 abandon。
  檢查與登記在同一把鎖裡完成（reserve 這個動作本身是不可分割的），
  所以不論兩支流程間隔多久、甚至同時起跑，後到的那支一定看得到先到的那筆。

四種狀態：

  in_progress  已訂位、站還在做。**會擋住後面的人**（這正是重點）。
  completed    站已交付。會擋住後面的人。
  abandoned    中途放棄，明確退位。不擋人。
  過期          in_progress 超過 --stale-minutes（預設 120 分鐘）沒有下文，
               視為當機或中斷，自動不擋人，避免失敗的站永久佔位。

同時寫入怎麼處理：
  用 O_CREAT|O_EXCL 建鎖檔（這個動作在 Windows 與 POSIX 都是原子的），
  拿不到就退讓重試；鎖檔本身超過 LOCK_STALE_SECONDS 沒人動就視為前一支當掉、強制接手。
  寫檔一律先寫暫存檔再 os.replace，中途被砍不會留下半截或零位元組的歷史檔。

用法：

  # 一、開始設計前：看目前要避開什麼
  python scripts/design_history.py plan

  # 二、選定 DNA、底色、字體的當下（不是站做完之後）立刻訂位
  python scripts/design_history.py reserve \
      --brand "Postevand Supply" --category "Water" \
      --primary-dna DNA-44 --primary-family J \
      --bg-tone cool-white --display "Nimbus Sans" --body "Archivo" \
      --ui-framework shadcn/ui --project ./sites/postevand
  # → 印出 RESERVED id=9，違反去重規則時直接非零退出，不會寫進去

  # 三、站交付後
  python scripts/design_history.py commit --id 9 --maturity-score 14

  # 四、站做不下去了
  python scripts/design_history.py abandon --id 9 --reason "圖庫沒過驗收"
"""

import argparse
import io
import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_HISTORY = Path(__file__).resolve().parent.parent / 'data' / 'design-history.json'

BG_TONES = ('warm-paper', 'cool-white', 'dark', 'tinted')
BODY_FONT_AVOID = ('inter',)          # 2020-2023 SaaS 的預設臉，見 SKILL.md Phase 1.05
RECENT_WINDOW = 3                      # 去重看最近幾筆
RESERVE_STALE_MINUTES = 120            # in_progress 超過這個時間視為中斷
LOCK_STALE_SECONDS = 120               # 鎖檔超過這個時間視為前一支當掉
LOCK_WAIT_SECONDS = 30

# 2026-08-06 補完（uniqueness-guarantee.md）：訂位制擴充到 DNA 抽前過濾與結構指紋。
DEFAULT_DNA_INDEX = Path(__file__).resolve().parent.parent / 'data' / 'dna-index.json'
DEFAULT_STRUCT_HISTORY = Path(__file__).resolve().parent.parent / 'data' / 'structural-history.json'
PURPLE_HUE_BUCKETS = (240, 270)        # anti-patterns.md #5：#7C3AED/#6D28D9/#8B5CF6 落在這兩桶
POOL_FAMILY_WINDOW = 5                 # A1：抽前剔除看近 5 筆 primary family
KNOWN_SERIF_DISPLAY_CLUSTER = {        # SKILL.md 1.05 第 4 條點名的「襯線大標＋暖紙底」範式
    'fraunces', 'cormorant garamond', 'cormorant', 'dm serif display', 'playfair display',
}
STRUCT_WINDOW = 8                      # 1.07 第 3 步：結構指紋看近 8 站
EDIT_DISTANCE_MIN = 3                  # 區塊序列判準：編輯距離 < 3 視為太像
PAGE_JACCARD_MAX = 0.8                 # 分頁組合判準：Jaccard ≥ 0.8 視為太像


# ─── 檔案鎖與原子寫入 ────────────────────────────────────────────────

class LockTimeout(RuntimeError):
    pass


class FileLock:
    """用 O_CREAT|O_EXCL 建鎖檔。這個系統呼叫在 Windows 與 POSIX 上都是原子的。"""

    def __init__(self, target: Path, wait: float = LOCK_WAIT_SECONDS):
        self.path = Path(str(target) + '.lock')
        self.wait = wait
        self.fd = None

    def __enter__(self):
        deadline = time.time() + self.wait
        while True:
            try:
                self.fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
                os.write(self.fd, ('%d %s\n' % (os.getpid(), datetime.now().isoformat())).encode())
                return self
            except FileExistsError:
                if self._break_if_stale():
                    continue
                if time.time() > deadline:
                    raise LockTimeout('等不到 %s 的寫入鎖，前一支流程可能卡住了' % self.path.name)
                time.sleep(0.05)

    def _break_if_stale(self) -> bool:
        try:
            age = time.time() - self.path.stat().st_mtime
        except FileNotFoundError:
            return True
        if age > LOCK_STALE_SECONDS:
            try:
                os.unlink(str(self.path))
                return True
            except OSError:
                return False
        return False

    def __exit__(self, *exc):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        try:
            os.unlink(str(self.path))
        except OSError:
            pass
        return False


def load_history(path: Path) -> dict:
    if not path.is_file():
        return {'version': '3.2', 'generations': []}
    return json.loads(io.open(str(path), encoding='utf-8').read())


def save_history(path: Path, data: dict) -> None:
    """先寫暫存檔再換過去。**絕不用 w 模式直接開原檔**，中途失敗會留下零位元組的歷史檔。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix='.design-history-', suffix='.tmp')
    os.close(fd)
    io.open(tmp, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    os.replace(tmp, str(path))


# ─── 狀態判讀 ────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec='seconds')


def is_stale(entry: dict, stale_minutes: int) -> bool:
    """in_progress 放太久沒下文，視為中斷，不再擋人。"""
    if entry.get('status') != 'in_progress':
        return False
    stamp = entry.get('reserved_at')
    if not stamp:
        return True
    try:
        reserved = datetime.fromisoformat(stamp)
    except ValueError:
        return True
    if reserved.tzinfo is None:
        reserved = reserved.astimezone()
    return datetime.now().astimezone() - reserved > timedelta(minutes=stale_minutes)


def blocking_entries(data: dict, stale_minutes: int = RESERVE_STALE_MINUTES) -> list:
    """會擋住新站的紀錄：已完成的，加上還在進行中且沒過期的。舊資料沒有 status 一律當已完成。"""
    out = []
    for e in data.get('generations', []):
        status = e.get('status', 'completed')
        if status == 'abandoned':
            continue
        if is_stale(e, stale_minutes):
            continue
        out.append(e)
    return out


def recent_entries(data: dict, window: int = RECENT_WINDOW,
                   stale_minutes: int = RESERVE_STALE_MINUTES) -> list:
    return blocking_entries(data, stale_minutes)[-window:]


def infer_bg_tone(entry: dict) -> str:
    """舊筆沒有 bg_tone 時，退回用 colors.secondary 推斷（SKILL.md Phase 1.05 第 4 條）。"""
    tone = entry.get('bg_tone')
    if tone:
        return tone
    hexcode = (entry.get('colors') or {}).get('secondary', '')
    return classify_hex_tone(hexcode) if hexcode.startswith('#') else 'unknown'


def classify_hex_tone(hexcode: str) -> str:
    """把一個背景色歸到四類底色系。判準用色度（max-min）與色相，不用 HSL 飽和度：
    近白的暖色調（#f5f3ee）算出來的 HSL 飽和度高達 0.26，會被誤判成有彩色底。"""
    h = hexcode.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        return 'unknown'
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return 'unknown'
    mx, mn = max(r, g, b), min(r, g, b)
    lightness = (mx + mn) / 2.0
    chroma = mx - mn
    if lightness < 100:
        return 'dark'
    if chroma <= 4:
        return 'cool-white'
    if chroma > 20:
        return 'tinted'
    if mx == r:
        hue = 60.0 * (((g - b) / float(chroma)) % 6)
    elif mx == g:
        hue = 60.0 * (((b - r) / float(chroma)) + 2)
    else:
        hue = 60.0 * (((r - g) / float(chroma)) + 4)
    return 'warm-paper' if 15 <= hue <= 75 else 'cool-white'


def hue_bucket(hexcode: str):
    """12 桶 × 30°。灰階／無彩色（chroma=0）回傳 None，不落入任何色相桶——
    None 不代表「安全」，代表「這個判準判不出來」，呼叫端不可把 None 當成通過。"""
    h = (hexcode or '').strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        return None
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None
    mx, mn = max(r, g, b), min(r, g, b)
    chroma = mx - mn
    if chroma == 0:
        return None
    if mx == r:
        hue = 60.0 * (((g - b) / float(chroma)) % 6)
    elif mx == g:
        hue = 60.0 * (((b - r) / float(chroma)) + 2)
    else:
        hue = 60.0 * (((r - g) / float(chroma)) + 4)
    return int(hue // 30) * 30


# ─── DNA 抽前過濾（A1：先過濾池子再抽，不是抽完再檢查）───────────────

def load_dna_index(path: Path) -> list:
    if not path.is_file():
        return []
    return json.loads(io.open(str(path), encoding='utf-8').read()).get('dna', [])


def eligible_pool(data: dict, dna_list: list, stale_minutes: int = RESERVE_STALE_MINUTES) -> list:
    """三重交集剔除：近 5 筆 primary family、紫色 hue（不看歷史，永遠剔除)、
    近 3 筆 display 字體撞名或連續 2 次以上撞同一個「襯線大標」範式。
    回傳 dna-index.json 裡通過篩選的完整條目（不只 id），抽的人只准從這裡面抽。"""
    blocking = blocking_entries(data, stale_minutes)
    fam_window = blocking[-POOL_FAMILY_WINDOW:]
    font_window = blocking[-RECENT_WINDOW:]
    banned_fam = {e.get('primary_family') for e in fam_window if e.get('primary_family')}
    banned_display = {(e.get('fonts') or {}).get('display', '').strip().lower()
                       for e in font_window if (e.get('fonts') or {}).get('display')}
    serif_recent = sum(1 for e in font_window
                        if (e.get('fonts') or {}).get('display', '').strip().lower()
                        in KNOWN_SERIF_DISPLAY_CLUSTER)
    pool = []
    for d in dna_list:
        if d.get('family') in banned_fam:
            continue
        if d.get('purple_flag'):
            continue
        font = (d.get('display_font') or '').strip().lower()
        if font and font in banned_display:
            continue
        if serif_recent >= 2 and d.get('display_font_paradigm') == 'serif-display-warm':
            continue
        pool.append(d)
    return pool


def edit_distance(a: list, b: list) -> int:
    """經典 Levenshtein，元素是 token（字串）不是字元。給結構序列比對用。"""
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, y in enumerate(b, 1):
            cost = 0 if x == y else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[-1]


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    union = len(a | b)
    return (len(a & b) / union) if union else 1.0


# ─── 去重規則（唯一實作，reserve 與 plan 共用同一份判準）────────────

def dedup_violations(recents: list, bg_tone: str, display: str, body: str, primary_hex: str = None) -> list:
    msgs = []
    tones = [infer_bg_tone(e) for e in recents]
    if bg_tone and tones.count(bg_tone) >= 2:
        msgs.append('底色系 %s 在最近 %d 筆裡已經出現 %d 次，第 3 次就是視覺收斂'
                    % (bg_tone, len(recents), tones.count(bg_tone)))
    used_display = [((e.get('fonts') or {}).get('display') or '').strip().lower() for e in recents]
    if display and display.strip().lower() in used_display:
        msgs.append('display 字體 %s 與最近 %d 筆其中一筆相同' % (display, len(recents)))
    if body and body.strip().lower() in BODY_FONT_AVOID:
        msgs.append('body 字體 %s 在迴避清單裡，換成同類別的替代字體'
                    '（Archivo／Instrument Sans／Schibsted Grotesk）' % body)
    if primary_hex:
        bucket = hue_bucket(primary_hex)
        if bucket in PURPLE_HUE_BUCKETS:
            msgs.append('主色 %s 落在紫色色相桶（%d°），anti-patterns.md 第 5 條「紫色濫用」禁止紫色當主色，'
                        '除非品牌色板明確指定（用 --force 並把理由寫進 --note）' % (primary_hex, bucket))
        elif bucket is not None:
            recent_buckets = [hue_bucket((e.get('colors') or {}).get('primary', '')) for e in recents]
            if bucket in recent_buckets:
                msgs.append('主色 %s 的色相桶（%d°）與最近 %d 筆其中一筆相同，A3 判準是近 3 筆不得同桶'
                            % (primary_hex, bucket, len(recents)))
    return msgs


# ─── 指令 ────────────────────────────────────────────────────────────

def cmd_plan(args) -> int:
    path = Path(args.history)
    data = load_history(path)
    recents = recent_entries(data, args.window, args.stale_minutes)
    print('歷史檔：%s' % path)
    print('會擋住新站的紀錄共 %d 筆，去重看最近 %d 筆：'
          % (len(blocking_entries(data, args.stale_minutes)), len(recents)))
    for e in recents:
        print('  id=%-4s %-10s %-22s bg=%-11s display=%-22s body=%s'
              % (e.get('id'), e.get('status', 'completed'), e.get('brand', ''),
                 infer_bg_tone(e), (e.get('fonts') or {}).get('display', ''),
                 (e.get('fonts') or {}).get('body', '')))
    tones = [infer_bg_tone(e) for e in recents]
    banned_tone = sorted({t for t in tones if tones.count(t) >= 2 and t != 'unknown'})
    print('\n本次必須避開：')
    print('  底色系：%s' % ('、'.join(banned_tone) if banned_tone else '（無，四類都可選）'))
    print('  display 字體：%s'
          % ('、'.join(sorted({(e.get('fonts') or {}).get('display', '') for e in recents}
                             - {'', 'unknown'})) or '（無）'))
    print('  body 字體：%s' % '、'.join(BODY_FONT_AVOID))
    stale = [e for e in data.get('generations', []) if is_stale(e, args.stale_minutes)]
    if stale:
        print('\n過期的訂位（超過 %d 分鐘沒下文，已自動不擋人）：%s'
              % (args.stale_minutes, '、'.join('id=%s' % e.get('id') for e in stale)))
    if args.pool:
        dna_list = load_dna_index(Path(args.dna_index))
        if not dna_list:
            print('\n--pool 需要 %s，檔案不存在或是空的' % args.dna_index)
            return 3
        pool = eligible_pool(data, dna_list, args.stale_minutes)
        print('\n本次可抽池（family／紫色／字體三重交集剔除後）：%d / %d 個 DNA'
              % (len(pool), len(dna_list)))
        if not pool:
            print('池子空了——這是最近抽樣把 family／字體範式吃滿的結果，不是資料錯誤。')
            print('要嘛等歷史視窗滾動出去，要嘛 reserve 時加 --force 並在 --note 寫明理由。')
            return 3
        for d in pool:
            print('  %-8s %-24s family=%s  hex=%-9s font=%s'
                  % (d['id'], d.get('name', ''), d.get('family', ''),
                     d.get('primary_hex') or '-', d.get('display_font') or '-'))
        print('只准從上面這份清單抽；reserve 時傳的 --primary-dna 若不在池內會被拒絕（除非 --force）。')
    return 0


def cmd_reserve(args) -> int:
    """檢查與登記在同一把鎖裡完成，這是整支腳本存在的理由。"""
    path = Path(args.history)
    if args.bg_tone not in BG_TONES:
        print('底色系只能是這四類之一：%s' % '、'.join(BG_TONES))
        return 2
    import re as _re
    if not _re.match(r'^#[0-9a-fA-F]{6}$', args.primary_hex):
        print('--primary-hex 必須是 #rrggbb 格式（六碼），收到：%s' % args.primary_hex)
        return 2
    with FileLock(path):
        data = load_history(path)
        recents = recent_entries(data, args.window, args.stale_minutes)
        problems = dedup_violations(recents, args.bg_tone, args.display, args.body, args.primary_hex)
        dna_list = load_dna_index(Path(args.dna_index))
        dna_ids = {d['id'] for d in dna_list}
        if dna_list and not args.no_pool_check and args.primary_dna in dna_ids:
            pool_ids = {d['id'] for d in eligible_pool(data, dna_list, args.stale_minutes)}
            if args.primary_dna not in pool_ids:
                problems.append('%s 不在本次可抽池內（family／紫色／字體三重交集已剔除；跑 plan --pool 看清單）'
                                % args.primary_dna)
        if problems and not args.force:
            print('REJECTED  這組設計基因違反去重規則，沒有寫進歷史檔：')
            for m in problems:
                print('  ✗ %s' % m)
            print('請換一組再訂位。真的要沿用就加 --force，理由要寫進 --note。')
            return 1
        ids = [e.get('id', 0) for e in data.get('generations', [])]
        new_id = (max(ids) if ids else 0) + 1
        entry = {
            'id': new_id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'in_progress',
            'reserved_at': now_iso(),
            'completed_at': None,
            'brand': args.brand,
            'category': args.category,
            'project_path': args.project,
            'primary_dna': args.primary_dna,
            'primary_family': args.primary_family,
            'secondary_dna': args.secondary_dna,
            'secondary_family': args.secondary_family,
            'secondary_contribution': args.secondary_contribution,
            'ui_framework': args.ui_framework,
            'colors': {
                'primary': args.primary_hex,
                'secondary': args.color_secondary,
                'accent': args.color_accent,
            },
            'fonts': {'display': args.display, 'body': args.body},
            'bg_tone': args.bg_tone,
            'bg_hex': args.bg_hex,
            'signature_fx': args.signature_fx,
            'maturity_score': 0,
            'note': args.note,
        }
        data.setdefault('generations', []).append(entry)
        data['version'] = '3.2'
        save_history(path, data)
    if problems:
        print('⚠️  --force：明知違反去重規則仍然訂位，理由請寫在 note 裡')
    print('RESERVED  id=%d  %s  bg=%s  display=%s  body=%s'
          % (new_id, args.brand, args.bg_tone, args.display, args.body))
    print('站交付後跑：commit --id %d ；做不下去跑：abandon --id %d' % (new_id, new_id))
    return 0


def _update(path: Path, entry_id: int, mutate) -> int:
    with FileLock(path):
        data = load_history(path)
        for e in data.get('generations', []):
            if e.get('id') == entry_id:
                mutate(e)
                save_history(path, data)
                return 0
        print('找不到 id=%d 的紀錄' % entry_id)
        return 1


def cmd_commit(args) -> int:
    def mutate(e):
        e['status'] = 'completed'
        e['completed_at'] = now_iso()
        if args.maturity_score is not None:
            e['maturity_score'] = args.maturity_score
        for key, val in (('display', args.display), ('body', args.body)):
            if val:
                e.setdefault('fonts', {})[key] = val
        if args.bg_tone:
            e['bg_tone'] = args.bg_tone
        if args.bg_hex:
            e['bg_hex'] = args.bg_hex
        if args.note:
            e['note'] = args.note
    rc = _update(Path(args.history), args.id, mutate)
    if rc == 0:
        print('COMMITTED  id=%d 已標記為 completed' % args.id)
    return rc


def cmd_abandon(args) -> int:
    def mutate(e):
        e['status'] = 'abandoned'
        e['completed_at'] = now_iso()
        e['note'] = (args.reason or e.get('note') or '')
    rc = _update(Path(args.history), args.id, mutate)
    if rc == 0:
        print('ABANDONED  id=%d 已退位，不再擋住後面的站' % args.id)
    return rc


# ─── 自我測試（證明防重複與同時寫入真的有作用）──────────────────────

def cmd_selftest(args) -> int:
    print('自我測試：造出「該被擋下來」與「該被擋不住」的情況')
    tmp = Path(tempfile.mkdtemp(prefix='dhistory_'))
    ok = True
    no_index = tmp / 'no-such-dna-index.json'  # 不存在 → load_dna_index 回空 list → 不啟用 pool 檢查
    try:
        hist = tmp / 'design-history.json'
        save_history(hist, {'version': '3.2', 'generations': []})

        def run(argv, dna_index=None):
            return main(['--history', str(hist), '--dna-index', str(dna_index or no_index)] + argv)

        base = ['--brand', 'A', '--primary-dna', 'DNA-01', '--bg-tone', 'warm-paper',
                '--display', 'Fraunces', '--body', 'Archivo', '--primary-hex', '#a17c3e']
        rc = run(['reserve'] + base)
        print('  %-38s %s' % ('第一站訂位', 'PASS' if rc == 0 else 'FAIL'))
        ok &= rc == 0

        # 第二站在第一站還沒 commit 的時候就來，這正是 2026-08-04 撞臉的情境
        rc = run(['reserve', '--brand', 'B', '--primary-dna', 'DNA-02',
                  '--bg-tone', 'warm-paper', '--display', 'Fraunces', '--body', 'Archivo',
                  '--primary-hex', '#204060'])
        print('  %-38s %s' % ('未完工時第二站撞同一組基因', 'PASS' if rc == 1 else 'FAIL'))
        ok &= rc == 1

        rc = run(['reserve', '--brand', 'B', '--primary-dna', 'DNA-02',
                  '--bg-tone', 'cool-white', '--display', 'Nimbus Sans', '--body', 'Inter',
                  '--primary-hex', '#204060'])
        print('  %-38s %s' % ('body 用 Inter 被擋', 'PASS' if rc == 1 else 'FAIL'))
        ok &= rc == 1

        rc = run(['reserve', '--brand', 'B', '--primary-dna', 'DNA-02',
                  '--bg-tone', 'cool-white', '--display', 'Nimbus Sans', '--body', 'Archivo',
                  '--primary-hex', '#204060'])
        print('  %-38s %s' % ('換一組基因就過', 'PASS' if rc == 0 else 'FAIL'))
        ok &= rc == 0

        data = load_history(hist)
        n_blocking = len(blocking_entries(data))
        print('  %-38s %s' % ('未完工的訂位也算數', 'PASS' if n_blocking == 2 else 'FAIL'))
        ok &= n_blocking == 2

        run(['abandon', '--id', '1', '--reason', '測試'])
        rc = run(['reserve', '--brand', 'C', '--primary-dna', 'DNA-03',
                  '--bg-tone', 'warm-paper', '--display', 'Fraunces', '--body', 'Archivo',
                  '--primary-hex', '#a17c3e'])
        print('  %-38s %s' % ('abandon 之後不再佔位', 'PASS' if rc == 0 else 'FAIL'))
        ok &= rc == 0

        # ── 2026-08-06 補完：hue／purple／pool／verify／structural ──────

        # 紫色主色永遠被擋（anti-patterns.md #5），不看歷史
        rc = run(['reserve', '--brand', 'P', '--primary-dna', 'DNA-99', '--bg-tone', 'dark',
                  '--display', 'Unique1', '--body', 'Archivo', '--primary-hex', '#7C3AED'])
        print('  %-38s %s' % ('紫色主色被擋（anti-patterns #5）', 'PASS' if rc == 1 else 'FAIL'))
        ok &= rc == 1

        # 主色 hue 桶與前一筆相同 → 擋（#556677 與 #dd8844 特意同桶／不同桶，見下方 pool 測試複用邏輯）
        hist_hue = tmp / 'hue.json'
        save_history(hist_hue, {'version': '3.2', 'generations': []})
        rc1 = main(['--history', str(hist_hue), '--dna-index', str(no_index),
                    'reserve', '--brand', 'H1', '--primary-dna', 'DNA-01', '--bg-tone', 'warm-paper',
                    '--display', 'HueA', '--body', 'Archivo', '--primary-hex', '#223344'])
        rc2 = main(['--history', str(hist_hue), '--dna-index', str(no_index),
                    'reserve', '--brand', 'H2', '--primary-dna', 'DNA-02', '--bg-tone', 'cool-white',
                    '--display', 'HueB', '--body', 'Archivo', '--primary-hex', '#334455'])
        print('  %-38s %s' % ('主色色相桶與前筆同桶被擋', 'PASS' if rc1 == 0 and rc2 == 1 else 'FAIL'))
        ok &= (rc1 == 0 and rc2 == 1)

        # A1：抽前池過濾。假 dna-index 3 筆，2 筆 family A、1 筆 family B
        fake_index = tmp / 'fake-dna-index.json'
        io.open(str(fake_index), 'w', encoding='utf-8').write(json.dumps({'dna': [
            {'id': 'DNA-A1', 'name': 'FamA1', 'family': 'A', 'primary_hex': None,
             'purple_flag': False, 'display_font': None, 'display_font_paradigm': None},
            {'id': 'DNA-A2', 'name': 'FamA2', 'family': 'A', 'primary_hex': None,
             'purple_flag': False, 'display_font': None, 'display_font_paradigm': None},
            {'id': 'DNA-B1', 'name': 'FamB1', 'family': 'B', 'primary_hex': None,
             'purple_flag': False, 'display_font': None, 'display_font_paradigm': None},
        ]}, ensure_ascii=False))
        hist_pool = tmp / 'pool.json'
        save_history(hist_pool, {'version': '3.2', 'generations': []})
        rc1 = main(['--history', str(hist_pool), '--dna-index', str(fake_index),
                    'reserve', '--brand', 'F1', '--primary-dna', 'DNA-A1', '--primary-family', 'A',
                    '--bg-tone', 'warm-paper', '--display', 'PoolA', '--body', 'Archivo',
                    '--primary-hex', '#556677'])
        rc2 = main(['--history', str(hist_pool), '--dna-index', str(fake_index),
                    'reserve', '--brand', 'F2', '--primary-dna', 'DNA-A2', '--primary-family', 'A',
                    '--bg-tone', 'cool-white', '--display', 'PoolB', '--body', 'Archivo',
                    '--primary-hex', '#dd8844'])
        rc3 = main(['--history', str(hist_pool), '--dna-index', str(fake_index),
                    'reserve', '--brand', 'F3', '--primary-dna', 'DNA-B1', '--primary-family', 'B',
                    '--bg-tone', 'cool-white', '--display', 'PoolC', '--body', 'Archivo',
                    '--primary-hex', '#998877'])
        print('  %-38s %s' % ('抽到池外（同 family 已用）被擋', 'PASS' if rc1 == 0 and rc2 == 1 else 'FAIL'))
        ok &= (rc1 == 0 and rc2 == 1)
        print('  %-38s %s' % ('池內（不同 family）照樣通過', 'PASS' if rc3 == 0 else 'FAIL'))
        ok &= (rc3 == 0)

        # A2：verify 是牙齒——查無訂位就不准開工
        hist_verify = tmp / 'verify.json'
        save_history(hist_verify, {'version': '3.2', 'generations': []})
        proj = str(tmp / 'sites' / 'verify-site')
        main(['--history', str(hist_verify), '--dna-index', str(no_index),
              'reserve', '--brand', 'V', '--primary-dna', 'DNA-01', '--bg-tone', 'warm-paper',
              '--display', 'VerifyDisp', '--body', 'Archivo', '--primary-hex', '#665544',
              '--project', proj])
        rc_ok = main(['--history', str(hist_verify), 'verify', '--project', proj])
        rc_missing = main(['--history', str(hist_verify), 'verify',
                            '--project', str(tmp / 'sites' / 'never-reserved')])
        print('  %-38s %s' % ('verify 找得到訂位', 'PASS' if rc_ok == 0 else 'FAIL'))
        ok &= rc_ok == 0
        print('  %-38s %s' % ('verify 查無訂位就中止（非零退出）', 'PASS' if rc_missing == 1 else 'FAIL'))
        ok &= rc_missing == 1

        # C5：結構訂位併入同一支腳本，區塊序列編輯距離 <3 視為太像
        hist_struct = tmp / 'structural-history.json'
        save_history(hist_struct, {'version': '3.2', 'generations': []})
        rc1 = main(['--struct-history', str(hist_struct), 'struct-reserve', '--brand', 'S1',
                    '--project', str(tmp / 's1'), '--seed', '1',
                    '--sections', 'hero,usp,grid,testimonial,faq,footer',
                    '--pages', 'home,shop,product,cart,checkout'])
        rc2 = main(['--struct-history', str(hist_struct), 'struct-reserve', '--brand', 'S2',
                    '--project', str(tmp / 's2'), '--seed', '2',
                    '--sections', 'hero,usp,grid,testimonial,faq,footer2',
                    '--pages', 'home,shop,product,cart,about'])
        print('  %-38s %s' % ('結構序列太像被擋（編輯距離<3）', 'PASS' if rc1 == 0 and rc2 == 1 else 'FAIL'))
        ok &= (rc1 == 0 and rc2 == 1)

        rc3 = main(['--struct-history', str(hist_struct), 'struct-reserve', '--brand', 'S3',
                    '--project', str(tmp / 's3'), '--seed', '3',
                    '--sections', 'usp,hero,collection,lookbook,press,newsletter,footer',
                    '--pages', 'home,lookbook,collections,story,contact'])
        print('  %-38s %s' % ('結構序列夠不一樣就過', 'PASS' if rc3 == 0 else 'FAIL'))
        ok &= rc3 == 0

        # commit／abandon 直接沿用既有子指令，指到結構歷史檔即可（同一把鎖，不造第二套）
        rc_commit = main(['--history', str(hist_struct), 'commit', '--id', '1'])
        print('  %-38s %s' % ('結構訂位可用既有 commit 收尾', 'PASS' if rc_commit == 0 else 'FAIL'))
        ok &= rc_commit == 0

        # C3：used-categories 讀 design-history 的 category 欄位，不靠 used_categories.json
        hist_cat = tmp / 'cat.json'
        save_history(hist_cat, {'version': '3.2', 'generations': [
            {'id': 1, 'status': 'completed', 'category': 'Talisman'},
            {'id': 2, 'status': 'in_progress',
             'reserved_at': now_iso(), 'category': 'Organization'},
            {'id': 3, 'status': 'abandoned', 'category': 'ShouldNotCount'},
        ]})
        rc_cat = main(['--history', str(hist_cat), 'used-categories', '--json'])
        print('  %-38s %s' % ('used-categories 排除 abandoned', 'PASS' if rc_cat == 0 else 'FAIL'))
        ok &= rc_cat == 0

        # 同時寫入：兩個 process 同時 reserve，兩筆都要在，不可以互相蓋掉
        import subprocess
        hist2 = tmp / 'race.json'
        save_history(hist2, {'version': '3.2', 'generations': []})
        procs = []
        for i in range(6):
            procs.append(subprocess.Popen(
                [sys.executable, os.path.abspath(__file__), '--history', str(hist2),
                 '--dna-index', str(no_index),
                 'reserve', '--force',
                 '--brand', 'R%d' % i, '--primary-dna', 'DNA-%02d' % i,
                 '--bg-tone', 'cool-white', '--display', 'F%d' % i, '--body', 'Archivo',
                 '--primary-hex', '#%02x%02x%02x' % (10 * i, 20 * i, 30 * i)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        for p in procs:
            p.wait()
        rows = load_history(hist2)['generations']
        ids = sorted(e['id'] for e in rows)
        race_ok = len(rows) == 6 and ids == list(range(1, 7))
        print('  %-38s %s（實得 %d 筆、id=%s）'
              % ('六支同時訂位不互相蓋掉', 'PASS' if race_ok else 'FAIL', len(rows), ids))
        ok &= race_ok
    finally:
        shutil.rmtree(str(tmp), ignore_errors=True)
        print('  測試樣本已清除：%s' % (not tmp.exists()))
    print('自我測試：%s' % ('全數通過' if ok else '沒過，這支腳本的判定不算數'))
    return 0 if ok else 1


def cmd_verify(args) -> int:
    """Phase 2 開工前跑：查無本站的 in_progress／completed 訂位就中止建站。
    A2：訂位制只有「登記」沒有「下游強制查驗」等於沒有牙齒，這支就是牙齒。"""
    path = Path(args.history)
    data = load_history(path)
    project = (args.project or '').strip()
    matches = [e for e in blocking_entries(data, args.stale_minutes)
               if (e.get('project_path') or '').strip() == project]
    if not matches:
        print('FAIL  找不到 %s 的訂位紀錄。開工前必須先跑 reserve，不可以跳過。' % project)
        return 1
    entry = matches[-1]
    print('PASS  id=%s 訂位存在，status=%s，DNA=%s，bg=%s，display=%s'
          % (entry.get('id'), entry.get('status'), entry.get('primary_dna'),
             entry.get('bg_tone'), (entry.get('fonts') or {}).get('display')))
    if args.decisions:
        dpath = Path(args.decisions)
        if not dpath.is_file():
            print('WARN  --decisions 指定的檔案不存在：%s（跳過內容比對）' % dpath)
            return 0
        content = io.open(str(dpath), encoding='utf-8').read()
        checks = [
            ('primary_dna', entry.get('primary_dna')),
            ('bg_tone', entry.get('bg_tone')),
            ('display font', (entry.get('fonts') or {}).get('display')),
        ]
        mismatch = False
        for label, val in checks:
            if val and val != 'unknown' and val not in content:
                print('FAIL  DECISIONS.md 裡找不到訂位登記的 %s＝%s（文件與登記對不上）' % (label, val))
                mismatch = True
        if mismatch:
            return 1
        print('PASS  DECISIONS.md 內容與訂位登記一致（primary_dna／bg_tone／display 三項都找得到）')
    return 0


def cmd_used_categories(args) -> int:
    """C3：廢除獨立的 used_categories.json，品類去重直接讀 design-history 的 category 欄位
    （單一真相）。abandoned 不算用過，其餘（completed／未過期的 in_progress）都算。"""
    data = load_history(Path(args.history))
    cats = sorted({(e.get('category') or '').strip()
                   for e in blocking_entries(data, args.stale_minutes)
                   if (e.get('category') or '').strip()})
    if args.json:
        print(json.dumps(cats, ensure_ascii=False))
    else:
        for c in cats:
            print(c)
    return 0


def cmd_struct_plan(args) -> int:
    """C5：結構訂位併入同一把鎖。看近 8 站的區塊序列與分頁組合，不再是人工比對。"""
    path = Path(args.struct_history)
    data = load_history(path)
    recents = blocking_entries(data, args.stale_minutes)[-STRUCT_WINDOW:]
    print('結構歷史檔：%s' % path)
    print('近 %d 站的結構指紋：' % len(recents))
    for e in recents:
        print('  id=%-4s %-18s seed=%-6s sections=%s'
              % (e.get('id'), e.get('brand', ''), e.get('structural_seed'),
                 '/'.join(e.get('section_sequence') or [])))
        print('              pages=%s' % '/'.join(e.get('page_combo') or []))
    return 0


def cmd_struct_reserve(args) -> int:
    """檢查（編輯距離／Jaccard）與登記同一把鎖，比照 design reserve 的訂位式作法。
    commit／abandon 直接沿用既有的 `commit`／`abandon` 子指令，指到 --history 這個結構檔即可，
    不重造第二套（同一把鎖管所有「選定即登記」，見 uniqueness-guarantee.md）。"""
    path = Path(args.struct_history)
    sections = [s.strip() for s in args.sections.split(',') if s.strip()]
    pages = [s.strip() for s in args.pages.split(',') if s.strip()]
    with FileLock(path):
        data = load_history(path)
        recents = blocking_entries(data, args.stale_minutes)[-STRUCT_WINDOW:]
        problems = []
        for e in recents:
            other_sections = e.get('section_sequence') or []
            dist = edit_distance(sections, other_sections)
            if dist < EDIT_DISTANCE_MIN:
                problems.append('與 id=%s（%s）的區塊序列編輯距離只有 %d（門檻 %d），太像'
                                % (e.get('id'), e.get('brand', ''), dist, EDIT_DISTANCE_MIN))
            other_pages = set(e.get('page_combo') or [])
            jac = jaccard(set(pages), other_pages)
            if jac >= PAGE_JACCARD_MAX:
                problems.append('與 id=%s（%s）的分頁組合 Jaccard 相似度 %.2f（門檻需 <%.2f），太像'
                                % (e.get('id'), e.get('brand', ''), jac, PAGE_JACCARD_MAX))
        if problems and not args.force:
            print('REJECTED  結構指紋撞近 %d 站，沒有寫進去：' % STRUCT_WINDOW)
            for m in problems:
                print('  ✗ %s' % m)
            print('換一組 seed／區塊順序／分頁組合再訂位，或加 --force 並在 --note 寫明理由。')
            return 1
        ids = [e.get('id', 0) for e in data.get('generations', [])]
        new_id = (max(ids) if ids else 0) + 1
        entry = {
            'id': new_id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'in_progress',
            'reserved_at': now_iso(),
            'completed_at': None,
            'brand': args.brand,
            'project_path': args.project,
            'structural_seed': args.seed,
            'section_sequence': sections,
            'page_combo': pages,
            'note': args.note,
        }
        data.setdefault('generations', []).append(entry)
        save_history(path, data)
    if problems:
        print('⚠️  --force：明知結構太像仍訂位，理由請寫在 note 裡')
    print('RESERVED  struct id=%d  seed=%s  sections=%s'
          % (new_id, args.seed, '/'.join(sections)))
    print('站交付後跑：commit --history %s --id %d ；做不下去跑：abandon --history %s --id %d'
          % (path, new_id, path, new_id))
    return 0


def build_parser():
    p = argparse.ArgumentParser(description='設計基因的訂位式登記（選中就登記，不等站做完）')
    p.add_argument('--history', default=str(DEFAULT_HISTORY))
    p.add_argument('--struct-history', default=str(DEFAULT_STRUCT_HISTORY),
                    help='結構訂位（struct-plan／struct-reserve）用的歷史檔，與 --history 分開')
    p.add_argument('--dna-index', default=str(DEFAULT_DNA_INDEX))
    p.add_argument('--window', type=int, default=RECENT_WINDOW)
    p.add_argument('--stale-minutes', type=int, default=RESERVE_STALE_MINUTES)
    sub = p.add_subparsers(dest='cmd', required=True)

    sp = sub.add_parser('plan', help='看這次要避開哪些底色與字體；加 --pool 印出可抽的 DNA 清單')
    sp.add_argument('--pool', action='store_true',
                     help='A1：先用 family／紫色／字體三重交集過濾 dna-index.json，只印出可抽的清單')
    sp.set_defaults(func=cmd_plan)

    sp = sub.add_parser('reserve', help='選定基因的當下立刻訂位（檢查與登記同一把鎖）')
    sp.add_argument('--brand', required=True)
    sp.add_argument('--category', default='')
    sp.add_argument('--project', default='')
    sp.add_argument('--primary-dna', required=True)
    sp.add_argument('--primary-family', default='')
    sp.add_argument('--secondary-dna', default='none')
    sp.add_argument('--secondary-family', default='none')
    sp.add_argument('--secondary-contribution', default='none')
    sp.add_argument('--ui-framework', default='')
    sp.add_argument('--bg-tone', required=True, choices=list(BG_TONES))
    sp.add_argument('--bg-hex', default='')
    sp.add_argument('--display', required=True)
    sp.add_argument('--body', required=True)
    sp.add_argument('--primary-hex', required=True,
                     help='#rrggbb，必填。去重主鍵從「DNA id」改成可觀測維度後，這是主色 hue 桶判準的來源')
    sp.add_argument('--signature-fx', default='none',
                     help='本站簽名動效（tilt/magnetic/parallax/none…），近 3 筆不建議重複，登記制不強制擋')
    sp.add_argument('--color-secondary', default='unknown')
    sp.add_argument('--color-accent', default='unknown')
    sp.add_argument('--note', default='')
    sp.add_argument('--force', action='store_true', help='明知違反去重規則仍要登記')
    sp.add_argument('--no-pool-check', action='store_true',
                     help='跳過 A1 池子檢查（僅供測試／已知例外使用，正常流程不要加）')
    sp.set_defaults(func=cmd_reserve)

    sp = sub.add_parser('commit', help='站交付後把訂位轉成已完成（design 或 structural 兩種歷史檔都適用）')
    sp.add_argument('--id', type=int, required=True)
    sp.add_argument('--maturity-score', type=int)
    sp.add_argument('--display', default='')
    sp.add_argument('--body', default='')
    sp.add_argument('--bg-tone', default='')
    sp.add_argument('--bg-hex', default='')
    sp.add_argument('--note', default='')
    sp.set_defaults(func=cmd_commit)

    sp = sub.add_parser('abandon', help='站做不下去，退位讓給別人（design 或 structural 兩種歷史檔都適用）')
    sp.add_argument('--id', type=int, required=True)
    sp.add_argument('--reason', default='')
    sp.set_defaults(func=cmd_abandon)

    sp = sub.add_parser('verify', help='A2：Phase 2 開工前查有沒有本站的訂位，查無就中止建站')
    sp.add_argument('--project', required=True)
    sp.add_argument('--decisions', default='',
                     help='選填：DECISIONS.md 路徑，額外比對訂位維度是否真的寫進文件裡')
    sp.set_defaults(func=cmd_verify)

    sp = sub.add_parser('used-categories', help='C3：印出目前算「已用過」的品類（讀 design-history，不再靠 used_categories.json）')
    sp.add_argument('--json', action='store_true')
    sp.set_defaults(func=cmd_used_categories)

    sp = sub.add_parser('struct-plan', help='C5：看近 8 站的結構指紋（區塊序列／分頁組合）')
    sp.set_defaults(func=cmd_struct_plan)

    sp = sub.add_parser('struct-reserve', help='C5：選定結構 seed 的當下立刻訂位（編輯距離／Jaccard 判重）')
    sp.add_argument('--brand', required=True)
    sp.add_argument('--project', default='')
    sp.add_argument('--seed', required=True)
    sp.add_argument('--sections', required=True, help='逗號分隔的區塊 token 序列，如 hero,usp,grid,faq,footer')
    sp.add_argument('--pages', required=True, help='逗號分隔的分頁組合，如 home,shop,product,cart,checkout')
    sp.add_argument('--note', default='')
    sp.add_argument('--force', action='store_true')
    sp.set_defaults(func=cmd_struct_reserve)

    sp = sub.add_parser('selftest', help='證明防重複與同時寫入真的有作用')
    sp.set_defaults(func=cmd_selftest)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except LockTimeout as exc:
        print('FAIL  %s' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
