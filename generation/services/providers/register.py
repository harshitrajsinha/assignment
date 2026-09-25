from .openai import OpenAIProvider
from .gemini import GeminiProvider
import logging

logger = logging.getLogger(__name__)


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
            logger.error(
                "Unsupported LLM provider requested: provider=%s",
                provider,
            )

            raise ValueError(
                f"Unsupported provider: {provider}. "
                f"Supported providers: {list(cls._providers.keys())}"
            )

        try:
            register_provider = provider_class()

            logger.info(
                "LLM provider initialized successfully: provider=%s",
                provider,
            )

            return register_provider

        except Exception:
            logger.exception(
                "Failed to initialize LLM provider: provider=%s",
                provider,
            )
            raise