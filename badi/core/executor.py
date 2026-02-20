"""Task Executor"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

from badi.core.planner import TaskPlan, PlanStep
from badi.modules.base import MODULE_REGISTRY

logger = logging.getLogger(__name__)

class ExecutionResult(BaseModel):
    success: bool
    steps_completed: int
    steps_failed: int
    results: List[Dict[str, Any]]
    errors: List[Dict[str, Any]]
    duration_seconds: float

class TaskExecutor:
    async def execute_plan(self, plan: TaskPlan, require_confirmation: bool = True) -> ExecutionResult:
        start = datetime.now()
        results, errors = [], []
        completed, failed = 0, 0
        
        for group in plan.parallel_groups:
            for step_id in group:
                step = next((s for s in plan.steps if s.id == step_id), None)
                if not step:
                    continue
                
                try:
                    module_name, capability = step.module.split(".", 1)
                    module = MODULE_REGISTRY.get(module_name)
                    if module:
                        result = await module.run(capability, **step.params)
                        result["step_id"] = step.id
                        results.append(result)
                        completed += 1 if result.get("success") else 0
                        failed += 0 if result.get("success") else 1
                except Exception as e:
                    errors.append({"step_id": step.id, "error": str(e)})
                    failed += 1
        
        return ExecutionResult(
            success=failed==0,
            steps_completed=completed,
            steps_failed=failed,
            results=results,
            errors=errors,
            duration_seconds=(datetime.now()-start).total_seconds()
        )

async def execute_plan(plan: TaskPlan, require_confirmation: bool = True) -> ExecutionResult:
    executor = TaskExecutor()
    return await executor.execute_plan(plan, require_confirmation)
