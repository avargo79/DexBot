# DexBot Usage Examples

This guide provides practical examples for using DexBot's core systems and utilities. These examples demonstrate real-world usage patterns for common development tasks.

## Table of Contents

- [UO Item Database System](#uo-item-database-system)
- [Looting System Integration](#looting-system-integration)
- [Configuration Management](#configuration-management)
- [Testing and Development](#testing-and-development)

## UO Item Database System

The UO Item Database provides a comprehensive JSON-based system for item lookups, categorization, and metadata management. This system is essential for building efficient looting configurations and item recognition.

### Basic Item Lookups

```python
# Import the database utility
from utils.uo_items import get_item_database

# Get the database instance
db = get_item_database()

# Look up an item by decimal ID
gold_item = db.get_item_by_id(3821)  # Gold Coins
if gold_item:
    print(f"Found: {gold_item['name']} (Hex: {gold_item['hex_id']})")
    print(f"Value Tier: {gold_item.get('value_tier', 'unknown')}")
    print(f"Stackable: {gold_item.get('stackable', False)}")

# Look up an item by hex ID
diamond_item = db.get_item_by_hex("0x0F16")  # Diamond
if diamond_item:
    print(f"Found: {diamond_item['name']} (Decimal: {diamond_item['decimal_id']})")
    print(f"Aliases: {diamond_item.get('aliases', [])}")
```

### Searching and Filtering

```python
# Search by name/alias (partial matching)
gem_items = db.find_items_by_name("gem")
for item in gem_items[:3]:  # Show first 3 matches
    print(f"- {item['name']} (ID: {item['decimal_id']}, Hex: {item['hex_id']})")

# Get all items in a category
currency_items = db.get_items_by_category("currency")
for item_key, item_data in currency_items.items():
    print(f"- {item_data['name']} (ID: {item_data['decimal_id']})")

# Get items by value tier
high_value_items = db.get_items_by_value_tier("very_high")
for item in high_value_items[:5]:  # Show first 5
    print(f"- {item['name']} (ID: {item['decimal_id']}) - {item.get('category', 'unknown')} category")
```

### Database Statistics

```python
# Get comprehensive database statistics
stats = db.get_database_stats()
print(f"Total categories: {stats['total_categories']}")
print(f"Total items: {stats['total_items']}")
print(f"Categories: {', '.join(stats['categories'])}")
```

## Looting System Integration

The UO Item Database integrates seamlessly with the looting system to enable dynamic, configuration-driven loot management.

### Building Dynamic Loot Lists

```python
# Build a comprehensive loot list using database queries
loot_ids = []

# Add all currency items
for item_key, item_data in db.get_items_by_category("currency").items():
    loot_ids.append(item_data['decimal_id'])

# Add all very high value items
for item in db.get_items_by_value_tier("very_high"):
    loot_ids.append(item['decimal_id'])

# Remove duplicates and sort
final_loot_ids = sorted(set(loot_ids))
print(f"Generated loot list: {final_loot_ids}")
```

### Converting Name-Based Config to IDs

```python
# Convert user-friendly names to item IDs for looting configuration
loot_config = [
    "Gold", "Gem", "Diamond", "Ruby", "Emerald", 
    "Reagent", "Potion", "Magic"
]

resolved_ids = []
for item_name in loot_config:
    items = db.find_items_by_name(item_name.lower())
    if items:
        for item in items:
            resolved_ids.append(item['decimal_id'])
            print(f"'{item_name}' -> {item['name']} (ID: {item['decimal_id']})")
    else:
        print(f"'{item_name}' -> Not found in database")

final_ids = sorted(set(resolved_ids))
print(f"Final loot IDs: {final_ids}")
```

### Integration with Looting System Configuration

```python
# Example: Update looting configuration with database-driven item lists
from config.config_manager import ConfigManager

config_manager = ConfigManager()

# Get current looting config
looting_config = config_manager.get_config("looting")

# Build high-value item list from database
high_value_ids = [item['decimal_id'] for item in db.get_items_by_value_tier("very_high")]

# Update configuration
looting_config['high_value_items'] = high_value_ids
config_manager.update_config("looting", looting_config)

print(f"Updated looting config with {len(high_value_ids)} high-value items")
```

## Configuration Management

Examples of working with DexBot's configuration system for customizing bot behavior.

### Loading and Modifying Configurations

```python
from config.config_manager import ConfigManager

# Initialize configuration manager
config_manager = ConfigManager()

# Load specific system configuration
auto_heal_config = config_manager.get_config("auto_heal")
print(f"Current healing threshold: {auto_heal_config.get('heal_threshold', 'Not set')}")

# Modify configuration
auto_heal_config['heal_threshold'] = 75
auto_heal_config['use_bandages'] = True

# Save updated configuration
config_manager.update_config("auto_heal", auto_heal_config)
```

### Creating Custom Configuration Profiles

```python
# Create a custom combat configuration for specific scenarios
combat_config = {
    "auto_target": True,
    "attack_range": 10,
    "preferred_weapons": ["bow", "crossbow"],
    "flee_health_threshold": 25,
    "target_priority": ["murderer", "criminal", "hostile"]
}

# Save as a new configuration profile
config_manager.save_config("combat_ranged", combat_config)
print("Created custom ranged combat configuration")
```

## Testing and Development

Examples for testing and validating DexBot functionality during development.

### Running System Tests

```python
# Example of testing the auto-heal system
from systems.auto_heal import AutoHealSystem
from config.config_manager import ConfigManager

# Initialize system with test configuration
config = {
    "heal_threshold": 80,
    "use_potions": True,
    "use_bandages": True,
    "potion_delay": 10
}

auto_heal = AutoHealSystem(config)

# Simulate test scenarios
test_scenarios = [
    {"player_health": 60, "max_health": 100, "expected": "should_heal"},
    {"player_health": 90, "max_health": 100, "expected": "no_heal"},
]

for scenario in test_scenarios:
    # Mock player health for testing
    result = auto_heal.should_heal(scenario["player_health"], scenario["max_health"])
    print(f"Health {scenario['player_health']}/{scenario['max_health']}: {result}")
```

### Performance Profiling

```python
import time
from utils.uo_items import get_item_database

# Performance test for database lookups
db = get_item_database()

# Test lookup performance
start_time = time.time()
for i in range(1000):
    item = db.get_item_by_id(3821)  # Gold lookup
end_time = time.time()

print(f"1000 database lookups took {end_time - start_time:.4f} seconds")
print(f"Average lookup time: {(end_time - start_time) / 1000 * 1000:.2f} ms")
```

## Running the Examples

To run these examples in your development environment:

1. **Ensure DexBot Environment**: Make sure you're in the RazorEnhanced scripting environment
2. **Import Path Setup**: The examples assume the DexBot `src` directory is in your Python path
3. **Configuration Files**: Ensure required configuration files exist in the `config/` directory
4. **Database Files**: Verify the UO item database files are present in the `ref/` directory

### Example Script Template

```python
"""
Template for running DexBot usage examples.
"""
import sys
import os

# Add DexBot src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Your example code here."""
    try:
        # Your example implementation
        pass
        
    except Exception as e:
        print(f"❌ Error running example: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
```

## Best Practices

### Error Handling
- Always wrap database operations in try-catch blocks
- Validate item IDs and configurations before using them
- Use the Logger system for debugging and error tracking

### Performance Considerations
- Cache database instances rather than creating new ones repeatedly
- Use batch operations when processing multiple items
- Consider memory usage for long-running bot sessions (12+ hours)

### Integration Patterns
- Follow the modular architecture when extending systems
- Use the ConfigManager for all configuration operations
- Implement proper logging for debugging and monitoring

## Related Documentation

- **[Development Guide](DEVELOPMENT_GUIDE.md)** - Complete development workflow
- **[Features & Capabilities](FEATURES.md)** - System feature documentation
- **[Project Status](PROJECT_STATUS.md)** - Current implementation status
- **[Product Requirements](prds/README.md)** - Detailed feature specifications

For additional examples and the complete runnable code, see the `examples/` directory in the project root.
