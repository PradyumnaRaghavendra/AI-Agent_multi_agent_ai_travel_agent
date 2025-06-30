# Itinerary planning logic
import random
from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from data.models import DayPlan, Weather, Attraction, Transportation

class ItineraryPlanner:
    """Service for creating detailed day-by-day itineraries"""
    
    def __init__(self):
        # Activity timing preferences
        self.activity_timings = {
            'morning': {'start': 9, 'end': 12, 'activities': ['museums', 'galleries', 'parks', 'sightseeing']},
            'afternoon': {'start': 13, 'end': 17, 'activities': ['activities', 'shopping', 'tours', 'attractions']},
            'evening': {'start': 18, 'end': 21, 'activities': ['dining', 'entertainment', 'nightlife', 'cultural']}
        }
        
        # Weather-based activity recommendations
        self.weather_activities = {
            'sunny': ['outdoor tours', 'parks', 'walking tours', 'outdoor activities'],
            'rainy': ['museums', 'galleries', 'shopping', 'indoor attractions'],
            'cloudy': ['sightseeing', 'cultural sites', 'mixed activities'],
            'cold': ['indoor attractions', 'museums', 'warm cafes', 'shopping'],
            'hot': ['indoor attractions', 'early morning tours', 'evening activities']
        }
        
        # Transportation estimates between activities
        self.transport_estimates = {
            'walking': {'cost': 0, 'time': 15},
            'public_transport': {'cost': 3, 'time': 20},
            'taxi': {'cost': 12, 'time': 15},
            'uber': {'cost': 10, 'time': 12}
        }
    
    def create_itinerary(self, trip_details: Dict[str, Any], weather_data: List[Weather], 
                        attractions: List[Attraction], restaurants: List[Attraction], 
                        activities: List[Attraction]) -> List[DayPlan]:
        """Create complete day-by-day itinerary"""
        
        total_days = trip_details['total_days']
        start_date = trip_details['start_date']
        budget_range = trip_details.get('budget_range', 'mid-range')
        group_size = trip_details.get('group_size', 1)
        interests = trip_details.get('preferences', {}).get('interests', [])
        
        itinerary = []
        
        # Distribute attractions, restaurants, and activities across days
        daily_attractions = self._distribute_items_across_days(attractions, total_days, 2)
        daily_restaurants = self._distribute_items_across_days(restaurants, total_days, 2)
        daily_activities = self._distribute_items_across_days(activities, total_days, 1)
        
        for day_num in range(1, total_days + 1):
            current_date = start_date + timedelta(days=day_num - 1)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Get weather for this day
            day_weather = self._get_weather_for_day(weather_data, day_num - 1)
            
            # Create day plan
            day_plan = DayPlan(
                day=day_num,
                date=date_str,
                weather=day_weather
            )
            
            # Add attractions for the day
            if day_num <= len(daily_attractions):
                day_plan.attractions = daily_attractions[day_num - 1]
            
            # Add restaurants for the day
            if day_num <= len(daily_restaurants):
                day_plan.restaurants = daily_restaurants[day_num - 1]
            
            # Add activities for the day
            if day_num <= len(daily_activities):
                day_plan.activities = daily_activities[day_num - 1]
            
            # Optimize schedule based on weather and interests
            day_plan = self._optimize_day_schedule(day_plan, interests, budget_range)
            
            # Add transportation between activities
            day_plan.transportation = self._plan_transportation(day_plan, budget_range)
            
            # Calculate daily costs
            day_plan.daily_cost = self._calculate_daily_cost(day_plan, group_size)
            
            itinerary.append(day_plan)
        
        # Balance the itinerary across days
        itinerary = self._balance_itinerary(itinerary, total_days)
        
        return itinerary
    
    def _distribute_items_across_days(self, items: List[Attraction], total_days: int, items_per_day: int) -> List[List[Attraction]]:
        """Distribute attractions/restaurants/activities across days"""
        if not items:
            return [[] for _ in range(total_days)]
        
        # Sort items by rating (best first)
        sorted_items = sorted(items, key=lambda x: x.rating, reverse=True)
        
        daily_items = []
        for day in range(total_days):
            start_idx = day * items_per_day
            end_idx = start_idx + items_per_day
            day_items = sorted_items[start_idx:end_idx]
            daily_items.append(day_items)
        
        return daily_items
    
    def _get_weather_for_day(self, weather_data: List[Weather], day_index: int) -> Weather:
        """Get weather data for specific day"""
        if day_index < len(weather_data):
            return weather_data[day_index]
        
        # Fallback weather if not enough data
        return Weather(
            temperature=22.0,
            description="Partly Cloudy",
            humidity=65,
            wind_speed=5.0,
            feels_like=24.0,
            date=(datetime.now() + timedelta(days=day_index)).strftime('%Y-%m-%d')
        )
    
    def _optimize_day_schedule(self, day_plan: DayPlan, interests: List[str], budget_range: str) -> DayPlan:
        """Optimize daily schedule based on weather and preferences"""
        
        # Get weather condition category
        weather_condition = self._categorize_weather(day_plan.weather)
        
        # Reorder activities based on weather
        if weather_condition == 'rainy':
            # Prioritize indoor activities
            day_plan.attractions = self._prioritize_indoor_activities(day_plan.attractions)
            day_plan.activities = self._prioritize_indoor_activities(day_plan.activities)
        elif weather_condition == 'sunny':
            # Prioritize outdoor activities
            day_plan.attractions = self._prioritize_outdoor_activities(day_plan.attractions)
            day_plan.activities = self._prioritize_outdoor_activities(day_plan.activities)
        
        # Add timing recommendations
        day_plan = self._add_timing_recommendations(day_plan)
        
        # Add weather-specific recommendations
        day_plan = self._add_weather_recommendations(day_plan, weather_condition)
        
        return day_plan
    
    def _categorize_weather(self, weather: Weather) -> str:
        """Categorize weather condition"""
        description = weather.description.lower()
        temp = weather.temperature
        
        if 'rain' in description or 'storm' in description:
            return 'rainy'
        elif temp < 10:
            return 'cold'
        elif temp > 30:
            return 'hot'
        elif 'sun' in description or 'clear' in description:
            return 'sunny'
        else:
            return 'cloudy'
    
    def _prioritize_indoor_activities(self, activities: List[Attraction]) -> List[Attraction]:
        """Prioritize indoor activities for bad weather"""
        indoor_keywords = ['museum', 'gallery', 'mall', 'center', 'indoor', 'theater', 'cinema']
        
        indoor_activities = []
        outdoor_activities = []
        
        for activity in activities:
            is_indoor = any(keyword in activity.name.lower() or keyword in activity.description.lower() 
                          for keyword in indoor_keywords)
            
            if is_indoor:
                indoor_activities.append(activity)
            else:
                outdoor_activities.append(activity)
        
        return indoor_activities + outdoor_activities
    
    def _prioritize_outdoor_activities(self, activities: List[Attraction]) -> List[Attraction]:
        """Prioritize outdoor activities for good weather"""
        outdoor_keywords = ['park', 'garden', 'tour', 'walk', 'outdoor', 'beach', 'view', 'nature']
        
        outdoor_activities = []
        indoor_activities = []
        
        for activity in activities:
            is_outdoor = any(keyword in activity.name.lower() or keyword in activity.description.lower() 
                           for keyword in outdoor_keywords)
            
            if is_outdoor:
                outdoor_activities.append(activity)
            else:
                indoor_activities.append(activity)
        
        return outdoor_activities + indoor_activities
    
    def _add_timing_recommendations(self, day_plan: DayPlan) -> DayPlan:
        """Add timing recommendations for activities"""
        
        # Add timing attributes to activities
        for i, attraction in enumerate(day_plan.attractions):
            if i == 0:
                attraction.recommended_time = "9:00 AM - 11:00 AM"
                attraction.time_slot = "morning"
            else:
                attraction.recommended_time = "2:00 PM - 4:00 PM"
                attraction.time_slot = "afternoon"
        
        for activity in day_plan.activities:
            activity.recommended_time = "10:00 AM - 1:00 PM"
            activity.time_slot = "morning-afternoon"
        
        for i, restaurant in enumerate(day_plan.restaurants):
            if i == 0:
                restaurant.recommended_time = "12:00 PM - 1:30 PM"
                restaurant.time_slot = "lunch"
            else:
                restaurant.recommended_time = "7:00 PM - 9:00 PM"
                restaurant.time_slot = "dinner"
        
        return day_plan
    
    def _add_weather_recommendations(self, day_plan: DayPlan, weather_condition: str) -> DayPlan:
        """Add weather-specific recommendations"""
        recommendations = []
        
        if weather_condition == 'rainy':
            recommendations.extend([
                "Carry an umbrella or raincoat",
                "Focus on indoor attractions today",
                "Consider museum hopping",
                "Perfect day for shopping centers"
            ])
        elif weather_condition == 'sunny':
            recommendations.extend([
                "Great day for outdoor activities",
                "Don't forget sunscreen and water",
                "Perfect for walking tours",
                "Consider outdoor dining"
            ])
        elif weather_condition == 'cold':
            recommendations.extend([
                "Dress warmly in layers",
                "Indoor attractions recommended",
                "Hot drinks and warm cafes",
                "Shorter outdoor activities"
            ])
        elif weather_condition == 'hot':
            recommendations.extend([
                "Stay hydrated and seek shade",
                "Plan indoor activities during peak heat",
                "Early morning or evening outdoor activities",
                "Air-conditioned venues recommended"
            ])
        
        # Add recommendations as an attribute to the day plan
        if not hasattr(day_plan, 'recommendations'):
            day_plan.recommendations = []
        day_plan.recommendations.extend(recommendations)
        
        return day_plan
    
    def _plan_transportation(self, day_plan: DayPlan, budget_range: str) -> List[Transportation]:
        """Plan transportation between activities"""
        transportation = []
        
        # Count total activities for the day
        total_activities = len(day_plan.attractions) + len(day_plan.activities) + len(day_plan.restaurants)
        
        if total_activities <= 1:
            return transportation
        
        # Determine transport mode based on budget
        transport_modes = {
            'budget': ['walking', 'public_transport'],
            'mid-range': ['walking', 'public_transport', 'uber'],
            'luxury': ['taxi', 'uber', 'public_transport']
        }
        
        available_modes = transport_modes.get(budget_range, ['public_transport', 'walking'])
        
        # Create transportation entries between activities
        for i in range(total_activities - 1):
            mode = random.choice(available_modes)
            transport_info = self.transport_estimates[mode]
            
            transport = Transportation(
                mode=mode.replace('_', ' ').title(),
                estimated_cost=transport_info['cost'],
                duration=transport_info['time']
            )
            transportation.append(transport)
        
        return transportation
    
    def _calculate_daily_cost(self, day_plan: DayPlan, group_size: int) -> float:
        """Calculate total cost for the day"""
        total_cost = 0.0
        
        # Add attraction costs
        for attraction in day_plan.attractions:
            total_cost += attraction.estimated_cost * group_size
        
        # Add restaurant costs
        for restaurant in day_plan.restaurants:
            total_cost += restaurant.estimated_cost * group_size
        
        # Add activity costs
        for activity in day_plan.activities:
            total_cost += activity.estimated_cost * group_size
        
        # Add transportation costs
        for transport in day_plan.transportation:
            total_cost += transport.estimated_cost * group_size
        
        return round(total_cost, 2)
    
    def _balance_itinerary(self, itinerary: List[DayPlan], total_days: int) -> List[DayPlan]:
        """Balance activities across days to avoid overloading"""
        
        # Calculate average activities per day
        total_attractions = sum(len(day.attractions) for day in itinerary)
        total_activities = sum(len(day.activities) for day in itinerary)
        
        target_attractions_per_day = max(1, total_attractions // total_days)
        target_activities_per_day = max(1, total_activities // total_days)
        
        # Redistribute if any day is heavily overloaded
        for i, day_plan in enumerate(itinerary):
            if len(day_plan.attractions) > target_attractions_per_day + 1:
                # Move excess attractions to less busy days
                excess = day_plan.attractions[target_attractions_per_day:]
                day_plan.attractions = day_plan.attractions[:target_attractions_per_day]
                
                # Find days with fewer attractions
                for j, other_day in enumerate(itinerary):
                    if j != i and len(other_day.attractions) < target_attractions_per_day and excess:
                        other_day.attractions.append(excess.pop(0))
            
            # Recalculate daily cost after rebalancing
            day_plan.daily_cost = self._calculate_daily_cost(day_plan, 1)  # Will be multiplied by group size later
        
        return itinerary
    
    def generate_itinerary_summary(self, itinerary: List[DayPlan]) -> Dict[str, Any]:
        """Generate summary of the complete itinerary"""
        
        total_attractions = sum(len(day.attractions) for day in itinerary)
        total_restaurants = sum(len(day.restaurants) for day in itinerary)
        total_activities = sum(len(day.activities) for day in itinerary)
        total_cost = sum(day.daily_cost for day in itinerary)
        
        # Find best rated activities
        all_items = []
        for day in itinerary:
            all_items.extend(day.attractions + day.restaurants + day.activities)
        
        top_rated = sorted(all_items, key=lambda x: x.rating, reverse=True)[:5]
        
        # Weather overview
        weather_conditions = [day.weather.description for day in itinerary]
        
        summary = {
            'total_days': len(itinerary),
            'total_attractions': total_attractions,
            'total_restaurants': total_restaurants,
            'total_activities': total_activities,
            'estimated_total_cost': round(total_cost, 2),
            'average_daily_cost': round(total_cost / len(itinerary), 2) if itinerary else 0,
            'top_rated_experiences': [
                {
                    'name': item.name,
                    'type': item.type,
                    'rating': item.rating,
                    'cost': item.estimated_cost
                } for item in top_rated
            ],
            'weather_overview': {
                'conditions': weather_conditions,
                'rainy_days': len([w for w in weather_conditions if 'rain' in w.lower()]),
                'sunny_days': len([w for w in weather_conditions if 'sun' in w.lower() or 'clear' in w.lower()])
            },
            'daily_highlights': [
                {
                    'day': day.day,
                    'date': day.date,
                    'weather': day.weather.description,
                    'main_attractions': [a.name for a in day.attractions[:2]],
                    'main_activity': day.activities[0].name if day.activities else None,
                    'cost': day.daily_cost
                } for day in itinerary
            ]
        }
        
        return summary
    
    def export_itinerary_to_text(self, itinerary: List[DayPlan], trip_details: Dict[str, Any]) -> str:
        """Export itinerary to formatted text"""
        
        text_output = []
        text_output.append("=" * 60)
        text_output.append(f"TRAVEL ITINERARY - {trip_details['destination'].upper()}")
        text_output.append("=" * 60)
        text_output.append(f"Duration: {len(itinerary)} days")
        text_output.append(f"Dates: {trip_details['start_date']} to {trip_details['end_date']}")
        text_output.append(f"Budget Range: {trip_details['budget_range'].title()}")
        text_output.append("")
        
        for day_plan in itinerary:
            text_output.append(f"DAY {day_plan.day} - {day_plan.date}")
            text_output.append("-" * 40)
            text_output.append(f"Weather: {day_plan.weather}")
            text_output.append("")
            
            if day_plan.attractions:
                text_output.append("🏛️  ATTRACTIONS:")
                for attraction in day_plan.attractions:
                    time_info = getattr(attraction, 'recommended_time', 'Flexible timing')
                    text_output.append(f"   • {attraction.name} ({time_info})")
                    text_output.append(f"     Rating: {attraction.rating}⭐ | Cost: ${attraction.estimated_cost}")
                text_output.append("")
            
            if day_plan.activities:
                text_output.append("🎯 ACTIVITIES:")
                for activity in day_plan.activities:
                    time_info = getattr(activity, 'recommended_time', 'Flexible timing')
                    text_output.append(f"   • {activity.name} ({time_info})")
                    text_output.append(f"     Duration: {activity.duration}h | Cost: ${activity.estimated_cost}")
                text_output.append("")
            
            if day_plan.restaurants:
                text_output.append("🍽️  DINING:")
                for restaurant in day_plan.restaurants:
                    time_info = getattr(restaurant, 'recommended_time', 'Meal time')
                    text_output.append(f"   • {restaurant.name} ({time_info})")
                    text_output.append(f"     Rating: {restaurant.rating}⭐ | Cost: ${restaurant.estimated_cost}")
                text_output.append("")
            
            if hasattr(day_plan, 'recommendations') and day_plan.recommendations:
                text_output.append("💡 RECOMMENDATIONS:")
                for rec in day_plan.recommendations:
                    text_output.append(f"   • {rec}")
                text_output.append("")
            
            text_output.append(f"💰 Daily Cost Estimate: ${day_plan.daily_cost}")
            text_output.append("")
            text_output.append("=" * 60)
            text_output.append("")
        
        return "\n".join(text_output)