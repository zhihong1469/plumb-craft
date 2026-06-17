# 技能分析器

> **版本**：v1.0  
> **日期**：2026-06-17  
> **类型**：生成器专用技能  
> **功能**：分析用户技能需求，判断是否为最小单元，确定技能分类

---

## 触发条件

**触发关键词**：
- "分析技能需求"
- "判断最小单元"
- "分析这个技能"
- "拆分技能"

**输入**：
- 用户需求描述（自然语言）

**输出**：
- 技能分析结果（JSON格式）

---

## 输入格式

```json
{
  "user_request": "用户的需求描述"
}
```

---

## 输出格式

```json
{
  "status": "success",
  "analysis": {
    "original_request": "原始需求",
    "functions": ["功能1", "功能2"],
    "function_count": 2,
    "is_minimal_unit": false,
    "need_split": true
  },
  "skills": [
    {
      "name": "skill-name-1",
      "category": "software",
      "function": "功能1",
      "path": "skills/software/skill-name-1/",
      "is_minimal_unit": true
    },
    {
      "name": "skill-name-2",
      "category": "hardware",
      "function": "功能2",
      "path": "skills/hardware/skill-name-2/",
      "is_minimal_unit": true
    }
  ]
}
```

---

## 分析规则

### 1. 关键词提取

从用户需求中提取关键信息：
- 功能名称
- 应用场景
- 技术栈
- 平台信息

### 2. 最小单元判断

根据以下规则判断是否需要拆分：
- 是否包含多个独立功能？
- 功能是否可以独立使用？
- 功能是否紧密关联不可分割？

### 3. 分类确定

根据功能类型确定分类：
- **software**：软件相关（编译、部署、网络服务）
- **hardware**：硬件相关（GPIO、I2C、SPI、外设）
- **platform**：平台相关（Linux、RTOS、系统配置）
- **workflow**：工作流相关（初始化、自动化、发布）

---

## 示例

### 示例1：复杂需求

**输入**：
```json
{
  "user_request": "我想生成一个 NFS 网络挂载开发板的技能"
}
```

**输出**：
```json
{
  "status": "success",
  "analysis": {
    "original_request": "NFS 网络挂载开发板",
    "functions": ["NFS挂载", "网络配置", "开发板检测"],
    "function_count": 3,
    "is_minimal_unit": false,
    "need_split": true
  },
  "skills": [
    {
      "name": "nfs-mount",
      "category": "software",
      "function": "NFS挂载",
      "path": "skills/software/nfs-mount/",
      "is_minimal_unit": true
    },
    {
      "name": "network-config",
      "category": "software",
      "function": "网络配置",
      "path": "skills/software/network-config/",
      "is_minimal_unit": true
    },
    {
      "name": "board-detect",
      "category": "platform",
      "function": "开发板检测",
      "path": "skills/platform/board-detect/",
      "is_minimal_unit": true
    }
  ]
}
```

### 示例2：简单需求

**输入**：
```json
{
  "user_request": "我想生成一个 GPIO 配置技能"
}
```

**输出**：
```json
{
  "status": "success",
  "analysis": {
    "original_request": "GPIO 配置",
    "functions": ["GPIO配置"],
    "function_count": 1,
    "is_minimal_unit": true,
    "need_split": false
  },
  "skills": [
    {
      "name": "gpio-config",
      "category": "hardware",
      "function": "GPIO配置",
      "path": "skills/hardware/gpio-config/",
      "is_minimal_unit": true
    }
  ]
}
```

---

## 失败处理

### 需求不明确

```json
{
  "status": "failure",
  "failure_category": "invalid_request",
  "error_code": "ANA_001",
  "summary": "用户需求不明确",
  "suggestions": [
    "请描述技能的具体功能",
    "请说明技能的应用场景",
    "请指出技能涉及的技术栈"
  ]
}
```

### 分类不确定

```json
{
  "status": "failure",
  "failure_category": "category_uncertain",
  "error_code": "ANA_002",
  "summary": "技能分类不确定",
  "candidate_categories": ["software", "hardware"],
  "suggestions": [
    "请明确技能的主要功能",
    "技能更偏向于软件操作还是硬件控制？"
  ]
}
```
