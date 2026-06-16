# HW001 - GPIO 配置技能

## 技能信息

| 项目 | 内容 |
|------|------|
| 技能ID | HW001 |
| 技能名称 | gpio-config |
| 触发关键词 | gpio,引脚,配置,导出,设置 |
| 平台支持 | Linux/裸机 |
| 状态 | 待设计 |

## 触发条件

用户输入包含以下关键词时触发：
- "配置 GPIO"
- "设置引脚"
- "导出 GPIO"
- "GPIO 方向"

## 执行步骤

1. **参数解析**：解析 GPIO 编号、方向（输入/输出）、初始值
2. **权限检查**：检查是否有操作 GPIO 的权限
3. **导出 GPIO**：写入 `/sys/class/gpio/export`
4. **设置方向**：写入 `/sys/class/gpio/gpioX/direction`
5. **设置值**：如为输出模式，写入初始值
6. **返回结果**：返回操作状态和 GPIO 路径

## 输出格式

```json
{
    "status": "success",
    "summary": "GPIO 配置成功",
    "evidence": [
        {
            "type": "output",
            "content": "GPIO 50 已配置为输出模式，初始值: 1",
            "title": "配置结果"
        }
    ],
    "gpio_path": "/sys/class/gpio/gpio50"
}
```

## 依赖工具

| 工具名称 | 用途 | 最低版本 | 检测方法 |
|---------|------|---------|---------|
| /sys/class/gpio | sysfs GPIO 接口 | - | 检查目录是否存在 |

## 安全注意事项

- GPIO 操作需要 root 权限
- 确保 GPIO 编号在设备支持范围内
- 避免配置系统关键引脚