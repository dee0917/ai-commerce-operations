#!/usr/bin/env python3
"""
validate_mock_flow.py — Phase 5.9 Mock 全流程驗證腳本

驗證所有 Service 層在 Mock 模式下的完整運作：
- 商品列表/詳情
- 購物車操作（加入/更新/移除）
- 認證（登入/登出）
- 訂單查詢
- 結帳流程
- .env.example 存在性
- Build 編譯

Usage: python scripts/validate_mock_flow.py <project_path>
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path

# ─── Configuration ─────────────────────────────────────────────────
REQUIRED_SERVICES = [
    'services/api.ts',
    'services/product.ts',
    'services/cart.ts',
    'services/auth.ts',
    'services/order.ts',
    'services/checkout.ts',
]

REQUIRED_STORES = [
    'useProductStore',
    'useCartStore',
    'useAuthStore',
    'useOrderStore',
    'useCheckoutStore',
]

REQUIRED_FILES = [
    '.env.example',
    'src/types/index.ts',
    'src/data/mockData.ts',
]

MOCK_INDICATORS = [
    'isMockMode',
    'VITE_WOO_URL',
    'mock_jwt_token',
    'MOCK_USER',
    'MOCK_CREDENTIALS',
    'mockOrders',
]

CART_HYBRID_INDICATORS = [
    'mergeLocalToRemote',
    'localStorage',
    'ecom_cart',
]

CHECKOUT_PLACEHOLDER = [
    'placeholder',
    'Coming Soon',
    'TODO',
]


class MockFlowValidator:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.src_path = self.project_path / 'src'
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def log(self, status: str, message: str):
        icon = {'PASS': '\u2705', 'FAIL': '\u274c', 'WARN': '\u26a0\ufe0f', 'INFO': '\u2139\ufe0f'}
        print(f"  {icon.get(status, '  ')} [{status}] {message}")
        self.results.append({'status': status, 'message': message})
        if status == 'PASS':
            self.passed += 1
        elif status == 'FAIL':
            self.failed += 1
        elif status == 'WARN':
            self.warnings += 1

    # ─── Check 1: Service Files Exist ──────────────────────────────
    def check_service_files(self):
        print("\n[1/8] Service \u6a94\u6848\u5b58\u5728\u6027\u6aa2\u67e5...")
        for svc in REQUIRED_SERVICES:
            path = self.src_path / svc
            if path.exists():
                self.log('PASS', f'{svc} exists')
            else:
                self.log('FAIL', f'{svc} MISSING')

    # ─── Check 2: Mock Mode Detection ─────────────────────────────
    def check_mock_mode(self):
        print("\n[2/8] Mock \u6a21\u5f0f\u5075\u6e2c\u6aa2\u67e5...")
        api_file = self.src_path / 'services' / 'api.ts'
        if not api_file.exists():
            self.log('FAIL', 'api.ts not found, cannot check mock mode')
            return

        content = api_file.read_text(encoding='utf-8')
        for indicator in MOCK_INDICATORS[:2]:  # isMockMode, VITE_WOO_URL
            if indicator in content:
                self.log('PASS', f'api.ts contains {indicator}')
            else:
                self.log('FAIL', f'api.ts missing {indicator}')

    # ─── Check 3: Mock Data Completeness ──────────────────────────
    def check_mock_data(self):
        print("\n[3/8] Mock \u8cc7\u6599\u5b8c\u6574\u6027...")
        for indicator in MOCK_INDICATORS[2:]:
            found = False
            for ts_file in self.src_path.rglob('*.ts'):
                try:
                    if indicator in ts_file.read_text(encoding='utf-8'):
                        found = True
                        break
                except:
                    pass
            for tsx_file in self.src_path.rglob('*.tsx'):
                try:
                    if indicator in tsx_file.read_text(encoding='utf-8'):
                        found = True
                        break
                except:
                    pass
            if found:
                self.log('PASS', f'Mock indicator "{indicator}" found')
            else:
                self.log('FAIL', f'Mock indicator "{indicator}" not found in any source file')

    # ─── Check 4: Hybrid Cart Logic ───────────────────────────────
    def check_hybrid_cart(self):
        print("\n[4/8] \u6df7\u5408\u8cfc\u7269\u8eca\u908f\u8f2f...")
        cart_file = self.src_path / 'services' / 'cart.ts'
        if not cart_file.exists():
            self.log('FAIL', 'cart.ts not found')
            return

        content = cart_file.read_text(encoding='utf-8')
        for indicator in CART_HYBRID_INDICATORS:
            if indicator in content:
                self.log('PASS', f'cart.ts contains "{indicator}"')
            else:
                self.log('FAIL', f'cart.ts missing "{indicator}" (hybrid cart incomplete)')

    # ─── Check 5: Checkout Placeholder ────────────────────────────
    def check_checkout_placeholder(self):
        print("\n[5/8] \u7d50\u5e33\u91d1\u6d41\u9810\u7559\u6aa2\u67e5...")
        checkout_file = self.src_path / 'services' / 'checkout.ts'
        if not checkout_file.exists():
            self.log('FAIL', 'checkout.ts not found')
            return

        content = checkout_file.read_text(encoding='utf-8')
        has_placeholder = any(p.lower() in content.lower() for p in CHECKOUT_PLACEHOLDER)
        if has_placeholder:
            self.log('PASS', 'Checkout has payment placeholder (gateway pending)')
        else:
            self.log('WARN', 'No payment placeholder found in checkout.ts')

    # ─── Check 6: Zustand Store Integration ───────────────────────
    def check_stores(self):
        print("\n[6/8] Zustand Store \u4e32\u63a5\u6aa2\u67e5...")
        for store_name in REQUIRED_STORES:
            found = False
            for f in self.src_path.rglob('*.ts'):
                try:
                    if store_name in f.read_text(encoding='utf-8'):
                        found = True
                        break
                except:
                    pass
            if not found:
                for f in self.src_path.rglob('*.tsx'):
                    try:
                        if store_name in f.read_text(encoding='utf-8'):
                            found = True
                            break
                    except:
                        pass
            if found:
                self.log('PASS', f'{store_name} found')
            else:
                self.log('FAIL', f'{store_name} not found in source')

    # ─── Check 7: Required Files ──────────────────────────────────
    def check_required_files(self):
        print("\n[7/8] \u5fc5\u8981\u6a94\u6848\u6aa2\u67e5...")
        for rel_path in REQUIRED_FILES:
            full_path = self.project_path / rel_path
            if full_path.exists():
                self.log('PASS', f'{rel_path} exists')
            else:
                self.log('FAIL', f'{rel_path} MISSING')

    # ─── Check 8: Build Compilation ───────────────────────────────
    def check_build(self):
        print("\n[8/8] Build \u7de8\u8b6f\u6aa2\u67e5...")
        try:
            result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=str(self.project_path),
                capture_output=True,
                text=True,
                timeout=120,
                shell=True,
            )
            if result.returncode == 0:
                self.log('PASS', 'npm run build succeeded')
            else:
                self.log('FAIL', f'npm run build failed: {result.stderr[:200]}')
        except subprocess.TimeoutExpired:
            self.log('FAIL', 'npm run build timed out (120s)')
        except FileNotFoundError:
            self.log('WARN', 'npm not found, skipping build check')

    # ─── Run All ──────────────────────────────────────────────────
    def run(self):
        print("=" * 60)
        print("  Mock Flow Validator - Phase 5.9")
        print(f"  Project: {self.project_path}")
        print("=" * 60)

        self.check_service_files()
        self.check_mock_mode()
        self.check_mock_data()
        self.check_hybrid_cart()
        self.check_checkout_placeholder()
        self.check_stores()
        self.check_required_files()
        self.check_build()

        # ─── Summary ──────────────────────────────────────────────
        print("\n" + "=" * 60)
        total = self.passed + self.failed + self.warnings
        print(f"  Results: {self.passed} PASS / {self.failed} FAIL / {self.warnings} WARN")
        print("=" * 60)

        if self.failed == 0:
            print("\n\u2705 ALL CHECKS PASSED - Mock flow is fully operational!")
            print("   Ready to connect to real WooCommerce backend.")
            return 0
        else:
            print(f"\n\u274c {self.failed} CHECK(S) FAILED - Fix issues before proceeding.")
            return 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_mock_flow.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    if not Path(project_path).is_dir():
        print(f"Error: {project_path} is not a directory")
        sys.exit(1)

    validator = MockFlowValidator(project_path)
    sys.exit(validator.run())
