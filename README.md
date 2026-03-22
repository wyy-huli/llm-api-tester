# LLM API Tester

> 轻量级多 Provider LLM API 测试工具

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 项目目标

统一接口测试多个 LLM Provider（OpenAI、Anthropic），自动化验证 API 响应质量，生成对比测试报告。

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/wyyhuli/llm-api-tester.git
cd llm-api-tester

# 安装依赖
pip install -r requirements.txt

# 或者安装为包
pip install -e .
```

### 配置 API Key

```bash
# 方式 1：环境变量（推荐）
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# 方式 2：代码中传入
```

### 基础使用

```python
from llm_tester import LLMClient, Provider

# 初始化客户端
client = LLMClient(
    provider=Provider.OPENAI,
    api_key="sk-...",  # 或从环境变量读取
    model="gpt-4o",
)

# 发送请求
response = client.chat(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, who are you?"}
    ],
    temperature=0.7,
    max_tokens=1000
)

# 获取响应
print(f"Content: {response.content}")
print(f"Latency: {response.latency:.2f}s")
print(f"Tokens: {response.usage}")
```

### CLI 使用

```bash
# 单次测试
llm-test --provider openai --prompt "Say hello"

# 批量测试
llm-test --provider openai --batch test_cases.json

# 对比测试
llm-test --compare --providers openai,anthropic --prompt "What is AI?"

# 导出 JSON 报告
llm-test --provider openai --prompt "Hello" --output json --output-file report.json
```

## 📁 项目结构

```
llm-api-tester/
├── llm_tester/              # 主包
│   ├── client.py            # 统一客户端
│   ├── providers/           # Provider 实现
│   │   ├── base.py          # 抽象基类
│   │   ├── openai_client.py
│   │   └── anthropic_client.py
│   ├── validators/          # 验证器
│   ├── reporters/           # 报告生成
│   └── utils/               # 工具函数
├── tests/                   # 测试
├── examples/                # 示例
├── cli.py                   # CLI 入口
├── pyproject.toml
└── README.md
```

## ✅ 功能特性

- ✅ 统一接口测试多个 Provider
- ✅ 自动重试和超时控制
- ✅ 响应验证（Schema、延迟、Token）
- ✅ 文本/JSON 报告生成
- ✅ CLI 工具支持
- ✅ 批量测试和对比测试

## 🧪 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 带覆盖率
pytest tests/ -v --cov=llm_tester --cov-report=html

# 运行单个测试
pytest tests/test_client.py -v
```

## 📝 示例代码

查看 `examples/` 目录获取更多使用示例。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
