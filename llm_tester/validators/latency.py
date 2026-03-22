"""
延迟验证器
"""

from typing import List
from ..providers.base import LLMResponse


class LatencyValidator:
    """
    延迟验证器
    
    Usage:
        validator = LatencyValidator(max_latency=5.0)
        result = validator.validate(response)
    """
    
    def __init__(
        self,
        max_latency: float = 5.0,
        max_first_token: float = 2.0
    ):
        """
        Args:
            max_latency: 最大可接受延迟（秒）
            max_first_token: 最大首 token 时间（秒）
        """
        self.max_latency = max_latency
        self.max_first_token = max_first_token
    
    def validate(self, response: LLMResponse) -> bool:
        """验证延迟是否在可接受范围内"""
        if response.latency > self.max_latency:
            return False
        
        if response.first_token_time > self.max_first_token:
            return False
        
        return True
    
    def validate_batch(self, responses: List[LLMResponse]) -> dict:
        """
        批量验证延迟
        
        Returns:
            统计信息字典
        """
        if not responses:
            return {"error": "No responses to validate"}
        
        latencies = [r.latency for r in responses if r.latency > 0]
        
        if not latencies:
            return {"error": "No valid latency data"}
        
        return {
            "count": len(latencies),
            "avg": sum(latencies) / len(latencies),
            "min": min(latencies),
            "max": max(latencies),
            "p95": sorted(latencies)[int(len(latencies) * 0.95)] if len(latencies) > 20 else max(latencies),
            "pass_rate": sum(1 for l in latencies if l <= self.max_latency) / len(latencies),
        }
