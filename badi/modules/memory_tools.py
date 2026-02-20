"""
Memory Tools Module

Provides capabilities for storing and retrieving user preferences and memories.
"""

from typing import Dict, Any
from badi.modules.base import Module, ModuleCapability, ModuleParameter, register_module
from badi.memory import get_db, save_preference, get_preference


class MemoryToolsModule(Module):
    """Module for managing user memory and preferences"""
    
    name = "memory_tools"
    description = "Store and retrieve user preferences and memories"
    version = "1.0.0"
    is_read_only = False
    requires_confirmation = False
    
    capabilities = [
        ModuleCapability(
            name="remember_preference",
            description="Remember a user preference",
            parameters=[
                ModuleParameter(
                    name="key",
                    type="string",
                    description="Preference key/name",
                    required=True
                ),
                ModuleParameter(
                    name="value",
                    type="string",
                    description="Preference value",
                    required=True
                ),
                ModuleParameter(
                    name="user_id",
                    type="int",
                    description="User ID",
                    required=True
                )
            ]
        ),
        ModuleCapability(
            name="get_preference",
            description="Retrieve a user preference",
            parameters=[
                ModuleParameter(
                    name="key",
                    type="string",
                    description="Preference key/name",
                    required=True
                ),
                ModuleParameter(
                    name="user_id",
                    type="int",
                    description="User ID",
                    required=True
                )
            ]
        ),
        ModuleCapability(
            name="log_message",
            description="Log a message or note",
            parameters=[
                ModuleParameter(
                    name="message",
                    type="string",
                    description="Message to log",
                    required=True
                )
            ]
        )
    ]
    
    async def run(self, capability: str, **kwargs) -> Dict[str, Any]:
        """Execute capability"""
        valid, error = self.validate_parameters(capability, kwargs)
        if not valid:
            return {"success": False, "error": error}
        
        try:
            if capability == "remember_preference":
                return await self._remember_preference(**kwargs)
            elif capability == "get_preference":
                return await self._get_preference(**kwargs)
            elif capability == "log_message":
                return await self._log_message(**kwargs)
            else:
                return {"success": False, "error": f"Unknown capability: {capability}"}
        except Exception as e:
            self.logger.error(f"Error in {capability}: {e}")
            return {"success": False, "error": str(e)}
    
    async def _remember_preference(self, key: str, value: str, user_id: int) -> Dict[str, Any]:
        """Save a preference"""
        db = get_db()
        save_preference(db, user_id, key, value)
        
        return {
            "success": True,
            "result": {
                "key": key,
                "value": value,
                "message": f"Preference '{key}' saved"
            }
        }
    
    async def _get_preference(self, key: str, user_id: int) -> Dict[str, Any]:
        """Retrieve a preference"""
        db = get_db()
        value = get_preference(db, user_id, key)
        
        if value is None:
            return {
                "success": False,
                "error": f"Preference '{key}' not found"
            }
        
        return {
            "success": True,
            "result": {
                "key": key,
                "value": value
            }
        }
    
    async def _log_message(self, message: str) -> Dict[str, Any]:
        """Log a message"""
        self.logger.info(f"Message: {message}")
        
        return {
            "success": True,
            "result": {
                "message": message,
                "logged": True
            }
        }


# Auto-register
register_module(MemoryToolsModule())
