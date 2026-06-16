# L1 技能索引层

> L1 技能索引层：技能清单、触发关键词、入口路径
> 全局常驻，紧随身份层，任务分发阶段直接匹配

---

## 技能分类体系

| 分类 | 标识 | 说明 | 目录路径 |
|------|------|------|---------|
| **基础工具类** | T | 通用工具能力，所有技能都可能用到 | `skills/tools/` |
| **开发辅助类** | D | 辅助技能开发的工具 | `skills/dev/` |
| **测试验证类** | V | 测试相关技能 | `skills/test/` |
| **运维管理类** | O | 运维管理能力 | `skills/ops/` |
| **安全防护类** | S | 安全相关技能 | `skills/security/` |
| **AI 适配类** | A | 与大模型交互的适配技能 | `skills/ai/` |
| **软件技能类** | SW | 软件层面的技能（编译、调试、代码生成） | `skills/software/` |
| **硬件技能类** | HW | 硬件层面的技能（电路调试、引脚配置） | `skills/hardware/` |
| **平台技能类** | PL | 平台相关技能（Linux/RTOS/裸机） | `skills/platform/` |
| **工作流编排类** | WF | 工作流编排（多技能组合） | `skills/workflow/` |

---

## 基础工具类（T）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| T001 | 工具探测 | find tool,工具查找,探测工具 | `skills/tools/tool-detect/SKILL.md` | 跨平台 | ✅ 已实现 |
| T002 | 路径规范化 | path,路径处理,路径规范 | `skills/tools/path-normalize/SKILL.md` | 跨平台 | ✅ 已实现 |
| T003 | 命令执行 | exec,run command,执行命令 | `skills/tools/cmd-exec/SKILL.md` | 跨平台 | ✅ 已实现 |
| T004 | 配置解析 | config,配置解析,读取配置 | `skills/tools/config-parser/SKILL.md` | 跨平台 | 📋 待设计 |
| T005 | 日志记录 | log,日志记录,debug | `skills/tools/logging/SKILL.md` | 跨平台 | 📋 待设计 |
| T006 | 文件操作 | file,文件操作,读写文件 | `skills/tools/file-ops/SKILL.md` | 跨平台 | 📋 待设计 |

---

## 开发辅助类（D）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| D001 | 技能初始化 | init,创建技能,新建技能 | `skills/dev/skill-init/SKILL.md` | 跨平台 | ✅ 已实现 |
| D002 | 技能文档生成 | 生成文档,文档导出,doc gen | `skills/dev/doc-gen/SKILL.md` | 跨平台 | 📋 待设计 |
| D003 | 技能打包发布 | 打包,发布,deploy | `skills/dev/skill-package/SKILL.md` | 跨平台 | 📋 待设计 |
| D004 | 技能模板管理 | 模板,template,脚手架 | `skills/dev/template-manager/SKILL.md` | 跨平台 | 📋 待设计 |
| D005 | 架构分析 | 架构分析,架构评估,理想架构 | `skills/dev/arch-analysis/SKILL.md` | 跨平台 | 📋 待设计 |
| D006 | 代码规范编写 | 代码规范,编码规范,code style | `skills/dev/code-style/SKILL.md` | 跨平台 | 📋 待设计 |
| D007 | 项目初始化 | project init,项目初始化 | `skills/dev/project-init/SKILL.md` | 跨平台 | 📋 待设计 |

---

## 测试验证类（V）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| V001 | 技能单元测试 | 测试,单元测试,run test | `skills/test/unit-test/SKILL.md` | 跨平台 | 📋 待设计 |
| V002 | 技能集成测试 | 集成测试,流程测试 | `skills/test/integration-test/SKILL.md` | 跨平台 | 📋 待设计 |
| V003 | 技能合规检查 | lint,合规检查,校验 | `skills/test/skill-lint/SKILL.md` | 跨平台 | ✅ 已实现 |
| V004 | 跨平台兼容性测试 | 跨平台测试,兼容性测试 | `skills/test/compat-test/SKILL.md` | 跨平台 | 📋 待设计 |
| V005 | 边界条件测试 | 边界测试,异常测试 | `skills/test/boundary-test/SKILL.md` | 跨平台 | 📋 待设计 |
| V006 | 性能测试 | 性能测试,benchmark | `skills/test/performance-test/SKILL.md` | 跨平台 | 📋 待设计 |
| V007 | 回归测试 | 回归测试,regression | `skills/test/regression-test/SKILL.md` | 跨平台 | 📋 待设计 |

---

## 运维管理类（O）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| O001 | 技能安装部署 | install,部署,安装 | `skills/ops/skill-install/SKILL.md` | 跨平台 | 📋 待设计 |
| O002 | 技能状态监控 | 监控,状态,health | `skills/ops/skill-monitor/SKILL.md` | 跨平台 | 📋 待设计 |
| O003 | 日志管理 | log,日志,debug | `skills/ops/log-manager/SKILL.md` | 跨平台 | 📋 待设计 |
| O004 | 版本管理 | version,升级,更新 | `skills/ops/version-manager/SKILL.md` | 跨平台 | 📋 待设计 |
| O005 | 资源管理 | resource,资源,memory | `skills/ops/resource-manager/SKILL.md` | 跨平台 | 📋 待设计 |
| O006 | 依赖管理 | dependency,依赖,package | `skills/ops/dependency-manager/SKILL.md` | 跨平台 | 📋 待设计 |

---

## 安全防护类（S）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| S001 | 高危操作拦截 | 安全检查,拦截,protect | `skills/security/high-risk-block/SKILL.md` | 跨平台 | 📋 待设计 |
| S002 | 权限校验 | auth,权限,permission | `skills/security/permission-check/SKILL.md` | 跨平台 | 📋 待设计 |
| S003 | 输入验证 | validate,验证,sanitize | `skills/security/input-validate/SKILL.md` | 跨平台 | 📋 待设计 |
| S004 | 安全审计 | audit,安全审计,日志审计 | `skills/security/security-audit/SKILL.md` | 跨平台 | 📋 待设计 |
| S005 | 数据加密 | encrypt,加密,security | `skills/security/data-encrypt/SKILL.md` | 跨平台 | 📋 待设计 |

---

## AI 适配类（A）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| A001 | 输出格式化 | format,输出格式 | `skills/ai/output-format/SKILL.md` | 跨平台 | ✅ 部分实现 |
| A002 | 意图识别 | intent,识别,路由 | `skills/ai/intent-recognition/SKILL.md` | 跨平台 | 📋 待设计 |
| A003 | 上下文管理 | context,历史,memory | `skills/ai/context-manager/SKILL.md` | 跨平台 | 📋 待设计 |
| A004 | 多模态输出 | multimodal,多模态,图片 | `skills/ai/multimodal-output/SKILL.md` | 跨平台 | 📋 待设计 |
| A005 | 技能推荐 | recommend,推荐,skill suggest | `skills/ai/skill-recommend/SKILL.md` | 跨平台 | 📋 待设计 |

---

## 软件技能类（SW）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| SW001 | build-linux-app | 编译,build,make,cmake | `skills/software/build-linux-app/SKILL.md` | Linux | ✅ 已实现 |
| SW002 | flash-jlink | 烧录,flash,刷机,jlink | `skills/software/flash-jlink/SKILL.md` | Linux/Windows | 📋 待设计 |
| SW003 | debug-gdb | 调试,debug,gdb | `skills/software/debug-gdb/SKILL.md` | Linux | 📋 待设计 |
| SW004 | code-gen | 代码生成,generate,code gen | `skills/software/code-gen/SKILL.md` | 跨平台 | 📋 待设计 |
| SW005 | static-analysis | 静态分析,analyze,lint | `skills/software/static-analysis/SKILL.md` | 跨平台 | 📋 待设计 |
| SW006 | cross-compile | 交叉编译,cross compile | `skills/software/cross-compile/SKILL.md` | Linux | 📋 待设计 |
| SW007 | makefile-generate | makefile,生成构建脚本 | `skills/software/makefile-gen/SKILL.md` | 跨平台 | 📋 待设计 |

---

## 硬件技能类（HW）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| HW001 | gpio-config | gpio,引脚,配置 | `skills/hardware/gpio-config/SKILL.md` | Linux/裸机 | ✅ 待完善 |
| HW002 | i2c-scan | i2c,scan,扫描 | `skills/hardware/i2c-scan/SKILL.md` | Linux/裸机 | ✅ 待完善 |
| HW003 | spi-debug | spi,debug,调试 | `skills/hardware/spi-debug/SKILL.md` | Linux/裸机 | ✅ 待完善 |
| HW004 | uart-debug | uart,serial,串口 | `skills/hardware/uart-debug/SKILL.md` | Linux/裸机 | 📋 待设计 |
| HW005 | rga-image-process | rga,图像处理,格式转换 | `skills/hardware/rga-image-process/SKILL.md` | RK3562 | 📋 待设计 |
| HW006 | pwm-config | pwm,脉冲,配置 | `skills/hardware/pwm-config/SKILL.md` | Linux/裸机 | 📋 待设计 |
| HW007 | adc-read | adc,模数转换,采样 | `skills/hardware/adc-read/SKILL.md` | Linux/裸机 | 📋 待设计 |

---

## 平台技能类（PL）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| PL001 | linux-build | linux,build,构建 | `skills/platform/linux-build/SKILL.md` | Linux | ✅ 待完善 |
| PL002 | freertos-config | freertos,config,配置 | `skills/platform/freertos-config/SKILL.md` | RTOS | ✅ 待完善 |
| PL003 | rt-thread-config | rtthread,config,配置 | `skills/platform/rt-thread-config/SKILL.md` | RTOS | 📋 待设计 |
| PL004 | baremetal-init | baremetal,init,裸机 | `skills/platform/baremetal-init/SKILL.md` | 裸机 | 📋 待设计 |
| PL005 | platform-detect | detect,platform,平台 | `skills/platform/platform-detect/SKILL.md` | 跨平台 | 📋 待设计 |
| PL006 | rknn-inference | rknn,AI推理,神经网络 | `skills/platform/rknn-inference/SKILL.md` | RK3562 | 📋 待设计 |
| PL007 | mpp-video | mpp,视频解码,vpu | `skills/platform/mpp-video/SKILL.md` | RK3562 | 📋 待设计 |
| PL008 | librga-build | librga,RGA,图像加速 | `skills/platform/librga-build/SKILL.md` | RK3562 | 📋 待设计 |

---

## 工作流编排类（WF）

| 技能ID | 技能名称 | 触发关键词 | 入口路径 | 平台支持 | 状态 |
|--------|---------|-----------|---------|---------|------|
| WF001 | project-init | init,项目,初始化 | `skills/workflow/project-init/SKILL.md` | 跨平台 | ✅ 待完善 |
| WF002 | deploy-release | deploy,release,部署 | `skills/workflow/deploy-release/SKILL.md` | 跨平台 | ✅ 待完善 |
| WF003 | ci-cd | ci,cd,自动化 | `skills/workflow/ci-cd/SKILL.md` | 跨平台 | 📋 待设计 |
| WF004 | build-test-deploy | build-test-deploy,构建测试部署 | `skills/workflow/build-test-deploy/SKILL.md` | 跨平台 | 📋 待设计 |
| WF005 | rk3562-porting | rk3562,移植,硬件加速 | `skills/workflow/rk3562-porting/SKILL.md` | RK3562 | 📋 待设计 |

---

## 技能匹配规则

### 优先级顺序

1. **精确匹配**：触发关键词完全匹配
2. **模糊匹配**：触发关键词部分匹配
3. **上下文推断**：根据上下文推断技能类型

### 匹配示例

| 用户输入 | 匹配技能 | 匹配方式 |
|---------|---------|---------|
| "帮我编译一下项目" | SW001 build-linux-app | 精确匹配 |
| "用cmake构建工程" | SW001 build-linux-app | 精确匹配 |
| "配置GPIO引脚" | HW001 gpio-config | 精确匹配 |
| "扫描I2C总线" | HW002 i2c-scan | 精确匹配 |
| "初始化FreeRTOS项目" | PL002 freertos-config | 上下文推断 |

### 路径映射（向后兼容）

| 旧路径 | 新路径 | 说明 |
|--------|--------|------|
| `skills/build-linux-app/` | `skills/software/build-linux-app/` | 软件技能迁移 |
| `skills/flash-jlink/` | `skills/software/flash-jlink/` | 软件技能迁移 |
| `skills/gpio-config/` | `skills/hardware/gpio-config/` | 硬件技能迁移 |

---

## 技能状态说明

| 状态标识 | 说明 |
|---------|------|
| ✅ 已实现 | 技能已完成开发并通过测试 |
| ✅ 部分实现 | 技能部分功能已实现 |
| ✅ 待完善 | 技能框架已创建，待完善实现 |
| 📋 待设计 | 技能待设计和开发 |
| 🔄 开发中 | 技能正在开发中 |

---

## 技能生命周期

```
设计 → 初始化 → 开发 → 测试 → 合规检查 → 发布 → 部署 → 监控 → 更新
  ↓         ↓        ↓       ↓          ↓         ↓        ↓       ↓
D005     D001    编码    V001      V003      D003     O001    O002   O004
```

---

## 技能开发优先级

### P0 - 核心必备（立即实现）

| 技能ID | 技能名称 | 原因 |
|--------|---------|------|
| D001 | 技能初始化 | 快速创建技能的基础 |
| V003 | 技能合规检查 | 保障技能质量的核心工具 |
| T001 | 工具探测 | 跨平台能力的基础 |
| T002 | 路径规范化 | 跨平台能力的基础 |
| T003 | 命令执行 | 跨平台能力的基础 |

### P1 - 功能完善（短期实现）

| 技能ID | 技能名称 | 原因 |
|--------|---------|------|
| V001 | 技能单元测试 | 保障技能质量 |
| D002 | 技能文档生成 | 提高开发效率 |
| D005 | 架构分析 | 核心设计能力 |
| D006 | 代码规范编写 | 保障代码质量 |
| O001 | 技能安装部署 | 部署能力 |

### P2 - 体验优化（中期实现）

| 技能ID | 技能名称 | 原因 |
|--------|---------|------|
| A002 | 意图识别 | 提升 AI 交互体验 |
| S001 | 高危操作拦截 | 安全保障 |
| PL006 | rknn-inference | RK3562 AI 推理 |
| HW005 | rga-image-process | RK3562 图像处理 |