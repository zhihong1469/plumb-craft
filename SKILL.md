---
name: plumb-link
description: plumb-link 技能集的总控入口。核心职责是技能生成器的入口，引导用户生成新技能。同时提供安装指引和指令消歧能力，技能列表统一由 agents/skill_registry.yaml 管理。
metadata:
  internal: true
---

# plumb-link 总控

本技能负责三类交互：**安装指引**、**指令消歧**、**技能生成引导**。

---

## 一、安装指引

当用户请求安装 plumb-link 项目的 skill 时，引导用户查看安装说明文件。

### 1.1 安装说明位置

安装相关信息请参考：
- **安装脚本**：`scripts/install.py`
- **技能列表**：`agents/skill_registry.yaml`（统一管理所有技能元数据）

### 1.2 安装方式

```bash
# 全部安装
python3 scripts/install.py /path/to/project

# 按需安装（参考 agents/skill_registry.yaml 获取技能名称）
python3 scripts/install.py /path/to/project --skills skill-name1 skill-name2
```

### 1.3 技能列表查询

可用技能列表统一维护在 `agents/skill_registry.yaml`，包含：
- 技能名称、分类、版本
- 关键词、支持平台
- 依赖工具列表

---

## 二、指令消歧

当用户发出模糊指令时，先尝试自动探测；若无法明确判断，从注册表查询候选 skill 让用户选择。

### 2.1 消歧流程

```
用户输入模糊指令
    │
    ▼
查询 agents/skill_registry.yaml
    │
    ▼
自动匹配
    │
    ├─ 唯一匹配 → 直接调用对应 skill
    │
    └─ 匹配多个或无法判断 → 列出候选 skill 供用户选择
```

### 2.2 匹配规则

指令消歧通过查询 `agents/skill_registry.yaml` 中的关键词进行匹配：
- **软件技能**：编译、build、make、cmake、构建、交叉编译
- **硬件技能**：GPIO、引脚、i2c、spi、总线、设备
- **平台技能**：freertos、linux、内核、配置
- **工作流技能**：init、项目、deploy、release、部署、发布

### 2.3 示例交互

```
👤 编译
🤖 正在查询可用技能...
🤖 检测到多个匹配技能：
   1. build-linux-app — Linux 应用编译
   2. linux-build — Linux 内核构建
   请输入编号或 skill 名称：

👤 1
🤖 使用 build-linux-app，正在配置编译环境...
```

---

## 三、技能生成引导

当用户希望生成新技能时，引导其使用 plumb-link 根目录的技能生成器。

### 3.1 触发关键词

- "生成一个技能"
- "创建新技能"
- "我想实现一个XXX的技能"
- "我需要一个XXX技能"

### 3.2 生成流程

当用户表达技能生成需求时：

1. **读取入口**：AI 读取 `.trae/SKILL.md`（技能生成器入口）
2. **分析需求**：理解用户的技能需求
3. **最小单元分析**：判断是否需要拆分（参考 `.trae/rules/01-minimal-unit.md`）
4. **确定分类和路径**：根据功能确定技能分类（参考 `.trae/rules/02-path-structure.md`）
5. **生成目录结构**：创建技能目录和文件
6. **更新注册表**：将技能信息添加到 `agents/skill_registry.yaml`
7. **返回结果**：报告生成结果

### 3.3 技能分类体系

| 大类 | 小类示例 | 适用场景 |
|------|---------|---------|
| **software** | T(编译)、D(部署)、V(版本)、O(运维)、S(服务)、A(应用) | 软件相关技能 |
| **hardware** | HW(硬件) | 硬件相关技能 |
| **platform** | PL(平台) | 平台相关技能 |
| **workflow** | WF(工作流) | 工作流相关技能 |

### 3.4 示例交互

```
👤 我想生成一个 NFS 网络挂载开发板的技能
🤖 正在分析技能需求...

分析结果：
- 是否为最小单元：否
- 拆分方案：
  1. nfs-mount（NFS 挂载）→ software
  2. network-config（网络配置）→ software
  3. board-detect（开发板检测）→ platform

开始生成...

✓ 已生成技能：nfs-mount
  路径：skills/software/nfs-mount/
✓ 已生成技能：network-config
  路径：skills/software/network-config/
✓ 已生成技能：board-detect
  路径：skills/platform/board-detect/

✓ 已更新注册表：agents/skill_registry.yaml

下一步建议：
1. 完善各技能脚本实现
2. 编写测试用例
3. 添加参考文档
```

---

## 四、与 plug-lens 关系

plumb-link 与 plug-lens 形成姊妹双生态：

| 项目 | 定位 | 职责 |
|------|------|------|
| **plug-lens** | 嵌入式业务代码的可插拔架构框架 | 做业务落地 |
| **plumb-link** | 嵌入式AI技能的垂准基准与生态适配框架 | 做开发提效 |

---

## 安装后提示

安装完成后，告知用户：

- 已安装的 skill 列表
- 使用 `/skill-name` 调用具体 skill
- 用自然语言描述需求即可触发对应 skill
- 管理命令：参考 `scripts/install.py` 实现
