"""
Base Module System for B.A.D.I.

Provides abstract base class and registry for all capability modules.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ModuleParameter(BaseModel):
    """Definition of a module parameter"""
    name: str
    type: str  # 'string', 'int', 'float', 'bool', 'list', 'dict'
    description: str
    required: bool = True
    default: Optional[Any] = None


class ModuleCapability(BaseModel):
    """Description of a module capability/function"""
    name: str
    description: str
    parameters: List[ModuleParameter] = Field(default_factory=list)
    returns: str = "Result dictionary"
    examples: List[str] = Field(default_factory=list)


class Module(ABC):
    """
    Abstract base class for all B.A.D.I. modules
    
    All capability modules should inherit from this class and
    implement the required methods.
    """
    
    # Module metadata (override in subclass)
    name: str = "base_module"
    description: str = "Base module"
    version: str = "1.0.0"
    author: str = "B.A.D.I. Contributors"
    
    # Permission settings
    requires_confirmation: bool = False
    is_read_only: bool = True
    max_scope: Optional[str] = None  # e.g., "downloads_folder"
    
    # Capabilities
    capabilities: List[ModuleCapability] = []
    
    def __init__(self):
        """Initialize module"""
        self.enabled = True
        self.logger = logging.getLogger(f"badi.modules.{self.name}")
    
    @abstractmethod
    async def run(self, capability: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a module capability
        
        Args:
            capability: Name of the capability to execute
            **kwargs: Parameters for the capability
            
        Returns:
            Dictionary with results
            {
                "success": bool,
                "result": Any,
                "error": Optional[str],
                "metadata": Optional[dict]
            }
        """
        pass
    
    def validate_parameters(self, capability: str, params: dict) -> tuple[bool, Optional[str]]:
        """
        Validate parameters for a capability
        
        Args:
            capability: Capability name
            params: Parameters to validate
            
        Returns:
            (is_valid, error_message)
        """
        # Find capability definition
        cap_def = None
        for cap in self.capabilities:
            if cap.name == capability:
                cap_def = cap
                break
        
        if not cap_def:
            return False, f"Unknown capability: {capability}"
        
        # Check required parameters
        for param in cap_def.parameters:
            if param.required and param.name not in params:
                if param.default is None:
                    return False, f"Missing required parameter: {param.name}"
                else:
                    params[param.name] = param.default
        
        return True, None
    
    def get_capabilities_description(self) -> str:
        """
        Get a formatted description of all capabilities
        
        Returns:
            Formatted string describing all capabilities
        """
        desc = f"Module: {self.name}\n"
        desc += f"Description: {self.description}\n\n"
        desc += "Capabilities:\n"
        
        for cap in self.capabilities:
            desc += f"  - {cap.name}: {cap.description}\n"
            if cap.parameters:
                desc += "    Parameters:\n"
                for param in cap.parameters:
                    req = "required" if param.required else "optional"
                    desc += f"      - {param.name} ({param.type}, {req}): {param.description}\n"
        
        return desc
    
    def get_capability_names(self) -> List[str]:
        """Get list of capability names"""
        return [cap.name for cap in self.capabilities]
    
    def to_dict(self) -> dict:
        """Convert module metadata to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "requires_confirmation": self.requires_confirmation,
            "is_read_only": self.is_read_only,
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "parameters": [
                        {
                            "name": p.name,
                            "type": p.type,
                            "description": p.description,
                            "required": p.required,
                            "default": p.default
                        }
                        for p in cap.parameters
                    ]
                }
                for cap in self.capabilities
            ]
        }


class ModuleRegistry:
    """
    Global registry for all modules
    
    Modules register themselves on import.
    """
    
    def __init__(self):
        self._modules: Dict[str, Module] = {}
        self.logger = logging.getLogger("badi.modules.registry")
    
    def register(self, module: Module):
        """
        Register a module
        
        Args:
            module: Module instance to register
        """
        if module.name in self._modules:
            self.logger.warning(f"Module '{module.name}' already registered, overwriting")
        
        self._modules[module.name] = module
        self.logger.info(f"Registered module: {module.name}")
    
    def unregister(self, name: str):
        """Unregister a module by name"""
        if name in self._modules:
            del self._modules[name]
            self.logger.info(f"Unregistered module: {name}")
    
    def get(self, name: str) -> Optional[Module]:
        """Get a module by name"""
        return self._modules.get(name)
    
    def get_all(self) -> Dict[str, Module]:
        """Get all registered modules"""
        return self._modules.copy()
    
    def get_enabled(self) -> Dict[str, Module]:
        """Get only enabled modules"""
        return {name: mod for name, mod in self._modules.items() if mod.enabled}
    
    def list_modules(self) -> List[str]:
        """Get list of all module names"""
        return list(self._modules.keys())
    
    def list_enabled_modules(self) -> List[str]:
        """Get list of enabled module names"""
        return [name for name, mod in self._modules.items() if mod.enabled]
    
    def get_capability(self, full_name: str) -> Optional[tuple[Module, str]]:
        """
        Get module and capability from full name
        
        Args:
            full_name: Format 'module_name.capability_name'
            
        Returns:
            (module, capability_name) or None
        """
        if "." not in full_name:
            return None
        
        module_name, capability_name = full_name.split(".", 1)
        module = self.get(module_name)
        
        if module and capability_name in module.get_capability_names():
            return module, capability_name
        
        return None
    
    def get_all_capabilities(self) -> List[Dict[str, Any]]:
        """
        Get list of all capabilities across all modules
        
        Returns:
            List of capability dictionaries with module info
        """
        capabilities = []
        
        for module_name, module in self.get_enabled().items():
            for cap in module.capabilities:
                capabilities.append({
                    "module": module_name,
                    "full_name": f"{module_name}.{cap.name}",
                    "name": cap.name,
                    "description": cap.description,
                    "parameters": [
                        {
                            "name": p.name,
                            "type": p.type,
                            "description": p.description,
                            "required": p.required
                        }
                        for p in cap.parameters
                    ],
                    "requires_confirmation": module.requires_confirmation,
                    "is_read_only": module.is_read_only
                })
        
        return capabilities


# Global module registry
MODULE_REGISTRY = ModuleRegistry()


def register_module(module: Module):
    """Register a module with the global registry"""
    MODULE_REGISTRY.register(module)


def get_module(name: str) -> Optional[Module]:
    """Get a module by name"""
    return MODULE_REGISTRY.get(name)


def list_modules() -> List[str]:
    """List all registered module names"""
    return MODULE_REGISTRY.list_modules()


def get_all_capabilities() -> List[Dict[str, Any]]:
    """Get all capabilities across all modules"""
    return MODULE_REGISTRY.get_all_capabilities()
