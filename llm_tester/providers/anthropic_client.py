"""
Anthropic Provider 实现
"""

import time
from typing import List, Dict, Any, Optional

from .base import BaseProvider, LLMResponse


class AnthropicProvider(BaseProvider):
    """Anthropic Claude API Provider"""
    
    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
    
    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        timeout: int = 30,
        **kwargs
    ):
        super().__init__(
            api_key=api_key,
            model=model,
            timeout=timeout,
            **kwargs
        )
        self._client = None
    
    @property
    def client(self):
        """懒加载 Anthropic 客户端"""
        if self._client is None:
            try:
                from anthropic import Anthropic
                self._client = Anthropic(api_key=self.api_key, timeout=self.timeout)
            except ImportError:
                raise ImportError("Please install anthropic: pip install anthropic")
        return self._client
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """发送对话请求到 Anthropic API"""
        start_time = time.time()
        
        try:
            # 分离 system prompt
            system_prompt = ""
            conversation_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                else:
                    conversation_messages.append(msg)
            
            params = {
                "model": self.model,
                "messages": conversation_messages,
                "max_tokens": kwargs.get("max_tokens", 1000),
            }
            
            if system_prompt:
                params["system"] = system_prompt
            if "temperature" in kwargs:
                params["temperature"] = kwargs["temperature"]
            
            response = self.client.messages.create(**params)
            end_time = time.time()
            
            content = response.content[0].text if response.content else ""
            
            usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
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
        """验证 Anthropic API 连接"""
        try:
            response = self.chat(
                messages=[{"role": "user", "content": "Say hello in one word"}]
            )
            return response.error is None and len(response.content) > 0
        except Exception:
            return False
