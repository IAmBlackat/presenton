"""
Utility functions for determining which LLM provider to use for template generation.

Customized by FutureForge Studios Private Limited (https://ffstudios.io)

This module allows template generation to use the same local/self-hosted model
that is configured for content generation, or fall back to API-based generation.
"""

from enums.llm_provider import LLMProvider
from utils.get_env import get_template_llm_provider_env, get_llm_provider_env
from utils.llm_provider import get_llm_provider


def get_template_llm_provider() -> LLMProvider:
    """
    Determine which LLM provider to use for template generation.
    
    Logic:
    1. If TEMPLATE_LLM_PROVIDER is explicitly set to "api", use OpenAI (for GPT-5 Responses API)
    2. If TEMPLATE_LLM_PROVIDER is explicitly set to "local", use the same provider as content generation
    3. If TEMPLATE_LLM_PROVIDER is not set, default to "local" if using a local model for content,
       otherwise use OpenAI (for GPT-5 Responses API)
    
    Returns:
        LLMProvider: The provider to use for template generation
    """
    template_provider_setting = get_template_llm_provider_env()
    content_provider = get_llm_provider()
    
    # If explicitly set to use API (OpenAI GPT-5 Responses API)
    if template_provider_setting == "api":
        return LLMProvider.OPENAI
    
    # If explicitly set to use local model
    if template_provider_setting == "local":
        return content_provider
    
    # Default behavior: use local if content generation uses local, otherwise use API
    if content_provider in [LLMProvider.OLLAMA, LLMProvider.CUSTOM]:
        return content_provider
    else:
        return LLMProvider.OPENAI


def should_use_local_model_for_templates() -> bool:
    """
    Check if local model should be used for template generation.
    
    Returns:
        bool: True if local model should be used, False if API should be used
    """
    return get_template_llm_provider() in [LLMProvider.OLLAMA, LLMProvider.CUSTOM]


def should_use_api_model_for_templates() -> bool:
    """
    Check if API model (OpenAI GPT-5 Responses API) should be used for template generation.
    
    Returns:
        bool: True if API model should be used, False if local model should be used
    """
    return get_template_llm_provider() == LLMProvider.OPENAI
