# 注册表更新器主程序

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class RegistryUpdater:
    """注册表更新器：更新技能注册表"""
    
    REQUIRED_FIELDS = [
        "name", "category", "version", "description",
        "keywords", "platforms", "required_tools"
    ]
    
    VALID_CATEGORIES = ["software", "hardware", "platform", "workflow"]
    
    def __init__(self, registry_path: str):
        """
        初始化注册表更新器
        
        Args:
            registry_path: 注册表文件路径
        """
        self.registry_path = Path(registry_path)
    
    def update(self, skill_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新注册表
        
        Args:
            skill_info: 技能信息字典
            
        Returns:
            更新结果字典
        """
        # 1. 验证数据完整性
        validation = self._validate(skill_info)
        if not validation["valid"]:
            return {
                "status": "failure",
                "failure_category": "validation_error",
                "error_code": "REG_001",
                "summary": "数据验证失败",
                "details": validation
            }
        
        # 2. 读取注册表
        registry = self._read_registry()
        
        # 3. 检查冲突
        conflict = self._check_conflict(registry, skill_info)
        if conflict:
            return {
                "status": "failure",
                "failure_category": "skill_exists",
                "error_code": "REG_002",
                "summary": "技能已存在",
                "existing_skill": conflict
            }
        
        # 4. 添加技能
        registry["skills"].append(self._prepare_skill_record(skill_info))
        
        # 5. 保存注册表
        try:
            self._write_registry(registry)
        except Exception as e:
            return {
                "status": "failure",
                "failure_category": "file_error",
                "error_code": "REG_003",
                "summary": "注册表保存失败",
                "error_details": str(e)
            }
        
        return {
            "status": "success",
            "summary": "注册表更新成功",
            "updated_skill": {
                "name": skill_info["name"],
                "category": skill_info["category"],
                "version": skill_info["version"]
            },
            "registry_location": str(self.registry_path)
        }
    
    def _validate(self, skill_info: Dict[str, Any]) -> Dict[str, Any]:
        """验证数据完整性"""
        missing_fields = []
        
        for field in self.REQUIRED_FIELDS:
            if field not in skill_info or not skill_info[field]:
                missing_fields.append(field)
        
        if missing_fields:
            return {
                "valid": False,
                "missing_fields": missing_fields
            }
        
        # 验证分类
        if skill_info["category"] not in self.VALID_CATEGORIES:
            return {
                "valid": False,
                "error": f"无效的分类: {skill_info['category']}",
                "valid_categories": self.VALID_CATEGORIES
            }
        
        return {"valid": True}
    
    def _read_registry(self) -> Dict[str, Any]:
        """读取注册表"""
        if not self.registry_path.exists():
            return {"skills": []}
        
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {"skills": []}
    
    def _check_conflict(self, registry: Dict[str, Any], 
                        skill_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """检查冲突"""
        for skill in registry.get("skills", []):
            if skill["name"] == skill_info["name"]:
                return skill
        return None
    
    def _prepare_skill_record(self, skill_info: Dict[str, Any]) -> Dict[str, Any]:
        """准备技能记录"""
        record = {
            "name": skill_info["name"],
            "category": skill_info["category"],
            "version": skill_info["version"],
            "description": skill_info["description"],
            "keywords": skill_info["keywords"],
            "platforms": skill_info["platforms"],
            "required_tools": skill_info["required_tools"],
            "agents": skill_info.get("agents", ["openai", "claude", "trae"]),
            "author": skill_info.get("author", "Plumb-Link Team"),
            "license": skill_info.get("license", "MIT"),
            "status": skill_info.get("status", "stable"),
            "generated_at": datetime.now().strftime("%Y-%m-%d")
        }
        
        if "shared_deps" in skill_info:
            record["shared_deps"] = skill_info["shared_deps"]
        
        if "optional_tools" in skill_info:
            record["optional_tools"] = skill_info["optional_tools"]
        
        return record
    
    def _write_registry(self, registry: Dict[str, Any]):
        """写入注册表"""
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            yaml.dump(registry, f, allow_unicode=True, default_flow_style=False)


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "failure",
            "error_code": "REG_001",
            "summary": "缺少输入参数"
        }, ensure_ascii=False, indent=2))
        return
    
    skill_info = json.loads(sys.argv[1])
    
    # 获取注册表路径
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    registry_path = script_dir / "agents" / "skill_registry.yaml"
    
    updater = RegistryUpdater(str(registry_path))
    result = updater.update(skill_info)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
