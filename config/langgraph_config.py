# LangGraph Multi-Agent Configuration
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class LangGraphConfig:
    """Configuration for LangGraph multi-agent system"""
    
    # Google Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = "gemini-2.0-flash"  # Using Gemini Flash 2.0
    
    # DuckDuckGo Search Configuration
    DUCKDUCKGO_MAX_RESULTS = 10
    DUCKDUCKGO_REGION = "us-en"
    DUCKDUCKGO_SAFESEARCH = "moderate"
    
    # Agent Configuration
    MAX_ITERATIONS = 50
    RECURSION_LIMIT = 100
    
    # Travel Planning Configuration
    WEATHER_SEARCH_ENABLED = True
    ATTRACTION_SEARCH_ENABLED = True
    HOTEL_SEARCH_ENABLED = True
    RESTAURANT_SEARCH_ENABLED = True
    
    # Model Parameters
    TEMPERATURE = 0.7
    MAX_TOKENS = 4000
    TOP_P = 0.9
    
    @classmethod
    def get_gemini_config(cls) -> Dict[str, Any]:
        """Get Gemini model configuration"""
        return {
            "model": cls.GEMINI_MODEL,
            "temperature": cls.TEMPERATURE,
            "max_output_tokens": cls.MAX_TOKENS,
            "top_p": cls.TOP_P,
        }
    
    @classmethod
    def get_search_config(cls) -> Dict[str, Any]:
        """Get DuckDuckGo search configuration"""
        return {
            "max_results": cls.DUCKDUCKGO_MAX_RESULTS,
            "region": cls.DUCKDUCKGO_REGION,
            "safesearch": cls.DUCKDUCKGO_SAFESEARCH,
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configurations are present"""
        if not cls.GEMINI_API_KEY:
            print("⚠️ Warning: GEMINI_API_KEY not found in environment variables")
            print("Please set GEMINI_API_KEY in your .env file")
            return False
        return True

# Initialize configuration
langgraph_config = LangGraphConfig()

# Validate configuration on import
if not langgraph_config.validate_config():
    print("❌ Configuration validation failed")
    print("Please check your .env file and ensure GEMINI_API_KEY is set")
else:
    print("✅ LangGraph configuration loaded successfully")
