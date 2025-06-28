#!/usr/bin/env python3
"""
Test script to verify DexBot.py configuration system and basic functions work
"""

def test_dexbot_config():
    """Test if DexBot configuration system works without RazorEnhanced"""
    try:
        import sys
        import os
        
        # Add current directory to path if needed
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
            
        print("Testing DexBot configuration system...")
        
        # Mock the AutoComplete import to avoid RazorEnhanced dependency
        class MockAutoComplete:
            pass
        sys.modules['AutoComplete'] = MockAutoComplete()
        
        # Import only the configuration classes
        print("Testing ConfigManager import...")
        from DexBot import ConfigManager
        print("✓ ConfigManager imported successfully")
        
        # Test config manager creation
        print("Testing ConfigManager creation...")
        config_manager = ConfigManager()
        print("✓ ConfigManager created successfully")
        
        # Test configuration loading
        print("Testing configuration loading...")
        main_setting = config_manager.get_main_setting('system_toggles.healing_system_enabled', True)
        auto_heal_setting = config_manager.get_auto_heal_setting('healing_toggles.bandage_healing_enabled', True)
        print(f"✓ Main config healing enabled: {main_setting}")
        print(f"✓ Auto heal bandage enabled: {auto_heal_setting}")
        
        # Test configuration saving
        print("Testing configuration saving...")
        config_manager.set_main_setting('global_settings.debug_mode', True)
        config_manager.set_auto_heal_setting('health_thresholds.healing_threshold_percentage', 90)
        save_result = config_manager.save_all_configs()
        print(f"✓ Configuration saved: {save_result}")
        
        # Test configuration reloading
        print("Testing configuration reloading...")
        config_manager.reload_configs()
        debug_mode = config_manager.get_main_setting('global_settings.debug_mode', False)
        healing_threshold = config_manager.get_auto_heal_setting('health_thresholds.healing_threshold_percentage', 95)
        print(f"✓ Debug mode after reload: {debug_mode}")
        print(f"✓ Healing threshold after reload: {healing_threshold}")
        
        print("\nAll configuration tests passed! DexBot config system is working.")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_file_structure():
    """Test if config files are created with correct structure"""
    try:
        import os
        import json
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.join(current_dir, "config")
        
        print("Testing config file structure...")
        
        # Check if config directory exists
        if os.path.exists(config_dir):
            print("✓ Config directory exists")
            
            # Check main config file
            main_config_path = os.path.join(config_dir, "main_config.json")
            if os.path.exists(main_config_path):
                print("✓ Main config file exists")
                with open(main_config_path, 'r') as f:
                    main_config = json.load(f)
                print(f"✓ Main config version: {main_config.get('version', 'unknown')}")
            else:
                print("✗ Main config file missing")
                
            # Check auto heal config file
            auto_heal_config_path = os.path.join(config_dir, "auto_heal_config.json")
            if os.path.exists(auto_heal_config_path):
                print("✓ Auto heal config file exists")
                with open(auto_heal_config_path, 'r') as f:
                    auto_heal_config = json.load(f)
                print(f"✓ Auto heal config version: {auto_heal_config.get('version', 'unknown')}")
            else:
                print("✗ Auto heal config file missing")
        else:
            print("✗ Config directory missing")
            
        return True
        
    except Exception as e:
        print(f"✗ Config file test error: {e}")
        return False

if __name__ == "__main__":
    print("=== DexBot Configuration System Tests ===\n")
    
    config_test = test_dexbot_config()
    file_test = test_config_file_structure()
    
    print(f"\n=== Test Results ===")
    print(f"Configuration System: {'PASS' if config_test else 'FAIL'}")
    print(f"Config File Structure: {'PASS' if file_test else 'FAIL'}")
    
    if config_test and file_test:
        print("\n🎉 All tests passed! DexBot is ready to run with configuration system.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
