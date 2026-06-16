# PL001 - Linux 构建技能

## 技能信息

| 项目 | 内容 |
|------|------|
| 技能ID | PL001 |
| 技能名称 | linux-build |
| 触发关键词 | linux,build,构建,编译内核 |
| 平台支持 | Linux |
| 状态 | 待设计 |

## 触发条件

用户输入包含以下关键词时触发：
- "构建 Linux"
- "编译内核"
- "Linux build"

## 执行步骤

1. **参数解析**：解析内核配置、目标平台、编译选项
2. **依赖检查**：检查 gcc、make、bison、flex 等工具
3. **配置内核**：执行 make menuconfig 或加载配置文件
4. **执行编译**：执行 make 命令
5. **打包镜像**：生成 boot.img 或 zImage
6. **返回结果**：返回编译状态和输出文件路径

## 输出格式

```json
{
    "status": "success",
    "summary": "Linux 内核编译完成",
    "evidence": [
        {
            "type": "file",
            "path": "/path/to/zImage",
            "title": "内核镜像"
        },
        {
            "type": "file",
            "path": "/path/to/arch/arm/boot/dts/rk3562.dtb",
            "title": "设备树"
        }
    ],
    "output_files": ["/path/to/zImage", "/path/to/rk3562.dtb"]
}
```

## 依赖工具

| 工具名称 | 用途 | 最低版本 | 检测方法 |
|---------|------|---------|---------|
| gcc | 编译器 | 7.0+ | gcc --version |
| make | 构建工具 | 4.0+ | make --version |
| bison | 语法分析器 | 3.0+ | bison --version |
| flex | 词法分析器 | 2.6+ | flex --version |

## 安全注意事项

- 内核编译需要大量磁盘空间（建议 > 20GB）
- 编译时间较长，请耐心等待