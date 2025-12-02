# AI Research Agent with LangGraph

An intelligent research assistant that uses LangGraph to clarify research queries, fetch relevant papers from Google Scholar, and save results to markdown files.

## Features

- **Query Clarification**: Uses OpenAI with structured output parsing to refine and structure research queries
- **Google Scholar Integration**: Fetches relevant research papers using the Scholarly library
- **LangGraph Workflow**: Implements a multi-step agent workflow with state management
- **FastAPI Server**: Provides a REST API for easy interaction
- **Markdown Output**: Saves research results with paper names and links to markdown files

## Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment Variables**

Choose your LLM provider (OpenAI, DeepSeek, OpenRouter, or Gemini):

```bash
cp .env.example .env
# Edit .env and set:
# - LLM_PROVIDER=openai, deepseek, openrouter, or gemini
# - Add the corresponding API key
```

**For OpenAI:**
```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

**For DeepSeek:**
```
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your-key-here
```

**For OpenRouter:**
```
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-your-key-here
```

**For Gemini:**
```
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your-google-api-key-here
```

3. **Run the Agent**

### Option 1: Direct Python Script
```bash
python agent.py "your research query here"
```

### Option 2: FastAPI Server
```bash
python api_server.py
```

Then make a POST request:
```bash
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning for climate change"}'
```

## Project Structure

- `agent.py` - Main LangGraph agent implementation
- `query_clarifier.py` - OpenAI-based query clarification with structured output
- `scholar_fetcher.py` - Google Scholar API integration
- `api_server.py` - FastAPI server for the research agent
- `models.py` - Pydantic models for structured data
- `results/` - Directory where markdown results are saved

## How It Works

1. **Query Input**: User provides a research query
2. **Clarification**: Agent uses OpenAI to clarify and structure the query
3. **Paper Fetching**: Searches Google Scholar for relevant papers
4. **Result Writing**: Saves paper names and links to a markdown file

## Example Output

The agent creates markdown files in the `results/` directory with content like:

```markdown
# Research Results: PerFed Personalized Fedeated Learning

**Clarified Query**: Personalized Federated Learning, PerFed (Personalized Federated), Federated Learning Personalization, Client-Specific Model Adaptation

## Papers Found

1. [PerFED-GAN: Personalized federated learning via generative adversarial networks](https://ieeexplore.ieee.org/abstract/document/9766407/)
2. [Perfedmask: Personalized federated learning with optimized masking vectors](https://openreview.net/forum?id=hxEIgUXLFF)
...
```

## Requirements

- Python 3.9+
- API key for one of: OpenAI, DeepSeek, OpenRouter, or Gemini
- Scholarly - for Google Scholar Feed Crawlng
