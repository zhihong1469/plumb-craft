#!/usr/bin/env python3
"""
HW001 - GPIO 配置技能
"""

import sys
import os
from pathlib import Path
import json

# 添加公共库路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "common" / "src"))

from common.src.error_code import ErrorCode
from common.inc.data_struct import SkillResult, Evidence


class GpioConfigExecutor:
    """GPIO 配置执行器"""
    
    def __init__(self):
        self.gpio_base = "/sys/class/gpio"
    
    def execute(self, gpio_num: int, direction: str = "out", value: int = 0) -> SkillResult:
        """
        执行 GPIO 配置
        
        Args:
            gpio_num: GPIO 编号
            direction: 方向 (in/out)
            value: 初始值 (0/1)
        
        Returns:
            SkillResult: 执行结果
        """
        try:
            # 验证参数
            if direction not in ["in", "out"]:
                return SkillResult.failure(
                    summary="方向参数无效，必须为 'in' 或 'out'",
                    failure_category="validation_error",
                    error_code=ErrorCode.VALIDATION_ERROR.value
                )
            
            if value not in [0, 1]:
                return SkillResult.failure(
                    summary="初始值必须为 0 或 1",
                    failure_category="validation_error",
                    error_code=ErrorCode.VALIDATION_ERROR.value
                )
            
            # 检查权限
            if not os.access(self.gpio_base, os.W_OK):
                return SkillResult.failure(
                    summary="权限不足，需要 root 权限操作 GPIO",
                    failure_category="permission_error",
                    error_code=ErrorCode.PERMISSION_ERROR.value
                )
            
            # 导出 GPIO
            export_path = os.path.join(self.gpio_base, "export")
            with open(export_path, "w") as f:
                f.write(str(gpio_num))
            
            # 设置方向
            gpio_path = os.path.join(self.gpio_base, f"gpio{gpio_num}")
            dir_path = os.path.join(gpio_path, "direction")
            with open(dir_path, "w") as f:
                f.write(direction)
            
            # 设置初始值（仅输出模式）
            if direction == "out":
                value_path = os.path.join(gpio_path, "value")
                with open(value_path, "w") as f:
                    f.write(str(value))
            
            evidence = [
                Evidence(
                    type="output",
                    content=f"GPIO {gpio_num} 已配置为 {direction} 模式，初始值: {value}",
                    title="配置结果"
                )
            ]
            
            return SkillResult.success(
                summary="GPIO 配置成功",
                evidence=evidence,
                extra={"gpio_path": gpio_path}
            )
        
        except FileNotFoundError:
            return SkillResult.failure(
                summary=f"GPIO {gpio_num} 不存在或系统不支持",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )
        except PermissionError:
            return SkillResult.failure(
                summary="权限不足，需要 root 权限",
                failure_category="permission_error",
                error_code=ErrorCode.PERMISSION_ERROR.value
            )
        except Exception as e:
            return SkillResult.failure(
                summary=f"GPIO 配置失败: {str(e)}",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )


def main():
    """主函数"""
    # 默认参数
    gpio_num = 50
    direction = "out"
    value = 0
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        gpio_num = int(sys.argv[1])
    if len(sys.argv) > 2:
        direction = sys.argv[2]
    if len(sys.argv) > 3:
        value = int(sys.argv[3])
    
    executor = GpioConfigExecutor()
    result = executor.execute(gpio_num, direction, value)
    
    # 输出结构化结果
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())