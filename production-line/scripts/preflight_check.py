#!/usr/bin/env python3
"""
Pre-flight Check - 系統預檢腳本
在開始生成電商網站前，驗證所有必要的依賴與數據源
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class PreflightChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.skill_root = Path(__file__).parent.parent

    def check_node_version(self) -> bool:
        """檢查 Node.js 版本"""
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            version = result.stdout.strip().replace('v', '')
            major_version = int(version.split('.')[0])

            if major_version >= 18:
                print(f"{Colors.GREEN}✓{Colors.RESET} Node.js {version} (>= 18 required)")
                return True
            else:
                self.errors.append(f"Node.js version {version} is too old (>= 18 required)")
                return False
        except FileNotFoundError:
            self.errors.append("Node.js not found. Please install Node.js >= 18")
            return False

    def check_npm_version(self) -> bool:
        """檢查 npm 版本（Windows 上 npm 是 npm.cmd，需用 shutil.which 解析）"""
        import shutil
        npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
        if not npm_cmd:
            self.errors.append("npm not found")
            return False
        try:
            result = subprocess.run([npm_cmd, '--version'], capture_output=True, text=True)
            version = result.stdout.strip()
            major_version = int(version.split('.')[0])

            if major_version >= 9:
                print(f"{Colors.GREEN}✓{Colors.RESET} npm {version} (>= 9 required)")
                return True
            else:
                self.errors.append(f"npm version {version} is too old (>= 9 required)")
                return False
        except (FileNotFoundError, ValueError):
            self.errors.append("npm not found")
            return False

    def check_python_version(self) -> bool:
        """檢查 Python 版本"""
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            print(f"{Colors.GREEN}✓{Colors.RESET} Python {version.major}.{version.minor} (>= 3.8 required)")
            return True
        else:
            self.errors.append(f"Python {version.major}.{version.minor} is too old (>= 3.8 required)")
            return False

    def check_product_data_source(self) -> Tuple[bool, Dict]:
        """檢查商品數據源"""
        # 商品資料來源：先讀環境變數，沒設就用技能目錄底下的 data/
        base = os.environ.get("PRODUCT_DATA_DIR") or str(
            Path(__file__).resolve().parent.parent / "data")
        data_path = Path(base) / "extracted_products.json"

        if not data_path.exists():
            self.warnings.append(f"Product data source not found: {data_path}")
            print(f"{Colors.YELLOW}⚠{Colors.RESET} Product data not found (will use fallback)")
            return False, {}

        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 驗證數據結構
            if not isinstance(data, list):
                self.warnings.append("Product data is not a list")
                return False, {}

            valid_categories = [cat for cat in data if 'id' in cat and 'items' in cat]

            if len(valid_categories) >= 3:
                print(f"{Colors.GREEN}✓{Colors.RESET} Product data found ({len(valid_categories)} categories)")
                return True, {'categories': len(valid_categories), 'path': str(data_path)}
            else:
                self.warnings.append(f"Only {len(valid_categories)} valid categories (3+ recommended)")
                return False, {}

        except json.JSONDecodeError:
            self.warnings.append("Product data is not valid JSON")
            return False, {}
        except Exception as e:
            self.warnings.append(f"Error reading product data: {str(e)}")
            return False, {}

    def check_skill_dependency(self, skill_name: str, script_path: str) -> bool:
        """檢查技能依賴"""
        full_path = self.skill_root / script_path

        if full_path.exists():
            print(f"{Colors.GREEN}✓{Colors.RESET} {skill_name} available")
            return True
        else:
            self.errors.append(f"{skill_name} not found at {full_path}")
            return False

    def check_disk_space(self, required_mb: int = 500) -> bool:
        """檢查磁碟空間"""
        try:
            stat = shutil.disk_usage(self.skill_root)
            free_mb = stat.free / (1024 * 1024)

            if free_mb >= required_mb:
                print(f"{Colors.GREEN}✓{Colors.RESET} Disk space: {int(free_mb)} MB free (>= {required_mb} MB required)")
                return True
            else:
                self.warnings.append(f"Low disk space: {int(free_mb)} MB (>= {required_mb} MB recommended)")
                return False
        except Exception as e:
            self.warnings.append(f"Cannot check disk space: {str(e)}")
            return False

    def run_all_checks(self) -> Dict:
        """執行所有檢查"""
        print(f"\n{Colors.BLUE}═══════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BLUE}   Auto E-commerce Pre-flight Check{Colors.RESET}")
        print(f"{Colors.BLUE}═══════════════════════════════════════{Colors.RESET}\n")

        results = {
            'node': self.check_node_version(),
            'npm': self.check_npm_version(),
            'python': self.check_python_version(),
            'product_data': self.check_product_data_source()[0],
            'ui_ux_pro_max': self.check_skill_dependency(
                'ui-ux-pro-max',
                '.agent/skills/ui-ux-pro-max/scripts/search.py'
            ),
            'generate_image': self.check_skill_dependency(
                'generate-image',
                '.agent/skills/generate-image/scripts/generate_image.py'
            ),
            'disk_space': self.check_disk_space()
        }

        # 總結
        print(f"\n{Colors.BLUE}═══════════════════════════════════════{Colors.RESET}")

        critical_passed = all([results['node'], results['npm'], results['python']])
        recommended_passed = all([
            results['ui_ux_pro_max'],
            results['generate_image']
        ])

        if critical_passed and recommended_passed:
            print(f"{Colors.GREEN}✓ ALL CHECKS PASSED{Colors.RESET}")
            print(f"  System is ready for full automation mode")
            return_code = 0
        elif critical_passed:
            print(f"{Colors.YELLOW}⚠ PARTIAL PASS{Colors.RESET}")
            print(f"  Critical dependencies OK, but will use fallback mode")
            return_code = 1
        else:
            print(f"{Colors.RED}✗ CHECKS FAILED{Colors.RESET}")
            print(f"  Missing critical dependencies")
            return_code = 2

        # 顯示錯誤與警告
        if self.errors:
            print(f"\n{Colors.RED}Errors:{Colors.RESET}")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print(f"\n{Colors.YELLOW}Warnings:{Colors.RESET}")
            for warning in self.warnings:
                print(f"  • {warning}")

        print(f"\n{Colors.BLUE}═══════════════════════════════════════{Colors.RESET}\n")

        return {
            'success': critical_passed,
            'fallback_mode': not recommended_passed,
            'results': results,
            'errors': self.errors,
            'warnings': self.warnings,
            'return_code': return_code
        }

if __name__ == '__main__':
    checker = PreflightChecker()
    result = checker.run_all_checks()
    sys.exit(result['return_code'])
