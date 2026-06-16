# HW003 - SPI 调试技能

## 技能信息

| 项目 | 内容 |
|------|------|
| 技能ID | HW003 |
| 技能名称 | spi-debug |
| 触发关键词 | spi,debug,调试,设备列表 |
| 平台支持 | Linux/裸机 |
| 状态 | 待设计 |

## 触发条件

用户输入包含以下关键词时触发：
- "SPI 调试"
- "SPI 设备"
- "SPI 测试"

## 执行步骤

1. **参数解析**：解析 SPI 总线编号和片选
2. **权限检查**：检查是否有访问 SPI 设备的权限
3. **检查设备**：检查 SPI 设备文件是否存在
4. **执行测试**：使用 spidev_test 进行基本测试
5. **返回结果**：返回测试结果

## 输出格式

```json
{
    "status": "success",
    "summary": "SPI 测试完成",
    "evidence": [
        {
            "type": "output",
            "content": "SPI 设备 /dev/spidev0.0 测试通过",
            "title": "测试结果"
        }
    ],
    "spi_devices": ["/dev/spidev0.0", "/dev/spidev0.1"]
}
```

## 依赖工具

| 工具名称 | 用途 | 最低版本 | 检测方法 |
|---------|------|---------|---------|
| spidev_test | SPI 测试工具 | - | spidev_test --help |

## 安全注意事项

- SPI 设备需要正确配置设备树
- 确保 SPI 总线未被其他设备占用