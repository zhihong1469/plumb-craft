# L2 通用规则层

> L2 通用规则层：编码规范、脚本标准、依赖要求
> 全局常驻，索引之后，基础约束前置，所有任务默认生效

---

## 一、编码规范

### 1.1 Python 编码规范

#### 文件结构
```
scripts/
├── inc/           # 常量、配置类（不包含业务逻辑）
│   ├── config.py  # 配置定义
│   └── const.py   # 常量定义
└── src/           # 业务逻辑
    └── main.py    # 主入口
```

#### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件/目录 | 小写+连字符 | `cmd_utils.py` |
| 类名 | PascalCase | `SkillExecutor` |
| 函数/方法 | snake_case | `run_command()` |
| 变量 | snake_case | `tool_path` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY` |
| 私有成员 | _underscore_prefix | `_internal_method()` |

#### 代码风格

| 规则 | 说明 |
|------|------|
| 缩进 | 4 个空格，禁止使用 Tab |
| 行长度 | 最大 120 字符 |
| 空行 | 函数/类之间空两行 |
| 导入 | 按标准库→第三方库→本地库顺序，每组空一行 |
| 类型提示 | 所有函数参数和返回值必须有类型提示 |

#### 示例代码

```python
"""
模块说明文档
"""

import os
import sys
from typing import Optional, List, Dict

def run_command(cmd: List[str], cwd: Optional[str] = None) -> Dict[str, str]:
    """
    执行命令
    
    Args:
        cmd: 命令参数列表
        cwd: 工作目录
    
    Returns:
        包含 stdout、stderr、returncode 的字典
    """
    # 实现逻辑
    pass
```

---

## 二、脚本标准

### 2.1 脚本结构规范

每个技能脚本必须遵循以下结构：

```python
#!/usr/bin/env python3
"""
技能名称 - 技能描述
"""

import sys
import os
from pathlib import Path

# 添加公共库路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "common" / "src"))

# 导入公共模块
from common.src.platform_detect import get_platform_info
from common.src.cmd_utils import run_command
from common.src.path_utils import normalize_path
from common.src.error_code import ErrorCode
from common.inc.data_struct import SkillResult, Evidence

# 导入本地配置
from scripts.inc.skill_config import DEFAULT_CONFIG


class SkillExecutor:
    """技能执行器"""
    
    def __init__(self, config=None):
        self.config = config or DEFAULT_CONFIG
        self.platform_info = get_platform_info()
    
    def execute(self) -> SkillResult:
        """执行技能主逻辑"""
        try:
            # 1. 参数校验
            # 2. 执行操作
            # 3. 返回结果
            return SkillResult.success(
                summary="执行成功",
                evidence=[]
            )
        except Exception as e:
            return SkillResult.failure(
                summary=f"执行失败: {str(e)}",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )


def main():
    """主函数"""
    executor = SkillExecutor()
    result = executor.execute()
    
    # 输出结构化结果
    import json
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
```

### 2.2 输出格式标准

所有技能必须返回结构化输出，格式如下：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | ✅ | success / partial / failure |
| summary | string | ✅ | 执行摘要（人类可读） |
| evidence | array | ✅ | 证据列表，包含输出文件路径等 |
| failure_category | string | ❌ | 失败类型（仅 failure 时） |
| error_code | string | ❌ | 错误码（仅 failure 时） |
| duration | float | ❌ | 执行耗时（秒） |

#### Evidence 结构

| 字段 | 类型 | 说明 |
|------|------|------|
| type | string | 证据类型：file / output / log |
| path | string | 文件路径（如适用） |
| content | string | 内容摘要 |
| title | string | 证据标题 |

### 2.3 错误处理标准

#### 错误分类

| 分类 | 说明 | 示例 |
|------|------|------|
| validation_error | 参数验证失败 | 参数为空、格式错误 |
| dependency_error | 依赖缺失 | 工具未找到、版本不兼容 |
| runtime_error | 运行时错误 | 命令执行失败、文件不存在 |
| permission_error | 权限错误 | 无权限访问文件 |
| platform_error | 平台不支持 | 技能不支持当前平台 |

#### 错误码体系

| 错误码 | 含义 |
|--------|------|
| E0001 | 参数验证失败 |
| E0002 | 依赖工具未找到 |
| E0003 | 依赖工具版本不兼容 |
| E0004 | 命令执行失败 |
| E0005 | 文件不存在 |
| E0006 | 权限不足 |
| E0007 | 平台不支持 |
| E9999 | 未知错误 |

---

## 三、依赖要求

### 3.1 工具依赖声明

每个技能必须在 `SKILL.md` 中声明依赖工具：

```markdown
## 依赖工具
| 工具名称 | 用途 | 最低版本 | 检测方法 |
|---------|------|---------|---------|
| cmake | 构建工具 | 3.16.0 | cmake --version |
| gcc | 编译器 | 7.0.0 | gcc --version |
```

### 3.2 Python 依赖管理

项目根目录必须有 `pyproject.toml`：

```toml
[project]
name = "plumb-link"
version = "1.0.0"
dependencies = [
    "pydantic>=2.0.0",
    "pyyaml>=6.0",
    "pyserial>=3.5",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### 3.3 工具探测优先级

工具探测必须遵循以下优先级：

1. **环境变量**：`${TOOL_NAME}_PATH`
2. **工程目录**：`.tools/${tool_name}/`
3. **系统 PATH**：`shutil.which()`
4. **通用路径**：预定义的工具安装目录
5. **默认路径**：回退到已知默认位置

---

## 四、跨平台兼容要求

### 4.1 路径处理

| 平台 | 路径分隔符 | 特殊处理 |
|------|-----------|---------|
| Windows | `\` | 使用 `pathlib` 自动处理 |
| Linux/macOS | `/` | 使用 `pathlib` 自动处理 |

### 4.2 命令执行

- 使用 `subprocess.run()` 执行命令
- Windows 命令需要 `.exe` 后缀
- Linux/macOS 需要可执行权限

### 4.3 平台检测

```python
from common.src.platform_detect import is_windows, is_linux, is_macos

if is_windows():
    tool_path = "tool.exe"
elif is_linux():
    tool_path = "tool"
```

---

## 五、安全规范

### 5.1 高危操作清单

| 操作类型 | 示例命令 | 安全要求 |
|----------|---------|---------|
| 文件删除 | `rm -rf`, `del` | 需要人工确认 |
| 格式化 | `mkfs`, `format` | 需要人工确认 |
| 网络访问 | `curl`, `wget` | 限制目标地址 |
| 系统修改 | `chmod`, `chown` | 限制范围 |
| 硬件操作 | 烧录、寄存器修改 | 需要人工确认 |

### 5.2 输入验证

- 所有用户输入必须进行验证
- 禁止路径遍历攻击（`../`）
- 禁止命令注入攻击
- 限制输入长度

---

## 六、文档规范

### 6.1 SKILL.md 必须包含

| 章节 | 说明 |
|------|------|
| 技能信息 | 技能ID、名称、分类、作者等 |
| 触发条件 | 技能何时触发 |
| 执行步骤 | 具体执行流程 |
| 输出格式 | 返回数据结构 |
| 依赖工具 | 需要的外部工具 |
| 安全注意事项 | 高危操作说明 |

### 6.2 代码注释

- 模块必须有文档字符串
- 函数必须有文档字符串（包含 Args、Returns）
- 复杂逻辑必须有注释说明
- 注释必须是中文

---

## 七、测试规范

### 7.1 测试用例要求

每个技能必须包含以下测试：

| 测试类型 | 说明 |
|----------|------|
| 正常流程 | 验证技能正常执行 |
| 失败流程 | 验证错误处理 |
| 边界条件 | 验证极端输入 |

### 7.2 测试文件结构

```
testcases/
├── test_skill.py      # 单元测试
├── test_integration.py # 集成测试
└── test_boundary.py   # 边界测试
```

### 7.3 测试覆盖率

- 单元测试覆盖率 ≥ 80%
- 关键路径必须有测试覆盖

---

## 八、版本规范

### 8.1 版本号格式

```
MAJOR.MINOR.PATCH
```

| 部分 | 说明 |
|------|------|
| MAJOR | 不兼容的API变更 |
| MINOR | 向后兼容的功能新增 |
| PATCH | 向后兼容的问题修复 |

### 8.2 版本管理

- 使用 `pyproject.toml` 管理版本
- 每次发布更新版本号
- 保持向后兼容

---

## 九、技能目录结构规范

### 9.1 标准目录结构

```
skills/{category}/{skill_name}/
├── SKILL.md           # ✅ 必需：技能契约文件
├── scripts/           # ✅ 必需：脚本实现
│   ├── inc/           # ✅ 必需：常量、配置
│   │   └── skill_config.py
│   └── src/           # ✅ 必需：源码实现
│       └── main.py    # ✅ 必需：主入口
├── references/        # ⭕ 推荐：技能专属参考资料
├── testcases/         # ⭕ 推荐：测试用例
│   └── test_skill.py
└── README.md          # ⭕ 推荐：技能说明文档
```

### 9.2 目录命名规则

| 目录 | 命名规则 | 示例 |
|------|---------|------|
| 技能目录 | 小写+连字符 | `build-linux-app` |
| 分类目录 | 小写 | `software`, `hardware` |
| 文件 | 小写+连字符 | `skill_config.py` |

---

## 十、技能生命周期管理

### 10.1 技能状态流转

```
待设计 → 开发中 → 测试中 → 已验证 → 发布 → 维护
   ↓         ↓        ↓        ↓       ↓      ↓
 D005     编码    V001/V002   V003    D003   O004
```

### 10.2 各阶段要求

| 阶段 | 要求 | 输出物 |
|------|------|--------|
| 待设计 | 定义技能需求和接口契约 | SKILL.md（初稿） |
| 开发中 | 实现技能逻辑 | scripts/src/main.py |
| 测试中 | 编写并执行测试用例 | testcases/ |
| 已验证 | 通过所有测试和合规检查 | 测试报告 |
| 发布 | 打包并发布技能 | 技能包 |
| 维护 | 修复bug和更新功能 | 更新日志 |

---

## 十一、配置文件规范

### 11.1 配置文件格式

| 格式 | 适用场景 | 示例 |
|------|---------|------|
| JSON | 简单配置、机器可读 | `config.json` |
| YAML | 复杂配置、人类可读 | `config.yaml` |
| INI | 简单键值对 | `config.ini` |

### 11.2 配置加载优先级

```
命令行参数 > 本地项目配置 > 全局用户配置 > 系统环境变量 > 默认配置
```

### 11.3 敏感配置处理

- 敏感信息（密码、密钥）不得硬编码
- 使用环境变量或密钥管理服务
- 配置文件不应包含敏感信息

---

## 十二、日志规范

### 12.1 日志级别

| 级别 | 说明 | 使用场景 |
|------|------|---------|
| DEBUG | 调试信息 | 开发调试 |
| INFO | 一般信息 | 正常执行流程 |
| WARNING | 警告信息 | 潜在问题 |
| ERROR | 错误信息 | 可恢复的错误 |
| CRITICAL | 严重错误 | 不可恢复的错误 |

### 12.2 日志格式

```
[时间戳] [级别] [模块] [消息]
```

示例：
```
[2024-01-15 10:30:00] [INFO] [build-linux-app] 编译开始
[2024-01-15 10:35:00] [SUCCESS] [build-linux-app] 编译完成
```