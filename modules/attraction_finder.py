# Attractions, restaurants, activities
import requests
import json
from typing import List, Dict, Any, Optional
import random
from ..data.models import Attraction
from ..config.api_config import api_config
from ..config.app_config import app_config

class AttractionFinder:
    """Service for finding attractions, restaurants, and activities"""
    
    def __init__(self):
        self.api_key = api_config.GOOGLE_PLACES_API_KEY
        self.base_url = api_config.PLACES_BASE_URL
        self.session = requests.Session()
        
        # Price mapping for different budget ranges
        self.budget_price_mapping = {
            'budget': {'min': 0, 'max': 2, 'multiplier': 0.7},
            'mid-range': {'min': 1, 'max': 3, 'multiplier': 1.0},
            'luxury': {'min': 2, 'max': 4, 'multiplier': 1.5}
        }
        
        # Cost estimates for different types (base costs in USD)
        self.cost_estimates = {
            'attraction': {'budget': 15, 'mid-range': 25, 'luxury': 45},
            'restaurant': {'budget': 20, 'mid-range': 40, 'luxury': 80},
            'activity': {'budget': 30, 'mid-range': 60, 'luxury': 120}
        }
    
    def find_attractions(self, trip_details: Dict[str, Any]) -> List[Attraction]:
        """Find tourist attractions based on trip details"""
        try:
            attractions = []
            query = f"tourist attractions in {trip_details['destination']}"
            
            # Try API call first
            if self.api_key:
                places_data = self._search_places(query, 'tourist_attraction')
                attractions = self._process_places_data(places_data, 'attraction', trip_details)
            
            # Fallback to mock data if API fails or no key
            if not attractions:
                attractions = self._get_mock_attractions(trip_details)
            
            return attractions[:app_config.MAX_ATTRACTIONS]
            
        except Exception as e:
            print(f"Error finding attractions: {e}")
            return self._get_mock_attractions(trip_details)
    
    def find_restaurants(self, trip_details: Dict[str, Any]) -> List[Attraction]:
        """Find restaurants based on trip details"""
        try:
            restaurants = []
            query = f"restaurants in {trip_details['destination']}"
            
            # Try API call first
            if self.api_key:
                places_data = self._search_places(query, 'restaurant')
                restaurants = self._process_places_data(places_data, 'restaurant', trip_details)
            
            # Fallback to mock data
            if not restaurants:
                restaurants = self._get_mock_restaurants(trip_details)
            
            return restaurants[:app_config.MAX_RESTAURANTS]
            
        except Exception as e:
            print(f"Error finding restaurants: {e}")
            return self._get_mock_restaurants(trip_details)
    
    def find_activities(self, trip_details: Dict[str, Any]) -> List[Attraction]:
        """Find activities based on trip details and preferences"""
        try:
            activities = []
            
            # Build query based on preferences
            interests = trip_details.get('preferences', {}).get('interests', [])
            if interests:
                query = f"{' '.join(interests)} activities in {trip_details['destination']}"
            else:
                query = f"things to do activities in {trip_details['destination']}"
            
            # Try API call first
            if self.api_key:
                places_data = self._search_places(query, 'point_of_interest')
                activities = self._process_places_data(places_data, 'activity', trip_details)
            
            # Fallback to mock data
            if not activities:
                activities = self._get_mock_activities(trip_details)
            
            return activities[:app_config.MAX_ACTIVITIES]
            
        except Exception as e:
            print(f"Error finding activities: {e}")
            return self._get_mock_activities(trip_details)
    
    def _search_places(self, query: str, place_type: str) -> List[Dict]:
        """Search places using Google Places API"""
        try:
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': query,
                'key': self.api_key,
                'type': place_type
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data.get('results', [])
            
        except Exception as e:
            print(f"API search failed: {e}")
            return []
    
    def _process_places_data(self, places_data: List[Dict], place_type: str, trip_details: Dict) -> List[Attraction]:
        """Process Google Places API response into Attraction objects"""
        attractions = []
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        for place in places_data:
            try:
                # Extract basic information
                name = place.get('name', 'Unknown')
                rating = place.get('rating', 4.0)
                price_level = place.get('price_level', 2)
                address = place.get('formatted_address', 'Address not available')
                
                # Estimate cost based on type and budget
                estimated_cost = self._estimate_cost(place_type, budget_range, price_level)
                
                # Determine duration based on type
                duration = self._get_duration_by_type(place_type)
                
                attraction = Attraction(
                    name=name,
                    type=place_type,
                    rating=rating,
                    price_level=price_level,
                    address=address,
                    description=self._generate_description(place, place_type),
                    estimated_cost=estimated_cost,
                    duration=duration
                )
                
                attractions.append(attraction)
                
            except Exception as e:
                print(f"Error processing place data: {e}")
                continue
        
        return attractions
    
    def _estimate_cost(self, place_type: str, budget_range: str, price_level: int) -> float:
        """Estimate cost based on place type, budget range, and price level"""
        base_cost = self.cost_estimates.get(place_type, {}).get(budget_range, 30)
        
        # Adjust based on price level (0-4 scale from Google)
        price_multipliers = {0: 0.5, 1: 0.7, 2: 1.0, 3: 1.3, 4: 1.8}
        multiplier = price_multipliers.get(price_level, 1.0)
        
        return round(base_cost * multiplier, 2)
    
    def _get_duration_by_type(self, place_type: str) -> int:
        """Get typical duration in hours for different place types"""
        durations = {
            'attraction': 2,
            'restaurant': 1,
            'activity': 3
        }
        return durations.get(place_type, 2)
    
    def _generate_description(self, place: Dict, place_type: str) -> str:
        """Generate a description for the place"""
        types = place.get('types', [])
        rating = place.get('rating', 0)
        
        description_parts = []
        
        if rating >= 4.5:
            description_parts.append("Highly rated")
        elif rating >= 4.0:
            description_parts.append("Well-reviewed")
        
        if 'museum' in types:
            description_parts.append("cultural attraction")
        elif 'park' in types:
            description_parts.append("outdoor space")
        elif 'restaurant' in types:
            description_parts.append("dining establishment")
        elif 'shopping_mall' in types:
            description_parts.append("shopping destination")
        
        return " ".join(description_parts) if description_parts else f"Popular {place_type}"
    
    def _get_mock_attractions(self, trip_details: Dict) -> List[Attraction]:
        """Generate mock attraction data when API is unavailable"""
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        mock_attractions = [
            {
                'name': f'{destination} Historical Museum',
                'rating': 4.3,
                'price_level': 2,
                'description': 'Learn about local history and culture',
                'duration': 2
            },
            {
                'name': f'{destination} Central Park',
                'rating': 4.5,
                'price_level': 0,
                'description': 'Beautiful public park perfect for relaxation',
                'duration': 2
            },
            {
                'name': f'{destination} Art Gallery',
                'rating': 4.2,
                'price_level': 2,
                'description': 'Contemporary and classical art exhibitions',
                'duration': 2
            },
            {
                'name': f'{destination} Old Town District',
                'rating': 4.6,
                'price_level': 1,
                'description': 'Historic architecture and charming streets',
                'duration': 3
            },
            {
                'name': f'{destination} Observatory',
                'rating': 4.4,
                'price_level': 2,
                'description': 'Panoramic city views and astronomical exhibits',
                'duration': 2
            },
            {
                'name': f'{destination} Cultural Center',
                'rating': 4.1,
                'price_level': 2,
                'description': 'Local performances and cultural events',
                'duration': 2
            },
            {
                'name': f'{destination} Botanical Gardens',
                'rating': 4.7,
                'price_level': 1,
                'description': 'Diverse plant collections and peaceful walkways',
                'duration': 2
            },
            {
                'name': f'{destination} Waterfront Promenade',
                'rating': 4.5,
                'price_level': 0,
                'description': 'Scenic waterfront walks and recreational activities',
                'duration': 2
            }
        ]
        
        attractions = []
        for mock in mock_attractions:
            cost = self._estimate_cost('attraction', budget_range, mock['price_level'])
            
            attraction = Attraction(
                name=mock['name'],
                type='attraction',
                rating=mock['rating'],
                price_level=mock['price_level'],
                address=f"{destination} City Center",
                description=mock['description'],
                estimated_cost=cost,
                duration=mock['duration']
            )
            attractions.append(attraction)
        
        return attractions
    
    def _get_mock_restaurants(self, trip_details: Dict) -> List[Attraction]:
        """Generate mock restaurant data"""
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        mock_restaurants = [
            {
                'name': f'The Local Bistro - {destination}',
                'rating': 4.4,
                'price_level': 2,
                'description': 'Traditional local cuisine with modern twist'
            },
            {
                'name': f'{destination} Street Food Market',
                'rating': 4.2,
                'price_level': 1,
                'description': 'Authentic street food and local delicacies'
            },
            {
                'name': 'Fine Dining Restaurant',
                'rating': 4.6,
                'price_level': 3,
                'description': 'Upscale dining experience with seasonal menu'
            },
            {
                'name': 'Rooftop Cafe',
                'rating': 4.3,
                'price_level': 2,
                'description': 'Great views with coffee and light meals'
            },
            {
                'name': 'Family Restaurant',
                'rating': 4.1,
                'price_level': 2,
                'description': 'Comfortable atmosphere with international cuisine'
            },
            {
                'name': 'Vegetarian Haven',
                'rating': 4.5,
                'price_level': 2,
                'description': 'Plant-based cuisine with fresh local ingredients'
            },
            {
                'name': 'Seafood Speciality',
                'rating': 4.4,
                'price_level': 3,
                'description': 'Fresh seafood with harbor views'
            }
        ]
        
        restaurants = []
        for mock in mock_restaurants:
            cost = self._estimate_cost('restaurant', budget_range, mock['price_level'])
            
            restaurant = Attraction(
                name=mock['name'],
                type='restaurant',
                rating=mock['rating'],
                price_level=mock['price_level'],
                address=f"{destination} Downtown",
                description=mock['description'],
                estimated_cost=cost,
                duration=1
            )
            restaurants.append(restaurant)
        
        return restaurants
    
    def _get_mock_activities(self, trip_details: Dict) -> List[Attraction]:
        """Generate mock activity data"""
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        interests = trip_details.get('preferences', {}).get('interests', [])
        
        # Base activities
        mock_activities = [
            {
                'name': f'{destination} City Walking Tour',
                'rating': 4.3,
                'price_level': 1,
                'description': 'Guided tour of major landmarks and hidden gems',
                'duration': 3
            },
            {
                'name': 'Local Cooking Class',
                'rating': 4.6,
                'price_level': 2,
                'description': 'Learn to cook traditional dishes with local chef',
                'duration': 4
            },
            {
                'name': 'Bike Rental & City Tour',
                'rating': 4.2,
                'price_level': 2,
                'description': 'Explore the city on two wheels',
                'duration': 3
            },
            {
                'name': 'River Cruise',
                'rating': 4.4,
                'price_level': 2,
                'description': 'Scenic boat ride with city skyline views',
                'duration': 2
            },
            {
                'name': 'Adventure Sports Package',
                'rating': 4.5,
                'price_level': 3,
                'description': 'Thrilling outdoor activities and adventures',
                'duration': 4
            }
        ]
        
        # Add interest-specific activities
        if 'museums' in [i.lower() for i in interests]:
            mock_activities.append({
                'name': f'{destination} Museum Pass',
                'rating': 4.4,
                'price_level': 2,
                'description': 'Access to multiple museums and galleries',
                'duration': 4
            })
        
        if 'food' in [i.lower() for i in interests]:
            mock_activities.append({
                'name': 'Food & Wine Tasting Tour',
                'rating': 4.7,
                'price_level': 3,
                'description': 'Sample local wines and gourmet food',
                'duration': 3
            })
        
        if 'nightlife' in [i.lower() for i in interests]:
            mock_activities.append({
                'name': 'Evening Entertainment Package',
                'rating': 4.2,
                'price_level': 3,
                'description': 'Experience local nightlife and entertainment',
                'duration': 4
            })
        
        activities = []
        for mock in mock_activities:
            cost = self._estimate_cost('activity', budget_range, mock['price_level'])
            
            activity = Attraction(
                name=mock['name'],
                type='activity',
                rating=mock['rating'],
                price_level=mock['price_level'],
                address=f"{destination} Activity Center",
                description=mock['description'],
                estimated_cost=cost,
                duration=mock.get('duration', 3)
            )
            activities.append(activity)
        
        return activities
    
    def get_recommendations_by_interests(self, attractions: List[Attraction], interests: List[str]) -> List[Attraction]:
        """Filter and rank attractions based on user interests"""
        if not interests:
            return attractions
        
        scored_attractions = []
        interest_keywords = [interest.lower() for interest in interests]
        
        for attraction in attractions:
            score = 0
            attraction_text = f"{attraction.name} {attraction.description}".lower()
            
            # Score based on keyword matches
            for keyword in interest_keywords:
                if keyword in attraction_text:
                    score += 2
                
                # Bonus for exact matches in name
                if keyword in attraction.name.lower():
                    score += 1
            
            # Bonus for high ratings
            if attraction.rating >= 4.5:
                score += 1
            elif attraction.rating >= 4.0:
                score += 0.5
            
            scored_attractions.append((attraction, score))
        
        # Sort by score (descending) and return attractions
        scored_attractions.sort(key=lambda x: x[1], reverse=True)
        return [attraction for attraction, score in scored_attractions]