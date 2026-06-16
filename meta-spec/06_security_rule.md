# 安全红线规则（L6 安全护栏层）

> 本文件定义技能执行过程中的安全约束和风险管控机制
> 全局常驻（首尾双放置）+ 每步工具调用前校验，三重保险

---

## 一、安全护栏架构

### 1.1 三重安全校验机制

```
用户请求 → L6-1 前置检查 → L6-2 调用拦截 → L6-3 执行审计
              │                │               │
              ▼                ▼               ▼
           规则匹配       参数校验        结果记录
              │                │               │
              ▼                ▼               ▼
          允许/阻止      允许/阻止      日志归档
```

### 1.2 安全层级

| 层级 | 名称 | 职责 | 触发时机 | 注意力位置 |
|------|------|------|---------|-----------|
| **L6-1** | 前置检查 | 规则匹配、权限验证 | 请求进入时 | System Prompt开头 |
| **L6-2** | 调用拦截 | 参数校验、高危操作检测 | 工具调用前 | 每次调用前置 |
| **L6-3** | 执行审计 | 结果记录、异常追踪 | 执行完成后 | 结尾兜底 |

---

## 二、高危操作清单

### 2.1 操作风险分级

| 操作类型 | 风险等级 | 处理策略 | 示例命令 |
|----------|---------|---------|---------|
| **硬件烧录** | 高 | 必须人工确认 | flash、burn、写入固件 |
| **系统格式化** | 高 | 必须人工确认 | mkfs、format、dd if=* of=/dev/* |
| **文件删除** | 高 | 必须人工确认 | rm -rf、del /s |
| **网络请求** | 中 | 白名单控制 | curl、wget、git clone |
| **文件覆盖** | 中 | 备份机制 | cp -f、覆盖写入 |
| **脚本执行** | 低 | 参数校验 | python、bash、powershell |

### 2.2 高危命令黑名单

```yaml
blocked_commands:
  # 文件系统操作
  - rm -rf /
  - rm -rf /*
  - dd if=* of=/dev/*
  - mkfs.* /dev/*
  - fdisk /dev/*
  - format C:
  - format D:
  
  # 系统修改
  - chmod -R 777 /
  - chown -R root:root /
  
  # 网络操作（未授权）
  - curl http://
  - wget http://
  
  # 进程操作
  - kill -9 -1
  - shutdown -h now
  - reboot -f
```

### 2.3 受限路径清单

| 路径类型 | 路径模式 | 限制说明 |
|---------|---------|---------|
| 系统目录 | /etc/*, /usr/*, /bin/* | 禁止修改 |
| 设备文件 | /dev/* | 禁止格式化、写入 |
| 用户目录 | ~/ | 允许正常操作 |
| 临时目录 | /tmp/* | 允许操作 |

---

## 三、安全配置

### 3.1 网络白名单

```yaml
allowed_domains:
  - github.com
  - gitlab.com
  - gitee.com
  - *.kernel.org
  - *.rockchip.com
  - *.nxp.com
```

### 3.2 文件操作限制

```yaml
file_operations:
  max_file_size: 104857600  # 100MB
  allowed_extensions:
    - .txt
    - .md
    - .py
    - .c
    - .h
    - .cpp
    - .hpp
    - .json
    - .yaml
    - .yml
    - .xml
    - .ini
    - .sh
    - .bat
    - .makefile
    - .cmake
    - .config
    - .dtb
    - .img
    - .bin
    - .elf
    - .so
    - .a
  blocked_paths:
    - /etc/
    - /usr/bin/
    - /bin/
    - /sbin/
    - /boot/
    - /dev/
```

### 3.3 权限配置

| 角色 | 权限级别 | 可执行操作 |
|------|---------|-----------|
| **管理员** | 完整权限 | 所有操作（含高危） |
| **开发者** | 受限权限 | 开发相关操作，需确认高危 |
| **测试员** | 测试权限 | 仅测试操作 |
| **访客** | 只读权限 | 仅查看操作 |

---

## 四、人工确认机制

### 4.1 确认流程

```
检测到高危操作 → 暂停执行 → 生成确认请求 → 等待用户确认(30秒超时) → 继续/终止
```

### 4.2 确认请求格式

```json
{
  "confirm_required": true,
  "operation_type": "hardware_flash",
  "risk_level": "high",
  "description": "即将烧录固件到设备",
  "target_device": "/dev/sdb",
  "firmware_path": "/path/to/firmware.img",
  "timestamp": "2026-06-15T10:00:00Z",
  "timeout_seconds": 30,
  "requires_confirmation": true
}
```

### 4.3 确认响应格式

```json
{
  "confirmed": true,
  "user_id": "user123",
  "timestamp": "2026-06-15T10:00:15Z",
  "reason": "确认烧录"
}
```

---

## 五、审计日志

### 5.1 日志格式

```json
{
  "timestamp": "2026-06-15T10:00:00Z",
  "skill_name": "flash-imx6ull",
  "skill_id": "SW002",
  "operation_type": "hardware_flash",
  "status": "completed",
  "user_confirmation": true,
  "user_id": "user123",
  "execution_time": 120.5,
  "output": "Flash completed successfully",
  "evidence": [
    {
      "type": "file",
      "path": "/path/to/output.log",
      "title": "烧录日志"
    }
  ],
  "risk_level": "high"
}
```

### 5.2 日志存储

| 存储位置 | 说明 | 保留期限 |
|---------|------|---------|
| 本地日志 | ./logs/ | 30天 |
| 审计数据库 | 集中存储 | 永久 |

---

## 六、安全错误码

| 错误码 | 描述 | 处理建议 |
|--------|------|---------|
| SEC_BLOCKED_OPERATION | 操作被安全规则阻止 | 检查操作是否合法，如需执行请联系管理员 |
| SEC_REQUIRES_CONFIRMATION | 需要人工确认 | 等待用户确认或取消操作 |
| SEC_INVALID_PERMISSION | 权限不足 | 联系管理员获取更高权限 |
| SEC_NETWORK_BLOCKED | 网络请求被阻止 | 检查目标地址是否在白名单中 |
| SEC_FILE_SIZE_EXCEEDED | 文件大小超限 | 压缩或分批处理 |
| SEC_PATH_BLOCKED | 路径被阻止 | 使用允许的路径 |
| SEC_INPUT_VALIDATION_FAILED | 输入验证失败 | 检查输入参数格式 |
| SEC_INJECTION_DETECTED | 检测到注入攻击 | 检查输入内容，避免恶意注入 |

---

## 七、安全检查 API

### 7.1 前置检查接口

```python
def security_pre_check(skill_name: str, skill_id: str, params: dict) -> SecurityCheckResult:
    """
    安全前置检查
    
    Args:
        skill_name: 技能名称
        skill_id: 技能ID
        params: 技能参数
    
    Returns:
        SecurityCheckResult: 检查结果
    """
    pass
```

### 7.2 操作拦截接口

```python
def security_intercept(command: str, command_type: str) -> SecurityCheckResult:
    """
    命令拦截检查
    
    Args:
        command: 待执行命令
        command_type: 命令类型
    
    Returns:
        SecurityCheckResult: 拦截结果
    """
    pass
```

### 7.3 日志记录接口

```python
def security_log(
    skill_name: str, 
    skill_id: str, 
    operation_type: str, 
    status: str, 
    details: dict = None
) -> None:
    """
    记录安全审计日志
    
    Args:
        skill_name: 技能名称
        skill_id: 技能ID
        operation_type: 操作类型
        status: 执行状态
        details: 详细信息
    """
    pass
```

---

## 八、安全配置文件

### 8.1 配置文件路径

```
~/.plumb-link/security/config.yaml   # 用户级别
/etc/plumb-link/security/config.yaml # 系统级别
./security/config.yaml               # 项目级别
```

### 8.2 配置优先级

```
命令行参数 > 项目级别 > 用户级别 > 系统级别 > 默认配置
```

---

## 九、安全最佳实践

### 9.1 输入验证

| 验证类型 | 说明 | 示例 |
|---------|------|------|
| 类型检查 | 检查参数类型是否正确 | int、str、bool |
| 范围检查 | 检查数值是否在允许范围 | 端口号 1-65535 |
| 格式检查 | 检查字符串格式 | 路径、URL、IP地址 |
| 长度检查 | 检查字符串长度 | 最大长度限制 |
| 注入检查 | 检查是否包含恶意代码 | SQL注入、命令注入 |

### 9.2 输出验证

| 验证项 | 说明 |
|-------|------|
| 输出格式 | 必须是结构化JSON |
| 敏感信息 | 禁止包含密码、密钥 |
| 输出大小 | 限制最大输出长度 |

### 9.3 权限最小化

- 以最小权限运行
- 避免使用 sudo
- 限制文件访问权限

---

> **说明**：本文件为安全护栏层的架构定义，具体实现将根据实际业务场景自动生成和填充。