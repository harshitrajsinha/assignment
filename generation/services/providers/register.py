from .openai import OpenAIProvider
from .gemini import GeminiProvider


class ProviderFactory:
    """Register the LLM provider to be used"""
    
    providers = {
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
    }
    
    @classmethod
    def create_provider(cls, provider: str):
        
        provider_class = cls.providers.get(provider.lower())
        
        if provider_class is None:
            raise ValueError(
                f"Unsupported provider: {provider}. "
                f"Supported providers: {list(cls._providers.keys())}"
            )
        
        return provider_class()