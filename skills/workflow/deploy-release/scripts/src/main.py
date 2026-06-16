#!/usr/bin/env python3
"""
WF002 - 部署发布技能
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


class DeployReleaseExecutor:
    """部署发布执行器"""
    
    def __init__(self):
        pass
    
    def execute(self, target_host: str, deploy_path: str = "/opt/app", 
                version: str = "v1.0.0", local_dir: str = ".") -> SkillResult:
        """
        执行部署发布
        
        Args:
            target_host: 目标主机地址
            deploy_path: 部署路径
            version: 版本号
            local_dir: 本地代码目录
        
        Returns:
            SkillResult: 执行结果
        """
        try:
            # 验证参数
            if not target_host:
                return SkillResult.failure(
                    summary="目标主机不能为空",
                    failure_category="validation_error",
                    error_code=ErrorCode.VALIDATION_ERROR.value
                )
            
            # 检查本地目录
            if not os.path.isdir(local_dir):
                return SkillResult.failure(
                    summary=f"本地目录不存在: {local_dir}",
                    failure_category="validation_error",
                    error_code=ErrorCode.VALIDATION_ERROR.value
                )
            
            # 创建远程目录
            cmd = ["ssh", target_host, f"mkdir -p {deploy_path}"]
            result = run_command(cmd)
            if result["returncode"] != 0:
                return SkillResult.failure(
                    summary=f"创建远程目录失败: {result['stderr']}",
                    failure_category="runtime_error",
                    error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
                )
            
            # 传输文件
            cmd = ["scp", "-r", local_dir, f"{target_host}:{deploy_path}"]
            result = run_command(cmd)
            if result["returncode"] != 0:
                return SkillResult.failure(
                    summary=f"文件传输失败: {result['stderr']}",
                    failure_category="runtime_error",
                    error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
                )
            
            # 设置权限
            cmd = ["ssh", target_host, f"chmod -R 755 {deploy_path}"]
            run_command(cmd)
            
            evidence = [
                Evidence(
                    type="output",
                    content=f"应用已部署到 {target_host}:{deploy_path}",
                    title="部署结果"
                )
            ]
            
            return SkillResult.success(
                summary="部署完成",
                evidence=evidence,
                extra={
                    "target_host": target_host,
                    "deployed_version": version
                }
            )
        
        except Exception as e:
            return SkillResult.failure(
                summary=f"部署失败: {str(e)}",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )


def main():
    """主函数"""
    target_host = ""
    deploy_path = "/opt/app"
    version = "v1.0.0"
    local_dir = "."
    
    if len(sys.argv) > 1:
        target_host = sys.argv[1]
    if len(sys.argv) > 2:
        deploy_path = sys.argv[2]
    if len(sys.argv) > 3:
        version = sys.argv[3]
    if len(sys.argv) > 4:
        local_dir = sys.argv[4]
    
    executor = DeployReleaseExecutor()
    result = executor.execute(target_host, deploy_path, version, local_dir)
    
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())