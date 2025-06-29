# Hotel search and cost estimation
import requests
import json
from typing import List, Dict, Any, Optional
import random
from ..data.models import Hotel
from ..config.api_config import api_config

class HotelEstimator:
    """Service for finding hotels and estimating accommodation costs"""
    
    def __init__(self):
        self.api_key = api_config.GOOGLE_PLACES_API_KEY
        self.base_url = api_config.PLACES_BASE_URL
        self.session = requests.Session()
        
        # Base price ranges by budget category (per night in USD)
        self.budget_price_ranges = {
            'budget': {'min': 30, 'max': 80, 'avg': 50},
            'mid-range': {'min': 80, 'max': 200, 'avg': 130},
            'luxury': {'min': 200, 'max': 500, 'avg': 300}
        }
        
        # City price multipliers (adjust based on destination cost)
        self.city_multipliers = {
            'new york': 1.8,
            'london': 1.6,
            'paris': 1.5,
            'tokyo': 1.4,
            'sydney': 1.3,
            'dubai': 1.4,
            'singapore': 1.3,
            'default': 1.0
        }
    
    def find_hotels(self, trip_details: Dict[str, Any]) -> List[Hotel]:
        """Find hotels based on trip requirements"""
        try:
            hotels = []
            destination = trip_details['destination']
            budget_range = trip_details.get('budget_range', 'mid-range')
            
            # Try API search first
            if self.api_key:
                hotels_data = self._search_hotels_api(destination)
                hotels = self._process_hotels_data(hotels_data, trip_details)
            
            # Fallback to mock data if API fails
            if not hotels:
                hotels = self._generate_mock_hotels(trip_details)
            
            # Sort by rating and price appropriateness
            hotels = self._rank_hotels(hotels, budget_range)
            
            return hotels[:6]  # Return top 6 options
            
        except Exception as e:
            print(f"Error finding hotels: {e}")
            return self._generate_mock_hotels(trip_details)
    
    def _search_hotels_api(self, destination: str) -> List[Dict]:
        """Search for hotels using Google Places API"""
        try:
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': f'hotels in {destination}',
                'key': self.api_key,
                'type': 'lodging'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data.get('results', [])
            
        except Exception as e:
            print(f"Hotel API search failed: {e}")
            return []
    
    def _process_hotels_data(self, hotels_data: List[Dict], trip_details: Dict) -> List[Hotel]:
        """Process Google Places API response into Hotel objects"""
        hotels = []
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        for hotel_data in hotels_data:
            try:
                name = hotel_data.get('name', 'Unknown Hotel')
                rating = hotel_data.get('rating', 4.0)
                address = hotel_data.get('formatted_address', f'{destination} City Center')
                price_level = hotel_data.get('price_level', 2)
                
                # Estimate price per night
                price_per_night = self._estimate_hotel_price(destination, budget_range, price_level, rating)
                
                # Generate amenities based on price level and rating
                amenities = self._generate_amenities(price_level, rating)
                
                hotel = Hotel(
                    name=name,
                    rating=rating,
                    price_per_night=price_per_night,
                    address=address,
                    amenities=amenities
                )
                
                hotels.append(hotel)
                
            except Exception as e:
                print(f"Error processing hotel data: {e}")
                continue
        
        return hotels
    
    def _estimate_hotel_price(self, destination: str, budget_range: str, price_level: int, rating: float) -> float:
        """Estimate hotel price per night"""
        # Get base price range
        base_range = self.budget_price_ranges.get(budget_range, self.budget_price_ranges['mid-range'])
        base_price = base_range['avg']
        
        # Apply city multiplier
        city_key = destination.lower()
        multiplier = self.city_multipliers.get(city_key, self.city_multipliers['default'])
        
        # Adjust for price level (0-4 scale from Google Places)
        price_level_multipliers = {0: 0.6, 1: 0.8, 2: 1.0, 3: 1.3, 4: 1.8}
        price_multiplier = price_level_multipliers.get(price_level, 1.0)
        
        # Adjust for rating (higher rated hotels tend to be more expensive)
        if rating >= 4.5:
            rating_multiplier = 1.2
        elif rating >= 4.0:
            rating_multiplier = 1.1
        elif rating < 3.5:
            rating_multiplier = 0.9
        else:
            rating_multiplier = 1.0
        
        final_price = base_price * multiplier * price_multiplier * rating_multiplier
        
        # Add some randomness for variety
        final_price *= random.uniform(0.9, 1.1)
        
        return round(final_price, 2)
    
    def _generate_amenities(self, price_level: int, rating: float) -> List[str]:
        """Generate amenities based on price level and rating"""
        basic_amenities = ['Free WiFi', 'Air Conditioning', '24/7 Reception']
        
        mid_range_amenities = [
            'Restaurant', 'Room Service', 'Fitness Center', 'Business Center',
            'Laundry Service', 'Parking', 'Breakfast Included'
        ]
        
        luxury_amenities = [
            'Spa', 'Pool', 'Concierge Service', 'Airport Shuttle',
            'Multiple Restaurants', 'Bar/Lounge', 'Valet Parking',
            'Premium Bedding', 'Mini Bar', 'Balcony/View'
        ]
        
        amenities = basic_amenities.copy()
        
        if price_level >= 2:
            amenities.extend(random.sample(mid_range_amenities, min(4, len(mid_range_amenities))))
        
        if price_level >= 3 or rating >= 4.5:
            amenities.extend(random.sample(luxury_amenities, min(3, len(luxury_amenities))))
        
        return list(set(amenities))  # Remove duplicates
    
    def _generate_mock_hotels(self, trip_details: Dict) -> List[Hotel]:
        """Generate mock hotel data when API is unavailable"""
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        mock_hotels_data = [
            {
                'name': f'Grand {destination} Hotel',
                'rating': 4.5,
                'price_level': 3,
                'address': f'{destination} City Center'
            },
            {
                'name': f'{destination} Plaza',
                'rating': 4.3,
                'price_level': 3,
                'address': f'Downtown {destination}'
            },
            {
                'name': f'Budget Stay {destination}',
                'rating': 4.0,
                'price_level': 1,
                'address': f'{destination} Tourist District'
            },
            {
                'name': f'Comfort Inn {destination}',
                'rating': 4.1,
                'price_level': 2,
                'address': f'{destination} Central'
            },
            {
                'name': f'{destination} Luxury Resort',
                'rating': 4.7,
                'price_level': 4,
                'address': f'{destination} Premium District'
            },
            {
                'name': f'Business Hotel {destination}',
                'rating': 4.2,
                'price_level': 2,
                'address': f'{destination} Business District'
            },
            {
                'name': f'Boutique {destination}',
                'rating': 4.4,
                'price_level': 3,
                'address': f'{destination} Historic Quarter'
            },
            {
                'name': f'Extended Stay {destination}',
                'rating': 3.9,
                'price_level': 1,
                'address': f'{destination} Residential Area'
            }
        ]
        
        hotels = []
        for hotel_data in mock_hotels_data:
            price_per_night = self._estimate_hotel_price(
                destination, budget_range, hotel_data['price_level'], hotel_data['rating']
            )
            
            amenities = self._generate_amenities(hotel_data['price_level'], hotel_data['rating'])
            
            hotel = Hotel(
                name=hotel_data['name'],
                rating=hotel_data['rating'],
                price_per_night=price_per_night,
                address=hotel_data['address'],
                amenities=amenities
            )
            
            hotels.append(hotel)
        
        return hotels
    
    def _rank_hotels(self, hotels: List[Hotel], budget_range: str) -> List[Hotel]:
        """Rank hotels based on budget range and quality"""
        target_range = self.budget_price_ranges.get(budget_range, self.budget_price_ranges['mid-range'])
        
        scored_hotels = []
        for hotel in hotels:
            score = 0
            
            # Score based on rating
            score += hotel.rating * 10
            
            # Score based on price appropriateness for budget
            price_diff = abs(hotel.price_per_night - target_range['avg'])
            max_diff = target_range['max'] - target_range['min']
            price_score = max(0, 10 - (price_diff / max_diff * 10))
            score += price_score
            
            # Bonus for being within budget range
            if target_range['min'] <= hotel.price_per_night <= target_range['max']:
                score += 5
            
            # Bonus for good amenities
            score += len(hotel.amenities) * 0.5
            
            scored_hotels.append((hotel, score))
        
        # Sort by score (descending)
        scored_hotels.sort(key=lambda x: x[1], reverse=True)
        return [hotel for hotel, score in scored_hotels]
    
    def calculate_accommodation_cost(self, hotels: List[Hotel], nights: int, budget_range: str) -> Dict[str, Any]:
        """Calculate total accommodation costs"""
        if not hotels:
            return {'total_cost': 0, 'cost_per_night': 0, 'recommended_hotel': None}
        
        # Get the best hotel within budget
        target_range = self.budget_price_ranges.get(budget_range, self.budget_price_ranges['mid-range'])
        
        suitable_hotels = [h for h in hotels if target_range['min'] <= h.price_per_night <= target_range['max']]
        recommended_hotel = suitable_hotels[0] if suitable_hotels else hotels[0]
        
        total_cost = recommended_hotel.calculate_total_cost(nights)
        
        return {
            'total_cost': total_cost,
            'cost_per_night': recommended_hotel.price_per_night,
            'recommended_hotel': recommended_hotel,
            'alternatives': hotels[:3]  # Top 3 alternatives
        }
    
    def get_hotel_suggestions_by_group_size(self, hotels: List[Hotel], group_size: int) -> List[Dict[str, Any]]:
        """Suggest hotel arrangements based on group size"""
        suggestions = []
        
        for hotel in hotels[:3]:  # Top 3 hotels
            if group_size <= 2:
                # Single room
                arrangement = {
                    'hotel': hotel,
                    'rooms': 1,
                    'room_type': 'Double Room',
                    'total_per_night': hotel.price_per_night,
                    'cost_per_person': hotel.price_per_night / group_size
                }
            elif group_size <= 4:
                # Two rooms or suite
                arrangement = {
                    'hotel': hotel,
                    'rooms': 2,
                    'room_type': '2 Double Rooms',
                    'total_per_night': hotel.price_per_night * 2,
                    'cost_per_person': (hotel.price_per_night * 2) / group_size
                }
            else:
                # Multiple rooms
                rooms_needed = (group_size + 1) // 2  # 2 people per room
                arrangement = {
                    'hotel': hotel,
                    'rooms': rooms_needed,
                    'room_type': f'{rooms_needed} Double Rooms',
                    'total_per_night': hotel.price_per_night * rooms_needed,
                    'cost_per_person': (hotel.price_per_night * rooms_needed) / group_size
                }
            
            suggestions.append(arrangement)
        
        return suggestions