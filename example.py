"""
Example script demonstrating how to use the AI Research Agent.

This script shows different ways to interact with the agent:
1. Direct Python usage
2. Testing individual components
"""

from agent import ResearchAgent
from query_clarifier import QueryClarifier
from scholar_fetcher import ScholarFetcher


def example_full_agent():
    """Example: Run the full agent workflow."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Full Agent Workflow")
    print("="*60)
    
    agent = ResearchAgent(max_papers=5)
    result = agent.run("deep learning for medical image analysis")
    
    if result.get("output_file"):
        print(f"\n✓ Results saved to: {result['output_file']}")
        print(f"✓ Papers found: {len(result.get('papers', []))}")


def example_query_clarification():
    """Example: Test query clarification only."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Query Clarification Only")
    print("="*60)
    
    # You can specify the provider explicitly or let it use env variable
    # clarifier = QueryClarifier(provider="openai")      # Force OpenAI
    # clarifier = QueryClarifier(provider="deepseek")    # Force DeepSeek
    # clarifier = QueryClarifier(provider="openrouter")  # Force OpenRouter
    clarifier = QueryClarifier()  # Use LLM_PROVIDER from .env
    
    queries = [
        "AI for healthcare",
        "quantum computing applications",
        "renewable energy optimization"
    ]
    
    for query in queries:
        print(f"\nOriginal: {query}")
        result = clarifier.clarify(query)
        print(f"Clarified: {result.clarified_query}")
        print(f"Domain: {result.research_domain}")
        print(f"Key Concepts: {', '.join(result.key_concepts[:3])}")


def example_scholar_search():
    """Example: Test Google Scholar search only."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Google Scholar Search Only")
    print("="*60)
    
    fetcher = ScholarFetcher(max_results=3)
    papers = fetcher.fetch_papers("transformer models natural language processing")
    
    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Year: {paper.year}, Citations: {paper.citation_count}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print(" AI RESEARCH AGENT - EXAMPLES")
    print("="*70)
    
    # Uncomment the examples you want to run:
    
    # Example 1: Full agent workflow (requires OpenAI API key)
    # example_full_agent()
    
    # Example 2: Query clarification (requires OpenAI API key)
    # example_query_clarification()
    
    # Example 3: Scholar search (no API key needed, but may be slow)
    # example_scholar_search()
    
    print("\n" + "="*70)
    print("NOTE: Uncomment the examples in the script to run them.")
    print("Make sure to set your OPENAI_API_KEY in a .env file first!")
    print("="*70 + "\n")
