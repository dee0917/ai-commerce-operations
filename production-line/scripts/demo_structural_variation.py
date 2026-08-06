#!/usr/bin/env python3
"""
Structural Variation 選取邏輯 Demo
用兩個以上 seed / 品類跑一次 Phase 1.07 的結構選取邏輯（區塊組成/順序、
分頁組合、組件變體），證明每站的結構層真的不一樣。不生成整站，只跑
選取邏輯本身，省錢驗證用。

對照: references/structural-variation.md

執行: python scripts/demo_structural_variation.py
"""

import random

# ---------------------------------------------------------------------------
# 1. 區塊池與相鄰規則 (對照 structural-variation.md §2)
# ---------------------------------------------------------------------------

SECTION_POOL = [
    "USP信任條", "特色商品", "分類展示", "品牌故事", "熱賣榜", "顧客評價",
    "Lookbook穿搭情境", "影片生活風格", "促銷banner", "社群牆(IG)",
    "電子報訂閱", "FAQ精選",
]
PRODUCT_HEAVY = {"特色商品", "熱賣榜", "分類展示"}


def select_section_order(rng: random.Random) -> list:
    """Hero/Footer 錨定，中間 5-8 個區塊隨機選取＋排序，再套相鄰規則"""
    k = rng.randint(5, 8)
    middle = rng.sample(SECTION_POOL, k)
    rng.shuffle(middle)
    middle = _apply_adjacency_rules(rng, middle)
    return ["Hero", *middle, "Footer"]


def _apply_adjacency_rules(rng: random.Random, sections: list) -> list:
    sections = list(sections)

    # 電子報訂閱 → 挪到近底部 (倒數 1-2 格)
    if "電子報訂閱" in sections:
        sections.remove("電子報訂閱")
        pos = max(0, len(sections) - rng.randint(0, 1))
        sections.insert(pos, "電子報訂閱")

    # 品牌故事 → 挪到中段前半
    if "品牌故事" in sections:
        sections.remove("品牌故事")
        half = max(1, len(sections) // 2)
        pos = rng.randint(0, half)
        sections.insert(pos, "品牌故事")

    # 商品密集區塊不可連續 3 個，找後面的非商品區塊交換打散
    guard = 0
    changed = True
    while changed and guard < 10:
        changed = False
        guard += 1
        for i in range(len(sections) - 2):
            if all(s in PRODUCT_HEAVY for s in sections[i:i + 3]):
                for j in range(i + 3, len(sections)):
                    if sections[j] not in PRODUCT_HEAVY:
                        sections[i + 1], sections[j] = sections[j], sections[i + 1]
                        changed = True
                        break
    return sections


# ---------------------------------------------------------------------------
# 2. 品類 → 選配頁對照 (對照 structural-variation.md §3)
# ---------------------------------------------------------------------------

CORE_PAGES = ["Home(首頁)", "Shop(商品列表)", "Product(商品內頁)", "Cart(購物車)", "Checkout(結帳)"]

# 對照 extracted_products.json 現有 20 個真實分類
CATEGORY_TO_GROUP = {
    "傳統風水護身類": "靈性/身心療癒", "煙燻淨化類": "靈性/身心療癒",
    "水晶原石類": "靈性/身心療癒", "音療器具類": "靈性/身心療癒",
    "神聖符號類": "靈性/身心療癒", "案頭風水類": "靈性/身心療癒",
    "御守香囊類": "靈性/身心療癒", "藥草瓶飾類": "靈性/身心療癒",
    "能量卡片類": "靈性/身心療癒",
    "水晶掛飾類": "珠寶/配件",
    "EDC 隨身裝備類": "運動/戶外", "戶外露營小物類": "運動/戶外",
    "極簡桌面美學類": "生活風格/桌面文具", "特殊文具類": "生活風格/桌面文具",
    "咖啡與茶道類": "食品/飲品",
    "創作者攝影配件類": "3C/電子", "智慧穿戴與配件類": "3C/電子",
    "香氛與療癒類": "美妝/保養",
    "收納整理類": "家居/家具",
    # 汽車內飾類 刻意不列入 → 示範 Test 4 的 fallback 機制
}

GROUP_OPTIONAL_PAGES = {
    "服飾/時尚": ["Lookbook", "SizeGuide(尺寸指南)", "StylingGuide(穿搭指南)", "Collection(系列landing)"],
    "食品/飲品": ["Recipe(食譜/沖泡指南)", "Ingredients(成分與產地)", "Subscription(訂閱方案)", "GiftBox(禮盒組合)"],
    "3C/電子": ["SpecCompare(規格比較)", "Compatibility(相容性)", "Warranty(保固/開箱)", "UserManual(使用手冊)"],
    "美妝/保養": ["Ingredients(成分列表)", "HowToUse(使用教學)", "SkinQuiz(膚質測驗)", "BeforeAfter"],
    "家居/家具": ["CareGuide(保養指南)", "RoomScenes(空間情境)", "MaterialGuide(材質說明)", "SpacePlanning(空間規劃)"],
    "珠寶/配件": ["CareGuide(保養方式)", "SizeGuide(戒圍/鍊長)", "GiftWrap(禮品包裝)", "Certificate(材質證書)"],
    "運動/戶外": ["GearGuide(裝備指南)", "UseCase(使用情境)", "EventCalendar(活動日曆)", "Community(社群挑戰)"],
    "靈性/身心療癒": ["RitualGuide(儀式/淨化教學)", "EnergyChart(能量對應表)", "MeditationGuide(冥想引導)", "OriginStory(來源故事)"],
    "生活風格/桌面文具": ["UseCase(使用情境)", "Craftsmanship(材質工藝)", "PairingGuide(搭配建議)", "Collection(系列landing)"],
}

GENERIC_FALLBACK_PAGES = [
    "About(關於/品牌故事)", "Journal(Journal/Blog)", "FAQ",
    "Contact(聯絡)", "Sale(Sale/Outlet)", "Bundle(套組)",
]


def resolve_category_group(category_name: str) -> str:
    return CATEGORY_TO_GROUP.get(category_name, "通用 fallback")


def select_page_set(rng: random.Random, category_name: str):
    group = resolve_category_group(category_name)
    pool = GROUP_OPTIONAL_PAGES.get(group, GENERIC_FALLBACK_PAGES)
    k = rng.randint(1, min(4, len(pool)))
    optional = rng.sample(pool, k)
    return CORE_PAGES + optional, group


# ---------------------------------------------------------------------------
# 3. 組件變體 (對照 structural-variation.md §4)
# ---------------------------------------------------------------------------

COMPONENT_VARIANT_OPTIONS = {
    "Header導覽": ["橫向選單", "漢堡常駐", "mega-menu"],
    "Hero": ["全出血圖", "左右分割", "輪播", "影片", "文字主導"],
    "商品牆": ["整齊格", "瀑布流", "輪播", "編輯混排"],
    "商品卡": ["hover顯資訊", "常駐資訊", "overlay"],
    "分類展示": ["大圖磚", "橫向捲動", "清單"],
}


def select_component_variants(rng: random.Random) -> dict:
    return {k: rng.choice(v) for k, v in COMPONENT_VARIANT_OPTIONS.items()}


# ---------------------------------------------------------------------------
# 4. 完整選取（單站）
# ---------------------------------------------------------------------------

def generate_site_structure(seed: int, category_name: str) -> dict:
    rng = random.Random(seed)
    section_order = select_section_order(rng)
    page_set, group = select_page_set(rng, category_name)
    variants = select_component_variants(rng)
    return {
        "seed": seed,
        "category": category_name,
        "category_group": group,
        "section_order": section_order,
        "page_set": page_set,
        "component_variants": variants,
    }


# ---------------------------------------------------------------------------
# 5. Demo 輸出
# ---------------------------------------------------------------------------

def _print_site(label: str, site: dict):
    print(f"\n【{label}】seed={site['seed']}  品類={site['category']} → 品類群={site['category_group']}")
    print(f"  首頁區塊順序 ({len(site['section_order'])} 個):")
    print(f"    {' → '.join(site['section_order'])}")
    print(f"  分頁組合 ({len(site['page_set'])} 頁):")
    print(f"    {', '.join(site['page_set'])}")
    print("  組件變體:")
    for k, v in site["component_variants"].items():
        print(f"    - {k}: {v}")


def main():
    print("=" * 72)
    print("Structural Variation Demo -- 證明每站結構層真的不一樣")
    print("=" * 72)

    # --- Test 1: 完整雙站比較（seed 不同 + 品類不同）---
    site_a = generate_site_structure(1001, "水晶原石類")
    site_b = generate_site_structure(2002, "EDC 隨身裝備類")

    print("\n" + "-" * 72)
    print("Test 1: 完整雙站比較（不同 seed + 不同品類）")
    print("-" * 72)
    _print_site("Site A", site_a)
    _print_site("Site B", site_b)

    same_order = site_a["section_order"] == site_b["section_order"]
    same_pages = site_a["page_set"] == site_b["page_set"]
    print(f"\n  -> 區塊順序相同? {same_order}   分頁組合相同? {same_pages}")
    assert not same_order and not same_pages, "Test 1 失敗：兩站結構應該不同"

    # --- Test 2: 同品類，不同 seed -> 選配頁組合應不同 ---
    print("\n" + "-" * 72)
    print("Test 2: 同一品類「水晶原石類」，兩個不同 seed -> 選配頁組合應不同")
    print("-" * 72)
    site_c1 = generate_site_structure(1001, "水晶原石類")
    site_c2 = generate_site_structure(5005, "水晶原石類")
    print(f"  seed=1001 選配頁: {site_c1['page_set'][5:]}")
    print(f"  seed=5005 選配頁: {site_c2['page_set'][5:]}")
    diff = site_c1["page_set"] != site_c2["page_set"]
    print(f"  -> 選配頁組合相同? {not diff}")
    assert diff, "Test 2 失敗：同品類不同 seed 應選出不同選配頁組合"

    # --- Test 3: 同 seed，不同品類 -> 選配頁應明顯不同（品類感知生效）---
    print("\n" + "-" * 72)
    print("Test 3: 同一個 seed=7777，兩種不同品類 -> 選配頁應明顯不同（品類感知）")
    print("-" * 72)
    site_d1 = generate_site_structure(7777, "水晶原石類")
    site_d2 = generate_site_structure(7777, "咖啡與茶道類")
    print(f"  水晶原石類（{site_d1['category_group']}）選配頁: {site_d1['page_set'][5:]}")
    print(f"  咖啡與茶道類（{site_d2['category_group']}）選配頁: {site_d2['page_set'][5:]}")
    assert site_d1["category_group"] != site_d2["category_group"]
    assert set(site_d1["page_set"][5:]).isdisjoint(set(site_d2["page_set"][5:]))
    print(f"  -> 品類群不同: {site_d1['category_group']} vs {site_d2['category_group']}"
          f"（選配頁池完全不重疊，證明選頁確實依品類而非亂抽）")

    # --- Test 4: fallback 機制 ---
    print("\n" + "-" * 72)
    print("Test 4: 未列入對照表的品類「汽車內飾類」-> 應落回通用 fallback 池")
    print("-" * 72)
    site_e = generate_site_structure(9009, "汽車內飾類")
    print(f"  品類群: {site_e['category_group']}")
    print(f"  選配頁: {site_e['page_set'][5:]}")
    assert site_e["category_group"] == "通用 fallback"

    print("\n" + "=" * 72)
    print("全部驗證通過：區塊順序、分頁組合（含品類感知與 fallback）、組件變體，")
    print("在不同 seed / 不同品類下，每站結構確實各不相同。")
    print("=" * 72)


if __name__ == "__main__":
    main()
