"""
标准输出结构体定义

定义所有技能必须遵循的输出格式
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Evidence:
    """证据项"""
    type: str  # file, directory, command, output, log
    path: Optional[str] = None  # 路径或命令
    content: Optional[str] = None  # 内容摘要
    title: Optional[str] = None  # 标题
    metadata: Dict[str, Any] = field(default_factory=dict)  # 额外元数据


@dataclass
class SkillResult:
    """技能执行结果"""
    status: str  # success, partial, failure
    summary: str  # 执行摘要
    evidence: List[Evidence] = field(default_factory=list)  # 证据列表
    failure_category: Optional[str] = None  # 失败类别
    error_code: Optional[str] = None  # 错误码
    extra: Dict[str, Any] = field(default_factory=dict)  # 额外数据
    duration: Optional[float] = None  # 执行耗时（秒）
    suggestions: List[str] = field(default_factory=list)  # 解决建议
    recovery_actions: List[str] = field(default_factory=list)  # 恢复操作
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())  # 时间戳

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "status": self.status,
            "summary": self.summary,
            "evidence": [
                {
                    "type": e.type,
                    "path": e.path,
                    "content": e.content,
                    "title": e.title,
                    "metadata": e.metadata
                }
                for e in self.evidence
            ],
            "failure_category": self.failure_category,
            "error_code": self.error_code,
            "extra": self.extra,
            "duration": self.duration,
            "suggestions": self.suggestions,
            "recovery_actions": self.recovery_actions,
            "timestamp": self.timestamp
        }

    @classmethod
    def success(cls, summary: str, evidence: List[Evidence] = None, extra: Dict[str, Any] = None, duration: float = None) -> "SkillResult":
        """创建成功结果"""
        return cls(
            status="success",
            summary=summary,
            evidence=evidence or [],
            extra=extra or {},
            duration=duration
        )

    @classmethod
    def partial(cls, summary: str, evidence: List[Evidence] = None, warnings: List[str] = None, extra: Dict[str, Any] = None) -> "SkillResult":
        """创建部分成功结果"""
        return cls(
            status="partial",
            summary=summary,
            evidence=evidence or [],
            suggestions=warnings or [],
            extra=extra or {}
        )

    @classmethod
    def failure(cls, summary: str, failure_category: str, error_code: str = None, suggestions: List[str] = None, evidence: List[Evidence] = None) -> "SkillResult":
        """创建失败结果"""
        return cls(
            status="failure",
            summary=summary,
            failure_category=failure_category,
            error_code=error_code,
            suggestions=suggestions or [],
            evidence=evidence or []
        )


@dataclass
class ToolDetectionResult:
    """工具检测结果"""
    tool_name: str  # 工具名称
    found: bool  # 是否找到
    path: Optional[str] = None  # 工具路径
    version: Optional[str] = None  # 工具版本
    compatible: bool = True  # 是否兼容

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "tool_name": self.tool_name,
            "found": self.found,
            "path": self.path,
            "version": self.version,
            "compatible": self.compatible
        }


@dataclass
class PlatformInfo:
    """平台信息"""
    system: str  # linux, windows, macos
    arch: str  # x86_64, arm64, armv7
    python_version: str  # Python 版本
    os_version: Optional[str] = None  # OS 版本
    is_wsl: bool = False  # 是否 WSL
    is_container: bool = False  # 是否容器

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "system": self.system,
            "arch": self.arch,
            "python_version": self.python_version,
            "os_version": self.os_version,
            "is_wsl": self.is_wsl,
            "is_container": self.is_container
        }


@dataclass
class BuildConfig:
    """构建配置"""
    compiler: str  # 编译器
    cflags: str = ""  # C 编译选项
    ldflags: str = ""  # 链接选项
    optimization_level: str = "O2"  # 优化级别
    debug_symbols: bool = False  # 调试符号
    parallel_jobs: int = 1  # 并行任务数
    target_arch: str = "arm"  # 目标架构
    sysroot_path: Optional[str] = None  # sysroot 路径

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "compiler": self.compiler,
            "cflags": self.cflags,
            "ldflags": self.ldflags,
            "optimization_level": self.optimization_level,
            "debug_symbols": self.debug_symbols,
            "parallel_jobs": self.parallel_jobs,
            "target_arch": self.target_arch,
            "sysroot_path": self.sysroot_path
        }


@dataclass
class SecurityCheckResult:
    """安全检查结果"""
    operation: str  # 操作类型
    risk_level: str  # 风险级别：high, medium, low
    allowed: bool  # 是否允许
    reason: str = ""  # 原因
    requires_confirmation: bool = False  # 是否需要人工确认

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "operation": self.operation,
            "risk_level": self.risk_level,
            "allowed": self.allowed,
            "reason": self.reason,
            "requires_confirmation": self.requires_confirmation
        }


@dataclass
class SkillMetadata:
    """技能元数据"""
    skill_id: str  # 技能ID
    skill_name: str  # 技能名称
    category: str  # 分类
    author: str  # 作者
    version: str  # 版本
    description: str  # 描述
    keywords: List[str] = field(default_factory=list)  # 关键词
    platforms: List[str] = field(default_factory=list)  # 支持平台
    required_tools: List[str] = field(default_factory=list)  # 依赖工具
    output_format: str = "structured"  # 输出格式

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "category": self.category,
            "author": self.author,
            "version": self.version,
            "description": self.description,
            "keywords": self.keywords,
            "platforms": self.platforms,
            "required_tools": self.required_tools,
            "output_format": self.output_format
        }


@dataclass
class LintIssue:
    """合规检查问题"""
    severity: str  # 级别：error, warning, info
    code: str  # 问题代码
    message: str  # 问题描述
    file: Optional[str] = None  # 文件路径
    line: Optional[int] = None  # 行号

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "file": self.file,
            "line": self.line
        }