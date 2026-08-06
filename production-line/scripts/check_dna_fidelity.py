#!/usr/bin/env python3
"""
check_dna_fidelity.py — DNA 忠實度檢查（交付驗收 A 區第 11.6 項）

要擋的事：**選了一個 DNA，做出來的東西卻不照它做，而且沒有任何東西會叫。**

  2026-08-04 實測：某站在 Phase 1.05 選了 DNA-44（Postevand），
  該條目白紙黑字寫「White/light neutral base」與「Bold sans headings」，
  實際產出是暖紙底 #f5f3ee ＋ Newsreader 襯線標題。
  版面沒壞、字體有載入、驗收全綠，沒有一項檢查看的是「有沒有照選定的 DNA 做」。

判準（三邊對照，對不上就 FAIL）：

  ① 編譯後的 CSS  → 實際的底色與 font-family 第一順位
  ② design-history.json → 這個站當初登記選了哪個 DNA
  ③ real-ecommerce-dna.md → 那個 DNA 條目寫的底色與字體規格

  ①推不出③就是 FAIL，不是扣分。無法判定也是 FAIL：
  讀不到底色、認不出字體類別、DNA 條目寫不清楚，一律當作沒通過，
  因為「判不出來」與「做錯了」對交付的意義完全一樣。

這支腳本自己先過變異測試：跑正式檢查前，先造出「故意違反 DNA」的假樣本，
確認抓得到才會相信它說 PASS。抓不到就中止，該次結果不算數。

**與 typography-baseline.md 的分工（不要各訂一套字型判準）**：
字級階層、展示字型配額、eyebrow、留白節奏、圓角與圖比那些鎖值，
定義與判準**全部在 `references/typography-baseline.md`**，用 Playwright 讀計算後樣式逐條驗，
這支腳本一條都不重寫也不覆寫。
這支只回答另一個問題：**底色與字體的「類別」對不對得上選定的 DNA 條目**。
兩者互補：DNA 決定「該長哪一類」，typography-baseline 決定「同一類裡要做到什麼水準」。

用法：

  python scripts/check_dna_fidelity.py <project_path>
  python scripts/check_dna_fidelity.py <project_path> --dna-id DNA-44
  python scripts/check_dna_fidelity.py --selftest-only
"""

import argparse
import io
import json
import math
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DEFAULT_HISTORY = HERE.parent / 'data' / 'design-history.json'
DEFAULT_DNA_REF = HERE.parent / 'references' / 'real-ecommerce-dna.md'

# 這些都是「瀏覽器或框架的預設退路」，不是設計選的字體。
# 取 font-family 第一順位時要跳過，否則會把 Tailwind 預設堆疊裡的 Noto Sans、
# SFMono-Regular 當成這個站的設計字體（實測踩過）。
SYSTEM_STACK = ('-apple-system', 'blinkmacsystemfont', 'segoe ui', 'roboto',
                'system-ui', 'helvetica', 'arial', 'sans-serif', 'serif',
                'monospace', 'ui-sans-serif', 'ui-serif', 'ui-monospace',
                'sfmono', 'menlo', 'monaco', 'consolas', 'liberation mono',
                'courier', 'noto sans', 'noto color emoji', 'apple color emoji',
                'segoe ui emoji', 'segoe ui symbol', 'cantarell', 'oxygen',
                'ubuntu', 'droid sans', 'fira sans', 'emoji',
                'inherit', 'initial', 'unset', 'var(')

# 整條 font-family 全是系統退路時用這個標記。它跟「讀不到」不一樣：
# 讀不到是我們沒本事讀，這個是真的量到了，量到的結果是設計字體沒生效。
SYSTEM_DEFAULT = '（系統預設字體）'

# ─── 顏色 ────────────────────────────────────────────────────────────


def _srgb(c: float) -> int:
    c = 12.92 * c if c <= 0.0031308 else 1.055 * (max(c, 0.0) ** (1 / 2.4)) - 0.055
    return int(round(min(max(c, 0.0), 1.0) * 255))


def oklch_to_hex(L: float, C: float, H: float) -> str:
    h = math.radians(H)
    a, b = C * math.cos(h), C * math.sin(h)
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bl = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    return '#%02x%02x%02x' % (_srgb(r), _srgb(g), _srgb(bl))


def hsl_to_hex(h: float, s: float, l: float) -> str:
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs(((h / 60.0) % 2) - 1))
    m = l - c / 2
    rgb = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][int(h // 60) % 6]
    return '#%02x%02x%02x' % tuple(int(round((v + m) * 255)) for v in rgb)


def to_hex(value: str):
    """把 CSS 顏色字面值轉成 #rrggbb。認不出來就回 None（不猜）。"""
    v = value.strip().lower().rstrip(';').strip()
    m = re.match(r'^#([0-9a-f]{3}|[0-9a-f]{6})$', v)
    if m:
        h = m.group(1)
        return '#' + (''.join(c * 2 for c in h) if len(h) == 3 else h)
    if v in ('white', '#fff'):
        return '#ffffff'
    if v == 'black':
        return '#000000'
    m = re.match(r'^rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)', v)
    if m:
        return '#%02x%02x%02x' % tuple(int(float(g)) for g in m.groups())
    m = re.match(r'^hsla?\(\s*([\d.]+)(?:deg)?[\s,]+([\d.]+)%[\s,]+([\d.]+)%', v)
    if m:
        h, s, light = (float(g) for g in m.groups())
        return hsl_to_hex(h, s / 100.0, light / 100.0)
    m = re.match(r'^oklch\(\s*([\d.]+)(%?)[\s,]+([\d.]+)[\s,]+([\d.]+)', v)
    if m:
        L = float(m.group(1)) / (100.0 if m.group(2) else 1.0)
        return oklch_to_hex(L, float(m.group(3)), float(m.group(4)))
    # shadcn 把 HSL 拆成裸值存在變數裡（--background: 45 60% 97%），用的時候才包 hsl()
    m = re.match(r'^([\d.]+)\s+([\d.]+)%\s+([\d.]+)%$', v)
    if m:
        return hsl_to_hex(float(m.group(1)), float(m.group(2)) / 100.0, float(m.group(3)) / 100.0)
    return None


VAR_RE = re.compile(r'var\(\s*(--[\w-]+)\s*(?:,([^()]*))?\)')


def resolve_value(value: str, varmap: dict, depth: int = 4) -> str:
    """把 var(--x) 換成真正的值。`hsl(var(--background))` 這種寫法不解就什麼都讀不到。"""
    out = value
    for _ in range(depth):
        if 'var(' not in out:
            break
        out = VAR_RE.sub(lambda m: varmap.get(m.group(1), (m.group(2) or '').strip()), out)
    return out.strip()


def is_dark_scope(sel: str) -> bool:
    """深色模式的覆寫區塊。站的預設外觀是淺色那一組，不能拿深色那組來當實際底色。"""
    s = sel.lower()
    return ('.dark' in s or 'data-theme="dark"' in s or "data-theme='dark'" in s
            or 'prefers-color-scheme' in s or '.theme-dark' in s)


def classify_bg(hexcode: str) -> str:
    """四類底色系，與 design_history.py 同一套判準（色度與色相，不用 HSL 飽和度）。"""
    from design_history import classify_hex_tone
    return classify_hex_tone(hexcode)


# ─── 字體分類 ────────────────────────────────────────────────────────

SERIF_TOKENS = ('serif', 'garamond', 'baskerville', 'didot', 'bodoni', 'caslon',
                'playfair', 'times', 'georgia', 'recoleta', 'tiempos', 'canela',
                'freight', 'ogg', 'domaine', 'sectra', 'fraunces', 'newsreader',
                'lora', 'spectral', 'literata', 'prata', 'marcellus', 'petrona',
                'crimson', 'cormorant', 'merriweather', 'source serif', 'noto serif',
                'libre baskerville', 'eb garamond', 'reckless', 'editorial')
SANS_TOKENS = ('sans', 'grotesk', 'grotesque', 'helvetica', 'neue haas', 'akzidenz',
               'univers', 'arial', 'inter', 'archivo', 'poppins', 'montserrat',
               'karla', 'manrope', 'satoshi', 'schibsted', 'figtree', 'outfit',
               'aeonik', 'suisse', 'sohne', 'söhne', 'founders', 'degular',
               'obviously', 'futura', 'avenir', 'gilroy', 'roboto', 'lato',
               'nunito', 'rubik', 'jost', 'urbanist', 'geist', 'diatype',
               'sf pro', 'system font', 'circular', 'sofia', 'quicksand',
               'comfortaa', 'oswald', 'barlow', 'assistant', 'geologica',
               'matter', 'geneva', 'apercu', 'regola', 'aktiv', 'graphik')
MONO_TOKENS = ('mono', 'courier', 'menlo', 'consolas', 'jetbrains')
SLAB_TOKENS = ('slab', 'rockwell', 'zilla', 'gooper')
SCRIPT_TOKENS = ('script', 'hand-drawn', 'handwritten', 'handwriting', 'brush',
                 'caveat', 'sacramento', 'pacifico', 'calligraph')
# 這些形容詞在 DNA 的 Typography 欄位裡固定指「平常的無襯線」
SANS_ADJECTIVES = ('geometric', 'rounded', 'condensed', 'clean', 'standard',
                   'simple', 'readable', 'modern', 'minimal', 'neutral')


def font_class(name: str) -> str:
    n = (name or '').strip().strip('"\'').lower()
    if not n:
        return 'unknown'
    if any(t in n for t in SCRIPT_TOKENS):
        return 'script'
    if any(t in n for t in MONO_TOKENS):
        return 'mono'
    if any(t in n for t in SLAB_TOKENS):
        return 'slab'
    # 先擋掉 sans-serif 這種寫法，免得被當成 serif
    n_nosans = re.sub(r'sans[-\s]?serif', ' sans ', n)
    if any(t in n_nosans for t in SERIF_TOKENS):
        return 'serif'
    if any(t in n_nosans for t in SANS_TOKENS):
        return 'sans'
    return 'unknown'


GENERIC_MAP = (('sans-serif', 'sans'), ('monospace', 'mono'), ('cursive', 'script'),
               ('serif', 'serif'), ('system-ui', 'sans'))


def generic_of(stack: str) -> str:
    """
    整條 font-family 最後那個泛用字族就是作者自己宣告的類別
    （`font-family: Cinzel, "Playfair Display", serif` → serif）。
    名字認不出來的時候用這個，比硬記幾百個字體名可靠。
    """
    low = (stack or '').lower()
    for token, cls in GENERIC_MAP:
        if re.search(r'\b%s\b' % re.escape(token), low):
            return cls
    return 'unknown'


def resolve_class(name: str, stack: str = '') -> str:
    """認得的字體名優先（名字才知道 Fraunces 是襯線），認不得就退回宣告的泛用字族。"""
    cls = font_class(name)
    return cls if cls != 'unknown' else generic_of(stack)


# ─── ① 從編譯後的 CSS 讀實際值 ───────────────────────────────────────

RULE_RE = re.compile(r'([^{}@]+)\{([^{}]*)\}')
BG_VARS = ('--background', '--bg', '--color-background', '--color-bg',
           '--page-bg', '--surface', '--paper', '--body-bg')
DISPLAY_VARS = ('--font-display', '--font-heading', '--heading-font-family',
                '--font-headline', '--font-title')
BODY_VARS = ('--font-body', '--font-sans', '--default-font-family', '--font-base')


def first_family(decl_value: str):
    """取 font-family 的第一順位，跳過系統堆疊與 var() 轉指。"""
    for part in decl_value.split(','):
        p = part.strip().strip('"\'').strip()
        if not p:
            continue
        if any(p.lower().startswith(s) for s in SYSTEM_STACK):
            continue
        return p
    return None


def find_css(project: Path, explicit: str = ''):
    if explicit:
        p = Path(explicit)
        return [p] if p.is_file() else []
    files = sorted((project / 'dist' / 'assets').glob('*.css'))
    if not files:
        files = sorted((project / 'dist').rglob('*.css'))
    if not files:
        files = sorted(project.rglob('*.css'))
        files = [f for f in files if 'node_modules' not in f.parts]
    return files


BODY_CLASS_RE = re.compile(r'<body[^>]*\sclass=["\']([^"\']+)["\']', re.I)
HTML_CLASS_RE = re.compile(r'<html[^>]*\sclass=["\']([^"\']+)["\']', re.I)


def parse_rules(css_text: str):
    """回傳 [(選擇器清單, {屬性: 值})]，照檔案順序。"""
    out = []
    for sel_raw, body in RULE_RE.findall(css_text):
        sels = [' '.join(s.split()).lower() for s in sel_raw.split(',') if s.strip()]
        decls = {}
        for decl in body.split(';'):
            if ':' not in decl:
                continue
            prop, _, val = decl.partition(':')
            decls[prop.strip().lower()] = val.strip()
        if sels and decls:
            out.append((sels, decls))
    return out


def _pick(rules, want_sel, props):
    """
    在符合 want_sel 的規則裡找 props 任一個屬性，回傳 (值, 來源)。
    後面的規則蓋前面的（同選擇器時 CSS 就是靠順序決勝負），深色模式區塊不算。
    """
    hit = None
    for sels, decls in rules:
        if all(is_dark_scope(s) for s in sels):
            continue
        if not any(want_sel(s) for s in sels):
            continue
        for p in props:
            if p in decls:
                hit = (decls[p], '%s { %s }' % (sels[0], p))
    return hit if hit else (None, '')


def build_varmap(rules) -> dict:
    """收集自訂屬性的值。深色模式那組先擱著，淺色沒定義才拿來墊。"""
    light, dark = {}, {}
    for sels, decls in rules:
        target = dark if all(is_dark_scope(s) for s in sels) else light
        for prop, val in decls.items():
            if prop.startswith('--'):
                target[prop] = val
    for k, v in dark.items():
        light.setdefault(k, v)
    return light


def extract_actual(css_text: str, html_text: str = '') -> dict:
    """
    回傳實際的底色與字體。讀不到就留 None，交給呼叫端判 FAIL。

    ⚠️ 真實產出多半不是 `body { background-color }`，而是
    `<body class="bg-obsidian-950 font-sans">` 這種 utility class，
    所以一定要連 HTML 上掛的 class 一起解，否則整支腳本對真的站讀不出東西。
    """
    got = {'bg_hex': None, 'bg_from': '', 'display': None, 'display_from': '',
           'display_stack': '', 'body': None, 'body_from': '', 'body_stack': ''}
    rules = parse_rules(css_text)
    body_classes = []
    for pat in (BODY_CLASS_RE, HTML_CLASS_RE):
        m = pat.search(html_text or '')
        if m:
            body_classes += m.group(1).split()

    def from_classes(props):
        for cls in body_classes:
            val, src = _pick(rules, lambda s, c='.' + cls.lower(): s == c, props)
            if val:
                return val, src
        return None, ''

    varmap = build_varmap(rules)

    def resolve(v):
        return resolve_value(v, varmap)

    # ── 底色 ──
    val, src = _pick(rules, lambda s: s in ('body', 'html', 'html body'),
                     ('background-color', 'background'))
    if val:
        got['bg_hex'], got['bg_from'] = to_hex(resolve(val).split(' url(')[0]), src
    if not got['bg_hex']:
        val, src = from_classes(('background-color', 'background'))
        if val:
            got['bg_hex'], got['bg_from'] = to_hex(resolve(val).split(' url(')[0]), 'body class ' + src
    if not got['bg_hex']:
        val, src = _pick(rules, lambda s: True, BG_VARS)
        if val:
            got['bg_hex'], got['bg_from'] = to_hex(resolve(val)), src

    # ── body 字體（先解，display 的退路要拿它來比對）──
    # ⚠️ 自帶 theme token 的框架（Radix Themes 這類）會用 `.radix-themes { --default-font-family }`
    # 把 body 的字體繼承整條切斷，站內每一段文字都在 <Theme> 裡面。
    # 所以這個 token 存在時它才是實際生效的內文字體，`body { font-family }` 只是擺著好看。
    val, src = _pick(rules, lambda s: True, ('--default-font-family',))
    if val:
        got['body'], got['body_from'], got['body_stack'] = first_family(resolve(val)), src, resolve(val)
        if not got['body']:
            got['body'] = SYSTEM_DEFAULT
    if not got['body']:
        val, src = _pick(rules, lambda s: s in ('body', 'html', 'html body'), ('font-family',))
        if val:
            got['body'], got['body_from'], got['body_stack'] = first_family(resolve(val)), src, val
    if not got['body']:
        val, src = from_classes(('font-family',))
        if val:
            got['body'], got['body_from'], got['body_stack'] = first_family(resolve(val)), 'body class ' + src, val
    if not got['body']:
        val, src = _pick(rules, lambda s: True, BODY_VARS)
        if val:
            got['body'], got['body_from'], got['body_stack'] = first_family(resolve(val)), src, val

    # ── display 字體 ──
    val, src = _pick(rules, lambda s: True, DISPLAY_VARS)
    if val:
        rv = resolve(val)
        got['display'], got['display_from'], got['display_stack'] = first_family(rv), src, rv
        if not got['display'] and re.search(r'-apple-system|system-ui|blinkmac', rv, re.I):
            got['display'] = SYSTEM_DEFAULT
    if not got['display']:
        val, src = _pick(rules, lambda s: bool(re.match(r'^h[1-6]$', s))
                         or s.startswith('.font-display') or s.startswith('.font-heading'),
                         ('font-family',))
        if val:
            got['display'], got['display_from'], got['display_stack'] = first_family(val), src, val
    if not got['display']:
        # Tailwind 這類站的標題字體只存在於 utility class（.font-serif）裡，
        # 沒有 h1 規則也沒有變數。取一個「不是掛在 body 上、而且跟內文字體不同」的字體類 class。
        lower_body_classes = {c.lower() for c in body_classes}
        for sels, decls in rules:
            if 'font-family' not in decls:
                continue
            for s in sels:
                if not s.startswith('.font-') or s[1:] in lower_body_classes:
                    continue
                fam = first_family(decls['font-family'])
                if fam and fam.strip().lower() != (got['body'] or '').strip().lower():
                    got['display'], got['display_from'] = fam, '%s { font-family }' % s
                    got['display_stack'] = decls['font-family']
                    break
            if got['display']:
                break
    return got


# ─── ③ 從 DNA 條目讀規格 ─────────────────────────────────────────────

TONE_KEYWORDS = (
    ('warm-paper', ('cream', 'ivory', 'beige', 'sand', 'oat', 'bone', 'ecru',
                    'off-white', 'off white', 'warm white', 'warm neutral', 'paper',
                    'linen', 'parchment', 'kraft', 'almond', 'greige', 'wheat',
                    'warm grey', 'warm gray', 'eggshell', 'khaki', 'taupe',
                    'stone', 'canvas', 'latte', 'earth', 'clay', 'wood', 'tan',
                    'camel', 'mushroom', 'brown', 'caramel', 'warm')),
    ('cool-white', ('white', 'cool white', 'light neutral', 'pure white', 'neutral base',
                    'light grey', 'light gray', 'cool grey', 'cool gray', 'silver',
                    'monochromatic', 'monochrome', 'greyscale', 'grayscale',
                    'grey', 'gray', 'neutral', 'titanium', 'porcelain')),
    ('dark', ('black', 'charcoal', 'dark', 'noir', 'midnight', 'ink', 'onyx',
              'deep navy', 'navy', 'jet', 'graphite', 'slate', 'monochrome')),
    ('tinted', ('tinted', 'saturated', 'pastel', 'bold color', 'bold colour',
                'vibrant', 'colored base', 'coloured base', 'color block',
                'colour block', 'yellow', 'mint', 'coral', 'teal', 'lavender',
                'chartreuse', 'olive', 'terracotta', 'matcha', 'blue', 'orange',
                'green', 'pink', 'purple', 'red', 'gold', 'sage', 'mauve')),
)
HEX_RE = re.compile(r'#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b')


def dna_block(ref_text: str, dna_id: str):
    m = re.search(r'^###\s+%s:.*?$(.*?)(?=^###\s|\Z)' % re.escape(dna_id),
                  ref_text, re.M | re.S)
    return m.group(1) if m else None


def field(block: str, label: str):
    m = re.search(r'^\-\s+\*\*%s:\*\*\s*(.+)$' % re.escape(label), block, re.M)
    return m.group(1).strip() if m else ''


def _tones_in(text: str):
    low = text.lower()
    tones = [tone for tone, keys in TONE_KEYWORDS if any(k in low for k in keys)]
    if 'off-white' in low or 'off white' in low:
        tones.append('cool-white')
    if not tones:
        tones = [t for t in (classify_bg(h) for h in HEX_RE.findall(text)) if t != 'unknown']
    return list(dict.fromkeys(tones))


def base_segment(color_temp: str):
    """
    有明講底的就只看那一段：整句拿去比對會把『dark gray text』的 dark 算進底色，
    DNA-44 就是這樣被放過的。

    沒明講底的（例如「Warm gold, off-white, soft black」只是列了色盤），
    退回整句，把每一段的色系聯集起來當允許值。這時候判斷會比較寬鬆，
    但那是 DNA 條目本身沒指定底色，不是這支腳本放水。
    """
    segs = [s.strip() for s in re.split(r'[,.;+()/]', color_temp) if s.strip()]
    for s in segs:
        low = s.lower()
        if any(k in low for k in ('base', 'background', 'backdrop', ' bg', 'bg ')):
            return s, True
    return color_temp.strip(), False


def spec_bg_tones(color_temp: str):
    seg, explicit = base_segment(color_temp)
    tones = _tones_in(seg)
    if not explicit and not tones:
        tones = _tones_in(color_temp)
    return tones, seg + ('' if explicit else '（條目沒指定底色，取整句色盤的聯集）')


def spec_font_classes(typography: str):
    low = re.sub(r'sans[-\s]?serif', ' sans ', typography.lower())
    classes = []
    if any(t in low for t in SCRIPT_TOKENS):
        classes.append('script')
    if re.search(r'\bmono\w*', low):
        classes.append('mono')
    if 'slab' in low:
        classes.append('slab')
    if 'serif' in low:
        classes.append('serif')
    if 'sans' in low or 'grotesk' in low or 'grotesque' in low:
        classes.append('sans')
    if any(t in low for t in SANS_ADJECTIVES):
        classes.append('sans')
    for name in re.findall(r'"([^"]+)"', typography):
        c = font_class(name)
        if c != 'unknown':
            classes.append(c)
    for token in re.split(r'[.,()+]', typography):
        c = font_class(token)
        if c != 'unknown':
            classes.append(c)
    return list(dict.fromkeys(classes))


# ─── ② 這個站當初登記選了哪個 DNA ────────────────────────────────────

def lookup_dna(history_path: Path, project: Path, brand: str = '', entry_id=None):
    if not history_path.is_file():
        return None, '找不到歷史檔 %s' % history_path
    data = json.loads(io.open(str(history_path), encoding='utf-8').read())
    rows = data.get('generations', [])
    target = None
    if entry_id is not None:
        target = next((e for e in rows if e.get('id') == entry_id), None)
    elif brand:
        target = next((e for e in reversed(rows)
                       if (e.get('brand') or '').lower() == brand.lower()), None)
    elif project is not None:
        key = project.resolve().name.lower()
        target = next((e for e in reversed(rows)
                       if key and key in (e.get('project_path') or '').lower().replace('\\', '/')), None)
        if target is None:
            target = next((e for e in reversed(rows)
                           if (e.get('brand') or '').lower().replace(' ', '-') == key), None)
    if target is None:
        return None, ('在 %s 裡找不到這個站的登記紀錄。Phase 1.05 選定基因時就該用 '
                      'design_history.py reserve 訂位，沒訂位就無從對照。' % history_path.name)
    dna = target.get('primary_dna') or ''
    if not dna or dna == 'unknown':
        return None, 'id=%s 這筆沒有記主 DNA（primary_dna=%r），對不了' % (target.get('id'), dna)
    return target, ''


# ─── 檢查本體 ────────────────────────────────────────────────────────

def run_check(project: Path, dna_id: str, ref_text: str, css_path=None,
              quiet: bool = False) -> bool:
    def say(msg=''):
        if not quiet:
            print(msg)

    block = dna_block(ref_text, dna_id)
    if block is None:
        say('  FAIL  DNA 條目 %s 在 real-ecommerce-dna.md 裡找不到' % dna_id)
        return False
    color_temp, typography = field(block, 'Color Temp'), field(block, 'Typography')
    want_tones, seg = spec_bg_tones(color_temp)
    want_classes = spec_font_classes(typography)

    files = find_css(project, str(css_path) if css_path else '')
    if not files:
        say('  FAIL  找不到編譯後的 CSS（先跑 npm run build），無法判定就是不通過')
        return False
    css_text = '\n'.join(io.open(str(f), encoding='utf-8', errors='replace').read() for f in files)
    html_text = ''
    for cand in (project / 'dist' / 'index.html', project / 'index.html'):
        if cand.is_file():
            html_text = io.open(str(cand), encoding='utf-8', errors='replace').read()
            break
    actual = extract_actual(css_text, html_text)

    say('  DNA %s 規格：底色「%s」→ %s ；字體「%s」→ %s'
        % (dna_id, seg, '/'.join(want_tones) or '判不出來',
           typography[:60], '/'.join(want_classes) or '判不出來'))

    ok = True

    if not want_tones:
        say('  FAIL  這個 DNA 條目的 Color Temp 寫不出可判定的底色，無法對照 → 視為不通過')
        ok = False
    elif actual['bg_hex'] is None:
        say('  FAIL  編譯後的 CSS 讀不出底色（找不到 body/html 的 background 或 --background）')
        ok = False
    else:
        got_tone = classify_bg(actual['bg_hex'])
        if got_tone in want_tones:
            say('  PASS  底色：規格說 %s、實際是 %s %s（來源 %s）'
                % ('/'.join(want_tones), got_tone, actual['bg_hex'], actual['bg_from']))
        else:
            say('  FAIL  底色：規格說 %s、實際是 %s %s（來源 %s）'
                % ('/'.join(want_tones), got_tone, actual['bg_hex'], actual['bg_from']))
            ok = False

    primary = actual['display'] or actual['body']
    label = 'display' if actual['display'] else 'body'
    primary_stack = actual['display_stack'] if actual['display'] else actual['body_stack']
    if not want_classes:
        say('  FAIL  這個 DNA 條目的 Typography 寫不出可判定的字體類別 → 視為不通過')
        ok = False
    elif not primary:
        say('  FAIL  編譯後的 CSS 讀不出主要字體的第一順位')
        ok = False
    elif primary == SYSTEM_DEFAULT:
        say('  FAIL  字體：規格說 %s、實際是系統預設字體（%s）。'
            '設計字體沒有生效，等於這個站沒有識別；'
            '自帶 theme token 的框架要在框架樣式之後覆寫 --default-font-family'
            % ('/'.join(want_classes), (actual['display_from'] or actual['body_from'])))
        ok = False
    else:
        got_class = resolve_class(primary, primary_stack)
        src = actual['display_from'] or actual['body_from']
        if got_class == 'unknown':
            say('  FAIL  主要字體 %s（%s）認不出是哪一類，判不出來就是不通過' % (primary, label))
            ok = False
        elif got_class in want_classes:
            say('  PASS  字體：規格說 %s、實際是 %s（%s，%s）'
                % ('/'.join(want_classes), got_class, primary, src))
        else:
            say('  FAIL  字體：規格說 %s、實際是 %s（%s，%s）'
                % ('/'.join(want_classes), got_class, primary, src))
            ok = False

    if actual['display'] and actual['body']:
        body_class = resolve_class(actual['body'], actual['body_stack'])
        if want_classes and body_class not in want_classes + ['unknown']:
            say('  註記  body 字體 %s 是 %s，不在規格的 %s 裡；'
                '規格只寫單一類別時，body 走同類別的替代字體'
                % (actual['body'], body_class, '/'.join(want_classes)))
    return ok


# ─── 變異測試：先證明這支腳本抓得到違規 ──────────────────────────────

PLAIN_HTML = '<html><body><div id="root"></div></body></html>'

MUTANTS = {
    # 這一組就是 2026-08-04 那個站：選了 DNA-44 白底粗體無襯線，做成暖紙底＋襯線標題
    'violate_both': ('body{background-color:#f5f3ee;font-family:Archivo,sans-serif}'
                     'h1,h2{font-family:Newsreader,Georgia,serif}', PLAIN_HTML, False),
    'violate_bg':   ('body{background-color:#f3ead6;font-family:"Nimbus Sans",sans-serif}'
                     'h1{font-family:"Nimbus Sans",sans-serif}', PLAIN_HTML, False),
    'violate_font': ('body{background-color:#ffffff;font-family:Archivo,sans-serif}'
                     'h1{font-family:Fraunces,serif}', PLAIN_HTML, False),
    # 真實產出常見寫法：底色與字體掛在 body 的 utility class 上，CSS 裡沒有 body 規則
    'violate_utility': ('.bg-paper{background-color:#f5f3ee}'
                        '.font-serif{font-family:Fraunces,Georgia,serif}',
                        '<html><body class="bg-paper font-serif"></body></html>', False),
    # 內文字體乖乖照規格，標題偷偷換成襯線且只寫在 utility class 裡
    'violate_display_only': ('.bg-white{background-color:#fff}'
                             '.font-sans{font-family:"Nimbus Sans",sans-serif}'
                             '.font-serif{font-family:Newsreader,Georgia,serif}',
                             '<html><body class="bg-white font-sans"></body></html>', False),
    'unreadable':   ('.card{padding:1rem}', PLAIN_HTML, False),
    'compliant':    ('body{background-color:#ffffff;font-family:"Nimbus Sans",sans-serif}'
                     'h1,h2{font-family:"Nimbus Sans",sans-serif}', PLAIN_HTML, True),
    'compliant_oklch': ('body{background-color:oklch(1 0 0);font-family:Archivo,sans-serif}'
                        ':root{--font-display:"Neue Haas Grotesk",sans-serif}',
                        PLAIN_HTML, True),
    'compliant_utility': ('.bg-white{background-color:#fff}'
                          '.font-sans{font-family:"Nimbus Sans",Archivo,sans-serif}',
                          '<html><body class="bg-white font-sans"></body></html>', True),
}


def selftest(ref_text: str) -> bool:
    print('  [自我測試] 造出故意違反 DNA-44 的假樣本，確認抓得到…')
    tmp = Path(tempfile.mkdtemp(prefix='dnafid_'))
    ok = True
    try:
        for name, (css, html, expect_pass) in MUTANTS.items():
            proj = tmp / name
            (proj / 'dist' / 'assets').mkdir(parents=True)
            io.open(str(proj / 'dist' / 'assets' / 'index.css'), 'w', encoding='utf-8').write(css)
            io.open(str(proj / 'dist' / 'index.html'), 'w', encoding='utf-8').write(html)
            got = run_check(proj, 'DNA-44', ref_text, quiet=True)
            good = (got == expect_pass)
            print('    %-18s 期望 %-4s 實得 %-4s  %s'
                  % (name, 'PASS' if expect_pass else 'FAIL',
                     'PASS' if got else 'FAIL', '✓' if good else '✗ 這支腳本沒有偵測能力'))
            if not good:
                ok = False
    finally:
        shutil.rmtree(str(tmp), ignore_errors=True)
        print('    樣本已清除：%s' % (not tmp.exists()))
    return ok


def main():
    parser = argparse.ArgumentParser(description='DNA 忠實度檢查：做出來的東西有沒有照選定的 DNA')
    parser.add_argument('project_path', nargs='?', default='')
    parser.add_argument('--dna-id', default='', help='略過歷史檔查詢，直接指定要對照哪個 DNA')
    parser.add_argument('--brand', default='', help='用品牌名找歷史檔那一筆')
    parser.add_argument('--entry-id', type=int, help='用歷史檔的 id 找那一筆')
    parser.add_argument('--history', default=str(DEFAULT_HISTORY))
    parser.add_argument('--dna-ref', default=str(DEFAULT_DNA_REF))
    parser.add_argument('--css', default='', help='直接指定編譯後的 CSS 檔')
    parser.add_argument('--selftest-only', action='store_true')
    args = parser.parse_args()

    ref_path = Path(args.dna_ref)
    if not ref_path.is_file():
        sys.exit('找不到 DNA 參考檔：%s' % ref_path)
    ref_text = io.open(str(ref_path), encoding='utf-8').read()

    print('=' * 62)
    print('  DNA 忠實度檢查（驗收 A 區 11.6）')
    print('=' * 62)
    print('\n偵測能力自我測試（不通過的話下面的結果不算數）')
    if not selftest(ref_text):
        print('\n中止：這支腳本沒有通過變異測試，本次結果一律不算數。')
        return 2
    if args.selftest_only:
        print('\n（--selftest-only：只跑變異測試）')
        return 0

    if not args.project_path:
        sys.exit('要檢查哪個站？給 project_path。')
    project = Path(args.project_path)
    if not project.is_dir():
        sys.exit('找不到專案目錄：%s' % project)

    dna_id = args.dna_id
    entry = None
    if not dna_id:
        entry, err = lookup_dna(Path(args.history), project, args.brand, args.entry_id)
        if entry is None:
            print('\n檢查：%s' % project)
            print('  FAIL  %s' % err)
            print('\n結論：NOT-READY，不得交付')
            return 1
        dna_id = entry['primary_dna']

    print('\n檢查：%s' % project)
    if entry:
        print('  歷史檔 id=%s（%s）登記的主 DNA 是 %s'
              % (entry.get('id'), entry.get('brand', ''), dna_id))
    ok = run_check(project, dna_id, ref_text, args.css)

    print('\n' + '=' * 62)
    print('  DNA 忠實度：%s' % ('PASS' if ok else 'FAIL，不得交付，要重做'))
    print('=' * 62)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
