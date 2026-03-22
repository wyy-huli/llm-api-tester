#!/usr/bin/env python3
"""
LLM API Tester - CLI 工具

Usage:
    llm-test --provider openai --prompt "Hello"
    llm-test --batch test_cases.json
    llm-test --compare --providers openai,anthropic
"""

import argparse
import json
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from llm_tester import LLMClient, Provider
from llm_tester.reporters.text import TextReporter
from llm_tester.reporters.json_reporter import JSONReporter


def main():
    parser = argparse.ArgumentParser(
        description="LLM API Tester - 多 Provider LLM API 测试工具"
    )
    
    parser.add_argument(
        "--provider",
        type=str,
        default="openai",
        choices=["openai", "anthropic"],
        help="Provider 名称"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        help="模型名称（可选）"
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        help="测试 prompt"
    )
    
    parser.add_argument(
        "--batch",
        type=str,
        help="批量测试文件路径（JSON）"
    )
    
    parser.add_argument(
        "--compare",
        action="store_true",
        help="对比模式（多个 Provider）"
    )
    
    parser.add_argument(
        "--providers",
        type=str,
        help="对比模式的 Provider 列表（逗号分隔）"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        choices=["text", "json"],
        default="text",
        help="输出格式"
    )
    
    parser.add_argument(
        "--output-file",
        type=str,
        help="输出文件路径"
    )
    
    args = parser.parse_args()
    
    # 批量测试模式
    if args.batch:
        run_batch_test(args)
        return
    
    # 对比模式
    if args.compare:
        run_compare_test(args)
        return
    
    # 单次测试
    if not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    run_single_test(args)


def run_single_test(args):
    """单次测试"""
    provider = Provider(args.provider)
    
    try:
        client = LLMClient(
            provider=provider,
            model=args.model,
        )
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    print(f"Testing {provider.value}...")
    response = client.chat(
        messages=[{"role": "user", "content": args.prompt}]
    )
    
    if args.output == "json":
        reporter = JSONReporter()
        report = reporter.generate([response], "Single Test")
        
        if args.output_file:
            reporter.export([response], args.output_file, "Single Test")
            print(f"Report saved to: {args.output_file}")
        else:
            print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        reporter = TextReporter()
        reporter.print([response], "Single Test")


def run_batch_test(args):
    """批量测试"""
    batch_file = Path(args.batch)
    
    if not batch_file.exists():
        print(f"❌ File not found: {batch_file}")
        sys.exit(1)
    
    with open(batch_file, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)
    
    provider = Provider(args.provider)
    
    try:
        client = LLMClient(provider=provider, model=args.model)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    responses = []
    
    for i, test_case in enumerate(test_cases, 1):
        prompt = test_case.get("prompt", "")
        print(f"[{i}/{len(test_cases)}] Testing...")
        
        response = client.chat(
            messages=[{"role": "user", "content": prompt}]
        )
        responses.append(response)
    
    # 生成报告
    if args.output == "json":
        reporter = JSONReporter()
        
        if args.output_file:
            reporter.export(responses, args.output_file, "Batch Test")
            print(f"Report saved to: {args.output_file}")
        else:
            report = reporter.generate(responses, "Batch Test")
            print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        reporter = TextReporter()
        reporter.print(responses, "Batch Test")


def run_compare_test(args):
    """对比测试"""
    if not args.providers:
        print("❌ Please specify --providers (e.g., --providers openai,anthropic)")
        sys.exit(1)
    
    if not args.prompt:
        print("❌ Please specify --prompt")
        sys.exit(1)
    
    provider_names = [p.strip() for p in args.providers.split(",")]
    responses = []
    
    for name in provider_names:
        try:
            provider = Provider(name)
        except ValueError:
            print(f"⚠️  Skipping unknown provider: {name}")
            continue
        
        print(f"Testing {name}...")
        
        try:
            client = LLMClient(provider=provider)
            response = client.chat(
                messages=[{"role": "user", "content": args.prompt}]
            )
            responses.append(response)
        except Exception as e:
            print(f"❌ {name} failed: {e}")
    
    if not responses:
        print("No successful tests")
        sys.exit(1)
    
    # 生成对比报告
    reporter = TextReporter()
    reporter.print(responses, "Provider Comparison")
    
    if args.output_file:
        json_reporter = JSONReporter()
        json_reporter.export(responses, args.output_file, "Provider Comparison")
        print(f"JSON report saved to: {args.output_file}")


if __name__ == "__main__":
    main()
