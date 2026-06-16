# Python 脚本开发规范

> 所有技能脚本必须遵循的编码标准

---

## 编码风格

### PEP 8 规范

```python
# ✅ 正确：使用4空格缩进
def build_project():
    result = execute_command("make")
    return result

# ❌ 错误：使用Tab缩进
def build_project():
	result = execute_command("make")
	return result
```

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量 | 小写+下划线 | `build_result` |
| 函数 | 小写+下划线 | `execute_build()` |
| 类 | 大驼峰 | `BuildExecutor` |
| 常量 | 大写+下划线 | `MAX_RETRIES` |
| 私有成员 | 前缀下划线 | `_internal_var` |

### 类型注解

```python
from typing import Dict, List, Optional

def execute_command(
    command: str,
    cwd: Optional[str] = None,
    timeout: int = 60
) -> Dict[str, any]:
    """执行命令并返回结构化结果"""
    pass
```

---

## 函数结构规范

### 标准函数模板

```python
def function_name(param1: str, param2: int) -> Dict[str, any]:
    """
    函数简短描述

    详细描述（可选）

    Args:
        param1: 参数1描述
        param2: 参数2描述

    Returns:
        返回值描述

    Raises:
        ValueError: 参数无效时
        RuntimeError: 运行时错误
    """
    # 1. 参数校验
    if not param1:
        raise ValueError("param1 不能为空")

    # 2. 执行逻辑
    try:
        result = do_something(param1, param2)
    except Exception as e:
        raise RuntimeError(f"执行失败: {e}")

    # 3. 返回结果
    return {
        "status": "success",
        "result": result
    }
```

---

## 错误处理规范

### 统一错误处理

```python
from common.src.error_code import ErrorCode
from common.src.log_utils import log_error

def execute_build():
    """执行构建"""
    try:
        result = run_command("make")
        return result
    except FileNotFoundError as e:
        log_error(f"工具未找到: {e}")
        return {
            "status": "failure",
            "failure_category": "tool_missing",
            "summary": str(e)
        }
    except PermissionError as e:
        log_error(f"权限不足: {e}")
        return {
            "status": "failure",
            "failure_category": "permission_denied",
            "summary": str(e)
        }
    except Exception as e:
        log_error(f"未知错误: {e}")
        return {
            "status": "failure",
            "failure_category": "runtime_error",
            "summary": str(e)
        }
```

---

## 日志记录规范

### 日志级别

| 级别 | 用途 | 示例 |
|------|------|------|
| DEBUG | 调试信息 | `log_debug("开始执行构建")` |
| INFO | 一般信息 | `log_info("构建成功")` |
| WARNING | 警告信息 | `log_warning("构建时间过长")` |
| ERROR | 错误信息 | `log_error("构建失败")` |

### 日志格式

```python
from common.src.log_utils import log_info, log_error, log_warning

def build_project():
    log_info("开始构建项目")
    try:
        result = execute_build()
        log_info(f"构建成功: {result}")
        return result
    except Exception as e:
        log_error(f"构建失败: {e}")
        raise
```

---

## 文件操作规范

### 路径处理

```python
from pathlib import Path
from common.src.path_utils import normalize_path

# ✅ 正确：使用 pathlib 和统一路径处理
config_path = normalize_path("config/build.conf")
config_file = Path(config_path)

if config_file.exists():
    content = config_file.read_text()

# ❌ 错误：硬编码路径分隔符
config_path = "config\\build.conf"  # Windows only
```

### 文件读写

```python
from pathlib import Path

def read_config(config_path: str) -> Dict[str, any]:
    """读取配置文件"""
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    content = config_file.read_text(encoding='utf-8')
    return parse_config(content)

def write_output(output_path: str, content: str):
    """写入输出文件"""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding='utf-8')
```

---

## 命令执行规范

### 跨平台命令封装

```python
from common.src.cmd_utils import run_command

def execute_build():
    """执行构建"""
    # 自动适配 Windows/Linux 命令差异
    result = run_command("make -j4", cwd="build", timeout=300)
    return result.to_structured_output()
```

### 命令参数处理

```python
def execute_command_with_args(command: str, args: List[str]) -> Dict[str, any]:
    """执行带参数的命令"""
    # 参数安全处理
    safe_args = [arg for arg in args if arg]
    full_command = f"{command} {' '.join(safe_args)}"

    result = run_command(full_command)
    return result.to_structured_output()
```

---

## 配置文件规范

### 配置文件格式

```json
{
  "version": "1.0.0",
  "toolchain": {
    "compiler": "gcc",
    "archiver": "ar"
  },
  "build": {
    "parallel_jobs": 4,
    "optimization_level": "O2"
  },
  "output": {
    "directory": "build/output",
    "format": "elf"
  }
}
```

### 配置解析

```python
from common.src.config_parser import parse_config

def load_config(config_path: str) -> Dict[str, any]:
    """加载配置文件"""
    try:
        config = parse_config(config_path)
        validate_config(config)
        return config
    except Exception as e:
        log_error(f"配置加载失败: {e}")
        raise
```

---

## 测试规范

### 单元测试

```python
import unittest
from unittest.mock import patch, MagicMock

class TestBuildExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = BuildExecutor()

    @patch('common.src.cmd_utils.run_command')
    def test_execute_build_success(self, mock_run):
        """测试成功构建"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Build successful"
        )

        result = self.executor.execute_build()
        self.assertEqual(result["status"], "success")

    @patch('common.src.cmd_utils.run_command')
    def test_execute_build_failure(self, mock_run):
        """测试构建失败"""
        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="Build failed"
        )

        result = self.executor.execute_build()
        self.assertEqual(result["status"], "failure")
```

---

## 违反示例

❌ 不使用类型注解
❌ 硬编码路径分隔符
❌ 不处理异常
❌ 不记录日志
❌ 直接使用 `os.system()`

---

## 正确示例

✅ 完整的类型注解
✅ 使用统一路径处理
✅ 完善的错误处理
✅ 规范的日志记录
✅ 使用封装的命令执行

---

## 总结

| 规范 | 要求 |
|------|------|
| **编码风格** | 遵循 PEP 8 |
| **命名规范** | 统一命名约定 |
| **类型注解** | 必须添加类型注解 |
| **函数结构** | 标准化函数模板 |
| **错误处理** | 统一错误处理机制 |
| **日志记录** | 规范的日志级别和格式 |
| **文件操作** | 使用 pathlib 和统一路径处理 |
| **命令执行** | 使用跨平台命令封装 |
| **配置文件** | 标准化配置格式 |
| **测试** | 完整的单元测试 |