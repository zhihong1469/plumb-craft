"""
技能测试执行工具

批量执行技能测试用例
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import json
import unittest
import subprocess

from common.src.path_utils import normalize_path, list_files


class SkillTester:
    """技能测试执行器"""

    def __init__(self, skill_path: str):
        """
        初始化测试执行器

        Args:
            skill_path: 技能路径
        """
        self.skill_path = Path(skill_path)
        self.test_results = []

    def discover_tests(self) -> List[str]:
        """
        发现测试文件

        Returns:
            测试文件列表
        """
        testcases_dir = self.skill_path / "testcases"

        if not testcases_dir.exists():
            return []

        test_files = list_files(testcases_dir, "test_*.py")
        return test_files

    def run_test_file(self, test_file: str) -> Dict[str, any]:
        """
        运行测试文件

        Args:
            test_file: 测试文件路径

        Returns:
            测试结果
        """
        try:
            # 使用 unittest 运行测试
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromName(test_file.replace(".py", ""))

            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)

            return {
                "test_file": test_file,
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "skipped": len(result.skipped),
                "success": result.wasSuccessful()
            }

        except Exception as e:
            return {
                "test_file": test_file,
                "tests_run": 0,
                "failures": 0,
                "errors": 1,
                "skipped": 0,
                "success": False,
                "error": str(e)
            }

    def run_all_tests(self) -> Dict[str, any]:
        """
        运行所有测试

        Returns:
            测试结果汇总
        """
        print(f"测试技能: {self.skill_path}")

        # 发现测试文件
        test_files = self.discover_tests()

        if not test_files:
            print("  ⚠️  没有找到测试文件")
            return {
                "skill_path": str(self.skill_path),
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "test_results": [],
                "overall_status": "no_tests"
            }

        print(f"  发现 {len(test_files)} 个测试文件")

        # 运行测试
        results = []
        total_tests = 0
        passed_tests = 0

        for test_file in test_files:
            print(f"\n  运行测试: {Path(test_file).name}")
            result = self.run_test_file(test_file)
            results.append(result)

            total_tests += result["tests_run"]
            if result["success"]:
                passed_tests += result["tests_run"]

            status = "✅ 通过" if result["success"] else "❌ 失败"
            print(f"  {status}: {result['tests_run']} 个测试")

        # 汇总结果
        print(f"\n测试结果: {passed_tests}/{total_tests} 通过")

        return {
            "skill_path": str(self.skill_path),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "test_results": results,
            "overall_status": "pass" if passed_tests == total_tests else "fail"
        }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="技能测试执行")
    parser.add_argument("skill_path", help="技能路径")
    parser.add_argument("--output", help="输出结果到文件")

    args = parser.parse_args()

    # 检查技能路径
    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"❌ 技能路径不存在: {skill_path}")
        return 1

    # 运行测试
    tester = SkillTester(skill_path)
    result = tester.run_all_tests()

    # 输出结果
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到: {args.output}")

    return 0 if result["overall_status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())