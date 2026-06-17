# 元数据标准

> **版本**：v1.0  
> **日期**：2026-06-17  
> **参考依据**：[00_道-法-器三维架构：技能开发标准原则.md](../../guide/00_道法层技能开发标准层原则.md)（四大元原则）

---

## 一、SKILL.md 元数据标准

### 1.1 标准格式

```markdown
---
name: {skill-name}
version: 1.0.0
description: {技能描述}
keywords: ["关键词1", "关键词2", "关键词3"]
platforms: ["linux", "windows", "macos"]
required_tools: ["工具1", "工具2"]
optional_tools: ["工具3"]
output_format: structured
author: "Plumb-Link Team"
license: "MIT"
---

# 技能说明

## 触发条件
- 触发条件1
- 触发条件2

## 执行步骤
1. 步骤1
2. 步骤2
3. 步骤3

## 输出格式
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | ✅ | success/partial/failure |
| summary | string | ✅ | 执行摘要 |
| evidence | array | ✅ | 输出文件列表和命令信息 |
| failure_category | string | ❌ | 失败类型（仅失败时） |
| error_code | string | ❌ | 错误码（仅失败时） |

## 依赖工具
| 工具名称 | 用途 | 检测方法 |
|---------|------|---------|
| 工具1 | 用途1 | 检测方法1 |
| 工具2 | 用途2 | 检测方法2 |

## 失败分类
| 分类 | 说明 | 建议 |
|------|------|------|
| tool_missing | 缺少必需工具 | 安装对应工具，检查 PATH |
| config_error | 配置错误 | 检查配置参数 |
| execution_error | 执行错误 | 查看详细错误信息 |

## 安全注意事项
- 注意事项1
- 注意事项2

## 参考资料
- [参考1](url1)
- [参考2](url2)
```

### 1.2 必需字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 技能名称（小写字母+连字符） |
| version | string | ✅ | 版本号（语义化版本） |
| description | string | ✅ | 技能描述（简短说明） |
| keywords | array | ✅ | 关键词列表（用于触发匹配） |
| platforms | array | ✅ | 支持的平台 |
| required_tools | array | ✅ | 必需工具 |
| output_format | string | ✅ | 输出格式（固定为 structured） |

### 1.3 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| optional_tools | array | 可选工具 |
| author | string | 作者 |
| license | string | 许可证 |

### 1.4 字段规范

| 字段 | 规范 | 示例 |
|------|------|------|
| name | 小写字母+连字符，不超过20字符 | gpio-config |
| version | 语义化版本（x.y.z） | 1.0.0 |
| description | 简短描述，不超过100字符 | GPIO 引脚配置技能 |
| keywords | 字符串数组，3-10个关键词 | ["gpio", "配置", "引脚"] |
| platforms | 平台列表 | ["linux", "windows"] |
| required_tools | 工具名称列表 | ["python3"] |

---

## 二、agents/openai.yaml 元数据标准

### 2.1 标准格式

```yaml
interface:
  display_name: "{技能显示名称}"
  short_description: "{简短描述}"
  default_prompt: |
    使用 {skill-name} 技能完成任务...

intent_keywords:
  - "关键词1"
  - "关键词2"
  - "关键词3"

file_patterns:
  - "*.ext1"
  - "*.ext2"

platforms:
  - linux
  - windows
  - macos

required_tools:
  - tool1
  - tool2

optional_tools:
  - tool3

handoff:
  on_success:
    - next-skill1
    - next-skill2
  on_failure:
    - failure-type: next-skill
```

### 2.2 必需字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| interface | object | ✅ | 接口配置 |
| interface.display_name | string | ✅ | 显示名称 |
| interface.short_description | string | ✅ | 简短描述 |
| intent_keywords | array | ✅ | 意图关键词 |
| platforms | array | ✅ | 支持平台 |

### 2.3 字段规范

| 字段 | 规范 | 示例 |
|------|------|------|
| display_name | 中文显示名称 | GPIO 配置 |
| short_description | 简短描述，不超过50字符 | 配置 GPIO 引脚 |
| intent_keywords | 3-10个触发关键词 | ["gpio", "引脚", "配置"] |
| platforms | 平台列表 | ["linux", "windows"] |

---

## 三、生成器技能元数据标准

### 3.1 skill-analyzer 元数据

```yaml
name: skill-analyzer
version: 1.0.0
description: "分析用户技能需求，判断最小单元"
keywords:
  - "技能分析"
  - "需求分析"
  - "最小单元"
category: workflow
```

### 3.2 skill-creator 元数据

```yaml
name: skill-creator
version: 1.0.0
description: "创建新技能目录结构"
keywords:
  - "技能创建"
  - "目录生成"
category: workflow
```

### 3.3 registry-updater 元数据

```yaml
name: registry-updater
version: 1.0.0
description: "更新技能注册表"
keywords:
  - "注册表更新"
  - "技能注册"
category: workflow
```

---

## 四、元数据验证

### 4.1 SKILL.md 验证清单

| 检查项 | 检查内容 | 失败处理 |
|--------|---------|---------|
| **必需字段** | name, version, description 等 | 返回错误 |
| **字段格式** | 类型是否正确 | 返回错误 |
| **字段规范** | 是否符合命名规范 | 返回修正建议 |
| **触发条件** | 是否包含触发关键词 | 返回建议 |
| **输出格式** | 是否包含输出格式定义 | 返回建议 |

### 4.2 openai.yaml 验证清单

| 检查项 | 检查内容 | 失败处理 |
|--------|---------|---------|
| **必需字段** | display_name, intent_keywords 等 | 返回错误 |
| **字段格式** | 类型是否正确 | 返回错误 |
| **关键词数量** | 是否在 3-10 个之间 | 返回建议 |
| **平台列表** | 是否有效平台 | 返回错误 |

---

## 五、元数据模板生成

### 5.1 SKILL.md 模板生成

```python
def generate_skill_metadata(skill_name: str, description: str, 
                          keywords: list, platforms: list,
                          required_tools: list) -> dict:
    """生成 SKILL.md 元数据"""
    return {
        "name": skill_name,
        "version": "1.0.0",
        "description": description,
        "keywords": keywords,
        "platforms": platforms,
        "required_tools": required_tools,
        "output_format": "structured",
        "author": "Plumb-Link Team",
        "license": "MIT"
    }
```

### 5.2 openai.yaml 模板生成

```python
def generate_openai_metadata(skill_name: str, display_name: str,
                            keywords: list, platforms: list) -> dict:
    """生成 agents/openai.yaml 元数据"""
    return {
        "interface": {
            "display_name": display_name,
            "short_description": f"使用 {display_name} 技能",
            "default_prompt": f"使用 {skill_name} 技能完成任务..."
        },
        "intent_keywords": keywords,
        "platforms": platforms,
        "required_tools": [],
        "optional_tools": [],
        "handoff": {
            "on_success": [],
            "on_failure": []
        }
    }
```
