# Plumb-Link 项目结构

> AI 技能落地规范架构 - 项目结构总览

---

## 目录结构

```
plumb-link/
├── .gitignore                          # Git 忽略文件配置
├── LICENSE                             # MIT 许可证
├── README.md                           # 项目说明文档
├── pyproject.toml                      # Python 项目配置
│
├── meta-spec/                          # 元规范层
│   ├── 00_principles.md               # 四大元原则
│   ├── 01_layer_arch.md               # 六层架构设计
│   ├── 02_dir_std.md                  # 目录结构标准
│   ├── 03_skill_contract.md           # SKILL.md 契约标准
│   └── 04_script_std/                 # 脚本编写标准
│       ├── python_style.md            # Python 编码规范
│       ├── cross_platform.md          # 跨平台适配规范
│       └── error_handle.md            # 错误处理标准
│
├── common/                             # 公共能力层
│   ├── inc/                           # 公共头文件
│   │   ├── data_struct.py            # 标准数据结构
│   │   ├── error_code.py             # 错误码定义
│   │   └── platform_def.py           # 平台常量定义
│   └── src/                           # 公共源文件
│       ├── platform_detect.py        # 平台检测模块
│       ├── path_utils.py             # 路径处理模块
│       └── cmd_utils.py              # 命令执行模块
│
├── framework/                          # 框架能力层
│   └── src/                           # 框架源文件
│       ├── skill_init.py             # 技能初始化脚手架
│       ├── skill_lint.py             # 技能合规检查工具
│       ├── skill_test.py             # 技能测试执行工具
│       └── workflow_orch.py          # 工作流编排引擎
│
├── skills/                             # 技能集合层
│   └── build-linux-app/              # 示例技能：Linux 应用构建
│       ├── SKILL.md                  # 技能契约文档
│       ├── README.md                 # 技能说明文档
│       ├── scripts/                  # 技能脚本
│       │   ├── inc/                  # 技能配置
│       │   │   └── skill_config.py  # 构建配置
│       │   └── src/                  # 技能实现
│       │       └── main.py          # 主程序
│       ├── references/               # 参考资料
│       └── testcases/                # 测试用例
│
├── platform-knowledge/                 # 平台知识层
│   ├── rk3562.md                     # RK3562 平台知识
│   ├── imx6ull.md                    # i.MX6ULL 平台知识
│   └── common-linux.md               # 通用 Linux 知识
│
└── templates/                          # 输出模板层
    ├── code/                         # 代码模板
    │   └── code_templates.md         # C/Python/Shell 模板
    ├── build/                        # 构建模板
    │   └── build_templates.md        # 构建输出模板
    └── report/                       # 报告模板
        └── report_templates.md       # 各类报告模板
```

---

## 文件说明

### 根目录文件

| 文件 | 说明 |
|------|------|
| `.gitignore` | Git 版本控制忽略配置 |
| `LICENSE` | MIT 开源许可证 |
| `README.md` | 项目概述、快速开始、目录结构 |
| `pyproject.toml` | Python 项目配置、依赖管理 |

### 元规范层 (meta-spec/)

| 文件 | 说明 |
|------|------|
| `00_principles.md` | 四大元原则：契约优先、变与不变分离、单向依赖、目录即约定 |
| `01_layer_arch.md` | 六层架构：元规范→公共能力→框架能力→技能集合→平台知识→输出模板 |
| `02_dir_std.md` | 全局目录结构、技能目录结构、命名规范 |
| `03_skill_contract.md` | SKILL.md 契约标准：格式、字段、输出格式 |
| `04_script_std/python_style.md` | Python 编码规范：风格、命名、函数结构 |
| `04_script_std/cross_platform.md` | 跨平台适配规范：路径、命令、工具检测 |
| `04_script_std/error_handle.md` | 错误处理标准：错误码、异常、消息格式 |

### 公共能力层 (common/)

| 文件 | 说明 |
|------|------|
| `inc/data_struct.py` | 标准数据结构：SkillResult、Evidence、CommandResult |
| `inc/error_code.py` | 错误码定义：ErrorCode 枚举、错误分类 |
| `inc/platform_def.py` | 平台常量：Platform 枚举、路径配置、工具名称 |
| `src/platform_detect.py` | 平台检测：get_platform_info、find_tool、detect_tool |
| `src/path_utils.py` | 路径处理：normalize_path、join_paths、ensure_directory |
| `src/cmd_utils.py` | 命令执行：run_command、check_tool、execute_script |

### 框架能力层 (framework/)

| 文件 | 说明 |
|------|------|
| `src/skill_init.py` | 技能初始化脚手架：一键创建标准技能目录结构 |
| `src/skill_lint.py` | 技能合规检查工具：检查目录结构、SKILL.md、代码风格 |
| `src/skill_test.py` | 技能测试执行工具：批量执行技能测试用例 |
| `src/workflow_orch.py` | 工作流编排引擎：多技能串行/并行调用 |

### 技能集合层 (skills/)

| 目录 | 说明 |
|------|------|
| `build-linux-app/` | 示例技能：Linux 应用构建 |
| `build-linux-app/SKILL.md` | 技能契约文档：触发条件、执行步骤、输出格式 |
| `build-linux-app/scripts/inc/skill_config.py` | 构建配置：BuildConfig 类、优化级别 |
| `build-linux-app/scripts/src/main.py` | 主程序：BuildExecutor 类、构建逻辑 |

### 平台知识层 (platform-knowledge/)

| 文件 | 说明 |
|------|------|
| `rk3562.md` | RK3562 平台知识：编译器、内核、API 速查、编译参数 |
| `imx6ull.md` | i.MX6ULL 平台知识：编译器、内核、API 速查、编译参数 |
| `common-linux.md` | 通用 Linux 知识：文件系统、进程管理、网络操作 |

### 输出模板层 (templates/)

| 文件 | 说明 |
|------|------|
| `code/code_templates.md` | 代码模板：C、Python、Shell、Makefile、CMakeLists.txt |
| `build/build_templates.md` | 构建模板：构建开始、进度、成功、失败、统计 |
| `report/report_templates.md` | 报告模板：代码审查、测试报告、性能分析、安全审计 |

---

## 快速开始

### 1. 创建新技能

```bash
python framework/src/skill_init.py my-skill --author "Your Name"
```

### 2. 检查技能合规性

```bash
python framework/src/skill_lint.py skills/my-skill
```

### 3. 运行技能测试

```bash
python framework/src/skill_test.py skills/my-skill
```

### 4. 执行技能

```bash
python skills/my-skill/scripts/src/main.py
```

---

## 核心特性

### 1. 六层架构设计
- 元规范层：定义架构原则和标准
- 公共能力层：提供跨平台基础能力
- 框架能力层：提供技能脚手架和工具
- 技能集合层：实现具体业务技能
- 平台知识层：提供平台特定知识
- 输出模板层：提供标准化输出格式

### 2. 跨平台支持
- 自动检测平台信息
- 统一路径处理
- 跨平台命令执行
- 平台特定知识库

### 3. 标准化输出
- 统一的数据结构
- 标准的错误码
- 结构化的结果格式
- 多种输出模板

### 4. 开发工具链
- 技能初始化脚手架
- 合规性检查工具
- 测试执行工具
- 工作流编排引擎

---

## 设计原则

### 1. 契约优先
- SKILL.md 定义技能接口
- 标准化的数据结构
- 明确的输入输出格式

### 2. 变与不变分离
- 公共能力层封装不变部分
- 技能集合层实现变化部分
- 平台知识层隔离平台差异

### 3. 单向依赖
- 上层依赖下层
- 同层模块独立
- 避免循环依赖

### 4. 目录即约定
- 标准化的目录结构
- 清晰的文件组织
- 自动化工具支持

---

## 扩展指南

### 添加新技能
1. 使用 `skill_init.py` 创建技能目录
2. 编辑 `SKILL.md` 定义技能契约
3. 实现 `scripts/src/main.py` 技能逻辑
4. 添加测试用例到 `testcases/`
5. 运行 `skill_lint.py` 检查合规性

### 添加平台知识
1. 在 `platform-knowledge/` 创建新文件
2. 定义平台专属约束
3. 提供 API 速查
4. 列出编译参数

### 添加输出模板
1. 在 `templates/` 创建新目录
2. 定义模板格式
3. 提供使用示例
4. 说明字段含义

---

## 参考资料

- [架构设计原则](meta-spec/00_principles.md)
- [六层架构设计](meta-spec/01_layer_arch.md)
- [目录结构标准](meta-spec/02_dir_std.md)
- [技能契约标准](meta-spec/03_skill_contract.md)
- [Python 编码规范](meta-spec/04_script_std/python_style.md)
- [跨平台适配规范](meta-spec/04_script_std/cross_platform.md)
- [错误处理标准](meta-spec/04_script_std/error_handle.md)

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。