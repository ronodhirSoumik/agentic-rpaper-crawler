from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import ClarifiedQuery
from llm_provider import LLMProviderProcessor, LLMConfig


class QueryClarifier:
    """Clarifies and structures research queries using configured LLM provider."""
    
    def __init__(
        self,
        provider: str = None,
        model_name: str = None,
        temperature: float = 0.3
    ):
        """
        Initialize the query clarifier.
        
        Args:
            provider: LLM provider ("openai", "deepseek", "openrouter", "gemini").
                     If None, reads from LLM_PROVIDER env variable.
            model_name: Model name to use (auto-selected based on provider if None).
            temperature: Temperature for generation.
        """
        # Get LLM configuration from processor
        self.config = LLMProviderProcessor.get_config(
            provider=provider,
            model_name=model_name,
            temperature=temperature
        )
        
        # Initialize LLM with configuration
        llm_kwargs = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "api_key": self.config.api_key
        }
        
        # Add base_url if specified (for DeepSeek, OpenRouter, Gemini)
        if self.config.base_url:
            llm_kwargs["base_url"] = self.config.base_url
        
        self.llm = ChatOpenAI(**llm_kwargs)
        
        # Log which provider is being used
        print(f"Using {self.config.provider.upper()} with model: {self.config.model_name}")
        
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
