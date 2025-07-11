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
    
    def __init__(self, database_path: Optional[str] = None):
        """Initialize the database.
        
        Args:
            database_path: Path to the JSON database file. If None, uses default location.
        """
        if database_path is None:
            # Default to the ref directory - handle multiple execution contexts
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Try multiple possible locations for the database file
            possible_paths = [
                # For bundled script in DexBot directory
                os.path.join(script_dir, 'ref', 'uo_item_database.json'),
                # For bundled script in RazorEnhanced Scripts directory
                os.path.join(script_dir, 'DexBot', 'ref', 'uo_item_database.json'),
                # For development from src/utils/
                os.path.join(script_dir, '..', '..', 'ref', 'uo_item_database.json'),
                # For bundled script from dist/ directory
                os.path.join(script_dir, '..', 'ref', 'uo_item_database.json'),
                # Absolute path fallback
                r'C:\Program Files (x86)\Ultima Online Unchained\Data\Plugins\RazorEnhanced\Scripts\DexBot\ref\uo_item_database.json'
            ]
            
            database_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    database_path = path
                    break
            
            # If still not found, use the first path as default (will show proper error)
            if database_path is None:
                database_path = possible_paths[0]
        
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
                if item_data.get('hex_id', '').upper() == hex_id.upper():
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

    def get_items_by_ids(self, item_ids: List[Union[int, str]]) -> Dict[Union[int, str], Optional[Dict[str, Any]]]:
        """
        Get multiple items by their decimal IDs in a single operation.
        
        This method is optimized for bulk lookups commonly needed during
        corpse looting when evaluating multiple items simultaneously.
        
        Args:
            item_ids: List of decimal item IDs (int or str)
            
        Returns:
            Dictionary mapping item_id -> item_data (or None if not found)
            
        Example:
            results = db.get_items_by_ids([3821, 3862, 3859])
            for item_id, item_data in results.items():
                if item_data:
                    print(f"Found {item_data['name']} (ID: {item_id})")
        """
        results = {}
        lookup = self.data.get('quick_lookup', {}).get('by_decimal_id', {})
        
        for item_id in item_ids:
            item_id_str = str(item_id)
            if item_id_str in lookup:
                item_path = lookup[item_id_str]
                results[item_id] = self._get_item_by_path(item_path)
            else:
                results[item_id] = None
        
        return results

    def get_items_by_names(self, names: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get multiple items by their names in a single operation.
        
        Args:
            names: List of item names or aliases to search for
            
        Returns:
            Dictionary mapping name -> list of matching item_data
            
        Example:
            results = db.get_items_by_names(['gem', 'reagent', 'potion'])
            for name, items in results.items():
                print(f"Found {len(items)} items for '{name}'")
        """
        results = {}
        lookup = self.data.get('quick_lookup', {}).get('by_name', {})
        
        for name in names:
            name_lower = name.lower()
            items = []
            
            if name_lower in lookup:
                for item_path in lookup[name_lower]:
                    item_data = self._get_item_by_path(item_path)
                    if item_data:
                        items.append(item_data)
            
            results[name] = items
        
        return results

    def get_items_by_categories(self, categories: List[str]) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Get items from multiple categories in a single operation.
        
        Args:
            categories: List of category names
            
        Returns:
            Dictionary mapping category -> category_items
            
        Example:
            results = db.get_items_by_categories(['gems', 'reagents', 'potions'])
            for category, items in results.items():
                print(f"Category '{category}' has {len(items)} items")
        """
        results = {}
        db_categories = self.data.get('categories', {})
        
        for category in categories:
            if category in db_categories:
                results[category] = db_categories[category].get('items', {})
            else:
                results[category] = {}
        
        return results

    def evaluate_items_for_looting(self, item_ids: List[Union[int, str]], 
                                 value_threshold: str = 'medium') -> Dict[Union[int, str], Dict[str, Any]]:
        """
        Bulk evaluate items for looting decisions based on database information.
        
        This method is specifically designed for integration with the looting system,
        providing all necessary information for looting decisions in a single call.
        
        Args:
            item_ids: List of item IDs to evaluate
            value_threshold: Minimum value tier ('low', 'medium', 'high', 'very_high')
            
        Returns:
            Dictionary mapping item_id -> evaluation_result containing:
            - 'item_data': Full item information or None
            - 'should_loot': Boolean recommendation based on value tier
            - 'value_tier': Item's value tier or 'unknown'
            - 'category': Item's category or 'unknown'
            - 'reason': Text explanation of the decision
            
        Example:
            evaluations = db.evaluate_items_for_looting([3821, 3862, 9999])
            for item_id, eval_result in evaluations.items():
                if eval_result['should_loot']:
                    print(f"LOOT: {eval_result['reason']}")
        """
        tier_order = ['low', 'medium', 'high', 'very_high']
        threshold_index = tier_order.index(value_threshold) if value_threshold in tier_order else 1
        
        items_data = self.get_items_by_ids(item_ids)
        evaluations = {}
        
        for item_id, item_data in items_data.items():
            if item_data:
                value_tier = item_data.get('value_tier', 'low')
                category = item_data.get('category', 'unknown')
                
                # Determine if item meets threshold
                tier_index = tier_order.index(value_tier) if value_tier in tier_order else 0
                should_loot = tier_index >= threshold_index
                
                # Generate reason
                if should_loot:
                    reason = f"{item_data.get('name', 'Unknown')} ({value_tier} value {category})"
                else:
                    reason = f"Below {value_threshold} threshold ({value_tier} value)"
                
                evaluations[item_id] = {
                    'item_data': item_data,
                    'should_loot': should_loot,
                    'value_tier': value_tier,
                    'category': category,
                    'reason': reason
                }
            else:
                evaluations[item_id] = {
                    'item_data': None,
                    'should_loot': False,
                    'value_tier': 'unknown',
                    'category': 'unknown',
                    'reason': f'Item ID {item_id} not found in database'
                }
        
        return evaluations

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

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance-related statistics about the database.
        
        Returns:
            Dictionary containing performance metrics and cache statistics
        """
        quick_lookup = self.data.get('quick_lookup', {}) 
        categories = self.data.get('categories', {})
        
        return {
            'database_size_items': sum(len(cat_data.get('items', {})) for cat_data in categories.values()),
            'lookup_table_sizes': {
                'by_decimal_id': len(quick_lookup.get('by_decimal_id', {})),
                'by_name': len(quick_lookup.get('by_name', {})),
                'by_value_tier': len(quick_lookup.get('by_value_tier', {}))
            },
            'memory_usage_estimate': len(str(self.data)),
            'categories_available': list(categories.keys()),
            'value_tiers_available': list(quick_lookup.get('by_value_tier', {}).keys())
        }
        
    def get_available_categories(self) -> List[str]:
        """Get list of all available categories in the database.
        
        Returns:
            List of category names
        """
        categories = self.data.get('categories', {})
        return list(categories.keys())


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


# New bulk operation convenience functions
def evaluate_items_for_looting(item_ids: List[Union[int, str]], 
                             value_threshold: str = 'medium') -> Dict[Union[int, str], Dict[str, Any]]:
    """
    Bulk evaluate items for looting decisions - convenience function.
    
    Args:
        item_ids: List of item IDs to evaluate
        value_threshold: Minimum value tier ('low', 'medium', 'high', 'very_high')
        
    Returns:
        Dictionary mapping item_id -> evaluation_result
        
    Example:
        # Evaluate a corpse with multiple items
        corpse_items = [3821, 3862, 3859, 9999]  # Gold, Diamond, Ruby, Unknown
        evaluations = evaluate_items_for_looting(corpse_items, 'medium')
        
        loot_these = [item_id for item_id, eval_result in evaluations.items() 
                      if eval_result['should_loot']]
    """
    db = get_item_database()
    return db.evaluate_items_for_looting(item_ids, value_threshold)


def get_items_by_ids(item_ids: List[Union[int, str]]) -> Dict[Union[int, str], Optional[Dict[str, Any]]]:
    """
    Bulk lookup items by IDs - convenience function.
    
    Args:
        item_ids: List of decimal item IDs
        
    Returns:
        Dictionary mapping item_id -> item_data (or None if not found)
    """
    db = get_item_database()
    return db.get_items_by_ids(item_ids)


def get_database_performance_stats() -> Dict[str, Any]:
    """Get performance statistics about the UO Items Database."""
    db = get_item_database()
    return db.get_performance_stats()


