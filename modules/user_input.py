# Handles user input
import re
from datetime import datetime, date, timedelta
from typing import Dict, Any, Tuple, List, Optional

class UserInputHandler:
    """Handles and validates user input for trip planning"""
    
    def __init__(self):
        self.valid_currencies = ['USD', 'EUR', 'GBP', 'INR', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'SGD']
        self.budget_ranges = ['budget', 'mid-range', 'luxury']
        self.popular_destinations = [
            'New York', 'London', 'Paris', 'Tokyo', 'Sydney', 'Dubai', 'Singapore',
            'Barcelona', 'Amsterdam', 'Rome', 'Istanbul', 'Bangkok', 'Mumbai',
            'Berlin', 'Vienna', 'Prague', 'Lisbon', 'Copenhagen', 'Stockholm'
        ]
        self.common_interests = [
            'museums', 'art', 'history', 'food', 'nightlife', 'shopping', 'nature',
            'adventure', 'culture', 'architecture', 'photography', 'music', 'sports',
            'beaches', 'mountains', 'festivals', 'local experiences', 'luxury'
        ]
    
    def get_trip_details(self) -> Dict[str, Any]:
        """Collect all trip details from user with comprehensive validation"""
        
        print("🌍 Welcome to AI Travel Agent & Expense Planner!")
        print("=" * 60)
        print("Let's plan your perfect trip! Please provide the following details:")
        print("-" * 60)
        
        # Get basic trip information
        destination = self._get_destination()
        start_date, end_date, total_days = self._get_dates()
        budget_range = self._get_budget_range()
        currency = self._get_currency()
        group_size = self._get_group_size()
        
        # Get preferences and special requirements
        preferences = self._get_preferences()
        
        # Get additional options
        additional_options = self._get_additional_options()
        
        trip_details = {
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'total_days': total_days,
            'budget_range': budget_range,
            'currency': currency,
            'group_size': group_size,
            'preferences': preferences,
            'additional_options': additional_options,
            'input_timestamp': datetime.now()
        }
        
        return trip_details
    
    def _get_destination(self) -> str:
        """Get and validate destination with suggestions"""
        print("\n📍 DESTINATION")
        print("Popular destinations:", ", ".join(self.popular_destinations[:10]))
        
        while True:
            destination = input("\nEnter your destination city: ").strip()
            
            if not destination:
                print("❌ Please enter a destination.")
                continue
            
            if len(destination) < 2:
                print("❌ Please enter a valid city name (at least 2 characters).")
                continue
            
            # Check for numbers or special characters
            if not re.match(r'^[a-zA-Z\s\-\'\.]+$', destination):
                print("❌ Please enter a valid city name (letters, spaces, hyphens, and apostrophes only).")
                continue
            
            # Capitalize properly
            destination = destination.title()
            
            # Confirm unusual destinations
            if destination not in self.popular_destinations:
                confirm = input(f"Did you mean '{destination}'? (y/n): ").lower().strip()
                if confirm not in ['y', 'yes']:
                    continue
            
            return destination
    
    def _get_dates(self) -> Tuple[date, date, int]:
        """Get and validate travel dates with intelligent suggestions"""
        print("\n📅 TRAVEL DATES")
        print("Format: YYYY-MM-DD (e.g., 2025-12-25)")
        
        while True:
            try:
                # Get start date
                start_input = input("\nEnter start date: ").strip()
                if not start_input:
                    print("❌ Start date is required.")
                    continue
                
                start_date = datetime.strptime(start_input, "%Y-%m-%d").date()
                
                # Validate start date
                if start_date < date.today():
                    print("❌ Start date cannot be in the past.")
                    continue
                
                if start_date > date.today() + timedelta(days=365):
                    confirm = input("⚠️  That's quite far in the future. Are you sure? (y/n): ").lower()
                    if confirm not in ['y', 'yes']:
                        continue
                
                # Get end date
                end_input = input("Enter end date: ").strip()
                if not end_input:
                    print("❌ End date is required.")
                    continue
                
                end_date = datetime.strptime(end_input, "%Y-%m-%d").date()
                
                # Validate end date
                if end_date <= start_date:
                    print("❌ End date must be after start date.")
                    continue
                
                total_days = (end_date - start_date).days
                
                # Validate trip duration
                if total_days > 90:
                    confirm = input(f"⚠️  That's a {total_days}-day trip! Are you sure? (y/n): ").lower()
                    if confirm not in ['y', 'yes']:
                        continue
                
                # Show trip summary
                print(f"✅ Trip duration: {total_days} days")
                
                # Suggest optimal duration
                if total_days < 2:
                    print("💡 Consider extending to at least 2-3 days for a more fulfilling experience.")
                elif total_days > 14:
                    print("💡 For trips longer than 2 weeks, consider planning multiple destinations.")
                
                return start_date, end_date, total_days
                
            except ValueError:
                print("❌ Please enter dates in YYYY-MM-DD format (e.g., 2025-12-25).")
    
    def _get_budget_range(self) -> str:
        """Get budget preference with detailed explanations"""
        print("\n💰 BUDGET RANGE")
        print("Choose your budget category:")
        print("1. Budget      - Hostels, street food, public transport (~$50-80/day)")
        print("2. Mid-range   - Hotels, restaurants, mixed transport (~$100-150/day)")
        print("3. Luxury      - Premium hotels, fine dining, private transport (~$200+/day)")
        
        while True:
            try:
                choice = input("\nSelect budget range (1-3) or type the name: ").strip().lower()
                
                if choice in ['1', 'budget']:
                    print("✅ Budget travel selected - Great for backpackers and cost-conscious travelers!")
                    return 'budget'
                elif choice in ['2', 'mid-range', 'mid', 'middle']:
                    print("✅ Mid-range travel selected - Perfect balance of comfort and value!")
                    return 'mid-range'
                elif choice in ['3', 'luxury', 'premium', 'high-end']:
                    print("✅ Luxury travel selected - Experience the finest accommodations and services!")
                    return 'luxury'
                else:
                    print("❌ Please select 1, 2, 3 or type 'budget', 'mid-range', or 'luxury'.")
                    
            except KeyboardInterrupt:
                raise
            except:
                print("❌ Please enter a valid selection.")
    
    def _get_currency(self) -> str:
        """Get preferred currency with exchange rate info"""
        print(f"\n💱 CURRENCY")
        print("Supported currencies:")
        print("USD (US Dollar)    EUR (Euro)         GBP (British Pound)")
        print("INR (Indian Rupee) JPY (Japanese Yen) CAD (Canadian Dollar)")
        print("AUD (Australian $) CHF (Swiss Franc)  CNY (Chinese Yuan)")
        print("SGD (Singapore $)")
        
        while True:
            currency = input("\nEnter your preferred currency (default: USD): ").upper().strip()
            
            if not currency:
                print("✅ Using USD as default currency.")
                return "USD"
            
            if currency in self.valid_currencies:
                print(f"✅ Currency set to {currency}")
                if currency != 'USD':
                    print("💡 All costs will be calculated in USD first, then converted to your currency.")
                return currency
            else:
                print(f"❌ '{currency}' is not supported.")
                print(f"Supported currencies: {', '.join(self.valid_currencies)}")
    
    def _get_group_size(self) -> int:
        """Get number of travelers with group discounts info"""
        print("\n👥 GROUP SIZE")
        
        while True:
            try:
                size_input = input("Number of travelers (including yourself): ").strip()
                
                if not size_input:
                    print("❌ Please enter the number of travelers.")
                    continue
                
                size = int(size_input)
                
                if size <= 0:
                    print("❌ Group size must be at least 1.")
                    continue
                
                if size > 20:
                    confirm = input(f"⚠️  That's a large group of {size} people. Are you sure? (y/n): ").lower()
                    if confirm not in ['y', 'yes']:
                        continue
                
                # Provide group-specific advice
                if size == 1:
                    print("✅ Solo travel - Perfect for flexibility and self-discovery!")
                elif size == 2:
                    print("✅ Couple/pair travel - Great for romantic getaways or friend trips!")
                elif size <= 4:
                    print("✅ Small group - Ideal for family trips or close friends!")
                elif size <= 8:
                    print("✅ Medium group - Consider booking group accommodations!")
                    print("💡 You may qualify for group discounts on activities and tours.")
                else:
                    print("✅ Large group - Definitely look into group rates and bulk bookings!")
                    print("💡 Consider splitting into smaller groups for some activities.")
                
                return size
                
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def _get_preferences(self) -> Dict[str, Any]:
        """Get detailed user preferences and requirements"""
        print("\n🎯 TRAVEL PREFERENCES")
        print("Help us personalize your trip by sharing your interests and requirements.")
        
        preferences = {}
        
        # Interests
        print(f"\nInterests (comma-separated):")
        print(f"Examples: {', '.join(self.common_interests[:12])}")
        interests_input = input("Your interests (press Enter to skip): ").strip()
        
        if interests_input:
            interests = [interest.strip().lower() for interest in interests_input.split(',')]
            # Validate and suggest corrections
            valid_interests = []
            for interest in interests:
                if interest in self.common_interests:
                    valid_interests.append(interest)
                else:
                    # Find close matches
                    suggestions = [ci for ci in self.common_interests if interest in ci or ci in interest]
                    if suggestions:
                        print(f"💡 Did you mean '{suggestions[0]}' instead of '{interest}'?")
                        confirm = input("(y/n): ").lower().strip()
                        if confirm in ['y', 'yes']:
                            valid_interests.append(suggestions[0])
                        else:
                            valid_interests.append(interest)  # Keep original
                    else:
                        valid_interests.append(interest)  # Keep original
            
            preferences['interests'] = valid_interests
            print(f"✅ Interests recorded: {', '.join(valid_interests)}")
        else:
            preferences['interests'] = []
        
        # Dietary restrictions
        dietary = input("\nDietary restrictions/preferences (vegetarian, vegan, halal, etc.): ").strip()
        preferences['dietary_restrictions'] = dietary
        if dietary:
            print(f"✅ Dietary preferences noted: {dietary}")
        
        # Mobility considerations
        mobility = input("Mobility considerations or accessibility needs: ").strip()
        preferences['mobility'] = mobility
        if mobility:
            print(f"✅ Accessibility needs noted: {mobility}")
        
        # Activity level
        print("\nPreferred activity level:")
        print("1. Relaxed - Minimal walking, leisure activities")
        print("2. Moderate - Some walking, balanced itinerary") 
        print("3. Active - Lots of walking, adventure activities")
        
        while True:
            activity_level = input("Select activity level (1-3): ").strip()
            if activity_level in ['1']:
                preferences['activity_level'] = 'relaxed'
                print("✅ Relaxed pace selected - Perfect for a laid-back vacation!")
                break
            elif activity_level in ['2']:
                preferences['activity_level'] = 'moderate'
                print("✅ Moderate pace selected - Good balance of activities and rest!")
                break
            elif activity_level in ['3']:
                preferences['activity_level'] = 'active'
                print("✅ Active pace selected - Adventure awaits!")
                break
            else:
                print("❌ Please select 1, 2, or 3.")
        
        # Travel style
        print("\nTravel style:")
        print("1. Tourist - Popular attractions and experiences")
        print("2. Explorer - Mix of popular and off-the-beaten-path")
        print("3. Local - Authentic, local experiences")
        
        while True:
            travel_style = input("Select travel style (1-3): ").strip()
            if travel_style in ['1']:
                preferences['travel_style'] = 'tourist'
                print("✅ Tourist style - You'll see all the must-visit spots!")
                break
            elif travel_style in ['2']:
                preferences['travel_style'] = 'explorer'
                print("✅ Explorer style - Perfect mix of famous and hidden gems!")
                break
            elif travel_style in ['3']:
                preferences['travel_style'] = 'local'
                print("✅ Local style - Authentic cultural immersion!")
                break
            else:
                print("❌ Please select 1, 2, or 3.")
        
        return preferences
    
    def _get_additional_options(self) -> Dict[str, Any]:
        """Get additional options and special requests"""
        print("\n⚙️  ADDITIONAL OPTIONS")
        options = {}
        
        # Transportation preferences
        print("Transportation preferences:")
        print("1. Public transport preferred")
        print("2. Mix of transport options")
        print("3. Private transport preferred")
        
        while True:
            transport = input("Select preference (1-3, or press Enter for default): ").strip()
            if not transport or transport == '2':
                options['transport_preference'] = 'mixed'
                break
            elif transport == '1':
                options['transport_preference'] = 'public'
                print("✅ Public transport preferred - Eco-friendly and budget-conscious!")
                break
            elif transport == '3':
                options['transport_preference'] = 'private'
                print("✅ Private transport preferred - Comfort and convenience!")
                break
            else:
                print("❌ Please select 1, 2, or 3.")
        
        # Accommodation preferences
        accommodation_prefs = input("\nAccommodation preferences (hotel, hostel, airbnb, etc.): ").strip().lower()
        options['accommodation_preference'] = accommodation_prefs
        
        # Special occasions
        special_occasion = input("Special occasion (anniversary, birthday, honeymoon, etc.): ").strip()
        options['special_occasion'] = special_occasion
        if special_occasion:
            print(f"✅ Special occasion noted: {special_occasion} - We'll make it memorable!")
        
        # Additional requests
        additional_requests = input("Any other special requests or requirements: ").strip()
        options['additional_requests'] = additional_requests
        
        return options
    
    def confirm_details(self, details: Dict[str, Any]) -> bool:
        """Display comprehensive trip summary and confirm details"""
        print("\n" + "="*70)
        print("📋 COMPLETE TRIP SUMMARY")
        print("="*70)
        
        # Basic Information
        print(f"🌍 Destination: {details['destination']}")
        print(f"📅 Travel Dates: {details['start_date']} to {details['end_date']}")
        print(f"⏰ Duration: {details['total_days']} days")
        print(f"👥 Group Size: {details['group_size']} traveler(s)")
        print(f"💰 Budget Range: {details['budget_range'].title()}")
        print(f"💱 Currency: {details['currency']}")
        
        # Preferences
        preferences = details.get('preferences', {})
        if preferences.get('interests'):
            print(f"🎯 Interests: {', '.join(preferences['interests'])}")
        
        if preferences.get('activity_level'):
            print(f"🚶 Activity Level: {preferences['activity_level'].title()}")
        
        if preferences.get('travel_style'):
            print(f"✈️  Travel Style: {preferences['travel_style'].title()}")
        
        if preferences.get('dietary_restrictions'):
            print(f"🍽️  Dietary: {preferences['dietary_restrictions']}")
        
        # Additional Options
        additional = details.get('additional_options', {})
        if additional.get('transport_preference'):
            print(f"🚌 Transport: {additional['transport_preference'].title()} preferred")
        
        if additional.get('special_occasion'):
            print(f"🎉 Special Occasion: {additional['special_occasion']}")
        
        print("="*70)
        
        # Cost estimate preview
        self._show_cost_preview(details)
        
        print("\n" + "="*70)
        
        while True:
            print("\nOptions:")
            print("1. Confirm and continue")
            print("2. Edit details")
            print("3. Cancel")
            
            choice = input("Please select (1-3): ").strip()
            
            if choice == '1':
                print("✅ Details confirmed! Let's plan your amazing trip...")
                return True
            elif choice == '2':
                return self._edit_details(details)
            elif choice == '3':
                confirm_cancel = input("Are you sure you want to cancel? (y/n): ").lower().strip()
                if confirm_cancel in ['y', 'yes']:
                    print("❌ Trip planning cancelled.")
                    return False
            else:
                print("❌ Please select 1, 2, or 3.")
    
    def _show_cost_preview(self, details: Dict[str, Any]) -> None:
        """Show estimated cost preview based on inputs"""
        budget_range = details['budget_range']
        days = details['total_days']
        group_size = details['group_size']
        
        # Rough estimates per person per day
        daily_estimates = {
            'budget': 60,
            'mid-range': 120,
            'luxury': 250
        }
        
        daily_cost = daily_estimates.get(budget_range, 120)
        total_per_person = daily_cost * days
        total_for_group = total_per_person * group_size
        
        print(f"\n💡 ROUGH COST ESTIMATE ({details['currency']})")
        print(f"   Daily per person: ~{daily_cost}")
        print(f"   Total per person: ~{total_per_person:,}")
        print(f"   Total for group: ~{total_for_group:,}")
        print("   (This is a rough estimate - detailed costs will be calculated next)")
    
    def _edit_details(self, details: Dict[str, Any]) -> bool:
        """Allow user to edit specific details"""
        print("\n📝 EDIT TRIP DETAILS")
        print("What would you like to change?")
        print("1. Destination")
        print("2. Dates")
        print("3. Budget range")
        print("4. Currency")
        print("5. Group size")
        print("6. Preferences")
        print("7. Go back to confirmation")
        
        while True:
            choice = input("Select what to edit (1-7): ").strip()
            
            if choice == '1':
                details['destination'] = self._get_destination()
            elif choice == '2':
                start_date, end_date, total_days = self._get_dates()
                details['start_date'] = start_date
                details['end_date'] = end_date
                details['total_days'] = total_days
            elif choice == '3':
                details['budget_range'] = self._get_budget_range()
            elif choice == '4':
                details['currency'] = self._get_currency()
            elif choice == '5':
                details['group_size'] = self._get_group_size()
            elif choice == '6':
                details['preferences'] = self._get_preferences()
            elif choice == '7':
                return self.confirm_details(details)
            else:
                print("❌ Please select 1-7.")
                continue
            
            print("✅ Details updated!")
            
            # Ask if they want to edit more or confirm
            while True:
                next_action = input("Edit more details (e) or confirm (c)? ").lower().strip()
                if next_action in ['e', 'edit']:
                    break
                elif next_action in ['c', 'confirm']:
                    return self.confirm_details(details)
                else:
                    print("❌ Please enter 'e' for edit or 'c' for confirm.")
    
    def get_quick_trip_details(self) -> Dict[str, Any]:
        """Quick mode for experienced users"""
        print("🚀 QUICK TRIP SETUP")
        print("For experienced users - minimal questions!")
        
        destination = input("Destination: ").strip().title()
        start_date = datetime.strptime(input("Start date (YYYY-MM-DD): "), "%Y-%m-%d").date()
        end_date = datetime.strptime(input("End date (YYYY-MM-DD): "), "%Y-%m-%d").date()
        budget_range = input("Budget (budget/mid-range/luxury): ").lower().strip()
        
        if budget_range not in self.budget_ranges:
            budget_range = 'mid-range'
        
        return {
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'total_days': (end_date - start_date).days,
            'budget_range': budget_range,
            'currency': 'USD',
            'group_size': 1,
            'preferences': {'interests': [], 'activity_level': 'moderate', 'travel_style': 'tourist'},
            'additional_options': {},
            'input_timestamp': datetime.now()
        }
    
    def validate_input_completeness(self, details: Dict[str, Any]) -> List[str]:
        """Validate that all required information is present"""
        issues = []
        
        required_fields = ['destination', 'start_date', 'end_date', 'budget_range', 'currency', 'group_size']
        
        for field in required_fields:
            if field not in details or not details[field]:
                issues.append(f"Missing {field}")
        
        # Date validation
        if 'start_date' in details and 'end_date' in details:
            if details['start_date'] >= details['end_date']:
                issues.append("End date must be after start date")
            
            if details['start_date'] < date.today():
                issues.append("Start date cannot be in the past")
        
        # Budget validation
        if details.get('budget_range') not in self.budget_ranges:
            issues.append("Invalid budget range")
        
        # Currency validation
        if details.get('currency') not in self.valid_currencies:
            issues.append("Invalid currency")
        
        # Group size validation
        if not isinstance(details.get('group_size'), int) or details.get('group_size', 0) <= 0:
            issues.append("Invalid group size")
        
        return issues