"""Data models for the AI Travel Agent"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import date, datetime

@dataclass
class Weather:
    """Weather information for a specific day"""
    temperature: float  # in Celsius
    description: str
    humidity: int  # percentage
    wind_speed: float  # km/h
    feels_like: float  # in Celsius
    date: str  # YYYY-MM-DD format
    
    def __str__(self) -> str:
        return f"{self.description}, {self.temperature}°C (feels like {self.feels_like}°C)"

@dataclass  
class Attraction:
    """Tourist attraction, restaurant, or activity"""
    name: str
    type: str  # 'attraction', 'restaurant', 'activity'
    rating: float  # 1-5 scale
    price_level: int  # 0-4 scale (Google Places style)
    address: str
    description: str
    estimated_cost: float  # in USD
    duration: int  # hours
    
    def __str__(self) -> str:
        return f"{self.name} ({self.rating}⭐) - ${self.estimated_cost}"

@dataclass
class Hotel:
    """Hotel accommodation option"""
    name: str
    rating: float  # 1-5 scale
    price_per_night: float  # in USD
    address: str
    amenities: List[str]
    
    def calculate_total_cost(self, nights: int) -> float:
        """Calculate total cost for given number of nights"""
        return self.price_per_night * nights
    
    def __str__(self) -> str:
        return f"{self.name} ({self.rating}⭐) - ${self.price_per_night}/night"

@dataclass
class Transportation:
    """Transportation option between locations"""
    mode: str  # 'Walking', 'Public Transport', 'Taxi', 'Uber', etc.
    estimated_cost: float  # in USD
    duration: int  # minutes
    
    def __str__(self) -> str:
        return f"{self.mode} - ${self.estimated_cost} ({self.duration} min)"

@dataclass
class DayPlan:
    """Complete plan for a single day"""
    day: int
    date: str  # YYYY-MM-DD format
    weather: Weather
    attractions: List[Attraction] = None
    restaurants: List[Attraction] = None
    activities: List[Attraction] = None
    transportation: List[Transportation] = None
    daily_cost: float = 0.0
    
    def __post_init__(self):
        """Initialize empty lists if None"""
        if self.attractions is None:
            self.attractions = []
        if self.restaurants is None:
            self.restaurants = []
        if self.activities is None:
            self.activities = []
        if self.transportation is None:
            self.transportation = []
    
    def get_total_activities(self) -> int:
        """Get total number of planned activities for the day"""
        return len(self.attractions) + len(self.restaurants) + len(self.activities)
    
    def __str__(self) -> str:
        return f"Day {self.day} ({self.date}) - {self.get_total_activities()} activities, ${self.daily_cost}"

@dataclass
class TripSummary:
    """Complete trip summary with all details"""
    destination: str
    start_date: date
    end_date: date
    total_days: int
    total_cost: float
    daily_budget: float
    currency: str
    converted_total: float
    itinerary: List[DayPlan]
    hotels: List[Hotel]
    
    # Additional summary data (added by TripSummaryGenerator)
    trip_overview: Dict[str, Any] = None
    weather_summary: Dict[str, Any] = None
    accommodation_summary: Dict[str, Any] = None
    expense_summary: Dict[str, Any] = None
    itinerary_highlights: Dict[str, Any] = None
    recommendations: Dict[str, Any] = None
    travel_tips: List[str] = None
    
    def __post_init__(self):
        """Initialize empty dictionaries/lists if None"""
        if self.trip_overview is None:
            self.trip_overview = {}
        if self.weather_summary is None:
            self.weather_summary = {}
        if self.accommodation_summary is None:
            self.accommodation_summary = {}
        if self.expense_summary is None:
            self.expense_summary = {}
        if self.itinerary_highlights is None:
            self.itinerary_highlights = {}
        if self.recommendations is None:
            self.recommendations = {}
        if self.travel_tips is None:
            self.travel_tips = []
    
    def get_cost_per_person(self, group_size: int) -> float:
        """Calculate cost per person"""
        return self.converted_total / group_size if group_size > 0 else self.converted_total
    
    def get_average_daily_cost(self) -> float:
        """Calculate average daily cost"""
        return self.converted_total / self.total_days if self.total_days > 0 else 0.0
    
    def __str__(self) -> str:
        return f"Trip to {self.destination} ({self.total_days} days) - {self.currency} {self.converted_total:.2f}"

# Utility functions for model creation
def create_mock_weather(temperature: float = 22.0, description: str = "Partly Cloudy", date_str: str = None) -> Weather:
    """Create a mock weather object for testing"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    return Weather(
        temperature=temperature,
        description=description,
        humidity=65,
        wind_speed=10.0,
        feels_like=temperature + 2,
        date=date_str
    )

def create_mock_attraction(name: str = "Sample Attraction", attraction_type: str = "attraction") -> Attraction:
    """Create a mock attraction for testing"""
    return Attraction(
        name=name,
        type=attraction_type,
        rating=4.2,
        price_level=2,
        address="Sample Address",
        description="Sample description",
        estimated_cost=25.0,
        duration=2
    )

def create_mock_hotel(name: str = "Sample Hotel") -> Hotel:
    """Create a mock hotel for testing"""
    return Hotel(
        name=name,
        rating=4.0,
        price_per_night=100.0,
        address="Sample Hotel Address",
        amenities=["WiFi", "Breakfast", "Pool"]
    )