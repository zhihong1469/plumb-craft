# 注册表更新规则

> **版本**：v1.0  
> **日期**：2026-06-17  
> **参考依据**：[06_plumb-link技能生成器规则.md](../../guide/06_plumb-link技能生成器规则.md)（技能生成器规则）

---

## 一、注册表位置

### 1.1 注册表文件

```
plumb-link/agents/skill_registry.yaml
```

### 1.2 注册表结构

```yaml
skills:
  - name: build-linux-app
    category: software
    version: 1.0.0
    description: "编译 Linux 应用程序"
    keywords:
      - "编译"
      - "build"
      - "make"
    agents:
      - openai
      - claude
      - trae
    shared_deps:
      - tool_config
      - build_utils
    platforms:
      - linux
      - windows
      - macos
    required_tools:
      - gcc
      - make
    author: "Plumb-Link Team"
    license: "MIT"
    status: "stable"
```

---

## 二、更新流程

### 2.1 更新步骤

```
步骤 1：读取 skill_registry.yaml
    │
    ▼
步骤 2：验证技能信息完整性
    │
    ▼
步骤 3：检查是否已存在
    │
    ├─ 已存在 → 返回冲突
    └─ 不存在 → 继续
    │
    ▼
步骤 4：添加到 skills 列表
    │
    ▼
步骤 5：保存更新后的文件
    │
    ▼
步骤 6：返回更新结果
```

### 2.2 更新类型

| 更新类型 | 触发条件 | 处理方式 |
|---------|---------|---------|
| **新增技能** | 生成新技能 | 添加到 skills 列表 |
| **更新技能** | 技能升级 | 更新对应记录 |
| **删除技能** | 技能移除 | 从列表中删除 |
| **批量更新** | 多个技能变更 | 批量处理 |

---

## 三、技能记录格式

### 3.1 完整记录格式

```yaml
skills:
  - name: {skill-name}              # 必需：技能名称
    category: {category}            # 必需：分类
    version: 1.0.0                  # 必需：版本号
    description: "{描述}"           # 必需：技能描述
    keywords:                        # 必需：关键词
      - "关键词1"
      - "关键词2"
    agents:                          # 推荐：支持的大模型
      - openai
      - claude
      - trae
    shared_deps:                     # 可选：共享依赖
      - tool_config
    platforms:                       # 必需：支持平台
      - linux
      - windows
    required_tools:                  # 必需：必需工具
      - tool1
    optional_tools:                  # 可选：可选工具
      - tool2
    author: "Plumb-Link Team"        # 推荐：作者
    license: "MIT"                  # 推荐：许可证
    status: "stable"                # 推荐：状态
    generated_at: "2026-06-17"      # 自动：生成时间
```

### 3.2 必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 技能名称（小写字母+连字符） |
| category | string | 分类（software/hardware/platform/workflow） |
| version | string | 版本号（语义化版本） |
| description | string | 技能描述 |
| keywords | array | 关键词列表 |
| platforms | array | 支持平台 |
| required_tools | array | 必需工具 |

### 3.3 推荐字段

| 字段 | 类型 | 说明 |
|------|------|------|
| agents | array | 支持的大模型 |
| shared_deps | array | 共享依赖 |
| author | string | 作者 |
| license | string | 许可证 |
| status | string | 状态（stable/beta/develop） |
| generated_at | string | 生成时间 |

---

## 四、更新验证

### 4.1 更新前验证

| 检查项 | 检查内容 | 不通过处理 |
|--------|---------|-----------|
| **字段完整性** | 是否包含所有必需字段 | 返回错误 |
| **字段格式** | 字段类型是否正确 | 返回错误 |
| **分类有效性** | 分类是否在四大类中 | 返回错误 |
| **工具有效性** | 工具名称是否符合规范 | 返回警告 |
| **重复检测** | 是否已存在同名技能 | 返回冲突 |

### 4.2 更新后验证

| 检查项 | 检查内容 | 失败处理 |
|--------|---------|-----------|
| **文件保存** | 文件是否成功保存 | 返回错误 |
| **数据完整性** | 数据是否完整保存 | 返回错误 |
| **YAML 语法** | YAML 语法是否正确 | 返回错误 |

---

## 五、更新输出

### 5.1 成功输出

```json
{
  "status": "success",
  "summary": "技能注册表更新成功",
  "updated_skill": {
    "name": "gpio-config",
    "category": "hardware",
    "version": "1.0.0"
  },
  "registry_location": "agents/skill_registry.yaml"
}
```

### 5.2 失败输出

```json
{
  "status": "failure",
  "failure_category": "registry_update_error",
  "error_code": "REG_001",
  "summary": "技能注册表更新失败",
  "error_details": "缺少必需字段: category",
  "suggestions": [
    "请补充 category 字段",
    "category 必须为: software/hardware/platform/workflow"
  ]
}
```

### 5.3 冲突输出

```json
{
  "status": "failure",
  "failure_category": "skill_conflict",
  "error_code": "REG_002",
  "summary": "技能已存在",
  "existing_skill": {
    "name": "gpio-config",
    "category": "hardware",
    "version": "1.0.0"
  },
  "suggestions": [
    "使用不同的技能名称",
    "更新现有技能版本"
  ]
}
```

---

## 六、批量更新

### 6.1 批量更新格式

```yaml
batch_update:
  operations:
    - operation: add
      skill:
        name: nfs-mount
        category: software
        # ... 其他字段
    - operation: update
      skill_name: gpio-config
      updates:
        version: "1.0.1"
    - operation: delete
      skill_name: old-skill
```

### 6.2 批量更新验证

| 检查项 | 检查内容 | 处理方式 |
|--------|---------|---------|
| **操作有效性** | 操作类型是否有效 | 返回错误 |
| **技能存在性** | 被更新/删除的技能是否存在 | 返回错误 |
| **字段完整性** | 新增/更新的字段是否完整 | 返回错误 |

---

## 七、最佳实践

### 7.1 更新时机

| 时机 | 说明 | 建议 |
|------|------|------|
| **生成技能后** | 立即更新注册表 | 必须 |
| **技能升级后** | 更新版本号 | 必须 |
| **技能废弃后** | 从注册表删除 | 推荐 |
| **定期维护** | 检查注册表一致性 | 推荐 |

### 7.2 数据维护

| 维护项 | 说明 | 频率 |
|--------|------|------|
| **版本同步** | 确保版本号与实际一致 | 每次升级 |
| **状态更新** | 更新技能状态 | 每次状态变更 |
| **依赖更新** | 更新共享依赖列表 | 每次依赖变更 |
| **一致性检查** | 检查注册表与实际目录一致性 | 每月 |

### 7.3 备份策略

| 策略 | 说明 | 频率 |
|------|------|------|
| **自动备份** | 每次更新前备份 | 必须 |
| **版本控制** | 使用 Git 版本控制 | 必须 |
| **定期归档** | 归档历史版本 | 每月 |
