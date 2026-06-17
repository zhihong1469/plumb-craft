# 技能创建器主程序

import json
import os
from pathlib import Path
from typing import Dict, List, Any


class SkillCreator:
    """技能创建器：根据分析结果创建技能"""
    
    def __init__(self, base_path: str):
        """
        初始化技能创建器
        
        Args:
            base_path: plumb-link 根目录路径
        """
        self.base_path = Path(base_path)
        self.created_files = []
    
    def create(self, skill_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建技能
        
        Args:
            skill_info: 技能信息字典
            
        Returns:
            创建结果字典
        """
        skill_name = skill_info["name"]
        category = skill_info["category"]
        path = skill_info["path"]
        
        # 1. 检查路径冲突
        full_path = self.base_path / path
        if full_path.exists():
            return {
                "status": "failure",
                "failure_category": "path_conflict",
                "error_code": "CRE_001",
                "summary": "技能路径已存在",
                "existing_path": str(full_path)
            }
        
        # 2. 创建目录结构
        try:
            self._create_directories(full_path)
        except Exception as e:
            return {
                "status": "failure",
                "failure_category": "directory_error",
                "error_code": "CRE_002",
                "summary": "目录创建失败",
                "error_details": str(e)
            }
        
        # 3. 生成文件
        try:
            self._generate_skill_md(full_path, skill_info)
            self._generate_main_py(full_path, skill_info)
            self._generate_openai_yaml(full_path, skill_info)
        except Exception as e:
            return {
                "status": "failure",
                "failure_category": "file_error",
                "error_code": "CRE_003",
                "summary": "文件生成失败",
                "error_details": str(e)
            }
        
        return {
            "status": "success",
            "summary": "技能创建成功",
            "skill": {
                "name": skill_name,
                "category": category,
                "path": str(full_path)
            },
            "created_files": self.created_files
        }
    
    def _create_directories(self, path: Path):
        """创建目录结构"""
        dirs = [
            path,
            path / "scripts" / "src",
            path / "agents",
            path / "references",
            path / "testcases"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _generate_skill_md(self, path: Path, info: Dict[str, Any]):
        """生成 SKILL.md"""
        content = f"""---
name: {info['name']}
version: 1.0.0
description: {info.get('description', info.get('function', ''))}
keywords: {json.dumps(info.get('keywords', []), ensure_ascii=False)}
platforms: {json.dumps(info.get('platforms', ['linux']), ensure_ascii=False)}
required_tools: {json.dumps(info.get('required_tools', []), ensure_ascii=False)}
output_format: structured
author: "Plumb-Link Team"
license: "MIT"
---

# {info.get('function', info['name'])}

## 触发条件
- {info.get('function', info['name'])}
- {info['name']}

## 执行步骤
1. 步骤1
2. 步骤2
3. 步骤3

## 输出格式
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | ✅ | success/partial/failure |
| summary | string | ✅ | 执行摘要 |
| evidence | array | ✅ | 输出文件列表 |
| failure_category | string | ❌ | 失败类型 |
| error_code | string | ❌ | 错误码 |

## 安全注意事项
- 注意1
"""
        
        file_path = path / "SKILL.md"
        file_path.write_text(content, encoding='utf-8')
        self.created_files.append(str(file_path))
    
    def _generate_main_py(self, path: Path, info: Dict[str, Any]):
        """生成主脚本"""
        content = f'''"""技能主程序：{info['name']}"""

import json
from pathlib import Path


class {info['name'].replace('-', '_').title().replace('_', '')}:
    """{info.get('function', info['name'])}"""
    
    def execute(self, params: dict = None) -> dict:
        """
        执行技能
        
        Args:
            params: 执行参数
            
        Returns:
            执行结果
        """
        return {{
            "status": "success",
            "summary": "{info.get('function', info['name'])}执行成功"
        }}


def main():
    """主函数"""
    import sys
    
    params = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {{}}
    
    skill = {info['name'].replace('-', '_').title().replace('_', '')}()
    result = skill.execute(params)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
'''
        
        file_path = path / "scripts" / "src" / "main.py"
        file_path.write_text(content, encoding='utf-8')
        self.created_files.append(str(file_path))
    
    def _generate_openai_yaml(self, path: Path, info: Dict[str, Any]):
        """生成 openai.yaml"""
        content = f"""interface:
  display_name: "{info.get('function', info['name'])}"
  short_description: "{info.get('description', info.get('function', ''))}"
  default_prompt: |
    使用 {info['name']} 技能完成任务...

intent_keywords:
  - "{info.get('function', info['name'])}"
  - "{info['name']}"

platforms:
  - linux
  - windows

required_tools: []
"""
        
        file_path = path / "agents" / "openai.yaml"
        file_path.write_text(content, encoding='utf-8')
        self.created_files.append(str(file_path))


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "failure",
            "error_code": "CRE_001",
            "summary": "缺少输入参数"
        }, ensure_ascii=False, indent=2))
        return
    
    skill_info = json.loads(sys.argv[1])
    
    # 获取 plumb-link 根目录
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    creator = SkillCreator(str(script_dir))
    
    result = creator.create(skill_info)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
