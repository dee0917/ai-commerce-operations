#!/usr/bin/env python3
"""
Product Data Loader - 商品數據載入與轉換腳本
自動從 progress-report 專案讀取商品數據，轉換為 mockData.ts 格式
"""

import os
import sys
import json
import random
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class ProductDataLoader:
    def __init__(self, data_dir: str = r"`<商品資料目錄>`"):
        self.data_dir = Path(data_dir)
        self.extracted_products_path = self.data_dir / "extracted_products.json"
        # 2026-08-06 廢除：used_categories.json 是獨立檔，跟 design-history.json 兩套帳必然脫節
        # （C3 破口）。品類去重改讀 design-history.json 的 category 欄位——單一真相。
        self.design_history_path = (Path(__file__).parent.parent / "data" / "design-history.json")
        self.output_dir = Path(__file__).parent.parent / "temp"
        self.output_dir.mkdir(exist_ok=True)

        # Fallback 商品分類池 (當數據源不可用時)
        self.fallback_categories = [
            {
                "id": "## Luxury Jewelry",
                "name": "Luxury Jewelry",
                "items": [
                    {"name": "Diamond Necklace", "description": "Elegant 18K white gold necklace"},
                    {"name": "Sapphire Ring", "description": "Royal blue sapphire engagement ring"},
                    {"name": "Pearl Earrings", "description": "Tahitian pearl drop earrings"},
                    {"name": "Gold Bracelet", "description": "24K gold chain bracelet"},
                    {"name": "Ruby Pendant", "description": "Heart-shaped ruby pendant"},
                ]
            },
            {
                "id": "## Artisan Coffee",
                "name": "Artisan Coffee",
                "items": [
                    {"name": "Ethiopian Yirgacheffe", "description": "Single-origin floral notes"},
                    {"name": "Colombian Supremo", "description": "Smooth medium roast"},
                    {"name": "Sumatra Mandheling", "description": "Bold earthy flavor"},
                    {"name": "Kenya AA", "description": "Bright citrus acidity"},
                    {"name": "Costa Rica Tarrazu", "description": "Honey process sweet finish"},
                ]
            },
            {
                "id": "## Organic Skincare",
                "name": "Organic Skincare",
                "items": [
                    {"name": "Rose Water Toner", "description": "Hydrating facial toner"},
                    {"name": "Vitamin C Serum", "description": "Brightening anti-aging serum"},
                    {"name": "Hyaluronic Moisturizer", "description": "Deep hydration cream"},
                    {"name": "Charcoal Face Mask", "description": "Detoxifying clay mask"},
                    {"name": "Retinol Night Cream", "description": "Overnight renewal treatment"},
                ]
            },
            {
                "id": "## Sustainable Fashion",
                "name": "Sustainable Fashion",
                "items": [
                    {"name": "Organic Cotton T-Shirt", "description": "Fair trade basic tee"},
                    {"name": "Recycled Denim Jeans", "description": "Eco-friendly slim fit"},
                    {"name": "Bamboo Hoodie", "description": "Soft breathable hoodie"},
                    {"name": "Hemp Sneakers", "description": "Vegan casual shoes"},
                    {"name": "Linen Shirt", "description": "Natural fiber button-down"},
                ]
            },
            {
                "id": "## Home Fragrance",
                "name": "Home Fragrance",
                "items": [
                    {"name": "Lavender Candle", "description": "Relaxing aromatherapy candle"},
                    {"name": "Sandalwood Incense", "description": "Meditative woody scent"},
                    {"name": "Eucalyptus Diffuser", "description": "Refreshing reed diffuser"},
                    {"name": "Vanilla Room Spray", "description": "Warm comforting mist"},
                    {"name": "Citrus Wax Melts", "description": "Energizing wax cubes"},
                ]
            }
        ]

    def load_extracted_products(self) -> Optional[List[Dict]]:
        """載入 extracted_products.json"""
        if not self.extracted_products_path.exists():
            print(f"⚠️  Product data not found: {self.extracted_products_path}")
            print(f"📦 Using fallback category pool")
            return None

        try:
            with open(self.extracted_products_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list) or len(data) == 0:
                print(f"⚠️  Invalid product data format")
                return None

            print(f"✓ Loaded {len(data)} categories from extracted_products.json")
            return data

        except Exception as e:
            print(f"⚠️  Error loading product data: {str(e)}")
            return None

    def load_used_categories(self) -> List[str]:
        """已使用的分類直接讀 design-history.json 的 category 欄位（單一真相）。
        排除 abandoned；沒有 category 欄位的舊筆自然被忽略。"""
        if not self.design_history_path.exists():
            return []
        try:
            with open(self.design_history_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cats = set()
            for e in data.get('generations', []):
                if e.get('status') == 'abandoned':
                    continue
                cat = (e.get('category') or '').strip()
                if cat:
                    cats.add(cat)
            return sorted(cats)
        except Exception as e:
            print(f"⚠️  Error reading design-history.json for used categories: {str(e)}")
            return []

    def save_used_category(self, category_id: str, used_categories: List[str]):
        """2026-08-06 起這裡不再寫檔。記錄的責任在 Phase 1.05 那一步——DNA 訂位時的
        `design_history.py reserve --category` 本來就必填這個欄位，寫兩處只會兩套帳兜不上。
        這裡保留函式簽名避免舊呼叫端炸掉，並提醒接下來要做什麼。"""
        print(f"ℹ️  品類選定：{category_id}（不再寫 used_categories.json；"
              f"確保稍後 design_history.py reserve --category \"{category_id}\" 有真的執行，"
              f"去重才會生效）")

    def select_random_category(self) -> Dict:
        """隨機選擇一個未使用的分類"""
        # 嘗試載入真實數據
        categories = self.load_extracted_products()

        # 使用 Fallback
        if categories is None:
            categories = self.fallback_categories

        # 載入已使用的分類
        used_categories = self.load_used_categories()

        # 過濾未使用的分類：用 id 比對（extracted_products.json 真實 schema是
        # {id, title, items}，沒有 name 欄位）。⚠️ design-history.json 舊筆的 category
        # 存的是英文品牌化分類（如 "Talisman"），跟這裡的中文原始 id 對不上，舊筆天生比不中——
        # 跟之前 used_categories.json 停在 3 月是同一種「事實上沒在擋」，不是新退步。
        # 往後 reserve --category 要填這裡選中的 cat['id'] 原始字串，比對才會真的生效。
        available = [cat for cat in categories if cat.get('id') not in used_categories]

        # 若全部用完：design-history.json 是永久紀錄不會清空，用完全部分類代表一輪跑完，
        # 直接進下一輪即可（等同原本「重置」的效果，但不用清資料）。
        if not available:
            print(f"🔄 All categories used (design-history.json 已涵蓋全部分類)，開始新一輪")
            available = categories

        # 隨機選擇
        selected = random.choice(available)

        # 記錄已使用
        self.save_used_category(selected['id'], used_categories)

        print(f"🎲 Selected category: {selected.get('name', selected['id'])}")
        return selected

    def format_product_label(self, name: str, description: str = "") -> str:
        """
        ⚠️ 這個函式不做翻譯。它只把商品名與描述併成一個顯示用標籤，原文照回。

        原名為 translate_to_english()，但實作從來沒有翻譯過任何字，
        名稱與行為不符 → 已改名為實際行為。
        輸入是中文就輸出中文，不要當成「已經是英文」使用。

        TODO(未實作): 要真的翻譯必須接翻譯服務（Google Translate API 或 LLM）。
                      在接上之前，非英文來源的商品資料不適合直接上英文站。
        """
        return f"{name} ({description})" if description else name

    def generate_mock_data(self, category: Dict) -> List[Dict]:
        """生成 mockData.ts 格式的商品數據"""
        items = category.get('items', [])[:12]  # 最多 12 個商品

        mock_products = []

        for idx, item in enumerate(items):
            name = item.get('name', f'Product {idx+1}')
            description = item.get('description', '')

            # 顯示用標籤（注意：不是翻譯，原文照回，見 format_product_label docstring）
            display_label = self.format_product_label(name, description)

            # 生成 slug
            slug = display_label.lower().replace(' ', '-').replace('(', '').replace(')', '')[:50]

            # 隨機價格
            base_price = random.randint(20, 200)

            # salePrice 恆為 None，禁止產生折扣價。
            # 規則：示範資料沒有 30 天最低價基準，標劃線原價違反 UK DMCCA / EU Omnibus。
            #       見 PITFALLS.md:106（salePrice 帶值就要攔）
            #       與 references/anti-patterns.md:186（Mock 資料站一律不得劃線）。
            # 保留欄位、值恆為 None：合規閘門 ecommerce-checklist.py:540-544 明定
            #       salePrice: null 代表「這個商品沒有特價」，不算違規。
            # 不要把隨機折扣加回來 —— 那等於本 repo 自己生產自己合規閘門要擋的違法資料。
            sale_price = None

            product = {
                'id': f'prod-{idx+1:03d}',
                'slug': slug,
                'name': display_label,
                'description': description or f'High-quality {display_label.lower()}',
                'price': base_price,
                'salePrice': sale_price,
                'category': category.get('name', 'General'),
                'images': [
                    f'/images/products/{slug}-1.jpg',
                    f'/images/products/{slug}-2.jpg',
                ],
                'inStock': True,
                'stock': random.randint(5, 50),
                'rating': round(random.uniform(4.0, 5.0), 1),
                'reviews': random.randint(10, 200)
            }

            mock_products.append(product)

        return mock_products

    def run(self, validate: bool = False, auto_fix: bool = False) -> Dict:
        """執行完整流程"""
        print(f"\n{'='*50}")
        print(f"  Product Data Loader")
        print(f"{'='*50}\n")

        # 選擇分類
        selected_category = self.select_random_category()

        # 生成 Mock Data
        mock_products = self.generate_mock_data(selected_category)

        # 儲存輸出
        category_output = self.output_dir / "selected_category.json"
        products_output = self.output_dir / "products_for_mockdata.json"

        with open(category_output, 'w', encoding='utf-8') as f:
            json.dump(selected_category, f, ensure_ascii=False, indent=2)

        with open(products_output, 'w', encoding='utf-8') as f:
            json.dump(mock_products, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Generated {len(mock_products)} products")
        print(f"✓ Saved to: {products_output}")

        return {
            'category': selected_category,
            'products': mock_products,
            'output_path': str(products_output)
        }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load and convert product data')
    parser.add_argument('--validate', action='store_true', help='Validate data structure')
    parser.add_argument('--auto-fix', action='store_true', help='Auto-fix data issues')
    args = parser.parse_args()

    loader = ProductDataLoader()
    result = loader.run(validate=args.validate, auto_fix=args.auto_fix)

    print(f"\n{'='*50}\n")
    sys.exit(0)
