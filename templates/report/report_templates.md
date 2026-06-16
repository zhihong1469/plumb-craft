# 报告输出模板

> 各类报告的标准输出格式

---

## 代码审查报告模板

```markdown
# 代码审查报告

**项目**: {project_name}
**版本**: {version}
**审查日期**: {date}
**审查人**: {reviewer}

## 审查摘要

| 指标 | 数值 |
|------|------|
| 总文件数 | {total_files} |
| 总代码行数 | {total_lines} |
| 发现问题数 | {issues_count} |
| 严重问题 | {critical_count} |
| 一般问题 | {major_count} |
| 轻微问题 | {minor_count} |

## 问题列表

### 严重问题

1. **内存泄漏** ({file}:{line})
   - **描述**: 未释放分配的内存
   - **建议**: 添加 free() 调用
   - **代码**: `char *buffer = malloc(1024);`

### 一般问题

1. **未使用的变量** ({file}:{line})
   - **描述**: 变量声明但未使用
   - **建议**: 删除或使用该变量
   - **代码**: `int temp = 0;`

### 轻微问题

1. **缺少注释** ({file}:{line})
   - **描述**: 复杂逻辑缺少注释说明
   - **建议**: 添加注释说明

## 审查结论

**总体评价**: {overall_rating}
**建议**: {recommendations}

## 下一步行动

- [ ] 修复严重问题
- [ ] 修复一般问题
- [ ] 改进轻微问题
- [ ] 重新审查
```

---

## 测试报告模板

```markdown
# 测试报告

**项目**: {project_name}
**版本**: {version}
**测试日期**: {date}
**测试环境**: {environment}

## 测试摘要

| 指标 | 数值 |
|------|------|
| 总测试用例 | {total_tests} |
| 通过测试 | {passed_tests} |
| 失败测试 | {failed_tests} |
| 跳过测试 | {skipped_tests} |
| 通过率 | {pass_rate}% |
| 执行时间 | {duration}s |

## 测试详情

### 单元测试

| 测试用例 | 状态 | 执行时间 | 备注 |
|---------|------|---------|------|
| test_function_1 | ✅ 通过 | 0.5s | - |
| test_function_2 | ❌ 失败 | 0.3s | 断言失败 |
| test_function_3 | ⏭️ 跳过 | 0.0s | 依赖缺失 |

### 集成测试

| 测试用例 | 状态 | 执行时间 | 备注 |
|---------|------|---------|------|
| test_integration_1 | ✅ 通过 | 2.1s | - |
| test_integration_2 | ✅ 通过 | 1.8s | - |

## 失败详情

### test_function_2

**错误信息**: `AssertionError: expected 5, got 3`

**堆栈跟踪**:
```
File "tests/test_main.py", line 42, in test_function_2
    assert result == 5
```

**建议**: 检查函数实现或测试用例

## 测试结论

**总体评价**: {overall_rating}
**建议**: {recommendations}

## 下一步行动

- [ ] 修复失败测试
- [ ] 补充缺失测试
- [ ] 提高测试覆盖率
- [ ] 重新测试
```

---

## 性能分析报告模板

```markdown
# 性能分析报告

**项目**: {project_name}
**版本**: {version}
**分析日期**: {date}
**分析工具**: {tool}

## 性能摘要

| 指标 | 数值 | 目标 | 状态 |
|------|------|------|------|
| 启动时间 | {startup_time}s | {target_startup}s | {status} |
| 内存占用 | {memory_usage}MB | {target_memory}MB | {status} |
| CPU 使用率 | {cpu_usage}% | {target_cpu}% | {status} |
| 响应时间 | {response_time}ms | {target_response}ms | {status} |

## 性能详情

### 启动性能

| 阶段 | 耗时 | 占比 |
|------|------|------|
| 初始化 | {init_time}s | {init_percent}% |
| 加载配置 | {config_time}s | {config_percent}% |
| 连接数据库 | {db_time}s | {db_percent}% |
| 其他 | {other_time}s | {other_percent}% |

### 内存使用

| 模块 | 内存占用 | 占比 |
|------|---------|------|
| 核心模块 | {core_memory}MB | {core_percent}% |
| 数据缓存 | {cache_memory}MB | {cache_percent}% |
| 其他 | {other_memory}MB | {other_percent}% |

### CPU 使用

| 函数 | CPU 时间 | 调用次数 | 平均时间 |
|------|---------|---------|---------|
| function_1 | {cpu_time_1}s | {calls_1} | {avg_time_1}s |
| function_2 | {cpu_time_2}s | {calls_2} | {avg_time_2}s |

## 性能瓶颈

1. **瓶颈1**: {bottleneck_1}
   - **影响**: {impact_1}
   - **建议**: {suggestion_1}

2. **瓶颈2**: {bottleneck_2}
   - **影响**: {impact_2}
   - **建议**: {suggestion_2}

## 优化建议

### 短期优化
- [ ] 优化 {optimization_1}
- [ ] 优化 {optimization_2}

### 长期优化
- [ ] 重构 {refactoring_1}
- [ ] 重构 {refactoring_2}

## 性能结论

**总体评价**: {overall_rating}
**建议**: {recommendations}
```

---

## 安全审计报告模板

```markdown
# 安全审计报告

**项目**: {project_name}
**版本**: {version}
**审计日期**: {date}
**审计工具**: {tool}

## 安全摘要

| 指标 | 数值 |
|------|------|
| 总检查项 | {total_checks} |
| 高危漏洞 | {high_count} |
| 中危漏洞 | {medium_count} |
| 低危漏洞 | {low_count} |
| 信息项 | {info_count} |

## 漏洞详情

### 高危漏洞

1. **SQL 注入** ({file}:{line})
   - **CVE**: {cve_id}
   - **描述**: 用户输入未经过滤直接拼接到 SQL 查询中
   - **影响**: 可能导致数据泄露或篡改
   - **修复建议**: 使用参数化查询
   - **代码**: `query = "SELECT * FROM users WHERE id = " + user_input`

### 中危漏洞

1. **XSS 攻击** ({file}:{line})
   - **描述**: 用户输入未经过滤直接输出到页面
   - **影响**: 可能导致跨站脚本攻击
   - **修复建议**: 对输出进行 HTML 转义

### 低危漏洞

1. **信息泄露** ({file}:{line})
   - **描述**: 错误信息包含敏感信息
   - **影响**: 可能泄露系统信息
   - **修复建议**: 自定义错误页面

## 安全建议

### 立即修复
- [ ] 修复高危漏洞
- [ ] 修复中危漏洞

### 计划修复
- [ ] 修复低危漏洞
- [ ] 改进安全实践

## 安全结论

**总体评价**: {overall_rating}
**建议**: {recommendations}

## 下一步行动

- [ ] 修复已发现漏洞
- [ ] 进行安全测试
- [ ] 建立安全监控
- [ ] 定期安全审计
```

---

## 输出字段说明

### 状态值
| 状态 | 说明 |
|------|------|
| ✅ 通过 | 测试通过 |
| ❌ 失败 | 测试失败 |
| ⏭️ 跳过 | 测试跳过 |

### 严重级别
| 级别 | 说明 |
|------|------|
| 严重 | 必须立即修复 |
| 一般 | 应该尽快修复 |
| 轻微 | 可以延后修复 |

### 风险级别
| 级别 | 说明 |
|------|------|
| 高危 | 严重安全风险 |
| 中危 | 中等安全风险 |
| 低危 | 轻微安全风险 |

---

## 使用示例

```python
import markdown
from datetime import datetime

def generate_test_report(project_name: str, test_results: dict) -> str:
    """生成测试报告"""
    template = """
# 测试报告

**项目**: {project_name}
**测试日期**: {date}

## 测试摘要

| 指标 | 数值 |
|------|------|
| 总测试用例 | {total_tests} |
| 通过测试 | {passed_tests} |
| 失败测试 | {failed_tests} |
| 通过率 | {pass_rate}% |
"""

    return template.format(
        project_name=project_name,
        date=datetime.now().strftime("%Y-%m-%d"),
        **test_results
    )
```

---

## 输出格式要求

- 使用 Markdown 格式
- 日期使用 YYYY-MM-DD 格式
- 百分比使用 0-100 范围
- 时间使用秒或毫秒单位
- 内存使用 MB 单位
- 代码使用代码块格式