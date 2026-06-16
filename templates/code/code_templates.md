# 代码输出模板

> 自动生成的代码模板

---

## C 代码模板

```c
/**
 * @file {filename}
 * @brief {description}
 * @author {author}
 * @date {date}
 * @version {version}
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * @brief 函数简短描述
 *
 * 详细描述（可选）
 *
 * @param param1 参数1描述
 * @param param2 参数2描述
 * @return 返回值描述
 */
int function_name(int param1, char *param2)
{
    // 参数校验
    if (param2 == NULL) {
        return -1;
    }

    // 实现逻辑
    int result = 0;

    // 返回结果
    return result;
}

/**
 * @brief 主函数
 *
 * @param argc 参数个数
 * @param argv 参数列表
 * @return 返回码
 */
int main(int argc, char *argv[])
{
    // 解析参数
    if (argc < 2) {
        printf("Usage: %s <arguments>\n", argv[0]);
        return 1;
    }

    // 执行逻辑
    int result = function_name(atoi(argv[1]), argv[2]);

    // 返回结果
    return result == 0 ? 0 : 1;
}
```

---

## Python 代码模板

```python
"""
{filename} - {description}

@author {author}
@date {date}
@version {version}
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional


def function_name(param1: int, param2: str) -> int:
    """
    函数简短描述

    详细描述（可选）

    Args:
        param1: 参数1描述
        param2: 参数2描述

    Returns:
        返回值描述
    """
    # 参数校验
    if not param2:
        return -1

    # 实现逻辑
    result = 0

    # 返回结果
    return result


def main():
    """主函数"""
    # 解析参数
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <arguments>")
        return 1

    # 执行逻辑
    result = function_name(int(sys.argv[1]), sys.argv[2])

    # 返回结果
    return 0 if result == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## Shell 脚本模板

```bash
#!/bin/bash
#
# {filename} - {description}
#
# @author {author}
# @date {date}
# @version {version}

set -e  # 遇到错误立即退出
set -u  # 使用未定义变量时报错
set -o pipefail  # 管道中任何命令失败都返回失败

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 参数检查
if [ $# -lt 1 ]; then
    log_error "Usage: $0 <arguments>"
    exit 1
fi

# 主逻辑
main() {
    log_info "开始执行..."

    # 实现逻辑

    log_info "执行完成"
    return 0
}

# 执行主函数
main "$@"
```

---

## Makefile 模板

```makefile
# Makefile for {project_name}
# @author {author}
# @date {date}

# 编译器
CC = gcc
CXX = g++
AR = ar
STRIP = strip

# 编译选项
CFLAGS = -Wall -Wextra -std=c11
CFLAGS += -O2 -pipe
CFLAGS += -g

# 链接选项
LDFLAGS = -Wl,-rpath,/usr/local/lib

# 源文件
SRCS = $(wildcard src/*.c)
OBJS = $(SRCS:.c=.o)

# 目标文件
TARGET = build/{project_name}

# 默认目标
all: $(TARGET)

# 编译目标
$(TARGET): $(OBJS)
	@mkdir -p build
	$(CC) $(OBJS) -o $@ $(LDFLAGS)

# 编译源文件
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# 清理
clean:
	rm -f $(OBJS) $(TARGET)

# 安装
install: $(TARGET)
	install -m 755 $(TARGET) /usr/local/bin/

# 卸载
uninstall:
	rm -f /usr/local/bin/{project_name}

# 帮助
help:
	@echo "Available targets:"
	@echo "  all      - Build the project (default)"
	@echo "  clean    - Remove build artifacts"
	@echo "  install  - Install the binary"
	@echo "  uninstall- Uninstall the binary"
	@echo "  help     - Show this help message"

.PHONY: all clean install uninstall help
```

---

## CMakeLists.txt 模板

```cmake
# CMakeLists.txt for {project_name}
# @author {author}
# @date {date}

cmake_minimum_required(VERSION 3.10)
project({project_name} C)

# 设置 C 标准
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# 编译选项
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O2 -pipe")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g")

# 输出目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# 源文件
file(GLOB_RECURSE SOURCES "src/*.c")

# 创建可执行文件
add_executable(${PROJECT_NAME} ${SOURCES})

# 链接库
target_link_libraries(${PROJECT_NAME} PRIVATE m pthread)

# 安装规则
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
)

# 打印配置信息
message(STATUS "Project: ${PROJECT_NAME}")
message(STATUS "C Compiler: ${CMAKE_C_COMPILER}")
message(STATUS "C Flags: ${CMAKE_C_FLAGS}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
```

---

## 输出说明

- 代码遵循对应语言的标准规范
- 添加了必要的注释和文档字符串
- 包含类型注解（Python）
- 包含错误处理
- 包含参数校验
- 遵循最佳实践

---

## 自定义字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| {filename} | 文件名 | main.c |
| {description} | 文件描述 | 主程序入口 |
| {author} | 作者名称 | Your Name |
| {date} | 日期 | 2026-06-15 |
| {version} | 版本号 | 1.0.0 |
| {project_name} | 项目名称 | myapp |