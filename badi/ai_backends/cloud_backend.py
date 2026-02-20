"""
Cloud AI backends for OpenAI, Anthropic, and Google Gemini

Provides unified interface for cloud API calls.
"""

from typing import List, Dict, Optional
import logging

from badi.config import get_config

logger = logging.getLogger(__name__)

# Try importing cloud SDKs
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.debug("OpenAI SDK not available")

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.debug("Anthropic SDK not available")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.debug("Google Gemini SDK not available")


class CloudBackend:
    """Unified interface for cloud AI providers"""
    
    def __init__(
        self,
        provider: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize cloud backend
        
        Args:
            provider: Provider name ('openai', 'anthropic', 'gemini')
            model: Model name (uses default if not specified)
            api_key: API key (uses config if not specified)
        """
        self.provider = provider.lower()
        config = get_config()
        
        # Set up provider-specific defaults
        if self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise RuntimeError("OpenAI SDK not installed. Run: pip install openai")
            self.api_key = api_key or config.openai_api_key
            self.model = model or "gpt-4-turbo-preview"
            self.client = OpenAI(api_key=self.api_key)
            
        elif self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise RuntimeError("Anthropic SDK not installed. Run: pip install anthropic")
            self.api_key = api_key or config.anthropic_api_key
            self.model = model or "claude-3-5-sonnet-20241022"
            self.client = Anthropic(api_key=self.api_key)
            
        elif self.provider == "gemini":
            if not GEMINI_AVAILABLE:
                raise RuntimeError("Google SDK not installed. Run: pip install google-generativeai")
            self.api_key = api_key or config.gemini_api_key
            self.model = model or "gemini-pro"
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
            
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        if not self.api_key:
            raise ValueError(f"No API key found for {provider}")
        
        logger.info(f"Initialized {provider} backend with model {self.model}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 512,
        **kwargs
    ) -> str:
        """
        Generate chat completion
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific parameters
            
        Returns:
            Generated response text
        """
        try:
            if self.provider == "openai":
                return self._chat_openai(messages, temperature, max_tokens, **kwargs)
            elif self.provider == "anthropic":
                return self._chat_anthropic(messages, temperature, max_tokens, **kwargs)
            elif self.provider == "gemini":
                return self._chat_gemini(messages, temperature, max_tokens, **kwargs)
        except Exception as e:
            logger.error(f"Error calling {self.provider}: {e}")
            return f"Error: {str(e)}"
    
    def _chat_openai(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """OpenAI chat completion"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def _chat_anthropic(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Anthropic chat completion"""
        # Separate system messages
        system_messages = [m["content"] for m in messages if m["role"] == "system"]
        system = system_messages[0] if system_messages else None
        
        # Filter out system messages
        chat_messages = [m for m in messages if m["role"] != "system"]
        
        response = self.client.messages.create(
            model=self.model,
            messages=chat_messages,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.content[0].text
    
    def _chat_gemini(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Google Gemini chat completion"""
        # Convert messages to Gemini format
        chat_history = []
        for msg in messages[:-1]:  # All except last
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({"role": role, "parts": [msg["content"]]})
        
        # Start chat with history
        chat = self.client.start_chat(history=chat_history)
        
        # Send last message
        last_message = messages[-1]["content"]
        response = chat.send_message(
            last_message,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )
        return response.text
    
    @property
    def model_name(self) -> str:
        """Get model identifier"""
        return f"{self.provider}-{self.model}"
    
    @property
    def is_available(self) -> bool:
        """Check if backend is configured and available"""
        return self.api_key is not None


def get_cloud_backend(provider: str, model: Optional[str] = None) -> CloudBackend:
    """
    Get a cloud backend instance
    
    Args:
        provider: Provider name ('openai', 'anthropic', 'gemini')
        model: Optional model override
        
    Returns:
        CloudBackend instance
    """
    return CloudBackend(provider, model)


def is_provider_available(provider: str) -> bool:
    """Check if a cloud provider is available and configured"""
    config = get_config()
    
    if provider == "openai":
        return OPENAI_AVAILABLE and config.openai_api_key is not None
    elif provider == "anthropic":
        return ANTHROPIC_AVAILABLE and config.anthropic_api_key is not None
    elif provider == "gemini":
        return GEMINI_AVAILABLE and config.gemini_api_key is not None
    
    return False
