# 最小单元分析规则

> **版本**：v1.0  
> **日期**：2026-06-17  
> **参考依据**：[00_道-法-器三维架构：技能开发标准原则.md](../../guide/00_道法层技能开发标准层原则.md)（四大元原则）

---

## 一、最小单元定义

### 1.1 什么是最小单元

**最小单元技能**是指：
- 只实现一个明确的功能
- 不可继续拆分
- 职责边界清晰
- 可独立使用和复用

### 1.2 最小单元特征

| 特征 | 说明 | 示例 |
|------|------|------|
| **单一功能** | 只做一件事 | GPIO配置 |
| **明确输入** | 输入定义清晰 | GPIO引脚号 |
| **明确输出** | 输出定义清晰 | 配置状态 |
| **独立可用** | 可单独使用 | 可不依赖其他技能 |
| **可复用** | 可在多处使用 | 任何需要GPIO的项目 |

---

## 二、拆分原则

### 2.1 必须拆分的场景

| 场景 | 拆分原因 | 示例 |
|------|---------|------|
| **多步骤流程** | 违反单一职责 | "编译并烧录" → 拆分 |
| **多个接口** | 涉及多个接口 | "I2C和SPI配置" → 拆分 |
| **多个平台** | 涉及多个平台 | "Linux和RTOS" → 拆分 |
| **配置+执行** | 配置和执行分离 | "配置并运行" → 拆分 |

### 2.2 可保留的场景

| 场景 | 保留原因 | 示例 |
|------|---------|------|
| **单一操作** | 已是最小单元 | "GPIO配置" |
| **紧密关联** | 步骤不可分割 | "make编译" |
| **原子操作** | 不可再拆分 | "I2C扫描" |

---

## 三、分析流程

### 3.1 分析步骤

```
步骤 1：理解用户需求
    │
    ▼
步骤 2：提取功能关键词
    │
    ▼
步骤 3：判断功能数量
    │
    ▼
步骤 4：如果是多功能，拆分
    │
    ▼
步骤 5：验证拆分结果
```

### 3.2 判断树

```
技能需求
    │
    ├─ 是否只包含一个功能？
    │   │
    │   ├─ 是 → 最小单元
    │   │
    │   └─ 否 → 进入拆分判断
    │
    ├─ 功能是否紧密关联？（不可分割）
    │   │
    │   ├─ 是 → 最小单元
    │   │
    │   └─ 否 → 需要拆分
    │
    └─ 功能是否可以独立使用？
        │
        ├─ 是 → 可保留
        │
        └─ 否 → 需要拆分
```

---

## 四、拆分示例

### 4.1 拆分示例

#### 示例1：NFS 网络挂载开发板

**原始需求**：NFS 网络挂载开发板

**分析**：
- 功能1：NFS 挂载
- 功能2：网络配置
- 功能3：开发板检测

**拆分方案**：
```
1. nfs-mount（软件技能）
   - 功能：挂载 NFS 文件系统
   - 分类：software
   - 路径：skills/software/nfs-mount/

2. network-config（软件技能）
   - 功能：配置网络连接
   - 分类：software
   - 路径：skills/software/network-config/

3. board-detect（平台技能）
   - 功能：检测开发板
   - 分类：platform
   - 路径：skills/platform/board-detect/
```

#### 示例2：编译并烧录固件

**原始需求**：编译并烧录固件

**分析**：
- 功能1：编译固件
- 功能2：烧录固件

**拆分方案**：
```
1. firmware-build（平台技能）
   - 功能：编译固件
   - 分类：platform
   - 路径：skills/platform/firmware-build/

2. firmware-flash（平台技能）
   - 功能：烧录固件
   - 分类：platform
   - 路径：skills/platform/firmware-flash/
```

### 4.2 保留示例

#### 示例3：GPIO 配置

**原始需求**：GPIO 引脚配置

**分析**：
- 功能：配置 GPIO 引脚
- 判断：已是最小单元

**保留方案**：
```
gpio-config（硬件技能）
- 功能：配置 GPIO 引脚
- 分类：hardware
- 路径：skills/hardware/gpio-config/
```

#### 示例4：I2C 设备扫描

**原始需求**：I2C 总线设备扫描

**分析**：
- 功能：扫描 I2C 设备
- 判断：已是最小单元

**保留方案**：
```
i2c-scan（硬件技能）
- 功能：扫描 I2C 总线设备
- 分类：hardware
- 路径：skills/hardware/i2c-scan/
```

---

## 五、分析输出

### 5.1 输出格式

```json
{
  "skill_name": "技能名称",
  "is_minimal_unit": true/false,
  "analysis": {
    "functions": ["功能1", "功能2"],
    "function_count": 2,
    "need_split": true/false
  },
  "if_split": {
    "split_skills": [
      {
        "name": "技能1",
        "category": "software",
        "path": "skills/software/skill1/",
        "function": "功能1"
      }
    ]
  },
  "if_minimal": {
    "name": "技能名",
    "category": "hardware",
    "path": "skills/hardware/skill-name/"
  }
}
```

### 5.2 输出示例

#### 最小单元输出

```json
{
  "skill_name": "gpio-config",
  "is_minimal_unit": true,
  "analysis": {
    "functions": ["配置GPIO引脚"],
    "function_count": 1,
    "need_split": false
  },
  "if_minimal": {
    "name": "gpio-config",
    "category": "hardware",
    "path": "skills/hardware/gpio-config/"
  }
}
```

#### 拆分输出

```json
{
  "skill_name": "NFS网络挂载",
  "is_minimal_unit": false,
  "analysis": {
    "functions": ["NFS挂载", "网络配置", "开发板检测"],
    "function_count": 3,
    "need_split": true
  },
  "if_split": {
    "split_skills": [
      {
        "name": "nfs-mount",
        "category": "software",
        "path": "skills/software/nfs-mount/",
        "function": "NFS挂载"
      },
      {
        "name": "network-config",
        "category": "software",
        "path": "skills/software/network-config/",
        "function": "网络配置"
      },
      {
        "name": "board-detect",
        "category": "platform",
        "path": "skills/platform/board-detect/",
        "function": "开发板检测"
      }
    ]
  }
}
```
