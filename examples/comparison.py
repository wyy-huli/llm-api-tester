#!/usr/bin/env python3
"""
Provider 对比示例
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_tester import LLMClient, Provider
from llm_tester.reporters.text import TextReporter


def main():
    prompt = "What are the key differences between AI testing and traditional software testing?"
    
    print("=" * 60)
    print("Provider Comparison Test")
    print("=" * 60)
    print(f"\nPrompt: {prompt}\n")
    
    responses = []
    
    # 测试 OpenAI
    if os.getenv("OPENAI_API_KEY"):
        print("Testing OpenAI...")
        try:
            openai_client = LLMClient(provider=Provider.OPENAI)
            response = openai_client.chat(
                messages=[{"role": "user", "content": prompt}]
            )
            response.model = f"OpenAI ({response.model})"
            responses.append(response)
            print(f"✅ OpenAI: {response.latency:.2f}s")
        except Exception as e:
            print(f"❌ OpenAI failed: {e}")
    else:
        print("⚠️  Skipping OpenAI (no API key)")
    
    # 测试 Anthropic
    if os.getenv("ANTHROPIC_API_KEY"):
        print("Testing Anthropic...")
        try:
            anthropic_client = LLMClient(provider=Provider.ANTHROPIC)
            response = anthropic_client.chat(
                messages=[{"role": "user", "content": prompt}]
            )
            response.model = f"Anthropic ({response.model})"
            responses.append(response)
            print(f"✅ Anthropic: {response.latency:.2f}s")
        except Exception as e:
            print(f"❌ Anthropic failed: {e}")
    else:
        print("⚠️  Skipping Anthropic (no API key)")
    
    if not responses:
        print("\n❌ No successful tests")
        return
    
    # 生成对比报告
    print("\n")
    reporter = TextReporter()
    reporter.print(responses, "Provider Comparison")


if __name__ == "__main__":
    main()
