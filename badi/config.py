"""
B.A.D.I. Configuration Module

Loads and validates configuration from environment variables and .env file.
"""

from pathlib import Path
from typing import Literal, Optional, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BADIConfig(BaseSettings):
    """Main configuration class for B.A.D.I."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="BADI_"
    )
    
    # Operation Mode
    mode: Literal["local", "cloud", "hybrid"] = Field(
        default="hybrid",
        description="Operation mode: local, cloud, or hybrid"
    )
    
    # Database Paths
    db_path: Path = Field(
        default=Path("./data/badi.db"),
        description="Path to SQLite database"
    )
    vector_dir: Path = Field(
        default=Path("./data/chroma"),
        description="Directory for ChromaDB vector store"
    )
    
    # Local LLM Configuration
    local_model_path: Optional[Path] = Field(
        default=None,
        description="Path to local GGUF model file"
    )
    local_context_size: int = Field(
        default=4096,
        description="Context window size for local model"
    )
    local_threads: int = Field(
        default=4,
        description="Number of CPU threads for local inference"
    )
    local_gpu_layers: int = Field(
        default=0,
        description="Number of layers to offload to GPU (0 = CPU only)"
    )
    
    # vLLM Configuration
    vllm_enabled: bool = Field(
        default=False,
        description="Whether vLLM server is available"
    )
    vllm_url: str = Field(
        default="http://localhost:8000/v1",
        description="vLLM server URL"
    )
    vllm_model: str = Field(
        default="Qwen/Qwen2.5-1.5B-Instruct",
        description="Model name for vLLM"
    )
    
    # Cloud API Keys
    openai_api_key: Optional[str] = Field(
        default=None,
        env="OPENAI_API_KEY",
        description="OpenAI API key"
    )
    anthropic_api_key: Optional[str] = Field(
        default=None,
        env="ANTHROPIC_API_KEY",
        description="Anthropic API key"
    )
    gemini_api_key: Optional[str] = Field(
        default=None,
        env="GEMINI_API_KEY",
        description="Google Gemini API key"
    )
    
    # Backend Selection
    chat_backend: Literal["local", "vllm", "openai", "anthropic", "gemini"] = Field(
        default="local",
        description="Backend for chat interactions"
    )
    planner_backend: Literal["local", "vllm", "openai", "anthropic", "gemini"] = Field(
        default="local",
        description="Backend for task planning"
    )
    summarizer_backend: Literal["local", "vllm", "openai", "anthropic", "gemini"] = Field(
        default="local",
        description="Backend for summarization"
    )
    
    # Module Configuration
    enabled_modules: List[str] = Field(
        default=["system_control", "memory_tools", "web_search"],
        description="List of enabled module names"
    )
    
    # Permission Settings
    require_confirmation: bool = Field(
        default=True,
        description="Require user confirmation for actions"
    )
    auto_approve_read_only: bool = Field(
        default=True,
        description="Auto-approve read-only operations"
    )
    
    # Voice Settings
    voice_enabled: bool = Field(
        default=False,
        description="Enable voice interaction"
    )
    whisper_model: Literal["tiny", "base", "small", "medium", "large"] = Field(
        default="base",
        description="Whisper model size"
    )
    wake_word: str = Field(
        default="hey badi",
        description="Wake word for voice activation"
    )
    
    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging level"
    )
    log_file: Optional[Path] = Field(
        default=Path("./data/badi.log"),
        description="Path to log file"
    )
    
    # Web Search
    search_api_key: Optional[str] = Field(
        default=None,
        description="API key for web search provider"
    )
    search_provider: Literal["serpapi", "duckduckgo"] = Field(
        default="duckduckgo",
        description="Web search provider"
    )
    
    # Advanced Settings
    max_plan_steps: int = Field(
        default=10,
        description="Maximum number of steps in a plan"
    )
    execution_timeout: int = Field(
        default=300,
        description="Execution timeout in seconds"
    )
    vector_search_top_k: int = Field(
        default=5,
        description="Number of results for vector search"
    )
    
    @field_validator("db_path", "vector_dir", "log_file", mode="before")
    @classmethod
    def ensure_path(cls, v):
        """Convert string paths to Path objects"""
        if v is None:
            return v
        return Path(v) if not isinstance(v, Path) else v
    
    @field_validator("enabled_modules", mode="before")
    @classmethod
    def parse_modules(cls, v):
        """Parse comma-separated module list"""
        if isinstance(v, str):
            return [m.strip() for m in v.split(",") if m.strip()]
        return v
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        # Create data directory
        if self.db_path:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create vector store directory
        if self.vector_dir:
            self.vector_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log directory
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create models directory if using local model
        if self.local_model_path and not self.local_model_path.exists():
            self.local_model_path.parent.mkdir(parents=True, exist_ok=True)
    
    def validate_backend_config(self) -> List[str]:
        """Validate that required API keys are present for selected backends"""
        errors = []
        
        backends_to_check = {
            self.chat_backend,
            self.planner_backend,
            self.summarizer_backend
        }
        
        for backend in backends_to_check:
            if backend == "openai" and not self.openai_api_key:
                errors.append("OpenAI backend selected but OPENAI_API_KEY not set")
            elif backend == "anthropic" and not self.anthropic_api_key:
                errors.append("Anthropic backend selected but ANTHROPIC_API_KEY not set")
            elif backend == "gemini" and not self.gemini_api_key:
                errors.append("Gemini backend selected but GEMINI_API_KEY not set")
            elif backend == "local" and not self.local_model_path:
                errors.append("Local backend selected but BADI_LOCAL_MODEL_PATH not set")
        
        return errors


# Global configuration instance
_config: Optional[BADIConfig] = None


def get_config() -> BADIConfig:
    """Get or create the global configuration instance"""
    global _config
    if _config is None:
        _config = BADIConfig()
        _config.ensure_directories()
    return _config


def reload_config() -> BADIConfig:
    """Reload configuration from environment"""
    global _config
    _config = BADIConfig()
    _config.ensure_directories()
    return _config
