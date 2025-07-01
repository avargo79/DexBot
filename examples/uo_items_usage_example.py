"""
Example: Using the UO Item Database System

This example demonstrates how to use the new JSON-based UO item database
and utility module for script-friendly item lookups.
"""

import sys
import os

# Add the src directory to path to import from DexBot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.uo_items import get_item_database


def main():
    """Demonstrate UO item database usage."""
    print("=== UO Item Database Usage Example ===\n")
    
    # Get the database instance
    db = get_item_database()
    
    # Example 1: Look up an item by decimal ID
    print("1. Looking up item by decimal ID (3821 = Gold Coins)")
    gold_item = db.get_item_by_id(3821)
    if gold_item:
        print(f"   Found: {gold_item['name']} (Hex: {gold_item['hex_id']})")
        print(f"   Value Tier: {gold_item.get('value_tier', 'unknown')}")
        print(f"   Stackable: {gold_item.get('stackable', False)}")
    else:
        print("   Item not found")
    print()
    
    # Example 2: Look up an item by hex ID
    print("2. Looking up item by hex ID (0x0F16 = Diamond)")
    diamond_item = db.get_item_by_hex("0x0F16")
    if diamond_item:
        print(f"   Found: {diamond_item['name']} (Decimal: {diamond_item['decimal_id']})")
        print(f"   Aliases: {diamond_item.get('aliases', [])}")
    print()
    
    # Example 3: Search by name/alias
    print("3. Searching for items by name/alias 'gem'")
    gem_items = db.find_items_by_name("gem")
    for item in gem_items[:3]:  # Show first 3 matches
        print(f"   - {item['name']} (ID: {item['decimal_id']}, Hex: {item['hex_id']})")
    if len(gem_items) > 3:
        print(f"   ... and {len(gem_items) - 3} more")
    print()
    
    # Example 4: Get all items in a category
    print("4. Getting all currency items")
    currency_items = db.get_items_by_category("currency")
    for item_key, item_data in currency_items.items():
        print(f"   - {item_data['name']} (ID: {item_data['decimal_id']})")
    print()
    
    # Example 5: Get items by value tier
    print("5. Getting high-value items")
    high_value_items = db.get_items_by_value_tier("very_high")
    for item in high_value_items[:5]:  # Show first 5
        print(f"   - {item['name']} (ID: {item['decimal_id']}) - {item.get('category', 'unknown')} category")
    print()
    
    # Example 6: Practical usage for looting configuration
    print("6. Practical example: Building a loot list")
    loot_ids = []
    
    # Add all currency items
    for item_key, item_data in db.get_items_by_category("currency").items():
        loot_ids.append(item_data['decimal_id'])
    
    # Add all very high value items
    for item in db.get_items_by_value_tier("very_high"):
        loot_ids.append(item['decimal_id'])
    
    print(f"   Generated loot list (decimal IDs): {sorted(set(loot_ids))}")
    print()
    
    # Example 7: Database statistics
    print("7. Database statistics")
    stats = db.get_database_stats()
    print(f"   Total categories: {stats['total_categories']}")
    print(f"   Total items: {stats['total_items']}")
    print(f"   Categories: {', '.join(stats['categories'])}")
    print()


def demonstrate_looting_integration():
    """Show how this could integrate with the looting system."""
    print("=== Looting System Integration Example ===\n")
    
    db = get_item_database()
    
    # Example: Convert string-based loot config to IDs
    loot_config = [
        "Gold", "Gem", "Diamond", "Ruby", "Emerald", 
        "Reagent", "Potion", "Magic"
    ]
    
    print("Converting loot configuration from names to IDs:")
    resolved_ids = []
    
    for item_name in loot_config:
        items = db.find_items_by_name(item_name.lower())
        if items:
            for item in items:
                resolved_ids.append(item['decimal_id'])
                print(f"   '{item_name}' -> {item['name']} (ID: {item['decimal_id']})")
        else:
            print(f"   '{item_name}' -> Not found in database")
    
    print(f"\nFinal loot IDs: {sorted(set(resolved_ids))}")
    print()


if __name__ == "__main__":
    try:
        main()
        demonstrate_looting_integration()
        print("✅ Example completed successfully!")
    except Exception as e:
        print(f"❌ Error running example: {e}")
        import traceback
        traceback.print_exc()
