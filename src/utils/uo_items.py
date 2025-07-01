"""
UO Item Database Utility

This module provides convenient access to the Ultima Online item database
for DexBot scripts and configuration.
"""

import json
import os
from typing import Dict, List, Optional, Union, Any


class UOItemDatabase:
    """Utility class for working with UO item IDs and data."""
    
    def __init__(self, database_path: str = None):
        """Initialize the database.
        
        Args:
            database_path: Path to the JSON database file. If None, uses default location.
        """
        if database_path is None:
            # Default to the ref directory
            database_path = os.path.join(os.path.dirname(__file__), '..', '..', 'ref', 'uo_item_database.json')
        
        self.database_path = database_path
        self.data = self._load_database()
    
    def _load_database(self) -> Dict[str, Any]:
        """Load the item database from JSON file."""
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: UO item database not found at {self.database_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in item database: {e}")
            return {}
    
    def get_item_by_id(self, item_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get item data by decimal ID.
        
        Args:
            item_id: The decimal item ID (int or str)
            
        Returns:
            Dict with item data or None if not found
        """
        item_id_str = str(item_id)
        lookup = self.data.get('quick_lookup', {}).get('by_decimal_id', {})
        
        if item_id_str in lookup:
            item_path = lookup[item_id_str]
            return self._get_item_by_path(item_path)
        
        return None
    
    def get_item_by_hex(self, hex_id: str) -> Optional[Dict[str, Any]]:
        """Get item data by hex ID.
        
        Args:
            hex_id: The hex item ID (e.g., '0x0F16')
            
        Returns:
            Dict with item data or None if not found
        """
        # Normalize hex format
        if not hex_id.startswith('0x'):
            hex_id = '0x' + hex_id.upper()
        else:
            hex_id = '0x' + hex_id[2:].upper()
        
        # Search through all categories
        categories = self.data.get('categories', {})
        for category_name, category_data in categories.items():
            items = category_data.get('items', {})
            for item_key, item_data in items.items():
                if item_data.get('hex_id', '').upper() == hex_id:
                    # Return a copy with additional metadata
                    result = item_data.copy()
                    result['key'] = item_key
                    result['category'] = category_name
                    return result
        
        return None

    def get_items_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Get items by name or alias.
        
        Args:
            name: The item name or alias to search for
            
        Returns:
            List of item data dictionaries
        """
        name_lower = name.lower()
        lookup = self.data.get('quick_lookup', {}).get('by_name', {})
        
        items = []
        if name_lower in lookup:
            for item_path in lookup[name_lower]:
                item_data = self._get_item_by_path(item_path)
                if item_data:
                    items.append(item_data)
        
        return items
    
    def find_items_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Find items by name or alias (alias for get_items_by_name for compatibility).
        
        Args:
            name: The item name or alias to search for
            
        Returns:
            List of matching item data dictionaries
        """
        return self.get_items_by_name(name)

    def get_items_by_value_tier(self, tier: str) -> List[Dict[str, Any]]:
        """Get items by value tier.
        
        Args:
            tier: Value tier ('very_high', 'high', 'medium', 'low')
            
        Returns:
            List of item data dictionaries
        """
        lookup = self.data.get('quick_lookup', {}).get('by_value_tier', {})
        
        items = []
        if tier in lookup:
            for item_path in lookup[tier]:
                item_data = self._get_item_by_path(item_path)
                if item_data:
                    items.append(item_data)
        
        return items
    
    def get_items_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """Get all items in a category.
        
        Args:
            category: Category name (e.g., 'gems', 'reagents', 'potions')
            
        Returns:
            Dictionary of items in the category
        """
        categories = self.data.get('categories', {})
        if category in categories:
            return categories[category].get('items', {})
        return {}
    
    def get_item_ids_by_name(self, name: str) -> List[int]:
        """Get decimal item IDs by name or alias.
        
        Args:
            name: The item name or alias
            
        Returns:
            List of decimal item IDs
        """
        items = self.get_items_by_name(name)
        return [item['decimal_id'] for item in items if 'decimal_id' in item]
    
    def get_valuable_items(self, min_tier: str = 'medium') -> List[int]:
        """Get item IDs for valuable items.
        
        Args:
            min_tier: Minimum value tier ('low', 'medium', 'high', 'very_high')
            
        Returns:
            List of decimal item IDs
        """
        tier_order = ['low', 'medium', 'high', 'very_high']
        if min_tier not in tier_order:
            return []
        
        min_index = tier_order.index(min_tier)
        valuable_tiers = tier_order[min_index:]
        
        item_ids = []
        for tier in valuable_tiers:
            items = self.get_items_by_value_tier(tier)
            item_ids.extend([item['decimal_id'] for item in items if 'decimal_id' in item])
        
        return list(set(item_ids))  # Remove duplicates
    
    def _get_item_by_path(self, path: str) -> Optional[Dict[str, Any]]:
        """Get item data by internal path (e.g., 'currency.gold_coins').
        
        Args:
            path: Dot-separated path to item
            
        Returns:
            Item data dictionary or None
        """
        try:
            parts = path.split('.')
            if len(parts) != 2:
                return None
            
            category, item_key = parts
            categories = self.data.get('categories', {})
            
            if category in categories and 'items' in categories[category]:
                items = categories[category]['items']
                if item_key in items:
                    # Add the item key for reference
                    item_data = items[item_key].copy()
                    item_data['key'] = item_key
                    item_data['category'] = category
                    return item_data
        except Exception:
            pass
        
        return None
    
    def list_categories(self) -> List[str]:
        """Get list of all available categories."""
        return list(self.data.get('categories', {}).keys())
    
    def get_category_info(self, category: str) -> Optional[str]:
        """Get description for a category."""
        categories = self.data.get('categories', {})
        if category in categories:
            return categories[category].get('description', '')
        return None
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the database.
        
        Returns:
            Dictionary with database statistics
        """
        categories = self.data.get('categories', {})
        total_items = 0
        category_names = []
        
        for category_name, category_data in categories.items():
            category_names.append(category_name)
            items = category_data.get('items', {})
            total_items += len(items)
        
        return {
            'total_categories': len(categories),
            'total_items': total_items,
            'categories': category_names,
            'version': self.data.get('metadata', {}).get('version', 'unknown'),
            'last_updated': self.data.get('metadata', {}).get('last_updated', 'unknown')
        }


# Convenience functions for common usage
def get_item_database() -> UOItemDatabase:
    """Get a shared instance of the item database."""
    if not hasattr(get_item_database, '_instance'):
        get_item_database._instance = UOItemDatabase()
    return get_item_database._instance


def get_item_id(name: str) -> Optional[int]:
    """Quick lookup for single item ID by name.
    
    Args:
        name: Item name or alias
        
    Returns:
        First matching decimal item ID or None
    """
    db = get_item_database()
    items = db.get_items_by_name(name)
    return items[0]['decimal_id'] if items else None


def get_gem_ids() -> List[int]:
    """Get all gem item IDs."""
    db = get_item_database()
    return db.get_item_ids_by_name('gem')


def get_reagent_ids() -> List[int]:
    """Get all reagent item IDs."""
    db = get_item_database()
    return db.get_item_ids_by_name('reagent')


def get_potion_ids() -> List[int]:
    """Get all potion item IDs."""
    db = get_item_database()
    return db.get_item_ids_by_name('potion')


def get_valuable_item_ids(min_tier: str = 'high') -> List[int]:
    """Get item IDs for valuable items."""
    db = get_item_database()
    return db.get_valuable_items(min_tier)


# Example usage for DexBot scripts
if __name__ == "__main__":
    # Example usage
    db = UOItemDatabase()
    
    print("=== UO Item Database Example Usage ===")
    
    # Get item by ID
    gold_item = db.get_item_by_id(3821)
    print(f"Item ID 3821: {gold_item['name'] if gold_item else 'Not found'}")
    
    # Get items by name
    gems = db.get_items_by_name('gem')
    print(f"Found {len(gems)} gems")
    
    # Get valuable items
    valuable = db.get_valuable_items('high')
    print(f"High-value item IDs: {valuable}")
    
    # Get category items
    potions = db.get_items_by_category('potions')
    print(f"Potion categories: {list(potions.keys())}")
    
    # Quick lookups
    print(f"Gold ID: {get_item_id('gold')}")
    print(f"Gem IDs: {get_gem_ids()}")
    print(f"Reagent IDs: {get_reagent_ids()}")
