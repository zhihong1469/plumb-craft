"""
技能合规检查工具

检查技能是否符合规范
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import json
import re

from common.src.path_utils import normalize_path, list_files, list_directories


class SkillLinter:
    """技能合规检查器"""

    # 技能分类
    VALID_CATEGORIES = {"tools", "dev", "test", "ops", "security", "ai", "software", "hardware", "platform", "workflow"}
    
    # 技能ID前缀映射
    SKILL_PREFIXES = {
        "tools": "T",
        "dev": "D",
        "test": "V",
        "ops": "O",
        "security": "S",
        "ai": "A",
        "software": "SW",
        "hardware": "HW",
        "platform": "PL",
        "workflow": "WF"
    }

    def __init__(self, skill_path: str):
        """
        初始化检查器

        Args:
            skill_path: 技能路径
        """
        self.skill_path = Path(skill_path)
        self.issues = []
        self.warnings = []
        self.skill_name = self.skill_path.name

    def check_directory_structure(self) -> bool:
        """检查目录结构"""
        required_dirs = [
            "scripts/inc",
            "scripts/src",
            "references",
            "testcases"
        ]

        all_valid = True

        for required_dir in required_dirs:
            dir_path = self.skill_path / required_dir
            if not dir_path.exists():
                self.issues.append(f"缺少必需目录: {required_dir}")
                all_valid = False

        return all_valid

    def check_skill_md(self) -> bool:
        """检查 SKILL.md 文件（新格式）"""
        skill_md_path = self.skill_path / "SKILL.md"

        if not skill_md_path.exists():
            self.issues.append("缺少 SKILL.md 文件")
            return False

        # 读取文件内容
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查必需章节
        required_sections = [
            "## 技能信息",
            "## 触发条件",
            "## 执行步骤",
            "## 输出格式",
            "## 依赖工具"
        ]

        for section in required_sections:
            if section not in content:
                self.issues.append(f"SKILL.md 缺少必需章节: {section}")

        # 检查技能信息表格
        if "## 技能信息" in content:
            info_section = content[content.find("## 技能信息"):]
            if "技能ID" not in info_section:
                self.warnings.append("SKILL.md 技能信息中缺少技能ID")
            if "技能名称" not in info_section:
                self.warnings.append("SKILL.md 技能信息中缺少技能名称")
            if "分类" not in info_section:
                self.warnings.append("SKILL.md 技能信息中缺少分类")

        return True

    def check_skill_id_format(self) -> bool:
        """检查技能ID格式"""
        # 从路径推断分类
        category = self.skill_path.parent.name if self.skill_path.parent.name in self.VALID_CATEGORIES else None
        
        if category and category in self.SKILL_PREFIXES:
            expected_prefix = self.SKILL_PREFIXES[category]
            
            # 读取 SKILL.md 中的技能ID
            skill_md_path = self.skill_path / "SKILL.md"
            if skill_md_path.exists():
                with open(skill_md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # 查找技能ID
                match = re.search(r"技能ID\s*\|\s*([^\s|]+)", content)
                if match:
                    skill_id = match.group(1)
                    if not skill_id.startswith(expected_prefix):
                        self.warnings.append(f"技能ID {skill_id} 应以 {expected_prefix} 开头")
                
        return True

    def check_script_structure(self) -> bool:
        """检查脚本结构"""
        script_dir = self.skill_path / "scripts"

        # 检查 inc 目录
        inc_dir = script_dir / "inc"
        if not inc_dir.exists():
            self.issues.append("缺少 scripts/inc 目录")
            return False

        # 检查 src 目录
        src_dir = script_dir / "src"
        if not src_dir.exists():
            self.issues.append("缺少 scripts/src 目录")
            return False

        # 检查 main.py
        main_py = src_dir / "main.py"
        if not main_py.exists():
            self.issues.append("缺少 scripts/src/main.py 文件")
            return False

        # 检查 skill_config.py
        config_py = inc_dir / "skill_config.py"
        if not config_py.exists():
            self.warnings.append("建议创建 scripts/inc/skill_config.py 配置文件")

        return True

    def check_main_script_content(self) -> bool:
        """检查主脚本内容规范"""
        main_py = self.skill_path / "scripts" / "src" / "main.py"
        
        if not main_py.exists():
            return False

        with open(main_py, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查必需的导入
        required_imports = [
            "from common.src.error_code import ErrorCode",
            "from common.inc.data_struct import SkillResult, Evidence",
            "SkillExecutor",
            "def main()"
        ]

        for imp in required_imports:
            if imp not in content:
                self.warnings.append(f"main.py 建议包含: {imp}")

        # 检查输出格式
        if "json.dumps" not in content:
            self.warnings.append("main.py 应使用 json.dumps 输出结构化结果")

        # 检查退出码
        if "sys.exit(main())" not in content:
            self.warnings.append("main.py 应在 if __name__ == '__main__' 中调用 sys.exit(main())")

        return True

    def check_python_style(self) -> bool:
        """检查 Python 代码风格"""
        script_dir = self.skill_path / "scripts" / "src"

        # 查找所有 Python 文件
        python_files = list_files(script_dir, "*.py", recursive=True)

        all_valid = True

        for py_file in python_files:
            # 检查文件编码
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # 检查文件头
                if not content.startswith("#!/usr/bin/env python3"):
                    self.warnings.append(f"{py_file}: 建议添加 shebang (#!/usr/bin/env python3)")

                # 检查是否有类型注解
                if "def " in content and "->" not in content:
                    self.warnings.append(f"{py_file}: 建议添加函数返回类型注解")

                # 检查是否有文档字符串
                if "def " in content and '"""' not in content and "'''" not in content:
                    self.warnings.append(f"{py_file}: 建议添加函数文档字符串")

                # 检查命名规范
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    # 检查函数名
                    func_match = re.match(r"def (\w+)\(", line)
                    if func_match:
                        func_name = func_match.group(1)
                        if not func_name.islower() or "_" not in func_name and len(func_name) > 1:
                            if not func_name.startswith("_"):
                                self.warnings.append(f"{py_file}:{i+1}: 函数名建议使用 snake_case: {func_name}")

                # 检查行长度
                for i, line in enumerate(lines):
                    if len(line) > 120:
                        self.warnings.append(f"{py_file}:{i+1}: 行长度超过 120 字符")

            except Exception as e:
                self.issues.append(f"{py_file}: 文件读取失败: {e}")
                all_valid = False

        return all_valid

    def check_test_coverage(self) -> bool:
        """检查测试覆盖"""
        testcases_dir = self.skill_path / "testcases"

        if not testcases_dir.exists():
            self.warnings.append("缺少 testcases 目录")
            return False

        # 查找测试文件
        test_files = list_files(testcases_dir, "test_*.py")

        if not test_files:
            self.warnings.append("没有找到测试文件")
            return False

        # 检查测试文件内容
        for test_file in test_files:
            with open(test_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "unittest.TestCase" not in content:
                self.warnings.append(f"{test_file}: 建议继承 unittest.TestCase")

        return True

    def check_documentation(self) -> bool:
        """检查文档"""
        readme_path = self.skill_path / "README.md"

        if not readme_path.exists():
            self.warnings.append("建议创建 README.md 文档")
            return False

        return True

    def check_output_format(self) -> bool:
        """检查输出格式规范"""
        main_py = self.skill_path / "scripts" / "src" / "main.py"
        
        if not main_py.exists():
            return True

        with open(main_py, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查是否返回结构化结果
        if "SkillResult.success" not in content and "SkillResult.failure" not in content:
            self.warnings.append("main.py 应使用 SkillResult.success/failure 返回结果")

        # 检查状态字段
        if '"status"' not in content and "status=" not in content:
            self.warnings.append("返回结果应包含 status 字段")

        # 检查 summary 字段
        if '"summary"' not in content and "summary=" not in content:
            self.warnings.append("返回结果应包含 summary 字段")

        # 检查 evidence 字段
        if '"evidence"' not in content and "evidence=" not in content:
            self.warnings.append("返回结果应包含 evidence 字段")

        return True

    def check_security_rules(self) -> bool:
        """检查安全规则"""
        main_py = self.skill_path / "scripts" / "src" / "main.py"
        
        if not main_py.exists():
            return True

        with open(main_py, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查高危操作
        dangerous_patterns = [
            (r"rm\s+-rf", "使用 rm -rf 可能导致数据丢失"),
            (r"format\s+", "格式化操作需要确认"),
            (r"chmod\s+777", "使用 chmod 777 存在安全风险"),
            (r"os\.remove\(", "文件删除操作需要确认"),
            (r"subprocess\.run\([" , "命令执行需要验证输入")
        ]

        for pattern, warning in dangerous_patterns:
            if re.search(pattern, content):
                self.warnings.append(f"main.py: {warning}")

        return True

    def run_all_checks(self) -> Dict[str, any]:
        """
        运行所有检查

        Returns:
            检查结果
        """
        print(f"检查技能: {self.skill_path}")

        # 运行各项检查
        checks = [
            ("目录结构", self.check_directory_structure),
            ("SKILL.md", self.check_skill_md),
            ("技能ID格式", self.check_skill_id_format),
            ("脚本结构", self.check_script_structure),
            ("脚本内容", self.check_main_script_content),
            ("代码风格", self.check_python_style),
            ("输出格式", self.check_output_format),
            ("安全规则", self.check_security_rules),
            ("测试覆盖", self.check_test_coverage),
            ("文档", self.check_documentation)
        ]

        results = {}

        for check_name, check_func in checks:
            try:
                result = check_func()
                results[check_name] = "通过" if result else "失败"
                print(f"  {check_name}: {'✅ 通过' if result else '❌ 失败'}")
            except Exception as e:
                results[check_name] = f"异常: {e}"
                print(f"  {check_name}: ❌ 异常: {e}")

        # 汇总结果
        total_checks = len(checks)
        passed_checks = sum(1 for result in results.values() if result == "通过")

        print(f"\n检查结果: {passed_checks}/{total_checks} 通过")

        if self.issues:
            print(f"\n❌ 发现 {len(self.issues)} 个问题:")
            for issue in self.issues:
                print(f"  - {issue}")

        if self.warnings:
            print(f"\n⚠️  发现 {len(self.warnings)} 个警告:")
            for warning in self.warnings:
                print(f"  - {warning}")

        return {
            "skill_path": str(self.skill_path),
            "skill_name": self.skill_name,
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "results": results,
            "issues": self.issues,
            "warnings": self.warnings,
            "overall_status": "pass" if not self.issues else "fail"
        }


def lint_all_skills(skills_dir: str) -> List[Dict]:
    """检查所有技能"""
    results = []
    skills_path = Path(skills_dir)
    
    if not skills_path.exists():
        print(f"❌ 技能目录不存在: {skills_dir}")
        return results
    
    # 遍历分类目录
    for category_dir in skills_path.iterdir():
        if category_dir.is_dir() and category_dir.name in SkillLinter.VALID_CATEGORIES:
            # 遍历技能目录
            for skill_dir in category_dir.iterdir():
                if skill_dir.is_dir():
                    linter = SkillLinter(str(skill_dir))
                    result = linter.run_all_checks()
                    results.append(result)
                    print()
    
    # 汇总
    total_skills = len(results)
    passed_skills = sum(1 for r in results if r["overall_status"] == "pass")
    total_issues = sum(len(r["issues"]) for r in results)
    total_warnings = sum(len(r["warnings"]) for r in results)
    
    print("=" * 50)
    print(f"汇总结果: {passed_skills}/{total_skills} 技能通过检查")
    print(f"发现问题: {total_issues} 个")
    print(f"发现警告: {total_warnings} 个")
    
    return results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="技能合规检查")
    parser.add_argument("path", help="技能路径或技能目录")
    parser.add_argument("--output", help="输出结果到文件")
    parser.add_argument("--all", action="store_true", help="检查所有技能")

    args = parser.parse_args()

    results = []

    if args.all:
        # 检查所有技能
        results = lint_all_skills(args.path)
    else:
        # 检查单个技能
        skill_path = Path(args.path)
        if not skill_path.exists():
            print(f"❌ 路径不存在: {skill_path}")
            return 1

        if skill_path.is_dir() and skill_path.parent.name in SkillLinter.VALID_CATEGORIES:
            # 单个技能
            linter = SkillLinter(str(skill_path))
            results = [linter.run_all_checks()]
        elif skill_path.is_dir() and skill_path.name == "skills":
            # 技能根目录
            results = lint_all_skills(str(skill_path))
        else:
            print(f"❌ 无效路径: {skill_path}")
            return 1

    # 输出结果
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到: {args.output}")

    # 返回退出码
    if any(r["overall_status"] == "fail" for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())