"""
AI Backend Selector and Router

Intelligently selects the appropriate AI backend based on
task type, complexity, and availability.
"""

from typing import Optional, Literal, Protocol
import logging

from badi.config import get_config
from badi.ai_backends.local_llama_cpp import get_local_backend, is_available as local_available
from badi.ai_backends.cloud_backend import get_cloud_backend, is_provider_available

logger = logging.getLogger(__name__)


class AIBackend(Protocol):
    """Protocol for AI backend interface"""
    
    def chat(self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 512, **kwargs) -> str:
        """Generate chat completion"""
        ...
    
    @property
    def model_name(self) -> str:
        """Get model identifier"""
        ...
    
    @property
    def is_available(self) -> bool:
        """Check if backend is available"""
        ...


class BackendSelector:
    """
    Intelligent backend selection based on task requirements
    
    Handles fallback logic and automatic selection between
    local and cloud backends.
    """
    
    def __init__(self):
        self.config = get_config()
        self._backends_cache = {}
    
    def get_backend(
        self,
        task_type: Literal["chat", "planner", "summarizer"] = "chat",
        prefer_local: bool = True,
        online: bool = True
    ) -> AIBackend:
        """
        Get the appropriate backend for a task
        
        Args:
            task_type: Type of task ('chat', 'planner', 'summarizer')
            prefer_local: Prefer local backend when available
            online: Whether network is available
            
        Returns:
            AIBackend instance
            
        Raises:
            RuntimeError: If no backend is available
        """
        # Determine preferred backend from config
        if task_type == "chat":
            preferred = self.config.chat_backend
        elif task_type == "planner":
            preferred = self.config.planner_backend
        elif task_type == "summarizer":
            preferred = self.config.summarizer_backend
        else:
            preferred = "local"
        
        # Apply mode and availability constraints
        mode = self.config.mode
        
        # Local-only mode or offline
        if mode == "local" or not online:
            if local_available():
                return self._get_local()
            else:
                raise RuntimeError(
                    "Local mode selected but no local model available. "
                    "Set BADI_LOCAL_MODEL_PATH to a valid GGUF model."
                )
        
        # Cloud-only mode
        if mode == "cloud":
            if preferred in ["openai", "anthropic", "gemini"]:
                return self._get_cloud(preferred)
            else:
                # Fallback to first available cloud provider
                for provider in ["openai", "anthropic", "gemini"]:
                    if is_provider_available(provider):
                        logger.info(f"Falling back to {provider} for cloud mode")
                        return self._get_cloud(provider)
                raise RuntimeError(
                    "Cloud mode selected but no cloud API keys configured. "
                    "Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY."
                )
        
        # Hybrid mode - try preferred, fall back intelligently
        if preferred == "local" and local_available():
            return self._get_local()
        
        elif preferred in ["openai", "anthropic", "gemini"]:
            if is_provider_available(preferred):
                return self._get_cloud(preferred)
            else:
                logger.warning(f"{preferred} not available, trying fallback")
        
        # Fallback logic for hybrid mode
        if prefer_local and local_available():
            return self._get_local()
        
        # Try cloud providers
        for provider in ["openai", "anthropic", "gemini"]:
            if is_provider_available(provider):
                logger.info(f"Using {provider} backend")
                return self._get_cloud(provider)
        
        # Last resort: try local even if not preferred
        if local_available():
            logger.info("No cloud providers available, using local backend")
            return self._get_local()
        
        raise RuntimeError(
            "No AI backend available. Please configure either:\n"
            "1. Local: Download a GGUF model and set BADI_LOCAL_MODEL_PATH\n"
            "2. Cloud: Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY"
        )
    
    def _get_local(self) -> AIBackend:
        """Get local backend with caching"""
        if "local" not in self._backends_cache:
            self._backends_cache["local"] = get_local_backend()
        return self._backends_cache["local"]
    
    def _get_cloud(self, provider: str) -> AIBackend:
        """Get cloud backend with caching"""
        if provider not in self._backends_cache:
            self._backends_cache[provider] = get_cloud_backend(provider)
        return self._backends_cache[provider]
    
    def list_available_backends(self) -> dict:
        """List all available backends"""
        available = {
            "local": local_available(),
            "openai": is_provider_available("openai"),
            "anthropic": is_provider_available("anthropic"),
            "gemini": is_provider_available("gemini"),
        }
        return available


# Global selector instance
_selector: Optional[BackendSelector] = None


def get_selector() -> BackendSelector:
    """Get or create the global backend selector"""
    global _selector
    if _selector is None:
        _selector = BackendSelector()
    return _selector


def get_backend_for_task(
    task_type: Literal["chat", "planner", "summarizer"] = "chat",
    **kwargs
) -> AIBackend:
    """
    Convenience function to get backend for a task
    
    Args:
        task_type: Type of task
        **kwargs: Additional arguments for get_backend
        
    Returns:
        AIBackend instance
    """
    selector = get_selector()
    return selector.get_backend(task_type, **kwargs)
