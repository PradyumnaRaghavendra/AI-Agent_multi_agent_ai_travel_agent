# Unit tests for weather module
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.weather_service import WeatherService
from data.models import Weather

class TestWeatherService(unittest.TestCase):
    """Test cases for WeatherService class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.weather_service = WeatherService()
    
    def test_create_mock_weather(self):
        """Test that mock weather is created correctly"""
        weather = self.weather_service._get_mock_weather()
        
        self.assertIsInstance(weather, Weather)
        self.assertIsInstance(weather.temperature, float)
        self.assertIsInstance(weather.description, str)
        self.assertGreater(weather.temperature, -50)
        self.assertLess(weather.temperature, 60)
    
    def test_weather_forecast_fallback(self):
        """Test weather forecast with fallback data"""
        forecast = self.weather_service._get_mock_forecast(5)
        
        self.assertIsInstance(forecast, list)
        self.assertEqual(len(forecast), 5)
        
        for weather in forecast:
            self.assertIsInstance(weather, Weather)

if __name__ == '__main__':
    unittest.main()
