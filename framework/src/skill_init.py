"""
技能初始化脚手架

一键创建标准技能目录结构，支持多分类
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import json

from common.src.path_utils import normalize_path, ensure_directory, join_paths


class SkillInit:
    """技能初始化器"""

    # 技能分类定义
    SKILL_CATEGORIES = {
        "tools": {"name": "基础工具类", "prefix": "T"},
        "dev": {"name": "开发辅助类", "prefix": "D"},
        "test": {"name": "测试验证类", "prefix": "V"},
        "ops": {"name": "运维管理类", "prefix": "O"},
        "security": {"name": "安全防护类", "prefix": "S"},
        "ai": {"name": "AI 适配类", "prefix": "A"},
        "software": {"name": "软件技能类", "prefix": "SW"},
        "hardware": {"name": "硬件技能类", "prefix": "HW"},
        "platform": {"name": "平台技能类", "prefix": "PL"},
        "workflow": {"name": "工作流编排类", "prefix": "WF"},
    }

    def __init__(self, skill_name: str, category: str = "tools", author: str = "Unknown"):
        """
        初始化技能初始化器

        Args:
            skill_name: 技能名称
            category: 技能分类
            author: 作者名称
        """
        self.skill_name = skill_name
        self.category = category.lower()
        self.author = author
        
        # 验证分类
        if self.category not in self.SKILL_CATEGORIES:
            raise ValueError(f"未知分类: {self.category}，支持的分类: {', '.join(self.SKILL_CATEGORIES.keys())}")
        
        # 技能路径 = skills/分类/技能名
        self.skill_dir = Path("skills") / self.category / skill_name
        self.category_info = self.SKILL_CATEGORIES[self.category]

    def create_directory_structure(self):
        """创建目录结构"""
        directories = [
            self.skill_dir,
            self.skill_dir / "scripts" / "inc",
            self.skill_dir / "scripts" / "src",
            self.skill_dir / "references",
            self.skill_dir / "testcases"
        ]

        for directory in directories:
            ensure_directory(directory)

    def create_skill_md(self):
        """创建 SKILL.md 文件"""
        category_name = self.category_info["name"]
        skill_prefix = self.category_info["prefix"]
        
        skill_md_content = f"""# {skill_prefix}xxx - {self.skill_name}

## 技能信息

| 项目 | 内容 |
|------|------|
| 技能ID | {skill_prefix}xxx |
| 技能名称 | {self.skill_name} |
| 分类 | {category_name} |
| 触发关键词 | 关键词1,关键词2 |
| 平台支持 | 跨平台 |
| 状态 | 待设计 |
| 作者 | {self.author} |

## 触发条件

用户输入包含以下关键词时触发：
- "关键词1"
- "关键词2"

## 执行步骤

1. 参数解析
2. 执行操作
3. 返回结果

## 输出格式

```json
{{
    "status": "success",
    "summary": "执行摘要",
    "evidence": [],
    "extra": {{}}
}}
```

## 依赖工具

| 工具名称 | 用途 | 最低版本 | 检测方法 |
|---------|------|---------|---------|
| tool1 | 工具用途 | 1.0+ | tool1 --version |

## 安全注意事项

- 安全说明

## 参考资料

- [文档链接](url)
"""

        skill_md_path = self.skill_dir / "SKILL.md"
        with open(skill_md_path, "w", encoding="utf-8") as f:
            f.write(skill_md_content)

    def create_skill_config(self):
        """创建技能配置文件"""
        config_content = """\"\"\"
技能配置模块

定义技能相关的配置和常量
\"\"\"

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SkillConfig:
    \"\"\"技能配置\"\"\"
    # 添加配置字段
    pass


# 默认配置
DEFAULT_CONFIG = SkillConfig()
"""

        config_path = self.skill_dir / "scripts" / "inc" / "skill_config.py"
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)

    def create_main_script(self):
        """创建主脚本文件"""
        main_script_content = """#!/usr/bin/env python3
\"\"\"
技能主模块

实现技能的主要功能
\"\"\"

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional

# 添加公共库路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "common" / "src"))

from common.src.platform_detect import get_platform_info
from common.src.cmd_utils import run_command
from common.src.path_utils import normalize_path
from common.src.error_code import ErrorCode
from common.inc.data_struct import SkillResult, Evidence

from scripts.inc.skill_config import DEFAULT_CONFIG


class SkillExecutor:
    \"\"\"技能执行器\"\"\"

    def __init__(self, config=None):
        \"\"\"
        初始化技能执行器

        Args:
            config: 技能配置
        \"\"\"
        self.config = config or DEFAULT_CONFIG
        self.platform_info = get_platform_info()

    def execute(self) -> SkillResult:
        \"\"\"
        执行技能

        Returns:
            执行结果
        \"\"\"
        # 实现技能逻辑
        try:
            # 1. 参数校验
            # 2. 执行操作
            # 3. 返回结果

            return SkillResult.success(
                summary="技能执行成功",
                evidence=[]
            )

        except Exception as e:
            return SkillResult.failure(
                summary=f"技能执行失败: {str(e)}",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )


def main():
    \"\"\"主函数\"\"\"
    executor = SkillExecutor()
    result = executor.execute()

    # 输出结果
    import json
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    # 返回退出码
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
"""

        main_script_path = self.skill_dir / "scripts" / "src" / "main.py"
        with open(main_script_path, "w", encoding="utf-8") as f:
            f.write(main_script_content)
        # 设置可执行权限
        os.chmod(main_script_path, 0o755)

    def create_test_template(self):
        """创建测试模板"""
        test_content = """\"\"\"
技能测试用例
\"\"\"

import unittest
import sys
from pathlib import Path

# 添加脚本路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "src"))

from main import SkillExecutor


class TestSkill(unittest.TestCase):
    \"\"\"技能测试\"\"\"

    def setUp(self):
        \"\"\"测试前准备\"\"\"
        self.executor = SkillExecutor()

    def test_execute_success(self):
        \"\"\"测试成功执行\"\"\"
        result = self.executor.execute()
        self.assertEqual(result.status, "success")

    def test_execute_failure(self):
        \"\"\"测试失败执行\"\"\"
        # 模拟失败场景
        pass


if __name__ == "__main__":
    unittest.main()
"""

        test_path = self.skill_dir / "testcases" / "test_skill.py"
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(test_content)

    def create_readme(self):
        """创建 README 文件"""
        category_name = self.category_info["name"]
        readme_content = f"""# {self.skill_name} 技能

## 技能信息

| 项目 | 内容 |
|------|------|
| 名称 | {self.skill_name} |
| 分类 | {category_name} |
| 作者 | {self.author} |
| 许可证 | MIT |

## 技能描述

技能详细描述

## 使用方法

```bash
python skills/{self.category}/{self.skill_name}/scripts/src/main.py
```

## 配置说明

配置项说明

## 依赖工具

- tool1: 工具用途

## 测试

```bash
python -m pytest skills/{self.category}/{self.skill_name}/testcases/
```
"""

        readme_path = self.skill_dir / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

    def create_all(self):
        """创建所有文件"""
        print(f"创建技能: {self.skill_name}")
        print(f"分类: {self.category_info['name']}")

        self.create_directory_structure()
        self.create_skill_md()
        self.create_skill_config()
        self.create_main_script()
        self.create_test_template()
        self.create_readme()

        print(f"✅ 技能创建成功: {self.skill_dir}")
        print(f"📝 请编辑 SKILL.md 文件完善技能描述")
        print(f"🔧 请实现 scripts/src/main.py 中的技能逻辑")
        print(f"🧪 请添加测试用例到 testcases/ 目录")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="创建新技能")
    parser.add_argument("skill_name", help="技能名称")
    parser.add_argument("-c", "--category", default="tools", 
                        help=f"技能分类，可选: {', '.join(SkillInit.SKILL_CATEGORIES.keys())}")
    parser.add_argument("--author", default="Unknown", help="作者名称")

    args = parser.parse_args()

    # 验证技能名称
    skill_name = args.skill_name.lower().replace(" ", "-")
    if not all(c.isalnum() or c == "-" for c in skill_name):
        print("❌ 技能名称只能包含字母、数字和连字符")
        return 1
    
    # 验证分类
    if args.category.lower() not in SkillInit.SKILL_CATEGORIES:
        print(f"❌ 未知分类: {args.category}")
        print(f"   支持的分类: {', '.join(SkillInit.SKILL_CATEGORIES.keys())}")
        return 1

    # 创建技能
    try:
        init = SkillInit(skill_name, args.category, args.author)
        init.create_all()
    except Exception as e:
        print(f"❌ 创建技能失败: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())