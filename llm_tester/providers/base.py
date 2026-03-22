"""
Provider 抽象基类和响应数据类
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class Provider(Enum):
    """支持的 LLM Provider"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


@dataclass
class LLMResponse:
    """LLM API 响应数据类"""
    
    content: str
    """响应文本内容"""
    
    usage: Dict[str, int] = field(default_factory=dict)
    """Token 使用统计：{"input_tokens": int, "output_tokens": int}"""
    
    latency: float = 0.0
    """总延迟（秒）"""
    
    first_token_time: float = 0.0
    """首 token 时间（秒）"""
    
    model: str = ""
    """使用的模型名称"""
    
    raw_response: Any = None
    """原始响应对象"""
    
    error: Optional[str] = None
    """错误信息（如果有）"""
    
    def __post_init__(self):
        """确保 usage 字典有默认值"""
        if not self.usage:
            self.usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}


class BaseProvider(ABC):
    """Provider 抽象基类"""
    
    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
        **kwargs
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.timeout = timeout
        self.config = kwargs
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """发送对话请求"""
        pass
    
    @abstractmethod
    async def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """流式对话（异步）"""
        pass
    
    @abstractmethod
    def validate_connection(self) -> bool:
        """验证 API 连接"""
        pass
