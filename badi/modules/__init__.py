"""
B.A.D.I. Module System

Auto-imports all available modules to ensure they register themselves.
"""

from badi.modules.base import (
    Module,
    ModuleCapability,
    ModuleParameter,
    MODULE_REGISTRY,
    register_module,
    get_module,
    list_modules,
    get_all_capabilities
)

# Import all modules to trigger auto-registration
try:
    from badi.modules.system_control import SystemControlModule
except ImportError as e:
    import logging
    logging.warning(f"Could not import system_control module: {e}")

try:
    from badi.modules.memory_tools import MemoryToolsModule
except ImportError as e:
    import logging
    logging.warning(f"Could not import memory_tools module: {e}")

# Add more module imports here as you create them
# try:
#     from badi.modules.web_search import WebSearchModule
# except ImportError:
#     pass

__all__ = [
    "Module",
    "ModuleCapability",
    "ModuleParameter",
    "MODULE_REGISTRY",
    "register_module",
    "get_module",
    "list_modules",
    "get_all_capabilities",
]
