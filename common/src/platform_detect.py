"""
跨平台探测模块

检测平台、架构、工具链等信息
"""

import platform
import os
import sys
from pathlib import Path
from typing import Optional, Dict, List
import shutil
import subprocess

# 添加 inc 目录到路径
_CURRENT_DIR = Path(__file__).resolve().parent
_INC_DIR = _CURRENT_DIR.parent / "inc"
sys.path.insert(0, str(_INC_DIR))

from platform_def import Platform, Architecture, TOOL_NAMES, SERIAL_PORT_PATTERNS
from data_struct import PlatformInfo, ToolDetectionResult


def get_platform_info() -> PlatformInfo:
    """获取平台信息"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    # 检测是否 WSL
    is_wsl = False
    if system == "linux":
        try:
            with open("/proc/version", "r") as f:
                version_content = f.read().lower()
                is_wsl = "microsoft" in version_content or "wsl" in version_content
        except Exception:
            pass

    # 检测是否容器
    is_container = False
    if system == "linux":
        is_container = os.path.exists("/.dockerenv") or os.path.exists("/.dockerinit")

    # 映射系统名称
    if system == "linux":
        system_name = Platform.LINUX.value
    elif system == "windows":
        system_name = Platform.WINDOWS.value
    elif system == "darwin":
        system_name = Platform.MACOS.value
    else:
        system_name = Platform.UNKNOWN.value

    # 映射架构名称
    if arch in ["x86_64", "amd64"]:
        arch_name = Architecture.X86_64.value
    elif arch in ["arm64", "aarch64"]:
        arch_name = Architecture.ARM64.value
    elif arch in ["armv7", "armv7l"]:
        arch_name = Architecture.ARMV7.value
    else:
        arch_name = Architecture.UNKNOWN.value

    return PlatformInfo(
        system=system_name,
        arch=arch_name,
        python_version=python_version,
        is_wsl=is_wsl,
        is_container=is_container
    )


def get_current_platform() -> Platform:
    """获取当前平台枚举"""
    info = get_platform_info()
    return Platform(info.system)


def is_windows() -> bool:
    """判断是否 Windows"""
    return get_current_platform() == Platform.WINDOWS


def is_linux() -> bool:
    """判断是否 Linux"""
    return get_current_platform() == Platform.LINUX


def is_macos() -> bool:
    """判断是否 macOS"""
    return get_current_platform() == Platform.MACOS


def find_tool(
    tool_name: str,
    env_var: Optional[str] = None,
    search_paths: Optional[List[str]] = None
) -> Optional[str]:
    """
    查找工具路径

    Args:
        tool_name: 工具名称
        env_var: 环境变量名称
        search_paths: 搜索路径列表

    Returns:
        工具路径，未找到返回 None
    """
    current_platform = get_current_platform()

    # 1. 用户自定义路径（环境变量）
    if env_var:
        custom_path = os.environ.get(env_var)
        if custom_path and Path(custom_path).exists():
            return custom_path

    # 2. 当前工程 .tools/ 目录
    if search_paths:
        for search_path in search_paths:
            tool_path = Path(search_path) / tool_name
            if tool_path.exists():
                return str(tool_path)

    # 3. 系统 PATH 环境变量
    system_path = shutil.which(tool_name)
    if system_path:
        return system_path

    # 4. 通用工具安装目录
    common_paths = get_common_tool_paths(current_platform)
    for common_path in common_paths:
        tool_path = Path(common_path) / tool_name
        if tool_path.exists():
            return str(tool_path)

    # 5. 默认路径回退
    return None


def get_common_tool_paths(platform: Platform) -> List[str]:
    """获取通用工具路径"""
    from platform_def import PLATFORM_PATHS

    paths = []
    platform_paths = PLATFORM_PATHS.get(platform, {})

    for key, path in platform_paths.items():
        if path.startswith("~"):
            path = str(Path(path).expanduser())
        elif "%" in path:  # Windows 环境变量
            path = os.path.expandvars(path)

        if Path(path).exists():
            paths.append(path)

    return paths


def detect_tool(tool_name: str, min_version: Optional[str] = None) -> ToolDetectionResult:
    """
    检测工具

    Args:
        tool_name: 工具名称
        min_version: 最低版本要求

    Returns:
        工具检测结果
    """
    tool_path = find_tool(tool_name)

    if not tool_path:
        return ToolDetectionResult(
            tool_name=tool_name,
            found=False
        )

    # 获取版本信息
    version = get_tool_version(tool_name, tool_path)

    # 检查版本兼容性
    compatible = True
    if min_version and version:
        compatible = check_version_compatibility(version, min_version)

    return ToolDetectionResult(
        tool_name=tool_name,
        found=True,
        path=tool_path,
        version=version,
        compatible=compatible
    )


def get_tool_version(tool_name: str, tool_path: str) -> Optional[str]:
    """获取工具版本"""
    try:
        result = subprocess.run(
            [tool_path, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            # 从输出中提取版本号
            output = result.stdout.strip()
            version = extract_version_from_output(output)
            return version

    except Exception:
        pass

    return None


def extract_version_from_output(output: str) -> Optional[str]:
    """从输出中提取版本号"""
    import re

    # 常见版本号模式
    patterns = [
        r'\d+\.\d+\.\d+',  # 1.2.3
        r'\d+\.\d+',       # 1.2
        r'v\d+\.\d+\.\d+', # v1.2.3
    ]

    for pattern in patterns:
        match = re.search(pattern, output)
        if match:
            return match.group(0)

    return None


def check_version_compatibility(current_version: str, min_version: str) -> bool:
    """检查版本兼容性"""
    try:
        current_parts = [int(x) for x in current_version.split('.')]
        min_parts = [int(x) for x in min_version.split('.')]

        # 补齐版本号位数
        max_len = max(len(current_parts), len(min_parts))
        current_parts.extend([0] * (max_len - len(current_parts)))
        min_parts.extend([0] * (max_len - len(min_parts)))

        return current_parts >= min_parts

    except Exception:
        return False


def get_serial_ports() -> List[str]:
    """获取串口列表"""
    current_platform = get_current_platform()
    patterns = SERIAL_PORT_PATTERNS.get(current_platform, [])

    serial_ports = []
    for pattern in patterns:
        if current_platform == Platform.WINDOWS:
            # Windows 串口需要特殊处理
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            serial_ports.extend([port.device for port in ports])
        else:
            # Linux/macOS 使用 glob 模式
            import glob
            serial_ports.extend(glob.glob(pattern))

    return serial_ports


def get_env_var(var_name: str, default: Optional[str] = None) -> Optional[str]:
    """获取环境变量"""
    return os.environ.get(var_name, default)


def set_env_var(var_name: str, value: str):
    """设置环境变量"""
    os.environ[var_name] = value


def get_env_vars_with_prefix(prefix: str) -> Dict[str, str]:
    """获取指定前缀的环境变量"""
    result = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            result[key] = value
    return result