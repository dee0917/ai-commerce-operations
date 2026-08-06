#!/usr/bin/env python3
"""
E-commerce Quality Checklist v11.1 (Master-Grade)
=================================================
基於 Antigravity Kit 與 eCommerce 最佳實踐的 8 層自動化驗證管線。
新增：深層路由解析、資源完整性檢查、以及更嚴格的圖片掃描（解決死圖/打不開頁面問題）。
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# ANSI 顏色
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}")

def print_step(text: str):
    print(f"{Colors.CYAN}[Step] {text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

# 11 頁路由定義
REQUIRED_ROUTES = {
    "Layer A (Core)": [
        ("/", "Home Page"),
        ("/shop", "Shop Page"),
        ("/product/:slug", "Product Detail"),
        ("/cart", "Cart Page"),
        ("/checkout", "Checkout Page"),
        ("/search", "Search Page"),
    ],
    "Layer B (Member)": [
        ("/account/login", "Login Page"),
        ("/account/register", "Register Page"),
        ("/account/orders", "Order History"),
        ("/account/profile", "User Profile"),
    ],
    "Layer C (Policy)": [
        ("/policies", "Policy Pages (FAQ/Shipping/Returns)"),
    ],
}

# =============================================================
# P0: Build Verification (打包驗證)
# =============================================================
def check_build(project_path: Path) -> dict:
    """驗證項目是否能成功打包"""
    print_step("P0: Build Verification")
    
    # 解析 npm 路徑（Windows 上 npm 是 npm.cmd，裸 ["npm"] 會 FileNotFoundError）
    import shutil
    npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm_cmd:
        print_error("npm not found")
        return {"name": "Build Verification", "passed": False, "skipped": False, "details": "npm not found"}

    # 檢查是否安裝了依賴
    if not (project_path / "node_modules").exists():
        print_warning("node_modules missing, running npm install...")
        subprocess.run([npm_cmd, "install"], cwd=str(project_path), capture_output=True)

    result = subprocess.run([npm_cmd, "run", "build"], cwd=str(project_path), capture_output=True, text=True)
    
    if result.returncode == 0:
        print_success("Build: SUCCESS")
        return {"name": "Build Verification", "passed": True, "skipped": False, "details": "Build passed"}
    else:
        print_error("Build: FAILED")
        print(f"{Colors.RED}{result.stderr[:500]}...{Colors.ENDC}")
        return {"name": "Build Verification", "passed": False, "skipped": False, "details": "Build error"}

# =============================================================
# P1: Route Completeness (11 頁全覆蓋)
# =============================================================
def check_routes(project_path: Path) -> dict:
    """更深層地驗證 11 頁路由是否在代碼中定義並實作"""
    print_step("P1: Route Completeness (Deep Scan)")
    
    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "Route Completeness", "passed": False, "skipped": True, "details": "No src/"}

    # 1. 掃描路由定義內容
    route_content = ""
    for ext in ["*.tsx", "*.ts", "*.jsx", "*.js"]:
        for f in src_dir.rglob(ext):
            try:
                route_content += f.read_text(encoding="utf-8", errors="ignore")
            except:
                pass

    # 2. 確保物理文件存在于 pages 目錄
    pages_dir = src_dir / "pages"
    found_pages = []
    if pages_dir.exists():
        for f in pages_dir.rglob("*"):
            if f.is_file():
                found_pages.append(f.stem.lower())
    
    found = []
    missing = []
    total_count = 0

    for layer, routes in REQUIRED_ROUTES.items():
        for route_path, route_name in routes:
            total_count += 1
            # 搜尋路由定義中的路徑
            pattern = re.escape(route_path).replace(r"\:", ":")
            is_defined = re.search(pattern, route_content) or re.search(re.escape(route_path.rstrip("/")), route_content)
            
            # 模糊匹配頁面物理文件
            route_clean = route_path.strip("/").replace("/", "-").lower() or "home"
            is_implemented = any(route_clean in p or p in route_clean or ("policy" in route_clean and "policy" in p) for p in found_pages)
            
            if is_defined and is_implemented:
                found.append(f"  ✅ {route_name}")
            elif not is_defined:
                missing.append(f"  ❌ {route_name} (Missing ROUTE definition)")
            else:
                missing.append(f"  ❌ {route_name} (Missing COMPONENT file in pages/)")

    for f in found:
        print(f)
    for m in missing:
        print(m)

    passed = len(missing) == 0
    if passed:
        print_success(f"Routes: ALL {total_count} pages verified")
    else:
        print_error(f"Routes: {len(missing)} pages incomplete")

    return {"name": "Route Completeness", "passed": passed, "skipped": False, "details": f"{len(found)}/{total_count}"}

# =============================================================
# P2: Commerce Logic (購物車/結帳)
# =============================================================
REQUIRED_COMMERCE_FEATURES = [
    ("addItem", "Add to Cart"),
    ("removeItem", "Remove from Cart"),
    ("updateQuantity", "Update Quantity"),
    ("clearCart", "Clear Cart"),
    ("subtotal", "Subtotal Calculation"),
    ("useCart", "Cart Store Hook"),
    ("processCheckout", "Checkout Process"),
]

def check_commerce_logic(project_path: Path) -> dict:
    """驗證購物車與結帳核心邏輯是否完整"""
    print_step("P2: Commerce Logic (Cart/Checkout)")

    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "Commerce Logic", "passed": False, "skipped": True, "details": "No src/"}

    all_source = ""
    for ext in ["*.tsx", "*.ts"]:
        for f in src_dir.rglob(ext):
            try:
                all_source += f.read_text(encoding="utf-8", errors="ignore")
            except:
                pass

    found = []
    missing = []

    for feature_id, feature_name in REQUIRED_COMMERCE_FEATURES:
        if feature_id in all_source:
            found.append(f"  ✅ {feature_name}")
        else:
            missing.append(f"  ❌ {feature_name}")

    for f in found:
        print(f)
    for m in missing:
        print(m)

    passed = len(missing) == 0
    if passed:
        print_success("Commerce Logic: ALL features present")
    else:
        print_error(f"Commerce Logic: {len(missing)} features MISSING")

    return {"name": "Commerce Logic", "passed": passed, "skipped": False, "details": f"{len(found)}/{len(REQUIRED_COMMERCE_FEATURES)}"}

# =============================================================
# P3: Image Health (解決死圖問題)
# =============================================================
def check_image_health(project_path: Path) -> dict:
    """深度檢查圖片資源完整性，解決死圖問題"""
    print_step("P3: Deep Image Health Check")

    src_dir = project_path / "src"
    public_dir = project_path / "public"
    
    if not src_dir.exists():
        return {"name": "Image Health", "passed": False, "skipped": True, "details": "No src/"}

    issues = []
    safe_image_found = False
    raw_img_count = 0
    referenced_assets = set()

    for ext in ["*.tsx", "*.jsx", "*.ts"]:
        for f in src_dir.rglob(ext):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                rel_path = f.relative_to(project_path)

                if "SafeImage" in content:
                    safe_image_found = True

                # 尋找本地資源引用，例如 src="/images/hero.png"
                assets = re.findall(r'src=["\'](/(?:images|assets|img)/[^"\']+)["\']', content)
                referenced_assets.update(assets)

                # 嚴格檢查直接使用 <img (除非在 SafeImage 組建內部)
                if "SafeImage" not in str(f):
                    raw_imgs = re.findall(r'<img\s', content)
                    if raw_imgs:
                        raw_img_count += len(raw_imgs)
                        issues.append(f"  ❌ {rel_path}: {len(raw_imgs)} raw <img> tags found (MUST use SafeImage)")

            except:
                pass

    # 驗證引用的本地資源文件是否存在於 public/
    broken_assets = []
    if public_dir.exists():
        for asset in referenced_assets:
            local_path = public_dir / asset.lstrip("/")
            if not local_path.exists():
                broken_assets.append(asset)
                issues.append(f"  ❌ Broken Asset: {asset} (Not found in public/ directory)")
    
    if safe_image_found:
        print(f"  ✅ SafeImage architecture verified")
    else:
        issues.append("  ❌ SafeImage component NOT FOUND in project")

    if broken_assets:
        print_error(f"Found {len(broken_assets)} broken image references")
    
    for issue in issues[:15]:
        print(issue)

    passed = safe_image_found and raw_img_count == 0 and len(broken_assets) == 0
    if passed:
        print_success("Image Health: 100% Solid (No broken links)")
    else:
        print_error(f"Image Health: {len(issues)} blockers detected")

    return {"name": "Image Health", "passed": passed, "skipped": False, "details": f"Broken: {len(broken_assets)}, Raw: {raw_img_count}"}

# =============================================================
# P4: SEO Schema.org
# =============================================================
def check_seo(project_path: Path) -> dict:
    """驗證 SEO 基礎建設"""
    print_step("P4: SEO & Schema.org Check")

    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "SEO Schema.org", "passed": False, "skipped": True, "details": "No src/"}

    all_source = ""
    for ext in ["*.tsx", "*.ts", "*.jsx"]:
        for f in src_dir.rglob(ext):
            try:
                all_source += f.read_text(encoding="utf-8", errors="ignore")
            except:
                pass

    checks = {
        "Helmet/Meta Tags": "react-helmet" in all_source or "Helmet" in all_source or "<title" in all_source,
        "Product Schema (ld+json)": "application/ld+json" in all_source or "schema.org" in all_source.lower(),
        "Meta Description": 'meta.*description' in all_source.lower() or "description" in all_source,
        "OG Tags": "og:" in all_source or "openGraph" in all_source,
    }

    for name, found in checks.items():
        if found:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name}")

    passed_count = sum(1 for v in checks.values() if v)
    passed = passed_count >= 2  # 至少 Helmet + Schema

    if passed:
        print_success(f"SEO: {passed_count}/{len(checks)} checks passed")
    else:
        print_error(f"SEO: Only {passed_count}/{len(checks)} passed")

    return {"name": "SEO Schema.org", "passed": passed, "skipped": False, "details": f"{passed_count}/{len(checks)}"}

# =============================================================
# P5: Anti-Pattern Guard
# =============================================================
def check_anti_patterns(project_path: Path) -> dict:
    """偵測常見設計反模式"""
    print_step("P5: Anti-Pattern Guard")

    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "Anti-Pattern Guard", "passed": True, "skipped": True, "details": "No src/"}

    warnings = []

    for ext in ["*.tsx", "*.ts", "*.jsx", "*.css"]:
        for f in src_dir.rglob(ext):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                rel_path = f.relative_to(project_path)

                # 檢測 dangerouslySetInnerHTML
                if "dangerouslySetInnerHTML" in content:
                    warnings.append(f"  ⚠️ {rel_path}: dangerouslySetInnerHTML detected")

                # 檢測空的 onClick
                empty_handlers = re.findall(r'onClick=\{?\(\)\s*=>\s*\{\s*\}\}?', content)
                if empty_handlers:
                    warnings.append(f"  ❌ {rel_path}: empty onClick handler")

            except:
                pass

    for w in warnings[:15]:
        print(w)

    passed = not any("❌" in w for w in warnings)
    return {"name": "Anti-Pattern Guard", "passed": passed, "skipped": False, "details": f"{len(warnings)} issues"}

# =============================================================
# P6: Security Basics
# =============================================================
def check_security(project_path: Path) -> dict:
    """預防硬編碼 API Key"""
    print_step("P6: Security Basics")

    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "Security Basics", "passed": True, "skipped": True, "details": "No src/"}

    issues = []
    for ext in ["*.tsx", "*.ts", "*.jsx", "*.js"]:
        for f in src_dir.rglob(ext):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                if re.search(r'(?:api_key|token|auth)\s*[:=]\s*["\'][A-Za-z0-9_-]{32,}["\']', content, re.IGNORECASE):
                    issues.append(f"  ❌ {f.relative_to(project_path)}: Potential hardcoded secret")
            except:
                pass

    passed = len(issues) == 0
    return {"name": "Security Basics", "passed": passed, "skipped": False, "details": f"{len(issues)} issues"}

# =============================================================
# P7: UK/EU Compliance Gate (DMCCA 2024 / Omnibus / CPRs)
# =============================================================
# 法源：UK DMCCA 2024 (2025-04 生效)、CPRs、EU Omnibus Directive、EU UCPD。
# 規則書：references/anti-patterns.md §UK / EU 法律禁區 (L1-L6)。
# 原則：這些手法不是全面禁止，是「有真實依據才可以用」。
#       拿不出依據時的預設行為是不產生該元素，而不是產生一個假的。
COMPLIANCE_RULES = [
    # (規則代號, 說明, regex, 是否可被 EVIDENCE.md 豁免)
    ("L1", "無 30 天最低價基準的劃線原價 (line-through)",
     r"line-through", True),
    ("L1", "無基準的折扣幅度宣稱 (% OFF)",
     r"\d+\s*%\s*off\b", True),
    ("L1", "無基準的降價宣稱 (Was/Now、Save $X)",
     r"(?:\bwas\b\s*[:\s]*[$£€]\s*\d)|(?:\bsave\b\s*[$£€]\s*\d)", True),
    ("L1", "折扣價欄位被渲染 (compareAtPrice / originalPrice / oldPrice)",
     r"\b(?:compareAtPrice|compare_at_price|originalPrice|original_price|oldPrice|old_price)\b", True),
    ("L3", "硬寫的假庫存數字 (Only N left)",
     r"only\s*\{?\s*\d+\s*\}?\s*(?:items?\s*)?left", False),
    ("L3", "假的即時瀏覽人數 (N people are viewing)",
     r"\d+\s*(?:\+)?\s*(?:people|customers|others|shoppers)\s*(?:are\s*)?(?:viewing|watching|looking)", False),
    ("L3", "無銷售紀錄支撐的銷量宣稱 (Sold N+ times)",
     r"sold\s*\d+\+?\s*times", False),
    ("L5", "加購/訂閱預設勾選 (defaultChecked / checked={true})",
     r"(?:defaultChecked(?!\s*=\s*\{\s*false\s*\})|checked\s*=\s*\{\s*true\s*\})", False),
]

# 折價券／首購優惠不是「降價宣稱」：它沒有拿歷史價格當基準，不受 30 天規則約束。
# 這類語境下的 "% off" 降為人工覆核，避免誤殺合法優惠導致整關被關掉。
VOUCHER_CONTEXT = re.compile(
    r"first\s+(?:order|purchase|time)|sign\s*[- ]?up|subscribe|newsletter|"
    r"welcome\s+(?:offer|code)|promo\s*code|coupon|discount\s+code|referr",
    re.IGNORECASE)

# L2 需要跨行判斷：倒數計時器有沒有綁定一個真實的絕對截止時間
# WARNING 已知盲點（2026-07 明確不修，留給後續維護者）：本檢查是「單檔」判斷。
#    若倒數邏輯被拆成兩個檔案（例如元件在 CountdownBanner.tsx、計時在 useCountdown.ts），
#    每個檔案各自看起來都不完整，會漏抓。要補的話得做跨檔 import 追蹤。
COUNTDOWN_HINT = re.compile(
    r"countdown|timeLeft|time_left|timeRemaining|secondsLeft|hoursLeft|minutesLeft",
    re.IGNORECASE)
REAL_DEADLINE_HINT = re.compile(
    r"new\s+Date\s*\(\s*['\"`]|Date\.parse|endsAt|ends_at|endDate|end_date|expiresAt|expires_at|deadline",
    re.IGNORECASE)


# -------------------------------------------------------------
# compliance/EVIDENCE.md 結構化驗證
# -------------------------------------------------------------
# 前提：英國站是我們自己的 Shopify 店，價格歷史是自家資料，不是跟外部要的。
# 格式（markdown 表格，逐 SKU 一列，缺任一欄該 SKU 不予豁免）：
#   | sku | window_start | window_end | lowest_price | currency | was_price | source | generated_at |
# 驗證：欄位齊全 + 日期在有效視窗內 + was_price 不得高於 lowest_price。
# 注意：某 SKU 若真的沒有 30 天歷史（新品），正確做法是「不劃線」，不是放寬這裡的驗證。
# 已知邊界（開店後補）：這裡只驗格式，不驗數字真假。手打假數字 + source 填
# manual-verified 會通過。等 Shopify 店開了再接價格歷史 API 對帳；在那之前
# EVIDENCE.md 的內容真實性由填寫的人負責，不是這支腳本背書。
EVIDENCE_COLUMNS = ["sku", "window_start", "window_end", "lowest_price",
                    "currency", "was_price", "source", "generated_at"]
EVIDENCE_SOURCES = {"shopify-price-history-export", "internal-price-log", "manual-verified"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _parse_date(text):
    try:
        return datetime.strptime(text.strip()[:10], "%Y-%m-%d")
    except Exception:
        return None


def parse_price_evidence(evidence_path: Path):
    """回傳 (valid_skus, errors)。空殼檔 / 缺欄 / 日期過期 / was_price 過高都不算數。"""
    errors = []
    valid_skus = []
    try:
        raw = evidence_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [], ["  [L1-EVIDENCE] 無法讀取 compliance/EVIDENCE.md: %s" % e]

    rows = [ln for ln in raw.splitlines() if ln.strip().startswith("|")]
    if not rows:
        return [], ["  [L1-EVIDENCE] compliance/EVIDENCE.md 找不到任何 SKU 表格列（空殼檔不予豁免）"]

    header = [c.strip().lower() for c in rows[0].strip().strip("|").split("|")]
    missing = [c for c in EVIDENCE_COLUMNS if c not in header]
    if missing:
        return [], ["  [L1-EVIDENCE] EVIDENCE.md 表頭缺少必要欄位: %s" % ", ".join(missing)]
    idx = {c: header.index(c) for c in EVIDENCE_COLUMNS}

    today = datetime.now()
    for ln in rows[1:]:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < len(header):
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        sku = cells[idx["sku"]]
        rowerr = []

        for c in EVIDENCE_COLUMNS:
            if not cells[idx[c]]:
                rowerr.append("缺 %s" % c)

        ws_raw, we_raw = cells[idx["window_start"]], cells[idx["window_end"]]
        ws, we = _parse_date(ws_raw), _parse_date(we_raw)
        if ws_raw and not DATE_RE.match(ws_raw):
            rowerr.append("window_start 非 YYYY-MM-DD")
        if we_raw and not DATE_RE.match(we_raw):
            rowerr.append("window_end 非 YYYY-MM-DD")
        if ws and we:
            if (we - ws).days < 29:
                rowerr.append("視窗不足 30 天 (%d 天)" % ((we - ws).days + 1))
            if (today - we).days > 1:
                rowerr.append("window_end %s 早於生成日前 1 天（資料過期）" % we_raw)

        try:
            lowest = float(str(cells[idx["lowest_price"]]).replace(",", "").lstrip("$"))
            was = float(str(cells[idx["was_price"]]).replace(",", "").lstrip("$"))
            if lowest <= 0:
                rowerr.append("lowest_price 必須大於 0")
            if was > lowest:
                rowerr.append("was_price %s 高於 30 天最低價 %s（這正是違法標價）" % (was, lowest))
        except Exception:
            rowerr.append("lowest_price / was_price 不是數字")

        if cells[idx["source"]] not in EVIDENCE_SOURCES:
            rowerr.append("source 必須是 %s 之一" % "／".join(sorted(EVIDENCE_SOURCES)))
        if cells[idx["generated_at"]] and not _parse_date(cells[idx["generated_at"]]):
            rowerr.append("generated_at 無法解析")

        if rowerr:
            errors.append("  [L1-EVIDENCE] SKU %s 不予豁免：%s" % (sku or "(空白)", "；".join(rowerr)))
        else:
            valid_skus.append(sku)

    if not valid_skus and not errors:
        errors.append("  [L1-EVIDENCE] EVIDENCE.md 沒有任何有效 SKU 記錄（空殼檔不予豁免）")
    return valid_skus, errors


# -------------------------------------------------------------
# 資料端掃描：堵源頭，不只堵渲染出口
# -------------------------------------------------------------
# 渲染端（src/*.tsx）只是出口；商品資料檔裡的 compareAtPrice 才是源頭。
# 只堵出口不堵源頭，換一種渲染寫法就繞過去了。
DATA_PRICE_FIELDS = [
    "compareAtPrice", "compare_at_price", "comparePrice", "compare_price",
    "originalPrice", "original_price", "oldPrice", "old_price",
    "listPrice", "list_price", "msrp", "rrp", "wasPrice", "was_price",
    "salePrice", "sale_price", "discountPercent", "discount_percent",
    "discountPercentage", "discount_percentage",
]
# 2026-08-05 補：WooCommerce 命名的「折扣旗標」，**只掃 JSON 資料檔，不掃 .ts/.tsx**。
# 由來：實測 examples/ 三個站用的是 regular_price / sale_price / on_sale（底線 Woo 命名），
#       不是 camelCase。on_sale: true 本身就是一句降價宣稱（前台據此渲染劃線價），
#       而原本兩份清單都沒有它 → 突變測試證實整個漏掉。
#
# 為什麼只掃 JSON、不併進 DATA_PRICE_FIELDS：
#   JSON 走 _walk_json，比對的是「真正的 key」加「真正的 value」，位置無歧義。
#   行掃描只能用 regex，分不出欄位名出現在 key 位還是 value 位。實測把 on_sale
#   併進行掃描，examples/vanguard/src/services/api.ts:77,90,91 立刻產生 3 條誤報
#   —— 那是把 Woo Store API 回應轉成 UI 形狀的 mapper，值是執行期算出來的，
#   檔案裡沒有任何商品資料。本檔設計原則（見上方 :524 註解）本來就是
#   「商品資料檔才是源頭」，mapper 程式碼不歸資料掃描判。
#
# ⚠️ 已知盲點（誠實記錄，不是已解決）：
#   若有人把 on_sale: true 直接寫死在 mockData.ts 的內聯物件裡，本檢查抓不到。
#   要補得做 AST 解析分辨 key/value 位置，不是再加一條 regex。
DATA_PRICE_FLAG_FIELDS = ["onSale", "on_sale"]

# 故意不收 regular_price / regularPrice：在 Woo 命名裡那是「原本的售價」，
# 每個商品都必定帶值，收了會 100% 誤報、逼人直接關掉閘門。
# 降價宣稱的判準是 sale_price 帶值，或 on_sale 為真。
DATA_SCARCITY_FIELDS = [
    "viewingNow", "viewing_now", "viewersCount", "viewers_count",
    "peopleViewing", "people_viewing", "watchingNow", "watching_now",
    "soldCount", "sold_count", "unitsSold", "units_sold",
    "stockLeft", "stock_left", "inventoryCount", "inventory_count",
    "remainingStock", "remaining_stock", "unitsLeft", "units_left",
]
# 欄位存在不等於有在做降價宣稱：sale_price: "" 或 salePrice: null 代表「這個商品沒有特價」。
# 只有帶實際數值的欄位才是違規。
#
# 2026-08-05 修正（突變測試抓到，雙向都錯）：
#   原本寫法是「整行掃一次」且錨在行尾（`\s*[,}\]]?\s*$`），不看值屬於哪個欄位：
#   (a) 漏抓（嚴重）：`{ id: 1, salePrice: 79, note: null }`
#       → 行尾的 `note: null` 讓整行被判為「沒有特價」，真違規被靜默跳過。
#         閘門是 blocking 的，靜默跳過等於違法資料直接過關交付。
#   (b) 誤殺：`{ id: 'p1', price: 44, salePrice: null },`
#       → 值後面有兩個收尾字元（` },`），行尾錨比對不到 → 乾淨資料被判違規。
#         這正是 load_products.py 的產出被寫進 mockData.ts 內聯物件時的形狀。
# 改法：只看「該欄位名緊接著的那個值」，不再看行尾。兩種錯誤都消失。
# 維護提醒：不要為了少寫一個函式而改回整行 regex，這兩個錯誤會一起回來。
_EMPTY_VALUE = r"""(?:(?:null|undefined|None|false)(?!\w)|0(?![\d.])|""|'')"""

def field_value_is_empty(line: str, field: str) -> bool:
    """line 裡的 field 是否帶著「等於沒有特價」的空值（null/""/0/false…）。"""
    return re.search(r"\b%s\b\s*[:=]\s*%s" % (re.escape(field), _EMPTY_VALUE),
                     line, re.IGNORECASE) is not None

# 欄位的值以識別字／函式呼叫開頭 ＝ 執行期才算出來的，不是寫死的商品資料。
# 排除 true/false/null/undefined/None：那些是字面值，要照一般規則判。
DERIVED_VALUE_START = r"""(?!(?:true|false|null|undefined|None)\b)[A-Za-z_$]"""
# -------------------------------------------------------------
# SCAN_FALSE_POSITIVE_NOTE — 掃描範圍與誤報率是「量出來的」，不是猜的
# -------------------------------------------------------------
# 實測日期：2026-07-31
# 樣本：本技能過去產出的 3 個真實站台
#       （20260321-ink-and-quill、20260321-stow、20260320-aura-cards）
#
# 第一版（全專案掃描 + 欄位名清單 + 非空值判斷）：
#   26 條 hit，其中真違規 16、誤報 10 → 誤報率 38.5%
#   誤報全部同一個原因：`salePrice || price` / `?? price` 這種「取有效售價」的慣用法
#   （算購物車小計、排序篩選、顯示單一價格），畫面上沒有任何價格比較，不是降價宣稱。
#
# 第二版（加上 fallback 慣用法排除，就是下面那條 `||` / `??` 規則）：
#   16 條 hit，真違規 16、誤報 0 → 誤報率 0%，且第一版抓到的真違規一條都沒漏。
#
# 結論：維持全專案掃描，不退回寫死目錄清單。
#   （寫死清單實測會漏：只掃 src/ + 根目錄時，data/products.json 直接漏掉，
#     而那正是已證實會出事的位置。）
#   誤報用「欄位名 + 非空值 + 慣用法排除 + 排除 .d.ts/型別宣告」四層收，
#   而不是用縮小掃描範圍來收。日後誤報變高，請照同樣方式找誤報的共同原因，
#   不要縮範圍。
#
# 已知邊界（開店後補，不是現在的缺陷）：
#   compliance/EVIDENCE.md 目前只驗「格式齊全、日期有效、was_price 不高於 lowest_price」，
#   **不驗數字本身是真的**。有人手打一列假數字、source 填 manual-verified 就會通過。
#   等英國站 Shopify 真的開了，再接 Shopify 價格歷史 API 做對帳。
#   在那之前，EVIDENCE.md 的內容真實性靠人負責，不靠這支腳本。

# 掃描範圍：src/** 全域 + 根目錄（不用固定目錄清單，避免結構一變就漏抓）
DATA_SCAN_EXTS = [".json", ".ts", ".tsx", ".js", ".jsx"]
EXCLUDED_DIRS = {"node_modules", "dist", "build", ".next", "coverage", ".git"}

# 型別宣告不是商品資料：salePrice?: number; / salePrice: string | null;
TYPE_ANNOTATION = re.compile(
    r"\??\s*:\s*(?:number|string|boolean|any|unknown|null|undefined|Date|"
    r"Array\s*<|[A-Z]\w*\[\]|\w+\[\])(?:\s*\|\s*(?:number|string|boolean|null|undefined))*"
    r"\s*;?\s*$")

DATA_SKIP_FILES = {"package.json", "package-lock.json", "tsconfig.json",
                   "tsconfig.node.json", "tsconfig.app.json", "components.json"}


def _walk_json(node, fields, found, path=""):
    """在 JSON 結構裡找出有實際值的違規欄位。"""
    if isinstance(node, dict):
        for k, v in node.items():
            child = "%s.%s" % (path, k) if path else k
            if k in fields and v not in (None, "", 0, False, "0"):
                found.append((child, v))
            _walk_json(v, fields, found, child)
    elif isinstance(node, list):
        for n, v in enumerate(node[:200]):
            _walk_json(v, fields, found, "%s[%d]" % (path, n))


def scan_data_sources(project_path: Path):
    """全專案掃描，抓商品資料裡帶值的降價欄位與假稀缺欄位。

    設計取捨：**不使用固定目錄清單**。寫死 data/ public/ 這種清單，
    等於把「下次專案結構一變就漏抓」寫進設計裡。改用
    「全域掃描 + 欄位名清單 + 非空值判斷 + 針對誤報原因的排除規則」。
    誤報用實測數據控管（見本檔 SCAN_FALSE_POSITIVE_NOTE）。
    """
    hits = []
    targets = []
    # 全專案掃描（不是 src/ + 根目錄）：實測發現只掃 src/ 會漏掉 data/products.json，
    # 而那正是我們已經證實會出事的位置。範圍寧可寬，誤報用欄位/值/慣用法規則收。
    for ext in DATA_SCAN_EXTS:
        targets.extend(project_path.rglob("*" + ext))

    seen_files = set()
    seen_hits = set()
    for f in targets:
        sf = str(f)
        if f.name in DATA_SKIP_FILES or f in seen_files:
            continue
        if any(part in EXCLUDED_DIRS for part in f.parts):
            continue
        if f.name.endswith(".d.ts"):      # 型別宣告檔沒有資料，只有欄位名
            continue
        seen_files.add(f)
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = f.relative_to(project_path)

        if f.suffix == ".json":
            try:
                data = json.loads(content)
            except Exception:
                data = None
            if data is not None:
                for fields, code, label in (
                        # 折扣旗標只在 JSON 這條路徑掃（見 DATA_PRICE_FLAG_FIELDS 註解）
                        (set(DATA_PRICE_FIELDS) | set(DATA_PRICE_FLAG_FIELDS), "L1", "降價欄位"),
                        (set(DATA_SCARCITY_FIELDS), "L3", "假稀缺欄位")):
                    found = []
                    _walk_json(data, fields, found)
                    for keypath, val in found[:10]:
                        hits.append((code, "  [%s|DATA] %s  商品資料含%s %s = %s"
                                     % (code, rel, label, keypath, val)))
                continue

        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            for code, fieldlist, label in (("L1", DATA_PRICE_FIELDS, "降價欄位"),
                                           ("L3", DATA_SCARCITY_FIELDS, "假稀缺欄位")):
                for fld in fieldlist:
                    if not re.search(r"\b%s\b" % re.escape(fld), line):
                        continue
                    # 欄位存在但沒有值（""/null/undefined/0）＝沒有在做降價宣稱
                    # 只看這個欄位自己的值，不看整行（見 field_value_is_empty 上方註解）
                    if field_value_is_empty(line, fld):
                        break
                    # 型別宣告不是資料：salePrice?: number; / salePrice: string | null;
                    if TYPE_ANNOTATION.search(line):
                        break
                    # `salePrice || price` / `salePrice ?? price` 是「取有效售價」的
                    # 合法慣用法（算小計、排序、顯示單一價格），畫面上沒有任何價格比較，
                    # 不構成降價宣稱。實測這一條就是資料端誤報的唯一來源。
                    if re.search(r"\b%s\s*(?:\|\||\?\?)" % re.escape(fld), line):
                        break
                    # 值是執行期算出來的表達式（識別字／函式呼叫／三元），不是字面值
                    # → 這是對應或計算程式碼，不是商品資料。
                    # 實例：examples/vanguard/src/services/api.ts:90
                    #       `sale_price: onSale ? sale : '',`（Woo Store API mapper）
                    # 商品資料裡的違規值一定是字面值（79 / "79" / true），所以這條
                    # 不會放過真違規。（舊版是靠行尾剛好有 `: '',` 才誤打誤撞不報，
                    # 那是巧合不是規則，欄位順序一換就會爆。）
                    if re.search(r"\b%s\b\s*[:=]\s*%s" % (re.escape(fld), DERIVED_VALUE_START),
                                 line):
                        break
                    key = (str(rel), i, code)
                    if key in seen_hits:
                        break
                    seen_hits.add(key)
                    hits.append((code, "  [%s|DATA] %s:%d  商品資料含%s %s | %s"
                                 % (code, rel, i, label, fld, line.strip()[:60])))
                    break
    return hits


def check_uk_eu_compliance(project_path: Path) -> dict:
    """UK/EU 不實標價與黑暗模式硬攔查。違反即不得交付（不看分數）。"""
    print_step("P7: UK/EU Compliance Gate (DMCCA / Omnibus)")

    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "UK/EU Compliance Gate", "passed": True, "skipped": True,
                "details": "No src/", "blocking": True}

    # 豁免依據：compliance/EVIDENCE.md 必須逐 SKU 通過結構化驗證，空殼檔不算數
    evidence = project_path / "compliance" / "EVIDENCE.md"
    violations = []
    waived = []
    valid_skus = []
    if evidence.exists():
        valid_skus, ev_errors = parse_price_evidence(evidence)
        violations.extend(ev_errors)
        if valid_skus:
            print_warning("EVIDENCE.md 通過驗證的 SKU：%s → 這些 L1 降價宣稱改為人工覆核"
                          % ", ".join(valid_skus[:10]))
        else:
            print_error("compliance/EVIDENCE.md 存在但沒有任何有效 SKU 記錄 → 不予豁免")
    has_evidence = len(valid_skus) > 0

    for ext in ["*.tsx", "*.ts", "*.jsx", "*.js", "*.css", "*.html"]:
        for f in src_dir.rglob(ext):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            rel_path = f.relative_to(project_path)
            lines = content.splitlines()

            for code, desc, pattern, waivable in COMPLIANCE_RULES:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        hit = "  [%s] %s:%d  %s | %s" % (
                            code, rel_path, i, desc, line.strip()[:80])
                        # 折價券語境看上下 3 行（CTA 按鈕文字常與說明文分行）
                        window = chr(10).join(lines[max(0, i - 4): i + 3])
                        is_voucher = "% OFF" in desc and VOUCHER_CONTEXT.search(window)
                        if is_voucher:
                            waived.append(hit + "  << 折價券語境，人工確認非降價宣稱")
                        elif waivable and has_evidence:
                            waived.append(hit)
                        else:
                            violations.append(hit)

            # L2: 有倒數邏輯但沒有任何絕對截止時間 → 重整就重來的假倒數
            if COUNTDOWN_HINT.search(content) and "setInterval" in content:
                if not REAL_DEADLINE_HINT.search(content):
                    violations.append(
                        "  [L2] %s  倒數計時器未綁定真實絕對截止時間（重整即重置＝假倒數）" % rel_path)

    # 資料端：商品資料檔才是源頭，渲染端只是出口
    for code, hit in scan_data_sources(project_path):
        if code == "L1" and has_evidence:
            waived.append(hit)
        else:
            violations.append(hit)

    for w in waived:
        print_warning(w.strip())
    for v in violations:
        print_error(v)

    passed = len(violations) == 0
    if passed:
        print_success("UK/EU Compliance: 無違規（渲染端與資料端皆無無基準劃線價 / 假倒數 / 假庫存 / 預設勾選）")
    else:
        print_error("UK/EU Compliance Gate FAILED：%d 項違規，依 DMCCA/Omnibus 不得交付。"
                    % len(violations))
        print_error("修法方式見 references/anti-patterns.md §UK / EU 法律禁區")

    return {"name": "UK/EU Compliance Gate", "passed": passed, "skipped": False,
            "details": "%d violations" % len(violations), "blocking": True}

# =============================================================
# Summary & Scorecard
# =============================================================

# =============================================================
# P8: Motion Baseline（motion-system.md §四 四項最低要求，2026-08-06 從「規則在沒人跑」改成自動關卡）
# =============================================================
def check_motion_baseline(project_path: Path) -> dict:
    """motion-system.md 四項最低要求：whileInView 進場、MotionConfig、reduced-motion、
    具名 cubic-bezier（不是裸 transition-colors）。amberflask 健檢曾 FAIL 三項半，
    根因是「規則寫在文件裡但驗收沒人跑」——這支就是補那個洞，blocking=True 直接擋交付。"""
    print_step("P8: Motion Baseline (motion-system.md §四)")
    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "Motion Baseline", "passed": True, "skipped": True, "details": "No src/", "blocking": True}

    all_source = ""
    for ext in ["*.tsx", "*.ts", "*.jsx", "*.css"]:
        for f in src_dir.rglob(ext):
            try:
                all_source += f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass

    while_in_view_count = len(re.findall(r'whileInView', all_source))
    has_motion_config = "MotionConfig" in all_source
    has_reduced_motion = bool(re.search(r'prefers-reduced-motion|reducedMotion', all_source))
    has_named_easing = bool(re.search(r'cubic-bezier\s*\(', all_source))

    items = {
        "whileInView >= 6（首頁滾動進場）": while_in_view_count >= 6,
        "MotionConfig 存在": has_motion_config,
        "reduced-motion 有包": has_reduced_motion,
        "具名 cubic-bezier（非預設 ease）": has_named_easing,
    }
    for name, ok in items.items():
        print(f"  {'✅' if ok else '❌'} {name}")

    passed = all(items.values())
    n_pass = sum(items.values())
    if passed:
        print_success(f"Motion Baseline: {n_pass}/4 全過")
    else:
        print_error(f"Motion Baseline: {n_pass}/4（whileInView={while_in_view_count}）")

    return {"name": "Motion Baseline", "passed": passed, "skipped": False,
            "details": f"{n_pass}/4，whileInView={while_in_view_count}", "blocking": True}


# =============================================================
# P9: 每商品圖庫下限（image-scene-spec.md「每商品圖庫下限」鐵律）
# =============================================================
_PRODUCT_BLOCK_RE = re.compile(
    r"(?:id|slug)\s*:\s*['\"]([^'\"]+)['\"][^{}]*?images\s*:\s*\[([^\]]*)\]", re.DOTALL)
_IMG_URL_RE = re.compile(r"['\"`]([^'\"`]+\.(?:jpg|jpeg|png|webp))['\"`]", re.IGNORECASE)


def check_product_image_count(project_path: Path) -> dict:
    """image-scene-spec.md 鐵律：每個商品至少 3 張專屬圖，任兩商品不得共用同一張圖片 URL。
    2026-08 thirdstop(單圖 x8)/tensile(單圖 x4) 破口的直接對應檢查，blocking=True。"""
    print_step("P9: Product Image Count (image-scene-spec.md)")
    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "Product Image Count", "passed": True, "skipped": True, "details": "No src/", "blocking": True}

    data_files = list(src_dir.rglob("mockData.ts")) + list(src_dir.rglob("*products*.ts")) + \
                 list(src_dir.rglob("*products*.json"))
    if not data_files:
        return {"name": "Product Image Count", "passed": True, "skipped": True,
                "details": "No product data file found", "blocking": True}

    under_min = []
    url_owner = {}
    dup_urls = []
    total_products = 0

    for f in data_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in _PRODUCT_BLOCK_RE.finditer(content):
            pid, block = m.group(1), m.group(2)
            urls = _IMG_URL_RE.findall(block)
            total_products += 1
            if len(urls) < 3:
                under_min.append(f"  ❌ {pid}: only {len(urls)} image(s) (minimum 3)")
            for u in urls:
                if u in url_owner and url_owner[u] != pid:
                    dup_urls.append(f"  ❌ {u}: shared between {url_owner[u]} and {pid}")
                else:
                    url_owner[u] = pid

    for line in (under_min + dup_urls)[:15]:
        print(line)

    if total_products == 0:
        return {"name": "Product Image Count", "passed": True, "skipped": True,
                "details": "No parseable product blocks (data shape not recognized by this checker)",
                "blocking": True}

    passed = not under_min and not dup_urls
    if passed:
        print_success(f"Product Image Count: {total_products} products, all ≥3 unique images")
    else:
        print_error(f"Product Image Count: {len(under_min)} under minimum, {len(dup_urls)} shared URLs")

    return {"name": "Product Image Count", "passed": passed, "skipped": False,
            "details": f"{total_products} products, {len(under_min)} under-min, {len(dup_urls)} shared",
            "blocking": True}


# =============================================================
# P10: 色彩對比與美感鎖值（typography-baseline.md 六、七章，2026-08-06 新增）
# =============================================================
def _relative_luminance(hexcode: str) -> float:
    h = hexcode.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = lin(r), lin(g), lin(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast_ratio(hex1: str, hex2: str) -> float:
    l1, l2 = _relative_luminance(hex1), _relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


_HEX_RE_LOCAL = re.compile(r'#([0-9a-fA-F]{6})\b')
_PAIR_RULE_RE = re.compile(r'\{([^{}]*)\}')
_COLOR_PROP_RE = re.compile(r'(?<!background-)(?<!border-)\bcolor\s*:\s*(#[0-9a-fA-F]{6})', re.IGNORECASE)
_BG_PROP_RE = re.compile(r'background(?:-color)?\s*:\s*(#[0-9a-fA-F]{6})', re.IGNORECASE)


def check_color_contrast(project_path: Path) -> dict:
    """WCAG AA 對比度（內文 4.5:1）。⚠️ 靜態掃法：只抓同一個 CSS 規則區塊裡明寫的
    color/background hex 配對，抓不到跨檔繼承或 Tailwind 動態 class 算出來的顏色——
    這是近似值不是真正的 computed style 稽核（那要 Playwright 讀 getComputedStyle，
    是 wcag-audit-patterns 技能的活）。這裡先接一個會真的動的靜態關卡，
    比「規則寫著沒人跑」好，但不要誤會這裡涵蓋全部情況。"""
    print_step("P10: Color Contrast (WCAG AA, static approximation)")
    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "Color Contrast (WCAG AA)", "passed": True, "skipped": True, "details": "No src/", "blocking": True}

    failures = []
    checked = 0
    for ext in ["*.css", "*.tsx", "*.ts"]:
        for f in src_dir.rglob(ext):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for block_m in _PAIR_RULE_RE.finditer(content):
                block = block_m.group(1)
                cm = _COLOR_PROP_RE.search(block)
                bm = _BG_PROP_RE.search(block)
                if not (cm and bm):
                    continue
                checked += 1
                ratio = _contrast_ratio(cm.group(1), bm.group(1))
                if ratio < 4.5:
                    failures.append(f"  ❌ {f.relative_to(project_path)}: {cm.group(1)} on {bm.group(1)} "
                                    f"= {ratio:.2f}:1 (需 ≥4.5:1)")

    for line in failures[:15]:
        print(line)

    if checked == 0:
        return {"name": "Color Contrast (WCAG AA)", "passed": True, "skipped": True,
                "details": "No same-block color+background hex pairs found to check", "blocking": True}

    passed = not failures
    if passed:
        print_success(f"Color Contrast: {checked} pairs checked, all ≥4.5:1")
    else:
        print_error(f"Color Contrast: {len(failures)}/{checked} pairs below 4.5:1")

    return {"name": "Color Contrast (WCAG AA)", "passed": passed, "skipped": False,
            "details": f"{len(failures)}/{checked} below threshold", "blocking": True}


def check_aesthetic_locks(project_path: Path) -> dict:
    """typography-baseline.md 七、首屏 + 美感鎖值：全站 hue 桶 ≤3、unique box-shadow ≤3、
    首屏恰一 h1、禁自動輪播。CTA 數量與「哪個是主 CTA」需要語意判斷，靜態掃描不可靠，
    刻意不做假檢查——留給 site-quality-rubric.md 人審（見 docstring 誠實標註原則）。"""
    print_step("P11: Aesthetic Lock Values (typography-baseline.md)")
    src_dir = project_path / "src"
    if not src_dir.exists():
        return {"name": "Aesthetic Locks", "passed": True, "skipped": True, "details": "No src/", "blocking": True}

    all_source = ""
    home_source = ""
    for ext in ["*.tsx", "*.ts", "*.jsx", "*.css"]:
        for f in src_dir.rglob(ext):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            all_source += content
            if re.search(r'(index|home|page)\.(tsx|jsx)$', f.name, re.IGNORECASE):
                home_source += content

    # hue 桶（沿用 design_history.py / check_site_distance.py 同一顆 30° 分桶邏輯，各自獨立一份小函式）
    hexes = {m.group(0) for m in _HEX_RE_LOCAL.finditer(all_source)}
    buckets = set()
    for hx in hexes:
        h = hx.lstrip('#')
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        mx, mn = max(r, g, b), min(r, g, b)
        if mx - mn <= 4:
            continue  # 中性色不占色相桶
        if mx == r:
            hue = 60.0 * (((g - b) / float(mx - mn)) % 6)
        elif mx == g:
            hue = 60.0 * (((b - r) / float(mx - mn)) + 2)
        else:
            hue = 60.0 * (((r - g) / float(mx - mn)) + 4)
        buckets.add(int(hue // 30) * 30)
    hue_count = len(buckets)

    shadows = set(re.findall(r'box-shadow\s*:\s*([^;]+);', all_source))
    shadow_count = len(shadows)

    h1_count = len(re.findall(r'<h1[\s>]', home_source)) if home_source else len(re.findall(r'<h1[\s>]', all_source))
    has_autoplay_carousel = bool(re.search(r'(swiper|embla|carousel)[^;{}]{0,80}autoplay', all_source, re.IGNORECASE))

    items = {
        f"全站色相桶 ≤3（實測 {hue_count}）": hue_count <= 3,
        f"unique box-shadow ≤3（實測 {shadow_count}）": shadow_count <= 3,
        f"首屏恰一 h1（實測 {h1_count}）": h1_count == 1,
        "禁自動輪播（swiper/embla autoplay）": not has_autoplay_carousel,
    }
    for name, ok in items.items():
        print(f"  {'✅' if ok else '❌'} {name}")

    passed = all(items.values())
    n_pass = sum(items.values())
    if passed:
        print_success(f"Aesthetic Locks: {n_pass}/4 全過")
    else:
        print_error(f"Aesthetic Locks: {n_pass}/4")

    return {"name": "Aesthetic Locks", "passed": passed, "skipped": False,
            "details": f"{n_pass}/4，hue={hue_count} shadow={shadow_count} h1={h1_count}", "blocking": True}

def print_scorecard(results: List[dict], start_time: datetime):
    """輸出品質計分卡"""
    duration = (datetime.now() - start_time).total_seconds()
    print_header("📊 E-COMMERCE QUALITY SCORECARD")

    passed_count = sum(1 for r in results if r["passed"] and not r.get("skipped"))
    total_non_skipped = sum(1 for r in results if not r.get("skipped"))
    score = int((passed_count / max(total_non_skipped, 1)) * 100)

    for r in results:
        status = f"{Colors.GREEN}✅{Colors.ENDC}" if r["passed"] else f"{Colors.RED}❌{Colors.ENDC}"
        if r.get("skipped"): status = f"{Colors.YELLOW}⏭️ {Colors.ENDC}"
        print(f"  {status} {r['name']} [{r.get('details', '')}]")

    print(f"\n  {Colors.BOLD}TOTAL SCORE: {score}/100{Colors.ENDC} (Time: {duration:.1f}s)")

    # Blocking check（法規類）不看分數：只要沒過就一律不得交付
    blocked = [r for r in results if r.get("blocking") and not r["passed"] and not r.get("skipped")]
    if blocked:
        for r in blocked:
            print_error(f"BLOCKING: {r['name']} 未通過 → 不得交付（法規風險，非評分項）")
        return False

    return score >= 75

def main():
    import argparse
    parser = argparse.ArgumentParser(description="E-commerce Quality Checklist v11.1")
    parser.add_argument("project", help="Project path to validate")
    parser.add_argument("--preview", action="store_true", help="Auto-start preview server after successful checks")

    args = parser.parse_args()
    project_path = Path(args.project).resolve()

    if not project_path.exists():
        print(f"❌ Error: Path {project_path} not found")
        sys.exit(1)

    start_time = datetime.now()
    checks = [check_build, check_routes, check_commerce_logic, check_image_health, check_seo, check_anti_patterns, check_security, check_uk_eu_compliance, check_motion_baseline, check_product_image_count, check_color_contrast, check_aesthetic_locks]
    results = [fn(project_path) for fn in checks]

    all_passed = print_scorecard(results, start_time)

    if args.preview and all_passed:
        print_header("🌐 AUTO-START PREVIEW")
        preview_script = project_path / ".agent" / "scripts" / "auto_preview.py"
        if preview_script.exists():
            subprocess.run(["python", str(preview_script), "start", "5173"], cwd=str(project_path))
            print(f"\n  {Colors.BOLD}{Colors.GREEN}👉 PREVIEW URL: http://localhost:5173{Colors.ENDC}\n")
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
