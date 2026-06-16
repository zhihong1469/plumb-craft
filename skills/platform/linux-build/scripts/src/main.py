#!/usr/bin/env python3
"""
PL001 - Linux 构建技能
"""

import sys
import os
from pathlib import Path
import json

# 添加公共库路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "common" / "src"))

from common.src.error_code import ErrorCode
from common.src.cmd_utils import run_command
from common.src.platform_detect import get_platform_info
from common.inc.data_struct import SkillResult, Evidence


class LinuxBuildExecutor:
    """Linux 构建执行器"""
    
    def __init__(self):
        self.required_tools = ["gcc", "make", "bison", "flex"]
    
    def check_dependencies(self):
        """检查依赖工具"""
        missing = []
        for tool in self.required_tools:
            result = run_command(["which", tool])
            if result["returncode"] != 0:
                missing.append(tool)
        return missing
    
    def execute(self, kernel_dir: str = ".", config_file: str = None, jobs: int = 4) -> SkillResult:
        """
        执行 Linux 构建
        
        Args:
            kernel_dir: 内核源代码目录
            config_file: 配置文件路径
            jobs: 并行编译任务数
        
        Returns:
            SkillResult: 执行结果
        """
        try:
            # 检查依赖
            missing = self.check_dependencies()
            if missing:
                return SkillResult.failure(
                    summary=f"缺少依赖工具: {', '.join(missing)}",
                    failure_category="dependency_error",
                    error_code=ErrorCode.DEPENDENCY_NOT_FOUND.value
                )
            
            # 检查目录
            if not os.path.isdir(kernel_dir):
                return SkillResult.failure(
                    summary=f"内核目录不存在: {kernel_dir}",
                    failure_category="validation_error",
                    error_code=ErrorCode.VALIDATION_ERROR.value
                )
            
            original_dir = os.getcwd()
            os.chdir(kernel_dir)
            
            try:
                # 加载配置
                if config_file and os.path.exists(config_file):
                    run_command(["cp", config_file, ".config"])
                elif os.path.exists(".config"):
                    pass
                else:
                    # 使用默认配置
                    run_command(["make", "defconfig"])
                
                # 执行编译
                cmd = ["make", f"-j{jobs}"]
                result = run_command(cmd, timeout=3600)  # 1小时超时
                
                if result["returncode"] != 0:
                    return SkillResult.failure(
                        summary=f"编译失败: {result['stderr']}",
                        failure_category="runtime_error",
                        error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
                    )
                
                # 查找输出文件
                output_files = []
                zimage_path = os.path.join("arch", "arm", "boot", "zImage")
                if os.path.exists(zimage_path):
                    output_files.append(os.path.abspath(zimage_path))
                
                dtb_pattern = os.path.join("arch", "arm", "boot", "dts", "*.dtb")
                import glob
                for dtb in glob.glob(dtb_pattern):
                    output_files.append(os.path.abspath(dtb))
                
                evidence = []
                for f in output_files[:3]:  # 最多显示3个文件
                    evidence.append(Evidence(
                        type="file",
                        path=f,
                        title=os.path.basename(f)
                    ))
                
                return SkillResult.success(
                    summary="Linux 内核编译完成",
                    evidence=evidence,
                    extra={"output_files": output_files}
                )
            
            finally:
                os.chdir(original_dir)
        
        except Exception as e:
            return SkillResult.failure(
                summary=f"Linux 构建失败: {str(e)}",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )


def main():
    """主函数"""
    kernel_dir = "."
    config_file = None
    jobs = 4
    
    if len(sys.argv) > 1:
        kernel_dir = sys.argv[1]
    if len(sys.argv) > 2:
        config_file = sys.argv[2]
    if len(sys.argv) > 3:
        jobs = int(sys.argv[3])
    
    executor = LinuxBuildExecutor()
    result = executor.execute(kernel_dir, config_file, jobs)
    
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())