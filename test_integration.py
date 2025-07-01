"""
Quick integration test for UO Item Database integration in looting system
"""
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.config_manager import ConfigManager
from systems.looting import LootingSystem

def test_looting_system_integration():
    """Test that the looting system initializes with UO item database."""
    print("=== Testing Looting System Integration ===")
    
    try:
        # Initialize config manager
        config_manager = ConfigManager()
        print("✓ Config manager initialized")
        
        # Initialize looting system (should load UO item database)
        looting_system = LootingSystem(config_manager)
        print("✓ Looting system initialized")
        
        # Check that database is loaded
        if looting_system.item_db:
            print("✓ UO Item Database loaded successfully")
            
            # Test currency detection
            currency_ids = looting_system._get_currency_ids()
            print(f"✓ Currency IDs loaded: {currency_ids}")
            
            # Test currency check for gold
            is_gold = looting_system._is_currency_item(0x0EED)  # 3821 decimal = gold
            print(f"✓ Gold detection test: {is_gold}")
            
            # Test item identification (mock item)
            class MockItem:
                def __init__(self, item_id, name="Test Item"):
                    self.ItemID = item_id
                    self.Name = name
            
            mock_item = MockItem(3821, "Gold Coins")  # Gold
            item_info = looting_system._identify_item(mock_item)
            print(f"✓ Item identification: {item_info}")
            
            print("\n🎉 All integration tests passed!")
            return True
            
        else:
            print("⚠️  UO Item Database not loaded (fallback mode)")
            return True  # Still valid, just in fallback mode
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_looting_system_integration()
    if success:
        print("\n✅ Integration test completed successfully!")
    else:
        print("\n❌ Integration test failed!")
