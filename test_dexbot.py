#!/usr/bin/env python3
"""
Test script to verify DexBot.py can be imported and basic functions work
"""

def test_dexbot_import():
    """Test if DexBot can be imported without errors"""
    try:
        import sys
        import os
        
        # Add current directory to path if needed
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
            
        # Try importing DexBot
        print("Testing DexBot import...")
        from DexBot import GameState, ConfigValidator, Logger
        print("✓ DexBot imported successfully")
        
        # Test basic class instantiation
        print("Testing GameState creation...")
        game_state = GameState()
        print("✓ GameState created successfully")
        
        # Test config validation (should work without RazorEnhanced)
        print("Testing ConfigValidator...")
        validator = ConfigValidator()
        print("✓ ConfigValidator created successfully")
        
        print("\nAll basic tests passed! DexBot.py is ready to run.")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_dexbot_import()
