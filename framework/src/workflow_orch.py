"""
技能编排引擎

实现多技能串行/并行调用规则
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Callable
import json
import concurrent.futures
from dataclasses import dataclass

from common.src.path_utils import normalize_path, join_paths
from common.src.cmd_utils import run_command
from common.inc.data_struct import SkillResult


@dataclass
class SkillStep:
    """技能步骤"""
    skill_name: str
    skill_path: str
    args: Optional[Dict] = None
    depends_on: Optional[List[str]] = None
    parallel: bool = False


class WorkflowOrchestrator:
    """工作流编排器"""

    def __init__(self):
        """初始化编排器"""
        self.steps: List[SkillStep] = []
        self.results: Dict[str, SkillResult] = {}

    def add_step(
        self,
        skill_name: str,
        skill_path: str,
        args: Optional[Dict] = None,
        depends_on: Optional[List[str]] = None,
        parallel: bool = False
    ):
        """
        添加技能步骤

        Args:
            skill_name: 技能名称
            skill_path: 技能路径
            args: 技能参数
            depends_on: 依赖的技能名称列表
            parallel: 是否并行执行
        """
        step = SkillStep(
            skill_name=skill_name,
            skill_path=skill_path,
            args=args or {},
            depends_on=depends_on or [],
            parallel=parallel
        )
        self.steps.append(step)

    def execute_step(self, step: SkillStep) -> SkillResult:
        """
        执行单个技能步骤

        Args:
            step: 技能步骤

        Returns:
            执行结果
        """
        try:
            # 构建命令
            script_path = join_paths(step.skill_path, "scripts", "src", "main.py")

            if not Path(script_path).exists():
                return SkillResult.failure(
                    summary=f"技能脚本不存在: {script_path}",
                    failure_category="file_not_found"
                )

            # 执行技能
            result = run_command(f'python "{script_path}"', timeout=300)

            if result.success():
                # 解析输出
                try:
                    output_data = json.loads(result.stdout)
                    return SkillResult(**output_data)
                except json.JSONDecodeError:
                    return SkillResult.success(
                        summary="技能执行成功",
                        evidence=[]
                    )
            else:
                return SkillResult.failure(
                    summary=f"技能执行失败: {result.stderr}",
                    failure_category="execution_error"
                )

        except Exception as e:
            return SkillResult.failure(
                summary=f"技能执行异常: {str(e)}",
                failure_category="runtime_error"
            )

    def check_dependencies(self, step: SkillStep) -> bool:
        """
        检查依赖是否满足

        Args:
            step: 技能步骤

        Returns:
            依赖是否满足
        """
        for dep_name in step.depends_on:
            if dep_name not in self.results:
                return False

            dep_result = self.results[dep_name]
            if dep_result.status != "success":
                return False

        return True

    def execute_sequential(self) -> Dict[str, SkillResult]:
        """
        串行执行所有步骤

        Returns:
            所有步骤的执行结果
        """
        print("开始串行执行工作流")

        for step in self.steps:
            print(f"执行步骤: {step.skill_name}")

            # 检查依赖
            if not self.check_dependencies(step):
                print(f"  ❌ 依赖不满足，跳过: {step.skill_name}")
                self.results[step.skill_name] = SkillResult.failure(
                    summary=f"依赖不满足: {step.depends_on}",
                    failure_category="dependency_error"
                )
                continue

            # 执行步骤
            result = self.execute_step(step)
            self.results[step.skill_name] = result

            status = "✅ 成功" if result.status == "success" else "❌ 失败"
            print(f"  {status}: {result.summary}")

        return self.results

    def execute_parallel(self) -> Dict[str, SkillResult]:
        """
        并行执行可并行的步骤

        Returns:
            所有步骤的执行结果
        """
        print("开始并行执行工作流")

        # 分离可并行和不可并行的步骤
        parallel_steps = [step for step in self.steps if step.parallel]
        sequential_steps = [step for step in self.steps if not step.parallel]

        # 先执行串行步骤
        for step in sequential_steps:
            print(f"执行串行步骤: {step.skill_name}")

            if not self.check_dependencies(step):
                print(f"  ❌ 依赖不满足，跳过: {step.skill_name}")
                self.results[step.skill_name] = SkillResult.failure(
                    summary=f"依赖不满足: {step.depends_on}",
                    failure_category="dependency_error"
                )
                continue

            result = self.execute_step(step)
            self.results[step.skill_name] = result

            status = "✅ 成功" if result.status == "success" else "❌ 失败"
            print(f"  {status}: {result.summary}")

        # 并行执行可并行步骤
        if parallel_steps:
            print(f"并行执行 {len(parallel_steps)} 个步骤")

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self.execute_step, step): step
                    for step in parallel_steps
                }

                for future in concurrent.futures.as_completed(futures):
                    step = futures[future]
                    try:
                        result = future.result()
                        self.results[step.skill_name] = result

                        status = "✅ 成功" if result.status == "success" else "❌ 失败"
                        print(f"  {status}: {step.skill_name} - {result.summary}")

                    except Exception as e:
                        self.results[step.skill_name] = SkillResult.failure(
                            summary=f"执行异常: {str(e)}",
                            failure_category="runtime_error"
                        )
                        print(f"  ❌ 异常: {step.skill_name} - {str(e)}")

        return self.results

    def execute(self, parallel: bool = False) -> Dict[str, SkillResult]:
        """
        执行工作流

        Args:
            parallel: 是否并行执行

        Returns:
            所有步骤的执行结果
        """
        if parallel:
            return self.execute_parallel()
        else:
            return self.execute_sequential()

    def get_summary(self) -> Dict[str, any]:
        """
        获取执行摘要

        Returns:
            执行摘要
        """
        total_steps = len(self.steps)
        successful_steps = sum(
            1 for result in self.results.values()
            if result.status == "success"
        )

        return {
            "total_steps": total_steps,
            "successful_steps": successful_steps,
            "failed_steps": total_steps - successful_steps,
            "success_rate": successful_steps / total_steps if total_steps > 0 else 0,
            "results": {
                name: result.to_dict()
                for name, result in self.results.items()
            }
        }


def main():
    """主函数"""
    # 示例：创建一个简单的工作流
    orchestrator = WorkflowOrchestrator()

    # 添加步骤
    orchestrator.add_step(
        skill_name="build",
        skill_path="skills/build-linux-app",
        parallel=False
    )

    orchestrator.add_step(
        skill_name="test",
        skill_path="skills/test-app",
        depends_on=["build"],
        parallel=False
    )

    # 执行工作流
    results = orchestrator.execute(parallel=False)

    # 输出摘要
    summary = orchestrator.get_summary()
    print("\n工作流执行摘要:")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    return 0 if summary["failed_steps"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())