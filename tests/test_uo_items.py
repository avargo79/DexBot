"""
Test suite for utils.uo_items module
Tests the UOItemDatabase class with pass, fail, and edge case scenarios
Focus on the new UO item database optimization work
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.uo_items import UOItemDatabase, get_item_database, get_item_id, get_gem_ids, get_reagent_ids, get_potion_ids, get_valuable_item_ids, evaluate_items_for_looting, get_items_by_ids, get_database_performance_stats


class TestUOItemDatabaseClass(unittest.TestCase):
    """Test the UOItemDatabase class directly"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db_data = {
            "metadata": {
                "version": "2.0",
                "total_items": 5,
                "last_updated": "2025-06-30"
            },
            "categories": {
                "currency": {
                    "description": "Gold and currency items",
                    "items": {
                        "gold_coins": {
                            "decimal_id": 3821,
                            "hex_id": "0x0EED",
                            "name": "Gold Coins",
                            "aliases": ["gold"],
                            "value_tier": "high"
                        }
                    }
                },
                "gems": {
                    "description": "Precious gems",
                    "items": {
                        "diamond": {
                            "decimal_id": 3862,
                            "hex_id": "0x0F16", 
                            "name": "Diamond",
                            "aliases": ["gem"],
                            "value_tier": "very_high"
                        },
                        "ruby": {
                            "decimal_id": 3863,
                            "hex_id": "0x0F17",
                            "name": "Ruby", 
                            "aliases": ["gem"],
                            "value_tier": "high"
                        }
                    }
                }
            },
            "quick_lookup": {
                "by_decimal_id": {
                    "3821": "currency.gold_coins",
                    "3862": "gems.diamond",
                    "3863": "gems.ruby"
                },
                "by_name": {
                    "gold": ["currency.gold_coins"],
                    "gem": ["gems.diamond", "gems.ruby"]
                },
                "by_value_tier": {
                    "high": ["currency.gold_coins", "gems.ruby"],
                    "very_high": ["gems.diamond"]
                }
            }
        }

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join')
    @patch('os.path.dirname')
    def test_database_initialization_pass_case(self, mock_dirname, mock_join, mock_file):
        """Test UOItemDatabase initializes correctly with valid data"""
        mock_dirname.return_value = "/fake/src/utils"
        mock_join.return_value = "/fake/ref/uo_item_database.json"
        mock_file.return_value.read.return_value = json.dumps(self.mock_db_data)
        
        db = UOItemDatabase()
        self.assertIsNotNone(db.data)
        self.assertEqual(db.data["metadata"]["version"], "2.0")
        self.assertEqual(db.data["metadata"]["total_items"], 5)

    @patch('builtins.open', side_effect=FileNotFoundError())
    @patch('os.path.join')
    @patch('os.path.dirname')
    def test_database_initialization_fail_case(self, mock_dirname, mock_join, mock_file):
        """Test UOItemDatabase handles missing database file"""
        mock_dirname.return_value = "/fake/src/utils"
        mock_join.return_value = "/fake/ref/uo_item_database.json"
        
        db = UOItemDatabase()
        self.assertEqual(db.data, {})

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join')
    @patch('os.path.dirname')
    def test_database_initialization_edge_case(self, mock_dirname, mock_join, mock_file):
        """Test UOItemDatabase handles invalid JSON"""
        mock_dirname.return_value = "/fake/src/utils"
        mock_join.return_value = "/fake/ref/uo_item_database.json"
        mock_file.return_value.read.return_value = "invalid json"
        
        db = UOItemDatabase()
        self.assertEqual(db.data, {})

    def test_get_item_by_id_pass_cases(self):
        """Test get_item_by_id with valid IDs"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test with integer ID
            gold = db.get_item_by_id(3821)
            self.assertIsNotNone(gold)
            self.assertEqual(gold["name"], "Gold Coins")
            self.assertEqual(gold["category"], "currency")
            
            # Test with string ID
            diamond = db.get_item_by_id("3862")
            self.assertIsNotNone(diamond)
            self.assertEqual(diamond["name"], "Diamond")

    def test_get_item_by_id_fail_case(self):
        """Test get_item_by_id with invalid ID"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            result = db.get_item_by_id(99999)
            self.assertIsNone(result)

    def test_get_item_by_id_edge_cases(self):
        """Test get_item_by_id with edge cases"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test with None
            self.assertIsNone(db.get_item_by_id(None))
            
            # Test with negative ID
            self.assertIsNone(db.get_item_by_id(-1))
            
            # Test with float ID
            self.assertIsNone(db.get_item_by_id(3821.5))

    def test_get_item_by_hex_pass_cases(self):
        """Test get_item_by_hex with valid hex IDs"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test with proper 0x format
            diamond = db.get_item_by_hex("0x0F16")
            self.assertIsNotNone(diamond)
            self.assertEqual(diamond["name"], "Diamond")
            
            # Test without 0x prefix
            ruby = db.get_item_by_hex("0F17")
            self.assertIsNotNone(ruby)
            self.assertEqual(ruby["name"], "Ruby")

    def test_get_item_by_hex_fail_case(self):
        """Test get_item_by_hex with invalid hex ID"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            result = db.get_item_by_hex("0xFFFF")
            self.assertIsNone(result)

    def test_get_item_by_hex_edge_cases(self):
        """Test get_item_by_hex with edge cases"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test with lowercase hex
            diamond = db.get_item_by_hex("0x0f16")
            self.assertIsNotNone(diamond)
            self.assertEqual(diamond["name"], "Diamond")
            
            # Test with empty string
            self.assertIsNone(db.get_item_by_hex(""))
            
            # Test with invalid format
            self.assertIsNone(db.get_item_by_hex("not_hex"))

    def test_get_items_by_name_pass_cases(self):
        """Test get_items_by_name with valid names"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test finding gold
            gold_items = db.get_items_by_name("gold")
            self.assertEqual(len(gold_items), 1)
            self.assertEqual(gold_items[0]["name"], "Gold Coins")
            
            # Test finding gems (multiple results)
            gem_items = db.get_items_by_name("gem")
            self.assertEqual(len(gem_items), 2)
            gem_names = [item["name"] for item in gem_items]
            self.assertIn("Diamond", gem_names)
            self.assertIn("Ruby", gem_names)

    def test_get_items_by_name_fail_case(self):
        """Test get_items_by_name with invalid name"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            result = db.get_items_by_name("nonexistent")
            self.assertEqual(result, [])

    def test_get_items_by_name_edge_cases(self):
        """Test get_items_by_name with edge cases"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test with empty string
            self.assertEqual(db.get_items_by_name(""), [])
            
            # Test case insensitive (should work since we lowercase in lookup)
            gold_items = db.get_items_by_name("GOLD")
            self.assertEqual(len(gold_items), 1)

    def test_get_items_by_category_pass_cases(self):
        """Test get_items_by_category with valid categories"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test currency category
            currency = db.get_items_by_category("currency")
            self.assertIsInstance(currency, dict)
            self.assertIn("gold_coins", currency)
            
            # Test gems category
            gems = db.get_items_by_category("gems")
            self.assertIsInstance(gems, dict)
            self.assertEqual(len(gems), 2)
            self.assertIn("diamond", gems)
            self.assertIn("ruby", gems)

    def test_get_items_by_category_fail_case(self):
        """Test get_items_by_category with invalid category"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            result = db.get_items_by_category("nonexistent")
            self.assertEqual(result, {})

    def test_get_items_by_category_edge_cases(self):
        """Test get_items_by_category with edge cases"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test with empty string
            self.assertEqual(db.get_items_by_category(""), {})
            
            # Test with None
            self.assertEqual(db.get_items_by_category(None), {})

    def test_get_items_by_value_tier_pass_cases(self):
        """Test get_items_by_value_tier with valid tiers"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test high value tier
            high_items = db.get_items_by_value_tier("high")
            self.assertEqual(len(high_items), 2)
            
            # Test very high value tier
            very_high_items = db.get_items_by_value_tier("very_high")
            self.assertEqual(len(very_high_items), 1)
            self.assertEqual(very_high_items[0]["name"], "Diamond")

    def test_get_items_by_value_tier_fail_case(self):
        """Test get_items_by_value_tier with invalid tier"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            result = db.get_items_by_value_tier("invalid")
            self.assertEqual(result, [])

    def test_get_items_by_value_tier_edge_cases(self):
        """Test get_items_by_value_tier with edge cases"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            # Test with empty string
            self.assertEqual(db.get_items_by_value_tier(""), [])
            
            # Test with None
            self.assertEqual(db.get_items_by_value_tier(None), [])

    def test_get_database_stats_pass_case(self):
        """Test get_database_stats returns correct information"""
        with patch.object(UOItemDatabase, '_load_database', return_value=self.mock_db_data):
            db = UOItemDatabase()
            
            stats = db.get_database_stats()
            self.assertEqual(stats["total_categories"], 2)
            self.assertEqual(stats["total_items"], 3)  # Actual count, not metadata
            self.assertEqual(stats["version"], "2.0")
            self.assertIn("currency", stats["categories"])
            self.assertIn("gems", stats["categories"])


class TestConvenienceFunctions(unittest.TestCase):
    """Test the convenience functions for common usage"""

    @patch('utils.uo_items.get_item_database')
    def test_get_item_id_pass_case(self, mock_get_db):
        """Test get_item_id returns correct ID"""
        mock_db = MagicMock()
        mock_db.get_items_by_name.return_value = [{"decimal_id": 3821}]
        mock_get_db.return_value = mock_db
        
        result = get_item_id("gold")
        self.assertEqual(result, 3821)

    @patch('utils.uo_items.get_item_database')
    def test_get_item_id_fail_case(self, mock_get_db):
        """Test get_item_id returns None for unknown item"""
        mock_db = MagicMock()
        mock_db.get_items_by_name.return_value = []
        mock_get_db.return_value = mock_db
        
        result = get_item_id("nonexistent")
        self.assertIsNone(result)

    @patch('utils.uo_items.get_item_database')
    def test_get_item_id_edge_case(self, mock_get_db):
        """Test get_item_id with edge cases"""
        mock_db = MagicMock()
        mock_db.get_items_by_name.return_value = [{"name": "Gold", "no_decimal_id": True}]
        mock_get_db.return_value = mock_db
        
        # Should handle missing decimal_id gracefully
        with self.assertRaises(KeyError):
            get_item_id("gold")

    @patch('utils.uo_items.get_item_database')
    def test_get_gem_ids_pass_case(self, mock_get_db):
        """Test get_gem_ids returns list of gem IDs"""
        mock_db = MagicMock()
        mock_db.get_item_ids_by_name.return_value = [3862, 3863]
        mock_get_db.return_value = mock_db
        
        result = get_gem_ids()
        self.assertEqual(result, [3862, 3863])

    @patch('utils.uo_items.get_item_database')
    def test_get_gem_ids_fail_case(self, mock_get_db):
        """Test get_gem_ids with no gems found"""
        mock_db = MagicMock()
        mock_db.get_item_ids_by_name.return_value = []
        mock_get_db.return_value = mock_db
        
        result = get_gem_ids()
        self.assertEqual(result, [])

    @patch('utils.uo_items.get_item_database')
    def test_get_valuable_item_ids_pass_case(self, mock_get_db):
        """Test get_valuable_item_ids returns correct IDs"""
        mock_db = MagicMock()
        mock_db.get_valuable_items.return_value = [3821, 3862, 3863]
        mock_get_db.return_value = mock_db
        
        result = get_valuable_item_ids("high")
        self.assertEqual(result, [3821, 3862, 3863])

    @patch('utils.uo_items.get_item_database')
    def test_get_valuable_item_ids_fail_case(self, mock_get_db):
        """Test get_valuable_item_ids with invalid tier"""
        mock_db = MagicMock()
        mock_db.get_valuable_items.return_value = []
        mock_get_db.return_value = mock_db
        
        result = get_valuable_item_ids("invalid")
        self.assertEqual(result, [])

    @patch('utils.uo_items.get_item_database')
    def test_get_valuable_item_ids_edge_case(self, mock_get_db):
        """Test get_valuable_item_ids with edge cases"""
        mock_db = MagicMock()
        mock_db.get_valuable_items.return_value = [3821, 3862]
        mock_get_db.return_value = mock_db
        
        # Test with default tier
        result = get_valuable_item_ids()
        self.assertEqual(result, [3821, 3862])


class TestSingletonPattern(unittest.TestCase):
    """Test the singleton pattern for get_item_database"""

    def test_singleton_pass_case(self):
        """Test that singleton pattern returns same instance"""
        # Use the singleton function twice
        db1 = get_item_database()
        db2 = get_item_database()
        
        # Should be the same instance
        self.assertIs(db1, db2)


class TestBulkOperations(unittest.TestCase):
    """Test the new bulk operation methods"""
    
    def setUp(self):
        """Set up test fixtures for bulk operations"""
        self.mock_db_data = {
            "metadata": {
                "version": "2.0",
                "total_items": 5,
                "last_updated": "2025-06-30"
            },
            "categories": {
                "currency": {
                    "description": "Gold and currency items",
                    "items": {
                        "gold_coins": {
                            "decimal_id": 3821,
                            "hex_id": "0x0EED",
                            "name": "Gold Coins",
                            "aliases": ["gold"],
                            "value_tier": "high"
                        }
                    }
                },
                "gems": {
                    "description": "Precious gems",
                    "items": {
                        "diamond": {
                            "decimal_id": 3862,
                            "hex_id": "0x0F16", 
                            "name": "Diamond",
                            "aliases": ["gem"],
                            "value_tier": "very_high"
                        },
                        "ruby": {
                            "decimal_id": 3859,
                            "hex_id": "0x0F13",
                            "name": "Ruby",
                            "aliases": ["gem"],
                            "value_tier": "high"
                        }
                    }
                },
                "reagents": {
                    "description": "Spell reagents",
                    "items": {
                        "black_pearl": {
                            "decimal_id": 3962,
                            "hex_id": "0x0F7A",
                            "name": "Black Pearl",
                            "aliases": ["reagent"],
                            "value_tier": "medium"
                        }
                    }
                }
            },
            "quick_lookup": {
                "by_decimal_id": {
                    "3821": "currency.gold_coins",
                    "3862": "gems.diamond", 
                    "3859": "gems.ruby",
                    "3962": "reagents.black_pearl"
                },
                "by_name": {
                    "gold": ["currency.gold_coins"],
                    "gem": ["gems.diamond", "gems.ruby"],
                    "reagent": ["reagents.black_pearl"]
                },
                "by_value_tier": {
                    "very_high": ["gems.diamond"],
                    "high": ["currency.gold_coins", "gems.ruby"],
                    "medium": ["reagents.black_pearl"]
                }
            }
        }
    
    # Bulk ID Lookup Tests
    def test_get_items_by_ids_pass_case(self):
        """Test bulk ID lookup with valid IDs"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test bulk lookup
            results = db.get_items_by_ids([3821, 3862, 3859])
            
            # Should return all three items
            self.assertEqual(len(results), 3)
            self.assertIsNotNone(results[3821])
            self.assertIsNotNone(results[3862])
            self.assertIsNotNone(results[3859])
            
            # Check specific item data
            self.assertEqual(results[3821]['name'], 'Gold Coins')
            self.assertEqual(results[3862]['name'], 'Diamond')
            self.assertEqual(results[3859]['name'], 'Ruby')
    
    def test_get_items_by_ids_fail_case(self):
        """Test bulk ID lookup with invalid IDs"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test with non-existent IDs
            results = db.get_items_by_ids([9999, 8888])
            
            # Should return None for both
            self.assertEqual(len(results), 2)
            self.assertIsNone(results[9999])
            self.assertIsNone(results[8888])
    
    def test_get_items_by_ids_edge_case(self):
        """Test bulk ID lookup with mixed valid/invalid IDs"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test with mix of valid and invalid IDs
            results = db.get_items_by_ids([3821, 9999, 3862])
            
            # Should return mixed results
            self.assertEqual(len(results), 3)
            self.assertIsNotNone(results[3821])
            self.assertIsNone(results[9999])
            self.assertIsNotNone(results[3862])
    
    # Bulk Name Lookup Tests
    def test_get_items_by_names_pass_case(self):
        """Test bulk name lookup with valid names"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test bulk name lookup
            results = db.get_items_by_names(['gold', 'gem'])
            
            # Should return results for both names
            self.assertEqual(len(results), 2)
            self.assertEqual(len(results['gold']), 1)
            self.assertEqual(len(results['gem']), 2)  # Diamond and Ruby
            
            # Check specific results
            self.assertEqual(results['gold'][0]['name'], 'Gold Coins')
            gem_names = [item['name'] for item in results['gem']]
            self.assertIn('Diamond', gem_names)
            self.assertIn('Ruby', gem_names)
    
    def test_get_items_by_names_fail_case(self):
        """Test bulk name lookup with invalid names"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test with non-existent names
            results = db.get_items_by_names(['nonexistent', 'invalid'])
            
            # Should return empty lists
            self.assertEqual(len(results), 2)
            self.assertEqual(results['nonexistent'], [])
            self.assertEqual(results['invalid'], [])
    
    # Bulk Category Lookup Tests  
    def test_get_items_by_categories_pass_case(self):
        """Test bulk category lookup with valid categories"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test bulk category lookup
            results = db.get_items_by_categories(['currency', 'gems'])
            
            # Should return items for both categories
            self.assertEqual(len(results), 2)
            self.assertEqual(len(results['currency']), 1)
            self.assertEqual(len(results['gems']), 2)
            
            # Check specific results
            self.assertIn('gold_coins', results['currency'])
            self.assertIn('diamond', results['gems'])
            self.assertIn('ruby', results['gems'])
    
    def test_get_items_by_categories_fail_case(self):
        """Test bulk category lookup with invalid categories"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test with non-existent categories
            results = db.get_items_by_categories(['nonexistent', 'invalid'])
            
            # Should return empty dictionaries
            self.assertEqual(len(results), 2)
            self.assertEqual(results['nonexistent'], {})
            self.assertEqual(results['invalid'], {})
    
    # Bulk Looting Evaluation Tests
    def test_evaluate_items_for_looting_pass_case(self):
        """Test bulk looting evaluation with various items"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test evaluation with medium threshold
            results = db.evaluate_items_for_looting([3821, 3862, 3962], 'medium')
            
            # Should return evaluations for all items
            self.assertEqual(len(results), 3)
            
            # Check evaluation results
            self.assertTrue(results[3821]['should_loot'])  # Gold (high value)
            self.assertTrue(results[3862]['should_loot'])  # Diamond (very high value)
            self.assertTrue(results[3962]['should_loot'])  # Black Pearl (medium value)
            
            # Check reasons are provided
            self.assertIn('reason', results[3821])
            self.assertIn('reason', results[3862])
            self.assertIn('reason', results[3962])
    
    def test_evaluate_items_for_looting_fail_case(self):
        """Test bulk looting evaluation with high threshold"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test evaluation with high threshold
            results = db.evaluate_items_for_looting([3821, 3862, 3962], 'high')
            
            # Should return evaluations for all items
            self.assertEqual(len(results), 3)
            
            # Check evaluation results
            self.assertTrue(results[3821]['should_loot'])   # Gold (high value)
            self.assertTrue(results[3862]['should_loot'])   # Diamond (very high value)
            self.assertFalse(results[3962]['should_loot'])  # Black Pearl (medium value, below threshold)
    
    def test_evaluate_items_for_looting_edge_case(self):
        """Test bulk looting evaluation with unknown items"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Test evaluation with unknown item
            results = db.evaluate_items_for_looting([3821, 9999], 'medium')
            
            # Should return evaluations for both items
            self.assertEqual(len(results), 2)
            
            # Check evaluation results
            self.assertTrue(results[3821]['should_loot'])   # Gold (known item)
            self.assertFalse(results[9999]['should_loot'])  # Unknown item
            self.assertIn('not found', results[9999]['reason'])
    
    # Performance Stats Tests
    def test_get_performance_stats_pass_case(self):
        """Test performance stats retrieval"""
        with patch('builtins.open', mock_open(read_data=json.dumps(self.mock_db_data))):
            db = UOItemDatabase('test_db.json')
            
            # Get performance stats
            stats = db.get_performance_stats()
            
            # Should return comprehensive stats
            self.assertIn('database_size_items', stats)
            self.assertIn('lookup_table_sizes', stats)
            self.assertIn('memory_usage_estimate', stats)
            self.assertIn('categories_available', stats)
            self.assertIn('value_tiers_available', stats)
            
            # Check specific values
            self.assertEqual(stats['database_size_items'], 4)  # 4 total items
            self.assertEqual(len(stats['categories_available']), 3)  # 3 categories
            
            # Check lookup table sizes
            lookup_sizes = stats['lookup_table_sizes']
            self.assertEqual(lookup_sizes['by_decimal_id'], 4)
            self.assertEqual(lookup_sizes['by_name'], 3)
            self.assertEqual(lookup_sizes['by_value_tier'], 3)


class TestBulkConvenienceFunctions(unittest.TestCase):
    """Test the new bulk convenience functions"""
    
    @patch('utils.uo_items.get_item_database')
    def test_evaluate_items_for_looting_convenience_pass_case(self, mock_get_db):
        """Test the convenience function for bulk looting evaluation"""
        # Mock the database
        mock_db = MagicMock()
        mock_db.evaluate_items_for_looting.return_value = {
            3821: {'should_loot': True, 'reason': 'Gold Coins (high value currency)'},
            3862: {'should_loot': True, 'reason': 'Diamond (very_high value gems)'
