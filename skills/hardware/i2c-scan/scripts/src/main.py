#!/usr/bin/env python3
"""
HW002 - I2C 扫描技能
"""

import sys
import os
from pathlib import Path
import json
import subprocess

# 添加公共库路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "common" / "src"))

from common.src.error_code import ErrorCode
from common.src.cmd_utils import run_command
from common.inc.data_struct import SkillResult, Evidence


class I2cScanExecutor:
    """I2C 扫描执行器"""
    
    def __init__(self):
        self.i2c_dev_base = "/dev/i2c-"
    
    def detect_tool(self):
        """检测 i2cdetect 工具是否存在"""
        try:
            result = subprocess.run(["which", "i2cdetect"], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def execute(self, bus_num: int = 0) -> SkillResult:
        """
        执行 I2C 扫描
        
        Args:
            bus_num: I2C 总线编号
        
        Returns:
            SkillResult: 执行结果
        """
        try:
            # 检测工具
            if not self.detect_tool():
                return SkillResult.failure(
                    summary="未找到 i2cdetect 工具，请安装 i2c-tools",
                    failure_category="dependency_error",
                    error_code=ErrorCode.DEPENDENCY_NOT_FOUND.value
                )
            
            # 检查总线设备
            bus_path = f"{self.i2c_dev_base}{bus_num}"
            if not os.path.exists(bus_path):
                return SkillResult.failure(
                    summary=f"I2C 总线 {bus_num} 不存在",
                    failure_category="runtime_error",
                    error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
                )
            
            # 执行扫描
            cmd = ["i2cdetect", "-y", str(bus_num)]
            result = run_command(cmd)
            
            if result["returncode"] != 0:
                return SkillResult.failure(
                    summary=f"I2C 扫描失败: {result['stderr']}",
                    failure_category="runtime_error",
                    error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
                )
            
            # 解析结果
            devices = []
            lines = result["stdout"].strip().split("\n")[1:]  # 跳过首行
            for line in lines:
                parts = line.split()
                if len(parts) > 1:
                    addr = parts[0]
                    for i, val in enumerate(parts[1:]):
                        if val != "--":
                            devices.append({
                                "address": f"0x{addr}{chr(ord('a') + i)}",
                                "description": self._get_device_desc(f"0x{addr}{chr(ord('a') + i)}")
                            })
            
            evidence = [
                Evidence(
                    type="output",
                    content=f"总线 {bus_num} 上发现 {len(devices)} 个设备: {', '.join([d['address'] for d in devices])}",
                    title="扫描结果"
                )
            ]
            
            return SkillResult.success(
                summary="I2C 扫描完成",
                evidence=evidence,
                extra={"devices": devices}
            )
        
        except Exception as e:
            return SkillResult.failure(
                summary=f"I2C 扫描失败: {str(e)}",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )
    
    def _get_device_desc(self, addr: str) -> str:
        """获取设备描述（简化版）"""
        known_devices = {
            "0x50": "EEPROM",
            "0x51": "EEPROM",
            "0x68": "RTC",
            "0x48": "ADC",
            "0x4a": "GPIO Expander",
            "0x3c": "OLED Display",
            "0x60": "PMIC"
        }
        return known_devices.get(addr, "Unknown")


def main():
    """主函数"""
    bus_num = 0
    if len(sys.argv) > 1:
        bus_num = int(sys.argv[1])
    
    executor = I2cScanExecutor()
    result = executor.execute(bus_num)
    
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())