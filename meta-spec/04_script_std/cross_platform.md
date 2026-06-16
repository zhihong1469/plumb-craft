# Linux/Windows 跨平台适配细则

> 保证技能在 Linux 和 Windows 平台都能正常运行

---

## 核心原则

### 1. 路径处理统一化

```python
# ✅ 正确：使用 pathlib 和统一路径处理
from pathlib import Path
from common.src.path_utils import normalize_path

config_path = normalize_path("config/build.conf")
config_file = Path(config_path)

# ❌ 错误：硬编码路径分隔符
config_path = "config\\build.conf"  # Windows only
config_path = "config/build.conf"   # Linux only
```

### 2. 命令执行抽象化

```python
# ✅ 正确：使用跨平台命令封装
from common.src.cmd_utils import run_command

result = run_command("make -j4", cwd="build")

# ❌ 错误：直接使用 os.system
import os
os.system("make -j4")  # 平台差异大
```

### 3. 环境变量统一化

```python
# ✅ 正确：使用统一环境变量处理
from common.src.platform_detect import get_env_var

gcc_path = get_env_var("GCC_PATH", default="gcc")

# ❌ 错误：直接访问环境变量
import os
gcc_path = os.environ.get("GCC_PATH", "gcc")  # 平台差异
```

---

## 路径处理规范

### 路径分隔符

| 操作 | Windows | Linux | 统一处理 |
|------|---------|-------|---------|
| 路径拼接 | `\` | `/` | `Path() / "subdir"` |
| 路径分割 | `;` | `:` | `os.pathsep` |
| 当前目录 | `.` | `.` | `Path.cwd()` |
| 用户目录 | `C:\Users\xxx` | `/home/xxx` | `Path.home()` |

### 路径处理示例

```python
from pathlib import Path
from common.src.path_utils import normalize_path

# 路径拼接
base_path = Path("project")
sub_path = base_path / "src" / "main.c"

# 路径规范化
normalized = normalize_path("src/../config/file.conf")

# 路径存在性检查
if sub_path.exists():
    content = sub_path.read_text()

# 路径创建
output_dir = Path("build/output")
output_dir.mkdir(parents=True, exist_ok=True)
```

---

## 命令执行规范

### 命令差异处理

| 操作 | Windows | Linux | 统一处理 |
|------|---------|-------|---------|
| 列出文件 | `dir` | `ls` | `Path.iterdir()` |
| 删除文件 | `del` | `rm` | `Path.unlink()` |
| 复制文件 | `copy` | `cp` | `shutil.copy()` |
| 移动文件 | `move` | `mv` | `shutil.move()` |
| 创建目录 | `mkdir` | `mkdir -p` | `Path.mkdir()` |

### 命令执行封装

```python
from common.src.cmd_utils import run_command, CommandResult

def execute_build():
    """执行构建"""
    result = run_command(
        command="make -j4",
        cwd="build",
        timeout=300,
        env={"CC": "gcc"}
    )

    if result.returncode == 0:
        return {
            "status": "success",
            "summary": "构建成功",
            "evidence": [
                {
                    "type": "file",
                    "path": "build/output/app.elf",
                    "description": "可执行文件"
                }
            ]
        }
    else:
        return {
            "status": "failure",
            "summary": f"构建失败: {result.stderr}",
            "failure_category": "compilation_error"
        }
```

---

## 工具检测规范

### 工具检测优先级

```python
from common.src.platform_detect import find_tool

def detect_gcc():
    """检测 GCC 编译器"""
    # 1. 用户自定义路径
    gcc_path = find_tool("gcc", env_var="GCC_PATH")
    if gcc_path:
        return gcc_path

    # 2. 当前工程 .tools/ 目录
    gcc_path = find_tool("gcc", search_paths=[".tools/bin"])
    if gcc_path:
        return gcc_path

    # 3. 系统 PATH
    gcc_path = find_tool("gcc")
    if gcc_path:
        return gcc_path

    # 4. 默认路径回退
    return None
```

### 工具名称映射

| 功能 | Windows | Linux | 统一名称 |
|------|---------|-------|---------|
| C编译器 | gcc.exe | gcc | gcc |
| Python | python.exe | python3 | python |
| Make | make.exe | make | make |
| CMake | cmake.exe | cmake | cmake |

---

## 环境变量规范

### 环境变量命名

| 变量名 | 用途 | 示例 |
|--------|------|------|
| GCC_PATH | GCC 路径 | `C:\gcc\bin\gcc.exe` |
| MAKE_PATH | Make 路径 | `/usr/bin/make` |
| BUILD_DIR | 构建目录 | `build` |
| OUTPUT_DIR | 输出目录 | `build/output` |

### 环境变量处理

```python
from common.src.platform_detect import get_env_var, set_env_var

# 获取环境变量
gcc_path = get_env_var("GCC_PATH", default="gcc")
build_dir = get_env_var("BUILD_DIR", default="build")

# 设置环境变量
set_env_var("BUILD_DIR", "build")

# 列出相关环境变量
env_vars = get_env_var(prefix="BUILD_")
```

---

## 权限处理规范

### 文件权限

```python
from pathlib import Path
import stat

def set_executable(file_path: str):
    """设置文件可执行权限"""
    file = Path(file_path)

    if file.exists():
        # 设置可执行权限
        current_mode = file.stat().st_mode
        file.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
```

### 目录权限

```python
def create_directory_with_perms(dir_path: str):
    """创建目录并设置权限"""
    dir = Path(dir_path)
    dir.mkdir(parents=True, exist_ok=True)

    # 设置目录权限（755）
    dir.chmod(0o755)
```

---

## 平台检测规范

### 平台信息获取

```python
from common.src.platform_detect import get_platform_info

def get_system_info():
    """获取系统信息"""
    info = get_platform_info()

    return {
        "system": info["system"],        # windows/linux/macos
        "arch": info["arch"],            # x86_64/arm64
        "python_version": info["python_version"],
        "is_wsl": info.get("is_wsl", False)
    }
```

### 平台特定逻辑

```python
from common.src.platform_detect import is_windows, is_linux

def get_serial_ports():
    """获取串口列表"""
    if is_windows():
        return get_windows_serial_ports()
    elif is_linux():
        return get_linux_serial_ports()
    else:
        return []
```

---

## 违反示例

❌ 硬编码路径分隔符
❌ 直接使用平台特定命令
❌ 不处理环境变量差异
❌ 不检查平台类型
❌ 不处理权限问题

---

## 正确示例

✅ 使用 pathlib 处理路径
✅ 使用统一命令封装
✅ 处理环境变量差异
✅ 检查平台类型
✅ 正确处理权限

---

## 总结

| 规范 | 要求 |
|------|------|
| **路径处理** | 使用 pathlib 和统一路径处理 |
| **命令执行** | 使用跨平台命令封装 |
| **工具检测** | 五级优先级检测 |
| **环境变量** | 统一环境变量处理 |
| **权限处理** | 正确设置文件/目录权限 |
| **平台检测** | 检测平台类型，执行平台特定逻辑 |