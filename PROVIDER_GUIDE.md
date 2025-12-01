# Provider Configuration Guide

## Choosing Your LLM Provider

This application supports three LLM providers for query clarification:

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

### OpenRouter
- **Model**: `openai/gpt-4o-mini` (default)
- **Pros**: Access to multiple models through one API, flexible pricing
- **Cons**: Additional abstraction layer
- **Get API Key**: https://openrouter.ai/keys
- **Note**: Can access various models (OpenAI, Anthropic, Google, etc.)

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

# For OpenRouter
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-your-key-here
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

# Force OpenRouter
agent = ResearchAgent(provider="openrouter")
```

**API Request:**
```bash
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning for climate change",
    "provider": "openrouter"
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

# Use Claude via OpenRouter
clarifier = QueryClarifier(
    provider="openrouter",
    model_name="anthropic/claude-3-sonnet"
)

# Use Gemini via OpenRouter
clarifier = QueryClarifier(
    provider="openrouter",
    model_name="google/gemini-pro"
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
