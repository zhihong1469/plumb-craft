---
name: build-linux-app
version: 1.0.0
description: 编译 Linux 应用程序，支持 x86_64 本地编译和 ARM64 交叉编译
keywords: ["编译", "build", "make", "cmake", "构建", "交叉编译", "arm64"]
platforms: ["linux", "windows", "macos"]
required_tools: ["gcc", "make"]
optional_tools: ["cmake", "ninja"]
output_format: structured
author: "Plumb-Link Team"
license: "MIT"
---

# 技能说明

## 触发条件
- 用户提到"编译"、"build"、"make"、"cmake"、"交叉编译"等关键词
- 当前目录存在 Makefile 或 CMakeLists.txt
- 检测到 C/C++ 源代码文件

## 执行步骤
1. 检测工具链（gcc, make, cmake）
2. 读取构建配置（Makefile 或 CMakeLists.txt）
3. 支持 CMakePresets.json 预设加载
4. 选择编译模式（本地编译/交叉编译）
5. 执行构建命令
6. 收集构建产物
7. 返回结构化结果

## 输出格式
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | ✅ | success/partial/failure |
| summary | string | ✅ | 执行摘要 |
| evidence | array | ✅ | 输出文件列表和命令信息 |
| failure_category | string | ❌ | 失败类型（仅失败时） |
| error_code | string | ❌ | 错误码（仅失败时） |

## 支持的命令行参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| --source | str | . | 源目录路径 |
| --build-dir | str | build | 构建目录路径 |
| --preset | str | None | CMake 预设名称 |
| --generator | str | None | CMake 生成器 |
| --build-type | str | Release | 构建类型 (Debug/Release/RelWithDebInfo) |
| --toolchain | str | None | 工具链文件路径 |
| --arch | str | None | 目标架构 (x86_64/arm64) |
| --target | str | all | 构建目标 |
| --parallel | int | 1 | 并行构建线程数 |
| --build-system | str | None | 构建系统（自动检测） |
| --detect | flag | False | 探测构建环境 |
| --list-presets | flag | False | 列出可用 CMake 预设 |
| --json | flag | False | 输出 JSON 格式结果 |

## 依赖工具
| 工具名称 | 用途 | 检测方法 |
|---------|------|---------|
| gcc | C 编译器 | gcc --version |
| g++ | C++ 编译器 | g++ --version |
| make | 构建工具 | make --version |
| cmake | 构建工具（可选） | cmake --version |
| ninja | 构建工具（可选） | ninja --version |
| aarch64-linux-gnu-gcc | ARM64 交叉编译器 | aarch64-linux-gnu-gcc --version |

## 交叉编译支持
- 架构：ARM64 (aarch64)
- 工具链前缀：aarch64-none-linux-gnu-, aarch64-linux-gnu-, aarch64-linux-musl-
- 环境变量：CROSS_COMPILE（优先使用）

## 失败分类
| 分类 | 说明 | 建议 |
|------|------|------|
| tool_missing | 缺少必需工具 | 安装对应工具，检查 PATH |
| project-config-error | 项目配置错误 | 检查 CMakeLists.txt 或 Makefile |
| compilation_error | 编译错误 | 检查源代码，查看详细错误信息 |
| artifact-missing | 未找到构建产物 | 检查构建配置和源代码 |
| config_missing | 配置缺失 | 提供必要的配置参数 |
| config_error | 配置无效 | 检查配置参数是否正确 |
| not_supported | 不支持的操作 | 检查目标平台和架构 |

## 安全注意事项
- 构建过程可能需要较长执行时间
- 建议在隔离环境中执行构建
- 注意磁盘空间是否充足
- 交叉编译需要额外的工具链支持

## 参考资料
- [GCC 文档](https://gcc.gnu.org/onlinedocs/)
- [Make 文档](https://www.gnu.org/software/make/manual/)
- [CMake 文档](https://cmake.org/documentation/)
- [CMakePresets 文档](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)
