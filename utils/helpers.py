# Utility functions
from datetime import datetime, date
from typing import Dict, Any, Tuple, List
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount with currency symbol"""
    symbols = {
        'USD': '$', 'EUR': '€', 'GBP': '£', 'INR': '₹',
        'JPY': '¥', 'CAD': 'C$', 'AUD': 'A$'
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"

def calculate_days_between_dates(start_date: date, end_date: date) -> int:
    """Calculate number of days between two dates"""
    return (end_date - start_date).days

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def parse_date_string(date_str: str) -> date:
    """Parse date string in YYYY-MM-DD format"""
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def get_season_from_date(travel_date: date) -> str:
    """Determine season based on travel date (Northern Hemisphere)"""
    month = travel_date.month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"

def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage with error handling"""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 1)

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def group_items_by_key(items: List[Dict], key: str) -> Dict[str, List[Dict]]:
    """Group list of dictionaries by a specific key"""
    grouped = {}
    for item in items:
        group_key = item.get(key, 'Unknown')
        if group_key not in grouped:
            grouped[group_key] = []
        grouped[group_key].append(item)
    return grouped

def display_header():
    """Display application header"""
    print("\n" + "="*80)
    print("🤖 AI TRAVEL AGENT & EXPENSE PLANNER")
    print("="*80)
    print("Real-time Weather • Top Attractions • Cost Analysis • Complete Itinerary")
    print("="*80)

def save_to_file(content: str, filename: str) -> bool:
    """Save content to file with error handling"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False
