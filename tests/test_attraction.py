# Unit tests for attraction module
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.attraction_finder import AttractionFinder
from data.models import Attraction

class TestAttractionFinder(unittest.TestCase):
    """Test cases for AttractionFinder class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.finder = AttractionFinder()
        self.sample_trip_details = {
            'destination': 'Paris',
            'budget_range': 'mid-range',
            'preferences': {'interests': ['museums', 'food']},
            'group_size': 2
        }
    
    def test_create_mock_attractions(self):
        """Test that mock attractions are created correctly"""
        attractions = self.finder._get_mock_attractions(self.sample_trip_details)
        
        self.assertIsInstance(attractions, list)
        self.assertGreater(len(attractions), 0)
        
        for attraction in attractions:
            self.assertIsInstance(attraction, Attraction)
            self.assertEqual(attraction.type, 'attraction')
            self.assertIn('Paris', attraction.name)
    
    def test_estimate_cost(self):
        """Test cost estimation function"""
        cost = self.finder._estimate_cost('attraction', 'mid-range', 2)
        self.assertIsInstance(cost, float)
        self.assertGreater(cost, 0)

if __name__ == '__main__':
    unittest.main()
