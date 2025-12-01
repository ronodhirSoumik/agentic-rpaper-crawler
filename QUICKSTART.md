# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Your API Key

**Choose your LLM provider** (OpenAI, DeepSeek, or OpenRouter):

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and configure your provider:

   **Option A: Using OpenAI**
   ```
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-your-openai-key-here
   ```

   **Option B: Using DeepSeek**
   ```
   LLM_PROVIDER=deepseek
   DEEPSEEK_API_KEY=your-deepseek-key-here
   ```

   **Option C: Using OpenRouter**
   ```
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=sk-or-your-openrouter-key-here
   ```

### Step 3: Run the Agent

**Option A: Command Line**
```bash
python agent.py "machine learning for climate change"
```

**Option B: API Server**
```bash
# Start the server
python api_server.py

# In another terminal, make a request:
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{"query": "deep learning for medical imaging"}'
```

## 📁 Output

Results are saved to the `results/` directory as markdown files with:
- Paper titles
- Author names
- Publication years
- Citation counts
- Direct links to papers

## 🔧 Troubleshooting

**Issue**: `ModuleNotFoundError`  
**Solution**: Run `pip install -r requirements.txt`

**Issue**: `DeepSeek API key not found`  
**Solution**: Create a `.env` file with your `DEEPSEEK_API_KEY`

**Issue**: Google Scholar is slow  
**Solution**: Reduce `max_papers` parameter (default is 10, try 5)

## 📚 Examples

See `example.py` for more usage examples:
```bash
python example.py
```

## 🎯 What It Does

1. **Clarifies** your research query using AI
2. **Fetches** relevant papers from Google Scholar
3. **Saves** results to a formatted markdown file

That's it! Happy researching! 🎓
