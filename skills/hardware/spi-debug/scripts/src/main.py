#!/usr/bin/env python3
"""
HW003 - SPI 调试技能
"""

import sys
import os
from pathlib import Path
import json
import glob

# 添加公共库路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "common" / "src"))

from common.src.error_code import ErrorCode
from common.inc.data_struct import SkillResult, Evidence


class SpiDebugExecutor:
    """SPI 调试执行器"""
    
    def __init__(self):
        self.spi_dev_pattern = "/dev/spidev*"
    
    def list_devices(self):
        """列出所有 SPI 设备"""
        return glob.glob(self.spi_dev_pattern)
    
    def execute(self, bus_num: int = 0, cs_num: int = 0) -> SkillResult:
        """
        执行 SPI 调试
        
        Args:
            bus_num: SPI 总线编号
            cs_num: 片选编号
        
        Returns:
            SkillResult: 执行结果
        """
        try:
            # 获取所有 SPI 设备
            devices = self.list_devices()
            
            if not devices:
                return SkillResult.failure(
                    summary="未发现 SPI 设备",
                    failure_category="runtime_error",
                    error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
                )
            
            # 检查指定设备
            target_device = f"/dev/spidev{bus_num}.{cs_num}"
            
            if target_device not in devices:
                evidence = [
                    Evidence(
                        type="output",
                        content=f"可用 SPI 设备: {', '.join(devices)}",
                        title="设备列表"
                    )
                ]
                return SkillResult.failure(
                    summary=f"SPI 设备 {target_device} 不存在",
                    failure_category="runtime_error",
                    error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value,
                    evidence=evidence
                )
            
            # 检查权限
            if not os.access(target_device, os.R_OK):
                return SkillResult.failure(
                    summary=f"没有权限访问 {target_device}",
                    failure_category="permission_error",
                    error_code=ErrorCode.PERMISSION_ERROR.value
                )
            
            evidence = [
                Evidence(
                    type="output",
                    content=f"SPI 设备 {target_device} 测试通过",
                    title="测试结果"
                ),
                Evidence(
                    type="output",
                    content=f"可用 SPI 设备: {', '.join(devices)}",
                    title="设备列表"
                )
            ]
            
            return SkillResult.success(
                summary="SPI 测试完成",
                evidence=evidence,
                extra={"spi_devices": devices}
            )
        
        except Exception as e:
            return SkillResult.failure(
                summary=f"SPI 调试失败: {str(e)}",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )


def main():
    """主函数"""
    bus_num = 0
    cs_num = 0
    
    if len(sys.argv) > 1:
        bus_num = int(sys.argv[1])
    if len(sys.argv) > 2:
        cs_num = int(sys.argv[2])
    
    executor = SpiDebugExecutor()
    result = executor.execute(bus_num, cs_num)
    
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())