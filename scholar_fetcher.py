from scholarly import scholarly
from models import ResearchPaper
from typing import List
import time


class ScholarFetcher:
    """Fetches research papers from Google Scholar."""
    
    def __init__(self, max_results: int = 10):
        self.max_results = max_results
    
    def fetch_papers(self, search_query: str) -> List[ResearchPaper]:
        """
        Fetch research papers from Google Scholar.
        
        Args:
            search_query: The search query to use
            
        Returns:
            List of ResearchPaper objects
        """
        papers = []
        
        try:
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
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.5)
                    
                except StopIteration:
                    # No more results
                    break
                except Exception as e:
                    print(f"Error fetching paper {i+1}: {str(e)}")
                    continue
        
        except Exception as e:
            print(f"Error in Scholar search: {str(e)}")
        
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
    
    print(f"Found {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {', '.join(paper.authors[:3])}")
        print(f"   Year: {paper.year}")
        print(f"   Citations: {paper.citation_count}")
        print(f"   URL: {paper.url}")
