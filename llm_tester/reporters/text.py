"""
文本报告生成器
"""

from typing import List
from ..providers.base import LLMResponse


class TextReporter:
    """文本报告生成器"""
    
    def generate(self, responses: List[LLMResponse], title: str = "Test Report") -> str:
        """
        生成文本报告
        
        Args:
            responses: 响应列表
            title: 报告标题
        
        Returns:
            格式化的文本报告
        """
        lines = [
            "=" * 60,
            f" {title}",
            "=" * 60,
            "",
        ]
        
        for i, response in enumerate(responses, 1):
            lines.append(f"[Test {i}]")
            lines.append(f"  Model: {response.model}")
            lines.append(f"  Status: {'✅ Success' if not response.error else '❌ Failed'}")
            
            if response.error:
                lines.append(f"  Error: {response.error}")
            else:
                lines.append(f"  Content: {response.content[:100]}...")
                lines.append(f"  Latency: {response.latency:.2f}s")
                lines.append(f"  Tokens: {response.usage.get('total_tokens', 'N/A')}")
            
            lines.append("")
        
        # 统计信息
        if responses:
            successful = sum(1 for r in responses if not r.error)
            avg_latency = sum(r.latency for r in responses if r.latency > 0) / max(successful, 1)
            
            lines.extend([
                "-" * 60,
                "Summary:",
                f"  Total: {len(responses)}",
                f"  Successful: {successful}",
                f"  Failed: {len(responses) - successful}",
                f"  Success Rate: {successful / len(responses) * 100:.1f}%",
                f"  Avg Latency: {avg_latency:.2f}s",
                "-" * 60,
            ])
        
        return "\n".join(lines)
    
    def print(self, responses: List[LLMResponse], title: str = "Test Report"):
        """直接打印报告"""
        print(self.generate(responses, title))
