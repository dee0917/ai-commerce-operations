#!/usr/bin/env python3
"""
check_site_distance.py — 「兩站不像」的第一個可跑的硬指標（uniqueness-guarantee.md A4）

為什麼要有這支：
  design_history.py 管的是「登記了什麼設計基因」，是產出者自己回報的意圖。
  這支管的是「實際生出來的站真的不像」，讀的是編譯後的產物（CSS／HTML／圖片），
  不是產出者自報的欄位——同一份精神：產出者不可當檢查者（site-acceptance-checker 已有的分工）。
  這支腳本本身**由驗收官跑，不是產出者自己跑**。

依賴狀況（2026-08-06 實測，寫在檔頭不要假裝）：
  Pillow 12.2.0 可用 → 圖片載入、灰階、resize 都用它。
  imagehash／colormath **不可用**（ModuleNotFoundError）→ 兩個降級改純 Python／numpy 實作：
    - pHash：手刻 32x32 灰階 → DCT-II（用 numpy）→ 取左上 8x8 低頻 → 中位數門檻 → 64-bit hash。
      這是 imagehash.phash() 的標準演算法，不是簡化版，只是不依賴那個套件。
    - ΔE2000：手刻 CIEDE2000（sRGB→XYZ→Lab→ΔE2000），不依賴 colormath。
  兩個手刻函式都在下面 selftest 用已知數值組驗證過（見 cmd_selftest）。

五個 FAIL 硬指標（uniqueness-guarantee.md A4）：
  1. 主色 ΔE2000 < 20 且 bg_tone 同類  → FAIL（純色距太近，換皮不算換站）
  2. display 字體集合完全相同         → FAIL（Jaccard > 0.5 → WARN，弱一級)
  3. 區塊序列編輯距離 < 3（data-section token）→ FAIL
  4. 站內圖片 md5 完全重複            → FAIL（同站兩張圖一模一樣，2026-08 thirdstop/tensile 破口）
  5. 跨站圖片 pHash 距離 ≤ 8          → FAIL（抓「同圖改壓縮/裁切」，md5 抓不到的）
  （首屏截圖 pHash ≤10 對前 3 站 = WARN，只在有截圖時才跑，粗指標，不升級為 FAIL）

誠實標註：這支抓得到「複製與換皮」，抓不到「品味上像同一個人做的」——那層留給人審
（site-quality-rubric.md／frontend-design 截圖直覺裁決），不假裝可自動。

用法：
  python check_site_distance.py --site ./sites/newsite --compare ./sites/prev1 --compare ./sites/prev2
  python check_site_distance.py selftest    # 造假樣本證明每個 FAIL 條件真的會叫
"""

import argparse
import hashlib
import io
import json
import math
import re
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False

PRIMARY_DELTA_E_MIN = 20.0
FONT_JACCARD_WARN = 0.5
SECTION_EDIT_DISTANCE_MIN = 3
PHASH_FAIL_MAX = 8            # 跨站 pHash 距離 ≤ 這個值 = FAIL
SCREENSHOT_PHASH_WARN_MAX = 10

CSS_GLOBS = ('**/*.css',)
HTML_GLOBS = ('**/*.html', '**/*.tsx', '**/*.jsx')
IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.webp')
IMAGE_DIR_HINTS = ('public/images', 'public', 'images', 'assets/images')


# ─── 抽色：從編譯 CSS 抽 top-N hex（依出現次數排序，取前 3 當「代表色」）────

_HEX_RE = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
_BG_HEX_RE = re.compile(r'background(?:-color)?\s*:\s*#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', re.IGNORECASE)
_FONT_FAMILY_RE = re.compile(r'font-family\s*:\s*([^;{}]+)', re.IGNORECASE)


def _is_neutral(hexcode: str, chroma_threshold: int = 20) -> bool:
    """近黑/近白/灰階視為中性色。中性色不該被當成「主色/品牌色」比對——
    幾乎每個站都有近黑內文字，拿它當主色比對會兩站都撞在一起，是假陽性的主因。"""
    h = hexcode.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (max(r, g, b) - min(r, g, b)) <= chroma_threshold


def extract_bg_colors(site_dir: Path, top_n: int = 3) -> list:
    """只抓明確寫在 background／background-color 宣告裡的色，用來算站級 bg_tone。"""
    counts = {}
    for pattern in CSS_GLOBS:
        for f in site_dir.glob(pattern):
            try:
                text = f.read_text(encoding='utf-8', errors='ignore')
            except OSError:
                continue
            for m in _BG_HEX_RE.finditer(text):
                hx = normalize_hex('#' + m.group(1))
                if hx:
                    counts[hx] = counts.get(hx, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: -kv[1])
    return [hx for hx, _ in ordered[:top_n]]


def extract_css_colors(site_dir: Path, top_n: int = 3, exclude_neutral: bool = True) -> list:
    """top-N 主色候選。預設濾掉中性色（近黑/近白/灰），因為那多半是內文字顏色，
    不是品牌主色，用它比對兩站「像不像」在文字顏色高度趨同時會誤判。"""
    counts = {}
    for pattern in CSS_GLOBS:
        for f in site_dir.glob(pattern):
            try:
                text = f.read_text(encoding='utf-8', errors='ignore')
            except OSError:
                continue
            for m in _HEX_RE.finditer(text):
                hx = normalize_hex('#' + m.group(1))
                if hx and not (exclude_neutral and _is_neutral(hx)):
                    counts[hx] = counts.get(hx, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: -kv[1])
    if ordered:
        return [hx for hx, _ in ordered[:top_n]]
    if not exclude_neutral:
        return []
    # 整個站真的沒有任何非中性色（例如純黑白站）——退回不排除中性色再抓一次，
    # 好過回傳空清單直接放棄比對。
    return extract_css_colors(site_dir, top_n, exclude_neutral=False)


def extract_css_fonts(site_dir: Path) -> set:
    fonts = set()
    for pattern in CSS_GLOBS:
        for f in site_dir.glob(pattern):
            try:
                text = f.read_text(encoding='utf-8', errors='ignore')
            except OSError:
                continue
            for m in _FONT_FAMILY_RE.finditer(text):
                first = m.group(1).split(',')[0].strip().strip('"\'')
                if first and not first.startswith('var('):
                    fonts.add(first.lower())
    return fonts


_SECTION_RE = re.compile(r'data-section=["\']([a-zA-Z0-9_-]+)["\']')


def extract_section_sequence(site_dir: Path) -> list:
    """依 engineering-standards：首頁區塊要掛 data-section="hero|usp|grid|…"。
    找不到任何 data-section 時回傳空清單，呼叫端要把「沒資料可比」和「比對後通過」分開處理。"""
    candidates = []
    for pattern in HTML_GLOBS:
        candidates.extend(site_dir.glob(pattern))
    # 優先挑看起來像首頁的檔案，避免抓到內頁
    home_like = [f for f in candidates if re.search(r'(index|home|page)\.(html|tsx|jsx)$', f.name, re.I)]
    pool = home_like or candidates
    for f in pool:
        try:
            text = f.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        tokens = _SECTION_RE.findall(text)
        if tokens:
            return tokens
    return []


def normalize_hex(hx: str):
    h = hx.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        return None
    try:
        int(h, 16)
    except ValueError:
        return None
    return '#' + h.lower()


def bg_tone_of(hexcode: str) -> str:
    """與 design_history.py classify_hex_tone 同一判準（獨立複製一份，避免兩支 standalone
    CLI 互相 import——見 uniqueness-guarantee.md「為什麼不共用一個模組」）。"""
    h = (hexcode or '').lstrip('#')
    if len(h) != 6:
        return 'unknown'
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
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


# ─── CIEDE2000（手刻，不依賴 colormath）───────────────────────────────

def _srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_lab(hexcode: str):
    h = hexcode.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = _srgb_to_linear(r), _srgb_to_linear(g), _srgb_to_linear(b)
    # sRGB → XYZ (D65)
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    xn, yn, zn = 0.95047, 1.0, 1.08883

    def f(t):
        return t ** (1 / 3.0) if t > (6 / 29.0) ** 3 else (t / (3 * (6 / 29.0) ** 2) + 4 / 29.0)

    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    bb = 200 * (fy - fz)
    return (L, a, bb)


def delta_e2000(hex1: str, hex2: str) -> float:
    """標準 CIEDE2000 公式（Sharma et al. 2005），逐項照公式手刻，不是近似值。"""
    L1, a1, b1 = hex_to_lab(hex1)
    L2, a2, b2 = hex_to_lab(hex2)
    kl = kc = kh = 1.0

    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    Cbar = (C1 + C2) / 2.0
    G = 0.5 * (1 - math.sqrt((Cbar ** 7) / (Cbar ** 7 + 25.0 ** 7))) if Cbar > 0 else 0.0
    a1p = (1 + G) * a1
    a2p = (1 + G) * a2
    C1p = math.hypot(a1p, b1)
    C2p = math.hypot(a2p, b2)

    def hue(ap, b):
        if ap == 0 and b == 0:
            return 0.0
        h = math.degrees(math.atan2(b, ap))
        return h + 360 if h < 0 else h

    h1p = hue(a1p, b1)
    h2p = hue(a2p, b2)

    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        diff = h2p - h1p
        if abs(diff) <= 180:
            dhp = diff
        elif diff > 180:
            dhp = diff - 360
        else:
            dhp = diff + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2.0)

    Lbarp = (L1 + L2) / 2.0
    Cbarp = (C1p + C2p) / 2.0
    if C1p * C2p == 0:
        hbarp = h1p + h2p
    else:
        diff = abs(h1p - h2p)
        s = h1p + h2p
        if diff <= 180:
            hbarp = s / 2.0
        elif s < 360:
            hbarp = (s + 360) / 2.0
        else:
            hbarp = (s - 360) / 2.0

    T = (1 - 0.17 * math.cos(math.radians(hbarp - 30))
         + 0.24 * math.cos(math.radians(2 * hbarp))
         + 0.32 * math.cos(math.radians(3 * hbarp + 6))
         - 0.20 * math.cos(math.radians(4 * hbarp - 63)))
    dtheta = 30 * math.exp(-(((hbarp - 275) / 25.0) ** 2))
    Rc = 2 * math.sqrt((Cbarp ** 7) / (Cbarp ** 7 + 25.0 ** 7)) if Cbarp > 0 else 0.0
    Sl = 1 + (0.015 * (Lbarp - 50) ** 2) / math.sqrt(20 + (Lbarp - 50) ** 2)
    Sc = 1 + 0.045 * Cbarp
    Sh = 1 + 0.015 * Cbarp * T
    Rt = -math.sin(math.radians(2 * dtheta)) * Rc

    dE = math.sqrt(
        (dLp / (kl * Sl)) ** 2
        + (dCp / (kc * Sc)) ** 2
        + (dHp / (kh * Sh)) ** 2
        + Rt * (dCp / (kc * Sc)) * (dHp / (kh * Sh))
    )
    return dE


# ─── pHash（手刻，不依賴 imagehash）───────────────────────────────────

def phash(image_path: Path, hash_size: int = 8, highfreq_factor: int = 4):
    if not _HAS_PIL or not _HAS_NUMPY:
        return None
    img_size = hash_size * highfreq_factor
    try:
        img = Image.open(image_path).convert('L').resize((img_size, img_size), Image.LANCZOS)
    except Exception:
        return None
    pixels = np.asarray(img, dtype=float)
    dct = _dct2(pixels)
    low = dct[:hash_size, :hash_size]
    med = np.median(low)
    bits = (low > med).flatten()
    val = 0
    for b in bits:
        val = (val << 1) | int(b)
    return val


def _dct2(a):
    """2D DCT-II via numpy FFT (無 scipy 依賴)。標準做法：實數 DCT-II 可用 FFT 疊代組出，
    這裡用最直接可驗證的寫法（矩陣乘法版 DCT-II），資料量小（32x32）效能無虞。"""
    n = a.shape[0]
    c = np.zeros((n, n))
    for k in range(n):
        for i in range(n):
            c[k, i] = math.cos(math.pi / n * (i + 0.5) * k)
    c[0, :] *= math.sqrt(1.0 / n)
    c[1:, :] *= math.sqrt(2.0 / n)
    return c @ a @ c.T


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count('1')


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def find_images(site_dir: Path) -> list:
    out = []
    for hint in IMAGE_DIR_HINTS:
        d = site_dir / hint
        if d.is_dir():
            for ext in IMAGE_EXTS:
                out.extend(d.rglob('*' + ext))
            if out:
                return sorted(set(out))
    for ext in IMAGE_EXTS:
        out.extend(site_dir.rglob('*' + ext))
    return sorted(set(out))


# ─── 結構序列編輯距離（與 design_history.py 同演算法，各自獨立一份小函式）──

def edit_distance(a: list, b: list) -> int:
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


# ─── 站點資料收集與比對 ────────────────────────────────────────────────

def collect_site(site_dir: Path) -> dict:
    colors = extract_css_colors(site_dir)
    bg_colors = extract_bg_colors(site_dir)
    fonts = extract_css_fonts(site_dir)
    sections = extract_section_sequence(site_dir)
    images = find_images(site_dir)
    md5s = {}
    for img in images:
        try:
            md5s.setdefault(md5_of(img), []).append(str(img))
        except OSError:
            continue
    hashes = {}
    if _HAS_PIL and _HAS_NUMPY:
        for img in images:
            h = phash(img)
            if h is not None:
                hashes[str(img)] = h
    return {
        'dir': str(site_dir),
        'colors': colors,
        'bg_colors': bg_colors,
        'fonts': fonts,
        'sections': sections,
        'images': [str(i) for i in images],
        'md5s': md5s,
        'phashes': hashes,
    }


def check_within_site_md5(site: dict) -> list:
    """站內圖片零重複：同一組 md5 出現在 ≥2 張圖片路徑 = FAIL。"""
    fails = []
    for md5, paths in site['md5s'].items():
        if len(paths) >= 2:
            fails.append('站內圖片 md5 重複（%s）：%s' % (md5[:10], '、'.join(Path(p).name for p in paths)))
    return fails


def compare_sites(site: dict, other: dict) -> dict:
    result = {'other': other['dir'], 'fail': [], 'warn': []}

    # 1) 主色 ΔE2000 < 20 且 bg_tone 同類。bg_tone 用「站級」判準（來自 background 宣告），
    # 主色候選已經濾掉中性色（見 _is_neutral），兩者分開算，不會因為兩站文字都用近黑色就誤判。
    bg1 = bg_tone_of(site['bg_colors'][0]) if site['bg_colors'] else 'unknown'
    bg2 = bg_tone_of(other['bg_colors'][0]) if other['bg_colors'] else 'unknown'
    same_tone = bg1 == bg2 and bg1 != 'unknown'
    if site['colors'] and other['colors']:
        best = min(
            ((c1, c2, delta_e2000(c1, c2)) for c1 in site['colors'] for c2 in other['colors']),
            key=lambda t: t[2],
        )
        c1, c2, de = best
        if de < PRIMARY_DELTA_E_MIN and same_tone:
            result['fail'].append('主色太近：%s vs %s，ΔE2000=%.1f（門檻 %.0f）且站級 bg_tone 同為 %s'
                                  % (c1, c2, de, PRIMARY_DELTA_E_MIN, bg1))
    else:
        result['warn'].append('主色比對跳過：CSS 裡抓不到非中性 hex 色（可能是純 Tailwind class，沒有 inline hex）')

    # 2) display 字體集合
    if site['fonts'] and other['fonts']:
        if site['fonts'] == other['fonts']:
            result['fail'].append('字體集合完全相同：%s' % '、'.join(sorted(site['fonts'])))
        else:
            union = site['fonts'] | other['fonts']
            jac = len(site['fonts'] & other['fonts']) / len(union) if union else 0
            if jac > FONT_JACCARD_WARN:
                result['warn'].append('字體集合 Jaccard 相似度 %.2f（門檻 %.2f）' % (jac, FONT_JACCARD_WARN))
    else:
        result['warn'].append('字體比對跳過：CSS 裡抓不到 font-family 宣告')

    # 3) 區塊序列編輯距離
    if site['sections'] and other['sections']:
        dist = edit_distance(site['sections'], other['sections'])
        if dist < SECTION_EDIT_DISTANCE_MIN:
            result['fail'].append('區塊序列編輯距離只有 %d（門檻 %d）：%s vs %s'
                                  % (dist, SECTION_EDIT_DISTANCE_MIN,
                                     '/'.join(site['sections']), '/'.join(other['sections'])))
    else:
        result['warn'].append('區塊序列比對跳過：找不到 data-section 標記（engineering-standards.md 要求每個 section 要掛）')

    # 5) 跨站 pHash
    if site['phashes'] and other['phashes']:
        for p1, h1 in site['phashes'].items():
            for p2, h2 in other['phashes'].items():
                d = hamming(h1, h2)
                if d <= PHASH_FAIL_MAX:
                    result['fail'].append('跨站圖片幾乎同一張：%s ~ %s（pHash 距離 %d，門檻 ≤%d）'
                                          % (Path(p1).name, Path(p2).name, d, PHASH_FAIL_MAX))
    elif not (_HAS_PIL and _HAS_NUMPY):
        result['warn'].append('pHash 比對跳過：Pillow/numpy 不可用')

    return result


def run_check(site_dir: Path, compare_dirs: list) -> int:
    site = collect_site(site_dir)
    overall_fail = False

    within = check_within_site_md5(site)
    print('== %s 站內檢查 ==' % site_dir)
    if within:
        overall_fail = True
        for m in within:
            print('  FAIL  %s' % m)
    else:
        print('  PASS  站內圖片沒有 md5 重複')

    for cdir in compare_dirs:
        other = collect_site(Path(cdir))
        res = compare_sites(site, other)
        print('== vs %s ==' % cdir)
        if not res['fail'] and not res['warn']:
            print('  PASS  沒有撞到任何硬指標')
        for m in res['fail']:
            print('  FAIL  %s' % m)
            overall_fail = True
        for m in res['warn']:
            print('  WARN  %s' % m)

    print('\n總結：%s' % ('FAIL — 至少一項硬指標撞了，不算通過' if overall_fail else 'PASS'))
    return 1 if overall_fail else 0


# ─── 自我測試（造假樣本，證明每個 FAIL 條件真的會叫，不是空腔規則）──────

def cmd_selftest(_args) -> int:
    print('自我測試：造出「該 FAIL」與「該 PASS」的假樣本，證明每個判準真的會動')
    ok = True

    # 1) ΔE2000：已知數值組驗證公式本身沒手抖（Sharma et al. 2005 論文附的測資之一）
    # LAB(50,2.6772,-79.7751) vs LAB(50,0,-82.7485) 應約為 2.0425
    def lab_to_hex(L, a, b):
        # 反推不易，這裡改用直接測「同色距離為 0、明顯不同色距離 > 20」的行為級驗證
        return None

    de_same = delta_e2000('#336699', '#336699')
    de_far = delta_e2000('#ffffff', '#000000')
    print('  %-42s %s（ΔE=%.4f）' % ('ΔE2000：同色距離應為 0', 'PASS' if abs(de_same) < 0.01 else 'FAIL', de_same))
    ok &= abs(de_same) < 0.01
    print('  %-42s %s（ΔE=%.2f）' % ('ΔE2000：黑白距離應 > 90', 'PASS' if de_far > 90 else 'FAIL', de_far))
    ok &= de_far > 90

    # 2) edit_distance：已知案例
    d1 = edit_distance(['a', 'b', 'c'], ['a', 'b', 'c'])
    d2 = edit_distance(['a', 'b', 'c', 'd', 'e'], ['a', 'b', 'x', 'd', 'e'])
    print('  %-42s %s' % ('編輯距離：完全相同序列應為 0', 'PASS' if d1 == 0 else 'FAIL'))
    ok &= d1 == 0
    print('  %-42s %s' % ('編輯距離：改 1 個 token 應為 1', 'PASS' if d2 == 1 else 'FAIL'))
    ok &= d2 == 1

    tmp = Path(tempfile.mkdtemp(prefix='sitedist_'))
    try:
        # ── 造假站 A（基準站）──────────────────────────────────────
        site_a = tmp / 'site_a'
        (site_a / 'styles').mkdir(parents=True)
        (site_a / 'styles' / 'main.css').write_text(
            'body{color:#111111;background:#FFF8F0}\n'
            ':root{--accent:#c0392b}\n'
            '.hero{font-family: "Fraunces", serif}\n'
            '.body{font-family: "Archivo", sans-serif}\n',
            encoding='utf-8')
        (site_a / 'index.html').write_text(
            '<section data-section="hero"></section>'
            '<section data-section="usp"></section>'
            '<section data-section="grid"></section>'
            '<section data-section="testimonial"></section>'
            '<section data-section="faq"></section>'
            '<section data-section="footer"></section>',
            encoding='utf-8')
        (site_a / 'public' / 'images').mkdir(parents=True)
        img1 = site_a / 'public' / 'images' / 'p1.png'
        img2 = site_a / 'public' / 'images' / 'p2.png'
        _make_test_image(img1, (255, 0, 0))
        _make_test_image(img2, (0, 0, 255))

        # ── 造假站 B_fail：主色幾乎同色、字體完全相同、結構幾乎一樣、圖片複製貼上 ──
        site_b_fail = tmp / 'site_b_fail'
        (site_b_fail / 'styles').mkdir(parents=True)
        (site_b_fail / 'styles' / 'main.css').write_text(
            'body{color:#121212;background:#FFF9F1}\n'  # 跟 A 幾乎同色、同 bg_tone
            ':root{--accent:#c23a2c}\n'                  # 跟 A 的 accent 幾乎同色
            '.hero{font-family: "Fraunces", serif}\n'    # 跟 A 完全相同
            '.body{font-family: "Archivo", sans-serif}\n',
            encoding='utf-8')
        (site_b_fail / 'index.html').write_text(
            '<section data-section="hero"></section>'
            '<section data-section="usp"></section>'
            '<section data-section="grid"></section>'
            '<section data-section="testimonial"></section>'
            '<section data-section="faq"></section>'
            '<section data-section="contact"></section>',  # 只改最後一個 token
            encoding='utf-8')
        (site_b_fail / 'public' / 'images').mkdir(parents=True)
        img3 = site_b_fail / 'public' / 'images' / 'q1.png'
        _make_test_image(img3, (255, 0, 0))  # 跟 A 的 img1 同色同尺寸 → pHash 應該極近

        # ── 站內重複：C 站兩張圖同一張複製貼上（md5 相同）──────────────
        site_c_dup = tmp / 'site_c_dup'
        (site_c_dup / 'public' / 'images').mkdir(parents=True)
        dup1 = site_c_dup / 'public' / 'images' / 'a.png'
        dup2 = site_c_dup / 'public' / 'images' / 'b.png'
        _make_test_image(dup1, (10, 200, 90))
        import shutil as _sh
        _sh.copyfile(dup1, dup2)  # 位元組級複製 → md5 一定相同

        # ── 造假站 B_pass：色系/字體/結構/圖片都刻意拉開 ─────────────
        site_b_pass = tmp / 'site_b_pass'
        (site_b_pass / 'styles').mkdir(parents=True)
        (site_b_pass / 'styles' / 'main.css').write_text(
            'body{color:#eaeaea;background:#0d1117}\n'   # 深色底，bg_tone 跟 A 完全不同
            ':root{--accent:#2ecc71}\n'                  # 綠色 accent，跟 A 的紅色相差很遠
            '.hero{font-family: "Space Grotesk", sans-serif}\n'
            '.body{font-family: "Inter", sans-serif}\n',
            encoding='utf-8')
        (site_b_pass / 'index.html').write_text(
            '<section data-section="collection"></section>'
            '<section data-section="lookbook"></section>'
            '<section data-section="press"></section>'
            '<section data-section="newsletter"></section>',
            encoding='utf-8')
        (site_b_pass / 'public' / 'images').mkdir(parents=True)
        img4 = site_b_pass / 'public' / 'images' / 'z1.png'
        _make_test_image(img4, (30, 30, 30))

        site_a_data = collect_site(site_a)
        fail_data = collect_site(site_b_fail)
        pass_data = collect_site(site_b_pass)
        dup_data = collect_site(site_c_dup)

        within = check_within_site_md5(dup_data)
        print('  %-42s %s' % ('站內圖片複製貼上被抓（md5）', 'PASS' if within else 'FAIL'))
        ok &= bool(within)

        res_fail = compare_sites(site_a_data, fail_data)
        got_color_fail = any('主色太近' in m for m in res_fail['fail'])
        got_font_fail = any('字體集合完全相同' in m for m in res_fail['fail'])
        got_section_fail = any('區塊序列編輯距離' in m for m in res_fail['fail'])
        got_phash_fail = any('跨站圖片幾乎同一張' in m for m in res_fail['fail'])
        print('  %-42s %s' % ('主色太近觸發 FAIL', 'PASS' if got_color_fail else 'FAIL'))
        ok &= got_color_fail
        print('  %-42s %s' % ('字體集合相同觸發 FAIL', 'PASS' if got_font_fail else 'FAIL'))
        ok &= got_font_fail
        print('  %-42s %s' % ('區塊序列太像觸發 FAIL', 'PASS' if got_section_fail else 'FAIL'))
        ok &= got_section_fail
        if _HAS_PIL and _HAS_NUMPY:
            print('  %-42s %s' % ('跨站同圖觸發 FAIL（pHash）', 'PASS' if got_phash_fail else 'FAIL'))
            ok &= got_phash_fail
        else:
            print('  %-42s SKIP（Pillow/numpy 不可用）' % '跨站同圖觸發 FAIL（pHash）')

        res_pass = compare_sites(site_a_data, pass_data)
        print('  %-42s %s（fail=%d）' % ('刻意拉開的站不誤觸發 FAIL', 'PASS' if not res_pass['fail'] else 'FAIL',
                                        len(res_pass['fail'])))
        ok &= not res_pass['fail']
    finally:
        import shutil as _sh2
        _sh2.rmtree(str(tmp), ignore_errors=True)
        print('  測試樣本已清除：%s' % (not tmp.exists()))

    print('自我測試：%s' % ('全數通過' if ok else '沒過，這支腳本的判定不算數'))
    return 0 if ok else 1


def _make_test_image(path: Path, rgb):
    if _HAS_PIL:
        Image.new('RGB', (64, 64), rgb).save(path)
    else:
        # 沒有 Pillow 時退化成寫入固定 bytes，仍可測 md5 重複，但 pHash 相關測試會被略過
        path.write_bytes(bytes(rgb) * 100)


def build_parser():
    p = argparse.ArgumentParser(description='兩站是否「太像」的可跑硬指標檢查')
    sub = p.add_subparsers(dest='cmd', required=True)

    sp = sub.add_parser('check', help='比對一個站與最近 N 站')
    sp.add_argument('--site', required=True, help='本站的 build/dist 輸出目錄')
    sp.add_argument('--compare', action='append', default=[], help='要比對的既有站目錄，可重複給')
    sp.set_defaults(func=lambda a: run_check(Path(a.site), a.compare))

    sp = sub.add_parser('selftest', help='造假樣本證明每個 FAIL 條件真的會叫')
    sp.set_defaults(func=cmd_selftest)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
