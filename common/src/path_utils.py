"""
统一路径处理模块

处理跨平台路径问题
"""

import os
import sys
import platform as sys_platform
from pathlib import Path
from typing import Union, List

# 添加 inc 目录到路径
_CURRENT_DIR = Path(__file__).resolve().parent
_INC_DIR = _CURRENT_DIR.parent / "inc"
sys.path.insert(0, str(_INC_DIR))

from platform_def import Platform, PATH_SEPARATOR


def _get_current_platform() -> Platform:
    """获取当前平台"""
    system = sys_platform.system().lower()
    if system == "linux":
        return Platform.LINUX
    elif system == "windows":
        return Platform.WINDOWS
    elif system == "darwin":
        return Platform.MACOS
    return Platform.UNKNOWN


def normalize_path(path: Union[str, Path]) -> str:
    """
    规范化路径

    Args:
        path: 输入路径

    Returns:
        规范化后的路径字符串
    """
    if isinstance(path, str):
        path = Path(path)

    # 转换为绝对路径
    path = path.resolve()

    # 统一路径分隔符
    current_platform = _get_current_platform()
    separator = PATH_SEPARATOR.get(current_platform, "/")

    return str(path).replace("\\", separator).replace("/", separator)


def join_paths(*paths: Union[str, Path]) -> str:
    """
    拼接路径

    Args:
        *paths: 路径片段

    Returns:
        拼接后的路径
    """
    result = Path(paths[0])
    for path in paths[1:]:
        result = result / path

    return normalize_path(result)


def get_relative_path(path: Union[str, Path], base: Union[str, Path]) -> str:
    """
    获取相对路径

    Args:
        path: 目标路径
        base: 基准路径

    Returns:
        相对路径
    """
    path = normalize_path(path)
    base = normalize_path(base)

    try:
        relative = Path(path).relative_to(Path(base))
        return str(relative)
    except ValueError:
        # 无法计算相对路径，返回绝对路径
        return path


def ensure_directory(path: Union[str, Path]) -> str:
    """
    确保目录存在

    Args:
        path: 目录路径

    Returns:
        目录路径
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return normalize_path(path)


def get_file_extension(path: Union[str, Path]) -> str:
    """
    获取文件扩展名

    Args:
        path: 文件路径

    Returns:
        文件扩展名（包含点）
    """
    return Path(path).suffix


def get_file_name(path: Union[str, Path], with_extension: bool = True) -> str:
    """
    获取文件名

    Args:
        path: 文件路径
        with_extension: 是否包含扩展名

    Returns:
        文件名
    """
    path = Path(path)
    if with_extension:
        return path.name
    else:
        return path.stem


def get_parent_directory(path: Union[str, Path]) -> str:
    """
    获取父目录

    Args:
        path: 路径

    Returns:
        父目录路径
    """
    return normalize_path(Path(path).parent)


def is_absolute_path(path: Union[str, Path]) -> bool:
    """
    判断是否绝对路径

    Args:
        path: 路径

    Returns:
        是否绝对路径
    """
    return Path(path).is_absolute()


def is_sub_path(path: Union[str, Path], base: Union[str, Path]) -> bool:
    """
    判断是否为子路径

    Args:
        path: 路径
        base: 基准路径

    Returns:
        是否为子路径
    """
    try:
        Path(path).relative_to(Path(base))
        return True
    except ValueError:
        return False


def list_files(
    directory: Union[str, Path],
    pattern: str = "*",
    recursive: bool = False
) -> List[str]:
    """
    列出目录中的文件

    Args:
        directory: 目录路径
        pattern: 文件匹配模式
        recursive: 是否递归

    Returns:
        文件路径列表
    """
    directory = Path(directory)

    if recursive:
        files = directory.rglob(pattern)
    else:
        files = directory.glob(pattern)

    return [normalize_path(f) for f in files if f.is_file()]


def list_directories(
    directory: Union[str, Path],
    pattern: str = "*",
    recursive: bool = False
) -> List[str]:
    """
    列出目录中的子目录

    Args:
        directory: 目录路径
        pattern: 目录匹配模式
        recursive: 是否递归

    Returns:
        目录路径列表
    """
    directory = Path(directory)

    if recursive:
        dirs = directory.rglob(pattern)
    else:
        dirs = directory.glob(pattern)

    return [normalize_path(d) for d in dirs if d.is_dir()]


def get_file_size(path: Union[str, Path]) -> int:
    """
    获取文件大小

    Args:
        path: 文件路径

    Returns:
        文件大小（字节）
    """
    return Path(path).stat().st_size


def get_directory_size(directory: Union[str, Path]) -> int:
    """
    获取目录大小

    Args:
        directory: 目录路径

    Returns:
        目录大小（字节）
    """
    total_size = 0
    directory = Path(directory)

    for file_path in directory.rglob("*"):
        if file_path.is_file():
            total_size += file_path.stat().st_size

    return total_size


def split_path(path: Union[str, Path]) -> List[str]:
    """
    分割路径为多个部分

    Args:
        path: 路径

    Returns:
        路径部分列表
    """
    return list(Path(path).parts)


def get_common_path(paths: List[Union[str, Path]]) -> str:
    """
    获取多个路径的公共路径

    Args:
        paths: 路径列表

    Returns:
        公共路径
    """
    if not paths:
        return ""

    path_objects = [Path(p) for p in paths]
    common = Path(os.path.commonpath([str(p) for p in path_objects]))

    return normalize_path(common)


def expand_user_path(path: Union[str, Path]) -> str:
    """
    展开用户路径（~）

    Args:
        path: 路径

    Returns:
        展开后的路径
    """
    return normalize_path(Path(path).expanduser())


def expand_env_vars(path: Union[str, Path]) -> str:
    """
    展开环境变量

    Args:
        path: 路径

    Returns:
        展开后的路径
    """
    if isinstance(path, Path):
        path = str(path)

    expanded = os.path.expandvars(path)
    return normalize_path(expanded)