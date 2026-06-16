# Skills 目录架构与实现大纲

## 一、设计原则

### 1.1 最小原则
每个技能点只包含一个核心功能，代码量可控，便于 AI 生成和维护。

### 1.2 单文件优先（当前策略）
当前采用**单文件脚本模式**，所有逻辑集中在 `scripts/*.py` 中，不引入跨技能依赖。

### 1.3 共享预留（未来扩展）
当同类技能数量超过 3 个时，可提取公共逻辑到 `common/` 目录，实现代码复用。

---

## 二、目录结构

```
skills/                                    # 技能总目录
├── catalog_frame.md                       # 本文件：架构说明与实现大纲
│
├── software/                              # 软件技能分类
│   ├── common/                            # 软件类技能共享模块（预留空实现）
│   │   ├── tool_config.py                 # 工具配置管理（预留）
│   │   ├── build_utils.py                 # 构建工具函数（预留）
│   │   └── version.py                     # 版本管理（预留）
│   │
│   └── build-linux-app/                   # Linux 应用构建技能（已实现）
│       ├── SKILL.md                       # 技能元数据：触发条件、输出格式、参数说明
│       └── scripts/
│           └── linux_builder.py           # 主脚本：CMake/Makefile 构建、交叉编译、产物扫描
│
├── hardware/                              # 硬件技能分类
│   ├── gpio-config/                       # GPIO 配置技能（空实现）
│   ├── i2c-scan/                          # I2C 扫描技能（空实现）
│   └── spi-debug/                         # SPI 调试技能（空实现）
│
├── platform/                              # 平台技能分类
│   ├── linux-build/                       # Linux 内核构建（空实现）
│   └── freertos-config/                   # FreeRTOS 配置（空实现）
│
└── workflow/                              # 工作流编排技能
    ├── project-init/                      # 项目初始化（空实现）
    └── deploy-release/                    # 部署发布（空实现）
```

---

## 三、技能点标准结构

每个技能点必须包含以下文件：

```
skill-name/
├── SKILL.md                               # 技能元数据（大模型读取）
│   ├── 触发条件（关键词、文件检测）
│   ├── 执行步骤
│   ├── 输出格式（JSON Schema）
│   ├── 命令行参数说明
│   ├── 依赖工具列表
│   └── 失败分类与建议
│
└── scripts/
    └── {skill_name}.py                    # 主脚本（单文件实现）
```

### 3.1 SKILL.md 规范

```markdown
---
name: skill-name
version: 1.0.0
description: 技能描述
keywords: ["关键词1", "关键词2"]
platforms: ["linux", "windows"]
required_tools: ["gcc", "make"]
output_format: structured
---

## 触发条件
- 用户提到"编译"、"build"等关键词
- 当前目录存在 Makefile 或 CMakeLists.txt

## 执行步骤
1. 检测工具链
2. 读取配置
3. 执行构建
4. 收集产物

## 输出格式
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 是 | success/failure |

## 失败分类
| 分类 | 说明 | 建议 |
|------|------|------|
| tool_missing | 缺少工具 | 安装对应工具 |
```

### 3.2 主脚本规范

```python
#!/usr/bin/env python3
"""技能描述"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# 尝试导入共享模块（如果存在）
try:
    from tool_config import get_tool_path
    _HAS_SHARED = True
except ImportError:
    _HAS_SHARED = False

    def get_tool_path(name: str) -> str | None:
        return None


@dataclass
class SkillResult:
    """技能执行结果"""
    status: str  # success, failure
    summary: str
    evidence: list[str] = field(default_factory=list)
    failure_category: str | None = None


def main():
    parser = argparse.ArgumentParser(description="技能描述")
    parser.add_argument("--param", type=str, help="参数说明")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    
    # 执行逻辑
    result = SkillResult(status="success", summary="执行成功")
    
    if args.json:
        print(json.dumps(result.__dict__, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

---

## 四、共享模块演进策略

### 4.1 当前状态（单文件模式）

每个技能点独立实现，无外部依赖。

**优点：**
- 部署简单，复制单个文件即可
- 无版本兼容问题
- AI 生成容易

**缺点：**
- 同类技能代码重复
- 修改公共逻辑需改 N 个文件

### 4.2 触发条件（何时提取共享模块）

当满足以下条件时，提取公共逻辑到 `common/`：

1. **数量阈值**：同类技能 >= 3 个
2. **重复阈值**：公共代码行数 >= 100 行
3. **变更频率**：某段逻辑 1 个月内修改 >= 2 次

### 4.3 提取步骤

```
步骤 1：识别公共代码
   对比 build-linux-app、build-android-app、build-ios-app
   发现重复：detect_tool、scan_artifacts、BuildResult

步骤 2：创建共享模块
   common/
   ├── tool_config.py          # 从各技能提取工具配置逻辑
   └── build_utils.py          # 从各技能提取构建工具函数

步骤 3：修改技能脚本
   原：from tool_config import get_tool_path  # 内置兼容层
   新：from common.tool_config import get_tool_path  # 引用共享模块

步骤 4：验证兼容性
   确保旧技能在新共享模块下仍能运行
```

### 4.4 版本管理

共享模块需维护版本：

```python
# common/version.py
__version__ = "1.0.0"
COMPATIBLE_VERSIONS = ["1.0.0"]

def check_compatibility(required: str) -> bool:
    return required in COMPATIBLE_VERSIONS
```

---

## 五、技能分类与扩展规划

### 5.1 软件技能（software）

| 技能名 | 状态 | 功能 | 共享模块需求 |
|--------|------|------|-------------|
| build-linux-app | 已实现 | Linux 应用构建（CMake/Makefile） | 未来需 build_utils |
| build-android-app | 规划中 | Android 应用构建 | 未来需 build_utils |
| debug-gdb | 规划中 | GDB 调试辅助 | 未来需 debug_utils |
| code-gen | 规划中 | 代码生成模板 | 未来需 template_utils |

### 5.2 硬件技能（hardware）

| 技能名 | 状态 | 功能 | 共享模块需求 |
|--------|------|------|-------------|
| gpio-config | 空实现 | GPIO 引脚配置 | 未来需 board_utils |
| i2c-scan | 空实现 | I2C 设备扫描 | 未来需 bus_utils |
| spi-debug | 空实现 | SPI 通信调试 | 未来需 bus_utils |

### 5.3 平台技能（platform）

| 技能名 | 状态 | 功能 | 共享模块需求 |
|--------|------|------|-------------|
| linux-build | 空实现 | Linux 内核编译 | 未来需 kernel_utils |
| freertos-config | 空实现 | FreeRTOS 配置 | 未来需 rtos_utils |
| baremetal-init | 规划中 | 裸机启动代码生成 | 未来需 startup_utils |

### 5.4 工作流技能（workflow）

| 技能名 | 状态 | 功能 | 共享模块需求 |
|--------|------|------|-------------|
| project-init | 空实现 | 项目脚手架初始化 | 未来需 scaffold_utils |
| deploy-release | 空实现 | 部署发布流程 | 未来需 deploy_utils |
| ci-cd-config | 规划中 | CI/CD 配置生成 | 未来需 ci_utils |

---

## 六、技能开发流程

### 6.1 新增技能步骤

```
1. 确定技能分类（software/hardware/platform/workflow）
2. 创建 skill-name/ 目录
3. 编写 SKILL.md（定义触发条件、参数、输出格式）
4. 编写 scripts/{skill_name}.py（单文件实现）
5. 本地测试：python scripts/{skill_name}.py --help
6. 验证输出格式是否符合 SKILL.md 定义
```

### 6.2 技能测试标准

每个技能需验证：

1. **参数测试**：所有命令行参数正常工作
2. **环境探测**：`--detect` 能正确识别工具链
3. **错误处理**：缺少工具时返回正确失败分类
4. **JSON 输出**：`--json` 输出符合 SCHEMA
5. **产物验证**：构建产物能被正确扫描和识别

---

## 七、与 Total 项目的差异说明

| 维度 | Total 项目 | Plumb-Link（当前） |
|------|-----------|-------------------|
| **脚本结构** | 单文件（linux_builder.py） | 单文件（与 Total 一致） |
| **共享模块** | tool_config.py（已提取） | tool_config.py（预留空实现） |
| **agents 配置** | openai.yaml（大模型接口） | 暂未实现（规划中） |
| **SKILL.md** | 无（依赖 agents 配置） | 有（大模型直接读取） |
| **目录深度** | 扁平（scripts/ 直接放文件） | 扁平（与 Total 一致） |
| **产物扫描** | size >= 64 字节过滤 | size >= 64 字节过滤（与 Total 一致） |
| **错误分类** | 详细分类（project-config-error 等） | 详细分类（与 Total 一致） |

**核心差异：**
- Total 使用 `agents/openai.yaml` 定义大模型接口
- Plumb-Link 使用 `SKILL.md` 作为大模型入口
- 两者脚本层实现已对齐

---

## 八、待办事项

- [x] build-linux-app 技能实现（单文件模式）
- [ ] agents/openai.yaml 大模型接口配置
- [ ] 测试用例（testcases/ 目录）
- [ ] 共享模块提取（当同类技能 >= 3 个时）
- [ ] 硬件技能实现（gpio-config、i2c-scan、spi-debug）
- [ ] 平台技能实现（linux-build、freertos-config）
- [ ] 工作流技能实现（project-init、deploy-release）
- [ ] CI/CD 集成（自动化测试和部署）

---

## 九、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-06-16 | 初始版本，定义目录结构和实现规范 |
