# Currency conversion logic
import requests
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from config.api_config import api_config

class CurrencyConverter:
    """Service for currency conversion and exchange rate management"""
    
    def __init__(self):
        self.api_key = api_config.EXCHANGERATE_API_KEY
        self.base_url = api_config.EXCHANGE_RATE_URL
        self.session = requests.Session()
        
        # Cache for exchange rates (to avoid frequent API calls)
        self.rate_cache = {}
        self.cache_timestamp = None
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        
        # Fallback exchange rates (approximate, updated periodically)
        self.fallback_rates = {
            'USD': 1.0,  # Base currency
            'EUR': 0.85,
            'GBP': 0.73,
            'INR': 83.12,
            'JPY': 149.50,
            'CAD': 1.36,
            'AUD': 1.52,
            'CHF': 0.88,
            'CNY': 7.24,
            'SGD': 1.34
        }
        
        # Currency symbols
        self.currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'INR': '₹',
            'JPY': '¥',
            'CAD': 'C$',
            'AUD': 'A$',
            'CHF': 'CHF',
            'CNY': '¥',
            'SGD': 'S$'
        }
    
    def get_exchange_rate(self, from_currency: str = 'USD', to_currency: str = 'USD') -> float:
        """Get exchange rate between two currencies"""
        if from_currency == to_currency:
            return 1.0
        
        try:
            # Check cache first
            if self._is_cache_valid():
                rate_key = f"{from_currency}_{to_currency}"
                if rate_key in self.rate_cache:
                    return self.rate_cache[rate_key]
            
            # Fetch fresh rates
            rates = self._fetch_exchange_rates(from_currency)
            if rates and to_currency in rates:
                rate = rates[to_currency]
                
                # Update cache
                self._update_cache(from_currency, rates)
                
                return rate
            
            # Fallback to stored rates
            return self._get_fallback_rate(from_currency, to_currency)
            
        except Exception as e:
            print(f"Error getting exchange rate: {e}")
            return self._get_fallback_rate(from_currency, to_currency)
    
    def convert_amount(self, amount: float, from_currency: str = 'USD', to_currency: str = 'USD') -> float:
        """Convert amount from one currency to another"""
        if amount <= 0:
            return 0.0
        
        rate = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * rate
        
        return round(converted_amount, 2)
    
    def convert_expenses(self, expense_breakdown: Dict[str, Any], target_currency: str) -> Dict[str, Any]:
        """Convert all expenses to target currency"""
        base_currency = expense_breakdown.get('base_currency', 'USD')
        
        if base_currency == target_currency:
            # Add currency symbols and return
            return self._add_currency_formatting(expense_breakdown, target_currency)
        
        try:
            conversion_rate = self.get_exchange_rate(base_currency, target_currency)
            
            converted_expenses = {
                'base_currency': base_currency,
                'target_currency': target_currency,
                'conversion_rate': conversion_rate,
                'converted_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'original_total': expense_breakdown.get('total_cost', 0),
                'converted_total': 0
            }
            
            # Convert all expense categories
            categories_to_convert = [
                'accommodation_cost', 'food_cost', 'activities_cost', 
                'transportation_cost', 'miscellaneous_cost', 'total_cost'
            ]
            
            for category in categories_to_convert:
                if category in expense_breakdown:
                    original_amount = expense_breakdown[category]
                    converted_amount = self.convert_amount(original_amount, base_currency, target_currency)
                    converted_expenses[category] = converted_amount
                    
                    if category == 'total_cost':
                        converted_expenses['converted_total'] = converted_amount
            
            # Convert daily budget if available
            if 'daily_budget' in expense_breakdown:
                converted_expenses['daily_budget'] = self.convert_amount(
                    expense_breakdown['daily_budget'], base_currency, target_currency
                )
            
            # Add detailed breakdown if available
            if 'detailed_breakdown' in expense_breakdown:
                converted_expenses['detailed_breakdown'] = self._convert_detailed_breakdown(
                    expense_breakdown['detailed_breakdown'], base_currency, target_currency
                )
            
            # Add currency formatting
            converted_expenses = self._add_currency_formatting(converted_expenses, target_currency)
            
            return converted_expenses
            
        except Exception as e:
            print(f"Error converting expenses: {e}")
            # Return original with currency formatting
            return self._add_currency_formatting(expense_breakdown, base_currency)
    
    def _fetch_exchange_rates(self, base_currency: str) -> Optional[Dict[str, float]]:
        """Fetch exchange rates from API"""
        try:
            if self.api_key:
                # Use paid API if key available
                url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{base_currency}"
            else:
                # Use free API
                url = f"{self.base_url}/{base_currency}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'rates' in data:
                return data['rates']
            elif 'conversion_rates' in data:  # Different API format
                return data['conversion_rates']
            
            return None
            
        except Exception as e:
            print(f"Failed to fetch exchange rates: {e}")
            return None
    
    def _get_fallback_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate using fallback rates"""
        try:
            from_rate = self.fallback_rates.get(from_currency, 1.0)
            to_rate = self.fallback_rates.get(to_currency, 1.0)
            
            # Convert via USD
            if from_currency != 'USD':
                usd_amount = 1.0 / from_rate
            else:
                usd_amount = 1.0
            
            if to_currency != 'USD':
                final_rate = usd_amount * to_rate
            else:
                final_rate = usd_amount
            
            return round(final_rate, 4)
            
        except Exception:
            return 1.0  # Safe fallback
    
    def _is_cache_valid(self) -> bool:
        """Check if cached exchange rates are still valid"""
        if not self.cache_timestamp:
            return False
        
        return datetime.now() - self.cache_timestamp < self.cache_duration
    
    def _update_cache(self, base_currency: str, rates: Dict[str, float]):
        """Update exchange rate cache"""
        self.cache_timestamp = datetime.now()
        
        # Store rates with base currency prefix
        for currency, rate in rates.items():
            cache_key = f"{base_currency}_{currency}"
            self.rate_cache[cache_key] = rate
    
    def _convert_detailed_breakdown(self, detailed_breakdown: Dict, from_currency: str, to_currency: str) -> Dict:
        """Convert detailed expense breakdown"""
        converted_breakdown = {}
        
        for category, items in detailed_breakdown.items():
            if isinstance(items, list):
                converted_items = []
                for item in items:
                    if isinstance(item, dict) and 'cost' in item:
                        converted_item = item.copy()
                        converted_item['cost'] = self.convert_amount(
                            item['cost'], from_currency, to_currency
                        )
                        converted_items.append(converted_item)
                    else:
                        converted_items.append(item)
                converted_breakdown[category] = converted_items
            elif isinstance(items, (int, float)):
                converted_breakdown[category] = self.convert_amount(items, from_currency, to_currency)
            else:
                converted_breakdown[category] = items
        
        return converted_breakdown
    
    def _add_currency_formatting(self, expenses: Dict[str, Any], currency: str) -> Dict[str, Any]:
        """Add currency symbols and formatting to expense dictionary"""
        symbol = self.currency_symbols.get(currency, currency)
        formatted_expenses = expenses.copy()
        
        # Add currency info
        formatted_expenses['currency_symbol'] = symbol
        formatted_expenses['currency_code'] = currency
        
        # Add formatted strings for display
        amount_fields = [
            'accommodation_cost', 'food_cost', 'activities_cost',
            'transportation_cost', 'miscellaneous_cost', 'total_cost',
            'daily_budget', 'converted_total'
        ]
        
        for field in amount_fields:
            if field in formatted_expenses and isinstance(formatted_expenses[field], (int, float)):
                amount = formatted_expenses[field]
                formatted_expenses[f"{field}_formatted"] = f"{symbol}{amount:,.2f}"
        
        return formatted_expenses
    
    def get_supported_currencies(self) -> List[str]:
        """Get list of supported currencies"""
        return list(self.fallback_rates.keys())
    
    def get_currency_info(self, currency_code: str) -> Dict[str, str]:
        """Get information about a currency"""
        currency_names = {
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'GBP': 'British Pound',
            'INR': 'Indian Rupee',
            'JPY': 'Japanese Yen',
            'CAD': 'Canadian Dollar',
            'AUD': 'Australian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'SGD': 'Singapore Dollar'
        }
        
        return {
            'code': currency_code,
            'name': currency_names.get(currency_code, currency_code),
            'symbol': self.currency_symbols.get(currency_code, currency_code)
        }
    
    def format_amount(self, amount: float, currency: str) -> str:
        """Format amount with currency symbol"""
        symbol = self.currency_symbols.get(currency, currency)
        return f"{symbol}{amount:,.2f}"
    
    def get_conversion_summary(self, from_currency: str, to_currency: str, amount: float = 1.0) -> Dict[str, Any]:
        """Get conversion summary with rate information"""
        rate = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = self.convert_amount(amount, from_currency, to_currency)
        
        return {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'exchange_rate': rate,
            'original_amount': amount,
            'converted_amount': converted_amount,
            'formatted_original': self.format_amount(amount, from_currency),
            'formatted_converted': self.format_amount(converted_amount, to_currency),
            'rate_date': datetime.now().strftime('%Y-%m-%d'),
            'rate_info': f"1 {from_currency} = {rate:.4f} {to_currency}"
        }