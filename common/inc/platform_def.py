"""
平台定义模块

定义平台枚举、路径常量、系统判断
"""

from enum import Enum
from typing import Dict, List


class Platform(Enum):
    """平台枚举"""
    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "macos"
    UNKNOWN = "unknown"


class Architecture(Enum):
    """架构枚举"""
    X86_64 = "x86_64"
    ARM64 = "arm64"
    ARMV7 = "armv7"
    UNKNOWN = "unknown"


# 平台路径常量
PLATFORM_PATHS: Dict[Platform, Dict[str, str]] = {
    Platform.LINUX: {
        "usr_bin": "/usr/bin",
        "usr_local_bin": "/usr/local/bin",
        "opt_bin": "/opt/bin",
        "home_bin": "~/bin",
        "tools_dir": ".tools/bin",
    },
    Platform.WINDOWS: {
        "program_files": "C:\\Program Files",
        "program_files_x86": "C:\\Program Files (x86)",
        "local_app_data": "%LOCALAPPDATA%",
        "tools_dir": ".tools\\bin",
    },
    Platform.MACOS: {
        "usr_local_bin": "/usr/local/bin",
        "homebrew_bin": "/usr/local/bin",
        "opt_homebrew_bin": "/opt/homebrew/bin",
        "tools_dir": ".tools/bin",
    },
}


# 工具名称映射
TOOL_NAMES: Dict[str, Dict[Platform, str]] = {
    "gcc": {
        Platform.LINUX: "gcc",
        Platform.WINDOWS: "gcc.exe",
        Platform.MACOS: "gcc",
    },
    "python": {
        Platform.LINUX: "python3",
        Platform.WINDOWS: "python.exe",
        Platform.MACOS: "python3",
    },
    "make": {
        Platform.LINUX: "make",
        Platform.WINDOWS: "make.exe",
        Platform.MACOS: "make",
    },
}


# 串口设备名称模式
SERIAL_PORT_PATTERNS: Dict[Platform, List[str]] = {
    Platform.LINUX: [
        "/dev/ttyUSB*",
        "/dev/ttyACM*",
        "/dev/ttyS*",
    ],
    Platform.WINDOWS: [
        "COM*",
    ],
    Platform.MACOS: [
        "/dev/tty.usbserial*",
        "/dev/tty.usbmodem*",
    ],
}


# 环境变量名称
ENV_VAR_NAMES: Dict[str, Dict[Platform, str]] = {
    "gcc_path": {
        Platform.LINUX: "GCC_PATH",
        Platform.WINDOWS: "GCC_PATH",
        Platform.MACOS: "GCC_PATH",
    },
    "python_path": {
        Platform.LINUX: "PYTHON_PATH",
        Platform.WINDOWS: "PYTHON_PATH",
        Platform.MACOS: "PYTHON_PATH",
    },
}


# 文件权限
FILE_PERMISSIONS: Dict[str, int] = {
    "readable": 0o444,
    "writable": 0o644,
    "executable": 0o755,
    "private": 0o600,
}


# 路径分隔符
PATH_SEPARATOR: Dict[Platform, str] = {
    Platform.LINUX: "/",
    Platform.WINDOWS: "\\",
    Platform.MACOS: "/",
}


# 环境变量路径分隔符
ENV_PATH_SEPARATOR: Dict[Platform, str] = {
    Platform.LINUX: ":",
    Platform.WINDOWS: ";",
    Platform.MACOS: ":",
}