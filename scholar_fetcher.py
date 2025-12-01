from scholarly import scholarly, ProxyGenerator
from models import ResearchPaper
from typing import List
import time

class ScholarFetcher:
    """Fetches research papers from Google Scholar with proxy support."""
    
    def __init__(self, max_results: int = 10, use_proxy: bool = True):
        """
        Initialize the scholar fetcher.
        
        Args:
            max_results: Maximum number of papers to fetch
            use_proxy: Whether to use proxy to avoid blocking (recommended)
        """
        self.max_results = max_results
        
        # Set up proxy to avoid Google Scholar blocking
        if use_proxy:
            try:
                print("Setting up proxy for Google Scholar...")
                pg = ProxyGenerator()
                
                # Try FreeProxies first (no API key needed)
                success = pg.FreeProxies()
                scholarly.use_proxy(pg)
                
                print("Proxy configured successfully")
            except Exception as e:
                print(f"Warning: Could not set up proxy: {e}")
                print("Continuing without proxy (may be rate-limited)")
    
    def fetch_papers(self, search_query: str, retry_count: int = 3) -> List[ResearchPaper]:
        """
        Fetch research papers from Google Scholar with retry logic.
        
        Args:
            search_query: The search query to use
            retry_count: Number of retries if request fails
            
        Returns:
            List of ResearchPaper objects
        """
        papers = []
        
        for attempt in range(retry_count):
            try:
                print(f"Searching Google Scholar: '{search_query}' (attempt {attempt + 1}/{retry_count})")
                
                # Search for papers
                search_results = scholarly.search_pubs(search_query)
                
                # Fetch up to max_results papers
                for i in range(self.max_results):
                    try:
                        paper_data = next(search_results)
                        
                        # Extract paper information
                        paper = ResearchPaper(
                            title=paper_data.get('bib', {}).get('title', 'Unknown Title'),
                            authors=paper_data.get('bib', {}).get('author', []),
                            year=int(paper_data.get('bib', {}).get('pub_year', 0)) if paper_data.get('bib', {}).get('pub_year') else None,
                            url=paper_data.get('pub_url') or paper_data.get('eprint_url'),
                            citation_count=paper_data.get('num_citations', 0),
                            abstract=paper_data.get('bib', {}).get('abstract')
                        )
                        
                        papers.append(paper)
                        print(f"  ✓ Found: {paper.title[:60]}...")
                        
                        # Small delay to avoid rate limiting
                        time.sleep(1)
                        
                    except StopIteration:
                        # No more results
                        print(f"No more results available (found {len(papers)} papers)")
                        break
                    except Exception as e:
                        print(f"  Error fetching paper {i+1}: {str(e)}")
                        continue
                
                # If we got here, the search succeeded
                print(f"✓ Successfully fetched {len(papers)} papers")
                return papers
                
            except Exception as e:
                error_msg = str(e)
                print(f"✗ Error in Google Scholar search (attempt {attempt + 1}/{retry_count}): {error_msg}")
                
                if "Cannot fetch" in error_msg or "blocked" in error_msg.lower():
                    if attempt < retry_count - 1:
                        wait_time = (attempt + 1) * 5  # Exponential backoff
                        print(f"  Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                    else:
                        print("  ❌ All retry attempts failed. Google Scholar may be blocking requests.")

                else:
                    # Different error, don't retry
                    break
        
        return papers
    
    def fetch_papers_with_terms(self, search_terms: List[str]) -> List[ResearchPaper]:
        """
        Fetch papers using multiple search terms and combine results.
        
        Args:
            search_terms: List of search terms to use
            
        Returns:
            Combined list of unique ResearchPaper objects
        """
        all_papers = []
        seen_titles = set()
        
        for term in search_terms[:3]:  # Limit to first 3 search terms to avoid too many requests
            papers = self.fetch_papers(term)
            
            # Add only unique papers
            for paper in papers:
                if paper.title not in seen_titles:
                    all_papers.append(paper)
                    seen_titles.add(paper.title)
        
        # Sort by citation count (descending)
        all_papers.sort(key=lambda p: p.citation_count or 0, reverse=True)
        
        return all_papers[:self.max_results]


if __name__ == "__main__":
    # Test the scholar fetcher
    fetcher = ScholarFetcher(max_results=5)
    
    papers = fetcher.fetch_papers("machine learning climate change")
    
    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {', '.join(paper.authors[:3])}")
        print(f"   Year: {paper.year}")
        print(f"   Citations: {paper.citation_count}")
        print(f"   URL: {paper.url}")
