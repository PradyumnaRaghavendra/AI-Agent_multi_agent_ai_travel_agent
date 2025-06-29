# LangGraph Agent Tools
import asyncio
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from duckduckgo_search import DDGS
import json
import re
from datetime import datetime
from config.langgraph_config import langgraph_config as config

class TravelAgentTools:
    """Collection of tools for the LangGraph travel agents"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,
            google_api_key=config.GEMINI_API_KEY,
            temperature=config.TEMPERATURE,
            max_output_tokens=config.MAX_TOKENS,
            top_p=config.TOP_P,
        )
        self.search_config = config.get_search_config()
    
    @tool
    def search_destination_info(query: str) -> str:
        """Search for destination information using DuckDuckGo"""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query + " travel destination guide attractions",
                    max_results=config.DUCKDUCKGO_MAX_RESULTS,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No search results found for destination: {query}"
                
                # Format results for agent consumption
                formatted_results = []
                for i, result in enumerate(results[:5], 1):
                    formatted_results.append(
                        f"{i}. {result.get('title', 'No title')}\n"
                        f"   {result.get('body', 'No description')}\n"
                        f"   Source: {result.get('href', 'No URL')}\n"
                    )
                
                return "\n".join(formatted_results)
        except Exception as e:
            return f"Error searching for destination info: {str(e)}"
    
    @tool
    def search_weather_info(destination: str, dates: str = "") -> str:
        """Search for weather information for a destination"""
        try:
            weather_query = f"{destination} weather forecast {dates} travel climate"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    weather_query,
                    max_results=5,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No weather information found for {destination}"
                
                weather_info = []
                for result in results[:3]:
                    weather_info.append(
                        f"• {result.get('title', 'Weather Info')}\n"
                        f"  {result.get('body', 'No details available')}\n"
                    )
                
                return f"Weather information for {destination}:\n" + "\n".join(weather_info)
        except Exception as e:
            return f"Error searching weather info: {str(e)}"
    
    @tool
    def search_attractions(destination: str, interests: str = "") -> str:
        """Search for attractions and activities in a destination"""
        try:
            attraction_query = f"{destination} top attractions activities {interests} must visit places"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    attraction_query,
                    max_results=8,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No attractions found for {destination}"
                
                attractions = []
                for i, result in enumerate(results[:6], 1):
                    attractions.append(
                        f"{i}. {result.get('title', 'Attraction')}\n"
                        f"   {result.get('body', 'No description')[:200]}...\n"
                    )
                
                return f"Top attractions in {destination}:\n" + "\n".join(attractions)
        except Exception as e:
            return f"Error searching attractions: {str(e)}"
    
    @tool
    def search_hotels(destination: str, budget: str = "mid-range") -> str:
        """Search for hotel information and pricing"""
        try:
            hotel_query = f"{destination} hotels {budget} best places to stay accommodation"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    hotel_query,
                    max_results=6,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No hotel information found for {destination}"
                
                hotels = []
                for i, result in enumerate(results[:4], 1):
                    hotels.append(
                        f"{i}. {result.get('title', 'Hotel')}\n"
                        f"   {result.get('body', 'No details')[:180]}...\n"
                    )
                
                return f"Hotel options in {destination} ({budget} budget):\n" + "\n".join(hotels)
        except Exception as e:
            return f"Error searching hotels: {str(e)}"
    
    @tool
    def search_restaurants(destination: str, cuisine: str = "") -> str:
        """Search for restaurants and dining options"""
        try:
            restaurant_query = f"{destination} best restaurants {cuisine} local food dining where to eat"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    restaurant_query,
                    max_results=6,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No restaurant information found for {destination}"
                
                restaurants = []
                for i, result in enumerate(results[:4], 1):
                    restaurants.append(
                        f"{i}. {result.get('title', 'Restaurant')}\n"
                        f"   {result.get('body', 'No details')[:180]}...\n"
                    )
                
                return f"Restaurant recommendations in {destination}:\n" + "\n".join(restaurants)
        except Exception as e:
            return f"Error searching restaurants: {str(e)}"
    
    @tool
    def search_local_tips(destination: str) -> str:
        """Search for local tips, culture, and insider information"""
        try:
            tips_query = f"{destination} local tips insider guide cultural etiquette what to know"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    tips_query,
                    max_results=5,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No local tips found for {destination}"
                
                tips = []
                for result in results[:3]:
                    tips.append(
                        f"• {result.get('title', 'Local Tip')}\n"
                        f"  {result.get('body', 'No details')[:200]}...\n"
                    )
                
                return f"Local tips for {destination}:\n" + "\n".join(tips)
        except Exception as e:
            return f"Error searching local tips: {str(e)}"
    
    @tool
    def search_budget_info(destination: str, duration: str = "") -> str:
        """Search for budget and cost information"""
        try:
            budget_query = f"{destination} travel budget cost daily expenses {duration} how much money"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    budget_query,
                    max_results=5,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No budget information found for {destination}"
                
                budget_info = []
                for result in results[:3]:
                    budget_info.append(
                        f"• {result.get('title', 'Budget Info')}\n"
                        f"  {result.get('body', 'No details')[:200]}...\n"
                    )
                
                return f"Budget information for {destination}:\n" + "\n".join(budget_info)
        except Exception as e:
            return f"Error searching budget info: {str(e)}"

# Create global tools instance
travel_tools = TravelAgentTools()

# Export individual tools for LangGraph
search_destination_info = travel_tools.search_destination_info
search_weather_info = travel_tools.search_weather_info
search_attractions = travel_tools.search_attractions
search_hotels = travel_tools.search_hotels
search_restaurants = travel_tools.search_restaurants
search_local_tips = travel_tools.search_local_tips
search_budget_info = travel_tools.search_budget_info

# List of all available tools
ALL_TOOLS = [
    search_destination_info,
    search_weather_info,
    search_attractions,
    search_hotels,
    search_restaurants,
    search_local_tips,
    search_budget_info
]
