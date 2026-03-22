"""
统一客户端接口
"""

from typing import List, Dict, Optional, Type
from .providers.base import Provider, LLMResponse, BaseProvider
from .providers.openai_client import OpenAIProvider
from .providers.anthropic_client import AnthropicProvider


class LLMClient:
    """
    统一 LLM 客户端
    
    Usage:
        client = LLMClient(provider=Provider.OPENAI, api_key="sk-...")
        response = client.chat(messages=[{"role": "user", "content": "Hello"}])
    """
    
    PROVIDER_MAP = {
        Provider.OPENAI: OpenAIProvider,
        Provider.ANTHROPIC: AnthropicProvider,
    }
    
    def __init__(
        self,
        provider: Provider,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        **kwargs
    ):
        """
        初始化 LLM 客户端
        
        Args:
            provider: Provider 类型（OPENAI/ANTHROPIC）
            api_key: API 密钥（如不传则从环境变量读取）
            model: 模型名称
            base_url: 自定义 API 地址
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
            **kwargs: 其他配置参数
        """
        self.provider = provider
        self.max_retries = max_retries
        self._kwargs = kwargs
        
        # 获取 Provider 类
        provider_class = self.PROVIDER_MAP.get(provider)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {provider}")
        
        # 处理 API Key
        if not api_key:
            import os
            if provider == Provider.OPENAI:
                api_key = os.getenv("OPENAI_API_KEY")
            elif provider == Provider.ANTHROPIC:
                api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise ValueError(
                f"API key required. Set {provider.value.upper()}_API_KEY env var or pass api_key parameter."
            )
        
        # 处理默认模型
        if not model:
            if provider == Provider.OPENAI:
                model = "gpt-4o"
            elif provider == Provider.ANTHROPIC:
                model = "claude-3-5-sonnet-20241022"
        
        # 创建 Provider 实例
        self._provider: BaseProvider = provider_class(
            api_key=api_key,
            model=model,
            base_url=base_url,
            timeout=timeout,
            **kwargs
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """
        发送对话请求
        
        Args:
            messages: 消息列表
            **kwargs: temperature, max_tokens 等参数
        
        Returns:
            LLMResponse: 响应对象
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return self._provider.chat(messages, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)  # 指数退避
        
        # 所有重试失败
        return LLMResponse(
            content="",
            error=f"All {self.max_retries} retries failed. Last error: {last_error}",
            model=str(self.provider.value),
        )
    
    def validate_connection(self) -> bool:
        """验证 API 连接"""
        return self._provider.validate_connection()
    
    def switch_provider(self, provider: Provider, api_key: Optional[str] = None):
        """
        切换 Provider
        
        Args:
            provider: 新的 Provider
            api_key: 新 Provider 的 API 密钥
        """
        self.__init__(
            provider=provider,
            api_key=api_key,
            **self._kwargs
        )
