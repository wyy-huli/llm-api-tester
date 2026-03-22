"""
验证器测试
"""

import pytest
from llm_tester.providers.base import LLMResponse
from llm_tester.validators import ResponseValidator, LatencyValidator


class TestResponseValidator:
    """响应验证器测试"""
    
    def test_valid_response(self):
        """测试有效响应"""
        validator = ResponseValidator()
        
        response = LLMResponse(
            content="Hello, world!",
            usage={"total_tokens": 10},
            latency=1.5,
            model="gpt-4o"
        )
        
        result = validator.validate(response)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_empty_content(self):
        """测试空内容"""
        validator = ResponseValidator()
        
        response = LLMResponse(
            content="",
            usage={},
            latency=1.0,
            model="gpt-4o"
        )
        
        result = validator.validate(response)
        
        assert result.is_valid is False
        assert any("empty" in err for err in result.errors)
    
    def test_error_response(self):
        """测试错误响应"""
        validator = ResponseValidator()
        
        response = LLMResponse(
            content="",
            error="API timeout",
            model="gpt-4o"
        )
        
        result = validator.validate(response)
        
        assert result.is_valid is False
        assert any("Error" in err for err in result.errors)


class TestLatencyValidator:
    """延迟验证器测试"""
    
    def test_within_threshold(self):
        """测试延迟在阈值内"""
        validator = LatencyValidator(max_latency=5.0)
        
        response = LLMResponse(
            content="OK",
            latency=2.0,
            model="gpt-4o"
        )
        
        assert validator.validate(response) is True
    
    def test_exceeds_threshold(self):
        """测试延迟超出阈值"""
        validator = LatencyValidator(max_latency=5.0)
        
        response = LLMResponse(
            content="OK",
            latency=8.0,
            model="gpt-4o"
        )
        
        assert validator.validate(response) is False
    
    def test_batch_validation(self):
        """测试批量验证"""
        validator = LatencyValidator(max_latency=5.0)
        
        responses = [
            LLMResponse(content="OK", latency=1.0, model="gpt-4o"),
            LLMResponse(content="OK", latency=2.0, model="gpt-4o"),
            LLMResponse(content="OK", latency=6.0, model="gpt-4o"),  # 超出
        ]
        
        stats = validator.validate_batch(responses)
        
        assert stats["count"] == 3
        assert stats["avg"] == 3.0
        assert stats["min"] == 1.0
        assert stats["max"] == 6.0
