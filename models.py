from pydantic import BaseModel, Field
from typing import List, Optional


class ClarifiedQuery(BaseModel):
    """Structured output for clarified research query."""
    
    original_query: str = Field(description="The original user query")
    clarified_query: str = Field(description="The clarified and structured research query")
    key_concepts: List[str] = Field(description="Key concepts extracted from the query")
    search_terms: List[str] = Field(description="Optimized search terms for academic databases")
    research_domain: str = Field(description="The primary research domain or field")


class ResearchPaper(BaseModel):
    """Model for a research paper."""
    
    title: str = Field(description="Title of the research paper")
    authors: List[str] = Field(default_factory=list, description="List of authors")
    year: Optional[int] = Field(default=None, description="Publication year")
    url: Optional[str] = Field(default=None, description="URL to the paper")
    citation_count: Optional[int] = Field(default=None, description="Number of citations")
    abstract: Optional[str] = Field(default=None, description="Paper abstract")


class AgentState(BaseModel):
    """State object for the LangGraph agent."""
    
    original_query: str = Field(description="Original user query")
    clarified_query: Optional[ClarifiedQuery] = Field(default=None, description="Clarified query object")
    papers: List[ResearchPaper] = Field(default_factory=list, description="List of fetched papers")
    output_file: Optional[str] = Field(default=None, description="Path to output markdown file")
    error: Optional[str] = Field(default=None, description="Error message if any")
    
    class Config:
        arbitrary_types_allowed = True
