#!/usr/bin/env python3
"""
WF001 - 项目初始化技能
"""

import sys
import os
from pathlib import Path
import json

# 添加公共库路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "common" / "src"))

from common.src.error_code import ErrorCode
from common.src.cmd_utils import run_command
from common.inc.data_struct import SkillResult, Evidence


class ProjectInitExecutor:
    """项目初始化执行器"""
    
    def __init__(self):
        self.templates = {
            "c": ["src/main.c", "include/", "Makefile", "README.md"],
            "cpp": ["src/main.cpp", "include/", "CMakeLists.txt", "README.md"],
            "python": ["src/main.py", "pyproject.toml", "README.md"],
            "embedded": ["src/main.c", "src/hal/", "include/", "Makefile", "README.md"],
        }
    
    def execute(self, project_name: str, template: str = "c", with_git: bool = True) -> SkillResult:
        """
        初始化项目
        
        Args:
            project_name: 项目名称
            template: 模板类型 (c/cpp/python/embedded)
            with_git: 是否初始化 git
        
        Returns:
            SkillResult: 执行结果
        """
        try:
            # 验证模板类型
            if template not in self.templates:
                return SkillResult.failure(
                    summary=f"未知模板类型: {template}，支持的类型: {', '.join(self.templates.keys())}",
                    failure_category="validation_error",
                    error_code=ErrorCode.VALIDATION_ERROR.value
                )
            
            # 检查目录是否存在
            if os.path.exists(project_name):
                return SkillResult.failure(
                    summary=f"目录已存在: {project_name}",
                    failure_category="runtime_error",
                    error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
                )
            
            # 创建目录结构
            files_created = []
            os.makedirs(project_name)
            
            for item in self.templates[template]:
                item_path = os.path.join(project_name, item)
                if item.endswith("/"):
                    # 创建目录
                    os.makedirs(item_path, exist_ok=True)
                else:
                    # 创建文件
                    with open(item_path, "w") as f:
                        f.write(self._get_file_content(item))
                    files_created.append(item)
            
            # 初始化 git
            if with_git:
                original_dir = os.getcwd()
                os.chdir(project_name)
                try:
                    run_command(["git", "init"])
                    run_command(["git", "add", "."])
                    run_command(["git", "commit", "-m", "Initial commit"])
                finally:
                    os.chdir(original_dir)
            
            evidence = [
                Evidence(
                    type="output",
                    content=f"项目 {project_name} 创建成功，包含 {len(files_created)} 个文件",
                    title="初始化结果"
                )
            ]
            
            return SkillResult.success(
                summary="项目初始化完成",
                evidence=evidence,
                extra={
                    "project_path": os.path.abspath(project_name),
                    "files_created": files_created
                }
            )
        
        except Exception as e:
            return SkillResult.failure(
                summary=f"项目初始化失败: {str(e)}",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )
    
    def _get_file_content(self, filename: str) -> str:
        """获取文件内容模板"""
        content_map = {
            "src/main.c": """#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}
""",
            "src/main.cpp": """#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
""",
            "src/main.py": """#!/usr/bin/env python3

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""",
            "Makefile": """CC = gcc
CFLAGS = -Wall -Wextra

TARGET = app
SRCS = src/main.c

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)
""",
            "CMakeLists.txt": """cmake_minimum_required(VERSION 3.10)

project(MyProject)

set(CMAKE_CXX_STANDARD 11)

add_executable(app src/main.cpp)
""",
            "pyproject.toml": """[project]
name = "myproject"
version = "0.1.0"
dependencies = []
""",
            "README.md": """# Project Name

## Description

This is a project template.

## Build

```bash
# Build instructions
```

## Run

```bash
# Run instructions
```
"""
        }
        return content_map.get(filename, "")


def main():
    """主函数"""
    project_name = "my-project"
    template = "c"
    with_git = True
    
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    if len(sys.argv) > 2:
        template = sys.argv[2]
    if len(sys.argv) > 3:
        with_git = sys.argv[3].lower() == "true"
    
    executor = ProjectInitExecutor()
    result = executor.execute(project_name, template, with_git)
    
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())