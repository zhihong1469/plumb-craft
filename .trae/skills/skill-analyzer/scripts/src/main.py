# 技能分析器主程序

import json
from typing import Dict, List, Any


class SkillAnalyzer:
    """技能分析器：根据用户需求分析技能结构"""
    
    # 关键词映射表
    KEYWORD_MAPPING = {
        "software": ["编译", "构建", "部署", "网络", "服务", "NFS", "配置"],
        "hardware": ["GPIO", "I2C", "SPI", "UART", "外设", "引脚", "硬件"],
        "platform": ["Linux", "RTOS", "FreeRTOS", "系统", "平台", "开发板"],
        "workflow": ["初始化", "自动化", "发布", "工作流", "流程"]
    }
    
    def analyze(self, user_request: str) -> Dict[str, Any]:
        """
        分析用户需求
        
        Args:
            user_request: 用户需求描述
            
        Returns:
            分析结果字典
        """
        # 1. 提取功能
        functions = self._extract_functions(user_request)
        
        # 2. 判断最小单元
        is_minimal_unit = self._is_minimal_unit(functions)
        
        # 3. 确定技能列表
        skills = self._determine_skills(user_request, functions, is_minimal_unit)
        
        return {
            "status": "success",
            "analysis": {
                "original_request": user_request,
                "functions": functions,
                "function_count": len(functions),
                "is_minimal_unit": is_minimal_unit,
                "need_split": not is_minimal_unit
            },
            "skills": skills
        }
    
    def _extract_functions(self, request: str) -> List[str]:
        """提取功能关键词"""
        functions = []
        
        # 简单实现：基于关键词提取
        keywords = request.replace("我想生成一个", "").replace("技能", "").strip()
        
        # 常见拆分场景
        if "NFS" in request or "网络" in request:
            if "NFS" in request:
                functions.append("NFS挂载")
            if "网络" in request:
                functions.append("网络配置")
            if "开发板" in request:
                functions.append("开发板检测")
        else:
            functions.append(keywords)
        
        return functions if functions else [keywords]
    
    def _is_minimal_unit(self, functions: List[str]) -> bool:
        """判断是否为最小单元"""
        # 单个功能 = 最小单元
        # 多个功能 = 需要拆分
        return len(functions) == 1
    
    def _determine_skills(self, request: str, functions: List[str], 
                         is_minimal: bool) -> List[Dict[str, str]]:
        """确定技能列表"""
        skills = []
        
        # 确定分类
        category = self._determine_category(request)
        
        # 生成技能名称
        for i, func in enumerate(functions):
            skill_name = self._generate_skill_name(func)
            
            skills.append({
                "name": skill_name,
                "category": category,
                "function": func,
                "path": f"skills/{category}/{skill_name}/",
                "is_minimal_unit": True
            })
        
        return skills
    
    def _determine_category(self, request: str) -> str:
        """确定技能分类"""
        request_lower = request.lower()
        
        for category, keywords in self.KEYWORD_MAPPING.items():
            for keyword in keywords:
                if keyword.lower() in request_lower:
                    return category
        
        return "software"  # 默认分类
    
    def _generate_skill_name(self, func: str) -> str:
        """生成技能名称"""
        # 移除非字母数字字符，转换为小写
        name = ''.join(c if c.isalnum() else '-' for c in func)
        return name.lower()


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "failure",
            "error_code": "ANA_001",
            "summary": "缺少输入参数"
        }, ensure_ascii=False, indent=2))
        return
    
    user_request = sys.argv[1]
    
    analyzer = SkillAnalyzer()
    result = analyzer.analyze(user_request)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
