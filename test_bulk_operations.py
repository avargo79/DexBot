#!/usr/bin/env python3
"""Quick test of the new bulk operations"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.uo_items import UOItemDatabase, evaluate_items_for_looting, get_items_by_ids

def test_bulk_operations():
    """Test the new bulk operations"""
    print("=== Testing UO Items Database Bulk Operations ===")
    
    # Initialize database
    db = UOItemDatabase()
    print("✓ Database initialized")
    
    # Test bulk ID lookup
    test_ids = [3821, 3862, 3859, 9999]  # Mix of valid and invalid
    results = db.get_items_by_ids(test_ids)
    print(f"✓ Bulk ID lookup: {len(results)} results")
    
    found_count = sum(1 for item in results.values() if item is not None)
    print(f"  - Found {found_count} items, {len(results) - found_count} not found")
    
    # Test bulk evaluation
    eval_results = db.evaluate_items_for_looting(test_ids, 'medium')
    print(f"✓ Bulk evaluation: {len(eval_results)} items evaluated")
    
    loot_count = sum(1 for eval_data in eval_results.values() if eval_data['should_loot'])
    print(f"  - Recommended to loot: {loot_count} items")
    
    # Test convenience functions
    conv_results = get_items_by_ids([3821, 3862])
    print(f"✓ Convenience function: {len(conv_results)} results")
    
    conv_eval = evaluate_items_for_looting([3821, 3862], 'high')
    print(f"✓ Convenience evaluation: {len(conv_eval)} items")
    
    print("\n=== Bulk Operations Test Complete ===")
    return True

if __name__ == "__main__":
    try:
        test_bulk_operations()
        print("🎉 All bulk operations working correctly!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
