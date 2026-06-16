"""
跨平台命令执行模块

封装命令执行并处理跨平台差异
"""

import subprocess
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

# 添加同目录到路径
_CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_CURRENT_DIR))

from platform_detect import is_windows, is_linux, is_macos


@dataclass
class CommandResult:
    """命令执行结果"""
    success: bool
    stdout: str
    stderr: str
    returncode: int
    command: str
    duration: float = 0.0
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "returncode": self.returncode,
            "command": self.command,
            "duration": self.duration,
            "error_message": self.error_message
        }


def run_command(
    cmd: List[str],
    cwd: Optional[str] = None,
    timeout: Optional[int] = 300,
    env: Optional[Dict[str, str]] = None,
    capture_output: bool = True,
    shell: bool = False
) -> CommandResult:
    """
    执行命令

    Args:
        cmd: 命令参数列表
        cwd: 工作目录
        timeout: 超时时间（秒）
        env: 环境变量
        capture_output: 是否捕获输出
        shell: 是否使用shell执行

    Returns:
        CommandResult: 命令执行结果
    """
    start_time = datetime.now()
    
    try:
        # 设置环境变量
        process_env = os.environ.copy()
        if env:
            process_env.update(env)
        
        # 处理路径问题
        if cwd:
            cwd = str(Path(cwd).resolve())
        
        # 执行命令
        result = subprocess.run(
            cmd,
            cwd=cwd,
            timeout=timeout,
            env=process_env,
            capture_output=capture_output,
            text=True,
            shell=shell
        )
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return CommandResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            command=" ".join(cmd),
            duration=duration
        )
    
    except subprocess.TimeoutExpired:
        duration = (datetime.now() - start_time).total_seconds()
        return CommandResult(
            success=False,
            stdout="",
            stderr="Command timeout",
            returncode=-1,
            command=" ".join(cmd),
            duration=duration,
            error_message="Command timeout"
        )
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        return CommandResult(
            success=False,
            stdout="",
            stderr=str(e),
            returncode=-2,
            command=" ".join(cmd),
            duration=duration,
            error_message=str(e)
        )


def check_tool(tool_name: str, min_version: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    检查工具是否存在

    Args:
        tool_name: 工具名称
        min_version: 最低版本要求

    Returns:
        (是否找到, 版本信息)
    """
    from common.src.platform_detect import detect_tool
    
    result = detect_tool(tool_name, min_version)
    return result.found, result.version


def execute_script(
    script_path: str,
    args: Optional[List[str]] = None,
    cwd: Optional[str] = None,
    timeout: int = 300
) -> CommandResult:
    """
    执行脚本文件

    Args:
        script_path: 脚本路径
        args: 参数列表
        cwd: 工作目录
        timeout: 超时时间

    Returns:
        CommandResult: 执行结果
    """
    script_path = str(Path(script_path).resolve())
    
    if not os.path.exists(script_path):
        return CommandResult(
            success=False,
            stdout="",
            stderr=f"Script not found: {script_path}",
            returncode=-1,
            command=script_path,
            error_message="Script not found"
        )
    
    # 判断脚本类型并构建命令
    if script_path.endswith(".py"):
        cmd = [sys.executable, script_path] + (args or [])
    elif script_path.endswith(".sh"):
        cmd = ["bash", script_path] + (args or [])
    elif script_path.endswith(".bat") or script_path.endswith(".cmd"):
        cmd = ["cmd.exe", "/c", script_path] + (args or [])
    elif is_windows() and not script_path.endswith((".exe", ".com")):
        # Windows 可执行文件（无后缀）
        cmd = [script_path] + (args or [])
    else:
        # 其他可执行文件
        cmd = [script_path] + (args or [])
    
    return run_command(cmd, cwd=cwd, timeout=timeout)


def run_parallel_commands(
    commands: List[List[str]],
    cwd: Optional[str] = None,
    timeout: int = 300
) -> List[CommandResult]:
    """
    并行执行多个命令

    Args:
        commands: 命令列表
        cwd: 工作目录
        timeout: 超时时间

    Returns:
        List[CommandResult]: 命令执行结果列表
    """
    results = []
    for cmd in commands:
        result = run_command(cmd, cwd=cwd, timeout=timeout)
        results.append(result)
    return results


def get_command_output(cmd: List[str], cwd: Optional[str] = None) -> str:
    """
    获取命令输出

    Args:
        cmd: 命令参数列表
        cwd: 工作目录

    Returns:
        命令输出字符串
    """
    result = run_command(cmd, cwd=cwd)
    return result.stdout.strip()


def parse_command_line(command_line: str) -> List[str]:
    """
    解析命令行字符串

    Args:
        command_line: 命令行字符串

    Returns:
        解析后的命令参数列表
    """
    import shlex
    
    if is_windows():
        # Windows 命令行解析
        result = []
        current = ""
        in_quotes = False
        escape = False
        
        for char in command_line:
            if escape:
                current += char
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_quotes = not in_quotes
            elif char == " " and not in_quotes:
                if current:
                    result.append(current)
                    current = ""
            else:
                current += char
        
        if current:
            result.append(current)
        
        return result
    else:
        # Unix/Linux 命令行解析
        return shlex.split(command_line)


def build_command(base_cmd: str, *args: str) -> List[str]:
    """
    构建命令列表

    Args:
        base_cmd: 基础命令
        args: 参数列表

    Returns:
        完整的命令参数列表
    """
    cmd = [base_cmd]
    cmd.extend(args)
    return cmd


def which(program: str) -> Optional[str]:
    """
    查找可执行文件路径

    Args:
        program: 程序名称

    Returns:
        程序路径，未找到返回 None
    """
    import shutil
    return shutil.which(program)


def get_env_path() -> List[str]:
    """
    获取 PATH 环境变量中的路径列表

    Returns:
        路径列表
    """
    path_env = os.environ.get("PATH", "")
    if is_windows():
        return path_env.split(";")
    else:
        return path_env.split(":")


def set_env_path(paths: List[str]):
    """
    设置 PATH 环境变量

    Args:
        paths: 路径列表
    """
    if is_windows():
        os.environ["PATH"] = ";".join(paths)
    else:
        os.environ["PATH"] = ":".join(paths)


def append_to_path(path: str):
    """
    追加路径到 PATH 环境变量

    Args:
        path: 路径
    """
    current_paths = get_env_path()
    if path not in current_paths:
        current_paths.append(path)
        set_env_path(current_paths)


def prepend_to_path(path: str):
    """
    前置路径到 PATH 环境变量

    Args:
        path: 路径
    """
    current_paths = get_env_path()
    if path not in current_paths:
        current_paths.insert(0, path)
        set_env_path(current_paths)