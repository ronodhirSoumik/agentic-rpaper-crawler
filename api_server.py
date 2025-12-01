from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent import ResearchAgent
from models import AgentState
from typing import Optional
import uvicorn


app = FastAPI(
    title="AI Research Agent API",
    description="API for the LangGraph-based research agent that fetches papers from Google Scholar",
    version="1.0.0"
)


class ResearchRequest(BaseModel):
    """Request model for research queries."""
    query: str = Field(..., description="The research query to process", min_length=3)
    max_papers: Optional[int] = Field(default=10, description="Maximum number of papers to fetch", ge=1, le=50)
    provider: Optional[str] = Field(default=None, description="LLM provider: 'openai' or 'deepseek' (defaults to env LLM_PROVIDER)")


class ResearchResponse(BaseModel):
    """Response model for research results."""
    success: bool
    message: str
    output_file: Optional[str] = None
    papers_found: int = 0
    clarified_query: Optional[str] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AI Research Agent API",
        "version": "1.0.0",
        "endpoints": {
            "POST /research": "Submit a research query",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    """
    Process a research query and fetch relevant papers.
    
    Args:
        request: ResearchRequest with query and optional max_papers
        
    Returns:
        ResearchResponse with results and output file path
    """
    try:
        # Create and run the agent
        agent = ResearchAgent(max_papers=request.max_papers, provider=request.provider)
        result = agent.run(request.query)
        
        # Check for errors
        if result.get("error"):
            return ResearchResponse(
                success=False,
                message="Research completed with errors",
                error=result["error"]
            )
        
        # Success response
        return ResearchResponse(
            success=True,
            message="Research completed successfully",
            output_file=result.get("output_file"),
            papers_found=len(result.get("papers", [])),
            clarified_query=result.get("clarified_query").clarified_query if result.get("clarified_query") else None
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting AI Research Agent API Server")
    print("="*60)
    print("\nAPI Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("\nExample usage:")
    print('curl -X POST "http://localhost:8000/research" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"query": "machine learning for climate change"}\'')
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
