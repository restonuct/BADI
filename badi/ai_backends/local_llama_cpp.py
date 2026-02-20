"""
Local LLM backend using llama.cpp

Provides offline inference using GGUF quantized models.
"""

from typing import List, Dict, Optional, Any
import logging
from pathlib import Path

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    logging.warning("llama-cpp-python not installed. Local LLM backend unavailable.")

from badi.config import get_config

logger = logging.getLogger(__name__)


class LocalLlamaCppBackend:
    """
    Local LLM backend using llama.cpp
    
    Supports GGUF models for efficient CPU/GPU inference.
    """
    
    def __init__(self, model_path: Optional[Path] = None):
        """
        Initialize the local LLM backend
        
        Args:
            model_path: Path to GGUF model file
        """
        if not LLAMA_CPP_AVAILABLE:
            raise RuntimeError("llama-cpp-python is not installed. Run: pip install llama-cpp-python")
        
        config = get_config()
        
        if model_path is None:
            model_path = config.local_model_path
        
        if not model_path or not Path(model_path).exists():
            raise FileNotFoundError(
                f"Local model not found at: {model_path}\n"
                "Please download a GGUF model from HuggingFace and set BADI_LOCAL_MODEL_PATH"
            )
        
        logger.info(f"Loading local model from: {model_path}")
        
        # Initialize llama.cpp model
        self.model = Llama(
            model_path=str(model_path),
            n_ctx=config.local_context_size,
            n_threads=config.local_threads,
            n_gpu_layers=config.local_gpu_layers,
            verbose=config.log_level == "DEBUG"
        )
        
        logger.info("Local model loaded successfully")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 512,
        **kwargs
    ) -> str:
        """
        Generate a chat completion
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            Generated response text
        """
        try:
            # Create chat completion
            response = self.model.create_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Extract response content
            if response and "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            else:
                logger.error("Invalid response format from local model")
                return "Error: Could not generate response"
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error: {str(e)}"
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 512,
        stop: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        """
        Generate text completion from a prompt
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stop: Stop sequences
            **kwargs: Additional parameters
            
        Returns:
            Generated text
        """
        try:
            response = self.model(
                prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop or [],
                **kwargs
            )
            
            if response and "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["text"]
            else:
                logger.error("Invalid response format from local model")
                return "Error: Could not generate response"
                
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return f"Error: {str(e)}"
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        try:
            return self.model.embed(text)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []
    
    @property
    def model_name(self) -> str:
        """Get model name"""
        return "local-llama-cpp"
    
    @property
    def is_available(self) -> bool:
        """Check if backend is available"""
        return self.model is not None


# Global backend instance
_backend: Optional[LocalLlamaCppBackend] = None


def get_local_backend() -> LocalLlamaCppBackend:
    """Get or create the local backend instance"""
    global _backend
    if _backend is None:
        _backend = LocalLlamaCppBackend()
    return _backend


def is_available() -> bool:
    """Check if local backend is available"""
    return LLAMA_CPP_AVAILABLE and get_config().local_model_path is not None
