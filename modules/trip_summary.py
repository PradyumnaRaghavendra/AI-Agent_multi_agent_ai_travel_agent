import json
from typing import Dict, Any, List
from datetime import datetime
from data.models import TripSummary, DayPlan, Hotel, Weather

class TripSummaryGenerator:
    """Service for generating comprehensive trip summaries"""
    
    def __init__(self):
        self.summary_template = {
            'trip_overview': {},
            'weather_summary': {},
            'accommodation_summary': {},
            'expense_summary': {},
            'itinerary_highlights': {},
            'recommendations': {},
            'travel_tips': {}
        }
    
    def generate_summary(self, trip_details: Dict[str, Any], weather_data: List[Weather], 
                        hotels: List[Hotel], expense_breakdown: Dict[str, Any], 
                        itinerary: List[DayPlan]) -> TripSummary:
        """Generate complete trip summary"""
        
        # Create TripSummary object
        summary = TripSummary(
            destination=trip_details['destination'],
            start_date=trip_details['start_date'],
            end_date=trip_details['end_date'],
            total_days=trip_details['total_days'],
            total_cost=expense_breakdown.get('total_cost', 0),
            daily_budget=expense_breakdown.get('daily_budget', 0),
            currency=expense_breakdown.get('target_currency', 'USD'),
            converted_total=expense_breakdown.get('converted_total', expense_breakdown.get('total_cost', 0)),
            itinerary=itinerary,
            hotels=hotels[:3]  # Top 3 hotel recommendations
        )
        
        # Add additional summary data
        summary.trip_overview = self._generate_trip_overview(trip_details, expense_breakdown)
        summary.weather_summary = self._generate_weather_summary(weather_data)
        summary.accommodation_summary = self._generate_accommodation_summary(hotels, trip_details)
        summary.expense_summary = self._generate_expense_summary(expense_breakdown)
        summary.itinerary_highlights = self._generate_itinerary_highlights(itinerary)
        summary.recommendations = self._generate_recommendations(trip_details, weather_data, itinerary)
        summary.travel_tips = self._generate_travel_tips(trip_details, weather_data)
        
        return summary
    
    def _generate_trip_overview(self, trip_details: Dict[str, Any], expense_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trip overview section"""
        
        overview = {
            'destination': trip_details['destination'],
            'duration': f"{trip_details['total_days']} days",
            'travel_dates': f"{trip_details['start_date']} to {trip_details['end_date']}",
            'group_size': trip_details.get('group_size', 1),
            'budget_category': trip_details.get('budget_range', 'mid-range').title(),
            'total_budget': expense_breakdown.get('converted_total', 0),
            'currency': expense_breakdown.get('target_currency', 'USD'),
            'cost_per_person': expense_breakdown.get('cost_per_person', 0),
            'daily_budget': expense_breakdown.get('daily_budget', 0),
            'interests': trip_details.get('preferences', {}).get('interests', []),
            'planning_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Add trip type classification
        duration = trip_details['total_days']
        if duration <= 3:
            overview['trip_type'] = 'Weekend Getaway'
        elif duration <= 7:
            overview['trip_type'] = 'Short Vacation'
        elif duration <= 14:
            overview['trip_type'] = 'Extended Holiday'
        else:
            overview['trip_type'] = 'Long-term Travel'
        
        return overview
    
    def _generate_weather_summary(self, weather_data: List[Weather]) -> Dict[str, Any]:
        """Generate weather summary section"""
        
        if not weather_data:
            return {'status': 'Weather data unavailable'}
        
        temperatures = [w.temperature for w in weather_data]
        conditions = [w.description for w in weather_data]
        
        summary = {
            'forecast_period': f"{len(weather_data)} days",
            'temperature_range': {
                'min': min(temperatures),
                'max': max(temperatures),
                'average': round(sum(temperatures) / len(temperatures), 1)
            },
            'conditions': list(set(conditions)),
            'rainy_days': len([w for w in weather_data if 'rain' in w.description.lower()]),
            'sunny_days': len([w for w in weather_data if 'sun' in w.description.lower() or 'clear' in w.description.lower()]),
            'daily_forecast': [
                {
                    'date': w.date,
                    'temperature': w.temperature,
                    'condition': w.description,
                    'feels_like': w.feels_like
                } for w in weather_data
            ]
        }
        
        # Add weather-based recommendations
        avg_temp = summary['temperature_range']['average']
        
        weather_recommendations = []
        if avg_temp < 10:
            weather_recommendations.append("Pack warm clothing including jackets and layers")
        elif avg_temp > 25:
            weather_recommendations.append("Pack light, breathable clothing and sun protection")
        else:
            weather_recommendations.append("Pack versatile clothing for moderate temperatures")
        
        if summary['rainy_days'] > 0:
            weather_recommendations.append("Bring waterproof clothing and umbrella")
        
        summary['packing_recommendations'] = weather_recommendations
        
        return summary
    
    def _generate_accommodation_summary(self, hotels: List[Hotel], trip_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generate accommodation summary section"""
        
        if not hotels:
            return {'status': 'No hotel recommendations available'}
        
        recommended_hotel = hotels[0]  # Top recommendation
        total_nights = trip_details['total_days']
        
        summary = {
            'recommended_hotel': {
                'name': recommended_hotel.name,
                'rating': recommended_hotel.rating,
                'price_per_night': recommended_hotel.price_per_night,
                'total_cost': recommended_hotel.calculate_total_cost(total_nights),
                'address': recommended_hotel.address,
                'amenities': recommended_hotel.amenities
            },
            'alternative_options': [
                {
                    'name': hotel.name,
                    'rating': hotel.rating,
                    'price_per_night': hotel.price_per_night,
                    'total_cost': hotel.calculate_total_cost(total_nights)
                } for hotel in hotels[1:4]  # Next 3 options
            ],
            'total_nights': total_nights,
            'budget_range': {
                'lowest_option': min(h.price_per_night for h in hotels),
                'highest_option': max(h.price_per_night for h in hotels),
                'recommended_price': recommended_hotel.price_per_night
            }
        }
        
        return summary
    
    def _generate_expense_summary(self, expense_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """Generate expense summary section"""
        
        summary = {
            'total_cost': expense_breakdown.get('converted_total', 0),
            'currency': expense_breakdown.get('target_currency', 'USD'),
            'daily_budget': expense_breakdown.get('daily_budget', 0),
            'cost_per_person': expense_breakdown.get('cost_per_person', 0),
            'budget_category': expense_breakdown.get('budget_range', 'mid-range').title(),
            
            'cost_breakdown': {
                'accommodation': expense_breakdown.get('accommodation_cost', 0),
                'food_dining': expense_breakdown.get('food_cost', 0),
                'activities_attractions': expense_breakdown.get('activities_cost', 0),
                'transportation': expense_breakdown.get('transportation_cost', 0),
                'miscellaneous': expense_breakdown.get('miscellaneous_cost', 0)
            },
            
            'percentage_breakdown': expense_breakdown.get('cost_percentages', {}),
            
            'budget_tips': [
                "Book accommodations and flights in advance for better rates",
                "Consider eating at local restaurants for authentic and affordable meals",
                "Use public transportation when available",
                "Look for free activities and attractions",
                "Set aside 10-15% extra for unexpected expenses"
            ]
        }
        
        # Add currency conversion info if applicable
        if expense_breakdown.get('base_currency') != expense_breakdown.get('target_currency'):
            summary['currency_conversion'] = {
                'original_currency': expense_breakdown.get('base_currency', 'USD'),
                'converted_to': expense_breakdown.get('target_currency', 'USD'),
                'exchange_rate': expense_breakdown.get('conversion_rate', 1.0),
                'conversion_date': expense_breakdown.get('converted_date', datetime.now().strftime('%Y-%m-%d'))
            }
        
        return summary
    
    def _generate_itinerary_highlights(self, itinerary: List[DayPlan]) -> Dict[str, Any]:
        """Generate itinerary highlights section"""
        
        if not itinerary:
            return {'status': 'No itinerary available'}
        
        # Collect all attractions, restaurants, and activities
        all_attractions = []
        all_restaurants = []
        all_activities = []
        
        for day in itinerary:
            all_attractions.extend(day.attractions)
            all_restaurants.extend(day.restaurants)
            all_activities.extend(day.activities)
        
        # Get top-rated items
        top_attractions = sorted(all_attractions, key=lambda x: x.rating, reverse=True)[:5]
        top_restaurants = sorted(all_restaurants, key=lambda x: x.rating, reverse=True)[:5]
        top_activities = sorted(all_activities, key=lambda x: x.rating, reverse=True)[:3]
        
        highlights = {
            'total_days_planned': len(itinerary),
            'must_visit_attractions': [
                {
                    'name': attr.name,
                    'rating': attr.rating,
                    'estimated_cost': attr.estimated_cost,
                    'duration': attr.duration,
                    'description': attr.description
                } for attr in top_attractions
            ],
            'recommended_restaurants': [
                {
                    'name': rest.name,
                    'rating': rest.rating,
                    'estimated_cost': rest.estimated_cost,
                    'description': rest.description
                } for rest in top_restaurants
            ],
            'top_activities': [
                {
                    'name': act.name,
                    'rating': act.rating,
                    'estimated_cost': act.estimated_cost,
                    'duration': act.duration,
                    'description': act.description
                } for act in top_activities
            ],
            'daily_overview': [
                {
                    'day': day.day,
                    'date': day.date,
                    'weather': day.weather.description,
                    'temperature': day.weather.temperature,
                    'planned_activities': len(day.attractions) + len(day.activities),
                    'dining_options': len(day.restaurants),
                    'estimated_cost': day.daily_cost,
                    'highlights': [attr.name for attr in day.attractions[:2]] + 
                                [act.name for act in day.activities[:1]]
                } for day in itinerary
            ]
        }
        
        return highlights
    
    def _generate_recommendations(self, trip_details: Dict[str, Any], weather_data: List[Weather], 
                                itinerary: List[DayPlan]) -> Dict[str, Any]:
        """Generate personalized recommendations"""
        
        recommendations = {
            'packing_essentials': [],
            'local_tips': [],
            'safety_advice': [],
            'cultural_considerations': [],
            'money_matters': []
        }
        
        # Packing recommendations based on weather and activities
        if weather_data:
            avg_temp = sum(w.temperature for w in weather_data) / len(weather_data)
            
            if avg_temp < 15:
                recommendations['packing_essentials'].extend([
                    "Warm jacket and layers",
                    "Comfortable walking boots",
                    "Gloves and warm accessories"
                ])
            elif avg_temp > 25:
                recommendations['packing_essentials'].extend([
                    "Light, breathable clothing",
                    "Sun hat and sunglasses",
                    "Sunscreen and water bottle"
                ])
            
            rainy_days = len([w for w in weather_data if 'rain' in w.description.lower()])
            if rainy_days > 0:
                recommendations['packing_essentials'].extend([
                    "Waterproof jacket or umbrella",
                    "Waterproof bag for electronics"
                ])
        
        # Activity-based packing
        has_outdoor_activities = any(
            any('outdoor' in act.description.lower() or 'park' in act.name.lower() 
                for act in day.activities + day.attractions)
            for day in itinerary
        )
        
        if has_outdoor_activities:
            recommendations['packing_essentials'].extend([
                "Comfortable walking shoes",
                "Daypack for excursions",
                "Camera for sightseeing"
            ])
        
        # Local tips
        recommendations['local_tips'] = [
            f"Research local customs and etiquette in {trip_details['destination']}",
            "Download offline maps and translation apps",
            "Learn basic phrases in the local language",
            "Keep emergency contact numbers handy",
            "Research tipping customs and local payment methods"
        ]
        
        # Safety advice
        recommendations['safety_advice'] = [
            "Keep copies of important documents in separate locations",
            "Inform someone about your daily itinerary",
            "Stay aware of your surroundings, especially in crowded areas",
            "Keep emergency cash in local currency",
            "Research local emergency numbers and procedures"
        ]
        
        # Money matters
        currency = trip_details.get('currency', 'USD')
        recommendations['money_matters'] = [
            f"Notify your bank about travel to {trip_details['destination']}",
            f"Have some local currency for small purchases",
            "Use ATMs affiliated with major banks for better exchange rates",
            "Keep receipts for expense tracking",
            "Consider travel insurance for unexpected costs"
        ]
        
        return recommendations
    
    def _generate_travel_tips(self, trip_details: Dict[str, Any], weather_data: List[Weather]) -> List[str]:
        """Generate general travel tips"""
        
        tips = [
            "Arrive at attractions early to avoid crowds",
            "Keep your phone charged and carry a portable charger",
            "Stay hydrated and take breaks during long walking days",
            "Try local cuisine but be cautious with street food if you have a sensitive stomach",
            "Respect local customs and dress codes, especially at religious sites",
            "Keep important documents and valuables secure",
            "Take photos but also take time to enjoy moments without a camera",
            "Be flexible with your itinerary - sometimes the best experiences are unplanned",
            "Connect with locals for authentic recommendations",
            "Consider purchasing a city tourist pass if visiting multiple attractions"
        ]
        
        # Add weather-specific tips
        if weather_data:
            rainy_days = len([w for w in weather_data if 'rain' in w.description.lower()])
            if rainy_days > len(weather_data) * 0.3:  # More than 30% rainy days
                tips.append("Have indoor backup plans for rainy days")
        
        return tips
    
    def save_to_file(self, summary: TripSummary, filename: str = None) -> str:
        """Save trip summary to a text file"""
        
        if not filename:
            destination = summary.destination.replace(' ', '_').replace(',', '')
            filename = f"trip_summary_{destination}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        content = self._format_summary_for_file(summary)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return filename
        except Exception as e:
            raise Exception(f"Failed to save file: {e}")
    
    def _format_summary_for_file(self, summary: TripSummary) -> str:
        """Format trip summary for file output"""
        
        output = []
        output.append("="*80)
        output.append("COMPLETE TRAVEL PLAN SUMMARY")
        output.append("="*80)
        output.append("")
        
        # Trip Overview
        output.append("🌍 TRIP OVERVIEW")
        output.append("-"*40)
        output.append(f"Destination: {summary.destination}")
        output.append(f"Duration: {summary.total_days} days ({summary.start_date} to {summary.end_date})")
        output.append(f"Total Budget: {summary.currency} {summary.converted_total:,.2f}")
        output.append(f"Daily Budget: {summary.currency} {summary.daily_budget:,.2f}")
        output.append("")
        
        # Weather Summary
        if hasattr(summary, 'weather_summary'):
            weather = summary.weather_summary
            output.append("🌤️ WEATHER FORECAST")
            output.append("-"*40)
            if 'temperature_range' in weather:
                temp_range = weather['temperature_range']
                output.append(f"Temperature Range: {temp_range['min']}°C to {temp_range['max']}°C")
                output.append(f"Average Temperature: {temp_range['average']}°C")
            output.append(f"Expected Conditions: {', '.join(weather.get('conditions', []))}")
            if weather.get('packing_recommendations'):
                output.append("Packing Recommendations:")
                for rec in weather['packing_recommendations']:
                    output.append(f"  • {rec}")
            output.append("")
        
        # Accommodation
        if summary.hotels:
            output.append("🏨 ACCOMMODATION")
            output.append("-"*40)
            hotel = summary.hotels[0]
            output.append(f"Recommended: {hotel.name}")
            output.append(f"Rating: {hotel.rating}⭐")
            output.append(f"Price: {summary.currency} {hotel.price_per_night:.2f} per night")
            output.append(f"Total Cost: {summary.currency} {hotel.calculate_total_cost(summary.total_days):.2f}")
            output.append(f"Address: {hotel.address}")
            if hotel.amenities:
                output.append(f"Amenities: {', '.join(hotel.amenities[:5])}")
            output.append("")
        
        # Itinerary Highlights
        if summary.itinerary:
            output.append("📅 DAILY ITINERARY")
            output.append("-"*40)
            for day in summary.itinerary:
                output.append(f"Day {day.day} ({day.date})")
                output.append(f"Weather: {day.weather.description}, {day.weather.temperature}°C")
                
                if day.attractions:
                    output.append("  Attractions:")
                    for attr in day.attractions:
                        output.append(f"    • {attr.name} ({attr.rating}⭐)")
                
                if day.activities:
                    output.append("  Activities:")
                    for act in day.activities:
                        output.append(f"    • {act.name} ({act.duration}h)")
                
                if day.restaurants:
                    output.append("  Dining:")
                    for rest in day.restaurants:
                        output.append(f"    • {rest.name} ({rest.rating}⭐)")
                
                output.append(f"  Estimated Daily Cost: {summary.currency} {day.daily_cost:.2f}")
                output.append("")
        
        # Travel Tips
        if hasattr(summary, 'travel_tips'):
            output.append("💡 TRAVEL TIPS")
            output.append("-"*40)
            for tip in summary.travel_tips[:10]:  # Top 10 tips
                output.append(f"• {tip}")
            output.append("")
        
        output.append("="*80)
        output.append("Happy Travels! 🎉")
        output.append("Generated by AI Travel Agent & Expense Planner")
        output.append(f"Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("="*80)
        
        return "\n".join(output)
    
    def export_to_json(self, summary: TripSummary, filename: str = None) -> str:
        """Export summary to JSON format"""
        
        if not filename:
            destination = summary.destination.replace(' ', '_').replace(',', '')
            filename = f"trip_data_{destination}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert summary to dictionary
        summary_dict = {
            'destination': summary.destination,
            'start_date': summary.start_date.isoformat() if hasattr(summary.start_date, 'isoformat') else str(summary.start_date),
            'end_date': summary.end_date.isoformat() if hasattr(summary.end_date, 'isoformat') else str(summary.end_date),
            'total_days': summary.total_days,
            'total_cost': summary.total_cost,
            'currency': summary.currency,
            'hotels': [
                {
                    'name': hotel.name,
                    'rating': hotel.rating,
                    'price_per_night': hotel.price_per_night,
                    'address': hotel.address,
                    'amenities': hotel.amenities
                } for hotel in summary.hotels
            ],
            'itinerary': [
                {
                    'day': day.day,
                    'date': day.date,
                    'weather': {
                        'temperature': day.weather.temperature,
                        'description': day.weather.description,
                        'humidity': day.weather.humidity
                    },
                    'attractions': [{'name': a.name, 'rating': a.rating, 'cost': a.estimated_cost} for a in day.attractions],
                    'restaurants': [{'name': r.name, 'rating': r.rating, 'cost': r.estimated_cost} for r in day.restaurants],
                    'activities': [{'name': act.name, 'rating': act.rating, 'cost': act.estimated_cost} for act in day.activities],
                    'daily_cost': day.daily_cost
                } for day in summary.itinerary
            ]
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(summary_dict, f, indent=2, ensure_ascii=False)
            return filename
        except Exception as e:
            raise Exception(f"Failed to save JSON file: {e}")# Final trip summary generator
