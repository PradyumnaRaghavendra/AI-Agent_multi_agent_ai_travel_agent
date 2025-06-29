"""
Specialized Travel Planning Agents
"""

import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from . import BaseAgent, AgentRole, Message, MessageType
# Import data models directly (will work when run from proper context)
try:
    from ..data.models import Weather, Attraction, Hotel
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from data.models import Weather, Attraction, Hotel

class TravelAdvisorAgent(BaseAgent):
    """Expert travel advisor agent with destination knowledge"""
    
    def __init__(self):
        super().__init__(
            agent_id="travel_advisor",
            role=AgentRole.TRAVEL_ADVISOR,
            capabilities=["destination_expertise", "attraction_recommendations", "cultural_insights"]
        )
        
        # Initialize destination knowledge
        self.destination_expertise = {
            'london': {
                'must_visit': ['British Museum', 'Tower Bridge', 'Big Ben', 'Hyde Park'],
                'hidden_gems': ['Leadenhall Market', 'Sky Garden', 'Neal\'s Yard'],
                'cultural_tips': ['Queue etiquette', 'Pub culture', 'Sunday roast tradition'],
                'best_areas': ['Covent Garden', 'South Bank', 'Notting Hill'],
                'transport_tips': ['Oyster Card', 'Walking preferred in Zone 1', 'Night Tube weekends']
            },
            'paris': {
                'must_visit': ['Eiffel Tower', 'Louvre', 'Notre-Dame', 'Champs-Élysées'],
                'hidden_gems': ['Sainte-Chapelle', 'Père Lachaise Cemetery', 'Marché aux Puces'],
                'cultural_tips': ['Greeting etiquette', 'Dining times', 'Museum passes'],
                'best_areas': ['Le Marais', 'Saint-Germain', 'Montmartre'],
                'transport_tips': ['Metro day passes', 'Walking zones', 'Vélib bike sharing']
            },
            'tokyo': {
                'must_visit': ['Senso-ji Temple', 'Shibuya Crossing', 'Tsukiji Market', 'Imperial Palace'],
                'hidden_gems': ['Golden Gai', 'Robot Restaurant', 'Omoide Yokocho'],
                'cultural_tips': ['Bowing etiquette', 'Shoe removal', 'Onsen rules'],
                'best_areas': ['Shinjuku', 'Harajuku', 'Asakusa'],
                'transport_tips': ['JR Pass', 'IC Cards', 'Rush hour avoidance']
            }
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages"""
        if message.msg_type == MessageType.QUERY:
            content = message.content
            
            if 'destination_advice' in content:
                advice = self._provide_destination_advice(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'destination_advice': advice}
                )
            elif 'attraction_recommendations' in content:
                recommendations = self._recommend_attractions(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RECOMMENDATION,
                    {'attractions': recommendations}
                )
        
        return None
    
    def generate_recommendation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate travel recommendations based on context"""
        destination = context.get('destination', '').lower()
        interests = context.get('interests', [])
        duration = context.get('duration', 3)
        
        recommendation = {
            'agent': self.agent_id,
            'type': 'travel_advice',
            'confidence': 0.8,
            'recommendations': {}
        }
        
        if destination in self.destination_expertise:
            dest_info = self.destination_expertise[destination]
            
            # Core attractions
            must_visit = dest_info['must_visit'][:min(duration, len(dest_info['must_visit']))]
            recommendation['recommendations']['must_visit'] = must_visit
            
            # Interest-based suggestions
            if 'culture' in interests or 'history' in interests:
                recommendation['recommendations']['cultural_sites'] = dest_info.get('cultural_tips', [])
            
            if 'food' in interests:
                recommendation['recommendations']['food_experiences'] = self._get_food_recommendations(destination)
            
            # Hidden gems for explorers
            recommendation['recommendations']['hidden_gems'] = dest_info.get('hidden_gems', [])[:2]
            
            # Practical tips
            recommendation['recommendations']['transport_tips'] = dest_info.get('transport_tips', [])
            recommendation['recommendations']['best_areas'] = dest_info.get('best_areas', [])
            
            recommendation['confidence'] = 0.9
        else:
            # Generic recommendations
            recommendation['recommendations']['general_advice'] = [
                'Research local customs and etiquette',
                'Download offline maps and translation apps',
                'Try local cuisine and specialties',
                'Visit both famous landmarks and local neighborhoods'
            ]
            recommendation['confidence'] = 0.6
        
        return recommendation
    
    def _provide_destination_advice(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Provide comprehensive destination advice"""
        destination = request.get('destination', '').lower()
        
        if destination in self.destination_expertise:
            return self.destination_expertise[destination]
        else:
            return {
                'must_visit': ['Main city center', 'Local markets', 'Cultural sites'],
                'cultural_tips': ['Research local customs', 'Learn basic phrases'],
                'transport_tips': ['Use public transport', 'Walk when possible']
            }
    
    def _recommend_attractions(self, request: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend attractions based on interests"""
        interests = request.get('interests', [])
        destination = request.get('destination', '').lower()
        
        recommendations = []
        
        if destination in self.destination_expertise:
            dest_info = self.destination_expertise[destination]
            
            # Add must-visit attractions
            for attraction in dest_info['must_visit']:
                recommendations.append({
                    'name': attraction,
                    'type': 'must_visit',
                    'reason': 'Iconic landmark',
                    'estimated_duration': 2
                })
            
            # Add interest-based recommendations
            if 'culture' in interests or 'history' in interests:
                for gem in dest_info['hidden_gems'][:2]:
                    recommendations.append({
                        'name': gem,
                        'type': 'cultural',
                        'reason': 'Rich cultural experience',
                        'estimated_duration': 1.5
                    })
        
        return recommendations[:8]  # Limit to 8 recommendations
    
    def _get_food_recommendations(self, destination: str) -> List[str]:
        """Get food recommendations for destination"""
        food_recs = {
            'london': ['Traditional pub lunch', 'Fish and chips', 'Afternoon tea', 'Sunday roast'],
            'paris': ['Café culture', 'Boulangerie pastries', 'Wine tasting', 'Bistro dining'],
            'tokyo': ['Sushi omakase', 'Ramen shops', 'Izakaya experience', 'Street food']
        }
        return food_recs.get(destination, ['Local specialties', 'Street food', 'Traditional restaurants'])

class BudgetOptimizerAgent(BaseAgent):
    """Agent specialized in budget optimization and cost-saving strategies"""
    
    def __init__(self):
        super().__init__(
            agent_id="budget_optimizer",
            role=AgentRole.BUDGET_OPTIMIZER,
            capabilities=["cost_analysis", "budget_optimization", "deal_finding"]
        )
        
        # Cost-saving strategies database
        self.optimization_strategies = {
            'accommodation': [
                'Book accommodations outside city center',
                'Consider hostels or guesthouses',
                'Look for properties with kitchen facilities',
                'Check for group discounts',
                'Book in advance for better rates'
            ],
            'transportation': [
                'Use public transport passes',
                'Walk when distances are reasonable',
                'Consider bike rentals',
                'Avoid peak-hour taxi rides',
                'Book flights in advance'
            ],
            'food': [
                'Try local street food and markets',
                'Look for lunch specials',
                'Cook some meals if kitchen available',
                'Avoid tourist area restaurants',
                'Try happy hour deals'
            ],
            'activities': [
                'Look for free walking tours',
                'Check for museum free days',
                'Consider city tourist passes',
                'Book group activities for discounts',
                'Explore free parks and public spaces'
            ]
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process budget-related queries"""
        if message.msg_type == MessageType.QUERY:
            content = message.content
            
            if 'budget_optimization' in content:
                optimization = self._optimize_budget(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'budget_optimization': optimization}
                )
            elif 'cost_analysis' in content:
                analysis = self._analyze_costs(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'cost_analysis': analysis}
                )
        
        return None
    
    def generate_recommendation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate budget optimization recommendations"""
        budget_range = context.get('budget_range', 'mid-range')
        total_cost = context.get('total_cost', 0)
        duration = context.get('duration', 3)
        group_size = context.get('group_size', 1)
        
        recommendation = {
            'agent': self.agent_id,
            'type': 'budget_optimization',
            'confidence': 0.85,
            'savings_potential': 0,
            'strategies': []
        }
        
        # Calculate potential savings
        daily_budget = total_cost / duration if duration > 0 else 0
        
        # Analyze budget and suggest optimizations
        if budget_range == 'luxury' and daily_budget > 200:
            recommendation['strategies'].extend([
                'Consider mid-range alternatives for some expenses',
                'Mix luxury and budget experiences',
                'Look for package deals'
            ])
            recommendation['savings_potential'] = total_cost * 0.15  # 15% potential savings
            
        elif budget_range == 'mid-range' and daily_budget > 120:
            recommendation['strategies'].extend([
                'Optimize accommodation location vs. cost',
                'Use public transport strategically',
                'Mix restaurant dining with local markets'
            ])
            recommendation['savings_potential'] = total_cost * 0.10  # 10% potential savings
            
        elif budget_range == 'budget':
            recommendation['strategies'].extend([
                'Maximize free activities and attractions',
                'Consider shared accommodations',
                'Focus on local street food and markets'
            ])
            recommendation['savings_potential'] = total_cost * 0.20  # 20% potential savings
        
        # Add group-specific savings
        if group_size > 2:
            recommendation['strategies'].extend([
                'Look for group discounts on activities',
                'Consider apartment rentals over hotel rooms',
                'Split transportation costs'
            ])
            recommendation['savings_potential'] += total_cost * 0.05
        
        # Add category-specific strategies
        for category in ['accommodation', 'transportation', 'food', 'activities']:
            if category in context.get('expense_breakdown', {}):
                recommendation['strategies'].extend(
                    self.optimization_strategies[category][:2]
                )
        
        return recommendation
    
    def _optimize_budget(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Provide detailed budget optimization plan"""
        current_budget = request.get('budget', 0)
        target_savings = request.get('target_savings', 0.1)  # 10% default
        
        optimization_plan = {
            'current_budget': current_budget,
            'target_savings_percentage': target_savings * 100,
            'estimated_savings': current_budget * target_savings,
            'optimization_actions': []
        }
        
        # Priority-ordered optimization actions
        actions = [
            {'action': 'Review accommodation options', 'potential_savings': 0.08, 'effort': 'low'},
            {'action': 'Optimize transportation choices', 'potential_savings': 0.05, 'effort': 'low'},
            {'action': 'Research free and low-cost activities', 'potential_savings': 0.07, 'effort': 'medium'},
            {'action': 'Plan strategic dining choices', 'potential_savings': 0.06, 'effort': 'low'},
            {'action': 'Look for package deals and discounts', 'potential_savings': 0.04, 'effort': 'medium'}
        ]
        
        cumulative_savings = 0
        for action in actions:
            if cumulative_savings < target_savings:
                optimization_plan['optimization_actions'].append(action)
                cumulative_savings += action['potential_savings']
        
        optimization_plan['total_potential_savings'] = cumulative_savings * current_budget
        
        return optimization_plan
    
    def _analyze_costs(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze cost breakdown and identify optimization opportunities"""
        expense_breakdown = request.get('expense_breakdown', {})
        
        analysis = {
            'total_expenses': sum(expense_breakdown.values()),
            'category_analysis': {},
            'recommendations': []
        }
        
        total = analysis['total_expenses']
        
        for category, amount in expense_breakdown.items():
            percentage = (amount / total * 100) if total > 0 else 0
            
            analysis['category_analysis'][category] = {
                'amount': amount,
                'percentage': percentage,
                'status': 'normal'
            }
            
            # Flag high-cost categories
            if category == 'accommodation' and percentage > 45:
                analysis['category_analysis'][category]['status'] = 'high'
                analysis['recommendations'].append(f'Accommodation costs are high ({percentage:.1f}%). Consider alternatives.')
            elif category == 'food' and percentage > 35:
                analysis['category_analysis'][category]['status'] = 'high'
                analysis['recommendations'].append(f'Food costs are high ({percentage:.1f}%). Try local markets and street food.')
            elif category == 'activities' and percentage > 30:
                analysis['category_analysis'][category]['status'] = 'high'
                analysis['recommendations'].append(f'Activity costs are high ({percentage:.1f}%). Look for free alternatives.')
        
        return analysis

class WeatherAnalystAgent(BaseAgent):
    """Agent specialized in weather analysis and weather-based recommendations"""
    
    def __init__(self):
        super().__init__(
            agent_id="weather_analyst",
            role=AgentRole.WEATHER_ANALYST,
            capabilities=["weather_analysis", "activity_optimization", "packing_advice"]
        )
        
        # Weather-activity mapping
        self.weather_activities = {
            'sunny': {
                'recommended': ['outdoor tours', 'parks', 'walking', 'outdoor dining', 'sightseeing'],
                'avoid': ['indoor-only activities during day'],
                'packing': ['sunscreen', 'hat', 'light clothing', 'water bottle']
            },
            'rainy': {
                'recommended': ['museums', 'galleries', 'shopping', 'indoor attractions', 'cafes'],
                'avoid': ['extensive outdoor walking', 'outdoor sports'],
                'packing': ['umbrella', 'waterproof jacket', 'indoor shoes']
            },
            'cold': {
                'recommended': ['indoor attractions', 'hot drinks', 'warm cafes', 'covered markets'],
                'avoid': ['long outdoor exposure', 'water activities'],
                'packing': ['warm layers', 'gloves', 'warm boots', 'thermal wear']
            },
            'hot': {
                'recommended': ['early morning tours', 'air-conditioned venues', 'evening activities'],
                'avoid': ['midday outdoor activities', 'heavy physical activities'],
                'packing': ['cooling towel', 'extra water', 'breathable clothing', 'cooling gel']
            }
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process weather-related queries"""
        if message.msg_type == MessageType.QUERY:
            content = message.content
            
            if 'weather_optimization' in content:
                optimization = self._optimize_for_weather(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'weather_optimization': optimization}
                )
            elif 'packing_advice' in content:
                advice = self._generate_packing_advice(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'packing_advice': advice}
                )
        
        return None
    
    def generate_recommendation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate weather-based recommendations"""
        weather_forecast = context.get('weather_forecast', [])
        planned_activities = context.get('planned_activities', [])
        
        recommendation = {
            'agent': self.agent_id,
            'type': 'weather_optimization',
            'confidence': 0.8,
            'weather_insights': {},
            'activity_adjustments': [],
            'packing_recommendations': []
        }
        
        if weather_forecast:
            # Analyze weather patterns
            weather_summary = self._analyze_weather_patterns(weather_forecast)
            recommendation['weather_insights'] = weather_summary
            
            # Generate activity adjustments
            adjustments = self._suggest_activity_adjustments(weather_forecast, planned_activities)
            recommendation['activity_adjustments'] = adjustments
            
            # Generate packing advice
            packing_advice = self._comprehensive_packing_advice(weather_forecast)
            recommendation['packing_recommendations'] = packing_advice
            
            recommendation['confidence'] = 0.9
        
        return recommendation
    
    def _analyze_weather_patterns(self, forecast: List[Dict]) -> Dict[str, Any]:
        """Analyze weather patterns from forecast"""
        if not forecast:
            return {}
        
        conditions = [day.get('description', '').lower() for day in forecast]
        temperatures = [day.get('temperature', 20) for day in forecast]
        
        analysis = {
            'avg_temperature': sum(temperatures) / len(temperatures),
            'min_temperature': min(temperatures),
            'max_temperature': max(temperatures),
            'rainy_days': len([c for c in conditions if 'rain' in c or 'storm' in c]),
            'sunny_days': len([c for c in conditions if 'sun' in c or 'clear' in c]),
            'dominant_condition': max(set(conditions), key=conditions.count) if conditions else 'unknown',
            'temperature_variation': max(temperatures) - min(temperatures)
        }
        
        # Add insights
        insights = []
        if analysis['rainy_days'] > len(forecast) * 0.4:
            insights.append("Expect frequent rain - plan indoor alternatives")
        if analysis['temperature_variation'] > 15:
            insights.append("Large temperature variation - pack layers")
        if analysis['avg_temperature'] < 10:
            insights.append("Cold weather expected - pack warm clothing")
        elif analysis['avg_temperature'] > 25:
            insights.append("Hot weather expected - stay hydrated and seek shade")
        
        analysis['insights'] = insights
        
        return analysis
    
    def _suggest_activity_adjustments(self, forecast: List[Dict], activities: List[Dict]) -> List[Dict]:
        """Suggest activity adjustments based on weather"""
        adjustments = []
        
        for i, day_weather in enumerate(forecast):
            day_condition = self._categorize_weather_condition(day_weather)
            day_activities = [a for a in activities if a.get('day') == i + 1]
            
            weather_prefs = self.weather_activities.get(day_condition, {})
            recommended = weather_prefs.get('recommended', [])
            avoid = weather_prefs.get('avoid', [])
            
            for activity in day_activities:
                activity_type = activity.get('type', '').lower()
                
                # Check if activity should be avoided
                if any(avoid_item in activity_type for avoid_item in avoid):
                    adjustments.append({
                        'day': i + 1,
                        'activity': activity.get('name'),
                        'adjustment': 'consider_alternative',
                        'reason': f'Weather condition ({day_condition}) not ideal for this activity',
                        'alternatives': recommended[:3]
                    })
                
                # Suggest timing adjustments for hot weather
                elif day_condition == 'hot' and 'outdoor' in activity_type:
                    adjustments.append({
                        'day': i + 1,
                        'activity': activity.get('name'),
                        'adjustment': 'timing_change',
                        'reason': 'Hot weather - recommend early morning or evening',
                        'suggested_time': 'early morning (8-10 AM) or evening (6-8 PM)'
                    })
        
        return adjustments
    
    def _categorize_weather_condition(self, weather: Dict) -> str:
        """Categorize weather condition"""
        description = weather.get('description', '').lower()
        temperature = weather.get('temperature', 20)
        
        if 'rain' in description or 'storm' in description:
            return 'rainy'
        elif temperature < 10:
            return 'cold'
        elif temperature > 28:
            return 'hot'
        elif 'sun' in description or 'clear' in description:
            return 'sunny'
        else:
            return 'mild'
    
    def _comprehensive_packing_advice(self, forecast: List[Dict]) -> List[str]:
        """Generate comprehensive packing advice"""
        all_conditions = []
        temperatures = []
        
        for day_weather in forecast:
            condition = self._categorize_weather_condition(day_weather)
            all_conditions.append(condition)
            temperatures.append(day_weather.get('temperature', 20))
        
        packing_advice = set()
        
        # Add condition-specific items
        for condition in set(all_conditions):
            if condition in self.weather_activities:
                packing_advice.update(self.weather_activities[condition]['packing'])
        
        # Add temperature-based items
        min_temp = min(temperatures)
        max_temp = max(temperatures)
        
        if min_temp < 5:
            packing_advice.update(['heavy winter coat', 'thermal underwear', 'winter boots'])
        elif min_temp < 15:
            packing_advice.update(['warm jacket', 'long pants', 'closed shoes'])
        
        if max_temp > 25:
            packing_advice.update(['shorts', 'tank tops', 'sandals', 'sun hat'])
        
        # Add versatile items
        if max_temp - min_temp > 15:
            packing_advice.update(['layers', 'versatile jacket', 'multiple shoe options'])
        
        return list(packing_advice)
    
    def _optimize_for_weather(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize itinerary for weather conditions"""
        forecast = request.get('weather_forecast', [])
        itinerary = request.get('itinerary', [])
        
        optimization = {
            'original_plan': len(itinerary),
            'adjustments_made': 0,
            'optimized_itinerary': [],
            'weather_alerts': []
        }
        
        for day_plan in itinerary:
            day_num = day_plan.get('day', 1)
            if day_num <= len(forecast):
                weather = forecast[day_num - 1]
                condition = self._categorize_weather_condition(weather)
                
                # Optimize activities for weather
                optimized_day = day_plan.copy()
                activities = day_plan.get('activities', [])
                
                # Reorder activities based on weather
                if condition == 'rainy':
                    # Prioritize indoor activities
                    indoor_activities = [a for a in activities if 'indoor' in a.get('type', '').lower()]
                    outdoor_activities = [a for a in activities if 'outdoor' in a.get('type', '').lower()]
                    optimized_day['activities'] = indoor_activities + outdoor_activities
                elif condition == 'hot':
                    # Schedule outdoor activities for early/late hours
                    optimized_day['scheduling_note'] = 'Outdoor activities recommended for early morning or evening'
                
                optimization['optimized_itinerary'].append(optimized_day)
                
                # Add weather alerts
                if condition in ['rainy', 'cold', 'hot']:
                    optimization['weather_alerts'].append({
                        'day': day_num,
                        'condition': condition,
                        'alert': f'Weather condition: {condition} - check recommended adjustments'
                    })
                    optimization['adjustments_made'] += 1
        
        return optimization
    
    def _generate_packing_advice(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed packing advice"""
        forecast = request.get('weather_forecast', [])
        destination = request.get('destination', '')
        duration = request.get('duration', 3)
        
        advice = {
            'essential_items': [],
            'weather_specific': [],
            'optional_items': [],
            'packing_tips': []
        }
        
        if forecast:
            weather_items = self._comprehensive_packing_advice(forecast)
            advice['weather_specific'] = weather_items
        
        # Essential items for any trip
        advice['essential_items'] = [
            'passport/ID', 'phone charger', 'medications', 'comfortable walking shoes',
            'change of clothes', 'toiletries', 'travel insurance documents'
        ]
        
        # Duration-based suggestions
        if duration > 7:
            advice['optional_items'].extend(['laundry detergent', 'extra chargers', 'first aid kit'])
        
        # General packing tips
        advice['packing_tips'] = [
            'Pack light - you can buy items you forgot',
            'Bring layers for temperature changes',
            'Keep essential documents in carry-on',
            'Leave room for souvenirs',
            'Check airline baggage restrictions'
        ]
        
        return advice

class LocalExpertAgent(BaseAgent):
    """Local expert agent with insider knowledge and real-time insights"""
    
    def __init__(self):
        super().__init__(
            agent_id="local_expert",
            role=AgentRole.LOCAL_EXPERT,
            capabilities=["local_insights", "real_time_updates", "hidden_gems", "cultural_guidance"]
        )
        
        # Initialize local knowledge database
        self.local_insights = {
            'london': {
                'current_events': ['Thames Festival (Sept)', 'Christmas Markets (Dec)', 'Pride (June)'],
                'seasonal_tips': {
                    'spring': ['Cherry blossoms in Regent\'s Park', 'Easter events'],
                    'summer': ['Outdoor cinema in parks', 'Thames beach events'],
                    'autumn': ['Fall colors in Hyde Park', 'Halloween events'],
                    'winter': ['Ice skating rinks', 'Christmas lights on Oxford Street']
                },
                'local_favorites': ['Borough Market on Saturday mornings', 'Hampstead Heath walks', 'Free museums on Sundays'],
                'insider_tips': ['Avoid Oxford Street on weekends', 'Book restaurant tables in advance', 'Use citymapper app'],
                'current_closures': [],  # Would be updated in real-time
                'price_alerts': ['Transport strikes possible', 'Theatre booking deals midweek'],
                'safety_updates': ['Standard precautions in crowded areas', 'Beware of pickpockets on tube']
            },
            'paris': {
                'current_events': ['Fashion Week (Mar/Oct)', 'Nuit Blanche (Oct)', 'Fête de la Musique (June)'],
                'seasonal_tips': {
                    'spring': ['Café terraces open', 'Perfect for Seine walks'],
                    'summer': ['Paris Plages beach event', 'Long museum hours'],
                    'autumn': ['Harvest season in wine bars', 'Fewer crowds'],
                    'winter': ['Christmas markets', 'Cozy bistro season']
                },
                'local_favorites': ['Marché Saint-Germain', 'Evening Seine cruise', 'Père Lachaise at sunset'],
                'insider_tips': ['Learn basic French greetings', 'Many shops close for lunch', 'Sunday mornings are best for Louvre'],
                'current_closures': [],
                'price_alerts': ['Metro passes cheaper for longer stays', 'Museum passes save money'],
                'safety_updates': ['Standard city precautions', 'Keep valuables secure in crowds']
            },
            'tokyo': {
                'current_events': ['Cherry Blossom season (Mar-May)', 'Summer festivals (July-Aug)', 'Autumn leaves (Nov)'],
                'seasonal_tips': {
                    'spring': ['Hanami parties in parks', 'Peak tourist season'],
                    'summer': ['Hot and humid', 'Festival season'],
                    'autumn': ['Perfect weather', 'Beautiful fall colors'],
                    'winter': ['Cold but clear', 'Winter illuminations']
                },
                'local_favorites': ['Tsukiji Outer Market breakfast', 'Senso-ji at dawn', 'Golden Gai at night'],
                'insider_tips': ['Cash is still king', 'Learn basic bow etiquette', 'Download translation app'],
                'current_closures': [],
                'price_alerts': ['JR Pass must buy before arrival', 'Happy hour deals common'],
                'safety_updates': ['Extremely safe city', 'Natural disaster preparedness apps recommended']
            }
        }
        
        # Simulated real-time data sources
        self.real_time_sources = {
            'events': 'eventbrite_api',
            'weather': 'local_weather_updates',
            'transportation': 'transit_apps',
            'closures': 'official_tourism_sites',
            'safety': 'government_travel_advisories'
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process local expertise queries"""
        if message.msg_type == MessageType.QUERY:
            content = message.content
            
            if 'local_insights' in content:
                insights = self._provide_local_insights(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'local_insights': insights}
                )
            elif 'real_time_updates' in content:
                updates = self._get_real_time_updates(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'real_time_updates': updates}
                )
        
        return None
    
    def generate_recommendation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate local expert recommendations"""
        destination = context.get('destination', '').lower()
        visit_date = context.get('visit_date', datetime.now())
        interests = context.get('interests', [])
        
        recommendation = {
            'agent': self.agent_id,
            'type': 'local_expertise',
            'confidence': 0.9,
            'local_recommendations': {}
        }
        
        if destination in self.local_insights:
            local_data = self.local_insights[destination]
            
            # Seasonal recommendations
            season = self._get_season(visit_date)
            if season in local_data.get('seasonal_tips', {}):
                recommendation['local_recommendations']['seasonal_tips'] = local_data['seasonal_tips'][season]
            
            # Current events and festivals
            recommendation['local_recommendations']['current_events'] = local_data.get('current_events', [])
            
            # Local favorites and hidden gems
            recommendation['local_recommendations']['local_favorites'] = local_data.get('local_favorites', [])
            
            # Insider tips
            recommendation['local_recommendations']['insider_tips'] = local_data.get('insider_tips', [])
            
            # Safety and practical updates
            recommendation['local_recommendations']['safety_updates'] = local_data.get('safety_updates', [])
            recommendation['local_recommendations']['price_alerts'] = local_data.get('price_alerts', [])
            
            # Interest-specific local recommendations
            if 'food' in interests:
                recommendation['local_recommendations']['food_spots'] = self._get_local_food_spots(destination)
            if 'nightlife' in interests:
                recommendation['local_recommendations']['nightlife'] = self._get_nightlife_tips(destination)
            if 'shopping' in interests:
                recommendation['local_recommendations']['shopping'] = self._get_shopping_tips(destination)
        
        return recommendation
    
    def _provide_local_insights(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Provide detailed local insights"""
        destination = request.get('destination', '').lower()
        insight_type = request.get('insight_type', 'general')
        
        if destination not in self.local_insights:
            return {'error': f'No local insights available for {destination}'}
        
        local_data = self.local_insights[destination]
        
        insights = {
            'destination': destination,
            'insight_type': insight_type,
            'data': {}
        }
        
        if insight_type == 'general':
            insights['data'] = local_data
        elif insight_type in local_data:
            insights['data'] = local_data[insight_type]
        
        return insights
    
    def _get_real_time_updates(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate real-time updates (would connect to actual APIs)"""
        destination = request.get('destination', '').lower()
        
        # Simulated real-time data
        updates = {
            'timestamp': datetime.now().isoformat(),
            'destination': destination,
            'updates': {
                'transportation': f'Normal service on public transport in {destination}',
                'weather': 'Current conditions favorable for outdoor activities',
                'events': 'No major events causing disruption today',
                'attractions': 'All major attractions open with normal hours',
                'safety': 'No current travel advisories'
            }
        }
        
        return updates
    
    def _get_season(self, date: datetime) -> str:
        """Determine season based on date"""
        month = date.month
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'
    
    def _get_local_food_spots(self, destination: str) -> List[str]:
        """Get local food recommendations"""
        food_spots = {
            'london': ['Borough Market', 'Brick Lane curry houses', 'Traditional pubs for fish & chips'],
            'paris': ['Local bistros in Marais', 'Boulangeries for fresh pastries', 'Wine bars in Saint-Germain'],
            'tokyo': ['Tsukiji Outer Market', 'Ramen shops in Shibuya', 'Izakayas in Golden Gai']
        }
        return food_spots.get(destination, ['Explore local markets', 'Ask locals for recommendations'])
    
    def _get_nightlife_tips(self, destination: str) -> List[str]:
        """Get nightlife recommendations"""
        nightlife = {
            'london': ['West End for theatre', 'Shoreditch for trendy bars', 'Camden for live music'],
            'paris': ['Montmartre for cabaret', 'Latin Quarter for student bars', 'Champs-Élysées for clubs'],
            'tokyo': ['Golden Gai for tiny bars', 'Roppongi for international scene', 'Shibuya for karaoke']
        }
        return nightlife.get(destination, ['Check local event listings', 'Ask hotel concierge'])
    
    def _get_shopping_tips(self, destination: str) -> List[str]:
        """Get shopping recommendations"""
        shopping = {
            'london': ['Oxford Street for department stores', 'Camden Market for alternative', 'Portobello Road for antiques'],
            'paris': ['Champs-Élysées for luxury', 'Le Marais for boutiques', 'Flea markets for vintage'],
            'tokyo': ['Ginza for luxury', 'Harajuku for youth fashion', 'Akihabara for electronics']
        }
        return shopping.get(destination, ['Explore local shopping districts', 'Look for local markets'])


class ItineraryPlannerAgent(BaseAgent):
    """Specialized agent for creating optimized daily itineraries"""
    
    def __init__(self):
        super().__init__(
            agent_id="itinerary_planner",
            role=AgentRole.ITINERARY_PLANNER,
            capabilities=["route_optimization", "timing_coordination", "logistics_planning", "schedule_balancing"]
        )
        
        # Initialize planning algorithms and templates
        self.itinerary_templates = {
            'cultural': {
                'morning': ['Museums', 'Historical sites'],
                'afternoon': ['Cultural districts', 'Art galleries'],
                'evening': ['Traditional dining', 'Local performances']
            },
            'adventure': {
                'morning': ['Outdoor activities', 'Adventure sports'],
                'afternoon': ['Nature exploration', 'Active experiences'],
                'evening': ['Local cuisine', 'Relaxation']
            },
            'family': {
                'morning': ['Family-friendly attractions', 'Interactive museums'],
                'afternoon': ['Parks', 'Kid-friendly activities'],
                'evening': ['Family restaurants', 'Early entertainment']
            },
            'romantic': {
                'morning': ['Scenic walks', 'Peaceful attractions'],
                'afternoon': ['Couples activities', 'Shopping'],
                'evening': ['Fine dining', 'Romantic experiences']
            }
        }
        
        # Transportation and timing knowledge
        self.transport_times = {
            'london': {'walking': 15, 'tube': 8, 'bus': 12, 'taxi': 10},
            'paris': {'walking': 12, 'metro': 6, 'bus': 15, 'taxi': 8},
            'tokyo': {'walking': 10, 'train': 5, 'bus': 20, 'taxi': 15}
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process itinerary planning requests"""
        if message.msg_type == MessageType.QUERY:
            content = message.content
            
            if 'create_itinerary' in content:
                itinerary = self._create_detailed_itinerary(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'itinerary': itinerary}
                )
            elif 'optimize_schedule' in content:
                optimized = self._optimize_schedule(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'optimized_schedule': optimized}
                )
        
        return None
    
    def generate_recommendation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimized itinerary recommendations"""
        destination = context.get('destination', '').lower()
        duration = context.get('duration', 3)
        interests = context.get('interests', [])
        attractions = context.get('attractions', [])
        weather_forecast = context.get('weather_forecast', [])
        
        recommendation = {
            'agent': self.agent_id,
            'type': 'itinerary_planning',
            'confidence': 0.85,
            'daily_plans': [],
            'optimization_notes': []
        }
        
        # Create daily itineraries
        for day in range(duration):
            daily_plan = self._create_daily_plan(
                day + 1, destination, interests, attractions, 
                weather_forecast[day] if day < len(weather_forecast) else None
            )
            recommendation['daily_plans'].append(daily_plan)
        
        # Add optimization suggestions
        recommendation['optimization_notes'] = [
            'Schedule adjusted for weather conditions',
            'Transport time optimized between locations',
            'Activities grouped by geographical proximity',
            'Rest periods included for optimal energy management'
        ]
        
        return recommendation
    
    def _create_detailed_itinerary(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive daily itinerary"""
        attractions = request.get('attractions', [])
        preferences = request.get('preferences', {})
        weather_info = request.get('weather', {})
        
        itinerary = {
            'total_days': len(attractions) if isinstance(attractions, list) else 1,
            'daily_schedules': [],
            'logistics': {
                'recommended_transport': 'public_transport',
                'estimated_walking_time': '2-3 hours daily',
                'rest_breaks': 'Every 2-3 activities'
            }
        }
        
        # Create schedule for each day
        for day_num in range(itinerary['total_days']):
            daily_schedule = {
                'day': day_num + 1,
                'morning': {'time': '9:00-12:00', 'activities': []},
                'afternoon': {'time': '13:00-17:00', 'activities': []},
                'evening': {'time': '18:00-21:00', 'activities': []}
            }
            
            # Distribute activities based on type and weather
            if isinstance(attractions, list) and attractions:
                day_attractions = attractions[:3]  # Limit to 3 per day
                attractions = attractions[3:]  # Remove used attractions
                
                # Assign to time slots
                if day_attractions:
                    daily_schedule['morning']['activities'].append(day_attractions[0])
                if len(day_attractions) > 1:
                    daily_schedule['afternoon']['activities'].append(day_attractions[1])
                if len(day_attractions) > 2:
                    daily_schedule['evening']['activities'].append(day_attractions[2])
            
            itinerary['daily_schedules'].append(daily_schedule)
        
        return itinerary
    
    def _create_daily_plan(self, day_number: int, destination: str, interests: List[str], 
                          attractions: List[str], weather: Optional[Dict]) -> Dict[str, Any]:
        """Create optimized plan for a single day"""
        
        # Determine plan type based on interests
        plan_type = 'cultural'  # default
        if 'adventure' in interests or 'outdoor' in interests:
            plan_type = 'adventure'
        elif 'family' in interests:
            plan_type = 'family'
        elif 'romantic' in interests:
            plan_type = 'romantic'
        
        template = self.itinerary_templates.get(plan_type, self.itinerary_templates['cultural'])
        
        daily_plan = {
            'day': day_number,
            'theme': plan_type.title(),
            'weather_consideration': self._get_weather_adjustment(weather),
            'schedule': {
                'morning': {
                    'time': '9:00 AM - 12:00 PM',
                    'focus': template['morning'][0] if template['morning'] else 'Exploration',
                    'activities': attractions[:2] if attractions else ['Explore local area'],
                    'transport_notes': 'Start with closest attractions'
                },
                'afternoon': {
                    'time': '1:00 PM - 5:00 PM',
                    'focus': template['afternoon'][0] if template['afternoon'] else 'Discovery',
                    'activities': attractions[2:4] if len(attractions) > 2 else ['Lunch and exploration'],
                    'transport_notes': 'Use public transport between districts'
                },
                'evening': {
                    'time': '6:00 PM - 9:00 PM',
                    'focus': template['evening'][0] if template['evening'] else 'Dining',
                    'activities': attractions[4:5] if len(attractions) > 4 else ['Local dining experience'],
                    'transport_notes': 'Walking preferred for evening activities'
                }
            },
            'estimated_costs': {
                'transport': 15,
                'attractions': 45,
                'meals': 60
            },
            'energy_level': 'High morning, moderate afternoon, relaxed evening'
        }
        
        return daily_plan
    
    def _optimize_schedule(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize existing schedule for better flow"""
        current_schedule = request.get('schedule', {})
        optimization_criteria = request.get('criteria', ['time', 'cost', 'energy'])
        
        optimized = {
            'original_schedule': current_schedule,
            'optimizations_applied': [],
            'improved_schedule': current_schedule.copy(),  # Would apply actual optimizations
            'estimated_improvements': {
                'time_saved': '30-45 minutes per day',
                'cost_reduction': '10-15%',
                'energy_efficiency': '20% better pacing'
            }
        }
        
        # Add optimization notes
        for criteria in optimization_criteria:
            if criteria == 'time':
                optimized['optimizations_applied'].append('Reorganized activities by geographical proximity')
            elif criteria == 'cost':
                optimized['optimizations_applied'].append('Grouped activities with combo tickets')
            elif criteria == 'energy':
                optimized['optimizations_applied'].append('Balanced high and low energy activities')
        
        return optimized
    
    def _get_weather_adjustment(self, weather: Optional[Dict]) -> str:
        """Get weather-based adjustments for the day"""
        if not weather:
            return 'No weather data available'
        
        condition = weather.get('condition', '').lower()
        if 'rain' in condition:
            return 'Indoor activities prioritized due to rain'
        elif 'snow' in condition:
            return 'Warm indoor venues recommended'
        elif 'sunny' in condition:
            return 'Great day for outdoor exploration'
        elif 'cloud' in condition:
            return 'Perfect for walking and sightseeing'
        
        return 'Weather conditions considered in planning'


class CoordinatorAgent(BaseAgent):
    """Master coordinator agent that orchestrates all other agents"""
    
    def __init__(self):
        super().__init__(
            agent_id="coordinator",
            role=AgentRole.COORDINATOR,
            capabilities=["agent_orchestration", "decision_synthesis", "conflict_resolution", "workflow_management"]
        )
        
        # Define agent coordination workflows
        self.coordination_workflows = {
            'full_trip_planning': [
                {'agent': 'travel_advisor', 'task': 'destination_analysis'},
                {'agent': 'weather_analyst', 'task': 'weather_forecast'},
                {'agent': 'local_expert', 'task': 'local_insights'},
                {'agent': 'budget_optimizer', 'task': 'cost_analysis'},
                {'agent': 'itinerary_planner', 'task': 'schedule_creation'}
            ],
            'budget_optimization': [
                {'agent': 'budget_optimizer', 'task': 'primary_analysis'},
                {'agent': 'local_expert', 'task': 'cost_saving_tips'},
                {'agent': 'travel_advisor', 'task': 'alternative_suggestions'}
            ],
            'weather_adaptation': [
                {'agent': 'weather_analyst', 'task': 'forecast_update'},
                {'agent': 'itinerary_planner', 'task': 'schedule_adjustment'},
                {'agent': 'local_expert', 'task': 'indoor_alternatives'}
            ]
        }
        
        # Agent priority system
        self.agent_priorities = {
            'safety_concern': ['local_expert', 'travel_advisor'],
            'budget_concern': ['budget_optimizer', 'local_expert'],
            'weather_concern': ['weather_analyst', 'itinerary_planner'],
            'logistics_concern': ['itinerary_planner', 'travel_advisor']
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process coordination requests"""
        if message.msg_type == MessageType.REQUEST:
            content = message.content
            
            if 'coordinate_planning' in content:
                plan = self._coordinate_trip_planning(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'coordinated_plan': plan}
                )
            elif 'resolve_conflict' in content:
                resolution = self._resolve_agent_conflict(content)
                return Message(
                    self.agent_id, message.sender, MessageType.RESPONSE,
                    {'conflict_resolution': resolution}
                )
        
        return None
    
    def generate_recommendation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate all agents to generate comprehensive recommendation"""
        planning_type = context.get('planning_type', 'full_trip_planning')
        user_priorities = context.get('priorities', [])
        
        recommendation = {
            'agent': self.agent_id,
            'type': 'coordinated_planning',
            'confidence': 0.95,
            'coordination_summary': {},
            'final_recommendation': {},
            'agent_contributions': {},
            'decision_rationale': []
        }
        
        # Execute coordination workflow
        workflow = self.coordination_workflows.get(planning_type, 
                                                  self.coordination_workflows['full_trip_planning'])
        
        for step in workflow:
            agent_role = step['agent']
            task = step['task']
            
            # Simulate agent consultation (in real implementation, would call actual agents)
            agent_input = self._simulate_agent_consultation(agent_role, task, context)
            recommendation['agent_contributions'][agent_role] = agent_input
        
        # Synthesize all agent inputs
        final_plan = self._synthesize_agent_inputs(
            recommendation['agent_contributions'], context, user_priorities
        )
        
        recommendation['final_recommendation'] = final_plan
        recommendation['coordination_summary'] = {
            'agents_consulted': len(workflow),
            'consensus_level': 0.85,
            'conflicts_resolved': 0,
            'optimization_applied': True
        }
        
        # Add decision rationale
        recommendation['decision_rationale'] = [
            'Combined expertise from all specialized agents',
            'Prioritized user preferences and constraints',
            'Optimized for best overall travel experience',
            'Balanced multiple factors (cost, weather, logistics, local insights)'
        ]
        
        return recommendation
    
    def _coordinate_trip_planning(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate comprehensive trip planning"""
        trip_context = request.get('trip_context', {})
        user_preferences = request.get('preferences', {})
        
        coordination_plan = {
            'coordination_id': f"coord_{int(datetime.now().timestamp())}",
            'trip_context': trip_context,
            'agent_assignments': {},
            'execution_order': [],
            'expected_completion': 'Within 5 minutes',
            'quality_metrics': {
                'completeness': 0.9,
                'consistency': 0.85,
                'user_alignment': 0.88
            }
        }
        
        # Assign tasks to agents based on trip context
        if trip_context.get('budget_conscious'):
            coordination_plan['agent_assignments']['budget_optimizer'] = 'Primary cost analysis and optimization'
            coordination_plan['execution_order'].append('budget_optimizer')
        
        if trip_context.get('weather_sensitive'):
            coordination_plan['agent_assignments']['weather_analyst'] = 'Weather impact analysis'
            coordination_plan['execution_order'].append('weather_analyst')
        
        # Always include core agents
        coordination_plan['agent_assignments']['travel_advisor'] = 'Destination expertise and recommendations'
        coordination_plan['agent_assignments']['local_expert'] = 'Local insights and real-time updates'
        coordination_plan['agent_assignments']['itinerary_planner'] = 'Schedule optimization and logistics'
        
        coordination_plan['execution_order'].extend(['travel_advisor', 'local_expert', 'itinerary_planner'])
        
        return coordination_plan
    
    def _resolve_agent_conflict(self, conflict_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflicts between agent recommendations"""
        conflicting_agents = conflict_data.get('agents', [])
        conflict_type = conflict_data.get('type', 'recommendation_mismatch')
        
        resolution = {
            'conflict_type': conflict_type,
            'involved_agents': conflicting_agents,
            'resolution_strategy': 'weighted_consensus',
            'final_decision': {},
            'compromise_elements': [],
            'confidence': 0.8
        }
        
        # Apply resolution strategy based on conflict type
        if conflict_type == 'budget_vs_quality':
            resolution['final_decision'] = 'Optimize for mid-range options with selective premium choices'
            resolution['compromise_elements'] = [
                'Mix budget and premium accommodations',
                'Prioritize experiences over material comforts',
                'Use local alternatives for some meals'
            ]
        elif conflict_type == 'indoor_vs_outdoor':
            resolution['final_decision'] = 'Weather-adaptive flexible planning'
            resolution['compromise_elements'] = [
                'Primary outdoor plan with indoor backups',
                'Weather monitoring with day-of adjustments',
                'Mix of both activity types'
            ]
        
        return resolution
    
    def _simulate_agent_consultation(self, agent_role: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate consultation with specialized agent"""
        # This would call actual agents in full implementation
        simulated_responses = {
            'travel_advisor': {
                'expertise_level': 'high',
                'recommendations': ['Visit top attractions', 'Explore local culture', 'Try regional cuisine'],
                'confidence': 0.9
            },
            'budget_optimizer': {
                'cost_analysis': 'Moderate budget required',
                'savings_opportunities': ['Group discounts', 'Off-season pricing', 'Local transport'],
                'confidence': 0.85
            },
            'weather_analyst': {
                'forecast_summary': 'Generally favorable conditions',
                'recommendations': ['Pack layers', 'Plan indoor alternatives', 'Check daily updates'],
                'confidence': 0.8
            },
            'local_expert': {
                'insider_knowledge': 'High local expertise available',
                'special_recommendations': ['Hidden gems', 'Local events', 'Cultural tips'],
                'confidence': 0.9
            },
            'itinerary_planner': {
                'logistics_assessment': 'Efficient routing possible',
                'optimization_potential': ['Time savings', 'Transport efficiency', 'Energy management'],
                'confidence': 0.85
            }
        }
        
        return simulated_responses.get(agent_role, {'confidence': 0.5, 'status': 'limited_data'})
    
    def _synthesize_agent_inputs(self, agent_inputs: Dict[str, Dict], context: Dict[str, Any], 
                                priorities: List[str]) -> Dict[str, Any]:
        """Synthesize inputs from all agents into final recommendation"""
        synthesis = {
            'destination_plan': {},
            'budget_plan': {},
            'schedule_plan': {},
            'contingency_plan': {},
            'overall_confidence': 0.85
        }
        
        # Extract key information from each agent
        if 'travel_advisor' in agent_inputs:
            synthesis['destination_plan'] = {
                'attractions': agent_inputs['travel_advisor'].get('recommendations', []),
                'cultural_insights': 'Comprehensive destination expertise applied'
            }
        
        if 'budget_optimizer' in agent_inputs:
            synthesis['budget_plan'] = {
                'cost_estimate': 'Optimized for user budget range',
                'savings_strategies': agent_inputs['budget_optimizer'].get('savings_opportunities', [])
            }
        
        if 'itinerary_planner' in agent_inputs:
            synthesis['schedule_plan'] = {
                'daily_structure': 'Optimized for efficiency and enjoyment',
                'logistics': 'Transport and timing coordinated'
            }
        
        # Add contingency planning
        synthesis['contingency_plan'] = {
            'weather_backup': 'Indoor alternatives identified',
            'budget_flexibility': 'Cost adjustment options available',
            'schedule_adaptation': 'Flexible timing for key activities'
        }
        
        return synthesis
