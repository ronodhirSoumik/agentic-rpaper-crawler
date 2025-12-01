# Provider Configuration Guide

## Choosing Between OpenAI and DeepSeek

This application supports two LLM providers for query clarification:

### OpenAI
- **Model**: `gpt-4o-mini` (default)
- **Pros**: High quality, well-tested, reliable
- **Cons**: Paid API (costs per token)
- **Get API Key**: https://platform.openai.com/api-keys

### DeepSeek
- **Model**: `deepseek-chat` (default)
- **Pros**: Cost-effective alternative
- **Cons**: May have different performance characteristics
- **Get API Key**: https://platform.deepseek.com/

## Configuration

### Method 1: Environment Variable (Recommended)

Set in your `.env` file:

```bash
# For OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# For DeepSeek
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your-key-here
```

### Method 2: Programmatic Selection

You can override the provider in code:

**Python Script:**
```python
from agent import ResearchAgent

# Force OpenAI
agent = ResearchAgent(provider="openai")

# Force DeepSeek
agent = ResearchAgent(provider="deepseek")
```

**API Request:**
```bash
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning for climate change",
    "provider": "deepseek"
  }'
```

## Custom Models

You can also specify custom models:

```python
from query_clarifier import QueryClarifier

# Use GPT-4
clarifier = QueryClarifier(
    provider="openai",
    model_name="gpt-4"
)

# Use specific DeepSeek model
clarifier = QueryClarifier(
    provider="deepseek",
    model_name="deepseek-chat"
)
```

## Switching Providers

To switch providers, simply update your `.env` file:

```bash
# Change from OpenAI to DeepSeek
LLM_PROVIDER=deepseek  # Change this line
DEEPSEEK_API_KEY=your-key-here  # Add this
```

No code changes needed! The agent will automatically use the new provider on next run.
