"""
Catalog Plates - 生圖失敗時的合格退路（型錄式規格卡）

設計立場：退路不知道商品長什麼樣，所以退路不該假裝畫商品。
它該做的是把「已知為真的規格資料」排版成一張有設計感的型錄規格卡：
材質色票 + 質感紋理 + 規格排版 + 印刷裁切標記。

看起來像刻意設計的品牌型錄頁，不是沒填圖的空白稿。

輸入 JSON 格式：
{
  "palette": {"paper": "#fcf9f1", "bone": "#f4efe3", "ink": "#1f2320", "accent": "#efa807"},
  "output_dir": "public/images/products",
  "items": [
    {
      "code": "14001",
      "name": "QR-38 Arca Plate",
      "sku": "TS-QR38",
      "category": "Rigging",
      "materials": ["6061-T6 aluminium", "Graphite anodised"],
      "specs": [{"label": "Material", "value": "6061-T6 aluminium"}],
      "tags": ["Arca-Swiss", "1/4-20"],
      "weight": "61 g"
    }
  ]
}

用法：
    python scripts/generate_catalog_plates.py --config catalog_plates.json
    python scripts/generate_catalog_plates.py --config catalog_plates.json --size 900
"""

import argparse
import hashlib
import json
import math
import os
import re
from pathlib import Path

# ---------------------------------------------------------------- 材質對照

# 每種材質給一組（亮、暗）色與一種紋理。紋理決定色票裡看到的質感。
MATERIAL_TABLE = [
    # 深色表面處理要排在鋁之前，"graphite anodised" 才會落到深色而不是淺鋁
    (("blackened", "graphite", "matte black", "charcoal", "black"),
     ("#5a5f5b", "#23261f", "brushed")),
    (("aluminium", "aluminum", "6061", "7075", "anodis", "anodiz"),
     ("#d5d8d4", "#8d938c", "brushed")),
    (("brass", "bronze"), ("#e8bf6a", "#a3752a", "brushed")),
    (("copper",), ("#d08a5e", "#8a4a2b", "brushed")),
    (("steel", "stainless", "chrome", "titanium"),
     ("#c3c9cd", "#6f777c", "brushed")),
    # 顏色詞排在金屬之後，避免 "tan" 誤中 "titanium" 這類子字串
    (("tan", "saddle"), ("#c08b57", "#7a4d26", "speckle")),
    (("olive", "od green"), ("#77804f", "#414c2a", "speckle")),
    (("leather", "hide", "suede"), ("#a9754a", "#5d3820", "speckle")),
    (("canvas", "cordura", "nylon", "webbing", "cotton", "twill"),
     ("#6c7a48", "#39421f", "weave")),
    (("wood", "walnut", "oak", "beech", "maple", "ash"),
     ("#a97b4d", "#6b4423", "grain")),
    (("carbon", "microfibre", "microfiber"), ("#7c8280", "#3a3f3c", "dots")),
    (("rubber", "silicone", "tpu", "eva", "foam"),
     ("#4a4f4b", "#232623", "dots")),
    (("glass", "optical", "crystal", "lens", "coated"),
     ("#dfe7e4", "#9fb0ac", "sheen")),
    (("fur", "faux", "windjammer", "acrylic pile"),
     ("#cfc3a8", "#8e8163", "speckle")),
    (("led", "light", "lumen", "diffus"), ("#f4d68d", "#c18f18", "sheen")),
    (("plastic", "abs", "polycarbonate", "resin"),
     ("#c8cbc6", "#7d817c", "dots")),
]

DEFAULT_MATERIAL = ("#c6c2b6", "#7b776c", "brushed")

DEFAULT_PALETTE = {
    "paper": "#fcf9f1",
    "bone": "#f4efe3",
    "ink": "#1f2320",
    "accent": "#efa807",
}


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def match_material(text):
    low = str(text).lower()
    for keys, spec in MATERIAL_TABLE:
        for k in keys:
            if k in low:
                return spec
    return DEFAULT_MATERIAL


def seed_of(value):
    return int(hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:8], 16)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(c1, c2, t):
    a, b = hex_to_rgb(c1), hex_to_rgb(c2)
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ------------------------------------------------------------ 文字寬度估算

# SVG 沒有量測 API，用經驗係數估字寬。寧可估寬一點，讓字不要溢出版面。
WIDTH_FACTOR = {"serif": 0.50, "mono": 0.60, "sans": 0.52}


def text_width(text, size, family="serif"):
    return len(str(text)) * size * WIDTH_FACTOR.get(family, 0.52)


def wrap(text, size, family, max_width, max_lines):
    words = str(text).split()
    lines, current = [], ""
    for w in words:
        trial = (current + " " + w).strip()
        if text_width(trial, size, family) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = w
            if len(lines) == max_lines:
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) == max_lines and len(" ".join(lines)) < len(text.strip()):
        last = lines[-1]
        while last and text_width(last + "...", size, family) > max_width:
            last = last[:-1]
        lines[-1] = last.rstrip() + "..."
    return lines


def fit_size(text, family, max_width, start, minimum):
    size = start
    while size > minimum and text_width(text, size, family) > max_width:
        size -= 1
    return size


# ------------------------------------------------------------------- 紋理

def texture_defs(idx, kind, light, dark, seed):
    """回傳一個 <pattern>，貼在色票上做材質質感。"""
    pid = "tex%d" % idx
    rnd = seed

    def nxt(mod):
        nonlocal rnd
        rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
        return rnd % mod

    if kind == "brushed":
        lines = []
        for x in range(0, 40, 2):
            op = 0.05 + nxt(9) / 100.0
            lines.append(
                '<line x1="%d" y1="0" x2="%d" y2="40" stroke="%s" '
                'stroke-width="1" opacity="%.2f"/>' % (x, x, light, op))
        body = "".join(lines)
        size = 40
    elif kind == "weave":
        body = ('<rect width="12" height="12" fill="none"/>'
                '<line x1="0" y1="0" x2="12" y2="0" stroke="%s" stroke-width="3" opacity="0.22"/>'
                '<line x1="0" y1="6" x2="12" y2="6" stroke="%s" stroke-width="3" opacity="0.16"/>'
                '<line x1="0" y1="0" x2="0" y2="12" stroke="%s" stroke-width="3" opacity="0.20"/>'
                '<line x1="6" y1="0" x2="6" y2="12" stroke="%s" stroke-width="3" opacity="0.14"/>'
                % (light, dark, dark, light))
        size = 12
    elif kind == "grain":
        paths = []
        for i in range(6):
            y = i * 10 + 4
            amp = 2 + nxt(4)
            paths.append(
                '<path d="M0 %d Q 15 %d 30 %d T 60 %d" fill="none" stroke="%s" '
                'stroke-width="1.4" opacity="%.2f"/>'
                % (y, y - amp, y, y, dark, 0.14 + nxt(12) / 100.0))
        body = "".join(paths)
        size = 60
    elif kind == "speckle":
        dots = []
        for _ in range(26):
            dots.append('<circle cx="%d" cy="%d" r="%.1f" fill="%s" opacity="%.2f"/>'
                        % (nxt(30), nxt(30), 0.6 + nxt(12) / 10.0, dark,
                           0.10 + nxt(20) / 100.0))
        body = "".join(dots)
        size = 30
    elif kind == "dots":
        body = ('<circle cx="4" cy="4" r="1.1" fill="%s" opacity="0.30"/>'
                '<circle cx="12" cy="12" r="1.1" fill="%s" opacity="0.22"/>' % (dark, light))
        size = 16
    else:  # sheen
        body = ('<line x1="-10" y1="30" x2="30" y2="-10" stroke="%s" stroke-width="6" opacity="0.16"/>'
                '<line x1="0" y1="40" x2="40" y2="0" stroke="%s" stroke-width="2" opacity="0.22"/>'
                % (light, dark))
        size = 40

    return pid, ('<pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse">%s</pattern>'
                 % (pid, size, size, body))


def grain_layer(seed, size, ink):
    """紙張顆粒。密度低、只在暗處微微可見，用來壓掉 SVG 的塑膠感。"""
    rnd = seed

    def nxt(mod):
        nonlocal rnd
        rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
        return rnd % mod

    out = []
    for _ in range(420):
        out.append('<circle cx="%d" cy="%d" r="%.2f" fill="%s" opacity="%.3f"/>'
                   % (nxt(size), nxt(size), 0.3 + nxt(60) / 100.0, ink,
                      0.015 + nxt(35) / 1000.0))
    return "".join(out)


# ------------------------------------------------------------------ 主繪製

def build_plate(item, palette, size=900):
    paper = palette.get("paper", DEFAULT_PALETTE["paper"])
    bone = palette.get("bone", DEFAULT_PALETTE["bone"])
    ink = palette.get("ink", DEFAULT_PALETTE["ink"])
    accent = palette.get("accent", DEFAULT_PALETTE["accent"])

    seed = seed_of(item.get("sku") or item.get("code") or item.get("name"))
    m = size / 900.0  # 版面按 900 設計，其他尺寸等比縮放

    def s(v):
        return round(v * m, 1)

    pad = s(58)
    inner = size - pad * 2

    serif = "Fraunces, Georgia, 'Times New Roman', serif"
    mono = "'IBM Plex Mono', ui-monospace, 'Consolas', monospace"

    defs, body = [], []

    # ---- 底：紙色 + 顆粒
    body.append('<rect width="%d" height="%d" fill="%s"/>' % (size, size, paper))
    body.append('<g>%s</g>' % grain_layer(seed, size, ink))

    # ---- 印刷裁切標記（四角），型錄印刷感的來源
    cm, off = s(20), s(26)
    for cx, cy, dx, dy in ((off, off, 1, 1), (size - off, off, -1, 1),
                           (off, size - off, 1, -1), (size - off, size - off, -1, -1)):
        body.append('<path d="M%s %s h%s M%s %s v%s" stroke="%s" stroke-width="1" '
                    'opacity="0.30" fill="none"/>'
                    % (cx, cy, s(20) * dx, cx, cy, s(20) * dy, ink))

    # ---- 版框
    body.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" '
                'stroke-width="1" opacity="0.16"/>' % (pad, pad, inner, inner, ink))

    # ---- 頁首：分類 / 料號
    head_y = pad + s(38)
    category = str(item.get("category") or "Catalogue").upper()
    sku = str(item.get("sku") or item.get("code") or "")
    body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" letter-spacing="%s" '
                'fill="%s" opacity="0.62">%s</text>'
                % (pad + s(22), head_y, mono, s(15), s(3.4), ink, esc(category)))
    if sku:
        body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" letter-spacing="%s" '
                    'text-anchor="end" fill="%s" opacity="0.62">%s</text>'
                    % (size - pad - s(22), head_y, mono, s(15), s(2.4), ink, esc(sku)))
    rule_y = pad + s(58)
    body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1" opacity="0.16"/>'
                % (pad + s(22), rule_y, size - pad - s(22), rule_y, ink))

    # ---- 品名（襯線大字，最多兩行，寬度不足時自動降級字級）
    tx = pad + s(22)
    tw = inner - s(44)
    name = str(item.get("name") or "")
    n_size = fit_size(name, "serif", tw * 1.9, s(52), s(30))
    lines = wrap(name, n_size, "serif", tw, 2)
    ty = rule_y + s(62)
    for i, ln in enumerate(lines):
        body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s">%s</text>'
                    % (tx, ty + i * n_size * 1.14, serif, n_size, ink, esc(ln)))

    tags = [t for t in (item.get("tags") or []) if t]
    tag_y = ty + len(lines) * n_size * 1.14 + s(12)
    if tags:
        body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" letter-spacing="%s" '
                    'fill="%s" opacity="0.55">%s</text>'
                    % (tx, tag_y, mono, s(14), s(2.2), ink,
                       esc(" / ".join(str(t).upper() for t in tags[:4]))))

    # ---- 材質色票帶：每格是一種真實材質或表面處理
    materials = [x for x in (item.get("materials") or []) if x][:4]
    if not materials:
        for sp in (item.get("specs") or []):
            if str(sp.get("label", "")).lower() in ("material", "materials", "finish", "body"):
                materials.append(sp.get("value"))
        materials = materials[:4] or ["Composite"]

    sw_top = tag_y + s(30)
    sw_h = s(238)
    gap = s(10)
    count = len(materials)
    sw_w = (tw - gap * (count - 1)) / count

    for i, mat in enumerate(materials):
        light, dark, kind = match_material(mat)
        pid, pattern = texture_defs(i, kind, light, dark, seed + i * 977)
        gid = "grad%d" % i
        defs.append(pattern)
        defs.append(
            '<linearGradient id="%s" x1="0" y1="0" x2="0.35" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient>'
            % (gid, mix(light, "#ffffff", 0.28), light, dark))

        x = tx + i * (sw_w + gap)
        body.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>'
                    % (x, sw_top, sw_w, sw_h, gid))
        body.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>'
                    % (x, sw_top, sw_w, sw_h, pid))
        # 上緣高光與下緣陰影，讓色票有實體厚度而不是平色塊
        body.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#ffffff" opacity="0.30"/>'
                    % (x, sw_top, sw_w, s(2)))
        body.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" opacity="0.22"/>'
                    % (x, sw_top + sw_h - s(3), sw_w, s(3), ink))
        body.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" '
                    'stroke-width="1" opacity="0.22"/>' % (x, sw_top, sw_w, sw_h, ink))

        # 色票編號壓在左上角
        body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" opacity="0.70">'
                    '%02d</text>' % (x + s(10), sw_top + s(22), mono, s(13), paper, i + 1))

        cap = str(mat).upper()
        c_size = fit_size(cap, "mono", sw_w, s(12.5), s(8))
        body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" letter-spacing="%s" '
                    'fill="%s" opacity="0.68">%s</text>'
                    % (x, sw_top + sw_h + s(20), mono, c_size, s(1.1), ink, esc(cap)))

    # 色票帶右緣的品牌重點色，整張唯一的彩度
    body.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>'
                % (tx, sw_top + sw_h + s(32), s(46), s(4), accent))

    # ---- 規格表：真實資料，虛線引導
    specs = [sp for sp in (item.get("specs") or []) if sp.get("label")][:5]
    sp_y = sw_top + sw_h + s(70)
    row_h = s(31)
    for i, sp in enumerate(specs):
        y = sp_y + i * row_h
        label = str(sp.get("label", "")).upper()
        value = str(sp.get("value", ""))
        v_size = fit_size(value, "mono", tw * 0.60, s(15), s(10))
        body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" letter-spacing="%s" '
                    'fill="%s" opacity="0.52">%s</text>'
                    % (tx, y, mono, s(13), s(1.6), ink, esc(label)))
        body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" text-anchor="end" '
                    'fill="%s" opacity="0.88">%s</text>'
                    % (tx + tw, y, mono, v_size, ink, esc(value)))
        body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1" '
                    'stroke-dasharray="1 4" opacity="0.28"/>'
                    % (tx, y + s(5), tx + tw, y + s(5), ink))

    # ---- 商品短述：型錄卡下半的內容，避免大片留白
    note = str(item.get("note") or "").strip()
    bar_top = size - pad - s(78)  # 比例尺位置，短述不可壓到
    n_y = sp_y + len(specs) * row_h + s(26)
    max_note_lines = max(0, min(3, int((bar_top - s(34) - n_y) / s(26)) + 1))
    if note and max_note_lines:
        for i, ln in enumerate(wrap(note, s(17), "serif", tw * 1.04, max_note_lines)):
            body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" '
                        'opacity="0.72">%s</text>'
                        % (tx, n_y + i * s(26), serif, s(17), ink, esc(ln)))

    # ---- 公制比例尺：技術型錄語言，證明這張卡是刻意的規格頁
    bar_y = bar_top
    bar_w = s(240)  # 代表 60 mm
    body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.4" '
                'opacity="0.55"/>' % (tx, bar_y, tx + bar_w, bar_y, ink))
    for i in range(7):
        x = tx + bar_w * i / 6.0
        tall = s(9) if i % 3 == 0 else s(5)
        body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.2" '
                    'opacity="0.55"/>' % (x, bar_y, x, bar_y - tall, ink))
    for mm, frac in ((0, 0.0), (30, 0.5), (60, 1.0)):
        body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" text-anchor="middle" '
                    'fill="%s" opacity="0.50">%d</text>'
                    % (tx + bar_w * frac, bar_y - s(15), mono, s(11), ink, mm))
    body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" letter-spacing="%s" '
                'fill="%s" opacity="0.50">SCALE MM</text>'
                % (tx + bar_w + s(16), bar_y - s(2), mono, s(11), s(1.8), ink))

    # ---- 頁尾
    foot_y = size - pad - s(24)
    body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1" opacity="0.16"/>'
                % (tx, foot_y - s(24), tx + tw, foot_y - s(24), ink))
    left_foot = item.get("footer_left") or ("REF %s" % (item.get("code") or sku or ""))
    right_foot = item.get("weight") or item.get("footer_right") or ""
    body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" letter-spacing="%s" '
                'fill="%s" opacity="0.50">%s</text>'
                % (tx, foot_y, mono, s(13), s(2.2), ink, esc(str(left_foot).upper())))
    if right_foot:
        body.append('<text x="%s" y="%s" font-family="%s" font-size="%s" letter-spacing="%s" '
                    'text-anchor="end" fill="%s" opacity="0.50">%s</text>'
                    % (tx + tw, foot_y, mono, s(13), s(2.2), ink, esc(str(right_foot).upper())))

    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
           'role="img" aria-label="%s"><title>%s</title><defs>%s</defs>%s</svg>'
           % (size, size, size, size, esc(name), esc(name), "".join(defs), "".join(body)))
    return svg


# ------------------------------------------------------------------- 入口

# ================================================================ 橫幅／封面
# hero 與分類封面走「工程製圖」語言：零件視圖 + 尺寸標註 + 剖面線 + 圖號 + 標題欄。
# 商品卡是排版，這裡是製圖；共通的是紙感、裁切標記、單一彩度 accent。

MONO = "'IBM Plex Mono', ui-monospace, 'Consolas', monospace"
SERIF = "Fraunces, Georgia, 'Times New Roman', serif"


def _ln(p, x1, y1, x2, y2, ink, w=1.6, op=0.85, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
             'stroke-width="%.2f" opacity="%.2f"%s/>' % (x1, y1, x2, y2, ink, w, op, d))


def _txt(p, x, y, text, ink, size=13, anchor="start", ls=1.6, op=0.6, font=MONO):
    p.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" letter-spacing="%.1f" '
             'text-anchor="%s" fill="%s" opacity="%.2f">%s</text>'
             % (x, y, font, size, ls, anchor, ink, op, esc(text)))


def _centerline(p, x1, y1, x2, y2, ink):
    _ln(p, x1, y1, x2, y2, ink, 1.0, 0.45, "16 5 3 5")


def dim_h(p, x1, x2, y, label, ink):
    """水平尺寸標註：端點延伸線 + 斜割線 + 置中標籤。"""
    for x in (x1, x2):
        _ln(p, x, y - 7, x, y + 7, ink, 1.2, 0.7)
        _ln(p, x - 4, y + 4, x + 4, y - 4, ink, 1.2, 0.7)
    _ln(p, x1, y, x2, y, ink, 1.2, 0.7)
    _txt(p, (x1 + x2) / 2, y - 8, label, ink, 13, "middle", 1.4, 0.75)


def dim_v(p, x, y1, y2, label, ink):
    for y in (y1, y2):
        _ln(p, x - 7, y, x + 7, y, ink, 1.2, 0.7)
        _ln(p, x - 4, y + 4, x + 4, y - 4, ink, 1.2, 0.7)
    _ln(p, x, y1, x, y2, ink, 1.2, 0.7)
    _txt(p, x + 10, (y1 + y2) / 2 + 4, label, ink, 13, "start", 1.4, 0.75)


def hatch_def(ink):
    return ('<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" '
            'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="%s" '
            'stroke-width="1" opacity="0.5"/></pattern>' % ink)


def _rrect(p, x, y, w, h, r, ink, sw=1.8, fill="none", op=0.9):
    p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" '
             'stroke="%s" stroke-width="%.2f" opacity="%.2f"/>' % (x, y, w, h, r, fill, ink, sw, op))


def _circ(p, cx, cy, r, ink, sw=1.8, fill="none", op=0.9):
    p.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%.2f" '
             'opacity="%.2f"/>' % (cx, cy, r, fill, ink, sw, op))


def _knurl_ring(p, cx, cy, r, ink, n=48, tick=6):
    for i in range(n):
        a = 2 * math.pi * i / n
        _ln(p, cx + r * math.cos(a), cy + r * math.sin(a),
            cx + (r - tick) * math.cos(a), cy + (r - tick) * math.sin(a), ink, 1.0, 0.55)


# ---- 零件視圖庫：每個 motif 畫進 (x, y, w, h) 的框，回傳圖名供 FIG 標籤用

def motif_arca_plate(p, x, y, w, h, ink, accent):
    bw, bh = w * 0.92, min(h * 0.62, w * 0.42)
    bx, by = x + (w - bw) / 2, y + (h - bh) / 2
    _rrect(p, bx, by, bw, bh, 8, ink, 2.2)
    for inset in (7, 13):  # 燕尾導緣
        _ln(p, bx + inset, by + inset, bx + bw - inset, by + inset, ink, 1.1, 0.6)
        _ln(p, bx + inset, by + bh - inset, bx + bw - inset, by + bh - inset, ink, 1.1, 0.6)
    for i in range(3):  # 螺孔
        cx = bx + bw * (0.25 + 0.25 * i)
        cy = by + bh / 2
        _circ(p, cx, cy, bh * 0.14, ink, 1.8)
        _ln(p, cx - bh * 0.09, cy, cx + bh * 0.09, cy, ink, 1.6, 0.8)
    _circ(p, bx + bw * 0.5, by + bh / 2, bh * 0.14 + 5, accent, 1.4, "none", 0.9)
    _centerline(p, bx - 16, by + bh / 2, bx + bw + 16, by + bh / 2, ink)
    _centerline(p, bx + bw / 2, by - 14, bx + bw / 2, by + bh + 14, ink)
    dim_v(p, bx + bw + 26, by, by + bh, "38", ink)
    dim_h(p, bx, bx + bw, by + bh + 28, "70 MM", ink)
    return "QR PLATE / TOP"


def motif_dovetail_section(p, x, y, w, h, ink, accent):
    bw = w * 0.8
    bh = min(h * 0.5, bw * 0.36)
    bx, by = x + (w - bw) / 2, y + (h - bh) / 2
    t = bh * 0.9
    pth = ("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z"
           % (bx + t * 0.6, by, bx + bw - t * 0.6, by, bx + bw, by + bh, bx, by + bh))
    p.append('<path d="%s" fill="url(#hatch)" stroke="%s" stroke-width="2.0" opacity="0.9"/>'
             % (pth, ink))
    _ln(p, bx - 14, by + bh, bx + bw + 14, by + bh, ink, 2.0, 0.9)
    dim_h(p, bx + t * 0.6, bx + bw - t * 0.6, by - 16, "38 MM", ink)
    _txt(p, bx + bw + 10, by + bh - 4, "45°", ink, 12, "start", 1.0, 0.7)
    return "DOVETAIL / SECTION A-A"


def motif_magic_arm(p, x, y, w, h, ink, accent):
    cx, cy = x + w / 2, y + h * 0.42
    r_j = min(w, h) * 0.075
    ends = [(x + w * 0.12, y + h * 0.82), (x + w * 0.88, y + h * 0.82)]
    for ex, ey in ends:
        ang = math.atan2(ey - cy, ex - cx)
        d = math.hypot(ex - cx, ey - cy)
        ux, uy = (ex - cx) / d, (ey - cy) / d
        sx0, sy0 = cx + ux * r_j * 1.25, cy + uy * r_j * 1.25  # 從中心圓邊緣起筆
        ex0, ey0 = ex - ux * r_j, ey - uy * r_j
        ox, oy = math.sin(ang) * r_j * 0.55, -math.cos(ang) * r_j * 0.55
        for sgn in (1, -1):
            _ln(p, sx0 + ox * sgn, sy0 + oy * sgn, ex0 + ox * sgn, ey0 + oy * sgn, ink, 2.2, 0.9)
        _circ(p, ex, ey, r_j, ink, 2.2)
        _circ(p, ex, ey, r_j * 0.4, ink, 1.4)
    _circ(p, cx, cy, r_j * 1.25, ink, 2.2)
    _ln(p, cx, cy - r_j * 1.25, cx, cy - r_j * 2.6, accent, 3.2, 0.95)  # 鎖桿
    _circ(p, cx, cy - r_j * 2.9, r_j * 0.38, accent, 2.0)
    _centerline(p, ends[0][0], ends[0][1], cx, cy, ink)
    _centerline(p, cx, cy, ends[1][0], ends[1][1], ink)
    dim_h(p, ends[0][0], ends[1][0], y + h * 0.98, "178 MM CENTRES", ink)
    return "ARTICULATING ARM / ELEVATION"


def motif_clamp(p, x, y, w, h, ink, accent):
    s_ = min(w, h)
    cx, cy = x + w / 2, y + h * 0.42
    r_o, r_i = s_ * 0.33, s_ * 0.2
    # C 形鉗口：開口朝右
    p.append('<path d="M%.1f %.1f A%.1f %.1f 0 1 0 %.1f %.1f" fill="none" stroke="%s" '
             'stroke-width="2.4" opacity="0.9"/>'
             % (cx + r_o * 0.7, cy - r_o * 0.72, r_o, r_o, cx + r_o * 0.7, cy + r_o * 0.72, ink))
    p.append('<path d="M%.1f %.1f A%.1f %.1f 0 1 0 %.1f %.1f" fill="none" stroke="%s" '
             'stroke-width="1.6" opacity="0.7"/>'
             % (cx + r_i * 0.6, cy - r_i * 0.8, r_i, r_i, cx + r_i * 0.6, cy + r_i * 0.8, ink))
    # 鎖緊螺桿（下方進入），螺紋短斜線
    sx = cx - r_o * 0.15
    _ln(p, sx, cy + r_o * 0.9, sx, cy + r_o * 1.3, ink, 2.2, 0.9)
    for i in range(5):
        yy = cy + r_o * (0.95 + 0.07 * i)
        _ln(p, sx - 5, yy + 3, sx + 5, yy - 3, ink, 1.1, 0.6)
    _circ(p, sx, cy + r_o * 1.42, s_ * 0.055, accent, 2.0)
    dim_v(p, cx + r_o * 0.95, cy - r_i * 0.8, cy + r_i * 0.8, "10-60", ink)
    return "GRIP CLAMP / JAW"


def motif_filter_ring(p, x, y, w, h, ink, accent):
    r = min(w, h) * 0.42
    cx, cy = x + w / 2, y + h / 2
    _circ(p, cx, cy, r, ink, 2.4)
    _knurl_ring(p, cx, cy, r, ink, 72, r * 0.07)
    _circ(p, cx, cy, r * 0.82, ink, 1.6)
    _circ(p, cx, cy, r * 0.74, ink, 1.2, "none", 0.6)
    p.append('<path d="M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f" fill="none" stroke="%s" '
             'stroke-width="2" opacity="0.35"/>'
             % (cx - r * 0.45, cy - r * 0.28, r * 0.55, r * 0.55, cx - r * 0.05, cy - r * 0.52, ink))
    _centerline(p, cx - r - 14, cy, cx + r + 14, cy, ink)
    _centerline(p, cx, cy - r - 14, cx, cy + r + 14, ink)
    dim_h(p, cx - r, cx + r, cy + r + 26, "Ø 67 MM", ink)
    _txt(p, cx + r * 0.72, cy - r * 0.72, "M67 x 0.75", ink, 12, "start", 1.0, 0.7)
    return "UV FILTER / FRONT"


def motif_lens_cap(p, x, y, w, h, ink, accent):
    r = min(w, h) * 0.38
    cx, cy = x + w / 2, y + h / 2
    _circ(p, cx, cy, r, ink, 2.2)
    _knurl_ring(p, cx, cy, r, ink, 60, r * 0.1)
    _circ(p, cx, cy, r * 0.62, ink, 1.4, "none", 0.7)
    _circ(p, cx, cy, r * 0.1, accent, 1.6)
    _centerline(p, cx - r - 12, cy, cx + r + 12, cy, ink)
    return "MACHINED CAP / FRONT"


def motif_soft_release(p, x, y, w, h, ink, accent):
    s_ = min(w, h)
    cx, cy = x + w / 2, y + h * 0.4
    r = s_ * 0.24
    _circ(p, cx, cy, r, ink, 2.2)
    p.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" '
             'stroke-width="1.6" opacity="0.7"/>'
             % (cx - r * 0.6, cy - r * 0.1, cx, cy + r * 0.35, cx + r * 0.6, cy - r * 0.1, ink))
    sx = cx
    _ln(p, sx, cy + r, sx, cy + r + s_ * 0.3, ink, 2.4, 0.9)
    for i in range(5):
        yy = cy + r + s_ * 0.05 * (i + 1)
        _ln(p, sx - 6, yy + 3, sx + 6, yy - 3, ink, 1.1, 0.6)
    dim_h(p, cx - r, cx + r, cy - r - 14, "11 MM", ink)
    return "SOFT RELEASE / SECTION"


def motif_strap(p, x, y, w, h, ink, accent):
    bx, by, bw, bh = x + w * 0.08, y + h * 0.18, w * 0.84, h * 0.6
    p.append('<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" fill="none" stroke="%s" '
             'stroke-width="14" opacity="0.85" stroke-linecap="round"/>'
             % (bx, by + bh * 0.75, bx + bw * 0.3, by - bh * 0.35,
                bx + bw * 0.7, by - bh * 0.35, bx + bw, by + bh * 0.75, ink))
    p.append('<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" fill="none" stroke="%s" '
             'stroke-width="1.2" opacity="0.9" stroke-dasharray="5 4"/>'
             % (bx, by + bh * 0.75, bx + bw * 0.3, by - bh * 0.35,
                bx + bw * 0.7, by - bh * 0.35, bx + bw, by + bh * 0.75, "#fcf9f1"))
    _circ(p, bx + bw, by + bh * 0.82, min(w, h) * 0.09, ink, 2.4)
    _circ(p, bx, by + bh * 0.82, min(w, h) * 0.055, accent, 2.0)
    _txt(p, x + w / 2, y + h * 0.98, "3.5 MM VEG TAN", ink, 12, "middle", 1.4, 0.6)
    return "WRIST STRAP / SADDLE STITCH"


def motif_card_case(p, x, y, w, h, ink, accent):
    bw, bh = w * 0.8, min(h * 0.7, w * 0.56)
    bx, by = x + (w - bw) / 2, y + (h - bh) / 2
    _rrect(p, bx, by, bw, bh, 10, ink, 2.2)
    _rrect(p, bx + 8, by + 8, bw - 16, bh - 16, 6, ink, 1.1, "none", 0.5)  # 防水墊圈線
    cols, rows = 3, 2
    for r_ in range(rows):
        for c_ in range(cols):
            sw_ = (bw - 40 - (cols - 1) * 10) / cols
            sh_ = (bh - 40 - (rows - 1) * 10) / rows
            _rrect(p, bx + 20 + c_ * (sw_ + 10), by + 20 + r_ * (sh_ + 10), sw_, sh_, 4,
                   ink, 1.3, "none", 0.65)
    _rrect(p, bx + 20, by + 20, (bw - 60) / 3, (bh - 50) / 2, 4, accent, 1.5, "none", 0.9)
    dim_h(p, bx, bx + bw, by + bh + 24, "98 MM", ink)
    return "CARD VAULT / PLAN"


def motif_fill_light(p, x, y, w, h, ink, accent):
    bw, bh = w * 0.66, min(h * 0.72, w * 0.46)
    bx, by = x + (w - bw) / 2, y + (h - bh) / 2
    _rrect(p, bx, by, bw, bh, 10, ink, 2.2)
    for i in range(1, 6):
        _ln(p, bx + bw * i / 6, by + 6, bx + bw * i / 6, by + bh - 6, ink, 0.9, 0.4)
    for i in range(1, 4):
        _ln(p, bx + 6, by + bh * i / 4, bx + bw - 6, by + bh * i / 4, ink, 0.9, 0.4)
    dial_r = min(w, h) * 0.055
    dial_x = bx + bw + dial_r * 1.7
    _circ(p, dial_x, by + bh / 2, dial_r, accent, 2.0)
    _knurl_ring(p, dial_x, by + bh / 2, dial_r, accent, 20, 3)
    dim_h(p, bx, bx + bw, by + bh + 24, "120 MM", ink)
    return "POCKET LIGHT / FACE"


def motif_windjammer(p, x, y, w, h, ink, accent):
    r = min(w, h) * 0.3
    cx, cy = x + w / 2, y + h * 0.42
    rnd = seed_of("wind")
    for i in range(64):
        a = 2 * math.pi * i / 64
        rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
        ext = r * (0.16 + (rnd % 100) / 700.0)
        _ln(p, cx + r * math.cos(a), cy + r * math.sin(a),
            cx + (r + ext) * math.cos(a), cy + (r + ext) * math.sin(a), ink, 1.0, 0.55)
    _circ(p, cx, cy, r, ink, 1.4, "none", 0.5)
    _rrect(p, cx - r * 0.3, cy + r * 1.32, r * 0.6, r * 0.45, 4, ink, 1.8)
    dim_h(p, cx - r, cx + r, cy + r * 1.98, "Ø 90 MM", ink)
    return "WINDJAMMER / PROFILE"


def motif_screw(p, x, y, w, h, ink, accent):
    s_ = min(w, h)
    cx, cy = x + w / 2, y + h * 0.3
    hw, hh = s_ * 0.3, s_ * 0.16
    _rrect(p, cx - hw / 2, cy, hw, hh, 3, ink, 2.0)
    for i in range(1, 6):
        _ln(p, cx - hw / 2 + hw * i / 6, cy + 2, cx - hw / 2 + hw * i / 6, cy + hh - 2,
            ink, 0.9, 0.5)
    sw_ = s_ * 0.14
    _ln(p, cx - sw_ / 2, cy + hh, cx - sw_ / 2, cy + hh + s_ * 0.36, ink, 1.8, 0.9)
    _ln(p, cx + sw_ / 2, cy + hh, cx + sw_ / 2, cy + hh + s_ * 0.36, ink, 1.8, 0.9)
    for i in range(7):
        yy = cy + hh + s_ * 0.05 * (i + 0.5)
        _ln(p, cx - sw_ / 2 - 2, yy + 4, cx + sw_ / 2 + 2, yy - 4, ink, 1.1, 0.65)
    _ln(p, cx - sw_ / 2 - 2, cy + hh + s_ * 0.36, cx + sw_ / 2 + 2, cy + hh + s_ * 0.36,
        ink, 1.8, 0.9)
    _txt(p, cx, cy + hh + s_ * 0.5, "1/4-20 UNC", ink, 12, "middle", 1.2, 0.7)
    return "ADAPTER SCREW / SIDE"


def motif_pen(p, x, y, w, h, ink, accent):
    bw, bh = w * 0.72, min(h * 0.24, w * 0.16)
    bx, by = x + (w - bw) / 2, y + (h - bh) / 2
    _rrect(p, bx, by, bw, bh, bh / 2, ink, 2.0)
    _ln(p, bx + bw * 0.62, by, bx + bw * 0.62, by + bh, ink, 1.4, 0.7)
    p.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="none" stroke="%s" '
             'stroke-width="1.8" opacity="0.85"/>'
             % (bx + bw, by + bh * 0.2, bx + bw + bh * 0.9, by + bh / 2,
                bx + bw, by + bh * 0.8, ink))
    _ln(p, bx + bw * 0.08, by + bh / 2, bx + bw * 0.2, by + bh / 2, accent, 3.0, 0.9)
    dim_h(p, bx, bx + bw + bh * 0.9, by + bh + 20, "112 MM", ink)
    return "CLEANING PEN / SIDE"


def motif_tripod(p, x, y, w, h, ink, accent):
    cx = x + w / 2
    top = y + h * 0.12
    base = y + h * 0.88
    _circ(p, cx, top, min(w, h) * 0.07, ink, 2.2)
    _circ(p, cx, top, min(w, h) * 0.032, accent, 1.6)
    _rrect(p, cx - 7, top + min(w, h) * 0.07, 14, h * 0.12, 3, ink, 1.8)
    for dx in (-1, 0, 1):
        ex = cx + dx * w * 0.3
        _ln(p, cx, top + min(w, h) * 0.07 + h * 0.12, ex, base, ink, 2.0, 0.85)
        _ln(p, ex - 8, base, ex + 8, base, ink, 2.0, 0.85)
    dim_h(p, cx - w * 0.3, cx + w * 0.3, base + 22, "130 MM FOLDED", ink)
    return "POCKET TRIPOD / ELEVATION"


MOTIFS = {
    "arca_plate": motif_arca_plate, "dovetail_section": motif_dovetail_section,
    "magic_arm": motif_magic_arm, "clamp": motif_clamp, "filter_ring": motif_filter_ring,
    "lens_cap": motif_lens_cap, "soft_release": motif_soft_release, "strap": motif_strap,
    "card_case": motif_card_case, "fill_light": motif_fill_light,
    "windjammer": motif_windjammer, "screw": motif_screw, "pen": motif_pen,
    "tripod": motif_tripod,
}


def _sheet_base(body, W, H, palette, seed):
    paper, ink = palette["paper"], palette["ink"]
    body.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, paper))
    for i in range(1, 10):  # 工程紙的橫細線
        yy = H * i / 10
        body.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1" '
                    'opacity="0.05"/>' % (yy, W, yy, ink))
    body.append('<g>%s</g>' % grain_layer(seed, max(W, H), ink))
    off = 24
    for cx, cy, dx, dy in ((off, off, 1, 1), (W - off, off, -1, 1),
                           (off, H - off, 1, -1), (W - off, H - off, -1, -1)):
        body.append('<path d="M%s %s h%s M%s %s v%s" stroke="%s" stroke-width="1" '
                    'opacity="0.30" fill="none"/>' % (cx, cy, 18 * dx, cx, cy, 18 * dy, ink))


def _title_block(body, x, y, w, ink, rows):
    """工程圖標題欄：右下角的小表格。"""
    rh = 26
    h = rh * len(rows)
    body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" '
                'stroke-width="1.2" opacity="0.5"/>' % (x, y, w, h, ink))
    p = []
    for i, (label, value) in enumerate(rows):
        yy = y + rh * i
        if i:
            _ln(p, x, yy, x + w, yy, ink, 1.0, 0.4)
        _txt(p, x + 10, yy + 17, label, ink, 10, "start", 1.6, 0.5)
        _txt(p, x + w - 10, yy + 17, value, ink, 11, "end", 1.0, 0.75)
    _ln(p, x + w * 0.38, y, x + w * 0.38, y + h, ink, 1.0, 0.4)
    body.extend(p)


def build_banner(item, palette, W, H):
    """hero 橫幅：大型零件製圖 + 副視圖 + 標題欄。疏朗、線多字少。"""
    ink = palette["ink"]
    accent = palette["accent"]
    seed = seed_of(item.get("file") or item.get("title") or "banner")
    defs = [hatch_def(ink)]
    body = []
    _sheet_base(body, W, H, palette, seed)

    motifs = [m for m in (item.get("motifs") or []) if m in MOTIFS][:3]
    figs = []
    if len(motifs) == 1:
        boxes = [(W * 0.18, H * 0.16, W * 0.64, H * 0.6)]
    elif len(motifs) == 2:
        boxes = [(W * 0.08, H * 0.14, W * 0.5, H * 0.62), (W * 0.62, H * 0.2, W * 0.3, H * 0.5)]
    else:
        boxes = [(W * 0.06, H * 0.12, W * 0.46, H * 0.64),
                 (W * 0.57, H * 0.08, W * 0.36, H * 0.4),
                 (W * 0.56, H * 0.52, W * 0.26, H * 0.28)]
    for (bx, by, bw, bh), name in zip(boxes, motifs):
        cap = MOTIFS[name](body, bx, by, bw, bh, ink, accent)
        figs.append(cap)
        _txt(body, bx + bw / 2, by + bh + 34, "FIG %02d · %s" % (len(figs), cap),
             ink, 12, "middle", 2.0, 0.55)

    tb_w = min(300, W * 0.24)
    _title_block(body, W - tb_w - 44, H - 26 * 3 - 40, tb_w, ink, [
        ("DRAWN", str(item.get("brand") or "THIRDSTOP SUPPLY")),
        ("SHEET", str(item.get("sheet") or "01")),
        ("SCALE", "1 : 1 MM"),
    ])
    if item.get("title"):
        _txt(body, 48, H - 44, str(item["title"]).upper(), ink, 14, "start", 3.0, 0.6)

    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
            'role="img" aria-label="%s"><title>%s</title><defs>%s</defs>%s</svg>'
            % (W, H, W, H, esc(item.get("title") or ""), esc(item.get("title") or ""),
               "".join(defs), "".join(body)))


def build_cover(item, palette, W, H):
    """分類封面：品類代表零件 2-3 件排排站 + 左緣 accent 條 + 品類名。"""
    ink = palette["ink"]
    accent = palette["accent"]
    seed = seed_of(item.get("file") or item.get("title") or "cover")
    defs = [hatch_def(ink)]
    body = []
    _sheet_base(body, W, H, palette, seed)
    body.append('<rect x="0" y="0" width="14" height="%d" fill="%s"/>' % (H, accent))

    motifs = [m for m in (item.get("motifs") or []) if m in MOTIFS][:3]
    n = max(1, len(motifs))
    figs = []
    for i, name in enumerate(motifs):
        bw = (W - 120) / n * 0.86
        bx = 70 + (W - 120) * i / n + ((W - 120) / n - bw) / 2
        by, bh = H * 0.16, H * 0.52
        cap = MOTIFS[name](body, bx, by, bw, bh, ink, accent)
        figs.append(cap)
        _txt(body, bx + bw / 2, by + bh + 40, "FIG %02d" % (i + 1), ink, 12, "middle", 2.0, 0.5)

    if item.get("title"):
        body.append('<text x="48" y="%d" font-family="%s" font-size="30" fill="%s" '
                    'opacity="0.9">%s</text>' % (H - 46, SERIF, ink, esc(item["title"])))
    _txt(body, W - 48, H - 50, str(item.get("kicker") or "CATALOGUE SECTION"),
         ink, 12, "end", 2.4, 0.5)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
            'role="img" aria-label="%s"><title>%s</title><defs>%s</defs>%s</svg>'
            % (W, H, W, H, esc(item.get("title") or ""), esc(item.get("title") or ""),
               "".join(defs), "".join(body)))


def run(config_path, size=None, out_dir=None):
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    palette = dict(DEFAULT_PALETTE)
    palette.update(cfg.get("palette") or {})
    target = Path(out_dir or cfg.get("output_dir") or ".")
    target.mkdir(parents=True, exist_ok=True)
    px = size or int(cfg.get("size") or 900)

    written = []
    for item in cfg.get("items", []):
        code = str(item.get("code") or item.get("sku") or item.get("name"))
        code = re.sub(r"[^A-Za-z0-9_-]+", "-", code).strip("-")
        svg = build_plate(item, palette, px)
        path = target / ("%s.svg" % code)
        tmp = path.with_suffix(".svg.tmp")
        tmp.write_text(svg, encoding="utf-8")
        os.replace(tmp, path)
        written.append(str(path))
        print("[plate] %s  %s" % (code, item.get("name")))

    # 橫幅／封面：banners 各自帶 file / width / height / kind(hero|cover) / motifs
    for b in cfg.get("banners", []):
        W, H = int(b.get("width") or 1600), int(b.get("height") or 900)
        builder = build_cover if b.get("kind") == "cover" else build_banner
        svg = builder(b, palette, W, H)
        path = Path(b.get("out_dir") or target) / str(b["file"])
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".svg.tmp")
        tmp.write_text(svg, encoding="utf-8")
        os.replace(tmp, path)
        written.append(str(path))
        print("[%s] %s  %s" % (b.get("kind") or "hero", b["file"], b.get("title") or ""))

    print("\n%d files written" % len(written))
    return written


def main():
    ap = argparse.ArgumentParser(description="Generate catalogue spec plates as the image fallback")
    ap.add_argument("--config", required=True, help="JSON config path")
    ap.add_argument("--size", type=int, help="Square size in px (default 900)")
    ap.add_argument("--out", help="Override output directory")
    args = ap.parse_args()
    run(args.config, args.size, args.out)


if __name__ == "__main__":
    main()
