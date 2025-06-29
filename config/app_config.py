"""Application configuration settings"""

# Application Settings
APP_NAME = "AI Travel Agent & Expense Planner"
VERSION = "1.0.0"

# Default Settings
DEFAULT_CURRENCY = "USD"
DEFAULT_BUDGET_RANGE = "mid-range"
DEFAULT_TRIP_DURATION = 7

# Limits and Constraints
MAX_TRIP_DURATION = 90  # days
MIN_TRIP_DURATION = 1   # day
MAX_GROUP_SIZE = 20
MIN_GROUP_SIZE = 1

# Results Limits
MAX_ATTRACTIONS = 10
MAX_RESTAURANTS = 8
MAX_ACTIVITIES = 6
MAX_HOTELS = 8

# Cache Settings
CACHE_DURATION_HOURS = 1
MAX_CACHE_SIZE = 100

# File Settings
OUTPUT_DIRECTORY = "trip_plans"
MAX_FILE_SIZE_MB = 10

# Display Settings
MAX_DISPLAY_ITEMS = 5
TRUNCATE_DESCRIPTION_LENGTH = 100

# Cost Estimation Settings
EMERGENCY_FUND_PERCENTAGE = 0.15  # 15% buffer
TAX_AND_FEES_PERCENTAGE = 0.08    # 8% for taxes and fees

# Weather Forecast Settings
MAX_FORECAST_DAYS = 16
WEATHER_UPDATE_INTERVAL_HOURS = 6

# Create app config object for imports
class AppConfig:
    DEFAULT_CURRENCY = DEFAULT_CURRENCY
    DEFAULT_BUDGET_RANGE = DEFAULT_BUDGET_RANGE
    MAX_ATTRACTIONS = MAX_ATTRACTIONS
    MAX_RESTAURANTS = MAX_RESTAURANTS
    MAX_ACTIVITIES = MAX_ACTIVITIES
    MAX_HOTELS = MAX_HOTELS

# Global instance for importing
app_config = AppConfig()