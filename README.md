# Plumb-Link Framework

> AI技能落地规范架构：嵌入式软件工程思维升维的大模型工具SDK

---

## 项目名称溯源
### 垂准连接链路（plumb-link）

**「plumb（垂准）」** 源自拉丁语 `plumbum`（铅），本义为工匠校准垂直方向的铅垂线，是工程领域最本源的基准工具，引申三层核心内涵：
- **垂直深耕**：锚定嵌入式垂直赛道，聚焦领域开发痛点，打通通用AI到场景落地的最后一公里，不做泛化能力；
- **基准定规**：定义整套技能集的垂准基准线，上至元设计原则，下至开发规范、质量底线与安全红线，所有能力沿基准落地，保证体系不跑偏、不发散；
- **形意呼应**：拼写与 `plug` 形近，暗含技能单元可插拔、可复用的模块化属性，与姊妹项目 plug-lens 的架构哲学一脉相承。

**「link（链路）」** 本义为链环、连接纽带，是异构系统间协同的核心载体，引申两层核心内涵：
- **生态适配**：搭建通用AI生态（Claude Code / Trae 等宿主）与嵌入式垂直场景之间的适配桥梁，屏蔽平台格式差异，实现「一次开发，多生态运行」；
- **架构暗合**：拼写与 `line` 形近，暗合「线束工程」的分层架构理念，为技能扩展划定清晰跑道，保证体系有序生长、不杂乱。

> 核心立意：plumb-link 的本质是嵌入式AI开发的「铅垂线」——大模型解决效率与数量问题，而垂准线锚定专业边界与工程质量，让AI能力在垂直领域精准落地，有量更有质。

---

## 与 plug-lens 的关系

与 **plug-lens** 形成姊妹双生态：

| 项目 | 定位 | 职责 |
|------|------|------|
| **plug-lens** | 嵌入式业务代码的可插拔架构框架 | 做业务落地 |
| **plumb-link** | 嵌入式AI技能的垂准基准与生态适配框架 | 做开发提效 |

---

## 核心定位

面向大模型的嵌入式级技能开发框架，用软件工程第一性原理构建稳定、可扩展、高质量的 AI 技能生态。

---

## 核心特性

- **六层架构设计**：映射大模型完整思考链路，渐进式信息揭露
- **大模型认知特性适配**：注意力U型分布、两阶段推理、结构化信息提取
- **嵌入式级跨平台兼容**：工具探测五级优先级、路径自动处理、命令封装抽象
- **SOLID原则实践**：单一职责、开闭原则、里氏替换、接口隔离、依赖倒置
- **三重安全校验**：前置检查 → 工具调用前拦截 → 执行后审计
- **与上游平台兼容**：100%复用Claude Code标准，同时增加嵌入式领域增强
- **技能生成器**：在 plumb-link 根目录通过 `.trae/SKILL.md` 引导 AI 生成新技能

---

## 快速开始

### 安装

```bash
pip install -e .
```

### 创建新技能

通过技能生成器在根目录生成：

```bash
# 在 plumb-link 根目录下与 AI 对话
# "我想生成一个 XXX 技能"
```

或使用脚手架工具：

```bash
skill-init create my-skill
```

### 校验技能合规性

```bash
skill-lint my-skill
```

### 运行技能测试

```bash
skill-test my-skill
```

---

## 目录结构

```
plumb-link/
├── SKILL.md                  # 总控入口（安装引导、指令消歧、技能生成引导）
├── .trae/                    # 技能生成器
│   ├── SKILL.md              # 生成器入口
│   ├── rules/                # 生成规则
│   │   ├── 00-skill-generation.md
│   │   ├── 01-minimal-unit.md
│   │   ├── 02-path-structure.md
│   │   ├── 03-metadata-std.md
│   │   └── 04-registry-update.md
│   └── skills/               # 生成器专用技能
│       ├── skill-analyzer/
│       ├── skill-creator/
│       └── registry-updater/
├── meta-spec/                # 元设计规范（稳定核心）
├── common/                   # 全局公共库（底层能力）
├── framework/                # 框架核心（脚手架能力）
├── platform-knowledge/       # 平台专属知识
├── skills/                   # 专项技能实现
├── templates/                # 输出模板
├── agents/                   # 技能注册表
│   ├── skill_registry.yaml
│   └── template.yaml
└── tools/                    # 开发工具
```

---

## 架构分层

| 层级 | 名称 | 职责 |
|------|------|------|
| L0 | 身份边界层 | 定义角色、核心能力、禁止事项 |
| L1 | 技能索引层 | 技能清单、触发关键词、入口路径 |
| L2 | 通用规则层 | 编码规范、脚本标准、依赖要求 |
| L3 | 平台知识层 | 芯片/平台专属约束、API速查 |
| L4 | 专项技能层 | 具体步骤、工具调用、业务逻辑 |
| L5 | 输出模板层 | 输出格式、结构定义、返回标准 |
| L6 | 安全护栏层 | 高危操作清单、人工确认机制 |

---

## 技能分类体系

| 分类 | 说明 | 示例 |
|------|------|------|
| **software** | 软件相关技能 | build-linux-app、nfs-mount |
| **hardware** | 硬件相关技能 | gpio-config、i2c-scan |
| **platform** | 平台相关技能 | freertos-config、linux-build |
| **workflow** | 工作流相关技能 | project-init、deploy-release |

---

## 文档

### 核心架构文档
- [架构设计文档](meta-spec/01_layer_arch.md)
- [开发规范](meta-spec/04_script_std/)
- [SKILL.md契约标准](meta-spec/03_skill_contract.md)
- [安全规范](meta-spec/06_security_rule.md)

### 设计指南
- [guide/00_道-法-器三维架构原则](../guide/00_道法层技能开发标准层原则.md)
- [guide/01_法维度：六层架构设计](../guide/01_技能术法层架构原则.md)
- [guide/02_器具落地规则](../guide/02_器具落地规则.md)
- [guide/06_plumb-link技能生成器规则](../guide/06_plumb-link技能生成器规则.md)
> 是的，如果我们把技能点比作器，我们就可以把本项目看做是法则。
---

## 开源参考

本项目在设计与实现过程中参考了以下优秀的开源项目，向它们致敬：

### 核心参考

| 项目 | 链接 | 参考内容 |
|------|------|----------|
| **embed-ai-tool** | https://github.com/LeoKemp223/embed-ai-tool.git | 嵌入式AI技能集设计、SKILL.md结构、安装脚本 |
| **claude-code** | https://github.com/anthropics/claude-code.git | 技能标准、能力扩展、Claude API集成 |
| **garycli** | https://github.com/garycli/garycli.git | CLI框架设计、插件系统、跨平台支持 |
| **nanoGPT** | https://github.com/karpathy/nanoGPT.git | 模型纯 Transformer架构、性能优化、推理能力 |

### 参考要点

- **embed-ai-tool**：参考其嵌入式技能集设计、SKILL.md契约格式、安装机制
- **claude-code**：参考其技能标准、能力扩展机制、分清边界不做重复实现
- **garycli**：参考其插件系统、跨平台支持、CLI设计模式，未来可扩展
- **nanoGPT**：未来将进一步了解Transformer架构，完善功能和性能

---

## 许可证

### MIT License

本项目采用 **MIT 许可证** 开源。在项目根目录下的LICENSE 中找到。

MIT 许可证是非常宽泛的开源许可证，与绝大多数开源项目（包括 GPL、Apache、BSD 等）兼容，允许：

- ✅ 商业使用
- ✅ 修改
- ✅ 分发
- ✅ 私有使用

唯一要求是保留版权声明和许可证声明。

---

## 致谢

感谢所有开源贡献者，是你们的智慧和分享让这个项目成为可能。
