from langgraph.graph import StateGraph, END
from models import AgentState, ClarifiedQuery
from query_clarifier import QueryClarifier
from scholar_fetcher import ScholarFetcher
from typing import Dict, Any
import os
from datetime import datetime
from pathlib import Path


class ResearchAgent:
    """LangGraph-based research agent that clarifies queries and fetches papers."""
    
    def __init__(self, max_papers: int = 10, provider: str = None):
        """
        Initialize the research agent.
        
        Args:
            max_papers: Maximum number of papers to fetch
            provider: LLM provider ("openai" or "deepseek"). If None, reads from env
        """
        self.query_clarifier = QueryClarifier(provider=provider)
        self.scholar_fetcher = ScholarFetcher(max_results=max_papers)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("clarify_query", self._clarify_query_node)
        workflow.add_node("fetch_papers", self._fetch_papers_node)
        workflow.add_node("write_results", self._write_results_node)
        
        # Define edges
        workflow.set_entry_point("clarify_query")
        workflow.add_edge("clarify_query", "fetch_papers")
        workflow.add_edge("fetch_papers", "write_results")
        workflow.add_edge("write_results", END)
        
        return workflow.compile()
    
    def _clarify_query_node(self, state: AgentState) -> Dict[str, Any]:
        """Node to clarify the research query."""
        print(f"\n🔍 Clarifying query: {state.original_query}")
        
        try:
            clarified = self.query_clarifier.clarify(state.original_query)
            print(f"✓ Clarified: {clarified.clarified_query}")
            print(f"  Key concepts: {', '.join(clarified.key_concepts)}")
            print(f"  Research domain: {clarified.research_domain}")
            
            return {"clarified_query": clarified}
        
        except Exception as e:
            error_msg = f"Error clarifying query: {str(e)}"
            print(f"✗ {error_msg}")
            return {"error": error_msg}
    
    def _fetch_papers_node(self, state: AgentState) -> Dict[str, Any]:
        """Node to fetch papers from Google Scholar."""
        if state.error:
            return {}
        
        print(f"\n📚 Fetching papers from Google Scholar...")
        
        try:
            # Use the clarified query and search terms
            papers = self.scholar_fetcher.fetch_papers_with_terms(
                state.clarified_query.search_terms
            )
            
            print(f"✓ Found {len(papers)} papers")
            
            return {"papers": papers}
        
        except Exception as e:
            error_msg = f"Error fetching papers: {str(e)}"
            print(f"✗ {error_msg}")
            return {"error": error_msg}
    
    def _write_results_node(self, state: AgentState) -> Dict[str, Any]:
        """Node to write results to a markdown file."""
        if state.error:
            return {}
        
        print(f"\n📝 Writing results to markdown file...")
        
        try:
            # Create results directory if it doesn't exist
            results_dir = Path("results")
            results_dir.mkdir(exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_query = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' 
                               for c in state.original_query)[:50]
            filename = f"{safe_query}_{timestamp}.md"
            filepath = results_dir / filename
            
            # Write markdown content
            content = self._generate_markdown(state)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Results saved to: {filepath}")
            
            return {"output_file": str(filepath)}
        
        except Exception as e:
            error_msg = f"Error writing results: {str(e)}"
            print(f"✗ {error_msg}")
            return {"error": error_msg}
    
    def _generate_markdown(self, state: AgentState) -> str:
        """Generate markdown content for the results."""
        lines = []
        
        # Title
        lines.append(f"# Research Results: {state.original_query}\n")
        
        # Clarified query section
        if state.clarified_query:
            lines.append(f"**Clarified Query**: {state.clarified_query.clarified_query}\n")
            lines.append(f"**Research Domain**: {state.clarified_query.research_domain}\n")
            lines.append(f"**Key Concepts**: {', '.join(state.clarified_query.key_concepts)}\n")
        
        # Papers section
        lines.append(f"\n## Papers Found ({len(state.papers)} results)\n")
        
        if state.papers:
            for i, paper in enumerate(state.papers, 1):
                lines.append(f"\n### {i}. {paper.title}\n")
                
                if paper.authors:
                    authors_str = ', '.join(paper.authors[:5])
                    if len(paper.authors) > 5:
                        authors_str += f" et al. ({len(paper.authors)} authors)"
                    lines.append(f"**Authors**: {authors_str}\n")
                
                if paper.year:
                    lines.append(f"**Year**: {paper.year}\n")
                
                if paper.citation_count is not None:
                    lines.append(f"**Citations**: {paper.citation_count}\n")
                
                if paper.url:
                    lines.append(f"**Link**: [{paper.url}]({paper.url})\n")
                
                if paper.abstract:
                    abstract_preview = paper.abstract[:300] + "..." if len(paper.abstract) > 300 else paper.abstract
                    lines.append(f"\n**Abstract**: {abstract_preview}\n")
        else:
            lines.append("No papers found for this query.\n")
        
        # Footer
        lines.append(f"\n---\n")
        lines.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        return '\n'.join(lines)
    
    def run(self, query: str) -> AgentState:
        """
        Run the research agent with a query.
        
        Args:
            query: The research query
            
        Returns:
            Final AgentState with results
        """
        print(f"\n{'='*60}")
        print(f"AI Research Agent")
        print(f"{'='*60}")
        
        # Create initial state
        initial_state = AgentState(original_query=query)
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        print(f"\n{'='*60}")
        if final_state.get("error"):
            print(f"❌ Agent completed with errors: {final_state['error']}")
        else:
            print(f"✅ Agent completed successfully!")
            print(f"   Output file: {final_state.get('output_file')}")
        print(f"{'='*60}\n")
        
        return final_state


if __name__ == "__main__":
    import sys
    
    # Get query from command line or use default
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "machine learning for climate change prediction"
    
    # Run the agent
    agent = ResearchAgent(max_papers=10)
    result = agent.run(query)
