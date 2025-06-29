"""API Configuration for external services"""
import os
from typing import Optional

# Weather API Configuration
OPENWEATHER_API_KEY: Optional[str] = os.getenv('OPENWEATHER_API_KEY')
WEATHER_BASE_URL: str = "http://api.openweathermap.org/data/2.5"

# Google Places API Configuration  
GOOGLE_PLACES_API_KEY: Optional[str] = os.getenv('GOOGLE_PLACES_API_KEY')
PLACES_BASE_URL: str = "https://maps.googleapis.com/maps/api/place"

# Currency Exchange API Configuration
EXCHANGERATE_API_KEY: Optional[str] = os.getenv('EXCHANGERATE_API_KEY')
EXCHANGE_RATE_URL: str = "https://api.exchangerate-api.com/v4/latest"

# Backup free APIs (no key required)
FREE_WEATHER_URL: str = "https://api.open-meteo.com/v1/forecast"
FREE_EXCHANGE_URL: str = "https://api.exchangerate-api.com/v4/latest"

def get_api_status() -> dict:
    """Check which APIs have valid keys"""
    return {
        'weather': bool(OPENWEATHER_API_KEY),
        'places': bool(GOOGLE_PLACES_API_KEY), 
        'exchange': bool(EXCHANGERATE_API_KEY)
    }

# Create API config object for imports
class APIConfig:
    OPENWEATHER_API_KEY = OPENWEATHER_API_KEY
    WEATHER_BASE_URL = WEATHER_BASE_URL
    GOOGLE_PLACES_API_KEY = GOOGLE_PLACES_API_KEY
    PLACES_BASE_URL = PLACES_BASE_URL
    EXCHANGERATE_API_KEY = EXCHANGERATE_API_KEY
    EXCHANGE_RATE_URL = EXCHANGE_RATE_URL

# Global instance for importing
api_config = APIConfig()