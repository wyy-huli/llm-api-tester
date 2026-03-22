"""
JSON 报告生成器
"""

import json
from typing import List
from ..providers.base import LLMResponse


class JSONReporter:
    """JSON 报告生成器"""
    
    def generate(self, responses: List[LLMResponse], title: str = "Test Report") -> dict:
        """
        生成 JSON 报告
        
        Args:
            responses: 响应列表
            title: 报告标题
        
        Returns:
            报告字典
        """
        report = {
            "title": title,
            "total": len(responses),
            "successful": 0,
            "failed": 0,
            "tests": [],
        }
        
        latencies = []
        
        for i, response in enumerate(responses, 1):
            test_result = {
                "id": i,
                "model": response.model,
                "success": response.error is None,
                "latency": response.latency,
                "tokens": response.usage,
            }
            
            if response.error:
                test_result["error"] = response.error
                report["failed"] += 1
            else:
                test_result["content"] = response.content[:500]  # 限制长度
                report["successful"] += 1
                latencies.append(response.latency)
            
            report["tests"].append(test_result)
        
        # 统计信息
        if latencies:
            report["statistics"] = {
                "avg_latency": sum(latencies) / len(latencies),
                "min_latency": min(latencies),
                "max_latency": max(latencies),
                "success_rate": report["successful"] / len(responses) * 100,
            }
        
        return report
    
    def export(self, responses: List[LLMResponse], filepath: str, title: str = "Test Report"):
        """
        导出到 JSON 文件
        
        Args:
            responses: 响应列表
            filepath: 输出文件路径
            title: 报告标题
        """
        report = self.generate(responses, title)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filepath
