"""
OpenAI Provider 实现
"""

import time
from typing import List, Dict, Any, Optional

from .base import BaseProvider, LLMResponse


class OpenAIProvider(BaseProvider):
    """OpenAI API Provider"""
    
    DEFAULT_MODEL = "gpt-4o"
    DEFAULT_BASE_URL = "https://api.openai.com/v1"
    
    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        base_url: Optional[str] = None,
        timeout: int = 30,
        **kwargs
    ):
        super().__init__(
            api_key=api_key,
            model=model,
            base_url=base_url or self.DEFAULT_BASE_URL,
            timeout=timeout,
            **kwargs
        )
        self._client = None
    
    @property
    def client(self):
        """懒加载 OpenAI 客户端"""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    timeout=self.timeout
                )
            except ImportError:
                raise ImportError("Please install openai: pip install openai")
        return self._client
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """发送对话请求到 OpenAI API"""
        start_time = time.time()
        
        try:
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 1000),
            }
            
            response = self.client.chat.completions.create(**params)
            end_time = time.time()
            
            choice = response.choices[0]
            content = choice.message.content or ""
            
            usage = {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            
            return LLMResponse(
                content=content,
                usage=usage,
                latency=end_time - start_time,
                first_token_time=end_time - start_time,
                model=self.model,
                raw_response=response,
            )
            
        except Exception as e:
            end_time = time.time()
            return LLMResponse(
                content="",
                latency=end_time - start_time,
                model=self.model,
                error=str(e),
            )
    
    async def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """流式对话（异步）"""
        raise NotImplementedError("Stream not implemented yet")
    
    def validate_connection(self) -> bool:
        """验证 OpenAI API 连接"""
        try:
            response = self.chat(
                messages=[{"role": "user", "content": "Say hello in one word"}]
            )
            return response.error is None and len(response.content) > 0
        except Exception:
            return False
