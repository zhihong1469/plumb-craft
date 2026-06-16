#!/usr/bin/env python3
"""
PL002 - FreeRTOS 配置技能
"""

import sys
import os
from pathlib import Path
import json

# 添加公共库路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "common" / "src"))

from common.src.error_code import ErrorCode
from common.inc.data_struct import SkillResult, Evidence


class FreeRTOSConfigExecutor:
    """FreeRTOS 配置执行器"""
    
    def __init__(self):
        self.config_template = """/* FreeRTOS Configuration File */

#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

/* Clock Configuration */
#define configCPU_CLOCK_HZ                      {cpu_clock_hz}U
#define configTICK_RATE_HZ                      {tick_rate_hz}U

/* Heap Configuration */
#define configTOTAL_HEAP_SIZE                   {heap_size}U
#define configAPPLICATION_ALLOCATED_HEAP        {application_heap}

/* Task Configuration */
#define configMAX_PRIORITIES                    {max_priorities}U
#define configMAX_TASK_NAME_LEN                 {max_task_name_len}U
#define configUSE_PREEMPTION                    {use_preemption}U
#define configUSE_TIME_SLICING                  {use_time_slicing}U

/* Queue Configuration */
#define configQUEUE_REGISTRY_SIZE               {queue_registry_size}U

/* Timer Configuration */
#define configUSE_TIMERS                        {use_timers}U
#define configTIMER_TASK_PRIORITY               {timer_task_priority}U
#define configTIMER_QUEUE_LENGTH                {timer_queue_length}U

/* Hook Functions */
#define configUSE_IDLE_HOOK                     {use_idle_hook}U
#define configUSE_TICK_HOOK                     {use_tick_hook}U

/* Memory Management */
#define configSUPPORT_DYNAMIC_ALLOCATION        {support_dynamic}U
#define configSUPPORT_STATIC_ALLOCATION         {support_static}U

/* Miscellaneous */
#define INCLUDE_vTaskPrioritySet                {include_priority_set}U
#define INCLUDE_uxTaskPriorityGet               {include_priority_get}U
#define INCLUDE_vTaskDelete                     {include_task_delete}U
#define INCLUDE_vTaskSuspend                    {include_task_suspend}U
#define INCLUDE_xTaskGetSchedulerState          {include_scheduler_state}U

#endif /* FREERTOS_CONFIG_H */
"""
    
    def execute(self, output_path: str = "FreeRTOSConfig.h", **kwargs) -> SkillResult:
        """
        生成 FreeRTOS 配置文件
        
        Args:
            output_path: 输出文件路径
            **kwargs: 配置参数
        
        Returns:
            SkillResult: 执行结果
        """
        try:
            # 默认配置参数
            params = {
                "cpu_clock_hz": kwargs.get("cpu_clock_hz", 72000000),
                "tick_rate_hz": kwargs.get("tick_rate_hz", 1000),
                "heap_size": kwargs.get("heap_size", 10240),
                "application_heap": kwargs.get("application_heap", 0),
                "max_priorities": kwargs.get("max_priorities", 5),
                "max_task_name_len": kwargs.get("max_task_name_len", 16),
                "use_preemption": kwargs.get("use_preemption", 1),
                "use_time_slicing": kwargs.get("use_time_slicing", 1),
                "queue_registry_size": kwargs.get("queue_registry_size", 10),
                "use_timers": kwargs.get("use_timers", 1),
                "timer_task_priority": kwargs.get("timer_task_priority", 3),
                "timer_queue_length": kwargs.get("timer_queue_length", 10),
                "use_idle_hook": kwargs.get("use_idle_hook", 0),
                "use_tick_hook": kwargs.get("use_tick_hook", 0),
                "support_dynamic": kwargs.get("support_dynamic", 1),
                "support_static": kwargs.get("support_static", 0),
                "include_priority_set": kwargs.get("include_priority_set", 1),
                "include_priority_get": kwargs.get("include_priority_get", 1),
                "include_task_delete": kwargs.get("include_task_delete", 1),
                "include_task_suspend": kwargs.get("include_task_suspend", 1),
                "include_scheduler_state": kwargs.get("include_scheduler_state", 1),
            }
            
            # 生成配置文件
            config_content = self.config_template.format(**params)
            
            # 确保目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            with open(output_path, "w") as f:
                f.write(config_content)
            
            evidence = [
                Evidence(
                    type="file",
                    path=os.path.abspath(output_path),
                    title="FreeRTOSConfig.h"
                )
            ]
            
            return SkillResult.success(
                summary="FreeRTOS 配置完成",
                evidence=evidence,
                extra={"config_params": params}
            )
        
        except Exception as e:
            return SkillResult.failure(
                summary=f"FreeRTOS 配置失败: {str(e)}",
                failure_category="runtime_error",
                error_code=ErrorCode.RUNTIME_UNKNOWN_ERROR.value
            )


def main():
    """主函数"""
    output_path = "FreeRTOSConfig.h"
    params = {}
    
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    
    # 解析键值对参数（如 cpu_clock_hz=72000000）
    for arg in sys.argv[2:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            if value.isdigit():
                params[key] = int(value)
            else:
                params[key] = value
    
    executor = FreeRTOSConfigExecutor()
    result = executor.execute(output_path, **params)
    
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())