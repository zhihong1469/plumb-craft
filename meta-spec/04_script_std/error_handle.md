# 统一错误码、异常处理范式

> 所有技能必须遵循的错误处理标准

---

## 错误码定义

### 错误码格式

错误码采用分层结构：`类别_子类_具体错误`

```
格式: CATEGORY_SUBCATEGORY_SPECIFIC
示例: TOOL_MISSING_GCC_NOT_FOUND
```

### 错误类别

| 类别 | 说明 | 示例 |
|------|------|------|
| TOOL | 工具相关错误 | TOOL_MISSING_GCC |
| PERM | 权限相关错误 | PERM_DENIED_WRITE |
| BUILD | 构建相关错误 | BUILD_COMPILATION_ERROR |
| RUNTIME | 运行时错误 | RUNTIME_SEGFAULT |
| NETWORK | 网络相关错误 | NETWORK_TIMEOUT |
| CONFIG | 配置相关错误 | CONFIG_INVALID_FORMAT |
| VALIDATION | 验证相关错误 | VALIDATION_MISSING_PARAM |

### 常用错误码

```python
# 工具相关
TOOL_MISSING_GCC = "TOOL_MISSING_GCC"
TOOL_MISSING_MAKE = "TOOL_MISSING_MAKE"
TOOL_VERSION_INCOMPATIBLE = "TOOL_VERSION_INCOMPATIBLE"

# 权限相关
PERM_DENIED_READ = "PERM_DENIED_READ"
PERM_DENIED_WRITE = "PERM_DENIED_WRITE"
PERM_DENIED_EXECUTE = "PERM_DENIED_EXECUTE"

# 构建相关
BUILD_COMPILATION_ERROR = "BUILD_COMPILATION_ERROR"
BUILD_LINK_ERROR = "BUILD_LINK_ERROR"
BUILD_TIMEOUT = "BUILD_TIMEOUT"

# 运行时相关
RUNTIME_SEGFAULT = "RUNTIME_SEGFAULT"
RUNTIME_TIMEOUT = "RUNTIME_TIMEOUT"
RUNTIME_MEMORY_ERROR = "RUNTIME_MEMORY_ERROR"

# 网络相关
NETWORK_TIMEOUT = "NETWORK_TIMEOUT"
NETWORK_CONNECTION_ERROR = "NETWORK_CONNECTION_ERROR"
NETWORK_DNS_ERROR = "NETWORK_DNS_ERROR"

# 配置相关
CONFIG_INVALID_FORMAT = "CONFIG_INVALID_FORMAT"
CONFIG_MISSING_FIELD = "CONFIG_MISSING_FIELD"
CONFIG_INVALID_VALUE = "CONFIG_INVALID_VALUE"

# 验证相关
VALIDATION_MISSING_PARAM = "VALIDATION_MISSING_PARAM"
VALIDATION_INVALID_PARAM = "VALIDATION_INVALID_PARAM"
VALIDATION_OUT_OF_RANGE = "VALIDATION_OUT_OF_RANGE"
```

---

## 异常处理范式

### 标准异常处理模板

```python
from common.src.error_code import ErrorCode
from common.src.log_utils import log_error, log_warning
from typing import Dict, any

def execute_operation() -> Dict[str, any]:
    """执行操作的标准异常处理模板"""
    try:
        # 1. 参数校验
        result = validate_params()
        if not result["valid"]:
            return {
                "status": "failure",
                "failure_category": "validation_error",
                "summary": result["message"],
                "error_code": result["error_code"]
            }

        # 2. 执行操作
        result = do_operation()

        # 3. 返回成功结果
        return {
            "status": "success",
            "summary": "操作成功",
            "evidence": result["evidence"]
        }

    except FileNotFoundError as e:
        log_error(f"文件未找到: {e}")
        return {
            "status": "failure",
            "failure_category": "file_not_found",
            "summary": str(e),
            "error_code": "FILE_NOT_FOUND"
        }

    except PermissionError as e:
        log_error(f"权限不足: {e}")
        return {
            "status": "failure",
            "failure_category": "permission_denied",
            "summary": str(e),
            "error_code": "PERM_DENIED_OPERATION"
        }

    except TimeoutError as e:
        log_error(f"操作超时: {e}")
        return {
            "status": "failure",
            "failure_category": "timeout",
            "summary": str(e),
            "error_code": "OPERATION_TIMEOUT"
        }

    except Exception as e:
        log_error(f"未知错误: {e}")
        return {
            "status": "failure",
            "failure_category": "runtime_error",
            "summary": str(e),
            "error_code": "RUNTIME_UNKNOWN_ERROR"
        }
```

---

## 错误信息格式

### 标准错误信息结构

```python
{
    "status": "failure",
    "failure_category": "tool_missing",
    "error_code": "TOOL_MISSING_GCC",
    "summary": "GCC 编译器未安装",
    "details": {
        "required_tool": "gcc",
        "expected_version": ">= 9.0",
        "install_command": "apt-get install gcc"  # Linux
    },
    "suggestions": [
        "安装 GCC 编译器",
        "检查环境变量 GCC_PATH",
        "使用系统包管理器安装"
    ],
    "recovery_actions": [
        "自动尝试安装",
        "使用备用工具链",
        "跳过此步骤"
    ]
}
```

### 错误信息字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | ✅ | 错误状态：failure |
| failure_category | string | ✅ | 失败类别 |
| error_code | string | ✅ | 具体错误码 |
| summary | string | ✅ | 错误摘要 |
| details | object | ❌ | 详细信息 |
| suggestions | array | ❌ | 解决建议 |
| recovery_actions | array | ❌ | 恢复操作 |

---

## 错误恢复机制

### 自动恢复策略

```python
def execute_with_recovery(operation: str):
    """执行带自动恢复的操作"""
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            result = execute_operation(operation)
            if result["status"] == "success":
                return result

            # 检查是否可恢复
            if is_recoverable(result["error_code"]):
                log_warning(f"操作失败，尝试恢复: {result['error_code']}")
                recovery_result = attempt_recovery(result)
                if recovery_result["success"]:
                    continue

            retry_count += 1

        except Exception as e:
            log_error(f"操作异常: {e}")
            retry_count += 1

    return {
        "status": "failure",
        "summary": f"操作失败，已重试 {max_retries} 次",
        "error_code": "OPERATION_MAX_RETRIES"
    }
```

### 可恢复错误判断

```python
RECOVERABLE_ERRORS = [
    "NETWORK_TIMEOUT",
    "OPERATION_TIMEOUT",
    "FILE_LOCKED",
    "RESOURCE_BUSY"
]

def is_recoverable(error_code: str) -> bool:
    """判断错误是否可恢复"""
    return error_code in RECOVERABLE_ERRORS
```

---

## 错误日志规范

### 日志级别选择

| 错误级别 | 日志级别 | 说明 |
|---------|---------|------|
| 工具缺失 | ERROR | 阻止操作继续 |
| 权限不足 | ERROR | 需要用户干预 |
| 配置错误 | WARNING | 可能继续执行 |
| 网络超时 | WARNING | 可重试 |
| 运行时错误 | ERROR | 需要调试 |

### 日志格式

```python
from common.src.log_utils import log_error, log_warning

def log_error_with_context(error_code: str, context: Dict[str, any]):
    """记录带上下文的错误日志"""
    log_error(
        f"错误码: {error_code}, "
        f"上下文: {context}, "
        f"堆栈: {traceback.format_exc()}"
    )
```

---

## 违反示例

❌ 不捕获异常
❌ 捕获所有异常但不处理
❌ 不记录错误日志
❌ 错误信息不明确
❌ 不提供恢复建议

---

## 正确示例

✅ 完整的异常处理
✅ 详细的错误信息
✅ 规范的日志记录
✅ 提供恢复建议
✅ 错误码标准化

---

## 总结

| 规范 | 要求 |
|------|------|
| **错误码格式** | 类别_子类_具体错误 |
| **异常处理** | 标准异常处理模板 |
| **错误信息** | 结构化错误信息 |
| **恢复机制** | 自动恢复策略 |
| **日志记录** | 规范的日志级别和格式 |