# Total and daily cost calculation
from typing import Dict, Any, List
from ..data.models import Hotel, Attraction, Transportation

class ExpenseCalculator:
    """Service for calculating total trip expenses"""
    
    def __init__(self):
        # Base multipliers for different budget ranges
        self.budget_multipliers = {
            'budget': 0.8,
            'mid-range': 1.0,
            'luxury': 1.5
        }
        
        # Transportation cost estimates per day (USD)
        self.transportation_costs = {
            'budget': 15,      # Public transport, walking
            'mid-range': 35,   # Mix of transport, some taxis
            'luxury': 60       # Private transport, taxis
        }
        
        # Miscellaneous daily costs (shopping, tips, etc.)
        self.miscellaneous_costs = {
            'budget': 20,
            'mid-range': 40,
            'luxury': 80
        }
    
    def calculate_total_expenses(self, trip_details: Dict[str, Any], hotels: List[Hotel], 
                               attractions: List[Attraction], restaurants: List[Attraction], 
                               activities: List[Attraction]) -> Dict[str, Any]:
        """Calculate comprehensive trip expenses"""
        
        total_days = trip_details['total_days']
        budget_range = trip_details.get('budget_range', 'mid-range')
        group_size = trip_details.get('group_size', 1)
        
        # Calculate accommodation costs
        accommodation_cost = self._calculate_accommodation_cost(hotels, total_days, budget_range)
        
        # Calculate food costs
        food_cost = self._calculate_food_cost(restaurants, total_days, group_size, budget_range)
        
        # Calculate activities cost
        activities_cost = self._calculate_activities_cost(attractions + activities, total_days, group_size, budget_range)
        
        # Calculate transportation costs
        transportation_cost = self._calculate_transportation_cost(total_days, group_size, budget_range)
        
        # Calculate miscellaneous costs
        miscellaneous_cost = self._calculate_miscellaneous_cost(total_days, group_size, budget_range)
        
        # Calculate totals
        total_cost = (accommodation_cost + food_cost + activities_cost + 
                     transportation_cost + miscellaneous_cost)
        
        daily_budget = total_cost / total_days if total_days > 0 else 0
        
        # Create detailed breakdown
        expense_breakdown = {
            'base_currency': 'USD',
            'trip_duration': total_days,
            'group_size': group_size,
            'budget_range': budget_range,
            
            # Main categories
            'accommodation_cost': round(accommodation_cost, 2),
            'food_cost': round(food_cost, 2),
            'activities_cost': round(activities_cost, 2),
            'transportation_cost': round(transportation_cost, 2),
            'miscellaneous_cost': round(miscellaneous_cost, 2),
            
            # Totals
            'total_cost': round(total_cost, 2),
            'daily_budget': round(daily_budget, 2),
            'cost_per_person': round(total_cost / group_size, 2) if group_size > 0 else 0,
            'daily_cost_per_person': round(daily_budget / group_size, 2) if group_size > 0 else 0,
            
            # Detailed breakdown
            'detailed_breakdown': self._create_detailed_breakdown(
                hotels, attractions, restaurants, activities, trip_details
            ),
            
            # Percentage breakdown
            'cost_percentages': self._calculate_cost_percentages(
                accommodation_cost, food_cost, activities_cost, 
                transportation_cost, miscellaneous_cost, total_cost
            )
        }
        
        return expense_breakdown
    
    def _calculate_accommodation_cost(self, hotels: List[Hotel], total_days: int, budget_range: str) -> float:
        """Calculate accommodation costs"""
        if not hotels:
            # Fallback estimation
            base_costs = {'budget': 40, 'mid-range': 100, 'luxury': 250}
            return base_costs.get(budget_range, 100) * total_days
        
        # Use the most appropriate hotel based on budget
        suitable_hotels = self._filter_hotels_by_budget(hotels, budget_range)
        selected_hotel = suitable_hotels[0] if suitable_hotels else hotels[0]
        
        return selected_hotel.calculate_total_cost(total_days)
    
    def _calculate_food_cost(self, restaurants: List[Attraction], total_days: int, 
                           group_size: int, budget_range: str) -> float:
        """Calculate food and dining costs"""
        if not restaurants:
            # Fallback estimation (3 meals per day)
            base_daily_cost = {'budget': 25, 'mid-range': 50, 'luxury': 100}
            return base_daily_cost.get(budget_range, 50) * total_days * group_size
        
        # Calculate based on restaurant costs (assuming 2-3 restaurant meals per day)
        avg_meal_cost = sum(r.estimated_cost for r in restaurants[:5]) / min(len(restaurants), 5)
        meals_per_day = 2.5  # Average between 2-3 restaurant meals
        
        daily_food_cost = avg_meal_cost * meals_per_day * group_size
        return daily_food_cost * total_days
    
    def _calculate_activities_cost(self, activities: List[Attraction], total_days: int, 
                                 group_size: int, budget_range: str) -> float:
        """Calculate activities and attractions costs"""
        if not activities:
            # Fallback estimation
            base_daily_cost = {'budget': 30, 'mid-range': 60, 'luxury': 120}
            return base_daily_cost.get(budget_range, 60) * total_days * group_size
        
        # Calculate based on planned activities (1-2 major activities per day)
        activities_per_day = min(2, len(activities) / max(total_days, 1))
        avg_activity_cost = sum(a.estimated_cost for a in activities[:10]) / min(len(activities), 10)
        
        daily_activities_cost = avg_activity_cost * activities_per_day * group_size
        return daily_activities_cost * total_days
    
    def _calculate_transportation_cost(self, total_days: int, group_size: int, budget_range: str) -> float:
        """Calculate transportation costs"""
        daily_transport_cost = self.transportation_costs.get(budget_range, 35)
        
        # Group discounts for larger groups (shared taxis, etc.)
        if group_size > 2:
            group_multiplier = 1 + (group_size - 1) * 0.7  # Not linear scaling
        else:
            group_multiplier = group_size
        
        return daily_transport_cost * group_multiplier * total_days
    
    def _calculate_miscellaneous_cost(self, total_days: int, group_size: int, budget_range: str) -> float:
        """Calculate miscellaneous costs (shopping, tips, emergencies)"""
        daily_misc_cost = self.miscellaneous_costs.get(budget_range, 40)
        return daily_misc_cost * group_size * total_days
    
    def _filter_hotels_by_budget(self, hotels: List[Hotel], budget_range: str) -> List[Hotel]:
        """Filter hotels based on budget range"""
        budget_ranges = {
            'budget': (0, 80),
            'mid-range': (80, 200),
            'luxury': (200, 1000)
        }
        
        min_price, max_price = budget_ranges.get(budget_range, (80, 200))
        
        suitable_hotels = [h for h in hotels if min_price <= h.price_per_night <= max_price]
        return suitable_hotels if suitable_hotels else hotels
    
    def _create_detailed_breakdown(self, hotels: List[Hotel], attractions: List[Attraction], 
                                 restaurants: List[Attraction], activities: List[Attraction], 
                                 trip_details: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed expense breakdown"""
        breakdown = {
            'accommodation': {
                'recommended_hotel': hotels[0].name if hotels else 'Standard Hotel',
                'price_per_night': hotels[0].price_per_night if hotels else 100,
                'total_nights': trip_details['total_days'],
                'total_cost': hotels[0].calculate_total_cost(trip_details['total_days']) if hotels else 100 * trip_details['total_days']
            },
            
            'dining': [
                {
                    'name': r.name,
                    'type': 'restaurant',
                    'estimated_cost': r.estimated_cost,
                    'rating': r.rating
                } for r in restaurants[:5]
            ],
            
            'attractions': [
                {
                    'name': a.name,
                    'type': a.type,
                    'estimated_cost': a.estimated_cost,
                    'duration': a.duration,
                    'rating': a.rating
                } for a in attractions[:8]
            ],
            
            'activities': [
                {
                    'name': a.name,
                    'type': a.type,
                    'estimated_cost': a.estimated_cost,
                    'duration': a.duration,
                    'rating': a.rating
                } for a in activities[:6]
            ],
            
            'transportation': {
                'daily_estimate': self.transportation_costs.get(trip_details.get('budget_range', 'mid-range'), 35),
                'total_days': trip_details['total_days'],
                'group_size': trip_details['group_size'],
                'description': self._get_transportation_description(trip_details.get('budget_range', 'mid-range'))
            },
            
            'miscellaneous': {
                'daily_estimate': self.miscellaneous_costs.get(trip_details.get('budget_range', 'mid-range'), 40),
                'total_days': trip_details['total_days'],
                'group_size': trip_details['group_size'],
                'includes': ['Shopping', 'Tips', 'Souvenirs', 'Emergency fund', 'Incidentals']
            }
        }
        
        return breakdown
    
    def _calculate_cost_percentages(self, accommodation: float, food: float, activities: float, 
                                  transportation: float, miscellaneous: float, total: float) -> Dict[str, float]:
        """Calculate percentage breakdown of costs"""
        if total == 0:
            return {}
        
        return {
            'accommodation': round((accommodation / total) * 100, 1),
            'food': round((food / total) * 100, 1),
            'activities': round((activities / total) * 100, 1),
            'transportation': round((transportation / total) * 100, 1),
            'miscellaneous': round((miscellaneous / total) * 100, 1)
        }
    
    def _get_transportation_description(self, budget_range: str) -> str:
        """Get transportation description based on budget"""
        descriptions = {
            'budget': 'Public transport, walking, occasional taxi',
            'mid-range': 'Mix of public transport, taxis, and ride-sharing',
            'luxury': 'Private transport, taxis, premium services'
        }
        return descriptions.get(budget_range, 'Mixed transportation options')
    
    def calculate_budget_comparison(self, base_expenses: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Compare costs across different budget ranges"""
        base_total = base_expenses['total_cost']
        base_budget = base_expenses['budget_range']
        
        comparison = {}
        
        for budget_range in ['budget', 'mid-range', 'luxury']:
            if budget_range == base_budget:
                comparison[budget_range] = {
                    'total_cost': base_total,
                    'daily_budget': base_expenses['daily_budget'],
                    'difference': 0,
                    'percentage_change': 0
                }
            else:
                multiplier = self.budget_multipliers[budget_range] / self.budget_multipliers[base_budget]
                adjusted_total = base_total * multiplier
                
                comparison[budget_range] = {
                    'total_cost': round(adjusted_total, 2),
                    'daily_budget': round(adjusted_total / base_expenses['trip_duration'], 2),
                    'difference': round(adjusted_total - base_total, 2),
                    'percentage_change': round(((adjusted_total - base_total) / base_total) * 100, 1)
                }
        
        return comparison
    
    def get_cost_saving_tips(self, expenses: Dict[str, Any]) -> List[str]:
        """Generate cost-saving tips based on expense breakdown"""
        tips = []
        budget_range = expenses.get('budget_range', 'mid-range')
        percentages = expenses.get('cost_percentages', {})
        
        # Accommodation tips
        if percentages.get('accommodation', 0) > 40:
            tips.append("Consider staying in budget hotels or guesthouses to reduce accommodation costs")
            tips.append("Look for hotels slightly outside city center for better rates")
        
        # Food tips
        if percentages.get('food', 0) > 35:
            tips.append("Try local street food and markets for authentic and budget-friendly meals")
            tips.append("Consider hotels with breakfast included")
        
        # Activities tips
        if percentages.get('activities', 0) > 30:
            tips.append("Look for free walking tours and public attractions")
            tips.append("Check for group discounts on activities and attractions")
        
        # Transportation tips
        if percentages.get('transportation', 0) > 20:
            tips.append("Use public transportation instead of taxis when possible")
            tips.append("Consider getting a city transport pass for multiple days")
        
        # General tips based on budget range
        if budget_range != 'budget':
            tips.append("Travel during off-peak seasons for better rates")
            tips.append("Book accommodations and activities in advance for early bird discounts")
        
        tips.append("Set aside 10-15% of your budget for unexpected expenses")
        tips.append("Use travel apps to find deals and compare prices")
        
        return tips