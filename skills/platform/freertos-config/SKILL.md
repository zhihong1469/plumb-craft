# PL002 - FreeRTOS 配置技能

## 技能信息

| 项目 | 内容 |
|------|------|
| 技能ID | PL002 |
| 技能名称 | freertos-config |
| 触发关键词 | freertos,config,配置,RTOS |
| 平台支持 | RTOS |
| 状态 | 待设计 |

## 触发条件

用户输入包含以下关键词时触发：
- "配置 FreeRTOS"
- "FreeRTOS 初始化"
- "RTOS 配置"

## 执行步骤

1. **参数解析**：解析目标 MCU、时钟频率、任务配置
2. **模板加载**：加载 FreeRTOS 配置模板
3. **参数替换**：替换配置参数（任务栈大小、优先级等）
4. **生成文件**：生成 FreeRTOSConfig.h
5. **返回结果**：返回配置文件路径

## 输出格式

```json
{
    "status": "success",
    "summary": "FreeRTOS 配置完成",
    "evidence": [
        {
            "type": "file",
            "path": "/path/to/FreeRTOSConfig.h",
            "title": "配置文件"
        }
    ],
    "config_params": {
        "configCPU_CLOCK_HZ": 72000000,
        "configTOTAL_HEAP_SIZE": 10240,
        "configMAX_TASK_NAME_LEN": 16
    }
}
```

## 依赖工具

| 工具名称 | 用途 | 最低版本 | 检测方法 |
|---------|------|---------|---------|
| FreeRTOS | RTOS 源码 | 10.0+ | 检查源码目录 |

## 安全注意事项

- 确保配置参数与硬件匹配
- 堆大小配置需合理，避免内存溢出