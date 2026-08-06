"""
Auto Test and Fix - 自動化測試與修復編排引擎
整合所有自動化腳本，實現完全自動化的品質保證流程

執行順序:
1. Preflight Check (系統檢查)
2. Build + Auto Fix (編譯 + 自動修復)
3. Image Generation Fallback (圖片生成)
4. Start Dev Server (啟動預覽)
5. Run Quality Checklist (品質檢查)
6. Generate Report (生成報告)

Usage:
    python scripts/auto_test_and_fix.py [project_path]
"""

import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple
import sys

class AutoTestAndFix:
    def __init__(self, project_path: str = "."):
        self.project_root = Path(project_path).resolve()
        self.scripts_dir = Path(__file__).parent
        self.results = {
            "preflight": None,
            "build": None,
            "images": None,
            "server": None,
            "quality": None
        }

    def run_script(self, script_name: str, args: List[str] = None) -> Tuple[bool, str]:
        """執行 Python 腳本"""
        script_path = self.scripts_dir / script_name
        cmd = ["python", str(script_path)]

        if args:
            cmd.extend(args)

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )

            output = result.stdout + result.stderr
            return result.returncode == 0, output

        except subprocess.TimeoutExpired:
            return False, f"Timeout after 300 seconds"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def run_npm_command(self, command: str, timeout: int = 120) -> Tuple[bool, str]:
        """執行 npm 命令"""
        try:
            result = subprocess.run(
                ["npm", "run", command],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            output = result.stdout + result.stderr
            return result.returncode == 0, output

        except subprocess.TimeoutExpired:
            return False, f"Timeout after {timeout} seconds"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def phase_preflight(self) -> bool:
        """Phase -1: Preflight Check"""
        print("\n" + "=" * 60)
        print("Phase -1: Preflight Check")
        print("=" * 60)

        success, output = self.run_script("preflight_check.py")

        self.results["preflight"] = {
            "success": success,
            "output": output[-500:]  # 保存最後 500 字元
        }

        if success:
            print("✅ Preflight check passed")
        else:
            print("⚠️ Preflight check failed (continuing with fallback mode)")
            print(output[-300:])

        # Preflight 失敗不阻斷流程，繼續執行
        return True

    def phase_build(self) -> bool:
        """Phase 1: Build + Auto Fix"""
        print("\n" + "=" * 60)
        print("Phase 1: Build + Auto Fix")
        print("=" * 60)

        success, output = self.run_script("auto_fix_build.py", [str(self.project_root)])

        self.results["build"] = {
            "success": success,
            "output": output[-500:]
        }

        if success:
            print("✅ Build succeeded (with auto-fixes)")
            return True
        else:
            print("❌ Build failed even after auto-fixes")
            print(output[-300:])
            return False

    def phase_images(self) -> bool:
        """Phase 2: Image Generation"""
        print("\n" + "=" * 60)
        print("Phase 2: Image Generation")
        print("=" * 60)

        # 檢查是否有圖片配置檔案
        img_config = self.project_root / "image_config.json"

        if not img_config.exists():
            print("⚠️ No image_config.json found, skipping image generation")
            self.results["images"] = {"success": True, "skipped": True}
            return True

        success, output = self.run_script(
            "generate_images_fallback.py",
            ["--batch", str(img_config)]
        )

        self.results["images"] = {
            "success": success,
            "output": output[-500:]
        }

        if success:
            print("✅ All images generated successfully")
        else:
            print("⚠️ Some images failed (using fallback)")
            # 圖片失敗不阻斷流程

        return True

    def phase_server(self) -> bool:
        """Phase 3: Start Dev Server"""
        print("\n" + "=" * 60)
        print("Phase 3: Start Dev Server")
        print("=" * 60)

        # 檢查 dev server 是否已在運行
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 5173))
            sock.close()

            if result == 0:
                print("✅ Dev server already running on http://localhost:5173")
                self.results["server"] = {"success": True, "already_running": True}
                return True

        except Exception:
            pass

        # 啟動 dev server（背景執行）
        print("Starting dev server in background...")

        try:
            subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # 等待 server 啟動
            print("Waiting for server to start...")
            max_wait = 30
            for i in range(max_wait):
                time.sleep(1)
                try:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex(('localhost', 5173))
                    sock.close()

                    if result == 0:
                        print(f"✅ Server started after {i+1} seconds")
                        self.results["server"] = {"success": True, "start_time": i+1}
                        return True
                except Exception:
                    pass

            print("⚠️ Server did not start within 30 seconds")
            self.results["server"] = {"success": False, "timeout": True}
            return False

        except Exception as e:
            print(f"❌ Failed to start server: {str(e)}")
            self.results["server"] = {"success": False, "error": str(e)}
            return False

    def phase_quality(self) -> bool:
        """Phase 4: Quality Checklist"""
        print("\n" + "=" * 60)
        print("Phase 4: Quality Checklist")
        print("=" * 60)

        # 檢查是否有 ecommerce-checklist.py
        checklist_script = self.scripts_dir / "ecommerce-checklist.py"

        if not checklist_script.exists():
            print("⚠️ ecommerce-checklist.py not found, skipping quality check")
            self.results["quality"] = {"success": True, "skipped": True}
            return True

        success, output = self.run_script(
            "ecommerce-checklist.py",
            ["--preview"]
        )

        self.results["quality"] = {
            "success": success,
            "output": output[-500:]
        }

        if success:
            print("✅ Quality checklist passed")
        else:
            print("⚠️ Quality checklist found issues")
            print(output[-300:])

        # Quality check 失敗不阻斷流程
        return True

    def generate_report(self) -> Dict:
        """生成最終報告"""
        print("\n" + "=" * 60)
        print("Final Report")
        print("=" * 60)

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project": str(self.project_root),
            "phases": self.results,
            "summary": {
                "total_phases": 5,
                "passed_phases": sum(
                    1 for phase in self.results.values()
                    if phase and phase.get("success", False)
                ),
                "critical_failures": []
            }
        }

        # 檢查關鍵失敗
        if not self.results["build"]["success"]:
            report["summary"]["critical_failures"].append("Build failed")

        if not self.results["server"]["success"]:
            report["summary"]["critical_failures"].append("Server failed to start")

        # 打印摘要
        print(f"\nPassed Phases: {report['summary']['passed_phases']}/{report['summary']['total_phases']}")

        if report["summary"]["critical_failures"]:
            print("\n❌ Critical Failures:")
            for failure in report["summary"]["critical_failures"]:
                print(f"  - {failure}")
        else:
            print("\n✅ All critical phases passed")

        # 儲存報告
        report_file = self.project_root / "AUTO_TEST_REPORT.json"
        report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"\n📊 Report saved to: {report_file}")

        return report

    def run(self) -> bool:
        """執行完整流程"""
        print("=" * 60)
        print("Auto Test and Fix - Orchestrator")
        print("=" * 60)
        print(f"Project: {self.project_root}")
        print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        start_time = time.time()

        # Phase -1: Preflight
        if not self.phase_preflight():
            print("\n⚠️ Preflight failed, but continuing...")

        # Phase 1: Build
        if not self.phase_build():
            print("\n❌ Build failed, aborting")
            self.generate_report()
            return False

        # Phase 2: Images
        self.phase_images()

        # Phase 3: Server
        if not self.phase_server():
            print("\n⚠️ Server failed to start")

        # Phase 4: Quality
        self.phase_quality()

        # Generate Report
        report = self.generate_report()

        elapsed_time = time.time() - start_time

        print("\n" + "=" * 60)
        print(f"Total Time: {elapsed_time:.1f} seconds")
        print("=" * 60)

        # 判斷整體成功
        success = (
            self.results["build"]["success"] and
            len(report["summary"]["critical_failures"]) == 0
        )

        if success:
            print("\n🎉 All tests passed! Project ready for preview.")
            print(f"\n🌐 Preview: http://localhost:5173")
        else:
            print("\n❌ Some critical tests failed. Check report for details.")

        return success

def main():
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."

    orchestrator = AutoTestAndFix(project_path)
    success = orchestrator.run()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
