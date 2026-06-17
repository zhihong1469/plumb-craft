# 注册表更新器

> **版本**：v1.0  
> **日期**：2026-06-17  
> **类型**：生成器专用技能  
> **功能**：更新技能注册表 skill_registry.yaml

---

## 触发条件

**触发关键词**：
- "更新注册表"
- "注册技能"
- "添加到注册表"

**输入**：
- 技能信息（来自 skill-creator）

**输出**：
- 更新结果（JSON格式）

---

## 输入格式

```json
{
  "name": "skill-name",
  "category": "hardware",
  "version": "1.0.0",
  "description": "技能描述",
  "keywords": ["关键词1", "关键词2"],
  "platforms": ["linux", "windows"],
  "required_tools": ["tool1"],
  "author": "Plumb-Link Team",
  "license": "MIT"
}
```

---

## 输出格式

### 成功输出

```json
{
  "status": "success",
  "summary": "注册表更新成功",
  "updated_skill": {
    "name": "skill-name",
    "category": "hardware",
    "version": "1.0.0"
  },
  "registry_location": "agents/skill_registry.yaml"
}
```

### 失败输出

```json
{
  "status": "failure",
  "failure_category": "registry_error",
  "error_code": "REG_001",
  "summary": "注册表更新失败",
  "error_details": "缺少必需字段: category"
}
```

---

## 更新流程

### 1. 读取注册表

从 `agents/skill_registry.yaml` 读取现有数据

### 2. 验证数据

检查必需字段是否完整

### 3. 检查冲突

检查是否已存在同名技能

### 4. 添加记录

将新技能添加到 skills 列表

### 5. 保存文件

将更新后的数据写回文件

---

## 注册表格式

```yaml
skills:
  - name: skill-name
    category: hardware
    version: 1.0.0
    description: 技能描述
    keywords:
      - 关键词1
      - 关键词2
    agents:
      - openai
      - claude
      - trae
    platforms:
      - linux
      - windows
    required_tools:
      - tool1
    author: Plumb-Link Team
    license: MIT
    status: stable
    generated_at: 2026-06-17
```

---

## 验证规则

### 必需字段

| 字段 | 说明 |
|------|------|
| name | 技能名称（小写字母+连字符） |
| category | 分类 |
| version | 版本号 |
| description | 描述 |
| keywords | 关键词列表 |
| platforms | 支持平台 |
| required_tools | 必需工具 |

### 分类有效值

| 分类 | 说明 |
|------|------|
| software | 软件技能 |
| hardware | 硬件技能 |
| platform | 平台技能 |
| workflow | 工作流技能 |

---

## 错误处理

### 缺少必需字段

```json
{
  "status": "failure",
  "failure_category": "missing_field",
  "error_code": "REG_001",
  "summary": "缺少必需字段",
  "missing_fields": ["category"],
  "required_fields": ["name", "category", "version", "description", "keywords", "platforms", "required_tools"]
}
```

### 技能已存在

```json
{
  "status": "failure",
  "failure_category": "skill_exists",
  "error_code": "REG_002",
  "summary": "技能已存在",
  "existing_skill": {
    "name": "gpio-config",
    "category": "hardware"
  },
  "suggestions": [
    "使用不同的技能名称",
    "更新现有技能版本"
  ]
}
```

### 注册表文件错误

```json
{
  "status": "failure",
  "failure_category": "file_error",
  "error_code": "REG_003",
  "summary": "注册表文件错误",
  "error_details": "文件不存在或格式错误"
}
```
