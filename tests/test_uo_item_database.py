"""
UO Item Database Test Suite

Tests for the UO item database system including the JSON database,
utility functions, and integration capabilities.
"""

import unittest
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.uo_items import get_item_database, get_item_id, get_gem_ids, get_reagent_ids, get_potion_ids


class TestUOItemDatabase(unittest.TestCase):
    """Test the UO Item Database functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = get_item_database()
    
    def test_database_loads(self):
        """Test that the database loads successfully"""
        self.assertIsNotNone(self.db)
        self.assertIsInstance(self.db.data, dict)
        self.assertIn('metadata', self.db.data)
        self.assertIn('categories', self.db.data)
    
    def test_database_metadata(self):
        """Test database metadata is correct"""
        metadata = self.db.data.get('metadata', {})
        self.assertGreater(metadata.get('total_items', 0), 100)
        self.assertEqual(metadata.get('version'), '2.0')
        self.assertEqual(metadata.get('format'), 'JSON')
    
    def test_get_item_by_id(self):
        """Test getting items by decimal ID"""
        # Test gold coins (ID: 3821)
        gold = self.db.get_item_by_id(3821)
        self.assertIsNotNone(gold)
        self.assertEqual(gold['name'], 'Gold Coins')
        self.assertEqual(gold['hex_id'], '0x0EED')
        
        # Test non-existent item
        non_existent = self.db.get_item_by_id(99999)
        self.assertIsNone(non_existent)
    
    def test_get_item_by_hex(self):
        """Test getting items by hex ID"""
        # Test diamond (Hex: 0x0F16)
        diamond = self.db.get_item_by_hex('0x0F16')
        self.assertIsNotNone(diamond)
        self.assertEqual(diamond['name'], 'Diamond')
        
        # Test with different hex formats
        diamond2 = self.db.get_item_by_hex('0F16')
        self.assertIsNotNone(diamond2)
        self.assertEqual(diamond2['name'], 'Diamond')
    
    def test_find_items_by_name(self):
        """Test finding items by name/alias"""
        # Test finding gems
        gems = self.db.find_items_by_name('gem')
        self.assertGreater(len(gems), 5)  # Should find multiple gems
        
        # Test specific item name
        gold_items = self.db.find_items_by_name('gold')
        self.assertGreater(len(gold_items), 0)
    
    def test_get_items_by_category(self):
        """Test getting items by category"""
        # Test currency category
        currency = self.db.get_items_by_category('currency')
        self.assertIsInstance(currency, dict)
        self.assertIn('gold_coins', currency)
        
        # Test gems category
        gems = self.db.get_items_by_category('gems')
        self.assertIsInstance(gems, dict)
        self.assertGreater(len(gems), 5)
    
    def test_get_items_by_value_tier(self):
        """Test getting items by value tier"""
        high_value = self.db.get_items_by_value_tier('high')
        self.assertIsInstance(high_value, list)
        self.assertGreater(len(high_value), 0)
        
        very_high_value = self.db.get_items_by_value_tier('very_high')
        self.assertIsInstance(very_high_value, list)
    
    def test_utility_functions(self):
        """Test standalone utility functions"""
        # Test get_item_id
        gold_id = get_item_id('gold')
        self.assertIsNotNone(gold_id)
        self.assertIsInstance(gold_id, int)
        
        # Test category functions
        gem_ids = get_gem_ids()
        self.assertIsInstance(gem_ids, list)
        self.assertGreater(len(gem_ids), 5)
        
        reagent_ids = get_reagent_ids()
        self.assertIsInstance(reagent_ids, list)
        self.assertGreater(len(reagent_ids), 5)
        
        potion_ids = get_potion_ids()
        self.assertIsInstance(potion_ids, list)
        self.assertGreater(len(potion_ids), 5)


class TestUOItemDatabaseIntegration(unittest.TestCase):
    """Test UO Item Database integration scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = get_item_database()
    
    def test_loot_list_generation(self):
        """Test generating loot lists for the looting system"""
        # Simulate generating a loot list
        loot_items = []
        
        # Add all currency items
        currency = self.db.get_items_by_category('currency')
        for item_data in currency.values():
            loot_items.append(item_data['decimal_id'])
        
        # Add all gems
        gems = self.db.get_items_by_category('gems')
        for item_data in gems.values():
            loot_items.append(item_data['decimal_id'])
        
        self.assertGreater(len(loot_items), 5)
        self.assertIn(3821, loot_items)  # Gold coins should be included
    
    def test_name_to_id_conversion(self):
        """Test converting item names to IDs for configuration"""
        test_names = ['gold', 'gem', 'diamond', 'reagent', 'potion']
        
        for name in test_names:
            items = self.db.find_items_by_name(name)
            self.assertGreater(len(items), 0, f"Should find items for '{name}'")
    
    def test_database_completeness(self):
        """Test that database has comprehensive coverage"""
        categories = self.db.list_categories()
        
        # Should have key categories
        expected_categories = ['currency', 'gems', 'reagents', 'potions', 'weapons', 'armor']
        for category in expected_categories:
            self.assertIn(category, categories, f"Should have {category} category")
        
        # Should have reasonable number of items
        total_items = self.db.data.get('metadata', {}).get('total_items', 0)
        self.assertGreater(total_items, 100, "Should have substantial item coverage")


def main():
    """Run all UO item database tests"""
    print("=== UO Item Database Test Suite ===\n")
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTest(unittest.makeSuite(TestUOItemDatabase))
    suite.addTest(unittest.makeSuite(TestUOItemDatabaseIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    if result.wasSuccessful():
        print("\n✅ All UO Item Database tests passed!")
        return 0
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return 1


if __name__ == "__main__":
    exit(main())
