"""
客户端测试
"""

import pytest
import os
from llm_tester import LLMClient, Provider


class TestLLMClient:
    """LLMClient 测试类"""
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key")
    def test_openai_basic(self):
        """测试 OpenAI 基础对话"""
        client = LLMClient(provider=Provider.OPENAI)
        
        response = client.chat(
            messages=[{"role": "user", "content": "Say hello in one word"}]
        )
        
        assert response.error is None
        assert len(response.content) > 0
        assert response.latency > 0
        assert response.usage["total_tokens"] > 0
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="No Anthropic API key")
    def test_anthropic_basic(self):
        """测试 Anthropic 基础对话"""
        client = LLMClient(provider=Provider.ANTHROPIC)
        
        response = client.chat(
            messages=[{"role": "user", "content": "Say hello in one word"}]
        )
        
        assert response.error is None
        assert len(response.content) > 0
        assert response.latency > 0
    
    def test_invalid_provider(self):
        """测试无效 Provider"""
        with pytest.raises(ValueError):
            # 尝试创建不支持的 Provider
            from llm_tester.providers.base import Provider
            # 这里需要实际测试，但暂时跳过
            pass
    
    def test_missing_api_key(self):
        """测试缺失 API Key"""
        # 临时清除环境变量
        old_key = os.environ.pop("OPENAI_API_KEY", None)
        
        try:
            with pytest.raises(ValueError, match="API key required"):
                LLMClient(provider=Provider.OPENAI, api_key=None)
        finally:
            # 恢复环境变量
            if old_key:
                os.environ["OPENAI_API_KEY"] = old_key
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key")
    def test_latency_statistics(self):
        """测试延迟统计"""
        client = LLMClient(provider=Provider.OPENAI)
        
        latencies = []
        for i in range(3):
            response = client.chat(
                messages=[{"role": "user", "content": f"Test {i}"}]
            )
            latencies.append(response.latency)
        
        avg_latency = sum(latencies) / len(latencies)
        print(f"平均延迟：{avg_latency:.2f}s")
        
        assert avg_latency < 10.0  # 平均延迟应小于 10 秒
