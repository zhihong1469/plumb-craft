# 全局目录结构规范

> 所有技能必须遵循的统一目录结构标准

---

## 整体目录结构

```
skill-framework/                  # 技能开发框架（母工程）
├── LICENSE
├── pyproject.toml
├── README.md
│
# ===================== 【元规范层】稳定核心（永久不变区）=====================
├── meta-spec/                    # 元设计规范全集
│   ├── 00_principles.md          # 四大元原则
│   ├── 01_layer_arch.md          # 整体分层架构
│   ├── 02_dir_std.md             # 全局目录结构规范（本文件）
│   ├── 03_skill_contract.md      # SKILL.md 接口契约标准
│   ├── 04_script_std/            # Python 脚本开发规范
│   ├── 05_dependency_rule.md     # 技能调用、依赖、编排规则
│   ├── 06_security_rule.md       # 安全红线
│   └── appendix/                 # 附录
│       ├── keyword_list.md       # 触发关键词规范
│       ├── exit_code.md          # 全局错误码定义
│       └── platform_map.md       # 系统/平台映射表
│
# ===================== 【系统基建层】公共基础（底层能力）=====================
├── common/                       # 全局公共库
│   ├── inc/                      # 头文件/常量/结构体定义
│   │   ├── platform_def.py       # 平台枚举、路径常量
│   │   ├── error_code.py         # 全局统一错误码
│   │   └── data_struct.py        # 标准输出结构体
│   └── src/                      # 实现源码
│       ├── platform_detect.py    # 跨平台探测
│       ├── path_utils.py         # 统一路径处理
│       ├── cmd_utils.py          # 跨平台命令封装
│       ├── config_parser.py      # 统一配置解析
│       └── log_utils.py          # 全局日志规范
│
# ===================== 【核心框架层】脚手架能力 =====================
├── framework/                    # 框架核心
│   ├── src/
│   │   ├── skill_init.py         # 脚手架1：一键新建技能目录
│   │   ├── skill_lint.py         # 脚手架2：合规检查
│   │   ├── skill_test.py         # 脚手架3：批量测试
│   │   └── workflow_orch.py      # 技能编排引擎
│   └── templates/                # 技能模板
│       ├── skill_base_template/  # 基础技能模板
│       └── plugin_template/      # 插件完整模板
│
# ===================== 【平台适配层】芯片/平台专属知识 =====================
├── platform-knowledge/           # L3 平台知识
│   ├── rk3562.md                 # RK3562 专属约束
│   ├── imx6ull.md                # i.MX6ULL 专属约束
│   └── common-linux.md           # 通用 Linux 知识
│
# ===================== 【专项技能层】业务技能实现 =====================
├── skills/                       # L4 专项技能
│   ├── build-linux-app/          # 示例技能
│   │   ├── SKILL.md              # 技能契约文件
│   │   ├── scripts/              # 执行脚本
│   │   │   ├── inc/
│   │   │   └── src/
│   │   ├── references/           # 参考资料
│   │   └── testcases/            # 测试用例
│   └── flash-imx6ull/            # 示例技能
│
# ===================== 【输出模板层】格式规范 =====================
├── templates/                    # L5 输出模板
│   ├── code/                     # 代码输出模板
│   ├── build/                    # 构建输出模板
│   └── report/                   # 报告输出模板
│
# ===================== 【工程运维层】人类使用 =====================
├── tools/                        # 开发工具
├── tests/                        # 框架测试
└── docs/                         # 文档
```

---

## 技能目录标准结构

每个技能必须遵循以下标准结构：

```
skill-name/
├── SKILL.md                      # ✅ 必需：技能契约文件
├── scripts/                      # ✅ 必需：执行脚本目录
│   ├── inc/                      # ✅ 必需：头文件/常量定义
│   │   └── skill_config.py       # 技能配置定义
│   └── src/                      # ✅ 必需：实现源码
│       ├── main.py               # ✅ 必需：主入口
│       ├── executor.py           # 可选：执行器
│       └── utils.py              # 可选：工具函数
├── references/                   # 可选：参考资料目录
│   ├── api_reference.md          # API参考文档
│   └── examples/                 # 示例代码
└── testcases/                    # 可选：测试用例目录
    ├── test_normal.py            # 正常场景测试
    ├── test_failure.py           # 失败场景测试
    └── test_edge.py              # 边界场景测试
```

---

## 目录命名规范

### 技能目录命名
- 使用小写字母和连字符：`build-linux-app`
- 避免使用下划线：`build_linux_app` ❌
- 使用描述性名称：`flash-imx6ull` ✅

### 文件命名规范
- Python文件：使用下划线分隔：`skill_config.py`
- Markdown文件：使用下划线分隔：`api_reference.md`
- 配置文件：使用点分隔：`skill.config.json`

---

## 三类内容划分

| 类别 | 大模型是否读取 | 包含目录 | 设计原则 |
|------|---------------|----------|----------|
| **模型可读层** | 是，直接进入上下文 | `meta-spec/` 核心规范、`skills/*/SKILL.md`、`platform-knowledge/` | 格式高度结构化，语言极简精准 |
| **脚本执行层** | 否，只看执行结果 | `common/`、`skills/*/scripts/` | 大模型不读源码，只调用脚本 |
| **工程运维层** | 否，完全不进入上下文 | `framework/`、`tools/`、`tests/`、`docs/` | 给开发者用的工具和文档 |

---

## 目录权限规范

### 只读目录
- `meta-spec/`：元规范文件，框架启动后不可修改
- `common/`：公共库，技能不可修改

### 可写目录
- `skills/`：技能目录，可以新增/修改
- `templates/`：模板目录，可以扩展
- `platform-knowledge/`：平台知识，可以新增

---

## 违反示例

❌ 技能目录下没有 `SKILL.md`
❌ 脚本直接放在技能根目录，没有 `scripts/` 子目录
❌ 使用大写字母命名目录：`BuildLinuxApp/`
❌ 在 `common/` 中添加业务逻辑

---

## 正确示例

✅ 每个技能都有标准的目录结构
✅ 使用小写字母和连字符命名
✅ 头文件放在 `inc/`，源码放在 `src/`
✅ 参考资料、测试用例独立目录

---

## 总结

| 规范 | 要求 |
|------|------|
| **目录结构** | 严格遵循标准结构 |
| **命名规范** | 小写字母+连字符 |
| **内容划分** | 模型可读/脚本执行/工程运维三层分离 |
| **权限规范** | 明确只读/可写目录 |
| **自动发现** | 目录即约定，无需注册 |