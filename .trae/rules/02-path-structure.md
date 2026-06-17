# 路径结构规范

> **版本**：v1.0  
> **日期**：2026-06-17  
> **参考依据**：[02_器具落地规则.md](../../guide/02_器具落地规则.md)（落地场景定义）

---

## 一、路径格式

### 1.1 基础路径格式

```
skills/{category}/{skill-name}/
```

### 1.2 分类目录

| 分类 | 目录名 | 说明 |
|------|--------|------|
| software | skills/software/ | 软件相关技能 |
| hardware | skills/hardware/ | 硬件相关技能 |
| platform | skills/platform/ | 平台相关技能 |
| workflow | skills/workflow/ | 工作流技能 |

---

## 二、命名规范

### 2.1 技能名称规则

| 规则 | 要求 | 示例 | 反例 |
|------|------|------|------|
| **小写字母** | 使用小写字母 | gpio-config | GPIO-Config |
| **连字符分隔** | 使用连字符 `-` | nfs-mount | nfs_mount |
| **不超过20字符** | 名称简洁 | gpio-config | gpio-configuration |
| **英文命名** | 使用英文 | nfs-mount | nfs挂载 |
| **无空格** | 不使用空格 | network-config | network config |

### 2.2 路径规范

| 规范 | 要求 | 示例 |
|------|------|------|
| **全小写** | 路径全小写 | skills/hardware/ |
| **无空格** | 不使用空格 | skills/software/ |
| **无特殊字符** | 仅使用字母数字和连字符 | - |
| **相对路径** | 相对于 plumb-link 根目录 | skills/software/ |

---

## 三、完整目录结构

### 3.1 标准结构

```
skills/{category}/{skill-name}/
├── SKILL.md              # 技能契约（必需）
├── scripts/              # 脚本目录（必需）
│   └── {skill_name}.py   # 主脚本文件
├── agents/               # 大模型接口（可选）
│   └── openai.yaml       # OpenAI 接口配置
├── references/           # 参考文档（可选）
│   └── usage.md          # 使用说明
└── testcases/            # 测试用例（可选）
    └── test_*.py         # 测试文件
```

### 3.2 最小结构

```
skills/{category}/{skill-name}/
├── SKILL.md              # 必需
└── scripts/              # 必需
    └── {skill_name}.py   # 必需
```

---

## 四、路径示例

### 4.1 软件技能

```
skills/software/build-linux-app/
├── SKILL.md
├── scripts/
│   └── build_linux_app.py
└── agents/
    └── openai.yaml
```

### 4.2 硬件技能

```
skills/hardware/gpio-config/
├── SKILL.md
├── scripts/
│   └── gpio_config.py
└── agents/
    └── openai.yaml
```

### 4.3 平台技能

```
skills/platform/linux-build/
├── SKILL.md
├── scripts/
│   └── linux_build.py
└── agents/
    └── openai.yaml
```

### 4.4 工作流技能

```
skills/workflow/project-init/
├── SKILL.md
├── scripts/
│   └── project_init.py
└── agents/
    └── openai.yaml
```

---

## 五、路径冲突检测

### 5.1 冲突检测规则

| 冲突类型 | 检测方法 | 处理方式 |
|---------|---------|---------|
| **同名技能** | 检查 skill_registry.yaml | 返回错误 |
| **同名目录** | 检查 skills/ 下目录 | 返回错误 |
| **非法字符** | 检查名称字符 | 返回修正建议 |

### 5.2 冲突检测流程

```
步骤 1：生成路径
    │
    ▼
步骤 2：检查分类目录
    │
    ├─ 分类目录存在 → 继续
    └─ 分类目录不存在 → 创建目录
    │
    ▼
步骤 3：检查技能目录
    │
    ├─ 技能目录不存在 → 可用
    └─ 技能目录已存在 → 冲突
    │
    ▼
步骤 4：返回结果
```

---

## 六、生成器专用路径

### 6.1 技能生成器路径

```
plumb-link/
├── .trae/                      # 技能生成器目录
│   ├── SKILL.md               # 技能生成器入口
│   ├── rules/                 # 生成规则
│   │   ├── 00-skill-generation.md
│   │   ├── 01-minimal-unit.md
│   │   ├── 02-path-structure.md
│   │   ├── 03-metadata-std.md
│   │   └── 04-registry-update.md
│   └── skills/                # 生成器专用技能
│       ├── skill-analyzer/
│       │   └── SKILL.md
│       ├── skill-creator/
│       │   └── SKILL.md
│       └── registry-updater/
│           └── SKILL.md
```

### 6.2 生成技能存放路径

```
plumb-link/
└── skills/                    # 生成的技能存放位置
    ├── software/
    ├── hardware/
    ├── platform/
    └── workflow/
```

---

## 七、路径验证

### 7.1 验证检查清单

| 检查项 | 检查内容 | 验证方法 |
|--------|---------|---------|
| **格式正确** | 符合 `skills/{category}/{skill-name}/` | 正则匹配 |
| **分类有效** | 分类在四大类中 | 分类列表检查 |
| **名称有效** | 符合命名规范 | 命名规则检查 |
| **无冲突** | 路径未被占用 | 目录检查 |
| **目录完整** | 包含必需文件 | 文件列表检查 |

### 7.2 验证输出

```json
{
  "path": "skills/hardware/gpio-config/",
  "valid": true,
  "checks": {
    "format": {
      "status": "pass",
      "pattern": "skills/{category}/{skill-name}/"
    },
    "category": {
      "status": "pass",
      "category": "hardware",
      "valid_categories": ["software", "hardware", "platform", "workflow"]
    },
    "name": {
      "status": "pass",
      "name": "gpio-config",
      "length": 11,
      "valid": true
    },
    "conflict": {
      "status": "pass",
      "exists": false
    }
  }
}
```
