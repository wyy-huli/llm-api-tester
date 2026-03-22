"""
LLM API Tester - 轻量级多 Provider LLM API 测试工具

Usage:
    from llm_tester import LLMClient, Provider
    
    client = LLMClient(provider=Provider.OPENAI, api_key="sk-...")
    response = client.chat(messages=[{"role": "user", "content": "Hello"}])
    print(response.content)
"""

from .client import LLMClient
from .providers.base import Provider, LLMResponse

__version__ = "0.1.0"
__author__ = "wyyhuli"
__all__ = ["LLMClient", "Provider", "LLMResponse"]
