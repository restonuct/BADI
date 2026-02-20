"""Request Router"""
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel

from badi.ai_backends import get_backend_for_task
from badi.memory import get_db, get_recent_interactions, get_vector_store
from badi.core.planner import create_plan
from badi.core.executor import execute_plan

logger = logging.getLogger(__name__)

class Request(BaseModel):
    text: str
    user_id: int
    intent: str = "unknown"
    metadata: Optional[Dict] = None

class Response(BaseModel):
    text: str
    success: bool = True
    data: Optional[Dict] = None
    error: Optional[str] = None

class RequestRouter:
    async def route(self, request: Request) -> Response:
        context = await self._get_context(request.user_id)
        intent = await self._classify_intent(request.text, context)
        
        if intent == "task":
            return await self._handle_task(request, context)
        else:
            return await self._handle_chat(request, context)
    
    async def _get_context(self, user_id: int) -> Dict[str, Any]:
        db = get_db()
        recent = get_recent_interactions(db, user_id, limit=5)
        return {"recent_interactions": [{"role": i.role, "content": i.content} for i in reversed(recent)]}
    
    async def _classify_intent(self, text: str, context: Dict) -> str:
        keywords = ["organize", "move", "scan", "find", "create", "delete", "search"]
        return "task" if any(kw in text.lower() for kw in keywords) else "chat"
    
    async def _handle_chat(self, request: Request, context: Dict) -> Response:
        messages = context.get("recent_interactions", []) + [{"role": "user", "content": request.text}]
        backend = get_backend_for_task("chat")
        response_text = backend.chat(messages, temperature=0.7, max_tokens=512)
        return Response(text=response_text, success=True)
    
    async def _handle_task(self, request: Request, context: Dict) -> Response:
        try:
            plan = await create_plan(request.text, context)
            result = await execute_plan(plan, require_confirmation=False)
            text = f"Task completed. {result.steps_completed} steps executed." if result.success else f"Task partially completed. {result.steps_failed} failed."
            return Response(text=text, success=result.success, data={"plan": plan.dict(), "result": result.dict()})
        except Exception as e:
            return Response(text=f"Task failed: {e}", success=False, error=str(e))

async def route_request(request: Request) -> Response:
    router = RequestRouter()
    return await router.route(request)
