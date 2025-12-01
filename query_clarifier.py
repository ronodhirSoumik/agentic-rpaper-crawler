from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import ClarifiedQuery
import os
from dotenv import load_dotenv

load_dotenv()


class QueryClarifier:
    """Clarifies and structures research queries using OpenAI or DeepSeek."""
    
    def __init__(self, model_name: str = None, temperature: float = 0.3, provider: str = None):
        """
        Initialize the query clarifier.
        
        Args:
            model_name: Model name to use (auto-selected based on provider if None)
            temperature: Temperature for generation
            provider: LLM provider ("openai" or "deepseek"). If None, reads from LLM_PROVIDER env var
        """
        # Determine provider
        if provider is None:
            provider = os.getenv("LLM_PROVIDER", "openai").lower()
        
        self.provider = provider
        
        # Set default model based on provider
        if model_name is None:
            if provider == "deepseek":
                model_name = "deepseek-chat"
            else:
                model_name = "gpt-4o-mini"
        
        # Initialize LLM based on provider
        if provider == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
            
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=temperature,
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            print(f"🤖 Using DeepSeek API with model: {model_name}")
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=temperature,
                api_key=api_key
            )
            print(f"🤖 Using OpenAI API with model: {model_name}")
        
        self.parser = PydanticOutputParser(pydantic_object=ClarifiedQuery)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert research assistant specializing in clarifying and structuring academic research queries.
            
Your task is to:
1. Understand the user's research intent
2. Clarify ambiguous terms and concepts
3. Extract key concepts and research domains
4. Generate optimized search terms for academic databases like Google Scholar

{format_instructions}"""),
            ("user", "Research Query: {query}")
        ])
    
    def clarify(self, query: str) -> ClarifiedQuery:
        """
        Clarify and structure a research query.
        
        Args:
            query: The original research query from the user
            
        Returns:
            ClarifiedQuery object with structured information
        """
        chain = self.prompt | self.llm | self.parser
        
        result = chain.invoke({
            "query": query,
            "format_instructions": self.parser.get_format_instructions()
        })
        
        return result


if __name__ == "__main__":
    # Test the query clarifier
    clarifier = QueryClarifier()
    
    test_query = "machine learning for climate change"
    result = clarifier.clarify(test_query)
    
    print("Original Query:", result.original_query)
    print("Clarified Query:", result.clarified_query)
    print("Key Concepts:", result.key_concepts)
    print("Search Terms:", result.search_terms)
    print("Research Domain:", result.research_domain)
