#!/usr/bin/env python3
"""
inject_services.py — Phase 5 Service 層自動注入輔助腳本

在階段一前端驗收後，檢查項目狀態並準備 Service 層注入。
此腳本主要做前置檢查和目錄準備，實際 Service 代碼由 Claude Code 根據
service-layer-spec.md 和 cart-hybrid-spec.md 規格生成。

Usage: python scripts/inject_services.py <project_path> [--check-only]
"""

import os
import sys
import json
from pathlib import Path


SERVICE_FILES = {
    'api.ts': 'Shared API foundation (mock detection, wooFetch, nonce management)',
    'product.ts': 'ProductService (dual-mode product queries)',
    'cart.ts': 'CartService (hybrid localStorage / Store API cart)',
    'auth.ts': 'AuthService (JWT authentication with auto-refresh)',
    'order.ts': 'OrderService (order queries with Bearer Token)',
    'checkout.ts': 'CheckoutService (checkout framework, payment placeholder)',
}

STORE_FILES = {
    'useProductStore.ts': 'Product store → ProductService',
    'useCartStore.ts': 'Cart store → CartService (hybrid)',
    'useAuthStore.ts': 'Auth store → AuthService',
    'useOrderStore.ts': 'Order store → OrderService',
    'useCheckoutStore.ts': 'Checkout store → CheckoutService',
}


def check_prerequisites(project_path: Path) -> dict:
    """Check if the project is ready for service injection."""
    results = {'ready': True, 'checks': []}

    # Check package.json exists
    pkg = project_path / 'package.json'
    if pkg.exists():
        results['checks'].append(('PASS', 'package.json found'))
        pkg_data = json.loads(pkg.read_text(encoding='utf-8'))
        deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}

        # Check required deps
        for dep in ['react', 'zustand', 'react-router-dom']:
            if dep in deps:
                results['checks'].append(('PASS', f'{dep} installed'))
            else:
                results['checks'].append(('FAIL', f'{dep} not in dependencies'))
                results['ready'] = False
    else:
        results['checks'].append(('FAIL', 'package.json not found'))
        results['ready'] = False

    # Check src directory
    src = project_path / 'src'
    if src.is_dir():
        results['checks'].append(('PASS', 'src/ directory exists'))
    else:
        results['checks'].append(('FAIL', 'src/ directory not found'))
        results['ready'] = False

    # Check mockData exists
    mock_data = src / 'data' / 'mockData.ts'
    if mock_data.exists():
        results['checks'].append(('PASS', 'src/data/mockData.ts exists'))
    else:
        # Also check mockData.tsx
        mock_data_tsx = src / 'data' / 'mockData.tsx'
        if mock_data_tsx.exists():
            results['checks'].append(('PASS', 'src/data/mockData.tsx exists'))
        else:
            results['checks'].append(('WARN', 'mockData.ts not found (will need to create)'))

    # Check types
    types_file = src / 'types' / 'index.ts'
    if types_file.exists():
        results['checks'].append(('PASS', 'src/types/index.ts exists'))
    else:
        results['checks'].append(('WARN', 'src/types/index.ts not found (will create)'))

    # Check existing services directory
    services = src / 'services'
    if services.is_dir():
        existing = [f.name for f in services.iterdir() if f.suffix in ('.ts', '.tsx')]
        if existing:
            results['checks'].append(('INFO', f'Existing services: {", ".join(existing)}'))
        else:
            results['checks'].append(('INFO', 'services/ exists but empty'))
    else:
        results['checks'].append(('INFO', 'services/ will be created'))

    # Check existing stores
    stores = src / 'stores'
    if not stores.is_dir():
        stores = src / 'store'
    if stores.is_dir():
        existing = [f.name for f in stores.iterdir() if f.suffix in ('.ts', '.tsx')]
        results['checks'].append(('INFO', f'Existing stores: {", ".join(existing)}'))
    else:
        results['checks'].append(('INFO', 'No stores/ directory found'))

    # Check build works
    node_modules = project_path / 'node_modules'
    if node_modules.is_dir():
        results['checks'].append(('PASS', 'node_modules exists'))
    else:
        results['checks'].append(('WARN', 'node_modules not found — run npm install first'))

    return results


def prepare_directories(project_path: Path):
    """Create directories needed for service injection."""
    src = project_path / 'src'

    dirs_to_create = [
        src / 'services',
        src / 'types',
        src / 'hooks',
    ]

    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  \u2705 {d.relative_to(project_path)}/")


def generate_env_example(project_path: Path):
    """Generate .env.example file."""
    env_content = """# ═══════════════════════════════════════════
# E-Commerce Configuration
# ═══════════════════════════════════════════

# WordPress / WooCommerce Backend URL
# Leave EMPTY for Mock mode (frontend-only demo)
# Fill in to connect to real WooCommerce backend
VITE_WOO_URL=

# ═══════════════════════════════════════════
# Backend-only (NEVER in frontend bundle)
# Used by scripts/sync-to-wp.mjs only
# ═══════════════════════════════════════════
WOO_CONSUMER_KEY=
WOO_CONSUMER_SECRET=
"""
    env_path = project_path / '.env.example'
    env_path.write_text(env_content.strip() + '\n', encoding='utf-8')
    print(f"  \u2705 .env.example generated")


def print_injection_plan():
    """Print the service injection plan."""
    print("\n" + "=" * 60)
    print("  Service Injection Plan")
    print("=" * 60)

    print("\n  src/services/ (6 files):")
    for fname, desc in SERVICE_FILES.items():
        print(f"    \u2192 {fname}: {desc}")

    print("\n  src/stores/ (5 files to modify/create):")
    for fname, desc in STORE_FILES.items():
        print(f"    \u2192 {fname}: {desc}")

    print("\n  Additional files:")
    print("    \u2192 .env.example: Environment variable template")
    print("    \u2192 src/types/index.ts: WooCommerce type definitions")
    print("    \u2192 src/hooks/useAuth.ts: Enhanced auth hook")

    print("\n  Reference specs:")
    print("    \u2192 references/service-layer-spec.md")
    print("    \u2192 references/cart-hybrid-spec.md")
    print("    \u2192 references/woocommerce-api.md")
    print("    \u2192 references/member-zone.md")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/inject_services.py <project_path> [--check-only]")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    check_only = '--check-only' in sys.argv

    if not project_path.is_dir():
        print(f"Error: {project_path} is not a directory")
        sys.exit(1)

    print("=" * 60)
    print("  Service Layer Injection - Phase 5 Preparation")
    print(f"  Project: {project_path}")
    print("=" * 60)

    # Run checks
    print("\n\U0001f50d Pre-injection checks...")
    results = check_prerequisites(project_path)

    icons = {'PASS': '\u2705', 'FAIL': '\u274c', 'WARN': '\u26a0\ufe0f', 'INFO': '\u2139\ufe0f'}
    for status, msg in results['checks']:
        print(f"  {icons[status]} [{status}] {msg}")

    if check_only:
        if results['ready']:
            print("\n\u2705 Project is ready for service injection!")
        else:
            print("\n\u274c Project has issues that need to be resolved first.")
        sys.exit(0 if results['ready'] else 1)

    if not results['ready']:
        print("\n\u274c Cannot proceed — fix the FAIL items above first.")
        sys.exit(1)

    # Prepare
    print("\n\U0001f4c1 Preparing directories...")
    prepare_directories(project_path)

    print("\n\U0001f4dd Generating .env.example...")
    generate_env_example(project_path)

    # Print plan
    print_injection_plan()

    print("\n" + "=" * 60)
    print("  \u2705 Preparation complete!")
    print("  Next: Claude Code will inject service files per spec.")
    print("=" * 60)
