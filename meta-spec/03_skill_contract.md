# SKILL.md 接口契约标准

> 所有技能必须遵循的统一契约格式

---

## 契约格式规范

每个技能必须包含 `SKILL.md` 文件，格式如下：

```markdown
---
name: skill-name
version: 1.0.0
description: 技能描述（一句话说明）
keywords: ["关键词1", "关键词2", "关键词3"]
platforms: ["linux", "windows"]
required_tools: ["tool1", "tool2"]
output_format: structured
author: "作者名称"
license: "MIT"
---

# 技能说明

## 触发条件
- 用户提到"关键词1"、"关键词2"等
- 当前目录满足特定条件
- 检测到特定文件

## 执行步骤
1. 第一步操作
2. 第二步操作
3. 第三步操作

## 输出格式
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | ✅ | success/partial/failure |
| summary | string | ✅ | 执行摘要 |
| evidence | array | ✅ | 证据/输出文件列表 |
| failure_category | string | ❌ | 失败类型（仅失败时） |

## 依赖工具
| 工具名称 | 用途 | 检测方法 |
|---------|------|---------|
| gcc | 编译 | gcc --version |
| make | 构建 | make --version |

## 安全注意事项
- 高危操作说明
- 人工确认要求
- 权限需求

## 参考资料
- [文档链接1](url)
- [文档链接2](url)
```

---

## YAML Frontmatter 字段说明

### 必填字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| name | string | 技能名称（小写+连字符） | build-linux-app |
| version | string | 版本号（语义化版本） | 1.0.0 |
| description | string | 技能描述 | 编译 Linux 应用程序 |
| keywords | array | 触发关键词列表 | ["编译", "build", "make"] |
| platforms | array | 支持的平台列表 | ["linux"] |
| required_tools | array | 必需的工具列表 | ["gcc", "make"] |
| output_format | string | 输出格式 | structured |

### 可选字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| author | string | 作者名称 | Your Name |
| license | string | 许可证 | MIT |
| category | string | 技能分类 | build |
| priority | number | 优先级（1-10） | 5 |

---

## 输出格式规范

### 标准输出结构

所有技能必须返回以下结构化输出：

```json
{
  "status": "success|partial|failure",
  "summary": "执行摘要",
  "evidence": [
    {
      "type": "file|directory|command",
      "path": "路径",
      "description": "描述"
    }
  ],
  "failure_category": "tool_missing|permission_denied|compilation_error|runtime_error",
  "details": {
    "additional_field": "value"
  }
}
```

### Status 字段说明

| 值 | 说明 | 使用场景 |
|----|------|---------|
| success | 完全成功 | 所有步骤都成功完成 |
| partial | 部分成功 | 主要目标达成，但有次要问题 |
| failure | 完全失败 | 主要目标未达成 |

### Failure Category 字段说明

| 值 | 说明 | 示例 |
|----|------|------|
| tool_missing | 工具缺失 | gcc not found |
| permission_denied | 权限不足 | cannot write to directory |
| compilation_error | 编译错误 | syntax error in code |
| runtime_error | 运行时错误 | segmentation fault |
| network_error | 网络错误 | connection timeout |
| validation_error | 验证失败 | invalid configuration |

---

## 触发关键词规范

### 关键词设计原则
- 使用用户常用词汇
- 避免过于专业的术语
- 支持中英文双语
- 包含同义词

### 关键词示例

| 技能 | 关键词 |
|------|--------|
| build-linux-app | ["编译", "build", "make", "cmake", "构建"] |
| flash-imx6ull | ["烧录", "flash", "刷机", "下载"] |
| debug-app | ["调试", "debug", "gdb", "断点"] |

---

## 平台支持规范

### 平台标识

| 标识 | 说明 | 示例系统 |
|------|------|---------|
| linux | Linux 系统 | Ubuntu, Debian, CentOS |
| windows | Windows 系统 | Windows 10, Windows 11 |
| macos | macOS 系统 | macOS 12, macOS 13 |

### 跨平台处理

技能必须处理不同平台的差异：
- 路径分隔符：`/` vs `\`
- 命令差异：`ls` vs `dir`
- 权限处理：chmod vs ACL

---

## 工具检测规范

### 检测方法

```python
from common.src.cmd_utils import check_tool

def check_required_tools():
    tools = ["gcc", "make", "cmake"]
    for tool in tools:
        if not check_tool(tool):
            return {
                "status": "failure",
                "summary": f"工具 {tool} 未安装",
                "failure_category": "tool_missing"
            }
    return {"status": "success"}
```

### 工具检测优先级

1. 用户自定义路径（环境变量）
2. 当前工程 `.tools/` 目录
3. 系统 PATH 环境变量
4. 通用工具安装目录
5. 默认路径回退

---

## 安全注意事项规范

### 高危操作清单

| 操作类型 | 风险等级 | 处理策略 |
|----------|---------|---------|
| 硬件烧录 | 高 | 必须人工确认 |
| 系统格式化 | 高 | 必须人工确认 |
| 网络请求 | 中 | 白名单控制 |
| 文件覆盖 | 中 | 备份机制 |
| 脚本执行 | 低 | 参数校验 |

### 安全检查流程

```python
def security_check(operation: str) -> bool:
    """安全检查"""
    high_risk_ops = ["format", "erase", "flash"]
    if operation in high_risk_ops:
        return request_user_confirmation()
    return True
```

---

## 违反示例

❌ SKILL.md 缺少 YAML frontmatter
❌ 关键词过于专业：["交叉编译", "工具链"]
❌ 输出格式不规范
❌ 没有安全注意事项

---

## 正确示例

✅ 完整的 YAML frontmatter
✅ 用户友好的关键词
✅ 标准化的输出格式
✅ 完整的安全注意事项

---

## 总结

| 规范 | 要求 |
|------|------|
| **文件格式** | YAML frontmatter + Markdown 内容 |
| **必填字段** | name, version, description, keywords, platforms, required_tools |
| **输出格式** | 标准化 JSON 结构 |
| **关键词** | 用户友好，支持双语 |
| **平台支持** | 明确支持的平台列表 |
| **工具检测** | 五级优先级检测 |
| **安全规范** | 高危操作人工确认 |