#!/usr/bin/env python3
"""
基础使用示例
"""

import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_tester import LLMClient, Provider


def main():
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Please set OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='sk-...'")
        return
    
    # 初始化客户端
    print("Initializing OpenAI client...")
    client = LLMClient(
        provider=Provider.OPENAI,
        model="gpt-4o",
        max_retries=3,
    )
    
    # 验证连接
    print("Validating connection...")
    if not client.validate_connection():
        print("❌ Connection failed")
        return
    
    print("✅ Connection successful\n")
    
    # 发送请求
    prompt = "Explain what is AI testing in 2 sentences"
    print(f"Prompt: {prompt}\n")
    
    response = client.chat(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    # 显示结果
    print("Response:")
    print("-" * 40)
    print(response.content)
    print("-" * 40)
    print(f"\nLatency: {response.latency:.2f}s")
    print(f"Tokens: {response.usage}")
    print(f"Model: {response.model}")


if __name__ == "__main__":
    main()
