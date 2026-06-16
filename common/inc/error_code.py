"""
全局统一错误码定义

所有错误码采用分层结构：类别_子类_具体错误
"""

from enum import Enum
from typing import Dict, List


class ErrorCode(str, Enum):
    """错误码枚举"""

    # ================ 工具相关错误 ================
    TOOL_MISSING_GCC = "TOOL_MISSING_GCC"
    TOOL_MISSING_MAKE = "TOOL_MISSING_MAKE"
    TOOL_MISSING_PYTHON = "TOOL_MISSING_PYTHON"
    TOOL_MISSING_CMAKE = "TOOL_MISSING_CMAKE"
    TOOL_MISSING_NINJA = "TOOL_MISSING_NINJA"
    TOOL_VERSION_INCOMPATIBLE = "TOOL_VERSION_INCOMPATIBLE"
    TOOL_EXECUTION_FAILED = "TOOL_EXECUTION_FAILED"
    TOOL_NOT_FOUND = "TOOL_NOT_FOUND"
    DEPENDENCY_NOT_FOUND = "DEPENDENCY_NOT_FOUND"

    # ================ 权限相关错误 ================
    PERM_DENIED_READ = "PERM_DENIED_READ"
    PERM_DENIED_WRITE = "PERM_DENIED_WRITE"
    PERM_DENIED_EXECUTE = "PERM_DENIED_EXECUTE"
    PERM_DENIED_ACCESS = "PERM_DENIED_ACCESS"
    PERMISSION_ERROR = "PERMISSION_ERROR"

    # ================ 构建相关错误 ================
    BUILD_COMPILATION_ERROR = "BUILD_COMPILATION_ERROR"
    BUILD_LINK_ERROR = "BUILD_LINK_ERROR"
    BUILD_TIMEOUT = "BUILD_TIMEOUT"
    BUILD_DEPENDENCY_MISSING = "BUILD_DEPENDENCY_MISSING"
    BUILD_CONFIG_INVALID = "BUILD_CONFIG_INVALID"
    BUILD_TARGET_NOT_FOUND = "BUILD_TARGET_NOT_FOUND"
    BUILD_OUTPUT_MISSING = "BUILD_OUTPUT_MISSING"

    # ================ 运行时相关错误 ================
    RUNTIME_SEGFAULT = "RUNTIME_SEGFAULT"
    RUNTIME_TIMEOUT = "RUNTIME_TIMEOUT"
    RUNTIME_MEMORY_ERROR = "RUNTIME_MEMORY_ERROR"
    RUNTIME_UNKNOWN_ERROR = "RUNTIME_UNKNOWN_ERROR"
    RUNTIME_NULL_POINTER = "RUNTIME_NULL_POINTER"
    RUNTIME_INDEX_OUT_OF_BOUNDS = "RUNTIME_INDEX_OUT_OF_BOUNDS"

    # ================ 网络相关错误 ================
    NETWORK_TIMEOUT = "NETWORK_TIMEOUT"
    NETWORK_CONNECTION_ERROR = "NETWORK_CONNECTION_ERROR"
    NETWORK_DNS_ERROR = "NETWORK_DNS_ERROR"
    NETWORK_SSL_ERROR = "NETWORK_SSL_ERROR"
    NETWORK_UNREACHABLE = "NETWORK_UNREACHABLE"
    NETWORK_AUTHENTICATION_FAILED = "NETWORK_AUTHENTICATION_FAILED"

    # ================ 配置相关错误 ================
    CONFIG_INVALID_FORMAT = "CONFIG_INVALID_FORMAT"
    CONFIG_MISSING_FIELD = "CONFIG_MISSING_FIELD"
    CONFIG_INVALID_VALUE = "CONFIG_INVALID_VALUE"
    CONFIG_PARSE_ERROR = "CONFIG_PARSE_ERROR"
    CONFIG_FILE_NOT_FOUND = "CONFIG_FILE_NOT_FOUND"
    CONFIG_VERSION_MISMATCH = "CONFIG_VERSION_MISMATCH"

    # ================ 验证相关错误 ================
    VALIDATION_ERROR = "VALIDATION_ERROR"
    VALIDATION_MISSING_PARAM = "VALIDATION_MISSING_PARAM"
    VALIDATION_INVALID_PARAM = "VALIDATION_INVALID_PARAM"
    VALIDATION_OUT_OF_RANGE = "VALIDATION_OUT_OF_RANGE"
    VALIDATION_TYPE_MISMATCH = "VALIDATION_TYPE_MISMATCH"
    VALIDATION_FORMAT_ERROR = "VALIDATION_FORMAT_ERROR"

    # ================ 文件相关错误 ================
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_ALREADY_EXISTS = "FILE_ALREADY_EXISTS"
    FILE_READ_ERROR = "FILE_READ_ERROR"
    FILE_WRITE_ERROR = "FILE_WRITE_ERROR"
    FILE_LOCKED = "FILE_LOCKED"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    FILE_FORMAT_ERROR = "FILE_FORMAT_ERROR"
    FILE_ENCODING_ERROR = "FILE_ENCODING_ERROR"

    # ================ 目录相关错误 ================
    DIR_NOT_FOUND = "DIR_NOT_FOUND"
    DIR_NOT_EMPTY = "DIR_NOT_EMPTY"
    DIR_CREATE_FAILED = "DIR_CREATE_FAILED"
    DIR_ACCESS_DENIED = "DIR_ACCESS_DENIED"
    DIR_TOO_MANY_FILES = "DIR_TOO_MANY_FILES"

    # ================ 硬件相关错误 ================
    HARDWARE_NOT_FOUND = "HARDWARE_NOT_FOUND"
    HARDWARE_ACCESS_DENIED = "HARDWARE_ACCESS_DENIED"
    HARDWARE_TIMEOUT = "HARDWARE_TIMEOUT"
    HARDWARE_COMMUNICATION_ERROR = "HARDWARE_COMMUNICATION_ERROR"
    HARDWARE_INIT_FAILED = "HARDWARE_INIT_FAILED"
    HARDWARE_NOT_SUPPORTED = "HARDWARE_NOT_SUPPORTED"

    # ================ 安全相关错误 ================
    SECURITY_HIGH_RISK_OPERATION = "SECURITY_HIGH_RISK_OPERATION"
    SECURITY_PERMISSION_DENIED = "SECURITY_PERMISSION_DENIED"
    SECURITY_AUTHENTICATION_FAILED = "SECURITY_AUTHENTICATION_FAILED"
    SECURITY_AUTHORIZATION_FAILED = "SECURITY_AUTHORIZATION_FAILED"
    SECURITY_INPUT_VALIDATION_FAILED = "SECURITY_INPUT_VALIDATION_FAILED"
    SECURITY_INJECTION_ATTACK = "SECURITY_INJECTION_ATTACK"

    # ================ 操作相关错误 ================
    OPERATION_CANCELLED = "OPERATION_CANCELLED"
    OPERATION_TIMEOUT = "OPERATION_TIMEOUT"
    OPERATION_MAX_RETRIES = "OPERATION_MAX_RETRIES"
    OPERATION_NOT_SUPPORTED = "OPERATION_NOT_SUPPORTED"
    OPERATION_INVALID_STATE = "OPERATION_INVALID_STATE"
    OPERATION_NOT_IMPLEMENTED = "OPERATION_NOT_IMPLEMENTED"

    # ================ 平台相关错误 ================
    PLATFORM_NOT_SUPPORTED = "PLATFORM_NOT_SUPPORTED"
    PLATFORM_DETECTION_FAILED = "PLATFORM_DETECTION_FAILED"
    PLATFORM_ARCH_MISMATCH = "PLATFORM_ARCH_MISMATCH"
    PLATFORM_VERSION_INCOMPATIBLE = "PLATFORM_VERSION_INCOMPATIBLE"

    # ================ 技能相关错误 ================
    SKILL_NOT_FOUND = "SKILL_NOT_FOUND"
    SKILL_LOAD_FAILED = "SKILL_LOAD_FAILED"
    SKILL_EXECUTE_FAILED = "SKILL_EXECUTE_FAILED"
    SKILL_CONFIG_INVALID = "SKILL_CONFIG_INVALID"
    SKILL_DEPRECATED = "SKILL_DEPRECATED"

    # ================ 数据相关错误 ================
    DATA_PARSE_ERROR = "DATA_PARSE_ERROR"
    DATA_VALIDATION_ERROR = "DATA_VALIDATION_ERROR"
    DATA_FORMAT_ERROR = "DATA_FORMAT_ERROR"
    DATA_CORRUPTED = "DATA_CORRUPTED"


# 错误类别映射
ERROR_CATEGORIES: Dict[str, str] = {
    # 工具相关
    "TOOL_MISSING": "tool_missing",
    "TOOL_VERSION": "tool_version",
    "TOOL_EXECUTION": "tool_execution",
    "DEPENDENCY": "dependency_error",

    # 权限相关
    "PERM_DENIED": "permission_denied",
    "PERMISSION": "permission_error",

    # 构建相关
    "BUILD_COMPILATION": "compilation_error",
    "BUILD_LINK": "link_error",
    "BUILD_TIMEOUT": "timeout",
    "BUILD_DEPENDENCY": "dependency_missing",
    "BUILD_CONFIG": "config_invalid",
    "BUILD_TARGET": "target_not_found",

    # 运行时相关
    "RUNTIME_SEGFAULT": "runtime_error",
    "RUNTIME_TIMEOUT": "timeout",
    "RUNTIME_MEMORY": "memory_error",
    "RUNTIME_UNKNOWN": "runtime_error",
    "RUNTIME_NULL": "runtime_error",
    "RUNTIME_INDEX": "runtime_error",

    # 网络相关
    "NETWORK_TIMEOUT": "timeout",
    "NETWORK_CONNECTION": "connection_error",
    "NETWORK_DNS": "dns_error",
    "NETWORK_SSL": "ssl_error",
    "NETWORK_UNREACHABLE": "connection_error",
    "NETWORK_AUTHENTICATION": "authentication_failed",

    # 配置相关
    "CONFIG_INVALID": "config_invalid",
    "CONFIG_MISSING": "config_missing",
    "CONFIG_PARSE": "parse_error",
    "CONFIG_FILE": "file_not_found",
    "CONFIG_VERSION": "version_mismatch",

    # 验证相关
    "VALIDATION": "validation_error",

    # 文件相关
    "FILE_NOT_FOUND": "file_not_found",
    "FILE_ALREADY_EXISTS": "file_already_exists",
    "FILE_READ": "file_read_error",
    "FILE_WRITE": "file_write_error",
    "FILE_LOCKED": "file_locked",
    "FILE_TOO_LARGE": "file_too_large",
    "FILE_FORMAT": "file_format_error",
    "FILE_ENCODING": "encoding_error",

    # 目录相关
    "DIR_NOT_FOUND": "dir_not_found",
    "DIR_NOT_EMPTY": "dir_not_empty",
    "DIR_CREATE": "dir_create_failed",
    "DIR_ACCESS": "dir_access_denied",

    # 硬件相关
    "HARDWARE_NOT_FOUND": "hardware_not_found",
    "HARDWARE_ACCESS": "hardware_access_denied",
    "HARDWARE_TIMEOUT": "hardware_timeout",
    "HARDWARE_COMMUNICATION": "hardware_communication_error",
    "HARDWARE_INIT": "hardware_init_failed",
    "HARDWARE_NOT_SUPPORTED": "hardware_not_supported",

    # 安全相关
    "SECURITY_HIGH_RISK": "security_high_risk",
    "SECURITY_PERMISSION": "permission_denied",
    "SECURITY_AUTHENTICATION": "authentication_failed",
    "SECURITY_AUTHORIZATION": "authorization_failed",
    "SECURITY_INPUT": "validation_error",
    "SECURITY_INJECTION": "security_injection",

    # 操作相关
    "OPERATION_CANCELLED": "operation_cancelled",
    "OPERATION_TIMEOUT": "timeout",
    "OPERATION_MAX_RETRIES": "max_retries",
    "OPERATION_NOT_SUPPORTED": "not_supported",
    "OPERATION_INVALID_STATE": "invalid_state",
    "OPERATION_NOT_IMPLEMENTED": "not_implemented",

    # 平台相关
    "PLATFORM_NOT_SUPPORTED": "platform_not_supported",
    "PLATFORM_DETECTION": "detection_failed",
    "PLATFORM_ARCH": "arch_mismatch",
    "PLATFORM_VERSION": "version_incompatible",

    # 技能相关
    "SKILL_NOT_FOUND": "skill_not_found",
    "SKILL_LOAD": "skill_load_failed",
    "SKILL_EXECUTE": "skill_execute_failed",
    "SKILL_CONFIG": "skill_config_invalid",
    "SKILL_DEPRECATED": "skill_deprecated",

    # 数据相关
    "DATA_PARSE": "parse_error",
    "DATA_VALIDATION": "validation_error",
    "DATA_FORMAT": "format_error",
    "DATA_CORRUPTED": "data_corrupted",
}


def get_error_category(error_code: str) -> str:
    """获取错误类别"""
    for prefix, category in ERROR_CATEGORIES.items():
        if error_code.startswith(prefix):
            return category
    return "unknown_error"


def is_recoverable(error_code: str) -> bool:
    """判断错误是否可恢复"""
    recoverable_errors = [
        "NETWORK_TIMEOUT",
        "OPERATION_TIMEOUT",
        "FILE_LOCKED",
        "HARDWARE_TIMEOUT",
        "BUILD_TIMEOUT",
    ]
    return any(error_code.startswith(prefix) for prefix in recoverable_errors)


def get_error_message(error_code: str) -> str:
    """获取错误消息"""
    error_messages: Dict[str, str] = {
        "TOOL_NOT_FOUND": "工具未找到",
        "DEPENDENCY_NOT_FOUND": "依赖未找到",
        "PERMISSION_ERROR": "权限错误",
        "BUILD_COMPILATION_ERROR": "编译错误",
        "BUILD_LINK_ERROR": "链接错误",
        "BUILD_TIMEOUT": "构建超时",
        "RUNTIME_UNKNOWN_ERROR": "运行时未知错误",
        "VALIDATION_ERROR": "验证错误",
        "FILE_NOT_FOUND": "文件未找到",
        "DIR_NOT_FOUND": "目录未找到",
        "PLATFORM_NOT_SUPPORTED": "平台不支持",
        "SKILL_NOT_FOUND": "技能未找到",
        "SKILL_EXECUTE_FAILED": "技能执行失败",
    }
    
    for prefix, message in error_messages.items():
        if error_code.startswith(prefix):
            return message
    return "未知错误"


def get_suggestions(error_code: str) -> List[str]:
    """获取错误建议"""
    suggestions_map: Dict[str, List[str]] = {
        "TOOL_NOT_FOUND": ["检查工具是否已安装", "检查 PATH 环境变量"],
        "DEPENDENCY_NOT_FOUND": ["安装缺失的依赖", "检查依赖版本"],
        "PERMISSION_ERROR": ["以管理员身份运行", "检查文件/目录权限"],
        "BUILD_COMPILATION_ERROR": ["检查代码语法", "检查编译选项"],
        "BUILD_LINK_ERROR": ["检查链接库路径", "检查库是否存在"],
        "FILE_NOT_FOUND": ["检查文件路径是否正确", "确认文件存在"],
        "DIR_NOT_FOUND": ["检查目录路径是否正确", "创建缺失的目录"],
        "PLATFORM_NOT_SUPPORTED": ["使用支持的平台", "检查平台兼容性"],
    }
    
    for prefix, suggestions in suggestions_map.items():
        if error_code.startswith(prefix):
            return suggestions
    return ["检查日志获取更多信息"]