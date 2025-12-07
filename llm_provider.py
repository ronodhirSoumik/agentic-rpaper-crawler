from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMConfig:
    """Configuration for an LLM provider."""
    
    provider: str
    model_name: str
    api_key: str
    base_url: Optional[str] = None
    temperature: float = 0.3
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.api_key:
            raise ValueError(f"{self.provider.upper()}_API_KEY not found in environment variables")


class LLMProviderProcessor:
    """
    Centralized processor for LLM provider configurations.
    
    Handles configuration for OpenAI, DeepSeek, OpenRouter, and Gemini providers.
    Reads from environment variables and provides a unified interface.
    """
    
    # Provider-specific defaults
    PROVIDER_DEFAULTS = {
        "openai": {
            "model_name": "gpt-4o-mini",
            "base_url": None,
            "api_key_env": "OPENAI_API_KEY"
        },
        "deepseek": {
            "model_name": "deepseek-chat",
            "base_url": "https://api.deepseek.com",
            "api_key_env": "DEEPSEEK_API_KEY"
        },
        "openrouter": {
            "model_name": "alibaba/tongyi-deepresearch-30b-a3b:free",
            "base_url": "https://openrouter.ai/api/v1",
            "api_key_env": "OPENROUTER_API_KEY"
        },
        "gemini": {
            "model_name": "gemini-2.5-flash",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "api_key_env": "GOOGLE_API_KEY"
        }
    }
    
    @classmethod
    def get_config(
        cls,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.3
    ) -> LLMConfig:
        """
        Get LLM configuration for the specified provider.
        
        Args:
            provider: Provider name ("openai", "deepseek", "openrouter", "gemini").
                     If None, reads from LLM_PROVIDER env variable.
            model_name: Model name to use. If None, uses provider default.
            temperature: Temperature for generation.
            
        Returns:
            LLMConfig object with all necessary configuration.
            
        Raises:
            ValueError: If provider is invalid or API key is missing.
        """
        # Determine provider
        if provider is None:
            provider = os.getenv("LLM_PROVIDER", "openai").lower()
        else:
            provider = provider.lower()
        
        # Validate provider
        if provider not in cls.PROVIDER_DEFAULTS:
            valid_providers = ", ".join(cls.PROVIDER_DEFAULTS.keys())
            raise ValueError(
                f"Invalid provider '{provider}'. "
                f"Valid options: {valid_providers}"
            )
        
        # Get provider defaults
        defaults = cls.PROVIDER_DEFAULTS[provider]
        
        # Determine model name
        if model_name is None:
            model_name = defaults["model_name"]
        
        # Get API key
        api_key_env = defaults["api_key_env"]
        api_key = os.getenv(api_key_env)
        
        if not api_key:
            raise ValueError(
                f"API key not found. Please set {api_key_env} in your .env file"
            )
        
        # Create and return config
        config = LLMConfig(
            provider=provider,
            model_name=model_name,
            api_key=api_key,
            base_url=defaults["base_url"],
            temperature=temperature
        )
        
        return config
    
    @classmethod
    def get_available_providers(cls) -> list[str]:
        """Get list of available provider names."""
        return list(cls.PROVIDER_DEFAULTS.keys())
    
    @classmethod
    def get_default_model(cls, provider: str) -> str:
        """Get default model name for a provider."""
        provider = provider.lower()
        if provider not in cls.PROVIDER_DEFAULTS:
            raise ValueError(f"Unknown provider: {provider}")
        return cls.PROVIDER_DEFAULTS[provider]["model_name"]


if __name__ == "__main__":
    # Test the processor
    print("Testing LLM Provider Processor\n")
    
    # Show available providers
    print(f"Available providers: {LLMProviderProcessor.get_available_providers()}\n")
    
    # Test each provider (will fail if API keys not set)
    for provider in ["openai", "deepseek", "openrouter", "gemini"]:
        try:
            config = LLMProviderProcessor.get_config(provider=provider)
            print(f"✓ {provider.upper()} Configuration:")
            print(f"  Model: {config.model_name}")
            print(f"  Base URL: {config.base_url or 'Default'}")
            print(f"  API Key: {'*' * 10}{config.api_key[-4:] if len(config.api_key) > 4 else '****'}")
            print()
        except ValueError as e:
            print(f"✗ {provider.upper()}: {e}\n")
