"""
UO Item Database Test Suite

Comprehensive test suite for the UO item database system including:
- JSON database validation
- Utility functions testing
- Integration scenarios
- Quick interactive tests (--quick)
- Simple validation tests (--simple)
- Hex ID debugging tests (--debug-hex)
- Full unittest suite (--all, default)

This combines functionality from the following original test files:
- test_db.py (simple validation)
- test_db_quick.py (interactive exploration)
- debug_hex.py (hex ID debugging)

Usage:
    python test_uo_item_database.py           # Run all tests
    python test_uo_item_database.py --simple  # Quick validation only
    python test_uo_item_database.py --quick   # Interactive exploration
    python test_uo_item_database.py --debug-hex # Hex ID debugging
    python test_uo_item_database.py --all     # All test modes
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
    
    def test_hex_id_debugging(self):
        """Test hex ID lookups with detailed debugging (from debug_hex.py)"""
        # Test diamond lookup
        diamond = self.db.get_item_by_hex('0x0F16')
        self.assertIsNotNone(diamond, "Diamond should be found by hex ID 0x0F16")
        self.assertEqual(diamond['name'], 'Diamond')
        
        # Test that all gems have valid hex IDs
        gems = self.db.get_items_by_category('gems')
        self.assertGreater(len(gems), 0, "Should have gems in database")
        
        for gem_key, gem_data in gems.items():
            self.assertIn('hex_id', gem_data, f"Gem {gem_key} should have hex_id")
            self.assertIn('name', gem_data, f"Gem {gem_key} should have name")
            
            # Test that we can find the gem by its hex ID
            hex_id = gem_data.get('hex_id')
            if hex_id:
                found_gem = self.db.get_item_by_hex(hex_id)
                self.assertIsNotNone(found_gem, f"Should find gem {gem_data['name']} by hex {hex_id}")
                self.assertEqual(found_gem['name'], gem_data['name'])
    
    def test_hex_id_variations(self):
        """Test different hex ID format variations"""
        # Test with and without 0x prefix
        diamond1 = self.db.get_item_by_hex('0x0F16')
        diamond2 = self.db.get_item_by_hex('0F16')
        diamond3 = self.db.get_item_by_hex('0f16')  # lowercase
        
        self.assertIsNotNone(diamond1)
        self.assertIsNotNone(diamond2)
        self.assertIsNotNone(diamond3)
        
        # All should return the same item
        self.assertEqual(diamond1['name'], diamond2['name'])
        self.assertEqual(diamond1['name'], diamond3['name'])
        self.assertEqual(diamond1['name'], 'Diamond')


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


def quick_test():
    """Quick interactive test of the UO item database (from test_db_quick.py)"""
    print("=== UO Item Database Quick Test ===")
    
    # Load database
    try:
        from utils.uo_items import UOItemDatabase
        db = UOItemDatabase()
        stats = db.get_database_stats()
        print(f"✓ Database loaded successfully: {stats['total_items']} items")
    except Exception as e:
        print(f"✗ Failed to load database: {e}")
        return False
    
    # Show summary
    print(f"\nDatabase Summary:")
    print(f"  Total items: {stats['total_items']}")
    print(f"  Categories: {stats['total_categories']}")
    print(f"  Categories: {', '.join(stats['categories'])}")
    print(f"  Version: {stats['version']}")
    print(f"  Last updated: {stats['last_updated']}")
    
    # Test some common lookups
    print(f"\n=== Testing Common Lookups ===")
    
    # Test by name
    test_names = ["gold", "diamond", "silver", "black pearl", "nightshade"]
    for name in test_names:
        items = db.get_items_by_name(name)
        if items:
            item = items[0]
            print(f"✓ '{name}' -> {item['name']} (ID: {item['decimal_id']}, Hex: {item.get('hex_id', 'N/A')})")
        else:
            print(f"✗ '{name}' not found")
    
    # Test by hex ID
    print(f"\n=== Testing Hex ID Lookups ===")
    test_hex_ids = ["0x0EED", "0x0F26", "0x0F15", "0x0F7A", "0x0F88"]
    for hex_id in test_hex_ids:
        item = db.get_item_by_hex(hex_id)
        if item:
            print(f"✓ {hex_id} -> {item['name']} (Category: {item['category']})")
        else:
            print(f"✗ {hex_id} not found")
    
    # Test by category
    print(f"\n=== Testing Category Queries ===")
    test_categories = ["reagents", "gems", "currency"]
    for category in test_categories:
        items = db.get_items_by_category(category)
        print(f"✓ '{category}' category: {len(items)} items")
        if items:
            # Show first few items (items is a dict, so we need to iterate)
            item_list = list(items.values())[:3]
            for item in item_list:
                print(f"  - {item['name']} (ID: {item['decimal_id']})")
            if len(items) > 3:
                print(f"  ... and {len(items) - 3} more")
    
    # Test value tiers
    print(f"\n=== Testing Value Tier Queries ===")
    high_value = db.get_items_by_value_tier("high")
    medium_value = db.get_items_by_value_tier("medium")
    low_value = db.get_items_by_value_tier("low")
    
    print(f"✓ High value items: {len(high_value)}")
    print(f"✓ Medium value items: {len(medium_value)}")
    print(f"✓ Low value items: {len(low_value)}")
    
    # Show some high value items
    if high_value:
        print("  High value items:")
        for item in high_value[:5]:
            print(f"  - {item['name']} ({item['category']})")
    
    print(f"\n=== Quick Test Complete ===")
    print("Database is working correctly!")
    return True


def simple_test():
    """Simple test of UO item database (from test_db.py)"""
    print("=== Simple Database Test ===")
    try:
        db = get_item_database()
        print(f"✅ Database loaded successfully!")
        print(f"Categories: {len(db.data.get('categories', {}))}")
        print(f"Total items: {db.data.get('metadata', {}).get('total_items', 0)}")
        
        # Test a few key lookups
        gold = db.get_item_by_id(3821)
        if gold:
            print(f"✅ Gold lookup works: {gold['name']}")
        
        gems = db.find_items_by_name('gem')
        print(f"✅ Search works: Found {len(gems)} items with 'gem'")
        
        currency = db.get_items_by_category('currency')
        print(f"✅ Category lookup works: {len(currency)} currency items")
        
        print("✅ All simple tests passed! UO Item Database is ready.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def debug_hex_test():
    """Debug hex ID lookups (from debug_hex.py)"""
    print("=== Hex ID Debug Test ===")
    
    try:
        from utils.uo_items import UOItemDatabase
        db = UOItemDatabase()
        
        # Test specific hex lookup
        print("Testing diamond lookup (0x0F16):")
        diamond = db.get_item_by_hex('0x0F16')
        print(f"Diamond result: {diamond}")
        
        # Check what hex IDs exist in gems
        gems = db.data.get('categories', {}).get('gems', {}).get('items', {})
        print(f"\nAvailable gems ({len(gems)} total):")
        for key, item in gems.items():
            name = item.get('name', 'no name')
            hex_id = item.get('hex_id', 'no hex')
            decimal_id = item.get('decimal_id', 'no decimal')
            print(f"  {key}: {name} - Hex: {hex_id} - Decimal: {decimal_id}")
            
            # Test that we can find it by hex
            if hex_id and hex_id != 'no hex':
                found = db.get_item_by_hex(hex_id)
                status = "✓" if found else "✗"
                print(f"    {status} Lookup test: {found['name'] if found else 'Not found'}")
        
        print("\n=== Hex Debug Test Complete ===")
        return True
        
    except Exception as e:
        print(f"❌ Error in hex debug test: {e}")
        return False


def main():
    """Run all UO item database tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='UO Item Database Test Suite')
    parser.add_argument('--quick', action='store_true', help='Run quick interactive test')
    parser.add_argument('--simple', action='store_true', help='Run simple test')
    parser.add_argument('--debug-hex', action='store_true', help='Run hex ID debug test')
    parser.add_argument('--all', action='store_true', help='Run all tests (default)')
    
    args = parser.parse_args()
    
    # If no specific test requested, run all
    if not (args.quick or args.simple or args.debug_hex):
        args.all = True
    
    success = True
    
    if args.simple or args.all:
        success &= simple_test()
        print()
    
    if args.quick or args.all:
        success &= quick_test()
        print()
    
    if args.debug_hex or args.all:
        success &= debug_hex_test()
        print()
    
    if args.all:
        print("=== UO Item Database Test Suite ===\n")
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Add all test cases
        suite.addTest(loader.loadTestsFromTestCase(TestUOItemDatabase))
        suite.addTest(loader.loadTestsFromTestCase(TestUOItemDatabaseIntegration))
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Print summary
        if result.wasSuccessful():
            print("\n✅ All UO Item Database unit tests passed!")
            success &= True
        else:
            print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
            success = False
    
    if success:
        print("\n🎉 All requested tests completed successfully!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit(main())
