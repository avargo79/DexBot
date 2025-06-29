"""
Test script for Combat System functionality
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.config_manager import ConfigManager
from systems.combat import CombatSystem
from core.logger import Logger

def test_combat_system():
    """Test basic combat system functionality"""
    print("🧪 Testing Combat System...")
    
    try:
        # Initialize config manager
        config_manager = ConfigManager()
        
        # Test config loading
        combat_enabled = config_manager.get_combat_setting('system_toggles.combat_system_enabled')
        print(f"✅ Combat system enabled setting: {combat_enabled}")
        
        max_range = config_manager.get_combat_setting('target_selection.max_range')
        print(f"✅ Max target range: {max_range}")
        
        priority_mode = config_manager.get_combat_setting('target_selection.priority_mode')
        print(f"✅ Target priority mode: {priority_mode}")
        
        # Initialize combat system
        combat_system = CombatSystem(config_manager)
        print("✅ Combat system initialized successfully")
        
        # Test target detection (will return empty list in development environment)
        targets = combat_system.detect_targets()
        print(f"✅ Target detection works - found {len(targets)} targets")
        
        # Test target selection with empty list
        selected = combat_system.select_target(targets)
        print(f"✅ Target selection works - selected: {selected}")
        
        # Test disengage
        combat_system.disengage()
        print("✅ Disengage works")
        
        print("🎉 All Combat System tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Combat System test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_combat_system()
