"""Task Planner - Uses LLM to decompose tasks"""
import json
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from badi.ai_backends import get_backend_for_task
from badi.modules.base import MODULE_REGISTRY

logger = logging.getLogger(__name__)

class PlanStep(BaseModel):
    id: int
    module: str
    description: str
    params: Dict[str, Any] = Field(default_factory=dict)
    depends_on: List[int] = Field(default_factory=list)

class TaskPlan(BaseModel):
    goal: str
    steps: List[PlanStep]
    parallel_groups: List[List[int]] = Field(default_factory=list)

class TaskPlanner:
    def __init__(self):
        self.logger = logging.getLogger("badi.core.planner")
    
    async def create_plan(self, goal: str, context: Optional[Dict] = None) -> TaskPlan:
        capabilities = MODULE_REGISTRY.get_all_capabilities()
        cap_desc = "\n".join([f"- {cap['full_name']}: {cap['description']}" for cap in capabilities])
        
        prompt = f"""Create an execution plan for: {goal}

Available: {cap_desc}

Return JSON: {{"goal": "...", "steps": [{{"id": 1, "module": "module.capability", "description": "...", "params": {{}}, "depends_on": []}}], "parallel_groups": [[1]]}}"""
        
        backend = get_backend_for_task("planner")
        response = backend.chat([{"role": "user", "content": prompt}], temperature=0.3, max_tokens=1024)
        
        try:
            data = json.loads(response.strip().replace("```json", "").replace("```", ""))
            return TaskPlan(**data)
        except:
            return TaskPlan(goal=goal, steps=[PlanStep(id=1, module="memory_tools.log_message", description="Plan failed", params={"message": "Planning failed"})])

async def create_plan(goal: str, context: Optional[Dict] = None) -> TaskPlan:
    planner = TaskPlanner()
    return await planner.create_plan(goal, context)
