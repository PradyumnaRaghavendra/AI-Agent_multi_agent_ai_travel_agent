import requests
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from config.api_config import api_config
from data.models import Weather

class WeatherService:
    """Service for fetching weather data"""
    
    def __init__(self):
        self.api_key = api_config.OPENWEATHER_API_KEY
        self.base_url = api_config.WEATHER_BASE_URL
        self.session = requests.Session()
    
    def get_current_weather(self, city: str) -> Optional[Weather]:
        """Get current weather for a city"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return Weather(
                temperature=data['main']['temp'],
                description=data['weather'][0]['description'].title(),
                humidity=data['main']['humidity'],
                wind_speed=data['wind'].get('speed', 0),
                feels_like=data['main']['feels_like'],
                date=datetime.now().strftime('%Y-%m-%d')
            )
            
        except Exception as e:
            print(f"Error fetching current weather: {e}")
            return self._get_mock_weather()
    
    def get_weather_forecast(self, city: str, days: int = 5) -> List[Weather]:
        """Get weather forecast for multiple days"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(days * 8, 40)  # 8 forecasts per day (3-hour intervals), max 40
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            daily_forecasts = []
            processed_dates = set()
            
            for item in data['list']:
                date_str = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                
                if date_str not in processed_dates:
                    weather = Weather(
                        temperature=item['main']['temp'],
                        description=item['weather'][0]['description'].title(),
                        humidity=item['main']['humidity'],
                        wind_speed=item['wind'].get('speed', 0),
                        feels_like=item['main']['feels_like'],
                        date=date_str
                    )
                    daily_forecasts.append(weather)
                    processed_dates.add(date_str)
                
                if len(daily_forecasts) >= days:
                    break
            
            return daily_forecasts
            
        except Exception as e:
            print(f"Error fetching weather forecast: {e}")
            return self._get_mock_forecast(days)
    
    def _get_mock_weather(self) -> Weather:
        """Return mock weather data when API fails"""
        return Weather(
            temperature=22.0,
            description="Partly Cloudy",
            humidity=65,
            wind_speed=5.2,
            feels_like=24.0,
            date=datetime.now().strftime('%Y-%m-%d')
        )
    
    def _get_mock_forecast(self, days: int) -> List[Weather]:
        """Return mock forecast data when API fails"""
        forecasts = []
        base_date = datetime.now()
        
        for i in range(days):
            date_str = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
            temp = 20 + (i % 10)  # Varying temperature
            
            weather = Weather(
                temperature=float(temp),
                description=["Sunny", "Partly Cloudy", "Cloudy", "Light Rain"][i % 4],
                humidity=60 + (i % 20),
                wind_speed=3.0 + (i % 5),
                feels_like=float(temp + 2),
                date=date_str
            )
            forecasts.append(weather)
        
        return forecasts
    
    def get_weather_summary(self, forecasts: List[Weather]) -> Dict[str, Any]:
        """Generate weather summary for the trip"""
        if not forecasts:
            return {}
        
        temps = [w.temperature for w in forecasts]
        
        return {
            'avg_temperature': round(sum(temps) / len(temps), 1),
            'min_temperature': min(temps),
            'max_temperature': max(temps),
            'conditions': [w.description for w in forecasts],
            'rainy_days': len([w for w in forecasts if 'rain' in w.description.lower()]),
            'recommendations': self._get_weather_recommendations(forecasts)
        }
    
    def _get_weather_recommendations(self, forecasts: List[Weather]) -> List[str]:
        """Generate weather-based recommendations"""
        recommendations = []
        temps = [w.temperature for w in forecasts]
        avg_temp = sum(temps) / len(temps)
        
        if avg_temp < 10:
            recommendations.append("Pack warm clothes - it will be cold!")
        elif avg_temp > 30:
            recommendations.append("Pack light, breathable clothing - it will be hot!")
        
        rainy_days = len([w for w in forecasts if 'rain' in w.description.lower()])
        if rainy_days > 0:
            recommendations.append(f"Pack an umbrella - rain expected on {rainy_days} day(s)")
        
        if any(w.wind_speed > 10 for w in forecasts):
            recommendations.append("Expect windy conditions - secure loose items")
        
        return recommendations# Weather fetching logic
