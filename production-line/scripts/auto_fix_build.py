"""
Auto Fix Build - TypeScript 錯誤自動修復引擎
自動檢測並修復常見的 TypeScript 編譯錯誤

Usage:
    python scripts/auto_fix_build.py [project_path]
"""

import subprocess
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import sys

class TypeScriptAutoFixer:
    def __init__(self, project_path: str = "."):
        self.project_root = Path(project_path).resolve()
        self.max_iterations = 5
        self.fixed_errors = []

    def run_build(self) -> Tuple[bool, str]:
        """執行 npm run build 並捕獲錯誤"""
        import shutil
        npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
        if not npm_cmd:
            return False, "npm not found"
        try:
            result = subprocess.run(
                [npm_cmd, "run", "build"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0, result.stderr + result.stdout
        except subprocess.TimeoutExpired:
            return False, "Build timeout after 120 seconds"
        except Exception as e:
            return False, f"Build error: {str(e)}"

    def parse_typescript_errors(self, build_output: str) -> List[Dict]:
        """解析 TypeScript 錯誤訊息"""
        errors = []

        # Pattern 1: src/path/file.tsx(12,5): error TS2322: Type 'string' is not assignable to type 'number'
        pattern1 = r"([^(]+)\((\d+),(\d+)\): error (TS\d+): (.+)"

        # Pattern 2: src/path/file.tsx:12:5 - error TS2322: Type 'string' is not assignable to type 'number'
        pattern2 = r"([^:]+):(\d+):(\d+) - error (TS\d+): (.+)"

        for match in re.finditer(pattern1, build_output):
            errors.append({
                "file": match.group(1).strip(),
                "line": int(match.group(2)),
                "column": int(match.group(3)),
                "code": match.group(4),
                "message": match.group(5).strip()
            })

        for match in re.finditer(pattern2, build_output):
            errors.append({
                "file": match.group(1).strip(),
                "line": int(match.group(2)),
                "column": int(match.group(3)),
                "code": match.group(4),
                "message": match.group(5).strip()
            })

        return errors

    def fix_missing_import(self, file_path: Path, error: Dict) -> bool:
        """修復缺少的 import 聲明"""
        # TS2304: Cannot find name 'X'
        if error["code"] != "TS2304":
            return False

        match = re.search(r"Cannot find name '(\w+)'", error["message"])
        if not match:
            return False

        missing_name = match.group(1)

        # 常見的 React/TypeScript import
        import_map = {
            "React": "import React from 'react';",
            "useState": "import { useState } from 'react';",
            "useEffect": "import { useEffect } from 'react';",
            "useContext": "import { useContext } from 'react';",
            "useRef": "import { useRef } from 'react';",
            "useMemo": "import { useMemo } from 'react';",
            "useCallback": "import { useCallback } from 'react';",
            "Link": "import { Link } from 'react-router-dom';",
            "useNavigate": "import { useNavigate } from 'react-router-dom';",
            "useParams": "import { useParams } from 'react-router-dom';",
            "motion": "import { motion } from 'framer-motion';",
        }

        if missing_name not in import_map:
            return False

        content = file_path.read_text(encoding="utf-8")
        import_statement = import_map[missing_name]

        # 檢查是否已存在
        if import_statement in content:
            return False

        # 在第一個非空行前插入
        lines = content.split("\n")
        insert_index = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith("//"):
                insert_index = i
                break

        lines.insert(insert_index, import_statement)
        file_path.write_text("\n".join(lines), encoding="utf-8")

        self.fixed_errors.append({
            "type": "missing_import",
            "file": str(file_path),
            "fix": f"Added {import_statement}"
        })

        return True

    def fix_type_annotation(self, file_path: Path, error: Dict) -> bool:
        """修復類型註解問題"""
        # TS7006: Parameter 'x' implicitly has an 'any' type
        if error["code"] != "TS7006":
            return False

        match = re.search(r"Parameter '(\w+)' implicitly has an 'any' type", error["message"])
        if not match:
            return False

        param_name = match.group(1)
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        if error["line"] - 1 >= len(lines):
            return False

        line = lines[error["line"] - 1]

        # 嘗試自動推斷類型
        # 常見模式: (e) => ... → (e: React.MouseEvent) => ...
        if "onClick" in line or "onSubmit" in line or "onChange" in line:
            new_line = line.replace(f"({param_name})", f"({param_name}: React.FormEvent)")
            lines[error["line"] - 1] = new_line
            file_path.write_text("\n".join(lines), encoding="utf-8")

            self.fixed_errors.append({
                "type": "type_annotation",
                "file": str(file_path),
                "fix": f"Added type annotation for {param_name}"
            })

            return True

        return False

    def fix_unused_variable(self, file_path: Path, error: Dict) -> bool:
        """修復未使用的變數警告"""
        # TS6133: 'x' is declared but its value is never read
        if error["code"] != "TS6133":
            return False

        match = re.search(r"'(\w+)' is declared but", error["message"])
        if not match:
            return False

        var_name = match.group(1)
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        if error["line"] - 1 >= len(lines):
            return False

        line = lines[error["line"] - 1]

        # 如果是 const/let/var 聲明，加上 _ 前綴
        if re.search(rf"\b(const|let|var)\s+{var_name}\b", line):
            new_line = re.sub(rf"\b{var_name}\b", f"_{var_name}", line)
            lines[error["line"] - 1] = new_line
            file_path.write_text("\n".join(lines), encoding="utf-8")

            self.fixed_errors.append({
                "type": "unused_variable",
                "file": str(file_path),
                "fix": f"Prefixed unused variable {var_name} with _"
            })

            return True

        return False

    def fix_missing_return_type(self, file_path: Path, error: Dict) -> bool:
        """修復缺少返回類型"""
        # TS7010: Function lacks return type annotation
        if error["code"] != "TS7010":
            return False

        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        if error["line"] - 1 >= len(lines):
            return False

        line = lines[error["line"] - 1]

        # 如果是箭頭函數或函數聲明，添加 void 返回類型
        if "=>" in line and ":" not in line.split("=>")[0]:
            # const func = () => { ... } → const func = (): void => { ... }
            new_line = re.sub(r"\)\s*=>", "): void =>", line)
            if new_line != line:
                lines[error["line"] - 1] = new_line
                file_path.write_text("\n".join(lines), encoding="utf-8")

                self.fixed_errors.append({
                    "type": "return_type",
                    "file": str(file_path),
                    "fix": "Added void return type"
                })

                return True

        return False

    def fix_property_does_not_exist(self, file_path: Path, error: Dict) -> bool:
        """修復屬性不存在錯誤"""
        # TS2339: Property 'x' does not exist on type 'Y'
        if error["code"] != "TS2339":
            return False

        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        if error["line"] - 1 >= len(lines):
            return False

        line = lines[error["line"] - 1]

        # 常見模式: process.env.VITE_XXX
        if "process.env" in line:
            # 在文件開頭添加類型聲明
            type_declaration = """
declare global {
  interface ImportMetaEnv {
    [key: string]: string | undefined;
  }
}
""".strip()

            if type_declaration not in content:
                lines.insert(0, type_declaration)
                lines.insert(1, "")
                file_path.write_text("\n".join(lines), encoding="utf-8")

                self.fixed_errors.append({
                    "type": "env_type",
                    "file": str(file_path),
                    "fix": "Added ImportMetaEnv type declaration"
                })

                return True

        return False

    def apply_fixes(self, errors: List[Dict]) -> int:
        """應用所有修復"""
        fixed_count = 0

        for error in errors:
            file_path = self.project_root / error["file"]

            if not file_path.exists():
                continue

            # 嘗試所有修復策略
            fixed = (
                self.fix_missing_import(file_path, error) or
                self.fix_type_annotation(file_path, error) or
                self.fix_unused_variable(file_path, error) or
                self.fix_missing_return_type(file_path, error) or
                self.fix_property_does_not_exist(file_path, error)
            )

            if fixed:
                fixed_count += 1

        return fixed_count

    def run(self) -> bool:
        """主執行流程"""
        print("=" * 60)
        print("TypeScript Auto-Fix Engine")
        print("=" * 60)
        print(f"Project: {self.project_root}\n")

        for iteration in range(1, self.max_iterations + 1):
            print(f"\n[Iteration {iteration}/{self.max_iterations}]")
            print("-" * 60)

            # 執行 build
            success, output = self.run_build()

            if success:
                print("✅ Build succeeded!")
                if self.fixed_errors:
                    print(f"\n🔧 Total fixes applied: {len(self.fixed_errors)}")
                    for fix in self.fixed_errors:
                        print(f"  - {fix['type']}: {fix['file']}")
                return True

            # 解析錯誤
            errors = self.parse_typescript_errors(output)

            if not errors:
                print("❌ Build failed but no TypeScript errors detected")
                print("\nBuild output:")
                print(output[-500:])  # 顯示最後 500 字元
                return False

            print(f"Found {len(errors)} TypeScript errors")

            # 應用修復
            fixed_count = self.apply_fixes(errors)

            print(f"Fixed {fixed_count} errors in this iteration")

            if fixed_count == 0:
                print("\n⚠️ No automatic fixes available for remaining errors")
                print("\nRemaining errors:")
                for error in errors[:5]:  # 顯示前 5 個錯誤
                    print(f"  {error['file']}:{error['line']} - {error['code']}: {error['message']}")
                return False

        print(f"\n❌ Reached maximum iterations ({self.max_iterations})")
        return False

def main():
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."

    fixer = TypeScriptAutoFixer(project_path)
    success = fixer.run()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
