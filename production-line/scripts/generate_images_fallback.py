"""
Generate Images Fallback - 多層圖片生成備援系統

⚠️ 這支腳本實際可用的層數是 2 層，不是 3 層。實測狀態（2026-08-05）：

  Tier 1  generate-image MCP (FLUX)  →  ❌ 本腳本未實作。
          MCP 只能從 Claude Code 環境呼叫，純 Python 執行時取不到。
          generate_tier1_flux() 現在會直接 raise NotImplementedError，
          不再靜默回 False 假裝「試過了但失敗」。
  Tier 2  source.unsplash.com        →  ❌ 端點已死。
          2026-08-05 實測 HTTP 503（Heroku Application Error），
          Unsplash 已於 2024 停用 source.unsplash.com。此層目前 100% 失敗。
  Tier 3  placehold.co               →  ✅ 可用，但這是唯一實際會生效的層。
  Tier 3b PIL 本地漸變                →  ✅ 可用（需安裝 Pillow）。

  結論：目前每一張圖都會落到 Tier 3 / 3b。
  ⚠️ 而 references/site-quality-rubric.md:8 把 placehold.co 列為「很 AI」的反例
     —— 也就是說本備援鏈的實際唯一產物，正是品質規範自己點名的反面教材。
     這個矛盾尚未解決，接真圖源（Unsplash 正式 API + key，或本地生圖模型）之前
     不要把本腳本的產出當成可上線的視覺素材。

Usage:
    python scripts/generate_images_fallback.py --category "Sustainable Home" --output hero.png
"""

import argparse
import requests
import random
import time
from pathlib import Path
from typing import Optional, Dict, List
import json

class ImageGenerationFallback:
    def __init__(self):
        self.unsplash_access_key = None  # 可從環境變數讀取
        self.placeholder_service = "https://placehold.co"

    def generate_tier1_flux(self, prompt: str, output_path: Path) -> bool:
        """
        ⚠️ Tier 1 未實作 —— 這是一個空殼，不要當成「有備援」。

        generate-image MCP (FLUX) 只能由 Claude Code 環境呼叫，
        這支純 Python 腳本沒有 MCP 通道，做不到。
        原本的實作是 `return False`，看起來像「試過但失敗」，
        會讓讀程式的人以為備援鏈有三層 —— 那是假的，所以改成明確拋錯。

        要用 FLUX 生圖，請在 Claude Code 內走 SlashCommand("/generate-image")，
        不要呼叫這個函式。

        TODO(未實作): 若要讓純 Python 也能生圖，需接本地生圖模型或生圖 API，
                      不是把這裡改回 return False 就算數。
        """
        raise NotImplementedError(
            "Tier 1 (generate-image MCP / FLUX) 未在本腳本實作："
            "MCP 只能從 Claude Code 環境呼叫，純 Python 無此通道。"
            "請改用 SlashCommand('/generate-image')，或接本地生圖模型。"
        )

    def generate_tier2_unsplash(self, category: str, output_path: Path) -> bool:
        """
        Tier 2: 從 Unsplash 下載高質量圖片
        """
        print("[Tier 2] 嘗試從 Unsplash 獲取圖片...")

        # 品類關鍵字映射
        category_keywords = {
            "sustainable home": ["sustainable", "eco friendly", "natural home"],
            "luxury jewelry": ["luxury jewelry", "gold", "diamond"],
            "artisan coffee": ["artisan coffee", "coffee beans", "cafe"],
            "tech gadgets": ["technology", "gadgets", "electronics"],
            "organic skincare": ["organic skincare", "natural cosmetics", "spa"],
            "fashion": ["fashion", "clothing", "style"],
            "furniture": ["furniture", "interior design", "home decor"],
            "food": ["gourmet food", "culinary", "cooking"]
        }

        # 獲取關鍵字
        keywords = category_keywords.get(category.lower(), [category])
        query = random.choice(keywords)

        try:
            # ⚠️ 這個端點已經死了，不是偶發失敗。
            # 2026-08-05 實測：GET https://source.unsplash.com/1920x1080/?coffee,beans
            #   → HTTP 503，回 Heroku 的 "Application Error" HTML（567 bytes），無轉址。
            # Unsplash 已於 2024 停用 source.unsplash.com 這個免 key 端點。
            # 也就是說本層目前必定失敗，每次都會落到 Tier 3 placehold.co。
            # 要修必須改用 Unsplash 正式 API（api.unsplash.com + Access Key，
            # 讀 self.unsplash_access_key / 環境變數），本輪未做。
            url = f"https://source.unsplash.com/1920x1080/?{query.replace(' ', ',')}"

            print(f"  查詢: {query}")

            response = requests.get(url, timeout=15, allow_redirects=True)

            if response.status_code == 200:
                output_path.write_bytes(response.content)
                print(f"  ✅ 成功從 Unsplash 下載圖片")
                print(f"  儲存至: {output_path}")
                return True
            else:
                print(f"  ❌ Unsplash API 返回 {response.status_code}")
                return False

        except Exception as e:
            print(f"  ❌ Unsplash 下載失敗: {str(e)}")
            return False

    def generate_tier3_placeholder(self, width: int, height: int, text: str, output_path: Path) -> bool:
        """
        Tier 3: 生成高質量 Placeholder（保底方案）
        """
        print("[Tier 3] 使用 Placeholder 保底方案...")

        try:
            # 使用 placehold.co 生成漂亮的 placeholder
            # 格式: https://placehold.co/1920x1080/png?text=Your+Text
            url = f"{self.placeholder_service}/{width}x{height}/2D3748/FFFFFF/png?text={text.replace(' ', '+')}"

            print(f"  生成: {width}x{height} placeholder")

            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                output_path.write_bytes(response.content)
                print(f"  ✅ 成功生成 Placeholder")
                print(f"  儲存至: {output_path}")
                return True
            else:
                print(f"  ❌ Placeholder 服務返回 {response.status_code}")
                return False

        except Exception as e:
            print(f"  ❌ Placeholder 生成失敗: {str(e)}")
            return False

    def generate_tier3_gradient(self, width: int, height: int, colors: List[str], output_path: Path) -> bool:
        """
        Tier 3b: 使用 PIL 生成漸變背景（本地備援）
        """
        print("[Tier 3b] 生成本地漸變圖片...")

        try:
            from PIL import Image, ImageDraw

            # 創建漸變背景
            img = Image.new('RGB', (width, height), color=colors[0])
            draw = ImageDraw.Draw(img)

            # 簡單的垂直漸變
            for i in range(height):
                ratio = i / height
                r = int(int(colors[0][1:3], 16) * (1 - ratio) + int(colors[1][1:3], 16) * ratio)
                g = int(int(colors[0][3:5], 16) * (1 - ratio) + int(colors[1][3:5], 16) * ratio)
                b = int(int(colors[0][5:7], 16) * (1 - ratio) + int(colors[1][5:7], 16) * ratio)
                draw.line([(0, i), (width, i)], fill=(r, g, b))

            img.save(output_path)
            print(f"  ✅ 成功生成漸變圖片")
            print(f"  儲存至: {output_path}")
            return True

        except ImportError:
            print("  ❌ PIL 未安裝，無法生成漸變圖片")
            return False
        except Exception as e:
            print(f"  ❌ 漸變生成失敗: {str(e)}")
            return False

    def generate(self, category: str, image_type: str, output_path: Path,
                 width: int = 1920, height: int = 1080, force_unsplash: bool = True) -> bool:
        """
        主要生成方法 - 強制優先使用 Unsplash

        Args:
            force_unsplash: 強制使用 Unsplash（預設 True），即使 generate-image 可用
        """
        print("=" * 60)
        print("Image Generation Fallback System")
        print("=" * 60)
        print(f"Category: {category}")
        print(f"Type: {image_type}")
        print(f"Output: {output_path}")
        print(f"Size: {width}x{height}")
        print(f"Force Unsplash: {force_unsplash}\n")

        # 強制優先使用 Unsplash（高質量免費圖庫）
        print("[Priority] 強制優先使用 Unsplash 高質量圖庫...")
        if self.generate_tier2_unsplash(category, output_path):
            return True

        print("\n⚠️ Unsplash 失敗，嘗試 Placeholder 保底方案...")
        time.sleep(1)

        # Tier 3: Placeholder（保底方案）
        placeholder_text = f"{category} - {image_type}"
        if self.generate_tier3_placeholder(width, height, placeholder_text, output_path):
            return True

        print("\n⚠️ Placeholder 失敗，嘗試本地漸變...")
        time.sleep(1)

        # Tier 3b: 本地漸變（最終保底）
        default_colors = ["#2D3748", "#4A5568"]  # 預設灰色漸變
        if self.generate_tier3_gradient(width, height, default_colors, output_path):
            return True

        print("\n❌ 所有圖片生成方案均失敗")
        return False

    def batch_generate(self, config_file: Path) -> Dict[str, bool]:
        """
        批次生成多張圖片

        config_file 格式:
        {
            "category": "Sustainable Home",
            "images": [
                {"type": "hero", "filename": "hero.png", "width": 1920, "height": 1080},
                {"type": "category1", "filename": "cat1.png", "width": 800, "height": 600},
                ...
            ]
        }
        """
        print("=" * 60)
        print("Batch Image Generation")
        print("=" * 60)

        config = json.loads(config_file.read_text(encoding="utf-8"))
        category = config["category"]
        images = config["images"]

        results = {}

        for img_config in images:
            print(f"\n[{img_config['type']}]")
            output_path = config_file.parent / img_config["filename"]

            success = self.generate(
                category=category,
                image_type=img_config["type"],
                output_path=output_path,
                width=img_config.get("width", 1920),
                height=img_config.get("height", 1080)
            )

            results[img_config["type"]] = success
            time.sleep(2)  # 避免請求過於頻繁

        print("\n" + "=" * 60)
        print("Batch Generation Summary")
        print("=" * 60)

        for img_type, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {img_type}")

        success_count = sum(results.values())
        total_count = len(results)
        print(f"\nSuccess Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")

        return results

def main():
    parser = argparse.ArgumentParser(description="Multi-tier image generation with fallback")
    parser.add_argument("--category", required=True, help="Product category (e.g., 'Sustainable Home')")
    parser.add_argument("--type", default="hero", help="Image type (e.g., 'hero', 'category')")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--width", type=int, default=1920, help="Image width")
    parser.add_argument("--height", type=int, default=1080, help="Image height")
    parser.add_argument("--batch", help="Batch mode: path to config JSON file")

    args = parser.parse_args()

    generator = ImageGenerationFallback()

    if args.batch:
        config_file = Path(args.batch)
        results = generator.batch_generate(config_file)
        success = all(results.values())
    else:
        output_path = Path(args.output)
        success = generator.generate(
            category=args.category,
            image_type=args.type,
            output_path=output_path,
            width=args.width,
            height=args.height
        )

    exit(0 if success else 1)

if __name__ == "__main__":
    main()
